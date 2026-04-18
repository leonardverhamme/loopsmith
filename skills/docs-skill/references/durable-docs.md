# Durable Docs

Good engineering docs reduce repeated re-discovery. They should be concise, navigable, and grounded in the code.

## Put Docs in the Right Home

- `README.md`: entrypoint, setup, and basic usage
- `docs/Architecture.md`: system map, modules, boundaries, major flows
- `docs/ADR/`: one decision per record
- runbooks: operational procedures, failure handling, release or recovery steps
- feature docs: local flow, contracts, and user-facing behavior for one area

## Good Durable Docs

- name the real commands
- link to the real paths
- explain boundaries, not just implementations
- age well across code changes

## Bad Durable Docs

- giant essays nobody can scan
- duplicated setup steps in three places
- stale commands copied from old commits
- speculative docs for workflows that do not exist yet

## Source Signals

- Claude Code has a dedicated documentation workflow and emphasizes checking docs against project standards: [code.claude.com/docs/en/common-workflows](https://code.claude.com/docs/en/common-workflows)
- OpenAI Codex guidance emphasizes persistent repo context in `AGENTS.md` plus repo-native docs: [openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- MCAF treats durable docs and architecture maps as part of the repo's operating system for agents: [mcaf.managed-code.com](https://mcaf.managed-code.com/)
