# AGENTS.md — DeckDone Repository

## Repo Structure

This is a **skill repository**, not a traditional code project. The skill lives in `skills/deckdone/` — a self-contained opencode skill directory. The repo root holds project-level documentation (README, SETUP.md, LICENSE, design docs).

```
<repo root>/            ← git root, README/SETUP/LICENSE live here
skills/deckdone/        ← the skill itself (SKILL.md is the entrypoint)
  references/           ← decision-support docs read by the AI at runtime
  scripts/              ← validation scripts (Python, stdlib only)
```

## Skill Architecture

- `skills/deckdone/SKILL.md` — the skill entrypoint. A ~575-line workflow orchestration file that AI agents read and follow. It does NOT contain PPTX generation logic itself — it delegates to the `pptx` skill (from `anthropics/skills`).
- `references/*.md` — reference data the AI reads at specific workflow steps (frameworks, page types, style presets, quality checklists).
- `scripts/validate-*.py` — mechanical validators run after specific workflow steps. Python stdlib only (no third-party deps).

## Validation Scripts

```bash
# Validate content-plan.md structure (run after workflow Step 7)
python skills/deckdone/scripts/validate-content-plan.py <content-plan.md>

# Validate HTML slide files for html2pptx compatibility (run after Steps 9-10)
python skills/deckdone/scripts/validate-html-slides.py <wireframes-directory/>
```

Both exit 0 on pass, 1 on any failure. No pip dependencies.

## Key Conventions

- **Language**: SKILL.md and all reference files are in English. The AI communicates with users in their preferred language.
- **html2pptx constraints**: HTML slides must use `width: 720pt; height: 405pt` on body, all text inside `<p>`/`<h1>`-`<h6>`/`<ul>`/`<ol>` tags, no CSS gradients, web-safe fonts only. The validate-html-slides.py script enforces these.
- **Valid page types**: Cover, Agenda, Section Divider, Content-Text, Content-TwoCol, Data-Chart, Quote, Timeline, Comparison, Closing, Composite-Diagram, Pipeline-Flow. Defined in validate-content-plan.py and references/layout-patterns.md.
- **Content plan fields**: Each zone needs `- Type:`, `- Content:` (non-empty), `- Max Length:`, `- Visual Weight:` (primary|secondary|auxiliary). The list-item format (`- Field: value`) must be used — the validator matches this pattern.

## Dependencies

The skill depends on the `pptx` skill from `anthropics/skills` (not this repo). Optional skills (pdf, docx, xlsx, theme-factory) are also from `anthropics/skills`. See `SETUP.md` for install commands.

## When Editing This Repo

- Do not modify SKILL.md line counts beyond ~600 lines. If content grows, move it to a new reference file in `references/` and add a cross-reference in SKILL.md.
- The harness improvement principle: when a generated slide has quality issues, fix the harness (reference files, validation rules), not just the individual slide. See `references/quality-checklist.md`.
- The `docs/` directory contains the original design spec and implementation plan — historical reference only, not authoritative if they conflict with the actual files.
