"""Dark gothic profile art (banner, section headers, footer, activity graph). No external assets.
Usage: python tools/make_gothic.py      (activity graph reads tools/cal.json from `gh api graphql`)
"""
import base64, datetime, json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'assets')
random.seed(13)
b64 = lambda n: base64.b64encode(open(os.path.join(ROOT, 'tools', n), 'rb').read()).decode()
UC, PO = b64('uc.woff'), b64('po.woff')

INK, INK2, BONE, DIM, ASH, RED = '#09090b', '#121216', '#e9e3d1', '#a8a291', '#3a3a42', '#9c1c2c'
FONTS = f"""@font-face{{font-family:'UC';src:url(data:font/woff;base64,{UC}) format('woff')}}
@font-face{{font-family:'PO';src:url(data:font/woff;base64,{PO}) format('woff')}}"""

# ------------------------------------------------------------------ shared pieces
def scallop(x0, x1, y, step=34, depth=15, flip=1):
    d = ''.join(f'M{x},{y} q{step/2},{depth*flip} {step},0 ' for x in range(x0, x1 - step + 1, step))
    return f'<path d="{d}" fill="none" stroke="{BONE}" stroke-opacity=".55" stroke-width="1.2"/>'

def quatrefoil(r=9):
    return ''.join(f'<circle cx="{dx}" cy="{dy}" r="{r*0.62}" fill="none" stroke="{BONE}" stroke-width="1.2" transform="translate({0},{0})"/>' for dx, dy in [(0, -r*.62), (r*.62, 0), (0, r*.62), (-r*.62, 0)]) + f'<circle r="2" fill="{BONE}"/>'

def corner():
    return f'''<g stroke="{BONE}" stroke-opacity=".8" fill="none" stroke-width="1.3">
<path d="M0,0 H92 M0,0 V92"/><path d="M14,14 H70 M14,14 V70" stroke-opacity=".45"/>
<path d="M92,0 q14,0 14,14 q0,-9 -9,-9" /><path d="M0,92 q0,14 14,14 q-9,0 -9,-9"/>
<circle cx="14" cy="14" r="5"/><circle cx="14" cy="14" r="1.6" fill="{BONE}"/></g>
<g transform="translate(46 0)">{quatrefoil(9)}</g><g transform="translate(0 46)">{quatrefoil(9)}</g>'''

def frame(W, H, m=22):
    return f'''<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="none" stroke="{BONE}" stroke-opacity=".7" stroke-width="1.6"/>
<rect x="{m+8}" y="{m+8}" width="{W-2*m-16}" height="{H-2*m-16}" fill="none" stroke="{BONE}" stroke-opacity=".28" stroke-dasharray="1 5"/>
<g transform="translate({m},{m})">{corner()}</g>
<g transform="translate({W-m},{m}) scale(-1,1)">{corner()}</g>
<g transform="translate({m},{H-m}) scale(1,-1)">{corner()}</g>
<g transform="translate({W-m},{H-m}) scale(-1,-1)">{corner()}</g>
{scallop(m+100, W-m-100, m, flip=1)}{scallop(m+100, W-m-100, H-m, flip=-1)}'''

BAT = f'<path d="M0,0 C-6,-11 -19,-13 -29,-4 C-22,-6 -15,-3 -11,3 C-7,-1 -3,1 0,5 C3,1 7,-1 11,3 C15,-3 22,-6 29,-4 C19,-13 6,-11 0,0Z" fill="#000" stroke="{BONE}" stroke-opacity=".5" stroke-width=".8"/>'

# ================================================================== BANNER
W, H = 1200, 540
stars = ''.join(f'<circle cx="{random.randint(30,W-30)}" cy="{random.randint(30,330)}" r="{random.choice([.6,.8,1.1,1.5])}" fill="{BONE}" class="tw" style="animation-delay:{random.random()*5:.1f}s;animation-duration:{2+random.random()*3:.1f}s"/>' for _ in range(110))
flies = ''.join(f'<circle cx="{random.randint(560,1150)}" cy="{random.randint(330,470)}" r="1.8" fill="#fff6c8" class="ff" style="animation-delay:{random.random()*8:.1f}s;animation-duration:{5+random.random()*6:.1f}s;--dx:{random.randint(-40,40)}px;--dy:{random.randint(-50,50)}px"/>' for _ in range(22))
bats = ''.join(f'<g class="bat" style="animation-delay:{i*2.3:.1f}s;animation-duration:{13+i*1.7:.1f}s;--y:{random.randint(-40,40)}px;--s:{.55+random.random()*.6:.2f}"><g class="wing" style="animation-delay:{i*.09:.2f}s">{BAT}</g></g>' for i in range(7))
grave = lambda x, y, s=1: f'<g transform="translate({x},{y}) scale({s})"><path d="M-14,0 V-34 Q-14,-48 0,-48 Q14,-48 14,-34 V0Z" fill="#050507" stroke="{BONE}" stroke-opacity=".35"/><path d="M0,-40 V-24 M-6,-33 H6" stroke="{BONE}" stroke-opacity=".5"/></g>'
tree = f'<g transform="translate(940 420)" stroke="#000" fill="none" stroke-linecap="round"><path d="M0,0 C4,-60 -6,-100 2,-150" stroke-width="9"/><path d="M2,-100 C-30,-120 -50,-140 -64,-170 M2,-120 C30,-140 54,-150 70,-184 M-6,-70 C-34,-80 -60,-78 -80,-98 M4,-84 C30,-92 58,-90 78,-112 M2,-150 C-6,-170 -4,-190 8,-206" stroke-width="3.6"/></g>'
figure = f'''<g transform="translate(1030 444)">
 <circle class="lh" cx="92" cy="-132" r="74" fill="#ffd993" opacity=".38" filter="url(#blur)"/>
 <path d="M-130,6 Q-60,-14 0,-8 T150,4 V30 H-130Z" fill="#000"/>
 <g class="sway">
 <path d="M3,-300 C-3,-278 -24,-266 -32,-236 C-40,-206 -46,-170 -62,-110 C-72,-70 -82,-30 -98,2 L-78,-8 L-62,4 L-44,-6 L-26,4 L-8,-6 L10,4 L28,-6 L46,4 L64,-6 L80,4 L98,2 C84,-34 76,-72 66,-110 C50,-170 42,-206 34,-236 C26,-266 8,-278 3,-300Z" fill="#050507" stroke="{BONE}" stroke-opacity=".45" stroke-width="1.2"/>
 <path d="M3,-262 C-14,-262 -22,-246 -22,-230 C-22,-214 -12,-204 3,-204 C18,-204 28,-214 28,-230 C28,-246 20,-262 3,-262Z" fill="#000"/>
 <g class="eye"><ellipse cx="-6" cy="-232" rx="3.6" ry="2" fill="{BONE}"/><ellipse cx="12" cy="-232" rx="3.6" ry="2" fill="{BONE}"/></g>
 <path d="M30,-196 C52,-176 66,-156 82,-142" fill="none" stroke="{BONE}" stroke-opacity=".5" stroke-width="5" stroke-linecap="round"/>
 <path d="M30,-196 C52,-176 66,-156 82,-142" fill="none" stroke="#050507" stroke-width="3.6" stroke-linecap="round"/>
 </g>
 <g transform="translate(92 -132)"><path d="M-7,-14 q7,-12 14,0" fill="none" stroke="{BONE}" stroke-width="1.6"/><rect x="-9" y="-13" width="18" height="26" rx="2" fill="#2a1b08" stroke="{BONE}" stroke-width="1.4"/>
 <g class="flame"><path d="M0,10 C-7,2 -4,-6 0,-14 C4,-6 7,2 0,10Z" fill="#ffc861"/><path d="M0,8 C-3,2 -2,-3 0,-8 C2,-3 3,2 0,8Z" fill="#fff4cf"/></g></g>
</g>'''

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Rudra Vable, Neverfinished005">
<defs><style>
{FONTS}
.tw{{animation:tw 3s ease-in-out infinite}}@keyframes tw{{0%,100%{{opacity:.12}}50%{{opacity:1}}}}
.moon{{animation:moon 8s ease-in-out infinite;transform-origin:880px 150px}}@keyframes moon{{0%,100%{{opacity:.55;transform:scale(1)}}50%{{opacity:.95;transform:scale(1.07)}}}}
.fog1{{animation:f1 40s linear infinite alternate}}.fog2{{animation:f2 56s linear infinite alternate}}
@keyframes f1{{from{{transform:translateX(-200px)}}to{{transform:translateX(200px)}}}}@keyframes f2{{from{{transform:translateX(180px)}}to{{transform:translateX(-220px)}}}}
.bat{{opacity:0;transform:translate(1280px,0);animation:fly 15s linear infinite}}
@keyframes fly{{0%{{opacity:0;transform:translate(1260px,calc(150px + var(--y))) scale(var(--s))}}6%{{opacity:1}}50%{{transform:translate(620px,calc(90px + var(--y))) scale(var(--s))}}94%{{opacity:1}}100%{{opacity:0;transform:translate(-60px,calc(190px + var(--y))) scale(var(--s))}}}}
.wing{{animation:fl .32s ease-in-out infinite alternate;transform-origin:0 0}}@keyframes fl{{from{{transform:scaleY(1)}}to{{transform:scaleY(.35)}}}}
.ff{{animation:ff 7s ease-in-out infinite;opacity:0}}@keyframes ff{{0%,100%{{opacity:0;transform:translate(0,0)}}50%{{opacity:.95;transform:translate(var(--dx),var(--dy))}}}}
.flame{{transform-origin:0 10px;animation:fk 1.1s ease-in-out infinite alternate}}@keyframes fk{{0%{{transform:scale(1,1) rotate(-4deg)}}50%{{transform:scale(.9,1.12) rotate(4deg)}}100%{{transform:scale(1.06,.94) rotate(-2deg)}}}}
.lh{{animation:lh 1.7s ease-in-out infinite alternate}}@keyframes lh{{from{{opacity:.22}}to{{opacity:.55}}}}
.sway{{transform-origin:0 0;animation:sw 6s ease-in-out infinite}}@keyframes sw{{0%,100%{{transform:skewX(0)}}50%{{transform:skewX(-1.4deg)}}}}
.eye{{animation:ey 5s ease-in-out infinite}}@keyframes ey{{0%,93%,100%{{opacity:1}}96%{{opacity:.05}}}}
.rise{{opacity:0;animation:ri 1.4s cubic-bezier(.2,.8,.2,1) .3s forwards}}@keyframes ri{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:none}}}}
.shine{{animation:sh 7s ease-in-out 2.2s infinite}}@keyframes sh{{0%,100%{{opacity:0;transform:translateX(0)}}12%{{opacity:.8}}34%{{opacity:0;transform:translateX(520px)}}}}
.sub{{opacity:0;animation:fi 1.2s ease 1.3s forwards}}@keyframes fi{{to{{opacity:1}}}}
.t1{{width:0;animation:ty 3.6s steps(30) 2.4s forwards}}.t2{{width:0;animation:ty2 3.4s steps(28) 6.4s forwards}}
@keyframes ty{{to{{width:420px}}}}@keyframes ty2{{to{{width:410px}}}}
.caret{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}
</style>
<filter id="blur" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2400" height="1600"><feGaussianBlur stdDeviation="26"/></filter>
<filter id="blur2" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2400" height="1600"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .16 0"/></filter>
<radialGradient id="mg" cx="42%" cy="38%" r="70%"><stop offset="0" stop-color="#fffaf0"/><stop offset=".6" stop-color="{BONE}"/><stop offset="1" stop-color="#9d9784"/></radialGradient>
<radialGradient id="mglow"><stop offset="0" stop-color="{BONE}" stop-opacity=".5"/><stop offset="1" stop-color="{BONE}" stop-opacity="0"/></radialGradient>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050507"/><stop offset=".7" stop-color="#101016"/><stop offset="1" stop-color="#0b0b0e"/></linearGradient>
<linearGradient id="fogg" x1="0" x2="1"><stop offset="0" stop-color="{BONE}" stop-opacity="0"/><stop offset=".5" stop-color="{BONE}" stop-opacity=".16"/><stop offset="1" stop-color="{BONE}" stop-opacity="0"/></linearGradient>
<linearGradient id="left" x1="0" x2="1"><stop offset="0" stop-color="{INK}" stop-opacity=".9"/><stop offset=".5" stop-color="{INK}" stop-opacity=".35"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>
<linearGradient id="streak" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="txt" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="{BONE}"/><stop offset="1" stop-color="#a8a291"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="6"/></clipPath>
<clipPath id="k1"><rect class="t1" x="70" y="360" height="30"/></clipPath><clipPath id="k2"><rect class="t2" x="70" y="398" height="30"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g>{stars}</g>
<circle class="moon" cx="880" cy="150" r="190" fill="url(#mglow)"/>
<g><circle cx="880" cy="150" r="82" fill="url(#mg)"/>
<g fill="#000" opacity=".13"><circle cx="855" cy="128" r="14"/><circle cx="902" cy="170" r="19"/><circle cx="872" cy="186" r="8"/><circle cx="910" cy="124" r="9"/></g></g>
<g>{bats}</g>
<path d="M0,{H} L0,430 Q160,396 330,424 T640,420 T960,428 T1200,414 L1200,{H}Z" fill="#050507"/>
{tree}{grave(700,452,1.1)}{grave(760,458,.8)}{grave(640,460,.7)}
<path d="M0,{H} L0,470 Q220,448 420,470 T820,466 T1200,462 L1200,{H}Z" fill="#000"/>
{figure}
<g class="fog1"><ellipse cx="760" cy="470" rx="540" ry="44" fill="url(#fogg)" filter="url(#blur)"/></g>
<g class="fog2"><ellipse cx="520" cy="430" rx="560" ry="36" fill="url(#fogg)" filter="url(#blur)"/></g>
<rect width="{W}" height="{H}" fill="url(#left)"/>
<g>{flies}</g>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".5"/>
{frame(W, H)}
<g class="rise">
<text x="68" y="200" font-family="UC,'Times New Roman',serif" font-size="104" fill="url(#txt)">Rudra Vable</text>
<g transform="skewX(-16)"><rect class="shine" x="30" y="100" width="70" height="120" fill="url(#streak)" opacity="0"/></g>
</g>
<g class="sub"><path d="M72,226 H300" stroke="{BONE}" stroke-opacity=".7"/><g transform="translate(312 226)">{quatrefoil(8)}</g><path d="M326,226 H420" stroke="{BONE}" stroke-opacity=".4"/>
<text x="72" y="276" font-family="PO,Georgia,serif" font-size="30" fill="{DIM}" letter-spacing="4">@Neverfinished005</text>
<text x="72" y="316" font-family="'Courier New',monospace" font-size="14" fill="#7d7868" letter-spacing="4">SPAWNS AT NIGHT · CODES · EXPLORES</text></g>
<g clip-path="url(#k1)"><text x="70" y="382" font-family="'Courier New',monospace" font-size="19" fill="{BONE}">&gt; python · ml · sql · dsa · mobile</text></g>
<g clip-path="url(#k2)"><text x="70" y="420" font-family="'Courier New',monospace" font-size="16" fill="{DIM}">// admiring stars &amp; nature</text></g>
<rect class="caret" x="70" y="438" width="10" height="3" fill="{BONE}"/>
</g></svg>'''
open(os.path.join(A, 'g-banner.svg'), 'w', encoding='utf-8').write(banner)

# ================================================================== SECTION HEADERS
def header(slug, label, sub):
    hw, hh = 1200, 96
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {hw} {hh}" width="100%" role="img" aria-label="{label}"><defs><style>{FONTS}
.sh{{animation:sh 6s ease-in-out infinite}}@keyframes sh{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
.sw{{animation:sw 5s ease-in-out infinite}}@keyframes sw{{0%{{transform:translateX(-300px);opacity:0}}20%{{opacity:.8}}60%{{opacity:0;transform:translateX(900px)}}100%{{opacity:0;transform:translateX(900px)}}}}
</style><linearGradient id="st" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{BONE}" stop-opacity="0"/><stop offset="1" stop-color="{BONE}" stop-opacity=".8"/></linearGradient>
<linearGradient id="r" x1="1" x2="0"><stop offset="0" stop-color="{BONE}" stop-opacity="0"/><stop offset="1" stop-color="{BONE}" stop-opacity=".8"/></linearGradient></defs>
<rect x="40" y="46" width="410" height="1.4" fill="url(#l)"/><rect x="750" y="46" width="410" height="1.4" fill="url(#r)"/>
<rect x="40" y="53" width="380" height="1" fill="url(#l)" opacity=".4"/><rect x="780" y="53" width="380" height="1" fill="url(#r)" opacity=".4"/>
<g class="sh"><g transform="translate(456 48)">{quatrefoil(9)}</g><g transform="translate(744 48)">{quatrefoil(9)}</g></g>
<text x="600" y="62" text-anchor="middle" font-family="UC,'Times New Roman',serif" font-size="46" fill="{BONE}">{label}</text>
<text x="600" y="86" text-anchor="middle" font-family="'Courier New',monospace" font-size="11" fill="{DIM}" letter-spacing="6">{sub}</text>
<g transform="skewX(-18)"><rect class="sw" x="0" y="20" width="60" height="60" fill="url(#st)" opacity="0"/></g></svg>'''
for slug, label, sub in [('about', 'The Dossier', 'ABOUT THE WANDERER'), ('arsenal', 'The Arsenal', 'LANGUAGES · TOOLS'), ('relics', 'Relics', 'THINGS I BUILT'), ('vitals', 'Vital Signs', 'ACTIVITY · STATS')]:
    open(os.path.join(A, f'g-{slug}.svg'), 'w', encoding='utf-8').write(header(slug, label, sub))

# ================================================================== FOOTER
fw, fh = 1200, 120
foot = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fw} {fh}" width="100%"><defs><style>{FONTS}.fl{{animation:fl 4s ease-in-out infinite}}@keyframes fl{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}</style></defs>
{scallop(60, 1140, 20, 36, 16)}{scallop(60, 1140, 28, 36, 16)}
<g class="fl"><g transform="translate(600 20)">{quatrefoil(10)}</g></g>
<text x="600" y="84" text-anchor="middle" font-family="UC,'Times New Roman',serif" font-size="30" fill="{BONE}">stay nocturnal</text>
<text x="600" y="108" text-anchor="middle" font-family="'Courier New',monospace" font-size="11" fill="{DIM}" letter-spacing="6">NEVERFINISHED · NEVER DONE</text></svg>'''
open(os.path.join(A, 'g-footer.svg'), 'w', encoding='utf-8').write(foot)

# ================================================================== ACTIVITY GRAPH (monochrome)
cal = json.load(open(os.path.join(ROOT, 'tools', 'cal.json'), encoding='utf-8'))['data']['viewer']['contributionsCollection']['contributionCalendar']
weeks, total = cal['weeks'], cal['totalContributions']
mx = max(d['contributionCount'] for w in weeks for d in w['contributionDays']) or 1
cell, gap, left, top = 15, 4, 56, 112
GW = left + len(weeks) * (cell + gap) + 36
GH = top + 7 * (cell + gap) + 66
shade = lambda n: '#17171c' if n == 0 else '#4a4a52' if n / mx < .25 else '#86827a' if n / mx < .5 else '#c9c3b1' if n / mx < .8 else '#ffffff'
cells = ''
for wi, w in enumerate(weeks):
    for d in w['contributionDays']:
        di = (datetime.date.fromisoformat(d['date']).weekday() + 1) % 7
        n = d['contributionCount']
        cells += f'<rect x="{left+wi*(cell+gap)}" y="{top+di*(cell+gap)}" width="{cell}" height="{cell}" rx="3" fill="{shade(n)}"{" filter=\"url(#g)\"" if n else ""} class="c" style="animation-delay:{wi*.02:.2f}s"><title>{d["date"]}: {n}</title></rect>'
mn, months, last, lw = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], '', None, -9
for wi, w in enumerate(weeks):
    m = w['contributionDays'][0]['date'][5:7]
    if m != last and wi - lw >= 3:
        lw = wi; months += f'<text x="{left+wi*(cell+gap)}" y="{top-12}" font-family="\'Courier New\',monospace" font-size="11" fill="{DIM}">{mn[int(m)]}</text>'
    last = m
leg = ''.join(f'<rect x="{GW-200+i*20}" y="{GH-42}" width="14" height="14" rx="3" fill="{c}"/>' for i, c in enumerate(['#17171c', '#4a4a52', '#86827a', '#c9c3b1', '#ffffff']))
act = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW} {GH}" width="100%" role="img" aria-label="{total} contributions in the last year"><defs><style>{FONTS}.c{{opacity:0;transform-box:fill-box;transform-origin:center;animation:p .5s ease forwards}}@keyframes p{{from{{opacity:0;transform:scale(.3)}}to{{opacity:1}}}}</style>
<filter id="g" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="{GW}" height="{GH}" fill="{INK}" stroke="{BONE}" stroke-opacity=".5" rx="4"/>
<rect x="9" y="9" width="{GW-18}" height="{GH-18}" fill="none" stroke="{BONE}" stroke-opacity=".22" stroke-dasharray="1 5" rx="2"/>
<text x="{left}" y="56" font-family="UC,serif" font-size="40" fill="{BONE}">Graveyard Shift</text>
<text x="{left}" y="82" font-family="'Courier New',monospace" font-size="13" fill="{DIM}" letter-spacing="3">{total} CONTRIBUTIONS · LAST 12 MONTHS</text>
{months}{cells}
<text x="{GW-214}" y="{GH-31}" text-anchor="end" font-family="'Courier New',monospace" font-size="11" fill="{DIM}">less</text>{leg}
<text x="{GW-92}" y="{GH-31}" font-family="'Courier New',monospace" font-size="11" fill="{DIM}">more</text></svg>'''
open(os.path.join(A, 'g-activity.svg'), 'w', encoding='utf-8').write(act)
print('ok', {n: os.path.getsize(os.path.join(A, n)) // 1024 for n in os.listdir(A) if n.startswith('g-')})
