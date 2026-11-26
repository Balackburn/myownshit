#!/usr/bin/env python3
"""Le bulletin (story 110; a primary-school report stamped « Peut mieux faire », and a teacher who never looks up from her knitting).
This man found his primary-school report: « Peut mieux faire. » Thirty years on he goes back to school to do better: full marks everywhere, even in
sport; the verdict: « Peut mieux faire. » His boss reads it and fires him, then finds his own and eats it. Companies demand the reports: nobody did
better. The whole country goes back to school, the minister at the back by the radiator; the kindergarten takes the offices (meetings end at half
past four, with a snack) and the country has never been so well run. The minister hands in a blank sheet: « Peut mieux faire. » In the teacher's
drawer, forty years of papers never read, and an order from the ministry, signed without reading, by him too. For the first time the teacher reads a
paper: his. « Peut mieux faire. »
Running gag (silent): the teacher never looks up from her knitting (S02, S03, S04, S12); her orange scarf grows each time; every report carries the
same crooked red stamp (one texture). S15 she puts the knitting down; S16 the stamp becomes handwriting.
Cards: LICENCIÉ (S05), RENTRÉE (S08). No other word but the reports'; no figure anywhere (boards blank but a chalk sun, clocks with hands only), no
flag, emblem or upright cross. At most five people in a shot, two child-scale shots (S09, S10)."""
from story_kit import *
import math

st = Story('bulletin', look='natural')
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
def REPORT(pid, state='old', **kw): return P(pid, 'buReport', opts={'state': state, **kw.pop('opts', {})}, **kw)
def SHOW(pid, actor, state='old', hand='R', off=(0.0, 0.14, 0.06), **o):
    """a report held up square to the lens"""
    return P(pid, 'buReport', on={'actor': actor, 'hand': hand, 'offset': list(off), 'face': 'camera'}, opts={'state': state, **o})

# ---------------------------------------------------------------- the classroom and the running gag
# the board wall at z -3.2; the teacher's desk at the front left, she sits behind it facing the class (+Z), knitting, her eyes on her needles (never up
# before S15); her orange scarf grows: to the floor (S02), along the gym bench (S03), in heaps round her chair (S12), out of the door (S15)
TD = [-1.5, 0, -1.9]; TCH = [-1.5, 0, -2.45]; TRY = 0
LAP = add(TCH, [0, 0.62, 0.32])   # her knitting, in her lap
KNITLOOK = add(TCH, [0, 0.55, 0.45])
HC = [0.55, 0, 0.35]; HRY = 200   # his tiny chair, facing her
DOWN = {'lid': 0.55, 'mouth': 'line', 'brow': 0.1, 'gy': 0.8}   # her face: eyes down on the needles
CLASS = {'color': '#EDE3C8'}
def KNITTER(id_, pos, ry, keys_extra=(), clip='sit'):
    ks = [k(0.0, clip=clip), k(0.0, look=add(pos, [0, 0.5, 0.45])), TK(0.0, {'R': R5(add(pos, [0.08, 0.66, 0.32])), 'L': R5(add(pos, [-0.08, 0.66, 0.32]))}, {'R': 'pinch', 'L': 'pinch'}, DOWN, bend={'neck': SP(0.35)}, d=0.0),
          *[TK(r(0.2 + 0.25 * j), {'R': R5(add(pos, [0.08 + 0.02 * (j % 2), 0.67, 0.33])), 'L': R5(add(pos, [-0.08 + 0.02 * (j % 2), 0.66, 0.32]))}, d=0.12, keep=True) for j in range(14)], *keys_extra]
    return act(id_, pos, ry, clip, 'neutral', keys=ks)
def KNIT(pid, actor='maitresse'): return P(pid, 'buKnit', on={'actor': actor, 'hand': 'R', 'offset': [-0.08, 0.0, 0.04]})
def SCARF(pid, pts): return P(pid, 'buScarf', pos=pts[0], opts={'pts': [[r(p[0] - pts[0][0]), r(p[1] - pts[0][1]), r(p[2] - pts[0][2])] for p in pts]})
def LOOKS(id_): return [P(f'{id_}_perm', 'buPerm', on={'actor': id_, 'joint': 'head', 'offset': [0, 0.36, -0.01]}), P(f'{id_}_lunettes', 'buHalfMoon', on={'actor': id_, 'joint': 'head', 'offset': [0, 0.07, 0.17]})]
def TINY(pid, pos, ry=0, color='#2F62B5'): return P(pid, 'buTinyChair', pos=pos, ry=ry, opts={'color': color})
def ROWS(prefix, skip=()):
    out = []
    for i in range(3):
        for j in range(3):
            if (i, j) in skip: continue
            x, z = r(-0.7 + 1.0 * j), r(-0.4 + 0.95 * i); out += [P(f'{prefix}c{i}{j}', 'buTinyChair', pos=[x, 0, r(z + 0.3)], ry=180), P(f'{prefix}d{i}{j}', 'buTinyDesk', pos=[x, 0, z], ry=180)]
    return out


# ================================================================= S01
# 1: two cuts. The attic (a sloping room, one dusty skylight, one cardboard box): he opens the box and pulls out a yellowed school report. Close on the
#    report, square to the lens, filling the frame: grey scribble rows and the big crooked red stamp « PEUT MIEUX FAIRE »
D1 = st.dur('S01'); CUT1 = r(st.at('S01', 'L01', 8) - 0.1); PULL1 = 1.1
HK1 = [0.0, 0, 0.6]; BOX1 = [0.0, 0, 1.25]
C1 = fcam(0.0, [0.9, 1.3, 3.9], {'head': add(HK1, [0, 1.85, 0]), 'box': add(BOX1, [0.35, 0, 0.3]), 'boxL': add(BOX1, [-0.35, 0.4, 0]), 'feet': HK1}, top=0.14, bottom=0.76, push=0.25)
C1b = cam(CUT1, [0.0, 1.36, 1.45], [0.0, 1.36, 1.4], [0.0, 1.36, 0.0], [0.0, 1.36, 0.0], lens=24)   # the report fills the frame
kh1 = [k(0.0, clip='kneel'), k(0.0, look=add(BOX1, [0, 0.3, 0])), TK(0.0, {'R': R5(add(BOX1, [0.15, 0.42, 0])), 'L': R5(add(BOX1, [-0.15, 0.42, 0]))}, {'R': 'spread', 'L': 'spread'}, CALM, bend={'spine': SP(0.3)}, d=0.0),
       TK(0.45, {'R': R5(add(BOX1, [0.1, 0.25, 0.05]))}, {'R': 'pinch'}, d=0.2, keep=True), TK(PULL1, {'R': R5(add(HK1, [0.1, 1.45, 0.45]))}, sq=(0.97, 1.04, 0.97), d=0.3, keep=True), k(PULL1, look=add(HK1, [0.1, 1.45, 0.45]), lookDur=0.2),   # out comes the report
       TK(r(PULL1 + 0.4), face={'lid': 0.1, 'mouth': 'O', 'brow': 0.7}, d=0.1, keep=True), *blink(0.7, CALM), k(CUT1, visible=False)]
st.shot('S01', 'whiteVoid', setOpts={'color': '#D8C8A8'}, look={'sunDir': [0.3, 0.9, 0.5]},
        actors=[act('mec', HK1, 180, 'kneel', 'neutral', keys=kh1)],
        props=[P('grenier1', 'buAttic', pos=[0, 0, 0]), P('carton1', 'buBox', pos=BOX1, opts={'w': 0.6}),
               P('bulletin1', 'buReport', pos=add(BOX1, [0, 0.2, 0]), rot=[-1.5708, 0, 0], opts={'state': 'old', 'w': 0.36}, keys=[k(r(PULL1 - 0.3), attach='mec', hand='R', offset=[0.0, 0.16, 0.05], rot=[0, 0, 0]), k(CUT1, visible=False)]), P('bulletin1b', 'buReport', pos=[0.0, 1.36, 0.0], opts={'state': 'old', 'w': 0.36}, keys=[k(0.0, visible=False), k(CUT1, visible=True)])], cams=[C1, C1b])
st.cue('whoosh', 'S01', PULL1, 0.2); st.cue('clack', 'S01', CUT1, 0.3)

# ================================================================= S02
# 2: the classroom (the board shows only a chalk sun): he sits squeezed into a tiny chair, knees to his chin, among rows of empty tiny chairs. In front,
#    the same teacher thirty years older (short white curly perm, mustard twin-set, half-moon glasses on a chain) knits a bright orange scarf that
#    already reaches the floor, her eyes on her needles; a big wooden stamp on her desk beside the ball of wool
D2 = st.dur('S02')
C2 = fcam(0.0, [2.9, 1.45, -1.0], {'hero': add(HC, [0, 1.6, 0]), 'heroF': HC, 'tch': add(TCH, [0, 1.9, 0]), 'tchF': add(TCH, [0, 0, 0.4]), 'scarf': add(TCH, [0.2, 0, 0.9])}, top=0.12, bottom=0.76, push=0.25)
kh2 = [k(0.0, clip='sitFloor'), k(0.0, look=HEAD(TCH, 1.4)), TK(0.0, face={'lid': 0.2, 'mouth': 'line', 'brow': 0.6}, d=0.0), *blink(0.9, CALM), k(1.6, look='camera', lookDur=0.2), TK(1.6, face={'lid': 0.25, 'mouth': 'wavy', 'brow': 0.7}, d=0.1, keep=True), *blink(2.4, CALM), *BREATHE(0.2, D2, 0.5)]
SCARF2 = [add(LAP, [0.05, -0.05, 0.02]), add(TCH, [0.05, 0.35, 0.42]), add(TCH, [0.1, 0.02, 0.55])]
st.shot('S02', 'whiteVoid', setOpts=CLASS, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[act('mec', add(HC, [0, 0.33, 0]), HRY, 'sitFloor', 'neutral', keys=kh2), KNITTER('maitresse', TCH, TRY)],
        props=[P('classe2', 'buClass', pos=[0, 0, 0]), *ROWS('r2', skip=((1, 1),)), TINY('chaise2', HC, HRY), P('pupitre2', 'buTinyDesk', pos=add(HC, [-0.1, 0, -0.45]), ry=HRY),
               P('bureau2', 'buTable', pos=TD, opts={'len': 1.4}), P('chaiseM2', 'buTinyChair', pos=TCH, opts={'color': '#7A5C3A'}, scale=1.4), P('tampon2', 'buStamp', pos=add(TD, [0.35, 1.06, 0.1])), KNIT('tricot2'), SCARF('echarpe2', SCARF2), *LOOKS('maitresse')], cams=[C2])

# ================================================================= S03
# 3: two cuts. His test sheet slaps onto his tiny desk: a row of big gold stars and nothing else. Cut: the gym: he climbs the rope in his suit and tie,
#    stretching like rubber up to the ceiling and touching it; on the bench below the teacher knits, the scarf now trailing the whole bench, eyes down
D3 = st.dur('S03'); CUT3 = r(st.at('S03', 'L03', 4) - 0.1); SLAP3 = 0.3
DESK3 = [0.0, 0, 0.0]
C3 = cam(0.0, [0.0, 1.45, 0.55], [0.0, 1.4, 0.5], [0.0, 0.55, -0.05], [0.0, 0.55, -0.05], lens=40)   # down on the desk
ROPE3 = [0.8, 4.2, -0.4]; HR3 = [0.8, 0, -0.4]; BENCH3 = [-1.2, 0, -0.6]
C3b = fcam(CUT3, [-0.2, 1.3, 4.6], {'ceil': [0.8, 4.2, -0.4], 'hero': [0.8, 0.5, -0.4], 'tch': add(BENCH3, [0.3, 1.8, 0]), 'benchL': add(BENCH3, [-1.6, 0.4, 0])}, top=0.08, bottom=0.76, push=0.2)
TB3 = add(BENCH3, [0.4, 0.06, 0.05])   # she sits on the bench
kh3 = [k(0.0, visible=False), k(CUT3, visible=True), k(0.0, clip='stand'), k(CUT3, to=add(HR3, [0, 1.2, 0]), dur=0.01), TK(CUT3, {'R': R5(add(ROPE3, [0, -1.8, 0.05])), 'L': R5(add(ROPE3, [0, -2.3, 0.05]))}, {'R': 'grip', 'L': 'grip'}, face={'lid': 0.2, 'mouth': 'line', 'brow': 0.5}, d=0.0, keep=True),
       TK(r(CUT3 + 0.25), {'R': R5(add(ROPE3, [0, -0.15, 0.05])), 'L': R5(add(ROPE3, [0, -0.6, 0.05]))}, bend={'spine': [0, 0, 0, 1.25, None], 'armL': [0, 0, 0, 1.4, None], 'armR': [0, 0, 0, 1.4, None]}, sq=(0.86, 1.25, 0.86), d=0.18, e='out', keep=True),   # stretched like rubber up to the ceiling
       TK(r(CUT3 + 0.5), {'R': R5(add(ROPE3, [0.05, -0.02, 0.05]))}, {'R': 'spread'}, d=0.08, keep=True), k(r(CUT3 + 0.55), look='camera', lookDur=0.15), *blink(r(CUT3 + 0.7), CALM)]
st.shot('S03', 'whiteVoid', setOpts=CLASS, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[act('mec', HR3, 0, 'stand', 'neutral', keys=kh3), KNITTER('maitresse', TB3, 20, keys_extra=[k(0.0, visible=False), k(CUT3, visible=True)])],
        props=[P('pupitre3', 'buTinyDesk', pos=DESK3, keys=[k(CUT3, visible=False)]), P('copie3', 'buReport', pos=[0.0, 1.2, -0.05], rot=[-1.5708, 0, 0], opts={'state': 'stars', 'w': 0.34}, keys=[k(0.0, to=[0.0, 0.56, -0.05], dur=SLAP3, ease='in'), k(SLAP3, squash=[1.2, 0.6, 1.2], dur=0.2), k(CUT3, visible=False)]),
               P('gym3', 'buGym', pos=[0, 0, 0], opts={'benchX': BENCH3[0], 'benchZ': BENCH3[2]}, keys=[k(0.0, visible=False), k(CUT3, visible=True)]), P('corde3', 'rope', pos=ROPE3, opts={'len': 4.2}, keys=[k(0.0, visible=False), k(CUT3, visible=True)]),
               P('classe3', 'buClass', pos=[0, 0, 0], keys=[k(CUT3, visible=False)]), KNIT('tricot3'), SCARF('echarpe3', [add(TB3, [0.05, 0.57, 0.34]), add(TB3, [0.1, 0.45, 0.2]), add(BENCH3, [1.5, 0.46, 0.0]), add(BENCH3, [-1.55, 0.46, 0.0])]), *LOOKS('maitresse')], cams=[C3, C3b])
st.cue('thud', 'S03', SLAP3, 0.35); st.cue('pop', 'S03', r(CUT3 + 0.5), 0.3)

# ================================================================= S04
# 4: the teacher's desk: without lifting her eyes from her knitting she brings the big wooden stamp down on his new report, thunk; the report pops up to
#    the lens: three handwritten « Très bien » rows and, below them, the same crooked red stamp. His jaw drops to his chest
D4 = st.dur('S04'); THUNK4 = 0.45; POP4 = 0.7; JAW4 = 1.15
HS4 = add(TD, [1.05, 0, 0.15]); HSRY4 = -95
REP4 = add(TD, [0.25, 0.79, 0.15]); UP4 = add(TD, [0.2, 1.3, 0.75])
C4 = fcam(0.0, [0.4, 1.4, 1.5], {'rep': UP4, 'repB': add(UP4, [0, -0.3, 0]), 'hero': add(HS4, [0, 2.3, 0]), 'tch': add(TCH, [0, 1.85, 0])}, top=0.1, bottom=0.76, push=0.15)
kt4 = [TK(r(THUNK4 - 0.2), {'R': R5(add(REP4, [0.0, 0.35, 0]))}, {'R': 'grip'}, d=0.12, keep=True), TK(THUNK4, {'R': R5(add(REP4, [0.0, 0.1, 0]))}, sq=(1.04, 0.96, 1.04), d=0.05, e='in', keep=True), TK(r(THUNK4 + 0.25), {'R': R5(add(TCH, [0.08, 0.66, 0.32]))}, {'R': 'pinch'}, sq=(1, 1, 1), d=0.2, keep=True)]
kh4 = [k(0.0, clip='stand'), k(0.0, look=REP4), TK(0.0, HANDS(HS4, HSRY4), {'R': 'rest', 'L': 'rest'}, {'lid': 0.1, 'mouth': 'smile', 'brow': 0.6}, d=0.0), k(POP4, look=UP4, lookDur=0.1),
       TK(r(JAW4 - 0.06), sq=(1.05, 0.95, 1.05), d=0.05, keep=True), TK(JAW4, face={**POP, 'jaw': 1.0}, sq=(0.9, 1.12, 0.9), scl={'head': [0.9, 1.22, 0.9]}, d=0.05, e='out', keep=True), TK(r(JAW4 + 0.35), face={**POP, 'jaw': 1.0}, sq=(0.92, 1.1, 0.92), d=0.25, keep=True)]   # the jaw to his chest
st.shot('S04', 'whiteVoid', setOpts=CLASS, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[KNITTER('maitresse', TCH, TRY, keys_extra=kt4), act('mec', HS4, HSRY4, 'stand', 'neutral', keys=kh4)],
        props=[P('classe4', 'buClass', pos=[0, 0, 0]), P('bureau4', 'buTable', pos=TD, opts={'len': 1.4}), P('chaiseM4', 'buTinyChair', pos=TCH, opts={'color': '#7A5C3A'}, scale=1.4), KNIT('tricot4'), *LOOKS('maitresse'),
               P('tampon4', 'buStamp', on={'actor': 'maitresse', 'hand': 'R', 'offset': [0, 0.28, 0.02]}, keys=[k(0.0, visible=False), k(r(THUNK4 - 0.25), visible=True), k(r(THUNK4 + 0.3), visible=False)]),
               P('bulletin4', 'buReport', pos=REP4, rot=[-1.5708, 0, 0], opts={'state': 'new', 'w': 0.4}, keys=[k(POP4, to=UP4, dur=0.18, ease='out'), k(POP4, rotTo=[0, -0.3, 0], dur=0.18), k(r(POP4 + 0.18), squash=[1.15, 0.85, 1.15], dur=0.2)]),
               SCARF('echarpe4', [add(LAP, [0.05, -0.05, 0.02]), add(TCH, [0.05, 0.35, 0.42]), add(TCH, [0.15, 0.02, 0.65]), add(TCH, [0.6, 0.02, 0.9])])], cams=[C4])
st.cue('thud', 'S04', THUNK4, 0.5); st.cue('pop', 'S04', POP4, 0.3); st.cue('whoosh', 'S04', JAW4, 0.25)

# ================================================================= S05
# 5: the office: the boss (grey moustache, waistcoat) reads the report at arm's length, then points at the door without a word; the hero walks out past
#    him carrying a cardboard box, a tiny bright school backpack on his back. LICENCIÉ card
D5 = st.dur('S05'); POINT5 = 0.75; LIC5 = st.at('S05', 'L05', 4)
BO5 = [-0.3, 0, -0.7]; BRY5 = 30; HA5, HB5 = [-0.9, 0, 0.6], [3.1, 0, 0.3]
C5 = fcam(0.0, [1.0, 1.4, 3.3], {'boss': add(BO5, [0, 2.35, 0]), 'bossF': BO5, 'hA': add(HA5, [0, 2.3, 0]), 'door': [3.4, 2.0, 0.2]}, top=0.2, bottom=0.76, push=0.15)
kb5 = [k(0.0, clip='stand'), k(0.0, look=off(BO5, BRY5, 0.65, 0.1, 1.55)), TK(0.0, {'R': R5(off(BO5, BRY5, 0.65, 0.12, 1.55))}, {'R': 'pinch'}, {'lid': 0.5, 'mouth': 'line', 'brow': -0.4}, bend={'spine': SP(-0.12)}, d=0.0),
       TK(POINT5, {'R': R5(off(BO5, BRY5, 0.3, 0.2, 1.1)), 'L': R5([2.6, 1.55, 0.3])}, {'L': 'point'}, bend={'spine': SP(0.0)}, d=0.12, keep=True), k(POINT5, look=[3.4, 1.6, 0.2], lookDur=0.12), *blink(1.5, GRAVE)]
kh5 = [k(0.0, clip='stand'), k(0.0, look=HEAD(BO5, 1.9)), TK(0.0, {'R': R5(off(HA5, 90, 0.35, 0.2, 1.1)), 'L': R5(off(HA5, 90, 0.35, -0.2, 1.1))}, {'R': 'grip', 'L': 'grip'}, SAD, d=0.0),
       k(r(POINT5 + 0.25), clip='walk', blend=0.08), k(r(POINT5 + 0.25), to=HB5, dur=r(D5 - POINT5 - 0.25), clip='walk', face='keep', params={'freq': 1.4}), *WALKHANDS(r(POINT5 + 0.25), r(D5 - POINT5 - 0.25), [HA5, HB5], {'R': (0.35, 0.2, 1.1), 'L': (0.35, -0.2, 1.1)})]
st.shot('S05', 'whiteVoid', setOpts={'color': '#C8D2DA'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[act('patron', BO5, BRY5, 'stand', 'neutral', keys=kb5), act('mec', HA5, 90, 'stand', 'neutral', keys=kh5)],
        props=[P('bureau5', 'buOffice', pos=[0, 0, 0], opts={'deskZ': -1.5}), SHOW('bulletin5', 'patron', 'new', off=(0.0, 0.16, 0.05)),
               P('carton5', 'buBox', on={'actor': 'mec', 'hand': 'R', 'offset': [0.17, -0.12, 0.1]}, opts={'w': 0.45}), P('cartable5', 'buBackpack', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.45, -0.2]}, opts={'color': '#E8C030'}),
               P('moustache5', 'buMoustache', on={'actor': 'patron', 'joint': 'head', 'offset': [0, -0.02, 0.17]}), P('cheveux5', 'buHair', on={'actor': 'patron', 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'color': '#A8A8A8'})], cams=[C5])
st.card('S05', 'LICENCIÉ', at=LIC5); st.cue('thud', 'S05', LIC5, 0.3)

# ================================================================= S06
# 6: the same office, the door shut: the boss pulls his own yellowed report out of a desk drawer and holds it up beside his face to the lens: the same
#    crooked red stamp with the same blot. A sweat drop pops. He glances left and right, crumples it into a ball, swallows it in one gulp (his throat
#    bulges like a cartoon snake), and straightens his tie
D6 = st.dur('S06'); SHOW6 = 0.45; GLANCE6 = 1.0; CRUMP6 = 1.45; GULP6 = r(st.at('S06', 'L06', 7)); TIE6 = r(GULP6 + 0.55)
BO6 = [0.0, 0, -0.2]
C6 = cam(0.0, [0.15, 1.85, 1.9], [0.15, 1.84, 1.75], [0.05, 1.8, -0.2], [0.05, 1.78, -0.2], lens=34)   # close: his face and his report
kb6 = [k(0.0, clip='stand'), k(0.0, look=[0.4, 0.8, -0.6]), TK(0.0, {'R': R5(off(BO6, 0, 0.3, 0.25, 0.9))}, {'R': 'pinch'}, GRAVE, d=0.0),
       TK(SHOW6, {'R': R5(off(BO6, 0, 0.32, 0.28, 1.72))}, d=0.2, keep=True), k(SHOW6, look='camera', lookDur=0.15),   # beside his face, to the lens
       TK(r(SHOW6 + 0.3), face={'lid': 0.0, 'mouth': 'wavy', 'brow': 0.9}, d=0.06, keep=True), k(GLANCE6, look=[-2.0, 1.8, 0.5], lookDur=0.08), k(r(GLANCE6 + 0.2), look=[2.0, 1.8, 0.5], lookDur=0.08),   # left, right
       TK(CRUMP6, {'R': R5(off(BO6, 0, 0.3, 0.05, 1.4)), 'L': R5(off(BO6, 0, 0.3, -0.05, 1.4))}, {'L': 'grip', 'R': 'grip'}, d=0.12, keep=True), k(CRUMP6, look='camera', lookDur=0.1),
       TK(r(GULP6 - 0.15), {'R': R5(off(BO6, 0, 0.12, 0.0, 1.82))}, d=0.12, keep=True), TK(GULP6, face={'lid': 0.0, 'mouth': 'O', 'brow': 0.9, 'jaw': 0.6}, sq=(0.94, 1.08, 0.94), d=0.05, keep=True), TK(r(GULP6 + 0.1), {'R': R5(off(BO6, 0, 0.3, 0.25, 0.9)), 'L': R5(off(BO6, 0, 0.3, -0.2, 0.95))}, face={'lid': 0.3, 'mouth': 'line', 'brow': 0.6}, sq=(1, 1, 1), d=0.15, keep=True),   # gulp
       TK(TIE6, {'R': R5(off(BO6, 0, 0.18, 0.02, 1.62)), 'L': R5(off(BO6, 0, 0.17, -0.03, 1.5))}, {'R': 'pinch', 'L': 'pinch'}, face=GRAVE, d=0.15, keep=True), TK(r(TIE6 + 0.35), {'R': R5(off(BO6, 0, 0.3, 0.25, 0.9)), 'L': R5(off(BO6, 0, 0.3, -0.2, 0.95))}, d=0.2, keep=True), *blink(r(D6 - 0.3), GRAVE)]
st.shot('S06', 'whiteVoid', setOpts={'color': '#C8D2DA'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[act('patron', BO6, 0, 'stand', 'neutral', keys=kb6)],
        props=[P('bureau6', 'buOffice', pos=[0, 0, -0.6], opts={'desk': False}),
               P('bulletin6', 'buReport', on={'actor': 'patron', 'hand': 'R', 'offset': [0.0, 0.14, 0.05], 'face': 'camera'}, opts={'state': 'old', 'w': 0.34, 'crumple': [CRUMP6, r(CRUMP6 + 0.25)]}, keys=[k(GULP6, visible=False)]),
               DROP('goutte6', 'patron', r(SHOW6 + 0.3), offset=(0.25, 0.3, 0.05)), P('moustache6', 'buMoustache', on={'actor': 'patron', 'joint': 'head', 'offset': [0, -0.02, 0.17]}), P('cheveux6', 'buHair', on={'actor': 'patron', 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'color': '#A8A8A8'}),
               P('gorge6', 'buCrumb', pos=add(BO6, [0, 1.62, 0.1]), scale=5.0, keys=[k(0.0, visible=False), k(GULP6, visible=True), k(GULP6, to=add(BO6, [0, 1.25, 0.14]), dur=0.4, ease='in'), k(r(GULP6 + 0.42), visible=False)])], cams=[C6])   # the lump goes down his throat
st.cue('pop', 'S06', r(SHOW6 + 0.3), 0.2); st.cue('whoosh', 'S06', CRUMP6, 0.25); st.cue('pop', 'S06', GULP6, 0.4)

# ================================================================= S07
# 7: an open-plan office: a staff manager with a clipboard walks along three employees standing in a row; each holds their old report up to the lens in
#    turn, each with the same stamp. The manager reaches the end, sighs, and holds up his own: the same. Four people
D7 = st.dur('S07'); EMP7 = [[-0.85, 0, 0.0], [0.0, 0, 0.0], [0.85, 0, 0.0]]; UPS7 = [0.35, 0.95, 1.55]; OWN7 = r(st.at('S07', 'L07', 6) + 0.1)
MA7, MB7 = [-1.5, 0, 0.75], [1.55, 0, 0.75]
C7 = fcam(0.0, [0.0, 1.35, 3.6], {'e0': add(EMP7[0], [-0.3, 2.3, 0]), 'e2': add(EMP7[2], [0.3, 2.3, 0]), 'm': add(MB7, [0.3, 2.3, 0]), 'mA': add(MA7, [-0.2, 2.3, 0])}, top=0.14, bottom=0.76, push=0.2)
emps7 = []
for i, (p, t_) in enumerate(zip(EMP7, UPS7)):
    nm = f'employe{i + 1}'
    emps7.append(act(nm, p, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, {'R': R5(off(p, 0, 0.3, 0.22, 0.95))}, {'R': 'pinch'}, CALM, d=0.0), TK(t_, {'R': R5(off(p, 0, 0.38, 0.12, 1.75))}, d=0.18, keep=True), TK(r(t_ + 0.3), face={'lid': 0.3, 'mouth': 'wavy', 'brow': 0.6}, d=0.08, keep=True), *blink(r(0.8 + 0.4 * i), CALM)]))
km7 = [k(0.0, clip='walk'), k(0.0, to=MB7, dur=r(OWN7 - 0.2), clip='walk', face='keep', params={'freq': 1.3}), k(r(OWN7 - 0.2), clip='stand', blend=0.1), *[k(t_, look=HEAD(EMP7[i], 1.7), lookDur=0.15) for i, t_ in enumerate(UPS7)],
       TK(0.0, {'L': R5(off(MA7, 90, 0.3, -0.15, 1.1))}, {'L': 'pinch'}, CALM, d=0.0), TK(r(OWN7 - 0.25), sq=(1.04, 0.95, 1.04), bend={'spine': SP(0.2)}, face={'lid': 0.6, 'mouth': 'line', 'brow': 0.4}, d=0.15, keep=True),   # a sigh
       k(r(OWN7 - 0.1), face=0, turn=0.15), TK(OWN7, {'R': R5(off(MB7, 0, 0.38, 0.12, 1.75))}, {'R': 'pinch'}, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.2, keep=True), k(OWN7, look='camera', lookDur=0.15)]
st.shot('S07', 'whiteVoid', setOpts={'color': '#D8DEE4'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[*emps7, act('chef', MA7, 90, 'walk', 'neutral', keys=km7)],
        props=[P('plateau7', 'buOffice', pos=[0, 0, -0.8], opts={'desk': False}), *[P(f'poste7_{i}', 'buDesk', pos=[x, 0, -1.5]) for i, x in enumerate([-1.6, 0.0, 1.6])],
               *[SHOW(f'bulletin7_{i}', f'employe{i + 1}', 'old', off=(0.0, 0.14, 0.05), w=0.3) for i in range(3)], SHOW('bulletin7_c', 'chef', 'old', off=(0.0, 0.14, 0.05), w=0.3),
               P('chemise7', 'buFiles', on={'actor': 'chef', 'hand': 'L', 'offset': [0, 0.05, 0.05]}, opts={'n': 2}), P('cheveux7', 'buHair', on={'actor': 'chef', 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'color': '#8A5A32'})], cams=[C7])
for t_ in UPS7: st.cue('whoosh', 'S07', t_, 0.15)

# ================================================================= S08
# 8: two cuts. A school gate in morning light (plain railings, no lettering, no flag): four grown-ups in suits and work clothes file through, each with a
#    small bright school backpack, one swinging a lunchbox; a lollipop lady holds up a plain coloured disc. Five people. RENTRÉE card. Cut: the classroom
#    back row: the minister (dark suit, no sash, no badge) squeezed into the last tiny desk beside the radiator, knees to his chin, gazing out of the window
D8 = st.dur('S08'); CUT8 = r(st.at('S08', 'L08', 7) - 0.1)
GA8 = [[-3.4, 0, 2.2], [-4.4, 0, 2.6], [-5.4, 0, 2.2], [-6.4, 0, 2.6]]; GB8 = [[1.0, 0, -1.6], [0.1, 0, -1.0], [-0.8, 0, -0.5], [-1.7, 0, 0.1]]
LADY8 = [1.3, 0, 1.4]
C8 = fcam(0.0, [2.4, 1.3, 5.2], {'gate': [0.0, 1.9, 0.0], 'lady': add(LADY8, [0, 2.3, 0]), 'a1': add(GB8[1], [0, 2.3, 0]), 'a3': add(lerp3(GA8[3], GB8[3], 0.5), [0, 2.3, 0]), 'f': [0, 0, 2.6]}, top=0.2, bottom=0.76, push=0.2)
MIN8 = [-3.0, 0.33, 0.5]; MRY8 = -110
C8b = fcam(CUT8, [-1.2, 1.3, 2.6], {'min': add(MIN8, [0, 1.6, 0]), 'minF': add(MIN8, [0, -0.33, 0.2]), 'win': [-4.1, 2.3, 0.2], 'rad': [-4.0, 0.2, 0.6]}, top=0.14, bottom=0.76, push=0.15)
adults8 = []
for i in range(4):
    nm = ['adulte1', 'adulte2', 'adulte3', 'adulte4'][i]
    adults8.append(act(nm, GA8[i], 60, 'walk', 'neutral', keys=[k(0.0, clip='walk'), k(0.0, to=GB8[i], dur=r(CUT8 - 0.05), clip='walk', ease='linear', face='keep', params={'freq': 1.6}), k(0.0, look=add(GB8[i], [0, 1.7, -1])), k(CUT8, visible=False)]))
klady = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(off(LADY8, -30, 0.25, 0.25, 1.35))}, {'R': 'grip'}, HAPPY, d=0.0), *blink(0.8, HAPPY), k(CUT8, visible=False)]
kmin8 = [k(0.0, visible=False), k(CUT8, visible=True), k(0.0, clip='sitFloor'), k(0.0, look=[-4.1, 2.0, 0.2]), TK(0.0, face={'lid': 0.45, 'mouth': 'line', 'brow': 0.2}, d=0.0), *blink(r(CUT8 + 0.8), {'lid': 0.45, 'mouth': 'line', 'brow': 0.2}), *BREATHE(r(CUT8 + 0.1), D8, 0.5)]
st.shot('S08', 'grassland', setOpts={'grass': '#9CC860'}, look={'sunDir': [0.6, 0.6, 0.6]},
        actors=[*adults8, act('dame', LADY8, -30, 'stand', 'neutral', keys=klady), act('ministre', MIN8, MRY8, 'sitFloor', 'neutral', keys=kmin8)],
        props=[P('portail8', 'buGate', pos=[0, 0, 0], ry=-30, keys=[k(CUT8, visible=False)]), *[P(f'cartable8_{i}', 'buBackpack', on={'actor': f'adulte{i + 1}', 'joint': 'torso', 'offset': [0, 0.45, -0.2]}, opts={'color': ['#E8C030', '#E86AA0', '#5EAA4A', '#3E8ACC'][i]}, keys=[k(CUT8, visible=False)]) for i in range(4)],
               P('gouter8', 'buLunchbox', on={'actor': 'adulte2', 'hand': 'R', 'offset': [0, 0.0, 0.0]}, keys=[k(CUT8, visible=False)]), P('disque8', 'buDisc', on={'actor': 'dame', 'hand': 'R', 'offset': [0, 0, 0]}, keys=[k(CUT8, visible=False)]),
               P('classe8', 'buClass', pos=[0, 0, 2.5], keys=[k(0.0, visible=False), k(CUT8, visible=True)]), TINY('chaise8', add(MIN8, [0, -0.33, 0]), MRY8, '#2F62B5'), P('pupitre8', 'buTinyDesk', pos=add(MIN8, [0.35, -0.33, -0.1]), ry=MRY8),
               P('cheveux8', 'buHair', on={'actor': 'ministre', 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'color': '#B8B8B8'})], cams=[C8, C8b])
st.card('S08', 'RENTRÉE', at=st.at('S08', 'L08', 4))

# ================================================================= S09
# 9: child scale, shot one of two. An open-plan office: three small kids in oversized suits, sleeves dangling past their hands, sit on stacks of thick
#    binders at the big desks; one answers a phone bigger than his head, very serious, and nods
D9 = st.dur('S09'); PHONE9 = 0.6; NOD9 = [1.2, 1.7, 2.2]
KID9 = [[-1.3, 0.34, 0.25], [0.0, 0.34, 0.25], [1.3, 0.34, 0.25]]
C9 = fcam(0.0, [0.2, 1.2, 3.6], {'k0': add(KID9[0], [-0.3, 1.2, 0]), 'k2': add(KID9[2], [0.4, 1.2, 0]), 'desk': [0, 0.74, -0.35], 'deskB': [0, 0, 0.5]}, top=0.16, bottom=0.76, push=0.2)
kids9 = []
for i, p in enumerate(KID9):
    nm = f'enfant{i + 1}'; ks = [k(0.0, clip='sit'), k(0.0, look=[p[0], 1.0, -0.6]), TK(0.0, face={'lid': 0.3, 'mouth': 'line', 'brow': -0.3}, d=0.0), *blink(r(0.7 + 0.5 * i), {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}), *BREATHE(0.1, D9, 0.5)]
    if i == 1: ks += [TK(PHONE9, {'R': R5(add(p, [0.12, 0.6, 0.05]))}, {'R': 'grip'}, d=0.2, keep=True), k(PHONE9, look='camera', lookDur=0.2), *[x for t_ in NOD9 for x in (TK(t_, bend={'neck': SP(0.35)}, d=0.1, keep=True), TK(r(t_ + 0.18), bend={'neck': SP(0.0)}, d=0.12, keep=True))]]
    kids9.append(act(nm, p, 0, 'sit', 'neutral', keys=ks, scale=0.6))
st.shot('S09', 'whiteVoid', setOpts={'color': '#D8DEE4'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=kids9,
        props=[P('plateau9', 'buOffice', pos=[0, 0, -0.9], opts={'desk': False}), *[P(f'poste9_{i}', 'buDesk', pos=[p[0], 0, -0.25]) for i, p in enumerate(KID9)], *[P(f'classeurs9_{i}', 'buBinders', pos=[p[0], 0, p[2]], opts={'n': 4}) for i, p in enumerate(KID9)],
               *[P(f'veste9_{i}', 'buBigJacket', on={'actor': f'enfant{i + 1}', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'color': ['#3A4A6A', '#5A5A5A', '#4A3A2A'][i]}) for i in range(3)],
               P('telephone9', 'bigPhone', on={'actor': 'enfant2', 'hand': 'R', 'offset': [0, 0.0, 0.02]}, opts={'w': 0.12}, keys=[k(0.0, visible=False), k(PHONE9, visible=True)])], cams=[C9])

# ================================================================= S10
# 10: child scale, shot two of two. The boardroom: five kids round the long table; the wall clock (hands only) clicks to half past four, juice boxes and
#     pains au chocolat slide down the table, and all five dash out at once, leaving their office chairs spinning
D10 = st.dur('S10'); CLICK10 = r(st.at('S10', 'L10', 6)); SNACK10 = r(st.at('S10', 'L10', 7)); DASH10 = r(SNACK10 + 0.55)
SEATS10 = [[-1.2, 0, -0.75], [0.0, 0, -0.75], [1.2, 0, -0.75], [-0.6, 0, 0.75], [0.6, 0, 0.75]]
C10 = fcam(0.0, [2.4, 1.6, 3.4], {'t0': [-1.8, 0.74, -0.6], 't1': [1.8, 0.74, 0.6], 'clock': [0.0, 2.3, -1.9], 'k3': [-0.6, 1.3, 0.85]}, top=0.12, bottom=0.76, push=0.2)
kids10 = []
for i, p in enumerate(SEATS10):
    ry = 0 if p[2] < 0 else 180; nm = f'enfant{i + 1}'; out = [-4.0, 0, r(p[2] * 1.5)]
    kids10.append(act(nm, add(p, [0, 0.12, 0]), ry, 'sit', 'neutral', scale=0.6, keys=[k(0.0, clip='sit'), k(0.0, look=[0, 0.8, 0]), TK(0.0, face={'lid': 0.3, 'mouth': 'line', 'brow': -0.2}, d=0.0), k(CLICK10, look=[0.0, 2.3, -1.9], lookDur=0.1),
        TK(r(CLICK10 + 0.1), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, d=0.06, keep=True), k(r(DASH10 + 0.03 * i), clip='run', blend=0.04), k(r(DASH10 + 0.03 * i), to=out, dur=0.45, clip='run', ease='in', face='keep'), k(r(DASH10 + 0.03 * i), face=-90, turn=0.08)]))
st.shot('S10', 'whiteVoid', setOpts={'color': '#D8D2C8'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=kids10,
        props=[P('salle10', 'buOffice', pos=[0, 0, 0.9], opts={'desk': False}), P('table10', 'buTable', pos=[0, 0, 0], opts={'len': 3.6}), P('horloge10', 'buClock', pos=[0.0, 2.3, -1.85], opts={'time': [[0.0, 4.48], [CLICK10, 4.5]]}),
               *[P(f'fauteuil10_{i}', 'officeChair', pos=p, ry=0 if p[2] < 0 else 180, keys=[k(r(DASH10 + 0.1), rotTo=[0, 12.0, 0], dur=2.0, ease='out')]) for i, p in enumerate(SEATS10)],
               *[P(f'veste10_{i}', 'buBigJacket', on={'actor': f'enfant{i + 1}', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'color': ['#3A4A6A', '#5A5A5A', '#4A3A2A', '#2E4A5A', '#5A4A6A'][i]}) for i in range(5)],
               *[P(f'jus10_{i}', 'buJuice', pos=[-1.8, 0.77, r(-0.25 + 0.5 * (i % 2))], opts={'color': ['#F2A030', '#5EAA4A', '#E86AA0'][i % 3]}, keys=[k(SNACK10, to=[r(-1.2 + 0.6 * i), 0.77, r(-0.25 + 0.5 * (i % 2))], dur=0.35, ease='out')]) for i in range(5)],
               *[P(f'pain10_{i}', 'buPain', pos=[1.8, 0.77, r(0.25 - 0.5 * (i % 2))], keys=[k(SNACK10, to=[r(1.2 - 0.6 * i), 0.77, r(0.25 - 0.5 * (i % 2))], dur=0.35, ease='out')]) for i in range(5)]], cams=[C10])
st.cue('clack', 'S10', CLICK10, 0.4); st.cue('whoosh', 'S10', SNACK10, 0.25); st.cue('whoosh', 'S10', DASH10, 0.4)

# ================================================================= S11
# 11: the same boardroom, empty: on the wall a big crayon drawing of an arrow that shoots up toward a smiling yellow sun, carries on over the top of the
#     wall and across the ceiling; slow push-in; the files in perfect square piles and one crumb of pain au chocolat
D11 = st.dur('S11')
C11 = cam(0.0, [0.0, 1.3, 3.6], [0.0, 1.55, 2.4], [0.0, 1.9, -1.9], [0.0, 2.3, -1.9], lens=52, ease='inOut')
st.shot('S11', 'whiteVoid', setOpts={'color': '#D8D2C8'}, look={'sunDir': [0.3, 0.9, 0.6]}, actors=[],
        props=[P('salle11', 'buOffice', pos=[0, 0, 0.9], opts={'desk': False}), P('table11', 'buTable', pos=[0, 0, 0], opts={'len': 3.6}), P('dessin11', 'buArrow', pos=[0.2, 0, -1.83], opts={'h': 3.0, 'w': 3.0, 'd': 2.4}), P('horloge11', 'buClock', pos=[-1.5, 2.3, -1.85], opts={'time': [[0.0, 4.5]]}),
               *[P(f'dossiers11_{i}', 'buFiles', pos=[r(-1.2 + 0.8 * i), 0.77, 0.0]) for i in range(4)], P('miette11', 'buCrumb', pos=[0.35, 0.77, 0.3]), *[P(f'fauteuil11_{i}', 'officeChair', pos=p, ry=0 if p[2] < 0 else 180) for i, p in enumerate(SEATS10)]], cams=[C11])

# ================================================================= S12
# 12: the classroom: the minister walks up and hands in a perfectly blank sheet; the teacher, eyes on her knitting, the scarf now coiled in heaps round
#     her chair, stamps it, thunk. The minister holds the sheet up to the lens: blank but for the same crooked red stamp. He narrows his eyes at her
D12 = st.dur('S12'); GIVE12 = 0.9; THUNK12 = r(st.at('S12', 'L12', 6) - 0.1); SHOW12 = r(THUNK12 + 0.6)
MA12, MB12 = [1.6, 0, 0.2], [-0.55, 0, -1.6]; MRY12 = yaw(MB12, TCH)
SHEET12 = add(TD, [0.3, 0.79, 0.15])
C12 = fcam(0.0, [0.9, 1.45, 0.9], {'min': add(MB12, [0, 2.35, 0]), 'tch': add(TCH, [0, 1.9, 0]), 'heap': add(TCH, [0.7, 0, 0.6]), 'heapL': add(TCH, [-0.7, 0, 0.5]), 'minA': add(MA12, [0, 2.3, 0])}, top=0.12, bottom=0.76, push=0.2)
km12 = [k(0.0, clip='walk'), k(0.0, to=MB12, dur=r(GIVE12 - 0.15), clip='walk', face='keep'), k(r(GIVE12 - 0.15), clip='stand', blend=0.1), k(r(GIVE12 - 0.15), face=MRY12, turn=0.15), k(0.0, look=HEAD(TCH, 1.4)),
        TK(0.0, {'R': R5(off(MA12, -120, 0.3, 0.22, 1.05))}, {'R': 'pinch'}, GRAVE, d=0.0), TK(GIVE12, {'R': R5(add(SHEET12, [0, 0.06, 0]))}, d=0.2, keep=True), TK(r(GIVE12 + 0.35), {'R': R5(off(MB12, MRY12, 0.3, 0.22, 1.0))}, {'R': 'rest'}, d=0.2, keep=True),
        TK(r(SHOW12 - 0.1), {'R': R5(off(MB12, 70, 0.4, 0.1, 1.7))}, {'R': 'pinch'}, d=0.2, keep=True), k(r(SHOW12 - 0.15), face=70, turn=0.15), k(SHOW12, look='camera', lookDur=0.15),   # to the lens
        TK(r(SHOW12 + 0.6), face={'lid': 0.65, 'mouth': 'line', 'brow': -0.9}, d=0.1, keep=True), k(r(SHOW12 + 0.6), face=MRY12, turn=0.2), k(r(SHOW12 + 0.6), look=HEAD(TCH, 1.4), lookDur=0.2), *blink(r(D12 - 0.3), GRAVE)]   # he narrows his eyes at her
kt12 = [TK(r(THUNK12 - 0.2), {'R': R5(add(SHEET12, [0.0, 0.35, 0]))}, {'R': 'grip'}, d=0.12, keep=True), TK(THUNK12, {'R': R5(add(SHEET12, [0.0, 0.1, 0]))}, sq=(1.04, 0.96, 1.04), d=0.05, e='in', keep=True), TK(r(THUNK12 + 0.25), {'R': R5(add(TCH, [0.08, 0.66, 0.32]))}, {'R': 'pinch'}, sq=(1, 1, 1), d=0.2, keep=True)]
HEAPS12 = [[add(TCH, [0.05, 0.57, 0.32]), add(TCH, [0.2, 0.3, 0.5]), add(TCH, [0.5, 0.02, 0.5]), add(TCH, [0.6, 0.02, -0.2]), add(TCH, [-0.1, 0.02, -0.55]), add(TCH, [-0.7, 0.02, -0.1]), add(TCH, [-0.6, 0.02, 0.5]), add(TCH, [0.2, 0.02, 0.75]), add(TCH, [0.75, 0.02, 0.3])]]
st.shot('S12', 'whiteVoid', setOpts=CLASS, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[KNITTER('maitresse', TCH, TRY, keys_extra=kt12), act('ministre', MA12, -120, 'walk', 'neutral', keys=km12)],
        props=[P('classe12', 'buClass', pos=[0, 0, 0]), P('bureau12', 'buTable', pos=TD, opts={'len': 1.4}), P('chaiseM12', 'buTinyChair', pos=TCH, opts={'color': '#7A5C3A'}, scale=1.4), KNIT('tricot12'), *LOOKS('maitresse'), SCARF('echarpe12', HEAPS12[0]),
               P('tampon12', 'buStamp', on={'actor': 'maitresse', 'hand': 'R', 'offset': [0, 0.28, 0.02]}, keys=[k(0.0, visible=False), k(r(THUNK12 - 0.25), visible=True), k(r(THUNK12 + 0.3), visible=False)]),
               P('copie12', 'buReport', on={'actor': 'ministre', 'hand': 'R', 'offset': [0.0, 0.14, 0.05]}, opts={'state': 'blank', 'stamp': False, 'w': 0.34}, keys=[k(r(GIVE12 + 0.05), detach=True), k(r(GIVE12 + 0.05), to=SHEET12, dur=0.01), k(r(GIVE12 + 0.05), rotTo=[-1.5708, 0, 0], dur=0.01), k(THUNK12, visible=False)]),
               P('copie12b', 'buReport', pos=SHEET12, rot=[-1.5708, 0, 0], opts={'state': 'blank', 'w': 0.34}, keys=[k(0.0, visible=False), k(THUNK12, visible=True), k(r(SHOW12 - 0.12), attach='ministre', hand='R', offset=[0.0, 0.14, 0.05], rot=[0, 0, 0])]),
               P('cheveux12', 'buHair', on={'actor': 'ministre', 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'color': '#B8B8B8'})], cams=[C12])
st.cue('thud', 'S12', THUNK12, 0.5)

# ================================================================= S13
# 13: the empty classroom at break: the minister pulls the teacher's desk drawer and it slides out and out, metres long, crammed with untouched papers,
#     each with the same stamp; on top a thick bundle of memos held by a big plain red wax seal. He lifts the bundle up to the camera
D13 = st.dur('S13'); PULL13 = 0.5; LIFT13 = r(st.at('S13', 'L13', 9))
MN13 = [-1.5, 0, -0.55]; DRW13 = add(TD, [0, 0.55, 0.42])
C13 = fcam(0.0, [1.9, 1.5, 2.0], {'min': add(MN13, [0, 2.35, 0]), 'drawer': add(DRW13, [0, 0, 2.2]), 'drawerB': add(DRW13, [0.3, -0.5, 0.1]), 'desk': add(TD, [-0.7, 0.8, 0])}, top=0.12, bottom=0.76, push=0.2)
km13 = [k(0.0, clip='stand'), k(0.0, look=DRW13), TK(0.0, {'R': R5(add(DRW13, [0.05, 0.05, 0.12]))}, {'R': 'grip'}, CALM, bend={'spine': SP(0.3)}, d=0.0),
        k(PULL13, to=add(MN13, [0, 0, 1.4]), dur=1.0, ease='out', face='keep'), TK(PULL13, {'R': R5(add(DRW13, [0.05, 0.05, 1.5]))}, bend={'spine': SP(0.2)}, d=1.0, keep=True), k(r(PULL13 + 0.5), look=add(DRW13, [0, 0, 0.6]), lookDur=0.3),   # out and out
        TK(r(PULL13 + 1.2), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, d=0.08, keep=True), TK(LIFT13, {'R': R5(add(MN13, [0.15, 1.5, 1.85])), 'L': R5(add(MN13, [-0.15, 1.5, 1.85]))}, {'R': 'pinch', 'L': 'pinch'}, bend={'spine': SP(0.0)}, face=GRAVE, d=0.3, keep=True), k(LIFT13, look='camera', lookDur=0.2), *blink(r(D13 - 0.4), GRAVE)]
st.shot('S13', 'whiteVoid', setOpts=CLASS, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[act('ministre', MN13, 180, 'stand', 'neutral', keys=km13)],
        props=[P('classe13', 'buClass', pos=[0, 0, 0]), P('bureau13', 'buTable', pos=TD, opts={'len': 1.4}), P('tiroir13', 'buDrawer', pos=DRW13, opts={'out': [[0.0, 0.0], [PULL13, 0.05], [r(PULL13 + 1.0), 2.4]], 'n': 26}),
               P('liasse13', 'buMemos', pos=add(DRW13, [0, 0.13, 2.35]), rot=[-1.5708, 0, 0], keys=[k(0.0, visible=False), k(r(PULL13 + 1.0), visible=True), k(r(LIFT13 - 0.1), attach='ministre', hand='R', offset=[-0.15, 0.14, 0.05], rot=[0, 0, 0])]),
               P('cheveux13', 'buHair', on={'actor': 'ministre', 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'color': '#B8B8B8'})], cams=[C13])
st.cue('whoosh', 'S13', PULL13, 0.4)

# ================================================================= S14
# 14: close: he holds one memo to the lens: the plain wax seal and a signature scribble. He looks at the scribble, then at the fountain pen clipped to his
#     own breast pocket; a sweat drop pops, and he slowly slides down behind his tiny desk until only his eyes show above it
D14 = st.dur('S14'); PEN14 = r(st.at('S14', 'L14', 3)); SLIDE14 = r(PEN14 + 0.6)
MS14 = [0.0, 0.33, 0.0]
C14 = cam(0.0, [0.0, 1.5, 2.7], [0.0, 1.45, 2.6], [0.0, 1.5, 0.0], [0.0, 1.1, 0.0], lens=48)
km14 = [k(0.0, clip='sitFloor'), k(0.0, look='camera'), TK(0.0, {'R': R5([0.12, 1.3, 0.45]), 'L': R5([-0.12, 1.3, 0.45])}, {'R': 'pinch', 'L': 'pinch'}, GRAVE, d=0.0), k(0.7, look=[0.1, 1.3, 0.45], lookDur=0.2),
        k(PEN14, look=[0.08, 1.15, 0.2], lookDur=0.25), TK(r(PEN14 + 0.1), face={'lid': 0.0, 'mouth': 'wavy', 'brow': 0.9}, d=0.06, keep=True), TK(r(PEN14 + 0.3), {'R': R5([0.15, 0.8, 0.35]), 'L': R5([-0.15, 0.8, 0.35])}, d=0.3, keep=True),
        k(SLIDE14, to=add(MS14, [0, -0.62, 0.05]), dur=r(D14 - SLIDE14 - 0.2), clip='sitFloor', ease='inOut'), k(r(SLIDE14 + 0.3), look='camera', lookDur=0.3), *blink(r(D14 - 0.2), {'lid': 0.0, 'mouth': 'wavy', 'brow': 0.9})]   # down behind the desk, only his eyes over it
st.shot('S14', 'whiteVoid', setOpts=CLASS, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[act('ministre', MS14, 0, 'sitFloor', 'neutral', keys=km14)],
        props=[P('classe14', 'buClass', pos=[0, 0, 2.5]), TINY('chaise14', [0, 0, 0], 0), P('pupitre14', 'buTinyDesk', pos=[0, 0, 0.42], ry=0),
               P('memo14', 'buMemos', on={'actor': 'ministre', 'hand': 'R', 'offset': [-0.12, 0.16, 0.05], 'face': 'camera'}, opts={'w': 0.34}, keys=[k(r(PEN14 + 0.3), detach=True), k(r(PEN14 + 0.3), to=[0.0, 0.57, 0.42], dur=0.25, ease='in'), k(r(PEN14 + 0.3), rotTo=[-1.5708, 0, 0], dur=0.25)]),
               P('stylo14', 'buPen', on={'actor': 'ministre', 'joint': 'torso', 'offset': [0.1, 0.55, 0.16]}), DROP('goutte14', 'ministre', r(PEN14 + 0.15), offset=(0.25, 0.3, 0.05)),
               P('cheveux14', 'buHair', on={'actor': 'ministre', 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'color': '#B8B8B8'})], cams=[C14])
st.cue('pop', 'S14', r(PEN14 + 0.15), 0.25)

# ================================================================= S15
# 15: the classroom: the teacher puts her knitting down for the first time (the scarf runs off her lap, across the floor and out of the door), settles
#     big thick glasses on her nose, picks up the hero's gold-star sheet and reads it slowly, head moving left to right; the hero at his tiny desk leans
#     forward, hopeful, eyes huge
D15 = st.dur('S15'); DOWN15 = 0.3; GLASS15 = 0.9; READ15 = 1.4
C15 = fcam(0.0, [1.3, 1.35, 0.1], {'tch': add(TCH, [0, 1.95, 0]), 'tchF': add(TCH, [0, 0, 0.5]), 'hero': add(HC, [0, 1.6, 0]), 'heroF': HC}, top=0.12, bottom=0.76, push=0.2)
SH15 = add(TCH, [0.0, 1.35, 0.45])
kt15 = [k(0.0, clip='sit'), k(0.0, look=KNITLOOK), TK(0.0, {'R': R5(add(TCH, [0.08, 0.66, 0.32])), 'L': R5(add(TCH, [-0.08, 0.66, 0.32]))}, {'R': 'pinch', 'L': 'pinch'}, DOWN, bend={'neck': SP(0.35)}, d=0.0),
        TK(DOWN15, {'R': R5(add(TD, [0.3, 0.82, 0.1])), 'L': R5(add(TD, [0.1, 0.82, 0.1]))}, d=0.25, keep=True),   # the knitting down, for the first time
        TK(GLASS15, {'R': R5(add(TCH, [0.08, 1.75, 0.2])), 'L': R5(add(TCH, [-0.08, 1.75, 0.2]))}, {'R': 'pinch', 'L': 'pinch'}, bend={'neck': SP(0.0)}, face={'lid': 0.3, 'mouth': 'line', 'brow': 0.3, 'gy': 0.0}, d=0.25, keep=True),   # the big glasses on
        TK(READ15, {'R': R5(add(SH15, [0.15, 0, 0])), 'L': R5(add(SH15, [-0.15, 0, 0]))}, d=0.25, keep=True), *[k(r(READ15 + 0.3 + 0.35 * j), look=add(SH15, [0.12 if j % 2 else -0.12, -0.05 * j, 0]), lookDur=0.3) for j in range(5)]]   # reading, left to right
kh15 = [k(0.0, clip='sitFloor'), k(0.0, look=HEAD(TCH, 1.4)), TK(0.0, face={'lid': 0.2, 'mouth': 'line', 'brow': 0.6}, d=0.0), TK(READ15, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 0.6}, sq=(0.96, 1.05, 0.96), bend={'spine': SP(0.3)}, d=0.2, keep=True), *BREATHE(0.2, D15, 0.45), *blink(0.8, CALM)]
st.shot('S15', 'whiteVoid', setOpts=CLASS, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[act('maitresse', TCH, TRY, 'sit', 'neutral', keys=kt15), act('mec', add(HC, [0, 0.33, 0]), HRY, 'sitFloor', 'neutral', keys=kh15)],
        props=[P('classe15', 'buClass', pos=[0, 0, 0]), *ROWS('r15', skip=((1, 1),)), TINY('chaise15', HC, HRY), P('pupitre15', 'buTinyDesk', pos=add(HC, [-0.1, 0, -0.45]), ry=HRY),
               P('bureau15', 'buTable', pos=TD, opts={'len': 1.4}), P('chaiseM15', 'buTinyChair', pos=TCH, opts={'color': '#7A5C3A'}, scale=1.4), *LOOKS('maitresse'),
               P('tricot15', 'buKnit', on={'actor': 'maitresse', 'hand': 'R', 'offset': [-0.08, 0.0, 0.04]}, keys=[k(r(DOWN15 + 0.25), detach=True), k(r(DOWN15 + 0.25), to=add(TD, [0.25, 0.8, 0.1]), dur=0.01)]),
               SCARF('echarpe15', [add(TD, [0.25, 0.8, 0.1]), add(TD, [-0.3, 0.02, 0.5]), add(TCH, [-1.2, 0.02, 1.2]), [-4.2, 0.02, 1.4]]),
               P('lunettes15', 'bigGlasses', on={'actor': 'maitresse', 'joint': 'head', 'offset': [0, 0.08, 0.18]}, keys=[k(0.0, visible=False), k(GLASS15, visible=True)]),
               P('copie15', 'buReport', pos=add(TD, [-0.3, 0.79, 0.15]), rot=[-1.5708, 0, 0], opts={'state': 'stars', 'w': 0.34}, keys=[k(r(READ15 - 0.1), attach='maitresse', hand='R', offset=[-0.15, 0.14, 0.05], rot=[0, 0, 0])])], cams=[C15])

# ================================================================= S16
# 16: close on the gold-star sheet: she writes by hand under the stars, in big round blue letters on two lines, « Peut mieux / faire. », held more than a
#     second. Cut: he squashes down into his tiny chair like a deflating balloon until only his red tie shows above the desk. Hold
D16 = st.dur('S16'); WR16 = [0.05, 0.7]; CUT16 = r(max(WR16[1] + 1.05, D16 - 0.5))
C16 = cam(0.0, [0.0, 1.0, 1.7], [0.0, 1.0, 1.62], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], lens=22)   # the sheet fills the frame
HD16 = [0.0, 0.33, 0.0]
C16b = cam(CUT16, [0.0, 0.85, 2.4], [0.0, 0.83, 2.3], [0.0, 0.8, 0.0], [0.0, 0.7, 0.0], lens=44)
kh16 = [k(0.0, visible=False), k(CUT16, visible=True), k(0.0, clip='sitFloor'), k(0.0, look='camera'), TK(0.0, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, d=0.0),
        TK(CUT16, face={'lid': 0.4, 'mouth': 'line', 'brow': 0.6}, sq=(1, 1, 1), d=0.0, keep=True), TK(r(CUT16 + 0.05), sq=(1.25, 0.6, 1.25), face={'lid': 0.6, 'mouth': 'wavy', 'brow': 0.8}, d=0.25, e='in', keep=True), k(r(CUT16 + 0.05), to=add(HD16, [0, -0.12, 0]), dur=0.25, clip='sitFloor', ease='in')]   # he goes down like a balloon
st.shot('S16', 'whiteVoid', setOpts=CLASS, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[act('mec', HD16, 0, 'sitFloor', 'neutral', keys=kh16)],
        props=[P('copie16', 'buReport', pos=[0.0, 1.0, 0.0], opts={'state': 'stars', 'w': 0.42, 'write': WR16}, keys=[k(CUT16, visible=False)]),
               P('stylo16', 'buPen', pos=[-0.12, 1.08, 0.05], rot=[0, 0, -0.6], opts={'cap': False}, keys=[*[k(r(WR16[0] + (WR16[1] - WR16[0]) * j / 6), to=[r(-0.15 + 0.06 * (j % 3)), r(1.08 - 0.07 * (j // 3)), 0.05], dur=r((WR16[1] - WR16[0]) / 6)) for j in range(6)], k(r(WR16[1] + 0.05), to=[0.25, 1.25, 0.1], dur=0.2), k(CUT16, visible=False)]),
               P('classe16', 'buClass', pos=[0, 0, 2.6], keys=[k(0.0, visible=False), k(CUT16, visible=True)]), TINY('chaise16', [0, 0, 0], 0), P('pupitre16', 'buTinyDesk', pos=[0, 0, 0.42], ry=0, keys=[k(0.0, visible=False), k(CUT16, visible=True)])], cams=[C16, C16b])
st.cue('clack', 'S16', r(CUT16 + 0.05), 0.2)

for g_ in [('S01', CUT1, 'mec', 'report'), ('S02', 1.6, 'mec', 'school'), ('S03', SLAP3, 'mec', 'stars'), ('S04', THUNK4, 'maitresse', 'stamp'), ('S05', POINT5, 'patron', 'fired'), ('S06', GULP6, 'patron', 'gulp'),
           ('S07', OWN7, 'chef', 'same'), ('S08', CUT8, 'ministre', 'back'), ('S09', PHONE9, 'enfant2', 'phone'), ('S10', DASH10, 'enfant1', 'dash'), ('S11', 0.5, None, 'arrow'),
           ('S12', THUNK12, 'maitresse', 'stamp'), ('S13', PULL13, 'ministre', 'drawer'), ('S14', SLIDE14, 'ministre', 'slide'), ('S15', READ15, 'maitresse', 'reads'), ('S16', CUT16, 'mec', 'deflate')]:
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
GUEST = lambda pr, seed, suit, **kw: {'preset': pr, 'seed': seed, 'hat': 'none', 'suit': suit, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX, 'tie': '#3A3D44', **kw}
st.write("Le bulletin", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'maitresse': GUEST('madame', 6301, '#D8A830', pants='#8A6A3A', shirt='#F4E8C8'),
    'patron': GUEST('politique', 6302, '#6A6E74', shirt='#F4F1EA', pants='#5A5E64'), 'chef': GUEST('worker', 6303, '#5E8C4A', glasses=True),
    'employe1': GUEST('madame', 6304, '#8A5AB0'), 'employe2': GUEST('tourist', 6305, '#3E8ACC'), 'employe3': GUEST('sportif', 6306, '#E8913A'),
    'ministre': GUEST('politique', 6307, '#22252C', pants='#22252C', glasses=True),
    'adulte1': GUEST('worker', 6308, '#E8913A'), 'adulte2': GUEST('madame', 6309, '#5EAA4A'), 'adulte3': GUEST('tourist', 6310, '#3E8ACC'), 'adulte4': GUEST('fermier', 6311, '#8A6A45'),
    'dame': GUEST('madame', 6312, '#F2D030', pants='#2E5E9E'),
    **{f'enfant{i + 1}': GUEST(['tourist', 'sportif', 'madame', 'worker', 'fermier'][i], 6320 + i, '#3A4A6A', build={'width': 1.0, 'headWidth': 1.3, 'headScale': 1.25}) for i in range(5)},
})
