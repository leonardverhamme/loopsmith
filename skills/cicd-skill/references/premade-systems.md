# Proven Systems Behind This Skill

This skill is based on the overlap between official CI docs and current agent workflow guidance.

## GitHub Actions

GitHub's official docs provide the concrete primitives this skill leans on:

- workflow syntax
- reusable workflows
- composite actions
- matrix strategy
- environments and workflow structure

Sources:

- [Workflows and actions reference](https://docs.github.com/en/actions/reference/workflows-and-actions)
- [Reuse workflows](https://docs.github.com/actions/using-workflows/reusing-workflows)
- [Reusing workflow configurations](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations)

## OpenAI Codex

OpenAI's guidance supports keeping tasks well-scoped, using the task queue, and making work verifiable through commands and tests:

- [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- [Introducing Codex](https://openai.com/index/introducing-codex/)

## Claude Code

Claude's docs explicitly position GitHub Actions and CI as a home for recurring automated work, and emphasize practical workflows over giant monolithic prompts:

- [Common workflows](https://code.claude.com/docs/en/common-workflows)
- [Best practices](https://code.claude.com/docs/en/best-practices)

## MCAF

MCAF's public CI/CD skill and framework reinforce:

- repo-native context
- verification as the real gate
- small explicit skills over giant always-on instructions

Sources:

- [MCAF concepts](https://mcaf.managed-code.com/)
- [MCAF skills catalog](https://mcaf.managed-code.com/skills)

