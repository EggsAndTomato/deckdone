# Density Presets Design — Presentation Information Density Control

**Date:** 2026-04-17
**Status:** Approved
**Affects:** `skills/deckdone/SKILL.md`, `references/layout-types.md`, `references/layout-templates.md`, `references/quality-checklist.md`

---

## Problem

Generated presentations have low information density — too few words per slide, excessive whitespace. The current harness treats all presentations as "speaker-assisted" style with sparse keywords. Users who need reading-type or detailed-presentation decks have no way to express this intent.

The root cause: `layout-types.md` hardcodes a single set of content capacity limits (e.g., "Max 6 bullets, max 90 chars/bullet"), and `layout-templates.md` hardcodes generous padding and line-height. There is no density dimension in the workflow.

## Solution

Add a three-level density choice in Phase 1 (Discovery), defined by **use case** rather than abstract complexity:

| Level | ID | Chinese | Description |
|-------|----|---------|-------------|
| Presentation | `presentation` | 演讲辅助型 | Keywords + visuals. Audience watches the speaker, not the slides. |
| Detailed Presentation | `detailed-presentation` | 演讲详述型 | Key points with supporting arguments. Speaker adds context. |
| Reading | `reading` | 阅读型 | Self-contained document. Reader understands without a presenter. |

### Design Principles

1. **Use-case framing** — Levels are named by how the deck will be used, not by abstract "simple/complex". Users naturally know whether they are presenting or writing a reading document.
2. **Data-driven presets** — Density rules live in a reference file (`density-presets.md`), not in workflow logic. The harness principle: fix the harness, not individual slides.
3. **Capacity + spacing, not font sizes** — Presets define content capacity limits and layout spacing parameters. Font sizes are chosen dynamically by the AI at generation time based on actual content amount within spacing constraints. Only a minimum readable font floor is enforced.
4. **Minimal workflow disruption** — Only Step 1 (new question), Step 7 (read capacity from preset), and Steps 9-10 (read spacing from preset) change. No new steps, no validation script changes.

---

## Parameter Design

### Global Spacing Parameters

Control how much of the 720pt × 405pt slide is available for content.

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Slide padding | 48pt | 36pt | 24pt |
| Line-height (body) | 1.9 | 1.6 | 1.35 |
| Paragraph gap (between bullets/blocks) | 14pt | 8pt | 4pt |
| Min readable body font | 14pt | 12pt | 10pt |

### Font Size Decision Rule

The AI selects font sizes at generation time. The rule:

1. Calculate available content area: 720pt × 405pt minus padding from density preset.
2. Choose the largest font size that fits all zone content within the available area.
3. Do not exceed the max content capacity for this page type + density level.
4. Do not go below the minimum readable body font for this density level.

No fixed font sizes are stored in the preset. The AI has full context (slide dimensions, actual text length, spacing parameters) and can reason about optimal sizing.

### Content Capacity per Page Type

Each page type has three columns of capacity limits. "Low-impact types" (Cover, Section Divider, Quote, Closing, Data-Chart) have no capacity differences across levels — only spacing parameters apply globally.

#### Content-Text

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max bullets | 4 | 6 | 10 |
| Max chars/bullet | 40 | 90 | 200 |
| Sub-bullets | none | 1 level | 2 levels |

#### Content-TwoCol

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max bullets/col | 3 | 4 | 6 |
| Max chars/col | 150 | 300 | 600 |

#### Agenda

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max items | 6 | 8 | 12 |
| Max chars/item | 30 | 50 | 80 |
| Sub-descriptions | no | optional | yes |

#### Timeline

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max events (horizontal) | 4 | 6 | 8 |
| Max chars/description | 20 | 40 | 80 |

#### Comparison

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max criteria rows | 4 | 5 | 8 |
| Max chars/cell | 30 | 60 | 120 |

#### Composite-Diagram

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max nodes | 8 | 12 | 15 |
| Max chars/node label | 20 | 30 | 50 |
| Node descriptions | no | brief | yes |

#### Pipeline-Flow

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max stages/row | 4 | 5 | 6 |
| Max chars/stage desc | 15 | 30 | 60 |
| Sub-step rows | no | optional | yes |

---

## File Changes

### New File: `references/density-presets.md`

Contains all parameter tables above plus design philosophy descriptions. This is the single source of truth for density behavior. Approximately 80-100 lines.

### Modified: `skills/deckdone/SKILL.md`

Three surgical edits:

1. **Step 1 (Brief), question list** — After audience questions, add:
   > **Density:** 演讲辅助型 / 演讲详述型 / 阅读型 — "Will the audience read this deck on their own, or will you present it live?"

   Read `references/density-presets.md` to present the three options with descriptions. User selection recorded in `brief.md`.

2. **`brief.md` template** — Add field:
   ```markdown
   ## Density: [presentation | detailed-presentation | reading]
   ## Density Reasoning: [one sentence]
   ```

3. **Resume Protocol** — Add note: "Include density level in the Context Summary section of `deckdone-state.md` to ensure it survives cross-conversation resumption."

4. **Step 7 (Content Plan)** — Add instruction: "Read the density level from `brief.md`. Read the corresponding content capacity limits from `references/density-presets.md`. Use these as Max Length values for each zone instead of the defaults in `layout-types.md`."

4. **Step 9/10 (Implementation)** — Add instruction: "Read the density level from `brief.md`. Read the corresponding spacing parameters from `references/density-presets.md`. Apply padding, line-height, and gap values to HTML templates. Choose font sizes dynamically based on actual content amount within spacing constraints, respecting the minimum readable font floor."

### Modified: `references/layout-types.md`

Replace each page type's hardcoded "Content density" line with a cross-reference:

```
Content density: See references/density-presets.md for per-level capacity limits.
```

Keep zone ratio and font size scale references (those are structural, not density-dependent).

### Modified: `references/layout-templates.md`

Add comments to each template marking adjustable density parameters:

```html
<!-- DENSITY: padding adjustable — see density-presets.md -->
<div class="slide" style="padding: 36pt 48pt; ...">
```

```html
<!-- DENSITY: line-height adjustable — see density-presets.md -->
<ul style="font-size: 14pt; line-height: 1.9; ...">
```

Remove hardcoded font-size values from templates. The AI will set these at generation time.

### Modified: `references/quality-checklist.md`

Two new checks:

**Step 1 (Brief Validation):**
- [ ] **Density level is specified** — one of `presentation`, `detailed-presentation`, or `reading` is recorded with a one-sentence reasoning

**Step 7 (Content Plan Validation):**
- [ ] **Zone max lengths comply with density preset** — no zone exceeds the capacity limit for the chosen density level from `density-presets.md`

Also update the existing Step 7 check "No zone exceeds the max character limit defined in `layout-types.md`" to reference `density-presets.md` instead.

**Implementation note for font-size removal:** Remove font-size from content text elements (`<p>`, `<li>`, `<h2>`-`<h6>` within content zones). Keep font-size on structural elements (connector arrows `→`, decorative labels) as they are layout-level, not content-level.

### Unchanged Files

- `scripts/validate-content-plan.py` — Only validates field format (`-Type:`, `-Content:`, etc.), not numeric values. No change needed.
- `scripts/validate-html-slides.py` — Only validates html2pptx compatibility (dimensions, tag usage). No change needed.
- `references/layout-skeleton-format.md` — Wireframe format is density-agnostic.
- `references/style-presets.md` — Visual style is orthogonal to density.
- `references/narrative-frameworks.md` — Narrative structure is density-agnostic.

---

## Workflow Impact Summary

| Step | Change | Magnitude |
|------|--------|-----------|
| Step 1 Brief | New density question + brief field | Small |
| Step 2-3 | None | — |
| Step 4 | None | — |
| Step 5 | Wireframe content summaries may be longer at higher density, but flow unchanged | None |
| Step 6 | None | — |
| Step 7 | Max Length sourced from density preset instead of hardcoded defaults | Small |
| Step 8 | None | — |
| Step 9-10 | Spacing from preset, font sizes chosen dynamically | Medium |
| Step 11 | None | — |

Total: 1 new file (~80-100 lines), 4 modified files with surgical edits, 0 deleted files, 0 new validation scripts.
