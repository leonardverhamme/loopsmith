# Advanced Quality

Use this reference for the layers that make a suite more trustworthy than basic unit plus e2e coverage.

## Regression

- Any meaningful bug fix should usually gain a permanent regression test.
- Start from the smallest layer that can reproduce the bug with confidence.
- If the bug required a browser to observe, consider an e2e or browser-level regression.

## Accessibility

- Use Playwright plus `@axe-core/playwright` for automated checks.
- Also check keyboard flow, visible focus, labels, dialog focus trapping, and error messaging manually when needed.
- Automated scans help, but they do not replace manual accessibility review.

## Contract Testing

- Use Pact or an equivalent contract layer when frontend and backend assumptions drift or service boundaries are high risk.
- Focus on the actual requests, responses, and message shapes the consumer depends on.
- Verify providers against those expectations.

## Visual Regression

- Use Playwright screenshot assertions only for stable pages or components.
- Keep viewport, data, and environment stable.
- Avoid snapshotting highly volatile content.

## Edge-Case And Property-Based Testing

- Use `fast-check` selectively for critical invariants, parsers, import or export logic, money rules, and tricky state transitions.
- Property-based tests are high leverage when example-based tests keep missing weird input combinations.

## Mutation Testing

- Use Stryker selectively when you need to measure whether tests actually detect broken logic.
- Run it on critical domains, not the entire repo by default.

## Flake And Speed

- The larger and more integration-heavy a test is, the more likely it is to flake.
- Fix root causes before adding retries.
- Keep the test suite partitioned so fast feedback stays fast.

## Source Notes

- Pact:
  - https://docs.pact.io/getting_started/how_pact_works
  - https://docs.pact.io/implementation_guides/javascript/docs/consumer
- fast-check:
  - https://fast-check.dev/
- StrykerJS:
  - https://stryker-mutator.io/docs/stryker-js/introduction/
- Google flakiness guidance:
  - https://testing.googleblog.com/2017/04/

