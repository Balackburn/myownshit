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
         ('S17', 'L09', 4), ('S18', 'L10', 0), ('S19', 'L10', 4), ('S20', 'L11', 0), ('S21', 22.05, 0), ('S22', 'L12', 0), ('S23', 'L12', 3), ('S24', 'L13', 0),
         ('S25', 'L13', 7), ('S26', 28.9, 0)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}
r3 = lambda v: [round(x, 3) for x in v]
SHADE = '#6A5878'                                     # the one shade of every shadow of the film (actors, props, pictograms): a flat violet, half-way in value between his navy suit and the sunny wall (in ink black she was one mass with his suit)
INK = SHADE
def DIAL(id, pos, t0, t1=None, shade=False, r=0.075, ry=-90, rot=None):
    # the face of a watch, as big as a fist, facing the road: it stands where a wrist is while it is looked at (from t0 to t1: it pops in and out with
    # the arm). On a wrist a watch shows its strap or its edge whichever way the forearm turns; on a shadow it was black on black
    ks = [k(0.0, scale=0.01, dur=0.0)] if t0 > 0 else []
    if t0 > 0: ks.append(k(t0, scale=1.0, dur=0.08, ease='outBack'))
    if t1 is not None: ks.append(k(t1, scale=0.01, dur=0.07, ease='in'))
    return P(id, 'watchFace', pos=pos, ry=ry, **({'rot': rot, 'rotOrder': 'YXZ'} if rot else {}), opts={'r': r, **({'rim': SHADE, 'hands': SHADE} if shade else {})}, keys=ks)
FLATX, FLATZ, THIN = [0.03, 1, 1], [1, 1, 0.03], 0.03   # a shadow on a wall he walks along (flattened across his shoulders); one that faces out of its wall, or lies on the ground

# ---- the street: the right-hand pavement (x 5..10) of the Paris street, a sunny blank wall along it (its face at x = WX, toward the road). The sun comes
#      from the road side, a little from down the street: shadows fall on the wall, a little behind whoever walks toward -Z
STREET = {'clear': [-80, 80], 'eiffel': False, 'paveW': 6.5}   # paveW: the pavements run under the house fronts (at 5 m a dark gutter showed along the foot of the walls)
WX = 9.6; HX = 8.85; SX = round(WX - 0.03, 3)        # the wall; his line along it; the plane of his shadow on it
SUN = {'sunDir': [-0.8, 0.5, -0.3], 'fill': 1.25, 'ao': 0.3}   # ao: a man who has no shadow had a soft dark halo on the wall behind him
LAG = 0.55                                           # how far behind him (toward +Z) his shadow stands on the wall when all is well
WALLC = {'color': '#E4E7E5', 'foot': '#CDD1CC', 'cap': '#BEC3BE', 'strip': True}   # a paler, cooler render (under the warm sun the cream one came out orange, the colour of his skin); strip: the string course and the balcony of the next floor: the foot of a Paris house
def WALL(zc=0.0, w=16.0, plaque=None, stencil=None, sun=None, **kw):   # plaque / stencil / sun: where (world z) the street plaque, the stencilled DÉFENSE D'AFFICHER, the slanted edge of a roof's shade are
    o = {'w': w, 'h': 3.4, **WALLC, **kw}
    if plaque is not None: o['plaque'] = {'text': 'RUE DU SOLEIL', 'x': round(plaque - zc, 3), 'y': 2.66, 'w': 0.8}   # between the heads (a man of the series is 2.2 m to the top of his tuft, 2.45 seen from the road) and the string course
    if stencil is not None: o['stencil'] = {'x': round(stencil - zc, 3), 'y': 2.46, 'w': 1.25}   # above the heads (at 2 m a man who walked by hid half of it)
    if sun is not None: o['sun'] = {'x': round(sun - zc, 3), 'w': -3.0, 'slope': 0.42}   # (it runs down toward -Z: the left of the picture)
    return P('wall', 'plainWall', pos=[WX, 0, zc], ry=-90, opts=o)
def POTELET(z, dx=0.3):   # a Paris bollard at dx from the wall, and its shadow on the wall, in the shade of the film, where the sun puts it: the rule (a thing has a shadow, on time)
    return [P('pot', 'potelet', pos=[round(WX - dx, 3), 0, z], castShadow=False), P('pots', 'potelet', pos=[SX, 0, round(z + dx * LAG / (WX - HX), 3)], silhouette=SHADE, flat=[0.03, 1, 1])]
VW = 1.5                                             # a walk, m/s
def wallcam(t, z0, z1, d=5.3, h=1.45, lh=1.3, lens=44, **kw):   # a camera on the road side looking square at the wall, from z0 to z1
    return cam(t, [round(WX - d, 3), h, z0], [round(WX - d, 3), h, z1], [WX, lh, z0], [WX, lh, z1], lens=lens, **kw)

# 1: the hook. He walks along the wall; his shadow walks the same walk on the wall six tenths of a second behind him: more than a metre of bare wall
#    between them. He stops; she walks on, arrives, stops; his eyes go to her; her head turns: two white eyes
D1 = st.dur('S01'); T1 = 0.72; DL1 = 0.5               # he stops; how late she is
Z1 = 0.55                                            # where he stops
ZP1 = round(Z1 + 1.07, 3)                            # the bollard of this stretch of wall: at the right of the frame, its shadow beside it, on time
WALL1 = lambda: WALL(2.0, plaque=Z1 + 0.97, sun=Z1 + 0.05)   # the wall of the first shots (and of the last walk): RUE DU SOLEIL over the bollard, clear of the heads; the shade of a roof in the top left corner
zh1 = lambda t: round(Z1 + VW * max(0.0, T1 - t), 3)   # his z at t
st.shot('S01', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, zh1(0.0)], 180, 'stand', 'neutral', keys=[k(0.0, look=[HX - 2.4, 1.65, round(zh1(0.0) - 4.0, 3)]), k(T1, look=None), k(0.0, to=[HX, 0, Z1], dur=T1, clip='walk', ease='linear', face=180, cruise='in'),   # his head a third of the way to us as he walks (in pure profile a head of the series is an ear on a box)
            k(T1 + 0.22, toon={'face': {'gx': 0.9, 'browL': 0.5}}, toonDur=0.08), k(T1 + 0.52, toon={'face': {'browL': 0.6}}, toonDur=0.06), k(T1 + 0.5, look=[WX - 5.3, 1.5, Z1 + 0.3]), k(T1 + 0.5, expr='unimpressed'), k(T1 + 0.8, toon={'face': {'browL': 0.6, 'lid': 1}}, toonDur=0.05), k(T1 + 0.9, toon={'face': {'browL': 0.7, 'lid': 0.4}}, toonDur=0.06)]),   # his eyes go back to her; then his head comes to us: you see? a slow blink
        act('ombre', [SX, 0.0, zh1(-DL1) + LAG], 180, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(0.0, to=[SX, 0, Z1 + LAG], dur=T1 + DL1, clip='walk', ease='linear', face=180, cruise='in'),
            k(T1 + DL1 + 0.04, look=[WX - 5.3, 1.5, Z1 + 0.4]), k(T1 + DL1 + 0.04, expr='worried'), k(T1 + DL1 + 0.3, toon={'sq': FLATX, 'bend': {'neck': [0, 0, 0.22, 1, None]}}, toonDur=0.12)])],   # she has arrived: her head turns to us: two eyes; then goes on one side: sorry
        props=[WALL1(), *POTELET(ZP1)],
        cams=[wallcam(0.0, zh1(0.0) + 0.45, Z1 + 0.45, d=4.5), wallcam(T1, Z1 + 0.45, Z1 + 0.4, d=4.5)])   # closer than the first staging (two figures at half the height of a frame that was two thirds beige)
st.cue('sfx:tick', 'S01', T1, 0.3)

# 2: by a second. Closer. His wrist comes up, a white dial on it; he looks at it; his arm goes down; half a second later she lifts hers, alone, and
#    bends her head to it; his head comes round to her, three quarters to us
D2 = st.dur('S02'); U2, W2, DL2 = 0.1, 0.44, 0.5; LAG2 = 0.66   # his wrist is up; it goes down; hers comes up; how far behind him she stands here (her forearm must not touch his back)
cam2 = lambda t, z0, z1, **kw: wallcam(t, z0, z1, d=3.8, h=1.5, lh=1.45, **kw)
WR2M = [HX - 0.36, 1.5, Z1 - 0.2]                    # his wrist: up in front of him, on the camera side: looking at it his face is three quarters to us (across his chest, the watch was hidden and his head was hair and an ear)
WR2S = [SX, 1.5, round(Z1 + LAG2 - 0.3, 3)]          # hers: up in front of her chest, on the wall
st.shot('S02', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, Z1], 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'hands': {'L': 'fist'}, 'reach': {'L': [HX - 0.1, 1.0, Z1 - 0.1, 1, 0.06]}}, toonDur=0.0),
            k(0.0, toon={'hands': {'L': 'fist'}, 'reach': {'L': [*WR2M, 1, 0.06]}, 'face': {'gy': 0.5, 'gx': -0.5}}, toonDur=U2, toonEase='outBack'), k(0.02, look=WR2M),   # up: his eyes, then his head, on the dial
            k(W2, toon={'face': {'browL': 0.5}}, toonDur=0.14, toonEase='in'), k(W2 + 0.04, look=None),                                            # down
            k(W2 + 0.22, toon={'face': {'gx': -0.9, 'browL': 0.7}}, toonDur=0.06), k(W2 + 0.3, look=[WX - 2.6, 1.6, Z1 + 1.3]),                           # his eyes, then his head, go back to her
            k(W2 + 0.4, toon={'face': {'browL': 0.8, 'lid': 0.3}}, toonDur=0.08)]),
        act('ombre', [SX, 0, round(Z1 + LAG2, 3)], 180, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(DL2, toon={'sq': FLATX, 'hands': {'L': 'fist'}, 'reach': {'L': [*WR2S, 1, 0.06]}, 'bend': {'neck': [0.34, 0, 0, 1, None]}}, toonDur=U2, toonEase='outBack'),   # late: her wrist comes up when his is down; her head bends to it
            k(DL2 + 0.3, toon={'sq': FLATX, 'hands': {'L': 'fist'}, 'reach': {'L': [*WR2S, 1, 0.06]}, 'bend': {'neck': [0.34, 0, 0, 1, None]}, 'face': {'eye': 0.3}}, toonDur=0.06)])],
        props=[WALL(2.0, sun=Z1 + 0.05), DIAL('dialm', [WR2M[0] - 0.07, WR2M[1] + 0.02, WR2M[2] - 0.02], U2 * 0.5, W2 + 0.03), DIAL('dials', [SX - 0.012, WR2S[1] + 0.02, WR2S[2] - 0.03], DL2 + U2 * 0.5, shade=True)],
        cams=[cam2(0.0, Z1 + 0.2, Z1 + 0.17)])
st.cue('sfx:tick', 'S02', 0.02, 0.3); st.cue('sfx:tick', 'S02', DL2 + 0.02, 0.25)

# 3: then by an hour. He waits on a bench at the foot of the wall, his eyes on his watch; over him the clock runs an hour in half a second; then
#    she drops into her place on the wall behind him, out of breath
D3 = st.dur('S03'); H3 = 0.4; A3 = 0.42                # the clock stops; she arrives
Z3 = -6.0; BEN3 = [round(WX - 0.47, 3), 0, Z3]; SEAT3 = [round(BEN3[0] + 0.05, 3), 0.02, Z3 - 0.25]
st.shot('S03', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', SEAT3, -90, 'sitWatch', 'unimpressed', keys=[k(0.0, look=None), k(H3 + 0.02, toon={'face': {'gy': -0.7, 'gx': -0.5, 'browL': 0.5}}, toonDur=0.06),   # his eyes go up to the clock
            k(A3 + 0.2, clip='sit', blend=0.12), k(A3 + 0.24, toon={'face': {'lid': 0.4, 'browL': 0.6}}, toonDur=0.08), k(A3 + 0.24, look=[WX - 4.6, 1.3, Z3])]),                 # she is there: he does not turn round: a look at us
        act('ombre', [SX, 4.6, Z3 + 0.2], -90, 'sit', 'worried', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATZ}, toonDur=0.0),
            k(A3 - 0.06, to=[SX, 0.95, Z3 + 0.2], dur=0.07, clip='sit', glide=True, ease='out', face=-90, blend=0.0), k(A3 - 0.04, toon={'sq': [0.86, 1.2, 0.03], 'face': {'eye': 0.5}}, toonDur=0.05, toonEase='out'),   # she falls into the picture, long
            k(A3 + 0.02, toon={'sq': [1.08, 0.94, 0.03], 'bend': {'shinL': [-0.5, 0, 0, 1, None], 'shinR': [0.5, 0, 0, 1, None]}, 'face': {'eye': 0.5}}, toonDur=0.05), k(A3 + 0.07, toon={'sq': [1.02, 0.98, 0.03], 'bend': {'shinL': [0.5, 0, 0, 1, None], 'shinR': [-0.5, 0, 0, 1, None]}, 'face': {'eye': 0.5}}, toonDur=0.05),   # and hangs over her place, three frames, her legs going
            k(A3 + 0.1, to=[SX, 0.02, Z3 + 0.2], dur=0.05, clip='sit', glide=True, ease='in', face=-90, blend=0.0),
            k(A3 + 0.15, toon={'sq': [1.16, 0.84, 0.03]}, toonDur=0.03), k(A3 + 0.2, toon={'sq': [0.93, 1.08, 0.03], 'settle': 0.5}, toonDur=0.07, toonEase='outBack'),   # she lands, and springs back (squashed to 0.7 she sank under the seat of the bench)
            *[x for i in range(3) for x in (k(round(A3 + 0.3 + 0.14 * i, 3), toon={'sq': [1.07, 0.93, 0.03], 'bend': {'spine': [0.16, 0, 0, 1, None]}}, toonDur=0.07), k(round(A3 + 0.37 + 0.14 * i, 3), toon={'sq': [0.96, 1.06, 0.03], 'bend': {'spine': [-0.06, 0, 0, 1, None]}}, toonDur=0.07))]])],   # out of breath: her shoulders go up and down
        props=[WALL(Z3 + 2.0), P('bench', 'bench', pos=BEN3, ry=-90, opts={'w': 2.0}),
               P('clock', 'wallClock', pos=[round(WX - 0.05, 3), 2.72, Z3 + 0.85], ry=-90, opts={'rate': round(1 / H3, 3), 'until': H3, 'hours': 0})],
        cams=[wallcam(0.0, Z3 + 0.25, Z3 + 0.22, d=4.6, h=1.3, lh=1.55)])
st.cue('sfx:tick', 'S03', H3, 0.4); st.cue('whoosh', 'S03', A3 - 0.06, 0.25, 0.1, 500, 1500); st.cue('thud', 'S03', A3 + 0.15, 0.4)

# 4: one morning. He comes along the wall, stops, turns to us and stretches, eyes shut: behind him the wall is bare
D4 = st.dur('S04'); T4 = 0.3; Z4 = 0.55
wall4 = lambda t, d=4.2, **kw: wallcam(t, Z4 + 0.47, Z4 + 0.44, d=d, h=1.45, lh=1.4, **kw)   # he at the left, the bare wall in the middle, the bollard and its shadow at the right: it has one
STRETCH = lambda dy=0.0, **kw: {'hands': {'L': 'spread', 'R': 'spread'}, 'reach': {'L': [HX - 0.1, 2.5 + dy, Z4 + 0.32, 1, 0.08], 'R': [HX - 0.1, 2.5 + dy, Z4 - 0.32, 1, 0.08]}, **kw}   # both arms up over his head
st.shot('S04', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, round(Z4 + VW * T4, 3)], 180, 'stand', 'happy', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, Z4], dur=T4, clip='walk', ease='out', face=180, cruise='in'),
            k(T4 - 0.06, face=-78, turn=0.16), k(T4, expr='yawn'),                                                                             # he stops and turns to us
            k(T4 - 0.02, toon=STRETCH(-0.25, sq=[1.03, 0.96, 1.03], face={'jaw': 0.5}), toonDur=0.1, toonEase='in'),
            k(T4 + 0.1, toon=STRETCH(0.05, sq=[0.93, 1.1, 0.93], bend={'spine': [-0.16, 0, 0, 1.06, None]}, face={'jaw': 0.8}), toonDur=0.16, toonEase='out'),   # up on his toes: a stretch, a yawn
            k(T4 + 0.3, toon=STRETCH(0.0, sq=[0.95, 1.07, 0.95], bend={'spine': [-0.2, 0, 0, 1.06, None]}, face={'jaw': 0.6}, settle=0.5), toonDur=0.12)])],
        props=[WALL1(), *POTELET(ZP1)],
        cams=[wall4(0.0)])
st.cue('whoosh', 'S04', 0.0, 0.2, 0.3, 300, 1200); st.cue('sfx:stretch', 'S04', T4, 0.3)

# 5: she has not come. Arms still up, one eye opens and slides to the wall; his head goes round: nothing: where she should be, an outline in dashes and
#    a question mark; his arms come down; he lifts a foot and looks under his shoe; then at us
D5 = st.dur('S05'); E5, H5, O5, F5, U5 = 0.08, 0.22, 0.34, 0.56, 0.86   # an eye opens; his head goes to the wall; the outline; the foot; to us
GH5 = [SX, 0.0, round(Z4 + 0.66, 3)]                 # where she should stand on the wall: beside him, in clear view
st.shot('S05', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, Z4], -78, 'stand', 'yawn', blink=0, keys=[k(0.0, look=None), k(0.0, toon=STRETCH(0.0, sq=[0.95, 1.07, 0.95], bend={'spine': [-0.2, 0, 0, 1.06, None]}, face={'jaw': 0.6}), toonDur=0.0),
            k(E5, toon=STRETCH(0.0, sq=[0.96, 1.05, 0.96], face={'lidL': 1, 'gx': 0.9, 'browR': 0.8}), toonDur=0.06), k(E5, expr='neutral'),                          # one eye, toward the wall
            k(H5, look=[WX, 1.3, Z4 + 1.0]), k(H5 + 0.02, toon=STRETCH(-0.1, face={'brow': 0.7, 'eye': 0.3}), toonDur=0.1),                                          # his head goes round
            k(O5 + 0.06, toon={'sq': [1.04, 0.95, 1.04], 'face': {'brow': 1, 'eye': 0.45, 'jaw': 0.35}}, toonDur=0.1, toonEase='out'), k(O5 + 0.06, expr='surprised'),   # his arms drop
            k(F5 - 0.08, look=[HX - 0.9, 0.9, Z4 - 0.12]), k(F5, clip='showSole', blend=0.12), k(F5, toon={'sq': [0.98, 1.03, 0.98], 'face': {'brow': 0.8, 'gy': 0.8}}, toonDur=0.1),   # under his shoe: he holds it up to us: nothing there either
            k(U5 - 0.06, clip='stand', blend=0.1), k(U5 - 0.04, look=[WX - 4.0, 1.45, Z4 + 0.34]), k(U5, toon={'face': {'brow': 1, 'eye': 0.4, 'mouth': 'o'}}, toonDur=0.08), k(U5, expr='worried')])],   # to us
        props=[WALL1(), *POTELET(ZP1), P('ghost', 'ghostOutline', pos=GH5, ry=-90, opts={'at': O5, 'h': 1.75}),
               P('sole', 'shoeSole', on={'actor': 'mec', 'joint': 'footR', 'offset': [0, -0.075, 0.06]}, castShadow=False)],
        cams=[wall4(0.0), glide([wallcam(H5, Z4 + 0.47, Z4 + 0.47, d=4.1, h=1.45, lh=1.3)], 0.25)])   # the frame slides to the place where she should be (the outline whole, its arm inside the frame)
st.cue('pop', 'S05', O5, 0.45); st.cue('sfx:tick', 'S05', E5, 0.25); st.cue('whoosh', 'S05', H5, 0.2, 0.15, 500, 1800)

# ---- the town hall: the registry desk (ÉTAT CIVIL), a clerk behind it
MAIRIE = {'map': False, 'plant': False, 'bannerY': 2.78, 'clockX': 9, 'wall': '#CFE0CC', 'band': '#6F9B7A', 'trim': '#4E7458',   # a green office (in cream and wood it was the beige of the street wall: the cut did not change place)
          'front': 3.3, 'frontSign': {'text': 'ÉTAT CIVIL', 'x': 1.0, 'y': 2.62, 'w': 1.35}}   # the wall behind him, seen from her side: where we are
VIS, CLK = [-0.1, 0, 0.42], [0.0, 0, -1.66]           # where he stands; where she sits... stands
EYE_C, EYE_V = [0.0, 1.42, -1.52], [-0.1, 1.5, 0.3]   # her eyes; his: each shot of the pair is seen from the other's place
PO6 = [0.38, 1.5, 0.14]                              # the notice he holds up beside his head
# 6: he declares her missing: seen from the clerk's place: he holds up a notice beside his head: PERDUE, and the outline of a man: his; his finger taps
#    the outline, then his own chest
D6 = st.dur('S06'); U6, A6, A6B, B6 = 0.14, 0.4, 0.62, 0.84   # the notice is up; his finger on the outline; again; on his own chest
HOLD6 = lambda l, **kw: {'hands': {'R': 'grip', 'L': 'point'}, 'reach': {'R': [PO6[0] + 0.02, PO6[1] - 0.36, PO6[2] + 0.03, 1, 0.05], 'L': [*l, 1, 0.14]}, **kw}
L6A, L6B, L6C = [PO6[0] - 0.3, 1.2, PO6[2] - 0.12], [PO6[0] + 0.02, PO6[1] - 0.1, PO6[2] - 0.04], [VIS[0] - 0.02, 1.32, VIS[2] - 0.2]   # his left forefinger: waiting; on the outline; on his own chest
st.shot('S06', 'mairie', setOpts=MAIRIE, actors=[
        act('mec', VIS, 180, 'stand', 'worried', keys=[k(0.0, look=EYE_C), k(0.0, toon=HOLD6(L6A, face={'brow': 0.9, 'eye': 0.3}), toonDur=0.0),
            k(A6 - 0.14, toon=HOLD6(L6A, face={'brow': 0.9, 'eye': 0.3, 'gx': -0.8}), toonDur=0.08), k(A6 - 0.06, toon=HOLD6(L6B, scl={'handL': [1.25, 1.25, 1.25]}, face={'brow': 0.9, 'gx': -0.8}), toonDur=0.06, toonEase='in'),   # his eyes, then his finger, to the outline: this (held three frames: at two it was a blur)
            k(A6 + 0.1, toon=HOLD6(L6A, face={'brow': 1, 'eye': 0.3}), toonDur=0.06), k(A6B - 0.06, toon=HOLD6(L6B, scl={'handL': [1.25, 1.25, 1.25]}, face={'brow': 1}), toonDur=0.06, toonEase='in'),                                    # twice
            k(B6 - 0.1, toon=HOLD6(L6A, face={'brow': 1, 'eye': 0.3}), toonDur=0.05), k(B6 - 0.04, toon=HOLD6(L6C, sq=[0.97, 1.04, 0.97], face={'brow': 1, 'eye': 0.4, 'mouth': 'o'}), toonDur=0.06, toonEase='in'),                         # then on his own chest: mine
            k(B6 + 0.1, toon=HOLD6(L6C, settle=0.5, face={'brow': 1, 'eye': 0.4, 'mouth': 'o'}), toonDur=0.08), k(B6 + 0.26, toon=HOLD6(L6C, face={'brow': 1, 'eye': 0.4, 'lid': 1}), toonDur=0.04), k(B6 + 0.33, toon=HOLD6(L6C, face={'brow': 1, 'eye': 0.4}), toonDur=0.04)])],
        props=[P('poster', 'lostPoster', pos=[PO6[0], PO6[1] - 0.75, PO6[2]], ry=180, opts={'w': 0.52}, keys=[k(0.0, to=PO6, dur=U6, ease='outBack'), k(A6, squash=[1.07, 0.94, 1.0], dur=0.14), k(A6B, squash=[1.07, 0.94, 1.0], dur=0.14)])],   # it gives under each tap of his finger
        cams=[cam(0.0, [0.13, 1.52, -2.38], [0.13, 1.52, -2.26], [0.13, 1.4, 0.3], [0.13, 1.4, 0.3], lens=54)])   # from her side of the desk: the notice at the left, his face at the right, the desk across the bottom
st.cue('whoosh', 'S06', 0.0, 0.25, 0.15, 500, 1800); st.cue('sfx:tick', 'S06', A6, 0.3); st.cue('sfx:tick', 'S06', A6B, 0.3); st.cue('thud', 'S06', B6, 0.2)

# 7: at the town hall. Seen from his place: the clerk holds his notice up between them (we see its back): her eyes, over its top edge and her glasses,
#    go down to it, up to us, down to it
D7 = st.dur('S07'); SH7 = [0.0, 1.45, -1.1]            # the sheet, held up at arm's length, facing her: high enough for her eyes alone to clear it (its top edge was tangent to her chin: a blank slab under a whole face)
CLKH = lambda **kw: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [SH7[0] + 0.2, SH7[1] - 0.12, SH7[2] - 0.02, 1, 0.05], 'R': [SH7[0] - 0.2, SH7[1] - 0.12, SH7[2] - 0.02, 1, 0.05]}, **kw}
CAM7 = lambda t, dz=0.0, **kw: cam(t, [0.42, 1.36, 0.6 - dz], [0.4, 1.36, 0.48 - dz], [0.0, 1.76, -1.9], [0.0, 1.76, -1.9], lens=44, **kw)   # low enough for the banner over her
st.shot('S07', 'mairie', setOpts=MAIRIE, actors=[
        act('clerk', CLK, 0, 'stand', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon=CLKH(face={'gy': 0.8, 'gx': -0.6, 'browL': 0.4}), toonDur=0.0),      # she reads: her eyes run along a line, her head after them
            k(0.04, toon=CLKH(face={'gy': 0.8, 'gx': 0.6, 'browL': 0.4}, bend={'neck': [0.1, 0.1, 0, 1, None]}), toonDur=0.16, toonEase='linear'),
            k(0.22, toon=CLKH(face={'gy': 0.85, 'gx': -0.6, 'browL': 0.5}, bend={'neck': [0.14, -0.1, 0, 1, None]}), toonDur=0.05),                                 # the next line
            k(0.3, toon=CLKH(face={'gy': -0.35, 'brow': 0.6}, bend={'neck': [0.24, 0, 0, 1, None]}), toonDur=0.07), k(0.32, look=[0.42, 1.36, 0.95]),               # up to us over her glasses: her head goes down as her eyes come up
            k(0.56, toon=CLKH(face={'gy': 0.8, 'browL': 0.6}, bend={'neck': [0.1, 0, 0, 1, None]}), toonDur=0.07), k(0.58, look=None),                               # down to it
            k(0.7, toon=CLKH(face={'gy': 0.8, 'browL': 0.6, 'lid': 1}, bend={'neck': [0.1, 0, 0, 1, None]}), toonDur=0.04), k(0.77, toon=CLKH(face={'gy': 0.8, 'browL': 0.6}, bend={'neck': [0.1, 0, 0, 1, None]}), toonDur=0.04)])],   # a blink
        props=[P('poster', 'lostPoster', pos=SH7, ry=180, rot=[0.12, 0, 0], opts={'w': 0.46, 'back': True})],
        cams=[CAM7(0.0)])
st.cue('pop', 'S07', 0.0, 0.25)

# 8: the answer. She lays the sheet on her desk, takes her stamp, breathes on it, looks at us over her glasses, and stamps: a small dry tap
D8 = st.dur('S08'); L8, HA8, LK8, UP8, TP8 = 0.14, 0.36, 0.6, 0.8, 1.0   # the sheet is down; she breathes on the stamp; a look at us; the stamp goes up a little; the tap
ONDESK = [0.0, 0.835, -0.72]                         # the sheet, flat on the desk
ST8A, ST8B, ST8C, ST8D = [-0.36, 0.98, -1.05], [-0.1, 1.36, -1.3], [-0.04, 1.16, -0.82], [-0.04, 0.9, -0.76]   # the stamp: off the ink pad; at her mouth; over the sheet; on it
CLK8 = lambda r, **kw: {'hands': {'L': 'open', 'R': 'grip'}, 'reach': {'L': [0.24, 0.87, -0.86, 1, 0.08], 'R': [*r, 1, 0.05]}, **kw}
st.shot('S08', 'mairie', setOpts={**MAIRIE, 'plate': False}, actors=[   # (the plate on the front of the desk stood under the captions)
        act('clerk', CLK, 0, 'stand', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon=CLKH(face={'gy': 0.8, 'browL': 0.5}), toonDur=0.0),
            k(0.02, toon=CLK8(ST8A, bend={'spine': [0.18, 0, 0, 1, None]}, face={'gy': 0.8}), toonDur=L8, toonEase='inOut'),                                      # the sheet down, her hand to the stamp
            k(HA8 - 0.14, toon=CLK8(ST8B, face={'gy': 0.3, 'jaw': 0.1}), toonDur=0.12, toonEase='out'), k(HA8, toon=CLK8(ST8B, sq=[1.03, 0.97, 1.03], face={'jaw': 0.7, 'cheeks': 0.6, 'lid': 0.6}), toonDur=0.05),   # hah
            k(HA8 + 0.14, toon=CLK8(ST8B, face={'jaw': 0.0, 'lid': 0.3}), toonDur=0.08),
            k(LK8, toon=CLK8(ST8C, face={'gy': -0.3, 'browL': 0.8, 'lid': 0.35}), toonDur=0.14, toonEase='inOut'), k(LK8 + 0.02, look=[0.42, 2.08, 1.15]),               # a look at us over her glasses, the stamp over the sheet
            k(UP8, toon=CLK8([ST8C[0] - 0.06, ST8C[1] + 0.42, ST8C[2] - 0.1], sq=[0.99, 1.02, 0.99], bend={'spine': [-0.06, 0, 0, 1, None]}, face={'gy': -0.3, 'browL': 0.9, 'lid': 0.3}), toonDur=0.12, toonEase='out'),   # up: to her shoulder: she grows with it
            k(TP8 - 0.05, toon=CLK8(ST8D, sq=[1.05, 0.94, 1.05], bend={'spine': [0.2, 0, 0, 1, None]}, face={'gy': -0.3, 'browL': 0.8, 'lid': 0.35}), toonDur=0.05, toonEase='in'),   # and down, two frames: her eyes have not left us
            k(TP8 + 0.05, toon=CLK8([ST8D[0], ST8D[1] + 0.07, ST8D[2]], settle=0.4, face={'gy': -0.3, 'browL': 0.9, 'lid': 0.35}), toonDur=0.08)])],
        props=[P('poster', 'lostPoster', pos=SH7, ry=180, rot=[0.12, 0, 0], opts={'w': 0.46, 'stampAt': TP8, 'back': True}, keys=[k(0.02, to=ONDESK, dur=L8, ease='inOut'), k(0.02, rotTo=[-1.5, 0, 0], dur=L8, ease='inOut'),   # she turns it over as she lays it down: the print up, its foot toward us
                    k(TP8, to=[ONDESK[0], ONDESK[1] + 0.05, ONDESK[2]], dur=0.05, ease='out'), k(TP8 + 0.05, to=ONDESK, dur=0.07, ease='in')]),
               P('stamp', 'rubberStamp', on={'actor': 'clerk', 'hand': 'R', 'offset': [0, -0.06, 0.02], 'rot': [3.1416, 0, 0]}, scale=1.5),
               P('hah', 'dustPuff', pos=[-0.08, 1.38, -1.14], scale=0.2, opts={'once': True, 'startAt': HA8, 'period': 0.3, 'color': '#FFFFFF'}),
               P('tap', 'impactStars', pos=[-0.04, 0.95, -0.7], rot=[-0.9, 0, 0], opts={'at': TP8, 'n': 5, 'r': 0.24, 'r0': 0.08, 'dur': 0.26, 'size': 0.055})],
        fx=[{'type': 'shake', 'at': TP8, 'dur': 0.12, 'amount': 0.012}],
        cams=[cam(0.0, [0.42, 2.35, 1.7], [0.4, 2.35, 1.62], [-1.068, -1.646, -7.345], [-1.068, -1.646, -7.345], lens=50)])   # from higher: her whole face at the top, the sheet on the desk above the caption band (kit fit(): at first the stamp landed under the captions)
st.cue('sfx:slideDown', 'S08', 0.02, 0.2); st.cue('sfx:gasp', 'S08', HA8, 0.3); st.cue('clack', 'S08', TP8, 0.6)

# 9: « Elle est majeure. »: she holds the sheet up beside her face, its front to us this time: the outline, and across it, in red: MAJEURE; she says it
D9 = st.dur('S09'); PO9 = [-0.37, 1.75, -1.14]   # the sheet: beside her face (lower, its stamp fell in the caption band)
W9 = [round(w['s'] - st.SH['S09'][0], 3) for w in st.L['L05']['words']]
CLK9 = lambda **kw: {'hands': {'L': 'open', 'R': 'grip'}, 'reach': {'R': [PO9[0] + 0.05, PO9[1] - 0.36, PO9[2] - 0.03, 1, 0.05], 'L': [0.2, 0.86, -0.85, 1, 0.08]}, **kw}
st.shot('S09', 'mairie', setOpts={**MAIRIE, 'bannerX': -0.25}, actors=[
        act('clerk', CLK, 0, 'stand', 'unimpressed', blink=0, keys=st.talk('L05', 'S09', 'unimpressed') + [k(0.0, look=[0.2, 1.4, 0.75]), k(0.0, toon=CLK9(face={'browL': 0.8, 'lid': 0.35}), toonDur=0.0),
            *[x for i, t in enumerate(W9) for x in (k(max(0.0, t), toon=CLK9(sq=[0.98, 1.03, 0.98], face={'jaw': 0.55 if i < 2 else 0.8, 'browL': 0.9, 'lid': 0.3}), toonDur=0.05, toonEase='out'), k(max(0.0, t) + (0.1 if i < 2 else 0.3), toon=CLK9(face={'browL': 0.8, 'lid': 0.35}), toonDur=0.08))],   # her jaw long on each word
            *[x for dt, j in ((0.2, 0.6), (0.42, 0.75)) for x in (k(round(max(0.0, W9[-1]) + dt, 3), toon=CLK9(sq=[0.98, 1.03, 0.98], face={'jaw': j, 'browL': 0.9, 'lid': 0.3}), toonDur=0.05, toonEase='out'), k(round(max(0.0, W9[-1]) + dt + 0.12, 3), toon=CLK9(face={'browL': 0.8, 'lid': 0.35, 'jaw': 0.15}), toonDur=0.07))],   # ma-jeu-re: three beats of the jaw (it stopped after the first: the line ran on over a shut mouth)
            k(0.9, toon=CLK9(face={'browL': 0.9, 'lid': 1}), toonDur=0.04), k(0.96, toon=CLK9(face={'browL': 0.9, 'lid': 0.35, 'mouth': 'smirk'}), toonDur=0.04)])],   # a blink: next
        props=[P('poster', 'lostPoster', pos=[PO9[0], PO9[1] - 0.5, PO9[2]], ry=0, opts={'w': 0.46, 'stampAt': -1}, keys=[k(0.0, to=PO9, dur=0.12, ease='outBack')])],
        cams=[cam(0.0, [0.16, 1.4, 0.8], [0.15, 1.4, 0.68], [-0.25, 1.75, -1.4], [-0.25, 1.75, -1.4], lens=44)])   # the sheet at the left (off the edge of the frame), her face at the right
st.cue('whoosh', 'S09', 0.0, 0.25, 0.12, 500, 1800)
# (no title card here: with the red stamp and the caption the word was three times in one picture; the card of this film is on « Avec un avocat »)

# ---- further down the street: another stretch of sunny wall
Z10 = -14.0
LEGS = lambda f=1.9: {k_: [0, 0, 0, f, None] for k_ in ('legL', 'shinL', 'legR', 'shinR')}
TALLB = {'spine': [0, 0, 0, 1.25, None], 'neck': [0, 0, 0, 1.3, None], **LEGS()}   # she, stretched to another man's height: on legs twice as long, a longer back, a longer neck: his outline (the tuft, the tie), another man's size
LEGUP = 0.86                                         # what legs 1.9 times as long lift her hips by (the stretch runs down from the hip: without it her feet were under the pavement)
TALL = lambda **kw: {'sq': [0.03, 1, 0.9], 'bend': TALLB, **kw}
TALLF = lambda **kw: {'sq': [0.9, 1, 0.03], 'bend': TALLB, **kw}                    # the same, turned to face out of the wall
# 10: she already worked elsewhere. A very tall man in a hat strides along the wall (left to right, for once: the sun is behind him and his shadow goes
#     before him): on the wall, a shadow we know (the tuft, the tie) on legs twice as long, in step with him to the frame. The frame goes with them and
#     finds our man, who watches them come; they stop; two watches come up together; his hand goes out to her
D10 = st.dur('S10'); VT = 1.7; ST10 = 0.95; T10 = round(ST10 - 0.22, 3)   # the tall man's speed; when he has stopped; when he starts to slow
ZS10 = round(Z10, 3); LAG10 = 0.62                   # where he stops; her place on the wall, ahead of him
zt10 = lambda t: round(ZS10 - 0.15 - VT * (T10 - t), 3) if t < T10 else round(ZS10 - 0.15 * (1 - min(1.0, (t - T10) / 0.22)) ** 3, 3)   # the tall man's z
ME10 = [HX, 0, round(ZS10 + 1.68, 3)]                # our man: on their way, at the right, facing them
WRT10 = [HX - 0.42, 2.42, round(ZS10 + 0.3, 3)]      # the tall man's wrist, up (on the road side); hers, on the wall
WRS10 = [SX, 2.62, round(ZS10 + LAG10 + 0.32, 3)]
UPT = lambda **kw: {'hands': {'R': 'fist'}, 'reach': {'R': [*WRT10, 1, 0.06]}, **kw}
UPS = lambda **kw: TALL(hands={'L': 'fist'}, reach={'L': [*WRS10, 1, 0.06]}, **kw)
cam10 = lambda t, z0, z1, **kw: cam(t, [round(WX - 7.0, 3), 1.25, z0], [round(WX - 7.0, 3), 1.25, z1], [WX, 1.95, z0], [WX, 1.95, z1], lens=44, **kw)   # low, far enough for a man of three metres and a half
st.shot('S10', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('grand', [HX, 0, zt10(0.0)], 0, 'walk', 'smug', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, zt10(T10)], dur=T10, clip='walk', ease='linear', face=0, cruise='in'),
            k(T10, to=[HX, 0, ZS10], dur=0.22, clip='walk', then='stand', ease='out', face=0),
            k(ST10 + 0.12, toon=UPT(face={'gy': 0.5}), toonDur=0.1, toonEase='outBack'), k(ST10 + 0.14, look=WRT10)]),                                     # he stops; his wrist comes up
        act('ombre', [SX, LEGUP, round(zt10(0.0) + LAG10, 3)], 0, 'walk', 'neutral', keys=[k(0.0, look=None), k(0.0, toon=TALL(), toonDur=0.0),
            k(0.0, to=[SX, LEGUP, round(zt10(T10) + LAG10, 3)], dur=T10, clip='walk', ease='linear', face=0, cruise='in'),
            k(T10, to=[SX, LEGUP, round(ZS10 + LAG10, 3)], dur=0.22, clip='walk', then='stand', ease='out', face=0),
            k(ST10 + 0.12, toon=UPS(), toonDur=0.1, toonEase='outBack')]),                                                                                # in step with him; she stops with him; her wrist comes up with his: not a frame late
        act('mec', ME10, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[WX, 1.9, round(zt10(0.25) + LAG10, 3)]), k(0.0, toon={'face': {'lid': 0.4}}, toonDur=0.0),          # a glance at who comes: a tall man and his shadow: so what
            k(0.26, look=[WX - 5.5, 1.5, round(ME10[2] - 0.5, 3)]), k(0.3, toon={'face': {'lid': 0.45, 'browL': 0.3}}, toonDur=0.06),                                  # his head comes back to us
            k(0.5, look=[WX, 2.3, round(zt10(0.62) + LAG10, 3)]), k(0.5, expr='surprised'),                                                                              # ...and whips back: that tuft, that tie
            k(0.52, toon={'scl': {'head': [1.4, 0.86, 1]}, 'sq': [0.95, 1.08, 0.95], 'bend': {'neck': [0, 0, 0, 1.22, None]}, 'face': {'pop': 0.8, 'jaw': 0.5}}, toonDur=0.06, toonEase='out'),   # his eyes come out on stalks
            k(0.64, toon={'bend': {'neck': [0, 0, 0, 1.12, None], 'spine': [-0.12, 0, 0, 1, None]}, 'face': {'pop': 0.75, 'jaw': 0.5}}, toonDur=0.1),                       # he leans back to see her whole
            *[k(t, look=[WX, 2.2, round(zt10(t + 0.1) + LAG10, 3)]) for t in (0.7, 0.9)],
            k(0.9, toon={'bend': {'spine': [-0.1, 0, 0, 1, None]}, 'sq': [0.98, 1.03, 0.98], 'face': {'pop': 0.2, 'brow': 1, 'eye': 0.45, 'jaw': 0.45}}, toonDur=0.1),
            k(ST10 + 0.2, toon={'hands': {'R': 'spread'}, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'reach': {'R': [HX + 0.3, 1.7, round(ZS10 + LAG10 + 0.75, 3), 0.9, 0.1]}, 'face': {'brow': 1, 'eye': 0.45, 'jaw': 0.6}}, toonDur=0.2, toonEase='out')])],   # a hand goes out to her
        props=[WALL(Z10 + 2.0), DIAL('dialt', [WRT10[0] - 0.08, WRT10[1] + 0.02, WRT10[2] + 0.02], ST10 + 0.17), DIAL('dials', [SX - 0.012, WRS10[1] + 0.02, WRS10[2] + 0.03], ST10 + 0.17, shade=True)],
        cams=[cam10(0.0, ZS10 + 0.26, ZS10 + 0.5, ease='out'), cam10(ST10, ZS10 + 0.5, ZS10 + 0.52)])   # her stretched shadow is in the frame first, the tall man walks into it after her; our man is whole in the frame before his double take (with a longer pan he was cut by its edge when his eyes came out)
st.cue('whoosh', 'S10', 0.0, 0.2, 0.4, 300, 1200); st.cue('sfx:tick', 'S10', ST10 + 0.17, 0.3)

# 11: for a taller guy. Closer on the two of them: two watches, two heads bent, to the frame (she was half a second late for ours). Her head turns:
#     two white eyes on us; she turns round to face us out of her wall: a shrug, both palms out: that is how it is; and back to work
D11 = st.dur('S11'); E11, G11, B11 = 0.3, 0.48, 0.92   # her eyes on us; she faces us: the shrug; back to work
Z11 = ZS10; OM11 = [SX, LEGUP, round(Z11 + LAG10, 3)]
st.shot('S11', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('grand', [HX, 0, Z11], 0, 'stand', 'smug', keys=[k(0.0, look=WRT10), k(0.0, toon=UPT(face={'gy': 0.5}), toonDur=0.0), k(0.5, toon=UPT(face={'gy': 0.5, 'lid': 1}), toonDur=0.04), k(0.58, toon=UPT(face={'gy': 0.5}), toonDur=0.04)]),   # he has seen nothing: a blink
        act('ombre', OM11, 0, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon=UPS(), toonDur=0.0),                                                                          # with him, to the frame
            k(E11, look=[WX - 4.0, 2.0, Z11 + 0.4]), k(E11, toon=UPS(face={'eye': 0.5}), toonDur=0.06), k(E11, expr='surprised'),                                               # her eyes on us, wide
            k(G11, face=-90, turn=0.0), k(G11, look=None), k(G11, clip='shrug', blend=0.0), k(G11, toon=TALLF(sq=[1.0, 0.94, 0.03], scl={'handL': [1.5, 1.5, 1.5], 'handR': [1.5, 1.5, 1.5]}, face={'eye': 0.4, 'brow': 0.8}), toonDur=0.0),   # she turns to face us, in one frame (a flat thing has no three quarters): shoulders up, palms out
            k(G11 + 0.04, toon=TALLF(sq=[0.86, 1.06, 0.03], scl={'handL': [1.5, 1.5, 1.5], 'handR': [1.5, 1.5, 1.5]}, face={'eye': 0.4, 'brow': 0.8}), toonDur=0.08, toonEase='outBack'),
            k(G11 + 0.26, toon=TALLF(scl={'handL': [1.5, 1.5, 1.5], 'handR': [1.5, 1.5, 1.5]}, face={'eye': 0.4, 'brow': 0.8, 'lid': 1}), toonDur=0.04), k(G11 + 0.33, toon=TALLF(scl={'handL': [1.5, 1.5, 1.5], 'handR': [1.5, 1.5, 1.5]}, face={'eye': 0.4, 'brow': 0.8}), toonDur=0.04),   # a blink
            k(B11, face=0, turn=0.0), k(B11, clip='stand', blend=0.0), k(B11, expr='neutral'), k(B11, toon=UPS(sq=[0.03, 1.05, 0.86]), toonDur=0.0), k(B11 + 0.04, toon=UPS(settle=0.5), toonDur=0.08)])],   # and back to her place, her wrist up: at work
        props=[WALL(Z10 + 2.0), DIAL('dialt', [WRT10[0] - 0.08, WRT10[1] + 0.02, WRT10[2] + 0.02], 0.0), DIAL('dials', [SX - 0.012, WRS10[1] + 0.02, WRS10[2] + 0.03], 0.0, G11, shade=True), DIAL('dials2', [SX - 0.012, WRS10[1] + 0.02, WRS10[2] + 0.03], B11 + 0.03, shade=True)],
        cams=[cam(0.0, [round(WX - 5.6, 3), 1.4, round(Z11 + 0.42, 3)], [round(WX - 5.5, 3), 1.4, round(Z11 + 0.46, 3)], [WX, 2.0, round(Z11 + 0.42, 3)], [WX, 2.0, round(Z11 + 0.46, 3)], lens=44)])
st.cue('sfx:tick', 'S11', 0.05, 0.3); st.cue('pop', 'S11', E11, 0.3); st.cue('whoosh', 'S11', G11, 0.25, 0.1, 500, 1600); st.cue('whoosh', 'S11', B11, 0.2, 0.1, 500, 1600)

# 12: he hired one. A rail of shadows for hire stands against the wall (LOCATION D'OMBRES): five of them hang from hangers, each with its two white
#     eyes, and sway. He stands in front of its near end; his arm goes along the rail over their heads: the tall one: no; the wide one: no; and it
#     shoots to the far end, three metres long: the small one; a grin at us: this one; he unhooks her and brings her back at arm's length
D12 = st.dur('S12'); Z12 = -22.0; RK = [round(WX - 0.5, 3), 0, Z12]; RW12 = 2.2; NH12 = 4
hz12 = lambda i: round(Z12 - RW12 / 2 + 0.08 + (i + 0.5) * (RW12 - 0.16) / NH12, 3)   # the hanger number i along the rail (0: the far one, the small one; 3: the nearest to him)
ME12 = [7.8, 0, round(Z12 + 1.0, 3)]                 # he: beyond the near end of the rail, nearer to us than it: half the height of the frame (in the plane of the rail he was a third of it)
CAM12 = [round(RK[0] - 6.3, 3), 1.5, round(Z12 + 0.22, 3)]
HK12 = lambda i, y=2.07: [RK[0] - 0.1, y, hz12(i)]   # over a hanger: his arm runs along the rail, above the heads, on bare wall
PT12 = lambda i, **kw: {'hands': {'L': 'point', 'R': 'open'}, 'scl': {'handL': [1.5, 1.5, 1.5]}, 'reach': {'L': [*HK12(i), 1, 0.14]}, **kw}
P12A, P12B, P12C, T12, G12, U12, R12 = 0.0, 0.17, 0.34, 0.5, 0.74, 0.82, 1.06   # the tall one; the wide one; the small one; this one (to us); his hand on her hanger; she comes off; back at his side
st.shot('S12', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', ME12, 205, 'stand', 'neutral', keys=[k(0.0, look=HK12(3, 1.7)), k(0.0, toon=PT12(3, face={'brow': -0.3}), toonDur=0.0),
            k(P12B, toon=PT12(2, face={'brow': -0.4, 'gx': -0.4}), toonDur=0.08, toonEase='out'), k(P12B, look=HK12(2, 1.7)),                                  # no; no
            k(P12C - 0.04, toon=PT12(2, sq=[1.04, 0.96, 1.04], face={'brow': -0.2}), toonDur=0.04), k(P12C, toon=PT12(0, sq=[0.97, 1.03, 0.97], face={'brow': 0.9, 'eye': 0.3}), toonDur=0.1, toonEase='outBack'), k(P12C, look=HK12(0, 1.5)),   # and all the way: the small one
            k(T12, look=CAM12), k(T12 + 0.02, expr='happy'), k(T12 + 0.02, toon=PT12(0, face={'brow': 1}), toonDur=0.06),                                         # this one (to us)
            k(G12, toon={'hands': {'L': 'grip', 'R': 'open'}, 'scl': {'handL': [1.5, 1.5, 1.5]}, 'reach': {'L': [*HK12(0, 1.98), 1, 0.05]}, 'face': {'brow': 0.9}}, toonDur=0.06), k(G12, look=HK12(0, 1.6)),   # his hand on her hanger
            k(U12, toon={'hands': {'L': 'grip', 'R': 'open'}, 'scl': {'handL': [1.5, 1.5, 1.5]}, 'reach': {'L': [ME12[0] + 0.5, 1.9, round(ME12[2] - 0.75, 3), 1, 0.05]}, 'sq': [0.97, 1.04, 0.97], 'face': {'brow': 0.9}}, toonDur=round(R12 - U12, 3), toonEase='in')]),   # and the arm comes back, with her
        act('petite', [SX, 0.7, hz12(0)], -90, 'hangBar', 'happy', keys=[k(0.0, visible=False), k(0.0, look=None), k(0.0, toon={'sq': FLATZ}, toonDur=0.0), k(U12, visible=True),
            k(U12, to=[SX, 0.62, round(ME12[2] - 0.75, 3)], dur=round(R12 - U12, 3), clip='hangBar', then='hangBar', glide=True, ease='in', face=-90),
            k(R12 - 0.02, toon={'sq': [1.0, 1.0, 0.03], 'bend': {'spine': [0, 0, 0.3, 1, None]}}, toonDur=0.06)])],                                                # she swings at the end of his arm
        props=[WALL(Z12 + 2.0), P('rack', 'shadowRack', pos=RK, ry=-90, opts={'w': RW12, 'h': 2.0, 'kinds': ['kid', 'dogv', 'man', 'tall'], 'slim': True, 'manH': 1.36, 'signH': 0.5, 'pick': [[P12A, 3], [P12B, 2], [P12C + 0.03, 1], [P12C + 0.07, 0]], 'gone': [U12, 0]})],   # four, apart (five on two metres hung as one mass): the small one, a dog hung by its collar, a plain one, the tall one
        cams=[cam(0.0, CAM12, [CAM12[0] + 0.2, CAM12[1], CAM12[2]], [RK[0], 1.45, CAM12[2]], [RK[0], 1.45, CAM12[2]], lens=44)])
st.cue('sfx:stretch', 'S12', P12B, 0.2); st.cue('whoosh', 'S12', P12C, 0.3, 0.12, 400, 1800); st.cue('sfx:ding', 'S12', T12 + 0.02, 0.3); st.cue('sfx:twang', 'S12', U12, 0.3)

# 13: too small. He walks along the wall; behind him, on the wall, a shadow half his height trots to keep up, two steps for each of his, and waves at
#     us over her head; his eyes go back and down to her, then his head comes to us, and stays
D13 = st.dur('S13'); Z13 = -26.0; LAG13 = 0.76         # she trots well behind him (at his heels her wave landed on his hand: they held hands)
zh13 = lambda t: round(Z13 + 1.0 - VW * t, 3)
ZS14 = round(zh13(D13) - VW * 0.16, 3)                # where he stops in the next shot
STEN = round(ZS14 + LAG13 + 0.02, 3)                  # the stencil DÉFENSE D'AFFICHER on this stretch of wall: over the place where the fine will be stuck
WV13 = lambda t, i: [SX, 1.4, round(zh13(t) + LAG13 + (0.13 if i % 2 else -0.13), 3)]
st.shot('S13', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, zh13(0.0)], 180, 'walk', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, zh13(D13)], dur=D13, clip='walk', ease='linear', face=180, cruise=True),
            k(0.1, toon={'face': {'gx': 0.9, 'gy': 0.5, 'browL': 0.6}}, toonDur=0.08),                                                                   # his eyes go back and down to it
            k(0.34, look=[WX - 3.9, 1.45, zh13(0.6) - 0.3]), k(0.4, toon={'face': {'lid': 0.45, 'browL': 0.7}}, toonDur=0.08),                              # then his head comes to us: fifteen frames of it
            k(0.7, toon={'face': {'lid': 1, 'browL': 0.7}}, toonDur=0.04), k(0.78, toon={'face': {'lid': 0.45, 'browL': 0.7}}, toonDur=0.05)]),              # a slow blink
        act('petite', [SX, 0, round(zh13(0.0) + LAG13, 3)], 180, 'run', 'happy', params={'freq': 3.4, 'bounce': 0.8}, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(0.0, to=[SX, 0, round(zh13(D13) + LAG13, 3)], dur=D13, clip='run', params={'freq': 3.4, 'bounce': 0.8}, ease='linear', face=180, cruise=True),
            k(0.16, look=[WX - 4.0, 1.2, zh13(0.4)]), k(0.2, toon={'sq': FLATX, 'hands': {'R': 'spread'}, 'scl': {'handR': [1.5, 1.5, 1.5]}, 'reach': {'R': [*WV13(0.26, 0), 1, 0.08]}}, toonDur=0.08),   # her eyes on us: a wave, over her head
            *[k(0.28 + 0.1 * i, toon={'sq': FLATX, 'hands': {'R': 'spread'}, 'scl': {'handR': [1.5, 1.5, 1.5]}, 'reach': {'R': [*WV13(0.36 + 0.1 * i, i + 1), 1, 0.08]}}, toonDur=0.09) for i in range(6)]])],
        props=[WALL(Z13 + 0.5, stencil=STEN)],
        cams=[wallcam(0.0, zh13(0.0) + 0.27, zh13(D13) + 0.27, d=4.1, h=2.0, lh=1.25)])   # from a little above: she is small; and his head stays under the stencil
st.cue('sfx:squeak', 'S13', 0.0, 0.2)

# 14: he was fined. A whistle behind him: he stops dead, in the air for two frames, and turns round: a policeman has come up behind them, a hand up:
#     halt; on the wall the policeman has a proper shadow, cap and all, a hand up too; between the two men the small one looks up at it, and shrinks
D14 = st.dur('S14'); Z14 = zh13(D13); T14 = 0.16; TR14 = 0.44   # the whistle: he stops; he has turned round
ZC14 = round(ZS14 + 1.3, 3)                           # the policeman: behind him (at the right: the place of his own shadow is between them: nobody has to point across anybody)
PT14 = [SX, 0, round(ZS14 + LAG13, 3)]                # the small one: where she was when he stopped
HALT = lambda x, zc, **kw: {'scl': {'handR': [1.7, 1.7, 1.7]}, 'reach': {'R': [x, 2.3, round(zc - 0.5, 3), 1, 0.0]}, **kw}   # a hand up, high: over his cap (at shoulder height the hand of his shadow was behind his own body)
cam14 = lambda t, z0, z1, d=6.3, **kw: wallcam(t, z0, z1, d=d, h=1.4, lh=1.5, **kw)
st.shot('S14', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, Z14], 180, 'walk', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, ZS14], dur=T14, clip='walk', ease='linear', face=180, cruise='in'),
            k(T14, clip='stand', blend=0.06), k(T14, to=[HX, 0.16, ZS14], dur=0.06, glide=True, ease='out', face=180), k(T14 + 0.12, to=[HX, 0, ZS14], dur=0.08, glide=True, ease='in', face=180),   # the whistle: off the ground, two frames in the air
            k(T14 - 0.02, toon={'sq': [0.9, 1.14, 0.9], 'face': {'brow': 1, 'eye': 0.5}}, toonDur=0.06, toonEase='out'), k(T14, expr='surprised'),
            k(T14 + 0.18, toon={'sq': [1.08, 0.92, 1.08], 'face': {'brow': 1, 'eye': 0.45}}, toonDur=0.05), k(T14 + 0.24, toon={'settle': 0.6, 'face': {'brow': 1, 'eye': 0.4, 'gx': -0.9}}, toonDur=0.1),   # down, flat; his eyes go back first
            k(T14 + 0.3, look=[HX - 1.0, 1.6, ZC14]), k(TR14 - 0.1, face=-110, turn=0.1), k(TR14, face=-42, turn=0.12), k(TR14 + 0.04, expr='worried'),                                          # his head, then all of him: round, three quarters to us
            k(TR14 + 0.2, toon={'face': {'brow': 0.9, 'eye': 0.3, 'mouth': 'wavy'}}, toonDur=0.1), k(TR14 + 0.3, toon={'face': {'brow': 0.9, 'eye': 0.3, 'mouth': 'wavy', 'lid': 1}}, toonDur=0.04), k(TR14 + 0.37, toon={'face': {'brow': 0.9, 'eye': 0.3, 'mouth': 'wavy'}}, toonDur=0.04)]),
        act('petite', [SX, 0, round(Z14 + LAG13, 3)], 180, 'run', 'happy', params={'freq': 3.4, 'bounce': 0.8}, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(0.0, to=PT14, dur=T14, clip='run', params={'freq': 3.4, 'bounce': 0.8}, then='stand', ease='linear', face=180, cruise='in'),
            k(T14 + 0.02, toon={'sq': [0.03, 0.86, 1.15]}, toonDur=0.05), k(T14 + 0.1, toon={'sq': [0.03, 1.08, 0.94], 'settle': 0.5}, toonDur=0.08), k(T14 + 0.04, expr='surprised'),   # she stops too
            k(T14 + 0.2, face=0, turn=0.0), k(T14 + 0.22, look=[SX, 1.9, round(ZC14 + LAG, 3)]), k(T14 + 0.24, toon={'sq': [0.03, 1.14, 0.9], 'face': {'eye': 0.5}}, toonDur=0.08, toonEase='outBack'),   # she turns round (a flat thing turns in one frame) and looks up at the big one: on her toes
            k(T14 + 0.5, toon={'sq': [0.03, 0.82, 1.12], 'tremble': 1, 'face': {'eye': 0.5}}, toonDur=0.14)]),                                                                             # and shrinks
        act('flic', [HX, 0, round(ZC14 + 1.1, 3)], -142, 'stand', 'determined', keys=[k(0.0, look='mec'), k(0.0, to=[HX, 0, ZC14], dur=0.2, clip='walk', then='halt', ease='out', face=-142),
            k(0.1, clip='halt', blend=0.1), k(0.1, toon=HALT(HX - 0.12, ZC14, sq=[0.97, 1.05, 0.97]), toonDur=0.1, toonEase='outBack'), k(0.3, toon=HALT(HX - 0.12, ZC14, settle=0.5), toonDur=0.1),
            k(0.6, toon=HALT(HX - 0.12, ZC14, face={'browL': 0.6, 'lid': 1}), toonDur=0.04), k(0.67, toon=HALT(HX - 0.12, ZC14, face={'browL': 0.6}), toonDur=0.04)]),
        act('ombreflic', [SX, 0, round(ZC14 + 1.1 + LAG, 3)], 180, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0), k(0.0, to=[SX, 0, round(ZC14 + LAG, 3)], dur=0.2, clip='walk', then='halt', ease='out', face=180),
            k(0.1, clip='halt', blend=0.1), k(0.1, toon=HALT(SX, ZC14 + LAG, sq=[0.03, 1.05, 0.97]), toonDur=0.1, toonEase='outBack'), k(0.3, toon=HALT(SX, ZC14 + LAG, sq=FLATX, settle=0.5), toonDur=0.1)])],
        props=[WALL(Z13 + 0.5, stencil=STEN)],
        cams=[cam14(0.0, round(ZS14 + 0.98, 3), round(ZS14 + 0.9, 3))])
st.cue('sfx:whistle', 'S14', T14 - 0.04, 0.45); st.cue('sfx:squeak', 'S14', T14, 0.35); st.cue('thud', 'S14', T14 + 0.2, 0.25)

# 15: for walking without a shadow. The policeman points at the wall between them, where our man's shadow should be: nothing; our man's eyes follow
#     the finger; the flat hand goes down over the small one: « this high »: she shrinks under it; then a slip comes out of his pocket and his arm
#     sticks it on the wall over her head, where the head of a proper shadow would be: AMENDE, SANS OMBRE: right under DÉFENSE D'AFFICHER
D15 = st.dur('S15'); P15, M15, K15, SL15 = 0.08, 0.36, 0.62, 0.74   # he points; « this high »; the slip is out; the slap (early enough for the slip to be read alone for half a second)
FINE15 = [SX, 1.87, round(PT14[2] - 0.02, 3)]         # where the head of a proper shadow would be: over the small one
NOW15 = [round(SX - 0.06, 3), 1.7, round(PT14[2] + 0.05, 3)]   # the bare wall he points at
HI15 = [round(SX - 0.1, 3), 1.2, round(PT14[2] + 0.02, 3)]    # « this high »: a flat hand over her head
ARM = lambda p, hand='point', tip=0.14, **kw: {'hands': {'R': hand}, 'scl': {'handR': [1.5, 1.5, 1.5]}, 'reach': {'R': [*p, 1, tip]}, **kw}
ZC15 = round(ZS14 + 1.95, 3); XC15 = round(HX + 0.3, 3)   # the policeman in this shot: out of the frame at the right, nearer the wall: his arm comes into the picture, along the wall (from the road, an arm that points at the wall points away from us: a fist by his chin)
st.shot('S15', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, ZS14], -42, 'stand', 'worried', keys=[k(0.0, look=[HX - 1.0, 1.6, ZC14]), k(0.0, toon={'face': {'brow': 0.9, 'eye': 0.3, 'mouth': 'wavy'}}, toonDur=0.0),
            k(P15 + 0.06, toon={'face': {'gx': 0.9, 'brow': 0.8, 'eye': 0.35}}, toonDur=0.06), k(P15 + 0.14, look=NOW15),                                              # his eyes, then his head, follow the finger to the wall: nothing
            k(M15 + 0.02, toon={'face': {'gx': 0.6, 'gy': 0.8, 'brow': 0.7}}, toonDur=0.06), k(M15 + 0.1, look=[SX, 0.9, PT14[2]]),                                    # down to the small one
            k(SL15 + 0.04, toon={'sq': [1.05, 0.94, 1.05], 'face': {'brow': 1, 'eye': 0.45, 'jaw': 0.3}}, toonDur=0.05), k(SL15 + 0.04, look=FINE15),                   # the slap: he starts
            k(SL15 + 0.16, toon={'settle': 0.5, 'face': {'brow': 1, 'eye': 0.4, 'jaw': 0.3}}, toonDur=0.1),
            k(SL15 + 0.34, look=[WX - 5.0, 1.5, ZS14 + 0.3]), k(SL15 + 0.4, toon={'face': {'brow': 0.4, 'lid': 0.45}}, toonDur=0.1), k(SL15 + 0.4, expr='unimpressed'),   # then us
            k(SL15 + 0.56, toon={'face': {'brow': 0.4, 'lid': 1}}, toonDur=0.04), k(SL15 + 0.63, toon={'face': {'brow': 0.4, 'lid': 0.45}}, toonDur=0.04)]),
        act('petite', PT14, 0, 'stand', 'surprised', keys=[k(0.0, look=[SX, 1.9, round(ZC14 + LAG, 3)]), k(0.0, toon={'sq': [0.03, 0.82, 1.12], 'tremble': 1, 'face': {'eye': 0.5}}, toonDur=0.0),
            k(M15 - 0.02, toon={'sq': [0.03, 0.92, 1.05], 'face': {'eye': 0.5}}, toonDur=0.06), k(M15 + 0.04, look=None), k(M15 + 0.06, toon={'sq': [0.03, 0.66, 1.3], 'face': {'eye': 0.4}}, toonDur=0.08, toonEase='out'),   # the hand comes down over her: she flattens under it
            k(K15, toon={'sq': [0.03, 0.9, 1.06], 'settle': 0.5, 'face': {'eye': 0.5}}, toonDur=0.1),
            k(SL15, toon={'sq': [0.03, 0.6, 1.36], 'face': {'eye': 0.5}}, toonDur=0.04), k(SL15 + 0.1, toon={'sq': FLATX, 'settle': 0.6, 'face': {'eye': 0.5}}, toonDur=0.1), k(SL15 + 0.16, look=[SX, 2.4, PT14[2] - 0.3]),   # the slap over her head; she looks up at it
            k(SL15 + 0.44, toon={'sq': FLATX, 'face': {'eye': 0.5, 'lid': 1}}, toonDur=0.04), k(SL15 + 0.5, toon={'sq': FLATX, 'face': {'eye': 0.5}}, toonDur=0.04)]),
        act('flic', [XC15, 0, ZC15], 180, 'stand', 'determined', keys=[k(0.0, look='mec'), k(0.0, toon=ARM([XC15, 1.5, round(ZC15 - 0.5, 3)]), toonDur=0.0),
            k(P15, toon=ARM(NOW15, sq=[0.98, 1.03, 0.98], face={'browL': 0.7}), toonDur=0.1, toonEase='outBack'),                                                        # his arm comes into the picture: there: nothing
            k(P15 + 0.14, toon=ARM([NOW15[0], NOW15[1] + 0.06, NOW15[2]]), toonDur=0.05), k(P15 + 0.2, toon=ARM(NOW15), toonDur=0.05),                                   # a tap of the finger on the bare wall
            k(M15, toon=ARM(HI15, 'open', 0.06), toonDur=0.1, toonEase='out'),                                                                                              # « this high »
            k(M15 + 0.09, toon=ARM([HI15[0], HI15[1] - 0.08, HI15[2]], 'open', 0.06), toonDur=0.05), k(M15 + 0.15, toon=ARM(HI15, 'open', 0.06), toonDur=0.05),             # twice
            k(K15 - 0.1, toon=ARM([XC15, 1.6, round(ZC15 - 0.4, 3)], 'grip', 0.05), toonDur=0.08, toonEase='in'),                                                           # the arm goes out of the picture: to his pocket
            k(K15, toon=ARM([FINE15[0] - 0.05, FINE15[1] + 0.3, round(FINE15[2] + 0.75, 3)], 'spread', 0.08), toonDur=0.07, toonEase='out'),                              # and comes back with a slip
            k(SL15 - 0.04, toon=ARM([FINE15[0] - 0.05, FINE15[1], FINE15[2]], 'spread', 0.08, sq=[1.04, 0.97, 1.04]), toonDur=0.04, toonEase='in'),                        # onto the wall
            k(SL15 + 0.1, toon=ARM([FINE15[0] - 0.05, FINE15[1] - 0.02, round(FINE15[2] + 0.12, 3)], 'open', 0.08, settle=0.5), toonDur=0.06), k(SL15 + 0.2, toon=ARM([XC15, 1.5, round(ZC15 - 0.5, 3)], 'open', 0.08), toonDur=0.14, toonEase='in')])],   # a pat; and the arm goes home: the slip alone on the wall
        props=[WALL(Z13 + 0.5, stencil=STEN), P('fine', 'fineSlip', pos=[FINE15[0] - 0.05, FINE15[1] + 0.3, round(FINE15[2] + 1.6, 3)], ry=-90, opts={'w': 0.58}, keys=[k(0.0, visible=False), k(K15 - 0.06, visible=True),
                    k(K15 - 0.06, to=[FINE15[0] - 0.05, FINE15[1] + 0.3, round(FINE15[2] + 0.75, 3)], dur=0.13, ease='out'), k(SL15 - 0.04, to=FINE15, dur=0.04, ease='in')]),   # it comes in with his hand
               P('slap', 'impactStars', pos=[FINE15[0] - 0.02, FINE15[1], FINE15[2]], ry=-90, opts={'at': SL15, 'n': 6, 'r': 0.5, 'r0': 0.3, 'dur': 0.28, 'size': 0.07})],
        fx=[{'type': 'shake', 'at': SL15, 'dur': 0.14, 'amount': 0.018}],
        cams=[cam14(0.0, round(ZS14 + 0.64, 3), round(ZS14 + 0.62, 3), d=5.0)])   # he at the left, the wall where his shadow should be in the middle: the small one, and over her the place of the fine, under the stencil
st.cue('sfx:tick', 'S15', P15, 0.25); st.cue('sfx:slideDown', 'S15', M15, 0.25); st.cue('whoosh', 'S15', K15, 0.2, 0.1, 500, 1800); st.cue('clack', 'S15', SL15, 0.6)

# 16: yesterday she came back. He sits on the bench at the wall, slumped, his head in his hands' place: down; the small one sits on the wall beside
#     him, swinging her legs. His own shadow slides along the wall and stops beside the bench, hands on her hips, tapping a foot. His eyes go to the
#     side; his head; a grin; he is up, arms wide
D16 = st.dur('S16'); Z16 = -34.0; A16, E16, G16, UP16 = 0.42, 0.62, 0.9, 1.06
BEN16 = [round(WX - 0.47, 3), 0, Z16]; SEAT16 = [round(BEN16[0] + 0.05, 3), 0.02, round(Z16 - 0.2, 3)]
OM16 = [SX, 0, round(Z16 + 0.62, 3)]                 # where she stops on the wall: beside the bench, in clear view
PT16 = [SX, 0.5, round(Z16 - 0.84, 3)]               # the small one: on the wall at the other end of the bench (beside his head she was one mass with it)
SLUMP = {'bend': {'spine': [0.42, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}}
st.shot('S16', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', SEAT16, -90, 'sitSlump', 'sad', keys=[k(0.0, look=None), k(0.0, toon={**SLUMP, 'face': {'gy': 0.6, 'lid': 0.4}}, toonDur=0.0),                          # bent double: a real slump
            k(0.2, toon={**SLUMP, 'sq': [1.02, 0.97, 1.02], 'face': {'gy': 0.6, 'lid': 0.4, 'cheeks': 0.5}}, toonDur=0.14), k(0.36, toon={**SLUMP, 'face': {'gy': 0.6, 'lid': 0.4}}, toonDur=0.2),   # a sigh
            k(E16, toon={'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'gx': -0.9, 'brow': 0.6, 'eye': 0.3}}, toonDur=0.07), k(E16 + 0.1, look=OM16[:1] + [1.5] + OM16[2:]), k(E16 + 0.12, expr='surprised'),      # his eyes, then his head: her
            k(G16, look=[WX - 4.5, 1.4, Z16 + 0.2]), k(G16, expr='bigGrin'), k(G16, toon={'sq': [1.04, 0.95, 1.04], 'face': {'brow': 1}}, toonDur=0.08),                           # to us: a grin; he gathers himself
            k(UP16, clip='armsUp', blend=0.08), k(UP16, to=[SEAT16[0] - 0.25, 0, SEAT16[2]], dur=0.12, glide=True, ease='out', face=-90), k(UP16, toon={'sq': [0.9, 1.14, 0.9]}, toonDur=0.06, toonEase='out'),   # up, arms wide
            k(UP16 + 0.1, toon={'sq': [1.03, 0.97, 1.03], 'settle': 0.7}, toonDur=0.08)]),
        act('petite', PT16, -90, 'sitEdge', 'happy', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATZ}, toonDur=0.0), k(A16 + 0.1, look=OM16[:1] + [1.6] + OM16[2:]), k(A16 + 0.14, toon={'sq': [0.9, 1.1, 0.03], 'face': {'eye': 0.5}}, toonDur=0.08), k(A16 + 0.12, expr='surprised')]),   # she sees the big one: sits up straight
        act('ombre', [SX, 0, round(Z16 + 3.2, 3)], -90, 'handsOnHips', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': [1.0, 1.0, 0.03], 'bend': {'spine': [0, 0, -0.16, 1, None]}}, toonDur=0.0),
            k(0.0, to=OM16, dur=A16, clip='handsOnHips', glide=True, ease='out', face=-90),                                                               # she slides in along the wall, facing out of it, hands on her hips, leaning into it
            k(A16 - 0.04, toon={'sq': [1.06, 0.96, 0.03], 'bend': {'spine': [0, 0, 0.12, 1, None]}}, toonDur=0.06), k(A16 + 0.04, toon={'sq': FLATZ, 'settle': 0.5}, toonDur=0.1), k(A16 + 0.1, look=[SX, 1.2, Z16 - 0.2]),   # stops: her eyes on him
            *[x for i in range(4) for x in (k(A16 + 0.2 + 0.16 * i, toon={'sq': FLATZ, 'bend': {'shinL': [0.5, 0, 0, 1, None], 'spine': [0, 0, 0.05, 1, None]}}, toonDur=0.07), k(A16 + 0.28 + 0.16 * i, toon={'sq': FLATZ}, toonDur=0.06))],   # a foot taps: well?
            k(G16 + 0.1, toon={'sq': FLATZ, 'bend': {'neck': [0, 0, 0.25, 1, None]}}, toonDur=0.1)])],                                                      # her head on one side
        props=[WALL(Z16 + 2.0), P('bench', 'bench', pos=BEN16, ry=-90, opts={'w': 2.0})],
        cams=[wallcam(0.0, Z16 - 0.1, Z16 - 0.14, d=5.6, h=1.3, lh=1.4)])   # the small one at the left, he in the middle, the place where she stops at the right
st.cue('sfx:slideUp', 'S16', A16 - 0.2, 0.25); st.cue('pop', 'S16', G16, 0.3); st.cue('sfx:boing', 'S16', UP16, 0.3); [st.cue('sfx:tick', 'S16', A16 + 0.27 + 0.16 * i, 0.2) for i in range(4)]

# 17: with a lawyer. A second shadow slides in beside hers: a gown, the two white tabs of a barrister under the chin, a flat briefcase; when it has
#     stopped, a flat hand comes up between the two heads: stop. His arms come down. Then, closer on him: a lump goes down his throat; his pupils shake
D17 = st.dur('S17'); A17, H17, G17 = 0.2, 0.32, 0.6   # the lawyer is there; the hand; the gulp
AV17 = [SX, 0, round(OM16[2] + 0.95, 3)]              # the lawyer: beside her, a body's width of bare wall between them (at 0.72 they were one mass)
st.shot('S17', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [SEAT16[0] - 0.25, 0, SEAT16[2]], -90, 'armsUp', 'bigGrin', blink=0, keys=[k(0.0, look=[WX - 4.5, 1.4, Z16 + 0.2]),
            k(A17 - 0.02, toon={'face': {'gx': -0.9, 'brow': 0.5}}, toonDur=0.06), k(A17 + 0.08, look=AV17[:1] + [1.5] + AV17[2:]), k(A17 + 0.1, expr='worried'),            # his eyes, his head: who is that
            k(H17 + 0.02, clip='stand', blend=0.16), k(H17 + 0.02, toon={'sq': [1.03, 0.96, 1.03], 'bend': {'spine': [0.1, 0, 0, 0.97, None]}}, toonDur=0.16),               # the hand: his arms come down
            k(G17 - 0.06, look=[WX - 4.3, 1.45, Z16 + 0.1]), k(G17, toon={'face': {'gulp': 0.0, 'brow': 0.9, 'eye': 0.35, 'pupilShake': 1, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.04),
            k(G17 + 0.04, toon={'face': {'gulp': 1.0, 'brow': 0.9, 'eye': 0.35, 'pupilShake': 1, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.26, toonEase='linear'),              # to us: a lump goes down; his pupils shake
            k(G17 + 0.32, toon={'face': {'brow': 0.9, 'eye': 0.35, 'pupilShake': 0.6, 'tremble': 1, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.06)]),
        act('petite', PT16, -90, 'sitEdge', 'surprised', keys=[k(0.0, look=AV17[:1] + [1.6] + AV17[2:]), k(0.0, toon={'sq': FLATZ, 'face': {'eye': 0.5}}, toonDur=0.0),
            k(H17 + 0.06, to=[SX, 0, round(PT16[2] - 0.3, 3)], dur=0.1, clip='stand', glide=True, ease='in', face=180), k(H17 + 0.12, toon={'sq': FLATX}, toonDur=0.06),
            k(H17 + 0.16, to=[SX, 0, round(PT16[2] - 2.6, 3)], dur=0.5, clip='sneak', ease='in', face=180)]),                                                                # she slips off the wall and tiptoes out
        act('ombre', OM16, -90, 'handsOnHips', 'neutral', keys=[k(0.0, look=[SX, 1.2, Z16 - 0.2]), k(0.0, toon={'sq': FLATZ, 'bend': {'neck': [0, 0, 0.25, 1, None]}}, toonDur=0.0), k(A17 + 0.06, look=None), k(A17 + 0.06, toon={'sq': FLATZ}, toonDur=0.08), k(A17 + 0.06, clip='nod', blend=0.1)]),   # she nods to her counsel
        act('avocat', [SX, 0, round(AV17[2] + 1.6, 3)], -90, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': [1.0, 1.0, 0.03], 'bend': {'spine': [0, 0, -0.16, 1, None]}}, toonDur=0.0),
            k(0.0, to=AV17, dur=A17, clip='stand', glide=True, ease='out', face=-90), k(A17 - 0.04, toon={'sq': [1.06, 0.96, 0.03], 'bend': {'spine': [0, 0, 0.12, 1, None]}}, toonDur=0.06), k(A17 + 0.04, toon={'sq': FLATZ, 'settle': 0.5}, toonDur=0.08),   # she slides in the same way
            k(H17, toon={'sq': [1.0, 1.04, 0.03], 'hands': {'R': 'spread'}, 'scl': {'handR': [1.8, 1.8, 1.8]}, 'reach': {'R': [SX, 2.0, round(AV17[2] - 0.47, 3), 1, 0.1]}}, toonDur=0.08, toonEase='outBack'),   # a flat hand: stop: up between their two heads, on bare wall
            k(H17 + 0.06, look=[SX, 1.2, Z16 - 0.2])])],
        props=[WALL(Z16 + 2.0), P('bench', 'bench', pos=BEN16, ry=-90, opts={'w': 2.0}),
               P('rabat', 'rabat', on={'actor': 'avocat', 'joint': 'neck', 'offset': [0, 0.03, 0.6]}, opts={'s': 2.0}),   # (she is flattened thirty times: half a metre in front of her neck is 2 cm)
               P('case', 'briefcase', on={'actor': 'avocat', 'hand': 'L', 'offset': [0, -0.2, 0]}, silhouette=SHADE, scale=1.1)],   # a flat shade like her (it was a coloured thing among shadows)
        cams=[wallcam(0.0, Z16 + 0.62, Z16 + 0.62, d=6.0, h=1.3, lh=1.5), glide([wallcam(G17 - 0.06, Z16 - 0.42, Z16 - 0.45, d=3.1, h=1.4, lh=1.45)], 0.22)])   # him, her, her counsel, whole; then in on him for the gulp (she is out of that frame: its edge cut her through an eye)
st.cue('sfx:slideUp', 'S17', 0.0, 0.25); st.cue('pop', 'S17', H17, 0.35); st.cue('sfx:gasp', 'S17', G17, 0.25)
st.card('S17', 'AVEC UN AVOCAT')

# 18: the judge has ruled. He looks at us over his glasses; his arm goes up over his wig, the gavel at the end of it: a breath: and comes down on
#     the block: the wig hops, the glasses slide down his nose
D18 = st.dur('S18'); W18, HIT18 = 0.3, 0.56            # the gavel is up; it lands
COURT = {'handle': 'TRIBUNAL', 'windowX': -1.5, 'chairW': 1.2, 'chairH': 2.75, 'chairX': 0.15, 'benchGlow': '#33312B'}   # (a bench less lit than the series': white captions on cream did not read)
JG = [-0.35, -0.3, -14.0]; BLK = [0.12, 1.18, -13.3]  # the judge; the block on his bench
GAV = [round(BLK[0] - 0.47, 3), 1.33, BLK[2]]         # the gavel after the blow: its head on the block, its handle toward his hand
GRIP18 = {'hands': {'L': 'grip'}, 'reach': {'L': [GAV[0] + 0.04, GAV[1], GAV[2] - 0.02, 1, 0.05]}}
UP18 = lambda y=2.25, **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [0.1, y, -13.6, 1, 0.05]}, **kw}   # his fist, high beside his wig, on the side of the block: the gavel over it (the clip raises it behind his head: from the front nothing went up)   # his fist on the handle (it lay across the picture with no hand on it)
CAM18 = lambda t, **kw: cam(t, [0.3, 1.72, -10.7], [0.27, 1.72, -10.95], [-0.02, 1.68, -14.0], [-0.02, 1.68, -14.0], lens=45, **kw)   # further back and higher than the series' judge shot: the raised gavel, his face and the block on the bench in one frame (the mallet's head and the plate were cut by its edge)
st.shot('S18', 'replicaCourt', setOpts=COURT, actors=[
        act('juge', JG, -35, 'gavelStrikeL', 'determined', params={'hit': HIT18}, blink=0, keys=[k(0.0, look=[0.3, 1.72, -10.7]), k(0.0, toon=UP18(1.6, face={'browL': 0.7, 'lid': 0.3}), toonDur=0.0),
            k(0.08, toon=UP18(2.34, sq=[0.96, 1.07, 0.96], face={'brow': -0.6, 'lid': 0.2, 'cheeks': 0.6}), toonDur=round(W18 - 0.08, 3), toonEase='out'),            # up on a breath
            k(W18 + 0.04, toon=UP18(2.25, sq=[0.97, 1.05, 0.97], face={'brow': -0.8, 'lid': 0.2, 'cheeks': 0.6}), toonDur=0.1),                                        # the hold at the top: six frames
            k(HIT18 - 0.05, toon={'sq': [1.06, 0.93, 1.06], 'scl': {'head': [1.1, 0.86, 1.1]}, **GRIP18, 'face': {'brow': -0.9, 'eye': 0.3, 'jaw': 0.3}}, toonDur=0.05, toonEase='in'),   # the blow: his head sinks into his collar
            k(HIT18 + 0.06, toon={'sq': [0.98, 1.04, 0.98], 'scl': {'head': [0.95, 1.1, 0.95]}, **GRIP18, 'face': {'brow': -0.7, 'lid': 0.3}}, toonDur=0.07, toonEase='out'),             # and springs back: the wig hops
            k(HIT18 + 0.16, toon={**GRIP18, 'settle': 0.6, 'face': {'browL': 0.8, 'lid': 0.35, 'mouth': 'smirk'}}, toonDur=0.1)])],
        props=[P('specs', 'glasses', on={'actor': 'juge', 'joint': 'head', 'offset': [0.02, 0.17, 0.15]}, opts={'r': 0.042, 'dx': 0.07},
                 keys=[k(HIT18, attach='juge', joint='head', offset=[0.02, 0.1, 0.17], dur=0.08, ease='outBack')]),                                                   # they slide down his nose at the blow
               P('gavelUp', 'gavel', on={'actor': 'juge', 'hand': 'L'}, keys=[k(0.0, visible=True), k(round(HIT18 - 0.02, 3), visible=False)]),
               P('gavel', 'gavel', pos=GAV, rot=[0, 0, -1.5708], keys=[k(0.0, visible=False), k(round(HIT18 - 0.02, 3), visible=True), k(HIT18, squash=[1.25, 0.7, 1.25], dur=0.2)]),
               P('block', 'soundBlock', pos=BLK), P('hit', 'impactStars', pos=[BLK[0], BLK[1] + 0.16, BLK[2] + 0.12], opts={'at': HIT18, 'n': 6, 'r': 0.34, 'r0': 0.14, 'dur': 0.26, 'size': 0.06})],
        fx=[{'type': 'shake', 'at': HIT18, 'dur': 0.18, 'amount': 0.02}],
        cams=[CAM18(0.0)])
st.cue('whoosh', 'S18', HIT18 - 0.16, 0.25, 0.14, 300, 1400); st.cue('clack', 'S18', HIT18, 0.7)

# 19: shared custody. A calendar drops over the front of his bench: GARDE ALTERNÉE: one row of seven days: a day for him (white), a day for her (the
#     violet of her shade); a red frame hops from day to day; over the edge of the bench the judge's eyes follow it; then they come to us
D19 = st.dur('S19'); CAL19 = [-0.1, 0.86, -12.24]; H19 = 0.24; N19 = 7
st.shot('S19', 'replicaCourt', setOpts=COURT,
        actors=[act('juge', JG, -35, 'stand', 'smug', keys=[k(0.0, look=[CAL19[0], 0.2, -11.6]), k(0.0, toon={'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'gy': 0.8}}, toonDur=0.0),
            *[k(round(H19 + 0.12 * i, 3), toon={'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'gy': 0.8, 'gx': round(0.6 - 0.2 * i, 2)}}, toonDur=0.05) for i in range(N19)],
            k(1.04, look=[0.0, 1.2, -9.6]), k(1.06, toon={'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': {'browL': 0.6, 'lid': 0.4}}, toonDur=0.1)])],
        props=[P('cal', 'custodyCalendar', pos=[CAL19[0], CAL19[1] + 1.1, CAL19[2]], opts={'w': 1.02, 'rows': 1, 'mark': [[round(H19 + 0.12 * i, 3), i] for i in range(N19)]}, keys=[k(0.0, to=CAL19, dur=0.14, ease='in'), k(0.14, to=[CAL19[0], CAL19[1] + 0.07, CAL19[2]], dur=0.06, ease='out'), k(0.2, to=CAL19, dur=0.06, ease='in')]),
               P('specs', 'glasses', on={'actor': 'juge', 'joint': 'head', 'offset': [0.02, 0.1, 0.17]}, opts={'r': 0.042, 'dx': 0.07}),
               P('gavel', 'gavel', pos=[GAV[0], 1.24, GAV[2]], rot=[0, 0, -1.5708]), P('block', 'soundBlock', pos=[BLK[0], 1.16, BLK[2]])],   # the gavel lies on the bench (in the air at his neck, its handle ended in his face)
        cams=[cam(0.0, [0.0, 1.0, -9.7], [0.0, 1.0, -9.9], [-0.1, 1.08, -13.0], [-0.1, 1.08, -13.0], lens=44)])
st.cue('thud', 'S19', 0.14, 0.45); [st.cue('sfx:tick', 'S19', round(H19 + 0.12 * i, 3), 0.3) for i in range(N19)]

# ---- his bedroom, an even day. He sleeps in his bed, in his suit; his shadow lies on the floor beside the bed, flat
ROOM = {'poster': 'JOUR\nPAIR', 'posterBg': '#1B2F6B', 'posterFg': '#F4F1E8', 'blanket': '#E9D9A6', 'clutter': False}   # a pale blanket: a navy man who goes flat on it must be seen (on the blue one he was navy lines on blue)
BEDX, BEDZ = -2.6, -1.9                              # the bed of the set: along Z, its pillow at the wall end (-Z)
INBED = [BEDX, 0.62, round(BEDZ + 0.1, 3)]            # him, on the bed, on his back, his head at the pillow
UP21 = [-1.4, 0, -0.2]                               # where she stands when she is up: at the foot corner of the bed: beside him, not in front of him
ONFLOOR = [UP21[0], 0.0, round(UP21[2] - 1.03, 3)]   # her, on the floor beside the bed, on her back: her feet where she will stand (lying, an actor's place is the middle of the body: the feet are 1.03 m along the facing)
FLOORFLAT = [1, 1, 0.05]                              # lying on the back, flat on the floor (the body's own depth is up)
HEAD20 = [ONFLOOR[0], 0.05, round(ONFLOOR[2] - 0.95, 3)]   # her head on the floor
CLOCK20 = [round(ONFLOOR[0] - 0.5, 3), 0.0, round(ONFLOOR[2] - 0.7, 3)]   # the alarm clock: on the floor between the bed and her shoulder
CAL20 = P('cal', 'custodyCalendar', pos=[-1.55, 1.5, -2.97], opts={'w': 0.56, 'big': {'day': 2, 'who': 'ELLE'}})   # the day of the judgment, over the bed: one big framed 2: ELLE (the whole calendar was a centimetre of lettering)
# 20: on even days. From over the foot of the bed: the alarm clock rings and hops; he frowns in his sleep; on the floor two white eyes open
D20 = st.dur('S20'); R20 = 0.05; CAM20P = [-0.3, 2.55, 0.1]
LOOK20, LENS20, _w20 = fit(CAM20P, {'headA': [HEAD20[0] + 0.25, 0.05, round(HEAD20[2] - 0.27, 3)], 'headB': [HEAD20[0] - 0.25, 0.05, round(HEAD20[2] + 0.33, 3)], 'sh': [HEAD20[0] + 0.3, 0.05, round(HEAD20[2] + 0.58, 3)],
                                    'clock': [CLOCK20[0] - 0.12, 0.32, CLOCK20[2]], 'his': [BEDX, 0.95, round(BEDZ - 0.85, 3)], 'calT': [-1.55, 1.84, -2.97]}, margin=0.05, top=0.05, bottom=0.75)   # her head and shoulders, the clock, his head on the pillow, the big 2: her eyes must be read on a phone (with the whole of her in the frame they were two points)
st.shot('S20', 'chambre', setOpts=ROOM, actors=[
        act('mec', INBED, 0, 'lieBack', 'sleepy', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 1}}, toonDur=0.0),
            k(R20 + 0.08, toon={'face': {'lid': 1, 'brow': -0.8, 'mouth': 'clench'}, 'bend': {'spine': [0, 0.2, 0, 1, None]}}, toonDur=0.1)]),                         # he frowns in his sleep
        act('ombre3', ONFLOOR, 0, 'lieBack', 'sleepy', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLOORFLAT, 'face': {'lid': 1}}, toonDur=0.0),
            k(R20 + 0.16, toon={'sq': FLOORFLAT, 'face': {'eye': 0.55}}, toonDur=0.04), k(R20 + 0.16, expr='surprised')])],                                          # her eyes open: two white eyes on the floor
        props=[P('clock', 'alarmClock', pos=CLOCK20, ry=20, scale=1.0, opts={'time': '07:00', 'ringAt': R20, 'button': 'ARRÊT'}), CAL20],
        cams=[cam(0.0, CAM20P, [CAM20P[0], CAM20P[1] - 0.1, CAM20P[2] - 0.08], LOOK20, LOOK20, lens=LENS20 or 50)])
st.cue('sfx:ding', 'S20', R20, 0.5); st.cue('sfx:ding', 'S20', R20 + 0.26, 0.45)

# 21: she is the one who gets up. Seen from the foot of the bed, three quarters. One: a flat arm slaps the clock; she peels off the floor, thin as
#     paper, tips up on her feet, and fills out with a pop: a body; her white eyes come to us and stay. Two: she stretches, both arms up (his stretch
#     of the other morning) and he, on the bed behind her, goes flat as a sheet, lifts, hangs over the edge of the bed, and slips down to the floor
#     at her feet: the shadow of a shadow
D21 = st.dur('S21'); H21, P21, U21, I21, E21, X21, F21, HG21, FL21, LD21 = 0.07, 0.16, 0.4, 0.46, 0.6, 0.86, 0.9, 1.06, 1.2, 1.38
DN21 = [round(UP21[0] - 0.02, 3), 0.0, round(UP21[2] - 0.12 - 1.03, 3)]   # where he ends: on the floor, his feet at her heels
CAM21P = [2.6, 1.9, 1.6]
HANG21 = [round(BEDX + 0.75, 3), 0.42, round(BEDZ + 0.2, 3)]   # where he hangs in the air: over the edge of the bed, between it and her
LOOK21, LENS21, _w21 = fit(CAM21P, {'his': [BEDX, 0.95, round(BEDZ - 0.85, 3)], 'foot': [BEDX - 0.3, 0.6, round(BEDZ + 1.0, 3)], 'top': [UP21[0], 2.8, UP21[2]], 'hang': [HANG21[0], 2.7, HANG21[2]], 'fl': [UP21[0] + 0.45, 0.0, UP21[2] + 0.2], 'dn': [DN21[0], 0.05, round(DN21[2] - 0.95, 3)]},
                                    margin=0.06, top=0.06, bottom=0.9)
UPARMS = lambda dy=0.0, **kw: {'hands': {'L': 'spread', 'R': 'spread'}, 'reach': {'L': [UP21[0] + 0.3, 2.55 + dy, UP21[2], 1, 0.08], 'R': [UP21[0] - 0.3, 2.55 + dy, UP21[2], 1, 0.08]}, **kw}
st.shot('S21', 'chambre', setOpts=ROOM, actors=[
        act('ombre3', ONFLOOR, 0, 'lieBack', 'surprised', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLOORFLAT, 'face': {'eye': 0.55}}, toonDur=0.0),
            k(H21 - 0.07, toon={'sq': FLOORFLAT, 'hands': {'R': 'open'}, 'reach': {'R': [CLOCK20[0], 0.42, CLOCK20[2] + 0.05, 1, 0.08]}, 'face': {'eye': 0.55}}, toonDur=0.07, toonEase='in'),   # a flat arm, on the clock
            k(H21 + 0.05, toon={'sq': FLOORFLAT, 'face': {'eye': 0.55}}, toonDur=0.06),
            k(P21, to=UP21, dur=round(U21 - P21, 3), clip='stand', then='stand', glide=True, ease='inOut', face=0, blend=round(U21 - P21, 3)),                              # she peels off the floor and tips up on her feet: thin as paper
            k(P21, toon={'sq': [1, 1.04, 0.05], 'face': {'eye': 0.55}}, toonDur=0.1), k(U21, toon={'sq': [1.05, 0.97, 0.05], 'face': {'eye': 0.55}}, toonDur=0.05),         # upright: a cut-out
            k(I21, toon={'sq': [1.2, 0.9, 1.3], 'face': {'eye': 0.55}}, toonDur=0.05, toonEase='out'),                                                                       # and fills out: a pop
            k(I21 + 0.06, toon={'sq': [0.94, 1.07, 0.92], 'face': {'eye': 0.5}}, toonDur=0.06), k(I21 + 0.12, toon={'settle': 0.6, 'face': {'eye': 0.5}}, toonDur=0.08),
            k(E21 - 0.08, look=CAM21P), k(E21 + 0.12, toon={'face': {'eye': 0.5, 'lid': 1}}, toonDur=0.04), k(E21 + 0.18, toon={'face': {'eye': 0.5}}, toonDur=0.04),        # her eyes on us, eight frames; a blink
            k(X21 - 0.04, look=None), k(X21 - 0.04, expr='yawn'), k(X21, toon=UPARMS(-0.3, sq=[1.04, 0.95, 1.04]), toonDur=0.08, toonEase='in'),
            k(X21 + 0.08, toon=UPARMS(0.05, sq=[0.93, 1.1, 0.93], bend={'spine': [-0.18, 0, 0, 1.06, None]}), toonDur=0.14, toonEase='out'),                                  # she stretches: on her toes
            k(X21 + 0.34, toon={'sq': [1.03, 0.97, 1.03], 'settle': 0.5}, toonDur=0.12), k(X21 + 0.36, expr='neutral'),
            k(LD21 - 0.06, look=[DN21[0], 0.0, round(DN21[2] - 0.6, 3)]), k(LD21 + 0.02, toon={'face': {'eye': 0.5}}, toonDur=0.06)]),                                         # her eyes go down to what has landed at her feet
        act('mec', INBED, 0, 'lieBack', 'sleepy', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 1, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.0),
            k(F21, toon={'sq': [1.1, 1.05, 0.06], 'face': {'eye': 0.45, 'brow': 1}}, toonDur=0.1, toonEase='in'), k(F21 + 0.02, expr='surprised'),                            # he goes flat: his eyes open
            k(F21 + 0.08, to=HANG21, dur=round(HG21 - F21 - 0.08, 3), clip='stand', then='stand', glide=True, ease='out', face=58, blend=0.1),                               # he comes off the bed and stands up in the air, a sheet of paper, his flat front to us (lying flat in the air he was a line seen from its edge)
            k(F21 + 0.1, toon={'sq': [1.05, 1.08, 0.05], 'face': {'eye': 0.5, 'brow': 1, 'jaw': 0.4}}, toonDur=0.08),
            k(HG21, toon={'sq': [1.08, 1.02, 0.05], 'tremble': 1, 'bend': {'spine': [0, 0.3, 0, 1, None], 'neck': [0, -0.3, 0, 1, None]}, 'face': {'eye': 0.5, 'brow': 1, 'jaw': 0.4, 'gy': 0.8, 'pupilShake': 1}}, toonDur=0.06),   # and hangs there, four frames, bowing like a sheet of paper: his eyes go down: the floor
            k(HG21 + 0.07, toon={'sq': [1.08, 1.02, 0.05], 'tremble': 1, 'bend': {'spine': [0, -0.26, 0, 1, None], 'neck': [0, 0.26, 0, 1, None]}, 'face': {'eye': 0.5, 'brow': 1, 'jaw': 0.4, 'gy': 0.8, 'pupilShake': 1}}, toonDur=0.06),
            k(FL21, to=DN21, dur=round(LD21 - FL21, 3), clip='lieBack', then='lieBack', glide=True, ease='in', face=0, blend=0.16),                                              # then he slides down, and lies
            k(FL21 + 0.03, toon={'sq': [1.0, 1.16, 0.05], 'face': {'eye': 0.45, 'brow': 1}}, toonDur=0.08),
            k(LD21, toon={'sq': [1.16, 1.05, 0.04], 'face': {'brow': 0.6, 'eye': 0.3}}, toonDur=0.03), k(LD21 + 0.05, toon={'sq': FLOORFLAT, 'settle': 0.4, 'face': {'brow': 0.3, 'lid': 0.4}}, toonDur=0.06), k(LD21 + 0.05, expr='unimpressed')])],
        props=[P('clock', 'alarmClock', pos=CLOCK20, ry=20, scale=1.0, opts={'time': '07:00', 'ringAt': 0.0, 'stopAt': H21, 'button': 'ARRÊT'}), CAL20],
        cams=[cam(0.0, CAM21P, [CAM21P[0] - 0.12, CAM21P[1], CAM21P[2] - 0.08], LOOK21, LOOK21, lens=LENS21 or 50)])
st.cue('clack', 'S21', H21, 0.5); st.cue('sfx:slideUp', 'S21', P21, 0.3); st.cue('pop', 'S21', I21, 0.4); st.cue('sfx:stretch', 'S21', X21, 0.3); st.cue('sfx:slideDownSlow', 'S21', FL21, 0.3); st.cue('thud', 'S21', LD21, 0.2)

# ---- the street again: she walks, upright, a body of shade with two white eyes; he follows
MP = {'expr': 'neutral'}                              # her march: the clip's own face is « proud »: eyes shut: on a shadow, no eyes at all
V23 = round(VW * 1.15, 3); DRAG = 1.2                # her pace; his hips, that far behind her: his soles at her heels
FLAT23 = [1.06, 1.0, 0.1]
Z22 = round(ZP1 + 1.25, 3)
zs22 = lambda t: round(Z22 - V23 * t, 3)             # her z
JNT = lambda z0, raised=(): P('joints', 'pavingJoints', pos=[round(HX - 0.35, 3), 0, z0], opts={'w': 2.5, 'step': 0.45, 'len': 14, 'raised': list(raised)})
ZJ22 = round(zs22(st.dur('S22')) - 0.04 + 8 * 0.45, 3)   # the joints of this pavement: the ninth slab stands proud: his heels meet it a moment after the next cut
# 22: he follows. The wall of the first shot: she comes along it where he walked, head high, a body now: she passes in front of the bollard, which
#     has its shadow on the wall: she has none: behind her the wall is bare. Her white eyes come to us and stay. At her heels, on the pavement: a
#     long flat thing in a navy suit
D22 = st.dur('S22')
st.shot('S22', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('ombre3', [HX, 0, zs22(0.0)], 180, 'marchPomp', 'neutral', params=MP, keys=[k(0.0, look=None), k(0.0, to=[HX, 0, zs22(D22)], dur=D22, clip='marchPomp', params=MP, ease='linear', face=180, cruise=True),
            k(0.0, toon={'face': {'eye': 0.4, 'brow': 0.3}}, toonDur=0.0),
            k(0.52, look=[WX - 4.7, 1.5, round(zs22(0.9) - 0.3, 3)]),                                                                                 # her white eyes come to us, as his did: and stay
            k(0.96, toon={'face': {'eye': 0.4, 'brow': 0.3, 'lid': 1}}, toonDur=0.04), k(1.03, toon={'face': {'eye': 0.4, 'brow': 0.5}}, toonDur=0.04)]),   # a blink
        act('mec', [HX, 0, round(zs22(0.0) + DRAG, 3)], 180, 'lieBack', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLAT23, 'face': {'lid': 0.4}}, toonDur=0.0),
            k(0.0, to=[HX, 0, round(zs22(D22) + DRAG, 3)], dur=D22, clip='lieBack', then='lieBack', glide=True, ease='linear', face=180, cruise=True)])],
        props=[WALL1(), *POTELET(ZP1), JNT(ZJ22, [8])],
        cams=[wallcam(0.0, round(zs22(0.0) - 0.3, 3), round(zs22(D22) - 0.3, 3), d=4.7, h=1.95, lh=1.35)])   # she in the right half of the frame, room before her; of him: his shins, on the ground at the right edge
st.cue('whoosh', 'S22', 0.0, 0.2, 0.4, 300, 1200)

def topcam(t0, t1, zf, x0, H=3.6, tilt=8.0, zoff=0.02, lens=44, **kw):
    # from straight above, almost: the way a shadow on the ground is seen. The bottom edge of the frame runs through her heels: a camera this steep
    # sees nothing of a body that stands at the foot of its frame but its feet (lower and further ahead she was a dark mass over a third of the
    # picture, on top of him). He lies up the frame from her heels, his head at the top, his face the right way up
    def at(t):
        zb = zf(t) + zoff; zc = zb + H * math.tan(math.radians(lens / 2 - tilt)); zl = zc + H * math.tan(math.radians(tilt))
        return [x0, H, round(zc, 3)], [x0, 0.0, round(zl, 3)]
    a, la = at(t0); b, lb = at(t1)
    return cam(t0, a, b, la, lb, lens=lens, ease='linear', **kw)
# 23: on the ground. From above: two heels at the foot of the frame, and he, flat, on his back, sliding after them feet first, looking at the sky;
#     the joints of the pavement go by; one slab stands proud: his heels hit it and the bump runs up him: hips, head: his head hangs two frames
D23 = st.dur('S23'); B23 = 0.12                         # his heels meet the slab
zs23 = lambda t: round(zs22(D22) - V23 * t, 3)
BUMP = lambda a, b, c, **kw: {'sq': [1.06, 1.0, 0.1 + 0.07 * b], 'bend': {'shinL': [-0.5 * a, 0, 0, 1, None], 'shinR': [-0.5 * a, 0, 0, 1, None], 'spine': [-0.4 * b, 0, 0, 1, None], 'neck': [0.55 * c, 0, 0, 1, None]}, **kw}   # heels up; hips up; head up
st.shot('S23', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('ombre3', [HX, 0, zs23(0.0)], 180, 'marchPomp', 'neutral', params=MP, keys=[k(0.0, look=None), k(0.0, to=[HX, 0, zs23(D23)], dur=D23, clip='marchPomp', params=MP, ease='linear', face=180, cruise=True)]),
        act('mec', [HX, 0, round(zs23(0.0) + DRAG, 3)], 180, 'lieBack', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLAT23, 'face': {'lid': 0.4}}, toonDur=0.0),
            k(0.0, to=[HX, 0, round(zs23(D23) + DRAG, 3)], dur=D23, clip='lieBack', then='lieBack', glide=True, ease='linear', face=180, cruise=True),
            k(B23, toon=BUMP(1, 0, 0, face={'eye': 0.3, 'brow': 0.6}), toonDur=0.04, toonEase='out'),                                                   # his heels
            k(B23 + 0.12, toon=BUMP(0.2, 1, 0, face={'eye': 0.35, 'brow': 0.8}), toonDur=0.06, toonEase='out'),                                         # his hips
            k(B23 + 0.24, toon=BUMP(0, 0.2, 1, scl={'head': [0.94, 1.12, 0.94]}, face={'eye': 0.45, 'brow': 1, 'jaw': 0.3}), toonDur=0.06, toonEase='out'), k(B23 + 0.24, expr='surprised'),   # his head: off the ground, two frames
            k(B23 + 0.36, toon={'sq': [1.1, 1.0, 0.08], 'scl': {'head': [1.1, 0.88, 1.1]}, 'face': {'eye': 0.3, 'brow': 0.4}}, toonDur=0.04, toonEase='in'),                                  # and down: flat
            k(B23 + 0.44, toon={'sq': FLAT23, 'settle': 0.5, 'face': {'lid': 0.4, 'gx': 0.0, 'gy': 0.0}}, toonDur=0.08), k(B23 + 0.44, expr='unimpressed')])],                               # his eyes come to us
        props=[WALL1(), JNT(ZJ22, [8])],
        cams=[topcam(0.0, D23, zs23, HX)])
st.cue('sfx:slideDownSlow', 'S23', 0.0, 0.25); st.cue('thud', 'S23', B23, 0.25); st.cue('thud', 'S23', B23 + 0.12, 0.25); st.cue('clack', 'S23', B23 + 0.36, 0.3)

# 24: he says tarmac is fine. She has taken to the road: the dashes of its line go by; he slides after her on the smooth tarmac, his hands behind
#     his head, an ankle on a knee, a foot that beats time; a slow blink; on « ça va » an arm comes out and a thumb comes up, big
D24 = st.dur('S24'); RX = 3.4; Z24 = -8.0; TH24 = round(26.79 - st.SH['S24'][0], 3)
zs24 = lambda t: round(Z24 - V23 * t, 3)
TH = lambda zf, t, dy=0.0, dx=0.0: [round(RX - 0.33 + dx, 3), 0.42 + dy, round(zf(t) + 0.02 + 1.95, 3), 1, 0.06]   # his thumb: held up over the tarmac beside his shoulder, at the right of the picture
BEAT = lambda t0, t1: [k(round(t0 + 0.15 * i, 3), toon={'sq': FLAT23, 'bend': {'shinL': [0.35 if i % 2 else -0.1, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.12) for i in range(int((t1 - t0) / 0.15))]
st.shot('S24', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('ombre3', [RX, 0, zs24(0.0)], 180, 'marchPomp', 'neutral', params=MP, keys=[k(0.0, look=None), k(0.0, to=[RX, 0, zs24(D24)], dur=D24, clip='marchPomp', params=MP, ease='linear', face=180, cruise=True)]),
        act('mec', [RX, 0, round(zs24(0.0) + DRAG, 3)], 180, 'lieRelax', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLAT23, 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.0, to=[RX, 0, round(zs24(D24) + DRAG, 3)], dur=D24, clip='lieRelax', then='lieRelax', glide=True, ease='linear', face=180, cruise=True),
            *BEAT(0.1, 0.52), k(0.56, toon={'sq': FLAT23, 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.06), k(0.72, toon={'sq': FLAT23, 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.06), *BEAT(0.78, TH24 - 0.14),   # his foot beats time; a slow blink
            k(TH24 - 0.12, toon={'sq': FLAT23, 'hands': {'L': 'thumbUp'}, 'scl': {'handL': [2.1, 2.1, 2.1]}, 'reach': {'L': TH(zs24, TH24, 0.1)}, 'face': {'lid': 0.3, 'brow': 0.5, 'mouth': 'smirk'}}, toonDur=0.12, toonEase='outBack'),   # a thumb: it is fine
            *[k(round(TH24 + 0.12 * i, 3), toon={'sq': FLAT23, 'hands': {'L': 'thumbUp'}, 'scl': {'handL': [2.1, 2.1, 2.1]}, 'reach': {'L': TH(zs24, TH24 + 0.12 * i, 0.06 if i % 2 else 0.0)}, 'face': {'lid': 0.3, 'brow': 0.5, 'mouth': 'smirk'}}, toonDur=0.11) for i in range(1, int((D24 - TH24) / 0.12) + 1)]])],
        props=[P('dash', 'roadDashes', pos=[round(RX + 0.62, 3), 0, round(Z24 + 4.0, 3)], opts={'len': 16, 'period': 1.5, 'dash': 0.8})],
        cams=[topcam(0.0, D24, zs24, RX)])
st.cue('whoosh', 'S24', 0.0, 0.15, D24, 200, 700); st.cue('sfx:ding', 'S24', TH24, 0.3)

# 25: cobbles, less so. The setts come up the frame under her heels, then under his: he rattles over each one: his body ripples, his head hammers,
#     his pupils shake; the frame comes down on his face: the thumb is still up beside it, and shakes too
D25 = st.dur('S25'); C25 = 0.06                        # his heels reach the first sett
zs25 = lambda t: round(zs24(D24) - V23 * t, 3)
ZC25 = round(zs25(C25) + 0.17, 3)                      # the near end of the cobbles (his heels are there at C25)
HD25 = lambda t: round(zs25(t) + 0.17 + 1.93, 3)       # the middle of his head
def rattle(t0, t1, zf):
    ks = []; n = int((t1 - t0) / 0.066)
    for i in range(n):
        t = round(t0 + 0.066 * i, 3); a = 1 if i % 2 else -1; w = min(1.0, (i + 1) / 4)   # it climbs from his heels to his head in four hits
        ks.append(k(t, toon={'sq': [1.06, 1.0 - 0.03 * a * w, 0.1 + 0.05 * (a > 0) * w], 'hands': {'L': 'thumbUp'}, 'scl': {'handL': [1.7, 1.7, 1.7]}, 'reach': {'L': [round(RX - 0.27 + 0.03 * a, 3), 0.3 + 0.06 * a * w, round(zf(t) + 0.02 + 1.84, 3), 1, 0.06]},
                         'bend': {'spine': [0.14 * a * w, 0, 0, 1, None], 'neck': [-0.3 * a * w, 0, 0.1 * a * w, 1, None]}, 'face': {'eye': 0.35, 'brow': 0.9, 'pupilShake': w, 'tremble': w, 'jaw': 0.25 + 0.2 * (a > 0), 'cheeks': 0.6 * w}}, toonDur=0.05))
    return ks
st.shot('S25', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('ombre3', [RX, 0, zs25(0.0)], 180, 'marchPomp', 'neutral', params=MP, keys=[k(0.0, look=None), k(0.0, to=[RX, 0, zs25(D25)], dur=D25, clip='marchPomp', params=MP, ease='linear', face=180, cruise=True)]),
        act('mec', [RX, 0, round(zs25(0.0) + DRAG, 3)], 180, 'lieRelax', 'unimpressed', blink=0, keys=[k(0.0, look=None),
            k(0.0, toon={'sq': FLAT23, 'hands': {'L': 'thumbUp'}, 'scl': {'handL': [2.1, 2.1, 2.1]}, 'reach': {'L': TH(zs25, 0.0)}, 'face': {'eye': 0.3, 'brow': 0.7, 'gy': 0.9}}, toonDur=0.0), k(0.0, expr='worried'),   # his eyes are on what is coming
            k(0.0, to=[RX, 0, round(zs25(D25) + DRAG, 3)], dur=D25, clip='lieRelax', then='lieRelax', glide=True, ease='linear', face=180, cruise=True),
            *rattle(C25, D25, zs25)])],
        props=[P('cob', 'cobbles', pos=[RX, 0, round(ZC25 - 4.5, 3)], opts={'len': 9.0, 'w': 2.6, 'h': 0.05}), P('dash', 'roadDashes', pos=[round(RX + 0.62, 3), 0, round(Z24 + 4.0, 3)], opts={'len': round(Z24 + 4.0 - ZC25 - 0.3, 2), 'period': 1.5, 'dash': 0.8})],
        fx=[{'type': 'shake', 'at': C25, 'dur': round(D25 - C25, 3), 'amount': 0.008}],
        cams=[topcam(0.0, 0.32, zs25, RX), glide([cam(0.32, [RX, 1.8, round(HD25(0.32) - 0.42, 3)], [RX, 1.8, round(HD25(D25) - 0.42, 3)], [round(RX - 0.1, 3), 0.0, round(HD25(0.32) - 0.1, 3)], [round(RX - 0.1, 3), 0.0, round(HD25(D25) - 0.1, 3)], lens=44, ease='linear')], 0.7)])   # it comes down on his head as he rattles: his face, and the thumb beside it
[st.cue('clack', 'S25', round(C25 + 0.066 * i, 3), 0.28 if i % 2 else 0.2) for i in range(int((D25 - C25) / 0.066))]

# 26: the end. A crossing, the red man. Seen from behind them, from high: she walks to the kerb and stops; he does not: he slides on between her
#     feet and out over the white bars of the crossing, as long as the road is wide; he stops with his head between her heels; her white eyes go
#     down to him; he comes back like elastic, past her, and settles. She looks at her watch; a foot taps. Then, from above, close: his flat face:
#     his eyes come to us; a slow blink
D26 = st.dur('S26'); Z26 = -40.0; ST26, OV26, HD26, BK26, W26, CI26 = 0.3, 0.72, 0.9, 1.16, 1.26, 1.7   # she stops; he has gone as far as he goes; he starts back; he is back; her watch; the cut-in on his face
XK = 5.5; V26 = 2.0                                    # where she stops, at the kerb (the kerb is the line x = 5)
xs26 = lambda t: round(XK + V26 * max(0.0, ST26 - t), 3)
XB26 = round(XK + DRAG, 3); XO26 = round(XK - 2.35, 3)   # his hips: behind her; and when he has slid on: all of him out on the crossing, a metre and a half in front of her feet (with his head between her feet, his body was hidden behind her)
CAM26 = [10.2, 4.4, round(Z26 + 3.4, 3)]; LOOK26 = [5.25, 0.5, round(Z26 - 0.2, 3)]   # behind her and on her left (from straight behind, her own body hid the road in front of her feet as far as the other kerb: he slid out of sight)
WR26 = [round(XK - 0.2, 3), 1.52, round(Z26 + 0.4, 3)]   # her wrist, up at her left: toward the camera
HEAD26 = round(XB26 + 0.93, 3)                         # the middle of his head when he is back
st.shot('S26', 'parisStreet', setOpts={**STREET, 'clear': [-90, 80]}, look=SUN, actors=[
        act('ombre3', [xs26(0.0), 0, Z26], -90, 'marchPomp', 'neutral', params=MP, keys=[k(0.0, look=None), k(0.0, to=[XK, 0, Z26], dur=ST26, clip='marchPomp', params=MP, ease='linear', face=-90, cruise='in'),
            k(ST26, clip='stand', blend=0.08), k(ST26, toon={'sq': [1.05, 0.95, 1.05], 'settle': 0.5}, toonDur=0.06),
            k(OV26 - 0.14, look=[round(XK - 1.6, 3), 0.0, Z26]), k(OV26 - 0.04, toon={'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'eye': 0.5}}, toonDur=0.1),       # her eyes go down to him, out there in front of her: she leans to see
            k(BK26 - 0.06, toon={'settle': 0.5}, toonDur=0.12), k(BK26, look=None),
            k(W26, toon={'hands': {'L': 'fist'}, 'reach': {'L': [*WR26, 1, 0.06]}}, toonDur=0.1, toonEase='outBack'), k(W26 + 0.04, look=WR26),                           # her watch: he is late
            *[x for i in range(3) for x in (k(round(W26 + 0.16 + 0.14 * i, 3), toon={'hands': {'L': 'fist'}, 'reach': {'L': [*WR26, 1, 0.06]}, 'bend': {'shinR': [0.45, 0, 0, 1, None]}}, toonDur=0.06), k(round(W26 + 0.23 + 0.14 * i, 3), toon={'hands': {'L': 'fist'}, 'reach': {'L': [*WR26, 1, 0.06]}}, toonDur=0.05))]]),   # a foot taps
        act('mec', [round(xs26(0.0) + DRAG, 3), 0, Z26], -90, 'lieBack', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLAT23, 'face': {'lid': 0.4}}, toonDur=0.0),
            k(0.0, to=[XB26, 0, Z26], dur=ST26, clip='lieBack', then='lieBack', glide=True, ease='linear', face=-90, cruise='in'),                                          # behind her heels, at her pace
            k(ST26, to=[XO26, 0, Z26], dur=round(OV26 - ST26, 3), clip='lieBack', then='lieBack', glide=True, ease='out', face=-90),                                         # she has stopped: he goes on, between her feet, out over the crossing
            k(ST26 + 0.04, toon={'sq': [1.0, 1.3, 0.08], 'face': {'eye': 0.45, 'brow': 1}}, toonDur=0.14, toonEase='out'), k(ST26 + 0.04, expr='surprised'),                  # longer and longer
            k(OV26, toon={'sq': [1.0, 1.36, 0.08], 'face': {'eye': 0.45, 'brow': 1, 'gx': 0.0, 'gy': -0.6}}, toonDur=0.06),                                                   # stopped: his eyes go up to hers
            k(HD26, to=[round(XB26 + 0.3, 3), 0, Z26], dur=round(BK26 - HD26 - 0.08, 3), clip='lieBack', then='lieBack', glide=True, ease='in', face=-90),                     # and back, like elastic: too far
            k(HD26, toon={'sq': [1.0, 1.5, 0.07], 'face': {'eye': 0.5, 'brow': 1}}, toonDur=0.06), k(BK26 - 0.1, toon={'sq': [1.25, 0.8, 0.12], 'face': {'eye': 0.3, 'brow': 0.6}}, toonDur=0.05),   # he bunches up
            k(BK26 - 0.08, to=[XB26, 0, Z26], dur=0.12, clip='lieBack', then='lieBack', glide=True, ease='inOut', face=-90),
            k(BK26 + 0.04, toon={'sq': [0.98, 1.08, 0.1]}, toonDur=0.06), k(BK26 + 0.12, toon={'sq': FLAT23, 'settle': 0.6, 'face': {'lid': 0.4}}, toonDur=0.1), k(BK26 + 0.12, expr='unimpressed'),
            k(CI26 + 0.12, toon={'sq': FLAT23, 'face': {'lid': 0.35, 'gx': 0.0, 'gy': 0.0, 'browL': 0.4}}, toonDur=0.1),                                                        # his eyes to us
            k(CI26 + 0.32, toon={'sq': FLAT23, 'face': {'lid': 1, 'browL': 0.4}}, toonDur=0.08), k(CI26 + 0.47, toon={'sq': FLAT23, 'face': {'lid': 0.4, 'browL': 0.5}}, toonDur=0.08)])],   # a slow blink
        props=[P('zebra', 'zebra', pos=[4.55, 0, Z26], ry=180, opts={'n': 6, 'len': 3.2, 'bar': 0.5, 'gap': 0.45}),
               P('light', 'trafficLight', pos=[5.22, 0, round(Z26 - 1.55, 3)], ry=-112, opts={'state': [[0, 'g']], 'headRy': 112, 'poleColor': '#98A0A8', 'housing': '#2E4A3B', 'ped': 'r'}),   # the red man faces us; on her right (on her left its pole stood in front of the crossing, where he slides out)
               P('joints', 'pavingJoints', pos=[round(XK + 2.2, 3), 0, round(Z26 + 3.0, 3)], opts={'w': 5.2, 'step': 0.5, 'len': 6.5}),
               DIAL('dial26', [round(WR26[0] + 0.06, 3), WR26[1] + 0.03, round(WR26[2] + 0.05, 3)], W26 + 0.06, CI26, shade=True, r=0.14, ry=56, rot=[-0.45, 0, 0])],
        cams=[cam(0.0, CAM26, [CAM26[0] - 0.15, CAM26[1], CAM26[2]], LOOK26, LOOK26, lens=52),
              cam(CI26, [round(HEAD26 - 0.34, 3), 1.85, Z26], [round(HEAD26 - 0.3, 3), 1.75, Z26], [round(HEAD26 + 0.02, 3), 0.0, Z26], [round(HEAD26 + 0.02, 3), 0.0, Z26], lens=44)])   # then from above, close: his flat face, the right way up, 40 % of the width
st.cue('sfx:squeak', 'S26', ST26, 0.3); st.cue('sfx:stretch', 'S26', ST26 + 0.04, 0.35); st.cue('sfx:twang', 'S26', HD26, 0.4); st.cue('thud', 'S26', BK26, 0.3); st.cue('sfx:tick', 'S26', W26 + 0.1, 0.3); [st.cue('sfx:tick', 'S26', round(W26 + 0.19 + 0.14 * i, 3), 0.2) for i in range(3)]

SIL = {'silhouette': SHADE, 'silhouetteEyes': 2.0, 'darkEyes': 1.8}   # a shadow: one flat shade; its eyes: white ovals (a gain of 2: white after the look's tone curve), big enough for a phone
RIM3 = '#8A78A2'                                      # the edge of each part of her once she is a body (from the morning she gets up): a lighter violet: without it a flat shade that stands in a room is a hole in the picture
st.write("L'ombre", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, clothGravity=True, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'castShadow': False},
    'ombre': {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, **SIL},
    'ombre3': {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, **SIL, 'silhouetteRim': RIM3, 'silhouetteRimW': 0.014},
    'clerk': {'preset': 'mamie', 'seed': 141, 'build': {'width': 0.9, 'headWidth': 1.3, 'height': 0.94}},
    'grand': {'preset': 'fringant', 'seed': 143, 'hat': 'fedora', 'build': {'width': 0.8, 'headWidth': 1.2, 'height': 1.5}, 'castShadow': False},   # one and a half times our man, and a hat: another outline than his
    'petite': {'preset': 'lemec', 'build': {'width': 0.9, 'headWidth': 1.35, 'height': 0.5}, **SIL},
    'flic': {'preset': 'cop', 'seed': 151, 'build': {'width': 0.92, 'headWidth': 1.3}, 'castShadow': False},
    'ombreflic': {'preset': 'cop', 'seed': 151, 'build': {'width': 0.92, 'headWidth': 1.3}, **SIL},
    'avocat': {'preset': 'avocat', 'seed': 153, 'build': {'width': 0.9, 'headWidth': 1.3}, **SIL}})
