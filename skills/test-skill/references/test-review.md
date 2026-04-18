# Test Review

Load this before stopping on any testing task.

## Checklist

- The chosen test layer matches the real risk.
- The repo's existing test stack was reused where possible.
- Happy path and failure path are both covered.
- Edge cases that matter are covered.
- Browser tests use resilient locators and web-first assertions.
- Accessibility checks were included when UI behavior changed.
- A real bug fix gained regression coverage or a clear reason why it did not.
- The executed commands are the smallest correct validation for the change.
- When a correct test failed, product code was fixed instead of weakening the test.
- The resulting failures would point at the broken behavior, not at brittle setup.

## Output Format

1. What layer or layers were added or changed
2. What commands were run
3. What remains risky or untested
