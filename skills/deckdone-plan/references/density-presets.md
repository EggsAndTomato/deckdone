# Density Presets — Content Capacity

Reference for density selection and content planning.

---

## Design Philosophy

| Level | ID | Chinese | Philosophy |
|-------|----|---------|------------|
| Presentation | `presentation` | 演讲辅助型 | Keywords + visuals. Audience watches the speaker, not the slides. |
| Detailed Presentation | `detailed-presentation` | 演讲详述型 | Key points with supporting arguments. Speaker adds context. |
| Reading | `reading` | 阅读型 | Self-contained document. Reader understands without a presenter. |

**Selection question:** "Will the audience read this deck on their own, or will you present it live?"

---

## Visual Element Density

Each density level implies a target ratio of visually-driven pages (Data-Chart, Timeline, Pipeline-Flow, Composite-Diagram with structured diagrams) versus text-driven pages (Content-Text, Content-TwoCol, Quote). This guides page type assignment in Step 4 and SVG generation in deckdone-build Step 7.

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Target visual page ratio | ≥50% | ≥35% | ≥25% |
| Chart/diagram page types per 10 slides | 5-6 | 3-4 | 2-3 |
| Icon usage intensity | liberal (1-2 icons per content page) | moderate (icons for key concepts) | minimal (icons for navigation/structure only) |
| Data-Chart pages | prefer charts over bullet lists for data | mix of charts and text | charts when data is complex; tables acceptable |
| Shape/decoration intensity | bold accent shapes, gradient fills | subtle accent lines, light fills | minimal decoration, clean lines |

**How the AI uses this:**

1. **Step 3 (Outline):** When estimating pages, aim for the target visual page ratio. If the outline is text-heavy, suggest splitting dense text into Timeline, Comparison, or Data-Chart pages.
2. **Step 4 (Page Type Assignment):** Actively assign visual page types. For example, prefer Data-Chart over Content-Text when presenting metrics; prefer Timeline over bullet lists for sequential information; prefer Comparison over Content-TwoCol for side-by-side analysis.
3. **Step 5 (Wireframe):** Ensure chart zones include structured data (`<dl>` format). Every visual page type MUST have `data-chart-ref` or `data-*-structured` attributes.
4. **deckdone-build Step 7 (SVG Generation):** Apply the matching chart template. Never render chart/diagram/timeline data as plain text — always use graphical SVG elements.

---

## Content Capacity per Page Type

### Content-Text

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max bullets | 4 | 6 | 10 |
| Max chars/bullet | 40 | 90 | 200 |
| Sub-bullets | none | 1 level | 2 levels |

### Content-TwoCol

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max bullets/col | 3 | 4 | 6 |
| Max chars/col | 150 | 300 | 600 |

### Agenda

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max items | 6 | 8 | 12 |
| Max chars/item | 30 | 50 | 80 |
| Sub-descriptions | no | optional | yes |

### Timeline

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max events (horizontal) | 4 | 6 | 8 |
| Max chars/description | 20 | 40 | 80 |

### Comparison

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max criteria rows | 4 | 5 | 8 |
| Max chars/cell | 30 | 60 | 120 |

### Composite-Diagram

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max nodes | 8 | 12 | 15 |
| Max chars/node label | 20 | 30 | 50 |
| Node descriptions | no | brief | yes |

### Pipeline-Flow

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max stages/row | 4 | 5 | 6 |
| Max chars/stage desc | 15 | 30 | 60 |
| Sub-step rows | no | optional | yes |

### Low-Impact Types

Cover, Section Divider, Quote, Closing, Data-Chart have no capacity differences across density levels.
