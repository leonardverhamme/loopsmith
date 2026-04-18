# Checklist Format

When this skill needs a durable state file, keep it compact and execution-oriented.

## Good Structure

```md
# Refactor Plan

## Goal

Short statement of the structural outcome and invariant.

## Waves

- [ ] Wave 1: safety net and seams
- [ ] Wave 2: migrate callers
- [ ] Wave 3: remove compatibility path
- [ ] Wave 4: docs and closeout

## Validation

- command 1
- command 2

## Risks

- risk and mitigation
```

## Rules

- Keep the file short.
- Track waves, not every tiny edit.
- Only mark a box complete after the wave is implemented and verified.
- Reopen a box if later validation shows the wave is not actually done.
