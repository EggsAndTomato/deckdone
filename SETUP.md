# DeckDone Setup Guide

## Prerequisites
- Node.js 18+
- Python 3.10+
- opencode, Claude Code, or compatible AI coding tool

## Before You Begin

Determine your setup:

1. **Install scope** — Do you want DeckDone available for all projects (global) or only the current project (project-level)?
2. **OS** — The paths and commands differ between Linux/macOS and Windows.

| | Global (all projects) | Project-level (current only) |
|---|---|---|
| **Linux/macOS** | `~/.config/opencode/skills/` | `<project-root>/.opencode/skills/` |
| **Windows** | `C:\Users\<you>\.config\opencode\skills\` | `<project-root>\.opencode\skills\` |

> The steps below use the placeholder `SKILLS_DIR` to represent the chosen path. Replace it with your actual directory.

---

## Step 1: Install DeckDone Skill

The skill is in the `skills/deckdone/` subdirectory of this repo. Clone the repo, then copy the skill folder into your SKILLS_DIR.

```bash
# 1. Clone this repo to a temporary location
git clone https://github.com/anomalyco/deckdone.git /tmp/deckdone

# 2. Copy the skill into SKILLS_DIR
# Linux / macOS (global)
mkdir -p ~/.config/opencode/skills
cp -r /tmp/deckdone/skills/deckdone ~/.config/opencode/skills/deckdone

# Linux / macOS (project-level)
mkdir -p .opencode/skills
cp -r /tmp/deckdone/skills/deckdone .opencode/skills/deckdone

# Windows — global (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\opencode\skills"
Copy-Item -Recurse C:\Temp\deckdone\skills\deckdone "$env:USERPROFILE\.config\opencode\skills\deckdone"

# Windows — project-level (PowerShell)
New-Item -ItemType Directory -Force -Path .opencode\skills
Copy-Item -Recurse C:\Temp\deckdone\skills\deckdone .opencode\skills\deckdone
```

---

## Step 2: Install Required Dependencies

### Anthropic skills (required: pptx)

The pptx skill is from the [anthropics/skills](https://github.com/anthropics/skills) monorepo (`skills/pptx` subdirectory).

```bash
# 1. Clone the Anthropic skills repo
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills

# 2. Copy pptx skill into SKILLS_DIR
# Linux / macOS (global)
cp -r /tmp/anthropic-skills/skills/pptx ~/.config/opencode/skills/pptx

# Linux / macOS (project-level)
cp -r /tmp/anthropic-skills/skills/pptx .opencode/skills/pptx

# Windows — global (PowerShell)
Copy-Item -Recurse C:\Temp\anthropic-skills\skills\pptx "$env:USERPROFILE\.config\opencode\skills\pptx"

# Windows — project-level (PowerShell)
Copy-Item -Recurse C:\Temp\anthropic-skills\skills\pptx .opencode\skills\pptx
```

### Runtime dependencies (required)

These npm packages install globally regardless of skill install scope.

```bash
npm install -g pptxgenjs playwright sharp react-icons
npx playwright install chromium
```

---

## Step 3 (Optional): Install Optional Skill Dependencies

Only install the ones you need. Each provides automatic file extraction — without it, the user will be asked to paste content as text.

These skills are also from the [anthropics/skills](https://github.com/anthropics/skills) monorepo. If you already cloned it in Step 2, skip the clone command.

```bash
# If not already cloned:
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
```

### PDF support
```bash
# Linux / macOS
cp -r /tmp/anthropic-skills/skills/pdf <SKILLS_DIR>/pdf
# Windows (PowerShell)
Copy-Item -Recurse C:\Temp\anthropic-skills\skills\pdf <SKILLS_DIR>\pdf
pip install markitdown
```

### Word document support
```bash
# Linux / macOS
cp -r /tmp/anthropic-skills/skills/docx <SKILLS_DIR>/docx
# Windows (PowerShell)
Copy-Item -Recurse C:\Temp\anthropic-skills\skills\docx <SKILLS_DIR>\docx
```

### Spreadsheet support
```bash
# Linux / macOS
cp -r /tmp/anthropic-skills/skills/xlsx <SKILLS_DIR>/xlsx
# Windows (PowerShell)
Copy-Item -Recurse C:\Temp\anthropic-skills\skills\xlsx <SKILLS_DIR>\xlsx
```

### Extended style presets
```bash
# Linux / macOS
cp -r /tmp/anthropic-skills/skills/theme-factory <SKILLS_DIR>/theme-factory
# Windows (PowerShell)
Copy-Item -Recurse C:\Temp\anthropic-skills\skills\theme-factory <SKILLS_DIR>\theme-factory
```

---

## Verification

Run the validation scripts to verify installation. Adjust the path to match your install scope and OS.

```bash
# Linux / macOS (global)
python ~/.config/opencode/skills/deckdone/scripts/validate-content-plan.py --help

# Linux / macOS (project-level)
python .opencode/skills/deckdone/scripts/validate-content-plan.py --help

# Windows — global (PowerShell)
python "$env:USERPROFILE\.config\opencode\skills\deckdone\scripts\validate-content-plan.py" --help

# Windows — project-level (PowerShell)
python .opencode\skills\deckdone\scripts\validate-content-plan.py --help
```

All commands should print usage information without errors.

---

## Quick Start

Once installed, start a new conversation with your AI tool and say:

"Create a presentation using DeckDone about [your topic]"

The AI will load the DeckDone skill and begin the phased workflow.
