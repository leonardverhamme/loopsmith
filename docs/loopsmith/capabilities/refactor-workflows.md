<!-- loopsmith:auto-generated -->
# Refactor workflows

- Key: `refactor-workflows`
- Group: `workflows`
- Status: `ok`
- Front door: `$refactor-skill / $refactor-deep-audit`

## Summary

Refactor workflows

## Navigation Skills

- `refactor-skill`
- `refactor-deep-audit`
- `refactor-orchestrator`

## Entry Points

- `$refactor-skill`
- `$refactor-deep-audit`
- `$refactor-orchestrator`
- `loopsmith run refactor-deep-audit`

## Backing Interfaces

- `skill` `refactor-deep-audit` [ok]
- `skill` `refactor-orchestrator` [ok]
- `skill` `refactor-skill` [ok]

## Overlap Policy

- Use the local refactor skills as the capability surface; do not split by underlying tooling.
