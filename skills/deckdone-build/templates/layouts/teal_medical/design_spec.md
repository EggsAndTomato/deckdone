# Teal Medical - Design Specification

> Suitable for medical presentations, biotech reports, clinical research, healthcare SaaS demos, and life science research. Style: calm-clinical, modern-professional, approachable precision, trust.

---

## I. Template Overview

| Property          | Description                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| **Template Name** | Teal Medical (teal_medical)                                                                     |
| **Use Cases**     | Medical presentations, biotech reports, clinical research, healthcare SaaS, life science        |
| **Design Tone**   | Calm-clinical, modern-professional, approachable precision, trust                               |
| **Theme Mode**    | Light theme (light gray-blue backgrounds with teal accents)                                     |

---

## II. Canvas Specification

| Property           | Value                                    |
| ------------------ | ---------------------------------------- |
| **Format**         | Standard 16:9                            |
| **Dimensions**     | 1280 × 720 px                           |
| **viewBox**        | `0 0 1280 720`                          |
| **Safe Margins**   | 60px (left/right), 50px (top/bottom)    |
| **Content Area**   | x: 120–1220, y: 160–620                 |
| **Title Area**     | y: 50–100                                |
| **Grid Baseline**  | 40px                                     |
| **Sidebar Width**  | 80px (left edge, gradient teal)          |

---

## III. Color Scheme

### Primary Colors

| Role                | Value      | Notes                                             |
| ------------------- | ---------- | ------------------------------------------------- |
| **Teal**            | `#0D7377`  | Brand identity, sidebar, accents, key elements    |
| **Light Teal**      | `#5EA8A7`  | Secondary accents, dividers, background elements  |
| **Coral**           | `#FF6B35`  | Warm highlight accent (sparingly — underlines, small bars) |

### Neutral Colors

| Role                 | Value      | Usage                                  |
| -------------------- | ---------- | -------------------------------------- |
| **Background**       | `#F5F9FA`  | Very light gray-blue, all page backgrounds |
| **Dark Slate**       | `#1A2B3C`  | Headings, titles                       |
| **Medium Gray**      | `#4A5568`  | Body text, subtitles                   |
| **Light Border**     | `#C8DDE0`  | Dashed borders, subtle dividers        |

### Decorative Colors

| Role                 | Value                    | Usage                                  |
| -------------------- | ------------------------ | -------------------------------------- |
| **Hex Pattern**      | `#0D7377` at 0.04–0.06 opacity | Background hexagonal texture      |
| **Molecular Nodes**  | `#0D7377` at 0.10–0.18 opacity | Molecular decoration circles      |
| **Molecular Bonds**  | `#0D7377` at 0.10–0.15 opacity | Molecular decoration lines         |

---

## IV. Typography System

### Font Stack

**Font**: `Arial` — all text elements (clean, modern, universal)

### Font Size Hierarchy

| Level    | Usage              | Size    | Weight  | Color     |
| -------- | ------------------ | ------- | ------- | --------- |
| H1       | Cover main title   | 52px    | Bold    | `#1A2B3C` |
| H2       | Page title         | 32–36px | Bold    | `#1A2B3C` |
| H2-alt   | Chapter title      | 56px    | Bold    | `#1A2B3C` |
| H3       | Section label      | 24px    | Bold    | `#0D7377` |
| P        | Body content       | 20px    | Regular | `#4A5568` |
| Caption  | Supplementary text | 14–16px | Regular | `#5EA8A7` or `#4A5568` |

---

## V. Core Design Principles

### Medical-Clinical Style

1. **Sidebar Consistency**: An 80px teal gradient sidebar on the left edge of cover, TOC, and content pages creates visual continuity and brand identity.
2. **Hexagonal Background Texture**: Scattered hexagonal outlines at 4–6% opacity evoke molecular/life science aesthetics without distracting from content.
3. **Molecular Decorations**: Small molecular node-and-bond patterns (circles connected by lines) in the lower-right corners add thematic personality.
4. **Coral Warmth**: A single coral accent line (3px) below titles adds human warmth to the otherwise clinical palette. Used once per page maximum.
5. **Generous Whitespace**: Medical design demands precision and breathing room. Content areas are well-spaced with clear hierarchy.

### Advanced Styling Features

1. **Gradient Sidebar**: Linear gradient from `#0D7377` (top) to `#5EA8A7` (bottom) adds depth.
2. **Dashed Content Frames**: Content areas use dashed rounded borders (`stroke-dasharray="10,6"`) in light teal for a clean, structured feel.
3. **Chapter Watermark**: Chapter pages display a very large, semi-transparent chapter number as a background watermark.
4. **Rounded Paths**: All rounded rectangles use `<path>` with arc commands (no `<rect rx="">`).

---

## VI. Page Types

### 1. Cover Page (01_cover.svg)

- **Layout**: Left sidebar + centered-right title area.
- **Background**: `#F5F9FA` with scattered hexagonal outlines at ~5% opacity on the right two-thirds.
- **Sidebar**: 80px teal gradient left edge.
- **Title**: Arial bold, dark slate, positioned at x=140.
- **Coral Accent**: 3px × 180px coral line below title.
- **Subtitle**: Medium gray, below accent line.
- **Footer**: Author and date bottom-right.
- **Decoration**: Molecular node-and-bond pattern in lower-right corner.

### 2. Table of Contents (02_toc.svg)

- **Layout**: Left sidebar + vertical item list.
- **Header**: "Contents" in teal bold with thin teal underline.
- **Items**: 6 entries with teal circle numbers (white text), title placeholders, and teal divider lines.
- **Decoration**: Hexagonal background pattern, page number bottom-right.

### 3. Chapter Page (02_chapter.svg)

- **Background**: `#F5F9FA`.
- **Top Bar**: 3px teal bar across full width.
- **Right Strip**: 6px × 720px vertical teal strip on right edge.
- **Watermark**: Very large chapter number (~280px) in light teal at ~5% opacity.
- **Title**: Arial bold, dark slate, centered.
- **Coral Accent**: 3px × 200px line below title.
- **Description**: Medium gray subtitle below accent.

### 4. Content Page (03_content.svg)

- **Top**: 3px teal bar across full width.
- **Sidebar**: 80px teal gradient left edge.
- **Title**: Arial bold at x=120.
- **Content Area**: Dashed rounded border in light teal (`stroke-dasharray="10,6"`).
- **Footer**: Source text left, page number right.
- **Decoration**: Molecular pattern in bottom-right corner.

### 5. Ending Page (04_ending.svg)

- **Background**: `#F5F9FA`.
- **Top Bar**: 3px teal bar across full width.
- **Center**: "Thank You" in Arial bold, dark slate.
- **Teal Underline**: Below the main text.
- **Contact**: Medium gray contact info below underline.
- **Decoration**: Molecular pattern on the right side.
- **Hexagonal Pattern**: Scattered at very low opacity.

---

## VII. Layout Modes

### Standard Layout Zones

| Zone     | Position          | Content                               |
| -------- | ----------------- | ------------------------------------- |
| Top Bar  | y=0, height=3px   | Full-width teal accent bar            |
| Sidebar  | x=0, width=80px   | Teal gradient (cover, TOC, content)   |
| Title    | y=50–100          | Page title, bold                      |
| Content  | y=160–620         | Main content with optional dashed frame |
| Footer   | y=670–710         | Source (left), page number (right)    |

---

## VIII. Spacing Specification

| Element              | Spacing                                  |
| -------------------- | ---------------------------------------- |
| Title to accent line | 20px below title baseline                |
| Accent line width    | 180–200px                                |
| Accent line height   | 3px                                      |
| TOC item spacing     | 75px vertical between items              |
| TOC divider          | Full-width, 1px, light teal at 30% opacity |
| Content area margin  | 40px from title, 50px from footer        |
| Safe content padding | 20px inside dashed frame                 |

---

## IX. SVG Technical Constraints

### Mandatory Rules

1. viewBox: `0 0 1280 720` — no width/height attributes on root `<svg>`
2. NO `<rect rx="">` — use `<path>` with arc commands for rounded rectangles
3. NO `<style>`, `class`, or CSS properties
4. NO `<g opacity="">` — set `fill-opacity` / `stroke-opacity` on individual elements
5. NO `rgba()` — use hex color + separate `fill-opacity` / `stroke-opacity`
6. NO CSS gradients — use SVG `<defs>` `<linearGradient>` / `<radialGradient>`
7. NO `<mask>`, `<foreignObject>`, `<animate>`, `<script>`
8. NO multi-line `<tspan>` with `y` or `dy` — use separate `<text>` elements
9. Gradients defined in `<defs>` at the top of the SVG
10. Use `gradientUnits="userSpaceOnUse"` with explicit coordinates

### Rounded Rectangle Path Template

For a rounded rect at (x, y) with width w, height h, radius r:

```
M (x+r),(y) L (x+w-r),(y) A r,r 0 0,1 (x+w),(y+r) L (x+w),(y+h-r) A r,r 0 0,1 (x+w-r),(y+h) L (x+r),(y+h) A r,r 0 0,1 (x),(y+h-r) L (x),(y+r) A r,r 0 0,1 (x+r),(y) Z
```

---

## X. Placeholder Specification

| Placeholder             | Description                        |
| ----------------------- | ---------------------------------- |
| `{{TITLE}}`             | Main title (cover)                 |
| `{{SUBTITLE}}`          | Subtitle (cover)                   |
| `{{AUTHOR}}`            | Speaker/Author                     |
| `{{DATE}}`              | Date                               |
| `{{PAGE_TITLE}}`        | Page title (content pages)         |
| `{{CONTENT_AREA}}`      | Content area prompt text           |
| `{{CHAPTER_NUM}}`       | Chapter number (e.g., 01)          |
| `{{CHAPTER_TITLE}}`     | Chapter title                      |
| `{{CHAPTER_DESC}}`      | Chapter description                |
| `{{PAGE_NUM}}`          | Page number                        |
| `{{TOC_ITEM_1_TITLE}}`  | TOC item 1 title                   |
| `{{TOC_ITEM_2_TITLE}}`  | TOC item 2 title                   |
| `{{TOC_ITEM_3_TITLE}}`  | TOC item 3 title                   |
| `{{TOC_ITEM_4_TITLE}}`  | TOC item 4 title                   |
| `{{TOC_ITEM_5_TITLE}}`  | TOC item 5 title                   |
| `{{TOC_ITEM_6_TITLE}}`  | TOC item 6 title                   |
| `{{THANK_YOU}}`         | Thank-you message                  |
| `{{ENDING_SUBTITLE}}`   | Ending subtitle                    |
| `{{CLOSING_MESSAGE}}`   | Closing message                    |
| `{{CONTACT_INFO}}`      | Primary contact info               |
| `{{SOURCE}}`            | Source/confidentiality label       |
