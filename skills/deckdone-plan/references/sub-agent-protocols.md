# Sub-Agent Delegation Protocols for deckdone-plan

Guide for delegating context-heavy steps to sub-agents via the Task tool during the planning phase. The main agent handles user interaction; sub-agents handle large file generation.

---

## General Rules

1. **Delegate generation, keep interaction** — Sub-agents produce files. The main agent handles all Q&A, review loops, and user confirmations.
2. **Input via prompt** — Sub-agents start fresh. Pass file paths to read and all relevant context in the prompt.
3. **Output via files** — Sub-agents write results to the project directory. The main agent confirms files exist, never reads full content.
4. **Sub-agent type** — Use `subagent_type: "general"` for all generation tasks.
5. **Review loop stays in main agent** — After sub-agent generates wireframes.html, the main agent edits it directly during the review loop (targeted edits are small).

---

## Step 5: Wireframe Generation + Content Plan Export

Step 5 has two delegation points:

### 5a. Wireframe HTML Generation

Delegate the initial generation of `wireframes.html` to a single sub-agent.

**Main Agent Responsibilities:**
1. Read `brief.md`, `outline.md`, `layout-system.md` in main agent (needed for user discussion context).
2. Delegate full `wireframes.html` generation to one sub-agent.
3. Tell user the file path, ask them to open in browser.
4. Handle the review loop directly (small targeted edits to wireframes.html).

**Prompt Template:**

```
You are generating a low-fidelity HTML wireframe file for a presentation. Generate a single HTML file containing ALL slides.

## Files to Read (READ ALL BEFORE GENERATING)

1. `references/wireframe-guide.md` — HTML structure, zone rendering, chart placeholders, auto-refresh script, layout templates per page type (MANDATORY — follow every rule)
2. `references/density-presets.md` — content capacity limits for the density level
3. `references/layout-types.md` — per-type zone templates and ratios
4. `brief.md` — presentation title, density level, key message
5. `outline.md` — section structure, page count, per-page purpose
6. `layout-system.md` — page type assignment per slide

## Presentation Context

- Title: [from brief.md]
- Total pages: [N]
- Density level: [from brief.md]
- Key Message: [from brief.md]

## Generation Rules

1. Single HTML file: `wireframes.html` in the project directory.
2. Each slide = one 16:9 proportional div with gray-bordered zones.
3. Every zone contains REAL content text (never "Lorem ipsum", "placeholder", or "TBD").
4. Zone labels show: [type] (weight) — e.g., [title] (primary).
5. Chart zones include structured <dl> data (see wireframe-guide.md Chart Placeholder section).
6. Include auto-refresh script (3-second interval, scroll position preservation).
7. Include thumbnail navigation bar at the bottom.
8. No visual styling — gray borders, black text, no colors, no decorative elements.
9. Text volume must match the density level from brief.md.

## Output

Write `wireframes.html` to the project directory. Return: total slide count and file path.
```

### 5b. Content Plan + Layout Skeleton Export

After the user confirms all wireframes, delegate the markdown export to a sub-agent.

**Main Agent Responsibilities:**
1. Receive user confirmation on wireframes.
2. Delegate export of `content-plan.md` and `layout-skeleton.md` to one sub-agent.
3. Run validation: `python scripts/validate-content-plan.py content-plan.md`
4. Confirm validation passes.

**Prompt Template:**

```
You are exporting two markdown files from a confirmed HTML wireframe. Read the wireframe and reference files, then produce content-plan.md and layout-skeleton.md.

## Files to Read (READ ALL)

1. `wireframes.html` — the confirmed wireframe with all slide content
2. `brief.md` — density level, key message
3. `outline.md` — section structure
4. `layout-system.md` — page type assignments
5. `references/layout-skeleton-format.md` — format specification for layout-skeleton.md
6. `references/density-presets.md` — Max Length values per density level

## content-plan.md Format

Each slide needs:

```markdown
## P## — [Title]

**Page Type:** [type]
**Total Zones:** [N]
**Visual Narrative Path:** [path description]

### Zone 1
- Type: [title|subtitle|body|bullet-list|chart-area|...]
- Content: [exact text from wireframe — must be non-empty]
- Max Length: [value from density presets]
- Visual Weight: [primary|secondary|auxiliary]

### Zone 2
...

### Chart Zone (if applicable)
- Chart Type: [Line|Bar|Pie|...]
- Chart Title: [title]
- X-Axis: [description]
- Y-Axis: [description]
- Data Points: [structured data from <dl>]
- Key Insight: [one sentence]

### Acceptance Criteria
- [ ] Content matches wireframe
- [ ] Zone count matches layout-system.md
- [ ] Text within density limits
- [ ] Chart data complete (if applicable)
```

For zones containing statistics, quantified data, third-party claims, or direct quotes, add:
- Source: [attribution from materials/00-index.md Data Points table]

## layout-skeleton.md Format

Follow the specification in `references/layout-skeleton-format.md`:
- Overview table (Page, Title, Type, Zones)
- Per-page zone layout summary

## Output

Write `content-plan.md` and `layout-skeleton.md` to the project directory. Return: file paths and page count.
```

---

## Context Savings Estimate

| Step | Without Sub-Agent | With Sub-Agent | Savings |
|------|------------------|----------------|---------|
| 5a wireframe HTML | 1500-3000 lines HTML in main context | ~50 lines (prompt + result) | ~98% |
| 5b markdown export | 500-1000 lines generated markdown | ~50 lines (prompt + result) | ~95% |
| **Total plan Phase 2** | **~3000 lines** | **~100 lines** | **~97%** |

---

## Review Loop Handling

After the sub-agent generates `wireframes.html`, the main agent handles the review loop directly. This is acceptable because:

1. **Edits are targeted** — User says "change the title on page 5" → small edit, ~5 lines of context.
2. **No full file reads needed** — Use search/grep to locate the edit target, then use the Edit tool.
3. **Auto-refresh handles display** — The browser reloads automatically, the main agent doesn't need to see the visual result.

If the user requests a major restructuring (add/remove pages, change 5+ pages), delegate the full regeneration to a new sub-agent with updated instructions.
