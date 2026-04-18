# Dense Product UI

Load this for internal tools, CRUD and product UIs, admin and ops views, dense app screens, shadcn plus Tailwind pages, Notion-like table-first layouts, and bloated UI refactors.

## When to Use

- Entity, record, list, settings, form, and workflow pages
- Refactoring spacious shadcn or Tailwind screens
- Fixing too much padding, copy, radius, card nesting, or decorative hierarchy

## Core Principles

- Default module pages to table-first.
- Keep one primary action per area.
- Use low chrome and compact density.
- Keep copy short and labels concise.
- Use restrained hierarchy, not marketing hierarchy.
- Prefer fewer cards and fewer visible actions.
- Pick consistency over novelty.

## Page Archetypes

- Module page: full-width header row, compact filters, table as the main surface, create action near the title or table controls
- Record page: restrained title row, key metadata first, related sections only if they support the main task, tabs only when the record truly has modes
- Form page: compact single-column form by default, short labels, tightly grouped fields, actions close to the form
- Settings page: group by concern, keep prose minimal, show controls directly, avoid panel sprawl
- Overview page: optional KPI strip, one or two justified charts, always provide a path back to the underlying table or records
- Empty state: one short sentence and one action, no illustrations, no marketing copy, no giant spacing

## Density Defaults

- Default gaps: `gap-1`, `gap-2`, `gap-3`
- Default padding: `p-2`, `p-3`
- Avoid large padding on app screens.
- Standard row and control height: `h-8`
- Icon buttons: `h-7 w-7` or `h-8 w-8`
- Keep text mostly `text-sm`, with `text-xs` for metadata.
- Page titles should be restrained, not marketing-sized.

## Radius Rules

- `rounded-sm` for small controls
- `rounded-sm` or `rounded-md` for buttons and inputs
- `rounded-md` for tables, cards, sheets, and dialogs
- `rounded-lg` only when justified by the existing system
- Ban `rounded-xl`, `rounded-2xl`, and pill-shaped controls by default

## Copy Budget

- Every sentence must earn its place.
- Labels are usually 1 to 3 words.
- Table headers are usually 1 to 2 words.
- Empty state copy is 1 short sentence plus 1 action.
- Helper text is off by default.
- Use helper text only for non-obvious format, warnings, irreversible actions, or recovery guidance.
- Never repeat the page title in body copy.

## Table Rules

- Default to shadcn `Table` or TanStack Table based on complexity.
- Keep header and body cell density compact.
- Use subtle hover, not loud row treatment.
- Keep the top bar compact.
- Attach search and filter rows directly to the table.
- Row click should open the record, page, or sheet.
- Keep the create flow near a small `+` action.
- Avoid nested cards around the table.
- Avoid big toolbar stacks.
- Show at most 3 visible secondary actions per section.

## Form Rules

- Use a compact 1-column form by default.
- Use 2 columns only for short related fields on wide screens.
- Keep labels concise and visible.
- Do not spam helper text.
- Validation should be short and actionable.
- Match form density to the surrounding table or module density.

## Empty States

- One sentence
- One action
- No illustrations
- No marketing copy
- No giant spacing

## Prohibited Patterns

- Giant heroes
- Dashboard-card spam
- Multiple nested cards around core CRUD
- Decorative charts on CRUD pages
- Verbose intros above tables
- Oversized headings
- Repeated subtitles
- Oversized modals for simple forms
- Too many visible actions
- Pill buttons by default

## Working Loop

1. Critique the requested UI for density, copy volume, radius, hierarchy, and whether it should really be a table, form, chart, or chat surface.
2. Generate the compact version.
3. Self-audit with the checklist and revise if needed.

## Self-Audit

Revise if any answer is yes:

- Does a standard surface use `rounded-xl` or larger?
- Is a module page not table-first without a strong reason?
- Is a table wrapped in unnecessary cards?
- Is there too much explanatory copy?
- Are labels or headers verbose?
- Does the page look like marketing instead of product?
- Is the empty state oversized?
- Are there too many visible actions?
- Is density inconsistent across the screen?
