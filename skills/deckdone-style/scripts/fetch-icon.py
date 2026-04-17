#!/usr/bin/env python3
"""Fetch a Tabler icon SVG. Checks local icons/ first, then jsdelivr CDN."""

import argparse
import os
import subprocess
import sys
import urllib.request
import urllib.error

TABLER_CDN = (
    "https://cdn.jsdelivr.net/npm/@tabler/icons@3.41.1/icons/outline/{name}.svg"
)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_ICONS_DIR = os.path.join(SCRIPT_DIR, "..", "references", "icons")


def find_local_icon(name):
    path = os.path.join(LOCAL_ICONS_DIR, f"{name}.svg")
    return path if os.path.isfile(path) else None


def download_icon(name):
    url = TABLER_CDN.format(name=name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "deckdone-style/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                return None
            return resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return None


def sharp_convert(input_path, output_path, size):
    try:
        result = subprocess.run(
            [
                "node",
                "-e",
                f'require("sharp")("{input_path}").resize({size},{size}).png().toFile("{output_path}").then(()=>process.exit(0)).catch(()=>process.exit(1))',
            ],
            capture_output=True,
            timeout=30,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main():
    parser = argparse.ArgumentParser(description="Fetch a Tabler icon SVG/PNG")
    parser.add_argument("name", help="Icon name (kebab-case, e.g. chart-bar)")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument(
        "--size", type=int, default=48, help="PNG size in pixels (default: 48)"
    )
    parser.add_argument("--png", action="store_true", help="Force PNG output via Sharp")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    svg_data = None
    source = None

    local_path = find_local_icon(args.name)
    if local_path:
        with open(local_path, "rb") as f:
            svg_data = f.read()
        source = "local"
    else:
        svg_data = download_icon(args.name)
        if svg_data:
            source = "cdn"
        else:
            print(
                f"Error: Icon '{args.name}' not found locally or on CDN",
                file=sys.stderr,
            )
            sys.exit(2)

    svg_output = os.path.join(args.output_dir, f"{args.name}.svg")
    with open(svg_output, "wb") as f:
        f.write(svg_data)
    print(f"OK: {args.name}.svg ({source}, {len(svg_data)} bytes)")

    if args.png:
        png_output = os.path.join(args.output_dir, f"{args.name}.png")
        if sharp_convert(svg_output, png_output, args.size):
            print(f"OK: {args.name}.png ({args.size}x{args.size})")
        else:
            print(f"Warning: Sharp conversion failed, SVG kept", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
