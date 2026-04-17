# Layout Patterns — Page Type Library

## Table of Contents

1. [Cover](#1-cover)
2. [Agenda](#2-agenda)
3. [Section Divider](#3-section-divider)
4. [Content-Text](#4-content-text)
5. [Content-TwoCol](#5-content-twocol)
6. [Data-Chart](#6-data-chart)
7. [Quote](#7-quote)
8. [Timeline](#8-timeline)
9. [Comparison](#9-comparison)
10. [Closing](#10-closing)
11. [Composite-Diagram](#11-composite-diagram)
12. [Pipeline-Flow](#12-pipeline-flow)
13. [Composite Sub-Patterns](#13-composite-sub-patterns)

---

## 1. Cover

Full-bleed hero slide for opening a deck. Displays title, subtitle, and optional date/author. Use a solid background color or a pre-rendered PNG for visual impact.

**Typical use case:** First slide of any presentation.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         justify-content: center; align-items: center; padding: 60pt 80pt; box-sizing: border-box; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 36pt; text-align: center; margin: 0 0 12pt 0;">Title Here</h1>
  <p style="font-size: 18pt; text-align: center; margin: 0 0 24pt 0;">Subtitle goes here</p>
  <p style="font-size: 12pt; text-align: center; margin: 0;">Author · Date</p>
</div>
</body>
</html>
```

**Layout rules:**
- Single centered flex column. No zone splits.
- Content vertically centered with `justify-content: center`.
- Padding: 60pt top/bottom, 80pt sides.

**Content density:**
- Max: 1 title, 1 subtitle, 1 metadata line.
- Title: 32–40pt. Subtitle: 16–20pt. Metadata: 10–12pt.
- Title max 60 characters. Subtitle max 100 characters.

---

## 2. Agenda

Numbered section list. Supports vertical single-column or multi-column grid layout.

**Typical use case:** Table of contents or meeting agenda overview.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 36pt 48pt; box-sizing: border-box; }
.content { display: flex; flex: 1; gap: 32pt; }
.col { flex: 1; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 24pt; margin: 0 0 20pt 0;">Agenda</h1>
  <div class="content">
    <ol class="col" style="font-size: 14pt; margin: 0; padding-left: 20pt; line-height: 2.2;">
      <li>Topic One</li>
      <li>Topic Two</li>
      <li>Topic Three</li>
    </ol>
    <ol start="4" class="col" style="font-size: 14pt; margin: 0; padding-left: 20pt; line-height: 2.2;">
      <li>Topic Four</li>
      <li>Topic Five</li>
      <li>Topic Six</li>
    </ol>
  </div>
</div>
</body>
</html>
```

**Layout rules:**
- Title zone: top ~15%. Content zone: remaining ~85%.
- Two-column split at 50/50 when items > 5. Single column otherwise.
- Ordered list with `line-height: 2.2` for comfortable spacing.

**Content density:**
- Max 10–12 agenda items total.
- Items: 14–16pt. Title: 22–26pt.
- Each item max 50 characters.

---

## 3. Section Divider

Bold visual break between major sections. Large title with optional brief description.

**Typical use case:** Separating chapters or topic areas within a deck.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         justify-content: center; padding: 48pt 80pt; box-sizing: border-box; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 40pt; margin: 0 0 16pt 0;">Section Title</h1>
  <p style="font-size: 16pt; margin: 0; max-width: 480pt;">Brief description of this section goes here.</p>
</div>
</body>
</html>
```

**Layout rules:**
- Single column, vertically centered.
- Generous left padding (80pt) for asymmetric emphasis.
- Description capped at 480pt width.

**Content density:**
- Max: 1 title, 1 description line.
- Title: 36–44pt. Description: 14–18pt.
- Title max 40 characters. Description max 120 characters.

---

## 4. Content-Text

Standard single-column content slide with title and body text. Supports paragraphs and bullet lists.

**Typical use case:** General information delivery, explanations, key points.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 32pt 48pt; box-sizing: border-box; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 22pt; margin: 0 0 16pt 0;">Title Here</h1>
  <ul style="font-size: 14pt; margin: 0; padding-left: 20pt; line-height: 1.9;">
    <li>First key point with supporting detail</li>
    <li>Second key point with supporting detail</li>
    <li>Third key point with supporting detail</li>
    <li>Fourth key point with supporting detail</li>
  </ul>
</div>
</body>
</html>
```

**Layout rules:**
- Title zone: top ~12%. Body zone: remaining ~88%.
- Single column. Bullet list is default; swap to `<p>` for prose.
- Left padding 48pt, line-height 1.9 for readability.

**Content density:**
- Max 6 bullet points or 3 short paragraphs.
- Title: 20–24pt. Body: 13–15pt.
- Each bullet max 90 characters. Total body max ~540 characters.

---

## 5. Content-TwoCol

Two-column content layout with a shared title bar. Supports 50/50 and 40/60 splits.

**Typical use case:** Side-by-side text, text+image, pros/cons, feature pairs.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 32pt 48pt; box-sizing: border-box; }
.cols { display: flex; flex: 1; gap: 32pt; }
.col-left { flex: 1; }
.col-right { flex: 1; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 22pt; margin: 0 0 16pt 0;">Title Here</h1>
  <div class="cols">
    <div class="col-left">
      <h2 style="font-size: 16pt; margin: 0 0 8pt 0;">Left Heading</h2>
      <p style="font-size: 13pt; margin: 0; line-height: 1.7;">Left column content goes here.</p>
    </div>
    <div class="col-right">
      <h2 style="font-size: 16pt; margin: 0 0 8pt 0;">Right Heading</h2>
      <p style="font-size: 13pt; margin: 0; line-height: 1.7;">Right column content goes here.</p>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:**
- Title zone: top ~12%. Two-column body: remaining 88%.
- Default 50/50 split. For 40/60, set `col-left { flex: 2; }` and `col-right { flex: 3; }`.
- Gap between columns: 24–36pt.

**Content density:**
- Max 4 bullets or 2 paragraphs per column.
- Title: 20–24pt. Column headings: 14–16pt. Body: 12–14pt.
- Each column max 300 characters.

---

## 6. Data-Chart

Chart-dominant slide with title, large visualization area, and optional interpretation text.

**Typical use case:** Presenting data, graphs, charts with brief commentary.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 32pt 48pt; box-sizing: border-box; }
.chart-area { flex: 1; display: flex; align-items: center; justify-content: center; }
.chart-placeholder { border: 1pt solid #cccccc; width: 100%; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 22pt; margin: 0 0 12pt 0;">Chart Title</h1>
  <div class="chart-area">
    <img class="chart-placeholder" src="chart.png" style="max-height: 220pt;" />
  </div>
  <p style="font-size: 11pt; margin: 8pt 0 0 0;">Key insight or interpretation text goes here.</p>
</div>
</body>
</html>
```

**Layout rules:**
- Title zone: top ~10%. Chart zone: ~65% height. Interpretation: bottom ~12%.
- Chart area centered with `align-items: center`.
- Chart rendered as pre-rendered PNG (no SVG or CSS graphics).

**Content density:**
- Max 1 chart image, 1 interpretation line.
- Title: 20–24pt. Interpretation: 10–12pt.
- Interpretation max 150 characters. Chart max height 220pt.

---

## 7. Quote

Large quotation with attribution. Centered or left-offset for visual emphasis.

**Typical use case:** Highlighting a testimonial, mission statement, or keynote quote.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Georgia, serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         justify-content: center; padding: 60pt 80pt; box-sizing: border-box; }
</style></head>
<body>
<div class="slide">
  <p style="font-size: 24pt; font-style: italic; margin: 0 0 24pt 0; line-height: 1.5;">"Quotation text goes here with impactful wording that resonates."</p>
  <p style="font-size: 12pt; font-family: Arial, sans-serif; margin: 0;">— Author Name, Title</p>
</div>
</body>
</html>
```

**Layout rules:**
- Vertically centered single column. Uses serif font (Georgia) for quote.
- Padding 80pt sides creates a narrower reading column (~560pt).
- Attribution uses sans-serif for contrast.

**Content density:**
- Max 1 quote, 1 attribution line.
- Quote: 22–28pt. Attribution: 11–13pt.
- Quote max 180 characters.

---

## 8. Timeline

Sequential events or milestones displayed horizontally or vertically.

**Typical use case:** Project roadmap, company history, process evolution.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 32pt 48pt; box-sizing: border-box; }
.timeline { display: flex; flex: 1; gap: 16pt; align-items: flex-start; padding-top: 16pt; }
.event { flex: 1; text-align: center; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 22pt; margin: 0 0 8pt 0;">Timeline Title</h1>
  <div class="timeline">
    <div class="event">
      <h3 style="font-size: 13pt; margin: 0 0 6pt 0;">Q1 2025</h3>
      <p style="font-size: 11pt; margin: 0;">Milestone one</p>
    </div>
    <div class="event">
      <h3 style="font-size: 13pt; margin: 0 0 6pt 0;">Q2 2025</h3>
      <p style="font-size: 11pt; margin: 0;">Milestone two</p>
    </div>
    <div class="event">
      <h3 style="font-size: 13pt; margin: 0 0 6pt 0;">Q3 2025</h3>
      <p style="font-size: 11pt; margin: 0;">Milestone three</p>
    </div>
    <div class="event">
      <h3 style="font-size: 13pt; margin: 0 0 6pt 0;">Q4 2025</h3>
      <p style="font-size: 11pt; margin: 0;">Milestone four</p>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:**
- Title zone: top ~12%. Timeline: remaining space as horizontal flex row.
- Each event column is equal width (`flex: 1`).
- For vertical variant, change timeline to `flex-direction: column` with date labels.

**Content density:**
- Max 6 events (horizontal) or 8 events (vertical).
- Date label: 12–14pt bold. Description: 10–12pt.
- Each event description max 40 characters.

---

## 9. Comparison

Side-by-side A vs B comparison with shared criteria rows. Two equal columns.

**Typical use case:** Comparing products, strategies, options, before/after.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 32pt 48pt; box-sizing: border-box; }
.header-row { display: flex; margin-bottom: 12pt; }
.header-row div { flex: 1; }
.rows { display: flex; flex-direction: column; gap: 8pt; flex: 1; }
.row { display: flex; gap: 24pt; }
.row div { flex: 1; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 22pt; margin: 0 0 16pt 0;">Comparison Title</h1>
  <div class="header-row">
    <div><h2 style="font-size: 16pt; margin: 0;">Option A</h2></div>
    <div><h2 style="font-size: 16pt; margin: 0;">Option B</h2></div>
  </div>
  <div class="rows">
    <div class="row">
      <div><p style="font-size: 12pt; margin: 0;">Criteria 1 value for A</p></div>
      <div><p style="font-size: 12pt; margin: 0;">Criteria 1 value for B</p></div>
    </div>
    <div class="row">
      <div><p style="font-size: 12pt; margin: 0;">Criteria 2 value for A</p></div>
      <div><p style="font-size: 12pt; margin: 0;">Criteria 2 value for B</p></div>
    </div>
    <div class="row">
      <div><p style="font-size: 12pt; margin: 0;">Criteria 3 value for A</p></div>
      <div><p style="font-size: 12pt; margin: 0;">Criteria 3 value for B</p></div>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:**
- Title: top ~10%. Header row with column labels. Criteria rows share 50/50 split.
- Each row is a flex container with two equal children.
- Gap between columns: 24pt. Gap between rows: 8pt.

**Content density:**
- Max 6 criteria rows.
- Title: 20–24pt. Column headers: 14–16pt. Cell text: 11–13pt.
- Each cell max 60 characters.

---

## 10. Closing

Summary takeaway with call to action and contact information.

**Typical use case:** Final slide of a presentation.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         justify-content: center; align-items: center; padding: 48pt 80pt; box-sizing: border-box; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 28pt; text-align: center; margin: 0 0 16pt 0;">Key Takeaway</h1>
  <p style="font-size: 14pt; text-align: center; margin: 0 0 32pt 0;">Summary of the main message or call to action.</p>
  <p style="font-size: 11pt; text-align: center; margin: 0;">contact@example.com · example.com</p>
</div>
</body>
</html>
```

**Layout rules:**
- Vertically and horizontally centered. Single column.
- Three-tier structure: takeaway → CTA → contact.
- Padding 80pt sides for narrower, focused content width.

**Content density:**
- Max 1 takeaway, 1 CTA line, 1 contact line.
- Takeaway: 24–30pt. CTA: 13–16pt. Contact: 10–12pt.
- Takeaway max 60 characters. CTA max 120 characters.

---

## 11. Composite-Diagram

Complex nested layout for architecture diagrams, hierarchy charts, and agent maps. Uses nested flex containers up to 3 levels deep.

**Typical use case:** System architecture, org charts, agent topology, data flow diagrams.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 28pt 40pt; box-sizing: border-box; }
.diagram { flex: 1; display: flex; flex-direction: column; gap: 10pt; }
.layer { display: flex; gap: 10pt; }
.layer > div { flex: 1; border: 1pt solid #999999; padding: 8pt; }
.nested { display: flex; flex-direction: column; gap: 6pt; }
.nested > div { border: 1pt solid #cccccc; padding: 4pt 8pt; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 20pt; margin: 0 0 12pt 0;">Diagram Title</h1>
  <div class="diagram">
    <div class="layer">
      <div><p style="font-size: 11pt; margin: 0; text-align: center;">Top Layer A</p></div>
      <div><p style="font-size: 11pt; margin: 0; text-align: center;">Top Layer B</p></div>
    </div>
    <div class="layer">
      <div>
        <p style="font-size: 11pt; margin: 0 0 4pt 0; text-align: center;">Middle Layer</p>
        <div class="nested">
          <div><p style="font-size: 10pt; margin: 0;">Child Node 1</p></div>
          <div><p style="font-size: 10pt; margin: 0;">Child Node 2</p></div>
          <div><p style="font-size: 10pt; margin: 0;">Child Node 3</p></div>
        </div>
      </div>
      <div><p style="font-size: 11pt; margin: 0; text-align: center;">Middle Layer B</p></div>
    </div>
    <div class="layer">
      <div><p style="font-size: 11pt; margin: 0; text-align: center;">Bottom Layer</p></div>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:**
- Title: top ~8%. Diagram area fills remaining space.
- Up to 3 nesting levels: layer → box → nested children.
- Each layer is a horizontal flex row. Boxes within share equal width.
- Borders (1pt solid) define node boundaries. No CSS gradients.

**Content density:**
- Max 12–15 node boxes total across all layers.
- Node labels: 10–12pt. Title: 18–22pt.
- Each node label max 30 characters.

---

## 12. Pipeline-Flow

Sequential process visualization with labeled stages arranged in a horizontal flow.

**Typical use case:** CI/CD pipeline, workflow steps, customer journey, data processing stages.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 32pt 48pt; box-sizing: border-box; }
.pipeline { flex: 1; display: flex; align-items: center; gap: 8pt; }
.stage { flex: 1; border: 1pt solid #999999; padding: 12pt 8pt; text-align: center; }
.connector { width: 16pt; display: flex; align-items: center; justify-content: center; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 22pt; margin: 0 0 16pt 0;">Pipeline Title</h1>
  <div class="pipeline">
    <div class="stage">
      <h3 style="font-size: 12pt; margin: 0 0 4pt 0;">Stage 1</h3>
      <p style="font-size: 10pt; margin: 0;">Input</p>
    </div>
    <div class="connector"><p style="font-size: 16pt; margin: 0;">→</p></div>
    <div class="stage">
      <h3 style="font-size: 12pt; margin: 0 0 4pt 0;">Stage 2</h3>
      <p style="font-size: 10pt; margin: 0;">Process</p>
    </div>
    <div class="connector"><p style="font-size: 16pt; margin: 0;">→</p></div>
    <div class="stage">
      <h3 style="font-size: 12pt; margin: 0 0 4pt 0;">Stage 3</h3>
      <p style="font-size: 10pt; margin: 0;">Transform</p>
    </div>
    <div class="connector"><p style="font-size: 16pt; margin: 0;">→</p></div>
    <div class="stage">
      <h3 style="font-size: 12pt; margin: 0 0 4pt 0;">Stage 4</h3>
      <p style="font-size: 10pt; margin: 0;">Output</p>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:**
- Title: top ~12%. Pipeline row: vertically centered in remaining space.
- Stages share equal width (`flex: 1`). Connectors are fixed-width (16–20pt).
- Arrow connectors use text character `→` inside `<p>` tags.
- For multi-row pipelines, wrap pipeline divs in a column flex container.

**Content density:**
- Max 6 stages per row. Max 2 rows.
- Stage name: 11–13pt. Stage description: 9–11pt.
- Stage name max 20 characters. Description max 30 characters.

---

## 13. Composite Sub-Patterns

### 13a. Nested-Box Architecture (3-Level Deep)

Three nesting levels for representing hierarchical systems: outer boundary → subsystem → component.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 28pt 36pt; box-sizing: border-box; }
.arch { flex: 1; border: 2pt solid #333333; padding: 10pt; display: flex; gap: 10pt; }
.subsystem { flex: 1; border: 1pt solid #666666; padding: 8pt; display: flex; flex-direction: column; gap: 6pt; }
.component { border: 1pt solid #aaaaaa; padding: 4pt 6pt; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 20pt; margin: 0 0 10pt 0;">System Architecture</h1>
  <div class="arch">
    <div class="subsystem">
      <p style="font-size: 11pt; margin: 0 0 6pt 0;">Subsystem A</p>
      <div class="component"><p style="font-size: 10pt; margin: 0;">Component A1</p></div>
      <div class="component"><p style="font-size: 10pt; margin: 0;">Component A2</p></div>
    </div>
    <div class="subsystem">
      <p style="font-size: 11pt; margin: 0 0 6pt 0;">Subsystem B</p>
      <div class="component"><p style="font-size: 10pt; margin: 0;">Component B1</p></div>
      <div class="component"><p style="font-size: 10pt; margin: 0;">Component B2</p></div>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:** Outer box (2pt border) → subsystems (1pt border) → components (1pt lighter border). Each level reduces font size by 1pt.

**Content density:** Max 3 subsystems, 4 components each. Labels max 25 characters.

---

### 13b. Agent/Service Matrix (Grid)

Rectangular grid where rows represent agents and columns represent service interfaces or capabilities.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 28pt 36pt; box-sizing: border-box; }
.grid { display: flex; flex-direction: column; gap: 4pt; flex: 1; }
.grid-header { display: flex; gap: 4pt; }
.grid-header div { flex: 1; }
.grid-row { display: flex; gap: 4pt; }
.grid-row div { flex: 1; border: 1pt solid #cccccc; padding: 6pt; }
.label-col { flex: 0 0 100pt !important; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 20pt; margin: 0 0 10pt 0;">Agent Matrix</h1>
  <div class="grid">
    <div class="grid-header">
      <div class="label-col"></div>
      <div><p style="font-size: 10pt; margin: 0; text-align: center;">Service 1</p></div>
      <div><p style="font-size: 10pt; margin: 0; text-align: center;">Service 2</p></div>
      <div><p style="font-size: 10pt; margin: 0; text-align: center;">Service 3</p></div>
    </div>
    <div class="grid-row">
      <div class="label-col"><p style="font-size: 10pt; margin: 0;">Agent A</p></div>
      <div><p style="font-size: 9pt; margin: 0; text-align: center;">Yes</p></div>
      <div><p style="font-size: 9pt; margin: 0; text-align: center;">No</p></div>
      <div><p style="font-size: 9pt; margin: 0; text-align: center;">Yes</p></div>
    </div>
    <div class="grid-row">
      <div class="label-col"><p style="font-size: 10pt; margin: 0;">Agent B</p></div>
      <div><p style="font-size: 9pt; margin: 0; text-align: center;">No</p></div>
      <div><p style="font-size: 9pt; margin: 0; text-align: center;">Yes</p></div>
      <div><p style="font-size: 9pt; margin: 0; text-align: center;">Yes</p></div>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:** Fixed label column (100pt) + equal flex columns for services. Rows are equal height. Grid gap: 4pt.

**Content density:** Max 5 agents × 5 services. Cell values max 15 characters.

---

### 13c. Layered Stack (Horizontal Layers)

Stacked horizontal bands representing infrastructure or protocol layers. Each layer is a full-width row.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 28pt 36pt; box-sizing: border-box; }
.stack { flex: 1; display: flex; flex-direction: column; gap: 6pt; justify-content: center; }
.layer { border: 1pt solid #999999; padding: 12pt 16pt; display: flex; align-items: center; gap: 12pt; }
.layer-tag { flex: 0 0 80pt; }
.layer-content { flex: 1; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 20pt; margin: 0 0 10pt 0;">Stack Architecture</h1>
  <div class="stack">
    <div class="layer">
      <div class="layer-tag"><p style="font-size: 11pt; margin: 0;">Presentation</p></div>
      <div class="layer-content"><p style="font-size: 10pt; margin: 0;">UI components, templates, themes</p></div>
    </div>
    <div class="layer">
      <div class="layer-tag"><p style="font-size: 11pt; margin: 0;">Application</p></div>
      <div class="layer-content"><p style="font-size: 10pt; margin: 0;">Business logic, routing, middleware</p></div>
    </div>
    <div class="layer">
      <div class="layer-tag"><p style="font-size: 11pt; margin: 0;">Data</p></div>
      <div class="layer-content"><p style="font-size: 10pt; margin: 0;">Database, cache, storage layer</p></div>
    </div>
    <div class="layer">
      <div class="layer-tag"><p style="font-size: 11pt; margin: 0;">Infrastructure</p></div>
      <div class="layer-content"><p style="font-size: 10pt; margin: 0;">Servers, networking, orchestration</p></div>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:** Vertical flex column. Each layer is a full-width row with fixed label (80pt) + flexible description. Layers equally spaced.

**Content density:** Max 6 layers. Tag max 20 characters. Description max 60 characters per layer.

---

### 13d. Pipeline/Flow with Connectors (Sequential Stages)

Enhanced pipeline with labeled connectors and optional sub-steps per stage. Supports branching and merge patterns.

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 28pt 36pt; box-sizing: border-box; }
.flow { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 16pt; }
.flow-row { display: flex; align-items: center; justify-content: center; gap: 6pt; }
.stage { border: 1pt solid #999999; padding: 10pt 14pt; text-align: center; min-width: 80pt; }
.arrow { width: 24pt; text-align: center; }
.sub-row { display: flex; justify-content: center; gap: 10pt; }
.sub-stage { border: 1pt solid #cccccc; padding: 6pt 10pt; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 20pt; margin: 0 0 10pt 0;">Process Flow</h1>
  <div class="flow">
    <div class="flow-row">
      <div class="stage"><p style="font-size: 11pt; margin: 0;">Source</p></div>
      <div class="arrow"><p style="font-size: 14pt; margin: 0;">→</p></div>
      <div class="stage"><p style="font-size: 11pt; margin: 0;">Validate</p></div>
      <div class="arrow"><p style="font-size: 14pt; margin: 0;">→</p></div>
      <div class="stage"><p style="font-size: 11pt; margin: 0;">Transform</p></div>
      <div class="arrow"><p style="font-size: 14pt; margin: 0;">→</p></div>
      <div class="stage"><p style="font-size: 11pt; margin: 0;">Load</p></div>
    </div>
    <div class="sub-row">
      <div class="sub-stage"><p style="font-size: 9pt; margin: 0;">Parse</p></div>
      <div class="sub-stage"><p style="font-size: 9pt; margin: 0;">Schema</p></div>
      <div class="sub-stage"><p style="font-size: 9pt; margin: 0;">Enrich</p></div>
      <div class="sub-stage"><p style="font-size: 9pt; margin: 0;">Dedupe</p></div>
    </div>
  </div>
</div>
</body>
</html>
```

**Layout rules:** Main row for primary stages. Sub-row for detail steps aligned beneath. Arrow connectors 24pt wide. Stages use `min-width` instead of flex for fixed sizing.

**Content density:** Max 5 primary stages, 6 sub-steps. Stage labels max 15 characters. Sub-step labels max 12 characters.

---

## General Guidelines

### Zone Ratio Reference

| Page Type | Title Zone | Content Zone | Split |
|---|---|---|---|
| Cover | 100% | — | centered |
| Agenda | 15% | 85% | 50/50 cols |
| Section Divider | 100% | — | centered |
| Content-Text | 12% | 88% | single col |
| Content-TwoCol | 12% | 88% | 50/50 or 40/60 |
| Data-Chart | 10% | 78% + 12% | chart + interpretation |
| Quote | 100% | — | centered |
| Timeline | 12% | 88% | equal events |
| Comparison | 10% | 90% | 50/50 cols |
| Closing | 100% | — | centered |
| Composite-Diagram | 8% | 92% | multi-layer |
| Pipeline-Flow | 12% | 88% | equal stages |

### Font Size Scale

- **Slide title:** 20–24pt (general), 32–44pt (cover/divider)
- **Section heading:** 14–16pt
- **Body text:** 12–15pt
- **Caption/detail:** 9–11pt
- **Metadata:** 10–12pt

### Web-Safe Font Stack

- **Sans-serif:** Arial, Verdana, Tahoma, Trebuchet MS
- **Serif:** Georgia, Times New Roman
- **Monospace:** Courier New, Consolas

### html2pptx Constraints

- Body dimensions: `width: 720pt; height: 405pt` (10:7 aspect ratio).
- All visible text must be inside `<p>`, `<h1>`–`<h6>`, `<ul>`, or `<ol>` tags.
- No bare text nodes inside `<div>` elements.
- No CSS gradients — use pre-rendered PNG images instead.
- Use inline styles or `<style>` blocks only (no external stylesheets).
- Flexbox is supported; CSS Grid is not.
- Images referenced by relative or absolute path to PNG files.
