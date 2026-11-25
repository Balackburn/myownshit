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
def PLATEW(sid, p, ry, rr=0.24):
    c = off(p, ry, 0.5, -0.34, 1.2); return P(f'assiette{sid}', 'fuPlate', pos=c, rot=[1.15, math.radians(ry), 0], rotOrder='YXZ', opts={'r': rr}), add(c, [0, -0.2, 0.09])   # face-on, tilted up to us; (prop, where his hand grips it)
PLATE = lambda sid, actor='mec', hand='L', rr=0.24: P(f'assiette{sid}', 'fuPlate', on={'actor': actor, 'hand': hand, 'offset': [0, -0.04, 0.16], 'rot': [1.2, 0, 0]}, opts={'r': rr})   # a big dirty plate, held up in front
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
AG1 = [([2.2, 0, 0.3], [2.1, 0, 1.0]), ([2.35, 0, 0.0], [2.8, 0, 1.4]), ([2.05, 0, -0.2], [2.4, 0, 1.95])]
PL1W, GRIP1 = PLATEW('S01', HER1, HRY1)
C1 = fcam(0.0, [0.9, 1.0, 4.4], {'heroTop': add(HER1, [0, 2.3, 0]), 'heroKnee': add(HER1, [0, 0.45, 0]), 'leftRoom': add(HER1, [-0.6, 1.2, 0.2]), 'plate': GRIP1, 'agTop': add(AG1[1][1], [0, 2.35, 0]), 'door': [2.2, 2.1, 0.0], 'ag3': add(AG1[2][1], [0, 2.35, 0]), 'ag3b': add(AG1[1][1], [0, 0.45, 0])}, top=0.1, bottom=0.8, margin=0.08, push=0.25)   # low
chk('S01', C1, {'heroFace': add(HER1, [0, 1.95, 0]), 'phone': [1.25, 1.5, 0.05], 'ag1': add(AG1[0][1], [0, 2.0, 0]), 'ag2': add(AG1[1][1], [0, 2.0, 0]), 'ag3': add(AG1[2][1], [0, 2.0, 0])})
k1 = [k(0.0, clip='stand'), k(0.0, look=[1.25, 1.55, 0.05]), TK(0.0, {'R': R5(off(HER1, HRY1, 0.15, 0.22, 1.95)), 'L': R5(GRIP1)}, {'R': 'grip', 'L': 'grip'}, CALM, bend={'neck': SP(0.0, -0.2)}, d=0.0),
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
        props=[KITCHEN('S01', burstAt=BURST1, handsetFrom=HANG1), PL1W, P('combine1', 'fuHandset', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.04, 0.03]}, keys=[k(0.0, visible=True), k(HANG1, visible=False)]),
               *[x for i in range(1, 4) for x in AGENT('S01', i)]], cams=[C1])
st.cue('clack', 'S01', HANG1, 0.3); st.cue('thud', 'S01', BURST1, 0.5); st.cue('whoosh', 'S01', r(BURST1 + 0.02), 0.25, 0.12, 300, 2000)

# ================================================================= S02
# 2: close on the open cupboard under the sink: one fat bright drop swells on the pipe and falls into a small saucepan, plic; three agents crouch
#    round it in a row, shades on, staring
D2 = st.dur('S02'); FALL2 = 0.15
PAN = [0.0, 0.08, 0.33]
AG2 = [[-0.6, 0, 1.0], [0.6, 0, 1.0], [0.95, 0, 1.75]]
C2 = cam(0.0, [0.0, 1.2, 3.3], [0.0, 1.18, 3.1], [0.0, 0.62, 0.33], [0.0, 0.62, 0.33], lens=60)
chk('S02', C2, {'drop': DRIP, 'pan': PAN, **{f'face{i}': add(p, [0, 1.25, 0]) for i, p in enumerate(AG2)}})
agents2 = []
for i, p in enumerate(AG2):
    ry = yaw(p, [0, 0, 0.33])
    ks = [k(0.0, clip='kneel'), k(0.0, look=add(DRIP, [0, 0.3, 0.1])), TK(0.0, HANDS(p, ry, 0.3, 0.2, 0.55, 0.3, -0.2, 0.55), {'R': 'rest', 'L': 'rest'}, STERN, bend={'spine': SP(0.25), 'neck': SP(0.0)}, d=0.0),
          TK(r(0.85 + 0.03 * i), bend={'spine': SP(0.42), 'neck': SP(0.0)}, face={**STERN, 'brow': -0.9, 'lid': 0.1}, sq=(0.97, 1.05, 0.97), d=0.1, keep=True), TK(r(1.12 + 0.03 * i), face=STERN, sq=(1, 1, 1), d=0.12, keep=True), k(r(FALL2 + 0.45), look=add(DRIP, [0, -0.05, 0]), lookDur=0.15), k(r(FALL2 + 0.82), look=PAN, lookDur=0.08), *blink(r(FALL2 + 0.92 + 0.03 * i), STERN)]
    agents2.append(act(f'agent{i + 1}', p, ry, 'kneel', 'neutral', keys=ks))
st.shot('S02', 'whiteVoid', setOpts=KV, look=LOOKK, actors=agents2,
        props=[KITCHEN('S02', doors=1), P('casserole2', 'fuPan', pos=PAN), P('goutte2', 'fuDrop', pos=add(DRIP, [0, -0.03, 0]), opts={'s': 0.42, 'fall': [FALL2, 1.2, 0.2], 'once': True}),
               *[x for i in range(1, 4) for x in AGENT('S02', i)]], cams=[C2])
st.cue(PLIC, 'S02', r(FALL2 + 0.9), 0.45)

# ================================================================= S03
# 3: wider: two agents wind black-and-yellow tape round the sink, a third snaps a giant padlock on the cupboard doors; the hero in the doorway with
#    his plate
D3 = st.dur('S03'); TAPE3, LOCK3 = 0.35, r(st.at('S03', 'L03', 7) - 0.15)
HER3 = [1.25, 0, 1.8]; HRY3 = -30
PL3W, GRIP3 = PLATEW('S03', HER3, HRY3)
AG3 = [[-0.9, 0, 0.72], [0.9, 0, 0.72], [0.3, 0, 1.2]]
C3 = fcam(0.0, [-0.35, 1.3, 4.9], {'heroTop': add(HER3, [0, 2.3, 0]), 'heroKnee': add(HER3, [0, 0.55, 0]), 'tapeL': [-1.1, 0.4, 0.66], 'tapeR': [1.1, 0.4, 0.66], 'aTop': add(AG3[0], [0, 2.35, 0]), 'lock': [0, 0.45, 0.72]}, top=0.1, bottom=0.8, margin=0.06, push=0.2)
chk('S03', C3, {'heroFace': add(HER3, [0, 1.95, 0]), 'lock': [0, 0.62, 0.72], **{f'a{i}': add(p, [0, 2.0, 0]) for i, p in enumerate(AG3)}})
k3 = [k(0.0, clip='stand'), k(0.0, look=[0, 0.8, 0.6]), TK(0.0, {'R': R5(off(HER3, HRY3, 0.15, 0.28, 0.95)), 'L': R5(GRIP3)}, {'R': 'rest', 'L': 'grip'}, WORRY, d=0.0),
      TK(r(LOCK3 + 0.02), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, sq=(1.04, 0.96, 1.04), d=0.04, keep=True), TK(r(LOCK3 + 0.2), face=WORRY, sq=(1, 1, 1), d=0.12, keep=True),
      k(r(LOCK3 + 0.5), look='camera', lookDur=0.2), *blink(0.8, WORRY), *blink(2.4, WORRY), *BREATHE(0.1, D3, 0.5, 0.012)]
agents3 = []
for i, p in enumerate(AG3):
    ry = 180 + [20, -20, 25][i]
    if i < 2:
        sx = [-1, 1][i]
        ks = [k(0.0, clip='stand'), k(0.0, look=[0, 0.8, 0.6]), TK(0.0, {'R': R5([sx * 0.75 - 0.12, 0.7, 0.7]), 'L': R5([sx * 0.75 + 0.12, 0.62, 0.7])}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.25)}, d=0.0),
              *[TK(r(TAPE3 + 0.25 * j), {'R': R5([sx * (0.75 - 0.08 * (j % 2)) - 0.12, 0.72 - 0.25 * (j % 2), 0.72]), 'L': R5([sx * (0.75 - 0.08 * (j % 2)) + 0.12, 0.64 - 0.25 * (j % 2), 0.72])}, d=0.22, keep=True) for j in range(4)]]   # winding the tape ends
    else:
        ks = [k(0.0, clip='stand'), k(0.0, look=[0, 0.6, 0.7]), TK(0.0, {'R': R5([-0.15, 0.95, 0.85]), 'L': R5([0.15, 0.95, 0.85])}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.35)}, d=0.0),
              TK(r(LOCK3 - 0.15), {'R': R5([-0.1, 0.7, 0.8]), 'L': R5([0.1, 0.7, 0.8])}, d=0.15, keep=True), TK(LOCK3, {'R': R5([-0.1, 0.62, 0.78]), 'L': R5([0.1, 0.62, 0.78])}, {'R': 'open', 'L': 'open'}, sq=(1.04, 0.95, 1.04), d=0.05, keep=True),
              TK(r(LOCK3 + 0.25), {'R': R5(off(p, ry, 0.2, 0.25, 1.0)), 'L': R5(off(p, ry, 0.2, -0.25, 1.0))}, {'R': 'rest', 'L': 'rest'}, sq=(1, 1, 1), d=0.2, keep=True), k(r(LOCK3 + 0.3), look='camera', lookDur=0.15)]
    ks += [*blink(r(0.9 + 0.35 * i), STERN), *blink(r(2.2 + 0.2 * i), STERN), *BREATHE(r(0.05 + 0.1 * i), D3, 0.6, 0.012)] + ([k(r(2.0 + 0.3 * i), look='camera', lookDur=0.2)] if i < 2 else [])
    agents3.append(act(f'agent{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S03', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('mec', HER3, HRY3, 'stand', 'neutral', keys=k3), *agents3],
        props=[KITCHEN('S03', tape=TAPE3, burstAt=-1), P('cadenas3', 'fuPadlock', pos=[0, 0.62, 0.74], opts={'w': 0.5, 'open': True, 'shutAt': LOCK3}, keys=[k(0.0, visible=False), k(r(LOCK3 - 0.2), visible=True)]),
               PL3W, *[x for i in range(1, 4) for x in AGENT('S03', i)]], cams=[C3])
st.cue('sfx:zip', 'S03', TAPE3, 0.3); st.cue('clang', 'S03', LOCK3, 0.45)

# ================================================================= S04
# 4: the mugshot: one big drop stands against a height chart, holding a blank plate, front view then side view, a flash each time; the agent
#    beside it does a double take at the second flash
D4 = st.dur('S04'); FL1, FL2 = 0.15, 0.85
DR4 = [0.12, 1.12, 0.0]; PLQ = [0.12, 0.68, 0.2]
AG4 = [-0.62, 0, 0.3]; AGR4 = 20
C4 = fcam(0.0, [-0.12, 1.25, 3.0], {'dropTop': add(DR4, [0, 0.32, 0]), 'plateB': add(PLQ, [0, -0.14, 0]), 'agTop': add(AG4, [0, 2.4, 0]), 'agChest': add(AG4, [0.2, 1.2, 0]), 'chartR': [0.75, 1.5, -0.35]}, top=0.1, bottom=0.72, margin=0.06, push=0.12)
chk('S04', C4, {'dropTop': add(DR4, [0, 0.3, 0]), 'plate': PLQ, 'plateB': add(PLQ, [0, -0.14, 0]), 'agFace': add(AG4, [0, 1.95, 0])})
kag4 = [k(0.0, clip='stand'), k(0.0, look=DR4), TK(0.0, HANDS(AG4, AGR4, 0.1, 0.25, 0.95, 0.1, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, STERN, d=0.0),
        k(0.3, clip='doubleTakeToon', params={'side': -1, 'beat': 0.22, 'pop': 0.9, 'jaw': 0.5}, blend=0.05), *blink(0.12, STERN)]
st.shot('S04', 'whiteVoid', setOpts={'color': '#B9C4CC'}, look={'sunDir': [0.1, 0.8, 1.0]}, actors=[act('agent1', AG4, AGR4, 'stand', 'neutral', keys=kag4)],
        props=[P('toise4', 'fuChart', pos=[0, 0, -0.35], opts={'w': 2.4}),
               P('goutte4', 'fuDrop', pos=DR4, ry=0, opts={'s': 0.75, 'eyes': True}, keys=[k(r(FL2 - 0.04), rotTo=[0, 1.45, 0], dur=0.06)]),
               P('plaque4', 'mugshotPlate', pos=PLQ, opts={'lines': [' ', ' '], 'w': 0.5, 'h': 0.28}),
               P('flash4', 'camFlash', pos=[0.45, 1.5, 1.0], opts={'at': [FL1, FL2], 'w': 0.6}), *AGENT('S04', 1)], cams=[C4])
st.cue('sfx:shutter', 'S04', FL1, 0.45); st.cue('sfx:shutter', 'S04', FL2, 0.45); st.cue('whoosh', 'S04', 0.86, 0.2)

# ================================================================= S05
# 5: close insert on the morse printer: a fat paper strip feeds out with thick dots and dashes; then a pull back to the agent in big headphones
#    kneeling beside the cupboard, a boom microphone held right under the drip: the drop lands on it, plic
D5 = st.dur('S05'); PULL5 = 0.85; FALL5 = 0.55
MOR = [-1.7, 0.0, 0.45]
AG5, AGR5 = [-0.6, 0, 1.2], 115
HB5 = off(AG5, AGR5, 0.42, 0.18, 0.78); MIC5 = [0.04, 0.12, 0.36]
C5 = cam(0.0, add(MOR, [0.0, 0.95, 1.3]), add(MOR, [0.0, 0.92, 1.24]), add(MOR, [0.0, 0.12, 0.42]), add(MOR, [0.0, 0.12, 0.42]), lens=44)   # the printer up top, its strip feeding down the frame
C5b = (fcam(PULL5, [0.75, 1.1, 3.3], {'agTop': add(AG5, [0, 2.0, 0]), 'agFace': add(AG5, [0, 1.25, 0]), 'drip': DRIP, 'mic': MIC5, 'morse': add(MOR, [0, 0.25, 0]), 'pan': [0, 0.06, 0.33]}, top=0.12, bottom=0.74, margin=0.06, push=0.15))   # a straight cut
chk('S05', C5, {'box': add(MOR, [0, 0.2, 0]), 'stripA': add(MOR, [0, 0.15, 0.3]), 'stripB': add(MOR, [0, 0.15, 0.9])})
chk('S05b', C5b, {'agFace': add(AG5, [0, 1.25, 0]), 'agTop': add(AG5, [0, 1.75, 0]), 'drip': DRIP, 'mic': MIC5})
kag5 = [k(0.0, clip='kneel'), k(0.0, look=DRIP), TK(0.0, {'R': R5(HB5), 'L': R5(lerp3(HB5, MIC5, 0.28))}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.15)}, d=0.0),
        TK(r(FALL5 + 0.78), face={**STERN, 'brow': -0.9, 'lid': 0.05}, sq=(0.96, 1.06, 0.96), d=0.06, keep=True), TK(r(FALL5 + 0.95), face=STERN, sq=(1, 1, 1), d=0.12, keep=True),
        k(1.45, look='camera', lookDur=0.15), *blink(0.95, STERN)]
st.shot('S05', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('agent1', AG5, AGR5, 'kneel', 'neutral', keys=kag5)],
        props=[KITCHEN('S05', doors=1), P('morse5', 'fuMorse', pos=MOR, ry=0, opts={'s': 1.3, 'feed': [0.0, 2.6]}), P('goutte5', 'fuDrop', pos=DRIP, opts={'s': 0.26, 'fall': [FALL5, 1.0, 0.2], 'once': True}),
               P('casque5', 'fuPhones', on={'actor': 'agent1', 'joint': 'head'}), P('perche5', 'fuBoom', pos=HB5, opts={'b': [r(MIC5[i] - HB5[i]) for i in range(3)], 's': 1.5}),
               P('casserole5', 'fuPan', pos=[0, 0.08, 0.33]), *AGENT('S05', 1)], cams=[C5, C5b])
st.cue('sfx:ticks', 'S05', 0.05, 0.3); st.cue(PLIC, 'S05', r(FALL5 + 0.75), 0.45)

# ================================================================= S06
# 6: the palace in one shot: a generic front, the fence and gate before it, a giant padlock on the gate pops open with a clunk
D6 = st.dur('S06'); OPEN6 = r(st.at('S06', 'L06', 4) - 0.05)
PAL = [0, 0, -9.0]; GATE = add(PAL, [0, 1.25, 7.2])
C6 = cam(0.0, [1.2, 0.9, 6.5], [1.0, 0.95, 5.8], [0.0, 3.0, -6.0], [0.0, 3.0, -6.0], lens=48)
chk('S06', C6, {'lock': GATE, 'palTop': add(PAL, [0, 8.1, 1.0]), 'palL': add(PAL, [-7, 3, 0]), 'gateFoot': add(PAL, [0, 0, 7.0])})
st.shot('S06', 'grassland', look={'sunDir': [0.5, 0.9, 0.8]}, actors=[],
        props=[P('palais6', 'fuPalace', pos=PAL, opts={'gateAt': r(OPEN6 + 0.5)}), P('cadenas6', 'fuPadlock', pos=GATE, opts={'w': 0.9, 'openAt': OPEN6, 'shiverAt': r(max(0.1, OPEN6 - 0.7))}),
               P('cour6', 'parkLot', pos=add(PAL, [0, 0, 5]), opts={'w': 18, 'd': 10, 'color': '#D8D0BE'})], cams=[C6])
st.cue('sfx:rattle', 'S06', r(max(0.1, OPEN6 - 0.6)), 0.15); st.cue('clang', 'S06', OPEN6, 0.5); st.cue('sfx:rattle', 'S06', r(OPEN6 + 0.5), 0.3)

# ================================================================= S07
# 7: the palace office: a technician types, the padlock on his screen snaps shut green; a snap cut to the kitchen pipe: one more drop, plic, and
#    the agent in headphones writes it down
D7 = st.dur('S07'); SHUT7 = r(st.at('S07', 'L07', 3) + 0.05); CUT7 = r(st.at('S07', 'L07', 4) - 0.03)
OFF = [30.0, 0, 0.0]
TEC = add(OFF, [0.0, 0, 0.85]); TRY = 160
SCR = add(OFF, [0.0, 0.76, 0.0])
C7 = fcam(0.0, [r(OFF[0] + 1.8), 1.7, 2.6], {'scrTL': add(SCR, [-0.55, 0.95, 0]), 'scrBR': add(SCR, [0.55, 0.25, 0]), 'tecTop': add(TEC, [0, 2.75, 0]), 'tecFace': add(TEC, [0, 1.95, 0]), 'tecBack': add(TEC, [0.25, 1.95, 0.3]), 'kb': add(SCR, [0, 0.0, 0.6])}, top=0.12, bottom=0.78, margin=0.16, push=0.15)   # from the side: the screen and his face
AGM7, AGRY7 = [0.5, 0, 1.15], -110   # turned toward the side camera, 3/4
PAD7 = off(AGM7, AGRY7, 0.42, 0.02, 0.85)
C7b = fcam(CUT7, [-1.7, 1.2, 2.8], {'agTop': add(AGM7, [0, 2.0, 0]), 'agFace': add(AGM7, [0, 1.25, 0]), 'drip': DRIP, 'pan': [0, 0.04, 0.33], 'pad': PAD7}, top=0.12, bottom=0.76, margin=0.1, push=0.1)
chk('S07', C7, {'screen': add(SCR, [0, 0.6, 0]), 'tecFace': add(TEC, [0, 1.95, 0]), 'kb': add(SCR, [0, 0.05, 0.45])})
chk('S07b', C7b, {'agFace': add(AGM7, [0, 1.25, 0]), 'drip': DRIP, 'pad': PAD7, 'pan': [0, 0.08, 0.33]})
ktec = [k(0.0, clip='stand'), k(0.0, look=add(SCR, [0, 0.95, 0])), TK(0.0, {'R': R5(add(SCR, [-0.15, 0.06, 0.45])), 'L': R5(add(SCR, [0.15, 0.06, 0.45]))}, {'R': 'point', 'L': 'point'}, CALM, bend={'spine': SP(0.3), 'neck': SP(0.0)}, d=0.0),
        *[TK(r(0.08 * j), {'R': R5(add(SCR, [-0.15 + 0.04 * (j % 3), 0.04 + 0.03 * (j % 2), 0.45])), 'L': R5(add(SCR, [0.15 - 0.04 * (j % 2), 0.04 + 0.03 * ((j + 1) % 2), 0.45]))}, d=0.07, keep=True) for j in range(7)],
        TK(SHUT7, face=SMUG, sq=(0.97, 1.04, 0.97), bend={'spine': SP(0.0)}, d=0.1, keep=True), k(r(SHUT7 + 0.1), look='camera', lookDur=0.15)]
FALL7 = r(CUT7 + 0.0); HIT7 = r(FALL7 + 0.6)
EAR7 = off(AGM7, AGRY7, 0.02, 0.2, 1.42)
kag7 = [k(0.0, clip='kneel'), k(0.0, look=DRIP), TK(0.0, {'R': R5(off(AGM7, AGRY7, 0.4, 0.15, 0.8)), 'L': R5(PAD7)}, {'R': 'pinch', 'L': 'grip'}, STERN, bend={'spine': SP(0.15)}, d=0.0),
        k(r(HIT7 - 0.3), look=[0, 0.35, 0.33], lookDur=0.12),
        TK(r(HIT7 + 0.02), {'R': R5(EAR7)}, {'R': 'open'}, {**STERN, 'brow': 0.9, 'lid': 0.0, 'mouth': 'O'}, sq=(0.94, 1.08, 0.94), d=0.07, e='out', keep=True),   # startled: a hand to the earphone
        TK(r(HIT7 + 0.3), face={**STERN, 'brow': -1.0, 'lid': 0.05}, sq=(1, 1, 1), d=0.1, keep=True), k(r(HIT7 + 0.3), look=PAD7, lookDur=0.1),
        *[TK(r(HIT7 + 0.38 + 0.06 * j), {'R': R5(add(PAD7, [0.08 * (j % 2) - 0.04, 0.05 - 0.01 * j, 0.03]))}, {'R': 'pinch'}, d=0.05, keep=True) for j in range(11)], k(r(HIT7 + 1.1), look='camera', lookDur=0.12)]   # a frantic scribble
st.shot('S07', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('tech', TEC, TRY, 'stand', 'neutral', keys=ktec), act('agent1', AGM7, AGRY7, 'kneel', 'neutral', keys=kag7)],
        props=[KITCHEN('S07', doors=1), P('mur7', 'fuChart', pos=add(OFF, [0, 0, -1.0]), opts={'w': 0.01}), P('bureau7', 'desk', pos=add(OFF, [0, 0, 0.1]), opts={'w': 1.6}),
               P('ecran7', 'fuScreen', pos=SCR, opts={'shutAt': SHUT7, 'keys': [0.05, 0.13, 0.21, 0.3, 0.38, 0.46]}),
               P('goutte7', 'fuDrop', pos=DRIP, opts={'s': 0.3, 'fall': [FALL7, 0.8, 0.36], 'once': True}), P('casque7', 'fuPhones', on={'actor': 'agent1', 'joint': 'head'}),
               P('bloc7', 'clipboardProp', on={'actor': 'agent1', 'hand': 'L', 'offset': [0, -0.02, 0.08], 'rot': [0, 0, 0]}, scale=1.3), P('casserole7', 'fuPan', pos=[0, 0.08, 0.33]), *AGENT('S07', 1)], cams=[C7, C7b])
st.cue('sfx:ticks', 'S07', 0.05, 0.3); st.cue('sfx:beep', 'S07', SHUT7, 0.35); st.cue(PLIC, 'S07', HIT7, 0.45); st.cue('sfx:paper', 'S07', r(HIT7 + 0.3), 0.2)

# ================================================================= S08
# 8: a newsstand in the street: every paper has the same front page, a huge photo of one drop; two passers-by walk in, stop, look down at the
#    papers, look away, then snap back: a double take; FUITE
D8 = st.dur('S08'); CARD8 = st.at('S08', 'L08', 7)
KIO = [0.0, 0, -1.6]
PB = [([-1.7, 0, 1.6], [-0.85, 0, 1.3], 25), ([1.8, 0, 1.4], [0.9, 0, 1.15], -30)]
C8 = fcam(0.0, [0.2, 1.4, 5.2], {'kioskTop': add(KIO, [0, 2.5, 0]), 'kioskL': add(KIO, [-1.35, 0.8, 0]), 'kioskR': add(KIO, [1.35, 0.8, 0]), 'p1': add(PB[0][1], [0, 2.3, 0]), 'p2': add(PB[1][1], [0, 2.3, 0])}, top=0.22, bottom=0.84, margin=0.13, push=0.25)
chk('S08', C8, {'paper': add(KIO, [0, 1.75, 0.05]), 'p1Face': add(PB[0][1], [0, 1.95, 0]), 'p2Face': add(PB[1][1], [0, 1.95, 0])})
pass8 = []
for i, (a, b, ry) in enumerate(PB):
    stop = r(0.55 + 0.1 * i); down = add(KIO, [0, 1.2, 0.3]) if i == 0 else off(b, ry, 0.45, 0.2, 1.15)
    tk = r(1.25 + 0.2 * i)
    ks = [k(0.0, clip='walk'), k(0.0, to=b, dur=stop, clip='walk', ease='out', face='keep'), k(stop, clip='stand', blend=0.15), k(0.0, look='camera'),
          TK(0.0, HANDS(a, ry, 0.15, 0.25, 0.95, 0.15, -0.25, 0.95) if i == 0 else {'L': R5(off(a, ry, 0.15, -0.25, 0.95))}, {'R': 'rest', 'L': 'rest'}, CALM, d=0.0),
          TK(stop, HANDS(b, ry, 0.15, 0.25, 0.95, 0.15, -0.25, 0.95) if i == 0 else {'L': R5(off(b, ry, 0.15, -0.25, 0.95))}, d=0.15, keep=True),
          k(r(stop + 0.05), look=down, lookDur=0.15), k(r(tk - 0.35), look='camera', lookDur=0.2),   # a look down, a look away...
          k(tk, look=down, lookDur=0.05), TK(tk, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(0.93, 1.1, 0.93), scl={'head': [1.15, 0.9, 1]}, d=0.05, e='out', keep=True),   # ...and the snap back
          TK(r(tk + 0.12), sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.12, keep=True), k(r(D8 - 0.5), look='camera', lookDur=0.2), *blink(r(stop + 0.3), CALM)]
    pass8.append(act(f'passant{i + 1}', a, ry, 'walk', 'neutral', keys=ks))
st.shot('S08', 'street', look={'sunDir': [0.5, 0.9, 0.7]}, actors=pass8,
        props=[P('kiosque8', 'fuKiosk', pos=KIO), P('journal8', 'fuPaper', on={'actor': 'passant2', 'hand': 'R', 'offset': [0, 0.12, 0.08]}, opts={'w': 0.42})], cams=[C8])
st.card('S08', 'FUITE', at=CARD8)
st.cue('sfx:step', 'S08', 0.15, 0.2); st.cue('sfx:paper', 'S08', 0.6, 0.3); st.cue('whoosh', 'S08', 1.25, 0.15)

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
km9 += [*blink(2.4, SAD), TK(0.3, face={**SAD, 'lid': 0.9}, sq=(1.12, 0.86, 1.12), d=0.05, e='out', keep=True), TK(0.7, sq=(1.25, 0.72, 1.25), d=0.05, e='out', keep=True),
        TK(1.1, face={'lid': 0.9, 'mouth': 'line', 'brow': 0.7}, sq=(1.42, 0.56, 1.42), d=0.05, e='out', keep=True), TK(1.75, face={'lid': 0.6, 'mouth': 'line', 'brow': 0.5}, sq=(0.95, 1.06, 0.95), d=0.1, e='out', keep=True), TK(1.95, face=SAD, sq=(1.02, 0.98, 1.02), d=0.1, keep=True), TK(2.1, sq=(1, 1, 1), d=0.1, keep=True),
        k(1.75, look=[-1.5, 1.6, 6.0], lookDur=0.05), k(1.83, look=[1.5, 1.6, 6.0], lookDur=0.05), k(1.91, look=[-1.2, 1.6, 6.0], lookDur=0.05), k(1.99, look='camera', lookDur=0.06)]   # shakes his head clear   # squashed flatter by each flash, then he puffs back up
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
        TK(r(STAMP10 - 0.05), bend={'armR': [0, 0, 0, 1.35, None], 'foreR': [0, 0, 0, 1.7, 0.7]}, d=0.04, keep=True),
        TK(STAMP10, {'R': R5(add(DEC, [0.02, 0.0, 0.2]))}, {'R': 'grip'}, {**STERN, 'lid': 0.1, 'mouth': 'clench'}, sq=(1.05, 0.94, 1.05), bend={'armR': [0, 0, 0, 1, None], 'foreR': [0, 0, 0, 1, None]}, d=0.06, e='out', keep=True),
        TK(r(STAMP10 + 0.3), {'R': R5(add(DEC, [-0.05, 0.45, 0.2]))}, face=SMUG, sq=(1, 1, 1), d=0.2, keep=True), k(r(STAMP10 + 0.35), look='camera', lookDur=0.2), *blink(0.5, STERN)]
ka10 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(add(DEC, [-0.27, 0.0, -0.02])), 'L': R5(add(DEC, [0.27, 0.0, -0.02]))}, {'R': 'grip', 'L': 'grip'}, CALM, d=0.0),
        TK(STAMP10, face={'lid': 1.0, 'mouth': 'line', 'brow': 0.4}, sq=(1.02, 0.97, 1.02), d=0.04, keep=True), TK(r(STAMP10 + 0.15), face=CALM, sq=(1, 1, 1), d=0.1, keep=True), *blink(1.6, CALM)]
st.shot('S10', 'office', setOpts={'door': False, 'printer': False, 'carpet': False, 'picture': False}, look={'sunDir': [0.3, 0.9, 0.9]},
        actors=[act('president', PRES, PRY, 'stand', 'neutral', keys=kp10), act('aide', AIDE, ARY, 'stand', 'neutral', keys=ka10)],
        props=[P('decret10', 'fuDecree', on={'actor': 'aide', 'hand': 'R', 'offset': [0.27, 0.0, 0.02], 'rot': [1.5708, 0, 0]}, opts={'w': 0.5, 'stampAt': r(STAMP10 + 0.02)}),
               P('tampon10', 'fuStamp', on={'actor': 'president', 'hand': 'R', 'offset': [0, -0.02, 0.0]}, opts={'s': 1.3, 'hitAt': STAMP10}), P('tableau10', 'fuSinkBoard', pos=[0.05, 0, -2.75], opts={'w': 0.9, 'y0': 1.85})], cams=[C10])
st.cue('thud', 'S10', STAMP10, 0.5)

# ================================================================= S11
# 11: outside his house: the mixer's drum and chute high in the frame, a fat grey ribbon of concrete falls on a gravity arc into the kitchen
#    window and splashes on the sill; a soldier at the side waves it on; a cut to the result seen from high in the kitchen: a lumpy grey block
#    swelling up to the wall cupboards, a big white fridge sticking out of it askew, a big apple magnet on it; a last dollop plops beside it; the
#    magnet creeps down and drops off
D11 = st.dur('S11'); CUT11 = 1.43; CARD11 = r(CUT11 + 0.05)
MIX = [2.6, 0, -0.4]; MRY = -40
WIN11 = [-1.74, 1.15, -4.02]
LIP11 = [-0.85, 2.55, -3.05]; SPL11 = [-1.74, 0.72, -3.82]; CH11 = [0.55, 2.95, -2.1]
SOL = [[-3.0, 0, -3.3], [1.0, 0, -2.5]]
KIT11 = [60.0, 0, 0.0]; FX11, FZ11 = -0.6, 1.7
C11 = fcam(0.0, [-2.6, 1.15, 0.9], {'drumTop': [1.2, 3.25, -1.3], 'chute': CH11, 'lip': LIP11, 'winBL': add(WIN11, [-0.65, -0.62, 0]), 'winBR': add(WIN11, [0.65, -0.62, 0]), 's0': add(SOL[0], [0, 2.35, 0]), 's0k': add(SOL[0], [0, 0.7, 0])}, top=0.06, bottom=0.78, margin=0.06, push=0.2)
C11b = fcam(CUT11, add(KIT11, [FX11 + 0.9, 4.4, 4.3]), {'fridgeTop': add(KIT11, [FX11 - 0.35, 3.65, FZ11]), 'fridgeBase': add(KIT11, [FX11 + 0.3, 2.1, FZ11 + 0.45]), 'cupL': add(KIT11, [FX11 - 1.0, 3.15, 0.2]), 'cupR': add(KIT11, [FX11 + 1.1, 3.15, 0.2]),
          'blkL': add(KIT11, [FX11 - 0.9, 2.2, 2.6]), 'blkR': add(KIT11, [FX11 + 1.1, 2.2, 2.6])}, top=0.12, bottom=0.78, margin=0.04, push=0.25)
chk('S11', C11, {'lip': LIP11, 'splash': SPL11, 's0': add(SOL[0], [0, 2.0, 0]), 'drum': [1.2, 3.0, -1.3]})
chk('S11b', C11b, {'fridgeTop': add(KIT11, [FX11 - 0.35, 3.65, FZ11]), 'fridgeBase': add(KIT11, [FX11, 2.1, FZ11 + 0.4]), 'plop': add(KIT11, [FX11 + 0.85, 2.3, FZ11 + 0.6])})
ks1 = [k(0.0, clip='stand'), k(0.0, look=WIN11), TK(0.0, {'R': R5(off(SOL[0], 115, 0.35, 0.3, 1.75)), 'L': R5(off(SOL[0], 115, 0.2, -0.3, 1.0))}, {'R': 'point', 'L': 'rest'}, STERN, d=0.0),
       *[TK(r(0.15 + 0.3 * j), {'R': R5(off(SOL[0], 115, 0.35 + 0.1 * (j % 2), 0.3 - 0.25 * (j % 2), 1.65 + 0.15 * (j % 2)))}, {'R': 'open' if j % 2 else 'point'}, d=0.18, keep=True) for j in range(4)],
       k(1.0, look='camera', lookDur=0.15), *blink(0.8, STERN)]
ks2 = [k(0.0, clip='stand'), k(0.0, look=CH11), TK(0.0, {'R': R5(off(SOL[1], 220, 0.35, 0.25, 1.95)), 'L': R5(off(SOL[1], 220, 0.35, -0.25, 1.95))}, {'R': 'open', 'L': 'open'}, STERN, d=0.0),
       *[TK(r(0.3 + 0.3 * j), {'R': R5(off(SOL[1], 220, 0.35, 0.25 + 0.08 * (j % 2), 1.95 - 0.1 * (j % 2)))}, d=0.25, keep=True) for j in range(3)], *blink(0.7, STERN)]
sold = [act('soldat1', SOL[0], 115, 'stand', 'neutral', keys=ks1), act('soldat2', SOL[1], 220, 'stand', 'neutral', keys=ks2)]
st.shot('S11', 'pavillon', setOpts={'fence': False, 'mailbox': False}, look={'sunDir': [0.5, 0.9, 0.7]}, actors=sold,
        props=[P('toupie11', 'fuMixer', pos=MIX, ry=MRY, opts={}),
               P('coulee11', 'fuPour', pos=LIP11, opts={'from': [r(CH11[i] - LIP11[i]) for i in range(3)], 'to': [r(SPL11[i] - LIP11[i]) for i in range(3)], 'r': 0.22, 'pour': [0.05, 3.3]}),
               P('fenetre11', 'fuWindow', pos=WIN11, opts={'w': 1.25, 'h': 1.05, 'fill': [0.45, 1.4]}),
               P('cuisine11', 'fuKitchen', pos=KIT11, opts={'doorX': 2.2, 'tap': False, 'wallH': 6.0, 'upper': True}),
               P('beton11', 'fuConcrete', pos=KIT11, opts={'h': 2.2, 'slope': [0.26, 1.0, 0.3], 'fx': FX11, 'fz': FZ11, 'fw': 1.0, 'fh': 1.5, 'ftilt': [0.16, 0.35, 0.26],
                 'lumps': [[FX11 - 1.3, 1.9, 0.55, 0.18], [FX11 + 1.1, 1.2, 0.6, 0.24], [FX11 + 0.4, 0.75, 0.5, 0.26], [FX11 - 0.7, 0.7, 0.55, 0.3], [FX11 + 1.7, 2.2, 0.45, 0.14], [FX11 - 1.9, 1.0, 0.5, 0.22]],
                 'plop': [r(CUT11 + 0.3), FX11 + 0.85, FZ11 + 0.6], 'dust': [r(CUT11 + 0.32), FX11 + 0.85, FZ11 + 0.6], 'slide': [r(CUT11 + 0.7), r(CUT11 + 1.5)]})], cams=[C11, C11b])
st.card('S11', 'BÉTON', at=CARD11)
st.cue('engine', 'S11', 0.0, 0.3); st.cue('sfx:pour', 'S11', 0.1, 0.45); st.cue('sfx:splat', 'S11', 0.4, 0.4); st.cue('thud', 'S11', CUT11, 0.4); st.cue('sfx:splat', 'S11', r(CUT11 + 0.3), 0.35); st.cue('clack', 'S11', r(CUT11 + 1.7), 0.3)

# ================================================================= S12
# 12: downstairs: the neighbour on his sofa watches TV, a bowl of crisps on his knees; a drop forms on the ceiling and falls, plic, into the bowl
D12 = st.dur('S12'); FALL12 = 0.35
NB = [0.0, 0, -2.85]; NRY = 0
BOWL = add(NB, [0, 0.75, 0.62])
C12 = cam(0.0, [0.9, 1.3, 1.6], [0.88, 1.29, 1.45], [0.0, 1.55, -2.3], [0.0, 1.5, -2.3], lens=46)
chk('S12', C12, {'nbFace': add(NB, [0, 1.6, 0.15]), 'bowl': BOWL, 'ceil': add(BOWL, [0, 1.75, 0])})
knb = [k(0.0, clip='sit'), k(0.0, look=[-1.0, 1.0, -1.95]), TK(0.0, {'R': R5(add(BOWL, [-0.2, 0.05, 0.0])), 'L': R5(add(BOWL, [0.2, 0.05, 0.0]))}, {'R': 'grip', 'L': 'grip'}, CALM, d=0.0),
       TK(0.5, {'R': R5(add(BOWL, [-0.05, 0.12, 0.0]))}, {'R': 'pinch'}, d=0.15, keep=True), TK(0.8, {'R': R5(add(NB, [-0.05, 1.45, 0.3]))}, {'R': 'pinch'}, d=0.2, keep=True),
       TK(1.3, {'R': R5(add(BOWL, [-0.2, 0.05, 0.0]))}, {'R': 'grip'}, d=0.2, keep=True), k(1.47, look=BOWL, lookDur=0.06),
       TK(1.48, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'jaw': 1.0}, sq=(1.04, 0.96, 1.04), d=0.06, e='out', keep=True),
       TK(1.75, face={'lid': 0.2, 'mouth': 'O', 'brow': 0.8, 'jaw': 0.8}, sq=(1, 1, 1), d=0.15, keep=True), *blink(0.6, CALM)]   # the take: eyes out, jaw down
st.shot('S12', 'livingRoom', setOpts={'tv': False, 'picture': False}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[act('voisin', NB, NRY, 'sit', 'neutral', keys=knb)],
        props=[P('bol12', 'fuBowl', pos=BOWL, opts={'splashAt': 1.45, 'chipsAt': 1.46, 'water': [[1.45, 0], [1.6, 0.25]]}), P('goutte12', 'fuDrop', pos=add(BOWL, [0, 1.75, 0]), opts={'s': 0.2, 'fall': [FALL12, 1.47, 1.62], 'once': True}),
               P('tele12', 'fuTV', pos=[-1.0, 0, -1.95], ry=140), P('plafond12', 'fuCeiling', pos=add(BOWL, [0, 1.98, 0]), opts={'w': 3.2, 'd': 3.2, 'wetAt': 0.0})], cams=[C12])
st.cue(PLIC, 'S12', 1.45, 0.5)

# ================================================================= S13
# 13: two agents walk the handcuffed neighbour slowly out of his flat; he holds the bowl out in front, tilted to us, half full of blue water, chunky
#    cuffs on his wrists under it; a sheepish glance down, a small shrug
D13 = st.dur('S13')
N0, N1 = [0.0, 0, -1.5], [0.0, 0, -0.3]
C13 = cam(0.0, [0.5, 1.5, 4.4], [0.5, 1.5, 4.25], [0.0, 1.3, -0.7], [0.0, 1.3, -0.55], lens=44)
BW = [0, 1.22, 0.45]; CF = [0, 1.02, 0.36]
chk('S13', C13, {'nbFace0': add(N0, [0, 1.95, 0]), 'nbFace1': add(N1, [0, 1.95, 0]), 'bowl1': add(N1, BW), 'cuffs': add(N1, CF), 'a1': add(N1, [-0.8, 2.0, -0.25]), 'a2': add(N1, [0.8, 2.0, -0.25])})
def at13(p0, p1, t): return lerp3(p0, p1, min(1.0, t / D13))
STEP13 = 0.2
SHY = {'lid': 0.5, 'mouth': 'line', 'brow': 0.8}
kn13 = [k(0.0, clip='walk'), k(0.0, to=N1, dur=D13, clip='walk', ease='linear', face='keep', params={'freq': 1.2}), k(0.0, look='camera'),
        TK(0.0, {'R': R5(add(add(N0, BW), [-0.17, -0.05, -0.04])), 'L': R5(add(add(N0, BW), [0.17, -0.05, -0.04]))}, {'R': 'grip', 'L': 'grip'}, SHY, d=0.0),
        *[TK(r(j * STEP13), {'R': R5(add(add(at13(N0, N1, r((j + 1) * STEP13)), BW), [-0.17, -0.05, -0.04])), 'L': R5(add(add(at13(N0, N1, r((j + 1) * STEP13)), BW), [0.17, -0.05, -0.04]))}, d=STEP13, e='linear', keep=True) for j in range(int(D13 / STEP13) + 1)],
        k(0.45, look=add(N1, [0, 0.6, 0.6]), lookDur=0.2), TK(0.5, face={**SHY, 'lid': 0.7}, d=0.15, keep=True), k(1.15, look='camera', lookDur=0.2),   # a glance down...
        TK(1.15, face=SHY, sq=(1.05, 0.94, 1.05), bend={'spine': SP(-0.05)}, d=0.12, keep=True), TK(1.4, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.15, keep=True), *blink(0.25, SHY)]   # ...and a small shrug
ag13 = []
for i, sx in enumerate([-1, 1]):
    a, b = add(N0, [sx * 0.8, 0, -0.25]), add(N1, [sx * 0.8, 0, -0.25])
    hi, lo = ('L' if sx < 0 else 'R'), ('R' if sx < 0 else 'L')
    ks = [k(0.0, clip='walk'), k(0.0, to=b, dur=D13, clip='walk', ease='linear', face='keep', params={'freq': 1.2}), k(0.0, look='camera'),
          TK(0.0, {hi: R5(add(a, [-sx * 0.5, 1.25, 0.12])), lo: R5(off(a, 0, 0.1, 0.25 if sx < 0 else -0.25, 0.95))}, {'R': 'grip', 'L': 'grip'}, STERN, d=0.0),
          *[TK(r(j * STEP13), {hi: R5(add(at13(a, b, r((j + 1) * STEP13)), [-sx * 0.5, 1.25, 0.12])), lo: R5(off(at13(a, b, r((j + 1) * STEP13)), 0, 0.1, 0.25 if sx < 0 else -0.25, 0.95))}, d=STEP13, e='linear', keep=True) for j in range(int(D13 / STEP13) + 1)],
          *blink(r(0.4 + 0.5 * i), STERN)]
    ag13.append(act(f'agent{i + 1}', a, 0, 'walk', 'neutral', keys=ks))
st.shot('S13', 'livingRoom', setOpts={'tv': False}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[act('voisin', N0, 0, 'walk', 'neutral', keys=kn13), *ag13],
        props=[P('bol13', 'fuBowl', pos=add(N0, BW), rot=[0.6, 0, 0], opts={'water': 0.98, 'r': 0.2, 'crisps': False}, keys=[k(0.0, to=add(N1, BW), dur=D13, ease='linear')]),
               P('menottes13', 'fuCuffs', pos=add(N0, CF), opts={'s': 1.25}, keys=[k(0.0, to=add(N1, CF), dur=D13, ease='linear')]),
               *[x for i in range(1, 3) for x in AGENT('S13', i)]], cams=[C13])
for j in range(3): st.cue('sfx:step', 'S13', r(0.25 + 0.6 * j), 0.2)

# ================================================================= S14
# 14: a dark van pulls up, seen three-quarter; the plumber in blue bib overalls and cap, black shades and an earpiece, rides in on the side step,
#    steps down (a squash held two or three frames as he lands), toolbox in hand, and walks slowly at us
D14 = st.dur('S14'); STOP14 = 0.5; DOWN14 = 0.9; LAND14 = 1.15
VAN = [0.6, 0, 2.6]; VAN0 = add(VAN, [1.6, 0, 0])
PL0, PL1, PL2 = [0.35, 0.32, 3.72], [0.55, 0, 4.25], [2.2, 0, 6.0]
C14 = fcam(0.0, [4.6, 1.35, 9.6], {'plTop0': add(PL0, [0, 2.45, 0]), 'plTop2': add(PL2, [0, 2.45, 0]), 'plKnee2': add(PL2, [0, 0.5, 0]), 'vanL': add(VAN, [-1.4, 2.3, 1.0]), 'vanR': add(VAN, [2.2, 1.0, -0.6])}, top=0.1, bottom=0.8, margin=0.06, push=0.4)
chk('S14', C14, {'plFace0': add(PL0, [0, 1.95, 0]), 'plFace2': add(PL2, [0, 1.95, 0]), 'van': add(VAN, [2.4, 1.2, 0.0]), 'vanBack': add(VAN, [-2.4, 1.2, 1.0])})
PFACE = {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}
kpl14 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'L': R5(add(PL0, [0.3, 1.4, -0.15]))}, {'R': 'grip', 'L': 'grip'}, PFACE, d=0.0),   # one hand on the door frame
         k(0.0, to=PL0, dur=STOP14, ease='out', face='keep'),
         TK(r(DOWN14 - 0.1), {'L': R5(off(PL0, 0, 0.1, -0.25, 0.95))}, {'L': 'rest'}, sq=(1.05, 0.94, 1.05), d=0.1, keep=True),
         k(DOWN14, to=PL1, dur=r(LAND14 - DOWN14), ease='in', face='keep'), TK(DOWN14, sq=(0.96, 1.06, 0.96), d=0.08, keep=True),   # steps down off the step
         TK(LAND14, sq=(1.22, 0.78, 1.22), d=0.0, keep=True), TK(r(LAND14 + 0.1), sq=(1.2, 0.8, 1.2), d=0.0, keep=True), TK(r(LAND14 + 0.11), sq=(0.95, 1.06, 0.95), d=0.08, e='out', keep=True), TK(r(LAND14 + 0.25), sq=(1, 1, 1), d=0.08, keep=True),   # the landing squash, held
         k(r(LAND14 + 0.25), to=PL2, dur=r(D14 - LAND14 - 0.25), clip='walk', ease='linear', face='keep', params={'freq': 1.1}), *blink(1.7, PFACE)]
st.shot('S14', 'cottageStreet', look={'sunDir': [0.5, 0.9, 0.7]}, actors=[act('plombier', add(PL0, [1.6, 0, 0]), 0, 'stand', 'neutral', keys=kpl14)],
        props=[P('van14', 'fuVan', pos=VAN0, opts={'stopAt': STOP14, 'doorAt': -1, 'color': '#4A5260'}, keys=[k(0.0, to=VAN, dur=STOP14, ease='out')]),
               P('trottoir14', 'parkLot', pos=[1.5, 0.03, 6.0], opts={'w': 14, 'd': 9, 'color': '#C9C4BA'}),
               P('caisse14', 'fuToolbox', on={'actor': 'plombier', 'hand': 'R', 'offset': [0, -0.03, 0]}), P('lunettes14', 'shades', on={'actor': 'plombier', 'joint': 'head', 'offset': [0, 0.28, 0.36]}, opts={'s': 1.45}),
               P('salopette14', 'fuOveralls', on={'actor': 'plombier', 'joint': 'torso', 'offset': [0, 0.12, 0.16]}), P('casquette14', 'fuCap', on={'actor': 'plombier', 'joint': 'head', 'offset': [0, 0.47, 0.0]})], cams=[C14])
st.cue('sfx:brake', 'S14', 0.25, 0.4); st.cue('thud', 'S14', LAND14, 0.3)
for j in range(2): st.cue('sfx:stepHeavy', 'S14', r(1.6 + 0.45 * j), 0.2)

# ================================================================= S15
# 15: the kitchen, a hole chiselled in the concrete: the plumber holds out on his flat mitten an oversized black washer; a price tag pops beside
#    it with one small coin drawn on it
D15 = st.dur('S15'); TAG15 = r(st.at('S15', 'L15', 5) - 0.05)
PL15 = [0.35, 0, 3.0]; PRY15 = -15
RING = off(PL15, PRY15, 0.72, 0.02, 1.6)
C15 = cam(0.0, [-0.3, 1.65, 5.6], [-0.28, 1.64, 5.4], [0.2, 1.45, 2.2], [0.2, 1.45, 2.2], lens=44)
chk('S15', C15, {'plFace': add(PL15, [0, 1.95, 0]), 'plTop': add(PL15, [0, 2.4, 0]), 'ring': RING, 'tag': add(RING, [-0.45, 0.25, 0]), 'hole': [0.0, 0.9, 2.62]})
kpl15 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(RING), 'L': R5(off(PL15, PRY15, 0.2, -0.25, 1.0))}, {'R': 'open', 'L': 'rest'}, {'lid': 0.35, 'mouth': 'line', 'brow': -0.1}, d=0.0),
         TK(0.35, sq=(0.98, 1.05, 0.98), d=0.3, keep=True), TK(0.75, sq=(1, 1, 1), d=0.3, keep=True),   # a proud breath
         TK(r(TAG15 - 0.3), face=SMUG, bend={'neck': SP(0.0, 0.18)}, d=0.15, keep=True), TK(r(TAG15 + 0.5), bend={'neck': SP(0.0, 0.0)}, d=0.2, keep=True), *blink(0.6, CALM)]
st.shot('S15', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('plombier', PL15, PRY15, 'stand', 'neutral', keys=kpl15)],
        props=[KITCHEN('S15', tap=False), P('beton15', 'fuConcrete', pos=KIT, opts={'fx': -2.1, 'h': 2.65, 'hole': [0.0, 0.9]}),
               P('joint15', 'fuRing', pos=add(RING, [0, 0.05, 0]), rot=[0.45, 0, 0], opts={'R': 0.11}), P('salopette15', 'fuOveralls', on={'actor': 'plombier', 'joint': 'torso', 'offset': [0, 0.12, 0.16]}), P('etiquette15', 'fuTag', pos=add(RING, [-0.3, 0.42, 0.05]), opts={'w': 0.3, 'popAt': TAG15}),
               P('lunettes15', 'shades', on={'actor': 'plombier', 'joint': 'head', 'offset': [0, 0.28, 0.36]}, opts={'s': 1.45}), P('casquette15', 'fuCap', on={'actor': 'plombier', 'joint': 'head', 'offset': [0, 0.47, 0.0]})], cams=[C15])
st.cue('sfx:pop', 'S15', TAG15, 0.4); st.cue('sfx:cash', 'S15', r(TAG15 + 0.1), 0.2)

# ================================================================= S16
# 16: the palace office: the plumber's invoice, wide, unrolls off the desk and on across the floor toward us; one agent rolls it back up from
#    its end (a fat roll in his hands), the other holds the big safe open and slams it: a shake and a puff
D16 = st.dur('S16'); ROLL16 = 1.6; SLAM16 = 2.75   # (rolled back from 1.6 to 2.5)
DESK16 = [-0.45, 0, -1.4]; INV = [-0.45, 0.78, -1.05]; SAFE = [1.0, 0, -0.75]
AG16 = [[-0.88, 0, 1.45], [0.3, 0, -1.05]]
C16 = cam(0.0, [-0.3, 1.75, 5.4], [-0.25, 1.73, 5.2], [-0.15, 0.95, -0.6], [-0.15, 0.95, -0.6], lens=48)
chk('S16', C16, {'desk': add(DESK16, [0, 0.8, 0]), 'invEnd': [-0.45, 0.0, 2.2], 'safe': add(SAFE, [0, 1.4, 0]), **{f'a{i}': add(p, [0, 2.0, 0]) for i, p in enumerate(AG16)}})
UNR = [[0.1, 0], [1.3, 5.0], [ROLL16, 5.0], [2.5, 2.0]]
def inv_end(t):   # where the floor end of the invoice is (z) at t
    u = UNR[0][1]
    for (a, va), (b, vb) in zip(UNR, UNR[1:]):
        if a <= t < b: x = (t - a) / (b - a); u = va + (vb - va) * x * x * (3 - 2 * x); break
        if t >= b: u = vb
    return r(INV[2] + 0.08 + max(0.0, u - 0.78))
ry1 = 90
ka1 = [k(0.0, clip='stand'), k(0.0, look=[-0.45, 0.9, -0.6]), TK(0.0, HANDS(AG16[0], ry1, 0.15, 0.25, 0.95, 0.15, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, STERN, d=0.0),
       TK(0.6, face={**STERN, 'brow': 0.6, 'lid': 0.0}, d=0.08, keep=True), k(1.2, look=[-0.45, 0.4, 1.6], lookDur=0.15), k(1.25, clip='kneel', blend=0.2),
       *[TK(r(1.4 + 0.15 * j), {'R': R5([-0.6, 0.2, r(max(1.05, min(1.9, inv_end(1.55 + 0.15 * j))))]), 'L': R5([-0.3, 0.2, r(max(1.05, min(1.9, inv_end(1.55 + 0.15 * j))))])}, {'R': 'grip', 'L': 'grip'}, bend={'spine': SP(0.3), 'neck': SP(0.0)}, d=0.15, keep=True) for j in range(7)],   # kneeling at the near end, hands on the roll   # stooped from the hips, hands on the roll as it comes back
       TK(r(SLAM16 + 0.05), {'R': R5([-0.55, 0.45, 1.35]), 'L': R5([-0.35, 0.45, 1.35])}, {'R': 'grip', 'L': 'grip'}, SMUG, bend={'spine': SP(0.0)}, d=0.25, keep=True), k(r(SLAM16 + 0.1), look='camera', lookDur=0.15)]
ry2 = 35
DOOR16 = add(SAFE, [-0.55, 1.0, 0.55])
ka2 = [k(0.0, clip='stand'), k(0.0, look=[-0.45, 0.6, 0.5]), TK(0.0, {'R': R5(DOOR16), 'L': R5(off(AG16[1], ry2, 0.15, -0.25, 0.95))}, {'R': 'grip', 'L': 'rest'}, STERN, d=0.0),
       k(1.0, look='camera', lookDur=0.15), *blink(1.3, STERN), k(r(SLAM16 - 0.3), look=SAFE, lookDur=0.1),
       TK(r(SLAM16 - 0.12), {'R': R5(add(SAFE, [-0.15, 1.0, 0.5])), 'L': R5(add(SAFE, [-0.4, 0.95, 0.5]))}, {'R': 'open', 'L': 'open'}, sq=(1.06, 0.94, 1.06), bend={'spine': SP(0.25)}, d=0.1, e='out', keep=True),
       TK(r(SLAM16 + 0.2), {'R': R5(off(AG16[1], ry2, 0.15, 0.25, 0.95)), 'L': R5(off(AG16[1], ry2, 0.15, -0.25, 0.95))}, {'R': 'rest', 'L': 'rest'}, SMUG, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.2, keep=True), k(r(SLAM16 + 0.25), look='camera', lookDur=0.15)]
st.shot('S16', 'office', setOpts={'door': False, 'printer': False, 'carpet': False, 'picture': False}, look={'sunDir': [0.3, 0.9, 0.9]},
        actors=[act('agent1', AG16[0], ry1, 'stand', 'neutral', keys=ka1), act('agent2', AG16[1], ry2, 'stand', 'neutral', keys=ka2)],
        props=[P('bureau16', 'desk', pos=DESK16, opts={'w': 1.5}), P('facture16', 'fuInvoice', pos=INV, opts={'w': 0.42, 'unroll': UNR, 'len': 6.0, 'drop': 0.78, 'endRoll': 5.0}),
               P('coffre16', 'fuSafe', pos=SAFE, ry=-25, opts={'door': [[0, 1]], 'slamAt': SLAM16}), *[x for i in range(1, 3) for x in AGENT('S16', i)]], cams=[C16])
st.cue('sfx:paper', 'S16', 0.2, 0.35); st.cue('sfx:paper', 'S16', ROLL16, 0.3); st.cue('clang', 'S16', SLAM16, 0.6); st.cue('sfx:poof', 'S16', r(SLAM16 + 0.02), 0.25)

# ================================================================= S17
# 17: the kitchen after: a clean tap; seen 3/4 front over the sink, the hero finally rinses his big plate under a visible stream (the stains wash
#    off), then turns the lever off with a clear twist; not a drop (silence)
D17 = st.dur('S17'); OFF17 = 0.95
HER17 = [0.5, 0, 0.8]; HRY17 = -135
TAPP = [0.0, 0.945, 0.1]
PL17 = [0.02, 0.98, 0.44]; LEV17 = [0.15, 1.145, 0.1]
C17 = fcam(0.0, [-1.15, 1.6, 0.8], {'heroTop': add(HER17, [0, 2.35, 0]), 'heroWaist': add(HER17, [0, 0.9, 0]), 'tap': add(TAPP, [0, 0.32, 0.3]), 'plate': PL17, 'plateB': add(PL17, [0, -0.1, 0.1])}, top=0.1, bottom=0.76, margin=0.1, push=0.15)
chk('S17', C17, {'heroFace': add(HER17, [0, 1.95, 0]), 'heroTop': add(HER17, [0, 2.3, 0]), 'tap': add(TAPP, [0, 0.3, 0.3]), 'plate': PL17, 'lever': LEV17})
FACE17 = {'lid': 0.35, 'mouth': 'smile', 'brow': 0.2}
k17 = [k(0.0, clip='stand'), k(0.0, look=PL17), TK(0.0, {'L': R5(add(PL17, [0.12, 0.0, 0.12])), 'R': R5(add(PL17, [-0.05, 0.03, 0.05]))}, {'L': 'grip', 'R': 'open'}, FACE17, bend={'spine': SP(0.15)}, d=0.0),
       *[TK(r(0.08 + 0.12 * j), {'R': R5(add(PL17, [-0.06 + 0.1 * (j % 2), 0.03, 0.05 - 0.06 * (j % 2)]))}, d=0.11, keep=True) for j in range(6)],   # scrubbing
       TK(r(OFF17 - 0.15), {'R': R5(add(LEV17, [0.02, 0.03, 0.05]))}, {'R': 'pinch'}, d=0.12, keep=True), k(r(OFF17 - 0.15), look=LEV17, lookDur=0.1),
       TK(r(OFF17 + 0.02), {'R': R5(add(LEV17, [0.1, 0.03, -0.02]))}, {'R': 'pinch'}, d=0.12, e='out', keep=True),   # the twist
       TK(r(OFF17 + 0.25), {'R': R5(off(HER17, HRY17, 0.25, 0.25, 1.05))}, {'R': 'rest'}, {**FACE17, 'lid': 0.2, 'brow': 0.4}, d=0.15, keep=True), k(r(OFF17 + 0.2), look='camera', lookDur=0.15), *blink(0.5, FACE17)]
st.shot('S17', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('mec', HER17, HRY17, 'stand', 'neutral', keys=k17)],
        props=[KITCHEN('S17', tap=False), P('robinet17', 'fuTap', pos=TAPP, opts={'flow': [[0.0, r(OFF17 + 0.08)]], 'flowLen': 0.2, 'flowR': 0.016, 'flowOp': 0.55, 'leverAt': r(OFF17 + 0.02)}),
               P('assiette17', 'fuPlate', pos=PL17, rot=[0.25, 0, -0.15], opts={'r': 0.26, 'cleanAt': 0.15, 'cleanDur': 0.7})], cams=[C17])
st.cue('sfx:pour', 'S17', 0.0, 0.25); st.cue('sfx:squeak', 'S17', OFF17, 0.25)

# ================================================================= S18
# 18: close on the tap from the end of the counter, its spout a third of the frame: the hero walks away out of frame to the left; the spout
#    winds up, swivels after him (ease, overshoot, settle), its nozzle turns to us and a grille with a red light blinks on inside; held
D18 = st.dur('S18'); SW18 = [0.55, 1.35]; LIGHT18 = 1.6
H18A, H18B = [-1.45, 0, 0.6], [0.25, 0, 2.6]
TH0, TH1 = -1.28, 0.15
SP18 = add(TAPP, [0, 0.6, 0])   # the spout pivot at s 2
def MOUTH18(th, tilt=0.0): return [r(SP18[0] + 0.64 * math.sin(th)), r(SP18[1] - 0.1), r(SP18[2] + 0.64 * math.cos(th))]
C18 = fcam(0.0, [1.2, 1.3, 0.85], {'colBot': add(TAPP, [0, 0.0, 0]), 'colTop': SP18, 'mouth0': MOUTH18(TH0), 'mouth1': MOUTH18(TH1), 'heroTop': add(H18A, [0, 2.35, 0])}, top=0.12, bottom=0.74, margin=0.16, push=0.12)
chk('S18', C18, {'mouth0': MOUTH18(TH0), 'mouth1': MOUTH18(TH1), 'heroA': add(H18A, [0, 1.95, 0]), 'heroMid': add(lerp3(H18A, H18B, 0.5), [0, 1.95, 0]), 'heroB': add(H18B, [0, 1.95, 0])})
k18 = [k(0.0, clip='walk'), k(0.0, to=H18B, dur=1.1, clip='walk', ease='inOut', face='keep'), k(0.0, look='camera'), k(1.1, visible=False)]
SWV = [[0.0, TH0], [SW18[0], TH0], [r(SW18[0] + 0.18), r(TH0 - 0.14)], [r(SW18[1] - 0.12), r(TH1 + 0.16)], [SW18[1], TH1]]   # wind-up, swing, overshoot, settle
st.shot('S18', 'whiteVoid', setOpts=KV, look=LOOKK, actors=[act('mec', H18A, yaw(H18A, H18B), 'walk', 'neutral', keys=k18)],
        props=[KITCHEN('S18', tap=False, burstAt=-1), P('robinet18', 'fuTap', pos=TAPP, opts={'s': 2.0, 'swivel': SWV, 'tilt': [[0.0, 0.0], [SW18[0], 0.0], [SW18[1], -0.18]],
               'peek': [[0.0, 0.0], [r(SW18[1] + 0.05), 0.0], [r(LIGHT18 - 0.05), -0.75]], 'lightAt': LIGHT18, 'ledR': 0.012, 'glowR': 0.03})], cams=[C18])
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
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
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
    'plombier': {'preset': 'worker', 'seed': 1004, 'outfit': 'suit', 'suit': '#E6E1D6', 'lapel': '#E6E1D6', 'tie': '#E6E1D6', 'shirt': '#E6E1D6', 'cuff': '#E6E1D6', 'pants': '#3E7FD6', 'hat': 'none', 'hair': 'crew', 'hairColor': '#2A2420', 'facial': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
