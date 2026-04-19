<!-- loopsmith:auto-generated -->
# Testing workflows

- Key: `test-workflows`
- Group: `workflows`
- Status: `ok`
- Front door: `$test-skill / $test-deep-audit`

## Summary

Testing workflows

## Navigation Skills

- `test-skill`
- `test-deep-audit`

## Entry Points

- `$test-skill`
- `$test-deep-audit`
- `loopsmith run test-deep-audit`

## Backing Interfaces

- `skill` `test-deep-audit` [ok]
- `skill` `test-skill` [ok]

## Overlap Policy

- Collapse testing transports behind one testing surface; use repo-native CLIs and Playwright first.
