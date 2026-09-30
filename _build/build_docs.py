"""All markdown documentation. Tables are generated from tokens/content so docs never drift from values."""
import os
import tokens as tk
import content as ct
import svgkit as k

ROOT = "/home/claude/out/glance-inspired-design-system"
O, I, R, G = tk.OBS, tk.INF, tk.REC, tk.ORIG


def md(rel, s):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(s.strip() + "\n")


LEGEND = "● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation"

SOURCES = [
    ("S1", "Glance homepage", "https://glance.com/", "Primary", "Taglines ('Glance it. Shop it.', 'Shopping that Understands You'), single 'Download The App' CTA, dark hero-first layout, sections for AI agents."),
    ("S2", "Glance · About us", "https://glance.com/us/about-us", "Primary", "Agentic commerce positioning; surfaces: lock screen, app, connected TV, brand sites; 'Shopping, minus the heavy lifting'; US MAU claims."),
    ("S3", "Brandfetch · glance.com", "https://brandfetch.com/glance.com", "Secondary (brand registry)", "Brand colours #FF0049 / #FC034D (red), #DDBEF0 (lavender), #000000. No font listed."),
    ("S4", "TechCrunch · Glance launches gen-AI shopping on the lock screen (Feb 2025)", "https://techcrunch.com/2025/02/26/lockscreen-platform-glance-launches-gen-ai-led-shopping-experience-gets-fresh-backing-from-google", "Secondary (press)", "Selfie-based avatar; outfits on the lock screen; CEO: like a fashion magazine where you are the model; tap reveals products from ~400 partners."),
    ("S5", "Android Central · Glance AI lock-screen visuals", "https://www.androidcentral.com/apps-software/glance-ai-allows-to-shop-fashion-via-personalized-ai-generated-lock-screen-visuals", "Secondary (press)", "Save / share / set as wallpaper; one tap to explore looks and products; 1.5M active users in US trials, half returning weekly."),
    ("S6", "Forbes · Glance AI and Samsung (Jun 2025)", "https://www.forbes.com/sites/charliefink/2025/06/04/glance-ai-and-samsung-bring-personalized-shopping-to-the-lock-screen/", "Secondary (press)", "Opt-in; 'you're reacting to an image of yourself'; purchase from the screen; seasonal and limited-time highlights."),
    ("S7", "Glance press release · AI-native commerce platform", "https://glance.com/us/newsroom/pressrelease/glance-ai-launches-ai-native-commerce-platform-for-hyper-real-visual-shopping", "Primary", "Three-model architecture; looks styled on the user; save/share/wallpaper; plans to expand to beauty, accessories and travel."),
    ("S8", "App Store · Glance – My Personal Shopper", "https://apps.apple.com/us/app/glance-my-personal-shopper/id6742974181", "Primary (store listing)", "Personalised feed, moodboards, shoppable collections by colour/style, chat to refine, weather/trend/occasion awareness, Siri entry, home-screen widget."),
    ("S9", "Google Play · Glance – Shop with AI", "https://play.google.com/store/apps/details?id=com.glance.ai", "Primary (store listing)", "'Styled around you'; editorial-quality imagery 'starring you'; reviews complain about forced installs and hard-to-remove behaviour."),
    ("S10", "Google Play · Glance AI Lockscreen", "https://play.google.com/store/apps/details?id=com.glance.ailockscreen", "Primary (store listing)", "AI Looks, live widgets (weather, steps), curated news and scores 'without even unlocking your phone'."),
    ("S11", "InMobi · Partner with Glance", "https://go.inmobi.com/partner-with-glance/", "Primary (advertiser page)", "Ad formats: Impact (full-screen imagery), Engagement (video, interactive), Promotion (one-click installs); content before unlock; ~200M Indian users."),
    ("S12", "9to5Google · Glance lock screen in the US (Apr 2024)", "https://9to5google.com/2024/04/26/glance-android-lockscreen-motorola-turn-off/", "Secondary (press)", "Persistent news widget with category tags; weather appears when conditions change; full-screen prompts to re-enable."),
    ("S13", "Medium · Samsung Glance news stories", "https://androidlockscreeen.medium.com/swipe-to-stay-updated-exploring-the-news-stories-on-the-samsung-glance-lock-screen-b2d7d2eac614", "Tertiary (blog; lower reliability)", "Horizontal swiping between stories; ~10 category tabs starting with 'For You'; 'catch up in seconds'."),
    ("S14", "Glance blog · Smart AI shopping platform features", "https://glance.com/us/blogs/glanceai/fashion/smart-ai-shopping-platform", "Primary (company blog)", "Natural-language + visual search; feeds from saves and dwell time; context-aware (time, location, events); fit-confidence percentages; single-tap checkout."),
]


def research():
    md("00_RESEARCH/source-log.md", f"""
# Source log

Research date: 30 September 2026. {LEGEND}

## Method and limits
- Sources were read through public pages, press, store listings and a brand registry. **The production stylesheet, font files and
  screenshots could not be inspected directly from this environment** (direct network access to glance.com was blocked by policy), so:
  - no pixel value, font or spacing is labelled ● Observed unless a source states it;
  - the two brand hues (#FF0049, #DDBEF0) are ● observed via a brand registry (S3), not via Glance's own CSS;
  - everything else visual is ◐ inferred from described behaviour, ○ reconstructed, or ◇ original.
- Store-listing claims (ratings, MAU) are company-reported and were not independently verified.
- Glance ships different experiences by market (India lock screen with games, video and ads; US lock screen as a news widget; Glance AI
  app for shopping). This package treats them as one family and says which surface an observation comes from.

| ID | Source | Type | What it established |
|---|---|---|---|
""" + "\n".join(f"| {a} | [{b}]({c}) | {d} | {e} |" for a, b, c, d, e in SOURCES) + """

## Reference material not used as design primitives
The Glance name, logo and wordmark, product photography and AI-generated imagery are Glance's property. They were used only as
reference. This package's wordmark ("wake"), icons, placeholder imagery and screens are original.
""")

    md("00_RESEARCH/design-language-analysis.md", f"""
# Design language analysis

{LEGEND}

## One-paragraph read
Glance is a **wake-first** product: its native surface is the lock screen, where a person looks for two seconds. Everything in the
language follows from that. Imagery is full-bleed and does the work of layout ● (S11, S4); copy is a single stand-alone line ◐; action
is one tap ● (S11, S5); personalisation is shown by *putting the user in the picture*, literally, with AI looks "starring you" ● (S4, S9);
and the feed is a tuned stream split by topic tabs rather than a menu tree ● (S13, S8). The brand palette is black with a hot red and a
lavender ● (S3). The newer Glance AI app reframes the whole thing as an "intelligent shopping agent" ● (S1, S2), which adds chat,
moodboards and context-awareness (weather, trends, occasions) ● (S8, S14).

## Characteristics, classified

| Characteristic | Finding | Class | Evidence |
|---|---|---|---|
| Surface | Lock screen first; app, TV, brand sites as extensions | ● | S2, S11 |
| Canvas | Dark theme on marketing site; black in brand palette | ● / ◐ | S1, S3 |
| Brand colour | Hot red #FF0049 (variant #FC034D) | ● | S3 |
| Secondary colour | Lavender #DDBEF0 | ● | S3 |
| Imagery | Full-screen imagery and video as ad/content formats | ● | S11 |
| Likeness | AI-generated images of the user wearing products | ● | S4, S5, S6, S7 |
| Copy | Two-verb brand line; short imperative CTAs | ● | S1 |
| Editorial framing | "Fashion magazine… you are the model" | ● | S4 |
| Interaction | One tap / one click from lock screen to content or product | ● | S5, S11 |
| Navigation | Topic tabs starting with For You; horizontal swiping | ● (tertiary source) | S13 |
| Personalisation inputs | Saves, dwell time, weather, trends, occasions, time of day | ● | S8, S14 |
| Utility | Widgets (weather, steps, scores) appearing on the lock screen | ● | S10, S12 |
| Control and trust | Users complain about forced installs and re-enable prompts | ● | S9, S10, S12 |
| Typography | Not identifiable from available sources | — | Reconstructed as Inter + Instrument Serif ○/◇ |
| Radius, spacing, shadows | Not measurable from available sources | — | Reconstructed ○ |

## What makes it different from utility-first apps
1. **The first screen is not the app.** Utility apps start at a home screen with navigation; Glance starts at content on a screen the user
   did not open on purpose. So value must be immediate and interruption must be cheap to dismiss.
2. **Browsing is the job, not a step before the job.** Discovery is the product ("replacing manual searching and scrolling" S2).
3. **The user is the model.** Personalisation is visible in the imagery rather than hidden in ranking.
4. **Commerce is one tap from inspiration**, not a separate funnel.

## Where the observed language is weak (and this system adds something)
- **Trust and control.** Public reviews show frustration with lack of control (S9, S10, S12). This system adds ◇ "Why this", visible
  inferred interests, a likeness delete control, and "Sponsored" badges.
- **Freshness of facts.** A commerce or travel surface that quotes prices must show when they were checked. ◇ freshness stamps.
""")

    md("00_RESEARCH/visual-pattern-analysis.md", f"""
# Visual pattern analysis

{LEGEND}

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
""")

    md("00_RESEARCH/interaction-pattern-analysis.md", f"""
# Interaction pattern analysis

{LEGEND}

| Interaction | Finding | Class | Source |
|---|---|---|---|
| Wake → consume | Content before unlock, no search or scroll needed | ● | S11 |
| Next item | Horizontal swipe between stories | ● (tertiary) | S13 |
| Change topic | Category tabs, For You first | ● (tertiary) | S13 |
| Engage | One tap reveals products / content | ● | S4, S5 |
| Save / share / wallpaper | Actions on AI looks | ● | S5, S7 |
| Refine by conversation | Chat to refine style; Siri entry | ● | S8 |
| Feedback | Upvote/downvote tuning planned at launch | ● | S4 |
| Purchase | Single-tap checkout, from the screen | ● | S6, S14 |
| Re-engagement | Full-screen prompts to turn the feature back on | ● (negative) | S12 |
| Motion | Not documented | ○ | See 10_MOTION: inferred values |

## Discovery vs transaction
Discovery is ambient and reversible (swipe, skip, save). Transaction is explicit and rare (one primary button, confirmation when money
moves). The system encodes the boundary with colour: iris and glass controls for discovery, signal red only for the commitment.

## Immediacy devices
Live badges, freshness stamps, story progress bars, counts (watching, saved), and time-of-day heroes. Every immediacy device must be
true: "Live" only when live, prices only with a timestamp ◇.
""")

    md("00_RESEARCH/information-hierarchy.md", f"""
# Information hierarchy

{LEGEND}

| Level | Role | Description |
|---|---|---|
""" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in ct.HIERARCHY) + """

## How it changes by content type

| Type | L1 hook | L2 headline | L3 context | L4 metadata | L5 action |
|---|---|---|---|---|---|
""" + "\n".join("| " + " | ".join(r) + " |" for r in ct.HIERARCHY_BY_TYPE) + """

## Scanning model
On a hook: image → headline → action (a Z that ends on the button). On a feed: vertical F down the left edge (kickers, titles) with
horizontal excursions into rails. On detail: headline → byline → first paragraph → sticky action. ◐ inferred from the observed formats;
the order is enforced by type size and position rather than colour.
""")

    md("00_RESEARCH/competitive-reference.md", f"""
# Competitive reference

These are well-known public patterns used as comparison points (general product knowledge, not new research). {LEGEND}

| Product | Pattern | What this system borrows | What it avoids |
|---|---|---|---|
| Instagram Stories / Reels | 9:16 full-bleed, progress bars, right-edge actions | Story viewer, entertainment feed | Endless autoplay on every surface |
| Pinterest | Masonry discovery, saves as the main signal | Discovery masonry; saves drive recommendations | Visual noise from unequal tiles on the home feed |
| Netflix | Rows named by reason ("Because you watched") | Reason-named rails | Hidden reasons for the hero |
| Google Discover | Card feed with "Not interested" controls | More / less / why controls | Tiny, buried controls |
| Samsung / Android lock screens | Glanceable widgets | Utility modules that appear on change | Permanent widgets |
| Booking.com AI trip planner / KAYAK.ai | Prices shown as structured cards from inventory, not model text | Fare card bound to offer ID | LLM-written prices |

## Positioning
Glance-like surfaces sit between **Stories** (full-bleed, swipe) and **Pinterest** (taste, saves), with a commerce action one tap away.
The differentiator this system leans into is **"starring you"** plus **visible trust** (reasons, freshness, sources).
""")


def principles():
    L = [f"# Design principles\n\n{LEGEND}\n\nTen principles, validated against the source log. Each lists its evidence and confidence.\n"]
    for i, (n, one, why, looks, inter, do, dont, ex, conf, ev) in enumerate(ct.PRINCIPLES):
        L.append(f"""## {i + 1:02d} · {n} {conf}

**{one}**

- **Why it exists:** {why}
- **What it looks like:** {looks}
- **What it means for interaction:** {inter}
- **Do:** {do}
- **Don't:** {dont}
- **Example:** {ex}
- **Evidence:** {ev}
""")
    L.append("""## Principles considered and rejected or merged
- "High information density without clutter" → merged into **Dense, not cluttered** (08).
- "Rich media as a structural element" → **Media is the layout** (02).
- "Strong visual hierarchy" → treated as a property of every principle and of the 5-level hierarchy, not a principle on its own.
- "Contextual utility" → **Context is a primitive** (07).
""")
    md("01_DESIGN_PRINCIPLES/principles.md", "\n".join(L))

    md("01_DESIGN_PRINCIPLES/visual-principles.md", f"""
# Visual principles

{LEGEND}

1. **Dark stage, bright media.** Background `#0C0C10`, media ground `#000`. Imagery supplies most of the colour on any screen. ◐
2. **One red per screen.** `--color-primary` appears on one element: the action, or a live indicator. ○
3. **Lavender is information.** Iris marks reasons, AI and personalisation, and is always tappable to explain itself. ◇
4. **No boxes around media.** Media cards have no padding container; text sits on the ground or on a scrim. ○
5. **Radius by role.** Pill for anything tapped, 16 for cards, 24 for heroes and sheets, 0 for full-bleed. ○
6. **Elevation by tone on dark.** No shadows on dark surfaces; surface → surface-elevated steps instead. Shadows only on light. ○
7. **Two families.** Serif for the editorial hook (once per screen), Inter for everything else. ◇
8. **Metadata is one line.** Middle-dot separated, tabular numerals, tertiary colour. ◇
9. **Scrims are mandatory.** Any word on an image sits on `--scrim-bottom` or `--scrim-top`. ◐
10. **Decoration must carry meaning.** The only decorative devices are the live pulse, the iris sparkle and one signal glow. ○
""")

    md("01_DESIGN_PRINCIPLES/interaction-principles.md", f"""
# Interaction principles

{LEGEND}

1. **Tap to engage, swipe to skip.** The cheapest gesture moves on; commitment needs a deliberate tap. ● (S5, S13)
2. **Whole card is the target.** Only Card A has a button; other cards open on tap, tune on long-press. ○
3. **Commitment rises one step at a time:** hook → feed → detail → action. Never jump from a hook to checkout. ◐
4. **Reversible by default.** Save, hide and dismiss show a toast with Undo for 4 seconds. ○
5. **Money moments confirm.** Any change in price between quote and action opens a dialog that restates the new value. ◇
6. **Media leads motion.** Media is the shared element; chrome follows 60–180ms later. ◇
7. **Nothing auto-advances except stories**, and stories pause on press and respect reduced motion. ○
8. **The assistant is one tap away** (centre of the bottom bar), and every search can hand off to it. ◇ (motivated by S8 chat/Siri)
9. **Explain on demand.** Any iris element opens "Why this" in a sheet or tooltip. ◇
10. **Never trap.** Back, edge-swipe and swipe-down close always work; re-enable prompts never block a screen. ◇ (reaction to S12)
""")

    md("01_DESIGN_PRINCIPLES/content-principles.md", f"""
# Content principles

{LEGEND}

## Headlines
- Sentence case, one idea, **≤ 60 characters on media (2 lines)**, ≤ 80 in lists. Specific nouns and numbers: "Six beaches", "₹4,120".
- The headline must make sense with no image and no click. No "You won't believe…".

## Labels and kickers
- Kicker = category · angle, uppercase, ≤ 24 characters: "Travel · For you", "The long read".
- Category labels are nouns. Status labels are adjectives ("Live", "New", "Sponsored").

## Metadata
- Order: **source · context · time** for content; **price · was · off** then **freshness** for commerce; separator " · ".
- Times: "2m", "18 min ago", "Mon". Prices: currency symbol, Indian digit grouping, tabular: ₹5,842.

## Recommendation language (confidence ladder)
| Strength of signal | Phrase | Example |
|---|---|---|
| User's own action | Because you… | Because you saved Goa |
| Behaviour of similar users | Popular with people like you | |
| Similar item | Similar to… | Similar to Panjim |
| Context | For your… / Near you | For Saturday's forecast |
| Trend | Trending near you / Popular now | |

Never state identity ("Because you are a woman in Delhi"). Never imply surveillance ("We noticed you were at…").

## CTA language
Verb + object, ≤ 3 words where possible: Plan a trip · Book at ₹5,842 · See fare · Open official page · Talk to an expert.

## Urgency, trending and social proof
Only real numbers with a source: "Only 3 left" (inventory API), "12.4k watching", "48k saved". No fake countdowns.

## Commerce information
Brand → name → price row → freshness. Price is always rendered from data with "Price checked HH:MM". Sponsored placements say so.

## Entertainment information
Who · where · live/duration · audience. "Live" badge only while live; afterwards "Replay".

## Example content structures
```
Hook (lock screen)          Commerce card                 Recommendation card
─────────────────           ─────────────                 ───────────────────
[badge] For you             [badge] Price drop            [reason] Because you saved Goa
TRAVEL · FOR YOU            Northline                     Palolem after the rains
Monsoon's over. Six         Court low sneaker in red      8 stays · from ₹3,200
beaches worth a long…       ₹4,299  ₹5,999  28% off
Wake Travel · 4 min         ● Price checked 9:41
[Explore →]
```
""")

    md("01_DESIGN_PRINCIPLES/accessibility-principles.md", f"""
# Accessibility principles

{LEGEND}

## Contrast (computed from tokens)
| Pair | Ratio | Result |
|---|---|---|
| White on `primary-action` #E6003F (buttons) | {tk.contrast('#FFFFFF', '#E6003F'):.2f}:1 | AA |
| White on `primary` #FF0049 | {tk.contrast('#FFFFFF', '#FF0049'):.2f}:1 | Large text / icons only — hence `primary-action` for buttons |
| `primary` on dark background | {tk.contrast('#FF0049', '#0C0C10'):.2f}:1 | AA |
| `text-secondary` on dark | {tk.contrast('#B8B8C2', '#0C0C10'):.2f}:1 | AAA |
| `text-tertiary` on dark surface | {tk.contrast('#85838F', '#16161B'):.2f}:1 | AA |
| `text-tertiary` on light surface | {tk.contrast('#6B6975', '#F6F5F8'):.2f}:1 | AA |
| `iris` on `iris-subtle` (dark) | {tk.contrast('#DDBEF0', '#251A2E'):.2f}:1 | AAA |
| `success` on light | {tk.contrast('#0A7F4A', '#FFFFFF'):.2f}:1 | AA |

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
""")


def foundations_docs():
    rows = []
    for t, d, l, u, cf in tk.COLORS:
        rows.append(f"| `--color-{t}` | {d.upper()} | {tk.rgb_str(d)} | {tk.hsl_str(d)} | {l.upper()} | {tk.contrast_note(t, 'dark'):.2f} / {tk.contrast_note(t, 'light'):.2f} | {u} | {cf} |")
    md("04_COLORS/color-system.md", f"""
# Colour system

![Palette](palette.svg)

{LEGEND}

**Observed / reconstructed approximation.** #FF0049 and #DDBEF0 appear in a public brand registry for glance.com (source S3).
They are not taken from Glance's CSS and are not official values. Every other value is reconstructed or original.

## Meaning
- **Signal (red) means now:** the one action on a screen, live indicators. Budget ≈ 0.5% of pixels.
- **Iris (lavender) means you:** reasons, AI, personalisation, the assistant.
- **Stage and surfaces** are near-black so imagery supplies the colour.
- **Semantic** colours are distinct from the brand: success green (fresh, verified), warning amber (cached, changed), error orange-red.

## Tokens (dark default · light)
Contrast column = ratio against the theme background (dark / light).

| Token | Dark HEX | RGB | HSL | Light HEX | Contrast | Usage | Conf. |
|---|---|---|---|---|---|---|---|
""" + "\n".join(rows) + """

## Content overlays
| Token | Value | Usage | Conf. |
|---|---|---|---|
""" + "\n".join(f"| `--{t}` | `{v}` | {u} | {cf} |" for t, v, u, cf in tk.OVERLAYS) + """

## Light / dark behaviour
Dark is default (`:root`). Light is `[data-theme="light"]`. Brand hues, stage, scrims, media overlays and text-on-media are identical in
both themes; neutrals invert; iris and semantic colours darken in light for contrast. See [light-theme.svg](light-theme.svg),
[dark-theme.svg](dark-theme.svg).

## Contrast guidance
- Body text: `text-primary` / `text-secondary` only.
- `text-tertiary`: metadata ≥ 12px only.
- `primary` as text: dark theme only, ≥ 15px semibold. On light use `primary-dark`.
- Filled buttons: `primary-action` (4.73:1 with white), never `primary`.
""")

    trows = "\n".join(f"| `{n}` | {'Instrument Serif' if v['family'] == 'display' else 'Inter'} | {v['weight']} | {v['size']}px | {v['lh']} | {v['ls']}em | {v['max']}ch | {v['usage']} | {v['conf']} |"
                      for n, v in tk.T.items())
    md("03_TYPOGRAPHY/typography-spec.md", f"""
# Typography

![Type scale](type-scale.svg)
![Type in context](typography-samples.svg)

{LEGEND}

## Families
| Role | Family | Why | Licence |
|---|---|---|---|
| Functional (UI, body, numbers) | **Inter** ○ | Glance's production face could not be identified from public sources. Inter is a neutral, highly legible grotesque with tabular figures and the ₹ glyph, close to the clean geometric sans that app-commerce products of this kind typically use. | SIL OFL |
| Editorial hook | **Instrument Serif** ◇ | Expresses the observed "fashion magazine starring you" positioning. Condensed, high-contrast serif that holds up at 40–72px. Original choice, not observed. | SIL OFL |

If you know the production face, change `--font-sans` in one place; the scale holds.

## Scale (mobile; desktop sizes in parentheses in `typography.json`)
| Token | Family | Weight | Size | Line height | Tracking | Max line | Usage | Conf. |
|---|---|---|---|---|---|---|---|---|
{trows}

Desktop (≥1024px): display-xl 72 · display 56 · h1 40 · h2 28 · headline-media 32 · body-l 18.

## Rules
1. One serif moment per screen. Never serif for UI, numbers, labels.
2. Numbers are Inter with `font-variant-numeric: tabular-nums`.
3. Uppercase only for `label` (+0.08em).
4. On media: `headline-media`, 2 lines max, over `--scrim-bottom`.
5. Body line length 60–72 characters; captions ≤ 60.
6. Font files: see `fonts/` (Inter, Instrument Serif, OFL licences included).
""")

    md("05_GRID_AND_LAYOUT/layout-system.md", f"""
# Layout system

![Grid](grid.svg) ![Spacing](spacing-scale.svg) ![Responsive](responsive-layouts.svg)

{LEGEND}

## Spacing ○
Base unit **4px**, structural rhythm **8px**.

| Token | Value | Use |
|---|---|---|
""" + "\n".join(f"| `--{n}` | {v}px | {tk.SPACE_USAGE.get(n, '')} |" for n, v in tk.SPACE) + """

| Layout value | Mobile | Tablet | Desktop |
|---|---|---|---|
| Screen margin | 16 | 24 | 32 (48 wide) |
| Gutter | 12 | 16 | 24 |
| Section gap | 32 | 40 | 48 |
| Card padding | 16 (20 hero) | 20 | 24 |
| Rail card gap | 12 | 12 | 16 |

## Grid and breakpoints ○
| Breakpoint | Range | Columns | Margin | Gutter | Content |
|---|---|---|---|---|---|
""" + "\n".join(f"| {n} | {lo}–{hi if hi else '∞'} | {cols} | {m} | {g} | {cont} |" for n, lo, hi, cols, m, g, cont in tk.BREAKPOINTS) + """

## Card widths
| Card | Mobile | Tablet | Desktop |
|---|---|---|---|
| A hero | 100% − margins (4:5) | 100% (16:9) | 8/12 cols (16:9) |
| B standard | 171 (2-up) / 240 (rail) | 3-up | 4–5 up |
| C compact | 100% | 50% | 4/12 cols |
| D commerce | 171 (2-up) | 4-up | 5–6 up |
| E recommendation | 240 (rail) | 240 | 218–240 |
| F editorial | 100% | 100% | 6/12 cols |

## Layout archetypes
Feed · Content detail · Commerce · Recommendation · Editorial — see [responsive-layouts.svg](responsive-layouts.svg). Media breaks the
grid deliberately: heroes go full-bleed on mobile; rails bleed past the right margin to show a peek.
""")

    md("06_ICONS/icon-guidelines.md", f"""
# Icon guidelines

![Icon sheet](icon-sheet.svg)

{LEGEND} — the icon set is **◇ original**; Glance's icons are not documented publicly.

- **Grid:** 24 × 24, live area 20 × 20 (2px padding).
- **Stroke:** {k.ICON_STROKE}px, round caps, round joins. At 16/20px the stroke is compensated to keep optical weight.
- **Corners:** 1–1.5px radii on rectangles; no sharp outer corners except arrows.
- **Style:** outline. Fill only for active states (liked heart, play). Dots use filled circles r=1.6.
- **Colour:** inherits text colour (`currentColor`). Iris for personalisation, signal only for live.
- **Sizes:** 16 (chips, badges) · 20 (inputs, dense rows) · 24 (nav, default) · 32 (deck).
- **Files:** individual SVGs in `svg/` ({len(k.ICONS)} icons); sprite in `11_SVG_ASSETS/icons/sprite.svg` (`<use href="#i-home"/>`).

| Group | Icons |
|---|---|
""" + "\n".join(f"| {g} | {', '.join(v)} |" for g, v in k.ICON_GROUPS.items()) + """

**Do:** pair icons with labels in navigation. **Don't:** mix with third-party icon sets; don't scale strokes arbitrarily.
""")

    md("10_MOTION/motion-principles.md", f"""
# Motion principles

![Transitions](transitions.svg)

{LEGEND} — Glance does not publish motion specs. Values below are **◐ inferred** from the observed interaction model (swipe stories,
one-tap engage) or **○ reconstructed**.

1. **Fast in, quick out.** Enter 240–360ms, exit 240ms.
2. **Media leads.** The image is the shared element; chrome follows.
3. **Follow the finger.** Sheets, stories and rails track the gesture 1:1 and settle with `emphasized` easing.
4. **One spring.** Only the like has overshoot.
5. **Live things breathe.** The live dot pulses; nothing else loops except skeletons.
6. **Respect reduced motion.**

## Tokens
| Duration | Value | | Easing | Curve |
|---|---|---|---|---|
""" + "\n".join(f"| {a} | {b}ms | | {c} | `{d}` |" for (a, b), (c, d) in zip(list(tk.DURATION.items()), list(tk.EASING.items()))) + """

## Interaction table
| Interaction | Duration | Easing | Behaviour | Conf. |
|---:|---:|---|---|---|
""" + "\n".join(f"| {n} | {d}ms | {e} | {b} | {cf} |" for n, d, e, b, cf in tk.MOTION) + """

## Reduced motion
Transforms → 0ms; cross-fades 160ms; story auto-advance paused (tap to advance); live pulse off; skeleton shimmer becomes static.
""")

    md("10_MOTION/interaction-states.md", f"""
# Interaction states

{LEGEND}

| Component | Default | Hover (pointer) | Pressed | Focus | Disabled | Loading | Selected / active |
|---|---|---|---|---|---|---|---|
| Primary button | primary-action | #D1003A | primary-dark, scale .97 | 2px primary ring + 2px offset | surface-muted, tertiary text | spinner, width locked | — |
| Secondary button | inverse fill | 94% inverse | 85% inverse | ring | surface-muted | spinner | — |
| Tertiary button | border | surface fill | surface-muted | ring | divider border | spinner | — |
| Icon button | muted/glass | +8% white | +12% white | ring | tertiary icon | — | filled icon |
| Chip | surface-muted | surface-elevated | scale .97 | ring | 40% | — | inverse fill + check |
| Card | — | lift 2px, media 1.03 (240ms) | scale .98 (100ms) | ring around card | — | skeleton | visited: title secondary |
| Tab | tertiary 500 | secondary | — | ring | — | — | primary 700 + signal bar |
| Toggle | off: surface-muted | — | knob 22 wide | ring | 40% | — | on: primary-action |
| Text field | 1px border | border 24% | — | 2px primary | surface, tertiary | trailing spinner | — |
| Like | outline | — | like-pop 360 spring | ring | — | — | filled signal |
| Fare card | live (green stamp) | — | — | — | — | skeleton + "Checking live fares…" | changed: amber + dialog |
""")


def patterns():
    pats = [
        ("content-discovery", "Content discovery", "Find something worth attention without searching.", "Waking the phone, opening the app, or pulling to refresh.",
         "Hook (Card A) → category tabs → reason rail (E) → trending (C) → category tiles.", ["Open", "Scan", "Discover", "Engage", "Deep dive"],
         "Swipe/scroll to skip, tap to open, long-press to tune.", "User opens a detail page or saves an item within the session.",
         ["Open: hero chosen by time + context", "Scan: vertical scroll, horizontal rails", "Discover: reason line catches attention", "Engage: tap → shared-media transition", "Deep dive: detail with one sticky action"]),
        ("personalization", "Personalisation", "Feel understood without feeling watched.", "Any module chosen by a user signal.",
         "Iris header or reason chip on the item; 'Why' tooltip; more/less/why controls; editable 'Your taste' in profile.", ["Signal", "Recommendation", "Explanation", "Action"],
         "Tap iris text → why; long-press card → tune sheet; remove interest chips in profile.", "User engages, or tunes and keeps using the feed (tuning is success, not failure).",
         ["Signal captured (save, dwell, context)", "Recommendation rendered with reason", "Explanation on demand", "Action: open, more, less, turn off"]),
        ("recommendation", "Recommendation", "Get a relevant next thing with a reason.", "End of content, empty states, rails on home.",
         "Rail of Card E with a section header naming the signal; confidence expressed in wording.", ["Signal", "Recommendation", "Explanation", "Action"],
         "Swipe rail; tap card; overflow → more/less/why; dismiss with Undo.", "Click-through or save, with low 'less like this' rate.",
         ["Rank candidates", "Attach the strongest honest reason", "Render with reason chip", "Log feedback"]),
        ("editorial", "Editorial", "Read something crafted, calmly.", "Featured slot, long-read tag, curated collection.",
         "Card F (serif headline) → detail with hero image, byline, body-l, sticky action if commerce-linked.", ["Preview", "Open", "Consume", "Continue"],
         "Tap to open; scroll to read; progress implied by scroll; related at end.", "Read depth ≥ 60% or a follow-on action.",
         ["Preview in feed", "Open with shared media", "Consume at body-l", "Continue: related rail + action"]),
        ("commerce", "Commerce", "Go from inspiration to purchase without doubt about price.", "A look, product card, or price alert.",
         "Look (starring you) with hotspots → product sheet / PDP → one 'Buy on store' action; price with freshness stamp.", ["Discover", "Evaluate", "Compare", "Act"],
         "Tap hotspot → sheet; swipe gallery; select size; tap buy (external) — confirm only if price changed.", "Purchase started with the same price that was shown.",
         ["Discover: look or card", "Evaluate: PDP, fit confidence, price checked", "Compare: similar items rail / compare icon", "Act: buy; re-price check; dialog on change"]),
        ("entertainment", "Entertainment", "Be entertained in seconds; come back later.", "Live event, video in feed, story rings.",
         "Video card (16:9) → full-screen 9:16 player with right-edge actions → continue chip.", ["Thumbnail", "Hook", "Play", "Continue"],
         "Tap to play; swipe up for next; hold to pause; set reminder for upcoming live.", "Watch time ≥ 30s or reminder set.",
         ["Thumbnail with live/duration", "Hook: title + live count", "Play full-screen", "Continue chip / next item"]),
        ("notification", "Notification", "Hear only about changes that matter to me.", "Data change on something the user saved or follows.",
         "Grouped list (Today / Earlier), icon circle coded by type, data line with source and time; lock-screen hook for high-value changes.", ["Change", "Alert", "Open", "Act"],
         "Tap to open the changed thing; swipe to dismiss; settings per type.", "Opened alert led to an action; low mute rate.",
         ["Detect a real change (price, rule, live)", "Alert with the new value + freshness", "Open the thing, not a generic page", "Act or dismiss"]),
        ("onboarding", "Onboarding", "Get a feed that feels like mine in under a minute.", "First run, or new surface enabled.",
         "3 steps: value statement → interest picker (chips) → optional likeness (selfie) with explicit consent and delete control.", ["Promise", "Pick", "Personalise", "Land"],
         "Tap chips (≥3), skip anytime, continue button shows count.", "Lands on a home whose hero matches a picked interest.",
         ["Promise: what wakes you up", "Pick: interests as chips", "Personalise: opt-in selfie, privacy line", "Land: first hero uses a pick"]),
    ]
    for slug, name, goal, trig, ui, flow, inter, succ, states in pats:
        extra = ""
        if slug == "commerce":
            extra = """
## Price integrity (case extension ◇)
Prices on cards, buttons and alerts are rendered from the offer/catalogue response and bound to its ID. A re-price check runs when the
user taps the action; if the value moved, a dialog restates the new price. Supplier timeout → amber "Cached HH:MM" and "Check live price",
never a guessed number.
"""
        if slug == "personalization":
            extra = """
## When and how explicit
| Situation | Explicitness | Example |
|---|---|---|
| Uses the user's own action | Explicit reason | Because you saved Goa |
| Uses likeness | Explicit badge + delete control | Starring you |
| Uses location / weather | Contextual metadata | 26° forecast · Delhi |
| Trend or popularity | Implicit label | Trending near you |

**Confidence** is communicated through wording (see content principles), never through percentages, except fit confidence in commerce
(observed as a Glance feature, S14), which is shown as a percentage with its basis ("based on your last two purchases").

## Components
"For you" tab and badge · "Because you watched…" header · "Trending near you" · "Continue watching" chip · "Recommended" rail ·
"Popular now" header · "Based on your interests" line in profile.
"""
        md(f"08_PATTERNS/{slug}.md", f"""
# {name}

● Observed · ◐ Strong inference · ○ Reconstruction · ◇ Original interpretation — pattern flows are ○ reconstructions built on observed behaviour.

```
{'  →  '.join(flow)}
```

| | |
|---|---|
| **User goal** | {goal} |
| **Trigger** | {trig} |
| **UI structure** | {ui} |
| **Interaction** | {inter} |
| **Success condition** | {succ} |

## State transitions
""" + "\n".join(f"{i + 1}. {s_}" for i, s_ in enumerate(states)) + "\n" + extra)


def readmes():
    md("README.md", f"""
# {tk.SYSTEM_NAME} — a Glance-inspired design system

Version {tk.VERSION} · {tk.DATE}

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
""")

    md("QUICKSTART.md", f"""
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
""")

    md("DESIGN_SYSTEM_SUMMARY.md", f"""
# Design system summary

{LEGEND}

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
""")

    md("09_SCREEN_TEMPLATES/README.md", """
# Screen templates

13 phone templates (390 × 844 in a device frame), all composed from `07_COMPONENTS`. ◇ Original screens; not copies of Glance screens.

| File | Screen | Key components |
|---|---|---|
| lockscreen.svg | Lock-screen hook | full-bleed media, story bars, badge, headline-media, glass actions |
| home.svg | Personalised home | top bar, tabs, Card A, reason rail (E), bottom nav |
| discovery.svg | Content discovery | search, chips, masonry tiles |
| content-detail.svg | Content detail | media hero, serif headline, byline, sticky action with live price |
| commerce.svg | Commerce feed | segmented, look with hotspots, Card D grid |
| product-detail.svg | Product detail | gallery, price + freshness, size chips, fit confidence, buy bar |
| profile.svg | Profile | stats, inferred-taste chips, personalisation toggles |
| search.svg | Search | focused search, recents, suggestions, Ask card, results |
| onboarding.svg | Onboarding | progress, serif statement, interest chips, privacy line |
| news-feed.svg | News feed | tabs on media, story bars, right-edge actions |
| entertainment-feed.svg | Entertainment | live video, counts, continue chip, progress |
| notifications.svg | Notifications | segmented, grouped alerts with data lines |
| recommendation-feed.svg | Recommendation feed | reasons, more/less, why tooltip |
""")
    md("12_UI_EXAMPLES/README.md", """
# UI examples

| File | What it shows |
|---|---|
| personalized-home.svg | Lock screen → home → detail: one story through three moments |
| content-feed.svg | News, entertainment and discovery sharing one vertical grammar |
| recommendation-feed.svg | For you with reasons, data-backed updates, editable taste |
| dashboard.svg | Desktop (1440) personalised home with side navigation |
| commerce-feed.svg | Desktop (1440) look + shoppable grid |
| travel-assistant/ | Case application: fare alert, fare card from the API, cited policy + deflect/handoff (3 singles + flow) |
""")
    md("13_DECK_ASSETS/README.md", """
# Deck assets

16 slides, 1920 × 1080, SVG (editable) and PNG (`png/`, drop into any slide tool). Fonts: install `fonts/` for exact rendering.

title-slide · design-dna-slide · visual-language-slide · color-slide · typography-slide · component-slide · card-anatomy-slide ·
content-hierarchy-slide · personalization-slide · interaction-model-slide · design-principles-slide · example-product-slide ·
summary-slide · section-divider · architecture-slide · closing-slide
""")
    md("11_SVG_ASSETS/README.md", """
# SVG assets

| Folder | Contents | Notes |
|---|---|---|
| logos/ | `wake` wordmark (dark/light), symbol, `logo-slot.svg` | Original placeholder mark. The Glance logo is a trademark and is intentionally not included. |
| icons/ | `sprite.svg` with `<symbol id="i-…">` | Same icons as `06_ICONS/svg` |
| decorative/ | live signal, iris sparkle, separator, highlight underline, focus brackets, accent arc, signal blob, image masks (rounded, arch, pill, ticket) | Use one decorative device per composition |
| backgrounds/ | stage-signal, iris-aurora, light-iris (1920 × 1080) | Slide and hero grounds |
| gradients/ | scrim-bottom, scrim-top, signal-iris, iris-night, dusk | Functional gradients only |
| patterns/ | dot-grid, scan-lines, contours | Behind diagrams, never behind body text |
| illustrations/ | 20 original placeholder scenes (4:5) + `_image-system.svg` | Replace with licensed photography |
""")


if __name__ == "__main__":
    research(); principles(); foundations_docs(); patterns(); readmes()
    print("docs ok")
