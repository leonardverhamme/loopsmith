---
name: "playwright"
description: "Use when a task needs real browser automation from the terminal through the local Playwright wrapper: navigation, snapshots, clicks, forms, screenshots, data extraction, or UI-flow debugging."
---

# Playwright CLI Skill

## Stability

- Treat this skill as stable infrastructure.
- Do not edit this skill unless the user explicitly opens `$editskill` for it.

## Repo artifacts

- Put helper scripts, snapshots, and browser artifacts in the target repo, not in `$CODEX_HOME` and not in a skill folder.

Drive a real browser from the terminal using the wrapper first. Treat this skill as CLI-first automation; do not pivot to `@playwright/test` unless the user explicitly asks for test files.

## Prerequisite check

Before proposing commands, check whether `npx` is available:

```bash
command -v npx >/dev/null 2>&1
```

If it is not available, pause and ask the user to install Node.js/npm. Provide these steps verbatim:

```bash
# Verify Node/npm are installed
node --version
npm --version

# If missing, install Node.js/npm, then:
npm install -g @playwright/cli@latest
playwright-cli --help
```

Once `npx` is present, proceed with the wrapper script.

## Skill path

PowerShell / Windows:

```powershell
$env:PWCLI = if (Get-Command playwright.cmd -ErrorAction SilentlyContinue) {
  "playwright.cmd"
} elseif (Test-Path ".\\agentctl\\playwright.cmd") {
  (Resolve-Path ".\\agentctl\\playwright.cmd").Path
} elseif ($env:CODEX_HOME -and (Test-Path (Join-Path $env:CODEX_HOME "agentctl\\playwright.cmd"))) {
  (Join-Path $env:CODEX_HOME "agentctl\\playwright.cmd")
} else {
  throw "No playwright wrapper found on PATH, in ./agentctl, or in `$CODEX_HOME\\agentctl."
}
```

Fallback Bash path:

```bash
if command -v playwright.cmd >/dev/null 2>&1; then
  export PWCLI="playwright.cmd"
elif [ -x "./skills/playwright/scripts/playwright_cli.sh" ]; then
  export PWCLI="./skills/playwright/scripts/playwright_cli.sh"
else
  export PWCLI="./agentctl/playwright.cmd"
fi
```

## Quick start

```bash
"$PWCLI" open https://playwright.dev --headed
"$PWCLI" snapshot
"$PWCLI" click e15
"$PWCLI" type "Playwright"
"$PWCLI" press Enter
"$PWCLI" screenshot
```

## Core workflow

1. Open the page.
2. Snapshot to get stable element refs.
3. Interact using refs from the latest snapshot.
4. Re-snapshot after navigation or significant DOM changes.
5. Capture artifacts when useful.
6. If the browser route is locked or stale, start a fresh CLI session instead of stopping.
7. If the current app port is unavailable or already occupied, rerun the app on another free port and continue there.

## Snapshot again after

- navigation
- substantial UI changes
- opening or closing modals or menus
- tab switches

Refs go stale. When a command fails because a ref is missing, snapshot again.

## Common patterns

### Form fill and submit

```bash
"$PWCLI" open https://example.com/form --headed
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "password123"
"$PWCLI" click e3
"$PWCLI" snapshot
"$PWCLI" screenshot
```

### Debug a UI flow with traces

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" tracing-start
# ...interactions...
"$PWCLI" tracing-stop
```

### Multi-tab work

```bash
"$PWCLI" tab-new https://example.com
"$PWCLI" tab-list
"$PWCLI" tab-select 0
"$PWCLI" snapshot
```

## References

Open only what you need:

- CLI command reference: `../../docs/agent-cli-os/skill-support/playwright/cli.md`
- Practical workflows and troubleshooting: `../../docs/agent-cli-os/skill-support/playwright/workflows.md`

## Guardrails

- Always snapshot before referencing element ids like `e12`.
- Re-snapshot when refs seem stale.
- Prefer explicit commands over `eval` and `run-code` unless needed.
- When you do not have a fresh snapshot, use placeholder refs like `eX` and say why; do not bypass refs with `run-code`.
- Use `--headed` when a visual check will help.
- When capturing artifacts in this repo, use `output/playwright/` and avoid introducing new top-level artifact folders.
- Default to CLI commands and workflows, not Playwright test specs.
- Do not stop because another Playwright session has the MCP or browser route locked; open a fresh CLI-driven browser session and continue.
- Do not treat the first chosen localhost port as fixed; if the app is runnable and the port is blocked, switch to another free port and finish the verification.
