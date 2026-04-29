# Diagram Type → SmartArt Template

Diagram pages use native PowerPoint SmartArt via template injection. 150+ templates are available in `templates/smartart/`.

## How It Works

1. Plan phase assigns `Page Type: Content-Diagram` and `Relationship Type`
2. Build phase AI consults `references/smartart-catalog.md` to select the best SmartArt template
3. `scripts/smartart_inject.py` injects the template into the PPTX
4. WPS/PowerPoint renders the SmartArt natively

## Template Selection

The AI chooses from 150+ SmartArt templates organized by 8 categories:
- **List** (28 types) — bullet enumerations, feature lists
- **Process** (37 types) — sequential steps, workflows
- **Cycle** (9 types) — iterative processes, loops
- **Hierarchy** (15 types) — org charts, tree structures
- **Relationship** (29 types) — venn, gear, radial, equation
- **Matrix** (3 types) — 2D grids, prioritization
- **Pyramid** (4 types) — layered structures, proportional
- **Picture** (25 types) — image-accented layouts

See `references/smartart-catalog.md` for the complete indexed catalog.
