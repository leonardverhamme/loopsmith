# Architecture Overview

An architecture overview should help a new engineer or agent navigate the system quickly.

## What It Should Contain

- major modules or services
- boundaries and ownership
- core request or data flows
- integration points and contracts
- where to start for the most common kinds of changes

## What It Should Not Become

- a full design book
- a duplicate of every source directory
- a stale diagram graveyard

## Strong Pattern

MCAF's public guidance explicitly recommends a current `docs/Architecture.md` as the global architecture map for a solution, with diagrams where they materially help:

- [MCAF concepts](https://mcaf.managed-code.com/)
- [MCAF skills catalog](https://mcaf.managed-code.com/skills)

## Useful Diagram Rule

Use Mermaid only when it clarifies:

- system or module boundaries
- request and data flow
- major integration relationships

Do not add diagrams just to make the doc look richer.
