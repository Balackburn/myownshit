#!/usr/bin/env python3
"""Le pardon (story 103; a reflex « pardon » in the street, a pardon from the president, and a whole judicial machine built on it).
This man said « pardon » in the street; the president pardoned him. Pardoned for what? Nobody knew. Problem: you cannot pardon an innocent man, so he
was tried for nothing; the prosecutor asked for life so the pardon would be worth it; sentenced at noon, pardoned at one minute past. Since then every
« pardon » counts as a plea for mercy: eight million trials a morning in the metro, the president signs pardons on a conveyor belt, more popular than
ever. The inmates said pardon in chorus and the prisons emptied, the director too, who switched off the lights. The minister banned the word
(« Excusez-moi »: three years, « Oups »: six months); people bump into each other in silence and the backpacks have won. The president never said
pardon: he was the one who bumped this man.
Silent plants: the huge lemon polka-dot tie on the faceless torso that bumps him (S01) and slaps the scroll on the rail (S06), then on the president in
every shot he is in (S01, S09, S15, S16); the baguette broken in S01 in two halves in every shot with the hero (S02, S04, S06, S08, S14, S16).
Cards: GRACIÉ (S06), INTERDIT (S12). The only other word on screen: « PARDON » on the minister's board, struck through by one diagonal red line.
No figure, flag, emblem, portrait or sash; generic uniforms; nobody hurt."""
from story_kit import *
import math

st = Story('pardon', look='natural')
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
HALF = {'L': {'offset': [0.0, -0.07, 0.05], 'rot': [0, 0, -1.5708]}, 'R': {'offset': [0.0, -0.07, 0.05], 'rot': [0, 0, -1.5708]}}   # along the fingers
def HALVES(sid, who='mec', t0=None, t1=None, both=None):
    """the two halves of the broken baguette, one in each mitten (or both in one mitten: both='L', crossed)"""
    out = []
    for j, h in enumerate(('L', 'R')):
        ks = ([k(0.0, visible=False), k(t0, visible=True)] if t0 is not None else []) + ([k(t1, visible=False)] if t1 is not None else [])
        on = {'actor': who, 'hand': h, **HALF[h]} if not both else {'actor': who, 'hand': both, 'offset': [0.0, -0.07, 0.05 + 0.06 * j], 'rot': [0, 0.5 * (j - 0.5), -1.5708 + 0.35 * (j - 0.5)]}
        out.append(P(f'demi{h}{sid}', 'pdBaguette', opts={'half': 'R', 'len': 0.8}, on=on, **({'keys': ks} if ks else {})))
    return out

# ================================================================= S01
# 1: the pavement in front of a bakery, low: he steps out with a long baguette held at his chest; a dark-suited torso barges in from the right, face out
#    of frame, a huge lemon polka-dot tie flapping on its chest; the baguette snaps in two (crack, crumbs), he half spins round and says « pardon » to
#    the empty air. Cut: a plain office: the round president, the same tie, signs a big parchment and holds it up beside his head
D1 = st.dur('S01'); CUT1 = r(st.at('S01', 'L01', 8) - 0.1); HIT1 = snap(0.4); SNAP1 = r(HIT1 + 0.03); SWAP1 = r(HIT1 + 0.3); OUT1 = r(HIT1 + 0.1)
BK1 = [0, 0, -1.3]; H01 = [0, 0, -0.55]; H1 = [0, 0, 0.2]; HRY1 = -35
TS0, TSH, TS2, TS1 = [2.7, 0, 0.0], [0.78, 0, 0.1], [0.2, 0, -0.75], [-3.6, 0, -0.9]   # the round bumper (the president's own body, head turned away: no face), shoulder to shoulder, then behind him and off
C1 = cam(0.0, [0.5, 1.35, 4.6], [0.48, 1.35, 4.45], [0.15, 1.3, 0.2], [0.15, 1.31, 0.2], lens=46)
OF = [40.0, 0, 0.0]; PR1 = add(OF, [0.15, 0, -0.2]); DESK1 = add(OF, [0.15, 0, 0.45])
SCR1A = add(OF, [-0.1, 0.8, 0.45]); SCR1B = add(PR1, [-0.78, 1.66, 0.1])
C1b = cam(CUT1, add(OF, [0.05, 1.4, 3.1]), add(OF, [0.05, 1.4, 2.85]), add(OF, [-0.15, 1.35, 0.0]), add(OF, [-0.15, 1.38, 0.0]), lens=46)
BG1 = off(H1, 0, 0.35, 0.42, 1.3)   # the baguette held out at his right side (screen left), clear of the torso
chk('S01', C1, {'heroTop': add(H1, [0, 2.35, 0]), 'heroMouth': add(H1, [0, 1.8, 0]), 'bumperTop@hit': add(TSH, [0, 2.1, 0]), 'tie@hit': add(TSH, [0, 1.3, 0.5]), 'baguette': BG1, 'heroFeet': H1})
chk('S01b', C1b, {'presFace': add(PR1, [0, 1.72, 0]), 'presTop': add(PR1, [0, 2.0, 0]), 'tie': add(PR1, [0, 1.15, 0.4]), 'scroll': SCR1B, 'scrollTop': add(SCR1B, [0, 0.36, 0]), 'desk': add(DESK1, [0.7, 0.76, 0.35])})
TAKE1 = 0.85; SPIN1 = 1.07; HRY1b = -52
k1 = [k(0.0, clip='walk'), k(0.0, to=H1, dur=0.3, clip='walk', ease='out', params={'freq': 2.4}), k(0.3, clip='stand'), k(0.0, look='camera'),
      TK(0.0, {'R': R5(BG1), 'L': R5(off(H1, 0, 0.3, -0.05, 1.3))}, {'R': 'grip', 'L': 'open'}, CALM, d=0.0),
      k(r(HIT1 - 0.1), look=HEAD(TSH, 1.9), lookDur=0.06), TK(r(HIT1 - 0.1), face={**CALM, 'brow': 0.4}, sq=(1.03, 0.97, 1.03), d=0.08, keep=True),   # his eyes catch it a beat before
      TK(HIT1, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'jaw': 0.6}, sq=(0.72, 1.22, 0.9), scl={'head': [1.4, 0.75, 1.1]}, bend={'spine': SP(-0.1, 0.55)}, d=0.03, e='out', keep=True),   # the shove: pinched, the head smeared flat
      k(r(HIT1 + 0.03), face=r(HRY1 - 40), turn=0.12), TK(r(HIT1 + 0.1), sq=(1.12, 0.9, 1.12), scl={'head': [0.9, 1.15, 0.95]}, bend={'spine': SP(0.05, -0.2)}, d=0.06, keep=True),   # the spin overshoots...
      k(r(HIT1 + 0.2), face=HRY1, turn=0.15), TK(r(HIT1 + 0.22), face=WORRY, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, bend={'spine': SP(0.0, 0.0)}, d=0.1, keep=True),   # ...and settles half round
      TK(SWAP1, {'R': R5(off(H1, HRY1, 0.32, 0.36, 1.2)), 'L': R5(off(H1, HRY1, 0.32, -0.36, 1.2))}, {'R': 'grip', 'L': 'grip'}, d=0.1, keep=True),   # a half in each mitten
      k(r(TAKE1 - 0.06), look='camera', lookDur=0.05),
      TK(TAKE1, face={**POP, 'jaw': 0.5}, sq=(0.9, 1.14, 0.9), scl={'head': [0.92, 1.12, 0.95]}, d=0.04, e='out', keep=True),   # the take, held 6 frames...
      TK(r(TAKE1 + 0.17), face={**POP, 'jaw': 0.3}, sq=(0.93, 1.1, 0.93), d=0.03, keep=True), TK(r(SPIN1 - 0.02), face=WORRY, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.05, keep=True),
      k(r(SPIN1 - 0.04), look=HEAD(off(H1, HRY1b, 2.5, 0, 0), 2.0), lookDur=0.05), k(SPIN1, face=r(HRY1b - 30), turn=0.12), k(r(SPIN1 + 0.13), face=HRY1b, turn=0.12),   # ...then the half turn to the empty air, overshooting
      TK(SPIN1, sq=(1.1, 0.9, 1.1), scl={'head': [1.6, 0.85, 0.9]}, bend={'spine': SP(0.0, -0.25)}, d=0.04, e='out', keep=True), TK(r(SPIN1 + 0.08), scl={'head': [1, 1, 1]}, d=0.05, keep=True),   # the half turn smeared wide TK(r(SPIN1 + 0.14), sq=(1, 1, 1), bend={'spine': SP(0.0, 0.0)}, d=0.08, keep=True),
      TK(r(SPIN1 + 0.12), {'R': R5(off(H1, HRY1b, 0.32, 0.36, 1.2)), 'L': R5(off(H1, HRY1b, 0.32, -0.36, 1.2))}, d=0.12, keep=True),
      TK(r(SPIN1 + 0.15), bend={'spine': SP(0.35)}, d=0.12, keep=True), *TALK(r(SPIN1 + 0.17), WORRY, 4, 0.07), TK(r(SPIN1 + 0.55), bend={'spine': SP(0.0)}, d=0.15, keep=True),   # a little bow: « pardon »
      *blink(r(SPIN1 + 0.6), WORRY), *BREATHE(r(SPIN1 + 0.55), CUT1, 0.35)]
st.shot('S01', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', H01, 0, 'walk', 'neutral', keys=k1)],
        props=[P('sol1', 'pdGround', pos=[0, 0, 0], opts={'kerb': 3.0}), P('boulangerie1', 'pdBakery', pos=BK1, opts={'w': 7}),
               P('baguette1', 'pdBaguette', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.36, 0.05], 'rot': [0, 0, -1.5708]}, opts={'snapAt': SNAP1, 'len': 0.8}, keys=[k(SWAP1, visible=False)]),
               *HALVES('S01', t0=SWAP1),
               P('bousculeur1', 'pdPresident', pos=TS0, ry=-60, opts={'round': 1.15, 'walk': [0, 1.2, 2.8], 'flap': 2.8, 'bounce': [HIT1], 'look': [[0, PI]], 'smile': [[0, 0.4]]},   # his head turned right round: we never see his face
                 keys=[k(0.0, to=TSH, dur=HIT1, ease='in'), k(HIT1, squash=[1.2, 0.85, 1.2], dur=0.3), k(OUT1, to=TS2, dur=0.18, ease='inOut'), k(r(OUT1 + 0.18), to=TS1, dur=0.3, ease='in'), k(r(OUT1 + 0.5), visible=False)]),
               P('bureau1', 'pdRoom', pos=OF, opts={'w': 5, 'd': 4, 'wall': '#E6DCCB', 'floor': '#B58E66', 'window': {'x': -1.3, 'y': 1.7, 'w': 1.1, 'h': 1.2}}),
               P('table1', 'table', pos=DESK1, opts={'w': 1.5, 'd': 0.7, 'h': 0.76, 'color': '#8A6A45'}),
               P('president1', 'pdPresident', pos=PR1, opts={'round': 1.05, 'sign': [[r(CUT1 + 0.05), r(CUT1 + 0.55)]], 'raise': [[r(CUT1 + 0.72), D1]], 'bounce': [r(CUT1 + 0.56), r(CUT1 + 0.74)],   # a little dip first (anticipation), then up
                 'smile': [[0, 0.6], [r(CUT1 + 0.7), 1.0]], 'blink': [r(CUT1 + 0.95)], 'look': [[0, -0.2], [r(CUT1 + 0.6), -0.2], [r(CUT1 + 0.75), 0.15], [r(CUT1 + 1.05), 0.0]]}),
               P('parchemin1', 'pdScroll', pos=SCR1A, rot=[-1.5708, 0, 0], opts={'w': 0.42, 'h': 0.56}, keys=[k(r(CUT1 + 0.56), to=add(SCR1A, [0, -0.04, 0]), dur=0.12, ease='out'), k(r(CUT1 + 0.7), to=SCR1B, dur=0.15, ease='out'), k(r(CUT1 + 0.7), rotTo=[0, 0, 0], dur=0.15),
                 k(r(CUT1 + 0.85), squash=[1.1, 0.9, 1.0], dur=0.3), *[k(r(CUT1 + 0.9 + 0.2 * j), rotTo=[0, 0, 0.06 if j % 2 else -0.06], dur=0.2) for j in range(int((D1 - CUT1 - 0.9) / 0.2) + 1)]])],   # waved a little, proudly
        cams=[C1, C1b])
st.cue('sfx:step', 'S01', 0.05, 0.25); st.cue('whoosh', 'S01', r(HIT1 - 0.15), 0.3); st.cue('sfx:gasp', 'S01', TAKE1, 0.2); st.cue('thud', 'S01', HIT1, 0.45); st.cue('sfx:crunch', 'S01', SNAP1, 0.45)
st.cue('sfx:paper', 'S01', r(CUT1 + 0.1), 0.3); st.cue('sfx:pop', 'S01', r(CUT1 + 0.62), 0.25)

# ================================================================= S02
# 2: his doorstep: he holds the big scroll in one mitten, a baguette half in the other; two gendarmes and a clerk lean over the scroll from both
#    sides, then shrug together
D2 = st.dur('S02'); SHR2 = r(st.at('S02', 'L02', 3) - 0.12)
FAC2 = [0, 0, -1.2]; H2 = [0, 0, 0.0]
SC2 = off(H2, 0, 0.5, 0.12, 1.62)   # held up in HIS mitten, in front of him, clear of the two gendarmes
G21 = [-0.9, 0, 0.35]; G22 = [0.95, 0, 0.4]; CL2 = [0.5, 0, -0.6]   # the clerk in the gap between the hero and the right gendarme
C2 = fcam(0.0, [0.2, 1.7, 4.0], {'heroTop': add(H2, [0, 2.4, 0]), 'g1': add(G21, [-0.3, 2.3, 0]), 'g2': add(G22, [0.35, 2.3, 0]), 'cl': add(CL2, [0.3, 2.2, 0]), 'waist': add(H2, [0, 1.05, 0.4])}, top=0.08, bottom=0.74, push=0.3)
chk('S02', C2, {'heroFace': add(H2, [0, 1.95, 0]), 'scroll': SC2, 'g1Face': add(G21, [0, 1.85, 0]), 'g2Face': add(G22, [0, 1.85, 0]), 'clFace': add(CL2, [0, 1.8, 0])})
k2 = [k(0.0, clip='stand'), k(0.0, look=HEAD(SC2, 1.95)), TK(0.0, {'R': R5(add(SC2, [0.0, -0.25, 0.02])), 'L': R5(off(H2, 0, 0.3, -0.32, 1.1))}, {'R': 'grip', 'L': 'grip'}, WORRY, d=0.0),
      k(0.6, look='camera', lookDur=0.15), TK(SHR2, face={**WORRY, 'brow': 1.0}, sq=(0.93, 1.1, 0.93), d=0.06, e='out', keep=True), TK(r(SHR2 + 0.2), face=WORRY, sq=(1, 1, 1), d=0.15, keep=True),   # his brows up, stretched tall
      *blink(0.9, WORRY), *BREATHE(r(SHR2 + 0.3), D2, 0.45)]
lean = []
for i, (p, nm) in enumerate([(G21, 'gendarme1'), (G22, 'gendarme2'), (CL2, 'greffier')]):
    ry = yaw(p, SC2)
    ks = [k(0.0, clip='stand'), k(0.0, look=HEAD(SC2, 1.8)), TK(0.0, face=GRAVE, d=0.0),
          TK(0.02, bend={'spine': SP(-0.1)}, sq=(1.04, 0.96, 1.04), d=0.06, keep=True),   # a little rise back first...
          TK(r(0.1 + 0.03 * i), bend={'spine': SP(0.45)}, face={**GRAVE, 'lid': 0.5}, sq=(0.96, 1.05, 0.96), d=0.12, e='out', keep=True), TK(r(0.3 + 0.03 * i), bend={'spine': SP(0.5)}, sq=(1, 1, 1), d=0.12, keep=True),   # ...then a quick lean over the scroll
          TK(r(SHR2 - 0.15), bend={'spine': SP(0.0)}, d=0.12, keep=True), k(r(SHR2 - 0.02), clip='bigShrug', blend=0.08), k(r(SHR2 - 0.06), look=HEAD(add(p, [0, 0, 2.0]), 1.9), lookDur=0.08),
          TK(SHR2, face={'lid': 0.3, 'mouth': 'line', 'brow': 1.0}, sq=(0.86, 1.18, 0.86), bend={'neck': SP(-0.25)}, d=0.06, e='out', keep=True),   # all together: shoulders up past the ears...
          TK(r(SHR2 + 0.1), sq=(1.06, 0.95, 1.06), d=0.08, keep=True), TK(r(SHR2 + 0.22), sq=(1, 1, 1), bend={'neck': SP(0.0)}, d=0.1, keep=True), k(r(SHR2 + 0.45), clip='stand', blend=0.2),   # ...overshoot down and settle
          *blink(r(0.5 + 0.2 * i), GRAVE), *BREATHE(r(SHR2 + 0.4), D2, 0.5)]
    lean.append(act(nm, p, ry, 'stand', 'neutral', keys=ks))
st.shot('S02', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.3, 0.9, 0.8]},
        actors=[act('mec', H2, 0, 'stand', 'neutral', keys=k2), *lean],
        props=[P('sol2', 'pdGround', pos=[0, 0, 0], opts={'color': '#D9CDB4'}), P('facade2', 'pdFacade', pos=FAC2, opts={'w': 10}), P('porte2', 'door', pos=add(FAC2, [0, 0, 0.05])),
               P('parchemin2', 'pdScroll', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.2, 0.06], 'rot': [0, 0, 0]}, opts={'w': 0.42, 'h': 0.56}),
               *HALVES('S02', both='L')], cams=[C2])
st.cue('sfx:paper', 'S02', 0.1, 0.2); st.cue('sfx:twang', 'S02', SHR2, 0.2)

# ================================================================= S03
# 3: a plain law office: a lawyer in a black gown holds the scroll up to the window light; on « Problème » a big red X stamps across it diagonally
#    with a buzzer; he shakes his head
D3 = st.dur('S03'); X3 = 0.34
RM3 = [0, 0, 0]; AV3 = [-0.2, 0, -0.3]; ARY3 = 10
SC3 = [0.45, 1.95, -0.05]; SC3L = [0.4, 1.5, 0.05]
C3 = fcam(0.0, [-0.1, 1.7, 3.4], {'top': add(AV3, [0, 2.3, 0]), 'sc': add(SC3, [0.32, 0.4, 0]), 'chest': add(AV3, [-0.45, 1.0, 0]), 'win': [1.3, 2.3, -1.9]}, top=0.08, bottom=0.7, push=0.2)
chk('S03', C3, {'avFace': add(AV3, [0, 1.85, 0]), 'scroll': SC3, 'scrollLow': add(SC3, [0, -0.36, 0])})
ka = [k(0.0, clip='stand'), k(0.0, look=HEAD(SC3, 1.95)), TK(0.0, {'R': R5(add(SC3, [-0.24, -0.1, 0.03])), 'L': R5(add(SC3, [0.24, -0.1, 0.03]))}, {'R': 'pinch', 'L': 'pinch'}, {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}, d=0.0),
      TK(0.06, face={'lid': 0.85, 'mouth': 'line', 'brow': -0.4}, bend={'spine': SP(-0.08)}, d=0.06, keep=True),   # he squints up at it against the light...
      TK(r(X3 + 0.02), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, scl={'head': [0.82, 1.32, 0.9]}, sq=(0.92, 1.08, 0.92), d=0.04, e='out', keep=True),   # the X: his head shoots up tall
      TK(r(X3 + 0.2), face=STERN, scl={'head': [1, 1, 1]}, sq=(1, 1, 1), d=0.12, keep=True),
      *[k(r(0.6 + 0.2 * j), look=HEAD(add(AV3, [-1.2 if j % 2 == 0 else 1.2, 0, 2.5]), 1.9), lookDur=0.12) for j in range(5)], k(1.65, look='camera', lookDur=0.15),
      TK(0.6, face={**STERN, 'mouth': 'clench'}, bend={'spine': SP(0.0, 0.12)}, d=0.12, keep=True), *[TK(r(0.8 + 0.2 * j), bend={'spine': SP(0.0, -0.12 if j % 2 == 0 else 0.12)}, d=0.18, keep=True) for j in range(4)],   # the whole body shakes no
      TK(1.45, {'R': R5(add(SC3L, [-0.24, -0.1, 0.03])), 'L': R5(add(SC3L, [0.24, -0.1, 0.03]))}, bend={'spine': SP(0.08)}, face=GRAVE, d=0.25, keep=True),   # lowers it, grave
      TK(1.75, sq=(1.03, 0.97, 1.03), d=0.2, keep=True), *blink(1.5, STERN), *blink(2.15, GRAVE), *BREATHE(1.7, D3, 0.4)]
st.shot('S03', 'whiteVoid', setOpts={'color': '#DDE5EA'}, look={'sunDir': [0.5, 0.8, 0.6]},
        actors=[act('avocat', AV3, ARY3, 'stand', 'neutral', keys=ka)],
        props=[P('cabinet3', 'pdRoom', pos=RM3, opts={'w': 5, 'd': 4, 'wall': '#D9E2E8', 'floor': '#9C7B58', 'window': {'x': 1.1, 'y': 1.8, 'w': 1.3, 'h': 1.4}}),
               P('parchemin3', 'pdScroll', pos=SC3, opts={'w': 0.5, 'h': 0.66, 'xAt': X3, 'xFrom': 1.3}, keys=[k(X3, squash=[1.12, 0.85, 1.0], dur=0.3), k(1.45, to=SC3L, dur=0.25, ease='inOut')]),
               P('robe3', 'pdRobe', on={'actor': 'avocat', 'joint': 'hips', 'offset': [0, 0.05, 0]}, opts={'L': 0.95})], cams=[C3])
st.cue('sfx:beep', 'S03', X3, 0.4); st.cue('thud', 'S03', X3, 0.35)

# ================================================================= S04 / S05 / S06 (the courtroom: plain wood, no emblem)
CRT = [0, 0, 0]
DK = [-1.7, 0, 0.7]; DRY = 35; HD = off(DK, DRY, -0.5, 0.0, 0.0)
JB = [1.4, 0, -1.6]; JRY = -25; JU = off(JB, JRY, -0.7, 0.0, 0.4)
TR = [-0.2, 0, -0.4]
RAIL = lambda s: off(DK, DRY, 0.6, s, 1.03)
def courtProps(sid, dock_open=False):
    return [P(f'salle{sid}', 'pdRoom', pos=CRT, opts={'w': 9, 'd': 6, 'h': 3.6, 'wall': '#E3D3B5', 'floor': '#8A6A45', 'trim': '#6A4A30'}),
            P(f'box{sid}', 'pdDock', pos=DK, ry=DRY, opts={'w': 1.5, 'depth': 1.2, **({'open': 'L'} if dock_open else {})}),
            P(f'estrade{sid}', 'pdJudgeBench', pos=JB, ry=JRY, opts={'w': 2.4})]
def judgeAct(ks, pos=None, ry=None): return act('juge', pos or JU, JRY if ry is None else ry, 'sit', 'neutral', keys=ks)

# 4: the hero sits in the dock, the two baguette halves laid on the rail in front of him; the judge looks across at the evidence table: a big empty
#    tray with a large brown tag
D4 = st.dur('S04'); JG4 = st.at('S04', 'L04', 4); RN4 = st.at('S04', 'L04', 5)
DK4 = [-0.2, 0, 0.45]; HD4 = add(DK4, [0, 0, -0.5]); RAIL4 = lambda x: add(DK4, [x, 1.03, 0.6])   # the dock square to us: his deadpan face to the lens
TR4 = [0.5, 0, 1.25]; JB4 = [1.3, 0, -1.9]; JU4 = add(JB4, [0, 0.4, -0.7]); JRY4 = -30
C4 = cam(0.0, [0.3, 1.75, 4.6], [0.28, 1.75, 4.35], [0.15, 1.05, 0.4], [0.15, 1.05, 0.4], lens=48)   # a little high: tray, tag and face above the band
chk('S04', C4, {'heroFace': add(HD4, [0, 1.5, 0]), 'heroTop': add(HD4, [0, 1.95, 0]), 'judgeFace': add(JU4, [0, 1.5, 0]), 'tray': add(TR4, [0, 0.9, 0]), 'trayR': add(TR4, [0.65, 0.9, 0.35]), 'railL': RAIL4(-0.3)})
kj4 = [k(0.0, clip='sit'), k(0.0, look=HEAD(TR4, 1.5)), TK(0.0, HANDS(JU4, JRY4, 0.45, 0.25, 1.38, 0.45, -0.25, 1.38), {'R': 'rest', 'L': 'rest'}, GRAVE, d=0.0),
       k(r(JG4 - 0.1), look=HEAD(HD4, 1.5), lookDur=0.22), TK(r(JG4 - 0.16), face={**STERN, 'lid': 0.5}, d=0.06, keep=True), TK(r(JG4 + 0.15), face=STERN, d=0.1, keep=True),   # the eyes go first, the head follows
       k(r(JG4 + 0.25), toon={'face': {**STERN, 'lid': 1.0}}, toonDur=0.14, keepPose=True), k(r(JG4 + 0.5), toon={'face': STERN}, toonDur=0.14, keepPose=True),   # a slow blink at him
       k(r(RN4 - 0.05), look=HEAD(TR4, 1.4), lookDur=0.06), TK(r(RN4 - 0.03), face={'lid': 0.75, 'mouth': 'O', 'brow': 0.9}, scl={'head': [1.25, 0.82, 1.1]}, bend={'spine': SP(0.3)}, d=0.05, e='out', keep=True),   # a squint at the empty tray: head squashed wide
       TK(r(RN4 + 0.3), scl={'head': [1, 1, 1]}, d=0.15, keep=True), *blink(0.4, GRAVE), *blink(1.7, GRAVE), *BREATHE(0.2, D4, 0.5)]
kh4 = [k(0.0, clip='sit'), k(0.0, look='camera'), TK(0.0, {'R': R5(add(HD4, [-0.2, 0.68, 0.42])), 'L': R5(add(HD4, [0.2, 0.68, 0.42]))}, {'R': 'rest', 'L': 'rest'}, {'lid': 0.0, 'mouth': 'line', 'brow': 0.15}, d=0.0),
       k(r(JG4 - 0.12), look=HEAD(JU4, 1.9), lookDur=0.1), k(r(JG4 + 0.3), look='camera', lookDur=0.12),   # a glance at the judge, back to us
       TK(r(RN4 + 0.05), face={'lid': 0.05, 'mouth': 'line', 'brow': 0.35}, sq=(1.06, 0.93, 1.06), d=0.15, keep=True), *blink(0.45, {'lid': 0.0, 'mouth': 'line', 'brow': 0.15}), *blink(1.75, {'lid': 0.15, 'mouth': 'line', 'brow': 0.3}), *BREATHE(0.1, D4, 0.5)]
st.shot('S04', 'whiteVoid', setOpts={'color': '#E3D3B5'}, look={'sunDir': [0.3, 0.9, 0.7]},
        actors=[act('mec', HD4, 0, 'sit', 'neutral', keys=kh4), judgeAct(kj4, JU4, JRY4)],
        props=[P('salleS04', 'pdRoom', pos=CRT, opts={'w': 9, 'd': 6, 'h': 3.6, 'wall': '#E3D3B5', 'floor': '#8A6A45', 'trim': '#6A4A30'}),
               P('boxS04', 'pdDock', pos=DK4, opts={'w': 1.5, 'depth': 1.2}), P('estradeS04', 'pdJudgeBench', pos=JB4, ry=JRY4, opts={'w': 2.4}),
               P('preuves4', 'pdTray', pos=TR4, ry=-15, scale=1.15),
               P('demiL4', 'pdBaguette', pos=RAIL4(-0.06), ry=8, opts={'half': 'L', 'len': 0.8}), P('demiR4', 'pdBaguette', pos=RAIL4(0.06), ry=-8, opts={'half': 'R', 'len': 0.8})], cams=[C4])
st.cue('sfx:gasp', 'S04', RN4, 0.15)

# 5: the prosecutor in a red gown thumps his table and points at the hero; in his other mitten he holds up a big iron ball and chain; the hero does
#    not move
D5 = st.dur('S05'); TH5 = 0.22; PT5 = r(st.at('S05', 'L05', 5) - 0.05); TH5b = r(st.at('S05', 'L05', 9) - 0.05)   # « grâce »: the ball dropped on the table
PC = [0.7, 0, 1.1]; PRY = 12   # three-quarters to us; the hero is off to his right
TB5 = off(PC, PRY, 0.5, -0.15, 0.0)   # a long table before him: the fist thumps its right end, the ball drops on its left end
C5 = cam(0.0, [2.6, 1.7, 3.6], [2.45, 1.7, 3.4], [-0.1, 1.35, 0.6], [-0.1, 1.35, 0.6], lens=56)
chk('S05', C5, {'pFace': add(PC, [0, 1.85, 0]), 'heroFace': add(HD, [0, 1.5, 0]), 'chainHand': off(PC, PRY, 0.3, -0.4, 2.05)})
TT5 = off(PC, PRY, 0.5, 0.3, 0.8); TL5 = off(PC, PRY, 0.5, -0.45, 0.8)
kp5 = [k(0.0, clip='stand'), k(0.0, look='camera'), k(r(PT5 - 0.1), look=HEAD(HD, 1.9), lookDur=0.08), k(r(PT5 + 0.6), look='camera', lookDur=0.15),   # he plays to us; one glare at the hero on « perpétuité » TK(0.0, {'R': R5(add(TT5, [0.1, 0.35, 0.1])), 'L': R5(off(PC, PRY, 0.2, -0.42, 2.1))}, {'R': 'fist', 'L': 'fist'}, STERN, d=0.0),   # the ball and chain held high out to his left
       TK(0.0, {'R': R5(off(PC, PRY, 0.25, 0.3, 2.25)), 'L': R5(off(PC, PRY, 0.2, -0.42, 2.1))}, d=0.0, keep=True), TK(r(TH5 - 0.12), {'R': R5(off(PC, PRY, 0.15, 0.3, 2.35))}, sq=(0.92, 1.1, 0.92), bend={'spine': SP(-0.15)}, d=0.1, keep=True),   # the fist up high (anticipation)...
       TK(TH5, {'R': R5(add(TT5, [0.1, 0.02, 0.1]))}, face={**STERN, 'mouth': 'clench'}, sq=(1.18, 0.82, 1.18), bend={'spine': SP(0.35)}, d=0.05, e='in', keep=True),   # ...the thump: squashed down onto it
       TK(r(TH5 + 0.2), {'R': R5(add(TT5, [0.1, 0.25, 0.1]))}, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.15, keep=True),
       TK(PT5, {'R': R5(lerp3(add(PC, [0, 1.65, 0]), add(HD, [0, 1.5, 0]), 0.3))}, {'R': 'point'}, bend={'spine': SP(0.15)},   # the arm dead straight at the hero
       face={'lid': 0.1, 'mouth': 'O', 'brow': -0.9, 'jaw': 0.8}, scl={'head': [1.3, 1.3, 1.3]}, d=0.06, e='out', keep=True),   # « perpétuité »: the head swells
       TK(r(PT5 + 0.25), face=STERN, scl={'head': [1, 1, 1]}, d=0.2, keep=True),
       TK(r(TH5b - 0.16), {'L': R5(off(PC, PRY, 0.3, -0.4, 2.45))}, bend={'spine': SP(-0.1)}, sq=(0.94, 1.08, 0.94), d=0.1, keep=True),   # the ball swung up (anticipation)...
       TK(TH5b, {'L': R5(add(TL5, [0.0, 1.12, 0.0]))}, face={'lid': 0.0, 'mouth': 'clench', 'brow': -1.0}, bend={'spine': SP(0.3)}, sq=(1.12, 0.9, 1.12), d=0.06, e='in', keep=True),   # ...and dropped on the table: CLANG
       TK(r(TH5b + 0.25), face=STERN, sq=(1, 1, 1), bend={'spine': SP(0.05)}, d=0.15, keep=True), *blink(1.0, STERN), *blink(2.2, STERN), *BREATHE(0.6, D5, 0.5)]
kh5 = [k(r(TH5b + 0.25), toon={'face': {**WORRY, 'lid': 1.0}}, toonDur=0.18, keepPose=True), k(r(TH5b + 0.6), toon={'face': WORRY}, toonDur=0.18, keepPose=True),   # one slow blink at the clang
       k(0.0, clip='sit'), k(0.0, look=HEAD(PC, 1.9)), TK(0.0, {'R': R5(off(HD, DRY, 0.42, 0.2, 0.68)), 'L': R5(off(HD, DRY, 0.42, -0.2, 0.68))}, {'R': 'rest', 'L': 'rest'}, WORRY, d=0.0),
       *blink(0.9, WORRY), *BREATHE(0.1, D5, 0.55)]
st.shot('S05', 'whiteVoid', setOpts={'color': '#E3D3B5'}, look={'sunDir': [0.3, 0.9, 0.7]},
        actors=[act('procureur', PC, PRY, 'stand', 'neutral', keys=kp5), act('mec', HD, DRY, 'sit', 'neutral', keys=kh5)],
        props=[*courtProps('S05'), P('table5', 'table', pos=TB5, ry=PRY, opts={'w': 1.6, 'd': 0.6, 'h': 0.78, 'color': '#8A6A45'}, keys=[k(TH5, squash=[1.12, 0.78, 1.12], dur=0.4), k(TH5b, squash=[1.12, 0.78, 1.12], dur=0.4)]),
               P('robe5', 'pdRobe', on={'actor': 'procureur', 'joint': 'hips', 'offset': [0, 0.05, 0]}, opts={'L': 0.95, 'color': '#8E3A28'}), P('rabat5', 'pdRobe', on={'actor': 'procureur', 'joint': 'torso', 'offset': [0, 0.42, 0.17]}, opts={'bib': True}),
               P('boulet5', 'pdBallChain', on={'actor': 'procureur', 'hand': 'L', 'offset': [0, -0.04, 0], 'hang': True}, opts={'r': 0.2, 'n': 8}),
               P('demiL5', 'pdBaguette', pos=RAIL(-0.28), ry=DRY, opts={'half': 'L', 'len': 0.8}), P('demiR5', 'pdBaguette', pos=RAIL(0.28), ry=DRY, opts={'half': 'R', 'len': 0.8})], cams=[C5])
st.cue('thud', 'S05', TH5, 0.45); st.cue('sfx:rattleShort', 'S05', 0.3, 0.2); st.cue('sfx:rattle', 'S05', PT5, 0.25); st.cue('clang', 'S05', TH5b, 0.45)

# 6: the big courtroom clock fills the frame, no figure, both hands straight up; the gavel bangs. The minute hand jumps one visible notch with a tick
#    and a wobble. Cut: a dark-suited torso with the lemon tie leans in and slaps a fresh scroll on the dock rail; he takes it and walks out through
#    the swing doors with his scroll and his baguette halves. GRACIÉ card
D6 = st.dur('S06'); GR6 = st.at('S06', 'L06', 3); CUT6 = r(GR6 + 0.3); CUT6c = r(GR6 + 0.78)
CK = [0, 2.2, -2.95]
C6 = cam(0.0, [0.0, 2.36, -0.97], [0.0, 2.36, -1.07], [0.0, 2.36, -2.95], [0.0, 2.36, -2.95], lens=44)   # the hub at 60 %, the noon mark at 27 %: under the card band
DB = [40.0, 0, 0.0]; HB = add(DB, [0.1, 0, -0.1])
TSB0, TSB1 = add(DB, [2.4, 0, 0.75]), add(DB, [1.25, 0, 0.75])
SCB0, SCB1 = add(DB, [1.35, 1.5, 1.15]), add(DB, [0.3, 1.04, 0.35])
C6b = cam(CUT6, add(DB, [1.0, 1.25, 3.7]), add(DB, [0.9, 1.25, 3.5]), add(DB, [-0.1, 1.45, 0.0]), add(DB, [-0.2, 1.45, 0.0]), lens=50)
DD = [80.0, 0, 0.0]; HD0, HD1 = add(DD, [0.0, 0, -0.9]), add(DD, [0.15, 0, 1.0])   # the swing doors, from the corridor side: he bursts through toward us
SWING6 = r(CUT6c + 0.3)
C6c = cam(CUT6c, add(DD, [0.6, 1.45, 4.2]), add(DD, [0.55, 1.45, 4.0]), add(DD, [0.1, 1.3, 0.0]), add(DD, [0.1, 1.3, 0.0]), lens=46)
chk('S06', C6, {'noon': add(CK, [0, 0.53, 0.04]), 'hub': CK, 'clockBot': add(CK, [0, -0.66, 0]), 'clockL': add(CK, [-0.66, 0, 0])})
chk('S06b', C6b, {'heroTop': add(HB, [0, 2.35, 0]), 'bumper': add(TSB1, [0, 2.1, 0]), 'tie': add(TSB1, [0, 1.3, 0.5]), 'rail': SCB1})
chk('S06c', C6c, {'lintel': add(DD, [0, 2.4, 0]), 'heroTop@end': add(HD1, [0, 2.35, 0]), 'heroFeet@end': HD1, 'doorL': add(DD, [-0.75, 1.0, 0])})
T6 = r(CUT6 + 0.12); TAKE6 = r(CUT6 + 0.36)
kh6 = [k(0.0, clip='stand'), k(0.0, look=HEAD(add(DB, [1.5, 0, 1.5]), 2.0)),
       TK(0.0, {'R': R5(off(HB, 0, 0.3, 0.3, 1.1)), 'L': R5(off(HB, 0, 0.3, -0.3, 1.1))}, {'R': 'rest', 'L': 'grip'}, WORRY, d=0.0),
       k(r(T6 - 0.05), look=HEAD(SCB1, 1.9), lookDur=0.06),
       TK(r(T6 + 0.02), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(1.15, 0.82, 1.15), d=0.03, e='out', keep=True), TK(r(T6 + 0.1), sq=(0.94, 1.08, 0.94), d=0.06, keep=True), TK(r(T6 + 0.2), face=WORRY, sq=(1, 1, 1), d=0.08, keep=True),   # the slap makes him jump
       TK(r(TAKE6 - 0.12), {'R': R5(add(SCB1, [0, 0.06, 0.02]))}, {'R': 'grip'}, d=0.1, keep=True), TK(r(TAKE6 + 0.05), {'R': R5(off(HB, 0, 0.35, 0.3, 1.3))}, face={**WORRY, 'mouth': 'smile'}, d=0.1, keep=True),
       k(CUT6c, to=HD0, dur=0.01, clip='walk', face='keep'), k(r(CUT6c + 0.01), face=0, turn=0.01),
       k(r(CUT6c + 0.02), to=HD1, dur=r(D6 - CUT6c), clip='walk', ease='linear', face='keep', params={'freq': 2.4}), k(CUT6c, look='camera', lookDur=0.01),
       *WALKHANDS(r(CUT6c + 0.02), r(D6 - CUT6c), [HD0, HD1], {'R': (0.3, 0.3, 1.3), 'L': (0.3, -0.3, 1.1)}),
       TK(SWING6, sq=(1.1, 0.92, 1.1), face={**WORRY, 'mouth': 'smile', 'brow': 0.8}, d=0.05, keep=True), TK(r(SWING6 + 0.15), sq=(1, 1, 1), d=0.1, keep=True)]   # through the doors, scroll held up
st.shot('S06', 'whiteVoid', setOpts={'color': '#E3D3B5'}, look={'sunDir': [0.3, 0.9, 0.7]},
        actors=[act('mec', HB, 0, 'stand', 'neutral', keys=kh6)],
        props=[P('salleS06', 'pdRoom', pos=CRT, opts={'w': 9, 'd': 6, 'h': 3.6, 'wall': '#E3D3B5', 'floor': '#8A6A45', 'trim': '#6A4A30'}), P('horloge6', 'pdClock', pos=CK, opts={'r': 0.62, 'jumpAt': GR6}),
               P('salleB6', 'pdRoom', pos=DB, opts={'w': 9, 'd': 5, 'h': 3.6, 'wall': '#E3D3B5', 'floor': '#8A6A45', 'trim': '#6A4A30'}),
               P('box6', 'pdDock', pos=DB, opts={'w': 1.5}),
               P('couloir6', 'pdGround', pos=DD, opts={'w': 12, 'd': 10, 'color': '#A88A64'}), P('battants6', 'pdSwingDoors', pos=DD, opts={'swingAt': SWING6}),
               P('bousculeur6', 'pdPresident', pos=TSB0, ry=-70, opts={'round': 1.15, 'look': [[0, PI]], 'pat': [T6], 'bounce': [T6], 'flap': 2.0},   # the same round body, head turned away: it leans in and slaps the scroll down
                 keys=[k(0.0, visible=False), k(CUT6, visible=True), k(CUT6, to=TSB1, dur=0.12, ease='out'), k(T6, squash=[1.15, 0.88, 1.15], dur=0.25), k(r(T6 + 0.12), to=TSB0, dur=0.25, ease='in')]),
               P('parchemin6', 'pdScroll', pos=SCB0, rot=[-1.5708, 0, 0], opts={'w': 0.42, 'h': 0.56}, keys=[k(0.0, visible=False), k(CUT6, visible=True), k(CUT6, to=SCB1, dur=0.12, ease='in'), k(T6, squash=[1.2, 0.6, 1.2], dur=0.25),
                 k(TAKE6, attach='mec', hand='R', offset=[0.0, 0.2, 0.06], rot=[0, 0, 0])]),
               *HALVES('S06', both='L')], cams=[C6, C6b, C6c])
st.cue('clack', 'S06', 0.2, 0.5); st.cue('clack', 'S06', 0.45, 0.4); st.cue('sfx:tick', 'S06', GR6, 0.6); st.cue('thud', 'S06', T6, 0.4); st.cue('sfx:squeak', 'S06', SWING6, 0.35); st.cue('sfx:squeak', 'S06', r(SWING6 + 0.35), 0.2)
st.card('S06', 'GRACIÉ', at=GR6)

# ================================================================= S07
# 7: a street: two passers-by bump shoulders; one bows and says « pardon »; a clerk pops out from behind a lamppost and hands him a big sealed scroll
D7 = st.dur('S07'); BMP7 = 0.3; BOW7 = r(st.at('S07', 'L07', 2) - 0.25); POP7 = r(BOW7 + 0.45); GIVE7 = r(POP7 + 0.45)
FAC7 = [0, 0, -2.6]; LP7 = [-1.0, 0, -0.6]
PA0, PA1 = [1.8, 0, 0.3], [0.6, 0, 0.3]; PB0, PB1 = [-0.9, 0, -0.15], [0.2, 0, -0.15]
CL0, CL1 = [-1.05, 0, -0.75], [-0.45, 0, 0.15]
C7 = fcam(0.0, [0.5, 1.5, 5.2], {'paTop': add(PA1, [0, 2.2, 0]), 'pbTop': add(PB1, [0, 2.2, 0]), 'clTop': add(CL1, [-0.3, 2.1, 0]), 'lamp': add(LP7, [0, 2.6, 0]), 'knee': add(PA1, [0.4, 0.9, 0.2])}, top=0.08, bottom=0.74, push=0.25)
chk('S07', C7, {'paFace': add(PA1, [0, 1.85, 0]), 'pbFace': add(PB1, [0, 1.85, 0]), 'clFace@pop': add(CL0, [0, 1.8, 0]), 'clFace': add(CL1, [0, 1.8, 0])})
SC7 = lerp3(add(CL1, [0, 1.45, 0]), add(PA1, [0, 1.45, 0]), 0.5)   # the scroll handed over between them, against the plain wall
kpa = [k(0.0, clip='walk'), k(0.0, to=PA1, dur=BMP7, clip='walk', ease='linear', params={'freq': 2.0}), k(BMP7, clip='stand'), k(0.0, look=HEAD(PB1, 1.9)),
       TK(BMP7, face={'lid': 0.0, 'mouth': 'clench', 'brow': 0.9}, sq=(1.2, 0.85, 1.0), bend={'spine': SP(-0.2, -0.4)}, d=0.04, e='out', keep=True), TK(r(BMP7 + 0.15), face=WORRY, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.12, keep=True),
       k(BOW7, face=-90, turn=0.15), k(r(BOW7 + 0.05), clip='bow', blend=0.12), *TALK(r(BOW7 + 0.18), WORRY, 3),
       k(r(POP7 + 0.05), clip='stand', blend=0.15), k(r(POP7 + 0.05), look=HEAD(CL1, 1.85), lookDur=0.12), k(r(POP7 + 0.1), face=yaw(PA1, CL1), turn=0.2),
       TK(r(GIVE7 - 0.08), {'R': R5(add(SC7, [0.05, -0.2, 0.0]))}, {'R': 'grip'}, d=0.12),
       TK(r(GIVE7 + 0.2), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'jaw': 1.0}, scl={'head': [0.85, 1.25, 0.85]}, d=0.05, e='out', keep=True), TK(r(GIVE7 + 0.4), scl={'head': [1, 1, 1]}, face=WORRY, d=0.12, keep=True),
       *blink(r(GIVE7 + 0.5), WORRY), *BREATHE(r(GIVE7 + 0.4), D7, 0.35)]
kpb = [k(0.0, clip='walk'), k(0.0, to=PB1, dur=BMP7, clip='walk', ease='linear', params={'freq': 2.0}), k(BMP7, clip='stand'), k(0.0, look=HEAD(PA1, 1.9)),
       TK(BMP7, face={'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, scl={'head': [1.3, 0.8, 1.0]}, d=0.04, e='out', keep=True), TK(r(BMP7 + 0.15), face=CALM, scl={'head': [1, 1, 1]}, d=0.12, keep=True),
       k(r(BMP7 + 0.35), to=[2.8, 0, -0.5], dur=1.5, clip='walk', ease='in', params={'freq': 1.8}), *blink(0.8, CALM)]   # walks on behind him, out right
kcl = [k(0.0, clip='stand'), k(0.0, visible=False), k(POP7, visible=True), k(0.0, look=HEAD(PA1, 1.9)),
       TK(0.0, {'R': R5(off(CL0, 60, 0.4, 0.15, 1.35))}, {'R': 'grip'}, HAPPY, bend={'spine': SP(0.0, -0.6)}, d=0.0),   # hidden behind the lamppost, leaning
       k(POP7, to=add(CL0, [0.35, 0, 0.1]), dur=0.07, clip='stand', ease='out', face='keep'),
       TK(POP7, sq=(1.45, 0.78, 0.9), bend={'spine': SP(0.0, 0.7)}, d=0.03, e='out', keep=True), TK(r(POP7 + 0.08), sq=(0.88, 1.15, 0.95), bend={'spine': SP(0.0, -0.25)}, d=0.06, keep=True),   # pops out sideways, stretched, and overshoots
       TK(r(POP7 + 0.18), sq=(1, 1, 1), bend={'spine': SP(0.0, 0.0)}, d=0.08, keep=True),
       k(r(POP7 + 0.12), to=CL1, dur=0.25, clip='walk', ease='out', params={'freq': 2.6}), k(r(POP7 + 0.37), clip='stand'),
       TK(r(POP7 + 0.2), {'R': R5(add(SC7, [-0.05, -0.2, 0.0]))}, d=0.15, keep=True), TK(r(GIVE7 + 0.12), {'R': R5(off(CL1, 60, 0.3, 0.25, 1.05))}, {'R': 'rest'}, d=0.15, keep=True),
       *blink(r(GIVE7 + 0.3), HAPPY), *BREATHE(r(GIVE7 + 0.3), D7, 0.35), k(r(GIVE7 + 0.55), look='camera', lookDur=0.2)]
st.shot('S07', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('passant1', PA0, -90, 'walk', 'neutral', keys=kpa), act('passant2', PB0, 90, 'walk', 'neutral', keys=kpb), act('greffier', CL0, 60, 'stand', 'neutral', keys=kcl)],
        props=[P('sol7', 'pdGround', pos=[0, 0, 0], opts={'kerb': 2.5}), P('facade7', 'pdFacade', pos=FAC7, opts={'w': 14, 'color': '#F2DCCB'}), P('lampe7', 'streetLamp', pos=LP7, opts={'height': 3.6}),
               P('parchemin7', 'pdScroll', on={'actor': 'greffier', 'hand': 'R', 'offset': [0.0, 0.2, 0.06], 'rot': [0, 0, 0]}, opts={'w': 0.38, 'h': 0.5},
                 keys=[k(0.0, visible=False), k(POP7, visible=True), k(GIVE7, attach='passant1', hand='R', offset=[0.0, 0.2, 0.06], rot=[0, 0, 0])])], cams=[C7])
st.cue('thud', 'S07', BMP7, 0.35); st.cue('sfx:pop', 'S07', POP7, 0.4); st.cue('sfx:paper', 'S07', GIVE7, 0.3)

# ================================================================= S08
# 8: a metro carriage, five passengers: they jostle, bow and mouth « pardon » together; a judge in a black robe, large in the foreground on a folding
#    seat, bangs his gavel twice for each one and scrolls pile up on his lap; the hero stands in the corner with his two halves, mouth shut
D8 = st.dur('S08'); BW8 = [0.2, 0.62, 1.04, 1.46, 1.88]; BANG8 = [r(b + d_) for b in BW8 for d_ in (0.14, 0.3)]   # each passenger bows in turn; bang-bang after each
JG8 = [2.25, 0, -0.5]; JRY8 = 80; LAP8 = off(JG8, JRY8, 0.33, 0.0, 0.6)   # the judge three-quarter in the lower right corner
PS8 = [[-0.6, 0, -0.3], [-0.9, 0, 0.3], [-1.4, 0, -0.05], [-1.8, 0, -0.4], [-2.2, 0, 0.25]]   # the five passengers in the clear lane behind
H8 = [0.4, 0, 0.75]; HRY8 = 110
C8 = cam(0.0, [3.85, 2.0, 0.15], [3.82, 2.0, 0.15], [-0.5, 1.0, -0.25], [-0.5, 1.0, -0.25], lens=70)   # high: the judge low in the corner, the lane of bows clear beside him
chk('S08', C8, {'judgeTop': add(JG8, [0, 1.95, 0]), 'lap': LAP8, 'pileTop': add(LAP8, [0, 0.55, 0]), 'heroFace': add(H8, [0, 1.95, 0]), **{f'p{i}': add(p, [0, 1.85, 0]) for i, p in enumerate(PS8)}})
UP8 = off(JG8, JRY8, 0.3, 0.3, 1.75); HIT8 = add(LAP8, [0.0, 0.1, 0.0])
kj8 = [k(0.0, clip='sit'), k(0.0, look='camera'), TK(0.0, {'R': R5(off(JG8, JRY8, 0.4, 0.28, 1.15)), 'L': R5(add(LAP8, [0.05, 0.1, -0.15]))}, {'R': 'grip', 'L': 'rest'}, STERN, d=0.0)]
JFX = [dict(sq=(1.15, 0.86, 1.15)), dict(bend={'spine': SP(0.35)}), dict(sq=(1.08, 0.9, 1.08), bend={'spine': SP(0.2, 0.2)}), dict(sq=(1.2, 0.82, 1.2), bend={'spine': SP(0.3)}), dict(sq=(0.95, 1.06, 0.95), bend={'spine': SP(0.25, -0.2)})] * 2   # a different body take on each bang (the head stays)
for j, b in enumerate(BANG8):
    kj8 += [TK(r(b - 0.08), {'R': R5(UP8)}, bend={'spine': SP(-0.1)}, d=0.05, e='out', keep=True),   # the gavel up...
            TK(b, {'R': R5(HIT8)}, d=0.035, e='in', keep=True, **{'face': {**STERN, 'mouth': 'clench'}, **JFX[j]}),   # ...bang
            TK(r(b + 0.05), {'R': R5(off(JG8, JRY8, 0.42, 0.28, 1.25))}, face=STERN, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.04, keep=True)]
kj8 += [*blink(1.2, STERN), *blink(2.35, STERN), *BREATHE(2.1, D8, 0.4)]
pas = []
for i, p in enumerate(PS8):
    ry = 90 + (25 if i % 2 == 0 else -25); ks = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, face=CALM, d=0.0)]
    b = BW8[i]
    ks += [TK(r(b - 0.18), bend={'spine': SP(0.0, 0.35 if i % 2 else -0.35)}, sq=(1.06, 0.95, 1.06), d=0.08, keep=True),   # jostled...
           k(b, clip='bow', blend=0.06), *TALK(r(b + 0.05), WORRY, 2, 0.07), TK(r(b + 0.14), sq=(1.08, 0.92, 1.08), d=0.05, keep=True),   # ...bows, « pardon »
           k(r(b + 0.4), clip='stand', blend=0.12), TK(r(b + 0.4), bend={'spine': SP(0.0)}, sq=(1, 1, 1), d=0.12, keep=True)]
    ks += [*blink(r(0.9 + 0.1 * i), CALM), *BREATHE(2.0, D8, 0.4)]
    pas.append(act(f'voyageur{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
kh8 = [k(0.0, clip='stand'), k(0.0, look=HEAD(PS8[1], 1.9)), TK(0.0, {'R': R5(off(H8, HRY8, 0.35, 0.36, 1.2)), 'L': R5(off(H8, HRY8, 0.35, -0.36, 1.2))}, {'R': 'grip', 'L': 'grip'}, SHUT, d=0.0),
       k(1.0, look='camera', lookDur=0.2), k(1.9, look=HEAD(JG8, 1.6), lookDur=0.15), *blink(1.3, SHUT), *blink(2.4, SHUT), *BREATHE(0.2, D8, 0.5)]
st.shot('S08', 'whiteVoid', setOpts={'color': '#2A3038'}, look={'sunDir': [0.2, 0.9, 0.4]},
        actors=[act('juge', JG8, JRY8, 'sit', 'neutral', keys=kj8), *pas, act('mec', H8, HRY8, 'stand', 'neutral', keys=kh8)],
        props=[P('rame8', 'metroCar', pos=[0, 0, 0], opts={'len': 8, 'sway': [0.006, 7]}), P('strapontin8', 'table', pos=add(JG8, [0, 0, -0.05]), opts={'w': 0.45, 'd': 0.4, 'h': 0.47, 'color': '#3A3D44', 'legs': '#2A2C31'}),
               P('maillet8', 'gavel', on={'actor': 'juge', 'hand': 'R'}, scale=1.5, keys=[k(b, squash=[1.25, 0.75, 1.25], dur=0.18) for b in BANG8]),
               P('pile8', 'pdScrollPile', pos=add(LAP8, [0, -0.02, 0]), ry=JRY8 - 90, opts={'h': 0.25, 'w': 0.3, 'r': 0.06, 'perRow': 2, 'adds': BANG8}),
               *HALVES('S08')], cams=[C8])
for b in BANG8: st.cue('clack', 'S08', b, 0.4)
st.cue('engine', 'S08', 0.0, 0.15)

# ================================================================= S09
# 9: the presidential office: a conveyor belt carries scrolls past the president, who signs each in one stroke; behind him signed scrolls pile up to
#    the ceiling. Cut: close on his chest as he proudly straightens the big lemon tie while, through the window behind, five people cheer and throw
#    flowers
D9 = st.dur('S09'); CUT9 = r(st.at('S09', 'L09', 8) - 0.1)
PR9 = [0, 0, -0.35]; CV9 = [0, 0, 0.42]
SIGN9 = []; _t = 0.05; _d = 0.42
while _t + _d < CUT9 - 0.05: SIGN9.append([r(_t), r(_t + _d * 0.85)]); _t += _d; _d = max(0.2, _d * 0.85)   # one big loop per parchment, faster and faster
C9 = fcam(0.0, [0.2, 1.65, 3.4], {'belt': add(CV9, [0.6, 0.9, 0.3]), 'beltL': add(CV9, [-0.6, 0.9, 0.3]), 'pres': add(PR9, [0, 2.15, 0])}, top=0.1, bottom=0.74, push=0.25)
chk('S09', C9, {'presFace': add(PR9, [0, 1.72, 0]), 'tie': add(PR9, [0, 1.2, 0.45]), 'pileTop': [-0.95, 3.0, -1.2]})
OF9 = [40.0, 0, 0.0]; PR9B = add(OF9, [0.0, 0, -0.2]); WIN9 = add(OF9, [0.0, 2.36, -1.49])   # the window high behind him: the five cheering over his head
C9b = cam(CUT9, add(OF9, [0.05, 1.6, 2.2]), add(OF9, [0.05, 1.62, 2.05]), add(OF9, [0.0, 1.47, -0.2]), add(OF9, [0.0, 1.49, -0.2]), lens=44)
chk('S09b', C9b, {'face': add(PR9B, [0, 1.72, 0]), 'top': add(PR9B, [0, 2.05, 0]), 'tieKnot': add(PR9B, [0, 1.4, 0.45]), 'tieEnd': add(PR9B, [0, 0.95, 0.5]), 'winL': add(WIN9, [-0.46, 0, 0]), 'winR': add(WIN9, [0.46, 0, 0]), 'winTop': add(WIN9, [0, 0.25, 0])})
st.shot('S09', 'whiteVoid', setOpts={'color': '#E6DCCB'}, look={'sunDir': [0.3, 0.9, 0.8]}, actors=[],
        props=[P('bureau9', 'pdRoom', pos=[0, 0, 0], opts={'w': 6, 'd': 4, 'h': 3.1, 'wall': '#E6DCCB', 'floor': '#B58E66'}),
               P('pile9a', 'pdScrollPile', pos=[-0.85, 0, -1.2], opts={'h': 1.9, 'w': 0.7, 'perRow': 4, 'adds': [r(0.1 + 0.11 * n) for n in range(18)]}), P('pile9b', 'pdScrollPile', pos=[0.85, 0, -1.2], opts={'h': 1.9, 'w': 0.7, 'perRow': 4, 'adds': [r(0.15 + 0.11 * n) for n in range(18)]}),   # the piles grow while he signs
               P('tapis9', 'pdConveyor', pos=CV9, opts={'len': 3.0, 'speed': 0.6, 'signX': 0.05}),
               P('president9', 'pdPresident', pos=PR9, opts={'round': 1.1, 'pen': True, 'signBig': True, 'sign': SIGN9, 'bounce': [s[1] for s in SIGN9], 'smile': [[0, 0.8], [1.0, 1.0], [1.6, 0.8]], 'blink': [0.9, 1.9],
                 'look': [[0, 0.3], [0.8, 0.3], [0.95, 0.0], [1.5, 0.0], [1.65, 0.3]]}),
               P('bureau9b', 'pdRoom', pos=OF9, opts={'w': 4, 'd': 3, 'h': 3.1, 'wall': '#E6DCCB', 'floor': '#B58E66', 'window': {'x': 0.0, 'y': 2.36, 'w': 0.95, 'h': 0.5}}),
               P('foule9', 'pdCheer', pos=WIN9, opts={'w': 0.93, 'h': 0.48}),
               P('president9b', 'pdPresident', pos=PR9B, opts={'round': 1.1, 'straighten': [[r(CUT9 + 0.06), r(CUT9 + 0.85)]], 'puff': [r(CUT9 + 0.9)], 'smile': [[0, 0.8], [r(CUT9 + 0.85), 1.0]], 'blink': [r(CUT9 + 0.5), r(CUT9 + 1.5)],
                 'look': [[0, 0.0], [r(CUT9 + 0.9), 0.0], [r(CUT9 + 1.05), -0.25], [r(CUT9 + 1.6), -0.25], [r(CUT9 + 1.75), 0.0]]})], cams=[C9, C9b])
for s in SIGN9: st.cue('sfx:paper', 'S09', s[0], 0.2)
st.cue('sfx:choir', 'S09', CUT9, 0.2); st.cue('sfx:stretch', 'S09', r(CUT9 + 0.1), 0.2)

# ================================================================= S10
# 10: a prison yard in bright daylight: five inmates in striped outfits face a guard and bow together, saying « pardon »; the big gate swings open
#     and they walk out in single file
D10 = st.dur('S10'); BOW10 = r(st.at('S10', 'L10', 4) - 0.25); GATE10 = r(st.at('S10', 'L10', 7) - 0.1)
PZ10 = [0, 0, -3.0]; GD10 = [1.1, 0, 0.9]; GRY10 = -130
IN10 = [[-1.3, 0, -0.2], [-0.75, 0, -0.1], [-0.2, 0, 0.0], [0.35, 0, -0.1], [0.9, 0, -0.2]]
C10 = cam(0.0, [0.3, 1.7, 6.2], [0.3, 1.7, 5.85], [0.0, 1.35, -0.6], [0.0, 1.35, -0.6], lens=54)
chk('S10', C10, {**{f'in{i}': add(p, [0, 1.85, 0]) for i, p in enumerate(IN10)}, 'gdFace': add(GD10, [0, 1.85, 0]), 'gate': [0, 1.3, -2.0]})
kin = []
for i, p in enumerate(IN10):
    t0 = r(GATE10 + 0.2 + 0.28 * i)   # one by one, in single file
    path = [[-0.2, 0, -1.3], [-0.2, 0, -4.5]]
    ks = [k(0.0, clip='stand'), k(0.0, look=HEAD(GD10, 1.9)), TK(0.0, face=SAD, d=0.0),
          k(BOW10, clip='bow', blend=0.1), *TALK(r(BOW10 + 0.15), SAD, 3), TK(r(BOW10 + 0.3), sq=(1.1, 0.9, 1.1), d=0.08, keep=True),   # all bowed together
          k(r(BOW10 + 0.65), clip='stand', blend=0.15), TK(r(BOW10 + 0.65), sq=(1, 1, 1), d=0.12, keep=True),
          k(GATE10, look=HEAD([0, 0, -3.0], 1.9), lookDur=0.1), TK(GATE10, face={**HAPPY, 'brow': 1.0}, scl={'head': [1.15, 1.15, 1.15]}, d=0.05, e='out', keep=True), TK(r(GATE10 + 0.2), scl={'head': [1, 1, 1]}, face=HAPPY, d=0.12, keep=True),
          k(t0, path=path, clip='walk', speed=1.8, params={'freq': 2.0}), *blink(r(0.4 + 0.07 * i), SAD), *BREATHE(0.1, BOW10, 0.4)]
    kin.append(act(f'detenu{i + 1}', p, 0, 'stand', 'neutral', keys=ks))
kg10 = [k(r(GATE10 - 0.05), clip='doubleTakeToon', params={'side': -1, 'beat': 0.25, 'pop': 0.8, 'jaw': 0.5}), k(r(GATE10 + 0.85), clip='stand', blend=0.2), k(r(GATE10 + 0.3), look=HEAD([0, 0, -3.0], 2.0), lookDur=0.08),   # a double take at the gate opening
        k(0.0, clip='stand'), k(0.0, look=HEAD(IN10[2], 1.9)), TK(0.0, face=STERN, d=0.0), TK(r(BOW10 + 0.3), face={**STERN, 'brow': 0.6}, sq=(0.95, 1.06, 0.95), d=0.1, keep=True),
        TK(r(BOW10 + 0.7), face=SAD, sq=(1, 1, 1), d=0.15, keep=True), *blink(0.6, STERN), *blink(2.4, SAD), *BREATHE(0.2, D10, 0.5)]
st.shot('S10', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[*kin, act('gardien', GD10, GRY10, 'stand', 'neutral', keys=kg10)],
        props=[P('cour10', 'pdGround', pos=[0, 0, 0], opts={'color': '#C9C2B3'}),
               *[P(f'rayures10_{i + 1}', 'pdStripes', on={'actor': f'detenu{i + 1}', 'joint': 'torso', 'offset': [0, 0.66, 0]}, opts={'w': 0.6 * [1.0, 1.15, 0.9, 1.05, 0.95][i], 'd': 0.38, 'h': 0.9}) for i in range(5)], P('prison10', 'pdPrison', pos=PZ10, ry=180, opts={'w': 10, 'lit': False, 'gate': [[0, 0], [GATE10, 0], [r(GATE10 + 0.5), 1]]})], cams=[C10])
st.cue('sfx:clink', 'S10', GATE10, 0.4); st.cue('sfx:squeak', 'S10', r(GATE10 + 0.1), 0.3)

# ================================================================= S11
# 11: the prison front, windows lit warm yellow: the director in a suit, last one out, shuts the gate and leaves the big key in it, flips a big wall
#     switch; the windows go from yellow to grey one row at a time
D11 = st.dur('S11'); FLIP11 = r(st.at('S11', 'L11', 5) - 0.05)
PZ11 = [0, 0, -2.0]; SW11 = [1.6, 1.45, -1.96]   # a BIG switch beside the gate
DIR0, DIR1 = [0.0, 0, -2.6], [0.75, 0, -1.2]; DIR2 = [1.05, 0, -1.35]; DIR3 = [-1.9, 0, 1.3]   # beside the switch, facing us; he leaves toward us, out left
C11 = cam(0.0, [1.2, 1.05, 2.8], [1.1, 1.06, 2.6], [0.5, 2.6, -2.0], [0.5, 2.6, -2.0], lens=72)   # low and wide, closer: his face, the key, the switch and the three rows
chk('S11', C11, {'dirFace': add(DIR1, [0, 1.85, 0]), 'switch': SW11, 'key': [0.9, 1.2, -1.6], 'dir3': add(DIR3, [0, 1.85, 0])})
kd11 = [k(0.0, clip='walk'), k(0.0, to=DIR1, dur=0.5, clip='walk', ease='out', params={'freq': 2.0}), k(0.5, clip='stand'), k(0.0, look='camera'), TK(0.0, face=CALM, d=0.0),
        k(0.5, face=-150, turn=0.15), k(0.5, look=HEAD([0.8, 0, -1.6], 1.9), lookDur=0.12),
        TK(0.5, {'R': R5([0.75, 1.25, -1.62])}, {'R': 'grip'}, d=0.12), TK(1.0, {'R': R5([0.95, 1.2, -1.75])}, d=0.45, keep=True),   # pushes the gate shut, the key stays in it
        TK(1.1, {'R': R5(off(DIR1, 0, 0.2, 0.3, 1.0))}, {'R': 'rest'}, d=0.15, keep=True),
        k(1.1, to=DIR2, dur=0.3, clip='walk', ease='inOut', params={'freq': 2.2}), k(1.4, clip='stand'), k(1.12, face=25, turn=0.2), k(1.2, look='camera', lookDur=0.1),
        TK(r(FLIP11 - 0.3), {'L': R5(add(SW11, [0.1, 0.8, 0.25]))}, {'L': 'open'}, bend={'spine': SP(-0.1, -0.2)}, d=0.15, keep=True),   # the arm wound up high...
        TK(FLIP11, {'L': R5(add(SW11, [0, -0.05, 0.1]))}, {'L': 'fist'}, bend={'spine': SP(0.1, 0.25)}, d=0.06, e='in', keep=True), k(r(FLIP11 - 0.1), look=HEAD(SW11, 1.9), lookDur=0.06), k(r(FLIP11 + 0.15), look='camera', lookDur=0.1),   # ...a wide arc down onto the lever
        TK(r(FLIP11 + 0.04), face={'lid': 0.0, 'mouth': 'smile', 'brow': 1.0}, sq=(1.12, 0.88, 1.12), scl={'head': [1.2, 0.85, 1.2]}, d=0.04, e='out', keep=True),   # the click: a little satisfied squash
        TK(r(FLIP11 + 0.2), face=CALM, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.12, keep=True), TK(r(FLIP11 + 0.2), {'L': R5(off(DIR2, 25, 0.05, -0.3, 0.95))}, {'L': 'rest'}, d=0.18, keep=True),
        k(r(FLIP11 + 0.3), look=HEAD([0, 0, -2], 3.0), lookDur=0.15), k(r(FLIP11 + 0.42), look=HEAD(DIR3, 1.9), lookDur=0.12), k(r(FLIP11 + 0.45), to=DIR3, dur=1.1, clip='walk', ease='in', params={'freq': 1.8}),
        *WALKHANDS(r(FLIP11 + 0.45), 1.1, [DIR2, DIR3], {'R': (0.05, 0.3, 0.95), 'L': (0.05, -0.3, 0.95)}), *blink(1.9, CALM)]   # the arm down, a glance up at the dark windows, and off
st.shot('S11', 'whiteVoid', setOpts={'color': '#45507A'}, look={'sunDir': [0.5, 0.5, 0.8]},   # dusk: a deep blue sky, the same grey stone as in S10
        actors=[act('directeur', DIR0, 0, 'walk', 'neutral', keys=kd11)],
        props=[P('rue11', 'pdGround', pos=[0, 0, 0], opts={'color': '#7A726C', 'kerb': 2.0}), P('prison11', 'pdPrison', pos=PZ11, opts={'w': 7, 'key': True, 'offAt': r(FLIP11 + 0.06), 'offEvery': 0.25, 'gate': [[0, 1], [0.5, 1], [1.0, 0]]}),
               P('interrupteur11', 'pdSwitch', pos=SW11, scale=2.6, opts={'flipAt': FLIP11})], cams=[C11])
st.cue('sfx:clink', 'S11', 1.0, 0.35); st.cue('clack', 'S11', FLIP11, 0.5)

# ================================================================= S12
# 12: a press room, a plain blue backdrop: the minister holds up a big white board with « PARDON » struck through by one diagonal red line;
#     flashbulbs. INTERDIT card
D12 = st.dur('S12'); IT12 = st.at('S12', 'L12', 3)
MN12 = [0, 0, -0.4]; PD12 = [0, 0, 0.15]; BD0, BD1 = [0, 1.0, 0.42], [0, 1.38, 0.48]
C12 = fcam(0.0, [0.25, 1.65, 3.8], {'top': add(MN12, [0, 2.7, 0]), 'boardL': add(BD1, [-0.6, 0.35, 0]), 'boardR': add(BD1, [0.6, -0.35, 0]), 'pod': add(PD12, [0.5, 1.15, 0.3])}, top=0.1, bottom=0.74, push=0.2)
chk('S12', C12, {'face': add(MN12, [0, 1.85, 0]), 'board': BD1})
FL12 = [0.15, 0.62, IT12, r(IT12 + 0.55)]
km12 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(add(BD0, [-0.6, 0.05, 0.04])), 'L': R5(add(BD0, [0.6, 0.05, 0.04]))}, {'R': 'grip', 'L': 'grip'}, STERN, d=0.0),
        TK(0.06, {'R': R5(add(BD1, [-0.6, 0.05, 0.04])), 'L': R5(add(BD1, [0.6, 0.05, 0.04]))}, d=0.22, e='out', keep=True),   # mittens round the board's edges, sleeves showing
        *[x for ft in FL12 for x in [k(r(ft + 0.02), toon={'face': {**STERN, 'lid': 0.85, 'brow': -1.0}}, toonDur=0.03, keepPose=True), k(r(ft + 0.16), toon={'face': STERN}, toonDur=0.08, keepPose=True)]],   # he squints at each flash
        TK(r(IT12 - 0.02), face={'lid': 0.3, 'mouth': 'clench', 'brow': -1.0}, sq=(0.9, 1.14, 0.9), bend={'spine': SP(-0.15)}, d=0.05, e='out', keep=True),   # « interdit »: chin up, stretched stiff
        TK(r(IT12 + 0.2), sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.15, keep=True), *BREATHE(1.0, D12, 0.4)]
st.shot('S12', 'whiteVoid', setOpts={'color': '#3E6A9A'}, look={'sunDir': [0.3, 0.9, 0.9]},
        actors=[act('ministre', MN12, 0, 'stand', 'neutral', keys=km12)],
        props=[P('salle12', 'pdRoom', pos=[0, 0, 0], opts={'w': 6, 'd': 4, 'wall': '#3E6A9A', 'floor': '#5E656D', 'trim': '#2E5280'}), P('pupitre12', 'pdPodium', pos=PD12),
               P('panneau12', 'pdBoard', pos=BD0, opts={'w': 1.1, 'h': 0.6}, keys=[k(0.06, to=BD1, dur=0.22, ease='out'), k(r(IT12 - 0.02), squash=[1.08, 0.9, 1.0], dur=0.3)]),
               P('flashsG12', 'flashBursts', pos=[-0.42, 1.55, 1.4], opts={'n': 2, 'w': 0.05, 'h': 0.3, 'at': [FL12[0], FL12[2]], 'life': 0.12}, scale=0.6), P('flashsD12', 'flashBursts', pos=[0.44, 1.7, 1.4], opts={'n': 2, 'w': 0.05, 'h': 0.3, 'at': [FL12[1], FL12[3]], 'life': 0.12}, scale=0.6)], cams=[C12])   # small bursts at the frame edges, from cameras out of shot
for tt in FL12: st.cue('sfx:pop', 'S12', tt, 0.2)
st.card('S12', 'INTERDIT', at=IT12)

# ================================================================= S13
# 13: a gendarme handcuffs a man in mid-bow after he has bumped a lady carrying a big grocery bag. Cut: a man who has dropped a cup claps a mitten
#     over his mouth while a second gendarme writes him a big ticket
D13 = st.dur('S13'); CUT13 = r(st.at('S13', 'L13', 3) - 0.1); BMP13 = 0.15; BOW13 = 0.35; CUFF13 = 0.9
FAC13 = [0, 0, -2.4]; DA13 = [0.9, 0, -0.25]; DRY13 = -75; HM0, HM1 = [-1.4, 0, 0.1], [0.2, 0, 0.0]; GA0, GA1 = [-1.4, 0, -0.9], [-0.35, 0, -0.55]
C13 = fcam(0.0, [0.2, 1.5, 5.0], {'daTop': add(DA13, [0.2, 2.15, 0]), 'hmTop': add(HM1, [0, 2.2, 0]), 'gaTop': add(GA1, [-0.2, 2.2, 0]), 'bag': off(DA13, DRY13, 0.3, -0.3, 0.9), 'knee': add(HM1, [0, 0.85, 0.3])}, top=0.08, bottom=0.74, push=0.2)
chk('S13', C13, {'daFace': add(DA13, [0, 1.85, 0]), 'hmFace': add(HM1, [0, 1.85, 0]), 'gaFace': add(GA1, [0, 1.85, 0])})
B13 = [0.0, 0, -30.0]; HM2 = add(B13, [-0.3, 0, 0.0]); GB13 = add(B13, [0.75, 0, 0.35]); CUP13 = off(HM2, 20, 0.35, 0.25, 0.0)
C13b = cam(CUT13, add(B13, [0.1, 1.55, 3.6]), add(B13, [0.1, 1.55, 3.35]), add(B13, [0.1, 1.35, 0.0]), add(B13, [0.1, 1.38, 0.0]), lens=50)
chk('S13b', C13b, {'hmTop': add(HM2, [0, 2.2, 0]), 'gbTop': add(GB13, [0, 2.2, 0]), 'cup': CUP13, 'hmFace': add(HM2, [0, 1.85, 0])})
kda = [*[k(r(1.0 + 0.2 * j), look=HEAD(add(HM1, [0.25 if j % 2 else -0.25, 0, 0]), 1.85), lookDur=0.15) for j in range(3)], k(0.0, clip='stand'), k(0.0, look=HEAD(HM1, 1.85)), TK(0.0, {'L': R5(off(DA13, DRY13, 0.25, -0.3, 0.95)), 'R': R5(off(DA13, DRY13, 0.2, 0.3, 1.0))}, {'L': 'grip', 'R': 'rest'}, CALM, d=0.0),
       TK(BMP13, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(0.85, 1.12, 0.85), bend={'spine': SP(-0.1, 0.3)}, d=0.04, e='out', keep=True), TK(r(BMP13 + 0.2), face=WORRY, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.12, keep=True),
       k(r(CUFF13 + 0.05), look=HEAD(GA1, 1.85), lookDur=0.12), *blink(0.6, WORRY), *BREATHE(1.0, CUT13, 0.4)]
khm = [k(0.0, clip='walk'), k(0.0, to=HM1, dur=BMP13, clip='walk', ease='linear', params={'freq': 2.4}), k(BMP13, clip='stand'), k(r(BMP13 + 0.02), face=90, turn=0.12), k(0.0, look=HEAD(DA13, 1.85)),
       TK(BMP13, face=WORRY, sq=(1.15, 0.88, 1.15), d=0.04, e='out', keep=True), TK(r(BMP13 + 0.12), sq=(1, 1, 1), d=0.1, keep=True),
       k(BOW13, clip='bow', blend=0.1), *TALK(r(BOW13 + 0.1), WORRY, 3),
       TK(r(CUFF13 + 0.02), face=POP, scl={'head': [1.3, 0.82, 1.2]}, d=0.04, e='out', keep=True), TK(r(CUFF13 + 0.25), face=SAD, scl={'head': [1, 1, 1]}, d=0.15, keep=True),   # cuffed mid-bow: the eyes pop, the head squashed wide
       *blink(r(CUFF13 + 0.4), SAD), *[TK(r(CUFF13 + 0.3 + 0.09 * j), sq=(1.03, 0.97, 1.03) if j % 2 else (0.98, 1.02, 0.98), bend={'spine': SP(0.0, 0.06 if j % 2 else -0.06)}, d=0.08, keep=True) for j in range(7)]]   # trembling, stuck in his bow
kga = [k(0.0, clip='stand'), k(0.0, look=HEAD(HM1, 1.85)), TK(0.0, {'R': R5(off(GA0, 60, 0.35, 0.2, 1.2))}, {'R': 'grip'}, STERN, d=0.0),
       k(0.3, to=GA1, dur=0.35, clip='walk', ease='out', params={'freq': 2.4}), k(0.65, clip='stand'),
       TK(0.6, {'R': R5(off(HM1, 90, 0.55, 0.2, 1.05))}, d=0.25, keep=True), TK(r(CUFF13 + 0.1), {'R': R5(off(GA1, 60, 0.25, 0.25, 1.0))}, {'R': 'rest'}, d=0.2, keep=True), *blink(1.2, STERN)]
khm2 = [k(0.0, clip='stand'), k(0.0, look=HEAD(CUP13, 1.6)), TK(0.0, {'R': R5(off(HM2, 20, 0.35, 0.25, 1.0)), 'L': R5(off(HM2, 20, 0.2, -0.3, 1.0))}, {'R': 'open', 'L': 'rest'}, POP, d=0.0),
        TK(r(CUT13 + 0.12), {'L': R5(off(HM2, 20, 0.45, -0.1, 1.45))}, {'L': 'open'}, d=0.06, keep=True),   # the mitten comes up...
        TK(r(CUT13 + 0.2), {'L': R5(off(HM2, 20, 0.34, 0.0, 1.84), 1, 0.02), 'R': R5(off(HM2, 20, 0.3, 0.3, 1.0))}, {'L': 'open'}, face={'lid': 0.0, 'mouth': 'clench', 'brow': 1.0}, scl={'head': [1.22, 0.82, 1.1]}, d=0.04, e='out', keep=True),   # ...SLAP over his mouth: the head squashed
        TK(r(CUT13 + 0.32), scl={'head': [0.92, 1.08, 0.95]}, sq=(0.94, 0.94, 0.94), d=0.06, keep=True), TK(r(CUT13 + 0.5), scl={'head': [1, 1, 1]}, sq=(0.96, 0.96, 0.96), d=0.15, keep=True),   # rebound, then he shrinks a little
        k(r(CUT13 + 0.5), look=HEAD(GB13, 1.85), lookDur=0.15), *blink(0.8, POP), *blink(r(CUT13 + 1.0), {'lid': 0.0, 'mouth': 'clench', 'brow': 1.0})]
kgb = [k(0.0, clip='writeOnHeld'), k(0.0, look=HEAD(HM2, 1.6)), TK(0.0, face=STERN, d=0.0), *blink(r(CUT13 + 0.7), STERN), *BREATHE(CUT13, D13, 0.4)]
st.shot('S13', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('dame', DA13, DRY13, 'stand', 'neutral', keys=kda), act('homme1', HM0, 90, 'walk', 'neutral', keys=khm), act('gendarme1', GA0, 60, 'stand', 'neutral', keys=kga),
                act('homme2', HM2, 20, 'stand', 'neutral', keys=khm2), act('gendarme2', GB13, -60, 'writeOnHeld', 'neutral', keys=kgb)],
        props=[P('sol13', 'pdGround', pos=[0, 0, -15], opts={'d': 60, 'kerb': 17.5}), P('facade13', 'pdFacade', pos=FAC13, opts={'w': 14, 'color': '#F3E9C9'}), P('facade13b', 'pdFacade', pos=add(B13, [0, 0, -2.4]), opts={'w': 14, 'color': '#E8E1EE'}),
               P('courses13', 'pdGroceries', on={'actor': 'dame', 'hand': 'L', 'offset': [0, -0.4, 0.05], 'sway': 1}, keys=[k(BMP13, squash=[1.15, 0.8, 1.15], dur=0.35), *[k(r(0.7 + 0.22 * j), squash=[1.04, 0.96, 1.04], dur=0.22) for j in range(4)]]),
               P('menottes13', 'handcuffs', on={'actor': 'gendarme1', 'hand': 'R'}, keys=[k(CUFF13, attach='homme1', hand='R', sway=1), k(CUFF13, squash=[1.3, 0.7, 1.3], dur=0.35), *[k(r(CUFF13 + 0.3 + 0.18 * j), squash=[1.08, 0.92, 1.08], dur=0.18) for j in range(3)]]),
               P('gobelet13', 'pdCup', pos=CUP13, scale=2.0, opts={'fall': r(CUT13 - 0.18), 'h': 0.5}), P('carnet13', 'pdTicket', on={'actor': 'gendarme2', 'hand': 'L', 'offset': [0, 0.0, 0.1], 'rot': [1.1, 0, 0]}, scale=1.3)], cams=[C13, C13b])
st.cue('thud', 'S13', BMP13, 0.3); st.cue('sfx:cuff', 'S13', CUFF13, 0.5); st.cue('sfx:splash', 'S13', r(CUT13 + 0.12), 0.35); st.cue('sfx:gulp', 'S13', r(CUT13 + 0.3), 0.25); st.cue('sfx:scratch', 'S13', r(CUT13 + 0.5), 0.2)

# ================================================================= S14
# 14: a metro platform: three commuters across the frame, mouths shut, the hero among them with his halves; two tall travellers with huge backpacks
#     turn round together and the backpacks sweep all three off their feet like skittles; they land sitting, dazed, unhurt; the baguette stays put
D14 = st.dur('S14'); BS14 = r(st.at('S14', 'L14', 2) - 0.05); TURN14 = r(st.at('S14', 'L14', 6) - 0.15)
ROW = -1.3; T1 = [-0.46, 0, ROW + 0.75]; T2 = [0.46, 0, ROW + 0.75]; CM = [[-0.85, 0, ROW], [0.0, 0, ROW], [0.85, 0, ROW]]   # the travellers in their own plane, in front, in the gaps, side on: the sacks are theirs
FALL14 = [r(TURN14 + 0.14), r(TURN14 + 0.3), r(TURN14 + 0.18)]; UP14, HANG14, DOWN14 = 0.16, 0.13, 0.14
C14 = cam(0.0, [0.0, 1.35, 3.6], [0.0, 1.35, 3.45], [0.0, 1.6, -1.4], [0.0, 1.6, -1.4], lens=50)
chk('S14', C14, {**{f'c{i}': add(p, [0, 1.9, 0]) for i, p in enumerate(CM)}, 'cSit': add(CM[1], [0, 1.1, 0]), 'feet': CM[1]})
kc14 = []
SITFX = [dict(scl={'head': [1.25, 0.8, 1.15]}), dict(scl={'head': [1.35, 0.7, 1.2]}), dict(scl={'head': [0.8, 1.25, 0.9]})]   # three different landings
for i, p in enumerate(CM):
    nm = 'mec' if i == 1 else f'navetteur{i + 1}'; f = FALL14[i]; sx = -1 if i == 0 else (1 if i == 2 else 0)
    ks = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, face=SHUT, d=0.0),
          TK(BS14, bend={'spine': SP(0.0, 0.3 if i != 1 else -0.3)}, sq=(1.05, 0.96, 1.05), d=0.08, e='out', keep=True), TK(r(BS14 + 0.25), bend={'spine': SP(0.0, 0.0)}, sq=(1, 1, 1), d=0.12, keep=True),   # elbowed, silently
          k(r(BS14 + 0.1), look=HEAD(CM[1 - sx if i != 1 else 0], 1.9), lookDur=0.12), k(r(BS14 + 0.6), look='camera', lookDur=0.15),
          k(f, clip='sitFloor', blend=0.1), k(f, to=add(p, [0.1 * sx, 0.9, 0.18 if sx else -0.05]), dur=UP14, clip='sitFloor', ease='out', face='keep'),   # swept off his feet: up in an arc...
          TK(f, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(0.85, 1.2, 0.85), d=0.05, e='out', keep=True), TK(r(f + UP14), sq=(1.05, 0.95, 1.05), d=0.08, keep=True),   # stretched in the launch
          k(r(f + UP14), to=add(p, [0.13 * sx, 0.95, 0.22 if sx else -0.05]), dur=HANG14, clip='sitFloor', ease='inOut', face='keep'),   # ...hangs there a beat...
          k(r(f + UP14 + HANG14), to=add(p, [0.16 * sx, 0, 0.26 if sx else 0.05]), dur=DOWN14, clip='sitFloor', ease='inOut', face='keep'),   # ...and drops onto his backside
          TK(r(f + UP14 + HANG14 + DOWN14), face=DAZED, d=0.03, e='out', keep=True, **SITFX[i]), TK(r(f + UP14 + HANG14 + DOWN14 + 0.15), scl={'head': [1, 1, 1]}, d=0.08, keep=True),
          TK(r(f + UP14 + HANG14 + DOWN14 + 0.3), sq=(1, 1, 1), d=0.12, keep=True),
          *([TK(r(f + UP14 + HANG14 + DOWN14), sq=(1.55, 0.45, 1.55), d=0.03, e='out', keep=True), TK(r(f + UP14 + HANG14 + DOWN14 + 0.14), sq=(0.88, 1.18, 0.88), d=0.08, keep=True),
             TK(r(f + UP14 + HANG14 + DOWN14 + 0.28), sq=(1, 1, 1), d=0.1, keep=True)] if i == 1 else []),   # the hero lands flat as a pancake and pops back up
          k(r(f + 0.6), look=HEAD(add(p, [0.6 * (1 if i % 2 == 0 else -1), 0, 2.0]), 1.4), lookDur=0.2), *[k(r(f + 0.5 + 0.3 * j), look=HEAD(add(p, [(-0.6 if j % 2 == 0 else 0.6), 0, 2.0]), 1.4), lookDur=0.2) for j in range(3)],
          *blink(r(0.6 + 0.2 * i), SHUT), *blink(r(f + 0.8), DAZED), *BREATHE(r(f + 0.5), D14, 0.4)]
    if i == 1: ks += [TK(0.0, {'R': R5(off(p, 0, 0.3, 0.32, 1.1)), 'L': R5(off(p, 0, 0.3, -0.32, 1.1))}, {'R': 'grip', 'L': 'grip'}, d=0.0, keep=True),
                      TK(f, {'R': R5(off(p, 0, 0.35, 0.45, 2.3)), 'L': R5(off(p, 0, 0.35, -0.45, 2.3))}, d=0.12, keep=True),   # arms up in the air (with him), a half in each mitten
                      TK(r(f + UP14 + HANG14), {'R': R5(off(add(p, [0, 0, 0.05]), 0, 0.45, 0.42, 0.75)), 'L': R5(off(add(p, [0, 0, 0.05]), 0, 0.45, -0.42, 0.75))}, d=DOWN14, keep=True)]   # down with him: landed, the halves still held up
    kc14.append(act(nm, p, 0, 'stand', 'neutral', keys=ks))
ktr = []
for i, (p, sd) in enumerate([(T1, -1), (T2, 1)]):
    nm = f'routard{i + 1}'; ry0 = 90 * sd   # side on, facing out: the sack sticks out toward the middle
    ks = [k(0.0, clip='stand'), k(0.0, look=HEAD(add(p, [sd * 2.0, 0, 0.5]), 2.0)), TK(0.0, face=CALM, d=0.0),
          k(0.45, face=r(ry0 + 20 * sd), turn=0.15), TK(0.45, sq=(1.04, 0.97, 1.04), bend={'spine': SP(-0.1, 0.0)}, d=0.12, keep=True),   # a little wind-up...
          k(0.62, face=r(ry0 * 0.6), turn=0.7), TK(0.62, bend={'spine': SP(0.0, 0.0)}, d=0.2, keep=True), k(0.62, look='camera', lookDur=0.3),   # ...a slow quarter turn...
          k(TURN14, face=0, turn=0.1), k(r(TURN14 + 0.1), face=r(-ry0), turn=0.12),   # ...and the whip round through the row: the sacks sweep it
          TK(TURN14, sq=(1.3, 0.82, 1.3), scl={'head': [1.45, 0.85, 0.9]}, bend={'spine': SP(0.0, 0.3 * sd)}, d=0.04, e='out', keep=True),   # smeared in the whip
          TK(r(TURN14 + 0.18), sq=(0.95, 1.06, 0.95), scl={'head': [1, 1, 1]}, bend={'spine': SP(0.0, 0.0)}, d=0.08, keep=True), TK(r(TURN14 + 0.35), sq=(1, 1, 1), d=0.15, keep=True),
          *blink(r(0.3 + 0.4 * i), CALM), *blink(r(TURN14 + 0.6), CALM), *BREATHE(0.1, TURN14, 0.5), *BREATHE(r(TURN14 + 0.4), D14, 0.45)]
    ktr.append(act(nm, p, ry0, 'stand', 'neutral', keys=ks))
st.shot('S14', 'whiteVoid', setOpts={'color': '#2A2C30'}, look={'sunDir': [0.2, 0.9, 0.6]},
        actors=[*kc14, *ktr],
        props=[P('quai14', 'metroPlatform', pos=[0, 0, 0], opts={'len': 12, 'depth': 4, 'name': ' ', 'bench': False}),
               P('mur14', 'pdGround', pos=[0, 6.0, -4.06], rot=[1.5708, 0, 0], opts={'w': 14, 'd': 8, 'color': '#E3DED2'}),   # the tiled wall goes on up (no black void)
               *[P(f'sac14_{i + 1}', 'pdRucksack', on={'actor': f'routard{i + 1}', 'joint': 'torso', 'offset': [0, 0.3, -0.16]}, scale=1.35, opts={'color': ['#2F7F5C', '#B5452E'][i], 'dark': ['#1E5A40', '#7E2E20'][i]}) for i in range(2)],
               *HALVES('S14')], cams=[C14])
st.cue('whoosh', 'S14', TURN14, 0.4); st.cue('thud', 'S14', r(FALL14[0] + 0.18), 0.35); st.cue('thud', 'S14', r(FALL14[2] + 0.18), 0.3); st.cue('thud', 'S14', r(FALL14[1] + 0.18), 0.35)

# ================================================================= S15
# 15: the pavement, four passers-by: the president strides through toward us, his shoulders knocking people aside left and right, mouth shut, the
#     lemon tie flapping big in frame
D15 = st.dur('S15'); P150, P151 = [0.0, 0, -5.2], [0.0, 0, 0.6]
def pz(t): return P150[2] + (P151[2] - P150[2]) * min(1.0, t / (D15 - 0.05))
PAS15 = [[-0.85, 0, -3.8], [0.9, 0, -2.6], [-0.9, 0, -1.4], [0.95, 0, -0.5]]
def tz(z): return r((z - P150[2]) / (P151[2] - P150[2]) * (D15 - 0.05))
C15 = cam(0.0, [0.15, 0.3, 4.0], [0.12, 0.33, 3.5], [0.0, 1.3, -2.0], [0.0, 1.45, -0.6], lens=50)   # from the ground: every foot near the horizon
chk('S15', C15, {'pres@0': add(P150, [0, 1.9, 0]), 'pres@end': add(P151, [0, 1.9, 0]), 'tie@end': add(P151, [0, 1.2, 0.45]), 'p0': add(PAS15[0], [0, 1.85, 0]), 'p3': add(PAS15[3], [0, 1.85, 0])})
kp15 = []
KN = [dict(sq=(0.8, 1.2, 0.8)), dict(scl={'head': [1.4, 0.75, 1.1]}), dict(sq=(1.25, 0.8, 1.25)), dict(face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'jaw': 1.0})]
for i, p in enumerate(PAS15):
    t = tz(p[2]) - 0.05; sx = -1 if p[0] < 0 else 1; ry = 180 if i % 2 == 0 else 160
    ks = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, face=CALM, d=0.0), k(r(t - 0.4), look=HEAD([0, 0, pz(t)], 1.8), lookDur=0.2),
          k(t, to=add(p, [sx * 0.9, 0, 0.15]), dur=0.22, clip='stand', ease='out', face='keep'), TK(t, bend={'spine': SP(-0.1, 0.5 * sx)}, d=0.04, e='out', keep=True, **{'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.9}, **KN[i]}),   # knocked aside
          TK(r(t + 0.3), face=WORRY, bend={'spine': SP(0.0, 0.1 * sx)}, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.15, keep=True), *blink(r(t + 0.5), WORRY), *BREATHE(0.1, t, 0.5), *BREATHE(r(t + 0.45), D15, 0.45)]
    kp15.append(act(f'passant{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S15', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=kp15,
        props=[P('sol15', 'pdGround', pos=[0, 0, 0], opts={'kerb': -6.0}), P('facade15', 'pdFacade', pos=[-2.6, 0, -2.0], ry=90, opts={'w': 16, 'color': '#EFE6D2'}),
               P('president15', 'pdPresident', pos=P150, opts={'round': 1.1, 'walk': [0, D15, 2.6], 'flap': 2.6, 'smile': [[0, 0.45]], 'bounce': [tz(p[2]) for p in PAS15], 'blink': [1.2]}, keys=[k(0.0, to=P151, dur=r(D15 - 0.05), ease='linear')])], cams=[C15])
for p in PAS15: st.cue('thud', 'S15', tz(p[2]), 0.3)
st.cue('sfx:stepHeavy', 'S15', 0.1, 0.2)

# ================================================================= S16
# 16: line 1 replayed wide: the bakery door, the hero coming out with a whole baguette; the president strides in from the right, tie flapping, and
#     shoulders him; the baguette snaps; the hero says « pardon ». Without looking back the president signs a scroll while walking away. Hold on the
#     hero, a broken half in each mitten
D16 = st.dur('S16'); HIT16 = snap(st.at('S16', 'L16', 4) - 0.05); SNAP16 = r(HIT16 + 0.03); SWAP16 = r(HIT16 + 0.3)
BK16 = [0, 0, -1.3]; H016 = [0, 0, -0.5]; H16 = [0, 0, 0.5]; HRY16 = -35
PATH16 = [[-1.3, 0, -2.4], [-0.74, 0, 0.42], [-1.15, 0, 1.25], [-3.1, 0, 3.2]]   # from behind on his baguette side (tie to us), the shoulder, then off toward us on the left: never behind him
LEG1 = math.dist(PATH16[0], PATH16[1]); LEGS = sum(math.dist(PATH16[n], PATH16[n + 1]) for n in range(1, 3))
OUT16 = r(HIT16 + 1.55); RAISE16 = r(HIT16 + 0.3); SIGN16 = [r(RAISE16 + 0.2), r(RAISE16 + 0.45), r(RAISE16 + 0.7)]
T16b = r(HIT16 + 1.05)   # slow while he signs (in frame), then off fast
C16 = cam(0.0, [0.5, 1.5, 6.8], [0.3, 1.5, 5.6], [-0.35, 2.05, -0.2], [-0.1, 1.85, 0.2], lens=48, ease='inOut')
chk('S16', C16, {'heroTop': add(H16, [0, 2.35, 0]), 'heroFeet': H16, 'baguette': off(H16, 0, 0.35, 0.42, 1.3), 'prA': add(PATH16[0], [0, 2.0, 0]), 'prHit': add(PATH16[1], [0, 2.0, 0]), 'prEnd': add(PATH16[-1], [0, 2.3, 0]), 'bake': add(BK16, [2.5, 4.2, 0])})
BG16 = off(H16, 0, 0.35, 0.42, 1.3)
kh16 = [k(0.0, clip='walk'), k(0.0, to=H16, dur=0.45, clip='walk', ease='out', params={'freq': 2.2}), k(0.45, clip='stand'), k(0.0, look='camera'),
        TK(0.0, {'R': R5(BG16), 'L': R5(off(H16, 0, 0.3, -0.05, 1.3))}, {'R': 'grip', 'L': 'open'}, CALM, d=0.0),
        k(r(HIT16 - 0.12), look=HEAD(PATH16[1], 2.0), lookDur=0.06),
        TK(HIT16, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'jaw': 1.0}, sq=(1.25, 0.8, 1.15), scl={'head': [0.85, 1.3, 0.9]}, bend={'spine': SP(-0.1, -0.4)}, d=0.04, e='out', keep=True),   # this time: squashed down, the head shot up
        k(r(HIT16 + 0.02), face=r(HRY16 - 30), turn=0.12), k(r(HIT16 + 0.16), face=HRY16, turn=0.15),
        TK(r(HIT16 + 0.16), face=WORRY, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, bend={'spine': SP(0.0)}, d=0.12, keep=True),
        TK(SWAP16, {'R': R5(off(H16, HRY16, 0.32, 0.36, 1.2)), 'L': R5(off(H16, HRY16, 0.32, -0.36, 1.2))}, {'R': 'grip', 'L': 'grip'}, d=0.1, keep=True),
        *TALK(r(HIT16 + 0.32), WORRY, 4, 0.08), *[k(r(HIT16 + 0.25 + 0.35 * j), look=HEAD(PATH16[min(3, 2 + j // 2)], 2.0), lookDur=0.2) for j in range(4)],
        k(2.2, face=0, turn=0.3), k(2.15, look='camera', lookDur=0.15), TK(2.2, {'R': R5(off(H16, 0, 0.38, 0.42, 1.3)), 'L': R5(off(H16, 0, 0.38, -0.42, 1.3))}, face=SAD, d=0.25, keep=True),   # the hold, alone: a half in each mitten
        k(2.45, look=HEAD(off(H16, 0, 0.4, 0.42, 0), 1.6), lookDur=0.3), k(2.7, look=HEAD(off(H16, 0, 0.4, -0.42, 0), 1.6), lookDur=0.15), k(2.92, look='camera', lookDur=0.15),   # one half, the other, then back to us
        *blink(1.7, WORRY), *blink(2.45, SAD), *BREATHE(1.4, D16, 0.35)]
st.shot('S16', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', H016, 0, 'walk', 'neutral', keys=kh16)],
        props=[P('sol16', 'pdGround', pos=[0, 0, 0], opts={'kerb': 3.2}), P('boulangerie16', 'pdBakery', pos=BK16, opts={'w': 8}),
               P('baguette16', 'pdBaguette', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.36, 0.05], 'rot': [0, 0, -1.5708]}, opts={'snapAt': SNAP16, 'len': 0.8}, keys=[k(SWAP16, visible=False)]),
               *HALVES('S16', t0=SWAP16),
               P('president16', 'pdPresident', pos=PATH16[0], ry=yaw(PATH16[0], PATH16[1]), opts={'round': 1.1, 'walk': [0, D16, 2.4], 'flap': 2.4, 'signUp': [[RAISE16, D16]], 'bounce': [HIT16, r(RAISE16 - 0.17)], 'smile': [[0, 0.45]], 'blink': [0.4]},
                 keys=[k(0.0, to=PATH16[1], dur=HIT16, ease='linear'), k(HIT16, squash=[1.1, 0.9, 1.1], dur=0.25),
                       k(r(HIT16 + 0.06), to=PATH16[2], dur=r(T16b - HIT16 - 0.06), ease='linear'), k(r(HIT16 + 0.02), rotTo=[0, math.radians(yaw(PATH16[1], PATH16[2])), 0], dur=0.15),
                       k(T16b, to=PATH16[3], dur=r(OUT16 - T16b), ease='linear'), k(T16b, rotTo=[0, math.radians(yaw(PATH16[2], PATH16[3])), 0], dur=0.12), k(r(OUT16 + 0.05), visible=False)]),   # 'to' moves and turns: away, out of frame by ~43.9 s
               P('parchemin16', 'pdScroll', on={'actor': 'president16', 'offset': [-0.42, 2.4, 0.05], 'rot': [0, 0, 0]}, opts={'w': 0.55, 'h': 0.68, 'signAt': SIGN16},   # held up into the open sky at the left
                 keys=[k(0.0, visible=False), k(RAISE16, visible=True), k(RAISE16, squash=[0.6, 1.3, 1.0], dur=0.25)])], cams=[C16])
st.cue('sfx:stepHeavy', 'S16', 0.2, 0.2); st.cue('thud', 'S16', HIT16, 0.45); st.cue('sfx:crunch', 'S16', SNAP16, 0.45); st.cue('sfx:paper', 'S16', r(HIT16 + 0.5), 0.25); [st.cue('sfx:scratch', 'S16', t_, 0.18) for t_ in SIGN16]

for g_ in [('S01', HIT1, 'mec', 'bump'), ('S02', SHR2, 'mec', 'shrug'), ('S03', X3, 'avocat', 'stamp'), ('S04', RN4, 'juge', 'tray'), ('S05', PT5, 'procureur', 'life'),
           ('S06', GR6, 'mec', 'minute'), ('S07', POP7, 'greffier', 'scroll'), ('S08', BANG8[0], 'juge', 'gavel'), ('S09', CUT9, 'mec', 'tie'), ('S10', BOW10, 'detenu3', 'bow'),
           ('S11', FLIP11, 'directeur', 'switch'), ('S12', IT12, 'ministre', 'board'), ('S13', CUFF13, 'homme1', 'cuffs'), ('S14', TURN14, 'mec', 'skittles'), ('S15', 0.5, 'passant1', 'shove'), ('S16', HIT16, 'mec', 'reveal')]:
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
GEND = {'preset': 'cop', 'outfit': 'suit', 'suit': '#1E2A44', 'pants': '#1E2A44', 'shirt': '#C9D6EA', 'lapel': '#18223A', 'tie': '#18223A', 'cuff': '#1E2A44', 'hat': 'copcap', 'hatColor': '#1E2A44', 'hatBand': '#2A2C30', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
GUEST = lambda pr, seed, suit: {'preset': pr, 'seed': seed, 'hat': 'none', 'suit': suit, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
GOWN = {'preset': 'avocat', 'hat': 'none', 'toon': EX}
st.write("Le pardon", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'gendarme1': {**GEND, 'seed': 3101}, 'gendarme2': {**GEND, 'seed': 3102},
    'greffier': {'preset': 'politique', 'seed': 3103, 'suit': '#8A939E', 'lapel': '#7A838E', 'tie': '#3A3D44', 'hair': 'receding', 'hairColor': '#8A8A86', 'glasses': True, 'toon': EX},
    'avocat': {**GOWN, 'seed': 3104},
    'juge': {**GOWN, 'seed': 3105, 'hair': 'bald', 'facial': 'beard', 'beardColor': '#BDBDBD', 'glasses': True, 'build': {'width': 1.15, 'headWidth': 1.25, 'belly': 0.1}},
    'procureur': {**GOWN, 'seed': 3106, 'suit': '#8E3A28', 'pants': '#8E3A28', 'lapel': '#6E2C1E', 'cuff': '#8E3A28', 'hair': 'slick', 'hairColor': '#2A2420', 'glasses': False, 'facial': 'mustache'},
    **{f'passant{i + 1}': GUEST(['worker', 'tourist', 'madame', 'fermier'][i], 3110 + i, ['#3E7FB6', '#D9A23A', '#C8322A', '#5E8C4A'][i]) for i in range(4)},
    **{f'voyageur{i + 1}': GUEST(['madame', 'worker', 'tourist', 'femme', 'fermier'][i], 3120 + i, ['#8A5AB6', '#2E7D4F', '#C86A2A', '#3E5FB6', '#B5452E'][i]) for i in range(5)},
    **{f'detenu{i + 1}': {'preset': 'pyjama', 'seed': 3130 + i, 'suit': '#2E3138', 'pants': '#2E3138', 'cuff': '#2E3138', 'hair': 'buzz', 'facial': 'stubble', 'toon': EX, 'build': {'width': [1.0, 1.15, 0.9, 1.05, 0.95][i]}} for i in range(5)},   # dark grey with white stripes
    'gardien': {**GEND, 'seed': 3140, 'suit': '#2E4A7A', 'pants': '#2E4A7A', 'lapel': '#2E4A7A', 'tie': '#2E4A7A', 'shirt': '#2E4A7A', 'cuff': '#2E4A7A', 'hatColor': '#2E4A7A'},   # plain blue
    'directeur': {'preset': 'politique', 'seed': 3141, 'suit': '#6A5440', 'lapel': '#5A4634', 'tie': '#2E4A6A', 'hair': 'receding', 'hairColor': '#8A8A86', 'facial': 'mustache', 'glasses': True, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 3142, 'suit': '#4A4F58', 'lapel': '#3C414A', 'tie': '#7A2E2E', 'hair': 'slick', 'hairColor': '#3A3A40', 'glasses': False, 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'dame': {'preset': 'madame', 'seed': 3143, 'suit': '#C86A8A', 'toon': EX},
    'homme1': GUEST('worker', 3144, '#2E7D4F'), 'homme2': GUEST('tourist', 3145, '#3E5FB6'),
    'navetteur1': GUEST('madame', 3146, '#7A5A8A'), 'navetteur3': GUEST('fermier', 3147, '#C9822E'),
    'routard1': {'preset': 'sportif', 'seed': 3148, 'hair': 'crew', 'toon': EX, 'build': {'height': 1.12}}, 'routard2': {'preset': 'sportif', 'seed': 3149, 'suit': '#C9729A', 'hair': 'bun', 'toon': EX, 'build': {'height': 1.1}},
})
