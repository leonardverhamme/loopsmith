<!-- loopsmith:auto-generated -->
# Loopsmith Command Map

This is the frozen v1 command surface that maintenance checks expect.

## Quick Routing Rules

- `doctor` is the shortest health-oriented entrypoint.
- `capabilities` is the full menu for capability discovery.
- `capability <key>` is the drill-down page for a single capability and should be preferred before choosing lower-level vendor tools.
- `status` is for workflow progress, not general health.
- `run` is only for deep workflows that use the shared runner/state contract.
- `run` should prefer a real worker runtime such as Codex CLI or an explicit worker command, not chat-only repetition.
- `research` is for evidence creation, not implementation.
- `skills` wraps official install/update tooling and provenance checks.
- `maintenance` is only for the control plane itself.

## Verification Notes

- `run` is tested at two levels: the shared workflow runner directly and the public `loopsmith run` CLI path.
- Shared state transitions are expected to end as `complete`, `blocked`, or `stalled`; `ready_allowed` must gate any `complete` state.
- Shared-registry updates are expected to tolerate concurrent deep workflows without losing entries.

## Core

- `loopsmith doctor [--fix] [--json]`
  - Check installed tools, wrappers, auth health, and browser readiness, with optional local repair.
- `loopsmith capabilities [--json]`
  - Emit the machine-readable capability inventory and grouped front doors.
- `loopsmith capability <key> [--json]`
  - Show the drill-down page for a capability group or a single capability.
- `loopsmith status [--repo <path>] [--all] [--json]`
  - Inspect repo-local or registry-backed deep workflow state.
- `loopsmith run <workflow> [--repo <path>] [--worker-command <cmd>]`
  - Launch or resume a deep workflow through the shared runner.
- `loopsmith self-check [--json]`
  - Compare wrapper version, bundle version, config schema, and plugin health.
- `loopsmith version [--json]`
  - Show wrapper and bundle version information.
- `loopsmith upgrade [--version <tag>] [--json]`
  - Upgrade the installed bundle from its recorded release source.

Typical sequence:

- `loopsmith doctor`
- `loopsmith capabilities` if you need the full menu
- `loopsmith status --all` if you need workflow progress
- `loopsmith run <workflow>` only when a deep workflow is the right shape
- If no worker runtime is healthy, configure `--worker-command` or `AGENTCTL_CODEX_WORKER_TEMPLATE` before treating the run as unattended

## Research

- `loopsmith research web <query> [--limit N]`
  - Research current public web sources through the shared evidence contract.
- `loopsmith research github <query> [--limit N]`
  - Research GitHub repositories, code, issues, and releases through gh-first routing.
- `loopsmith research scout <query> [--limit N]`
  - Run web and GitHub research together and merge them into one evidence envelope.

Typical sequence:

- `loopsmith research web <query>` for current official docs or standards
- `loopsmith research github <query>` for field practice and repository evidence
- `loopsmith research scout <query>` when both are needed before implementation

## Config

- `loopsmith config show [--repo <path>] [--json]`
  - Show bundled, user, repo, and effective config layers.
- `loopsmith config path [--scope bundled|user|repo] [--json]`
  - Show the path for one config scope.
- `loopsmith config set <key> <value> [--scope user|repo] [--json]`
  - Set a structured config key in the user or repo layer.
- `loopsmith config unset <key> [--scope user|repo] [--json]`
  - Remove a structured config key from the user or repo layer.


## Skills

- `loopsmith skills list [--project] [--json]`
  - List installed skills through the official skills CLI.
- `loopsmith skills add <source> [--skill <name>] [--ref <ref>] [--project]`
  - Install skills with provenance recording and optional pinning.
- `loopsmith skills check [--project] [--json]`
  - Compare installed skills with the local provenance lock file.
- `loopsmith skills update [--project] [--json]`
  - Refresh tracked skills from the lock file without broad unsafe updates.

Typical sequence:

- `loopsmith skills list` to inspect current installs
- `loopsmith skills check` to inspect provenance and local-vs-external management
- `loopsmith skills add ...` only when you are intentionally extending the skill surface

## Maintenance

- `loopsmith maintenance check [--json]`
  - Check command/docs/plugin drift and write a machine-readable maintenance report.
- `loopsmith maintenance audit [--json]`
  - Run the full maintenance pass, refresh docs, and update maintenance state.
- `loopsmith maintenance fix-docs [--json]`
  - Regenerate the human-facing loopsmith docs from current machine state.
- `loopsmith maintenance render-report [--json]`
  - Render the maintenance Markdown page and JSON report without regenerating every doc.

Typical sequence:

- `loopsmith maintenance check` for a quick control-plane inspection
- `loopsmith maintenance audit` after code or contract changes
- `loopsmith maintenance fix-docs` only when the docs need regeneration without broader change
