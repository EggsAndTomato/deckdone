#!/usr/bin/env python3
"""Validates content-plan.md against structural rules for DeckDone."""

import re
import sys

VALID_PAGE_TYPES = {
    "Cover",
    "Agenda",
    "Section Divider",
    "Content-Text",
    "Content-TwoCol",
    "Data-Chart",
    "Quote",
    "Timeline",
    "Comparison",
    "Closing",
    "Composite-Diagram",
    "Pipeline-Flow",
}

VALID_VISUAL_WEIGHTS = {"primary", "secondary", "auxiliary"}

PLACEHOLDER_RE = re.compile(r"^\s*(TBD|TODO|PLACEHOLDER|N/A|---)\s*$", re.IGNORECASE)


def parse_slides(text):
    sections = re.split(r"^## Slide", text, flags=re.MULTILINE)
    slides = []
    for section in sections[1:]:
        title_match = re.match(r"\s*(\d+|.+?)(?:\n|$)", section)
        title = title_match.group(1).strip().rstrip(":") if title_match else "Untitled"
        slides.append((title, section))
    return slides


def extract_field(section, field_name):
    pattern = re.compile(
        rf"^\s*-?\s*{re.escape(field_name)}\s*[:：]\s*(.+)$", re.MULTILINE
    )
    m = pattern.search(section)
    return m.group(1).strip() if m else None


def extract_zones(section):
    zone_sections = re.split(r"^### Zone", section, flags=re.MULTILINE)
    zones = []
    for zs in zone_sections[1:]:
        label_match = re.match(r"\s*(\S+)", zs)
        label = label_match.group(1).strip().rstrip(":") if label_match else "?"
        zones.append((label, zs))
    return zones


def has_acceptance_criteria(section):
    ac_match = re.search(r"^#+\s*Acceptance Criteria", section, re.MULTILINE)
    if not ac_match:
        return False
    ac_body = section[ac_match.end() :]
    return bool(re.search(r"^- \[[ xX]\]", ac_body, re.MULTILINE))


def is_empty_content(value):
    if value is None:
        return True
    stripped = value.strip()
    if not stripped:
        return True
    return bool(PLACEHOLDER_RE.match(stripped))


def validate_slide(title, section, catalog_icons=None):
    errors = []
    zone_errors = {}

    page_type = extract_field(section, "Page Type")
    if page_type is None:
        errors.append("Missing: Page Type field")
    elif page_type not in VALID_PAGE_TYPES:
        errors.append(f"Invalid Page Type: {page_type}")

    total_zones = extract_field(section, "Total Zones")
    if total_zones is None:
        errors.append("Missing: Total Zones field")
    else:
        try:
            tz = int(total_zones)
            if tz <= 0:
                raise ValueError
        except ValueError:
            errors.append(f"Invalid Total Zones: {total_zones}")

    zones = extract_zones(section)
    for label, zs in zones:
        z_errs = []
        zt = extract_field(zs, "Type")
        if zt is None:
            z_errs.append("missing Type field")

        content_val = extract_field(zs, "Content")
        if is_empty_content(content_val):
            z_errs.append("Content is empty")

        ml = extract_field(zs, "Max Length")
        if ml is None:
            z_errs.append("missing Max Length field")

        vw = extract_field(zs, "Visual Weight")
        if vw is None:
            z_errs.append("missing Visual Weight field")
        elif vw not in VALID_VISUAL_WEIGHTS:
            z_errs.append(f"invalid Visual Weight: {vw}")

        icon_val = extract_field(zs, "Icon")
        if icon_val is not None and icon_val.strip().lower() != "none":
            if catalog_icons is not None and icon_val.strip() not in catalog_icons:
                z_errs.append(f"icon '{icon_val.strip()}' not found in catalog")

        if z_errs:
            zone_errors[label] = z_errs

    if not has_acceptance_criteria(section):
        errors.append("Missing: Acceptance Criteria with checkboxes")

    return errors, zone_errors, len(zones)


def load_catalog_icons(catalog_path):
    icons = set()
    try:
        with open(catalog_path, encoding="utf-8") as f:
            text = f.read()
    except (FileNotFoundError, OSError):
        return None
    skip = {"icon name", "---", "-----------", "default icon", "zone position"}
    for m in re.finditer(r"^\|[^|]+\|\s*([a-z][a-z0-9-]+)\s*\|", text, re.MULTILINE):
        val = m.group(1).strip()
        if val.lower() not in skip:
            icons.add(val)
    for m in re.finditer(r"^\s*-\s+`([^`]+)`", text, re.MULTILINE):
        icons.add(m.group(1).strip())
    return icons if icons else None


def main():
    catalog_path = None
    args = sys.argv[1:]
    content_path = None
    i = 0
    while i < len(args):
        if args[i] == "--catalog" and i + 1 < len(args):
            catalog_path = args[i + 1]
            i += 2
        elif content_path is None:
            content_path = args[i]
            i += 1
        else:
            i += 1

    if content_path is None:
        print(
            "Usage: python validate-content-plan.py <content-plan.md> [--catalog <icon-catalog.md>]"
        )
        sys.exit(2)

    catalog_icons = None
    if catalog_path:
        catalog_icons = load_catalog_icons(catalog_path)
        if catalog_icons is None:
            print(f"Warning: Could not load icon catalog from {catalog_path}")
        else:
            print(f"Loaded {len(catalog_icons)} icons from catalog")

    try:
        with open(content_path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {content_path}")
        sys.exit(2)
    except OSError as e:
        print(f"Error reading file: {e}")
        sys.exit(2)

    slides = parse_slides(text)
    if not slides:
        print("No slides found. Ensure slides use '## Slide' headers.")
        sys.exit(2)

    print("=== Content Plan Validation ===")
    passed = 0
    failed = 0
    total_zones = 0

    for title, section in slides:
        errors, zone_errors, zone_count = validate_slide(
            title, section, catalog_icons=catalog_icons
        )
        total_zones += zone_count
        if not errors and not zone_errors:
            print(f"Slide {failed + passed + 1}: {title} - PASS ({zone_count} zones)")
            passed += 1
        else:
            print(f"Slide {failed + passed + 1}: {title} - FAIL")
            for err in errors:
                print(f"  - {err}")
            for zlabel, zerrs in zone_errors.items():
                for ze in zerrs:
                    print(f"  - Zone {zlabel}: {ze}")
            failed += 1

    print("\n=== Summary ===")
    print(f"Total slides: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total zones: {total_zones}")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
