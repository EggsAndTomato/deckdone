---
name: deckdone-plan
description: "Structured workflow for planning presentation content (15-40 slides). Orchestrates content discovery, layout planning, and detailed content writing through a phased, gate-controlled process. Produces editable markdown deliverables: brief, outline, layout system, and a content plan with layout skeleton. Visual style selection is deferred to deckdone-build. Use when the user needs to plan what a presentation should contain — the output can be used by deckdone-build or any PPT generation tool."
---

# DeckDone Plan — Presentation Content Planning Workflow

## Overview

This skill handles **content planning only** — Steps 1 through 5 of the DeckDone workflow. It produces a set of editable markdown files that fully describe what a presentation should contain, how it should be structured, and what content goes where. Visual style (colors, fonts, decoration) is **not** part of this skill — it belongs to `deckdone-build`.

The user may freely edit any deliverable file between planning and building. The planning phase makes no assumptions about the build tool.

### Workflow at a Glance

| Phase | Name | Interaction | Steps | Goal |
|-------|------|-------------|-------|------|
| 1 | Discovery | Deep | 1-3 | Understand what to communicate; gather materials |
| 2 | Layout + Content | Real-time visual | 4-5 | Define page types, then discuss content with live HTML wireframes |

### Design Principles

1. **Gate-controlled phases** — Proceed only after user confirmation and verified deliverables.
2. **Content-only planning** — No visual style decisions. Colors, fonts, decoration are deferred to `deckdone-build`.
3. **Content-first, visuals-second** — Determine what to say before deciding how it looks.
4. **Live wireframe review** — Step 5 uses low-fidelity HTML wireframes with real content for real-time browser review.
5. **Density-aware** — Designed for slides with 20-50+ text elements, not simple bullet slides.

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
| `wireframes.html` | 2 | 5 | Low-fidelity HTML wireframes for live review |
| `content-plan.md` | 2 | 5 | Detailed content per visual zone |
| `layout-skeleton.md` | 2 | 5 | Per-page zone layout summary |
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
2. Read `references/narrative-frameworks.md`. Recommend 1-2 frameworks based on purpose + audience.
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
3. Generate topic tree (2-3 levels). Annotate core arguments for each section.
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

## Phase 2: Layout + Content [Real-time Visual Review]

Goal: Define page layouts and fill in real content with live HTML wireframe review.

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
- Page 4-5: Composite-Diagram
- Page 6: Data-Chart
- Page 7: Timeline
...
```

**Gate:** User confirms page type assignments.

**State Update:** Update `deckdone-state.md` — Phase 2, Step 4 complete.

---

### Step 5: Content Wireframe Review

⛔ **BLOCKING** — User must review and confirm content via live wireframes.

**Prerequisites:** Steps 1-4 completed. `brief.md`, `outline.md`, and `layout-system.md` confirmed.

**AI Behavior:**

1. Read `references/wireframe-guide.md` for HTML wireframe generation rules.
2. Read `references/density-presets.md` for content capacity limits based on density level from `brief.md`.
3. Read `references/layout-types.md` for per-type zone templates and ratios.
4. Generate `wireframes.html` — a single low-fidelity HTML file containing all slides:
   - Each slide rendered as a 1280×720 proportional `<div>` with gray-bordered zones
   - Zones labeled with type, visual weight, and filled with real content text
   - Chart zones show placeholder boxes with chart type, title, axes, and data points
   - No visual styling (no colors from style-guide, no decorative fonts, no gradients)
   - Auto-refresh script included for live browser review
   - Thumbnail navigation bar at the bottom for quick page switching
5. Present the file to the user. Instruct them to open `wireframes.html` in a browser.
6. Discuss content and layout with the user while they watch the browser auto-update:
   - **Content completeness** — all key points covered, no gaps or redundancies
   - **Layout reasonableness** — zone sizes and positions make sense
   - **Information hierarchy** — primary/secondary/auxiliary weight reflected in zone sizes
   - **Chart necessity** — every chart has a clear message, no chart for chart's sake
7. Edit `wireframes.html` in response to user feedback. Changes appear in browser within 3 seconds.
8. Iterate until user confirms all pages. When confirmed:
   a. Export `content-plan.md` — per-zone content specification following the mandatory template.
   b. Export `layout-skeleton.md` — per-page zone layout summary (overview table + zone list per page).
9. Optionally run validation:
   ```bash
   python scripts/validate-content-plan.py content-plan.md
   ```

**Content Plan Mandatory Template (per slide):**

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

**Chart Zone Content Format (in wireframe and content-plan):**

```markdown
### Zone C: [chart name]
- Type: chart
- Chart Type: [line | bar | pie | scatter | area | stacked-bar]
- Chart Title: "[chart title]"
- X-Axis: [dimension description]
- Y-Axis: [measure description]
- Data Points: [key values or ranges]
- Key Insight: [one sentence — what this chart should communicate]
- Max Length: N/A
- Visual Weight: [primary | secondary]
```

**Deliverable:** `wireframes.html` + `content-plan.md` + `layout-skeleton.md`

**Gate:** User confirms all page content via wireframe review.

**State Update:** Update `deckdone-state.md` — Phase 2 complete. All planning phases complete.

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

See `references/state-templates.md` for the full state file, trace file, and harness improvement log templates.

---

## Quality Validation

Follow binary pass/fail checks per step. For Steps 1-5, use the checklists in `references/quality-checklist.md`. Every checkbox must pass before advancing.

For Step 5, run mechanical validation:
```bash
python scripts/validate-content-plan.py content-plan.md
```
Checks: valid page types, required zone fields (`- Type:`, `- Content:`, `- Max Length:`, `- Visual Weight:`), no empty/TBD content, Visual Narrative Path per slide, Total Zones matches actual zone count, Max Length is a positive integer, content length within Max Length, chart zones have Chart Data specification. Exits 0 on pass, 1 on failure. No pip dependencies.

Optional icon validation:
```bash
python scripts/validate-content-plan.py content-plan.md --catalog <icon-catalog.md>
```
