# Prompt Shortcuts

Use these short prompts in the Codex app instead of pasting a giant workflow each time.

## Bare Invocation

```text
$test-deep-audit
```

Behavior:
- Refresh `docs/test-deep-audit-checklist.md` from a fresh full repo test audit
- Immediately execute the checklist in the same run
- Keep working until complete or blocked
- Validate and only then reply `ready`

## Fresh Audit

```text
$test-deep-audit
Audit the full repo into docs/test-deep-audit-checklist.md. Use checkboxes and do not implement fixes yet.
```

## Parallel Audit

```text
$test-deep-audit
Audit the full repo into docs/test-deep-audit-checklist.md. Use subagents in parallel by audit zone, then merge and deduplicate the checklist.
```

## Execute Checklist

```text
$test-deep-audit
Open docs/test-deep-audit-checklist.md and complete every unchecked item. Mark boxes done only after implementation and validation. Reply only when the checklist state is accurate.
```

