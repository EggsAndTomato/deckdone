# DeckDone Optimization Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add environment detection, image-PDF extraction, and quality check automation to the DeckDone skill.

**Architecture:** Three new Python scripts (stdlib + minimal deps) added to `skills/deckdone/scripts/`, one existing script extended with argparse, and SKILL.md updated with new sections. Each script is self-contained with graceful degradation.

**Tech Stack:** Python 3.8+ (stdlib), pypdf, pypdfium2 (pulls in Pillow), argparse

**Spec:** `docs/superpowers/specs/2026-04-17-deckdone-optimization-design.md`

---

## Chunk 1: Environment Detection Script

### Task 1: Create `check-env.py` — Core Detection Logic

**Files:**
- Create: `skills/deckdone/scripts/check-env.py`

- [ ] **Step 1: Write the complete `check-env.py` script**

```python
#!/usr/bin/env python3
"""Checks DeckDone dependencies and optionally installs missing ones."""

import argparse
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys


CHECKS = [
    {
        "id": "python",
        "category": "Python",
        "name": "Python 3.8+",
        "check": "check_python",
        "install_cmd": None,
        "install_hint": "Install Python 3.8+ from https://python.org",
    },
    {
        "id": "pypdf",
        "category": "Python",
        "name": "pypdf",
        "check": "check_pypdf",
        "install_cmd": "pip install pypdf",
    },
    {
        "id": "pypdfium2",
        "category": "Python",
        "name": "pypdfium2",
        "check": "check_pypdfium2",
        "install_cmd": "pip install pypdfium2",
    },
    {
        "id": "pdfplumber",
        "category": "Python",
        "name": "pdfplumber",
        "check": "check_pdfplumber",
        "install_cmd": "pip install pdfplumber",
        "optional": True,
    },
    {
        "id": "node",
        "category": "Node.js",
        "name": "Node.js 18+",
        "check": "check_node",
        "install_cmd": None,
        "install_hint": "Install Node.js 18+ from https://nodejs.org",
    },
    {
        "id": "pptxgenjs",
        "category": "Node.js",
        "name": "pptxgenjs (global)",
        "check": "check_pptxgenjs",
        "install_cmd": "npm install -g pptxgenjs",
    },
    {
        "id": "playwright",
        "category": "Node.js",
        "name": "playwright (global)",
        "check": "check_playwright",
        "install_cmd": "npm install -g playwright",
    },
    {
        "id": "sharp",
        "category": "Node.js",
        "name": "sharp (global)",
        "check": "check_sharp",
        "install_cmd": "npm install -g sharp",
    },
    {
        "id": "pw_browsers",
        "category": "Node.js",
        "name": "Playwright browsers",
        "check": "check_pw_browsers",
        "install_cmd": "npx playwright install",
    },
    {
        "id": "libreoffice",
        "category": "System",
        "name": "LibreOffice",
        "check": "check_libreoffice",
        "install_cmd": None,
        "install_hint": "Install LibreOffice: winget install TheDocumentFoundation.LibreOffice (Win) / brew install --cask libreoffice (macOS) / apt install libreoffice (Linux)",
        "optional": True,
    },
]


def check_python():
    return sys.version_info >= (3, 8)


def check_pypdf():
    return importlib.util.find_spec("pypdf") is not None


def check_pypdfium2():
    return importlib.util.find_spec("pypdfium2") is not None


def check_pdfplumber():
    return importlib.util.find_spec("pdfplumber") is not None


def check_node():
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return False
        version_str = result.stdout.strip().lstrip("v")
        major = int(version_str.split(".")[0])
        return major >= 18
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        return False


def _check_npm_global(package):
    try:
        result = subprocess.run(
            ["npm", "list", "-g", package],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_pptxgenjs():
    return _check_npm_global("pptxgenjs")


def check_playwright():
    return _check_npm_global("playwright")


def check_sharp():
    return _check_npm_global("sharp")


def check_pw_browsers():
    if platform.system() == "Windows":
        base = os.environ.get("LOCALAPPDATA", "")
        pw_dir = os.path.join(base, "ms-playwright") if base else ""
    else:
        pw_dir = os.path.expanduser("~/.cache/ms-playwright")
    if not pw_dir or not os.path.isdir(pw_dir):
        return False
    entries = os.listdir(pw_dir)
    return len(entries) > 0


def check_libreoffice():
    candidates = ["soffice", "libreoffice"]
    if platform.system() == "Windows":
        candidates.append(
            os.path.join(
                os.environ.get("ProgramFiles", r"C:\Program Files"),
                "LibreOffice",
                "program",
                "soffice.exe",
            )
        )
    for cmd in candidates:
        if shutil.which(cmd):
            return True
        if os.path.isfile(cmd):
            return True
    return False


CHECK_FUNCS = {
    "python": check_python,
    "pypdf": check_pypdf,
    "pypdfium2": check_pypdfium2,
    "pdfplumber": check_pdfplumber,
    "node": check_node,
    "pptxgenjs": check_pptxgenjs,
    "playwright": check_playwright,
    "sharp": check_sharp,
    "pw_browsers": check_pw_browsers,
    "libreoffice": check_libreoffice,
}


def run_checks():
    results = []
    for check in CHECKS:
        func = CHECK_FUNCS[check["id"]]
        passed = func()
        results.append({**check, "passed": passed})
    return results


def print_report(results):
    current_cat = None
    for r in results:
        if r["category"] != current_cat:
            current_cat = r["category"]
            print(f"\n{current_cat}:")
        status = "PASS" if r["passed"] else ("SKIP" if r.get("optional") else "FAIL")
        suffix = " (optional)" if r.get("optional") else ""
        print(f"  [{status}] {r['name']}{suffix}")

    required_fails = [r for r in results if not r["passed"] and not r.get("optional")]
    optional_fails = [r for r in results if not r["passed"] and r.get("optional")]
    print()

    if not required_fails and not optional_fails:
        print("All dependencies satisfied.")
    elif not required_fails:
        print(f"Core dependencies OK. {len(optional_fails)} optional item(s) missing.")
    else:
        print(f"FAIL: {len(required_fails)} required item(s) missing.")
        for r in required_fails:
            print(f"  - {r['name']}")
            if r.get("install_cmd"):
                print(f"    Install: {r['install_cmd']}")
            elif r.get("install_hint"):
                print(f"    {r['install_hint']}")


def print_json_report(results):
    output = []
    for r in results:
        output.append({
            "id": r["id"],
            "name": r["name"],
            "category": r["category"],
            "passed": r["passed"],
            "optional": r.get("optional", False),
            "install_cmd": r.get("install_cmd"),
        })
    print(json.dumps(output, indent=2))


def install_missing(results, auto_yes=False):
    missing = [r for r in results if not r["passed"] and r.get("install_cmd")]
    if not missing:
        print("Nothing to install.")
        return

    print(f"\n{len(missing)} item(s) to install:\n")
    for r in missing:
        print(f"  {r['name']}: {r['install_cmd']}")
    print()

    for r in missing:
        if auto_yes:
            print(f"Installing {r['name']}...")
            _run_install(r["install_cmd"])
        else:
            answer = input(f"Install {r['name']}? ({r['install_cmd']}) [y/N]: ").strip().lower()
            if answer == "y":
                _run_install(r["install_cmd"])
            else:
                print(f"  Skipped {r['name']}.")


def _run_install(cmd):
    try:
        result = subprocess.run(cmd, shell=True, timeout=120)
        if result.returncode == 0:
            print(f"  OK")
        else:
            print(f"  FAILED (exit code {result.returncode})")
    except subprocess.TimeoutExpired:
        print(f"  FAILED (timeout)")


def main():
    parser = argparse.ArgumentParser(
        description="Check DeckDone dependencies"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install missing dependencies (prompts for confirmation)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Auto-confirm all installs (use with --install for non-interactive mode)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    args = parser.parse_args()

    if args.json and args.install:
        print("Error: --json and --install are mutually exclusive", file=sys.stderr)
        sys.exit(2)

    results = run_checks()

    if args.json:
        print_json_report(results)
        required_fails = [r for r in results if not r["passed"] and not r.get("optional")]
        sys.exit(1 if required_fails else 0)

    print_report(results)

    if args.install:
        install_missing(results, auto_yes=args.yes)
        print("\n--- Re-checking ---")
        results = run_checks()
        print_report(results)

    required_fails = [r for r in results if not r["passed"] and not r.get("optional")]
    sys.exit(1 if required_fails else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test `check-env.py` in report mode**

Run: `python skills/deckdone/scripts/check-env.py`
Expected: Prints a table of all dependencies with PASS/FAIL/SKIP status. Exit code 0 if all required items pass, 1 otherwise.

- [ ] **Step 3: Test `check-env.py` in JSON mode**

Run: `python skills/deckdone/scripts/check-env.py --json`
Expected: Outputs valid JSON array with id/name/category/passed/optional/install_cmd per item.

- [ ] **Step 4: Test `check-env.py` help**

Run: `python skills/deckdone/scripts/check-env.py --help`
Expected: Shows argparse help with --install, --yes, --json flags documented.

- [ ] **Step 5: Commit**

```bash
git add skills/deckdone/scripts/check-env.py
git commit -m "feat(scripts): add check-env.py for dependency detection"
```

---

## Chunk 2: Image-PDF Extraction Script

### Task 2: Create `extract-pdf.py`

**Files:**
- Create: `skills/deckdone/scripts/extract-pdf.py`

- [ ] **Step 1: Write the complete `extract-pdf.py` script**

```python
#!/usr/bin/env python3
"""Extracts text from PDFs. Handles image-type PDFs by rendering pages as PNG."""

import argparse
import os
import re
import sys


def check_deps():
    missing = []
    try:
        import pypdf
    except ImportError:
        missing.append("pypdf")
    try:
        import pypdfium2 as pdfium
    except ImportError:
        missing.append("pypdfium2")
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(2)


def load_pdf(filepath):
    try:
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        return reader
    except Exception as e:
        encrypted = "encrypt" in str(e).lower() or "password" in str(e).lower()
        if encrypted:
            print(f"Error: PDF appears to be encrypted/protected: {filepath}")
            print("Please provide a decrypted copy of this PDF.")
            sys.exit(1)
        print(f"Error reading PDF: {e}")
        sys.exit(1)


def get_page_text(reader, page_num):
    try:
        page = reader.pages[page_num]
        text = page.extract_text()
        return text.strip() if text else ""
    except Exception:
        return ""


def classify_pages(reader):
    total = len(reader.pages)
    page_types = {}

    if total <= 50:
        for i in range(total):
            text = get_page_text(reader, i)
            page_types[i] = "text" if len(text) > 20 else "image"
    else:
        sample_indices = [0, total // 4, total // 2, 3 * total // 4, total - 1]
        sample_indices = sorted(set(i for i in sample_indices if i < total))
        samples = {i: get_page_text(reader, i) for i in sample_indices}
        all_text = all(len(samples[i]) > 20 for i in sample_indices)
        all_image = all(len(samples[i]) <= 20 for i in sample_indices)

        if all_text:
            for i in range(total):
                page_types[i] = "text"
        elif all_image:
            for i in range(total):
                page_types[i] = "image"
        else:
            for i in range(total):
                text = get_page_text(reader, i)
                page_types[i] = "text" if len(text) > 20 else "image"

    return page_types


def extract_text_pages(reader, page_types, output_dir):
    text_pages = [i for i, t in page_types.items() if t == "text"]
    if not text_pages:
        return []

    written = []
    for page_num in text_pages:
        text = get_page_text(reader, page_num)
        filename = f"{page_num + 1:02d}-page-{page_num + 1:03d}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Page {page_num + 1}\n\n{text}\n")
        written.append(filename)
    return written


def render_image_pages(filepath, page_types, output_dir):
    import pypdfium2 as pdfium

    image_pages = [i for i, t in page_types.items() if t == "image"]
    if not image_pages:
        return []

    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    pdf = pdfium.PdfDocument(filepath)
    rendered = []

    for page_num in image_pages:
        page = pdf[page_num]
        bitmap = page.render(scale=200 / 72)
        pil_img = bitmap.to_pil()
        img_filename = f"page-{page_num + 1:03d}.png"
        img_path = os.path.join(images_dir, img_filename)
        pil_img.save(img_path)
        rendered.append((page_num + 1, img_filename))

    pdf.close()
    return rendered


def write_manifest(source_name, total_pages, rendered, output_dir):
    manifest_path = os.path.join(output_dir, "image-pdf-manifest.md")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(f"# Image PDF Extraction Manifest\n\n")
        f.write(f"## Source: {source_name}\n")
        f.write(f"## Total Pages: {total_pages}\n")
        f.write(f"## Status: Images rendered, awaiting AI visual extraction\n\n")
        f.write(f"## Instructions for AI Agent\n")
        f.write(f"For each page image below, use visual recognition to extract:\n")
        f.write(f"- All text content (headings, body text, labels, data)\n")
        f.write(f"- Table structures (rows, columns, values)\n")
        f.write(f"- Chart/graph descriptions (type, data points, trends)\n")
        f.write(f"- Image descriptions (diagrams, photos)\n\n")
        f.write(f"## Pages\n")
        for page_num, img_filename in rendered:
            f.write(f"- Page {page_num}: images/{img_filename}\n")
    return manifest_path


def write_index(source_name, page_types, text_files, manifest_path, output_dir):
    index_path = os.path.join(output_dir, "00-index.md")
    text_count = sum(1 for t in page_types.values() if t == "text")
    image_count = sum(1 for t in page_types.values() if t == "image")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# Source Index\n\n")
        f.write(f"- Source: {source_name}\n")
        f.write(f"- Total pages: {len(page_types)}\n")
        f.write(f"- Text pages: {text_count}\n")
        f.write(f"- Image pages: {image_count}\n")
        if text_files:
            f.write(f"- Text files: {', '.join(text_files)}\n")
        if manifest_path:
            f.write(f"- Image manifest: image-pdf-manifest.md\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDFs; render image-type pages as PNG for AI visual extraction"
    )
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument(
        "--output", "-o",
        default="materials",
        help="Output directory (default: materials/)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI for image rendering (default: 200)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.pdf_file):
        print(f"Error: File not found: {args.pdf_file}")
        sys.exit(2)

    check_deps()

    source_name = os.path.basename(args.pdf_file)
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    reader = load_pdf(args.pdf_file)
    page_types = classify_pages(reader)
    total = len(reader.pages)

    text_count = sum(1 for t in page_types.values() if t == "text")
    image_count = sum(1 for t in page_types.values() if t == "image")

    print(f"PDF: {source_name}")
    print(f"Total pages: {total}")
    print(f"Text pages: {text_count}")
    print(f"Image pages: {image_count}")

    text_files = []
    manifest_path = None

    if text_count > 0:
        print(f"\nExtracting text from {text_count} page(s)...")
        text_files = extract_text_pages(reader, page_types, output_dir)
        print(f"  Wrote {len(text_files)} text file(s)")

    if image_count > 0:
        print(f"\nRendering {image_count} image page(s) as PNG...")
        rendered = render_image_pages(args.pdf_file, page_types, output_dir)
        print(f"  Rendered {len(rendered)} image(s)")
        manifest_path = write_manifest(source_name, total, rendered, output_dir)
        print(f"  Manifest: {manifest_path}")

    write_index(source_name, page_types, text_files, manifest_path, output_dir)
    print(f"\nDone. Output in: {output_dir}/")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test `extract-pdf.py` with no arguments**

Run: `python skills/deckdone/scripts/extract-pdf.py`
Expected: Prints usage help from argparse.

- [ ] **Step 3: Test `extract-pdf.py` with a non-existent file**

Run: `python skills/deckdone/scripts/extract-pdf.py nonexistent.pdf`
Expected: Prints "Error: File not found: nonexistent.pdf", exit code 2.

- [ ] **Step 4: Test `extract-pdf.py` with a real text-type PDF**

Run: `python skills/deckdone/scripts/extract-pdf.py <any-text-pdf> --output /tmp/test-materials`
Expected: Classifies pages as text, writes per-page .md files, no image manifest.

- [ ] **Step 5: Test `extract-pdf.py` with a real image-type PDF (if available)**

Run: `python skills/deckdone/scripts/extract-pdf.py <any-image-pdf> --output /tmp/test-materials2`
Expected: Classifies pages as image, renders PNGs, writes manifest with AI instructions.

- [ ] **Step 6: Test `extract-pdf.py` error handling for encrypted PDF**

Create or find a password-protected PDF, then run:
`python skills/deckdone/scripts/extract-pdf.py <encrypted.pdf> --output /tmp/test-materials3`
Expected: Prints "Error: PDF appears to be encrypted/protected" with guidance message, exit code 1.

- [ ] **Step 7: Commit**

```bash
git add skills/deckdone/scripts/extract-pdf.py
git commit -m "feat(scripts): add extract-pdf.py for text and image-type PDF extraction"
```

---

## Chunk 3: Quality Check Automation

### Task 3: Extend `validate-html-slides.py` with argparse + completeness checks

**Files:**
- Modify: `skills/deckdone/scripts/validate-html-slides.py`

- [ ] **Step 1: Add argparse to `validate-html-slides.py`**

Replace the `main()` function and add completeness/emptiness checks. The existing `SlideValidator` class and `validate_file()` function remain unchanged.

New `main()`:

```python
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

    sections = re.findall(r"###\s+Section\s+\d+", text, re.IGNORECASE)
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
```

Also add `import argparse` to the imports at the top of the file (replace `import sys` if not already present — it is already present, so just add `import argparse`).

- [ ] **Step 2: Test backward compatibility — run without flags**

Run: `python skills/deckdone/scripts/validate-html-slides.py <some-dir-with-html>`
Expected: Same behavior as before — validates html2pptx compatibility, prints PASS/FAIL per file. No completeness check.

- [ ] **Step 3: Test with `--outline` flag**

Run: `python skills/deckdone/scripts/validate-html-slides.py <some-dir> --outline outline.md`
Expected: Runs standard validation PLUS completeness check (file count vs outline page count) and emptiness check.

- [ ] **Step 4: Test `--help`**

Run: `python skills/deckdone/scripts/validate-html-slides.py --help`
Expected: Shows argparse help with directory positional arg and --outline flag.

- [ ] **Step 5: Commit**

```bash
git add skills/deckdone/scripts/validate-html-slides.py
git commit -m "feat(scripts): add completeness and emptiness checks to validate-html-slides.py"
```

### Task 4: Create `validate-colors.py`

**Files:**
- Create: `skills/deckdone/scripts/validate-colors.py`

- [ ] **Step 1: Write the complete `validate-colors.py` script**

```python
#!/usr/bin/env python3
"""Validates that HTML slides use colors from the defined palette."""

import argparse
import os
import re
import sys


ALLOWED_GRAYSCALE = {
    "000000", "FFFFFF",
    "333333", "4A4A4A", "666666",
    "999999", "AAAAAA", "B0B0B0", "CCCCCC",
    "D0D0D0", "E0E0E0", "F0F0F0", "F8F8F8",
}

CSS_COLOR_PROPS = {
    "color", "background", "background-color",
    "border", "border-color",
    "border-top", "border-bottom", "border-left", "border-right",
    "outline", "outline-color",
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

    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL | re.IGNORECASE)
    for block in style_blocks:
        all_colors.update(extract_colors_from_css(block))

    inline_styles = re.findall(r'style\s*=\s*["\']([^"\']*)["\']', content, re.IGNORECASE)
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
                for color in palette_only:
                    if color in palette_set:
                        continue
                    else:
                        closest = find_closest(color, list(palette_set))
                        print(f'  - Unexpected color "#{color}" (closest palette: #{closest})')
                warned += 1

    print(f"\n=== Summary ===")
    print(f"Checked: {passed + warned}")
    print(f"Pass: {passed}")
    print(f"Warn: {warned}")

    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test `validate-colors.py` with no arguments**

Run: `python skills/deckdone/scripts/validate-colors.py`
Expected: Prints argparse usage help.

- [ ] **Step 3: Test with a sample style-guide.md and HTML directory**

Create a test style-guide.md with a `## Palette:` line containing hex values, and run against a directory with HTML files. Verify it reports expected PASS/WARN results.

- [ ] **Step 4: Commit**

```bash
git add skills/deckdone/scripts/validate-colors.py
git commit -m "feat(scripts): add validate-colors.py for palette consistency checking"
```

---

## Chunk 4: SKILL.md and Reference Updates

### Task 5: Move State File Templates to `references/state-templates.md`

**Files:**
- Create: `skills/deckdone/references/state-templates.md`
- Modify: `skills/deckdone/SKILL.md:502-575`

- [ ] **Step 1: Create `references/state-templates.md`**

Extract the entire "State File Templates" section from SKILL.md (lines 502-575) into a new file. The new file contains:
- `deckdone-state.md` template
- `deckdone-trace.md` template
- `harness-improvements.md` template

These are copied verbatim from the current SKILL.md.

- [ ] **Step 2: Replace the State File Templates section in SKILL.md**

Replace lines 502-575 in SKILL.md with:

```markdown
## State File Templates

See `references/state-templates.md` for complete templates for `deckdone-state.md`, `deckdone-trace.md`, and `harness-improvements.md`.
```

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/references/state-templates.md skills/deckdone/SKILL.md
git commit -m "refactor: move state file templates to references/state-templates.md"
```

### Task 6: Update SKILL.md with Pre-Flight, Dependencies, and Step changes

**Files:**
- Modify: `skills/deckdone/SKILL.md`

- [ ] **Step 1: Add Pre-Flight section**

Insert after the "Cross-Conversation Continuity" section (after line ~115), before "Phase 1":

```markdown
## Pre-Flight: Environment Check

Before starting Phase 1, run:

    python scripts/check-env.py

If any items fail, resolve them before proceeding. For guided installation:

    python scripts/check-env.py --install          # interactive y/n per item
    python scripts/check-env.py --install --yes    # auto-confirm all (for AI agent use)
```

- [ ] **Step 2: Add Python (Optional) subsection to Dependencies**

After the "### Optional (graceful degradation)" table, add:

```markdown
### Python (Optional)

| Dependency | Type | Degradation if missing |
|-----------|------|----------------------|
| pypdf | pip | Image-type PDFs cannot be processed by extract-pdf.py |
| pypdfium2 | pip | Image-type PDFs cannot be rendered to PNG |
| pdfplumber | pip | Complex PDF layouts may extract text with lower fidelity |

If these packages are unavailable, image-type PDFs fall back to asking the user to paste text content.
```

- [ ] **Step 3: Update Step 2 (Material Collection)**

In the `.pdf` line under Step 2, replace:
```
   - `.pdf` → use pdf skill; if unavailable, ask user to paste text content
```
with:
```
   - `.pdf` → Run `python scripts/extract-pdf.py <file> --output materials/`
     - If text-layer detected: text extracted automatically
     - If image-type: pages rendered as PNG, follow manifest instructions for visual extraction
   - If `extract-pdf.py` is unavailable, fall back to pdf skill or ask user to paste text content
```

- [ ] **Step 4: Update Step 10 validation**

In Step 10, replace the existing validation line:
```
**Validation:** Run `python scripts/validate-html-slides.py wireframes/`.
```
with:
```
**Validation:**
- Run `python scripts/validate-html-slides.py wireframes/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md wireframes/`
```

- [ ] **Step 5: Update Step 11 validation**

In Step 11, after the existing validation content, add:
```
**Validation:**
- Run `python scripts/validate-html-slides.py wireframes/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md wireframes/`
```

- [ ] **Step 6: Verify SKILL.md line count**

Run: `wc -l skills/deckdone/SKILL.md`
Expected: Under 600 lines.

- [ ] **Step 7: Commit**

```bash
git add skills/deckdone/SKILL.md
git commit -m "feat(skill): add pre-flight check, extract-pdf integration, and color validation to SKILL.md"
```

---

## Chunk 5: Final Verification

### Task 7: Run all scripts and verify integration

- [ ] **Step 1: Run check-env.py**

Run: `python skills/deckdone/scripts/check-env.py`
Expected: Reports all dependencies with no errors.

- [ ] **Step 2: Run validate-content-plan.py (unchanged, verify still works)**

Run: `python skills/deckdone/scripts/validate-content-plan.py <any-content-plan.md>` (or verify it shows usage help)
Expected: Still works as before.

- [ ] **Step 3: Run validate-html-slides.py in both modes**

Run: `python skills/deckdone/scripts/validate-html-slides.py --help`
Expected: Shows --outline flag.

- [ ] **Step 4: Run validate-colors.py**

Run: `python skills/deckdone/scripts/validate-colors.py --help`
Expected: Shows positional args for style_guide and html_directory.

- [ ] **Step 5: Final commit (if any fixups needed)**

```bash
git add -A
git commit -m "chore: final verification fixups"
```
