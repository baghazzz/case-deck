# Implementation

| File | What it is |
|---|---|
| `tokens.css` | All tokens as CSS custom properties (identical to `02_DESIGN_TOKENS/design-tokens.css`). Dark default, `[data-theme="light"]` override, responsive and reduced-motion overrides. |
| `components.css` | Reusable classes: typography, layout, buttons, icon buttons, FAB, chips, badges, inputs, tabs, top/bottom nav, media, cards A–F, modules, overlays, assistant cards, skeleton. Uses only tokens. |
| `example.html` | A complete demo page (header, hero, trending, recommendation rail, commerce grid, editorial, assistant cards, footer, bottom nav). Open it in a browser; toggle the theme with the Theme button. |
| `component-specifications.md` | Implementation spec per component: markup, classes, tokens, states, accessibility. |

## Setup
```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components.css">
```
`components.css` loads Inter and Instrument Serif from `../fonts/`. Icons: inline `11_SVG_ASSETS/icons/sprite.svg` once in the page,
then `<svg class="icon"><use href="#i-home"/></svg>`.

## Mapping to design files
Class names match component names in `07_COMPONENTS` (e.g. `.card--hero` = Card A, `.card--reco` = Card E). Token names match the
JSON files one-to-one (`colors.json › dark › primary` → `--color-primary`).

## Browser notes
Uses `aspect-ratio`, `color-mix()`, `backdrop-filter` (with -webkit- prefix) and `:focus-visible` — supported in current Chrome, Safari,
Firefox and Edge.
