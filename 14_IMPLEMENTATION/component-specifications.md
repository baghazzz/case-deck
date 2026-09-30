# Component specifications

All sizes in px; all colours are tokens. States follow `10_MOTION/interaction-states.md`.

## Button — `.btn`
| Variant | Class | Tokens |
|---|---|---|
| Primary | `.btn--primary` | bg `--color-primary-action`, hover `--color-primary-hover`, active `--color-primary-dark`, text `--color-text-on-primary` |
| Secondary | `.btn--secondary` | bg `--color-text-primary`, text `--color-background` (theme inverse) |
| Tertiary | `.btn--tertiary` | inset 1px `--color-border` |
| On media | `.btn--glass` | `--glass-light` + 20px blur |
| Text | `.btn--text` | `--color-primary-light` (dark) / `--color-primary-dark` (light) |
Sizes: default 44 (M), `.btn--l` 52, `.btn--s` 32. Radius `--radius-pill`. Label 15/600. Loading: `aria-busy="true"`. Disabled: `disabled`
or `aria-disabled="true"`. **A11y:** native `<button>` or `<a>`; icon-only buttons need `aria-label`.

## Icon button — `.icon-btn`
44 circle; `.icon-btn--glass` on media; `.icon-btn--plain` in bars. 20px icon.

## Floating action — `.fab`
56 high, pill, `--shadow-signal`. One per app (the assistant).

## Chip — `.chip`
34 high, 14px padding, 14/500. Selected: `aria-pressed="true"` or `.chip--selected`. Iris: `.chip--iris` for inferred facets. Glass: `.chip--glass`.
Container `.chip-row` scrolls horizontally.

## Badge — `.badge`
22 high, 10.5/600 uppercase, +8% tracking. Kinds: `--live` (pulsing dot), `--new`, `--trending`, `--for-you`, `--fresh`, `--verified`,
`--warning`, `--sponsored`. Max two per card.

## Search — `.search`
48 pill, `--color-surface-muted`; focus ring via `:focus-within` 2px `--color-primary`. Contains `<svg>` + `<input>`.

## Text field — `.field`
Label 12 above, input 52 high radius `--radius-m`, helper 12 below; `.field--error` switches border and helper to `--color-error`.

## Tabs — `.tabs > .tab`
`role="tablist"` / `role="tab"`, `aria-selected`. Active: 700 + 16×3 `--color-primary` bar. Gap 22.

## Segmented — `.segmented > button[aria-pressed]`
40 track, 32 segments, selected = theme inverse.

## Top bar — `.topbar`
Sticky 64, translucent background (88%) + blur, hairline bottom. Wordmark `.wordmark` (display italic 28 + signal dot).

## Bottom nav — `.bottom-nav`
Fixed, 5 items, 11px labels, `aria-current="page"` for active, `.is-assistant` for the iris centre item. Hidden ≥1024 (use side nav).

## Media — `.media` + `.ratio-*`
Radius `--radius-l`, inner 1px 8% white stroke, `object-position: center 35%`. Ratios: 9x16, 4x5, 1x1, 16x9, 3x2, 3x4. `.scrim-b` overlay.

## Cards
| Card | Class | Structure |
|---|---|---|
| A hero | `.card.card--hero` | `img` + `.scrim-b` + `.card__top` (badge, save) + `.card__body` (kicker, `.t-hook`, `.meta`, CTA row) |
| B standard | `.card.card--standard` | `.media.ratio-3x2` + `.kicker` + `.card__title.t-h3.clamp-2` + `.meta` |
| C compact | `.card.card--compact` (+ `.has-rank`) | [`.rank`] + `.media` 72 + title/meta |
| D commerce | `.card.card--commerce` | `.media` (badge, `.save[aria-pressed]`) + `.brand` + `.name` + `.price` + `.fresh` |
| E recommendation | `.card.card--reco` | `img` + `.reason` (iris) + `.card__body` (title, meta) |
| F editorial | `.card.card--editorial` | `.media.ratio-3x2` + `.kicker` + serif `.card__title` + dek + meta |
Whole card is one `<a>`; nested buttons (save) stop propagation. Accessible name = kicker + title + meta (+ reason for E).

## Modules
`.section-header` (h2 + optional `.why` iris line + "See all"), `.rail` (snap, 240 columns, bleeds past margins), `.tooltip-why`.

## Overlays
`.sheet` (radius-xl top, grabber, 360ms enter), `.toast` (48 pill, one action), `.scrim` (`--scrim-full`).

## Assistant (case extension)
`.fare` fare card — price rendered from API data with `.fresh` (or `.fresh--stale` when cached); primary button repeats the price.
`.cited` policy answer with `.cited__source` (publisher, last verified, link). A deflect card is `.cited` with an info icon, a secondary
"Open official page" and a tertiary "Talk to an expert".

## Skeleton — `.skeleton`
Shimmer 1.4s linear; static under reduced motion.
