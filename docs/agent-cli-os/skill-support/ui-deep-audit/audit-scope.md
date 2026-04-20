# Audit Scope

Use this reference to ensure the audit covers the full app rather than only the most obvious screens.

## Coverage Areas

- Navigation and information architecture
- Landing or overview screens
- Module, CRUD, record, and detail pages
- Tables, filters, bulk actions, search, and empty states
- Forms, validation, helper text, confirmations, and destructive flows
- Typography, scanability, spacing, density, and hierarchy
- Color palette, contrast, borders, shadows, radius, and surface consistency
- Charts, analytics surfaces, legends, and tooltips
- AI chat, assistant, reasoning, sources, tools, and artifact surfaces
- Mobile and narrow viewport behavior
- Accessibility, keyboard flow, visible focus, labels, and semantics
- Consistency with the local design system and shadcn primitives

## Audit Order

1. Map the app shell and navigation.
2. Enumerate the major pages or route groups.
3. Review each page for overall task structure.
4. Drill into sections and components only where the page-level pass exposes issues.
5. Review shared visual tokens and recurring components across the app.

## Parallel Partitioning

When the user explicitly asks for subagents or deeper parallel coverage, split the audit by zone:

- Navigation and IA
- Overview and dashboard pages
- CRUD and module pages
- Forms and validation UX
- Tables and readability
- Palette, contrast, spacing, radius, and tokens
- AI conversation UI
- Responsive behavior
- Accessibility and keyboard behavior
- Consistency and design-system drift

