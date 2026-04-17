# Layout Templates — Decorated (with Icon & Illustration Slots)

Extended from `skills/deckdone/references/layout-templates.md`.
Each template adds icon and illustration slots marked with `<!-- DECKDONE-STYLE: ... -->` comments.
Replace placeholder `src` values (e.g. `ICON_THEME`, `ILLUSTRATION`) with actual image references at generation time.

For page type definitions and layout rules, see `references/layout-types.md`.
For density-dependent spacing parameters, see `references/density-presets.md`.

---

## 1. Cover

```html
<!DOCTYPE html>
<html>
<head><style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; }
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: row;
         justify-content: center; align-items: center; padding: 60pt 80pt; box-sizing: border-box; }
.main { flex: 0 0 75%; display: flex; flex-direction: column; align-items: center; }
.illustration-area { flex: 0 0 25%; display: flex; align-items: center; justify-content: center; }
</style></head>
<body>
<div class="slide">
  <div class="main">
    <!-- DECKDONE-STYLE: theme icon slot -->
    <img src="ICON_THEME" style="width: 48pt; height: 48pt; margin-bottom: 16pt;" />
    <h1 style="font-size: 36pt; text-align: center; margin: 0 0 12pt 0;">Title Here</h1>
    <p style="font-size: 18pt; text-align: center; margin: 0 0 24pt 0;">Subtitle goes here</p>
    <p style="font-size: 12pt; text-align: center; margin: 0;">Author · Date</p>
  </div>
  <div class="illustration-area">
    <!-- DECKDONE-STYLE: illustration slot -->
    <img src="ILLUSTRATION" style="max-width: 100%; max-height: 120pt;" />
  </div>
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
/* DENSITY: padding adjustable — see density-presets.md */
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 36pt 48pt; box-sizing: border-box; }
.content { display: flex; flex: 1; gap: 32pt; }
.col { flex: 1; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 24pt; margin: 0 0 20pt 0;">Agenda</h1>
  <div class="content">
    <!-- DENSITY: line-height adjustable — see density-presets.md -->
    <ol class="col" style="margin: 0; padding-left: 20pt; line-height: 2.2;">
      <!-- DECKDONE-STYLE: section icon slot -->
      <li><img src="ICON_SECTION" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Topic One</li>
      <li><img src="ICON_SECTION" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Topic Two</li>
      <li><img src="ICON_SECTION" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Topic Three</li>
    </ol>
    <ol start="4" class="col" style="margin: 0; padding-left: 20pt; line-height: 2.2;">
      <li><img src="ICON_SECTION" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Topic Four</li>
      <li><img src="ICON_SECTION" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Topic Five</li>
      <li><img src="ICON_SECTION" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Topic Six</li>
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
.title-row { display: flex; align-items: center; margin-bottom: 16pt; }
.illustration-area { margin-top: 16pt; display: flex; justify-content: center; }
</style></head>
<body>
<div class="slide">
  <div class="title-row">
    <!-- DECKDONE-STYLE: section icon slot -->
    <img src="ICON_SECTION" style="width: 40pt; height: 40pt; margin-right: 16pt;" />
    <h1 style="font-size: 40pt; margin: 0;">Section Title</h1>
  </div>
  <p style="font-size: 16pt; margin: 0; max-width: 480pt;">Brief description of this section goes here.</p>
  <div class="illustration-area">
    <!-- DECKDONE-STYLE: illustration slot -->
    <img src="ILLUSTRATION" style="max-width: 100%; max-height: 120pt;" />
  </div>
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
/* DENSITY: padding adjustable — see density-presets.md */
.slide { width: 720pt; height: 405pt; display: flex; flex-direction: column;
         padding: 32pt 48pt; box-sizing: border-box; }
</style></head>
<body>
<div class="slide">
  <h1 style="font-size: 22pt; margin: 0 0 16pt 0;">Title Here</h1>
  <!-- DENSITY: line-height adjustable — see density-presets.md -->
  <ul style="margin: 0; padding-left: 20pt; line-height: 1.9;">
    <!-- DECKDONE-STYLE: bullet icon slot -->
    <li><img src="ICON_BULLET" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />First key point with supporting detail</li>
    <li><img src="ICON_BULLET" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Second key point with supporting detail</li>
    <li><img src="ICON_BULLET" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Third key point with supporting detail</li>
    <li><img src="ICON_BULLET" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Fourth key point with supporting detail</li>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
      <!-- DECKDONE-STYLE: column icon slot -->
      <h2 style="margin: 0 0 8pt 0;"><img src="ICON_COL" style="width: 24pt; height: 24pt; vertical-align: middle; margin-right: 6pt;" />Left Heading</h2>
      <!-- DENSITY: line-height adjustable — see density-presets.md -->
      <p style="margin: 0; line-height: 1.7;">Left column content goes here.</p>
    </div>
    <div class="col-right">
      <!-- DECKDONE-STYLE: column icon slot -->
      <h2 style="margin: 0 0 8pt 0;"><img src="ICON_COL" style="width: 24pt; height: 24pt; vertical-align: middle; margin-right: 6pt;" />Right Heading</h2>
      <!-- DENSITY: line-height adjustable — see density-presets.md -->
      <p style="margin: 0; line-height: 1.7;">Right column content goes here.</p>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
  <!-- DECKDONE-STYLE: insight icon slot -->
  <p style="margin: 8pt 0 0 0;"><img src="info-circle" style="width: 16pt; height: 16pt; vertical-align: middle; margin-right: 4pt;" />Key insight or interpretation text goes here.</p>
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
  <p style="font-size: 60pt; color: [accent]; opacity: 0.3; margin: 0; line-height: 0.5;">"</p>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
      <!-- DECKDONE-STYLE: event icon slot -->
      <img src="ICON_EVENT" style="width: 24pt; height: 24pt; border-radius: 50%; margin: 0 auto 6pt; display: block;" />
      <h3 style="margin: 0 0 6pt 0;">Q1 2025</h3>
      <p style="margin: 0;">Milestone one</p>
    </div>
    <div class="event">
      <!-- DECKDONE-STYLE: event icon slot -->
      <img src="ICON_EVENT" style="width: 24pt; height: 24pt; border-radius: 50%; margin: 0 auto 6pt; display: block;" />
      <h3 style="margin: 0 0 6pt 0;">Q2 2025</h3>
      <p style="margin: 0;">Milestone two</p>
    </div>
    <div class="event">
      <!-- DECKDONE-STYLE: event icon slot -->
      <img src="ICON_EVENT" style="width: 24pt; height: 24pt; border-radius: 50%; margin: 0 auto 6pt; display: block;" />
      <h3 style="margin: 0 0 6pt 0;">Q3 2025</h3>
      <p style="margin: 0;">Milestone three</p>
    </div>
    <div class="event">
      <!-- DECKDONE-STYLE: event icon slot -->
      <img src="ICON_EVENT" style="width: 24pt; height: 24pt; border-radius: 50%; margin: 0 auto 6pt; display: block;" />
      <h3 style="margin: 0 0 6pt 0;">Q4 2025</h3>
      <p style="margin: 0;">Milestone four</p>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
    <!-- DECKDONE-STYLE: header icon slot -->
    <div><h2 style="margin: 0;"><img src="ICON_A" style="width: 24pt; height: 24pt; vertical-align: middle; margin-right: 6pt;" />Option A</h2></div>
    <!-- DECKDONE-STYLE: header icon slot -->
    <div><h2 style="margin: 0;"><img src="ICON_A" style="width: 24pt; height: 24pt; vertical-align: middle; margin-right: 6pt;" />Option B</h2></div>
  </div>
  <div class="rows">
    <div class="row">
      <div><p style="margin: 0;">Criteria 1 value for A</p></div>
      <div><p style="margin: 0;">Criteria 1 value for B</p></div>
    </div>
    <div class="row">
      <div><p style="margin: 0;">Criteria 2 value for A</p></div>
      <div><p style="margin: 0;">Criteria 2 value for B</p></div>
    </div>
    <div class="row">
      <div><p style="margin: 0;">Criteria 3 value for A</p></div>
      <div><p style="margin: 0;">Criteria 3 value for B</p></div>
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
  <!-- DECKDONE-STYLE: closing icon slot -->
  <img src="ICON_CLOSING" style="width: 48pt; height: 48pt; margin-bottom: 16pt;" />
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
/* DENSITY: padding adjustable — see density-presets.md */
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
      <div>
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0; text-align: center;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Top Layer A</p>
      </div>
      <div>
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0; text-align: center;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Top Layer B</p>
      </div>
    </div>
    <div class="layer">
      <div>
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0 0 4pt 0; text-align: center;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Middle Layer</p>
        <div class="nested">
          <div><p style="margin: 0;">Child Node 1</p></div>
          <div><p style="margin: 0;">Child Node 2</p></div>
          <div><p style="margin: 0;">Child Node 3</p></div>
        </div>
      </div>
      <div>
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0; text-align: center;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Middle Layer B</p>
      </div>
    </div>
    <div class="layer">
      <div>
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0; text-align: center;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Bottom Layer</p>
      </div>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
      <!-- DECKDONE-STYLE: stage icon slot -->
      <img src="ICON_STAGE" style="width: 32pt; height: 32pt; margin: 0 auto 4pt; display: block;" />
      <h3 style="margin: 0 0 4pt 0;">Stage 1</h3>
      <p style="margin: 0;">Input</p>
    </div>
    <!-- DECKDONE-STYLE: styled connector -->
    <div class="connector"><img src="chevron-right" style="width: 16pt; height: 16pt;" /></div>
    <div class="stage">
      <!-- DECKDONE-STYLE: stage icon slot -->
      <img src="ICON_STAGE" style="width: 32pt; height: 32pt; margin: 0 auto 4pt; display: block;" />
      <h3 style="margin: 0 0 4pt 0;">Stage 2</h3>
      <p style="margin: 0;">Process</p>
    </div>
    <!-- DECKDONE-STYLE: styled connector -->
    <div class="connector"><img src="chevron-right" style="width: 16pt; height: 16pt;" /></div>
    <div class="stage">
      <!-- DECKDONE-STYLE: stage icon slot -->
      <img src="ICON_STAGE" style="width: 32pt; height: 32pt; margin: 0 auto 4pt; display: block;" />
      <h3 style="margin: 0 0 4pt 0;">Stage 3</h3>
      <p style="margin: 0;">Transform</p>
    </div>
    <!-- DECKDONE-STYLE: styled connector -->
    <div class="connector"><img src="chevron-right" style="width: 16pt; height: 16pt;" /></div>
    <div class="stage">
      <!-- DECKDONE-STYLE: stage icon slot -->
      <img src="ICON_STAGE" style="width: 32pt; height: 32pt; margin: 0 auto 4pt; display: block;" />
      <h3 style="margin: 0 0 4pt 0;">Stage 4</h3>
      <p style="margin: 0;">Output</p>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
      <!-- DECKDONE-STYLE: subsystem icon slot -->
      <p style="margin: 0 0 6pt 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Subsystem A</p>
      <div class="component"><p style="margin: 0;">Component A1</p></div>
      <div class="component"><p style="margin: 0;">Component A2</p></div>
    </div>
    <div class="subsystem">
      <!-- DECKDONE-STYLE: subsystem icon slot -->
      <p style="margin: 0 0 6pt 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Subsystem B</p>
      <div class="component"><p style="margin: 0;">Component B1</p></div>
      <div class="component"><p style="margin: 0;">Component B2</p></div>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
      <!-- DECKDONE-STYLE: subsystem icon slot -->
      <div><p style="margin: 0; text-align: center;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Service 1</p></div>
      <!-- DECKDONE-STYLE: subsystem icon slot -->
      <div><p style="margin: 0; text-align: center;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Service 2</p></div>
      <!-- DECKDONE-STYLE: subsystem icon slot -->
      <div><p style="margin: 0; text-align: center;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Service 3</p></div>
    </div>
    <div class="grid-row">
      <!-- DECKDONE-STYLE: subsystem icon slot -->
      <div class="label-col"><p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Agent A</p></div>
      <div><p style="margin: 0; text-align: center;">Yes</p></div>
      <div><p style="margin: 0; text-align: center;">No</p></div>
      <div><p style="margin: 0; text-align: center;">Yes</p></div>
    </div>
    <div class="grid-row">
      <!-- DECKDONE-STYLE: subsystem icon slot -->
      <div class="label-col"><p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Agent B</p></div>
      <div><p style="margin: 0; text-align: center;">No</p></div>
      <div><p style="margin: 0; text-align: center;">Yes</p></div>
      <div><p style="margin: 0; text-align: center;">Yes</p></div>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
      <div class="layer-tag">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Presentation</p>
      </div>
      <div class="layer-content"><p style="margin: 0;">UI components, templates, themes</p></div>
    </div>
    <div class="layer">
      <div class="layer-tag">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Application</p>
      </div>
      <div class="layer-content"><p style="margin: 0;">Business logic, routing, middleware</p></div>
    </div>
    <div class="layer">
      <div class="layer-tag">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Data</p>
      </div>
      <div class="layer-content"><p style="margin: 0;">Database, cache, storage layer</p></div>
    </div>
    <div class="layer">
      <div class="layer-tag">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Infrastructure</p>
      </div>
      <div class="layer-content"><p style="margin: 0;">Servers, networking, orchestration</p></div>
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
/* DENSITY: padding adjustable — see density-presets.md */
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
      <div class="stage">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Source</p>
      </div>
      <!-- DECKDONE-STYLE: styled connector -->
      <div class="arrow"><img src="chevron-right" style="width: 16pt; height: 16pt;" /></div>
      <div class="stage">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Validate</p>
      </div>
      <!-- DECKDONE-STYLE: styled connector -->
      <div class="arrow"><img src="chevron-right" style="width: 16pt; height: 16pt;" /></div>
      <div class="stage">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Transform</p>
      </div>
      <!-- DECKDONE-STYLE: styled connector -->
      <div class="arrow"><img src="chevron-right" style="width: 16pt; height: 16pt;" /></div>
      <div class="stage">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Load</p>
      </div>
    </div>
    <div class="sub-row">
      <div class="sub-stage">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Parse</p>
      </div>
      <div class="sub-stage">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Schema</p>
      </div>
      <div class="sub-stage">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Enrich</p>
      </div>
      <div class="sub-stage">
        <!-- DECKDONE-STYLE: subsystem icon slot -->
        <p style="margin: 0;"><img src="ICON_SUBSYSTEM" style="width: 20pt; height: 20pt; vertical-align: middle; margin-right: 4pt;" />Dedupe</p>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```
