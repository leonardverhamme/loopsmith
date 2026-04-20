# Proven Systems Behind This Skill

This skill is intentionally not invented from scratch. Its shape comes from a few systems that keep repeating the same reliable habits.

## Official and High-Trust Sources

### OpenAI Codex

- Keep repo context durable in `AGENTS.md`
- Give the agent well-scoped tasks
- Use task queues and verifiable checks instead of giant prompts

Sources:

- [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- [Introducing Codex](https://openai.com/index/introducing-codex/)

### Claude Code

- Refactor code as a standard workflow
- Prefer small, testable increments
- Verify after the change

Source:

- [Common workflows](https://code.claude.com/docs/en/common-workflows)

### MCAF

- Keep skills small and explicit
- Keep durable engineering context in the repo
- Use tests and analyzers as the gates
- Treat architecture and ADRs as repo-native context, not chat-only memory

Sources:

- [MCAF concepts](https://mcaf.managed-code.com/)
- [MCAF skills catalog](https://mcaf.managed-code.com/skills)

## Classic Refactor Foundation

Martin Fowler's guidance remains the most stable baseline for safe refactoring:

- preserve behavior
- take small steps
- test frequently

Source:

- [Refactoring article PDF](https://martinfowler.com/distributedComputing/refactoring.pdf)

## What This Skill Borrows

- small, behavior-preserving steps
- explicit scoping
- validation after each step
- repo-native commands over invented ones
- structural cleanup without broad speculative redesign

