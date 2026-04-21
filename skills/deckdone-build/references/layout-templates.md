# SVG Layout Templates

SVG templates for DeckDone slide generation. Each template uses `{{PLACEHOLDER}}` tokens replaced from content-plan.md and `{{STYLE_TOKEN}}` values replaced from style-guide.md.

## Token Reference

### Content Tokens

| Token | Source | Description |
|-------|--------|-------------|
| `{{TITLE}}` | content-plan.md Zone A | Page title |
| `{{SUBTITLE}}` | content-plan.md Zone B | Subtitle (Cover, Section Divider) |
| `{{DATE}}` | content-plan.md metadata | Date string |
| `{{AUTHOR}}` | content-plan.md metadata | Author name |
| `{{PAGE_NUM}}` | auto-generated | Slide page number |
| `{{SECTION_NUMBER}}` | content-plan.md | Section/chapter number (e.g. "01") |
| `{{DESCRIPTION}}` | content-plan.md Zone B | Section description |
| `{{ITEM_1}}` .. `{{ITEM_6}}` | content-plan.md Zone B | Agenda/list items |
| `{{COL_L_HEADING}}` | content-plan.md Zone B | Left column heading |
| `{{COL_R_HEADING}}` | content-plan.md Zone C | Right column heading |
| `{{COL_L_BODY}}` | content-plan.md Zone B | Left column body text |
| `{{COL_R_BODY}}` | content-plan.md Zone C | Right column body text |
| `{{CHART_SRC}}` | content-plan.md Zone B | Chart image path or base64 data URI |
| `{{INTERPRETATION}}` | content-plan.md Zone C | Chart interpretation text |
| `{{QUOTE_TEXT}}` | content-plan.md Zone A | Quotation text |
| `{{ATTRIBUTION}}` | content-plan.md Zone B | Quote attribution (e.g. "Author Name, Title") |
| `{{EVENT_N_DATE}}` | content-plan.md Zone B | Timeline event N date label |
| `{{EVENT_N_DESC}}` | content-plan.md Zone B | Timeline event N description |
| `{{OPTION_A}}` | content-plan.md Zone B | Comparison option A label |
| `{{OPTION_B}}` | content-plan.md Zone C | Comparison option B label |
| `{{CRITERIA_LABEL_N}}` | content-plan.md | Nth criteria row label |
| `{{CRITERIA_A_N}}` | content-plan.md | Nth criteria value for option A |
| `{{CRITERIA_B_N}}` | content-plan.md | Nth criteria value for option B |
| `{{TAKEAWAY}}` | content-plan.md Zone A | Key takeaway message |
| `{{CTA_TEXT}}` | content-plan.md Zone B | Call to action text |
| `{{CONTACT_INFO}}` | content-plan.md Zone C | Contact information string |
| `{{STAGE_N_NAME}}` | content-plan.md Zone B | Pipeline stage N name |
| `{{STAGE_N_DESC}}` | content-plan.md Zone B | Pipeline stage N description |
| `{{LAYER_N_LABEL}}` | content-plan.md | Diagram layer N label |
| `{{NODE_N_LABEL}}` | content-plan.md | Diagram node N label |

### Style Tokens

| Token | Source | Description |
|-------|--------|-------------|
| `{{BG_COLOR}}` | style-guide.md palette | Background fill (`#hex`) |
| `{{ACCENT_COLOR}}` | style-guide.md palette | Accent/highlight color (`#hex`) |
| `{{TEXT_PRIMARY}}` | style-guide.md palette | Primary text color (`#hex`) |
| `{{TEXT_SECONDARY}}` | style-guide.md palette | Secondary text color (`#hex`) |
| `{{TEXT_TERTIARY}}` | style-guide.md palette | Tertiary/muted text color (`#hex`) |
| `{{FONT_FAMILY}}` | style-guide.md typography | Primary font stack (sans-serif) |
| `{{FONT_SERIF}}` | style-guide.md typography | Serif font stack |
| `{{BORDER_COLOR}}` | style-guide.md palette | Border/separator color (`#hex`) |

## SVG Technical Constraints

See `references/svg-constraints.md` for the full constraint list. Key rules:

- **viewBox:** `0 0 1280 720`
- **All text** in `<text>` elements (separate elements per line, no multi-line tspan)
- **Rounded rects** as `<path>` with arc commands — never `<rect rx="">`
- **Icons** as `<use data-icon="...">` placeholders
- **No** CSS `<style>` blocks, no flexbox, no `<rect rx="">`, no `<g opacity="">`
- **Gradients** in `<defs>` with `gradientUnits="userSpaceOnUse"` and hex stop colors
- **Arrows** via `<marker>` elements in `<defs>` with `marker-end` references
- **Shadows** via `<filter>` in `<defs>` using `feGaussianBlur` + `feOffset`

---

## 1. Cover

Full-bleed background with gradient overlay. Left accent bar, decorative corner arcs, centered title/subtitle with accent underline, footer metadata.

**Zones:** Title (primary, centered) > Subtitle > Footer metadata.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="coverGrad" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="{{ACCENT_COLOR}}" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="{{BG_COLOR}}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#coverGrad)"/>

  <!-- Left accent bar -->
  <rect x="0" y="0" width="8" height="720" fill="{{ACCENT_COLOR}}"/>

  <!-- Decorative top-right corner arc -->
  <path d="M 1280,0 L 1100,0 A 180,180 0 0,1 1280,180 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.06"/>

  <!-- Decorative bottom-left corner arc -->
  <path d="M 0,720 L 0,580 A 140,140 0 0,0 140,720 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.04"/>

  <!-- Zone A: Title -->
  <text x="640" y="310" font-family="{{FONT_FAMILY}}" font-size="56" fill="{{TEXT_PRIMARY}}" text-anchor="middle" font-weight="bold">{{TITLE}}</text>

  <!-- Accent underline -->
  <line x1="540" y1="340" x2="740" y2="340" stroke="{{ACCENT_COLOR}}" stroke-width="3" stroke-linecap="round"/>

  <!-- Zone B: Subtitle -->
  <text x="640" y="400" font-family="{{FONT_FAMILY}}" font-size="26" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{SUBTITLE}}</text>

  <!-- Zone C: Footer metadata -->
  <text x="640" y="670" font-family="{{FONT_FAMILY}}" font-size="14" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{AUTHOR}} · {{DATE}}</text>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 2. Agenda

Title with icon, two-column numbered list. Each item has an accent-filled number circle. Subtle dashed vertical divider between columns.

**Zones:** Title (top 15%) > Content (85%, two columns 50/50).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="agendaHdrGrad" gradientUnits="userSpaceOnUse" x1="80" y1="40" x2="400" y2="40">
      <stop offset="0%" stop-color="{{ACCENT_COLOR}}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{{BG_COLOR}}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Title area subtle background -->
  <rect x="80" y="35" width="320" height="40" fill="url(#agendaHdrGrad)"/>

  <!-- Zone A: Title -->
  <use data-icon="tabler-outline/list" x="80" y="38" width="32" height="32" fill="{{ACCENT_COLOR}}"/>
  <text x="122" y="64" font-family="{{FONT_FAMILY}}" font-size="30" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>

  <!-- Title underline -->
  <line x1="80" y1="80" x2="350" y2="80" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Vertical column divider (dashed) -->
  <line x1="640" y1="110" x2="640" y2="640" stroke="{{BORDER_COLOR}}" stroke-width="1" stroke-dasharray="4,4"/>

  <!-- Left column: Items 1-3 -->
  <circle cx="112" cy="150" r="20" fill="{{ACCENT_COLOR}}" fill-opacity="0.12"/>
  <text x="112" y="157" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">1</text>
  <text x="146" y="157" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_PRIMARY}}">{{ITEM_1}}</text>

  <circle cx="112" cy="225" r="20" fill="{{ACCENT_COLOR}}" fill-opacity="0.12"/>
  <text x="112" y="232" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">2</text>
  <text x="146" y="232" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_PRIMARY}}">{{ITEM_2}}</text>

  <circle cx="112" cy="300" r="20" fill="{{ACCENT_COLOR}}" fill-opacity="0.12"/>
  <text x="112" y="307" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">3</text>
  <text x="146" y="307" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_PRIMARY}}">{{ITEM_3}}</text>

  <!-- Right column: Items 4-6 -->
  <circle cx="692" cy="150" r="20" fill="{{ACCENT_COLOR}}" fill-opacity="0.12"/>
  <text x="692" y="157" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">4</text>
  <text x="726" y="157" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_PRIMARY}}">{{ITEM_4}}</text>

  <circle cx="692" cy="225" r="20" fill="{{ACCENT_COLOR}}" fill-opacity="0.12"/>
  <text x="692" y="232" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">5</text>
  <text x="726" y="232" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_PRIMARY}}">{{ITEM_5}}</text>

  <circle cx="692" cy="300" r="20" fill="{{ACCENT_COLOR}}" fill-opacity="0.12"/>
  <text x="692" y="307" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">6</text>
  <text x="726" y="307" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_PRIMARY}}">{{ITEM_6}}</text>

  <!-- Bottom accent -->
  <rect x="80" y="660" width="120" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 3. Section Divider

Large semi-transparent chapter number as background element. Bold accent bar, title, and description vertically centered. Right-edge accent strip.

**Zones:** Section number (decorative) > Title (primary) > Description.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="sectionGrad" gradientUnits="userSpaceOnUse" x1="80" y1="300" x2="500" y2="500">
      <stop offset="0%" stop-color="{{ACCENT_COLOR}}" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="{{BG_COLOR}}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>
  <rect x="80" y="300" width="420" height="200" fill="url(#sectionGrad)"/>

  <!-- Right-edge accent strip -->
  <rect x="1220" y="0" width="8" height="720" fill="{{ACCENT_COLOR}}" fill-opacity="0.25"/>

  <!-- Decorative bottom line -->
  <rect x="80" y="660" width="1120" height="1" fill="{{BORDER_COLOR}}" fill-opacity="0.3"/>

  <!-- Zone A (decorative): Large section number -->
  <text x="100" y="430" font-family="{{FONT_FAMILY}}" font-size="200" fill="{{ACCENT_COLOR}}" fill-opacity="0.08" font-weight="bold">{{SECTION_NUMBER}}</text>

  <!-- Accent bar -->
  <rect x="80" y="355" width="200" height="5" fill="{{ACCENT_COLOR}}"/>

  <!-- Zone B: Title -->
  <text x="80" y="420" font-family="{{FONT_FAMILY}}" font-size="48" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>

  <!-- Zone C: Description -->
  <text x="80" y="475" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_SECONDARY}}">{{DESCRIPTION}}</text>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 4. Content-Text

Top accent bar, title with underline, body text as separate `<text>` elements with bullet dot decorations. Clean single-column layout.

**Zones:** Title (top 12%) > Body bullets (88%).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Top accent bar -->
  <rect x="80" y="42" width="1120" height="4" fill="{{ACCENT_COLOR}}"/>

  <!-- Zone A: Title -->
  <text x="80" y="95" font-family="{{FONT_FAMILY}}" font-size="30" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>

  <!-- Title underline -->
  <line x1="80" y1="110" x2="380" y2="110" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Zone B: Body bullets -->
  <circle cx="94" cy="158" r="4" fill="{{ACCENT_COLOR}}"/>
  <text x="112" y="163" font-family="{{FONT_FAMILY}}" font-size="19" fill="{{TEXT_SECONDARY}}">{{BODY_LINE_1}}</text>

  <circle cx="94" cy="208" r="4" fill="{{ACCENT_COLOR}}"/>
  <text x="112" y="213" font-family="{{FONT_FAMILY}}" font-size="19" fill="{{TEXT_SECONDARY}}">{{BODY_LINE_2}}</text>

  <circle cx="94" cy="258" r="4" fill="{{ACCENT_COLOR}}"/>
  <text x="112" y="263" font-family="{{FONT_FAMILY}}" font-size="19" fill="{{TEXT_SECONDARY}}">{{BODY_LINE_3}}</text>

  <circle cx="94" cy="308" r="4" fill="{{ACCENT_COLOR}}"/>
  <text x="112" y="313" font-family="{{FONT_FAMILY}}" font-size="19" fill="{{TEXT_SECONDARY}}">{{BODY_LINE_4}}</text>

  <circle cx="94" cy="358" r="4" fill="{{ACCENT_COLOR}}"/>
  <text x="112" y="363" font-family="{{FONT_FAMILY}}" font-size="19" fill="{{TEXT_SECONDARY}}">{{BODY_LINE_5}}</text>

  <!-- Right-side decoration -->
  <rect x="1240" y="42" width="4" height="200" fill="{{ACCENT_COLOR}}" fill-opacity="0.15"/>

  <!-- Bottom accent -->
  <rect x="80" y="660" width="80" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 5. Content-TwoCol

Title at top, vertical accent divider separating two independent columns. Each column has its own heading and body text lines. Dots anchor the divider endpoints.

**Zones:** Title (top 12%) > Left column (44%) | Divider | Right column (44%).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Top accent bar -->
  <rect x="80" y="42" width="1120" height="4" fill="{{ACCENT_COLOR}}"/>

  <!-- Zone A: Title -->
  <text x="80" y="90" font-family="{{FONT_FAMILY}}" font-size="30" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>

  <!-- Title underline -->
  <line x1="80" y1="105" x2="380" y2="105" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Vertical accent divider with endpoint dots -->
  <line x1="640" y1="130" x2="640" y2="650" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-opacity="0.25"/>
  <circle cx="640" cy="130" r="4" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>
  <circle cx="640" cy="650" r="4" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Zone B: Left column -->
  <text x="100" y="155" font-family="{{FONT_FAMILY}}" font-size="22" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{COL_L_HEADING}}</text>
  <line x1="100" y1="168" x2="340" y2="168" stroke="{{BORDER_COLOR}}" stroke-width="1"/>

  <text x="100" y="205" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{TEXT_SECONDARY}}">{{COL_L_LINE_1}}</text>
  <text x="100" y="240" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{TEXT_SECONDARY}}">{{COL_L_LINE_2}}</text>
  <text x="100" y="275" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{TEXT_SECONDARY}}">{{COL_L_LINE_3}}</text>
  <text x="100" y="310" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{TEXT_SECONDARY}}">{{COL_L_LINE_4}}</text>

  <!-- Zone C: Right column -->
  <text x="680" y="155" font-family="{{FONT_FAMILY}}" font-size="22" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{COL_R_HEADING}}</text>
  <line x1="680" y1="168" x2="920" y2="168" stroke="{{BORDER_COLOR}}" stroke-width="1"/>

  <text x="680" y="205" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{TEXT_SECONDARY}}">{{COL_R_LINE_1}}</text>
  <text x="680" y="240" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{TEXT_SECONDARY}}">{{COL_R_LINE_2}}</text>
  <text x="680" y="275" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{TEXT_SECONDARY}}">{{COL_R_LINE_3}}</text>
  <text x="680" y="310" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{TEXT_SECONDARY}}">{{COL_R_LINE_4}}</text>

  <!-- Bottom accent -->
  <rect x="80" y="660" width="80" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 6. Data-Chart

Title with chart icon, large chart area framed by a rounded rect with subtle drop shadow, interpretation text below with accent dot prefix.

**Zones:** Title (top 10%) > Chart area (65%) > Interpretation (12%).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <filter id="chartShadow" x="-2%" y="-2%" width="104%" height="108%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="6" result="blur"/>
      <feOffset dx="0" dy="3" result="offsetBlur"/>
      <feFlood flood-color="#000000" flood-opacity="0.08" result="color"/>
      <feComposite in2="offsetBlur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Zone A: Title with icon -->
  <use data-icon="tabler-outline/chart-bar" x="80" y="30" width="28" height="28" fill="{{ACCENT_COLOR}}"/>
  <text x="118" y="55" font-family="{{FONT_FAMILY}}" font-size="28" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>

  <!-- Title underline -->
  <line x1="80" y1="70" x2="380" y2="70" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Zone B: Chart frame (rounded rect path) -->
  <path d="M 108,88 L 1172,88 A 8,8 0 0,1 1180,96 L 1180,480 A 8,8 0 0,1 1172,488 L 108,488 A 8,8 0 0,1 100,480 L 100,96 A 8,8 0 0,1 108,88 Z" fill="{{BG_COLOR}}" stroke="{{BORDER_COLOR}}" stroke-width="1" filter="url(#chartShadow)"/>

  <!-- Chart grid lines (subtle) -->
  <line x1="120" y1="180" x2="1160" y2="180" stroke="{{BORDER_COLOR}}" stroke-width="0.5" stroke-opacity="0.3"/>
  <line x1="120" y1="270" x2="1160" y2="270" stroke="{{BORDER_COLOR}}" stroke-width="0.5" stroke-opacity="0.3"/>
  <line x1="120" y1="360" x2="1160" y2="360" stroke="{{BORDER_COLOR}}" stroke-width="0.5" stroke-opacity="0.3"/>

  <!-- Chart image placeholder -->
  <image x="110" y="98" width="1060" height="380" href="{{CHART_SRC}}" preserveAspectRatio="xMidYMid meet"/>

  <!-- Zone C: Interpretation -->
  <circle cx="108" cy="530" r="6" fill="{{ACCENT_COLOR}}"/>
  <text x="124" y="535" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}">{{INTERPRETATION}}</text>

  <!-- Bottom accent -->
  <rect x="80" y="660" width="80" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 7. Quote

Serif italic text, centered. Decorative large quotation mark rendered as SVG path. Accent line below quote text, attribution with em-dash.

**Zones:** Quotation mark (decorative) > Quote text (primary) > Attribution.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Subtle background accent shape -->
  <rect x="540" y="240" width="200" height="280" fill="{{ACCENT_COLOR}}" fill-opacity="0.03"/>

  <!-- Zone A (decorative): Large opening quotation mark as SVG path -->
  <path d="M 195,265 Q 195,205 250,185 L 262,210 Q 228,222 228,265 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.15"/>
  <path d="M 285,265 Q 285,205 340,185 L 352,210 Q 318,222 318,265 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.15"/>

  <!-- Zone A: Quote text (each line as separate text element) -->
  <text x="640" y="320" font-family="{{FONT_SERIF}}" font-size="28" fill="{{TEXT_PRIMARY}}" font-style="italic" text-anchor="middle">{{QUOTE_LINE_1}}</text>
  <text x="640" y="365" font-family="{{FONT_SERIF}}" font-size="28" fill="{{TEXT_PRIMARY}}" font-style="italic" text-anchor="middle">{{QUOTE_LINE_2}}</text>
  <text x="640" y="410" font-family="{{FONT_SERIF}}" font-size="28" fill="{{TEXT_PRIMARY}}" font-style="italic" text-anchor="middle">{{QUOTE_LINE_3}}</text>

  <!-- Accent line below quote -->
  <line x1="565" y1="445" x2="715" y2="445" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Zone B: Attribution -->
  <text x="640" y="490" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_SECONDARY}}" text-anchor="middle">— {{ATTRIBUTION}}</text>

  <!-- Left accent bar -->
  <rect x="0" y="0" width="4" height="720" fill="{{ACCENT_COLOR}}" fill-opacity="0.2"/>
</svg>
```

---

## 8. Timeline

Horizontal timeline with accent-colored connecting line, filled circle nodes (ring style) at equal intervals. Date labels above nodes, description text below.

**Zones:** Title (top 12%) > Timeline nodes and labels (88%).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Zone A: Title -->
  <text x="80" y="58" font-family="{{FONT_FAMILY}}" font-size="28" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>
  <line x1="80" y1="73" x2="380" y2="73" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Top accent bar -->
  <rect x="80" y="42" width="1120" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.15"/>

  <!-- Timeline horizontal line -->
  <line x1="180" y1="340" x2="1100" y2="340" stroke="{{ACCENT_COLOR}}" stroke-width="3" stroke-linecap="round"/>

  <!-- Node 1: cx=220 -->
  <circle cx="220" cy="340" r="14" fill="{{ACCENT_COLOR}}"/>
  <circle cx="220" cy="340" r="8" fill="{{BG_COLOR}}"/>
  <line x1="220" y1="310" x2="220" y2="280" stroke="{{ACCENT_COLOR}}" stroke-width="1" stroke-opacity="0.4"/>
  <text x="220" y="270" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">{{EVENT_1_DATE}}</text>
  <text x="220" y="385" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{EVENT_1_DESC}}</text>
  <text x="220" y="408" font-family="{{FONT_FAMILY}}" font-size="13" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{EVENT_1_DETAIL}}</text>

  <!-- Node 2: cx=480 -->
  <circle cx="480" cy="340" r="14" fill="{{ACCENT_COLOR}}"/>
  <circle cx="480" cy="340" r="8" fill="{{BG_COLOR}}"/>
  <line x1="480" y1="310" x2="480" y2="280" stroke="{{ACCENT_COLOR}}" stroke-width="1" stroke-opacity="0.4"/>
  <text x="480" y="270" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">{{EVENT_2_DATE}}</text>
  <text x="480" y="385" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{EVENT_2_DESC}}</text>
  <text x="480" y="408" font-family="{{FONT_FAMILY}}" font-size="13" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{EVENT_2_DETAIL}}</text>

  <!-- Node 3: cx=740 -->
  <circle cx="740" cy="340" r="14" fill="{{ACCENT_COLOR}}"/>
  <circle cx="740" cy="340" r="8" fill="{{BG_COLOR}}"/>
  <line x1="740" y1="310" x2="740" y2="280" stroke="{{ACCENT_COLOR}}" stroke-width="1" stroke-opacity="0.4"/>
  <text x="740" y="270" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">{{EVENT_3_DATE}}</text>
  <text x="740" y="385" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{EVENT_3_DESC}}</text>
  <text x="740" y="408" font-family="{{FONT_FAMILY}}" font-size="13" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{EVENT_3_DETAIL}}</text>

  <!-- Node 4: cx=1000 -->
  <circle cx="1000" cy="340" r="14" fill="{{ACCENT_COLOR}}"/>
  <circle cx="1000" cy="340" r="8" fill="{{BG_COLOR}}"/>
  <line x1="1000" y1="310" x2="1000" y2="280" stroke="{{ACCENT_COLOR}}" stroke-width="1" stroke-opacity="0.4"/>
  <text x="1000" y="270" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">{{EVENT_4_DATE}}</text>
  <text x="1000" y="385" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{EVENT_4_DESC}}</text>
  <text x="1000" y="408" font-family="{{FONT_FAMILY}}" font-size="13" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{EVENT_4_DETAIL}}</text>

  <!-- Bottom accent -->
  <rect x="80" y="660" width="80" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 9. Comparison

Header row with accent-colored rounded rect backgrounds for each option. Criteria rows with alternating subtle backgrounds. Vertical dividers separate label column from option columns.

**Zones:** Title (top 10%) > Header row > Criteria rows (90%, 50/50 split).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Zone A: Title -->
  <text x="80" y="55" font-family="{{FONT_FAMILY}}" font-size="28" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>
  <line x1="80" y1="70" x2="380" y2="70" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Header row backgrounds (rounded rects) -->
  <path d="M 366,95 L 774,95 A 6,6 0 0,1 780,101 L 780,139 A 6,6 0 0,1 774,145 L 366,145 A 6,6 0 0,1 360,139 L 360,101 A 6,6 0 0,1 366,95 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.1"/>
  <path d="M 806,95 L 1214,95 A 6,6 0 0,1 1220,101 L 1220,139 A 6,6 0 0,1 1214,145 L 806,145 A 6,6 0 0,1 800,139 L 800,101 A 6,6 0 0,1 806,95 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.1"/>

  <!-- Header row text -->
  <text x="100" y="126" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_TERTIARY}}" font-weight="bold">CRITERIA</text>
  <text x="570" y="126" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_PRIMARY}}" text-anchor="middle" font-weight="bold">{{OPTION_A}}</text>
  <text x="1010" y="126" font-family="{{FONT_FAMILY}}" font-size="20" fill="{{TEXT_PRIMARY}}" text-anchor="middle" font-weight="bold">{{OPTION_B}}</text>

  <!-- Header icons -->
  <use data-icon="tabler-outline/letter-a" x="490" y="105" width="24" height="24" fill="{{ACCENT_COLOR}}" fill-opacity="0.5"/>
  <use data-icon="tabler-outline/letter-b" x="930" y="105" width="24" height="24" fill="{{ACCENT_COLOR}}" fill-opacity="0.5"/>

  <!-- Vertical column dividers -->
  <line x1="350" y1="95" x2="350" y2="560" stroke="{{BORDER_COLOR}}" stroke-width="1" stroke-opacity="0.4"/>
  <line x1="790" y1="95" x2="790" y2="560" stroke="{{BORDER_COLOR}}" stroke-width="1" stroke-opacity="0.4"/>

  <!-- Row 1 (alternating bg) -->
  <path d="M 104,160 L 1216,160 A 4,4 0 0,1 1220,164 L 1220,224 A 4,4 0 0,1 1216,228 L 104,228 A 4,4 0 0,1 100,224 L 100,164 A 4,4 0 0,1 104,160 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.03"/>
  <text x="120" y="200" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{CRITERIA_LABEL_1}}</text>
  <text x="570" y="200" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{CRITERIA_A_1}}</text>
  <text x="1010" y="200" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{CRITERIA_B_1}}</text>

  <!-- Row 2 -->
  <text x="120" y="275" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{CRITERIA_LABEL_2}}</text>
  <text x="570" y="275" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{CRITERIA_A_2}}</text>
  <text x="1010" y="275" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{CRITERIA_B_2}}</text>

  <!-- Row 3 (alternating bg) -->
  <path d="M 104,305 L 1216,305 A 4,4 0 0,1 1220,309 L 1220,369 A 4,4 0 0,1 1216,373 L 104,373 A 4,4 0 0,1 100,369 L 100,309 A 4,4 0 0,1 104,305 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.03"/>
  <text x="120" y="345" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{CRITERIA_LABEL_3}}</text>
  <text x="570" y="345" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{CRITERIA_A_3}}</text>
  <text x="1010" y="345" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{CRITERIA_B_3}}</text>

  <!-- Row 4 -->
  <text x="120" y="420" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{CRITERIA_LABEL_4}}</text>
  <text x="570" y="420" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{CRITERIA_A_4}}</text>
  <text x="1010" y="420" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{CRITERIA_B_4}}</text>

  <!-- Bottom accent -->
  <rect x="80" y="660" width="80" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 10. Closing

Vertically centered layout. Key takeaway headline, CTA text inside a rounded button shape, contact info with icon placeholders. Top and bottom accent bars with gradient overlay.

**Zones:** Takeaway (primary) > CTA button > Contact info.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="closingGrad" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="{{ACCENT_COLOR}}" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="{{BG_COLOR}}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#closingGrad)"/>

  <!-- Top accent bar -->
  <rect x="0" y="0" width="1280" height="4" fill="{{ACCENT_COLOR}}"/>

  <!-- Bottom accent bar -->
  <rect x="0" y="716" width="1280" height="4" fill="{{ACCENT_COLOR}}"/>

  <!-- Left accent strip -->
  <rect x="0" y="0" width="4" height="720" fill="{{ACCENT_COLOR}}" fill-opacity="0.2"/>

  <!-- Decorative corner arc -->
  <path d="M 1280,720 L 1100,720 A 180,180 0 0,1 1280,540 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.04"/>

  <!-- Zone A: Takeaway -->
  <text x="640" y="280" font-family="{{FONT_FAMILY}}" font-size="42" fill="{{TEXT_PRIMARY}}" text-anchor="middle" font-weight="bold">{{TAKEAWAY}}</text>

  <!-- Accent line below takeaway -->
  <line x1="540" y1="305" x2="740" y2="305" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Zone B: CTA button (rounded rect path) -->
  <path d="M 520,340 L 760,340 A 25,25 0 0,1 785,365 L 785,365 A 25,25 0 0,1 760,390 L 520,390 A 25,25 0 0,1 495,365 L 495,365 A 25,25 0 0,1 520,340 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.1" stroke="{{ACCENT_COLOR}}" stroke-width="1.5"/>
  <text x="640" y="371" font-family="{{FONT_FAMILY}}" font-size="18" fill="{{ACCENT_COLOR}}" text-anchor="middle" font-weight="bold">{{CTA_TEXT}}</text>

  <!-- Zone C: Contact info with icons -->
  <use data-icon="tabler-outline/mail" x="530" y="432" width="20" height="20" fill="{{TEXT_TERTIARY}}" fill-opacity="0.6"/>
  <text x="560" y="448" font-family="{{FONT_FAMILY}}" font-size="14" fill="{{TEXT_TERTIARY}}">{{CONTACT_INFO}}</text>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 11. Composite-Diagram

Multi-level nested box architecture. Outer container with heavy stroke, subsystem boxes with medium stroke, component boxes with light stroke. Three horizontal layers demonstrating nesting depth.

**Zones:** Title (top 8%) > Diagram layers (92%, up to 3 nesting levels).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Zone A: Title -->
  <text x="80" y="52" font-family="{{FONT_FAMILY}}" font-size="26" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>
  <line x1="80" y1="66" x2="380" y2="66" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Zone B: Diagram area -->

  <!-- Outer container (heavy stroke, r=10) -->
  <path d="M 90,80 L 1190,80 A 10,10 0 0,1 1200,90 L 1200,565 A 10,10 0 0,1 1190,575 L 90,575 A 10,10 0 0,1 80,565 L 80,90 A 10,10 0 0,1 90,80 Z" fill="none" stroke="{{TEXT_PRIMARY}}" stroke-width="2" stroke-opacity="0.15"/>

  <!-- Top Layer: Box A (r=6) -->
  <path d="M 106,100 L 619,100 A 6,6 0 0,1 625,106 L 625,174 A 6,6 0 0,1 619,180 L 106,180 A 6,6 0 0,1 100,174 L 100,106 A 6,6 0 0,1 106,100 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.06" stroke="{{TEXT_PRIMARY}}" stroke-width="1" stroke-opacity="0.2"/>
  <text x="362" y="146" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{LAYER_1_LABEL_A}}</text>

  <!-- Top Layer: Box B (r=6) -->
  <path d="M 656,100 L 1174,100 A 6,6 0 0,1 1180,106 L 1180,174 A 6,6 0 0,1 1174,180 L 656,180 A 6,6 0 0,1 650,174 L 650,106 A 6,6 0 0,1 656,100 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.06" stroke="{{TEXT_PRIMARY}}" stroke-width="1" stroke-opacity="0.2"/>
  <text x="915" y="146" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{LAYER_1_LABEL_B}}</text>

  <!-- Middle Layer: Wide box with nested children (r=6) -->
  <path d="M 106,200 L 619,200 A 6,6 0 0,1 625,206 L 625,429 A 6,6 0 0,1 619,435 L 106,435 A 6,6 0 0,1 100,429 L 100,206 A 6,6 0 0,1 106,200 Z" fill="none" stroke="{{TEXT_PRIMARY}}" stroke-width="1" stroke-opacity="0.25"/>
  <text x="362" y="225" font-family="{{FONT_FAMILY}}" font-size="15" fill="{{TEXT_PRIMARY}}" font-weight="bold" text-anchor="middle">{{LAYER_2_LABEL}}</text>

  <!-- Nested child 1 (r=4) -->
  <path d="M 119,248 L 606,248 A 4,4 0 0,1 610,252 L 610,290 A 4,4 0 0,1 606,294 L 119,294 A 4,4 0 0,1 115,290 L 115,252 A 4,4 0 0,1 119,248 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.04" stroke="{{BORDER_COLOR}}" stroke-width="1"/>
  <text x="362" y="276" font-family="{{FONT_FAMILY}}" font-size="14" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{NODE_1_LABEL}}</text>

  <!-- Nested child 2 (r=4) -->
  <path d="M 119,306 L 606,306 A 4,4 0 0,1 610,310 L 610,348 A 4,4 0 0,1 606,352 L 119,352 A 4,4 0 0,1 115,348 L 115,310 A 4,4 0 0,1 119,306 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.04" stroke="{{BORDER_COLOR}}" stroke-width="1"/>
  <text x="362" y="334" font-family="{{FONT_FAMILY}}" font-size="14" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{NODE_2_LABEL}}</text>

  <!-- Nested child 3 (r=4) -->
  <path d="M 119,364 L 606,364 A 4,4 0 0,1 610,368 L 610,406 A 4,4 0 0,1 606,410 L 119,410 A 4,4 0 0,1 115,406 L 115,368 A 4,4 0 0,1 119,364 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.04" stroke="{{BORDER_COLOR}}" stroke-width="1"/>
  <text x="362" y="392" font-family="{{FONT_FAMILY}}" font-size="14" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{NODE_3_LABEL}}</text>

  <!-- Middle Layer: Side box (r=6) -->
  <path d="M 656,200 L 1174,200 A 6,6 0 0,1 1180,206 L 1180,429 A 6,6 0 0,1 1174,435 L 656,435 A 6,6 0 0,1 650,429 L 650,206 A 6,6 0 0,1 656,200 Z" fill="none" stroke="{{TEXT_PRIMARY}}" stroke-width="1" stroke-opacity="0.25"/>
  <text x="915" y="320" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{LAYER_2_LABEL_B}}</text>

  <!-- Bottom Layer: Full-width box (r=6) -->
  <path d="M 106,460 L 1174,460 A 6,6 0 0,1 1180,466 L 1180,544 A 6,6 0 0,1 1174,550 L 106,550 A 6,6 0 0,1 100,544 L 100,466 A 6,6 0 0,1 106,460 Z" fill="{{ACCENT_COLOR}}" fill-opacity="0.06" stroke="{{TEXT_PRIMARY}}" stroke-width="1" stroke-opacity="0.2"/>
  <text x="640" y="512" font-family="{{FONT_FAMILY}}" font-size="17" fill="{{TEXT_PRIMARY}}" text-anchor="middle">{{LAYER_3_LABEL}}</text>

  <!-- Bottom accent -->
  <rect x="80" y="660" width="80" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```

---

## 12. Pipeline-Flow

Sequential stage boxes with arrow connectors. Arrowhead defined as `<marker>` in `<defs>`. Each stage box is a rounded rect with name and description. Sub-step labels below the pipeline.

**Zones:** Title (top 12%) > Pipeline stages (88%, equal-width with arrows).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="{{ACCENT_COLOR}}"/>
    </marker>
    <linearGradient id="stageGrad" gradientUnits="userSpaceOnUse" x1="0" y1="270" x2="0" y2="420">
      <stop offset="0%" stop-color="{{ACCENT_COLOR}}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{{BG_COLOR}}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="{{BG_COLOR}}"/>

  <!-- Top accent bar -->
  <rect x="80" y="42" width="1120" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.15"/>

  <!-- Zone A: Title -->
  <text x="80" y="85" font-family="{{FONT_FAMILY}}" font-size="28" fill="{{TEXT_PRIMARY}}" font-weight="bold">{{TITLE}}</text>
  <line x1="80" y1="100" x2="380" y2="100" stroke="{{ACCENT_COLOR}}" stroke-width="2" stroke-linecap="round"/>

  <!-- Stage 1 box (x=50, y=280, w=220, h=130, r=10) -->
  <path d="M 60,280 L 260,280 A 10,10 0 0,1 270,290 L 270,400 A 10,10 0 0,1 260,410 L 60,410 A 10,10 0 0,1 50,400 L 50,290 A 10,10 0 0,1 60,280 Z" fill="url(#stageGrad)" stroke="{{ACCENT_COLOR}}" stroke-width="1.5" stroke-opacity="0.4"/>
  <text x="160" y="330" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_PRIMARY}}" text-anchor="middle" font-weight="bold">{{STAGE_1_NAME}}</text>
  <text x="160" y="355" font-family="{{FONT_FAMILY}}" font-size="13" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{STAGE_1_DESC}}</text>

  <!-- Arrow 1 -->
  <line x1="280" y1="345" x2="360" y2="345" stroke="{{ACCENT_COLOR}}" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Stage 2 box (x=370) -->
  <path d="M 380,280 L 580,280 A 10,10 0 0,1 590,290 L 590,400 A 10,10 0 0,1 580,410 L 380,410 A 10,10 0 0,1 370,400 L 370,290 A 10,10 0 0,1 380,280 Z" fill="url(#stageGrad)" stroke="{{ACCENT_COLOR}}" stroke-width="1.5" stroke-opacity="0.4"/>
  <text x="480" y="330" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_PRIMARY}}" text-anchor="middle" font-weight="bold">{{STAGE_2_NAME}}</text>
  <text x="480" y="355" font-family="{{FONT_FAMILY}}" font-size="13" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{STAGE_2_DESC}}</text>

  <!-- Arrow 2 -->
  <line x1="600" y1="345" x2="680" y2="345" stroke="{{ACCENT_COLOR}}" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Stage 3 box (x=690) -->
  <path d="M 700,280 L 900,280 A 10,10 0 0,1 910,290 L 910,400 A 10,10 0 0,1 900,410 L 700,410 A 10,10 0 0,1 690,400 L 690,290 A 10,10 0 0,1 700,280 Z" fill="url(#stageGrad)" stroke="{{ACCENT_COLOR}}" stroke-width="1.5" stroke-opacity="0.4"/>
  <text x="800" y="330" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_PRIMARY}}" text-anchor="middle" font-weight="bold">{{STAGE_3_NAME}}</text>
  <text x="800" y="355" font-family="{{FONT_FAMILY}}" font-size="13" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{STAGE_3_DESC}}</text>

  <!-- Arrow 3 -->
  <line x1="920" y1="345" x2="1000" y2="345" stroke="{{ACCENT_COLOR}}" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Stage 4 box (x=1010) -->
  <path d="M 1020,280 L 1220,280 A 10,10 0 0,1 1230,290 L 1230,400 A 10,10 0 0,1 1220,410 L 1020,410 A 10,10 0 0,1 1010,400 L 1010,290 A 10,10 0 0,1 1020,280 Z" fill="url(#stageGrad)" stroke="{{ACCENT_COLOR}}" stroke-width="1.5" stroke-opacity="0.4"/>
  <text x="1120" y="330" font-family="{{FONT_FAMILY}}" font-size="16" fill="{{TEXT_PRIMARY}}" text-anchor="middle" font-weight="bold">{{STAGE_4_NAME}}</text>
  <text x="1120" y="355" font-family="{{FONT_FAMILY}}" font-size="13" fill="{{TEXT_SECONDARY}}" text-anchor="middle">{{STAGE_4_DESC}}</text>

  <!-- Sub-step labels below pipeline -->
  <text x="160" y="450" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{STAGE_1_SUB}}</text>
  <text x="480" y="450" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{STAGE_2_SUB}}</text>
  <text x="800" y="450" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{STAGE_3_SUB}}</text>
  <text x="1120" y="450" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="middle">{{STAGE_4_SUB}}</text>

  <!-- Stage number badges -->
  <circle cx="70" cy="295" r="12" fill="{{ACCENT_COLOR}}"/>
  <text x="70" y="300" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{BG_COLOR}}" text-anchor="middle" font-weight="bold">1</text>
  <circle cx="390" cy="295" r="12" fill="{{ACCENT_COLOR}}"/>
  <text x="390" y="300" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{BG_COLOR}}" text-anchor="middle" font-weight="bold">2</text>
  <circle cx="710" cy="295" r="12" fill="{{ACCENT_COLOR}}"/>
  <text x="710" y="300" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{BG_COLOR}}" text-anchor="middle" font-weight="bold">3</text>
  <circle cx="1030" cy="295" r="12" fill="{{ACCENT_COLOR}}"/>
  <text x="1030" y="300" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{BG_COLOR}}" text-anchor="middle" font-weight="bold">4</text>

  <!-- Bottom accent -->
  <rect x="80" y="660" width="80" height="3" fill="{{ACCENT_COLOR}}" fill-opacity="0.4"/>

  <!-- Page number -->
  <text x="1230" y="700" font-family="{{FONT_FAMILY}}" font-size="12" fill="{{TEXT_TERTIARY}}" text-anchor="end">{{PAGE_NUM}}</text>
</svg>
```
