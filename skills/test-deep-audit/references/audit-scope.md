# Audit Scope

Use this reference to ensure the audit covers the full repository and not just a few test files.

## Coverage Areas

- Package manager scripts and test entrypoints
- CI workflows, matrix strategy, caching, sharding, and quality gates
- Unit coverage and missing low-level logic tests
- Integration coverage across modules, services, routes, and data boundaries
- Frontend component, form, and page-flow coverage
- Browser smoke, e2e, and Playwright coverage
- Accessibility test coverage and manual keyboard gaps
- Contract and schema-drift protection between frontend and backend or service boundaries
- Visual regression where layout drift matters
- Regression-test discipline for bug fixes
- Edge-case, property-based, mutation, flake, and speed risks
- Fixtures, factories, seeds, mocks, and isolation quality

## Audit Order

1. Map current commands and CI entrypoints.
2. Map current test frameworks and layers.
3. Review the highest-risk product surfaces and backend boundaries.
4. Review test gaps, brittleness, and quality drift.
5. Review speed, flakiness, and closeout discipline.

## Parallel Partitioning

When the user explicitly asks for subagents or deeper parallel coverage, split the audit by zone:

- scripts and CI
- unit and integration
- backend boundaries
- frontend and browser coverage
- accessibility and visual
- contracts and schemas
- edge cases, mutation, flake, and speed
