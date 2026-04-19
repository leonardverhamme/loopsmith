# Agentctl Capability Registry

`agentctl capabilities` is the curated capability registry for the control plane.

Canonical file:

- `../state/capabilities.json`
- `../state/inventory.json` is the raw autodetected source that feeds this curated registry

Top-level shape:

- `schema_version`
- `generated_at`
- `codex_home`
- `summary`
- `installed_skills`
- `local_skills`
- `plugins`
- `mcp_servers`
- `tools`
- `capabilities`
- `overlap_analysis`
- `detect_only_tools`

Interpretation rules:

- Treat `capabilities[*].front_door` as the default route for that capability.
- Treat the raw inventory as the installed surface and the capability registry as the compact default menu.
- Treat `capabilities[*].backing_interfaces` as supporting metadata, not the primary menu.
- Treat `overlap_analysis` as the collapse policy for overlapping plugin, CLI, skill, and MCP routes.
- Treat `tools.*.status` as current local health, not cloud readiness.
- Treat `detect_only_tools` as intentionally detect-only until a repeated workflow justifies a richer adapter.
- Refresh this registry through `agentctl doctor` or `agentctl capabilities`, not by hand.
