# UI Review

Load this before you finalize any app UI.

## When to Use

- After building or revising a CRUD, settings, analytics, or AI conversation screen
- When a screen risks becoming too spacious, decorative, verbose, or card-heavy
- Before merge or before presenting UI code as final

## Checklist

- Density: gaps, padding, control heights, and surface size are compact and consistent
- Hierarchy: one clear task per screen, restrained headings, no marketing framing
- Copy length: labels, helper text, headers, and empty states stay within the budget
- Radius: uses small or medium radius, not oversized rounded surfaces
- Table-first structure: module pages default to full-width tables unless there is a strong reason not to
- Form clarity: labels are concise, forms are aligned, validation is short and actionable
- Chart justification: charts exist for analysis, not decoration, and stay compact
- AI chat compactness: message spacing, prompt chrome, reasoning, and sources stay secondary
- shadcn consistency: reuse existing primitives, variants, and theme tokens instead of parallel systems
- Anti-patterns: no generic bloated AI dashboard layout, no card-inside-card CRUD, no giant hero copy

## Output Format

1. Verdict: `pass` or `revise`
2. Top 5 issues
3. Minimal patch plan
4. Revised code targets

