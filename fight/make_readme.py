#!/usr/bin/env python3
"""Generates the animated README header. Everything is native SVG animation baked
ahead of time, so GitHub can render it inside an <img> with no JavaScript.
Usage: python3 make_readme.py <dir with zodiak-italic-var.woff2 and general-sans-normal-var.woff2>
Output: readme-dark.svg, readme-light.svg next to this file."""
import math, pathlib, random, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

random.seed(7)
FONTS = pathlib.Path(sys.argv[1]); HERE = pathlib.Path(__file__).parent
W, H, T = 830, 310, 26.0
FLOOR = 298; HIP = FLOOR - 29
TOMATO, PURPLE = '#D9502A', '#8B5CF6'
nt = lambda v: f'{v:.1f}'.rstrip('0').rstrip('.')


class Face:
    def __init__(s, file, wght):
        s.f = instancer.instantiateVariableFont(TTFont(FONTS / file), {'wght': wght})
        s.gs, s.cmap, s.hm = s.f.getGlyphSet(), s.f.getBestCmap(), s.f['hmtx']

    def adv(s, c, size): return s.hm[s.cmap[ord(c)]][0] * size / 1000

    def path(s, c, size, ox, oy):
        k = size / 1000; pen = SVGPathPen(s.gs, ntos=nt)
        s.gs[s.cmap[ord(c)]].draw(TransformPen(pen, (k, 0, 0, -k, ox, oy)))
        return pen.getCommands()


serif, sans = Face('zodiak-italic-var.woff2', 500), Face('general-sans-normal-var.woff2', 500)


class L:
    def __init__(s, c, x, y, size, face, born, line, word):
        s.c, s.face, s.size = c, face, size
        s.w = face.adv(c, size); s.hx, s.hy = x + s.w / 2, y - size * .32
        s.d = face.path(c, size, -s.w / 2, size * .32)
        s.x, s.y, s.vx, s.vy, s.r, s.vr = s.hx, s.hy, 0, 0, 0, 0
        s.born, s.line, s.word = born, line, word; s.free = False; s.keys = []; s.thrown = None


letters = []
def line(text, x, y, size, face, t0, cps, idx):
    word = 0
    for i, c in enumerate(text):
        if c == ' ': x += face.adv(c, size); word += 1; continue
        l = L(c, x, y, size, face, t0 + i / cps, idx, word); letters.append(l); x += l.w
    return x

line("Hi, I'm Rohit", 24, 62, 46, serif, .3, 22, 0)
strike_end = line('Dear hiring manager,', 24, 98, 18, sans, 1.2, 34, 1)
line('This is a README, not a cover letter.', 24, 128, 18, sans, 2.4, 34, 2)
line('Growth engineer, AI engineer, social media strategist.', 24, 158, 18, sans, 3.8, 38, 3)
line('20+ hackathons won. 509 stars on Tastemaker.', 24, 188, 18, sans, 5.4, 34, 4)
finale = []
for l in letters[:0]: pass
n = len(letters); line('Anyway. Hire me.', 410, 262, 38, serif, 21.3, 26, 5); finale = letters[n:]; letters = letters[:n]
nine = [l for l in letters if l.line == 4 and l.word == 3]  # "509"

# --- stickman choreography -------------------------------------------------
P = {  # lean, front arm, elbow, back arm, elbow, front thigh, knee, back thigh, knee
    'stand': (2, 12, 10, -12, 10, 6, -2, -6, 2), 'crouch': (25, 40, 40, -30, 40, 70, -100, -20, -60),
    'run1': (18, 60, 60, -60, 70, 55, -20, -40, -70), 'run2': (18, -60, 70, 60, 60, -40, -70, 55, -20),
    'fly': (0, 150, 10, -150, -10, 20, -20, -20, 20), 'tuck': (0, 60, 90, 40, 90, 100, -120, 90, -120),
    'throw0': (-15, -140, 30, -40, 30, 20, -10, -20, 10), 'throw1': (25, 100, 10, -60, 20, 40, -10, -30, -30),
    'kick': (10, 70, 20, -100, 20, 95, 0, -30, -50), 'hit': (-35, 130, 10, 110, 10, 40, 20, 20, 30),
    'punch1': (20, 90, 0, -50, 90, 30, -20, -30, -20), 'punch2': (20, -50, 90, 90, 0, 30, -20, -30, -20),
    'upper': (-10, 170, 0, -40, 80, 20, -30, -30, -40), 'cast': (0, 140, 20, -140, -20, 8, 0, -8, 0),
    'point': (0, 100, 0, -15, 10, 6, -2, -6, 2), 'wave1': (0, 150, 30, -15, 10, 6, -2, -6, 2),
    'wave2': (0, 150, -30, -15, 10, 6, -2, -6, 2), 'dust': (15, 40, 100, 30, 100, 10, -5, -10, 5),
}
K = [(8.7, 128, HIP + 6, 'crouch', 1), (9.0, 128, 190, 'fly', 1), (9.45, 190, HIP - 14, 'tuck', 1), (9.6, 190, HIP + 4, 'crouch', 1), (9.95, 190, HIP, 'stand', 1),
     (10.55, 190, HIP, 'crouch', 1), (10.8, 190, 215, 'tuck', 1), (11.1, 190, HIP, 'crouch', 1)]
def run(t0, t1, x0, x1, K):
    n = max(2, int((t1 - t0) / .11)); face = 1 if x1 > x0 else -1
    for i in range(n + 1):
        K.append((t0 + (t1 - t0) * i / n, x0 + (x1 - x0) * i / n, HIP - (2 if i % 2 else 0), 'run1' if i % 2 else 'run2', face))
run(11.2, 12.0, 190, 430, K)
K += [(12.1, 430, HIP, 'throw0', 1), (12.3, 430, HIP, 'throw1', 1), (12.6, 430, HIP, 'stand', 1)]
run(12.65, 13.05, 430, 545, K)
K += [(13.15, 560, HIP + 4, 'crouch', 1), (13.42, 590, 150, 'kick', 1), (13.7, 625, 200, 'tuck', 1), (13.95, 640, HIP + 4, 'crouch', 1), (14.15, 640, HIP, 'stand', 1),
      (14.42, 640, HIP, 'stand', 1), (14.55, 600, 240, 'hit', 1), (14.95, 470, HIP - 2, 'hit', 1), (15.2, 470, HIP + 4, 'crouch', 1), (15.4, 470, HIP, 'stand', 1)]
run(15.45, 15.9, 470, 600, K)
K += [(15.95, 605, HIP, 'punch1', 1), (16.1, 605, HIP, 'punch2', 1), (16.25, 608, HIP, 'punch1', 1), (16.42, 608, HIP + 6, 'crouch', 1), (16.6, 615, 225, 'upper', 1),
      (17.0, 618, HIP, 'crouch', 1), (17.25, 618, HIP, 'stand', 1), (17.7, 618, HIP, 'dust', 1), (17.9, 618, HIP, 'stand', 1), (18.1, 618, HIP, 'dust', 1), (18.3, 618, HIP, 'stand', 1)]
run(18.35, 19.15, 618, 330, K)
K += [(19.3, 330, HIP, 'cast', 1), (20.9, 330, HIP, 'cast', 1), (21.15, 330, HIP, 'point', 1)]
for i in range(9):
    K.append((22.0 + i * .22, 330, HIP, 'wave1' if i % 2 else 'wave2', 1))
K.append((24.1, 330, HIP, 'stand', 1))
run(24.15, 24.95, 330, 128, K)
K += [(25.05, 128, HIP + 4, 'crouch', -1), (25.4, 128, HIP + 34, 'crouch', -1)]
ease = lambda u: u * u * (3 - 2 * u)

def stick(t):
    for a, b in zip(K, K[1:]):
        if a[0] <= t <= b[0]:
            u = ease((t - a[0]) / (b[0] - a[0] or 1))
            return a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, [p + (q - p) * u for p, q in zip(P[a[3]], P[b[3]])], (b if u > .5 else a)[4]
    return K[-1][1], K[-1][2], list(P[K[-1][3]]), K[-1][4]

def joints(x, y, p, f):
    lean = math.radians(p[0]); nx, ny = x + 28 * math.sin(lean) * f, y - 28 * math.cos(lean)
    hx, hy = nx + 9 * math.sin(lean) * f, ny - 9 * math.cos(lean)
    def limb(ox, oy, a, b, l):
        a = math.radians(a); ab = a + math.radians(b)
        e = (ox + math.sin(a) * f * l, oy + math.cos(a) * l)
        return e, (e[0] + math.sin(ab) * f * l, e[1] + math.cos(ab) * l)
    aF, aB = limb(nx, ny, p[1], p[2], 13), limb(nx, ny, p[3], p[4], 13)
    lF, lB = limb(x, y, p[5], p[6], 15), limb(x, y, p[7], p[8], 15)
    d = 'M%s %sL%s %s' % (nt(hx), nt(hy), nt(x), nt(y))
    for (e, h), o in ((lF, (x, y)), (lB, (x, y)), (aF, (nx, ny)), (aB, (nx, ny))):
        d += 'M%s %sL%s %sL%s %s' % (nt(o[0]), nt(o[1]), nt(e[0]), nt(e[1]), nt(h[0]), nt(h[1]))
    return d, hx, hy, lF[1], aF[1]

# --- slop card -------------------------------------------------------------
CARD = [(0, 900, 95, 0), (7.4, 900, 95, 0), (7.9, 655, 95, -3), (8.2, 655, 95, 2), (8.5, 655, 95, 0), (12.45, 655, 95, 0), (12.6, 680, 85, 8), (13.0, 660, 95, 0), (13.42, 660, 95, 0),
        (13.65, 745, 62, 22), (14.1, 720, 110, 6), (14.3, 700, 120, -8), (14.44, 640, 232, -4), (14.8, 660, 232, 0), (15.9, 660, 232, 0), (16.0, 672, 228, 5), (16.15, 660, 232, -3), (16.3, 676, 226, 6), (16.55, 662, 232, 0), (16.95, 640, 40, 40), (17.0, 640, 40, 40)]
def card(t):
    for a, b in zip(CARD, CARD[1:]):
        if a[0] <= t <= b[0]:
            u = ease((t - a[0]) / (b[0] - a[0] or 1)); return [p + (q - p) * u for p, q in zip(a[1:], b[1:])]
    return CARD[-1][1:]

# --- physics, one 60Hz step at a time so letters react to the stickman -----
DT = 1 / 60; HOLE = (128, 240); BLAST = 9.0; KEY_EVERY = 5
def blast(x, y, power, radius):
    for l in letters:
        if l.t_hidden: continue
        d = math.hypot(l.x - x, l.y - y)
        if d < radius:
            k = power * (1 - d / radius) * random.uniform(.6, 1.2); a = math.atan2(l.y - y, l.x - x) + random.uniform(-.5, .5)
            l.free = True; l.vx += math.cos(a) * k; l.vy += math.sin(a) * k - 90; l.vr += random.uniform(-14, 14)
for l in letters: l.t_hidden = False
shards = [dict(x=640, y=40, vx=random.uniform(-260, 260), vy=random.uniform(-260, 60), r=0, vr=random.uniform(-12, 12), s=random.uniform(6, 16), c=random.choice(['#6366F1', '#8B5CF6', '#A855F7', '#C084FC']), keys=[]) for _ in range(16)]
step = 0; hits = {BLAST: (HOLE[0], HOLE[1] - 40, 760, 540), 13.42: (620, 200, 200, 130), 14.44: (640, 290, 560, 240), 16.95: (640, 60, 0, 1)}
fired = set(); t = 0
while t < T:
    for ht, a in hits.items():
        if ht not in fired and t >= ht: fired.add(ht); blast(*a)
    sx, sy, sp, sf = stick(t); foot = joints(sx, sy, sp, sf)[3]
    if 12.1 <= t < 12.14:
        for i, l in enumerate(nine): l.thrown = (t + i * .05, l.x, l.y, l.r); l.free = False
    for l in letters:
        if t >= 19.3:  # the spell: everything flies home
            start = 19.3 + (ord(l.c) % 7) * .03 + l.hx / 2600
            if t >= start:
                if not hasattr(l, 'rx'): l.rx, l.ry, l.rr = l.x, l.y, l.r; l.free = False; l.thrown = None
                u = ease(min(1, (t - start) / .9)); l.x = l.rx + (l.hx - l.rx) * u; l.y = l.ry + (l.hy - l.ry) * u - math.sin(u * math.pi) * 34; l.r = l.rr * (1 - u)
        elif l.thrown and t >= l.thrown[0]:
            t0, x0, y0, r0 = l.thrown; u = (t - t0) / .36
            if u >= 1:
                l.thrown = None; l.free = True; l.vx, l.vy, l.vr = random.uniform(-150, 40), -170, random.uniform(-16, 16)
            else:
                cx, cy, _ = card(t); l.x = x0 + (cx - 60 - x0) * u; l.y = y0 + (cy - y0) * u - 40 * math.sin(u * math.pi); l.r = r0 + u * 12
        elif l.free:
            l.vy += 900 * DT; l.x += l.vx * DT; l.y += l.vy * DT; l.r += l.vr * DT
            if l.x < 6 or l.x > W - 6: l.vx *= -.5; l.x = min(max(l.x, 6), W - 6)
            if l.y > FLOOR - 5:
                l.y = FLOOR - 5; l.vy *= -.28; l.vx *= .72; l.vr *= .5
                if abs(l.vy) < 26: l.vy = 0; l.vr = 0; l.r = round(l.r / math.pi) * math.pi
            if t < 19 and math.hypot(l.x - foot[0], l.y - foot[1]) < 13 and abs(l.vy) < 60:  # feet scuff the pile
                l.vx += sf * 170; l.vy -= 230; l.vr += sf * 11
    if t >= 16.95:
        for s in shards:
            s['vy'] += 700 * DT; s['x'] += s['vx'] * DT; s['y'] += s['vy'] * DT; s['r'] += s['vr'] * DT
            if s['y'] > FLOOR - 3: s['y'] = FLOOR - 3; s['vy'] *= -.3; s['vx'] *= .6
    if step % KEY_EVERY == 0:
        for l in letters:
            k = (round(l.x - l.hx, 1), round(l.y - l.hy, 1), round(math.degrees(l.r), 0))
            if not l.keys: l.keys.append((0, k))
            elif l.keys[-1][1] != k:
                if t - l.keys[-1][0] > .09: l.keys.append((round(t - .08, 2), l.keys[-1][1]))  # hold, then move
                l.keys.append((round(t, 2), k))
        if t >= 16.95:
            for s in shards: s['keys'].append((round(t, 2), s['x'], s['y'], math.degrees(s['r'])))
    t += DT; step += 1

# --- SVG output ------------------------------------------------------------
def anim(attr, kf, extra='', tag='animate'):
    kf = sorted(kf, key=lambda k: k[0])
    if kf[0][0] > 0: kf = [(0, kf[0][1])] + kf
    if kf[-1][0] < T: kf = kf + [(T, kf[-1][1])]
    out = [kf[0]]
    for i in range(1, len(kf) - 1):
        if not (kf[i][1] == out[-1][1] == kf[i + 1][1]) and kf[i][0] > out[-1][0]: out.append(kf[i])
    if kf[-1][0] > out[-1][0]: out.append(kf[-1])
    return f'<{tag} attributeName="{attr}" values="{";".join(str(v) for _, v in out)}" keyTimes="{";".join(f"{a / T:.4f}".rstrip("0").rstrip(".") if a else "0" for a, _ in out)}" dur="{T:g}s" repeatCount="indefinite" {extra}/>'
tr = lambda kf, typ='translate': anim('transform', kf, f'type="{typ}"', 'animateTransform')
OUT = lambda a=25.5, b=25.8: [(0, 1), (a, 1), (b, 0)]

def letter_svg(l, ink):
    show = [(0, 0), (l.born, 0), (l.born + .06, 1), (25.45, 1), (25.8, 0)]
    fill = ink
    kids = anim('opacity', show)
    if l.line in (3, 4):
        at = 8.0 + l.hx / 900
        kids += anim('fill', [(0, ink), (at, ink), (at + .2, PURPLE), (17.0, PURPLE), (17.5, ink)])
    if l.line == 0: fill = TOMATO
    moved = any(k[1] != (0, 0, 0) for k in l.keys)
    inner = f'<path d="{l.d}" fill="{fill}">{kids}</path>'
    if moved:
        inner = f'<g>{tr([(a, f"{k[0]} {k[1]}") for a, k in l.keys])}<g>{tr([(a, k[2]) for a, k in l.keys], "rotate")}{inner}</g></g>'
    return f'<g transform="translate({nt(l.hx)} {nt(l.hy)})">{inner}</g>'

def burst(x, y, t0, color, n=9, r=46):
    out = ''
    for i in range(n):
        a = i / n * 2 * math.pi + random.uniform(-.2, .2); r2 = r * random.uniform(.7, 1.1)
        x1, y1 = x + math.cos(a) * 12, y + math.sin(a) * 12; x2, y2 = x + math.cos(a) * r2, y + math.sin(a) * r2
        out += f'<line x1="{nt(x1)}" y1="{nt(y1)}" x2="{nt(x1)}" y2="{nt(y1)}" stroke="{color}" stroke-width="2.5" stroke-linecap="round" opacity="0">' \
               + anim('x2', [(0, nt(x1)), (t0, nt(x1)), (t0 + .16, nt(x2))]) + anim('y2', [(0, nt(y1)), (t0, nt(y1)), (t0 + .16, nt(y2))]) + anim('opacity', [(0, 0), (t0, 0), (t0 + .01, 1), (t0 + .24, 0)]) + '</line>'
    return out

def build(ink, bg, name):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>Hi, I\'m Rohit. A stickman fights an AI-slop card that attacks this README, then puts the page back together.</title>'
    s += f'<defs><linearGradient id="slop" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366F1"/><stop offset="1" stop-color="#A855F7"/></linearGradient></defs>'
    shake = [(0, '0 0')]
    for ht, amp in ((9.0, 7), (12.5, 3), (13.42, 5), (14.44, 7), (16.95, 8)):
        shake += [(ht - .01, '0 0')] + [(ht + i * .05, f'{amp * (-1) ** i * (1 - i / 6):.1f} {amp * .6 * (-1) ** (i + 1) * (1 - i / 6):.1f}') for i in range(6)] + [(ht + .3, '0 0')]
    s += '<g>' + tr(shake)
    # the tear in the page
    pts = [(-46, -6), (-30, -24), (-12, -16), (6, -30), (24, -18), (44, -22), (38, 0), (50, 16), (22, 18), (4, 28), (-20, 20), (-38, 24)]
    hole = ' '.join(f'{x},{y}' for x, y in pts)
    s += f'<g transform="translate({HOLE[0]} {HOLE[1] + 10})"><g>' + tr([(0, 0), (8.72, 0), (9.05, 1.15), (9.3, 1), (25.3, 1), (25.65, 0)], 'scale') + f'<polygon points="{hole}" fill="{"#010409" if bg == "dark" else "#1f2328"}" stroke="{TOMATO}" stroke-width="1.5"/></g>'
    for a in (-160, -120, -60, -20, 30, 150):
        x, y = 44 * math.cos(math.radians(a)), 30 * math.sin(math.radians(a)); xe, ye = x * 2.1, y * 2.2
        s += f'<line x1="{nt(x)}" y1="{nt(y)}" x2="{nt(xe)}" y2="{nt(ye)}" stroke="{ink}" stroke-width="1" opacity="0">' + anim('opacity', [(0, 0), (8.7, 0), (9, .5), (25.3, .5), (25.6, 0)]) + '</line>'
    s += '</g>'
    # crossed out greeting
    s += f'<line x1="22" y1="92" x2="22" y2="92" stroke="{TOMATO}" stroke-width="2">' + anim('x2', [(0, 22), (2.0, 22), (2.35, nt(strike_end)), (8.9, nt(strike_end)), (9.0, 22)]) + '</line>'
    for l in letters: s += letter_svg(l, ink)
    for l in finale:
        s += f'<g transform="translate({nt(l.hx)} {nt(l.hy)})"><path d="{l.d}" fill="{TOMATO}">' + anim('opacity', [(0, 0), (l.born, 0), (l.born + .08, 1), (25.45, 1), (25.8, 0)]) + '</path></g>'
    # slop card
    uw = 'Unlock seamless synergy'
    txt = ''.join(f'<path d="{sans.path(c, 12, x, 0)}" fill="#fff"/>' for c, x in (lambda r=[-68.0]: [(c, (r.append(r[-1] + sans.adv(c, 12)) or r[-2])) for c in uw])() if c != ' ')
    ct = [t / 10 for t in range(0, 261)]; cx = [(t, card(t)) for t in ct if 7.2 < t < 17.2]
    s += '<g opacity="0">' + anim('opacity', [(0, 0), (7.4, 0), (7.45, 1), (16.94, 1), (16.96, 0)])
    s += tr([(t, f'{nt(c[0])} {nt(c[1])}') for t, c in cx]) + '<g>' + tr([(t, nt(c[2])) for t, c in cx], 'rotate')
    s += '<rect x="-78" y="-46" width="156" height="92" rx="16" fill="url(#slop)"/>' + txt.replace('<path', '<path transform="translate(0 28)"')
    for ex in (-22, 22):
        s += f'<circle cx="{ex}" cy="-12" r="8" fill="#fff"/><circle cx="{ex + 3}" cy="-11" r="3.5" fill="#1e1b4b"/><line x1="{ex - 11}" y1="{-24 - (ex < 0) * -5}" x2="{ex + 11}" y2="{-24 + (ex < 0) * 5 - (ex > 0) * -0}" stroke="#1e1b4b" stroke-width="3"/>'
    for t0, d in ((13.42, 'M-78 -10L-44 -2L-52 18L-30 30'), (16.2, 'M40 -46L30 -18L52 -4L44 22')):
        s += f'<path d="{d}" fill="none" stroke="#1e1b4b" stroke-width="2.5" opacity="0">' + anim('opacity', [(0, 0), (t0, 0), (t0 + .02, 1)]) + '</path>'
    s += '</g></g>'
    # slop blob shot at the stickman
    s += '<circle r="13" fill="url(#slop)" opacity="0">' + anim('opacity', [(0, 0), (10.15, 0), (10.2, 1), (11.3, 1), (11.32, 0)]) + anim('cx', [(0, 580), (10.2, 580), (11.3, 60)]) + anim('cy', [(0, 110), (10.2, 110), (11.3, 268)]) + '</circle>'
    for sh in shards:
        s += f'<rect x="{-sh["s"] / 2:.1f}" y="{-sh["s"] / 2:.1f}" width="{sh["s"]:.1f}" height="{sh["s"]:.1f}" fill="{sh["c"]}" opacity="0">' + anim('opacity', [(0, 0), (16.95, 0), (16.97, 1), (18.6, 1), (19, 0)])
        k = [x for i, x in enumerate(sh['keys']) if i % 2 == 0 and x[0] < 19.1]
        s += tr([(a, f'{nt(x)} {nt(y)}') for a, x, y, _ in k]) + '</rect>'
    for x, y, t0, c in ((128, 200, 9.0, ink), (600, 95, 12.5, TOMATO), (610, 140, 13.42, TOMATO), (640, 262, 14.44, PURPLE), (668, 226, 16.0, TOMATO), (668, 226, 16.3, TOMATO), (640, 60, 16.95, PURPLE)):
        s += burst(x, y, t0, c, 11 if t0 == 16.95 else 9, 70 if t0 in (9.0, 16.95) else 44)
    # stickman
    ts = [8.7 + i / 20 for i in range(int((25.45 - 8.7) * 20) + 1)]; fr = [joints(*stick(t)) for t in ts]
    vis = [(0, 0), (8.72, 0), (8.74, 1), (25.3, 1), (25.45, 0)]
    trail = []; hx, hy = fr[0][1], fr[0][2]
    for (t, f) in zip(ts, fr):
        hx += (f[1] - hx) * .28; hy += (f[2] + 5 - hy) * .28
        trail.append((t, f'M{nt(f[1])} {nt(f[2] - 1)}L{nt(hx - 8 * (1 if f[1] > hx else -1))} {nt(hy)}L{nt(hx - 17 * (1 if f[1] > hx else -1))} {nt(hy + 3)}'))
    s += '<g fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0">' + anim('opacity', vis)
    s += f'<path stroke="{TOMATO}" stroke-width="3">' + anim('d', trail) + '</path>'
    s += f'<path stroke="{ink}" stroke-width="3.2">' + anim('d', [(t, f[0]) for t, f in zip(ts, fr)]) + '</path>'
    s += f'<circle r="8" fill="{bg_fill(bg)}" stroke="{ink}" stroke-width="3">' + anim('cx', [(t, nt(f[1])) for t, f in zip(ts, fr)]) + anim('cy', [(t, nt(f[2])) for t, f in zip(ts, fr)]) + '</circle></g>'
    s += '</g></svg>'
    (HERE / name).write_text(s); print(name, len(s) // 1024, 'KB')

bg_fill = lambda bg: '#0d1117' if bg == 'dark' else '#ffffff'
build('#e6edf3', 'dark', 'readme-dark.svg')
build('#1f2328', 'light', 'readme-light.svg')
