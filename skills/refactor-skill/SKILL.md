---
name: refactor-skill
description: "Use when a bounded feature area or module needs a behavior-preserving refactor: split long files, extract helpers or components, tighten boundaries, remove duplication, or modernize patterns. Not for broad checklist-driven campaigns; use refactor-deep-audit."
---

# Refactor Skill

## Stability

- Treat this skill as stable infrastructure.
- Do not edit this skill unless the user explicitly opens `$editskill` for it.

Use this skill for small to medium refactors that should stay behavior-preserving, test-backed, and tightly scoped.

Use:

- `$refactor-deep-audit` for repo-wide audits and checklist execution
- `$refactor-orchestrator` for phased multi-module migrations
- `$test-skill` when safety nets need to be added or expanded
- `$docs-skill` when docs or ADRs must change with the structure

## Bare Invocation Behavior

If the user explicitly invokes `$refactor-skill` with no meaningful extra instruction, do a lightweight refactor review and report:

1. the most obvious safe refactor targets in the current area
2. the behavior constraints and validation path
3. the smallest high-value refactor to do next

## Required Workflow

1. Inspect the target code first:
   - responsibilities, boundaries, call sites, data flow, existing tests, validation commands, and any repo constraints
2. Define the behavior boundary before editing.
3. Load only the references you need:
   - Always: `references/behavior-preserving.md`, `references/safety-net.md`, `references/scope-control.md`
   - Common moves: `references/refactor-patterns.md`
   - Comparative lookup only: `references/premade-systems.md`, `references/prompt-template.md`
4. If coverage is weak, add or update the smallest useful characterization tests before risky edits.
5. Refactor in small verified steps.
6. Run the relevant checks after each meaningful step or batch.
7. Keep the diff narrow and structural.
8. Report what improved, what remains awkward, and what should wait for a broader pass.

## Default Refactor Posture

- Preserve behavior first.
- Prefer small steps over one-shot rewrites.
- Backfill safety nets before risky changes.
- Reuse existing repo abstractions before inventing new ones.
- Favor extraction, renaming, and simplification over architectural churn.
- Use repo-native CLIs first for validation.

## Hard Rules

- Do not silently mix feature changes into a refactor.
- Do not weaken correct tests just to get green.
- Do not do a repo-wide sweep without explicit scope.
- Do not leave the code in a partially broken state between steps when smaller steps are possible.
- If a correct test exposes a real defect, fix the product code or setup, not the test.
- Stop and ask only when ongoing user changes create a direct conflict.

## References

- `references/behavior-preserving.md`
- `references/refactor-patterns.md`
- `references/safety-net.md`
- `references/scope-control.md`
- `references/premade-systems.md`
- `references/prompt-template.md`
