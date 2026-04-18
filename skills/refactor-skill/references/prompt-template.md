# Prompt Template

Use these short forms when the user needs help phrasing a refactor task.

## General

```text
$refactor-skill
Refactor <files or subsystem> in small verified steps. Preserve behavior, keep the diff structural, and run the relevant checks as you go.
```

## With Invariant

```text
$refactor-skill
Refactor <target area> without changing <user-visible or API-visible behavior>. Add the minimum safety net needed, then keep iterating until the relevant checks are green.
```
