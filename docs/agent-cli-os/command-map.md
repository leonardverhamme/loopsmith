<!-- agent-cli-os:auto-generated -->
# Agent CLI OS Command Map

This is the frozen v1 command surface that maintenance checks expect.

## Quick Routing Rules

- `doctor` is the shortest health-oriented entrypoint.
- `capabilities` is the compact grouped menu for capability discovery.
- `capability <key>` is the drill-down page for a single capability and should be preferred before choosing lower-level vendor tools.
- `skill-map` is the human-facing one-pager for the grouped menu, local front-door skills, and plugin-family counts.
- `inventory` is the raw autodetected surface for debugging, not the default front door.
- `repo-intel` is the default repo-first graph route when the target repo is already known.
- `computer-intel` is the whole-laptop exception path for repo discovery and cross-repo routing.
- `status` is for workflow progress, not general health.
- `run` is only for deep workflows that use the shared runner/state contract.
- `loop` is the generic long-task wrapper when there is no dedicated deep workflow for the job.
- `run` should prefer a real worker runtime such as Codex CLI or an explicit worker command, not chat-only repetition.
- `research` is for evidence creation, not implementation.
- `skills` wraps official install/update tooling and provenance checks.
- `maintenance` is only for the control plane itself.

## Verification Notes

- `run` is tested at two levels: the shared workflow runner directly and the public `agentcli run` CLI path.
- Shared state transitions are expected to end as `complete`, `blocked`, or `stalled`; `ready_allowed` must gate any `complete` state.
- Shared-registry updates are expected to tolerate concurrent deep workflows without losing entries.

## Core

- `agentcli doctor [--fix] [--json]`
  - Check installed tools, wrappers, auth health, and browser readiness, with optional local repair.
- `agentcli capabilities [--json]`
  - Show the compact grouped capability menu, not the raw installed inventory.
- `agentcli capability <key> [--json]`
  - Show the drill-down page for a capability group or a single capability.
- `agentcli skill-map [--json]`
  - Generate the human-facing skill/menu map and the matching one-page PDF.
- `agentcli status [--repo <path>] [--all] [--json]`
  - Inspect repo-local or registry-backed deep workflow state.
- `agentcli run <workflow> [--repo <path>] [--worker-command <cmd>]`
  - Launch or resume a deep workflow through the shared runner.
- `agentcli loop <name> [--repo <path>] (--task <text> | --task-file <path>)`
  - Launch a generic long task through the shared disk-backed loop when no dedicated deep workflow already fits.
- `agentcli self-check [--json]`
  - Compare wrapper version, bundle version, config schema, and plugin health.
- `agentcli version [--json]`
  - Show wrapper and bundle version information.
- `agentcli upgrade [--version <tag>] [--json]`
  - Upgrade the installed bundle from its recorded release source.

Typical sequence:

- `agentcli doctor`
- `agentcli capabilities` for the compact grouped menu
- `agentcli skill-map` for the human one-page map of local front-door skills
- `agentcli inventory show` only when you need the raw detected surface
- `agentcli status --all` if you need workflow progress
- `agentcli run <workflow>` when a dedicated deep workflow is the right shape
- `agentcli loop <name>` when the task is large but does not cleanly map to a dedicated deep workflow
- If no worker runtime is healthy, configure `--worker-command` or `AGENTCTL_CODEX_WORKER_TEMPLATE` before treating the run as unattended

## Research

- `agentcli research web <query> [--limit N]`
  - Research current public web sources through the shared evidence contract.
- `agentcli research github <query> [--limit N]`
  - Research GitHub repositories, code, issues, and releases through gh-first routing.
- `agentcli research scout <query> [--limit N]`
  - Run web and GitHub research together and merge them into one evidence envelope.

Typical sequence:

- `agentcli research web <query>` for current official docs or standards
- `agentcli research github <query>` for field practice and repository evidence
- `agentcli research scout <query>` when both are needed before implementation

## Inventory

- `agentcli inventory refresh [--repo <path>] [--json]`
  - Refresh and persist the raw autodetected inventory snapshot.
- `agentcli inventory show [--kind tools|skills|plugins|apps|mcp|all] [--scope user|repo|all] [--json]`
  - Inspect the raw app-aware inventory behind the curated capability menu.
- `agentcli inventory item <kind>:<name> [--json]`
  - Show one raw inventory record.

Typical sequence:

- `agentcli inventory refresh` after local installs or config changes that affect detection
- `agentcli inventory show --kind all --scope all` to inspect the raw detected surface
- `agentcli inventory item tool:gh` or a similar selector when one record needs detail

## Repo-Intel

- `agentcli repo-intel status [--repo <path>] [--json]`
  - Inspect Graphify-backed repo-intel health for one repo.
- `agentcli repo-intel ensure [--repo <path>] [--json]`
  - Create or refresh repo-intel artifacts for one repo, including `.graphifyignore`, managed `.gitignore` hygiene, manifest state, and the tiny AGENTS hint.
- `agentcli repo-intel update [--repo <path>] [--code-only|--semantic|--full] [--json]`
  - Refresh repo-intel artifacts using the lightest valid Graphify path for the current repo state.
- `agentcli repo-intel query <question> [--repo <path>] [--budget N] [--dfs] [--json]`
  - Query the local repo graph through Graphify instead of falling back to broad raw-file search.
- `agentcli repo-intel audit [--repo <path> | --all-trusted | --all-discovered] [--fix] [--json]`
  - Audit repo-intel and managed repo-hygiene status for one repo, every trusted repo, or every discovered repo from the machine-wide registry.
- `agentcli repo-intel serve [--repo <path>] [--json]`
  - Prepare or launch the local Graphify MCP server for the current repo graph.

Typical sequence:

- `agentcli repo-intel status` as soon as you enter a repo or before broad raw-file search
- `agentcli repo-intel ensure` when the repo graph is missing, stale, or broken
- `agentcli repo-intel query "<question>"` for architecture, flows, and path questions before wide grep
- `agentcli repo-intel serve` when an MCP client should talk to the local graph directly

## Computer-Intel

- `agentcli computer-intel status [--json]`
  - Inspect the machine-wide laptop discovery index and its scan coverage.
- `agentcli computer-intel refresh [--json]`
  - Refresh the machine-wide laptop discovery index without replacing per-repo Graphify graphs.
- `agentcli computer-intel search <query> [--kind all|repo|vault|graph|service|root|path] [--limit N] [--json]`
  - Search the machine-wide discovery surface to find repos, vaults, Graphify exports, services, or matching paths anywhere on the laptop.

Typical sequence:

- `agentcli computer-intel status` or `agentcli computer-intel refresh` when the task is about the whole laptop
- `agentcli computer-intel search <query>` to find the right repo, graph, vault, or path anywhere on the machine
- Switch back to `agentcli repo-intel ...` once the target repo is known

## Config

- `agentcli config show [--repo <path>] [--json]`
  - Show bundled, user, repo, and effective config layers.
- `agentcli config path [--scope bundled|user|repo] [--json]`
  - Show the path for one config scope.
- `agentcli config set <key> <value> [--scope user|repo] [--json]`
  - Set a structured config key in the user or repo layer.
- `agentcli config unset <key> [--scope user|repo] [--json]`
  - Remove a structured config key from the user or repo layer.


## Skills

- `agentcli skills list [--project] [--json]`
  - List installed skills through the official skills CLI.
- `agentcli skills add <source> [--skill <name>] [--ref <ref>] [--project]`
  - Install skills with provenance recording and optional pinning.
- `agentcli skills check [--project] [--json]`
  - Compare installed skills with the local provenance lock file.
- `agentcli skills update [--project] [--json]`
  - Refresh tracked skills from the lock file without broad unsafe updates.

Typical sequence:

- `agentcli skills list` to inspect current installs
- `agentcli skills check` to inspect provenance and local-vs-external management
- `agentcli skills add ...` only when you are intentionally extending the skill surface

## Maintenance

- `agentcli maintenance check [--json]`
  - Check command/docs/plugin drift and write a machine-readable maintenance report.
- `agentcli maintenance audit [--json]`
  - Run the full maintenance pass, refresh docs, and update maintenance state.
- `agentcli maintenance fix-docs [--json]`
  - Regenerate the human-facing Agent CLI OS docs from current machine state.
- `agentcli maintenance render-report [--json]`
  - Render the maintenance Markdown page and JSON report without regenerating every doc.

Typical sequence:

- `agentcli maintenance check` for a quick control-plane inspection
- `agentcli maintenance audit` after code or contract changes
- `agentcli maintenance fix-docs` only when the docs need regeneration without broader change
