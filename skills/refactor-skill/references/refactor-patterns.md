# Common Refactor Patterns

Use the smallest move that improves the design enough.

## Preferred Moves

- Extract helper or utility when a block has one clear purpose.
- Extract service or adapter when IO or side effects blur a business flow.
- Extract component or subview when a UI file mixes layout and orchestration.
- Replace boolean soup with a named function, enum, or object.
- Move logic closer to the module that owns the data or responsibility.
- Rename types, variables, and functions when intent is the real problem.
- Introduce a thin compatibility wrapper when changing callers all at once is risky.

## File and Module Cleanup

- Split oversized files by responsibility, not by arbitrary line count.
- Keep public entrypoints thin and predictable.
- Prefer one obvious ownership location for a behavior.
- Remove dead branches only after checking call sites and tests.

## Dependency Cleanup

- Prefer one-way dependencies across layers.
- Move shared code down into a neutral layer instead of creating cycles.
- If a cycle exists, extract the shared contract instead of keeping two modules tightly coupled.

## Validation Habit

After each significant move:

- run the narrowest useful test command
- run typecheck or lint if the repo treats them as quality gates
- inspect imports, exports, and call sites for accidental surface changes

