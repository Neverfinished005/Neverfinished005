"""Generates the animated dark banner and the contribution graph used by the profile README.
Run:  gh api graphql -f query='...' > tools/cal.json   then   python tools/make_profile_art.py
"""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'assets')
random.seed(7)

BG1, BG2 = '#07060d', '#140a1f'
PINK, PINK2, OCHRE, GOLD, CREAM = '#e9739f', '#b02a66', '#c08f14', '#e3b04b', '#f4eee6'

# ----------------------------------------------------------------------------- HERO
W, H = 1200, 420
stars = ''.join(
    f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,H-120)}" r="{random.choice([.7,.9,1.2,1.6])}" fill="#fff" class="tw" style="animation-delay:{random.random()*4:.2f}s;animation-duration:{2+random.random()*3:.2f}s"/>'
    for _ in range(90))
embers = ''.join(
    f'<circle cx="{random.randint(40,W-40)}" cy="{H-20}" r="{random.choice([1.4,1.8,2.4])}" fill="{random.choice([PINK,GOLD,OCHRE])}" class="em" style="animation-delay:{random.random()*9:.2f}s;animation-duration:{7+random.random()*6:.2f}s;--dx:{random.randint(-60,60)}px"/>'
    for _ in range(34))
beads = ''.join(f'<circle cx="0" cy="-158" r="{3 if i%2==0 else 1.6}" fill="{GOLD if i%2==0 else PINK}" transform="rotate({i*10})"/>' for i in range(36))
petals = ''.join(
    f'<path d="M0,0 C26,-34 22,-92 0,-122 C-22,-92 -26,-34 0,0Z" transform="rotate({i*22.5})" fill="url(#pl)" stroke="{PINK}" stroke-opacity=".55" stroke-width="1"/>'
    for i in range(16))
petals2 = ''.join(
    f'<path d="M0,0 C20,-26 16,-68 0,-90 C-16,-68 -20,-26 0,0Z" transform="rotate({i*30+15})" fill="url(#pl2)" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>'
    for i in range(12))

hero = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Rudra Vable: Alpha.Kore builder">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
  <radialGradient id="moon" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{PINK}" stop-opacity=".55"/><stop offset=".55" stop-color="{PINK2}" stop-opacity=".18"/><stop offset="1" stop-color="{PINK2}" stop-opacity="0"/></radialGradient>
  <linearGradient id="pl" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#7a1646"/><stop offset=".55" stop-color="{PINK2}"/><stop offset="1" stop-color="#f6b3cb"/></linearGradient>
  <linearGradient id="pl2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#5e1034"/><stop offset=".6" stop-color="#d44a84"/><stop offset="1" stop-color="#ffd0e0"/></linearGradient>
  <linearGradient id="ink" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120b1c"/><stop offset="1" stop-color="#000"/></linearGradient>
  <linearGradient id="txt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CREAM}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="22"/></filter>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  .tw{{animation:tw 3s ease-in-out infinite}} @keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
  .em{{animation:em 9s linear infinite;opacity:0}} @keyframes em{{0%{{opacity:0;transform:translate(0,0)}}15%{{opacity:.9}}100%{{opacity:0;transform:translate(var(--dx),-360px)}}}}
  .spin{{transform-origin:0 0;animation:spin 80s linear infinite}} .spin.r{{animation-direction:reverse;animation-duration:140s}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  .breathe{{animation:br 6s ease-in-out infinite;transform-origin:0 0}} @keyframes br{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.045)}}}}
  .name{{animation:nm 4s ease-in-out infinite}} @keyframes nm{{0%,100%{{filter:drop-shadow(0 0 6px rgba(233,115,159,.45))}}50%{{filter:drop-shadow(0 0 18px rgba(227,176,75,.85))}}}}
  .fade1{{opacity:0;animation:fi 1s ease .4s forwards}} .fade2{{opacity:0;animation:fi 1s ease 1.2s forwards}} .fade3{{opacity:0;animation:fi 1s ease 2s forwards}}
  @keyframes fi{{to{{opacity:1}}}}
  .scan{{animation:sc 6s linear infinite}} @keyframes sc{{0%{{transform:translateY(-20px)}}100%{{transform:translateY({H+20}px)}}}}
  .blink{{animation:bl 1s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}
  .cloak{{animation:cl 5s ease-in-out infinite;transform-origin:50% 100%}} @keyframes cl{{0%,100%{{transform:skewX(0)}}50%{{transform:skewX(-1.6deg)}}}}
  .eye{{animation:ey 4s ease-in-out infinite}} @keyframes ey{{0%,92%,100%{{opacity:1}}95%{{opacity:.1}}}}
</style>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <g>{stars}</g>
  <ellipse cx="900" cy="200" rx="360" ry="260" fill="url(#moon)"/>

  <g transform="translate(900 205)">
    <g class="spin r"><circle r="188" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-dasharray="2 7"/>{beads}</g>
    <g class="breathe">
      <g class="spin">{petals}</g>
      <g class="spin r">{petals2}</g>
      <circle r="38" fill="#2a0d19" stroke="{GOLD}" stroke-width="2"/><circle r="30" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-dasharray="1.5 4"/>
    </g>
  </g>

  <path d="M0,{H} L0,330 Q120,300 230,330 T470,325 T700,335 T1000,328 T1200,320 L1200,{H}Z" fill="#05040a"/>
  <path d="M0,{H} L0,368 Q200,345 380,366 T760,362 T1200,356 L1200,{H}Z" fill="#000"/>

  <g transform="translate(1085 232)"><g class="cloak" filter="url(#glow)">
    <path d="M0,-92 C-26,-92 -42,-70 -44,-44 C-46,-20 -58,2 -66,34 C-72,60 -80,86 -84,118 L84,118 C80,86 72,60 66,34 C58,2 46,-20 44,-44 C42,-70 26,-92 0,-92Z" fill="url(#ink)" stroke="{PINK}" stroke-opacity=".55" stroke-width="1.4"/>
    <path d="M0,-70 C-18,-70 -28,-54 -28,-36 C-28,-22 -18,-12 0,-12 C18,-12 28,-22 28,-36 C28,-54 18,-70 0,-70Z" fill="#000"/>
    <g class="eye"><ellipse cx="-9" cy="-40" rx="5" ry="2.4" fill="{GOLD}"/><ellipse cx="9" cy="-40" rx="5" ry="2.4" fill="{GOLD}"/></g>
    <path d="M-44,-44 C-30,-30 30,-30 44,-44" fill="none" stroke="{GOLD}" stroke-opacity=".5"/>
  </g></g>

  <g>{embers}</g>
  <rect class="scan" x="0" y="0" width="{W}" height="2" fill="{PINK}" opacity=".12"/>

  <g class="name fade1">
    <text x="64" y="168" font-family="Georgia,'Times New Roman',serif" font-size="68" font-weight="700" fill="url(#txt)" letter-spacing="2">RUDRA VABLE</text>
  </g>
  <g class="fade2">
    <rect x="64" y="188" width="150" height="3" fill="{OCHRE}"/>
    <text x="64" y="232" font-family="Verdana,Arial,sans-serif" font-size="19" fill="{CREAM}" letter-spacing="4">BUILDER AT ALPHA.KORE</text>
  </g>
  <g class="fade3">
    <text x="64" y="272" font-family="'Courier New',monospace" font-size="17" fill="{PINK}" opacity=".95">&gt; software · automation · ai<tspan class="blink" fill="{GOLD}">_</tspan></text>
    <text x="64" y="306" font-family="'Courier New',monospace" font-size="15" fill="#9d93ad">// Vadodara, India</text>
  </g>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="{OCHRE}" stroke-opacity=".45"/>
</g>
</svg>'''
open(os.path.join(A, 'hero.svg'), 'w', encoding='utf-8').write(hero)

# ----------------------------------------------------------------------------- CONTRIBUTION GRAPH
cal = json.load(open(os.path.join(ROOT, 'tools', 'cal.json'), encoding='utf-8'))['data']['viewer']['contributionsCollection']['contributionCalendar']
weeks, total = cal['weeks'], cal['totalContributions']
mx = max((d['contributionCount'] for w in weeks for d in w['contributionDays']), default=1) or 1
cell, gap, left, top = 16, 4, 56, 104
GW = left + len(weeks) * (cell + gap) + 40
GH = top + 7 * (cell + gap) + 70
def colour(n):
    if n == 0: return '#1b1428'
    t = n / mx
    return '#6e2a54' if t < .25 else '#b02a66' if t < .5 else '#e9739f' if t < .8 else '#ffd0e0'
cells = ''
for wi, w in enumerate(weeks):
    for d in w['contributionDays']:
        di = __import__('datetime').date.fromisoformat(d['date']).weekday()  # Mon=0
        di = (di + 1) % 7                                               # Sun=0
        n = d['contributionCount']
        x, y = left + wi * (cell + gap), top + di * (cell + gap)
        glow = ' filter="url(#g)"' if n else ''
        delay = f'{(wi*0.018):.2f}'
        cells += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{colour(n)}"{glow} class="c" style="animation-delay:{delay}s"><title>{d["date"]}: {n} contribution{"s" if n!=1 else ""}</title></rect>'
months = ''
last = None
lastwi = -9
for wi, w in enumerate(weeks):
    m = w['contributionDays'][0]['date'][5:7]
    if m != last and wi - lastwi >= 3:
        lastwi = wi
        months += f'<text x="{left + wi*(cell+gap)}" y="{top-14}" font-family="Verdana,Arial,sans-serif" font-size="12" fill="#9d93ad">{["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(m)]}</text>'
        last = m
    elif m != last:
        last = m
days = ''.join(f'<text x="{left-12}" y="{top + i*(cell+gap) + 12}" text-anchor="end" font-family="Verdana,Arial,sans-serif" font-size="11" fill="#9d93ad">{n}</text>' for i, n in [(1,'Mon'),(3,'Wed'),(5,'Fri')])
leg = ''.join(f'<rect x="{GW-210+i*22}" y="{GH-44}" width="16" height="16" rx="4" fill="{c}"/>' for i, c in enumerate(['#1b1428','#6e2a54','#b02a66','#e9739f','#ffd0e0']))
graph = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW} {GH}" width="100%" role="img" aria-label="{total} contributions in the last year">
<defs><linearGradient id="gb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
<filter id="g" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>.c{{opacity:0;animation:pop .5s ease forwards}}@keyframes pop{{from{{opacity:0;transform:scale(.4)}}to{{opacity:1}}}}.c{{transform-box:fill-box;transform-origin:center}}</style>
<rect width="{GW}" height="{GH}" rx="16" fill="url(#gb)" stroke="{OCHRE}" stroke-opacity=".4"/>
<text x="{left}" y="40" font-family="Georgia,serif" font-size="24" font-weight="700" fill="{CREAM}">Activity</text>
<text x="{left}" y="62" font-family="Verdana,Arial,sans-serif" font-size="13" fill="{PINK}">{total} contributions in the last year</text>
{months}{days}{cells}
<text x="{GW-226}" y="{GH-31}" text-anchor="end" font-family="Verdana,Arial,sans-serif" font-size="11" fill="#9d93ad">less</text>{leg}
<text x="{GW-92}" y="{GH-31}" font-family="Verdana,Arial,sans-serif" font-size="11" fill="#9d93ad">more</text>
</svg>'''
open(os.path.join(A, 'activity.svg'), 'w', encoding='utf-8').write(graph)

# ----------------------------------------------------------------------------- SECTION DIVIDER
div = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 28" width="100%"><defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{PINK2}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{PINK2}" stop-opacity="0"/></linearGradient></defs>
<style>.dm{{animation:dm 3s ease-in-out infinite;transform-origin:600px 14px}}@keyframes dm{{0%,100%{{transform:rotate(45deg) scale(1)}}50%{{transform:rotate(225deg) scale(1.3)}}}}</style>
<rect x="60" y="13" width="1080" height="2" fill="url(#d)"/><rect class="dm" x="594" y="8" width="12" height="12" fill="{GOLD}" transform="rotate(45 600 14)"/></svg>'''
open(os.path.join(A, 'divider-dark.svg'), 'w', encoding='utf-8').write(div)
print('ok', total, GW, GH)
