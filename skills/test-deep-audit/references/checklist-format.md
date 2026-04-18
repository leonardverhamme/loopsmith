# Checklist Format

The checklist file is the canonical queue. Keep it resumable, easy to hand off, and strict enough that completed boxes mean something.

## Default Path

- Default to `docs/test-deep-audit-checklist.md`
- Use a user-specified path when provided

## Recommended Structure

```md
# Test Deep Audit Checklist

## Status
- Last updated: 2026-04-18
- Areas reviewed: 0
- Total issues: 0
- Completed: 0
- Remaining: 0

## Audit Map
- [x] Test commands and CI
- [ ] Unit and integration
- [ ] Browser and e2e
- [ ] Accessibility
- [ ] Contracts

## Findings

### Test commands and CI
- [ ] [High] Add a single repo-documented smoke command that runs the fastest high-signal checks.
  Why: Contributors have no obvious default validation path before shipping.
  Fix target: `package.json`, CI workflow docs
  Validate: Run the new command locally and in CI.

### Checkout API client
- [ ] [High] Add a consumer-side contract test for the checkout client.
  Why: The frontend depends on response shapes that are not enforced anywhere.
  Fix target: `src/api/checkout/*`
  Validate: Consumer contract generation plus provider verification path documented.
```

## Item Rules

- Use `- [ ]` for unresolved or blocked work.
- Use `- [x]` only for work that is implemented and validated.
- Group by area or subsystem, then by page, package, or file target.
- Include severity, why it matters, fix target, and validation method.
- Prefer one issue per checkbox rather than giant multi-problem items.
