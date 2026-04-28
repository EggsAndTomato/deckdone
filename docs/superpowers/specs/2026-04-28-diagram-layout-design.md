# Diagram Layout Support — Design Spec

**Date:** 2026-04-28
**Status:** Draft

## 1. Problem Statement

DeckDone's current 12 layout templates are text-container-oriented — each slide is a frame that holds content, with decoration independent of information semantics. The extracted reference slides (`extracted_images/page_01–13.png`) demonstrate a fundamentally different paradigm: **diagram-heavy, visual-metaphor-oriented slides** where the layout itself conveys meaning (gears = synergy, pyramid = hierarchy, triangle = tension, staircase = progression).

| Dimension | Current DeckDone | Target |
|-----------|-----------------|--------|
| Layout philosophy | Content-container + decoration | Visual metaphor + data structure |
| Layout-semantic coupling | Loose | Tight |
| Template approach | Fixed SVG + placeholder replacement | AI dynamic generation per page |
| Coverage | 12 standard types | 12 standard + 14 diagram types |

## 2. Architecture Decision

**Chosen: Extend deckdone-build (not create a new skill).**

Rationale:
- deckdone-build's SKILL.md can be slimmed (templates and style-presets are already in reference files), leaving room for diagram generation logic
- Single pipeline — all SVG files feed into the same PPTX converter; splitting into two skills adds coordination overhead with no benefit
- The standard/diagram split is a **generation strategy fork at Step 7**, not a skill boundary

## 3. File Structure Changes

```
skills/
  deckdone-plan/
    SKILL.md                                ← modify: Step 4-5 flow
    references/
      relationship-layout-map.md            ← NEW: 14-type mapping table
    scripts/
      validate-content-plan.py              ← extend: validate diagram-data references

  deckdone-build/
    SKILL.md                                ← slim: keep flow, move details to references
    references/
      style-presets.md                      ← existing (no changes needed)
      svg-constraints.md                    ← existing (no changes needed)
      layout-templates.md                   ← existing (no changes needed)
      diagram-specs.md                      ← NEW: 13 diagram type schemas + generation guides
      quality-checklist.md                  ← extend: diagram SVG check items
      sub-agent-protocols.md                ← extend: diagram sub-agent protocol
    scripts/
      validate-svg-slides.py                ← extend: diagram validation rules
    templates/                              ← no changes
```

Runtime outputs (per project):
```
<project-dir>/
  content-plan.md                           ← added: Relationship-Type field for diagram pages
  diagram-data/                             ← NEW directory
    P05_Hub-and-Spoke.md
    P07_Pyramid.md
    ...
  svg_output/                               ← unchanged: all SVGs land here
    P05_Hub-and-Spoke.svg
    ...
```

## 4. Relationship → Layout Mapping (14 Types)

The mapping table is stored in `deckdone-plan/references/relationship-layout-map.md`. The AI in Step 4 identifies content intent, matches to a relationship type, then assigns the corresponding page type.

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
| 时序 | Clear chronological order | Timeline | Horizontal axis + nodes + dates + descriptions |
| 漏斗 | Progressive narrowing/filtering, each stage subselects the previous | Filter-Funnel | Stacked trapezoids decreasing in width top→bottom |
| 交集 | Overlapping concepts sharing a common area | Overlapping-Spheres | 2-3 overlapping circles + intersection labels |
| 循环 | Iterative improvement loop, feedback-driven | Iterative-Cycle | Circular arrangement of steps + center label + directional arrows |
| 桥接 | Current state → target state with bridging path | Bridge-and-Gap | Left box (current) → bridge (path items) → right box (future) |

### Relationship Detection Heuristics (Step 4)

The AI applies these formal triggers in priority order to classify content:

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

If NO trigger fires, the page is classified as a standard text/content type. Multiple triggers? Earliest match wins (higher priority).

> **Note on Timeline:** 时序 (chronological order) uses the existing `Timeline` standard template in `layout-templates.md`. It is included in this table for classification completeness but does NOT use the diagram-data pathway — no `Content-Diagram` page type, no `diagram-data/` file, no `diagram-specs.md` entry.

## 5. Diagram-Data File Format

Each diagram page produces one `diagram-data/<page-slug>.md` file. The schema varies by Diagram Type, defined in `diagram-specs.md`. The data file is structured YAML, without visual coordinates or colors — only semantic structure.

### Schema by Type

**Hub-and-Spoke:**
```yaml
Type: Hub-and-Spoke
Center:
  Label: <text>
  Color-Role: primary
Branches:
  - Label: <text>
    Items: [<item1>, <item2>, ...]
  - ...
```

**Pyramid:**
```yaml
Type: Pyramid
Direction: top-down
Layers:
  - Label: <text>
    Color-Role: <role>
    Items: [<item1>, ...]
  - ...
```

**Dual-Gears:**
```yaml
Type: Dual-Gears
Left-Gear:
  Label: <text>
  Color-Role: primary
  Items: [<item1>, ...]
Right-Gear:
  Label: <text>
  Color-Role: accent
  Items: [<item1>, ...]
Center-Arrow:
  Label: <text>
```

**Tension-Triangle:**
```yaml
Type: Tension-Triangle
Nodes:
  - Label: <text>
  - Label: <text>
  - Label: <text>
Edges:
  - From: <node index>
    To: <node index>
    Label: <tension description>
```

**Bubble-Matrix:**
```yaml
Type: Bubble-Matrix
X-Axis: <label>
Y-Axis: <label>
Quadrants:
  Top-Right: <label>
  Top-Left: <label>
  Bottom-Right: <label>
  Bottom-Left: <label>
Bubbles:
  - Label: <text>
    X: <0.0–1.0>
    Y: <0.0–1.0>
    Size: small|medium|large
    Color-Role: <role>
Takeaway: <text>
```

**Staircase:**
```yaml
Type: Staircase
Steps:
  - Label: <text>
    Color-Role: <role>
    Items: [<item1>, ...]
  - ...
```

**Split-Comparison:**
```yaml
Type: Split-Comparison
Left:
  Label: <text>
  Color-Role: secondary
  Items: [<item1>, ...]
Right:
  Label: <text>
  Color-Role: accent
  Items: [<item1>, ...]
```

**Data-Card-Grid:**
```yaml
Type: Data-Card-Grid
Layout: 2x2|1x4
Cards:
  - Label: <text>
    Value: <number or text>
    Unit: <optional>
    Icon: <tabler icon hint>
  - ...
```

**Layered-Architecture:**
```yaml
Type: Layered-Architecture
Layers:
  - Label: <text>
    Color-Role: <role>
    Subcomponents:
      - Label: <text>
      - ...
  - ...
```

**Filter-Funnel:**
```yaml
Type: Filter-Funnel
Direction: top-down
Layers:
  - Label: <text>
    Color-Role: <role>
    Width: <percentage>
    Items: [<item1>, ...]
  - ...
```

**Overlapping-Spheres:**
```yaml
Type: Overlapping-Spheres
Circles:
  - Label: <text>
    Color-Role: <role>
  - Label: <text>
    Color-Role: <role>
  - Label: <text>
    Color-Role: <role>
Overlap-Labels:
  "1,2": <label for intersection of circles 1 and 2>
  "1,2,3": <label for three-way intersection>
```

**Iterative-Cycle:**
```yaml
Type: Iterative-Cycle
Direction: clockwise
Steps:
  - Label: <text>
  - ...
Center-Label: <text>
```

**Bridge-and-Gap:**
```yaml
Type: Bridge-and-Gap
Current-State:
  Label: <text>
  Color-Role: secondary
  Items: [<item1>, ...]
Future-State:
  Label: <text>
  Color-Role: accent
  Items: [<item1>, ...]
Bridge:
  Label: <text>
  Items: [<item1>, ...]
Gap-Analysis: <text>
```

### Design Principles

1. **No visual coordinates** — diagram-data contains only semantic structure; the AI maps this to SVG pixels at generation time.
2. **Color-Role abstraction** — values reference style-preset roles (`primary`, `secondary`, `accent`, `accent-light`, `bg`), never hardcoded hex.
3. **Icon auto-selection** — `Items` and `Labels` are used by the build phase AI to auto-select matching tabler icons via semantic match.

## 6. Plan Stage Changes (deckdone-plan)

### Step 4: Page Type Assignment

Current flow:
```
Analyze outline → assign Page-Type from {Cover, Agenda, ..., Closing}
```

New flow:
```
Analyze outline → for each page:
  1. Is this informational (presenting facts) or relational (expressing a relationship)?
  2. If informational → assign standard Page-Type
  3. If relational → match against relationship-layout-map → assign Content-Diagram + Relationship-Type
  4. Output to content-plan.md
```

### Step 5: Content Plan + Diagram Data

New outputs:
- `content-plan.md` — Diagram pages include `Relationship-Type` field
- `diagram-data/<page-slug>.md` — One file per diagram page, structured per Diagram Type schema

The plan-phase AI reads `diagram-specs.md` to understand the required structure, then fills in the diagram-data file based on the content outline.

### validate-content-plan.py Extension

- Validate that every Content-Diagram page has a corresponding `diagram-data/<page-slug>.md`
- Validate that each diagram-data file has a recognized `Type` with required fields present

## 7. Build Stage Changes (deckdone-build)

### Step 7: SVG Generation Fork

```
Main agent identifies two page groups:
  ├── Standard pages (Cover, Agenda, Content-Text, Data-Chart, ...)
  │   └── existing sub-agent protocol (template replacement, 3-5 pages/batch)
  │
  └── Diagram pages (Content-Diagram with Relationship-Type)
      └── NEW diagram sub-agent protocol (AI dynamic generation, 2-3 pages/batch)
```

Both groups write to the same `svg_output/` directory. All sub-agents launch in parallel.

### Diagram Sub-Agent Protocol

Added to `references/sub-agent-protocols.md`. Batch size: 2-3 diagram pages (smaller than standard because AI dynamic construction consumes more tokens than template replacement).

**Prompt template:**

```
You are generating diagram SVG slides. You are responsible for [N] diagram pages.

## Files to Read (READ ALL BEFORE GENERATING)
1. references/svg-constraints.md — MANDATORY rules
2. references/diagram-specs.md — read ONLY sections for: [Diagram Type 1, Diagram Type 2]
3. style-guide.md — color palette, typography
4. diagram-data/<page-slug>.md — for each page in this batch
5. extracted_images/page_XX.png — reference image (if annotated in diagram-specs)

## Design Context (LOCKED — use these exact values)
[Paste style-guide colors and fonts]

## Your Pages
- P##_<Name>: Diagram Type = <Type>
- P##_<Name>: Diagram Type = <Type>

## Generation Rules
1. One SVG per page: viewBox="0 0 1280 720" width="1280" height="720"
2. ALL svg-constraints.md rules — no exceptions
3. Apply LOCKED design context to all Color-Role references
4. Use <use data-icon="tabler-{filled|outline}/{name}"/> for icons
5. Save to svg_output/P##_<Name>.svg

## Output
Write SVG files to svg_output/. Return the list of file paths created.
```

### diagram-specs.md Structure

~350 lines total. For each of the 13 Diagram Types (excluding Timeline), define:
1. **Schema** — Required and optional fields in diagram-data
2. **Content Mapping** — How diagram-data fields map to SVG elements
3. **Color-Role → Fill** — How style-preset roles translate to SVG fills
4. **Reference Image** — Path to sample in `extracted_images/` (if available)
5. **Design Principle** — One-line description of the visual structure
6. **Constraints & Limits** — Max nodes/layers/branches, min requirements

Design principles per type:

| Diagram Type | Reference Image | Design Principle |
|-------------|----------------|------------------|
| Hub-and-Spoke | page_03.png | Center circle + radial lines to 4-6 branch cards; branches surround center at equal angular intervals |
| Pyramid | page_07.png | Segmented triangle, 3-4 layers; top layer narrowest, base widest; color gradient from accent (top) to primary (base) |
| Dual-Gears | page_10.png | Two interlocking gear shapes, left primary + right accent; labels etched inside each gear; upward synergy arrow between them |
| Tension-Triangle | page_08.png | Three nodes at triangle vertices + bidirectional arrow connectors; center gear icon at intersection point |
| Bubble-Matrix | page_06.png | 2×2 quadrant with labeled axes; bubbles positioned by X/Y, sized by Size field; top-right quadrant highlighted; bottom takeaway bar |
| Staircase | page_12.png | 3-5 ascending blocks left→right, each step higher than previous; Color-Role gradient light→accent; numbered badges on each step |
| Split-Comparison | page_02.png | Vertical divider splitting slide; left = secondary palette (past/gray), right = accent palette (future/blue); connecting lines between corresponding elements |
| Data-Card-Grid | page_04.png | 2×2 or 1×N cards with thin border; large accent-colored number + label + icon per card |
| Layered-Architecture | page_11.png | 2-4 horizontal stacked blocks; darker fill as layers descend; subcomponents as nested rounded rects within each layer |
| Filter-Funnel | None | 3-6 stacked trapezoids centered vertically; width decreases: 100% → 75% → 50% → 30%; labels centered in each layer, white on fill |
| Overlapping-Spheres | None | 2-3 circles with transparency fill (fill-opacity for overlap); intersection labels positioned at overlap centers |
| Iterative-Cycle | None | 4-6 steps arranged in circle; clockwise arrows between steps; center label inside a circle |
| Bridge-and-Gap | None | Left box (current state, secondary fill) → center bridge markup items → right box (future state, accent fill); gap text below bridge |

## 8. style-presets.md and Color-Role

Existing style-presets define these logical roles already present in the palette format:

| Color-Role | Maps to | Usage in Diagrams |
|-----------|---------|-------------------|
| `primary` | `Primary` in style-preset | Main structural elements (center node, base layers) |
| `secondary` | `Secondary` in style-preset | Supporting elements (branches, secondary layers) |
| `accent` | `Accent` in style-preset | Highlights, arrows, selected bubbles |
| `accent-light` | `Accent` in style-preset | Light fills applied via `fill-opacity="0.25"` on individual elements (NOT `<g opacity>`) |
| `bg` | `Background` in style-preset | Page background, card interiors |

**accent-light implementation:** Apply `fill="{{Accent}}"` + `fill-opacity="0.25"` on individual elements. This complies with `svg-constraints.md` (only `<g opacity>` is banned; per-element `fill-opacity` is allowed).

No changes needed to the 18 existing style presets.

## 9. Validation Extensions

### validate-svg-slides.py (diagram additions)

- Verify diagram SVGs contain expected structural elements per Diagram Type (e.g., Hub-and-Spoke must have at least one `<circle>`)
- Verify icon references use `<use data-icon="..."/>` syntax
- Verify no banned elements from svg-constraints.md
- Verify `viewBox="0 0 1280 720"`

### quality-checklist.md (diagram additions)

- Diagram fills use Color-Role consistency (same role same color across pages)
- All diagram-data fields are consumed (no data lost in translation)
- Branch/node counts match between diagram-data and SVG
- Text labels are complete and positioned legibly

## 10. Error Handling

### Malformed diagram-data.md
- `validate-content-plan.py` checks: file exists, `Type` field is a recognized type, required fields present, field types match schema
- Sub-agent receives validated data → no malformed input reaches generation

### Sub-Agent Generation Failure
- If a diagram sub-agent fails (timeout, invalid output), main agent:
  1. Identifies the failing pages from sub-agent output
  2. Re-delegates those pages to a fresh sub-agent (1-2 pages, tighter scope)
  3. Max 2 retries per page; on persistent failure, asks user: "regenerate with different parameters?"
- All diagram sub-agents run in parallel with standard sub-agents; failures in one don't block others

### Relationship-Type Match Failure
- If plan AI cannot match any relationship trigger (Section 4 heuristics yield no match), defaults to `Content-Text` or `Content-TwoCol`
- The AI does NOT force a diagram on content that doesn't fit any relationship type

### Diagram Data Exceeds Visual Space
- See Section 14 (Constraints & Limits table) — each type has a max and overflow behavior
- `validate-content-plan.py` checks node/layer/branch counts against limits before generation

## 11. Context Budget Analysis

| Phase | Standard pages (per batch) | Diagram pages (per batch) |
|-------|---------------------------|--------------------------|
| Batch size | 3-5 pages | 2-3 pages |
| Reference files loaded | layout-templates (~740 lines) | diagram-specs section (~30 lines) |
| Per-page data | content-plan zones (~15 lines) | diagram-data file (~30 lines) |
| Per-page output | ~120 lines SVG | ~180 lines SVG |
| Total context/batch | ~1500 lines | ~620 lines |

Main agent only sees sub-agent results (file paths), not intermediate SVG content. **Net gain: ~96% context savings**, consistent with existing protocol.

## 12. User Experience Impact

**No change.** The user's step sequence (1-8) is identical. The standard/diagram split is purely internal to Step 7.

The only user-visible change: during Step 5 review, diagram pages display as relationship placeholders in the wireframe rather than text-only blocks (a quality improvement).

## 13. Implementation Order

1. `deckdone-plan/references/relationship-layout-map.md` — mapping table
2. `deckdone-build/references/diagram-specs.md` — schemas + generation guides
3. Modify `deckdone-plan/SKILL.md` Step 4-5 flow
4. Extend `deckdone-plan/scripts/validate-content-plan.py`
5. Modify `deckdone-build/SKILL.md` Step 7 flow (fork logic)
6. Extend `deckdone-build/references/sub-agent-protocols.md` (diagram protocol)
7. Extend `deckdone-build/references/quality-checklist.md`
8. Extend `deckdone-build/scripts/validate-svg-slides.py`

## 14. Resolved Design Decisions

### extracted_images/ Retention
**Decision:** Keep `extracted_images/` permanently as reference assets. These serve as visual references for sub-agents during diagram SVG generation. Without them, the AI has no visual anchor for the target design quality.

### Mixed Pages (Standard Zones + Diagram)
**Decision:** A page is EITHER standard OR Content-Diagram, never both. If a diagram page needs auxiliary text (subtitle, interpretation, footnote), those are expressed as standard Zone entries in `content-plan.md` alongside the `Relationship-Type` field. The sub-agent renders these as text below or beside the diagram, not as part of the diagram structure.

### Diagram-Data Overflow
**Decision (Constraints & Limits):**

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
