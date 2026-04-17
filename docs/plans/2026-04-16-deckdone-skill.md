# DeckDone Skill Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the DeckDone presentation creation workflow skill as a complete, distributable opencode skill.

**Architecture:** Single skill with references progressive disclosure. SKILL.md contains the core workflow orchestration logic (~500 lines). Six reference files provide decision-support content. Two validation scripts provide mechanical enforcement. SETUP.md enables distribution.

**Tech Stack:** Markdown (skill files), Python 3.10+ (validation scripts), html2pptx + PptxGenJS (runtime, via pptx skill dependency)

**Spec:** `docs/2026-04-16-deckdone-skill-design.md`

---

## File Structure

```
deckdone/
├── SKILL.md                              # Core workflow (~500 lines)
├── SETUP.md                              # AI-readable installation guide (~80 lines)
├── LICENSE                                # MIT license
├── scripts/
│   ├── validate-content-plan.py           # Content plan validation (~100 lines)
│   └── validate-html-slides.py            # HTML slide validation (~80 lines)
└── references/
    ├── layout-patterns.md                 # 12+ page types with HTML examples (~300 lines)
    ├── narrative-frameworks.md            # 6 frameworks with audience matrix (~250 lines)
    ├── audience-analysis.md               # Audience profiling methodology (~150 lines)
    ├── style-presets.md                   # 15-20 visual style presets (~200 lines)
    ├── html-wireframe-guide.md            # Wireframe generation standards (~150 lines)
    └── quality-checklist.md               # Per-step validation checklists (~200 lines)
```

---

## Chunk 1: SKILL.md

### Task 1: Initialize Skill Directory Structure

**Files:**
- Create: `deckdone/` (root)
- Create: `deckdone/scripts/`
- Create: `deckdone/references/`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p deckdone/scripts deckdone/references
```

- [ ] **Step 2: Create LICENSE file**

Create `deckdone/LICENSE` with MIT license text.

- [ ] **Step 3: Verify structure**

Run: `ls -R deckdone/`
Expected: SKILL.md not yet created; directories scripts/ and references/ exist.

---

### Task 2: Write SKILL.md — Frontmatter, Overview, and Dependencies

**Files:**
- Create: `deckdone/SKILL.md`

- [ ] **Step 1: Write SKILL.md frontmatter and overview section**

Write `deckdone/SKILL.md` with the following content structure (refer to spec Section 1-3):

```markdown
---
name: deckdone
description: "Structured workflow for creating large, complex presentations (15-40 slides) from scratch. Orchestrates content discovery, visual design, and production through a phased, gate-controlled process. Use when the user asks to create a presentation, build slides, or make a PPT/PPTX deck — especially for information-dense decks like business plans, product roadmaps, R&D strategy presentations, or any 'visual storytelling' format where the presenter reads the pictures. Handles material collection, narrative framework selection, page-by-page wireframing, detailed content planning, and batch PPTX generation via the pptx skill."
---

# DeckDone — Presentation Creation Workflow

[Overview section covering: problem statement, the 4-phase workflow at a glance, design principles (gate-controlled phases, progressive interaction, content-first, graceful degradation, density-aware)]

## Dependencies

### Required
[list with installation commands]

### Optional (graceful degradation)
[list with degradation behavior]

## Dependency Detection
[runtime detection logic for each optional skill]

## Quick Reference: Deliverable Files
[table of all deliverable files and when they're produced]

## Cross-Conversation Continuity
[Resume Protocol — how to detect and resume from deckdone-state.md]
[State Update Protocol — when and how to update state]
```

Content must be drawn directly from spec Sections 1, 2, 3, and 7. Use imperative/infinitive form throughout.

- [ ] **Step 2: Verify frontmatter is valid YAML**

Read back the first 5 lines of SKILL.md. Confirm `name:` and `description:` fields are present and description is comprehensive (>200 characters).

---

### Task 3: Write SKILL.md — Phase 1 Workflow (Steps 1-3)

**Files:**
- Modify: `deckdone/SKILL.md`

- [ ] **Step 1: Append Phase 1: Discovery section to SKILL.md**

Add after the Dependencies section. Content from spec Section 4, Phase 1 (Steps 1-3).

For each step include:
- **AI Behavior**: Numbered list of actions, one question at a time
- **Deliverable**: Exact file path and markdown template
- **Gate**: What must be confirmed before proceeding
- **State Update**: What to write to deckdone-state.md at this step
- **Validation**: Which quality-checklist.md section to run

Format:
```markdown
## Phase 1: Discovery

### Step 1: Presentation Brief

**AI Behavior**:
1. [specific action]
2. [specific action]

**Deliverable**: `brief.md`
[include template]

**Gate**: User confirms brief.md content is accurate.

**State Update**: Update deckdone-state.md — Phase 1, Step 1 complete.

**Validation**: Run quality-checklist.md Section 1.1.

---

### Step 2: Material Collection
[same structure]

---

### Step 3: Content Outline
[same structure]
```

- [ ] **Step 2: Verify Phase 1 section is complete**

Read back Phase 1 section. Confirm all 3 steps are present, each has AI Behavior + Deliverable + Gate + State Update + Validation.

---

### Task 4: Write SKILL.md — Phase 2 Workflow (Steps 4-6)

**Files:**
- Modify: `deckdone/SKILL.md`

- [ ] **Step 1: Append Phase 2: Design section to SKILL.md**

Content from spec Section 4, Phase 2 (Steps 4-6). Same format as Phase 1.

For Step 4 (Page Types), include the full list of 12 page types inline (Cover through Pipeline-Flow) so the AI doesn't need to read layout-patterns.md to make initial assignments.

For Step 6 (Wireframes), include the batch strategy (5-8 pages per batch) and reference html-wireframe-guide.md for detailed standards.

- [ ] **Step 2: Verify Phase 2 section references layout-patterns.md correctly**

Confirm Step 4 says "Read references/layout-patterns.md for detailed HTML skeletons and layout rules" at the right point.

---

### Task 5: Write SKILL.md — Phase 3-4 Workflow (Steps 7-11)

**Files:**
- Modify: `deckdone/SKILL.md`

- [ ] **Step 1: Append Phase 3: Content section (Steps 7-8)**

Content from spec Section 4, Phase 3. Include the mandatory structured task template for content-plan.md (from spec Section 8.2).

- [ ] **Step 2: Append Phase 4: Implementation section (Steps 9-11)**

Content from spec Section 4, Phase 4. Include:
- Step 9: Test generation with template locking
- Step 10: Batch generation with section chunking and space competition check
- Step 11: Final quality review referencing quality-checklist.md

For Steps 9-11, include the specific html2pptx and thumbnail.py commands from the pptx skill.

- [ ] **Step 3: Verify Phase 3-4 mentions pptx skill commands**

Confirm the plan references:
- `html2pptx()` function from pptx skill
- `python scripts/thumbnail.py` from pptx skill
- Sharp rasterization commands

---

### Task 6: Write SKILL.md — Harness Engineering and Final Sections

**Files:**
- Modify: `deckdone/SKILL.md`

- [ ] **Step 1: Append Harness Engineering Principles section**

Content from spec Section 8, condensed for SKILL.md:
- Verification loop principle (refer to quality-checklist.md for details)
- Structured task template principle (referenced in Step 7)
- Execution trace principle (referenced in State Update Protocol)
- Harness improvement principle with the core quote

This section should be concise (~50 lines) — the details live in reference files.

- [ ] **Step 2: Append State File Templates section**

Include the template for:
- `deckdone-state.md` (from spec Section 7)
- `deckdone-trace.md` (from spec Section 8.3)
- `harness-improvements.md` (from spec Section 8.4)

- [ ] **Step 3: Verify SKILL.md total line count**

Run: `wc -l deckdone/SKILL.md`
Expected: 400-550 lines. If over 550, move content to reference files.

---

## Chunk 2: Reference Files

### Task 7: Write references/layout-patterns.md

**Files:**
- Create: `deckdone/references/layout-patterns.md`

- [ ] **Step 1: Write the page type library**

Content from spec Section 5 (layout-patterns.md). Must include:

1. **Table of Contents** listing all 12+ page types
2. For each page type:
   - Name and description
   - Typical use case
   - HTML skeleton (minimal working example with zone structure)
   - Layout rules (zone ratios, flexbox patterns)
   - Content density guidelines (max text elements, recommended font sizes, max characters per zone)
3. **Special Composite-Diagram patterns** section:
   - Nested-box architecture layout (3-level deep example)
   - Agent/service matrix layout (grid example)
   - Layered stack layout (horizontal layers example)
   - Pipeline/flow layout (sequential stages example)

Each page type's HTML skeleton must use proper html2pptx conventions:
- `width: 720pt; height: 405pt` on body
- All text inside `<p>`, `<h1>`-`<h6>`, `<ul>`, or `<ol>` tags
- No CSS gradients (use pre-rendered PNGs)
- Web-safe fonts only

Target: ~300 lines.

- [ ] **Step 2: Verify HTML skeletons are valid**

For each HTML skeleton in the file, confirm:
- Body has correct dimensions
- All text is inside proper tags
- No CSS gradients used
- Flexbox is used for layout

---

### Task 8: Write references/narrative-frameworks.md

**Files:**
- Create: `deckdone/references/narrative-frameworks.md`

- [ ] **Step 1: Write the narrative frameworks reference**

Content from spec Section 5 (narrative-frameworks.md). Must include:

1. **Table of Contents**
2. Six frameworks, each with:
   - Name and structure description
   - When to use (audience × purpose matrix)
   - Example outline for a 20-page presentation
   - Page type suggestions per section
3. **Framework Selection Guide** — a decision tree or matrix:
   - Rows: purpose types (report, proposal, training, pitch, analysis)
   - Columns: audience types (executive, technical, mixed, external)
   - Cells: recommended framework(s)

Six frameworks:
1. SCQA (Situation-Complication-Question-Answer)
2. Pyramid Principle (conclusions-first)
3. Timeline (chronological narrative)
4. Problem-Solution-Benefit
5. Theme-Illustration-Application
6. Data-Insight-Action

Target: ~250 lines.

- [ ] **Step 2: Verify framework selection guide is complete**

Confirm all 6 frameworks have entries in the audience × purpose matrix.

---

### Task 9: Write references/audience-analysis.md

**Files:**
- Create: `deckdone/references/audience-analysis.md`

- [ ] **Step 1: Write the audience analysis reference**

Content from spec Section 5 (audience-analysis.md). Must include:

1. **Role-Level Categories** — executive, middle management, team/IC, external client, mixed — each with information needs and attention span characteristics
2. **Subject Familiarity Matrix** — expert, familiar, general, unfamiliar — each with impact on content depth and jargon level
3. **Decision-Making Tendency Models**:
   - Data-driven: wants numbers, charts, evidence
   - Story-driven: wants narratives, examples, case studies
   - Action-oriented: wants conclusions, next steps, clear asks
   - Detail-oriented: wants methodology, process, comprehensive coverage
4. **Audience-to-Design Impact Matrix** — how audience profile affects:
   - Narrative framework choice
   - Content density per slide
   - Visual style (formal vs. casual, minimal vs. rich)
   - Information hierarchy (conclusions-first vs. building up)

Target: ~150 lines.

---

### Task 10: Write references/style-presets.md

**Files:**
- Create: `deckdone/references/style-presets.md`

- [ ] **Step 1: Write the visual style presets reference**

Content from spec Section 5 (style-presets.md). Must include:

1. **Table of Contents** listing all presets
2. 15-20 style presets. Each preset:
   - Style name and mood description (1 sentence)
   - Color palette: primary, secondary, accent, background, text (hex values)
   - Typography: heading font, body font, size scale (heading/body/label/sizes)
   - Decoration patterns: border style, shape patterns, background treatment
   - Best suited for: presentation types + audience
   - Pre-render requirements: which effects need Sharp rasterization

Include the 18 color palettes from the existing pptx skill SKILL.md as a starting point, expanded with typography and decoration guidance for each.

3. **Custom Palette Creation Guide** — when to create a custom palette vs. use a preset

Target: ~200 lines.

---

### Task 11: Write references/html-wireframe-guide.md

**Files:**
- Create: `deckdone/references/html-wireframe-guide.md`

- [ ] **Step 1: Write the wireframe generation guide**

Content from spec Section 5 (html-wireframe-guide.md). Must include:

1. **Grayscale Color Scheme Rules** — specific hex values for wireframe elements
2. **Zone Labeling Conventions** — how to annotate content types in wireframes
3. **Visual Weight Annotation Syntax** — primary (dark), secondary (medium), auxiliary (light)
4. **Composite-Diagram Zone Structure Notation** — how to represent nested zones in wireframes
5. **Batch Display Strategy** — 5-8 pages per batch, section-based grouping
6. **Wireframe HTML Template** — a complete working wireframe HTML file showing all conventions
7. **Browser Preview Integration** — how to use webapp-testing skill for displaying wireframes

Target: ~150 lines.

- [ ] **Step 2: Verify wireframe template is valid HTML**

Confirm the wireframe template follows html2pptx conventions (correct dimensions, text in proper tags).

---

### Task 12: Write references/quality-checklist.md

**Files:**
- Create: `deckdone/references/quality-checklist.md`

- [ ] **Step 1: Write the quality validation checklist**

Content from spec Section 8.1 (Multi-Level Verification Loops). Must include:

1. **Table of Contents** organized by step number
2. Per-step validation sections:
   - Step 1 (brief.md): 4-5 checks
   - Step 2 (materials/): 3-4 checks
   - Step 3 (outline.md): 4-5 checks
   - Step 4 (layout-system.md): 4-5 checks
   - Step 5 (style-guide.md): 3-4 checks
   - Step 6 (wireframes/): 5-6 checks
   - Step 7 (content-plan.md): 5-6 checks
   - Step 9 (test-slides/): 5-6 checks
   - Step 10 (output.pptx): 4-5 checks
   - Step 11 (final.pptx): 5-6 checks
3. **Harness Improvement Protocol** — how to turn a failed check into a harness improvement entry
4. **Cross-Conversation Resume Validation** — what to check when resuming from deckdone-state.md

Each check should be a concrete, binary pass/fail question.

Target: ~200 lines.

---

### Task 13: Validate Reference Files Completeness

- [ ] **Step 1: Verify all reference files exist and have table of contents**

Run: `ls deckdone/references/`
Expected: 6 files.

Read the first 10 lines of each file. Confirm each has a Table of Contents.

- [ ] **Step 2: Verify SKILL.md references match actual files**

Search SKILL.md for all `references/` path references. Confirm each referenced file exists.

---

## Chunk 3: Scripts, Distribution, and Integration

### Task 14: Write scripts/validate-content-plan.py

**Files:**
- Create: `deckdone/scripts/validate-content-plan.py`

- [ ] **Step 1: Write the content plan validation script**

The script validates `content-plan.md` against structural rules. No external dependencies beyond Python stdlib.

**Functionality:**
1. Parse content-plan.md
2. For each slide section, verify:
   - "Page Type:" field is present and matches a known type
   - "Total Zones:" field is present and numeric
   - Each zone has: Type, Content (non-empty), Max Length, Visual Weight
   - No zone Content field is empty or contains only TBD/placeholder text
   - Acceptance Criteria section exists with at least 1 checkbox item
3. Print summary: total slides, total zones, pass/fail per slide
4. Exit code 0 if all pass, 1 if any fail

**Usage:**
```bash
python scripts/validate-content-plan.py content-plan.md
```

Target: ~100 lines.

- [ ] **Step 2: Test with a valid content-plan sample**

Create a temporary test file `test-content-plan.md` with a valid 2-slide content plan. Run the script against it. Expected: exit code 0.

- [ ] **Step 3: Test with an invalid content-plan sample**

Create a temporary test file with missing zones and empty Content fields. Run the script. Expected: exit code 1 with specific error messages.

- [ ] **Step 4: Clean up test files**

Delete temporary test files.

---

### Task 15: Write scripts/validate-html-slides.py

**Files:**
- Create: `deckdone/scripts/validate-html-slides.py`

- [ ] **Step 1: Write the HTML slide validation script**

The script validates HTML slide files for html2pptx compatibility. No external dependencies beyond Python stdlib.

**Functionality:**
1. Accept a directory path containing HTML slide files
2. For each .html file:
   - Parse the HTML
   - Verify body element has `width: 720pt; height: 405pt` (or other valid dimensions)
   - Verify all text is inside `<p>`, `<h1>`-`<h6>`, `<ul>`, or `<ol>` tags (no bare text in `<div>` or `<span>`)
   - Verify no CSS gradients (`linear-gradient`, `radial-gradient`) — these break html2pptx
   - Verify web-safe fonts only (Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact)
   - Verify all `<img>` src attributes reference existing files
3. Print summary per file
4. Exit code 0 if all pass, 1 if any fail

**Usage:**
```bash
python scripts/validate-html-slides.py wireframes/
```

Target: ~80 lines.

- [ ] **Step 2: Test with a valid HTML slide**

Create a temporary valid HTML slide file. Run the script. Expected: exit code 0.

- [ ] **Step 3: Test with an invalid HTML slide (bare text, gradient)**

Create a temporary invalid HTML slide with bare text in a div and a CSS gradient. Run the script. Expected: exit code 1 with specific errors.

- [ ] **Step 4: Clean up test files**

Delete temporary test files.

---

### Task 16: Write SETUP.md

**Files:**
- Create: `deckdone/SETUP.md`

- [ ] **Step 1: Write the installation guide**

Content from spec Section 6 (Distribution Strategy). Must include:

```markdown
# DeckDone Setup Guide

## Prerequisites
- Node.js 18+
- Python 3.10+
- opencode, Claude Code, or compatible AI coding tool

## Step 1: Install DeckDone Skill
[git clone to skills directory]

## Step 2: Install Required Dependencies

### pptx skill (required)
[git clone or npm install instructions]

### Runtime dependencies (required)
[npm install -g commands for pptxgenjs, playwright, sharp, react-icons]

### Playwright browser (required)
[npx playwright install chromium]

## Step 3 (Optional): Install Optional Skill Dependencies

### PDF support
[install pdf skill + pip install markitdown]

### Word document support
[install docx skill]

### Spreadsheet support
[install xlsx skill]

### Extended style presets
[install theme-factory skill]

## Verification
[Test command to verify installation]
```

Target: ~80 lines.

- [ ] **Step 2: Verify SETUP.md commands are accurate**

Read back all commands in SETUP.md. Confirm:
- npm package names are correct
- Python package names are correct
- File paths use the correct skills directory for opencode (`~/.config/opencode/skills/`)

---

### Task 17: Final Integration Validation

- [ ] **Step 1: Validate skill structure**

Run the skill-creator's quick_validate.py:

```bash
python C:/Users/gxlei/.config/opencode/skills/skill-creator/scripts/quick_validate.py deckdone/
```

Expected: All checks pass.

- [ ] **Step 2: Verify SKILL.md line count**

Run: `wc -l deckdone/SKILL.md`
Expected: 400-550 lines.

- [ ] **Step 3: Verify all cross-references are valid**

In SKILL.md, find all references to `references/` files and `scripts/` files. Confirm each referenced file exists in the deckdone/ directory.

- [ ] **Step 4: Verify all files exist**

```bash
ls -R deckdone/
```

Expected output should show:
```
SKILL.md
SETUP.md
LICENSE
references/
  layout-patterns.md
  narrative-frameworks.md
  audience-analysis.md
  style-presets.md
  html-wireframe-guide.md
  quality-checklist.md
scripts/
  validate-content-plan.py
  validate-html-slides.py
```

- [ ] **Step 5: Package the skill (optional)**

If skill-creator's package_skill.py is available:

```bash
python C:/Users/gxlei/.config/opencode/skills/skill-creator/scripts/package_skill.py deckdone/ ./dist
```

Expected: deckdone.skill file created in ./dist/

---

### Task 18: Clean Up Project Root

- [ ] **Step 1: Remove unpacked FY26BP files (build artifacts)**

```bash
rm -rf fy26bp_unpacked/
```

These were analysis artifacts, not part of the skill.

- [ ] **Step 2: Verify final project structure**

```bash
ls -R
```

Expected: `docs/` (with spec and plan), `deckdone/` (skill files), `FY26BP.pptx` (reference sample).
