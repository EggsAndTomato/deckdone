---
name: deckdone-build
description: "Convert presentation content plans into high-quality PPTX files. Starts with visual style selection and test page generation, then batch-generates all slides via SVG→DrawingML pipeline. Takes markdown deliverables from deckdone-plan (content-plan, layout-skeleton, outline) and generates SVG slides, then converts to native PPTX shapes. Use when the user has a completed content plan and wants to produce the final PPT."
---

# DeckDone Build Skill

Convert presentation content plans into production-quality PPTX files. This skill handles **visual style selection** and **SVG generation + PPTX export**.

## Input Files

Required deliverables (from deckdone-plan):

| File | Source Step | Purpose |
|------|-----------|---------|
| `content-plan.md` | Step 5 | Per-page content, zones, visual narrative |
| `layout-skeleton.md` | Step 5 | Page-level layout assignments |
| `outline.md` | Step 3 | Section structure, page count |

Optional: `layout-system.md` (Step 4), `brief.md` (Step 1).

## Workflow

| Step | Goal |
|------|------|
| 6 | Visual style selection + test page generation |
| 7 | Batch SVG generation + quality review |
| 8 | Final export + presentation guide |

---

## Execution Discipline (MANDATORY)

> The following rules have the highest priority — violating any one constitutes execution failure:

1. **SERIAL EXECUTION** — Steps 6→7→8 in order. Each step's output is the next step's input.
2. **SUB-AGENT DELEGATION** — Delegate context-heavy generation (SVG code, presentation guide text) to sub-agents. The main agent orchestrates and handles user interaction only. See `references/sub-agent-protocols.md` for prompt templates and delegation patterns.
3. **LOCK DESIGN CONTEXT** — Before Step 7, extract and lock global tokens (colors, font scale, spacing, decoration patterns). Paste the FULL locked context into every sub-agent prompt — this is critical for style consistency.
4. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require full stop. Wait for explicit user confirmation before proceeding.
5. **NO SPECULATIVE EXECUTION** — Do not pre-write SVG code during earlier steps.
6. **READ CONSTRAINTS FIRST** — Read `references/svg-constraints.md` before starting Step 6.
7. **PARALLEL BATCHES** — In Step 7, split pages into batches of 3-5 and delegate to parallel sub-agents (max 6 concurrent). Each sub-agent generates its batch independently.

---

## Step 6: Visual Style + Test Generation

⛔ **BLOCKING** — User must confirm visual style and test results before proceeding.

**Prerequisites:** All input files from deckdone-plan present. Read `references/svg-constraints.md`.

**AI Behavior:**

### 6a. Style Selection

1. Read `brief.md` for purpose, audience, and context.
2. Read `references/style-presets.md` (moved from deckdone-plan) for color and typography presets.
3. Recommend 2-3 styles based on presentation purpose + audience profile.
4. Show style previews: color palette + typography + decoration characteristics.
5. User selects a style or fine-tunes parameters.
6. Write `style-guide.md`.

```markdown
# Style Guide
## Palette: [primary/secondary/accent/background/text — hex values]
## Typography: [heading font + body font + size scale]
## Decoration: [border style / shape patterns / background treatment]
## Layout Rules: [margins / spacing / content area ratios]
```

### 6b. Test SVG Generation (delegate to sub-agent)

1. Read `references/sub-agent-protocols.md` for the Step 6b prompt template.
2. From `layout-system.md`, identify all distinct layout types used.
3. Select **one page per layout type** as test samples.
4. Delegate all test SVG generation to a single sub-agent (subagent_type: "general"). Paste the full locked design context from `style-guide.md` into the prompt.
5. After sub-agent completes, run conversion:
   ```bash
   python scripts/svg_to_pptx.py <project-dir> -s svg_output -o test-slides/output.pptx --only native
   ```
6. Present to user for review. Check:
   - Layout accuracy against `layout-skeleton.md`
   - Text cutoff or overflow
   - Color and spacing correctness
   - SVG-to-PPTX conversion fidelity
7. If unsatisfied, adjust and re-delegate (max 3 rounds per page).
8. Lock final template parameters → `template-params.md`.

**Deliverable:** `style-guide.md` + `test-slides/output.pptx` + `template-params.md`

**Gate:** User confirms visual style and all test page visuals.

---

## Step 7: Batch Generation + Quality Review

⛔ **BLOCKING** — Step 6 gate must be passed.

### 7a. Batch SVG Generation (delegate to parallel sub-agents)

1. **Lock design context** — extract from `style-guide.md` and `template-params.md`:
   - Global color tokens (primary, secondary, accent, backgrounds, text levels)
   - Font scale (heading sizes, body size, caption size, line-height)
   - Spacing system (margins, padding, gaps)
   - Decoration patterns (dividers, accent shapes, icon usage)
1.5 **Separate standard and diagram pages:**
   - Scan content-plan.md for pages with Page Type: Content-Diagram.
   - Standard pages → batch SVG generation (existing protocol).
   - Diagram pages → SVG generation via `scripts/diagram_svg.py` (programmatic coordinates, no sub-agent, no AI guessing).
2. **Read `references/sub-agent-protocols.md`** for the Step 7a prompt template and batch splitting logic.
3. **Split pages into batches** for standard SVG generation:
   - Standard pages only (Content-Diagram pages excluded from SVG batches).
   - 3-5 standard pages per sub-agent batch.
   - Total concurrent sub-agents ≤ 6.
4. **Launch all sub-agents in parallel** in a single message (multiple Task tool calls). Each prompt must contain:
   - The FULL locked design context (pasted inline — do not abbreviate)
   - The specific pages assigned to that batch (from `content-plan.md` + `layout-skeleton.md`)
   - File paths to read: `svg-constraints.md`, layout templates, chart templates
   - The per-page-type visual element rules (from this SKILL.md)
5. **Wait for all sub-agents to complete**, then run conversion:
   ```bash
   python scripts/svg_to_pptx.py <project-dir> -s svg_output -o output.pptx --only native
   ```
   6. Run SVG validation on all files:
   ```bash
   python scripts/validate-svg-slides.py svg_output/ [--outline outline.md] [--content-plan content-plan.md]
   ```

#### Per-Page-Type Visual Element Rules (MANDATORY)

Every SVG must contain graphical elements (not just `<text>`). The following rules map each page type to the visual elements it MUST include:

**Data-Chart pages:**
- Read the matching chart template from `templates/charts/` (use `charts_index.json` quickLookup to find the best match by keyword).
- Extract the SVG structure: axes (`<line>`), bars/slices/points (`<rect>`/`<path>`/`<circle>`), gridlines, legend boxes.
- Replace template data with actual values from the content-plan chart zone.
- The chart area MUST contain non-text graphical elements (bars, lines, slices, nodes, etc.) — never render chart data as bullet text.

**Timeline pages:**
- Use `templates/charts/timeline.svg` as structural reference.
- MUST include: a horizontal/vertical timeline line (`<line>`), milestone nodes (`<circle>`), card outlines (`<rect>` or `<path>`), and connector lines.
- Never render timeline events as plain text without visual node+line structure.

**Pipeline-Flow pages:**
- Use `templates/charts/process_flow.svg` or `templates/charts/chevron_process.svg` as structural reference.
- MUST include: stage containers (`<rect>` or `<path>` with rounded corners), arrow connectors between stages (`<line>` with `marker-end` or `<path>`).
- Never render pipeline stages as plain text without shape containers and arrows.

**Comparison pages:**
- MUST include: column/row container outlines (`<rect>` or `<path>`), divider lines (`<line>`), and header background fills.
- Use `templates/charts/comparison_table.svg` or `templates/charts/comparison_columns.svg` as structural reference when the content fits.

**Composite-Diagram pages:**
- MUST include: component boxes (`<rect>` or `<path>`), connector lines/arrows between components, and layer separator lines.
- For Layered Stack sub-pattern: horizontal band backgrounds (`<rect>` with fill) for each layer.
- For Nested-Box sub-pattern: nested rectangles with different border styles.
- Use `charts_index.json` to find matching infographic templates (e.g., `hub_spoke`, `mind_map`, `concentric_circles`, `org_chart`).

**Content-Text / Content-TwoCol pages:**
- MAY include accent shapes (decorative lines, icon placeholders via `<use data-icon="...">`, section dividers).
- These page types have the most freedom, but should not be entirely bare — add at least one visual element beyond text (e.g., a colored sidebar bar, accent line, or icon).

**Cover / Section Divider / Closing pages:**
- Layout template provides visual chrome (background, sidebar, decorations). Ensure these decorative elements are preserved from the template.

#### Diagram Page Rules (Content-Diagram — Programmatic SVG)

Content-Diagram pages use programmatic SVG generation (NOT AI-dynamic, NOT sub-agent):

```python
from diagram_svg import draw_diagram

svg_string = draw_diagram('pyramid', data, style)
with open('svg_output/P05_Pyramid.svg', 'w') as f:
    f.write(svg_string)
```

The generated SVG goes through the same `svg_to_pptx` pipeline as standard pages.

### 7b. Quality Review

1. Generate thumbnail overview of all slides.
2. Check each page against `content-plan.md` and `style-guide.md`:
   - **Consistency** — All pages follow the same style (palette, fonts, spacing).
   - **Completeness** — No missing pages or content zones.
   - **Readability** — Text sizes sufficient, contrast adequate, no overflow.
   - **SVG compliance** — All files pass `validate-svg-slides.py`.
3. Fix problem pages — regenerate individual SVGs as needed.
4. Re-run converter if any SVGs changed:
   ```bash
   python scripts/svg_to_pptx.py <project-dir> -s svg_output -o output.pptx --only native
   ```
 


**Deliverable:** `output.pptx` (standard SVGs converted + SmartArt injected)

---

## Step 8: Final Export + Presentation Guide

⛔ **BLOCKING** — User must confirm presentation guide content.

**AI Behavior:**

### 8a. Final PPTX

1. Verify all SVGs pass validation.
2. Run final conversion:
   ```bash
    python scripts/svg_to_pptx.py <project-dir> -s svg_output -o final.pptx --only native
   ```

### 8b. Presentation Guide (delegate to sub-agent)

1. Read `references/sub-agent-protocols.md` for the Step 8b prompt template.
2. Delegate presentation guide generation to a single sub-agent. The sub-agent reads all confirmed deliverables and writes `presentation-guide.md` following the 5-module template in `references/presentation-guide-template.md`:
   - **Module 1: Overview** — topic, core message, audience, slide count, duration, narrative framework
   - **Module 2: Design Rationale** — narrative logic, section intentions, key design decisions
   - **Module 3: Slide Key Points** — per-slide emphasis levels (★ Key / Normal / ⏭ Skippable), time allocation
   - **Module 4: Speaking Notes** — transition cues, anticipated questions, timing guidance
   - **Module 5: Data Sources** — per-slide data provenance quick reference for speaker Q&A readiness
3. After sub-agent completes, present `presentation-guide.md` to user for confirmation. Allow edits.

**Deliverables:** `final.pptx` + `presentation-guide.md`

**Gate:** User confirms presentation guide content.

---

## Revision Mode (Post-completion Modifications)

After Step 8, the user may request modifications to the finished PPTX. The AI supports targeted revisions without regenerating the entire deck.

### Supported Modification Types

| Type | Approach | Scope |
|------|----------|-------|
| Change text on a page | Edit SVG `<text>` elements, re-convert | Single page |
| Change layout of a page | Regenerate that page's SVG | Single page |
| Change global colors | Update `style-guide.md`, regenerate all SVGs | All pages |
| Add/remove pages | Update outline, generate/delete SVGs, renumber | Adjacent pages |
| Adjust chart data | Edit SVG chart elements | Single page |

### Revision Workflow

1. User describes the desired change.
2. AI reads `page-index.md` (if available) or scans `svg_output/` to locate target pages.
3. AI reads the relevant SVG file(s) + `content-plan.md` + `style-guide.md`.
4. AI makes targeted edits to SVG(s).
5. Re-run converter:
   ```bash
    python scripts/svg_to_pptx.py <project-dir> -s svg_output -o final-revised.pptx --only native
   ```
6. Present revised PPTX to user.

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/svg_to_pptx/` | SVG→DrawingML converter package (forked from PPT Master) |
| `scripts/svg_to_pptx.py` | CLI wrapper for the converter |
| `scripts/validate-svg-slides.py` | SVG compliance validator (checks constraints from svg-constraints.md) |
| `scripts/embed_icons.py` | Resolve `<use data-icon>` placeholders with actual SVG icon paths |
| `scripts/embed_images.py` | Convert image file references to base64 data URIs |
| `scripts/diagram_svg.py` | Programmatic SVG generator (14 types) for Content-Diagram pages |

## Template Assets

| Asset | Path | Count |
|-------|------|-------|
| Chart templates | `templates/charts/` | 52 |
| Icons (tabler-filled) | `templates/icons/tabler-filled/` | 1,053 |
| Icons (tabler-outline) | `templates/icons/tabler-outline/` | 5,039 |
| Layout templates | `templates/layouts/` | 3 styles |

Query icons on demand: `ls templates/icons/<library>/ | grep <keyword>`

## Dependencies

- **Required:** python-pptx, lxml (for svg_to_pptx converter)
- **Required skill:** deckdone-build (this file)
- **Optional skill:** deckdone-plan (for creating input deliverables — Steps 1-5)

## Harness Principle

When a generated slide has quality issues, fix the **harness** not the slide: update `references/svg-constraints.md`, `templates/layouts/`, or `scripts/`. Log in `harness-improvements.md`.
