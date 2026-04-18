# ADR Patterns

Use an ADR when the repo needs a durable record of a technical decision, trade-off, or policy shift.

## Good ADR Scope

- choosing one architecture pattern over another
- changing a core dependency or platform
- introducing a major data model or contract change
- setting a policy with long-term impact

## Keep ADRs Short

Typical structure:

1. Title and status
2. Context
3. Decision
4. Consequences
5. Links to affected code, docs, or follow-up ADRs

## ADR Rules

- one decision per record
- write the rationale, not just the conclusion
- state the trade-offs
- keep implementation detail secondary unless it explains the choice

## Proven Templates

- [Architectural Decision Records](https://adr.github.io/)
- [MADR](https://adr.github.io/madr/)
- [joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)

## Practical Use

If the user changed code but did not actually make a durable design decision, do not force an ADR.
