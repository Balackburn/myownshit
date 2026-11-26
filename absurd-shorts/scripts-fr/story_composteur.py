#!/usr/bin/env python3
"""Le composteur (story 106; a fine composted with the ticket grows into a money tree, the country buries train tickets, and the fine grows too).
This man did not punch his train ticket: a fine. So he composts the ticket at the bottom of the garden, with the fine. In spring a money tree grows. His
neighbours buy train tickets to bury them; trains leave full and empty; the ticket price triples; money grows on trees; squirrels bury notes; in autumn
every note falls at once; they rake them and burn them; only the train ticket is worth anything. One morning the fine has grown too: an inspector.
Running gag (silent): beside the money tree in every shot of the hero's garden, a shoot in a navy peaked cap grows: a shoot (S03, S04), a knee-high bush
with a branch ending in a chrome punch that clacks (S08), a man-sized bush shaped like a uniform, eyes painted shut (S12), that bursts into leaves and
is the inspector of S01 (S13). Never in the neighbours' gardens. S16 is S01 again: the same framing, the same punch and hand-over of a blank pink slip.
Cards: COMPLET (S05), KRACH (S09). No other word, no figure, currency sign, flag, emblem or upright cross; the notes are blank lilac sheets with an
empty oval, the ticket a pale yellow card with one empty dotted circle, the fine a blank pink slip. At most five people in a shot."""
from story_kit import *
import math

st = Story('composteur', look='natural')
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
    return out
def DROP(pid, actor, t0, offset=(-0.24, 0.42, 0.0), scale=0.75):
    """a sweat drop that pops on his temple at t0, clear of the eye"""
    return P(pid, 'sweatDrop', on={'actor': actor, 'joint': 'head', 'offset': list(offset)}, scale=scale, keys=[k(0.0, visible=False), k(t0, visible=True), k(t0, squash=[1.6, 0.5, 1.6], dur=0.3)])
def CAP(pid, actor, y=0.42, s=0.8): return P(pid, 'coCap', on={'actor': actor, 'joint': 'head', 'offset': [0, y, 0]}, opts={'s': s})
def PYJ(pid, actor='mecPyj'): return P(pid, 'coPyjama', on={'actor': actor, 'joint': 'torso', 'offset': PYJ_OFF}, opts={'w': 0.52, 'd': 0.34, 'h': 0.85})
PYJ_OFF = [0, 0.62, 0]
def PUNCH(pid, actor='controleur', snap=(), s=1.3): return P(pid, 'coPunch', on={'actor': actor, 'hand': 'R', 'offset': [0, -0.12, 0.04], 'face': 'camera'}, opts={'snap': list(snap), 's': s})   # (round 2) turned flat to the lens, jaws up: a pair of pliers, never a gun
SHH = None

# the hero's garden (one layout for S02, S03, S08, S12-S16): the compost bin, the money tree growing out of it, the capped shoot beside the trunk
G0 = [0, 0, 0]; CB = [0.55, 0, -1.35]; SHT = [-0.6, 0, -0.8]
def GARDEN(sid, lawn='#7FB85A', wall='#EFE2C8'): return [P(f'jardin{sid}', 'coGarden', pos=G0, opts={'w': 7, 'd': 6, 'lawn': lawn, 'wall': wall}), P(f'compost{sid}', 'coCompost', pos=CB)]

# the inspector's punch-and-hand-over (S01 and S16, the same gesture and the same framing relative to him): the slip in his left mitten, the punch in
# his right; t0: the punch comes to the slip, CLACK, the slip is held out to the hero's hand point HAND, the hero takes it (one prop)
def INSP_CAM(at, P_, ry, push=0.12):
    # over the hero's shoulder, from above
    f, l = off(P_, ry, 2.4, -0.35, 1.8), off(P_, ry, 0.0, 0.05, 1.55); d = [l[i] - f[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in d))
    return cam(at, f, [r(f[i] + d[i] / n * push) for i in range(3)], l, l, lens=46)
def TWO_CAM(at, P_, ry, push=0.1):
    """(round 1) the S01 / S16 two-shot: three-quarters on the inspector, the hero (1.6 m in front of him) side on in silhouette: the slump and the hand-over read"""
    f, l = off(P_, ry, DGAP / 2, -3.7, 1.55), off(P_, ry, DGAP / 2, 0.0, 1.32); d = [l[i] - f[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in d))
    return cam(at, f, [r(f[i] + d[i] / n * push) for i in range(3)], l, l, lens=46)
DGAP, DHAND = 1.25, 0.68   # the inspector and the hero: 1.25 m apart; the slip held out 0.68 m in front of him
def INSP_KEYS(t0, P_, ry, HAND):
    SL = off(P_, ry, 0.38, -0.12, 1.25)
    return [TK(max(0.0, r(t0 - 0.4)), {'R': R5(off(P_, ry, 0.3, 0.22, 1.2)), 'L': R5(SL)}, {'R': 'grip', 'L': 'pinch'}, STERN, d=0.0),
            TK(r(t0 - 0.15), {'R': R5(add(SL, [0.0, 0.18, 0.0]))}, bend={'spine': SP(0.05)}, d=0.12, keep=True),   # the punch up (wind-up)
            TK(t0, {'R': R5(add(SL, [0.0, 0.06, 0.02]))}, sq=(1.06, 0.95, 1.06), face={**STERN, 'mouth': 'clench'}, d=0.05, e='in', keep=True),   # CLACK
            TK(r(t0 + 0.15), {'R': R5(off(P_, ry, 0.3, 0.22, 1.2))}, sq=(1, 1, 1), face=STERN, d=0.12, keep=True),
            TK(r(t0 + 0.3), {'L': R5(HAND)}, bend={'spine': SP(0.12)}, d=0.18, keep=True),   # held out to him
            TK(r(t0 + 0.75), {'L': R5(off(P_, ry, 0.2, -0.3, 1.0))}, {'L': 'rest'}, bend={'spine': SP(0.0)}, d=0.2, keep=True)]

# ================================================================= S01
# 1: two cuts. A mainline carriage, fields scrolling past: the inspector (navy uniform, plain navy cap) holds the hero's ticket right up to the lens and
#    taps its empty dotted circle with his big chrome punch, shaking his head. Cut: he punches a blank pink slip, clack, and hands it over; the hero
#    takes it and his shoulders sag
D1 = st.dur('S01'); TAP1 = r(st.at('S01', 'L01', 4)); CUT1 = r(min(st.at('S01', 'L01', 9) - 0.1, 1.85)); PN1 = r(CUT1 + 0.1)   # (round 3) the slip lands early enough for the sag to be held
HS1 = [-0.75, 0, -0.65]; HRY1 = 90; P1 = add(HS1, [r(DGAP * 0.807), 0, r(DGAP * 0.59)]); IRY1 = yaw(P1, HS1)
HAND1 = off(P1, IRY1, DHAND, -0.05, 1.3)
TK1 = off(P1, IRY1, 0.55, -0.04, 1.36)   # (round 3) the ticket held to the lens, below his eye line: the taps never hide his face
TAPP = off(TK1, IRY1, 0.03, -0.055, 0.0)   # the dotted circle (to his left, our right)
C1 = cam(0.0, off(P1, IRY1, 1.45, 0.0, 1.64), off(P1, IRY1, 1.35, 0.0, 1.64), off(P1, IRY1, 0.0, 0.0, 1.66), off(P1, IRY1, 0.0, 0.0, 1.66), lens=46)   # from his eyes
C1b = TWO_CAM(CUT1, P1, IRY1)
chk('S01', C1, {'ticket': TK1, 'head': off(P1, IRY1, 0, 0, 2.3)}); chk('S01b', C1b, {'head': off(P1, IRY1, 0, 0, 2.45), 'slip': off(P1, IRY1, 0.38, -0.12, 1.25), 'hand': HAND1, 'hero': add(HS1, [0, 1.65, 0])})
ki1 = [k(0.0, clip='stand'), k(0.0, look=HEAD(HS1, 1.3)), TK(0.0, {'R': R5(off(P1, IRY1, 0.3, 0.22, 1.2)), 'L': R5(add(TK1, [0.0, -0.08, -0.02]))}, {'R': 'grip', 'L': 'pinch'}, STERN, d=0.0),
       TK(r(TAP1 - 0.15), {'R': R5(add(off(TAPP, IRY1, 0.07, 0, 0), [0, 0.06, 0]))}, d=0.12, keep=True), TK(TAP1, {'R': R5(TAPP)}, sq=(1.03, 0.97, 1.03), d=0.05, e='in', keep=True),   # tap...
       TK(r(TAP1 + 0.12), {'R': R5(add(off(TAPP, IRY1, 0.07, 0, 0), [0, 0.06, 0]))}, sq=(1, 1, 1), d=0.06, keep=True), TK(r(TAP1 + 0.24), {'R': R5(TAPP)}, d=0.05, e='in', keep=True),   # ...tap, in the circle
       TK(r(TAP1 + 0.4), {'R': R5(off(P1, IRY1, 0.3, 0.22, 1.2))}, d=0.15, keep=True),
       *[k(r(TAP1 + 0.45 + 0.15 * j), look=HEAD(off(P1, IRY1, 1.0, 0.9 if j % 2 == 0 else -0.9, 0), 1.45), lookDur=0.07) for j in range(4)], k(r(TAP1 + 1.1), look='camera', lookDur=0.1),   # he shakes his head
       TK(r(TAP1 + 0.45), face={**STERN, 'brow': -0.8}, d=0.1, keep=True), *blink(0.45, STERN), *blink(r(CUT1 + 0.1), STERN), *blink(r(D1 - 0.3), STERN)]
ki1 += [k(CUT1, toon={'reach': {'R': R5(off(P1, IRY1, 0.3, 0.22, 1.2)), 'L': R5(off(P1, IRY1, 0.38, -0.12, 1.25))}}, toonDur=0.0, keepPose=True), *INSP_KEYS(PN1, P1, IRY1, HAND1)]
kh1 = [k(0.0, visible=False), k(CUT1, visible=True), k(0.0, clip='sit'), k(0.0, look=HEAD(P1, 2.0)), TK(0.0, {'R': R5(off(HS1, HRY1, 0.4, 0.2, 0.75)), 'L': R5(off(HS1, HRY1, 0.4, -0.2, 0.75))}, {'R': 'rest', 'L': 'rest'}, WORRY, d=0.0),
       TK(r(PN1 + 0.3), {'R': R5(add(HAND1, [0.0, -0.02, 0.0]))}, {'R': 'pinch'}, d=0.2, keep=True),   # he takes it...
       TK(r(PN1 + 0.5), sq=(1.07, 0.88, 1.07), bend={'spine': SP(0.3)}, face=SAD, d=0.12, keep=True), TK(r(PN1 + 0.62), bend={'spine': SP(0.3), 'neck': SP(0.35)}, d=0.15, keep=True), k(r(PN1 + 0.75), look='camera', lookDur=0.15),   # (round 3) the shoulders drop, the head follows, held
       *blink(r(PN1 + 1.1), SAD), *BREATHE(0.2, D1, 0.5)]
st.shot('S01', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('controleur', P1, IRY1, 'stand', 'neutral', keys=ki1), act('mec', HS1, HRY1, 'sit', 'neutral', keys=kh1)],
        props=[P('wagon1', 'coCarriage', pos=[0, 0, 0], opts={'len': 8, 'scroll': 5}),
               P('billet1', 'coTicket', on={'actor': 'controleur', 'hand': 'L', 'offset': [0.0, 0.1, 0.06], 'face': 'camera'}, keys=[k(CUT1, visible=False)]),
               P('amende1', 'coFine', on={'actor': 'controleur', 'hand': 'L', 'offset': [0.0, 0.12, 0.06], 'face': 'camera'}, opts={'punchAt': PN1}, keys=[k(0.0, visible=False), k(CUT1, visible=True), k(r(PN1 + 0.52), attach='mec', hand='R', offset=[0.0, 0.12, 0.05], rot=[0, 0, 0])]),
               PUNCH('poincon1', snap=[TAP1, r(TAP1 + 0.24), PN1], s=0.85),
               CAP('casquette1', 'controleur')], cams=[C1, C1b])
st.cue('sfx:tick', 'S01', TAP1, 0.25); st.cue('clack', 'S01', PN1, 0.5); st.cue('engine', 'S01', 0.0, 0.12)

# ================================================================= S02
# 2: his back garden, low camera: a wooden compost bin full of peelings. He drops the ticket in, then the pink slip, covers them with a spadeful of
#    peelings and pats it down; a worm pops its head up, looks at us and goes back in
D2 = st.dur('S02'); DT2 = 0.55; DF2 = 1.25; SP2 = 1.75
HB2 = add(CB, [-0.1, 0, -0.8]); HRY2 = 0; TOP2 = add(CB, [0, 0.95, 0])   # behind the bin, facing us: his face reads
C2 = fcam(0.0, [1.6, 0.55, 2.6], {'heroTop': add(HB2, [0, 2.35, 0]), 'heroFeet': HB2, 'bin': add(CB, [0.5, 0, 0.5]), 'binL': add(CB, [-0.5, 0.9, 0.5]), 'worm': add(CB, [-0.2, 0.4, 0.75])}, top=0.1, bottom=0.88)
chk('S02', C2, {'heroTop': add(HB2, [0, 2.35, 0]), 'bin': add(CB, [0, 0.8, 0])})
kh2 = [k(0.0, clip='stand'), k(0.0, look=TOP2), TK(0.0, {'R': R5(off(HB2, HRY2, 0.35, 0.2, 1.2)), 'L': R5(off(HB2, HRY2, 0.3, -0.25, 1.1))}, {'R': 'pinch', 'L': 'pinch'}, GRAVE, d=0.0),
       TK(r(DT2 - 0.3), {'R': R5(add(TOP2, [-0.1, 0.25, 0.1]))}, d=0.25, keep=True), TK(DT2, {'R': R5(add(TOP2, [-0.1, 0.3, 0.1]))}, {'R': 'spread'}, sq=(1.03, 0.97, 1.03), d=0.06, keep=True),   # plop: the ticket
       TK(r(DF2 - 0.3), {'L': R5(add(TOP2, [0.1, 0.25, 0.1]))}, d=0.25, keep=True), TK(DF2, {'L': R5(add(TOP2, [0.1, 0.3, 0.1]))}, {'L': 'spread'}, d=0.06, keep=True),   # and the fine
       TK(r(SP2 - 0.05), {'R': R5(off(HB2, HRY2, 0.3, 0.3, 0.9)), 'L': R5(off(HB2, HRY2, 0.35, 0.1, 1.15))}, {'R': 'grip', 'L': 'grip'}, d=0.15, keep=True),   # the spade
       TK(r(SP2 + 0.35), {'R': R5(add(TOP2, [0.0, 0.6, 0.35])), 'L': R5(add(TOP2, [0.0, 0.9, 0.45]))}, bend={'spine': SP(0.2)}, d=0.25, keep=True),   # the spadeful over the bin
       TK(r(SP2 + 0.65), {'R': R5(add(TOP2, [0.0, 0.25, 0.3])), 'L': R5(add(TOP2, [0.0, 0.6, 0.4]))}, sq=(1.09, 0.9, 1.09), d=0.07, e='in', keep=True), TK(r(SP2 + 0.8), {'R': R5(add(TOP2, [0.0, 0.5, 0.3])), 'L': R5(add(TOP2, [0.0, 0.85, 0.4]))}, sq=(1, 1, 1), d=0.1, keep=True),   # pat...
       TK(r(SP2 + 0.95), {'R': R5(add(TOP2, [0.0, 0.25, 0.3])), 'L': R5(add(TOP2, [0.0, 0.6, 0.4]))}, sq=(1.09, 0.9, 1.09), d=0.07, e='in', keep=True), TK(r(SP2 + 1.1), {'R': R5(add(TOP2, [0.0, 0.5, 0.3])), 'L': R5(add(TOP2, [0.0, 0.85, 0.4]))}, sq=(1, 1, 1), face=SMUG, d=0.1, keep=True),   # ...pat
       *blink(1.0, GRAVE), *BREATHE(0.2, D2, 0.5)]
st.shot('S02', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', HB2, HRY2, 'stand', 'neutral', keys=kh2)],
        props=[*GARDEN('S02'),
               P('billet2', 'coTicket', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.12, 0.05], 'face': 'camera'}, opts={'w': 0.42, 'h': 0.21}, keys=[k(r(DT2 + 0.03), detach=True, fall=True, floor=0.62)]),
               P('amende2', 'coFine', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, 0.16, 0.05], 'face': 'camera'}, opts={'w': 0.32, 'h': 0.42}, keys=[k(r(DF2 + 0.03), detach=True, fall=True, floor=0.64)]),
               P('pelle2', 'coSpade', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.05, 0], 'rot': [0, 0, 0]}, scale=1.3, opts={'dumpAt': r(SP2 + 0.4)}, keys=[k(0.0, visible=False), k(r(SP2 - 0.05), visible=True)]),
               P('ver2', 'coWorm', pos=add(CB, [-0.35, 0, 0.8]), opts={'s': 0.75, 'up': [[r(SP2 + 1.2), r(D2 - 0.12)]]})], cams=[C2])   # (round 3) the worm head-sized; it snaps back in
st.cue('sfx:paper', 'S02', DT2, 0.25); st.cue('sfx:paper', 'S02', DF2, 0.25); st.cue('thud', 'S02', r(SP2 + 0.65), 0.3); st.cue('thud', 'S02', r(SP2 + 0.95), 0.3); st.cue('sfx:pop', 'S02', r(SP2 + 1.3), 0.15)

# ================================================================= S03
# 3: the same garden in spring: out of the compost bin rises a round tree whose leaves are all blank lilac banknotes, fluttering. His jaw drops; he picks
#    one and holds it up to the light: the oval is empty. Beside the trunk, at the lens' height in this low shot, a bright-green shoot in a navy cap
D3 = st.dur('S03'); GROW3 = r(st.at('S03', 'L03', 3) - 0.3); JAW3 = r(st.at('S03', 'L03', 9) - 0.05); PICK3 = r(st.at('S03', 'L03', 10) - 0.15)
HB3 = add(CB, [-1.5, 0, -0.35]); HRY3 = 25; LEAF3 = add(CB, [-0.9, 1.8, 0.3]); UP3 = off(HB3, HRY3, 0.5, 0.32, 1.85)   # (round 3) beside his face, at mid-frame: the arm clear of the face
C3b = cam(r(JAW3 - 0.12), off(HB3, HRY3, 1.7, -0.2, 1.75), off(HB3, HRY3, 1.6, -0.2, 1.75), off(HB3, HRY3, 0, 0, 1.75), off(HB3, HRY3, 0, 0, 1.75), lens=46)   # (round 2) close on the take
C3 = fcam(0.0, [0.4, 0.6, 2.6], {'crown': add(CB, [-0.3, 2.6, 0]), 'shoot': add(SHT, [0, 0.4, 0]), 'shootB': SHT, 'heroTop': add(HB3, [0, 2.45, 0]), 'heroL': add(HB3, [-0.3, 1.2, 0]), 'heroF': add(HB3, [0, 0.3, 0])}, top=0.07, bottom=0.76, push=0.25)
chk('S03', C3, {'crown': add(CB, [0, 3.0, 0]), 'shoot': add(SHT, [0, 0.25, 0]), 'heroTop': add(HB3, [0, 2.35, 0])})
kh3 = [k(0.0, clip='stand'), k(0.0, look=add(CB, [0, 0.8, 0])), TK(0.0, HANDS(HB3, HRY3), {'R': 'rest', 'L': 'rest'}, CALM, d=0.0),
       k(r(GROW3 + 0.1), look=add(CB, [0, 1.5, 0]), lookDur=0.3), k(r(GROW3 + 0.7), look=add(CB, [0, 2.3, 0]), lookDur=0.3),   # his eyes follow it up
       TK(r(JAW3 - 0.08), sq=(1.06, 0.94, 1.06), d=0.06, keep=True), TK(JAW3, face={**POP, 'jaw': 1.0}, sq=(0.88, 1.15, 0.88), scl={'head': [0.88, 1.25, 0.9]}, d=0.05, e='out', keep=True), TK(r(JAW3 + 0.32), face={**POP, 'jaw': 1.0}, sq=(0.9, 1.13, 0.9), d=0.27, keep=True),   # (round 1) the take: eyes out on stalks, jaw to his chest, held
       TK(r(JAW3 + 0.45), face={**JAW, 'jaw': 0.6}, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.1, keep=True),
       TK(PICK3, {'R': R5(LEAF3)}, {'R': 'pinch'}, d=0.2, keep=True), k(PICK3, look=LEAF3, lookDur=0.15),   # he picks one...
       TK(r(PICK3 + 0.35), {'R': R5(UP3)}, face={'lid': 0.1, 'mouth': 'O', 'brow': 0.6}, bend={'neck': SP(-0.3)}, d=0.3, keep=True), k(r(PICK3 + 0.35), look=UP3, lookDur=0.25),   # ...and holds it up to the light
       TK(r(PICK3 + 0.8), face={'lid': 0.1, 'mouth': 'line', 'brow': 0.9}, d=0.1, keep=True), *blink(1.0, CALM), *blink(r(PICK3 + 0.9), {'lid': 0.1, 'mouth': 'line', 'brow': 0.9}), *BREATHE(0.2, D3, 0.5)]
st.shot('S03', 'whiteVoid', setOpts={'color': '#B4DCF2'}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('mec', HB3, HRY3, 'stand', 'neutral', keys=kh3)],
        props=[*GARDEN('S03', lawn='#86C460'), P('arbre3', 'coMoneyTree', pos=add(CB, [0, 0.35, 0]), opts={'grow': [[0, 0.0], [GROW3, 0.0], [r(GROW3 + 0.25), 0.35], [r(GROW3 + 0.9), 1.05], [r(GROW3 + 1.1), 1.0]]}),
               P('pousse3', 'coShoot', pos=SHT, scale=1.8, opts={'stage': 1}),
               P('billetb3', 'coNote', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.1, 0.05], 'face': 'camera'}, keys=[k(0.0, visible=False), k(r(PICK3 + 0.05), visible=True)])], cams=[C3, C3b])
st.cue('sfx:stretch', 'S03', GROW3, 0.25); st.cue('sfx:gasp', 'S03', JAW3, 0.2)

# ================================================================= S04
# 4: back gardens over low fences: three neighbours kneel in a row, each burying a yellow ticket with a trowel, patting the soil in sync; in the next
#    garden the hero does the same (a young money tree and the capped shoot beside him). Four people
D4 = st.dur('S04'); GW4 = 1.25; XS4 = [r((i - 1.5) * GW4) for i in range(4)]
C4 = fcam(0.0, [XS4[3] + 0.45, 0.38, 1.75], {'hero': [XS4[3], 1.55, 0.15], 'tk': [XS4[3] - 0.15, 0.0, 0.75], 'shoot': [XS4[3] + 0.5, 0.75, 0.55], 'n0': [XS4[0], 1.45, 0.15], 'n0f': [XS4[0], 0.0, 0.3]}, top=0.14, bottom=0.76, push=0.2)   # (round 3) low and close along the row
kn4 = []
for i, x in enumerate(XS4):
    p = [x, 0, 0.15]; ry = 0; nm = 'mec' if i == 3 else f'voisin{i + 1}'; T = add(p, [0.1, 0.06, 0.45])
    ks = [k(0.0, clip='kneel'), k(0.0, look=T), TK(0.0, {'R': R5(add(T, [0.05, 0.25, 0])), 'L': R5(add(T, [-0.2, 0.05, -0.05]))}, {'R': 'grip', 'L': 'spread'}, CALM, bend={'spine': SP(0.25)}, d=0.0)]
    for j in range(int((D4 - 0.2) / 0.48)):
        t = r(0.15 + 0.48 * j); ks += [TK(t, {'R': R5(add(T, [0.08, 0.02, -0.06]))}, bend={'spine': SP(0.4)}, d=0.1, keep=True), TK(r(t + 0.14), {'R': R5(add(T, [0.0, 0.2, 0.08]))}, bend={'spine': SP(0.28)}, d=0.1, keep=True),
                                         TK(r(t + 0.28), {'L': R5(add(T, [-0.05, 0.02, 0.0]))}, {'L': 'spread'}, sq=(1.05, 0.95, 1.05), d=0.06, e='in', keep=True), TK(r(t + 0.4), {'L': R5(add(T, [-0.2, 0.12, -0.05]))}, sq=(1, 1, 1), d=0.08, keep=True)]   # dig, then pat   # pat, pat: all in sync
    ks += [k(1.6, look='camera', lookDur=0.2), k(2.1, look=T, lookDur=0.2), *blink(r(0.7 + 0.15 * i), CALM)]
    kn4.append(act(nm, p, ry, 'kneel', 'neutral', keys=ks))
st.shot('S04', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=kn4,
        props=[P('jardins4', 'coGardens', pos=[0, 0, 0], opts={'n': 4, 'gw': GW4, 'd': 4}), *[P(f'billet4_{i}', 'coTicket', pos=[x - 0.15, 0.04, 0.62], rot=[-1.2, 0, 0.2], opts={'w': 0.5, 'h': 0.25}) for i, x in enumerate(XS4)],
               *[P(f'truelle4_{i}', 'coTrowel', on={'actor': 'mec' if i == 3 else f'voisin{i + 1}', 'hand': 'R', 'offset': [0, 0.04, 0]}) for i in range(4)],
               P('arbre4', 'coMoneyTree', pos=[XS4[3] + 0.4, 0, -0.9], opts={'s': 0.55, 'n': 70}), P('pousse4', 'coShoot', pos=[XS4[3] + 0.5, 0, 0.55], scale=2.4, opts={'stage': 1})], cams=[C4])
for j in range(int((D4 - 0.2) / 0.48)): st.cue('sfx:stepSoft', 'S04', r(0.43 + 0.48 * j), 0.1)

# ================================================================= S05
# 5: a station platform (the sign hidden under a plain band, a clock with hands only), shot from the platform: the carriage slides past, every seat empty;
#    the driver waves out of his cab at nobody, a lone pigeon on the platform watches it go. COMPLET card
D5 = st.dur('S05'); TR0, TR1 = [-3.4, 0, 1.6], [5.6, 0, 1.6]   # turned round (its windows face the platform): the windows of empty seats first, then the cab and its waving driver
def tr5(t): return lerp3(TR0, TR1, min(1.0, t / D5))
C5 = fcam(0.0, [-1.7, 1.65, -2.5], {'clock': [-0.9, 2.55, -0.7], 'clockB': [-0.9, 0.3, -0.7], 'edge': [1.5, 0.0, 0.0], 'winT': [1.0, 2.3, 0.2], 'cabT': [0.6, 2.55, 0.2]}, top=0.2, bottom=0.8, push=0.15, lenses=range(20, 61))   # (round 2) three-quarters from the platform
chk('S05', C5, {'win': [0.4, 1.75, 1.42], 'roof': [0.4, 2.9, 1.6], 'drv': add(add(TR0, [5.0, -0.25, 1.35]), [0, 2.3, 0])})
DRV = [-5.0, 0.05, -1.62]   # he leans out of the cab's side window
kd5 = [k(0.0, clip='wave'), k(0.0, to=add(TR1, DRV), dur=r(D5 - 0.8), clip='wave', ease='out', face='keep'), k(0.0, look='camera'), TK(0.0, face=HAPPY, d=0.0), *blink(0.5, HAPPY)]
st.shot('S05', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('conducteur', add(TR0, DRV), 180, 'wave', 'neutral', keys=kd5)],
        props=[P('quai5', 'coPlatform', pos=[0, 0, 0], opts={'len': 20, 'clockX': -0.9, 'clockZ': -0.7, 'clockH': 2.0, 'benchX': -4.0}), P('train5', 'coTrain', pos=TR0, ry=180, opts={'len': 9, 'wheels': False}, keys=[k(0.0, to=TR1, dur=r(D5 - 0.8), ease='out')])], cams=[C5])
st.cue('engine', 'S05', 0.0, 0.3); st.card('S05', 'COMPLET', at=st.at('S05', 'L05', 3))

# ================================================================= S06
# 6: a ticket window, a wall with a glass hatch: behind the glass the clerk swaps a small blank red price tag for a bigger one, then a huge one that slaps
#    over the whole glass; the customer in front beams and pushes a whole leafy lilac money branch through the slot
D6 = st.dur('S06'); SW6a = r(st.at('S06', 'L06', 4)); SW6b = r(SW6a + 0.6); SW60 = r(SW6a - 0.6); PUSH6 = r(st.at('S06', 'L06', 9) - 0.3)   # (round 3) small, bigger, huge: 0.6 s apart
CK6 = [0.0, 0, -0.55]; CU6 = [0.42, 0, 0.75]; CURY6 = 215
C6 = fcam(0.0, [-0.9, 1.6, 3.0], {'glassT': [0, 2.3, 0.06], 'glassL': [-0.75, 1.1, 0.06], 'cuTop': add(CU6, [0, 2.6, 0]), 'cuR': add(CU6, [0.45, 2.0, 0]), 'cuF': CU6, 'ckTop': add(CK6, [0, 2.3, 0])}, top=0.12, bottom=0.88)
kc6 = [k(0.0, clip='stand'), k(0.0, look=HEAD(CU6, 1.9)), TK(0.0, {'R': R5([0.25, 1.62, 0.0]), 'L': R5(off(CK6, 0, 0.25, -0.3, 1.0))}, {'R': 'pinch', 'L': 'rest'}, GRAVE, d=0.0),
       TK(r(SW6a - 0.15), {'R': R5([0.2, 1.55, -0.02])}, d=0.1, keep=True), TK(SW6a, {'R': R5([0.15, 1.7, 0.0])}, d=0.08, keep=True),   # swap...
       TK(r(SW6b - 0.25), {'R': R5([0.0, 2.15, -0.1])}, sq=(0.85, 1.22, 0.85), bend={'spine': SP(-0.15)}, d=0.15, keep=True), TK(SW6b, {'R': R5([0.0, 1.75, 0.0])}, sq=(1.15, 0.85, 1.15), bend={'spine': SP(0.12)}, d=0.05, e='in', keep=True),   # (round 1) a stretch up... and SNAP
       TK(r(SW6b + 0.12), sq=(0.96, 1.05, 0.96), d=0.08, keep=True), TK(r(SW6b + 0.3), {'R': R5(off(CK6, 0, 0.25, 0.3, 1.0))}, {'R': 'rest'}, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.2, keep=True), *blink(0.6, GRAVE), *blink(2.4, GRAVE), *BREATHE(0.2, D6, 0.5)]
SLOT6 = [0.0, 1.14, 0.12]
ku6 = [k(0.0, clip='stand'), k(0.0, look=[0, 1.7, 0.06]), *[k(r(t_ + 0.08), look=pt_, lookDur=0.06) for t_, pt_ in ((max(0.05, SW60), [0.25, 1.62, 0.08]), (r(SW60 + 0.3), HEAD(CK6, 1.9)), (SW6a, [0.15, 1.7, 0.08]), (r(SW6a + 0.3), HEAD(CK6, 1.9)))], TK(0.0, {'R': R5(off(CU6, CURY6, 0.3, 0.15, 1.1)), 'L': R5(off(CU6, CURY6, 0.3, -0.15, 1.15))}, {'R': 'grip', 'L': 'grip'}, CALM, d=0.0),   # (round 3) eye-darts between the tags
       TK(r(SW6b + 0.05), face={**HAPPY, 'mouth': 'smile', 'lid': 0.0}, sq=(0.95, 1.07, 0.95), d=0.06, e='out', keep=True), k(r(SW6b + 0.1), face=-35, turn=0.15), k(r(SW6b + 0.2), look='camera', lookDur=0.15), TK(r(SW6b + 0.3), sq=(1, 1, 1), d=0.12, keep=True), k(r(PUSH6 - 0.35), face=CURY6, turn=0.2),   # he turns to us and beams
       k(r(PUSH6 - 0.2), look=SLOT6, lookDur=0.15), TK(PUSH6, {'R': R5(add(SLOT6, [0.05, 0.05, 0.1])), 'L': R5(add(SLOT6, [-0.05, 0.12, 0.18]))}, bend={'spine': SP(0.2)}, d=0.3, keep=True),   # the branch through the slot
       TK(r(PUSH6 + 0.4), {'R': R5(add(SLOT6, [0.05, 0.03, -0.05]))}, d=0.2, keep=True), *blink(1.1, CALM), *BREATHE(0.2, D6, 0.5)]
st.shot('S06', 'whiteVoid', setOpts={'color': '#E8DCC8'}, look={'sunDir': [0.3, 0.9, 0.8]},
        actors=[act('guichetier', CK6, 0, 'stand', 'neutral', keys=kc6), act('client', CU6, CURY6, 'stand', 'neutral', keys=ku6)],
        props=[P('guichet6', 'coHatch', pos=[0, 0, 0]),
               P('prix6a', 'coTag', pos=[0.25, 1.62, 0.08], opts={'w': 0.14, 'slapAt': max(0.05, SW60)}, keys=[k(SW6a, visible=False)]), P('prix6b', 'coTag', pos=[0.15, 1.7, 0.085], opts={'w': 0.34, 'slapAt': SW6a}, keys=[k(SW6b, visible=False)]),
               P('prix6c', 'coTag', pos=[0.0, 1.68, 0.09], opts={'w': 1.3, 'slapAt': SW6b}),
               P('branche6', 'coBranch', on={'actor': 'client', 'hand': 'R', 'offset': [0, 0.05, 0.05], 'rot': [1.2, 0, 0]})], cams=[C6])
st.cue('sfx:paper', 'S06', max(0.05, SW60), 0.2); st.cue('sfx:paper', 'S06', SW6a, 0.2); st.cue('thud', 'S06', SW6b, 0.4); st.cue('sfx:paper', 'S06', PUSH6, 0.25)

# ================================================================= S07
# 7: two cuts. From the air, rolling hills of round lilac money trees ripple in the wind like a sea. Cut: a hiker on a forest path lifts his boot, a
#    lilac note stuck to the sole, and peels it off like a leaf
D7 = st.dur('S07'); CUT7 = r(st.at('S07', 'L07', 6) - 0.1); LIFT7 = r(CUT7 + 0.55); PEEL7 = r(LIFT7 + 0.45)
F7 = [100.0, 0, 0]
C7 = cam(0.0, add(F7, [-9.0, 13.0, 15.0]), add(F7, [-6.5, 11.5, 11.0]), add(F7, [0.0, 0.0, -2.0]), add(F7, [0.5, 0.0, -3.0]), lens=46, ease='inOut')
HK7a, HK7 = [0.0, 0, -1.6], [0.0, 0, 0.0]; HRY7 = 0
C7b = fcam(CUT7, [1.1, 1.0, 2.6], {'top': add(HK7, [0, 2.35, 0]), 'foot': off(HK7, HRY7, 0.55, 0.12, 0.6)}, top=0.12, bottom=0.66)
FOOT7 = off(HK7, HRY7, 0.32, 0.12, 0.5)
kk7 = [k(0.0, clip='walk'), k(0.0, visible=False), k(CUT7, visible=True), k(CUT7, to=HK7, dur=0.45, clip='walk', ease='out', params={'freq': 1.8}), k(r(CUT7 + 0.45), clip='stand', blend=0.08),
       k(0.0, look='camera'), TK(0.0, HANDS(HK7a, 0), {'R': 'rest', 'L': 'rest'}, CALM, d=0.0),
       *[TK(r(CUT7 + 0.2 * j), HANDS(lerp3(HK7a, HK7, min(1.0, 0.2 * j / 0.45)), 0), d=0.2, e='linear', keep=True) for j in range(3)],
       TK(r(LIFT7 - 0.15), sq=(1.05, 0.93, 1.05), bend={'spine': SP(0.1)}, d=0.1, keep=True),   # (round 3) anticipation
       TK(LIFT7, plant={'R': [*FOOT7, 1]}, sq=(1, 1, 1), bend={'spine': SP(0.3)}, face={'lid': 0.2, 'mouth': 'line', 'brow': 0.6}, d=0.15, keep=True), k(LIFT7, look=FOOT7, lookDur=0.15),   # the boot up into the lens: something on the sole
       TK(r(PEEL7 - 0.12), {'R': R5(add(FOOT7, [0.0, -0.06, 0.1]))}, {'R': 'pinch'}, d=0.15, keep=True),
       TK(r(PEEL7 + 0.08), {'R': R5(add(FOOT7, [0.0, 0.3, 0.2]))}, sq=(0.95, 1.06, 0.95), d=0.1, keep=True),   # pinch and peel, with a stretch
       TK(r(PEEL7 + 0.3), {'R': R5(off(HK7, HRY7, 0.4, 0.35, 1.6))}, plant={'R': [*off(HK7, HRY7, 0.05, 0.12, 0.0), 0]}, sq=(1, 1, 1), bend={'spine': SP(0.0)}, d=0.15, e='out', keep=True), k(r(PEEL7 + 0.2), look=off(HK7, HRY7, 0.35, 0.2, 1.75), lookDur=0.2),   # flick
       TK(r(PEEL7 + 0.45), face={'lid': 0.3, 'mouth': 'line', 'brow': 0.3}, d=0.1, keep=True), k(r(PEEL7 + 0.7), look='camera', lookDur=0.15), *blink(r(PEEL7 + 0.55), CALM)]
st.shot('S07', 'whiteVoid', setOpts={'color': SKY}, look={'sunDir': [0.4, 0.9, 0.8]},
        actors=[act('randonneur', HK7a, HRY7, 'walk', 'neutral', keys=kk7)],
        props=[P('foret7', 'coForest', pos=F7, opts={'w': 44, 'd': 44, 'n': 170}), P('chemin7', 'coPath', pos=[0, 0, 0]),
               *[P(f'arbre7_{i}', 'coMoneyTree', pos=p, opts={'s': 0.9, 'n': 90}) for i, p in enumerate([[-1.6, 0, -1.2], [1.7, 0, -2.0], [-1.9, 0, -3.5]])],
               P('billet7', 'coNote', on={'actor': 'randonneur', 'joint': 'footR', 'offset': [0, -0.07, 0.06], 'rot': [1.5708, 0, 0]}, opts={'w': 0.62}, keys=[k(PEEL7, attach='randonneur', hand='R', offset=[0.0, 0.1, 0.05], rot=[0, 0, 0]), k(r(PEEL7 + 0.32), detach=True, fall=True, floor=0.02)])], cams=[C7, C7b])
st.cue('gust', 'S07', 0.0, 0.3); st.cue('sfx:paper', 'S07', PEEL7, 0.3)

# ================================================================= S08
# 8: two cuts. The hero's garden: a big squirrel stuffs a note into its cheeks, digs and buries it, and a money sapling pops up behind it at once. Cut,
#    close: it buries another next to the capped shoot, now a knee-high bush with one branch ending in a chrome punch: the punch twitches, CLACK, and
#    the squirrel leaps back
D8 = st.dur('S08'); CUT8 = r(st.at('S08', 'L08', 6) - 0.1); POP8 = r(CUT8 - 0.35); CLK8 = r(st.at('S08', 'L08', 8) + 0.1)
SQ8a, SQ8 = [-1.9, 0, 0.6], [-1.15, 0, 0.35]; SAP8 = [-1.45, 0, -0.35]
SQ8c0, SQ8c = [-1.6, 0, 0.5], add(SHT, [-0.5, 0, 0.4])   # (round 3) one squirrel-length left of the bush, under the punch branch   # (round 1) on the punch side, clear of the bin
C8 = fcam(0.0, [-0.6, 0.6, 1.9], {'sq': add(SQ8, [0, 0.7, 0]), 'sqF': SQ8, 'sap': add(SAP8, [0, 1.2, 0]), 'sapF': SAP8, 'bush': add(SHT, [0.2, 0.9, 0]), 'bushF': add(SHT, [0.2, 0, 0.2])}, top=0.12, bottom=0.8, push=0.15)
C8b = fcam(CUT8, [-0.2, 0.6, 2.0], {'bush': add(SHT, [0, 0.85, 0]), 'bushB': add(SHT, [-0.3, 0.0, 0]), 'punch': add(SHT, [-0.65, 0.75, 0.15]), 'sqTop': add(SQ8c, [0, 1.0, 0]), 'sqF': add(SQ8c, [0.2, 0, 0.1])}, top=0.14, bottom=0.8, push=0.1)
st.shot('S08', 'whiteVoid', setOpts={'color': '#B4DCF2'}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[],
        props=[*GARDEN('S08', lawn='#86C460'), P('arbre8', 'coMoneyTree', pos=add(CB, [0, 0.35, 0])), P('buisson8', 'coShoot', pos=SHT, opts={'stage': 2, 'snap': [CLK8], 'twitch': [r(CLK8 - 0.35), r(CLK8 - 0.08)]}),
               P('pousse8', 'coMoneyTree', pos=SAP8, opts={'n': 50, 'grow': [[0, 0], [POP8, 0], [r(POP8 + 0.12), 0.4], [r(POP8 + 0.22), 0.3], [r(POP8 + 0.3), 0.33]]}), P('etincelle8', 'coSparkle', pos=add(SAP8, [0, 0.5, 0.2]), opts={'at': POP8}),
               P('ecureuil8', 'coSquirrel', pos=SQ8a, ry=60, scale=1.1, opts={'hop': [[0.0, 0.45], [r(CUT8), r(CUT8 + 0.35)]], 'dig': [[0.75, r(POP8 - 0.05)], [r(CUT8 + 0.45), r(CLK8 - 0.1)]], 'cheeks': [0.45, 0.85], 'startle': r(CLK8 + 0.06), 'popAt': r(CLK8 + 0.04)},
                 keys=[k(0.0, to=SQ8, dur=0.45, ease='out'), k(0.5, rotTo=[0, -0.4, 0], dur=0.2), k(CUT8, to=SQ8c0, dur=0.01), k(r(CUT8 + 0.02), to=SQ8c, dur=0.33, ease='out'), k(r(CUT8 + 0.02), rotTo=[0, -0.35, 0], dur=0.1)])], cams=[C8, C8b])
st.cue('sfx:scratch', 'S08', 0.8, 0.2); st.cue('sfx:pop', 'S08', POP8, 0.3); st.cue('clack', 'S08', CLK8, 0.5); st.cue('sfx:squeak', 'S08', r(CLK8 + 0.05), 0.25)

# ================================================================= S09
# 9: an autumn street in orange light, two money trees: they drop all their notes at once, brown and curled, in one big shower; a passer-by under a tree
#    vanishes beneath the pile, only his hat showing on top. KRACH card
D9 = st.dur('S09'); FALL9 = r(st.at('S09', 'L09', 5) - 0.15); KR9 = st.at('S09', 'L09', 6); POP9 = r(FALL9 + 1.0)
T9a, T9b = [-1.1, 0, -0.9], [1.5, 0, -1.6]; PA9a, PA9 = [-2.6, 0, -0.4], [-0.95, 0, -0.35]
C9 = fcam(0.0, [0.0, 1.1, 4.0], {'crownA': add(T9a, [0, 2.6, 0]), 'heapL': add(PA9, [-0.8, 0, 0.3]), 'heapR': add(PA9, [0.8, 0, 0.3]), 'popTop': add(PA9, [0, 3.75, 0]), 'treeB': add(T9b, [0.3, 2.4, 0])}, top=0.24, bottom=0.74)   # (round 3) closer, the heap above the captions
kp9 = [k(0.0, clip='walk'), k(0.0, to=PA9, dur=r(FALL9 - 0.3), clip='walk', ease='out', params={'freq': 1.8}), k(r(FALL9 - 0.3), clip='stand', blend=0.1), k(0.0, look='camera'), TK(0.0, face=CALM, d=0.0),
       *WALKHANDS(0.0, r(FALL9 - 0.3), [PA9a, PA9], {'R': (0.1, 0.25, 1.0), 'L': (0.1, -0.25, 1.0)}),
       k(r(FALL9 - 0.1), look=add(T9a, [0, 2.4, 0]), lookDur=0.1), TK(r(FALL9 + 0.05), face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0}, sq=(0.92, 1.1, 0.92), d=0.05, e='out', keep=True),
       k(r(FALL9 + 0.6), visible=False), k(POP9, visible=True), k(POP9, to=add(PA9, [0, 1.25, 0.05]), dur=0.01, clip='stand', face='keep'), k(POP9, look='camera', lookDur=0.0),
       TK(POP9, face={'lid': 0.4, 'mouth': 'line', 'brow': 0.3}, sq=(0.8, 1.3, 0.8), d=0.04, e='out', keep=True), TK(r(POP9 + 0.12), sq=(1.12, 0.88, 1.12), d=0.07, keep=True), TK(r(POP9 + 0.25), sq=(1, 1, 1), d=0.1, keep=True), *blink(r(POP9 + 0.4), CALM)]   # (round 1) POP: out of the pile, hat on
st.shot('S09', 'whiteVoid', setOpts={'color': '#F8EAD2'}, look={'sunDir': [0.3, 0.8, -0.5]},
        actors=[act('passant', PA9a, 90, 'walk', 'neutral', keys=kp9)],
        props=[P('rue9', 'coStreet', pos=[0, 0, 0], opts={'w': 14}), P('arbre9a', 'coMoneyTree', pos=T9a, opts={'brown': True, 'dropAt': FALL9, 'trunk': '#3A2414'}), P('arbre9b', 'coMoneyTree', pos=T9b, opts={'brown': True, 'dropAt': r(FALL9 + 0.02), 'trunk': '#3A2414'}),
               P('tas9', 'coHeap', pos=add(PA9, [0, 0, 0.05]), opts={'h': 2.25, 'r': 0.85, 'n': 150, 'growAt': [r(FALL9 + 0.15), r(FALL9 + 0.55)]}),
               P('chapeau9', 'coHat', on={'actor': 'passant', 'joint': 'head', 'offset': [0, 0.36, 0]}, keys=[k(r(FALL9 + 0.5), visible=False), k(POP9, visible=True)]),
               P('chapeau9b', 'coHat', pos=add(PA9, [0, 2.24, 0.05]), opts={'bumpAt': r(FALL9 + 0.55)}, keys=[k(0.0, visible=False), k(r(FALL9 + 0.5), visible=True), k(POP9, visible=False)])], cams=[C9])
st.cue('gust', 'S09', r(FALL9 - 0.2), 0.3); st.cue('thud', 'S09', r(FALL9 + 0.5), 0.5); st.card('S09', 'KRACH', at=KR9)

# ================================================================= S10
# 10: two cuts. A park: two gardeners in orange rake brown banknote leaves into a huge heap while a third blows more onto it. Cut: the heap is a
#    bonfire, and the same three warm their mittens at it, one toasting a sausage on a stick. Three people, never more
D10 = st.dur('S10'); CUT10 = r(st.at('S10', 'L10', 5) - 0.1)
HP10 = [0.0, 0, -0.4]; GD10 = [[-1.4, 0, 0.1], [1.2, 0, 0.0], [2.1, 0, 0.95]]   # (round 3) the blower on the side
C10 = fcam(0.0, [0.6, 1.9, 5.0], {**{f'g{i}': add(p, [0, 2.3, 0]) for i, p in enumerate(GD10)}, **{f'f{i}': p for i, p in enumerate(GD10)}, 'heap': add(HP10, [0, 1.0, 0])}, top=0.12, bottom=0.82)
WARM = [[-1.3, 0, 0.3], [1.1, 0, 0.55], [1.9, 0, -0.35]]   # (round 2) nobody behind the fire: all three on the sides, a clear gap
C10b = fcam(CUT10, [0.3, 1.45, 3.4], {'fire': add(HP10, [0, 1.5, 0]), 'fireL': add(HP10, [-0.95, 0.2, 0.3]), 'w1': add(WARM[1], [0, 2.3, 0]), 'w2': add(WARM[2], [0, 2.3, 0]), 'f1': WARM[1], 'f2': WARM[2]}, top=0.12, bottom=0.76)   # (round 3) closer on the fire: mittens and sausage
gd10 = []
for i, (p, w) in enumerate(zip(GD10, WARM)):
    ry = yaw(p, HP10); ryw = yaw(w, HP10); orange = {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}
    if i < 2:   # raking toward the heap
        ks = [k(0.0, clip='stand'), k(0.0, look=add(HP10, [0, 0.3, 0])), TK(0.0, {'R': R5(off(p, ry, 0.45, 0.15, 1.05)), 'L': R5(off(p, ry, 0.3, -0.1, 1.3))}, {'R': 'grip', 'L': 'grip'}, orange, bend={'spine': SP(0.2)}, d=0.0)]
        for j in range(int(CUT10 / 0.45)): t = r(0.1 + 0.45 * j); ks += [TK(t, {'R': R5(off(p, ry, 0.7, 0.15, 0.85)), 'L': R5(off(p, ry, 0.55, -0.1, 1.1))}, bend={'spine': SP(0.35)}, d=0.18, keep=True), TK(r(t + 0.22), {'R': R5(off(p, ry, 0.35, 0.15, 1.05)), 'L': R5(off(p, ry, 0.25, -0.1, 1.3))}, bend={'spine': SP(0.15)}, d=0.2, keep=True)]
    else:   # blowing more onto it
        ks = [k(0.0, clip='stand'), k(0.0, look=add(HP10, [0, 0.3, 0])), TK(0.0, {'R': R5(off(p, ry, 0.35, 0.15, 1.05)), 'L': R5(off(p, ry, 0.45, -0.05, 1.0))}, {'R': 'grip', 'L': 'grip'}, orange, d=0.0), *[TK(r(0.2 + 0.3 * j), sq=(1.02, 0.98, 1.02) if j % 2 else (1, 1, 1), d=0.15, keep=True) for j in range(int(CUT10 / 0.3))]]
    ks += [k(CUT10, to=w, dur=0.01, clip='stand', face='keep'), k(CUT10, face=ryw, turn=0.01), k(CUT10, look=add(HP10, [0, 1.0, 0]), lookDur=0.0),
           TK(r(CUT10 + 0.02), {'R': R5(off(w, ryw, 0.5, 0.12, 1.15)), 'L': R5(off(w, ryw, 0.5, -0.12, 1.15))}, {'R': 'spread', 'L': 'spread'}, face=HAPPY, bend={'spine': SP(0.05)}, d=0.0, keep=True)]
    if i == 2: ks += [TK(r(CUT10 + 0.02), {'R': R5(off(w, ryw, 0.45, 0.12, 1.2))}, {'R': 'grip'}, d=0.0, keep=True)]
    ks += [*[TK(r(CUT10 + 0.2 + 0.35 * j), {'L': R5(off(w, ryw, 0.52 + 0.04 * (j % 2), -0.12, 1.15 + 0.03 * (j % 2)))}, d=0.3, keep=True) for j in range(int((D10 - CUT10) / 0.35))],   # rubbing the mittens
           k(r(CUT10 + 0.6 + 0.15 * i), look='camera', lookDur=0.2), *blink(r(0.6 + 0.2 * i), orange), *blink(r(CUT10 + 0.5 + 0.2 * i), HAPPY), *BREATHE(0.1, D10, 0.5)]
    gd10.append(act(f'jardinier{i + 1}', p, ry, 'stand', 'neutral', keys=ks))
st.shot('S10', 'whiteVoid', setOpts={'color': '#C8D8E4'}, look={'sunDir': [-0.4, 0.8, 0.7]},
        actors=gd10,
        props=[P('parc10', 'coPath', pos=[0, 0, -2.5]), *[P(f'arbre10_{i}', 'coMoneyTree', pos=p, opts={'brown': True, 'dropAt': -5, 'n': 90}) for i, p in enumerate([[-2.4, 0, -2.6], [2.2, 0, -3.0]])],
               P('tas10', 'coHeap', pos=HP10, opts={'h': 0.9, 'r': 0.95, 'n': 120}, keys=[k(CUT10, visible=False)]), P('feu10', 'coBonfire', pos=HP10, opts={'r': 0.9, 'flame': 0.8}, keys=[k(0.0, visible=False), k(CUT10, visible=True)]),
               P('rateau10a', 'coRake', on={'actor': 'jardinier1', 'hand': 'R', 'offset': [0, 0.05, 0], 'rot': [0.6, 0, 0]}, keys=[k(CUT10, visible=False)]), P('rateau10b', 'coRake', on={'actor': 'jardinier2', 'hand': 'R', 'offset': [0, 0.05, 0], 'rot': [0.6, 0, 0]}, keys=[k(CUT10, visible=False)]),
               P('souffleur10', 'coBlower', on={'actor': 'jardinier3', 'hand': 'R', 'offset': [0, 0.0, 0.05]}, opts={'on': True}, keys=[k(CUT10, visible=False)]),
               P('saucisse10', 'coSausage', on={'actor': 'jardinier3', 'hand': 'R', 'offset': [0, 0.03, 0.03], 'rot': [1.0, 0, 0]}, keys=[k(0.0, visible=False), k(CUT10, visible=True)])], cams=[C10, C10b])
st.cue('sfx:scratch', 'S10', 0.1, 0.2); st.cue('gust', 'S10', 0.2, 0.25); st.cue('sfx:crunch', 'S10', CUT10, 0.3)

# ================================================================= S11
# 11: the station ticket window: a truck loaded with three whole money trees backs up to it, beep beep; the clerk, large behind his glass, counts the
#    trees with one finger, nods, and slides a single yellow ticket across the counter, very dignified
D11 = st.dur('S11'); TRK0, TRK1 = [6.2, 0, -3.4], [1.0, 0, -3.4]; CNT11 = [r(st.at('S11', 'L11', 5) + 0.1 + 0.35 * j) for j in range(3)]; NOD11 = r(CNT11[2] + 0.4); SLIDE11 = r(st.at('S11', 'L11', 12) - 0.2)
CK11 = CK6
C11 = fcam(0.0, [0.25, 1.75, 2.6], {'ckTop': add(CK11, [0, 2.45, 0]), 'ckW': add(CK11, [0, 1.05, 0]), 'glassL': [-0.72, 1.15, 0.06], 'glassR': [0.72, 2.25, 0.06]}, top=0.1, bottom=0.76, push=0.45)   # (round 3) medium on the clerk; the trees through the glass behind him
C11b = cam(r(SLIDE11 - 0.3), [0.25, 1.75, 1.3], [0.1, 1.5, 0.95], [0.05, 1.12, 0.15], [0.05, 1.12, 0.3], lens=40)   # close on the single ticket
TKT11 = [0.0, 1.13, -0.05]
kc11 = [k(0.0, clip='stand'), k(0.0, look=add(TRK0, [0, 2.0, 0])), TK(0.0, HANDS(CK11, 0), {'R': 'rest', 'L': 'rest'}, GRAVE, d=0.0),
        *[k(r(0.4 * j), look=add(lerp3(TRK0, TRK1, min(1.0, 0.4 * j / 2.2)), [-1.0, 2.0, 0]), lookDur=0.35) for j in range(6)],
        TK(r(CNT11[0] - 0.3), {'R': R5(off(CK11, 0, 0.38, 0.22, 1.75))}, {'R': 'point'}, d=0.2, keep=True),   # (round 3) a big finger up
        *[x for j, t in enumerate(CNT11) for x in (TK(r(t - 0.12), face={**GRAVE, 'gx': 0.8 - 0.8 * j}, d=0.05, keep=True), k(t, look=add(TRK1, [-1.6 + 1.05 * j, 2.3, 0]), lookDur=0.14),
                                                   TK(t, {'R': R5(off(CK11, 0, 0.42, 0.22, 1.82))}, face={**GRAVE, 'mouth': 'O' if j % 2 else 'line', 'gx': 0.8 - 0.8 * j}, sq=(0.97, 1.03, 0.97), d=0.06, e='out', keep=True), TK(r(t + 0.14), {'R': R5(off(CK11, 0, 0.38, 0.22, 1.75))}, sq=(1, 1, 1), d=0.1, keep=True))],   # the eyes lead each count: one, two, three
        TK(r(CNT11[2] + 0.25), {'R': R5(off(CK11, 0, 0.25, 0.3, 1.05))}, {'R': 'rest'}, d=0.15, keep=True),
        k(r(NOD11 - 0.15), look='camera', lookDur=0.15), TK(r(NOD11 - 0.05), bend={'neck': SP(-0.1)}, face={**GRAVE, 'gx': 0.0}, d=0.1, keep=True), TK(r(NOD11 + 0.12), bend={'neck': SP(0.45)}, face={**GRAVE, 'lid': 0.6}, d=0.25, keep=True), TK(r(NOD11 + 0.55), bend={'neck': SP(0.0)}, d=0.25, keep=True),   # (round 3) a slow, dignified nod
        TK(r(SLIDE11 - 0.2), {'L': R5(add(TKT11, [0.0, 0.03, 0.0]))}, {'L': 'pinch'}, d=0.15, keep=True), TK(SLIDE11, {'L': R5(add(TKT11, [0.0, 0.03, 0.4]))}, d=0.35, keep=True),   # the single ticket slid across
        *[TK(r(SLIDE11 + 0.5 + 0.25 * j + dt), {'L': R5(add(TKT11, [0.0, 0.03 + dy, 0.4]))}, sq=sq_, d=0.06, keep=True) for j in range(2) for dt, dy, sq_ in ((0.0, 0.07, (1, 1, 1)), (0.1, 0.0, (1.02, 0.98, 1.02)))],   # tap, tap: there you are
        k(r(SLIDE11 + 0.4), look='camera', lookDur=0.2), *blink(1.2, GRAVE), *blink(r(SLIDE11 + 0.55), GRAVE), *BREATHE(0.2, D11, 0.5)]
st.shot('S11', 'whiteVoid', setOpts={'color': '#E8DCC8'}, look={'sunDir': [0.3, 0.9, 0.8]},
        actors=[act('guichetier', CK11, 0, 'stand', 'neutral', keys=kc11)],
        props=[P('guichet11', 'coHatch', pos=[0, 0, 0], opts={'room': False}), P('prix11a', 'coTag', pos=[-0.45, 1.95, 0.085], opts={'w': 0.3}), P('prix11b', 'coTag', pos=[0.5, 1.95, 0.085], opts={'w': 0.22}), P('camion11', 'coTruck', pos=TRK0, opts={'trees': 3, 'beep': [0.3, 0.75, 1.2, 1.65, 2.1]}, keys=[k(0.0, to=TRK1, dur=2.2, ease='out')]),
               P('billet11', 'coTicket', pos=TKT11, rot=[-1.5708, 0, 0], opts={'w': 0.24, 'h': 0.12}, keys=[k(SLIDE11, to=add(TKT11, [0, 0, 0.4]), dur=0.35, ease='inOut')])], cams=[C11, C11b])
for t in [0.3, 0.75, 1.2, 1.65, 2.1]: st.cue('sfx:beep', 'S11', t, 0.2)

# ================================================================= S12
# 12: the hero's garden at dawn (the same cream wall, the compost bin, the money tree): in striped pyjamas, mug in hand, he stands beside the bush by
#    the trunk, now man-sized and shaped like a man in uniform (a leafy shell, eyes painted shut, a navy cap, a branch ending in the chrome punch): a sip,
#    a breath, a slow look up at it
D12 = st.dur('S12'); IRYE = -60; HP12 = off(SHT, IRYE, 1.3, 0, 0); HRY12 = 25   # (round 2) he stands to the left of the bush, three-quarters to us
DAWN_LAWN, DAWN_WALL = '#78AE58', '#EADCC2'
_f12, _l12, _n12 = fitBack([-0.9, 1.5, 3.2], {'bushTop': add(SHT, [0, 2.5, 0]), 'bushM': add(SHT, [0.3, 1.0, 0.2]), 'heroTop': add(HP12, [0, 2.4, 0]), 'heroHips': add(HP12, [0, 0.9, 0]), 'heroL': add(HP12, [-0.4, 1.4, 0])}, top=0.1, bottom=0.76, margin=0.09, lenses=range(26, 61))
C12 = cam(0.0, [_f12[0], r(_f12[1] - 0.6), _f12[2]], _f12, [_l12[0], r(_l12[1] - 0.55), _l12[2]], _l12, lens=_n12, ease='inOut')   # (round 3) medium two-shot, craning up the bush to its cap
MUG = {'R': R5(off(HP12, HRY12, 0.3, 0.15, 1.3))}
SIP = {'R': R5(off(HP12, HRY12, 0.22, 0.06, 1.78))}
kh12 = [k(0.0, clip='stand'), k(0.0, look=off(HP12, HRY12, 0.4, 0.15, 1.25)), TK(0.0, {**MUG, 'L': R5(off(HP12, HRY12, 0.15, -0.28, 1.0))}, {'R': 'grip', 'L': 'rest'}, {'lid': 0.55, 'mouth': 'line', 'brow': 0.1}, d=0.0),
        TK(0.55, SIP, bend={'neck': SP(-0.15)}, d=0.3, keep=True), TK(0.9, face={'lid': 0.75, 'mouth': 'O', 'brow': 0.1}, d=0.1, keep=True), TK(1.25, MUG, face={'lid': 0.5, 'mouth': 'line', 'brow': 0.1}, bend={'neck': SP(0.0)}, d=0.3, keep=True),   # a sip
        TK(1.45, sq=(1.05, 1.04, 1.05), d=0.3, keep=True), TK(1.85, sq=(0.98, 0.98, 0.98), d=0.35, keep=True), TK(2.3, sq=(1, 1, 1), d=0.3, keep=True),   # (round 3) the chest rises, a breath out
        TK(1.62, face={'lid': 0.4, 'mouth': 'line', 'brow': 0.3, 'gy': -0.8}, d=0.08, keep=True), k(1.8, look=add(SHT, [0, 2.2, 0.15]), lookDur=1.0), TK(2.3, face={'lid': 0.25, 'mouth': 'line', 'brow': 0.5}, d=0.2, keep=True),   # a slow look up at the bush   # the eyes go up first, then the head
        *blink(0.3, {'lid': 0.55, 'mouth': 'line', 'brow': 0.1}), *blink(2.8, {'lid': 0.25, 'mouth': 'line', 'brow': 0.5}), *BREATHE(0.2, D12, 0.5, 0.02)]
st.shot('S12', 'whiteVoid', setOpts={'color': '#C8D4E4'}, look={'sunDir': [0.6, 0.5, 0.7]},
        actors=[act('mecPyj', HP12, HRY12, 'stand', 'neutral', keys=kh12)],
        props=[*GARDEN('S12', lawn=DAWN_LAWN, wall=DAWN_WALL), P('arbre12', 'coMoneyTree', pos=add(CB, [0, 0.35, 0])), P('buisson12', 'coShoot', pos=SHT, ry=20, opts={'stage': 3}), PYJ('pyjama12'),
               P('tasse12', 'coMug', on={'actor': 'mecPyj', 'hand': 'R', 'offset': [0, 0.02, 0.06]}, opts={'steam': True})], cams=[C12])
st.cue('sfx:gulp', 'S12', 0.95, 0.2)

# ================================================================= S13
# 13: close: the painted eyes open; the leafy shell bursts into a puff of leaves and the inspector of line one stands in its place, identical
D13 = st.dur('S13'); OPEN13 = 0.12; BURST13 = 0.42; IRY13 = IRYE
C13 = cam(0.0, off(SHT, IRY13, 2.5, -0.2, 1.8), off(SHT, IRY13, 2.35, -0.19, 1.8), add(SHT, [0, 1.7, 0]), add(SHT, [0, 1.7, 0]), lens=42)
chk('S13', C13, {'top': add(SHT, [0, 2.45, 0]), 'chest': add(SHT, [0, 1.2, 0])})
ki13 = [k(0.0, visible=False), k(BURST13, visible=True), k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(off(SHT, IRY13, 0.3, 0.22, 1.2)), 'L': R5(off(SHT, IRY13, 0.2, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, STERN, d=0.0),
        TK(BURST13, sq=(0.9, 1.12, 0.9), d=0.04, e='out', keep=True), TK(r(BURST13 + 0.12), sq=(1.04, 0.97, 1.04), d=0.06, keep=True), TK(r(BURST13 + 0.24), sq=(1, 1, 1), d=0.08, keep=True), *blink(0.85, STERN)]
st.shot('S13', 'whiteVoid', setOpts={'color': '#C8D4E4'}, look={'sunDir': [0.6, 0.5, 0.7]},
        actors=[act('controleur', SHT, IRY13, 'stand', 'neutral', keys=ki13)],
        props=[*GARDEN('S13', lawn=DAWN_LAWN, wall=DAWN_WALL), P('arbre13', 'coMoneyTree', pos=add(CB, [0, 0.35, 0])), P('buisson13', 'coShoot', pos=SHT, ry=IRY13, opts={'stage': 3, 'openAt': OPEN13, 'burstAt': BURST13}),
               CAP('casquette13', 'controleur'), PUNCH('poincon13')], cams=[C13])
st.cue('sfx:pop', 'S13', OPEN13, 0.2); st.cue('whoosh', 'S13', BURST13, 0.4)

# ================================================================= S14
# 14: « Billet, s'il vous plaît. »: from the hero's eyes: he holds out his mitten to us, the punch raised beside him, lip flaps
D14 = st.dur('S14'); IRY14 = IRYE
C14 = cam(0.0, off(SHT, IRY14, 2.15, 0.05, 1.62), off(SHT, IRY14, 2.0, 0.05, 1.62), off(SHT, IRY14, 0.0, 0.0, 1.7), off(SHT, IRY14, 0.0, 0.0, 1.7), lens=44)
TLK = {**STERN, 'jaw': 0.35}
ki14 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'R': R5(off(SHT, IRY14, 0.3, 0.22, 1.2)), 'L': R5(off(SHT, IRY14, 0.2, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, STERN, d=0.0),
        TK(0.06, {'L': R5(off(SHT, IRY14, 0.62, -0.08, 1.48)), 'R': R5(off(SHT, IRY14, 0.15, 0.32, 1.65))}, {'L': 'open', 'R': 'grip'}, bend={'spine': SP(0.15)}, d=0.18, keep=True),   # the arm out to the lens, the punch up at his side
        *[TK(r(0.05 + 0.17 * j), face=TLK if j % 2 == 0 else STERN, d=0.04, keep=True) for j in range(6)], TK(1.1, face=STERN, d=0.06, keep=True), *blink(1.15, STERN), *BREATHE(0.4, D14, 0.4)]
st.shot('S14', 'whiteVoid', setOpts={'color': '#C8D4E4'}, look={'sunDir': [0.6, 0.5, 0.7]},
        actors=[act('controleur', SHT, IRY14, 'stand', 'neutral', keys=ki14)],
        props=[*GARDEN('S14', lawn=DAWN_LAWN, wall=DAWN_WALL), P('arbre14', 'coMoneyTree', pos=add(CB, [0, 0.35, 0])), CAP('casquette14', 'controleur'), PUNCH('poincon14', snap=[0.9], s=0.85)], cams=[C14])
st.cue('clack', 'S14', 0.9, 0.25)

# ================================================================= S15
# 15: he pats his pyjama pockets twice: empty. His eyes slide to the compost bin, then slowly his head follows, held; a sweat drop pops on his temple and
#    he shrinks a little
D15 = st.dur('S15'); TURN15 = r(st.at('S15', 'L15', 4) - 0.25); DROP15 = r(TURN15 + 1.0)
HP15 = add(CB, [1.05, 0, -0.05]); HRY15 = -30; CAM15 = add(HP15, [-0.35, 1.6, 2.3])   # (round 3) a cheat: he stands just right of the bin, so the look to it is a three-quarter turn
INS15 = add(HP15, [0.58, 0, 0.6]); IRY15 = yaw(INS15, HP15)   # the inspector stays, at the frame's right edge
C15 = fcam(0.0, CAM15, {'top': add(HP15, [0, 2.45, 0]), 'hips': add(HP15, [0, 0.95, 0]), 'heroR': add(HP15, [0.35, 1.5, 0]), 'binT': add(CB, [-0.3, 1.05, 0.3])}, top=0.1, bottom=0.76, push=0.12)
POCK = lambda dy: {'R': R5(off(HP15, HRY15, 0.2, 0.22, 0.95 + dy)), 'L': R5(off(HP15, HRY15, 0.2, -0.22, 0.95 + dy))}   # (round 3) reach, not touch: the hands slap the pockets
kh15 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, face={'lid': 0.2, 'mouth': 'line', 'brow': 0.5}, d=0.0),
        TK(0.08, POCK(0.18), {'R': 'spread', 'L': 'spread'}, d=0.1, keep=True), TK(0.24, POCK(0.0), sq=(1.08, 0.9, 1.08), d=0.06, e='in', keep=True), TK(0.4, POCK(0.18), sq=(1, 1, 1), d=0.1, keep=True), TK(0.56, POCK(0.0), sq=(1.08, 0.9, 1.08), d=0.06, e='in', keep=True),   # PAT, PAT: empty
        TK(0.78, POCK(0.06), sq=(1, 1, 1), face={'lid': 0.2, 'mouth': 'wavy', 'brow': 0.6}, d=0.12, keep=True),
        TK(r(TURN15 - 0.07), face={'lid': 0.15, 'mouth': 'wavy', 'brow': 0.7, 'gx': -0.9}, d=0.05, keep=True),   # the eyes go first, two frames ahead...
        k(TURN15, look=add(CB, [0, 0.9, 0]), lookDur=1.0), TK(r(TURN15 + 0.9), face={'lid': 0.15, 'mouth': 'wavy', 'brow': 0.7, 'gx': -0.5}, d=0.2, keep=True),   # ...then, slowly (1 s), the head
        TK(DROP15, face={'lid': 0.05, 'mouth': 'wavy', 'brow': 0.9, 'gx': -0.9}, sq=(1.1, 0.86, 1.1), d=0.08, e='out', keep=True), TK(r(DROP15 + 0.2), sq=(1.06, 0.9, 1.06), d=0.15, keep=True), *BREATHE(0.9, D15, 0.45, 0.02)]   # the drop pops: he shrinks
ki15 = [k(0.0, clip='stand'), k(0.0, look=HEAD(HP15, 1.9)), TK(0.0, {'R': R5(off(INS15, IRY15, 0.2, 0.3, 1.8)), 'L': R5(off(INS15, IRY15, 0.5, -0.12, 1.35))}, {'R': 'grip', 'L': 'open'}, STERN, d=0.0), *blink(0.7, STERN), *blink(1.8, STERN), *BREATHE(0.3, D15, 0.45)]
st.shot('S15', 'whiteVoid', setOpts={'color': '#C8D4E4'}, look={'sunDir': [0.6, 0.5, 0.7]},
        actors=[act('mecPyj', HP15, HRY15, 'stand', 'neutral', keys=kh15), act('controleur', INS15, IRY15, 'stand', 'neutral', keys=ki15)],
        props=[*GARDEN('S15', lawn=DAWN_LAWN, wall=DAWN_WALL), P('arbre15', 'coMoneyTree', pos=add(CB, [0, 0.35, 0])), PYJ('pyjama15'), CAP('casquette15', 'controleur'), PUNCH('poincon15', s=0.85), DROP('goutte15', 'mecPyj', DROP15, offset=(0.3, 0.22, 0.05))], cams=[C15])
st.cue('sfx:pop', 'S15', DROP15, 0.2)

# ================================================================= S16
# 16: « Amende. »: S01 again: the same two-shot at the same scale and the same timing, the same punch, clack, the same hand-over of a blank pink slip.
#    Cut: three-quarters on him, the compost bin in the frame: the slip, the bin, the slip. Deadpan
D16 = st.dur('S16'); IRY16 = IRYE; PN16 = r(PN1 - CUT1)
HAND16 = off(SHT, IRY16, DHAND, -0.05, 1.3); HP16 = off(SHT, IRY16, DGAP, 0, 0); HRY16 = yaw(HP16, SHT)
CUT16 = r(PN16 + 0.95)
C16 = TWO_CAM(0.0, SHT, IRY16)
SLIPV = off(HP16, -30, 0.4, 0.12, 1.5)
C16b = fcam(CUT16, [-3.3, 1.45, 2.1], {'top': add(HP16, [0, 2.4, 0]), 'feet': add(HP16, [0, 0, 0.2]), 'slip': add(SLIPV, [0, 0.25, 0]), 'binL': add(CB, [-0.5, 1.0, 0.5]), 'binT': add(CB, [0, 1.05, 0])}, top=0.12, bottom=0.75, push=0.1)   # (round 3) three-quarters, whole, the bin beside him
_g = [HP16[0] + 3.3, HP16[2] - 2.1]; _n = math.hypot(*_g); _g = [_g[0] / _n, _g[1] / _n]
INS16b = [r(HP16[0] - 1.0 * -_g[1] - 0.3 * _g[0]), 0, r(HP16[2] - 1.0 * _g[0] - 0.3 * _g[1])]; IRY16b = yaw(INS16b, HP16)   # (round 3) cut 2: he steps to the frame's left edge, hand still out
ki16 = [k(0.0, clip='stand'), k(0.0, look=HEAD(HP16, 1.9)), *INSP_KEYS(PN16, SHT, IRY16, HAND16), *blink(0.6, STERN), *blink(1.5, STERN),
        k(CUT16, to=INS16b, dur=0.01, clip='stand', face='keep'), k(CUT16, face=IRY16b, turn=0.01), k(CUT16, look=HEAD(HP16, 1.9), lookDur=0.0), TK(CUT16, {'L': R5(off(INS16b, IRY16b, 0.62, 0.0, 1.35)), 'R': R5(off(INS16b, IRY16b, 0.2, 0.3, 1.75))}, {'L': 'open', 'R': 'grip'}, STERN, d=0.0, keep=True)]
kh16 = [k(0.0, clip='stand'), k(0.0, look=HEAD(SHT, 2.0)), TK(0.0, HANDS(HP16, HRY16), {'R': 'rest', 'L': 'rest'}, {'lid': 0.15, 'mouth': 'wavy', 'brow': 0.8}, d=0.0),
        TK(r(PN16 + 0.3), {'R': R5(add(HAND16, [0.0, -0.02, 0.0]))}, {'R': 'pinch'}, d=0.2, keep=True), TK(r(PN16 + 0.5), sq=(1.07, 0.88, 1.07), bend={'spine': SP(0.3)}, face=SAD, d=0.12, keep=True), TK(r(PN16 + 0.62), bend={'spine': SP(0.3), 'neck': SP(0.35)}, d=0.15, keep=True),   # the same sag, held
        k(CUT16, face=-30, turn=0.01), TK(CUT16, {'R': R5(SLIPV)}, sq=(1, 1, 1), bend={'spine': SP(0.05)}, face=DEAD, d=0.0, keep=True),
        k(r(CUT16 + 0.05), look=SLIPV, lookDur=0.12), k(r(CUT16 + 0.4), look=add(CB, [0, 0.9, 0]), lookDur=0.15), k(r(CUT16 + 0.75), look=SLIPV, lookDur=0.15),   # slip, compost, slip
        *blink(r(D16 - 0.25), DEAD), *BREATHE(r(CUT16 + 0.1), D16, 0.4, 0.02)]
st.shot('S16', 'whiteVoid', setOpts={'color': '#C8D4E4'}, look={'sunDir': [0.6, 0.5, 0.7]},
        actors=[act('controleur', SHT, IRY16, 'stand', 'neutral', keys=ki16), act('mecPyj', HP16, HRY16, 'stand', 'neutral', keys=kh16)],
        props=[*GARDEN('S16', lawn=DAWN_LAWN, wall=DAWN_WALL), P('arbre16', 'coMoneyTree', pos=add(CB, [0, 0.35, 0])), CAP('casquette16', 'controleur'), PYJ('pyjama16'),
               P('amende16', 'coFine', on={'actor': 'controleur', 'hand': 'L', 'offset': [0.0, 0.12, 0.06], 'face': 'camera'}, opts={'punchAt': PN16}, keys=[k(r(PN16 + 0.52), attach='mecPyj', hand='R', offset=[0.0, 0.12, 0.05], rot=[0, 0, 0])]),
               PUNCH('poincon16', snap=[PN16], s=0.85)], cams=[C16, C16b])
st.cue('clack', 'S16', PN16, 0.5)

for g_ in [('S01', PN1, 'controleur', 'fine'), ('S02', DF2, 'mec', 'compost'), ('S03', JAW3, 'mec', 'tree'), ('S04', 1.0, 'mec', 'bury'), ('S05', 0.85, 'conducteur', 'empty'), ('S06', SW6b, 'guichetier', 'price'),
           ('S07', PEEL7, 'randonneur', 'leaf'), ('S08', CLK8, 'mec', 'punch'), ('S09', FALL9, 'passant', 'krach'), ('S10', CUT10, 'jardinier1', 'fire'), ('S11', SLIDE11, 'guichetier', 'ticket'),
           ('S12', 1.0, 'mecPyj', 'bush'), ('S13', BURST13, 'controleur', 'burst'), ('S14', 0.3, 'controleur', 'billet'), ('S15', DROP15, 'mecPyj', 'drop'), ('S16', PN16, 'controleur', 'fine')]:
    st.gag(*g_)

for _sc in st.scenes:
    for _a in _sc['actors']:
        _run = {'reach': {}, 'hands': {}}
        for _kk in sorted((x for x in _a.get('keys', []) if isinstance(x, dict) and 'toon' in x), key=lambda x: x.get('at', 0)):
            for _n in ('reach', 'hands'):
                if _n in _kk['toon']: _kk['toon'][_n] = {**_run[_n], **_kk['toon'][_n]}; _run[_n] = dict(_kk['toon'][_n])
            for _sd in (_kk['toon'].get('touch') or {}):   # a touch on a side lets go of that side's reach
                _run['reach'].pop(_sd, None); _kk['toon']['reach'] = {x: y for x, y in _run['reach'].items()}
print('\n'.join(CHECKS))

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
GUEST = lambda pr, seed, suit: {'preset': pr, 'seed': seed, 'hat': 'none', 'suit': suit, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
INSP = {'preset': 'cop', 'outfit': 'suit', 'seed': 6101, 'suit': '#1E2A44', 'pants': '#1E2A44', 'shirt': '#C9D6EA', 'lapel': '#18223A', 'tie': '#18223A', 'cuff': '#1E2A44', 'hat': 'none', 'glasses': False, 'toon': EX}
st.write("Le composteur", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'mecPyj': {**MEC, 'preset': 'mecPyjama'}, 'controleur': INSP,
    **{f'voisin{i + 1}': GUEST(['fermier', 'madame', 'tourist'][i], 6110 + i, ['#C86A2A', '#C8322A', '#5E8C4A'][i]) for i in range(3)},
    'conducteur': GUEST('worker', 6120, '#2E5E9E'), 'guichetier': GUEST('madame', 6121, '#5A6E9A'), 'client': GUEST('tourist', 6122, '#D9A23A'),
    'randonneur': GUEST('sportif', 6123, '#5E8C4A'), 'passant': GUEST('politique', 6124, '#6A5440'),
    **{f'jardinier{i + 1}': {'preset': 'worker', 'seed': 6130 + i, 'suit': '#F07A1E', 'pants': '#F07A1E', 'lapel': '#F2C94C', 'cuff': '#F07A1E', 'hat': 'none', 'toon': EX} for i in range(3)},
})
