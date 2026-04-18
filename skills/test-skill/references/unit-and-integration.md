# Unit And Integration

Use this reference when the work is mostly backend, business logic, or app-internal behavior.

## Unit Tests

Use unit tests for:

- pure functions
- parsers and serializers
- validation rules
- formatting logic
- reducers and state transitions
- pricing, permission, and policy logic

Rules:

- Test public behavior, not implementation trivia.
- Keep mocks at real boundaries only.
- Cover invalid inputs, empty inputs, null and undefined, thrown errors, and boundary values.
- Prefer table-driven tests when many cases share the same shape.

## Integration Tests

Use integration tests for:

- service plus repository or database
- route plus auth and permission checks
- component plus data fetching and user interaction
- form plus validation plus submit side effects
- queue, cache, or API boundary behavior

Rules:

- Minimize mocking.
- Exercise real module boundaries.
- Verify through the public interface the app actually uses.
- Cover happy path, failure path, and authorization path.

## Default Tooling

- Vitest is the best default candidate for modern JS or TS repos, especially when Vite is already present or the repo lacks a clear runner.
- If the repo already uses Jest, Pytest, PHPUnit, JUnit, Go test, Cargo test, or another established runner, stay with it.

## Source Notes

- Vitest rationale and performance:
  - https://vitest.dev/guide/why
  - https://vitest.dev/blog/
