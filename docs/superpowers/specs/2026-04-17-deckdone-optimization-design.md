# DeckDone Skill Optimization Design

**Date:** 2026-04-17
**Status:** Approved
**Scope:** Environment detection, image-PDF extraction, quality check automation

---

## Background

An external agent used DeckDone to create a 15-page medical AI presentation and reported that ~30% of time was spent on environment issues. The PDF materials were image-type (no text layer), requiring trial-and-error extraction. Quality checks referenced in `quality-checklist.md` were never mechanically enforced.

This design addresses three areas identified from that report, in priority order.

---

## Optimization 1: Environment Detection Script

### What

Add `scripts/check-env.py` — a startup-time dependency checker that runs before any DeckDone workflow step.

### Detection Items

| Category | Item | How to Check |
|----------|------|-------------|
| Python | Python 3.8+ available | `sys.version_info` |
| Python | `pypdf` installed | `import pypdf` |
| Python | `pypdfium2` installed | `import pypdfium2` |
| Python | `pdfplumber` installed | `import pdfplumber` |
| Node.js | Node.js 18+ available | `node --version` subprocess |
| Node.js | `pptxgenjs` global module | `npm list -g pptxgenjs` |
| Node.js | `playwright` global module | `npm list -g playwright` |
| Node.js | `sharp` global module | `npm list -g sharp` |
| System | LibreOffice available | Try: `soffice`, `libreoffice` (macOS), check common install paths |
| Node.js | Playwright browsers installed | Check `%LOCALAPPDATA%\ms-playwright` (Win) or `~/.cache/ms-playwright` (macOS/Linux) for browser directories |

### Behavior Modes

| Mode | Flag | Behavior |
|------|------|----------|
| Report | (default) | Print pass/fail table, exit 0 if all pass, 1 if any fail |
| Install | `--install` | For each missing item, show install command, prompt y/n, execute if confirmed |
| Install (non-interactive) | `--install --yes` | Auto-confirm all installs without prompts — use this mode when invoked by AI agents |
| JSON | `--json` | Output structured JSON for AI agent parsing |

### Install Commands Reference

Each detected item has a corresponding install command:

- Python packages: `pip install pypdf pypdfium2 pdfplumber`
- Node globals: `npm install -g pptxgenjs playwright sharp`
- Playwright browsers: `npx playwright install`
- LibreOffice: Platform-specific (apt/brew/winget)

### SKILL.md Integration

Add a "Pre-Flight Check" section before Phase 1:

```markdown
## Pre-Flight: Environment Check

Before starting Phase 1, run:

    python scripts/check-env.py

If any items fail, resolve them before proceeding. For guided installation:

    python scripts/check-env.py --install          # interactive y/n per item
    python scripts/check-env.py --install --yes    # auto-confirm all (for AI agent use)
```

### Constraints

- Python stdlib only (subprocess, importlib.util for detection)
- No side effects in report mode
- `--install` mode requires explicit y/n confirmation per item (interactive)
- `--install --yes` mode auto-confirms all installs (for AI agent use)
- Exit code: 0 = all pass, 1 = any fail, 2 = usage error

---

## Optimization 2: Image-PDF Extraction Script

### What

Add `scripts/extract-pdf.py` — handles PDFs with no text layer by converting pages to images for AI visual extraction.

### Flow

```
Input PDF
  │
  ├─ Test text layer on ALL pages (sample first, middle, last if >50 pages)
  │   ├─ All pages have text → Text extraction mode
  │   ├─ No pages have text → Full image mode
  │   └─ Mixed → Hybrid mode (text pages extracted, image pages rendered)
  │
  └─ Output to materials/ directory
```

### Behavior

1. **Text-layer detection**: For PDFs ≤50 pages, test every page with `pypdf`. For PDFs >50 pages, first sample first/middle/last pages to determine if it's fully text or fully image (fast path). If any sampled page lacks text, fall back to testing every page for per-page classification. Classify each page individually as text or image.
2. **Text extraction** (text pages): Extract text per page, write one `.md` file per text page.
3. **Image conversion** (image pages): Use `pypdfium2` to render each image page as PNG at 200 DPI, save to `materials/images/`, include in manifest.
4. **Hybrid output**: Both text `.md` files and image manifest for the same PDF.
5. **AI integration**: The manifest instructs the AI agent to process each image through visual recognition.
6. **Encrypted PDFs**: Catch `pypdf` decryption errors and print a clear message asking the user to provide a decrypted copy.

### Output Format

For text-type PDF:
```
materials/
├── 00-index.md          # Source metadata
├── 01-page-001.md       # Extracted text from page 1
├── 02-page-002.md       # Extracted text from page 2
└── ...
```

Note: Each page gets its own `.md` file (not grouped) to avoid splitting logical sections across files. The AI can merge related pages during content analysis.

For image-type PDF:
```
materials/
├── 00-index.md
├── image-pdf-manifest.md   # List of pages + AI instructions
└── images/
    ├── page-001.png
    ├── page-002.png
    └── ...
```

### Manifest Template

```markdown
# Image PDF Extraction Manifest

## Source: [filename]
## Total Pages: [N]
## Status: Images rendered, awaiting AI visual extraction

## Instructions for AI Agent
For each page image below, use visual recognition to extract:
- All text content (headings, body text, labels, data)
- Table structures (rows, columns, values)
- Chart/graph descriptions (type, data points, trends)
- Image descriptions (diagrams, photos)

## Pages
- Page 1: images/page-001.png
- Page 2: images/page-002.png
...
```

### SKILL.md Integration

Add to Step 2 (Material Collection), after "For each file provided":

```markdown
   - `.pdf` → Run `python scripts/extract-pdf.py <file> --output materials/`
     - If text-layer detected: text extracted automatically
     - If image-type: pages rendered as PNG, follow manifest instructions for visual extraction
   - If `extract-pdf.py` is unavailable, fall back to pdf skill or ask user to paste text
```

### Dependencies

- Required: `pypdf` (text detection), `pypdfium2` (image rendering)
- Optional: `pdfplumber` (better text extraction for complex layouts)
- DPI: 200 (balance between quality and file size; ~500-800KB per page)
- Large PDFs: If PDF exceeds 50 pages, automatically sample first/middle/last pages for text-layer detection instead of scanning all pages

**SKILL.md Dependencies table update**: Add these Python packages to a new `### Python (Optional)` subsection under Dependencies, with graceful degradation note: "If pypdfium2 is unavailable, image-type PDFs fall back to asking user to paste text."

### Constraints

- Python stdlib + pypdf + pypdfium2 only
- No API calls from the script (AI handles visual recognition externally)
- Graceful error on missing dependencies (print install instructions)
- Output directory created if not exists

---

## Optimization 3: Quality Check Automation

### What

Extend existing validation scripts and add a new color consistency checker.

### 3a: Extend `validate-html-slides.py`

Add the following checks. The script will be refactored to use `argparse` (stdlib) for flag handling. Backward compatible: the positional directory argument still works as before.

**CLI syntax**:
```bash
python scripts/validate-html-slides.py <directory>                          # original behavior
python scripts/validate-html-slides.py <directory> --outline outline.md     # + completeness check
```

**File completeness check** (active when `--outline` is provided):
- Accept a `--outline` parameter pointing to `outline.md`
- Parse total page count from outline
- Verify HTML file count matches page count
- Verify each HTML file is non-empty (> 100 bytes)
- Report missing or empty files

**Empty slide detection**:
- Parse each HTML file for text content in `<p>`, `<h1>`-`<h6>`, `<li>` tags
- Flag slides with fewer than 2 text elements as "potentially empty"

### 3b: New `scripts/validate-colors.py`

**Purpose**: Verify all colors used in HTML slides conform to the defined palette.

**Usage**:
```bash
python scripts/validate-colors.py <style-guide.md> <html-directory>
```

**Behavior**:
1. Parse `style-guide.md` to extract the color palette from the `## Palette:` heading line. The parser expects a single line in the format `## Palette: primary/secondary/accent/background/text — hex values`, where hex values are matched by regex `#[0-9A-Fa-f]{6}`. If the palette heading is not found or contains fewer than 3 hex values, print a warning and exit with code 2.
2. Scan all HTML files for color values in:
   - `style` attributes: `color`, `background`, `background-color`, `border`, `border-color`
   - `<style>` blocks: same CSS properties
3. Extract hex colors only (`#RGB` expanded to `#RRGGBB`, `#RRGGBB` as-is). Skip named colors, `rgb()`/`rgba()` notation, `transparent`, `inherit`, and `var()` references — these are allowed without validation.
4. Normalize to `#RRGGBB` uppercase format
5. Compare against palette + allowlisted colors
6. Report any colors not in the allowed set

**Output**:
```
=== Color Consistency Check ===
Palette: #1B365D, #2E5C8A, #E8A838, #FFFFFF, #1A1A1A

slide-01-cover.html - PASS
slide-02-agenda.html - WARN
  - Unexpected color "#3A7BD5" at line 15 (closest palette: #2E5C8A)
  - Unexpected color "#F0F0F0" at line 22 (wireframe gray - acceptable)

=== Summary ===
Checked: 15 files
Pass: 13
Warn: 2
Fail: 0
```

**Tolerance**: Always-allowed colors (not requiring palette match): `#000000` (black), `#FFFFFF` (white), grayscale range `#E0E0E0`-`#F8F8F8` (wireframe grays), `#333333`-`#666666` (text grays), `#999999`/`#AAAAAA`/`#CCCCCC` (borders/connectors). Named colors, `rgb()`/`rgba()`, `transparent`, `inherit`, and CSS variables are skipped entirely.

### SKILL.md Integration

Update Step 10 (Batch Generation) validation:
```markdown
**Validation:**
- Run `python scripts/validate-html-slides.py wireframes/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md wireframes/`
```

Update Step 11 (Final Quality Review):
```markdown
**Validation:**
- Run `python scripts/validate-html-slides.py wireframes/ --outline outline.md` (re-verify completeness)
- Run `python scripts/validate-colors.py style-guide.md wireframes/` (re-verify colors)
```

---

## Implementation Order

1. `scripts/check-env.py` — standalone, no dependencies on other changes
2. `scripts/extract-pdf.py` — adds pypdfium2 to check-env detection
3. Extend `validate-html-slides.py` — builds on existing script
4. New `scripts/validate-colors.py` — standalone script
5. SKILL.md updates — update after all scripts are ready

## File Changes Summary

| Action | File | Description |
|--------|------|-------------|
| New | `scripts/check-env.py` | Environment dependency checker |
| New | `scripts/extract-pdf.py` | Image-PDF extraction pipeline |
| New | `scripts/validate-colors.py` | Color palette consistency checker |
| Modify | `scripts/validate-html-slides.py` | Add completeness and emptiness checks (use argparse) |
| Modify | `skills/deckdone/SKILL.md` | Add Pre-Flight section, update Dependencies table, update Steps 2/10/11 |

## What We Explicitly Don't Do

- **Fast/slow mode** — deferred; the current 4-phase structure provides value for complex decks
- **State management simplification** — deferred; cross-conversation resume needs full state
- **HTML template fragment library** — layout-patterns.md already has per-type templates
- **html2pptx constraint consolidation** — constraints already documented in layout-patterns.md General Guidelines section
- **Playwright thumbnail fallback** — separate concern, can be addressed independently later

## SKILL.md Line Budget Management

Current SKILL.md is 575 lines with a ~600 line budget. To create headroom for the new Pre-Flight section (~10 lines), Step 2 additions (~4 lines), and Step 10/11 updates (~4 lines):

**Mitigation**: Move the State File Templates section (lines 502-575, ~73 lines) to a new `references/state-templates.md`. Replace with a 5-line reference:

```markdown
## State File Templates

See `references/state-templates.md` for complete templates for `deckdone-state.md`, `deckdone-trace.md`, and `harness-improvements.md`.
```

This frees ~68 lines, bringing the effective count to ~507 lines with ample headroom.
