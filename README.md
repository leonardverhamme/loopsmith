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
loopsmith inventory show
loopsmith status --all
loopsmith run <workflow>
loopsmith loop <name> --task "<brief>"
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

Run a generic long task through the durable loop:

```powershell
loopsmith loop repo-cleanup --repo C:\path\to\repo --task "Reduce stale scripts, tighten docs, add missing tests, and keep going until the checklist is empty."
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

Default structured keys now cover:

- worker runtime defaults
- browser route preference
- compact menu behavior
- raw inventory refresh behavior
- personal guidance snippet directories and budgets

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
loopsmith inventory show --kind tools --scope all
```

`loopsmith capabilities` is the curated compact front door.

`loopsmith inventory show` is the raw autodetected surface for debugging and inspection when the curated menu is not enough.

The detailed routing notes live in generated capability pages under `docs/loopsmith/capabilities/`.

Default menu budgets:

- max 8 top-level groups
- max 25 items per menu bucket before deterministic splitting
- names-first output by default

## Why This Stays Small

`loopsmith` is intentionally split into three layers:

- raw autodetected inventory
- curated capability menu
- thin visible front-door skills

That separation is the main token-efficiency rule.

It prevents the default route from becoming a giant flat dump of:

- every installed skill
- every plugin-contributed skill
- every MCP server
- every CLI on the machine

The default menu stays compact because:

- newly detected tools are not promoted automatically
- raw inventory lives behind `loopsmith inventory show`
- top-level output is names-first instead of paragraph-first
- personal guidance is budgeted instead of appended into skills
- thin skills stay navigation-first and push detail into docs and drill-down pages

## Raw Inventory

`loopsmith` now persists the raw autodetected inventory to:

```text
agentctl/state/inventory.json
```

That snapshot includes:

- machine CLIs
- globally installed skills
- repo-scoped skills when present
- installed/configured plugins
- configured MCP servers

Use:

```powershell
loopsmith inventory refresh
loopsmith inventory show --kind all --scope all
loopsmith inventory item tool:gh
```

This is intentionally separate from the curated capability menu.

## Personal Guidance Snippets

Small personal guidance snippets can now be referenced through structured config instead of bloating skills or prompts.

By default, `loopsmith` validates:

- max guidance files
- max total guidance lines

The compact guidance snapshot is stored at:

```text
agentctl/state/guidance.json
```

This keeps private user preferences out of:

- capability skills
- repo skills
- giant inline config blobs

The goal is better routing with less prompt clutter, not another hidden prompt dump.

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

When there is no dedicated deep workflow for the job, use the generic `$loopsmith` skill plus:

```powershell
loopsmith loop <name> --repo C:\path\to\repo --task "<brief>"
```

That loop uses the same runner contract, but stores its queue under `docs/<name>-checklist.md`, `docs/<name>-progress.md`, and `.codex-workflows/<name>/state.json`.

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
- [docs/loopsmith/inventory.md](docs/loopsmith/inventory.md)

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

When changing the source repo itself, run maintenance from the source tree, not through an already installed bundle:

```powershell
python -m agentctl.agentctl maintenance audit --json
```

That source-tree command now refreshes the checked-in docs directly and refuses to retarget maintenance writes outside the real loopsmith repo root.
