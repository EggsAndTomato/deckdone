# deckdone-style Skill Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a new `deckdone-style` skill that provides curated icons, illustration sources, enhanced style presets, and decoration rules to improve the visual quality of DeckDone-generated presentations.

**Architecture:** New skill at `skills/deckdone-style/` with SKILL.md entry point, references (icons, catalog, presets, guides, decorated templates), and scripts (fetch-icon, fetch-illustration, validate-style-assets). Minimal changes to parent `deckdone` skill (SKILL.md, quality-checklist.md, validate-content-plan.py).

**Tech Stack:** Python 3 (stdlib only for scripts), Tabler Icons SVG (MIT), unDraw API (online), Sharp/npm (optional SVG→PNG).

**Spec:** `docs/superpowers/specs/2026-04-17-deckdone-style-design.md`

---

## File Structure

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `skills/deckdone-style/SKILL.md` | Skill entry point, read by AI at workflow Steps 6/7/9/10 |
| Create | `skills/deckdone-style/references/icon-catalog.md` | Semantic → icon name mapping for content-plan Step 7 |
| Create | `skills/deckdone-style/references/illustration-sources.md` | unDraw URL templates, slug recommendations, color customization |
| Create | `skills/deckdone-style/references/enhanced-presets.md` | 18 improved style presets with icon/decoration/illustration rules |
| Create | `skills/deckdone-style/references/decoration-guide.md` | Per-page-type decoration rules (REQUIRED/RECOMMENDED/OPTIONAL) |
| Create | `skills/deckdone-style/references/layout-templates-decorated.md` | HTML templates with fixed icon/illustration `<img>` slots |
| Create | `skills/deckdone-style/references/icons/*.svg` | ~200 curated Tabler Icons SVG files |
| Create | `skills/deckdone-style/scripts/fetch-icon.py` | Download/copy icon SVG, optionally convert to PNG via Sharp |
| Create | `skills/deckdone-style/scripts/fetch-illustration.py` | Fetch unDraw SVG with accent color swap |
| Create | `skills/deckdone-style/scripts/validate-style-assets.py` | Validate icon/illustration references in content-plan.md |
| Modify | `skills/deckdone/SKILL.md` | Add deckdone-style integration at Steps 6/7/9/10 (~17 lines) |
| Modify | `skills/deckdone/references/quality-checklist.md` | Add icon/illustration validation checks |
| Modify | `skills/deckdone/scripts/validate-content-plan.py` | Accept Icon/Illustration fields |

---

## Chunk 1: Foundation (SKILL.md + icon-catalog + illustration-sources + decoration-guide)

### Task 1: Create deckdone-style directory structure

**Files:**
- Create: `skills/deckdone-style/SKILL.md`
- Create: `skills/deckdone-style/references/` (directory)
- Create: `skills/deckdone-style/scripts/` (directory)

- [ ] **Step 1: Create directories**

```bash
mkdir -p skills/deckdone-style/references/icons
mkdir -p skills/deckdone-style/scripts
```

- [ ] **Step 2: Write SKILL.md with frontmatter and overview**

Write `skills/deckdone-style/SKILL.md`:

```markdown
---
name: deckdone-style
description: "Visual resource and style enhancement skill for DeckDone. Provides curated icon catalog, illustration sources (unDraw), enhanced style presets, and per-page-type decoration rules. Use alongside the deckdone skill to add icons, illustrations, and refined visual styling to generated presentations."
---

# DeckDone-Style — Visual Resources and Style Enhancement

## Overview

DeckDone-Style provides the visual resource layer for DeckDone presentations. It owns four domains:

1. **Icons** — Curated SVG icon pack (~200 Tabler Icons) with semantic catalog mapping
2. **Illustrations** — Online illustration sources (unDraw) with color customization
3. **Enhanced Presets** — Improved style presets with decoration systems
4. **Decoration Rules** — Per-page-type rules for icon/illustration placement

The parent `deckdone` skill invokes this skill at Steps 6, 7, 9, and 10. This skill makes zero workflow decisions — it provides resources and rules that the workflow consumes.

## Skill Detection

The parent deckdone skill detects deckdone-style by attempting to read this file. If readable, the skill is available. If not, deckdone degrades to its built-in `references/style-presets.md`.

## How to Use

### At Step 6 (Visual Style Direction)

1. Read `references/enhanced-presets.md` instead of deckdone's `references/style-presets.md`
2. Read `references/decoration-guide.md` for per-page-type decoration rules
3. Recommend 2–3 enhanced presets based on purpose + audience
4. Show style previews including icon style, illustration zones, and decoration characteristics
5. User selects a style. Write `style-guide.md` including the preset's icon/decoration sections.

### At Step 7 (Detailed Content Plan)

1. Read `references/icon-catalog.md` for semantic → icon mappings
2. For each zone, assign an icon name from the catalog when the decoration guide mandates one
3. Add to each zone: `- Icon: [name or "None"]`
4. For Cover and Section Divider pages: add `- Illustration: [unDraw slug or "None"]`

### At Step 9/10 (Test/Batch Generation)

1. Run `scripts/fetch-icon.py <icon_name> <output_dir> [--size N]` for each assigned icon
2. Run `scripts/fetch-illustration.py <slug> <accent_color> <output_dir>` for cover/divider illustrations
3. Use `references/layout-templates-decorated.md` instead of deckdone's `references/layout-templates.md`
4. Place icons in HTML per `references/decoration-guide.md` rules

### Validation

After Step 7, run:
```bash
python scripts/validate-style-assets.py <content-plan.md> --catalog references/icon-catalog.md --icons-dir references/icons/
```

## Dependencies

| Dependency | Type | Purpose |
|-----------|------|---------|
| Tabler Icons | Bundled SVGs | ~200 curated icons in `references/icons/` |
| unDraw | Online API | Illustration fetching (requires internet) |
| Sharp (npm global) | Optional | SVG→PNG rasterization for icons/illustrations |

## Graceful Degradation

| Component Missing | Behavior |
|-------------------|----------|
| unDraw unreachable | No illustrations; geometric CSS patterns as fallback |
| Sharp unavailable | SVG icons/illustrations used directly via `<img>` |
| fetch-icon.py fails | AI inlines SVG content directly into HTML |
| Icon not found (local + CDN) | AI uses Unicode text markers (▶ ● ◆ →) |

## Harness Improvement Principle

When a generated slide has icon or illustration quality issues, fix the harness — not the slide. Update:
- `references/icon-catalog.md` if icon choices are semantically wrong
- `references/decoration-guide.md` if placement rules are inappropriate
- `references/enhanced-presets.md` if style/decoration settings produce poor results
- `references/layout-templates-decorated.md` if icon/illustration slots cause layout problems

Log all improvements in deckdone's shared `harness-improvements.md`.
```

- [ ] **Step 3: Verify SKILL.md line count is under 100 lines**

Run: `python -c "print(sum(1 for _ in open('skills/deckdone-style/SKILL.md', encoding='utf-8')))"`

Expected: under 100 lines (this is just the entry point; details are in references)

- [ ] **Step 4: Commit**

```bash
git add skills/deckdone-style/SKILL.md
git commit -m "feat(deckdone-style): add SKILL.md entry point"
```

---

### Task 2: Create icon-catalog.md

**Files:**
- Create: `skills/deckdone-style/references/icon-catalog.md`

- [ ] **Step 1: Write icon-catalog.md**

Write `skills/deckdone-style/references/icon-catalog.md`:

```markdown
# Icon Catalog — Semantic Mapping

Reference for Step 7 (Content Plan). Maps content themes and page zones to specific icon names from the bundled Tabler Icons set.

## Usage

During content planning, match each zone's semantic theme to an icon below. If no exact match exists, use the closest category. Every icon name must correspond to a file in `references/icons/{name}.svg`.

---

## By Content Theme

| Theme | Icon Name | Also Good For |
|-------|-----------|---------------|
| growth / revenue | trending-up | KPI, increase, improvement |
| decline / decrease | trending-down | loss, reduction, risk |
| strategy / plan | target | goals, focus, objective |
| team / collaboration | users-group | teamwork, group, collective |
| individual / person | user | personal, individual, member |
| leadership / management | crown | executive, authority, C-suite |
| technology / IT | code | software, engineering, dev |
| infrastructure | server | hardware, backend, hosting |
| data / database | database | storage, records, persistence |
| cloud / networking | cloud | internet, SaaS, remote |
| AI / machine learning | robot | automation, ML, intelligent |
| analytics / data viz | chart-bar | statistics, metrics, reporting |
| trends / time series | chart-line | progress, trajectory, forecast |
| pie / proportions | chart-pie | distribution, segments, share |
| communication | message | chat, messaging, dialog |
| email / outreach | mail | contact, newsletter, inbox |
| presentation / public speaking | presentation | slides, keynote, talk |
| announcement | megaphone | broadcast, promotion, alert |
| finance / budget | coin | money, cost, pricing |
| investment | chart-candle | trading, market, portfolio |
| receipt / billing | receipt | invoice, payment, transaction |
| process / workflow | list-check | steps, procedure, operations |
| settings / configuration | settings | preferences, options, control |
| refresh / update | refresh | reload, sync, retry |
| timeline / roadmap | clock | schedule, deadline, timing |
| schedule / calendar | calendar | date, event, planning |
| security / protection | shield | safety, compliance, guard |
| risk / warning | alert-triangle | caution, danger, attention |
| success / achievement | trophy | win, award, recognition |
| failure / error | x | cancel, reject, remove |
| approval / correct | check | confirm, validate, done |
| innovation / idea | rocket | launch, startup, breakthrough |
| learning / education | school | training, course, academy |
| knowledge / docs | book | documentation, manual, guide |
| creativity / design | pencil | edit, write, create |
| tool / utility | tool | build, fix, utility |
| speed / performance | bolt | fast, energy, power |
| growth / nature | leaf | eco, green, organic |
| energy / enthusiasm | flame | passion, hot, trending |
| celebration / milestone | stars | highlight, featured, premium |
| global / international | world | worldwide, global, earth |
| connection / link | link | URL, reference, association |
| download | download | import, retrieve, save |
| upload | upload | export, publish, deploy |
| search / find | search | query, lookup, discover |
| filter / refine | filter | narrow, sort, criteria |
| lock / privacy | lock | secure, private, restricted |
| unlock / open | lock-open | access, permission, granted |
| folder / organize | folder | directory, collection, group |
| copy / duplicate | copy | clone, replicate, backup |
| external / outbound | external-link | open, redirect, outside |
| arrow / direction | arrow-right | next, proceed, continue |
| expand / detail | chevron-right | drill-down, show-more, navigate |
| checklist | checklist | task-list, todo, validation |
| notification | bell | alert, remind, notify |
| heart / favorite | heart | like, love, endorse |
| star / rating | star | review, score, premium |
| flag / milestone | flag | marker, milestone, important |
| home / start | home | landing, dashboard, main |
| briefcase / business | briefcase | work, corporate, professional |
| question / help | help | support, FAQ, assistance |
| info / information | info-circle | details, about, context |
| plus / add | plus | create, new, insert |
| minus / remove | minus | delete, reduce, subtract |

---

## By Page Type Defaults

Icons that should be selected when no specific theme override is needed.

| Page Type | Default Icon |
|-----------|-------------|
| Cover | (match presentation topic from brief) |
| Agenda | list-check |
| Section Divider | (match section theme) |
| Content-Text | (none required) |
| Content-TwoCol | (none required) |
| Data-Chart | chart-bar |
| Quote | star |
| Timeline | clock |
| Comparison | scale (or chevron-right vs chevron-left) |
| Closing | flag |
| Composite-Diagram | (match diagram topic) |
| Pipeline-Flow | arrow-right |

---

## By Page Zone

Guidance for icon sizes in specific page positions.

| Zone Position | Icon Size | When to Use |
|---------------|-----------|-------------|
| Slide title prefix | 32–48pt | Always on Cover, Section Divider; optional elsewhere |
| Bullet point prefix | 16pt | Recommended for Content-Text and Content-TwoCol H2 items |
| Timeline event node | 24pt | Always; replaces text marker |
| Pipeline stage header | 32pt | Always; top of each stage card |
| Comparison column header | 24pt | Recommended for each side |
| Composite-Diagram subsystem | 20pt | Recommended for subsystem labels |
| Chart interpretation | 16pt | Optional; insight/lightbulb icon |

---

## Icon Naming Convention

All icon names use kebab-case matching the Tabler Icons outline set naming:
- Valid: `trending-up`, `chart-bar`, `list-check`
- Invalid: `TrendingUp`, `chart_bar`, `listcheck`

To verify an icon exists: check for `references/icons/{name}.svg` file.
To find new icons: browse https://tabler.io/icons (use outline style names).
```

- [ ] **Step 2: Verify file is valid markdown**

Run: `python -c "f=open('skills/deckdone-style/references/icon-catalog.md',encoding='utf-8'); print(sum(1 for _ in f), 'lines')"`

Expected: ~130-140 lines

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone-style/references/icon-catalog.md
git commit -m "feat(deckdone-style): add icon-catalog.md with semantic mappings"
```

---

### Task 3: Create illustration-sources.md

**Files:**
- Create: `skills/deckdone-style/references/illustration-sources.md`

- [ ] **Step 1: Write illustration-sources.md**

Write `skills/deckdone-style/references/illustration-sources.md`:

```markdown
# Illustration Sources

Reference for Step 9/10 (Generation). Provides illustration source configuration for fetching themed SVG illustrations.

---

## unDraw (Primary Source)

| Property | Value |
|----------|-------|
| **URL** | https://undraw.co |
| **License** | Free, no attribution required |
| **Format** | SVG |
| **Color customization** | Replace default `#6C63FF` with accent color |
| **Best for** | Cover slides, Section Dividers |

### How It Works

1. Browse or search illustrations at https://undraw.co/illustrations
2. Each illustration has a slug (visible in the URL, e.g., `business-plan`)
3. `fetch-illustration.py` downloads the SVG and swaps the primary color
4. The SVG/PNG is placed in the slide's illustration zone

### Color Replacement

All unDraw SVGs use a single primary color (`#6C63FF`). The fetch script:
1. Replaces `#6C63FF` and `#6c63ff` (case-insensitive) with the preset's accent color
2. If neither color is found: replaces the most frequent hex color (heuristic fallback, logs warning)

---

## Recommended Illustrations by Presentation Theme

| Section Theme | Recommended Slugs | Visual Description |
|---------------|-------------------|-------------------|
| Business Strategy | `business-plan`, `strategy`, `growth` | Charts, targets, upward arrows |
| Technology | `developer-activity`, `coding`, `server` | Screens, code, devices |
| Team & People | `team-spirit`, `collaboration`, `meeting` | People working together |
| Data & Analytics | `data-analysis`, `statistics`, `metrics` | Dashboards, graphs |
| Success & Goals | `finish-line`, `achiever`, `winner` | Trophies, checkmarks, celebrations |
| Innovation | `innovative`, `creative`, `brainstorming` | Lightbulbs, rockets, ideas |
| Finance | `investment`, `savings`, `finance` | Money, charts, growth |
| Communication | `messaging`, `presentation`, `connecting` | Speech bubbles, devices |
| Education | `education`, `learning`, `knowledge` | Books, graduation, classroom |
| Security | `security`, `protection`, `safe` | Shields, locks, guards |
| Health | `health`, `medical`, `wellness` | Hearts, medical, activity |
| Travel | `travel`, `adventure`, `destination` | Maps, planes, landmarks |

---

## Access Notes

- unDraw is accessible from China mainland (verified 2026-04)
- The API endpoint `undraw.co/api/illustration/{slug}` is unofficial and may change
- If unDraw is unreachable: degrade to CSS geometric patterns (circles, rectangles) using the accent color
- Pre-downloaded fallback illustrations could be added to `references/illustrations/` if needed

## Alternative Sources (Future)

These are NOT currently integrated but noted for potential future use:

| Source | URL | License | Notes |
|--------|-----|---------|-------|
| Open Peeps | https://www.openpeeps.com | CC0 | Hand-drawn characters; requires Figma/Sketch |
| Open Doodles | https://www.opendoodles.com | CC0 | Sketchy illustrations; direct SVG download |
| Humaaans | https://www.humaaans.com | CC0 | Mix-and-match people; Figma-based |
| DrawKit | https://www.drawkit.com | MIT (free tier) | Polished illustrations; some premium |
```

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone-style/references/illustration-sources.md
git commit -m "feat(deckdone-style): add illustration-sources.md"
```

---

### Task 4: Create decoration-guide.md

**Files:**
- Create: `skills/deckdone-style/references/decoration-guide.md`

- [ ] **Step 1: Write decoration-guide.md**

Write `skills/deckdone-style/references/decoration-guide.md`:

```markdown
# Decoration Guide — Per-Page-Type Rules

Reference for Step 7 (Content Plan) and Step 9/10 (Generation). Defines which visual elements (icons, illustrations, decorative patterns) are placed where on each page type.

## Severity Levels

| Level | Meaning |
|-------|---------|
| REQUIRED | Must be present. Missing = validation failure. |
| RECOMMENDED | Should be present. Absence tolerated but logged. |
| OPTIONAL | Nice to have. No validation impact. |

---

## Cover

- **[REQUIRED]** Right or bottom 25% area: illustration from unDraw (fetched via `fetch-illustration.py`)
- **[REQUIRED]** Title left: 48pt icon matching the presentation's main theme (from `icon-catalog.md`)
- **[OPTIONAL]** Background: subtle gradient or geometric pattern in accent color tint (10% opacity)

## Agenda

- **[RECOMMENDED]** Each numbered item: 16pt icon prefix matching the section theme
- **[OPTIONAL]** Right margin: vertical accent line in primary color

## Section Divider

- **[REQUIRED]** Title left: 40pt icon reflecting the section's theme
- **[RECOMMENDED]** Bottom 20%: illustration from unDraw or decorative pattern
- **[OPTIONAL]** Background: subtle accent tint (5% opacity overlay)

## Content-Text

- **[RECOMMENDED]** Each top-level bullet: 16pt icon prefix (semantic match from catalog)
- **[OPTIONAL]** Title underline: 2px accent color line, 48pt wide, 4pt below title
- **[OPTIONAL]** Left margin: thin vertical accent line (1px, 20% opacity)

## Content-TwoCol

- **[RECOMMENDED]** Each column heading: 24pt icon prefix
- **[OPTIONAL]** Center divider: 1px line in secondary color
- **[OPTIONAL]** Each bullet: 14pt icon prefix

## Data-Chart

- **[REQUIRED]** Chart area: pre-rendered PNG chart (existing deckdone behavior)
- **[RECOMMENDED]** Interpretation text area: 16pt `info-circle` or `trending-up` icon prefix
- **[OPTIONAL]** Chart border: 1px rounded rectangle in secondary color

## Quote

- **[RECOMMENDED]** Large decorative opening quotation mark (60pt, accent color, 30% opacity)
- **[OPTIONAL]** Closing quotation mark (right-aligned, 40pt)
- No icons — Quote pages use typography as decoration.

## Timeline

- **[REQUIRED]** Each event node: 24pt icon (circular crop, `border-radius: 50%`)
  - Default icons: `clock` for past, `flag` for current, `rocket` for future
  - Override with semantic theme icons from catalog
- **[RECOMMENDED]** Connecting line: 2px solid primary color between nodes
- **[OPTIONAL]** Node background: small circular fill in accent color (behind icon)

## Comparison

- **[RECOMMENDED]** Each side header: 24pt icon (e.g., `check` vs `x`, or thematic icons)
- **[RECOMMENDED]** Boolean comparison cells: ✓ (`check` icon) / ✗ (`x` icon) instead of text
- **[OPTIONAL]** Alternating row background tint (5% primary color)

## Closing

- **[REQUIRED]** Centered icon above takeaway: 48pt `flag` or `rocket` or theme icon
- **[OPTIONAL]** Background: subtle gradient matching cover slide (bookend effect)
- **[OPTIONAL]** Bottom decorative line in accent color

## Composite-Diagram

- **[RECOMMENDED]** Subsystem/layer header: 20pt icon prefix
- **[OPTIONAL]** Background tint per layer (alternating 3% and 5% primary color)
- **[OPTIONAL]** Connection arrows: 1px lines with arrowheads in secondary color

## Pipeline-Flow

- **[REQUIRED]** Each stage header: 32pt icon (semantic match: `search` → input, `settings` → process, `check` → validate, `rocket` → output)
- **[REQUIRED]** Arrow connectors: SVG arrow style (not plain `→` text). Use a styled `<div>` with chevron icon or CSS triangle in primary color.
- **[RECOMMENDED]** Stage cards: 1pt border in primary color, 4px border-radius
- **[OPTIONAL]** Active/current stage: accent color border highlight (2pt)
```

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone-style/references/decoration-guide.md
git commit -m "feat(deckdone-style): add decoration-guide.md"
```

---

## Chunk 2: Scripts (fetch-icon, fetch-illustration, validate-style-assets)

### Task 5: Create fetch-icon.py

**Files:**
- Create: `skills/deckdone-style/scripts/fetch-icon.py`

- [ ] **Step 1: Write fetch-icon.py**

Write `skills/deckdone-style/scripts/fetch-icon.py`:

```python
#!/usr/bin/env python3
"""Fetch a Tabler icon SVG. Checks local icons/ first, then jsdelivr CDN."""

import argparse
import os
import shutil
import subprocess
import sys
import urllib.request
import urllib.error

TABLER_CDN = "https://cdn.jsdelivr.net/npm/@tabler/icons@3.41.1/icons/outline/{name}.svg"
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
                "node", "-e",
                f'require("sharp")("{input_path}").resize({size},{size}).png().toFile("{output_path}").then(()=>process.exit(0)).catch(()=>process.exit(1))'
            ],
            capture_output=True, timeout=30
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main():
    parser = argparse.ArgumentParser(description="Fetch a Tabler icon SVG/PNG")
    parser.add_argument("name", help="Icon name (kebab-case, e.g. chart-bar)")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--size", type=int, default=48, help="PNG size in pixels (default: 48)")
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
            print(f"Error: Icon '{args.name}' not found locally or on CDN", file=sys.stderr)
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
```

- [ ] **Step 2: Test with a local icon (will fail gracefully since no icons yet)**

Run: `python skills/deckdone-style/scripts/fetch-icon.py trending-up ./tmp/test-icons`
Expected: "Error: Icon 'trending-up' not found locally or on CDN" (exit 2) or succeeds if CDN reachable

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone-style/scripts/fetch-icon.py
git commit -m "feat(deckdone-style): add fetch-icon.py script"
```

---

### Task 6: Create fetch-illustration.py

**Files:**
- Create: `skills/deckdone-style/scripts/fetch-illustration.py`

- [ ] **Step 1: Write fetch-illustration.py**

Write `skills/deckdone-style/scripts/fetch-illustration.py`:

```python
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
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError):
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

    hex_colors = re.findall(r'#[0-9a-fA-F]{6}', svg_text)
    if hex_colors:
        most_common = Counter(hex_colors).most_common(1)[0][0]
        return svg_text.replace(most_common, new_color), True

    return svg_text, True


def sharp_convert(input_path, output_path):
    try:
        result = subprocess.run(
            [
                "node", "-e",
                f'require("sharp")("{input_path}").resize(800,600).fit("inside").png().toFile("{output_path}").then(()=>process.exit(0)).catch(()=>process.exit(1))'
            ],
            capture_output=True, timeout=30
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main():
    parser = argparse.ArgumentParser(description="Fetch unDraw illustration with custom color")
    parser.add_argument("slug", help="unDraw illustration slug (e.g. business-plan)")
    parser.add_argument("accent_color", help="Accent color hex (e.g. #E8A838)")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--png", action="store_true", help="Also convert to PNG via Sharp")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    svg_url = fetch_illustration_url(args.slug)
    if not svg_url:
        print(f"Error: Could not fetch illustration '{args.slug}' from unDraw", file=sys.stderr)
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
        print(f"Warning: Used heuristic color replacement for {args.slug}", file=sys.stderr)
        print(f"OK: {args.slug}.svg ({len(svg_text)} bytes, heuristic color)", file=sys.stderr)
        exit_code = 2
    else:
        print(f"OK: {args.slug}.svg ({len(svg_text)} bytes, color: {args.accent_color})")
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
```

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone-style/scripts/fetch-illustration.py
git commit -m "feat(deckdone-style): add fetch-illustration.py script"
```

---

### Task 7: Create validate-style-assets.py

**Files:**
- Create: `skills/deckdone-style/scripts/validate-style-assets.py`

- [ ] **Step 1: Write validate-style-assets.py**

Write `skills/deckdone-style/scripts/validate-style-assets.py`:

```python
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

    for match in re.finditer(r"\|\s*`?([\w-]+)`?\s*\|", text):
        name = match.group(1).strip()
        if name and not name.startswith("-") and name not in ("Icon Name", "name", "Required"):
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

    for match in re.finditer(r"^\s*-\s*Illustration\s*[:：]\s*(.+)$", text, re.MULTILINE):
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
    parser.add_argument("--icons-dir", required=True, help="Path to references/icons/ directory")
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
```

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone-style/scripts/validate-style-assets.py
git commit -m "feat(deckdone-style): add validate-style-assets.py script"
```

---

## Chunk 3: Curated Icon Pack

### Task 8: Download and curate Tabler Icons

**Files:**
- Create: `skills/deckdone-style/references/icons/*.svg` (~200 files)

- [ ] **Step 1: Write a one-time download script (not committed)**

Create a temporary `scripts/_download-icons.py` (utility only, not part of the skill):

```python
#!/usr/bin/env python3
"""One-time utility to download curated Tabler Icons. NOT part of the skill."""
import os
import urllib.request
import urllib.error
import time

CDN = "https://cdn.jsdelivr.net/npm/@tabler/icons@3.41.1/icons/outline/{name}.svg"

ICONS = [
    # Growth & Metrics
    "trending-up", "trending-down", "chart-bar", "chart-line", "chart-pie",
    "chart-candle", "arrow-up-right", "target", "gauge", "report-analytics",
    "report", "chart-arrows", "chart-dots", "chart-area",
    "numbers", "percentage", "hash", "math-function", "delta",
    # People & Team
    "users", "user-plus", "handshake", "brain", "heart", "eye",
    "users-group", "user", "crown", "megaphone",
    "man", "woman", "baby", "school", "stethoscope",
    # Technology
    "code", "server", "database", "cloud", "cpu", "wifi",
    "robot", "terminal", "device-desktop", "device-mobile",
    "bug", "git-branch", "binary", "encryption",
    "stack", "layers-subtract", "component", "plug", "webhook",
    # Process & Flow
    "arrows-transfer-up", "refresh", "settings", "list-check", "clock",
    "checklist", "timeline", "subtask", "transfer-in", "transfer-out",
    "arrows-sort", "sort-ascending", "sort-descending", "filter", "adjustments",
    "arrows-exchange", "arrows-join", "arrows-split", "route", "transform-point",
    # Communication
    "mail", "message", "presentation", "news",
    "messages", "quote", "note", "notes",
    "share", "forward", "reply", "phone", "headset",
    # Finance
    "coin", "currency-dollar", "receipt", "wallet", "piggy-bank",
    "credit-card", "bank", "cash", "businessplan",
    # Status & Actions
    "check", "x", "alert-triangle", "info-circle", "plus", "minus",
    "download", "upload", "circle-check", "circle-x",
    "alert-circle", "help", "exclamation-mark",
    "thumbs-up", "thumbs-down", "star", "bookmark",
    # Navigation & Layout
    "chevron-right", "arrow-right", "external-link", "layout", "grid",
    "list", "chevron-left", "chevron-down", "chevron-up", "dots",
    "menu", "dots-vertical", "arrow-left", "arrow-down", "arrow-up",
    # Nature & Abstract
    "leaf", "sun", "sparkles", "stars", "rocket", "flag", "flame", "bolt",
    "moon", "cloud-rain", "flower", "tree", "world", "mountain",
    # Objects
    "book", "briefcase", "calendar", "folder", "lock", "lock-open", "shield", "tool",
    "pencil", "palette", "photo", "camera", "microscope", "beaker", "globe", "compass",
    "map", "home", "building", "truck",
    # Arrows & Connectors
    "arrow-back-up", "arrow-forward-up", "circle-arrow-right",
    "square-arrow-right", "arrow-badge-right", "arrow-wave-right",
    "arrow-big-right", "arrow-big-down", "circle",
    # Search & Discovery
    "search", "zoom-in", "zoom-out", "scan", "eye",
    # Misc useful
    "bell", "link", "copy", "clock", "trophy", "letter-a",
]

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "references", "icons")
os.makedirs(OUT_DIR, exist_ok=True)

success = 0
failed = 0
for name in ICONS:
    out_path = os.path.join(OUT_DIR, f"{name}.svg")
    if os.path.exists(out_path):
        success += 1
        continue
    url = CDN.format(name=name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "deckdone-style/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                with open(out_path, "wb") as f:
                    f.write(resp.read())
                success += 1
                print(f"  OK: {name}")
            else:
                failed += 1
                print(f"  FAIL ({resp.status}): {name}")
    except Exception as e:
        failed += 1
        print(f"  FAIL: {name} ({e})")
    time.sleep(0.1)

print(f"\nDone: {success} downloaded, {failed} failed")
```

- [ ] **Step 2: Run download script**

Run: `python skills/deckdone-style/scripts/_download-icons.py`
Expected: ~180-200 successful downloads, some may fail (non-existent icon names)

- [ ] **Step 3: Count downloaded icons**

Run: `ls skills/deckdone-style/references/icons/*.svg | Measure-Object | Select-Object -ExpandProperty Count`
Expected: 150-200 files

- [ ] **Step 4: Verify total size is under 1MB**

Run: `Get-ChildItem skills/deckdone-style/references/icons/ | Measure-Object -Property Length -Sum | Select-Object -ExpandProperty Sum`
Expected: < 1,000,000 bytes (~500-800KB)

- [ ] **Step 5: Spot-check a few SVGs are valid XML**

Run: `python -c "import xml.etree.ElementTree as ET; ET.parse('skills/deckdone-style/references/icons/trending-up.svg'); print('OK')"`
Expected: OK

- [ ] **Step 6: Delete the temporary download script**

Run: `rm skills/deckdone-style/scripts/_download-icons.py`

- [ ] **Step 7: Commit icons**

```bash
git add skills/deckdone-style/references/icons/
git commit -m "feat(deckdone-style): add curated Tabler Icons SVG pack (~200 icons)"
```

---

## Chunk 4: Enhanced Presets

### Task 9: Create enhanced-presets.md

**Files:**
- Create: `skills/deckdone-style/references/enhanced-presets.md`

This is a large file (~600 lines). Write it by transforming each of the 18 existing presets from `skills/deckdone/references/style-presets.md` with a mechanical approach.

- [ ] **Step 1: Write enhanced-presets.md using transformation rules**

Write `skills/deckdone-style/references/enhanced-presets.md`. For each preset in `style-presets.md`, apply this **exact transformation**:

1. Copy the original sections: description, palette table, typography, decoration, best suited for, pre-render
2. After the existing **Typography** line, insert this block (same for all presets):

```
**Icon Style:** Stroke width 1.5px. Color: primary for title icons, secondary for bullet icons, accent for highlight icons. Sizes: 48pt title, 32pt section, 24pt node, 16pt bullet.

**Illustration Zone:** Cover right 25%, max-height 120pt. Section Divider bottom 20%, max-height 80pt. Other types: none.
```

3. Replace the existing **Decoration** section with an enhanced version that adds to the original. Use these rules per preset personality:

| Preset | Enhanced Decoration |
|--------|-------------------|
| Corporate Blue | Subtle 2px bottom borders in primary on headers. Rounded rectangles (8px radius) for content cards. Header accent underline 48pt wide. |
| Ocean Teal | Thin horizontal rules in secondary. Soft rounded cards with 6px radius and light shadows. Header accent underline with dot end-caps. |
| Forest Green | Organic rounded shapes. Warm cream backgrounds. Accent earthy tan borders. Leaf-inspired accent dots on title slides. |
| Sunset Warmth | Bold geometric accent bars (4px) along left edge. Warm gradient on title slide backgrounds. Circular badge elements in accent color. |
| Midnight Purple | Elegant gold accent lines 1px under headings. Soft lavender-tinted backgrounds. Decorative diamond shapes (8pt) as section markers. |
| Steel Gray | No decorative borders. Flat rectangular content blocks. Blue accent used sparingly: data highlights and CTA only. Thin 1px dividers. |
| Cherry Red | Strong red header bars spanning full width. Dark accent blocks for key metrics. Warning-style iconography. Bold 3px accent lines. |
| Navy Gold | Gold accent lines 2px under headings. Navy sidebar strip left edge 40pt wide. Classic serif styling. Gold corner brackets (16pt). |
| Arctic Blue | Grid-line patterns in light blue (0.5px). Orange accent for chart highlights. Tabular layouts with clean cell borders. |
| Terracotta Earth | Warm-toned border frames (2px, secondary). Rounded shapes with earthy feel. Cream backgrounds. Decorative terracotta dot clusters. |
| Electric Neon | Neon glow effects on accent text. Dark backgrounds with luminous border highlights. Gradient overlays mixing cyan and purple. |
| Sage Serenity | Soft muted borders in sage tones. Large rounded content blocks 12px radius. Minimal decoration — generous white space. Thin 1px sage dividers. |
| Crimson Elite | Bold gold accent lines 2px and corner embellishments. Deep crimson header blocks. Serif headings with tight letter-spacing. Gold star marks. |
| Teal Coral | Clean teal borders 1px. Coral callout boxes with rounded corners. Pill shapes for statistics. Structured grid with teal borders. |
| Dark Carbon | Subtle gradient transitions between dark tones. Thin bright accent lines for section breaks. Code-block styled areas. |
| Warm Sand | Warm rounded frames 6px radius. Sand-colored backgrounds. Brown accent underlines on headings 2px. Friendly padding. |
| Royal Indigo | Gold accent dividers 2px and star-shaped highlights. Deep indigo header bands. Wide letter-spacing for headings. Gold dot accents. |
| Clean White | No decoration. Content is decoration. Blue accent for hyperlinks and CTA only. Maximum white space. Thin 1px gray dividers. |

4. Keep the existing **Pre-render** line unchanged.

- [ ] **Step 2: Verify line count**

Run: `python -c "print(sum(1 for _ in open('skills/deckdone-style/references/enhanced-presets.md', encoding='utf-8')))"`
Expected: ~550-650 lines

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone-style/references/enhanced-presets.md
git commit -m "feat(deckdone-style): add enhanced-presets.md (18 presets with icon/decoration)"
```

---

## Chunk 5: Decorated Layout Templates

### Task 10: Create layout-templates-decorated.md

**Files:**
- Create: `skills/deckdone-style/references/layout-templates-decorated.md`

This file extends each template from `skills/deckdone/references/layout-templates.md` (565 lines) by adding icon and illustration `<img>` slots. Use a mechanical transformation.

- [ ] **Step 1: Write layout-templates-decorated.md using transformation rules**

Copy `skills/deckdone/references/layout-templates.md` as the starting point. Then apply these **exact transformations** per template:

**Cover** — Wrap existing centered content in a flex row. Add illustration area:

Find the `<div class="slide">` content and restructure to:
```html
<div class="slide">
  <div style="display: flex; width: 100%; align-items: center;">
    <div style="flex: 1;">
      <!-- DECKDONE-STYLE: theme icon slot -->
      <img src="ICON_THEME" style="width: 48pt; height: 48pt; margin-bottom: 16pt;" />
      <h1 style="font-size: 36pt; text-align: center; margin: 0 0 12pt 0;">Title Here</h1>
      <p style="font-size: 18pt; text-align: center; margin: 0 0 24pt 0;">Subtitle goes here</p>
      <p style="font-size: 12pt; text-align: center; margin: 0;">Author · Date</p>
    </div>
    <!-- DECKDONE-STYLE: illustration slot -->
    <div style="flex: 0 0 25%; display: flex; align-items: center; justify-content: center;">
      <img src="ILLUSTRATION" style="max-width: 100%; max-height: 120pt;" />
    </div>
  </div>
</div>
```

**Agenda** — Add optional icons before each `<li>`:

Before each `<li>Topic`, insert:
```html
      <li><img src="ICON_SECTION" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Topic One</li>
```

**Section Divider** — Add icon and optional illustration:

```html
<div class="slide">
  <div style="display: flex; align-items: center; margin-bottom: 16pt;">
    <!-- DECKDONE-STYLE: section icon slot -->
    <img src="ICON_SECTION" style="width: 40pt; height: 40pt; margin-right: 16pt;" />
    <h1 style="font-size: 40pt; margin: 0;">Section Title</h1>
  </div>
  <p style="font-size: 16pt; margin: 0; max-width: 480pt;">Brief description.</p>
  <!-- DECKDONE-STYLE: illustration slot -->
  <div style="position: absolute; bottom: 48pt; right: 80pt;">
    <img src="ILLUSTRATION" style="max-height: 80pt;" />
  </div>
</div>
```

**Content-Text** — Add optional icons before bullets:

Change each `<li>` to:
```html
<li><img src="ICON_BULLET" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />First key point</li>
```

**Content-TwoCol** — Add icons before column headings:

```html
<h2 style="margin: 0 0 8pt 0;"><img src="ICON_COL" style="width: 24pt; height: 24pt; vertical-align: middle; margin-right: 6pt;" />Left Heading</h2>
```

**Data-Chart** — Add insight icon before interpretation:

```html
<p style="margin: 8pt 0 0 0;"><img src="info-circle" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Key insight text</p>
```

**Quote** — Add decorative quotation marks (no icon changes):

```html
<p style="font-size: 60pt; color: ACCENT; opacity: 0.3; margin: 0; line-height: 0.5;">"</p>
<p style="font-size: 24pt; font-style: italic; ...">"Quotation text..."</p>
```

**Timeline** — Replace text markers with icon images per event:

```html
<div class="event">
  <!-- DECKDONE-STYLE: event icon slot -->
  <img src="ICON_EVENT" style="width: 24pt; height: 24pt; border-radius: 50%; margin: 0 auto 6pt; display: block;" />
  <h3 style="margin: 0 0 6pt 0;">Q1 2025</h3>
  <p style="margin: 0;">Milestone one</p>
</div>
```

**Comparison** — Add icons before headers and check/x for booleans:

```html
<div><h2 style="margin: 0;"><img src="ICON_A" style="width: 24pt; height: 24pt; vertical-align: middle; margin-right: 6pt;" />Option A</h2></div>
```

**Closing** — Add centered icon above takeaway:

```html
<div class="slide">
  <!-- DECKDONE-STYLE: closing icon slot -->
  <img src="ICON_CLOSING" style="width: 48pt; height: 48pt; margin-bottom: 16pt;" />
  <h1 style="...">Key Takeaway</h1>
  ...
</div>
```

**Composite-Diagram (13a-13d)** — Add icons before subsystem labels:

```html
<p style="margin: 0 0 6pt 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Subsystem A</p>
```

**Pipeline-Flow** — Add icons per stage and styled arrow connectors:

```html
<div class="stage">
  <!-- DECKDONE-STYLE: stage icon slot -->
  <img src="ICON_STAGE" style="width: 32pt; height: 32pt; margin: 0 auto 4pt; display: block;" />
  <h3 style="margin: 0 0 4pt 0;">Stage 1</h3>
  <p style="margin: 0;">Input</p>
</div>
<div class="connector"><img src="chevron-right" style="width: 16pt; height: 16pt;" /></div>
```

Apply all transformations to produce the complete file. Mark every insertion with `<!-- DECKDONE-STYLE: ... -->` comments.

- [ ] **Step 2: Verify all 12 base templates are covered**

Check that file contains sections for: Cover, Agenda, Section Divider, Content-Text, Content-TwoCol, Data-Chart, Quote, Timeline, Comparison, Closing, Composite-Diagram (13a-13d), Pipeline-Flow.

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone-style/references/layout-templates-decorated.md
git commit -m "feat(deckdone-style): add decorated layout templates with icon slots"
```

---

## Chunk 6: Integration with Parent deckdone Skill

### Task 11: Update deckdone SKILL.md

**Files:**
- Modify: `skills/deckdone/SKILL.md` (~17 lines added)

- [ ] **Step 1: Add deckdone-style to Optional Dependencies table**

After the `theme-factory skill` row in the Optional Dependencies table (around line 51), add:

```
| deckdone-style skill | Skill | Use built-in `references/style-presets.md`, no icons or illustrations |
```

- [ ] **Step 2: Add style-integration note to Step 6**

After line "1. Read `references/style-presets.md` (15–20 style presets)." (around line 361), add:

```
   - If deckdone-style skill is available, read its `references/enhanced-presets.md` instead. Also read `references/decoration-guide.md`.
```

- [ ] **Step 3: Add icon/illustration fields to Step 7**

After the existing zone template (around line 415, after `- Pre-render:` field), add:

```
   - For each zone, when deckdone-style is available: add `- Icon: [name from icon-catalog.md or "None"]`
   - For Cover and Section Divider slides: add `- Illustration: [unDraw slug or "None"]`
```

- [ ] **Step 4: Add fetch commands to Step 9**

After the Pre-render elements step (around line 459), add:

```
   - If deckdone-style is available: run `fetch-icon.py` for each assigned icon and `fetch-illustration.py` for cover/divider illustrations. Use `layout-templates-decorated.md` instead of `layout-templates.md`.
```

- [ ] **Step 5: Add fetch commands to Step 10**

In the per-chunk section (around line 489), add:

```
   - If deckdone-style is available: same icon/illustration fetch as Step 9.
```

- [ ] **Step 6: Verify SKILL.md is under 600 lines**

Run: `python -c "print(sum(1 for _ in open('skills/deckdone/SKILL.md', encoding='utf-8')))"`
Expected: ~574 lines

- [ ] **Step 7: Commit**

```bash
git add skills/deckdone/SKILL.md
git commit -m "feat(deckdone): integrate deckdone-style at Steps 6/7/9/10"
```

---

### Task 12: Update quality-checklist.md

**Files:**
- Modify: `skills/deckdone/references/quality-checklist.md`

- [ ] **Step 1: Add icon/illustration checks to Step 7 section**

After the existing Step 7 checks (around line 82), add:

```markdown
- [ ] **All pages that require icons (per decoration-guide.md) have icon names assigned** — no REQUIRED icon slot is blank
- [ ] **Cover and Section Divider pages have illustration slugs or explicit "None"** — no cover/divider is missing the Illustration field
```

- [ ] **Step 2: Add icon/illustration checks to Step 9 section**

After the existing Step 9 checks (around line 91), add:

```markdown
- [ ] **All assigned icons are present as files in the test-slides directory** — no broken `<img>` references
- [ ] **Cover and divider illustrations render correctly** — not a broken image placeholder
- [ ] **Icon colors match the style guide palette** — icons use primary/secondary/accent colors, not default black
```

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/references/quality-checklist.md
git commit -m "feat(deckdone): add icon/illustration validation checks to quality checklist"
```

---

### Task 13: Update validate-content-plan.py

**Files:**
- Modify: `skills/deckdone/scripts/validate-content-plan.py`

- [ ] **Step 1: Add Icon and Illustration field awareness and optional catalog validation**

Add a new optional `--catalog` argument to `validate-content-plan.py`. When provided, validate that icon names exist in the catalog. This replaces the original no-op approach.

After the `VALID_VISUAL_WEIGHTS` set (line 22), add:

```python
ICON_CATALOG = None
```

Modify `main()` to accept optional `--catalog` argument. After the existing `parser.add_argument` line (line 125), add:

```python
    parser.add_argument("--catalog", help="Path to icon-catalog.md for icon name validation")
```

In `main()`, after reading the file (around line 131), add catalog loading:

```python
    catalog_icons = None
    if args.catalog:
        try:
            with open(args.catalog, encoding="utf-8") as cf:
                catalog_text = cf.read()
            catalog_icons = set()
            for m in re.finditer(r"\|\s*`?([\w-]+)`?\s*\|", catalog_text):
                name = m.group(1).strip()
                if name and not name.startswith("-"):
                    catalog_icons.add(name)
        except OSError:
            print(f"Warning: Could not read catalog: {args.catalog}", file=sys.stderr)
            catalog_icons = None
```

In `validate_zone()`, after the Visual Weight check (around line 112), add icon validation:

```python
        icon_val = extract_field(zs, "Icon")
        if icon_val is not None and icon_val.strip().lower() != "none":
            if catalog_icons is not None and icon_val.strip() not in catalog_icons:
                z_errs.append(f"icon '{icon_val.strip()}' not found in catalog")
```

Note: The `- Illustration:` field is accepted without validation (slug format is validated by `validate-style-assets.py`).

- [ ] **Step 2: Test the validator still works with existing content-plan format**

Run: `python skills/deckdone/scripts/validate-content-plan.py --help`
Expected: usage message showing new `--catalog` option (no import errors)

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/scripts/validate-content-plan.py
git commit -m "feat(deckdone): accept Icon/Illustration fields in validate-content-plan.py"
```

---

## Chunk 7: Validation and Final Checks

### Task 14: End-to-end validation

- [ ] **Step 1: Verify all new files exist**

```bash
ls skills/deckdone-style/SKILL.md
ls skills/deckdone-style/references/icon-catalog.md
ls skills/deckdone-style/references/illustration-sources.md
ls skills/deckdone-style/references/enhanced-presets.md
ls skills/deckdone-style/references/decoration-guide.md
ls skills/deckdone-style/references/layout-templates-decorated.md
ls skills/deckdone-style/scripts/fetch-icon.py
ls skills/deckdone-style/scripts/fetch-illustration.py
ls skills/deckdone-style/scripts/validate-style-assets.py
```

Expected: all files present

- [ ] **Step 2: Run fetch-icon.py with a local icon**

Run: `python skills/deckdone-style/scripts/fetch-icon.py trending-up ./tmp/test-deckdone-icons`
Expected: "OK: trending-up.svg (local, N bytes)"

- [ ] **Step 3: Run fetch-icon.py with CDN fallback (icon not in local pack)**

Run: `python skills/deckdone-style/scripts/fetch-icon.py zodiac-gemini ./tmp/test-deckdone-icons`
Expected: Downloads from CDN (exit 0) or "not found" (exit 2) — either is acceptable

- [ ] **Step 4: Run validate-style-assets.py against a test content plan**

Create a minimal test content plan at `./tmp/test-plan.md`:

```markdown
## Slide 1: Test
- Page Type: Cover
- Total Zones: 3
- Pre-render Elements: None
- Visual Narrative Path: Top to bottom

### Zone A: Title
- Type: title
- Content: "Test Title"
- Max Length: 60
- Visual Weight: primary
- Icon: trending-up
- Illustration: business-plan
```

Run: `python skills/deckdone-style/scripts/validate-style-assets.py ./tmp/test-plan.md --catalog skills/deckdone-style/references/icon-catalog.md --icons-dir skills/deckdone-style/references/icons/`
Expected: PASS (exit 0) with icon and illustration references validated

- [ ] **Step 5: Verify SKILL.md line counts**

```bash
python -c "print('deckdone SKILL.md:', sum(1 for _ in open('skills/deckdone/SKILL.md', encoding='utf-8')), 'lines')"
python -c "print('deckdone-style SKILL.md:', sum(1 for _ in open('skills/deckdone-style/SKILL.md', encoding='utf-8')), 'lines')"
```

Expected: deckdone under 600, deckdone-style under 400

- [ ] **Step 6: Verify icon count and size**

```bash
python -c "import os; icons=[f for f in os.listdir('skills/deckdone-style/references/icons') if f.endswith('.svg')]; print(f'{len(icons)} icons')"
python -c "import os; total=sum(os.path.getsize(os.path.join('skills/deckdone-style/references/icons',f)) for f in os.listdir('skills/deckdone-style/references/icons') if f.endswith('.svg')); print(f'{total/1024:.0f} KB total')"
```

Expected: 150-200 icons, 300-800 KB

- [ ] **Step 7: Final commit (if any uncommitted changes)**

```bash
git add -A
git status
# Only commit if there are actual changes
```
