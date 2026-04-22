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

Chart zones are rendered as labeled placeholder boxes instead of real charts:

```html
<div class="zone" data-weight="primary">
  <div class="zone-label">[chart-area] (primary)</div>
  <div class="chart-placeholder">
    <div class="chart-type">📊 Line Chart</div>
    <div class="chart-title">2024 Monthly Sales Trend</div>
    <div class="chart-axes">X: Month (Jan-Dec) | Y: Sales (10k CNY)</div>
    <div class="chart-data">Peak in Jun, overall upward trend</div>
  </div>
</div>
```

### Chart Placeholder Fields

| Field | Required | Description |
|-------|----------|-------------|
| Chart Type | Yes | Line / Bar / Pie / Scatter / Area / Stacked-Bar |
| Chart Title | Yes | What the chart shows |
| Axes | Conditional | X-axis and Y-axis descriptions (not for pie charts) |
| Data Points | Yes | Key values, ranges, or trends the chart should convey |
| Key Insight | Recommended | One sentence — what conclusion the audience should draw |

### Chart Type Indicators

| Type | Indicator |
|------|-----------|
| Line | 📈 |
| Bar | 📊 |
| Pie | 🥧 |
| Scatter | ⊕ |
| Area | △ |
| Stacked-Bar | 📊 (stacked) |

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

### Pipeline-Flow (3-13 Zones)

Horizontal stages with arrow indicators between zones:

```html
<div class="pipeline-row">
  <div class="zone stage">[body] Stage 1 (secondary)</div>
  <div class="arrow">→</div>
  <div class="zone stage">[body] Stage 2 (secondary)</div>
  <div class="arrow">→</div>
  <div class="zone stage">[body] Stage 3 (secondary)</div>
</div>
```

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
