# Quality Validation Checklist (Steps 6-8)

> Per-step binary pass/fail checks for DeckDone build deliverables.
> Every checkbox must be answered **YES** or **NO** before advancing.

---

| Step | Deliverable | Section |
|------|-------------|---------|
| 6 | `style-guide.md` + test SVGs | [Step 6](#step-6-style--test-svg-validation) |
| 7 | batch SVGs + output.pptx | [Step 7](#step-7-batch-svg--quality-validation) |
| 8 | `final.pptx` + presentation guide | [Step 8](#step-8-final-export--presentation-guide-validation) |

---

## Step 6: Style + Test SVG Validation

### Style Guide

- [ ] **Complete palette defined** with at least: primary, secondary, accent, background, and text colors
- [ ] **Typography specified** — heading font family, body font family, and at least three size tiers
- [ ] **Decoration patterns documented** — or explicit "None" statement
- [ ] **Layout rules specified** — margins, spacing, content area ratios

### Test SVGs

- [ ] **No text overflow in any test SVG** — all text within its zone
- [ ] **No element overlap detected** — no two content zones overlap
- [ ] **All icons render correctly** — no broken `<use data-icon>` placeholders
- [ ] **Adequate contrast between text and background**
- [ ] **Style is consistent across different page types** — same palette, fonts, spacing
- [ ] **SVG compliance check passed** — validate-svg-slides.py exits 0
- [ ] **All viewBox dimensions are correct** — `0 0 1280 720`

## Step 7: Batch SVG + Quality Validation

- [ ] **All planned pages present** — SVG count matches outline.md
- [ ] **No missing content from content-plan.md** — every zone's text appears
- [ ] **Consistent style across all pages** — no drift in colors, fonts, spacing
- [ ] **Cross-page visual identity is uniform** — all pages look like they belong together
- [ ] **Design context was locked before generation** — global tokens documented
- [ ] **Section transitions feel natural**
- [ ] **PPTX opens without errors** — no corruption warnings
- [ ] **All shapes are editable** — native DrawingML shapes, not images
- [ ] **Text sizes are readable** — no body text below 10pt, no heading below 14pt
- [ ] **Color palette is uniform** — every page uses colors from style-guide.md
- [ ] **No blank or partially rendered slides**

### Native Shape Diagram Checks (Content-Diagram pages)

- [ ] **All diagram-data items are present** — every node from diagram-data/*.md appears as a shape on the slide
- [ ] **No text overflow** — all text fits within its shape boundaries
- [ ] **Color consistency** — diagram colors match style-guide.md palette
- [ ] **Layout type is correct** — the diagram visual matches the DeckDone diagram type

## Step 8: Final Export + Presentation Guide Validation

### PPTX

- [ ] **final.pptx opens without errors**
- [ ] **All slides render correctly** — no visual glitches

### Presentation Guide

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
