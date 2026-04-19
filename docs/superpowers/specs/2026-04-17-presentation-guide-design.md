# Design: Presentation Guide (Step 12)

**Date:** 2026-04-17
**Status:** Approved
**Scope:** Add Step 12 to DeckDone workflow — generate a concise presentation guide after PPT completion

---

## Problem

The person creating the PPT is often not the person presenting it. Without context about the design intent, narrative strategy, and emphasis points, a presenter may misdeliver the content — rushing key slides, skipping important context, or failing to connect the narrative arc.

## Solution

Add a Step 12 at the end of Phase 4 that generates a single `presentation-guide.md` file — a concise, practical quick-reference handbook for the presenter.

## Design Decisions

### Decision 1: Placement — Step 12 after Step 11

**Chosen:** New Step 12 in Phase 4, after Final Review (Step 11).
**Alternatives considered:**
- Step 11 sub-step: rejected because Step 11 already has heavy responsibilities (quality check, fixes, final generation)
- Independent skill: rejected because it adds installation/maintenance burden and breaks the integrated workflow
- Split (design rationale in Step 7, speaking guide in Step 11): rejected because a single coherent document is simpler to produce and maintain

**Rationale:** By Step 12, all deliverables are confirmed. The PPT is final. The guide can reference stable content without risk of becoming stale.

### Decision 2: Output format — Markdown

**Chosen:** Single `presentation-guide.md` file.
**Alternatives considered:**
- `.docx` output: rejected as unnecessary dependency on docx skill
- Both formats: rejected as over-engineering for a quick-reference document

**Rationale:** Markdown is lightweight, version-control friendly, and easy to read and edit. Users can convert to other formats if needed.

### Decision 3: Content structure — 4 concise modules

**Chosen:** 4 modules, designed for quick scanning, not long-form reading.
**Alternatives considered:**
- 5-module detailed version (with separate Slide-by-Sheet Speaking Flow and Speaking Strategy): rejected as too verbose
- 3-module minimal version (removing design rationale): rejected because presenters need to understand WHY the deck was built a certain way

**Rationale:** The guide must be scannable in 5-10 minutes. Tables over prose. Keywords over sentences.

### Decision 4: Interaction model — Lightweight confirmation

**Chosen:** AI generates the guide, presents it, user confirms or edits.
**Rationale:** Consistent with Phase 3's interaction depth. The guide is a derivative work (all inputs are confirmed), so heavy iteration is unlikely.

### Decision 5: Language — Follow user's language

**Chosen:** The guide is written in the same language the user has been using throughout the DeckDone session.
**Rationale:** If the deck was created in Chinese, the guide should be in Chinese. No configuration needed.

---

## Document Structure

### Module 1: PPT Overview

```markdown
## PPT Overview

- **Topic:** [presentation topic]
- **Core Message:** [one sentence — the Key Message from brief.md]
- **Audience:** [one-sentence audience profile from brief.md]
- **Total Slides:** [N] | **Suggested Duration:** [X minutes]
- **Narrative Framework:** [name] — [1-2 sentence reasoning for why this framework]
```

Data source: `brief.md`

### Module 2: Design Rationale

```markdown
## Design Rationale

**Narrative Logic:** [3-5 sentences explaining the overall story arc and why chapters are ordered this way]

**Section Intentions:**

| Section | Title | What the audience should conclude |
|---------|-------|-----------------------------------|
| 1 | ... | [one sentence] |
| 2 | ... | [one sentence] |
| ... | ... | ... |

**Key Design Decisions:**
- [Decision 1: e.g., "Used timeline layout for Section 3 to emphasize progression"]
- [Decision 2: e.g., "Data-Chart pages placed after each argument to provide evidence anchoring"]
- [Decision 3: e.g., "Chose warm color palette because audience is external client — builds trust"]
```

Data sources: `brief.md`, `outline.md`, `style-guide.md`

### Module 3: Slide-by-Slide Key Points

```markdown
## Slide Key Points

| # | Title | Key Points | Emphasis | Time |
|---|-------|-----------|----------|------|
| 1 | Cover | [1-2 keywords] | Normal | 0.5min |
| 2 | Agenda | [1-2 keywords] | Normal | 0.5min |
| 3 | ... | [1-2 keywords] | ★ Key | 2min |
| ... | ... | ... | ... | ... |

> ★ = Key slide (critical for the core message) | ⏭ = Skippable if time is short
```

Data source: `content-plan.md`, `layout-skeleton.md`

**Emphasis levels:**
- ★ Key: Critical for supporting the Key Message — slow down, elaborate, repeat
- Normal: Standard coverage
- ⏭ Skippable: Can be dropped if time is short

**Time allocation logic:**
- Total time from `brief.md` Scale field
- Key slides get proportionally more time
- Cover/Agenda/Closing get minimal time
- Section Dividers are transition moments (brief)

### Module 4: Speaking Notes

```markdown
## Speaking Notes

**Opening:** [1-2 sentences on how to start — hook the audience]

**Key Emphasis Points:**
- Slides [X, Y, Z]: [what to emphasize and why]
- Slide [N]: [specific caution — e.g., "chart needs guided interpretation"]

**Potential Q&A:**
1. **[Question]** → [key points for the answer]
2. **[Question]** → [key points for the answer]
3. **[Question]** → [key points for the answer]

**Time Management:**
- Short on time: Skip slides [list]
- Extra time: Expand on slides [list]
```

Data sources: All deliverables (synthesis)

---

## AI Behavior for Step 12

```
### Step 12: Presentation Guide

**AI Behavior:**

1. Read the following confirmed deliverables:
   - brief.md (purpose, audience, framework, density)
   - outline.md (section structure, page count)
   - content-plan.md (per-page content, visual narrative paths)
   - style-guide.md (visual style)
   - layout-skeleton.md (page layout overview)
2. Generate presentation-guide.md following the 4-module structure.
3. Determine emphasis levels based on each page's contribution to the Key Message.
4. Calculate time allocation from brief.md Scale field, weighted by emphasis.
5. Predict 2-3 likely audience questions based on content gaps or contentious points.
6. Present to user for confirmation. Allow edits.

**Deliverable:** presentation-guide.md

**Gate:** User confirms presentation guide content.

**State Update:** Update deckdone-state.md — Phase 4, Step 12 complete.
```

---

## Files to Modify

| File | Change |
|------|--------|
| `skills/deckdone/SKILL.md` | Add Step 12 section (~35 lines). Update Workflow at a Glance table (Phase 4: Steps 9-12). Update Deliverable Files table (add `presentation-guide.md`). |
| `skills/deckdone/references/quality-checklist.md` | Add Step 12 validation section (4-5 checks). |
| `skills/deckdone/references/state-templates.md` | Add `presentation-guide.md` to Deliverable Status list in state template. |
| `AGENTS.md` | No changes needed (no new page types or validation scripts). |

## Validation Checks for Step 12

- [ ] `presentation-guide.md` exists and is non-empty
- [ ] Module 1 (Overview) includes Core Message, Audience, page count, and framework
- [ ] Module 3 (Slide Key Points) has one row per slide matching `outline.md` page count
- [ ] Module 4 (Speaking Notes) includes at least 2 potential Q&A items
- [ ] Total time allocation sums to the declared Suggested Duration ±10%

## Estimated Line Count Impact

- SKILL.md: +35 lines (well within the ~600 line budget)
- quality-checklist.md: +10 lines
- state-templates.md: +1 line

Total: ~46 lines added across 3 files. No new files created (the guide itself is generated at runtime).
