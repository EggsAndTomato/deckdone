# Quality Validation Checklist (Steps 1-5)

> Per-step binary pass/fail checks for DeckDone planning deliverables.
> Every checkbox must be answered **YES** or **NO** before advancing to the next step.

---

| Step | Deliverable | Section |
|------|-------------|---------|
| 1 | `brief.md` | [Step 1](#step-1-briefmd-validation) |
| 2 | `materials/` | [Step 2](#step-2-materials-validation) |
| 3 | `outline.md` | [Step 3](#step-3-outlinemd-validation) |
| 4 | `layout-system.md` | [Step 4](#step-4-layout-systemmd-validation) |
| 5 | `wireframes.html` + `content-plan.md` + `layout-skeleton.md` | [Step 5](#step-5-content-wireframe-validation) |

---

## Step 1: brief.md Validation

- [ ] **Purpose field is populated** and matches one of the defined types (Work report, Proposal, Knowledge sharing, Project kickoff, Summary, Other)
- [ ] **Key Message is exactly one sentence** — no compound clauses, no ambiguity
- [ ] **Audience profile includes all three dimensions**: role level, familiarity, AND tendency
- [ ] **Narrative framework is selected with reasoning** — framework name stated with one-line justification
- [ ] **Scale includes estimated page count** with a min-max range
- [ ] **Density level is specified** with one-sentence reasoning

## Step 2: materials/ Validation

- [ ] **`materials/00-index.md` exists** with complete source listing
- [ ] **Each source has topic tags and scenario annotations**
- [ ] **Key data points are extracted and documented**
- [ ] **No source file is missing from the index**
- [ ] **Web-sourced materials have source URL annotated** in their index entry

## Step 3: outline.md Validation

- [ ] **Page count is within the declared Scale range** from `brief.md`
- [ ] **Every page has a purpose and key point annotated**
- [ ] **Every section has a core argument**
- [ ] **Section page counts sum to the total declared pages**
- [ ] **Narrative framework structure is visible in the outline**

## Step 4: layout-system.md Validation

- [ ] **Every page is assigned a valid page type** from the 12 defined types
- [ ] **No undefined or unrecognized page types**
- [ ] **Page type distribution is reasonable** — variety reflects content diversity
- [ ] **Composite-Diagram pages have sub-zone descriptions**

## Step 5: Content Wireframe Validation

- [ ] **`wireframes.html` exists and is openable in a browser**
- [ ] **Auto-refresh script is present** — browser reloads within 3 seconds of file change
- [ ] **Thumbnail navigation bar present** — clickable links for all slides
- [ ] **All planned pages are present** — page count matches `outline.md`
- [ ] **Every page uses a valid page type** matching `layout-system.md`
- [ ] **Every zone has real content** — no "TBD", "placeholder", or "Lorem ipsum"
- [ ] **Chart zones have complete specs** — chart type, title, axes, key data points
- [ ] **Visual weight is annotated per zone** — primary / secondary / auxiliary
- [ ] **No visual styling applied** — no colors, no decorative fonts, no gradients
- [ ] **`content-plan.md` exported** with per-zone content following mandatory template
- [ ] **`layout-skeleton.md` exported** with overview table and per-page zone summary
- [ ] **`content-plan.md` passes validation**: `python scripts/validate-content-plan.py content-plan.md`

---

## Harness Improvement Protocol

When a check fails:

1. **Document** in `harness-improvements.md`: step, check, expected vs actual
2. **Root cause**: harness gap (missing validation) vs execution error
3. **If harness gap**: update the relevant reference file or validation script
4. **Add a new check** if the failure type was not already covered
5. **Verify fix prevents recurrence** — re-run and confirm

---

## Cross-Conversation Resume Validation

When resuming from `deckdone-state.md`:

1. [ ] State file exists, parseable, not corrupted
2. [ ] Current phase and step clearly stated
3. [ ] All completed deliverable files exist on disk
4. [ ] Context Summary is under 500 words and includes Key Message
5. [ ] No pending items conflict with current state
6. [ ] Trace file has entries for all completed steps
