# Layout Templates — Complete HTML Slide Templates

Reference for Step 6 (Wireframes), Step 9 (Test Generation), and Step 10 (Batch Generation).

For page type definitions and layout rules, see `references/layout-types.md`.

---

## 1. Cover

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

---

## 2. Agenda

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

---

## 3. Section Divider

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

---

## 4. Content-Text

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

---

## 5. Content-TwoCol

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

---

## 6. Data-Chart

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

---

## 7. Quote

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

---

## 8. Timeline

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

---

## 9. Comparison

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

---

## 10. Closing

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

---

## 11. Composite-Diagram

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

---

## 12. Pipeline-Flow

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

---

## 13a. Nested-Box Architecture

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

---

## 13b. Agent/Service Matrix

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

---

## 13c. Layered Stack

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

---

## 13d. Pipeline/Flow with Connectors

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
