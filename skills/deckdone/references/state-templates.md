# State File Templates

Templates for DeckDone workflow state tracking files.

---

## deckdone-state.md

```markdown
# DeckDone Progress State

## Status
- Phase: [current phase name]
- Current Step: [step number and name]
- Last Activity: [datetime]
- Progress: [e.g., "Section 2/4 layout skeletons confirmed"]

## Completed Steps
- [x] Phase 1, Step 1: Brief confirmed ([date])
- [x] Phase 1, Step 2: Materials collected ([date])
...

## Key Decisions
- Framework: [chosen framework + why]
- Style: [chosen style + palette]
- [any other critical decisions]

## Deliverable Status
- brief.md [confirmed | in progress | not started]
- materials/ [status]
- outline.md [status]
- layout-system.md [status]
- style-guide.md [status]
- layout-skeleton.md [status]
- content-plan.md [status]
- test-slides/ [status]
- output.pptx [status]
- final.pptx [status]
- presentation-guide.md [status]

## Context Summary
[Under 500 words. Must include: presentation purpose, key message,
 audience profile, scale, chosen framework, style direction.
 Enough for a fresh AI instance to understand the project.]

## Pending Items
- [unresolved questions]
- [deferred decisions]
```

---

## deckdone-trace.md

```markdown
# DeckDone Execution Trace

## Session 1: [date] [start time]–[end time]
### Step [N] → [name]
- Iterations: [count] (describe rounds of changes)
- User decisions: [list key decisions made by user]
- Adjustments: [what was changed from initial output]
- Issues encountered: [list problems and resolutions]
- Output: [file paths] status

### Step [N+1] → [name]
...
```

---

## harness-improvements.md

```markdown
# Harness Improvement Log

## Improvement #[N]
- Date: [date]
- Trigger: [what went wrong, on which slide/step]
- Root Cause: [why it happened — harness gap analysis]
- Fix: [what was changed in the harness]
- Updated Files: [which reference files or templates were modified]
```
