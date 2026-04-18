# Shared Deep-Skill Workflow Schema

This directory defines the shared runtime contract for deep skills:

- `ui-deep-audit`
- `test-deep-audit`
- `docs-deep-audit`
- `cicd-deep-audit`
- `refactor-deep-audit`

The deep skill is the worker. The runner owns repetition, retries, stagnation detection, and stop conditions.

## Canonical State

Repo-local machine state:

- `.codex-workflows/<workflow-name>/state.json`

Human-facing files:

- checklist file, such as `docs/ui-deep-audit-checklist.md`
- optional progress projection, such as `docs/ui-deep-audit-progress.md`

Global mirror:

- `../workflow-state/registry.json`

The global registry is a convenience mirror only. The repo-local state is the source of truth.

## Required State Fields

- `schema_version`
- `workflow_name`
- `skill_name`
- `repo_root`
- `checklist_path`
- `progress_path`
- `status`
  - `initializing`
  - `running`
  - `complete`
  - `blocked`
  - `stalled`
  - `error`
- `iteration`
- `max_iterations`
- `stagnant_iterations`
- `max_stagnant_iterations`
- `tasks_total`
- `tasks_done`
- `tasks_blocked`
- `tasks_open`
- `last_batch`
- `last_validation`
- `last_error`
- `ready_allowed`
- `remaining_items`
- `blocked_items`
- `evidence`

## Checklist Expectations

The checklist remains Markdown for human visibility.

Required checkbox format:

```md
- [ ] unresolved item
- [x] completed item
```

Blocked items stay unchecked and should include a blocker note on the same item or the next line.

## Guard Contract

Command:

```text
python ../workflow-tools/workflow_guard.py --state <state.json>
```

Exit codes:

- `0`: complete, `ready` allowed
- `1`: unfinished, continue loop
- `2`: blocked or stalled, stop and surface why
- `3`: invalid or inconsistent state/checklist, stop hard

## Runner Contract

Command:

```text
python ../workflow-tools/workflow_runner.py --skill <skill-name> --repo <repo-root> [--checklist <path>] [--max-iterations 30] [--max-stagnant 3]
```

Current worker-command requirement:

- pass `--worker-command "<command>"`, or
- set `CODEX_WORKFLOW_WORKER_COMMAND`

The runner is ready for future Codex/cloud wrappers, but this environment does not currently provide a directly callable local `codex` CLI path, so worker invocation stays explicit in v1.

Compatibility note:

- older states may still contain `state_version`
- `schema_version` is now the canonical field
- runtime helpers backfill `schema_version` from `state_version` when needed

## Worker Environment Variables

Every worker pass receives:

- `CODEX_WORKFLOW_STATE`
- `CODEX_WORKFLOW_CHECKLIST`
- `CODEX_WORKFLOW_PROGRESS`
- `CODEX_WORKFLOW_SKILL`
- `CODEX_WORKFLOW_REPO`
- `CODEX_WORKFLOW_ITERATION`
- `CODEX_WORKFLOW_RETRY_HINT`

Workers are expected to:

1. load or initialize workflow state if needed
2. update the checklist for the current batch
3. update the state if they add richer validation or evidence
4. never self-certify `ready` without the guard passing

## Retry and Stall Rules

- The runner retries automatically while work remains.
- If a pass makes no meaningful progress, the runner increments `stagnant_iterations`.
- Meaningful progress means at least one of:
  - an item moved from open to done
  - blocked items changed
  - the remaining set materially changed
- After `max_stagnant_iterations` consecutive no-progress passes, the runner stops:
  - `blocked` if all remaining items are blocked
  - `stalled` otherwise
