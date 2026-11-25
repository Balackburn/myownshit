#!/usr/bin/env python3
"""La fuite (story 99, cycle 53; an institutional escalation from a drip, a bill and a dry last line).
This man reported a leak; the secret service landed: a leak under the sink. An hour later his sink was classified, every drop filed. The drops fell
in morse and gave the palace password; the palace changed it, the next drop gave the new one. The press: the leak of the century. The interior
minister resigned (he had let it run). The president ordered it sealed: the army drowned the sink in concrete, the fridge too. The leak came out at
the neighbour's below, arrested for receiving. The service sent its best plumber: a new washer, ten cents; invoice, three million, classified. The
tap no longer leaks. It listens.
Staging: a pale green kitchen (fuKitchen in whiteVoid, back wall at z 0, door in the back wall at x 2.2, sink at x 0, fridge at x -2.1) holds S01-S03,
S05, S07 (cut from the palace office corner built at x 30), S15, S17, S18. Agents in black suits and shades indoors (shades has its earpiece wire); the
plumber in navy overalls, a cap and shades. The hero in a pale blue bathrobe holds the same dirty plate in S01 and S03 and rinses it in S17. Drops:
fuDrop (head-sized, glossy, swell then fall and splash) with a plic (sfx:splat) in S02, S05, S07, S12; none in S17. S04 one standing drop with eyes
and a blank plate against a height chart without figures, front then side, a flash each. S06 a generic palace (no flag, no emblem) with a giant
padlock on its gate that pops open. S08 a kiosk whose papers all show one drop. S09 the minister down the palace steps with a dripping box. S10 the
decree held upright by an aide, the stamp brought down on it, the sink drawing circled behind. S11 a mixer truck pouring through the window, cut to
the concrete block with the fridge's top corner and its magnet. S12-S13 the neighbour's bowl (crisps, then water). S14 a black van, the plumber's slow
walk. S15 the washer flat on his open mitten, a tag with a drawn coin. S16 the invoice unrolling across the floor, rolled up into a safe that slams.
S18 the spout swivels after the hero, then a red light in a grille inside it.
Cards: FUITE (S08), BÉTON (S11). No word on screen otherwise; no digit, flag, emblem or brand; nobody hurt.
Lessons applied: prefixed props (fu); one shot per line; k(0.0, clip=...); hands by side (R at his right, s > 0 in off()); faces above the captions,
heads under the card band on the card shots; space between heads; valid sfx names only (checked by the audit)."""
from story_kit import *
import math

st = Story('fuite', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 19)])
PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
def lerp3(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
CHECKS = []
def chk(sid, c, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(c['from'], c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
    if c.get('to'): CHECKS.append(f"{sid}(end): " + ' | '.join(f"{n} {project(c['to'], c.get('lookAt2') or c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
def fcam(at, frm, pts, top=0.08, bottom=0.76, margin=0.05, push=0.15, lenses=range(30, 61), ease='linear'):
    """a camera at frm (backed off along its bearing if needed) aimed and lensed by fit() to hold every point, pushing in `push` m over the shot"""
    f, look, lens = fitBack(frm, pts, top=top, bottom=bottom, margin=margin, lenses=lenses)
    d = [look[i] - f[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in d)); to = [r(f[i] + d[i] / n * push) for i in range(3)]
    return cam(at, f, to, look, look, lens=lens, ease=ease)
def R5(p, w=1, s=0.04): return [*p, w, s]
EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
def TK(t, reach=None, hands=None, face=None, sq=None, bend=None, d=0.12, e='inOut', keep=False, scl=None, plant=None):
    tn = {}
    if reach: tn['reach'] = reach
    if hands: tn['hands'] = hands
    if face: tn['face'] = face
    if sq: tn['sq'] = list(sq)
    if bend: tn['bend'] = bend
    if scl: tn['scl'] = scl
    if plant: tn['plant'] = plant
    return k(t, toon=tn, toonDur=d, toonEase=e, **({'keepPose': True} if keep else {}))
def blink(t, face): return [k(t, toon={'face': {**face, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face}, toonDur=0.06, keepPose=True)]
def SP(a, side=0.0): return [a, side, 0, 1, None]
def BREATHE(t0, t1, every=0.55, a=0.012): return [k(r(t0 + i * every), toon={'sq': [1 - a * 0.5, 1 + a, 1 - a * 0.5] if i % 2 == 0 else [1, 1, 1]}, toonDur=r(every * 0.9), toonEase='inOut', keepPose=True) for i in range(int((t1 - t0) / every) + 1)]
def DROP(pid, actor, offset, scale, t0=None):
    """a sweat drop on an actor's head (scale grows from shot to shot)"""
    return P(pid, 'sweatDrop', on={'actor': actor, 'joint': 'head', 'offset': offset}, scale=scale, **({'keys': [k(0.0, visible=False), k(t0, visible=True)]} if t0 else {}))


# faces
CALM = {'lid': 0.3, 'mouth': 'line', 'brow': 0.0}
WORRY = {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}
GRAVE = {'lid': 0.4, 'mouth': 'line', 'brow': -0.4}
STERN = {'lid': 0.35, 'mouth': 'line', 'brow': -0.6}
SMUG = {'lid': 0.35, 'mouth': 'smile', 'brow': 0.2}
SAD = {'lid': 0.5, 'mouth': 'line', 'brow': 0.5}

def HANDS(p, ry, rf=0.25, rs=0.25, ry_=1.0, lf=0.25, ls=-0.25, ly=1.0):
    """two hands by the body: R at his right (s > 0), L at his left (s < 0)"""
    return {'R': R5(off(p, ry, rf, rs, ry_)), 'L': R5(off(p, ry, lf, ls, ly))}
SHADE = [0.0, 0.4, 0.2]
def AGENT(sid, i): return [P(f'lunettes{sid}_{i}', 'shades', on={'actor': f'agent{i}', 'joint': 'head', 'offset': SHADE}, opts={'s': 1.25})]
PLATE = lambda sid, actor='mec', hand='L': P(f'assiette{sid}', 'fuPlate', on={'actor': actor, 'hand': hand, 'offset': [0, -0.06, 0.06], 'rot': [1.2, 0, 0]})
PLIC = 'sfx:splat'

# ================================================================= the kitchen (S01-S03, S05, S07, S15, S17, S18), whiteVoid, back wall at z 0
KIT = [0, 0, 0]
def KITCHEN(sid, **o): return P(f'cuisine{sid}', 'fuKitchen', pos=KIT, opts={'doorX': 2.2, 'phoneX': 1.25, **o})
DRIP = [0.0, 0.48, 0.33]
LOOKK = {'sunDir': [0.35, 0.9, 0.8]}
KV = {'color': '#DCE8E0'}

# ================================================================= S01
# 1: low at cupboard height: the hero in his bathrobe, his dirty plate in his left hand, hangs up the wall phone with his right; on « Les
#    services secrets » the door in the back wall bursts open and three agents in black suits and shades stride in
D1 = st.dur('S01'); HANG1, BURST1 = 0.55, r(st.at('S01', 'L01', 6) - 0.1)
HER1 = [1.05, 0, 0.75]; HRY1 = -20
AG1 = [([2.2, 0, 0.3], [1.95, 0, 1.25]), ([2.35, 0, 0.0], [2.55, 0, 1.75]), ([2.05, 0, -0.2], [1.45, 0, 1.85])]
C1 = fcam(0.0, [0.4, 0.75, 4.6], {'heroTop': add(HER1, [0, 2.3, 0]), 'heroFeet': HER1, 'agTop': add(AG1[1][1], [0, 2.35, 0]), 'door': [2.2, 2.1, 0.0], 'ag3': add(AG1[2][1], [0, 2.35, 0]), 'ag3b': AG1[1][1]}, top=0.1, bottom=0.86, margin=0.1, push=0.25)   # low
chk('S01', C1, {'heroFace': add(HER1, [0, 1.95, 0]), 'phone': [1.25, 1.5, 0.05], 'ag1': add(AG1[0][1], [0, 2.0, 0]), 'ag2': add(AG1[1][1], [0, 2.0, 0]), 'ag3': add(AG1[2][1], [0, 2.0, 0])})
k1 = [k(0.0, clip='stand'), k(0.0, look=[1.25, 1.55, 0.05]), TK(0.0, {'R': R5(off(HER1, HRY1, 0.15, 0.22, 1.95)), 'L': R5(off(HER1, HRY1, 0.38, -0.2, 1.1))}, {'R': 'grip', 'L': 'grip'}, CALM, bend={'neck': SP(0.0, -0.2)}, d=0.0),
      TK(0.3, {'R': R5([1.22, 1.52, 0.18])}, {'R': 'grip'}, d=0.22, keep=True), TK(HANG1, {'R': R5([1.18, 1.5, 0.14])}, {'R': 'open'}, d=0.08, keep=True),
      TK(0.85, {'R': R5(off(HER1, HRY1, 0.15, 0.3, 0.95))}, {'R': 'rest'}, d=0.2, keep=True), k(0.85, look='camera', lookDur=0.2),
      TK(r(BURST1 + 0.04), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.9, 'pop': 0.6}, sq=(0.92, 1.1, 0.92), d=0.05, keep=True), k(r(BURST1 + 0.05), look=[2.2, 1.8, 0.4], lookDur=0.08),
      TK(r(BURST1 + 0.25), face={**WORRY, 'pop': 0.0}, sq=(1, 1, 1), d=0.15, keep=True), *blink(0.95, CALM), *BREATHE(0.9, BURST1, 0.5, 0.012)]
agents1 = []
for i, (a, b) in enumerate(AG1):
    t0 = r(BURST1 + 0.12 + 0.12 * i)
    ks = [k(0.0, clip='stand'), k(0.0, visible=False), k(t0, visible=True), k(t0, to=b, dur=r(D1 - t0 - 0.1), clip='walk', ease='out', face='keep'), k(0.0, look='camera'),
          TK(0.0, HANDS(a, yaw(a, b), 0.1, 0.25, 0.95, 0.1, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, STERN, d=0.0)]
    agents1.append(act(f'agent{i + 1}', a, yaw(a, b), 'stand', 'neutral', keys=ks))
st.shot('S01', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('mec', HER1, HRY1, 'stand', 'neutral', keys=k1), *agents1],
        props=[KITCHEN('S01', burstAt=BURST1, handsetFrom=HANG1), PLATE('S01'), P('combine1', 'fuHandset', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.04, 0.03]}, keys=[k(0.0, visible=True), k(HANG1, visible=False)]),
               *[x for i in range(1, 4) for x in AGENT('S01', i)]], cams=[C1])
st.cue('clack', 'S01', HANG1, 0.3); st.cue('thud', 'S01', BURST1, 0.5); st.cue('whoosh', 'S01', r(BURST1 + 0.02), 0.25, 0.12, 300, 2000)

# ================================================================= S02
# 2: close on the open cupboard under the sink: one fat bright drop swells on the pipe and falls into a small saucepan, plic; three agents crouch
#    round it in a row, shades on, staring
D2 = st.dur('S02'); FALL2 = 0.15
PAN = [0.0, 0.08, 0.33]
AG2 = [[-0.55, 0, 0.95], [0.55, 0, 0.95], [0.85, 0, 1.35]]
C2 = cam(0.0, [0.2, 1.4, 4.0], [0.2, 1.38, 3.8], [0.197, -0.393, -5.838], [0.197, -0.393, -5.838], lens=57)
chk('S02', C2, {'drop': DRIP, 'pan': PAN, **{f'face{i}': add(p, [0, 1.25, 0]) for i, p in enumerate(AG2)}})
agents2 = []
for i, p in enumerate(AG2):
    ry = yaw(p, [0, 0, 0.33])
    ks = [k(0.0, clip='kneel'), k(0.0, look=add(DRIP, [0, -0.15, 0])), TK(0.0, HANDS(p, ry, 0.3, 0.2, 0.55, 0.3, -0.2, 0.55), {'R': 'rest', 'L': 'rest'}, STERN, bend={'spine': SP(0.25), 'neck': SP(0.05)}, d=0.0),
          TK(r(0.85 + 0.03 * i), bend={'spine': SP(0.35), 'neck': SP(0.2)}, face={**STERN, 'brow': -0.8}, d=0.1, keep=True), k(r(1.05 + 0.04 * i), look='camera', lookDur=0.12)]
    agents2.append(act(f'agent{i + 1}', p, ry, 'kneel', 'neutral', keys=ks))
st.shot('S02', 'whiteVoid', setOpts=KV, look=LOOKK, actors=agents2,
        props=[KITCHEN('S02', doors=1), P('casserole2', 'fuPan', pos=PAN), P('goutte2', 'fuDrop', pos=DRIP, opts={'s': 0.26, 'fall': [FALL2, 1.2, 0.18], 'once': True}),
               *[x for i in range(1, 4) for x in AGENT('S02', i)]], cams=[C2])
st.cue(PLIC, 'S02', r(FALL2 + 0.9), 0.45)

# ================================================================= S03
# 3: wider: two agents wind black-and-yellow tape round the sink, a third snaps a giant padlock on the cupboard doors; the hero in the doorway with
#    his plate
D3 = st.dur('S03'); TAPE3, LOCK3 = 0.35, r(st.at('S03', 'L03', 7) - 0.15)
HER3 = [2.25, 0, 0.45]; HRY3 = -25
AG3 = [[-0.8, 0, 0.95], [0.75, 0, 0.95], [0.45, 0, 1.25]]
C3 = fcam(0.0, [-0.3, 1.55, 5.6], {'heroTop': add(HER3, [0, 2.3, 0]), 'heroFeet': HER3, 'sinkL': [-0.9, 0.95, 0.6], 'aTop': add(AG3[0], [0, 2.35, 0]), 'floor': [0.2, 0, 1.6]}, top=0.1, bottom=0.82, margin=0.08, push=0.25)
chk('S03', C3, {'heroFace': add(HER3, [0, 1.95, 0]), 'lock': [0, 0.62, 0.72], **{f'a{i}': add(p, [0, 2.0, 0]) for i, p in enumerate(AG3)}})
k3 = [k(0.0, clip='stand'), k(0.0, look=[0, 0.8, 0.6]), TK(0.0, {'R': R5(off(HER3, HRY3, 0.15, 0.28, 0.95)), 'L': R5(off(HER3, HRY3, 0.38, -0.2, 1.1))}, {'R': 'rest', 'L': 'grip'}, WORRY, d=0.0),
      TK(r(LOCK3 + 0.02), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, sq=(1.04, 0.96, 1.04), d=0.04, keep=True), TK(r(LOCK3 + 0.2), face=WORRY, sq=(1, 1, 1), d=0.12, keep=True),
      k(r(LOCK3 + 0.5), look='camera', lookDur=0.2), *blink(0.8, WORRY), *blink(2.4, WORRY), *BREATHE(0.1, D3, 0.5, 0.012)]
agents3 = []
for i, p in enumerate(AG3):
    ry = 180 + [20, -20, 25][i]
    if i < 2:
        sx = [-1, 1][i]
        ks = [k(0.0, clip='stand'), k(0.0, look=[0, 0.8, 0.6]), TK(0.0, {'R': R5([sx * 0.2 - 0.15, 0.95, 0.68]), 'L': R5([sx * 0.2 + 0.15, 0.95, 0.68])}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.25)}, d=0.0),
              *[TK(r(TAPE3 + 0.25 * j), {'R': R5([sx * (0.2 + 0.25 * j) - 0.15, 0.95 - 0.15 * (j % 2), 0.7]), 'L': R5([sx * (0.2 + 0.25 * j) + 0.15, 0.9 - 0.15 * (j % 2), 0.7])}, d=0.22, keep=True) for j in range(4)]]
    else:
        ks = [k(0.0, clip='stand'), k(0.0, look=[0, 0.6, 0.7]), TK(0.0, {'R': R5([-0.15, 0.95, 0.85]), 'L': R5([0.15, 0.95, 0.85])}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.35)}, d=0.0),
              TK(r(LOCK3 - 0.15), {'R': R5([-0.1, 0.7, 0.8]), 'L': R5([0.1, 0.7, 0.8])}, d=0.15, keep=True), TK(LOCK3, {'R': R5([-0.1, 0.62, 0.78]), 'L': R5([0.1, 0.62, 0.78])}, {'R': 'open', 'L': 'open'}, sq=(1.04, 0.95, 1.04), d=0.05, keep=True),
              TK(r(LOCK3 + 0.25), {'R': R5(off(p, ry, 0.2, 0.25, 1.0)), 'L': R5(off(p, ry, 0.2, -0.25, 1.0))}, {'R': 'rest', 'L': 'rest'}, sq=(1, 1, 1), d=0.2, keep=True), k(r(LOCK3 + 0.3), look='camera', lookDur=0.15)]
    ks += [*blink(r(0.9 + 0.35 * i), STERN), *blink(r(2.2 + 0.2 * i), STERN), *BREATHE(r(0.05 + 0.1 * i), D3, 0.6, 0.012)] + ([k(r(2.0 + 0.3 * i), look='camera', lookDur=0.2)] if i < 2 else [])
    agents3.append(act(f'agent{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S03', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('mec', HER3, HRY3, 'stand', 'neutral', keys=k3), *agents3],
        props=[KITCHEN('S03', tape=TAPE3, burstAt=-1), P('cadenas3', 'fuPadlock', pos=[0, 0.62, 0.72], opts={'w': 0.38, 'open': True, 'shutAt': LOCK3}, keys=[k(0.0, visible=False), k(r(LOCK3 - 0.2), visible=True)]),
               PLATE('S03'), *[x for i in range(1, 4) for x in AGENT('S03', i)]], cams=[C3])
st.cue('sfx:zip', 'S03', TAPE3, 0.3); st.cue('clang', 'S03', LOCK3, 0.45)

# ================================================================= S04
# 4: the mugshot: one big drop stands against a height chart, holding a blank plate, front view then side view, a flash each time
D4 = st.dur('S04'); FL1, FL2 = 0.15, 0.85
DR4 = [0.0, 1.05, 0.0]
C4 = cam(0.0, [0.0, 1.0, 2.3], [0.0, 1.0, 2.2], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], lens=40)
chk('S04', C4, {'dropTop': add(DR4, [0, 0.3, 0]), 'plate': [0, 0.6, 0.1], 'chartTop': [0, 1.8, -0.2]})
st.shot('S04', 'whiteVoid', setOpts={'color': '#B9C4CC'}, look={'sunDir': [0.1, 0.8, 1.0]}, actors=[],
        props=[P('toise4', 'fuChart', pos=[0, 0, -0.35], opts={'w': 2.4}),
               P('goutte4', 'fuDrop', pos=DR4, ry=0, opts={'s': 0.75, 'eyes': True}, keys=[k(r(FL2 - 0.04), rotTo=[0, 1.45, 0], dur=0.06)]),
               P('plaque4', 'mugshotPlate', pos=[0, 0.58, 0.18], opts={'lines': [' ', ' '], 'w': 0.5, 'h': 0.28}),
               P('flash4', 'camFlash', pos=[0.35, 1.45, 0.9], opts={'at': [FL1, FL2], 'w': 0.6})], cams=[C4])
st.cue('sfx:shutter', 'S04', FL1, 0.45); st.cue('sfx:shutter', 'S04', FL2, 0.45)

# ================================================================= S05
# 5: close insert on the morse printer: a fat paper strip feeds out with thick dots and dashes; then a pull back to the agent in big headphones
#    kneeling with a microphone under the drip, plic
D5 = st.dur('S05'); PULL5 = 0.85; FALL5 = 0.6
MOR = [0.75, 0.0, 1.05]
AGM = [0.35, 0, 1.25]; AGRY = -150
C5 = cam(0.0, [0.75, 0.75, 1.75], [0.75, 0.7, 1.7], [0.75, 0.1, 1.35], [0.75, 0.1, 1.38], lens=40)
C5b = glide([cam(PULL5, [1.7, 1.15, 4.2], [1.7, 1.15, 4.3], [0.3, 0.75, 0.8], [0.3, 0.75, 0.8], lens=44)], 0.35)
chk('S05', C5, {'strip': [0.75, 0.13, 1.4], 'stripEnd': [0.75, 0.13, 1.65], 'box': [0.75, 0.2, 1.05]})
chk('S05b', C5b, {'agFace': add(AGM, [0, 1.25, 0]), 'agTop': add(AGM, [0, 1.6, 0]), 'drip': DRIP, 'strip': [0.75, 0.1, 1.5]})
kag5 = [k(0.0, clip='kneel'), k(0.0, look=DRIP), TK(0.0, {'R': R5([0.05, 0.26, 0.42]), 'L': R5(off(AGM, AGRY, 0.3, -0.2, 0.5))}, {'R': 'grip', 'L': 'rest'}, STERN, bend={'spine': SP(0.3), 'neck': SP(0.25)}, d=0.0),
        TK(1.2, face={**STERN, 'brow': -0.8, 'lid': 0.2}, d=0.08, keep=True), k(1.35, look='camera', lookDur=0.15)]
st.shot('S05', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('agent1', AGM, AGRY, 'kneel', 'neutral', keys=kag5)],
        props=[KITCHEN('S05', doors=1), P('morse5', 'fuMorse', pos=MOR, ry=0, opts={'s': 1.3, 'feed': [0.0, 1.6]}), P('goutte5', 'fuDrop', pos=DRIP, opts={'s': 0.22, 'fall': [0.25, 1.4, 0.3], 'once': True}),
               P('casque5', 'fuPhones', on={'actor': 'agent1', 'joint': 'head'}), P('micro5', 'fuMic', on={'actor': 'agent1', 'hand': 'R', 'offset': [0, -0.02, 0.04], 'rot': [1.5, 0, 0]}),
               P('casserole5', 'fuPan', pos=[0, 0.08, 0.33]), *AGENT('S05', 1)], cams=[C5, C5b])
st.cue('sfx:ticks', 'S05', 0.05, 0.3); st.cue(PLIC, 'S05', 1.3, 0.45)

# ================================================================= S06
# 6: the palace in one shot: a generic front, the fence and gate before it, a giant padlock on the gate pops open with a clunk
D6 = st.dur('S06'); OPEN6 = r(st.at('S06', 'L06', 4) - 0.05)
PAL = [0, 0, -9.0]; GATE = add(PAL, [0, 1.25, 7.2])
C6 = cam(0.0, [1.2, 0.9, 6.5], [1.0, 0.95, 5.8], [0.0, 3.0, -6.0], [0.0, 3.0, -6.0], lens=48)
chk('S06', C6, {'lock': GATE, 'palTop': add(PAL, [0, 8.1, 1.0]), 'palL': add(PAL, [-7, 3, 0]), 'gateFoot': add(PAL, [0, 0, 7.0])})
st.shot('S06', 'grassland', look={'sunDir': [0.5, 0.9, 0.8]}, actors=[],
        props=[P('palais6', 'fuPalace', pos=PAL, opts={'gateAt': r(OPEN6 + 0.5)}), P('cadenas6', 'fuPadlock', pos=GATE, opts={'w': 0.9, 'openAt': OPEN6}),
               P('cour6', 'parkLot', pos=add(PAL, [0, 0, 5]), opts={'w': 18, 'd': 10, 'color': '#D8D0BE'})], cams=[C6])
st.cue('clang', 'S06', OPEN6, 0.5); st.cue('sfx:rattle', 'S06', r(OPEN6 + 0.5), 0.3)

# ================================================================= S07
# 7: the palace office: a technician types, the padlock on his screen snaps shut green; a snap cut to the kitchen pipe: one more drop, plic, and
#    the agent in headphones writes it down
D7 = st.dur('S07'); SHUT7 = r(st.at('S07', 'L07', 3) + 0.05); CUT7 = r(st.at('S07', 'L07', 4) - 0.03)
OFF = [30.0, 0, 0.0]
TEC = add(OFF, [0.0, 0, 0.85]); TRY = 160
SCR = add(OFF, [0.0, 0.76, 0.0])
C7 = fcam(0.0, [r(OFF[0] + 1.8), 1.7, 2.6], {'scrTL': add(SCR, [-0.55, 0.95, 0]), 'scrBR': add(SCR, [0.55, 0.25, 0]), 'tecTop': add(TEC, [0, 2.35, 0]), 'tecFace': add(TEC, [0, 1.95, 0]), 'kb': add(SCR, [0, 0.0, 0.6])}, top=0.1, bottom=0.8, margin=0.12, push=0.2)   # from the side: the screen and his face
AGM7, AGRY7 = [0.5, 0, 1.15], -110   # turned toward the side camera, 3/4
C7b = fcam(CUT7, [-1.7, 1.15, 2.7], {'agTop': add(AGM7, [0, 1.85, 0]), 'agFace': add(AGM7, [0, 1.25, 0]), 'drip': DRIP, 'pan': [0, 0.08, 0.33], 'pad': off(AGM7, AGRY7, 0.35, -0.12, 0.45)}, top=0.15, bottom=0.8, margin=0.1, push=0.1)
chk('S07', C7, {'screen': add(SCR, [0, 0.6, 0]), 'tecFace': add(TEC, [0, 1.95, 0]), 'kb': add(SCR, [0, 0.05, 0.45])})
chk('S07b', C7b, {'agFace': add(AGM7, [0, 1.25, 0]), 'drip': DRIP, 'pad': add(AGM7, [0.1, 0.6, -0.3])})
ktec = [k(0.0, clip='stand'), k(0.0, look=add(SCR, [0, 0.5, 0])), TK(0.0, {'R': R5(add(SCR, [-0.15, 0.06, 0.45])), 'L': R5(add(SCR, [0.15, 0.06, 0.45]))}, {'R': 'point', 'L': 'point'}, CALM, bend={'spine': SP(0.25)}, d=0.0),
        *[TK(r(0.08 * j), {'R': R5(add(SCR, [-0.15 + 0.04 * (j % 3), 0.04 + 0.03 * (j % 2), 0.45])), 'L': R5(add(SCR, [0.15 - 0.04 * (j % 2), 0.04 + 0.03 * ((j + 1) % 2), 0.45]))}, d=0.07, keep=True) for j in range(7)],
        TK(SHUT7, face=SMUG, sq=(0.97, 1.04, 0.97), bend={'spine': SP(0.0)}, d=0.1, keep=True), k(r(SHUT7 + 0.1), look='camera', lookDur=0.15)]
FALL7 = r(CUT7 + 0.05)
kag7 = [k(0.0, clip='kneel'), k(0.0, look=DRIP), TK(0.0, {'R': R5([0.05, 0.26, 0.42]), 'L': R5(off(AGM7, AGRY7, 0.35, -0.12, 0.45))}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.3), 'neck': SP(0.25)}, d=0.0),
        TK(r(FALL7 + 1.1), face={**STERN, 'brow': -0.8, 'lid': 0.2}, d=0.08, keep=True), k(r(FALL7 + 1.15), look=off(AGM7, AGRY7, 0.35, -0.12, 0.45), lookDur=0.12),
        *[TK(r(FALL7 + 1.2 + 0.08 * j), {'R': R5(off(AGM7, AGRY7, 0.37, -0.05 + 0.03 * (j % 2), 0.47))}, {'R': 'pinch'}, d=0.07, keep=True) for j in range(5)]]
st.shot('S07', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('tech', TEC, TRY, 'stand', 'neutral', keys=ktec), act('agent1', AGM7, AGRY7, 'kneel', 'neutral', keys=kag7)],
        props=[KITCHEN('S07', doors=1), P('mur7', 'fuChart', pos=add(OFF, [0, 0, -1.0]), opts={'w': 0.01}), P('bureau7', 'desk', pos=add(OFF, [0, 0, 0.1]), opts={'w': 1.6}),
               P('ecran7', 'fuScreen', pos=SCR, opts={'shutAt': SHUT7, 'keys': [0.05, 0.13, 0.21, 0.3, 0.38, 0.46]}),
               P('goutte7', 'fuDrop', pos=DRIP, opts={'s': 0.22, 'fall': [FALL7, 1.4, 0.3], 'once': True}), P('casque7', 'fuPhones', on={'actor': 'agent1', 'joint': 'head'}),
               P('bloc7', 'clipboardProp', on={'actor': 'agent1', 'hand': 'L', 'offset': [0, -0.06, 0.05], 'rot': [1.2, 0, 0]}), P('casserole7', 'fuPan', pos=[0, 0.08, 0.33]), *AGENT('S07', 1)], cams=[C7, C7b])
st.cue('sfx:ticks', 'S07', 0.05, 0.3); st.cue('sfx:beep', 'S07', SHUT7, 0.35); st.cue(PLIC, 'S07', r(FALL7 + 1.05), 0.45)

# ================================================================= S08
# 8: a newsstand in the street: every paper has the same front page, a huge photo of one drop; passers-by stop and stare; FUITE
D8 = st.dur('S08'); CARD8 = st.at('S08', 'L08', 7)
KIO = [0.0, 0, -1.6]
PB = [([-0.85, 0, 1.3], 25), ([0.9, 0, 1.15], -30)]
C8 = fcam(0.0, [0.2, 1.4, 5.2], {'kioskTop': add(KIO, [0, 2.5, 0]), 'kioskL': add(KIO, [-1.35, 0.8, 0]), 'kioskR': add(KIO, [1.35, 0.8, 0]), 'p1': add(PB[0][0], [0, 2.3, 0]), 'p2': add(PB[1][0], [0, 2.3, 0])}, top=0.22, bottom=0.84, margin=0.13, push=0.25)
chk('S08', C8, {'paper': add(KIO, [0, 1.75, 0.05]), 'p1Face': add(PB[0][0], [0, 1.95, 0]), 'p2Face': add(PB[1][0], [0, 1.95, 0]), 'p1Top': add(PB[0][0], [0, 2.3, 0])})
pass8 = []
for i, (p, ry) in enumerate(PB):
    ks = [k(0.0, clip='stand'), k(0.0, look=add(KIO, [0, 1.6, 0])), TK(0.0, HANDS(p, ry, 0.15, 0.25, 0.95, 0.15, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, {'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, d=0.0),
          TK(r(0.5 + 0.2 * i), sq=(0.95, 1.06, 0.95), d=0.1, keep=True), TK(r(0.7 + 0.2 * i), sq=(1, 1, 1), d=0.15, keep=True), k(r(1.7 + 0.2 * i), look='camera', lookDur=0.2), *blink(r(1.2 + 0.3 * i), CALM)]
    pass8.append(act(f'passant{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S08', 'street', look={'sunDir': [0.5, 0.9, 0.7]}, actors=pass8,
        props=[P('kiosque8', 'fuKiosk', pos=KIO), P('journal8', 'fuPaper', on={'actor': 'passant2', 'hand': 'R', 'offset': [0, 0.12, 0.08]}, opts={'w': 0.42})], cams=[C8])
st.card('S08', 'FUITE', at=CARD8)
st.cue('sfx:paper', 'S08', 0.4, 0.3)

# ================================================================= S09
# 9: the palace steps: the interior minister walks down with a cardboard box in his arms; it drips on every step behind him; flashbulbs
D9 = st.dur('S09')
PAL9 = [0, 0, -3.0]
def stepY(z):   # the palace steps (fuPalace at PAL9): tops at 0.9 (z < -1.4), 0.6, 0.3, then the ground (z > 0.0)
    zz = z - PAL9[2]
    return 0.9 if zz < 1.6 else 0.6 if zz < 2.15 else 0.3 if zz < 2.7 else 0.0
MPATH = [[0.0, PAL9[2] + 1.3], [0.0, PAL9[2] + 1.9], [0.0, PAL9[2] + 2.45], [0.0, PAL9[2] + 3.0], [0.0, PAL9[2] + 3.6]]
C9 = cam(0.0, [1.6, 1.0, 4.2], [1.5, 1.0, 4.0], [0.0, 1.45, -0.6], [0.0, 1.35, -0.4], lens=46)
chk('S09', C9, {'minTop0': [0, 0.9 + 2.3, MPATH[0][1]], 'minFace1': [0, 1.95, MPATH[-1][1]], 'box': [0, 1.05, MPATH[-1][1] + 0.4]})
km9 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5([-0.25, 2.0, MPATH[0][1] + 0.38]), 'L': R5([0.25, 2.0, MPATH[0][1] + 0.38])}, {'R': 'open', 'L': 'open'}, SAD, d=0.0)]
tt = 0.15
for j in range(1, len(MPATH)):
    z = MPATH[j][1]; y = stepY(z); dt = 0.6
    km9 += [k(tt, to=[0.0, y, z], dur=dt, clip='walk', ease='inOut', face='keep'), TK(r(tt + dt), {'R': R5([-0.25, y + 1.1, z + 0.38]), 'L': R5([0.25, y + 1.1, z + 0.38])}, d=dt, e='linear', keep=True)]
    tt = r(tt + dt)
km9 += [*blink(1.0, SAD), *blink(2.4, SAD)]
st.shot('S09', 'grassland', look={'sunDir': [0.5, 0.9, 0.8]}, actors=[act('ministre', [0.0, 0.9, MPATH[0][1]], 0, 'stand', 'neutral', keys=km9)],
        props=[P('palais9', 'fuPalace', pos=PAL9, opts={'fenceZ': 30}), P('carton9', 'fuDripBox', on={'actor': 'ministre', 'joint': 'torso', 'offset': [0, -0.05, 0.38]}, opts={'rate': 0.35, 'fallH': 1.0}),
               P('flash9', 'flashBursts', pos=[0.9, 1.5, 1.6], opts={'n': 6, 'w': 1.6, 'h': 1.0, 'at': [0.3, 0.7, 1.1, 1.6, 2.0, 2.5, 2.9]})], cams=[C9])
for j in range(4): st.cue('sfx:step', 'S09', r(0.4 + 0.6 * j), 0.25)
st.cue(PLIC, 'S09', 0.9, 0.2); st.cue(PLIC, 'S09', 2.1, 0.2); st.cue('sfx:shutter', 'S09', 0.3, 0.3); st.cue('sfx:shutter', 'S09', 1.6, 0.3)

# ================================================================= S10
# 10: the president's office (no flag, no emblem): an aide holds the decree upright facing us, the president brings a big stamp down on it, elbow
#    bent; behind them a board with the drawing of the sink, circled
D10 = st.dur('S10'); STAMP10 = r(st.at('S10', 'L10', 3) + 0.05)
PRES = [-0.45, 0, -1.6]; PRY = 25
AIDE = [0.55, 0, -1.25]; ARY = -25
DEC = [0.15, 1.35, -0.85]
C10 = cam(0.0, [0.1, 1.55, 2.6], [0.1, 1.55, 2.4], [0.05, 1.45, -1.5], [0.05, 1.45, -1.5], lens=44)
chk('S10', C10, {'presFace': add(PRES, [0, 2.0, 0]), 'presTop': add(PRES, [0, 2.3, 0]), 'aideFace': add(AIDE, [0, 2.0, 0]), 'decree': DEC, 'board': [0.05, 2.15, -2.7]})
kp10 = [k(0.0, clip='stand'), k(0.0, look=DEC), TK(0.0, {'R': R5(add(DEC, [-0.05, 0.55, 0.12])), 'L': R5(off(PRES, PRY, 0.3, -0.25, 1.05))}, {'R': 'grip', 'L': 'rest'}, STERN, bend={'spine': SP(0.1)}, d=0.0),
        TK(r(STAMP10 - 0.2), {'R': R5(add(DEC, [-0.05, 0.7, 0.16]))}, {'R': 'grip'}, {**STERN, 'brow': -0.8}, sq=(0.97, 1.04, 0.97), d=0.15, keep=True),
        TK(STAMP10, {'R': R5(add(DEC, [0.02, 0.0, 0.2]))}, {'R': 'grip'}, {**STERN, 'lid': 0.1, 'mouth': 'clench'}, sq=(1.05, 0.94, 1.05), d=0.05, e='out', keep=True),
        TK(r(STAMP10 + 0.3), {'R': R5(add(DEC, [-0.05, 0.45, 0.2]))}, face=SMUG, sq=(1, 1, 1), d=0.2, keep=True), k(r(STAMP10 + 0.35), look='camera', lookDur=0.2), *blink(0.5, STERN)]
ka10 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(add(DEC, [-0.27, 0.0, -0.02])), 'L': R5(add(DEC, [0.27, 0.0, -0.02]))}, {'R': 'grip', 'L': 'grip'}, CALM, d=0.0),
        TK(STAMP10, face={'lid': 1.0, 'mouth': 'line', 'brow': 0.4}, sq=(1.02, 0.97, 1.02), d=0.04, keep=True), TK(r(STAMP10 + 0.15), face=CALM, sq=(1, 1, 1), d=0.1, keep=True), *blink(1.6, CALM)]
st.shot('S10', 'office', setOpts={'door': False, 'printer': False, 'carpet': False, 'picture': False}, look={'sunDir': [0.3, 0.9, 0.9]},
        actors=[act('president', PRES, PRY, 'stand', 'neutral', keys=kp10), act('aide', AIDE, ARY, 'stand', 'neutral', keys=ka10)],
        props=[P('decret10', 'fuDecree', on={'actor': 'aide', 'hand': 'R', 'offset': [0.27, 0.0, 0.02], 'rot': [1.5708, 0, 0]}, opts={'w': 0.5, 'stampAt': r(STAMP10 + 0.02)}),
               P('tampon10', 'fuStamp', on={'actor': 'president', 'hand': 'R', 'offset': [0, -0.02, 0.0]}, opts={'s': 1.3}), P('tableau10', 'fuSinkBoard', pos=[0.05, 0, -2.75], opts={'w': 0.9, 'y0': 1.85})], cams=[C10])
st.cue('thud', 'S10', STAMP10, 0.5)

# ================================================================= S11
# 11: outside his house: a mixer truck pours grey concrete through the kitchen window, soldiers guide the chute; a cut to the result: a huge smooth
#    grey block filling the kitchen, only the top corner of the white fridge sticking out, one magnet on it; BÉTON
D11 = st.dur('S11'); CUT11 = r(st.at('S11', 'L11', 7) - 0.03); CARD11 = st.at('S11', 'L11', 6)
MIX = [2.6, 0, -0.4]; MRY = -40   # its chute toward the house front
SOL = [[-0.2, 0, -1.9], [0.9, 0, -2.4]]
KIT11 = [60.0, 0, 0.0]
C11 = fcam(0.0, [2.0, 1.3, 6.5], {'chute': [0.0, 1.2, -2.6], 'streamEnd': [-1.3, 0.4, -3.7], 'drum': [1.9, 3.0, -1.0], **{f's{i}': add(p, [0, 2.3, 0]) for i, p in enumerate(SOL)}, 's0f': SOL[0]}, top=0.12, bottom=0.82, margin=0.08, push=0.25)
C11b = cam(CUT11, add(KIT11, [-0.7, 3.5, 5.0]), add(KIT11, [-0.75, 3.47, 4.8]), add(KIT11, [-1.65, 2.5, 1.5]), add(KIT11, [-1.65, 2.5, 1.5]), lens=46)   # above the block: its smooth top and the fridge corner with its magnet
chk('S11', C11, {'chute': [0.0, 1.2, -2.6], 'streamEnd': [-1.3, 0.4, -3.7], **{f's{i}': add(p, [0, 2.0, 0]) for i, p in enumerate(SOL)}, 'cab': add(MIX, [2.4, 2.4, 0])})
chk('S11b', C11b, {'fridge': add(KIT11, [-1.6, 2.9, 2.25]), 'blockL': add(KIT11, [-3.3, 1.3, 2.6]), 'blockR': add(KIT11, [3.3, 1.3, 2.6])})
sold = []
for i, p in enumerate(SOL):
    ry = 30 if i == 0 else -20
    ks = [k(0.0, clip='stand'), k(0.0, look=[-0.6, 0.9, -3.2]), TK(0.0, HANDS(p, ry, 0.45, 0.2, 1.35, 0.45, -0.2, 1.35) if i == 0 else HANDS(p, ry, 0.3, 0.3, 1.6, 0.25, -0.3, 1.1), {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.2)}, d=0.0),
          *[TK(r(0.4 + 0.45 * j), sq=(1.03, 0.97, 1.03) if j % 2 == 0 else (1, 1, 1), d=0.2, keep=True) for j in range(4)], k(1.6, look='camera', lookDur=0.2), *blink(1.0 + 0.4 * i, STERN)]
    sold.append(act(f'soldat{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S11', 'pavillon', setOpts={'fence': False, 'mailbox': False}, look={'sunDir': [0.5, 0.9, 0.7]}, actors=sold,
        props=[P('toupie11', 'fuMixer', pos=MIX, ry=MRY, opts={'pour': [0.1, 3.4], 'pourLen': 1.9}),
               P('cuisine11', 'fuKitchen', pos=KIT11, opts={'doorX': 2.2, 'tap': False, 'wallH': 6.0}), P('beton11', 'fuConcrete', pos=KIT11, opts={'fx': -1.6, 'fz': 1.9, 'h': 2.65})], cams=[C11, C11b])
st.card('S11', 'BÉTON', at=CARD11)
st.cue('engine', 'S11', 0.0, 0.3); st.cue('sfx:pour', 'S11', 0.2, 0.4)

# ================================================================= S12
# 12: downstairs: the neighbour on his sofa watches TV, a bowl of crisps on his knees; a drop forms on the ceiling and falls, plic, into the bowl
D12 = st.dur('S12'); FALL12 = 0.35
NB = [0.0, 0, -2.85]; NRY = 0
BOWL = add(NB, [0, 0.75, 0.62])
C12 = cam(0.0, [0.9, 1.3, 1.6], [0.88, 1.29, 1.45], [0.0, 1.55, -2.3], [0.0, 1.5, -2.3], lens=46)
chk('S12', C12, {'nbFace': add(NB, [0, 1.6, 0.15]), 'bowl': BOWL, 'ceil': add(BOWL, [0, 1.75, 0])})
knb = [k(0.0, clip='sit'), k(0.0, look=[3.0, 1.0, -1.2]), TK(0.0, {'R': R5(add(BOWL, [-0.2, 0.05, 0.0])), 'L': R5(add(BOWL, [0.2, 0.05, 0.0]))}, {'R': 'grip', 'L': 'grip'}, CALM, d=0.0),
       TK(0.5, {'R': R5(add(BOWL, [-0.05, 0.12, 0.0]))}, {'R': 'pinch'}, d=0.15, keep=True), TK(0.8, {'R': R5(add(NB, [-0.05, 1.45, 0.3]))}, {'R': 'pinch'}, d=0.2, keep=True),
       TK(1.3, {'R': R5(add(BOWL, [-0.2, 0.05, 0.0]))}, {'R': 'grip'}, d=0.2, keep=True), k(1.5, look=BOWL, lookDur=0.12), TK(1.55, face={'lid': 0.0, 'mouth': 'O', 'brow': 0.7}, d=0.06, keep=True), *blink(0.6, CALM)]
st.shot('S12', 'livingRoom', setOpts={'tv': False}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[act('voisin', NB, NRY, 'sit', 'neutral', keys=knb)],
        props=[P('bol12', 'fuBowl', pos=BOWL, opts={'splashAt': 1.45, 'water': [[1.45, 0], [1.6, 0.25]]}), P('goutte12', 'fuDrop', pos=add(BOWL, [0, 1.75, 0]), opts={'s': 0.2, 'fall': [FALL12, 1.47, 1.62], 'once': True}),
               P('tele12', 'tv', pos=[2.2, 0, -1.0], ry=-70, opts={})], cams=[C12])
st.cue(PLIC, 'S12', 1.45, 0.5)

# ================================================================= S13
# 13: two agents walk the handcuffed neighbour out of his flat; he still holds the bowl, now half full of water, out at chest height like evidence
D13 = st.dur('S13')
N0, N1 = [0.0, 0, -1.6], [0.0, 0, 0.3]
C13 = cam(0.0, [0.5, 1.5, 4.4], [0.5, 1.5, 4.2], [0.0, 1.3, -0.4], [0.0, 1.3, -0.2], lens=44)
chk('S13', C13, {'nbFace0': add(N0, [0, 1.95, 0]), 'nbFace1': add(N1, [0, 1.95, 0]), 'a1': add(N1, [-0.75, 2.0, -0.2]), 'a2': add(N1, [0.75, 2.0, -0.2])})
kn13 = [k(0.0, clip='walk'), k(0.0, to=N1, dur=D13, clip='walk', ease='linear', face='keep'), k(0.0, look='camera'),
        TK(0.0, {'R': R5(off(N0, 0, 0.45, 0.08, 1.35)), 'L': R5(off(N0, 0, 0.45, -0.08, 1.35))}, {'R': 'grip', 'L': 'grip'}, SAD, d=0.0),
        TK(D13, {'R': R5(off(N1, 0, 0.45, 0.08, 1.35)), 'L': R5(off(N1, 0, 0.45, -0.08, 1.35))}, d=D13, e='linear', keep=True), *blink(0.7, SAD)]
ag13 = []
for i, sx in enumerate([-1, 1]):
    a, b = add(N0, [sx * 0.75, 0, -0.2]), add(N1, [sx * 0.75, 0, -0.2])
    ks = [k(0.0, clip='walk'), k(0.0, to=b, dur=D13, clip='walk', ease='linear', face='keep'), k(0.0, look='camera'),
          TK(0.0, {('L' if sx < 0 else 'R'): R5(add(a, [-sx * 0.42, 1.3, 0.1])), ('R' if sx < 0 else 'L'): R5(off(a, 0, 0.1, 0.25 if sx < 0 else -0.25, 0.95))}, {'R': 'grip', 'L': 'grip'}, STERN, d=0.0),
          TK(D13, {('L' if sx < 0 else 'R'): R5(add(b, [-sx * 0.42, 1.3, 0.1])), ('R' if sx < 0 else 'L'): R5(off(b, 0, 0.1, 0.25 if sx < 0 else -0.25, 0.95))}, d=D13, e='linear', keep=True)]
    ag13.append(act(f'agent{i + 1}', a, 0, 'walk', 'neutral', keys=ks))
st.shot('S13', 'livingRoom', setOpts={'tv': False}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[act('voisin', N0, 0, 'walk', 'neutral', keys=kn13), *ag13],
        props=[P('bol13', 'fuBowl', on={'actor': 'voisin', 'hand': 'R', 'offset': [-0.08, -0.05, 0.05]}, opts={'water': 0.6}), P('menottes13', 'handcuffs', on={'actor': 'voisin', 'hand': 'L', 'offset': [0.06, 0.02, 0]}, scale=0.45),
               *[x for i in range(1, 3) for x in AGENT('S13', i)]], cams=[C13])
for j in range(3): st.cue('sfx:step', 'S13', r(0.2 + 0.5 * j), 0.2)

# ================================================================= S14
# 14: a black van stops; the plumber in overalls and cap, black shades and an earpiece, steps out with a small toolbox; a slow walk toward the house
D14 = st.dur('S14'); STOP14 = 0.5; OUT14 = 0.85
VAN = [0.6, 0, 2.6]
PL0, PL1 = [0.0, 0, 4.1], [-1.5, 0, 3.4]
C14 = cam(0.0, [-3.6, 1.3, 12.5], [-3.55, 1.3, 12.3], [0.35, 1.25, 2.4], [0.1, 1.25, 2.4], lens=46)
chk('S14', C14, {'plFace0': add(PL0, [0, 1.95, 0]), 'plFace1': add(PL1, [0, 1.95, 0]), 'van': add(VAN, [2.0, 1.2, 1.0]), 'vanR': add(VAN, [-2.5, 1.2, 1.0])})
kpl14 = [k(0.0, clip='stand'), k(0.0, visible=False), k(OUT14, visible=True), k(OUT14, to=PL1, dur=r(D14 - OUT14), clip='walk', ease='linear', face='keep'), k(0.0, look='camera'),
         TK(0.0, {'R': R5(off(PL0, 210, 0.05, 0.28, 0.9)), 'L': R5(off(PL0, 210, 0.1, -0.25, 0.95))}, {'R': 'grip', 'L': 'rest'}, {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}, d=0.0)]
st.shot('S14', 'cottageStreet', look={'sunDir': [0.5, 0.9, 0.7]}, actors=[act('plombier', PL0, 210, 'stand', 'neutral', keys=kpl14)],
        props=[P('van14', 'fuVan', pos=add(VAN, [3.0, 0, 0]), opts={'stopAt': STOP14, 'doorAt': 0.6}, keys=[k(0.0, to=VAN, dur=STOP14, ease='out')]),
               P('caisse14', 'fuToolbox', on={'actor': 'plombier', 'hand': 'R', 'offset': [0, -0.03, 0]}), P('lunettes14', 'shades', on={'actor': 'plombier', 'joint': 'head', 'offset': SHADE}, opts={'s': 1.25}),
               P('casquette14', 'fuCap', on={'actor': 'plombier', 'joint': 'head', 'offset': [0, 0.47, 0.0]})], cams=[C14])
st.cue('sfx:brake', 'S14', 0.25, 0.4); st.cue('sfx:zip', 'S14', 0.6, 0.25)

# ================================================================= S15
# 15: the kitchen, a hole chiselled in the concrete: the plumber holds out on his flat mitten an oversized black washer; a price tag pops beside
#    it with one small coin drawn on it
D15 = st.dur('S15'); TAG15 = r(st.at('S15', 'L15', 5) - 0.05)
PL15 = [0.35, 0, 3.0]; PRY15 = -15
RING = off(PL15, PRY15, 0.48, 0.12, 1.25)
C15 = cam(0.0, [-0.3, 1.65, 5.6], [-0.28, 1.64, 5.4], [0.2, 1.45, 2.2], [0.2, 1.45, 2.2], lens=44)
chk('S15', C15, {'plFace': add(PL15, [0, 1.95, 0]), 'plTop': add(PL15, [0, 2.4, 0]), 'ring': RING, 'tag': add(RING, [-0.45, 0.25, 0]), 'hole': [0.0, 0.9, 2.62]})
kpl15 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(RING), 'L': R5(off(PL15, PRY15, 0.2, -0.25, 1.0))}, {'R': 'open', 'L': 'rest'}, {'lid': 0.35, 'mouth': 'line', 'brow': -0.1}, d=0.0),
         k(r(TAG15 - 0.1), look=add(RING, [-0.4, 0.2, 0]), lookDur=0.12), k(r(TAG15 + 0.4), look='camera', lookDur=0.15), TK(r(TAG15 + 0.4), face=SMUG, d=0.12, keep=True), *blink(0.6, CALM)]
st.shot('S15', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('plombier', PL15, PRY15, 'stand', 'neutral', keys=kpl15)],
        props=[KITCHEN('S15', tap=False), P('beton15', 'fuConcrete', pos=KIT, opts={'fx': -2.1, 'h': 2.65, 'hole': [0.0, 0.9]}),
               P('joint15', 'fuRing', on={'actor': 'plombier', 'hand': 'R', **HAND_FLAT}, opts={'R': 0.1}), P('etiquette15', 'fuTag', pos=add(RING, [-0.52, 0.45, 0.05]), opts={'w': 0.3, 'popAt': TAG15}),
               P('lunettes15', 'shades', on={'actor': 'plombier', 'joint': 'head', 'offset': SHADE}, opts={'s': 1.25}), P('casquette15', 'fuCap', on={'actor': 'plombier', 'joint': 'head', 'offset': [0, 0.47, 0.0]})], cams=[C15])
st.cue('sfx:pop', 'S15', TAG15, 0.4); st.cue('sfx:cash', 'S15', r(TAG15 + 0.1), 0.2)

# ================================================================= S16
# 16: the palace office: the plumber's invoice unrolls off the desk and keeps unrolling across the floor; two agents roll it up and shove it into a
#    big safe, which slams shut
D16 = st.dur('S16'); ROLL16 = 2.0; SLAM16 = 2.75
DESK16 = [-0.6, 0, -1.4]; INV = [-0.6, 0.78, -1.05]; SAFE = [1.0, 0, -1.75]
AG16 = [[-1.0, 0, 0.6], [0.15, 0, -0.35]]
C16 = cam(0.0, [-0.2, 1.75, 5.4], [-0.15, 1.73, 5.2], [-0.05, 0.95, -0.6], [-0.05, 0.95, -0.6], lens=48)
chk('S16', C16, {'desk': add(DESK16, [0, 0.8, 0]), 'invEnd': [-0.6, 0.0, 2.2], 'safe': add(SAFE, [0, 1.4, 0]), **{f'a{i}': add(p, [0, 2.0, 0]) for i, p in enumerate(AG16)}})
ag16 = []
for i, p in enumerate(AG16):
    ry = yaw(p, [-0.6, 0, 0.6])
    pick = [[-0.62, 0.14, 0.45], [-0.5, 0.2, -0.3]][i]   # each picks the paper right by him
    ks = [k(0.0, clip='stand'), k(0.0, look=[-0.6, 0.9, 0.6]), TK(0.0, HANDS(p, ry, 0.15, 0.25, 0.95, 0.15, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, STERN, d=0.0),
          k(1.3, look=pick, lookDur=0.15), TK(1.5, {'R': R5(add(pick, [-0.12, 0.25, 0])), 'L': R5(add(pick, [0.12, 0.25, 0]))}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.9), 'neck': SP(0.2)}, d=0.3, keep=True),
          (TK(ROLL16, {'R': R5(add(SAFE, [-0.12, 1.0, 0.55])), 'L': R5(add(SAFE, [0.12, 1.0, 0.55]))}, bend={'spine': SP(0.2), 'neck': SP(0.0)}, d=0.4, keep=True) if i == 1 else
           TK(ROLL16, {'R': R5(add(pick, [-0.1, 0.35, 0.05])), 'L': R5(add(pick, [0.1, 0.35, 0.05]))}, {'R': 'fist', 'L': 'fist'}, bend={'spine': SP(0.6), 'neck': SP(0.1)}, d=0.3, keep=True)),
          TK(r(SLAM16 + 0.05), HANDS(p, ry, 0.15, 0.25, 0.95, 0.15, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, SMUG, d=0.25, keep=True), k(r(SLAM16 + 0.1), look='camera', lookDur=0.15)]
    ag16.append(act(f'agent{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S16', 'office', setOpts={'door': False, 'printer': False, 'carpet': False, 'picture': False}, look={'sunDir': [0.3, 0.9, 0.9]}, actors=ag16,
        props=[P('bureau16', 'desk', pos=DESK16, opts={'w': 1.5}), P('facture16', 'fuInvoice', pos=INV, opts={'unroll': [[0.1, 0], [1.6, 3.6], [ROLL16, 3.6], [r(ROLL16 + 0.35), 0]], 'len': 4.0, 'drop': 0.78}),
               P('coffre16', 'fuSafe', pos=SAFE, ry=0, opts={'door': [[0, 1]], 'slamAt': SLAM16}), *[x for i in range(1, 3) for x in AGENT('S16', i)]], cams=[C16])
st.cue('sfx:paper', 'S16', 0.2, 0.35); st.cue('sfx:zip', 'S16', ROLL16, 0.3); st.cue('clang', 'S16', SLAM16, 0.6)

# ================================================================= S17
# 17: the kitchen after: the concrete gone, a clean tap; the hero finally rinses his plate and closes the tap; not a drop (silence)
D17 = st.dur('S17'); OFF17 = 1.0
HER17 = [0.25, 0, 0.8]; HRY17 = -125
TAPP = [0.0, 0.945, 0.1]
C17 = fcam(0.0, [-1.5, 1.55, 2.6], {'heroTop': add(HER17, [0, 2.35, 0]), 'heroWaist': add(HER17, [0, 0.9, 0]), 'tap': add(TAPP, [0, 0.32, 0.3]), 'sink': [-0.35, 0.92, 0.33]}, top=0.1, bottom=0.82, margin=0.12, push=0.2)
chk('S17', C17, {'heroTop': add(HER17, [0, 2.3, 0]), 'tap': add(TAPP, [0, 0.3, 0.3]), 'plate': [0.0, 1.05, 0.45]})
k17 = [k(0.0, clip='stand'), k(0.0, look=[0, 0.95, 0.35]), TK(0.0, {'L': R5([0.08, 1.02, 0.42]), 'R': R5([-0.15, 1.0, 0.45])}, {'L': 'grip', 'R': 'open'}, {'lid': 0.4, 'mouth': 'smile', 'brow': 0.2}, bend={'spine': SP(0.3), 'neck': SP(0.3)}, d=0.0),
       *[TK(r(0.12 + 0.14 * j), {'R': R5([-0.15 + 0.1 * (j % 2), 1.0, 0.45])}, d=0.12, keep=True) for j in range(6)],
       TK(OFF17, {'R': R5([0.12, 1.18, 0.12])}, {'R': 'pinch'}, d=0.12, keep=True), TK(r(OFF17 + 0.2), {'R': R5([-0.2, 1.0, 0.5])}, {'R': 'rest'}, bend={'spine': SP(0.1), 'neck': SP(0.0)}, d=0.15, keep=True), k(1.2, look='camera', lookDur=0.15)]
st.shot('S17', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('mec', HER17, HRY17, 'stand', 'neutral', keys=k17)],
        props=[KITCHEN('S17', tap=False), P('robinet17', 'fuTap', pos=TAPP, opts={'flow': [[0.0, OFF17]], 'flowLen': 0.12}), PLATE('S17')], cams=[C17])
st.cue('sfx:pour', 'S17', 0.0, 0.25); st.cue('sfx:squeak', 'S17', OFF17, 0.25)

# ================================================================= S18
# 18: close on the tap, its spout a third of the frame: the hero walks out of frame to the left; the spout slowly swivels to follow him; then a small
#    round grille with a red light blinks on inside the opening; held
D18 = st.dur('S18'); SW18 = [0.55, 1.35]; LIGHT18 = 1.5
H18A, H18B = [1.45, 0, 0.75], [2.2, 0, -0.2]
C18 = fcam(0.0, [-0.5, 1.2, 1.2], {'mouth': [0.0, 1.36, 0.76], 'colTop': [0.0, 1.55, 0.1], 'colBot': [0.0, 0.95, 0.1], 'door': [2.2, 2.0, 0.05], 'doorB': [2.2, 0.9, 0.05]}, top=0.1, bottom=0.8, margin=0.08, push=0.05)   # low under the spout: the grille shows
chk('S18', C18, {'mouth': [0.0, 1.19, 0.42], 'col': [0.0, 1.05, 0.1], 'heroA': add(H18A, [0, 1.95, 0]), 'door': [2.2, 1.6, 0.05]})
k18 = [k(0.0, clip='walk'), k(0.0, to=H18B, dur=1.0, clip='walk', ease='inOut', face='keep'), k(0.0, look='camera'), k(0.95, visible=False)]
st.shot('S18', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('mec', H18A, yaw(H18A, H18B), 'walk', 'neutral', keys=k18)],
        props=[KITCHEN('S18', tap=False, burstAt=-1), P('robinet18', 'fuTap', pos=TAPP, opts={'s': 2.0, 'swivel': [[0.0, -0.7], [SW18[0], -0.7], [SW18[1], 1.45]], 'lightAt': LIGHT18})], cams=[C18])
st.cue('sfx:squeak', 'S18', SW18[0], 0.15); st.cue('sfx:beep', 'S18', LIGHT18, 0.2)

for g_ in [('S01', BURST1, 'mec', 'door'), ('S02', 1.2, 'agent1', 'plic'), ('S03', LOCK3, 'agent3', 'lock'), ('S04', FL2, 'agent1', 'mugshot'),
           ('S05', 1.3, 'agent1', 'morse'), ('S06', OPEN6, 'agent1', 'gate'), ('S07', SHUT7, 'tech', 'lock'), ('S08', 0.6, 'passant1', 'papers'),
           ('S09', 1.0, 'ministre', 'drip'), ('S10', STAMP10, 'president', 'stamp'), ('S11', CUT11, 'soldat1', 'concrete'), ('S12', 1.45, 'voisin', 'plic'),
           ('S13', 0.8, 'voisin', 'evidence'), ('S14', STOP14, 'plombier', 'van'), ('S15', TAG15, 'plombier', 'tag'), ('S16', SLAM16, 'agent1', 'safe'),
           ('S17', OFF17, 'mec', 'tap'), ('S18', LIGHT18, 'mec', 'red')]:
    st.gag(*g_)

# a toon key that names one hand's reach replaces the whole reach (keepPose merges only the top level): carry the other hand's reach and hand
# pose from the previous keys of the same actor so a one-handed gesture never drops the other hand
for _sc in st.scenes:
    for _a in _sc['actors']:
        _run = {'reach': {}, 'hands': {}}
        for _kk in sorted((x for x in _a.get('keys', []) if isinstance(x, dict) and 'toon' in x), key=lambda x: x.get('at', 0)):
            for _n in ('reach', 'hands'):
                if _n in _kk['toon']: _kk['toon'][_n] = {**_run[_n], **_kk['toon'][_n]}; _run[_n] = dict(_kk['toon'][_n])
print('\n'.join(CHECKS))

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'outfit': 'pajamas', 'suit': '#9FB8D8', 'pants': '#9FB8D8', 'shirt': '#C9D8EA', 'lapel': '#86A2C6', 'tie': '#9FB8D8', 'cuff': '#C9D8EA',
       'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
AG = {'outfit': 'suit', 'suit': '#1C1E22', 'pants': '#1C1E22', 'lapel': '#14161A', 'tie': '#14161A', 'shirt': '#F2F2EE', 'cuff': '#1C1E22', 'hat': 'none', 'glasses': False, 'facial': 'none', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
SOLDIER = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'hair': 'crew', 'hairColor': '#3A3028', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("La fuite", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'agent1': {**AG, 'preset': 'cop', 'seed': 991, 'hair': 'crew', 'hairColor': '#2A2420'}, 'agent2': {**AG, 'preset': 'cop2', 'seed': 992, 'hair': 'bald'}, 'agent3': {**AG, 'preset': 'swat', 'seed': 993, 'hair': 'slick', 'hairColor': '#17161A'},
    'tech': {'preset': 'savant', 'seed': 994, 'outfit': 'suit', 'suit': '#5A6A7A', 'lapel': '#4A5A6A', 'tie': '#2E3A46', 'hat': 'none', 'hair': 'spiky', 'hairColor': '#3A2A20', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'passant1': {'preset': 'madame', 'seed': 995, 'hat': 'none', 'suit': '#2E7D4F', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'passant2': {'preset': 'worker', 'seed': 996, 'hat': 'none', 'suit': '#1F4E8C', 'pants': '#22324A', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 997, 'hat': 'none', 'suit': '#4A4F58', 'lapel': '#3C414A', 'tie': '#7A2E2E', 'shirt': '#E8ECF0', 'hairColor': '#8A8A86', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'prefet', 'seed': 998, 'hat': 'none', 'suit': '#2B3A55', 'lapel': '#22304A', 'tie': '#3C66B0', 'facial': 'none', 'hairColor': '#BDBDBD', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'aide': {'preset': 'journaliste', 'seed': 999, 'hat': 'none', 'suit': '#5A5F6A', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'soldat1': {**SOLDIER, 'preset': 'cop', 'seed': 1001}, 'soldat2': {**SOLDIER, 'preset': 'cop2', 'seed': 1002, 'hair': 'bald'},
    'voisin': {'preset': 'pyjama', 'seed': 1003, 'hat': 'none', 'suit': '#C9A86A', 'pants': '#7A6A4A', 'hair': 'receding', 'hairColor': '#6A5A4A', 'facial': 'mustache', 'glasses': False, 'build': {'width': 1.1, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'plombier': {'preset': 'worker', 'seed': 1004, 'outfit': 'worker', 'suit': '#2E4563', 'pants': '#2E4563', 'hat': 'none', 'hair': 'crew', 'hairColor': '#2A2420', 'facial': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
