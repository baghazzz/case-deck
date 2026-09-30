# Design system summary

● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation

## What makes the Glance visual language distinctive?
It is built for the **two seconds after a screen wakes**. That produces a full-bleed, image-first canvas ●, a single stand-alone
headline ◐, one-tap engagement ●, and personalisation you can *see* because the user is literally in the image ("starring you") ●.
The palette is black with a hot red and a lavender ●. Compared with utility apps it has almost no chrome and treats browsing as the
product, not the path to it.

## Major design principles
1. Wake-first ● 2. Media is the layout ● 3. One hook, one action ◐ 4. Red means now, lavender means you ○ 5. Starring you ●
6. Discovery over navigation ● 7. Context is a primitive ● 8. Dense, not cluttered ○ 9. Editorial voice ◇ 10. Show your sources ◇

## Core visual primitives
Dark stage (#0C0C10 / #000) · signal red #FF0049 (buttons #E6003F) · iris #DDBEF0 · bottom scrim · Inter + Instrument Serif ·
4px spacing · pill / 16 / 24 radii · tone-based elevation · 1.75px rounded icons · 9:16, 4:5, 3:2, 16:9 media ratios.

## Most reusable components
Card A hero · Card E recommendation (with reason) · Card D commerce (with freshness) · Card C compact · primary pill button · chips ·
badges · category tabs · bottom nav with centred assistant · "Why this" tooltip · bottom sheet.

## How the system handles content discovery
A tuned stream, not a menu: hook → topic tabs → reason-named rails → trending → category tiles. Swipe to skip, tap to open, long-press
to tune. Rails peek at ≥40% and never auto-scroll; stories auto-advance and pause on press.

## How it communicates personalisation
By **showing** (the user's likeness, city, weather or saved trip inside the content) and **naming** (one iris line: "Because you saved
Goa"). Confidence is expressed through wording. Controls — more, less, why, delete — are always one tap away.

## How it balances density and simplicity
A **density gradient**: the hook shows one thing; the feed shows many in a strict grammar (one card system, one metadata style, two
type families, no boxes on media); detail pages add depth only after the user commits.

## Applying the principles to a new product without copying Glance
- Keep the *logic*, change the *identity*: swap the signal and iris hues, the serif, and the imagery; keep "one red = now, one tint = you".
- Keep wake-first discipline: can a stranger understand the hook in two seconds with no tap?
- Keep "show your sources": every volatile fact (price, availability, rule) is rendered from its source with a timestamp or citation.
- Use your own photography and your own mark. The `wake` wordmark and placeholder art here are stand-ins, and so is this package's name.

**Applied example in this package:** a travel assistant (`12_UI_EXAMPLES/travel-assistant/`): lock-screen fare alert bound to a live
quote, fare cards rendered from the API, policy answers that cite or defer to a human. One line: *fetch what changes, cite what rules,
show why.*
