# Quality Gates

CI should be a faithful gate, not a separate universe.

## Preferred Gate Order

For most repos:

1. dependency install or restore
2. lint and formatting checks if enforced
3. typecheck or compile check if relevant
4. tests
5. build or package

## Fast vs Slow

- Put fast correctness feedback on pull requests.
- Put heavy packaging, publish, or deployment logic on the events that really need it.
- Keep smoke deploy validation or preview checks close to the deploy step when relevant.

## Avoid

- broad `continue-on-error`
- duplicate installs across jobs without value
- release-only checks blocking every tiny PR unless justified
- pretending a passing workflow is enough when the underlying command is wrong locally
