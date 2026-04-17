# Design: deckdone-style Skill

> Date: 2026-04-17
> Status: Draft
> Author: AI + gxlei

## Problem

Generated presentations have four visual quality issues:
1. **Too few icons** — slides look like plain text; missing icons next to titles, bullets, flow nodes
2. **Missing decorative illustrations** — cover slides and section dividers lack visual richness
3. **Color/typography not refined** — the 18 style presets lack decoration nuance and design sophistication
4. **Overall lack of design sense** — output looks AI-generated, not professional

The current `deckdone` skill (SKILL.md 557 lines, references ~2,400 lines) handles workflow orchestration well but has no visual resource strategy. All style/visual content lives in `references/style-presets.md` (445 lines) which only defines flat color palettes — no icon guidance, no illustration placement rules, no decoration system.

## Decision

Split visual resources and style enhancement into a new **`deckdone-style`** skill. The parent `deckdone` skill retains workflow orchestration; `deckdone-style` owns icon catalog, illustration sources, enhanced presets, and decoration rules.

**Resource strategy**: Curated icons (~200 SVGs, ~500KB) bundled locally in `references/icons/`; illustrations fetched online from unDraw at generation time.

**Skill detection**: deckdone checks for deckdone-style at the point of use (following existing pattern from SKILL.md:66-71). Detection: attempt to read `references/enhanced-presets.md` from the deckdone-style skill path. If readable, skill is available. If not, degrade to existing `style-presets.md`.

**Harness improvement principle**: This skill adopts the same harness improvement principle from deckdone. When a generated slide has icon/illustration quality issues, the fix targets the catalog (`icon-catalog.md`), guide (`decoration-guide.md`), or templates (`layout-templates-decorated.md`) — not the individual slide. Every visual failure is logged in the shared `harness-improvements.md`.

## Architecture

```
skills/
  deckdone/                          ← existing (modified)
    SKILL.md                         ← Step 6/7/9 call deckdone-style
    references/
      style-presets.md               ← RETAINED as fallback (no deckdone-style)
      layout-types.md                ← unchanged
      layout-templates.md            ← unchanged
      layout-skeleton-format.md      ← unchanged
      density-presets.md             ← unchanged
      quality-checklist.md           ← updated with icon/illustration checks
      state-templates.md             ← unchanged
      audience-analysis.md           ← unchanged
      narrative-frameworks.md        ← unchanged

  deckdone-style/                    ← NEW skill
    SKILL.md                         ← entry point (~350-400 lines)
    references/
      icons/                         ← ~200 curated Tabler SVGs (~500KB)
      icon-catalog.md                ← semantic mapping: scenario → icon name
      illustration-sources.md        ← unDraw URL templates, usage guide, color customization
      enhanced-presets.md            ← improved style presets replacing style-presets.md
      decoration-guide.md            ← per-page-type decoration rules
      layout-templates-decorated.md  ← icon/illustration-augmented HTML templates (extends deckdone's layout-templates.md)
    scripts/
      fetch-icon.py                  ← download single SVG from CDN (fallback for non-curated icons)
      fetch-illustration.py          ← fetch unDraw illustration with custom color
      validate-style-assets.py       ← validate icon/illustration references in content-plan.md
```

## Components

### 1. references/icons/ — Curated Icon Pack

~200 SVG files from Tabler Icons (MIT license). Selected by PPT relevance.

Categories and counts (approximate):

| Category | Count | Example icons |
|----------|-------|---------------|
| Growth & Metrics | 20 | trending-up, chart-bar, chart-line, arrow-up-right, target, gauge, report-analytics |
| People & Team | 15 | users, user-plus, handshake, brain, heart, eye, users-group |
| Technology | 20 | code, server, database, cloud, cpu, wifi, robot, terminal |
| Process & Flow | 20 | arrows-transfer-up, refresh, settings, list-check, clock, checklist, timeline |
| Communication | 15 | mail, message, presentation, speakerphone, news, megaphone |
| Finance | 10 | coin, currency-dollar, receipt, wallet, piggy-bank, chart-pie |
| Status & Actions | 20 | check, x, alert-triangle, info-circle, plus, minus, download, upload |
| Navigation & Layout | 15 | chevron-right, arrow-right, external-link, layout, grid, list |
| Nature & Abstract | 15 | leaf, sun, sparkles, stars, rocket, flag, flame, bolt |
| Objects | 20 | book, briefcase, calendar, folder, lock, shield, tool, pencil |
| Arrows & Connectors | 15 | arrow-right, arrow-down, corner-down-right, transform |
| People (roles) | 15 | user, users, man, woman, baby, school, nurse, doctor |

Total: ~200 icons. Each SVG is 1-3KB. Total size ~500KB.

### 2. references/icon-catalog.md

Semantic mapping table. AI reads this during content-plan (Step 7) to select appropriate icons.

```markdown
## Semantic → Icon Mapping

### By Content Theme
- growth/revenue → trending-up
- strategy/plan → target
- team/collaboration → users-group
- technology/IT → code
- data/analytics → chart-bar
- communication → message
- finance/budget → coin
- process/workflow → list-check
- timeline/roadmap → clock
- security/risk → shield
- innovation → rocket
- success/achievement → trophy
- problem/challenge → alert-triangle
- learning/education → school

### By Page Zone
- Title area → 32-48pt icon matching section theme
- Bullet points → 16pt icon per major bullet (optional)
- Timeline nodes → 24pt circular icon
- Pipeline stages → 32pt icon per stage
- Comparison headers → 24pt icon per side
```

### 3. references/illustration-sources.md

```markdown
## unDraw (Primary)

- License: Custom (free, no attribution required)
- URL pattern: https://undraw.co/illustrations/{keyword}
- API: https://undraw.co/api/illustration/{slug} → returns SVG URL
- Color customization: Replace #6C63FF in SVG with accent color
- Best for: Cover slides, section dividers, empty area fill
- Usage: fetch-illustration.py handles download and color swap

## Recommended Illustrations by Section Type

| Section Theme | unDraw illustration slug |
|---------------|-------------------------|
| Business/Strategy | business-plan, strategy, growth |
| Technology | developer-activity, coding, server |
| Team/People | team-spirit, collaboration, meeting |
| Data/Analytics | data-analysis, statistics, metrics |
| Success/Goals | finish-line, achiever, winner |
| Innovation | innovative, creative, brainstorming |
| Finance | investment, savings, finance |
| Communication | messaging, presentation, connecting |

## Access Notes
- unDraw is accessible from China mainland (tested)
- If unDraw unavailable, degrade to geometric patterns using CSS shapes + accent color
```

### 4. references/enhanced-presets.md

Based on the existing 18 presets, each enhanced with:

- **Icon placement rules**: Which zones get icons and at what size
- **Illustration zones**: Cover/divider pages define a reserved area (15-25% of slide) for illustrations
- **Decoration system**: Background patterns, corner ornaments, divider styles
- **Gradient backgrounds**: Which presets need Sharp-rasterized gradients
- **Improved typography scale**: More refined sizing with optical adjustments
- **Decorative elements catalog**: Lines, dots, geometric shapes per style personality

Each preset now has these additional sections:

```markdown
## [Preset Name]

### Palette
(existing 5 colors)

### Typography
(existing + refined scale)

### Icon Style
- Stroke width: 1.5px (matches Tabler default)
- Color: primary for titles, secondary for bullets, accent for highlights
- Size: 32pt title, 24pt section, 16pt bullet

### Illustration Zone
- Cover: right 25% area, 120pt max height
- Section Divider: bottom 20% area, 80pt max height
- Other types: none

### Decoration
- Header: 2px accent underline, 48pt wide
- Body: no decoration
- Footer: subtle dot pattern in background tint
- Corner: none
```

### 5. references/decoration-guide.md

Per-page-type rules for where to place icons, illustrations, and decorative elements:

```markdown
## Cover
- [REQUIRED] Right or bottom 25% area: illustration (unDraw)
- [REQUIRED] Title left: 48pt icon matching presentation theme
- [OPTIONAL] Background: gradient or geometric pattern

## Section Divider
- [REQUIRED] Title left: 40pt icon reflecting section theme
- [RECOMMENDED] Bottom 20%: illustration or decorative pattern
- [OPTIONAL] Background: subtle accent tint

## Content-Text
- [RECOMMENDED] Each H2 bullet: 16pt icon prefix
- [OPTIONAL] Title underline: 2px accent line, 48pt wide

## Content-TwoCol
- [RECOMMENDED] Each column header: 24pt icon
- [OPTIONAL] Divider line between columns

## Data-Chart
- [REQUIRED] Chart rendered as PNG (existing)
- [RECOMMENDED] Interpretation area: 16pt insight icon

## Timeline
- [REQUIRED] Each node: 24pt circular icon replacing text marker
- [RECOMMENDED] Connecting line: 2px primary color

## Comparison
- [RECOMMENDED] Each side header: 24pt icon
- [RECOMMENDED] Checkmark/x-mark icons for boolean comparisons

## Pipeline-Flow
- [REQUIRED] Each stage top: 32pt icon
- [REQUIRED] Arrows: SVG arrow style (not plain →)

## Composite-Diagram
- [RECOMMENDED] Subsystem headers: 20pt icon
- [OPTIONAL] Background tint per layer
```

### 5b. references/layout-templates-decorated.md

Extended HTML templates that add icon and illustration slots to the original `layout-templates.md`. These are the canonical "decorated" versions — Phase 4 uses these instead of the originals when deckdone-style is available.

Key differences from original templates:

| Template | Added Elements |
|----------|---------------|
| Cover | `<img>` slot for illustration in right 25%; `<img>` for theme icon at 48pt left of title |
| Section Divider | `<img>` for section icon at 40pt left of title; optional illustration area bottom 20% |
| Timeline | `<img>` per event node replacing text markers; 24pt circular crop |
| Pipeline-Flow | `<img>` per stage top at 32pt; SVG arrow connectors replacing `→` text |
| Content-Text | Optional `<img>` before each `<li>` at 16pt |
| Content-TwoCol | `<img>` before each column heading at 24pt |
| Comparison | `<img>` before each header at 24pt; ✓/✗ icons for boolean rows |
| Composite-Diagram | `<img>` before subsystem labels at 20pt |

These templates are deterministic — every `<img>` has a fixed position and size. The AI fills in the `src` attribute from the content plan's icon/illustration fields. No creative decisions required in Step 9/10.

**Maintenance model**: `layout-templates-decorated.md` is a standalone file containing full HTML templates (not deltas). When the original `layout-templates.md` is updated, the decorated version must be synced. To reduce drift risk, the decorated templates are organized with clear markers like `<!-- DECKDONE-STYLE: icon slot -->` at every insertion point so diffs are easy to spot.

### 6. scripts/fetch-icon.py

```python
# Input: icon_name (str), output_dir (str), size (int, default 48)
# Behavior:
#   1. Check local references/icons/{icon_name}.svg first
#   2. If not found, download from jsdelivr CDN:
#      https://cdn.jsdelivr.net/npm/@tabler/icons@3.41.1/icons/outline/{icon_name}.svg
#      (pinned version; update version constant when upgrading icon pack)
#   3. If sharp available: convert to PNG at specified size via subprocess
#      sharp invocation: node -e "require('sharp')(stdin).resize(size,size).png().toFile(outfile)"
#   4. Output: {output_dir}/{icon_name}.png or .svg
# Exit codes: 0=success, 1=failure, 2=not-found-locally-or-online
# No third-party Python deps (uses subprocess for sharp, urllib for download)
```

### 7. scripts/fetch-illustration.py

```python
# Input: illustration_slug (str), accent_color (hex), output_dir (str)
# Behavior:
#   1. Fetch SVG from unDraw:
#      GET https://undraw.co/api/illustration/{slug}
#      Expected response: JSON with "url" field pointing to SVG
#      If API returns error or unexpected format, exit 1 with descriptive message
#   2. Download SVG content from the URL
#   3. Replace default color:
#      - Case-insensitive regex: #6C63FF and #6c63ff → accent_color
#      - If neither found: replace the most frequent hex color in the SVG (heuristic)
#      - Log warning if using heuristic fallback
#   4. If sharp available: convert to PNG via subprocess
#   5. Output: {output_dir}/{slug}.png or .svg
# Exit codes: 0=success, 1=fetch-failure, 2=color-replace-warning
# No third-party Python deps
```

### 8. scripts/validate-style-assets.py

Validates that all icon/illustration references in content-plan.md resolve to actual assets.

```python
# Input: content-plan.md path, icon-catalog path, icons-dir path
# Checks:
#   1. Every "- Icon:" field references a name that exists in icon-catalog.md
#   2. Every icon name in catalog has a corresponding .svg in icons-dir
#   3. Every SVG in icons-dir is well-formed XML with <svg> root element
#   4. Every "- Illustration:" field is either "None" or a valid unDraw slug format
# Exit: 0 on pass, 1 on any failure
# No third-party deps
```

## Changes to Existing deckdone Skill

### SKILL.md Modifications

1. **Dependencies section**: Add `deckdone-style` as Optional dependency
   - Degradation: fall back to existing `style-presets.md`, no icons, no illustrations

2. **Step 6 (Visual Style Direction)**:
   - Add: "If deckdone-style skill is available, read `references/enhanced-presets.md` instead of `references/style-presets.md`"
   - Add: "Read `references/decoration-guide.md` for per-page-type decoration rules"

3. **Step 7 (Detailed Content Plan)**:
   - Add: "Read `references/icon-catalog.md` from deckdone-style. For each zone of type 'icon', select an appropriate icon name from the catalog."
   - Add icon field to zone spec: `- Icon: [name from catalog or "None"]`
   - Add illustration field to cover/divider pages: `- Illustration: [unDraw slug or "None"]`

4. **Step 9 (Test Generation)**:
   - Add: "Run `fetch-icon.py` to download and rasterize icons"
   - Add: "Run `fetch-illustration.py` to fetch cover/divider illustrations"
   - Add: "Place icons in HTML per decoration-guide.md rules"

5. **Step 10 (Batch Generation)**:
   - Same icon/illustration fetch steps as Step 9

### quality-checklist.md Updates

Add to Step 7 validation:
- [ ] Every page that requires icons (per decoration-guide.md) has icon names assigned
- [ ] Cover and Section Divider pages have illustration slugs or explicit "None"

Add to Step 9 validation:
- [ ] All assigned icons are present as files in the test-slides directory
- [ ] Cover/divider illustrations render correctly (not broken image)
- [ ] Icon colors match the style guide palette

### validate-content-plan.py Updates

The existing `validate-content-plan.py` in deckdone must be updated to:
- Accept `- Icon:` and `- Illustration:` as valid optional zone fields (not reject them as unknown)
- When deckdone-style is available: validate that icon names exist in the catalog

### SKILL.md Line Budget

Current SKILL.md: 557 lines. AGENTS.md cap: ~600 lines. Available: ~43 lines.

Planned additions to SKILL.md:
- Dependencies table: +2 lines (deckdone-style entry)
- Step 6: +3 lines (conditional read instruction)
- Step 7: +4 lines (icon/illustration fields)
- Step 9: +5 lines (fetch-icon/fetch-illustration calls)
- Step 10: +3 lines (same fetch steps)
- Total: ~17 lines added → 574 lines (under cap)

If further additions are needed, move content to a new `references/style-integration.md` file that SKILL.md cross-references.

## Dependency Graph

```
deckdone
  ├── pptx skill (required)
  ├── deckdone-style skill (optional, enhances visuals)
  │     └── references/icons/ (bundled, offline)
  │     └── unDraw (online, for illustrations)
  ├── theme-factory skill (optional, additional presets)
  ├── pdf/docx/xlsx skills (optional, material extraction)
  └── sharp (optional, SVG→PNG rasterization)
```

## Graceful Degradation

| Component Missing | Behavior |
|-------------------|----------|
| deckdone-style skill entirely | Use existing style-presets.md, no icons, no illustrations |
| unDraw unreachable | No illustrations, geometric CSS patterns as fallback |
| sharp unavailable | SVG icons used directly via `<img src="icon.svg">` in HTML. Sharp is required by parent deckdone (SKILL.md:42), so this row only applies if deckdone's own sharp dependency is later relaxed. |
| fetch-icon.py fails | AI reads the SVG file content from `references/icons/` and inlines it as `<svg>` in the HTML template |
| Local icons/ missing | fetch-icon.py downloads from jsdelivr CDN |
| Both local icons AND CDN unreachable | fetch-icon.py exits 1 with error message. AI falls back to text-based markers (unicode symbols: ▶ ● ◆ → etc.) matching the icon catalog's semantic mapping |
| unDraw default color changes | fetch-illustration.py does case-insensitive regex replacement of both `#6C63FF` and `#6c63ff`. If neither found in SVG, replaces the most frequent color (heuristic). Logs a warning. |

## Estimated Sizes

| Component | Size |
|-----------|------|
| deckdone-style SKILL.md | ~80-100 lines (thin entry point, details in references) |
| references/icon-catalog.md | ~100 lines |
| references/illustration-sources.md | ~80 lines |
| references/enhanced-presets.md | ~600 lines (expanded from 445) |
| references/decoration-guide.md | ~120 lines |
| references/layout-templates-decorated.md | ~650 lines (extended from 565 original) |
| references/icons/ (200 SVGs) | ~500KB |
| scripts/fetch-icon.py | ~80 lines |
| scripts/fetch-illustration.py | ~80 lines |
| scripts/validate-style-assets.py | ~60 lines |
| **Total new content** | ~2,200 lines + 500KB icons |

## Success Criteria

1. Every generated slide has at least 1 icon (except Quote type)
2. Cover and Section Divider slides have a themed illustration
3. Pipeline-Flow stages have distinct icons per stage
4. Timeline nodes use circular icon markers instead of text
5. Visual consistency — all decorations follow the selected preset's personality
6. No broken image placeholders in any generated slide
7. All icon/illustration references pass `validate-style-assets.py` validation

## SKILL.md Frontmatter

```yaml
---
name: deckdone-style
description: "Visual resource and style enhancement skill for DeckDone. Provides curated icon catalog, illustration sources (unDraw), enhanced style presets, and per-page-type decoration rules. Use alongside the deckdone skill to add icons, illustrations, and refined visual styling to generated presentations."
---
```

## Icon Pack Curation Criteria

Icons are selected using these rules:
1. Every icon must have at least 1 semantic mapping in `icon-catalog.md` (no orphan icons)
2. Priority: icons with multiple semantic mappings (e.g., `chart-bar` → data/analytics AND finance/report)
3. Coverage: at least 3 icons per category listed in the catalog
4. Excluded: brand logos, duplicate variants (use outline only), icons >3KB SVG size
5. All icons are from Tabler Icons outline set (MIT license, consistent 24×24 2px stroke grid)
