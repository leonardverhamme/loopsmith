---
name: cicd-deep-audit
description: "Use when a repo needs a full CI/CD audit, a canonical checklist, and execute-until-ready remediation across pipelines, release automation, environments, quality gates, and deployment safety."
---

# CI/CD Deep Audit

## Stability

- Treat this skill as stable infrastructure.
- Do not edit this skill unless the user explicitly opens `$editskill` for it.

## Repo artifacts

- Put workflow helpers and audit artifacts in the target repo, not in `$CODEX_HOME` and not in a skill folder.

Use this skill for the heavy CI/CD workflow that `$cicd-skill` should not absorb: full automation audit, canonical checklist creation, tracked execution, and final closeout.

## Required Entry Point

- If `agentcli` is available, start or resume through `agentcli run cicd-deep-audit`.
- Treat `docs/cicd-deep-audit-checklist.md` as the human queue and `.codex-workflows/cicd-deep-audit/state.json` as the machine queue.
- Re-read both before each batch. Repair state from the checklist when they disagree.
- Do not pretend a manual chat batch is an unattended loop.

## Default Behavior

If the user explicitly invokes `$cicd-deep-audit` with no meaningful extra instruction:

1. Use `docs/cicd-deep-audit-checklist.md`.
2. Audit the pipeline surface and create or refresh the checklist when needed.
3. Execute unchecked items in the same run.
4. Close out only when zero unchecked items remain and validation passes.

## Required Workflow

1. Inspect the repo first:
   - CI workflows, release automation, deploy configs, build and test commands, concurrency, caches, environments, permissions, secrets references, artifact flow, and rollback docs
2. Load only the references you need:
   - Always: `references/audit-scope.md`, `references/checklist-format.md`, `references/execution-loop.md`, `references/closeout.md`
   - Prompt shortcuts only when needed: `references/prompt-shortcuts.md`
3. Load `$cicd-skill` before implementing checklist items.
4. Create or refresh the checklist unless the user explicitly asked for audit-only mode.
5. Group findings by automation surface, then by workflow, environment, or subsystem.
6. Use markdown checkboxes:
   - `- [ ]` unresolved or blocked
   - `- [x]` implemented and validated
7. Keep findings concrete and implementation-ready.
8. Start execution in the same run unless the user explicitly asked for audit-only mode.
9. Before marking anything done, implement it, validate workflow logic and underlying commands, and update the checklist.
10. Continue until zero unchecked items remain or a real blocker remains.
11. Only reply `ready` when the closeout rules pass.

## Closeout Rules

- Do not say `ready` if any `- [ ]` items remain.
- Do not say `ready` if items were marked complete without evidence of workflow changes and validation.
- Do not say `ready` if key quality gates, release safety, or pipeline correctness still drift from the checklist claims.
- If blocked items remain, say what is blocked and why.

## References

- `references/audit-scope.md`
- `references/checklist-format.md`
- `references/execution-loop.md`
- `references/closeout.md`
- `references/prompt-shortcuts.md`
