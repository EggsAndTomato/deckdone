---
name: deckdone-plan
description: "Structured workflow for planning presentation content (15-40 slides). Orchestrates content discovery, visual design direction, and detailed content planning through a phased, gate-controlled process. Produces editable markdown deliverables: brief, outline, layout system, wireframes, style guide, and content plan. Use when the user needs to plan a presentation — the output can be used by deckdone-build, PPT Master, or manual PPT creation."
---

# DeckDone Plan — Presentation Content Planning Workflow

## Overview

This skill handles **content planning only** — Steps 1 through 8 of the DeckDone workflow. It produces a set of editable markdown files that fully describe what a presentation should contain, how it should be structured, and what visual style it should use. These deliverables can be consumed by **any** PPT generation tool: `deckdone-build`, PPT Master, manual PowerPoint creation, or any other builder.

The user may freely edit any deliverable file between planning and building. The planning phase makes no assumptions about the build tool.

### Workflow at a Glance

| Phase | Name | Interaction | Steps | Goal |
|-------|------|-------------|-------|------|
| 1 | Discovery | Deep | 1–3 | Understand what to communicate; gather materials |
| 2 | Design | Page-by-page | 4–6 | Define layout skeleton, page types, and visual style |
| 3 | Content | Lightweight | 7–8 | Write exact content for every visual zone |

### Design Principles

1. **Gate-controlled phases** — Proceed only after user confirmation and verified deliverables.
2. **Progressive interaction depth** — Deep discussion early; lightweight confirmation later.
3. **Content-first, visuals-second** — Determine what to say before deciding how it looks.
4. **Density-aware** — Designed for slides with 20–50+ text elements, not simple bullet slides.

---

## Dependencies

**Required:**
- This skill (`deckdone-plan`) and its `references/` directory

**Optional:**
- `pdf` skill — for extracting text from PDF source materials
- `docx` skill — for extracting text from DOCX source materials
- `xlsx` skill — for extracting data from spreadsheet source materials
- Web fetch capability — for collecting materials from URLs

**Python:**
- stdlib only — `scripts/validate-content-plan.py` requires no third-party packages

---

## Quick Reference: Deliverable Files

| File | Phase | Step | Description |
|------|-------|------|-------------|
| `brief.md` | 1 | 1 | Presentation brief |
| `materials/` | 1 | 2 | Collected and classified source materials |
| `outline.md` | 1 | 3 | Content outline with page estimates |
| `layout-system.md` | 2 | 4 | Page type assignments per slide |
| `layout-skeleton.md` | 2 | 5 | Text wireframes with zone layout and content summaries |
| `style-guide.md` | 2 | 6 | Visual style definition (color + typography) |
| `content-plan.md` | 3 | 7 | Detailed content per visual zone |
| `deckdone-state.md` | all | all | Progress state file |
| `deckdone-trace.md` | all | all | Execution trace log |

---

## Cross-Conversation Continuity

Large presentation planning often spans multiple AI conversations. The workflow supports clean resumption without losing decisions or progress.

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

---

### Step 2: Material Collection

**AI Behavior:**

1. Ask the user for reference materials. Suggest possible types:
   - Company documents / Personal work records / Industry reports / Policy documents / Data spreadsheets / Other
2. For each file provided, detect format and extract:
   - `.pdf` → use pdf skill; if unavailable, ask user to paste text content
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
3. For Composite-Diagram and Pipeline-Flow types: identify sub-layout zones within the page.
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
```

**Gate:** User confirms page type assignments.

**State Update:** Update `deckdone-state.md` — Phase 2, Step 4 complete.

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

---

### Step 6: Visual Style Direction

**AI Behavior:**

1. Read `references/style-presets.md` for color and typography presets (15–20 style presets).
2. Recommend 2–3 styles based on presentation purpose + audience profile.
3. Show style previews: color palette + typography + decoration characteristics.
4. User selects a style or fine-tunes parameters.

**Deliverable:** `style-guide.md`

```markdown
# Style Guide
## Palette: [primary/secondary/accent/background/text — hex values]
## Typography: [heading font + body font + size scale]
## Decoration: [border style / shape patterns / background treatment]
## Layout Rules: [margins / spacing / content area ratios]
```

**Gate:** User confirms style direction. Phase 2 complete.

**State Update:** Update `deckdone-state.md` — Phase 2, Step 6 complete.

---

## Phase 3: Content [Lightweight Confirmation]

Goal: Write the exact content for every visual zone on every page.

### Step 7: Detailed Content Plan

**AI Behavior:**

1. Based on confirmed outline + layout-system + layout-skeleton + style-guide, generate a detailed content spec per page. Read the density level from `brief.md`. Read the corresponding content capacity limits from `references/density-presets.md`. Use these as Max Length values for each zone instead of the defaults in `layout-types.md`.
2. Organize content by **visual zone** (not by title + body). Each zone annotated with: content type, text volume, visual weight (primary / secondary / auxiliary).
3. Include chart data specifications for placeholder areas.
4. For visual storytelling presentations, annotate each page's **visual narrative path** (viewer eye flow).
5. Display in batches by section.

**Deliverable:** `content-plan.md`

Mandatory template for each slide:

```markdown
## Slide [N]: [Title]
- Page Type: [MUST match a type from layout-system.md]
- Total Zones: [count]
- Visual Narrative Path: [eye flow description]

### Zone A: [name]
- Type: [title | body | label | data | icon | chart]
- Content: "[EXACT text — required, cannot be empty]"
- Max Length: [character count, from density-presets.md]
- Visual Weight: [primary | secondary | auxiliary]

### Zone B: [name]
- Type: [title | body | label | data | icon | chart]
- Content: "[EXACT text]"
- Max Length: [character count]
- Visual Weight: [primary | secondary | auxiliary]

### Acceptance Criteria
- [ ] All zones have content within max length
- [ ] Chart data complete with values and labels (if applicable)
- [ ] No zone has placeholder or TBD content
```

**Gate:** User confirms all page content plans.

**State Update:** Update `deckdone-state.md` — Phase 3, Step 7 complete.

**Validation:** Optionally run `python scripts/validate-content-plan.py content-plan.md`.

---

### Step 8: User Content Confirmation

- Allow the user to modify specific copy, data, or zone assignments.
- After confirmation, the deliverables are ready for `deckdone-build` or any PPT generation tool. The user may edit any deliverable file before proceeding.

**State Update:** Update `deckdone-state.md` — Phase 3 complete. All planning phases complete.

---

## Harness Engineering Principles

### Verification Loop Principle

Every phase and step has explicit validation checkpoints. Verification is not deferred to the final output — it happens at each gate. When scripts are available, prefer mechanical enforcement (e.g., `scripts/validate-content-plan.py`) over AI self-assessment.

### Structured Task Template Principle

The content plan (`content-plan.md`) is the **contract between planning and implementation**. Whatever tool consumes these deliverables should make zero creative decisions — every detail is specified in the content plan. Structure in, structure out: the more specific the planning output, the more consistent the built result.

### Execution Trace Principle

Append to `deckdone-trace.md` after every step completion, **before** updating `deckdone-state.md`. The trace provides the "why" behind the state file's "what". When resuming across conversations, read both files to understand both current position and reasoning history.

### Harness Improvement Principle

> When a generated deliverable has quality issues, do NOT just fix the deliverable. Identify the root cause and update the harness (reference files, templates, validation rules) to prevent this class of error for all future sessions.

Every failure is a diagnostic signal. Log improvements in `harness-improvements.md`. Compound improvement: every harness fix applies to all future sessions, independent of model improvements.

---

## State File Templates

### deckdone-state.md

Tracks: Status (phase/step/date/progress), Completed Steps (checklist with dates), Key Decisions (framework, style, etc.), Deliverable Status (each file: confirmed/in-progress/not-started), Context Summary (under 500 words; must include purpose, key message, audience, scale, framework, style), Pending Items.

### deckdone-trace.md

Per-session, per-step log with: Iterations, User Decisions, Adjustments, Issues Encountered, Output file paths. Append after every step, before updating state.

### harness-improvements.md

Per-improvement log with: Date, Trigger (what went wrong, where), Root Cause, Fix applied, Updated Files.

---

## Quality Validation

Follow binary pass/fail checks per step. For Steps 1–7, use the checklists in `references/quality-checklist.md`. Every checkbox must pass before advancing.

For Step 7, run mechanical validation:
```bash
python scripts/validate-content-plan.py content-plan.md
```
Checks: valid page types, required zone fields (`- Type:`, `- Content:`, `- Max Length:`, `- Visual Weight:`), no empty/TBD content. Exits 0 on pass, 1 on failure. No pip dependencies.
