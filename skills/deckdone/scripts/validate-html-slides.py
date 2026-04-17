#!/usr/bin/env python3
"""Validates HTML slide files for html2pptx compatibility."""

import argparse
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SAFE_FONTS = {
    "arial",
    "helvetica",
    "times new roman",
    "georgia",
    "courier new",
    "verdana",
    "tahoma",
    "trebuchet ms",
    "impact",
    "sans-serif",
    "serif",
    "monospace",
}

TEXT_TAGS = {
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "table",
    "th",
    "td",
}


class SlideValidator(HTMLParser):
    def __init__(self, html_dir):
        super().__init__()
        self.html_dir = html_dir
        self.errors = []
        self._style_lines = []
        self._tag_stack = []
        self._line_num = 0
        self._body_ok = False

    def handle_decl(self, decl):
        pass

    def handle_data(self, data):
        if not data.strip():
            return
        if self._tag_stack:
            current = self._tag_stack[-1]
            if current.lower() in ("div", "span"):
                line = self.getpos()[0]
                preview = data.strip()[:40]
                self.errors.append(
                    f'Bare text in <{current}> at line ~{line}: "{preview}"'
                )

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        self._tag_stack.append(tag_lower)
        attrs_dict = dict(attrs)
        line = self.getpos()[0]

        if tag_lower == "body":
            style = attrs_dict.get("style", "")
            if "width: 720pt" in style and "height: 405pt" in style:
                self._body_ok = True
            elif "width:720pt" in style and "height:405pt" in style:
                self._body_ok = True
            else:
                self.errors.append(
                    "Body missing required dimensions: width:720pt; height:405pt"
                )

        if tag_lower == "style":
            self._style_lines.append({"line": line, "ended": False})

        style_val = attrs_dict.get("style", "")
        if style_val:
            self._check_gradients(style_val, f"style attribute at line ~{line}")
            self._check_fonts(style_val, f"style attribute at line ~{line}")

        if tag_lower == "img":
            src = attrs_dict.get("src", "")
            if src:
                img_path = Path(self.html_dir) / src
                if not img_path.exists():
                    self.errors.append(f'Image not found: "{src}" at line ~{line}')

    def handle_endtag(self, tag):
        if tag.lower() == "style" and self._style_lines:
            self._style_lines[-1]["ended"] = True
        if self._tag_stack and self._tag_stack[-1] == tag.lower():
            self._tag_stack.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self._tag_stack and self._tag_stack[-1] == tag.lower():
            self._tag_stack.pop()

    def _check_gradients(self, css_text, location):
        if re.search(r"(linear|radial)-gradient\s*\(", css_text, re.IGNORECASE):
            m = re.search(
                r"((linear|radial)-gradient\s*\([^)]*\))", css_text, re.IGNORECASE
            )
            gradient_str = m.group(1) if m else "gradient"
            self.errors.append(f'CSS gradient found: "{gradient_str}" in {location}')

    def _check_fonts(self, css_text, location):
        m = re.search(r"font-family\s*:\s*([^;\"'}]+)", css_text, re.IGNORECASE)
        if m:
            fonts_str = m.group(1).strip().rstrip(";")
            for font in fonts_str.split(","):
                font_clean = font.strip().strip("'\"").lower()
                if font_clean and font_clean not in SAFE_FONTS:
                    self.errors.append(f'Unsafe font "{font.strip()}" in {location}')


def validate_file(filepath):
    html_dir = str(Path(filepath).parent)
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return [f"Error reading file: {e}"], False

    parser = SlideValidator(html_dir)
    try:
        parser.feed(content)
    except Exception as e:
        return [f"HTML parse error: {e}"], False

    style_blocks = re.findall(
        r"<style[^>]*>(.*?)</style>", content, re.DOTALL | re.IGNORECASE
    )

    if not parser._body_ok:
        body_in_style = False
        for block in style_blocks:
            body_rule = re.search(
                r"body\s*\{[^}]*width\s*:\s*720pt[^}]*height\s*:\s*405pt",
                block,
                re.IGNORECASE,
            )
            if body_rule:
                body_in_style = True
                break
            body_rule2 = re.search(
                r"body\s*\{[^}]*height\s*:\s*405pt[^}]*width\s*:\s*720pt",
                block,
                re.IGNORECASE,
            )
            if body_rule2:
                body_in_style = True
                break
        if body_in_style:
            parser._body_ok = True
            parser.errors = [
                e for e in parser.errors if "Body missing required dimensions" not in e
            ]

    for block in style_blocks:
        parser._check_gradients(block, "<style>")
        parser._check_fonts(block, "<style>")

    return parser.errors, parser._body_ok


def parse_outline_pages(outline_path):
    try:
        with open(outline_path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"Warning: Cannot read outline: {e}")
        return None

    total_match = re.search(r"##\s*Total\s+Pages?\s*:\s*(\d+)", text, re.IGNORECASE)
    if total_match:
        return int(total_match.group(1))

    page_matches = re.findall(r"-\s*Page\s+\d+", text, re.IGNORECASE)
    if page_matches:
        return len(page_matches)

    return None


def count_text_elements(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return 0

    count = 0
    for tag in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "li"):
        count += len(re.findall(rf"<{tag}[\s>]", content, re.IGNORECASE))
    return count


def check_completeness(dirpath, html_files, outline_path):
    errors = []

    expected = parse_outline_pages(outline_path)
    if expected is not None:
        actual = len(html_files)
        if actual != expected:
            errors.append(
                f"File count mismatch: expected {expected} pages (from outline), found {actual} HTML files"
            )

    for filename in html_files:
        filepath = os.path.join(dirpath, filename)
        try:
            size = os.path.getsize(filepath)
            if size < 100:
                errors.append(f"{filename}: file is nearly empty ({size} bytes)")
        except OSError:
            errors.append(f"{filename}: cannot read file")

    return errors


def check_emptiness(dirpath, html_files):
    warnings = []
    for filename in html_files:
        filepath = os.path.join(dirpath, filename)
        count = count_text_elements(filepath)
        if count < 2:
            warnings.append(
                f"{filename}: potentially empty (only {count} text element(s))"
            )
    return warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validate HTML slide files for html2pptx compatibility"
    )
    parser.add_argument(
        "directory",
        help="Directory containing HTML slide files",
    )
    parser.add_argument(
        "--outline",
        help="Path to outline.md for completeness checking",
        default=None,
    )
    args = parser.parse_args()

    dirpath = args.directory
    if not os.path.isdir(dirpath):
        print(f"Error: Not a directory: {dirpath}")
        sys.exit(2)

    html_files = sorted(f for f in os.listdir(dirpath) if f.lower().endswith(".html"))

    if not html_files:
        print(f"No .html files found in: {dirpath}")
        sys.exit(2)

    print("=== HTML Slide Validation ===")
    passed = 0
    failed = 0

    for filename in html_files:
        filepath = os.path.join(dirpath, filename)
        errors, _ = validate_file(filepath)
        if not errors:
            print(f"{filename} - PASS")
            passed += 1
        else:
            print(f"{filename} - FAIL")
            for err in errors:
                print(f"  - {err}")
            failed += 1

    if args.outline:
        print("\n=== Completeness Check ===")
        comp_errors = check_completeness(dirpath, html_files, args.outline)
        if comp_errors:
            for err in comp_errors:
                print(f"  - {err}")
            failed += len(comp_errors)
        else:
            print("  All files present and non-empty.")

    print("\n=== Emptiness Check ===")
    empty_warnings = check_emptiness(dirpath, html_files)
    if empty_warnings:
        for w in empty_warnings:
            print(f"  WARN: {w}")
    else:
        print("  No empty slides detected.")

    print("\n=== Summary ===")
    print(f"Total files: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
