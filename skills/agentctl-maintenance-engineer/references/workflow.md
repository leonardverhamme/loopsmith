# Agentctl Maintenance Workflow

Primary commands:

- `agentctl maintenance check`
- `agentctl maintenance audit`
- `agentctl maintenance fix-docs`
- `agentctl maintenance render-report`

Primary outputs:

- `docs/agentctl/overview.md`
- `docs/agentctl/command-map.md`
- `docs/agentctl/state-schema.md`
- `docs/agentctl/capability-registry.md`
- `docs/agentctl/cloud-readiness.md`
- `docs/agentctl/maintenance.md`
- `docs/agentctl/maintenance-report.json`
- `.codex-workflows/agentctl-maintenance/state.json`

Use `audit` when:

- command or adapter behavior changed
- plugin packaging changed
- config enablement changed
- the maintenance docs should be fully regenerated

Use `fix-docs` when:

- the machine state is correct and only the generated docs need to be refreshed

Use `render-report` when:

- the maintenance Markdown page and JSON report need a fast refresh without regenerating every doc
