# Dark Neon - Design Specification

> Suitable for developer conferences, AI/ML showcases, tech demos, cybersecurity reviews, and any presentation requiring a futuristic, immersive dark-mode aesthetic.

---

## I. Template Overview

| Property           | Description                                                                      |
| ------------------ | -------------------------------------------------------------------------------- |
| **Template Name**  | Dark Neon (dark_neon)                                                            |
| **Use Cases**      | Developer conferences, AI/ML showcases, cybersecurity presentations, tech demos  |
| **Design Tone**    | Cyberpunk, futuristic, high-contrast, immersive                                  |
| **Theme Mode**     | Full dark theme — all pages use dark backgrounds with neon accent lighting       |

---

## II. Canvas Specification

| Property           | Value                                          |
| ------------------ | ---------------------------------------------- |
| **Format**         | Standard 16:9                                  |
| **Dimensions**     | 1280 × 720 px                                  |
| **viewBox**        | `0 0 1280 720`                                 |
| **Safe Margins**   | 80px (left/right), 60px (top/bottom)           |
| **Content Area**   | x: 80-1200, y: 120-640                         |
| **Title Area**     | y: 50-110                                      |
| **Grid Baseline**  | 40px                                           |

---

## III. Color Scheme

### Core Palette

| Role                 | Value       | Usage                                            |
| -------------------- | ----------- | ------------------------------------------------ |
| **Background**       | `#0A0A14`   | All page backgrounds — near-black with blue tint  |
| **Surface**          | `#12121F`   | Card/panel backgrounds, slightly lighter dark     |
| **Surface Raised**   | `#1A1A2E`   | Hover states, elevated containers                 |
| **Cyan Accent**      | `#00D2FF`   | Primary accent — titles, borders, key highlights  |
| **Purple Accent**    | `#7A2FCD`   | Secondary accent — gradients, decorative elements |
| **Neon Pink**        | `#FF0080`   | Warm accent — emphasis, badges, alerts            |
| **Neon Green**       | `#00FF88`   | Status/success accent — sparingly                 |

### Text Colors

| Role                 | Value       | Usage                                            |
| -------------------- | ----------- | ------------------------------------------------ |
| **Heading White**    | `#FFFFFF`   | All headings and titles                          |
| **Body Gray**        | `#B0B0C0`   | Body text, descriptions                          |
| **Muted Gray**       | `#606080`   | Captions, metadata, page numbers                 |
| **Cyan Text**        | `#00D2FF`   | Labels, section numbers, interactive elements    |

### Gradient Definitions

| Name                 | Colors                          | Usage                      |
| -------------------- | ------------------------------- | -------------------------- |
| **Glow Cyan-Purple** | `#00D2FF` → `#7A2FCD`           | Cover glow, accent bars    |
| **Glow Pink-Cyan**   | `#FF0080` → `#00D2FF`           | Ending page glow           |
| **Surface Fade**     | `#12121F` → `#0A0A14`           | Panel backgrounds          |

---

## IV. Typography System

### Font Stack

**Font Stack**: `Arial, Helvetica, sans-serif`

### Font Size Hierarchy

| Level    | Usage              | Size    | Weight  | Color      |
| -------- | ------------------ | ------- | ------- | ---------- |
| H1       | Cover main title   | 56-64px | Bold    | `#FFFFFF`  |
| H2       | Page title         | 32-36px | Bold    | `#FFFFFF`  |
| H3       | Section/card title | 22-26px | Bold    | `#FFFFFF`  |
| P        | Body content       | 18-20px | Regular | `#B0B0C0`  |
| Label    | Section numbers    | 14-16px | Bold    | `#00D2FF`  |
| Caption  | Metadata/footer    | 12-14px | Regular | `#606080`  |

---

## V. Page Structure

### General Layout

| Area         | Position/Height | Description                                    |
| ------------ | --------------- | ---------------------------------------------- |
| **Top**      | y=0-50          | Accent bars, corner decorations                |
| **Header**   | y=50-120        | Title area with underline accent               |
| **Content**  | y=130-640       | Main content area                              |
| **Footer**   | y=660-720       | Page number, source label, bottom accent       |

### Decorative Elements (recurring across pages)

1. **Grid Overlay**: Subtle horizontal + vertical lines at ~0.05 opacity across the background
2. **Corner L-Shapes**: L-shaped line decorations in cyan at top-left and bottom-right corners
3. **Particle Dots**: Small circles (2-4px) scattered at low opacity for depth
4. **Neon Accent Lines**: Thin horizontal/vertical lines in cyan or purple for visual separation
5. **Radial Glows**: Large radial gradients with low opacity for ambient lighting effects

---

## VI. Page Types

### 1. Cover Page (01_cover.svg)

- **Background**: `#0A0A14` with large radial cyan-purple glow in center area
- **Grid**: Thin horizontal and vertical lines at 0.07-0.10 opacity across the canvas
- **Particles**: Small circles scattered in the upper half
- **Title**: Large bold white text, left-aligned at ~x:100
- **Subtitle**: Cyan-tinted text below title
- **Accent Line**: Thin neon cyan horizontal line between title and subtitle
- **Footer**: Author and date at bottom with muted styling
- **Corners**: L-shaped decorative corner elements in cyan

### 2. Table of Contents (02_toc.svg)

- **Background**: `#0A0A14` with subtle purple glow at top
- **Top Accent Bar**: Thin gradient line (cyan → purple) spanning the width
- **Label**: "CONTENTS" in cyan with letter-spacing
- **Items**: 4-6 vertical list items, each with:
  - Small cyan dot or number circle
  - Item title text (placeholder `{{TOC_ITEM_N_TITLE}}`)
  - Thin horizontal divider line in muted gray
- **Footer**: Page number at bottom right

### 3. Chapter Page (02_chapter.svg)

- **Background**: `#0A0A14` with purple-tinted radial glow
- **Chapter Number**: Very large, semi-transparent text (opacity ~0.06) behind content
- **Title**: Bold white text, left-aligned
- **Subtitle**: Cyan text below title
- **Accent Line**: Short cyan horizontal line below title
- **Edge Accent**: Gradient strip (cyan → purple) on the left edge, full height
- **Decorative**: Small geometric shapes (diamonds, dots) scattered at low opacity

### 4. Content Page (03_content.svg)

- **Background**: `#0A0A14`
- **Top Accent Bar**: Thin gradient line at the very top
- **Left Accent**: Vertical cyan line at x=80
- **Title**: Bold white text at top
- **Content Area**: Large dashed-border container (cyan border, low opacity) indicating the safe zone
- **Content Placeholder**: Centered `{{CONTENT_AREA}}` text
- **Footer**: Source label left, page number right
- **Corner Decorations**: Small dot clusters in corners

### 5. Ending Page (04_ending.svg)

- **Background**: `#0A0A14` with large pink-cyan radial glow behind center text
- **Main Text**: Large "THANK YOU" text centered, bold white
- **Subtitle**: Smaller text below in cyan
- **Accent Line**: Thin line above the footer
- **Contact Info**: Centered below the main message
- **Geometric Decorations**: Hexagons, diamonds, and dots at low opacity
- **Bottom Accent**: Gradient bar at the very bottom

---

## VII. Layout Modes

### Content Area Dimensions

| Mode          | Dimensions               | Usage                        |
| ------------- | ------------------------ | ---------------------------- |
| Full-width    | x: 100-1180, y: 130-640 | Standard content             |
| Two-column    | L: 100-620, R: 660-1180  | Side-by-side comparison      |
| Centered      | x: 240-1040, y: 180-560  | Quotes, focused statements   |

### Safe Zone

All text must remain within x: 80-1200, y: 60-700 to avoid clipping.

---

## VIII. Spacing Specification

| Element              | Spacing          |
| -------------------- | ---------------- |
| **Title to body**    | 30px             |
| **Section gap**      | 40px             |
| **Bullet line height** | 36px          |
| **Card padding**     | 24px             |
| **Footer baseline**  | y=700            |
| **Left margin**      | 100px            |
| **Right margin**     | 80px from right  |

---

## IX. SVG Technical Constraints

### Mandatory Rules

1. viewBox: `0 0 1280 720`, width="1280" height="720"
2. **NO** `<rect rx="">` — use `<path>` with arc commands for rounded rectangles
3. **NO** `<style>` blocks or `class` attributes
4. **NO** `<g opacity="">` — set `fill-opacity` / `stroke-opacity` on individual elements
5. **NO** `rgba()` — use hex color + separate `fill-opacity` attribute
6. **NO** CSS gradients — use SVG `<defs>` `<linearGradient>` / `<radialGradient>`
7. **NO** `<mask>`, `<foreignObject>`, `<animate>`, `<script>`
8. **NO** multi-line `<tspan>` with `y`/`dy` — use separate `<text>` elements per line
9. Gradients defined in `<defs>` with `gradientUnits="userSpaceOnUse"` and hex stop colors
10. `stop-color` as attribute (not CSS `style="stop-color:..."`)
11. Background via `<rect>` elements only
12. All text uses `font-family="Arial"` — no other fonts

### Rounded Rectangle Pattern

```xml
<!-- Rounded rect: x=100, y=200, w=400, h=80, r=8 -->
<path d="M 108,200 L 492,200 A 8,8 0 0,1 500,208 L 500,272 A 8,8 0 0,1 492,280 L 108,280 A 8,8 0 0,1 100,272 L 100,208 A 8,8 0 0,1 108,200 Z"/>
```

---

## X. Placeholder Specification

| Placeholder               | Description                  |
| ------------------------- | ---------------------------- |
| `{{TITLE}}`               | Main title                   |
| `{{SUBTITLE}}`            | Subtitle                     |
| `{{AUTHOR}}`              | Speaker/Author               |
| `{{DATE}}`                | Date                         |
| `{{PAGE_TITLE}}`          | Page title                   |
| `{{CONTENT_AREA}}`        | Content area prompt text     |
| `{{CHAPTER_NUM}}`         | Chapter number (e.g. "01")   |
| `{{CHAPTER_TITLE}}`       | Chapter title                |
| `{{CHAPTER_DESC}}         | Chapter description          |
| `{{PAGE_NUM}}`            | Page number                  |
| `{{TOC_ITEM_1_TITLE}}`    | TOC item 1 title             |
| `{{TOC_ITEM_2_TITLE}}`    | TOC item 2 title             |
| `{{TOC_ITEM_3_TITLE}}`    | TOC item 3 title             |
| `{{TOC_ITEM_4_TITLE}}`    | TOC item 4 title             |
| `{{TOC_ITEM_5_TITLE}}`    | TOC item 5 title             |
| `{{THANK_YOU}}`           | Thank-you message            |
| `{{ENDING_SUBTITLE}}`     | Ending subtitle              |
| `{{CLOSING_MESSAGE}}`     | Closing message              |
| `{{CONTACT_INFO}}`        | Primary contact info         |
| `{{SOURCE}}`              | Source/confidentiality label |
