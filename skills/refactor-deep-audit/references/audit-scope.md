# Audit Scope

Use this skill when a repo needs a structural cleanup campaign, especially an older codebase with accumulated design debt.

## Cover These Areas

- overly long files and functions
- duplicated logic and parallel implementations
- tangled responsibilities and mixed concerns
- unstable module boundaries and dependency cycles
- outdated abstractions, adapters, or compatibility paths
- poor separation between domain, IO, UI, and orchestration layers
- call-site sprawl that makes migrations risky

## Look For

- files that are hard to reason about or test
- recurring patterns that should be extracted or normalized
- repeated code that wants one owner
- seams missing around side effects or integrations
- places where architecture docs no longer match the code

## Good Outcome

The repo becomes easier to navigate, safer to extend, and more LLM-friendly without turning into a speculative rewrite.

