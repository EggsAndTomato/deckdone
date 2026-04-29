# Diagram Type → SmartArt Layout Mapping

Reference for mapping DeckDone diagram types to PowerPoint native SmartArt layouts. The actual injection is handled by `scripts/smartart_inject.py`.

## How It Works

When a page has `Page Type: Content-Diagram`, the build phase:
1. Reads `diagram-data/<page-slug>.md` for structured content
2. Looks up this file to find the corresponding SmartArt layout key
3. Calls `SmartArtInjector.inject()` with the content items and layout key
4. PowerPoint/WPS loads the full layout definition from built-in resources via `uniqueId` URI

The layout is defined by a **minimal layout XML** referencing a Microsoft built-in layout URI — no custom layout algorithms needed. PowerPoint regenerates the visual rendering on first open.

## Diagram Type → SmartArt Layout Mapping

| DeckDone Type | SmartArt Key | SmartArt Layout | Description |
|--------------|-------------|----------------|-------------|
| Pyramid | `pyramid` | Basic Pyramid | Segmented triangle, top-to-bottom hierarchy |
| Hub-and-Spoke | `radial` | Basic Radial | Center circle + radiating branches |
| Dual-Gears | `gear` | Gear | Three interlocking gear shapes |
| Tension-Triangle | `converging` | Converging Radial | Three nodes converging to center |
| Bubble-Matrix | `matrix` | Basic Matrix | 2×2 quadrant grid |
| Staircase | `staircase` | Step Up Process | Ascending step blocks left→right |
| Split-Comparison | `opposing-arrows` | Opposing Arrows | Two sides with opposing arrows |
| Data-Card-Grid | `vlist` | Vertical Block List | Vertical blocks with text |
| Layered-Architecture | `hierarchy` | Hierarchy | Tree/hierarchy with layers |
| Filter-Funnel | `funnel` | Funnel | Stacked trapezoids, top→bottom |
| Overlapping-Spheres | `venn` | Basic Venn | 2-3 overlapping circles |
| Iterative-Cycle | `cycle` | Basic Cycle | Circular arrangement of steps |
| Bridge-and-Gap | `equation` | Equation | Left→bridge→right with connectors |

## Data Structure

All diagram types use a common item structure:

```python
items = [
    {
        'text': 'Main Node 1',
        'children': ['Sub 1a', 'Sub 1b']   # optional
    },
    {
        'text': 'Main Node 2',
        'children': ['Sub 2a']
    },
]
```

The `diagram-data/<page-slug>.md` file provides the content in this format. The injector converts it to SmartArt's `dataModel` XML with `parOf` connections.

### Type-Specific Guidance

**Pyramid:** Top item = tip, bottom item = base. Children appear inside each layer.

**Hub-and-Spoke / Radial:** Center item is implicit (derived from page title). Branch items form the spokes.

**Dual-Gears:** Three items → three gears. Children appear as labels beside each gear.

**Tension-Triangle:** Three items → three corner nodes.

**Bubble-Matrix:** Four items → four quadrants. Children = bubbles within each quadrant.

**Staircase:** Items in order → steps left to right. Children = sub-items within each step.

**Split-Comparison:** Two items → left vs right sides.

**Data-Card-Grid:** Items = cards. Children = metrics within each card.

**Layered-Architecture:** Items = layers top to bottom. Children = components within each layer.

**Filter-Funnel:** Items = funnel stages top to bottom.

**Overlapping-Spheres / Venn:** 2-3 items = circles. Each item's text is the circle label.

**Iterative-Cycle:** Items = steps around the circle.

**Bridge-and-Gap:** Three items = current state, bridge path, future state.

## Constraints

SmartArt handles layout, sizing, and text fitting natively. The only constraints are:

| Constraint | Value |
|-----------|-------|
| Max items per diagram | 10 (SmartArt limit for most layouts) |
| Max children per item | 5 |
| Max text length per item | 100 chars (truncated by SmartArt if exceeded) |
