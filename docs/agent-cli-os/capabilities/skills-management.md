<!-- agent-cli-os:auto-generated -->
# Skills management

- Key: `skills-management`
- Group: `core`
- Status: `ok`
- Front door: `$skills-management-capability`

## Summary

Use for listing, adding, checking, and safely updating installed skills and their provenance.

## Navigation Skills

- `skills-management-capability`

## Entry Points

- `$skills-management-capability`
- `agentcli capability skills-management`
- `agentcli skills list`
- `agentcli skills add`
- `agentcli skills check`
- `agentcli skills update`

## Routing Notes

- Use the capability skill first so the agent stays on the thin wrapper path instead of bypassing the official skills tooling.
- Keep installs pinned and provenance-aware rather than treating `skills update` as an uncontrolled bulk sync.

## Backing Interfaces

- `skill` `skills-management-capability` [ok]
- `tool` `npx` [ok]
- `tool` `skills` [ok]

## Overlap Policy

- Wrap official skills tooling rather than reimplementing it.
