# Prompt Shortcuts

Use these short prompts in the Codex app instead of pasting a giant workflow each time.

## Bare Invocation

```text
$ui-deep-audit
```

Behavior:
- Refresh or create `docs/ui-deep-audit-checklist.md` from a full audit
- Immediately execute unchecked items in the same run
- Keep working until complete or blocked
- Checklist fully checked: validate and only then reply `ready`

## Fresh Audit

```text
$ui-deep-audit
Audit the full app into docs/ui-deep-audit-checklist.md. Go page by page, use checkboxes, and do not implement fixes yet.
```

## Parallel Audit

```text
$ui-deep-audit
Audit the full app into docs/ui-deep-audit-checklist.md. Use subagents in parallel by audit zone, then merge and deduplicate the checklist.
```

## Execute Checklist

```text
$ui-deep-audit
Open docs/ui-deep-audit-checklist.md and complete every unchecked item. Mark boxes done only after implementation and validation. Reply only when the checklist state is accurate.
```

## Finish and Close Out

```text
$ui-deep-audit
Re-open docs/ui-deep-audit-checklist.md, verify that no unchecked items remain, and only reply `ready` if the checklist is truly complete and validated.
```

