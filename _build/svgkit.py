"""Low-level SVG primitives shared by every generated file.

Nothing here hard-codes a colour or size that is not in tokens.py.
"""
import math
import random
from functools import lru_cache
from xml.sax.saxutils import escape

from PIL import ImageFont

import tokens as tk

FONT_FILES = {
    ("sans", 400): "/root/.fonts/Inter-Regular.ttf",
    ("sans", 500): "/root/.fonts/Inter-Medium.ttf",
    ("sans", 600): "/root/.fonts/Inter-SemiBold.ttf",
    ("sans", 700): "/root/.fonts/Inter-Bold.ttf",
    ("sans", 800): "/root/.fonts/Inter-ExtraBold.ttf",
    ("display", 400): "/root/.fonts/InstrumentSerif-Regular.ttf",
    ("display-italic", 400): "/root/.fonts/InstrumentSerif-Italic.ttf",
}


@lru_cache(maxsize=None)
def _font(fam, weight, size):
    key = (fam, weight)
    if key not in FONT_FILES:
        key = (fam, 400) if (fam, 400) in FONT_FILES else ("sans", 400)
    return ImageFont.truetype(FONT_FILES[key], size=max(1, round(size * 4)))


def measure(s, size, weight=400, fam="sans", ls=0.0):
    """Width of a string in px (letter-spacing in em)."""
    if not s:
        return 0
    f = _font(fam, weight, size)
    w = f.getlength(s) / 4
    return w + ls * size * max(0, len(s) - 1)


def esc(s):
    return escape(str(s), {'"': "&quot;"})


# ---------------------------------------------------------------- document
class Svg:
    _uid = 0

    def __init__(self, w, h, title, desc="", bg=None, font_css=True):
        self.w, self.h = w, h
        self.title, self.desc = title, desc
        self.bg = bg
        self.parts = []
        self.defs = []
        self.font_css = font_css

    @classmethod
    def uid(cls, prefix="d"):
        cls._uid += 1
        return f"{prefix}{cls._uid}"

    def add(self, *frags):
        for f in frags:
            if f:
                self.parts.append(f)
        return self

    def define(self, frag):
        self.defs.append(frag)

    def render(self):
        style = (
            "<style>"
            f".sans{{font-family:{tk.FONT_SANS};}}"
            f".disp{{font-family:{tk.FONT_DISPLAY};}}"
            ".tnum{font-variant-numeric:tabular-nums;}"
            "</style>"
        )
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="t d">',
               f'<title id="t">{esc(self.title)}</title>',
               f'<desc id="d">{esc(self.desc or self.title)} · {tk.SYSTEM_NAME}, {tk.SYSTEM_TAG}. '
               f'Original vector artwork; not a Glance asset.</desc>',
               "<defs>" + style + "".join(self.defs) + "</defs>"]
        if self.bg:
            out.append(f'<rect id="background" width="{self.w}" height="{self.h}" fill="{self.bg}"/>')
        out.extend(self.parts)
        out.append("</svg>")
        return "\n".join(out)

    def save(self, path):
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(self.render())


def group(id_, *frags, transform=None, extra=""):
    t = f' transform="{transform}"' if transform else ""
    i = f' id="{id_}"' if id_ else ""
    return f"<g{i}{t}{extra}>" + "".join(f for f in frags if f) + "</g>"


# ---------------------------------------------------------------- shapes
def rect(x, y, w, h, fill="none", r=0, stroke=None, sw=1, opacity=None, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    rr = f' rx="{r}"' if r else ""
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}"{rr} fill="{fill}"{s}{o}{extra}/>'


def circle(cx, cy, r, fill="none", stroke=None, sw=1, opacity=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{fill}"{s}{o}/>'


def line(x1, y1, x2, y2, stroke, sw=1, dash=None, opacity=None, cap="butt"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}"{d}{o}/>')


def path(d, fill="none", stroke=None, sw=1, opacity=None, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<path d="{d}" fill="{fill}"{s}{o}{extra}/>'


def fmt(v):
    if isinstance(v, float):
        v = round(v, 2)
        if v == int(v):
            v = int(v)
    return str(v)


def rounded_top(x, y, w, h, r):
    return (f"M{fmt(x)} {fmt(y + h)}V{fmt(y + r)}a{r} {r} 0 0 1 {r} -{r}H{fmt(x + w - r)}a{r} {r} 0 0 1 {r} {r}"
            f"V{fmt(y + h)}Z")


# ---------------------------------------------------------------- text
def text(x, y, s, style="body", fill="#FFFFFF", anchor="start", weight=None, size=None, italic=False,
         opacity=None, ls=None, upper=False, tnum=False, fam=None, extra=""):
    spec = tk.T[style]
    fam = fam or spec["family"]
    size = size or spec["size"]
    weight = weight or spec["weight"]
    ls = spec["ls"] if ls is None else ls
    cls = "disp" if fam == "display" else "sans"
    if tnum:
        cls += " tnum"
    if upper:
        s = str(s).upper()
    it = ' font-style="italic"' if italic else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    lsa = f' letter-spacing="{round(ls * size, 2)}"' if ls else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (f'<text x="{fmt(x)}" y="{fmt(y)}" class="{cls}" font-size="{fmt(size)}" font-weight="{weight}"'
            f'{lsa}{it}{a} fill="{fill}"{o}{extra}>{esc(s)}</text>')


def tw(s, style="body", size=None, weight=None, upper=False, fam=None, italic=False):
    spec = tk.T[style]
    fam = fam or spec["family"]
    if fam == "display" and italic:
        fam = "display-italic"
    size = size or spec["size"]
    weight = weight or spec["weight"]
    if upper:
        s = str(s).upper()
    return measure(s, size, weight, fam, spec["ls"])


def wrap(s, width, style="body", size=None, weight=None, fam=None, italic=False):
    words = str(s).split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(trial, style, size, weight, fam=fam, italic=italic) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, width, style="body", fill="#FFFFFF", size=None, weight=None, lh=None, max_lines=None,
         anchor="start", italic=False, fam=None, opacity=None):
    """Wrapped multi-line text; returns (svg, height)."""
    spec = tk.T[style]
    size = size or spec["size"]
    lh = lh or spec["lh"]
    lines = wrap(s, width, style, size, weight, fam, italic)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while tw(last + "…", style, size, weight, fam=fam, italic=italic) > width and " " in last:
            last = last.rsplit(" ", 1)[0]
        lines[-1] = last + "…"
    out = []
    for i, ln in enumerate(lines):
        out.append(text(x, y + i * size * lh, ln, style, fill, anchor, weight, size, italic, opacity, fam=fam))
    return "".join(out), len(lines) * size * lh


def meta(x, y, parts, fill, style="metadata", sep=" · ", anchor="start", weight=None):
    return text(x, y, sep.join(p for p in parts if p), style, fill, anchor, weight=weight, tnum=True)


# ---------------------------------------------------------------- gradients
def lin_grad(stops, x1=0, y1=0, x2=0, y2=1, gid=None):
    gid = gid or Svg.uid("g")
    st = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                 for o, c, a in [(s + (None,))[:3] if len(s) == 2 else s for s in stops])
    return gid, (f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient>')


def rad_grad(stops, cx=.5, cy=.5, r=.5, gid=None):
    gid = gid or Svg.uid("r")
    st = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                 for o, c, a in [(s + (None,))[:3] if len(s) == 2 else s for s in stops])
    return gid, f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">{st}</radialGradient>'


def scrim_bottom(svg, x, y, w, h, start=.4, strength=.85, r=0, clip=None):
    gid, g = lin_grad([(0, "#000", 0), (start, "#000", .0), (min(1, start + .25), "#000", .35), (1, "#000", strength)])
    svg.define(g)
    c = f' clip-path="url(#{clip})"' if clip else ""
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{r}" fill="url(#{gid})"{c}/>'


def scrim_top(svg, x, y, w, h, strength=.55, r=0):
    gid, g = lin_grad([(0, "#000", strength), (1, "#000", 0)])
    svg.define(g)
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{r}" fill="url(#{gid})"/>'


def clip_round(svg, x, y, w, h, r):
    cid = Svg.uid("c")
    svg.define(f'<clipPath id="{cid}"><rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{r}"/></clipPath>')
    return cid


def clip_path_d(svg, d):
    cid = Svg.uid("c")
    svg.define(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
    return cid


# ---------------------------------------------------------------- icons
def _gear():
    pts = []
    n = 8
    for i in range(n * 4):
        a = (i / (n * 4)) * 2 * math.pi - math.pi / 2
        rr = 8.6 if (i % 4) in (0, 1) else 6.6
        pts.append((12 + rr * math.cos(a), 12 + rr * math.sin(a)))
    return "M" + "L".join(f"{p[0]:.2f} {p[1]:.2f}" for p in pts) + "Z"


ICONS = {
    "home": ["M3.5 10.5 12 3.8l8.5 6.7V19a1.5 1.5 0 0 1-1.5 1.5h-4.5v-6h-5v6H5A1.5 1.5 0 0 1 3.5 19z"],
    "search": ["M17 10.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z", "M15.3 15.3 20.5 20.5"],
    "back": ["M19.5 12h-15", "M10.5 6l-6 6 6 6"],
    "forward": ["M4.5 12h15", "M13.5 6l6 6-6 6"],
    "menu": ["M4 7h16", "M4 12h16", "M4 17h16"],
    "close": ["M6 6l12 12", "M18 6 6 18"],
    "more": [("dot", 6, 12), ("dot", 12, 12), ("dot", 18, 12)],
    "share": ["M12 15V3.8", "M7.5 8.3 12 3.8l4.5 4.5", "M5 12.5V19a1.5 1.5 0 0 0 1.5 1.5h11A1.5 1.5 0 0 0 19 19v-6.5"],
    "like": ["M12 20.2s-7.8-4.7-7.8-10.3A4.4 4.4 0 0 1 12 7.2a4.4 4.4 0 0 1 7.8 2.7c0 5.6-7.8 10.3-7.8 10.3z"],
    "bookmark": ["M7 3.5h10a1.5 1.5 0 0 1 1.5 1.5v15.5L12 16l-6.5 4.5V5A1.5 1.5 0 0 1 7 3.5z"],
    "play": ["M7.5 5v14a.9.9 0 0 0 1.4.8l10.8-7a.9.9 0 0 0 0-1.6L8.9 4.2A.9.9 0 0 0 7.5 5z"],
    "pause": ["M8.5 4.5v15", "M15.5 4.5v15"],
    "arrow": ["M7 17 17 7", "M8.5 7H17v8.5"],
    "chevron": ["M9.5 5.5 16 12l-6.5 6.5"],
    "chevron-down": ["M5.5 9.5 12 16l6.5-6.5"],
    "profile": ["M16 8a4 4 0 1 1-8 0 4 4 0 0 1 8 0z", "M4.5 20.5c.8-3.9 3.9-6 7.5-6s6.7 2.1 7.5 6"],
    "settings": [_gear(), "M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"],
    "notification": ["M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15z", "M10 20.5a2.2 2.2 0 0 0 4 0"],
    "location": ["M12 21s-6.5-5.8-6.5-11a6.5 6.5 0 0 1 13 0c0 5.2-6.5 11-6.5 11z", "M14.3 10a2.3 2.3 0 1 1-4.6 0 2.3 2.3 0 0 1 4.6 0z"],
    "calendar": ["M5.5 5h13a2 2 0 0 1 2 2v11.5a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z", "M3.5 10h17", "M8 3v4", "M16 3v4"],
    "shopping": ["M5.5 7.5h13l-.9 11.6a1.5 1.5 0 0 1-1.5 1.4H7.9a1.5 1.5 0 0 1-1.5-1.4z", "M9 10V6.5a3 3 0 0 1 6 0V10"],
    "entertainment": ["M6.5 4.5h11a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-11a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3z", "M10.2 9.2v5.6l4.6-2.8z"],
    "news": ["M5 4.5h10a1.5 1.5 0 0 1 1.5 1.5v14.5H6A2.5 2.5 0 0 1 3.5 18V6A1.5 1.5 0 0 1 5 4.5z",
             "M16.5 9h3a1 1 0 0 1 1 1v8a2.5 2.5 0 0 1-5 0", "M7 8.5h6", "M7 12h6", "M7 15.5h4"],
    "trending": ["M3.5 17 9.5 11l4 4 7-7.5", "M15 7.5h5.5V13"],
    "personalization": ["M11 3.5c.6 4.3 2.2 5.9 6.5 6.5-4.3.6-5.9 2.2-6.5 6.5-.6-4.3-2.2-5.9-6.5-6.5 4.3-.6 5.9-2.2 6.5-6.5z",
                        "M18.5 15.5c.2 1.3.7 1.8 2 2-1.3.2-1.8.7-2 2-.2-1.3-.7-1.8-2-2 1.3-.2 1.8-.7 2-2z"],
    "plane": ["M12 2.8c.9 0 1.5.9 1.5 2v5.1l7 4.1v2l-7-2.1v4.1l2.2 1.6v1.6L12 20.3l-3.7.9v-1.6l2.2-1.6v-4.1l-7 2.1v-2l7-4.1V4.8c0-1.1.6-2 1.5-2z"],
    "hotel": ["M3.5 19.5v-13", "M3.5 15.5h17v4", "M20.5 15.5v-3a2.5 2.5 0 0 0-2.5-2.5h-7.5v5.5", "M8.8 11.8a1.8 1.8 0 1 1-3.6 0 1.8 1.8 0 0 1 3.6 0z"],
    "passport": ["M7 3h10a1.5 1.5 0 0 1 1.5 1.5v15A1.5 1.5 0 0 1 17 21H7a1.5 1.5 0 0 1-1.5-1.5v-15A1.5 1.5 0 0 1 7 3z",
                 "M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0z", "M9.5 16.5h5"],
    "baggage": ["M7 7.5h10a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2z", "M9.5 7.5V5a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v2.5", "M9.5 11.5v5", "M14.5 11.5v5"],
    "meal": ["M7 3.5v17", "M4.8 3.5v4.8a2.2 2.2 0 0 0 4.4 0V3.5", "M16.5 20.5v-17c-2 1-3 3.2-3 6v4.5h3"],
    "shield-check": ["M12 3 19.5 6v5.5c0 4.6-3.2 8.2-7.5 9.5-4.3-1.3-7.5-4.9-7.5-9.5V6z", "M8.8 12.2l2.3 2.3 4.3-4.6"],
    "clock": ["M20.5 12a8.5 8.5 0 1 1-17 0 8.5 8.5 0 0 1 17 0z", "M12 7.5V12l3 2"],
    "info": ["M20.5 12a8.5 8.5 0 1 1-17 0 8.5 8.5 0 0 1 17 0z", "M12 11v5.5", ("dot", 12, 7.9)],
    "alert": ["M12 3.8 21 19.5H3z", "M12 10v4.5", ("dot", 12, 17)],
    "filter": ["M4 7h8.5", "M17.5 7H20", "M4 17h2.5", "M11.5 17H20", "M17 7a2 2 0 1 1-4 0 2 2 0 0 1 4 0z", "M11 17a2 2 0 1 1-4 0 2 2 0 0 1 4 0z"],
    "tag": ["M3.5 12.2V4.5a1 1 0 0 1 1-1h7.7l8.3 8.3a1.4 1.4 0 0 1 0 2l-6.7 6.7a1.4 1.4 0 0 1-2 0z", ("dot", 8, 8)],
    "globe": ["M20.5 12a8.5 8.5 0 1 1-17 0 8.5 8.5 0 0 1 17 0z", "M3.5 12h17", "M12 3.5c2.3 2.4 3.5 5.2 3.5 8.5s-1.2 6.1-3.5 8.5c-2.3-2.4-3.5-5.2-3.5-8.5s1.2-6.1 3.5-8.5z"],
    "weather": ["M15.8 12a3.8 3.8 0 1 1-7.6 0 3.8 3.8 0 0 1 7.6 0z", "M12 3.5v1.8", "M12 18.7v1.8", "M3.5 12h1.8", "M18.7 12h1.8",
                "M6 6l1.3 1.3", "M16.7 16.7 18 18", "M6 18l1.3-1.3", "M16.7 7.3 18 6"],
    "mic": ["M12 3.5a3 3 0 0 1 3 3v5a3 3 0 0 1-6 0v-5a3 3 0 0 1 3-3z", "M5.5 11.5a6.5 6.5 0 0 0 13 0", "M12 18v2.5"],
    "camera": ["M4.5 7.5h3l1.5-2h6l1.5 2h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1h-15a1 1 0 0 1-1-1v-10a1 1 0 0 1 1-1z",
               "M15.5 13a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0z"],
    "check": ["M5 12.5 10 17.5 19.5 7"],
    "plus": ["M12 5v14", "M5 12h14"],
    "grid": ["M4.5 4.5h6v6h-6z", "M13.5 4.5h6v6h-6z", "M4.5 13.5h6v6h-6z", "M13.5 13.5h6v6h-6z"],
    "lock": ["M7 10.5h10a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2z", "M8 10.5V8a4 4 0 0 1 8 0v2.5"],
    "refresh": ["M19.5 12a7.5 7.5 0 1 1-2.2-5.3", "M19.5 4.5v4h-4"],
    "external": ["M13.5 4.5h6v6", "M19.5 4.5l-8 8", "M17.5 13.5v5a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1v-11a1 1 0 0 1 1-1h5"],
    "compare": ["M7 4.5 3.5 8 7 11.5", "M3.5 8h13", "M17 12.5l3.5 3.5-3.5 3.5", "M20.5 16h-13"],
    "star": ["M12 3.8l2.5 5.2 5.7.8-4.1 4 1 5.7L12 16.8l-5.1 2.7 1-5.7-4.1-4 5.7-.8z"],
    "chat": ["M4.5 6.5a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-6.5l-4.5 3.5v-3.5h0a2 2 0 0 1-2-2z"],
    "live": [("dot", 12, 12, 2.2), "M8 8a5.7 5.7 0 0 0 0 8", "M16 8a5.7 5.7 0 0 1 0 8", "M5.2 5.2a9.6 9.6 0 0 0 0 13.6", "M18.8 5.2a9.6 9.6 0 0 1 0 13.6"],
}

ICON_GROUPS = {
    "Navigation": ["home", "search", "back", "forward", "menu", "close", "more", "chevron", "chevron-down", "arrow", "external"],
    "Actions": ["share", "like", "bookmark", "play", "pause", "plus", "check", "filter", "refresh", "compare", "mic", "camera"],
    "Content": ["entertainment", "news", "trending", "personalization", "shopping", "tag", "star", "chat", "live", "weather"],
    "System": ["profile", "settings", "notification", "location", "calendar", "clock", "info", "alert", "lock", "grid", "globe"],
    "Travel (case)": ["plane", "hotel", "passport", "baggage", "meal", "shield-check"],
}
ICON_STROKE = 1.75


def icon(name, x, y, size=24, color="#FFFFFF", sw=ICON_STROKE, fill_color=None):
    """Draw icon on its 24 grid, scaled to size; stroke width compensated so optical weight holds."""
    s = size / 24
    parts = []
    for p in ICONS[name]:
        if isinstance(p, tuple):
            r = p[3] if len(p) > 3 else 1.6
            parts.append(f'<circle cx="{p[1]}" cy="{p[2]}" r="{r}" fill="{color}"/>')
        else:
            parts.append(f'<path d="{p}"/>')
    f = fill_color or "none"
    return (f'<g transform="translate({fmt(x)} {fmt(y)}) scale({round(s, 4)})" fill="{f}" stroke="{color}" '
            f'stroke-width="{round(sw / s, 3)}" stroke-linecap="round" stroke-linejoin="round" '
            f'data-icon="{name}">' + "".join(parts) + "</g>")


def icon_file(name, color="currentColor"):
    parts = []
    for p in ICONS[name]:
        if isinstance(p, tuple):
            r = p[3] if len(p) > 3 else 1.6
            parts.append(f'  <circle cx="{p[1]}" cy="{p[2]}" r="{r}" fill="{color}" stroke="none"/>')
        else:
            parts.append(f'  <path d="{p}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{ICON_STROKE}" stroke-linecap="round" stroke-linejoin="round" '
            f'role="img" aria-label="{name}">\n  <title>{name}</title>\n' + "\n".join(parts) + "\n</svg>\n")


# ---------------------------------------------------------------- placeholder media (original art)
SCENES = ["dusk", "lagoon", "city", "mountain", "studio", "studio-iris", "food", "stadium", "concert", "plane",
          "hotel", "desert", "sneaker", "bag", "lamp", "watch", "iris", "news", "beach-city", "temple"]


def media(svg, x, y, w, h, scene="dusk", r=0, seed=None, label=None):
    """Original placeholder imagery drawn from simple shapes. Returns an svg group clipped to the frame."""
    rnd = random.Random(seed if seed is not None else hash(scene) % 1000)
    cid = clip_round(svg, x, y, w, h, r)
    g = []

    def lg(stops, x1=0, y1=0, x2=0, y2=1):
        gid, d = lin_grad(stops, x1, y1, x2, y2)
        svg.define(d)
        return f"url(#{gid})"

    def rg(stops, cx=.5, cy=.5, rr=.5):
        gid, d = rad_grad(stops, cx, cy, rr)
        svg.define(d)
        return f"url(#{gid})"

    X = lambda f: x + f * w
    Y = lambda f: y + f * h

    if scene == "dusk":
        g.append(rect(x, y, w, h, lg([(0, "#1A0B2E"), (.45, "#6A1C5C"), (.75, "#FF4D6D"), (1, "#FFB38A")])))
        g.append(circle(X(.62), Y(.62), min(w, h) * .16, "#FFD9B0", opacity=.95))
        g.append(path(f"M{x} {Y(.72)} Q{X(.25)} {Y(.62)} {X(.5)} {Y(.72)} T{X(1)} {Y(.7)} V{y + h} H{x}Z", "#2A0E2E"))
        g.append(path(f"M{x} {Y(.82)} Q{X(.3)} {Y(.76)} {X(.6)} {Y(.84)} T{X(1)} {Y(.8)} V{y + h} H{x}Z", "#12060F"))
    elif scene == "lagoon":
        g.append(rect(x, y, w, h, lg([(0, "#9FD8F0"), (.5, "#57B8D6"), (.52, "#1E8FA8"), (1, "#0B4F66")])))
        g.append(circle(X(.8), Y(.18), min(w, h) * .07, "#FFF6DA", opacity=.9))
        g.append(path(f"M{x} {Y(.78)} Q{X(.5)} {Y(.72)} {X(1)} {Y(.8)} V{y + h} H{x}Z", "#EBD2A6"))
        # palm
        px, py = X(.22), Y(.8)
        g.append(path(f"M{px} {py} Q{px + w * .03} {Y(.55)} {px + w * .08} {Y(.38)}", stroke="#1B2B24", sw=max(3, w * .012)))
        for a in (-60, -20, 20, 60, 110, 160):
            ra = math.radians(a)
            ex, ey = px + w * .08 + math.cos(ra) * w * .13, Y(.38) + math.sin(ra) * h * .06 + h * .02
            g.append(path(f"M{px + w * .08} {Y(.38)} Q{(px + w * .08 + ex) / 2} {Y(.33)} {ex} {ey}", stroke="#1B2B24",
                          sw=max(2, w * .01)))
        for i in range(4):
            yy = Y(.58 + i * .045)
            g.append(line(X(.35 + i * .05), yy, X(.55 + i * .06), yy, "#FFFFFF", 1.2, opacity=.35, cap="round"))
    elif scene in ("city", "beach-city"):
        top = "#07070C" if scene == "city" else "#F2A65A"
        mid = "#1D1433" if scene == "city" else "#E25B63"
        g.append(rect(x, y, w, h, lg([(0, top), (.7, mid), (1, "#2B1B3F" if scene == "city" else "#5A2A5E")])))
        if scene == "city":
            g.append(circle(X(.78), Y(.16), min(w, h) * .05, "#F4EEDC", opacity=.9))
        bx = x
        while bx < x + w:
            bw = w * rnd.uniform(.07, .14)
            bh = h * rnd.uniform(.25, .6)
            g.append(rect(bx, y + h - bh, bw - 2, bh, "#0D0A18" if scene == "city" else "#3A1838"))
            for wy in range(int((bh - 10) // 11)):
                for wx in range(int((bw - 8) // 8)):
                    if rnd.random() < .33:
                        g.append(rect(bx + 4 + wx * 8, y + h - bh + 8 + wy * 11, 3, 5, "#FFD27A",
                                      opacity=round(rnd.uniform(.4, .95), 2)))
            bx += bw
    elif scene == "mountain":
        g.append(rect(x, y, w, h, lg([(0, "#1F2F52"), (.6, "#7C94BD"), (1, "#D7E1EF")])))
        g.append(path(f"M{x} {Y(.75)} L{X(.3)} {Y(.35)} L{X(.5)} {Y(.6)} L{X(.72)} {Y(.25)} L{X(1)} {Y(.7)} V{y + h} H{x}Z", "#34466E"))
        g.append(path(f"M{X(.66)} {Y(.34)} L{X(.72)} {Y(.25)} L{X(.79)} {Y(.36)} L{X(.74)} {Y(.33)} L{X(.7)} {Y(.37)}Z", "#F2F5FA"))
        g.append(path(f"M{x} {Y(.85)} Q{X(.4)} {Y(.7)} {X(1)} {Y(.86)} V{y + h} H{x}Z", "#1C2742"))
    elif scene in ("studio", "studio-iris"):
        bgc = lg([(0, "#EAD9CC"), (1, "#C49E8C")]) if scene == "studio" else lg([(0, "#E9D8F5"), (1, "#9C7BC0")])
        coat = "#FF0049" if scene == "studio" else "#1E1A2B"
        g.append(rect(x, y, w, h, bgc))
        g.append(path(f"M{x} {Y(.8)} H{x + w} V{y + h} H{x}Z", "#000000", opacity=.08))
        cx = X(.5)
        s = min(w / .9, h)
        g.append(circle(cx, Y(.2), s * .07, "#5B3A2E"))
        g.append(rect(cx - s * .025, Y(.25), s * .05, s * .05, "#8A5A45"))
        g.append(path(f"M{cx - s * .16} {Y(.33)} Q{cx} {Y(.27)} {cx + s * .16} {Y(.33)} L{cx + s * .2} {Y(.72)} "
                      f"L{cx - s * .2} {Y(.72)}Z", coat))
        g.append(path(f"M{cx} {Y(.3)} L{cx - s * .05} {Y(.5)} L{cx} {Y(.72)}", stroke="#000000", sw=1.2, opacity=.25))
        g.append(rect(cx - s * .1, Y(.72), s * .07, Y(.95) - Y(.72), "#2A2530"))
        g.append(rect(cx + s * .03, Y(.72), s * .07, Y(.95) - Y(.72), "#2A2530"))
        g.append(circle(X(.14), Y(.14), s * .18, "#FFFFFF", opacity=.25))
    elif scene == "food":
        g.append(rect(x, y, w, h, rg([(0, "#3A2A20"), (1, "#120C08")], .5, .5, .8)))
        cx, cy, rr = X(.5), Y(.5), min(w, h) * .34
        g.append(circle(cx, cy, rr, "#F3EDE4"))
        g.append(circle(cx, cy, rr * .8, "#E0A33A"))
        for i in range(9):
            a = rnd.uniform(0, 6.28)
            d = rnd.uniform(0, rr * .55)
            g.append(circle(cx + math.cos(a) * d, cy + math.sin(a) * d, rr * rnd.uniform(.08, .16),
                            rnd.choice(["#C0392B", "#3E8E41", "#F4D35E", "#FFFFFF", "#7A3E1D"]), opacity=.95))
    elif scene == "stadium":
        g.append(rect(x, y, w, h, lg([(0, "#0B1A2E"), (.45, "#12324A"), (.46, "#1F7A3F"), (1, "#0F4F27")])))
        g.append(path(f"M{X(.1)} {y + h} L{X(.35)} {Y(.46)} H{X(.65)} L{X(.9)} {y + h}", stroke="#FFFFFF", sw=1.5, opacity=.5))
        g.append(path(f"M{X(.2)} {Y(.75)} Q{X(.5)} {Y(.65)} {X(.8)} {Y(.75)}", stroke="#FFFFFF", sw=1.5, opacity=.5))
        for i in range(5):
            g.append(circle(X(.1 + i * .2), Y(.12), min(w, h) * .025, "#FFFFFF", opacity=.9))
            g.append(path(f"M{X(.1 + i * .2)} {Y(.12)} L{X(.02 + i * .2)} {Y(.46)} H{X(.18 + i * .2)}Z", "#FFFFFF", opacity=.06))
    elif scene == "concert":
        g.append(rect(x, y, w, h, lg([(0, "#12051F"), (1, "#3B0B3F")])))
        for i, c in enumerate(["#FF0049", "#DDBEF0", "#FF7A45"]):
            sx = X(.25 + i * .25)
            g.append(path(f"M{sx} {y} L{sx - w * .22} {Y(.8)} H{sx + w * .22}Z", c, opacity=.22))
        g.append(rect(X(.2), Y(.55), w * .6, h * .04, "#000000", opacity=.5))
        bumps = "".join(f"a{w * .03} {w * .03} 0 0 1 {w * .06} 0" for _ in range(17))
        g.append(path(f"M{x} {Y(.9)} {bumps} V{y + h} H{x}Z", "#07020C"))
    elif scene == "plane":
        g.append(rect(x, y, w, h, lg([(0, "#2E5B9A"), (1, "#A9CBEE")])))
        for i in range(3):
            cy = Y(.65 + i * .1)
            g.append(path(f"M{x} {cy} Q{X(.3)} {cy - h * .05} {X(.6)} {cy} T{x + w} {cy} V{y + h} H{x}Z", "#FFFFFF", opacity=.18 + i * .1))
        s = min(w, h) / 24 * .5
        g.append(f'<g transform="translate({fmt(X(.52))} {fmt(Y(.22))}) rotate(40) scale({round(s, 3)})">'
                 f'<path d="{ICONS["plane"][0]}" fill="#FFFFFF"/></g>')
        g.append(line(X(.3), Y(.55), X(.5), Y(.33), "#FFFFFF", 2, opacity=.5, cap="round"))
    elif scene == "hotel":
        g.append(rect(x, y, w, h, lg([(0, "#E7D4BD"), (1, "#C9A983")])))
        g.append(rect(X(.58), Y(.12), w * .3, h * .36, "#1B2A4A", r=4))
        g.append(circle(X(.8), Y(.2), min(w, h) * .03, "#F6E9C8"))
        g.append(rect(X(.08), Y(.52), w * .72, h * .2, "#F7F2EA", r=6))
        g.append(rect(X(.08), Y(.42), w * .72, h * .12, "#8C5A3C", r=6))
        g.append(rect(X(.12), Y(.47), w * .18, h * .08, "#FFFFFF", r=5))
        g.append(rect(X(.34), Y(.47), w * .18, h * .08, "#FFFFFF", r=5))
        g.append(circle(X(.9), Y(.52), min(w, h) * .12, rg([(0, "#FFE7A8", .8), (1, "#FFE7A8", 0)])))
        g.append(rect(x, Y(.78), w, h * .22, "#6E4A33"))
    elif scene == "desert":
        g.append(rect(x, y, w, h, lg([(0, "#F7C98B"), (.6, "#F29E5C"), (1, "#C4623A")])))
        g.append(circle(X(.3), Y(.35), min(w, h) * .12, "#FFF1D0", opacity=.9))
        g.append(path(f"M{x} {Y(.7)} Q{X(.35)} {Y(.52)} {X(.7)} {Y(.72)} T{x + w} {Y(.65)} V{y + h} H{x}Z", "#B5532F"))
        g.append(path(f"M{x} {Y(.85)} Q{X(.5)} {Y(.72)} {x + w} {Y(.88)} V{y + h} H{x}Z", "#8A3A22"))
    elif scene == "temple":
        g.append(rect(x, y, w, h, lg([(0, "#FBD3A0"), (1, "#E9876B")])))
        cx = X(.5)
        g.append(path(f"M{cx - w * .3} {Y(.85)} V{Y(.55)} H{cx + w * .3} V{Y(.85)}Z", "#7A2E3A"))
        g.append(path(f"M{cx - w * .12} {Y(.55)} Q{cx} {Y(.2)} {cx + w * .12} {Y(.55)}Z", "#7A2E3A"))
        g.append(path(f"M{cx - w * .3} {Y(.55)} Q{cx - w * .22} {Y(.4)} {cx - w * .15} {Y(.55)}Z", "#8F3A45"))
        g.append(path(f"M{cx + w * .15} {Y(.55)} Q{cx + w * .22} {Y(.4)} {cx + w * .3} {Y(.55)}Z", "#8F3A45"))
        g.append(rect(cx - w * .05, Y(.66), w * .1, h * .19, "#3A1219", r=w * .05))
        g.append(rect(x, Y(.85), w, h * .15, "#C9765A"))
    elif scene in ("sneaker", "bag", "lamp", "watch"):
        g.append(rect(x, y, w, h, "#F1EEEA"))
        g.append(f'<ellipse cx="{fmt(X(.5))}" cy="{fmt(Y(.82))}" rx="{fmt(w * .3)}" ry="{fmt(h * .035)}" fill="#000" opacity=".12"/>')
        if scene == "sneaker":
            g.append(path(f"M{X(.18)} {Y(.74)} L{X(.18)} {Y(.54)} Q{X(.2)} {Y(.47)} {X(.29)} {Y(.49)} L{X(.35)} {Y(.52)} "
                          f"Q{X(.39)} {Y(.43)} {X(.47)} {Y(.44)} L{X(.56)} {Y(.55)} Q{X(.72)} {Y(.59)} {X(.81)} {Y(.64)} "
                          f"Q{X(.87)} {Y(.68)} {X(.85)} {Y(.74)}Z", "#FF0049"))
            g.append(path(f"M{X(.17)} {Y(.735)} H{X(.86)} Q{X(.87)} {Y(.79)} {X(.8)} {Y(.79)} H{X(.2)} Q{X(.16)} {Y(.79)} {X(.17)} {Y(.735)}Z", "#FFFFFF"))
            g.append(path(f"M{X(.22)} {Y(.62)} Q{X(.45)} {Y(.66)} {X(.6)} {Y(.6)}", stroke="#FFFFFF", sw=max(2, w * .012)))
            for i in range(3):
                g.append(line(X(.41 + i * .04), Y(.49 + i * .025), X(.45 + i * .04), Y(.535 + i * .02), "#FFFFFF", 2, cap="round"))
        elif scene == "bag":
            g.append(path(f"M{X(.4)} {Y(.36)} Q{X(.5)} {Y(.12)} {X(.6)} {Y(.36)}", stroke="#2B2230", sw=max(2, w * .018)))
            g.append(rect(X(.28), Y(.34), w * .44, h * .44, "#C79A6A", r=w * .04))
            g.append(rect(X(.28), Y(.34), w * .44, h * .08, "#B0845A", r=w * .02))
        elif scene == "lamp":
            g.append(path(f"M{X(.36)} {Y(.4)} L{X(.44)} {Y(.18)} H{X(.56)} L{X(.64)} {Y(.4)}Z", "#DDBEF0"))
            g.append(rect(X(.49), Y(.4), w * .02, h * .36, "#2B2230"))
            g.append(rect(X(.4), Y(.76), w * .2, h * .04, "#2B2230", r=3))
        else:
            g.append(rect(X(.46), Y(.12), w * .08, h * .7, "#2B2230", r=4))
            g.append(circle(X(.5), Y(.47), min(w, h) * .17, "#2B2230"))
            g.append(circle(X(.5), Y(.47), min(w, h) * .14, "#F7F4EF"))
            g.append(line(X(.5), Y(.47), X(.5), Y(.39), "#2B2230", 2, cap="round"))
            g.append(line(X(.5), Y(.47), X(.56), Y(.5), "#FF0049", 2, cap="round"))
    elif scene == "iris":
        g.append(rect(x, y, w, h, "#120E1A"))
        g.append(circle(X(.3), Y(.35), min(w, h) * .55, rg([(0, "#DDBEF0", .9), (1, "#DDBEF0", 0)])))
        g.append(circle(X(.75), Y(.7), min(w, h) * .5, rg([(0, "#FF0049", .7), (1, "#FF0049", 0)])))
        g.append(circle(X(.8), Y(.2), min(w, h) * .3, rg([(0, "#5AA9FF", .45), (1, "#5AA9FF", 0)])))
    elif scene == "news":
        g.append(rect(x, y, w, h, lg([(0, "#1D2B3A"), (1, "#3C5470")])))
        g.append(rect(X(.12), Y(.25), w * .3, h * .5, "#0F1824", opacity=.8))
        g.append(rect(X(.46), Y(.18), w * .2, h * .6, "#0F1824", opacity=.7))
        g.append(rect(X(.7), Y(.32), w * .18, h * .45, "#0F1824", opacity=.85))
        g.append(rect(x, Y(.78), w, h * .22, "#0A1119"))
        g.append(circle(X(.56), Y(.62), min(w, h) * .05, "#FF0049", opacity=.85))
    else:
        g.append(rect(x, y, w, h, "#333"))
    inner = f'<g clip-path="url(#{cid})" data-media="{scene}">' + "".join(g) + "</g>"
    return inner


# ---------------------------------------------------------------- misc
def hairline(x1, y, x2, color, sw=1, opacity=None):
    return line(x1, y, x2, y, color, sw, opacity=opacity)


def status_bar(x, y, w, color="#FFFFFF", time="9:41"):
    out = [text(x + 28, y + 30, time, "button", color, weight=600, size=15, tnum=True)]
    rx = x + w - 30
    out.append(rect(rx - 25, y + 20, 25, 12, "none", 3.5, stroke=color, sw=1, opacity=.9))
    out.append(rect(rx - 23, y + 22, 18, 8, color, 2))
    out.append(rect(rx + 1.5, y + 24, 1.5, 4, color, 1, opacity=.6))
    for i in range(4):
        out.append(rect(rx - 58 + i * 5, y + 30 - (i + 1) * 2.5, 3, (i + 1) * 2.5, color, 1))
    out.append(path(f"M{rx - 40} {y + 25} a8 8 0 0 1 11 0 M{rx - 37.5} {y + 28} a4 4 0 0 1 6 0", stroke=color, sw=1.6))
    return "".join(out)


def phone(svg, x, y, content_fn, w=390, h=844, bezel=10, radius=54, ground="#000000", label=None, label_color="#85838F"):
    """Device frame; content_fn(svg, sx, sy, sw, sh) returns svg for the screen."""
    out = []
    out.append(rect(x - bezel, y - bezel, w + 2 * bezel, h + 2 * bezel, "#1B1B20", radius + bezel,
                    stroke="#2E2E36", sw=1))
    cid = clip_round(svg, x, y, w, h, radius)
    out.append(f'<g clip-path="url(#{cid})">' + rect(x, y, w, h, ground) + content_fn(svg, x, y, w, h) + "</g>")
    out.append(rect(x + w / 2 - 62, y + 11, 124, 36, "#000000", 18))
    if label:
        out.append(text(x + w / 2, y + h + bezel + 34, label, "label", label_color, anchor="middle", upper=True))
    return group(None, *out)


def home_indicator(x, y, w, color="#FFFFFF"):
    return rect(x + w / 2 - 67, y - 13, 134, 5, color, 3)


def conf_mark(x, y, sym, color, size=10):
    """Draw a confidence mark as vector (fonts rarely carry ◐). (x, y) = left of mark, text baseline."""
    r = size / 2
    cx, cy = x + r, y - size * .38
    if sym == "●":
        return circle(cx, cy, r, color)
    if sym == "○":
        return circle(cx, cy, r - .6, "none", stroke=color, sw=1.2)
    if sym == "◐":
        return (circle(cx, cy, r - .6, "none", stroke=color, sw=1.2) +
                path(f"M{fmt(cx)} {fmt(cy - r + .6)} A{r - .6} {r - .6} 0 0 0 {fmt(cx)} {fmt(cy + r - .6)}Z", color))
    return path(f"M{fmt(cx)} {fmt(cy - r)} L{fmt(cx + r)} {fmt(cy)} L{fmt(cx)} {fmt(cy + r)} L{fmt(cx - r)} {fmt(cy)}Z", stroke=color, sw=1.2)


def conf_label(x, y, sym, label, color, style="caption", size=None):
    sz = size or tk.T[style]["size"]
    return conf_mark(x, y, sym, color, sz * .8) + text(x + sz * .8 + 6, y, label, style, color, size=size)
