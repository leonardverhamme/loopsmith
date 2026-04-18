# Premade Stack

Use this reference when choosing already-made tools or skill packs instead of inventing everything from scratch.

## Highest-Trust Official Pieces

### Playwright CLI

- Best current browser CLI layer for coding-agent workflows
- CLI-first and token-efficient
- Can install local skills

Source:
- https://playwright.dev/docs/getting-started-cli

### Playwright MCP

- Best when you truly need iterative browser reasoning over accessibility snapshots
- Not the default when CLI is enough

Source:
- https://playwright.dev/docs/next/getting-started-mcp

### Anthropic webapp-testing

- Useful premade webapp-testing skill for local web apps
- Strong on server lifecycle, DOM inspection, screenshots, and browser logs
- Better as a webapp/browser companion than as a complete test strategy

Sources:
- https://github.com/anthropics/skills
- https://officialskills.sh/anthropics/skills/webapp-testing

## Strong Community Packs

### TestMu AI or LambdaTest agent skills

- Broad premade testing library covering frameworks and cloud execution
- Best when you want many testing-framework skills fast
- Treat as a library of focused skills, not as the only testing strategy

Sources:
- https://www.testmuai.com/support/docs/selenium-agent-skills/
- https://www.testmuai.com/support/docs/browser-cloud-skills/

### TestDino Playwright Skill

- Broad Playwright-focused guide pack with many installable guides
- Useful as a reference or add-on when you want deeper Playwright-specific patterns

Source:
- https://testdino.com/blog/playwright-skill/

## Recommended Local Pattern

For Codex, the best setup is still:

1. one general testing skill
2. one deep audit skill
3. existing local `$playwright` skill for browser smoke and CLI-first automation
4. repo-native test CLIs as the source of truth

Do not replace that with one mega external skill pack.
