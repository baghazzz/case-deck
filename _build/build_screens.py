"""09 screen templates, 12 UI examples: every screen is built from components.py."""
import tokens as tk
import svgkit as k
import components as c
from svgkit import text, rect, line, circle, path, para, icon, tw, group, media
from sheets import sheet, section_label
from components import DARK as P, LIGHT

ROOT = "/home/claude/out/glance-inspired-design-system"
W, H = 390, 844


def sb(x, y, color="#FFFFFF"):
    return k.status_bar(x, y, W, color)


# ---------------------------------------------------------------- screens
def s_lockscreen(svg, x, y, w, h, scene="lagoon", kick="Travel · For you",
                 title="Monsoon's over. Six beaches worth a long weekend", meta=("Wake Travel", "4 min"), cta="Explore", fare=None):
    o = [media(svg, x, y, w, h, scene)]
    o.append(k.scrim_top(svg, x, y, w, 260, .5))
    o.append(k.scrim_bottom(svg, x, y, w, h, .42, .9))
    o.append(sb(x, y))
    o.append(icon("lock", x + w / 2 - 9, y + 60, 18, "#FFFFFF"))
    o.append(text(x + w / 2, y + 112, "Wednesday, 30 September", "button", "#FFFFFF", anchor="middle", size=17, weight=600))
    o.append(text(x + w / 2, y + 200, "9:41", "h1", "#FFFFFF", anchor="middle", size=96, weight=600, ls=-.03, tnum=True))
    lines = k.wrap(title, w - 40, "headline-media", size=28)[:3]
    by = y + h - 150 - 176 - (len(lines) - 1) * 32
    o.append(c.story_bars(x + 20, by - 30, w - 40, 5, 1, .55))
    b, bw = c.badge(x + 20, by, "For you" if not fare else "Live fare", "for-you" if not fare else "live-fare", on_media=True, h=24)
    o.append(b)
    o.append(c.kicker(x + 20, by + 50, kick, "rgba(255,255,255,.8)"))
    for i, ln in enumerate(lines):
        o.append(text(x + 20, by + 86 + i * 32, ln, "headline-media", "#FFFFFF", size=28))
    my = by + 86 + (len(lines) - 1) * 32 + 26
    o.append(k.meta(x + 20, my, meta, "rgba(255,255,255,.72)"))
    o.append(c.button(x + 20, my + 18, cta, "primary" if fare else "tertiary", "M", on_media=True, trailing="arrow"))
    o.append(c.icon_button(x + w - 20 - 44, my + 18, "share", variant="glass"))
    o.append(c.icon_button(x + w - 20 - 96, my + 18, "like", variant="glass"))
    o.append(c.icon_button(x + 30, y + h - 76, "live", variant="glass", size=44))
    o.append(c.icon_button(x + w - 74, y + h - 76, "camera", variant="glass", size=44))
    o.append(text(x + w / 2, y + h - 48, "Swipe for next story", "caption", "rgba(255,255,255,.64)", anchor="middle"))
    o.append(k.home_indicator(x, y + h, w))
    return "".join(o)


def s_home(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y), c.top_bar(x, y + 50, w, bell_badge="3")]
    o.append(text(x + 16, y + 150, "Good morning, Aria", "h1", P["text-primary"], size=28))
    o.append(k.meta(x + 16, y + 174, ("Wed 30 Sep", "31° Delhi", "3 new for you"), P["text-tertiary"]))
    o.append(c.category_tabs(x + 16, y + 216, ["For you", "Travel", "Style", "News", "Cricket", "Food"], 0))
    o.append(c.card_hero(svg, x + 16, y + 244, w - 32, 420))
    o.append(c.section_header(x + 16, y + 704, w - 32, "Because you saved Goa", iris=True, sub="Tuned to beaches · monsoon · under ₹8k"))
    xx = x + 16
    for sc, t_ in [("beach-city", "Sunset rooftops of Panjim"), ("desert", "Desert camps reopen")]:
        o.append(c.card_reco(svg, xx, y + 740, 240, 300, sc, "Because you saved Goa", t_, ("8 stays", "from ₹3,200")))
        xx += 252
    o.append(c.bottom_nav(x, y + h, w, 0))
    return "".join(o)


def s_discovery(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y)]
    o.append(text(x + 16, y + 104, "Discover", "h1", P["text-primary"], size=30))
    o.append(c.icon_button(x + w - 60, y + 72, "filter", variant="muted"))
    o.append(c.search_field(x + 16, y + 128, w - 32))
    o.append(c.chip_row(x + 16, y + 192, ["All", ("Near me", "location"), "Beaches", "Hills", "Food"], selected_index=0))
    cw = (w - 32 - 12) / 2
    cols = [[("lagoon", 230, "Beaches", "142 places"), ("food", 170, "Food trails", "38 walks"), ("stadium", 200, "Live cricket", "4 matches")],
            [("studio", 170, "Street style", "Starring you"), ("mountain", 230, "Hill towns", "61 guides"), ("concert", 200, "Music fests", "12 this month")]]
    for ci, col in enumerate(cols):
        yy = y + 246
        for sc, hh, t_, m_ in col:
            xx = x + 16 + ci * (cw + 12)
            o.append(media(svg, xx, yy, cw, hh, sc, 16))
            o.append(k.scrim_bottom(svg, xx, yy, cw, hh, .3, .8, 16))
            if m_ == "Starring you":
                o.append(c.badge(xx + 10, yy + 10, "Starring you", "for-you", on_media=True)[0])
            o.append(text(xx + 12, yy + hh - 32, t_, "h3", "#FFFFFF", size=17, weight=700))
            o.append(text(xx + 12, yy + hh - 13, m_, "caption", "rgba(255,255,255,.72)"))
            yy += hh + 12
    o.append(c.bottom_nav(x, y + h, w, 1))
    return "".join(o)


def s_content_detail(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), media(svg, x, y, w, 380, "temple")]
    o.append(k.scrim_top(svg, x, y, w, 140, .5))
    o.append(k.scrim_bottom(svg, x, y + 180, w, 200, .2, .9))
    o.append(sb(x, y))
    o.append(c.top_bar(x, y + 48, w, on_media=True, left="back", right=("bookmark", "share")))
    o.append(c.kicker(x + 20, y + 350, "The long read · Varanasi", "rgba(255,255,255,.85)"))
    t_, th = para(x + 20, y + 414, "Forty-eight hours in a city that wakes before you do", w - 40, "display", P["text-primary"], size=36, lh=1.04)
    o.append(t_)
    yy = y + 414 + th
    o.append(c.avatar(x + 20, yy - 4, 28, "M"))
    o.append(k.meta(x + 56, yy + 15, ("Meera Rao", "9 min read", "Updated 28 Sep"), P["text-tertiary"]))
    b, bh = para(x + 20, yy + 58, "Dawn on the ghats, lunch in the lanes, and the ceremony worth staying up for. A slow itinerary, built around when the city is at its best.",
                 w - 40, "body-l", P["text-secondary"])
    o.append(b)
    yy += 58 + bh + 10
    o.append(text(x + 20, yy + 10, "Day one · before sunrise", "h2", P["text-primary"], size=20))
    b, bh2 = para(x + 20, yy + 40, "Be at Assi ghat by 5:15. The boats leave when there is just enough light to see the far bank.", w - 40, "body", P["text-secondary"])
    o.append(b)
    # sticky action bar
    o.append(rect(x, y + h - 110, w, 110, "rgba(12,12,16,.96)"))
    o.append(line(x, y + h - 110, x + w, y + h - 110, P["divider"]))
    o.append(text(x + 20, y + h - 70, "Trips from ₹8,400", "h3", P["text-primary"], tnum=True))
    o.append(circle(x + 23, y + h - 49, 3, P["success"]))
    o.append(text(x + 32, y + h - 45, "Live · checked 9:41", "caption", P["success"], size=11, weight=600))
    bwid = c.button_width("Plan this trip", "M", trailing="arrow")
    o.append(c.button(x + w - 20 - bwid, y + h - 88, "Plan this trip", "primary", "M", trailing="arrow"))
    o.append(k.home_indicator(x, y + h, w))
    return "".join(o)


def s_commerce(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y)]
    o.append(text(x + 16, y + 104, "Style", "h1", P["text-primary"], size=30))
    o.append(c.segmented(x + w - 16 - 200, y + 76, ["Looks", "Products"], 0, w=200))
    o.append(media(svg, x + 16, y + 132, w - 32, 400, "studio", 24))
    o.append(k.scrim_bottom(svg, x + 16, y + 132, w - 32, 400, .45, .85, 24))
    o.append(c.badge(x + 32, y + 148, "Starring you", "for-you", on_media=True, h=24)[0])
    for (px, py) in [(x + 230, y + 250), (x + 238, y + 380)]:
        o.append(circle(px, py, 14, "rgba(255,255,255,.35)") + circle(px, py, 7, "#FFFFFF"))
    o.append(c.kicker(x + 36, y + 452, "Saturday brunch · 26°", "rgba(255,255,255,.8)"))
    o.append(text(x + 36, y + 484, "The red coat, three ways", "headline-media", "#FFFFFF"))
    o.append(k.meta(x + 36, y + 508, ("4 pieces", "from 3 stores"), "rgba(255,255,255,.72)"))
    o.append(c.section_header(x + 16, y + 572, w - 32, "Shop the look", action="All 4"))
    cw = (w - 32 - 12) / 2
    g, _ = c.card_commerce(svg, x + 16, y + 592, cw, "bag", "Loom & Co", "Canvas weekender tote", "₹2,190", None, None, badge_=None)
    o.append(g)
    g, _ = c.card_commerce(svg, x + 16 + cw + 12, y + 592, cw, "sneaker", liked=True)
    o.append(g)
    o.append(c.bottom_nav(x, y + h, w, 0))
    return "".join(o)


def s_product_detail(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), media(svg, x, y, w, 370, "sneaker"), sb(x, y, "#0C0C10")]
    o.append(c.icon_button(x + 12, y + 56, "back", variant="inverse", size=40))
    o.append(c.icon_button(x + w - 104, y + 56, "share", variant="inverse", size=40))
    o.append(c.icon_button(x + w - 56, y + 56, "like", variant="inverse", size=40))
    o.append(c.page_dots(x + w / 2, y + 346, 4, 0))
    yy = y + 404
    o.append(text(x + 20, yy, "Northline", "caption", P["text-tertiary"], weight=600))
    o.append(text(x + 20, yy + 32, "Court low sneaker", "h1", P["text-primary"], size=26))
    o.append(icon("star", x + 20, yy + 46, 16, P["warning"], fill_color=P["warning"]))
    o.append(k.meta(x + 42, yy + 59, ("4.6", "1,284 ratings", "Signal red"), P["text-tertiary"]))
    o.append(text(x + 20, yy + 104, "₹4,299", "h1", P["text-primary"], size=28, tnum=True))
    o.append(text(x + 124, yy + 104, "₹5,999", "metadata", P["text-tertiary"], tnum=True))
    o.append(line(x + 124, yy + 100, x + 124 + tw("₹5,999", "metadata"), yy + 100, P["text-tertiary"]))
    o.append(text(x + 180, yy + 104, "28% off", "metadata", P["success"], weight=600))
    o.append(circle(x + 23, yy + 125, 3, P["success"]))
    o.append(text(x + 32, yy + 129, "Price checked 9:41 · sold by Northline", "caption", P["text-tertiary"], size=11))
    o.append(text(x + 20, yy + 172, "Size (UK)", "button", P["text-primary"], size=14))
    o.append(text(x + w - 20, yy + 172, "Size guide", "button", P["text-secondary"], size=14, anchor="end", weight=500))
    xx = x + 20
    for i, sz in enumerate(["6", "7", "8", "9", "10"]):
        o.append(rect(xx, yy + 186, 58, 44, c.INV["dark"][0] if i == 2 else P["surface-muted"], 12))
        o.append(text(xx + 29, yy + 214, sz, "button", c.INV["dark"][1] if i == 2 else (P["text-tertiary"] if i == 4 else P["text-primary"]), anchor="middle"))
        xx += 68
    o.append(rect(x + 20, yy + 246, w - 40, 56, P["iris-subtle"], 12))
    o.append(icon("personalization", x + 34, yy + 262, 20, P["iris"]))
    o.append(text(x + 64, yy + 272, "Fit confidence 86% in UK 8", "body-s", P["iris"], weight=600))
    o.append(text(x + 64, yy + 290, "Based on your last two sneaker purchases", "caption", P["text-tertiary"]))
    o.append(rect(x, y + h - 106, w, 106, "rgba(12,12,16,.96)") + line(x, y + h - 106, x + w, y + h - 106, P["divider"]))
    o.append(c.icon_button(x + 20, y + h - 88, "bookmark", variant="muted"))
    o.append(c.button(x + 76, y + h - 92, "Buy on Northline", "primary", "L", width=w - 96, trailing="external"))
    o.append(k.home_indicator(x, y + h, w))
    return "".join(o)


def s_profile(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y), c.top_bar(x, y + 50, w, title="You", left=None, right=("settings",))]
    o.append(c.avatar(x + 20, y + 124, 72, "A", svg=svg))
    o.append(text(x + 108, y + 156, "Aria Sen", "h1", P["text-primary"], size=24))
    o.append(k.meta(x + 108, y + 180, ("Delhi", "member since 2025"), P["text-tertiary"]))
    for i, (n, lab) in enumerate([("128", "Saved"), ("3", "Trips"), ("12", "Following")]):
        xx = x + 20 + i * 120
        o.append(text(xx, y + 244, n, "h2", P["text-primary"], tnum=True))
        o.append(text(xx, y + 264, lab, "caption", P["text-tertiary"]))
    o.append(line(x + 20, y + 290, x + w - 20, y + 290, P["divider"]))
    o.append(c.section_header(x + 20, y + 330, w - 40, "Your taste", iris=True, action="Edit", sub="Inferred from saves and reads. Tap to remove."))
    xx, yy = x + 20, y + 366
    for lab in ["Beaches", "Street style", "Cricket", "Monsoon travel", "Sneakers"]:
        g, ww = c.chip(xx, yy, lab, variant="iris", trailing="close")
        if xx + ww > x + w - 20:
            xx, yy = x + 20, yy + 44
            g, ww = c.chip(xx, yy, lab, variant="iris", trailing="close")
        o.append(g)
        xx += ww + 8
    yy += 70
    o.append(text(x + 20, yy, "Personalisation", "h3", P["text-primary"]))
    rows = [("Use my location for trips", "Suggestions near Delhi", True), ("Show why I'm seeing things", "Adds a reason to every pick", True),
            ("Starring-you images", "Uses your photo · delete anytime", True), ("Personalised lock screen", "Stories on your lock screen", False)]
    for i, (a, b, on) in enumerate(rows):
        ry = yy + 22 + i * 64
        o.append(text(x + 20, ry + 20, a, "body", P["text-primary"], weight=500))
        o.append(text(x + 20, ry + 40, b, "caption", P["text-tertiary"]))
        o.append(c.toggle(x + w - 64, ry + 10, on))
        o.append(line(x + 20, ry + 56, x + w - 20, ry + 56, P["divider"]))
    o.append(c.bottom_nav(x, y + h, w, 4))
    return "".join(o)


def s_search(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y)]
    o.append(c.icon_button(x + 8, y + 60, "back", variant="plain", size=40))
    o.append(c.search_field(x + 52, y + 56, w - 68, value="goa in october", focused=True))
    o.append(text(x + 16, y + 146, "Recent", "caption", P["text-tertiary"], weight=600))
    o.append(c.chip_row(x + 16, y + 158, [("Palolem", "clock"), ("red coat", "clock"), ("ind vs aus", "clock")], selected_index=-1))
    rows = [("search", "goa in october weather", None, P["text-secondary"]), ("plane", "Flights Delhi → Goa", "from ₹4,120 · live fare", P["text-secondary"]),
            ("hotel", "Goa stays open after monsoon", "212 places", P["text-secondary"]), ("news", "Goa beach season opens early", "News · 2h", P["text-secondary"])]
    yy = y + 226
    for ic, t_, sub, col in rows:
        o.append(icon(ic, x + 20, yy + 8, 20, col))
        o.append(text(x + 56, yy + 22, t_, "body", P["text-primary"]))
        if sub:
            o.append(text(x + 56, yy + 40, sub, "caption", P["text-tertiary"]))
        o.append(icon("arrow", x + w - 40, yy + 10, 18, P["text-tertiary"]))
        yy += 58
    o.append(rect(x + 16, yy + 8, w - 32, 132, P["iris-subtle"], 16))
    o.append(icon("personalization", x + 32, yy + 26, 20, P["iris"]))
    o.append(text(x + 60, yy + 41, "Ask Wake", "button", P["iris"]))
    t_, th = para(x + 32, yy + 72, "What's Goa like in October, and which beaches open first after the monsoon?", w - 64, "body", P["text-primary"])
    o.append(t_)
    o.append(text(x + 32, yy + 124, "Answers cite their sources", "caption", P["text-tertiary"]))
    yy += 170
    o.append(c.section_header(x + 16, yy, w - 32, "Top stories", action=None))
    o.append(c.card_compact(svg, x + 16, yy + 18, w - 32, "lagoon", "Six beaches worth the flight this October", ("Wake Travel", "4 min")))
    o.append(c.card_compact(svg, x + 16, yy + 106, w - 32, "beach-city", "Panjim after dark: rooftops that reopened", ("Wake Travel", "6 min")))
    return "".join(o)


def s_onboarding(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), media(svg, x, y, w, 230, "iris"), sb(x, y)]
    o.append(c.story_bars(x + 20, y + 62, w - 40, 3, 1, 1))
    o.append(text(x + w - 20, y + 104, "Skip", "button", "rgba(255,255,255,.72)", anchor="end"))
    o.append(k.scrim_bottom(svg, x, y + 110, w, 120, 0, 1))
    o.append(c.kicker(x + 20, y + 262, "Step 2 of 3", P["iris"]))
    t_, th = para(x + 20, y + 306, "Pick what wakes you up", w - 40, "display", P["text-primary"], size=40, lh=1.02)
    o.append(t_)
    b, bh = para(x + 20, y + 306 + th + 8, "Choose three or more. Your lock screen and feed start here; you can change this anytime.", w - 40, "body", P["text-secondary"])
    o.append(b)
    labels = ["Travel", "Street style", "Cricket", "Bollywood", "Food", "Tech", "Sneakers", "Beauty", "Music", "Wellness"]
    sel = {0, 1, 4}
    xx, yy = x + 20, y + 306 + th + bh + 30
    for i, lab in enumerate(labels):
        g, ww = c.chip(0, 0, lab, selected=i in sel, icon_name="check" if i in sel else "plus", h=40)
        if xx + ww > x + w - 20:
            xx, yy = x + 20, yy + 50
        g, ww = c.chip(xx, yy, lab, selected=i in sel, icon_name="check" if i in sel else "plus", h=40)
        o.append(g)
        xx += ww + 8
    o.append(icon("lock", x + 20, y + h - 150, 16, P["text-tertiary"]))
    o.append(text(x + 44, y + h - 137, "Your picks are private and never shown to others.", "caption", P["text-tertiary"]))
    o.append(c.button(x + 20, y + h - 112, "Continue · 3 picked", "primary", "L", width=w - 40))
    o.append(k.home_indicator(x, y + h, w))
    return "".join(o)


def s_news_feed(svg, x, y, w, h):
    o = [media(svg, x, y, w, h, "news"), k.scrim_top(svg, x, y, w, 200, .6), k.scrim_bottom(svg, x, y, w, h, .35, .92), sb(x, y)]
    o.append(c.category_tabs(x + 16, y + 92, ["For you", "National", "Business", "Sports", "World"], 1, on_media=True))
    o.append(c.story_bars(x + 16, y + 118, w - 32, 6, 2, .3))
    yy = y + h - 380
    o.append(circle(x + 30, yy, 12, "rgba(255,255,255,.2)"))
    o.append(text(x + 30, yy + 4, "L", "label", "#FFFFFF", anchor="middle", size=11))
    o.append(k.meta(x + 50, yy + 4, ("The Daily Ledger", "National", "18 min"), "rgba(255,255,255,.8)"))
    t_, th = para(x + 16, yy + 48, "Rail budget adds 40 new routes for the festive season", w - 90, "headline-media", "#FFFFFF", size=28)
    o.append(t_)
    b, bh = para(x + 16, yy + 48 + th + 4, "Most new services start 15 October. Bookings open this weekend on the usual channels.", w - 90, "body", "rgba(255,255,255,.8)", max_lines=3)
    o.append(b)
    o.append(c.button(x + 16, yy + 48 + th + bh + 16, "Read full story", "tertiary", "M", on_media=True, trailing="arrow"))
    for i, (ic, n) in enumerate([("like", "2.4k"), ("bookmark", ""), ("share", "")]):
        ry = y + h - 380 + i * 70
        o.append(c.icon_button(x + w - 60, ry, ic, variant="glass"))
        if n:
            o.append(text(x + w - 38, ry + 62, n, "caption", "#FFFFFF", anchor="middle", size=11))
    o.append(c.bottom_nav(x, y + h, w, 0))
    return "".join(o)


def s_entertainment(svg, x, y, w, h):
    o = [media(svg, x, y, w, h, "concert"), k.scrim_top(svg, x, y, w, 180, .5), k.scrim_bottom(svg, x, y, w, h, .5, .9), sb(x, y)]
    o.append(c.top_bar(x, y + 48, w, on_media=True, left="back", right=("more",)))
    o.append(c.badge(x + 60, y + 60, "Live", "live")[0])
    o.append(icon("profile", x + 116, y + 62, 16, "#FFFFFF"))
    o.append(text(x + 136, y + 75, "12.4k", "caption", "#FFFFFF", weight=600, tnum=True))
    ry = y + h - 430
    for i, (ic, n) in enumerate([("like", "48k"), ("chat", "1.2k"), ("share", "Share"), ("bookmark", "Save")]):
        o.append(c.icon_button(x + w - 62, ry + i * 76, ic, variant="glass", size=48))
        o.append(text(x + w - 38, ry + i * 76 + 66, n, "caption", "#FFFFFF", anchor="middle", size=11, weight=600))
    yy = y + h - 250
    o.append(c.avatar(x + 16, yy - 22, 32, "M"))
    o.append(text(x + 56, yy - 1, "Monsoon Fest · Stage 2", "button", "#FFFFFF", size=14))
    t_, th = para(x + 16, yy + 36, "Front row for the closing set, live from Pune", w - 100, "headline-media", "#FFFFFF", size=24)
    o.append(t_)
    o.append(k.meta(x + 16, yy + 36 + th + 2, ("Music", "Live", "ends 11:30pm"), "rgba(255,255,255,.72)"))
    o.append(c.chip(x + 16, yy + 36 + th + 20, "Continue: Day 1 highlights", variant="glass", icon_name="play")[0])
    o.append(rect(x + 16, y + h - 104, w - 32, 3, "rgba(255,255,255,.32)", 1.5))
    o.append(rect(x + 16, y + h - 104, (w - 32) * .72, 3, "#FF0049", 1.5))
    o.append(c.bottom_nav(x, y + h, w, 1))
    return "".join(o)


def s_notifications(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y), c.top_bar(x, y + 50, w, title="Updates", left="back", right=("settings",))]
    o.append(c.segmented(x + 16, y + 118, ["All", "Trips", "For you"], 0, w=w - 32))
    groups = [("Today", [("tag", P["success"], "#0F2E22", "Delhi → Goa dropped to ₹4,120", "Live fare · checked 9:32 · Fri 16 Oct", "2m", None),
                         ("personalization", P["iris"], P["iris-subtle"], "Your look for Saturday is ready", "Starring you · 4 pieces · 26° forecast", "1h", "studio"),
                         ("live", P["primary"], "#3A0716", "Monsoon Fest is live now", "Stage 2 · 12.4k watching", "3h", "concert")]),
              ("Earlier", [("passport", P["info"], "#0E2340", "Thailand entry rules page updated", "We re-checked the official page · cited", "Mon", None),
                           ("trending", P["text-primary"], P["surface-muted"], "Trending near you: the ₹99 thali", "Food · Pune · 48k saved", "Sun", "food"),
                           ("alert", P["warning"], "#33260A", "Hotel price changed for Palolem Bay", "Now ₹3,640/night (was ₹3,200)", "Sat", None)])]
    yy = y + 196
    for gname, items in groups:
        o.append(text(x + 16, yy, gname, "caption", P["text-tertiary"], weight=600))
        yy += 16
        for ic, col, bg, t_, sub, tm, thumb in items:
            o.append(circle(x + 38, yy + 30, 22, bg))
            o.append(icon(ic, x + 27, yy + 19, 22, col))
            tws = w - 76 - 16 - (56 if thumb else 0) - 30
            tl = k.wrap(t_, tws, "body", weight=600)[:2]
            for i, ln in enumerate(tl):
                o.append(text(x + 72, yy + 24 + i * 20, ln, "body", P["text-primary"], weight=600, size=14))
            o.append(text(x + 72, yy + 24 + len(tl) * 20, sub, "caption", P["text-tertiary"], size=11))
            o.append(text(x + w - 16, yy + 24, tm, "caption", P["text-tertiary"], anchor="end", size=11))
            if thumb:
                o.append(media(svg, x + w - 16 - 48, yy + 32, 48, 48, thumb, 8))
            yy += 88
        yy += 10
    o.append(c.bottom_nav(x, y + h, w, 0))
    return "".join(o)


def s_reco_feed(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y)]
    o.append(text(x + 16, y + 104, "For you", "h1", P["text-primary"], size=30))
    o.append(c.icon_button(x + w - 60, y + 72, "filter", variant="muted"))
    o.append(icon("personalization", x + 16, y + 122, 16, P["iris"]))
    o.append(text(x + 38, y + 135, "Tuned to travel · street style · cricket", "body-s", P["iris"], weight=500))
    o.append(text(x + w - 16, y + 135, "Edit", "button", P["text-secondary"], anchor="end", size=14, weight=500))
    items = [("lagoon", "Because you saved Goa", "Palolem after the rains", ("8 stays", "from ₹3,200")),
             ("studio", "Matches your street style", "The red coat, three ways", ("4 pieces", "Starring you")),
             ("stadium", "You follow India cricket", "Final over, every angle", ("Highlights", "4:12"))]
    yy = y + 160
    for i, (sc, rs, t_, m_) in enumerate(items):
        o.append(c.card_reco(svg, x + 16, yy, w - 32, 230, sc, rs, t_, m_))
        if i == 0:
            o.append(c.button(x + 16, yy + 242, "More like this", "tertiary", "S", icon_name="plus"))
            o.append(c.button(x + 16 + c.button_width("More like this", "S", "plus") + 8, yy + 242, "Less like this", "tertiary", "S", icon_name="close"))
            g, th = c.tooltip(x + 16, yy + 292, w - 32, "Why you're seeing this", "You saved two Goa stories this week. Tap to tune or turn this off.")
            o.append(g)
            yy += 242 + 50 + th + 16
        else:
            yy += 246
    o.append(c.bottom_nav(x, y + h, w, 0))
    return "".join(o)


# ---------------------------------------------------------------- travel assistant (case)
def s_assistant_chat(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y), c.top_bar(x, y + 50, w, title="Ask", left="back", right=("more",))]
    g, h1 = c.chat_bubble_user(x + w - 16, y + 120, "Cheapest flight Delhi to Goa this Friday?")
    o.append(g)
    g, h2 = c.assistant_line(x + 16, y + 120 + h1 + 20, w - 32, "I checked live fares across six airlines at 9:41. Here's the cheapest non-stop:")
    o.append(g)
    fy = y + 120 + h1 + 20 + h2 + 20
    g, fh = c.price_card(x + 16, fy, w - 32)
    o.append(g)
    o.append(text(x + 16, fy + fh + 26, "2 more options · from ₹6,105", "button", P["primary-light"], size=14))
    o.append(icon("chevron-down", x + 16 + tw("2 more options · from ₹6,105", "button", size=14) + 4, fy + fh + 12, 16, P["primary-light"]))
    qy = fy + fh + 50
    o.append(c.chip_row(x + 16, qy, [("Baggage allowance?", "baggage"), ("Visa for Thailand?", "passport")], selected_index=-1, max_x=x + w))
    o.append(rect(x, y + h - 104, w, 104, "rgba(12,12,16,.96)") + line(x, y + h - 104, x + w, y + h - 104, P["divider"]))
    o.append(rect(x + 16, y + h - 90, w - 32 - 56, 48, P["surface-muted"], 24))
    o.append(text(x + 36, y + h - 60, "Ask about fares, stays, rules…", "body", P["text-tertiary"]))
    o.append(c.icon_button(x + w - 16 - 48, y + h - 92, "mic", variant="primary", size=48))
    o.append(k.home_indicator(x, y + h, w))
    return "".join(o)


def s_assistant_policy(svg, x, y, w, h):
    o = [rect(x, y, w, h, P["background"]), sb(x, y), c.top_bar(x, y + 50, w, title="Ask", left="back", right=("more",))]
    g, h1 = c.chat_bubble_user(x + w - 16, y + 118, "Do I need a visa for Thailand on an Indian passport?")
    o.append(g)
    yy = y + 118 + h1 + 16
    g, ph = c.policy_card(x + 16, yy, w - 32)
    o.append(g)
    yy += ph + 20
    g, h3 = c.chat_bubble_user(x + w - 16, yy, "And for a 10-hour transit in Kuala Lumpur?")
    o.append(g)
    yy += h3 + 16
    g, dh = c.deflect_card(x + 16, yy, w - 32)
    o.append(g)
    o.append(k.home_indicator(x, y + h, w))
    return "".join(o)


def s_assistant_lock(svg, x, y, w, h):
    return s_lockscreen(svg, x, y, w, h, "plane", "Your saved trip · Delhi → Goa", "Friday's fare to Goa dropped to ₹4,120",
                        ("Live fare", "checked 9:32", "Skyline Air"), "See fare", fare=True)


SCREENS = {
    "lockscreen": (s_lockscreen, "Lock screen hook", "09"),
    "home": (s_home, "Personalised home", "09"),
    "discovery": (s_discovery, "Content discovery", "09"),
    "content-detail": (s_content_detail, "Content detail", "09"),
    "commerce": (s_commerce, "Commerce feed", "09"),
    "product-detail": (s_product_detail, "Product detail", "09"),
    "profile": (s_profile, "Profile", "09"),
    "search": (s_search, "Search", "09"),
    "onboarding": (s_onboarding, "Onboarding", "09"),
    "news-feed": (s_news_feed, "News feed", "09"),
    "entertainment-feed": (s_entertainment, "Entertainment feed", "09"),
    "notifications": (s_notifications, "Notifications", "09"),
    "recommendation-feed-screen": (s_reco_feed, "Recommendation feed", "09"),
    "assistant-chat": (s_assistant_chat, "Travel assistant · live fare", "12"),
    "assistant-policy": (s_assistant_policy, "Travel assistant · cited policy", "12"),
    "assistant-lockscreen": (s_assistant_lock, "Travel assistant · lock-screen alert", "12"),
}


def phone_svg(name, fn, title):
    s = k.Svg(W + 60, H + 60, title, f"{title}: phone screen template built from {tk.SYSTEM_NAME} components")
    s.add(k.phone(s, 30, 30, fn))
    return s


def build_single():
    paths = {}
    for n, (fn, title, folder) in SCREENS.items():
        s = phone_svg(n, fn, title)
        sub = "09_SCREEN_TEMPLATES" if folder == "09" else "12_UI_EXAMPLES/travel-assistant"
        p = f"{ROOT}/{sub}/{n.replace('-screen', '')}.svg"
        s.save(p)
        paths[n] = p
    return paths


def multi(fname, title, desc, names, kick="UI examples · 12", conf=tk.ORIG, captions=None):
    n = len(names)
    Wd = 128 + n * (W + 20) + (n - 1) * 60
    s = sheet(max(Wd, 1600), 1260, kick, title, desc, title, conf)
    x0 = (max(Wd, 1600) - (n * (W + 20) + (n - 1) * 60)) / 2 + 10
    for i, nm in enumerate(names):
        fn = SCREENS[nm][0]
        xx = x0 + i * (W + 80)
        s.add(k.phone(s, xx, 250, fn))
        cap = captions[i] if captions else SCREENS[nm][1]
        s.add(text(xx + W / 2, 250 + H + 50, cap, "button", P["text-secondary"], anchor="middle", size=14))
        if i < n - 1:
            s.add(icon("forward", xx + W + 28, 250 + H / 2 - 12, 24, P["text-tertiary"]))
    s.save(f"{ROOT}/12_UI_EXAMPLES/{fname}")


# ---------------------------------------------------------------- desktop examples
def desktop_dashboard():
    DW, DH = 1440, 960
    s = k.Svg(DW, DH, "Desktop dashboard", "Wake on the web: personalised home dashboard at 1440px", bg=P["background"])
    # left rail
    s.add(rect(0, 0, 240, DH, P["surface"]), line(240, 0, 240, DH, P["divider"]))
    s.add(c.wordmark(32, 58, "#FFFFFF", 28))
    items = [("home", "For you", True), ("grid", "Discover", False), ("personalization", "Ask", False), ("bookmark", "Saved", False),
             ("plane", "Trips", False), ("shopping", "Style", False), ("notification", "Updates", False)]
    for i, (ic, lab, act) in enumerate(items):
        yy = 110 + i * 48
        if act:
            s.add(rect(16, yy - 6, 208, 42, P["surface-muted"], 12), rect(16, yy + 4, 3, 22, P["primary"], 1.5))
        col = P["iris"] if ic == "personalization" else (P["text-primary"] if act else P["text-secondary"])
        s.add(icon(ic, 32, yy + 3, 22, col))
        s.add(text(68, yy + 20, lab, "body", col, weight=600 if act else 500))
    s.add(rect(16, DH - 140, 208, 112, P["iris-subtle"], 16))
    s.add(icon("personalization", 32, DH - 124, 18, P["iris"]))
    s.add(text(58, DH - 110, "Tuned to you", "caption", P["iris"], weight=700, size=13))
    t_, th = para(32, DH - 86, "Travel · street style · cricket. Change anytime.", 176, "caption", P["text-secondary"])
    s.add(t_)
    # header
    s.add(c.search_field(280, 28, 520, "Search stories, looks, trips"))
    s.add(c.icon_button(1300, 30, "notification", variant="muted", badge="3"))
    s.add(c.avatar(1356, 32, 40, "A", svg=s))
    s.add(text(280, 138, "Good morning, Aria", "display", P["text-primary"], size=48))
    s.add(k.meta(280, 168, ("Wednesday 30 September", "31° Delhi", "3 new for you"), P["text-tertiary"]))
    s.add(c.category_tabs(280, 214, ["For you", "Travel", "Style", "News", "Cricket", "Food", "Music"], 0))
    # hero 16:9
    s.add(c.card_hero(s, 280, 244, 720, 405, "lagoon", "Travel · For you", "Monsoon's over. Six beaches worth the flight", ("Wake Travel", "4 min"), "Plan a trip"))
    # right column
    rx = 1032
    s.add(c.section_header(rx, 262, 376, "Trending near you", action=None))
    for i, (sc, t_, m_) in enumerate([("stadium", "Final over: chase needs 12 off 6", "Cricket · 2.1M reading"),
                                     ("food", "The ₹99 thali everyone is queueing for", "Food · Pune"),
                                     ("concert", "Monsoon fest lineup drops tonight", "Music · 48k saved"),
                                     ("news", "Metro line 3 opens early", "City · 12 min")]):
        s.add(c.card_compact(s, rx, 284 + i * 92, 376, sc, t_, (m_,), rank=i + 1, trailing=None))
    # rail
    s.add(c.section_header(280, 700, 1128, "Because you saved Goa", iris=True, sub="Tuned to beaches · monsoon · under ₹8k"))
    for i, (sc, t_) in enumerate([("beach-city", "Sunset rooftops of Panjim"), ("desert", "Desert camps reopen"), ("mountain", "Hill towns after rain"),
                                  ("temple", "Heritage walks in Old Goa"), ("food", "Goan thali trail")]):
        s.add(c.card_reco(s, 280 + i * 230, 736, 218, 210, sc, "Because you saved Goa" if i < 2 else "Similar trips", t_, ("from ₹3,200",)))
    s.save(f"{ROOT}/12_UI_EXAMPLES/dashboard.svg")

    # commerce desktop
    s = k.Svg(DW, DH, "Desktop commerce feed", "Wake Style on the web: look + shoppable products at 1440px", bg=P["background"])
    s.add(rect(0, 0, DW, 80, P["background"]), line(0, 80, DW, 80, P["divider"]))
    s.add(c.wordmark(48, 52, "#FFFFFF", 28))
    s.add(c.category_tabs(220, 48, ["For you", "Travel", "Style", "News", "Cricket"], 2))
    s.add(c.search_field(900, 16, 380))
    s.add(c.avatar(1360, 20, 40, "A", svg=s))
    s.add(media(s, 48, 112, 520, 650, "studio", 24))
    s.add(k.scrim_bottom(s, 48, 112, 520, 650, .5, .85, 24))
    s.add(c.badge(68, 132, "Starring you", "for-you", on_media=True, h=24)[0])
    for (px, py) in [(330, 300), (340, 470), (300, 690)]:
        s.add(circle(px, py, 14, "rgba(255,255,255,.35)"), circle(px, py, 7, "#FFFFFF"))
    s.add(c.kicker(76, 650, "Saturday brunch · 26°", "rgba(255,255,255,.8)"))
    s.add(text(76, 688, "The red coat, three ways", "headline-media", "#FFFFFF", size=32))
    s.add(k.meta(76, 716, ("4 pieces", "3 stores", "prices checked 9:41"), "rgba(255,255,255,.72)"))
    s.add(text(608, 140, "Shop the look", "h1", P["text-primary"], size=32))
    s.add(c.chip_row(608, 166, ["All", "Coats", "Shoes", "Bags", "Under ₹5k"], selected_index=0))
    prods = [("bag", "Loom & Co", "Canvas weekender tote", "₹2,190", None, None, None), ("sneaker", "Northline", "Court low sneaker in signal red", "₹4,299", "₹5,999", "28% off", ("Price drop", "price-drop")),
             ("watch", "Arc", "Field watch, 38mm", "₹8,450", "₹9,990", "15% off", ("Only 3 left", "warning")), ("lamp", "Halo", "Lilac desk lamp", "₹1,850", None, None, ("New", "new")),
             ("studio", "Marlow", "Wool-blend coat, signal red", "₹6,499", None, None, ("For you", "for-you")), ("sneaker", "Northline", "Court low, white", "₹4,299", None, None, None),
             ("bag", "Loom & Co", "Mini crossbody", "₹1,490", "₹1,990", "25% off", None), ("watch", "Arc", "Field watch, 40mm", "₹8,990", None, None, None)]
    for i, (sc, br, nm, pr, was, off, bd) in enumerate(prods):
        xx = 608 + (i % 4) * 202
        yy = 222 + (i // 4) * 370
        g, h_ = c.card_commerce(s, xx, yy, 184, sc, br, nm, pr, was, off, badge_=bd)
        s.add(g)
    s.save(f"{ROOT}/12_UI_EXAMPLES/commerce-feed.svg")


def build():
    build_single()
    multi("personalized-home.svg", "Personalised home, three moments",
          "From the lock screen to the app: the same story is the hook, the hero, and then the detail. Personalisation is shown by what "
          "appears and by one iris line saying why.", ["lockscreen", "home", "content-detail"],
          captions=["1 · Wake: the hook on the lock screen", "2 · Open: the hook becomes the hero", "3 · Deep dive: detail with live price"])
    multi("content-feed.svg", "Content feeds",
          "News and entertainment share one full-bleed vertical grammar: category tabs over media, progress at the top, text on the "
          "bottom scrim, actions on the right edge.", ["news-feed", "entertainment-feed", "discovery"], conf=tk.INF,
          captions=["News · full-bleed story", "Entertainment · live video", "Discovery · masonry"])
    multi("recommendation-feed.svg", "Recommendation feed",
          "Every recommendation carries its reason. The first card teaches the controls: more, less, and why.",
          ["recommendation-feed-screen", "notifications", "profile"],
          captions=["For you · reasons + tuning", "Updates · data-backed alerts", "You · inferred taste, editable"])
    multi("travel-assistant/travel-assistant-flow.svg", "Travel assistant, grounded",
          "The case-study product in this system: a lock-screen fare alert bound to a live quote, a fare card rendered from the API, "
          "and policy answers that cite or defer.", ["assistant-lockscreen", "assistant-chat", "assistant-policy"],
          kick="UI examples · 12 · case application",
          captions=["Alert: live fare, timestamped", "Answer: fare card from the API", "Rules: cite, or deflect and hand off"])
    desktop_dashboard()


if __name__ == "__main__":
    build()
    print("screens ok")
