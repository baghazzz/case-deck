"""14: example.html (generated so the icon sprite is inlined) + implementation docs."""
import os
import re
import tokens as tk

ROOT = "/home/claude/out/glance-inspired-design-system"
IMG = "../11_SVG_ASSETS/illustrations"


def ic(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def build():
    sprite = open(f"{ROOT}/11_SVG_ASSETS/icons/sprite.svg").read()
    sprite = sprite.replace('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">',
                            '<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0" aria-hidden="true">')
    reco = [("beach-city", "Because you saved Goa", "Sunset rooftops of Panjim", "14 spots", "open now"),
            ("desert", "Because you saved Jaisalmer", "Desert camps that open after the rains", "12 stays", "from ₹3,800"),
            ("mountain", "Similar to Sikkim", "Hill towns after the rain", "22 guides", "3–5 days"),
            ("temple", "Popular with people like you", "Heritage walks in Old Goa", "9 walks", "this weekend"),
            ("food", "For Saturday's forecast", "The Goan thali trail", "6 kitchens", "under ₹600")]
    reco_html = "\n".join(f'''        <a class="card card--reco" href="#">
          <img src="{IMG}/{sc}.svg" alt="">
          <span class="reason">{ic("personalization", "icon icon--16")}{r}</span>
          <div class="card__body"><div class="card__title clamp-3">{t}</div><div class="meta"><span>{a}</span><span>{b}</span></div></div>
        </a>''' for sc, r, t, a, b in reco)
    prods = [("sneaker", "Northline", "Court low sneaker in signal red", "₹4,299", "₹5,999", "28% off", ("badge--fresh", "Price drop"), True),
             ("bag", "Loom &amp; Co", "Canvas weekender tote", "₹2,190", None, None, None, False),
             ("watch", "Arc", "Field watch, 38mm", "₹8,450", "₹9,990", "15% off", ("badge--warning", "Only 3 left"), False),
             ("lamp", "Halo", "Lilac desk lamp", "₹1,850", None, None, ("badge--new", "New"), False)]
    prod_html = "\n".join(f'''        <a class="card card--commerce" href="#">
          <div class="media"><img src="{IMG}/{sc}.svg" alt="{n}">{f'<span class="badge {b[0]}">{b[1]}</span>' if b else ''}
            <button class="save" aria-pressed="{'true' if liked else 'false'}" aria-label="Save">{ic("like", "icon icon--20")}</button></div>
          <div class="brand">{br}</div><div class="name clamp-2">{n}</div>
          <div class="price"><strong>{p}</strong>{f'<s>{w}</s><span class="off">{o}</span>' if w else ''}</div>
          <div class="fresh">Price checked 9:41</div>
        </a>''' for sc, br, n, p, w, o, b, liked in prods)
    news = [("stadium", "Final over: chase needs 12 off 6", "Cricket", "Live", "2.1M reading"),
            ("news", "Rail budget adds 40 new routes for the festive season", "The Daily Ledger", "National", "18 min"),
            ("concert", "Monsoon fest lineup drops tonight", "Music", "48k saved", None),
            ("food", "The ₹99 thali everyone is queueing for", "Food", "Pune", "8 min")]
    news_html = "\n".join(f'''        <a class="card card--compact has-rank" href="#">
          <span class="rank">{i + 1}</span><div class="media"><img src="{IMG}/{sc}.svg" alt=""></div>
          <div><div class="card__title clamp-2">{t}</div><div class="meta">{''.join(f'<span>{m}</span>' for m in ms if m)}</div></div>
        </a>''' for i, (sc, t, *ms) in enumerate(news))

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{tk.SYSTEM_NAME} · example page</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components.css">
<style>
  /* page-level layout only; all visual values come from tokens.css / components.css */
  main {{ padding-bottom: 120px; }}
  .hero-grid {{ display: grid; gap: var(--space-6); }}
  @media (min-width: 1024px) {{ .hero-grid {{ grid-template-columns: 8fr 4fr; align-items: start; }} }}
  .products {{ display: grid; gap: var(--space-6) var(--gutter); grid-template-columns: repeat(2, 1fr); }}
  @media (min-width: 600px) {{ .products {{ grid-template-columns: repeat(4, 1fr); }} }}
  .two-col {{ display: grid; gap: var(--space-6); }}
  @media (min-width: 1024px) {{ .two-col {{ grid-template-columns: 1fr 1fr; }} }}
  .assist {{ display: grid; gap: var(--space-4); }}
  @media (min-width: 600px) {{ .assist {{ grid-template-columns: 1fr 1fr; }} }}
  footer {{ border-top: var(--border-hairline); margin-top: var(--space-10); padding: var(--space-8) 0 var(--space-12); color: var(--color-text-tertiary); }}
  .theme-toggle {{ margin-left: auto; }}
</style>
</head>
<body>
{sprite}
<header class="topbar"><div class="container row">
  <a class="wordmark" href="#" aria-label="wake home">wake</a>
  <nav class="tabs" aria-label="Topics" role="tablist" style="margin-left:var(--space-6)">
    <button class="tab" role="tab" aria-selected="true">For you</button><button class="tab" role="tab">Travel</button>
    <button class="tab" role="tab">Style</button><button class="tab" role="tab">News</button><button class="tab" role="tab">Cricket</button>
  </nav>
  <button class="btn btn--tertiary btn--s theme-toggle" onclick="document.documentElement.dataset.theme = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light'">Theme</button>
  <button class="icon-btn icon-btn--plain" aria-label="Updates">{ic("notification", "icon icon--20")}</button>
</div></header>

<main class="container">
  <section class="section">
    <p class="kicker t-tertiary">Wednesday 30 September · 31° Delhi</p>
    <h1 class="t-display" style="margin:var(--space-2) 0 var(--space-6)">Good morning, Aria</h1>
    <div class="hero-grid">
      <article class="card card--hero">
        <img src="{IMG}/lagoon.svg" alt="Beach after the monsoon">
        <div class="scrim-b"></div>
        <div class="card__top"><span class="badge badge--for-you">{ic("personalization", "icon icon--16")}For you</span>
          <button class="icon-btn icon-btn--glass" aria-label="Save">{ic("bookmark", "icon icon--20")}</button></div>
        <div class="card__body">
          <p class="kicker">Travel · For you</p>
          <h2 class="t-hook clamp-2" style="margin:var(--space-2) 0 0">Monsoon's over. Six beaches worth the flight</h2>
          <p class="meta"><span>Wake Travel</span><span>4 min</span></p>
          <div class="row"><a class="btn btn--primary" href="#">Plan a trip {ic("arrow")}</a>
            <button class="icon-btn icon-btn--glass" aria-label="Share" style="margin-left:auto">{ic("share", "icon icon--20")}</button></div>
        </div>
      </article>
      <aside>
        <div class="section-header"><h2 class="t-h2">Trending near you</h2></div>
        <div class="stack">
{news_html}
        </div>
      </aside>
    </div>
  </section>

  <section class="section" aria-labelledby="reco">
    <div class="section-header"><div><h2 class="t-h2" id="reco">{ic("personalization", "icon icon--20 t-iris")} Because you saved Goa</h2>
      <span class="why">Tuned to beaches · monsoon · under ₹8k</span></div><a href="#">See all</a></div>
    <div class="rail">
{reco_html}
    </div>
    <div class="tooltip-why" style="margin-top:var(--space-4);max-width:520px"><strong>Why you're seeing this</strong>
      You saved two Goa stories this week and read about monsoon travel. <a class="btn btn--text" href="#">Tune</a></div>
  </section>

  <section class="section" aria-labelledby="shop">
    <div class="section-header"><h2 class="t-h2" id="shop">Shop the look</h2>
      <div class="segmented"><button aria-pressed="true">Looks</button><button aria-pressed="false">Products</button></div></div>
    <div class="chip-row" style="margin-bottom:var(--space-5)"><button class="chip chip--selected">All</button><button class="chip">Coats</button>
      <button class="chip">Shoes</button><button class="chip chip--iris">{ic("personalization", "icon icon--16")}Your street style</button><button class="chip">Under ₹5k</button></div>
    <div class="products">
{prod_html}
    </div>
  </section>

  <section class="section two-col" aria-labelledby="news">
    <a class="card card--editorial" href="#">
      <div class="media ratio-3x2"><img src="{IMG}/temple.svg" alt="Varanasi temple at dawn"></div>
      <p class="kicker">The long read</p>
      <h2 class="card__title" id="news">Forty-eight hours in a city that wakes before you do</h2>
      <p class="clamp-3">A slow itinerary for Varanasi: dawn on the ghats, lunch in the lanes, and the ceremony worth staying up for.</p>
      <p class="meta"><span>Meera Rao</span><span>9 min read</span></p>
    </a>
    <div>
      <div class="section-header"><h2 class="t-h2">Ask, grounded</h2><span class="badge badge--sponsored">Demo</span></div>
      <div class="assist">
        <div class="fare">
          <div class="row"><span class="t-caption t-tertiary">Skyline Air · SK 2134</span><span class="badge badge--fresh" style="margin-left:auto">Live</span></div>
          <div class="fare__route"><div><div class="fare__time">06:10</div><div class="t-caption t-secondary">DEL</div></div><div class="fare__line"></div>
            <div style="text-align:right"><div class="fare__time">08:45</div><div class="t-caption t-secondary">GOI</div></div></div>
          <div class="fare__price">₹5,842</div><div class="fresh">Live fare · checked 9:41 · incl. taxes and fees</div>
          <a class="btn btn--primary btn--block" style="margin-top:var(--space-4)" href="#">Book at ₹5,842</a>
        </div>
        <div class="cited">
          <span class="badge badge--verified">{ic("shield-check", "icon icon--16")}Cited answer</span>
          <p>Indian passport holders can enter Thailand visa-free for tourism for a limited stay. Check stay length and conditions on the official page before you fly.</p>
          <div class="cited__source">{ic("passport", "icon icon--20")}<div><strong>Royal Thai Embassy, New Delhi</strong><br><span class="t-tertiary">Last verified 29 Sep 2026</span></div></div>
        </div>
      </div>
      <div style="margin-top:var(--space-4)"><span class="toast">{ic("check", "icon icon--20")} Saved to Goa trip <button>Undo</button></span></div>
    </div>
  </section>

  <footer>
    <div class="row" style="gap:var(--space-6);flex-wrap:wrap">
      <span class="wordmark" style="color:var(--color-text-primary)">wake</span>
      <span class="t-caption">{tk.SYSTEM_NAME} · {tk.SYSTEM_TAG} · v{tk.VERSION}. Demo content; placeholder art is original. Not affiliated with Glance.</span>
    </div>
  </footer>
</main>

<nav class="bottom-nav" aria-label="Primary">
  <a href="#" aria-current="page">{ic("home")}For you</a><a href="#">{ic("grid")}Discover</a>
  <a href="#" class="is-assistant">{ic("personalization")}Ask</a><a href="#">{ic("bookmark")}Saved</a><a href="#">{ic("profile")}You</a>
</nav>
</body>
</html>
'''
    with open(f"{ROOT}/14_IMPLEMENTATION/example.html", "w") as f:
        f.write(html)

    with open(f"{ROOT}/14_IMPLEMENTATION/README.md", "w") as f:
        f.write(f"""# Implementation

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
""")

    with open(f"{ROOT}/14_IMPLEMENTATION/component-specifications.md", "w") as f:
        f.write("""# Component specifications

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
""")


if __name__ == "__main__":
    build()
    print("impl ok")
