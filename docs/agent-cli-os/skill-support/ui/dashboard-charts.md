# Dashboard Charts

Load this for overview pages, analytics pages, and dashboard-like product surfaces.

## Core Rule

Charts are secondary to the data model. They must help interpretation, not just make the page feel richer.

## Pick The Right Dashboard Type

- Analytics-first page:
  - the chart is the main task
  - larger charts can be justified
  - the page may open with a chart as the primary surface
- Workbench or operator page:
  - the main task is a table, queue, form, or workflow
  - summaries and charts must stay compact
  - the primary work surface should usually appear in the first viewport

## First-Viewport Rules

- Prefer one compact header band over stacked title, breadcrumb, tabs, filters, stats, and actions.
- More than two stacked top bars is usually a defect.
- On workbench pages, top chrome should usually stay within roughly the first 20 to 25 percent of the viewport.
- A KPI strip should usually be one compact row, not a wall of promo cards.
- A top chart should not push the main table, queue, or form below the fold on workbench pages.

## Chart Card Rules

- Use restrained titles.
- Add a description only when it changes interpretation.
- Keep borders, radius, and padding aligned with the rest of the app.
- Prefer `rounded-md`, normal borders, and compact padding.
- Avoid giant chart cards, nested cards, or decorative framing.
- Keep legends, filters, and tabs inside the main chart header when possible instead of creating extra rows.

## Size And Layout Rules

- Usually keep charts to 1 or 2 per row.
- Use a stable height.
- On workbench pages, keep summary charts compact.
- On analytics-first pages, a larger primary chart can be justified, but it still needs tight surrounding chrome.
- If a chart needs a large footprint, make that page clearly chart-first instead of pretending it is also a dense CRUD surface.

## Readability Rules

- Keep legends compact and scannable.
- Do not let legends wrap into multiple noisy rows.
- Keep tooltips compact.
- Use subtle grids.
- Avoid loud gradients unless they encode meaning.
- Do not let axis labels, legend labels, or chart labels clip or overflow.
- If labels are too long, abbreviate, regroup, or choose a chart that reads better.

## Chart Selection Guide

- Bar or horizontal bar: category comparisons, rankings, counts, status distributions
- Line: trends over time, deltas, change points
- Area: cumulative or stacked contribution over time
- Pie or donut: small part-to-whole sets with very few categories

Avoid:

- decorative charts with no analytical job
- pie or donut charts with too many categories
- radar charts when bars would read faster

## Audit Questions

Revise if any answer is yes:

- Was the chart added without analytical reason?
- Is the page really a workbench page pretending to be a dashboard?
- Are there too many stacked header or control rows?
- Is the KPI strip or top chart tall enough to hide the main task?
- Is the chart card looser, rounder, or more padded than the rest of the app?
- Are legends, filters, or tabs creating extra chrome that should have been merged into one compact band?
- Do labels, legends, or axes wrap, clip, or overflow?
- Does the chart layout break the density of the rest of the app?
