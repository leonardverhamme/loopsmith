# Workflow Reuse and Matrix

Use reuse to remove duplication, not to hide clarity.

## Reusable Workflows

Use a reusable workflow when:

- multiple workflows repeat the same full job shape
- the same build or validation flow is reused across repos or triggers
- inputs, secrets, and outputs can be made explicit

Use a composite action when:

- you want to reuse a smaller bundle of steps within a job

## Matrix Strategy

Use a matrix when the repo truly supports multiple:

- runtimes
- OS targets
- versions
- packages or deploy targets

Avoid matrix expansion when it only slows CI without meaningful extra signal.

## Official References

- [Reuse workflows](https://docs.github.com/actions/using-workflows/reusing-workflows)
- [Avoiding duplication in workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/avoiding-duplication)

## Practical Rule

Prefer the smallest reusable unit that reduces copy-paste without making debugging harder.

