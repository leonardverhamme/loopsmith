# Release Safety

Shipping automation should reduce risk, not just reduce clicks.

## Basic Safety Moves

- use explicit environments for staging and production where supported
- keep promotion and deploy triggers intentional
- document rollback or re-run paths
- keep artifact boundaries explicit if one job builds and another deploys
- use concurrency controls when duplicate deploys would be harmful

## Secrets and Permissions

- pass only the secrets each workflow or job really needs
- prefer least-privileged token permissions
- do not guess environment names or secret keys

## When to Stay Manual

Keep steps manual if the repo lacks:

- a clear environment model
- secret ownership
- rollback confidence
- agreement on automatic deploy triggers
