# Execution Loop

Use this when the task is to work through an existing test checklist until it is done. In the default bare-invocation workflow, this loop must start immediately after the audit refresh.

## Rules

1. Open the checklist file and re-read it before starting a new batch.
2. Pick a coherent batch of unchecked items by subsystem or test layer.
3. Implement the missing tests, fixes, or workflow changes.
4. Run the smallest correct validation for that batch.
5. If a correct test fails, fix product code or setup rather than weakening the test.
6. Mark items `- [x]` only after implementation and validation.
7. Update the status counts in the checklist file.
8. Re-open the checklist file and continue with the next batch.
9. Repeat until there are no unchecked items left or a real blocker prevents further progress.

## Validation Standard

- Prefer the repo's actual test CLI and CI-equivalent commands.
- If a browser flow changed, verify the relevant page or test path.
- If only a manual check was possible, say so explicitly.
- Do not claim an item is complete if the relevant suite or command was not run.

## Blockers

- Leave blocked work as `- [ ]`.
- Append a short blocker note on the same item or the next line.
- Continue with other work unless the blocker prevents further progress.

## Anti-Patterns

- Do not mark boxes complete speculatively.
- Do not batch too many unrelated fixes before validating.
- Do not trust prior chat messages over the current checklist file.
- Do not weaken correct tests just to move the checklist forward.
- Do not say `ready` just because a large batch shipped; only the checklist state decides that.
- Do not stop after the audit refresh unless the user explicitly asked for audit-only behavior.

