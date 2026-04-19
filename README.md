# loopsmith

`loopsmith` is a capability-first Codex control plane for long-running agent work.

It gives agents one stable front door for:

- capability discovery
- deep workflow launch and resume
- research routing
- install health
- upgrade and maintenance

It does not replace the authoritative tools underneath. It routes into them.

## 5-Minute Setup

Install the public wrapper:

```powershell
pipx install git+https://github.com/leonardverhamme/loopsmith.git
```

Bootstrap the real bundle into your `CODEX_HOME`:

```powershell
loopsmith bootstrap
```

Repair common setup issues and confirm health:

```powershell
loopsmith doctor --fix
```

That is the main onboarding path.

`loopsmith` is the canonical public command. `agentctl` still works as a compatibility alias for the current migration release.

## What You Get

- `loopsmith` as the public wrapper command
- the internal `agentctl/` bundle under `CODEX_HOME`
- reusable local skills for UI, tests, docs, refactor, CI/CD, research, and maintenance
- a local plugin shell for Codex routing
- deep workflow state under `.codex-workflows/<workflow>/state.json`

## Core Commands

```text
loopsmith doctor --fix
loopsmith capabilities
loopsmith capability <key>
loopsmith status --all
loopsmith run <workflow>
loopsmith research web <query>
loopsmith research github <query>
loopsmith research scout <query>
loopsmith config show
loopsmith self-check
loopsmith upgrade
loopsmith maintenance audit
```

## Examples

Install on the current machine:

```powershell
pipx install git+https://github.com/leonardverhamme/loopsmith.git
loopsmith bootstrap
loopsmith doctor --fix
```

Install on another computer from a local checkout:

```powershell
git clone https://github.com/leonardverhamme/loopsmith.git
cd loopsmith
python .\scripts\install_bundle.py --codex-home C:\Users\you\.codex
```

Bootstrap from a local checkout during development:

```powershell
loopsmith bootstrap --source-root C:\path\to\loopsmith
```

Run a deep workflow:

```powershell
loopsmith run docs-deep-audit --repo C:\path\to\repo
```

Upgrade later:

```powershell
loopsmith upgrade
loopsmith self-check
```

## Config Layers

`loopsmith` uses a small structured config system with clear precedence:

1. bundled defaults
2. user-global config at `$CODEX_HOME/config.toml`
3. repo-local config at `<repo>/.loopsmith/config.toml`

Use:

```powershell
loopsmith config show
loopsmith config path --scope user
loopsmith config set worker.mode auto
loopsmith config set browser.preferred_route cli --scope repo --repo C:\path\to\repo
loopsmith config unset browser.preferred_route --scope repo --repo C:\path\to\repo
```

Structured config is intentionally small. Use `AGENTS.md` for natural-language guidance.

## Grouped Capability Navigation

The default capability menu is grouped so the top-level surface stays small:

- Core
- Workflows
- Research
- Platforms
- Browser & Design
- Native

Use:

```powershell
loopsmith capabilities
loopsmith capability platforms
loopsmith capability github-advanced-security
```

The detailed routing notes live in generated capability pages under `docs/loopsmith/capabilities/`.

## Deep Workflows

Bundled deep workflows:

- `ui-deep-audit`
- `test-deep-audit`
- `docs-deep-audit`
- `cicd-deep-audit`
- `refactor-deep-audit`

Each workflow is disk-backed:

- checklist or progress markdown in the target repo
- machine state in `.codex-workflows/<workflow>/state.json`

For unattended execution, the loop still needs a real worker route. `loopsmith` supports:

- `--worker-command`
- `CODEX_WORKFLOW_WORKER_COMMAND`
- `AGENTCTL_CODEX_WORKER_TEMPLATE`
- a callable standalone Codex CLI when auto-detected

## Install and Upgrade Model

The public wrapper is installable as a Python package.

The real bundle is installed into `CODEX_HOME` by `loopsmith bootstrap` and upgraded by `loopsmith upgrade`.

Install metadata is written to:

```text
agentctl/state/install-metadata.json
```

That metadata lets upgrades use the recorded source and version channel instead of guessing.

## Compatibility

This release intentionally keeps:

- the internal Python package name as `agentctl`
- the internal bundle directory as `agentctl/`
- `agentctl` as a compatibility command alias

That keeps existing installs and repo assumptions stable while the public product name changes to `loopsmith`.

## Documentation Map

- [docs/loopsmith/overview.md](docs/loopsmith/overview.md)
- [docs/loopsmith/zero-touch-setup.md](docs/loopsmith/zero-touch-setup.md)
- [docs/loopsmith/install-on-another-computer.md](docs/loopsmith/install-on-another-computer.md)
- [docs/loopsmith/unattended-worker-setup.md](docs/loopsmith/unattended-worker-setup.md)
- [docs/loopsmith/maintainer-guide.md](docs/loopsmith/maintainer-guide.md)
- [docs/loopsmith/skill-governance.md](docs/loopsmith/skill-governance.md)

## Release Model

- Python package: `loopsmith`
- canonical repo: `https://github.com/leonardverhamme/loopsmith`
- GitHub Releases carry the versioned bundle zip used by `bootstrap` and `upgrade`
- tagged releases build wheel, sdist, bundle zip, checksum, and publish to PyPI

## Maintenance

Treat the control plane as a maintained product:

```powershell
loopsmith maintenance audit
loopsmith self-check
```

The maintenance pass refreshes generated docs, checks plugin/config health, enforces grouped-menu budgets, and blocks reintroduced sidecar-app coupling in the product surface.
