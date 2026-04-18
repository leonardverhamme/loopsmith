# Proven Systems Behind This Skill

This orchestrator is based on the overlap between official agent guidance and established refactor practice.

## OpenAI Codex

OpenAI's current guidance emphasizes:

- well-scoped tasks
- explicit task queues
- durable repo context in `AGENTS.md`
- verifiable evidence from commands and tests

Sources:

- [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- [Introducing Codex](https://openai.com/index/introducing-codex/)

## Claude Code

Claude's common workflows explicitly treat refactoring as a standard workflow and recommend:

- identify legacy or awkward code first
- refactor to modern patterns while preserving behavior
- verify with tests
- use small, testable increments

Source:

- [Common workflows](https://code.claude.com/docs/en/common-workflows)

## MCAF

MCAF contributes the durable-repo-context and plan-first posture:

- skills stay small and explicit
- architecture and ADR docs live in the repo
- tests and analyzers are the gates
- non-trivial work often benefits from a small plan file

Sources:

- [MCAF concepts](https://mcaf.managed-code.com/)
- [MCAF skills catalog](https://mcaf.managed-code.com/skills)

## Classic Refactor Safety

Martin Fowler remains the clearest foundation for broad refactors:

- preserve behavior
- take small steps
- test frequently

Source:

- [Refactoring article PDF](https://martinfowler.com/distributedComputing/refactoring.pdf)
