---
name: docs-deep-audit
description: "Use when a repo needs a full documentation audit, a canonical checklist, and execute-until-ready remediation across README, onboarding, architecture, ADRs, runbooks, and command docs."
---

# Docs Deep Audit

## Visible Skill Usage

- When this skill is actively being used in chat, mention `$docs-deep-audit` once in a user-visible update so the human can see the highlighted skill route.
- Keep that mention concise and do not repeat it in every paragraph.

## Stability

- Treat this skill as stable infrastructure.
- Do not edit this skill unless the user explicitly opens `$editskill` for it.

## Repo artifacts

- Put generated docs helpers and audit artifacts in the target repo, not in `$CODEX_HOME` and not in a skill folder.

Use this skill for the heavy documentation workflow that `$docs-skill` should not absorb: full-repo docs audit, canonical checklist creation, tracked execution, and final closeout.

## Required Entry Point

- If `agentcli` is available, start or resume through `agentcli run docs-deep-audit`.
- Treat `docs/docs-deep-audit-checklist.md` as the human queue and `.codex-workflows/docs-deep-audit/state.json` as the machine queue.
- Re-read both before each batch. Repair state from the checklist when they disagree.
- Do not pretend a manual chat batch is an unattended loop.

## Default Behavior

If the user explicitly invokes `$docs-deep-audit` with no meaningful extra instruction:

1. Use `docs/docs-deep-audit-checklist.md`.
2. Audit the repo docs surface and create or refresh the checklist when needed.
3. Execute unchecked items in the same run.
4. Close out only when zero unchecked items remain and validation passes.

## Required Workflow

1. Inspect the repo first:
   - README, onboarding, architecture, ADRs, runbooks, command docs, feature docs, AGENTS files, and the code and commands they should reflect
2. Load only the references you need:
   - Always: `references/audit-scope.md`, `references/checklist-format.md`, `references/execution-loop.md`, `references/closeout.md`
   - Prompt shortcuts only when needed: `references/prompt-shortcuts.md`
3. Load `$docs-skill` before implementing checklist items.
4. Create or refresh the checklist unless the user explicitly asked for audit-only mode.
5. Group findings by doc surface, then by file or subsystem.
6. Use markdown checkboxes:
   - `- [ ]` unresolved or blocked
   - `- [x]` implemented and validated
7. Keep findings concrete and implementation-ready.
8. Start execution in the same run unless the user explicitly asked for audit-only mode.
9. Before marking anything done, implement it, verify commands, paths, and code alignment, and update the checklist.
10. Continue until zero unchecked items remain or a real blocker remains.
11. Only reply `ready` when the closeout rules pass.

## Closeout Rules

- Do not say `ready` if any `- [ ]` items remain.
- Do not say `ready` if items were marked complete without evidence of updated docs and verification.
- Do not say `ready` if key docs still drift from the code or commands.
- If blocked items remain, say what is blocked and why.

## References

- `references/audit-scope.md`
- `references/checklist-format.md`
- `references/execution-loop.md`
- `references/closeout.md`
- `references/prompt-shortcuts.md`
