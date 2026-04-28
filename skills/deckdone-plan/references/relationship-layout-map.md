# Relationship → Layout Map

Reference for Step 4 (Page Type Assignment). Maps content relationships to Content-Diagram page types.

---

## 1. How to Use

In Step 4, the AI analyzes each page in the content outline. For every page:

1. **Run the detection heuristics** (Section 3) — first match wins, priority-ordered.
2. **If matched:** Assign `Content-Diagram` page type with the corresponding `Relationship Type`.
3. **If no match:** Assign a standard page type per `references/layout-types.md`.

Pages assigned Content-Diagram write a companion `diagram-data/<page-slug>.md` file (see Section 4).

---

## 2. Mapping Table

| Relationship | Content Signal | Page Type | Visual Description |
|---|---|---|---|
| 层级 (Hierarchy) | Clear top-down/bottom-up: strategy→tactics→execution | Pyramid | Segmented triangle, top-narrow bottom-wide |
| 中心辐射 (Hub-and-Spoke) | One core concept + N parallel sub-domains radiating outward | Hub-and-Spoke | Center circle + radial connector lines + branch cards |
| 双驱联动 (Dual-Gears) | Two independent systems driving one goal together | Dual-Gears | Two interlocking gears + labels per gear + synergy arrow |
| 张力 (Tension) | Triangular relationship with unresolvable contradictions | Tension-Triangle | Three interconnected nodes in triangle + bidirectional arrows |
| 优先级 (Priority) | Two-dimensional evaluation (value + feasibility), items to position | Bubble-Matrix | 2×2 quadrant grid + variably-sized bubbles |
| 递进 (Progression) | Ordered phase evolution (3-5 steps), each dependent on prior | Staircase | Ascending step blocks + labels per stage |
| 对比 (Contrast) | Side-by-side comparison of two perspectives, non-tabular | Split-Comparison | Visual dividing line + dual-color zones + per-side icons |
| 数据KPI (Data KPI) | A set of key numeric indicators; data itself is the persuasion | Data-Card-Grid | 2×2 or 1×N cards + large numbers + icons |
| 分层系统 (Layered System) | Multi-layer architecture, subcomponents within layers, dependencies | Layered-Architecture | Horizontal stacked blocks + nested subcomponents + connectors |
| 时序 (Chronology) | Clear chronological order | Timeline | Horizontal axis + nodes + dates + descriptions |
| 漏斗 (Funnel) | Progressive narrowing/filtering, each stage subselects the previous | Filter-Funnel | Stacked trapezoids decreasing in width top→bottom |
| 交集 (Intersection) | Overlapping concepts sharing a common area | Overlapping-Spheres | 2-3 overlapping circles + intersection labels |
| 循环 (Cycle) | Iterative improvement loop, feedback-driven | Iterative-Cycle | Circular arrangement of steps + center label + directional arrows |
| 桥接 (Bridge) | Current state → target state with bridging path | Bridge-and-Gap | Left box (current) → bridge (path items) → right box (future) |

> **Note:** `Timeline` uses the existing standard template (see `references/layout-types.md`), NOT the diagram-data pathway. It is included here for classification completeness only. When detected, assign the standard `Timeline` page type — do not generate a `diagram-data/` file.

---

## 3. Detection Heuristics

Apply in priority order. First match wins. No match → fall back to standard page type per `layout-types.md`.

| Priority | Trigger (check content for...) | → Type |
|---|---|---|
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

### Heuristic Application Notes

- **Confidence thresholds:** If keywords are found but content structure contradicts the expected shape (e.g., "漏斗" but only 2 stages), skip the match and continue down the priority list.
- **Context window:** Analyze the page title, key points, and section headers — not just body text. Title-level keywords carry more weight than incidental body mentions.
- **Language:** Heuristics are written for Chinese content (the primary use case) but English equivalents are valid triggers. Match on semantic intent, not exact keywords.

---

## 4. Diagram Data File

Content-Diagram pages generate a companion `diagram-data/<page-slug>.md` file that defines the diagram structure. This file is consumed by `deckdone-build` during Step 7/8 to render the diagram SVG.

### Slug Convention

`P##_diagram-name.svg` → lowercase name with hyphens. Drop the page number prefix for the slug.

Examples:

| Page Name | Slug |
|---|---|
| P05_Hub-and-Spoke | `hub-and-spoke` |
| P08_Bubble-Matrix | `bubble-matrix` |
| P12_Filter-Funnel | `filter-funnel` |

### Diagram Data Schema

Each diagram type has a specific data schema defined in `deckdone-build/references/diagram-specs.md`. The `<page-slug>.md` file must conform to the schema for its type. Schemas define required fields, node limits, label formats, and optional metadata.

### File Location

```
skills/deckdone-plan/workdir/<deck-name>/
  content-plan.md
  layout-skeleton.md
  diagram-data/
    hub-and-spoke.md
    bubble-matrix.md
    filter-funnel.md
    ...
```

The diagram-data directory is created alongside content-plan.md and layout-skeleton.md at the end of Step 5.

---

## 5. Constraints & Limits

Each diagram type has maximum node/layer/branch limits and overflow behavior. These are enforced at Step 5 (content wireframe) and again at Step 7 (SVG generation).

| Diagram Type | Max Nodes/Layers/Branches | Overflow Behavior |
|---|---|---|
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

### Overflow Severity

- **Reject + request split:** Content exceeds layout capacity; AI must split into two separate Content-Diagram pages.
- **Truncate:** Content exceeds visual capacity but layout can accommodate the structure. Drop excess items with a logged warning.
- **Error:** Constraint is a hard structural limit. Stop processing and alert the user.
- **Adapt:** Adjust presentation (smaller bubbles/cards) rather than dropping content.
