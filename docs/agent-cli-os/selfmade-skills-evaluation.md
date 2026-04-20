# Self-Made Skills Evaluation

Generated from local `plugin-eval analyze` runs over repo-owned skills in `skills/` (excluding `.system`).

- Evaluated skills: **35**
- Average score: **98.3 / 100**
- Grade mix: **A 35**, **B 0**, **C 0**, **D 0**
- Risk mix: **low 23**, **medium 12**, **high 0**

## At A Glance

| Bucket | Skills | Avg score | Notes |
| --- | ---: | ---: | --- |
| Capability front doors | 15 | 100.0 | Stable |
| Everyday workflow skills | 6 | 95.0 | Stable |
| Deep audits | 5 | 98.0 | Stable |
| Control-plane and specialist skills | 9 | 97.8 | Stable |

## Current Lowest Scores

- `agentcli-maintenance-engineer`: **95 / A**, medium risk. Current pressure: trigger_cost_tokens is heavy relative to the current Codex baseline.
- `cicd-skill`: **95 / A**, medium risk. Current pressure: invoke_cost_tokens is heavy relative to the current Codex baseline.
- `context-skill`: **95 / A**, medium risk. Current pressure: trigger_cost_tokens is heavy relative to the current Codex baseline.
- `docs-skill`: **95 / A**, medium risk. Current pressure: deferred_cost_tokens is heavy relative to the current Codex baseline.
- `editskill`: **95 / A**, medium risk. Current pressure: The description does not clearly advertise when the skill should trigger.
- `internet-researcher`: **95 / A**, medium risk. Current pressure: trigger_cost_tokens is heavy relative to the current Codex baseline.
- `refactor-skill`: **95 / A**, medium risk. Current pressure: deferred_cost_tokens is heavy relative to the current Codex baseline.
- `skill-edit-mode`: **95 / A**, medium risk. Current pressure: The description does not clearly advertise when the skill should trigger.

## Capability front doors

| Skill | Score | Grade | Risk | Trigger | Invoke | Deferred | Pressure |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `android-testing-capability` | 100 | A | low | good | good | good | - |
| `autonomous-deep-runs-capability` | 100 | A | low | good | good | good | - |
| `browser-capability` | 100 | A | low | good | good | good | - |
| `figma-capability` | 100 | A | low | good | good | good | - |
| `github-capability` | 100 | A | low | good | good | good | - |
| `github-security-capability` | 100 | A | low | moderate | good | moderate | - |
| `ios-development-capability` | 100 | A | low | good | good | good | - |
| `macos-development-capability` | 100 | A | low | good | good | good | - |
| `nextjs-runtime-capability` | 100 | A | low | good | good | good | - |
| `research-capability` | 100 | A | low | good | good | good | - |
| `sentry-capability` | 100 | A | low | good | good | good | - |
| `skills-management-capability` | 100 | A | low | good | good | good | - |
| `stripe-capability` | 100 | A | low | good | good | good | - |
| `supabase-capability` | 100 | A | low | good | good | good | - |
| `vercel-capability` | 100 | A | low | good | good | good | - |

## Everyday workflow skills

| Skill | Score | Grade | Risk | Trigger | Invoke | Deferred | Pressure |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `cicd-skill` | 95 | A | medium | moderate | heavy | moderate | invoke_cost_tokens is heavy relative to the current Codex baseline. |
| `context-skill` | 95 | A | medium | heavy | moderate | moderate | trigger_cost_tokens is heavy relative to the current Codex baseline. |
| `docs-skill` | 95 | A | medium | moderate | moderate | heavy | deferred_cost_tokens is heavy relative to the current Codex baseline. |
| `refactor-skill` | 95 | A | medium | moderate | moderate | heavy | deferred_cost_tokens is heavy relative to the current Codex baseline. |
| `test-skill` | 95 | A | medium | good | moderate | heavy | deferred_cost_tokens is heavy relative to the current Codex baseline. |
| `ui-skill` | 95 | A | medium | good | heavy | moderate | invoke_cost_tokens is heavy relative to the current Codex baseline. |

## Deep audits

| Skill | Score | Grade | Risk | Trigger | Invoke | Deferred | Pressure |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `cicd-deep-audit` | 100 | A | low | good | moderate | moderate | - |
| `docs-deep-audit` | 100 | A | low | good | moderate | moderate | - |
| `refactor-deep-audit` | 100 | A | low | good | moderate | moderate | - |
| `test-deep-audit` | 95 | A | medium | good | moderate | heavy | deferred_cost_tokens is heavy relative to the current Codex baseline. |
| `ui-deep-audit` | 95 | A | medium | good | heavy | moderate | invoke_cost_tokens is heavy relative to the current Codex baseline. |

## Control-plane and specialist skills

| Skill | Score | Grade | Risk | Trigger | Invoke | Deferred | Pressure |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `github-researcher` | 100 | A | low | moderate | moderate | good | - |
| `loopsmith` | 100 | A | low | moderate | good | good | - |
| `playwright` | 100 | A | low | good | moderate | moderate | - |
| `refactor-orchestrator` | 100 | A | low | moderate | moderate | moderate | - |
| `web-github-scout` | 100 | A | low | moderate | moderate | good | - |
| `agentcli-maintenance-engineer` | 95 | A | medium | heavy | moderate | moderate | trigger_cost_tokens is heavy relative to the current Codex baseline. |
| `editskill` | 95 | A | medium | good | moderate | good | The description does not clearly advertise when the skill should trigger. |
| `internet-researcher` | 95 | A | medium | heavy | moderate | good | trigger_cost_tokens is heavy relative to the current Codex baseline. |
| `skill-edit-mode` | 95 | A | medium | good | moderate | moderate | The description does not clearly advertise when the skill should trigger. |

## Raw Artifacts

- Machine-readable summary: `.tmp-plugin-eval/all-skills-summary.json`
- Per-skill reports: `.tmp-plugin-eval/all-skills/<skill>/report.json`
- Per-skill improvement briefs: `.tmp-plugin-eval/all-skills/<skill>/brief.json`

## Notes

- `plugin-eval` is strongest at static prompt-budget and structural checks. High scores here do not replace real-world task success checks.
- Capability front doors remain strong because they stay thin and navigation-first.
- The main remaining pressure in the catalog is medium-weight trigger or invoke cost on a few specialist or maintenance skills, not failing checks.
