# UI Checklist

## Spacing

- Use `gap-1` to `gap-3` by default.
- Use `p-2` or `p-3` by default.
- Avoid large padding on standard app screens.

## Radius

- Default to `rounded-sm` or `rounded-md`.
- Use `rounded-lg` only with a clear reason.
- Do not ship `rounded-xl`, `rounded-2xl`, or pill controls by default.

## Typography

- Keep most text at `text-sm`.
- Use `text-xs` for metadata.
- Keep page titles restrained.

## Copy Budget

- Labels should usually be 1 to 3 words.
- Table headers should usually be 1 to 2 words.
- Helper text is off by default.
- Empty states get 1 sentence and 1 action.

## Tables

- Module pages default to full-width tables.
- Keep filters attached to the table.
- Avoid wrapping tables in decorative cards.
- Limit visible secondary actions.

## Forms

- Default to a compact 1-column layout.
- Use 2 columns only for short related fields on wide screens.
- Keep validation short and actionable.

## Charts

- Add charts only for real analytical questions.
- Keep charts compact and theme-aware.
- Prefer 1 or 2 charts per row.

## AI Chat

- Keep the welcome state minimal.
- Keep message spacing compact.
- Collapse reasoning after streaming.
- Keep sources secondary and collapsible.

## Empty States

- One sentence.
- One action.
- No illustrations or marketing filler.

## Actions

- One primary action per area.
- Keep secondary actions to the minimum visible set.
- Place create, edit, and filter actions near the work surface they affect.

## Review Questions Before Merge

- Is the page table-first when it should be?
- Is there any decorative chrome that can be removed?
- Is any copy repeating the obvious?
- Are radius and density consistent?
- Do charts or chat surfaces feel larger than the rest of the app?
