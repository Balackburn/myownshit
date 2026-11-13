#!/usr/bin/env python3
"""La gomme à mâcher (story 51, cycle 13 of the cartoon staging): this man stepped on a piece of chewing gum three weeks ago. Since then it stretches
behind him. The pink strand crosses the whole of Paris. The town hall listed it as a communal road. On Sundays the children skip with it. The city
hung a cable car on it. Yesterday he wanted to get rid of it: he pulled hard. The strand brought him back home in one second. Since then he works
from home.
Staging: every gag is the strand pulling on his leg: the foot glued to the pavement while he walks on reading his phone (the leg stretched to twice
its length by the new foot IK, `plant`), the snap and the ripple; the strand trailing behind him, a lady hopping over it; a pink line down the street
to the Eiffel tower; a road worker painting white dashes on it and his roller getting stuck; the children turning it as a skipping rope, and at the
other end, on his sofa, his leg whirling round in time while he reads the paper; a cable-car cabin riding it over the roofs, and him hanging upside
down by the foot at his desk, still typing; the grab, the lean, the strand stretching thin and taut, the yank; flying feet first over the roofs
along the strand, deadpan; planted head first in his own sofa like a dart; working from home, the slack strand coiled on the floor, one last jerk
of the foot. Natural look; cycle 13 tools: plant (feet held at points of the world), tether sag keys / wobble / taper / thin / spin, the key-pose
probe (st.gag), the frozen / repeated-take audit."""
from story_kit import *
import math

st = Story('gomme', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 9), ('S03', 'L02', 1), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L05', 7),
         ('S08', 'L06', 0), ('S09', 'L06', 5), ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L09', 0), ('S13', 'L09', 4), ('S14', 'L10', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)

GUM = '#F27BAA'
def STRAND(a, b, frm=None, until=None, sag=0.03, rad=0.02, taper=0.55, thin=None, **o):
    """the pink strand: a scene tether (director3: sag number or keys, wobble, taper, thin, spin)"""
    d = {'a': a, 'b': b, 'color': GUM, 'sag': sag, 'radius': rad, 'taper': taper, **o}
    if thin: d['thin'] = thin
    if frm is not None: d['from'] = frm
    if until is not None: d['until'] = until
    return d
FOOT = lambda who='mec', side='L': {'actor': who, 'joint': 'foot' + side, 'offset': [0, 0.01, 0.07]}   # the middle of the sole (the shoe hangs under the ankle joint)
HAND = lambda who='mec', side='R': {'actor': who, 'hand': side, 'offset': [0, -0.08, 0.02]}
PT = lambda p: {'point': [r(v) for v in p]}
STREET = {'clear': [-80, 80], 'paveW': 6.5}
LR = {'tv': False, 'carpet': False}
SEAT = [0.0, 0, -2.75]
PHONE = lambda pid: P(pid, 'smartPhone', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.03, 0.05], 'face': 'camera'}, scale=2.6, opts={'case': '#F2C94C'})
def PLANT(p, w=1.0, side='L', base=None):
    """a toon state with the foot held at p (weight w), on top of `base`"""
    d = dict(base or {}); d['plant'] = {side: [r(p[0]), r(p[1]), r(p[2]), w]}; return d

# 1: the hook. Low on the pavement: he walks toward us reading his phone and puts his left shoe right on a pink blob of gum (squelch); he walks on:
#    the shoe stays
D1 = st.dur('S01'); TS = round(st.at('S01', 'L01', 6) - 0.06, 3)
BLOB = [7.2, 0, 0.0]; GUMPT = [BLOB[0], 0.03, BLOB[2]]
X1 = 7.08
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [X1, 0, -1.25], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None),
            k(0.0, to=[X1, 0, 0.2], dur=TS, clip='walkRead', then='walkRead', ease='linear', face='move'),
            k(round(TS - 0.07, 3), toon=PLANT(GUMPT, 0.0), toonDur=0.0), k(TS, toon=PLANT(GUMPT, 1.0), toonDur=0.06),   # the shoe comes down on the gum and stays
            k(TS, to=[X1, 0, 0.72], dur=round(D1 - TS + 0.04, 3), clip='walkRead', then='stand', ease='linear', face='keep'),
            k(round(TS + 0.22, 3), look=[GUMPT[0], 0.0, GUMPT[2]]), k(round(TS + 0.45, 3), look=None)])],
        props=[PHONE('phone1'), P('blob1', 'gumBlob', pos=BLOB, opts={'r': 0.2, 'squelch': [[TS, 1.0]]})],
        cams=[FC(0.0, [7.55, 0.2, 1.75], [[GUMPT[0], 0.0, GUMPT[2]], [X1, 2.3, 0.72], [X1, 2.3, -1.25], [r(X1 + 0.5), 1.0, 0.2]], top=0.06, bottom=0.72)])
st.cue('sfx:splat', 'S01', TS, 0.45)

# 2: three weeks ago. From the front, three quarters: he walks on, on his phone; the left foot stays glued: the leg stretches back to the blob, twice
#    its length; it lets go: the leg snaps back with a ripple, a pink strand now runs from his sole to the blob; he does not even look
D2 = st.dur('S02'); SNAP = 1.0
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [X1, 0, 0.72], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=PLANT(GUMPT, 1.0), toonDur=0.0),
            k(0.0, to=[X1, 0, 2.78], dur=round(D2 + 0.03, 3), clip='walkRead', then='stand', ease='linear', face='keep'),
            k(round(SNAP - 0.12, 3), toon=PLANT(GUMPT, 1.0, base={'sq': [0.97, 1.03, 0.97]}), toonDur=0.1),                      # the strain, just before
            k(SNAP, toon={'plant': {'L': [GUMPT[0], GUMPT[1], GUMPT[2], 0.0]}, 'wave': {'legL': [0.16, 1.0, 0.0, 1], 'shinL': [0.16, 1.0, -1.0, 1]}}, toonDur=0.05, toonEase='out'),   # it lets go: the leg snaps
            k(round(SNAP + 0.32, 3), toon={'wave': {'legL': [0.0, 1.0, 2.0, 1], 'shinL': [0.0, 1.0, 1.0, 1]}}, toonDur=0.3),          # the ripple runs down and dies
            k(round(SNAP + 0.12, 3), look=[GUMPT[0], 0.0, GUMPT[2]]), k(round(SNAP + 0.42, 3), look=None)])],                     # a glance down, back to the phone
        props=[PHONE('phone2'), P('blob2', 'gumBlob', pos=BLOB, opts={'r': 0.2, 'pull': [[round(SNAP - 0.02, 3), 0.0], [round(SNAP + 0.08, 3), 1.0]]})],
        tethers=[STRAND(PT(GUMPT), FOOT(), frm=SNAP, sag=0.0, rad=0.026, taper=0.6, thin=[0.8], wobble=[[SNAP, 0.06, 30, 6]])],
        cams=[FC(0.0, [4.4, 1.15, 4.7], [[GUMPT[0], 0.0, GUMPT[2]], [X1, 2.3, 2.75], [X1, 2.3, 1.7], [X1, 0.0, 2.75]], top=0.1, bottom=0.74)])
st.cue('sfx:stretch', 'S02', 0.2, 0.3); st.cue('sfx:boing', 'S02', SNAP, 0.4)

# 3: since then it stretches behind him. From the front, low: he walks toward us on his phone, the pink strand trailing behind him all the way back to
#    the blob; a lady crossing the pavement hops over it, looks down at it, then at him
D3 = st.dur('S03'); HOP3 = 0.55
LADY_A = [5.4, 0, 3.4]; LADY_B = [r(X1 - 0.55), 0, 3.36]; LADY_C = [r(X1 + 0.5), 0, 3.32]; LADY_D = [9.4, 0, 3.25]
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [X1, 0, 5.3], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[X1, 0, 7.25], dur=round(D3 + 0.03, 3), clip='walkRead', then='stand', ease='linear', face='move'),
            k(round(D3 - 0.55, 3), look='camera')]),
        act('dame', LADY_A, 90, 'stand', 'neutral', keys=[k(0.0, look=[GUMPT[0], 0.0, 3.3]),
            k(0.0, to=LADY_B, dur=HOP3, clip='walk', then='stand', ease='linear', face='move'),
            k(HOP3, to=[X1, 0.32, 3.3], dur=0.13, glide=True, ease='out', face='keep'), k(HOP3, toon={'bend': {'legL': [-0.7, 0, 0, 1, None], 'shinL': [1.2, 0, 0, 1, None], 'legR': [-0.3, 0, 0, 1, None], 'shinR': [0.9, 0, 0, 1, None]}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.06),   # the hop over the strand
            k(round(HOP3 + 0.13, 3), to=LADY_C, dur=0.13, glide=True, ease='in', face='keep'), k(round(HOP3 + 0.2, 3), toon={'sq': [1.08, 0.92, 1.08]}, toonDur=0.04), k(round(HOP3 + 0.3, 3), toon={}, toonDur=0.08),
            k(round(HOP3 + 0.26, 3), to=LADY_D, dur=round(D3 - HOP3 - 0.23, 3), clip='walk', then='stand', ease='linear', face='move'),
            k(round(HOP3 + 0.32, 3), look=[X1, 1.9, 6.4])])],
        props=[PHONE('phone3'), P('blob3', 'gumBlob', pos=BLOB, opts={'r': 0.2, 'pull': [[0.0, 1.0]]})],
        tethers=[STRAND(PT(GUMPT), FOOT(), sag=0.0, rad=0.07, taper=0.35, thin=[4.0])],
        cams=[FC(0.0, [4.3, 1.05, 10.4], [[X1, 2.3, 5.3], [X1, 2.3, 7.25], [GUMPT[0], 0.0, GUMPT[2]], [5.6, 1.9, 3.4], [9.4, 1.9, 3.25], [X1, 0.0, 7.25]], top=0.1, bottom=0.74, drift=(0.0, 0.0, 0.25))])

# 4: the pink strand crosses the whole of Paris. High over the street: a pink line down the middle of the avenue to the Eiffel tower; a pluck runs
#    along it
D4 = st.dur('S04')
st.shot('S04', 'parisStreet', setOpts={**STREET, 'clear': [-200, 80]}, actors=[],
        props=[P('blob4', 'gumBlob', pos=[7.2, 0, 26.0], scale=6.0, opts={'r': 0.13})],
        tethers=[STRAND(PT([7.2, 0.4, 26.0]), PT([-6.0, 0.4, -160.0]), sag=0.0, rad=0.32, taper=0.0, n=24, segments=48, wobble=[[0.3, 0.6, 9, 1.6]])],
        cams=[cam(0.0, [-9.0, 26.0, 52.0], [-8.4, 25.4, 49.0], [0.5, 4.0, -40.0], [0.4, 4.2, -42.0], lens=40)])
st.cue('whoosh', 'S04', 0.25, 0.25, 0.8, 300, 900)

# 5: the town hall listed it as a communal road. On the pavement: a road worker walks backwards painting white dashes on the strand with a roller on a
#    pole; behind him a blue street plate VOIRIE COMMUNALE on a post; the roller sticks: he tugs, a pink thread stretches from it and snaps; he looks at us
D5 = st.dur('S05'); CARD5 = round(st.at('S05', 'L04', 4) - 0.05, 3); STK5 = 1.45
SX5 = 6.4; W5A = [6.95, 0, 1.9]; W5B = [6.95, 0, -0.35]; WALK5 = 1.35
POLE5 = 1.45; TIL5 = 2.26                                           # the pole: from the hands (prop origin) down and forward (+Z) to the roller on the strand
def HANDLE5(t):                                                     # where his hands hold the pole at t (he walks backwards toward -Z, facing +Z)
    u = min(1.0, max(0.0, t / WALK5)); return [r(SX5 + 0.12), 1.05, r(W5A[2] + 0.32 + (W5B[2] - W5A[2]) * u)]
HEAD5 = lambda t, a=TIL5: [SX5, r(HANDLE5(t)[1] + POLE5 * math.cos(a)), r(HANDLE5(t)[2] + POLE5 * math.sin(a))]
DASHES = [(z, r(max(0.05, (W5A[2] + 0.32 + POLE5 * math.sin(TIL5) - z) / (W5A[2] - W5B[2]) * WALK5))) for z in (3.0, 2.6, 2.2, 1.8, 1.4)]
def GRIP5(t, a=TIL5, extra=None):
    h = HANDLE5(t); d = {'reach': {'R': [h[0], h[1], h[2], 1, 0.05], 'L': [h[0], r(h[1] + 0.25 * math.cos(a)), r(h[2] + 0.25 * math.sin(a)), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}}
    d.update(extra or {}); return d
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('ouvrier', W5A, 0, 'stand', 'neutral', keys=[k(0.0, look=[SX5, 0.0, 2.6]),
            k(0.0, to=W5B, dur=WALK5, clip='walk', then='stand', ease='linear', face='keep', back=True),                        # backwards, painting
            *[k(round(t_, 3), toon=GRIP5(t_), toonDur=0.15, toonEase='linear') for t_ in (0.0, 0.3, 0.6, 0.9, 1.2, WALK5)],
            k(STK5, toon=GRIP5(WALK5, 1.95, {'sq': [0.97, 1.04, 0.97]}), toonDur=0.08),                                      # he lifts: it sticks
            k(round(STK5 + 0.18, 3), toon=GRIP5(WALK5, 2.1), toonDur=0.08),
            k(round(STK5 + 0.3, 3), toon=GRIP5(WALK5, 1.8, {'sq': [0.95, 1.06, 0.95]}), toonDur=0.07),                        # a harder tug: it snaps
            k(round(STK5 + 0.42, 3), toon=GRIP5(WALK5, 2.0), toonDur=0.12, settle=0.6),
            k(round(STK5 + 0.5, 3), look='camera')])],
        props=[P('roller5', 'paintRoller', pos=HANDLE5(0.0), rot=[TIL5, 0, 0], opts={'len': POLE5, 'rollerW': 0.22, 'rollerR': 0.065, 'color': '#F4F2EA', 'sleeve': '#F4F2EA'},
                 keys=[k(0.0, to=HANDLE5(WALK5), dur=WALK5, ease='linear'), k(STK5, rotTo=[1.95, 0, 0], dur=0.08), k(round(STK5 + 0.18, 3), rotTo=[2.1, 0, 0], dur=0.08),
                       k(round(STK5 + 0.3, 3), rotTo=[1.8, 0, 0], dur=0.07), k(round(STK5 + 0.42, 3), rotTo=[2.0, 0, 0], dur=0.12)]),
               P('plaque5', 'streetPlaque', pos=[8.6, 0, -1.1], ry=-25, opts={'lines': ['VOIRIE', 'COMMUNALE'], 'post': 2.45, 'w': 0.95, 'h': 0.5, 'screw': [[round(STK5 + 0.36, 3), 0.05]]}),
               *[P(f'dash5{i}', 'paperSheet', pos=[SX5, 0.1, z], rot=[round(-PI / 2, 4), 0, 0], opts={'w': 0.08, 'h': 0.3, 'paper': '#FFFFFF', 'bright': True}, keys=[k(0.0, visible=False), k(t_, visible=True)]) for i, (z, t_) in enumerate(DASHES)]],
        tethers=[STRAND(PT([SX5, 0.04, -9.0]), PT([SX5, 0.04, 9.0]), sag=0.0, rad=0.05, taper=0.0, n=12),
                 STRAND(PT([SX5, 0.07, r(HEAD5(WALK5)[2])]), {'prop': 'roller5', 'offset': [0, round(POLE5 - 0.04, 3), 0.03]}, frm=round(STK5 - 0.02, 3), until=round(STK5 + 0.33, 3), sag=0.0, rad=0.016, taper=0.7)],
        cams=[FC(0.0, [4.0, 1.3, 4.6], [[6.95, 2.25, 1.9], [6.95, 2.25, -0.35], [8.6, 2.5, -1.1], [8.6, 1.95, -1.1], [SX5, 0.0, 3.0], [SX5, 0.0, -1.0]], top=0.22, bottom=0.74)])   # (probe) his head below the title card band (29 % of it under VOIRIE COMMUNALE)
st.card('S05', 'VOIRIE COMMUNALE', at=CARD5)
st.cue('sfx:scratch', 'S05', 0.15, 0.25); st.cue('sfx:stretch', 'S05', STK5, 0.3); st.cue('sfx:twang', 'S05', round(STK5 + 0.32, 3), 0.3)

# 6: on Sundays the children skip with it. On the pavement, two children turn the strand like a skipping rope, a third jumps it, in time
D6 = st.dur('S06'); FQ = 1.5; ZA, ZB, XK = -22.0, -18.4, 6.6; ZC = round((ZA + ZB) / 2, 3)
def CIRC(t0, t1, c, rr, f, ph=0.0, n=12, w=1.0, tip=0.05):
    """reach keys that turn a hand round a small circle in the plane y-x at c (a skipping rope's handle)"""
    out, i = [], 0
    while True:
        t = round(t0 + i / (n * f), 3)
        if t > t1: break
        a = 2 * PI * (f * t + ph); out.append((t, [r(c[0] + rr * math.sin(a)), r(c[1] - rr * math.cos(a)), r(c[2]), w, tip])); i += 1
    return out
def TURN(side, c, ph):
    return [k(t, toon={'reach': {side: p}, 'hands': {side: 'grip'}}, toonDur=round(1 / (12 * FQ), 3), toonEase='linear') for t, p in CIRC(0.0, D6, c, 0.13, FQ, ph)]
HOPS6 = [round(n / FQ, 3) for n in range(0, 4) if n / FQ < D6]
def JUMPS(base):
    ks = []
    for th in HOPS6:
        a = max(0.0, round(th - 0.13, 3)); ks += [k(a, to=[base[0], 0.26, base[2]], dur=0.12, glide=True, ease='out', face='keep'), k(round(a + 0.12, 3), to=list(base), dur=0.12, glide=True, ease='in', face='keep'),
                                                  k(round(a + 0.24, 3), toon={'sq': [1.1, 0.88, 1.1], 'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.03), k(round(a + 0.3, 3), toon={'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.06)]
    return ks
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('enfant1', [XK, 0, ZA], 0, 'stand', 'happy', keys=[k(0.0, look=[XK, 0.9, ZC]), *TURN('R', [XK - 0.05, 0.85, ZA + 0.32], 0.0)]),
        act('enfant2', [XK, 0, ZB], 180, 'stand', 'happy', keys=[k(0.0, look=[XK, 0.9, ZC]), *TURN('L', [XK + 0.05, 0.85, ZB - 0.32], 0.0)]),
        act('enfant3', [XK, 0, ZC], -90, 'stand', 'happy', keys=[k(0.0, look='camera'), *JUMPS([XK, 0, ZC])])],
        tethers=[STRAND(HAND('enfant1', 'R'), HAND('enfant2', 'L'), sag=0.24, rad=0.028, taper=0.2, spin=[FQ, 0.0]),
                 STRAND(PT([XK, 0.3, -70.0]), HAND('enfant1', 'R'), sag=0.004, rad=0.026, taper=0.0),
                 STRAND(HAND('enfant2', 'L'), PT([XK, 0.3, 40.0]), sag=0.004, rad=0.026, taper=0.0)],
        cams=[FC(0.0, [1.1, 1.35, -13.2], [[XK, 1.45, ZA], [XK, 1.45, ZB], [XK, 0.0, ZC], [XK, 1.85, ZC], [XK, 0.0, ZA], [XK, 0.0, ZB], [XK, 1.1, r(ZB + 0.45)], [XK, 1.1, r(ZA - 0.45)]], top=0.12, bottom=0.74)])
st.cue('sfx:whoosh', 'S06', 0.0, 0.2)

# 7: at the other end, on his sofa, reading the paper, deadpan: his left leg whirls round in time with the rope, the strand going out of the window
D7 = st.dur('S07'); C7 = [r(SEAT[0] + 0.2), 0.78, r(SEAT[2] + 0.7)]; WIN7 = [3.55, 1.45, -3.45]
def WHIRL(t0, t1, f, rr=0.42, ph=0.25):
    out, i = [], 0
    while True:
        t = round(t0 + i / (12 * f), 3)
        if t > t1: break
        a = 2 * PI * (f * t + ph); p = [C7[0], r(C7[1] - rr * math.cos(a)), r(C7[2] + rr * math.sin(a))]
        out.append(k(t, toon={**PAPER7, 'plant': {'L': [*p, 1.0]}, 'sq': [1.0, r(1.0 - 0.025 * math.cos(a)), 1.0]}, toonDur=round(1 / (12 * f), 3), toonEase='linear')); i += 1
    return out
PAPER7 = {'reach': {'L': [r(SEAT[0] - 0.25), 1.3, r(SEAT[2] + 0.5), 1, 0.05], 'R': [r(SEAT[0] + 0.25), 1.3, r(SEAT[2] + 0.5), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}
st.shot('S07', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look=[SEAT[0], 1.35, r(SEAT[2] + 0.45)]), *WHIRL(0.0, D7, FQ), k(round(D7 - 0.5, 3), look='camera')])],
        props=[P('paper7', 'newspaper', pos=[SEAT[0], 1.08, r(SEAT[2] + 0.45)], rot=[1.3, 0, 0], scale=1.55, opts={'headline': 'DIMANCHE'})],
        tethers=[STRAND(FOOT(), PT(WIN7), sag=0.16, rad=0.026, taper=0.25, spin=[FQ, 0.25])],
        cams=[FC(0.0, [1.0, 1.2, 0.3], [[SEAT[0], 1.9, SEAT[2]], [C7[0], 0.3, C7[2]], [C7[0], 1.25, C7[2]], [r(SEAT[0] - 0.5), 1.0, SEAT[2]], [1.2, 1.1, -2.5]], top=0.1, bottom=0.74)])
st.cue('sfx:whoosh', 'S07', 0.1, 0.2)

# 8: the city hung a cable car on it. From a roof: a red cabin with three riders rides along the pink strand over the street, swinging, the strand
#    dipping under it; the Eiffel tower behind
D8 = st.dur('S08'); Y8, Z8 = 15.5, -12.0
st.shot('S08', 'parisStreet', setOpts={**STREET, 'clear': [-200, 80]}, actors=[],
        props=[P('cab8', 'cableCar', pos=[-4.6, round(Y8 - 0.55, 3), Z8], opts={'riders': 3, 'swing': [[0.0, 0.07]], 'tilt': -0.04}, keys=[k(0.0, to=[2.2, round(Y8 - 0.55, 3), Z8], dur=D8, ease='linear')])],
        tethers=[STRAND(PT([-45.0, Y8, Z8]), {'prop': 'cab8', 'offset': [0, 0.06, 0]}, sag=0.008, rad=0.07, taper=0.0, n=14),
                 STRAND({'prop': 'cab8', 'offset': [0, 0.06, 0]}, PT([45.0, Y8, Z8]), sag=0.008, rad=0.07, taper=0.0, n=14)],
        cams=[cam(0.0, [-3.6, 14.4, -4.2], [0.2, 14.4, -4.2], [-4.4, 13.9, -12.0], [1.9, 13.9, -12.0], lens=44)])
st.cue('sfx:rotor', 'S08', 0.0, 0.25)

# 9: ... and him at his desk, hanging upside down by the foot from the strand that comes in by the window, swinging gently, still typing, deadpan
D9 = st.dur('S09'); ME9 = [-1.75, 3.3, -2.3]
HANG = {'lay': [0, round(PI, 4)], 'bend': {'legR': [0.55, 0, 0, 1, None], 'shinR': [-1.5, 0, 0, 1, None]}}
TYPE9 = lambda dx: {'reach': {'L': [r(-1.75 - 0.12 + dx), 0.83, -1.78, 1, 0.08], 'R': [r(-1.75 + 0.12 - dx), 0.83, -1.78, 1, 0.08]}, 'hands': {'L': 'flat', 'R': 'flat'}, 'hose': 0.1}
st.shot('S09', 'office', setOpts={'door': False}, actors=[
        act('mec', ME9, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            *[k(round(i * 0.12, 3), toon={**HANG, 'lay': [0, round(PI + 0.07 * math.sin(i * 0.12 * 2 * PI * 0.9), 4)], **TYPE9(0.03 * (i % 2))}, toonDur=0.12, toonEase='linear') for i in range(int(D9 / 0.12) + 1)]])],
        props=[P('desk9', 'desk', pos=[-1.75, 0, -1.55], ry=180, opts={'w': 1.2, 'd': 0.6}), P('laptop9', 'laptop', pos=[-1.75, 0.76, -1.72], ry=180, opts={'text': 'RAPPORT'})],
        tethers=[STRAND(FOOT(), PT([-1.75, 9.5, -2.3]), sag=0.0, rad=0.026, taper=0.2)],
        cams=[FC(0.0, [-1.2, 1.5, 0.4], [[-1.75, 2.75, -2.3], [-1.75, 1.05, -2.3], [-1.75, 0.74, -1.45], [-2.2, 1.6, -2.3], [-1.3, 1.6, -2.3]], top=0.04, bottom=0.74)])   # (s3) on his face and the laptop, the legs going up out of the frame
st.cue('sfx:squeak', 'S09', 0.1, 0.25); st.cue('sfx:click', 'S09', 0.0, 0.25)

# 10: yesterday he wanted to get rid of it. On the pavement, the strand running from his shoe back toward home: he looks down, bends, grabs it with
#     both hands, stands up with it, plants his feet wide, takes a deep breath
D10 = st.dur('S10'); X10, Z10 = 7.1, 40.0; GRAB = 0.55; UP10 = 1.0
FAR = PT([7.2, 0.05, 0.0])
def HOLD10(lift=0.95, fwd=0.4, extra=None):
    d = {'reach': {'L': [r(X10 - 0.08), lift, r(Z10 - fwd + 0.05), 1, 0.05], 'R': [r(X10 + 0.06), r(lift - 0.04), r(Z10 - fwd - 0.12), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}
    d.update(extra or {}); return d
st.shot('S10', 'parisStreet', setOpts={**STREET, 'clear': [-80, 120]}, actors=[
        act('mec', [X10, 0, Z10], 180, 'stand', 'unimpressed', keys=[k(0.0, look=[X10, 0.0, r(Z10 - 0.6)]),
            k(round(GRAB - 0.27, 3), to=[X10, -0.42, Z10], dur=0.24, glide=True, ease='out', face='keep'),
            k(round(GRAB - 0.25, 3), toon={'plant': {'L': [r(X10 - 0.12), 0.0, r(Z10 + 0.04), 1.0], 'R': [r(X10 + 0.12), 0.0, r(Z10 - 0.04), 1.0]}, 'bend': {'spine': [0.45, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'reach': {'L': [r(X10 - 0.05), 0.12, r(Z10 - 0.5), 1, 0.05], 'R': [r(X10 + 0.06), 0.12, r(Z10 - 0.65), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.25),   # crouches and grabs
            k(GRAB, toon={'plant': {'L': [r(X10 - 0.12), 0.0, r(Z10 + 0.04), 1.0], 'R': [r(X10 + 0.12), 0.0, r(Z10 - 0.04), 1.0]}, 'bend': {'spine': [0.45, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'reach': {'L': [r(X10 - 0.05), 0.1, r(Z10 - 0.5), 1, 0.05], 'R': [r(X10 + 0.06), 0.1, r(Z10 - 0.65), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}, toonDur=0.08),
            k(round(UP10 - 0.3, 3), to=[X10, 0, Z10], dur=0.3, glide=True, ease='inOut', face='keep'),
            k(UP10, toon=HOLD10(), toonDur=0.3, toonEase='outBack'), k(round(UP10 + 0.1, 3), look=[X10, 1.0, r(Z10 - 8)]),
            k(round(UP10 + 0.45, 3), to=[r(X10 + 0.04), 0, r(Z10 + 0.15)], dur=0.2, glide=True, face='keep'),
            k(round(UP10 + 0.45, 3), toon=HOLD10(extra={'bend': {'legL': [0, 0.28, 0, 1, None], 'legR': [0, -0.28, 0, 1, None]}, 'sq': [1.0, 0.96, 1.0]}), toonDur=0.15),   # feet wide
            k(round(UP10 + 0.7, 3), toon=HOLD10(extra={'bend': {'legL': [0, 0.28, 0, 1, None], 'legR': [0, -0.28, 0, 1, None]}, 'sq': [1.08, 1.05, 1.12], 'face': {'puff': 0.8, 'brow': -0.7, 'lid': 0.25}}), toonDur=0.3, toonEase='in'),   # the big breath
            k(round(UP10 + 0.75, 3), look='camera')])],
        tethers=[STRAND(FOOT(), HAND('mec', 'L'), frm=round(GRAB + 0.02, 3), sag=0.25, rad=0.024, taper=0.3),
                 STRAND(HAND('mec', 'R'), FAR, frm=round(GRAB + 0.02, 3), sag=0.0, rad=0.026, taper=0.0, thin=[2.0], n=14),
                 STRAND(FOOT(), FAR, until=round(GRAB + 0.02, 3), sag=0.0, rad=0.026, taper=0.0, n=14)],
        cams=[FC(0.0, [4.4, 1.3, 36.6], [[X10, 2.3, Z10], [X10, 0.0, Z10], [r(X10 - 0.4), 1.0, r(Z10 - 1.0)], [r(X10 + 0.5), 1.2, Z10]], top=0.12, bottom=0.74)])
st.cue('sfx:stretch', 'S10', UP10, 0.25); st.cue('sfx:sniff', 'S10', round(UP10 + 0.7, 3), 0.3)

# 11: he pulled hard. From the side: he leans right back, arms out along the strand, which goes thin and taut and hums; he trembles; held; then the
#     strand wins: his arms shoot out after it, his feet leave the ground, and he is gone out of the frame
D11 = st.dur('S11'); YANK = 1.12; GONE = round(YANK + 0.18, 3)
def PULL(lean, fwd, extra=None):
    d = {'lay': [round(-lean, 3), 0], 'reach': {'L': [r(X10 - 0.06), 1.0, r(Z10 - fwd), 1, 0.05], 'R': [r(X10 + 0.06), 0.97, r(Z10 - fwd - 0.14), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'},
         'bend': {'legL': [-0.25, 0.22, 0, 1, None], 'legR': [-0.25, -0.22, 0, 1, None], 'shinL': [0.45, 0, 0, 1, None], 'shinR': [0.45, 0, 0, 1, None]},
         'plant': {'L': [r(X10 + 0.18), 0.0, r(Z10 - 0.35), 1.0], 'R': [r(X10 - 0.16), 0.0, r(Z10 - 0.3), 1.0]}, 'face': {'puff': 0.9, 'brow': -0.9, 'lid': 0.3, 'mouth': 'flat'}}
    if extra: d.update(extra)
    return d
st.shot('S11', 'parisStreet', setOpts={**STREET, 'clear': [-80, 120]}, actors=[
        act('mec', [X10, 0, r(Z10 + 0.15)], 180, 'stand', 'unimpressed', keys=[k(0.0, look=[X10, 1.0, r(Z10 - 8)]),
            k(0.0, toon=PULL(0.15, 0.45), toonDur=0.0), k(0.35, toon=PULL(0.42, 0.55), toonDur=0.3, toonEase='out'),
            *[k(round(0.65 + 0.05 * i, 3), toon=PULL(0.45 + 0.012 * (i % 2), 0.56, {'sq': [1.0, r(1.0 + 0.012 * (i % 2)), 1.0]}), toonDur=0.04) for i in range(9)],   # held, trembling
            k(round(YANK - 0.04, 3), toon=PULL(0.5, 0.6, {'face': {'puff': 0.2, 'brow': 0.9, 'pop': 0.0, 'lid': 0.0, 'mouth': 'O', 'jaw': 0.4}}), toonDur=0.04),   # it is going: the eyes open wide
            k(YANK, toon={'lay': [0.9, 0], 'reach': {'L': [r(X10 - 0.05), 1.0, r(Z10 - 2.4), 1, 0.05], 'R': [r(X10 + 0.05), 0.98, r(Z10 - 2.5), 1, 0.05]}, 'hose': 0.12, 'hands': {'L': 'grip', 'R': 'grip'},
                          'face': {'brow': 0.9, 'mouth': 'O', 'jaw': 0.5, 'lid': 0.0}, 'hairUp': 0.8}, toonDur=0.05, toonEase='out'),   # yanked: arms out, tipped forward
            k(YANK, to=[X10, 0.45, r(Z10 - 0.6)], dur=0.12, glide=True, ease='in', face='keep'),
            k(round(YANK + 0.12, 3), to=[X10, 0.9, r(Z10 - 26.0)], dur=0.12, glide=True, ease='in', face='keep')])],                    # gone
        props=[P('dust11', 'dustPuff', pos=[X10, 0.1, Z10], scale=0.7, opts={'once': True, 'startAt': YANK, 'period': 0.5, 'color': '#E8DCC6'}, keys=[k(0.0, visible=False), k(YANK, visible=True)])],
        tethers=[STRAND(FOOT(), HAND('mec', 'L'), until=YANK, sag=0.25, rad=0.022, taper=0.3),
                 STRAND(HAND('mec', 'R'), FAR, sag=[[0.0, 0.004], [0.4, 0.0]], rad=0.03, taper=0.0, thin=[1.2], n=14, wobble=[[0.65, 0.025, 60, 0.8]]),
                 STRAND(FOOT(), FAR, frm=YANK, sag=0.0, rad=0.03, taper=0.0, n=14)],
        cams=[FC(0.0, [3.9, 1.25, 38.3], [[X10, 2.3, r(Z10 + 0.15)], [X10, 0.0, r(Z10 + 0.15)], [X10, 1.0, r(Z10 - 1.5)], [X10, 2.05, r(Z10 + 1.15)], [X10, 1.4, r(Z10 + 1.35)], [r(X10 + 0.35), 2.1, r(Z10 + 1.3)]], top=0.12, bottom=0.74)])
st.cue('sfx:stretch', 'S11', 0.3, 0.35); st.cue('sfx:boing', 'S11', YANK, 0.45); st.cue('whoosh', 'S11', round(YANK + 0.08, 3), 0.4, 0.3, 500, 3200)

# 12: brought him home in one second. Alongside him over the roofs: he flies feet first along the pink strand, stretched by the speed, tie and hair
#     streaming, deadpan; the roofs race past under him
D12 = st.dur('S12'); Y12, Z12 = 17.0, -30.0
st.shot('S12', 'parisStreet', setOpts={**STREET, 'clear': [-200, 80]}, actors=[
        act('mec', [16.0, Y12, Z12], 0, 'stand', 'unimpressed', smear=0.6, keys=[k(0.0, look='camera'), k(0.0, toon={'lay': [0, round(-PI / 2, 4)], 'hairUp': 1.0, 'face': {'lid': 0.35}, 'bend': {'armL': [0, 0.6, 0, 1, None], 'armR': [0, -0.6, 0, 1, None]}}, toonDur=0.0),
            k(0.0, to=[-16.0, Y12, Z12], dur=D12, glide=True, ease='linear', face='keep')])],
        tethers=[STRAND(FOOT(), PT([-80.0, Y12, Z12]), sag=0.0, rad=0.04, taper=0.0, n=8)],
        cams=[cam(0.0, [17.0, round(Y12 + 0.7, 3), round(Z12 + 7.4, 3)], [-15.0, round(Y12 + 0.7, 3), round(Z12 + 7.4, 3)], [17.0, round(Y12 - 0.1, 3), Z12], [-15.0, round(Y12 - 0.1, 3), Z12], lens=46)])
st.cue('whoosh', 'S12', 0.0, 0.45, 0.85, 400, 3000)

# 13: home. His living room: he falls in from above, upside down, feet first along the strand, and plants himself head first in his own sofa like a dart;
#     the cushions bounce, dust; his legs stick up, quiver, flop
D13 = st.dur('S13'); HIT13 = 0.42
DART = {'lay': [0, round(PI, 4)], 'bend': {'armL': [0, 1.2, 0, 1, None], 'armR': [0, -1.2, 0, 1, None]}}
st.shot('S13', 'livingRoom', setOpts=LR, actors=[
        act('mec', [0.05, 6.4, -2.88], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**DART, 'face': {'lid': 0.35}}, toonDur=0.0),
            k(0.0, to=[0.05, 2.5, -2.88], dur=HIT13, glide=True, ease='in', face='keep'),
            k(HIT13, toon={**DART, 'sq': [1.18, 0.78, 1.18]}, toonDur=0.03, toonEase='out'),                                                          # the impact
            k(round(HIT13 + 0.08, 3), toon={**DART, 'sq': [0.94, 1.08, 0.94], 'wave': {'legL': [0.1, 1.0, 0.0, 1], 'legR': [0.1, 1.0, 0.5, 1]}}, toonDur=0.05),   # quivering
            k(round(HIT13 + 0.45, 3), toon={**DART, 'wave': {'legL': [0.0, 1.0, 2.0, 1], 'legR': [0.0, 1.0, 2.5, 1]}}, toonDur=0.3),
            k(round(HIT13 + 0.75, 3), toon={**DART, 'bend': {**DART['bend'], 'legL': [0.0, 0.5, 0, 1, None], 'legR': [0.0, -0.5, 0, 1, None], 'shinL': [0.9, 0, 0, 1, None], 'shinR': [0.9, 0, 0, 1, None]}}, toonDur=0.2, toonEase='in')])],   # they flop
        props=[P('dust13', 'dustPuff', pos=[0.05, 0.55, -2.6], scale=0.8, opts={'once': True, 'startAt': HIT13, 'period': 0.6, 'color': '#F2EAD8'}, keys=[k(0.0, visible=False), k(HIT13, visible=True)])],
        tethers=[STRAND(FOOT(), PT([0.3, 9.0, -2.6]), sag=0.0, rad=0.026, taper=0.2, until=round(HIT13 + 0.1, 3))],
        fx=[{'type': 'shake', 'at': HIT13, 'dur': 0.16, 'amount': 0.012}],
        cams=[FC(0.0, [0.45, 1.45, 1.0], [[0.05, 2.45, -2.88], [-1.25, 0.4, -2.75], [1.25, 0.4, -2.75], [0.05, 3.5, -2.88]], top=0.08, bottom=0.74)])
st.cue('whoosh', 'S13', 0.0, 0.35, 0.4, 600, 2400); st.cue('thud', 'S13', HIT13, 0.5)

# 14: since then he works from home. On his sofa, deadpan, the laptop on his knees, typing; the slack strand coiled on the floor from his shoe to the
#     window; a last jerk of the foot (the children again); he does not even look; a slow blink
D14 = st.dur('S14'); JERK = round(D14 - 1.05, 3)
LAP14 = {'reach': {'L': [-0.12, 0.72, -2.25, 1, 0.08], 'R': [0.12, 0.72, -2.25, 1, 0.08]}, 'hands': {'L': 'flat', 'R': 'flat'}}
COIL = [[0.4, 0.02, -1.6], [-0.35, 0.02, -1.0], [0.6, 0.02, -0.7], [1.6, 0.02, -1.4], [2.6, 0.02, -1.0], [3.4, 0.9, -3.3]]
st.shot('S14', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look=[0.0, 0.75, -2.2]), k(0.0, toon=LAP14, toonDur=0.0),
            *[k(round(0.2 + 0.11 * i, 3), toon={**LAP14, 'reach': {'L': [r(-0.12 + 0.02 * (i % 2)), r(0.72 + 0.012 * (i % 2)), -2.25, 1, 0.08], 'R': [r(0.12 - 0.02 * ((i + 1) % 2)), r(0.72 + 0.012 * ((i + 1) % 2)), -2.25, 1, 0.08]}}, toonDur=0.06) for i in range(int((JERK - 0.3) / 0.11))],   # typing
            k(JERK, toon={**LAP14, 'plant': {'L': [0.35, 0.95, -1.75, 1.0]}}, toonDur=0.05, toonEase='out'), k(round(JERK + 0.12, 3), toon={**LAP14, 'plant': {'L': [0.35, 0.95, -1.75, 0.0]}}, toonDur=0.12, toonEase='in'),   # the jerk of the foot
            k(round(D14 - 0.72, 3), look='camera'), k(round(D14 - 0.55, 3), toon={**LAP14, 'face': {'lid': 1}}, toonDur=0.14), k(round(D14 - 0.33, 3), toon=LAP14, toonDur=0.16)])],   # a slow blink at us
        props=[P('lap14', 'laptop', pos=[0.0, 0.6, -2.22], ry=180, scale=1.6, opts={'text': 'VISIO'})],
        tethers=[STRAND(FOOT(), PT(COIL[0]), sag=0.0, rad=0.024, taper=0.0), *[STRAND(PT(COIL[i]), PT(COIL[i + 1]), sag=0.0, rad=0.024, taper=0.0) for i in range(len(COIL) - 1)]],
        cams=[FC(0.0, [0.5, 1.1, 0.2], [[SEAT[0], 1.9, SEAT[2]], [0.4, 0.0, -1.6], [-0.35, 0.0, -1.3], [r(SEAT[0] - 0.55), 1.0, SEAT[2]], [r(SEAT[0] + 0.55), 1.0, SEAT[2]]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.08))])   # (s3) closer: him, the laptop, the first loops of strand
st.cue('sfx:click', 'S14', 0.2, 0.25); st.cue('sfx:boing', 'S14', JERK, 0.25)

# (cycle 13) the key poses, measured in the engine by render3 --probe
for g_ in [('S01', round(TS + 0.1, 3), 'mec', 'step'), ('S02', round(SNAP - 0.05, 3), 'mec', 'leg_stretch'), ('S03', HOP3, 'dame', 'hop'),
           ('S05', round(STK5 + 0.3, 3), 'ouvrier', 'stuck_roller'), ('S06', 0.05, 'enfant3', 'skip'), ('S07', 0.6, 'mec', 'leg_whirl'),
           ('S09', 0.5, 'mec', 'hanging'), ('S10', round(UP10 + 0.8, 3), 'mec', 'breath'), ('S11', 0.9, 'mec', 'pull'), ('S11', round(YANK + 0.03, 3), 'mec', 'yank'),
           ('S12', round(D12 / 2, 3), 'mec', 'flight'), ('S14', round(D14 - 0.5, 3), 'mec', 'blink')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])

st.write("La gomme à mâcher", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'shoes': True, 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'dame': {'preset': 'madame', 'seed': 511, 'suit': '#7A4E8C', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'ouvrier': {'preset': 'worker', 'seed': 512, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'enfant1': {'preset': 'gamin', 'seed': 513},
    'enfant2': {'preset': 'gamin', 'seed': 514},
    'enfant3': {'preset': 'gamin', 'seed': 515},
})
