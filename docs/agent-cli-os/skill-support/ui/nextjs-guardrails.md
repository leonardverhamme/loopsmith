# Next.js Guardrails

Use this reference only when the current repo is a Next.js App Router project.

These rules are aligned with the current Next.js 16.2.4 docs.

Relevant docs:

- Server and Client Components: `https://nextjs.org/docs/app/getting-started/server-and-client-components`
- `use client`: `https://nextjs.org/docs/app/api-reference/directives/use-client`
- Font optimization: `https://nextjs.org/docs/app/getting-started/fonts`
- Playwright: `https://nextjs.org/docs/app/guides/testing/playwright`

## Server First

In the App Router, pages and layouts are Server Components by default. Keep them server-side unless interactivity requires a client boundary.

Use Client Components only when you need:

- state
- event handlers
- effects
- browser APIs
- custom client-only hooks

## Keep Client Boundaries Narrow

- `'use client'` belongs only at the top of entry files that must run on the client.
- Once a file is a client entry, its imports and children join the client bundle. Keep that surface area small.
- Prefer a server page that renders a small interactive child instead of a client page that renders everything.

## Serializable Props

- Props passed from Server Components to Client Components must be serializable.
- Do not pass functions or server-only objects across the boundary.
- Shape data on the server, then pass the minimal plain-object payload to the client.

## Providers

- Client providers should wrap only the subtree that needs them.
- Do not move providers higher in the tree without reason. The current root layout already establishes the app i18n boundary.

## Fonts

- Continue using `next/font` in the root layout for application-wide typography.
- Reuse the existing `Manrope` and `IBM Plex Mono` variables instead of importing ad hoc fonts inside feature components.
- Do not add a new font family unless the user asks for a deliberate visual change.

## Server-Only and Client-Only Code

- Keep secrets, privileged fetches, and sensitive transforms in server modules and route handlers.
- If a shared module risks accidental client import, consider `server-only`.
- If a module depends on `window` or browser-only APIs, keep it behind a client boundary.

## Route and API Work

- Keep API and backend-oriented work in `src/app/api/**` or server-side helpers in `src/lib/**`.
- Do not move network or persistence logic into client components for convenience.

## Verification

For UI work in a Next.js repo:

- run `npm run lint`
- run `npm run typecheck`
- use `npm run test:component` for behavioral component changes
- use `npm run test:e2e` or `npm run test:mcp-workflow` for end-to-end flow changes

Playwright is the preferred way to verify real user journeys and navigation behavior.

