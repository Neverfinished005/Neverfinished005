"""Dark manga-gothic profile art: banner (image), section headers, vitals panel, animated activity map, footer.
Needs: tools/src-hero.jpg, tools/cal.json, tools/stats.json, tools/uc.woff, tools/po.woff, Pillow.
"""
import base64, datetime, io, json, os, random
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A, T = os.path.join(ROOT, 'assets'), os.path.join(ROOT, 'tools')
random.seed(21)
b64f = lambda n: base64.b64encode(open(os.path.join(T, n), 'rb').read()).decode()
UC, PO, GG = b64f('uc.woff'), b64f('po.woff'), b64f('gg.woff')
INK, BONE, DIM, FAINT = '#09090b', '#e9e3d1', '#a8a291', '#5e5a50'
FONTS = f"@font-face{{font-family:'UC';src:url(data:font/woff;base64,{UC}) format('woff')}}@font-face{{font-family:'PO';src:url(data:font/woff;base64,{PO}) format('woff')}}@font-face{{font-family:'GG';src:url(data:font/woff;base64,{GG}) format('woff');font-weight:700}}"

# ---------------------------------------------------------------- shared bits
def scallop(x0, x1, y, step=34, depth=14, flip=1, op=.5):
    d = ''.join(f'M{x},{y} q{step/2},{depth*flip} {step},0 ' for x in range(x0, x1 - step + 1, step))
    return f'<path d="{d}" fill="none" stroke="{BONE}" stroke-opacity="{op}" stroke-width="1.2"/>'

def quatre(r=9):
    return ''.join(f'<circle cx="{dx}" cy="{dy}" r="{r*.62}" fill="none" stroke="{BONE}" stroke-width="1.2"/>' for dx, dy in [(0, -r*.62), (r*.62, 0), (0, r*.62), (-r*.62, 0)]) + f'<circle r="2" fill="{BONE}"/>'

def corner():
    return f'''<g stroke="{BONE}" stroke-opacity=".85" fill="none" stroke-width="1.3"><path d="M0,0 H88 M0,0 V88"/><path d="M13,13 H64 M13,13 V64" stroke-opacity=".4"/>
<path d="M88,0 q13,0 13,13 q0,-8 -8,-8"/><path d="M0,88 q0,13 13,13 q-8,0 -8,-8"/><circle cx="13" cy="13" r="5"/><circle cx="13" cy="13" r="1.6" fill="{BONE}"/></g>
<g transform="translate(44 0)">{quatre(8)}</g><g transform="translate(0 44)">{quatre(8)}</g>'''

def frame(W, H, m=7):
    return f'''<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="none" stroke="{BONE}" stroke-opacity=".95" stroke-width="3.4"/>
<rect x="{m+12}" y="{m+12}" width="{W-2*m-24}" height="{H-2*m-24}" fill="none" stroke="{BONE}" stroke-opacity=".55" stroke-width="1.6" stroke-dasharray="2 6"/>
<g transform="translate({m},{m}) scale(1.6)">{corner()}</g><g transform="translate({W-m},{m}) scale(-1.6,1.6)">{corner()}</g>
<g transform="translate({m},{H-m}) scale(1.6,-1.6)">{corner()}</g><g transform="translate({W-m},{H-m}) scale(-1.6,-1.6)">{corner()}</g>
{scallop(m+150, W-m-150, m, step=44, depth=20, flip=1, op=.8)}{scallop(m+150, W-m-150, H-m, step=44, depth=20, flip=-1, op=.8)}'''

BAT = f'<path d="M0,0 C-6,-11 -19,-13 -29,-4 C-22,-6 -15,-3 -11,3 C-7,-1 -3,1 0,5 C3,1 7,-1 11,3 C15,-3 22,-6 29,-4 C19,-13 6,-11 0,0Z" fill="#000" stroke="{BONE}" stroke-opacity=".5" stroke-width=".8"/>'

# ================================================================ BANNER
W, H = 1200, 900
im = Image.open(os.path.join(T, 'src-hero.jpg')).convert('L').rotate(90, expand=True)
im.thumbnail((1300, 1300))
buf = io.BytesIO(); im.save(buf, 'JPEG', quality=74, optimize=True)
IMG = base64.b64encode(buf.getvalue()).decode()
MOON = (369, 320)   # crescent position inside the 1200x900 cover crop

dust = ''.join(f'<circle cx="{random.randint(30,W-30)}" cy="{random.randint(80,H-40)}" r="{random.choice([.8,1.1,1.6])}" fill="{BONE}" class="du" style="animation-delay:{random.random()*10:.1f}s;animation-duration:{8+random.random()*8:.1f}s;--dx:{random.randint(-40,40)}px"/>' for _ in range(40))
stars = ''.join(f'<circle cx="{random.randint(70,560)}" cy="{random.randint(70,470)}" r="{random.choice([.9,1.3,1.8])}" fill="#fff" class="tw" style="animation-delay:{random.random()*5:.1f}s;animation-duration:{1.8+random.random()*3:.1f}s"/>' for _ in range(36))
shoot = ''.join(f'<g class="sh" style="animation-delay:{d}s"><line x1="0" y1="0" x2="-110" y2="-44" stroke="url(#sg)" stroke-width="2.2" stroke-linecap="round"/></g>' for d in (3, 11, 19))
bats = ''.join(f'<g class="bat" style="animation-delay:{i*3.1:.1f}s;animation-duration:{14+i*2:.1f}s;--y:{random.randint(-30,50)}px;--s:{.5+random.random()*.55:.2f}"><g class="wg" style="animation-delay:{i*.1:.2f}s">{BAT}</g></g>' for i in range(5))
hatch = ''.join(f'<line x1="{x}" y1="0" x2="{x-120}" y2="{H}" stroke="#000" stroke-width="1.2" stroke-opacity=".5"/>' for x in range(0, W + 120, 11))

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Rudi">
<defs><style>{FONTS}
.kb{{animation:kb 30s ease-in-out infinite alternate;transform-origin:62% 55%}}@keyframes kb{{from{{transform:scale(1)}}to{{transform:scale(1.12) translate(-18px,-4px)}}}}
.mg{{animation:mg 6s ease-in-out infinite;transform-origin:{MOON[0]}px {MOON[1]}px}}@keyframes mg{{0%,100%{{opacity:.25;transform:scale(1)}}50%{{opacity:.8;transform:scale(1.18)}}}}
.tw{{animation:tw 3s ease-in-out infinite}}@keyframes tw{{0%,100%{{opacity:.1}}50%{{opacity:1}}}}
.sh{{opacity:0;animation:ss 22s linear infinite;transform:translate(560px,40px)}}@keyframes ss{{0%{{opacity:0;transform:translate(640px,30px)}}1%{{opacity:1}}5%{{opacity:0;transform:translate(300px,170px)}}100%{{opacity:0;transform:translate(300px,170px)}}}}
.fog1{{animation:f1 44s linear infinite alternate}}.fog2{{animation:f2 60s linear infinite alternate}}
@keyframes f1{{from{{transform:translateX(-220px)}}to{{transform:translateX(220px)}}}}@keyframes f2{{from{{transform:translateX(200px)}}to{{transform:translateX(-240px)}}}}
.bat{{opacity:0;animation:fly 16s linear infinite}}
@keyframes fly{{0%{{opacity:0;transform:translate(1260px,calc(150px + var(--y))) scale(var(--s))}}6%{{opacity:1}}50%{{transform:translate(640px,calc(90px + var(--y))) scale(var(--s))}}94%{{opacity:1}}100%{{opacity:0;transform:translate(-60px,calc(150px + var(--y))) scale(var(--s))}}}}
.wg{{animation:fl .3s ease-in-out infinite alternate}}@keyframes fl{{from{{transform:scaleY(1)}}to{{transform:scaleY(.35)}}}}
.du{{opacity:0;animation:du 12s linear infinite}}@keyframes du{{0%{{opacity:0;transform:translate(0,0)}}20%{{opacity:.8}}100%{{opacity:0;transform:translate(var(--dx),-170px)}}}}
.flash{{opacity:0;animation:fx 17s linear infinite}}@keyframes fx{{0%,92%,100%{{opacity:0}}93%{{opacity:.5}}94%{{opacity:.05}}95%{{opacity:.34}}98%{{opacity:0}}}}
.hat{{animation:hat 9s steps(2) infinite}}@keyframes hat{{0%{{transform:translate(0,0)}}50%{{transform:translate(8px,0)}}}}
.rise{{opacity:0;animation:ri 1.4s cubic-bezier(.2,.8,.2,1) .3s forwards}}@keyframes ri{{from{{opacity:0;transform:translateY(26px)}}to{{opacity:1;transform:none}}}}
.sub{{opacity:0;animation:fi 1.2s ease 1.3s forwards}}@keyframes fi{{to{{opacity:1}}}}
.glint{{animation:gl 8s ease-in-out 2.4s infinite}}@keyframes gl{{0%,100%{{opacity:0;transform:translateX(0)}}12%{{opacity:.85}}34%{{opacity:0;transform:translateX(560px)}}}}
.t1{{width:0;animation:ty 3.4s steps(30) 2.4s forwards}}.t2{{width:0;animation:ty 3.2s steps(26) 6s forwards}}@keyframes ty{{to{{width:440px}}}}
.caret{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}
</style>
<filter id="blur" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2400" height="1600"><feGaussianBlur stdDeviation="24"/></filter>
<filter id="hc" color-interpolation-filters="sRGB"><feComponentTransfer><feFuncR type="linear" slope="1.12" intercept="-.04"/><feFuncG type="linear" slope="1.1" intercept="-.04"/><feFuncB type="linear" slope="1.06" intercept="-.03"/></feComponentTransfer></filter>
<radialGradient id="mgl"><stop offset="0" stop-color="#fff" stop-opacity=".85"/><stop offset=".4" stop-color="{BONE}" stop-opacity=".3"/><stop offset="1" stop-color="{BONE}" stop-opacity="0"/></radialGradient>
<linearGradient id="sg" x1="1" x2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="fogg" x1="0" x2="1"><stop offset="0" stop-color="{BONE}" stop-opacity="0"/><stop offset=".5" stop-color="{BONE}" stop-opacity=".2"/><stop offset="1" stop-color="{BONE}" stop-opacity="0"/></linearGradient>
<linearGradient id="bot" x1="0" y1="0" x2="0" y2="1"><stop offset=".38" stop-color="{INK}" stop-opacity="0"/><stop offset=".78" stop-color="{INK}" stop-opacity=".82"/><stop offset="1" stop-color="{INK}" stop-opacity=".97"/></linearGradient>
<linearGradient id="lft" x1="0" x2="1"><stop offset="0" stop-color="{INK}" stop-opacity=".8"/><stop offset=".55" stop-color="{INK}" stop-opacity="0"/></linearGradient>
<radialGradient id="vig" cx="55%" cy="45%" r="78%"><stop offset=".55" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}" stop-opacity=".85"/></radialGradient>
<linearGradient id="streak" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="txt" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".6" stop-color="{BONE}"/><stop offset="1" stop-color="#a8a291"/></linearGradient>
<pattern id="ht" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="3" cy="3" r="1" fill="#000" fill-opacity=".5"/></pattern>
<clipPath id="card"><rect width="{W}" height="{H}" rx="4"/></clipPath>
<clipPath id="k1"><rect class="t1" x="68" y="494" height="30"/></clipPath><clipPath id="k2"><rect class="t2" x="68" y="532" height="28"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="#000"/>
<g class="kb"><image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" filter="url(#hc)" href="data:image/jpeg;base64,{IMG}" xlink:href="data:image/jpeg;base64,{IMG}"/></g>
<circle class="mg" cx="{MOON[0]}" cy="{MOON[1]}" r="190" fill="url(#mgl)"/>
<g>{stars}</g><g>{shoot}</g>
<g class="fog1"><ellipse cx="640" cy="820" rx="600" ry="60" fill="url(#fogg)" filter="url(#blur)"/></g>
<g class="fog2"><ellipse cx="480" cy="700" rx="600" ry="46" fill="url(#fogg)" filter="url(#blur)"/></g>
<g>{bats}</g>
<rect width="{W}" height="{H}" fill="url(#lft)"/><rect width="{W}" height="{H}" fill="url(#bot)"/><rect width="{W}" height="{H}" fill="url(#vig)"/>
<rect width="{W}" height="{H}" fill="url(#ht)" opacity=".55"/>
<g>{dust}</g>
<rect class="flash" width="{W}" height="{H}" fill="#fff"/>
{frame(W, H)}
<g class="rise"><text x="64" y="812" font-family="UC,'Times New Roman',serif" font-size="230" fill="url(#txt)">Rudi</text>
<g transform="skewX(-16)"><rect class="glint" x="20" y="640" width="90" height="190" fill="url(#streak)" opacity="0"/></g></g>
</g></svg>'''
open(os.path.join(A, 'g-banner-v5.svg'), 'w', encoding='utf-8').write(banner)

# ================================================================ SECTION HEADERS (ink band with moving hatch)
def header(slug, label, sub):
    hw, hh = 1200, 104
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {hw} {hh}" width="100%" role="img" aria-label="{label}"><defs><style>{FONTS}
.hb{{animation:hb 6s linear infinite}}@keyframes hb{{to{{transform:translateX(-22px)}}}}
.pp{{animation:pp 5s ease-in-out infinite}}@keyframes pp{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
.sw{{animation:sw 6s ease-in-out infinite}}@keyframes sw{{0%{{transform:translateX(-200px);opacity:0}}18%{{opacity:.8}}55%{{opacity:0;transform:translateX(1000px)}}100%{{opacity:0;transform:translateX(1000px)}}}}
</style>
<pattern id="h" width="11" height="22" patternUnits="userSpaceOnUse" patternTransform="skewX(-35)"><line x1="0" y1="0" x2="0" y2="22" stroke="{BONE}" stroke-width="1.4"/></pattern>
<linearGradient id="fadeL" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="fadeR" x1="1" x2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="mL"><rect x="40" y="0" width="440" height="{hh}" fill="url(#fadeL)"/></mask><mask id="mR"><rect x="720" y="0" width="440" height="{hh}" fill="url(#fadeR)"/></mask>
<linearGradient id="st" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<g mask="url(#mL)"><g class="hb"><rect x="40" y="40" width="470" height="14" fill="url(#h)" opacity=".7"/></g></g>
<g mask="url(#mR)"><g class="hb"><rect x="700" y="40" width="470" height="14" fill="url(#h)" opacity=".7"/></g></g>
<rect x="40" y="36" width="440" height="1.4" fill="{BONE}" opacity=".5" mask="url(#mL)"/><rect x="40" y="58" width="440" height="1.4" fill="{BONE}" opacity=".5" mask="url(#mL)"/>
<rect x="720" y="36" width="440" height="1.4" fill="{BONE}" opacity=".5" mask="url(#mR)"/><rect x="720" y="58" width="440" height="1.4" fill="{BONE}" opacity=".5" mask="url(#mR)"/>
<g class="pp"><g transform="translate(466 47)">{quatre(9)}</g><g transform="translate(734 47)">{quatre(9)}</g></g>
<text x="600" y="62" text-anchor="middle" font-family="UC,'Times New Roman',serif" font-size="48" fill="{BONE}">{label}</text>
<text x="600" y="90" text-anchor="middle" font-family="'Courier New',monospace" font-size="11" fill="{DIM}" letter-spacing="6">{sub}</text>
<g transform="skewX(-18)"><rect class="sw" x="0" y="20" width="60" height="60" fill="url(#st)" opacity="0"/></g></svg>'''
for slug, label, sub in [('about', 'The Dossier', 'ABOUT THE WANDERER'), ('arsenal', 'The Arsenal', 'LANGUAGES · TOOLS'), ('relics', 'Relics', 'THINGS I BUILT'), ('vitals', 'Vital Signs', 'STATS · ACTIVITY')]:
    open(os.path.join(A, f'g-{slug}.svg'), 'w', encoding='utf-8').write(header(slug, label, sub))

# ================================================================ VITALS (own panels, real data)
st = json.load(open(os.path.join(T, 'stats.json')))
cal = json.load(open(os.path.join(T, 'cal.json')))['data']['viewer']['contributionsCollection']['contributionCalendar']
days = [d for w in cal['weeks'] for d in w['contributionDays']]
today = datetime.date.today()
def streaks():
    best = cur = 0; run = 0
    for d in days:
        if d['contributionCount'] > 0: run += 1; best = max(best, run)
        else: run = 0
    cur = 0
    for d in reversed(days):
        if datetime.date.fromisoformat(d['date']) > today: continue
        if d['contributionCount'] > 0: cur += 1
        elif cur == 0 and datetime.date.fromisoformat(d['date']) == today: continue
        else: break
    return cur, best
cur, best = streaks()
total = cal['totalContributions']
tiles = [(str(total), 'CONTRIBUTIONS', 'last 12 months'), (str(st['commits']), 'COMMITS', 'last 12 months'), (str(cur), 'STREAK', f'now · best {best}'), (str(15), 'PUBLIC REPOS', f'{st["followers"]} followers · {st["stars"]} stars')]
VW, VH = 1200, 330
tw_, tg = 270, 16
tx0 = (VW - (4 * tw_ + 3 * tg)) // 2
tilesvg = ''
for i, (n, l, s) in enumerate(tiles):
    x = tx0 + i * (tw_ + tg)
    tilesvg += f'''<g class="tile" style="animation-delay:{i*.18:.2f}s" transform="translate({x} 18)"><rect width="{tw_}" height="150" fill="#0d0d10" stroke="{BONE}" stroke-opacity=".5"/>
<rect x="6" y="6" width="{tw_-12}" height="138" fill="none" stroke="{BONE}" stroke-opacity=".2" stroke-dasharray="1 4"/>
<rect x="8" y="8" width="{tw_-16}" height="138" fill="url(#vh)" opacity=".5"/>
<text x="{tw_/2}" y="84" text-anchor="middle" font-family="UC,serif" font-size="70" fill="{BONE}" class="num">{n}</text>
<text x="{tw_/2}" y="112" text-anchor="middle" font-family="'Courier New',monospace" font-size="13" fill="{BONE}" letter-spacing="4">{l}</text>
<text x="{tw_/2}" y="132" text-anchor="middle" font-family="'Courier New',monospace" font-size="11" fill="{DIM}">{s}</text>
<g transform="translate(14 14)"><path d="M0,10 V0 H10" fill="none" stroke="{BONE}"/></g><g transform="translate({tw_-14} 14) scale(-1,1)"><path d="M0,10 V0 H10" fill="none" stroke="{BONE}"/></g></g>'''
# language bar
lx, ly, lw = tx0, 210, 4 * tw_ + 3 * tg
shades = ['#ffffff', '#d9d3c1', '#aaa493', '#7d7868', '#5a574c', '#3d3b34']
seg, x = '', lx
for i, (n, p) in enumerate(st['langs']):
    w = lw * p / 100
    seg += f'<rect class="lg" x="{x:.1f}" y="{ly}" width="{max(w-2,2):.1f}" height="16" fill="{shades[i]}" style="animation-delay:{i*.25:.2f}s"><title>{n} {p}%</title></rect>'
    x += w
leg, lxx = '', lx
for i, (n, p) in enumerate(st['langs']):
    leg += f'<rect x="{lxx}" y="{ly+34}" width="12" height="12" fill="{shades[i]}"/><text x="{lxx+20}" y="{ly+45}" font-family="\'Courier New\',monospace" font-size="13" fill="{BONE}">{n} <tspan fill="{DIM}">{p}%</tspan></text>'
    lxx += 40 + len(f'{n} {p}%') * 8.2
vit = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="100%" role="img" aria-label="GitHub stats"><defs><style>{FONTS}
.tile{{opacity:0;animation:tl .9s ease forwards}}@keyframes tl{{from{{opacity:0;transform:translate(var(--x,0),30px)}}to{{opacity:1}}}}
.lg{{transform-box:fill-box;transform-origin:left;animation:lg 1.2s cubic-bezier(.2,.8,.2,1) both}}@keyframes lg{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.num{{animation:nm 5s ease-in-out infinite}}@keyframes nm{{0%,100%{{opacity:1}}48%{{opacity:1}}50%{{opacity:.6}}52%{{opacity:1}}}}
</style><pattern id="vh" width="9" height="18" patternUnits="userSpaceOnUse" patternTransform="skewX(-35)"><line x1="0" y1="0" x2="0" y2="18" stroke="{BONE}" stroke-opacity=".12"/></pattern></defs>
<rect width="{VW}" height="{VH}" fill="none"/>{tilesvg}
<text x="{lx}" y="{ly-14}" font-family="'Courier New',monospace" font-size="12" fill="{DIM}" letter-spacing="5">MOST USED SPELLS</text>
<rect x="{lx}" y="{ly}" width="{lw}" height="16" fill="#17171c"/>{seg}{leg}</svg>'''
open(os.path.join(A, 'g-stats.svg'), 'w', encoding='utf-8').write(vit)

# ================================================================ ACTIVITY MAP (continuously animated)
weeks = cal['weeks']
mx = max(d['contributionCount'] for d in days) or 1
cell, gap, left, top = 15, 4, 56, 112
GW = left + len(weeks) * (cell + gap) + 36
GH = top + 7 * (cell + gap) + 66
shade = lambda n: '#17171c' if n == 0 else '#4a4a52' if n / mx < .25 else '#86827a' if n / mx < .5 else '#c9c3b1' if n / mx < .8 else '#ffffff'
cells = ''
for wi, w in enumerate(weeks):
    for d in w['contributionDays']:
        di = (datetime.date.fromisoformat(d['date']).weekday() + 1) % 7
        n = d['contributionCount']
        x, y = left + wi * (cell + gap), top + di * (cell + gap)
        if n:
            cells += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{shade(n)}" filter="url(#g)" class="c on" style="animation-delay:{wi*.02:.2f}s,{(wi*.37+di*.21)%4:.2f}s"><title>{d["date"]}: {n}</title></rect>'
        else:
            cells += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{shade(0)}" class="c e" style="animation-delay:{wi*.02:.2f}s,{random.random()*9:.2f}s"><title>{d["date"]}: 0</title></rect>'
mn, months, last, lw_ = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], '', None, -9
for wi, w in enumerate(weeks):
    m = w['contributionDays'][0]['date'][5:7]
    if m != last and wi - lw_ >= 3:
        lw_ = wi; months += f'<text x="{left+wi*(cell+gap)}" y="{top-12}" font-family="\'Courier New\',monospace" font-size="11" fill="{DIM}">{mn[int(m)]}</text>'
    last = m
leg = ''.join(f'<rect x="{GW-200+i*20}" y="{GH-42}" width="14" height="14" rx="3" fill="{c}"/>' for i, c in enumerate(['#17171c', '#4a4a52', '#86827a', '#c9c3b1', '#ffffff']))
gx0, gx1 = left, left + len(weeks) * (cell + gap)
act = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW} {GH}" width="100%" role="img" aria-label="{total} contributions in the last year"><defs><style>{FONTS}
.c{{transform-box:fill-box;transform-origin:center}}
.c.on{{opacity:0;animation:pop .5s ease forwards,br 4s ease-in-out infinite}}
.c.e{{opacity:0;animation:pop .5s ease forwards,tw 9s ease-in-out infinite}}
@keyframes pop{{from{{opacity:0;transform:scale(.3)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes br{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}@keyframes tw{{0%,92%,100%{{opacity:1}}96%{{opacity:.35}}}}
.scan{{animation:sc 7s linear infinite}}@keyframes sc{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:1}}94%{{opacity:1}}100%{{transform:translateX({gx1-gx0}px);opacity:0}}}}
.moon{{animation:mo 6s ease-in-out infinite}}@keyframes mo{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}
</style>
<filter id="g" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="scg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<rect width="{GW}" height="{GH}" fill="{INK}" stroke="{BONE}" stroke-opacity=".5" rx="3"/>
<rect x="9" y="9" width="{GW-18}" height="{GH-18}" fill="none" stroke="{BONE}" stroke-opacity=".22" stroke-dasharray="1 5" rx="2"/>
<g class="moon"><circle cx="{GW-70}" cy="52" r="20" fill="{BONE}"/><circle cx="{GW-62}" cy="46" r="18" fill="{INK}"/></g>
<text x="{left}" y="56" font-family="UC,serif" font-size="40" fill="{BONE}">Graveyard Shift</text>
<text x="{left}" y="82" font-family="'Courier New',monospace" font-size="13" fill="{DIM}" letter-spacing="3">{total} CONTRIBUTIONS · LAST 12 MONTHS</text>
{months}{cells}
<g class="scan"><rect x="{gx0-20}" y="{top-6}" width="40" height="{7*(cell+gap)+8}" fill="url(#scg)"/></g>
<text x="{GW-214}" y="{GH-31}" text-anchor="end" font-family="'Courier New',monospace" font-size="11" fill="{DIM}">less</text>{leg}
<text x="{GW-92}" y="{GH-31}" font-family="'Courier New',monospace" font-size="11" fill="{DIM}">more</text></svg>'''
open(os.path.join(A, 'g-activity.svg'), 'w', encoding='utf-8').write(act)

# ================================================================ FOOTER
foot = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" width="100%"><defs><style>{FONTS}.fl{{animation:fl 4s ease-in-out infinite}}@keyframes fl{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}</style></defs>
{scallop(60, 1140, 20, 36, 16)}{scallop(60, 1140, 28, 36, 16)}<g class="fl"><g transform="translate(600 20)">{quatre(10)}</g></g>
<text x="600" y="84" text-anchor="middle" font-family="UC,'Times New Roman',serif" font-size="30" fill="{BONE}">stay nocturnal</text>
<text x="600" y="108" text-anchor="middle" font-family="'Courier New',monospace" font-size="11" fill="{DIM}" letter-spacing="6">NEVERFINISHED · NEVER DONE</text></svg>'''
open(os.path.join(A, 'g-footer.svg'), 'w', encoding='utf-8').write(foot)
print({n: os.path.getsize(os.path.join(A, n)) // 1024 for n in sorted(os.listdir(A)) if n.startswith('g-')})
