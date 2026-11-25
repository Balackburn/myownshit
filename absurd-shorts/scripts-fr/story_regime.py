#!/usr/bin/env python3
"""Le régime (story 101, cycle 53; a diet taken the political way, a slow escalation, a coup by dessert and a Monday loop).
This man went on a diet ("changé de régime") and the State took it politically: the president packed. The army swore allegiance to a broccoli; a
curfew at eight, for dessert. The old regime's cheeses fled abroad (the president trotting after them). The council of ministers was weighed, the
heaviest relieved of his duties. A resistance: éclairs under the coat; the gendarmes raided a clandestine raclette (his wife there, cheeks full). He
lost two kilos, the country a million tonnes. One evening a square of chocolate appeared (his wife's mitten); he cracked; the regime fell. The people
stormed the bakery, the cheeses came home, the camembert carried in triumph, the president too, ten kilos heavier. He starts again on Monday; the
president has not unpacked.
Running gag (silent): the wife eats a different dessert in every shot she is in (cream cake S01, a slice under the curfew S03, raclette S07, a crêpe
S15) and her mitten and sleeve (the green of her suit) slide in the chocolate at S09.
Cards: EXIL (S04), TOMBÉ (S11). No other word, no figure, flag, emblem, portrait or sash; generic uniforms; nobody hurt."""
from story_kit import *
import math

st = Story('regime', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 17)])
# the cuts are rounded to 4 decimals: one that rounds UP (8.0667 for 242/30) puts the frame of the cut in the shot before (a late cut by one frame); round them down
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

# faces
CALM = {'lid': 0.3, 'mouth': 'line', 'brow': 0.0}
WORRY = {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}
STERN = {'lid': 0.35, 'mouth': 'line', 'brow': -0.6}
SMUG = {'lid': 0.35, 'mouth': 'smile', 'brow': 0.2}
HAPPY = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}
SAD = {'lid': 0.5, 'mouth': 'line', 'brow': 0.5}
GRAVE = {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}
def HANDS(p, ry, rf=0.25, rs=0.25, ry_=1.0, lf=0.25, ls=-0.25, ly=1.0):
    """two hands by the body: R at his right (s > 0), L at his left (s < 0)"""
    return {'R': R5(off(p, ry, rf, rs, ry_)), 'L': R5(off(p, ry, lf, ls, ly))}
def DROP(pid, actor, offset, scale, t0=None):
    return P(pid, 'sweatDrop', on={'actor': actor, 'joint': 'head', 'offset': offset}, scale=scale, **({'keys': [k(0.0, visible=False), k(t0, visible=True)]} if t0 else {}))
def EAT(t0, t1, mouth_hand, plate_hand, every=0.5, face=None):
    """a fork going from the plate to the mouth and back (the wife's running gag): keys for the eating hand"""
    out = []; n = int((t1 - t0) / every) + 1
    for j in range(n):
        a = r(t0 + j * every); out += [TK(a, {'R': R5(mouth_hand)}, {'R': 'pinch'}, face={**(face or HAPPY), 'mouth': 'O'}, d=r(every * 0.35), keep=True), TK(r(a + every * 0.5), {'R': R5(plate_hand)}, {'R': 'pinch'}, face={**(face or HAPPY), 'mouth': 'smile'}, sq=(1.02, 0.98, 1.02) if j % 2 else (1, 1, 1), d=r(every * 0.35), keep=True)]
    return out
WIFE_SLEEVE = '#3E9A5A'; WIFE_MITTEN = '#2E7A46'

def WIFE(sid, p, ry, food, t0=0.1, t1=None, every=0.55):
    """the wife standing, a dessert plate in her left hand, eating with a fork in her right: (actor, props)"""
    t1 = t1 if t1 is not None else st.dur(sid) - 0.2
    plate = off(p, ry, 0.42, -0.12, 1.25); mouth = off(p, ry, 0.2, 0.04, 1.75)
    ks = [k(0.0, clip='stand'), k(0.0, look=plate), TK(0.0, {'L': R5(add(plate, [0, -0.03, 0])), 'R': R5(add(plate, [0.05, 0.05, 0.03]))}, {'L': 'grip', 'R': 'pinch'}, HAPPY, d=0.0),
          *EAT(t0, t1, mouth, add(plate, [0.03, 0.06, 0.02]), every), *blink(r(t0 + 0.7), HAPPY)]
    props = [P(f'dessert{sid}', 'rgPlate', pos=add(plate, [0, -0.07, 0]), opts={'food': food, 'r': 0.2 if food == 'crepe' else 0.15}), P(f'fourchette{sid}', 'rgFork', on={'actor': 'femme', 'hand': 'R', 'offset': [0, -0.02, 0.03]}, opts={'bite': '#FFF6E6' if food != 'crepe' else '#E9B65C'})]
    return act('femme', p, ry, 'stand', 'neutral', keys=ks), props

# ================================================================= S01
# 1: low across the kitchen table: the hero pushes away a plate of fries and pulls a plate with one big broccoli to him; behind him his wife eats a
#    big slice of cream cake. Cut: the presidential bedroom (plain walls, plain bedding): the round, kindly president sits on a stuffed suitcase to
#    close it, bouncing
D1 = st.dur('S01'); CUT1 = r(st.at('S01', 'L01', 6) - 0.12)
TB = [0, 0, 0]; TH = 0.82
HER1 = [0.0, 0, -0.62]
FR0, FR1 = [-0.2, TH, -0.22], [-0.62, TH, -0.12]
BR0, BR1 = [0.5, TH, 0.0], [0.12, TH, -0.12]
WF1 = [0.8, 0, -1.55]; WRY1 = -25
C1 = cam(0.0, [0.25, 1.1, 2.3], [0.22, 1.09, 2.15], [0.15, 1.5, -0.9], [0.15, 1.5, -0.9], lens=50)
BED = [40.0, 0, 0.0]
SUIT1 = add(BED, [0.3, 0, 0.3]); PRES1 = add(SUIT1, [0, 0.14, -0.04])
C1b = cam(CUT1, add(BED, [0.75, 1.15, 3.9]), add(BED, [0.72, 1.14, 3.7]), add(BED, [0.3, 0.95, 0.2]), add(BED, [0.3, 0.95, 0.2]), lens=50)   # low: the case under him reads
chk('S01', C1, {'heroFace': add(HER1, [0, 1.5, 0]), 'broc': BR1, 'fries': FR0, 'wifeFace': add(WF1, [0, 1.85, 0]), 'wifeFeet': WF1})
chk('S01b', C1b, {'presFace': add(PRES1, [0, 1.5, 0]), 'suit': SUIT1, 'suit2': add(BED, [1.2, 0.4, 0.4])})
k1 = [k(0.0, clip='sit'), k(0.0, look=FR0), TK(0.0, {'R': R5(add(FR0, [-0.05, 0.05, 0.12])), 'L': R5(add(BR0, [0.1, 0.05, 0.1]))}, {'R': 'open', 'L': 'grip'}, {**GRAVE, 'brow': 0.3}, d=0.0),
      TK(0.25, {'R': R5(add(FR1, [-0.05, 0.05, 0.12]))}, d=0.25, e='out', keep=True), k(0.35, look=BR1, lookDur=0.15),   # pushes the fries away...
      TK(0.55, {'L': R5(add(BR1, [0.1, 0.05, 0.1]))}, {'L': 'grip'}, d=0.3, keep=True),   # ...pulls the broccoli in
      TK(0.95, face={'lid': 0.0, 'mouth': 'line', 'brow': 0.9, 'pop': 0.0}, sq=(0.95, 1.06, 0.95), d=0.08, e='out', keep=True), TK(1.15, face={**GRAVE, 'mouth': 'smile'}, sq=(1, 1, 1), d=0.15, keep=True),
      k(1.05, look='camera', lookDur=0.15), *blink(0.6, GRAVE)]
wife1, wprops1 = WIFE('S01', WF1, WRY1, 'cake', t0=0.1, t1=r(CUT1 - 0.1), every=0.45)
PRESF = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.4}
kp1 = [k(0.0, clip='sit'), k(0.0, look='camera'), TK(0.0, HANDS(PRES1, 0, 0.3, 0.3, 0.55, 0.3, -0.3, 0.55), {'R': 'open', 'L': 'open'}, PRESF, d=0.0),
       *[TK(r(CUT1 + 0.08 + 0.22 * j), sq=(1.12, 0.86, 1.12) if j % 2 == 0 else (0.97, 1.04, 0.97), d=0.08, e='out', keep=True) for j in range(6)], *blink(r(CUT1 + 0.6), PRESF)]   # bounces on the lid
st.shot('S01', 'kitchenDay', actors=[act('mec', HER1, 0, 'sit', 'neutral', keys=k1), wife1],
        props=[P('table1', 'table', pos=TB, opts={'w': 1.6, 'd': 0.9, 'h': TH}), P('chaise1', 'chair', pos=add(HER1, [0, 0, -0.05])),
               P('frites1', 'rgPlate', pos=FR0, opts={'food': 'fries'}, keys=[k(0.25, to=FR1, dur=0.25, ease='out')]), P('brocoli1', 'rgPlate', pos=BR0, opts={'food': 'broccoli', 'r': 0.2}, keys=[k(0.55, to=BR1, dur=0.3, ease='inOut')]),
               *wprops1,
               P('chambre1', 'rgRoom', pos=BED, opts={'w': 5, 'd': 4, 'wall': '#E6DCCB', 'floor': '#B58E66'}), P('lit1', 'bed', pos=add(BED, [-1.4, 0, -0.9]), opts={'blanket': '#9AB0C8'}),
               P('valise1', 'rgCase', pos=SUIT1, opts={'w': 0.95, 'h': 0.48, 'd': 0.42, 'bulge': 0.2, 'squash': [r(CUT1 + 0.12 + 0.36 * j) for j in range(4)], 'latchAt': r(CUT1 + 1.4)}),
               P('president1', 'rgPresident', pos=PRES1, opts={'sit': True, 'round': 1.0, 'bounce': [r(CUT1 + 0.12 + 0.36 * j) for j in range(4)], 'smile': [[0, 0.6], [r(CUT1 + 1.4), 1.0]], 'blink': [r(CUT1 + 0.7)]}, keys=[k(r(CUT1 + 0.12 + 0.36 * j), to=add(PRES1, [0, 0.1 if j % 2 == 0 else 0.0, 0]), dur=0.15, ease='out') for j in range(4)]),
               P('valise1b', 'rgCase', pos=add(BED, [1.3, 0, 0.15]), opts={'w': 0.6, 'h': 0.55, 'd': 0.32})], cams=[C1, C1b])
st.cue('sfx:clink', 'S01', 0.3, 0.3); st.cue('thud', 'S01', r(CUT1 + 0.1), 0.3); st.cue('sfx:spring', 'S01', r(CUT1 + 0.12), 0.2); st.cue('sfx:spring', 'S01', r(CUT1 + 0.48), 0.2); st.cue('clack', 'S01', r(CUT1 + 1.4), 0.4)

# ================================================================= S02
# 2: the town square, low: a giant broccoli statue on a tall stone plinth on the right of the frame; a row of generals in plain uniforms and peaked
#    caps facing it (three-quarter to us) put a hand on the heart, then bow their heads in a wave toward it (no raised arm); a drum roll
D2 = st.dur('S02'); BOW2 = r(st.at('S02', 'L02', 3) - 0.25)
STAT = [0.0, 0, -4.0]; SQ = [-2.2, 1.25, 4.2]   # in the street, beside the statue's line
GEN = [[1.4, 0, -2.3], [2.3, 0, -2.6], [3.2, 0, -3.0], [4.0, 0, -3.5], [4.7, 0, -4.1]]
C2 = cam(0.0, SQ, add(SQ, [0.1, 0.0, -0.2]), [2.0, 2.2, -4.6], [2.0, 2.15, -4.6], lens=58)   # from beside the statue: its plinth, the broccoli against the sky, the generals facing us
chk('S02', C2, {'statTop': add(STAT, [0, 5.7, 0]), 'plinthFoot': add(STAT, [-0.8, 0, 0.8]), **{f'g{i}': add(p, [0, 1.95, 0]) for i, p in enumerate(GEN)}, 'gFeet': GEN[0]})
gens = []
for i, p in enumerate(GEN):
    ry = r(yaw(p, STAT) + 40)   # turned three-quarter toward us
    heart = off(p, ry, 0.22, -0.08, 1.45)
    ks = [k(0.0, clip='stand'), k(0.0, look=add(STAT, [0, 4.6, 0])), TK(0.0, HANDS(p, ry, 0.12, 0.25, 0.95, 0.12, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, STERN, d=0.0),
          TK(r(0.15 + 0.03 * i), {'R': R5(heart)}, {'R': 'open'}, sq=(0.98, 1.03, 0.98), d=0.18, keep=True),   # a hand on the heart, held
          TK(r(BOW2 + 0.1 * i), bend={'spine': SP(0.55), 'neck': SP(0.0)}, face={**STERN, 'lid': 0.9}, sq=(0.98, 1.02, 0.98), d=0.28, e='inOut', keep=True),   # a bow in a wave
          TK(r(BOW2 + 0.7 + 0.12 * i), bend={'spine': SP(0.05)}, face=STERN, sq=(1, 1, 1), d=0.28, keep=True), *blink(r(0.45 + 0.15 * i), STERN), *BREATHE(r(BOW2 + 1.0), D2, 0.4, 0.015)]
    gens.append(act(f'general{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S02', 'parisStreet', setOpts={'clouds': 4, 'eiffel': False}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=gens,
        props=[P('statue2', 'rgBroccoli', pos=STAT, opts={'s': 3.0, 'plinth': 2.0}), P('pave2', 'parkLot', pos=add(STAT, [-2, 0.02, 0]), opts={'w': 14, 'd': 12, 'color': '#C9BFAE'})], cams=[C2])
st.cue('sfx:ticks', 'S02', 0.0, 0.25); st.cue('sfx:ticks', 'S02', 0.6, 0.25); st.cue('sfx:fanfare', 'S02', r(BOW2 + 0.1), 0.25)

# ================================================================= S03
# 3: the dining room at dusk (orange sky and lit windows outside): a siren on a pole wails through the window; the hero lowers a glass dome over a
#    cake and snaps a big padlock on it; behind his back his wife already has a slice on her plate
D3 = st.dur('S03'); DOME3 = 0.35; LOCK3 = r(st.at('S03', 'L03', 4) - 0.1)
ROOM3 = [0, 0, 0]
HER3 = [0.0, 0, -0.78]; HRY3 = 0
CAKE3 = [0.0, 0.95, 0.2]
WF3 = [1.25, 0, -1.35]; WRY3 = -25
C3 = fcam(0.0, [-1.2, 1.4, 4.4], {'heroTop': add(HER3, [0, 2.35, 0]), 'heroKnee': add(HER3, [0, 0.5, 0]), 'cake': add(CAKE3, [0, 0.9, 0]), 'win': [-0.4, 2.3, -1.95], 'wife': add(WF3, [0, 2.3, 0]), 'wifeK': add(WF3, [0.3, 0.5, 0])}, top=0.1, bottom=0.78, margin=0.06, push=0.25)
chk('S03', C3, {'heroFace': add(HER3, [0, 1.95, 0]), 'cake': CAKE3, 'wifeFace': add(WF3, [0, 1.85, 0]), 'win': [-0.4, 1.8, -1.95]})
k3 = [k(0.0, clip='stand'), k(0.0, look=CAKE3), TK(0.0, {'R': R5(add(CAKE3, [-0.35, 1.35, 0.05])), 'L': R5(add(CAKE3, [0.35, 1.35, 0.05]))}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(0.05)}, d=0.0),
      TK(DOME3, {'R': R5(add(CAKE3, [-0.35, 0.95, 0.05])), 'L': R5(add(CAKE3, [0.35, 0.95, 0.05]))}, d=0.3, e='in', keep=True),   # lowers the dome
      TK(r(DOME3 + 0.32), sq=(1.05, 0.95, 1.05), d=0.05, keep=True), TK(r(DOME3 + 0.45), sq=(1, 1, 1), d=0.1, keep=True),
      TK(r(LOCK3 - 0.25), {'L': R5(add(CAKE3, [0.42, 0.18, 0.05])), 'R': R5(add(CAKE3, [-0.42, 0.5, -0.2]))}, {'L': 'pinch', 'R': 'open'}, bend={'spine': SP(0.1)}, d=0.2, keep=True),
      TK(LOCK3, {'L': R5(add(CAKE3, [0.4, 0.1, 0.06]))}, face={**STERN, 'lid': 0.1}, sq=(1.06, 0.94, 1.06), d=0.05, e='out', keep=True), TK(r(LOCK3 + 0.15), sq=(1, 1, 1), d=0.1, keep=True),   # snap
      k(r(LOCK3 + 0.25), look='camera', lookDur=0.15), TK(r(LOCK3 + 0.3), face=SMUG, bend={'spine': SP(0.0)}, d=0.15, keep=True), *blink(1.0, STERN)]
wife3, wprops3 = WIFE('S03', WF3, WRY3, 'cake', t0=0.6, every=0.5)
st.shot('S03', 'whiteVoid', setOpts={'color': '#E9DCC8'}, look={'sunDir': [-0.3, 0.6, 0.9]}, actors=[act('mec', HER3, HRY3, 'stand', 'neutral', keys=k3), wife3],
        props=[P('salle3', 'rgRoom', pos=[0, 0, 0.0], opts={'w': 6, 'd': 4, 'wall': '#E8C9A0', 'floor': '#A9784A', 'window': {'x': -0.4, 'y': 1.75, 'w': 1.6, 'h': 1.3, 'dusk': True}}),
               P('sirene3', 'alarmSiren', pos=[-0.95, 2.0, -1.93], opts={'from': 0.0, 's': 1.5, 'len': 0.4}),
               P('table3', 'table', pos=[0.0, 0, 0.2], opts={'w': 1.3, 'd': 0.8, 'h': 0.95}), P('gateau3', 'rgCake', pos=CAKE3, opts={'s': 0.38}),
               P('cloche3', 'rgDome', pos=add(CAKE3, [0, 0.95, 0]), opts={'r': 0.3, 'h': 0.6}, keys=[k(DOME3, to=CAKE3, dur=0.3, ease='in')]),
               P('cadenas3', 'fuPadlock', pos=add(CAKE3, [0.36, 0.12, 0.1]), ry=60, opts={'w': 0.3, 'open': True, 'shutAt': LOCK3}, keys=[k(0.0, visible=False), k(r(LOCK3 - 0.3), visible=True)]), *wprops3], cams=[C3])
st.cue('sfx:static', 'S03', 0.0, 0.2); st.cue('clang', 'S03', r(DOME3 + 0.3), 0.3); st.cue('sfx:cuff', 'S03', LOCK3, 0.45)

# ================================================================= S04
# 4: a country road at dusk (orange sky): a plain red-and-white barrier pole (no booth, no sign); big cheese wheels roll under it one after another;
#    at the back of the line the president trots after them with his two suitcases; EXIL
D4 = st.dur('S04'); CARD4 = r(st.at('S04', 'L04', 6))
BAR = [0.0, 0, 0.0]
C4 = cam(0.0, [0.5, 1.45, 4.3], [0.45, 1.44, 4.1], [-0.8, 1.0, 0.2], [-0.6, 1.0, 0.2], lens=60)
chk('S04', C4, {'barMid': [0, 1.05, 0], 'pres0': [-4.2, 1.95, 0.25], 'pres1': [-0.6, 1.95, 0.25]})
PR4A, PR4B = [-3.3, 0, 0.75], [-0.4, 0, 0.75]
cheeses = [P(f'fromage4_{i}', 'rgCheese', pos=[-3.0 + 1.0 * i, 0, -0.3], opts={'r': 0.42, 'roll': [0.0, D4, 4.2]}) for i in range(4)]   # on the barrier's line: they roll under the pole
st.shot('S04', 'grassland', look={'sunDir': [-0.6, 0.35, -0.5]}, actors=[],
        props=[P('ciel4', 'rgDusk', pos=[0, 0, -30], opts={'w': 90, 'h': 26, 'country': True}), P('route4', 'parkLot', pos=[0, 0.02, 0.2], opts={'w': 30, 'd': 2.6, 'color': '#6E6A66'}),
               P('barriere4', 'rgBarrier', pos=BAR, opts={'w': 2.6}), *cheeses,
               P('president4', 'rgPresident', pos=PR4A, ry=60, opts={'walk': [0.0, D4, 3.2], 'look': [[0, -0.6]], 'smile': [[0, 0.3]], 'carry': True}, keys=[k(0.0, to=PR4B, dur=D4, ease='linear')]),
               *[P(f'valise4{c}', 'rgCase', pos=add(PR4A, off([0, 0, 0], 60, 0.0, sx * 0.66, 0.4)), ry=60, opts={'w': 0.5, 'h': 0.4, 'd': 0.26, 'bulge': 0.2}, keys=[k(0.0, to=add(PR4B, off([0, 0, 0], 60, 0.0, sx * 0.62, 0.12)), dur=D4, ease='linear')]) for c, sx in (('a', 1), ('b', -1))]], cams=[C4])
st.card('S04', 'EXIL', at=CARD4)
for j in range(4): st.cue('sfx:stepRun', 'S04', r(0.3 + 0.55 * j), 0.15)

# ================================================================= S05
# 5: the town-hall council room (straight benches, a plain coloured board): a minister steps onto a column scale and its big weight jumps to the far
#    end with a clunk; behind him the next minister quietly takes off his jacket and shoes. Cut: two ushers carry the heavy minister out on his chair
D5 = st.dur('S05'); STEP5 = 0.2; JUMP5 = 0.55; CUT5 = r(st.at('S05', 'L05', 5) - 0.1)
SC5 = [0.3, 0, -0.6]
MIN1 = add(SC5, [0, 0.09, 0.05]); MIN1A = [0.3, 0, 0.4]
MIN2 = [-0.6, 0, -1.05]; MRY2 = 15
C5 = fcam(0.0, [0.6, 1.35, 4.6], {'m1Top': add(MIN1, [0, 2.45, 0]), 'scale': add(SC5, [0, 1.7, -0.2]), 'scaleB': add(SC5, [0, 0, 0.3]), 'm2Top': add(MIN2, [0, 2.4, 0]), 'm2K': add(MIN2, [0, 0.4, 0]), 'sign': [1.6, 2.2, -2.5]}, top=0.1, bottom=0.8, margin=0.07, push=0.25)
chk('S05', C5, {'m1Face': add(MIN1, [0, 1.95, 0]), 'weight': add(SC5, [0.2, 1.55, -0.2]), 'm2Face': add(MIN2, [0, 1.95, 0])})
CH5A, CH5B = [0.0, 0, 0.6], [2.6, 0, 0.6]
C5b = cam(CUT5, [0.6, 1.35, 5.2], [2.0, 1.35, 5.1], [0.4, 1.2, 0.6], [2.2, 1.2, 0.6], lens=48)
chk('S05b', C5b, {'minFace': add(CH5A, [0, 1.55, 0]), 'chairEnd': add(CH5B, [0, 1.5, 0])})
km1 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, HANDS(MIN1, 0, 0.1, 0.3, 1.0, 0.1, -0.3, 1.0), {'R': 'rest', 'L': 'rest'}, CALM, d=0.0), TK(0.1, sq=(1.05, 0.95, 1.05), d=0.08, keep=True), TK(0.25, sq=(1, 1, 1), d=0.1, keep=True),
       TK(JUMP5, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'jaw': 1.0}, sq=(1.3, 0.7, 1.3), d=0.04, e='out', keep=True), TK(r(JUMP5 + 0.3), face={**SAD, 'mouth': 'O', 'jaw': 0.6}, sq=(1.05, 0.95, 1.05), d=0.15, keep=True),   # flattened by the verdict
       k(r(JUMP5 + 0.02), look=add(SC5, [0.3, 1.6, -0.2]), lookDur=0.08), k(r(JUMP5 + 0.45), look='camera', lookDur=0.15), *blink(0.95, SAD), *BREATHE(1.1, CUT5, 0.45, 0.02)]
km2 = [k(0.0, clip='stand'), k(0.0, look=add(SC5, [0, 1.6, 0])), TK(0.0, {'R': R5(off(MIN2, MRY2, 0.15, 0.12, 1.6)), 'L': R5(off(MIN2, MRY2, 0.15, -0.12, 1.6))}, {'R': 'pinch', 'L': 'pinch'}, WORRY, d=0.0),   # at his lapels
       TK(0.45, {'R': R5(off(MIN2, MRY2, -0.1, 0.45, 1.3)), 'L': R5(off(MIN2, MRY2, -0.1, -0.45, 1.3))}, d=0.3, keep=True),   # the jacket off
       TK(0.95, {'R': R5(off(MIN2, MRY2, 0.25, 0.1, 0.25)), 'L': R5(off(MIN2, MRY2, 0.15, -0.3, 0.9))}, {'R': 'pinch', 'L': 'rest'}, bend={'spine': SP(0.7)}, d=0.3, keep=True),   # a shoe off
       TK(1.45, {'R': R5(off(MIN2, MRY2, 0.2, 0.3, 0.95))}, {'R': 'grip'}, bend={'spine': SP(0.0)}, face={**WORRY, 'mouth': 'smile'}, d=0.25, keep=True), *blink(0.3, WORRY)]
# the cut: the heavy minister sits on his chair; two ushers carry it out (they walk; their hands key every 0.2 s to the chair's arms)
DC = r(D5 - CUT5)
def chairAt(t): return lerp3(CH5A, CH5B, min(1.0, max(0.0, (t - CUT5) / DC)))
kc = [k(0.0, clip='sit'), k(0.0, look='camera'), k(0.0, visible=False), k(CUT5, visible=True), k(CUT5, to=add(CH5B, [0, -0.08, 0]), dur=DC, clip='sit', ease='linear', face='keep'),
      TK(0.0, HANDS(CH5A, 0, 0.3, 0.3, 0.6, 0.3, -0.3, 0.6), {'R': 'grip', 'L': 'grip'}, {**SAD, 'mouth': 'O'}, d=0.0), *blink(r(CUT5 + 0.5), SAD)]
ush = []
for i, sx in enumerate([-1, 1]):
    a = add(CH5A, [sx * 0.62, 0, 0]); b = add(CH5B, [sx * 0.62, 0, 0]); hand = 'L' if sx < 0 else 'R'; other = 'R' if sx < 0 else 'L'
    ks = [k(0.0, clip='walk'), k(0.0, visible=False), k(CUT5, visible=True), k(CUT5, to=b, dur=DC, clip='walk', ease='linear', face='keep', params={'freq': 1.8}), k(0.0, look='camera'),
          TK(0.0, {hand: R5(add(a, [-sx * 0.32, 0.68, 0.12])), other: R5(add(a, [-sx * 0.32, 0.68, -0.12]))}, {'R': 'grip', 'L': 'grip'}, {**STERN, 'mouth': 'clench'}, bend={'spine': SP(0.25)}, d=0.0),
          *[TK(r(CUT5 + j * 0.2), {hand: R5(add(chairAt(r(CUT5 + (j + 1) * 0.2)), [sx * 0.3, 0.6, 0.12])), other: R5(add(chairAt(r(CUT5 + (j + 1) * 0.2)), [sx * 0.3, 0.6, -0.12]))}, sq=(1.1, 0.86, 1.1) if j % 2 == 0 else (0.98, 1.0, 0.98), d=0.2, e='linear', keep=True) for j in range(int(DC / 0.2) + 1)]]   # buckling and waddling under it
    ush.append(act(f'huissier{i + 1}', a, -90 * sx, 'walk', 'neutral', keys=ks))
st.shot('S05', 'mairie', setOpts={'banner': False, 'map': False, 'desk': False, 'flagX': 40, 'clockX': -3.0}, look={'sunDir': [0.3, 0.9, 0.9]},
        actors=[act('ministre1', MIN1, 0, 'stand', 'neutral', keys=km1), act('ministre2', MIN2, MRY2, 'stand', 'neutral', keys=km2), act('ministre1b', add(CH5A, [0, 0.05, 0]), 0, 'sit', 'neutral', keys=kc), *ush],
        props=[P('balance5', 'rgScale', pos=SC5, scale=1.6, opts={'jumpAt': JUMP5}), P('banc5a', 'rgBench', pos=[-2.4, 0, -1.7], opts={'w': 3}), P('banc5b', 'rgBench', pos=[2.6, 0, -1.7], opts={'w': 3}),
               P('panneau5', 'rgSign', pos=[1.6, 2.2, -2.55], opts={'w': 1.5, 'h': 0.85}),
               P('chaise5', 'rgChair', pos=CH5A, opts={'squashAt': r(CUT5 + 0.05)}, keys=[k(0.0, visible=False), k(CUT5, visible=True), k(CUT5, to=CH5B, dur=DC, ease='linear')])], cams=[C5, C5b])
st.cue('sfx:step', 'S05', 0.1, 0.25); st.cue('clang', 'S05', JUMP5, 0.5); st.cue('sfx:stepHeavy', 'S05', r(CUT5 + 0.3), 0.25); st.cue('sfx:stepHeavy', 'S05', r(CUT5 + 0.75), 0.25)

# ================================================================= S06
# 6: tight, an alley at dusk under one street lamp: a man in a trench coat opens it toward us: its lining full of rows of glossy éclairs and choux;
#    a nervous buyer's mitten comes in and takes one
D6 = st.dur('S06'); OPEN6 = 0.35; TAKE6 = r(st.at('S06', 'L06', 6))
TM = [0.0, 0, 0.0]
C6 = cam(0.0, [0.2, 1.6, 2.7], [0.2, 1.58, 2.55], [0.05, 1.5, 0.0], [0.05, 1.5, 0.0], lens=54)
chk('S06', C6, {'face': add(TM, [0, 1.95, 0]), 'chest': add(TM, [0, 1.35, 0.25]), 'hem': add(TM, [0, 0.75, 0.2])})
ECL6 = add(TM, [0.42, 1.27, 0.25])
kt6 = [k(0.0, clip='stand'), k(0.0, look=[-1.2, 1.9, 1.5]), TK(0.0, {'R': R5(add(TM, [-0.12, 1.45, 0.3])), 'L': R5(add(TM, [0.12, 1.45, 0.3]))}, {'R': 'grip', 'L': 'grip'}, {'lid': 0.5, 'mouth': 'line', 'brow': -0.4}, d=0.0),
       TK(OPEN6, {'R': R5(add(TM, [-0.6, 1.35, 0.3])), 'L': R5(add(TM, [0.6, 1.35, 0.3]))}, d=0.25, e='out', keep=True), k(r(OPEN6 + 0.1), look=[1.2, 1.9, 1.5], lookDur=0.15),   # opens the coat, looks both ways
       k(r(OPEN6 + 0.8), look='camera', lookDur=0.12), TK(r(OPEN6 + 0.85), face={'lid': 0.4, 'mouth': 'smile', 'brow': 0.6}, d=0.1, keep=True), *blink(1.6, {'lid': 0.5, 'mouth': 'line', 'brow': -0.4}),
       *[TK(r(0.6 + 0.3 * j), sq=(1.02, 0.98, 1.02) if j % 2 == 0 else (0.99, 1.01, 0.99), bend={'spine': SP(0.05 * (j % 2), 0.06 * (1 if j % 2 else -1))}, d=0.25, keep=True) for j in range(5)],   # shifts his weight, sways
       k(0.95, look=[-1.2, 1.9, 1.5], lookDur=0.12), k(1.35, look=[1.2, 1.9, 1.5], lookDur=0.12), k(1.75, look='camera', lookDur=0.12),
       k(r(TAKE6 + 0.1), look=[1.2, 1.4, 1.5], lookDur=0.1), TK(r(TAKE6 + 0.15), face={'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}, sq=(1.02, 0.98, 1.02), d=0.1, keep=True), k(r(TAKE6 + 0.6), look='camera', lookDur=0.15), *BREATHE(1.2, D6, 0.5, 0.012), *blink(r(D6 - 0.5), {'lid': 0.4, 'mouth': 'smile', 'brow': 0.6})]
SLV6 = [[0.0, 1.6, 1.45, 1.3], [r(TAKE6 - 0.3), 1.6, 1.45, 1.3], [TAKE6, 0.52, 1.3, 0.42], [r(TAKE6 + 0.2), 0.52, 1.3, 0.42], [r(TAKE6 + 0.55), 1.7, 1.4, 1.2]]
st.shot('S06', 'streetNight', look={'sunDir': [0.3, 0.8, 0.6]}, actors=[act('resistant', TM, 0, 'stand', 'neutral', keys=kt6)],
        dark=[[0.0, 0.55, 0.001]], darkFloor=0.3, darkTint='#4A3A55', darkPool={'at': [0.0, 1.4, 0.3], 'r': 1.3, 'k': 1.0, 'tint': '#FFE2B0'},
        props=[P('ciel6', 'rgDusk', pos=[0, 0, -12], opts={'w': 30, 'h': 12}), P('lampe6', 'streetLamp', pos=[-0.62, 0, -0.45], opts={'on': True, 'height': 2.7}), P('mur6', 'brickWall', pos=[0, 0, -1.3]),
               P('manteau6', 'rgCoat', on={'actor': 'resistant', 'joint': 'torso', 'offset': [0, 0.42, 0.17]}, opts={'openAt': OPEN6, 'takeAt': r(TAKE6 + 0.02), 'take': [1, 1], 'w': 0.56, 'h': 0.95, 'color': '#4A3A2E'}),
               P('moufle6', 'rgSleeve', pos=SLV6[0][1:], ry=-130, opts={'color': '#6A5A8A', 'mitten': '#3E7FD6', 'holds': 'rgEclair', 'holdFrom': TAKE6}, keys=[k(SLV6[i][0], to=SLV6[i + 1][1:], dur=r(SLV6[i + 1][0] - SLV6[i][0]), ease='inOut') for i in range(len(SLV6) - 1)])], cams=[C6])
st.cue('sfx:zip', 'S06', OPEN6, 0.3); st.cue('sfx:paper', 'S06', TAKE6, 0.25)

# ================================================================= S07
# 7: a cellar lit warm by the glowing raclette machine itself: the door bursts open, two gendarmes in the doorway; round the machine six guests
#    freeze mid-bite, cheese dripping; among them the hero's wife, cheeks full
D7 = st.dur('S07'); BURST7 = 0.25
TAB7 = [0.0, 0, 0.3]; RAC7 = add(TAB7, [0, 0.95, 0])
DOOR7 = [-1.15, 0, -1.6]
GU = [([-0.95, 0, 0.0], 45), ([-0.45, 0, -0.38], 15), ([0.2, 0, -0.42], 0), ([0.95, 0, 0.0], -45), ([-0.75, 0, -0.75], 25), ([0.85, 0, -0.65], -25)]
C7 = cam(0.0, [0.25, 1.75, 3.4], [0.24, 1.74, 3.25], [0.35, 1.45, -0.8], [0.35, 1.45, -0.8], lens=56)
chk('S07', C7, {'door': add(DOOR7, [0, 1.8, 0]), 'rac': RAC7, **{f'g{i}': add(p, [0, 1.5, 0]) for i, (p, _) in enumerate(GU)}})
guests = []
for i, (p, ry) in enumerate(GU):
    nm = 'femme' if i == 2 else f'invite{i + 1}'
    mouth = off(p, ry, 0.2, 0.05, 1.42) if i != 2 else off(p, ry, 0.3, 0.12, 1.55)   # the wife's fork raised
    ks = [k(0.0, clip='sit'), k(0.0, look=RAC7), TK(0.0, {'R': R5(add(RAC7, [0.0, -0.05, 0.0]) if i % 2 else mouth), 'L': R5(off(p, ry, 0.35, -0.2, 0.95))}, {'R': 'pinch', 'L': 'rest'}, HAPPY, d=0.0),
          TK(r(BURST7 + 0.02 + 0.02 * i), face={'lid': 0.0, 'mouth': 'O' if i != 2 else 'line', 'brow': 1.0, 'pop': 1.0}, sq=(0.86, 1.2, 0.86), d=0.05, e='out', keep=True),   # eyes on stalks, a stretch up
          TK(r(BURST7 + 0.18 + 0.02 * i), face={'lid': 0.0, 'mouth': 'O' if i != 2 else 'line', 'brow': 1.0, 'pop': 0.3}, d=0.12, keep=True),
          k(r(BURST7 + 0.05 + 0.02 * i), look=add(DOOR7, [0, 1.8, 0]), lookDur=0.06), TK(r(BURST7 + 0.2), sq=(1, 1, 1), d=0.1, keep=True),
          k(r(1.1 + 0.15 * i), look='camera', lookDur=0.06), k(r(1.4 + 0.15 * i), look=add(DOOR7, [0, 1.8, 0]), lookDur=0.06)]   # eyes dart
    ks += [*[TK(r(BURST7 + 0.5 + 0.13 * j + 0.03 * i), sq=(1.015, 0.985, 1.015) if j % 2 == 0 else (1, 1, 1), d=0.06, keep=True) for j in range(14)], *blink(r(1.0 + 0.23 * i), {'lid': 0.0, 'mouth': 'O', 'brow': 1.0})]   # frozen, trembling
    if i == 2: ks += [TK(0.0, {'R': R5(off(p, ry, 0.32, 0.15, 1.6))}, {'R': 'pinch'}, d=0.0, keep=True), TK(r(BURST7 + 0.03), scl={'head': [1.18, 1.0, 1.05]}, d=0.06, keep=True), k(r(BURST7 + 0.8), look='camera', lookDur=0.15), TK(r(BURST7 + 1.2), scl={'head': [1.24, 0.97, 1.08]}, d=0.15, keep=True), TK(r(BURST7 + 1.5), scl={'head': [1.18, 1.0, 1.05]}, d=0.15, keep=True)]   # the wife: cheeks full, a chew, she looks at us   # the wife: cheeks full, she looks at us
    guests.append(act(nm, p, ry, 'sit', 'neutral', keys=ks))
gend = []
for i, sx in enumerate([-1, 1]):
    p = add(DOOR7, [sx * 0.3, 0, 0.25])
    ks = [k(0.0, clip='stand'), k(0.0, visible=False), k(BURST7, visible=True), k(0.0, look=RAC7), TK(0.0, HANDS(p, 0, 0.15, 0.25, 0.95, 0.15, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, STERN, d=0.0),
          TK(r(BURST7 + 0.1), sq=(1.08, 0.94, 1.08), d=0.05, e='out', keep=True), TK(r(BURST7 + 0.25), sq=(1, 1, 1), d=0.1, keep=True),
          TK(r(BURST7 + 0.4 + 0.1 * i), {'R': R5(off(p, 0, 0.5, 0.2, 1.7))}, {'R': 'point'}, d=0.15, keep=True), *blink(1.4, STERN)]
    gend.append(act(f'gendarme{i + 1}', p, 0, 'stand', 'neutral', keys=ks))
st.shot('S07', 'cave', look={'sunDir': [0.3, 0.9, 0.8]}, actors=[*guests, *gend],
        dark=[[0.0, 0.25, 0.001]], darkFloor=0.6, darkTint='#4A3A34', darkPool={'at': add(RAC7, [0, 0.45, -0.2]), 'r': 2.2, 'k': 1.0, 'tint': '#FFB860'},
        props=[P('table7', 'table', pos=TAB7, opts={'w': 1.4, 'd': 1.0, 'h': 0.95}), P('raclette7', 'rgRaclette', pos=RAC7),
               *[P(f'chaise7_{i}', 'chair', pos=p, ry=ry) for i, (p, ry) in enumerate(GU) if i < 4], P('fourchette7', 'rgFork', on={'actor': 'femme', 'hand': 'R', 'offset': [0, -0.02, 0.03]}, opts={'bite': '#FFD86A'}), P('porte7', 'rgDoor', pos=DOOR7, opts={'burstAt': BURST7, 'light': '#8FA8D0', 'dim': True})], cams=[C7])
st.cue('thud', 'S07', BURST7, 0.5); st.cue('whoosh', 'S07', BURST7, 0.2); st.cue('sfx:gasp', 'S07', r(BURST7 + 0.1), 0.3)

# ================================================================= S08
# 8: half a second: the hero on the column scale, the weight nudges back a hair. Cut, full frame: a giant weighbridge carrying a whole block of
#    houses, its big dial needle swinging a long way down; a crowd beside it cheers
D8 = st.dur('S08'); CUT8 = 0.55
SCALE8 = [40.0, 0, 0.0]; HER8 = add(SCALE8, [0, 0.09, 0.05])
C8 = cam(0.0, add(SCALE8, [1.1, 1.75, 1.9]), add(SCALE8, [1.07, 1.75, 1.8]), add(SCALE8, [0.15, 1.7, -0.2]), add(SCALE8, [0.15, 1.7, -0.2]), lens=50)   # the hero, the beam and the weight
chk('S08', C8, {'face': add(HER8, [0, 1.95, 0]), 'weight': add(SCALE8, [0.0, 1.55, -0.2])})
WB = [0.0, 0, -4.0]
C8b = fcam(CUT8, [0.6, 0.8, 9.2], {'wbL': add(WB, [-2.7, 0.0, 2.6]), 'wbTop': add(WB, [0, 3.9, 0]), 'gantry': add(WB, [4.3, 5.3, 1.8]), 'gR': add(WB, [4.3, 0.2, 1.8]), 'crowdT': [0, 2.0, 3.6]}, top=0.1, bottom=0.82, margin=0.03, push=0.3)
chk('S08b', C8b, {'dial': add(WB, [4.6, 3.6, 1.4]), 'house': add(WB, [0, 2.0, 0])})
kh8 = [k(0.0, clip='stand'), k(0.0, look=add(SCALE8, [0.1, 1.55, -0.2])), TK(0.0, HANDS(HER8, 0, 0.1, 0.25, 1.0, 0.1, -0.25, 1.0), {'R': 'rest', 'L': 'rest'}, {'lid': 0.0, 'mouth': 'line', 'brow': 0.7}, d=0.0),
       TK(0.2, face={'lid': 0.2, 'mouth': 'smile', 'brow': 0.9}, sq=(0.94, 1.08, 0.94), d=0.08, e='out', keep=True)]
CRW = [[1.6, 0, 1.4], [2.4, 0, 1.9], [-2.2, 0, 2.0], [-1.4, 0, 2.6]]
crowd8 = []
for i, p in enumerate(CRW):
    ry = 150 + 10 * i
    ks = [k(0.0, clip='stand'), k(0.0, look=add(WB, [3.55, 3.6, 1.6])), TK(0.0, HANDS(p, ry, 0.15, 0.25, 0.95, 0.15, -0.25, 0.95), {'R': 'rest', 'L': 'rest'}, CALM, d=0.0),
          *[TK(r(CUT8 + 0.35 + 0.05 * i + 0.3 * j), {'R': R5(off(p, ry, 0.15, 0.3, 2.3 - 0.25 * (j % 2))), 'L': R5(off(p, ry, 0.15, -0.3, 2.3 - 0.25 * ((j + 1) % 2)))}, {'R': 'open', 'L': 'open'}, HAPPY, sq=(0.96, 1.05, 0.96) if j % 2 == 0 else (1, 1, 1), d=0.15, keep=True) for j in range(4)]]
    crowd8.append(act(f'foule{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S08', 'grassland', look={'sunDir': [0.5, 0.9, 0.7]}, actors=[act('mec', HER8, 0, 'stand', 'neutral', keys=kh8), *crowd8],
        props=[P('salle8', 'rgRoom', pos=SCALE8, opts={'w': 4, 'd': 3, 'wall': '#E2EEF0', 'floor': '#D9D2C2'}), P('balance8', 'rgScale', pos=SCALE8, scale=1.25, opts={'nudge': [0.15, 0.04, 0.35]}),
               P('pont8', 'rgWeighbridge', pos=WB, opts={'w': 4.6, 'swing': [r(CUT8 + 0.2), r(CUT8 + 1.2), -0.3, 2.6], 'sink': [r(CUT8 + 0.1), r(CUT8 + 0.6), 0.12]})], cams=[C8, C8b])
st.cue('clack', 'S08', 0.25, 0.25); st.cue('sfx:tick', 'S08', r(CUT8 + 0.2), 0.3); st.cue('sfx:choir', 'S08', r(CUT8 + 0.4), 0.2)

# ================================================================= S09
# 9: the kitchen in the evening, one hanging lamp makes a warm pool on the table: the hero alone, staring; from the near edge of the frame the wife's
#    mitten and green sleeve slide one big glossy chocolate square into the light and withdraw; a sweat drop
D9 = st.dur('S09'); IN9, OUT9 = r(st.at('S09', 'L09', 3) - 0.35), r(st.at('S09', 'L09', 7))
TB9 = [0, 0, 0]; HER9 = [0.0, 0, -0.62]
CHO9 = [0.0, 0.95, 0.12]
C9 = cam(0.0, [0.25, 1.75, 2.3], [0.24, 1.74, 2.15], [0.0, 1.25, -0.1], [0.0, 1.25, -0.1], lens=48)
chk('S09', C9, {'face': add(HER9, [0, 1.5, 0]), 'choco': CHO9, 'lamp': [0, 2.4, 0.0], 'edge': [0.75, 1.0, 1.0]})
SL9 = [[0.0, 0.08, 1.06, 1.75], [IN9, 0.08, 1.06, 1.75], [r(IN9 + 0.5), 0.0, 1.06, 0.38], [r(OUT9 - 0.1), 0.0, 1.06, 0.38], [r(OUT9 + 0.4), 0.06, 1.06, 1.85]]   # from the near edge, toward the lamp
CHOK = [[0.0, add(SL9[0][1:], [0, -0.11, -0.16])], [IN9, add(SL9[1][1:], [0, -0.11, -0.16])], [r(IN9 + 0.5), add(SL9[2][1:], [0, -0.11, -0.16])]]   # the square rides ahead of the mitten, then stays
k9 = [k(0.0, clip='sit'), k(0.0, look=[0.0, 1.0, 0.9]), TK(0.0, HANDS(HER9, 0, 0.45, 0.25, 1.0, 0.45, -0.25, 1.0), {'R': 'rest', 'L': 'rest'}, {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}, d=0.0),
      k(r(IN9 + 0.15), look=[-0.8, 1.6, 1.6], lookDur=0.15),   # a look away (the eyes lead)...
      k(r(OUT9 + 0.05), look=add(CHO9, [0, 0.25, 0.1]), lookDur=0.05), TK(r(OUT9 + 0.05), face={'lid': 0.0, 'mouth': 'line', 'brow': 1.0}, scl={'head': [1.4, 0.88, 1.0]}, d=0.04, e='out', keep=True), TK(r(OUT9 + 0.12), scl={'head': [1, 1, 1]}, d=0.08, keep=True),   # ...and the whip back, smeared wide
      TK(r(OUT9 + 0.2), face={'lid': 0.1, 'mouth': 'line', 'brow': 0.8}, sq=(1, 1, 1), d=0.15, keep=True), *[TK(r(OUT9 + 0.3 + 0.12 * j), sq=(1.01, 0.99, 1.01) if j % 2 == 0 else (1, 1, 1), d=0.06, keep=True) for j in range(5)], *blink(0.6, CALM)]   # trembling
st.shot('S09', 'kitchenDay', look={'sunDir': [-0.5, 0.4, 0.6]}, actors=[act('mec', HER9, 0, 'sit', 'neutral', keys=k9)],
        dark=[[0.0, 0.72, 0.001]], darkFloor=0.22, darkTint='#3A2E34', darkPool={'at': [0.0, 1.1, 0.15], 'r': 1.0, 'k': 1.0, 'tint': '#FFE2A8'},
        props=[P('table9', 'table', pos=TB9, opts={'w': 1.6, 'd': 0.9, 'h': 0.95}), P('chaise9', 'chair', pos=add(HER9, [0, 0, -0.05])), P('lampe9', 'rgLamp', pos=[0, 3.3, -0.05], opts={'len': 0.95}),
               P('carre9', 'rgChoco', pos=CHOK[0][1], opts={'s': 0.24}, keys=[k(CHOK[i][0], to=CHOK[i + 1][1], dur=r(CHOK[i + 1][0] - CHOK[i][0]), ease='inOut') for i in range(len(CHOK) - 1)]),
               P('moufle9', 'rgSleeve', pos=SL9[0][1:], ry=180, opts={'color': WIFE_SLEEVE, 'mitten': '#C8322A', 'cuff': '#2E7A46', 'len': 0.9},
                 keys=[k(SL9[i][0], to=SL9[i + 1][1:], dur=r(SL9[i + 1][0] - SL9[i][0]), ease='inOut') for i in range(len(SL9) - 1)]),
               DROP('goutte9', 'mec', [0.25, 0.55, 0.1], 0.8, r(OUT9 + 0.3))], cams=[C9])
st.cue('sfx:paper', 'S09', r(IN9 + 0.4), 0.15); st.cue('sfx:gulp', 'S09', r(OUT9 + 0.4), 0.3)

# ================================================================= S10
# 10: close: the hero snaps the chocolate square in two, a loud crack, crumbs pop; his eyes close
D10 = st.dur('S10'); SNAP10 = 0.3
CH10 = [0.0, 1.22, 0.42]
C10 = cam(0.0, [0.2, 1.5, 1.9], [0.2, 1.5, 1.8], [0.0, 1.45, 0.0], [0.0, 1.45, 0.0], lens=48)
chk('S10', C10, {'face': [0, 1.95, 0.05], 'choco': CH10})
k10 = [k(0.0, clip='sit'), k(0.0, look=CH10), TK(0.0, {'R': R5(add(CH10, [-0.09, -0.01, 0.0])), 'L': R5(add(CH10, [0.09, -0.01, 0.0]))}, {'R': 'pinch', 'L': 'pinch'}, {'lid': 0.1, 'mouth': 'line', 'brow': 0.6}, d=0.0),
       TK(r(SNAP10 - 0.12), sq=(1.04, 0.96, 1.04), face={'lid': 0.0, 'mouth': 'line', 'brow': 0.8}, d=0.1, keep=True),
       TK(SNAP10, {'R': R5(add(CH10, [-0.17, 0.05, 0.0])), 'L': R5(add(CH10, [0.17, 0.05, 0.0]))}, face={'lid': 1.0, 'mouth': 'line', 'brow': 0.2}, sq=(0.95, 1.07, 0.95), d=0.06, e='out', keep=True),   # crack: eyes shut
       TK(r(SNAP10 + 0.01), scl={'head': [1.35, 0.5, 1.2]}, d=0.04, e='out', keep=True), TK(r(SNAP10 + 0.12), scl={'head': [0.9, 1.2, 0.95]}, d=0.1, keep=True), TK(r(SNAP10 + 0.25), scl={'head': [1, 1, 1]}, d=0.1, keep=True),   # flattened by the crack, then puffed back
       TK(r(SNAP10 + 0.2), face={'lid': 1.0, 'mouth': 'line', 'brow': 0.3}, sq=(1, 1, 1), d=0.15, keep=True), TK(r(SNAP10 + 0.4), sq=(1.04, 0.95, 1.04), bend={'spine': SP(0.12)}, d=0.4, keep=True)]   # eyes closed, a long exhale
st.shot('S10', 'kitchenDay', look={'sunDir': [-0.5, 0.4, 0.6]}, actors=[act('mec', [0, 0, 0], 0, 'sit', 'neutral', keys=k10)],
        dark=[[0.0, 0.5, 0.001]], darkFloor=0.32, darkTint='#4A3A40', darkPool={'at': add(CH10, [0, 0.2, 0]), 'r': 1.0, 'k': 1.0, 'tint': '#FFE2A8'},
        props=[P('chaise10', 'chair', pos=[0, 0, -0.05]), P('carre10', 'rgChoco', pos=CH10, rot=[1.25, 0, 0], opts={'s': 0.2, 'snapAt': SNAP10})], cams=[C10])
st.cue('sfx:crunch', 'S10', SNAP10, 0.6); st.cue('sfx:pop', 'S10', r(SNAP10 + 0.03), 0.25)

# ================================================================= S11
# 11: the town square from S02's angle: rope pullers small in the near corners haul; the broccoli statue creaks back, falls toward us across the frame
#    off its tall plinth, squashes on the cobbles, bounces once with hang time, then dust; TOMBÉ
D11 = st.dur('S11'); TOP11 = [0.4, 0.85]; CARD11 = r(TOP11[1] + 0.02)
RY11 = r(yaw(STAT, SQ) + 12)   # it falls toward us and across the frame: the plinth stays clear
PUL = [[-2.5, 0, -0.9], [-1.9, 0, -1.6], [0.9, 0, -0.6], [1.4, 0, -1.3]]
C11 = cam(0.0, [-2.6, 0.85, 6.0], [-2.55, 0.85, 5.9], [0.1, 2.6, -3.6], [0.1, 2.55, -3.6], lens=60)
chk('S11', C11, {'statTop': add(STAT, [0, 5.7, 0]), 'plinth': add(STAT, [0, 0.2, 0]), 'fallen': off(STAT, RY11, 4.0, 0, 0.6), **{f'p{i}': add(p, [0, 1.95, 0]) for i, p in enumerate(PUL)}})
pull = []
for i, p in enumerate(PUL):
    ry = yaw(p, STAT)
    hand = off(p, ry, 0.35, 0.0, 1.25)
    ks = [k(0.0, clip='stand'), k(0.0, look=add(STAT, [0, 4.5, 0])), TK(0.0, {'R': R5(add(hand, [0.03, 0.05, 0])), 'L': R5(add(hand, [-0.03, -0.05, 0.05]))}, {'R': 'grip', 'L': 'grip'}, STERN, bend={'spine': SP(-0.25)}, d=0.0),
          *[TK(r(0.02 + 0.13 * j), sq=(1.06, 0.94, 1.06) if j % 2 == 0 else (1, 1, 1), bend={'spine': SP(-0.45 if j % 2 == 0 else -0.25)}, d=0.1, keep=True) for j in range(3)],   # heave, heave
          TK(r(TOP11[0] + 0.25), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, d=0.1, keep=True),
          TK(r(TOP11[1] + 0.02), sq=(0.9, 1.12, 0.9), d=0.05, e='out', keep=True), TK(r(TOP11[1] + 0.15), sq=(1, 1, 1), d=0.1, keep=True), *blink(r(D11 - 0.3), STERN)]
    pull.append(act(f'foule{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S11', 'parisStreet', setOpts={'clouds': 4, 'eiffel': False}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=pull,
        props=[P('statue11', 'rgBroccoli', pos=STAT, ry=RY11, opts={'s': 3.0, 'plinth': 2.0, 'topple': [TOP11[0], TOP11[1], 1], 'creak': 0.3, 'dustDelay': 0.42,
                 'ropes': [[r(c) for c in ((lambda q: [q[0] * math.cos(math.radians(RY11)) - q[2] * math.sin(math.radians(RY11)), q[1], q[0] * math.sin(math.radians(RY11)) + q[2] * math.cos(math.radians(RY11))])([off(p, yaw(p, STAT), 0.35, 0.0, 1.25)[j] - STAT[j] for j in range(3)]))] for p in PUL]}),
               P('pave11', 'parkLot', pos=[-1.0, 0.03, 0.5], opts={'w': 12, 'd': 16, 'color': '#C9BFAE'})], cams=[C11])
st.card('S11', 'TOMBÉ', at=CARD11)
st.cue('sfx:stretch', 'S11', 0.05, 0.3); st.cue('sfx:squeak', 'S11', r(TOP11[0] - 0.15), 0.2); st.cue('thud', 'S11', TOP11[1], 0.7); st.cue('sfx:bonk', 'S11', r(TOP11[1] + 0.5), 0.3)

# ================================================================= S12
# 12: a street: a cheering crowd surges through a bakery door, baguettes held at chest height; the baker throws croissants over them like confetti
D12 = st.dur('S12')
BAK = [0.0, 0, -2.0]; DOORB = add(BAK, [0, 0, 0.1])
RUN = [([-1.6, 0, 1.4], 0.0), ([-2.0, 0, 2.3], 0.15), ([1.7, 0, 1.6], 0.05), ([2.0, 0, 2.5], 0.2), ([-1.0, 0, 3.0], 0.3)]
BAKER = add(BAK, [1.15, 0, 0.75])
C12 = cam(0.0, [0.6, 1.5, 6.4], [0.6, 1.48, 6.15], [0.0, 1.45, -1.0], [0.0, 1.45, -1.0], lens=54)
chk('S12', C12, {'door': add(DOORB, [0, 1.8, 0]), 'baker': add(BAKER, [0, 1.95, 0]), **{f'r{i}': add(p, [0, 1.95, 0]) for i, (p, _) in enumerate(RUN)}})
runners = []
for i, (p, t0) in enumerate(RUN):
    D = r(D12 - t0 - 0.05); ry = yaw(p, DOORB)
    def pos_at(t, p=p, t0=t0, D=D): return lerp3(p, add(DOORB, [0, 0, 0.2]), min(1.0, max(0.0, (t - t0) / D)))
    ks = [k(0.0, clip='run'), k(t0, to=add(DOORB, [0, 0, 0.2]), dur=D, clip='run', ease='in', face='keep', params={'freq': 2.6}), k(0.0, look='camera'), k(r(t0 + D - 0.05), visible=False),
          TK(0.0, {'R': R5(off(p, ry, 0.35, 0.12, 1.4)), 'L': R5(off(p, ry, 0.35, -0.12, 1.4))}, {'R': 'grip', 'L': 'grip'}, {'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, d=0.0),
          *[TK(r(j * 0.2), {'R': R5(off(pos_at(r((j + 1) * 0.2)), ry, 0.35, 0.12, 1.4)), 'L': R5(off(pos_at(r((j + 1) * 0.2)), ry, 0.35, -0.12, 1.4))}, d=0.2, e='linear', keep=True) for j in range(int(D12 / 0.2) + 1)]]
    runners.append(act(f'foule{i + 1}', p, ry, 'run', 'neutral', keys=ks))
kb = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(off(BAKER, 160, 0.2, 0.3, 1.2)), 'L': R5(off(BAKER, 160, 0.2, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, HAPPY, d=0.0),
      *[TK(r(0.15 + 0.3 * j), {'R': R5(off(BAKER, 160, 0.25, 0.25, 2.2 if j % 2 == 0 else 1.3))}, {'R': 'open' if j % 2 == 0 else 'grip'}, sq=(0.96, 1.05, 0.96) if j % 2 == 0 else (1, 1, 1), d=0.12, e='out', keep=True) for j in range(5)]]
st.shot('S12', 'parisStreet', setOpts={'clouds': 4, 'eiffel': False}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[*runners, act('boulanger', BAKER, 160, 'stand', 'neutral', keys=kb)],
        props=[P('boulangerie12', 'rgBakery', pos=BAK, opts={'w': 7}), P('trottoir12', 'parkLot', pos=add(BAK, [0, 0.02, 2.5]), opts={'w': 14, 'd': 6, 'color': '#D9D2C2'}),
               *[P(f'baguette12_{i}', 'baguette', on={'actor': f'foule{i + 1}', 'hand': 'R', 'offset': [0.0, 0.0, 0.0]}) for i in range(len(RUN))],
               P('croissants12', 'rgCroissants', pos=add(BAKER, [0, 2.1, 0]), opts={'n': 10, 'from': 0.15, 'every': 0.13, 'dir': [-0.6, 0.8]})], cams=[C12])
st.cue('sfx:stepRun', 'S12', 0.1, 0.3); st.cue('sfx:stepRun', 'S12', 0.6, 0.3); st.cue('sfx:choir', 'S12', 0.2, 0.15)

# ================================================================= S13
# 13: the same road and barrier as S04, now in bright sun: the cheese wheels roll back between two rows of applauding people; at the front the crowd
#    carries one big round camembert on its shoulders; confetti
D13 = st.dur('S13')
ROWS = [[-2.4, 0, -1.4], [-1.0, 0, -1.6], [0.6, 0, -1.5], [-2.0, 0, 2.2], [1.0, 0, 2.4]]
CAR0, CAR1 = [2.2, 0, -0.9], [-1.4, 0, -0.9]
CARRY = [[-0.45, 0, -0.3], [0.45, 0, -0.3], [-0.45, 0, 0.3], [0.45, 0, 0.3]]
C13 = cam(0.0, [0.5, 1.45, 4.3], [0.45, 1.44, 4.1], [-0.6, 1.55, 0.2], [-0.8, 1.55, 0.2], lens=60)   # the S04 framing
chk('S13', C13, {'camem0': add(CAR0, [0, 2.65, 0]), 'camem1': add(CAR1, [0, 2.65, 0]), **{f'row{i}': add(p, [0, 1.95, 0]) for i, p in enumerate(ROWS)}})
clap = []
for i, p in enumerate(ROWS):
    ry = (15 if p[0] < 0 else -15) + (180 if p[2] > 0 else 0)
    ks = [k(0.0, clip='stand'), k(0.0, look=CAR0), *[TK(r(0.05 * i + 0.22 * j), {'R': R5(off(p, ry, 0.35, 0.03 if j % 2 else 0.18, 1.45)), 'L': R5(off(p, ry, 0.35, -0.03 if j % 2 else -0.18, 1.45))}, {'R': 'open', 'L': 'open'}, HAPPY, d=0.1, keep=True) for j in range(int(D13 / 0.22))],
          k(1.5, look=CAR1, lookDur=0.4)]
    clap.append(act(f'foule{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
carriers = []
for i, o_ in enumerate(CARRY):
    a, b = add(CAR0, o_), add(CAR1, o_)
    def cpos(t, a=a, b=b): return lerp3(a, b, min(1.0, t / D13))
    ks = [k(0.0, clip='walk'), k(0.0, to=b, dur=D13, clip='walk', ease='linear', face='keep', params={'freq': 1.8}), k(0.0, look='camera'),
          TK(0.0, {'R': R5(add(a, [-o_[0] * 0.3, 2.45, -o_[2] * 0.3])), 'L': R5(add(a, [-o_[0] * 0.5, 2.45, -o_[2] * 0.5]))}, {'R': 'open', 'L': 'open'}, HAPPY, d=0.0),
          *[TK(r(j * 0.2), {'R': R5(add(cpos(r((j + 1) * 0.2)), [-o_[0] * 0.3, 2.45, -o_[2] * 0.3])), 'L': R5(add(cpos(r((j + 1) * 0.2)), [-o_[0] * 0.5, 2.45, -o_[2] * 0.5]))}, d=0.2, e='linear', keep=True) for j in range(int(D13 / 0.2) + 1)]]
    carriers.append(act(f'porteur{i + 1}', a, -90, 'walk', 'neutral', keys=ks))
cheeses13 = [P(f'fromage13_{i}', 'rgCheese', pos=[0.6 + 1.0 * i, 0, 0.0], ry=180, opts={'r': 0.42, 'roll': [0.0, D13, 4.4]}) for i in range(3)]
st.shot('S13', 'grassland', look={'sunDir': [0.5, 0.9, 0.7]}, actors=[*clap, *carriers],
        props=[P('route13', 'parkLot', pos=[0, 0.02, 0.4], opts={'w': 30, 'd': 3.2, 'color': '#8A8682'}), P('ciel13', 'rgDusk', pos=[0, 0, -30], opts={'w': 90, 'h': 26, 'country': True, 'day': True}), P('barriere13', 'rgBarrier', pos=[0.0, 0, 0.0], opts={'w': 2.6, 'lift': [[0, 1.3]]}), P('route13b', 'parkLot', pos=[0, 0.021, 0.2], opts={'w': 30, 'd': 2.6, 'color': '#6E6A66'}), *cheeses13,
               P('camembert13', 'rgCheese', pos=add(CAR0, [0, 2.48, 0]), opts={'r': 0.7, 'soft': True, 'flat': True, 'bob': 1.8}, keys=[k(0.0, to=add(CAR1, [0, 2.48, 0]), dur=D13, ease='linear')]),
               P('confettis13', 'confettiRain', pos=[0, 0, 0.5], opts={'w': 8, 'h': 4.5, 'd': 4, 'n': 140})], cams=[C13])
st.cue('sfx:fanfare', 'S13', 0.1, 0.25); st.cue('sfx:choir', 'S13', 0.4, 0.2)

# ================================================================= S14
# 14: behind the last cheese, the president walks in, now perfectly round and beaming, waving, his suitcases bulging; a jacket button pops off and
#    rolls past the camera
D14 = st.dur('S14'); POP14 = r(st.at('S14', 'L14', 7) - 0.1)
PR14A, PR14B = [1.9, 0, -0.4], [0.6, 0, 2.0]
C14 = fcam(0.0, [-0.6, 1.2, 8.2], {'pTop0': add(PR14A, [0, 2.1, 0]), 'pTop1': add(PR14B, [0, 2.15, 0]), 'pK1': add(PR14B, [0, 0.35, 0]), 'suitR': add(PR14B, [0.95, 0.5, 0]), 'suitL': add(PR14B, [-0.95, 0.5, 0])}, top=0.12, bottom=0.8, margin=0.08, push=0.3)
chk('S14', C14, {'pFace0': add(PR14A, [0, 1.95, 0]), 'pFace1': add(PR14B, [0, 1.95, 0])})
ry14 = yaw(PR14A, PR14B)
def p14(t): return lerp3(PR14A, PR14B, min(1.0, t / D14))
CH14 = add(p14(POP14), off([0, 0, 0], ry14, 0.62, 0, 1.0))
st.shot('S14', 'grassland', look={'sunDir': [0.5, 0.9, 0.7]}, actors=[],
        props=[P('route14', 'parkLot', pos=[0, 0.02, 0.8], opts={'w': 30, 'd': 3.2, 'color': '#8A8682'}), P('fromage14', 'rgCheese', pos=[0.4, 0, -0.2], ry=180, opts={'r': 0.42, 'roll': [0.0, D14, 3.5]}),
               P('president14', 'rgPresident', pos=PR14A, ry=ry14, opts={'round': 1.45, 'walk': [0.0, D14, 1.6], 'carry': True, 'smile': [[0, 1.0]], 'popAt': POP14, 'bounce': [POP14, r(POP14 + 0.02)]},
                 keys=[k(0.0, to=PR14B, dur=D14, ease='out')]),
               *[P(f'valise14{c}', 'rgCase', pos=add(PR14A, off([0, 0, 0], ry14, 0.1, sx * 0.78, 0.42)), ry=ry14, opts={'w': 0.55, 'h': 0.42, 'd': 0.3, 'bulge': 0.22}, keys=[k(0.0, to=add(PR14B, off([0, 0, 0], ry14, 0.1, sx * 0.78, 0.42)), dur=D14, ease='out')]) for c, sx in (('a', -1), ('b', 1))],   # a bulging case in each hand
               P('bouton14', 'rgButton', pos=CH14, scale=3.0, opts={'popAt': POP14, 'to': [r((-0.6 - CH14[0]) * 0.12), r(-CH14[1] / 3.0 + 0.02), r((8.2 - CH14[2]) * 0.14)], 'roll': [-0.25, 0.5]}, keys=[k(0.0, visible=False), k(POP14, visible=True)]),   # big, shot toward the lens
               P('confettis14', 'confettiRain', pos=[0.8, 0, 0.8], opts={'w': 6, 'h': 4, 'd': 3, 'n': 90})], cams=[C14])
st.cue('sfx:pop', 'S14', POP14, 0.45); st.cue('sfx:twang', 'S14', r(POP14 + 0.02), 0.2)

# ================================================================= S15
# 15: the kitchen: the hero, a tape measure round his waist, circles Monday in red on a big wall calendar; behind him his wife eats a crêpe
D15 = st.dur('S15'); CIRC15 = r(st.at('S15', 'L15', 3) - 0.25)
CAL = [-0.6, 1.75, -2.55]
HER15 = [0.15, 0, -1.85]; HRY15 = -70
WF15 = [1.25, 0, -1.2]; WRY15 = -35
C15 = fcam(0.0, [0.6, 1.25, 3.6], {'cal': add(CAL, [-0.3, 0.4, 0]), 'heroTop': add(HER15, [0, 2.35, 0]), 'heroK': add(HER15, [0, 0.55, 0]), 'wife': add(WF15, [0, 2.3, 0]), 'wifeR': add(WF15, [0.4, 1.0, 0])}, top=0.1, bottom=0.8, margin=0.06, push=0.25)
chk('S15', C15, {'cal': CAL, 'heroFace': add(HER15, [0, 1.95, 0]), 'wifeFace': add(WF15, [0, 1.85, 0])})
MON = add(CAL, [-0.18, 0.02, 0.06])
k15 = [k(0.0, clip='stand'), k(0.0, look=CAL), TK(0.0, {'R': R5(add(MON, [0.1, -0.1, 0.06])), 'L': R5(off(HER15, HRY15, 0.2, -0.28, 1.0))}, {'R': 'pinch', 'L': 'rest'}, {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}, d=0.0),
       *[TK(r(CIRC15 + 0.075 * j), {'R': R5(add(MON, [0.06 * math.cos(j * 0.8 + 1.6) - 0.12, 0.05 * math.sin(j * 0.8 + 1.6) - 0.02, 0.04]))}, bend={'spine': SP(0.1, 0.12)}, d=0.07, keep=True) for j in range(9)],   # the pen goes round, he leans in
       TK(r(CIRC15 + 0.7), {'R': R5(off(HER15, HRY15, 0.3, 0.3, 1.1))}, face={'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}, sq=(1.03, 0.97, 1.03), d=0.15, keep=True), k(r(CIRC15 + 0.7), look='camera', lookDur=0.15), *[TK(r(0.1 + 0.25 * j), {'R': R5(add(MON, [0.15 - 0.05 * (j % 2), -0.12, 0.08]))}, d=0.2, keep=True) for j in range(3)]]
wife15, wprops15 = WIFE('S15', WF15, WRY15, 'crepe', t0=0.1, every=0.5)
st.shot('S15', 'kitchenDay', actors=[act('mec', HER15, HRY15, 'stand', 'neutral', keys=k15), wife15],
        props=[P('calendrier15', 'rgCalendar', pos=CAL, opts={'w': 0.75, 'h': 0.95, 'circleAt': CIRC15, 'circleDur': 0.6, 'row': 2}), P('feutre15', 'rgMarker', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.0, 0.03]}),
               P('metre15', 'rgTapeRing', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.0, 0.0]}, opts={'r': 0.3}), *wprops15], cams=[C15])
st.cue('sfx:squeak', 'S15', CIRC15, 0.25)

# ================================================================= S16
# 16: the presidential bedroom from S01: the president in pyjamas sits on the bed; by the door on the right the two stuffed suitcases; he glances at
#    the wall calendar (Monday circled in red) by the door, a beat, gives the nearest case a little pat (it swells and settles) and leaves his hand on
#    it; held, deadpan
D16 = st.dur('S16'); PAT16 = r(st.at('S16', 'L16', 4))
BED16 = [0.0, 0, 0.0]
PR16 = add(BED16, [-0.45, 0.1, 0.25]); CAL16 = add(BED16, [0.45, 1.65, -1.94]); DOOR16 = add(BED16, [1.45, 0, -1.92])
SUITA = add(BED16, [0.4, 0, 0.35]); SUITB = add(BED16, [1.25, 0, -1.1])
C16 = cam(0.0, add(BED16, [0.1, 1.3, 5.6]), add(BED16, [0.1, 1.28, 5.15]), add(BED16, [0.2, 1.1, -0.4]), add(BED16, [0.2, 1.07, -0.4]), lens=54)   # a slow push
chk('S16', C16, {'face': add(PR16, [0, 1.45, 0]), 'cal': CAL16, 'suitA': add(SUITA, [0, 0.55, 0]), 'suitAfoot': SUITA, 'suitB': add(SUITB, [0.3, 0.55, 0]), 'door': add(DOOR16, [0, 2.2, 0])})
st.shot('S16', 'whiteVoid', setOpts={'color': '#E6DCCB'}, look={'sunDir': [0.3, 0.9, 0.8]}, actors=[],
        props=[P('chambre16', 'rgRoom', pos=BED16, opts={'w': 5, 'd': 4, 'wall': '#E6DCCB', 'floor': '#B58E66'}), P('lit16', 'bed', pos=add(BED16, [-0.6, 0, -0.75]), ry=90, opts={'blanket': '#9AB0C8'}),
               P('porte16', 'rgDoor', pos=DOOR16, opts={'light': '#F4EEE2', 'color': '#8A6A45'}),
               P('president16', 'rgPresident', pos=PR16, opts={'sit': True, 'pj': True, 'round': 1.45, 'look': [[0.0, 0.0], [0.25, 0.0], [0.45, 0.65], [r(PAT16 - 0.7), 0.65], [r(PAT16 - 0.4), 0.3]],
                 'pat': [PAT16], 'patArm': 'L', 'restAt': r(PAT16 + 0.3), 'bounce': [r(PAT16 + 0.02), r(PAT16 + 1.1), r(PAT16 + 1.9)], 'blink': [0.9, 1.6, r(PAT16 + 0.8), r(PAT16 + 1.6)], 'smile': [[0, 0.6], [r(PAT16 + 0.4), 0.95]]}),
               P('valise16a', 'rgCase', pos=SUITA, ry=-10, opts={'w': 0.6, 'h': 0.78, 'd': 0.34, 'bulge': 0.2, 'puff': [r(PAT16 + 0.02)]}),
               P('valise16b', 'rgCase', pos=SUITB, ry=-20, opts={'w': 0.66, 'h': 0.55, 'd': 0.34, 'bulge': 0.2}),
               P('calendrier16', 'rgCalendar', pos=CAL16, opts={'w': 0.5, 'h': 0.64, 'row': 2})], cams=[C16])
st.cue('sfx:bonk', 'S16', PAT16, 0.15)

for g_ in [('S01', CUT1, 'mec', 'packs'), ('S02', BOW2, 'general1', 'bow'), ('S03', LOCK3, 'mec', 'lock'), ('S04', 0.5, 'mec', 'trot'), ('S05', JUMP5, 'ministre1', 'scale'),
           ('S06', OPEN6, 'resistant', 'coat'), ('S07', BURST7, 'femme', 'raid'), ('S08', CUT8, 'mec', 'kilos'), ('S09', OUT9, 'mec', 'chocolate'), ('S10', SNAP10, 'mec', 'crack'),
           ('S11', TOP11[1], 'foule1', 'fall'), ('S12', 0.3, 'boulanger', 'bakery'), ('S13', 0.5, 'porteur1', 'triumph'), ('S14', POP14, 'mec', 'button'), ('S15', CIRC15, 'mec', 'monday'), ('S16', PAT16, 'mec', 'pat')]:
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
PRES = {'preset': 'politique', 'seed': 2101, 'hat': 'none', 'suit': '#2B3A55', 'lapel': '#22304A', 'tie': '#5A6E9A', 'shirt': '#EEF0F2', 'facial': 'none', 'hair': 'receding', 'hairColor': '#BDBDBD', 'glasses': False, 'toon': EX}
GENERAL = {'preset': 'cop', 'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'copcap', 'hatColor': '#4E5730', 'hatBand': '#2A2C22', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
GEND = {'preset': 'cop', 'outfit': 'suit', 'suit': '#1E2A44', 'pants': '#1E2A44', 'shirt': '#C9D6EA', 'lapel': '#18223A', 'tie': '#18223A', 'cuff': '#1E2A44', 'hat': 'copcap', 'hatColor': '#1E2A44', 'hatBand': '#2A2C30', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
MIN = {'preset': 'politique', 'hat': 'none', 'glasses': False, 'toon': EX}
GUEST = lambda pr, seed, suit: {'preset': pr, 'seed': seed, 'hat': 'none', 'suit': suit, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("Le régime", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'femme': {'preset': 'femme', 'seed': 2100, 'suit': WIFE_SLEEVE, 'glasses': False, 'toon': EX},
    **{f'general{i + 1}': {**GENERAL, 'seed': 2110 + i} for i in range(4)},
    'ministre1': {**MIN, 'seed': 2120, 'suit': '#4A4F58', 'lapel': '#3C414A', 'tie': '#7A2E2E', 'build': {'width': 1.5, 'headWidth': 1.35, 'belly': 0.35}},
    'ministre1b': {**MIN, 'seed': 2120, 'suit': '#4A4F58', 'lapel': '#3C414A', 'tie': '#7A2E2E', 'build': {'width': 1.5, 'headWidth': 1.35, 'belly': 0.35}},
    'ministre2': {**MIN, 'seed': 2121, 'suit': '#5A4A3A', 'lapel': '#4A3A2E', 'tie': '#2E4A6A', 'build': {'width': 0.95, 'headWidth': 1.2}},
    'huissier1': {**MIN, 'seed': 2122, 'suit': '#9AA3AE', 'lapel': '#8A939E', 'tie': '#3A3D44'}, 'huissier2': {**MIN, 'seed': 2123, 'suit': '#9AA3AE', 'lapel': '#8A939E', 'tie': '#3A3D44'},
    'resistant': {'preset': 'commissaire', 'seed': 2124, 'suit': '#B89A6A', 'lapel': '#A88A5A', 'glasses': False, 'toon': EX},
    **{f'invite{i + 1}': GUEST(['madame', 'worker', 'femme', 'tourist', 'fermier', 'mamie'][i], 2130 + i, ['#B5452E', '#3E7FB6', '#7A5A8A', '#D9A23A', '#5E8C4A', '#C86A8A'][i]) for i in range(6) if i != 2},
    'gendarme1': {**GEND, 'seed': 2140}, 'gendarme2': {**GEND, 'seed': 2141},
    **{f'foule{i + 1}': GUEST(['madame', 'worker', 'tourist', 'fermier', 'femme'][i], 2150 + i, ['#C8322A', '#3E7FB6', '#D9A23A', '#5E8C4A', '#8A5AB6'][i]) for i in range(5)},
    'boulanger': {'preset': 'chef', 'seed': 2160, 'glasses': False, 'toon': EX},
    **{f'porteur{i + 1}': GUEST(['worker', 'tourist', 'fermier', 'madame'][i], 2170 + i, ['#2E7D4F', '#C86A2A', '#3E5FB6', '#B5452E'][i]) for i in range(4)},
})
