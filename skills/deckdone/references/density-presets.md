# Density Presets — Content Capacity and Layout Spacing

Reference for Step 1 (density selection), Step 7 (content planning), and Steps 9–10 (HTML generation).

---

## Design Philosophy

| Level | ID | Chinese | Philosophy |
|-------|----|---------|------------|
| Presentation | `presentation` | 演讲辅助型 | Keywords + visuals. Audience watches the speaker, not the slides. |
| Detailed Presentation | `detailed-presentation` | 演讲详述型 | Key points with supporting arguments. Speaker adds context. |
| Reading | `reading` | 阅读型 | Self-contained document. Reader understands without a presenter. |

**Selection question:** "Will the audience read this deck on their own, or will you present it live?"

---

## Global Spacing Parameters

Control how much of the 720pt × 405pt slide is available for content.

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Slide padding | 48pt | 36pt | 24pt |
| Line-height (body) | 1.9 | 1.6 | 1.35 |
| Paragraph gap (between bullets/blocks) | 14pt | 8pt | 4pt |
| Min readable body font | 14pt | 12pt | 10pt |

---

## Font Size Decision Rule

The AI selects font sizes at generation time. The rule:

1. Calculate available content area: 720pt × 405pt minus padding from the table above.
2. Choose the largest font size that fits all zone content within the available area.
3. Do not exceed the max content capacity for this page type + density level (see tables below).
4. Do not go below the minimum readable body font for this density level.

No fixed font sizes are stored in this file. The AI has full context (slide dimensions, actual text length, spacing parameters) and can reason about optimal sizing.

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

Cover, Section Divider, Quote, Closing, Data-Chart have no capacity differences across density levels. Only global spacing parameters apply.
