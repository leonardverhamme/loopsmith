# Testing Strategy

Use this reference to choose the right layer before writing tests.

## Core Rule

Choose the smallest test layer that covers the real risk with clear signal.

## Layer Priorities

- Unit: pure logic, transforms, validators, reducers, math, parsing, permission rules
- Integration: module boundaries, service plus database, route plus auth, component plus data loading, form plus submit flow
- End-to-end: critical user journeys, cross-page regressions, browser-only behavior, role-based paths
- Browser smoke: quick real-browser verification without committing a full spec yet
- Regression: any real bug fix or incident-prone area
- Accessibility: forms, dialogs, navigation, tables, focus, keyboard, labels
- Contract: frontend client versus backend API, service versus service, events and messages
- Visual: stable pages or components where layout drift matters
- Edge-case and property-based: parsers, money logic, search, sort, import, export, date and time
- Mutation: critical logic where you need to know whether the current suite is actually strong

## Practical Balance

Rough heuristics from Google and web.dev still hold up:

- a broad unit base
- a strong integration middle
- a much smaller set of e2e tests

Do not treat those ratios as law. For modern product apps, a healthy integration layer often buys more confidence than bloated unit suites or excessive end-to-end coverage.

## Source Notes

- Google testing pyramid and 70/20/10 heuristic:
  - https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html
  - https://testing.googleblog.com/2009/05/
- web.dev testing strategy guidance:
  - https://web.dev/ta-strategies
  - https://web.dev/ta-what-to-test

