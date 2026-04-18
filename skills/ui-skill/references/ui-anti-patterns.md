# UI Anti-Patterns

## Card-Inside-Card CRUD

Why it is bad:
- Adds chrome without adding structure.
- Makes tables and forms feel smaller and noisier.

What to do instead:
- Let the table or form be the main surface.
- Use a single surrounding surface only when it adds real grouping or state.

## Giant Dashboard Cards

Why it is bad:
- Burns space and makes dense work slower to scan.
- Pushes real actions below the fold.

What to do instead:
- Use smaller surfaces, tighter padding, and fewer simultaneous panels.

## Oversized Headers

Why it is bad:
- Makes product pages feel like marketing pages.
- Pushes core work away from the top-left scan path.

What to do instead:
- Use restrained titles and let the table, form, or conversation carry the page.

## Too Much Helper Text

Why it is bad:
- Repeats the obvious and slows scanning.
- Creates visual clutter around simple inputs.

What to do instead:
- Show helper text only for format, warnings, irreversible actions, or recovery.

## Too Much Explanatory Copy

Why it is bad:
- Duplicates page titles and blocks the primary task.
- Makes CRUD surfaces feel heavier than they are.

What to do instead:
- Cut body copy to one short sentence only when orientation is necessary.

## Charts With No Reason

Why it is bad:
- Pretends analysis exists where the user really needs a table.
- Adds noise, legend overhead, and visual weight.

What to do instead:
- Use charts only for trend, comparison, or distribution questions the table cannot answer quickly.

## Huge AI Chat Welcome State

Why it is bad:
- Feels like a demo, not a product surface.
- Pushes the prompt and recent context too far down.

What to do instead:
- Keep the empty state to one short line, optional suggestions, and the input.

## Large Radius Everywhere

Why it is bad:
- Makes internal-product UI feel soft and toy-like.
- Breaks consistency with compact dense layouts.

What to do instead:
- Default to `rounded-sm` and `rounded-md`, with `rounded-lg` only when justified.
