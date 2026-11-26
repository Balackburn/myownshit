#!/usr/bin/env python3
"""Le spaghetti (story 112; a spaghetti flicked at the kitchen tiles becomes a masterpiece, and slides down all the while).
To see if his pasta is cooked this man flicks one spaghetti at the wall. It sticks; the neighbour cries masterpiece. That evening three critics are in
his kitchen; a museum buys the wall, he keeps the pot. The critics see the loneliness of modern man; every artist goes pasta, the art schools trade
brushes for colanders, ravioli reinvent cubism; a packet of noodles is worth a flat, the country eats rice; the insurer appraises the work, well, its
frame. One night it falls: tasted, it was not cooked; the other works fall too; the critics see the fall of modern man. The museum gives it back; he
puts it back in the pot, still boiling: two more minutes.
Running gag (silent): ONE fat deep-yellow strand slides down the 20 cm blue tiles a little lower in every shot, measured against the dark grout (the
position table in NOTES.md): on the reference grout line (S02a), a quarter tile lower (S02b), half (S03), one (S04), one and a half (S05), halfway
down in a drooping S with an opaque drop (S10), on the floor (S11). Nobody ever looks at it (gazes locked away on every key).
Cards: CHEF-D'ŒUVRE (S02), SCANDALE (S13). No other word, no figure, no brand, no price, no logo; no flag; at most five people in a shot."""
from story_kit import *
import math

st = Story('spaghetti', look='natural')
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

# ---------------------------------------------------------------- the running gag: one fat strand slides down the tiles
TILE = 0.2
KB = -1.6; KP = [0.2, 0.95, -1.55]   # the kitchen: back wall, the tile panel's pivot (12 x 8 tiles of 20 cm, its bottom on the counter)
MP = [0.0, 0.55, -1.44]   # the museum: the panel in its gilt frame
REF = 6   # the reference grout line: 6 rows up from the panel's bottom (kitchen y 2.15, museum y 1.75)
DROP = {'S02a': 0.0, 'S02b': 0.25, 'S03': 0.5, 'S04': 1.0, 'S05': 1.5, 'S10': 2.0}   # in tiles below the reference line (the position table, NOTES.md)
def STRAND(sid, D, shape='curve', fall=None, x=0.55):
    d = DROP[sid] * TILE
    o = {'x': x, 'ref': REF, 'drop': [[0.0, r(d)], [r(D), r(d + 0.012)]], 'shape': shape}
    if fall: o['fall'] = fall
    return o
def TILES(pid, pos, strand=None, keys=None):
    return P(pid, 'sgTiles', pos=pos, opts={'strand': strand} if strand else {}, **({'keys': keys} if keys else {}))
def CUTAT(t): return _dn(t)
def LOCKGAZE(a, gx=None, gy=None, lid=None):
    """the eyes keep where they are told on every toon key: gx/gy forced; exprW 0.4 makes the face 'strong' (no idle darts, no own blink: the blinks
    are keyed). Nobody ever looks at the strand"""
    for kk in a['keys']:
        tn = kk.get('toon')
        if tn is None: continue
        f = dict(tn.get('face') or {}); f.update({'expr': 'neutral', 'exprW': 0.4})
        if gx is not None: f['gx'] = gx
        if gy is not None: f['gy'] = gy
        if lid is not None and f.get('lid', 0) < 0.99: f['lid'] = max(lid, f.get('lid', 0))
        tn['face'] = f
    return a
def CHIN(side='R'): return {side: ['face', 0.0, -0.42, 0.06, 1, 0.02]}   # a hand under the chin
def TILT(a): return {'neck': [0, a, 0, 1, None]}
SPECS = lambda id_: P(f'{id_}_lunettes', 'sgSpecs', on={'actor': id_, 'joint': 'head', 'offset': [0, 0.28, 0.13]})
def STEAM(pid, pos, drift=(0.25, 0.1)): return P(pid, 'softWisp', pos=pos, opts={'color': '#F4F4F2', 'opacity': 0.85, 'n': 10, 'rise': 0.7, 'life': 1.4, 's0': 0.05, 's1': 0.16, 'drift': list(drift)})
POT = [-0.3, 0.97, -1.24]; TIMER = [0.35, 0.95, -1.32]; HOB = [0.3, 0, -0.62]
CRIT = ['critique1', 'critique2', 'critique3']

# ================================================================= S01
# 1: two cuts. The kitchen: he stands at the hob over a big pot of boiling water, steam puffs rising away from his head, the red egg timer beside it;
#    he fishes out one fat spaghetti on a fork. Cut: he flicks it at the tiles like a darts player, tongue out
D1 = st.dur('S01'); C1 = CUTAT(st.at('S01', 'L01', 8) - 0.1); FLICK1 = r(D1 - 0.35)
CA1 = cam(0.0, [-0.55, 1.55, 1.75], [-0.5, 1.53, 1.6], [0.0, 1.25, -0.9], [0.0, 1.27, -0.9], lens=48)
CB1 = cam(C1, [2.9, 1.7, -0.25], [2.82, 1.7, -0.3], [0.45, 1.7, -1.05], [0.45, 1.7, -1.05], lens=46)
kh1 = [k(0.0, clip='stand'), k(0.0, look=add(POT, [0, 0.1, 0])), TK(0.0, {'R': R5(add(POT, [0.02, 0.3, 0.05]))}, {'R': 'grip'}, CALM, bend={'spine': SP(0.15)}, d=0.0),
       TK(0.6, {'R': R5(add(POT, [0.02, 0.12, 0.05]))}, d=0.25, keep=True), TK(1.2, {'R': R5(add(POT, [0.2, 0.55, 0.35]))}, face={'lid': 0.15, 'mouth': 'line', 'brow': 0.4}, d=0.3, keep=True), k(1.2, look=add(POT, [0.2, 0.55, 0.35]), lookDur=0.3), *blink(0.9, CALM),
       k(C1, look=[0.2, 2.1, -1.55], lookDur=0.1), TK(C1, {'R': R5([0.45, 1.75, -0.6])}, face={'lid': 0.5, 'mouth': 'tongueout', 'brow': -0.4}, bend={'spine': SP(-0.05)}, d=0.05, keep=True),   # the darts player's cocked wrist
       TK(r(FLICK1 - 0.2), {'R': R5([0.42, 1.82, -0.48])}, d=0.15, keep=True), TK(FLICK1, {'R': R5([0.35, 1.8, -1.05])}, bend={'spine': SP(0.12)}, d=0.06, e='out', keep=True), TK(r(FLICK1 + 0.15), face={'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}, d=0.08, keep=True)]
st.shot('S01', 'whiteVoid', setOpts={'color': '#F1E6CC'}, look={'sunDir': [0.4, 0.9, 0.5]},
        actors=[act('mec', HOB, -120, 'stand', 'neutral', keys=kh1 + [k(r(C1 - 0.02), face=-170, turn=0.02)])],
        props=[P('cuisine1', 'sgKitchen', pos=[0, 0, 0]), TILES('carreaux1', KP), P('casserole1', 'sgPot', pos=POT), P('minuteur1', 'sgTimer', pos=TIMER, ry=-20), STEAM('vapeur1', add(POT, [0, 0.3, 0]), (0.35, 0.05)),
               P('fourchette1', 'sgForkStrand', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.0, 0.0]}, opts={'hide': FLICK1})], cams=[CA1, CB1])
st.cue('whoosh', 'S01', FLICK1, 0.2)

# ================================================================= S02
# 2: two cuts. Close on the wall: splat, the strand sticks in one elegant curve, its top exactly on a grout line. Cut: the neighbour (curlers, pink
#    dressing gown) leans in at the window, clutches both cheeks and cries out, then takes a photo with a plain phone; behind her shoulder the strand
#    already sits a quarter of a tile lower. CHEF-D'ŒUVRE
D2 = st.dur('S02'); C2 = CUTAT(st.at('S02', 'L02', 4) - 0.1); SPLAT2 = 0.08; SHOT2 = r(C2 + 0.95)
CA2 = cam(0.0, [0.77, 2.0, 1.05], [0.77, 2.0, 0.92], [0.77, 2.0, -1.55], [0.77, 2.0, -1.55], lens=46)
NB2 = [-1.7, 0, -1.82]
CB2 = cam(C2, [1.6, 1.7, 1.3], [1.55, 1.7, 1.2], [-0.15, 1.85, -1.6], [-0.15, 1.85, -1.6], lens=60)
kv2 = [k(0.0, visible=False), k(C2, visible=True), k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, bend={'spine': SP(0.35)}, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, d=0.0),
       TK(r(C2 + 0.05), touch={'R': ['face', -0.13, 0.05, 0.0, 1, 0.02], 'L': ['face', 0.13, 0.05, 0.0, 1, 0.02]}, hands={'R': 'spread', 'L': 'spread'}, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'jaw': 0.5}, d=0.12, keep=True),
       *TALK(r(C2 + 0.2), {'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, n=4), TK(r(SHOT2 - 0.25), {'R': R5(off(NB2, 0, 0.45, 0.45, 1.75))}, {'R': 'grip'}, face={'lid': 0.1, 'mouth': 'smile', 'brow': 0.8}, d=0.15, keep=True), *blink(r(D2 - 0.25), HAPPY)]
st.shot('S02', 'whiteVoid', setOpts={'color': '#F1E6CC'}, look={'sunDir': [0.4, 0.9, 0.5]},
        actors=[act('voisine', NB2, 0, 'stand', 'neutral', keys=kv2)],
        props=[P('cuisine2', 'sgKitchen', pos=[0, 0, 0]), TILES('carreaux2', KP, keys=[k(0.0, visible=False)]),
               P('carreaux2a', 'sgTiles', pos=KP, opts={'strand': STRAND('S02a', C2)}, keys=[k(C2, visible=False)]), P('carreaux2b', 'sgTiles', pos=KP, opts={'strand': {**STRAND('S02b', D2), 'drop': [[0.0, 0.05], [r(D2), 0.056]]}}, keys=[k(0.0, visible=False), k(C2, visible=True)]),
               P('casserole2', 'sgPot', pos=POT), P('minuteur2', 'sgTimer', pos=TIMER, ry=-20),
               P('bigoudis2', 'sgCurlers', on={'actor': 'voisine', 'joint': 'head', 'offset': [0, 0.47, -0.02]}), P('tel2', 'sgPhone', on={'actor': 'voisine', 'hand': 'R', 'offset': [0, 0.02, 0.02]}, keys=[k(0.0, visible=False), k(r(SHOT2 - 0.3), visible=True)]),
               P('flash2', 'sgFlash', pos=off(NB2, 0, 0.55, 0.75, 1.85), ry=40, opts={'at': [SHOT2], 'w': 0.3})], cams=[CA2, CB2])
st.cue('pop', 'S02', SPLAT2, 0.45); st.cue('clack', 'S02', SHOT2, 0.3)
st.card('S02', "CHEF-D'ŒUVRE", at=r(st.at('S02', 'L02', 9) - 0.05))

# ================================================================= S03
# 3: the same kitchen at night: three critics in black turtlenecks and tiny round glasses crowd round the wall with glasses of water, chins in hand;
#    the hero peeks round the doorway in his pyjamas. The strand half a tile below the line; nobody looks at it. Four people
D3 = st.dur('S03')
CR3 = [[-0.15, 0, -0.7], [0.55, 0, -0.55], [1.2, 0, -0.75]]; RY3 = [200, 180, 155]
C3 = cam(0.0, [-1.5, 1.85, 3.1], [-1.42, 1.85, 2.98], [0.95, 1.6, -1.1], [0.95, 1.6, -1.1], lens=56)
crit3 = []
for i, (p, ry) in enumerate(zip(CR3, RY3)):
    ks = [k(0.0, clip='stand'), k(0.0, look=add(p, [0.2 * (i - 1), 2.25, -1.0])), TK(0.0, touch=CHIN('R'), reach={'L': R5(off(p, ry, 0.25, -0.12, 1.1))}, hands={'L': 'grip'}, face={'lid': 0.45, 'mouth': 'line', 'brow': -0.5}, d=0.0),
          TK(r(0.9 + 0.3 * i), bend=TILT(0.2 * (1 if i % 2 else -1)), d=0.4, keep=True), *BREATHE(0.1, D3, 0.6, 0.015), *blink(r(0.6 + 0.5 * i), {'lid': 0.45, 'mouth': 'line', 'brow': -0.5}), *blink(r(1.9 + 0.2 * i), {'lid': 0.45, 'mouth': 'line', 'brow': -0.5})]
    crit3.append(LOCKGAZE(act(CRIT[i], p, ry, 'stand', 'neutral', keys=ks), gx=0.0, gy=-0.6))
DOOR3 = [2.45, 0, -1.85]
kh3 = [k(0.0, clip='stand'), k(0.0, look=[0.5, 1.7, -0.6]), TK(0.0, {'L': R5([2.0, 1.4, -1.6])}, {'L': 'grip'}, face={'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, bend={'spine': SP(0.0, -0.3)}, d=0.0), *blink(1.3, {'lid': 0.0, 'mouth': 'O', 'brow': 0.8}), TK(1.6, face={'lid': 0.0, 'mouth': 'O', 'brow': 0.9, 'gx': -0.5}, d=0.1, keep=True)]
st.shot('S03', 'whiteVoid', setOpts={'color': '#1E2A4A'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[*crit3, act('mecpj', DOOR3, 0, 'stand', 'neutral', keys=kh3)],
        props=[P('cuisine3', 'sgKitchen', pos=[0, 0, 0], opts={'night': True}), TILES('carreaux3', KP, strand=STRAND('S03', D3)), P('casserole3', 'sgPot', pos=POT, opts={'strands': False}),
               *[SPECS(c) for c in CRIT], *[P(f'verre3_{i}', 'sgGlass', on={'actor': c, 'hand': 'L', 'offset': [0, 0.0, 0.02]}) for i, c in enumerate(CRIT)]], cams=[C3])

# ================================================================= S04
# 4: two cuts. Two movers in plain grey coats and white gloves carry the tiled panel out like a big door, the strand a full tile below the line. Cut:
#    the kitchen open onto the street; a passer-by stops and looks in; the hero holds the pot's handle, the pot still boiling, and watches the wall go
D4 = st.dur('S04'); C4 = CUTAT(st.at('S04', 'L04', 6) - 0.1)
def PANEL4(t):   # the panel's pivot along its way: off the wall, out from the counter, then along toward the doorway
    if t <= 0.15: return KP
    if t <= 0.7: u = (t - 0.15) / 0.55; return [r(KP[0]), r(KP[1] + 0.08 * u), r(KP[2] + 0.75 * u)]
    u = min(1.0, (t - 0.7) / max(0.1, C4 - 0.7)); return [r(KP[0] + 1.1 * u), r(KP[1] + 0.08), r(KP[2] + 0.75 + 0.35 * u)]
TS4 = [r(0.15 + 0.15 * j) for j in range(int((C4 - 0.15) / 0.15) + 1)]
def MOVER(id_, side):   # each mover holds one end of the panel, walking with it
    ks = [k(0.0, clip='stand'), k(0.0, look=add(KP, [0.0, 1.2, 0.0]))]
    p0 = PANEL4(0.0); base = [r(p0[0] + side * 1.45), 0, r(p0[2] + 0.72)]
    ks.append(TK(0.0, {'R': R5([r(p0[0] + side * 1.2), r(p0[1] + 0.55), r(p0[2] + 0.05)]), 'L': R5([r(p0[0] + side * 1.2), r(p0[1] + 1.1), r(p0[2] + 0.05)])}, {'R': 'grip', 'L': 'grip'}, CALM, bend={'spine': SP(0.25)}, d=0.0))
    for t in TS4:
        p = PANEL4(t); ks.append(TK(t, {'R': R5([r(p[0] + side * 1.2), r(p[1] + 0.55), r(p[2] + 0.05)]), 'L': R5([r(p[0] + side * 1.2), r(p[1] + 1.1), r(p[2] + 0.05)])}, d=0.15, e='linear', keep=True))
    pe = PANEL4(C4); ks += [k(0.7, to=[r(pe[0] + side * 1.45), 0, r(pe[2] + 0.55)], dur=r(C4 - 0.7), clip='walk', face='keep', params={'freq': 1.3}), k(0.15, to=[r(p0[0] + side * 1.45), 0, r(p0[2] + 1.2)], dur=0.5, clip='walk', face='keep')]
    ks += [*blink(1.1, CALM), k(C4, visible=False)]
    return LOCKGAZE(act(id_, base, -90 * side, 'stand', 'neutral', keys=ks), gx=0.0, gy=-0.2)
CA4 = cam(0.0, [0.7, 1.7, 3.9], [0.85, 1.7, 3.75], [0.5, 1.45, -0.9], [0.95, 1.45, -0.9], lens=56)
STREET4 = [0, 0, -8.0]
CB4 = cam(C4, [-1.7, 1.55, 2.5], [-1.62, 1.55, 2.4], [0.3, 1.35, -1.6], [0.3, 1.35, -1.6], lens=50)
PASS4A, PASS4B = [-1.6, 0, -4.3], [0.4, 0, -4.3]
kp4 = [k(0.0, visible=False), k(C4, visible=True), k(C4, clip='walk'), k(C4, to=PASS4B, dur=0.7, clip='walk', face='keep'), k(r(C4 + 0.7), clip='stand', blend=0.1), k(r(C4 + 0.7), face=200, turn=0.25), k(C4, look=[0.6, 1.6, -0.6], lookDur=0.2), *blink(r(C4 + 1.0), CALM)]
kh4 = [k(0.0, visible=False), k(C4, visible=True), k(0.0, clip='stand'), k(0.0, look=[2.0, 1.4, -2.0]), TK(0.0, {'R': R5(add(POT, [0.26, 0.24, 0.0]))}, {'R': 'grip'}, face={'lid': 0.3, 'mouth': 'line', 'brow': 0.6}, d=0.0), *blink(r(C4 + 0.5), SAD), TK(r(C4 + 0.9), face={'lid': 0.4, 'mouth': 'line', 'brow': 0.7, 'gx': 0.4}, d=0.15, keep=True)]
km4 = [k(0.0, visible=False), k(C4, visible=True), k(0.0, clip='walk'), k(C4, to=[3.3, 0, -3.3], dur=r(D4 - C4), clip='walk', face='keep')]
st.shot('S04', 'whiteVoid', setOpts={'color': '#BFE0F0'}, look={'sunDir': [0.4, 0.9, 0.5]},
        actors=[MOVER('demenageur1', -1), MOVER('demenageur2', 1), act('passant', PASS4A, 90, 'walk', 'neutral', keys=kp4), act('mec', HOB, 125, 'stand', 'neutral', keys=kh4)],
        props=[P('cuisine4', 'sgKitchen', pos=[0, 0, 0], keys=[k(C4, visible=False)]), P('cuisine4b', 'sgKitchen', pos=[0, 0, 0], opts={'open': True}, keys=[k(0.0, visible=False), k(C4, visible=True)]),
               P('rue4', 'sgStreet', pos=STREET4, opts={'roadZ': 0.0}, keys=[k(0.0, visible=False), k(C4, visible=True)]),
               P('carreaux4', 'sgTiles', pos=KP, opts={'strand': STRAND('S04', D4)}, keys=[*[k(t, to=PANEL4(t), dur=0.15, ease='linear') for t in TS4], k(C4, to=[1.6, 1.03, -1.2], dur=0.01), k(r(C4 + 0.02), to=[3.6, 1.03, -3.6], dur=r(D4 - C4 - 0.05), ease='linear')]),
               P('casserole4', 'sgPot', pos=POT), P('minuteur4', 'sgTimer', pos=TIMER, ry=-20), STEAM('vapeur4', add(POT, [0, 0.3, 0]), (0.3, 0.05))], cams=[CA4, CB4])

# ================================================================= S05
# 5: the museum: the three critics in a row before the panel in its huge gilt frame, chins in hand, tilt their heads the same way at the same moment;
#    a red rope on brass posts, a dozing guard, a small blank label. The strand one and a half tiles below the line, a third of the frame wide
D5 = st.dur('S05'); TILT5 = r(D5 * 0.5)
CR5 = [[-1.45, 0, 0.55], [-0.8, 0, 0.7], [-0.15, 0, 0.55]]
C5 = cam(0.0, [0.25, 1.75, 5.6], [0.25, 1.75, 5.45], [0.0, 1.72, -1.4], [0.0, 1.72, -1.4], lens=40)
GARDE = [-1.95, 0, -0.85]
def CRITIC_ROW(prefix, pts, ry, tilt_t, tilt, D, nod=False):
    out = []
    for i, p in enumerate(pts):
        ks = [k(0.0, clip='stand'), k(0.0, look=[r(p[0] * 0.6), 2.4, -1.4]), TK(0.0, touch=CHIN('R'), reach={'L': R5(off(p, ry, 0.25, -0.12, 1.1))}, hands={'L': 'grip'}, face={'lid': 0.45, 'mouth': 'line', 'brow': -0.5}, d=0.0),
              TK(tilt_t, bend=TILT(tilt), d=0.25, e='out', keep=True), *BREATHE(0.1, D, 0.6, 0.015)]
        if nod: ks += [TK(r(tilt_t + 0.45), bend={'neck': [0.25, tilt, 0, 1, None]}, d=0.2, keep=True), TK(r(tilt_t + 0.75), bend={'neck': [0.0, tilt, 0, 1, None]}, d=0.2, keep=True), TK(r(tilt_t + 1.05), bend={'neck': [0.25, tilt, 0, 1, None]}, d=0.2, keep=True), TK(r(tilt_t + 1.35), bend={'neck': [0.0, tilt, 0, 1, None]}, d=0.2, keep=True)]
        out.append(LOCKGAZE(act(CRIT[i], p, ry, 'stand', 'neutral', keys=ks), gx=0.0, gy=-0.6))
    return out
def GUARD(D, wake=None):
    ks = [k(0.0, clip='sit'), k(0.0, look=add(GARDE, [0.4, 0.6, 0.9])), TK(0.0, face={'lid': 1.0, 'mouth': 'line', 'brow': 0.0}, bend={'neck': SP(0.45), 'spine': SP(0.1)}, d=0.0), *BREATHE(0.0, D, 0.9, 0.025)]
    if wake is not None: ks += [TK(wake, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 0.8}, bend={'neck': SP(-0.2), 'spine': SP(-0.1)}, sq=(0.92, 1.12, 0.92), d=0.06, e='out', keep=True), TK(r(wake + 0.2), sq=(1, 1, 1), d=0.1, keep=True), k(r(wake + 0.1), look='camera', lookDur=0.1)]
    return act('gardien', add(GARDE, [0, 0.0, 0]), 25, 'sit', 'neutral', keys=ks)
def MUSEUM(n, strand=None, night=False, morning=False, frame=True, extra=()):
    return [P(f'musee{n}', 'sgMuseum', pos=[0, 0, 0], opts={'night': night, 'morning': morning}), *([TILES(f'carreaux{n}', MP, strand=strand)] if frame else []),
            *([P(f'cadre{n}', 'sgGilt', pos=MP, opts={'w': 2.4, 'h': 1.6, 'b': 0.28})] if frame else []), P(f'cartel{n}', 'sgLabel', pos=[1.75, 1.35, -1.43]),
            P(f'cordon{n}', 'sgRope', pos=[0.0, 0, -0.55], opts={'len': 3.0}), P(f'chaise{n}', 'sgChair', pos=GARDE, ry=25), P(f'casquette{n}', 'sgCap', on={'actor': 'gardien', 'joint': 'head', 'offset': [0, 0.47, 0.0]}, opts=dict(extra)) if extra is not None else None]
st.shot('S05', 'whiteVoid', setOpts={'color': '#F4F3EF'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[*CRITIC_ROW('c5', CR5, 180, TILT5, 0.32, D5), GUARD(D5)],
        props=[*MUSEUM(5, STRAND('S05', D5)), *[SPECS(c) for c in CRIT]], cams=[C5])

# ================================================================= S06
# 6: the artist's attic: a painter in a smock and beret throws his brush out of the window and flings a handful of pasta at the canvas: a cartoon
#    tomato splat with five strands; one strand slaps back onto his face and hangs from his nose
D6 = st.dur('S06'); THROW6 = 0.35; FLING6 = 0.95; SPLAT6 = 1.2; SLAP6 = 1.45
PT6 = [0.45, 0, 0.35]; EASEL6 = [-1.05, 0, -0.6]
C6 = cam(0.0, [0.9, 1.7, 3.9], [0.86, 1.7, 3.76], [-0.3, 1.4, -0.5], [-0.3, 1.4, -0.5], lens=46)
kp6 = [k(0.0, clip='stand'), k(0.0, look=[1.4, 1.6, -1.6]), TK(0.0, {'R': R5(off(PT6, 150, 0.3, 0.25, 1.4))}, {'R': 'grip'}, face={'lid': 0.3, 'mouth': 'smile', 'brow': 0.6}, d=0.0),
       TK(0.15, {'R': R5(off(PT6, 150, -0.1, 0.35, 1.8))}, bend={'spine': SP(-0.15)}, d=0.12, keep=True), TK(THROW6, {'R': R5([1.0, 1.9, -1.2])}, bend={'spine': SP(0.1)}, d=0.08, e='out', keep=True),   # the brush out of the window
       k(0.55, look=add(EASEL6, [0, 1.4, 0]), lookDur=0.2), TK(0.7, {'R': R5(off(PT6, 210, -0.15, 0.3, 1.5))}, {'R': 'grip'}, d=0.15, keep=True), TK(FLING6, {'R': R5(add(EASEL6, [0.35, 1.35, 0.5]))}, bend={'spine': SP(0.2)}, d=0.07, e='out', keep=True),
       TK(SLAP6, face={'lid': 0.9, 'mouth': 'wavy', 'brow': 0.6}, sq=(1.05, 0.95, 1.05), bend={'neck': SP(-0.15)}, d=0.05, keep=True), k(r(SLAP6 + 0.1), look='camera', lookDur=0.15), TK(r(SLAP6 + 0.25), face={'lid': 0.3, 'mouth': 'line', 'brow': 0.3}, sq=(1, 1, 1), d=0.1, keep=True)]
st.shot('S06', 'whiteVoid', setOpts={'color': '#F0E4CC'}, look={'sunDir': [-0.3, 0.9, 0.4]},
        actors=[act('peintre', PT6, 200, 'stand', 'neutral', keys=kp6)],
        props=[P('atelier6', 'sgStudio', pos=[0, 0, 0]), P('chevalet6', 'sgEasel', pos=EASEL6, ry=20, opts={'w': 1.0, 'h': 1.2, 'art': 'splat', 'at': SPLAT6}), P('beret6', 'sgBeret', on={'actor': 'peintre', 'joint': 'head', 'offset': [0, 0.47, 0]}),
               P('pinceau6', 'sgBrush', on={'actor': 'peintre', 'hand': 'R', 'offset': [0, 0, 0]}, keys=[k(THROW6, detach=True), k(THROW6, to=[1.4, 1.7, -2.6], dur=0.35, ease='out'), k(r(THROW6 + 0.4), visible=False)]),
               P('poignee6', 'sgFling', pos=add(PT6, [-0.15, 1.5, -0.2]), opts={'at': FLING6, 'dur': 0.25, 'to': [-0.55, -0.0, -0.6]}),
               P('nez6', 'sgNoseStrand', on={'actor': 'peintre', 'joint': 'head', 'offset': [0, 0.2, 0.13]}, opts={'at': SLAP6})], cams=[C6])
st.cue('whoosh', 'S06', THROW6, 0.25); st.cue('pop', 'S06', SPLAT6, 0.4); st.cue('pop', 'S06', SLAP6, 0.3)

# ================================================================= S07
# 7: the art school: three students at their easels each hold a colander full of cooked pasta instead of a palette; the teacher demonstrates a huge
#    overhead throw like a shot-putter. Four people
D7 = st.dur('S07'); WIND7 = 0.6; THROW7 = 1.35
ST7 = [[-1.45, 0, -0.1], [-0.25, 0, -0.25], [0.95, 0, -0.1]]; PROF7 = [1.5, 0, 1.0]
C7 = cam(0.0, [0.5, 1.7, 5.4], [0.52, 1.7, 5.25], [0.35, 1.35, -0.2], [0.37, 1.35, -0.2], lens=54)
stud7 = []
for i, p in enumerate(ST7):
    ks = [k(0.0, clip='stand'), k(0.0, look=PROF7 and add(PROF7, [0, 1.8, 0])), TK(0.0, {'L': R5(off(p, 30, 0.35, -0.2, 1.1))}, {'L': 'grip'}, face={'lid': 0.3, 'mouth': 'line', 'brow': 0.3}, d=0.0),
          *blink(r(0.5 + 0.4 * i), CALM), *blink(r(2.1 + 0.2 * i), CALM), *BREATHE(0.1, D7, 0.6), TK(r(THROW7 + 0.1), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.9}, d=0.1, keep=True)]
    stud7.append(act(f'etudiant{i + 1}', p, 30, 'stand', 'neutral', keys=ks))
kprof7 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(off(PROF7, -40, 0.3, 0.2, 1.4))}, {'R': 'grip'}, face={'lid': 0.3, 'mouth': 'line', 'brow': -0.4}, d=0.0),
          TK(WIND7, {'R': R5(off(PROF7, -40, -0.25, 0.3, 1.75))}, sq=(1.06, 0.94, 1.06), bend={'spine': SP(-0.3, 0.15)}, face={'lid': 0.5, 'mouth': 'line', 'brow': -0.8}, d=0.35, keep=True),   # the shot-putter's crouch, the colander by his ear
          TK(THROW7, {'R': R5(off(PROF7, -40, 0.7, 0.1, 2.3))}, sq=(0.94, 1.08, 0.94), bend={'spine': SP(0.25, -0.1)}, face={'lid': 0.0, 'mouth': 'O', 'brow': 0.9}, d=0.12, e='out', keep=True),
          TK(r(THROW7 + 0.5), {'R': R5(off(PROF7, -40, 0.4, 0.2, 1.3))}, sq=(1, 1, 1), bend={'spine': SP(0.0)}, face={'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}, d=0.25, keep=True), *blink(r(D7 - 0.3), HAPPY)]
st.shot('S07', 'whiteVoid', setOpts={'color': '#EDE6D6'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[*stud7, act('prof', PROF7, -40, 'stand', 'neutral', keys=kprof7)],
        props=[P('ecole7', 'sgRoom', pos=[0, 0, 0], opts={'wall': '#E8E2D2'}), *[P(f'chevalet7_{i}', 'sgEasel', pos=add(p, [-0.45, 0, -0.65]), ry=15) for i, p in enumerate(ST7)],
               *[P(f'passoire7_{i}', 'sgColander', on={'actor': f'etudiant{i + 1}', 'hand': 'L', 'offset': [0, 0, 0]}) for i in range(3)], P('passoire7_p', 'sgColander', on={'actor': 'prof', 'hand': 'R', 'offset': [0, 0, 0]}),
               P('vol7', 'sgFling', pos=off(PROF7, -40, 0.7, 0.1, 2.3), opts={'at': THROW7, 'dur': 0.6, 'to': [-2.6, 0.6, -2.0]})], cams=[C7])
st.cue('whoosh', 'S07', THROW7, 0.35)

# ================================================================= S08
# 8: two cuts. A museum wall: square raviolis stacked into a cubist face with one eye on its side; the corner ravioli slips. Cut: a landscape of
#    coquillette dots with a yellow sun; three dots slide down
D8 = st.dur('S08'); C8 = CUTAT(st.at('S08', 'L08', 6) - 0.1)
RAV = [-1.6, 0.8, -1.44]; COQ = [1.6, 0.95, -1.44]
CA8 = cam(0.0, [-1.6, 1.55, 1.9], [-1.6, 1.55, 1.75], [-1.6, 1.5, -1.44], [-1.6, 1.5, -1.44], lens=42)
CB8 = cam(C8, [1.6, 1.45, 1.6], [1.6, 1.45, 1.48], [1.6, 1.45, -1.44], [1.6, 1.45, -1.44], lens=42)
st.shot('S08', 'whiteVoid', setOpts={'color': '#F4F3EF'}, look={'sunDir': [0.3, 0.9, 0.6]}, actors=[],
        props=[P('musee8', 'sgMuseum', pos=[0, 0, 0]), P('ravioli8', 'sgRavioli', pos=RAV, opts={'slip': r(C8 * 0.55)}), P('cadreR8', 'sgGilt', pos=RAV, opts={'w': 1.2, 'h': 1.4, 'b': 0.16}),
               P('coquillettes8', 'sgCoquillettes', pos=COQ, opts={'slide': r(C8 + 0.6)}), P('cadreC8', 'sgGilt', pos=COQ, opts={'w': 1.3, 'h': 1.0, 'b': 0.14})], cams=[CA8, CB8])

# ================================================================= S09
# 9: two cuts. A front doorstep: a woman solemnly hands over one plain pasta packet and receives a ring of house keys; they shake hands. Cut: a family
#    of three at the dinner table eat plain white rice, glum; behind them on the sideboard a pasta packet sits in a small safe, its door ajar
D9 = st.dur('S09'); C9 = CUTAT(st.at('S09', 'L09', 7) - 0.1); EX9 = 0.75; SHAKE9 = 1.35
VEN9 = [0.45, 0, 0.35]; PRO9 = [-0.25, 0, -0.35]
CA9 = cam(0.0, [-2.2, 1.55, 2.4], [-2.12, 1.55, 2.3], [0.1, 1.3, 0.0], [0.1, 1.3, 0.0], lens=46)
kv9 = [k(0.0, clip='stand'), k(0.0, look=add(PRO9, [0, 1.75, 0])), TK(0.0, {'L': R5(off(VEN9, -135, 0.35, -0.15, 1.15))}, {'L': 'grip'}, face={'lid': 0.4, 'mouth': 'line', 'brow': -0.3}, d=0.0),
       TK(r(EX9 - 0.25), {'L': R5(lerp3(add(VEN9, [0, 1.2, 0]), add(PRO9, [0, 1.2, 0]), 0.5))}, d=0.25, keep=True), TK(r(EX9 + 0.3), {'L': R5(off(VEN9, -135, 0.3, -0.18, 1.05))}, d=0.25, keep=True),
       TK(SHAKE9, {'R': R5(lerp3(add(VEN9, [0, 1.05, 0]), add(PRO9, [0, 1.05, 0]), 0.5))}, {'R': 'grip'}, d=0.25, keep=True), *[TK(r(SHAKE9 + 0.25 + 0.12 * j), {'R': R5(add(lerp3(add(VEN9, [0, 1.05, 0]), add(PRO9, [0, 1.05, 0]), 0.5), [0, 0.04 * (1 if j % 2 else -1), 0]))}, d=0.1, keep=True) for j in range(4)], *blink(0.4, GRAVE)]
kp9 = [k(0.0, clip='stand'), k(0.0, look=add(VEN9, [0, 1.7, 0])), TK(0.0, {'L': R5(off(PRO9, 45, 0.35, -0.15, 1.15))}, {'L': 'grip'}, face={'lid': 0.4, 'mouth': 'line', 'brow': -0.3}, d=0.0),
       TK(r(EX9 - 0.25), {'L': R5(add(lerp3(add(VEN9, [0, 1.2, 0]), add(PRO9, [0, 1.2, 0]), 0.5), [0, 0.06, 0]))}, d=0.25, keep=True), TK(r(EX9 + 0.3), {'L': R5(off(PRO9, 45, 0.3, -0.18, 1.05))}, d=0.25, keep=True),
       TK(SHAKE9, {'R': R5(add(lerp3(add(VEN9, [0, 1.05, 0]), add(PRO9, [0, 1.05, 0]), 0.5), [0, 0, 0.02]))}, {'R': 'grip'}, d=0.25, keep=True), *[TK(r(SHAKE9 + 0.25 + 0.12 * j), {'R': R5(add(lerp3(add(VEN9, [0, 1.05, 0]), add(PRO9, [0, 1.05, 0]), 0.5), [0, 0.04 * (1 if j % 2 else -1), 0.02]))}, d=0.1, keep=True) for j in range(4)], *blink(0.9, GRAVE)]
for _k in (kv9, kp9): _k.append(k(C9, visible=False))
FAM9 = [[-0.65, 0, -0.5], [0.0, 0, -0.5], [0.65, 0, -0.5]]
CB9 = cam(C9, [0.35, 1.45, 2.9], [0.33, 1.45, 2.78], [0.25, 1.05, -0.6], [0.25, 1.05, -0.6], lens=48)
fam9 = []
for i, (nm, p) in enumerate(zip(['pere', 'mere', 'fils'], FAM9)):
    bowl = add(p, [0, 0.8, 0.42])
    ks = [k(0.0, visible=False), k(C9, visible=True), k(0.0, clip='sit'), k(0.0, look=add(bowl, [0, 0, 0])), TK(0.0, {'R': R5(add(bowl, [0.06, 0.06, 0.0]))}, {'R': 'pinch'}, SAD, bend={'neck': SP(0.25)}, d=0.0),
          *[TK(r(C9 + 0.25 + 0.55 * j + 0.15 * i), {'R': R5(add(p, [0.06, 1.25 if j % 2 == 0 else 0.86, 0.22 if j % 2 == 0 else 0.42]))}, d=0.25, keep=True) for j in range(4)], *blink(r(C9 + 0.6 + 0.3 * i), SAD)]
    fam9.append(act(nm, add(p, [0, 0.0, 0]), 0, 'sit', 'neutral', keys=ks, **({'scale': 0.72} if nm == 'fils' else {})))
st.shot('S09', 'whiteVoid', setOpts={'color': '#BFE0F0'}, look={'sunDir': [0.4, 0.9, 0.5]},
        actors=[act('vendeuse', VEN9, -135, 'stand', 'neutral', keys=kv9), act('proprio', PRO9, 45, 'stand', 'neutral', keys=kp9), *fam9],
        props=[P('rue9', 'sgStreet', pos=[0, 0, 0], opts={'roadZ': 7.0, 'cottages': []}, keys=[k(C9, visible=False)]), P('maison9', 'cottage', pos=[-0.4, 0, -4.4], opts={'w': 6.4, 'd': 7, 'h': 2.7, 'rh': 1.6, 'color': '#F0C6CF', 'roof': '#5E83C6', 'door': '#2F5E8C'}, keys=[k(C9, visible=False)]),
               P('paquet9', 'sgPacket', on={'actor': 'vendeuse', 'hand': 'L', 'offset': [0, -0.05, 0.03]}, keys=[k(EX9, attach='proprio', hand='L', offset=[0, -0.05, 0.03]), k(C9, visible=False)]),
               P('cles9', 'sgKeys', on={'actor': 'proprio', 'hand': 'L', 'offset': [0, -0.02, 0.03]}, keys=[k(EX9, attach='vendeuse', hand='L', offset=[0, -0.02, 0.03]), k(C9, visible=False)]),
               P('salle9', 'sgDining', pos=[0, 0, 0], keys=[k(0.0, visible=False), k(C9, visible=True)]), P('table9', 'sgTable', pos=[0, 0, 0], opts={'len': 2.0}, keys=[k(0.0, visible=False), k(C9, visible=True)]),
               *[P(f'chaise9_{i}', 'sgChair', pos=add(p, [0, 0, -0.05]), keys=[k(0.0, visible=False), k(C9, visible=True)]) for i, p in enumerate(FAM9)],
               *[P(f'riz9_{i}', 'sgRice', pos=add(p, [0, 0.765, 0.42]), keys=[k(0.0, visible=False), k(C9, visible=True)]) for i, p in enumerate(FAM9)],
               P('buffet9', 'sgSideboard', pos=[1.75, 0, -1.3], keys=[k(0.0, visible=False), k(C9, visible=True)]), P('coffre9', 'sgSafe', pos=[1.75, 0.84, -1.3], ry=-15, keys=[k(0.0, visible=False), k(C9, visible=True)])], cams=[CA9, CB9])

# ================================================================= S10
# 10: the museum: an insurer in a grey suit measures the gilt frame with a blank tape measure, nods and stamps a blank form on his clipboard; behind him
#     the strand has slid halfway down the tiles into a drooping S, an opaque drop beneath it. He never looks at it. The guard dozes. Two people
D10 = st.dur('S10'); MEAS10 = 0.3; NOD10 = 1.6; STAMP10 = 2.3
AS10 = [1.3, 0, -0.25]
C10 = cam(0.0, [0.4, 1.6, 5.6], [0.4, 1.6, 5.45], [0.35, 1.4, -1.0], [0.35, 1.4, -1.0], lens=46)
ka10 = [k(0.0, clip='stand'), k(0.0, look=[1.45, 0.3, -1.3]), TK(0.0, {'R': R5([1.5, 0.75, -1.15]), 'L': R5(off(AS10, -120, 0.3, -0.18, 1.1))}, {'R': 'grip', 'L': 'grip'}, face={'lid': 0.45, 'mouth': 'line', 'brow': -0.4}, bend={'spine': SP(0.45)}, d=0.0),
        TK(1.1, {'R': R5(off(AS10, -120, 0.3, 0.22, 1.05))}, bend={'spine': SP(0.0)}, d=0.3, keep=True), k(1.1, look=[1.4, 2.45, -1.4], lookDur=0.3),   # up along the frame's edge (never the strand)
        TK(NOD10, bend={'neck': SP(0.3)}, d=0.12, keep=True), TK(r(NOD10 + 0.2), bend={'neck': SP(0.0)}, d=0.12, keep=True), TK(r(NOD10 + 0.4), bend={'neck': SP(0.3)}, d=0.12, keep=True), TK(r(NOD10 + 0.6), bend={'neck': SP(0.0)}, d=0.12, keep=True),
        k(r(STAMP10 - 0.3), look=off(AS10, -120, 0.35, -0.18, 1.1), lookDur=0.2), TK(r(STAMP10 - 0.15), {'R': R5(off(AS10, -120, 0.35, -0.16, 1.3))}, d=0.12, keep=True), TK(STAMP10, {'R': R5(off(AS10, -120, 0.35, -0.16, 1.13))}, sq=(1.03, 0.97, 1.03), d=0.05, e='in', keep=True), TK(r(STAMP10 + 0.2), sq=(1, 1, 1), d=0.1, keep=True),
        *blink(0.8, GRAVE), *blink(2.8, GRAVE)]
st.shot('S10', 'whiteVoid', setOpts={'color': '#F4F3EF'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[LOCKGAZE(act('assureur', AS10, -120, 'stand', 'neutral', keys=ka10)), GUARD(D10)],
        props=[*MUSEUM(10, STRAND('S10', D10, shape='S')), P('metre10', 'sgTape', pos=[1.3, 0.28, -1.22], ry=180, opts={'len': [[0.0, 0.05], [MEAS10, 0.05], [1.0, 2.55], [r(NOD10 + 0.6), 2.55], [r(NOD10 + 0.75), 0.05]]}),
               P('bloc10', 'sgClipboard', on={'actor': 'assureur', 'hand': 'L', 'offset': [0, 0.05, 0.05], 'rot': [-1.2, 0, 0]}), P('tampon10', 'sgStamp', on={'actor': 'assureur', 'hand': 'R', 'offset': [0, -0.02, 0]}, keys=[k(0.0, visible=False), k(r(NOD10 + 0.75), visible=True)])], cams=[C10])
st.cue('thud', 'S10', STAMP10, 0.3)

# ================================================================= S11
# 11: the museum at night, deep blue, never black, the guard asleep: the strand slithers down the last tiles and drops to the floor, flop. The guard
#     jerks awake and his cap pops off
D11 = st.dur('S11'); FALL11 = [0.15, 0.8]; WAKE11 = r(FALL11[1] + 0.05)
C11 = cam(0.0, [-1.0, 1.4, 3.6], [-0.98, 1.38, 3.48], [-0.95, 1.0, -1.0], [-0.95, 1.0, -1.0], lens=56)
st.shot('S11', 'whiteVoid', setOpts={'color': '#24305A'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[GUARD(D11, wake=WAKE11)],
        props=[*MUSEUM(11, {**STRAND('S10', 0.0, shape='S', fall=[FALL11[0], FALL11[1], r(MP[1] + REF * TILE), 0.35]), 'drop': 0.4}, night=True, extra={'pop': r(WAKE11 + 0.02), 'land': [0.3, -1.3, 0.3]})], cams=[C11])
st.cue('thud', 'S11', FALL11[1], 0.35); st.cue('pop', 'S11', WAKE11, 0.3)

# ================================================================= S12
# 12: the museum in the morning, in front of the empty tiles: a restorer in a white coat and gloves holds the strand up in tweezers and bites the end:
#     it snaps in two big dry pieces with a crisp crack; she pulls a sour face. Behind her, the three critics freeze, chins in hand. Four people
D12 = st.dur('S12'); BITE12 = 0.85; SNAP12 = 0.95
RS12 = [0.25, 0, 0.25]; CR12 = [[-0.9, 0, -0.45], [-0.15, 0, -0.6], [0.75, 0, -0.5]]
C12 = cam(0.0, [0.3, 1.65, 3.5], [0.3, 1.65, 3.38], [0.1, 1.55, -0.5], [0.1, 1.55, -0.5], lens=46)
kr12 = [k(0.0, clip='stand'), k(0.0, look=off(RS12, 0, 0.35, 0.05, 1.75)), TK(0.0, {'R': R5(off(RS12, 0, 0.32, 0.12, 1.72))}, {'R': 'pinch'}, face={'lid': 0.3, 'mouth': 'line', 'brow': 0.2}, d=0.0),
        TK(r(BITE12 - 0.25), {'R': R5(off(RS12, 0, 0.2, 0.05, 1.83))}, face={'lid': 0.4, 'mouth': 'O', 'brow': 0.2, 'jaw': 0.4}, d=0.2, keep=True), TK(BITE12, face={'lid': 0.5, 'mouth': 'line', 'brow': -0.2}, d=0.05, keep=True),
        TK(SNAP12, {'R': R5(off(RS12, 0, 0.32, 0.15, 1.65))}, face={'lid': 0.8, 'mouth': 'zigzag', 'brow': 0.9}, sq=(1.04, 0.96, 1.04), d=0.06, e='out', keep=True), k(r(SNAP12 + 0.1), look='camera', lookDur=0.15),
        *[TK(r(SNAP12 + 0.25 + 0.15 * j), bend={'neck': [0, 0.18 * (1 if j % 2 else -1), 0, 1, None]}, d=0.12, keep=True) for j in range(4)], *blink(0.4, CALM)]
st.shot('S12', 'whiteVoid', setOpts={'color': '#F6F0E4'}, look={'sunDir': [0.5, 0.8, 0.5]},
        actors=[act('restauratrice', RS12, 0, 'stand', 'neutral', keys=kr12), *CRITIC_ROW('c12', CR12, 0, 0.5, 0.0, D12)],
        props=[*MUSEUM(12, None, morning=True, extra=None), P('pince12', 'sgTweezers', on={'actor': 'restauratrice', 'hand': 'R', 'offset': [0, 0.0, 0.02]}),
               P('sec12', 'sgDryStrand', on={'actor': 'restauratrice', 'hand': 'R', 'offset': [0.0, 0.11, 0.03]}, opts={'snap': SNAP12, 'len': 0.5}), *[SPECS(c) for c in CRIT]], cams=[C12])
st.cue('clack', 'S12', SNAP12, 0.5)

# ================================================================= S13
# 13: three cuts in the museum hall, one fall each: the tagliatelle drape slides off its canvas, the ravioli face collapses, the coquillettes drop as one
#     sheet that breaks into a heap; the gilt frames hang empty. SCANDALE
D13 = st.dur('S13'); C13a = CUTAT(st.at('S13', 'L13', 3) - 0.05); C13b = CUTAT(st.at('S13', 'L13', 5) - 0.05)
TAG = [0.0, 0.9, -1.44]
CA13 = cam(0.0, [0.0, 1.45, 2.0], [0.0, 1.42, 1.9], [0.0, 1.1, -1.44], [0.0, 1.1, -1.44], lens=50)
CB13 = cam(C13a, [-1.6, 1.4, 1.9], [-1.6, 1.38, 1.8], [-1.6, 1.0, -1.44], [-1.6, 1.0, -1.44], lens=50)
CC13 = cam(C13b, [1.6, 1.4, 1.8], [1.6, 1.38, 1.7], [1.6, 0.9, -1.44], [1.6, 0.9, -1.44], lens=50)
st.shot('S13', 'whiteVoid', setOpts={'color': '#F4F3EF'}, look={'sunDir': [0.3, 0.9, 0.6]}, actors=[],
        props=[P('musee13', 'sgMuseum', pos=[0, 0, 0]), P('tagliatelle13', 'sgTagliatelle', pos=TAG, opts={'fall': 0.2, 'floor': TAG[1]}), P('cadreT13', 'sgGilt', pos=TAG, opts={'w': 1.1, 'h': 1.3, 'b': 0.15}),
               P('ravioli13', 'sgRavioli', pos=RAV, opts={'fall': r(C13a + 0.12)}), P('cadreR13', 'sgGilt', pos=RAV, opts={'w': 1.2, 'h': 1.4, 'b': 0.16}),
               P('coquillettes13', 'sgCoquillettes', pos=COQ, opts={'fall': r(C13b + 0.12), 'floor': COQ[1]}), P('cadreC13', 'sgGilt', pos=COQ, opts={'w': 1.3, 'h': 1.0, 'b': 0.14})], cams=[CA13, CB13, CC13])
st.cue('thud', 'S13', 0.55, 0.3); st.cue('thud', 'S13', r(C13a + 0.5), 0.3); st.cue('thud', 'S13', r(C13b + 0.5), 0.3)
st.card('S13', 'SCANDALE', at=r(C13b + 0.05))

# ================================================================= S14
# 14: the three critics before an empty gilt frame, chins in hand, tilt their heads together the other way, nodding gravely
D14 = st.dur('S14'); TILT14 = 0.7
CR14 = [[-0.65, 0, 0.5], [0.0, 0, 0.65], [0.65, 0, 0.5]]
C14 = cam(0.0, [-0.9, 1.75, 4.6], [-0.85, 1.75, 4.45], [0.05, 1.7, -1.4], [0.05, 1.7, -1.4], lens=42)
st.shot('S14', 'whiteVoid', setOpts={'color': '#F4F3EF'}, look={'sunDir': [0.3, 0.9, 0.6]},
        actors=[*CRITIC_ROW('c14', CR14, 180, TILT14, -0.32, D14, nod=True)],
        props=[P('musee14', 'sgMuseum', pos=[0, 0, 0]), P('cadre14', 'sgGilt', pos=MP, opts={'w': 2.4, 'h': 1.6, 'b': 0.28, 'empty': True}), P('cartel14', 'sgLabel', pos=[1.75, 1.35, -1.43]), P('cordon14', 'sgRope', pos=[0.0, 0, -0.55], opts={'len': 3.0}), *[SPECS(c) for c in CRIT]], cams=[C14])

# ================================================================= S15
# 15: the hero's kitchen, still open onto the street: a courier in white gloves hands him a velvet-lined case holding the two dry halves. Behind the
#     hero the pot still boils and steams, the red egg timer beside it, exactly as in line 1
D15 = st.dur('S15'); GIVE15 = 0.7
HE15 = [-0.15, 0, -0.5]; CO15 = [-1.05, 0, 0.35]
C15 = cam(0.0, [0.1, 1.55, 3.1], [0.06, 1.55, 2.98], [-0.6, 1.25, -0.1], [-0.6, 1.25, -0.1], lens=50)
MID15 = lerp3(add(HE15, [0, 1.12, 0]), add(CO15, [0, 1.12, 0]), 0.5)
kc15 = [k(0.0, clip='stand'), k(0.0, look=add(HE15, [0, 1.8, 0])), TK(0.0, {'R': R5(add(MID15, [0.12, 0, 0.05])), 'L': R5(add(MID15, [0.3, 0, 0.05]))}, {'R': 'grip', 'L': 'grip'}, GRAVE, d=0.0), *blink(1.2, GRAVE)]
kh15 = [k(0.0, clip='stand'), k(0.0, look=add(MID15, [0, -0.05, 0])), TK(0.0, {'R': R5(off(HE15, -50, 0.3, 0.2, 1.0))}, face={'lid': 0.2, 'mouth': 'line', 'brow': 0.6}, d=0.0),
        TK(GIVE15, {'R': R5(add(MID15, [-0.15, 0, 0.05])), 'L': R5(add(MID15, [-0.02, 0, 0.08]))}, {'R': 'grip', 'L': 'grip'}, face={'lid': 0.2, 'mouth': 'O', 'brow': 0.7}, d=0.25, keep=True), k(r(GIVE15 + 0.4), look='camera', lookDur=0.2), *blink(r(GIVE15 + 0.8), CALM)]
st.shot('S15', 'whiteVoid', setOpts={'color': '#BFE0F0'}, look={'sunDir': [0.4, 0.9, 0.5]},
        actors=[act('coursier', CO15, 130, 'stand', 'neutral', keys=kc15), act('mec', HE15, -50, 'stand', 'neutral', keys=kh15)],
        props=[P('cuisine15', 'sgKitchen', pos=[0, 0, 0], opts={'open': True}), P('rue15', 'sgStreet', pos=STREET4, opts={'roadZ': 0.0}), P('casserole15', 'sgPot', pos=POT), P('minuteur15', 'sgTimer', pos=TIMER, ry=-20),
               STEAM('vapeur15', add(POT, [0, 0.3, 0]), (0.25, -0.1)), P('ecrin15', 'sgCase', pos=add(MID15, [0.1, 0.03, 0.05]), ry=-20)], cams=[C15])

# ================================================================= S16
# 16: two cuts. Close: he drops the two halves into the pot and gives the red egg timer a tiny twist, tick tick. Cut: he fishes out one fat strand on
#     his fork, looks for a wall (there isn't one), turns, and flicks it straight at the camera: it sticks across the lens in the same curve, a decal
#     above the subtitles, and at once starts to slide down. Hold
D16 = st.dur('S16'); C16 = CUTAT(st.at('S16', 'L16', 6) - 0.1); DROP16 = 0.3; TWIST16 = r(C16 - 0.75); FLICK16 = r(C16 + 1.45)
CA16 = cam(0.0, [-1.25, 1.6, -0.55], [-1.2, 1.58, -0.6], [0.0, 1.0, -1.28], [0.0, 1.0, -1.28], lens=46)
HE16 = [-0.3, 0, -0.55]
CB16F, CB16L = [0.15, 1.6, 2.0], [-0.2, 1.55, -0.55]
CB16 = cam(C16, CB16F, CB16F, CB16L, CB16L, lens=46)
_dx = [CB16L[i] - CB16F[i] for i in range(3)]; _n = math.sqrt(sum(v * v for v in _dx)); LENS16 = [r(CB16F[i] + _dx[i] / _n * 0.3) for i in range(3)]; LRY16 = round(math.degrees(math.atan2(-_dx[0], -_dx[2])), 1)
kh16 = [k(0.0, clip='stand'), k(0.0, look=add(POT, [0, 0.1, 0])), TK(0.0, {'R': R5(add(POT, [0.05, 0.4, 0.12]))}, {'R': 'pinch'}, CALM, bend={'spine': SP(0.2)}, d=0.0),
        TK(r(DROP16 + 0.05), {'R': R5(add(POT, [0.05, 0.3, 0.1]))}, {'R': 'spread'}, d=0.1, keep=True), k(r(TWIST16 - 0.2), look=add(TIMER, [0, 0.12, 0]), lookDur=0.2),
        TK(r(TWIST16 - 0.15), {'R': R5(add(TIMER, [0.0, 0.17, 0.03]))}, {'R': 'pinch'}, d=0.15, keep=True), TK(r(TWIST16 + 0.2), {'R': R5(add(TIMER, [0.02, 0.17, 0.03]))}, d=0.1, keep=True),
        k(C16, look=[-1.8, 1.6, -0.5], lookDur=0.15), TK(C16, {'R': R5(add(HE16, [0.1, 1.35, 0.35]))}, {'R': 'grip'}, face={'lid': 0.2, 'mouth': 'line', 'brow': 0.6}, bend={'spine': SP(0.0)}, d=0.05, keep=True),
        k(r(C16 + 0.45), look=[1.8, 1.6, -0.5], lookDur=0.2), k(r(C16 + 0.9), look='camera', lookDur=0.2), TK(r(C16 + 0.95), face={'lid': 0.5, 'mouth': 'tongueout', 'brow': -0.4}, d=0.08, keep=True),
        TK(r(FLICK16 - 0.25), {'R': R5(add(HE16, [0.05, 1.8, 0.1]))}, d=0.15, keep=True), TK(FLICK16, {'R': R5(add(HE16, [0.05, 1.7, 0.8]))}, bend={'spine': SP(0.15)}, d=0.06, e='out', keep=True),
        TK(r(FLICK16 + 0.3), face={'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}, d=0.1, keep=True), *blink(r(FLICK16 + 0.8), HAPPY), *BREATHE(r(FLICK16 + 0.3), D16, 0.5)]
st.shot('S16', 'whiteVoid', setOpts={'color': '#BFE0F0'}, look={'sunDir': [0.4, 0.9, 0.5]},
        actors=[act('mec', HE16, 165, 'stand', 'neutral', keys=[*kh16[:1], *kh16[1:], k(C16, face=180, turn=0.01), k(r(C16 + 0.85), face=5, turn=0.25)])],
        props=[P('cuisine16', 'sgKitchen', pos=[0, 0, 0], opts={'open': True}), P('rue16', 'sgStreet', pos=STREET4, opts={'roadZ': 0.0}), P('casserole16', 'sgPot', pos=POT), P('minuteur16', 'sgTimer', pos=TIMER, ry=-20, opts={'turn': [[0.0, 0.0], [r(TWIST16 - 0.02), 0.0], [r(TWIST16 + 0.2), 0.5]]}),
               STEAM('vapeur16', add(POT, [0, 0.3, 0]), (0.25, -0.1)), P('moities16', 'sgHalves', pos=add(POT, [0.0, 0.28, 0.0]), opts={'at': DROP16, 'dur': 0.25, 'h': 0.2}),
               P('fourchette16', 'sgForkStrand', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0, 0]}, opts={'hide': FLICK16}, keys=[k(0.0, visible=False), k(C16, visible=True)]),
               P('objectif16', 'sgLensStrand', pos=LENS16, ry=LRY16, opts={'w': 0.12, 'at': r(FLICK16 + 0.1), 'slide': [[r(FLICK16 + 0.25), 0.0], [r(D16), 0.012]]})], cams=[CA16, CB16])
st.cue('clack', 'S16', TWIST16, 0.25); st.cue('clack', 'S16', r(TWIST16 + 0.15), 0.25); st.cue('pop', 'S16', r(FLICK16 + 0.1), 0.45)

for g_ in [('S01', FLICK1, 'mec', 'flick'), ('S02', SHOT2, 'voisine', 'masterpiece'), ('S03', 1.3, 'mecpj', 'critics'), ('S04', r(C4 + 0.9), 'mec', 'pot'), ('S05', TILT5, 'critique2', 'tilt'),
           ('S06', SLAP6, 'peintre', 'slap'), ('S07', THROW7, 'prof', 'throw'), ('S09', SHAKE9, 'vendeuse', 'keys'), ('S10', NOD10, 'assureur', 'frame'), ('S11', WAKE11, 'gardien', 'wake'),
           ('S12', SNAP12, 'restauratrice', 'snap'), ('S14', TILT14, 'critique2', 'fall'), ('S15', GIVE15, 'mec', 'case'), ('S16', FLICK16, 'mec', 'lens')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])

for _sc in st.scenes:
    _sc['props'] = [p_ for p_ in _sc['props'] if p_ is not None]
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
TURTLE = lambda seed, pants, hair: GUEST('politique', seed, '#1A1A1E', shirt='#1A1A1E', lapel='#1A1A1E', tie='#1A1A1E', pants=pants, hair='slick', hairColor=hair)
st.write("Le spaghetti", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'mecpj': {**MEC, 'suit': '#9CC2E6', 'pants': '#9CC2E6', 'shirt': '#B8D4EE', 'tie': '#9CC2E6'},
    'voisine': GUEST('madame', 7101, '#F2A6C8', pants='#F2A6C8', shirt='#F8C8DC', lapel='#E890B8', tie='#F2A6C8', hair='curly', hairColor='#9A8E84'),
    'critique1': TURTLE(7102, '#3A3A40', '#8A8A8A'), 'critique2': TURTLE(7103, '#5A4A3A', '#2A2420'), 'critique3': TURTLE(7104, '#2E3A4A', '#C8C4BC'),
    'demenageur1': GUEST('worker', 7105, '#8A8E94', pants='#6A6E74', gloves='#FFFFFF'), 'demenageur2': GUEST('worker', 7106, '#8A8E94', pants='#6A6E74', gloves='#FFFFFF'),
    'passant': GUEST('politique', 7107, '#2E4A7A', pants='#3A3D44'), 'gardien': GUEST('politique', 7108, '#22305A', pants='#22305A'),
    'peintre': GUEST('worker', 7109, '#E8E2D4', pants='#5A6A8A', shirt='#F4F1EA'), 'etudiant1': GUEST('madame', 7110, '#2E3A5A'), 'etudiant2': GUEST('politique', 7111, '#C8A030'), 'etudiant3': GUEST('sportif', 7112, '#7A2E3A'),
    'prof': GUEST('politique', 7113, '#6A6E74'), 'vendeuse': GUEST('madame', 7114, '#5A6E9A'), 'proprio': GUEST('politique', 7115, '#7A5A3A'),
    'pere': GUEST('politique', 7116, '#4A5A6A'), 'mere': GUEST('madame', 7117, '#8A5A6A'), 'fils': GUEST('sportif', 7118, '#3A6A8A', build={'width': 1.0, 'headWidth': 1.3, 'headScale': 1.3}),
    'assureur': GUEST('politique', 7119, '#6A6E74', pants='#5A5E64'), 'restauratrice': GUEST('madame', 7120, '#F4F4F2', pants='#E8E8E4', gloves='#FFFFFF'), 'coursier': GUEST('worker', 7121, '#2E4A6A', gloves='#FFFFFF'),
})
