"""UI component renderers. Screens, component sheets, card specs and deck slides all call these,
so a component looks identical wherever it appears."""
import tokens as tk
import svgkit as k
from svgkit import rect, circle, line, path, text, para, icon, tw, group, fmt

DARK = dict(tk.C_DARK)
LIGHT = dict(tk.C_LIGHT)
for P in (DARK, LIGHT):
    P["glass"] = "rgba(22,22,27,.56)"
    P["glass-light"] = "rgba(255,255,255,.16)"
    P["primary-hover"] = "#D1003A"
PAL = {"dark": DARK, "light": LIGHT}
# inverse fills for the secondary button / selected chip
INV = {"dark": ("#FFFFFF", "#0C0C10"), "light": ("#0C0C10", "#FFFFFF")}

BTN = {"L": (52, 24, 15), "M": (44, 20, 15), "S": (32, 14, 13)}


# ---------------------------------------------------------------- buttons
def button(x, y, label, variant="primary", size="M", state="default", theme="dark", icon_name=None,
           trailing=None, width=None, on_media=False):
    P = PAL[theme]
    h, pad, fs = BTN[size]
    isz = 18 if size != "S" else 16
    lw = tw(label, "button", size=fs) if label else 0
    content_w = lw + (isz + 8 if icon_name else 0) + (isz + 6 if trailing else 0)
    w = width or content_w + pad * 2
    inv_bg, inv_fg = INV[theme]
    if variant == "primary":
        bg = {"default": P["primary-action"], "hover": P["primary-hover"], "pressed": P["primary-dark"],
              "disabled": P["surface-muted"], "loading": P["primary-action"]}[state]
        fg = P["text-tertiary"] if state == "disabled" else "#FFFFFF"
        stroke = None
    elif variant == "secondary":
        bg = inv_bg if state != "disabled" else P["surface-muted"]
        if state == "pressed":
            bg = "#D9D9DE" if theme == "dark" else "#2A2A33"
        if state == "hover":
            bg = "#EDEDF0" if theme == "dark" else "#1C1C22"
        fg = inv_fg if state != "disabled" else P["text-tertiary"]
        stroke = None
    elif variant == "tertiary":
        bg = {"default": "none", "hover": P["surface"], "pressed": P["surface-muted"], "disabled": "none", "loading": "none"}[state]
        fg = P["text-primary"] if state != "disabled" else P["text-tertiary"]
        stroke = P["border"] if state != "disabled" else P["divider"]
        if on_media:
            bg, stroke, fg = "rgba(255,255,255,.16)", None, "#FFFFFF"
    else:  # text action
        bg, stroke = "none", None
        fg = P["primary-light"] if theme == "dark" else P["primary-dark"]
        if state == "disabled":
            fg = P["text-tertiary"]
        pad = 0
        w = width or content_w
    out = []
    if bg != "none" or stroke:
        out.append(rect(x, y, w, h, bg, h / 2, stroke=stroke, sw=1 if stroke else 1))
    if variant == "text" and state in ("hover", "pressed"):
        out.append(line(x, y + h / 2 + fs * .75, x + lw, y + h / 2 + fs * .75, fg, 1.5))
    cx = x + (w - content_w) / 2
    if state == "loading":
        cx0 = x + w / 2
        out.append(circle(cx0, y + h / 2, 8, "none", stroke=fg, sw=2, opacity=.3))
        out.append(path(f"M{cx0} {y + h / 2 - 8} a8 8 0 0 1 8 8", stroke=fg, sw=2))
        return group(None, *out)
    if icon_name:
        out.append(icon(icon_name, cx, y + (h - isz) / 2, isz, fg))
        cx += isz + 8
    if label:
        out.append(text(cx, y + h / 2 + fs * .36, label, "button", fg, size=fs))
        cx += lw + 6
    if trailing:
        out.append(icon(trailing, cx, y + (h - isz) / 2, isz, fg))
    return group(None, *out)


def button_width(label, size="M", icon_name=None, trailing=None):
    h, pad, fs = BTN[size]
    isz = 18 if size != "S" else 16
    return tw(label, "button", size=fs) + (isz + 8 if icon_name else 0) + (isz + 6 if trailing else 0) + pad * 2


def icon_button(x, y, name, theme="dark", size=44, variant="muted", state="default", color=None, badge=None):
    P = PAL[theme]
    bg = {"muted": P["surface-muted"], "glass": "rgba(22,22,27,.56)", "glass-light": "rgba(255,255,255,.18)",
          "plain": "none", "primary": P["primary-action"], "inverse": INV[theme][0]}[variant]
    fg = color or ("#FFFFFF" if variant in ("glass", "glass-light", "primary") else
                   INV[theme][1] if variant == "inverse" else P["text-primary"])
    if state == "pressed" and variant != "plain":
        bg = P["surface-elevated"] if variant == "muted" else bg
    if state == "disabled":
        fg = P["text-tertiary"]
    out = []
    if bg != "none":
        out.append(circle(x + size / 2, y + size / 2, size / 2, bg))
    if state == "pressed":
        out.append(circle(x + size / 2, y + size / 2, size / 2, "#FFFFFF", opacity=.12))
    isz = 20 if size <= 44 else 24
    out.append(icon(name, x + (size - isz) / 2, y + (size - isz) / 2, isz, fg))
    if badge:
        out.append(circle(x + size - 8, y + 8, 8, P["primary"]))
        out.append(text(x + size - 8, y + 11.5, badge, "label", "#FFFFFF", anchor="middle", size=9, ls=0))
    return group(None, *out)


def fab(x, y, name="personalization", label=None, theme="dark", svg=None):
    P = PAL[theme]
    out = []
    fid = None
    if svg is not None:
        fid = k.Svg.uid("f")
        svg.define(f'<filter id="{fid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>')
    if label:
        w = tw(label, "button") + 24 + 20 + 8 + 4
        if fid:
            out.append(rect(x + 6, y + 10, w - 12, 50, "#FF0049", 25, opacity=.45, extra=f' filter="url(#{fid})"'))
        out.append(rect(x, y, w, 56, P["primary-action"], 28))
        out.append(icon(name, x + 20, y + 16, 24, "#FFFFFF"))
        out.append(text(x + 52, y + 33, label, "button", "#FFFFFF"))
    else:
        if fid:
            out.append(f'<circle cx="{x + 28}" cy="{y + 36}" r="22" fill="#FF0049" opacity=".45" filter="url(#{fid})"/>')
        out.append(circle(x + 28, y + 28, 28, P["primary-action"]))
        out.append(icon(name, x + 16, y + 16, 24, "#FFFFFF"))
    return group(None, *out)


# ---------------------------------------------------------------- chips, badges, tags
def chip(x, y, label, theme="dark", selected=False, icon_name=None, variant="default", h=34, trailing=None):
    P = PAL[theme]
    fs = 14
    lw = tw(label, "button", size=fs, weight=500)
    w = lw + 28 + (22 if icon_name else 0) + (20 if trailing else 0)
    if variant == "iris":
        bg, fg, stroke = P["iris-subtle"], P["iris"], None
    elif variant == "media":
        bg, fg, stroke = "rgba(255,255,255,.18)", "#FFFFFF", None
    elif variant == "glass":
        bg, fg, stroke = "rgba(22,22,27,.56)", "#FFFFFF", None
    elif selected:
        bg, fg, stroke = INV[theme][0], INV[theme][1], None
    else:
        bg, fg, stroke = P["surface-muted"], P["text-primary"], None
    out = [rect(x, y, w, h, bg, h / 2, stroke=stroke)]
    cx = x + 14
    if icon_name:
        out.append(icon(icon_name, cx, y + (h - 16) / 2, 16, fg))
        cx += 22
    out.append(text(cx, y + h / 2 + 5, label, "button", fg, size=fs, weight=500))
    if trailing:
        out.append(icon(trailing, cx + lw + 4, y + (h - 14) / 2, 14, fg))
    return group(None, *out), w


def chip_row(x, y, labels, theme="dark", selected_index=0, gap=8, max_x=None, **kw):
    out = []
    cx = x
    for i, lab in enumerate(labels):
        icon_name = None
        if isinstance(lab, tuple):
            lab, icon_name = lab
        g, w = chip(cx, y, lab, theme, selected=(i == selected_index), icon_name=icon_name, **kw)
        out.append(g)
        cx += w + gap
        if max_x and cx > max_x:
            break
    return "".join(out)


BADGE_KINDS = {
    # kind: (bg, fg, icon, dot)
    "live": ("primary", "#FFFFFF", None, True),
    "new": ("#FFFFFF", "#0C0C10", None, False),
    "trending": ("glass", "#FFFFFF", "trending", False),
    "for-you": ("iris-subtle", "iris", "personalization", False),
    "price-drop": ("success-subtle", "success", "tag", False),
    "verified": ("success-subtle", "success", "shield-check", False),
    "sponsored": ("outline", "text-secondary", None, False),
    "warning": ("warning-subtle", "warning", "alert", False),
    "live-fare": ("success-subtle", "success", None, True),
}


def badge(x, y, label, kind="live", theme="dark", on_media=False, h=22):
    P = PAL[theme]
    bgk, fgk, ic, dot = BADGE_KINDS[kind]
    subtle = {"success-subtle": ("#0F2E22" if theme == "dark" else "#E3F5EC"),
              "warning-subtle": ("#33260A" if theme == "dark" else "#FFF3DC")}
    bg = P.get(bgk, subtle.get(bgk, bgk))
    if bgk == "glass":
        bg = "rgba(22,22,27,.56)"
    fg = P.get(fgk, fgk)
    if on_media and kind in ("for-you",):
        bg, fg = "rgba(37,26,46,.82)", "#DDBEF0"
    if on_media and kind in ("verified", "live-fare", "price-drop"):
        bg = "rgba(10,20,15,.72)"
        fg = "#2FD08A"
    fs = 10.5
    lw = tw(label, "label", size=fs, upper=True)
    w = lw + 16 + (15 if ic else 0) + (11 if dot else 0)
    out = []
    if bgk == "outline":
        out.append(rect(x, y, w, h, "none", h / 2, stroke=P["border"]))
    else:
        out.append(rect(x, y, w, h, bg, h / 2))
    cx = x + 8
    if dot:
        dc = "#FFFFFF" if kind == "live" else fg
        out.append(circle(cx + 3, y + h / 2, 3, dc))
        cx += 11
    if ic:
        out.append(icon(ic, cx - 1, y + (h - 13) / 2, 13, fg))
        cx += 15
    out.append(text(cx, y + h / 2 + 3.8, label, "label", fg, size=fs, upper=True))
    return group(None, *out), w


def kicker(x, y, label, color, size=11):
    return text(x, y, label, "label", color, upper=True, size=size)


def count_dot(x, y, n, theme="dark"):
    P = PAL[theme]
    return group(None, circle(x, y, 9, P["primary"]), text(x, y + 3.5, str(n), "label", "#FFFFFF", anchor="middle", size=10, ls=0))


# ---------------------------------------------------------------- inputs
def search_field(x, y, w, placeholder="Search stories, looks, trips", theme="dark", value=None, focused=False, h=48,
                 mic=True):
    P = PAL[theme]
    out = [rect(x, y, w, h, P["surface-muted"], h / 2,
                stroke=P["primary"] if focused else None, sw=2 if focused else 1)]
    out.append(icon("search", x + 16, y + (h - 20) / 2, 20, P["text-secondary"]))
    if value:
        out.append(text(x + 46, y + h / 2 + 5, value, "body", P["text-primary"]))
        if focused:
            cw = tw(value, "body")
            out.append(rect(x + 47 + cw, y + h / 2 - 10, 1.5, 20, P["primary"]))
        out.append(icon("close", x + w - 36, y + (h - 18) / 2, 18, P["text-secondary"]))
    else:
        out.append(text(x + 46, y + h / 2 + 5, placeholder, "body", P["text-tertiary"]))
        if mic:
            out.append(icon("mic", x + w - 38, y + (h - 20) / 2, 20, P["text-secondary"]))
    return group(None, *out)


def text_field(x, y, w, label, value=None, placeholder="", theme="dark", state="default", helper=None):
    P = PAL[theme]
    out = [text(x, y, label, "caption", P["text-secondary"])]
    stroke = {"default": P["border"], "focus": P["primary"], "error": P["error"], "disabled": P["divider"]}[state]
    out.append(rect(x, y + 10, w, 52, P["surface-muted"] if state != "disabled" else P["surface"], 12,
                    stroke=stroke, sw=2 if state in ("focus", "error") else 1))
    if value:
        out.append(text(x + 16, y + 42, value, "body", P["text-primary"] if state != "disabled" else P["text-tertiary"]))
    else:
        out.append(text(x + 16, y + 42, placeholder, "body", P["text-tertiary"]))
    if helper:
        col = P["error"] if state == "error" else P["text-tertiary"]
        if state == "error":
            out.append(icon("alert", x, y + 72, 14, col))
            out.append(text(x + 20, y + 83, helper, "caption", col))
        else:
            out.append(text(x, y + 83, helper, "caption", col))
    return group(None, *out)


def toggle(x, y, on=True, theme="dark"):
    P = PAL[theme]
    bg = P["primary-action"] if on else P["surface-muted"]
    return group(None, rect(x, y, 44, 26, bg, 13), circle(x + (31 if on else 13), y + 13, 10, "#FFFFFF"))


# ---------------------------------------------------------------- tabs & nav
def category_tabs(x, y, labels, active=0, theme="dark", on_media=False, gap=22):
    P = PAL[theme]
    out = []
    cx = x
    for i, lab in enumerate(labels):
        is_a = i == active
        col = ("#FFFFFF" if on_media else P["text-primary"]) if is_a else (
            "rgba(255,255,255,.64)" if on_media else P["text-tertiary"])
        out.append(text(cx, y, lab, "button", col, weight=700 if is_a else 500, size=15))
        lw = tw(lab, "button", size=15, weight=700 if is_a else 500)
        if is_a:
            out.append(rect(cx + lw / 2 - 8, y + 9, 16, 3, P["primary"], 1.5))
        cx += lw + gap
    return group("category-tabs", *out)


def segmented(x, y, labels, active=0, theme="dark", w=None):
    P = PAL[theme]
    seg_w = [tw(l, "button", size=14) + 32 for l in labels]
    total = w or sum(seg_w) + 8
    if w:
        seg_w = [(w - 8) / len(labels)] * len(labels)
    out = [rect(x, y, total, 40, P["surface-muted"], 20)]
    cx = x + 4
    for i, (lab, sw_) in enumerate(zip(labels, seg_w)):
        if i == active:
            out.append(rect(cx, y + 4, sw_, 32, INV[theme][0], 16))
        out.append(text(cx + sw_ / 2, y + 25, lab, "button", INV[theme][1] if i == active else P["text-secondary"],
                        anchor="middle", size=14))
        cx += sw_
    return group("segmented", *out)


def top_bar(x, y, w, theme="dark", title=None, on_media=False, left="logo", right=("notification", "avatar"),
            bell_badge=None):
    P = PAL[theme]
    fg = "#FFFFFF" if on_media else P["text-primary"]
    out = []
    if left == "logo":
        out.append(wordmark(x + 16, y + 30, fg))
    elif left == "back":
        out.append(icon_button(x + 12, y + 6, "back", theme, 40, "glass" if on_media else "plain", color=fg))
    if title:
        out.append(text(x + w / 2, y + 32, title, "h3", fg, anchor="middle"))
    rx = x + w - 16
    for r in reversed(right):
        if r == "avatar":
            rx -= 32
            out.append(avatar(rx, y + 10, 32, "A", ring=False))
        else:
            rx -= 40
            out.append(icon_button(rx, y + 6, r, theme, 40, "glass" if on_media else "plain", color=fg,
                                   badge=bell_badge if r == "notification" else None))
        rx -= 6
    return group("top-bar", *out)


def wordmark(x, y, color="#FFFFFF", size=24):
    """Original placeholder wordmark 'wake' (not a Glance mark)."""
    return group("wordmark", text(x, y, "wake", "display", color, size=size, italic=True, ls=-.01),
                 circle(x + tw("wake", "display", size=size, italic=True) + 5, y - size * .22, size * .12, "#FF0049"))


def avatar(x, y, s, initial="A", ring=False, seen=False, scene=None, svg=None):
    out = []
    if ring:
        gid, g = k.lin_grad([(0, "#FF0049"), (1, "#DDBEF0")], 0, 0, 1, 1)
        if svg:
            svg.define(g)
        out.append(circle(x + s / 2, y + s / 2, s / 2, "none" if not svg else f"url(#{gid})") if not seen else
                   circle(x + s / 2, y + s / 2, s / 2, "none", stroke="#3A3A44", sw=2))
        if not seen and not svg:
            out.append(circle(x + s / 2, y + s / 2, s / 2 - 1, "none", stroke="#FF0049", sw=2.5))
        inner = s - 8
        ox, oy = x + 4, y + 4
    else:
        inner, ox, oy = s, x, y
    if scene and svg:
        out.append(k.media(svg, ox, oy, inner, inner, scene, inner / 2))
    else:
        gid2, g2 = k.lin_grad([(0, "#DDBEF0"), (1, "#B98BDB")], 0, 0, 1, 1)
        if svg:
            svg.define(g2)
            out.append(circle(ox + inner / 2, oy + inner / 2, inner / 2, f"url(#{gid2})"))
        else:
            out.append(circle(ox + inner / 2, oy + inner / 2, inner / 2, "#B98BDB"))
        out.append(text(ox + inner / 2, oy + inner / 2 + inner * .17, initial, "h3", "#251A2E", anchor="middle",
                        size=inner * .45, weight=700))
    return group(None, *out)


NAV_ITEMS = [("home", "For you"), ("grid", "Discover"), ("personalization", "Ask"), ("bookmark", "Saved"), ("profile", "You")]


def bottom_nav(x, y_bottom, w, active=0, theme="dark", items=NAV_ITEMS, glass=True):
    P = PAL[theme]
    h = 84
    y = y_bottom - h
    out = [rect(x, y, w, h, "rgba(12,12,16,.92)" if theme == "dark" else "rgba(255,255,255,.94)"),
           line(x, y, x + w, y, P["divider"], 1)]
    n = len(items)
    cw = w / n
    for i, (ic, lab) in enumerate(items):
        cx = x + cw * i + cw / 2
        is_a = i == active
        col = P["text-primary"] if is_a else P["text-tertiary"]
        if ic == "personalization":
            out.append(circle(cx, y + 22, 18, P["iris-subtle"]))
            out.append(icon(ic, cx - 11, y + 11, 22, P["iris"]))
            out.append(text(cx, y + 54, lab, "caption", P["iris"] if not is_a else P["text-primary"], anchor="middle", size=11, weight=600))
            continue
        out.append(icon(ic, cx - 12, y + 10, 24, col))
        out.append(text(cx, y + 50, lab, "caption", col, anchor="middle", size=11, weight=600 if is_a else 500))
        if is_a:
            out.append(circle(cx, y + 4, 2, P["primary"]))
    out.append(k.home_indicator(x, y_bottom, w, P["text-primary"]))
    return group("bottom-nav", *out)


def section_header(x, y, w, title, theme="dark", action="See all", sub=None, iris=False):
    P = PAL[theme]
    out = []
    tx = x
    if iris:
        out.append(icon("personalization", x, y - 17, 18, P["iris"]))
        tx += 24
    out.append(text(tx, y, title, "h2", P["text-primary"], size=20))
    if action:
        out.append(text(x + w, y, action, "button", P["text-secondary"], anchor="end", size=14, weight=500))
    if sub:
        out.append(text(x, y + 20, sub, "body-s", P["iris"] if iris else P["text-tertiary"]))
    return group(None, *out)


def page_dots(cx, y, n, active=0, theme="dark", on_media=False):
    P = PAL[theme]
    out = []
    widths = [18 if i == active else 6 for i in range(n)]
    total = sum(widths) + 6 * (n - 1)
    x = cx - total / 2
    for i, wd in enumerate(widths):
        col = ("#FFFFFF" if on_media else P["text-primary"]) if i == active else (
            "rgba(255,255,255,.4)" if on_media else P["surface-muted"])
        out.append(rect(x, y, wd, 6, col, 3))
        x += wd + 6
    return group(None, *out)


def story_bars(x, y, w, n, active=0, progress=.45):
    gap = 4
    bw = (w - gap * (n - 1)) / n
    out = []
    for i in range(n):
        bx = x + i * (bw + gap)
        out.append(rect(bx, y, bw, 3, "rgba(255,255,255,.32)", 1.5))
        f = 1 if i < active else progress if i == active else 0
        if f:
            out.append(rect(bx, y, bw * f, 3, "rgba(255,255,255,.92)", 1.5))
    return group(None, *out)


# ---------------------------------------------------------------- cards
def card_hero(svg, x, y, w=358, h=448, scene="lagoon", kick="Travel · For you", title="Monsoon's over. Six beaches worth the flight",
              meta_parts=("Wake Travel", "4 min"), cta="Plan a trip", theme="dark", reason=None, badge_kind="for-you",
              badge_label="For you", r=24):
    P = PAL[theme]
    out = [k.media(svg, x, y, w, h, scene, r)]
    out.append(k.scrim_bottom(svg, x, y, w, h, start=.35, r=r))
    out.append(rect(x, y, w, h, "none", r, stroke="rgba(255,255,255,.08)"))
    if badge_kind:
        b, bw = badge(x + 16, y + 16, badge_label, badge_kind, theme, on_media=True, h=24)
        out.append(b)
    out.append(icon_button(x + w - 56, y + 12, "bookmark", theme, 40, "glass"))
    # text block from bottom
    by = y + h - 20 - 44
    out.append(button(x + 20, by, cta, "primary", "M", theme=theme, trailing="arrow"))
    out.append(icon_button(x + w - 20 - 44, by, "share", theme, 44, "glass"))
    meta_y = by - 18
    out.append(k.meta(x + 20, meta_y, meta_parts, "rgba(255,255,255,.72)"))
    lines = k.wrap(title, w - 40, "headline-media")[:3]
    lh = tk.T["headline-media"]["size"] * tk.T["headline-media"]["lh"]
    first = meta_y - 26 - lh * (len(lines) - 1)
    for i, ln in enumerate(lines):
        out.append(text(x + 20, first + i * lh, ln, "headline-media", "#FFFFFF"))
    out.append(kicker(x + 20, first - 30, kick, "rgba(255,255,255,.8)"))
    if reason:
        pass
    return group("card-hero", *out)


def card_standard(svg, x, y, w=240, scene="mountain", kick="Travel", title="The quiet hill towns nobody has told you about",
                  meta_parts=("Wake Travel", "6 min"), theme="dark", ratio=(3, 2), media_badge=None, r=16, lines=2):
    P = PAL[theme]
    mh = w * ratio[1] / ratio[0]
    out = [k.media(svg, x, y, w, mh, scene, r), rect(x, y, w, mh, "none", r, stroke="rgba(255,255,255,.08)")]
    if media_badge:
        b, bw = badge(x + 10, y + 10, media_badge[0], media_badge[1], theme, on_media=True)
        out.append(b)
    ty = y + mh + 22
    out.append(kicker(x, ty, kick, P["text-tertiary"]))
    t, th = para(x, ty + 22, title, w, "h3", P["text-primary"], max_lines=lines)
    out.append(t)
    out.append(k.meta(x, ty + 22 + th + 4, meta_parts, P["text-tertiary"]))
    return group("card-standard", *out), mh + 22 + 22 + th + 8


def card_compact(svg, x, y, w=358, scene="news", title="Metro line 3 opens early for festival week",
                 meta_parts=("City Desk", "12 min ago"), theme="dark", trailing="bookmark", kick=None, rank=None, thumb=72):
    P = PAL[theme]
    out = []
    tx = x
    if rank is not None:
        out.append(text(x, y + thumb / 2 + 10, str(rank), "display", P["text-tertiary"], size=32))
        tx += 30
    out.append(k.media(svg, tx, y, thumb, thumb, scene, 12))
    txt_x = tx + thumb + 14
    tw_ = x + w - txt_x - (36 if trailing else 0)
    ty = y + 18
    if kick:
        out.append(kicker(txt_x, ty - 2, kick, P["text-tertiary"], size=10))
        ty += 16
    t, th = para(txt_x, ty, title, tw_, "body", P["text-primary"], weight=600, max_lines=2, lh=1.35)
    out.append(t)
    out.append(k.meta(txt_x, ty + th + 2, meta_parts, P["text-tertiary"]))
    if trailing:
        out.append(icon(trailing, x + w - 22, y + thumb / 2 - 11, 22, P["text-secondary"]))
    return group("card-compact", *out)


def card_commerce(svg, x, y, w=171, scene="sneaker", brand="Northline", name="Court low sneaker in signal red",
                  price="₹4,299", was="₹5,999", off="28% off", theme="dark", badge_=("Price drop", "price-drop"),
                  fresh="Price checked 9:41", liked=False, r=16, ratio=(4, 5), store="Sold by Northline"):
    P = PAL[theme]
    mh = w * ratio[1] / ratio[0]
    out = [k.media(svg, x, y, w, mh, scene, r)]
    if badge_:
        b, bw = badge(x + 10, y + 10, badge_[0], badge_[1], "light")
        out.append(b)
    out.append(circle(x + w - 26, y + 26, 16, "rgba(255,255,255,.92)"))
    out.append(icon("like", x + w - 36, y + 16, 20, "#FF0049" if liked else "#0C0C10", fill_color="#FF0049" if liked else None))
    ty = y + mh + 20
    out.append(text(x, ty, brand, "caption", P["text-tertiary"], weight=600))
    t, th = para(x, ty + 19, name, w, "body-s", P["text-primary"], max_lines=2, weight=500, lh=1.35)
    out.append(t)
    py = ty + 19 + th + 8
    out.append(text(x, py, price, "h3", P["text-primary"], weight=700, tnum=True))
    pw = tw(price, "h3", weight=700)
    if was:
        out.append(text(x + pw + 8, py, was, "metadata", P["text-tertiary"], tnum=True))
        ww = tw(was, "metadata")
        out.append(line(x + pw + 8, py - 4, x + pw + 8 + ww, py - 4, P["text-tertiary"], 1))
        out.append(text(x + pw + 8 + ww + 6, py, off, "metadata", P["success"], weight=600))
    if fresh:
        out.append(circle(x + 3, py + 15, 3, P["success"]))
        out.append(text(x + 11, py + 19, fresh, "caption", P["text-tertiary"], size=11))
    return group("card-commerce", *out), mh + 20 + 19 + th + 8 + (22 if fresh else 0)


def card_reco(svg, x, y, w=240, h=320, scene="desert", reason="Because you saved Jaisalmer", title="Desert camps that open after the rains",
              meta_parts=("12 stays", "from ₹3,800"), theme="dark", r=16, feedback=True):
    P = PAL[theme]
    out = [k.media(svg, x, y, w, h, scene, r), k.scrim_bottom(svg, x, y, w, h, start=.3, r=r),
           rect(x, y, w, h, "none", r, stroke="rgba(255,255,255,.08)")]
    # reason chip
    fs = 12
    rw = tw(reason, "caption", size=fs, weight=600) + 38
    rw = min(rw, w - 24)
    out.append(rect(x + 12, y + 12, rw, 28, "rgba(37,26,46,.86)", 14))
    out.append(icon("personalization", x + 20, y + 18, 16, "#DDBEF0"))
    out.append(text(x + 42, y + 30.5, reason, "caption", "#DDBEF0", size=fs, weight=600))
    lines = k.wrap(title, w - 32, "h3", size=19, weight=700)[:3]
    ly = y + h - 44 - (len(lines) - 1) * 23
    for i, ln in enumerate(lines):
        out.append(text(x + 16, ly + i * 23, ln, "h3", "#FFFFFF", size=19, weight=700))
    out.append(k.meta(x + 16, y + h - 18, meta_parts, "rgba(255,255,255,.72)"))
    if feedback:
        out.append(icon("more", x + w - 34, y + h - 32, 20, "rgba(255,255,255,.8)"))
    return group("card-recommendation", *out)


def card_editorial(svg, x, y, w=358, scene="temple", kick="The long read", title="Forty-eight hours in a city that wakes before you do",
                   dek="A slow itinerary for Varanasi: dawn on the ghats, lunch in the lanes, and the ceremony worth staying up for.",
                   meta_parts=("Words by Meera Rao", "9 min read"), theme="dark", r=16, ratio=(3, 2)):
    P = PAL[theme]
    mh = w * ratio[1] / ratio[0]
    out = [k.media(svg, x, y, w, mh, scene, r), rect(x, y, w, mh, "none", r, stroke="rgba(255,255,255,.08)")]
    ty = y + mh + 26
    out.append(kicker(x, ty, kick, P["primary-light"] if theme == "dark" else P["primary-dark"]))
    t, th = para(x, ty + 34, title, w, "display", P["text-primary"], size=30, lh=1.08)
    out.append(t)
    d, dh = para(x, ty + 34 + th + 4, dek, w, "body-s", P["text-secondary"], max_lines=3)
    out.append(d)
    out.append(k.meta(x, ty + 34 + th + dh + 14, meta_parts, P["text-tertiary"]))
    return group("card-editorial", *out), mh + 26 + 34 + th + dh + 16


def card_news(svg, x, y, w=358, scene="news", source="The Daily Ledger", title="Rail budget adds 40 new routes for the festive season",
              time="18 min ago", theme="dark", r=16, kick="National"):
    P = PAL[theme]
    mh = w * 9 / 16
    out = [k.media(svg, x, y, w, mh, scene, r)]
    ty = y + mh + 16
    out.append(circle(x + 10, ty + 8, 10, P["surface-muted"]))
    out.append(text(x + 10, ty + 12, source[4] if source.startswith("The ") else source[0], "label", P["text-primary"], anchor="middle", size=10))
    out.append(k.meta(x + 28, ty + 12, (source, kick, time), P["text-tertiary"]))
    t, th = para(x, ty + 42, title, w, "h3", P["text-primary"], size=18, weight=700, max_lines=3)
    out.append(t)
    out.append(icon("share", x + w - 24, ty + 42 + th - 4, 20, P["text-tertiary"]))
    out.append(icon("bookmark", x + w - 56, ty + 42 + th - 4, 20, P["text-tertiary"]))
    return group("card-news", *out), mh + 16 + 42 + th + 8


def card_video(svg, x, y, w=358, scene="concert", title="Front row at the monsoon music fest", meta_parts=("Live now", "12.4k watching"),
               theme="dark", r=16, progress=.35, duration="LIVE"):
    P = PAL[theme]
    mh = w * 9 / 16
    out = [k.media(svg, x, y, w, mh, scene, r), k.scrim_bottom(svg, x, y, w, mh, .45, .7, r)]
    out.append(circle(x + w / 2, y + mh / 2, 28, "rgba(22,22,27,.56)"))
    out.append(icon("play", x + w / 2 - 11, y + mh / 2 - 12, 24, "#FFFFFF", fill_color="#FFFFFF"))
    if duration == "LIVE":
        b, bw = badge(x + 12, y + 12, "Live", "live")
    else:
        b, bw = badge(x + w - 60, y + mh - 34, duration, "trending")
    out.append(b)
    out.append(rect(x + 12, y + mh - 12, w - 24, 3, "rgba(255,255,255,.32)", 1.5))
    out.append(rect(x + 12, y + mh - 12, (w - 24) * progress, 3, "#FF0049", 1.5))
    t, th = para(x, y + mh + 24, title, w, "h3", P["text-primary"], max_lines=2)
    out.append(t)
    out.append(k.meta(x, y + mh + 24 + th + 2, meta_parts, P["text-tertiary"]))
    return group("card-video", *out), mh + 24 + th + 10


# ---------------------------------------------------------------- overlays
def bottom_sheet(svg, x, y, w, h, title, rows, theme="dark"):
    P = PAL[theme]
    out = [path(k.rounded_top(x, y, w, h, 24), P["surface-elevated"])]
    out.append(rect(x + w / 2 - 18, y + 8, 36, 5, P["border"] if theme == "dark" else "#D0CED8", 2.5))
    out.append(text(x + 20, y + 48, title, "h3", P["text-primary"], size=18))
    ry = y + 72
    for ic, lab, sub in rows:
        out.append(icon(ic, x + 20, ry + 10, 22, P["text-primary"] if ic != "personalization" else P["iris"]))
        out.append(text(x + 58, ry + 20, lab, "body", P["text-primary"], weight=500))
        if sub:
            out.append(text(x + 58, ry + 38, sub, "caption", P["text-tertiary"]))
        ry += 56 if sub else 48
        out.append(line(x + 58, ry - 6, x + w - 20, ry - 6, P["divider"]))
    return group("bottom-sheet", *out)


def toast(x, y, msg, action=None, theme="dark", ic="check", ic_color=None, w=None):
    P = PAL[theme]
    mw = tw(msg, "body-s", weight=500)
    aw = tw(action, "button", size=14) if action else 0
    w = w or mw + aw + 20 + 28 + (24 if action else 0) + 16
    bg = "#2A2A33" if theme == "dark" else "#0C0C10"
    out = [rect(x, y, w, 48, bg, 24)]
    out.append(icon(ic, x + 16, y + 14, 20, ic_color or P["success"]))
    out.append(text(x + 46, y + 29, msg, "body-s", "#FFFFFF", weight=500))
    if action:
        out.append(text(x + w - 18, y + 29, action, "button", "#FF4D7D", anchor="end", size=14))
    return group("toast", *out), w


def dialog(x, y, w, title, body, primary, secondary, theme="dark", ic="alert", ic_color=None):
    P = PAL[theme]
    bl = k.wrap(body, w - 48, "body")
    h = 24 + 40 + 16 + 28 + 10 + len(bl) * 22.5 + 24 + 52 + 12 + 44 + 16
    out = [rect(x, y, w, h, P["surface-elevated"], 24)]
    out.append(circle(x + 44, y + 44, 20, "#33260A" if theme == "dark" else "#FFF3DC"))
    out.append(icon(ic, x + 32, y + 32, 24, ic_color or P["warning"]))
    out.append(text(x + 24, y + 104, title, "h3", P["text-primary"], size=19, weight=700))
    for i, ln in enumerate(bl):
        out.append(text(x + 24, y + 132 + i * 22.5, ln, "body", P["text-secondary"]))
    by = y + 132 + len(bl) * 22.5 + 14
    out.append(button(x + 24, by, primary, "primary", "L", theme=theme, width=w - 48))
    out.append(button(x + 24, by + 60, secondary, "tertiary", "M", theme=theme, width=w - 48))
    return group("dialog", *out), h


def tooltip(x, y, w, title, body, theme="dark", arrow_x=None):
    P = PAL[theme]
    bl = k.wrap(body, w - 32, "body-s")
    h = 44 + len(bl) * 19 + 14
    out = [rect(x, y, w, h, P["iris-subtle"] if theme == "dark" else "#251A2E", 12,
                stroke="rgba(221,190,240,.3)" if theme == "dark" else None)]
    ax = arrow_x or x + 28
    out.append(path(f"M{ax - 8} {y} L{ax} {y - 8} L{ax + 8} {y}Z", P["iris-subtle"] if theme == "dark" else "#251A2E"))
    out.append(icon("personalization", x + 14, y + 14, 16, "#DDBEF0"))
    out.append(text(x + 38, y + 27, title, "caption", "#DDBEF0", weight=700, size=13))
    for i, ln in enumerate(bl):
        out.append(text(x + 16, y + 50 + i * 19, ln, "body-s", "#EDE3F5" if theme == "dark" else "#EDE3F5"))
    return group("tooltip", *out), h


# ---------------------------------------------------------------- travel-assistant (case) components
def chat_bubble_user(x_right, y, msg, theme="dark", max_w=260):
    P = PAL[theme]
    lines = k.wrap(msg, max_w - 32, "body")
    w = max(tw(l, "body") for l in lines) + 32
    h = 20 + len(lines) * 22.5
    x = x_right - w
    out = [rect(x, y, w, h, INV[theme][0], 20)]
    for i, ln in enumerate(lines):
        out.append(text(x + 16, y + 27 + i * 22.5, ln, "body", INV[theme][1]))
    return group("bubble-user", *out), h


def assistant_line(x, y, w, msg, theme="dark"):
    P = PAL[theme]
    out = [circle(x + 12, y + 12, 12, P["iris-subtle"]), icon("personalization", x + 4, y + 4, 16, P["iris"])]
    t, th = para(x + 34, y + 17, msg, w - 34, "body", P["text-primary"])
    out.append(t)
    return group("assistant-line", *out), max(th, 24)


def price_card(x, y, w, theme="dark", route=("DEL", "GOI"), airline="Skyline Air · SK 2134", times=("06:10", "08:45"),
               dur="2h 35m · Non-stop", price="₹5,842", fresh="Live fare · checked 9:41", note="Incl. taxes and fees · Economy saver",
               state="live", cta="Book at ₹5,842"):
    """Structured fare card. The number is rendered from the fare API response, never typed by the model."""
    P = PAL[theme]
    h = 270
    out = [rect(x, y, w, h, P["surface"], 16, stroke=P["border"])]
    out.append(text(x + 16, y + 30, airline, "caption", P["text-tertiary"], weight=600))
    lab, kind = {"live": ("Live", "live-fare"), "stale": ("Cached", "warning"), "changed": ("Price changed", "warning")}[state]
    b, bw = badge(0, 0, lab, kind, theme)
    b, bw = badge(x + w - 16 - bw, y + 14, lab, kind, theme)
    out.append(b)
    out.append(text(x + 16, y + 74, times[0], "h1", P["text-primary"], size=26, tnum=True))
    out.append(text(x + 16, y + 94, route[0], "caption", P["text-secondary"], weight=600))
    out.append(text(x + w - 16, y + 74, times[1], "h1", P["text-primary"], size=26, tnum=True, anchor="end"))
    out.append(text(x + w - 16, y + 94, route[1], "caption", P["text-secondary"], weight=600, anchor="end"))
    mx1, mx2 = x + 104, x + w - 104
    out.append(line(mx1, y + 66, mx2, y + 66, P["border"], 1.5, dash="3 4"))
    out.append(rect((mx1 + mx2) / 2 - 14, y + 54, 28, 24, P["surface"]))
    out.append(icon("plane", (mx1 + mx2) / 2 - 10, y + 56, 20, P["text-secondary"]))
    out.append(text((mx1 + mx2) / 2, y + 94, dur, "caption", P["text-tertiary"], anchor="middle", size=11))
    out.append(line(x + 16, y + 112, x + w - 16, y + 112, P["divider"]))
    out.append(text(x + 16, y + 148, price, "h1", P["text-primary"], size=30, tnum=True))
    if state == "changed":
        pw = tw(price, "h1", size=30)
        out.append(text(x + 26 + pw, y + 148, "was ₹5,210", "metadata", P["warning"], tnum=True))
    out.append(text(x + 16, y + 170, note, "caption", P["text-tertiary"], size=11))
    dotc = P["success"] if state == "live" else P["warning"]
    out.append(circle(x + w - 16 - tw(fresh, "caption", size=11, weight=600) - 10, y + 144, 3, dotc))
    out.append(text(x + w - 16, y + 148, fresh, "caption", dotc, size=11, weight=600, tnum=True, anchor="end"))
    out.append(button(x + 16, y + 198, cta, "primary", "L", theme=theme, width=w - 32))
    return group("fare-card", *out), h


def policy_card(x, y, w, theme="dark", q="Do I need a visa for Thailand on an Indian passport?",
                answer="Indian passport holders can enter Thailand visa-free for tourism for a limited stay. Check the stay length and entry conditions on the official page before you fly.",
                source="Royal Thai Embassy, New Delhi · Visa page", verified="Last verified 29 Sep 2026"):
    P = PAL[theme]
    al = k.wrap(answer, w - 32, "body")
    h = 56 + len(al) * 22.5 + 104
    out = [rect(x, y, w, h, P["surface"], 16, stroke=P["border"])]
    b, bw = badge(x + 16, y + 16, "Cited answer", "verified", theme)
    out.append(b)
    for i, ln in enumerate(al):
        out.append(text(x + 16, y + 66 + i * 22.5, ln, "body", P["text-primary"]))
    sy = y + 56 + len(al) * 22.5 + 16
    out.append(rect(x + 12, sy, w - 24, 60, P["surface-muted"], 12))
    out.append(rect(x + 12, sy, 3, 60, P["success"], 1.5))
    out.append(icon("passport", x + 26, sy + 18, 22, P["text-secondary"]))
    src_lines = k.wrap(source, w - 58 - 52, "caption", weight=600)
    src = src_lines[0] + ("…" if len(src_lines) > 1 else "")
    out.append(text(x + 58, sy + 26, src, "caption", P["text-primary"], weight=600))
    out.append(text(x + 58, sy + 44, verified, "caption", P["text-tertiary"], tnum=True))
    out.append(icon("external", x + w - 42, sy + 19, 20, P["text-secondary"]))
    return group("policy-card", *out), h


def deflect_card(x, y, w, theme="dark", title="I can't confirm this one from an official source",
                 body="Transit rules for this route changed recently. Rather than guess, here's the official page, or talk to a travel expert.",
                 primary="Open official page", secondary="Talk to an expert"):
    P = PAL[theme]
    bl = k.wrap(body, w - 32, "body-s")
    tl = k.wrap(title, w - 62, "h3")
    th = len(tl) * 22
    h = 44 + th + len(bl) * 19 + 8 + 44 + 8 + 44 + 16
    out = [rect(x, y, w, h, P["surface"], 16, stroke=P["border"])]
    out.append(icon("info", x + 16, y + 18, 20, P["info"]))
    for i, ln in enumerate(tl):
        out.append(text(x + 46, y + 33 + i * 22, ln, "h3", P["text-primary"]))
    for i, ln in enumerate(bl):
        out.append(text(x + 16, y + 46 + th + i * 19, ln, "body-s", P["text-secondary"]))
    by = y + 46 + th + len(bl) * 19 + 8
    out.append(button(x + 16, by, primary, "secondary", "M", theme=theme, width=w - 32, trailing="external"))
    out.append(button(x + 16, by + 52, secondary, "tertiary", "M", theme=theme, width=w - 32, icon_name="chat"))
    return group("deflect-card", *out), h


def skeleton_card(x, y, w, theme="dark", h_media=None):
    P = PAL[theme]
    mh = h_media or w * 2 / 3
    c = P["surface-muted"]
    return group("skeleton", rect(x, y, w, mh, c, 16), rect(x, y + mh + 16, w * .3, 10, c, 5),
                 rect(x, y + mh + 36, w * .9, 14, c, 7), rect(x, y + mh + 58, w * .65, 14, c, 7),
                 rect(x, y + mh + 82, w * .4, 10, c, 5))
