# Playwright CLI Reference

Use the preferred global wrapper unless the CLI is already installed globally:

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
"$env:PWCLI" --help
```

Fallback Bash wrapper:

```bash
if command -v playwright.cmd >/dev/null 2>&1; then
  export PWCLI="playwright.cmd"
elif [ -x "./skills/playwright/scripts/playwright_cli.sh" ]; then
  export PWCLI="./skills/playwright/scripts/playwright_cli.sh"
else
  export PWCLI="./agentctl/playwright.cmd"
fi
"$PWCLI" --help
```

Optional convenience alias:

```bash
alias pwcli="$PWCLI"
```

## Core

```bash
pwcli open https://example.com
pwcli close
pwcli snapshot
pwcli click e3
pwcli dblclick e7
pwcli type "search terms"
pwcli press Enter
pwcli fill e5 "user@example.com"
pwcli drag e2 e8
pwcli hover e4
pwcli select e9 "option-value"
pwcli upload ./document.pdf
pwcli check e12
pwcli uncheck e12
pwcli eval "document.title"
pwcli eval "el => el.textContent" e5
pwcli dialog-accept
pwcli dialog-accept "confirmation text"
pwcli dialog-dismiss
pwcli resize 1920 1080
```

## Navigation

```bash
pwcli go-back
pwcli go-forward
pwcli reload
```

## Keyboard

```bash
pwcli press Enter
pwcli press ArrowDown
pwcli keydown Shift
pwcli keyup Shift
```

## Mouse

```bash
pwcli mousemove 150 300
pwcli mousedown
pwcli mousedown right
pwcli mouseup
pwcli mouseup right
pwcli mousewheel 0 100
```

## Save as

```bash
pwcli screenshot
pwcli screenshot e5
pwcli pdf
```

## Tabs

```bash
pwcli tab-list
pwcli tab-new
pwcli tab-new https://example.com/page
pwcli tab-close
pwcli tab-close 2
pwcli tab-select 0
```

## DevTools

```bash
pwcli console
pwcli console warning
pwcli network
pwcli run-code "await page.waitForTimeout(1000)"
pwcli tracing-start
pwcli tracing-stop
```

## Sessions

Use a named session to isolate work:

```bash
pwcli --session todo open https://demo.playwright.dev/todomvc
pwcli --session todo snapshot
```

Or set an environment variable once:

```bash
export PLAYWRIGHT_CLI_SESSION=todo
pwcli open https://demo.playwright.dev/todomvc
```

