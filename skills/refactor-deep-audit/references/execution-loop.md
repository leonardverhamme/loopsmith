# Execution Loop

Use this when the task is to work through an existing refactor checklist until it is done. In the default bare-invocation workflow, this loop must start immediately after the audit refresh.

## Rules

1. Open the checklist file and re-read it before starting a new batch.
2. Pick a coherent batch of unchecked items by subsystem or migration wave.
3. Implement the refactor.
4. Run the smallest correct validation for that batch.
5. Mark items `- [x]` only after implementation and validation.
6. Update the status counts in the checklist file.
7. Re-open the checklist file and continue with the next batch.
8. Repeat until there are no unchecked items left or a real blocker prevents further progress.

## Validation Standard

- Prefer the repo's actual tests, typechecks, builds, and targeted smoke checks.
- Preserve behavior unless the user explicitly requested behavior change.
- If only partial validation is possible, state that explicitly in the checklist note or final report.

## Blockers

- Leave blocked work as `- [ ]`.
- Append a short blocker note on the same item or the next line.
- Continue with remaining work unless the blocker prevents further progress.

## Anti-Patterns

- Do not stop after the audit refresh unless the user explicitly asked for audit-only behavior.
- Do not mark boxes complete speculatively.
- Do not trust prior chat messages over the current checklist file.
- Do not mix feature redesign into a structural refactor wave and still call it complete.
