<!-- agent-cli-os:auto-generated -->
# Repo intelligence

- Key: `repo-intelligence`
- Group: `core`
- Status: `ok`
- Front door: `agentcli repo-intel`

## Summary

Use for per-repo graph health, repo-first graph routing, managed `.gitignore` hygiene, ensure/update flows, graph-backed repo queries, and workspace-wide trusted-repo audits.

## Entry Points

- `agentcli repo-intel status`
- `agentcli repo-intel ensure`
- `agentcli repo-intel update`
- `agentcli repo-intel query`
- `agentcli repo-intel audit`
- `agentcli repo-intel serve`

## Routing Notes

- When the agent is already inside a repo, keep that repo as the working universe and start with `agentcli repo-intel status` or `agentcli repo-intel ensure` before broad raw-file search.
- Trusted repos should default to `agentcli repo-intel ensure` when repo-intel, repo hygiene, or graph freshness drift appears so graph-first retrieval stays the normal path.
- Use `agentcli repo-intel query` for focused graph traversal and `agentcli repo-intel serve` when an MCP client should talk to the local graph directly.
- Use `agentcli computer-intel ...` only when the target repo is unknown or the task is explicitly cross-repo.
- Do not treat the workspace registry as the repo graph itself; it is an index-of-indexes over trusted repos.

## Backing Interfaces

- `tool` `graphify` [ok]

## Overlap Policy

- Keep repo intelligence as a CLI-first subsystem. Graphify is the indexing engine, Obsidian is a secondary export/view layer, and AGENTS guidance should stay a tiny routing hint only.
