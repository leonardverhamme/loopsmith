# Audit Scope

Use this skill when a repo's automation surface needs a full sweep.

## Cover These Areas

- CI workflow files and job structure
- release and deployment automation
- local commands versus CI commands
- lint, typecheck, test, build, package, and deploy gates
- reusable workflows, composite actions, and copy-paste workflow debt
- matrix usage, concurrency, cache usage, and artifact flow
- permissions, environments, manual approvals, and rollback guidance

## Look For

- slow or duplicated workflows without good reason
- missing or weak quality gates
- pipeline commands that drift from the real repo scripts
- unsafe deploy or release paths
- unclear environment promotion or rollback handling
- hidden assumptions about secrets and infrastructure
