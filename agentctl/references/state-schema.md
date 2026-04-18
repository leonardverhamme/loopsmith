# agentctl State Schema

`agentctl` relies on the shared deep-workflow schema already defined in:

- `../../workflow-tools/workflow_schema.md`

Canonical repo-local state:

- `.codex-workflows/<workflow>/state.json`

Required top-level fields:

- `schema_version`
- `workflow_name`
- `skill_name`
- `repo_root`
- `checklist_path`
- `progress_path`
- `status`
- `iteration`
- `max_iterations`
- `stagnant_iterations`
- `max_stagnant_iterations`
- `tasks_total`
- `tasks_done`
- `tasks_open`
- `tasks_blocked`
- `last_batch`
- `last_validation`
- `last_error`
- `ready_allowed`
- `remaining_items`
- `blocked_items`
- `evidence`

`agentctl status` reads only this shared schema. If it sees an older `state_version` field without `schema_version`, it backfills compatibility in memory but treats `schema_version` as the canonical contract.
