# Prompt Shortcuts

## Bare Invocation

```text
$cicd-deep-audit
```

Behavior:

- Refresh or create `docs/cicd-deep-audit-checklist.md` from a full automation audit
- Immediately execute unchecked items in the same run
- Keep working until complete or blocked
- Only then validate and potentially reply `ready`

## Audit Only

```text
$cicd-deep-audit
Audit the repo's CI/CD surface into docs/cicd-deep-audit-checklist.md. Use checkboxes and do not implement fixes yet.
```

