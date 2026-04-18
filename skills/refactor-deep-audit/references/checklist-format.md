# Checklist Format

Use a compact, execution-oriented checklist.

## Good Structure

```md
# Refactor Deep Audit Checklist

## Status

- Unchecked: 11
- Checked: 0

## API Layer

- [ ] Extract request validation from the route handlers into one shared module
- [ ] Remove duplicated pagination logic across three endpoints

## UI Shell

- [ ] Split the dashboard page into route orchestration and dedicated feature sections
```

## Rules

- Group by subsystem, then structural issue or wave.
- Keep each item fixable.
- Only mark an item complete after the refactor and validation are done.
