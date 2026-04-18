---
name: agentctl-router
description: Route Codex work through agentctl when the task is about capability discovery, research routing, maintenance, or deep workflow launch. Use when the user needs to know what tools exist, which interface is healthy, how to start or resume a deep workflow, or which research route should be used before implementation.
---

# Agentctl Router

## Overview

Use `agentctl` as the first door for control-plane questions and long-running workflow launch. Keep the source of truth in the underlying skills, vendor CLIs, Playwright, and Codex runtime.

## Routing Rules

- Use `agentctl doctor` or `agentctl capabilities` to inspect what is installed and healthy.
- Use `agentctl research web|github|scout` for evidence-driven research before implementation.
- Use `agentctl run <workflow>` for deep workflows such as `ui-deep-audit` or `test-deep-audit`.
- Use `agentctl maintenance ...` when the control plane itself may have drifted.

## Do Not Do

- Do not reinvent vendor CLI logic inside the skill.
- Do not bypass the shared workflow state contract for deep workflows.
- Do not assume cloud support from local success. Use the explicit cloud-readiness docs.
