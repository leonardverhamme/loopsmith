# Risk Review

Run this review before making the first broad change.

## Structural Risk Questions

- Which public contracts could break?
- Which modules have the most callers?
- Where are the weak or missing tests?
- Which files are already volatile or under active change?
- Which temporary compatibility layers will be needed?

## Operational Risk Questions

- Which commands prove the subsystem still works?
- Is there a safe batch size for migrations?
- Can the work be paused between waves without leaving the repo unusable?

## Escalation Signals

Slow down or rescope if:

- one wave grows to many unrelated concerns
- the validation path is unclear
- behavior changes are being mixed into the migration
- the refactor starts touching ownership boundaries that need an ADR
