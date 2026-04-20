# Refactor Phases

Broad refactors should be run as waves, not as a single undifferentiated rewrite.

## Recommended Phases

1. Map the current structure and target boundary.
2. Add or confirm safety nets.
3. Introduce adapters, facades, or compatibility shims if needed.
4. Migrate callers or consumers in batches.
5. Remove dead paths and temporary glue.
6. Update docs, architecture notes, and ADRs if the boundary changed.
7. Run final closeout validation.

## Why Waves Matter

- the blast radius stays understandable
- failures are easier to localize
- rollback or course correction stays possible
- the repo is not left in a long-lived broken intermediate state

## Good Wave Boundaries

- one package or module group
- one API surface
- one dependency direction fix
- one UI shell or feature slice
- one migration from old path to new path

