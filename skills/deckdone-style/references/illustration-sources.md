# Illustration Sources

Reference for Step 9/10 (Generation). Provides illustration source configuration for fetching themed SVG illustrations.

---

## unDraw (Primary Source)

| Property | Value |
|----------|-------|
| **URL** | https://undraw.co |
| **License** | Free, no attribution required |
| **Format** | SVG |
| **Color customization** | Replace default `#6C63FF` with accent color |
| **Best for** | Cover slides, Section Dividers |

### How It Works

1. Browse or search illustrations at https://undraw.co/illustrations
2. Each illustration has a slug (visible in the URL, e.g., `business-plan`)
3. `fetch-illustration.py` downloads the SVG and swaps the primary color
4. The SVG/PNG is placed in the slide's illustration zone

### Color Replacement

All unDraw SVGs use a single primary color (`#6C63FF`). The fetch script:
1. Replaces `#6C63FF` and `#6c63ff` (case-insensitive) with the preset's accent color
2. If neither color is found: replaces the most frequent hex color (heuristic fallback, logs warning)

---

## Recommended Illustrations by Presentation Theme

| Section Theme | Recommended Slugs | Visual Description |
|---------------|-------------------|-------------------|
| Business Strategy | `business-plan`, `strategy`, `growth` | Charts, targets, upward arrows |
| Technology | `developer-activity`, `coding`, `server` | Screens, code, devices |
| Team & People | `team-spirit`, `collaboration`, `meeting` | People working together |
| Data & Analytics | `data-analysis`, `statistics`, `metrics` | Dashboards, graphs |
| Success & Goals | `finish-line`, `achiever`, `winner` | Trophies, checkmarks, celebrations |
| Innovation | `innovative`, `creative`, `brainstorming` | Lightbulbs, rockets, ideas |
| Finance | `investment`, `savings`, `finance` | Money, charts, growth |
| Communication | `messaging`, `presentation`, `connecting` | Speech bubbles, devices |
| Education | `education`, `learning`, `knowledge` | Books, graduation, classroom |
| Security | `security`, `protection`, `safe` | Shields, locks, guards |
| Health | `health`, `medical`, `wellness` | Hearts, medical, activity |
| Travel | `travel`, `adventure`, `destination` | Maps, planes, landmarks |

---

## Access Notes

- unDraw is accessible from China mainland (verified 2026-04)
- The API endpoint `undraw.co/api/illustration/{slug}` is unofficial and may change
- If unDraw is unreachable: degrade to CSS geometric patterns (circles, rectangles) using the accent color
- Pre-downloaded fallback illustrations could be added to `references/illustrations/` if needed

## Alternative Sources (Future)

These are NOT currently integrated but noted for potential future use:

| Source | URL | License | Notes |
|--------|-----|---------|-------|
| Open Peeps | https://www.openpeeps.com | CC0 | Hand-drawn characters; requires Figma/Sketch |
| Open Doodles | https://www.opendoodles.com | CC0 | Sketchy illustrations; direct SVG download |
| Humaaans | https://www.humaaans.com | CC0 | Mix-and-match people; Figma-based |
| DrawKit | https://www.drawkit.com | MIT (free tier) | Polished illustrations; some premium |
