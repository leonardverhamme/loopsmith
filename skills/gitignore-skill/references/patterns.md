# Ignore Pattern Guide

Use this guide to choose safe `.gitignore` rules.

## Common Local Junk Classes

### Local agent and workflow state

- `.agentcli/`
- `.codex-workflows/`
- `.playwright-cli/`
- local scratch folders such as `.tmp/`, `tmp/`, `temp/`

These are usually safe to ignore when they exist only to support local agent work.

### Browser, test, and coverage output

- `playwright-report/`
- `test-results/`
- `coverage/`
- framework-specific local reports and screenshots
- `*.log`, `logs/`

Prefer directory rules over broad extension rules when possible.

### Build and package output

- `dist/`
- `build/`
- framework caches such as `.next/`, `.turbo/`
- local virtual environments such as `.venv/`, `venv/`
- language caches such as `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `__pycache__/`

These are common ignore candidates, but verify repo intent first. Some repos commit built artifacts deliberately.

### Graph and tooling output

- `graphify-out/`
- tool-generated reports
- exported local dashboards or temporary analysis bundles

Only ignore these when they are local working output, not when the repo intentionally checks them in.

## Safe Pattern Selection

- Prefer exact directories first: `playwright-report/`
- Then prefer narrow path globs: `output/playwright/`
- Use extension globs only when the entire class is truly disposable: `*.log`
- Avoid repo-wide globs that can hide source-of-truth files

## Things To Treat Carefully

- lockfiles
- fixtures
- migrations
- seeds
- checked-in snapshots
- docs exports that are part of the repo contract
- screenshots or test baselines intentionally stored in version control

These are not junk by default.
