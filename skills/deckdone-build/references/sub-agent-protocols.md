# Sub-Agent Delegation Protocols for deckdone-build

Guide for delegating context-heavy generation steps to sub-agents via the Task tool. This saves main-agent context by offloading large outputs (SVG code, presentation guide text) to isolated sub-agent sessions.

---

## General Rules

1. **Always delegate** — Steps 6b, 7a, and 8b should use sub-agents by default. The main agent orchestrates and handles user interaction only.
2. **Input via prompt** — Sub-agents cannot access the current conversation. Pass all necessary context via the Task prompt: file paths to read, locked design tokens, specific instructions.
3. **Output via files** — Sub-agents write results directly to the project directory. The main agent never sees the intermediate output content, only confirms files exist and runs validation.
4. **Sub-agent type** — Use `subagent_type: "general"` for all generation tasks.
5. **File reads are cheap** — Sub-agents can read reference files independently. List every file they need in the prompt.
6. **Batch sizing for Step 7** — 3-5 pages per sub-agent. For decks ≤ 10 pages, a single sub-agent suffices. For 11-20 pages, split into 2-3 agents. For 21+, split into 4-6 agents.
7. **Quality gate stays in main agent** — Running validators, presenting results to user, and handling review feedback remain in the main agent.

---

## Step 6b: Test SVG Generation

### Delegation Pattern

Single sub-agent generates all test SVGs for one round.

### Main Agent Responsibilities

1. Complete Step 6a (style selection) in main agent — interactive with user.
2. Identify distinct layout types from `layout-system.md`.
3. Select one test page per layout type.
4. Delegate all test SVG generation to one sub-agent.
5. Run converter and validator after sub-agent completes.
6. Present results to user for review.

### Prompt Template

```
You are generating test SVG slides for a presentation. Generate one test SVG per layout type listed below.

## Files to Read (READ ALL BEFORE GENERATING)

1. `references/svg-constraints.md` — SVG generation rules (MANDATORY — every rule must be followed)
2. `style-guide.md` — color palette, typography, decoration patterns
3. `content-plan.md` — read ONLY the pages listed in "Test Pages" below
4. `layout-skeleton.md` — read ONLY the pages listed in "Test Pages" below
5. Layout template from `templates/layouts/<style-name>/` — find the matching layout template for each page type
6. `templates/charts/charts_index.json` — if any test page is Data-Chart type, look up the matching chart template

## Design Context (LOCKED — use these exact values)

[Paste the full content of style-guide.md + template-params.md here]

## Test Pages

[Paste the specific page entries from layout-system.md and content-plan.md for each test page]

For each test page:
- Page number: P##_<Name>
- Page type: [type]
- Content zones: [list zones]

## Generation Rules

1. Generate one SVG file per test page.
2. Each SVG must have viewBox="0 0 1280 720" width="1280" height="720".
3. Follow ALL constraints in svg-constraints.md — no exceptions.
4. Apply the locked design context (colors, fonts, spacing) exactly.
5. For Data-Chart pages: include actual graphical chart elements (bars, lines, slices), not just text.
6. Save files to `svg_output/P##_Name.svg`.
7. Return: list of generated file paths.

## Output

Write the SVG files to `svg_output/`. Return the list of file paths you created.
```

---

## Step 7a: Batch SVG Generation

### Delegation Pattern

**Parallel sub-agents** — split pages into batches of 3-5, each handled by one sub-agent. All batches run concurrently.

### Main Agent Responsibilities

1. Lock design context from `style-guide.md` + `template-params.md`.
2. Split all pages into batches (3-5 pages per batch).
3. Launch all sub-agents in parallel (single message, multiple Task tool calls).
4. Wait for all sub-agents to complete.
5. Run converter: `python scripts/svg_to_pptx.py <project-dir> -s svg_output -o output.pptx --only native`
6. Run validator: `python scripts/validate-svg-slides.py svg_output/`
7. Proceed to quality review.

### Batch Splitting Logic

```
pages = total page count
if pages <= 10:
    batches = 1  (all pages in one sub-agent)
elif pages <= 20:
    batches = ceil(pages / 7)
else:
    batches = ceil(pages / 5)
max_batches = 6  (cap to avoid excessive parallelism)
```

Assign pages sequentially to batches (no need for complex scheduling).

### Prompt Template

```
You are generating SVG slides for a presentation. You are responsible for a batch of [N] pages.

## Files to Read (READ ALL BEFORE GENERATING)

1. `references/svg-constraints.md` — SVG generation rules (MANDATORY)
2. `style-guide.md` — color palette, typography, decoration patterns
3. `template-params.md` — locked template parameters
4. `content-plan.md` — read ONLY the pages listed in "Your Pages" below
5. `layout-skeleton.md` — read ONLY the pages listed in "Your Pages" below
6. Layout template from `templates/layouts/<style-name>/` — find the matching layout template for each page type
7. `templates/charts/charts_index.json` — for Data-Chart pages, find the matching chart template, then read the actual SVG file from `templates/charts/`

## Design Context (LOCKED — use these exact values for every page)

[Paste the full content of style-guide.md + template-params.md here]

## Your Pages

[Paste the specific page entries from content-plan.md for each assigned page]
[Paste the specific page entries from layout-skeleton.md for each assigned page]

Page list:
- P##_Name (PageType)
- P##_Name (PageType)
- ...

## Per-Page-Type Visual Element Rules

### Data-Chart pages
- Read the matching chart template from `templates/charts/`.
- Extract SVG structure: axes, bars/slices/points, gridlines, legend.
- Replace template data with actual values from the content-plan chart zone.
- Chart area MUST contain non-text graphical elements — never render chart data as bullet text.

### Timeline pages
- Include: horizontal/vertical timeline line, milestone nodes, card outlines, connector lines.
- Never render timeline events as plain text without visual node+line structure.

### Pipeline-Flow pages
- Include: stage containers with rounded corners, arrow connectors between stages.
- Never render pipeline stages as plain text without shape containers and arrows.

### Comparison pages
- Include: column/row container outlines, divider lines, header background fills.

### Composite-Diagram pages
- Include: component boxes, connector lines/arrows, layer separator lines.
- For Layered Stack: horizontal band backgrounds for each layer.
- For Nested-Box: nested rectangles with different border styles.

### Content-Text / Content-TwoCol pages
- Include at least one visual element beyond text (colored sidebar bar, accent line, or icon).

### Cover / Section Divider / Closing pages
- Preserve decorative elements from the layout template (background, sidebar, chrome).

## Generation Rules

1. Generate one SVG file per page, sequentially.
2. Each SVG: viewBox="0 0 1280 720" width="1280" height="720".
3. Follow ALL constraints in svg-constraints.md.
4. Apply the locked design context identically across all pages.
5. File naming: `svg_output/P##_Name.svg`.
6. Start each SVG with `<defs>` block for gradients/filters.
7. Element ordering: background → decorations → content → foreground.

## Output

Write the SVG files to `svg_output/`. Return the list of file paths you created, in order.
```

### Parallel Launch Example

The main agent sends one message with multiple Task tool calls:

```
// Agent 1: pages P01-P05
Task(subagent_type="general", prompt=<prompt with batch 1>)
// Agent 2: pages P06-P10
Task(subagent_type="general", prompt=<prompt with batch 2>)
// Agent 3: pages P11-P15
Task(subagent_type="general", prompt=<prompt with batch 3>)
```

---

## Step 8b: Presentation Guide Generation

### Delegation Pattern

Single sub-agent reads all deliverable files and generates the presentation guide.

### Main Agent Responsibilities

1. Verify all SVGs pass validation (Step 8a).
2. Run final PPTX conversion.
3. Delegate presentation guide writing to sub-agent.
4. Present the guide to user for confirmation.

### Prompt Template

```
You are writing a presentation guide for a finished presentation deck. Read all the input files below and generate `presentation-guide.md`.

## Files to Read (READ ALL)

1. `brief.md` — purpose, audience, framework, density, scale
2. `outline.md` — section structure, page count
3. `content-plan.md` — per-page content, visual narrative paths
4. `style-guide.md` — visual style
5. `layout-skeleton.md` — page layout overview
6. `materials/00-index.md` — data points with source attribution (if available)
7. `references/presentation-guide-template.md` — output template structure

## Output Format

Follow the 5-module template in `references/presentation-guide-template.md` exactly:
- Module 1: Overview
- Module 2: Design Rationale
- Module 3: Slide Key Points (with emphasis levels ★ Key / Normal / ⏭ Skippable)
- Module 4: Speaking Notes (transition cues, anticipated questions, timing guidance)
- Module 5: Data Sources (per-slide data provenance table)

## Rules

1. Emphasis levels: based on each page's contribution to the Key Message from brief.md.
2. Time allocation: total minutes ÷ total pages, weighted by emphasis. Default 1.5 min/page if no time estimate.
3. Predict 2-3 likely audience questions based on content gaps or contentious points.
4. Module 5: Only include slides with sourced data. Tag sources as "User-provided material", "Web search", or "⚠ Unverified".
5. Write in the user's preferred language (match the language of brief.md).
6. Write to `presentation-guide.md` in the project directory.

## Output

Write the file to `presentation-guide.md`. Return: "Done" when complete.
```

---

## Context Savings Estimate

| Step | Without Sub-Agent | With Sub-Agent | Savings |
|------|------------------|----------------|---------|
| 6b test SVGs | 5-8 × 200 lines = 1000-1600 lines in main context | ~50 lines (prompt + file list result) | ~95% |
| 7a batch SVGs | 30 × 200 lines = 6000 lines in main context | ~200 lines (prompts + file list results) | ~97% |
| 8b presentation guide | ~500 lines read + ~300 lines written | ~50 lines (prompt + confirmation) | ~94% |
| **Total build phase** | **~8000 lines** | **~300 lines** | **~96%** |

---

## Troubleshooting

### Sub-agent generates inconsistent styles

Cause: locked design context not pasted fully into the prompt.
Fix: always paste the COMPLETE content of `style-guide.md` + `template-params.md` into the "Design Context" section. Do not summarize or abbreviate.

### Sub-agent misses SVG constraints

Cause: sub-agent did not read `svg-constraints.md` carefully.
Fix: the prompt already instructs reading it. If issues persist, paste the key constraints directly into the prompt template.

### Validator fails after sub-agent generation

Cause: individual SVG constraint violation.
Fix: the main agent should read the validator output, identify the failing file, and either:
1. Re-delegate just that page to a new sub-agent with specific fix instructions, or
2. Fix it directly in the main agent (small fixes are acceptable in main context).

### Sub-agent runs out of context

Cause: batch too large (rare for 3-5 pages).
Fix: reduce batch size to 3 pages, or provide content-plan entries as inline text instead of asking the sub-agent to read the full file.
