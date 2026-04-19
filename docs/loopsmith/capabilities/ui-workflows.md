<!-- loopsmith:auto-generated -->
# UI workflows

- Key: `ui-workflows`
- Group: `workflows`
- Status: `ok`
- Front door: `$ui-skill / $ui-deep-audit`

## Summary

UI workflows

## Navigation Skills

- `ui-skill`
- `ui-deep-audit`

## Entry Points

- `$ui-skill`
- `$ui-deep-audit`
- `loopsmith run ui-deep-audit`

## Backing Interfaces

- `skill` `ui-deep-audit` [ok]
- `skill` `ui-skill` [ok]

## Overlap Policy

- Surface the UI skills first; plugin support stays a backing capability, not a separate menu.
