# Agent CLI OS Computer Intel

Use this guide for the machine-wide laptop discovery layer.

## Purpose

Computer-intel gives Agent CLI OS one machine-wide discovery surface for the
whole laptop without collapsing repo-local Graphify graphs into one monolithic
corpus.

The ownership split is deliberate:

- Agent CLI OS owns the machine-wide command surface and registry.
- Repo-intel owns per-repo Graphify state and repair flows.
- Graphify stays per repo or per corpus.
- Obsidian stays a secondary export and browsing layer.

## Public Naming Contract

Use these names on the public surface:

- product: `Agent CLI OS`
- main command: `agentcli`
- repo graph subsystem: `repo-intel`
- machine-wide discovery subsystem: `computer-intel`

Treat these as internal or compatibility-only:

- `agentctl`
- internal `agentctl/` bundle paths
- legacy command aliases

## Layers

### Machine-Wide Discovery

`computer-intel` is the laptop-wide discovery layer.

Canonical file:

- `agentctl/state/computer-graph.json`

This registry is metadata-first. It is for:

- discovered repos
- audit-candidate repos
- trusted repos
- Obsidian vaults
- Graphify outputs
- local service roots
- machine roots and path search

It is not the repo graph itself.

### Per-Repo Graphs

Repo-local Graphify artifacts stay canonical for repo work:

- `graphify-out/graph.json`
- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/graph.html` when generated
- `.graphifyignore`
- `.agentcli/repo-intel.json`

### Obsidian

Obsidian is optional.

- one shared vault root is fine
- one export folder per repo is preferred
- Obsidian is never the source of truth

## Commands

```powershell
agentcli computer-intel status
agentcli computer-intel refresh
agentcli computer-intel search "tenant service"

agentcli repo-intel status --repo C:\path\to\repo
agentcli repo-intel ensure --repo C:\path\to\repo
agentcli repo-intel audit --all-trusted
agentcli repo-intel audit --all-discovered
```

## Search Contract

Use `computer-intel` when the question is about the machine:

- where does this repo live?
- which repo probably owns this service?
- where is the Obsidian vault?
- which folders on the laptop match this name?

Use `repo-intel` when the target repo is already known and the question is
about structure, architecture, paths, or flows inside that repo.

The machine-wide layer should help you find the repo. It should not replace the
repo-local graph once you are inside the repo.

Operationally, `computer-intel` is the exception path:

- current-repo work should stay repo-first
- `computer-intel` should enter only when the target repo is unknown, the task is explicitly cross-repo, or whole-laptop discovery is the point of the task

## Discovery Scope

The default machine-wide scope is the laptop, not only trusted repos.

That means `computer-intel` should discover:

- repos across accessible laptop roots
- Obsidian vaults
- Graphify exports
- service roots such as compose-based directories
- matching file and directory paths during laptop-wide search

The default posture should be whole-laptop, not a tiny sample. Agent CLI OS
keeps the cached machine registry bounded for safety, but `computer-intel search`
also performs a live path scan across the configured laptop roots so the global
search layer can still find machine-wide matches even when the cached registry
was truncated.

Default whole-laptop search settings:

- `scan_scope = "laptop"`
- `directory_budget = 250000`
- `search_limit = 80`
- `live_search_limit = 120`

Safe defaults still matter:

- no mandatory repo mutation
- no giant machine-wide Graphify corpus
- no requirement that every discovered repo is auto-fixed
- no requirement that transient or tooling repos become repo-intel audit targets

## Trusted Versus Discovered Repos

- discovered repos: visible to machine-wide search
- audit-candidate repos: discovered repos that are reasonable repo-intel targets
- trusted repos: allowed to auto-fix through `repo-intel ensure` and
  `repo-intel audit --fix`

Machine-wide discovery can still find transient or tooling repos, for example:

- Codex temp/plugin mirrors
- vendor imports
- package-store clones
- internal worktree scratch paths

Those remain searchable through `computer-intel search`, but `repo-intel audit --all-discovered`
should focus on audit-candidate repos instead of treating every transient repo
as something that needs a graph.

`repo-intel audit --all-discovered --fix` should stay conservative:

- trusted repos may be repaired
- untrusted repos should be reported, not silently mutated

## AGENTS Contract

Keep the machine hint tiny:

- use `agentcli computer-intel search` only when the task is laptop-wide, the target repo is unknown, or the task is explicitly cross-repo
- use `agentcli repo-intel ...` once the target repo is known and stay there by default
- if `graphify-out/GRAPH_REPORT.md` exists and repo-intel is healthy, read it
  before broad raw-file search

That is enough. No machine-wide dump belongs in instructions.
