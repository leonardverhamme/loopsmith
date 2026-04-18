# Audit Scope

Use this skill when the durable documentation surface itself needs a full sweep.

## Cover These Areas

- root and nested `README.md`
- onboarding docs
- `AGENTS.md` and repo context docs
- architecture overviews and system maps
- ADRs and decision logs
- runbooks and command docs
- feature or subsystem docs that are supposed to guide maintenance

## Look For

- stale commands or broken paths
- duplicated or contradictory instructions
- undocumented module boundaries or ownership
- missing ADRs for durable architectural shifts
- docs that no longer match the code or CI
- missing operational recovery guidance where the repo clearly needs it

## Good Outcome

The repo should become easier for both humans and agents to navigate without turning into a docs graveyard.
