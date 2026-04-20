# Agent CLI OS Maintenance Contract

The maintenance subsystem treats the public `Agent CLI OS` control plane as a maintained product.

Canonical outputs:

- Human docs: `../../docs/agent-cli-os/*.md`
- Machine report: `../../docs/agent-cli-os/maintenance-report.json`
- Machine state: `../../.codex-workflows/agentcli-maintenance/state.json`

Required maintenance commands:

- `agentcli maintenance check`
- `agentcli maintenance audit`
- `agentcli maintenance fix-docs`
- `agentcli maintenance render-report`

Checks covered in v1:

- command surface docs exist and remain auto-generated
- required reference docs exist
- local plugin packaging exists and matches the expected plugin name
- plugin router skill exists
- plugin enablement is explicit in `config.toml`
- maintenance skill exists
- platform test files exist
- capability health remains visible

Exit intent:

- `ok`: no open findings remain
- `degraded`: warnings remain, but the control plane still works
- `error`: blocking maintenance findings exist and the platform should not be trusted blindly
