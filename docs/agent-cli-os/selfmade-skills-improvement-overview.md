# Self-Made Skills Improvement Overview

This page focuses on the skills that were weak before the rewrite pass and shows what changed after the pass.

## Before

- Average score before: **93.9 / 100**
- Grade mix before: **A 26**, **B 3**, **C 4**, **D 2**
- High-risk skills before: **6**

## Skills That Were Not Good

| Skill | Before | Why it was weak | After | Delta |
| --- | ---: | --- | ---: | ---: |
| `test-deep-audit` | 67 (D) | trigger_cost_tokens is excessive relative to the current Codex baseline. | 95 (A) | +28 |
| `test-skill` | 67 (D) | trigger_cost_tokens is excessive relative to the current Codex baseline. | 95 (A) | +28 |
| `docs-deep-audit` | 72 (C) | trigger_cost_tokens is excessive relative to the current Codex baseline. | 100 (A) | +28 |
| `playwright` | 81 (C) | deferred_cost_tokens is excessive relative to the current Codex baseline. | 100 (A) | +19 |
| `refactor-deep-audit` | 81 (C) | trigger_cost_tokens is excessive relative to the current Codex baseline. | 100 (A) | +19 |
| `ui-skill` | 81 (C) | deferred_cost_tokens is excessive relative to the current Codex baseline. | 95 (A) | +14 |
| `cicd-deep-audit` | 91 (B) | trigger_cost_tokens is heavy relative to the current Codex baseline. | 100 (A) | +9 |
| `refactor-skill` | 91 (B) | trigger_cost_tokens is heavy relative to the current Codex baseline. | 95 (A) | +4 |
| `ui-deep-audit` | 91 (B) | invoke_cost_tokens is heavy relative to the current Codex baseline. | 95 (A) | +4 |

## After

- Average score after: **98.3 / 100**
- Grade mix after: **A 35**, **B 0**, **C 0**, **D 0**
- High-risk skills after: **0**

## What Changed

- Deep-audit skills were shortened so their trigger text and invoked bodies no longer dominate the budget.
- `$ui-skill`, `$ui-deep-audit`, and `$playwright` kept their context, but bulky support material was moved out of the hot skill folder into `docs/agent-cli-os/skill-support/` so the front door stays compact.
- `$editskill` and `$skill-edit-mode` now explicitly route substantial skill rewrites through plugin-eval before and after changes.

## Biggest Score Gains

- `docs-deep-audit`: 72 -> 100 (+28)
- `test-deep-audit`: 67 -> 95 (+28)
- `test-skill`: 67 -> 95 (+28)
- `playwright`: 81 -> 100 (+19)
- `refactor-deep-audit`: 81 -> 100 (+19)
- `ui-skill`: 81 -> 95 (+14)
- `cicd-deep-audit`: 91 -> 100 (+9)
- `refactor-skill`: 91 -> 95 (+4)
- `ui-deep-audit`: 91 -> 95 (+4)
