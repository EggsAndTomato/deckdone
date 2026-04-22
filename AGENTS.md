# AGENTS.md — DeckDone Repository

## Repo Structure

This is a **skill repository** containing two opencode skills. The repo root holds project-level documentation.

```
<repo root>/
  skills/
    deckdone-plan/        ← Skill 1: Content planning (Steps 1-5)
      SKILL.md              Entrypoint — Discovery → Layout → Content wireframe review
      references/           Decision-support docs read by AI at runtime
      scripts/              Validation scripts (Python, stdlib only)
    deckdone-build/        ← Skill 2: Visual style + PPTX generation (Steps 6-8)
      SKILL.md              Entrypoint — Style selection → SVG generation → PPTX export
      references/           SVG templates, constraints, quality checklists, style presets
      scripts/              SVG→DrawingML converter + validators
      templates/            Chart templates (52), icons (6,092), layout templates (3)
```

## Skill Architecture

**deckdone-plan** — produces editable markdown deliverables (brief, outline, layout-system, content-plan, layout-skeleton). Content-only planning with no visual style decisions. Step 5 uses live HTML wireframes for real-time content review.

**deckdone-build** — starts with visual style selection (from presets), then produces PPTX via SVG→DrawingML pipeline. Consumes content-plan and layout-skeleton from deckdone-plan. Includes revision mode for post-completion modifications.

The two skills are independent: deckdone-build can consume plans from deckdone-plan, from manual authoring, or from any tool that produces the same markdown format.

## Workflow Overview

| Step | Skill | Phase | Goal |
|------|-------|-------|------|
| 1 | plan | Discovery | Presentation brief |
| 2 | plan | Discovery | Material collection |
| 3 | plan | Discovery | Content outline |
| 4 | plan | Layout | Page type assignment |
| 5 | plan | Layout + Content | HTML wireframe review → content-plan + layout-skeleton |
| 6 | build | Visual Style | Style selection + test page generation |
| 7 | build | Generation | Batch SVG generation + quality review |
| 8 | build | Export | Final PPTX + presentation guide |

## Validation Scripts

```bash
# Validate content-plan.md structure (deckdone-plan, after Step 5)
python skills/deckdone-plan/scripts/validate-content-plan.py <content-plan.md>

# Validate SVG files for svg_to_pptx compatibility (deckdone-build, after Step 7)
python skills/deckdone-build/scripts/validate-svg-slides.py <svg-directory/> [--outline outline.md]
```

Both exit 0 on pass, 1 on any failure.

## Key Conventions

- **Language**: SKILL.md and all reference files are in English. The AI communicates with users in their preferred language.
- **Plan = content only**: No visual style decisions in deckdone-plan. Colors, fonts, decoration belong to deckdone-build.
- **HTML wireframes**: Low-fidelity, no visual styling, auto-refresh for live browser review during Step 5. Chart zones show type/title/axes as placeholders.
- **SVG constraints**: viewBox `0 0 1280 720`, no CSS `<style>`, no `<rect rx="">`, no `<g opacity>`, no `rgba()`, no multi-line `<tspan>`. See `deckdone-build/references/svg-constraints.md`.
- **Valid page types**: Cover, Agenda, Section Divider, Content-Text, Content-TwoCol, Data-Chart, Quote, Timeline, Comparison, Closing, Composite-Diagram, Pipeline-Flow.
- **Content plan fields**: Each zone needs `- Type:`, `- Content:` (non-empty), `- Max Length:`, `- Visual Weight:` (primary|secondary|auxiliary).
- **Style presets**: 18 curated presets in `deckdone-build/references/style-presets.md` (moved from deckdone-plan).

## Dependencies

- **deckdone-plan**: Python stdlib only. Optional: pdf/docx skills for material extraction.
- **deckdone-build**: python-pptx, lxml. SVG converter uses stdlib xml.etree only (no additional deps).
- **Template assets**: 52 chart SVGs, 6,092 tabler icons (MIT), 3 layout templates — all bundled, no download needed.

## When Editing This Repo

- Do not modify either SKILL.md beyond ~450 lines. Move content to reference files and add cross-references.
- The harness improvement principle: when a generated slide has quality issues, fix the harness (reference files, validation rules, SVG constraints), not just the individual slide.
- The `svg_to_pptx/` package is forked from PPT Master. Upstream fixes should be evaluated and ported, but the fork has its own bug fixes not in upstream.
- The `docs/` directory contains design specs — historical reference only, not authoritative if they conflict with actual files.
