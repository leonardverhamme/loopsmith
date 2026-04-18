# Prompt Template

## Inspect Only

```text
$refactor-orchestrator
Inspect this repo and identify the highest-value broad refactor candidates, their risks, and the safest sequence. Do not execute changes yet.
```

## Scoped Execution

```text
$refactor-orchestrator
Refactor <subsystem or migration target> in tracked waves. Preserve behavior, keep a compact plan file if needed, validate each wave, and stop only after closeout.
```
