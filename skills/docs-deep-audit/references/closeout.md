# Closeout

Use this reference before the final response.

## `ready` Gate

Only reply `ready` when all of the following are true:

- The checklist file has zero `- [ ]` items remaining.
- The checklist file reflects the real completion state.
- Completed items have corresponding documentation updates.
- Relevant verification was run and did not reveal remaining drift.
- The durable docs are materially clearer and more aligned with the repo.

## If the Gate Fails

- Do not reply `ready`.
- Summarize what is still unchecked or blocked.
- Name the files, doc surfaces, or validations that still need work.
