# Prompt Shortcuts

## Bare Invocation

```text
$docs-deep-audit
```

Behavior:

- Refresh or create `docs/docs-deep-audit-checklist.md` from a full documentation audit
- Immediately execute unchecked items in the same run
- Keep working until complete or blocked
- Only then validate and potentially reply `ready`

## Audit Only

```text
$docs-deep-audit
Audit the repo's durable docs into docs/docs-deep-audit-checklist.md. Use checkboxes and do not implement fixes yet.
```

