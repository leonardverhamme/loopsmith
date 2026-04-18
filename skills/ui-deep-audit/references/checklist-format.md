# Checklist Format

The checklist file is the canonical queue. Keep it readable, resumable, and easy to hand off to follow-up agents.

## Default Path

- Default to `docs/ui-deep-audit-checklist.md`
- Use a user-specified path when provided

## Recommended Structure

```md
# UI Deep Audit Checklist

## Status
- Last updated: 2026-04-18
- Pages reviewed: 0
- Total issues: 0
- Completed: 0
- Remaining: 0

## App Map
- [x] Shell and navigation
- [ ] Overview
- [ ] Orders
- [ ] Customers

## Findings

### /overview

#### Header and summary
- [ ] [High] Reduce header height and remove duplicate descriptive copy.
  Why: The header pushes the primary table and metrics too far below the fold.
  Fix target: `app/overview/page.tsx`
  Validate: Visual check on desktop and narrow viewport.

#### Charts
- [ ] [Medium] Replace the donut with a compact horizontal bar chart.
  Why: The category comparison is hard to scan and the legend dominates the card.
  Fix target: `components/overview/revenue-breakdown.tsx`
  Validate: Visual check and legend readability.
```

## Item Rules

- Group by page first, then by section or component.
- Use `- [ ]` for unresolved or blocked work.
- Use `- [x]` only for work that is implemented and validated.
- Keep every finding concrete and fixable.
- Include severity, why it matters, target files or areas, and validation method.
- Prefer one issue per checkbox rather than giant combined items.
