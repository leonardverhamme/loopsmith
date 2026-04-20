---
name: loopsmith
description: Route very long or multi-step repo work into the loopsmith disk-backed loop. Use when a task is too large for chat-memory-only execution, when another skill needs a durable outer loop, or when a repo-specific checklist and state file should drive work until it is truly done.
---

# Loopsmith

## Skill Stability Rule

- Treat this skill as stable infrastructure.
- Never create, edit, rename, move, or delete this skill during normal task execution.
- Only touch skill files when the user explicitly asks to change the skill system itself and has confirmed `skill-edit-mode`.

## Use This For

- Large tasks that need many validated batches
- Work that should survive chat drift through disk-backed state
- Cases where another skill needs a durable outer loop instead of manual prompting

## Workflow

1. If a dedicated deep workflow already exists, prefer it first:
   - `agentcli run ui-deep-audit`
   - `agentcli run test-deep-audit`
   - `agentcli run docs-deep-audit`
   - `agentcli run refactor-deep-audit`
   - `agentcli run cicd-deep-audit`
2. If the task is novel or cross-cutting, write a concise task brief to disk or pass it inline.
3. Launch the generic loop with `agentcli loop <name> --task-file <path>` or `agentcli loop <name> --task "<brief>"`.
4. Let the outer runner own:
   - `.codex-workflows/<name>/state.json`
   - `docs/<name>-checklist.md`
   - `docs/<name>-progress.md`
5. Use `agentcli status --repo <path>` to inspect progress and resume from disk, not from chat memory.

## Rules

- Do not keep the queue only in chat.
- Do not fake completion after one batch if unchecked items remain.
- Keep the checklist stable and actionable enough for the next pass to resume.
- Use one coherent validated batch per pass and let the outer runner continue.
- If the work is blocked, leave the items unchecked and record the blocker instead of pretending the loop is done.

