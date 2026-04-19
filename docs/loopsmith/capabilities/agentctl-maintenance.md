<!-- loopsmith:auto-generated -->
# Loopsmith maintenance

- Key: `agentctl-maintenance`
- Group: `core`
- Status: `ok`
- Front door: `$agentctl-maintenance-engineer`

## Summary

Loopsmith maintenance

## Navigation Skills

- `agentctl-maintenance-engineer`

## Entry Points

- `loopsmith maintenance check`
- `loopsmith maintenance audit`
- `loopsmith maintenance fix-docs`

## Backing Interfaces

- `plugin` `loopsmith` [ok] (enabled=true)
- `skill` `agentctl-maintenance-engineer` [ok]

## Overlap Policy

- Keep maintenance as one capability surface for docs, packaging, registry health, and platform drift.
