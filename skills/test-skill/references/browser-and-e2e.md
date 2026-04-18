# Browser And E2E

Use this reference for real-browser verification and persistent end-to-end tests.

## CLI First

When browser automation is needed:

1. Prefer the repo's existing Playwright or browser test CLI if it exists.
2. Prefer `playwright-cli` or the local `$playwright` skill for smoke checks and exploration.
3. Use Playwright MCP only when CLI workflows cannot provide enough signal, or when persistent interactive browser reasoning is worth the extra overhead.

This matches Playwright's own guidance that `playwright-cli` is best for coding agents that favor token-efficient, skill-based workflows, while MCP is better for specialized iterative loops.

## Persistent E2E Tests

Use Playwright Test for permanent suites when the repo uses Playwright or needs a modern browser runner.

Rules:

- Prefer semantic locators and explicit contracts.
- Use web-first assertions.
- Avoid arbitrary sleeps.
- Keep tests isolated.
- Use saved auth state or fixtures intentionally.
- Turn a reproduced browser bug into a permanent spec when the bug matters.

## Browser Smoke Checks

Use smoke checks when:

- you need to confirm a UI flow before writing a permanent test
- a bug is hard to reason about from source alone
- you need a fast post-fix confirmation

## Accessibility And Visual Hooks

- Accessibility should live inside or beside Playwright tests via `@axe-core/playwright` plus manual keyboard checks.
- Visual regression should use `toHaveScreenshot()` only on stable pages or components and in a stable environment.

## Source Notes

- Playwright CLI versus MCP:
  - https://playwright.dev/docs/getting-started-cli
  - https://playwright.dev/docs/next/getting-started-mcp
- Playwright best practices:
  - https://playwright.dev/docs/best-practices
- Playwright visual comparisons:
  - https://playwright.dev/docs/next/test-snapshots
- Playwright accessibility:
  - https://playwright.dev/docs/next/accessibility-testing
- OpenAI Playwright skill page:
  - https://skills.sh/openai/skills/playwright
