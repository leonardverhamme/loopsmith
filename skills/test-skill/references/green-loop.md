# Green Loop

Use this reference when the task is not just to write tests, but to drive the code and tests to a correct green state.

## Core Rule

Do not optimize for green tests. Optimize for correct behavior plus green tests.

## Loop

1. Add or update the right tests for the change.
2. Run the relevant commands.
3. If tests fail, classify the failure:
   - product bug
   - incorrect test expectation
   - brittle or flaky test setup
   - missing fixture, seed, environment, or config
4. Fix the real cause.
5. Re-run until the relevant suites are green or a real blocker remains.

## Fix Discipline

- If the test expresses intended product behavior and fails, fix the product code.
- If the test is asserting the wrong contract, fix the test.
- If the test is brittle, stabilize it without lowering the behavioral bar.
- If the environment is wrong, fix the setup rather than weakening coverage.

## Anti-Patterns

- Deleting assertions just to get green
- Replacing meaningful assertions with smoke-level checks after a failure
- Marking broken behavior as expected without product reason
- Adding retries instead of addressing deterministic failures

