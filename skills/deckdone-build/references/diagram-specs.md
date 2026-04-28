# Diagram Generation Specifications

Reference for AI sub-agents generating diagram SVGs. Each diagram type maps structured `diagram-data/*.md` fields to SVG elements.

## General Rules

- All SVGs: `viewBox="0 0 1280 720"` `width="1280"` `height="720"`
- Follow ALL `svg-constraints.md` rules without exception
- Apply Color-Role from style-guide.md:
  - `primary` → Primary hex
  - `secondary` → Secondary hex
  - `accent` → Accent hex
  - `accent-light` → Accent hex + `fill-opacity="0.25"` on individual elements (NOT `<g opacity>`)
  - `bg` → Background hex
- Icons: use `<use data-icon="tabler-{outline|filled}/{name}" x="..." y="..." width="..." height="..." fill="..."/>`
- Text: separate `<text>` elements per line (no multi-line `<tspan>`)
- Rounded rects: `<path>` with arc commands, never `<rect rx="">`

## Diagram Types

### 1. Hub-and-Spoke

**Reference:** extracted_images/page_03.png

**Schema (diagram-data/\<page-slug\>.md):**
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

---

### 2. Pyramid

**Reference:** extracted_images/page_07.png

**Schema (diagram-data/\<page-slug\>.md):**
```yaml
Type: Pyramid
Direction: top-down
Layers:
  - Label: <text>
    Color-Role: <role>
    Items: [<item1>, ...]
```

**Design Principle:** Segmented triangle, 3-4 layers; top layer narrowest, base widest; color gradient from accent-light (top) → accent → secondary → primary (base).

**Content Mapping:**
- `Layers[i].Label` → text centered in layer band
- `Layers[i].Items` → bullet list below label within layer
- Layer bands rendered as trapezoids: top narrowest, each subsequent layer wider
- Pyramid centered at (640, 360), total height ~520px

**Color-Role:**
- Top layer: accent-light fill
- Mid layers: accent → secondary fills
- Base layer: primary fill
- Text: white on all fills

**Constraints:** Min 3 layers, max 5. Each layer ≤ 4 items. Labels ≤ 15 chars. Overflow: truncate, log warning.

---

### 3. Dual-Gears

**Reference:** extracted_images/page_10.png

**Schema (diagram-data/\<page-slug\>.md):**
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

**Design Principle:** Two interlocking gear shapes, left primary + right accent; labels inside each gear; upward synergy arrow between them.

**Content Mapping:**
- `Left-Gear.Label` → text centered in left gear circle
- `Right-Gear.Label` → text centered in right gear circle
- `Left-Gear.Items` / `Right-Gear.Items` → listed beside respective gear
- `Center-Arrow.Label` → text on synergy arrow between gears
- Gears rendered as circles with uniform gear-teeth path (e.g., 8 teeth)
- Center-Arrow rendered above or between gears

**Color-Role:**
- Left gear: primary fill with fill-opacity="0.25", primary stroke (2px)
- Right gear: accent fill with fill-opacity="0.25", accent stroke (2px)
- Gear labels: primary text inside gears
- Arrow + label: accent elements

**Constraints:** ≤ 5 items per gear. Labels ≤ 12 chars. Overflow: truncate to 5.

---

### 4. Tension-Triangle

**Reference:** extracted_images/page_08.png

**Schema (diagram-data/\<page-slug\>.md):**
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

**Design Principle:** Three nodes at triangle vertices; bidirectional arrow connectors along each edge; center gear icon at intersection point.

**Content Mapping:**
- `Nodes[i].Label` → text at vertex position
- `Edges[k].Label` → text centered along connector edge
- Triangle vertices: top center (640, 140), bottom-left (300, 540), bottom-right (980, 540)
- Center icon: tabler gear/gear icon at triangle centroid (640, 380)
- Edges rendered as bidirectional arrows (arrowheads at both ends)

**Color-Role:**
- Nodes: primary outline circle (r=40) + bg fill, primary text
- Edges: accent stroke (2px), accent arrowheads
- Edge labels: primary text, font-size 14
- Center icon: secondary fill

**Constraints:** Exactly 3 nodes (error if ≠ 3). Labels ≤ 15 chars. Edges must connect valid node pairs (0,1,2).

---

### 5. Bubble-Matrix

**Reference:** extracted_images/page_06.png

**Schema (diagram-data/\<page-slug\>.md):**
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

**Design Principle:** 2×2 quadrant grid with labeled axes; bubbles positioned by X/Y coordinates; top-right quadrant highlighted; bottom takeaway bar.

**Content Mapping:**
- `X-Axis` / `Y-Axis` → axis labels on horizontal and vertical edges
- `Quadrants.*` → labels at quadrant corners
- `Bubbles[i].X` / `Bubbles[i].Y` → center position mapped to pixel grid: (120 + X × 1040, 600 - Y × 460)
- `Bubbles[i].Size` → circle radius: small=25, medium=40, large=55
- `Bubbles[i].Label` → text centered inside bubble
- `Takeaway` → text in colored bar at slide bottom (y=670, height=50)

**Color-Role:**
- Quadrant background: bg fill
- Top-right quadrant: accent-light fill highlight
- Bubbles: fill determined by per-bubble Color-Role (primary/accent/secondary), text white on fill
- Takeaway bar: primary fill, white text

**Constraints:** ≤ 10 bubbles. Labels ≤ 12 chars. Overflow: reduce bubble size; abbreviate labels.

---

### 6. Staircase

**Reference:** extracted_images/page_12.png

**Schema (diagram-data/\<page-slug\>.md):**
```yaml
Type: Staircase
Steps:
  - Label: <text>
    Color-Role: <role>
    Items: [<item1>, ...]
```

**Design Principle:** 3-5 ascending blocks left→right; each step higher than previous; Color-Role gradient light → accent; numbered circle badges on each step.

**Content Mapping:**
- `Steps[i].Label` → text in step block
- `Steps[i].Items` → bullet list below label within block
- Step blocks: ascending from bottom-left (x=120, y=540) toward top-right (x=1160, y=180)
- Each step block: width=250, height=150, with 40px x-offset and 90px y-step increment
- Numbered badge: circle with step number (1, 2, 3...) on each step block

**Color-Role:**
- Step fill: gradient from accent-light (first step) through accent to primary (last step)
- Badge circles: accent fill, white number text
- Labels: primary text on accent-light steps, white text on darker steps

**Constraints:** Min 3 steps, max 5. Each step ≤ 4 items. Labels ≤ 15 chars. Overflow: reject and request split.

---

### 7. Split-Comparison

**Reference:** extracted_images/page_02.png

**Schema (diagram-data/\<page-slug\>.md):**
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

**Design Principle:** Vertical divider splitting slide; left = secondary palette, right = accent palette; connecting dashed lines between corresponding items.

**Content Mapping:**
- `Left.Label` → header text on left side (x=300, y=120)
- `Right.Label` → header text on right side (x=980, y=120)
- `Left.Items` / `Right.Items` → listed vertically on respective sides
- Dashed connector lines between corresponding items at same index (stroke-dasharray="6,4")
- Items positioned at y=220 + k × 65, where k = item index; max 6 positions

**Color-Role:**
- Left side: secondary fill with fill-opacity="0.12", primary text
- Right side: accent fill with fill-opacity="0.12", primary text
- Divider line: accent stroke (2px) at x=640
- Connector lines: secondary stroke (1.5px), dashed

**Constraints:** ≤ 6 items per side. Labels ≤ 15 chars. Overflow: truncate to 6.

---

### 8. Data-Card-Grid

**Reference:** extracted_images/page_04.png

**Schema (diagram-data/\<page-slug\>.md):**
```yaml
Type: Data-Card-Grid
Layout: 2x2|1x4
Cards:
  - Label: <text>
    Value: <number or text>
    Unit: <optional>
    Icon: <tabler icon hint>
```

**Design Principle:** 2×2 or 1×N cards with thin border; large accent-colored number/value with label + icon per card.

**Content Mapping:**
- `Cards[i].Value` → large text (font-size 42, bold) centered in card
- `Cards[i].Unit` → appended after value (font-size 18)
- `Cards[i].Label` → text below value (font-size 16)
- `Cards[i].Icon` → tabler icon beside label
- 2×2 layout: cards at (280, 200), (1000, 200), (280, 500), (1000, 500)
- 1×4 layout: cards at x={280, 560, 840, 1120}, y=340
- Each card: 280×220 area with 1px stroke border

**Color-Role:**
- Card background: bg fill
- Card border: secondary stroke (1px)
- Value numbers: accent fill
- Labels: primary text
- Icons: accent fill

**Constraints:** ≤ 6 cards (supports 2×3 layout). Value text ≤ 20 chars. Labels ≤ 15 chars. Overflow: switch to smaller card format.

---

### 9. Layered-Architecture

**Reference:** extracted_images/page_11.png

**Schema (diagram-data/\<page-slug\>.md):**
```yaml
Type: Layered-Architecture
Layers:
  - Label: <text>
    Color-Role: <role>
    Subcomponents:
      - Label: <text>
      - ...
```

**Design Principle:** 2-4 horizontal stacked blocks; darker fill as layers descend; subcomponents as nested rounded rects within each layer.

**Content Mapping:**
- `Layers[i].Label` → text on left edge of layer bar (x=120, vertically centered in bar)
- `Layers[i].Subcomponents[j].Label` → text inside nested rounded rect within layer
- Layer bars: width=1000, height=120, horizontally centered, stacked vertically with 20px gaps
- Subcomponent rects within layer: positioned after label, width=180, height=50, 10px gaps
- Arrows connecting subcomponents between adjacent layers where alignment suggests dependencies

**Color-Role:**
- Top layer: accent-light fill
- Mid layers: accent → secondary fills
- Bottom layer: primary fill
- Layer labels: white text on darker fills, primary text on light fills
- Subcomponent rects: bg fill, secondary stroke (1px)
- Subcomponent text: primary

**Constraints:** ≤ 4 layers, ≤ 5 subcomponents per layer. Labels ≤ 15 chars. Overflow: truncate subcomponents.

---

### 10. Filter-Funnel

**No reference image**

**Schema (diagram-data/\<page-slug\>.md):**
```yaml
Type: Filter-Funnel
Direction: top-down
Layers:
  - Label: <text>
    Color-Role: <role>
    Width: <percentage>
    Items: [<item1>, ...]
```

**Design Principle:** 3-6 stacked trapezoids centered vertically; width decreases: 100% → 75% → 50% → 30% for typical 4-layer funnel; labels centered in each layer.

**Content Mapping:**
- `Layers[i].Label` → text centered horizontally and vertically in trapezoid (white on fill)
- `Layers[i].Width` → percentage mapped to pixel width: Width% × 900px
- `Layers[i].Items` → small text below or beside layer (font-size 12)
- Trapezoids centered at x=640, stacked vertically with ~8px gaps
- Top trapezoid starts at y=120, total height spans ~520px
- Trapezoid rendering: `<path>` with top edge at calculated width and bottom edge at next layer's width

**Color-Role:**
- Top layer: accent-light fill
- Mid layers: accent → secondary fills
- Bottom layer: primary fill
- Text: white on all fills

**Constraints:** Min 3 layers, max 6. Labels ≤ 12 chars. Each layer ≤ 4 items. Overflow: reject and request split.

---

### 11. Overlapping-Spheres

**No reference image**

**Schema (diagram-data/\<page-slug\>.md):**
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

**Design Principle:** 2-3 overlapping circles with fill-opacity for visible intersection; labels at overlap centers.

**Content Mapping:**
- `Circles[i].Label` → text centered in circle
- `Overlap-Labels` → text positioned at intersection centroid of specified circles
- 2 circles: positioned at (460, 360) and (820, 360), r=220, horizontally overlapping
- 3 circles: positioned as equilateral triangle around (640, 360), r=200
- Intersection centroids calculated from circle positions (simple average of involved circle centers)

**Color-Role:**
- Each circle: its Color-Role fill with `fill-opacity="0.35"`
- Circle text: primary bold, centered in circle
- Overlap labels: primary bold, font-size 16

**Constraints:** 2-3 circles (error if > 3; Venn diagram limit). Labels ≤ 15 chars. Overlap labels required only when multiple circles present.

---

### 12. Iterative-Cycle

**No reference image**

**Schema (diagram-data/\<page-slug\>.md):**
```yaml
Type: Iterative-Cycle
Direction: clockwise
Steps:
  - Label: <text>
  - Label: <text>
  - ...
Center-Label: <text>
```

**Design Principle:** 4-6 steps arranged in circle; clockwise arrows between steps; center label inside a circle.

**Content Mapping:**
- `Steps[i].Label` → text at angular position on circle, angle = i × (360°/N) starting from top
- Step nodes: circles (r=50) at (640 + 260 × cos(angle), 360 + 260 × sin(angle))
- Arrows: curved paths with arrowheads between consecutive steps (after last → back to first)
- `Center-Label` → text centered in circle at (640, 360), r=80

**Color-Role:**
- Step nodes: primary stroke (2px), bg fill, primary text
- Arrows: accent stroke (2.5px) with arrowheads
- Center circle: secondary fill, primary text

**Constraints:** 4-6 steps (reject if < 4 or > 6). Labels ≤ 12 chars.

---

### 13. Bridge-and-Gap

**No reference image**

**Schema (diagram-data/\<page-slug\>.md):**
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

**Design Principle:** Left box (current state, secondary) → bridge → right box (future state, accent); gap analysis text below bridge.

**Content Mapping:**
- `Current-State.Label` → header in left box, `Current-State.Items` → bullet list below
- `Future-State.Label` → header in right box, `Future-State.Items` → bullet list below
- `Bridge.Label` → text centered in bridge section, `Bridge.Items` → path steps with arrow connectors
- `Gap-Analysis` → explanatory text below bridge, italic
- Left box: x=100–520, y=160–540 (secondary palette zone)
- Right box: x=760–1180, y=160–540 (accent palette zone)
- Bridge: centered between boxes at x=560–720, y=360, with Bridge.Items as horizontal sequence

**Color-Role:**
- Current-State box: secondary fill with fill-opacity="0.12", secondary stroke (1px)
- Future-State box: accent fill with fill-opacity="0.12", accent stroke (1px)
- Bridge: primary stroke (2px), primary-labeled items
- Gap-Analysis: primary text, italic, font-size 14

**Constraints:** ≤ 4 items per state. Labels ≤ 15 chars. Overflow: truncate.
