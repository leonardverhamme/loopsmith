# loopsmith Zero-Touch Setup

Use this when you want an agent or operator to get to a working install with the fewest possible steps.

## Fast Path

```powershell
pipx install git+https://github.com/leonardverhamme/loopsmith.git
loopsmith bootstrap
loopsmith doctor --fix
```

That is the canonical public setup path.

## What Bootstrap Does

- installs the bundle into `CODEX_HOME`
- keeps the internal bundle under `agentctl/`
- enables the `loopsmith` plugin in `config.toml`
- writes install metadata to `agentctl/state/install-metadata.json`
- runs post-install checks against the exact target `CODEX_HOME`

Post-install checks include:

- `loopsmith doctor --json`
- `loopsmith capabilities --json`
- `loopsmith maintenance audit --json`
- `loopsmith self-check --json`

## Local Development Bootstrap

If you are working from a local checkout:

```powershell
loopsmith bootstrap --source-root C:\path\to\loopsmith
```

Use `--source-root` only for local development. Public installs should prefer release artifacts.

## After Bootstrap

Run:

```powershell
loopsmith doctor --fix
loopsmith capabilities
loopsmith self-check
```

The install is in good shape when:

- `doctor` reports `ok` or only documented optional degradation
- `capabilities` shows the grouped top-level menu
- `self-check` reports matching wrapper, bundle, and config health
- `docs/loopsmith/maintenance-report.json` exists in `CODEX_HOME`

## Config Layers

`loopsmith` uses:

1. bundled defaults
2. `$CODEX_HOME/config.toml`
3. `<repo>/.loopsmith/config.toml`

Use `loopsmith config show` to inspect the merged result.

## Worker Runtime

Deep workflows only count as unattended when a real worker route exists.

Use one of:

- the auto-detected Codex CLI
- `--worker-command`
- `CODEX_WORKFLOW_WORKER_COMMAND`
- `AGENTCTL_CODEX_WORKER_TEMPLATE`

Read [unattended-worker-setup.md](unattended-worker-setup.md) before treating deep loops as fully autonomous.

## Script Placement Rule

Task-specific helper scripts belong in the target repo being worked on.

They do not belong in:

- `CODEX_HOME`
- the `loopsmith` bundle repo unless it is the active target repo
- `skills/`
- `plugins/*/skills/`
