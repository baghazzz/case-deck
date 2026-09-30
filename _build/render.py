"""Rasterise SVG / HTML files with Chromium for visual QA and PNG exports."""
import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def svg_size(p):
    import re
    head = Path(p).read_text()[:600]
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
    return float(m.group(1)), float(m.group(2))


def render_svgs(paths, out_dir, scale=1.0, max_w=None):
    os.makedirs(out_dir, exist_ok=True)
    outs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for sp in paths:
            w, h = svg_size(sp)
            s = scale
            if max_w and w * s > max_w:
                s = max_w / w
            pg.set_viewport_size({"width": int(w * s), "height": int(h * s)})
            pg.goto("file://" + os.path.abspath(sp))
            pg.evaluate(f"document.documentElement.style.width='{w * s}px';document.documentElement.style.height='{h * s}px'")
            pg.wait_for_timeout(80)
            op = os.path.join(out_dir, Path(sp).stem + ".png")
            pg.screenshot(path=op, clip={"x": 0, "y": 0, "width": int(w * s), "height": int(h * s)})
            outs.append(op)
        b.close()
    return outs


if __name__ == "__main__":
    out = sys.argv[1]
    sc = float(sys.argv[2])
    print(render_svgs(sys.argv[3:], out, sc))
