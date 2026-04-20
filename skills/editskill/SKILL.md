---
name: editskill
description: Use only when the user explicitly wants to create or change skill files and explicitly opens skill editing for the named targets. For substantial rewrites, evaluate before and after with plugin-eval.
---

# Edit Skill

Use this skill only for intentional work on the skill system itself.

## Entry Gate

- Do not use this skill just because a task touches tools, docs, or prompts.
- Only use this skill when the user explicitly asks to change a skill or create a new skill.
- Require explicit confirmation that skill editing should open for the named skill or skills before editing any files under `skills/` or `plugins/*/skills/`.

## What This Skill Covers

- Creating a new managed skill in a stable way
- Updating an existing managed skill after confirmation
- Renaming or reorganizing a managed skill after confirmation
- Regenerating or correcting companion `agents/openai.yaml`
- Validating a changed skill with the local validation path

## Safe Workflow

1. Confirm exactly which skill or skills may change.
2. Confirm whether this is a new skill, an update, a rename, or a packaging move.
3. Keep the change set as small as possible and avoid unrelated skill edits.
4. For substantial skill rewrites, run `plugin-eval analyze <skill-path>` first and save the brief.
5. Update the skill files, companion references, and `agents/openai.yaml` only for the confirmed scope.
6. Run `quick_validate.py` for every changed skill before stopping.
7. Re-run `plugin-eval analyze <skill-path>` after substantial changes so the before-and-after delta is visible.
8. If the skill is mirrored into a public bundle or plugin, sync that copy as part of the same change.
9. Summarize what changed and which skills were intentionally touched.

## Stability Rules

- Do not opportunistically clean up other skills while you are here.
- Do not widen the scope from one confirmed skill to many without a fresh confirmation.
- Do not edit curated third-party plugin skills unless the user explicitly asks for that and confirms the exact target.
- Do not leave a changed skill unvalidated.

## Compatibility

- Preferred public skill name: `$editskill`
- Legacy alias kept for compatibility: `$skill-edit-mode`

## References

- Use the built-in `skill-creator` guidance when you need help designing or validating a skill structure.
- Use `$plugin-eval:plugin-eval` or the local `plugin-eval analyze <skill-path>` command when you need a score, budget breakdown, or a before-and-after report.
- Use `$plugin-eval:improve-skill` when you already have an evaluation brief and want to turn it into a narrow rewrite plan.
- Follow the local `AGENTS.md` rules first when they are stricter than generic skill-creation guidance.
