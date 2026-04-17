---
name: deckdone-style
description: "Visual resource and style enhancement skill for DeckDone. Provides curated icon catalog, illustration sources (unDraw), enhanced style presets, and per-page-type decoration rules. Use alongside the deckdone skill to add icons, illustrations, and refined visual styling to generated presentations."
---

# DeckDone-Style — Visual Resources and Style Enhancement

## Overview

DeckDone-Style provides the visual resource layer for DeckDone presentations. It owns four domains:

1. **Icons** — Curated SVG icon pack (~200 Tabler Icons) with semantic catalog mapping
2. **Illustrations** — Online illustration sources (unDraw) with color customization
3. **Enhanced Presets** — Improved style presets with decoration systems
4. **Decoration Rules** — Per-page-type rules for icon/illustration placement

The parent `deckdone` skill invokes this skill at Steps 6, 7, 9, and 10. This skill makes zero workflow decisions — it provides resources and rules that the workflow consumes.

## Skill Detection

The parent deckdone skill detects deckdone-style by attempting to read this file. If readable, the skill is available. If not, deckdone degrades to its built-in `references/style-presets.md`.

## How to Use

### At Step 6 (Visual Style Direction)

1. Read `references/enhanced-presets.md` instead of deckdone's `references/style-presets.md`
2. Read `references/decoration-guide.md` for per-page-type decoration rules
3. Recommend 2–3 enhanced presets based on purpose + audience
4. Show style previews including icon style, illustration zones, and decoration characteristics
5. User selects a style. Write `style-guide.md` including the preset's icon/decoration sections.

### At Step 7 (Detailed Content Plan)

1. Read `references/icon-catalog.md` for semantic → icon mappings
2. For each zone, assign an icon name from the catalog when the decoration guide mandates one
3. Add to each zone: `- Icon: [name or "None"]`
4. For Cover and Section Divider pages: add `- Illustration: [unDraw slug or "None"]`

### At Step 9/10 (Test/Batch Generation)

1. Run `scripts/fetch-icon.py <icon_name> <output_dir> [--size N]` for each assigned icon
2. Run `scripts/fetch-illustration.py <slug> <accent_color> <output_dir>` for cover/divider illustrations
3. Use `references/layout-templates-decorated.md` instead of deckdone's `references/layout-templates.md`
4. Place icons in HTML per `references/decoration-guide.md` rules

### Validation

After Step 7, run:
```bash
python scripts/validate-style-assets.py <content-plan.md> --catalog references/icon-catalog.md --icons-dir references/icons/
```

## Dependencies

| Dependency | Type | Purpose |
|-----------|------|---------|
| Tabler Icons | Bundled SVGs | ~200 curated icons in `references/icons/` |
| unDraw | Online API | Illustration fetching (requires internet) |
| Sharp (npm global) | Optional | SVG→PNG rasterization for icons/illustrations |

## Graceful Degradation

| Component Missing | Behavior |
|-------------------|----------|
| unDraw unreachable | No illustrations; geometric CSS patterns as fallback |
| Sharp unavailable | SVG icons/illustrations used directly via `<img>` |
| fetch-icon.py fails | AI inlines SVG content directly into HTML |
| Icon not found (local + CDN) | AI uses Unicode text markers (▶ ● ◆ →) |

## Harness Improvement Principle

When a generated slide has icon or illustration quality issues, fix the harness — not the slide. Update:
- `references/icon-catalog.md` if icon choices are semantically wrong
- `references/decoration-guide.md` if placement rules are inappropriate
- `references/enhanced-presets.md` if style/decoration settings produce poor results
- `references/layout-templates-decorated.md` if icon/illustration slots cause layout problems

Log all improvements in deckdone's shared `harness-improvements.md`.
