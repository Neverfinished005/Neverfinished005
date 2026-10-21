"""Animated image-based profile banner built from the Alpha.Kore site artwork.
python tools/make_hero_image.py   (needs Pillow; reads ../New folder artwork path below)
"""
import base64, io, os, random
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r'C:\Users\ADMIN\Downloads\New folder\assets\alphakore_hero_v2.jpg'
random.seed(11)

img = Image.open(SRC).convert('RGB')
buf = io.BytesIO(); img.save(buf, 'JPEG', quality=80, optimize=True)
IMG = base64.b64encode(buf.getvalue()).decode()
FONT = base64.b64encode(open(os.path.join(ROOT, 'tools', 'rozha-sub.woff'), 'rb').read()).decode()

W, H = 1200, 560
INK, CREAM, GOLD, OCHRE, PINK = '#07060a', '#f1e8d8', '#e3b04b', '#c08f14', '#e9739f'

# picture placement: cover the frame, keep the figure on the right-centre
iw, ih = 1024, 571
sc = 1.12 * max(W / iw, H / ih)
dw, dh = iw * sc, ih * sc
ix, iy = W - dw + 40, (H - dh) / 2

dust = ''.join(
    f'<circle cx="{random.randint(30,W-30)}" cy="{random.randint(60,H-60)}" r="{random.choice([.8,1.1,1.5,2])}" fill="{random.choice([CREAM,GOLD])}" class="dust" style="animation-delay:{random.random()*10:.1f}s;animation-duration:{9+random.random()*9:.1f}s;--dx:{random.randint(-50,50)}px;--dy:{random.randint(-120,-30)}px"/>'
    for _ in range(46))
birds = ''.join(
    f'<g class="bird" style="animation-delay:{i*1.7:.1f}s;animation-duration:{16+i*2.2:.1f}s;--y:{random.randint(-30,30)}px"><path class="wing" d="M0,0 q7,-9 14,0 q7,-9 14,0" fill="none" stroke="{CREAM}" stroke-width="1.6" stroke-linecap="round" style="animation-delay:{i*.13:.2f}s"/></g>'
    for i in range(9))

# carved corner ornament (quarter mandala + curl), drawn once and mirrored
def petals(n, l, w, op):
    return ''.join(f'<path d="M0,0 C{w},{-l*.3} {w*.8},{-l*.78} 0,{-l} C{-w*.8},{-l*.78} {-w},{-l*.3} 0,0Z" transform="rotate({i*360/n})" fill="none" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1"/>' for i in range(n))
corner = f'''<g>{petals(12,46,12,.95)}{petals(12,30,9,.7)}<circle r="4" fill="{GOLD}"/><circle r="52" fill="none" stroke="{GOLD}" stroke-opacity=".6"/>
<path d="M60,0 H190 M0,60 V150" stroke="{GOLD}" stroke-opacity=".7"/><circle cx="196" cy="0" r="3" fill="{GOLD}"/><circle cx="0" cy="156" r="3" fill="{GOLD}"/></g>'''
M = 26
frame = f'''<rect x="{M}" y="{M}" width="{W-2*M}" height="{H-2*M}" fill="none" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.6"/>
<rect x="{M+9}" y="{M+9}" width="{W-2*M-18}" height="{H-2*M-18}" fill="none" stroke="{OCHRE}" stroke-opacity=".5" stroke-dasharray="2 6"/>
<g transform="translate({M},{M})">{corner}</g>
<g transform="translate({W-M},{M}) scale(-1,1)">{corner}</g>
<g transform="translate({M},{H-M}) scale(1,-1)">{corner}</g>
<g transform="translate({W-M},{H-M}) scale(-1,-1)">{corner}</g>
<g transform="translate({W/2},{M})"><path d="M-70,0 H70" stroke="{GOLD}" stroke-opacity=".6"/><path d="M0,-2 L12,10 L0,22 L-12,10Z" fill="{INK}" stroke="{GOLD}"/><circle cy="10" r="3" fill="{GOLD}"/></g>
<g transform="translate({W/2},{H-M})"><path d="M-70,0 H70" stroke="{GOLD}" stroke-opacity=".6"/><path d="M0,2 L12,-10 L0,-22 L-12,-10Z" fill="{INK}" stroke="{GOLD}"/><circle cy="-10" r="3" fill="{GOLD}"/></g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Rudra Vable, builder at Alpha.Kore">
<defs>
<style>
@font-face{{font-family:'RozhaE';src:url(data:font/woff;base64,{FONT}) format('woff')}}
.kb{{animation:kb 26s ease-in-out infinite alternate;transform-origin:78% 62%}} @keyframes kb{{from{{transform:scale(1)}}to{{transform:scale(1.13) translate(-14px,-6px)}}}}
.mist1{{animation:m1 34s linear infinite alternate}} .mist2{{animation:m2 48s linear infinite alternate}}
@keyframes m1{{from{{transform:translateX(-160px)}}to{{transform:translateX(160px)}}}} @keyframes m2{{from{{transform:translateX(140px)}}to{{transform:translateX(-180px)}}}}
.sun{{animation:sun 7s ease-in-out infinite;transform-origin:760px 360px}} @keyframes sun{{0%,100%{{opacity:.55;transform:scale(1)}}50%{{opacity:1;transform:scale(1.12)}}}}
.dust{{animation:dust 12s linear infinite;opacity:0}} @keyframes dust{{0%{{opacity:0;transform:translate(0,0)}}20%{{opacity:.85}}100%{{opacity:0;transform:translate(var(--dx),var(--dy))}}}}
.bird{{transform:translate(-80px,150px);animation:fly 18s linear infinite;opacity:0}}
@keyframes fly{{0%{{opacity:0;transform:translate(560px,calc(150px + var(--y)))}}8%{{opacity:.9}}90%{{opacity:.8}}100%{{opacity:0;transform:translate(1220px,calc(60px + var(--y)))}}}}
.wing{{animation:flap .5s ease-in-out infinite alternate;transform-origin:14px 0}} @keyframes flap{{from{{transform:scaleY(1)}}to{{transform:scaleY(-.55)}}}}
.title{{opacity:0;animation:rise 1.2s cubic-bezier(.2,.8,.2,1) .4s forwards}} @keyframes rise{{from{{opacity:0;transform:translateY(22px)}}to{{opacity:1;transform:none}}}}
.glint{{animation:glint 6s ease-in-out 2s infinite}} @keyframes glint{{0%,100%{{opacity:0;transform:translateX(0)}}15%{{opacity:.9}}30%{{opacity:0;transform:translateX(560px)}}}}
.rule{{transform-origin:0 0;transform:scaleX(0);animation:rule 1.1s ease 1.2s forwards}} @keyframes rule{{to{{transform:scaleX(1)}}}}
.sub{{opacity:0;animation:fi 1s ease 1.5s forwards}} @keyframes fi{{to{{opacity:1}}}}
.type1{{animation:t1 4s steps(34) 2.3s forwards;width:0}} @keyframes t1{{to{{width:400px}}}}
.type2{{animation:t1b 3s steps(29) 6.5s forwards;width:0}} @keyframes t1b{{to{{width:340px}}}}
.caret{{animation:bl 1s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}
.flame{{transform-origin:50% 100%;animation:fl 1.4s ease-in-out infinite alternate}} @keyframes fl{{0%{{transform:scale(1,1) rotate(-3deg)}}50%{{transform:scale(.92,1.1) rotate(3deg)}}100%{{transform:scale(1.05,.95) rotate(-1deg)}}}}
.halo{{animation:halo 2.4s ease-in-out infinite alternate}} @keyframes halo{{from{{opacity:.4}}to{{opacity:.95}}}}
.pulse{{animation:pul 5s ease-in-out infinite}} @keyframes pul{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
</style>
<filter id="ink" color-interpolation-filters="sRGB">
  <feColorMatrix type="saturate" values=".12"/>
  <feComponentTransfer><feFuncR type="linear" slope=".9" intercept="0"/><feFuncG type="linear" slope=".84" intercept="-.01"/><feFuncB type="linear" slope=".76" intercept="-.01"/></feComponentTransfer>
</filter>
<filter id="blur" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2400" height="1600"><feGaussianBlur stdDeviation="28"/></filter>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="left" x1="0" x2="1"><stop offset="0" stop-color="{INK}" stop-opacity=".97"/><stop offset=".42" stop-color="{INK}" stop-opacity=".86"/><stop offset=".78" stop-color="{INK}" stop-opacity=".12"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>
<linearGradient id="bot" x1="0" y1="0" x2="0" y2="1"><stop offset=".62" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}" stop-opacity=".95"/></linearGradient>
<radialGradient id="vig" cx="55%" cy="50%" r="75%"><stop offset=".5" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}" stop-opacity=".9"/></radialGradient>
<radialGradient id="sunc"><stop offset="0" stop-color="{GOLD}" stop-opacity=".7"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<linearGradient id="txt" x1="0" x2="1"><stop offset="0" stop-color="{CREAM}"/><stop offset=".6" stop-color="{GOLD}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="mist" x1="0" x2="1"><stop offset="0" stop-color="{CREAM}" stop-opacity="0"/><stop offset=".5" stop-color="{CREAM}" stop-opacity=".16"/><stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<clipPath id="c1"><rect class="type1" x="64" y="316" height="30"/></clipPath>
<clipPath id="c2"><rect class="type2" x="64" y="354" height="26"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g class="kb"><image x="{ix:.0f}" y="{iy:.0f}" width="{dw:.0f}" height="{dh:.0f}" href="data:image/jpeg;base64,{IMG}" xlink:href="data:image/jpeg;base64,{IMG}" filter="url(#ink)" preserveAspectRatio="none"/></g>
  <circle class="sun" cx="760" cy="360" r="140" fill="url(#sunc)" style="mix-blend-mode:screen"/>
  <g class="mist1"><ellipse cx="760" cy="430" rx="520" ry="46" fill="url(#mist)" filter="url(#blur)"/></g>
  <g class="mist2"><ellipse cx="600" cy="360" rx="560" ry="38" fill="url(#mist)" filter="url(#blur)"/></g>
  <rect width="{W}" height="{H}" fill="url(#left)"/><rect width="{W}" height="{H}" fill="url(#bot)"/><rect width="{W}" height="{H}" fill="url(#vig)"/>
  <g>{birds}</g>
  <g>{dust}</g>

  <g transform="translate(1068 452)">
    <circle class="halo" cx="0" cy="-22" r="44" fill="{GOLD}" opacity=".45" filter="url(#blur)"/>
    <path d="M-28,0 Q-24,16 0,18 Q24,16 28,0 Q10,6 0,6 Q-10,6 -28,0Z" fill="#a8641c" stroke="#3b1f08"/>
    <path d="M-28,0 Q0,-6 28,0" fill="none" stroke="#f3c47a"/>
    <g class="flame"><path d="M0,-3 C-9,-14 -6,-26 0,-38 C6,-26 9,-14 0,-3Z" fill="#ffb02e"/><path d="M0,-5 C-4,-13 -3,-22 0,-29 C3,-22 4,-13 0,-5Z" fill="#fff1c0"/></g>
  </g>

  {frame}

  <g class="title">
    <text x="64" y="176" font-family="RozhaE,'Rozha One',Georgia,serif" font-size="78" fill="url(#txt)" letter-spacing="3">RUDRA VABLE</text>
    <rect class="glint" x="64" y="112" width="26" height="86" fill="#fff" opacity="0" transform="skewX(-18)" style="mix-blend-mode:overlay"/>
  </g>
  <rect class="rule" x="64" y="200" width="170" height="3" fill="{OCHRE}"/>
  <g class="sub">
    <text x="64" y="250" font-family="RozhaE,'Rozha One',Georgia,serif" font-size="21" fill="{CREAM}" letter-spacing="7">BUILDER AT ALPHA.KORE</text>
    <text x="64" y="284" font-family="Verdana,Arial,sans-serif" font-size="13" fill="#a69b8c" letter-spacing="3">VADODARA · INDIA</text>
  </g>
  <g clip-path="url(#c1)"><text x="64" y="338" font-family="'Courier New',monospace" font-size="19" fill="{PINK}">&gt; software · automation · ai</text></g>
  <g clip-path="url(#c2)"><text x="64" y="374" font-family="'Courier New',monospace" font-size="16" fill="{GOLD}">// turning sparks into impact</text></g>
  <rect class="caret" x="64" y="394" width="10" height="3" fill="{GOLD}"/>
</g>
</svg>'''
out = os.path.join(ROOT, 'assets', 'hero-image.svg')
open(out, 'w', encoding='utf-8').write(svg)
print('ok', os.path.getsize(out) // 1024, 'KB')
