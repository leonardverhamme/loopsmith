# Agentctl Cloud Readiness Reference

Cloud support must be explicit, not implied by local success.

Use these classifications:

- `local-only`
- `cloud-ready`
- `cloud-ready-with-setup`
- `blocked-in-cloud`

Current default stance:

- `agentctl` core: `cloud-ready-with-setup`
- skills wrapper layer: `cloud-ready-with-setup`
- research web: `cloud-ready-with-setup`
- research GitHub: `cloud-ready-with-setup`
- research scout: `cloud-ready-with-setup`
- Playwright CLI: `cloud-ready-with-setup`
- Playwright MCP: `cloud-ready-with-setup`
- `gh`: `cloud-ready-with-setup`
- `vercel`: `cloud-ready-with-setup`
- `supabase`: `cloud-ready-with-setup`
- `firebase`: `cloud-ready-with-setup`
- `gcloud`: `cloud-ready-with-setup`

What cloud setup must usually provide:

- Python
- Node.js and `npx`
- any required CLI binaries
- browser runtime and Playwright dependencies when browser flows are expected
- auth material and environment variables for the chosen adapters
