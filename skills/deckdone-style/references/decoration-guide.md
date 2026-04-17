# Decoration Guide — Per-Page-Type Rules

Reference for Step 7 (Content Plan) and Step 9/10 (Generation). Defines which visual elements (icons, illustrations, decorative patterns) are placed where on each page type.

## Severity Levels

| Level | Meaning |
|-------|---------|
| REQUIRED | Must be present. Missing = validation failure. |
| RECOMMENDED | Should be present. Absence tolerated but logged. |
| OPTIONAL | Nice to have. No validation impact. |

---

## Cover

- **[REQUIRED]** Right or bottom 25% area: illustration from unDraw (fetched via `fetch-illustration.py`)
- **[REQUIRED]** Title left: 48pt icon matching the presentation's main theme (from `icon-catalog.md`)
- **[OPTIONAL]** Background: subtle gradient or geometric pattern in accent color tint (10% opacity)

## Agenda

- **[RECOMMENDED]** Each numbered item: 16pt icon prefix matching the section theme
- **[OPTIONAL]** Right margin: vertical accent line in primary color

## Section Divider

- **[REQUIRED]** Title left: 40pt icon reflecting the section's theme
- **[RECOMMENDED]** Bottom 20%: illustration from unDraw or decorative pattern
- **[OPTIONAL]** Background: subtle accent tint (5% opacity overlay)

## Content-Text

- **[RECOMMENDED]** Each top-level bullet: 16pt icon prefix (semantic match from catalog)
- **[OPTIONAL]** Title underline: 2px accent color line, 48pt wide, 4pt below title
- **[OPTIONAL]** Left margin: thin vertical accent line (1px, 20% opacity)

## Content-TwoCol

- **[RECOMMENDED]** Each column heading: 24pt icon prefix
- **[OPTIONAL]** Center divider: 1px line in secondary color
- **[OPTIONAL]** Each bullet: 14pt icon prefix

## Data-Chart

- **[REQUIRED]** Chart area: pre-rendered PNG chart (existing deckdone behavior)
- **[RECOMMENDED]** Interpretation text area: 16pt `info-circle` or `trending-up` icon prefix
- **[OPTIONAL]** Chart border: 1px rounded rectangle in secondary color

## Quote

- **[RECOMMENDED]** Large decorative opening quotation mark (60pt, accent color, 30% opacity)
- **[OPTIONAL]** Closing quotation mark (right-aligned, 40pt)
- No icons — Quote pages use typography as decoration.

## Timeline

- **[REQUIRED]** Each event node: 24pt icon (circular crop, `border-radius: 50%`)
  - Default icons: `clock` for past, `flag` for current, `rocket` for future
  - Override with semantic theme icons from catalog
- **[RECOMMENDED]** Connecting line: 2px solid primary color between nodes
- **[OPTIONAL]** Node background: small circular fill in accent color (behind icon)

## Comparison

- **[RECOMMENDED]** Each side header: 24pt icon (e.g., `check` vs `x`, or thematic icons)
- **[RECOMMENDED]** Boolean comparison cells: ✓ (`check` icon) / ✗ (`x` icon) instead of text
- **[OPTIONAL]** Alternating row background tint (5% primary color)

## Closing

- **[REQUIRED]** Centered icon above takeaway: 48pt `flag` or `rocket` or theme icon
- **[OPTIONAL]** Background: subtle gradient matching cover slide (bookend effect)
- **[OPTIONAL]** Bottom decorative line in accent color

## Composite-Diagram

- **[RECOMMENDED]** Subsystem/layer header: 20pt icon prefix
- **[OPTIONAL]** Background tint per layer (alternating 3% and 5% primary color)
- **[OPTIONAL]** Connection arrows: 1px lines with arrowheads in secondary color

## Pipeline-Flow

- **[REQUIRED]** Each stage header: 32pt icon (semantic match: `search` → input, `settings` → process, `check` → validate, `rocket` → output)
- **[REQUIRED]** Arrow connectors: SVG arrow style (not plain `→` text). Use a styled `<div>` with chevron icon or CSS triangle in primary color.
- **[RECOMMENDED]** Stage cards: 1pt border in primary color, 4px border-radius
- **[OPTIONAL]** Active/current stage: accent color border highlight (2pt)
