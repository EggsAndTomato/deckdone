# Organic Warm - Design Specification

> Suitable for sustainability/ESG reports, healthcare, wellness, education, nonprofit, and community presentations. Style: warm, organic, calming, grounded, approachable.

---

## I. Template Overview

| Property         | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| **Template Name**| Organic Warm (organic_warm)                                      |
| **Use Cases**    | Sustainability reports, ESG disclosures, healthcare, wellness, education, nonprofit, community |
| **Design Tone**  | Warm, organic, calming, grounded, approachable                   |
| **Theme Mode**   | Light theme (warm cream background throughout all pages)         |

---

## II. Canvas Specification

| Property           | Value                         |
| ------------------ | ----------------------------- |
| **Format**         | Standard 16:9                 |
| **Dimensions**     | 1280 × 720 px                |
| **viewBox**        | `0 0 1280 720`               |
| **Safe Margins**   | 80px (left/right), 60px (top/bottom) |
| **Content Area**   | x: 80-1200, y: 130-650       |
| **Title Area**     | y: 40-100                    |
| **Grid Baseline**  | 40px                         |

---

## III. Color Scheme

### Primary Colors

| Role               | Value       | Notes                                    |
| ------------------ | ----------- | ---------------------------------------- |
| **Forest Green**   | `#2D6A4F`   | Primary accent, titles, key elements     |
| **Sage Green**     | `#7D8A6E`   | Organic shapes, secondary accents        |
| **Terracotta**     | `#C4734E`   | Warm accent, emphasis, chapter dividers  |
| **Warm Gold**      | `#D4A76A`   | Decorative dots, subtle highlights       |

### Neutral Colors

| Role               | Value       | Usage                          |
| ------------------ | ----------- | ------------------------------ |
| **Warm Cream**     | `#FFFAF2`   | Main page background           |
| **Deep Cream**     | `#FFF5E8`   | Gradient endpoint, warm zones  |
| **Dark Brown**     | `#3D2C22`   | Headings, primary text         |
| **Medium Brown**   | `#5C4A3E`   | Body text, subtitles           |
| **Light Brown**    | `#8B7355`   | Captions, annotations          |

---

## IV. Typography System

### Font Stack

**Headings**: `Georgia, serif`
**Body**: `Arial, sans-serif`

### Font Size Hierarchy

| Level    | Usage              | Size    | Weight  | Font    |
| -------- | ------------------ | ------- | ------- | ------- |
| H1       | Cover main title   | 56px    | Bold    | Georgia |
| H2       | Page/chapter title | 32-52px | Bold    | Georgia |
| H3       | Section title      | 24px    | Bold    | Georgia |
| P        | Body content       | 20-22px | Regular | Arial   |
| Caption  | Supplementary text | 13-16px | Regular | Arial   |

---

## V. Core Design Principles

### Organic Warm Style

1. **Organic Curves**: Flowing bezier paths (leaf silhouettes, water curves) create natural movement and warmth.
2. **Warm Color Palette**: Earth tones (cream, brown, green, terracotta) evoke nature and sustainability.
3. **Subtle Decorations**: Gold accent dots, soft gradients, and low-opacity organic shapes add depth without clutter.
4. **Paper-Like Quality**: Warm cream backgrounds with subtle gradient variations create a tactile, premium feel.

### Advanced Styling Features

1. **Gradient Overlays**: Warm cream-to-deep-cream gradients add subtle depth to backgrounds.
2. **Opacity Layering**: Organic shapes use varying opacity levels (0.04-0.18) for a layered, breathing effect.
3. **Natural Curves**: All decorative elements use cubic bezier curves (C commands) for organic flow.
4. **Gold Accents**: Small gold dots (r=2-5, opacity=0.2-0.6) scattered near organic shapes add warmth.

---

## VI. Page Structure

### General Layout

| Area         | Position/Height | Description                            |
| ------------ | --------------- | -------------------------------------- |
| **Top**      | y=0-100         | Title area, green accent bar           |
| **Content**  | y=130-650       | Main content area                      |
| **Footer**   | y=660-720       | Page number, organic bottom curves     |

### Decorative Design

- **Organic Shapes**: Core visual element — leaf/wave silhouettes in sage green and terracotta at low opacity.
- **Vertical Accent Bar**: Narrow green gradient bar (6px wide) for TOC and content pages.
- **Gold Dots**: Small circular accents (r=2-5) near organic decorations.
- **Terracotta Lines**: Horizontal accent lines for emphasis and chapter dividers.

---

## VII. Page Types

### 1. Cover Page (01_cover.svg)

- **Layout**: Asymmetric layout with organic shapes on right, text on left.
- **Background**: Warm cream with subtle diagonal gradient to deep cream.
- **Decoration**: Large sage green organic leaf shape flowing from bottom-right; smaller terracotta overlay; leaf vein detail lines; gold accent dots.
- **Title**: Left-aligned, large Georgia bold text in dark brown with subtitle in medium brown.
- **Accent**: Thin green horizontal line below title.
- **Footer**: Author and date in warm brown tones at bottom-left.

### 2. Table of Contents (02_toc.svg)

- **Layout**: Vertical list with left accent bar.
- **Accent**: Narrow vertical green gradient bar on the left edge.
- **Header**: "Contents" label in Georgia bold with gold underline.
- **Items**: 6 items with green circle bullets, title placeholders, thin warm-brown divider lines.
- **Decoration**: Subtle organic curve in bottom-right corner with gold dots.

### 3. Chapter Page (02_chapter.svg)

- **Background**: Warm cream gradient with large semi-transparent chapter number as watermark in sage green.
- **Center**: "CHAPTER XX" label in sage green, bold chapter title in Georgia, terracotta accent line.
- **Decoration**: Multi-layer organic curves along bottom edge in sage/terracotta/gold; gold accent dots below title.

### 4. Content Page (03_content.svg)

- **Top**: Full-width thin green accent bar (4px).
- **Left**: Narrow vertical green sidebar (5px × 50px) as title prefix.
- **Title**: Page title in Georgia bold with subtle underline.
- **Content**: Dashed rounded border container (path with arc commands) in warm brown at low opacity.
- **Footer**: Page number in sage green at bottom-right.
- **Decoration**: Small organic curve in bottom-right corner.

### 5. Ending Page (04_ending.svg)

- **Layout**: Centered layout with organic wave decoration.
- **Top**: Full-width thin green accent bar.
- **Center**: "Thank You" in large Georgia bold centered, with subtitle in sage green.
- **Decoration**: Flowing organic wave band across the middle (sage green + terracotta layers); gold accent dots; bottom organic curves.
- **Contact**: Closing message and contact information below the wave.

---

## VIII. Common Components

### Rounded Dashed Content Container

```xml
<path d="M 88,130 L 1192,130 A 8,8 0 0,1 1200,138 L 1200,642 A 8,8 0 0,1 1192,650 L 88,650 A 8,8 0 0,1 80,642 L 80,138 A 8,8 0 0,1 88,130 Z"
      fill="none" stroke="#5C4A3E" stroke-width="1.5" stroke-dasharray="8,6" stroke-opacity="0.18" />
```

### Vertical Accent Bar

```xml
<rect x="40" y="0" width="6" height="720" fill="url(#sidebarGrad)" />
```

### Organic Leaf Shape

```xml
<path d="M 680,720 C 720,650 800,570 900,500 C 1000,430 1100,390 1280,350 L 1280,720 Z"
      fill="#7D8A6E" fill-opacity="0.12" />
```

### Gold Accent Dots

```xml
<circle cx="1100" cy="440" r="4" fill="#D4A76A" fill-opacity="0.6" />
<circle cx="1150" cy="420" r="3" fill="#D4A76A" fill-opacity="0.4" />
```

---

## IX. SVG Technical Constraints

### Mandatory Rules

1. Canvas: `viewBox="0 0 1280 720"` with `width="1280" height="720"`.
2. Rounded rectangles: use `<path>` with arc commands (A), NOT `<rect rx="">`.
3. Opacity: use `fill-opacity` / `stroke-opacity` on individual elements, NOT `<g opacity="">`.
4. Colors: hex only (`#RRGGBB`), NOT `rgba()` or named colors.
5. Gradients: define in `<defs>` with `gradientUnits="userSpaceOnUse"` and explicit x1/y1/x2/y2.
6. Text: separate `<text>` elements per line, NOT multi-line `<tspan>` with y/dy.
7. Prohibited: `<mask>`, `<foreignObject>`, `<style>`, `class`, `<animate>`, `<script>`, `textPath`.
8. Font families: Georgia (headings), Arial (body) — standard web-safe fonts only.

---

## X. Placeholder Specification

| Placeholder                   | Description                |
| ----------------------------- | -------------------------- |
| `{{TITLE}}`                   | Main title (cover)         |
| `{{SUBTITLE}}`                | Subtitle (cover)           |
| `{{AUTHOR}}`                  | Speaker/Author             |
| `{{DATE}}`                    | Date                       |
| `{{PAGE_TITLE}}`              | Page title (content)       |
| `{{CONTENT_AREA}}`            | Content area prompt text   |
| `{{CHAPTER_NUM}}`             | Chapter number (01)        |
| `{{CHAPTER_TITLE}}`           | Chapter title              |
| `{{CHAPTER_DESC}}`            | Chapter description        |
| `{{PAGE_NUM}}`                | Page number                |
| `{{TOC_ITEM_1_TITLE}}`        | TOC item 1 title           |
| `{{TOC_ITEM_2_TITLE}}`        | TOC item 2 title           |
| `{{TOC_ITEM_3_TITLE}}`        | TOC item 3 title           |
| `{{TOC_ITEM_4_TITLE}}`        | TOC item 4 title           |
| `{{TOC_ITEM_5_TITLE}}`        | TOC item 5 title           |
| `{{TOC_ITEM_6_TITLE}}`        | TOC item 6 title           |
| `{{THANK_YOU}}`               | Thank-you message          |
| `{{ENDING_SUBTITLE}}`         | Ending subtitle            |
| `{{CLOSING_MESSAGE}}`         | Closing message            |
| `{{CONTACT_INFO}}`            | Primary contact info       |
