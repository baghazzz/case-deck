# Visual pattern analysis

● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation

| Pattern | What we know | Class | How the system encodes it |
|---|---|---|---|
| Full-bleed media | "Impact" full-screen imagery format; looks set as wallpaper | ● S11, S5 | Card A, lock-screen template, 9:16 ratio token |
| Text on imagery | Lock-screen stories carry headlines over images | ◐ S13, S11 | `headline-media` 26/700, `--scrim-bottom`, 2-line limit |
| Dark canvas | Dark marketing site; black in palette | ● S1, S3 | `--color-background #0C0C10`, `--color-stage #000` |
| Hot red accent | #FF0049 | ● S3 | `--color-primary`; one per screen |
| Lavender | #DDBEF0 | ● S3 | `--color-iris`; assigned to personalisation ◇ |
| Cards | Collections, looks and product tiles in the app | ◐ S8 | Six card anatomies A–F |
| Chips / tabs | Topic tabs; collections by colour/style | ● S13, ◐ S8 | Category tabs, filter chips |
| Badges | Live, trending, category labels on content | ◐ S10, S11 | Badge set incl. Live, Trending, For you, Sponsored |
| Carousels | Scroll through multiple looks; swipe between stories | ● S4, S13 | Rails with peek, story bars |
| Bottom navigation | Not documented | ○ | Five items, assistant centred ◇ |
| Iconography | Not documented | ○ | Original 50-icon set, 1.75 stroke, rounded |
| Illustration | Glance relies on photography and AI imagery, not illustration | ◐ | No mascot/illustration system; abstract placeholders only |
| Shadows | Not documented | ○ | None on dark; soft shadows on light theme only |
| Radius | Not documented | ○ | 16 cards · 24 heroes · pill controls |
| Gradients | Not documented beyond imagery | ○ | Only functional: scrims; one signal glow for the FAB |
| Type | Not identifiable | ○ / ◇ | Inter (UI) + Instrument Serif (editorial hook) |

## Density vs simplicity
The lock screen is maximally simple (one story). The app is dense (feeds, collections, products). The system reconciles them with a
**density gradient**: hook → feed → detail, with density rising only as the user commits ○.
