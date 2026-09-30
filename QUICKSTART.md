# Quickstart

## 1. What is inside
Research → principles → tokens → type/colour → grid/space → icons → components → patterns → screens → motion → assets → examples →
deck → CSS. Every visual file was generated from one token source, so values match across SVG, CSS and docs.

## 2. How to navigate
| If you want to… | Open |
|---|---|
| Understand the language in 5 minutes | `DESIGN_SYSTEM_SUMMARY.md`, then `13_DECK_ASSETS/png/` |
| Know what is real vs reconstructed | `00_RESEARCH/source-log.md` |
| Pick colours / type | `04_COLORS/color-system.md`, `03_TYPOGRAPHY/typography-spec.md` |
| Build a screen | `09_SCREEN_TEMPLATES/`, `07_COMPONENTS/cards/README.md` |
| Build in code | `14_IMPLEMENTATION/example.html` |

## 3. Most important tokens
| Token | Value | Why it matters |
|---|---|---|
| `--color-background` | #0C0C10 | The dark stage |
| `--color-primary` | #FF0049 | Signal: live + the one action (● observed hue) |
| `--color-primary-action` | #E6003F | Button fill that passes AA with white |
| `--color-iris` | #DDBEF0 | Personalisation (● observed hue) |
| `--scrim-bottom` | 0 → .85 black | Required under text on media |
| `--font-sans` / `--font-display` | Inter / Instrument Serif | UI / editorial hook |
| `--space-4` | 16px | Screen margin, card padding |
| `--radius-l` / `--radius-xl` / `--radius-pill` | 16 / 24 / 999 | Cards / heroes / anything tapped |
| `--motion-ease-standard` | cubic-bezier(.2,0,0,1) | Default easing |

## 4. Most important components
Card A (hero) · Card E (recommendation with reason) · Card D (commerce with freshness) · primary button · chips · category tabs ·
bottom nav · "Why this" tooltip · fare card and cited-answer card (assistant extension).

## 5. SVG assets
- All SVGs have a `viewBox`, `<title>`/`<desc>`, grouped components (`id="card-hero"`, `id="bottom-nav"` …) and no raster images.
- Text uses Inter / Instrument Serif; install them from `fonts/` so SVGs render as designed (fallbacks are Helvetica/Arial and Georgia).
- Icons: `06_ICONS/svg/*.svg` use `currentColor`; the sprite is `11_SVG_ASSETS/icons/sprite.svg`.
- Placeholder imagery (`11_SVG_ASSETS/illustrations/`) is original; replace with licensed photography for production.

## 6. CSS
```html
<link rel="stylesheet" href="14_IMPLEMENTATION/tokens.css">
<link rel="stylesheet" href="14_IMPLEMENTATION/components.css">
<a class="btn btn--primary">Plan a trip</a>
<article class="card card--hero">…</article>
```
Add `data-theme="light"` to any element for the light theme.

## 7. Deck assets
16 slides at 1920×1080 in `13_DECK_ASSETS/` (SVG for editing, `png/` for PowerPoint/Keynote/Google Slides). Suggested order:
title → design DNA → visual language → colour → typography → components → card anatomy → hierarchy → personalisation → interaction
model → principles → example product → summary → closing. `section-divider.svg` and `architecture-slide.svg` are extras.
