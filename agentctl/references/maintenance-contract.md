# Agentctl Maintenance Contract

The maintenance subsystem treats `agentctl` as a maintained product.

Canonical outputs:

- Human docs: `../../docs/agentctl/*.md`
- Machine report: `../../docs/agentctl/maintenance-report.json`
- Machine state: `../../.codex-workflows/agentctl-maintenance/state.json`

Required maintenance commands:

- `agentctl maintenance check`
- `agentctl maintenance audit`
- `agentctl maintenance fix-docs`
- `agentctl maintenance render-report`

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
