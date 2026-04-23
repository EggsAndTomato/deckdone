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


def validate_file(filepath):
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

    return errors, warnings


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
    args = ap.parse_args()

    dirpath = args.directory
    if not os.path.isdir(dirpath):
        print(f"Error: Not a directory: {dirpath}")
        sys.exit(2)

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
        file_errors, file_warnings = validate_file(filepath)
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
