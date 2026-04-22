# DeckDone

English | **[中文](README.md)**

A structured workflow skill for creating large, complex presentations (15–40 slides) from scratch. Built for AI coding tools like [opencode](https://opencode.ai) and Claude Code.

## Core Idea

Separate "what to say" from "how it looks":

- **Plan phase** (Steps 1-5): Content and structure only. The final step uses live HTML wireframes with browser auto-refresh so you can review and discuss content in real-time, then exports a content contract.
- **Build phase** (Steps 6-8): Visuals only. After style selection, all pages are generated in batch with locked design tokens to ensure consistency.

The two phases are connected by markdown files — Build makes zero creative decisions, mechanically executing Plan's output.

## Who It's For

- **Information-dense decks** — business plans, product roadmaps, R&D strategy, architecture reviews
- **Visual storytelling** format — slides as visual aids for narration
- Anyone tired of AI-generated decks that look like "title + 3 bullets" on every page

## Workflow

```
User: "Create a DeckDone presentation about our FY26 R&D plan"
         │
  Plan · Step 1: Brief → Purpose? Audience? Key message?
  Plan · Step 2: Materials → Collect source docs, extract data
  Plan · Step 3: Outline → Narrative skeleton, estimate pages
         │  ✓ User confirms
  Plan · Step 4: Page types → Assign layout to each page
  Plan · Step 5: Content wireframes → Live browser review, confirm per page
         │  ✓ User confirms
  Build · Step 6: Style + test → Choose palette & fonts, generate test pages
  Build · Step 7: Batch generation → Sequential SVG generation, quality review
  Build · Step 8: Export → final.pptx + presentation guide
```

Every step has a gate — the AI won't proceed until you confirm. Need changes after completion? Revision Mode supports per-page edits, global color changes, and page add/remove.

## Installation

```bash
git clone https://github.com/anomalyco/deckdone.git /tmp/deckdone
mkdir -p ~/.config/opencode/skills
cp -r /tmp/deckdone/skills/deckdone-plan ~/.config/opencode/skills/
cp -r /tmp/deckdone/skills/deckdone-build ~/.config/opencode/skills/
pip install python-pptx lxml
```

For extracting content from PDF/DOCX/XLSX sources, additionally install the pdf, docx, and xlsx skills from [anthropics/skills](https://github.com/anthropics/skills).

## Quick Start

Once installed, start a new conversation:

> Create a DeckDone presentation about our FY26 R&D plan

The AI will walk you through purpose, audience, and key message step by step.

## Resuming Work

If a conversation ends mid-project:

> Continue my DeckDone presentation

The AI reads the state file and picks up exactly where it left off.

## Dependencies

| Dependency | Required | Purpose |
|-----------|----------|---------|
| python-pptx | Yes | PPTX generation |
| lxml | Yes | SVG parsing |
| pdf skill | No | PDF source extraction |
| docx skill | No | Word source extraction |
| xlsx skill | No | Spreadsheet data extraction |

## License

MIT
