# Design Tokens

This reference is intentionally reusable. It tells you how to infer a local design system first, and only fall back to a restrained default if the repo has none.

## Step 1: Find the Repo's Real Sources of Truth

Inspect these in order:

1. global theme files such as `globals.css`, CSS variables, theme providers, or tokens
2. `package.json` and component config such as `components.json`
3. root layouts, shells, nav bars, dashboards, and form-heavy screens
4. existing primitives and utility helpers

If a repo already has a stable visual language, preserve it.

## Step 2: Extract the Local System

Write down or mentally track:

- primary surface and background colors
- foreground and muted text colors
- accent and destructive colors
- default radii
- common shadows and border opacity
- heading, body, and metadata type scale
- common spacing rhythm
- common action patterns

## If shadcn/ui Is Present

Use these clues:

- `components.json`
- CSS variables in global styles
- existing `ui` primitive files
- button, card, input, sheet, tabs, badge, dialog, and table variants

When shadcn is present:

- prefer extending existing variants over creating parallel primitives
- respect the repo's base color choice and radius scale
- let typography and spacing drive hierarchy before adding decorative elements

## Restrained Fallback System

If the repo has no coherent system, introduce a simple one:

- one sans font family, optionally one mono family
- one neutral surface palette
- one accent color for active or confirmational emphasis
- one destructive color
- 3 clear text tiers: page title, section title, body
- compact or moderate spacing using a consistent rhythm
- small to medium radii
- faint shadows only where separation is needed

## Default Taste

Unless the repo style or the user says otherwise:

- prefer clarity over spectacle
- prefer restrained contrast and one accent over many competing colors
- prefer useful cards, lists, filters, and forms over decorative hero layouts
- avoid purple-by-default AI styling, oversized radii, floating gradient blobs, and excessive glass effects

## Typography

Good defaults when no system exists:

- page title: `text-2xl` or `text-xl`, `font-semibold`
- section title: `text-lg` or `text-base`, `font-semibold`
- body: `text-sm` or nearby, readable line height
- metadata: smaller, muted, and more compact

Do not use more type sizes than the screen needs.

## Color Usage

- keep primary text high-contrast
- use muted text only for secondary information
- use accent colors for selection, focus, or positive emphasis
- use destructive colors for destructive or blocking states only
- never use color as the only signal for important state

## Spacing

- keep spacing rhythmic and predictable
- related items should be visibly grouped
- dense enterprise UIs can be compact without becoming cramped
- avoid giant whitespace unless the product is intentionally editorial or marketing-oriented
