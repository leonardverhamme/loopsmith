<!-- agent-cli-os:auto-generated -->
# Computer intelligence

- Key: `computer-intelligence`
- Group: `core`
- Status: `ok`
- Front door: `agentcli computer-intel`

## Summary

Use for machine-wide discovery of repos, vaults, Graphify outputs, services, and laptop-wide path search without replacing repo-local graph traversal.

## Entry Points

- `agentcli computer-intel status`
- `agentcli computer-intel refresh`
- `agentcli computer-intel search`

## Routing Notes

- Treat `agentcli computer-intel ...` as the exception path, not the default repo workflow.
- Start with `agentcli computer-intel status` or `agentcli computer-intel refresh` only when the task is about the whole laptop rather than one repo.
- Use `agentcli computer-intel search` for laptop-wide discovery, then switch to `agentcli repo-intel ...` once the target repo is known.
- The machine-wide index is metadata-first and should not replace per-repo Graphify graphs for architecture questions.

## Overlap Policy

- Keep the machine-wide laptop discovery layer separate from per-repo Graphify graphs. Use the global index for whole-computer discovery and repo selection, then drop into repo-intel for repo-specific graph work.
