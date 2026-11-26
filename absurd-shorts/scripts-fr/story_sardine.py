#!/usr/bin/env python3
"""La sardine (story 108; one tent peg missing, a real sardine in oil planted in its place, and a seagull that kept the peg all along).
This man pitched his tent: one peg was missing. So he planted a real sardine, in oil. The storm takes the whole campsite but his tent; the next day the
whole campsite plants in oil, then the coast, then the mountain; sardines move to the camping aisle, tuna to the caravans, fishmongers sell mallets. The
seagulls follow the smell: each night they pull up a campsite, sardine by sardine. Thirty thousand tents migrate south in a V; ornithologists ring them.
One tent is left standing, his: the gulls avoid it; the whole country sleeps in it, packed like sardines. In the morning his sardine is gone, the tent
takes off: one peg missing, so they plant the biggest sardine: him.
Running gag (silent, never named): the big seagull keeps the stolen fat chrome peg in its beak in every shot of his campsite, stares at the oily sardine
closer each time (S02, S03, S09, S12: drool), stands on his ridge and drives the other gulls off with its wings spread (S09, S12); in S14 its belly is
round beside a clean skeleton; in S16 it drops the metal peg in the grass at the planted hero's chest. Never on his head: only on the tent.
Cards: PÉNURIE (S06), MIGRATION (S10). No other word, no figure, currency sign, flag, emblem or upright cross; plain tents; the tin has no label; the
scale a blank dial. At most five people in a shot."""
from story_kit import *
import math

st = Story('sardine', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 17)])
# the cuts are rounded to 4 decimals: one that rounds UP puts the frame of the cut in the shot before (a late cut by one frame); round them down
# the cuts are rounded to 4 decimals: one that rounds UP puts the frame of the cut in the shot before (a late cut by one frame); round them down
def _dn(v): return math.floor((round(v * 30) / 30) * 10000 - 1e-6) / 10000   # just under the 1/30 frame of the cut
st.SH = {sid: (_dn(a_) if a_ > 0 else 0.0, _dn(b_) if b_ < st.total else b_) for sid, (a_, b_) in st.SH.items()}
PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
def lerp3(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
def snap(t): return r(math.floor(t * 30) / 30 + 1 / 60)   # a time in the middle of its frame
CHECKS = []
def chk(sid, c, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(c['from'], c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
    if c.get('to'): CHECKS.append(f"{sid}(end): " + ' | '.join(f"{n} {project(c['to'], c.get('lookAt2') or c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
def fcam(at, frm, pts, top=0.08, bottom=0.76, margin=0.05, push=0.15, lenses=range(30, 61), ease='linear'):
    f, look, lens = fitBack(frm, pts, top=top, bottom=bottom, margin=margin, lenses=lenses)
    d = [look[i] - f[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in d)); to = [r(f[i] + d[i] / n * push) for i in range(3)]
    return cam(at, f, to, look, look, lens=lens, ease=ease)
def R5(p, w=1, s=0.04): return [*p, w, s]
def TK(t, reach=None, hands=None, face=None, sq=None, bend=None, d=0.12, e='inOut', keep=False, scl=None, plant=None, touch=None):
    tn = {}
    if reach: tn['reach'] = reach
    if touch: tn['touch'] = touch
    if hands: tn['hands'] = hands
    if face: tn['face'] = face
    if sq: tn['sq'] = list(sq)
    if bend: tn['bend'] = bend
    if scl: tn['scl'] = scl
    if plant: tn['plant'] = plant
    return k(t, toon=tn, toonDur=d, toonEase=e, **({'keepPose': True} if keep else {}))
def blink(t, face): return [k(t, toon={'face': {**face, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face}, toonDur=0.06, keepPose=True)]
def SP(a, side=0.0): return [a, side, 0, 1, None]
def BREATHE(t0, t1, every=0.55, a=0.012): return [k(r(t0 + i * every), toon={'sq': [1 - a * 0.5, 1 + a, 1 - a * 0.5] if i % 2 == 0 else [1, 1, 1]}, toonDur=r(every * 0.9), toonEase='inOut', keepPose=True) for i in range(max(1, int((t1 - t0) / every) + 1))]
def TALK(t0, face, n=3, step=0.09):
    """lip flaps: the mouth opens and shuts n times (a short word: « pardon »)"""
    out = []
    for j in range(n): out += [k(r(t0 + 2 * j * step), toon={'face': {**face, 'mouth': 'O', 'jaw': 0.5}}, toonDur=0.04, keepPose=True), k(r(t0 + (2 * j + 1) * step), toon={'face': {**face, 'mouth': 'line'}}, toonDur=0.04, keepPose=True)]
    return out
def HANDS(p, ry, rf=0.25, rs=0.25, ry_=1.0, lf=0.25, ls=-0.25, ly=1.0):
    return {'R': R5(off(p, ry, rf, rs, ry_)), 'L': R5(off(p, ry, lf, ls, ly))}
def HEAD(p, y=1.9): return [p[0], y, p[2]]   # a look target at head height
def along(pts, u):
    """the point at fraction u of the length of a polyline, and its heading (degrees)"""
    seg = [(pts[i], pts[i + 1], math.dist(pts[i], pts[i + 1])) for i in range(len(pts) - 1)]; L = sum(x[2] for x in seg); d = max(0.0, min(1.0, u)) * L
    for a, b, l in seg:
        if d <= l or (a, b, l) == seg[-1]: return lerp3(a, b, min(1.0, d / l if l else 0.0)), yaw(a, b)
        d -= l
def WALKHANDS(t0, dur, pts, hands, step=0.2):
    """hand keys every 0.2 s on a walking actor: each hand (name -> (f, s, y) in his frame) follows him along the path"""
    out = []
    for j in range(int(dur / step) + 2):
        t = r(t0 + j * step); p, hd = along(pts, (t - t0) / dur); sw = 0.04 if j % 2 else -0.04
        out.append(TK(t, {h: R5(off(p, hd, f + sw * (1 if h == 'R' else -1), s_, y)) for h, (f, s_, y) in hands.items()}, d=step, e='linear', keep=True))
    return out

# faces
CALM = {'lid': 0.3, 'mouth': 'line', 'brow': 0.0}
WORRY = {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}
STERN = {'lid': 0.35, 'mouth': 'line', 'brow': -0.6}
SMUG = {'lid': 0.35, 'mouth': 'smile', 'brow': 0.2}
HAPPY = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}
SAD = {'lid': 0.5, 'mouth': 'line', 'brow': 0.5}
GRAVE = {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}
DAZED = {'lid': 0.55, 'mouth': 'O', 'brow': 0.4}
POP = {'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 1.0}
JAW = {'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'jaw': 0.9}
DEAD = {'lid': 0.45, 'mouth': 'line', 'brow': 0.0}
SKY = '#A9D3EE'
def SELFPT(side='R', w=1):
    sx = -1 if side == 'R' else 1
    return {side: ['torso', r(0.07 * sx), 0.46, 0.27, w, 0.04, [r(0.75 * sx), -0.35, 0.6]]}
def BLINKS(t0, t1, face, every=2.2, ph=0.0):
    out, t = [], r(t0 + ph)
    while t < t1 - 0.15: out += blink(t, face); t = r(t + every + 0.3 * math.sin(t * 7))
def DROP(pid, actor, t0, offset=(-0.24, 0.42, 0.0), scale=0.75):
    """a sweat drop that pops on his temple at t0, clear of the eye"""
    return P(pid, 'sweatDrop', on={'actor': actor, 'joint': 'head', 'offset': list(offset)}, scale=scale, keys=[k(0.0, visible=False), k(t0, visible=True), k(t0, squash=[1.6, 0.5, 1.6], dur=0.3)])

# ---------------------------------------------------------------- the campsite and the running gag
# his tent at the origin, door toward +Z (the lens side); its front-left corner (-X, +Z) is the sardine's; the seagull (knee-high: creature scale 1.8,
# 0.76 m) keeps the stolen chrome peg in its beak in every shot of his campsite, and stares at the sardine closer each time; never on his head
TENT = [0.0, 0, 0.0]; TW = 1.6; SC = [-0.877, 0, 0.877]   # the sardine corner (where its peg would be)
ROPE_TOP = [-0.35, 0.68, 0.35]   # where the corner's rope leaves the dome
GS = 1.8   # the gull's scale
MEADOW = {'grass': '#8CC460'}
def PEG(pid, actor='mouette', keys=None, ph=0.0):
    """the stolen peg in the gull's beak (one prop: it follows the head), sticking out sideways like a cigar"""
    return P(pid, 'saPeg', on={'actor': actor, 'joint': 'head', 'offset': [0.02, -0.01, 0.1], 'rot': [0.1, 0.9, 0]}, opts={'ph': ph}, keys=keys or [])
def GULL(id_, pos, ry, clip='idle', keys=None, scale=GS): return act(id_, pos, ry, clip, 'neutral', keys=keys or [], scale=scale)
def TENT_(pid, pos=TENT, ry=0, **o): return P(pid, 'saTent', pos=pos, ry=ry, opts=o)
RIDGE = [0.0, 1.08, 0.0]   # the top of his dome: where the gull stands
NIGHT = dict(dark=[[0.0, 0.6]], darkFloor=0.5, darkTint='#6F8FE0')

# ================================================================= S01
# 1: two cuts. A campsite meadow, bright morning: the hero kneels by his little orange dome tent with a wooden mallet; three fat chrome pegs lie in a row
#    in the grass, the fourth corner flaps loose. The big white seagull lands, snatches a fourth peg and hops back two steps with it in its beak like a
#    cigar. Cut: he looks from the three pegs to the loose corner and back, and frowns
D1 = st.dur('S01'); CUT1 = r(st.at('S01', 'L01', 6) - 0.1)
HK1 = [0.55, 0, 1.45]; HRY1 = 10; PEGS1 = [[r(0.05 + 0.24 * i), 0.03, 1.95] for i in range(3)]; P4 = [-0.55, 0.03, 1.75]
G1a, G1b, G1c = [-2.4, 0, 1.5], [-0.75, 0, 1.75], [-1.35, 0, 2.0]; SNATCH1 = 0.75
C1 = fcam(0.0, [0.2, 1.1, 5.4], {'tent': [0, 1.15, 0], 'heroT': add(HK1, [0, 1.75, 0]), 'heroR': add(HK1, [0.55, 1.2, 0.2]), 'gull': add(G1c, [0, 0.8, 0]), 'gullA': add(G1b, [-0.2, 0, 0.3]), 'pegs': [0.3, 0, 2.1], 'tentB': [-0.9, 0, 0.9]}, top=0.14, bottom=0.76, push=0.2)
C1b = fcam(CUT1, [1.9, 1.25, 4.0], {'head': add(HK1, [0, 1.85, 0]), 'pegs': [0.0, 0.0, 2.05], 'pegs2': [0.6, 0, 2.05], 'corner': [-0.75, 0.2, 0.75], 'gull': add(G1c, [0, 0.8, 0]), 'gullF': G1c}, top=0.12, bottom=0.76, push=0.1)
kh1 = [k(0.0, clip='kneel'), k(0.0, look=add(PEGS1[2], [0.3, 0, -0.3])), TK(0.0, {'R': R5(off(HK1, HRY1, 0.4, 0.25, 0.9)), 'L': R5(off(HK1, HRY1, 0.45, -0.2, 0.6))}, {'R': 'grip', 'L': 'spread'}, CALM, bend={'spine': SP(0.25)}, d=0.0),
       *[x for j in range(3) for x in (TK(r(0.1 + 0.32 * j), {'R': R5(off(HK1, HRY1, 0.45, 0.25, 1.15))}, d=0.1, keep=True), TK(r(0.22 + 0.32 * j), {'R': R5(off(HK1, HRY1, 0.55, 0.2, 0.55))}, sq=(1.04, 0.96, 1.04), d=0.06, e='in', keep=True))],   # tock, tock, tock
       TK(1.1, sq=(1, 1, 1), d=0.1, keep=True), *blink(1.2, CALM),
       k(r(CUT1 + 0.05), look=add(PEGS1[1], [0, 0, 0]), lookDur=0.12), TK(r(CUT1 + 0.05), face={**CALM, 'gx': -0.3}, d=0.08, keep=True),   # the three pegs...
       TK(r(CUT1 + 0.3), face={**CALM, 'gx': 0.8}, d=0.05, keep=True), k(r(CUT1 + 0.36), look=[-0.75, 0.15, 0.75], lookDur=0.14),   # ...the loose corner (the eyes lead)...
       TK(r(CUT1 + 0.62), face={**CALM, 'gx': -0.6}, d=0.05, keep=True), k(r(CUT1 + 0.66), look=PEGS1[1], lookDur=0.12),   # ...and back
       TK(r(CUT1 + 0.9), face={'lid': 0.45, 'mouth': 'wavy', 'brow': -1.0, 'gx': 0.0}, sq=(1.04, 0.95, 1.04), d=0.06, keep=True), k(r(CUT1 + 0.95), look='camera', lookDur=0.15), *BREATHE(r(CUT1 + 1.0), D1, 0.45)]
kg1 = [k(0.0, clip='fly'), k(0.0, to=G1b, dur=0.42, clip='fly', ease='out', face='keep'), k(0.42, clip='idle', blend=0.08), k(0.5, look=P4, lookDur=0.1),
       k(r(SNATCH1 - 0.15), clip='peck', blend=0.06), k(r(SNATCH1 + 0.08), clip='hop', blend=0.04), k(r(SNATCH1 + 0.08), to=lerp3(G1b, G1c, 0.5), dur=0.22, clip='hop', ease='out', face='keep'), k(r(SNATCH1 + 0.32), to=G1c, dur=0.22, clip='hop', ease='out', face='keep'),   # hop, hop back   # snatch, two hops back
       k(r(SNATCH1 + 0.55), clip='idle', blend=0.1), k(r(SNATCH1 + 0.6), look='camera', lookDur=0.15)]
st.shot('S01', 'grassland', setOpts=MEADOW, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', HK1, HRY1, 'kneel', 'neutral', keys=kh1), GULL('mouette', G1a, 70, 'fly', keys=kg1)],
        props=[TENT_('tente1', loose=True), *[P(f'piquet1_{i}', 'saPeg', pos=p, ry=90, opts={'ph': 0.3 * i}) for i, p in enumerate(PEGS1)],
               P('piquet1', 'saPeg', pos=P4, ry=90, keys=[k(SNATCH1, attach='mouette', joint='head', offset=[0.02, -0.01, 0.1], rot=[0.1, 0.9, 0])]),
               P('maillet1', 'saMallet', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.04, 0]}), P('tente1b', 'saTent', pos=[-3.2, 0, -3.4], ry=20, opts={'color': '#3E8ACC'}),
               P('tente1c', 'saTent', pos=[2.8, 0, -3.8], ry=-15, opts={'color': '#E8C030'})], cams=[C1, C1b])
st.cue('thud', 'S01', 0.22, 0.2); st.cue('thud', 'S01', 0.54, 0.2); st.cue('thud', 'S01', 0.86, 0.2); st.cue('whoosh', 'S01', 0.1, 0.3); st.cue('pop', 'S01', SNATCH1, 0.2)

# ================================================================= S02
# 2: ground-level close-up: he rolls open a flat silver tin (no label), pulls out one big glistening sardine by the tail and drives it head first into
#    the ground with the mallet, bonk; he loops the guy rope round its tail. Behind him the seagull, peg in beak, stares at the fish
D2 = st.dur('S02'); OPEN2 = 0.25; PULL2 = 0.85; BONK2 = r(st.at('S02', 'L02', 7) - 0.05); LOOP2 = r(BONK2 + 0.6)
HK2 = add(SC, [0.75, 0, -0.05]); HRY2 = -60; TIN2 = add(SC, [0.35, 0.0, 0.32]); SARD_IN = add(SC, [0, 0.2, 0])
G2 = add(SC, [-0.75, 0, -0.75])
C2 = fcam(0.0, [-0.6, 0.5, 2.6], {'sard': add(SC, [0, 0.35, 0]), 'tin': TIN2, 'heroT': add(HK2, [0, 1.8, 0]), 'gull': add(G2, [0, 0.8, 0]), 'gullF': G2}, top=0.12, bottom=0.76, push=0.15)
kh2 = [k(0.0, clip='kneel'), k(0.0, look=TIN2), TK(0.0, {'R': R5(add(TIN2, [0.12, 0.08, 0])), 'L': R5(add(TIN2, [-0.1, 0.06, 0]))}, {'R': 'pinch', 'L': 'spread'}, CALM, bend={'spine': SP(0.35)}, d=0.0),
       TK(OPEN2, {'R': R5(add(TIN2, [-0.12, 0.08, 0]))}, d=0.4, keep=True),   # the key rolls the lid back
       TK(r(PULL2 - 0.12), {'L': R5(add(TIN2, [0.0, 0.06, 0]))}, {'L': 'pinch'}, d=0.1, keep=True), TK(PULL2, {'L': R5(add(TIN2, [0.0, 0.45, 0.05]))}, sq=(0.97, 1.04, 0.97), d=0.12, keep=True), k(PULL2, look=add(TIN2, [0, 0.45, 0]), lookDur=0.1),   # one big sardine, by the tail
       TK(r(BONK2 - 0.45), {'L': R5(add(SARD_IN, [0, 0.15, 0])), 'R': R5(add(SC, [0.15, 0.9, 0.1]))}, {'R': 'grip'}, sq=(1, 1, 1), d=0.2, keep=True), k(r(BONK2 - 0.4), look=SC, lookDur=0.12),   # held head down, the mallet up
       TK(BONK2, {'R': R5(add(SC, [0.05, 0.42, 0.05]))}, sq=(1.06, 0.92, 1.06), d=0.06, e='in', keep=True), TK(r(BONK2 + 0.12), {'R': R5(add(SC, [0.15, 0.7, 0.1])), 'L': R5(add(SC, [0.15, 0.3, 0.15]))}, {'L': 'spread'}, sq=(1, 1, 1), d=0.12, keep=True),   # BONK
       TK(LOOP2, {'L': R5(add(SC, [0.0, 0.32, 0.05]))}, {'L': 'pinch'}, d=0.15, keep=True), TK(r(LOOP2 + 0.3), {'L': R5(add(SC, [0.2, 0.45, 0.25]))}, d=0.15, keep=True),   # the rope looped round its tail
       TK(r(LOOP2 + 0.5), face=SMUG, d=0.1, keep=True), k(r(LOOP2 + 0.5), look='camera', lookDur=0.15), *blink(1.2, CALM)]
kg2 = [k(0.0, clip='idle'), k(0.0, look=TIN2), k(PULL2, look=add(TIN2, [0, 0.45, 0]), lookDur=0.1), k(BONK2, look=SARD_IN, lookDur=0.1), k(r(BONK2 + 0.2), clip='walk', blend=0.05), k(r(BONK2 + 0.2), to=add(G2, [0.25, 0, 0.15]), dur=0.4, clip='walk', ease='out', face='keep'), k(r(BONK2 + 0.6), clip='idle', blend=0.1)]   # it stares, a step closer
st.shot('S02', 'grassland', setOpts=MEADOW, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', HK2, HRY2, 'kneel', 'neutral', keys=kh2), GULL('mouette', G2, 60, 'idle', keys=kg2)],
        props=[TENT_('tente2', loose=True, looseUntil=LOOP2, ropeY=0.36), P('boucle2', 'saRing', pos=add(SC, [0, 0.38, 0]), rot=[1.5708, 0, 0], scale=0.35, keys=[k(0.0, visible=False), k(LOOP2, visible=True)]), P('boite2', 'saTin', pos=TIN2, ry=-20, opts={'openAt': OPEN2, 's': 1.9}),
               P('sardine2', 'saSardine', pos=add(TIN2, [0, 0.08, 0]), rot=[0, 0, 0], opts={'len': 0.44, 'squash': [[BONK2, 0], [r(BONK2 + 0.03), 1.0], [r(BONK2 + 0.14), 1.0], [r(BONK2 + 0.24), -0.35], [r(BONK2 + 0.34), 0.1], [r(BONK2 + 0.42), 0]]}, keys=[k(PULL2, attach='mec', hand='L', offset=[0, -0.2, 0.0], rot=[-1.5708, 0, 0]), k(BONK2, detach=True), k(BONK2, to=SARD_IN, dur=0.01), k(BONK2, rotTo=[1.5708, 0, 0], dur=0.01)]),
               P('maillet2', 'saMallet', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.04, 0]}), PEG('piquet2')], cams=[C2])
st.cue('clack', 'S02', OPEN2, 0.2); st.cue('thud', 'S02', BONK2, 0.5); st.cue('pop', 'S02', BONK2, 0.2)

# ================================================================= S03
# 3: a stormy night in deep blue, lightning flashes, rain streaks: three neighbouring tents tear loose and fly off like kites, one camper still clinging
#    to a pole, stretched out flat behind it. His little orange tent does not move an inch, its rope taut on the sardine. On its ridge, the seagull in
#    the rain, peg in beak
D3 = st.dur('S03'); TEAR3 = r(st.at('S03', 'L03', 4) - 0.05); FL3 = [0.35, r(TEAR3 + 0.1), 2.3]
NB3 = [[-3.0, 0, -2.2], [2.9, 0, -2.6], [-0.4, 0, -4.2]]; NBC3 = ['#3E8ACC', '#E8C030', '#5EAA4A']
C3 = fcam(0.0, [0.4, 0.75, 4.4], {'tent': [0, 2.0, 0], 'tentF': [0, 0, 0.9], 'nb0': add(NB3[0], [0, 1.1, 0]), 'nb1': add(NB3[1], [0, 1.1, 0]), 'sard': SC, 'sky': [-1.5, 3.4, -2.5]}, top=0.1, bottom=0.76, push=0.25)   # (round 1) lower, the gull on the ridge bigger
def fly3(p, i):   # torn off: up and away to the upper left, tumbling
    end = [r(p[0] - 2.2 + 1.6 * i), 4.2, r(p[2] - 1.5)]
    return [k(0.0, to=p, dur=0.01), k(r(TEAR3 - 0.3), to=add(p, [0.1, 0.05, 0]), dur=0.08), k(r(TEAR3 - 0.22), to=add(p, [-0.1, 0.0, 0]), dur=0.08), k(TEAR3, to=add(p, [0, 0.6, 0]), dur=0.1, ease='out'), k(r(TEAR3 + 0.15), to=end, dur=2.1, ease='inOut'), k(TEAR3, rotTo=[0.3, 0.4 * (i - 1), 0.8 * (1 - i)], dur=2.1)]
CAMPER3 = NB3[0]
kc3 = [k(0.0, clip='stand'), k(0.0, visible=False), k(TEAR3, visible=True), k(TEAR3, clip='superman', blend=0.05), TK(TEAR3, sq=(1.0, 0.8, 1.35), d=0.08, keep=True), k(TEAR3, to=add(CAMPER3, [0.6, 0.8, 0.3]), dur=0.15, clip='superman', face='keep'),
       k(r(TEAR3 + 0.15), to=[r(CAMPER3[0] + 0.6), 2.4, r(CAMPER3[2] + 1.0)], dur=2.1, clip='superman', ease='inOut', face='keep'), k(TEAR3, look=add(CAMPER3, [-1, 1.5, 0]), lookDur=0.1), TK(TEAR3, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, d=0.05, keep=True)]
kg3 = [k(0.0, clip='sit'), k(0.0, look=add(SC, [0, 0.2, 0])), *[k(r(0.5 + 0.8 * j), look=add(SC, [0.1 * (j % 2), 0.2, 0]), lookDur=0.2) for j in range(4)]]
st.shot('S03', 'grassland', setOpts={'grass': '#5E8C48', 'sky': ['#2A4C90', '#4A6AAA'], 'clouds': 0}, look={'sunDir': [0.3, 0.9, 0.6]}, dark=[[0.0, 0.45], *[x for t_ in FL3 for x in ([t_, 0.22, 0.02], [r(t_ + 0.14), 0.45, 0.1])]], darkFloor=0.62, darkTint='#7E9CEA',   # (round 1) lightning lights the set; never darker than the night
        actors=[act('campeur1', add(CAMPER3, [0.6, 0, 0.3]), -110, 'stand', 'neutral', keys=kc3), GULL('mouette', RIDGE, 20, 'sit', keys=kg3)],
        props=[TENT_('tente3'), *[P(f'voisine3_{i}', 'saTent', pos=p, opts={'color': NBC3[i]}, keys=fly3(p, i)) for i, p in enumerate(NB3)],
               P('sardine3', 'saSardine', pos=add(SC, [0, 0.17, 0]), rot=[1.5708, 0, 0], opts={'len': 0.36}), PEG('piquet3'),
               P('pluie3', 'saRain', pos=[0, 0, 1.0], opts={'w': 9, 'd': 6, 'h': 5.5, 'n': 220}, inDark=True), *[P(f'eclair3_{i}', 'saBolt', pos=[-2.5 + 2.5 * i, 7.5, -7.0], scale=1.3, opts={'at': [t_]}, inDark=True) for i, t_ in enumerate(FL3)]], cams=[C3])
st.cue('thunder', 'S03', FL3[0], 0.5); st.cue('thunder', 'S03', FL3[1], 0.6); st.cue('gust', 'S03', 0.0, 0.5); st.cue('rain', 'S03', 0.0, 0.3)

# ================================================================= S04
# 4: morning: four campers in shorts and sun hats kneel in a row at their tents, roll open sardine tins with the key in perfect sync, then hammer a
#    sardine in each, bonk bonk bonk bonk
D4 = st.dur('S04'); OPEN4 = 0.2; PULL4 = 0.75; BONKS4 = [r(1.3 + 0.24 * j) for j in range(4)]
XS4 = [r(-1.75 + 1.15 * i) for i in range(4)]; KZ4 = 0.9; TC4 = ['#3E8ACC', '#E8C030', '#5EAA4A', '#E8913A']
C4 = fcam(0.0, [XS4[3] + 1.6, 0.6, 3.0], {'h3': [XS4[3], 1.6, KZ4], 'h0': [XS4[0], 1.5, KZ4], 'tin3': [XS4[3] + 0.3, 0, KZ4 + 0.55], 'tin0': [XS4[0] + 0.3, 0, KZ4 + 0.55], 'gull': [XS4[3] + 1.0, 0.8, KZ4 + 0.6]}, top=0.12, bottom=0.76, push=0.2)   # (round 1) a low three-quarter angle along the row
cast4, props4 = [], []
for i, x in enumerate(XS4):
    p = [x, 0, KZ4]; nm = f'campeur{i + 1}'; T = [r(x + 0.3), 0, r(KZ4 + 0.5)]; S_ = [r(x - 0.3), 0, r(KZ4 + 0.45)]
    ks = [k(0.0, clip='kneel'), k(0.0, look=T), TK(0.0, {'R': R5(add(T, [0.1, 0.08, 0])), 'L': R5(add(T, [-0.08, 0.06, 0]))}, {'R': 'pinch', 'L': 'spread'}, CALM, bend={'spine': SP(0.3)}, d=0.0),
          TK(OPEN4, {'R': R5(add(T, [-0.12, 0.08, 0]))}, d=0.4, keep=True), TK(PULL4, {'L': R5(add(T, [0, 0.4, 0]))}, {'L': 'pinch'}, d=0.15, keep=True),
          TK(r(BONKS4[0] - 0.3), {'L': R5(add(S_, [0, 0.35, 0])), 'R': R5(add(S_, [0.12, 0.85, 0]))}, {'R': 'grip'}, d=0.2, keep=True), k(r(BONKS4[0] - 0.3), look=S_, lookDur=0.1)]
    for j, b in enumerate(BONKS4): ks += [TK(b, {'R': R5(add(S_, [0.05, 0.4, 0]))}, sq=(1.05, 0.93, 1.05), d=0.05, e='in', keep=True), TK(r(b + 0.12), {'R': R5(add(S_, [0.12, 0.8, 0]))}, sq=(1, 1, 1), d=0.1, keep=True)]
    ks += [*blink(r(0.6 + 0.1 * i), CALM)]
    cast4.append(act(nm, p, 0, 'kneel', 'neutral', keys=ks))
    props4 += [P(f'tente4_{i}', 'saTent', pos=[r(x + 0.58), 0, -0.9], opts={'color': TC4[i], 'w': 1.05, 'h': 0.85, 'ropes': False}), P(f'boite4_{i}', 'saTin', pos=T, opts={'openAt': OPEN4, 's': 1.3}),
               P(f'sardine4_{i}', 'saSardine', pos=add(T, [0, 0.06, 0]), opts={'len': 0.3}, keys=[k(PULL4, attach=nm, hand='L', offset=[0, -0.18, 0], rot=[-1.5708, 0, 0]), k(BONKS4[0], detach=True), k(BONKS4[0], to=add(S_, [0, 0.13, 0]), dur=0.01), k(BONKS4[0], rotTo=[1.5708, 0, 0], dur=0.01)]),
               P(f'maillet4_{i}', 'saMallet', on={'actor': nm, 'hand': 'R', 'offset': [0, 0.04, 0]}), P(f'chapeau4_{i}', 'coHat', on={'actor': nm, 'joint': 'head', 'offset': [0, 0.4, 0]})]
G4 = [XS4[3] + 0.75, 0, KZ4 + 0.9]
st.shot('S04', 'grassland', setOpts=MEADOW, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[*cast4, GULL('mouette', G4, -60, 'idle', keys=[k(0.0, look=add(G4, [-0.6, 0.1, 0])), *[k(b, look=[XS4[3] - 0.3, 0.2, KZ4 + 0.45], lookDur=0.06) for b in BONKS4[:1]]])],
        props=[*props4, PEG('piquet4')], cams=[C4])
for b in BONKS4: st.cue('thud', 'S04', b, 0.35)
st.cue('clack', 'S04', OPEN4, 0.25)

# ================================================================= S05
# 5: two cuts. A hillside above a turquoise bay covered in small plain dome tents, no people; in the near foreground one tent with a big silver fish tail
#    glinting at its corner. Cut: the same tents dotted on a green alpine slope under snowy peaks, each corner glinting
D5 = st.dur('S05'); CUT5 = r(st.at('S05', 'L05', 4) - 0.1)
F5 = [60.0, 0, 0]
C5 = cam(0.0, add(F5, [-0.3, 2.2, 7.4]), add(F5, [-0.25, 2.1, 6.4]), add(F5, [0.2, 0.6, -2.0]), add(F5, [0.2, 0.7, -2.0]), lens=46)   # (round 1) a push-in
F5b = [140.0, 0, 0]
C5b = cam(CUT5, add(F5b, [0.0, 2.2, 9.0]), add(F5b, [0.3, 2.5, 8.2]), add(F5b, [0.0, 2.8, -4.0]), add(F5b, [0.0, 3.0, -4.0]), lens=36)
FG5 = add(F5, [0.1, 0, 2.4])
st.shot('S05', 'whiteVoid', setOpts={'color': '#9ED2F0'}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[],
        props=[P('baie5', 'saTentField', pos=add(F5, [0, -0.35, 0.5]), opts={'n': 0, 'w': 60, 'd': 30, 'rise': 0.0, 'groundColor': '#1ED8D0'}),
               P('colline5', 'saTentField', pos=add(F5, [0, 1.6, -7.5]), opts={'n': 70, 'w': 30, 'd': 14, 'rise': 0.35, 'groundColor': '#86BE5C'}),
               P('tente5', 'saTent', pos=FG5, ry=20, opts={'color': '#3E8ACC', 'w': 1.3, 'h': 0.9}), P('sol5', 'saFlats', pos=add(FG5, [0, 0, 0.5]), opts={'spots': [[0, 0, 8.0, 4.0, 0]]}), P('queue5', 'saSardine', pos=add(FG5, [-0.62, 0.4, 0.78]), rot=[1.1, 0.4, 0], opts={'len': 0.9}),
               P('eclat5', 'saGlint', pos=add(FG5, [-0.5, 0.6, 0.85]), opts={'size': 0.3, 'every': 0.7}),
               P('pente5', 'saTentField', pos=F5b, opts={'n': 70, 'w': 40, 'd': 30, 'rise': 0.45, 'groundColor': '#6EAE52', 'glint': True}),
               P('sommets5', 'mountainRange', pos=add(F5b, [0, 5.0, -30.0]), opts={'n': 9, 'w': 70, 'h': 14})], cams=[C5, C5b])
st.cue('gust', 'S05', 0.0, 0.2); st.cue('pop', 'S05', 0.4, 0.2); st.cue('pop', 'S05', r(CUT5 + 0.3), 0.2)

# ================================================================= S06
# 6: a supermarket camping aisle (plain shelves, blank boxes): a single sardine tin on a red velvet cushion under a small glass dome, in a spotlight, no
#    price tag; a shopkeeper in white gloves lifts the dome for a customer, who gulps (sweat drop). In the next aisle behind them a caravan with a giant
#    tuna wedged under its wheel as a chock. PÉNURIE card
D6 = st.dur('S06'); LIFT6 = 0.9; GULP6 = 1.45; TUNA6 = r(st.at('S06', 'L06', 7))
PED6 = [0.0, 0, 0.6]; CUSH6 = add(PED6, [0, 1.0, 0]); SK6 = [1.0, 0, 0.0]; CU6 = [-1.0, 0, 0.3]
CAR6 = [0.9, 0, -2.4]
C6 = fcam(0.0, [0.0, 1.3, 3.6], {'sk': add(SK6, [0, 2.3, 0]), 'cu': add(CU6, [0, 2.3, 0]), 'cush': add(CUSH6, [0, -0.3, 0]), 'dome': add(CUSH6, [0, 0.55, 0]), 'tuna': add(CAR6, [0.2, 0.0, 1.2]), 'carT': add(CAR6, [0.6, 2.2, 0])}, top=0.2, bottom=0.76, push=0.2)   # (round 1) frontal on the dome
ksk6 = [k(0.0, clip='stand'), k(0.0, look=CUSH6), TK(0.0, {'R': R5(add(CUSH6, [0.18, 0.12, 0])), 'L': R5(add(CUSH6, [-0.05, 0.3, 0.1]))}, {'R': 'spread', 'L': 'spread'}, {'lid': 0.45, 'mouth': 'line', 'brow': 0.2}, d=0.0),
        TK(r(LIFT6 - 0.2), {'R': R5(add(CUSH6, [0.15, 0.3, 0])), 'L': R5(add(CUSH6, [-0.15, 0.3, 0]))}, {'R': 'pinch', 'L': 'pinch'}, d=0.15, keep=True), TK(LIFT6, {'R': R5(add(CUSH6, [0.55, 0.85, -0.25])), 'L': R5(add(CUSH6, [0.35, 0.95, -0.25]))}, sq=(0.97, 1.04, 0.97), d=0.5, keep=True),   # the dome lifted
        k(r(LIFT6 + 0.3), look=HEAD(CU6, 1.95), lookDur=0.2), TK(r(LIFT6 + 0.4), sq=(1, 1, 1), d=0.1, keep=True), *blink(2.3, {'lid': 0.45, 'mouth': 'line', 'brow': 0.2}), *BREATHE(1.4, D6, 0.5)]
kcu6 = [k(0.0, clip='stand'), k(0.0, look=CUSH6), TK(0.0, HANDS(CU6, 40), {'R': 'rest', 'L': 'rest'}, WORRY, d=0.0),
        TK(r(LIFT6 + 0.2), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 0.7}, sq=(0.94, 1.08, 0.94), d=0.06, e='out', keep=True),   # eyes out
        TK(r(GULP6 - 0.08), sq=(1.08, 0.9, 1.08), bend={'neck': SP(0.3)}, d=0.06, keep=True), TK(GULP6, face={**WORRY, 'jaw': 0.3, 'pop': 0.5}, sq=(0.9, 1.14, 0.9), bend={'neck': SP(-0.45)}, d=0.05, e='out', keep=True), TK(r(GULP6 + 0.2), face=WORRY, sq=(1, 1, 1), bend={'neck': SP(0.0)}, d=0.1, keep=True),   # gulp
        k(r(GULP6 + 0.4), look='camera', lookDur=0.15), *blink(2.6, WORRY), *BREATHE(1.8, D6, 0.5)]
st.shot('S06', 'whiteVoid', setOpts={'color': '#EDE6D6'}, look={'sunDir': [0.3, 0.9, 0.8]},
        actors=[act('commercant', SK6, -100, 'stand', 'neutral', keys=ksk6), act('client', CU6, 60, 'stand', 'neutral', keys=kcu6)],
        props=[P('rayonA6', 'saShelf', pos=[-1.8, 0, -0.8], opts={'w': 2.2}), P('rayonB6', 'saShelf', pos=[2.0, 0, -0.8], opts={'w': 2.0}),
               P('socle6', 'saPlinth', pos=PED6, opts={'h': 0.95}),
               P('coussin6', 'velvetCushion', pos=CUSH6, opts={'w': 0.38}), P('boite6', 'saTin', pos=add(CUSH6, [0, 0.08, 0]), ry=15),
               P('cloche6', 'saDome', pos=add(CUSH6, [0, 0.08, 0]), opts={'r': 0.22, 'h': 0.42}, keys=[k(r(LIFT6 - 0.02), attach='commercant', hand='R', offset=[-0.12, -0.25, 0.0], rot=[0, 0, 0])]),
               P('faisceau6', 'saBeam', pos=add(CUSH6, [0, 1.9, 0]), opts={'h': 1.8, 'r': 0.4}),
               P('caravane6', 'saCaravan', pos=CAR6), P('thon6', 'saTuna', pos=add(CAR6, [0.2, 0.17, 1.15]), ry=10, opts={'len': 1.0}),
               DROP('goutte6', 'client', GULP6)], cams=[C6])
st.card('S06', 'PÉNURIE', at=st.at('S06', 'L06', 1)); st.cue('clang', 'S06', LIFT6, 0.3); st.cue('pop', 'S06', GULP6, 0.3)

# ================================================================= S07
# 7: a fishmonger's stall on crushed ice: no fish left, only rows of wooden mallets laid out like fish and one rolled-up tent; the fishmonger in a
#    striped apron weighs a mallet on a scale with a blank dial and wraps it in paper, deadpan
D7 = st.dur('S07'); WEIGH7 = 0.55; WRAP7 = 1.15
ST7 = [0.0, 0, 0.0]; FM7 = [0.15, 0, -0.85]; SCL7 = [-0.05, 1.04, 0.28]; PAP7 = [0.6, 1.06, 0.2]
C7 = fcam(0.0, [-0.1, 2.0, 2.3], {'fm': add(FM7, [0, 2.35, 0]), 'fmL': add(FM7, [-0.4, 1.4, 0]), 'scale': add(SCL7, [0, 0.45, 0]), 'scaleB': add(SCL7, [0, -0.05, 0.25]), 'ice': [-0.6, 1.0, 0.4], 'ice2': [0.7, 1.0, 0.4]}, top=0.1, bottom=0.76, push=0.12)   # (round 2) from higher: the ice bed and the mallets in rows
kf7 = [k(0.0, clip='stand'), k(0.0, look=[-0.3, 1.1, 0.1]), TK(0.0, {'R': R5([-0.25, 1.15, -0.05]), 'L': R5([0.3, 1.1, -0.1])}, {'R': 'grip', 'L': 'rest'}, DEAD, d=0.0),
       TK(0.15, {'R': R5([-0.3, 1.35, 0.0])}, d=0.15, keep=True), TK(r(WEIGH7 - 0.05), {'R': R5(add(SCL7, [0.0, 0.55, 0]))}, d=0.25, keep=True), k(r(WEIGH7 - 0.1), look=add(SCL7, [0, 0.35, 0]), lookDur=0.12),   # onto the scale
       TK(r(WEIGH7 + 0.3), {'R': R5(add(PAP7, [0.0, 0.12, 0]))}, d=0.2, keep=True), TK(WRAP7, {'R': R5(add(PAP7, [0.18, 0.1, 0])), 'L': R5(add(PAP7, [-0.18, 0.12, 0]))}, {'L': 'spread'}, sq=(1.03, 0.97, 1.03), d=0.12, keep=True), TK(r(WRAP7 + 0.18), {'R': R5(add(PAP7, [-0.05, 0.22, 0])), 'L': R5(add(PAP7, [0.05, 0.22, 0]))}, sq=(1, 1, 1), d=0.12, keep=True), TK(r(WRAP7 + 0.36), {'R': R5(add(PAP7, [0.12, 0.12, 0.05])), 'L': R5(add(PAP7, [-0.12, 0.12, 0.05]))}, sq=(1.03, 0.97, 1.03), d=0.1, keep=True),   # wrapped   # fold one way, fold the other
       k(r(WRAP7 + 0.3), look='camera', lookDur=0.15), *blink(1.5, DEAD)]
st.shot('S07', 'whiteVoid', setOpts={'color': '#DCEBF2'}, look={'sunDir': [0.3, 0.9, 0.8]},
        actors=[act('poissonnier', FM7, 0, 'stand', 'neutral', keys=kf7)],
        props=[P('etal7', 'saStall', pos=ST7), P('balance7', 'saScale', pos=SCL7, opts={'weighAt': WEIGH7}), P('papier7', 'saPaper', pos=PAP7, opts={'wrapAt': WRAP7}),
               P('maillet7', 'saMallet', pos=[-0.3, 1.12, 0.0], rot=[1.5708, 0, 0.3], keys=[k(0.15, attach='poissonnier', hand='R', offset=[0, 0.04, 0], rot=[0, 0, 0]), k(r(WEIGH7 + 0.05), detach=True), k(r(WEIGH7 + 0.05), to=add(SCL7, [0, 0.47, 0]), dur=0.01), k(r(WEIGH7 + 0.05), rotTo=[0, 0, 1.5708], dur=0.01), k(r(WEIGH7 + 0.5), to=add(PAP7, [0, 0.05, 0]), dur=0.15), k(WRAP7, visible=False)]),
               P('tablier7', 'saApron', on={'actor': 'poissonnier', 'joint': 'torso', 'offset': [0, 0.35, 0.17]}, opts={'w': 0.5, 'h': 0.9})], cams=[C7])
st.cue('clang', 'S07', WEIGH7, 0.3); st.cue('whoosh', 'S07', WRAP7, 0.3)

# ================================================================= S08
# 8: a mountain campsite under snowy peaks: a flock of five seagulls glides in low; a cow with a bell looks up, and a hiker drops his sandwich
D8 = st.dur('S08'); DROP8 = r(st.at('S08', 'L08', 4))
COW8 = [-1.3, 0, 0.2]; HK8 = [0.85, 0, 0.9]; HRY8 = -30
C8 = fcam(0.0, [0.0, 1.0, 5.5], {'cow': add(COW8, [0, 1.6, 0]), 'cowF': add(COW8, [-0.9, 0, 0.3]), 'hk': add(HK8, [0, 2.35, 0]), 'hkF': HK8, 'hkR': add(HK8, [0.45, 1.3, 0]), 'sky': [0, 3.6, -1.0]}, top=0.12, bottom=0.76, push=0.2)
gulls8 = []
for i in range(5):
    a0 = [r(-7.0 - 1.0 * abs(i - 2)), r(3.4 + 0.25 * abs(i - 2)), r(-1.5 + 0.6 * (i - 2))]; a1 = [r(7.0 - 1.0 * abs(i - 2)), r(2.6 + 0.25 * abs(i - 2)), r(-1.2 + 0.6 * (i - 2))]
    gulls8.append(act(f'mouette{i + 2}' if i else 'mouetteA', a0, 90, 'fly', 'neutral', scale=1.5, keys=[k(0.0, clip='fly'), k(0.0, to=a1, dur=D8, clip='fly', ease='linear', face='keep')]))
kh8 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(off(HK8, HRY8, 0.3, 0.2, 1.45))}, {'R': 'pinch'}, HAPPY, d=0.0), k(0.6, look=[-2.0, 3.4, -1.0], lookDur=0.25), k(1.0, look=[0.5, 3.0, -1.0], lookDur=0.6),
       TK(r(DROP8 - 0.1), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 0.8}, sq=(0.93, 1.08, 0.93), d=0.06, e='out', keep=True), TK(DROP8, {'R': R5(off(HK8, HRY8, 0.3, 0.2, 1.0))}, {'R': 'spread'}, d=0.1, keep=True), TK(r(DROP8 + 0.3), sq=(1, 1, 1), d=0.12, keep=True), *blink(r(DROP8 + 0.6), {'lid': 0.1, 'mouth': 'O', 'brow': 0.8})]
st.shot('S08', 'grassland', setOpts={'grass': '#7CB458'}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('vache', COW8, 40, 'idle', 'neutral', keys=[k(0.0, clip='eat'), k(0.7, clip='idle', blend=0.1), k(0.7, look=[-1.0, 3.5, -1.0], lookDur=0.3), k(1.6, look=[1.0, 3.0, -1.0], lookDur=0.6)]), act('randonneur', HK8, HRY8, 'stand', 'neutral', keys=kh8), *gulls8],
        props=[P('sommets8', 'mountainRange', pos=[0, 0, -26.0], opts={'n': 7, 'w': 60, 'h': 18}), P('tente8a', 'saTent', pos=[-0.6, 0, -2.6], ry=10, opts={'color': '#3E8ACC'}), P('tente8b', 'saTent', pos=[2.4, 0, -3.2], opts={'color': '#E8C030'}),
               P('cloche8', 'saBell', on={'actor': 'vache', 'joint': 'neck', 'offset': [0, -0.12, 0.12]}), P('sandwich8', 'saSandwich', on={'actor': 'randonneur', 'hand': 'R', 'offset': [0, 0.0, 0.05]}, keys=[k(DROP8, detach=True), k(r(DROP8 + 0.35), to=add(HK8, [0.3, 0.03, 0.35]), dur=0.25, ease='in')])], cams=[C8])   # (round 2) it hangs in the air a beat, then drops
st.cue('gust', 'S08', 0.2, 0.4); st.cue('thud', 'S08', 0.8, 0.25); st.cue('pop', 'S08', r(DROP8 + 0.35), 0.25)

# ================================================================= S09
# 9: night in deep blue, tents lit from inside: three seagulls each pull a sardine out of the ground by the tail like a worm; the fish stretches and pops
#    free, the tent sags and lifts. In the foreground his orange tent: the peg-holding seagull on its ridge, wings spread like a bouncer; the other gulls
#    swerve away
D9 = st.dur('S09'); CUT9 = r(st.at('S09', 'L09', 7) - 0.1); PULLS9 = [0.75, r(CUT9 + 0.2), r(CUT9 + 0.55)]; POPS9 = [1.55, r(CUT9 + 0.6), r(CUT9 + 0.95)]; GUARD9 = r(CUT9 + 0.45)   # (round 2) two cuts: close on one gull, then the wide
BG9 = [[-2.6, 0, -2.6], [-0.2, 0, -3.4], [2.3, 0, -2.8]]; BGC9 = ['#3E8ACC', '#E8C030', '#5EAA4A']
H9 = [1.15, 0, 0.6]   # his tent, foreground right
def cornerOf(p, w=1.3): return [r(p[0] - w / 2 * 1.55 * 0.707), 0, r(p[2] + w / 2 * 1.55 * 0.707)]
C0_9 = cornerOf(BG9[0])
C9 = fcam(0.0, add(C0_9, [0.7, 0.55, 2.2]), {'gull': add(C0_9, [-0.4, 0.85, 0.35]), 'sard': add(C0_9, [0, 0.75, 0]), 'tentT': add(BG9[0], [0, 1.0, 0]), 'gullF': add(C0_9, [-0.9, 0, 0.9])}, top=0.14, bottom=0.76, push=0.15)   # close: the sardine pulled like a worm
C9b = fcam(CUT9, [0.7, 0.9, 3.6], {'h9': add(H9, [0, 2.35, 0]), 'h9R': add(H9, [0.95, 0.4, 0.2]), 'h9L': add(H9, [-0.95, 0.4, 0.2]), 'h9F': add(H9, [0, 0, 0.9]), 'bg1': add(BG9[1], [0, 1.0, 0])}, top=0.12, bottom=0.76, push=0.2)   # the guard on his orange tent
gulls9, sards9 = [], []
for i, (p, t0, tp) in enumerate(zip(BG9, PULLS9, POPS9)):
    c = cornerOf(p); g = add(c, [-0.35, 0, 0.3]); nm = f'mouette{i + 2}'
    gulls9.append(act(nm, add(g, [-0.5, 0, 0.4]) if i == 0 else g, 135, 'idle', 'neutral', scale=1.7, keys=[k(0.0, look=add(c, [0, 0.1, 0])), k(r(t0 - 0.15), clip='peck', blend=0.05), k(t0, clip='idle', blend=0.05), k(0.0, clip='walk' if i == 0 else 'idle'), *([k(0.0, to=g, dur=0.5, clip='walk', ease='out', face='keep')] if i == 0 else []), k(t0, to=add(g, [-0.25, 0, 0.25]), dur=r(tp - t0), ease='inOut', face='keep'), k(tp, clip='hop', blend=0.05), k(tp, to=add(g, [-0.6, 0, 0.55]), dur=0.4, clip='hop', face='keep')]))
    sards9.append(P(f'sardine9_{i}', 'saSardine', pos=add(c, [0, 0.12, 0]), rot=[1.5708, 0, 0], opts={'len': 0.34, 'wiggle': True, 'stretch': [[t0, 0], [r(tp - 0.05), 1.2], [r(tp + 0.04), -0.2], [r(tp + 0.14), 0]]}, keys=[k(tp, attach=nm, joint='head', offset=[0, -0.03, 0.14], rot=[0, 0, 0])]))
    sards9.append(P(f'tente9_{i}', 'saTent', pos=p, opts={'color': BGC9[i], 'w': 1.3, 'h': 0.95, 'lit': True, 'sag': [[tp, 0], [r(tp + 0.15), 0.7]], 'lift': [[r(tp + 0.15), 0], [r(tp + 0.5), 0.25], [r(tp + 1.2), 0.35]], 'tilt': [[r(tp + 0.15), 0], [r(tp + 1.0), 0.45]]}, inDark=True))
SW9a, SW9b = [-0.2, 2.2, 1.8], [3.6, 3.4, 0.4]
gulls9.append(act('mouette5', [-2.6, 2.4, 2.2], 80, 'fly', 'neutral', scale=1.5, keys=[k(0.0, clip='fly'), k(CUT9, to=SW9a, dur=0.6, clip='fly', ease='inOut', face='keep'), k(r(GUARD9 + 0.15), to=SW9b, dur=0.7, clip='flee', ease='out', face='keep'), k(r(GUARD9 + 0.15), face=40, turn=0.15)]))   # swerves away
st.shot('S09', 'grassland', setOpts={'grass': '#4E7A40', 'sky': ['#1E3C78', '#3A5A9A'], 'clouds': 0}, look={'sunDir': [0.3, 0.9, 0.6]}, **NIGHT,
        actors=[*gulls9, GULL('mouette', add(H9, [0, 1.08, 0]), -20, 'idle', keys=[k(0.0, look=add(cornerOf(H9, 1.6), [0, 0.2, 0])), k(r(GUARD9 - 0.25), clip='sit', blend=0.06), k(GUARD9, clip='celebrate', blend=0.03), k(GUARD9, look=SW9a, lookDur=0.1), k(r(GUARD9 + 1.0), clip='idle', blend=0.15), k(r(GUARD9 + 1.05), look=add(cornerOf(H9, 1.6), [0, 0.2, 0]), lookDur=0.2)])],
        props=[P('tente9', 'saTent', pos=H9, opts={}, inDark=True), P('sardine9', 'saSardine', pos=add(cornerOf(H9, 1.6), [0, 0.17, 0]), rot=[1.5708, 0, 0], opts={'len': 0.36}), PEG('piquet9'), *sards9], cams=[C9, C9b])
for t_ in POPS9: st.cue('pop', 'S09', t_, 0.3)
st.cue('clack', 'S09', GUARD9, 0.4)

# ================================================================= S10
# 10: the sky over fields: a V of exactly five plain dome tents (one in the lead, two on each arm) flies past, guy ropes trailing, one camper in a
#     sleeping bag dangling from the lead tent; no other tent, no speck. Below, a farmer leaning on a fence with a pitchfork looks up and lifts his cap.
#     MIGRATION card
D10 = st.dur('S10'); CAP10 = r(st.at('S10', 'L10', 7))
FA10 = [1.3, 0, -0.6]; FRY10 = -30
V10 = [[0, 0, 0], [-1.3, 0.35, -1.0], [1.3, 0.35, -1.0], [-2.6, 0.7, -2.0], [2.6, 0.7, -2.0]]; VC10 = ['#E8913A', '#3E8ACC', '#E8C030', '#5EAA4A', '#8A5AB0']
VA, VB = [2.6, 4.5, -4.5], [-3.2, 4.3, -4.5]   # (round 2) the lead's path: heading -X, nose to the frame's left; whole V in frame
def vpos(o_, p):   # the V turned to fly along +X: its arms trail back (-X)
    return [r(p[0] - o_[2] * 1.5), r(p[1] + o_[0] * 0.7), r(p[2] - abs(o_[0]) * 0.25)]   # (round 2) the V stands in a plane facing us: one arm up, one down
C10 = cam(0.0, [-0.3, 0.9, 5.2], [-0.32, 0.95, 4.95], [-0.2, 2.9, -3.0], [-0.3, 2.9, -3.0], lens=56)   # (round 2) a three-quarter view up at the V, the farmer in frame
kf10 = [k(0.0, clip='stand'), k(0.0, look=[-3.0, 4.5, -4.0]), TK(0.0, {'R': R5(off(FA10, FRY10, 0.3, 0.36, 1.25)), 'L': R5(off(FA10, FRY10, 0.4, -0.25, 1.15))}, {'R': 'grip', 'L': 'rest'}, CALM, bend={'spine': SP(0.1)}, d=0.0),
        k(0.5, look=[0.0, 5.0, -4.0], lookDur=1.5), TK(r(CAP10 - 0.3), {'L': R5(off(FA10, FRY10, 0.15, -0.1, 2.25))}, {'L': 'pinch'}, d=0.2, keep=True), TK(CAP10, {'L': R5(off(FA10, FRY10, 0.2, -0.15, 2.55))}, d=0.15, keep=True), TK(r(CAP10 + 0.45), {'L': R5(off(FA10, FRY10, 0.15, -0.1, 2.25))}, d=0.2, keep=True),   # he lifts his cap
        *blink(1.1, CALM), *BREATHE(0.2, D10, 0.5)]
st.shot('S10', 'grassland', setOpts={'grass': '#9CC860'}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('fermier', FA10, FRY10, 'stand', 'neutral', keys=kf10)],
        props=[*[P(f'tente10_{i}', 'saTent', pos=vpos(o_, VA), ry=90, opts={'color': VC10[i], 'ropes': False, 'trail': True, 'w': 1.3, 'h': 0.95}, keys=[k(0.0, to=vpos(o_, VB), dur=D10, ease='linear')]) for i, o_ in enumerate(V10)],
               P('sac10', 'saBag', pos=add(VA, [0, -0.1, 0]), scale=0.75, keys=[k(0.0, to=add(VB, [0, -0.1, 0]), dur=D10, ease='linear')]),
               P('cloture10', 'saFence', pos=[1.1, 0, -0.15], opts={'w': 3.2}),
               P('fourche10', 'pitchfork', pos=off(FA10, FRY10, 0.3, 0.38, 0.85), opts={'len': 1.6}), P('casquette10', 'coCap', on={'actor': 'fermier', 'hand': 'L', 'offset': [0, 0.02, 0.05]}, opts={'s': 0.8}, keys=[k(0.0, attach='fermier', joint='head', offset=[0, 0.42, 0]), k(r(CAP10 - 0.1), attach='fermier', hand='L', offset=[0, 0.02, 0.05]), k(r(CAP10 + 0.6), attach='fermier', joint='head', offset=[0, 0.42, 0])])], cams=[C10])   # (round 2) upright, the tines up
st.card('S10', 'MIGRATION', at=st.at('S10', 'L10', 3)); st.cue('gust', 'S10', 0.0, 0.3)

# ================================================================= S11
# 11: a hilltop: two scientists in khaki with big binoculars; one catches a low-flying tent with a giant butterfly net (a solid white cone), the other
#     clips a fat orange ring onto its pole; they let it go and it wobbles off after its V
D11 = st.dur('S11'); CATCH11 = 0.45; RING11 = 0.95; FREE11 = 1.3
SA11 = [-0.8, 0, 0.4]; SB11 = [0.75, 0, 0.5]; TT11 = [0.0, 2.2, -0.3]
NETG11 = off(SA11, 30, 0.38, 0.12, 1.2); NRY11 = yaw(NETG11, TT11); NS11 = 0.85
_a = 0.35; _ry = math.radians(NRY11); _ly, _lz = 2.8 * NS11 * math.cos(_a) - 0.3 * NS11 * math.sin(_a) * -1, 2.8 * NS11 * math.sin(_a) - 0.3 * NS11 * math.cos(_a)
CONE11 = [r(NETG11[0] + math.sin(_ry) * _lz), r(NETG11[1] + _ly), r(NETG11[2] + math.cos(_ry) * _lz)]   # (round 2) where the cone hangs at the catch   # the net's grip, in his hands; it swings toward the tent
C11 = fcam(0.0, [0.2, 1.4, 4.4], {'a': add(SA11, [0, 2.3, 0]), 'b': add(SB11, [0, 2.3, 0]), 'tent': add(CONE11, [0, 0.7, 0]), 'net': add(CONE11, [0, 0.5, 0]), 'aF': SA11, 'bF': SB11}, top=0.12, bottom=0.76, push=0.15)
ka11 = [k(0.0, clip='stand'), k(0.0, look=[-3.0, 2.2, -1.0]), TK(0.0, {'R': R5(add(NETG11, [0, -0.05, 0])), 'L': R5(add(NETG11, [0, 0.25, 0]))}, {'R': 'grip', 'L': 'grip'}, {'lid': 0.2, 'mouth': 'line', 'brow': 0.4}, d=0.0),
        TK(r(CATCH11 - 0.2), {'R': R5(add(NETG11, [-0.05, 0.05, -0.1])), 'L': R5(add(NETG11, [-0.05, 0.3, -0.12]))}, bend={'spine': SP(-0.15)}, d=0.15, keep=True), TK(CATCH11, {'R': R5(add(NETG11, [0.0, 0.0, 0.05])), 'L': R5(add(NETG11, [0.05, 0.25, 0.1]))}, bend={'spine': SP(0.2)}, sq=(1.04, 0.95, 1.04), d=0.08, e='in', keep=True),   # swoop
        k(CATCH11, look=TT11, lookDur=0.1), TK(FREE11, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.2, keep=True), k(r(FREE11 + 0.1), look=[3.0, 2.5, -1.0], lookDur=0.3)]
kb11 = [k(0.0, clip='binocs'), k(0.0, look=[-3.0, 2.2, -1.0]), k(r(CATCH11 - 0.1), clip='stand', blend=0.1), TK(r(RING11 - 0.15), {'R': R5(add(TT11, [0.3, -0.1, 0.3])), 'L': R5(add(TT11, [0.15, 0.05, 0.35]))}, {'R': 'pinch', 'L': 'pinch'}, d=0.15, keep=True), k(r(RING11 - 0.2), look=TT11, lookDur=0.1),
        TK(RING11, sq=(1.03, 0.97, 1.03), d=0.05, e='in', keep=True), TK(r(RING11 + 0.2), {'R': R5(off(SB11, -30, 0.25, 0.2, 1.1)), 'L': R5(off(SB11, -30, 0.3, -0.2, 1.1))}, {'R': 'rest', 'L': 'rest'}, sq=(1, 1, 1), d=0.2, keep=True), k(r(FREE11 + 0.1), look=[3.0, 2.5, -1.0], lookDur=0.3), *blink(1.6, CALM)]
st.shot('S11', 'grassland', setOpts={'grass': '#8CC460'}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('savant1', SA11, 30, 'stand', 'neutral', keys=ka11), act('savant2', SB11, -30, 'binocs', 'neutral', keys=kb11)],
        props=[P('tente11', 'saTent', pos=[-4.0, 2.4, -0.4], ry=90, opts={'color': '#3E8ACC', 'ropes': False, 'trail': True, 'w': 0.8, 'h': 0.6}, keys=[k(0.0, to=CONE11, dur=CATCH11, ease='out'), k(FREE11, to=[3.5, 3.0, -0.6], dur=r(D11 - FREE11), ease='in')]),
               P('filet11', 'saNet', pos=NETG11, ry=NRY11, opts={'s': NS11, 'tilt': [[0.0, -0.5], [r(CATCH11 - 0.2), -0.75], [CATCH11, 0.35], [FREE11, 0.35], [r(FREE11 + 0.25), -0.2]]}),
               P('bague11', 'saRing', on={'actor': 'savant2', 'hand': 'R', 'offset': [0, 0.0, 0.08]}, keys=[k(RING11, attach='tente11', offset=[0.0, 0.5, 0.55], rot=[0, 0, 0])]),
               P('jumelles11', 'saBinoculars', on={'actor': 'savant2', 'hand': 'L', 'offset': [0.05, 0.05, 0.05]}, keys=[k(r(CATCH11 - 0.1), visible=False)])], cams=[C11])
st.cue('whoosh', 'S11', CATCH11, 0.3); st.cue('clack', 'S11', RING11, 0.35)

# ================================================================= S12
# 12: the empty campsite, flattened yellow rectangles of grass where the tents stood; in the middle his little orange tent, the hero sipping coffee in a
#     folding chair outside it. Two seagulls glide toward it; the peg-holding seagull on the ridge spreads its wings and they swerve away at once. Then
#     it goes back to staring at the sardine corner, a drop of drool hanging from its beak
D12 = st.dur('S12'); SPREAD12 = r(st.at('S12', 'L12', 9) - 0.15); DROOL12 = r(SPREAD12 + 0.95)
CH12 = [0.95, 0, 1.15]; CRY12 = -25
GA12, GB12 = [[-3.6, 3.4, 1.4], [-4.0, 3.0, 0.6]], [[-1.3, 2.2, 1.2], [-1.7, 1.9, 0.5]]   # (round 1) they arc in, inside the frame
C12 = fcam(0.0, [-0.3, 0.85, 3.9], {'ridge': add(RIDGE, [0, 0.95, 0]), 'chairT': add(CH12, [0, 1.75, 0]), 'chairF': add(CH12, [0, 0, 0.3]), 'heroR': add(CH12, [0.5, 1.3, 0.2]), 'sard': SC, 'gB': add(GB12[0], [0, 0.4, 0])}, top=0.1, bottom=0.76, push=0.25)   # (round 2) tighter, lower
CUT12 = r(SPREAD12 + 0.85)
C12b = cam(CUT12, [-0.55, 1.35, 1.9], [-0.5, 1.33, 1.75], [-0.15, 1.38, 0.1], [-0.15, 1.36, 0.1], lens=40)   # close on the guard: the drool string toward the sardine
MUG12, SIP12 = off(CH12, CRY12, 0.35, 0.18, 1.05), off(CH12, CRY12, 0.25, 0.08, 1.6)
kh12 = [k(0.0, clip='sit'), k(0.0, look='camera'), TK(0.0, {'R': R5(MUG12), 'L': R5(off(CH12, CRY12, 0.3, -0.22, 0.85))}, {'R': 'grip', 'L': 'rest'}, {'lid': 0.4, 'mouth': 'line', 'brow': 0.1}, d=0.0),
        TK(0.35, {'R': R5(SIP12)}, sq=(1.02, 1.03, 1.02), bend={'neck': SP(-0.2)}, d=0.3, keep=True), TK(0.75, face={'lid': 0.8, 'mouth': 'O', 'brow': 0.1}, d=0.08, keep=True), TK(1.15, {'R': R5(MUG12)}, sq=(1, 1, 1), face={'lid': 0.4, 'mouth': 'smile', 'brow': 0.2}, bend={'neck': SP(0.0)}, d=0.3, keep=True), *blink(0.8, CALM), k(r(SPREAD12 + 0.2), look=[-3.0, 2.5, 1.0], lookDur=0.3), k(r(SPREAD12 + 1.0), look='camera', lookDur=0.3), *blink(2.6, CALM), *BREATHE(0.2, D12, 0.6)]   # (round 1) a sip, a breath
kgs12 = [act(f'mouette{i + 2}', GA12[i], 90, 'fly', 'neutral', scale=1.5, keys=[k(0.0, clip='fly'), k(0.4, to=GB12[i], dur=r(SPREAD12 - 0.3), clip='fly', ease='inOut', face='keep'), k(r(SPREAD12 + 0.1), clip='flee', blend=0.05), k(r(SPREAD12 + 0.1), face=-60, turn=0.12), k(r(SPREAD12 + 0.1), to=[-4.5, 3.6, -2.8 + 1.2 * i], dur=0.7, clip='flee', ease='out', face='keep')]) for i in range(2)]
kg12 = [k(0.0, clip='idle'), k(0.0, look=add(SC, [0, 0.2, 0])), k(r(SPREAD12 - 0.6), look=GB12[0], lookDur=0.15), k(r(SPREAD12 - 0.3), clip='sit', blend=0.08), k(SPREAD12, clip='celebrate', blend=0.03), k(SPREAD12, look=[-2.4, 2.0, 0.6], lookDur=0.08), k(r(SPREAD12 + 0.75), clip='idle', blend=0.15), k(r(SPREAD12 + 0.95), look=add(SC, [0, 0.2, 0]), lookDur=0.2), k(r(SPREAD12 + 1.0), look=add(SC, [0.05, 0.15, 0.05]), lookDur=0.4)]   # (round 1) crouch... then the wings spread wide
st.shot('S12', 'grassland', setOpts=MEADOW, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', CH12, CRY12, 'sit', 'neutral', keys=kh12), GULL('mouette', RIDGE, -40, 'idle', keys=kg12), *kgs12],
        props=[TENT_('tente12'), P('sardine12', 'saSardine', pos=add(SC, [0, 0.17, 0]), rot=[1.5708, 0, 0], opts={'len': 0.36}), PEG('piquet12'),
               P('chaise12', 'saChair', pos=CH12, ry=CRY12), P('tasse12', 'coMug', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.02, 0.06]}, opts={'steam': True}),
               P('herbe12', 'saFlats', pos=[0, 0, 0], opts={'spots': [[-3.2, -1.6, 1.6, 1.6, 0.2], [2.9, -2.2, 1.5, 1.5, -0.1], [-1.2, -3.8, 1.6, 1.6, 0.4], [3.4, 1.4, 1.4, 1.4, 0.1], [-3.6, 1.8, 1.5, 1.5, -0.3]]}),
               P('bave12', 'saDrool', on={'actor': 'mouette', 'joint': 'head', 'offset': [0, -0.03, 0.1]}, opts={'at': DROOL12, 'len': 0.45})], cams=[C12, C12b])
st.cue('clack', 'S12', SPREAD12, 0.4); st.cue('pop', 'S12', 0.4, 0.15)

# ================================================================= S13
# 13: two cuts. Outside: the little tent bulges and squashes like a balloon, arms and feet poking out of the door; two campers push a third in head first.
#     Cut: the tent seen straight from above, its top cut away: five sleepers head to toe like sardines in a tin, the hero in the middle; all five blink
D13 = st.dur('S13'); CUT13 = r(st.at('S13', 'L13', 6) - 0.1); PUSH13 = 0.55; IN13 = 1.1
C13 = fcam(0.0, [1.5, 1.7, 4.6], {'tent': [0, 1.5, 0], 'tentF': [0, 0, 0.9], 'pushA': [-0.9, 2.3, 1.7], 'pushB': [0.6, 2.3, 1.9], 'gull': [1.45, 0.8, 1.0]}, top=0.12, bottom=0.76, push=0.2)
C13b = cam(CUT13, [0.0, 5.0, 0.42], [0.0, 4.7, 0.4], [0.0, 0.0, 0.35], [0.0, 0.0, 0.35], lens=54)   # (round 1) straight down, nearer; the floor in the upper part of the frame, every face above 75 %
PA13, PB13, PC13 = [-0.8, 0, 1.45], [0.8, 0, 1.5], [0.0, 0, 1.35]
kpush = lambda p, s: [k(0.0, clip='stand'), k(0.0, look=add(PC13, [0, 1.0, 0])), TK(0.0, {'R': R5(add(PC13, [s * 0.15, 1.0, 0.25])), 'L': R5(add(PC13, [s * 0.05, 0.9, 0.2]))}, {'R': 'spread', 'L': 'spread'}, {'lid': 0.2, 'mouth': 'line', 'brow': 0.5}, bend={'spine': SP(0.3)}, d=0.0),
                      TK(PUSH13, {'R': R5(add(PC13, [s * 0.1, 0.8, -0.3])), 'L': R5(add(PC13, [s * 0.02, 0.7, -0.35]))}, bend={'spine': SP(0.55)}, sq=(1.05, 0.93, 1.05), d=0.15, keep=True), TK(r(IN13 + 0.1), sq=(1, 1, 1), bend={'spine': SP(0.1)}, d=0.2, keep=True), k(r(IN13 + 0.2), look='camera', lookDur=0.2), k(CUT13, visible=False)]
kc13 = [TK(PUSH13, sq=(1.25, 0.75, 1.25), d=0.06, keep=True), TK(r(PUSH13 + 0.12), sq=(0.85, 1.25, 0.85), d=0.08, keep=True), k(0.0, clip='diveIn'), k(0.0, to=add(PC13, [0, 0, 0.3]), dur=0.01), k(PUSH13, to=[0.0, 0, 0.55], dur=r(IN13 - PUSH13), clip='diveIn', ease='in', face='keep'), k(IN13, visible=False)]
SLEEP13 = [[-0.9, 0.05, 0.0, 0], [-0.45, 0.05, 0.0, 180], [0.0, 0.05, 0.0, 0], [0.45, 0.05, 0.0, 180], [0.9, 0.05, 0.0, 0]]   # x, y, z, ry: head to toe
BLINKS13 = [r(CUT13 + 0.45), r(CUT13 + 1.15)]
def ksleep(i):
    face = {'lid': 0.35, 'mouth': 'line', 'brow': 0.3}
    return [k(0.0, visible=False), k(CUT13, visible=True), k(0.0, clip='lieBack'), TK(0.0, face=face, d=0.0), *[x for b in BLINKS13 for x in blink(b, face)], k(0.0, look='camera')]
sleepers = [act('mec' if i == 2 else f'dormeur{i + 1}', [s[0], s[1], s[2]], s[3], 'lieBack', 'neutral', keys=ksleep(i)) for i, s in enumerate(SLEEP13)]
st.shot('S13', 'grassland', setOpts=MEADOW, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('campeur1', PA13, 160, 'stand', 'neutral', keys=kpush(PA13, 1)), act('campeur2', PB13, 200, 'stand', 'neutral', keys=kpush(PB13, -1)), act('campeur3', PC13, 180, 'diveIn', 'neutral', keys=kc13),
                GULL('mouette', [1.5, 0, 1.0], -60, 'idle', keys=[k(0.0, look=add(SC, [0, 0.2, 0])), k(CUT13, visible=False)]), *sleepers],
        props=[P('tente13', 'saTent', pos=TENT, opts={'bulge': [[0, 0.6], [0.25, 1.4], [0.45, 0.8], [0.7, 1.6], [IN13, 0.9], [r(IN13 + 0.12), 2.2], [r(IN13 + 0.3), 1.4], [r(IN13 + 0.5), 1.8], [CUT13, 1.6]]}, keys=[k(CUT13, visible=False)]),
               P('membres13', 'saLimbs', pos=[0, 0.0, 0.82], keys=[k(CUT13, visible=False)]), PEG('piquet13', keys=[k(CUT13, visible=False)]),
               P('coupe13', 'saTentCut', pos=TENT, opts={'w': 2.45, 'd': 2.5}, keys=[k(0.0, visible=False), k(CUT13, visible=True)]),
               *[P(f'couverture13_{i}', 'saBlanket', pos=[s_[0], 0.05, r(0.32 if s_[3] == 0 else -0.32)], ry=s_[3], opts={'w': 0.46, 'l': 1.15, 'color': ['#3E6A9A', '#5EAA4A', '#8A5AB0', '#E8C030', '#3E8ACC'][i]}, keys=[k(0.0, visible=False), k(CUT13, visible=True)]) for i, s_ in enumerate(SLEEP13)]], cams=[C13, C13b])
st.cue('pop', 'S13', 0.3, 0.3); st.cue('pop', 'S13', IN13, 0.4)

# ================================================================= S14
# 14: ground-level close-up on the tent corner at dawn: an empty hole, the guy rope slack. Next to it the seagull, its belly now round, licks its beak
#     beside a clean fish skeleton as long as itself, white on dark soil, then picks the chrome peg back up in its beak
D14 = st.dur('S14'); LICK14 = [0.35, 0.75]; PICK14 = 1.35
G14 = add(SC, [0.6, 0, 0.35]); BONES14 = add(SC, [0.1, 0.0, 0.65]); PEGG14 = add(G14, [-0.35, 0.03, 0.3])
C14 = fcam(0.0, [0.35, 0.45, 2.7], {'hole': add(SC, [-0.25, 0, 0]), 'gull': add(G14, [0, 0.85, 0]), 'gullF': add(G14, [0.2, 0, 0.2]), 'bonesL': add(BONES14, [-0.45, 0, 0]), 'bonesR': add(BONES14, [0.45, 0, 0])}, top=0.14, bottom=0.76, push=0.12)
kg14 = [k(0.0, clip='sit'), k(0.0, look='camera'), *[x for t_ in LICK14 for x in (k(t_, clip='talk', blend=0.05), k(r(t_ + 0.25), clip='sit', blend=0.08))], k(r(PICK14 - 0.25), clip='peck', blend=0.06), k(r(PICK14 - 0.25), look=PEGG14, lookDur=0.1), k(r(PICK14 + 0.15), clip='idle', blend=0.1), k(r(PICK14 + 0.25), look='camera', lookDur=0.15)]
st.shot('S14', 'grassland', setOpts={'grass': '#8CBC64', 'sky': ['#F2C8A0', '#F8E6CC']}, look={'sunDir': [0.8, 0.5, 0.6]},
        actors=[GULL('mouette', G14, -30, 'sit', keys=kg14)],
        props=[TENT_('tente14', loose=True), P('trou14', 'saHole', pos=SC, opts={'r': 0.07}), P('aretes14', 'saBones', pos=BONES14, ry=10, opts={'len': 0.75}), P('terre14', 'saHole', pos=BONES14, opts={'r': 0.42}),
               P('ventre14', 'saBelly', on={'actor': 'mouette', 'joint': 'body', 'offset': [0, -0.03, 0.03]}, opts={'r': 0.12}),
               P('piquet14', 'saPeg', pos=PEGG14, ry=60, keys=[k(PICK14, attach='mouette', joint='head', offset=[0.02, -0.01, 0.1], rot=[0.1, 0.9, 0])])], cams=[C14])
st.cue('pop', 'S14', LICK14[0], 0.2); st.cue('pop', 'S14', 1.0, 0.3)

# ================================================================= S15
# 15: the loose corner lifts and the whole bulging tent starts to rise, feet dangling out of the door; the hero, outside, jumps and grabs the guy rope
#     with both mittens and gets pulled up onto tiptoe
D15 = st.dur('S15'); RISE15 = 0.3; LIFT15 = 0.7; GRAB15 = r(st.at('S15', 'L15', 4) - 0.1); JUMP15 = r(GRAB15 - 0.25); TOP15 = r(JUMP15 + 0.22); HANG15 = r(TOP15 + 0.13)
HP15 = [-1.55, 0, 1.75]; HRY15 = 140   # (round 2) by the loose corner, facing it, the rope already in his fists
TEND15 = add(HP15, [0.62, 0, -0.62])   # the tent drifts over him: its loose corner ends straight above his fists
TK15 = [[0.0, TENT], [LIFT15, TENT], [r(GRAB15 + 0.3), lerp3(TENT, TEND15, 0.75)], [D15, TEND15]]
LY15 = [[0.0, 0.0], [LIFT15, 0.0], [GRAB15, 1.2], [r(GRAB15 + 0.35), 2.7], [D15, 3.3]]
def kv15(keys, t):
    for (a0, v0), (a1, v1) in zip(keys, keys[1:]):
        if t <= a1: u = 0 if a1 == a0 else (t - a0) / (a1 - a0); return v0 + (v1 - v0) * u if not isinstance(v0, list) else lerp3(v0, v1, u)
    return keys[-1][1]
CORN15 = lambda t: add(kv15(TK15, t), [-0.56, r(0.05 + kv15(LY15, t) + (0.35 if t > RISE15 + 0.3 else 0.35 * max(0, t - RISE15) / 0.3)), 0.56])   # the loose corner lifts first
FIST15 = off(HP15, HRY15, 0.35, 0.0, 1.15)
C15 = fcam(0.0, [0.9, 1.1, 5.4], {'tentT': add(TEND15, [0, 3.6, 0]), 'tent0': [0.9, 1.2, 0], 'hero': add(HP15, [0, 2.7, 0]), 'heroF': add(HP15, [0, 0, 0.3]), 'heroL': add(HP15, [-0.5, 1.4, 0]), 'gull': [-2.4, 0.8, 0.9]}, top=0.1, bottom=0.76, push=0.25)
kh15 = [k(0.0, clip='stand'), k(0.0, look=[-0.3, 1.0, 0.3]), TK(0.0, {'R': R5(FIST15), 'L': R5(add(FIST15, [0.04, -0.12, 0.03]))}, {'R': 'grip', 'L': 'grip'}, WORRY, bend={'spine': SP(0.1)}, d=0.0),
        k(RISE15, look=CORN15(0.6), lookDur=0.2), TK(r(RISE15 + 0.25), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 0.8}, sq=(0.94, 1.08, 0.94), d=0.06, e='out', keep=True),   # the corner goes up: eyes out
        TK(r(LIFT15 + 0.1), {'R': R5(add(FIST15, [0.0, 0.25, -0.05])), 'L': R5(add(FIST15, [0.04, 0.12, -0.05]))}, sq=(1, 1, 1), bend={'spine': SP(-0.15)}, d=0.2, keep=True), k(LIFT15, look=CORN15(1.2), lookDur=0.3),   # the rope pulls taut
        TK(r(JUMP15 - 0.12), sq=(1.1, 0.86, 1.1), bend={'spine': SP(0.25)}, d=0.1, keep=True),   # crouch...
        k(JUMP15, to=add(HP15, [0.1, 0.5, -0.1]), dur=r(TOP15 - JUMP15), ease='out'), TK(JUMP15, {'R': R5(add(FIST15, [0.1, 1.0, -0.1])), 'L': R5(add(FIST15, [0.12, 0.86, -0.1]))}, sq=(0.88, 1.16, 0.88), bend={'spine': SP(-0.1)}, d=0.12, keep=True),   # ...jump: up the rope
        TK(TOP15, sq=(0.86, 1.2, 0.86), d=0.04, keep=True),   # hang (four frames)
        k(HANG15, to=add(HP15, [0.2, 0.14, -0.2]), dur=0.15, ease='in'), k(r(HANG15 + 0.1), clip='onTiptoes', blend=0.06),
        TK(r(HANG15 + 0.12), {'R': R5(add(FIST15, [0.25, 1.35, -0.25])), 'L': R5(add(FIST15, [0.27, 1.2, -0.25]))}, sq=(0.82, 1.25, 0.82), bend={'spine': [-0.35, 0, 0, 1.25, None], 'armL': [0, 0, 0, 1.4, None], 'armR': [0, 0, 0, 1.4, None]}, face={'lid': 0.15, 'mouth': 'wavy', 'brow': 0.8}, d=0.15, keep=True),   # stretched on tiptoe, the rope straight up, the body a diagonal
        k(r(HANG15 + 0.2), look='camera', lookDur=0.15), *blink(r(HANG15 + 0.6), WORRY)]
ROPEK15 = [[r(t_), CORN15(t_)] for t_ in [i_ * 0.1 for i_ in range(int(D15 / 0.1) + 2)]]
kg15 = [k(0.0, clip='idle'), k(0.0, look=[0, 1.0, 0]), k(0.5, clip='hop', blend=0.05), k(0.85, clip='idle', blend=0.08), k(RISE15, look=CORN15(0.8), lookDur=0.2), k(r(GRAB15 + 0.2), look=CORN15(2.0), lookDur=0.4), k(1.6, clip='peck', blend=0.1), k(1.9, clip='idle', blend=0.1)]
st.shot('S15', 'grassland', setOpts=MEADOW, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', HP15, HRY15, 'stand', 'neutral', keys=kh15), GULL('mouette', [-2.4, 0, 0.9], 70, 'idle', keys=kg15)],
        props=[P('tente15', 'saTent', pos=TENT, opts={'loose': True, 'flap': [[0.0, D15]], 'bulge': [[0, 0.9], [0.4, 1.2], [0.6, 0.9]], 'lift': [[x_[0], x_[1]] for x_ in LY15], 'tilt': [[RISE15, 0], [r(RISE15 + 0.3), 0.2], [r(GRAB15 + 0.3), 0.08]], 'tiltX': [[RISE15, 0], [r(RISE15 + 0.3), -0.2], [r(GRAB15 + 0.3), -0.06]]},
                 keys=[k(LIFT15, to=TK15[2][1], dur=r(GRAB15 + 0.3 - LIFT15), ease='inOut'), k(r(GRAB15 + 0.3), to=TEND15, dur=r(D15 - GRAB15 - 0.3), ease='out')]),
               P('corde15', 'tieRope', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.0, 0.0]}, opts={'toKeys': ROPEK15, 'w': 0.03, 'color': '#E8E2D0', 'color2': '#E8E2D0'}),
               P('membres15', 'saLimbs', pos=[0, 0.05, 0.82], rot=[0.9, 0, 0], keys=[k(t_, to=add(add(kv15(TK15, t_), [0, kv15(LY15, t_), 0]), [0, 0.05, 0.82]), dur=0.1, ease='linear') for t_ in [r(i_ * 0.1) for i_ in range(int(D15 / 0.1) + 1)]]), PEG('piquet15')], cams=[C15])
st.cue('whoosh', 'S15', RISE15, 0.3); st.cue('pop', 'S15', GRAB15, 0.3)

# ================================================================= S16
# 16: the final shot, camera at about 2.3 m looking down about 17 degrees, the hole's edge high above the subtitle band: the tent sits firmly back on the
#     grass. At its corner the hero is planted chest-deep, tilted at 45 degrees like a peg, his red tie knotted to the guy rope and pulled taut; three
#     heads peek out of the tent door. The seagull lands on the tent's ridge, never on his head, and drops the chrome peg in the grass right at his chest.
#     He looks down at it. Hold one beat, deadpan
D16 = st.dur('S16'); LAND16 = 1.0; DROP16 = r(st.at('S16', 'L16', 7) + 0.1); HIT16 = r(DROP16 + 0.38); LOOK16 = r(HIT16 + 0.08)
H16 = [-1.0, 0, 1.0]; TILT16 = 0.785; BUR16 = 1.0   # the hole; 45 degrees; his feet 1.03 m down and 1.03 m toward the tent: he crosses the ground at the hole
HP16 = [r(H16[0] + BUR16), -BUR16, H16[2]]; HRY16 = 0
HEAD16 = [r(H16[0] - 0.42), 0.45, r(H16[2] + 0.05)]; PEGL16 = [r(H16[0] - 0.05), 0.04, r(H16[2] + 0.5)]   # his head; the peg lands in front of his chest, in his eyeline
TIE16 = [-0.3, 0.98, 0.3]   # the rope point high on the dome
C16 = cam(0.0, [-1.3, 2.3, 6.6], [-1.3, 2.25, 6.1], [-1.2, 0.55, 0.75], [-1.2, 0.53, 0.75], lens=42)   # (round 2) a slow push-in   # (round 1) about 17 degrees down; his head and the peg in the middle third
chk('S16', C16, {'hole': H16, 'holeF': add(H16, [0, 0, 0.4]), 'ridge': [0, 1.95, 0], 'head': HEAD16, 'peg': PEGL16, 'tentR': [0.85, 0, 0.6]})
PEND16 = {'hits': [-31.4], 'amp': TILT16, 'freq': 0.05, 'damp': 0.0, 'dir': 1}
kh16 = [k(0.0, clip='statueRock', params=PEND16, blend=0.0), k(0.0, look='camera'), TK(0.0, face=DEAD, d=0.0), *blink(1.3, DEAD),
        TK(r(HIT16 + 0.02), face={**DEAD, 'lid': 0.0, 'pop': 0.9, 'brow': 0.9}, d=0.04, e='out', keep=True), TK(r(HIT16 + 0.28), face={**DEAD, 'gy': 0.8}, d=0.06, keep=True),   # a brief take as it lands; then the eyes go down first...
        TK(r(LOOK16 + 0.2), face={**DEAD, 'gy': 0.9, 'lid': 0.35}, d=0.2, keep=True), *blink(r(LOOK16 + 1.0), {**DEAD, 'gy': 0.8}), *BREATHE(0.2, D16, 0.6, 0.008)]   # ...then the head; held, one blink
HEADS16 = [[0.0, -1.82, 0.97], [0.05, -1.57, 0.9], [-0.05, -1.32, 0.84]]   # three heads stacked in the door, the lowest in front (their bodies down in the ground)
kheads = lambda i: [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, face={'lid': 0.3, 'mouth': 'line', 'brow': 0.3}, d=0.0), *BREATHE(r(0.1 * i), D16, 0.55, 0.02), *[TK(r(0.5 + 0.9 * j + 0.2 * i), bend={'neck': [0, 0.12 * (-1) ** (i + j), 0, 1, None]}, d=0.3, keep=True) for j in range(4)], k(r(LOOK16 + 0.1 + 0.05 * i), look=PEGL16, lookDur=0.3), *blink(r(LOOK16 + 1.0), {'lid': 0.3, 'mouth': 'line', 'brow': 0.3})]
GA16 = [-3.0, 2.6, -1.4]; GB16 = [-0.9, 1.85, -0.3]
kg16 = [k(0.0, clip='fly'), k(0.0, to=GB16, dur=r(LAND16 - 0.4), clip='fly', ease='inOut', face='keep'), k(r(LAND16 - 0.4), to=RIDGE, dur=0.4, clip='fly', ease='out', face='keep'), k(r(LAND16 - 0.05), clip='hop', blend=0.04), k(r(LAND16 + 0.15), clip='idle', blend=0.12),   # glide, settle, the wings fold   # (round 2) a 12-frame glide down
        k(r(LAND16 + 0.25), look=PEGL16, lookDur=0.15), k(r(DROP16 - 0.12), clip='peck', blend=0.05), k(r(DROP16 + 0.15), clip='idle', blend=0.1), k(r(DROP16 + 0.5), look='camera', lookDur=0.2)]
st.shot('S16', 'grassland', setOpts=MEADOW, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', HP16, HRY16, 'statueRock', 'neutral', keys=kh16), *[act(f'campeur{i + 1}', p, 0, 'stand', 'neutral', keys=kheads(i)) for i, p in enumerate(HEADS16)], GULL('mouette', GA16, 120, 'fly', keys=kg16)],
        props=[TENT_('tente16', loose=True, looseUntil=0.0, ropeY=0.3), P('trou16', 'saHole', pos=H16, opts={'r': 0.33}),
               P('cravate16', 'tieRope', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.45, 0.16]}, opts={'to': TIE16, 'w': 0.075}),
               P('piquet16', 'saPeg', on={'actor': 'mouette', 'joint': 'head', 'offset': [0.02, -0.01, 0.1], 'rot': [0.1, 0.9, 0]},
                 keys=[k(DROP16, detach=True), k(DROP16, to=lerp3(RIDGE, PEGL16, 0.45), dur=0.2, ease='out'), k(r(DROP16 + 0.2), to=PEGL16, dur=0.18, ease='in'), k(DROP16, rotTo=[0, 1.2, 1.5708], dur=0.38),
                       k(HIT16, to=add(PEGL16, [0.03, 0.12, 0.04]), dur=0.09, ease='out'), k(r(HIT16 + 0.09), to=add(PEGL16, [0.05, 0, 0.06]), dur=0.09, ease='in')])], cams=[C16])   # it falls and bounces in front of his chest
st.cue('whoosh', 'S16', 0.2, 0.3); st.cue('clang', 'S16', HIT16, 0.4)

for g_ in [('S01', SNATCH1, 'mouette', 'peg'), ('S02', BONK2, 'mec', 'sardine'), ('S03', TEAR3, 'campeur1', 'storm'), ('S04', BONKS4[0], 'campeur1', 'bonk'), ('S05', 0.4, None, 'coast'), ('S06', GULP6, 'client', 'gulp'),
           ('S07', WEIGH7, 'poissonnier', 'mallet'), ('S08', DROP8, 'randonneur', 'gulls'), ('S09', GUARD9, 'mouette', 'guard'), ('S10', CAP10, 'fermier', 'migration'), ('S11', RING11, 'savant2', 'ring'),
           ('S12', SPREAD12, 'mouette', 'bouncer'), ('S13', IN13, 'campeur3', 'packed'), ('S14', PICK14, 'mouette', 'bones'), ('S15', GRAB15, 'mec', 'lift'), ('S16', DROP16, 'mouette', 'peg')]:
    st.gag(g_[0], g_[1], g_[2] or 'mec', g_[3])

for _sc in st.scenes:
    for _a in _sc['actors']:
        _run = {'reach': {}, 'hands': {}}
        for _kk in sorted((x for x in _a.get('keys', []) if isinstance(x, dict) and 'toon' in x), key=lambda x: x.get('at', 0)):
            for _n in ('reach', 'hands'):
                if _n in _kk['toon']: _kk['toon'][_n] = {**_run[_n], **_kk['toon'][_n]}; _run[_n] = dict(_kk['toon'][_n])
            for _sd in (_kk['toon'].get('touch') or {}):
                _run['reach'].pop(_sd, None); _kk['toon']['reach'] = {x: y for x, y in _run['reach'].items()}
print('\n'.join(CHECKS))

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
GUEST = lambda pr, seed, suit, **kw: {'preset': pr, 'seed': seed, 'hat': 'none', 'suit': suit, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX, 'tie': '#3A3D44', **kw}   # (round 2) no red tie on a guest
GULLC = {'type': 'creature', 'name': 'seagull', 'opts': {'seed': 4}}
st.write("La sardine", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'mouette': GULLC, 'mouetteA': {**GULLC, 'opts': {'seed': 11}}, **{f'mouette{i}': {**GULLC, 'opts': {'seed': 20 + i}} for i in range(2, 7)},
    **{f'campeur{i + 1}': GUEST(['sportif', 'tourist', 'fermier', 'madame'][i], 6200 + i, ['#E8C030', '#3E8ACC', '#5EAA4A', '#E8913A'][i]) for i in range(4)},
    **{f'dormeur{i}': GUEST(['tourist', 'madame', 'sportif', 'fermier', 'worker', 'politique'][i], 6210 + i, ['#3E8ACC', '#E8913A', '#5EAA4A', '#E8C030', '#8A5AB0', '#F07A1E'][i]) for i in range(6)},
    'commercant': GUEST('worker', 6220, '#2E5E9E', cuff='#FFFFFF'), 'client': GUEST('tourist', 6221, '#D9A23A'), 'poissonnier': GUEST('worker', 6222, '#F4F1EA', pants='#1E2E5A', shirt='#F4F1EA', lapel='#F4F1EA', tie='#1E2E5A', cuff='#F4F1EA'),
    'randonneur': GUEST('sportif', 6223, '#C8502A'), 'vache': {'type': 'creature', 'name': 'cow', 'opts': {'seed': 3}}, 'fermier': GUEST('fermier', 6224, '#6A7A4A', shirt='#E8C030'),
    'savant1': GUEST('worker', 6225, '#B8A070', pants='#8A7A50'), 'savant2': GUEST('madame', 6226, '#B8A070', pants='#8A7A50'),
})
