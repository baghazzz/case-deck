"""02–06, 10, 11: tokens, typography, colour, grid, icons, motion, SVG assets."""
import json
import math
import os

import tokens as tk
import svgkit as k
import components as c
from svgkit import text, rect, line, circle, path, para, icon, tw, group, media
from sheets import sheet, conf_tag, section_label
from components import DARK, LIGHT

OUT = "/home/claude/out/glance-inspired-design-system"


def w(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(content)


# ====================================================================== 02 tokens
def color_entry(tok, val, theme, usage, conf):
    bg = tk.C_DARK_HEX["background"] if theme == "dark" else tk.C_LIGHT_HEX["background"]
    comp = tk.blend(val, bg) if tk.alpha_of(val) < 1 else val
    cr = tk.contrast(comp, bg)
    crw = tk.contrast(comp, "#FFFFFF")
    crb = tk.contrast(comp, "#000000")
    if cr >= 7:
        g = "AAA text on background"
    elif cr >= 4.5:
        g = "AA text on background"
    elif cr >= 3:
        g = "Large text / icons / UI only on background"
    else:
        g = "Decorative / surface only; never text on background"
    return {"$value": tk.css_color(val), "$type": "color", "hex": val.upper(), "rgb": tk.rgb_str(val), "hsl": tk.hsl_str(val),
            "usage": usage, "contrast": {"onBackground": round(cr, 2), "withWhite": round(crw, 2), "withBlack": round(crb, 2),
                                         "guidance": g},
            "confidence": f"{conf} {tk.CONF_NAME[conf]}",
            "note": "Observed / reconstructed approximation. Not an official Glance value." if conf != tk.ORIG else
            "Original interpretation for this system."}


def build_tokens():
    colors = {"$description": f"{tk.SYSTEM_NAME} colour tokens. Dark is the default theme; light mirrors every role.",
              "source-note": "Brand hues #FF0049 and #DDBEF0 are observed via a public brand registry (Brandfetch). All other values are reconstructed approximations, not official Glance values.",
              "dark": {}, "light": {}, "overlay": {}}
    for t, d, l, u, cf in tk.COLORS:
        colors["dark"][t] = color_entry(t, d, "dark", u, cf)
        colors["light"][t] = color_entry(t, l, "light", u, cf)
    for t, v, u, cf in tk.OVERLAYS:
        colors["overlay"][t] = {"$value": v, "$type": "color" if not v.startswith("linear") else "gradient", "usage": u,
                                "confidence": f"{cf} {tk.CONF_NAME[cf]}"}
    w("02_DESIGN_TOKENS/colors.json", json.dumps(colors, indent=2, ensure_ascii=False))

    typo = {"$description": "Type tokens. Sizes are mobile; desktop multipliers in 'responsive'.",
            "families": {"display": {"$value": tk.FONT_DISPLAY, "note": "Instrument Serif (OFL). Editorial hooks only. ◇ Original interpretation"},
                         "sans": {"$value": tk.FONT_SANS, "note": "Inter (OFL). Everything functional. ○ Reconstruction — production face not confirmed"}},
            "styles": {}, "responsive": {"display-xl": 72, "display": 56, "h1": 40, "h2": 28, "headline-media": 32, "body-l": 18}}
    for n, v in tk.T.items():
        typo["styles"][n] = {"fontFamily": "{families.%s}" % v["family"], "fontWeight": v["weight"], "fontSize": f"{v['size']}px",
                             "lineHeight": v["lh"], "letterSpacing": f"{v['ls']}em", "maxLineLength": f"{v['max']}ch",
                             "textTransform": "uppercase" if n == "label" else "none", "usage": v["usage"],
                             "confidence": f"{v['conf']} {tk.CONF_NAME[v['conf']]}"}
    w("02_DESIGN_TOKENS/typography.json", json.dumps(typo, indent=2, ensure_ascii=False))

    w("02_DESIGN_TOKENS/spacing.json", json.dumps({"$description": "4px base unit. ○ Reconstruction of a 4/8 rhythm.",
                                                    "base": "4px", "scale": {n: {"$value": f"{v}px", "usage": tk.SPACE_USAGE.get(n, "")} for n, v in tk.SPACE},
                                                    "layout": {"screen-margin-mobile": "16px", "screen-margin-tablet": "24px",
                                                               "screen-margin-desktop": "32px", "gutter-mobile": "12px", "gutter-tablet": "16px",
                                                               "gutter-desktop": "24px", "card-padding": "16px", "card-padding-large": "20px",
                                                               "section-gap-mobile": "32px", "section-gap-desktop": "48px", "rail-card-gap": "12px"}}, indent=2))
    w("02_DESIGN_TOKENS/radius.json", json.dumps({n: {"$value": f"{v}px" if v != 999 else "999px", "usage": u, "confidence": f"{cf} {tk.CONF_NAME[cf]}"}
                                                  for n, v, u, cf in tk.RADIUS}, indent=2, ensure_ascii=False))
    w("02_DESIGN_TOKENS/shadows.json", json.dumps({n: {"$value": v, "usage": u, "confidence": f"{cf} {tk.CONF_NAME[cf]}"}
                                                   for n, v, u, cf in tk.SHADOWS}, indent=2, ensure_ascii=False))
    w("02_DESIGN_TOKENS/borders.json", json.dumps({n: {"$value": v, "usage": u} for n, v, u in tk.BORDERS}, indent=2))
    w("02_DESIGN_TOKENS/motion.json", json.dumps({
        "duration": {n: f"{v}ms" for n, v in tk.DURATION.items()},
        "easing": tk.EASING,
        "interactions": {n: {"duration": f"{d}ms", "easing": e, "behaviour": b, "confidence": f"{cf} {tk.CONF_NAME[cf]}"}
                         for n, d, e, b, cf in tk.MOTION},
        "reducedMotion": "Under prefers-reduced-motion: transforms become 0ms cross-fades of 160ms; story auto-advance pauses; live-pulse stops."},
        indent=2, ensure_ascii=False))
    css = tokens_css()
    w("02_DESIGN_TOKENS/design-tokens.css", css)
    w("14_IMPLEMENTATION/tokens.css", css)


def tokens_css():
    L = [f"/* {tk.SYSTEM_NAME} — {tk.SYSTEM_TAG} · design tokens v{tk.VERSION}",
         "   Generated from build/tokens.py. Dark is the default theme; add data-theme=\"light\" to any element for light.",
         "   ● observed  ◐ strong inference  ○ reconstruction  ◇ original interpretation",
         "   Colour values are observed/reconstructed approximations, not official Glance values. */", "",
         ":root {", "  color-scheme: dark;", "  /* colour · dark (default) */"]
    for t, d, l, u, cf in tk.COLORS:
        L.append(f"  --color-{t}: {tk.css_color(d)}; /* {cf} {u} */")
    L.append("  --color-primary-hover: #D1003A;")
    L.append("")
    L.append("  /* content overlays (theme-independent) */")
    for t, v, u, cf in tk.OVERLAYS:
        L.append(f"  --{t}: {v};")
    L.append("")
    L.append("  /* type */")
    L.append(f"  --font-display: {tk.FONT_DISPLAY};")
    L.append(f"  --font-sans: {tk.FONT_SANS};")
    for n, v in tk.T.items():
        L.append(f"  --type-{n}-size: {v['size']}px; --type-{n}-weight: {v['weight']}; --type-{n}-line: {v['lh']}; --type-{n}-tracking: {v['ls']}em;")
    L.append("")
    L.append("  /* space (4px base) */")
    L.append("  " + " ".join(f"--{n}: {v}px;" for n, v in tk.SPACE))
    L.append("  --screen-margin: 16px; --gutter: 12px; --section-gap: 32px; --content-max: 1280px;")
    L.append("")
    L.append("  /* radius */")
    L.append("  " + " ".join(f"--{n}: {v}px;" for n, v, u, cf in tk.RADIUS))
    L.append("")
    L.append("  /* elevation */")
    for n, v, u, cf in tk.SHADOWS:
        L.append(f"  --{n}: {v};")
    L.append("")
    L.append("  /* borders */")
    for n, v, u in tk.BORDERS:
        L.append(f"  --{n}: {v};")
    L.append("")
    L.append("  /* motion */")
    for n, v in tk.DURATION.items():
        L.append(f"  --motion-duration-{n}: {v}ms;")
    for n, v in tk.EASING.items():
        L.append(f"  --motion-ease-{n}: {v};")
    L.append("}")
    L.append("")
    L.append('[data-theme="light"] {')
    L.append("  color-scheme: light;")
    for t, d, l, u, cf in tk.COLORS:
        if d != l:
            L.append(f"  --color-{t}: {tk.css_color(l)};")
    L.append("  --color-primary-hover: #D1003A;")
    L.append("}")
    L.append("")
    L.append("@media (min-width: 600px) { :root { --screen-margin: 24px; --gutter: 16px; --section-gap: 40px; } }")
    L.append("@media (min-width: 1024px) { :root { --screen-margin: 32px; --gutter: 24px; --section-gap: 48px;")
    L.append("  --type-display-xl-size: 72px; --type-display-size: 56px; --type-h1-size: 40px; --type-h2-size: 28px;")
    L.append("  --type-headline-media-size: 32px; --type-body-l-size: 18px; } }")
    L.append("@media (min-width: 1440px) { :root { --screen-margin: 48px; --content-max: 1360px; } }")
    L.append("@media (prefers-reduced-motion: reduce) { :root { --motion-duration-fast: 0ms; --motion-duration-base: 0ms; --motion-duration-slow: 160ms; } }")
    return "\n".join(L) + "\n"


# ====================================================================== 03 typography
def build_typography():
    s = sheet(1600, 1500, "Foundations · 03", "Type scale",
              "Two families. Instrument Serif carries the editorial hook, sparingly. Inter carries everything that has to be read fast. "
              "Sizes are mobile; desktop steps up at 1024px.", "Type scale")
    y = 250
    col_spec = 1060
    for n, v in tk.T.items():
        sample = {"display-xl": "Starring you, every morning", "display": "Pick what wakes you up",
                  "headline-media": "Monsoon's over. Six beaches worth the flight", "h1": "Your trips", "h2": "Because you saved Goa",
                  "h3": "The quiet hill towns nobody has told you about", "body-l": "A slow itinerary for the city that wakes before you do.",
                  "body": "Fares are checked live before you see them, and every rule links to its source.",
                  "body-s": "Price includes taxes and our fee. It can change until you book.",
                  "caption": "Photo: original placeholder art", "label": "Travel · For you", "button": "Plan a trip",
                  "metadata": "Wake Travel · 4 min · ₹5,842 · 9:41"}[n]
        fam = v["family"]
        s.add(text(64, y + v["size"] * .85, sample, n, DARK["text-primary"], upper=(n == "label"), tnum=(n == "metadata")))
        s.add(text(col_spec, y + 14, n, "button", DARK["text-primary"], size=14))
        spec = f"{'Instrument Serif' if fam == 'display' else 'Inter'} {v['weight']} · {v['size']}/{v['lh']} · {v['ls']:+}em · ≤{v['max']}ch"
        s.add(text(col_spec, y + 34, spec, "metadata", DARK["text-secondary"]))
        s.add(text(col_spec, y + 52, v["usage"][:62], "caption", DARK["text-tertiary"]))
        s.add(conf_tag(1400, y + 14, v["conf"]))
        step = max(v["size"] * 1.25, 60) + 28
        s.add(line(64, y + step - 12, 1536, y + step - 12, DARK["divider"]))
        y += step
    s.save(f"{OUT}/03_TYPOGRAPHY/type-scale.svg")

    # samples in context
    s = sheet(1600, 1100, "Foundations · 03", "Type in context",
              "The hook is set in the serif only when the moment is editorial. On media, Inter Bold at 26px is the workhorse; "
              "metadata always uses middle dots and tabular numerals.", "Typography samples")
    s.add(c.card_hero(s, 64, 240, 358, 448))
    g, h = c.card_editorial(s, 470, 240, 358)
    s.add(g)
    # article column
    ax = 880
    s.add(c.kicker(ax, 262, "Visa & entry · Cited", DARK["primary-light"]))
    t, th = para(ax, 310, "What changes for Indian travellers this winter", 620, "display", DARK["text-primary"], size=44, lh=1.05)
    s.add(t)
    s.add(k.meta(ax, 310 + th + 6, ("Wake Travel desk", "Last verified 29 Sep 2026", "5 min"), DARK["text-tertiary"]))
    body = ("Every entry rule in this piece links to the official page it came from. Where a rule changed in the last seven days, "
            "we say so, and we tell you to check again before you fly. Prices quoted below were checked live at 9:41 and can move "
            "until you book.")
    t, bh = para(ax, 310 + th + 50, body, 620, "body-l", DARK["text-secondary"])
    s.add(t)
    qy = 310 + th + 50 + bh + 30
    s.add(rect(ax, qy, 3, 90, DARK["primary"]))
    t, qh = para(ax + 24, qy + 34, "Volatile facts are fetched. Rules are cited. Nothing is left to memory.", 580, "display", DARK["text-primary"], size=30, italic=True, lh=1.15)
    s.add(t)
    # pairing rules
    py = 790
    s.add(section_label(ax, py, "Pairing rules"))
    rules = ["Serif for the hook, never for UI chrome, labels, or numbers.",
             "One serif moment per screen. If the hero uses it, cards do not.",
             "Numbers are Inter with tabular figures, so prices align and do not jitter.",
             "Uppercase only for labels and kickers, tracked +8%.",
             "On media: Inter Bold, two lines max, always over the bottom scrim."]
    for i, r in enumerate(rules):
        s.add(text(ax, py + 34 + i * 30, f"{i + 1}", "button", DARK["primary"], size=14))
        s.add(text(ax + 28, py + 34 + i * 30, r, "body", DARK["text-secondary"]))
    s.save(f"{OUT}/03_TYPOGRAPHY/typography-samples.svg")


# ====================================================================== 04 colour
def swatch(s, x, y, w_, h_, t, val, usage, conf, fg, theme):
    s.add(rect(x, y, w_, h_, tk.css_color(val), 12, stroke=DARK["border"] if theme == "dark" else "#E2E0E8"))
    s.add(text(x, y + h_ + 24, t, "button", fg, size=14))
    s.add(text(x, y + h_ + 44, val.upper(), "metadata", fg, opacity=.72))
    s.add(k.conf_mark(x + k.tw(val.upper(), "metadata") + 8, y + h_ + 44, conf, fg, 9))
    lines = k.wrap(usage, w_, "caption")[:2]
    for i, ln in enumerate(lines):
        s.add(text(x, y + h_ + 62 + i * 16, ln, "caption", fg, opacity=.56))


def build_colors():
    groups = [("Brand · signal & iris", ["primary", "primary-action", "primary-dark", "primary-light", "primary-subtle", "iris", "iris-strong", "iris-subtle"]),
              ("Neutral · stage & surfaces", ["stage", "background", "surface", "surface-elevated", "surface-muted", "border", "divider"]),
              ("Text", ["text-primary", "text-secondary", "text-tertiary", "text-on-media"]),
              ("Semantic", ["success", "warning", "error", "info"])]
    cmap = {t: (d, l, u, cf) for t, d, l, u, cf in tk.COLORS}
    s = sheet(1600, 1640, "Foundations · 04", "Colour",
              "Red means now. Lavender means you. Everything else is a dark stage that lets imagery do the talking. "
              "#FF0049 and #DDBEF0 are observed brand hues; all other values are reconstructed approximations.", "Colour palette")
    y = 240
    for gname, toks in groups:
        s.add(section_label(64, y, gname))
        y += 22
        x = 64
        for t in toks:
            d, l, u, cf = cmap[t]
            swatch(s, x, y, 170, 96, t, d, u, cf, "#FFFFFF", "dark")
            x += 184
        y += 210
    # overlays
    s.add(section_label(64, y, "Content overlays"))
    y += 22
    x = 64
    for t, v, u, cf in tk.OVERLAYS[:6]:
        s.add(media(s, x, y, 220, 120, "dusk", 12))
        if t == "scrim-bottom":
            s.add(k.scrim_bottom(s, x, y, 220, 120, .0, .85, 12))
        elif t == "scrim-top":
            s.add(k.scrim_top(s, x, y, 220, 60, .55, 12))
        else:
            fill = {"scrim-full": "rgba(0,0,0,.48)", "glass": "rgba(22,22,27,.56)", "glass-light": "rgba(255,255,255,.16)",
                    "video-control": "rgba(255,255,255,.92)"}[t]
            if t in ("glass", "glass-light", "video-control"):
                s.add(rect(x + 40, y + 36, 140, 48, fill, 24))
            else:
                s.add(rect(x, y, 220, 120, fill, 12))
        s.add(text(x, y + 146, t, "button", "#FFFFFF", size=14))
        s.add(k.conf_label(x, y + 166, cf, u[:34], DARK["text-tertiary"]))
        x += 244
    y += 210
    # ratio bar
    s.add(section_label(64, y, "Colour budget on a typical screen"))
    y += 20
    parts = [("stage + background", .62, "#000000"), ("imagery", .24, None), ("surfaces", .09, "#202027"), ("text", .035, "#FFFFFF"),
             ("iris", .01, "#DDBEF0"), ("signal", .005, "#FF0049")]
    x = 64
    total = 1472
    for n, f, col in parts:
        ww = total * f
        if col:
            s.add(rect(x, y, ww, 36, col, 0, stroke=DARK["border"]))
        else:
            s.add(media(s, x, y, ww, 36, "dusk"))
        x += ww
    s.add(text(64, y + 64, "≈ 62% stage · 24% imagery · 9% surfaces · 3.5% text · 1% iris · 0.5% signal (a target, not a measurement)", "caption", DARK["text-tertiary"]))
    s.save(f"{OUT}/04_COLORS/palette.svg")

    for theme in ("light", "dark"):
        P = LIGHT if theme == "light" else DARK
        s = k.Svg(1600, 1000, f"{theme.title()} theme", f"{theme.title()} theme role map", bg=P["background"])
        s.add(text(64, 84, "Foundations · 04", "label", P["primary"] if theme == "dark" else P["primary-dark"], upper=True, size=12))
        s.add(text(64, 148, f"{theme.title()} theme", "display", P["text-primary"], size=64))
        s.add(text(64, 190, "Same roles, same component anatomy; only the values change. Media, scrims and the stage stay dark in both.",
                   "body", P["text-secondary"]))
        # role list
        y = 250
        for i, (t, d, l, u, cf) in enumerate(tk.COLORS):
            val = l if theme == "light" else d
            col = i // 12
            row = i % 12
            x = 64 + col * 380
            yy = y + row * 56
            s.add(rect(x, yy, 40, 40, tk.css_color(val), 10, stroke=P["border"]))
            s.add(text(x + 56, yy + 18, t, "button", P["text-primary"], size=14))
            cr = tk.contrast_note(t, theme)
            s.add(text(x + 56, yy + 36, f"{val.upper()} · {cr:.2f}:1 on bg", "metadata", P["text-tertiary"]))
        # mini UI
        px = 900
        s.add(rect(px, 240, 636, 700, P["surface"], 24))
        s.add(c.category_tabs(px + 32, 290, ["For you", "Travel", "Style", "News"], 0, theme))
        g, hh = c.card_standard(s, px + 32, 324, 270, "lagoon", "Travel", "Six beaches worth the flight", ("Wake Travel", "4 min"), theme)
        s.add(g)
        g, hh = c.card_commerce(s, px + 334, 324, 270, "sneaker", theme=theme, ratio=(3, 2))
        s.add(g)
        s.add(c.button(px + 32, 640, "Plan a trip", "primary", "L", theme=theme, trailing="arrow"))
        s.add(c.button(px + 210, 640, "Save", "secondary", "L", theme=theme, icon_name="bookmark"))
        s.add(c.button(px + 340, 640, "Share", "tertiary", "L", theme=theme, icon_name="share"))
        s.add(c.chip_row(px + 32, 720, ["For you", ("Street style", "personalization"), "Cricket"], theme))
        bx = px + 32
        for kd, lab in [("live-fare", "Live fare"), ("for-you", "For you"), ("verified", "Verified"), ("warning", "Price changed")]:
            g, bw = c.badge(bx, 780, lab, kd, theme)
            s.add(g)
            bx += bw + 8
        s.add(c.search_field(px + 32, 830, 572, theme=theme))
        s.save(f"{OUT}/04_COLORS/{theme}-theme.svg")


# ====================================================================== 05 grid & layout
def build_grid():
    s = sheet(1600, 1200, "Foundations · 05", "Grid",
              "Four columns on phones, eight on tablets, twelve on desktop. Media breaks the grid on purpose: full-bleed on mobile, "
              "edge-to-edge rails that peek past the margin.", "Grid system")
    frames = [("Mobile · 390", 64, 250, 390, 760, 4, 16, 12), ("Tablet · 820", 520, 250, 600, 760, 8, 24, 16),
              ("Desktop · 1440 (scaled 0.26)", 1180, 250, 356, 760, 12, 32 * .26, 24 * .26)]
    for name, x, y, fw, fh, cols, m, gtr in frames:
        s.add(rect(x, y, fw, fh, DARK["surface"], 16, stroke=DARK["border"]))
        cw = (fw - 2 * m - gtr * (cols - 1)) / cols
        for i in range(cols):
            s.add(rect(x + m + i * (cw + gtr), y, cw, fh, "#FF0049", 0, opacity=.12))
        s.add(text(x, y - 16, name, "button", DARK["text-primary"], size=14))
        s.add(text(x, y + fh + 28, f"{cols} col · margin {round(m / (0.26 if 'Desktop' in name else 1))} · gutter {round(gtr / (0.26 if 'Desktop' in name else 1))}",
                   "metadata", DARK["text-tertiary"]))
    # breakpoint table
    y = 1080
    s.add(section_label(64, y - 30, "Breakpoints"))
    xs = [64, 300, 520, 700, 880, 1060]
    for i, h_ in enumerate(["Name", "Range", "Columns", "Margin", "Gutter", "Content"]):
        s.add(text(xs[i], y, h_, "caption", DARK["text-tertiary"], weight=600))
    for r, (n, lo, hi, cols, m, g, cont) in enumerate(tk.BREAKPOINTS):
        yy = y + 0
    s.save(f"{OUT}/05_GRID_AND_LAYOUT/grid.svg")
    # rebuild with a proper table
    s = sheet(1600, 1320, "Foundations · 05", "Grid",
              "Four columns on phones, eight on tablets, twelve on desktop. Media breaks the grid on purpose: full-bleed on mobile, "
              "edge-to-edge rails that peek past the margin.", "Grid system")
    for name, x, y, fw, fh, cols, m, gtr in frames:
        s.add(rect(x, y, fw, fh, DARK["surface"], 16, stroke=DARK["border"]))
        cw = (fw - 2 * m - gtr * (cols - 1)) / cols
        for i in range(cols):
            s.add(rect(x + m + i * (cw + gtr), y, cw, fh, "#FF0049", 0, opacity=.12))
        s.add(text(x, y - 16, name, "button", DARK["text-primary"], size=14))
    y = 1080
    xs = [64, 280, 500, 680, 860, 1040]
    for i, h_ in enumerate(["Breakpoint", "Range", "Columns", "Margin", "Gutter", "Content width"]):
        s.add(text(xs[i], y, h_, "caption", DARK["text-tertiary"], weight=600))
    for r, (n, lo, hi, cols, m, g, cont) in enumerate(tk.BREAKPOINTS):
        yy = y + 36 + r * 36
        vals = [n, f"{lo}–{hi if hi else '∞'}px", str(cols), f"{m}px", f"{g}px", cont]
        for i, v in enumerate(vals):
            s.add(text(xs[i], yy, v, "body", DARK["text-primary"] if i == 0 else DARK["text-secondary"], weight=600 if i == 0 else 400))
        s.add(line(64, yy + 14, 1536, yy + 14, DARK["divider"]))
    s.save(f"{OUT}/05_GRID_AND_LAYOUT/grid.svg")

    # spacing scale
    s = sheet(1600, 1000, "Foundations · 05", "Space",
              "A 4px base with an 8px rhythm. Odd steps (12, 20) exist for type-driven gaps inside cards; everything structural lands on 8.",
              "Spacing scale")
    y = 250
    for n, v in tk.SPACE[1:]:
        s.add(text(64, y + 16, n, "button", DARK["text-primary"], size=14))
        s.add(text(200, y + 16, f"{v}px", "metadata", DARK["text-secondary"]))
        s.add(rect(300, y, v * 4, 22, DARK["primary"], 2))
        s.add(text(300 + v * 4 + 16, y + 16, tk.SPACE_USAGE.get(n, ""), "caption", DARK["text-tertiary"]))
        y += 56
    s.save(f"{OUT}/05_GRID_AND_LAYOUT/spacing-scale.svg")

    # responsive layouts (wireframes)
    s = sheet(1600, 1500, "Foundations · 05", "Responsive layouts",
              "Five layout archetypes at three breakpoints. Media blocks are shown solid; text blocks as bars. "
              "The hierarchy never changes between sizes; only the number of things side by side does.", "Responsive layouts")
    arche = ["Feed", "Content detail", "Commerce", "Recommendation", "Editorial"]
    M, Tb, D = DARK["surface-muted"], DARK["text-tertiary"], DARK["primary"]
    for i, a in enumerate(arche):
        y = 240 + i * 245
        s.add(text(64, y + 20, a, "h3", DARK["text-primary"]))
        # mobile
        mx, tx_, dx = 260, 460, 900
        s.add(rect(mx, y, 110, 210, DARK["surface"], 12, stroke=DARK["border"]))
        s.add(rect(tx_, y, 320, 210, DARK["surface"], 12, stroke=DARK["border"]))
        s.add(rect(dx, y, 636, 210, DARK["surface"], 12, stroke=DARK["border"]))
        if a == "Feed":
            s.add(media(s, mx + 8, y + 8, 94, 118, "lagoon", 8))
            s.add(rect(mx + 8, y + 134, 60, 6, Tb, 3))
            s.add(media(s, mx + 8, y + 150, 44, 52, "desert", 6)); s.add(media(s, mx + 58, y + 150, 44, 52, "city", 6))
            s.add(media(s, tx_ + 12, y + 12, 296, 110, "lagoon", 8))
            for j in range(3):
                s.add(media(s, tx_ + 12 + j * 100, y + 132, 92, 66, ["desert", "city", "mountain"][j], 6))
            s.add(media(s, dx + 16, y + 16, 400, 178, "lagoon", 8))
            for j in range(2):
                for q in range(2):
                    s.add(media(s, dx + 428 + q * 98, y + 16 + j * 92, 90, 86, ["desert", "city", "mountain", "food"][j * 2 + q], 6))
        elif a == "Content detail":
            s.add(media(s, mx, y, 110, 90, "temple", 12))
            for j in range(6):
                s.add(rect(mx + 10, y + 102 + j * 15, 90 - (j % 3) * 14, 6, Tb, 3))
            s.add(media(s, tx_, y, 320, 100, "temple", 12))
            for j in range(5):
                s.add(rect(tx_ + 40, y + 114 + j * 17, 240 - (j % 2) * 40, 7, Tb, 3))
            s.add(media(s, dx, y, 636, 90, "temple", 12))
            for j in range(5):
                s.add(rect(dx + 130, y + 106 + j * 18, 300 - (j % 2) * 50, 7, Tb, 3))
            s.add(rect(dx + 470, y + 106, 140, 90, M, 8))
        elif a == "Commerce":
            for j in range(2):
                for q in range(2):
                    s.add(media(s, mx + 8 + q * 49, y + 8 + j * 100, 45, 60, ["sneaker", "bag", "lamp", "watch"][j * 2 + q], 6))
                    s.add(rect(mx + 8 + q * 49, y + 72 + j * 100, 30, 5, Tb, 2))
            for q in range(4):
                s.add(media(s, tx_ + 12 + q * 76, y + 12, 70, 88, ["sneaker", "bag", "lamp", "watch"][q], 6))
                s.add(media(s, tx_ + 12 + q * 76, y + 112, 70, 88, ["watch", "lamp", "bag", "sneaker"][q], 6))
            s.add(media(s, dx + 16, y + 16, 220, 178, "studio", 8))
            for q in range(4):
                s.add(media(s, dx + 248 + q * 94, y + 16, 86, 108, ["sneaker", "bag", "lamp", "watch"][q], 6))
                s.add(rect(dx + 248 + q * 94, y + 134, 60, 6, Tb, 3))
        elif a == "Recommendation":
            s.add(rect(mx + 8, y + 8, 60, 8, "#DDBEF0", 4, opacity=.7))
            for j in range(3):
                s.add(media(s, mx + 8, y + 24 + j * 62, 94, 54, ["desert", "mountain", "beach-city"][j], 6))
            s.add(rect(tx_ + 12, y + 12, 120, 8, "#DDBEF0", 4, opacity=.7))
            for q in range(3):
                s.add(media(s, tx_ + 12 + q * 100, y + 30, 92, 168, ["desert", "mountain", "beach-city"][q], 8))
            s.add(rect(dx + 16, y + 16, 180, 8, "#DDBEF0", 4, opacity=.7))
            for q in range(5):
                s.add(media(s, dx + 16 + q * 122, y + 34, 114, 160, ["desert", "mountain", "beach-city", "lagoon", "temple"][q], 8))
        else:
            s.add(media(s, mx + 8, y + 8, 94, 64, "temple", 6))
            s.add(rect(mx + 8, y + 82, 80, 10, DARK["text-secondary"], 3))
            for j in range(5):
                s.add(rect(mx + 8, y + 104 + j * 14, 90 - (j % 2) * 20, 5, Tb, 2))
            s.add(media(s, tx_ + 12, y + 12, 180, 186, "temple", 8))
            s.add(rect(tx_ + 204, y + 20, 100, 12, DARK["text-secondary"], 3))
            for j in range(7):
                s.add(rect(tx_ + 204, y + 46 + j * 16, 100 - (j % 3) * 18, 5, Tb, 2))
            s.add(media(s, dx + 16, y + 16, 380, 178, "temple", 8))
            s.add(rect(dx + 412, y + 24, 200, 16, DARK["text-secondary"], 4))
            for j in range(6):
                s.add(rect(dx + 412, y + 56 + j * 18, 200 - (j % 3) * 30, 6, Tb, 3))
    for lbl, xx in [("Mobile", 260), ("Tablet", 460), ("Desktop", 900)]:
        s.add(text(xx, 226, lbl, "label", DARK["text-tertiary"], upper=True))
    s.save(f"{OUT}/05_GRID_AND_LAYOUT/responsive-layouts.svg")


# ====================================================================== 06 icons
def build_icons():
    names = sorted(k.ICONS)
    for n in names:
        w(f"06_ICONS/svg/{n}.svg", k.icon_file(n))
    # sprite
    syms = []
    for n in names:
        inner = k.icon_file(n).split("\n", 1)[1].rsplit("</svg>", 1)[0]
        inner = inner.replace(f"<title>{n}</title>", "")
        syms.append(f'<symbol id="i-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{k.ICON_STROKE}" '
                    f'stroke-linecap="round" stroke-linejoin="round">{inner.replace(chr(10), "")}</symbol>')
    w("11_SVG_ASSETS/icons/sprite.svg", '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n' + "\n".join(syms) + "\n</svg>\n")
    # sheet
    s = sheet(1600, 1520, "Foundations · 06", "Iconography",
              f"{len(names)} original icons on a 24px grid: {k.ICON_STROKE}px stroke, round caps and joins, 2px live-area padding. "
              "Outline by default; the like heart fills when active.", "Icon sheet")
    y = 250
    for gname, lst in k.ICON_GROUPS.items():
        s.add(section_label(64, y, gname))
        y += 24
        for i, n in enumerate(lst):
            x = 64 + i * 122
            s.add(rect(x, y, 106, 96, DARK["surface"], 12))
            s.add(icon(n, x + 41, y + 24, 24, "#FFFFFF"))
            s.add(text(x + 53, y + 78, n, "caption", DARK["text-tertiary"], anchor="middle", size=11))
        y += 140
    # construction grid
    gx, gy = 64, y + 10
    s.add(section_label(gx, gy - 6, "Construction"))
    gy += 14
    for n_i, (n, sz) in enumerate([("personalization", 192), ("plane", 192)]):
        ox = gx + n_i * 240
        s.add(rect(ox, gy, sz, sz, DARK["surface"], 12))
        for i in range(25):
            s.add(line(ox + i * sz / 24, gy, ox + i * sz / 24, gy + sz, "#FFFFFF", .5, opacity=.08))
            s.add(line(ox, gy + i * sz / 24, ox + sz, gy + i * sz / 24, "#FFFFFF", .5, opacity=.08))
        s.add(rect(ox + sz / 12, gy + sz / 12, sz * 10 / 12, sz * 10 / 12, "none", 0, stroke="#FF0049", sw=1, opacity=.6))
        s.add(icon(n, ox, gy, sz, "#FFFFFF", sw=k.ICON_STROKE * 8))
    rx = 600
    for i, r in enumerate(["24 × 24 grid, 20 × 20 live area", f"{k.ICON_STROKE}px stroke at 24px; stroke is compensated so 16px and 20px icons keep the same optical weight",
                           "Round caps and joins; corners use 1–1.5px radii", "Filled only for active state (like) and play",
                           "Icon colour follows text colour; iris for personalisation, signal only when live"]):
        s.add(text(rx, gy + 24 + i * 34, f"· {r}", "body", DARK["text-secondary"]))
    s.save(f"{OUT}/06_ICONS/icon-sheet.svg")


# ====================================================================== 10 motion
def build_motion():
    s = sheet(1600, 1200, "Foundations · 10", "Motion",
              "Fast in, quick out, nothing bounces except a like. Media moves with the finger; chrome moves after it. "
              "All values are inferred or reconstructed; production timing is not publicly documented.", "Motion transitions")
    # easing curves
    x0, y0 = 64, 250
    for i, (n, e) in enumerate([(n, v) for n, v in tk.EASING.items() if n != "linear"]):
        x = x0 + i * 250
        s.add(rect(x, y0, 220, 220, DARK["surface"], 12))
        nums = [float(v) for v in e[e.index("(") + 1:-1].split(",")]
        px, py, sz = x + 30, y0 + 190, 160
        d = f"M{px} {py} C{px + nums[0] * sz} {py - nums[1] * sz} {px + nums[2] * sz} {py - nums[3] * sz} {px + sz} {py - sz}"
        s.add(line(px, py, px + sz, py, DARK["border"]))
        s.add(line(px, py, px, py - sz, DARK["border"]))
        s.add(path(d, stroke="#FF0049", sw=3))
        s.add(text(x + 16, y0 + 250, n, "button", "#FFFFFF", size=14))
        s.add(text(x + 16, y0 + 270, e, "metadata", DARK["text-tertiary"]))
    # durations
    dx = 1100
    s.add(section_label(dx, y0 + 6, "Durations"))
    for i, (n, v) in enumerate(tk.DURATION.items()):
        yy = y0 + 36 + i * 44
        s.add(text(dx, yy + 14, n, "button", "#FFFFFF", size=14))
        s.add(text(dx + 100, yy + 14, f"{v}ms", "metadata", DARK["text-secondary"]))
        s.add(rect(dx + 180, yy + 2, min(v, 5000) / 1400 * 240 if v < 1000 else 250, 14, DARK["primary"], 7, opacity=1 if v < 1000 else .4))
    # storyboard: shared-element card to detail
    sy = 600
    s.add(section_label(64, sy, "Shared-media transition · card → detail · 360ms emphasized"))
    frames = [0, .25, .6, 1]
    for i, f in enumerate(frames):
        fx = 64 + i * 380
        s.add(rect(fx, sy + 24, 180, 390, DARK["stage"], 20, stroke=DARK["border"]))
        # card grows
        cx = fx + 12 + (0 - 12) * f
        cy = sy + 150 + (sy + 24 - (sy + 150)) * f
        cw = 156 + (180 - 156) * f
        ch = 120 + (200 - 120) * f
        fc = k.clip_round(s, fx, sy + 24, 180, 390, 20)
        s.add(f'<g clip-path="url(#{fc})">' + media(s, fx + 12 * (1 - f), cy, cw, ch, "lagoon", 12 * (1 - f) + 2) + "</g>")
        if f > .5:
            for j in range(4):
                s.add(rect(fx + 16, sy + 240 + j * 18, 140 - j * 20, 7, DARK["text-tertiary"], 3, opacity=(f - .5) * 2))
        s.add(text(fx, sy + 440, f"{int(f * 360)}ms", "metadata", DARK["text-secondary"]))
        if i < 3:
            s.add(icon("forward", fx + 250, sy + 200, 32, DARK["text-tertiary"]))
    s.add(text(64, sy + 500, "Media is the shared element: it scales from its card rect into the hero while the list dims to 40% and text fades in after 180ms.",
               "body", DARK["text-secondary"]))
    s.save(f"{OUT}/10_MOTION/transitions.svg")


# ====================================================================== 11 svg assets
def build_assets():
    base = f"{OUT}/11_SVG_ASSETS"
    # logos
    for theme, bgc, fg in [("dark", "#0C0C10", "#FFFFFF"), ("light", "#FFFFFF", "#0C0C10")]:
        s = k.Svg(320, 120, f"wake wordmark ({theme})", "Original placeholder wordmark for mockups", bg=None)
        s.add(c.wordmark(32, 78, fg, 56))
        s.save(f"{base}/logos/wake-wordmark-{theme}.svg")
    s = k.Svg(96, 96, "wake symbol", "Original placeholder app symbol")
    s.add(rect(0, 0, 96, 96, "#0C0C10", 24))
    s.add(text(48, 64, "w", "display", "#FFFFFF", size=64, italic=True, anchor="middle"))
    s.add(circle(70, 32, 6, "#FF0049"))
    s.save(f"{base}/logos/wake-symbol.svg")
    s = k.Svg(320, 120, "Partner logo slot", "Placeholder slot. Place a properly licensed partner or client mark here; the Glance logo is a trademark and is not a primitive of this system.")
    s.add(rect(1, 1, 318, 118, "none", 12, stroke="#85838F", sw=1.5, extra=' stroke-dasharray="6 6"'))
    s.add(text(160, 56, "Partner / client mark", "button", "#85838F", anchor="middle"))
    s.add(text(160, 80, "use licensed asset only", "caption", "#85838F", anchor="middle"))
    s.save(f"{base}/logos/logo-slot.svg")

    # gradients
    grads = {"scrim-bottom": [(0, "#000", 0), (.45, "#000", .35), (1, "#000", .85)],
             "scrim-top": [(0, "#000", .55), (1, "#000", 0)],
             "signal-iris": [(0, "#FF0049"), (1, "#DDBEF0")],
             "iris-night": [(0, "#251A2E"), (1, "#0C0C10")],
             "dusk": [(0, "#1A0B2E"), (.45, "#6A1C5C"), (.75, "#FF4D6D"), (1, "#FFB38A")]}
    for n, stops in grads.items():
        s = k.Svg(400, 400, f"Gradient: {n}", f"Gradient token {n}")
        horiz = n == "signal-iris"
        gid, g = k.lin_grad(stops, 0, 0, 1 if horiz else 0, 0 if horiz else 1)
        s.define(g)
        if n.startswith("scrim"):
            s.add(media(s, 0, 0, 400, 400, "lagoon"))
        s.add(rect(0, 0, 400, 400, f"url(#{gid})"))
        s.save(f"{base}/gradients/{n}.svg")

    # backgrounds
    s = k.Svg(1920, 1080, "Stage background", "Dark stage with faint signal glow")
    s.add(rect(0, 0, 1920, 1080, "#0C0C10"))
    gid, g = k.rad_grad([(0, "#FF0049", .22), (1, "#FF0049", 0)], .85, .1, .6)
    s.define(g)
    s.add(rect(0, 0, 1920, 1080, f"url(#{gid})"))
    s.save(f"{base}/backgrounds/stage-signal.svg")
    s = k.Svg(1920, 1080, "Iris aurora background", "Personalisation background: iris and signal fields on the stage")
    s.add(media(s, 0, 0, 1920, 1080, "iris"))
    s.save(f"{base}/backgrounds/iris-aurora.svg")
    s = k.Svg(1920, 1080, "Light paper background", "Light theme ground with a faint iris corner")
    s.add(rect(0, 0, 1920, 1080, "#F6F5F8"))
    gid, g = k.rad_grad([(0, "#DDBEF0", .45), (1, "#DDBEF0", 0)], .05, .95, .5)
    s.define(g)
    s.add(rect(0, 0, 1920, 1080, f"url(#{gid})"))
    s.save(f"{base}/backgrounds/light-iris.svg")

    # patterns
    s = k.Svg(400, 400, "Dot grid pattern", "8px dot grid used behind diagrams")
    pid = "dotgrid"
    s.define(f'<pattern id="{pid}" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#FFFFFF" opacity=".14"/></pattern>')
    s.add(rect(0, 0, 400, 400, "#0C0C10"), rect(0, 0, 400, 400, f"url(#{pid})"))
    s.save(f"{base}/patterns/dot-grid.svg")
    s = k.Svg(400, 400, "Scan lines pattern", "Fine horizontal lines for data-freshness moments")
    s.define('<pattern id="scan" width="400" height="6" patternUnits="userSpaceOnUse"><rect width="400" height="1" fill="#FFFFFF" opacity=".06"/></pattern>')
    s.add(rect(0, 0, 400, 400, "#0C0C10"), rect(0, 0, 400, 400, "url(#scan)"))
    s.save(f"{base}/patterns/scan-lines.svg")
    s = k.Svg(400, 400, "Contour pattern", "Topographic contours for travel moments")
    s.add(rect(0, 0, 400, 400, "#0C0C10"))
    for i in range(14):
        r_ = 20 + i * 22
        s.add(path(f"M{200 - r_} 220 C{200 - r_} {220 - r_ * 1.1} {200 + r_ * .9} {220 - r_ * .9} {200 + r_} 210 S{200 - r_ * .6} {230 + r_ * 1.05} {200 - r_} 220Z",
                   stroke="#DDBEF0", sw=1, opacity=round(.28 - i * .015, 3)))
    s.save(f"{base}/patterns/contours.svg")

    # decorative
    s = k.Svg(240, 240, "Live signal dot", "Live indicator: dot with pulse rings (animate ring scale 1→2.2, opacity .6→0)")
    s.add(circle(120, 120, 60, "#FF0049", opacity=.12), circle(120, 120, 36, "#FF0049", opacity=.25), circle(120, 120, 16, "#FF0049"))
    s.save(f"{base}/decorative/live-signal.svg")
    s = k.Svg(240, 240, "Iris sparkle", "Personalisation mark: sparkle on iris-subtle")
    s.add(circle(120, 120, 110, "#251A2E"), icon("personalization", 48, 48, 144, "#DDBEF0", sw=1.75 * 6))
    s.save(f"{base}/decorative/iris-sparkle.svg")
    s = k.Svg(600, 40, "Section separator", "Hairline with a signal dot, used between deck sections")
    s.add(line(0, 20, 280, 20, "#FFFFFF", 1, opacity=.16), circle(300, 20, 4, "#FF0049"), line(320, 20, 600, 20, "#FFFFFF", 1, opacity=.16))
    s.save(f"{base}/decorative/section-separator.svg")
    s = k.Svg(400, 60, "Highlight underline", "Marker-style underline for one key word in a deck title")
    s.add(path("M8 40 C120 28 280 26 392 34", stroke="#FF0049", sw=10, opacity=.9))
    s.save(f"{base}/decorative/highlight-underline.svg")
    s = k.Svg(200, 200, "Corner brackets", "Frame corners marking a focal point on an image")
    for (x, y, dx, dy) in [(20, 20, 1, 1), (180, 20, -1, 1), (20, 180, 1, -1), (180, 180, -1, -1)]:
        s.add(path(f"M{x} {y + dy * 36} V{y} H{x + dx * 36}", stroke="#FFFFFF", sw=3))
    s.save(f"{base}/decorative/focus-brackets.svg")
    s = k.Svg(400, 400, "Accent arc", "Quarter arc accent in signal to iris gradient")
    gid, g = k.lin_grad([(0, "#FF0049"), (1, "#DDBEF0")], 0, 0, 1, 1)
    s.define(g)
    s.add(path("M40 360 A320 320 0 0 1 360 40", stroke=f"url(#{gid})", sw=24))
    s.save(f"{base}/decorative/accent-arc.svg")
    s = k.Svg(400, 400, "Signal blob", "Soft gradient blob; one per composition, behind content only")
    fid = "blur"
    s.define('<filter id="blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="30"/></filter>')
    s.add(path("M200 60 C290 50 350 130 340 210 C330 300 250 350 180 340 C100 330 50 260 70 180 C85 110 130 70 200 60Z", "#FF0049", opacity=.7,
               extra=' filter="url(#blur)"'))
    s.add(path("M250 150 C310 150 330 220 300 260 C270 300 210 290 200 240 C190 190 210 150 250 150Z", "#DDBEF0", opacity=.8, extra=' filter="url(#blur)"'))
    s.save(f"{base}/decorative/signal-blob.svg")
    # masks
    masks = {"rounded": "M24 0H216A24 24 0 0 1 240 24V276A24 24 0 0 1 216 300H24A24 24 0 0 1 0 276V24A24 24 0 0 1 24 0Z",
             "arch": "M0 300V120A120 120 0 0 1 240 120V300Z", "pill": "M120 0A120 120 0 0 1 240 120V180A120 120 0 0 1 0 180V120A120 120 0 0 1 120 0Z",
             "ticket": "M16 0H224A16 16 0 0 1 240 16V130A20 20 0 0 0 240 170V284A16 16 0 0 1 224 300H16A16 16 0 0 1 0 284V170A20 20 0 0 0 0 130V16A16 16 0 0 1 16 0Z"}
    for n, d in masks.items():
        s = k.Svg(240, 300, f"Image mask: {n}", f"{n} mask applied to placeholder imagery")
        cid = k.clip_path_d(s, d)
        s.add(f'<g clip-path="url(#{cid})">' + media(s, 0, 0, 240, 300, "dusk") + "</g>")
        s.save(f"{base}/decorative/mask-{n}.svg")
    # illustrations (placeholder scenes)
    for sc in k.SCENES:
        s = k.Svg(400, 500, f"Placeholder image: {sc}", f"Original placeholder art ({sc}), 4:5. Replace with licensed photography in production.")
        s.add(media(s, 0, 0, 400, 500, sc))
        s.save(f"{base}/illustrations/{sc}.svg")
    # image-ratio composition
    s = sheet(1600, 1000, "Foundations · 11", "Image system",
              "Imagery is the layout. Ratios are chosen by job, crops keep the focal point in the upper-middle third, and every piece of "
              "text on an image sits on a scrim.", "Image ratios and treatment")
    x = 64
    for (rt, use, cf), sc in zip(tk.RATIOS, ["lagoon", "studio", "sneaker", "concert", "temple", "desert"]):
        a, b = [int(v) for v in rt.split(":")]
        hh = 300
        ww = hh * a / b
        if ww > 420:
            ww = 420
            hh = ww * b / a
        s.add(media(s, x, 250 + (300 - hh), ww, hh, sc, 16))
        s.add(text(x, 590, rt, "h3", "#FFFFFF"))
        lines = k.wrap(use, max(ww, 150), "caption")
        for i, ln in enumerate(lines[:3]):
            s.add(text(x, 612 + i * 16, ln, "caption", DARK["text-tertiary"]))
        s.add(conf_tag(x, 612 + len(lines[:3]) * 16 + 4, cf))
        x += ww + 28
    # treatment
    ty = 700
    s.add(section_label(64, ty, "Treatment"))
    items = [("No scrim", None), ("Bottom scrim .85", "b"), ("Top + bottom", "tb"), ("Focal third", "f")]
    for i, (lab, mode) in enumerate(items):
        xx = 64 + i * 200
        s.add(media(s, xx, ty + 20, 176, 176, "beach-city", 16))
        if mode in ("b", "tb"):
            s.add(k.scrim_bottom(s, xx, ty + 20, 176, 176, .2, .85, 16))
        if mode == "tb":
            s.add(k.scrim_top(s, xx, ty + 20, 176, 50, .55, 16))
        if mode == "f":
            for j in (1, 2):
                s.add(line(xx + 176 * j / 3, ty + 20, xx + 176 * j / 3, ty + 196, "#FFFFFF", 1, opacity=.5))
                s.add(line(xx, ty + 20 + 176 * j / 3, xx + 176, ty + 20 + 176 * j / 3, "#FFFFFF", 1, opacity=.5))
            s.add(circle(xx + 88, ty + 20 + 176 / 3, 8, "none", stroke="#FF0049", sw=2))
        if mode in ("b", "tb"):
            s.add(text(xx + 14, ty + 180, "Text lives here", "button", "#FFFFFF", size=14))
        s.add(text(xx, ty + 222, lab, "caption", DARK["text-secondary"]))
    rules = ["Radius 16 for cards, 24 for heroes, 0 for full-bleed.", "1px inner stroke at 8% white so dark images hold their edge.",
             "Object-position: center 35%; faces and products sit in the upper-middle third.",
             "Never put text on an image without scrim-bottom or scrim-top.", "Placeholder art in this package is original; replace with licensed photography."]
    for i, r_ in enumerate(rules):
        s.add(text(900, ty + 40 + i * 30, "· " + r_, "body", DARK["text-secondary"]))
    s.save(f"{base}/illustrations/_image-system.svg")


if __name__ == "__main__":
    build_tokens()
    build_typography()
    build_colors()
    build_grid()
    build_icons()
    build_motion()
    build_assets()
    print("foundations ok")
