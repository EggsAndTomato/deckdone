# SVG Generation Constraints

Rules for AI-generated SVG slides in DeckDone. All SVGs must comply with these constraints to convert correctly to PPTX via the svg_to_pptx converter.

## Canvas

- viewBox: `0 0 1280 720` (16:9 widescreen)
- width and height attributes must match: `width="1280" height="720"`
- All positioning is absolute pixel coordinates (no CSS layout, no flexbox, no flow)
- Background via `<rect>` elements only

## Banned Elements (DrawingML Incompatible)

| Banned | Alternative |
|--------|------------|
| `<foreignObject>` | Use `<text>` elements |
| `<mask>` | Use `fill-opacity` / `stroke-opacity` |
| `<style>` / `class` | Use inline styles only |
| `textPath` | Use plain `<text>` positioning |
| `<animate*>` | Static design only |
| `<script>` | No interactivity |
| `<iframe>` | Not applicable |
| `rgba()` | Use hex color + separate `fill-opacity` |
| CSS `linear-gradient()` | Use SVG `<defs>` `<linearGradient>` |
| CSS `radial-gradient()` | Use SVG `<defs>` `<radialGradient>` |
| `<g opacity="...">` | Set opacity on each child element individually |
| `<rect rx="..." ry="...">` | Write `<path>` with arc commands for rounded rectangles |
| `<tspan>` with `y` or `dy` | Use separate `<text>` elements per line |
| `preserveAspectRatio="slice"` | Use `xMidYMid meet` only |

## Text Rules

- Use separate `<text>` elements for each line of text (NOT multi-line `<tspan>`)
- Single `<tspan>` within a `<text>` is allowed for inline style variations
- Font stack: Arial, Georgia, Verdana, Tahoma, Trebuchet MS, Times New Roman, Courier New, Impact
- `font-size` in px only
- `text-anchor`: start | middle | end
- `dominant-baseline`: auto | middle | hanging
- Letter-spacing: bare number values only (SVG px units)

## Gradients

- Define in `<defs>` block at the top of the SVG
- `<linearGradient>` and `<radialGradient>` are supported
- Use `gradientUnits="userSpaceOnUse"` with explicit x1/y1/x2/y2 coordinates
- Stop colors must be hex format (#RRGGBB), not named colors or rgb()
- Stop opacity via `stop-opacity` attribute

## Images

- `<image>` elements supported with base64 data URIs or local file references
- `preserveAspectRatio="xMidYMid meet"` only — never "slice" or "xMinYMin slice"
- For base64: `href="data:image/png;base64,..."`
- For local files: `href="images/photo.png"`
- All images must be self-contained within the SVG or reference local files

## Icons

- Use placeholder syntax: `<use data-icon="tabler-filled/name" x="100" y="200" width="48" height="48" fill="#0076A8"/>`
- Or: `<use data-icon="tabler-outline/name" .../>`
- One icon library per presentation (never mix filled and outline)
- Recommended size: 32-48px for legibility
- Icons are resolved at build time by embed_icons.py

## Structure

- Every SVG must start with `<defs>` block for gradients/filters before first visual element
- Group visual sections with `<g>` tags and descriptive comments: `<!-- Header -->`, `<!-- Content Area -->`
- Each SVG file = one slide page
- Use meaningful element ordering: background → decorations → content → foreground

## File Naming

- Pattern: `P01_Cover.svg`, `P02_Agenda.svg`, `P03_Chapter_1.svg`, etc.
- Page number prefix (P01, P02...) for sort order
- Descriptive name after underscore
- No spaces in filenames (use underscores)

## Shape Drawing

- Rounded rectangles: use `<path>` with arc commands, NOT `<rect rx="">`
- Circles: `<circle>` or `<ellipse>` (both supported)
- Lines: `<line>` with stroke attributes
- Arrow connectors: `<line>` or `<path>` with `marker-end="url(#arrowhead)"`
- Arrow markers defined in `<defs>` as `<marker>` elements
- Complex shapes: `<path>` with M/L/C/A/Z commands

## Shadows and Effects

- `filter` elements in `<defs>` for drop shadows
- `feDropShadow` or `feGaussianBlur` + `feOffset` for shadow effects
- `fill-opacity` for transparency effects
- No `mix-blend-mode` (not supported in DrawingML)
