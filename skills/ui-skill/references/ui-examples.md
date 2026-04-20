# UI Examples

Use these as pattern anchors, not as hard templates.

## Ideal Module Page

```text
Page
- Header: title, count, primary action
- Inline controls: search, status filter, sort
- Table: full width, compact rows, row click opens detail
```

Notes:
- The table is the page, not a card inside another card.
- Filters sit directly above the table.
- Copy stays limited to labels and table metadata.

## Ideal Compact Form

```text
Form
- Title row: title, save action
- Field stack: concise labels, short validation, optional helper text only when needed
- Footer: save, secondary cancel
```

Notes:
- Default to one column.
- Use two columns only for short related fields on wide screens.
- Keep visual density aligned with nearby list and table screens.

## Ideal Overview Page With Justified Charts

```text
Overview
- KPI strip: 3 to 4 small stats
- Row 1: trend chart, category comparison chart
- Row 2: recent records table
```

Notes:
- Charts explain change or distribution, not decoration.
- Keep charts compact and link back to the underlying records.
- If the table tells the story better, remove the chart.

## Ideal Compact AI Chat Surface

```text
Workspace
- Header: title, model selector, secondary actions
- Conversation: compact messages, collapsible reasoning, compact tool results
- Footer: prompt box, send, optional attach
```

Notes:
- Suggestions appear only in the empty state.
- Sources stay secondary and collapsible.
- The chat should feel like a work surface inside the product, not a standalone demo.

