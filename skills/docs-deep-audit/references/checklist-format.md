# Checklist Format

Use a compact, execution-oriented checklist.

## Good Structure

```md
# Docs Deep Audit Checklist

## Status

- Unchecked: 12
- Checked: 0

## README

- [ ] Update local setup commands to match package scripts
- [ ] Remove stale environment variable names

## Architecture

- [ ] Refresh the module boundary section for the new API layer
```

## Rules

- Group by doc surface, then file or subsystem.
- Keep each item fixable.
- Only mark an item complete after the doc change and verification are done.
- Keep blocker notes short and factual.
