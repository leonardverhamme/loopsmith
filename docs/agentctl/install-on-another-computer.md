# Install Agentctl On Another Computer

Use this guide when you want to take `agentctl` to a second machine and end up with a working control plane, not just a copied folder.

## Supported Starting Points

You can start from either:

- a package install via `pipx install git+https://github.com/leonardverhamme/agentctl.git`
- a Git clone of the public repo
- an extracted release bundle zip such as `agentctl-v1.0.0.zip`

In both cases, the important requirement is that the extracted folder still contains:

- `agentctl/`
- `workflow-tools/`
- `skills/`
- `plugins/agentctl/`
- `docs/agentctl/`
- `scripts/install_bundle.py`

## Recommended Prerequisites

For a healthy install, the machine should have:

- Python 3.12 or later
- Node.js and `npx`
- a Chromium-compatible browser route if you want browser-backed verification

Optional but commonly useful:

- `gh`
- `vercel`
- `supabase`

`agentctl` will still install without every optional CLI, but `agentctl doctor` and `agentctl capabilities` will report what is missing or degraded.

## Install From A Clone

From the repo root:

```powershell
python .\scripts\install_bundle.py
```

If you want a non-default target:

```powershell
python .\scripts\install_bundle.py --codex-home C:\Users\you\.codex
```

## Install From The Terminal As A Package

If you want a user-facing CLI on PATH first, install the bootstrap wrapper:

```powershell
pipx install git+https://github.com/leonardverhamme/agentctl.git
agentctl bootstrap
agentctl doctor
```

If you are bootstrapping from an existing local checkout instead of downloading the public archive:

```powershell
agentctl bootstrap --source-root C:\path\to\agentctl
```

After bootstrap, the same `agentctl` command delegates into the installed bundle in your `CODEX_HOME`.

## Install From A Release Bundle

1. Extract the zip somewhere writable.
2. Open a terminal in the extracted folder.
3. Run:

```powershell
python .\scripts\install_bundle.py
```

The installer copies the bundle into the target `CODEX_HOME`, enables the plugin, and writes the bootstrap report against that exact target.

## What The Installer Does

The installer:

- copies `agentctl`, `workflow-tools`, `skills`, `plugins`, and `docs/agentctl` into the target `CODEX_HOME`
- enables the `agentctl` plugin in `config.toml`
- writes `agentctl/state/bootstrap-report.json`
- runs:
  - `agentctl doctor --json`
  - `agentctl capabilities --json`
  - `agentctl maintenance audit --json`

If those post-install checks are not `ok`, read the bootstrap report before trusting the machine.

## First Verification Pass

After install, run:

```powershell
agentctl.cmd doctor
agentctl.cmd capabilities
agentctl.cmd maintenance audit
```

If you prefer direct Python entry:

```powershell
python %CODEX_HOME%\agentctl\agentctl.py doctor
python %CODEX_HOME%\agentctl\agentctl.py capabilities
python %CODEX_HOME%\agentctl\agentctl.py maintenance audit
```

On macOS or Linux:

```bash
sh "$CODEX_HOME/agentctl.sh" doctor
sh "$CODEX_HOME/agentctl.sh" capabilities
sh "$CODEX_HOME/agentctl.sh" maintenance audit
```

## What To Check Before Declaring The Machine Ready

- `doctor` should be compact and not report control-plane failure.
- `capabilities` should show the expected capability menu.
- `maintenance audit` should end with `status: ok`.
- `docs/agentctl/maintenance-report.json` should exist in the installed `CODEX_HOME`.
- `.codex-workflows/agentctl-maintenance/state.json` should say `complete` with `ready_allowed: true`.

## If Browser Verification Is Required

If you plan to use UI or browser-backed test workflows, verify the browser route on that machine:

```powershell
$env:AGENTCTL_RUN_BROWSER_SMOKE="1"
$env:AGENTCTL_BROWSER="msedge"
python -m unittest discover -s agentctl/tests -p "test_browser_smoke.py"
```

If this fails because the browser route is missing, install a Chromium-compatible route before trusting UI or Playwright-heavy workflows.

## If Deep Loops Must Run Unattended

Installing the bundle is not enough by itself. A deep workflow only runs unattended when it can relaunch a real worker.

Read [unattended-worker-setup.md](unattended-worker-setup.md) next and configure one of:

- `--worker-command`
- `CODEX_WORKFLOW_WORKER_COMMAND`
- `AGENTCTL_CODEX_WORKER_TEMPLATE`

Without that, the loop metadata is present but the worker runtime is still manual.

## Machine-Local Versus Repo-Local Data

Keep this distinction clear:

- `CODEX_HOME` contains the installed control plane and its generated control-plane docs
- the target repo contains the real deep-workflow state, checklists, and any helper scripts created for that repo

Do not put task-specific helper scripts into `CODEX_HOME` unless the `agentctl` bundle repo itself is the target project.

## Good Final State

The machine is ready when all of these are true:

- `agentctl` commands run from the installed location
- the plugin is enabled
- the maintenance state is green
- the capability menu reflects the local machine honestly
- browser-backed verification is healthy if you need it
- unattended worker routing is configured if you need loops to keep going without chat repetition
