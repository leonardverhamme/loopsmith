# loopsmith Skill Governance

Use this guide when creating or changing local control-plane skills.

## Core Rule

One thin local skill per meaningful capability or workflow.

Not:

- one skill per raw command
- one skill per MCP method
- one skill per tiny variant

## Expected Shape

A good local capability skill should:

- be short
- be navigation-first
- route into `loopsmith capability <key>`
- avoid duplicating runtime logic

## Menu Budgets

Default maintenance budgets:

- max 8 top-level capability groups
- max 9 items per group page
- thin capability skills should stay within their line budget and remain navigation-first

If a new capability would overflow a group, split the menu shape before adding more flat items.

## Where Detail Belongs

- routing logic and health: `agentctl/lib/capabilities.py`
- generated docs: `docs/loopsmith/capabilities/`
- natural-language operator guidance: `README.md` and `docs/loopsmith/*.md`
- visible front door: the skill itself

Do not put long manuals into thin capability skills.

## Required Follow-Up When Skills Change

Update:

- `agentctl/lib/capabilities.py`
- generated docs via `loopsmith maintenance audit`
- `AGENTS.md`
- tests

Use `$skill-edit-mode` only when skill work is explicitly approved.
