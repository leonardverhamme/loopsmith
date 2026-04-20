# Agent CLI OS Maintenance Workflow

Primary commands:

- `agentcli maintenance check`
- `agentcli maintenance audit`
- `agentcli maintenance fix-docs`
- `agentcli maintenance render-report`

Primary outputs:

- `docs/agent-cli-os/overview.md`
- `docs/agent-cli-os/command-map.md`
- `docs/agent-cli-os/state-schema.md`
- `docs/agent-cli-os/capability-registry.md`
- `docs/agent-cli-os/cloud-readiness.md`
- `docs/agent-cli-os/maintenance.md`
- `docs/agent-cli-os/maintenance-report.json`
- `.codex-workflows/agentcli-maintenance/state.json`

Use `audit` when:

- command or adapter behavior changed
- plugin packaging changed
- config enablement changed
- the maintenance docs should be fully regenerated

Use `fix-docs` when:

- the machine state is correct and only the generated docs need to be refreshed

Use `render-report` when:

- the maintenance Markdown page and JSON report need a fast refresh without regenerating every doc
