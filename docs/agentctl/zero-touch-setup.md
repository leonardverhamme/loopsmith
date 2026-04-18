# Zero-Touch Setup

This bundle is designed so an agent can set it up with one command and then use the installed control plane without further user interaction.

## One-Command Bootstrap

From a clone or extracted release bundle:

```powershell
python .\scripts\install_bundle.py
```

That command:

- installs the bundle into `$CODEX_HOME` or `~/.codex`
- enables the `agentctl-platform` plugin in `config.toml`
- runs the post-install checks against that exact target `CODEX_HOME`
- runs:
  - `agentctl doctor --json`
  - `agentctl capabilities --json`
  - `agentctl maintenance audit --json`
- writes a machine-readable bootstrap report to:
  - `agentctl/state/bootstrap-report.json`

If you want to target a specific Codex home:

```powershell
python .\scripts\install_bundle.py --codex-home C:\Users\you\.codex
```

## What The Agent Should Do After Bootstrap

1. Run `agentctl doctor`
2. Run `agentctl capabilities`
3. Use `agentctl` as the first front door for:
   - capability discovery
   - research routing
   - deep workflow launch
   - maintenance checks

## Script Placement Rule

When an installed skill or workflow needs to create helper scripts for a user task, those scripts belong in the target repo being worked on, not in:

- `$CODEX_HOME`
- the `agentctl-platform` bundle repo
- any skill directory under `skills/`
- any plugin skill directory under `plugins/*/skills/`

Use the repo's own `scripts/`, `tools/`, or another repo-local path that matches the project structure.

## Existing Environment Discovery

The installed control plane discovers what is already present and healthy on the machine. It does not require the user to pre-classify tools by transport.

It looks across:

- installed skills
- enabled plugins
- configured MCP servers
- available CLIs
- workflow state already present in the repo

and then surfaces those as capabilities.
