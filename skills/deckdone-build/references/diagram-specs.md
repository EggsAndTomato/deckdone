# Diagram Type → SVG Generation

Reference for generating diagram slides using programmatic SVG (not AI-generated). Each diagram type is implemented as a function in `scripts/diagram_svg.py`.

## How It Works

When a page has `Page Type: Content-Diagram`, the build phase:
1. Reads `diagram-data/<page-slug>.md` for structured content
2. Parses the YAML data into a Python dict
3. Calls `draw_diagram(diagram_key, data, style)` from `diagram_svg.py`
4. The function returns a complete SVG string with precise coordinates calculated programmatically
5. The SVG is saved to `svg_output/` and converted to PPTX via `svg_to_pptx.py`

No sub-agents, no AI generation — pure deterministic Python code computing pixel positions with math.

## Diagram Key Mapping

| DeckDone Type | diagram_key | Function |
|--------------|-------------|----------|
| Pyramid | `pyramid` | Gradient-layered triangle |
| Hub-and-Spoke | `hub_spoke` | Center circle + 4 corner cards |
| Dual-Gears | `dual_gears` | Two circles + synergy arrow |
| Tension-Triangle | `tension_triangle` | 3 nodes + connector edges |
| Bubble-Matrix | `bubble_matrix` | 2×2 grid + sized bubbles |
| Staircase | `staircase` | Ascending blocks + badges |
| Split-Comparison | `split_comparison` | Vertical divider + dual sides |
| Data-Card-Grid | `data_card_grid` | Card grid with large numbers |
| Layered-Architecture | `layered_architecture` | Stacked blocks + subcomponents |
| Filter-Funnel | `filter_funnel` | Centered trapezoids |
| Overlapping-Spheres | `overlapping_spheres` | Circles with fill-opacity |
| Iterative-Cycle | `iterative_cycle` | Circular arrangement + center |
| Bridge-and-Gap | `bridge_gap` | Current → bridge → future |
| Timeline | `timeline_diagram` | Horizontal axis + nodes |

## SVG Quality

All SVGs feature:
- Gradient fills for depth (via `<linearGradient>`)
- Drop shadows on cards (via `<filter>`)
- Rounded corners on cards (via `<path>` arc commands)
- Accent color highlights
- Type-specific visual treatments
