#!/usr/bin/env python3
"""Le mot (story 105; a passive-aggressive note in the lobby, a whole country that recognises itself, and the snorer who never did).
A noise wakes this man every night; he pins up « Certains se reconnaîtront. » and the whole country recognises itself: confessions by the million,
even the prefect returns his neighbour's drill. Too many culprits: noise is banned. Firemen whisper, binmen tiptoe, roosters go under domes, people
talk by notes. The country sleeps, except him; giant microphones follow the noise to his bed: he snores and wakes himself up. The next morning there
is a note on his door; sixty million notes.
Running gags (silent): the neighbours' head-width bright pink earmuffs in every building shot (S01 lobby, S10 cutaway, S12 window) and the gift pair
with a bow on top of the paper avalanche (S16); the hero bolts upright in bed with the very same pose and relative framing (S01, S10, S13); guilt is
a sweat drop and a finger pointed at oneself (S02, S04, S14).
Cards: AVEUX (S03), SILENCE (S05). The only other words: the note « CERTAINS SE RECONNAÎTRONT. ». No figure, flag, emblem or sash; at most five people
in a shot."""
from story_kit import *
import math

st = Story('mot', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 17)])
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
SHUT = {'lid': 0.3, 'mouth': 'clench', 'brow': -0.2}
POP = {'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 1.0}
SKY = '#A9D3EE'
DAWN = '#BFD3E8'
def DROP(pid, actor, t0, offset=(0.18, 0.42, 0.1), scale=0.8):
    """a sweat drop that pops on his brow at t0 (guilt)"""
    return P(pid, 'sweatDrop', on={'actor': actor, 'joint': 'head', 'offset': list(offset)}, scale=scale, keys=[k(0.0, visible=False), k(t0, visible=True), k(t0, squash=[1.6, 0.5, 1.6], dur=0.3)])
def MUFFS(pid, actor, span=0.2, y=0.14):
    """the head-width bright pink fluffy earmuffs (never mentioned)"""
    return P(pid, 'moEarmuffs', on={'actor': actor, 'joint': 'head', 'offset': [0, y, 0]}, opts={'span': span, 'top': 0.24, 'r': 0.14})
def SELFPT(side='R', w=1):
    """(round 1) the index on his own chest: a touch in the frame of his torso, the elbow out in front (the pointSelf clip never showed)"""
    sx = -1 if side == 'R' else 1
    return {side: ['torso', r(0.07 * sx), 0.46, 0.27, w, 0.04, [r(0.75 * sx), -0.35, 0.6]]}
def GUILT(t0, face=None, side='R', bend=None):
    """the guilt beat: a jolt, then the finger pointed at oneself (never a flat hand on the chest), with an overshoot"""
    f = face or {'lid': 0.1, 'mouth': 'line', 'brow': 0.9}
    return [TK(t0, face={**f, 'mouth': 'O'}, sq=(0.9, 1.12, 0.9), d=0.04, e='out', keep=True),
            TK(r(t0 + 0.07), touch=SELFPT(side), hands={side: 'point'}, sq=(1.05, 0.96, 1.05), bend=bend or {'spine': SP(-0.12)}, d=0.07, e='out', keep=True),
            TK(r(t0 + 0.2), face=f, sq=(1, 1, 1), d=0.08, keep=True)]
def BLINKS(t0, t1, face, every=2.2, ph=0.0):
    """(round 1) a blink every ~2 s through a hold"""
    out, t = [], r(t0 + ph)
    while t < t1 - 0.15: out += blink(t, face); t = r(t + every + 0.3 * math.sin(t * 7))
    return out

# the bedroom (one layout everywhere: the bolt-upright shots are framed the same way relative to him)
def BEDROOM(sid, o, lamp_wobble=None, curtain_flap=None):
    return [P(f'chambre{sid}', 'moRoom', pos=o, opts={'w': 5, 'd': 4, 'h': 3, 'wall': '#CFDCEA', 'floor': '#A8927A'}),
            P(f'rideaux{sid}', 'moCurtains', pos=add(o, [0.3, 1.75, -1.93]), opts={'flap': curtain_flap or []}),
            P(f'lit{sid}', 'bed', pos=add(o, [-0.3, 0, -0.65]), opts={'blanket': '#8FB8D8'}),
            P(f'couette{sid}', 'moDuvet', pos=add(o, [-0.3, 0.58, -0.3]), opts={'w': 1.3, 'l': 1.15, 'h': 0.1, 'flapAt': []}),   # (round 1) thin: the sleeper reads over it
            P(f'lampe{sid}', 'moLamp', pos=add(o, [0.52, 0, -1.15]), opts={'wobble': lamp_wobble or []})]
def BEDPOS(o): return add(o, [-0.3, 0.52, -0.45])   # his hips in bed (lying: head on the pillow; sitting: legs under the duvet)
def BEDCAM(at, o, push=0.15):
    """(round 1) wider and lower than draft 1: the head stays in the frame at the apex of the bolt upright (fit: apex 12 %), the lit lamp and the curtains in
    the frame; one camera for S01, S10, S12b, S13"""
    # (round 1, draft 2) higher: the lying man reads over the duvet
    f, L = add(o, [0.9, 2.2, 3.2]), add(o, [-0.987, -0.104, -6.346]); d = [L[i] - f[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in d))
    return cam(at, f, [r(f[i] + d[i] / n * push) for i in range(3)], L, L, lens=44)
def BEDCHK(sid, c, o): chk(sid, c, {'apex': add(o, [-0.3, 2.5, -0.42]), 'lamp': add(o, [0.52, 1.05, -1.15]), 'curT': add(o, [0.3, 2.45, -1.93]), 'lieHead': add(o, [-0.3, 0.85, -1.15]), 'mic': add(o, [-0.35, 2.55, -1.2])})
def BEDMIC(pid, o, jolt=None):
    """(round 1) the boom mic hangs over the headboard, above the line of his head, its pole going up and back out of the frame (it ran through his head)"""
    return P(pid, 'moMic', pos=add(o, [-0.35, 2.62, -1.25]), rot=[0, -1.5708, -0.75], opts={'r': 0.3, 'pole': 2.4, 'jolt': jolt or []})
ASLEEP = {'lid': 1.0, 'mouth': 'line', 'brow': 0.0}
WIDE = {'lid': 0.0, 'mouth': 'line', 'brow': 1.0, 'pop': 0.5}
def LIE(t=0.0, face=ASLEEP): return [k(t, clip='lieBack'), TK(t, face=face, d=0.0)]
def SITUP(t0, after=1.0):
    """THE bolt upright: from lying to sitting in two frames, stretched (capped in round 1: the head left the frame), eyes wide... the same key in S01, S10
    and S13; speed lines (SMEAR) trail it"""
    return [k(r(t0 - 0.06), toon={'sq': [1.08, 0.9, 1.08]}, toonDur=0.05, keepPose=True),   # a twitch (anticipation)
            k(t0, clip='sitFloor', blend=0.07), TK(t0, face=WIDE, sq=(0.88, 1.12, 0.88), scl={'head': [0.94, 1.1, 0.97]}, d=0.04, e='out', keep=True),   # up, stretched
            TK(r(t0 + 0.12), sq=(1.08, 0.94, 1.08), scl={'head': [1.05, 0.95, 1.02]}, d=0.06, keep=True), TK(r(t0 + 0.24), face={**WIDE, 'pop': 0.2}, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.08, keep=True),   # overshoot, settle
            k(t0, look='camera', lookDur=0.04)]
def SMEAR(pid, o, t0): return P(pid, 'moSmear', pos=add(BEDPOS(o), [0, 0.35, -0.1]), opts={'at': [r(t0 - 0.01)], 'h': 1.3, 'w': 0.75, 'dur': 0.14})
def LOOKAROUND(t0, o, n=3, every=0.35): return [k(r(t0 + every * j), look=HEAD(add(o, [-1.5 if j % 2 == 0 else 1.5, 0, 0.6]), 1.6), lookDur=0.14) for j in range(n)]
def BEDHANDS(o, t=0.0): p = BEDPOS(o); return TK(t, {'R': R5(add(p, [-0.3, 0.12, 0.35])), 'L': R5(add(p, [0.3, 0.12, 0.35]))}, {'R': 'rest', 'L': 'rest'}, d=0.0, keep=True)

# ================================================================= S01
# 1: three cuts. The bedroom in pale dawn blue with the warm lamp on: a low rumble and he bolts upright, eyes wide. Cut: the lobby by day: he pins a
#    big note on the cork board with one firm mitten while two neighbours in head-width pink earmuffs walk past behind him. Cut: the note
D1 = st.dur('S01'); UP1 = r(st.at('S01', 'L01', 2) - 0.02); CUT1 = r(st.at('S01', 'L01', 7) - 0.1); CUT1b = r(st.at('S01', 'L01', 10) - 0.1)
B1 = [0, 0, 0]
C1 = BEDCAM(0.0, B1)
HALL = [40.0, 0, 0.0]; HB1 = add(HALL, [0.55, 0, -1.4]); BOARD1 = add(HALL, [0.55, 1.6, -1.97])
C1b = cam(CUT1, add(HALL, [-0.7, 1.6, 2.9]), add(HALL, [-0.68, 1.6, 2.7]), add(HALL, [-0.05, 1.55, -1.2]), add(HALL, [-0.07, 1.56, -1.2]), lens=50)
NOTE1 = [80.0, 1.6, 0.0]
C1c = cam(CUT1b, add(NOTE1, [0.04, 0.02, 1.05]), add(NOTE1, [0.03, 0.01, 0.92]), NOTE1, NOTE1, lens=40)
BEDCHK('S01', C1, B1)
chk('S01b', C1b, {'heroTop': add(HB1, [0, 2.35, 0]), 'board': BOARD1, 'nb1': add(HALL, [-0.9, 2.1, -0.4]), 'nb1feet': add(HALL, [-0.9, 0, -0.4])})
chk('S01c', C1c, {'noteL': add(NOTE1, [-0.21, 0, 0]), 'noteR': add(NOTE1, [0.21, 0, 0]), 'noteT': add(NOTE1, [0, 0.15, 0])})
k1 = [*LIE(0.0), BEDHANDS(B1), *[TK(r(0.05 + 0.4 * j), sq=(1.02, 0.99, 1.02) if j % 2 == 0 else (1, 1, 1), d=0.35, keep=True) for j in range(2)], *SITUP(UP1),
      TK(r(UP1 + 0.3), {'R': R5(add(BEDPOS(B1), [-0.35, 0.35, 0.3])), 'L': R5(add(BEDPOS(B1), [0.35, 0.35, 0.3]))}, {'R': 'spread', 'L': 'spread'}, d=0.1, keep=True),
      *LOOKAROUND(r(UP1 + 0.5), B1, 2, 0.35), k(r(UP1 + 1.25), look='camera', lookDur=0.15), *blink(r(UP1 + 1.1), WIDE), *BREATHE(r(UP1 + 0.4), CUT1, 0.35)]
PIN1 = r(CUT1 + 0.32)
kb1 = [k(0.0, visible=False), k(CUT1, visible=True), k(0.0, clip='stand'), k(0.0, look=BOARD1), TK(0.0, {'R': R5(add(BOARD1, [-0.1, -0.05, 0.25])), 'L': R5(off(HB1, 180, 0.2, -0.3, 1.0))}, {'R': 'open', 'L': 'rest'}, STERN, d=0.0),
       TK(r(PIN1 - 0.12), {'R': R5(add(BOARD1, [-0.05, 0.05, 0.3]))}, bend={'spine': SP(-0.1)}, d=0.08, keep=True),   # wind-up...
       TK(PIN1, {'R': R5(add(BOARD1, [0.0, 0.0, 0.07]))}, {'R': 'spread'}, face={**STERN, 'mouth': 'clench'}, sq=(1.12, 0.9, 1.12), bend={'spine': SP(0.15)}, d=0.04, e='in', keep=True),   # ...SLAP: pinned
       TK(r(PIN1 + 0.25), sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.1, keep=True), TK(r(PIN1 + 0.4), {'R': R5(off(HB1, 180, 0.25, 0.3, 1.0))}, {'R': 'rest'}, d=0.15, keep=True),
       k(r(PIN1 + 0.45), face=150, turn=0.2), k(r(PIN1 + 0.45), look='camera', lookDur=0.15), TK(r(PIN1 + 0.5), face=SMUG, d=0.1, keep=True)]   # turns to us, pleased with himself
nbs1 = []
for i in range(2):
    a, b = add(HALL, [-0.4 - 0.6 * i, 0, -1.0 - 0.15 * i]), add(HALL, [-2.4, 0, -1.25 - 0.15 * i]); t0 = r(CUT1 + 0.02 + 0.15 * i)   # past him on the left, at his depth: nobody in front of him
    ks = [k(0.0, clip='walk'), k(0.0, visible=False), k(CUT1, visible=True), k(t0, to=b, dur=r(CUT1b - t0 + 0.1), clip='walk', ease='linear', params={'freq': 1.8}),
          k(0.0, look=HEAD(add(HALL, [-2.5, 0, -2.0]), 1.9)), k(r(PIN1 + 0.02), look=HEAD(HB1, 1.9), lookDur=0.1), TK(0.0, face=CALM, d=0.0), *blink(r(CUT1 + 0.5 + 0.2 * i), CALM)]
    nbs1.append(act(f'voisin{i + 1}', a, yaw(a, b), 'walk', 'neutral', keys=ks))
st.shot('S01', 'whiteVoid', setOpts={'color': DAWN}, look={'sunDir': [0.3, 0.8, 0.8]},
        actors=[act('mecPyj', BEDPOS(B1), 0, 'lieBack', 'neutral', keys=k1 + [k(CUT1, visible=False)]), act('mec', HB1, 180, 'stand', 'neutral', keys=kb1), *nbs1],
        props=[*BEDROOM('S01', B1), P('hall1', 'moRoom', pos=HALL, opts={'w': 7, 'd': 4, 'h': 3.4, 'wall': '#EAE3D2', 'floor': '#DAD1C2'}),
               P('liege1', 'moCork', pos=add(BOARD1, [0, 0, -0.02])), P('boites1', 'moBoxes', pos=add(HALL, [-1.6, 1.5, -1.95])),
               P('mot1', 'moNote', pos=add(BOARD1, [0, 0, 0.03]), opts={'pinAt': PIN1}),
               P('motgros1', 'moNote', pos=NOTE1, opts={'w': 0.42, 'h': 0.3}), P('liegegros1', 'moCork', pos=add(NOTE1, [0.1, 0.05, -0.03]), opts={'w': 1.0, 'h': 0.8}),
               *[MUFFS(f'cacheoreilles1_{i + 1}', f'voisin{i + 1}') for i in range(2)], SMEAR('trait1', B1, UP1)], cams=[C1, C1b, C1c])
st.cue('engine', 'S01', 0.0, 0.25); st.cue('sfx:spring', 'S01', UP1, 0.3); st.cue('thud', 'S01', PIN1, 0.4); st.cue('sfx:paper', 'S01', r(PIN1 - 0.1), 0.25)

# ================================================================= S02
# 2: a street, three passers-by in a staircase and a cyclist riding at us: each stops dead in turn (every four frames), a sweat drop pops and he
#    points at his own chest; the cyclist skids to a stop (he never falls) and does the same, last
D2 = st.dur('S02')
PS2 = [[-1.1, 0, -2.0], [-0.6, 0, -1.1], [-0.1, 0, -0.2]]
CY1 = [0.5, 0, 0.85]; CY0 = add(CY1, [0, 0, -2.4]); BRAKE2 = 0.5; PT2 = [r(0.12 + 0.1333 * i) for i in range(3)] + [r(BRAKE2 + 0.16)]
C2 = cam(0.0, [0.3, 1.75, 5.2], [0.28, 1.74, 5.0], [0.0, 1.25, -1.0], [0.0, 1.25, -1.0], lens=46)
chk('S02', C2, {**{f'p{i}': add(p, [0, 2.2, 0]) for i, p in enumerate(PS2)}, **{f'f{i}': p for i, p in enumerate(PS2)}, 'cy': add(CY1, [0, 1.85, 0]), 'cyWF': add(CY1, [0, 0, 0.7])})
pas2 = []
for i, p in enumerate(PS2):
    ts = r(PT2[i] - 0.1); a = add(p, [0.55, 0, 0.15])
    ks = [k(0.0, clip='walk'), k(0.0, to=p, dur=ts, clip='walk', ease='linear', params={'freq': 2.0}), k(ts, clip='stand', blend=0.06), k(ts, face=-20, turn=0.08), k(0.0, look='camera'), TK(0.0, face=CALM, d=0.0),
          TK(ts, sq=(1.12, 0.88, 1.0), bend={'spine': SP(-0.15)}, d=0.04, e='out', keep=True), *GUILT(PT2[i]), TK(r(PT2[i] + 0.3), bend={'spine': SP(-0.05)}, d=0.1, keep=True),
          *blink(r(PT2[i] + 0.55), WORRY), *BREATHE(r(PT2[i] + 0.3), D2, 0.35)]
    pas2.append(act(f'passant{i + 1}', a, -105, 'walk', 'neutral', keys=ks))
kcy = [k(0.0, clip='ride', params={'cadence': 1.6}), k(0.0, to=CY1, dur=BRAKE2, clip='ride', ease='out', params={'cadence': 1.6}), k(BRAKE2, clip='ride', params={'cadence': 0.0}, blend=0.1),
       k(r(BRAKE2 - 0.06), face=29, turn=0.14), k(0.0, look='camera'), TK(0.0, face=CALM, d=0.0),   # the skid: the back wheel slides out, never a fall
       TK(r(BRAKE2 - 0.05), face={'lid': 0.0, 'mouth': 'clench', 'brow': 0.9}, sq=(1.15, 0.88, 1.0), bend={'spine': SP(0.2)}, d=0.05, e='out', keep=True), TK(r(BRAKE2 + 0.1), sq=(0.95, 1.06, 1.0), bend={'spine': SP(-0.45)}, d=0.07, keep=True),   # thrown forward, then sits up
       *GUILT(PT2[3], bend={'spine': SP(-0.5)}), TK(r(PT2[3] + 0.3), sq=(1, 1, 1), d=0.1, keep=True), *blink(r(PT2[3] + 0.5), WORRY), *BREATHE(r(PT2[3] + 0.3), D2, 0.35)]
st.shot('S02', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[*pas2, act('cycliste', CY0, 0, 'ride', 'neutral', keys=kcy)],
        props=[P('sol2', 'moGround', pos=[0, 0, 0]), P('facade2', 'moFacade', pos=[0, 0, -3.4], opts={'w': 14}),
               P('velo2', 'bicycle', pos=CY0, rot=[0, -1.5708, 0], keys=[k(0.0, to=CY1, dur=BRAKE2, ease='out'), k(r(BRAKE2 - 0.06), rotTo=[0, -1.0708, 0], dur=0.14), k(BRAKE2, squash=[0.94, 1.06, 1.0], dur=0.3)]),
               *[DROP(f'goutte2_{i + 1}', f'passant{i + 1}', PT2[i]) for i in range(3)], DROP('goutte2_c', 'cycliste', PT2[3])], cams=[C2])
for t in PT2: st.cue('sfx:pop', 'S02', t, 0.15)
st.cue('sfx:brake', 'S02', r(BRAKE2 - 0.08), 0.3)

# ================================================================= S03
# 3: a low shot of a plain police-station front: citizens in a zigzag queue running out of frame, each holding a signed sheet at chest height; the
#    officer at the door stamps the sheet the first one holds up vertically to his face, stamp, stamp; beside him a pile of signed sheets reaches his
#    shoulder. AVEUX card
D3 = st.dur('S03'); ST3 = [0.45, 0.85, 1.3]
OF3 = [0.5, 0, 0.45]; ORY3 = -70
Q3 = [[-0.1, 0, 0.75], [-0.75, 0, 0.75], [-0.8, 0, 1.5], [-0.1, 0, 1.5]]   # (round 1) a real zigzag: a lane of barriers that turns back on itself, seen from above
SH3 = off(Q3[0], 70, 0.32, 0.0, 1.75)
C3 = cam(0.0, [0.4, 3.0, 6.4], [0.39, 2.95, 6.15], [0.12, 1.25, 0.9], [0.12, 1.25, 0.9], lens=40)
chk('S03', C3, {'offTop': add(OF3, [0, 2.15, 0]), 'pileTop': [0.85, 1.5, 0.05], 'sheet': SH3, **{f'q{i}': add(p, [0, 2.1, 0]) for i, p in enumerate(Q3)}, 'door': [0.6, 2.9, 0.0]})
STAMP3 = off(OF3, ORY3, 0.32, 0.25, 1.45)
ko3 = [k(0.0, clip='stand'), k(0.0, look=HEAD(Q3[0], 1.9)), TK(0.0, {'R': R5(add(STAMP3, [0, 0.35, 0.05])), 'L': R5(off(OF3, ORY3, 0.25, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, STERN, d=0.0)]
for j, t in enumerate(ST3):
    ko3 += [TK(r(t - 0.12), {'R': R5(add(SH3, [0.12, 0.25, 0.08]))}, d=0.08, e='out', keep=True), TK(t, {'R': R5(add(SH3, [0.05, -0.05 + 0.05 * j, 0.06]))}, sq=(1.12, 0.9, 1.12) if j % 2 == 0 else (0.94, 1.08, 0.94), d=0.04, e='in', keep=True),
            TK(r(t + 0.12), {'R': R5(add(SH3, [0.12, 0.3, 0.1]))}, sq=(1, 1, 1), d=0.08, keep=True)]
ko3 += [*blink(1.6, STERN), *BREATHE(1.7, D3, 0.4)]
qs3 = []
for i, p in enumerate(Q3):
    ry = 70 if i == 0 else (90 if i == 1 else -90)   # the second row faces back along the lane
    if i == 0: hand = TK(0.0, {'R': R5(add(SH3, [-0.12, -0.12, -0.03])), 'L': R5(add(SH3, [0.12, -0.12, -0.03]))}, {'R': 'pinch', 'L': 'pinch'}, WORRY, d=0.0)   # held up vertically to his face
    else: hand = TK(0.0, {'R': R5(off(p, ry, 0.35, 0.15, 1.3)), 'L': R5(off(p, ry, 0.35, -0.15, 1.3))}, {'R': 'pinch', 'L': 'pinch'}, WORRY, d=0.0)
    ks = [k(0.0, clip='stand'), k(0.0, look=HEAD(OF3, 1.9)), hand, *[TK(t, sq=(1.06, 0.94, 1.06), d=0.04, e='out', keep=True) for t in ST3 if i == 0], *blink(r(0.5 + 0.25 * i), WORRY), *BREATHE(r(0.1 * i), D3, 0.45)]
    qs3.append(act(f'citoyen{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S03', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.7]},
        actors=[act('agent', OF3, ORY3, 'stand', 'neutral', keys=ko3), *qs3],
        props=[P('sol3', 'moGround', pos=[0, 0, 0], opts={'color': '#D9CDB4'}), P('commissariat3', 'moStation', pos=[0.6, 0, -0.4], opts={'doorX': 0.0}),
               P('feuille3', 'moSheet', on={'actor': 'citoyen1', 'hand': 'R', 'offset': [0.1, 0.12, 0.05], 'rot': [0, 0, 0]}, opts={'stampAt': ST3, 'seed': 2}),
               *[P(f'feuille3_{i + 2}', 'moSheet', on={'actor': f'citoyen{i + 2}', 'hand': 'R', 'offset': [0.12, 0.05, 0.06], 'rot': [0, 0, 0]}, opts={'seed': i + 3, 'w': 0.26, 'h': 0.34}) for i in range(3)],
               P('tampon3', 'moStamp', on={'actor': 'agent', 'hand': 'R', 'offset': [0, -0.12, 0.05]}, scale=1.5, keys=[k(t, squash=[1.25, 0.7, 1.25], dur=0.2) for t in ST3]),
               P('pile3', 'moPile', pos=[0.85, 0, 0.05], ry=-20, opts={'h': 1.5}, keys=[k(t, squash=[1.08, 0.9, 1.08], dur=0.3) for t in ST3]),
               P('barrieres3', 'moBarrier', opts={'lines': [[-0.45, 1.12, 0.9, 1.12], [-1.35, 1.88, 0.9, 1.88], [-1.35, 0.38, -1.35, 1.88]]}),
               P('casquette3', 'moCap', on={'actor': 'agent', 'joint': 'head', 'offset': [0, 0.3, 0]})], cams=[C3])
for t in ST3: st.cue('thud', 'S03', t, 0.35)
st.card('S03', 'AVEUX', at=st.at('S03', 'L03', 2))

# ================================================================= S04
# 4: a landing: a generic official in a dark suit and a plain peaked cap (no badge, no sash) rings a neighbour's door, a sweat drop on his brow, head
#    lowered, holding out a big bright-orange drill with both mittens; the neighbour steps out (on the open side, face to us) and takes it, eyes popping
D4 = st.dur('S04'); RING4 = 0.12; OPEN4 = 0.35; GIVE4 = r(st.at('S04', 'L04', 9) - 0.1)
LD = [0, 0, 0]; DOOR4 = add(LD, [0.55, 0, -1.5]); PF4 = add(LD, [1.5, 0, -1.0]); PRY4 = -28; NB0 = add(DOOR4, [0.0, 0, -0.7]); NB4 = add(LD, [0.6, 0, -0.95]); NRY4 = 40
DR4 = off(PF4, PRY4, 0.45, 0.0, 1.25); BELL4 = add(DOOR4, [0.72, 1.4, 0.06])
C4 = cam(0.0, [0.9, 1.5, 3.4], [0.88, 1.5, 3.2], [1.0, 1.6, -1.0], [1.0, 1.61, -1.0], lens=46)
chk('S04', C4, {'pfTop': add(PF4, [0, 2.4, 0]), 'nbTop': add(NB4, [0, 2.2, 0]), 'drill': DR4, 'doorTop': add(DOOR4, [0, 2.2, 0]), 'bell': BELL4})
kp4 = [k(0.0, clip='stand'), k(0.0, look=HEAD(off(PF4, PRY4, 1.6, 0.3, 0), 1.2)),   # ashamed: eyes on the floor in front of him, face to us
        TK(0.0, {'R': R5(add(BELL4, [0.1, 0.0, 0.12])), 'L': R5(add(DR4, [-0.05, -0.08, 0]))}, {'R': 'point', 'L': 'grip'}, WORRY, bend={'spine': SP(0.1), 'neck': SP(0.12)}, d=0.0),   # head lowered
       TK(RING4, {'R': R5(add(BELL4, [0.0, 0.0, 0.04]))}, d=0.05, e='in', keep=True), TK(r(RING4 + 0.25), {'R': R5(add(DR4, [0.08, -0.08, 0]))}, {'R': 'grip'}, d=0.18, keep=True),   # rings, then both mittens on the drill
       TK(r(OPEN4 + 0.25), sq=(0.96, 1.04, 0.96), d=0.1, keep=True), *BREATHE(0.5, GIVE4, 0.3, 0.025),   # sweating it out, quick breaths
       TK(GIVE4, {'R': R5(add(DR4, [0.1, 0.0, 0.0])), 'L': R5(add(DR4, [-0.06, 0.0, 0.0]))}, bend={'spine': SP(0.3), 'neck': SP(0.15)}, d=0.15, keep=True),   # held out, bowing
       TK(r(GIVE4 + 0.3), {'R': R5(off(PF4, PRY4, 0.2, 0.3, 1.0)), 'L': R5(off(PF4, PRY4, 0.2, -0.3, 1.0))}, {'R': 'rest', 'L': 'rest'}, bend={'spine': SP(0.1), 'neck': SP(0.12)}, d=0.2, keep=True),
       *GUILT(r(GIVE4 + 0.45), bend={'spine': SP(0.05), 'neck': SP(0.1)}), *blink(1.2, WORRY), *blink(r(GIVE4 + 0.9), WORRY)]
kn4 = [k(0.0, clip='stand'), k(r(OPEN4 + 0.15), to=NB4, dur=0.45, clip='walk', ease='out', params={'freq': 2.0}), k(r(OPEN4 + 0.6), clip='stand', blend=0.1), k(r(OPEN4 + 0.5), face=NRY4, turn=0.15),
       k(0.0, look='camera'), k(r(OPEN4 + 0.6), look=HEAD(PF4, 1.9), lookDur=0.15),
       TK(0.0, {'R': R5(off(NB0, 0, 0.3, 0.3, 1.0)), 'L': R5(off(NB0, 0, 0.2, -0.3, 1.0))}, {'R': 'rest', 'L': 'rest'}, CALM, d=0.0),
       *[TK(r(OPEN4 + 0.15 + 0.2 * j), {'R': R5(off(lerp3(NB0, NB4, min(1.0, 0.2 * j / 0.45)), 0, 0.15, 0.3, 1.0)), 'L': R5(off(lerp3(NB0, NB4, min(1.0, 0.2 * j / 0.45)), 0, 0.15, -0.3, 1.0))}, d=0.2, e='linear', keep=True) for j in range(4)],   # the hands walk out with him
       TK(r(OPEN4 + 0.85), {'R': R5(off(NB4, NRY4, 0.25, 0.3, 1.0)), 'L': R5(off(NB4, NRY4, 0.2, -0.3, 1.0))}, d=0.15, keep=True),
       k(r(GIVE4 - 0.4), look=HEAD(DR4, 1.7), lookDur=0.15),
       TK(r(GIVE4 + 0.12), {'R': R5(add(DR4, [0.1, 0.02, 0.0])), 'L': R5(add(DR4, [-0.08, 0.02, 0.0]))}, {'R': 'grip', 'L': 'grip'}, d=0.1, keep=True),
       TK(r(GIVE4 + 0.18), face={**POP, 'jaw': 0.9}, scl={'head': [0.88, 1.18, 0.9]}, sq=(0.92, 1.1, 0.92), d=0.04, e='out', keep=True), k(r(GIVE4 + 0.2), look='camera', lookDur=0.06),   # the take: eyes out on stalks, jaw down
       TK(r(GIVE4 + 0.5), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.8, 'pop': 0.3}, scl={'head': [1, 1, 1]}, sq=(1, 1, 1), d=0.12, keep=True),
       TK(r(GIVE4 + 0.55), {'R': R5(off(NB4, NRY4, 0.4, 0.15, 1.25)), 'L': R5(off(NB4, NRY4, 0.4, -0.1, 1.2))}, d=0.15, keep=True), *blink(r(GIVE4 + 0.9), CALM), *BREATHE(1.2, D4, 0.45)]
st.shot('S04', 'whiteVoid', setOpts={'color': '#E8E0D0'}, look={'sunDir': [0.3, 0.9, 0.8]},
        actors=[act('prefet', PF4, PRY4, 'stand', 'neutral', keys=kp4), act('voisin3', NB0, 0, 'stand', 'neutral', keys=kn4)],
        props=[P('palier4', 'moRoom', pos=LD, opts={'w': 5, 'd': 3, 'h': 2.8, 'wall': '#E8D8C0', 'floor': '#B9A58A', 'doorX': 0.55}), P('interieur4', 'moRoom', pos=add(DOOR4, [0, 0, -1.55]), opts={'w': 3, 'd': 3, 'h': 2.8, 'wall': '#D9E4D0', 'floor': '#A8927A'}), P('porte4', 'moDoor', pos=DOOR4, opts={'open': [[0, 0], [OPEN4, 0], [r(OPEN4 + 0.25), 0.9]], 'color': '#7A5A3C'}),
               P('perceuse4', 'moDrill', pos=DR4, ry=-PRY4 + 90, keys=[k(r(GIVE4 + 0.14), attach='voisin3', hand='R', offset=[0.0, -0.06, 0.08], rot=[0, 1.5708, 0])]),
               P('casquette4', 'moCap', on={'actor': 'prefet', 'joint': 'head', 'offset': [0, 0.54, 0]}, scale=0.75, opts={'color': '#22283A'}),
               DROP('goutte4', 'prefet', 0.3, (-0.24, 0.3, 0.02), 0.9)], cams=[C4])
st.cue('sfx:bell', 'S04', RING4, 0.3); st.cue('sfx:squeak', 'S04', OPEN4, 0.2); st.cue('sfx:gasp', 'S04', r(GIVE4 + 0.18), 0.2)

# ================================================================= S05
# 5: a council room, two straight benches one behind the other, a plain coloured panel: instead of a gavel the speaker slowly raises one finger to his
#    lips; the four councillors copy him at once. SILENCE card
D5 = st.dur('S05'); SH5 = r(st.at('S05', 'L05', 3) - 0.1); COPY5 = r(st.at('S05', 'L05', 7) - 0.15)
SPK = [-0.7, 0, -0.6]; SRY5 = 25
CO5 = [[-0.05, 0, -0.15], [0.55, 0, -0.15], [0.25, 0.45, -1.45], [0.85, 0.45, -1.45]]   # (round 1) two straight rows (the bench was a wide strip of empty wood)
C5 = cam(0.0, [0.15, 1.85, 6.0], [0.15, 1.85, 5.75], [0.08, 1.68, -0.7], [0.08, 1.69, -0.7], lens=38)
chk('S05', C5, {'spkTop': add(SPK, [0, 2.35, 0]), 'c0': add(CO5[0], [0, 1.65, 0]), 'c3': add(CO5[3], [0.3, 1.65, 0]), 'panel': [0.3, 3.75, -2.9], 'bench': [1.05, 0.9, 0.6]})
LIP = lambda p, ry, y=1.68: off(p, ry, 0.33, 0.0, y)
ks5 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, HANDS(SPK, SRY5, 0.4, 0.25, 1.08, 0.4, -0.25, 1.08), {'R': 'rest', 'L': 'rest'}, GRAVE, d=0.0),
       TK(0.5, sq=(1.01, 0.99, 1.01), bend={'spine': SP(0.05, 0.05)}, d=0.4, keep=True), k(0.6, look=HEAD(CO5[1], 1.6), lookDur=0.3), k(r(SH5 - 0.2), look='camera', lookDur=0.2),   # he looks over the room
       TK(SH5, {'R': R5(off(SPK, SRY5, 0.35, 0.15, 1.5))}, {'R': 'point'}, bend={'spine': SP(0.0)}, d=0.45, keep=True), TK(r(SH5 + 0.5), {'R': R5(LIP(SPK, SRY5, 1.9))}, face={**GRAVE, 'lid': 0.5}, d=0.4, e='inOut', keep=True),   # slowly, the finger to his lips
       TK(r(SH5 + 0.95), sq=(0.97, 1.04, 0.97), d=0.2, keep=True), *BLINKS(0.6, D5, GRAVE, 1.9), *BREATHE(r(SH5 + 1.0), D5, 0.45)]
cs5 = []
for i, p in enumerate(CO5):
    lk = HEAD(CO5[(i + 1) % 4], 1.6 + p[1])
    ks = [k(0.0, clip='sit'), k(0.0, look=HEAD(SPK, 1.9)), TK(0.0, HANDS(p, 0, 0.45, 0.25, p[1] + 0.92, 0.45, -0.25, p[1] + 0.92), {'R': 'rest', 'L': 'rest'}, CALM, d=0.0),
          k(r(0.3 + 0.25 * i), look=lk, lookDur=0.2), k(r(0.75 + 0.2 * i), look=HEAD(SPK, 1.9), lookDur=0.2),   # (round 1) they glance at each other, shift, fidget
          TK(r(0.4 + 0.3 * i), sq=(1.03, 0.97, 1.03), bend={'spine': SP(0.04, 0.06 * (1 if i % 2 else -1))}, d=0.3, keep=True), TK(r(1.0 + 0.3 * i), sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.3, keep=True),
          k(r(SH5 + 0.3 + 0.1 * i), look=HEAD(SPK, 1.9), lookDur=0.15), TK(r(SH5 + 0.35), face={'lid': 0.1, 'mouth': 'line', 'brow': 0.7}, d=0.1, keep=True),
          TK(r(COPY5 - 0.06), sq=(1.06, 0.94, 1.06), d=0.05, keep=True),   # anticipation
          TK(r(COPY5 + 0.02 * i), {'R': R5(LIP(p, 0, p[1] + 1.42))}, {'R': 'point'}, face={'lid': 0.1, 'mouth': 'clench', 'brow': 0.8}, sq=(0.9, 1.12, 0.9), d=0.05, e='out', keep=True),   # all at once: snap!
          TK(r(COPY5 + 0.15 + 0.02 * i), sq=(1, 1, 1), face={'lid': 0.2, 'mouth': 'clench', 'brow': 0.6}, d=0.08, keep=True), k(r(COPY5 + 0.3), look='camera', lookDur=0.15),
          k(r(COPY5 + 0.9 + 0.12 * i), look=lk, lookDur=0.15), k(r(COPY5 + 1.3 + 0.1 * i), look='camera', lookDur=0.15),
          *blink(r(0.4 + 0.3 * i), CALM), *blink(r(1.8 + 0.2 * i), CALM), *blink(r(COPY5 + 0.6 + 0.1 * i), {'lid': 0.2, 'mouth': 'clench', 'brow': 0.6}), *BREATHE(r(0.05 * i), D5, 0.5)]
    cs5.append(act(f'conseiller{i + 1}', p, 0, 'sit', 'neutral', keys=ks))
st.shot('S05', 'whiteVoid', setOpts={'color': '#E8DCC8'}, look={'sunDir': [0.3, 0.9, 0.8]},
        actors=[act('orateur', SPK, SRY5, 'stand', 'neutral', keys=ks5), *cs5],
        props=[P('salle5', 'moRoom', pos=[0, 0, -1.0], opts={'w': 6, 'd': 4.4, 'h': 4.2, 'wall': '#E8DCC8', 'floor': '#9C7B58'}),
               P('banc5', 'moCouncil', pos=[0.25, 0, 0], opts={'w': 1.6, 'lecternX': -0.95, 'lecternZ': -0.3, 'panel': False}),
               P('banc5b', 'moCouncil', pos=[0.55, 0.45, -1.3], opts={'w': 1.6, 'riser': 0.45, 'lecternX': None, 'panel': '#3E6A9A', 'panelW': 2.2, 'panelX': -0.25, 'panelY': 2.55})], cams=[C5])
st.cue('sfx:ticks', 'S05', 0.2, 0.15); st.card('S05', 'SILENCE', at=st.at('S05', 'L05', 7))

# ================================================================= S06
# 6: a street: a fire engine glides past (the camera rides along), its siren on a mast wrapped in a big knitted striped tea cosy, centre top of the
#    frame; two firemen ride its side step, a finger on their lips, mouthing « pin-pon »
D6 = st.dur('S06'); PIN6 = r(st.at('S06', 'L06', 3) - 0.05)
T0, T1 = [-1.6, 0, -0.6], [2.4, 0, -0.6]
def tr6(t): return lerp3(T0, T1, min(1.0, t / D6))
FM6 = [[-1.4, 0.55, 0.62], [-0.4, 0.55, 0.62]]   # on the side step, relative to the truck
CD6 = [-0.9, 2.1, 6.6]; CL6 = [-0.9, 2.22, 0.6]
C6 = cam(0.0, add(T0, CD6), add(T1, CD6), add(T0, CL6), add(T1, CL6), lens=44)   # (round 1) tracking with the truck: the cosy stays centre top
chk('S06', C6, {'cosyTop': add(T0, [-0.9, 3.4, 0.2]), 'fm0': add(T0, [-1.4, 2.75, 1.24]), 'fm1': add(T0, [-0.4, 2.75, 1.24])})
SHH = {'R': ['face', -0.03, 0.23, 0.06, 1, 0.02]}   # (round 1) the index on the lips, a touch on his own face: it follows the head (the world reach dropped)
fms6 = []
for i, rel in enumerate(FM6):
    p0, p1 = add(T0, [rel[0], rel[1], rel[2] + 0.62]), add(T1, [rel[0], rel[1], rel[2] + 0.62])
    ks = [k(0.0, clip='stand'), k(0.0, to=p1, dur=D6, clip='stand', ease='linear', face='keep'), k(0.0, look='camera'), TK(0.0, face=CALM, d=0.0)]
    ks += [TK(0.0, touch=SHH, hands={'R': 'point', 'L': 'grip'}, d=0.0, keep=True),
           *[TK(r(0.2 * j), {'L': R5(add(lerp3(p0, p1, min(1.0, 0.2 * j / D6)), [0.3, 1.0, -0.15]))}, d=0.2, e='linear', keep=True) for j in range(int(D6 / 0.2) + 2)],   # the other mitten on the rail (keyed along the ride)
           TK(r(PIN6 - 0.1), sq=(1.04, 0.96, 1.04), d=0.06, keep=True), *TALK(r(PIN6 + 0.03 * i), {'lid': 0.4, 'mouth': 'line', 'brow': 0.5}, 2, 0.1), TK(r(PIN6 + 0.45), face={'lid': 0.4, 'mouth': 'line', 'brow': 0.5}, sq=(1, 1, 1), d=0.1, keep=True),
           k(r(0.5 + 0.2 * i), look=HEAD(add(T0, [-0.9, 0, 0.2]), 3.2), lookDur=0.2), k(r(PIN6 - 0.15), look='camera', lookDur=0.15),   # a glance up at the muffled siren
           *blink(r(0.35 + 0.3 * i), CALM), *blink(r(1.5 + 0.1 * i), CALM), *BREATHE(0.1, D6, 0.45)]
    fms6.append(act(f'pompier{i + 1}', p0, 15, 'stand', 'neutral', keys=ks))
st.shot('S06', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=fms6,
        props=[P('sol6', 'moGround', pos=[0, 0, 0], opts={'kerb': 1.2}), P('facade6', 'moFacade', pos=[0, 0, -3.4], opts={'w': 16, 'color': '#F2DCCB'}),
               P('camion6', 'moFireTruck', pos=T0, opts={'speed': r(4.0 / D6), 'cosyX': -0.9}, keys=[k(0.0, to=T1, dur=D6, ease='linear')])], cams=[C6])
st.cue('sfx:whistle', 'S06', PIN6, 0.08); st.cue('engine', 'S06', 0.0, 0.1)

# ================================================================= S07
# 7: the pavement in front of the hero's building: two binmen in orange tiptoe in exaggerated slow motion, carrying the bin between them like a
#    sleeping baby
D7 = st.dur('S07')
BM0, BM1 = [1.6, 0, -0.2], [-0.9, 0, -0.2]
def bin7(t): return lerp3(BM0, BM1, min(1.0, max(0.0, t / (D7 - 0.1))))
C7 = cam(0.0, [0.2, 1.4, 4.3], [0.15, 1.4, 4.1], [0.2, 1.5, -0.4], [0.2, 1.5, -0.4], lens=48)
chk('S07', C7, {'b0start': add(BM0, [0.7, 2.1, 0]), 'b1end': add(BM1, [-0.7, 2.1, 0]), 'bin': add(bin7(1.4), [0, 1.15, 0]), 'feet': add(BM0, [0, 0, 0])})
bms7 = []
for i, sx in enumerate([1, -1]):
    p0, p1 = add(BM0, [0.55 * sx, 0, 0]), add(BM1, [0.55 * sx, 0, 0])
    ks = [k(0.0, clip='tiptoe', params={'freq': 0.55}), k(0.0, to=p1, dur=r(D7 - 0.1), clip='tiptoe', ease='linear', face='keep', params={'freq': 0.55}), k(0.0, look=HEAD(add(bin7(0.5), [0, 0, 0]), 1.6)), TK(0.0, face={'lid': 0.5, 'mouth': 'line', 'brow': 0.6}, d=0.0),
          *[TK(r(0.2 * j), {'R': R5(add(bin7(0.2 * j), [0.28 * sx, 1.12, 0.22])), 'L': R5(add(bin7(0.2 * j), [0.28 * sx, 1.02, -0.22]))}, {'R': 'open', 'L': 'open'}, sq=(1, 1.04, 1) if j % 2 else (1.02, 0.98, 1.02), d=0.2, e='linear', keep=True) for j in range(int(D7 / 0.2) + 2)],   # cradling it, keyed along the walk
          k(1.2, look='camera', lookDur=0.3), k(1.9, look=HEAD(bin7(2.0), 1.6), lookDur=0.3), *blink(r(0.8 + 0.4 * i), {'lid': 0.5, 'mouth': 'line', 'brow': 0.6}), *BREATHE(0.1, D7, 0.6, 0.02)]
    bms7.append(act(f'eboueur{i + 1}', p0, -90, 'tiptoe', 'neutral', keys=ks))
st.shot('S07', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=bms7,
        props=[P('sol7', 'moGround', pos=[0, 0, 0], opts={'kerb': 1.6}), P('facade7', 'moFacade', pos=[0, 0, -1.6], opts={'w': 14, 'color': '#EFE6D2'}),
               P('poubelle7', 'moBin', pos=add(BM0, [0, 0.72, 0]), rot=[1.35, -1.5708, 0], scale=0.85, opts={'blanket': True}, keys=[k(0.0, to=add(BM1, [0, 0.72, 0]), dur=r(D7 - 0.1), ease='linear'), *[k(r(0.4 * j), rotTo=[1.35, -1.5708, 0.12 if j % 2 else -0.12], dur=0.4) for j in range(int(D7 / 0.4) + 1)]])], cams=[C7])
st.cue('sfx:stepSoft', 'S07', 0.3, 0.15); st.cue('sfx:stepSoft', 'S07', 1.2, 0.15); st.cue('sfx:stepSoft', 'S07', 2.1, 0.15)

# ================================================================= S08
# 8: a farmyard at sunrise, orange sky: a farmer lowers a tall glass dome over a rooster (big in frame) on a fence post; the rooster crows three times
#    and each time the dome fogs up opaque white with a squash, then clears; the farmer gives one satisfied nod, his hat a beat behind
D8 = st.dur('S08'); DOWN8 = 0.3; CROW8 = [0.45, 0.83, 1.21]; NOD8 = 1.42
POST = [0.0, 0, 0.0]; ROO = [0.0, 1.0, 0.0]; FA8 = [0.8, 0, -0.55]; FRY8 = -55; DR8, DH8 = 0.62, 1.35   # (round 1) the dome taller than the crowing rooster
DOME0, DOME1 = add(ROO, [0.12, 1.1, 0.08]), add(ROO, [0, 0.0, 0])
C8 = cam(0.0, [0.2, 1.7, 4.6], [0.19, 1.7, 4.4], [0.15, 1.7, -0.2], [0.15, 1.71, -0.2], lens=44)
chk('S08', C8, {'domeTop@end': add(ROO, [0, DH8 + 0.07, 0]), 'domeL': add(ROO, [-DR8, 0, 0]), 'rooster': add(ROO, [0, 0.4, 0]), 'farmer': add(FA8, [0, 2.45, 0]), 'post': [0, 0.3, 0]})
kf8 = [k(0.0, clip='stand'), k(0.0, look=HEAD(ROO, 1.5)), TK(0.0, {'R': R5(add(DOME0, [-0.35, 0.5, 0])), 'L': R5(add(DOME0, [0.35, 0.5, 0]))}, {'R': 'grip', 'L': 'grip'}, CALM, bend={'spine': SP(0.1)}, d=0.0),
       TK(DOWN8, {'R': R5(add(DOME1, [-0.32, DH8 * 0.8, 0.05])), 'L': R5(add(DOME1, [0.32, DH8 * 0.8, 0.05]))}, bend={'spine': SP(0.25)}, d=DOWN8, e='inOut', keep=True),   # down over it...
       TK(r(DOWN8 + 0.05), sq=(1.06, 0.94, 1.06), d=0.05, keep=True), TK(r(DOWN8 + 0.2), {'R': R5(off(FA8, FRY8, 0.25, 0.3, 1.0)), 'L': R5(off(FA8, FRY8, 0.25, -0.3, 1.0))}, {'R': 'rest', 'L': 'rest'}, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.18, keep=True),
       *[TK(r(c + 0.06), sq=(0.97, 1.03, 0.97), face={'lid': 0.2, 'mouth': 'line', 'brow': 0.4}, d=0.05, keep=True) for c in CROW8],   # a little start at each crow
       TK(r(NOD8 - 0.06), bend={'neck': SP(-0.15)}, face=SMUG, d=0.06, keep=True), TK(NOD8, bend={'neck': SP(0.45)}, sq=(1.03, 0.97, 1.03), d=0.07, e='out', keep=True), TK(r(NOD8 + 0.16), bend={'neck': SP(-0.05)}, sq=(1, 1, 1), d=0.1, keep=True),   # one satisfied nod
       k(r(NOD8 + 0.12), look='camera', lookDur=0.1), *blink(r(CROW8[0] + 0.15), CALM), *BREATHE(0.6, D8, 0.4)]
st.shot('S08', 'whiteVoid', setOpts={'color': '#F4A25A'}, look={'sunDir': [-0.6, 0.4, 0.7]},
        actors=[act('fermier', FA8, FRY8, 'stand', 'neutral', keys=kf8)],
        props=[P('pre8', 'moGround', pos=[0, 0, 0], opts={'color': '#8CB060'}), P('grange8', 'moBarn', pos=[-2.6, 0, -4.0], ry=15), P('poteau8', 'moFence', pos=POST, opts={'h': 1.0, 'w': 5}),
               P('coq8', 'moRooster', pos=ROO, ry=-20, scale=1.0, opts={'crow': CROW8}),
               P('cloche8', 'moDome', pos=DOME0, opts={'r': DR8, 'h': DH8, 'fog': [r(c + 0.05) for c in CROW8], 'squash': [DOWN8] + [r(c + 0.05) for c in CROW8]}, keys=[k(0.0, to=DOME1, dur=DOWN8, ease='inOut')]),
               P('chapeau8', 'moHat', on={'actor': 'fermier', 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'nod': [NOD8]})], cams=[C8])
st.cue('sfx:clink', 'S08', DOWN8, 0.4); [st.cue('sfx:static', 'S08', c, 0.1) for c in CROW8]

# ================================================================= S09
# 9: a café terrace, two customers and a waiter: the customers silently slide big sheets of scribbles across the table to each other; the waiter takes
#    the order by holding up his own big sheet
D9 = st.dur('S09'); SL9 = [0.25, 0.95]
TB9 = [0.0, 0, 0.0]; CU9 = [[-0.75, 0, 0.0], [0.75, 0, 0.0]]; WT9 = [0.25, 0, -0.95]
C9 = cam(0.0, [0.3, 1.55, 3.7], [0.28, 1.55, 3.5], [0.05, 1.4, -0.2], [0.05, 1.41, -0.2], lens=48)
chk('S09', C9, {'wt': add(WT9, [0, 2.15, 0]), 'c0': add(CU9[0], [-0.3, 1.6, 0]), 'c1': add(CU9[1], [0.3, 1.6, 0]), 'sheetUp': add(WT9, [0.0, 1.75, 0.35])})
SA, SB = [-0.3, 0.77, 0.02], [0.3, 0.77, -0.02]
kc9 = []
for i, p in enumerate(CU9):
    ry = 90 if i == 0 else -90; me, you = (SA, SB) if i == 0 else (SB, SA); tslide = SL9[i]
    ks = [k(0.0, clip='sit'), k(0.0, look=HEAD(CU9[1 - i], 1.5)), TK(0.0, HANDS(p, ry, 0.4, 0.2, 0.8, 0.4, -0.2, 0.8), {'R': 'rest', 'L': 'rest'}, CALM, d=0.0),
          TK(r(tslide - 0.1), {'R': R5(add(me, [0, 0.05, 0]))}, {'R': 'open'}, d=0.1, keep=True), TK(r(tslide + 0.35), {'R': R5(add(you, [0.0, 0.05, 0]))}, d=0.35, keep=True),   # slides it across...
          TK(r(tslide + 0.5), {'R': R5(off(p, ry, 0.4, 0.2, 0.8))}, {'R': 'rest'}, d=0.15, keep=True),
          TK(r(SL9[1 - i] + 0.4), face={'lid': 0.0, 'mouth': 'line', 'brow': 0.9}, sq=(0.94, 1.08, 0.94), d=0.05, e='out', keep=True), TK(r(SL9[1 - i] + 0.6), face=CALM, sq=(1, 1, 1), d=0.1, keep=True),   # reads it: brows up
          *blink(r(0.5 + 0.5 * i), CALM), *BREATHE(0.1, D9, 0.45)]
    kc9.append(act(f'client{i + 1}', p, ry, 'sit', 'neutral', keys=ks))
kw9 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(off(WT9, 0, 0.35, 0.28, 1.65)), 'L': R5(off(WT9, 0, 0.35, -0.28, 1.65))}, {'R': 'pinch', 'L': 'pinch'}, {'lid': 0.4, 'mouth': 'line', 'brow': 0.3}, d=0.0),
       TK(1.3, sq=(0.96, 1.05, 0.96), d=0.1, keep=True), TK(1.45, sq=(1, 1, 1), d=0.1, keep=True), *blink(0.8, CALM), *BREATHE(0.1, D9, 0.5)]
st.shot('S09', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[*kc9, act('serveur', WT9, 0, 'stand', 'neutral', keys=kw9)],
        props=[P('sol9', 'moGround', pos=[0, 0, 0], opts={'color': '#D9CDB4'}), P('cafe9', 'moCafeFront', pos=[0, 0, -2.2], opts={'w': 8}), P('table9', 'moCafeTable', pos=TB9, opts={'chairs': True}),
               P('feuilleA9', 'moScribble', pos=SA, rot=[-1.5708, 0, 0], opts={'seed': 1, 'w': 0.36, 'h': 0.26}, keys=[k(SL9[0], to=SB, dur=0.35, ease='inOut')]),
               P('feuilleB9', 'moScribble', pos=add(SB, [0.0, 0.004, 0.18]), rot=[-1.5708, 0, 0], opts={'seed': 4, 'w': 0.36, 'h': 0.26}, keys=[k(SL9[1], to=add(SA, [0.0, 0.004, 0.18]), dur=0.35, ease='inOut')]),
               P('feuilleW9', 'moScribble', pos=off(WT9, 0, 0.42, 0.0, 1.65), opts={'seed': 7, 'w': 0.55, 'h': 0.4}, keys=[k(1.3, squash=[1.06, 0.94, 1.0], dur=0.25)])], cams=[C9])
st.cue('sfx:paper', 'S09', SL9[0], 0.25); st.cue('sfx:paper', 'S09', SL9[1], 0.25)

# ================================================================= S10
# 10: a block of flats cut open on three flats, pale dawn blue, a warm lamp in each: both neighbours sleep in their pink earmuffs; in the middle he
#     sleeps too... then (cut, the bedroom framed exactly as in line 1) he bolts upright the very same way
D10 = st.dur('S10'); CUT10 = r(st.at('S10', 'L10', 7) - 0.12); UP10 = r(CUT10 + 0.1)
FH10 = 2.85; CW = [0, FH10, 0]; BEDS10 = [add(CW, [0.25, FH10 + 0.52, -0.35]), add(CW, [0.25, 0.52, -0.35]), add(CW, [0.25, -FH10 + 0.52, -0.35])]   # three flats one above the other: neighbour, him, neighbour
C10 = cam(0.0, [0.3, 4.3, 11.6], [0.25, 4.1, 9.3], [0.0, 4.25, -0.3], [0.1, 3.75, -0.3], lens=46, ease='inOut')   # (round 1) a slow push in on his flat: the sleepers grow
B10 = [40.0, 0, 0.0]; C10b = BEDCAM(CUT10, B10)
BEDCHK('S10b', C10b, B10)
chk('S10', C10, {'left': [-1.7, 4.2, 1.1], 'right': [1.7, 4.2, 1.1], 'top': [0, 8.55, 1.1], 'bottom': [0, 0, 1.1], 'hero': add(BEDS10[1], [0, 0.4, -0.6])})
sl10 = []
for i, (bp, nm) in enumerate([(BEDS10[0], 'voisin1'), (BEDS10[2], 'voisine2')]):
    ks = [*LIE(0.0, {'lid': 1.0, 'mouth': 'smile', 'brow': 0.2}), *BREATHE(r(0.1 + 0.2 * i), D10, 0.7, 0.03)]
    if i == 0: ks += [k(1.1, clip='sleepSide', blend=0.35), TK(1.1, sq=(1.06, 0.95, 1.06), d=0.15, keep=True), TK(1.35, sq=(1, 1, 1), d=0.2, keep=True)]   # (round 1) he rolls over in his sleep
    else: ks += [TK(0.0, {'R': R5(add(bp, [0.3, 0.15, 0.3])), 'L': R5(add(bp, [0.3, 0.15, -0.3]))}, {'R': 'rest', 'L': 'rest'}, d=0.0, keep=True), TK(1.7, sq=(1.08, 0.94, 1.08), face={'lid': 1.0, 'mouth': 'O', 'brow': 0.3}, d=0.25, keep=True), TK(2.1, sq=(1, 1, 1), face={'lid': 1.0, 'mouth': 'smile', 'brow': 0.2}, d=0.25, keep=True)]   # a big sleepy sigh
    sl10.append(act(nm, bp, 90, 'lieBack', 'neutral', keys=ks))
kh10 = [*LIE(0.0), *BREATHE(0.1, CUT10, 0.7, 0.03), *[TK(r(0.5 + 0.8 * j), sq=(1.05, 0.97, 1.05), d=0.2, keep=True) for j in range(int(CUT10 / 0.8))], *[TK(r(0.75 + 0.8 * j), sq=(1, 1, 1), d=0.3, keep=True) for j in range(int(CUT10 / 0.8))], k(CUT10, to=BEDPOS(B10), dur=0.01, clip='lieBack', face='keep'), BEDHANDS(B10, r(CUT10 + 0.02)), *SITUP(UP10),
        TK(r(UP10 + 0.3), {'R': R5(add(BEDPOS(B10), [-0.35, 0.35, 0.3])), 'L': R5(add(BEDPOS(B10), [0.35, 0.35, 0.3]))}, {'R': 'spread', 'L': 'spread'}, d=0.1, keep=True),
        *LOOKAROUND(r(UP10 + 0.45), B10, 3, 0.33), k(r(UP10 + 1.45), look='camera', lookDur=0.15), *blink(r(UP10 + 1.2), WIDE), *BREATHE(r(UP10 + 0.4), D10, 0.35)]
st.shot('S10', 'whiteVoid', setOpts={'color': DAWN}, look={'sunDir': [0.3, 0.8, 0.8]},
        actors=[*sl10, act('mecPyj', BEDS10[1], 90, 'lieBack', 'neutral', keys=kh10 + [k(CUT10, face=0, turn=0.01)])],
        props=[P('coupe10', 'moCutaway', pos=CW, opts={'pulse': 1.4}), SMEAR('trait10', B10, UP10), P('couettes10', 'moDuvet', pos=add(CW, [0.3, FH10 + 0.6, -0.35]), ry=90, opts={'w': 1.0, 'l': 0.9, 'color': '#C8A0C8'}), P('couettes10b', 'moDuvet', pos=add(CW, [0.3, -FH10 + 0.6, -0.35]), ry=90, opts={'w': 1.0, 'l': 0.9, 'color': '#A8C890'}),
               P('couettes10c', 'moDuvet', pos=add(CW, [0.3, 0.6, -0.35]), ry=90, opts={'w': 1.0, 'l': 0.9}, keys=[k(CUT10, visible=False)]),
               *BEDROOM('S10', B10), MUFFS('cacheoreilles10_1', 'voisin1'), MUFFS('cacheoreilles10_2', 'voisine2')], cams=[C10, C10b])
st.cue('engine', 'S10', r(CUT10 - 0.3), 0.2); st.cue('sfx:spring', 'S10', UP10, 0.3)

# ================================================================= S11
# 11: a rooftop ridge, a big cat and a big pigeon in the foreground, his building behind: one rumbling snore rolls in; a TV aerial and a row of shutters
#     rattle, and the cat's and the pigeon's heads turn together toward the building
D11 = st.dur('S11'); SN11 = 0.35; TURN11 = r(st.at('S11', 'L11', 5) - 0.25)
RF = [0, 0, 0]; CAT = [0.1, 0.06, 0.0]; PIG = [0.75, 0.06, 0.05]
def TURN(a0, a1): return [[0, a0], [r(TURN11 - 0.13), a0], [TURN11, r(a0 + 0.2)], [r(TURN11 + 0.1), r(a1 - 0.25)], [r(TURN11 + 0.2), r(a1 + 0.08)], [r(TURN11 + 0.3), a1]]   # (round 1) together: 4 frames of anticipation, the snap, an overshoot
C11 = cam(0.0, [0.3, 0.85, 3.1], [0.28, 0.86, 2.95], [0.35, 1.25, -1.0], [0.35, 1.26, -1.0], lens=50)
chk('S11', C11, {'cat': add(CAT, [0, 0.8, 0]), 'pig': add(PIG, [0, 0.55, 0]), 'shut': [2.0, 2.0, -4.0], 'aer': [1.2, 1.4, 0.0]})
st.shot('S11', 'whiteVoid', setOpts={'color': '#C9DCEC'}, look={'sunDir': [0.3, 0.8, 0.7]}, actors=[],
        props=[P('toit11', 'moRoof', pos=RF, opts={'len': 4.2, 'rattle': [r(SN11 + 0.1), r(SN11 + 0.5)]}), P('immeuble11', 'moFacade', pos=[3.6, -3.0, -5.0], ry=-30, opts={'w': 8, 'h': 9, 'lit': True}),
               P('volets11', 'moShutters', pos=[3.4, 3.0, -4.75], ry=-30, opts={'n': 3, 'rattle': [r(SN11 + 0.15), r(SN11 + 0.55)]}),
               P('chat11', 'moCat', pos=CAT, scale=1.25, opts={'turn': TURN(0.2, -1.0), 'flinch': [SN11]}),
               P('pigeon11', 'moPigeon', pos=PIG, scale=1.3, opts={'turn': TURN(-0.3, -1.1), 'flinch': [SN11]})], cams=[C11])
st.cue('engine', 'S11', SN11, 0.4); st.cue('sfx:rattle', 'S11', r(SN11 + 0.1), 0.25)

# ================================================================= S12
# 12: two cuts. A street: a small truck, its back to us, swings a huge boom microphone on a crane arm up the facade to one window; two technicians in big
#     headphones on its flatbed and one beside it point at it, and at the next window a neighbour in pink earmuffs leans out. Cut: the fluffy mic hangs
#     over his headboard
D12 = st.dur('S12'); CUT12 = r(st.at('S12', 'L12', 12) - 0.12); FL12 = r(st.at('S12', 'L12', 11))
TR12 = [-0.6, 0, 2.2]; TRY12 = 110; WIN12 = [1.2, 3.9, -0.05]; NBW12 = [-0.8, 3.25, 0.3]
_c12, _s12 = math.cos(math.radians(TRY12)), math.sin(math.radians(TRY12))
def W12(l): return [r(TR12[0] + l[0] * _c12 + l[2] * _s12), l[1], r(TR12[2] - l[0] * _s12 + l[2] * _c12)]   # truck coordinates -> world
def L12(w): d = [w[0] - TR12[0], w[2] - TR12[2]]; return [r(d[0] * _c12 - d[1] * _s12), w[1], r(d[0] * _s12 + d[1] * _c12)]   # world -> truck coordinates
TIP12 = [[0.0, L12([-0.2, 2.6, 2.4])], [0.5, L12([0.3, 3.1, 1.6])], [r(FL12 - 0.2), L12([1.15, 4.0, 0.62])], [r(FL12 + 0.2), L12([1.1, 3.88, 0.6])]]   # (round 1) the truck turned, its back to us: it fits and nobody hides it
TECH12 = [W12([-1.65, 0.9, 0.45]), W12([-1.15, 0.9, -0.5]), [1.45, 0, 3.7]]   # two on the flatbed, one on the pavement
C12 = cam(0.0, [0.3, 1.9, 10.4], [0.3, 1.95, 10.0], [0.25, 3.12, 0.0], [0.25, 3.17, 0.0], lens=46)
B12 = [40.0, 0, 0.0]; C12b = BEDCAM(CUT12, B12, 0.2)
chk('S12', C12, {'win': WIN12, 'nbw': add(NBW12, [0, 2.0, 0]), **{f't{i}': add(p, [0, 2.2, 0]) for i, p in enumerate(TECH12)}, 'rear': W12([-2.0, 1.0, 0.95]), 'cab': W12([2.35, 2.05, -0.95])})
BEDCHK('S12b', C12b, B12)
tk12 = []
for i, p in enumerate(TECH12):
    ry = [75, 85, -65][i]; ry0 = 10   # they turn side on to point up (in profile: their backs hid the truck)
    ks = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, HANDS(p, ry0, 0.2, 0.3, p[1] + 1.0, 0.2, -0.3, p[1] + 1.0), {'R': 'rest', 'L': 'rest'}, CALM, d=0.0),
          k(r(0.45 + 0.1 * i), face=ry, turn=0.3), k(r(0.5 + 0.1 * i), look=HEAD(WIN12, 3.9), lookDur=0.3),
          *[TK(r(0.45 + 0.1 * i + 0.2 * j), HANDS(p, ry0 + (ry - ry0) * min(1.0, j / 1.5), 0.2, 0.3, p[1] + 1.0, 0.2, -0.3, p[1] + 1.0), d=0.2, e='linear', keep=True) for j in range(3)],   # the hands turn with him
          TK(r(1.2 + 0.12 * i), {'R': R5(off(p, ry, 0.45, 0.15, p[1] + 2.15))}, {'R': 'point'}, bend={'spine': SP(-0.15)}, d=0.15, keep=True),   # all point up at it
          TK(r(FL12 - 0.1), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(0.94, 1.08, 0.94), d=0.05, e='out', keep=True), TK(r(FL12 + 0.1), face=CALM, sq=(1, 1, 1), d=0.1, keep=True),
          *BLINKS(r(0.9 + 0.3 * i), CUT12, CALM, 1.8), *BREATHE(0.1, CUT12, 0.5)]
    tk12.append(act(f'technicien{i + 1}', p, ry0, 'stand', 'neutral', keys=ks))
knb12 = [k(0.0, clip='stand'), k(0.0, look=HEAD(add(WIN12, [-1.0, 0, 1.0]), 3.9)), TK(0.0, face=CALM, bend={'spine': SP(0.25)}, d=0.0), k(r(FL12 - 0.4), look=HEAD(WIN12, 4.0), lookDur=0.2),
         TK(r(FL12 - 0.3), face={'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}, d=0.1, keep=True), *BLINKS(1.0, CUT12, CALM, 2.0), *BREATHE(0.2, CUT12, 0.5)]
kh12 = [k(0.0, visible=False), k(CUT12, visible=True), *LIE(0.0, {'lid': 1.0, 'mouth': 'O', 'brow': 0.0, 'jaw': 0.8}), BEDHANDS(B12), *[TK(r(CUT12 + 0.25 * j), sq=(1.05, 0.97, 1.05) if j % 2 == 0 else (1, 1, 1), d=0.22, keep=True) for j in range(4)]]
st.shot('S12', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[*tk12, act('voisin1', NBW12, 0, 'stand', 'neutral', keys=knb12 + [k(CUT12, visible=False)]), act('mecPyj', BEDPOS(B12), 0, 'lieBack', 'neutral', keys=kh12)],
        props=[P('sol12', 'moGround', pos=[0, 0, 0], opts={'kerb': 1.0}), P('facade12', 'moFacade', pos=[0, 0, -0.1], opts={'w': 12, 'h': 9.5, 'lit': True}),
               P('camionmicro12', 'moMicTruck', pos=TR12, ry=TRY12, opts={'tip': TIP12}), MUFFS('cacheoreilles12', 'voisin1'),
               *[P(f'casque12_{i + 1}', 'moPhones', on={'actor': f'technicien{i + 1}', 'joint': 'head', 'offset': [0, 0.14, 0]}, opts={'span': 0.2, 'top': 0.24}) for i in range(3)],
               *BEDROOM('S12', B12), BEDMIC('micro12', B12)], cams=[C12, C12b])
st.cue('engine', 'S12', 0.0, 0.15); st.cue('sfx:stretch', 'S12', 0.4, 0.2); st.cue('engine', 'S12', r(CUT12 + 0.1), 0.3)

# ================================================================= S13
# 13: the bedroom, the lamp on, the mic over the headboard: he sleeps mouth wide open: three huge snores (snore lines), the curtains billow, the lamp
#     wobbles; the last one is held, mouth wide... and he wakes himself up, bolts upright exactly as in line 1 and looks round for the noise
D13 = st.dur('S13'); SN13 = [0.15, 0.6, 1.05]; UP13 = r(st.at('S13', 'L13', 4) - 0.03)
B13 = [0, 0, 0]; C13 = BEDCAM(0.0, B13, 0.1)
BEDCHK('S13', C13, B13)
SNORE = {'lid': 1.0, 'mouth': 'O', 'brow': 0.0, 'jaw': 1.0}
kh13 = [*LIE(0.0, {'lid': 1.0, 'mouth': 'O', 'brow': 0.0, 'jaw': 0.6}), BEDHANDS(B13)]
for j, t in enumerate(SN13):
    big = j == len(SN13) - 1
    kh13 += [TK(r(t - 0.08), sq=(0.95, 1.04, 0.95), face={**SNORE, 'jaw': 0.4}, d=0.07, keep=True),   # breath in
             TK(t, face=SNORE, sq=(1.12, 0.92, 1.12) if not big else (1.22, 0.86, 1.22), scl={'head': [1.1, 1.1, 1.1] if not big else [1.22, 1.2, 1.15]}, d=0.12, e='out', keep=True)]   # the snore swells him
    if not big: kh13 += [TK(r(t + 0.3), face={**SNORE, 'jaw': 0.5}, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.12, keep=True)]
    else: kh13 += [TK(r(t + 0.25), sq=(1.08, 0.94, 1.08), scl={'head': [1.12, 1.1, 1.08]}, d=0.15, keep=True), TK(r(UP13 - 0.1), face=SNORE, d=0.05, keep=True)]   # (round 1) the wide-open snore held until the wake
kh13 += [*SITUP(UP13), TK(r(UP13 + 0.3), {'R': R5(add(BEDPOS(B13), [-0.35, 0.35, 0.3])), 'L': R5(add(BEDPOS(B13), [0.35, 0.35, 0.3]))}, {'R': 'spread', 'L': 'spread'}, d=0.1, keep=True),
         *LOOKAROUND(r(UP13 + 0.4), B13, 3, 0.3), k(r(UP13 + 1.3), look='camera', lookDur=0.15), *blink(r(UP13 + 1.15), WIDE), *BREATHE(r(UP13 + 0.4), D13, 0.35)]
st.shot('S13', 'whiteVoid', setOpts={'color': DAWN}, look={'sunDir': [0.3, 0.8, 0.8]},
        actors=[act('mecPyj', BEDPOS(B13), 0, 'lieBack', 'neutral', keys=kh13)],
        props=[*BEDROOM('S13', B13, lamp_wobble=[r(t + 0.05) for t in SN13], curtain_flap=[r(t + 0.03) for t in SN13]), BEDMIC('micro13', B13, SN13),
               P('ronfle13', 'moSnore', pos=add(B13, [-0.28, 1.0, -1.0]), opts={'at': SN13, 'big': 2}), SMEAR('trait13', B13, UP13)], cams=[C13])
for t in SN13: st.cue('engine', 'S13', t, 0.45)
st.cue('sfx:spring', 'S13', UP13, 0.3)

# ================================================================= S14
# 14: in profile, sitting up in bed he scratches his box head; behind him a technician and the boom mic turn slowly to look at him. A beat, a sweat
#     drop pops and he points his index at his own chest, a clear silhouette against the plain wall
D14 = st.dur('S14'); GUILT14 = r(st.at('S14', 'L14', 5) - 0.1)
B14 = [0, 0, 0]; HP14 = BEDPOS(B14); TK14 = add(B14, [-1.6, 0, -1.05])
C14 = cam(0.0, add(B14, [2.35, 1.7, -0.3]), add(B14, [2.2, 1.69, -0.3]), add(B14, [-0.3, 1.5, -0.35]), add(B14, [-0.3, 1.5, -0.33]), lens=50)   # (round 1) tighter, side on: the gesture reads
chk('S14', C14, {'heroTop': add(HP14, [0, 1.75, 0]), 'chest': add(HP14, [0, 0.95, 0.2]), 't0': add(TK14, [0, 2.2, 0]), 'mic': add(B14, [-0.3, 2.55, -0.8])})
SCR = {'L': ['face', 0.42, 0.95, -0.02, 1, 0.02]}; SCR2 = {'L': ['face', 0.36, 1.0, 0.04, 1, 0.02]}
kh14 = [k(0.0, clip='sitFloor'), k(0.0, look='camera'), TK(0.0, {'R': R5(add(HP14, [-0.3, 0.12, 0.35])), 'L': R5(add(HP14, [0.3, 0.12, 0.35]))}, {'R': 'rest', 'L': 'rest'}, {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}, d=0.0),
        # (draft 2) the body side on, the box head turned to us (a box head in profile reads as seen from behind)
        *[TK(r(0.12 + 0.11 * j), touch=SCR if j % 2 == 0 else SCR2, hands={'L': 'claw'}, d=0.1, keep=True) for j in range(int((GUILT14 - 0.3) / 0.11))],   # scratching his box head
        TK(r(GUILT14 - 0.2), face={'lid': 0.15, 'mouth': 'line', 'brow': 0.7}, d=0.15, keep=True),
        TK(r(GUILT14 - 0.12), touch={'L': ['torso', 0.25, 0.5, 0.45, 1, 0.0, [0.8, -0.3, 0.5]]}, hands={'L': 'point'}, d=0.1, keep=True),   # the hand comes down in front of him...
        TK(GUILT14, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(0.9, 1.1, 0.9), d=0.05, e='out', keep=True),
        TK(r(GUILT14 + 0.08), touch=SELFPT('L'), hands={'L': 'point'}, d=0.25, keep=True),   # ...and slowly the index on his own chest
        TK(r(GUILT14 + 0.18), face={'lid': 0.1, 'mouth': 'line', 'brow': 0.9}, sq=(1, 1, 1), d=0.12, keep=True),         *blink(0.7, {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}), *BREATHE(0.2, D14, 0.4)]
ry0, ry1 = 150, yaw(TK14, HP14)
ktk = [k(0.0, clip='stand'), k(0.0, look=HEAD(add(TK14, [0, 0, -2]), 1.9)), TK(0.0, HANDS(TK14, ry0), {'R': 'rest', 'L': 'rest'}, CALM, d=0.0), k(0.3, face=ry1, turn=0.6), k(0.35, look=HEAD(HP14, 1.6), lookDur=0.5),
       *[TK(r(0.3 + 0.2 * j), HANDS(TK14, ry0 + (ry1 - ry0) * min(1.0, j / 3)), d=0.2, e='linear', keep=True) for j in range(4)],
       TK(r(GUILT14 + 0.1), face={'lid': 0.3, 'mouth': 'line', 'brow': 0.5}, sq=(0.97, 1.03, 0.97), d=0.15, keep=True), *blink(1.1, CALM), *BREATHE(0.1, D14, 0.5)]
st.shot('S14', 'whiteVoid', setOpts={'color': DAWN}, look={'sunDir': [0.3, 0.8, 0.8]},
        actors=[act('mecPyj', HP14, 0, 'sitFloor', 'neutral', keys=kh14), act('technicien1', TK14, ry0, 'stand', 'neutral', keys=ktk)],
        props=[*BEDROOM('S14', B14), DROP('goutte14', 'mecPyj', r(GUILT14 - 0.05), (0.2, 0.36, 0.08), 0.8),
               P('casque14_1', 'moPhones', on={'actor': 'technicien1', 'joint': 'head', 'offset': [0, 0.14, 0]}, opts={'span': 0.2, 'top': 0.24}),
               P('micro14', 'moMic', pos=add(B14, [-0.3, 2.55, -0.8]), rot=[0, -3.0, -0.41], opts={'r': 0.3, 'pole': 2.0}, keys=[k(0.3, rotTo=[0, -1.5708, -0.41], dur=0.9)])], cams=[C14])   # the mic turns to him
st.cue('sfx:pop', 'S14', r(GUILT14 - 0.05), 0.2)

# ================================================================= S15
# 15: the landing in bright morning light: he opens his front door and steps out beside it; one sheet is taped on it at eye level: a glance, he looks
#     away to us... snaps back (double take) and stretches toward « CERTAINS SE RECONNAÎTRONT. »
D15 = st.dur('S15'); OPEN15 = 0.25; SEE15 = r(st.at('S15', 'L15', 6) - 0.05); GL15 = r(min(SEE15 - 0.45, 1.25)); OUT15 = r(OPEN15 + 0.2)
LD15 = [0, 0, 0]; DOOR15 = add(LD15, [-0.35, 0, -1.5]); HI15, HO15 = add(DOOR15, [0.35, 0, -0.8]), add(DOOR15, [0.68, 0, 0.55])   # (round 1) he ends beside the door, not in front of the note
NOTE15 = add(DOOR15, [-0.1, 1.62, 0.12])
C15 = cam(0.0, add(LD15, [0.6, 1.6, 2.7]), add(LD15, [0.55, 1.6, 2.5]), add(LD15, [0.12, 1.68, -1.3]), add(LD15, [0.12, 1.68, -1.3]), lens=46)
chk('S15', C15, {'note': NOTE15, 'heroTop': add(HO15, [0, 2.35, 0]), 'door': add(DOOR15, [0, 2.2, 0])})
F15 = {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}
kh15 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, face=F15, d=0.0),
        k(OUT15, to=HO15, dur=0.5, clip='walk', ease='out', params={'freq': 2.0}), k(r(OUT15 + 0.5), clip='stand', blend=0.1), k(r(OUT15 + 0.35), face=-15, turn=0.15),
        k(GL15, look=NOTE15, lookDur=0.07), k(r(GL15 + 0.22), look='camera', lookDur=0.08), TK(r(GL15 + 0.25), face={**F15, 'lid': 0.3}, d=0.06, keep=True),   # a glance... and away, deadpan
        TK(r(SEE15 - 0.07), sq=(1.05, 0.95, 1.05), d=0.05, keep=True),   # a beat (anticipation)
        k(SEE15, look=NOTE15, lookDur=0.05), k(SEE15, face=-70, turn=0.1),   # ...the double take
        TK(r(SEE15 + 0.03), face=POP, sq=(0.9, 1.12, 0.9), scl={'head': [0.92, 1.15, 0.95]}, bend={'spine': SP(0.3), 'neck': SP(0.25)}, d=0.05, e='out', keep=True),   # stretched toward the note, eyes out
        TK(r(SEE15 + 0.25), face={'lid': 0.1, 'mouth': 'O', 'brow': 0.9, 'pop': 0.4}, sq=(1.02, 0.98, 1.02), scl={'head': [1, 1, 1]}, bend={'spine': SP(0.2), 'neck': SP(0.15)}, d=0.1, keep=True),
        TK(r(SEE15 + 0.4), face={'lid': 0.1, 'mouth': 'line', 'brow': 0.8}, sq=(1, 1, 1), bend={'spine': SP(0.12), 'neck': SP(0.1)}, d=0.12, keep=True),
        k(r(SEE15 + 0.55), look='camera', lookDur=0.2), *blink(r(SEE15 + 0.5), {'lid': 0.1, 'mouth': 'line', 'brow': 0.8}), *BREATHE(r(SEE15 + 0.3), D15, 0.4)]
st.shot('S15', 'whiteVoid', setOpts={'color': '#F2EADA'}, look={'sunDir': [0.5, 0.9, 0.7]},
        actors=[act('mecPyj', HI15, 0, 'stand', 'neutral', keys=kh15)],
        props=[P('palier15', 'moRoom', pos=LD15, opts={'w': 5, 'd': 3, 'h': 2.8, 'wall': '#F2E2C8', 'floor': '#B9A58A', 'doorX': -0.35}), P('porte15', 'moDoor', pos=DOOR15, opts={'open': [[0, 0], [OPEN15, 0], [r(OPEN15 + 0.3), 0.38]], 'note': True}),
               P('interieur15', 'moRoom', pos=add(DOOR15, [0, 0, -1.6]), opts={'w': 3, 'd': 3, 'h': 2.8, 'wall': '#D9E4F0', 'floor': '#A8927A'})], cams=[C15])
st.cue('sfx:squeak', 'S15', OPEN15, 0.25); st.cue('sfx:gasp', 'S15', SEE15, 0.15)

# ================================================================= S16
# 16: wider, the same landing: door, walls and ceiling papered with identical notes; a paper avalanche pours down from the stairwell and buries him flat;
#     he re-inflates with a pop, the sheets fly off round his feet; on top of the paper heap beside him lands a gift: big bright pink earmuffs with a
#     looped ribbon bow, tilted toward us. Deadpan: a slow blink, then one eye ticks toward the earmuffs
D16 = st.dur('S16'); AV16 = 0.1; HIT16 = 0.3; POP16 = 1.2; GIFT16 = 1.45; TIC16 = r(min(2.6, D16 - 0.4))
LD16 = [0, 0, 0]; DOOR16 = add(LD16, [-0.6, 0, -1.6]); H16 = add(DOOR16, [0.3, 0, 0.35]); STAIR16 = add(LD16, [1.55, 0, -0.6]); HEAP16 = add(LD16, [0.6, 0, -0.85])
GIFTP = add(HEAP16, [0.0, 1.12, 0.08])
C16 = cam(0.0, add(LD16, [0.3, 1.5, 3.0]), add(LD16, [0.28, 1.48, 2.75]), add(LD16, [0.1, 1.45, -1.0]), add(LD16, [0.1, 1.45, -1.0]), lens=46)
chk('S16', C16, {'ceiling': add(LD16, [0, 3.0, -1.0]), 'heroTop': add(H16, [0, 2.35, 0]), 'gift': GIFTP, 'giftTop': add(GIFTP, [0, 0.4, 0]), 'mound': add(H16, [0, 0.85, 0])})
DEAD = {'lid': 0.45, 'mouth': 'line', 'brow': 0.0}
kh16 = [k(0.0, clip='stand'), k(0.0, look=HEAD(add(STAIR16, [0, 0, -1.5]), 2.4)), TK(0.0, face={'lid': 0.1, 'mouth': 'line', 'brow': 0.8}, d=0.0),
        TK(0.12, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(0.95, 1.06, 0.95), d=0.05, e='out', keep=True),   # he sees it coming
        TK(HIT16, face={'lid': 1.0, 'mouth': 'clench', 'brow': 0.5}, sq=(1.25, 0.65, 1.25), d=0.06, e='out', keep=True), TK(0.6, sq=(1.55, 0.28, 1.55), d=0.25, keep=True),   # (round 1) buried flat under the sheets
        TK(r(POP16 - 0.08), sq=(1.6, 0.25, 1.6), d=0.06, keep=True), k(r(POP16 - 0.05), look='camera', lookDur=0.04),
        TK(POP16, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(0.82, 1.28, 0.82), scl={'head': [0.9, 1.15, 0.95]}, d=0.06, e='out', keep=True),   # ...POP: re-inflated
        TK(r(POP16 + 0.12), sq=(1.08, 0.93, 1.08), scl={'head': [1.04, 0.97, 1.02]}, d=0.07, keep=True), TK(r(POP16 + 0.25), face=DEAD, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.1, keep=True),
        k(r(GIFT16 + 0.15), look='camera', lookDur=0.1),
        TK(2.1, face={**DEAD, 'lid': 1.0}, d=0.18, keep=True), TK(2.38, face=DEAD, d=0.18, keep=True),   # a slow blink
        TK(TIC16, face={**DEAD, 'gx': 0.9, 'lidL': 0.6}, d=0.04, keep=True), TK(r(TIC16 + 0.18), face={**DEAD, 'gx': 0.9}, d=0.05, keep=True), TK(r(TIC16 + 0.32), face=DEAD, d=0.06, keep=True),   # one eye ticks toward the earmuffs
        *BREATHE(r(POP16 + 0.3), D16, 0.45)]
st.shot('S16', 'whiteVoid', setOpts={'color': '#F2EADA'}, look={'sunDir': [0.5, 0.9, 0.7]},
        actors=[act('mecPyj', H16, -10, 'stand', 'neutral', keys=kh16)],
        props=[P('palier16', 'moPapered', pos=LD16, opts={'w': 4.6, 'h': 3.0, 'd': 3.2, 'doorX': -0.6}), P('porte16', 'moDoor', pos=DOOR16, opts={'open': 0.38, 'note': True}),
               P('interieur16', 'moRoom', pos=add(DOOR16, [0, 0, -1.6]), opts={'w': 3, 'd': 3, 'h': 2.8, 'wall': '#D9E4F0', 'floor': '#A8927A'}),
               P('escalier16', 'moStairs', pos=STAIR16, opts={'n': 8, 'w': 1.0}),
               P('avalanche16', 'moAvalanche', pos=H16, opts={'n': 110, 'from': [1.7, 2.3, -0.4], 'at': AV16, 'dur': 0.55, 'mound': {'h': 0.9, 'r': 0.62}, 'burst': POP16}),
               P('tas16', 'moAvalanche', pos=HEAP16, opts={'n': 70, 'preset': True, 'mound': {'h': 1.05, 'r': 0.5}}),
               P('cadeau16', 'moEarmuffs', pos=GIFTP, rot=[0.4, -0.35, 0.15], opts={'bow': True, 'dropAt': r(GIFT16 - 0.3), 'dropH': 1.6, 'r': 0.2, 'span': 0.28, 'top': 0.34})], cams=[C16])
st.cue('sfx:paper', 'S16', AV16, 0.35); st.cue('thud', 'S16', HIT16, 0.3); st.cue('sfx:pop', 'S16', POP16, 0.3); st.cue('sfx:paper', 'S16', POP16, 0.25); st.cue('sfx:bonk', 'S16', GIFT16, 0.2)

for g_ in [('S01', UP1, 'mecPyj', 'bolt'), ('S02', 0.3, 'passant1', 'guilt'), ('S03', ST3[0], 'agent', 'stamp'), ('S04', GIVE4, 'prefet', 'drill'), ('S05', COPY5, 'conseiller1', 'shush'),
           ('S06', PIN6, 'pompier1', 'pinpon'), ('S07', 1.0, 'eboueur1', 'tiptoe'), ('S08', CROW8[0], 'fermier', 'dome'), ('S09', SL9[0], 'client1', 'notes'), ('S10', UP10, 'mecPyj', 'bolt'),
           ('S11', TURN11, 'mecPyj', 'heads'), ('S12', FL12, 'technicien1', 'mic'), ('S13', UP13, 'mecPyj', 'self'), ('S14', GUILT14, 'mecPyj', 'guilt'), ('S15', SEE15, 'mecPyj', 'note'), ('S16', GIFT16, 'mecPyj', 'gift')]:
    st.gag(*g_)

for _sc in st.scenes:
    for _a in _sc['actors']:
        _run = {'reach': {}, 'hands': {}}
        for _kk in sorted((x for x in _a.get('keys', []) if isinstance(x, dict) and 'toon' in x), key=lambda x: x.get('at', 0)):
            for _n in ('reach', 'hands'):
                if _n in _kk['toon']: _kk['toon'][_n] = {**_run[_n], **_kk['toon'][_n]}; _run[_n] = dict(_kk['toon'][_n])
print('\n'.join(CHECKS))

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
GUEST = lambda pr, seed, suit: {'preset': pr, 'seed': seed, 'hat': 'none', 'suit': suit, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("Le mot", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'mecPyj': MEC,   # (round 1, coordinator) the series' fixed model everywhere, in bed and on the landing too: navy suit, red tie, teal lapels
    'voisin1': GUEST('fermier', 5101, '#7A5A8A'), 'voisin2': GUEST('madame', 5102, '#C8322A'), 'voisine2': GUEST('femme', 5103, '#5E8C7A'), 'voisin3': GUEST('worker', 5104, '#5E8C4A'),
    **{f'passant{i + 1}': GUEST(['worker', 'tourist', 'madame', 'fermier'][i], 5110 + i, ['#3E7FB6', '#D9A23A', '#C8322A', '#5E8C4A'][i]) for i in range(4)},
    'cycliste': {'preset': 'sportif', 'seed': 5115, 'toon': EX},
    'agent': {'preset': 'cop', 'outfit': 'suit', 'seed': 5120, 'suit': '#1E2A44', 'pants': '#1E2A44', 'shirt': '#C9D6EA', 'lapel': '#18223A', 'tie': '#18223A', 'cuff': '#1E2A44', 'hat': 'none', 'glasses': False, 'toon': EX},   # (round 1) the stock cap carries a gold badge: a plain moCap prop
    **{f'citoyen{i + 1}': GUEST(['madame', 'tourist', 'worker', 'femme'][i], 5121 + i, ['#8A5AB6', '#C86A2A', '#2E7D4F', '#8A8070'][i]) for i in range(4)},
    'prefet': {'preset': 'politique', 'seed': 5130, 'suit': '#22283A', 'lapel': '#1A1E2C', 'tie': '#3A3D44', 'hat': 'none', 'hair': 'receding', 'glasses': False, 'facial': 'mustache', 'toon': EX},   # (round 1) cap: a plain moCap prop (the stock one has a badge)
    'orateur': {'preset': 'politique', 'seed': 5131, 'suit': '#4A4F58', 'lapel': '#3C414A', 'tie': '#7A2E2E', 'glasses': True, 'toon': EX},
    **{f'conseiller{i + 1}': GUEST(['politique', 'madame', 'commissaire', 'femme'][i], 5132 + i, ['#5A4A3A', '#2E4563', '#6A5440', '#7A3A4A'][i]) for i in range(4)},
    **{f'pompier{i + 1}': {'preset': 'pompier', 'seed': 5140 + i, 'facial': 'none' if i else 'mustache', 'toon': EX} for i in range(2)},
    **{f'eboueur{i + 1}': {'preset': 'worker', 'seed': 5145 + i, 'suit': '#F07A1E', 'pants': '#F07A1E', 'lapel': '#F2C94C', 'cuff': '#F07A1E', 'hat': 'none', 'toon': EX} for i in range(2)},
    'fermier': {'preset': 'fermier', 'seed': 5150, 'hat': 'none', 'toon': EX},   # (round 1) his straw hat is a prop: it lags behind the nod
    'client1': GUEST('madame', 5151, '#C86A8A'), 'client2': GUEST('commissaire', 5152, '#5A6E9A'), 'serveur': {'preset': 'serveur', 'seed': 5153, 'toon': EX},
    **{f'technicien{i + 1}': GUEST(['worker', 'tourist', 'fermier'][i], 5160 + i, ['#4A5560', '#3E5FB6', '#6A5440'][i]) for i in range(3)},
})
