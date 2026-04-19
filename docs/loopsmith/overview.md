<!-- loopsmith:auto-generated -->
# Loopsmith Overview

## Purpose

`loopsmith` is the thin Codex-first control plane for capability discovery, routing, health checks, deep-workflow launch, and machine-readable state.

## Layers

1. Repo guidance in `AGENTS.md` and a small set of stable docs.
2. Skills for repeated workflows such as UI, testing, refactor, docs, research, and maintenance.
3. `loopsmith` as the runtime control plane above those skills and above authoritative vendor interfaces.
4. Plugin packaging so the system can be installed and surfaced consistently.

## Current Status

- Maintenance status: `ok`
- Checks passed: 75 / 75
- Open findings: 0
- Blocked findings: 0

## First Things To Read

- `loopsmith doctor` for a compact health check.
- `loopsmith capabilities` for the grouped top-level capability menu.
- `loopsmith capability <key>` for a group page or a single capability drill-down page.
- `loopsmith status --all` for durable workflow state across repos.
- `loopsmith maintenance audit` after command, packaging, config, or contract changes.

## Manual Guides

- [Zero-touch setup](zero-touch-setup.md)
- [Install on another computer](install-on-another-computer.md)
- [Unattended worker setup](unattended-worker-setup.md)
- [Maintainer guide](maintainer-guide.md)
- [Skill governance](skill-governance.md)

## Common Flows

- Capability discovery: `loopsmith doctor` then `loopsmith capabilities`.
- External research: `loopsmith research web|github|scout <query>`.
- Deep remediation: `loopsmith run <workflow>` plus `.codex-workflows/<workflow>/state.json`.
- Control-plane upkeep: `$agentctl-maintenance-engineer` or `loopsmith maintenance audit`.

## Compatibility

- `loopsmith` is the canonical public command.
- `agentctl` remains a compatibility alias for the current migration release.
- The internal bundle path stays `agentctl/` for this release to avoid a risky filesystem and import break.

## Verified Guarantees

- Shared runner coverage exists for `complete`, `blocked`, and `stalled` terminal states.
- The CLI front door is covered end-to-end with `loopsmith run ...` and `loopsmith status --json` in temp repos.
- Fresh installs are smoke-tested and allowed to finish `ok` when only degraded-but-documented optional capabilities remain.
- The remaining environment-sensitive piece is the worker runtime itself; unattended runs still require a real callable worker route.

## Key Files

- Internal bundle path: `agentctl/`
- Capabilities snapshot: `agentctl/state/capabilities.json`
- Maintenance report: `docs/loopsmith/maintenance-report.json`
- Maintenance state: `.codex-workflows/agentctl-maintenance/state.json`

## What Loopsmith Does Not Own

- It does not replace the official `skills` CLI or `gh skill`.
- It does not replace vendor CLIs such as `gh`, `vercel`, or `supabase`.
- It does not replace Playwright as the browser runtime.
- It does not replace Codex execution or cloud environments.

## Known Limitations

- `gh skill` is not available locally, so publish/preview wrappers remain disabled.
- `firebase` is detected but intentionally remains detect-only in v1.
- `gcloud` is detected but intentionally remains detect-only in v1.
