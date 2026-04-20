# AI Conversation UI

Load this for ChatGPT-style or product-embedded AI interfaces in shadcn or Tailwind apps.

## Core Rule

AI chat UI must inherit the same product density as the rest of the app.

## Supported Component Families

- Conversation container
- Message
- Message content and response
- Prompt input
- Actions toolbar
- Model selector when needed
- Suggestions only in the empty state
- Reasoning
- Tool call display
- Sources and citations
- Branch or regenerate navigation
- Loading, shimmer, task, queue, and plan states
- Code block, artifact, and web preview surfaces

## Density and Behavior Rules

- No giant welcome hero.
- No huge assistant bubbles.
- No always-open reasoning blocks.
- No oversized source cards.
- No giant empty-state explanation.
- Keep spacing between messages compact.
- Keep streaming stable and readable.
- Keep tool and result displays compact and structured.
- Collapse reasoning by default after streaming completes.
- Keep sources secondary and collapsible.
- Keep prompt chrome minimal and aligned with the surrounding app shell.

## Anti-Patterns

- Demo-chat styling
- Huge onboarding copy inside the conversation
- Too much chrome around the prompt box
- Giant attachments or artifact panels by default
- Floating showcase layouts that ignore the rest of the app density

## Self-Audit

Revise if any answer is yes:

- Does the conversation feel larger than the rest of the app?
- Does reasoning dominate the screen?
- Do sources dominate the screen?
- Is message padding excessive?
- Is the welcome state too verbose?

