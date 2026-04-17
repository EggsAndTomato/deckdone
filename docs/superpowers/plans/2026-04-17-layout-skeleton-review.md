# Layout Skeleton Review Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a lightweight text-based layout skeleton review step (Step 5) to the DeckDone workflow, replacing the heavy HTML wireframe step (old Step 6).

**Architecture:** Edit SKILL.md to insert Step 5 (Layout Skeleton Review), delete old Step 6 (HTML Wireframes), and renumber all subsequent steps. Create a new reference file `layout-skeleton-format.md` with ASCII wireframe conventions. Update quality-checklist.md, state-templates.md, and delete html-wireframe-guide.md.

**Tech Stack:** Markdown editing only. No code changes. Python stdlib scripts unchanged.

**Spec:** `docs/superpowers/specs/2026-04-17-layout-skeleton-review-design.md`

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `skills/deckdone/references/layout-skeleton-format.md` | ASCII wireframe conventions and per-type templates |
| Modify | `skills/deckdone/SKILL.md` | Insert Step 5, delete old Step 6, renumber 5→6, 7→7, 9→9, 10→10, 11→11, update tables |
| Modify | `skills/deckdone/references/quality-checklist.md` | Reorder Step 5→6, insert new Step 5 checks, delete old Step 6 checks |
| Modify | `skills/deckdone/references/state-templates.md` | Replace wireframes/ with layout-skeleton.md |
| Delete | `skills/deckdone/references/html-wireframe-guide.md` | Orphaned after Step 6 removal |

---

## Chunk 1: Create layout-skeleton-format.md

This is the foundation reference file that Step 5 reads. All other changes reference it.

### Task 1: Create layout-skeleton-format.md

**Files:**
- Create: `skills/deckdone/references/layout-skeleton-format.md`

- [ ] **Step 1: Write the reference file**

Create `skills/deckdone/references/layout-skeleton-format.md` with the following content:

```markdown
# Layout Skeleton Format Reference

Conventions for generating text-based layout skeletons in Step 5 (Layout Skeleton Review). Read by the AI at workflow execution time.

---

## ASCII Box Drawing Characters

Use Unicode box-drawing characters for all zone diagrams:

| Purpose | Characters |
|---------|-----------|
| Outer box corners | `┌ ┐ └ ┘` |
| Outer box horizontal | `─` |
| Outer box vertical | `│` |
| T-junctions (splits) | `┬ ┴ ├ ┤` |
| Cross junction | `┼` |
| Double-line outer (Composite sub-patterns) | `╔ ╗ ╚ ╝ ║ ═` |
| Inner/nested zones | `┌ ┐ └ ┘ │ ─` (same single-line) with dashed content |

Max diagram width: **72 characters** (fits standard terminal).

---

## Zone Label Syntax

Each zone block contains three lines:

```
│ [type] Content summary text here              (weight) │
```

- `[type]` — one of: `title`, `subtitle`, `body`, `bullet-list`, `data-table`, `chart-area`, `image-area`, `quote`, `timeline-item`, `comparison-col`, `icon-grid`, `label`
- Content summary — noun phrase, max 80 chars, describes intent not exact copy
- `(weight)` — one of: `(primary)`, `(secondary)`, `(auxiliary)`

Multi-line zones repeat the content line for additional detail:

```
│ [type] First line of content summary          (weight) │
│        Second line of detail                            │
```

---

## Overview Table Schema

One table at the top of `layout-skeleton.md`, one row per page:

```markdown
| # | Type | Title | Key Content | Zones |
|---|------|-------|-------------|-------|
| 1 | Cover | Slide Title | One-phrase content scope | 3 |
```

Columns:
- `#` — page number from outline
- `Type` — page type from layout-system.md
- `Title` — slide headline
- `Key Content` — what this page communicates (max 60 chars)
- `Zones` — count of visual zones

Sorted by page number. Section dividers get their own rows.

---

## Per-Page-Type Default Layouts

Templates below show the standard zone arrangement for each page type. The AI uses these as starting points and adapts based on outline content.

### Cover

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  [title] Presentation title                     (primary)│
│  [subtitle] Subtitle or tagline              (secondary)│
│                                                          │
│  [label] Date / Author / Affiliation          (auxiliary)│
│                                                          │
└──────────────────────────────────────────────────────────┘
```
Zones: 3. Weight distribution: 1 primary, 1 secondary, 1 auxiliary.

### Agenda

```
┌──────────────────────────────────────────────────────────┐
│ [title] Agenda / Overview                       (primary)│
├──────────────────────────┬───────────────────────────────┤
│ [bullet-list]            │ [bullet-list]                 │
│ Section 1 items          │ Section 3 items               │
│ (secondary)              │ (secondary)                   │
├──────────────────────────┼───────────────────────────────┤
│ [bullet-list]            │ [bullet-list]                 │
│ Section 2 items          │ Section 4 items               │
│ (secondary)              │ (secondary)                   │
└──────────────────────────┴───────────────────────────────┘
```
Zones: 5 (1 title + 4 list columns, two-column grid). Weight: 1 primary, 4 secondary.

### Section Divider

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  [title] Section title                         (primary)│
│  [body] Brief section description            (secondary)│
│                                                          │
└──────────────────────────────────────────────────────────┘
```
Zones: 2. Weight: 1 primary, 1 secondary.

### Content-Text

```
┌──────────────────────────────────────────────────────────┐
│ [title] Slide headline                          (primary)│
├──────────────────────────────────────────────────────────┤
│ [bullet-list] Key point 1                     (secondary)│
│ [bullet-list] Key point 2                     (secondary)│
│ [bullet-list] Key point 3                     (secondary)│
│ [body] Supporting paragraph                    (secondary)│
├──────────────────────────────────────────────────────────┤
│ [label] Source / footnote                      (auxiliary)│
└──────────────────────────────────────────────────────────┘
```
Zones: 3-7. Weight: 1 primary, N secondary, 1 auxiliary.

### Content-TwoCol

```
┌──────────────────────────────────────────────────────────┐
│ [title] Slide headline                          (primary)│
├──────────────────────────┬───────────────────────────────┤
│ [body] Left column content │ [body] Right column content │
│ (secondary)                │ (secondary)                 │
│ [bullet-list] Left details │ [bullet-list] Right details │
├──────────────────────────┴───────────────────────────────┤
│ [label] Footer note                            (auxiliary)│
└──────────────────────────────────────────────────────────┘
```
Zones: 4-6. Split: 50/50 or 40/60. Weight: 1 primary, N secondary, 0-1 auxiliary.

### Data-Chart

```
┌──────────────────────────────────────────────────────────┐
│ [title] Slide headline                          (primary)│
├──────────────────────────────────────────────────────────┤
│ [chart-area] Chart type + data description     (primary)│
├──────────────────────────────────────────────────────────┤
│ [body] One-line data interpretation           (secondary)│
│ [label] Data source / footnote                 (auxiliary)│
└──────────────────────────────────────────────────────────┘
```
Zones: 4. Weight: 2 primary, 1 secondary, 1 auxiliary.

### Quote

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  [quote] Quotation text                        (primary)│
│                                                          │
│  [body] Attribution — Speaker Name, Role      (secondary)│
│                                                          │
└──────────────────────────────────────────────────────────┘
```
Zones: 2. Weight: 1 primary, 1 secondary.

### Timeline

```
┌──────────────────────────────────────────────────────────┐
│ [title] Slide headline                          (primary)│
├──────────────────────────────────────────────────────────┤
│ [timeline-item] Event 1  │ [timeline-item] Event 2       │
│ Date + description       │ Date + description            │
│ (secondary)              │ (secondary)                   │
├──────────────────────────┼───────────────────────────────┤
│ [timeline-item] Event 3  │ [timeline-item] Event 4       │
│ (secondary)              │ (secondary)                   │
└──────────────────────────┴───────────────────────────────┘
```
Zones: 3-9 (1 title + N events). Max 6 horizontal, 8 vertical.

### Comparison

```
┌──────────────────────────────────────────────────────────┐
│ [title] Slide headline                          (primary)│
├──────────────────────────┬───────────────────────────────┤
│ [comparison-col] Option A │ [comparison-col] Option B    │
│ (secondary)               │ (secondary)                  │
│ Criteria details           │ Criteria details             │
├──────────────────────────┴───────────────────────────────┤
│ [label] Summary note                           (auxiliary)│
└──────────────────────────────────────────────────────────┘
```
Zones: 3-4. Split: 50/50. Max 6 criteria rows.

### Closing

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  [title] Key takeaway / summary                (primary)│
│                                                          │
│  [body] Call to action                        (secondary)│
│                                                          │
│  [label] Contact info / thank you              (auxiliary)│
│                                                          │
└──────────────────────────────────────────────────────────┘
```
Zones: 3. Weight: 1 primary, 1 secondary, 1 auxiliary.

### Composite-Diagram

```
┌──────────────────────────────────────────────────────────┐
│ [title] Slide headline                          (primary)│
├──────────────────────────────────────────────────────────┤
│ ╔════════════════════════════════════════════════════════╗│
│ ║ [body] Subsystem 1 label                      (primary)║│
│ ║ ┌────────────────────┬───────────────────────────┐     ║│
│ ║ │ [label] Component A │ [label] Component B      │     ║│
│ ║ │ (secondary)        │ (secondary)               │     ║│
│ ║ └────────────────────┴───────────────────────────┘     ║│
│ ╚════════════════════════════════════════════════════════╝│
│ ╔════════════════════════════════════════════════════════╗│
│ ║ [body] Subsystem 2 label                    (secondary)║│
│ ║ ┌─────────────────┬──────────────────┬────────────┐   ║│
│ ║ │ [label] Comp C  │ [label] Comp D   │ [label] E  │   ║│
│ ║ └─────────────────┴──────────────────┴────────────┘   ║│
│ ╚════════════════════════════════════════════════════════╝│
└──────────────────────────────────────────────────────────┘
```
Zones: 3-15. Double-line borders for outer containers, single-line for inner components. Max 3 nesting levels.

### Pipeline-Flow

```
┌──────────────────────────────────────────────────────────┐
│ [title] Slide headline                          (primary)│
├──────────────────────────────────────────────────────────┤
│ [label] Stage 1  →  [label] Stage 2  →  [label] Stage 3 │
│ Description       Description        Description         │
│ (secondary)       (secondary)        (secondary)         │
├──────────────────────────────────────────────────────────┤
│ [body] Pipeline summary or output note        (auxiliary)│
└──────────────────────────────────────────────────────────┘
```
Zones: 3-13 (1 title + N stages + 0-1 summary). Max 6 stages/row, max 2 rows. Arrow connectors between stages.

---

## Content Summary Writing Guidelines

- Use **noun phrases**, not full sentences: "Revenue growth bar chart" not "This slide shows a bar chart about revenue growth"
- Max **80 characters** per zone summary
- Describe **intent and scope**, not exact copy: "Three key findings from Q4" not "Finding 1: X, Finding 2: Y"
- For chart areas: include chart type + data subject: "Pie chart: market share by segment"
- For image areas: describe the image role: "Product photo placeholder" or "Architecture diagram"
- Composite sub-zones: subsystem name + component count: "Auth layer — 4 microservices"
```

- [ ] **Step 2: Verify file exists**

Run: `ls skills/deckdone/references/layout-skeleton-format.md`
Expected: file listed

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/references/layout-skeleton-format.md
git commit -m "feat: add layout-skeleton-format.md reference for Step 5"
```

---

## Chunk 2: Edit SKILL.md — Tables and Phase 2

### Task 2: Update Workflow at a Glance table

**Files:**
- Modify: `skills/deckdone/SKILL.md:16-21`

- [ ] **Step 1: Update the table**

Replace lines 16-21 in SKILL.md:

Old:
```
| Phase | Name | Interaction | Steps | Goal |
|-------|------|-------------|-------|------|
| 1 | Discovery | Deep | 1–3 | Understand what to communicate; gather materials |
| 2 | Design | Page-by-page | 4–6 | Define layout system and visual style |
| 3 | Content | Lightweight | 7–8 | Write exact content for every visual zone |
| 4 | Implementation | Batch execution | 9–11 | Generate PPTX with quality assurance |
```

New:
```
| Phase | Name | Interaction | Steps | Goal |
|-------|------|-------------|-------|------|
| 1 | Discovery | Deep | 1–3 | Understand what to communicate; gather materials |
| 2 | Design | Page-by-page | 4–6 | Define layout skeleton, page types, and visual style |
| 3 | Content | Lightweight | 7–8 | Write exact content for every visual zone |
| 4 | Implementation | Batch execution | 9–11 | Generate PPTX with quality assurance |
```

Change: Phase 2 Steps stays "4–6" but Goal text updates to include "layout skeleton".

### Task 2b: Update Dependency Detection step number

**Files:**
- Modify: `skills/deckdone/SKILL.md:69`

- [ ] **Step 1: Renumber Step 5 reference to Step 6**

Line 69, change:
```
- **Step 5 (Visual Style):** Check for the theme-factory skill to surface additional presets. If unavailable, rely solely on `references/style-presets.md`.
```
to:
```
- **Step 6 (Visual Style):** Check for the theme-factory skill to surface additional presets. If unavailable, rely solely on `references/style-presets.md`.
```

### Task 3: Update Deliverable Files table

**Files:**
- Modify: `skills/deckdone/SKILL.md:78-93`

- [ ] **Step 1: Update the table**

Replace lines 78-93:

Old:
```markdown
| File | Phase | Step | Description |
|------|-------|------|-------------|
| `brief.md` | 1 | 1 | Presentation brief |
| `materials/` | 1 | 2 | Collected and classified source materials |
| `outline.md` | 1 | 3 | Content outline with page estimates |
| `layout-system.md` | 2 | 4 | Page type assignments per slide |
| `style-guide.md` | 2 | 5 | Visual style definition |
| `wireframes/` | 2 | 6 | HTML wireframes per slide |
| `content-plan.md` | 3 | 7 | Detailed content per visual zone |
| `test-slides/` | 4 | 9 | Test slide samples |
| `template-params.md` | 4 | 9 | Locked template parameters |
| `output.pptx` | 4 | 10 | Generated presentation |
| `final.pptx` | 4 | 11 | Final reviewed presentation |
| `deckdone-state.md` | all | all | Progress state file |
| `deckdone-trace.md` | all | all | Execution trace log |
| `harness-improvements.md` | all | all | Harness improvement log |
```

New:
```markdown
| File | Phase | Step | Description |
|------|-------|------|-------------|
| `brief.md` | 1 | 1 | Presentation brief |
| `materials/` | 1 | 2 | Collected and classified source materials |
| `outline.md` | 1 | 3 | Content outline with page estimates |
| `layout-system.md` | 2 | 4 | Page type assignments per slide |
| `layout-skeleton.md` | 2 | 5 | Text wireframes with zone layout and content summaries |
| `style-guide.md` | 2 | 6 | Visual style definition |
| `content-plan.md` | 3 | 7 | Detailed content per visual zone |
| `test-slides/` | 4 | 9 | Test slide samples |
| `template-params.md` | 4 | 9 | Locked template parameters |
| `output.pptx` | 4 | 10 | Generated presentation |
| `final.pptx` | 4 | 11 | Final reviewed presentation |
| `deckdone-state.md` | all | all | Progress state file |
| `deckdone-trace.md` | all | all | Execution trace log |
| `harness-improvements.md` | all | all | Harness improvement log |
```

Changes:
- Replace `wireframes/` row with `layout-skeleton.md` at Step 5
- Renumber `style-guide.md` from Step 5 to Step 6

### Task 4: Insert Step 5 (Layout Skeleton Review) and renumber old Step 5 → Step 6

**Files:**
- Modify: `skills/deckdone/SKILL.md:304-329`

- [ ] **Step 1: Replace old Step 5 header and add new Step 5**

Replace the content from line 304 (`### Step 5: Visual Style Direction`) through line 329 (`**Validation:** Run \`references/quality-checklist.md\` Section 2.2.`) plus the `---` on line 331.

The replacement is the **new Step 5** block followed by the **renumbered Step 6** (old Step 5), with a `---` separator between them:

```markdown
### Step 5: Layout Skeleton Review

**AI Behavior:**

1. Read confirmed `layout-system.md` (page type assignments from Step 4).
2. Read `references/layout-skeleton-format.md` for ASCII wireframe conventions and per-type zone templates.
3. Read `references/layout-types.md` for zone ratio references to inform zone sizes in text diagrams.
4. Read `outline.md` for section structure and page purposes.
5. Generate **overview table** — one row per page with: page number, page type, title, key content summary (one phrase), zone count.
6. Present overview table to user. **Gate 1:** User confirms overall rhythm, page order, and content scope. If rejection requires page type or count changes, return to Step 4 to revise `layout-system.md` before regenerating.
7. After overview approval, generate **per-page text wireframes** batched by section (5–8 pages per batch).
8. For each page:
   - Draw ASCII box diagram reflecting the page type's standard zone layout (from `references/layout-skeleton-format.md`).
   - Label each zone with type, one-line content summary, and visual weight.
   - For Composite-Diagram and Pipeline-Flow types: show sub-zone nesting with double-line outer borders.
9. **Gate 2:** User confirms each batch. If rejection requires structural changes to a page's type, return to Step 4 to revise. Adjustments applied before next batch.
10. After all batches confirmed, write `layout-skeleton.md`.

**Deliverable:** `layout-skeleton.md`

```markdown
# Layout Skeleton

## Overview

| # | Type | Title | Key Content | Zones |
|---|------|-------|-------------|-------|
| 1 | Cover | ... | ... | N |
...

---

## Slide 1: [Title] [PageType]
┌──────────────────────────────────────────────────────────┐
│ [zone-type] Content summary                   (weight)   │
├──────────────────────────────────────────────────────────┤
│ [zone-type] Content summary                   (weight)   │
└──────────────────────────────────────────────────────────┘
```

**Gate:** Overview confirmed + all per-page batches confirmed.

**State Update:** Update `deckdone-state.md` — Phase 2, Step 5 complete.

**Validation:** Run `references/quality-checklist.md` Section 2.2.

---

### Step 6: Visual Style Direction

**AI Behavior:**

1. Read `references/style-presets.md` (15–20 style presets).
2. Check for theme-factory skill availability. If available, surface additional presets.
3. Recommend 2–3 styles based on presentation purpose + audience profile.
4. Show style previews: color palette + typography + decoration characteristics.
5. User selects a style or fine-tunes parameters.

**Deliverable:** `style-guide.md`

```markdown
# Style Guide
## Palette: [primary/secondary/accent/background/text — hex values]
## Typography: [heading font + body font + size scale]
## Decoration: [border style / shape patterns / background treatment]
## Layout Rules: [margins / spacing / content area ratios]
## Pre-render Rules: [which visual effects need Sharp rasterization]
```

**Gate:** User confirms style direction. Phase 2 complete.

**State Update:** Update `deckdone-state.md` — Phase 2, Step 6 complete.

**Validation:** Run `references/quality-checklist.md` Section 2.3.
```

Changes:
- New Step 5 (Layout Skeleton Review) with AI behavior, deliverable, gate, state, validation
- Old Step 5 renumbered to Step 6
- Step 6 gate now includes "Phase 2 complete." (moved from deleted old Step 6)
- Step 6 validation section renumbered to 2.3

### Task 5: Delete old Step 6 (HTML Wireframes)

> **Note on execution order:** Tasks 5-8 all modify `SKILL.md`. Line numbers stated here are from the **original** file. Since Task 4 adds ~32 lines, tasks 5-8 should be executed **bottom-up** (Task 8 → 7 → 6 → 5) to avoid stale line numbers. Alternatively, use text-match (not line numbers) to locate edit targets.

**Files:**
- Modify: `skills/deckdone/SKILL.md:333-363`

- [ ] **Step 1: Remove the entire old Step 6 block**

Delete lines 333–363 (from `### Step 6: Page-by-page Wireframes (HTML)` through the closing `---`). This includes the entire step definition: AI behavior, deliverable (`wireframes/` directory), gate, state update, and validation sections.

- [ ] **Step 2: Verify deletion**

Read lines 329-370 of SKILL.md. Expected: Step 6 (Visual Style Direction) is immediately followed by Phase 3 header, with no trace of old Step 6 HTML Wireframes content.

### Task 6: Update Step 7 references

**Files:**
- Modify: `skills/deckdone/SKILL.md:373`

- [ ] **Step 1: Replace wireframes reference in Step 7 AI behavior**

Line 373, change:
```
1. Based on confirmed outline + layout-system + style-guide + wireframes, generate a detailed content spec per page.
```
to:
```
1. Based on confirmed outline + layout-system + layout-skeleton + style-guide, generate a detailed content spec per page.
```

### Task 7: Update Step 9 references

**Files:**
- Modify: `skills/deckdone/SKILL.md:444`

- [ ] **Step 1: Replace wireframes reference in Step 9**

Line 444, change:
```
   - Layout accuracy against wireframes
```
to:
```
   - Layout accuracy against layout-skeleton.md
```

### Task 8: Update Steps 10-11 validation commands

**Files:**
- Modify: `skills/deckdone/SKILL.md:483-484`
- Modify: `skills/deckdone/SKILL.md:505-506`

- [ ] **Step 1: Update Step 10 validation paths**

Replace lines 483-484:
```
- Run `python scripts/validate-html-slides.py wireframes/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md wireframes/`
```
with:
```
- Run `python scripts/validate-html-slides.py test-slides/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md test-slides/`
```

- [ ] **Step 2: Update Step 11 validation paths**

Replace lines 505-506:
```
- Run `python scripts/validate-html-slides.py wireframes/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md wireframes/`
```
with:
```
- Run `python scripts/validate-html-slides.py test-slides/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md test-slides/`
```

- [ ] **Step 3: Commit SKILL.md changes**

```bash
git add skills/deckdone/SKILL.md
git commit -m "feat: add Step 5 layout skeleton review, remove Step 6 HTML wireframes, renumber steps"
```

---

## Chunk 3: Update Reference Files and Delete html-wireframe-guide.md

### Task 9: Update quality-checklist.md

**Files:**
- Modify: `skills/deckdone/references/quality-checklist.md`

- [ ] **Step 1: Update Table of Contents (lines 10-21)**

Replace lines 10-21:

Old:
```markdown
| Step | Deliverable | Section |
|------|-------------|---------|
| 1 | `brief.md` | [Step 1: Brief Validation](#step-1-briefmd-validation) |
| 2 | `materials/` | [Step 2: Materials Validation](#step-2-materials-validation) |
| 3 | `outline.md` | [Step 3: Outline Validation](#step-3-outlinemd-validation) |
| 4 | `layout-system.md` | [Step 4: Layout System Validation](#step-4-layout-systemmd-validation) |
| 5 | `style-guide.md` | [Step 5: Style Guide Validation](#step-5-style-guidemd-validation) |
| 6 | `wireframes/` | [Step 6: Wireframes Validation](#step-6-wireframes-validation) |
| 7 | `content-plan.md` | [Step 7: Content Plan Validation](#step-7-content-planmd-validation) |
| 9 | `test-slides/` | [Step 9: Test Slides Validation](#step-9-test-slides-validation) |
| 10 | `output.pptx` | [Step 10: Output Validation](#step-10-outputpptx-validation) |
| 11 | `final.pptx` | [Step 11: Final Validation](#step-11-finalpptx-validation) |
```

New:
```markdown
| Step | Deliverable | Section |
|------|-------------|---------|
| 1 | `brief.md` | [Step 1: Brief Validation](#step-1-briefmd-validation) |
| 2 | `materials/` | [Step 2: Materials Validation](#step-2-materials-validation) |
| 3 | `outline.md` | [Step 3: Outline Validation](#step-3-outlinemd-validation) |
| 4 | `layout-system.md` | [Step 4: Layout System Validation](#step-4-layout-systemmd-validation) |
| 5 | `layout-skeleton.md` | [Step 5: Layout Skeleton Validation](#step-5-layout-skeleton-validation) |
| 6 | `style-guide.md` | [Step 6: Style Guide Validation](#step-6-style-guidemd-validation) |
| 7 | `content-plan.md` | [Step 7: Content Plan Validation](#step-7-content-planmd-validation) |
| 9 | `test-slides/` | [Step 9: Test Slides Validation](#step-9-test-slides-validation) |
| 10 | `output.pptx` | [Step 10: Output Validation](#step-10-outputpptx-validation) |
| 11 | `final.pptx` | [Step 11: Final Validation](#step-11-finalpptx-validation) |
```

- [ ] **Step 2: Replace Step 5 and Step 6 sections**

Find the existing sections (around lines 56-71):

Old Step 5 (style-guide):
```markdown
## Step 5: style-guide.md Validation

- [ ] **Complete palette defined** with at least: primary, secondary, accent, background, and text colors — all in valid hex format
- [ ] **Typography specified** — heading font family, body font family, and at least three size tiers (heading, subheading, body) with exact pt values
- [ ] **Decoration patterns documented** — divider styles, corner ornaments, background textures, or an explicit "None" statement
- [ ] **Pre-render rules documented** — which visual effects require Sharp processing (gradients, blurred overlays, complex shapes) are listed
```

Old Step 6 (wireframes):
```markdown
## Step 6: wireframes/ Validation

- [ ] **One HTML file exists per planned page** — file count matches the page count from `outline.md`
- [ ] **All HTML files have correct dimensions** — viewport is exactly 720pt × 405pt (no px, no %, no exceptions)
- [ ] **Every zone is labeled with content type** — each zone div contains a text label indicating its content role (title, body, chart, icon, etc.)
- [ ] **Visual weight is annotated** — each zone is marked primary, secondary, or auxiliary in a comment or data attribute
- [ ] **All pre-render element positions are marked** — icons, generated images, and gradient blocks are shown as labeled placeholder boxes
- [ ] **No CSS gradients used in wireframes** — wireframes use flat colors and borders only; gradients are deferred to pre-render
```

Replace both sections with:

```markdown
## Step 5: layout-skeleton.md Validation

- [ ] **Overview table has one row per planned page** — row count matches page count from `outline.md`
- [ ] **Every page uses a valid page type** matching `layout-system.md` assignments
- [ ] **Every zone is labeled with content type** — recognized type from the type catalog in `layout-skeleton-format.md`
- [ ] **Every zone has a non-empty content summary** — no zone is blank or "TBD"
- [ ] **Visual weight is annotated per zone** — primary / secondary / auxiliary
- [ ] **Per-type zone count is reasonable** — no page has a zone count that exceeds the maximum defined in `layout-types.md`
- [ ] **Composite-Diagram and Pipeline-Flow pages show sub-zone structure** — nested zones visible with appropriate border notation

## Step 6: style-guide.md Validation

- [ ] **Complete palette defined** with at least: primary, secondary, accent, background, and text colors — all in valid hex format
- [ ] **Typography specified** — heading font family, body font family, and at least three size tiers (heading, subheading, body) with exact pt values
- [ ] **Decoration patterns documented** — divider styles, corner ornaments, background textures, or an explicit "None" statement
- [ ] **Pre-render rules documented** — which visual effects require Sharp processing (gradients, blurred overlays, complex shapes) are listed
```

- [ ] **Step 3: Update resume validation section reference**

In the resume validation section, find (around line 138):
```
2. [ ] **Current phase and step are clearly stated** — the state file names exactly which step to resume from (e.g. "Step 6: wireframes")
```
Change to:
```
2. [ ] **Current phase and step are clearly stated** — the state file names exactly which step to resume from (e.g. "Step 5: layout-skeleton")
```

No other step-number-specific references remain in the checklist body.

- [ ] **Step 4: Commit**

```bash
git add skills/deckdone/references/quality-checklist.md
git commit -m "feat: update quality-checklist for Step 5 layout skeleton, remove Step 6 wireframes"
```

### Task 10: Update state-templates.md

**Files:**
- Modify: `skills/deckdone/references/state-templates.md:16`
- Modify: `skills/deckdone/references/state-templates.md:34`

- [ ] **Step 1: Replace wireframes reference in Progress example**

Line 16, change:
```
- Progress: [e.g., "Batch 2/4 wireframes confirmed"]
```
to:
```
- Progress: [e.g., "Section 2/4 layout skeletons confirmed"]
```

- [ ] **Step 2: Replace wireframes/ deliverable entry**

Line 34, change:
```
- wireframes/ [status with count]
```
to:
```
- layout-skeleton.md [status]
```

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/references/state-templates.md
git commit -m "feat: replace wireframes/ with layout-skeleton.md in state template"
```

### Task 11: Delete html-wireframe-guide.md

**Files:**
- Delete: `skills/deckdone/references/html-wireframe-guide.md`

- [ ] **Step 1: Delete the file**

```bash
rm skills/deckdone/references/html-wireframe-guide.md
```

- [ ] **Step 2: Commit**

```bash
git add -u skills/deckdone/references/html-wireframe-guide.md
git commit -m "chore: delete html-wireframe-guide.md (orphaned after Step 6 removal)"
```

---

## Chunk 4: Final Verification

### Task 12: Verify all changes are consistent

- [ ] **Step 1: Verify SKILL.md has no remaining references to "wireframes" or old step numbering**

Run: `grep -n "wireframe" skills/deckdone/SKILL.md`
Expected: only the new Step 5 reference to `references/layout-skeleton-format.md` (which is about wireframes in general), and the deleted Step 6 content should be gone. The word "wireframe" should only appear in Step 5's text ("text wireframes") and in Step 9's reference to "layout-skeleton.md" (not "wireframes").

Run: `grep -n "Step 6:" skills/deckdone/SKILL.md`
Expected: one match — `### Step 6: Visual Style Direction`

Run: `grep -n "Step 5:" skills/deckdone/SKILL.md`
Expected: one match — `### Step 5: Layout Skeleton Review`

- [ ] **Step 2: Verify html-wireframe-guide.md is deleted**

Run: `ls skills/deckdone/references/html-wireframe-guide.md`
Expected: file not found

- [ ] **Step 3: Verify layout-skeleton-format.md exists**

Run: `ls skills/deckdone/references/layout-skeleton-format.md`
Expected: file listed

- [ ] **Step 4: Verify quality-checklist.md has no references to "wireframes/"**

Run: `grep -n "wireframes" skills/deckdone/references/quality-checklist.md`
Expected: no matches

- [ ] **Step 5: Verify state-templates.md has no references to "wireframes/"**

Run: `grep -n "wireframes" skills/deckdone/references/state-templates.md`
Expected: no matches

- [ ] **Step 6: Verify references/ file list**

Run: `ls skills/deckdone/references/`
Expected: contains `layout-skeleton-format.md`, does NOT contain `html-wireframe-guide.md`
