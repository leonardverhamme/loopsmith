# Scope Control

This skill exists because most refactor tasks should stay small.

## Use This Skill When

- the work fits in one bounded area
- the goal is cleanup, modernization, extraction, or naming improvement
- validation can stay local

## Escalate to `$refactor-orchestrator` When

- the change spans many modules or packages
- there are phased migrations or temporary compatibility paths
- a checklist or plan file is needed to track waves
- the refactor will likely touch many call sites over time

## Task Framing

Frame refactor work like a well-scoped issue:

- target files or subsystem
- intended invariant
- known quality gates
- what should explicitly not change

## Why This Matters

OpenAI's Codex guidance repeatedly recommends well-scoped tasks and a lightweight queue rather than giant ambiguous assignments:

- [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- [Introducing Codex](https://openai.com/index/introducing-codex/)

