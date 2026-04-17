# Design: Layout Skeleton Review Step

**Date:** 2026-04-17
**Status:** Approved
**Problem:** The DeckDone workflow jumps from page-type assignment to HTML wireframes (or skips wireframes entirely), producing near-final output without a low-cost structural review. Users cannot quickly validate "does each page's layout and content outline make sense?" before committing to detailed design.

---

## 1. Problem Statement

Two issues observed in practice:

1. **AI skips Step 6 (HTML wireframes)** — the workflow proceeds from outline directly to content planning, bypassing layout review.
2. **Step 6's wireframes are too heavy** — when executed, the HTML wireframes are near-final quality, negating the purpose of a lightweight review checkpoint.

The user needs a low-cost, fast-feedback mechanism to confirm the structural skeleton of each page (zone layout + content summary) before entering visual style and detailed content phases.

---

## 2. Solution: New Step 5 — Layout Skeleton Review

### 2.1 Position in Workflow

Insert a new step between the current Step 4 (Page Types & Layout System) and Step 5 (Visual Style Direction). Remove the current Step 6 (HTML Wireframes). Renumber all subsequent steps.

**New workflow order:**

```
Phase 2: Design [Page-by-page Confirmation]
  Step 4: Page Types & Layout System         (unchanged)
  Step 5: Layout Skeleton Review             (NEW — text wireframes)
  Step 6: Visual Style Direction             (was Step 5)
Phase 3: Content [Lightweight Confirmation]
  Step 7: Detailed Content Plan              (was Step 7, unchanged)
  Step 8: User Content Confirmation          (was Step 8, unchanged)
Phase 4: Implementation [Batch Execution]
  Step 9: Test Generation                    (was Step 9, unchanged)
  Step 10: Batch Generation                  (was Step 10, unchanged)
  Step 11: Final Quality Review              (was Step 11, unchanged)
```

Total steps: 11 (continuous integer numbering, no sub-steps).

### 2.2 Deliverable

A single file `layout-skeleton.md` containing:

1. **Overview table** — one row per page with type, title, key content summary, zone count
2. **Per-page text wireframes** — ASCII box diagrams with zone labels and content summaries

### 2.3 Gate Design

Two gates within Step 5:

- **Gate 1 (Overview):** User confirms overall rhythm, page order, and content scope. If rejection requires page type or count changes, return to Step 4 to revise `layout-system.md` before regenerating the overview.
- **Gate 2 (Per-page, batched by section):** User confirms zone layout and content summary for each page, 5-8 pages per batch. If rejection requires structural changes to a page's type, return to Step 4 to revise that page's type assignment.

### 2.4 Text Wireframe Format

Each page rendered as:

```
## Slide N: [Title] [[PageType]]
┌──────────────────────────────────────────────────┐
│ [title] Slide headline text                       │
├──────────────────────┬───────────────────────────┤
│ [chart-area]         │ [data-table]               │
│ Bar chart: revenue   │ Key figures summary        │
│ (primary)            │ (secondary)                │
├──────────────────────┴───────────────────────────┤
│ [body] One-line interpretation of the data        │
│ (auxiliary)                                       │
└──────────────────────────────────────────────────┘
```

Each zone annotated with:
- `[type]` — content type (title / body / chart-area / data-table / bullet-list / image-area / quote / timeline-item / comparison-col / icon-grid / subtitle / label)
- One-line content summary
- `(weight)` — primary / secondary / auxiliary

### 2.5 Overview Table Format

```markdown
## Layout Skeleton — Overview

| # | Type | Title | Key Content | Zones |
|---|------|-------|-------------|-------|
| 1 | Cover | ... | ... | 3 |
| 2 | Agenda | ... | ... | 5 |
```

---

## 3. Changes Required

### 3.1 SKILL.md

| Section | Change |
|---------|--------|
| Workflow at a Glance table | Update Phase 2 steps and row for new Step 5; remove old Step 6 row |
| Deliverable Files table | Add `layout-skeleton.md` at Step 5; remove `wireframes/` row |
| Step 5 (new) | Full step definition: AI behavior, deliverable format, gates, state update |
| Step 6 (was Step 5) | Renumber; add "Phase 2 complete" gate marker (previously on old Step 6) |
| Step 6 (old, deleted) | Remove entire Step 6: Page-by-page Wireframes (HTML) section |
| Step 7 | Renumber (was Step 7); replace "wireframes" input reference with "layout-skeleton.md" in AI behavior line 1 |
| Steps 8-11 | Renumber; update validation command paths that reference `wireframes/` to point to `test-slides/` instead |
| Phase 4 intro | Update "Step 9" references to new numbers |
| Harness Engineering Principles | Update step number references |

### 3.2 New Reference File

Create `references/layout-skeleton-format.md`:
- ASCII box diagram conventions: use Unicode box-drawing characters (`┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘ │ ─`), max width 72 chars to fit terminal
- Per-page-type default zone layouts: one ASCII template for each of the 12 page types (Cover, Agenda, Section Divider, Content-Text, Content-TwoCol, Data-Chart, Quote, Timeline, Comparison, Closing, Composite-Diagram, Pipeline-Flow). Each template shows the standard zone arrangement with labeled zones and default weight assignments
- Content summary writing guidelines: one line per zone, max 80 chars, describe intent/content scope (not exact copy), use noun phrases ("Revenue growth bar chart") not full sentences
- Overview table schema: 5 columns (#, Type, Title, Key Content, Zones), sorted by page number
- Composite sub-pattern zone layouts: nested box notation for 13a-13d sub-patterns using `╔ ╗ ╚ ╝ ║ ═` for outer containers and `┌ ┐ └ ┘ │ ─` for inner zones

### 3.3 Updated Reference Files

| File | Change |
|------|--------|
| `references/quality-checklist.md` | (1) Move current Step 5 (style-guide) checks to Step 6 position. (2) Insert new Step 5 (layout-skeleton) checks at Step 5 position. (3) Delete old Step 6 (wireframes) checks entirely. (4) Update all step number references throughout (resume section, harness improvement examples). |
| `references/state-templates.md` | Replace `wireframes/ [status with count]` deliverable entry with `layout-skeleton.md [status]`; add Step 5 state tracking fields |
| `references/html-wireframe-guide.md` | **Delete** — its only consumer (old Step 6) is removed, so the file is orphaned |
| `references/layout-templates.md` | Keep — still used by Phase 4 (Step 9 test generation) |

### 3.4 Validation Scripts

| Script | Change |
|--------|--------|
| `scripts/validate-content-plan.py` | No change (validates content-plan.md, not affected) |
| `scripts/validate-html-slides.py` | No change (still used in Phase 4 for test-slides validation) |

No new validation scripts for Step 5. Rationale: the layout-skeleton.md ASCII format is human-readable by design; automated parsing of box-drawing characters would be fragile and provide low value relative to cost. The human gate (user reads and confirms text wireframes) is the primary quality mechanism. Mechanical validation is deferred to Phase 4 where HTML output can be reliably parsed by `validate-html-slides.py`.

---

## 4. Step 5 Full Specification

### Step 5: Layout Skeleton Review

**Phase:** 2 (Design)
**Preceded by:** Step 4 (Page Types & Layout System) — confirmed
**Followed by:** Step 6 (Visual Style Direction)

**AI Behavior:**

1. Read confirmed `layout-system.md` (page type assignments from Step 4).
2. Read `references/layout-skeleton-format.md` for ASCII wireframe conventions and per-type zone templates.
3. Read `references/layout-types.md` for zone ratio references to inform zone sizes in text diagrams.
4. Read `outline.md` for section structure and page purposes.
5. Generate **overview table** — one row per page with: page number, page type, title, key content summary (one phrase), zone count.
6. Present overview table to user. **Gate 1:** User confirms overall rhythm, page order, and content scope.
7. After overview approval, generate **per-page text wireframes** batched by section (5-8 pages per batch).
8. For each page:
   - Draw ASCII box diagram reflecting the page type's standard zone layout.
   - Label each zone with type, one-line content summary, and visual weight.
   - For Composite-Diagram and Pipeline-Flow types: show sub-zone nesting.
9. **Gate 2:** User confirms each batch. Adjustments applied before next batch.
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
┌───────────────────── ... ─────────────────────────┐
│ [zone-type] Content summary               (weight) │
├───────────────────── ... ─────────────────────────┤
│ [zone-type] Content summary               (weight) │
│                                                    │
├───────────────────── ... ─────────────────────────┤
│ [zone-type] Content summary               (weight) │
└───────────────────── ... ─────────────────────────┘

## Slide 2: ...
```

**Gate:** Overview confirmed + all per-page batches confirmed. Phase 2 Step 5 complete.

**State Update:** Update `deckdone-state.md` — Phase 2, Step 5 complete.

**Validation:** Run `references/quality-checklist.md` Section 2.2 (new Step 5 checks).

---

## 5. Step 5 Quality Checklist Items

The following checks will be added to `quality-checklist.md` as Section "Step 5: Layout Skeleton Validation":

- [ ] **Overview table has one row per planned page** — row count matches page count from `outline.md`
- [ ] **Every page uses a valid page type** matching `layout-system.md` assignments
- [ ] **Every zone is labeled with content type** — recognized type from the type catalog
- [ ] **Every zone has a non-empty content summary** — no zone is blank or "TBD"
- [ ] **Visual weight is annotated per zone** — primary/secondary/auxiliary
- [ ] **Per-type zone count matches layout-types.md defaults** — no page has an unreasonable number of zones
- [ ] **Composite-Diagram and Pipeline-Flow pages show sub-zone structure**

---

## 6. What Is NOT Changing

- Step 9 (Test Generation) retains its role as the first visual/HTML output checkpoint
- `references/layout-templates.md` remains used by Phase 4 for HTML generation
- `scripts/validate-html-slides.py` still validates test-slides in Phase 4
- The content-plan.md format (Step 7) is unchanged
- Narrative frameworks, style presets, audience analysis references are unaffected
- The state file and trace file mechanisms are unchanged (only step numbers shift)
- **Cross-conversation resume migration:** In-flight sessions created under old step numbering (e.g., "Phase 2, Step 5 complete" meaning Visual Style Direction) will misalign with the new numbering. Mitigation: update the quality-checklist.md resume section example from "Step 6: wireframes" to "Step 5: layout skeleton". A state file version field is not added at this time — users should start fresh sessions or manually reconcile. This is an acceptable trade-off since the skill is pre-1.0 and has no production users with persistent state.
