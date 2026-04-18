# Prompt Template

Use this when you want a repeatable session prompt for general UI work in any compatible web repo.

```text
Use $ui-skill for this task.

Task:
[describe the screen, flow, or refactor]

Constraints:
- First inspect this repo's existing design system, primitives, shell patterns, and verification commands.
- Reuse existing component primitives and layout patterns where possible.
- Keep the UI readable, production-oriented, and consistent with the local repo style.
- In server-first frameworks, keep server components as the default and add 'use client' only where interactivity requires it.
- Respect existing i18n, accessibility, and responsive patterns.

Process:
1. Inspect nearby routes, components, styles, and feature modules before editing.
2. Critique the current UI for hierarchy, spacing, contrast, states, mobile behavior, and component reuse.
3. Implement the smallest coherent change.
4. Verify with the repo's lint, typecheck, test, and browser-check commands as appropriate.

Output:
- short critique
- implemented changes
- verification performed
- any remaining UI or accessibility risk
```

For full-app audits, checkbox backlog generation, or execute-until-ready UI remediation, use `$ui-deep-audit` instead of this skill.
