# Closeout

Use this reference before the final response.

## `ready` Gate

Only reply `ready` when all of the following are true:

- The checklist file has zero `- [ ]` items remaining.
- The checklist file reflects the real completion state.
- Completed items have corresponding workflow or automation changes.
- Relevant validation was run and did not reveal remaining failures.
- The repo's CI/CD posture is materially better in the areas the checklist claimed to fix.

## If the Gate Fails

- Do not reply `ready`.
- Summarize what is still unchecked or blocked.
- Name the workflows, environments, or validations that still need work.
