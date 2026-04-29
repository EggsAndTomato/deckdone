# Diagram Type → Native Shape Mapping

Reference for generating diagram slides using python-pptx native shapes. Each diagram type is implemented as a function in `scripts/diagram_shapes.py`.

## How It Works

When a page has `Page Type: Content-Diagram`, the build phase:
1. Reads `diagram-data/<page-slug>.md` for structured content
2. Parses the YAML data into a Python dict
3. Calls `draw_diagram(slide, diagram_key, data, style)` from `diagram_shapes.py`
4. The function creates autoshapes, text boxes, and connectors on the slide

No sub-agents, no AI generation, no SVG — pure deterministic Python code. The approach mirrors WPS "智能图形": regular PowerPoint shapes with precise positioning.

## Diagram Key Mapping

| DeckDone Type | diagram_key | Function |
|--------------|-------------|----------|
| Pyramid | `pyramid` | `draw_pyramid()` |
| Hub-and-Spoke | `hub_spoke` | `draw_hub_spoke()` |
| Dual-Gears | `dual_gears` | `draw_dual_gears()` |
| Tension-Triangle | `tension_triangle` | `draw_tension_triangle()` |
| Bubble-Matrix | `bubble_matrix` | `draw_bubble_matrix()` |
| Staircase | `staircase` | `draw_staircase()` |
| Split-Comparison | `split_comparison` | `draw_split_comparison()` |
| Data-Card-Grid | `data_card_grid` | `draw_data_card_grid()` |
| Layered-Architecture | `layered_architecture` | `draw_layered_architecture()` |
| Filter-Funnel | `filter_funnel` | `draw_filter_funnel()` |
| Overlapping-Spheres | `overlapping_spheres` | `draw_overlapping_spheres()` |
| Iterative-Cycle | `iterative_cycle` | `draw_iterative_cycle()` |
| Bridge-and-Gap | `bridge_gap` | `draw_bridge_gap()` |
| Timeline | `timeline_diagram` | `draw_timeline_diagram()` |

## Data Format

Each `diagram-data/<page-slug>.md` file contains YAML matching the function's expected data structure. See `scripts/diagram_shapes.py` docstrings for each function's data format.

## Style Integration

Colors come from `style-guide.md` via a style dict:
```python
style = {
    'primary': RGBColor(...),      # from Style Guide Primary
    'secondary': RGBColor(...),    # from Style Guide Secondary
    'accent': RGBColor(...),       # from Style Guide Accent
    'bg': RGBColor(...),           # from Style Guide Background
    'text': RGBColor(...),         # from Style Guide Text
    'text_light': RGBColor(...),   # lighter text variant
    'font_heading': 'Arial',
    'font_body': 'Arial',
}
```

## Usage

```python
from diagram_shapes import draw_diagram

draw_diagram(slide, 'pyramid', data, style)
```
