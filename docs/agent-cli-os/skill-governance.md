# Agent CLI OS Control-Plane Governance

Use this guide when creating or changing local control-plane skills, menus, or routing metadata.

## Core Model

Keep three layers separate:

- raw autodetected inventory
- curated capability menu
- thin front-door skills

Do not collapse those into one flat surface.

## Front-Door Skill Rule

One thin local skill per meaningful capability or workflow.

Not:

- one skill per raw command
- one skill per MCP method
- one skill per vendor subcommand variant

`$loopsmith` remains the one intentional generic exception. It is only the front door for durable long-task loops and should continue to route into `agentcli loop <name>`.

## Menu Rules

Default maintenance budgets:

- max 8 top-level capability groups
- max 25 items per menu bucket
- names-first output by default

If a raw bucket would exceed `25`, split it deterministically before surfacing it.

Do not promote newly detected CLIs, MCP servers, plugin skills, or installed skills into the default capability menu automatically.

## Garbage Prevention

Assume every extra visible item has a real cost:

- more prompt clutter
- more routing ambiguity
- more maintenance drift
- more room for agents to overuse the wrong interface

So default to:

- fewer top-level names
- shorter `SKILL.md` files
- names-first menus
- drill-down pages for detail
- raw inventory for diagnostics only

If a new surface makes the default experience noisier without making the route clearer, it is probably the wrong shape.

## Where Detail Belongs

- raw installed surface: `agentctl/state/inventory.json`
- curated routing and health: `agentctl/lib/capabilities.py`
- generated docs: `docs/agent-cli-os/capabilities/` and `docs/agent-cli-os/inventory.md`
- user-facing quickstart: `README.md`
- thin visible front door: the local skill itself

Do not put long manuals into thin capability skills.

## Personal Guidance Rules

Use structured config to point to small guidance snippet directories.

Do not:

- embed long personal instructions into config values
- grow `SKILL.md` files into personal preference dumps
- use repo skills as the default place for private user guidance

Keep guidance within the configured file-count and total-line budgets so the control plane stays compact.

When users want long-lived personal preferences, prefer:

- one small snippet for routing preferences
- one small snippet for output style
- one small snippet for repo-specific exceptions

Do not let personal guidance turn into another hidden system prompt.

## Required Follow-Up When The Surface Changes

Update:

- `agentctl/lib/capabilities.py`
- inventory or guidance logic when the change affects detected surface or budgets
- generated docs via `agentcli maintenance audit`
- `AGENTS.md`
- tests

Use `$editskill` when skill work is explicitly approved. `$skill-edit-mode` remains a legacy alias only.

