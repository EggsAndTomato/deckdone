# Diagram Type → SmartArt Template

Diagram pages use native PowerPoint SmartArt via template injection. 150+ templates are available in `templates/smartart/`.

## How It Works

1. Plan phase assigns `Page Type: Content-Diagram` and `Relationship Type`
2. Build phase AI selects the best SmartArt template from this mapping
3. `inject(pptx, out, slide, template_key, texts=data)` injects the template with content
4. WPS/PowerPoint renders the SmartArt natively

## Relationship Type → SmartArt Template Mapping

| DeckDone Relationship | Recommended SmartArt Template(s) |
|----------------------|--------------------------------|
| 层级 (Pyramid) | `pyramid/pyramid1` (Basic Pyramid), `pyramid/pyramid3` (Pyramid List) |
| 中心辐射 (Hub-and-Spoke) | `cycle/radial1`, `relationship/radial1` |
| 双驱联动 (Dual-Gears) | `relationship/gear1` |
| 张力 (Tension-Triangle) | `relationship/balance1` |
| 优先级 (Bubble-Matrix) | `matrix/matrix1` (Basic Matrix) |
| 递进 (Staircase) | `process/process1`, `process/chevron1` |
| 对比 (Split-Comparison) | `relationship/opposingArrows` |
| 数据KPI (Data-Card-Grid) | `list/vList1`, `list/vList2` |
| 分层系统 (Layered-Architecture) | `hierarchy/hierarchy1`, `hierarchy/hierarchy2` |
| 过滤漏斗 (Filter-Funnel) | `relationship/funnel1` |
| 交集 (Overlapping-Spheres) | `relationship/venn1` |
| 循环 (Iterative-Cycle) | `cycle/cycle1` |
| 桥接 (Bridge-and-Gap) | `relationship/equation1` |
| 时序 (Timeline) | `process/process1` |

## Full Catalog

See `references/smartart-catalog.md` for the complete 150+ template index organized by 8 categories.
