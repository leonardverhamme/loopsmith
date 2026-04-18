# AGENTS And Context

Use this reference when deciding what belongs in `AGENTS.md` versus other repo docs.

## Core Rule

`AGENTS.md` should contain durable operating rules, not every detail about the repo.

## Put In `AGENTS.md`

- naming conventions
- command entrypoints
- verification rules
- important repo quirks
- file-location guidance that repeatedly matters
- constraints Codex cannot infer safely

## Keep Out Of `AGENTS.md`

- long architecture explanations
- page-by-page feature docs
- stale task-specific notes
- large examples better stored in normal docs

## Good Companion Docs

- `docs/Architecture.md` for module boundaries and system shape
- `docs/RepoMap.md` or similar for file-finding and key entrypoints
- runbooks for local startup, release, or incident workflows

## Source Notes

- OpenAI Codex recommends `AGENTS.md` for persistent repo guidance:
  - https://openai.com/index/introducing-codex/
  - https://openai.com/business/guides-and-resources/how-openai-uses-codex/
- MCAF explicitly treats context plus AGENTS plus repo docs as the durable system:
  - https://mcaf.managed-code.com/
