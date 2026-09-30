"""07: component library sheets, card deep-dive (SVG + anatomy + spec), per-folder READMEs."""
import os

import tokens as tk
import svgkit as k
import components as c
from svgkit import text, rect, line, circle, path, para, icon, tw, group, media
from sheets import sheet, conf_tag, section_label
from components import DARK, LIGHT

OUT = "/home/claude/out/glance-inspired-design-system/07_COMPONENTS"
TP, TS, TT = DARK["text-primary"], DARK["text-secondary"], DARK["text-tertiary"]


def md(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(content.strip() + "\n")


def callout(s, n, px, py, lx, ly, label, sub=None, anchor_left=True):
    """Numbered callout: dot on the part, leader to a label."""
    s.add(line(px, py, lx - 14, ly - 4, "#FF0049", 1, opacity=.7))
    s.add(circle(px, py, 4, "#FF0049"))
    s.add(circle(lx, ly - 4, 11, "#FF0049"))
    s.add(text(lx, ly, str(n), "label", "#FFFFFF", anchor="middle", size=11, ls=0))
    s.add(text(lx + 20, ly, label, "button", TP, size=14))
    if sub:
        s.add(text(lx + 20, ly + 18, sub, "caption", TT))


def dim(s, x1, y1, x2, y2, label, vertical=False):
    col = "#DDBEF0"
    s.add(line(x1, y1, x2, y2, col, 1))
    if vertical:
        s.add(line(x1 - 5, y1, x1 + 5, y1, col, 1), line(x2 - 5, y2, x2 + 5, y2, col, 1))
        s.add(text(x1 - 8, (y1 + y2) / 2 + 4, label, "caption", col, anchor="end", size=11))
    else:
        s.add(line(x1, y1 - 5, x1, y1 + 5, col, 1), line(x2, y2 - 5, x2, y2 + 5, col, 1))
        s.add(text((x1 + x2) / 2, y1 - 8, label, "caption", col, anchor="middle", size=11))


# ====================================================================== buttons
def buttons():
    s = sheet(1600, 1180, "Components · 07", "Buttons",
              "Pill-shaped, one primary per view. Primary is the signal red; secondary is the inverse of the theme; tertiary is an outline. "
              "On imagery, buttons turn to glass.", "Buttons", tk.INF)
    states = ["default", "hover", "pressed", "disabled", "loading"]
    for j, st in enumerate(states):
        s.add(text(260 + j * 200, 240, st, "label", TT, upper=True))
    for i, v in enumerate(["primary", "secondary", "tertiary", "text"]):
        y = 264 + i * 72
        s.add(text(64, y + 28, v, "button", TP, size=14))
        for j, st in enumerate(states):
            s.add(c.button(260 + j * 200, y, "Plan a trip", v, "M", st, "dark"))
    # light theme strip
    s.add(rect(64, 570, 1472, 110, LIGHT["background"], 16))
    s.add(text(88, 600, "Light theme", "label", LIGHT["text-tertiary"], upper=True))
    for j, v in enumerate(["primary", "secondary", "tertiary", "text"]):
        s.add(c.button(88 + j * 200, 616, "Plan a trip", v, "M", "default", "light"))
    s.add(c.icon_button(900, 616, "bookmark", "light"))
    s.add(c.icon_button(956, 616, "share", "light", variant="inverse"))
    # sizes
    y = 740
    s.add(section_label(64, y, "Sizes"))
    x = 64
    for sz in ["L", "M", "S"]:
        s.add(c.button(x, y + 20, f"Size {sz}", "primary", sz, trailing="arrow"))
        h, pad, fs = c.BTN[sz]
        s.add(text(x, y + 20 + h + 22, f"{h}px · pad {pad} · {fs}px label", "metadata", TT))
        x += c.button_width(f"Size {sz}", sz, trailing="arrow") + 60
    # icon buttons and FAB
    s.add(section_label(760, y, "Icon buttons"))
    for i, (v, n) in enumerate([("muted", "bookmark"), ("plain", "share"), ("inverse", "like"), ("primary", "plus")]):
        s.add(c.icon_button(760 + i * 64, y + 20, n, variant=v))
    s.add(media(s, 1030, y + 4, 240, 84, "dusk", 12))
    s.add(c.icon_button(1046, y + 24, "bookmark", variant="glass"))
    s.add(c.icon_button(1100, y + 24, "share", variant="glass"))
    s.add(c.button(1156, y + 24, "Open", "tertiary", "M", on_media=True))
    s.add(text(1030, y + 110, "Glass on media", "caption", TT))
    s.add(section_label(1330, y, "Floating action"))
    s.add(c.fab(1330, y + 20, label="Ask", svg=s))
    # rules
    ry = 920
    rules = [("One primary per view.", "If two actions compete, one becomes secondary or moves into a sheet."),
             ("Label = verb + object.", "\"Plan a trip\", \"Book at ₹5,842\", \"Open official page\". Never \"Submit\" or \"OK\"."),
             ("Prices in labels come from data.", "A button that carries a price is bound to the same quote ID as the card it sits on."),
             ("Min touch target 44 × 44.", "Size S (32px) is for dense desktop rows only, with 6px invisible padding.")]
    for i, (a, b) in enumerate(rules):
        xx = 64 + (i % 2) * 740
        yy = ry + (i // 2) * 70
        s.add(text(xx, yy, a, "h3", TP))
        s.add(text(xx, yy + 24, b, "body-s", TS))
    s.save(f"{OUT}/buttons/buttons.svg")
    md("buttons/README.md", f"""
# Buttons

![Buttons](buttons.svg)

**Confidence:** ◐ pill shape and a single red primary CTA are strongly inferred from public Glance surfaces ("Download The App", one-tap
"Glance it. Shop it."). Exact sizes, states and the inverse secondary are ○ reconstruction.

| Variant | Use | Dark | Light |
|---|---|---|---|
| Primary | The one action that moves the user forward | `--color-primary-action` fill, white label (4.73:1) | same |
| Secondary | Strong alternative, or primary on a screen that already has a red element | white fill, `#0C0C10` label | `#0C0C10` fill, white label |
| Tertiary | Low-emphasis alternatives, "Share", "Not now" | 1px `--color-border`, text-primary | same |
| Text action | Inline "See all", "Undo" | `--color-primary-light` | `--color-primary-dark` |
| Icon button | Save, share, close | 44px circle, `surface-muted` or glass on media | |
| Floating action | "Ask" — the assistant entry point. One per app. | primary-action + `shadow-signal` | |

## Sizes
| Size | Height | Padding-x | Label | Icon |
|---|---|---|---|---|
| L | 52 | 24 | 15/600 | 18 |
| M | 44 | 20 | 15/600 | 18 |
| S | 32 | 14 | 13/600 | 16 |

## States
Default → hover (`#D1003A`, darker, keeps AA) → pressed (`--color-primary-dark`, scale .97, 100ms) → disabled (`surface-muted`, tertiary text,
no pointer) → loading (label replaced by a 16px spinner; width locked so the layout does not jump).

## Do
- One primary per view; the red is a scarce resource.
- Put the price in the label when the button commits money: "Book at ₹5,842".
- Switch to glass variants on imagery.

## Don't
- Don't use the brand red for destructive actions (use a tertiary button with `--color-error` text and an icon).
- Don't stack two primaries. Don't use ALL CAPS labels.
- Don't write a price into a label by hand: bind it to the same fare/quote ID as the card.
""")


# ====================================================================== chips / badges / inputs / tabs
def chips():
    s = sheet(1600, 820, "Components · 07", "Chips",
              "Chips filter and steer. Selected is the theme inverse. Iris chips mark anything the system inferred about you. "
              "On imagery, chips go glass.", "Chips", tk.REC)
    s.add(section_label(64, 240, "States"))
    x = 64
    for lab, kw in [("Default", {}), ("Selected", {"selected": True}), ("With icon", {"icon_name": "location"}),
                    ("Iris · inferred", {"variant": "iris", "icon_name": "personalization"}), ("Dismissible", {"trailing": "close"})]:
        g, ww = c.chip(x, 260, lab, **kw)
        s.add(g)
        x += ww + 24
    s.add(section_label(64, 350, "Filter row (horizontal scroll, 16px leading margin, no trailing margin)"))
    s.add(c.chip_row(64, 370, ["All", ("Near me", "location"), "Under ₹5k", "This weekend", "Beaches", "Hills", "Food trails"], selected_index=0))
    s.add(section_label(64, 460, "Interest picker (onboarding, profile)"))
    labels = ["Travel", "Street style", "Cricket", "Bollywood", "Food", "Tech", "Sneakers", "Beauty", "Music", "Wellness", "Finance"]
    x, y = 64, 480
    for i, lab in enumerate(labels):
        g, ww = c.chip(x, y, lab, selected=i in (0, 1, 4), icon_name="check" if i in (0, 1, 4) else "plus", h=40)
        s.add(g)
        x += ww + 10
        if x > 900:
            x, y = 64, y + 52
    s.add(media(s, 1000, 240, 536, 300, "beach-city", 16))
    s.add(k.scrim_bottom(s, 1000, 240, 536, 300, .3, .8, 16))
    x = 1020
    for lab in ["Sunset spots", "Rooftops", "Street food"]:
        g, ww = c.chip(x, 480, lab, variant="glass")
        s.add(g)
        x += ww + 8
    s.add(text(1000, 566, "Glass chips on media", "caption", TT))
    rules = ["Height 34 (filter), 40 (picker). Radius pill. Label 14/500.", "Selected = inverse fill. Never red: red is reserved for action and live.",
             "Iris variant only for system-inferred facets (\"Because you like street style\").", "Rows scroll; never wrap filter chips onto two lines."]
    for i, r_ in enumerate(rules):
        s.add(text(64, 660 + i * 28, "· " + r_, "body", TS))
    s.save(f"{OUT}/chips/chips.svg")
    md("chips/README.md", """
# Chips

![Chips](chips.svg)

**Confidence:** ○ reconstruction. Category filtering by horizontal tabs/rows is ● observed on the lock-screen news surface (For You,
Business, Sports… tabs); chip styling is reconstructed.

| Variant | Fill | Label | When |
|---|---|---|---|
| Default | `surface-muted` | text-primary 14/500 | Available filter |
| Selected | theme inverse (white on dark) | inverse | Active filter; add a check icon in multi-select |
| Iris | `iris-subtle` | `iris` + sparkle | The system inferred this facet from behaviour |
| Glass | `rgba(22,22,27,.56)` | white | Chips placed on imagery |
| Dismissible | default + 14px close | | Applied filters in search |

**Anatomy:** 34px height · 14px side padding · 16px icon · 6–8px icon gap · pill radius · 8px gap between chips.

**Do:** keep labels to 1–3 words; lead with the most-used filter; use iris only for inferred facets.
**Don't:** use red for selection; wrap a filter row; mix iris and default chips in the same group without a header explaining why.
""")


def badges():
    s = sheet(1600, 720, "Components · 07", "Badges",
              "Badges state a fact about content: it is live, new, for you, verified, sponsored. Eleven-pixel uppercase labels, pill-shaped, "
              "one per card corner.", "Badges", tk.REC)
    x = 64
    s.add(section_label(64, 240, "On surfaces"))
    for kd, lab in [("live", "Live"), ("new", "New"), ("trending", "Trending"), ("for-you", "For you"), ("price-drop", "Price drop"),
                    ("verified", "Verified"), ("live-fare", "Live fare"), ("warning", "Price changed"), ("sponsored", "Sponsored")]:
        g, ww = c.badge(x, 260, lab, kd)
        s.add(g)
        s.add(text(x, 310, kd, "caption", TT, size=11))
        x += max(ww, 70) + 20
    s.add(section_label(64, 370, "On media"))
    s.add(media(s, 64, 390, 700, 180, "concert", 16))
    x = 84
    for kd, lab in [("live", "Live"), ("trending", "Trending"), ("for-you", "For you"), ("verified", "Verified")]:
        g, ww = c.badge(x, 410, lab, kd, on_media=True)
        s.add(g)
        x += ww + 10
    s.add(c.count_dot(830, 420, 3))
    s.add(c.icon_button(870, 400, "notification", badge="3"))
    s.add(text(830, 470, "Count dot / notification badge", "caption", TT))
    rules = ["\"Sponsored\" is always shown on paid placements: an outline badge, top-left, same size as the others.",
             "Live uses the signal red with a white dot; live-fare uses success green because it certifies data freshness, not urgency.",
             "Max one badge per corner; max two per card."]
    for i, r_ in enumerate(rules):
        s.add(text(830, 530 + i * 28, "· " + r_, "body-s", TS))
    s.save(f"{OUT}/badges/badges.svg")
    md("badges/README.md", """
# Badges

![Badges](badges.svg)

**Confidence:** ◐ "Live", "Trending" and category labels over content are strongly inferred from Glance's lock-screen and live-content
surfaces; the iris "For you" and green "Live fare / Verified" badges are ◇ original interpretation.

| Kind | Colour | Icon/dot | Meaning |
|---|---|---|---|
| live | primary fill, white | white dot, pulses 1600ms | Happening now |
| new | white fill | — | Added in the last 24h |
| trending | glass | trending | Velocity, not volume |
| for-you | iris-subtle / iris | sparkle | Selected by personalisation |
| price-drop | success-subtle | tag | Price lower than last seen |
| verified | success-subtle | shield-check | Answer is backed by a cited source |
| live-fare | success-subtle | dot | Price fetched live; carries a timestamp |
| warning | warning-subtle | alert | Price changed / data is cached |
| sponsored | outline | — | Paid placement. Mandatory on ads |

**Spec:** height 22 (24 on hero), padding-x 8, label 10.5–11/600 uppercase +8% tracking, pill radius, 4px from the card corner at 12–16px inset.

**Do:** pair any time-sensitive badge with a timestamp in metadata. **Don't:** use badges as buttons; stack three badges; show "Live" on anything not live.
""")


def inputs():
    s = sheet(1600, 900, "Components · 07", "Inputs",
              "Search is the primary input and is always a pill. Form fields are quieter: 12px radius, label above, helper below, "
              "error with icon and text, never colour alone.", "Inputs", tk.REC)
    s.add(section_label(64, 240, "Search"))
    s.add(c.search_field(64, 260, 420))
    s.add(c.search_field(64, 330, 420, value="goa in oct", focused=True))
    s.add(text(64, 410, "Empty · focused with query", "caption", TT))
    # suggestions dropdown
    s.add(rect(64, 430, 420, 200, DARK["surface-elevated"], 16))
    for i, (ic, t_, sub) in enumerate([("search", "goa in october weather", None), ("plane", "Flights to Goa", "from ₹4,120 · live"),
                                       ("personalization", "Ask: best beach for a quiet week?", None)]):
        yy = 450 + i * 60
        col = DARK["iris"] if ic == "personalization" else TS
        s.add(icon(ic, 84, yy + 6, 20, col))
        s.add(text(118, yy + 22, t_, "body", DARK["iris"] if ic == "personalization" else TP))
        if sub:
            s.add(text(118, yy + 40, sub, "caption", TT))
    s.add(section_label(560, 240, "Text fields"))
    s.add(c.text_field(560, 270, 360, "Full name", "Aria Sen"))
    s.add(c.text_field(560, 380, 360, "Email", "aria@", state="focus", helper="We'll send the booking here"))
    s.add(c.text_field(980, 270, 360, "Passport number", "K12", state="error", helper="Enter the full 8-character number"))
    s.add(c.text_field(980, 380, 360, "Nationality", "India", state="disabled", helper="Taken from your profile"))
    s.add(section_label(560, 530, "Toggles"))
    for i, (lab, on) in enumerate([("Use my location for trips", True), ("Show why I'm seeing this", True), ("Personalised lock screen", False)]):
        yy = 552 + i * 50
        s.add(text(560, yy + 18, lab, "body", TP))
        s.add(c.toggle(860, yy, on))
    rules = ["Search: 48px pill, 20px search icon, placeholder names what can be found.", "Fields: 52px, radius 12, 1px border; focus = 2px signal; error = 2px error + icon + text.",
             "Suggestions show the source of each row: query, entity, or 'Ask' (iris).", "Toggles are for preferences that apply immediately; no save button."]
    for i, r_ in enumerate(rules):
        s.add(text(64, 730 + i * 28, "· " + r_, "body", TS))
    s.save(f"{OUT}/inputs/inputs.svg")
    md("inputs/README.md", """
# Inputs

![Inputs](inputs.svg)

**Confidence:** ◐ natural-language and visual search is ● observed as a Glance AI capability ("Smart search beyond keywords"); field styling ○ reconstructed.

## Search field
48px height · pill · `surface-muted` fill · 20px icon at 16px inset · placeholder in text-tertiary · mic on the right when empty,
clear (×) when filled · focus ring 2px `--color-primary`. Suggestions list in `surface-elevated`, 16px radius, 60px rows; the last
row is always an iris "Ask" row that hands the query to the assistant.

## Text field
Label (caption, text-secondary) 10px above · 52px field · radius 12 · 16px padding · helper (caption) 8px below.
States: default (1px border) · focus (2px primary) · error (2px error + alert icon + message) · disabled (surface, tertiary text).

## Toggle
44 × 26, knob 20. On = primary-action. Changes apply instantly and are confirmed with a toast if they affect what the user sees.

**Do:** say what the error is and how to fix it. **Don't:** rely on red borders alone; don't disable the submit button without saying why.
""")


def tabs():
    s = sheet(1600, 700, "Components · 07", "Tabs",
              "Category tabs are the main way to change the feed's topic: text-only, left-aligned, horizontally scrolling, "
              "with a short signal bar under the active label.", "Tabs", tk.OBS)
    s.add(section_label(64, 240, "Category tabs · on background"))
    s.add(c.category_tabs(64, 290, ["For you", "Travel", "Style", "News", "Cricket", "Food", "Tech", "Music"], 0))
    s.add(section_label(64, 350, "Category tabs · on media"))
    s.add(media(s, 64, 370, 700, 110, "dusk", 16))
    s.add(k.scrim_top(s, 64, 370, 700, 80, .6, 16))
    s.add(c.category_tabs(88, 410, ["For you", "Travel", "Style", "News", "Cricket"], 1, on_media=True))
    s.add(section_label(860, 240, "Segmented control"))
    s.add(c.segmented(860, 260, ["Flights", "Hotels", "Trips"], 0))
    s.add(c.segmented(860, 330, ["Looks", "Products"], 1, w=300))
    s.add(c.segmented(860, 400, ["Day", "Week", "Month"], 1, theme="dark"))
    rules = ["Active: text-primary 15/700 + 16×3 signal bar, 9px below baseline.", "Inactive: text-tertiary 15/500. Gap 22px. Scrolls; first tab is always For you.",
             "Segmented: for 2–3 mutually exclusive views of the same content. Selected segment = theme inverse.",
             "Tabs change content in place (240ms cross-fade), never navigate away."]
    for i, r_ in enumerate(rules):
        s.add(text(64, 540 + i * 28, "· " + r_, "body", TS))
    s.save(f"{OUT}/tabs/tabs.svg")
    md("tabs/README.md", """
# Tabs

![Tabs](tabs.svg)

**Confidence:** ● observed — Glance's lock-screen news uses a row of topical tabs starting with "For You" (For You, Business, Sports,
National, International, Entertainment, Travel & Lifestyle…). Visual treatment (signal bar, weights) is ○ reconstruction.

| Type | Use | Spec |
|---|---|---|
| Category tabs | Switch the feed topic | 15px, active 700 + 16×3 primary bar, inactive 500 tertiary, 22px gap, horizontal scroll |
| Category tabs on media | Top of a full-bleed feed | White / 64% white, over `scrim-top` |
| Segmented control | 2–3 views of the same set (Flights / Hotels / Trips) | 40px pill track in surface-muted, selected = inverse |

**Do:** keep "For you" first and default. **Don't:** exceed ~10 tabs; don't use tabs for actions.
""")


# ====================================================================== navigation
def navigation():
    s = sheet(1600, 1180, "Components · 07", "Navigation",
              "Navigation stays thin so content can be big. A top bar with the wordmark and two icons, a five-item bottom bar "
              "with the assistant in the middle, and back as a glass button when the page is media-led.", "Navigation", tk.REC)
    s.add(section_label(64, 240, "Top bars"))
    s.add(rect(64, 260, 390, 56, DARK["background"], 0, stroke=DARK["divider"]))
    s.add(c.top_bar(64, 260, 390, bell_badge="3"))
    s.add(rect(64, 340, 390, 56, DARK["background"], 0, stroke=DARK["divider"]))
    s.add(c.top_bar(64, 340, 390, title="Your trips", left="back", right=("more",)))
    s.add(media(s, 64, 420, 390, 110, "lagoon", 0))
    s.add(k.scrim_top(s, 64, 420, 390, 80, .55))
    s.add(c.top_bar(64, 420, 390, on_media=True, left="back", right=("bookmark", "share")))
    for i, lab in enumerate(["Home · logo + actions", "Sub-page · back + title", "Media page · glass controls"]):
        s.add(text(480, 294 + i * 80 + (30 if i == 2 else 0), lab, "caption", TT))
    s.add(section_label(760, 240, "Bottom navigation (5 items, assistant centred)"))
    for i in range(3):
        s.add(c.bottom_nav(760, 344 + i * 100, 390, active=[0, 2, 4][i]))
        s.add(text(1170, 300 + i * 100, ["For you active", "Ask active", "You active"][i], "caption", TT))
    s.add(section_label(64, 590, "Category navigation"))
    s.add(c.category_tabs(64, 636, ["For you", "Travel", "Style", "News", "Cricket", "Food"], 0))
    s.add(section_label(64, 700, "Search entry"))
    s.add(c.search_field(64, 720, 390))
    s.add(section_label(760, 700, "Back navigation"))
    s.add(c.icon_button(760, 720, "back", variant="muted"))
    s.add(text(816, 748, "Plain surface", "caption", TT))
    s.add(media(s, 920, 712, 120, 60, "dusk", 12))
    s.add(c.icon_button(928, 720, "back", variant="glass"))
    s.add(text(1052, 748, "On media", "caption", TT))
    s.add(text(760, 800, "Edge swipe and hardware back always work; the button is a visual affordance, not the only exit.", "body-s", TS))
    rules = ["Bottom bar: 84px incl. home indicator, 24px icons, 11px labels, active = text-primary + 4px signal dot above.",
             "The centre item is the assistant (iris). It is never red; red stays for the in-context action.",
             "Top bar: 56px, wordmark left, max two icons right. On media pages: 40px glass circles.",
             "Hide the bottom bar on detail and checkout; show a sticky action bar instead."]
    for i, r_ in enumerate(rules):
        s.add(text(64, 880 + i * 30, "· " + r_, "body", TS))
    s.save(f"{OUT}/navigation/navigation.svg")
    md("navigation/README.md", """
# Navigation

![Navigation](navigation.svg)

**Confidence:** ◐ minimal chrome and topic tabs are strongly inferred from Glance surfaces (the lock screen has no navigation at all;
the app is feed-led). The five-item bar with a centred assistant is ◇ original interpretation, motivated by Glance's chat-based styling
refinement and "Hey Siri, let's Glance" entry points.

| Element | Spec | Notes |
|---|---|---|
| Top bar | 56px; wordmark (display italic 24) left; ≤2 icon buttons right (40px) | Notification bell carries a count badge |
| Sub-page bar | back (40px) + centred h3 title + one overflow | |
| Media top bar | glass 40px circles over `scrim-top` | Used on detail, story, product |
| Bottom nav | 84px incl. home indicator; 5 items; 24px icons; 11/600 labels | Items: For you · Discover · Ask · Saved · You |
| Category nav | category tabs (see tabs) directly under the top bar | Scrolls away with the feed; tabs re-appear on scroll-up |
| Search entry | 48px pill at the top of Discover | Tapping opens the search screen with recent + suggestions |
| Back | glass on media, plain elsewhere; edge-swipe always available | |

**Do:** let the feed scroll under a translucent bottom bar. **Don't:** add a hamburger menu; don't put more than one red element in the chrome.
""")


# ====================================================================== carousels
def carousels():
    s = sheet(1600, 1000, "Components · 07", "Carousels",
              "Rails are how the feed shows breadth without height. Cards peek past the right margin to say 'there is more', "
              "snap to the left edge, and never auto-scroll.", "Carousels", tk.INF)
    s.add(section_label(64, 240, "Rail with peek (mobile, 390 frame)"))
    s.add(rect(64, 258, 390, 400, DARK["background"], 20, stroke=DARK["border"]))
    cid = k.clip_round(s, 64, 258, 390, 400, 20)
    inner = [c.section_header(80, 300, 358, "Because you saved Goa", iris=True, sub="Tuned to beaches · monsoon · under ₹8k")]
    x = 80
    for sc, t_ in [("lagoon", "Palolem after the rains"), ("beach-city", "Sunset rooftops of Panjim"), ("desert", "Desert camps")]:
        inner.append(c.card_reco(s, x, 336, 240, 300, sc, "Because you saved Goa", t_, ("8 stays", "from ₹3,200"), feedback=False))
        x += 252
    s.add(f'<g clip-path="url(#{cid})">' + "".join(inner) + "</g>")
    dim(s, 80, 680, 320, 680, "card 240")
    dim(s, 320, 700, 332, 700, "12")
    dim(s, 332, 720, 454, 720, "peek ≥ 40%")
    s.add(section_label(560, 240, "Hero carousel with page indicator"))
    s.add(media(s, 560, 258, 460, 280, "mountain", 24))
    s.add(k.scrim_bottom(s, 560, 258, 460, 280, .4, .8, 24))
    s.add(text(584, 480, "Hill towns, 3 of 5", "headline-media", "#FFFFFF", size=22))
    s.add(c.page_dots(790, 514, 5, 2, on_media=True))
    s.add(section_label(1080, 240, "Story rings"))
    for i, (sc, lab, seen) in enumerate([("dusk", "Goa", False), ("food", "Food", False), ("stadium", "Cricket", True), ("studio", "Looks", True)]):
        xx = 1080 + i * 110
        gid, g = k.lin_grad([(0, "#FF0049"), (1, "#DDBEF0")], 0, 0, 1, 1)
        s.define(g)
        s.add(circle(xx + 36, 300, 36, "none", stroke=f"url(#{gid})" if not seen else "#3A3A44", sw=3))
        s.add(media(s, xx + 5, 269, 62, 62, sc, 31))
        s.add(text(xx + 36, 358, lab, "caption", TP if not seen else TT, anchor="middle"))
    s.add(text(1080, 400, "Gradient ring = unseen; grey = seen.", "caption", TT))
    s.add(section_label(1080, 450, "Story progress"))
    s.add(media(s, 1080, 470, 200, 190, "dusk", 16))
    s.add(c.story_bars(1092, 482, 176, 4, 1, .45))
    rules = ["Snap: left edge of the next card aligns to the screen margin (16px). 360ms emphasized.",
             "Peek: the next card shows at least 40% so the rail reads as scrollable without an arrow.",
             "Gap 12px. Card widths: 240 (reco), 171 (two-up), 300 (featured). Leading margin 16, trailing 16.",
             "No auto-advance on rails. Stories auto-advance at 5s and pause on press.",
             "Desktop: arrows appear on hover at the rail edges; scroll by one viewport minus one card."]
    for i, r_ in enumerate(rules):
        s.add(text(560, 600 + i * 30 + 80, "· " + r_, "body", TS))
    s.save(f"{OUT}/carousels/carousels.svg")
    md("carousels/README.md", """
# Carousels

![Carousels](carousels.svg)

**Confidence:** ● horizontal swiping between stories is observed on the Glance lock screen; ◐ rails and peeking cards are strongly inferred
from Glance AI's scrollable looks and collections; exact dimensions ○ reconstructed.

| Type | Card | Behaviour |
|---|---|---|
| Recommendation rail | Card E, 240 × 300 | Horizontal scroll, snap-start, 12 gap, ≥40% peek |
| Two-up rail | Card B/D, 171 wide | Same; used for products and quick reads |
| Hero carousel | Card A, full width | Page dots (active 18 × 6 pill), swipe only, no autoplay |
| Story rings | 72px ring, 62px media | Gradient ring (signal → iris) = unseen |
| Story viewer | 9:16 full-bleed | Progress bars at top, 5s auto-advance, tap left/right, hold to pause |

**Accessibility:** rails are lists (`role="list"`), every card is reachable by keyboard; on desktop show previous/next buttons;
auto-advance respects `prefers-reduced-motion`.
""")


# ====================================================================== content modules
def content_modules():
    s = sheet(1600, 1260, "Components · 07", "Content modules",
              "Modules are the sections the feed is built from. Each has one job: hook, explain why, rank, or group. "
              "Personalised modules say why they exist in one line of iris text.", "Content modules", tk.REC)
    # hero module
    s.add(section_label(64, 240, "Hero"))
    s.add(c.card_hero(s, 64, 258, 358, 448))
    # personalized module
    s.add(section_label(470, 240, "Personalised module"))
    s.add(c.section_header(470, 280, 520, "Because you saved Goa", iris=True, sub="Tuned to beaches · monsoon · under ₹8k"))
    s.add(c.card_reco(s, 470, 316, 250, 300, "lagoon", "Because you saved Goa", "Palolem after the rains", ("8 stays", "from ₹3,200")))
    s.add(c.card_reco(s, 732, 316, 250, 300, "beach-city", "Similar to Panjim", "Rooftops for sunset", ("14 spots", "open now")))
    g, h_ = c.tooltip(470, 640, 512, "Why you're seeing this", "You saved two Goa stories this week and read about monsoon travel. Tap to tune or turn this off.")
    s.add(g)
    # trending module
    s.add(section_label(1040, 240, "Trending near you"))
    items = [("stadium", "Final over: chase needs 12 off 6", "Cricket · 2.1M reading"), ("food", "The ₹99 thali everyone is queueing for", "Food · Pune"),
             ("concert", "Monsoon fest lineup drops tonight", "Music · 48k saved"), ("news", "Metro line 3 opens early for festival week", "City · 12 min")]
    for i, (sc, t_, m_) in enumerate(items):
        s.add(c.card_compact(s, 1040, 262 + i * 96, 496, sc, t_, (m_,), rank=i + 1, trailing=None))
    # category module
    s.add(section_label(64, 760, "Category tiles"))
    for i, (sc, lab) in enumerate([("lagoon", "Beaches"), ("mountain", "Hills"), ("food", "Food trails"), ("temple", "Heritage"), ("city", "Nightlife"), ("desert", "Deserts")]):
        xx = 64 + i * 176
        s.add(media(s, xx, 780, 164, 110, sc, 12))
        s.add(k.scrim_bottom(s, xx, 780, 164, 110, .2, .75, 12))
        s.add(text(xx + 12, 876, lab, "h3", "#FFFFFF", size=15))
    # section header spec
    s.add(section_label(1136, 760, "Section header"))
    s.add(c.section_header(1136, 800, 400, "Popular now"))
    s.add(c.section_header(1136, 860, 400, "Because you watched", iris=True, sub="3 new from creators you follow"))
    rules = ["Every module = header + content + (optional) one action. No module without a header except the hero.",
             "Personalised headers: sparkle + h2 + one iris sub-line naming the signal. Tap the line to open 'Why this'.",
             "Trending lists are ranked (serif numerals) and capped at 5; the metric that makes them trend is shown.",
             "Category tiles: 3:2, scrim, h3 label bottom-left. Six max per row on desktop, horizontal scroll on mobile."]
    for i, r_ in enumerate(rules):
        s.add(text(64, 960 + i * 30, "· " + r_, "body", TS))
    s.save(f"{OUT}/content-modules/content-modules.svg")
    md("content-modules/README.md", """
# Content modules

![Content modules](content-modules.svg)

**Confidence:** ◐ feed made of topical sections, trending and "For you" content is strongly inferred (Glance lock-screen playlists,
Glance AI trend-driven feeds); module anatomy is ○ reconstruction; the iris explanation line is ◇ original.

| Module | Built from | Rule |
|---|---|---|
| Hero | Card A | One per screen, first position. Changes by time of day. |
| Section header | h2 + optional iris sub-line + "See all" | Title says what, sub-line says why |
| Recommendation rail | Card E × n | Must carry a reason ("Because you saved Goa") |
| Featured content | Card F | Editorial pick; serif headline allowed |
| Trending | Card C with rank | Max 5, shows the trend metric |
| Category tiles | 3:2 media + scrim + label | Entry points into discovery |
| Personalised module | Header with sparkle + tooltip "Why this" | User can tune or hide it in one tap |

**Ordering on a home feed:** Hero → personalised rail → trending → category tiles → editorial → second rail. Utility modules
(weather, live score, fare alert) are inserted only when their data changes (see patterns/notification.md).
""")


# ====================================================================== media modules
def media_modules():
    s = sheet(1600, 1100, "Components · 07", "Media modules",
              "Media is structure, not decoration. Video, galleries, stories and shoppable looks each have one control model, "
              "and all of them keep text off the image unless a scrim is underneath.", "Media modules", tk.INF)
    s.add(section_label(64, 240, "Video card"))
    g, h_ = c.card_video(s, 64, 260, 440)
    s.add(g)
    g, h_ = c.card_video(s, 64, 580, 440, "stadium", "Last over, every angle", ("Highlights", "1.2M views"), progress=.62, duration="4:12")
    s.add(g)
    s.add(section_label(560, 240, "Story viewer (9:16)"))
    s.add(media(s, 560, 260, 300, 533, "dusk", 20))
    s.add(k.scrim_top(s, 560, 260, 300, 120, .5, 20))
    s.add(k.scrim_bottom(s, 560, 260, 300, 533, .45, .85, 20))
    s.add(c.story_bars(572, 272, 276, 5, 1, .6))
    s.add(c.avatar(572, 288, 28, "W"))
    s.add(text(608, 307, "Wake Travel · 2h", "caption", "#FFFFFF", weight=600))
    s.add(text(576, 690, "Goa's first sunny", "headline-media", "#FFFFFF", size=22))
    s.add(text(576, 716, "weekend in months", "headline-media", "#FFFFFF", size=22))
    s.add(c.button(576, 736, "See the beaches", "tertiary", "S", on_media=True, trailing="arrow"))
    s.add(section_label(920, 240, "Shoppable look (hotspots)"))
    s.add(media(s, 920, 260, 300, 375, "studio", 20))
    for (px, py) in [(1070, 360), (1080, 470), (1040, 600)]:
        s.add(circle(px, py, 14, "rgba(255,255,255,.35)"), circle(px, py, 7, "#FFFFFF"))
    s.add(rect(1110, 452, 150, 40, "rgba(22,22,27,.72)", 20))
    s.add(text(1124, 477, "Wool coat · ₹6,499", "caption", "#FFFFFF", weight=600))
    s.add(c.badge(932, 272, "Starring you", "for-you", on_media=True, h=24)[0])
    s.add(section_label(1280, 240, "Gallery"))
    s.add(media(s, 1280, 260, 256, 320, "sneaker", 16))
    s.add(c.page_dots(1408, 556, 4, 0))
    for i, sc in enumerate(["sneaker", "bag", "watch", "lamp"]):
        s.add(media(s, 1280 + i * 66, 600, 58, 58, sc, 8))
        if i == 0:
            s.add(rect(1280, 600, 58, 58, "none", 8, stroke="#FFFFFF", sw=2))
    rules = ["Video: 16:9 in feed, 9:16 full-screen. Play glyph in a 56px glass circle; progress 3px, signal fill.",
             "Stories: 5s per frame, hold to pause, tap edges to step, swipe down to close. Text sits on scrim-bottom.",
             "Hotspots: 28px ring + 14px dot; tap opens a product sheet, never navigates away from the look.",
             "Galleries: swipe, dots under the image, thumbnails on tablet+; zoom on pinch."]
    for i, r_ in enumerate(rules):
        s.add(text(560, 860 + i * 30, "· " + r_, "body", TS))
    s.save(f"{OUT}/media-modules/media-modules.svg")
    md("media-modules/README.md", """
# Media modules

![Media modules](media-modules.svg)

**Confidence:** ● full-screen imagery and video formats are observed (Glance's "Impact" full-screen and "Engagement" video formats;
AI looks set as wallpaper). ◐ story-style progress and hotspots are strongly inferred; specs are ○ reconstructed.

| Module | Ratio | Controls | Notes |
|---|---|---|---|
| Video card | 16:9 | 56px glass play, 3px progress, LIVE or duration badge | Muted autoplay only on Wi-Fi and only when 60% visible |
| Story viewer | 9:16 | progress bars, tap-step, hold-pause, swipe-down close | Max 7 frames per story |
| Shoppable look | 4:5 | hotspots (28/14), product sheet | "Starring you" iris badge when the image uses the user's likeness |
| Gallery | 1:1 / 4:5 | dots, thumbnails ≥ 600px | Pinch zoom; first image is the product on neutral ground |

**Likeness rule (◇):** any image generated with the user's photo carries the "Starring you" badge and a menu item to delete it.
""")


# ====================================================================== overlays
def overlays():
    s = sheet(1600, 1000, "Components · 07", "Overlays",
              "Sheets for choices, dialogs for consequences, toasts for confirmations, tooltips for explanations. "
              "Everything slides from where the finger is, and everything can be dismissed.", "Overlays", tk.REC)
    s.add(section_label(64, 240, "Bottom sheet"))
    s.add(rect(64, 258, 390, 560, DARK["background"], 20, stroke=DARK["border"]))
    s.add(media(s, 64, 258, 390, 560, "lagoon", 20))
    s.add(rect(64, 258, 390, 560, "rgba(0,0,0,.48)", 20))
    cid = k.clip_round(s, 64, 258, 390, 560, 20)
    s.add(f'<g clip-path="url(#{cid})">' + c.bottom_sheet(s, 64, 488, 390, 330, "Tune this feed",
                                                            [("personalization", "More like this", "Show more beach trips"),
                                                             ("close", "Less like this", None), ("info", "Why am I seeing this?", None),
                                                             ("settings", "Manage interests", None)]) + "</g>")
    s.add(section_label(520, 240, "Dialog"))
    g, h_ = c.dialog(520, 258, 340, "The fare changed", "The live price is now ₹5,842 (was ₹5,210). Nothing has been charged.",
                     "Continue at ₹5,842", "See other flights")
    s.add(g)
    s.add(section_label(920, 240, "Toasts"))
    g, w_ = c.toast(920, 258, "Saved to Goa trip", "Undo")
    s.add(g)
    g, w_ = c.toast(920, 318, "Couldn't reach the airline. Showing cached fare.", None, ic="alert", ic_color=DARK["warning"])
    s.add(g)
    s.add(section_label(920, 410, "Tooltip · why this"))
    g, h_ = c.tooltip(920, 430, 360, "Why you're seeing this", "You saved two Goa stories this week. Tap to tune.")
    s.add(g)
    s.add(section_label(920, 580, "Scrim"))
    s.add(media(s, 920, 600, 160, 100, "dusk", 12))
    s.add(rect(920, 600, 160, 100, "rgba(0,0,0,.48)", 12))
    s.add(text(1096, 656, "scrim-full rgba(0,0,0,.48) behind every modal", "caption", TT))
    rules = ["Sheet: radius 24 top, 36×5 grabber, max 90% height, drag to dismiss, 360ms enter / 240ms exit.",
             "Dialog: only for irreversible or money-changing moments. Title states the fact; primary restates the action with its value.",
             "Toast: 48px pill, bottom 96px above the nav, 4s, one action max. Warnings use the warning icon, never red.",
             "Tooltip: iris, explains personalisation or a data source. Arrow points at the thing it explains."]
    for i, r_ in enumerate(rules):
        s.add(text(520, 760 + i * 30, "· " + r_, "body", TS))
    s.save(f"{OUT}/overlays/overlays.svg")
    md("overlays/README.md", """
# Overlays

![Overlays](overlays.svg)

**Confidence:** ○ reconstruction throughout; the "Why am I seeing this" tooltip is ◇ original, added because personalisation transparency
is weak on today's surfaces (public reviews complain about the lock-screen experience being hard to control).

| Overlay | When | Spec |
|---|---|---|
| Bottom sheet | Choices about the current content (tune, share, sizes) | `surface-elevated`, radius 24 top, grabber, rows 48–56px |
| Dialog | Irreversible or money-changing consequence | 340 wide, radius 24, icon + h3 + body + stacked buttons |
| Toast | Confirmation or soft failure | 48px pill, 4s, one action |
| Tooltip | Explain personalisation or a data source | iris-subtle, radius 12, arrow |
| Scrim | Behind sheets and dialogs | rgba(0,0,0,.48), fades 240ms |

**Do:** make the dialog's primary button repeat the value ("Continue at ₹5,842"). **Don't:** use a dialog for marketing; don't stack overlays.
""")


# ====================================================================== cards (deep dive)
CARDS = [
    ("a", "hero", "Large hero card", "Card A"),
    ("b", "standard", "Standard content card", "Card B"),
    ("c", "compact", "Compact content card", "Card C"),
    ("d", "commerce", "Commerce card", "Card D"),
    ("e", "recommendation", "Recommendation card", "Card E"),
    ("f", "editorial", "Editorial / story card", "Card F"),
]

CARD_SPECS = {
    "a": dict(conf=tk.OBS, conf_note="Full-bleed imagery with headline over it is observed on Glance's lock screen ('Impact' full-screen format) and marketing pages; scrim values and dimensions are reconstructed.",
              dims="358 × 448 on mobile (4:5); 100% × 480 tablet; 720 × 405 desktop (16:9)", pad="20", radius="24 (0 when full-bleed on the lock screen)",
              ratio="4:5 mobile, 16:9 desktop, 9:16 lock screen", typo="kicker label 11/600 caps · headline-media 26/700 (2 lines) · metadata 12/500",
              meta="Source · read time (or price · freshness)", actions="1 primary pill (M) + 1 glass icon button; bookmark top-right", states="default · pressed (scale .98) · saved (bookmark filled) · loading (skeleton) · offline (cached badge)",
              responsive="Mobile: full width minus margins. Tablet: full width, 16:9. Desktop: 8 of 12 columns beside a 4-column rail.",
              use="Once per screen, first position. For the single most relevant thing right now.", dont="Don't put more than 2 lines of headline or more than one CTA; don't use without a scrim."),
    "b": dict(conf=tk.INF, conf_note="Media-on-top, text-below cards are strongly inferred from Glance's blog/newsroom and app collections; values reconstructed.",
              dims="240 wide in rails; 171 in two-up grids; media 3:2", pad="0 (text sits on the ground, not in a box)", radius="16 on media only",
              ratio="3:2 (travel, editorial) or 4:5 (looks)", typo="kicker 11/600 caps tertiary · h3 17/600 (2 lines) · metadata 12/500",
              meta="Source · read time", actions="Whole card is the tap target; long-press opens the tune sheet", states="default · pressed · visited (title to text-secondary) · loading",
              responsive="2 per row mobile grid; 3–4 per rail on tablet; 4–5 on desktop.", use="The default unit of the feed.", dont="Don't box it in a surface; don't add buttons."),
    "c": dict(conf=tk.REC, conf_note="Reconstruction based on news-list patterns in Glance's lock-screen news and trending modules.",
              dims="full width × 72 (thumb 72 × 72)", pad="0; 14px gap thumb→text", radius="12 on thumb",
              ratio="1:1 thumb", typo="body 15/600 (2 lines) · metadata 12/500 · optional kicker 10/600 caps",
              meta="Source · time ago · (rank metric)", actions="Trailing bookmark (22px) or none", states="default · pressed (row highlight surface) · read (title secondary)",
              responsive="Stacks on mobile; two columns on desktop.", use="Trending lists, notifications, search results, 'more from'.", dont="Don't use for hero content; don't show more than 5 in a ranked list."),
    "d": dict(conf=tk.INF, conf_note="Product tiles with brand, name, price and a save heart are strongly inferred from Glance AI's shoppable collections (400+ brand partners); freshness line is original.",
              dims="171 × auto in a 2-up grid (image 4:5 = 171 × 214)", pad="0; text below", radius="16 on image",
              ratio="4:5 (fashion, products on neutral ground); 1:1 for accessories", typo="brand caption 12/600 tertiary · name 13/500 (2 lines) · price h3 17/700 tabular · was-price 12 strike · off 12/600 success",
              meta="Store · freshness ('Price checked 9:41')", actions="Heart (32 circle, white 92%) top-right; whole card opens PDP", states="default · liked (heart filled signal, like-pop) · price-drop badge · out-of-stock (image 40% + 'Sold out' badge) · loading",
              responsive="2 per row mobile, 4 tablet, 5–6 desktop.", use="Any purchasable item.", dont="Don't write the price as free text from a model; render it from the catalogue/offer API with a timestamp."),
    "e": dict(conf=tk.ORIG, conf_note="Recommendation reasons ('Because you saved…') are an original interpretation of observed personalisation claims (feeds tuned by weather, trends, occasions, saves and dwell time).",
              dims="240 × 320 (3:4) in rails", pad="16", radius="16",
              ratio="3:4 full-bleed", typo="reason chip caption 12/600 iris · title h3 19/700 white (3 lines) · metadata 12/500 72% white",
              meta="Count · from-price or open-now", actions="Overflow (more) opens 'More like this / Less like this / Why'", states="default · pressed · dismissed (collapses, toast with Undo) · loading",
              responsive="Rail on all sizes; 5 visible on desktop.", use="Anything chosen by personalisation.", dont="Never show a recommendation without its reason; never phrase the reason as a claim about the user's identity."),
    "f": dict(conf=tk.ORIG, conf_note="Editorial serif treatment is an original interpretation of the observed 'fashion magazine where you are the model' positioning.",
              dims="358 wide; media 3:2", pad="0", radius="16 on media",
              ratio="3:2", typo="kicker 11/600 signal-light · display 30/1.08 serif · dek 13/400 (3 lines) · byline metadata",
              meta="Byline · read time", actions="Whole card; bookmark in the detail page", states="default · pressed · read",
              responsive="Full width mobile; 6 of 12 columns desktop with dek beside the image.", use="Long reads, guides, curated collections. Max one per screen.", dont="Don't use the serif anywhere else on the same screen."),
}


def card_render(s, key, x, y, theme="dark"):
    if key == "a":
        return c.card_hero(s, x, y), 448
    if key == "b":
        return c.card_standard(s, x, y)
    if key == "c":
        return c.card_compact(s, x, y), 72
    if key == "d":
        return c.card_commerce(s, x, y)
    if key == "e":
        return c.card_reco(s, x, y), 320
    if key == "f":
        return c.card_editorial(s, x, y)


def card_width(key):
    return {"a": 358, "b": 240, "c": 358, "d": 171, "e": 240, "f": 358}[key]


def cards():
    for key, slug, name, label in CARDS:
        sp = CARD_SPECS[key]
        # ---------- states sheet
        w_ = card_width(key)
        W = max(1600, 128 + 4 * w_ + 3 * 48) if key != "c" else 1600
        s = sheet(W, 900, f"Cards · {label}", name, f"{sp['use']} {sp['dont']}", f"{label} {name}", sp["conf"])
        states = ["Default", "Pressed", "Saved / active", "Loading"]
        x = 64
        for i, st in enumerate(states):
            s.add(section_label(x, 240, st))
            if st == "Loading":
                if key == "c":
                    s.add(rect(x, 260, 72, 72, DARK["surface-muted"], 12), rect(x + 86, 272, 200, 12, DARK["surface-muted"], 6),
                          rect(x + 86, 294, 150, 12, DARK["surface-muted"], 6), rect(x + 86, 316, 90, 9, DARK["surface-muted"], 4))
                elif key in ("a", "e"):
                    s.add(rect(x, 260, w_, 448 if key == "a" else 320, DARK["surface-muted"], 24 if key == "a" else 16))
                else:
                    s.add(c.skeleton_card(x, 260, w_, h_media=w_ * (5 / 4 if key == "d" else 2 / 3)))
            else:
                if st == "Pressed":
                    sc = .98
                    cx, cy = x + w_ / 2, 260 + 150
                    g, h_ = card_render(s, key, 0, 0)
                    s.add(f'<g transform="translate({x + w_ * .01} {260 + 3}) scale({sc})">{g}</g>')
                else:
                    g, h_ = card_render(s, key, x, 260)
                    s.add(g)
                    if st == "Saved / active":
                        if key == "d":
                            s.add(circle(x + w_ - 26, 286, 16, "#FFFFFF"))
                            s.add(icon("like", x + w_ - 36, 276, 20, "#FF0049", fill_color="#FF0049"))
                        elif key in ("a",):
                            s.add(circle(x + w_ - 36, 292, 20, "#FFFFFF"))
                            s.add(icon("bookmark", x + w_ - 46, 282, 20, "#0C0C10", fill_color="#0C0C10"))
                        elif key == "c":
                            s.add(icon("bookmark", x + w_ - 22, 285, 22, "#FFFFFF", fill_color="#FFFFFF"))
                        else:
                            g2, _ = c.toast(x, 260 + (h_ if isinstance(h_, (int, float)) else 300) + 20, "Saved", "Undo")
                            s.add(g2)
            x += w_ + 48 if key not in ("c",) else 0
            if key == "c":
                x = 64 + (i + 1) * 380
        s.add(line(64, 760, W - 64, 760, DARK["divider"]))
        s.add(text(64, 800, f"Dimensions: {sp['dims']}", "body-s", TS))
        s.add(text(64, 824, f"Ratio: {sp['ratio']} · Radius: {sp['radius']} · Padding: {sp['pad']}", "body-s", TS))
        s.save(f"{OUT}/cards/card-{key}-{slug}.svg")

        # ---------- anatomy sheet
        s = sheet(1600, 900, f"Cards · {label} · anatomy", f"{name}: anatomy", sp["conf_note"], f"{label} anatomy", sp["conf"])
        ox, oy = 180, 240
        g, h_ = card_render(s, key, ox, oy)
        s.add(g)
        h_ = h_ if isinstance(h_, (int, float)) else 300
        lx = 760
        parts = {
            "a": [("Media · full bleed", "4:5, scene fills the card", ox + 300, oy + 120), ("Badge · For you", "iris on media, 24px", ox + 60, oy + 28),
                  ("Save", "40px glass icon button", ox + 322, oy + 32), ("Kicker", "label 11/600 caps, 80% white", ox + 40, oy + 280),
                  ("Headline", "headline-media 26/700, ≤2 lines", ox + 120, oy + 318), ("Metadata", "source · time, 72% white", ox + 60, oy + 362),
                  ("Primary CTA", "button M, verb + object", ox + 80, oy + 406), ("Scrim", "bottom 55%, 0 → .85 black", ox + 250, oy + 250)],
            "b": [("Media", "3:2, radius 16, 1px inner stroke", ox + 120, oy + 80), ("Kicker", "11/600 caps tertiary", ox + 30, oy + 182),
                  ("Title", "h3 17/600, 2 lines", ox + 120, oy + 208), ("Metadata", "source · time", ox + 60, oy + 262)],
            "c": [("Thumbnail", "72 × 72, radius 12", ox + 36, oy + 36), ("Title", "body 15/600, 2 lines", ox + 180, oy + 20),
                  ("Metadata", "source · time ago", ox + 140, oy + 58), ("Trailing action", "bookmark 22", ox + 347, oy + 36)],
            "d": [("Image", "4:5 on neutral ground", ox + 80, oy + 110), ("Status badge", "price-drop, light", ox + 50, oy + 21),
                  ("Save", "32px white circle + heart", ox + 145, oy + 26), ("Brand", "caption 12/600", ox + 30, oy + 230),
                  ("Name", "13/500, 2 lines", ox + 90, oy + 256), ("Price row", "17/700 tabular + was + off", ox + 60, oy + 290),
                  ("Freshness", "success dot + time", ox + 60, oy + 310)],
            "e": [("Reason chip", "iris, sparkle + 'Because…'", ox + 120, oy + 26), ("Media", "3:4 full bleed + scrim", ox + 180, oy + 140),
                  ("Title", "h3 19/700 white, 3 lines", ox + 100, oy + 260), ("Metadata", "count · from-price", ox + 60, oy + 302),
                  ("Tune", "overflow → more/less/why", ox + 216, oy + 290)],
            "f": [("Media", "3:2, radius 16", ox + 180, oy + 110), ("Kicker", "signal-light caps", ox + 50, oy + 264),
                  ("Serif headline", "display 30/1.08", ox + 200, oy + 300), ("Dek", "body-s 13, 3 lines", ox + 200, oy + 380),
                  ("Byline", "metadata", ox + 80, oy + 426)],
        }[key]
        parts = sorted(parts, key=lambda p: p[3])
        for i, (lab, sub, px, py) in enumerate(parts):
            callout(s, i + 1, px, py, lx, 270 + i * 56, lab, sub)
        w_ = card_width(key)
        dim(s, ox, oy - 14, ox + w_, oy - 14, f"{w_}")
        # spec table
        tx = 1160
        rows = [("Dimensions", sp["dims"]), ("Radius", sp["radius"]), ("Padding", sp["pad"]), ("Image ratio", sp["ratio"]),
                ("Type", sp["typo"]), ("Metadata", sp["meta"]), ("Actions", sp["actions"]), ("States", sp["states"]), ("Responsive", sp["responsive"])]
        yy = 262
        for lab, val in rows:
            s.add(text(tx, yy, lab, "label", TT, upper=True, size=10))
            t_, th = para(tx, yy + 18, val, 376, "body-s", TS, max_lines=3, lh=1.35)
            s.add(t_)
            yy += 22 + th + 10
        s.save(f"{OUT}/cards/card-{key}-{slug}-anatomy.svg")

        md(f"cards/card-{key}-{slug}.md", f"""
# {label} · {name}

![{name}](card-{key}-{slug}.svg)
![{name} anatomy](card-{key}-{slug}-anatomy.svg)

**Confidence:** {sp['conf']} {tk.CONF_NAME[sp['conf']]} — {sp['conf_note']}

| Property | Value |
|---|---|
| Dimensions | {sp['dims']} |
| Padding | {sp['pad']} |
| Radius | {sp['radius']} |
| Image ratio | {sp['ratio']} |
| Typography | {sp['typo']} |
| Metadata | {sp['meta']} |
| Actions | {sp['actions']} |
| States | {sp['states']} |
| Responsive | {sp['responsive']} |

**Use:** {sp['use']}

**Don't:** {sp['dont']}

**Tokens:** `--radius-{'xl' if key == 'a' else 'm' if key == 'c' else 'l'}`, `--scrim-bottom`, `--type-{'headline-media' if key == 'a' else 'display' if key == 'f' else 'h3'}-*`,
`--color-text-tertiary` (metadata), `--color-{'iris' if key == 'e' else 'primary-action'}`.
""")

    # catalogue of remaining card types
    s = sheet(1600, 1620, "Cards · catalogue", "Card catalogue",
              "Ten card types from six anatomies. Featured = A; vertical = B; horizontal = C. News and media cards are B variants "
              "with a source row and a video control.", "Card catalogue")
    g, h_ = c.card_news(s, 64, 250, 358)
    s.add(g)
    s.add(text(64, 250 + h_ + 24, "News card · B variant · 16:9 + source row", "caption", TT))
    g, h_ = c.card_video(s, 470, 250, 358)
    s.add(g)
    s.add(text(470, 250 + h_ + 24, "Media card · video · B variant", "caption", TT))
    s.add(c.card_compact(s, 876, 250, 660, "desert", "Sam sand dunes: camps reopen 1 Oct", ("Rajasthan", "5 min")))
    s.add(c.card_compact(s, 876, 346, 660, "food", "The ₹99 thali everyone is queueing for", ("Food", "Pune", "8 min")))
    s.add(text(876, 450, "Horizontal card · C", "caption", TT))
    y2 = 660
    g, h_ = c.card_standard(s, 64, y2, 171, "beach-city", "Travel", "Panjim after dark", ("6 min",), ratio=(4, 5))
    s.add(g)
    s.add(text(64, y2 + h_ + 24, "Vertical card · B at 4:5", "caption", TT))
    g, h_ = c.card_commerce(s, 283, y2, 171, "bag", "Loom & Co", "Canvas weekender tote", "₹2,190", None, None, badge_=None, fresh="Price checked 9:41")
    s.add(g)
    s.add(text(283, y2 + h_ + 24, "Commerce · D, no discount", "caption", TT))
    g, h_ = c.card_commerce(s, 502, y2, 171, "watch", "Arc", "Field watch, 38mm", "₹8,450", "₹9,990", "15% off", badge_=("Only 3 left", "warning"),
                            fresh="Price checked 9:41")
    s.add(g)
    s.add(text(502, y2 + h_ + 24, "Commerce · D, scarcity", "caption", TT))
    s.add(c.card_reco(s, 740, y2, 300, 300, "mountain", "Popular with people like you", "Sikkim in the shoulder season", ("22 guides", "3–5 days")))
    s.add(text(740, y2 + 324, "Recommendation · E, square", "caption", TT))
    g, h_ = c.card_editorial(s, 1100, y2, 436, ratio=(16, 9))
    s.add(g)
    s.add(text(1100, y2 + h_ + 20, "Editorial · F at 16:9", "caption", TT))
    y3 = 1100
    s.add(c.card_hero(s, 64, y3, 800, 420, "concert", "Music · Live", "Monsoon fest: the whole lineup, live tonight", ("Wake Live", "starts 8pm"), "Set reminder",
                      badge_kind="live", badge_label="Live"))
    s.add(text(64, y3 + 444, "Featured · A at 16:9 (desktop)", "caption", TT))
    s.save(f"{OUT}/cards/card-catalogue.svg")

    md("cards/README.md", """
# Cards

Cards are the system's main unit. Six anatomies (A–F) cover every card type; the catalogue shows how news, media, featured,
horizontal and vertical cards derive from them.

| Card | File | Anatomy | Job |
|---|---|---|---|
| A · Large hero | [card-a-hero.md](card-a-hero.md) | media full-bleed + scrim + text on media + CTA | The one thing that matters now |
| B · Standard | [card-b-standard.md](card-b-standard.md) | media on top, text on ground | Default feed unit |
| C · Compact | [card-c-compact.md](card-c-compact.md) | thumb + two lines | Lists, trending, results |
| D · Commerce | [card-d-commerce.md](card-d-commerce.md) | product image + brand + price row + freshness | Anything purchasable |
| E · Recommendation | [card-e-recommendation.md](card-e-recommendation.md) | full-bleed + iris reason chip | Anything chosen by personalisation |
| F · Editorial | [card-f-editorial.md](card-f-editorial.md) | media + serif headline + dek | Long reads, guides |

![Card catalogue](card-catalogue.svg)

## Card system rules
- **Image-to-text ratio:** media takes 60–75% of the card's area on B, D, F and 100% on A, E. Text never exceeds 3 lines.
- **Aspect ratios:** 4:5 people/products, 3:2 places/editorial, 16:9 video/news, 3:4 recommendation, 1:1 thumbnails.
- **Radius:** 24 hero · 16 standard · 12 compact thumb · 0 full-bleed.
- **Overlay:** text on media only over `--scrim-bottom`; controls on media are glass.
- **Metadata:** one line, middle-dot separated, tabular numerals, text-tertiary (72% white on media).
- **CTA placement:** only Card A carries a button. Every other card is itself the tap target.
- **Density:** mobile shows 1 hero + ~1.5 rail cards above the fold, never more than 4 distinct things.
- **Hierarchy:** A > F > E > B/D > C. One A and at most one F per screen.
""")


# ====================================================================== assistant (case extension)
def assistant():
    s = sheet(1600, 1260, "Components · 07 · extension", "Assistant answer cards",
              "How the system extends to an AI travel assistant. Facts that change by the second are rendered as cards from their source; "
              "rules are quoted with the source attached; when neither is possible the assistant says so and hands off.", "Assistant cards", tk.ORIG)
    s.add(section_label(64, 240, "Fare card · live"))
    g, h_ = c.price_card(64, 260, 380)
    s.add(g)
    s.add(section_label(480, 240, "Fare card · cached (supplier timed out)"))
    g, h_ = c.price_card(480, 260, 380, state="stale", fresh="Cached 9:32 · couldn't reach airline", cta="Check live price")
    s.add(g)
    s.add(section_label(896, 240, "Fare card · price changed"))
    g, h_ = c.price_card(896, 260, 380, state="changed", fresh="Re-checked 9:44", cta="Continue at ₹5,842")
    s.add(g)
    s.add(section_label(64, 580, "Policy answer · cited"))
    g, h_ = c.policy_card(64, 600, 380)
    s.add(g)
    s.add(section_label(480, 580, "No source → deflect + handoff"))
    g, h_ = c.deflect_card(480, 600, 380)
    s.add(g)
    s.add(section_label(896, 580, "Conversation"))
    g, h1 = c.chat_bubble_user(1276, 600, "Cheapest flight Delhi to Goa this Friday?")
    s.add(g)
    g, h2 = c.assistant_line(896, 600 + h1 + 16, 380, "Checking live fares across 6 airlines…")
    s.add(g)
    s.add(c.skeleton_card(930, 600 + h1 + 60, 300, h_media=60))
    s.add(section_label(1330, 240, "Rules"))
    rules = ["The number on a fare card is rendered from the fare API response and bound to its offer ID. The model never types a price.",
             "Every fare shows its freshness: 'Live · checked 9:41' (green) or 'Cached 9:32' (amber).",
             "Policy answers carry a source row: publisher, page, last-verified date, external link.",
             "No retrieved source = no answer. Deflect to the official page and offer a human.",
             "Changed price = dialog with the new value in the primary label; nothing is charged silently."]
    y = 262
    for r_ in rules:
        t_, th = para(1330, y, r_, 220, "body-s", TS)
        s.add(t_)
        y += th + 14
    s.save(f"{OUT}/assistant/assistant-cards.svg")
    md("assistant/README.md", """
# Assistant answer cards (extension)

![Assistant cards](assistant-cards.svg)

**Confidence:** ◇ original interpretation. This folder shows how the Glance-inspired system extends to a conversational travel assistant,
the product in the case study. Glance's own roadmap mentions expanding the AI commerce platform to travel (press release, 2025), but no
travel UI is public, so nothing here is observed.

| Component | Purpose | Key rule |
|---|---|---|
| Fare card (live) | Show a flight option and price | Price rendered from the fare API response, bound to an offer ID; "Live · checked HH:MM" in success |
| Fare card (cached) | Supplier timed out or rate-limited | Amber "Cached" badge + timestamp; CTA becomes "Check live price", never "Book" |
| Fare card (changed) | Price moved between quote and decision | Amber "Price changed" + was-price; confirm via dialog |
| Policy answer (cited) | Visa, baggage, refund rules | Answer text constrained to the retrieved snippet; source row with publisher + last-verified date + link |
| Deflect card | No source found or source changed recently | Says so plainly; secondary button to the official page; tertiary to a human |
| Conversation | User bubble (inverse), assistant line (iris avatar), skeleton while checking | "Checking live fares…" state covers the 1–2s supplier latency |

These map one-to-one to the case plan: Option A (live price + fallback), Option B (cite-or-deflect) and the human handoff.
""")


if __name__ == "__main__":
    buttons(); chips(); badges(); inputs(); tabs(); navigation(); carousels(); content_modules(); media_modules(); overlays(); cards(); assistant()
    print("components ok")
