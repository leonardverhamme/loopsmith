# loopsmith Maintainer Guide

Use this when changing the control plane itself.

## Source Of Truth Split

Generated docs:

- `docs/loopsmith/overview.md`
- `docs/loopsmith/command-map.md`
- `docs/loopsmith/state-schema.md`
- `docs/loopsmith/capability-registry.md`
- `docs/loopsmith/cloud-readiness.md`
- `docs/loopsmith/maintenance.md`
- `docs/loopsmith/maintenance-report.json`

Do not hand-maintain those. Change the code and rerun maintenance.

Hand-maintained docs:

- `README.md`
- `docs/loopsmith/zero-touch-setup.md`
- `docs/loopsmith/install-on-another-computer.md`
- `docs/loopsmith/unattended-worker-setup.md`
- `docs/loopsmith/skill-governance.md`
- this file

## What To Update

If command surface or routing changes:

- `agentctl/`
- generated docs via `loopsmith maintenance audit`
- `README.md`

If install or upgrade logic changes:

- `agentctl/bootstrap.py`
- `agentctl/bundle_install.py`
- `scripts/install_bundle.py`
- `scripts/build_release_bundle.py`
- release workflows
- setup docs

If capability groups or skill front doors change:

- `agentctl/lib/capabilities.py`
- generated capability pages
- `AGENTS.md`
- `docs/loopsmith/skill-governance.md`
- related tests

## Minimum Validation

```powershell
python -m unittest discover -s agentctl/tests -p "test_*.py"
python -m unittest discover -s workflow-tools/tests -p "test_*.py"
python agentctl/agentctl.py maintenance audit --json
python -m build --sdist --wheel --outdir dist
python scripts/build_release_bundle.py --version v0.0.0-test --output-dir dist
```

For installability:

```powershell
python scripts/install_bundle.py --codex-home <temp dir>
```

## Release Expectations

Tagged releases should:

- build wheel and sdist
- build the `loopsmith-bundle-<version>.zip`
- publish GitHub release assets
- publish the Python package to PyPI
- keep bootstrap and upgrade working from released artifacts

## Maintainability Contract

- keep the top-level capability menu small
- keep thin capability skills short and navigation-first
- put detail in generated pages and docs, not in every `SKILL.md`
- fail maintenance if removed sidecar-app coupling reappears in the product surface
