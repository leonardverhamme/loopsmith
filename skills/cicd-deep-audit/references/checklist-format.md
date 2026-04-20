# Checklist Format

Use a compact, execution-oriented checklist.

## Good Structure

```md
# CI/CD Deep Audit Checklist

## Status

- Unchecked: 9
- Checked: 0

## Pull Request Gates

- [ ] Align lint and typecheck jobs with the actual package scripts
- [ ] Remove duplicated install steps across three workflows

## Release

- [ ] Add explicit artifact handoff between build and deploy jobs
```

## Rules

- Group by automation surface, then workflow or environment.
- Keep each item fixable.
- Only mark an item complete after the workflow change and validation are done.

