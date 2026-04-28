#!/usr/bin/env python3
"""Validates SVG slide files for svg_to_pptx compatibility."""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

SAFE_FONTS = {
    "arial", "georgia", "verdana", "tahoma", "trebuchet ms",
    "times new roman", "courier new", "impact",
    "sans-serif", "serif", "monospace",
}

BANNED_LOCAL_NAMES = {
    "mask", "style", "foreignobject", "script", "iframe", "textpath",
}

VISUAL_ELEMENTS = {
    "rect", "circle", "ellipse", "line", "polyline", "polygon",
    "path", "text", "image", "use",
}


def _local_tag(elem):
    tag = elem.tag
    if isinstance(tag, str) and tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag if isinstance(tag, str) else ""


def _all_attrs(elem):
    return elem.attrib


def _attr_local(name):
    if name.startswith("{"):
        return name.split("}", 1)[1]
    return name


def _check_canvas(root, errors):
    tag = _local_tag(root).lower()
    if tag != "svg":
        errors.append("Root element is not <svg>")
        return

    viewbox = root.get("viewBox", "")
    if viewbox != "0 0 1280 720":
        errors.append(f'viewBox must be "0 0 1280 720", got "{viewbox}"')

    width = root.get("width", "")
    height = root.get("height", "")
    if str(width) != "1280":
        errors.append(f'width must be "1280", got "{width}"')
    if str(height) != "720":
        errors.append(f'height must be "720", got "{height}"')


def _check_banned_elements(root, errors):
    for elem in root.iter():
        name = _local_tag(elem).lower()
        if name in BANNED_LOCAL_NAMES:
            errors.append(f'Banned element <{name}>')
        if name.startswith("animate"):
            errors.append(f'Banned element <{name}>')


def _check_banned_attributes(root, errors):
    for elem in root.iter():
        name = _local_tag(elem).lower()
        for attr_name, attr_val in elem.attrib.items():
            if isinstance(attr_val, str) and "rgba(" in attr_val.lower():
                errors.append(
                    f'rgba() in {_attr_local(attr_name)} on <{name}>'
                )
        if name == "g" and "opacity" in elem.attrib:
            errors.append(
                f'<g opacity="{elem.attrib["opacity"]}"> — '
                "set opacity on each child element instead"
            )


def _check_fonts(root, errors):
    for elem in root.iter():
        name = _local_tag(elem).lower()
        style_val = elem.get("style", "")
        if not style_val:
            continue
        m = re.search(r"font-family\s*:\s*([^;\"'}]+)", style_val, re.IGNORECASE)
        if not m:
            continue
        fonts_str = m.group(1).strip().rstrip(";")
        for font in fonts_str.split(","):
            font_clean = font.strip().strip("'\"").lower()
            if font_clean and font_clean not in SAFE_FONTS:
                errors.append(
                    f'Unsafe font "{font.strip()}" on <{name}>'
                )


def _check_tspan(root, errors):
    for elem in root.iter():
        name = _local_tag(elem).lower()
        if name != "tspan":
            continue
        bad_attrs = []
        if "y" in elem.attrib:
            bad_attrs.append(f'y="{elem.attrib["y"]}"')
        if "dy" in elem.attrib:
            bad_attrs.append(f'dy="{elem.attrib["dy"]}"')
        if bad_attrs:
            errors.append(
                f'<tspan> with {", ".join(bad_attrs)} — '
                "use separate <text> elements per line"
            )


def _check_rect_rounded(root, errors):
    for elem in root.iter():
        name = _local_tag(elem).lower()
        if name != "rect":
            continue
        for attr in ("rx", "ry"):
            val = elem.get(attr)
            if val is None:
                continue
            try:
                if float(val) != 0:
                    errors.append(
                        f'<rect {attr}="{val}"> — '
                        "use <path> with arc commands for rounded rectangles"
                    )
            except ValueError:
                errors.append(
                    f'<rect {attr}="{val}"> — '
                    "use <path> with arc commands for rounded rectangles"
                )


def _check_images(root, filepath, errors):
    for elem in root.iter():
        name = _local_tag(elem).lower()
        if name != "image":
            continue
        href = elem.get("href") or elem.get(f"{{{XLINK_NS}}}href", "")
        if not href:
            continue
        if href.startswith("data:image/"):
            continue
        img_path = Path(filepath).parent / href
        if not img_path.exists():
            errors.append(f'Image not found: "{href}"')


def _check_icons(root, errors):
    for elem in root.iter():
        name = _local_tag(elem).lower()
        if name != "use":
            continue
        icon = elem.get("data-icon", "")
        if not icon:
            continue
        if not (
            icon.startswith("tabler-filled/")
            or icon.startswith("tabler-outline/")
        ):
            errors.append(
                f'Invalid icon: data-icon="{icon}" — '
                "must start with tabler-filled/ or tabler-outline/"
            )


def _check_nonempty(root, warnings):
    text_count = 0
    visual_count = 0
    for elem in root.iter():
        name = _local_tag(elem).lower()
        if name == "text":
            text_count += 1
        if name in VISUAL_ELEMENTS:
            visual_count += 1
    if text_count < 3 and visual_count < 5:
        warnings.append(
            f"Potentially empty: {text_count} <text> elements, "
            f"{visual_count} visual elements (need >=3 text or >=5 visual)"
        )


GRAPHICAL_ELEMENTS = {
    "rect", "circle", "ellipse", "line", "polyline", "polygon",
    "path", "image",
}

VISUAL_PAGE_TYPES = {
    "chart", "timeline", "pipeline", "flow", "comparison", "diagram",
    "matrix", "process", "data-chart", "content-diagram",
}


def _classify_page_type(filename, content_plan_pages):
    if content_plan_pages is None:
        return None
    base = filename.lower().replace("_", " ")
    for ptype in VISUAL_PAGE_TYPES:
        if ptype in base:
            return ptype
    page_num_match = re.match(r"p(\d+)", filename, re.IGNORECASE)
    if page_num_match and content_plan_pages:
        idx = int(page_num_match.group(1)) - 1
        if 0 <= idx < len(content_plan_pages):
            entry = content_plan_pages[idx]
            return entry[0] if isinstance(entry, tuple) else entry
    return None


def _check_graphical_elements(root, filename, content_plan_pages, errors):
    page_type = _classify_page_type(filename, content_plan_pages)
    if page_type is None:
        return

    graphical_count = 0
    for elem in root.iter():
        name = _local_tag(elem).lower()
        if name in GRAPHICAL_ELEMENTS:
            graphical_count += 1

    if graphical_count < 3:
        errors.append(
            f"Page type '{page_type}' requires graphical SVG elements "
            f"(<rect>, <circle>, <line>, <path>, etc.) for chart/diagram/pipeline "
            f"rendering, but only {graphical_count} found. "
            f"Use the matching chart template from templates/charts/ and populate "
            f"it with data instead of rendering chart data as text."
        )


DIAGRAM_MIN_ELEMENTS = {
    "hub-and-spoke": {"circle": 1, "path": 1},
    "pyramid": {"path": 3},
    "dual-gears": {"circle": 2},
    "tension-triangle": {"circle": 3},
    "bubble-matrix": {"line": 2, "circle": 1},
    "staircase": {"path": 3},
    "split-comparison": {"line": 1},
    "data-card-grid": {"path": 4},
    "layered-architecture": {"path": 4},
    "filter-funnel": {"path": 3},
    "overlapping-spheres": {"circle": 2},
    "iterative-cycle": {"circle": 4},
    "bridge-and-gap": {"path": 2},
}


def _check_diagram_structure(root, filename, content_plan_pages, errors):
    """Validate diagram SVGs have expected structural elements for their type."""
    if content_plan_pages is None:
        return

    page_num_match = re.match(r"p(\d+)", filename.lower(), re.IGNORECASE)
    if not page_num_match:
        return
    idx = int(page_num_match.group(1)) - 1
    if idx < 0 or idx >= len(content_plan_pages):
        return

    entry = content_plan_pages[idx]
    if not isinstance(entry, tuple) or len(entry) != 2:
        return
    page_type, relationship_type = entry
    if not relationship_type:
        return

    element_counts = {}
    for elem in root.iter():
        tag = _local_tag(elem).lower()
        element_counts[tag] = element_counts.get(tag, 0) + 1

    requirements = DIAGRAM_MIN_ELEMENTS.get(relationship_type, {})
    for tag_name, min_count in requirements.items():
        actual = element_counts.get(tag_name, 0)
        if actual < min_count:
            errors.append(
                f"Diagram type '{relationship_type}' expects >= {min_count} "
                f"<{tag_name}> elements, found {actual}"
            )


def validate_file(filepath, content_plan_pages=None):
    errors = []
    warnings = []
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        return [f"XML parse error: {e}"], []

    root = tree.getroot()

    _check_canvas(root, errors)
    _check_banned_elements(root, errors)
    _check_banned_attributes(root, errors)
    _check_fonts(root, errors)
    _check_tspan(root, errors)
    _check_rect_rounded(root, errors)
    _check_images(root, filepath, errors)
    _check_icons(root, errors)
    _check_nonempty(root, warnings)
    _check_graphical_elements(root, os.path.basename(filepath), content_plan_pages, errors)
    _check_diagram_structure(root, os.path.basename(filepath), content_plan_pages, errors)

    return errors, warnings


def parse_content_plan_pages(content_plan_path):
    """Returns list of (page_type, relationship_type_or_None) tuples."""
    try:
        with open(content_plan_path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"[WARN] Cannot read content-plan: {e}")
        return None

    pages = []
    for m in re.finditer(
        r"##\s*Page\s+\d+[^#\n]*\n(.*?)(?=\n##\s*Page\s+\d+|\Z)",
        text,
        re.DOTALL | re.IGNORECASE,
    ):
        block = m.group(1).lower()
        section_text = m.group(0)

        rel_match = re.search(
            r"Relationship\s+Type\s*[:：]\s*(\S[^\n]*)",
            section_text,
            re.IGNORECASE,
        )
        relationship_type = None
        if rel_match:
            raw = rel_match.group(1).strip()
            relationship_type = raw.lower().replace(" ", "-")

        if "content-diagram" in block and relationship_type:
            pages.append(("content-diagram", relationship_type))
        elif any(kw in block for kw in VISUAL_PAGE_TYPES):
            for kw in VISUAL_PAGE_TYPES:
                if kw in block and kw != "content-diagram":
                    pages.append((kw, None))
                    break
        else:
            pages.append((None, None))

    return pages if pages else None


def parse_outline_pages(outline_path):
    try:
        with open(outline_path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"[WARN] Cannot read outline: {e}")
        return None

    total_match = re.search(
        r"##\s*Total\s+Pages?\s*:\s*(\d+)", text, re.IGNORECASE
    )
    if total_match:
        return int(total_match.group(1))

    page_matches = re.findall(r"-\s*Page\s+\d+", text, re.IGNORECASE)
    if page_matches:
        return len(page_matches)

    return None


def check_completeness(svg_dir, svg_files, outline_path, errors):
    expected = parse_outline_pages(outline_path)
    if expected is not None and len(svg_files) != expected:
        errors.append(
            f"File count mismatch: expected {expected} pages "
            f"(from outline), found {len(svg_files)} SVG files"
        )


def main():
    ap = argparse.ArgumentParser(
        description="Validate SVG slide files for svg_to_pptx compatibility"
    )
    ap.add_argument("directory", help="Directory containing SVG slide files")
    ap.add_argument(
        "--outline",
        help="Path to outline.md for completeness checking",
        default=None,
    )
    ap.add_argument(
        "--content-plan",
        help="Path to content-plan.md for page-type-aware graphical element checking",
        default=None,
    )
    args = ap.parse_args()

    dirpath = args.directory
    if not os.path.isdir(dirpath):
        print(f"Error: Not a directory: {dirpath}")
        sys.exit(2)

    content_plan_pages = None
    if args.content_plan:
        content_plan_pages = parse_content_plan_pages(args.content_plan)

    svg_files = sorted(
        f for f in os.listdir(dirpath) if f.lower().endswith(".svg")
    )
    if not svg_files:
        print(f"No .svg files found in: {dirpath}")
        sys.exit(2)

    total_errors = 0
    total_warnings = 0

    for filename in svg_files:
        filepath = os.path.join(dirpath, filename)
        file_errors, file_warnings = validate_file(filepath, content_plan_pages)
        for err in file_errors:
            print(f"[ERROR] {filename}: {err}")
        for warn in file_warnings:
            print(f"[WARN] {filename}: {warn}")
        total_errors += len(file_errors)
        total_warnings += len(file_warnings)

    if args.outline:
        comp_errors = []
        check_completeness(dirpath, svg_files, args.outline, comp_errors)
        for err in comp_errors:
            print(f"[ERROR] {err}")
        total_errors += len(comp_errors)

    print(
        f"\n{total_errors} errors, {total_warnings} warnings "
        f"in {len(svg_files)} files"
    )

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
