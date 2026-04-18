# Runbooks and Commands

Operational docs are only useful if they can be executed.

## Include

- exact command lines
- environment or secret prerequisites
- expected outputs or checkpoints
- recovery or rollback steps where relevant

## Verify Before Writing

- run the command if practical
- or confirm it directly from scripts, package files, CI, or tool config

## Good Runbook Habits

- keep procedures step-based
- separate prerequisites from execution
- link to the owning service or path
- note what to do when a step fails

## Bad Runbook Habits

- vague phrases like "start the app normally"
- unnamed secret requirements
- hidden assumptions about OS, shell, or package manager
