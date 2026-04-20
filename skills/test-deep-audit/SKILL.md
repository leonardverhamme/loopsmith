---
name: test-deep-audit
description: "Use when a repo needs a full test audit, a canonical checklist, and execute-until-ready remediation across backend, frontend, CI, browser, contracts, accessibility, and regression coverage."
---

# Test Deep Audit

## Stability

- Treat this skill as stable infrastructure.
- Do not edit this skill unless the user explicitly opens `$editskill` for it.

## Repo artifacts

- Put checklist files, helpers, fixtures, and generated test artifacts in the target repo, not in `$CODEX_HOME` and not in a skill folder.

Use this skill for the heavy workflow that `$test-skill` should not absorb: full-repo audit, canonical checklist creation, tracked execution, and final closeout.

## Required Entry Point

- If `agentcli` is available, start or resume through `agentcli run test-deep-audit`.
- Treat `docs/test-deep-audit-checklist.md` as the human queue and `.codex-workflows/test-deep-audit/state.json` as the machine queue.
- Re-read both before each batch. Repair state from the checklist when they disagree.
- Do not pretend a manual chat batch is an unattended loop.

## Default Behavior

If the user explicitly invokes `$test-deep-audit` with no meaningful extra instruction:

1. Use `docs/test-deep-audit-checklist.md`.
2. Audit the repo and create or refresh the checklist when needed.
3. Execute unchecked items in the same run.
4. Close out only when zero unchecked items remain and validation passes.

## Required Workflow

1. Inspect the repo first:
   - test commands, CI workflows, coverage tooling, fixtures, browser automation, accessibility, contracts, property-based testing, mutation gaps, flakiness, and speed
2. Load only the references you need:
   - Always: `references/audit-scope.md`, `references/checklist-format.md`, `references/execution-loop.md`, `references/closeout.md`
   - Prompt shortcuts only when needed: `references/prompt-shortcuts.md`
3. Load `$test-skill` before implementing checklist items.
4. Create or refresh the checklist unless the user explicitly asked for execution-only mode.
5. Group findings by area, then by page, feature, package, or subsystem.
6. Use markdown checkboxes:
   - `- [ ]` unresolved or blocked
   - `- [x]` implemented and validated
7. Keep findings concrete and implementation-ready.
8. Execute the checklist in the same run unless the user explicitly asked for audit-only mode.
9. Before marking anything done, implement it, validate it, run a real Playwright pass for runnable UI work, and update the checklist.
10. Continue until zero unchecked items remain or a real blocker remains.
11. Only reply `ready` when the closeout rules pass.

## Parallel And Agent Rules

- Use the checklist file as the stateful queue.
- If the user explicitly asks for subagents, split by audit zone or subsystem.
- Good slices include unit and integration, backend and API boundaries, frontend and forms, browser and Playwright, accessibility and visual regression, contracts and schemas, and flake or speed problems.

## Closeout Rules

- Do not say `ready` if any `- [ ]` items remain.
- Do not say `ready` if items were marked complete without evidence of implementation and validation.
- Do not say `ready` if a required browser pass was skipped because Playwright was busy or the first port was blocked.
- Do not say `ready` if the suite is still broken, flaky, or materially unbalanced in areas the checklist claimed to fix.
- If blocked items remain, say what is blocked and why.

## References

- `references/audit-scope.md`
- `references/checklist-format.md`
- `references/execution-loop.md`
- `references/closeout.md`
- `references/prompt-shortcuts.md`
