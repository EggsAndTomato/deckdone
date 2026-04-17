# Density Presets Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three-level information density control (演讲辅助型 / 演讲详述型 / 阅读型) to the DeckDone skill so users can choose whether their slides are speaker-assisted or reading-type.

**Architecture:** New reference file `density-presets.md` is the single source of truth for content capacity limits and spacing parameters. SKILL.md Step 1 gets a new density question; Steps 7, 9, 10 read the chosen preset. Existing templates and layout definitions are updated to cross-reference the preset instead of hardcoding values.

**Tech Stack:** Markdown reference files only. No code, no scripts.

**Spec:** `docs/superpowers/specs/2026-04-17-density-presets-design.md`

---

## Chunk 1: Core Reference File and SKILL.md Changes

### Task 1: Create `references/density-presets.md`

**Files:**
- Create: `skills/deckdone/references/density-presets.md`

- [ ] **Step 1: Write the density presets reference file**

Create `skills/deckdone/references/density-presets.md` with the following content:

```markdown
# Density Presets — Content Capacity and Layout Spacing

Reference for Step 1 (density selection), Step 7 (content planning), and Steps 9–10 (HTML generation).

---

## Design Philosophy

| Level | ID | Chinese | Philosophy |
|-------|----|---------|------------|
| Presentation | `presentation` | 演讲辅助型 | Keywords + visuals. Audience watches the speaker, not the slides. |
| Detailed Presentation | `detailed-presentation` | 演讲详述型 | Key points with supporting arguments. Speaker adds context. |
| Reading | `reading` | 阅读型 | Self-contained document. Reader understands without a presenter. |

**Selection question:** "Will the audience read this deck on their own, or will you present it live?"

---

## Global Spacing Parameters

Control how much of the 720pt × 405pt slide is available for content.

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Slide padding | 48pt | 36pt | 24pt |
| Line-height (body) | 1.9 | 1.6 | 1.35 |
| Paragraph gap (between bullets/blocks) | 14pt | 8pt | 4pt |
| Min readable body font | 14pt | 12pt | 10pt |

---

## Font Size Decision Rule

The AI selects font sizes at generation time. The rule:

1. Calculate available content area: 720pt × 405pt minus padding from the table above.
2. Choose the largest font size that fits all zone content within the available area.
3. Do not exceed the max content capacity for this page type + density level (see tables below).
4. Do not go below the minimum readable body font for this density level.

No fixed font sizes are stored in this file. The AI has full context (slide dimensions, actual text length, spacing parameters) and can reason about optimal sizing.

---

## Content Capacity per Page Type

### Content-Text

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max bullets | 4 | 6 | 10 |
| Max chars/bullet | 40 | 90 | 200 |
| Sub-bullets | none | 1 level | 2 levels |

### Content-TwoCol

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max bullets/col | 3 | 4 | 6 |
| Max chars/col | 150 | 300 | 600 |

### Agenda

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max items | 6 | 8 | 12 |
| Max chars/item | 30 | 50 | 80 |
| Sub-descriptions | no | optional | yes |

### Timeline

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max events (horizontal) | 4 | 6 | 8 |
| Max chars/description | 20 | 40 | 80 |

### Comparison

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max criteria rows | 4 | 5 | 8 |
| Max chars/cell | 30 | 60 | 120 |

### Composite-Diagram

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max nodes | 8 | 12 | 15 |
| Max chars/node label | 20 | 30 | 50 |
| Node descriptions | no | brief | yes |

### Pipeline-Flow

| Parameter | presentation | detailed-presentation | reading |
|-----------|-------------|----------------------|---------|
| Max stages/row | 4 | 5 | 6 |
| Max chars/stage desc | 15 | 30 | 60 |
| Sub-step rows | no | optional | yes |

### Low-Impact Types

Cover, Section Divider, Quote, Closing, Data-Chart have no capacity differences across density levels. Only global spacing parameters apply.
```

- [ ] **Step 2: Verify file exists and is well-formed**

Run: `python -c "f=open('skills/deckdone/references/density-presets.md'); print(len(f.readlines()), 'lines'); f.close()"`
Expected: ~90-100 lines, no errors.

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/references/density-presets.md
git commit -m "feat: add density-presets.md reference file for information density control"
```

---

### Task 2: Update SKILL.md — Step 1 Brief (density question + template)

**Files:**
- Modify: `skills/deckdone/SKILL.md:148-172`

- [ ] **Step 1: Add density question to Step 1 question list**

In `skills/deckdone/SKILL.md`, find the Step 1 question list (lines 148-156):

```
1. Ask one question at a time. Prefer multiple-choice formats:
   - **Purpose:** Work report / Proposal / Knowledge sharing / Project kickoff / Summary / Other
   - **Key Message:** One sentence — "What should the audience remember after this presentation?"
   - **Audience Profile:**
     - Role level (executive / middle management / team / external client / mixed)
     - Subject familiarity (expert / familiar / general / unfamiliar)
     - Audience tendency (data-driven / story-driven / action-oriented / detail-oriented)
   - **Context:** Formal meeting / Informal sharing / Training / Bidding / Other
   - **Scale:** Estimated page count, time limit
```

Insert after the `- **Scale:**` line:

```
   - **Density:** 演讲辅助型 (presentation) / 演讲详述型 (detailed-presentation) / 阅读型 (reading). Read `references/density-presets.md` for level descriptions. Ask: "Will the audience read this deck on their own, or will you present it live?"
```

- [ ] **Step 2: Update brief.md template to include density fields**

Find the brief.md template (lines 163-172):

```
# Presentation Brief
## Purpose: [purpose]
## Key Message: [one sentence]
## Audience: [profile + tendencies]
## Context: [scenario]
## Scale: [estimated pages, time limit]
## Narrative Framework: [chosen framework + reasoning]
## Methodology: [why this approach works for this audience]
```

Insert after `## Scale:` and before `## Narrative Framework:`:

```
## Density: [presentation | detailed-presentation | reading]
## Density Reasoning: [one sentence]
```

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/SKILL.md
git commit -m "feat: add density selection to Step 1 brief workflow"
```

---

### Task 3: Update SKILL.md — Resume Protocol (density in Context Summary)

**Files:**
- Modify: `skills/deckdone/SKILL.md:121-123`

- [ ] **Step 1: Add density to Context Summary requirements**

Find the State Update Protocol section (around line 122):

```
3. Always include the brief.md Key Message in Context Summary.
```

Insert after that line:

```
4. Always include the brief.md Density level in Context Summary.
```

(Renumber the existing line 4 to 5.)

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone/SKILL.md
git commit -m "feat: ensure density level survives cross-conversation resumption"
```

---

### Task 4: Update SKILL.md — Step 7 Content Plan (density-aware Max Length)

**Files:**
- Modify: `skills/deckdone/SKILL.md:389-393`

- [ ] **Step 1: Add density-aware instruction to Step 7**

Find Step 7 AI Behavior (around line 389):

```
1. Based on confirmed outline + layout-system + layout-skeleton + style-guide, generate a detailed content spec per page.
```

Insert after that line:

```
   Read the density level from `brief.md`. Read the corresponding content capacity limits from `references/density-presets.md`. Use these as Max Length values for each zone instead of the defaults in `layout-types.md`.
```

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone/SKILL.md
git commit -m "feat: make Step 7 content plan density-aware"
```

---

### Task 5: Update SKILL.md — Steps 9/10 (density-aware spacing + dynamic font)

**Files:**
- Modify: `skills/deckdone/SKILL.md:449-465` (Step 9)
- Modify: `skills/deckdone/SKILL.md:479-493` (Step 10)

- [ ] **Step 1: Add density-aware instruction to Step 9**

Find Step 9 AI Behavior item 2 (around line 456):

```
   b. Create HTML file with actual content + confirmed style. Use templates from `references/layout-templates.md`.
```

Insert after that line:

```
      Read the density level from `brief.md` and the corresponding spacing parameters from `references/density-presets.md`. Apply padding, line-height, and gap values. Choose font sizes dynamically based on actual content amount within spacing constraints, respecting the minimum readable font floor.
```

- [ ] **Step 2: Add density-aware instruction to Step 10**

Find Step 10 AI Behavior item 3 (around line 484):

```
   b. Generate HTML files.
```

Insert after that line:

```
      Apply density-level spacing from `references/density-presets.md`. Choose font sizes dynamically per slide based on actual content volume.
```

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/SKILL.md
git commit -m "feat: make Steps 9-10 density-aware with dynamic font sizing"
```

---

## Chunk 2: Reference File and Template Updates

### Task 6: Update `references/layout-types.md` (cross-reference density presets)

**Files:**
- Modify: `skills/deckdone/references/layout-types.md`

- [ ] **Step 1: Replace hardcoded Content density lines with cross-references**

For each page type that has a `**Content density:**` line, replace the hardcoded values with a cross-reference to `density-presets.md`. The exact replacements:

**Cover (line 12):**
```
**Content density:** See `references/density-presets.md`. Title max 60 chars, subtitle max 100 chars, metadata 10–12pt.
```

**Agenda (line 17):**
```
**Content density:** See `references/density-presets.md` for per-level item counts and character limits.
```

**Section Divider (line 22):**
```
**Content density:** See `references/density-presets.md`. Title max 40 chars, description max 120 chars.
```

**Content-Text (line 27):**
```
**Content density:** See `references/density-presets.md` for per-level bullet counts, character limits, and sub-bullet rules.
```

**Content-TwoCol (line 32):**
```
**Content density:** See `references/density-presets.md` for per-level column capacity limits.
```

**Data-Chart (line 37):**
```
**Content density:** See `references/density-presets.md`. 1 chart + 1 interpretation line.
```

**Quote (line 42):**
```
**Content density:** See `references/density-presets.md`. Quote max 180 chars.
```

**Timeline (line 47):**
```
**Content density:** See `references/density-presets.md` for per-level event counts and description limits.
```

**Comparison (line 52):**
```
**Content density:** See `references/density-presets.md` for per-level criteria row counts and cell character limits.
```

**Closing (line 57):**
```
**Content density:** See `references/density-presets.md`. Takeaway max 60 chars, CTA max 120 chars.
```

**Composite-Diagram (line 62):**
```
**Content density:** See `references/density-presets.md` for per-level node counts, label limits, and description rules.
```

**Pipeline-Flow (line 67):**
```
**Content density:** See `references/density-presets.md` for per-level stage counts and description limits.
```

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone/references/layout-types.md
git commit -m "refactor: cross-reference density-presets.md in layout-types.md"
```

---

### Task 7: Update `references/layout-templates.md` (density annotations)

**Files:**
- Modify: `skills/deckdone/references/layout-templates.md`

- [ ] **Step 1: Add density annotations and remove hardcoded content font-sizes**

For each HTML template, make two changes:
1. Add `<!-- DENSITY: padding adjustable -->` and `<!-- DENSITY: line-height adjustable -->` comments on adjustable parameters
2. Remove `font-size` from content-level elements (`<p>`, `<li>`, `<h2>`-`<h6>` within content zones)
3. **Keep** `font-size` on: slide-level `<h1>` (titles), connector arrows `→`, decorative/structural labels

Templates with no content font-size changes needed (structural only): Cover, Section Divider, Quote, Closing. Only add padding/line-height comments.

Affected templates with content font-sizes to remove:

- **Agenda:** remove `font-size: 14pt` from `<ol>` elements
- **Content-Text:** remove `font-size: 14pt` from `<ul>`
- **Content-TwoCol:** remove `font-size: 13pt` from `<p>`, `font-size: 16pt` from `<h2>`
- **Data-Chart:** remove `font-size: 11pt` from interpretation `<p>`
- **Timeline:** remove `font-size: 13pt` from `<h3>`, `font-size: 11pt` from `<p>`
- **Comparison:** remove `font-size: 12pt` from `<p>`, `font-size: 16pt` from `<h2>`
- **Composite-Diagram:** remove `font-size: 11pt` and `font-size: 10pt` from `<p>` inside `.component` and `.nested > div`
- **Pipeline-Flow:** remove `font-size: 12pt` from `.stage h3`, `font-size: 10pt` from `.stage p`
- **Nested-Box (13a):** remove `font-size: 11pt` from subsystem `<p>`, `font-size: 10pt` from component `<p>`
- **Agent Matrix (13b):** remove `font-size: 10pt` and `font-size: 9pt` from grid `<p>` elements
- **Layered Stack (13c):** remove `font-size: 11pt` from layer-tag `<p>`, `font-size: 10pt` from layer-content `<p>`
- **Pipeline/Flow with Connectors (13d):** remove `font-size: 11pt` from stage `<p>`, `font-size: 9pt` from sub-stage `<p>`. **Keep** `font-size: 14pt` on connector arrows

- [ ] **Step 2: Commit**

```bash
git add skills/deckdone/references/layout-templates.md
git commit -m "refactor: add density annotations and remove hardcoded content font-sizes from templates"
```

---

### Task 8: Update `references/quality-checklist.md` (density checks)

**Files:**
- Modify: `skills/deckdone/references/quality-checklist.md`

- [ ] **Step 1: Add density check to Step 1 validation**

Find Step 1 section (around line 25-31). After the last existing check, add:

```
- [ ] **Density level is specified** in brief.md — one of `presentation`, `detailed-presentation`, or `reading` is recorded with a one-sentence reasoning
```

- [ ] **Step 2: Add density compliance check to Step 7 and update existing reference**

Find Step 7 section (around line 74-80). Find the line:

```
- [ ] **No zone exceeds the max character limit** defined in `layout-types.md` for its zone type
```

Replace with:

```
- [ ] **No zone exceeds the max character limit** defined in `density-presets.md` for the chosen density level and page type
```

Then add after the last existing Step 7 check:

```
- [ ] **Zone max lengths comply with density preset** — no zone exceeds the capacity limit for the chosen density level from `references/density-presets.md`
```

- [ ] **Step 3: Commit**

```bash
git add skills/deckdone/references/quality-checklist.md
git commit -m "feat: add density validation checks to quality checklist"
```

---

## Chunk 3: Final Verification

### Task 9: Cross-file consistency check

**Files:** None (verification only)

- [ ] **Step 1: Verify all density references are consistent**

Manually verify:
1. `density-presets.md` exists and contains all page types mentioned in `layout-types.md`
2. `SKILL.md` Step 1 references `density-presets.md`
3. `SKILL.md` Step 7 references `density-presets.md`
4. `SKILL.md` Steps 9-10 reference `density-presets.md`
5. `quality-checklist.md` references `density-presets.md`
6. `layout-types.md` cross-references point to `density-presets.md`
7. No file still references old hardcoded density values as authoritative

Run: `grep -r "Max 6 bullets\|max 90 chars" skills/deckdone/references/layout-types.md`
Expected: No matches (all replaced with cross-references)

Run: `grep -r "density-presets" skills/deckdone/`
Expected: Multiple matches across SKILL.md, layout-types.md, quality-checklist.md

- [ ] **Step 2: Verify SKILL.md line count is within budget**

Run: `python -c "print(sum(1 for _ in open('skills/deckdone/SKILL.md')), 'lines')"`
Expected: No more than 20 lines added compared to pre-edit count (currently 553 lines, so max ~573 lines)

- [ ] **Step 3: Final commit if any fixes were needed**

```bash
git add -A
git commit -m "fix: address consistency issues from density presets integration"
```
