# HTML Wireframe Generation Guide

This guide defines the conventions for generating grayscale HTML wireframes used as presentation slide mockups. All wireframes follow a strict visual system to ensure consistency across batches.

---

## Table of Contents

1. [Grayscale Color Scheme Rules](#1-grayscale-color-scheme-rules)
2. [Zone Labeling Conventions](#2-zone-labeling-conventions)
3. [Visual Weight Annotation Syntax](#3-visual-weight-annotation-syntax)
4. [Composite-Diagram Zone Structure Notation](#4-composite-diagram-zone-structure-notation)
5. [Batch Display Strategy](#5-batch-display-strategy)
6. [Complete Wireframe HTML Template](#6-complete-wireframe-html-template)
7. [Browser Preview Integration](#7-browser-preview-integration)

---

## 1. Grayscale Color Scheme Rules

Every wireframe must use only the following hex values. No other colors are permitted.

| Role | Hex | Usage |
|---|---|---|
| Page background | `#FFFFFF` | Canvas behind all zones |
| Primary zones | `#4A4A4A` | Headers, hero banners, key callout areas |
| Secondary zones | `#8A8A8A` | Content columns, body text regions |
| Auxiliary zones | `#B0B0B0` | Labels, footnotes, decorative strips |
| Zone borders | `#CCCCCC` | `border` on every `.zone` div |
| Zone fill (light) | `#F0F0F0` | Auxiliary-weight zone backgrounds |
| Zone fill (medium) | `#E0E0E0` | Secondary-weight zone backgrounds |
| Zone fill (dark) | `#D0D0D0` | Primary-weight zone backgrounds |
| Text labels in zones | `#333333` | Body copy and readable text inside zones |
| Zone label text | `#666666` | Italic annotation labels identifying content type |

**Rules:**
- Never introduce brand colors, accent colors, or gradients into wireframes.
- If a zone needs to stand out, increase fill darkness rather than adding color.
- Header banners use `#4A4A4A` as background with white text, not as a fill.

---

## 2. Zone Labeling Conventions

Every zone must begin with a `<p class="zone-label">` element that declares its content type and a short description.

**Format:**
```html
<p class="zone-label">[TYPE]: [description]</p>
```

**Required CSS:**
```css
.zone-label {
  font-size: 10pt;
  color: #666666;
  margin: 0 0 4pt 0;
  font-style: italic;
}
```

**Recognized content types:**

| Type | Description |
|---|---|
| `title` | Slide headline or section title |
| `subtitle` | Sub-heading beneath a title |
| `body` | Paragraph or freeform text content |
| `bullet-list` | Bulleted or numbered list |
| `data-table` | Tabular data rows and columns |
| `chart-area` | Placeholder for a chart or graph |
| `image-area` | Placeholder for a photograph or illustration |
| `quote` | Pull-quote or testimonial block |
| `timeline-item` | Single entry in a timeline layout |
| `comparison-col` | One column in a comparison or versus layout |
| `icon-grid` | Grid of icons with short labels |

**Rules:**
- Every visible zone must carry a label, no exceptions.
- Labels appear inside the zone div as the first child element.
- The description should be a brief human-readable note, e.g., `"Left column key findings"`.

---

## 3. Visual Weight Annotation Syntax

Zones are assigned a weight to indicate their relative importance on the slide. Weight controls the fill shade and is also recorded as a `data-weight` attribute for programmatic access.

| Weight | Fill | `data-weight` | Use for |
|---|---|---|---|
| Primary | `#D0D0D0` (dark) | `"primary"` | Main content, key messages, hero areas |
| Secondary | `#E0E0E0` (medium) | `"secondary"` | Supporting content, details, sub-points |
| Auxiliary | `#F0F0F0` (light) | `"auxiliary"` | Labels, footnotes, decorative elements |

**CSS classes:**
```css
.zone-primary   { background: #D0D0D0; }
.zone-secondary { background: #E0E0E0; }
.zone-auxiliary { background: #F0F0F0; }
```

**HTML usage:**
```html
<div class="zone zone-primary" data-weight="primary">
  <p class="zone-label">BODY: Key takeaway paragraph</p>
</div>
```

**Rules:**
- Every zone must have exactly one weight.
- Weight classes are combined with the base `.zone` class.
- A single slide should contain at most one or two primary-weight zones to preserve visual hierarchy.

---

## 4. Composite-Diagram Zone Structure Notation

For complex slides with nested or interconnected regions, use the following conventions.

**Nesting:**
- Outer containers use solid `1pt solid #CCCCCC` borders.
- Inner sub-zones use dashed `1pt dashed #CCCCCC` borders.
- Each nesting level gets a lighter fill: outer → `#E0E0E0`, inner → `#F0F0F0`, deepest → `#F8F8F8`.
- Maximum 3 nesting levels to preserve readability.

**Connectors between zones:**
- Use a dedicated `<div>` with arrow content to indicate flow or relationship.
- Horizontal: `<div class="connector">→</div>`
- Vertical: `<div class="connector">↓</div>`
- Diagonal or cross: use `↘`, `↗`, etc.
- Connector divs are centered, `#999999` color, `12pt` font, `8pt` padding.

**Example:**
```html
<div style="display: flex; align-items: center;">
  <div class="zone zone-primary" data-weight="primary" style="flex: 1;">
    <p class="zone-label">CHART-AREA: Revenue bar chart</p>
  </div>
  <div class="connector">→</div>
  <div class="zone zone-secondary" data-weight="secondary" style="flex: 1; border-style: dashed;">
    <p class="zone-label">DATA-TABLE: Revenue numbers</p>
  </div>
</div>
```

---

## 5. Batch Display Strategy

Wireframes are generated and reviewed in batches, never one at a time.

**Batch rules:**
1. Group wireframes by logical section (5–8 pages per batch).
2. Generate all wireframes in a batch before presenting any to the user.
3. For each batch, create an index listing page numbers and content types.
4. The user confirms or requests changes to the entire batch before moving on.
5. Track confirmed batches in `deckdone-state.md` under a `wireframes-confirmed` key.

**Batch index format (in `deckdone-state.md`):**
```markdown
## Wireframe Batches

### Batch 1 — Status: confirmed
| Page | Layout Type | Title |
|------|-------------|-------|
| 1    | Title       | Cover |
| 2    | Content     | Agenda |
...
```

---

## 6. Complete Wireframe HTML Template

Below is a full working wireframe demonstrating every convention in this guide. Copy this as a starting point for any new wireframe.

```html
<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; width: 720pt; height: 405pt; font-family: Arial, sans-serif; background: #FFFFFF; }
.zone-label { font-size: 10pt; color: #666666; margin: 0 0 4pt 0; font-style: italic; }
.zone { border: 1pt solid #CCCCCC; padding: 8pt; margin: 4pt; }
.zone-primary { background: #D0D0D0; }
.zone-secondary { background: #E0E0E0; }
.zone-auxiliary { background: #F0F0F0; }
.wireframe-header { background: #4A4A4A; color: white; padding: 12pt; }
.connector { color: #999999; font-size: 12pt; padding: 0 8pt; text-align: center; }
</style>
</head>
<body>
<!-- Example: Content-TwoCol wireframe -->
<div style="display: flex; flex-direction: column; height: 405pt;">
  <div class="wireframe-header">
    <p class="zone-label" style="color: #CCCCCC;">TITLE: Slide banner</p>
    <h1 style="margin: 0; color: white;">Slide Title Here</h1>
  </div>
  <div style="display: flex; flex: 1; padding: 8pt;">
    <div class="zone zone-primary" data-weight="primary" style="flex: 1;">
      <p class="zone-label">BODY: Left column content</p>
      <p style="color: #333333;">Primary content placeholder for key message text.</p>
    </div>
    <div class="zone zone-secondary" data-weight="secondary" style="flex: 1;">
      <p class="zone-label">BODY: Right column content</p>
      <p style="color: #333333;">Supporting detail placeholder.</p>
    </div>
  </div>
  <div class="zone zone-auxiliary" data-weight="auxiliary">
    <p class="zone-label">FOOTER: Source attribution and notes</p>
  </div>
</div>
</body>
</html>
```

---

## 7. Browser Preview Integration

Use the `webapp-testing` skill to display wireframes to the user for review.

**Step-by-step:**

1. **Start a local HTTP server** serving the wireframes directory:
   ```bash
   python -m http.server 8080 --directory wireframes/
   ```

2. **Open each wireframe** in Playwright:
   ```
   Navigate to http://localhost:8080/slide-001.html
   ```

3. **Capture screenshots** for user review — one per wireframe file.

4. **Batch comparison** — display wireframes side-by-side by arranging multiple browser tabs or compositing screenshots into a single image.

5. **Teardown** — shut down the HTTP server after the batch review is complete.

**File naming convention:**
```
wireframes/
  batch-01/
    slide-001.html
    slide-002.html
    ...
  batch-02/
    slide-009.html
    ...
```
