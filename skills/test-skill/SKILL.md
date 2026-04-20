---
name: test-skill
description: "Use when a bounded change needs the agent to choose and add the materially needed tests itself: unit, integration, contract, browser, accessibility, regression, data, or performance smoke. Not for repo-wide checklist audits; use test-deep-audit."
---

# Test Skill

## Stability

- Treat this skill as stable infrastructure.
- Do not edit this skill unless the user explicitly opens `$editskill` for it.

## Repo artifacts

- Put helpers, fixtures, and generated test helpers in the target repo, not in `$CODEX_HOME` and not in a skill folder.

Use this skill for normal testing work across repos. Use `$test-deep-audit` instead for repo-wide audits, checkbox backlogs, or execute-until-ready remediation.

## Required Workflow

1. Inspect the repo first:
   - repo test commands, CI entrypoints, existing test folders, fixtures, mocks, seeds, factories, and any runnable browser path
2. Do a deliberate test-surface sweep before writing tests. Explicitly decide whether each of these layers is required, optional, or not needed:
   - unit, integration, API or contract, e2e, browser smoke or Playwright, accessibility, visual regression, regression for fixed bugs, edge-case or property-based, data or migration, performance smoke
3. Prefer the repo's existing test CLI first.
4. Load only the references you need:
   - Always: `references/strategy.md`, `references/test-review.md`
   - Unit or integration: `references/unit-and-integration.md`
   - Browser, e2e, or smoke: `references/browser-and-e2e.md`
   - Accessibility, contracts, visual, mutation, or edge-case: `references/advanced-quality.md`
   - Ecosystem lookup only: `references/premade-stack.md`, `references/prompt-template.md`
5. Choose the smallest correct combination of test layers that covers the risk.
6. Implement the tests in repo patterns.
7. Run the smallest correct validation before stopping. If runnable UI changed, include a real Playwright pass.
8. If a correct test fails, fix product code or setup instead of weakening the test.
9. Re-run until the relevant suites are green or a real blocker remains.
10. Report which layers were selected, what was verified, and what still carries risk.

## Bare invocation

If the user invokes `$test-skill` with no meaningful extra instruction, inspect the test stack and report:

1. current frameworks and commands
2. obvious gaps in unit, integration, e2e, and regression coverage
3. the highest-value tests to add next

## Default Testing Posture

- Prefer the repo's current framework over introducing a new one.
- Prefer focused, hermetic tests over sprawling brittle tests.
- Prefer integration tests over over-mocked unit tests when behavior crosses real module boundaries.
- Keep e2e coverage focused on critical user journeys and cross-page regressions.
- Add browser, accessibility, contract, visual, persistence, or performance coverage whenever the change materially affects that layer.
- Always add a regression test for a real bug fix when feasible.
- Prefer CLI-first browser workflows:
  - repo-native test CLI first
  - Playwright CLI or the local `$playwright` skill next
  - MCP or browser automation only when CLI workflows are insufficient

## Hard Rules

- Do not introduce a new test framework if the repo already has a working one for the same layer.
- Do not write redundant tests at three layers when one focused layer already covers the risk.
- Do not ask the user to enumerate test types when the repo and task already make the needed layers clear.
- Do not default to MCP when a CLI or test runner already provides the needed signal.
- Do not hide unresolved flakiness behind retries without identifying the cause.
- Do not mark a bug fix complete without adding or considering permanent regression coverage.
- Do not weaken assertions or delete meaningful coverage just to make the suite pass.
- Do not skip accessibility, contract, visual, or persistence coverage just because the user only asked for "tests" in general.
- Do not treat "Playwright was busy" or "the browser MCP was locked" as a reason to skip a needed browser validation.
- Do not stop browser validation because the first app port was occupied; use another free port and continue.

## References

- `references/strategy.md`
- `references/unit-and-integration.md`
- `references/browser-and-e2e.md`
- `references/advanced-quality.md`
- `references/green-loop.md`
- `references/premade-stack.md`
- `references/test-review.md`
- `references/prompt-template.md`
