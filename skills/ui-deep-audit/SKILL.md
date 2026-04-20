---
name: ui-deep-audit
description: Use when a React, Next.js, Tailwind, or shadcn/ui app needs a full UI audit, a canonical checklist, and execute-until-ready remediation across routes, shells, dashboards, forms, tables, and responsive behavior.
---

# UI Deep Audit

## Visible Skill Usage

- When this skill is actively being used in chat, mention `$ui-deep-audit` once in a user-visible update so the human can see the highlighted route.
- Keep that mention short and do not repeat it in every paragraph.

## Stability

- Treat this skill as stable infrastructure.
- Do not edit this skill unless the user explicitly opens `$editskill` for it.

## Repo artifacts

- Put audit checklists, screenshots, helpers, and generated artifacts in the target repo, not in `$CODEX_HOME` and not in a skill folder.

Use this skill for full-app UI audits, page-by-page checklist execution, dense operator-console cleanup, and execute-until-ready remediation. For implementation choices while working the checklist, load `$ui-skill`.

## Required Entry Point

- If `agentcli` is available, start or resume through `agentcli run ui-deep-audit`.
- Treat `docs/ui-deep-audit-checklist.md` as the human queue and `.codex-workflows/ui-deep-audit/state.json` as the machine queue.
- Re-read both before each batch. Repair state from the checklist when they disagree.
- Do not pretend a manual chat batch is an unattended loop.

## Default Behavior

If the user invokes `$ui-deep-audit` with no meaningful extra instruction:

1. Use `docs/ui-deep-audit-checklist.md`.
2. If it does not exist, audit the app and create it.
3. If it exists with unchecked items, execute the checklist.
4. If it exists with zero unchecked items, run closeout validation.
5. Only reply `ready` when closeout passes.

## Required Workflow

1. Inspect the app first:
   - routes, layouts, shell, navigation, shared UI, tokens, charts, tables, forms, AI surfaces, and verification commands
2. Load only the references you need:
   - Always: `../../docs/agent-cli-os/skill-support/ui-deep-audit/audit-scope.md`, `../../docs/agent-cli-os/skill-support/ui-deep-audit/checklist-format.md`, `../../docs/agent-cli-os/skill-support/ui-deep-audit/execution-loop.md`, `../../docs/agent-cli-os/skill-support/ui-deep-audit/closeout.md`
   - Prompt shortcuts only when needed: `../../docs/agent-cli-os/skill-support/ui-deep-audit/prompt-shortcuts.md`
3. Load `$ui-skill` before implementing checklist items.
4. Create or refresh the checklist if needed.
5. Group findings by page, then by section or component.
6. Use markdown checkboxes:
   - `- [ ]` unresolved or blocked
   - `- [x]` implemented and validated
7. Work small coherent batches.
8. Before marking any item done:
   - implement it
   - run the smallest correct validation
   - run a real Playwright browser pass for runnable UI
   - update the checklist
9. Continue until zero unchecked items remain.

## Audit Standards

- Cover the whole app, not just obvious screens.
- Prefer actionable defects over abstract design commentary.
- Treat low-value explainer copy as a defect when layout and labeling should carry the meaning.
- Treat density defects as first-class defects, especially stacked topbars, repeated toolbar rows, oversized dashboard headers, tall KPI strips, and top charts that push the main task below the fold.
- Check borders, radius, padding, legend wrapping, axis-label overflow, and chart-card sizing on overview and analytics pages.

## Dashboard-Specific Audit Checks

Flag a defect when any of these are true:

- top chrome consumes too much of the first viewport before the main task appears
- more than two stacked header or control bands appear without a strong reason
- a KPI strip or top chart is large enough that the main table, queue, or form is not visible early enough
- chart cards use loose borders, oversized padding, or inconsistent radius compared with the rest of the app
- legends, filters, or tabs create extra rows that should have been merged into the main control band
- axis labels, legends, or chart labels wrap, clip, or overflow in ways that hurt scanability

## Parallel And Agent Rules

- Use the checklist as the stateful queue.
- If the user explicitly asks for subagents, delegation, or parallel work, split by audit zone or page group.

## Closeout Rules

- Do not say `ready` if any `- [ ]` items remain.
- Do not say `ready` if items were marked done without implementation and validation.
- Do not say `ready` if runnable UI skipped real browser verification.
- Do not say `ready` if operator or dashboard pages still rely on long explainer copy or oversized top chrome.
- If blockers remain, say what is blocked and why.

## References

- `../../docs/agent-cli-os/skill-support/ui-deep-audit/audit-scope.md`
- `../../docs/agent-cli-os/skill-support/ui-deep-audit/checklist-format.md`
- `../../docs/agent-cli-os/skill-support/ui-deep-audit/execution-loop.md`
- `../../docs/agent-cli-os/skill-support/ui-deep-audit/closeout.md`
- `../../docs/agent-cli-os/skill-support/ui-deep-audit/prompt-shortcuts.md`
