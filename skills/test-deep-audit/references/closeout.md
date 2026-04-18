# Closeout

Use this reference before the final response.

## `ready` Gate

Only reply `ready` when all of the following are true:

- The checklist file has zero `- [ ]` items remaining.
- The checklist file reflects the real completion state.
- Completed items have corresponding implementation work.
- Relevant validation was run and did not reveal remaining failures.
- The repo's testing posture is materially better in the areas the checklist claimed to fix.

## If The Gate Fails

- Do not reply `ready`.
- Summarize what is still unchecked or blocked.
- Name the files, subsystems, or validations that still need work.

## Final Report Shape

- Checklist path
- Remaining unchecked count
- What was validated
- Whether the run is truly complete
