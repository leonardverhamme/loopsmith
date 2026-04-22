<!-- agent-cli-os:auto-generated -->
# Agent CLI OS Cloud Readiness

Cloud support is explicit, not assumed. A plugin install is not enough without a cloud environment that provides the required tools and auth.

## Minimum Cloud Bundle

- Python 3.12+ for Agent CLI OS
- Node.js and `npx` for the skills wrapper layer
- Playwright plus a Chromium-capable browser route if browser automation is required
- Auth and configuration for any vendor CLI you expect to use in cloud
- Write access to repo-local `.codex-workflows/` state and any generated docs/evidence paths

## Readiness Matrix

- `agent-cli-os core`: `cloud-ready-with-setup`
  - Requirements: Python 3.12+, Agent CLI OS bundle files under $CODEX_HOME, write access to workflow state
  - Notes: Pure Python stdlib control plane. Safe once the environment installs the home bundle.
- `skills wrapper layer`: `cloud-ready-with-setup`
  - Requirements: Node.js and npx, skills CLI availability, network access if installing from remotes
  - Notes: Agent CLI OS wraps official skills tooling rather than replacing it.
- `research web`: `cloud-ready-with-setup`
  - Requirements: network access, public web reachability
  - Notes: Uses public web fetches and the shared evidence envelope.
- `research github`: `cloud-ready-with-setup`
  - Requirements: gh installed, GitHub auth available in the environment
  - Notes: Prefers gh and only falls back to browser/web when GitHub CLI cannot answer the question.
- `research scout`: `cloud-ready-with-setup`
  - Requirements: web reachability, gh installed, GitHub auth
  - Notes: Runs web and GitHub tracks separately, then merges the evidence.
- `Playwright CLI`: `cloud-ready-with-setup`
  - Requirements: Node.js, Playwright package, Chromium or a compatible browser binary
  - Notes: Preferred browser adapter when a browser-capable CLI environment exists.
- `Playwright MCP`: `cloud-ready-with-setup`
  - Requirements: Playwright MCP server config, browser runtime support
  - Notes: Peer browser interface to the CLI path; use whichever structured interface fits the task.
- `gh`: `cloud-ready-with-setup`
  - Requirements: GitHub CLI, GitHub auth
  - Notes: Authoritative interface for GitHub-first workflows.
- `gh-codeql`: `cloud-ready-with-setup`
  - Requirements: GitHub CLI, github/gh-codeql extension, GitHub auth
  - Notes: Official GitHub CLI extension for managing and invoking the CodeQL CLI.
- `ghas-cli`: `cloud-ready-with-setup`
  - Requirements: Python 3.9+, callable ghas-cli build, GitHub token or auth context
  - Notes: Useful for GHAS enablement and rollout at scale, but local Windows packaging should be verified before you rely on it as the primary path.
- `graphify`: `cloud-ready-with-setup`
  - Requirements: Graphify CLI, repo-local write access, model/API access when semantic extraction is required
  - Notes: Repo-intel uses Graphify as an optional engine. Base Agent CLI OS install and CI should still work when Graphify is absent.
- `obsidian`: `optional-local-only`
  - Requirements: Local Obsidian install or vault path
  - Notes: Obsidian is a secondary repo-intel export/view layer, not the canonical repo graph store.
- `vercel`: `cloud-ready-with-setup`
  - Requirements: Vercel CLI, Vercel auth
  - Notes: Detected now and suitable for later richer adapters once usage patterns are stable.
- `supabase`: `cloud-ready-with-setup`
  - Requirements: Supabase CLI, project/auth context
  - Notes: First-class dual-route capability locally. Cloud use still depends on CLI plus MCP auth/setup being available.
- `firebase`: `cloud-ready-with-setup`
  - Requirements: Firebase CLI, project/auth context
  - Notes: Detect-only in v1.
- `gcloud`: `cloud-ready-with-setup`
  - Requirements: gcloud CLI, auth context, project configuration
  - Notes: Detect-only in v1.

## Cloud Bring-Up Checklist

- Install the internal `agentctl/` bundle under `$CODEX_HOME`.
- Verify `agentcli doctor` is healthy in the cloud environment itself.
- Verify vendor CLI auth before relying on GitHub-, Vercel-, or Supabase-backed flows.
- Verify the browser route before relying on research, UI, or test workflows that need runtime inspection.
- Verify the deep-run worker route before relying on unattended checklist completion. A checklist alone is not a worker.
- Treat any capability not explicitly marked healthy in cloud as unsupported until proven otherwise.

## Current Local Signals

- Capability summary: `ok`
- Browser route: `ok`
- GitHub CLI skill support: `false`
