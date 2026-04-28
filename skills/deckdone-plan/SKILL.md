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
6. **Match user language** — Communicate with the user in the language they use in conversation.

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
| `diagram-data/` | 2 | 5 | Per-page diagram structured data (for Content-Diagram pages) |
| `deckdone-state.md` | all | all | Progress state file |
| `deckdone-trace.md` | all | all | Execution trace log |

---

## Cross-Conversation Continuity

See `references/state-templates.md` for state file, trace file, and harness improvement log templates.

### Resume Protocol

When the user says "continue my presentation" or "resume deckdone":

1. Look for `deckdone-state.md` in the project directory.
2. Parse current phase, step, and deliverable status.
3. Read the Context Summary section (kept under 500 words).
4. Read the current phase's confirmed deliverable files.
5. Resume from the recorded step and inform the user.

### State Update Protocol

After each gate or phase transition, update `deckdone-state.md` with: current phase + step + date, key decisions, deliverable status, pending items. Keep Context Summary under 500 words. Must include Key Message and Density from `brief.md`. Write state file **before** proceeding to the next step.

---

## Phase 1: Discovery [Deep Interaction]

Goal: Understand what the presentation must communicate and gather the raw materials.

### Step 1: Presentation Brief

**AI Behavior:**

1. Ask one question at a time. Prefer multiple-choice formats:
   - **Purpose:** Work report / Proposal / Knowledge sharing / Project kickoff / Summary / Other
   - **Key Message:** One sentence — "What should the audience remember after this presentation?"
   - **Audience Profile:** Role level (executive / middle management / team / external client / mixed), Subject familiarity (expert / familiar / general / unfamiliar), Audience tendency (data-driven / story-driven / action-oriented / detail-oriented)
   - **Context:** Formal meeting / Informal sharing / Training / Bidding / Other
   - **Scale:** Estimated page count, time limit
   - **Density:** Read `references/density-presets.md` for level descriptions. Ask: "Will the audience read this deck on their own, or will you present it live?"
2. Read `references/narrative-frameworks.md`. Recommend 1-2 frameworks based on purpose + audience. Discuss with user.
3. Write `brief.md`.

**Deliverable:** `brief.md` (fields: Purpose, Key Message, Audience, Context, Scale, Density, Density Reasoning, Narrative Framework, Methodology)

**Gate:** User confirms `brief.md`.

**State Update:** Update `deckdone-state.md` — Phase 1, Step 1 complete.

---

### Step 2: Material Collection

⛔ **MANDATORY INTERACTION** — AI must explicitly ask about materials. Never skip this step.

**AI Behavior:**

1. Explicitly ask the user whether they have reference materials. Suggest possible types:
   - Company documents / Personal work records / Industry reports / Policy documents / Data spreadsheets / URLs / Other
2. Wait for user response. Three possible outcomes:
   - **User provides files/URLs** → extract and organize (see step 4 below).
   - **User says they have materials but will provide later** → note in state file, proceed to Step 3.
   - **User says no materials** → create minimal `materials/00-index.md` noting "No external materials provided".
3. After handling the user's response above (regardless of outcome), ask the user whether they would like you to search the web for supplementary materials. Offer suggested search topics based on brief's Purpose, Audience, and Key Message (e.g., industry reports, market data, competitor information, best practices). Two possible outcomes:
   - **User agrees** → perform targeted web search, organize results by topic with each source clearly annotated with its URL. Extract key data points, statistics, quotes, and findings relevant to the brief. Tag with applicable slide scenarios.
   - **User declines** → proceed to Step 3.
4. For each file provided, detect format and extract:
   - `.pdf` → use pdf skill; if unavailable, ask user to paste text content
   - `.docx` → use docx skill; if unavailable, ask user to paste text content
   - `.xlsx` / `.csv` → use xlsx skill; if unavailable, ask user to provide data as text
   - Plain text / URL → read directly
5. Organize all extracted content (from files and web search) by topic. Extract key data points, quotes, and cases.
6. Tag each material with applicable slide scenarios. Web-sourced materials must include source URL in their index entry.
7. In `materials/00-index.md`, add a **Data Points** section that extracts every quantified data point, statistic, or third-party claim from collected materials. Format:

   ```markdown
   ## Data Points
   | Data Point | Value | Source | Applicable Slides |
   |------------|-------|--------|-------------------|
   | [description] | [value] | [material name + page/section, or URL] | [slide refs] |
   ```

   **Source attribution rules:**
   - User-provided materials → tag with material name + page/section location (e.g., `2024 Industry Report p.12`)
   - Web search results → tag with full URL (e.g., `https://example.com/report`)
   - No identifiable source → tag as `Unverified` and warn the user that this data cannot be verified; recommend the user confirm or remove it

**Deliverable:** `materials/` directory (with `00-index.md` as source index)

**Gate:** User confirms material status.

**State Update:** Update `deckdone-state.md` — Phase 1, Step 2 complete.

---

### Step 3: Content Outline

**AI Behavior:**

1. Build narrative skeleton based on brief + materials.
2. Read `references/narrative-frameworks.md` for framework-specific guidance on section structure.
3. Read `references/density-presets.md` for visual element density targets. Actively plan visual page types (Data-Chart, Timeline, Comparison, Pipeline-Flow) to meet the target visual page ratio for the selected density level.
4. Generate topic tree (2-3 levels). Annotate core arguments for each section.
5. Estimate page count per section and total page count.
6. Discuss and iterate with the user (may require multiple rounds).

**Deliverable:** `outline.md` (Framework, Total Pages, Sections with per-page purpose + key point)

**Gate:** User confirms outline structure and page count. Phase 1 complete.

**State Update:** Update `deckdone-state.md` — Phase 1, Step 3 complete.

---

## Phase 2: Layout + Content [Real-time Visual Review]

Goal: Define page layouts and fill in real content with live HTML wireframe review.

### Step 4: Page Types and Layout System

**AI Behavior:**

1. Read `references/layout-types.md` for standard page type definitions.
2. Read `references/relationship-layout-map.md` for diagram type definitions and detection heuristics.
3. For each page in the outline, determine whether the content warrants a diagram layout:
   - Apply the detection heuristics (priority-ordered triggers) from relationship-layout-map.md.
   - If a relationship type match is found → assign Page Type: Content-Diagram and Relationship Type: <matched type>.
   - If no match → assign a standard page type from layout-types.md.
4. Read `references/density-presets.md` for visual element density targets. Prefer visual page types over text-only types: Data-Chart for metrics, Timeline for sequences, Comparison for side-by-side, Pipeline-Flow for processes, Composite-Diagram for architectures. Only use Content-Text when no visual type fits.
5. For Composite-Diagram, Pipeline-Flow, and Content-Diagram types: identify sub-layout zones.
6. Confirm page type assignments with the user.

**Deliverable:** `layout-system.md` (page type assignments per slide)

**Gate:** User confirms page type assignments.

**State Update:** Update `deckdone-state.md` — Phase 2, Step 4 complete.

---

### Step 5: Content Wireframe Review

⛔ **BLOCKING** — User must review and confirm content via live wireframes.

**Prerequisites:** Steps 1-4 completed. `brief.md`, `outline.md`, and `layout-system.md` confirmed.

**Sub-Agent Delegation:** This step delegates heavy generation to sub-agents. See `references/sub-agent-protocols.md` for full prompt templates.

**AI Behavior:**

#### 5a. Wireframe Generation (delegate to sub-agent)

1. Read `references/sub-agent-protocols.md` for delegation instructions.
2. Delegate `wireframes.html` generation to a sub-agent (subagent_type: "general"). The sub-agent reads all reference files and produces the HTML.
3. After sub-agent completes, confirm `wireframes.html` exists.
4. Tell the user: the file path, to open it in a browser (auto-refreshes every 3 seconds), and to give feedback while watching — AI will update and browser will refresh.
5. Enter the review loop in main agent: wait for user feedback → targeted edit `wireframes.html` → briefly confirm changes. Common feedback: content change, layout change, add/remove chart, page split/merge.
   - Small edits (1-3 pages): use Edit tool directly in main agent.
   - Major restructure (5+ pages): delegate full regeneration to a new sub-agent with updated instructions.

#### 5a-2. Diagram Data Generation (for Content-Diagram pages only)

For each Content-Diagram page from layout-system.md:
- Read `../deckdone-build/references/diagram-specs.md` to understand the required data structure for the diagram type.
- Based on the wireframe content, fill in a `diagram-data/<page-slug>.md` file following the schema for the diagram type.
- Each file must include: Type, required fields per type, and all content.
- The slug follows the convention: P##_Name.svg → lowercase name with hyphens → e.g., p05_hub-and-spoke.
- Ensure each diagram-data file complies with the constraints limits (max branches/nodes/layers per type).

#### 5b. Content Plan Export (delegate to sub-agent)

6. When user confirms all pages, delegate export to a sub-agent:
   - Input: `wireframes.html`, `brief.md`, `outline.md`, `layout-system.md`, reference files.
   - Output: `content-plan.md` + `layout-skeleton.md`.
7. After sub-agent completes, run validation:
   ```bash
   python scripts/validate-content-plan.py content-plan.md
   ```

**Content Plan Template (per slide):** Each slide needs Page Type, Total Zones, Visual Narrative Path. Each zone needs Type, Content (exact text, non-empty), Max Length (from `references/density-presets.md`), Visual Weight (primary|secondary|auxiliary). **Optional Source field:** when a zone contains statistics, quantified data, third-party claims, or direct quotes, add `- Source:` with the attribution from `materials/00-index.md` Data Points table. Zones without data references do not need Source. Chart zones additionally need: Chart Type, Chart Title, X-Axis, Y-Axis, Data Points, Key Insight. Each slide ends with Acceptance Criteria checkboxes.

**Deliverable:** `wireframes.html` + `content-plan.md` + `layout-skeleton.md` + `diagram-data/`

**Gate:** User confirms all page content via wireframe review.

**State Update:** Update `deckdone-state.md` — Phase 2 complete. All planning phases complete.

---

## Harness Principles

- **Fix the harness, not the output.** When deliverables have quality issues, update reference files and validation rules to prevent recurrence. Log in `harness-improvements.md`.
- **Append to `deckdone-trace.md`** after every step completion, before updating state. The trace captures "why"; the state captures "what".
- **Use the checklists** in `references/quality-checklist.md` at every step gate.

---

## State File Templates

See `references/state-templates.md`.

---

## Quality Validation

For Step 5, run: `python scripts/validate-content-plan.py content-plan.md` (checks: valid page types, required zone fields, no empty content, Max Length compliance, chart data completeness). Exits 0 on pass.
