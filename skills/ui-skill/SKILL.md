---
name: ui-skill
description: Use when building or refactoring dense React, Next.js, Tailwind, or shadcn/ui product screens, flows, and overview pages that need compact, production-grade UI. Not for full-app checklist audits; use ui-deep-audit.
---

# UI Skill

## Visible Skill Usage

- When this skill is actively being used in chat, mention `$ui-skill` once in a user-visible update so the human can see the highlighted route.
- Keep that mention short and do not repeat it in every paragraph.

## Skill Stability Rule

- Treat this skill as stable infrastructure.
- Do not edit, rename, move, or delete this skill during normal task work.
- Only touch skill files when the user explicitly asks for skill maintenance and explicitly opens `$editskill` for the named skills.

## Repo Artifact Rule

- Put helpers and verification artifacts in the target repo, not in `$CODEX_HOME`, not in a skill folder, and not in the Agent CLI OS repo unless that repo is the target.

## Use This Skill For

- Page and flow implementation, UI refactors, dense internal tools, compact overview surfaces, and product-like AI conversation UI.

Use `$ui-deep-audit` instead for full-app audits, checklist execution, or execute-until-ready UI remediation.

## Default Posture

- Prefer dense, calm, table-first product UI.
- Keep one main task per screen.
- Keep one compact header band whenever possible.
- Use structure, labels, counters, tabs, badges, and state chips before prose.
- Keep charts secondary to the data model.
- Make summaries and analytics earn their height.
- Preserve coherent local patterns before inventing new ones.

## Required Workflow

1. Inspect the repo first:
   - `package.json`, `components.json`, global styles, tokens, layouts, shell components, representative screens, and verification commands
2. Load the references you actually need:
   - Always: `../../docs/agent-cli-os/skill-support/ui/design-tokens.md`, `../../docs/agent-cli-os/skill-support/ui/component-rules.md`, `../../docs/agent-cli-os/skill-support/ui/a11y-gates.md`, `../../docs/agent-cli-os/skill-support/ui/ui-checklist.md`
   - Dense product surfaces: `../../docs/agent-cli-os/skill-support/ui/dense-product-ui.md`
   - Dashboard, overview, or analytics surfaces: `../../docs/agent-cli-os/skill-support/ui/dashboard-charts.md`
   - AI assistant surfaces: `../../docs/agent-cli-os/skill-support/ui/ai-conversation-ui.md`
   - Final review: `../../docs/agent-cli-os/skill-support/ui/ui-review.md`
   - Pattern lookup only: `../../docs/agent-cli-os/skill-support/ui/ui-examples.md`, `../../docs/agent-cli-os/skill-support/ui/ui-anti-patterns.md`
   - Next.js App Router only: `../../docs/agent-cli-os/skill-support/ui/nextjs-guardrails.md`
3. Critique before generating:
   - page type, density, copy volume, hierarchy, header height, and whether the surface should really be a table, form, chart, chat, or detail page
4. Implement with repo primitives:
   - reuse the existing primitive layer, keep route files thin, preserve server and client boundaries, and extend existing variants before creating wrappers
5. Run a real browser pass with `$browser-capability` and `$playwright` when the UI can run locally.
6. Review before stopping:
   - loading, empty, success, error, disabled, desktop, and narrow viewport states
   - density, spacing, borders, radius, and scanability
   - copy that should be removed instead of polished

## Dashboard And Overview Rules

- On operator, CRUD, and workbench pages, the main table, form, queue, or workflow surface should usually appear in the first viewport.
- Keep top chrome compact. Prefer one dense header band over stacked title, breadcrumb, tab, filter, stat, and action bars.
- Treat more than two stacked top bars as a defect unless the page has a strong structural reason.
- Treat a tall KPI strip, hero band, or top chart that pushes the main work below the fold as a defect on non-analytics-first pages.
- Use `references/dashboard-charts.md` for concrete chart height, border, legend, overflow, and first-viewport checks.

## Hard Rules

- Do not add intro paragraphs to operator, dashboard, queue, CRUD, or settings pages unless the user explicitly asked for editorial guidance.
- Do not add charts without analytical reason.
- Do not let top-of-page summary cards or charts dominate the first viewport on workbench pages.
- Do not wrap tables and forms in unnecessary cards.
- Do not stack multiple topbars when one compact band can hold the title, status, actions, filters, and tabs.
- Do not default to oversized radii, pill buttons, or wrapper piles.
- Do not call runnable UI work done without a real browser pass.
- Do not stop at "Playwright was busy"; use the CLI wrapper, a fresh browser session, or another free app port and finish the verification.

## References

- `../../docs/agent-cli-os/skill-support/ui/design-tokens.md`
- `../../docs/agent-cli-os/skill-support/ui/component-rules.md`
- `../../docs/agent-cli-os/skill-support/ui/a11y-gates.md`
- `../../docs/agent-cli-os/skill-support/ui/dense-product-ui.md`
- `../../docs/agent-cli-os/skill-support/ui/dashboard-charts.md`
- `../../docs/agent-cli-os/skill-support/ui/ai-conversation-ui.md`
- `../../docs/agent-cli-os/skill-support/ui/ui-review.md`
- `../../docs/agent-cli-os/skill-support/ui/ui-examples.md`
- `../../docs/agent-cli-os/skill-support/ui/ui-anti-patterns.md`
- `../../docs/agent-cli-os/skill-support/ui/ui-checklist.md`
- `../../docs/agent-cli-os/skill-support/ui/nextjs-guardrails.md` when the repo is Next.js App Router
- `../../docs/agent-cli-os/skill-support/ui/prompt-template.md` when the user wants a reusable session prompt
