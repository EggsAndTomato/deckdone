# Page Layout Templates (3 Templates)

Pre-built PPT page layout templates for DeckDone.

- **JSON Index**: [layouts_index.json](./layouts_index.json) (AI / programmatic lookup — preferred)

---

| Template | Category | Use Cases | Primary Color | Tone |
|----------|----------|-----------|---------------|------|
| `exhibit` | General | Strategic reports, executive presentations, board briefings | Gradient top bar + Gold accents | Conclusion-first, data-driven |
| `tech_blue` | General | Corporate reports, product launches, proposals | Tech Blue `#0078D7` | Professional, tech, clean |
| `smart_red` | General | Tech company profiles, education solutions | Smart Red-Orange `#DE3545` | Modern, vibrant, geometric |

---

## Template File Structure

Each template contains:

| Filename | Required | Purpose |
|----------|----------|---------|
| `design_spec.md` | Yes | Complete color, typography, and layout specs |
| `01_cover.svg` | Yes | Cover page |
| `02_toc.svg` | Optional | Table of contents |
| `02_chapter.svg` | Yes | Chapter/section divider |
| `03_content.svg` | Yes | Content page |
| `04_ending.svg` | Yes | Ending/closing page |

## Usage

Copy a template to your project directory:

```bash
cp templates/layouts/tech_blue/* <project_path>/templates/
```

Then read `design_spec.md` to understand the design specification before generating SVGs.

## SVG Technical Constraints

- viewBox: `0 0 1280 720`
- No CSS `<style>`, no `<rect rx="">`, no `<g opacity>`, no `rgba()`
- See `references/svg-constraints.md` for full rules
