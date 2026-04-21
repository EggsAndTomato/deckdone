# AGENTS.md — DeckDone Repository

## Repo Structure

This is a **skill repository** containing two opencode skills. The repo root holds project-level documentation.

```
<repo root>/
  skills/
    deckdone-plan/        ← Skill 1: Content planning (Steps 1-8)
      SKILL.md              Entrypoint — phased workflow for Discovery → Design → Content
      references/           Decision-support docs read by AI at runtime
      scripts/              Validation scripts (Python, stdlib only)
    deckdone-build/        ← Skill 2: PPTX generation (Steps 9-12)
      SKILL.md              Entrypoint — SVG generation → PPTX export
      references/           SVG templates, constraints, quality checklists
      scripts/              SVG→DrawingML converter + validators
      templates/            Chart templates (52), icons (6,092), layout templates (3)
```

## Skill Architecture

**deckdone-plan** — produces editable markdown deliverables (brief, outline, content-plan, style-guide, layout-skeleton). Content-first, gate-controlled. No rendering logic.

**deckdone-build** — consumes markdown plans and produces PPTX via SVG→DrawingML pipeline. Zero creative decisions — everything comes from input files. The SVG converter is forked from PPT Master (MIT license) with bug fixes.

The two skills are independent: deckdone-build can consume plans from deckdone-plan, from manual authoring, or from any tool that produces the same markdown format.

## Validation Scripts

```bash
# Validate content-plan.md structure (deckdone-plan, after Step 7)
python skills/deckdone-plan/scripts/validate-content-plan.py <content-plan.md>

# Validate SVG files for svg_to_pptx compatibility (deckdone-build, after Steps 9-10)
python skills/deckdone-build/scripts/validate-svg-slides.py <svg-directory/> [--outline outline.md]
```

Both exit 0 on pass, 1 on any failure.

## Key Conventions

- **Language**: SKILL.md and all reference files are in English. The AI communicates with users in their preferred language.
- **SVG constraints**: viewBox `0 0 1280 720`, no CSS `<style>`, no `<rect rx="">`, no `<g opacity>`, no `rgba()`, no multi-line `<tspan>`. See `deckdone-build/references/svg-constraints.md`.
- **Valid page types**: Cover, Agenda, Section Divider, Content-Text, Content-TwoCol, Data-Chart, Quote, Timeline, Comparison, Closing, Composite-Diagram, Pipeline-Flow.
- **Content plan fields**: Each zone needs `- Type:`, `- Content:` (non-empty), `- Max Length:`, `- Visual Weight:` (primary|secondary|auxiliary).

## Dependencies

- **deckdone-plan**: Python stdlib only. Optional: pdf/docx skills for material extraction.
- **deckdone-build**: python-pptx, lxml. SVG converter uses stdlib xml.etree only (no additional deps).
- **Template assets**: 52 chart SVGs, 6,092 tabler icons (MIT), 3 layout templates — all bundled, no download needed.

## When Editing This Repo

- Do not modify either SKILL.md beyond ~450 lines. Move content to reference files and add cross-references.
- The harness improvement principle: when a generated slide has quality issues, fix the harness (reference files, validation rules, SVG constraints), not just the individual slide.
- The `svg_to_pptx/` package is forked from PPT Master. Upstream fixes should be evaluated and ported, but the fork has its own bug fixes not in upstream.
- The `docs/` directory contains design specs — historical reference only, not authoritative if they conflict with actual files.
