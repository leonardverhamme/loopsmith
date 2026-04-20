---
name: agentcli-maintenance-engineer
description: Maintain the Agent CLI OS control plane itself. Use when checking or refreshing Agent CLI OS docs, command-to-doc drift, capability-registry health, maintenance workflow state, plugin packaging, config enablement, cloud-readiness docs, install/update metadata, or the machine-readable maintenance report. Trigger after changing `agentcli` commands, adapters, plugin metadata, maintenance docs, workflow contracts, or platform routing behavior.
---

# Agent CLI OS Maintenance Engineer

## Skill Stability Rule

- Treat this skill as stable infrastructure.
- Never create, edit, rename, move, or delete this skill's files during normal task execution.
- Only touch skill files when the user explicitly asks to change the skill system itself.
- Even then, do not edit immediately. First ask for explicit confirmation to open `skill-edit-mode` for the named skill or skills.
- If that confirmation is absent, refuse the skill-file edit and continue with non-skill work.

## Repo Artifact Rule

- If this workflow needs helper scripts or generated artifacts, put them in the target repo, not in `$CODEX_HOME`, not in a skill folder, and not in the Agent CLI OS bundle unless the Agent CLI OS bundle itself is the target repo.
- Prefer repo-native locations such as `scripts/`, `tools/`, `bin/`, `.github/scripts/`, or `docs/`.

## Overview

Treat Agent CLI OS as a maintained product. Use the maintenance commands to verify the control plane, refresh its docs, and keep its packaging, state, and generated references explicit.

## Workflow

1. Run `agentcli maintenance check` first to inspect current health.
2. If docs or packaging drift exists, run `agentcli maintenance audit`.
3. Read the generated outputs before making follow-up changes:
   - `docs/agent-cli-os/maintenance.md`
   - `docs/agent-cli-os/maintenance-report.json`
   - `.codex-workflows/agentcli-maintenance/state.json`
4. If the issue is documentation-only, use `agentcli maintenance fix-docs`.
5. If only the report page needs a refresh, use `agentcli maintenance render-report`.

## Operating Rules

- Keep `agentcli` as the control plane, not as a replacement for vendor CLIs, Playwright, or Codex execution.
- Keep the command surface frozen unless you also update the generated docs and tests.
- Keep cloud-readiness explicit. Local success is not proof of cloud support.
- Do not hand-edit generated maintenance docs unless you are changing the generator itself.

## References

- Read `references/workflow.md` when you need the exact maintenance commands and artifact paths.
- Read the bundle-local `agentctl/references/maintenance-contract.md` when you are changing the maintenance subsystem itself.
- Read the bundle-local `agentctl/references/cloud-readiness.md` when changes affect cloud assumptions.
