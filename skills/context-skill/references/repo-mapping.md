# Repo Mapping

Use this reference when creating or refreshing repo maps and architecture overviews.

## What To Map

- top-level folders and what lives in them
- app entrypoints and startup commands
- test, lint, typecheck, build, and run commands
- backend and frontend boundaries
- data, queue, cache, and external integration boundaries
- key shell, layout, routing, or service entrypoints
- where new code should usually go

## Good Output Shape

- short repo overview
- key commands
- module or layer map
- common file targets
- known traps or non-obvious conventions

## Good Targets

- `docs/Architecture.md`
- `docs/RepoMap.md`
- onboarding sections in README when the repo is small

## Source Notes

- Anthropic’s common workflows emphasize codebase understanding, tracing flows, and onboarding through direct questions:
  - https://code.claude.com/docs/en/tutorials
- Microsoft’s Deep Wiki plugin is a strong example of generating repo maps, onboarding guides, `Agents.md`, and llms docs from code:
  - https://microsoft.github.io/skills/
  - https://github.com/guaijie/deepwiki
- MCAF architecture-overview shows the value of a navigational `docs/Architecture.md`:
  - https://mcaf.managed-code.com/skills
