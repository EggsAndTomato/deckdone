# HTML Wireframe Generation Guide

Reference for generating low-fidelity HTML wireframes during Step 5 (Content Wireframe Review). These wireframes are for **content and layout review only** — no visual styling.

---

## Design Principles

1. **Low-fidelity only** — gray borders, black text, no colors, no gradients, no decorative elements.
2. **Real content** — every zone contains actual text from the content plan, not placeholder text.
3. **Chart placeholders** — chart zones show type, title, axes, and key data points in a labeled box.
4. **Live browser review** — auto-refresh script enables real-time updates during AI-user discussion.
5. **Single file** — all slides in one HTML file with thumbnail navigation.

---

## HTML Structure

### Document Layout

```
┌──────────────────────────────────────────────────┐
│  Header: "Presentation Wireframe — [title]"      │
│  Slide count + density level                      │
├──────────────────────────────────────────────────┤
│                                                   │
│  Slide Container (16:9 proportional)              │
│  ┌─────────────────────────────────────────┐      │
│  │ Zone: [type] (weight)                   │      │
│  │ Real content text goes here             │      │
│  ├─────────────────────────────────────────┤      │
│  │ Zone: [type] (weight)                   │      │
│  │ Real content text goes here             │      │
│  │ Multiple lines of actual content        │      │
│  └─────────────────────────────────────────┘      │
│                                                   │
│  Slide number + page type label                   │
│                                                   │
├──────────────────────────────────────────────────┤
│  Thumbnail Navigation Bar                         │
│  [1] [2] [3] [4] [5] [6] ... [N]                │
└──────────────────────────────────────────────────┘
```

### Slide Container Sizing

- Width: `100%` of content area (max `960px` for readability)
- Aspect ratio: 16:9 (use `aspect-ratio: 16/9` or `padding-bottom: 56.25%`)
- Each slide separated by `2rem` vertical spacing
- Slide background: `#FFFFFF`
- Zone borders: `2px solid #CCCCCC`
- Zone background: `#F9F9F9`

---

## Zone Rendering

### Standard Zone

Each zone is a `<div>` with:

```html
<div class="zone" data-weight="primary">
  <div class="zone-label">[title] (primary)</div>
  <div class="zone-content">Actual content text goes here.</div>
</div>
```

### Zone Label Format

```
[type] (weight)
```

- **type**: `title`, `subtitle`, `body`, `bullet-list`, `data-table`, `chart-area`, `image-area`, `quote`, `timeline-item`, `comparison-col`, `icon-grid`, `label`
- **weight**: `primary`, `secondary`, `auxiliary`

### Zone Sizing by Weight

| Weight | Min height | Font size | Indication |
|--------|-----------|-----------|------------|
| primary | 60px | 16px | Bold label border (`#888888`) |
| secondary | 40px | 14px | Normal label border (`#CCCCCC`) |
| auxiliary | 24px | 12px | Light label border (`#DDDDDD`) |

---

## Chart Placeholder Zones

Chart zones are rendered as labeled placeholder boxes that include **structured data** for later SVG rendering. Each chart placeholder MUST include `data-chart-ref` (the template key from `charts_index.json`) and structured data fields.

```html
<div class="zone" data-weight="primary">
  <div class="zone-label">[chart-area] (primary)</div>
  <div class="chart-placeholder" data-chart-ref="bar_chart">
    <div class="chart-type">📊 Bar Chart</div>
    <div class="chart-title">2024 Monthly Sales Trend</div>
    <div class="chart-axes">X: Month (Jan-Dec) | Y: Sales (10k CNY)</div>
    <div class="chart-data">
      <dl>
        <dt>categories</dt><dd>["Jan", "Feb", "Mar", "Apr", "May", "Jun"]</dd>
        <dt>series</dt><dd>[{"name":"Sales","values":[45,52,48,61,55,72],"color":"primary"}]</dd>
        <dt>unit</dt><dd>10k CNY</dd>
      </dl>
    </div>
    <div class="chart-insight">Peak in Jun, overall upward trend</div>
  </div>
</div>
```

### Chart Placeholder Fields

| Field | Required | Description |
|-------|----------|-------------|
| data-chart-ref | Yes | Template key from `charts_index.json` (e.g., `bar_chart`, `timeline`, `pie_chart`). Guides which SVG template to use in deckdone-build. |
| Chart Type | Yes | Line / Bar / Pie / Scatter / Area / Stacked-Bar / Timeline / Process-Flow / etc. |
| Chart Title | Yes | What the chart shows |
| Axes | Conditional | X-axis and Y-axis descriptions (not for pie charts) |
| Data Points | Yes | **Structured `<dl>` format** (see below) — key-value pairs the chart should visualize |
| Key Insight | Recommended | One sentence — what conclusion the audience should draw |

### Chart Type Indicators

| Type | Indicator | data-chart-ref examples |
|------|-----------|------------------------|
| Line | 📈 | `line_chart` |
| Bar | 📊 | `bar_chart`, `horizontal_bar_chart`, `grouped_bar_chart` |
| Pie / Donut | 🥧 | `pie_chart`, `donut_chart` |
| Scatter | ⊕ | `scatter_chart`, `bubble_chart` |
| Area | △ | `area_chart`, `stacked_area_chart` |
| Stacked-Bar | 📊 (stacked) | `stacked_bar_chart` |
| Timeline | ⏱ | `timeline` |
| Process / Flow | ➡ | `process_flow`, `chevron_process`, `numbered_steps` |
| Matrix / Quadrant | ⊞ | `matrix_2x2` |
| Comparison | ⚖ | `comparison_table`, `comparison_columns`, `butterfly_chart` |

### Structured Data Format for Chart Zones

Every chart zone MUST include a `<dl>` element inside `<div class="chart-data">` with machine-readable data. This structure is consumed by deckdone-build Step 7 to generate actual chart SVG shapes.

**Bar / Grouped Bar / Stacked Bar charts:**
```html
<dl>
  <dt>categories</dt><dd>["East", "South", "North", "West"]</dd>
  <dt>series</dt><dd>[{"name":"Q3 Sales","values":[185,142,128,96],"color":"primary"}]</dd>
  <dt>unit</dt><dd>M CNY</dd>
</dl>
```

**Line / Area charts:**
```html
<dl>
  <dt>categories</dt><dd>["Jan", "Feb", "Mar", "Apr", "May", "Jun"]</dd>
  <dt>series</dt><dd>[{"name":"Revenue","values":[45,52,48,61,55,72],"color":"primary"}]</dd>
  <dt>unit</dt><dd>10k CNY</dd>
</dl>
```

**Pie / Donut charts:**
```html
<dl>
  <dt>segments</dt><dd>[{"label":"R&D","value":45,"color":"primary"},{"label":"Validation","value":20,"color":"secondary"},{"label":"Platform","value":15,"color":"accent"},{"label":"Sales","value":12,"color":"aux1"},{"label":"Compliance","value":8,"color":"aux2"}]</dd>
  <dt>unit</dt><dd>%</dd>
</dl>
```

**Timeline / Roadmap:**
```html
<dl>
  <dt>milestones</dt><dd>[
    {"date":"2025 Q1","label":"Foundation","desc":"Data platform + CDSS pilot","status":"completed"},
    {"date":"2025 Q2","label":"Core Scenarios","desc":"Imaging AI + VTE alert","status":"in-progress"},
    {"date":"2025 Q3","label":"Scale","desc":"Full product matrix","status":"planned"},
    {"date":"2025 Q4","label":"Ecosystem","desc":"Federated learning + SaaS","status":"planned"}
  ]</dd>
</dl>
```

**Process Flow / Pipeline:**
```html
<dl>
  <dt>stages</dt><dd>[
    {"title":"Stage 1","subtitle":"Automation","items":["Report generation","Quality control"],"color":"primary"},
    {"title":"Stage 2","subtitle":"Decision Support","items":["CDSS diagnosis","Drug safety"],"color":"secondary"},
    {"title":"Stage 3","subtitle":"Operations","items":["Smart scheduling","DRG management"],"color":"accent"}
  ]</dd>
</dl>
```

**Matrix 2x2:**
```html
<dl>
  <dt>axis_x</dt><dd>{"label":"Feasibility","low":"Low","high":"High"}</dd>
  <dt>axis_y</dt><dd>{"label":"Value","low":"Low","high":"High"}</dd>
  <dt>quadrants</dt><dd>[
    {"position":"top-right","title":"Priority Breakthrough","items":["Imaging AI","CDSS","Quality control"],"color":"primary"},
    {"position":"top-left","title":"Strategic Investment","items":["Multi-modal reasoning","Virtual MDT"],"color":"secondary"},
    {"position":"bottom-right","title":"Efficiency Optimization","items":["Auto-documentation","Smart triage"],"color":"accent"},
    {"position":"bottom-left","title":"Watch & Explore","items":["Rare disease scenarios"],"color":"aux1"}
  ]</dd>
</dl>
```

---

## Auto-Refresh Script

Include at the end of `<body>`:

```html
<script>
  setInterval(() => {
    sessionStorage.setItem('scrollPos', window.scrollY);
    location.reload();
  }, 3000);
  window.addEventListener('load', () => {
    const pos = sessionStorage.getItem('scrollPos');
    if (pos) window.scrollTo(0, parseInt(pos));
  });
</script>
```

This refreshes every 3 seconds, preserving scroll position so the user can watch changes in real-time during discussion.

---

## Thumbnail Navigation Bar

Fixed at the bottom of the viewport. Each thumbnail is a clickable link that scrolls to the corresponding slide.

```html
<nav class="thumbnail-bar">
  <a href="#slide-1" class="thumb active">1</a>
  <a href="#slide-2" class="thumb">2</a>
  ...
</nav>
```

- Height: `40px`
- Background: `#333333`
- Each thumbnail: `36px × 24px`, white text, dark background
- Active/current slide highlighted with `#666666` background
- Click scrolls to the slide's `id` anchor

---

## Layout Templates by Page Type

### Cover (3 Zones)

```
┌──────────────────────────────────┐
│                                   │
│    [title] Title text (primary)   │
│                                   │
│  [subtitle] Subtitle (secondary) │
│                                   │
│  [label] Author · Date (aux)     │
│                                   │
└──────────────────────────────────┘
```

Vertical centering. Title takes ~40% of height.

### Agenda (5 Zones)

```
┌──────────────────────────────────┐
│ [title] Agenda (primary)         │
├───────────────┬──────────────────┤
│ [bullet-list] │ [bullet-list]    │
│ Section 1     │ Section 3        │
│ (secondary)   │ (secondary)      │
├───────────────┼──────────────────┤
│ [bullet-list] │ [bullet-list]    │
│ Section 2     │ Section 4        │
│ (secondary)   │ (secondary)      │
└───────────────┴──────────────────┘
```

### Data-Chart (4 Zones)

```
┌──────────────────────────────────┐
│ [title] Chart title (primary)    │
├──────────────────────────────────┤
│                                   │
│  [chart-area] 📊 Line Chart      │
│  Monthly sales trend              │
│  X: Month | Y: Sales             │
│  (primary)                        │
│                                   │
├──────────────────────────────────┤
│ [body] Key insight (secondary)   │
├──────────────────────────────────┤
│ [label] Data source (auxiliary)  │
└──────────────────────────────────┘
```

### Comparison (3-4 Zones)

```
┌──────────────────────────────────┐
│ [title] Comparison title         │
├─────────────┬────────────────────┤
│ [comp-col]  │ [comp-col]         │
│ Option A    │ Option B           │
│ (secondary) │ (secondary)        │
├─────────────┼────────────────────┤
│ [body]      │ [body]             │
│ Criteria 1  │ Criteria 1        │
│ (secondary) │ (secondary)        │
└─────────────┴────────────────────┘
```

### Composite-Diagram (3-15 Zones)

Use nested `<div>` containers with heavier borders for outer levels:

```html
<div class="zone diagram-outer" style="border-width: 3px;">
  <div class="zone-label">[title] Architecture (primary)</div>
  <div class="zone diagram-group" style="border-width: 2px;">
    <div class="zone-label">[body] Subsystem A (secondary)</div>
    <div class="zone"><div class="zone-label">[body] Component 1 (secondary)</div></div>
    <div class="zone"><div class="zone-label">[body] Component 2 (secondary)</div></div>
  </div>
</div>
```

### Timeline

Horizontal stages with milestone nodes:

```html
<div class="zone" data-weight="primary">
  <div class="zone-label">[title] Timeline title (primary)</div>
  <div class="zone-content" style="font-size:20px;font-weight:bold">Timeline title</div>
</div>
<div class="timeline-row" data-timeline-structured="true">
  <div class="timeline-item">
    <div class="zone-label">[timeline-item] (secondary)</div>
    <div class="zone-content">
      <b>Date/Phase</b><br>Description text
    </div>
  </div>
  <div class="timeline-arrow">→</div>
  <!-- more items -->
</div>
```

Every Timeline page MUST:
- Use the `timeline-row` / `timeline-item` / `timeline-arrow` CSS classes (visual containers with borders and arrows)
- Include structured data in a chart-data `<dl>` with `milestones` array (see Structured Data Format above)
- Each milestone must have: date, label, desc, and status

### Pipeline-Flow

Horizontal stages with arrow indicators between zones:

```html
<div class="pipeline-row" data-pipeline-structured="true">
  <div class="pipeline-stage">
    <div class="zone-label">[body] (secondary)</div>
    <div class="zone-content">
      <b>Stage Title</b><br><span style="font-size:12px">Item 1 · Item 2</span>
    </div>
  </div>
  <div class="pipeline-arrow">→</div>
  <!-- more stages -->
</div>
```

Every Pipeline-Flow page MUST:
- Use `pipeline-row` / `pipeline-stage` / `pipeline-arrow` CSS classes (visual containers with borders and arrows)
- Include structured data in a chart-data `<dl>` with `stages` array (see Structured Data Format above)
- Each stage must have: title, subtitle, items

### Comparison

Side-by-side columns with visual dividers:

```html
<div class="two-col" data-comparison-structured="true">
  <div class="col">
    <div class="zone-label">[comparison-col] Option A (secondary)</div>
    <div class="zone-content">
      <b>Heading</b><br>Detail text
    </div>
  </div>
  <div class="col">
    <div class="zone-label">[comparison-col] Option B (secondary)</div>
    <div class="zone-content">
      <b>Heading</b><br>Detail text
    </div>
  </div>
</div>
```

### Composite-Diagram

Use nested `<div>` containers with heavier borders for outer levels. MUST include a chart-data `<dl>` with the diagram structure:

```html
<div class="zone diagram-outer" style="border-width: 3px;" data-diagram-structured="true">
  <div class="zone-label">[title] Architecture (primary)</div>
  <div class="chart-data">
    <dl>
      <dt>diagram_type</dt><dd>layered_stack</dd>
      <dt>layers</dt><dd>[
        {"name":"Application","items":["CDSS","Operations","Research"],"color":"primary"},
        {"name":"Cognition","items":["LLM","RAG","Agent"],"color":"secondary"},
        {"name":"Data","items":["HIS/EMR","Governance","Privacy"],"color":"accent"}
      ]</dd>
    </dl>
  </div>
  <div class="diagram-group" style="border-width: 2px;">
    <div class="zone-label">[body] Subsystem A (secondary)</div>
    <div class="zone-content">Component details</div>
  </div>
</div>
```

Valid `diagram_type` values: `layered_stack`, `nested_box`, `hub_spoke`, `matrix`, `freeform`.

---

## Content Writing Rules for Wireframes

1. **Real text only** — never use "Lorem ipsum", "placeholder", or "TBD".
2. **Actual bullet text** — write the real bullet points that will appear on the slide.
3. **Chart data summary** — include the key data points the chart should visualize.
4. **Respect density limits** — text volume should match the density level from `brief.md`.
5. **Zone count matches layout-system.md** — every page type has a defined zone range.

---

## Export to Markdown

When the user confirms all wireframes, export two files:

1. **`content-plan.md`** — per-zone content specification following the mandatory template in SKILL.md Step 5.
2. **`layout-skeleton.md`** — overview table + per-page zone summary (simplified from the HTML structure).

The `wireframes.html` file is retained as a visual reference but is not consumed by `deckdone-build`.
