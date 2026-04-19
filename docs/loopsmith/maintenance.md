<!-- loopsmith:auto-generated -->
# Loopsmith Maintenance

## Last Run

- Generated: `2026-04-19T19:51:17.448344+00:00`
- Status: `ok`
- Checks passed: 83 / 83
- Open findings: 0
- Blocked findings: 0

## When to Run Maintenance

- After changing `agentctl` commands, adapters, or state contracts.
- After changing plugin metadata, plugin skills, or packaging layout.
- After adding or removing supported CLIs or browser routes.
- Before trusting cloud-readiness assumptions for a new workflow.

## Operator Runbook

1. Run `loopsmith maintenance check` for a quick signal.
2. If command surface, docs, or packaging changed, run `loopsmith maintenance audit`.
3. Read `maintenance.md`, `maintenance-report.json`, and `.codex-workflows/agentctl-maintenance/state.json` together.
4. Inspect `loopsmith inventory show` when a capability surface looks wrong or unexpectedly large.
5. Inspect `loopsmith self-check` when config, guidance, or menu budgets may be part of the problem.
6. If findings are doc-only, prefer `loopsmith maintenance fix-docs` over hand edits.
7. Re-run the relevant tests and smoke checks before trusting a green maintenance state.

## What Must Be Updated After Changes

- Refresh `docs/loopsmith/*.md` from machine state.
- Keep `agentctl/state/inventory.json` and `agentctl/state/guidance.json` healthy and within budget.
- Review hand-maintained guides such as `README.md`, `zero-touch-setup.md`, `install-on-another-computer.md`, `unattended-worker-setup.md`, `maintainer-guide.md`, and `skill-governance.md` when behavior or setup expectations change.
- Keep `state-schema.md`, `capability-registry.md`, and `maintenance-contract.md` aligned with code.
- Re-run tests for `agentctl` and the shared workflow tools.
- Re-run at least one CLI-level deep-workflow smoke after changing runner/state/guard behavior.
- Keep `AGENTS.md` aligned with the intended front door.
- If the skill surface changes, keep capability wrappers thin and update `skill-governance.md` in the same change.

## Verification Expectations

- `python -m unittest discover -s agentctl/tests -p "test_*.py"` passes.
- `python -m unittest discover -s workflow-tools/tests -p "test_*.py"` passes.
- A temp-repo `loopsmith run <workflow>` smoke can reach a correct terminal state with a real or explicit worker command.
- Fresh bundle install smoke keeps `bootstrap-report.json` truthful and does not fail purely on documented degraded capabilities.

## Clean State Expectations

- `maintenance-report.json` has `status: ok`.
- `.codex-workflows/agentctl-maintenance/state.json` has `status: complete` and `ready_allowed: true`.
- `loopsmith doctor` stays compact and health-focused.
- `loopsmith capabilities` stays capability-first.
- `loopsmith status --all` surfaces durable active workflows and hides stale temp history by default.

## Maintenance Checklist

- [x] No open maintenance findings remain.

## Known Limitations

- `gh skill` is not available locally, so publish/preview wrappers remain disabled.
- `firebase` is detected but intentionally remains detect-only in v1.
- `gcloud` is detected but intentionally remains detect-only in v1.
