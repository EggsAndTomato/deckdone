# Presentation Guide (Step 12) Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Step 12 to the DeckDone workflow that generates a concise `presentation-guide.md` after PPT completion.

**Architecture:** Add a new step (Step 12) at the end of Phase 4 in SKILL.md, update the quality checklist with validation checks, and update state templates to track the new deliverable. No new files created — the guide is generated at runtime.

**Tech Stack:** Markdown editing only. No code changes (no new scripts needed for a Markdown deliverable).

**Spec:** `docs/superpowers/specs/2026-04-17-presentation-guide-design.md`

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `skills/deckdone/SKILL.md` | Modify | Add Step 12 section, update Workflow table, update Deliverable Files table, update Step 11 state update text |
| `skills/deckdone/references/quality-checklist.md` | Modify | Add Step 12 validation section |
| `skills/deckdone/references/state-templates.md` | Modify | Add `presentation-guide.md` to Deliverable Status list |

---

## Chunk 1: All Tasks

### Task 1: Update SKILL.md — Workflow at a Glance table

**Files:**
- Modify: `skills/deckdone/SKILL.md:21`

- [ ] **Step 1: Update Phase 4 row in the Workflow at a Glance table**

Change the Phase 4 row from `Steps 9–11` to `Steps 9–12` and update the Goal column.

**Current content (line 21):**
```markdown
| 4 | Implementation | Batch execution | 9–11 | Generate PPTX with quality assurance |
```

**New content:**
```markdown
| 4 | Implementation | Batch execution | 9–12 | Generate PPTX with quality assurance and presentation guide |
```

- [ ] **Step 2: Verify the edit**

Read `skills/deckdone/SKILL.md` lines 16-22 and confirm the table shows `9–12` for Phase 4.

---

### Task 2: Update SKILL.md — Deliverable Files table

**Files:**
- Modify: `skills/deckdone/SKILL.md:91`

- [ ] **Step 1: Add presentation-guide.md row after final.pptx**

**Current content (line 91):**
```markdown
| `final.pptx` | 4 | 11 | Final reviewed presentation |
```

**New content (insert after line 91):**
```markdown
| `final.pptx` | 4 | 11 | Final reviewed presentation |
| `presentation-guide.md` | 4 | 12 | Speaker's quick-reference guide |
```

- [ ] **Step 2: Verify the edit**

Read `skills/deckdone/SKILL.md` lines 89-96 and confirm the new row is present.

---

### Task 3: Update SKILL.md — Step 11 State Update text

**Files:**
- Modify: `skills/deckdone/SKILL.md:530`

- [ ] **Step 1: Change Step 11 state update from "all phases complete" to "Phase 4, Step 11 complete"**

**Current content (line 530):**
```markdown
**State Update:** Update `deckdone-state.md` — all phases complete.
```

**New content:**
```markdown
**State Update:** Update `deckdone-state.md` — Phase 4, Step 11 complete.
```

- [ ] **Step 2: Verify the edit**

Read `skills/deckdone/SKILL.md` lines 528-532 and confirm the text says `Phase 4, Step 11 complete`.

---

### Task 4: Add Step 12 section to SKILL.md

**Files:**
- Modify: `skills/deckdone/SKILL.md:531-532` (insert between Step 11 closing `---` and Harness Engineering Principles)

- [ ] **Step 1: Insert Step 12 section**

Insert the following content **after line 532** (the `---` that closes Step 11) and **before line 534** (the `## Harness Engineering Principles` heading):

```markdown

### Step 12: Presentation Guide

Goal: Generate a concise quick-reference guide for the presenter. This is especially valuable when the deck creator and presenter are different people.

**AI Behavior:**

1. Read the following confirmed deliverables:
   - `brief.md` (purpose, audience, framework, density, scale)
   - `outline.md` (section structure, page count)
   - `content-plan.md` (per-page content, visual narrative paths)
   - `style-guide.md` (visual style)
   - `layout-skeleton.md` (page layout overview)
2. Generate `presentation-guide.md` following the 4-module structure below.
3. Determine emphasis levels (★ Key / Normal / ⏭ Skippable) based on each page's contribution to the Key Message from `brief.md`.
4. Calculate time allocation from `brief.md` Scale field (total minutes ÷ total pages, weighted by emphasis). If Scale has no time estimate, default to 1.5 minutes per page.
5. Predict 2–3 likely audience questions based on content gaps or contentious points in the material.
6. Write in the user's preferred language (same language used throughout the session).
7. Present to user for confirmation. Allow edits.

**Deliverable:** `presentation-guide.md`

```markdown
# Presentation Guide: [Presentation Title]

## Overview

- **Topic:** [topic from brief.md]
- **Core Message:** [Key Message — one sentence]
- **Audience:** [one-sentence profile]
- **Total Slides:** [N] | **Suggested Duration:** [X minutes]
- **Narrative Framework:** [name] — [1–2 sentence reasoning]

## Design Rationale

**Narrative Logic:** [3–5 sentences: why chapters are ordered this way, how the story builds]

**Section Intentions:**

| Section | Title | What the audience should conclude |
|---------|-------|-----------------------------------|
| 1 | [title] | [one sentence] |
| 2 | [title] | [one sentence] |
| ... | ... | ... |

**Key Design Decisions:**
- [Decision 1: e.g., "Timeline layout used for Section 3 to emphasize progression"]
- [Decision 2: e.g., "Data-Chart pages placed after arguments for evidence anchoring"]
- [Decision 3: e.g., "Warm palette chosen for external client audience — builds trust"]

## Slide Key Points

| # | Title | Key Points | Emphasis | Time |
|---|-------|-----------|----------|------|
| 1 | [title] | [1–2 keywords] | Normal | 0.5min |
| 2 | [title] | [1–2 keywords] | ★ Key | 2min |
| ... | ... | ... | ... | ... |

> ★ Key = critical for core message — slow down, elaborate | ⏭ = skippable if time is short

## Speaking Notes

**Opening:** [1–2 sentences: how to hook the audience in the first 30 seconds]

**Key Emphasis:**
- Slides [X, Y, Z]: [what to emphasize and why]
- Slide [N]: [specific caution, e.g., "chart needs guided interpretation"]

**Potential Q&A:**
1. **[Predicted question]** → [key points for the answer]
2. **[Predicted question]** → [key points for the answer]
3. **[Predicted question]** → [key points for the answer]

**Time Management:**
- Short on time: Skip slides [list by #]
- Extra time: Expand on slides [list by #]
```

**Gate:** User confirms presentation guide content.

**State Update:** Update `deckdone-state.md` — all phases complete.

---
```

- [ ] **Step 2: Verify the edit**

Read `skills/deckdone/SKILL.md` lines 530-600 and confirm:
- Step 12 heading is present
- 4-module template is intact
- Gate and State Update lines are present
- Harness Engineering Principles section follows after

---

### Task 5: Update quality-checklist.md — Add Step 12 validation

**Files:**
- Modify: `skills/deckdone/references/quality-checklist.md:21` and insert new section

- [ ] **Step 1: Update Table of Contents — add Step 12 row**

**Current content (line 21):**
```markdown
| 11 | `final.pptx` | [Step 11: Final Validation](#step-11-finalpptx-validation) |
```

**New content (insert after line 21):**
```markdown
| 11 | `final.pptx` | [Step 11: Final Validation](#step-11-finalpptx-validation) |
| 12 | `presentation-guide.md` | [Step 12: Presentation Guide Validation](#step-12-presentation-guidemd-validation) |
```

- [ ] **Step 2: Add Step 12 validation section**

Insert the following content **after line 113** (the last Step 11 checklist item `- [ ] **Narrative flow is coherent...`) and **before line 114** (the blank line before `---`):

```markdown

## Step 12: presentation-guide.md Validation

- [ ] **presentation-guide.md exists and is non-empty** — file is present in the project directory and contains content
- [ ] **Module 1 (Overview) includes required fields** — Core Message, Audience, Total Slides, Suggested Duration, and Narrative Framework are all present
- [ ] **Module 3 (Slide Key Points) has one row per slide** — row count matches the page count from `outline.md`
- [ ] **Module 4 (Speaking Notes) includes at least 2 potential Q&A items** — audience questions with answer key points
- [ ] **Total time allocation is reasonable** — sum of per-slide times falls within ±10% of the Suggested Duration
```

- [ ] **Step 3: Verify both edits**

Read `skills/deckdone/references/quality-checklist.md` and confirm:
- Table of Contents has Step 12 row
- Step 12 validation section exists with 5 checklist items
- Harness Improvement Protocol section still follows after

---

### Task 6: Update state-templates.md — Add presentation-guide.md to Deliverable Status

**Files:**
- Modify: `skills/deckdone/references/state-templates.md:37-38`

- [ ] **Step 1: Add presentation-guide.md line after final.pptx**

**Current content (line 38):**
```markdown
- final.pptx [status]
```

**New content:**
```markdown
- final.pptx [status]
- presentation-guide.md [status]
```

- [ ] **Step 2: Verify the edit**

Read `skills/deckdone/references/state-templates.md` lines 29-42 and confirm the new line is present.

---

### Task 7: Final verification

- [ ] **Step 1: Check SKILL.md line count**

Run: `wc -l skills/deckdone/SKILL.md`
Expected: ~593 lines (558 original + ~35 new). Must be under 600.

- [ ] **Step 2: Verify Step 12 is well-formed**

Read `skills/deckdone/SKILL.md` from Step 12 heading to the next major section. Confirm:
- Step 12 heading, AI Behavior, Deliverable, Gate, State Update are all present
- The 4-module template is complete (Overview, Design Rationale, Slide Key Points, Speaking Notes)
- No TODO or placeholder text

- [ ] **Step 3: Verify all files are consistent**

Grep all 3 modified files for `presentation-guide` and confirm each reference is correct and complete.

- [ ] **Step 4: Commit**

```bash
git add skills/deckdone/SKILL.md skills/deckdone/references/quality-checklist.md skills/deckdone/references/state-templates.md
git commit -m "feat: add Step 12 Presentation Guide to DeckDone workflow"
```
