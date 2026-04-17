#!/usr/bin/env python3
"""Validates that HTML slides use colors from the defined palette."""

import argparse
import os
import re
import sys


ALLOWED_GRAYSCALE = {
    "000000",
    "FFFFFF",
    "333333",
    "4A4A4A",
    "666666",
    "999999",
    "AAAAAA",
    "B0B0B0",
    "CCCCCC",
    "D0D0D0",
    "E0E0E0",
    "F0F0F0",
    "F8F8F8",
}

CSS_COLOR_PROPS = {
    "color",
    "background",
    "background-color",
    "border",
    "border-color",
    "border-top",
    "border-bottom",
    "border-left",
    "border-right",
    "outline",
    "outline-color",
}


def parse_palette(style_guide_path):
    try:
        with open(style_guide_path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"Error reading style guide: {e}")
        return None

    palette_heading = None
    for line in text.splitlines():
        if line.strip().startswith("## Palette"):
            palette_heading = line
            break

    if not palette_heading:
        return None

    hex_colors = re.findall(r"#[0-9A-Fa-f]{6}", palette_heading)
    if len(hex_colors) < 3:
        return None

    return [c.upper() for c in hex_colors]


def normalize_hex(color_str):
    color_str = color_str.strip().lstrip("#").upper()
    if len(color_str) == 3:
        color_str = "".join(c * 2 for c in color_str)
    if len(color_str) != 6:
        return None
    if not all(c in "0123456789ABCDEF" for c in color_str):
        return None
    return color_str


def extract_colors_from_css(css_text):
    colors = set()
    for prop_match in re.finditer(r"([\w-]+)\s*:\s*([^;}{]+)", css_text):
        prop_name = prop_match.group(1).strip().lower()
        if prop_name not in CSS_COLOR_PROPS:
            continue
        value = prop_match.group(2)
        for hex_match in re.finditer(r"#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})\b", value):
            normalized = normalize_hex(hex_match.group(0))
            if normalized:
                colors.add(normalized)
    return colors


def extract_colors_from_file(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return set()

    all_colors = set()

    style_blocks = re.findall(
        r"<style[^>]*>(.*?)</style>", content, re.DOTALL | re.IGNORECASE
    )
    for block in style_blocks:
        all_colors.update(extract_colors_from_css(block))

    inline_styles = re.findall(
        r'style\s*=\s*["\']([^"\']*)["\']', content, re.IGNORECASE
    )
    for style_val in inline_styles:
        all_colors.update(extract_colors_from_css(style_val))

    return all_colors


def find_closest(color, palette):
    def hex_distance(c1, c2):
        r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
        r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
        return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5

    closest = min(palette, key=lambda p: hex_distance(color, p))
    return closest


def main():
    parser = argparse.ArgumentParser(
        description="Validate HTML slides use colors from the style guide palette"
    )
    parser.add_argument("style_guide", help="Path to style-guide.md")
    parser.add_argument("html_directory", help="Directory containing HTML slide files")
    args = parser.parse_args()

    if not os.path.isfile(args.style_guide):
        print(f"Error: Style guide not found: {args.style_guide}")
        sys.exit(2)

    if not os.path.isdir(args.html_directory):
        print(f"Error: Not a directory: {args.html_directory}")
        sys.exit(2)

    palette = parse_palette(args.style_guide)
    if palette is None:
        print(f"Error: Cannot parse palette from {args.style_guide}")
        print("Expected: ## Palette: ... with at least 3 hex color values")
        sys.exit(2)

    palette_set = set(palette)

    html_files = sorted(
        f for f in os.listdir(args.html_directory) if f.lower().endswith(".html")
    )
    if not html_files:
        print(f"No .html files found in: {args.html_directory}")
        sys.exit(2)

    print("=== Color Consistency Check ===")
    print(f"Palette: {', '.join(palette)}")
    print()

    passed = 0
    warned = 0

    for filename in html_files:
        filepath = os.path.join(args.html_directory, filename)
        file_colors = extract_colors_from_file(filepath)
        palette_only = [c for c in sorted(file_colors) if c not in ALLOWED_GRAYSCALE]

        if not palette_only:
            print(f"{filename} - PASS")
            passed += 1
        else:
            non_palette = [c for c in palette_only if c not in palette_set]
            if not non_palette:
                print(f"{filename} - PASS")
                passed += 1
            else:
                print(f"{filename} - WARN")
                for color in non_palette:
                    closest = find_closest(color, list(palette_set))
                    print(
                        f'  - Unexpected color "#{color}" (closest palette: #{closest})'
                    )
                warned += 1

    print(f"\n=== Summary ===")
    print(f"Checked: {passed + warned}")
    print(f"Pass: {passed}")
    print(f"Warn: {warned}")

    sys.exit(0)


if __name__ == "__main__":
    main()
