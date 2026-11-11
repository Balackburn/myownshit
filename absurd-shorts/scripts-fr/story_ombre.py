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
STREET = {'clear': [-80, 80], 'eiffel': False, 'paveW': 6.5}   # paveW: the pavements run under the house fronts (at 5 m a dark gutter showed along the foot of the walls)
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

# 4: one morning. He comes along the wall, stops, turns to us and stretches, eyes shut: behind him the wall is bare
D4 = st.dur('S04'); T4 = 0.3; Z4 = 0.55
wall4 = lambda t, d=4.2, **kw: wallcam(t, Z4 + 0.25, Z4 + 0.22, d=d, h=1.45, lh=1.4, **kw)
STRETCH = lambda dy=0.0, **kw: {'hands': {'L': 'spread', 'R': 'spread'}, 'reach': {'L': [HX - 0.1, 2.5 + dy, Z4 + 0.32, 1, 0.08], 'R': [HX - 0.1, 2.5 + dy, Z4 - 0.32, 1, 0.08]}, **kw}   # both arms up over his head
st.shot('S04', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, round(Z4 + VW * T4, 3)], 180, 'stand', 'happy', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, Z4], dur=T4, clip='walk', ease='out', face=180, cruise='in'),
            k(T4 - 0.06, face=-78, turn=0.16), k(T4, expr='yawn'),                                                                             # he stops and turns to us
            k(T4 - 0.02, toon=STRETCH(-0.25, sq=[1.03, 0.96, 1.03], face={'jaw': 0.5}), toonDur=0.1, toonEase='in'),
            k(T4 + 0.1, toon=STRETCH(0.05, sq=[0.93, 1.1, 0.93], bend={'spine': [-0.16, 0, 0, 1.06, None]}, face={'jaw': 0.8}), toonDur=0.16, toonEase='out'),   # up on his toes: a stretch, a yawn
            k(T4 + 0.3, toon=STRETCH(0.0, sq=[0.95, 1.07, 0.95], bend={'spine': [-0.2, 0, 0, 1.06, None]}, face={'jaw': 0.6}, settle=0.5), toonDur=0.12)])],
        props=[WALL(2.0)],
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
            k(F5 - 0.08, look=[HX - 0.3, 0.1, Z4 - 0.2]), k(F5, clip='lookSole', blend=0.1), k(F5, toon={'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'brow': 0.8, 'gy': 0.6}}, toonDur=0.1),   # under his shoe
            k(U5 - 0.06, clip='stand', blend=0.1), k(U5 - 0.04, look=[WX - 4.0, 1.45, Z4 + 0.34]), k(U5, toon={'face': {'brow': 1, 'eye': 0.4, 'mouth': 'o'}}, toonDur=0.08), k(U5, expr='worried')])],   # to us
        props=[WALL(2.0), P('ghost', 'ghostOutline', pos=GH5, ry=-90, opts={'at': O5, 'h': 1.75})],
        cams=[wall4(0.0, d=3.9), glide([wallcam(H5, Z4 + 0.36, Z4 + 0.34, d=4.1, h=1.45, lh=1.3)], 0.25)])   # the frame slides to the place where she should be (the outline whole, its arm inside the frame)
st.cue('pop', 'S05', O5, 0.45); st.cue('sfx:tick', 'S05', E5, 0.25); st.cue('whoosh', 'S05', H5, 0.2, 0.15, 500, 1800)

# ---- the town hall: the registry desk (ÉTAT CIVIL), a clerk behind it
MAIRIE = {'map': False, 'plant': False, 'bannerY': 2.78, 'clockX': 9}
VIS, CLK = [-0.1, 0, 0.42], [0.0, 0, -1.66]           # where he stands; where she sits... stands
EYE_C, EYE_V = [0.0, 1.42, -1.52], [-0.1, 1.5, 0.3]   # her eyes; his: each shot of the pair is seen from the other's place
PO6 = [0.36, 1.5, 0.14]                              # the notice he holds up beside his head
# 6: he declares her missing: seen from the clerk's place: he holds up a notice beside his head: PERDUE, and the outline of a man: his; his finger taps
#    the outline, then his own chest
D6 = st.dur('S06'); U6, A6, B6 = 0.14, 0.44, 0.82
HOLD6 = lambda l, **kw: {'hands': {'R': 'grip', 'L': 'point'}, 'reach': {'R': [PO6[0] + 0.02, PO6[1] - 0.36, PO6[2] + 0.03, 1, 0.05], 'L': [*l, 1, 0.14]}, **kw}
L6A, L6B, L6C = [PO6[0] - 0.28, 1.2, PO6[2] - 0.12], [PO6[0] - 0.03, PO6[1] - 0.08, PO6[2] - 0.05], [VIS[0] - 0.02, 1.32, VIS[2] - 0.2]   # his left forefinger: waiting; on the outline; on his own chest
st.shot('S06', 'mairie', setOpts=MAIRIE, actors=[
        act('mec', VIS, 180, 'stand', 'worried', keys=[k(0.0, look=EYE_C), k(0.0, toon=HOLD6(L6A, face={'brow': 0.9, 'eye': 0.3}), toonDur=0.0),
            k(A6 - 0.14, toon=HOLD6(L6A, face={'brow': 0.9, 'eye': 0.3, 'gx': -0.8}), toonDur=0.08), k(A6 - 0.04, toon=HOLD6(L6B, scl={'handL': [1.2, 1.2, 1.2]}, face={'brow': 0.9, 'gx': -0.8}), toonDur=0.05, toonEase='in'),   # his eyes, then his finger, to the outline: this
            k(A6 + 0.06, toon=HOLD6(L6A, face={'brow': 1, 'eye': 0.3}), toonDur=0.08), k(A6 + 0.14, toon=HOLD6(L6B, scl={'handL': [1.2, 1.2, 1.2]}, face={'brow': 1}), toonDur=0.05, toonEase='in'),                                   # twice
            k(B6 - 0.12, toon=HOLD6(L6A, face={'brow': 1, 'eye': 0.3}), toonDur=0.08), k(B6, toon=HOLD6(L6C, sq=[0.97, 1.04, 0.97], face={'brow': 1, 'eye': 0.4, 'mouth': 'o'}), toonDur=0.07, toonEase='in'),                       # then on his own chest: mine
            k(B6 + 0.1, toon=HOLD6(L6C, settle=0.5, face={'brow': 1, 'eye': 0.4, 'mouth': 'o'}), toonDur=0.08), k(B6 + 0.26, toon=HOLD6(L6C, face={'brow': 1, 'eye': 0.4, 'lid': 1}), toonDur=0.04), k(B6 + 0.33, toon=HOLD6(L6C, face={'brow': 1, 'eye': 0.4}), toonDur=0.04)])],
        props=[P('poster', 'lostPoster', pos=[PO6[0], PO6[1] - 0.75, PO6[2]], ry=180, opts={'w': 0.46}, keys=[k(0.0, to=PO6, dur=U6, ease='outBack')])],
        cams=[cam(0.0, [0.13, 1.52, -2.38], [0.13, 1.52, -2.26], [0.13, 1.4, 0.3], [0.13, 1.4, 0.3], lens=54)])   # from her side of the desk: the notice at the left, his face at the right, the desk across the bottom
st.cue('whoosh', 'S06', 0.0, 0.25, 0.15, 500, 1800); st.cue('sfx:tick', 'S06', A6 - 0.04, 0.3); st.cue('sfx:tick', 'S06', A6 + 0.14, 0.3); st.cue('thud', 'S06', B6, 0.2)

# 7: at the town hall. Seen from his place: the clerk holds his notice up between them (we see its back): her eyes, over its top edge and her glasses,
#    go down to it, up to us, down to it
D7 = st.dur('S07'); SH7 = [0.0, 1.27, -1.1]            # the sheet, held up at arm's length, facing her
CLKH = lambda **kw: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [SH7[0] + 0.2, SH7[1] - 0.12, SH7[2] - 0.02, 1, 0.05], 'R': [SH7[0] - 0.2, SH7[1] - 0.12, SH7[2] - 0.02, 1, 0.05]}, **kw}
CAM7 = lambda t, dz=0.0, **kw: cam(t, [0.42, 1.36, 0.95 - dz], [0.4, 1.36, 0.85 - dz], [0.0, 1.72, -1.9], [0.0, 1.72, -1.9], lens=44, **kw)   # low enough for the banner over her
st.shot('S07', 'mairie', setOpts=MAIRIE, actors=[
        act('clerk', CLK, 0, 'stand', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon=CLKH(face={'gy': 0.8, 'browL': 0.4}), toonDur=0.0),                 # on the sheet
            k(0.24, toon=CLKH(face={'gy': -0.25, 'brow': 0.5}), toonDur=0.07), k(0.3, look=[0.42, 1.36, 0.95]),                                                    # up to us: eyes, then the head, a little
            k(0.52, toon=CLKH(face={'gy': 0.8, 'browL': 0.5}), toonDur=0.07), k(0.56, look=None),                                                                    # down to it
            k(0.7, toon=CLKH(face={'gy': 0.8, 'browL': 0.5, 'lid': 1}), toonDur=0.04), k(0.77, toon=CLKH(face={'gy': 0.8, 'browL': 0.5}), toonDur=0.04)])],                # a blink
        props=[P('poster', 'lostPoster', pos=SH7, ry=180, rot=[0.12, 0, 0], opts={'w': 0.46})],
        cams=[CAM7(0.0)])
st.cue('pop', 'S07', 0.0, 0.25)

# 8: the answer. She lays the sheet on her desk, takes her stamp, breathes on it, looks at us over her glasses, and stamps: a small dry tap
D8 = st.dur('S08'); L8, HA8, LK8, UP8, TP8 = 0.14, 0.4, 0.66, 0.9, 1.04   # the sheet is down; she breathes on the stamp; a look at us; the stamp goes up a little; the tap
ONDESK = [0.0, 0.835, -0.72]                         # the sheet, flat on the desk
ST8A, ST8B, ST8C, ST8D = [-0.36, 0.98, -1.05], [-0.1, 1.36, -1.3], [-0.04, 1.16, -0.82], [-0.04, 0.9, -0.76]   # the stamp: off the ink pad; at her mouth; over the sheet; on it
CLK8 = lambda r, **kw: {'hands': {'L': 'open', 'R': 'grip'}, 'reach': {'L': [0.24, 0.87, -0.86, 1, 0.08], 'R': [*r, 1, 0.05]}, **kw}
st.shot('S08', 'mairie', setOpts=MAIRIE, actors=[
        act('clerk', CLK, 0, 'stand', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon=CLKH(face={'gy': 0.8, 'browL': 0.5}), toonDur=0.0),
            k(0.02, toon=CLK8(ST8A, bend={'spine': [0.18, 0, 0, 1, None]}, face={'gy': 0.8}), toonDur=L8, toonEase='inOut'),                                      # the sheet down, her hand to the stamp
            k(HA8 - 0.14, toon=CLK8(ST8B, face={'gy': 0.3, 'jaw': 0.1}), toonDur=0.12, toonEase='out'), k(HA8, toon=CLK8(ST8B, sq=[1.03, 0.97, 1.03], face={'jaw': 0.7, 'cheeks': 0.6, 'lid': 0.6}), toonDur=0.05),   # hah
            k(HA8 + 0.14, toon=CLK8(ST8B, face={'jaw': 0.0, 'lid': 0.3}), toonDur=0.08),
            k(LK8, toon=CLK8(ST8C, face={'gy': -0.3, 'browL': 0.8, 'lid': 0.35}), toonDur=0.14, toonEase='inOut'), k(LK8 + 0.02, look=[0.42, 2.08, 1.15]),               # a look at us over her glasses, the stamp over the sheet
            k(UP8, toon=CLK8([ST8C[0], ST8C[1] + 0.1, ST8C[2]], face={'gy': -0.3, 'browL': 0.8, 'lid': 0.35}), toonDur=0.1, toonEase='out'),                           # up a little
            k(TP8 - 0.04, toon=CLK8(ST8D, bend={'spine': [0.12, 0, 0, 1, None]}, face={'gy': -0.3, 'browL': 0.8, 'lid': 0.35}), toonDur=0.04, toonEase='in'),          # tap: her eyes have not left us
            k(TP8 + 0.05, toon=CLK8([ST8D[0], ST8D[1] + 0.07, ST8D[2]], settle=0.4, face={'gy': -0.3, 'browL': 0.9, 'lid': 0.35}), toonDur=0.08)])],
        props=[P('poster', 'lostPoster', pos=SH7, ry=180, rot=[0.12, 0, 0], opts={'w': 0.46, 'stampAt': TP8}, keys=[k(0.02, to=ONDESK, dur=L8, ease='inOut'), k(0.02, rotTo=[-1.5, 0, 0], dur=L8, ease='inOut'),   # she turns it over as she lays it down: the print up, its foot toward us
                    k(TP8, to=[ONDESK[0], ONDESK[1] + 0.05, ONDESK[2]], dur=0.05, ease='out'), k(TP8 + 0.05, to=ONDESK, dur=0.07, ease='in')]),
               P('stamp', 'rubberStamp', on={'actor': 'clerk', 'hand': 'R', 'offset': [0, -0.06, 0.02], 'rot': [3.1416, 0, 0]}, scale=1.5),
               P('hah', 'dustPuff', pos=[-0.08, 1.38, -1.14], scale=0.2, opts={'once': True, 'startAt': HA8, 'period': 0.3, 'color': '#FFFFFF'}),
               P('tap', 'impactStars', pos=[-0.04, 0.95, -0.7], rot=[-0.9, 0, 0], opts={'at': TP8, 'n': 5, 'r': 0.24, 'r0': 0.08, 'dur': 0.26, 'size': 0.055})],
        fx=[{'type': 'shake', 'at': TP8, 'dur': 0.12, 'amount': 0.012}],
        cams=[cam(0.0, [0.42, 2.08, 1.15], [0.4, 2.08, 1.05], [0.0, 1.3, -1.1], [0.0, 1.3, -1.1], lens=44)])   # from higher: her face, and the sheet on the desk under her hands
st.cue('sfx:slideDown', 'S08', 0.02, 0.2); st.cue('sfx:gasp', 'S08', HA8, 0.3); st.cue('clack', 'S08', TP8, 0.6)

# 9: « Elle est majeure. »: she holds the sheet up beside her face, its front to us this time: the outline, and across it, in red: MAJEURE; she says it
D9 = st.dur('S09'); PO9 = [-0.37, 1.75, -1.14]   # the sheet: beside her face (lower, its stamp fell in the caption band)
W9 = [round(w['s'] - st.SH['S09'][0], 3) for w in st.L['L05']['words']]
CLK9 = lambda **kw: {'hands': {'L': 'open', 'R': 'grip'}, 'reach': {'R': [PO9[0] + 0.05, PO9[1] - 0.36, PO9[2] - 0.03, 1, 0.05], 'L': [0.2, 0.86, -0.85, 1, 0.08]}, **kw}
st.shot('S09', 'mairie', setOpts={**MAIRIE, 'banner': False}, actors=[
        act('clerk', CLK, 0, 'stand', 'unimpressed', blink=0, keys=st.talk('L05', 'S09', 'unimpressed') + [k(0.0, look=[0.2, 1.4, 0.75]), k(0.0, toon=CLK9(face={'browL': 0.8, 'lid': 0.35}), toonDur=0.0),
            *[x for i, t in enumerate(W9) for x in (k(max(0.0, t), toon=CLK9(sq=[0.98, 1.03, 0.98], face={'jaw': 0.55 if i < 2 else 0.8, 'browL': 0.9, 'lid': 0.3}), toonDur=0.05, toonEase='out'), k(max(0.0, t) + (0.1 if i < 2 else 0.3), toon=CLK9(face={'browL': 0.8, 'lid': 0.35}), toonDur=0.08))],   # her jaw long on each word
            k(0.78, toon=CLK9(face={'browL': 0.9, 'lid': 1}), toonDur=0.05), k(0.88, toon=CLK9(face={'browL': 0.9, 'lid': 0.35, 'mouth': 'smirk'}), toonDur=0.06)])],   # a slow blink: next
        props=[P('poster', 'lostPoster', pos=[PO9[0], PO9[1] - 0.5, PO9[2]], ry=0, opts={'w': 0.46, 'stampAt': -1}, keys=[k(0.0, to=PO9, dur=0.12, ease='outBack')])],
        cams=[cam(0.0, [0.16, 1.4, 0.8], [0.15, 1.4, 0.68], [-0.19, 1.75, -1.4], [-0.19, 1.75, -1.4], lens=44)])   # the sheet at the left, her face at the right, both between the card band and the caption band
st.cue('whoosh', 'S09', 0.0, 0.25, 0.12, 500, 1800)
st.card('S09', 'ELLE EST MAJEURE')

# ---- further down the street: another stretch of sunny wall
Z10 = -14.0
TALL = [0.03, 1.3, 0.86]                             # she, stretched to another man's height: thin, on her toes
# 10: she already worked elsewhere. Seen from behind our man (he stands at the left, his back to us): a tall man strides along the wall, and behind
#     him, on the wall, a shadow we know (the tuft): stretched to his height, and on time: step for step; our man's head goes with them
D10 = st.dur('S10'); VT = 1.9; ST10 = 0.95; T10 = round(ST10 - 0.22, 3)   # the tall man's speed; when he has stopped; when he starts to slow
ZS10 = round(Z10 + 1.05, 3); LAG10 = 0.62            # where he stops: in the open, at the right of our man (walking on, he ended behind him); her place behind him on the wall
zt10 = lambda t: round(ZS10 + 0.15 + VT * (T10 - t), 3) if t < T10 else round(ZS10 + 0.15 * (1 - min(1.0, (t - T10) / 0.22)) ** 3, 3)   # the tall man's z
ME10 = [HX - 1.5, 0, round(Z10 + 0.2, 3)]
st.shot('S10', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('grand', [HX, 0, zt10(0.0)], 180, 'walk', 'smug', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, zt10(T10)], dur=T10, clip='walk', ease='linear', face=180, cruise='in'),
            k(T10, to=[HX, 0, ZS10], dur=0.22, clip='walk', then='stand', ease='out', face=180), k(ST10 + 0.16, clip='checkWatch', blend=0.12)]),                # he stops; his wrist comes up
        act('ombre', [SX, 0, round(zt10(0.0) + LAG10, 3)], 180, 'walk', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': TALL, 'bend': {'neck': [0, 0, 0, 1.25, None]}}, toonDur=0.0),
            k(0.0, to=[SX, 0, round(zt10(T10) + LAG10, 3)], dur=T10, clip='walk', ease='linear', face=180, cruise='in'),
            k(T10, to=[SX, 0, round(ZS10 + LAG10, 3)], dur=0.22, clip='walk', then='stand', ease='out', face=180), k(ST10 + 0.16, clip='checkWatch', blend=0.12)]),   # in step with him, and she stops with him: not a frame late
        act('mec', ME10, -25, 'stand', 'surprised', keys=[k(0.0, look=[WX, 1.5, zt10(0.0) + 0.3]), *[k(t, look=[WX, 1.5, round(zt10(t + 0.12) + LAG10, 3)]) for t in (0.3, 0.6, 0.9)],   # at the left, three quarters to us: his head goes with them as they come; then stays on her
            k(0.0, toon={'face': {'brow': 0.8, 'eye': 0.3}}, toonDur=0.0), k(0.5, toon={'bend': {'spine': [0.1, 0, 0, 1, None]}, 'sq': [0.98, 1.03, 0.98], 'face': {'brow': 1, 'eye': 0.4, 'jaw': 0.3}}, toonDur=0.2),
            k(ST10 + 0.06, toon={'hands': {'R': 'spread'}, 'bend': {'spine': [0.14, 0, 0, 1, None]}, 'reach': {'R': [HX - 0.7, 1.35, round(Z10 + 0.85, 3), 0.9, 0.1]}, 'face': {'brow': 1, 'eye': 0.4, 'jaw': 0.5}}, toonDur=0.2, toonEase='out')])],   # a hand goes out to her
        props=[WALL(Z10 + 2.0)],
        cams=[cam(0.0, [WX - 6.6, 1.5, Z10 + 0.8], [WX - 6.5, 1.5, Z10 + 0.75], [WX, 1.5, Z10 + 0.8], [WX, 1.5, Z10 + 0.75], lens=44)])
st.cue('whoosh', 'S10', 0.0, 0.2, 0.4, 300, 1200)

# 11: for a taller guy. Closer on the wall: he stops and looks at his watch: she does it with him, to the frame (she was half a second late for ours);
#     then her head turns: two white eyes on us; a shrug; back to work
D11 = st.dur('S11'); E11, G11, B11 = 0.42, 0.62, 0.94   # (the watches are up from the last shot) her eyes on us; the shrug; back to work
Z11 = ZS10
st.shot('S11', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('grand', [HX, 0, Z11], 180, 'checkWatch', 'smug', keys=[k(0.0, look=None), k(B11 + 0.06, clip='stand', blend=0.12)]),
        act('ombre', [SX, 0, round(Z11 + LAG10, 3)], 180, 'checkWatch', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': TALL, 'bend': {'neck': [0, 0, 0, 1.25, None]}}, toonDur=0.0),   # with him, to the frame
            k(E11, clip='stand', blend=0.08), k(E11, look=[WX - 3.8, 1.5, Z11 + 0.2]), k(E11, toon={'sq': [0.03, 1.22, 0.9], 'bend': {'neck': [0, 0, 0, 1.25, None]}}, toonDur=0.06),   # her eyes on us: she comes down off her toes a little
            k(G11, clip='shrug', blend=0.08), k(G11, toon={'sq': [0.03, 1.24, 0.9], 'bend': {'neck': [0, 0, 0, 1.2, None]}}, toonDur=0.08),                 # a shrug: that is how it is
            k(B11, clip='stand', blend=0.1), k(B11, look=None), k(B11, toon={'sq': TALL, 'bend': {'neck': [0, 0, 0, 1.25, None]}}, toonDur=0.1)])],          # back up on her toes
        props=[WALL(Z10 + 2.0)],
        cams=[wallcam(0.0, Z11 + 0.12, Z11 + 0.08, d=4.8, h=1.55, lh=1.6)])
st.cue('sfx:tick', 'S11', 0.05, 0.3); st.cue('pop', 'S11', E11, 0.3)

# 12: he hired one. A rail of shadows for hire stands against the wall (LOCATION D'OMBRES): they hang from hangers and sway. He stands at its end; his
#     arm goes along the rail, longer at each hanger: the tall one, the wide one, the plain one, the dog: no; it stops, three metres long, on the last
#     one, the small one, unhooks it and brings it back
D12 = st.dur('S12'); Z12 = -22.0; RK = [WX - 0.5, 0, Z12]
hz12 = lambda i: round(Z12 + 1.2 - (i + 0.5) * 2.4 / 5, 3)   # the hanger number i along the rail (0: the nearest to him)
ME12 = [HX - 0.5, 0, round(Z12 + 1.5, 3)]
CAM12 = [round(WX - 8.9, 3), 1.5, round(Z12 - 0.2, 3)]   # across the road, square to the wall: he whole at the right, the rail and his arm across the frame (from his end of the rail he was a dark back cut by the edge)
PT12 = lambda i, y=1.62, **kw: {'hands': {'L': 'point', 'R': 'open'}, 'reach': {'L': [RK[0] - 0.2, y, hz12(i), 1, 0.14]}, **kw}
st.shot('S12', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', ME12, 188, 'stand', 'neutral', keys=[k(0.0, look=[RK[0], 1.5, hz12(0)]), k(0.0, toon=PT12(0, face={'brow': 0.5}), toonDur=0.0),
            *[x for i in (1, 2, 3) for x in (k(0.02 + 0.15 * i, toon=PT12(i, face={'brow': 0.5 - 0.1 * i, 'gx': -0.4}), toonDur=0.09, toonEase='out'), k(0.02 + 0.15 * i, look=[RK[0], 1.5, hz12(i)]))],   # too dear, too dear, too dear: his arm grows
            k(0.62, toon=PT12(4, 1.3, sq=[1.02, 0.97, 1.02], face={'brow': 0.9, 'eye': 0.3}), toonDur=0.09, toonEase='out'), k(0.62, look=CAM12), k(0.64, expr='happy'),               # the last, the small one: this one (to us)
            k(0.8, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [RK[0] - 0.12, 1.9, hz12(4), 1, 0.05]}, 'face': {'brow': 0.9}}, toonDur=0.08), k(0.8, look=[RK[0], 1.6, hz12(4)]),             # his hand goes up to its hanger
            k(0.94, toon={'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [ME12[0] - 0.15, 1.6, ME12[2] - 0.55, 1, 0.05]}, 'sq': [0.97, 1.04, 0.97], 'face': {'brow': 0.9}}, toonDur=0.12, toonEase='in')])],   # and the arm comes back
        props=[WALL(Z12 + 2.0), P('rack', 'shadowRack', pos=RK, ry=-90, opts={'w': 2.4, 'h': 2.0, 'kinds': ['kid', 'dog', 'man', 'wide', 'tall']})],   # (the rail's own order runs the other way: the small one at the far end)
        cams=[cam(0.0, CAM12, [CAM12[0] + 0.25, CAM12[1], CAM12[2]], [WX - 0.5, 1.35, Z12 + 0.3], [WX - 0.5, 1.35, Z12 + 0.3], lens=44)])
[st.cue('sfx:stretch', 'S12', 0.02 + 0.15 * i, 0.2) for i in (1, 2, 3)]; st.cue('sfx:ding', 'S12', 0.64, 0.3); st.cue('sfx:twang', 'S12', 0.94, 0.3)

# 13: too small. He walks along the wall; behind him, on the wall, a shadow half his height trots to keep up, two steps for each of his, and waves at
#     us; his eyes go down to it, then to us
D13 = st.dur('S13'); Z13 = -26.0
zh13 = lambda t: round(Z13 + 1.0 - VW * t, 3)
st.shot('S13', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, zh13(0.0)], 180, 'walk', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, zh13(D13)], dur=D13, clip='walk', ease='linear', face=180, cruise=True),
            k(0.26, toon={'face': {'gx': 0.9, 'gy': 0.5, 'browL': 0.6}}, toonDur=0.08),                                                                  # his eyes go back and down to it
            k(0.52, look=[WX - 3.9, 1.4, zh13(0.75) - 0.3]), k(0.56, toon={'face': {'lid': 0.45, 'browL': 0.7}}, toonDur=0.08)]),                           # then his head comes to us
        act('petite', [SX, 0, zh13(0.0) + LAG], 180, 'run', 'happy', params={'freq': 3.4, 'bounce': 0.8}, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(0.0, to=[SX, 0, zh13(D13) + LAG], dur=D13, clip='run', params={'freq': 3.4, 'bounce': 0.8}, ease='linear', face=180, cruise=True),
            k(0.36, look=[WX - 4.0, 1.2, zh13(0.6)]), k(0.4, toon={'sq': FLATX, 'hands': {'R': 'spread'}, 'reach': {'R': [SX, 1.35, zh13(0.55) + LAG, 1, 0.08]}}, toonDur=0.08),   # her eyes on us: a wave
            *[k(0.48 + 0.1 * i, toon={'sq': FLATX, 'hands': {'R': 'spread'}, 'reach': {'R': [SX, 1.35 + 0.0 * i, round(zh13(0.58 + 0.1 * i) + LAG + (0.16 if i % 2 else -0.16), 3), 1, 0.08]}}, toonDur=0.09) for i in range(4)]])],
        props=[WALL(Z13 + 0.5)],
        cams=[wallcam(0.0, zh13(0.0) + 0.15, zh13(D13) + 0.15, d=3.9, h=1.3, lh=1.15)])
st.cue('sfx:squeak', 'S13', 0.0, 0.2)

# 14: he was fined. A policeman steps into his way, a hand up: he stops short; on the wall the policeman has a proper shadow, cap and all, a hand up too;
#     the small one runs on past our man, sees it, and comes back behind his legs
D14 = st.dur('S14'); Z14 = zh13(D13); T14 = 0.3
ZC14 = round(Z14 - VW * T14 - 1.25, 3)                # the policeman
ZS14 = round(Z14 - VW * T14, 3)                       # where our man stops
LAGC = -0.3                                           # the policeman's shadow: just behind his back (the sun is in his face)
PALM = lambda who_x, zc, **kw: {'hands': {'R': 'spread'}, 'reach': {'R': [who_x, 1.5, round(zc + 0.6, 3), 1, 0.1]}, **kw}   # a hand up, palm toward the one who comes
st.shot('S14', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, Z14], 180, 'walk', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, ZS14], dur=T14, clip='walk', ease='linear', face=180, cruise='in'),
            k(T14 - 0.04, toon={'sq': [1.05, 0.95, 1.05], 'bend': {'spine': [-0.3, 0, 0, 1, None]}, 'face': {'brow': 1, 'eye': 0.4}}, toonDur=0.06, toonEase='out'), k(T14 - 0.04, expr='surprised'), k(T14 - 0.02, face=-142, turn=0.12),   # he stops short, leaning back, three quarters to us
            k(T14 + 0.14, toon={'settle': 0.6, 'bend': {'spine': [-0.08, 0, 0, 1, None]}, 'face': {'brow': 0.9, 'eye': 0.35}}, toonDur=0.12)]),
        act('petite', [SX, 0, Z14 + LAG], 180, 'run', 'happy', params={'freq': 3.4, 'bounce': 0.8}, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(0.0, to=[SX, 0, round(ZS14 - 0.55, 3)], dur=T14 + 0.16, clip='run', params={'freq': 3.4, 'bounce': 0.8}, ease='linear', face=180, cruise='in'),               # she runs on past him
            k(T14 + 0.18, toon={'sq': [0.03, 1.12, 0.9]}, toonDur=0.05), k(T14 + 0.18, look=[SX, 1.6, ZC14 + LAGC]),                                                        # sees the big one: up on her toes
            k(T14 + 0.3, to=[SX, 0, round(ZS14 + LAG + 0.1, 3)], dur=0.2, clip='run', params={'freq': 5.0, 'bounce': 0.6}, ease='inOut', face=0), k(T14 + 0.3, toon={'sq': FLATX}, toonDur=0.06)]),   # and back behind where his legs should be
        act('flic', [HX, 0, round(ZC14 - 0.5, 3)], -38, 'stand', 'determined', keys=[k(0.0, look='mec'), k(0.0, to=[HX, 0, ZC14], dur=0.14, clip='walk', ease='out', face=-38),
            k(0.06, toon=PALM(HX, ZC14, sq=[0.97, 1.05, 0.97], scl={'handR': [1.3, 1.3, 1.3]}), toonDur=0.1, toonEase='outBack')]),
        act('ombreflic', [SX, 0, round(ZC14 - 0.5 + LAGC, 3)], 0, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATX}, toonDur=0.0), k(0.0, to=[SX, 0, ZC14 + LAGC], dur=0.14, clip='walk', ease='out', face=0),
            k(0.06, toon=PALM(SX, ZC14 + LAGC, sq=[0.03, 1.05, 0.97], scl={'handR': [1.3, 1.3, 1.3]}), toonDur=0.1, toonEase='outBack')])],
        props=[WALL(Z13 + 0.5)],
        cams=[wallcam(0.0, round(ZS14 - 0.45, 3), round(ZS14 - 0.55, 3), d=4.9, h=1.4, lh=1.35)])
st.cue('sfx:whistle', 'S14', 0.04, 0.4); st.cue('sfx:squeak', 'S14', T14 - 0.04, 0.35)

# 15: for walking without a shadow. The policeman points at the wall behind our man: nothing; down at the small one: his flat hand says « this high »;
#     he writes, tears off the slip, and his arm goes all the way to the wall: he sticks the fine where the shadow should be; the small one looks up at it
D15 = st.dur('S15'); P15, M15, W15, SL15 = 0.1, 0.36, 0.56, 1.02   # he points; « this high »; he writes; the slap
FINE15 = [SX, 1.42, round(ZS14 + LAG + 0.05, 3)]       # where the head of a proper shadow would be
st.shot('S15', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [HX, 0, ZS14], -142, 'stand', 'worried', keys=[k(0.0, look='flic'), k(P15 + 0.1, toon={'face': {'gx': 0.9, 'brow': 0.7}}, toonDur=0.08), k(M15, toon={'face': {'gy': 0.7, 'brow': 0.7}}, toonDur=0.08),
            k(SL15 + 0.06, toon={'sq': [1.04, 0.95, 1.04], 'face': {'brow': 1, 'eye': 0.4, 'jaw': 0.3, 'gx': 0.9}}, toonDur=0.06), k(SL15 + 0.3, look=[WX - 4.0, 1.45, ZS14 - 0.1]), k(SL15 + 0.32, toon={'face': {'brow': 0.4, 'lid': 0.45}}, toonDur=0.1), k(SL15 + 0.32, expr='unimpressed')]),   # the slip; then us
        act('petite', [SX, 0, round(ZS14 + LAG + 0.1, 3)], 0, 'stand', 'worried', keys=[k(0.0, look=[SX, 1.6, ZC14 + LAGC]), k(0.0, toon={'sq': FLATX}, toonDur=0.0),
            k(M15 + 0.04, toon={'sq': [0.03, 0.86, 1.1]}, toonDur=0.08), k(W15, toon={'sq': FLATX}, toonDur=0.1),                                        # she shrinks under the hand
            k(SL15 + 0.02, toon={'sq': [0.03, 0.8, 1.15]}, toonDur=0.04), k(SL15 + 0.1, toon={'sq': FLATX, 'settle': 0.5}, toonDur=0.1), k(SL15 + 0.14, look=FINE15)]),   # the slap over her head; she looks up at it
        act('flic', [HX, 0, ZC14], -38, 'stand', 'determined', keys=[k(0.0, look='mec'), k(0.0, toon=PALM(HX, ZC14), toonDur=0.0),
            k(P15, toon={'hands': {'R': 'point'}, 'reach': {'R': [SX - 0.25, 1.35, round(ZS14 + 0.75, 3), 1, 0.14]}, 'face': {'browL': 0.6}}, toonDur=0.1, toonEase='out'), k(P15, look=[WX, 1.3, ZS14 + 0.8]),   # the wall behind him: nothing
            k(M15 - 0.08, look=[SX, 0.6, ZS14 + LAG]), k(M15, toon={'hands': {'R': 'open'}, 'reach': {'R': [HX + 0.35, 0.92, round(ZS14 - 0.25, 3), 1, 0.1]}, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'brow': -0.5}}, toonDur=0.1, toonEase='out'),   # « this high »
            k(M15 + 0.1, toon={'hands': {'R': 'open'}, 'reach': {'R': [HX + 0.35, 0.86, round(ZS14 - 0.25, 3), 1, 0.1]}, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'brow': -0.5}}, toonDur=0.06),
            k(W15, clip='writeOnHeld', blend=0.1), k(W15, toon={'face': {'brow': -0.6, 'gy': 0.6}}, toonDur=0.1), k(W15, look=None),                         # he writes
            k(SL15 - 0.16, clip='stand', blend=0.08), k(SL15 - 0.16, toon={'hands': {'R': 'spread'}, 'reach': {'R': [HX - 0.3, 1.8, round(ZC14 + 0.3, 3), 1, 0.1]}, 'sq': [0.97, 1.05, 0.97], 'bend': {'spine': [-0.15, 0, 0, 1, None]}}, toonDur=0.1, toonEase='out'),   # the slip, up
            k(SL15 - 0.04, toon={'hands': {'R': 'spread'}, 'reach': {'R': [FINE15[0] - 0.05, FINE15[1], FINE15[2], 1, 0.1]}, 'sq': [1.04, 0.97, 1.04], 'bend': {'spine': [0.22, 0.3, 0, 1, None]}}, toonDur=0.04, toonEase='in'), k(SL15 - 0.04, look=FINE15),   # and onto the wall: his arm goes all the way
            k(SL15 + 0.14, toon={'hands': {'R': 'open'}, 'settle': 0.5}, toonDur=0.14), k(SL15 + 0.16, look='mec'), k(SL15 + 0.2, clip='salute', blend=0.12)]),
        act('ombreflic', [SX, 0, ZC14 + LAGC], 0, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon=PALM(SX, ZC14 + LAGC, sq=FLATX), toonDur=0.0),
            k(P15, toon={'sq': FLATX}, toonDur=0.1), k(W15, clip='writeOnHeld', blend=0.1), k(SL15 - 0.16, clip='stand', blend=0.08), k(SL15 + 0.2, clip='salute', blend=0.12)])],
        props=[WALL(Z13 + 0.5), P('fine', 'fineSlip', pos=[HX - 0.3, 1.8, round(ZC14 + 0.3, 3)], ry=-90, opts={'w': 0.36}, keys=[k(0.0, visible=False), k(SL15 - 0.16, visible=True),
                    k(SL15 - 0.04, to=FINE15, dur=0.04, ease='in')]),
               P('slap', 'impactStars', pos=[FINE15[0] - 0.02, FINE15[1], FINE15[2]], ry=-90, opts={'at': SL15, 'n': 6, 'r': 0.42, 'r0': 0.2, 'dur': 0.28, 'size': 0.07})],
        fx=[{'type': 'shake', 'at': SL15, 'dur': 0.14, 'amount': 0.018}],
        cams=[wallcam(0.0, round(ZS14 - 0.55, 3), round(ZS14 - 0.5, 3), d=4.9, h=1.4, lh=1.35), glide([wallcam(SL15 - 0.1, round(ZS14 - 0.1, 3), round(ZS14 - 0.05, 3), d=4.0, h=1.4, lh=1.35)], 0.3)])
st.cue('sfx:tick', 'S15', P15, 0.25); st.cue('sfx:slideDown', 'S15', M15, 0.25); st.cue('sfx:squeak', 'S15', W15 + 0.1, 0.2); st.cue('clack', 'S15', SL15, 0.6)

# 16: yesterday she came back. He sits on the bench at the wall, slumped, the small one beside him on the wall, swinging her legs. His own shadow
#     slides along the wall and stops over him, hands on her hips. His eyes go to the side; his head; a grin; he is up, arms wide
D16 = st.dur('S16'); Z16 = -34.0; A16, E16, G16, UP16 = 0.42, 0.62, 0.9, 1.06
BEN16 = [round(WX - 0.47, 3), 0, Z16]; SEAT16 = [round(BEN16[0] + 0.05, 3), 0.02, round(Z16 - 0.2, 3)]
OM16 = [SX, 0, round(Z16 + 0.55, 3)]                 # where she stops on the wall: beside the bench, in clear view
st.shot('S16', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', SEAT16, -90, 'sitSlump', 'sad', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gy': 0.6, 'lid': 0.4}}, toonDur=0.0),
            k(E16, toon={'face': {'gx': -0.9, 'brow': 0.6, 'eye': 0.3}}, toonDur=0.07), k(E16 + 0.1, look=OM16[:1] + [1.5] + OM16[2:]), k(E16 + 0.12, expr='surprised'),      # his eyes, then his head: her
            k(G16, look=[WX - 4.5, 1.4, Z16 + 0.2]), k(G16, expr='bigGrin'), k(G16, toon={'sq': [1.04, 0.95, 1.04], 'face': {'brow': 1}}, toonDur=0.08),                           # to us: a grin; he gathers himself
            k(UP16, clip='armsUp', blend=0.08), k(UP16, to=[SEAT16[0] - 0.25, 0, SEAT16[2]], dur=0.12, glide=True, ease='out', face=-90), k(UP16, toon={'sq': [0.9, 1.14, 0.9]}, toonDur=0.06, toonEase='out'),   # up, arms wide
            k(UP16 + 0.1, toon={'sq': [1.03, 0.97, 1.03], 'settle': 0.7}, toonDur=0.08)]),
        act('petite', [SX, 0.5, round(Z16 - 0.62, 3)], -90, 'sitEdge', 'happy', keys=[k(0.0, look=None), k(0.0, toon={'sq': FLATZ}, toonDur=0.0), k(A16 + 0.1, look=OM16[:1] + [1.6] + OM16[2:]), k(A16 + 0.14, toon={'sq': [0.9, 1.1, 0.03]}, toonDur=0.08)]),   # she sees the big one: sits up straight
        act('ombre', [SX, 0, round(Z16 + 3.2, 3)], -90, 'handsOnHips', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': [1.0, 1.0, 0.03], 'bend': {'spine': [0, 0, -0.16, 1, None]}}, toonDur=0.0),
            k(0.0, to=OM16, dur=A16, clip='handsOnHips', glide=True, ease='out', face=-90),                                                               # she slides in along the wall, facing out of it, hands on her hips, leaning into it
            k(A16 - 0.04, toon={'sq': [1.06, 0.96, 0.03], 'bend': {'spine': [0, 0, 0.12, 1, None]}}, toonDur=0.06), k(A16 + 0.04, toon={'sq': FLATZ, 'settle': 0.5}, toonDur=0.1), k(A16 + 0.1, look=[WX - 4.5, 1.2, Z16 - 0.2])])],   # stops: her eyes on him
        props=[WALL(Z16 + 2.0), P('bench', 'bench', pos=BEN16, ry=-90, opts={'w': 2.0})],
        cams=[wallcam(0.0, Z16 + 0.1, Z16 + 0.35, d=5.6, h=1.3, lh=1.4)])   # the frame slides right with her arrival, to the frame of the next shot
st.cue('sfx:slideUp', 'S16', A16 - 0.2, 0.25); st.cue('pop', 'S16', G16, 0.3); st.cue('sfx:boing', 'S16', UP16, 0.3)

# 17: with a lawyer. A second shadow slides in beside hers: a gown, the two white tabs of a barrister under the chin, a briefcase; a flat hand comes
#     up: stop. His arms come down; a lump goes down his throat; his pupils shake. The small one tiptoes out
D17 = st.dur('S17'); A17, H17, G17 = 0.3, 0.42, 0.62   # the lawyer is there; the hand; the gulp
AV17 = [SX, 0, round(OM16[2] + 0.72, 3)]              # the lawyer: beside her, inside the frame (at 0.95 the edge cut him in two)
st.shot('S17', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('mec', [SEAT16[0] - 0.25, 0, SEAT16[2]], -90, 'armsUp', 'bigGrin', blink=0, keys=[k(0.0, look=[WX - 4.5, 1.4, Z16 + 0.2]),
            k(A17 - 0.06, toon={'face': {'gx': -0.9, 'brow': 0.5}}, toonDur=0.06), k(A17 + 0.04, look=AV17[:1] + [1.5] + AV17[2:]), k(A17 + 0.06, expr='worried'),          # his eyes, his head: who is that
            k(A17 - 0.02, clip='stand', blend=0.16), k(A17 - 0.02, toon={'sq': [1.03, 0.96, 1.03], 'bend': {'spine': [0.1, 0, 0, 0.97, None]}}, toonDur=0.16),               # his arms come down as the second one arrives (wide open, they covered both shadows)
            k(G17 - 0.06, look=[WX - 4.3, 1.45, Z16 + 0.3]), k(G17, toon={'face': {'gulp': 0.0, 'brow': 0.9, 'eye': 0.35, 'pupilShake': 1, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.04),
            k(G17 + 0.04, toon={'face': {'gulp': 1.0, 'brow': 0.9, 'eye': 0.35, 'pupilShake': 1, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.26, toonEase='linear'),              # to us: a lump goes down; his pupils shake
            k(G17 + 0.32, toon={'face': {'brow': 0.9, 'eye': 0.35, 'pupilShake': 0.6, 'tremble': 1, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.06)]),
        act('petite', [SX, 0.5, round(Z16 - 0.62, 3)], -90, 'sitEdge', 'worried', keys=[k(0.0, look=AV17[:1] + [1.6] + AV17[2:]), k(0.0, toon={'sq': FLATZ}, toonDur=0.0),
            k(H17, to=[SX, 0, round(Z16 - 1.0, 3)], dur=0.1, clip='stand', glide=True, ease='in', face=180), k(H17 + 0.06, toon={'sq': FLATX}, toonDur=0.06),
            k(H17 + 0.1, to=[SX, 0, round(Z16 - 3.4, 3)], dur=0.5, clip='sneak', ease='in', face=180)]),                                                                    # she slips off the bench and tiptoes out
        act('ombre', OM16, -90, 'handsOnHips', 'neutral', keys=[k(0.0, look=[WX - 4.5, 1.2, Z16 - 0.2]), k(0.0, toon={'sq': FLATZ}, toonDur=0.0), k(A17 + 0.1, look=None), k(A17 + 0.1, clip='nod', blend=0.1)]),   # she nods to her counsel
        act('avocat', [SX, 0, round(AV17[2] + 2.4, 3)], -90, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={'sq': [1.0, 1.0, 0.03], 'bend': {'spine': [0, 0, -0.16, 1, None]}}, toonDur=0.0),
            k(0.0, to=AV17, dur=A17, clip='stand', glide=True, ease='out', face=-90), k(A17 - 0.04, toon={'sq': [1.06, 0.96, 0.03], 'bend': {'spine': [0, 0, 0.12, 1, None]}}, toonDur=0.06), k(A17 + 0.04, toon={'sq': FLATZ, 'settle': 0.5}, toonDur=0.08),   # he slides in the same way
            k(H17, toon={'sq': [1.0, 1.04, 0.03], 'hands': {'R': 'spread'}, 'scl': {'handR': [1.7, 1.7, 1.7]}, 'reach': {'R': [SX, 1.98, round(AV17[2] - 0.36, 3), 1, 0.1]}}, toonDur=0.08, toonEase='outBack'),   # a flat hand: stop: up between their two heads, on bare wall (at shoulder height it was black on her black shoulder)
            k(H17 + 0.06, look=[WX - 4.5, 1.2, Z16 - 0.2])])],
        props=[WALL(Z16 + 2.0), P('bench', 'bench', pos=BEN16, ry=-90, opts={'w': 2.0}),
               P('rabat', 'rabat', on={'actor': 'avocat', 'joint': 'neck', 'offset': [0, 0.03, 0.6]}, opts={'s': 2.0}),   # (he is flattened thirty times: half a metre in front of his neck is 2 cm)
               P('case', 'briefcase', on={'actor': 'avocat', 'hand': 'L', 'offset': [0, -0.2, 0]}, opts={'color': INK}, scale=1.1)],
        cams=[wallcam(0.0, Z16 + 0.35, Z16 + 0.35, d=5.6, h=1.3, lh=1.4), glide([wallcam(G17 - 0.08, Z16 - 0.05, Z16 - 0.1, d=3.3, h=1.4, lh=1.45)], 0.24)])   # the frame of the last shot (him, her, her counsel); then in on him for the gulp
st.cue('sfx:slideUp', 'S17', 0.05, 0.25); st.cue('pop', 'S17', H17, 0.35); st.cue('sfx:gasp', 'S17', G17, 0.25)

# 18: the judge has ruled: the gavel
D18 = st.dur('S18'); HIT18 = 0.6
st.shot('S18', **JUDGE(hit=HIT18, nameplate='TRIBUNAL'))
st.cue('clack', 'S18', HIT18, 0.7)

# 19: shared custody. A calendar drops over the front of his bench: GARDE ALTERNÉE: a day for him (pale), a day for her (dark); a red frame hops from
#     day to day; over the edge of the bench the judge's eyes follow it
D19 = st.dur('S19'); CAL19 = [-0.1, 0.7, -12.24]
st.shot('S19', 'replicaCourt', setOpts={'handle': 'TRIBUNAL', 'windowX': -1.5, 'chairW': 1.2, 'chairH': 2.75, 'chairX': 0.15, 'benchGlow': '#5A564A'},
        actors=[act('juge', [-0.35, -0.3, -14.0], -35, 'stand', 'smug', keys=[k(0.0, look=[CAL19[0], 0.2, -11.6]), k(0.0, toon={'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'gy': 0.8}}, toonDur=0.0),
            *[k(0.3 + 0.2 * i, toon={'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'gy': 0.8, 'gx': 0.5 - 0.33 * i}}, toonDur=0.06) for i in range(4)],
            k(1.06, look=[0.0, 1.2, -9.6]), k(1.08, toon={'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': {'browL': 0.6, 'lid': 0.4}}, toonDur=0.1)])],
        props=[P('cal', 'custodyCalendar', pos=[CAL19[0], CAL19[1] + 1.1, CAL19[2]], opts={'w': 1.02, 'mark': [[0.3, 0], [0.5, 1], [0.7, 2], [0.9, 3]]}, keys=[k(0.0, to=CAL19, dur=0.14, ease='in'), k(0.14, to=[CAL19[0], CAL19[1] + 0.07, CAL19[2]], dur=0.06, ease='out'), k(0.2, to=CAL19, dur=0.06, ease='in')]),
               P('specs', 'glasses', on={'actor': 'juge', 'joint': 'head', 'offset': [0.02, 0.17, 0.15]}, opts={'r': 0.042, 'dx': 0.07}),
               P('gavel', 'gavel', pos=[-0.37, 1.41, -13.3], rot=[0, 0, -1.5708]), P('block', 'soundBlock', pos=[0.1, 1.18, -13.3])],
        cams=[cam(0.0, [0.0, 1.0, -9.7], [0.0, 1.0, -9.9], [-0.1, 1.08, -13.0], [-0.1, 1.08, -13.0], lens=44)])
st.cue('thud', 'S19', 0.14, 0.45); [st.cue('sfx:tick', 'S19', 0.3 + 0.2 * i, 0.3) for i in range(4)]

# ---- his bedroom, an even day. He sleeps in his bed, in his suit; his shadow lies on the floor beside the bed, flat
ROOM = {'poster': 'JOUR\nPAIR', 'posterBg': '#1B2F6B', 'posterFg': '#F4F1E8'}
BEDX, BEDZ = -2.6, -1.9                              # the bed of the set: along Z, its pillow at the wall end (-Z)
INBED = [BEDX, 0.62, round(BEDZ + 0.1, 3)]            # him, on the bed, on his back, his head at the pillow
ONFLOOR = [round(BEDX + 1.05, 3), 0.0, round(BEDZ + 0.2, 3)]   # her, on the floor beside the bed, on her back
FLOORFLAT = [1, 1, 0.05]                              # lying on the back, flat on the floor (the body's own depth is up)
CLOCK20 = [round(BEDX + 0.62, 3), 0.0, round(BEDZ - 0.72, 3)]
CAM20P = [2.3, 2.2, 1.4]
CAM20 = lambda t, dz=0.0, **kw: cam(t, [CAM20P[0], CAM20P[1], CAM20P[2] - dz], [CAM20P[0] - 0.05, CAM20P[1], CAM20P[2] - 0.08 - dz], [-1.75, 0.95, -1.55], [-1.75, 0.95, -1.55], lens=44, **kw)   # three quarters, from the foot of the bed, far enough for her to stand whole in the frame, arms up: she at the left quarter, the floor where he ends from her feet to the right
CAL20 = P('cal', 'custodyCalendar', pos=[-2.4, 1.8, -2.97], opts={'w': 1.0, 'mark': [[0, 1]]})   # the calendar of the judgment, over the bed: the 2 is framed (ELLE)
# 20: on even days. The alarm clock rings and hops; he turns over in his sleep; on the floor two white eyes open
D20 = st.dur('S20'); R20 = 0.08
st.shot('S20', 'chambre', setOpts=ROOM, actors=[
        act('mec', INBED, 0, 'lieBack', 'sleepy', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 1}}, toonDur=0.0),
            k(R20 + 0.1, toon={'face': {'lid': 1, 'brow': -0.6, 'mouth': 'wavy'}, 'bend': {'spine': [0, 0.2, 0, 1, None]}}, toonDur=0.1), k(R20 + 0.4, toon={'face': {'lid': 1, 'brow': -0.8, 'mouth': 'clench'}, 'bend': {'spine': [0, -0.2, 0, 1, None]}}, toonDur=0.16)]),   # he frowns in his sleep, turns a little
        act('ombre', ONFLOOR, 0, 'lieBack', 'sleepy', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLOORFLAT, 'face': {'lid': 1}}, toonDur=0.0),
            k(R20 + 0.28, toon={'sq': FLOORFLAT, 'face': {'eye': 0.5}}, toonDur=0.04), k(R20 + 0.28, expr='surprised')])],                                          # her eyes open: two white eyes on the floor
        props=[P('clock', 'alarmClock', pos=CLOCK20, ry=47, scale=1.0, opts={'time': '07:00', 'ringAt': R20, 'button': 'ARRÊT'}), CAL20],
        cams=[CAM20(0.0)])
st.cue('sfx:ding', 'S20', R20, 0.5); st.cue('sfx:ding', 'S20', R20 + 0.3, 0.45); st.cue('sfx:ding', 'S20', R20 + 0.6, 0.4)

# 21: she is the one who gets up. A flat black arm comes up off the floor and shuts the clock; she sits up, stands: the flat figure fills out into a body
#     as it rises; she stretches, both arms up (his stretch of the other morning); and he, on the bed, goes flat as a sheet and slips to the floor behind her
D21 = st.dur('S21'); H21, S21T, U21, F21, X21 = 0.1, 0.24, 0.42, 0.5, 0.66   # her hand on the clock; she sits up; she is up; he goes flat; she stretches
UP21 = [round(ONFLOOR[0] + 0.05, 3), 0, round(ONFLOOR[2] + 0.9, 3)]            # where she stands: where her feet were (lying, an actor's place is the middle of the body; standing, the feet)
SIT21 = [ONFLOOR[0], 0, round(ONFLOOR[2] + 0.12, 3)]
_l21 = (round(0.32 * math.cos(math.radians(50)), 3), round(-0.32 * math.sin(math.radians(50)), 3))   # her left, when she faces 50 degrees
DN21 = [ONFLOOR[0], 0.0, round(ONFLOOR[2] - 0.05, 3)]                         # where he ends: on the floor, where she lay, his feet at her feet: the shadow of a shadow
st.shot('S21', 'chambre', setOpts=ROOM, actors=[
        act('ombre', ONFLOOR, 0, 'lieBack', 'surprised', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLOORFLAT, 'face': {'eye': 0.5}}, toonDur=0.0),
            k(H21 - 0.08, toon={'sq': FLOORFLAT, 'hands': {'R': 'open'}, 'reach': {'R': [CLOCK20[0], 0.5, CLOCK20[2] + 0.05, 1, 0.08]}, 'bend': {'armR': [0, 0, 0, 1.4, None]}}, toonDur=0.08, toonEase='in'),   # a flat arm, on the clock
            k(S21T, to=SIT21, dur=0.08, clip='sitFloor', then='sitFloor', glide=True, ease='out', face=0, blend=0.12), k(S21T, toon={'sq': [1, 1, 0.45]}, toonDur=0.14, toonEase='out'),                                      # she sits up: she fills out
            k(U21 - 0.1, to=UP21, dur=0.12, clip='stand', then='stand', glide=True, ease='out', face=50, blend=0.12),   # then: without it, at the end of the move she went back to the clip she had before (lying) k(U21 - 0.1, toon={'sq': [0.92, 1.12, 0.92], 'auto': 0.4}, toonDur=0.1, toonEase='out'),   # up: a body
            k(U21 + 0.04, toon={'sq': [1.04, 0.96, 1.04], 'settle': 0.6}, toonDur=0.08),
            k(X21 - 0.06, expr='yawn'), k(X21, toon={'hands': {'L': 'spread', 'R': 'spread'}, 'reach': {'L': [round(UP21[0] + _l21[0], 3), 2.5, round(UP21[2] + _l21[1], 3), 1, 0.08], 'R': [round(UP21[0] - _l21[0], 3), 2.5, round(UP21[2] - _l21[1], 3), 1, 0.08]}, 'sq': [0.93, 1.1, 0.93], 'bend': {'spine': [-0.18, 0, 0, 1.06, None]}}, toonDur=0.16, toonEase='out'),   # she stretches
            k(X21 + 0.32, toon={'sq': [1.0, 1.0, 1.0], 'settle': 0.5}, toonDur=0.12), k(X21 + 0.34, look=CAM20P), k(X21 + 0.34, expr='neutral')]),          # her eyes to us
        act('mec', INBED, 0, 'lieBack', 'sleepy', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 1, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.0),
            k(F21, toon={'sq': [1.08, 1.04, 0.07], 'face': {'eye': 0.4, 'brow': 1}}, toonDur=0.1, toonEase='in'), k(F21 + 0.02, expr='surprised'),               # he goes flat: his eyes open
            k(F21 + 0.1, path=[[round(BEDX + 0.6, 3), 0.66, INBED[2] + 0.05], DN21], dur=0.26, clip='lieBack', then='lieBack', glide=True, ease='inOut', face=0),   # and slips off the bed like a sheet
            k(F21 + 0.36, toon={'sq': [1.1, 1.0, 0.05], 'face': {'brow': 0.6, 'eye': 0.3}}, toonDur=0.04), k(F21 + 0.44, toon={'sq': FLOORFLAT, 'settle': 0.4, 'face': {'brow': 0.3, 'lid': 0.4}}, toonDur=0.08), k(F21 + 0.46, expr='unimpressed')])],
        props=[P('clock', 'alarmClock', pos=CLOCK20, ry=47, scale=1.0, opts={'time': '07:00', 'ringAt': 0.0, 'stopAt': H21, 'button': 'ARRÊT'}), CAL20],
        cams=[CAM20(0.0, 0.1)])
st.cue('clack', 'S21', H21, 0.5); st.cue('sfx:slideUp', 'S21', S21T, 0.3); st.cue('sfx:stretch', 'S21', X21, 0.3); st.cue('sfx:slideDownSlow', 'S21', F21 + 0.1, 0.3); st.cue('thud', 'S21', F21 + 0.36, 0.2)

# ---- the street again: she walks, upright, a body of shade with two white eyes; he follows
Z22 = 0.55
zs22 = lambda t: round(Z22 + 2.3 - VW * 1.15 * t, 3)   # her z
# 22: he follows. The wall of the first shot: she comes along it, head high, where he walked; the frame goes with her; behind her, on the wall: nothing
D22 = st.dur('S22')
st.shot('S22', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('ombre', [HX, 0, zs22(0.0)], 180, 'marchPomp', 'proud', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, zs22(D22)], dur=D22, clip='marchPomp', ease='linear', face=180, cruise=True),
            k(0.75, look=[WX - 5.3, 1.5, zs22(0.9)]), k(1.1, look=None)])],                                                                 # her white eyes come to us, as his did; and go
        props=[WALL(2.0)],
        cams=[wallcam(0.0, zs22(0.0) + 0.5, zs22(D22) + 0.5)])
st.cue('whoosh', 'S22', 0.0, 0.2, 0.4, 300, 1200)

# 23: on the ground. From above, ahead of her: he slides along the pavement behind her heels, on his back, flat, his feet first, looking at the sky
D23 = st.dur('S23'); V23 = VW * 1.15
zs23 = lambda t: round(zs22(D22) - V23 * t, 3)
DRAG = 1.0                                            # his hips, that far behind her heels
def dragcam(t0, t1, zf, x0=HX, side=0.3, up=4.6, ahead=0.1, lens=44, push=0.0, **kw):
    # from straight above, almost: the way a shadow on the ground is seen. She is a dark shape at the bottom left, seen from over her head; he lies up
    # the frame from her heels, on a diagonal, his face the right way up, clear of her from the knees (lower and further ahead, she stood in front of
    # him: a dark mass cut by the edge of the frame, or over half of his body). push: the camera comes down toward his head over the shot (0..1)
    a = [x0 - side, up, zf(t0) - ahead]; b = [x0 - side, up, zf(t1) - ahead]; la = [x0, 0.0, zf(t0) + 0.7]; lb = [x0, 0.0, zf(t1) + 0.7]
    if push:
        hd = [x0 + 0.05, 0.1, zf(t1) + 1.45]; b = [b[i] + (hd[i] - b[i]) * push for i in range(3)]; lb = [lb[i] + (hd[i] - lb[i]) * min(1.0, push * 1.6) for i in range(3)]
    return cam(t0, [round(v, 3) for v in a], [round(v, 3) for v in b], [round(v, 3) for v in la], [round(v, 3) for v in lb], lens=lens, **kw)
FLAT23 = [1.06, 1.0, 0.1]
st.shot('S23', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('ombre', [HX, 0, zs23(0.0)], 180, 'marchPomp', 'proud', keys=[k(0.0, look=None), k(0.0, to=[HX, 0, zs23(D23)], dur=D23, clip='marchPomp', ease='linear', face=180, cruise=True)]),
        act('mec', [HX, 0, round(zs23(0.0) + DRAG, 3)], 180, 'lieBack', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLAT23, 'face': {'lid': 0.4}}, toonDur=0.0),
            k(0.0, to=[HX, 0, round(zs23(D23) + DRAG, 3)], dur=D23, clip='lieBack', then='lieBack', glide=True, ease='linear', face=180, cruise=True),
            k(0.36, toon={'sq': [1.06, 1.0, 0.16], 'face': {'eye': 0.3, 'brow': 0.8}}, toonDur=0.03), k(0.42, toon={'sq': FLAT23, 'settle': 0.4, 'face': {'lid': 0.4}}, toonDur=0.08),   # a joint in the paving: a bump
            k(0.5, toon={'sq': FLAT23, 'face': {'lid': 0.4, 'gx': 0.5, 'gy': 0.5}}, toonDur=0.08)])],                                       # his eyes come to us
        props=[WALL(2.0)],
        cams=[dragcam(0.0, D23, zs23)])
st.cue('sfx:slideDownSlow', 'S23', 0.0, 0.25); st.cue('thud', 'S23', 0.36, 0.25)

# 24: he says tarmac is fine. She has taken to the road; he slides after her on the smooth tarmac, his hands behind his head, an ankle on a knee; on
#     « ça va » a thumb comes up
D24 = st.dur('S24'); RX = 3.4; Z24 = -8.0; TH24 = round(26.79 - st.SH['S24'][0], 3)
zs24 = lambda t: round(Z24 - V23 * t, 3)
st.shot('S24', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('ombre', [RX, 0, zs24(0.0)], 180, 'marchPomp', 'proud', keys=[k(0.0, look=None), k(0.0, to=[RX, 0, zs24(D24)], dur=D24, clip='marchPomp', ease='linear', face=180, cruise=True)]),
        act('mec', [RX, 0, round(zs24(0.0) + DRAG, 3)], 180, 'lieRelax', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLAT23, 'face': {'lid': 0.4, 'gx': 0.5, 'gy': 0.5}}, toonDur=0.0),
            k(0.0, to=[RX, 0, round(zs24(D24) + DRAG, 3)], dur=D24, clip='lieRelax', then='lieRelax', glide=True, ease='linear', face=180, cruise=True),
            k(0.5, toon={'sq': FLAT23, 'face': {'lid': 0.4, 'gx': 0.5, 'gy': 0.5, 'lidL': 1}}, toonDur=0.05), k(0.62, toon={'sq': FLAT23, 'face': {'lid': 0.4, 'gx': 0.5, 'gy': 0.5}}, toonDur=0.05),                     # a blink
            k(TH24 - 0.12, toon={'sq': FLAT23, 'hands': {'R': 'thumbUp'}, 'reach': {'R': [RX - 0.55, 0.5, round(zs24(TH24) + DRAG + 0.55, 3), 1, 0.06]}, 'face': {'lid': 0.35, 'gx': 0.5, 'gy': 0.5, 'mouth': 'smirk'}}, toonDur=0.12, toonEase='outBack'),   # a thumb: it is fine
            *[k(TH24 + 0.1 * i, toon={'sq': FLAT23, 'hands': {'R': 'thumbUp'}, 'reach': {'R': [RX - 0.55, 0.5 + (0.04 if i % 2 else 0.0), round(zs24(TH24 + 0.1 * i) + DRAG + 0.55, 3), 1, 0.06]}, 'face': {'lid': 0.35, 'gx': 0.5, 'gy': 0.5, 'mouth': 'smirk'}}, toonDur=0.1) for i in range(1, int((D24 - TH24) / 0.1) + 1)]])],
        cams=[dragcam(0.0, D24, zs24, x0=RX)])
st.cue('whoosh', 'S24', 0.0, 0.15, D24, 200, 700); st.cue('sfx:ding', 'S24', TH24, 0.3)

# 25: cobbles, less so. The setts come up the frame: her heels click on them; then his heels, his back, his head: he rattles over each one: his body
#     ripples, his head hammers, his pupils shake, his thumb is still up and shakes too
D25 = st.dur('S25'); C25 = 0.26                        # his heels reach the first sett
zs25 = lambda t: round(zs24(D24) - V23 * t, 3)
ZC25 = round(zs25(C25) + DRAG - 0.9, 3)               # the near end of the cobbles (his heels are there at C25)
def rattle(t0, t1, zf):
    ks = []; n = int((t1 - t0) / 0.066)
    for i in range(n):
        t = round(t0 + 0.066 * i, 3); a = 1 if i % 2 else -1; w = min(1.0, (i + 1) / 4)   # it climbs from his heels to his head in four hits
        ks.append(k(t, toon={'sq': [1.06, 1.0 - 0.03 * a * w, 0.1 + 0.05 * (a > 0) * w], 'hands': {'R': 'thumbUp'}, 'reach': {'R': [RX - 0.55 + 0.03 * a, 0.5 + 0.05 * a * w, round(zf(t) + DRAG + 0.55, 3), 1, 0.06]},
                         'bend': {'spine': [0.14 * a * w, 0, 0, 1, None], 'neck': [-0.3 * a * w, 0, 0.1 * a * w, 1, None]}, 'face': {'eye': 0.35, 'brow': 0.9, 'pupilShake': w, 'tremble': w, 'jaw': 0.25 + 0.2 * (a > 0), 'cheeks': 0.6 * w}}, toonDur=0.05))
    return ks
st.shot('S25', 'parisStreet', setOpts=STREET, look=SUN, actors=[
        act('ombre', [RX, 0, zs25(0.0)], 180, 'marchPomp', 'proud', keys=[k(0.0, look=None), k(0.0, to=[RX, 0, zs25(D25)], dur=D25, clip='marchPomp', ease='linear', face=180, cruise=True)]),
        act('mec', [RX, 0, round(zs25(0.0) + DRAG, 3)], 180, 'lieRelax', 'unimpressed', blink=0, keys=[k(0.0, look=None),
            k(0.0, toon={'sq': FLAT23, 'hands': {'R': 'thumbUp'}, 'reach': {'R': [RX - 0.55, 0.5, round(zs25(0.0) + DRAG + 0.55, 3), 1, 0.06]}, 'face': {'lid': 0.35, 'gx': 0.5, 'gy': 0.5, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.0, to=[RX, 0, round(zs25(D25) + DRAG, 3)], dur=D25, clip='lieRelax', then='lieRelax', glide=True, ease='linear', face=180, cruise=True),
            k(C25 - 0.1, toon={'sq': FLAT23, 'hands': {'R': 'thumbUp'}, 'reach': {'R': [RX - 0.55, 0.5, round(zs25(C25 - 0.1) + DRAG + 0.55, 3), 1, 0.06]}, 'face': {'eye': 0.3, 'brow': 0.7, 'gy': 0.9}}, toonDur=0.08), k(C25 - 0.1, expr='worried'),   # his eyes go down to what is coming
            *rattle(C25, D25, zs25)])],
        props=[P('cob', 'cobbles', pos=[RX, 0, round(ZC25 - 4.0, 3)], opts={'len': 8.0, 'w': 2.6, 'h': 0.05})],
        fx=[{'type': 'shake', 'at': C25, 'dur': round(D25 - C25, 3), 'amount': 0.008}],
        cams=[dragcam(0.0, D25, zs25, x0=RX, push=0.3, ease='inOut')])   # it comes down on him as he rattles
[st.cue('clack', 'S25', round(C25 + 0.066 * i, 3), 0.28 if i % 2 else 0.2) for i in range(int((D25 - C25) / 0.066))]

# 26: the end. A crossing: the red man. She stops at the kerb; he slides on between her feet, past her, into the road: half a second late: comes back
#     under her like elastic; she looks at her watch; taps a foot; his eyes come to us; a slow blink
D26 = st.dur('S26'); Z26 = -40.0; ST26, OV26, BK26, W26 = 0.3, 0.52, 0.74, 0.9
PL26 = [7.25, 0, round(Z26 - 0.8, 3)]   # the light: beyond them, at the left of the picture (at the kerb, in front of the camera, its pole crossed his way)
st.shot('S26', 'parisStreet', setOpts={**STREET, 'clear': [-90, 80]}, look=SUN, actors=[
        act('ombre', [HX - 2.4, 0, round(Z26 + V23 * ST26, 3)], 180, 'marchPomp', 'proud', keys=[k(0.0, look=None), k(0.0, to=[HX - 2.4, 0, Z26], dur=ST26, clip='marchPomp', ease='linear', face=180, cruise='in'),
            k(ST26, clip='stand', blend=0.08), k(ST26, toon={'sq': [1.04, 0.96, 1.04], 'settle': 0.5}, toonDur=0.06),
            k(ST26 + 0.1, look=[HX - 2.4, 0.1, round(Z26 - 0.9, 3)]), k(BK26 + 0.04, look=None),                                                              # her eyes go down to him as he comes out between her feet
            k(W26, clip='checkWatch', blend=0.12)]),                                                                                                  # then her watch: he is late
        act('mec', [HX - 2.4, 0, round(Z26 + V23 * ST26 + DRAG, 3)], 180, 'lieBack', 'unimpressed', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'sq': FLAT23, 'face': {'lid': 0.4}}, toonDur=0.0),
            k(0.0, to=[HX - 2.4, 0, round(Z26 + DRAG, 3)], dur=ST26, clip='lieBack', then='lieBack', glide=True, ease='linear', face=180, cruise='in'),          # behind her heels, at her pace
            k(ST26, to=[HX - 2.4, 0, round(Z26 - 0.5, 3)], dur=round(OV26 - ST26, 3), clip='lieBack', then='lieBack', glide=True, ease='out', face=180),          # she has stopped: he goes on, between her feet: his head stops under her (further, his feet left the frame)
            k(ST26 + 0.04, toon={'sq': [1.0, 1.25, 0.08], 'face': {'eye': 0.4, 'brow': 1}}, toonDur=0.12, toonEase='out'), k(ST26 + 0.04, expr='surprised'),          # stretched by the pull
            k(OV26 + 0.04, to=[HX - 2.4, 0, round(Z26 + DRAG - 0.1, 3)], dur=round(BK26 - OV26 - 0.04, 3), clip='lieBack', then='lieBack', glide=True, ease='in', face=180),   # and back, like elastic
            k(BK26 - 0.02, toon={'sq': [1.2, 0.86, 0.1], 'face': {'eye': 0.3, 'brow': 0.6}}, toonDur=0.04), k(BK26 + 0.06, toon={'sq': FLAT23, 'settle': 0.6, 'face': {'lid': 0.4}}, toonDur=0.1), k(BK26 + 0.06, expr='unimpressed'),
            k(W26 + 0.25, toon={'sq': FLAT23, 'face': {'lid': 0.4, 'gx': -0.6, 'gy': 0.3}}, toonDur=0.1),                                                            # his eyes to us
            k(W26 + 0.5, toon={'sq': FLAT23, 'face': {'lid': 1, 'gx': -0.6, 'gy': 0.3}}, toonDur=0.08), k(W26 + 0.64, toon={'sq': FLAT23, 'face': {'lid': 0.45, 'gx': -0.6, 'gy': 0.3}}, toonDur=0.08)])],   # a slow blink
        props=[P('light', 'trafficLight', pos=PL26, ry=44, opts={'state': [[0, 'g']], 'headRy': -44, 'poleColor': '#98A0A8', 'housing': '#2E4A3B', 'ped': 'r'}),   # the red man faces the camera
               P('watch26', 'wristWatch', on={'actor': 'ombre', 'hand': 'L', 'offset': [0, 0.075, 0.0], 'rot': [0, 0, 0]}, opts={'s': 2.4, 'dialR': 0.03, 'both': True, 'bright': True})],   # a white dial: on a silhouette, an arm in front of the body is black on black
        cams=[cam(0.0, [3.85, 2.65, Z26 - 4.35], [3.9, 2.65, Z26 - 4.25], [6.5, 0.6, Z26 - 0.4], [6.5, 0.6, Z26 - 0.4], lens=44)])   # from above, well ahead of her, on the road side: his way runs along the diagonal of the frame: behind her up to the right, ahead of her down to the left
st.cue('sfx:squeak', 'S26', ST26, 0.3); st.cue('sfx:stretch', 'S26', ST26 + 0.04, 0.35); st.cue('sfx:twang', 'S26', OV26 + 0.04, 0.4); st.cue('thud', 'S26', BK26, 0.3); st.cue('sfx:tick', 'S26', W26 + 0.05, 0.3)

st.write("L'ombre", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, clothGravity=True, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'castShadow': False},
    'ombre': {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'silhouette': INK, 'darkEyes': 1.5},
    'clerk': {'preset': 'mamie', 'seed': 141, 'build': {'width': 0.9, 'headWidth': 1.3, 'height': 0.94}},
    'grand': {'preset': 'fringant', 'seed': 143, 'build': {'width': 0.8, 'headWidth': 1.2, 'height': 1.3}, 'castShadow': False},
    'petite': {'preset': 'lemec', 'build': {'width': 0.9, 'headWidth': 1.35, 'height': 0.5}, 'silhouette': INK, 'darkEyes': 1.6},
    'flic': {'preset': 'cop', 'seed': 151, 'build': {'width': 0.92, 'headWidth': 1.3}, 'castShadow': False},
    'ombreflic': {'preset': 'cop', 'seed': 151, 'build': {'width': 0.92, 'headWidth': 1.3}, 'silhouette': INK, 'darkEyes': 1.5},
    'avocat': {'preset': 'avocat', 'seed': 153, 'build': {'width': 0.9, 'headWidth': 1.3}, 'silhouette': INK, 'darkEyes': 1.5}})
