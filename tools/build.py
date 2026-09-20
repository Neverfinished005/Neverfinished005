#!/usr/bin/env python3
"""
GOTHAM PROFILE BUILDER
----------------------
Generates every SVG used by README.md into ../assets/.

  1. pip install fonttools
  2. edit the CONFIG block below
  3. python tools/build.py

All text is converted to vector outlines using the bundled Bebas Neue font
(SIL Open Font License), so the artwork looks identical on every device,
with no web-fonts and no external requests.
"""
import os
import random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

# ───────────────────────────── CONFIG ──────────────────────────────
NAME = "RUDRA VABLE"
TAGLINE = ["ASPIRING SOFTWARE DEVELOPER", "ML & AI ENTHUSIAST"]

QUOTES = [
    "LEARNING PYTHON + MACHINE LEARNING.",
    "SOLVING DSA PROBLEMS DAILY.",
    "BUILDING WITH SQL AND MOBILE APPS.",
    "OPEN TO SDE AND AI OPPORTUNITIES.",
]

# Utility belt: four pouches, up to five items each
BELT = [
    ("LANGUAGES", ["PYTHON", "JAVA", "C++", "SQL"]),
    ("MACHINE LEARNING", ["ML BASICS", "MODEL BUILDING", "APPLIED AI"]),
    ("FUNDAMENTALS", ["DSA", "PROBLEM SOLVING", "DBMS"]),
    ("BUILDING", ["MOBILE APPS", "ML MODELS", "DATABASES"]),
]

FOOTER_TOP = "GOTHAM NEEDS ANOTHER DEVELOPER."
FOOTER_SUB = "LIGHT THE SIGNAL. LET'S TALK."
# ───────────────────────────────────────────────────────────────────

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")
os.makedirs(OUT, exist_ok=True)

# Palette
GOTHAM = "#07080C"
ASPHALT = "#0C0F16"
STEEL = "#8B94A7"
FOG = "#D5DAE5"
SIGNAL = "#FFD400"
SIGNAL_HOT = "#FFF08A"

# ─────────────────────── text → vector outlines ────────────────────
FONT = TTFont(os.path.join(HERE, "BebasNeue-Regular.ttf"))
GS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
HMTX = FONT["hmtx"]
UPM = FONT["head"].unitsPerEm


def _n(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def text_width(t, size, ls=0.0):
    s = size / UPM
    ws = [HMTX[CMAP[ord(c)]][0] * s + ls for c in t if ord(c) in CMAP]
    return sum(ws) - ls if ws else 0


def text_path(t, size, x, y, anchor="start", ls=0.0):
    t = t.upper()
    w = text_width(t, size, ls)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    s = size / UPM
    cx, out = x, []
    for c in t:
        g = CMAP.get(ord(c))
        if g is None:
            continue
        pen = SVGPathPen(GS, ntos=_n)
        GS[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        out.append(pen.getCommands())
        cx += HMTX[g][0] * s + ls
    return "".join(out)


def fit(t, size, avail, ls=0.0):
    """Shrink font size so text fits within `avail` px."""
    w = text_width(t.upper(), size, ls)
    return size if w <= avail else size * avail / w


def text(t, size, x, y, fill, anchor="start", ls=0.0, extra=""):
    return f'<path d="{text_path(t, size, x, y, anchor, ls)}" fill="{fill}" {extra}/>'


# ───────────────────────── bat emblem ──────────────────────────────
# Original wing-and-ears emblem drawn in a 200 x 100 box, mirrored about x=100.
_RIGHT = [
    ("L", 104, 24), ("L", 110, 6), ("L", 118, 22),
    ("Q", 150, 2, 196, 22), ("Q", 199, 35, 185, 47),
    ("L", 177, 39), ("L", 168, 61), ("L", 157, 48), ("L", 146, 66),
    ("L", 136, 51), ("Q", 121, 57, 112, 76), ("L", 100, 95),
]


def _bat_d():
    p0 = (100, 24)
    pts = [p0] + [(s[-2], s[-1]) for s in _RIGHT]
    d = [f"M{p0[0]},{p0[1]}"]
    for s in _RIGHT:
        d.append(f"{s[0]}{','.join(map(str, s[1:]))}")
    for i in range(len(_RIGHT) - 1, -1, -1):
        s, tgt = _RIGHT[i], pts[i]
        tx = 200 - tgt[0]
        if s[0] == "L":
            d.append(f"L{tx},{tgt[1]}")
        else:
            d.append(f"Q{200 - s[1]},{s[2]} {tx},{tgt[1]}")
    d.append("Z")
    return "".join(d)


BAT_D = _bat_d()


def bat(x, y, w, fill, extra=""):
    """Bat emblem centred on (x, y), width w."""
    k = w / 200
    return (f'<path d="{BAT_D}" fill="{fill}" {extra} '
            f'transform="translate({x - 100 * k:.1f} {y - 50 * k:.1f}) scale({k:.3f})"/>')


# ───────────────────────── Gotham skyline ──────────────────────────
def skyline(rng, x0, x1, base, hmin, hmax, fill, lit, lit_op, density,
            flick=0, wmin=26, wmax=64, gothic=0.4):
    """Returns (svg, flicker_svg). Buildings + windows, deterministic per rng."""
    blds, wins, flick_wins = [], [], []
    x = x0
    while x < x1:
        w = rng.randint(wmin, wmax)
        h = rng.randint(hmin, hmax)
        top = base - h
        kind = rng.random()
        if kind < gothic:                       # pointed gothic roof
            roof = rng.randint(14, 30)
            d = f"M{x},{base}V{top}L{x + w / 2:.1f},{top - roof}L{x + w},{top}V{base}Z"
        elif kind < gothic + 0.2:               # stepped setback
            sw = w * 0.6
            sx = x + (w - sw) / 2
            st = rng.randint(10, 22)
            d = (f"M{x},{base}V{top}H{sx:.1f}V{top - st}H{sx + sw:.1f}"
                 f"V{top}H{x + w}V{base}Z")
        elif kind < gothic + 0.3:               # antenna tower
            ax = x + w / 2
            d = (f"M{x},{base}V{top}H{ax - 1:.1f}V{top - rng.randint(16, 34)}"
                 f"H{ax + 1:.1f}V{top}H{x + w}V{base}Z")
        else:                                   # flat roof w/ parapet notch
            d = f"M{x},{base}V{top}H{x + w}V{base}Z"
        blds.append(d)
        cols = max(1, int((w - 8) // 9))
        rows = min(13, int((h - 10) // 12))
        for r in range(rows):
            for c in range(cols):
                if rng.random() < density:
                    wx = x + 5 + c * 9 + (w - 8 - cols * 9) / 2
                    wy = top + 8 + r * 12
                    if flick and rng.random() < 0.06:
                        flick_wins.append((wx, wy))
                        flick -= 1
                    else:
                        wins.append(f"M{wx:.1f},{wy:.1f}h3.4v5h-3.4z")
        x += w + rng.randint(-4, 3)
    svg = f'<path d="{"".join(blds)}" fill="{fill}"/>'
    svg += f'<path d="{"".join(wins)}" fill="{lit}" opacity="{lit_op}"/>'
    fl = ""
    for i, (wx, wy) in enumerate(flick_wins):
        fl += (f'<rect class="anim f{i % 3 + 1}" x="{wx:.1f}" y="{wy:.1f}" '
               f'width="3.4" height="5" fill="{lit}" style="animation-delay:{(i * 0.7) % 5:.1f}s"/>')
    return svg, fl


REDUCED = "@media (prefers-reduced-motion: reduce){.anim{animation:none!important}}"


def svg_open(w, h, title, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{title}">'
            f'<title>{title}</title><style>{css}{REDUCED}</style>')


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {name:22s} {os.path.getsize(path) / 1024:6.1f} KB")


# ═══════════════════════════ HEADER ════════════════════════════════
def build_header():
    W, H = 1000, 420
    rng = random.Random(1939)
    sx, sy = 730, 104                    # bat-signal centre
    bx, by = 884, 338                    # searchlight base
    # beam geometry
    import math
    dx, dy = sx - bx, sy - by
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    r_end, r_start = 74, 5
    beam = (f"M{bx + px * r_start:.1f},{by + py * r_start:.1f}"
            f"L{sx + px * r_end:.1f},{sy + py * r_end:.1f}"
            f"L{sx - px * r_end:.1f},{sy - py * r_end:.1f}"
            f"L{bx - px * r_start:.1f},{by - py * r_start:.1f}Z")

    css = """
    .rain{animation:fall .9s linear infinite}
    @keyframes fall{to{transform:translateY(100px)}}
    .flash{opacity:0;animation:flash 11s linear infinite}
    @keyframes flash{0%,91%{opacity:0}92%{opacity:.34}93%{opacity:.02}94.5%{opacity:.2}96%,100%{opacity:0}}
    .sig{animation:sig 12s linear infinite}
    @keyframes sig{0%{opacity:0}2%{opacity:1}3.5%{opacity:.25}5%{opacity:1}6%{opacity:.5}7%{opacity:1}
                   30%{opacity:.86}55%{opacity:1}80%{opacity:.86}100%{opacity:1}}
    .f1{animation:fl 3.7s steps(1) infinite}
    .f2{animation:fl 5.3s steps(1) infinite}
    .f3{animation:fl 7.1s steps(1) infinite}
    @keyframes fl{0%{opacity:.85}38%{opacity:.85}39%{opacity:0}62%{opacity:0}63%{opacity:.85}100%{opacity:.85}}
    .fly{animation:fly 15s linear infinite}
    .bob{animation:bob 1.6s ease-in-out infinite}
    .flap{animation:flap .42s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}
    @keyframes fly{from{transform:translateX(-80px)}to{transform:translateX(1100px)}}
    @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
    @keyframes flap{from{transform:scaleY(1)}to{transform:scaleY(.5)}}
    .cape{animation:cape 3.2s ease-in-out infinite;transform-box:fill-box;transform-origin:right top}
    @keyframes cape{0%,100%{transform:skewX(0)}50%{transform:skewX(-5deg)}}
    """
    s = svg_open(W, H, f"{NAME}, Gotham City developer profile banner", css)

    s += f"""<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#03040A"/><stop offset=".55" stop-color="#0B0F1B"/><stop offset="1" stop-color="#1B2440"/>
  </linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="{SIGNAL}" stop-opacity=".42"/><stop offset=".5" stop-color="{SIGNAL}" stop-opacity=".12"/><stop offset="1" stop-color="{SIGNAL}" stop-opacity="0"/></radialGradient>
  <radialGradient id="disc"><stop offset="0" stop-color="{SIGNAL_HOT}"/><stop offset=".65" stop-color="{SIGNAL}"/><stop offset="1" stop-color="#E0B400"/></radialGradient>
  <linearGradient id="beamg" gradientUnits="userSpaceOnUse" x1="{bx}" y1="{by}" x2="{sx}" y2="{sy}">
    <stop offset="0" stop-color="{SIGNAL_HOT}" stop-opacity=".62"/><stop offset="1" stop-color="{SIGNAL}" stop-opacity=".16"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOTHAM}" stop-opacity=".72"/><stop offset=".6" stop-color="{GOTHAM}" stop-opacity="0"/></linearGradient>
  <filter id="blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="3.5"/></filter>
  <path id="bat" d="{BAT_D}"/>
  <path id="raintile" d=""/>
</defs>"""

    # sky + clouds
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += '<g filter="url(#blur)" opacity=".8">'
    for cx, cy, rx, ry, c, o in [(120, 60, 200, 34, "#1B2238", .9), (430, 30, 260, 30, "#1E2640", .8),
                                 (700, 60, 240, 44, "#28304C", .9), (930, 40, 170, 36, "#20283F", .9),
                                 (300, 150, 220, 26, "#141A2C", .7), (560, 175, 260, 24, "#1A2136", .6)]:
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}" opacity="{o}"/>'
    s += "</g>"
    # lightning wash (behind skyline so silhouettes pop)
    s += f'<rect class="anim flash" width="{W}" height="{H}" fill="#BFD2FF"/>'

    # signal: halo, beam, disc, emblem
    s += '<g class="anim sig">'
    s += f'<circle cx="{sx}" cy="{sy}" r="250" fill="url(#halo)"/>'
    s += f'<path d="{beam}" fill="url(#beamg)" filter="url(#soft)"/>'
    s += f'<path d="{beam}" fill="url(#beamg)" opacity=".55"/>'
    s += f'<ellipse cx="{sx}" cy="{sy}" rx="86" ry="66" fill="url(#disc)"/>'
    s += bat(sx, sy + 2, 104, "#06070B")
    s += "</g>"

    # skyline layers
    far, _ = skyline(rng, -20, W + 40, H, 60, 128, "#101625", "#FFCB3D", .22, .22, wmin=30, wmax=70)
    mid, mf = skyline(rng, -20, W + 40, H, 40, 104, "#0A0D15", "#FFCB3D", .5, .26, flick=9, wmin=28, wmax=60)
    s += far + mid + mf

    # falling rain
    tile_rng = random.Random(7)
    rd = "".join(f"M{tile_rng.uniform(-40, W + 40):.0f},{tile_rng.uniform(0, 100):.0f}l-5,16"
                 for _ in range(46))
    s = s.replace('<path id="raintile" d=""/>', f'<path id="raintile" d="{rd}" stroke="#9DB4FF" stroke-width="1" stroke-linecap="round"/>')
    s += '<g opacity=".28"><g class="anim rain">'
    for k in range(-1, 5):
        s += f'<use href="#raintile" y="{k * 100}"/>'
    s += "</g></g>"

    # flying bats (cross the signal)
    for (y0, size, delay, spd) in [(150, 22, 0, 15), (96, 15, 5.5, 17), (210, 12, 9.5, 20)]:
        s += (f'<g transform="translate(0 {y0})"><g class="anim fly" style="animation-delay:-{delay}s;animation-duration:{spd}s">'
              f'<g class="anim bob" style="animation-delay:-{delay / 2:.1f}s"><g class="anim flap">'
              f'<use href="#bat" fill="#020308" transform="translate({-size / 2:.1f} {-size / 4:.1f}) scale({size / 200:.3f})"/>'
              f'</g></g></g></g>')

    # near skyline + set-piece rooftops
    near, nf = skyline(rng, -20, 760, H, 26, 78, "#05070B", "#FFD23F", .75, .3, flick=6, wmin=30, wmax=58)
    s += near + nf
    # rooftop A (Batman) x 772-852, rooftop B (searchlight) x 852-930
    s += f'<path d="M772,{H}V334H778V326H846V334H852V{H}Z" fill="#05070B"/>'
    s += f'<path d="M852,{H}V346H858V340H924V346H930V{H}Z" fill="#05070B"/>'
    # gargoyle-ish finials
    s += '<path d="M776,326l3,-12l3,12zM840,326l3,-12l3,12z" fill="#05070B"/>'
    # rooftop windows
    ww = "".join(f"M{x},{y}h3.4v5h-3.4z" for x in (784, 800, 816, 832) for y in (350, 372, 394) if (x + y) % 3)
    s += f'<path d="{ww}" fill="#FFD23F" opacity=".6"/>'

    # Batman silhouette, standing at the roof edge, cape streaming in the wind
    s += ('<g transform="translate(818 326) scale(1.3)" fill="#020308">'
          '<g class="anim cape"><path d="M-1,-42C-8,-34 -22,-20 -34,-4L-27,-8L-23,-1L-18,-9L-13,-2L-9,-9L-4,-2L0,-8Z"/></g>'
          '<path d="M-2,-42L6,-42L7,-24L6,0L2,0L1,-13L-1,-13L-2,0L-6,0L-3,-24Z"/>'
          '<path d="M7,-37L14,-34L14,-32L6,-32Z"/>'
          '<ellipse cx="3" cy="-47" rx="4.6" ry="5.4"/>'
          '<path d="M-1.4,-49L-0.2,-59L3,-51.5L6.2,-59L7.4,-49Z"/></g>')

    # searchlight
    s += (f'<g fill="#05070B"><rect x="{bx - 14}" y="{by - 2}" width="28" height="8" rx="2"/>'
          f'<path d="M{bx - 12},{by - 2}A12,12 0 0 1 {bx + 12},{by - 2}Z"/></g>')
    s += f'<ellipse cx="{bx}" cy="{by - 4}" rx="8" ry="3" fill="{SIGNAL_HOT}"/>'

    # left-to-right readability fade behind the title
    s += f'<rect width="640" height="{H}" fill="url(#fade)"/>'

    # ── title block ──
    s += f'<path d="{text_path(NAME, 136, 64, 216, ls=3)}" fill="{SIGNAL}" opacity=".9" transform="translate(4 4)"/>'
    s += text(NAME, 136, 64, 216, "#F4F6FA", ls=3)
    # tagline with bat separators
    x, y = 68, 268
    for i, part in enumerate(TAGLINE):
        s += text(part, 25, x, y, STEEL, ls=2.2)
        x += text_width(part.upper(), 25, 2.2)
        if i < len(TAGLINE) - 1:
            s += bat(x + 19, y - 8, 21, SIGNAL)
            x += 38
    print(f"  tagline ends at x={x:.0f} (keep under ~790 to clear the beam)")
    # signature slash under name
    ex = 64 + text_width(NAME.upper(), 136, 3)
    s += f'<path d="M64,238H{ex:.0f}L{ex - 10:.0f},246H64Z" fill="{SIGNAL}"/>'
    s += f'<rect width="{W}" height="{H}" fill="none" stroke="#1B2033" stroke-width="2"/>'
    s += "</svg>"
    write("header.svg", s)


# ═══════════════════════ SECTION BANNERS ═══════════════════════════
def build_banner(fname, title, note):
    W, H = 1000, 76
    s = svg_open(W, H, f"{title}: {note}")
    tw = text_width(title.upper(), 46, 3)
    s += f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="8" fill="{ASPHALT}" stroke="#1E2432" stroke-width="2"/>'
    s += f'<path d="M14,14H104L88,62H14Z" fill="{SIGNAL}"/>'
    s += bat(52, 38, 50, "#07080C")
    s += text(title, 46, 122, 54, "#F4F6FA", ls=3)
    lx = 122 + tw + 22
    s += f'<path d="M{lx:.0f},36H{W - 250}" stroke="{SIGNAL}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round" opacity=".7"/>'
    s += text(note, 28, W - 30, 48, STEEL, anchor="end", ls=3)
    s += "</svg>"
    write(fname, s)


# ═════════════════════════ UTILITY BELT ════════════════════════════
def build_belt():
    n = max(len(it) for _, it in BELT)
    ph = 104 + (n - 1) * 32 + 26          # pouch height
    W, H = 1000, 60 + ph + 20
    s = svg_open(W, H, "Utility belt: " + "; ".join(f"{t.title()}: {', '.join(i).title()}" for t, i in BELT))
    s += f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="{GOTHAM}" stroke="#1E2432" stroke-width="2"/>'
    # strap
    s += '<rect x="1" y="26" width="998" height="48" fill="#141824"/>'
    s += f'<path d="M1,34H999M1,66H999" stroke="{SIGNAL}" stroke-width="1.5" stroke-dasharray="7 6" opacity=".55"/>'
    xs = [60, 266, 544, 750]
    for i, (title, items) in enumerate(BELT[:4]):
        x, y, w, h = xs[i], 60, 190, ph
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#0E1118" stroke="#2A3142" stroke-width="2"/>'
        # flap
        s += f'<path d="M{x},{y + 12}Q{x},{y} {x + 12},{y}H{x + w - 12}Q{x + w},{y} {x + w},{y + 12}V{y + 52}L{x + w / 2},{y + 68}L{x},{y + 52}Z" fill="#171C29" stroke="#2A3142" stroke-width="2"/>'
        s += f'<path d="M{x + 10},{y + 10}H{x + w - 10}V{y + 46}L{x + w / 2},{y + 60}L{x + 10},{y + 46}Z" fill="none" stroke="{SIGNAL}" stroke-width="1.2" stroke-dasharray="5 4" opacity=".55"/>'
        s += text(title, fit(title, 30, w - 36, 3), x + w / 2, y + 40, SIGNAL, anchor="middle", ls=3)
        for j, it in enumerate(items[:5]):
            iy = y + 104 + j * 32
            s += bat(x + 26, iy - 8, 15, SIGNAL, 'opacity=".85"')
            s += text(it, fit(it, 25, w - 58, 1.6), x + 42, iy, FOG, ls=1.6)
        # snap studs
        s += f'<circle cx="{x + w / 2}" cy="{y + 78}" r="4" fill="{SIGNAL}"/>'
    # buckle
    s += f'<rect x="452" y="18" width="96" height="64" rx="14" fill="{SIGNAL}" stroke="#B38F00" stroke-width="3"/>'
    s += '<rect x="460" y="26" width="80" height="48" rx="9" fill="#E7BC00"/>'
    s += bat(500, 50, 58, "#07080C")
    s += "</svg>"
    write("utility-belt.svg", s)


# ═════════════════════════════ TYPER ═══════════════════════════════
def build_typer():
    W, H = 1000, 58
    n, per = len(QUOTES), 3.6
    total = n * per
    css = ".q{opacity:0;animation:q %.1fs linear infinite}" % total
    # per-line visibility window as % of the total loop
    css += ("@keyframes q{0%%{opacity:0;transform:translateX(-10px)}%.2f%%{opacity:1;transform:translateX(0)}"
            "%.2f%%{opacity:1}%.2f%%{opacity:0}100%%{opacity:0}}") % (
        100 * 0.4 / total, 100 * (per - 0.5) / total, 100 * (per - 0.05) / total)
    s = svg_open(W, H, "Rotating one-liners", css)
    s += f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="8" fill="{ASPHALT}" stroke="#1E2432" stroke-width="2"/>'
    for i, qt in enumerate(QUOTES):
        w = text_width(qt.upper(), 30, 2.4)
        x = 500 - (w + 26) / 2
        s += (f'<g class="anim q" style="animation-delay:{i * per:.1f}s">'
              f'<rect x="{x:.1f}" y="17" width="7" height="26" fill="{SIGNAL}"/>'
              + text(qt, 30, x + 24, 42, FOG, ls=2.4) + "</g>")
    s += "</svg>"
    write("typing.svg", s)


# ═══════════════════════════ DIVIDER ═══════════════════════════════
def build_divider():
    W, H = 1000, 34
    s = svg_open(W, H, "divider")
    s += (f'<defs><linearGradient id="g"><stop offset="0" stop-color="{SIGNAL}" stop-opacity="0"/>'
          f'<stop offset="1" stop-color="{SIGNAL}" stop-opacity=".8"/></linearGradient>'
          f'<linearGradient id="h"><stop offset="0" stop-color="{SIGNAL}" stop-opacity=".8"/>'
          f'<stop offset="1" stop-color="{SIGNAL}" stop-opacity="0"/></linearGradient></defs>')
    s += '<rect x="60" y="16" width="380" height="2" fill="url(#g)"/><rect x="560" y="16" width="380" height="2" fill="url(#h)"/>'
    s += bat(500, 17, 56, SIGNAL)
    s += "</svg>"
    write("divider.svg", s)


# ════════════════════════════ FOOTER ═══════════════════════════════
def build_footer():
    W, H = 1000, 320
    rng = random.Random(1966)
    css = """
    .beat{animation:beat 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
    @keyframes beat{0%,100%{transform:scale(1);opacity:.85}50%{transform:scale(1.14);opacity:1}}
    .f1{animation:fl 4.1s steps(1) infinite}.f2{animation:fl 6.3s steps(1) infinite}.f3{animation:fl 8.9s steps(1) infinite}
    @keyframes fl{0%{opacity:.85}40%{opacity:.85}41%{opacity:0}60%{opacity:0}61%{opacity:.85}100%{opacity:.85}}
    """
    s = svg_open(W, H, f"{FOOTER_TOP} {FOOTER_SUB}", css)
    s += f"""<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03040A"/><stop offset="1" stop-color="#1B2440"/></linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="{SIGNAL}" stop-opacity=".5"/><stop offset=".55" stop-color="{SIGNAL}" stop-opacity=".1"/><stop offset="1" stop-color="{SIGNAL}" stop-opacity="0"/></radialGradient>
  <radialGradient id="disc"><stop offset="0" stop-color="{SIGNAL_HOT}"/><stop offset=".7" stop-color="{SIGNAL}"/><stop offset="1" stop-color="#E0B400"/></radialGradient>
</defs>"""
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += f'<circle class="anim beat" cx="500" cy="84" r="210" fill="url(#halo)"/>'
    s += f'<ellipse cx="500" cy="84" rx="66" ry="50" fill="url(#disc)"/>'
    s += bat(500, 86, 76, "#06070B")
    far, _ = skyline(rng, -20, W + 40, H, 36, 76, "#101625", "#FFCB3D", .25, .2, wmin=30, wmax=66)
    near, nf = skyline(rng, -20, W + 40, H, 18, 50, "#05070B", "#FFD23F", .7, .3, flick=6, wmin=30, wmax=60)
    s += far + near + nf
    s += text(FOOTER_TOP, 66, 500, 196, "#F4F6FA", anchor="middle", ls=3)
    s += text(FOOTER_SUB, 30, 500, 236, SIGNAL, anchor="middle", ls=4.5)
    s += f'<rect width="{W}" height="{H}" fill="none" stroke="#1B2033" stroke-width="2"/>'
    s += "</svg>"
    write("footer.svg", s)


if __name__ == "__main__":
    print("Building Gotham assets…")
    build_header()
    build_banner("h-case-file.svg", "CASE FILE", "ABOUT ME")
    build_banner("h-utility-belt.svg", "UTILITY BELT", "SKILLS")
    build_banner("h-current.svg", "CURRENT MISSION", "STATUS")
    build_banner("h-batcomputer.svg", "BAT-COMPUTER", "GITHUB STATS")
    build_banner("h-patrol.svg", "PATROL LOG", "ACTIVITY")
    build_banner("h-signal.svg", "THE BAT-SIGNAL", "CONTACT")
    build_belt()
    build_typer()
    build_divider()
    build_footer()
    print("Done.")
