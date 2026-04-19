---
name: deckdone
description: "Structured workflow for creating large, complex presentations (15-40 slides) from scratch. Orchestrates content discovery, visual design, and production through a phased, gate-controlled process. Use when the user asks to create a presentation, build slides, or make a PPT/PPTX deck — especially for information-dense decks like business plans, product roadmaps, R&D strategy presentations, or any 'visual storytelling' format where the presenter reads the pictures. Handles material collection, narrative framework selection, page-by-page wireframing, detailed content planning, and batch PPTX generation via the pptx skill."
---

# DeckDone — Presentation Creation Workflow

## Overview

Creating large, information-dense presentations (15–40 slides) is a multi-hour process requiring expertise in content structure, visual design, and PowerPoint tooling. Existing AI tools either produce simple "title + bullets" slides or lack the workflow discipline to maintain consistent quality across complex, multi-page decks.

DeckDone provides a structured, phased workflow that orchestrates content discovery, visual design, and production through a gate-controlled process. The user holds full decision-making authority at every stage.

### Workflow at a Glance

| Phase | Name | Interaction | Steps | Goal |
|-------|------|-------------|-------|------|
| 1 | Discovery | Deep | 1–3 | Understand what to communicate; gather materials |
| 2 | Design | Page-by-page | 4–6 | Define layout skeleton, page types, and visual style |
| 3 | Content | Lightweight | 7–8 | Write exact content for every visual zone |
| 4 | Implementation | Batch execution | 9–12 | Generate PPTX with quality assurance and presentation guide |

### Design Principles

1. **Gate-controlled phases** — Proceed only after user confirmation and verified deliverables.
2. **Progressive interaction depth** — Deep discussion early; lightweight confirmation later; automatic execution at the end.
3. **Content-first, visuals-second** — Determine what to say before deciding how it looks.
4. **Graceful degradation** — Work with minimal dependencies; optional skills enhance the experience.
5. **Density-aware** — Designed for slides with 20–50+ text elements, not simple bullet slides.

---

## Dependencies

See `references/dependencies.md` for the full dependency list (required, optional, Python), degradation behavior, and point-of-use detection rules.

---

## Quick Reference: Deliverable Files

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
| `presentation-guide.md` | 4 | 12 | Speaker's quick-reference guide |
| `deckdone-state.md` | all | all | Progress state file |
| `deckdone-trace.md` | all | all | Execution trace log |
| `harness-improvements.md` | all | all | Harness improvement log |

---

## Cross-Conversation Continuity

Large presentation creation often spans multiple AI conversations. The workflow supports clean resumption without losing decisions or progress.

### Resume Protocol

When the user says "continue my presentation" or "resume deckdone":

1. **Detect** — Look for `deckdone-state.md` in the project directory.
2. **Read state** — Parse current phase, step, and deliverable status.
3. **Read context** — Read the Context Summary section (kept under 500 words).
4. **Read deliverables** — Read the current phase's confirmed deliverable files.
5. **Resume** — Continue from the recorded step.
6. **Inform user** — "Resuming from Phase [X], Step [Y]. Last activity: [date]. Here is where we left off: [brief summary]."

### State Update Protocol

After each gate or phase transition:

1. Update `deckdone-state.md` with:
   - Current phase + step number + date
   - Key decisions made in this session
   - Deliverable files produced or confirmed
   - Pending items for next session
2. Keep Context Summary under 500 words.
3. Always include the brief.md Key Message in Context Summary.
4. Always include the brief.md Density level in Context Summary.
5. Write the state file **before** proceeding to the next step — not after.

---

## Pre-Flight: Environment Check

Before starting Phase 1, run:

    python scripts/check-env.py

If any items fail, resolve them before proceeding. For guided installation:

    python scripts/check-env.py --install          # interactive y/n per item
    python scripts/check-env.py --install --yes    # auto-confirm all (for AI agent use)

---

## Phase 1: Discovery [Deep Interaction]

Goal: Understand what the presentation must communicate and gather the raw materials.

### Step 1: Presentation Brief

**AI Behavior:**

1. Ask one question at a time. Prefer multiple-choice formats:
   - **Purpose:** Work report / Proposal / Knowledge sharing / Project kickoff / Summary / Other
   - **Key Message:** One sentence — "What should the audience remember after this presentation?"
   - **Audience Profile:**
     - Role level (executive / middle management / team / external client / mixed)
     - Subject familiarity (expert / familiar / general / unfamiliar)
     - Audience tendency (data-driven / story-driven / action-oriented / detail-oriented)
   - **Context:** Formal meeting / Informal sharing / Training / Bidding / Other
   - **Scale:** Estimated page count, time limit
   - **Density:** 演讲辅助型 (presentation) / 演讲详述型 (detailed-presentation) / 阅读型 (reading). Read `references/density-presets.md` for level descriptions. Ask: "Will the audience read this deck on their own, or will you present it live?"
2. Read `references/narrative-frameworks.md`. Recommend 1–2 frameworks based on purpose + audience.
3. Discuss framework selection and methodology reasoning with the user.
4. Write `brief.md`.

**Deliverable:** `brief.md`

```markdown
# Presentation Brief
## Purpose: [purpose]
## Key Message: [one sentence]
## Audience: [profile + tendencies]
## Context: [scenario]
## Scale: [estimated pages, time limit]
## Density: [presentation | detailed-presentation | reading]
## Density Reasoning: [one sentence]
## Narrative Framework: [chosen framework + reasoning]
## Methodology: [why this approach works for this audience]
```

**Gate:** User confirms `brief.md` content is accurate.

**State Update:** Update `deckdone-state.md` — Phase 1, Step 1 complete.

**Validation:** Run `references/quality-checklist.md` Section 1.1.

---

### Step 2: Material Collection

**AI Behavior:**

1. Ask the user for reference materials. Suggest possible types:
   - Company documents / Personal work records / Industry reports / Policy documents / Data spreadsheets / Other
2. For each file provided, detect format and extract:
   - `.pdf` → Run `python scripts/extract-pdf.py <file> --output materials/`
     - If text-layer detected: text extracted automatically
     - If image-type: pages rendered as PNG, follow manifest instructions for visual extraction
   - If `extract-pdf.py` is unavailable, fall back to pdf skill or ask user to paste text content
   - `.docx` → use docx skill; if unavailable, ask user to paste text content
   - `.xlsx` / `.csv` → use xlsx skill; if unavailable, ask user to provide data as text
   - Plain text / URL → read directly
3. Organize extracted content by topic. Extract key data points, quotes, and cases.
4. Tag each material with applicable slide scenarios.

**Deliverable:** `materials/` directory

```
materials/
├── 00-index.md          # Source index (origin + topic + applicable scenarios)
├── 01-topic-a.md        # Topic-classified extracted content
├── 02-topic-b.md
└── ...
```

**Gate:** User confirms material index is complete.

**State Update:** Update `deckdone-state.md` — Phase 1, Step 2 complete.

**Validation:** Run `references/quality-checklist.md` Section 1.2.

---

### Step 3: Content Outline

**AI Behavior:**

1. Build narrative skeleton based on brief + materials.
2. Read `references/narrative-frameworks.md` for framework-specific guidance on section structure.
3. Generate topic tree (2–3 levels). Annotate core arguments for each section.
4. Estimate page count per section and total page count.
5. Discuss and iterate with the user (may require multiple rounds).

**Deliverable:** `outline.md`

```markdown
# Presentation Outline
## Framework: [name]
## Total Pages: [estimated N]

### Section 1: [Title] (2 pages)
- Page 1: [purpose] — key point: ...
- Page 2: [purpose] — key point: ...

### Section 2: [Title] (4 pages)
...
```

**Gate:** User confirms outline structure and page count. Phase 1 complete.

**State Update:** Update `deckdone-state.md` — Phase 1, Step 3 complete.

**Validation:** Run `references/quality-checklist.md` Section 1.3.

---

## Phase 2: Design [Page-by-page Confirmation]

Goal: Define the visual system and layout for each page.

### Step 4: Page Types and Layout System

**AI Behavior:**

1. Read `references/layout-types.md` for page type definitions, layout rules, and content density limits. Predefined page types:
   - **Cover** — Title + subtitle + date/author
   - **Agenda** — Section list with numbering
   - **Section Divider** — Section title + brief description
   - **Content-Text** — Title + bullet points or paragraphs
   - **Content-TwoCol** — Title + left/right split
   - **Data-Chart** — Title + chart + interpretation text
   - **Quote** — Large quote + attribution
   - **Timeline** — Events/milestones display
   - **Comparison** — Side-by-side A vs B
   - **Closing** — Summary + call to action
   - **Composite-Diagram** — Complex nested-box layout (architecture diagrams, hierarchy charts, agent maps)
   - **Pipeline-Flow** — Process pipeline visualization
2. Assign a page type to each page based on the outline.
3. For Composite-Diagram and Pipeline-Flow types: identify sub-layout zones within the page and list pre-render element needs (icons, gradients, connectors).
4. Confirm page type assignments with the user.

**Deliverable:** `layout-system.md`

```markdown
# Layout System
## Defined Page Types: [list of used types]

## Page Assignment:
- Page 1: Cover
- Page 2: Agenda
- Page 3: Section Divider (Section 1)
- Page 4–5: Composite-Diagram
- Page 6: Data-Chart
- Page 7: Timeline
...

## Pre-render Elements:
- Icons needed: [list]
- Gradients needed: [list]
- Connectors/arrows: [list]
```

**Gate:** User confirms page type assignments.

**State Update:** Update `deckdone-state.md` — Phase 2, Step 4 complete.

**Validation:** Run `references/quality-checklist.md` Section 2.1.

---

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

1. Read `references/style-presets.md` (15–20 style presets). If deckdone-style skill is available, read its `references/enhanced-presets.md` instead. Also read `references/decoration-guide.md`.
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

---

## Phase 3: Content [Lightweight Confirmation]

Goal: Write the exact content for every visual zone on every page.

### Step 7: Detailed Content Plan

**AI Behavior:**

1. Based on confirmed outline + layout-system + layout-skeleton + style-guide, generate a detailed content spec per page. Read the density level from `brief.md`. Read the corresponding content capacity limits from `references/density-presets.md`. Use these as Max Length values for each zone instead of the defaults in `layout-types.md`. If deckdone-style is available, read `references/icon-catalog.md` and assign icon names to zones per decoration-guide rules.
2. Organize content by **visual zone** (not by title + body). When deckdone-style is available, add `- Icon: [name from icon-catalog.md or "None"]` to each zone. For Cover and Section Divider slides, add `- Illustration: [unDraw slug or "None"]`.
3. Each zone annotated with: content type, text volume, visual weight (primary / secondary / auxiliary).
4. Include a pre-render element list and chart data specifications for placeholder areas.
5. For visual storytelling presentations, annotate each page's **visual narrative path** (viewer eye flow).
6. Display in batches by section.

**Deliverable:** `content-plan.md`

Mandatory template for each slide:

```markdown
## Slide [N]: [Title]
- Page Type: [MUST match a type from layout-system.md]
- Total Zones: [count]
- Pre-render Elements: [list or "None"]
- Visual Narrative Path: [eye flow description]

### Zone A: [name]
- Type: [title | body | label | data | icon | chart]
- Content: "[EXACT text — required, cannot be empty]"
- Max Length: [character count, from layout-patterns.md]
- Visual Weight: [primary | secondary | auxiliary]
- Pre-render: [element name or "None"]

### Zone B: [name]
- Type: [title | body | label | data | icon | chart]
- Content: "[EXACT text]"
- Max Length: [character count]
- Visual Weight: [primary | secondary | auxiliary]
- Pre-render: [element name or "None"]

### Acceptance Criteria
- [ ] All zones have content within max length
- [ ] All pre-render elements listed in layout-system
- [ ] Chart data complete with values and labels (if applicable)
- [ ] No zone has placeholder or TBD content
```

**Gate:** User confirms all page content plans.

**State Update:** Update `deckdone-state.md` — Phase 3, Step 7 complete.

**Validation:** Run `references/quality-checklist.md` Section 3.1. Optionally run `python scripts/validate-content-plan.py content-plan.md`.

---

### Step 8: User Content Confirmation

- Allow the user to modify specific copy, data, or zone assignments.
- After confirmation, proceed to Phase 4.

**State Update:** Update `deckdone-state.md` — Phase 3 complete.

---

## Phase 4: Implementation [Batch Execution]

Goal: Produce the final PPTX file with quality assurance. Phase 4 makes **zero creative decisions** — every detail comes from the confirmed content plan.

### Step 9: Test Generation

**AI Behavior:**

1. Select one page per layout type as test samples.
2. For each test page, execute the full pipeline:
   a. Pre-render elements using Sharp (icons→PNG, gradients→PNG). If deckdone-style is available, run `fetch-icon.py` for each assigned icon and `fetch-illustration.py` for cover/divider illustrations.
   b. Create HTML file with actual content + confirmed style. Use templates from `references/layout-templates.md` (or `references/layout-templates-decorated.md` from deckdone-style if available). Read the density level from `brief.md` and the corresponding spacing parameters from `references/density-presets.md`. Apply padding, line-height, and gap values. Choose font sizes dynamically based on actual content amount within spacing constraints, respecting the minimum readable font floor.
   c. Call `html2pptx()` from the pptx skill to convert to PPTX.
   d. Generate thumbnail: `python scripts/thumbnail.py output.pptx preview --slides N`
3. User reviews thumbnails for:
   - Layout accuracy against layout-skeleton.md
   - Text cutoff or overflow
   - Color block and spacing reasonableness
   - Information density readability
4. If unsatisfied, adjust HTML and regenerate (max 3 rounds per page).
5. Lock template parameters for each page type.

**Deliverable:** `test-slides/` directory + `template-params.md`

**Gate:** User confirms all test page visuals.

**State Update:** Update `deckdone-state.md` — Phase 4, Step 9 complete.

**Validation:** Run `references/quality-checklist.md` Section 4.1. Optionally run `python scripts/validate-html-slides.py test-slides/`.

---

### Step 10: Batch Generation

**AI Behavior:**

1. Read locked template parameters from `template-params.md`.
2. Generate in section chunks (5–8 pages per chunk) to avoid context overflow.
3. Per chunk:
   a. Pre-render elements. If deckdone-style is available, run `fetch-icon.py` and `fetch-illustration.py` for icons and illustrations.
   b. Generate HTML files. Apply density-level spacing from `references/density-presets.md`. Choose font sizes dynamically per slide based on actual content volume. If deckdone-style is available, use `references/layout-templates-decorated.md`.
   c. `html2pptx()` conversion.
   d. Generate chunk thumbnails for intermediate check.
4. Merge all chunks into `output.pptx`.
5. For information-dense pages (50+ text blocks), run a **space competition check**:
   - Verify no text is cut off.
   - Verify no element overlap.
   - Verify adequate margins.

**Deliverable:** `output.pptx`

**State Update:** Update `deckdone-state.md` — Phase 4, Step 10 complete.

**Validation:**
- Run `python scripts/validate-html-slides.py test-slides/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md test-slides/`
```

---

### Step 11: Final Quality Review

**AI Behavior:**

1. Generate thumbnail grid: `python scripts/thumbnail.py output.pptx final-review --cols 4`
2. Read `references/quality-checklist.md` for the complete review checklist.
3. Check each item:
   - **Consistency** — All pages follow the same style (palette, fonts, spacing).
   - **Completeness** — No missing pages or content zones.
   - **Readability** — Text sizes sufficient, contrast adequate.
   - **Narrative flow** — Page transitions feel natural.
4. Fix problem pages.
5. Generate final version.

**Deliverable:** `final.pptx`

**Validation:**
- Run `python scripts/validate-html-slides.py test-slides/ --outline outline.md`
- Run `python scripts/validate-colors.py style-guide.md test-slides/`

**State Update:** Update `deckdone-state.md` — Phase 4, Step 11 complete.

---

### Step 12: Presentation Guide

Goal: Generate a concise quick-reference guide for the presenter. This is especially valuable when the deck creator and presenter are different people.

**AI Behavior:**

1. Read the following confirmed deliverables:
   - `brief.md` (purpose, audience, framework, density, scale)
   - `outline.md` (section structure, page count)
   - `content-plan.md` (per-page content, visual narrative paths)
   - `style-guide.md` (visual style)
   - `layout-skeleton.md` (page layout overview)
2. Generate `presentation-guide.md` following the 4-module structure in `references/presentation-guide-template.md`.
3. Determine emphasis levels (★ Key / Normal / ⏭ Skippable) based on each page's contribution to the Key Message from `brief.md`.
4. Calculate time allocation from `brief.md` Scale field (total minutes ÷ total pages, weighted by emphasis). If Scale has no time estimate, default to 1.5 minutes per page.
5. Predict 2–3 likely audience questions based on content gaps or contentious points in the material.
6. Write in the user's preferred language (same language used throughout the session).
7. Present to user for confirmation. Allow edits.

**Deliverable:** `presentation-guide.md`

See `references/presentation-guide-template.md` for the 4-module template (Overview, Design Rationale, Slide Key Points, Speaking Notes).

**Gate:** User confirms presentation guide content.

**State Update:** Update `deckdone-state.md` — all phases complete.

---

## Harness Engineering Principles

### Verification Loop Principle

Every phase and step has explicit validation checkpoints. Verification is not deferred to the final output — it happens at each gate. Refer to `references/quality-checklist.md` for the complete per-step checklist. When scripts are available, prefer mechanical enforcement (e.g., `scripts/validate-content-plan.py`, `scripts/validate-html-slides.py`) over AI self-assessment.

### Structured Task Template Principle

The content plan (`content-plan.md`) is the **contract between planning and implementation**. Phase 4 makes zero creative decisions — every detail is specified in the content plan. Structure in, structure out: the more specific the input to Phase 4, the more consistent the output. The implementing AI fills in blanks; it does not make decisions.

### Execution Trace Principle

Append to `deckdone-trace.md` after every step completion, **before** updating `deckdone-state.md`. The trace provides the "why" behind the state file's "what". When resuming across conversations, read both files to understand both current position and reasoning history.

### Harness Improvement Principle

> When a generated slide has quality issues, do NOT just fix the slide. Identify the root cause and update the harness (reference files, templates, validation rules) to prevent this class of error for all future slides.

Every failure is a diagnostic signal. Log improvements in `harness-improvements.md`. Compound improvement: every harness fix applies to all future sessions and all future slides, independent of model improvements.

---

## State File Templates

See `references/state-templates.md` for complete templates for `deckdone-state.md`, `deckdone-trace.md`, and `harness-improvements.md`.
