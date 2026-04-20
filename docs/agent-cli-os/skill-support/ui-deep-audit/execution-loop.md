# Execution Loop

Use this when the task is to work through an existing checklist file until everything is done. In the default bare-invocation workflow, this loop must start immediately after the audit refresh.

## Rules

1. Open the checklist file and re-read it before starting a new batch.
2. Pick a coherent batch of unchecked items by page or subsystem.
3. Implement the fixes.
4. Run the smallest correct validation for that batch.
5. Mark items `- [x]` only after implementation and validation.
6. Update the status counts in the checklist file.
7. Re-open the checklist file and continue with the next batch.
8. Repeat until there are no unchecked items left or a real blocker prevents further progress.

## Validation Standard

- Prefer repo lint, typecheck, tests, and browser checks when available.
- If only a manual visual verification is possible, say so explicitly in the checklist note or final report.
- Do not claim an item is complete if the relevant page was not checked after the change.

## Blockers

- Leave blocked work as `- [ ]`.
- Append a short blocker note on the same item or the next line.
- Continue with the remaining items instead of stopping the whole run unless the blocker prevents further progress.

## Anti-Patterns

- Do not mark boxes complete speculatively.
- Do not batch too many unrelated fixes before validating.
- Do not trust prior chat messages over the current checklist file.
- Do not say `ready` just because a large batch shipped; only the checklist state decides that.
- Do not stop after the audit refresh unless the user explicitly asked for audit-only behavior.

