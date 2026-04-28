# Diagram Layout Support — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 14 diagram-type slide layouts to DeckDone, enabling AI to dynamically generate diagram SVGs (Hub-and-Spoke, Pyramid, Dual-Gears, etc.) from structured diagram-data files.

**Architecture:** Extend deckdone-build's Step 7 with a generation fork: standard pages continue using layout templates, while diagram pages are dispatched to sub-agents that read diagram-data files + reference images + diagram-specs to dynamically construct SVGs. No new skill created — all changes contained within existing plan/build skills.

**Tech Stack:** Python stdlib (validate scripts), SVG xml.etree, markdown/YAML for diagram-data files.

**Spec:** `docs/superpowers/specs/2026-04-28-diagram-layout-design.md`

---

## File Map

| File | Operation | Responsibility |
|------|-----------|---------------|
| `skills/deckdone-plan/references/relationship-layout-map.md` | **Create** | 14-relationship→layout mapping table with detection heuristics |
| `skills/deckdone-build/references/diagram-specs.md` | **Create** | 13 diagram type schemas, content mappings, design principles, reference image paths |
| `skills/deckdone-plan/SKILL.md` | **Modify** | Step 4: add relationship detection flow; Step 5a: add diagram-data generation; Step 5b: validate diagram-data |
| `skills/deckdone-plan/scripts/validate-content-plan.py` | **Modify** | Add Content-Diagram page type, validate diagram-data/ files exist and are well-formed |
| `skills/deckdone-build/SKILL.md` | **Modify** | Step 7a: add diagram page detection + fork dispatch; add per-page-type rules for diagram types |
| `skills/deckdone-build/references/sub-agent-protocols.md` | **Modify** | Add Diagram SVG sub-agent prompt template and batch rules |
| `skills/deckdone-build/references/quality-checklist.md` | **Modify** | Add Step 7 diagram-specific quality checks |
| `skills/deckdone-build/scripts/validate-svg-slides.py` | **Modify** | Add diagram-type-aware graphical element validation |

---

## Chunk 0: Conventions & Prerequisites

**Page Slug Convention:** Page slugs are derived from the SVG filename pattern `P##_Name.svg`:
- Lowercase the name portion, replace spaces with hyphens
- Example: `P05_Hub-and-Spoke.svg` → slug = `p05_hub-and-spoke`
- The slug is used as the diagram-data filename: `diagram-data/<slug>.md`
- The slug is used to match SVGs to diagram types in validators

**Validators locate diagram-data files by:**
1. Parsing content-plan.md for pages with `Relationship Type: <X>`
2. Deriving the slug from page number and title
3. Looking for `diagram-data/<slug>.md` relative to project directory

### Task 1.1: Create relationship-layout-map.md

**Files:**
- Create: `skills/deckdone-plan/references/relationship-layout-map.md`

- [ ] **Step 1: Write the file**

Content: 14-row mapping table (Relationship + Content Signal + Page Type + Visual Description) and 14-priority detection heuristic table (Trigger → Type). Use content from spec Section 4.

```markdown
# Relationship → Layout Mapping

## How to Use

In Step 4 of deckdone-plan, the AI analyzes each outline page to determine whether its content expresses a relationship that benefits from a diagram layout. If a relationship is detected, the AI assigns `Page Type: Content-Diagram` and specifies the `Relationship Type`. If no relationship is detected, a standard page type is used.

## Mapping Table

| Relationship | Content Signal | Page Type | Visual Description |
|-------------|---------------|-----------|-------------------|
| 层级 | Clear top-down/bottom-up structure: strategy→tactics→execution | Pyramid | Segmented triangle, top-narrow bottom-wide |
| 中心辐射 | One core concept + N parallel sub-domains radiating outward | Hub-and-Spoke | Center circle + radial connector lines + branch cards |
| 双驱联动 | Two independent systems driving one goal together | Dual-Gears | Two interlocking gears + labels per gear + synergy arrow |
| 张力 | Triangular relationship with unresolvable contradictions | Tension-Triangle | Three interconnected nodes in triangle + bidirectional arrows |
| 优先级 | Two-dimensional evaluation (value + feasibility), items to position | Bubble-Matrix | 2×2 quadrant grid + variably-sized bubbles |
| 递进 | Ordered phase evolution (3-5 steps), each dependent on prior | Staircase | Ascending step blocks + labels per stage |
| 对比 | Side-by-side comparison of two perspectives, non-tabular | Split-Comparison | Visual dividing line + dual-color zones + per-side icons |
| 数据KPI | A set of key numeric indicators; data itself is the persuasion | Data-Card-Grid | 2×2 or 1×N cards + large numbers + icons |
| 分层系统 | Multi-layer architecture, subcomponents within layers, dependencies | Layered-Architecture | Horizontal stacked blocks + nested subcomponents + connectors |
| 时序 | Clear chronological order | Timeline | Horizontal axis + nodes + dates + descriptions; **uses standard Timeline template, NOT diagram-data pathway** |
| 漏斗 | Progressive narrowing/filtering, each stage subselects the previous | Filter-Funnel | Stacked trapezoids decreasing in width top→bottom |
| 交集 | Overlapping concepts sharing a common area | Overlapping-Spheres | 2-3 overlapping circles + intersection labels |
| 循环 | Iterative improvement loop, feedback-driven | Iterative-Cycle | Circular arrangement of steps + center label + directional arrows |
| 桥接 | Current state → target state with bridging path | Bridge-and-Gap | Left box (current) → bridge (path items) → right box (future) |

## Detection Heuristics (Priority-Ordered)

Apply these triggers in order. First match wins. If NO trigger fires, default to a standard page type.

| Priority | Trigger (check content for...) | → Type |
|---------|-------------------------------|--------|
| 1 | Two dimensions being evaluated simultaneously, items positioned on both axes | Bubble-Matrix |
| 2 | Two entities described as requiring each other, mutual dependency language ("双轮驱动", "协同", "互为") | Dual-Gears |
| 3 | Three forces/constraints in conflict, trade-off language ("张力", "矛盾", "博弈") | Tension-Triangle |
| 4 | Ordered phases (3-5), each described as building on the previous ("第N步", "阶段N", "后依赖前") | Staircase |
| 5 | One core concept with sister sub-domains radiating from it ("围绕", "四大赛道", "N大板块") | Hub-and-Spoke |
| 6 | Explicit tag words: "顶层/中层/底层", "战略/战术/执行", "上→下" hierarchy | Pyramid |
| 7 | Explicit tag words: "过去/未来", "传统/新", "Before/After", "vs" | Split-Comparison |
| 8 | Explicit tag words: "漏斗", "筛选", "转化", narrowing progression | Filter-Funnel |
| 9 | Explicit tag words: "交集", "重叠", "融合", "交叉" | Overlapping-Spheres |
| 10 | Explicit tag words: "循环", "闭环", "迭代", "反馈" | Iterative-Cycle |
| 11 | Explicit tag words: "现状→目标", "差距", "桥接", "转型路径", "as-is to-be" | Bridge-and-Gap |
| 12 | Architecture/stack language: "层", "架构", "系统分层", components within components | Layered-Architecture |
| 13 | Key numbers as primary content, minimal prose, metric-heavy | Data-Card-Grid |
| 14 | Sequential timeline dates | Timeline |

## Diagram Data File

For pages assigned `Page Type: Content-Diagram`, an additional `diagram-data/<page-slug>.md` file is generated in Step 5. The schema per diagram type is defined in `deckdone-build/references/diagram-specs.md`.

## Constraints & Limits

| Diagram Type | Max Nodes/Layers/Branches | Overflow Behavior |
|-------------|--------------------------|-------------------|
| Hub-and-Spoke | 6 branches | Reject and request split into two pages |
| Pyramid | 5 layers | Truncate; log warning |
| Dual-Gears | 5 items per gear | Truncate to 5 |
| Tension-Triangle | Exactly 3 nodes | Error if ≠ 3 |
| Bubble-Matrix | 10 bubbles | Reduce bubble size; label smaller bubbles with abbreviations |
| Staircase | 5 steps | Reject and request split |
| Split-Comparison | 6 items per side | Truncate |
| Data-Card-Grid | 6 cards (2×3 layout) | Switch to smaller card format |
| Layered-Architecture | 4 layers, 5 subcomponents each | Truncate subcomponents |
| Filter-Funnel | 6 layers | Reject and request split |
| Overlapping-Spheres | 3 circles | Error if > 3 (Venn limit) |
| Iterative-Cycle | 6 steps | Reject and request split |
| Bridge-and-Gap | 4 items per state | Truncate |
```

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone-plan/references/relationship-layout-map.md
git commit -m "feat(plan): add relationship-to-layout mapping reference"
```

---

### Task 1.2: Create diagram-specs.md

**Files:**
- Create: `skills/deckdone-build/references/diagram-specs.md`

- [ ] **Step 1: Write the file**

Content: 13 diagram type entries, each with Schema, Content Mapping, Color-Role rules, Reference Image path, Design Principle, and Constraints. Use content from spec Sections 5 and 7.

The file structure per type:

```markdown
# Diagram Generation Specifications

Reference for AI sub-agents generating diagram SVGs. Each diagram type maps structured `diagram-data/*.md` fields to SVG elements.

## General Rules

- All SVGs: viewBox="0 0 1280 720" width="1280" height="720"
- Follow ALL svg-constraints.md rules
- Apply Color-Role from style-guide.md:
  - `primary` → Primary hex color
  - `secondary` → Secondary hex color
  - `accent` → Accent hex color
  - `accent-light` → Accent hex + fill-opacity="0.25" on individual elements
  - `bg` → Background hex color
- Icons: use `<use data-icon="tabler-{outline|filled}/{name}" x="..." y="..." width="..." height="..." fill="..."/>`
- Text: separate `<text>` elements per line (no multi-line tspan)
- Rounded rects: `<path>` with arc commands, never `<rect rx="">`

## Diagram Types

### 1. Hub-and-Spoke

**Reference:** extracted_images/page_03.png

**Schema (diagram-data/<page>.md):**
```yaml
Type: Hub-and-Spoke
Center:
  Label: <text>
  Color-Role: primary
Branches:
  - Label: <text>
    Items: [<item1>, ...]
```

**Design Principle:** Center circle + radial connector lines to 4-6 branch cards; branches surround center at equal angular intervals.

**Content Mapping:**
- `Center.Label` → text centered in large circle at SVG center (640, 360)
- `Branches[i].Label` → card title
- `Branches[i].Items` → bullet list within card
- Branch cards positioned at equal angular intervals (360°/N) on radius ~200px from center

**Color-Role:**
- Center circle: primary fill, white text
- Connector lines: accent stroke, 2px width
- Branch cards: secondary stroke (1px), bg fill, primary text for titles

**Constraints:** Min 3 branches, max 6. Each branch ≤ 4 items. Labels ≤ 15 chars.

### 2. Pyramid

**Reference:** extracted_images/page_07.png

**Schema:**
```yaml
Type: Pyramid
Direction: top-down
Layers:
  - Label: <text>
    Color-Role: <role>
    Items: [<item1>, ...]
```

**Design Principle:** Segmented triangle, 3-4 layers; top layer narrowest, base widest; color gradient from accent (top) to primary (base).

**Content Mapping:**
- `Layers[i].Label` → centered text in layer band
- `Layers[i].Items` → small text list below layer label
- Layer band heights: equal division of triangle height
- Layer band widths: proportional (top=40% → middle=70% → base=100%)

**Color-Role:**
- Top layer: accent-light fill
- Middle layers: accent → secondary fill
- Bottom layer: primary fill
- Text: white on filled bands, primary color for labels outside

**Constraints:** Min 3 layers, max 5. Each layer ≤ 4 items. Labels ≤ 15 chars.
```

Continue for the remaining 11 types (Dual-Gears, Tension-Triangle, Bubble-Matrix, Staircase, Split-Comparison, Data-Card-Grid, Layered-Architecture, Filter-Funnel, Overlapping-Spheres, Iterative-Cycle, Bridge-and-Gap) following the same format: Schema, Design Principle, Content Mapping, Color-Role, Constraints. Use spec Sections 5 and 7 for content.

Each type entry should be ~20-30 lines. Total file ~350 lines.

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone-build/references/diagram-specs.md
git commit -m "feat(build): add diagram generation specs for 13 types"
```

---

## Chunk 2: Plan Skill Modifications

### Task 2.1: Modify deckdone-plan SKILL.md (Step 4-5)

**Files:**
- Modify: `skills/deckdone-plan/SKILL.md`

- [ ] **Step 1: Add relationship detection to Step 4**

In `skills/deckdone-plan/SKILL.md`, modify the Step 4 section (currently lines 177-191) to add relationship detection before page type assignment.

Replace lines 179-184:
```
1. Read `references/layout-types.md` for page type definitions. Assign a page type to each page based on the outline.
2. Read `references/density-presets.md` for visual element density targets. Prefer visual page types over text-only types: Data-Chart for metrics, Timeline for sequences, Comparison for side-by-side, Pipeline-Flow for processes, Composite-Diagram for architectures. Only use Content-Text when no visual type fits.
3. For Composite-Diagram and Pipeline-Flow types: identify sub-layout zones.
4. Confirm page type assignments with the user.
```

With:
```
1. Read `references/layout-types.md` for standard page type definitions.
2. Read `references/relationship-layout-map.md` for diagram type definitions and detection heuristics.
3. For each page in the outline, determine whether the content warrants a diagram layout:
   - Apply the detection heuristics (priority-ordered triggers) from relationship-layout-map.md.
   - If a relationship type match is found → assign `Page Type: Content-Diagram` and `Relationship Type: <matched type>`.
   - If no match → assign a standard page type from layout-types.md.
4. Read `references/density-presets.md` for visual element density targets. Prefer visual page types over text-only types: Data-Chart for metrics, Timeline for sequences, Comparison for side-by-side, Pipeline-Flow for processes, Composite-Diagram for architectures. Only use Content-Text when no visual type fits.
5. For Composite-Diagram, Pipeline-Flow, and Content-Diagram types: identify sub-layout zones.
6. Confirm page type assignments with the user.
```

- [ ] **Step 2: Add diagram-data generation to Step 5a**

In Step 5 (lines 194-231), add a sub-step between 5a (wireframe) and 5b (export) for diagram-data generation.

After the wireframe review loop (current line 213), insert before 5b:

```
#### 5a-2. Diagram Data Generation (for Content-Diagram pages only)

For each Content-Diagram page from layout-system.md:
  - Read `deckdone-build/references/diagram-specs.md` to understand the required data structure for the diagram type.
  - Based on the wireframe content, fill in a `diagram-data/<page-slug>.md` file following the schema for the diagram type.
  - Each file must include: `Type`, required fields per type, and all content.
  - The slug follows the convention: P##_Name.svg → lowercase name with hyphens → e.g., `p05_hub-and-spoke`.
Ensure each diagram-data file complies with the constraints limits (max branches/nodes/layers per type).
```

Note: The existing 5b numbering (steps 6-7) shifts to 8-9. Do NOT renumber the existing text — add the new step before 5b.

- [ ] **Step 3: Add diagram-data to deliverable list**

Add `diagram-data/` to the deliverables table (lines 50-60) and the Step 5 deliverable list (line 226).

In the deliverables table add:
```
| `diagram-data/` | 2 | 5 | Per-page diagram structured data (for Content-Diagram pages) |
```

In the Step 5 deliverable line update:
```
**Deliverable:** `wireframes.html` + `content-plan.md` + `layout-skeleton.md` + `diagram-data/`
```

- [ ] **Step 4: Commit**

```bash
git add skills/deckdone-plan/SKILL.md
git commit -m "feat(plan): add relationship detection and diagram-data generation to Steps 4-5"
```

---

### Task 2.2: Extend validate-content-plan.py

**Files:**
- Modify: `skills/deckdone-plan/scripts/validate-content-plan.py`

- [ ] **Step 1: Add Content-Diagram to valid page types**

Add `"Content-Diagram"` to `VALID_PAGE_TYPES` (line 7):

```python
VALID_PAGE_TYPES = {
    "Cover",
    "Agenda",
    "Section Divider",
    "Content-Text",
    "Content-TwoCol",
    "Data-Chart",
    "Quote",
    "Timeline",
    "Comparison",
    "Closing",
    "Composite-Diagram",
    "Pipeline-Flow",
    "Content-Diagram",  # <-- NEW
}
```

- [ ] **Step 2: Add diagram-data validation**

Add a new function `validate_diagram_data(content_plan_path)` that:

1. Parses content-plan.md for pages with `Page Type: Content-Diagram`
2. For each such page, verifies `Relationship Type` field is present and matches a known type
3. Checks that `diagram-data/<page-slug>.md` exists
3. Reads each diagram-data file and validates:
   - Has a `Type` field matching a known diagram type
   - Has the required fields for that type (per constraints below)
   - Respects max nodes/layers/branches limits

Required fields per type (minimal validation):
```python
DIAGRAM_REQUIRED_FIELDS = {
    "Hub-and-Spoke": ["Center", "Branches"],
    "Pyramid": ["Layers"],
    "Dual-Gears": ["Left-Gear", "Right-Gear"],
    "Tension-Triangle": ["Nodes"],
    "Bubble-Matrix": ["Bubbles"],
    "Staircase": ["Steps"],
    "Split-Comparison": ["Left", "Right"],
    "Data-Card-Grid": ["Cards"],
    "Layered-Architecture": ["Layers"],
    "Filter-Funnel": ["Layers"],
    "Overlapping-Spheres": ["Circles"],
    "Iterative-Cycle": ["Steps"],
    "Bridge-and-Gap": ["Current-State", "Future-State"],
}

DIAGRAM_MAX = {
    "Hub-and-Spoke": {"Branches": 6},
    "Pyramid": {"Layers": 5},
    "Dual-Gears": {"Items_per_gear": 5},
    "Tension-Triangle": {"Nodes": 3},
    "Bubble-Matrix": {"Bubbles": 10},
    "Staircase": {"Steps": 5},
    "Split-Comparison": {"Items_per_side": 6},
    "Data-Card-Grid": {"Cards": 6},
    "Layered-Architecture": {"Layers": 4, "Subcomponents_per_layer": 5},
    "Filter-Funnel": {"Layers": 6},
    "Overlapping-Spheres": {"Circles": 3},
    "Iterative-Cycle": {"Steps": 6},
    "Bridge-and-Gap": {"Items_per_state": 4},
}
```

- [ ] **Step 3: Integrate into main()**

Call the new validation function from `main()` after existing slide validation passes.

If diagram-data errors found: print each error and exit code 1.

- [ ] **Step 4: Test**

```bash
# Create a sample content-plan.md with one Content-Diagram page
python skills/deckdone-plan/scripts/validate-content-plan.py content-plan.md
# Expected: errors if Content-Diagram page has no diagram-data file
```

- [ ] **Step 5: Commit**

```bash
git add skills/deckdone-plan/scripts/validate-content-plan.py
git commit -m "feat(plan): add Content-Diagram and diagram-data validation"
```

---

## Chunk 3: Build Skill Modifications

### Task 3.1: Modify deckdone-build SKILL.md (Step 7 fork logic)

**Files:**
- Modify: `skills/deckdone-build/SKILL.md`

- [ ] **Step 1: Add diagram page detection to Step 7a**

In Step 7a (lines 99-123), after step 2 ("Lock design context"), add:

```
2.5 **Separate standard and diagram pages:**
   - Scan `content-plan.md` for pages with `Page Type: Content-Diagram`.
   - These pages require the diagram sub-agent protocol (see sub-agent-protocols.md).
   - Standard pages use the existing protocol.
```

And modify the batch splitting logic (lines 107-115) to note that diagram pages are split in smaller batches (2-3 pages) and use a different prompt template.

- [ ] **Step 2: Add diagram page visual element rules**

In Step 7a, after the existing per-page-type visual element rules section (lines 125-161), add:

```
#### Diagram Page Visual Element Rules (ADDITIONAL)

When a page has `Page Type: Content-Diagram` with `Relationship Type`:
- Read `references/diagram-specs.md` section for that relationship type.
- Read `diagram-data/<page-slug>.md` for structured layout data.
- Read `extracted_images/<reference>.png` if annotated in diagram-specs.
- Generate SVG dynamically (NOT from layout templates) following the Design Principle and Content Mapping from diagram-specs.md.
- All Color-Role references → locked style-guide.md colors.
- Icons auto-selected based on Label semantics.
- Must include graphical elements (paths, circles, lines) proportional to the diagram complexity — never render diagram data as text-only.
```

- [ ] **Step 3: Update deliverable list reference**

In Step 7 deliverable line (line 178), note that SVG files come from both standard and diagram sub-agents.

- [ ] **Step 4: Commit**

```bash
git add skills/deckdone-build/SKILL.md
git commit -m "feat(build): add diagram page fork logic to Step 7 SVG generation"
```

---

### Task 3.2: Extend sub-agent-protocols.md (diagram protocol)

**Files:**
- Modify: `skills/deckdone-build/references/sub-agent-protocols.md`

- [ ] **Step 1: Add diagram sub-agent section**

After the existing Step 7a protocol section (ends around line 196), add:

```markdown
---

## Step 7a (Diagram): Diagram SVG Generation

### Delegation Pattern

Diagram pages are dispatched to **separate** sub-agents from standard pages. They cannot share batches because the reference files and generation approach differ.

Batch size: 2-3 diagram pages per sub-agent (smaller than standard because AI dynamic SVG construction consumes more tokens).

Diagram sub-agents launch in parallel with standard sub-agents — all in the same message.

### Main Agent Responsibilities

1. After locking design context, scan `content-plan.md` for Content-Diagram pages.
2. Split diagram pages into batches (2-3 pages per batch).
3. Launch diagram sub-agents alongside standard sub-agents (same single-message dispatch).
4. All SVGs write to the same `svg_output/` directory regardless of source.

### Prompt Template

```
You are generating diagram SVG slides for a presentation. You are responsible for [N] diagram pages.

## Files to Read (READ ALL BEFORE GENERATING)

1. references/svg-constraints.md — SVG generation rules (MANDATORY — every rule must be followed)
2. references/diagram-specs.md — read ONLY the sections for the diagram types in your batch: [list types]
3. style-guide.md — color palette, typography, decoration patterns
4. For each page: diagram-data/<page-slug>.md — structured diagram data
5. extracted_images/page_XX.png — reference image (if annotated in diagram-specs for your types)

## Design Context (LOCKED — use these exact values for every page)

Primary: #XXXXXX
Secondary: #XXXXXX
Accent: #XXXXXX
Accent-Light: Primary with fill-opacity="0.25"
Background: #XXXXXX
Text Primary: #XXXXXX
Text Secondary: #XXXXXX
Heading Font: [font family] Bold, sizes: 42/36/30/24
Body Font: [font family], sizes: 18/16/14

## Your Pages

- P##_<Name>: Diagram Type = Hub-and-Spoke
- P##_<Name>: Diagram Type = Filter-Funnel
- ...

## Generation Rules

1. Each page = one SVG: viewBox="0 0 1280 720" width="1280" height="720"
2. ALL svg-constraints.md rules — no exceptions
3. Apply LOCKED design context to all Color-Role references
4. Use <use data-icon="tabler-{outline|filled}/{name}"/> for icon placeholders
5. Include a title zone at the top (consistent with standard pages for visual uniformity)
6. Render the diagram in the remaining body area
7. File naming: svg_output/P##_<Name>.svg
8. Start each SVG with <defs> block for gradients/filters

## Output

Write SVG files to svg_output/. Return the list of file paths created, in order.
```

### Context Budget (Diagram, per batch of 2-3 pages)

| Item | Lines |
|------|-------|
| svg-constraints.md | ~90 |
| diagram-specs section (1-2 types) | ~40 |
| diagram-data files (2-3 pages × 30 lines) | ~80 |
| Style-guide tokens | ~10 |
| Per-page SVG output (2-3 × 180 lines) | ~400 |
| **Total per batch** | **~600** |

### Diagram Sub-Agent Failure Recovery

If a diagram sub-agent fails (timeout, no output, invalid SVG):
1. **Main agent** identifies failing pages by checking which expected SVG files are missing or contain parse errors.
2. **Re-delegate** failing pages to a fresh sub-agent with 1-2 pages (tighter scope).
3. **Max 2 retries** per page.
4. **On persistent failure** (all retries exhausted): inform user with the last error output and ask: "Regenerate these pages with different parameters?" Do not silently skip.
5. Diagram sub-agent failures do NOT block standard sub-agents — standard SVGs are written independently.
```

- [ ] **Step 2: Update batch sizing guidance**

At the top of the file (General Rules, line 14), update batch sizing rule 6:

```
6. **Batch sizing for Step 7** — Standard pages: 3-5 pages per sub-agent. Diagram pages: 2-3 pages per sub-agent. For decks with both types, separate into standard and diagram groups, then split each group into batches.
```

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone-build/references/sub-agent-protocols.md
git commit -m "feat(build): add diagram SVG sub-agent protocol"
```

---

### Task 3.3: Extend quality-checklist.md (diagram checks)

**Files:**
- Modify: `skills/deckdone-build/references/quality-checklist.md`

- [ ] **Step 1: Add diagram-specific checks to Step 7**

In the Step 7 checklist section (after line 46), add:

```markdown
### Diagram SVG Checks (Content-Diagram pages)

- [ ] **All diagram-data fields are consumed** — no data lost in translation; every Label and Item from diagram-data/*.md appears in the SVG
- [ ] **Branch/node counts match** — e.g., Hub-and-Spoke SVG has as many branch cards as Branches[] in diagram-data
- [ ] **Color-Role consistency** — same role yields same hex color across all diagram SVGs in the deck
- [ ] **Diagram structure is recognizable** — the visual metaphor matches the relationship type (gears look like gears, pyramid looks like pyramid)
- [ ] **No text-only diagrams** — every diagram page contains graphical SVG elements (paths, circles, lines) beyond just `<text>`
- [ ] **Reference image alignment** — if a reference image was provided, the generated SVG uses the same visual structure (not necessarily pixel-identical, but same layout pattern)
- [ ] **Constraints respected** — no diagram exceeds its max nodes/layers/branches limit
```

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone-build/references/quality-checklist.md
git commit -m "feat(build): add diagram-specific quality checks"
```

---

### Task 3.4: Extend validate-svg-slides.py (diagram validation)

**Files:**
- Modify: `skills/deckdone-build/scripts/validate-svg-slides.py`

- [ ] **Step 1: Add Content-Diagram to visual page types**

Update the `VISUAL_PAGE_TYPES` set (line 200):

```python
VISUAL_PAGE_TYPES = {
    "chart", "timeline", "pipeline", "flow", "comparison", "diagram",
    "matrix", "process", "data-chart",
    "content-diagram",  # <-- NEW
}
```

This ensures Content-Diagram pages are checked for graphical element presence by the existing `_check_graphical_elements` function.

- [ ] **Step 2: Verify icon validation coverage**

**Verify that** the existing `_check_icons` function (line 161) already validates `<use data-icon="..."/>` syntax for all SVGs including diagram SVGs. No new function needed — the existing check covers diagram icons. Confirm `_check_icons` is called from `validate_file()`.

- [ ] **Step 3: Enhance diagram structure validation and content-plan parsing**

Update `parse_content_plan_pages` (line 266) to also extract the **specific diagram type** for Content-Diagram pages. The current function only extracts generic page type keywords. Add extraction of `Relationship Type` field:

```python
def parse_content_plan_pages(content_plan_path):
    """Returns list of (page_type, relationship_type_or_None) tuples."""
    try:
        with open(content_plan_path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"[WARN] Cannot read content-plan: {e}")
        return None

    pages = []
    # Parse each page block
    for m in re.finditer(
        r"##\s*Page\s+\d+[^#\n]*\n(.*?)(?=\n##\s*Page\s+\d+|\Z)",
        text,
        re.DOTALL | re.IGNORECASE,
    ):
        block = m.group(1).lower()
        # Extract relationship type for Content-Diagram pages
        rel_match = re.search(r"Relationship\s+Type\s*[:：]\s*(\S[^\n]*)", m.group(1), re.IGNORECASE)
        relationship_type = rel_match.group(1).strip().lower().replace(" ", "-") if rel_match else None
        
        if "content-diagram" in block and relationship_type:
            pages.append(("content-diagram", relationship_type))
        elif any(kw in block for kw in VISUAL_PAGE_TYPES):
            for kw in VISUAL_PAGE_TYPES:
                if kw in block and kw != "content-diagram":
                    pages.append((kw, None))
                    break
        else:
            pages.append((None, None))

    return pages if pages else None
```

Add the diagram structure checks function:

```python
DIAGRAM_MIN_ELEMENTS = {
    "hub-and-spoke": {"circle": 1, "path": 1},
    "pyramid": {"path": 3},
    "dual-gears": {"circle": 2},
    "tension-triangle": {"circle": 3},
    "bubble-matrix": {"line": 2, "circle": 1},
    "staircase": {"path": 3},
    "split-comparison": {"line": 1},
    "data-card-grid": {"path": 4},
    "layered-architecture": {"path": 4},
    "filter-funnel": {"path": 3},
    "overlapping-spheres": {"circle": 2},
    "iterative-cycle": {"circle": 4},
    "bridge-and-gap": {"path": 2},
}

def _check_diagram_structure(root, filename, content_plan_pages, errors):
    """Validate diagram SVGs have expected structural elements for their type."""
    if content_plan_pages is None:
        return
    
    # Match filename to content-plan page index
    page_num_match = re.match(r"p(\d+)", filename.lower(), re.IGNORECASE)
    if not page_num_match:
        return
    idx = int(page_num_match.group(1)) - 1
    if idx < 0 or idx >= len(content_plan_pages):
        return
    
    page_type, relationship_type = content_plan_pages[idx]
    if not relationship_type:
        return
    
    # Count SVG elements by local tag name
    element_counts = {}
    for elem in root.iter():
        tag = _local_tag(elem).lower()
        element_counts[tag] = element_counts.get(tag, 0) + 1
    
    # Check minimums
    requirements = DIAGRAM_MIN_ELEMENTS.get(relationship_type, {})
    for tag_name, min_count in requirements.items():
        actual = element_counts.get(tag_name, 0)
        if actual < min_count:
            errors.append(
                f"Diagram type '{relationship_type}' expects >= {min_count} "
                f"<{tag_name}> elements, found {actual}"
            )
```

- [ ] **Step 4: Integrate into validate_file()**

Call the diagram structure check from `validate_file()` (line 242) after the existing `_check_graphical_elements` call.

Also update `_classify_page_type` (line 206-218) to handle the new tuple format from `parse_content_plan_pages`:
```python
def _classify_page_type(filename, content_plan_pages):
    if content_plan_pages is None:
        return None
    base = filename.lower().replace("_", " ")
    for ptype in VISUAL_PAGE_TYPES:
        if ptype in base:
            return ptype
    page_num_match = re.match(r"p(\d+)", filename, re.IGNORECASE)
    if page_num_match and content_plan_pages:
        idx = int(page_num_match.group(1)) - 1
        if 0 <= idx < len(content_plan_pages):
            entry = content_plan_pages[idx]
            # Handle tuple format: (page_type, relationship_type_or_None)
            return entry[0] if isinstance(entry, tuple) else entry
    return None
```

- [ ] **Step 5: Test**

```bash
# Create a sample diagram SVG
python skills/deckdone-build/scripts/validate-svg-slides.py svg_output/ --content-plan content-plan.md --outline outline.md
# Expected: passes for valid diagram SVGs, fails for missing graphical elements
```

- [ ] **Step 6: Commit**

```bash
git add skills/deckdone-build/scripts/validate-svg-slides.py
git commit -m "feat(build): add diagram-type-aware SVG validation"
```

---

## Verification

After all chunks are complete, run a full end-to-end test:

1. Create a minimal project with one standard page and one diagram page
2. Run deckdone-plan Steps 1-5
3. Verify `content-plan.md` includes `Page Type: Content-Diagram` and `Relationship Type`
4. Verify `diagram-data/<page>.md` is generated with correct schema
5. Run `validate-content-plan.py` — should pass
6. Run deckdone-build Steps 6-8
7. Verify both SVGs are generated in `svg_output/`
8. Run `validate-svg-slides.py` — should pass
9. Convert to PPTX — should succeed
