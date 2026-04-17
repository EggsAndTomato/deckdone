# DeckDone Skill Design Specification

**Date**: 2026-04-16
**Status**: Draft
**Scope**: A workflow skill for creating large, complex presentations (15-40 slides) from scratch, targeting the "visual storytelling" use case where the presenter uses the PPT as visual aids to narrate from.

---

## 1. Overview

### Problem

Creating large, information-dense presentations (like annual business plans, product roadmaps, R&D strategy decks) is a multi-hour process requiring expertise in content structure, visual design, and PowerPoint tooling. Existing AI tools either focus on simple "title + bullets" slides or lack the workflow discipline to handle complex, multi-page presentations with consistent quality.

### Solution

**DeckDone** is an opencode/Claude Code skill that provides a structured, phased workflow for creating professional presentations. It orchestrates content discovery, design, and production through a gate-controlled process where the user has full decision-making authority at each stage.

### Design Principles

1. **Gate-controlled phases** — Cannot proceed without user confirmation and verified deliverables
2. **Progressive interaction depth** — Deep discussion in early phases, lightweight confirmation in later phases, automatic execution in final phase
3. **Content-first, visuals-second** — Determine what to say before deciding how it looks
4. **Graceful degradation** — Works with minimal dependencies; optional skills enhance the experience
5. **Density-aware** — Designed for slides with 20-50+ text elements, not simple bullet slides

### Target Use Cases

- Annual business plans (FY BP)
- Product roadmaps and strategy decks
- R&D investment proposals
- Technical architecture presentations
- Any presentation where the presenter "reads the pictures" (看图说话)

---

## 2. Architecture

### Positioning

DeckDone is a **workflow orchestration layer** that calls the existing `pptx` skill as its execution engine. It does not directly handle PPTX technical details.

```
User Input
    ↓
DeckDone (workflow orchestration)
    ├── Phase 1: Discovery (content understanding)
    ├── Phase 2: Design (visual planning)
    ├── Phase 3: Content (detailed writing)
    └── Phase 4: Implementation (production)
        └── pptx skill (html2pptx, thumbnail, etc.)
```

### Skill Directory Structure

```
deckdone/
├── SKILL.md                          # Core workflow (~400-500 lines)
├── SETUP.md                          # AI-readable installation guide
└── references/
    ├── layout-patterns.md            # 10+ page type templates with HTML examples
    ├── narrative-frameworks.md       # 5-6 narrative frameworks (SCQA, Pyramid, etc.)
    ├── audience-analysis.md          # Audience profiling methodology
    ├── style-presets.md              # 15-20 visual style presets
    ├── html-wireframe-guide.md       # Wireframe generation standards and templates
    └── quality-checklist.md          # Quality review checklist
```

### Language

SKILL.md and all reference files are written in **English**. The AI communicates with users in their preferred language during execution.

---

## 3. Dependencies

### Required

| Dependency | Type | Purpose |
|-----------|------|---------|
| pptx skill | Skill | Core PPTX generation (html2pptx, thumbnail) |
| pptxgenjs | npm global | PowerPoint generation library |
| playwright | npm global | HTML rendering for html2pptx |
| sharp | npm global | SVG→PNG icon/gradient rasterization |

### Optional (graceful degradation)

| Dependency | Type | Purpose | Degradation if missing |
|-----------|------|---------|----------------------|
| pdf skill | Skill | PDF content extraction | Ask user to paste text |
| docx skill | Skill | Word document extraction | Ask user to paste text |
| xlsx skill | Skill | Spreadsheet data reading | Ask user to provide CSV/text |
| theme-factory skill | Skill | Extended style presets | Use built-in style-presets.md |
| react-icons | npm global | Icon library | Use text-based icons or pre-rendered images |

### Dependency Declaration in SKILL.md

SKILL.md includes a Dependencies section that:
1. Lists all required and optional dependencies
2. Provides installation commands for each
3. Describes degradation behavior for missing optional dependencies
4. References SETUP.md for complete installation instructions

### Runtime Dependency Detection

Each workflow step checks for optional dependencies before use:

```
Step ② Material Collection:
  IF file is .pdf:
    IF pdf skill available → extract automatically
    ELSE → ask user to paste text content
  IF file is .docx:
    IF docx skill available → extract automatically
    ELSE → ask user to paste text content
```

---

## 4. Workflow

### Phase 1: Discovery [Deep Interaction]

**Goal**: Understand what the presentation must communicate and gather the raw materials.

#### Step 1: Presentation Brief

**AI Behavior**:
1. Ask one question at a time (prefer multiple choice):
   - **Purpose**: Work report / Proposal / Knowledge sharing / Project kickoff / Summary / Other
   - **Key Message**: One sentence — "What should the audience remember after this presentation?"
   - **Audience Profile**:
     - Role level (executive / middle management / team / external client / mixed)
     - Subject familiarity (expert / familiar / general / unfamiliar)
     - Audience tendency (data-driven / story-driven / action-oriented / detail-oriented)
   - **Context**: Formal meeting / Informal sharing / Training / Bidding / Other
   - **Scale**: Estimated page count, time limit
2. Read `references/narrative-frameworks.md`, recommend 1-2 frameworks based on purpose + audience
3. Discuss framework selection and methodology reasoning with user
4. Write `brief.md`

**Deliverable**: `brief.md`

```markdown
# Presentation Brief
## Purpose: [purpose]
## Key Message: [one sentence]
## Audience: [profile + tendencies]
## Context: [scenario]
## Scale: [estimated pages, time limit]
## Narrative Framework: [chosen framework + reasoning]
## Methodology: [why this approach works for this audience]
```

**Gate**: User confirms brief.md content is accurate.

#### Step 2: Material Collection

**AI Behavior**:
1. Ask user for reference materials. Suggest possible types:
   - Company documents / Personal work records / Industry reports / Policy documents / Data spreadsheets / Other
2. For each provided file:
   - `.pdf` → use pdf skill to extract text (or ask user to paste if unavailable)
   - `.docx` → use docx skill to extract text (or ask user to paste if unavailable)
   - `.xlsx` / `.csv` → use xlsx skill to read data (or ask user to provide as text)
   - Plain text / URL → read directly
3. Organize by topic, extract key data points, quotes, cases
4. Tag each material with applicable slide scenarios

**Deliverable**: `materials/` directory

```
materials/
├── 00-index.md          # Source index (origin + topic + applicable scenarios)
├── 01-topic-a.md        # Topic-classified extracted content
├── 02-topic-b.md
└── ...
```

**Gate**: User confirms material index is complete.

#### Step 3: Content Outline

**AI Behavior**:
1. Build narrative skeleton based on brief + materials
2. Read `references/narrative-frameworks.md` for framework-specific guidance
3. Generate topic tree (2-3 levels), annotate core arguments for each section
4. Estimate page count per section, total page count
5. Discuss and iterate with user (may require multiple rounds)

**Deliverable**: `outline.md`

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

**Gate**: User confirms outline structure and page count. → Phase 1 complete.

---

### Phase 2: Design [Page-by-page Confirmation]

**Goal**: Define the visual system and layout for each page.

#### Step 4: Page Types and Layout System

**AI Behavior**:
1. Read `references/layout-patterns.md` containing predefined page types:
   - **Cover** — Title + subtitle + date/author
   - **Agenda** — Section list with numbering
   - **Section Divider** — Section title + brief description
   - **Content-Text** — Title + bullet points/paragraphs
   - **Content-TwoCol** — Title + left/right split
   - **Data-Chart** — Title + chart + interpretation text
   - **Quote** — Large quote + attribution
   - **Timeline** — Events/milestones display
   - **Comparison** — A vs B comparison
   - **Closing** — Summary + call to action
   - **Composite-Diagram** — Complex nested-box layout (for architecture diagrams, hierarchy charts, agent maps)
   - **Pipeline-Flow** — Process pipeline visualization
2. Assign a page type to each page based on outline
3. For Composite-Diagram and Pipeline-Flow types, identify:
   - Sub-layout zones within the page
   - Pre-render element needs (icons, gradients, connectors)
4. Confirm page type assignments with user

**Deliverable**: `layout-system.md`

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

## Pre-render Elements:
- Icons needed: [list]
- Gradients needed: [list]
- Connectors/arrows: [list]
```

**Gate**: User confirms page type assignments.

#### Step 5: Visual Style Direction

**AI Behavior**:
1. Read `references/style-presets.md` (15-20 style presets)
2. Read `theme-factory` skill if available for additional presets
3. Recommend 2-3 styles based on presentation purpose + audience
4. Show style previews (color palette + typography + decoration characteristics)
5. User selects or fine-tunes

**Deliverable**: `style-guide.md`

```markdown
# Style Guide
## Palette: [primary/secondary/accent/background/text colors]
## Typography: [heading font + body font + sizes]
## Decoration: [border style / shape patterns / background treatment]
## Layout Rules: [margins / spacing / content area ratios]
## Pre-render Rules: [which visual effects need Sharp rasterization]
```

**Gate**: User confirms style direction.

#### Step 6: Page-by-page Wireframes (HTML)

**AI Behavior**:
1. Read `references/html-wireframe-guide.md` for wireframe standards
2. Generate HTML wireframe for each page:
   - Grayscale color scheme, annotate content block areas
   - Each area labeled with content type (title / body / chart / image)
   - Annotate emphasis areas and visual weight
   - For Composite-Diagram pages: show sub-zone structure with nesting levels
3. Display in batches by section (5-8 pages per batch, avoid overwhelming)
4. User confirms batch by batch; layouts can be adjusted
5. Optionally use webapp-testing skill for browser-based preview

**Deliverable**: `wireframes/` directory

```
wireframes/
├── slide-01-cover.html
├── slide-02-agenda.html
├── slide-03-section1-divider.html
├── slide-04-composite-architecture.html
└── ...
```

**Gate**: All page wireframes confirmed. → Phase 2 complete.

---

### Phase 3: Content [Lightweight Confirmation]

**Goal**: Write the exact content for every visual zone on every page.

#### Step 7: Detailed Content Plan

**AI Behavior**:
1. Based on confirmed outline + layout-system + style-guide + wireframes, generate detailed content spec per page:
   - Organize content by **visual zone** (not title + body)
   - Each zone annotated with: content type, text volume, visual weight (primary/secondary/auxiliary)
   - Pre-render element list (icons, gradients, connectors)
   - Chart data specifications (for placeholder areas)
2. For "visual storytelling" presentations, annotate each page's **visual narrative path** (viewer eye flow)
3. Display in batches by section

**Deliverable**: `content-plan.md`

```markdown
# Content Plan

## Slide 1: [Title] (Type: Composite-Diagram)
### Visual Narrative Path: Top banner → Center architecture → Bottom milestones

#### Zone A: Title Banner
- Type: Title + Subtitle
- Content: "..." (exact text)
- Weight: Primary

#### Zone B: Architecture Diagram
- Type: Nested-box layout (div/flexbox)
- Pre-render needed: [icon list, gradient list]
- Sub-zones:
  - B1: Cloud Platform box → text: "..."
  - B2: Middle Platform (3 columns) → text per column: "..."
  - B3: Product lines grid (6 columns) → text per cell: "..."

#### Zone C: Milestone Timeline
- Type: Horizontal timeline (div-based)
- Data: milestone1(date, text), milestone2(date, text), ...

## Slide 2: ...
```

**Gate**: User confirms all page content plans.

#### Step 8: User Content Confirmation

- User can modify specific copy, data, zone assignments
- After confirmation, proceed to Phase 4

---

### Phase 4: Implementation [Batch Execution]

**Goal**: Produce the final PPTX file with quality assurance.

#### Step 9: Test Generation

**AI Behavior**:
1. Select **one page per layout type** as test samples
2. For each test page, execute full pipeline:
   a. Pre-render elements (Sharp: icons→PNG, gradients→PNG)
   b. Create HTML file with actual content
   c. Call html2pptx to convert
   d. Generate thumbnail
3. User reviews thumbnails for:
   - Layout accuracy
   - Text cutoff or overflow
   - Color block / spacing reasonableness
   - Information density readability
4. If unsatisfied, adjust HTML and regenerate (max 3 rounds per page)
5. Lock template parameters for each page type

**Deliverable**: `test-slides/` directory + `template-params.md`

**Gate**: User confirms all test page visuals.

#### Step 10: Batch Generation

**AI Behavior**:
1. Read locked template parameters from `template-params.md`
2. Generate in **section chunks** (5-8 pages per chunk, avoid context overflow)
3. Per chunk:
   a. Pre-render elements
   b. Generate HTML files
   c. html2pptx conversion
   d. Generate chunk thumbnails for intermediate check
4. Merge all chunks into final .pptx
5. For information-dense pages (50+ text blocks), run **space competition check**:
   - Verify no text is cut off
   - Verify no element overlap
   - Verify adequate margins

**Deliverable**: `output.pptx`

#### Step 11: Final Quality Review

**AI Behavior**:
1. Generate full-PPT thumbnail grid: `python scripts/thumbnail.py output.pptx final-review --cols 4`
2. Check each item:
   - **Consistency**: All pages follow the same style (palette, fonts, spacing)
   - **Completeness**: No missing pages or content
   - **Readability**: Text sizes sufficient, contrast adequate
   - **Narrative flow**: Page transitions feel natural
3. Fix problem pages
4. Generate final version

**Deliverable**: `final.pptx`

Read `references/quality-checklist.md` for the complete review checklist.

---

## 5. Reference Files Specification

### layout-patterns.md

Predefined page type library with:
- 12+ page types, each with:
  - Description and typical use case
  - HTML skeleton example showing zone structure
  - Layout rules (zone ratios, flexbox patterns)
  - Content density guidelines (max text elements, recommended font sizes)
- Special patterns for Composite-Diagram:
  - Nested-box architecture layout
  - Agent/service matrix layout
  - Layered stack layout
  - Pipeline/flow layout

### narrative-frameworks.md

5-6 narrative frameworks:
- **SCQA** (Situation-Complication-Question-Answer) — for problem-solving proposals
- **Pyramid Principle** — for executive summaries and conclusions-first
- **Timeline** — for roadmaps and historical narratives
- **Problem-Solution-Benefit** — for sales pitches and proposals
- **Theme-Illustration-Application** — for knowledge sharing and training
- **Data-Insight-Action** — for analytical reports

Each framework includes:
- Structure description
- When to use (audience + purpose matrix)
- Example outline for a 20-page presentation
- Page type suggestions per section

### audience-analysis.md

Audience profiling methodology:
- Role-level categories and their information needs
- Subject familiarity matrix and its impact on content depth
- Decision-making tendency models (data-driven vs. story-driven vs. action-oriented vs. detail-oriented)
- How audience profile affects: narrative framework choice, content density, visual style

### style-presets.md

15-20 visual style presets. Each preset includes:
- Style name and mood description
- Color palette (primary, secondary, accent, background, text)
- Typography (heading font, body font, size scale)
- Decoration patterns (borders, shapes, backgrounds)
- Best suited for (presentation types + audience)
- Pre-render requirements (which effects need Sharp rasterization)

### html-wireframe-guide.md

Standards for generating HTML wireframes:
- Grayscale color scheme rules
- Zone labeling conventions
- Visual weight annotation syntax
- Composite-Diagram zone structure notation
- Batch display strategy (5-8 pages per batch)
- Integration with webapp-testing skill for browser preview

### quality-checklist.md

Final quality review checklist:
- Visual consistency checks (colors, fonts, spacing across all pages)
- Text integrity checks (no cutoff, no overflow, adequate font sizes)
- Layout checks (element alignment, margin adequacy, no overlaps)
- Content checks (all planned content present, accurate data)
- Narrative flow checks (page transitions, section breaks)
- Pre-render element checks (icons clear, gradients smooth, connectors visible)

---

## 6. Distribution Strategy

### Repository Structure

```
deckdone/                          # GitHub repository
├── SKILL.md                       # Main skill file with dependency declarations
├── SETUP.md                       # AI-readable installation guide
├── references/                    # Reference documentation
│   ├── layout-patterns.md
│   ├── narrative-frameworks.md
│   ├── audience-analysis.md
│   ├── style-presets.md
│   ├── html-wireframe-guide.md
│   └── quality-checklist.md
└── LICENSE
```

### Installation Method

Users install by:
1. Cloning the repo to their skills directory
2. Following SETUP.md instructions (which AI tools can read and execute)
3. SETUP.md includes commands for:
   - Installing the deckdone skill itself
   - Installing required pptx skill dependency
   - Installing npm runtime dependencies
   - Installing optional skill dependencies

### SETUP.md Structure

- Prerequisites (Node.js, Python, opencode/compatible tool)
- Step 1: Install deckdone skill (git clone)
- Step 2: Install required pptx skill (git clone)
- Step 3: Install runtime dependencies (npm install -g)
- Step 4 (Optional): Install optional skill dependencies
- Verification step

---

## 7. Cross-Conversation Continuity

### Problem

Large presentation creation spans multiple AI conversations. When context fills up, degrades, or the user returns after a break, the workflow must resume cleanly without losing decisions or progress.

### Solution: Progress State File + Resume Protocol

#### State File: `deckdone-state.md`

Created when the workflow starts, updated at every gate/phase transition.

**Structure**:

```markdown
# DeckDone Progress State

## Status
- Phase: [current phase name]
- Current Step: [step number and name]
- Last Activity: [datetime]
- Progress: [e.g., "Batch 2/4 wireframes confirmed"]

## Completed Steps
- [x] Phase 1, Step 1: Brief confirmed ([date])
- [x] Phase 1, Step 2: Materials collected ([date])
...

## Key Decisions
- Framework: [chosen framework + why]
- Style: [chosen style + palette]
- [any other critical decisions]

## Deliverable Status
- brief.md [✅ confirmed | 🔄 in progress | ❌ not started]
- materials/ [status]
- outline.md [status]
- layout-system.md [status]
- style-guide.md [status]
- wireframes/ [status with count]
- content-plan.md [status]
- test-slides/ [status]
- output.pptx [status]

## Context Summary
[Under 500 words. Must include: presentation purpose, key message, 
 audience profile, scale, chosen framework, style direction. 
 Enough for a fresh AI instance to understand the project.]

## Pending Items
- [unresolved questions]
- [deferred decisions]
```

#### Resume Protocol (in SKILL.md)

When a user says "continue my presentation" or "resume deckdone" in a new conversation:

1. **Detect**: Look for `deckdone-state.md` in the project directory
2. **Read state**: Parse current phase, step, deliverable status
3. **Read context**: Read the Context Summary section
4. **Read deliverables**: Read the current phase's confirmed deliverable files
5. **Resume**: Continue from the recorded step
6. **Inform user**: "Resuming from Phase [X], Step [Y]. Last activity: [date]. Here's where we left off: [brief summary from state]"

#### State Update Protocol

After each gate/phase transition, the AI must:

1. Update `deckdone-state.md`:
   - Current phase + step number
   - Date of last activity
   - Key decisions made in this session
   - Deliverable files produced or confirmed
   - Any pending items for next session
2. Keep Context Summary under 500 words
3. Always include the brief.md Key Message in Context Summary
4. Write state file BEFORE proceeding to next step (not after)

#### Example State File

```markdown
# DeckDone Progress State

## Status
- Phase: 2 - Design
- Current Step: 6 - Page Wireframes
- Last Activity: 2026-04-16 15:30
- Progress: Batch 1/4 confirmed (slides 1-8)

## Completed Steps
- [x] Phase 1, Step 1: Brief confirmed (2026-04-16 10:00)
- [x] Phase 1, Step 2: Materials collected (2026-04-16 11:00)
- [x] Phase 1, Step 3: Outline confirmed (2026-04-16 12:00)
- [x] Phase 2, Step 4: Layout system confirmed (2026-04-16 13:30)
- [x] Phase 2, Step 5: Style guide confirmed (2026-04-16 14:00)
- [~] Phase 2, Step 6: Wireframes in progress (batch 1/4 done)

## Key Decisions
- Framework: SCQA (Situation → Challenge → Direction → Action)
- Style: Teal & Coral (#5EA8A7 primary, corporate medical theme)
- 4 slides, Composite-Diagram heavy, information-dense
- Pre-render needed: 14 icons, 3 gradient backgrounds

## Deliverable Status
- brief.md ✅ confirmed
- materials/ ✅ confirmed (3 source docs)
- outline.md ✅ confirmed (4 sections, ~4 pages)
- layout-system.md ✅ confirmed (4 page types used)
- style-guide.md ✅ confirmed
- wireframes/ 🔄 in progress (8/32 done)
- content-plan.md ❌ not started
- test-slides/ ❌ not started
- output.pptx ❌ not started

## Context Summary
FY26 Business Plan for "添翼" medical software product line.
Audience: C-level executives. Purpose: Annual R&D investment review.
Key message: R&D investment in 3 projects drives product differentiation.
3 projects: Smart Hospital 2.0, AI 3.0 agents, Data Space 1.0.
Source materials: internal product specs, roadmap docs.
Style: professional medical-tech, blue-teal palette.
High information density per slide (50+ text blocks), visual storytelling format.

## Pending Items
- Wireframes batch 2/4 (slides 9-16) needs user confirmation
- User mentioned wanting to adjust Zone C layout on slide 1
```

---

## 8. Harness Engineering Principles

This skill is designed following Harness Engineering, the discipline of building the infrastructure that makes AI agents reliable. The core principle: **Agent = Model + Harness**. The skill is the harness; it constrains, informs, verifies, and corrects the AI's work.

### 8.1 Multi-Level Verification Loops

Verification does not happen only at the final output. Every phase and step has explicit validation checkpoints that must pass before proceeding.

**Per-step validation rules:**

| Step | Deliverable | Validation Rules |
|------|-----------|-----------------|
| Step 1 | brief.md | All required fields populated; Key Message is a single sentence; Narrative framework selected |
| Step 2 | materials/ | Material index exists; Each source has topic tags and scenario annotations |
| Step 3 | outline.md | Page count within declared Scale range; Every page has a purpose and key point; Every section has a core argument |
| Step 4 | layout-system.md | Every page assigned a valid page type; Pre-render elements listed; No undefined page types |
| Step 5 | style-guide.md | Complete palette (5 colors min); Typography specified; Pre-render rules documented |
| Step 6 | wireframes/ | One HTML file per page; Correct dimensions (720pt × 405pt); Every zone labeled with content type; All pre-render elements marked |
| Step 7 | content-plan.md | Every zone on every page has content; No zone exceeds max character limit; Chart data specs complete; Pre-render elements listed |
| Step 9 | test-slides/ | No text overflow; No element overlap; All images/icons render; Adequate contrast |
| Step 10 | output.pptx | All pages generated; No missing content; Consistent style across pages |
| Step 11 | final.pptx | Thumbnail grid passes visual review checklist |

**Implementation**: These rules are encoded in `references/quality-checklist.md`. After each step, the AI must run through the relevant checklist section and confirm all items pass before declaring the step complete.

### 8.2 Structured Task Template (Content Plan)

The content plan is the **contract between planning and implementation**. The AI executing Phase 4 should make zero creative decisions — every detail must be specified in the content plan.

**Mandatory template for each slide**:

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
(same structure)

### Acceptance Criteria
- [ ] All zones have content within max length
- [ ] All pre-render elements listed in layout-system
- [ ] Chart data complete with values and labels (if applicable)
- [ ] No zone has placeholder or TBD content
```

**Principle**: Structure in, structure out. The more specific the input to the implementation phase, the more consistent the output. The implementing AI fills in blanks, it does not make decisions.

### 8.3 Execution Trace

A running log of what happened during each session, providing context for cross-conversation debugging.

**File**: `deckdone-trace.md`

**Structure**:

```markdown
# DeckDone Execution Trace

## Session 1: [date] [start time]-[end time]
### Step [N] → [name]
- Iterations: [count] (describe rounds of changes)
- User decisions: [list key decisions made by user]
- Adjustments: [what was changed from initial output]
- Issues encountered: [list problems and resolutions]
- Output: [file paths] ✅/⚠️

### Step [N+1] → [name]
...
```

**Update rule**: Append to the trace after every step completion, before updating `deckdone-state.md`. The trace provides the "why" behind the state file's "what".

**Cross-conversation value**: When resuming, the AI reads both `deckdone-state.md` (current position) and `deckdone-trace.md` (what happened and why), enabling informed continuation.

### 8.4 Harness Improvement Feedback Loop

When a generated slide has quality issues, the fix is not just the slide — it is the harness. Every failure is a diagnostic signal.

**File**: `harness-improvements.md`

**Structure**:

```markdown
# Harness Improvement Log

## Improvement #[N]
- Date: [date]
- Trigger: [what went wrong, on which slide/step]
- Root Cause: [why it happened — harness gap analysis]
- Fix: [what was changed in the harness]
- Updated Files: [which reference files or templates were modified]
```

**Core principle from SKILL.md**:

> "When a generated slide has quality issues, do NOT just fix the slide. Identify the root cause and update the harness (reference files, templates, validation rules, or the content plan template) to prevent this class of error for all future slides."

**Compound improvement**: Every harness fix applies to all future sessions and all future slides. This is the compound flywheel — the harness gets better over time, independent of model improvements.

### 8.5 Validation Scripts (Mechanical Enforcement)

Where possible, validation rules are implemented as executable checks rather than relying on AI self-enforcement.

**Script-based validation** (in `scripts/` directory):

| Script | Purpose | Trigger |
|--------|---------|---------|
| `validate-content-plan.py` | Parse content-plan.md, verify all zones have content, check character limits against layout-patterns.md | After Step 7 |
| `validate-html-slides.py` | Check HTML dimensions, verify all text is in `<p>/<h1>-<h6>` tags, detect overflow | After Step 9-10 |

**Fallback for environments without Python**: The same validation rules are documented as checklists in `references/quality-checklist.md`. The AI runs through them manually when scripts are unavailable.

**Design principle**: Mechanical enforcement is preferred over documentation. Where a script can validate, it should. Where it cannot, a structured checklist serves as the fallback.

---

## 9. Future Considerations

These are explicitly **out of scope** for the initial version but noted for future iteration:

1. **Speaker notes generation** — Auto-generate speaking notes per slide based on content plan
2. **Template-based mode** — Support creating presentations from existing corporate templates
3. **Diagram generation integration** — Integrate Excalidraw or architecture-diagram skills for complex visual connections
4. **Multi-language presentations** — Support bilingual slides (e.g., Chinese + English)
5. **Animation and transitions** — Add slide transition and element animation effects
6. **Iterative refinement mode** — Support modifying an existing generated PPT through conversational feedback
7. **Parallel generation** — Generate multiple slides simultaneously using subagent-dispatch for faster production
