# Quality Validation Checklist (Steps 9–12)

> Per-step binary pass/fail checks for DeckDone build deliverables.
> Every checkbox must be answered **YES** or **NO** before advancing.

---

| Step | Deliverable | Section |
|------|-------------|---------|
| 9 | test SVGs | [Step 9](#step-9-test-svg-validation) |
| 10 | batch SVGs | [Step 10](#step-10-batch-svg-validation) |
| 11 | final PPTX | [Step 11](#step-11-final-pptx-validation) |
| 12 | presentation guide | [Step 12](#step-12-presentation-guide-validation) |

---

## Step 9: Test SVG Validation

- [ ] **No text overflow in any test SVG** — all text within its zone
- [ ] **No element overlap detected** — no two content zones overlap
- [ ] **All icons render correctly** — no broken `<use data-icon>` placeholders
- [ ] **Adequate contrast between text and background**
- [ ] **Style is consistent across different page types** — same palette, fonts, spacing
- [ ] **SVG compliance check passed** — validate-svg-slides.py exits 0
- [ ] **All viewBox dimensions are correct** — `0 0 1280 720`

## Step 10: Batch SVG Validation

- [ ] **All planned pages present** — SVG count matches outline.md
- [ ] **No missing content from content-plan.md** — every zone's text appears
- [ ] **Consistent style across all pages** — no drift in colors, fonts, spacing
- [ ] **Cross-page visual identity is uniform** — all pages look like they belong together
- [ ] **Design context was locked before generation** — global tokens documented
- [ ] **Section transitions feel natural**

## Step 11: Final PPTX Validation

- [ ] **PPTX opens without errors** — no corruption warnings
- [ ] **All shapes are editable** — native DrawingML shapes, not images
- [ ] **Text sizes are readable** — no body text below 10pt, no heading below 14pt
- [ ] **Color palette is uniform** — every page uses colors from style-guide.md
- [ ] **No blank or partially rendered slides**
- [ ] **Narrative flow is coherent** — sequential read supports Key Message

## Step 12: Presentation Guide Validation

- [ ] **presentation-guide.md exists and is non-empty**
- [ ] **Module 1 (Overview) includes required fields** — Core Message, Audience, Total Slides, Duration
- [ ] **Module 3 (Slide Key Points) has one row per slide** — matches outline.md
- [ ] **Module 4 (Speaking Notes) includes at least 2 potential Q&A items**
- [ ] **Total time allocation is reasonable** — within ±10% of Suggested Duration

---

## Harness Improvement Protocol

When a check fails:

1. **Document** in `harness-improvements.md`: step, check, expected vs actual
2. **Root cause**: harness gap vs execution error
3. **If harness gap**: update svg-constraints.md, layout-templates.md, or validate-svg-slides.py
4. **Add a new check** if failure type was not covered
5. **Verify fix prevents recurrence**
