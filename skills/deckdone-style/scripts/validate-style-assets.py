#!/usr/bin/env python3
"""Validate icon/illustration references in content-plan.md against style assets."""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET


def parse_icon_catalog(catalog_path):
    icons = set()
    try:
        with open(catalog_path, encoding="utf-8") as f:
            text = f.read()
    except (FileNotFoundError, OSError) as e:
        print(f"Error reading catalog: {e}", file=sys.stderr)
        return None

    skip = {
        "icon name",
        "theme",
        "also good for",
        "page type",
        "default icon",
        "zone position",
        "icon size",
        "when to use",
        "name",
        "required",
    }
    for match in re.finditer(
        r"^\|[^|]+\|\s*([a-z][a-z0-9-]+)\s*\|", text, re.MULTILINE
    ):
        name = match.group(1).strip()
        if name and name.lower() not in skip:
            icons.add(name)
    return icons


def check_icons_dir(icons_dir, catalog_icons):
    errors = []
    if not os.path.isdir(icons_dir):
        errors.append(f"Icons directory not found: {icons_dir}")
        return errors

    svg_files = set()
    for fname in os.listdir(icons_dir):
        if fname.endswith(".svg"):
            name = fname[:-4]
            svg_files.add(name)
            fpath = os.path.join(icons_dir, fname)
            try:
                tree = ET.parse(fpath)
                root = tree.getroot()
                if not root.tag.endswith("svg") and root.tag != "svg":
                    errors.append(f"{fname}: root element is not <svg>")
            except ET.ParseError as e:
                errors.append(f"{fname}: invalid XML ({e})")

    for icon_name in catalog_icons:
        if icon_name not in svg_files:
            errors.append(f"Catalog icon '{icon_name}' has no SVG in {icons_dir}")

    return errors


def parse_content_plan_icon_refs(plan_path):
    refs = {"icons": [], "illustrations": []}
    try:
        with open(plan_path, encoding="utf-8") as f:
            text = f.read()
    except (FileNotFoundError, OSError) as e:
        print(f"Error reading content plan: {e}", file=sys.stderr)
        return None

    for match in re.finditer(r"^\s*-\s*Icon\s*[:：]\s*(.+)$", text, re.MULTILINE):
        val = match.group(1).strip()
        if val and val.lower() != "none":
            refs["icons"].append(val)

    for match in re.finditer(
        r"^\s*-\s*Illustration\s*[:：]\s*(.+)$", text, re.MULTILINE
    ):
        val = match.group(1).strip()
        if val and val.lower() != "none":
            refs["illustrations"].append(val)

    return refs


def validate_icon_refs(icon_refs, catalog_icons, icons_dir):
    errors = []
    for icon_name in icon_refs:
        if icon_name not in catalog_icons:
            errors.append(f"Icon '{icon_name}' not found in catalog")
        else:
            svg_path = os.path.join(icons_dir, f"{icon_name}.svg")
            if not os.path.isfile(svg_path):
                errors.append(f"Icon '{icon_name}' catalog entry has no SVG file")
    return errors


def validate_illustration_refs(illust_refs):
    errors = []
    slug_re = re.compile(r"^[a-z0-9-]+$")
    for slug in illust_refs:
        if not slug_re.match(slug):
            errors.append(f"Invalid illustration slug format: '{slug}'")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate style asset references")
    parser.add_argument("content_plan", help="Path to content-plan.md")
    parser.add_argument("--catalog", required=True, help="Path to icon-catalog.md")
    parser.add_argument(
        "--icons-dir", required=True, help="Path to references/icons/ directory"
    )
    args = parser.parse_args()

    print("=== Style Assets Validation ===")
    all_errors = []

    catalog_icons = parse_icon_catalog(args.catalog)
    if catalog_icons is None:
        sys.exit(2)

    print(f"Catalog icons found: {len(catalog_icons)}")

    dir_errors = check_icons_dir(args.icons_dir, catalog_icons)
    if dir_errors:
        for e in dir_errors:
            print(f"  FAIL: {e}")
        all_errors.extend(dir_errors)
    else:
        print("  OK: All catalog icons have SVG files")

    refs = parse_content_plan_icon_refs(args.content_plan)
    if refs is None:
        sys.exit(2)

    print(f"\nContent plan icon refs: {len(refs['icons'])}")
    print(f"Content plan illustration refs: {len(refs['illustrations'])}")

    if refs["icons"]:
        icon_errors = validate_icon_refs(refs["icons"], catalog_icons, args.icons_dir)
        if icon_errors:
            for e in icon_errors:
                print(f"  FAIL: {e}")
            all_errors.extend(icon_errors)
        else:
            print("  OK: All icon refs valid")

    if refs["illustrations"]:
        illust_errors = validate_illustration_refs(refs["illustrations"])
        if illust_errors:
            for e in illust_errors:
                print(f"  FAIL: {e}")
            all_errors.extend(illust_errors)
        else:
            print("  OK: All illustration refs valid")

    print(f"\n=== Summary ===")
    if all_errors:
        print(f"FAIL: {len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print("PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
