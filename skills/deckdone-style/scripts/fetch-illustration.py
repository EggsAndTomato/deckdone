#!/usr/bin/env python3
"""Fetch an unDraw illustration SVG with color customization."""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from collections import Counter

UNDRAW_API = "https://undraw.co/api/illustration/{slug}"
UNDRAW_DEFAULT_COLOR = "#6C63FF"


def fetch_illustration_url(slug):
    url = UNDRAW_API.format(slug=slug)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "deckdone-style/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                return None
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("url")
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        OSError,
        json.JSONDecodeError,
    ):
        return None


def download_svg(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "deckdone-style/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                return None
            return resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return None


def replace_color(svg_text, new_color):
    new_color = new_color.strip().lstrip("#")
    new_color = f"#{new_color}"

    patterns = [
        re.compile(re.escape(UNDRAW_DEFAULT_COLOR), re.IGNORECASE),
        re.compile(re.escape(UNDRAW_DEFAULT_COLOR.lower()), re.IGNORECASE),
    ]

    for pat in patterns:
        if pat.search(svg_text):
            return pat.sub(new_color, svg_text), False

    hex_colors = re.findall(r"#[0-9a-fA-F]{6}", svg_text)
    if hex_colors:
        most_common = Counter(hex_colors).most_common(1)[0][0]
        return svg_text.replace(most_common, new_color), True

    return svg_text, True


def sharp_convert(input_path, output_path):
    try:
        result = subprocess.run(
            [
                "node",
                "-e",
                f'require("sharp")("{input_path}").resize(800,600).fit("inside").png().toFile("{output_path}").then(()=>process.exit(0)).catch(()=>process.exit(1))',
            ],
            capture_output=True,
            timeout=30,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Fetch unDraw illustration with custom color"
    )
    parser.add_argument("slug", help="unDraw illustration slug (e.g. business-plan)")
    parser.add_argument("accent_color", help="Accent color hex (e.g. #E8A838)")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument(
        "--png", action="store_true", help="Also convert to PNG via Sharp"
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    svg_url = fetch_illustration_url(args.slug)
    if not svg_url:
        print(
            f"Error: Could not fetch illustration '{args.slug}' from unDraw",
            file=sys.stderr,
        )
        sys.exit(1)

    svg_text = download_svg(svg_url)
    if not svg_text:
        print(f"Error: Could not download SVG from {svg_url}", file=sys.stderr)
        sys.exit(1)

    svg_text, used_heuristic = replace_color(svg_text, args.accent_color)

    svg_output = os.path.join(args.output_dir, f"{args.slug}.svg")
    with open(svg_output, "w", encoding="utf-8") as f:
        f.write(svg_text)

    if used_heuristic:
        print(
            f"Warning: Used heuristic color replacement for {args.slug}",
            file=sys.stderr,
        )
        print(
            f"OK: {args.slug}.svg ({len(svg_text)} bytes, heuristic color)",
            file=sys.stderr,
        )
        exit_code = 2
    else:
        print(
            f"OK: {args.slug}.svg ({len(svg_text)} bytes, color: {args.accent_color})"
        )
        exit_code = 0

    if args.png:
        png_output = os.path.join(args.output_dir, f"{args.slug}.png")
        if sharp_convert(svg_output, png_output):
            print(f"OK: {args.slug}.png")
        else:
            print(f"Warning: Sharp conversion failed, SVG kept", file=sys.stderr)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
