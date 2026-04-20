# Behavior-Preserving Refactors

This skill follows the repeated pattern across Martin Fowler, Claude Code refactor guidance, and OpenAI Codex guidance:

- define the intended behavior first
- make small structural changes
- verify after each step
- avoid mixing feature work into the same change

## Core Rule

If the external behavior changes, it is no longer a pure refactor. Treat that as feature work or a bug fix and document it honestly.

## Safe Sequence

1. State the invariant or user-visible behavior that must remain true.
2. Find the narrowest seam where the code can be improved.
3. Add or tighten tests if the seam has weak coverage.
4. Make one structural change at a time.
5. Run the most relevant checks immediately.
6. Repeat until the local structure is clean enough.

## Good Refactor Units

- extract function, class, hook, or component
- rename symbols for clearer intent
- move code to the module that already owns that responsibility
- split a long conditional or switch into named branches
- replace duplicated logic with one shared path
- invert a dependency so a boundary becomes clearer

## Avoid

- mixing rename, behavior changes, and architecture redesign in one step
- changing more files than needed for a local cleanup
- using "refactor" as cover for speculative redesign

## Source Signals

- Martin Fowler's long-standing guidance emphasizes small steps and testing frequently: [martinfowler.com/distributedComputing/refactoring.pdf](https://martinfowler.com/distributedComputing/refactoring.pdf)
- Claude Code's common refactor workflow explicitly recommends small, testable increments and preserving behavior: [code.claude.com/docs/en/common-workflows](https://code.claude.com/docs/en/common-workflows)
- OpenAI's Codex guidance recommends well-scoped tasks and verifiable output: [openai.com/business/guides-and-resources/how-openai-uses-codex/](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)

