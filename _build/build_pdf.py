"""Standalone design-system PDF (landscape 1200×800 px pages), amalgamating the whole package."""
import re
import html as H
import tokens as tk
import content as ct
import svgkit as k
import build_docs as bd

ROOT = "/home/claude/out/glance-inspired-design-system"
OUTPDF = "/home/claude/out/Glance-Inspired-Design-System.pdf"
C = tk.C_DARK_HEX

CF = {tk.OBS: "obs", tk.INF: "inf", tk.REC: "rec", tk.ORIG: "orig"}


def cf(sym, label=True):
    name = tk.CONF_NAME[sym]
    return f'<span class="cf cf-{CF[sym]}" title="{name}"></span>' + (f'<span class="cfl">{name}</span>' if label else "")


def marks(s):
    for sym in CF:
        s = s.replace(sym, cf(sym, False))
    return s


def svg_dims(rel):
    head = open(f"{ROOT}/{rel}").read(800)
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
    return float(m.group(1)), float(m.group(2))


def plate(rel, width, top=196, bottom=62, left=0, right=0, cls=""):
    """Embed an SVG sheet cropped to its body (drops its own header/footer)."""
    w, h = svg_dims(rel)
    vis_w = w - left - right
    sc = width / vis_w
    hh = (h - top - bottom) * sc
    return (f'<div class="plate {cls}" style="width:{width}px;height:{hh:.0f}px">'
            f'<img src="file://{ROOT}/{rel}" style="width:{w * sc:.0f}px;margin-top:{-top * sc:.0f}px;margin-left:{-left * sc:.0f}px"></div>')


def fit(rel, max_w=1088, max_h=596, top=196, bottom=62, left=0, right=0):
    w, h = svg_dims(rel)
    vis_w, vis_h = w - left - right, h - top - bottom
    sc = min(max_w / vis_w, max_h / vis_h)
    ww = vis_w * sc
    return f'<div style="display:flex;justify-content:center">' + plate(rel, ww, top, bottom, left, right) + "</div>"


def img(rel, width, cls=""):
    return f'<img class="{cls}" src="file://{ROOT}/{rel}" style="width:{width}px;display:block">'


PAGES = []


def page(kick, title, intro, body, dark=True, cls=""):
    n = len(PAGES) + 1
    intro_html = f'<p class="intro">{intro}</p>' if intro else ""
    PAGES.append(f'''<section class="page {cls}">
  <header class="ph"><div><div class="kick">{kick}</div><h1>{title}</h1></div>{intro_html}</header>
  <div class="body">{body}</div>
  <footer class="pf"><span>Wake · A Glance-inspired design system · v1.0</span>
    <span class="legend">{cf(tk.OBS)}{cf(tk.INF)}{cf(tk.REC)}{cf(tk.ORIG)}</span><span>{n:02d}</span></footer>
</section>''')


def table(headers, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


CSS = f"""
@font-face {{ font-family: Inter; src: url(file://{ROOT}/fonts/Inter-Regular.ttf); font-weight: 400; }}
@font-face {{ font-family: Inter; src: url(file://{ROOT}/fonts/Inter-Medium.ttf); font-weight: 500; }}
@font-face {{ font-family: Inter; src: url(file://{ROOT}/fonts/Inter-SemiBold.ttf); font-weight: 600; }}
@font-face {{ font-family: Inter; src: url(file://{ROOT}/fonts/Inter-Bold.ttf); font-weight: 700; }}
@font-face {{ font-family: 'Instrument Serif'; src: url(file://{ROOT}/fonts/InstrumentSerif-Regular.ttf); }}
@font-face {{ font-family: 'Instrument Serif'; src: url(file://{ROOT}/fonts/InstrumentSerif-Italic.ttf); font-style: italic; }}
@page {{ size: 1200px 800px; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: {C['background']}; color: #fff; font-family: Inter, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 1200px; height: 800px; position: relative; overflow: hidden; page-break-after: always; background: {C['background']};
  padding: 44px 56px 0; display: flex; flex-direction: column; }}
.ph {{ display: flex; justify-content: space-between; gap: 48px; align-items: flex-start; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,.08); }}
.kick {{ font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: {C['primary']}; }}
h1 {{ font: 400 50px/1 'Instrument Serif', serif; margin: 8px 0 0; letter-spacing: -.005em; }}
.intro {{ max-width: 470px; font-size: 13px; line-height: 1.5; color: {C['text-secondary']}; margin: 4px 0 0; }}
.body {{ flex: 1; padding-top: 18px; position: relative; overflow: hidden; }}
.pf {{ height: 40px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,.08);
  font-size: 10px; color: {C['text-tertiary']}; }}
.legend {{ display: flex; gap: 14px; align-items: center; }}
.cf {{ display: inline-block; width: 9px; height: 9px; border-radius: 50%; vertical-align: -1px; margin-right: 4px; }}
.cf-obs {{ background: currentColor; }}
.cf-inf {{ border: 1.2px solid currentColor; background: linear-gradient(90deg, currentColor 50%, transparent 50%); }}
.cf-rec {{ border: 1.2px solid currentColor; }}
.cf-orig {{ border: 1.2px solid currentColor; border-radius: 1px; transform: rotate(45deg) scale(.8); }}
.cfl {{ margin-right: 2px; }}
h2 {{ font-size: 15px; font-weight: 700; margin: 0 0 8px; letter-spacing: -.01em; }}
h3 {{ font-size: 13px; font-weight: 600; margin: 0 0 4px; }}
p, li {{ font-size: 12px; line-height: 1.5; color: {C['text-secondary']}; margin: 0 0 8px; }}
.lbl {{ font-size: 10px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: {C['text-tertiary']}; margin: 0 0 8px; }}
.cols {{ display: grid; gap: 28px; }}
.c2 {{ grid-template-columns: 1fr 1fr; }} .c3 {{ grid-template-columns: repeat(3, 1fr); }} .c4 {{ grid-template-columns: repeat(4, 1fr); }}
.c5 {{ grid-template-columns: repeat(5, 1fr); }}
table {{ width: 100%; border-collapse: collapse; font-size: 10.5px; }}
th {{ text-align: left; font-weight: 600; color: {C['text-tertiary']}; font-size: 9.5px; letter-spacing: .06em; text-transform: uppercase;
  padding: 6px 8px 6px 0; border-bottom: 1px solid rgba(255,255,255,.12); }}
td {{ padding: 6px 8px 6px 0; border-bottom: 1px solid rgba(255,255,255,.06); color: {C['text-secondary']}; vertical-align: top; line-height: 1.4; }}
td:first-child {{ color: #fff; font-weight: 600; }}
code {{ font-family: 'SF Mono', Menlo, monospace; font-size: 10px; color: {C['iris']}; }}
.plate {{ overflow: hidden; border-radius: 12px; }}
.plate img {{ display: block; }}
.num {{ font: 400 34px/1 'Instrument Serif'; color: {C['primary']}; }}
.card {{ background: {C['surface']}; border-radius: 16px; padding: 16px 18px; }}
.card.iris {{ background: {C['iris-subtle']}; }}
.card.sig {{ background: #3A0716; }}
.pill {{ display: inline-block; padding: 4px 10px; border-radius: 999px; background: {C['surface-muted']}; font-size: 11px; margin: 0 4px 4px 0; color: #fff; }}
.flow {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; font-size: 12px; font-weight: 600; }}
.flow span.s {{ background: {C['surface-muted']}; border-radius: 999px; padding: 6px 12px; }}
.flow span.a {{ color: {C['text-tertiary']}; }}
.big {{ font: 400 64px/1 'Instrument Serif'; }}
.quote {{ font: italic 400 30px/1.15 'Instrument Serif'; color: #fff; border-left: 3px solid {C['primary']}; padding-left: 18px; }}
.sw {{ height: 56px; border-radius: 10px; border: 1px solid rgba(255,255,255,.1); margin-bottom: 6px; }}
.cover {{ padding: 56px 64px 0; }}
.dim {{ color: {C['text-tertiary']}; }}
"""


def build():
    # ------------------------------------------------------------ 1 cover
    rules = "".join(f'<li><b style="color:#fff">{n}.</b> {d}</li>' for n, d, ic in ct.DNA)
    PAGES.append(f'''<section class="page cover">
  <div style="display:grid;grid-template-columns:1fr 430px;gap:40px;height:100%">
   <div>
    <div class="kick">Design system · version 1 · September 2026</div>
    <div style="font:italic 400 132px/1 'Instrument Serif';margin:34px 0 0;letter-spacing:-.01em">wake<span style="color:{C['primary']}">•</span></div>
    <div style="font:400 30px/1.1 'Instrument Serif';margin-top:10px">A Glance-inspired design system</div>
    <p style="font-size:15px;max-width:560px;margin-top:18px">A working design system reverse-engineered from the public design language of Glance —
    its lock-screen immediacy, media-led layout, "starring you" personalisation and one-tap commerce — rebuilt as principles, tokens,
    components, patterns, screens and slides you can reuse for a product case study.</p>
    <div class="cols c2" style="margin-top:26px;max-width:640px;gap:14px 28px">
      <div><div class="num" style="font-size:22px">01</div><h3>Research & principles</h3><p>14 sources, every claim classified, ten principles.</p></div>
      <div><div class="num" style="font-size:22px">02</div><h3>Foundations</h3><p>Colour, type, space, grid, icons, imagery, motion.</p></div>
      <div><div class="num" style="font-size:22px">03</div><h3>Components & patterns</h3><p>Six card anatomies, modules, navigation, overlays, eight UX patterns.</p></div>
      <div><div class="num" style="font-size:22px">04</div><h3>Screens, case, code</h3><p>16 screens, a grounded travel assistant, CSS and deck assets.</p></div>
    </div>
    <p class="dim" style="font-size:10px;margin-top:22px;max-width:640px">Not affiliated with or endorsed by Glance or InMobi. The Glance name and logo are trademarks and are not used as
    design primitives; "wake" is an original placeholder wordmark. All artwork is original. Type: Inter and Instrument Serif (SIL OFL).</p>
   </div>
   <div style="position:relative">
    <img src="file://{ROOT}/09_SCREEN_TEMPLATES/lockscreen.svg" style="position:absolute;left:0;top:10px;width:300px">
    <img src="file://{ROOT}/09_SCREEN_TEMPLATES/home.svg" style="position:absolute;left:170px;top:120px;width:270px">
    <div class="card" style="position:absolute;left:0;bottom:36px;width:420px;background:rgba(22,22,27,.92)">
      <div class="lbl" style="color:{C['primary']}">Five rules</div><ol style="margin:0;padding-left:0;list-style:none">{rules}</ol></div>
   </div>
  </div>
</section>''')

    # ------------------------------------------------------------ 2 method
    srows = [(a, f'<a style="color:#fff;text-decoration:none">{b}</a>', d, e) for a, b, c_, d, e in bd.SOURCES]
    page("Research · 00", "How this was made",
         "Every characteristic is classified. Only what a public source states is marked observed; the production CSS, fonts and "
         "screenshots could not be inspected from the build environment.",
         f'''<div class="cols" style="grid-template-columns:330px 1fr">
         <div>
           <div class="lbl">Confidence notation</div>
           <p>{cf(tk.OBS)} — stated or described in a public source</p>
           <p>{cf(tk.INF)} — follows directly from observed behaviour</p>
           <p>{cf(tk.REC)} — a system value chosen to fit the observed language</p>
           <p>{cf(tk.ORIG)} — added by this system; not claimed to exist in Glance</p>
           <div class="lbl" style="margin-top:18px">Method</div>
           <p>1 · Collect public sources · 2 · Extract and classify characteristics · 3 · Validate principles against evidence ·
           4 · Reconstruct tokens around two observed hues · 5 · Generate every artefact from one token source.</p>
           <div class="lbl" style="margin-top:18px">Limits</div>
           <p>Two colour values are observed (via a brand registry). No spacing, radius, type or motion value is claimed as observed.
           Glance differs by market; the source of each observation is named.</p>
         </div>
         <div>{table(["ID", "Source", "Type", "What it established"], srows, "small")}</div></div>''')
    # shrink sources table font via inline style
    PAGES[-1] = PAGES[-1].replace('<table class="small">', '<table class="small" style="font-size:8.6px">')

    # ------------------------------------------------------------ 3 analysis
    arows = [("Surface", "Lock screen first; app, TV, brand sites", tk.OBS, "S2, S11"), ("Canvas", "Dark marketing site; black in palette", tk.INF, "S1, S3"),
             ("Brand colour", "Hot red #FF0049", tk.OBS, "S3"), ("Secondary", "Lavender #DDBEF0", tk.OBS, "S3"),
             ("Imagery", "Full-screen imagery and video formats", tk.OBS, "S11"), ("Likeness", "AI images of the user wearing products", tk.OBS, "S4–S7"),
             ("Copy", "Two-verb brand line; short CTAs", tk.OBS, "S1"), ("Framing", "'A fashion magazine where you are the model'", tk.OBS, "S4"),
             ("Interaction", "One tap from lock screen to content or product", tk.OBS, "S5, S11"), ("Navigation", "Topic tabs from For You; horizontal swipe", tk.OBS, "S13"),
             ("Personalisation", "Saves, dwell, weather, trends, occasions, time", tk.OBS, "S8, S14"), ("Utility", "Weather, steps, scores widgets", tk.OBS, "S10, S12"),
             ("Trust", "Reviews complain about forced installs, re-enable prompts", tk.OBS, "S9, S12"),
             ("Type, radius, spacing, motion", "Not identifiable from sources", tk.REC, "—")]
    page("Research · 00", "Design language analysis",
         "Glance is a wake-first product. Everything follows from the two seconds after a screen lights up.",
         f'''<div class="cols" style="grid-template-columns:1fr 400px">
         <div>{table(["Characteristic", "Finding", "Class", "Source"], [(a, b, cf(c_), d) for a, b, c_, d in arows])}</div>
         <div>
          <div class="card" style="margin-bottom:14px"><div class="lbl">Different from utility-first apps</div>
           <p><b style="color:#fff">The first screen is not the app.</b> Content arrives on a screen nobody opened on purpose, so value must be instant and dismissal cheap.</p>
           <p><b style="color:#fff">Browsing is the job.</b> Discovery is the product, not the path to it.</p>
           <p><b style="color:#fff">The user is the model.</b> Personalisation shows up in the image, not only in the ranking.</p>
           <p style="margin:0"><b style="color:#fff">Commerce is one tap from inspiration.</b></p></div>
          <div class="card iris"><div class="lbl" style="color:{C['iris']}">Where this system adds something {cf(tk.ORIG, False)}</div>
           <p>Public reviews show frustration with control. The system adds visible reasons ("Why this"), editable inferred interests, a delete
           control for likeness, "Sponsored" badges, and freshness stamps on any volatile fact.</p></div>
         </div></div>''')

    # ------------------------------------------------------------ 4-5 principles
    for part, rng in ((1, range(0, 5)), (2, range(5, 10))):
        cards = ""
        for i in rng:
            n, one, why, looks, inter, do, dont, ex, conf, ev = ct.PRINCIPLES[i]
            cards += f'''<div class="card" style="padding:14px 16px"><div style="display:flex;justify-content:space-between;align-items:baseline">
              <span class="num">{i + 1:02d}</span><span style="font-size:10px;color:{C['text-tertiary']}">{cf(conf)}</span></div>
              <h2 style="margin-top:8px;font-size:14px">{n}</h2><p style="color:#fff;font-size:11.5px">{one}</p>
              <p style="font-size:10.5px"><b style="color:{C['text-primary']}">Why</b> {why}</p>
              <p style="font-size:10.5px"><b style="color:{C['success']}">Do</b> {do}</p>
              <p style="font-size:10.5px"><b style="color:{C['error']}">Don't</b> {dont}</p>
              <p style="font-size:10px;color:{C['text-tertiary']};margin:0">e.g. {ex}</p></div>'''
        page("Principles · 01", f"Design principles · {part} of 2",
             "Ten principles validated against the source log. Each has a reason, a behaviour, a do, a don't, and a confidence mark."
             if part == 1 else "Principles six to ten. Nine and ten are original: they are what the observed language needs to be trustworthy.",
             f'<div class="cols c5" style="gap:12px">{cards}</div>')

    # ------------------------------------------------------------ colour
    tone = [("primary", "Signal", "Action · live"), ("primary-action", "Signal action", "Buttons · 4.73:1"), ("iris", "Iris", "You · AI · why"),
            ("background", "Background", "The stage"), ("surface", "Surface", "Cards"), ("success", "Fresh", "Live · verified"),
            ("warning", "Changed", "Cached · moved"), ("error", "Error", "With an icon")]
    sw = "".join(f'<div><div class="sw" style="background:{C[t]}"></div><h3>{n}</h3><p class="dim" style="font-size:10px">{C[t]} · {u}</p></div>' for t, n, u in tone)
    page("Foundations · 02", "Colour",
         "Red means now. Lavender means you. #FF0049 and #DDBEF0 are observed via a brand registry; every other value is a reconstructed approximation, not an official Glance value.",
         f'''<div class="cols" style="grid-template-columns:1fr 330px">{plate("04_COLORS/palette.svg", 720, bottom=250)}
         <div><div class="cols c2" style="gap:10px 12px">{sw}</div>
         <div class="lbl" style="margin-top:12px">Contrast checks</div>
         {table(["Pair", "Ratio"], [("White on signal action", f"{tk.contrast('#FFFFFF', '#E6003F'):.2f} AA"), ("White on signal", f"{tk.contrast('#FFFFFF', '#FF0049'):.2f} large only"),
                                    ("Signal on background", f"{tk.contrast('#FF0049', '#0C0C10'):.2f} AA"), ("Tertiary on surface", f"{tk.contrast('#85838F', '#16161B'):.2f} AA"),
                                    ("Iris on iris subtle", f"{tk.contrast('#DDBEF0', '#251A2E'):.2f} AAA")])}</div></div>''')

    page("Foundations · 02", "Two themes, one set of roles",
         "Dark is the default because media looks best on it. Light mirrors every role; stage, scrims and text-on-media stay the same.",
         f'<div class="cols c2" style="gap:20px">{fit("04_COLORS/dark-theme.svg", 532, 596, top=226, bottom=50, left=880, right=50)}{fit("04_COLORS/light-theme.svg", 532, 596, top=226, bottom=50, left=880, right=50)}</div>')

    # ------------------------------------------------------------ type
    page("Foundations · 03", "Typography",
         "Instrument Serif for the editorial hook, once per screen. Inter for everything read fast, with tabular numerals for prices. The production face could not be identified; both are open-licence stand-ins.",
         f'''<div class="cols" style="grid-template-columns:1fr 300px">{plate("03_TYPOGRAPHY/type-scale.svg", 760, bottom=330)}
         <div><div class="card" style="margin-bottom:12px"><div style="font:400 60px/1 'Instrument Serif'">Aa</div><h3 style="margin-top:6px">Instrument Serif {cf(tk.ORIG, False)}</h3>
         <p style="margin:0">The magazine moment. Display 56 / 40.</p></div>
         <div class="card"><div style="font:700 60px/1 Inter">Aa</div><h3 style="margin-top:6px">Inter {cf(tk.REC, False)}</h3><p style="margin:0">UI, body, numbers, labels.</p></div>
         <div class="lbl" style="margin-top:14px">Rules</div>
         <p>One serif moment per screen · numbers always Inter, tabular · caps only for labels (+8%) · on media: two lines max, over the scrim.</p></div></div>''')
    page("Foundations · 03", "Type in context", "How the scale behaves on a hook, an editorial card and an article.",
         plate("03_TYPOGRAPHY/typography-samples.svg", 1088, bottom=62))

    # ------------------------------------------------------------ space etc.
    sp_rows = "".join(f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:5px"><span style="width:62px;font-size:10.5px;font-weight:600">{n}</span>'
                      f'<span style="width:34px;font-size:10px" class="dim">{v}px</span><span style="height:10px;width:{v * 2}px;background:{C["primary"]};border-radius:2px"></span></div>'
                      for n, v in tk.SPACE[1:])
    radii = "".join(f'<div style="text-align:center"><div style="width:52px;height:52px;border:1.5px solid #fff;border-radius:{min(v, 26)}px;margin:0 auto 6px"></div>'
                    f'<div style="font-size:10px;font-weight:600">{v if v != 999 else "pill"}</div><div class="dim" style="font-size:9px">{n[7:]}</div></div>' for n, v, u, c_ in tk.RADIUS)
    page("Foundations · 04", "Space, shape, elevation",
         "A 4px base with an 8px rhythm. Radii by role. On dark, elevation is a change of tone; shadows appear only on the light theme.",
         f'''<div class="cols c3">
         <div><div class="lbl">Space</div>{sp_rows}<p style="margin-top:10px">Margins 16 / 24 / 32 · gutters 12 / 16 / 24 · sections 32 / 40 / 48.</p></div>
         <div><div class="lbl">Shape</div><div class="cols c4" style="gap:14px 8px">{radii}</div>
           <p style="margin-top:14px">Pill for anything tapped · 16 cards · 24 heroes and sheets · 0 full-bleed.</p>
           <div class="lbl" style="margin-top:14px">Borders</div>{table(["Token", "Use"], [(f"<code>{n}</code>", u) for n, v, u in tk.BORDERS])}</div>
         <div><div class="lbl">Elevation</div>
           <div style="display:flex;gap:10px;margin-bottom:12px">{"".join(f'<div style="flex:1;height:56px;border-radius:12px;background:{C[t]};border:1px solid rgba(255,255,255,.08)"></div>' for t in ["background", "surface", "surface-elevated", "surface-muted"])}</div>
           <p>Dark: background → surface → elevated → muted.</p>
           <div style="background:#F6F5F8;border-radius:12px;padding:16px;display:flex;gap:12px">{"".join(f'<div style="flex:1;height:48px;border-radius:10px;background:#fff;box-shadow:{v if v != "none" else "none"}"></div>' for n, v, u, c_ in tk.SHADOWS[:4])}</div>
           <p style="margin-top:8px">Light: shadow-0 to shadow-3. <code>shadow-signal</code> is reserved for the one floating action.</p></div></div>''')

    page("Foundations · 04", "Grid and responsive layouts",
         "Four, eight and twelve columns. The hierarchy never changes between sizes; only how many things sit side by side.",
         f'<div class="cols" style="grid-template-columns:520px 1fr;gap:20px">{plate("05_GRID_AND_LAYOUT/grid.svg", 520, bottom=62)}{plate("05_GRID_AND_LAYOUT/responsive-layouts.svg", 540, bottom=62)}</div>')

    # ------------------------------------------------------------ icons + imagery
    page("Foundations · 05", "Iconography", "Fifty original icons on a 24 grid, 1.75px stroke, round caps and joins. Outline by default; fill only for active states.",
         plate("06_ICONS/icon-sheet.svg", 1088, bottom=62 + 150))
    decos = ["decorative/live-signal.svg", "decorative/iris-sparkle.svg", "decorative/mask-arch.svg", "decorative/mask-ticket.svg", "decorative/signal-blob.svg", "patterns/contours.svg"]
    dh = "".join(f'<div class="card" style="padding:8px;display:grid;place-items:center;height:110px"><img src="file://{ROOT}/11_SVG_ASSETS/{d}" style="max-height:94px;max-width:100%"></div>' for d in decos)
    page("Foundations · 06", "Imagery and decoration",
         "Imagery is the layout. Ratios are chosen by job, crops keep the focal point high, and every overlaid word has a scrim. Decoration is rare and always means something.",
         f'''{plate("11_SVG_ASSETS/illustrations/_image-system.svg", 1088, bottom=62)}''')
    page("Foundations · 06", "Decorative grammar",
         "Live pulse, iris sparkle, masks, one soft blob, contour lines. One decorative device per composition. Placeholder scenes are original and should be replaced with licensed photography.",
         f'''<div class="cols c3" style="gap:12px;margin-bottom:16px">{dh}</div>
         <div class="cols c5" style="gap:10px">{"".join(f'<img src="file://{ROOT}/11_SVG_ASSETS/illustrations/{sc}.svg" style="width:100%;border-radius:12px">' for sc in ["dusk", "lagoon", "studio", "concert", "hotel"])}</div>''')

    # ------------------------------------------------------------ motion
    page("Foundations · 07", "Motion",
         "Fast in, quick out; media leads and chrome follows; only the like springs. All values are inferred or reconstructed; production timing is not public.",
         fit("10_MOTION/transitions.svg"))
    page("Foundations · 07", "Motion specification", "Every interaction, its duration, curve and behaviour. Under reduced motion: transforms off, 160ms fades, stories paused, no pulse.",
         table(["Interaction", "Duration", "Easing", "Behaviour", "Class"], [(n, f"{d}ms", f"{e} <code>{tk.EASING[e]}</code>", b_, cf(c_)) for n, d, e, b_, c_ in tk.MOTION]))

    # ------------------------------------------------------------ components
    page("Components · 08", "Buttons", "One primary per view. Primary is the signal; secondary is the theme inverse; tertiary is an outline. On imagery, glass.",
         plate("07_COMPONENTS/buttons/buttons.svg", 1088, bottom=62))
    page("Components · 08", "Chips and badges", "Chips filter and steer; selected is the theme inverse and iris marks inferred facets. Badges state facts: live, new, for you, verified, sponsored.",
         fit("07_COMPONENTS/chips/chips.svg", 1088, 330) + '<div style="height:14px"></div>' + fit("07_COMPONENTS/badges/badges.svg", 1088, 250))
    page("Components · 08", "Inputs", "Search is always a pill and its last suggestion hands off to the assistant. Fields are quieter: label above, helper below, errors with an icon.",
         fit("07_COMPONENTS/inputs/inputs.svg"))
    page("Components · 08", "Tabs", "Topic tabs start at For you and change content in place. Segmented controls switch between views of the same set.",
         fit("07_COMPONENTS/tabs/tabs.svg"))
    page("Components · 08", "Navigation", "Thin chrome so content can be big. The assistant sits in the centre of the bottom bar, in iris; red stays for the in-context action.",
         fit("07_COMPONENTS/navigation/navigation.svg"))
    page("Components · 08", "Carousels", "Rails show breadth without height, peek at 40% and never auto-scroll. Stories auto-advance and pause on press.",
         fit("07_COMPONENTS/carousels/carousels.svg"))
    page("Components · 08", "Content modules", "Each module has one job: hook, explain why, rank, or group. Personalised modules name their signal in one iris line.",
         fit("07_COMPONENTS/content-modules/content-modules.svg"))
    page("Components · 08", "Media modules", "Video, stories, shoppable looks and galleries each have one control model. Text on media always sits on a scrim.",
         fit("07_COMPONENTS/media-modules/media-modules.svg"))
    page("Components · 08", "Overlays", "Sheets for choices, dialogs for consequences, toasts for confirmations, tooltips for explanations.",
         fit("07_COMPONENTS/overlays/overlays.svg"))

    # ------------------------------------------------------------ cards
    page("Cards · 09", "Six anatomies, ten card types",
         "Media takes 60–100% of every card. Text never exceeds three lines. Only the hero carries a button; every other card is its own tap target.",
         f'''<div class="cols" style="grid-template-columns:1fr 330px">{plate("07_COMPONENTS/cards/card-catalogue.svg", 740, bottom=62)}
         <div>{table(["Card", "Job"], [("A · Hero", "The one thing that matters now"), ("B · Standard", "Default feed unit"), ("C · Compact", "Lists, trending, results"),
                                      ("D · Commerce", "Anything purchasable, with freshness"), ("E · Recommendation", "Anything personalised, with its reason"), ("F · Editorial", "Long reads; serif headline")])}
         <div class="lbl" style="margin-top:14px">Card rules</div>
         <p>Ratios 4:5 people/products · 3:2 places · 16:9 video/news · 3:4 recommendations. Radius 24 / 16 / 12 / 0. One A and at most one F per screen.
         Hierarchy A &gt; F &gt; E &gt; B/D &gt; C. Metadata in one line, middle dots, tabular numbers.</p></div></div>''')
    import build_components as bc
    for key, slug, name, label in bc.CARDS:
        sp = bc.CARD_SPECS[key]
        page("Cards · 09", f"{label} · {name}", f"{sp['use']} {sp['dont']}",
             fit(f"07_COMPONENTS/cards/card-{key}-{slug}-anatomy.svg", 1088, 470, top=200, bottom=62)
             + '<div style="height:10px"></div>'
             + f'<p style="text-align:center;font-size:11px">{cf(sp["conf"])} — {sp["conf_note"]}</p>')

    # ------------------------------------------------------------ hierarchy + content
    hl = "".join(f'<div class="card {"sig" if i == 0 else ""}" style="margin-bottom:8px;width:{100 - i * 9}%;padding:10px 16px"><span class="lbl" style="color:{C["primary"] if i == 0 else C["text-tertiary"]}">{a}</span>'
                 f'<h3 style="margin:2px 0">{b}</h3><p style="margin:0;font-size:11px">{c_}</p></div>' for i, (a, b, c_) in enumerate(ct.HIERARCHY))
    page("Content · 10", "Information hierarchy", "Five levels, read in order. The levels hold for every content type; what fills them changes.",
         f'''<div class="cols" style="grid-template-columns:380px 1fr">{f"<div>{hl}</div>"}
         <div>{table(["Type", "L1 hook", "L2 headline", "L3 context", "L4 metadata", "L5 action"], ct.HIERARCHY_BY_TYPE)}
         <div class="lbl" style="margin-top:16px">Scanning model</div>
         <p>Hook: image → headline → action. Feed: an F down the left edge with excursions into rails. Detail: headline → byline → first paragraph → sticky action.</p></div></div>''')
    ladder = [("User's own action", "Because you saved Goa"), ("Similar users", "Popular with people like you"), ("Similar item", "Similar to Panjim"),
              ("Context", "For Saturday's forecast"), ("Trend", "Trending near you")]
    page("Content · 10", "Content design language",
         "Specific, sentence-case, stand-alone. Numbers and sources in every volatile claim. Recommendation language carries its own confidence.",
         f'''<div class="cols c3">
         <div><div class="lbl">Headlines</div><p>Sentence case · one idea · ≤ 60 characters on media (two lines), ≤ 80 in lists · specific nouns and numbers ("Six beaches", "₹4,120") · must make sense with no image.</p>
          <div class="lbl" style="margin-top:12px">Metadata</div><p>Source · context · time. For commerce: price · was · off, then freshness. Separator " · ". Tabular numerals, ₹ with Indian grouping.</p>
          <div class="lbl" style="margin-top:12px">CTA language</div><p>Verb + object: Plan a trip · Book at ₹5,842 · See fare · Open official page · Talk to an expert.</p></div>
         <div><div class="lbl">Recommendation language (strongest first)</div>{table(["Signal", "Phrase"], ladder)}
          <p style="margin-top:10px">Never state identity ("because you are…"); never imply surveillance ("we noticed you were at…").</p></div>
         <div><div class="lbl">Urgency, trending, social proof</div><p>Only real numbers with a source: "Only 3 left" (inventory), "12.4k watching", "48k saved". No fake countdowns. "Live" only while live.</p>
          <div class="card" style="margin-top:12px"><div class="lbl">Example · hook</div>
          <p style="margin:0;font-family:Menlo,monospace;font-size:10px;line-height:1.6;color:#fff">[For you]<br>TRAVEL · FOR YOU<br>Monsoon's over. Six beaches<br>worth a long weekend<br>Wake Travel · 4 min<br>[Explore →]</p></div></div></div>''')

    # ------------------------------------------------------------ patterns
    fl = ""
    for key, (name, steps) in ct.PATTERNS.items():
        fl += f'<div style="margin-bottom:14px"><h3>{name}</h3><div class="flow">' + '<span class="a">→</span>'.join(f'<span class="s">{s_}</span>' for s_ in steps) + "</div></div>"
    page("Patterns · 11", "Patterns and personalisation",
         "Commitment rises one step at a time. Personalisation is a loop: signal, recommendation, explanation, action — and the user can always see and change the loop.",
         f'''<div class="cols c2">
         <div>{fl}<h3>Notification</h3><div class="flow"><span class="s">Change</span><span class="a">→</span><span class="s">Alert with new value + time</span><span class="a">→</span><span class="s">Open the thing</span></div>
          <h3 style="margin-top:14px">Onboarding</h3><div class="flow"><span class="s">Promise</span><span class="a">→</span><span class="s">Pick ≥ 3</span><span class="a">→</span><span class="s">Opt-in likeness</span><span class="a">→</span><span class="s">Land on a matching hero</span></div></div>
         <div>{table(["Situation", "Explicitness", "Example"], [("Own action", "Explicit reason", "Because you saved Goa"), ("Likeness", "Badge + delete control", "Starring you"),
                                                              ("Location, weather", "Context in metadata", "26° forecast · Delhi"), ("Trend", "Implicit label", "Trending near you")])}
          <div class="card iris" style="margin-top:14px"><div class="lbl" style="color:{C['iris']}">Controls within one tap</div>
          <p style="margin:0">More like this · Less like this · Why am I seeing this · Remove inferred interest · Delete my photos · Turn off lock-screen stories.</p></div>
          <p style="margin-top:12px">Confidence is shown by wording, not percentages — except fit confidence in commerce (observed as a Glance feature), which states its basis.</p></div></div>''')

    # ------------------------------------------------------------ screens
    page("Screens · 12", "Personalised home, three moments", "The same story is the lock-screen hook, the app hero and the detail page. Personalisation is shown by what appears and named in one iris line.",
         plate("12_UI_EXAMPLES/personalized-home.svg", 1088, top=210, bottom=62))
    page("Screens · 12", "Content feeds", "News and entertainment share one vertical grammar; discovery is a masonry of entry points.",
         plate("12_UI_EXAMPLES/content-feed.svg", 1088, top=210, bottom=62))
    page("Screens · 12", "Recommendations, updates, you", "Every recommendation carries its reason; updates carry data and time; inferred taste is visible and removable.",
         plate("12_UI_EXAMPLES/recommendation-feed.svg", 1088, top=210, bottom=62))
    t4 = "".join(f'<img src="file://{ROOT}/09_SCREEN_TEMPLATES/{n}.svg" style="width:100%">' for n in ["discovery", "commerce", "product-detail", "search", "onboarding"])
    page("Screens · 12", "Screen templates", "Thirteen phone templates, all composed from the component library. Discovery, commerce, product, search, onboarding shown.",
         f'<div class="cols c5" style="gap:16px">{t4}</div>')
    page("Screens · 12", "On the web", "At 1440px the hero sits beside a ranked list; rails show five; side navigation replaces the bottom bar.",
         f'<div class="cols c2" style="gap:18px">{img("12_UI_EXAMPLES/dashboard.svg", 535)}{img("12_UI_EXAMPLES/commerce-feed.svg", 535)}</div>')

    # ------------------------------------------------------------ case
    page("Case application · 13", "A travel assistant that can't make up a fare",
         "How the system extends to the case-study product. Volatile facts are rendered from their source with a timestamp; rules are cited; when neither is possible, the assistant says so and hands off.",
         f'''<div class="cols" style="grid-template-columns:1fr 330px">{plate("12_UI_EXAMPLES/travel-assistant/travel-assistant-flow.svg", 740, top=210, bottom=62)}
         <div>{table(["Component", "Rule"], [("Fare card · live", "Price rendered from the fare API, bound to an offer ID. 'Live · checked 9:41' in green."),
                                            ("Fare card · cached", "Supplier timed out: amber 'Cached 9:32', CTA becomes 'Check live price'."),
                                            ("Price changed", "Dialog restates the new value in the primary label."),
                                            ("Cited answer", "Answer limited to the retrieved snippet; source row with publisher and last-verified date."),
                                            ("Deflect + handoff", "No source → say so, link the official page, offer a human.")])}
         <p class="quote" style="margin-top:16px;font-size:22px">Fetch what changes. Cite what rules. Show why.</p></div></div>''')
    page("Case application · 13", "Assistant answer cards", "All states of the extension components, built from the same tokens as the rest of the system.",
         plate("07_COMPONENTS/assistant/assistant-cards.svg", 1088, bottom=62 + 200))

    # ------------------------------------------------------------ accessibility
    page("Quality · 14", "Accessibility", "Contrast is computed from the tokens. Colour never carries meaning alone, and brand red is never an error.",
         f'''<div class="cols c2">
         <div>{table(["Pair", "Ratio", "Result"], [("White on primary-action", f"{tk.contrast('#FFFFFF', '#E6003F'):.2f}", "AA"), ("White on primary", f"{tk.contrast('#FFFFFF', '#FF0049'):.2f}", "Large text / icons only"),
                                                   ("Primary on background", f"{tk.contrast('#FF0049', '#0C0C10'):.2f}", "AA"), ("Text secondary on dark", f"{tk.contrast('#B8B8C2', '#0C0C10'):.2f}", "AAA"),
                                                   ("Text tertiary on dark surface", f"{tk.contrast('#85838F', '#16161B'):.2f}", "AA"), ("Text tertiary on light surface", f"{tk.contrast('#6B6975', '#F6F5F8'):.2f}", "AA"),
                                                   ("Iris on iris subtle", f"{tk.contrast('#DDBEF0', '#251A2E'):.2f}", "AAA"), ("Success on light", f"{tk.contrast('#0A7F4A', '#FFFFFF'):.2f}", "AA")])}</div>
         <div><ol style="padding-left:18px;margin:0">
          <li>Text on imagery always over a scrim.</li><li>Errors, warnings, live and verified carry an icon or a word.</li>
          <li>Error is orange-red (hue ≈ 15°) with an alert icon; brand red is hue ≈ 343°.</li><li>Targets ≥ 44 × 44.</li>
          <li>Reduced motion: transforms off, 160ms fades, stories paused, no pulse.</li><li>Cards expose one link named kicker + headline + metadata (+ reason).</li>
          <li>Focus: 2px signal ring, 2px offset, dark halo on media.</li><li>Layouts survive 200% text.</li>
          <li>Every personalisation and likeness image can be explained, tuned and deleted.</li></ol></div></div>''')

    # ------------------------------------------------------------ deck
    slides = ["title-slide", "design-dna-slide", "visual-language-slide", "color-slide", "typography-slide", "component-slide", "card-anatomy-slide", "content-hierarchy-slide",
              "personalization-slide", "interaction-model-slide", "design-principles-slide", "example-product-slide", "summary-slide", "section-divider", "architecture-slide", "closing-slide"]
    sl = "".join(f'<img src="file://{ROOT}/13_DECK_ASSETS/png/{n}.png" style="width:100%;border-radius:6px;border:1px solid rgba(255,255,255,.08)">' for n in slides)
    page("Deck · 15", "Deck assets", "Sixteen 1920×1080 slides, as editable SVG and as PNG for any slide tool. Built from the same components.",
         f'<div class="cols c4" style="gap:10px">{sl}</div>')

    # ------------------------------------------------------------ implementation
    page("Implementation · 16", "From tokens to code",
         "One token source generates the JSON, the CSS, every SVG, the slides and this document. Class names match component names.",
         f'''<div class="cols c3">
         <div><div class="lbl">tokens.css (excerpt)</div><pre style="background:{C['surface']};border-radius:12px;padding:14px;font:10px/1.55 Menlo,monospace;color:{C['iris']};margin:0;white-space:pre-wrap">:root {{
  --color-background: #0C0C10;
  --color-primary: #FF0049;
  --color-primary-action: #E6003F;
  --color-iris: #DDBEF0;
  --scrim-bottom: linear-gradient(…);
  --font-sans: Inter, …;
  --font-display: 'Instrument Serif', …;
  --space-4: 16px;
  --radius-l: 16px; --radius-xl: 24px;
  --motion-ease-standard:
    cubic-bezier(.2,0,0,1);
}}
[data-theme="light"] {{ … }}</pre></div>
         <div><div class="lbl">Component classes</div>{table(["Class", "Component"], [("<code>.btn--primary</code>", "Primary button"), ("<code>.chip--iris</code>", "Inferred facet"),
                                                                         ("<code>.badge--fresh</code>", "Live data"), ("<code>.card--hero</code>", "Card A"), ("<code>.card--reco</code>", "Card E"),
                                                                         ("<code>.card--commerce</code>", "Card D"), ("<code>.tabs .tab</code>", "Category tabs"), ("<code>.bottom-nav</code>", "Bottom bar"),
                                                                         ("<code>.fare</code> / <code>.cited</code>", "Assistant cards")])}</div>
         <div><div class="lbl">Package</div>{table(["Folder", "Contents"], [("00–01", "Research, principles"), ("02–06", "Tokens, type, colour, grid, icons"), ("07–08", "Components, patterns"),
                                                                      ("09–12", "Screens, motion, assets, examples"), ("13", "Deck assets"), ("14", "CSS, example.html, specs"), ("fonts", "Inter, Instrument Serif (OFL)")])}</div></div>''')

    # ------------------------------------------------------------ summary
    PAGES.append(f'''<section class="page cover" style="display:flex;flex-direction:column;justify-content:center">
    <div class="kick">Summary</div>
    <div style="font:400 60px/1.02 'Instrument Serif';max-width:980px;margin:18px 0 24px">A wake-first, media-led language that shows you why, and shows you its sources.</div>
    <div class="cols c4" style="max-width:1080px">
      <div><h3>Distinctive</h3><p>Built for the two seconds after a screen wakes: full-bleed media, one line, one tap, the user in the picture.</p></div>
      <div><h3>Primitives</h3><p>Dark stage · signal red · iris lavender · bottom scrim · Inter + Instrument Serif · pill/16/24 · 4px.</p></div>
      <div><h3>Discovery & personalisation</h3><p>A tuned stream with reason-named rails; more, less and why always one tap away.</p></div>
      <div><h3>Reuse without copying</h3><p>Keep the logic, change the identity: your hues, your serif, your photography, your mark.</p></div>
    </div>
    <p class="dim" style="margin-top:40px;font-size:10px">Wake v1.0 · September 2026 · Sources listed on page 2 · Not affiliated with Glance or InMobi · Original artwork.</p>
    </section>''')

    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(PAGES)}</body></html>"
    hp = "/tmp/claude-0/-home-claude/2a5c145d-7fe6-5b3a-8caa-b8de54422ab0/scratchpad/ds.html"
    open(hp, "w").write(doc)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 800})
        pg.goto("file://" + hp)
        pg.wait_for_timeout(1500)
        pg.pdf(path=OUTPDF, width="1200px", height="800px", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    print("pdf pages", len(PAGES))


if __name__ == "__main__":
    build()
