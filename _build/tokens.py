"""Single source of truth for every value in the package.

Every SVG, CSS file, JSON file and the PDF read from here, so a change in one
place propagates everywhere. Confidence marks:
  OBS  = directly observed        (●)
  INF  = strong inference         (◐)
  REC  = design-system reconstruction (○)
  ORIG = original interpretation  (◇)
"""
import colorsys

OBS, INF, REC, ORIG = "●", "◐", "○", "◇"
CONF_NAME = {OBS: "Observed", INF: "Strong inference", REC: "Reconstruction", ORIG: "Original interpretation"}

SYSTEM_NAME = "Wake"
SYSTEM_TAG = "A Glance-inspired design system"
VERSION = "1.0"
DATE = "September 2026"

# ---------------------------------------------------------------- colour
# (token, dark value, light value, usage, confidence)
COLORS = [
    # brand / primary ("signal" = the hot red that means now / act)
    ("primary", "#FF0049", "#FF0049", "Brand signal. Live dots, active indicators, icons, large display accents. Never body text on light.", OBS),
    ("primary-action", "#E6003F", "#E6003F", "Filled primary button with white label (passes 4.5:1).", ORIG),
    ("primary-dark", "#B80036", "#B80036", "Pressed state of primary-action; primary text on light surfaces.", REC),
    ("primary-light", "#FF4D7D", "#FF4D7D", "Links and inline emphasis on dark surfaces.", REC),
    ("primary-subtle", "#3A0716", "#FFE8EE", "Tinted ground behind primary badges and selected chips.", REC),
    # secondary ("iris" = lavender, means AI / personalised / you)
    ("iris", "#DDBEF0", "#7B4FA6", "Personalisation and AI marks: For You labels, sparkle, 'because you…' lines.", OBS),
    ("iris-strong", "#B98BDB", "#5E3786", "Iris icons and borders; hover of iris elements.", REC),
    ("iris-subtle", "#251A2E", "#F5EDFB", "Ground of personalisation chips and AI explanation panels.", REC),
    # neutrals
    ("stage", "#000000", "#000000", "Full-bleed media stage and lock-screen ground. Same in both themes.", OBS),
    ("background", "#0C0C10", "#FFFFFF", "App background.", INF),
    ("surface", "#16161B", "#F6F5F8", "Cards and grouped content without media.", REC),
    ("surface-elevated", "#202027", "#FFFFFF", "Sheets, menus, popovers. Light theme pairs it with shadow-2.", REC),
    ("surface-muted", "#2A2A33", "#ECEBF0", "Inputs, skeletons, inactive chips.", REC),
    ("border", "#FFFFFF1F", "#E2E0E8", "Component borders (12% white on dark).", REC),
    ("divider", "#FFFFFF14", "#EEEDF2", "Hairline list separators (8% white on dark).", REC),
    ("text-primary", "#FFFFFF", "#0C0C10", "Headlines, body.", INF),
    ("text-secondary", "#B8B8C2", "#55535E", "Supporting copy, descriptions.", REC),
    ("text-tertiary", "#85838F", "#6B6975", "Metadata, timestamps, placeholders.", REC),
    ("text-on-media", "#FFFFFF", "#FFFFFF", "Any text placed on imagery, always over a scrim.", OBS),
    ("text-on-primary", "#FFFFFF", "#FFFFFF", "Label on primary-action.", REC),
    # semantic
    ("success", "#2FD08A", "#0A7F4A", "Confirmed, verified, live-fresh data.", REC),
    ("warning", "#FFB020", "#9A5B00", "Price changed, stale data, limited stock.", REC),
    ("error", "#FF6B3D", "#C2381A", "Failures. Orange-red, kept visibly apart from the brand pink-red; always with an icon.", ORIG),
    ("info", "#5AA9FF", "#1F63C7", "Neutral system information, tips.", REC),
]

# overlays / content tokens (rgba strings; theme-independent)
OVERLAYS = [
    ("scrim-bottom", "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.35) 45%, rgba(0,0,0,.85) 100%)",
     "Bottom 55% of any media card carrying text.", INF),
    ("scrim-top", "linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 100%)",
     "Top 20% of full-bleed media, under the status bar and chrome.", INF),
    ("scrim-full", "rgba(0,0,0,.48)", "Media behind modals and sheets.", REC),
    ("glass", "rgba(22,22,27,.56)", "Floating controls on media, with 20px backdrop blur.", REC),
    ("glass-light", "rgba(255,255,255,.16)", "Chips and buttons placed directly on imagery.", REC),
    ("video-control", "rgba(255,255,255,.92)", "Play/pause glyphs and progress fill on video.", REC),
    ("video-track", "rgba(255,255,255,.32)", "Progress track on video and story bars.", REC),
    ("media-ground", "#000000", "Letterbox and loading ground for media.", OBS),
    ("signal-glow", "rgba(255,0,73,.35)", "Glow under the single floating action. Nowhere else.", ORIG),
]

# ---------------------------------------------------------------- type
FONT_DISPLAY = "'Instrument Serif', 'Times New Roman', Georgia, serif"
FONT_SANS = "Inter, 'Helvetica Neue', Arial, sans-serif"
FONT_MONO = "'JetBrains Mono', 'SF Mono', Menlo, monospace"

# name: (family, weight, size, line-height, letter-spacing(em), max chars, usage, confidence, style)
TYPE = [
    ("display-xl", "display", 400, 56, 1.00, -0.01, 18, "Editorial hooks on cover media and deck titles. Desktop 72.", ORIG, "normal"),
    ("display", "display", 400, 40, 1.05, -0.005, 22, "Section openers, onboarding statements. Desktop 56.", ORIG, "normal"),
    ("headline-media", "sans", 700, 26, 1.15, -0.02, 40, "Headline laid over imagery (lock-screen hook). Two lines max.", INF, "normal"),
    ("h1", "sans", 700, 30, 1.15, -0.02, 32, "Screen titles. Desktop 40.", REC, "normal"),
    ("h2", "sans", 700, 22, 1.2, -0.015, 40, "Section headers, rail titles.", REC, "normal"),
    ("h3", "sans", 600, 17, 1.3, -0.01, 48, "Card titles.", REC, "normal"),
    ("body-l", "sans", 400, 17, 1.5, 0.0, 64, "Article body, onboarding copy.", REC, "normal"),
    ("body", "sans", 400, 15, 1.5, 0.0, 72, "Default body copy.", REC, "normal"),
    ("body-s", "sans", 400, 13, 1.45, 0.0, 72, "Descriptions inside cards.", REC, "normal"),
    ("caption", "sans", 500, 12, 1.35, 0.0, 60, "Image credits, helper text.", REC, "normal"),
    ("label", "sans", 600, 11, 1.2, 0.08, 24, "Kickers and category labels, uppercase.", INF, "normal"),
    ("button", "sans", 600, 15, 1.0, -0.005, 24, "Button and chip labels.", REC, "normal"),
    ("metadata", "sans", 500, 12, 1.3, 0.01, 48, "Source · time · price facts, tabular numerals, middle-dot separated.", ORIG, "normal"),
]

# ---------------------------------------------------------------- space
SPACE = [("space-0", 0), ("space-1", 4), ("space-2", 8), ("space-3", 12), ("space-4", 16), ("space-5", 20),
         ("space-6", 24), ("space-7", 32), ("space-8", 40), ("space-9", 48), ("space-10", 64),
         ("space-11", 80), ("space-12", 96)]
SPACE_USAGE = {
    "space-1": "icon-to-label gap, dot separators", "space-2": "chip padding-y, inline gaps",
    "space-3": "card inner gap, chip padding-x", "space-4": "screen margin (mobile), card padding",
    "space-5": "card padding (large cards)", "space-6": "gap between modules inside a section",
    "space-7": "section spacing (mobile)", "space-8": "section spacing (tablet)", "space-9": "section spacing (desktop)",
    "space-10": "hero padding (desktop)", "space-11": "page top/bottom (desktop)", "space-12": "deck and marketing sections",
}

RADIUS = [("radius-none", 0, "Full-bleed media, dividers", OBS),
          ("radius-xs", 4, "Kicker tags, progress bars", REC),
          ("radius-s", 8, "Thumbnails, small media, tooltips", REC),
          ("radius-m", 12, "Inputs, compact cards, list thumbnails", REC),
          ("radius-l", 16, "Standard content and commerce cards", INF),
          ("radius-xl", 24, "Hero cards, bottom sheets (top corners)", INF),
          ("radius-2xl", 32, "Device frames and deck panels", REC),
          ("radius-pill", 999, "Buttons, chips, badges, search field", INF)]

SHADOWS = [("shadow-0", "none", "Dark theme default: elevation comes from surface tone, not shadow.", REC),
           ("shadow-1", "0 1px 2px rgba(12,12,16,.06), 0 1px 1px rgba(12,12,16,.04)", "Resting cards on light theme.", REC),
           ("shadow-2", "0 8px 24px rgba(12,12,16,.10)", "Sheets, menus, raised cards on light theme; hover.", REC),
           ("shadow-3", "0 24px 48px rgba(12,12,16,.18)", "Modals and device mockups.", REC),
           ("shadow-signal", "0 8px 24px rgba(255,0,73,.35)", "The one floating action button only.", ORIG)]

BORDERS = [("border-hairline", "1px solid var(--color-divider)", "List separators"),
           ("border-default", "1px solid var(--color-border)", "Inputs, outlined buttons, cards without media"),
           ("border-strong", "1.5px solid var(--color-text-primary)", "Secondary button on light theme, selected option"),
           ("border-focus", "2px solid var(--color-primary)", "Focus ring, drawn with 2px offset"),
           ("border-media", "1px solid rgba(255,255,255,.08)", "Inner stroke on media so dark images hold their edge on dark ground")]

MOTION = [
    # name, duration ms, easing, behaviour, confidence
    ("button-press", 100, "standard", "Scale to .97, background to pressed token.", REC),
    ("chip-select", 160, "standard", "Fill cross-fades; check icon slides in 4px.", REC),
    ("card-hover", 240, "standard", "translateY(-2px), shadow-2 (light) or surface lift (dark); media scales 1.03.", REC),
    ("card-press", 100, "standard", "Scale to .98.", REC),
    ("like-pop", 360, "spring", "Heart scales 1 → 1.25 → 1 and fills primary.", ORIG),
    ("sheet-enter", 360, "emphasized", "Slides up from bottom, scrim fades to .48.", INF),
    ("sheet-exit", 240, "exit", "Slides down; follows the finger if dragged.", INF),
    ("modal", 240, "emphasized", "Fade + scale .96 → 1.", REC),
    ("carousel-snap", 360, "emphasized", "Snap to nearest card after release; momentum preserved.", INF),
    ("story-advance", 5000, "linear", "Progress bar fills; next story cross-fades 240ms.", INF),
    ("page-push", 360, "emphasized", "New page in from right 24px + fade; old page dims.", REC),
    ("shared-media", 360, "emphasized", "Card media expands into the detail hero (shared element).", ORIG),
    ("skeleton-shimmer", 1400, "linear", "Gradient sweep left to right, loops until data arrives.", REC),
    ("live-pulse", 1600, "standard", "Live dot ring scales 1 → 2.2, opacity .6 → 0, loops.", ORIG),
    ("toast", 240, "emphasized", "Rises 16px + fade; auto-dismiss after 4s.", REC),
]
EASING = {"standard": "cubic-bezier(.2,0,0,1)", "emphasized": "cubic-bezier(.3,0,0,1)",
          "exit": "cubic-bezier(.4,0,1,1)", "spring": "cubic-bezier(.34,1.56,.64,1)", "linear": "linear"}
DURATION = {"instant": 100, "fast": 160, "base": 240, "slow": 360, "story": 5000}

BREAKPOINTS = [("mobile", 0, 599, 4, 16, 12, "fluid"), ("tablet", 600, 1023, 8, 24, 16, "fluid"),
               ("desktop", 1024, 1439, 12, 32, 24, "1280 max"), ("wide", 1440, None, 12, 48, 24, "1360 max")]

RATIOS = [("9:16", "Full-bleed lock-screen hook, stories, vertical video", OBS),
          ("4:5", "Look cards, starring-you imagery, hero card on mobile", INF),
          ("1:1", "Product thumbnails, avatars, square posts", INF),
          ("16:9", "Video, news imagery, desktop hero", OBS),
          ("3:2", "Editorial story cards, travel destinations", REC),
          ("21:9", "Panoramic banners and deck title art", ORIG)]


# ---------------------------------------------------------------- helpers
def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def alpha_of(h):
    h = h.lstrip("#")
    return int(h[6:8], 16) / 255 if len(h) == 8 else 1.0


def rgb_str(h):
    r, g, b = hex_rgb(h)
    a = alpha_of(h)
    return f"rgb({r}, {g}, {b})" if a == 1 else f"rgba({r}, {g}, {b}, {a:.2f})"


def hsl_str(h):
    r, g, b = [c / 255 for c in hex_rgb(h)]
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    a = alpha_of(h)
    base = f"hsl({round(hh * 360)}, {round(s * 100)}%, {round(l * 100)}%"
    return base + (")" if a == 1 else f" / {a:.2f})")


def lum(h):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = hex_rgb(h)
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def blend(fg, bg):
    """Composite an 8-digit hex over an opaque bg."""
    a = alpha_of(fg)
    fr = hex_rgb(fg)
    br = hex_rgb(bg)
    return "#" + "".join(f"{round(a * x + (1 - a) * y):02X}" for x, y in zip(fr, br))


def contrast(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + .05) / (y + .05)


def css_color(h):
    """CSS form: #RRGGBB or rgba() for 8-digit hex."""
    return h if len(h.lstrip('#')) == 6 else rgb_str(h)


C_DARK = {t: css_color(d) for t, d, l, u, c in COLORS}
C_LIGHT = {t: css_color(l) for t, d, l, u, c in COLORS}
C_DARK_HEX = {t: d for t, d, l, u, c in COLORS}
C_LIGHT_HEX = {t: l for t, d, l, u, c in COLORS}
SP = dict(SPACE)
R = {n: v for n, v, u, c in RADIUS}
T = {n: dict(family=f, weight=w, size=s, lh=lh, ls=ls, max=mx, usage=u, conf=c, style=st)
     for n, f, w, s, lh, ls, mx, u, c, st in TYPE}


def family(key):
    return FONT_DISPLAY if key == "display" else FONT_SANS


def contrast_note(token, theme):
    val = C_DARK_HEX[token] if theme == "dark" else C_LIGHT_HEX[token]
    bg = C_DARK_HEX["background"] if theme == "dark" else C_LIGHT_HEX["background"]
    if alpha_of(val) < 1:
        val = blend(val, bg)
    return contrast(val, bg)
