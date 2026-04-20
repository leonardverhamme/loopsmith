# Component Rules

Apply these rules when composing new screens or refactoring existing ones.

## Structure

- Keep route files, pages, and containers thin.
- Put reusable visual primitives in the repo's shared component layer.
- Put domain-specific assemblies in the repo's feature or module layer.
- Keep data shaping, formatting, and business logic out of presentational components.

## Reuse Before Invention

- Reach for the repo's real primitive layer first.
- If a repo already has shell or layout components, reuse them instead of rebuilding page framing.
- If shadcn is present, extend existing variants before creating wrapper piles.
- Only add a wrapper if it adds domain semantics, accessibility defaults, or repetitive composition value.

## Shell and Layout

- New screens should usually fit into the repo's existing layout or navigation frame.
- Titles, toolbars, filters, and secondary actions should align with neighboring screens.
- Mobile behavior should be considered at the same time as desktop behavior, not afterward.

## Cards and Lists

- Cards are containers for work, not decoration.
- Lead with the title, then supporting context, then actions.
- Keep action placement consistent within sibling cards.
- Status should be visible as both text and styling.

## Forms

- Labels must be visible.
- Group fields by user task, not raw schema order.
- Put helper text and validation near the field.
- Default to one primary action in a section; supporting actions should recede.
- Multi-step or sheet flows need a clear title, purpose, and next step.

## Copy

- Prefer direct, specific verbs.
- Avoid hype and filler.
- Keep helper text compact and scannable.
- If the repo is internationalized, write copy that survives expansion and translation.

## State Design

Every interactive surface should account for:

- loading
- empty
- success
- error
- disabled
- overflow or long content

Do not rely on color alone for meaning.

## Visual Discipline

- Keep spacing rhythmic across siblings.
- Keep control scale consistent inside one view.
- Avoid mixing ultra-soft marketing surfaces with dense operational controls.
- Prefer one strong accent moment over many competing highlights.

## What to Avoid

- Decorative dashboards with metrics that do not support action
- Giant headings and overspaced layouts without product reason
- Generic gradient-heavy AI visuals by default
- Empty states that do not suggest a next action
- Wrapper components that only rename props without improving behavior

