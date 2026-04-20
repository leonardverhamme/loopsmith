<!-- agent-cli-os:auto-generated -->
# Agent CLI OS maintenance

- Key: `agentcli-maintenance`
- Group: `core`
- Status: `ok`
- Front door: `$agentcli-maintenance-engineer`

## Summary

Use for control-plane maintenance, generated docs refreshes, machine-state audits, packaging drift, and maintenance-report regeneration.

## Navigation Skills

- `agentcli-maintenance-engineer`

## Entry Points

- `agentcli maintenance check`
- `agentcli maintenance audit`
- `agentcli maintenance fix-docs`

## Routing Notes

- Start with `$agentcli-maintenance-engineer` when the Agent CLI OS control plane itself changed or looks suspect.
- Use `agentcli maintenance audit` to refresh the generated docs, state, and maintenance report together instead of hand-editing generated files.

## Backing Interfaces

- `plugin` `agent-cli-os` [ok] (enabled=true)
- `skill` `agentcli-maintenance-engineer` [ok]

## Overlap Policy

- Keep maintenance as one capability surface for docs, packaging, registry health, and platform drift.
