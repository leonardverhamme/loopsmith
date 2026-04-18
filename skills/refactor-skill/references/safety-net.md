# Safety Net Before Refactoring

Refactoring is cheap when behavior is observable and expensive when it is not.

## Check Before Editing

- What commands prove the target area still works?
- Which tests already cover the path?
- Which user-facing or API-facing behaviors must not change?
- Is there a stable local CLI to run after each step?

## If Coverage Is Weak

Prefer the lightest useful safety net:

- a characterization test for current behavior
- a focused integration test around the seam you will touch
- a typecheck or compile pass if the language makes that a strong guardrail
- a browser or CLI smoke check for high-risk UI or workflow code

## After Each Step

- run the narrowest relevant validation command
- expand to the broader suite before stopping
- treat failures as information, not friction

## If Tests Fail

- confirm whether the test expresses correct behavior
- if yes, fix the product code or setup
- only change the test when the test itself is wrong, stale, or asserting implementation detail

This matches the same reliability rule already used in `test-skill`.
