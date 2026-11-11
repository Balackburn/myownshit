#!/usr/bin/env python3
"""L'ombre (story 42, cycle 6 of the cartoon staging): this man had a shadow that ran late. By a second, then by an hour. One morning she did not come.
He reported her missing at the town hall. He was told: "She is of age." She already worked elsewhere. For a taller guy. He hired one. Too small. He
was fined for walking without a shadow. Yesterday she came back. With a lawyer. The judge ordered shared custody. On even days, she is the one who
gets up. He follows. On the ground. He says tarmac is fine. Cobbles, less so.
Cartoon rig, cycle 6: a shadow is an actor (cast `silhouette`: one flat unlit colour, white eyes), flattened with `sq` and laid down with `lay`; the
hero casts no shadow of his own (`castShadow: False`); `tremble`, `pupilShake`, `gulp`; the tie obeys gravity upside down (`clothGravity`). Natural look."""
from story_kit import *
import math

st = Story('ombre', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 7), ('S03', 'L01', 9), ('S04', 'L02', 0), ('S05', 'L02', 2), ('S06', 'L03', 0), ('S07', 'L03', 5), ('S08', 'L04', 0),
         ('S09', 'L05', 0), ('S10', 'L06', 0), ('S11', 'L06', 4), ('S12', 'L07', 0), ('S13', 'L07', 5), ('S14', 'L08', 0), ('S15', 'L08', 5), ('S16', 'L09', 0),
         ('S17', 'L09', 4), ('S18', 'L10', 0), ('S19', 'L10', 4), ('S20', 'L11', 0), ('S21', 'L11', 3), ('S22', 'L12', 0), ('S23', 'L12', 3), ('S24', 'L13', 0),
         ('S25', 'L13', 7), ('S26', 28.9, 0)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}
r3 = lambda v: [round(x, 3) for x in v]
INK = '#262833'
FLATX, FLATZ, THIN = [0.03, 1, 1], [1, 1, 0.03], 0.03   # a shadow on a wall he walks along (flattened across his shoulders); one that faces out of its wall, or lies on the ground

# ---- the street: the right-hand pavement (x 5..10) of the Paris street, a sunny blank wall along it (its face at x = WX, toward the road). The sun comes
#      from the road side, a little from down the street: shadows fall on the wall, a little behind whoever walks toward -Z
STREET = {'clear': [-80, 80], 'eiffel': False}
WX = 9.6; HX = 8.85; SX = round(WX - 0.03, 3)        # the wall; his line along it; the plane of his shadow on it
SUN = {'sunDir': [-0.8, 0.5, -0.3], 'fill': 1.25}
LAG = 0.55                                           # how far behind him (toward +Z) his shadow stands on the wall when all is well
WALL = lambda zc=0.0, w=16.0, **kw: P('wall', 'plainWall', pos=[WX, 0, zc], ry=-90, opts={'w': w, 'h': 3.4, **kw})
VW = 1.5                                             # a walk, m/s
def wallcam(t, z0, z1, d=5.3, h=1.45, lh=1.3, lens=44, **kw):   # a camera on the road side looking square at the wall, from z0 to z1
    return cam(t, [round(WX - d, 3), h, z0], [round(WX - d, 3), h, z1], [WX, lh, z0], [WX, lh, z1], lens=lens, **kw)

# 1: the hook. He walks along the wall; his shadow walks the same walk on the wall six tenths of a second behind him: more than a metre of bare wall
#    between them. He stops; she walks on, arrives, stops; his eyes go to her; her head turns: two white eyes
D1 = st.dur('S01'); T1 = 0.72; DL1 = 0.5               # he stops; how late she is
Z1 = 0.55                                            # where he stops
zh1 = lambda t: round(Z1 + VW * max(0.0, T1 - t), 3)   # his z at t
st.shot('S01', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, zh1(0.0)], 180, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, Z1], dur=T1, clip='walk', ease='linear', face=180, cruise='in'),
            k(T1 + 0.22, toon={'face': {'gx': 0.9, 'browL': 0.5}}, toonDur=0.08), k(T1 + 0.52, toon={'face': {'browL': 0.6}}, toonDur=0.06), k(T1 + 0.5, look=[WX - 5.3, 1.5, Z1 + 0.3]), k(T1 + 0.5, expr='unimpressed')]),   # his eyes go back to her; then his head comes to us: you see?
        act('ombre', [SX, 0.0, zh1(-DL1) + LAG], 180, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(0.0, to=[SX, 0, Z1 + LAG], dur=T1 + DL1, clip='walk', ease='linear', face=180, cruise='in'),
            k(T1 + DL1 + 0.04, look=[WX - 5.3, 1.5, Z1 + 0.4]), k(T1 + DL1 + 0.04, expr='worried')])],                                             # she has arrived: her head turns to us: two eyes
        props=[WALL(2.0)],
        cams=[wallcam(0.0, zh1(0.0) + 0.45, Z1 + 0.45), wallcam(T1, Z1 + 0.45, Z1 + 0.4)])
st.cue('sfx:tick', 'S01', T1, 0.3)

# 2: by a second. Closer. He looks at his watch and lowers his arm; half a second later she looks at hers, alone; his head turns to her
D2 = st.dur('S02'); W2 = 0.46; DL2 = 0.5
cam2 = lambda t, z0, z1, **kw: wallcam(t, z0, z1, d=3.4, h=1.5, lh=1.5, **kw)
st.shot('S02', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, Z1], 180, 'checkWatch', 'unimpressed', keys=[k(0.0, look=None), k(W2, clip='stand', blend=0.12), k(W2 + 0.1, look=[SX, 1.7, Z1 + LAG]),   # his arm comes down; his head goes to the wall
            k(W2 + 0.3, toon={'face': {'browL': 0.7, 'lid': 0.3}}, toonDur=0.08)]),
        act('ombre', [SX, 0, Z1 + LAG], 180, 'stand', 'worried', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(DL2, clip='checkWatch', blend=0.1), k(DL2 + 0.3, toon={'sq': FLATX, 'face': {'eye': 0.3}}, toonDur=0.06)])],                                 # late: she looks at her wrist when he has finished
        props=[WALL(2.0)],
        cams=[cam2(0.0, Z1 + 0.3, Z1 + 0.27)])
st.cue('sfx:tick', 'S02', 0.02, 0.3); st.cue('sfx:tick', 'S02', DL2 + 0.02, 0.25)

# 3: then by an hour. He waits on a bench at the foot of the wall, his eyes on his watch; over him the clock runs an hour in half a second; then
#    she drops into her place on the wall behind him, out of breath
D3 = st.dur('S03'); H3 = 0.46; A3 = 0.52               # the clock stops; she arrives
Z3 = -6.0; BEN3 = [round(WX - 0.47, 3), 0, Z3]; SEAT3 = [round(BEN3[0] + 0.05, 3), 0.02, Z3 - 0.25]
st.shot('S03', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', SEAT3, -90, 'sitWatch', 'unimpressed', keys=[k(0.0, look=None), k(H3 + 0.02, toon={'face': {'gy': -0.7, 'gx': -0.5, 'browL': 0.5}}, toonDur=0.06),   # his eyes go up to the clock
            k(A3 + 0.2, clip='sit', blend=0.12), k(A3 + 0.24, toon={'face': {'lid': 0.4, 'browL': 0.6}}, toonDur=0.08), k(A3 + 0.24, look=[WX - 4.6, 1.3, Z3])]),                 # she is there: he does not turn round: a look at us
        act('ombre', [SX, 3.3, Z3 + 0.2], -90, 'sit', 'worried', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATZ}, toonDur=0.0),
            k(A3, to=[SX, 0.02, Z3 + 0.2], dur=0.12, clip='sit', glide=True, ease='in', face=-90, blend=0.0), k(A3 + 0.12, clip='sit', blend=0.02),
            k(A3 + 0.12, toon={'sq': [1.22, 0.74, 0.03]}, toonDur=0.03), k(A3 + 0.16, toon={'sq': [0.95, 1.06, 0.03], 'settle': 0.5}, toonDur=0.08, toonEase='outBack'),   # she lands, flat, and springs back
            k(A3 + 0.26, toon={'sq': [1.03, 0.97, 0.03]}, toonDur=0.07), k(A3 + 0.33, toon={'sq': [0.98, 1.03, 0.03]}, toonDur=0.07), k(A3 + 0.4, toon={'sq': [1.03, 0.97, 0.03]}, toonDur=0.07), k(A3 + 0.47, toon={'sq': FLATZ}, toonDur=0.07)])],   # out of breath
        props=[WALL(Z3 + 2.0), P('bench', 'bench', pos=BEN3, ry=-90, opts={'w': 2.0}),
               P('clock', 'wallClock', pos=[round(WX - 0.05, 3), 2.72, Z3 + 0.85], ry=-90, opts={'rate': round(1 / H3, 3), 'until': H3, 'hours': 0})],
        cams=[wallcam(0.0, Z3 + 0.25, Z3 + 0.22, d=4.6, h=1.3, lh=1.55)])
st.cue('sfx:tick', 'S03', H3, 0.4); st.cue('thud', 'S03', A3 + 0.12, 0.4)

st.write("L'ombre", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, clothGravity=True, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'castShadow': False},
    'ombre': {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'silhouette': INK, 'darkEyes': 1.5}})
