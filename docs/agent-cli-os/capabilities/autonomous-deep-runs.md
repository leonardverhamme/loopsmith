<!-- agent-cli-os:auto-generated -->
# Autonomous deep runs

- Key: `autonomous-deep-runs`
- Group: `core`
- Status: `ok`
- Front door: `$autonomous-deep-runs-capability`

## Summary

Use for launching, resuming, and diagnosing unattended deep workflows through the shared runner.

## Navigation Skills

- `autonomous-deep-runs-capability`

## Entry Points

- `$autonomous-deep-runs-capability`
- `agentcli capability autonomous-deep-runs`
- `agentcli run <workflow>`
- `CODEX_WORKFLOW_WORKER_COMMAND`
- `AGENTCTL_CODEX_WORKER_TEMPLATE`

## Routing Notes

- Start with the capability skill, then route into `agentcli run <workflow>`.
- A real worker command or `AGENTCTL_CODEX_WORKER_TEMPLATE` is still required for unattended execution.

## Backing Interfaces

- `skill` `autonomous-deep-runs-capability` [ok]
- `tool` `codex` [ok]

## Overlap Policy

- The outer execute-until-done loop must use a real worker command, not chat memory. Prefer Codex runtime when it is callable or explicitly templated.
