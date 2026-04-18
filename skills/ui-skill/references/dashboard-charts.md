# Dashboard Charts

Load this for analytics dashboards, overview pages, and chart views inside shadcn or Tailwind apps.

## Core Rule

Charts are secondary to the data model and should not be added just to make a page feel richer.

## Chart Placement Rules

- Put charts on overview or analytics pages.
- Use charts as alternate views over the same dataset when that improves analysis.
- Do not add charts to every CRUD page.
- Usually keep charts to 1 or 2 per row.

## Compact Chart Style Rules

- Use restrained titles.
- Add a short description only when it helps interpretation.
- Keep legends compact.
- Keep tooltips compact.
- Use subtle grids.
- Avoid loud gradients unless they encode meaning.
- Keep a stable height or aspect ratio.
- Do not build giant chart cards.
- Use Recharts through shadcn chart patterns when available.
- Keep charts theme-aware and accessible where supported.

## Chart Selection Guide

- Bar or horizontal bar: category comparisons, rankings, counts, status distributions
- Line: trends over time, deltas, change points
- Area: trends with cumulative weight or stacked contribution
- Pie or donut: small part-to-whole sets with very few categories
- Radar: only when comparing a small fixed set of dimensions and the shape matters

Avoid:

- Pie or donut charts with too many categories
- Radar charts that could be read faster as bars
- Decorative chart choices that hide the comparison

## Supported Families

- Bar: interactive, simple, horizontal, multiple, stacked, labeled
- Line: interactive, simple, multiple, dots, labeled, step
- Area: interactive, simple, stacked, gradient, legend, axes
- Pie and donut: simple, donut, center-text, interactive, legend, labeled
- Radar: simple, multiple, legend, dots, circular-grid, filled

## Self-Audit

Revise if any answer is yes:

- Was the chart added without analytical reason?
- Is the chart card oversized?
- Are legends or tooltips verbose?
- Does a pie chart have too many categories?
- Does the chart layout break the density of the rest of the app?
