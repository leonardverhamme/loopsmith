<!-- agent-cli-os:auto-generated -->
# Agent CLI OS State Schema

## Deep Workflow State

The shared deep-workflow schema lives at `agentctl/references/state-schema.md` and is the canonical contract for repo-local workflow state.

## Maintenance Report Schema

The maintenance report is stored at `docs/agent-cli-os/maintenance-report.json` and is mirrored into `.codex-workflows/agentcli-maintenance/state.json`.

Top-level report fields:

- `schema_version`
- `generated_at`
- `root`
- `summary`
- `command_surface`
- `artifacts`
- `docs`
- `references`
- `skills`
- `plugin`
- `tests`
- `cloud_readiness`
- `inventory_snapshot`
- `guidance_snapshot`
- `official_skill_loader`
- `repo_intel_trusted_audit`
- `capabilities_snapshot`
- `known_limitations`
- `findings`

## Lifecycle Semantics

- Repo-local workflow state is canonical; the global registry is only a convenience mirror.
- `ready_allowed` is the completion gate. A workflow must not claim `complete` unless this is `true`.
- `remaining_items` and `blocked_items` should always be derivable from the current checklist, not chat memory.
- `last_validation` should capture the smallest real validation that supports the last completed batch.
- Shared-registry writes must remain concurrency-safe because multiple deep workflows may update the registry at the same time.

## Status Meanings

- `initializing`: state exists but the first meaningful batch has not completed yet.
- `running`: the workflow is active and more work remains.
- `complete`: all tracked work is done and the ready gate passes.
- `blocked`: remaining work exists but a real blocker currently prevents completion.
- `stalled`: repeated attempts failed to make meaningful progress.
- `error`: the state itself is malformed or execution failed before a valid workflow step completed.

## Current Shared Workflow Fields

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

## Current Maintenance Summary

```json
{
  "blocked_findings": 0,
  "open_findings": 1,
  "passed_checks": 149,
  "status": "degraded",
  "total_checks": 150
}
```
