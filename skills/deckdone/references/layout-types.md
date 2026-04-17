# Layout Types — Page Type Definitions and Layout Rules

Reference for Step 4 (Page Type Assignment). For complete HTML templates, see `references/layout-templates.md`.

---

## Page Type Catalog

### 1. Cover
Full-bleed hero slide. Title + subtitle + optional date/author.
**Use:** First slide. **Layout:** Single centered flex column. **Zones:** Title (primary), subtitle, metadata.
**Content density:** Title 32–40pt max 60 chars. Subtitle 16–20pt max 100 chars. Metadata 10–12pt.

### 2. Agenda
Numbered section list. Single-column or two-column grid.
**Use:** Table of contents. **Layout:** Title top ~15%, content ~85%. Two-column at 50/50 when items > 5.
**Content density:** Max 10–12 items. Items 14–16pt max 50 chars each. Title 22–26pt.

### 3. Section Divider
Bold visual break between sections. Large title + optional description.
**Use:** Chapter separator. **Layout:** Vertically centered, generous left padding (80pt).
**Content density:** Title 36–44pt max 40 chars. Description 14–18pt max 120 chars.

### 4. Content-Text
Standard single-column content. Title + bullets or paragraphs.
**Use:** General information. **Layout:** Title top ~12%, body ~88%. Single column.
**Content density:** Max 6 bullets or 3 paragraphs. Title 20–24pt. Body 13–15pt max 90 chars/bullet.

### 5. Content-TwoCol
Two-column with shared title. 50/50 or 40/60 split.
**Use:** Side-by-side text, text+image, pros/cons. **Layout:** Title top ~12%, columns ~88%. Gap 24–36pt.
**Content density:** Max 4 bullets or 2 paragraphs per column. Title 20–24pt. Body 12–14pt max 300 chars/column.

### 6. Data-Chart
Chart-dominant slide with interpretation.
**Use:** Data presentation. **Layout:** Title top ~10%, chart ~65%, interpretation ~12%. Chart as pre-rendered PNG.
**Content density:** 1 chart + 1 interpretation line. Title 20–24pt. Interpretation 10–12pt max 150 chars.

### 7. Quote
Large quotation with attribution. Centered or left-offset.
**Use:** Testimonial, mission statement. **Layout:** Vertically centered single column. Serif font (Georgia).
**Content density:** 1 quote + 1 attribution. Quote 22–28pt max 180 chars. Attribution 11–13pt.

### 8. Timeline
Sequential events or milestones. Horizontal or vertical.
**Use:** Roadmap, history. **Layout:** Title top ~12%, timeline ~88%. Equal-width event columns.
**Content density:** Max 6 events (horizontal) or 8 (vertical). Date 12–14pt. Description 10–12pt max 40 chars.

### 9. Comparison
Side-by-side A vs B with shared criteria rows.
**Use:** Product compare, strategy options. **Layout:** Title top ~10%, header row, criteria rows 50/50. Gap 24pt.
**Content density:** Max 6 criteria rows. Cell text 11–13pt max 60 chars.

### 10. Closing
Summary takeaway + CTA + contact info.
**Use:** Final slide. **Layout:** Vertically and horizontally centered. Three-tier: takeaway → CTA → contact.
**Content density:** Takeaway 24–30pt max 60 chars. CTA 13–16pt max 120 chars. Contact 10–12pt.

### 11. Composite-Diagram
Complex nested layout. Up to 3 nesting levels.
**Use:** Architecture, org charts, agent topology. **Layout:** Title top ~8%, diagram ~92%. Layers as horizontal flex rows.
**Content density:** Max 12–15 node boxes. Node labels 10–12pt max 30 chars.

### 12. Pipeline-Flow
Sequential process with labeled stages.
**Use:** CI/CD, workflow, journey. **Layout:** Title top ~12%, pipeline ~88%. Equal-width stages with arrow connectors.
**Content density:** Max 6 stages/row, max 2 rows. Stage name 11–13pt max 20 chars. Description 9–11pt max 30 chars.

---

## Composite Sub-Patterns

- **13a. Nested-Box Architecture** — 3-level deep: outer (2pt border) → subsystem (1pt) → component (1pt lighter). Max 3 subsystems, 4 components each.
- **13b. Agent/Service Matrix** — Rectangular grid. Fixed label column (100pt) + equal flex columns. Max 5 agents × 5 services.
- **13c. Layered Stack** — Stacked horizontal bands. Fixed tag (80pt) + flexible description per layer. Max 6 layers.
- **13d. Pipeline/Flow with Connectors** — Main row + sub-row for detail steps. Arrow connectors 24pt wide. Max 5 primary stages, 6 sub-steps.

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
