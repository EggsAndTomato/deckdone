# State File Templates

Templates for deckdone-plan workflow state tracking.

---

## deckdone-state.md

```markdown
# DeckDone-Plan Progress State

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
# DeckDone-Plan Execution Trace

## Session 1: [date] [start time]–[end time]
### Step [N] → [name]
- Iterations: [count]
- User decisions: [list key decisions]
- Adjustments: [what was changed]
- Issues encountered: [problems and resolutions]
- Output: [file paths] status
```

---

## harness-improvements.md

```markdown
# Harness Improvement Log

## Improvement #[N]
- Date: [date]
- Trigger: [what went wrong, on which step]
- Root Cause: [harness gap analysis]
- Fix: [what was changed in the harness]
- Updated Files: [which reference files were modified]
```
