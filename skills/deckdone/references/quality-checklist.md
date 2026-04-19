# Quality Validation Checklist

> Per-step binary pass/fail checks for every deliverable in the DeckDone workflow.
> Every checkbox must be answered **YES** or **NO** before advancing to the next step.

---

## Table of Contents

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
| 12 | `presentation-guide.md` | [Step 12: Presentation Guide Validation](#step-12-presentation-guidemd-validation) |

---

## Step 1: brief.md Validation

- [ ] **Purpose field is populated** and matches one of the defined types (inform, persuade, teach, propose, report, align)
- [ ] **Key Message is exactly one sentence** — no compound clauses, no ambiguity
- [ ] **Audience profile includes all three dimensions**: role level (e.g. C-suite, IC), familiarity (none/basic/expert), AND tendency (skeptic, supporter, neutral)
- [ ] **Narrative framework is selected with reasoning** — the chosen framework name is stated and a one-line justification ties it to the audience/purpose
- [ ] **Scale includes estimated page count** with a min–max range (e.g. 12–15 pages) rather than a single number
- [ ] **Density level is specified** in brief.md — one of `presentation`, `detailed-presentation`, or `reading` is recorded with a one-sentence reasoning

## Step 2: materials/ Validation

- [ ] **`materials/00-index.md` exists** and contains a complete source listing with file references
- [ ] **Each source has topic tags and scenario annotations** — no source is listed without at least one topic tag and one scenario annotation
- [ ] **Key data points are extracted and documented** — quantitative evidence is written out, not just referenced by URL
- [ ] **No source file is missing from the index** — every file in `materials/` is listed in `00-index.md` and vice versa

## Step 3: outline.md Validation

- [ ] **Page count is within the declared Scale range** from `brief.md` — actual outline page total falls inside the min–max
- [ ] **Every page has a purpose and key point annotated** — no page exists without both fields
- [ ] **Every section has a core argument** — a single-sentence statement of what the section proves or conveys
- [ ] **Section page counts sum to the total declared pages** — no off-by-one or unaccounted pages
- [ ] **Narrative framework structure is visible in the outline** — the chosen framework's stages map clearly to sections (e.g. Setup → Confrontation → Resolution)

## Step 4: layout-system.md Validation

- [ ] **Every page is assigned a valid page type** from the 12 defined types in `layout-types.md`
- [ ] **Pre-render elements are listed per page** — or explicitly marked "None" where no pre-rendering is needed
- [ ] **No undefined or unrecognized page types** — every type string exactly matches one of the 12 canonical names
- [ ] **Page type distribution is reasonable** — not all pages use the same type; variety reflects content diversity
- [ ] **Composite-Diagram pages have sub-zone descriptions** — each composite page lists its constituent zones and their roles

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

## Step 7: content-plan.md Validation

- [ ] **Every zone on every page has content** — no zone contains "TBD", "TODO", or is left blank
- [ ] **No zone exceeds the max character limit** defined in `density-presets.md` for the chosen density level and page type
- [ ] **Chart data specs are complete** — every chart zone has values array, labels array, and chart type; non-chart zones are N/A
- [ ] **Pre-render elements are listed per slide** — each slide's pre-render manifest matches `layout-system.md`
- [ ] **Acceptance criteria checkboxes exist for each slide** — at least two binary criteria per slide that define "done"
- [ ] **Visual narrative path is described for each slide** — a one-line note on how the slide advances the overall story
- [ ] **Zone max lengths comply with density preset** — no zone exceeds the capacity limit for the chosen density level from `references/density-presets.md`
- [ ] **All pages that require icons (per decoration-guide.md) have icon names assigned** — no REQUIRED icon slot is blank
- [ ] **Cover and Section Divider pages have illustration slugs or explicit "None"** — no cover/divider is missing the Illustration field

## Step 9: test-slides/ Validation

- [ ] **No text overflow in any test slide** — all text is fully contained within its zone bounding box
- [ ] **No element overlap detected** — no two content zones share overlapping pixels
- [ ] **All images and icons render correctly** — no broken image placeholders, no missing SVG paths
- [ ] **Adequate contrast between text and background** — minimum WCAG AA contrast ratio (4.5:1 for body text)
- [ ] **Style is consistent across different page types** — same palette, same fonts, same spacing rules visible in all slides
- [ ] **Space competition check passed for dense pages** — pages with 4+ zones have no zone smaller than its minimum from `layout-types.md`
- [ ] **All assigned icons are present as files in the test-slides directory** — no broken `<img>` references
- [ ] **Cover and divider illustrations render correctly** — not a broken image placeholder
- [ ] **Icon colors match the style guide palette** — icons use primary/secondary/accent colors, not default black

## Step 10: output.pptx Validation

- [ ] **All planned pages are present in the file** — slide count matches `outline.md` page count exactly
- [ ] **No missing content from content-plan.md** — every zone's text, data, and media from the plan appears in the slide
- [ ] **Consistent style across all pages** — no drift in colors, fonts, or spacing between slides
- [ ] **All pre-render elements are visible** — icons, gradients, and generated images appear correctly rendered (not as blank boxes)
- [ ] **Section transitions feel natural** — no jarring jumps; each slide's opening connects to the previous slide's closing

## Step 11: final.pptx Validation

- [ ] **Thumbnail grid shows consistent visual identity** — when all slides are viewed side by side, they form a coherent visual system
- [ ] **Text sizes are readable** — no body text below 10pt; no heading below 14pt
- [ ] **Color palette is uniform across all pages** — spot-check confirms every page uses only colors from `style-guide.md`
- [ ] **All page numbers and titles are present** where planned — no slide is missing its page number or section title
- [ ] **No blank or partially rendered slides** — every slide has visible content in at least two zones
- [ ] **Narrative flow is coherent from start to finish** — a sequential read-through supports the Key Message from `brief.md`

## Step 12: presentation-guide.md Validation

- [ ] **presentation-guide.md exists and is non-empty** — file is present in the project directory and contains content
- [ ] **Module 1 (Overview) includes required fields** — Core Message, Audience, Total Slides, Suggested Duration, and Narrative Framework are all present
- [ ] **Module 3 (Slide Key Points) has one row per slide** — row count matches the page count from `outline.md`
- [ ] **Module 4 (Speaking Notes) includes at least 2 potential Q&A items** — audience questions with answer key points
- [ ] **Total time allocation is reasonable** — sum of per-slide times falls within ±10% of the Suggested Duration

---

## Harness Improvement Protocol

When a check above fails, follow this protocol to strengthen the system:

1. **Document the failure** in `harness-improvements.md` with:
   - Step number and check that failed
   - Expected result vs. actual result
   - Affected deliverable file(s)

2. **Identify the root cause** — classify into one of:
   - **Harness gap**: missing validation, unclear spec, or absent constraint in a reference file
   - **Execution error**: the spec was clear but the step was implemented incorrectly

3. **If harness gap**: update the relevant reference file or validation script to close the gap. Examples:
   - Add a missing constraint to `layout-types.md`
   - Add a new validation rule to this checklist
   - Clarify ambiguous language in `brief.md` instructions

4. **Add a new check to this checklist** if the failure type was not already covered by an existing checkbox. Number it within the appropriate step section.

5. **Verify the fix prevents recurrence** — re-run the failed step and confirm the same class of error cannot happen again. Log the verification in `harness-improvements.md`.

---

## Cross-Conversation Resume Validation

When resuming work from `deckdone-state.md`, complete ALL of the following before continuing:

1. [ ] **`deckdone-state.md` exists and is parseable** — file is present, valid YAML/Markdown, and not corrupted
2. [ ] **Current phase and step are clearly stated** — the state file names exactly which step to resume from (e.g. "Step 5: layout-skeleton")
3. [ ] **All completed deliverable files actually exist on disk** — cross-reference the state file's "completed" list with actual files; re-run any missing steps
4. [ ] **Context Summary is under 500 words and includes the Key Message** — the summary is compact enough to fit in a single context window and retains the presentation's core thesis
5. [ ] **No pending items conflict with current state** — if `deckdone-state.md` says "awaiting client input" but the user is ready to proceed, update the state before continuing
6. [ ] **`deckdone-trace.md` has entries for all completed steps** — every step marked as complete in the state file has a corresponding trace entry with timestamp and summary

> **If any resume check fails, stop and resolve the discrepancy before proceeding.** Running a step on a corrupted or inconsistent state will produce cascading errors.
