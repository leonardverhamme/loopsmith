# Install loopsmith On Another Computer

Use this when you want a second machine to end up with a working install, not just a copied folder.

## Recommended Path

```powershell
pipx install git+https://github.com/leonardverhamme/loopsmith.git
loopsmith bootstrap
loopsmith doctor --fix
```

## From A Local Checkout

```powershell
git clone https://github.com/leonardverhamme/loopsmith.git
cd loopsmith
python .\scripts\install_bundle.py --codex-home C:\Users\you\.codex
```

Or:

```powershell
loopsmith bootstrap --source-root C:\path\to\loopsmith
```

## Required Surface

The machine should have:

- Python 3.12+
- Node.js and `npx`

Recommended:

- a Chromium-capable browser route for Playwright-backed work
- optional vendor CLIs such as `gh`, `vercel`, and `supabase`

`loopsmith` will report missing optional tools honestly rather than pretending they are healthy.

## What To Verify

Run:

```powershell
loopsmith doctor --fix
loopsmith capabilities
loopsmith self-check
loopsmith maintenance audit
```

Good state:

- install metadata exists at `agentctl/state/install-metadata.json`
- `maintenance audit` returns `ok`
- generated docs exist under `docs/loopsmith/`
- the plugin is enabled
- the grouped capability menu renders cleanly

## Deep Loops

If the second machine must run unattended deep workflows, also configure a real worker route.

See [unattended-worker-setup.md](unattended-worker-setup.md).
