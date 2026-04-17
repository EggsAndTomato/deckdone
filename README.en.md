# DeckDone

English | **[中文](README.md)**

A structured workflow skill for creating large, complex presentations (15–40 slides) from scratch. Built for AI coding tools like [opencode](https://opencode.ai) and Claude Code.

## What It Does

DeckDone orchestrates the full presentation creation process through a **4-phase, gate-controlled workflow**:

| Phase | Name | What Happens |
|-------|------|-------------|
| 1 — Discovery | Deep interaction | Define purpose, audience, narrative framework; collect materials; build outline |
| 2 — Design | Page-by-page confirmation | Assign page types, choose visual style, generate HTML wireframes |
| 3 — Content | Lightweight confirmation | Write exact content for every visual zone on every page |
| 4 — Implementation | Batch execution | Test generation, batch PPTX production, final quality review |

Every phase ends with a **gate** — the user confirms deliverables before proceeding. No phase starts without the previous one being locked.

### Who It's For

- People building **information-dense decks** — business plans, product roadmaps, R&D strategy, architecture reviews
- Presenters who use the **"visual storytelling"** format (看图说话 — the slides are visual aids for narration)
- Anyone tired of AI-generated decks that look like "title + 3 bullets" on every page

### Design Principles

- **Content-first** — Decide what to say before deciding how it looks
- **Density-aware** — Handles 20–50+ text elements per slide, not simple bullet lists
- **Graceful degradation** — Works with minimal dependencies; optional skills (PDF, DOCX, XLSX) enhance the experience
- **Cross-conversation continuity** — Resume work across multiple AI sessions via state files

## File Structure

```
deckdone/                              ← repository root
├── README.md                          # Documentation (Chinese)
├── README.en.md                       # Documentation (English)
├── SETUP.md                           # Installation guide (AI-readable)
├── LICENSE                            # MIT
├── docs/                              # Design documents
└── skills/
    └── deckdone/                      # The skill itself
        ├── SKILL.md                   # Core workflow (~575 lines)
        ├── references/
        │   ├── layout-patterns.md     # 12+ page types with HTML skeletons
        │   ├── narrative-frameworks.md # 6 narrative frameworks + selection matrix
        │   ├── audience-analysis.md   # Audience profiling methodology
        │   ├── style-presets.md       # 18 visual style presets
        │   ├── html-wireframe-guide.md # Wireframe generation standards
        │   └── quality-checklist.md   # Per-step validation checklists
        └── scripts/
            ├── validate-content-plan.py # Content plan structural validator
            └── validate-html-slides.py  # HTML slide html2pptx validator
```

## Installation

### Option A: Let Your AI Tool Install It (Recommended)

DeckDone includes `SETUP.md` — a machine-readable installation guide. Ask your AI tool to handle the setup:

**Step 1:** Clone the repo first:

```bash
git clone https://github.com/anomalyco/deckdone.git
```

**Step 2:** Start a new conversation in your AI tool and send:

```
Please read deckdone/SETUP.md and follow the instructions to install all required and optional dependencies.
```

The AI will read `SETUP.md`, understand the dependency graph, and execute the installation commands.

### Option B: opencode Project-Level Install (current project only)

To use DeckDone only in the current project without a global install:

```bash
# In the project root
mkdir -p .opencode/skills

# Install DeckDone skill
git clone https://github.com/anomalyco/deckdone.git /tmp/deckdone
cp -r /tmp/deckdone/skills/deckdone .opencode/skills/deckdone

# Install pptx skill (from anthropics/skills)
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
cp -r /tmp/anthropic-skills/skills/pptx .opencode/skills/pptx

# Runtime dependencies still need global install
npm install -g pptxgenjs playwright sharp react-icons
npx playwright install chromium
```

opencode automatically loads skills from `.opencode/skills/` in the project directory — only available for that project.

### Option C: Manual Global Install

**Prerequisites:** Node.js 18+, Python 3.10+, opencode or Claude Code.

```bash
# 1. Install DeckDone skill
git clone https://github.com/anomalyco/deckdone.git /tmp/deckdone
mkdir -p ~/.config/opencode/skills
cp -r /tmp/deckdone/skills/deckdone ~/.config/opencode/skills/deckdone

# 2. Install the required pptx skill (from anthropics/skills)
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
cp -r /tmp/anthropic-skills/skills/pptx ~/.config/opencode/skills/pptx

# 3. Install runtime dependencies
npm install -g pptxgenjs playwright sharp react-icons
npx playwright install chromium
```

**Optional dependencies** (also from [anthropics/skills](https://github.com/anthropics/skills), for PDF/DOCX/XLSX extraction and extended styles):

```bash
# Skip the clone if you already did it in Step 2
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
cp -r /tmp/anthropic-skills/skills/pdf ~/.config/opencode/skills/pdf          # PDF support
pip install markitdown
cp -r /tmp/anthropic-skills/skills/docx ~/.config/opencode/skills/docx        # Word doc support
cp -r /tmp/anthropic-skills/skills/xlsx ~/.config/opencode/skills/xlsx        # Spreadsheet support
cp -r /tmp/anthropic-skills/skills/theme-factory ~/.config/opencode/skills/theme-factory  # Extended presets
```

### Verification

Choose the path matching your install method:

```bash
# Global install
python ~/.config/opencode/skills/deckdone/scripts/validate-content-plan.py --help

# Project-level install
python .opencode/skills/deckdone/scripts/validate-content-plan.py --help
```

The command should print usage information without errors.

## Quick Start

Once installed, start a new conversation and say:

> Create a presentation using DeckDone about [your topic]

The AI will load the skill and begin the phased workflow — starting with questions about purpose, audience, and key message.

## How the Workflow Works

```
User: "Create a DeckDone presentation about our FY26 R&D plan"
         │
    Phase 1: Discovery
    ├── Step 1: Brief → What's the purpose? Who's the audience? Key message?
    ├── Step 2: Materials → Collect source documents, extract key data
    └── Step 3: Outline → Build narrative skeleton, estimate page count
         │  (gate: user confirms outline)
    Phase 2: Design
    ├── Step 4: Page types → Assign layout to each page
    ├── Step 5: Style → Choose visual palette and typography
    └── Step 6: Wireframes → Generate HTML mockups (batch by batch)
         │  (gate: user confirms all wireframes)
    Phase 3: Content
    ├── Step 7: Content plan → Write exact text for every zone
    └── Step 8: Confirmation → User reviews and edits
         │  (gate: user confirms content)
    Phase 4: Implementation
    ├── Step 9: Test slides → Generate one sample per layout type
    ├── Step 10: Batch generation → Produce all slides in chunks
    └── Step 11: Final review → Quality check, deliver final.pptx
```

## Resuming Work

If a conversation ends mid-project, say in a new conversation:

> Continue my DeckDone presentation

The AI reads `deckdone-state.md`, restores context, and picks up exactly where it left off.

## Dependencies

| Dependency | Required | Purpose |
|-----------|----------|---------|
| pptx skill | Yes | PPTX generation engine |
| pptxgenjs | Yes | PowerPoint library |
| playwright | Yes | HTML rendering |
| sharp | Yes | Icon/gradient rasterization |
| pdf skill | No | Extract text from PDFs |
| docx skill | No | Extract text from Word docs |
| xlsx skill | No | Read spreadsheet data |
| theme-factory skill | No | Extended visual presets |

## License

MIT
