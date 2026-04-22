# Agent CLI OS Repo Intel

Use this guide for the repo-intelligence subsystem.

## Purpose

Repo-intel gives each trusted repo a deterministic graph-backed orientation layer without turning the whole machine into one giant corpus.

The ownership split is deliberate:

- Graphify is the indexing engine.
- Agent CLI OS owns the command surface, state machine, workspace registry, and minimal repo contract.
- Computer-intel owns the machine-wide laptop discovery index.
- Obsidian is an optional export and browsing layer, not the source of truth.

## Layers

### Workspace Registry

The machine-level registry is an index-of-indexes. It tracks trusted repos, graph paths, and health.

Canonical file:

- `agentctl/state/workspace-graph.json`

This is not the repo graph itself.

Only trusted repos belong in this registry. Ad hoc status checks on temp repos, test fixtures, or untrusted folders must not pollute it.

Trusted repo audit should only consider actual repo roots, not arbitrary trusted
container folders that happen to sit above multiple mirrors or scratch
directories.

For laptop-wide discovery across more than trusted repos, use `computer-intel`.

### Per-Repo Graph

Each repo keeps its own Graphify artifacts:

- `graphify-out/graph.json`
- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/graph.html` when generated
- `.graphifyignore`
- `.gitignore` with the managed Agent CLI OS repo-hygiene block
- `.agentcli/repo-intel.json`

The operational default is repo-first:

- once the target repo is known, stay inside that repo
- use the repo graph before broad raw-file search
- use the machine-wide layer only when the task is explicitly cross-repo or the target repo is still unknown

The git default should also stay repo-first:

- treat the current local branch as the canonical place for normal solo work
- do not create or switch branches just to preserve agent changes
- treat Codex-managed worktrees as temporary isolation only
- if work should be kept and pushed, continue from the local checkout so local commits and pushes do not require merging a worktree branch back
- create a separate branch only when explicitly requested or when a real PR flow or parallel-agent workflow needs branch isolation

### Obsidian Export

Obsidian is optional. If enabled through config, full repo-intel builds ask Graphify to export an Obsidian-friendly view for the repo.

The repo-local Graphify artifacts stay canonical.

## Commands

```powershell
agentcli repo-intel status
agentcli repo-intel ensure
agentcli repo-intel update
agentcli repo-intel query "show the auth flow"
agentcli repo-intel audit --all-trusted
agentcli repo-intel audit --all-discovered
agentcli repo-intel serve
```

### `status`

Fast local check for the current repo state.

`status` should resolve the enclosing git repo root, not only the current working directory, so the command remains correct from nested folders.

### `ensure`

Makes the repo compliant:

- creates `.graphifyignore` if needed
- creates or refreshes the managed `.gitignore` repo-hygiene block for logs, local artifacts, and common test outputs
- writes the tiny repo-local `AGENTS.md` routing hint
- builds the graph if missing
- updates the graph if stale

For trusted repos, `ensure` is the default repair path that should keep graph-first retrieval available before broad raw-file search.

### `update`

Refreshes an existing repo graph using the lightest valid path:

- `--code-only`
- `--semantic`
- `--full`

`--semantic` currently falls back to a full rebuild, because Graphify exposes a cheap code-only update path but not a separate semantic-only CLI refresh path.

### `query`

Runs Graphify's local graph query path against the repo graph instead of broad raw-file search.

### `audit`

Sweeps one repo or all trusted repos and reports:

- `fresh`
- `missing`
- `stale_code`
- `stale_semantic`
- `stale_config`
- `broken`
- `disabled`

`--all-discovered` uses the machine-wide computer-intel registry so you can see
repo-intel posture across audit-candidate repos found on the laptop, not only
the trusted set.

This is intentionally narrower than raw machine-wide search. `computer-intel`
may still discover transient or tooling repos, but those stay searchable only
through `computer-intel` and do not automatically become repo-intel audit work.

`--fix` stays conservative:

- trusted repos may be repaired automatically
- untrusted discovered repos are reported but not silently mutated

### `serve`

Prepares or launches an MCP stdio server over the local repo graph when a compatible Graphify Python runtime is available.

## State Meanings

- `missing`: required graph artifacts do not exist
- `building`: a build is currently marked in progress
- `fresh`: graph and manifest match the current repo state
- `stale_code`: code-bearing files changed
- `stale_semantic`: docs, notes, media, or other semantic sources changed
- `stale_config`: `.graphifyignore`, the managed `.gitignore` hygiene block, repo-intel config, AGENTS guidance, or Graphify runtime signature changed
- `broken`: artifacts exist but are unreadable, partial, or incompatible with the manifest
- `disabled`: repo-intel is explicitly disabled in config

## Safe Defaults

- No mandatory hook installation.
- No Graphify-owned repo mutation as the primary contract.
- No large graph data injected into `AGENTS.md`.
- No full-disk crawl.
- No requirement that every repo commit graph artifacts.
- No use of the machine-wide computer-intel registry as a replacement for the repo-local graph.
- No automatic escalation to `computer-intel` when the agent is already inside a known repo.
- No broad `.gitignore` takeover. The managed block stays narrow and focused on local agent artifacts, logs, and common test outputs.
- No automatic `codex/...` branch churn as the default local workflow.
- No requirement to merge a Codex worktree branch back before local commits and pushes.

## Team Repo Policy

Use judgment before committing Graphify outputs for shared repos. Local-only graphs are often safer when the graph may churn or when regeneration is not deterministic enough for every contributor.

## Validation And CI

Repo-intel stays inside the normal Agent CLI OS validation surface:

- `python -m unittest discover -s agentctl/tests -p "test_*.py"`
- `python -m unittest discover -s workflow-tools/tests -p "test_*.py"`
- `agentcli maintenance audit --json`

The existing CI workflow already runs the discovery-based Python test commands, so repo-intel does not need a separate workflow to stay gated.

## Tiny AGENTS Contract

The repo-local guidance should stay tiny:

- treat the current repo as the default working universe and use `agentcli computer-intel ...` only when the target repo is unknown or the task is explicitly cross-repo
- run `agentcli repo-intel status`, then `agentcli repo-intel ensure` when a trusted repo is missing, stale, or broken
- if `graphify-out/GRAPH_REPORT.md` exists and repo-intel is healthy, read it before broad raw search
- prefer `agentcli repo-intel query` or `agentcli repo-intel serve` for architecture and path questions, then open only the small set of raw files needed for editing or exact verification
- treat the current local branch as canonical for normal solo work; use worktrees as temporary isolation only
- keep commits and pushes local by default; create a separate branch only when a PR flow or parallel-agent workflow really needs isolation

That is enough. The graph content itself should not be placed in instructions.
