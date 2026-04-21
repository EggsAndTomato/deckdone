# State File Templates

Templates for deckdone-build workflow state tracking.

---

## deckdone-state.md

```markdown
# DeckDone-Build Progress State

## Status
- Step: [current step number and name]
- Last Activity: [datetime]
- Progress: [e.g., "Test generation round 2/3"]

## Input Files Status
- content-plan.md [found | missing]
- style-guide.md [found | missing]
- layout-skeleton.md [found | missing]
- outline.md [found | missing]

## Completed Steps
- [x] Step 9: Test SVGs confirmed ([date])
- [x] Step 10: Batch generation complete ([date])
...

## Design Context (locked at Step 10)
- Background: [hex]
- Accent: [hex]
- Text Primary: [hex]
- Text Secondary: [hex]
- Font Family: [family]
- Icon Library: [tabler-filled | tabler-outline]
- Base Font Size: [px]

## Output Status
- svg_output/ [status]
- test-slides/ [status]
- output.pptx [status]
- final.pptx [status]
- presentation-guide.md [status]
```

---

## deckdone-trace.md

```markdown
# DeckDone-Build Execution Trace

## Session 1: [date] [start time]–[end time]
### Step [N] → [name]
- SVGs generated: [count]
- Conversion result: [success/failure details]
- Issues encountered: [problems and resolutions]
- Output: [file paths] status
```

---

## harness-improvements.md

```markdown
# Harness Improvement Log

## Improvement #[N]
- Date: [date]
- Trigger: [what went wrong, on which slide/step]
- Root Cause: [harness gap — svg-constraints? layout-template? validator?]
- Fix: [what was changed]
- Updated Files: [which files were modified]
```
