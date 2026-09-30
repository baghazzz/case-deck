"""13: deck assets — 1920×1080 SVG slides built from the same components, plus PNG exports."""
import tokens as tk
import svgkit as k
import components as c
import content as ct
import build_screens as bs
from svgkit import text, rect, line, circle, path, para, icon, tw, group, media
from components import DARK as P

OUT = "/home/claude/out/glance-inspired-design-system/13_DECK_ASSETS"
SW, SH = 1920, 1080
M = 120


def slide(title_, desc, kick=None, num=None, bg=True):
    s = k.Svg(SW, SH, title_, desc, bg=P["background"] if bg else None)
    if kick:
        s.add(text(M, 132, kick, "label", P["primary"], upper=True, size=16))
    if num:
        s.add(text(SW - M, SH - 60, num, "metadata", P["text-tertiary"], anchor="end", size=16))
    s.add(text(M, SH - 60, f"{tk.SYSTEM_NAME} · {tk.SYSTEM_TAG}", "metadata", P["text-tertiary"], size=16))
    return s


def title_block(s, t, sub=None, y=236, size=88, width=1100):
    tt, th = para(M, y, t, width, "display", P["text-primary"], size=size, lh=1.0)
    s.add(tt)
    if sub:
        st, sh = para(M, y + th + 10, sub, 820, "body-l", P["text-secondary"], size=24, lh=1.4)
        s.add(st)
        return th + sh + 10
    return th


def phone_at(s, x, y, fn, scale=1.0):
    inner = k.phone(s, 0, 0, fn)
    return f'<g transform="translate({x} {y}) scale({scale})">{inner}</g>'


def build():
    slides = {}

    # 1 title
    s = slide("Title slide", "Cover visual")
    gid, g = k.rad_grad([(0, "#FF0049", .28), (1, "#FF0049", 0)], .82, .3, .55)
    s.define(g)
    s.add(rect(0, 0, SW, SH, f"url(#{gid})"))
    s.add(text(M, 190, "Product case study · design system", "label", P["primary"], upper=True, size=16))
    s.add(c.wordmark(M, 440, "#FFFFFF", 200))
    s.add(text(M, 540, "A Glance-inspired design system", "display", P["text-primary"], size=56))
    t_, th = para(M, 610, "Principles, tokens, components and screens for a wake-first, media-led, trustworthy product.", 760, "body-l", P["text-secondary"], size=24)
    s.add(t_)
    s.add(k.meta(M, 780, ("v1.0", "September 2026", "Original artwork · not a Glance asset"), P["text-tertiary"]))
    s.add(phone_at(s, 1120, 150, bs.s_lockscreen, .92))
    s.add(phone_at(s, 1480, 230, bs.s_home, .82))
    slides["title-slide"] = s

    # 2 design DNA
    s = slide("Design DNA", "Five traits that define the language", "Design DNA", "02")
    title_block(s, "Five traits, one language", "What makes a Glance-like interface feel like itself, reduced to five rules a team can check a screen against.")
    for i, (n, d, ic) in enumerate(ct.DNA):
        x = M + i * 344
        y = 560
        s.add(rect(x, y, 320, 360, P["surface"], 24))
        s.add(circle(x + 56, y + 64, 32, P["iris-subtle"] if ic == "personalization" else "#3A0716" if ic == "live" else P["surface-muted"]))
        s.add(icon(ic, x + 40, y + 48, 32, P["iris"] if ic == "personalization" else P["primary"] if ic == "live" else P["text-primary"]))
        s.add(text(x + 28, y + 150, f"0{i + 1}", "metadata", P["text-tertiary"], size=16))
        tt, th = para(x + 28, y + 196, n, 270, "display", P["text-primary"], size=36, lh=1.02)
        s.add(tt)
        dd, dh = para(x + 28, y + 196 + th + 12, d, 270, "body", P["text-secondary"], size=18)
        s.add(dd)
    slides["design-dna-slide"] = s

    # 3 visual language
    s = slide("Visual language", "Imagery-first cards, one red, one lavender, two families", "Visual language", "03")
    title_block(s, "A dark stage. Imagery does the talking.", "One red for action and live. Lavender for anything about you. Serif for the editorial moment; Inter for everything you read fast.", width=760)
    s.add(c.card_hero(s, 1010, 150, 380, 475))
    s.add(c.card_reco(s, 1420, 150, 380, 475, "studio", "Matches your street style", "The red coat, three ways", ("4 pieces", "Starring you")))
    s.add(c.chip_row(M, 660, ["For you", ("Street style", "personalization"), "Cricket", "Beaches"], selected_index=0))
    bx = M
    for kd, lab in [("live", "Live"), ("for-you", "For you"), ("live-fare", "Live fare"), ("verified", "Cited")]:
        g, bw = c.badge(bx, 730, lab, kd)
        s.add(g)
        bx += bw + 12
    for i, n in enumerate(["home", "search", "personalization", "like", "bookmark", "share", "plane", "passport", "trending", "live"]):
        s.add(icon(n, M + i * 64, 800, 32, P["iris"] if n == "personalization" else "#FFFFFF"))
    s.add(text(M, 930, "Aa", "display", P["text-primary"], size=96))
    s.add(text(M + 150, 930, "Aa", "h1", P["text-primary"], size=96))
    s.add(c.card_compact(s, 1010, 690, 790, "stadium", "Final over: chase needs 12 off 6", ("Cricket", "Live", "2.1M reading")))
    s.add(c.card_compact(s, 1010, 790, 790, "food", "The ₹99 thali everyone is queueing for", ("Food", "Pune")))
    slides["visual-language-slide"] = s

    # 4 colour
    s = slide("Color system", "Palette and meaning", "Colour system", "04")
    title_block(s, "Red means now. Lavender means you.", "#FF0049 and #DDBEF0 are observed brand hues. Everything else is reconstructed around one idea: colour is a job, not a mood.", width=1300)
    groups = [("primary", "Signal", "Action · live"), ("primary-action", "Signal action", "Buttons (4.73:1)"), ("iris", "Iris", "You · AI · why"),
              ("iris-subtle", "Iris subtle", "Reason grounds"), ("stage", "Stage", "Media ground"), ("surface", "Surface", "Cards"),
              ("text-secondary", "Text 2", "Supporting"), ("success", "Fresh", "Live · verified"), ("warning", "Changed", "Cached · moved"),
              ("error", "Error", "Failures + icon")]
    for i, (tkn, n, u) in enumerate(groups):
        x = M + (i % 5) * 340
        y = 560 + (i // 5) * 230
        val = tk.C_DARK_HEX[tkn]
        s.add(rect(x, y, 316, 130, val, 20, stroke=P["border"]))
        s.add(text(x, y + 166, n, "h3", P["text-primary"], size=22))
        s.add(text(x, y + 194, f"{val} · {u}", "metadata", P["text-tertiary"], size=16))
    slides["color-slide"] = s

    # 5 typography
    s = slide("Typography", "Two families", "Typography", "05")
    s.add(text(M, 380, "Aa", "display", P["text-primary"], size=260))
    s.add(text(M, 450, "Instrument Serif · the hook", "h3", P["text-primary"], size=24))
    s.add(text(M, 484, "Display 56 · 40. Once per screen. Editorial only.", "body", P["text-secondary"], size=18))
    s.add(text(M + 560, 380, "Aa", "h1", P["text-primary"], size=260, weight=700))
    s.add(text(M + 560, 450, "Inter · everything read fast", "h3", P["text-primary"], size=24))
    s.add(text(M + 560, 484, "700 headlines · 600 labels · 400 body · tabular prices", "body", P["text-secondary"], size=18))
    y = 580
    for n in ["display", "headline-media", "h2", "body", "metadata", "label"]:
        v = tk.T[n]
        sample = {"display": "Pick what wakes you up", "headline-media": "Monsoon's over. Six beaches worth the flight",
                  "h2": "Because you saved Goa", "body": "Fares are checked live before you see them.", "metadata": "Wake Travel · 4 min · ₹5,842 · 9:41",
                  "label": "Travel · For you"}[n]
        s.add(text(M, y + v["size"], sample, n, P["text-primary"], upper=(n == "label"), tnum=(n == "metadata")))
        s.add(text(1800, y + v["size"], f"{n} · {v['size']}/{v['lh']}", "metadata", P["text-tertiary"], anchor="end", size=16))
        y += v["size"] * 1.3 + 30
    s.add(text(1340, 300, "Pairing rules", "label", P["text-tertiary"], upper=True, size=14))
    for i, r_ in enumerate(["One serif moment per screen", "Numbers always Inter, tabular", "Caps only for labels, +8% tracking", "Two lines max on media"]):
        s.add(text(1340, 350 + i * 40, f"{i + 1}  {r_}", "body-l", P["text-secondary"], size=22))
    slides["typography-slide"] = s

    # 6 components
    s = slide("Component system", "Core components", "Component system", "06")
    title_block(s, "Few parts, used everywhere", "Buttons, chips, badges, search, tabs and navigation share one geometry: pill for anything you tap, 16 for cards, 24 for heroes.", width=1400)
    y = 520
    for i, v in enumerate(["primary", "secondary", "tertiary"]):
        s.add(c.button(M + i * 220, y, ["Plan a trip", "Save", "Share"][i], v, "L", icon_name=[None, "bookmark", "share"][i], trailing="arrow" if i == 0 else None))
    s.add(c.fab(M + 680, y - 2, label="Ask", svg=s))
    s.add(c.icon_button(M + 830, y + 4, "like"))
    s.add(c.chip_row(M, 620, ["For you", "Travel", ("Street style", "personalization"), "Cricket"], selected_index=0))
    s.add(c.search_field(M, 690, 620))
    s.add(c.category_tabs(M, 810, ["For you", "Travel", "Style", "News", "Cricket"], 0))
    s.add(c.segmented(M, 850, ["Flights", "Hotels", "Trips"], 0))
    s.add(c.bottom_nav(1060, 1000, 440))
    s.add(c.card_standard(s, 1060, 480, 300, "mountain")[0])
    g, _ = c.card_commerce(s, 1400, 480, 240, ratio=(1, 1))
    s.add(g)
    g, _ = c.toast(M, 930, "Saved to Goa trip", "Undo")
    s.add(g)
    slides["component-slide"] = s

    # 7 card anatomy
    s = slide("Card anatomy", "Hero card anatomy and the six card types", "Card anatomy", "07")
    title_block(s, "Six cards, one grammar", "Media on top or behind, text on the ground or on a scrim, metadata in one line, and only the hero carries a button.", width=760)
    s.add(c.card_hero(s, 1000, 150, 380, 475))
    parts = [("Badge · why", 1060, 180), ("Kicker", 1060, 440), ("Headline · 2 lines", 1200, 480), ("Metadata", 1080, 540), ("One action", 1100, 580)]
    for i, (lab, px, py) in enumerate(parts):
        ly = 190 + i * 90
        s.add(line(px, py, 1440, ly - 5, "#FF0049", 1.5, opacity=.8))
        s.add(circle(px, py, 6, "#FF0049"))
        s.add(circle(1460, ly - 5, 16, "#FF0049"))
        s.add(text(1460, ly + 1, str(i + 1), "label", "#FFFFFF", anchor="middle", size=14, ls=0))
        s.add(text(1490, ly + 3, lab, "h3", P["text-primary"], size=22))
    xs = M
    minis = [("A · Hero", "lagoon"), ("B · Standard", "mountain"), ("C · Compact", "news"), ("D · Commerce", "sneaker"), ("E · Recommendation", "desert"), ("F · Editorial", "temple")]
    for i, (lab, sc) in enumerate(minis):
        x = M + i * 140
        s.add(media(s, x, 700, 124, 150, sc, 12))
        s.add(text(x, 880, lab, "caption", P["text-secondary"], size=14))
    s.add(text(M, 940, "Hierarchy: A > F > E > B/D > C · one A and at most one F per screen", "body", P["text-tertiary"], size=18))
    slides["card-anatomy-slide"] = s

    # 8 content hierarchy
    s = slide("Content hierarchy", "Five levels", "Content hierarchy", "08")
    title_block(s, "What the eye reads, in order", None)
    s.add(c.card_hero(s, 1180, 150, 540, 680, "concert", "Music · Live", "Monsoon fest: the whole lineup, live tonight", ("Wake Live", "starts 8pm"), "Set reminder",
                      badge_kind="live", badge_label="Live"))
    for i, (lv, n, d) in enumerate(ct.HIERARCHY):
        y = 360 + i * 130
        wbar = 900 - i * 110
        s.add(rect(M, y, wbar, 100, P["surface"] if i else "#3A0716", 16))
        s.add(text(M + 28, y + 42, lv, "label", P["primary"] if i == 0 else P["text-tertiary"], upper=True, size=14))
        s.add(text(M + 28, y + 76, n, "h3", P["text-primary"], size=24))
        s.add(text(M + 330, y + 60, d, "body", P["text-secondary"], size=17)) if wbar > 600 else None
    slides["content-hierarchy-slide"] = s

    # 9 personalization
    s = slide("Personalization", "Signal to action", "Personalisation", "09")
    title_block(s, "Show the pick, name the reason, hand over the controls", None, width=1500, size=72)
    steps = [("Signal", "You saved two Goa stories this week", "bookmark"), ("Recommendation", "Palolem after the rains", "personalization"),
             ("Explanation", "Because you saved Goa · tap for why", "info"), ("Action", "More like this · Less · Turn off", "filter")]
    for i, (n, d, ic) in enumerate(steps):
        x = M + i * 430
        s.add(rect(x, 420, 390, 150, P["iris-subtle"] if i in (1, 2) else P["surface"], 20))
        s.add(icon(ic, x + 28, 448, 28, P["iris"] if i in (1, 2) else "#FFFFFF"))
        s.add(text(x + 72, 470, n, "h3", P["text-primary"], size=24))
        dd, dh = para(x + 28, 522, d, 340, "body", P["text-secondary"], size=17)
        s.add(dd)
        if i < 3:
            s.add(icon("forward", x + 396, 482, 28, P["text-tertiary"]))
    s.add(c.card_reco(s, M, 620, 300, 360, "lagoon", "Because you saved Goa", "Palolem after the rains", ("8 stays", "from ₹3,200")))
    g, th = c.tooltip(M + 330, 640, 420, "Why you're seeing this", "You saved two Goa stories this week and read about monsoon travel. Tap to tune or turn this off.")
    s.add(g)
    s.add(c.button(M + 330, 800, "More like this", "tertiary", "M", icon_name="plus"))
    s.add(c.button(M + 520, 800, "Less like this", "tertiary", "M", icon_name="close"))
    rules = ["Explicit when it uses the user's data or likeness", "Implicit (reason line only) for trend and context picks",
             "Confidence shown as wording, not percentages: 'Because you saved' > 'Similar to' > 'Popular near you'",
             "Every inferred interest is visible and removable in You"]
    for i, r_ in enumerate(rules):
        tt, th2 = para(1000, 660 + i * 76, "· " + r_, 780, "body-l", P["text-secondary"], size=21)
        s.add(tt)
    slides["personalization-slide"] = s

    # 10 interaction model
    s = slide("Interaction model", "Discovery flow and motion", "Interaction model", "10")
    title_block(s, "Glance, scan, commit", "Commitment rises one step at a time. Each step is reversible until money or data changes hands.", width=1400)
    flow = ct.PATTERNS["content-discovery"][1]
    desc = ["Wake the phone: one story", "Swipe the stream, tabs by topic", "A reason rail catches you", "Tap: media grows into detail", "Plan, save, share, book"]
    for i, (n, d) in enumerate(zip(flow, desc)):
        x = M + i * 344
        s.add(rect(x, 520, 316, 200, P["surface"] if i != 3 else "#3A0716", 20))
        s.add(text(x + 28, 572, f"0{i + 1}", "metadata", P["text-tertiary"], size=16))
        s.add(text(x + 28, 620, n, "display", P["text-primary"], size=40))
        dd, dh = para(x + 28, 666, d, 270, "body", P["text-secondary"], size=17)
        s.add(dd)
    rows = [("Tap / press", "100ms", "scale .97"), ("Card → detail", "360ms", "shared media, emphasized"), ("Sheet", "360 / 240ms", "slide + scrim .48"),
            ("Carousel", "360ms", "snap to margin"), ("Story", "5s", "auto-advance, hold to pause"), ("Like", "360ms", "the only spring")]
    for i, (a, b, d) in enumerate(rows):
        x = M + (i % 3) * 570
        y = 800 + (i // 3) * 70
        s.add(text(x, y, a, "h3", P["text-primary"], size=22))
        s.add(text(x + 190, y, b, "metadata", P["primary-light"], size=18))
        s.add(text(x + 330, y, d, "body", P["text-tertiary"], size=17))
    slides["interaction-model-slide"] = s

    # 11 principles
    s = slide("Design principles", "Ten principles", "Design principles", "11")
    s.add(text(M, 236, "Ten principles", "display", P["text-primary"], size=88))
    for i, pr in enumerate(ct.PRINCIPLES):
        x = M + (i % 2) * 850
        y = 330 + (i // 2) * 136
        s.add(text(x, y + 30, f"{i + 1:02d}", "display", P["primary"], size=40))
        s.add(text(x + 80, y + 26, pr[0], "h3", P["text-primary"], size=26))
        dd, dh = para(x + 80, y + 60, pr[1], 700, "body", P["text-secondary"], size=18, max_lines=2)
        s.add(dd)
        s.add(k.conf_mark(x + 80 + tw(pr[0], "h3", size=26) + 16, y + 24, pr[8], P["text-tertiary"], 14))
    slides["design-principles-slide"] = s

    # 12 example product
    s = slide("Example product experience", "Travel assistant, grounded", "Example product experience", "12")
    s.add(text(M, 236, "The system, applied: a travel assistant that can't make up a fare", "display", P["text-primary"], size=56))
    for i, (fn, cap) in enumerate([(bs.s_assistant_lock, "Live fare alert on the lock screen"), (bs.s_assistant_chat, "Fare card rendered from the API"),
                                   (bs.s_assistant_policy, "Rules cited, or deflected to a human")]):
        x = 260 + i * 500
        s.add(phone_at(s, x, 300, fn, .78))
        s.add(text(x + 152, 1000, cap, "body", P["text-secondary"], anchor="middle", size=18))
    slides["example-product-slide"] = s

    # 13 summary
    s = slide("Design system summary", "System at a glance", "Design system summary", "13")
    title_block(s, "The system on one page", None)
    stats = [("10", "principles"), ("24", "colour roles × 2 themes"), ("13", "type styles, 2 families"), ("13", "space steps, 4px base"),
             ("50", "icons on a 24 grid"), ("6", "card anatomies"), ("16", "screen templates"), ("15", "motion specs")]
    for i, (n, lab) in enumerate(stats):
        x = M + (i % 4) * 430
        y = 380 + (i // 4) * 210
        s.add(text(x, y + 80, n, "display", P["text-primary"], size=110))
        s.add(text(x, y + 124, lab, "body-l", P["text-secondary"], size=22))
    s.add(line(M, 830, SW - M, 830, P["divider"]))
    tt, th = para(M, 900, "Fetch what changes. Cite what rules. Show why. Let the image do the rest.", 1600, "display", P["text-primary"], size=48, italic=True)
    s.add(tt)
    slides["summary-slide"] = s

    # section divider
    s = slide("Section divider", "Section divider template")
    s.add(media(s, 960, 0, 960, SH, "iris"))
    s.add(text(M, 520, "02", "display", P["primary"], size=220))
    s.add(text(M, 660, "Components", "display", P["text-primary"], size=110))
    s.add(text(M, 730, "Cards, modules, navigation and overlays", "body-l", P["text-secondary"], size=26))
    slides["section-divider"] = s

    # architecture
    s = slide("Architecture", "How the system is layered", "System architecture", "—")
    title_block(s, "One logic, top to bottom", "Each layer only uses the layer above it. Change a token and every component, screen, slide and page follows.", width=900)
    layers = ["Principles", "Design tokens", "Typography + colour", "Grid + spacing", "Components", "Patterns", "Screens", "Implementation", "Deck + PDF"]
    for i, n in enumerate(layers):
        y = 150 + i * 96
        wbar = 560 + i * 26
        x = 1680 - wbar
        col = "#3A0716" if i == 0 else P["iris-subtle"] if i == 1 else P["surface"]
        s.add(rect(x, y, wbar, 80, col, 16))
        s.add(text(x + 28, y + 50, n, "h3", P["text-primary"], size=24))
        s.add(text(x + wbar - 28, y + 50, f"0{i}", "metadata", P["text-tertiary"], anchor="end", size=16))
        if i < len(layers) - 1:
            s.add(icon("chevron-down", 1680 - wbar / 2 - 12, y + 80, 24, P["text-tertiary"]))
    slides["architecture-slide"] = s

    # closing
    s = slide("Closing slide", "Closing")
    gid, g = k.rad_grad([(0, "#DDBEF0", .22), (1, "#DDBEF0", 0)], .15, .9, .6)
    s.define(g)
    s.add(rect(0, 0, SW, SH, f"url(#{gid})"))
    tt, th = para(M, 420, "Fetch what changes. Cite what rules. Show why.", 1400, "display", P["text-primary"], size=104, lh=1.0)
    s.add(tt)
    s.add(text(M, 420 + th + 40, "Thank you", "h2", P["text-secondary"], size=32))
    s.add(c.wordmark(SW - M - 260, SH - 140, "#FFFFFF", 72))
    slides["closing-slide"] = s

    order = ["title-slide", "design-dna-slide", "visual-language-slide", "color-slide", "typography-slide", "component-slide", "card-anatomy-slide",
             "content-hierarchy-slide", "personalization-slide", "interaction-model-slide", "design-principles-slide", "example-product-slide",
             "summary-slide", "section-divider", "architecture-slide", "closing-slide"]
    paths = []
    for n in order:
        p = f"{OUT}/{n}.svg"
        slides[n].save(p)
        paths.append(p)
    return paths


if __name__ == "__main__":
    ps = build()
    import render
    render.render_svgs(ps, f"{OUT}/png", 1.0)
    print("deck ok", len(ps))
