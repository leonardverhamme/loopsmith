# Prompt Shortcuts

## Bare Invocation

```text
$refactor-deep-audit
```

Behavior:

- Refresh or create `docs/refactor-deep-audit-checklist.md` from a broad structural audit
- Immediately execute unchecked items in the same run
- Keep working until complete or blocked
- Only then validate and potentially reply `ready`

## Audit Only

```text
$refactor-deep-audit
Audit this repo for structural cleanup and refactor opportunities into docs/refactor-deep-audit-checklist.md. Use checkboxes and do not implement fixes yet.
```
