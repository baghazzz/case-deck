# Accessibility principles

● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation

## Contrast (computed from tokens)
| Pair | Ratio | Result |
|---|---|---|
| White on `primary-action` #E6003F (buttons) | 4.73:1 | AA |
| White on `primary` #FF0049 | 3.93:1 | Large text / icons only — hence `primary-action` for buttons |
| `primary` on dark background | 4.97:1 | AA |
| `text-secondary` on dark | 9.92:1 | AAA |
| `text-tertiary` on dark surface | 4.84:1 | AA |
| `text-tertiary` on light surface | 4.95:1 | AA |
| `iris` on `iris-subtle` (dark) | 10.03:1 | AAA |
| `success` on light | 5.06:1 | AA |

## Rules
1. **Text on imagery** always over a scrim; target ≥ 4.5:1 against the darkest 60% of the scrimmed area.
2. **Never colour alone.** Errors, warnings, live and verified all carry an icon or a word.
3. **Brand red ≠ error.** Errors use `--color-error` (orange-red, hue ≈ 15°) plus an alert icon; brand red is hue ≈ 343°.
4. **Targets ≥ 44 × 44.** Chips are 34 tall with 5px invisible padding; S buttons (32) only on desktop.
5. **Motion:** honour `prefers-reduced-motion` (transforms off, 160ms fades, stories paused, no live pulse).
6. **Screen readers:** cards expose one link with an accessible name built from kicker + headline + metadata; badges are read as text;
   iris reasons are part of the name ("Recommended because you saved Goa").
7. **Focus:** 2px `--color-primary` ring with 2px offset on every interactive element; visible on media via a 2px dark halo.
8. **Text scaling:** layouts survive 200% text; headlines wrap to 3 lines max then truncate with a full title in the detail page.
9. **Language:** metadata abbreviations have full forms for assistive tech ("4 min" → "4 minute read").
10. **Control:** every personalisation and every likeness-based image can be explained, tuned and deleted.
