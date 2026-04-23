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
2. **NO BATCH SVG GENERATION** — Generate one SVG page at a time, sequentially. NEVER write multiple SVGs in a single response.
3. **LOCK DESIGN CONTEXT** — Before Step 7, extract and lock global tokens (colors, font scale, spacing, decoration patterns). Use this locked context for every subsequent page.
4. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require full stop. Wait for explicit user confirmation before proceeding.
5. **NO SPECULATIVE EXECUTION** — Do not pre-write SVG code during earlier steps.
6. **READ CONSTRAINTS FIRST** — Read `references/svg-constraints.md` before starting Step 6.
7. **MAIN-AGENT ONLY** — SVG generation MUST stay in the current main agent. Never delegate page generation to sub-agents.

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

### 6b. Test SVG Generation

1. From `layout-system.md`, identify all distinct layout types used.
2. Select **one page per layout type** as test samples.
3. For each test page:
   a. Read the SVG template from the relevant layout template in `templates/layouts/`.
   b. Replace placeholders with actual content from `content-plan.md`.
   c. Apply style tokens from `style-guide.md` (colors, fonts, spacing).
   d. Write the SVG file, strictly constrained by `references/svg-constraints.md`.
   e. Save to `svg_output/` with naming pattern: `P01_Cover.svg`, `P02_Agenda.svg`, etc.
4. After all test SVGs are written, run conversion:
   ```bash
   python scripts/svg_to_pptx.py <project-dir> -s svg_output -o test-slides/output.pptx
   ```
5. Present to user for review. Check:
   - Layout accuracy against `layout-skeleton.md`
   - Text cutoff or overflow
   - Color and spacing correctness
   - SVG-to-PPTX conversion fidelity
6. If unsatisfied, adjust and regenerate (max 3 rounds per page).
7. Lock final template parameters → `template-params.md`.

**Deliverable:** `style-guide.md` + `test-slides/output.pptx` + `template-params.md`

**Gate:** User confirms visual style and all test page visuals.

---

## Step 7: Batch Generation + Quality Review

⛔ **BLOCKING** — Step 6 gate must be passed.

### 7a. Batch SVG Generation

1. **Lock design context** — extract from `style-guide.md` and `template-params.md`:
   - Global color tokens (primary, secondary, accent, backgrounds, text levels)
   - Font scale (heading sizes, body size, caption size, line-height)
   - Spacing system (margins, padding, gaps)
   - Decoration patterns (dividers, accent shapes, icon usage)
2. Generate pages **sequentially, one at a time**:
   - Read page content from `content-plan.md`.
   - Read layout from `layout-skeleton.md`.
   - Write SVG constrained by `references/svg-constraints.md` AND locked design context.
   - Save to `svg_output/`.
   - Proceed to next page.
3. After all SVGs generated, run conversion:
   ```bash
   python scripts/svg_to_pptx.py <project-dir> -s svg_output -o output.pptx
   ```
4. Run SVG validation on all files:
   ```bash
   python scripts/validate-svg-slides.py svg_output/
   ```

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
   python scripts/svg_to_pptx.py <project-dir> -s svg_output -o output.pptx
   ```

**Deliverable:** `output.pptx` + all SVGs in `svg_output/`

---

## Step 8: Final Export + Presentation Guide

⛔ **BLOCKING** — User must confirm presentation guide content.

**AI Behavior:**

### 8a. Final PPTX

1. Verify all SVGs pass validation.
2. Run final conversion:
   ```bash
   python scripts/svg_to_pptx.py <project-dir> -s svg_output -o final.pptx
   ```

### 8b. Presentation Guide

1. Read confirmed deliverables:
   - `brief.md` (purpose, audience, framework, density, scale)
   - `outline.md` (section structure, page count)
   - `content-plan.md` (per-page content, visual narrative paths)
   - `style-guide.md` (visual style)
   - `layout-skeleton.md` (page layout overview)
2. Generate `presentation-guide.md` following the 4-module template in `references/presentation-guide-template.md`:
   - **Module 1: Overview** — topic, core message, audience, slide count, duration, narrative framework
   - **Module 2: Design Rationale** — narrative logic, section intentions, key design decisions
   - **Module 3: Slide Key Points** — per-slide emphasis levels (★ Key / Normal / ⏭ Skippable), time allocation
   - **Module 4: Speaking Notes** — transition cues, anticipated questions, timing guidance
3. Determine emphasis levels based on each page's contribution to the Key Message from `brief.md`.
4. Calculate time allocation from `brief.md` Scale field (total minutes ÷ total pages, weighted by emphasis). If no time estimate, default to 1.5 minutes per page.
5. Predict 2-3 likely audience questions based on content gaps or contentious points.
6. Write in the user's preferred language.
7. Present to user for confirmation. Allow edits.

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
   python scripts/svg_to_pptx.py <project-dir> -s svg_output -o final-revised.pptx
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
