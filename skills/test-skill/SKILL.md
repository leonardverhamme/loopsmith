---
name: test-skill
description: General cross-repo testing workflow for backend and frontend code. Use when adding or updating tests for new code, when the user says to add all needed tests for a feature or refactor, when fixing bugs with permanent regression coverage, when choosing and applying the right mix of unit, integration, API or contract, end-to-end, browser smoke, accessibility, visual, regression, edge-case, data or migration, and performance-smoke testing, or when tightening CI quality gates without test drift. This skill must select the materially needed test layers itself, add the right tests, run them, and keep iterating until the relevant suites are green, fixing product code when a correct test reveals a defect instead of weakening the test just to pass. Prefer repo-native CLIs first, then dedicated testing CLIs such as Playwright CLI, and only use MCP-style browser control when CLI workflows cannot provide enough signal. Not for full-repo checklist audits or execute-until-done remediation; use test-deep-audit for that.
---

# Test Skill

## Skill Stability Rule

- Treat this skill as stable infrastructure.
- Never create, edit, rename, move, or delete this skill's files during normal task execution.
- Only touch skill files when the user explicitly asks to change the skill system itself.
- Even then, do not edit immediately. First ask for explicit confirmation to open `skill-edit-mode` for the named skill or skills.
- If that confirmation is absent, refuse the skill-file edit and continue with non-skill work.

## Repo Artifact Rule

- If this workflow needs helper scripts, fixtures, or generated test helpers, create them in the target repo, not in `$CODEX_HOME`, not in a skill folder, and not in the agentctl bundle unless that bundle repo is the target.
- Prefer repo-native locations such as `scripts/`, `tools/`, `test/helpers/`, `tests/helpers/`, or `.github/scripts/`.

Use this skill for normal testing work across repos. It should make everyday testing decisions consistent, fast, and less brittle, while keeping frontend and backend coverage aligned with the actual risk in the code.

If you cannot load the supporting references for some reason, still follow the defaults in this file.

## What This Skill Covers

- Adding tests for new code
- Adding all needed tests for a newly added feature, subsystem, or refactor
- Refactoring weak or brittle tests
- Converting a bug fix into a permanent regression test
- Choosing and combining the right layers: unit, integration, API or contract, e2e, browser smoke, accessibility, visual, regression, edge-case, performance-smoke, and data or migration tests
- Keeping test suites fast and actionable
- Preserving the repo's existing testing stack without unnecessary framework drift

## Required Test-Surface Sweep

On every meaningful invocation of `$test-skill`, do a deliberate test-surface sweep before writing tests.

- Treat "add tests", "cover this feature", "make testing complete", or similar requests as permission to decide the needed test mix yourself.
- Do not wait for the user to separately ask for unit tests, integration tests, Playwright, regression coverage, or accessibility checks when the repo and task already imply them.
- Explicitly consider each of these layers and decide whether it is required, optional, or not needed for the current task:
  - unit
  - integration
  - API or contract
  - end-to-end
  - browser smoke or Playwright verification
  - accessibility
  - visual regression
  - regression coverage for fixed bugs
  - edge-case or property-based testing
  - data, migration, or persistence testing
  - performance smoke or startup-critical verification
- Only skip a layer when there is a concrete reason, such as "no runnable UI", "no external contract changed", or "visual risk is not material".
- In the final report, name the layers you selected and briefly explain anything important that you intentionally skipped.

## Use The Companion Audit Skill When Needed

If the request is any of the following, use `$test-deep-audit` instead:

- Full-repo test audit
- Writing or refreshing a checkbox backlog of test gaps
- Working a test checklist until every item is done
- Replying only `ready` when the whole test backlog is complete
- Auditing coverage, flakiness, CI, accessibility, contracts, and edge cases across the entire repo

## Bare Invocation Behavior

If the user explicitly invokes `$test-skill` with no meaningful extra instruction, do a lightweight test-stack inspection and report:

1. the current test frameworks and commands
2. obvious gaps in unit, integration, e2e, and regression coverage
3. the next highest-value tests to add

Do not run a full checklist audit in this mode.

## Required Workflow

1. Inspect the repo first:
   - `package.json`, lockfiles, `pyproject.toml`, `go.mod`, `Cargo.toml`, build files, CI workflows, and test scripts
   - existing test folders, fixtures, mocks, seeds, factories, and reporters
   - any browser or dev-server scripts needed for full-stack tests
2. Do the required test-surface sweep for the specific change:
   - Decide which layers are materially required.
   - Assume the user wants the full needed mix, not the minimum they happened to name.
   - Favor the smallest set that closes the real risk, but combine layers when one layer alone would leave a meaningful gap.
3. Prefer the repo's existing test CLI first.
4. If the repo does not already define the exact testing path you need, load the right references from this skill:
   - Always: `references/strategy.md`, `references/test-review.md`
   - Unit or integration work: `references/unit-and-integration.md`
   - Browser, e2e, or smoke verification: `references/browser-and-e2e.md`
   - Regression, accessibility, contracts, visual, edge-case, or mutation work: `references/advanced-quality.md`
   - Ecosystem and prebuilt tools: `references/premade-stack.md`
   - Short reusable prompts: `references/prompt-template.md`
5. Choose the smallest correct combination of test layers that covers the risk.
6. Implement the tests in repo patterns.
7. Run the smallest correct validation before stopping.
   - If the task affects runnable UI, browser flows, or frontend behavior that should be seen in a browser, include a real Playwright pass.
   - If the Playwright MCP route is locked, stale, or held by another session, fall back to the Playwright CLI wrapper and start a fresh browser session.
   - If the current app port is unavailable or unstable, restart the app on another free port and continue the browser validation there.
8. If a newly added or updated test fails, determine whether:
   - the test is correct and the product code is wrong
   - the test is wrong, brittle, or asserting the wrong contract
9. Fix the right thing:
   - if the test is correct, fix product code or setup
   - if the test is wrong, fix the test
10. Re-run until the relevant suites are green or a real blocker remains.
11. Report what was verified, which test layers were selected, and what still carries risk.

## Default Testing Posture

- Prefer the repo's current framework over introducing a new one.
- Prefer focused, hermetic tests over sprawling brittle tests.
- Prefer integration tests over over-mocked unit tests when the behavior crosses real module boundaries.
- Default to unit plus integration coverage together when isolated logic and real module boundaries both matter.
- Keep e2e coverage focused on critical user journeys and cross-page regressions.
- Add browser smoke or Playwright verification whenever the change affects runnable UI, browser-visible state, navigation, forms, or frontend regressions that are easy to miss in headless unit tests.
- Add accessibility checks whenever user-facing UI, forms, navigation, dialogs, or keyboard interaction materially change.
- Add contract coverage whenever an API boundary, schema, webhook, external integration, or typed interface contract changes.
- Add visual checks when styling, layout, responsive behavior, or design-system rendering changes are a real source of regression risk.
- Always add a regression test for a real bug fix when feasible.
- Add persistence or migration coverage when the task changes storage models, migrations, seeds, serialization, or repository boundaries.
- Add performance smoke verification when startup, hot paths, rendering cost, or expensive data flows could regress materially.
- When a correct test fails, prefer fixing product code over weakening the test.
- Prefer CLI-first browser workflows:
  - repo-native test CLI first
  - Playwright CLI or the local `$playwright` skill next
  - MCP/browser automation only when CLI workflows are insufficient

## Tool Defaults

- JavaScript or TypeScript repos: prefer existing runner; if the repo is Vite-oriented or lacks a clear default, Vitest is the best default candidate.
- Browser end-to-end: prefer Playwright Test for persistent suites.
- Browser smoke or exploratory verification: prefer the local `$playwright` skill or `playwright-cli`.
- Accessibility: prefer Playwright plus `@axe-core/playwright`, plus manual keyboard and focus checks.
- Contract testing: prefer Pact or the repo's existing schema or contract layer.
- Edge-case testing: use property-based testing selectively with `fast-check` for critical logic.
- Mutation testing: use Stryker selectively on critical domains, not on the entire repo by default.

## Hard Rules

- Do not introduce a new test framework if the repo already has a working one for the same layer.
- Do not write redundant tests at three layers when one focused layer already covers the risk.
- Do not ask the user to enumerate test types one by one when the repo and task already make the needed layers clear.
- Do not default to MCP when a CLI or test runner already provides the needed signal.
- Do not generate brittle selector-heavy e2e tests when semantic locators or explicit contracts exist.
- Do not hide unresolved flakiness behind retries without identifying the cause.
- Do not mark a bug fix complete without adding or considering permanent regression coverage.
- Do not weaken assertions or delete meaningful coverage just to make the suite pass.
- Do not keep patching tests when the tests correctly expose broken product behavior.
- Do not skip accessibility, contract, visual, or persistence coverage just because the user only asked for "tests" in general.
- Do not treat "Playwright was busy" or "the browser MCP was locked" as an acceptable reason to skip a needed browser validation.
- Do not stop browser validation because the first app port was occupied; use another free port and continue.
- Do not stop before checking failure paths, not just happy paths.

## References

- `references/strategy.md`
- `references/unit-and-integration.md`
- `references/browser-and-e2e.md`
- `references/advanced-quality.md`
- `references/green-loop.md`
- `references/premade-stack.md`
- `references/test-review.md`
- `references/prompt-template.md`

