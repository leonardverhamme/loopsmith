# Context Refresh

Use this reference after structural changes so repo context does not drift.

## Refresh Triggers

- new app or service entrypoint
- major folder move
- new verification command
- changed CI entrypoints
- changed architecture boundaries
- recurring confusion in recent tasks

## Refresh Loop

1. Find the source-of-truth files affected by the change.
2. Update `AGENTS.md` only if durable operating rules changed.
3. Update architecture or repo-map docs if structure changed.
4. Remove duplicated or stale context elsewhere.
5. State what remains implicit and should still be documented later.
