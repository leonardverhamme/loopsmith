# Migration Patterns

Use these when the refactor is closer to a migration than a local cleanup.

## Safer Migration Moves

- Introduce a thin wrapper around the old API, then migrate callers.
- Run old and new implementations behind one interface during transition.
- Deprecate loudly in code and docs before removal.
- Migrate read paths before write paths when that lowers risk.
- Keep data and contract shape adapters explicit rather than hidden.

## Avoid

- removing the old path before consumers are migrated
- changing contracts and call sites in one opaque batch
- mixing structural migration with unrelated cleanup

## When to Stop

If the migration needs new product behavior, this is no longer just refactoring. Split that work into a separate task.

