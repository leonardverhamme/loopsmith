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

## Repo Intel Manifest

Per repo, Agent CLI OS also owns:

- `.agentcli/repo-intel.json`

Required top-level fields:

- `schema_version`
- `repo_root`
- `repo_name`
- `graphify_version`
- `status`
- `last_successful_build_at`
- `last_successful_code_build_at`
- `last_successful_semantic_build_at`
- `last_built_commit`
- `last_built_branch`
- `graph_paths`
- `obsidian_export_path`
- `ignore_hash`
- `config_hash`
- `code_fingerprint`
- `semantic_fingerprint`
- `last_error`

Allowed repo-intel states:

- `missing`
- `building`
- `fresh`
- `stale_code`
- `stale_semantic`
- `stale_config`
- `broken`
- `disabled`

## Workspace Registry

Machine-level repo-intel summary lives at:

- `agentctl/state/workspace-graph.json`

That file is an index-of-indexes over trusted repos. It should contain repo summaries and graph paths, not raw graph content.
