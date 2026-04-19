# loopsmith Repo Guidance

- Keep this file short. It is a routing map, not the system of record. Put detail in `docs/loopsmith/`, generated pages, and `agentctl capability <key>`.
- Use `agentctl capabilities` as the default front door. Use `agentctl inventory show` only when the raw installed or autodetected surface matters.
- Keep the default surface compact: no flat dumps, no automatic promotion from detected tools into front-door capabilities, and no bloated capability skills.
- Prefer `agentctl run <workflow>` for named deep workflows. Use `$loopsmith` with `loopsmith loop <name>` for durable large tasks that need disk-backed state.
- After routing, prefer the healthiest authoritative interface that `agentctl` reports. Vendor CLIs remain authoritative for their own systems.
- Require a real Playwright verification pass for runnable UI or browser-facing work.
- When asked to add tests, use `$test-skill` and choose the materially needed layers.
- Never edit `skills/` or `plugins/*/skills/` unless the user explicitly asks for skill work and explicitly opens `$skill-edit-mode`.
- After changing control-plane behavior or routing surface, follow `docs/loopsmith/maintainer-guide.md` and run `python -m agentctl.agentctl maintenance audit --json`.
