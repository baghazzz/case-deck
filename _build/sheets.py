"""Shared layout for documentation sheets (dark stage, editorial header, legend footer)."""
import tokens as tk
import svgkit as k
from svgkit import text, rect, line, circle, para
from components import DARK as P

CONF_KEYS = [(tk.OBS, "Observed"), (tk.INF, "Strong inference"), (tk.REC, "Reconstruction"), (tk.ORIG, "Original interpretation")]


def sheet(w, h, kick, title, desc=None, file_title=None, conf=None):
    s = k.Svg(w, h, file_title or title, desc or title, bg=P["background"])
    s.add(text(64, 84, kick, "label", P["primary"], upper=True, size=12))
    s.add(text(64, 148, title, "display", P["text-primary"], size=64))
    if desc:
        t, th = para(w - 64 - 520, 76, desc, 520, "body", P["text-secondary"])
        s.add(t)
    s.add(line(64, 184, w - 64, 184, P["divider"]))
    # footer
    s.add(line(64, h - 56, w - 64, h - 56, P["divider"]))
    s.add(text(64, h - 26, f"{tk.SYSTEM_NAME} · {tk.SYSTEM_TAG} · v{tk.VERSION}", "caption", P["text-tertiary"]))
    fx = w - 64
    for sym, name in reversed(CONF_KEYS):
        tw_ = k.tw(name, "caption") + 16
        fx -= tw_
        col = P["text-primary"] if conf == sym else P["text-tertiary"]
        s.add(k.conf_label(fx, h - 26, sym, name, col))
        fx -= 20
    return s


def conf_tag(x, y, sym, color=None):
    return k.conf_label(x, y, sym, tk.CONF_NAME[sym], color or P["text-tertiary"], size=11)


def section_label(x, y, label, color=None):
    return text(x, y, label, "label", color or P["text-tertiary"], upper=True, size=11)
