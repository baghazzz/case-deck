# Wake — a Glance-inspired design system

Version 1.0 · September 2026

A complete, reverse-engineered design system that reproduces the **design language** of [Glance](https://glance.com/) — its lock-screen
immediacy, media-led layout, "starring you" personalisation and one-tap commerce — as reusable principles, tokens, components, patterns,
screens, deck assets and CSS. Built to support a product-management case-study presentation.

## What this is
- A structured, internally consistent system that anyone can use to design Glance-*like* product screens and slides.
- A research record that separates what was **observed** from what was **inferred**, **reconstructed**, or **invented**.
- Original vector artwork: icons, placeholder imagery, screens and slides were all drawn for this package.

## What this is not
- Not Glance's official design system, and not endorsed by Glance or InMobi.
- Not a copy of Glance assets. The Glance name and logo are trademarks and are **not** primitives here; the mockups use an original
  placeholder wordmark, "wake". A dashed `logo-slot.svg` marks where a licensed mark could go.
- Not pixel-accurate. Only two colour values are observed (via a brand registry); everything else is a documented reconstruction.

## Confidence notation (used everywhere)
```
● Observed              stated or described in a public source (see 00_RESEARCH/source-log.md)
◐ Strong inference      follows directly from observed behaviour
○ Reconstruction        a system value chosen to be consistent with the observed language
◇ Original interpretation  added by this system; not claimed to exist in Glance
```

## Research methodology
1. Collected public sources: homepage, about page, press release, app-store listings, advertiser page, press coverage, a brand registry,
   company blog (14 sources, [source log](00_RESEARCH/source-log.md)).
2. Extracted visual and product characteristics and classified each with the notation above.
3. Validated candidate principles against evidence; merged or rejected unsupported ones ([principles](01_DESIGN_PRINCIPLES/principles.md)).
4. Reconstructed a token system around the two observed hues and the observed behaviours.
5. Built every downstream artefact from one token source so the system stays coherent.
**Limit:** production CSS, fonts and screenshots could not be inspected directly from the build environment, so no spacing, radius or
type value is claimed as observed.

## Observed patterns (headline list)
Lock-screen-first surface · full-screen imagery and video formats · AI looks "starring you" · save/share/set-as-wallpaper · one-tap
engagement and purchase · topic tabs starting with For You · horizontal story swiping · context-aware feeds (weather, trends, occasions,
time) · chat refinement and Siri entry · black + #FF0049 red + #DDBEF0 lavender brand palette.

## Reconstructed patterns
Spacing (4/8), radii (pill · 16 · 24), elevation (tone on dark, shadow on light), type scale, card anatomies, grid, motion timings,
navigation bar, overlays.

## Original interpretations
Red = now / lavender = you colour semantics · Instrument Serif editorial hook · reason chips and "Why this" · freshness stamps ·
cited-answer and deflect cards for an AI assistant · likeness delete control · assistant in the centre of the nav.

## Package map
| Folder | Contents |
|---|---|
| `00_RESEARCH` | Source log, design/visual/interaction analysis, information hierarchy, competitive reference |
| `01_DESIGN_PRINCIPLES` | 10 principles + visual, interaction, content, accessibility principles |
| `02_DESIGN_TOKENS` | JSON tokens (colour, type, space, radius, shadow, border, motion) + `design-tokens.css` |
| `03_TYPOGRAPHY` … `05_GRID_AND_LAYOUT` | Specs and SVG specimens |
| `06_ICONS` | 50 original icons (individual SVGs) + guidelines |
| `07_COMPONENTS` | Buttons, cards (A–F deep dive), navigation, chips, badges, inputs, tabs, carousels, content/media modules, overlays, assistant (extension) |
| `08_PATTERNS` | Discovery, personalisation, recommendation, editorial, commerce, entertainment, notification, onboarding |
| `09_SCREEN_TEMPLATES` | 13 phone templates |
| `10_MOTION` | Motion principles, transitions, interaction states |
| `11_SVG_ASSETS` | Logos (original + slot), icon sprite, decorative, backgrounds, gradients, patterns, placeholder imagery |
| `12_UI_EXAMPLES` | Multi-screen compositions, desktop dashboard and commerce, travel-assistant case screens |
| `13_DECK_ASSETS` | 16 slides as SVG (1920×1080) + PNG exports |
| `14_IMPLEMENTATION` | `tokens.css`, `components.css`, `example.html`, component specifications |
| `fonts/` | Inter + Instrument Serif (SIL OFL) |

## Token system in one breath
Dark stage `#0C0C10`, stage `#000`; signal `#FF0049` (buttons `#E6003F`); iris `#DDBEF0`; Inter + Instrument Serif; 4px spacing;
radius pill/16/24; shadows only on light; motion 100/160/240/360ms with `cubic-bezier(.2,0,0,1)`.

## Component system in one breath
One primary button per view · chips for filters · badges state facts · six card anatomies (A hero, B standard, C compact, D commerce,
E recommendation, F editorial) · category tabs · five-item bottom bar with the assistant centred · sheets, dialogs, toasts, "why" tooltips.

## How to use
- **Designers:** start at [QUICKSTART.md](QUICKSTART.md); drag SVGs into Figma (they import as editable vectors with named groups).
- **Engineers:** link `14_IMPLEMENTATION/tokens.css` and `components.css`; open `example.html`.
- **Presenters:** use `13_DECK_ASSETS/*.svg` (or `png/`) directly on 16:9 slides.

## How to extend
1. Add tokens first (`build/tokens.py` in the source, or `design-tokens.css`), then components, then screens.
2. New card? Derive it from one of A–F and document which anatomy it extends (see `07_COMPONENTS/assistant/` for a worked example).
3. Keep the rules: one red per screen, iris only for personalisation, scrim under any text on media, sources for any volatile fact.
4. Classify every new claim about Glance with the confidence notation.

Also see [DESIGN_SYSTEM_SUMMARY.md](DESIGN_SYSTEM_SUMMARY.md) and the standalone PDF shipped next to this folder.
