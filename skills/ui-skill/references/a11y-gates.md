# Accessibility Gates

Use this as the final review checklist for any UI change, regardless of repo.

## Semantics

- One clear `h1` per route.
- Use semantic landmarks where they help: `header`, `main`, `nav`, `section`, `form`.
- Buttons trigger actions. Links navigate. Do not blur the distinction.

## Labels and Instructions

- Every input needs a visible label.
- Required or optional state should be obvious.
- Helper text and validation belong next to the control they describe.
- Icon-only controls need an accessible name.

## Focus and Keyboard

- Interactive controls must remain reachable and understandable by keyboard.
- Keep visible focus styling. Do not remove ring behavior without replacement.
- Sheets, menus, and modal-like surfaces must preserve a sane focus path.

## Contrast and Color

- Core text should generally sit on `text-foreground`.
- `text-muted-foreground` is for secondary information, not the primary instruction on a screen.
- Important state must not rely on color alone.
- If you use priority colors, pair them with text labels such as urgent, due soon, or on track.

## Target Size

- Small compact UI is acceptable, but standalone tap targets should still be comfortably usable on mobile.
- Be cautious with icon-only controls in dense headers and bottom navigation.

## Layout Readability

- Keep scan paths short and obvious.
- Group related controls and content in clear containers.
- Avoid very long uninterrupted paragraphs inside cards, sheets, or callouts.
- Make room for Dutch and French expansion without clipping or awkward wrapping.

## States

For every interactive flow, account for:

- loading
- empty
- success
- error
- disabled

An empty state should tell the user what to do next. An error state should explain what failed and what can be retried or corrected.

## Motion and Feedback

- Use motion only to clarify state changes or navigation, not for decoration.
- Loading and success feedback should appear close to the affected control or content area.
- Avoid animations that delay task completion.

## Verification

Minimum review before shipping:

1. Tab through the changed controls.
2. Confirm labels, focus, and state visibility.
3. Check one narrow mobile viewport and one desktop viewport.
4. Run the repo verification commands required by the scope.

If the user wants stronger enforcement and the repo does not already have it, suggest adding automated checks such as `eslint-plugin-jsx-a11y` or `@axe-core/playwright`.

