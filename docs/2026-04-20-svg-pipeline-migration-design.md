# DeckDone SVG Pipeline Migration — Design Spec

> **Goal:** Replace DeckDone's HTML→html2pptx pipeline (Steps 9–12) with an SVG→DrawingML pipeline, achieving visual quality comparable to PPT Master.

> **Architecture:** Fork PPT Master's `svg_to_pptx` converter (fix known bugs), adopt their SVG constraint docs as DeckDone references, rewrite `layout-templates.md` from HTML to SVG format. Steps 1–8 (Discovery → Content) remain unchanged.

> **Tech Stack:** Python + python-pptx + stdlib xml.etree.ElementTree (zero new runtime dependencies)

---

## 1. What Changes, What Stays

### Unchanged (Steps 1–8, ~76% of codebase)

| File | Why it stays |
|------|-------------|
| SKILL.md Steps 1–8 | Discovery, Design, Content phases have zero HTML dependency |
| density-presets.md | Pure content-capacity data |
| layout-skeleton-format.md | ASCII wireframe format is rendering-agnostic |
| layout-types.md | Page type catalog, zone ratios — abstract definitions |
| narrative-frameworks.md | Story structure, nothing visual |
| style-presets.md | Color palettes, typography — format-independent |
| quality-checklist.md (Steps 1–8 checks) | Format-agnostic |
| validate-content-plan.py | Validates markdown, no HTML dependency |
| presentation-guide-template.md | Text template |

### Rewritten

| File | Current → New | Scope |
|------|--------------|-------|
| `SKILL.md` Steps 9–12 | HTML generation → SVG generation | ~90 lines rewritten |
| `layout-templates.md` | 15 HTML templates → SVG templates | Full rewrite (~500 lines) |
| `validate-html-slides.py` | HTML validator → `validate-svg-slides.py` | Full rewrite (~250 lines) |
| `quality-checklist.md` Steps 9–11 | "HTML" → "SVG" terminology | Minor edits |

### New Files (forked from PPT Master)

| File | Source | Lines | Notes |
|------|--------|-------|-------|
| `scripts/svg_to_pptx/` (package, 13 files) | PPT Master | ~3,058 | Core converter, with bug fixes |
| `references/svg-constraints.md` | Derived from PPT Master's shared-standards.md | ~150 | SVG generation rules for AI |
| `references/svg-canvas-formats.md` | Derived from PPT Master | ~30 | viewBox, dimensions, coordinate system |

### New Files (template assets, copied from PPT Master)

| Directory | Contents | Notes |
|-----------|----------|-------|
| `templates/charts/` | 52 SVG visualization templates + charts_index.json | MIT, PPT Master original |
| `templates/icons/tabler-filled/` | 1,053 SVG icons | MIT, from tabler/icons project |
| `templates/icons/tabler-outline/` | 5,039 SVG icons | MIT, from tabler/icons project |
| `templates/layouts/exhibit/` | 5 SVG + design_spec.md | General-purpose layout |
| `templates/layouts/smart_red/` | 5 SVG + design_spec.md | General-purpose layout |
| `templates/layouts/科技蓝商务/` | 5 SVG + design_spec.md | General-purpose layout |

---

## 2. Bug Fixes in Forked Converter

5 critical bugs to fix in the copied `svg_to_pptx/` code:

| # | Bug | File | Fix |
|---|-----|------|-----|
| 1 | polygon/polyline ignore `transform="translate()"` | drawingml_elements.py:529,583 | Extract element's own translate and add to ctx.translate_x/y |
| 2 | Shadow direction angle wrong for negative dx | drawingml_styles.py:427 | Remove `max(dx, 0.001)`, use raw dx in atan2 |
| 3 | letter-spacing unit conversion 33% too large | drawingml_elements.py:791 | Change `* 100` to `* 75` (1px = 0.75pt = 75 hundredths-of-pt) |
| 4 | `<rect rx/ry>` rounded corners not converted | drawingml_elements.py:88 | Map to `prstGeom roundRect` with adj values (same logic as clipPath handler at line 978) |
| 5 | Hardcoded `lang="zh-CN"` on all text | drawingml_elements.py:723 | Detect language from text content, default to `lang="en-US"` for non-CJK |

---

## 3. SVG Constraints Document (New Reference)

`references/svg-constraints.md` — the rules AI must follow when generating SVG slides.

Derived from PPT Master's `shared-standards.md` but adapted for DeckDone's workflow:

### Canvas Rules
- viewBox: `0 0 1280 720`, width/height must match
- All elements absolute-positioned (no CSS layout, no flexbox)
- Backgrounds via `<rect>` elements

### Banned Features (DrawingML incompatible)
- `<mask>`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`
- `@font-face`, `<animate*>`, `<script>`, `<iframe>`
- `<symbol>` + `<use>` (but `<use data-icon="...">` is allowed for icon embedding)
- `rgba()` — use hex + `fill-opacity`/`stroke-opacity` separately
- `<g opacity="...">` — set opacity per child element
- CSS `linear-gradient()`/`radial-gradient()` — use SVG `<defs>` gradients only

### Text Rules
- No multi-line `<tspan>` — use separate `<text>` elements per line
- Font-family: web-safe fonts only (Arial, Georgia, Verdana, Tahoma, Trebuchet MS, Times New Roman, Courier New, Impact)
- No `<rect rx="...">` — write `<path>` with arc commands for rounded rectangles
- `preserveAspectRatio` on `<image>` — use "xMidYMid meet" only, never "slice"
- All images must be self-contained (base64 data URIs or local file references)

### Icon Usage
- Use `<use data-icon="tabler-filled/name" .../>` or `<use data-icon="tabler-outline/name" .../>` syntax
- One icon library per presentation (never mix filled and outline)
- icons are resolved at build time by `embed_icons.py`

### Structural Rules
- Every SVG must have a `<defs>` block for gradients/filters before first visual element
- Elements grouped by visual section using `<g>` tags with descriptive comments
- Letter-spacing: bare number values only (SVG px units)

---

## 4. SVG Template Format (Rewritten layout-templates.md)

Each page type gets an SVG template instead of HTML. Example — Cover page:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <!-- Gradients and filters defined here -->
  </defs>

  <!-- Background -->
  <rect width="1280" height="720" fill="{{BG_COLOR}}" />

  <!-- Decorative elements -->
  <rect x="60" y="62" width="80" height="3" fill="{{ACCENT_COLOR}}" rx="1.5" ry="1.5" />

  <!-- Title area -->
  <text x="640" y="300" font-family="Arial, sans-serif" font-size="56" font-weight="bold"
        fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{TITLE}}</text>

  <!-- Subtitle area -->
  <text x="640" y="365" font-family="Arial, sans-serif" font-size="26"
        fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{SUBTITLE}}</text>

  <!-- Footer -->
  <text x="60" y="680" font-family="Arial, sans-serif" font-size="14"
        fill="{{TEXT_TERTIARY}}">{{DATE}} · {{AUTHOR}}</text>
</svg>
```

Key differences from HTML templates:
- **No CSS flexbox** — all positions are absolute x,y coordinates
- **No pre-render pipeline** — gradients are native SVG `<linearGradient>`, icons are `<use data-icon="...">` placeholders
- **`{{PLACEHOLDER}}` syntax** — consistent with PPT Master's template convention
- **Style tokens** — `{{BG_COLOR}}`, `{{ACCENT_COLOR}}` etc. replaced from style-guide.md at generation time

### Page Types → SVG Templates

| # | Page Type | SVG Template Key Features |
|---|-----------|--------------------------|
| 1 | Cover | Full-bleed background, centered title, accent line, footer |
| 2 | Agenda | Two-column layout, numbered items, section indicators |
| 3 | Section Divider | Large chapter number + title, accent bar, minimal decoration |
| 4 | Content-Text | Top accent bar, title zone, body text as separate `<text>` elements |
| 5 | Content-TwoCol | Dividing line, two independent column groups |
| 6 | Data-Chart | Title + `<use data-icon>` chart placeholder + interpretation text |
| 7 | Quote | Serif font, centered, decorative quotation marks via `<path>` |
| 8 | Timeline | Horizontal node sequence with connecting `<line>` elements |
| 9 | Comparison | Header row + criteria rows, accent color per side |
| 10 | Closing | Centered takeaway + CTA + contact info |
| 11 | Composite-Diagram | Multi-layer nested `<rect>` groups with labels |
| 12 | Pipeline-Flow | Stage boxes with `<line>` arrow connectors + `<marker>` arrowheads |

---

## 5. New Pipeline: Steps 9–12

### Step 9: Test Generation (SVG)

**Inputs:** content-plan.md, style-guide.md, layout-skeleton.md, svg-constraints.md

**AI Behavior:**
1. Select 1 page per layout type as test samples
2. For each test page:
   a. Read the SVG template from layout-templates.md for the page type
   b. Replace `{{PLACEHOLDER}}` tokens with actual content from content-plan.md
   c. Replace `{{STYLE_TOKEN}}` values from style-guide.md
   d. Generate SVG file — AI writes the SVG directly, constrained by svg-constraints.md
   e. Run `python scripts/svg_to_pptx/svg_to_pptx.py . -s test-slides -o test-slides/output.pptx`
3. User reviews the PPTX (or exported thumbnails) for layout accuracy, text readability, visual quality
4. If unsatisfied, adjust SVG and regenerate (max 3 rounds per page)

**Deliverable:** `test-slides/` directory with SVG files + `test-slides/output.pptx`

**Gate:** User confirms all test page visuals.

### Step 10: Batch Generation (SVG)

**AI Behavior:**
1. Process in section chunks (5–8 pages per chunk) to avoid context overflow
2. **Lock design context** before generating: document global color tokens, font scale, spacing constants, decoration patterns. This context is passed to every chunk.
3. Generate **page by page sequentially** within each chunk — never batch-generate multiple SVGs at once
4. Per page:
   a. Generate SVG constrained by svg-constraints.md and locked design context
   b. Save to `svg_output/` directory
5. After all SVGs generated, run conversion:
   ```
   python scripts/svg_to_pptx/svg_to_pptx.py . -s output -o output.pptx
   ```

**Deliverable:** `svg_output/` + `output.pptx`

**Validation:** Run `python scripts/validate-svg-slides.py svg_output/`

### Step 11: Final Quality Review

Same logic as current Step 11 but checks SVG source instead of HTML:
- Consistency: all SVGs use same color tokens and font scale
- Completeness: every page from outline.md has a corresponding SVG
- SVG compliance: run validate-svg-slides.py on all files
- Fix problem pages and regenerate

**Deliverable:** `final.pptx`

### Step 12: Presentation Guide

Unchanged from current Step 12.

---

## 6. validate-svg-slides.py (New Script)

Replaces `validate-html-slides.py`. Checks:

1. **Canvas format:** `viewBox="0 0 1280 720"` present, width/height match
2. **No banned elements:** `<mask>`, `<style>`, `class`, `<foreignObject>`, `<animate*>`, `<script>`
3. **No banned attributes:** `rgba()`, `<g opacity>`, CSS gradients
4. **Font check:** only web-safe fonts in font-family attributes
5. **Text structure:** no multi-line `<tspan>` with `y` or `dy` attributes
6. **No `<rect rx>`:** rounded rects must be `<path>` elements
7. **Image references:** all `<image href>` are base64 data URIs or existing local files
8. **Icon references:** `<use data-icon="...">` references must match `tabler-filled/*` or `tabler-outline/*` prefix
9. **Completeness:** SVG file count matches outline.md page count
10. **Non-empty:** each SVG has at least 3 text elements or visual elements

Exit 0 on pass, 1 on any failure. Python stdlib only.

---

## 7. File Structure After Migration

```
skills/deckdone/
  SKILL.md                           # Modified: Steps 9-12 rewritten
  references/
    svg-constraints.md               # NEW: SVG generation rules
    svg-canvas-formats.md            # NEW: viewBox, dimensions
    layout-templates.md              # REWRITTEN: HTML → SVG templates
    layout-types.md                  # Minor edit: remove html2pptx constraints section
    layout-skeleton-format.md        # Unchanged
    style-presets.md                 # Minor edit: remove Sharp pre-render references
    density-presets.md               # Unchanged
    narrative-frameworks.md          # Unchanged
    quality-checklist.md             # Minor edit: Steps 9-11 terminology
    dependencies.md                  # Updated: remove html2pptx deps, add python-pptx
    presentation-guide-template.md   # Unchanged
    audience-analysis.md             # Unchanged
    state-templates.md               # Unchanged
  scripts/
    validate-svg-slides.py           # NEW: replaces validate-html-slides.py
    validate-content-plan.py         # Unchanged
    svg_to_pptx/                     # NEW: forked from PPT Master (with bug fixes)
      __init__.py
      drawingml_converter.py
      drawingml_context.py
      drawingml_elements.py
      drawingml_paths.py
      drawingml_styles.py
      drawingml_utils.py
      pptx_builder.py
      pptx_cli.py
      pptx_dimensions.py
      pptx_discovery.py
      pptx_media.py
      pptx_notes.py
      pptx_slide_xml.py
    svg_to_pptx.py                   # NEW: thin CLI wrapper
  templates/                         # NEW: copied from PPT Master
    charts/                          # 52 SVG visualization templates
    icons/
      tabler-filled/                 # 1,053 icons
      tabler-outline/                # 5,039 icons
    layouts/
      exhibit/                       # General-purpose
      smart_red/                     # General-purpose
      科技蓝商务/                     # General-purpose
```

---

## 8. Dependencies After Migration

### Removed
- html2pptx.js (Playwright + Sharp + PptxGenJS pipeline)
- Node.js runtime requirement for slide generation

### Added
- python-pptx (already installed)
- svg_to_pptx package (stdlib only, no new pip dependencies)

### Net Effect
- **Simpler dependency graph** — pure Python, no Node.js runtime needed for slide generation
- DeckDone still depends on the `pptx` skill for reading/analyzing existing PPTX files, but no longer for HTML→PPTX conversion

---

## 9. Migration Checklist

| # | Task | Type |
|---|------|------|
| 1 | Copy `svg_to_pptx/` package from PPT Master | Fork |
| 2 | Fix 5 confirmed bugs in converter | Fix |
| 3 | Copy template assets (charts, icons, layouts) | Copy |
| 4 | Write `references/svg-constraints.md` | New |
| 5 | Write `references/svg-canvas-formats.md` | New |
| 6 | Rewrite `references/layout-templates.md` (HTML → SVG) | Rewrite |
| 7 | Write `scripts/validate-svg-slides.py` | New |
| 8 | Modify `scripts/svg_to_pptx.py` CLI wrapper | New |
| 9 | Update `references/layout-types.md` (remove html2pptx section) | Edit |
| 10 | Update `references/style-presets.md` (remove Sharp references) | Edit |
| 11 | Update `references/quality-checklist.md` (Steps 9-11 terminology) | Edit |
| 12 | Update `references/dependencies.md` | Edit |
| 13 | Rewrite SKILL.md Steps 9-12 | Rewrite |
| 14 | Add PPT Master MIT license attribution file | Legal |
| 15 | Add tabler icons MIT license attribution file | Legal |
| 16 | Iterative test: generate sample deck, validate quality | Test |
