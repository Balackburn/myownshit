#!/usr/bin/env python3
"""Le boomerang (story 52, cycle 14 of the cartoon staging): this man threw a boomerang ten years ago. It never came back. The lost-property office
refused his declaration: a boomerang is not lost, it comes back. The air-traffic controllers opened it an air corridor. Planes give way to it.
Yesterday it came back, right during his wedding photo. He left with it. His wife is waiting for him. In ten years.
Staging: the throw as a rubber-band windup (the arm stretched back twice its length, the spine twisted, a tongue of concentration), the whip, the
corkscrew of the follow-through; waiting with his hand out, a passer-by drops a coin in it; at the lost-property counter the clerk holds up his form,
then her stamp comes down on the form and on his fingers (the hand flattened, then popping back); to make her point she throws her own little
boomerang round the room: his head follows it all the way round, a full turn on his neck, and snaps back; the controller sways round in circles with
the blip on his radar before drawing the corridor; in the sky, a corridor of orange cones standing on the clouds; an airliner brakes like a car at a
zebra crossing painted on the clouds (nose down, squashed), the boomerang crosses, the plane sets off again; the town-hall steps, everyone smiling for
the photo: the boomerang lands on his head, squashes it flat and keeps turning like a rotor: he lifts off, deadpan, still smiling, his body slowly
turning the other way under it; the bride in the park, her hand out, a child drops a coin in it, and far up in the sky a speck with a rotor goes by.
Natural look; cycle 14 tools: the review of 49-51 (the takes in the body, the lettering, the faces cheated to the lens), hairRest."""
from story_kit import *
import math

st = Story('boomerang', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 4), ('S06', 'L04', 0), ('S07', 'L04', 5),
         ('S08', 'L05', 0), ('S09', 'L05', 7), ('S10', 'L06', 0), ('S11', 'L07', 0), ('S12', 'L08', 0), ('S13', 'L08', 4), ('S14', 'L09', 0),
         ('S15', 'L10', 0), ('S16', 'L10', 3)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
def FWDV(ry): return (math.sin(math.radians(ry)), math.cos(math.radians(ry)))
def OFF(p, ry, fwd=0.0, rgt=0.0, y=0.0):                           # a point in front of / to the right of someone facing ry
    f = FWDV(ry); rr = (-f[1], f[0]); return [r(p[0] + fwd * f[0] + rgt * rr[0]), y, r(p[2] + fwd * f[1] + rgt * rr[1])]

PARK = {'seed': 31}
P0 = [0.0, 0, 0.0]; RY0 = -35                                         # in the park, three-quarter to us, turned toward the sky on screen left (at -70 the audit read a profile)
BOOM = lambda pid, **kw: P(pid, 'boomerang', **kw)
CUPPED = [0.3, 0.32, 0.36, 0.4, 0.25, 0.15]                          # a hand held out to receive
OUT = lambda who_p, ry: {'reach': {'R': [*OFF(who_p, ry, 0.42, 0.18, 1.12), 1, 0.04]}, 'hands': {'R': CUPPED}}   # the hand held out, palm up, waiting

# 1: the hook. In the park: a rubber-band windup, the boomerang over his shoulder, the arm stretched back twice its length, the spine wound up, the tip of
#    the tongue out; held; on « lancé » the whip forward, the boomerang gone off the top left, the follow-through pose
D1 = st.dur('S01'); REL1 = round(st.at('S01', 'L01', 3) - 0.06, 3)
FRONT1 = OFF(P0, RY0, 0.95, 0.15, 2.45); BACK1 = OFF(P0, RY0, -1.25, 0.35, 1.65)
AIM = {'brow': -0.5, 'lid': 0.35, 'tongue': 0.7, 'tongueLen': 0.12}
st.shot('S01', 'grassland', setOpts=PARK, actors=[
        act('mec', P0, RY0, 'stand', 'determined', keys=[k(0.0, look=[-3.2, 3.4, 1.6]), k(0.0, toon={'reach': {'R': [*OFF(P0, RY0, 0.0, 0.3, 1.85), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': AIM}, toonDur=0.0),
            k(0.1, toon={'reach': {'R': [*BACK1, 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [-0.15, 0.85, 0, 1, None]}, 'sq': [1.05, 0.95, 1.05], 'face': AIM, 'hose': 0.1}, toonDur=0.32, toonEase='inOut'),   # the windup: the arm stretched far back like a rubber band, the spine wound
            *[k(round(0.44 + 0.04 * i, 3), toon={'reach': {'R': [BACK1[0], r(BACK1[1] + (0.03 if i % 2 else -0.03)), BACK1[2], 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [-0.15, 0.88, 0, 1, None]}, 'sq': [1.06, 0.94, 1.06], 'face': AIM, 'hose': 0.1}, toonDur=0.03) for i in range(3)],   # held, quivering
            k(REL1, toon={'reach': {'R': [*FRONT1, 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.35, -0.9, 0, 1, None]}, 'sq': [0.9, 1.12, 0.9], 'face': {'brow': 0.3, 'lid': 0.0, 'mouth': 'O'}, 'hose': 0.1}, toonDur=0.05, toonEase='out'),   # the whip
            k(round(REL1 + 0.12, 3), toon={'reach': {'R': [*OFF(P0, RY0, 0.85, 0.05, 2.25), 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.45, -0.7, 0, 1, None]}, 'face': {'brow': 0.6, 'lid': 0.1}}, toonDur=0.15),   # the follow-through: leaning after it
            k(round(REL1 + 0.05, 3), look=[-6, 6.5, 3.5])]),
        ],
        props=[BOOM('boom1h', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.06, 0.04], 'rot': [PI / 2, 0, 0]}, scale=1.4, keys=[k(REL1, visible=False)]),
               BOOM('boom1', pos=FRONT1, scale=1.4, opts={'spin': [[REL1, 7.0]], 'wobble': 0.25}, keys=[k(0.0, visible=False), k(REL1, visible=True), k(REL1, to=[-6.5, 7.0, 3.2], dur=0.42, ease='out')]),
               P('bench1', 'bench', pos=[2.2, 0, -1.6], ry=-90), P('lamp1', 'streetLamp', pos=[-2.6, 0, -2.4])],
        cams=[FC(0.0, [0.9, 1.25, 3.6], [[P0[0], 2.55, P0[2]], [P0[0], 0.0, P0[2]], [BACK1[0], BACK1[1], BACK1[2]], [FRONT1[0], FRONT1[1] + 0.25, FRONT1[2]], [r(P0[0] + 0.5), 1.4, P0[2]]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.1))])
st.cue('whoosh', 'S01', 0.1, 0.25, 0.35, 300, 1200); st.cue('whoosh', 'S01', REL1, 0.4, 0.3, 600, 3000)

# 2: ten years ago. From behind him, low: the corkscrew of the follow-through (a turn and a half), a wobble, then he stops facing the sky, a hand at his brow;
#    the boomerang a spinning speck shrinking toward the horizon
D2 = st.dur('S02')
BRW = {'touch': {'R': ['face', 0.0, 0.78, 0.07, 1, 0.06]}, 'hands': {'R': 'open'}}   # a hand at his brow, shading his eyes
st.shot('S02', 'grassland', setOpts=PARK, actors=[
        act('mec', P0, RY0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'bend': {'armR': [0, -1.25, 0, 1, None], 'armL': [0, 1.25, 0, 1, None]}, 'sq': [0.93, 1.08, 0.93], 'face': {'lid': 0.2, 'brow': 0.4}}, toonDur=0.0),   # arms flung out by the spin
            *[k(round(0.03 + 0.085 * i, 3), to=list(P0), dur=0.085, clip='stand', then='stand', face=r(RY0 + 108 * (i + 1), 1)) for i in range(5)],   # a turn and a half on the spot
            k(0.48, toon={'sq': [1.04, 0.96, 1.04], 'bend': {'spine': [0, 0, 0.12, 1, None]}, 'face': {'cross': 0.6, 'lid': 0.3}}, toonDur=0.08), k(0.6, toon={'bend': {'spine': [0, 0, -0.1, 1, None]}, 'face': {'cross': 0.3, 'lid': 0.3}}, toonDur=0.12),   # dizzy, a wobble
            k(0.8, toon={**BRW, 'face': {'lid': 0.4}}, toonDur=0.15), k(0.8, look=[-30, 14, 10])])],   # then a hand at his brow, watching it go
        props=[BOOM('boom2', pos=[-1.5, 3.0, 1.4], scale=1.4, opts={'spin': [[0.0, 7.0]], 'wobble': 0.25}, keys=[k(0.0, to=[-34.0, 15.0, 12.0], dur=round(D2 - 0.05, 3), ease='out')]),
               P('lamp2', 'streetLamp', pos=[-2.6, 0, -2.4])],
        cams=[FC(0.0, [2.9, 0.75, -1.4], [[P0[0], 2.5, P0[2]], [P0[0], 0.0, P0[2]], [-4.0, 4.6, 2.0], [r(P0[0] - 0.5), 1.5, P0[2]]], top=0.1, bottom=0.74, drift=(0.0, 0.03, 0.0))])
st.cue('whoosh', 'S02', 0.05, 0.3, 0.45, 300, 1000)

# 3: it never came back. He waits, deadpan, his hand held out, eyes on the sky; a passer-by walks past and drops a coin in his hand; he looks at the coin,
#    then back up at the sky, the hand still out
D3 = st.dur('S03'); CN3 = round(st.at('S03', 'L02', 2) - 0.02, 3)
HAND3 = OFF(P0, RY0, 0.42, 0.18, 1.12)
st.shot('S03', 'grassland', setOpts=PARK, actors=[
        act('mec', P0, RY0, 'stand', 'unimpressed', keys=[k(0.0, look=[-6, 6.5, 3.5]), k(0.0, toon={**OUT(P0, RY0), 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.25, toon={**OUT(P0, RY0), 'face': {'lid': 1.0}}, toonDur=0.05), k(0.36, toon={**OUT(P0, RY0), 'face': {'lid': 0.45}}, toonDur=0.07),
            k(round(CN3 + 0.12, 3), look=[HAND3[0], 1.0, HAND3[2]]), k(round(CN3 + 0.12, 3), toon={**OUT(P0, RY0), 'bend': {'neck': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.5}}, toonDur=0.1),   # he looks at the coin...
            k(round(CN3 + 0.62, 3), look=[-6, 6.5, 3.5]), k(round(CN3 + 0.62, 3), toon={**OUT(P0, RY0), 'face': {'lid': 0.45}}, toonDur=0.12)]),   # ...and back at the sky
        act('gamin', [2.1, 0, 0.75], -95, 'stand', 'happy', keys=[k(0.0, look=[P0[0], 1.4, P0[2]]), k(0.0, to=[-2.4, 0, 0.95], dur=round(D3 - 0.05, 3), clip='walk', then='walk', ease='linear', face='move'),   # a child: small, he does not hide the man as he passes
            k(round(CN3 - 0.15, 3), toon={'reach': {'L': [HAND3[0], r(HAND3[1] + 0.12), HAND3[2], 1, 0.05]}, 'hands': {'L': 'pinch'}}, toonDur=0.1), k(round(CN3 + 0.08, 3), toon={}, toonDur=0.15), k(round(CN3 + 0.3, 3), look='camera')])],
        props=[P('coin3', 'coin', pos=[HAND3[0], r(HAND3[1] + 0.35), HAND3[2]], scale=1.6, keys=[k(0.0, visible=False), k(round(CN3 - 0.06, 3), visible=True), k(round(CN3 - 0.06, 3), to=[HAND3[0], r(HAND3[1] + 0.03), HAND3[2]], dur=0.08, ease='in')]),
               P('lamp3', 'streetLamp', pos=[-2.6, 0, -2.4])],
        cams=[FC(0.0, [-1.2, 1.45, 2.9], [[P0[0], 2.5, P0[2]], [P0[0], 0.55, P0[2]], [HAND3[0], 1.0, HAND3[2]], [r(P0[0] + 0.55), 1.6, P0[2]], [r(P0[0] - 0.6), 1.6, P0[2]]], top=0.12, bottom=0.74, drift=(0.04, 0.0, -0.08))])
st.cue('sfx:ding', 'S03', CN3, 0.3)

# 4: the lost-property office refused his declaration. The counter of OBJETS TROUVÉS, the shelves of lost things behind: the clerk holds up his form and
#    reads it over her glasses; he waits at the end of the counter, his hand flat on it
OFC = {'title': 'OBJETS TROUVÉS', 'plate': 'DÉCLARATIONS', 'map': False, 'deskZ': -0.9, 'wall': '#E9EEF0', 'band': '#6E8FA6', 'trim': '#3E5A70', 'floor': '#B9B2A4', 'joint': '#A39C8E'}
CLK = [-0.15, 0, -1.65]; ME4 = [0.95, 0, -0.25]; RYME = -55            # the clerk behind the counter facing us; him at its end, three-quarter to us
FORM4 = [-0.15, 1.42, -1.25]                                          # the form held up in her hands, facing us
HOLDF = {'reach': {'L': [r(FORM4[0] - 0.17), r(FORM4[1] - 0.12), r(FORM4[2] - 0.02), 1, 0.05], 'R': [r(FORM4[0] + 0.17), r(FORM4[1] - 0.12), r(FORM4[2] - 0.02), 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}}
FLATH = OFF(ME4, RYME, 0.42, 0.2, 0.86)                               # his hand flat on the counter
ONCTR = {'reach': {'R': [*FLATH, 1, 0.05]}, 'hands': {'R': 'open'}}
D4 = st.dur('S04')
st.shot('S04', 'mairie', setOpts=OFC, actors=[
        act('guichet', CLK, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[FORM4[0], 1.45, FORM4[2]]), k(0.0, toon={**HOLDF, 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.0),
            k(0.45, toon={**HOLDF, 'face': {'lid': 0.5, 'gy': 0.6, 'brow': 0.6}}, toonDur=0.1), k(0.7, look=[ME4[0], 1.9, ME4[2]]), k(0.72, toon={**HOLDF, 'face': {'lid': 0.4, 'brow': 0.8, 'gy': 0.3}}, toonDur=0.08)]),   # she reads, raises a brow, looks at him over her glasses
        act('mec', ME4, RYME, 'stand', 'unimpressed', keys=[k(0.0, look=[FORM4[0], 1.5, FORM4[2]]), k(0.0, toon={**ONCTR, 'face': {'lid': 0.45}}, toonDur=0.0), k(0.55, look='camera'), k(0.62, toon={**ONCTR, 'face': {'lid': 1.0}}, toonDur=0.05), k(0.74, toon={**ONCTR, 'face': {'lid': 0.45}}, toonDur=0.07)])],
        props=[P('shelf4', 'lostShelf', pos=[-0.4, 0, -2.3], opts={'sign': ''}),
               P('form4', 'lossForm', pos=FORM4, scale=1.0, opts={'s': 1.6})],
        cams=[FC(0.0, [0.45, 1.55, 2.5], [[CLK[0], 2.35, CLK[2]], [ME4[0], 2.45, ME4[2]], [r(CLK[0] - 0.55), 0.9, CLK[2]], [r(ME4[0] + 0.45), 0.9, ME4[2]], [FORM4[0], r(FORM4[1] + 0.3), FORM4[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.08))])
st.cue('sfx:paper', 'S04', 0.1, 0.25)

# 5: refused. Close over the counter: she slaps the form down by his hand and her stamp comes down: REFUSÉ on the form and on his fingers: his hand squashed
#    flat as a pancake, then it pops back; he blinks; she blows on her stamp
D5 = st.dur('S05'); ST5 = round(st.at('S05', 'L03', 4) + 0.06, 3)
FORM5 = [r(FLATH[0] - 0.35), 0.865, r(FLATH[2] - 0.12)]
st.shot('S05', 'mairie', setOpts=OFC, actors=[
        act('guichet', CLK, 25, 'stand', 'unimpressed', keys=[k(0.0, look=[FORM5[0], 0.9, FORM5[2]]), k(0.0, toon={'reach': {'R': [r(FORM5[0] + 0.12), 1.35, r(FORM5[2] - 0.05), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'gy': 0.5}}, toonDur=0.0),   # the stamp raised high...
            k(round(ST5 - 0.04, 3), toon={'reach': {'R': [r(FORM5[0] + 0.12), 0.98, r(FORM5[2] - 0.02), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'gy': 0.5, 'brow': -0.3}}, toonDur=0.04, toonEase='in'),   # ...and down
            k(round(ST5 + 0.3, 3), toon={'reach': {'R': [r(CLK[0] + 0.3), 1.55, r(CLK[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'puff': 0.6, 'mouth': 'kiss'}}, toonDur=0.15), k(round(ST5 + 0.3, 3), look=[r(CLK[0] + 0.3), 1.55, r(CLK[2] + 0.35)]),   # she blows on her stamp
            k(round(ST5 + 0.7, 3), look='camera')]),
        act('mec', ME4, RYME, 'stand', 'unimpressed', keys=[k(0.0, look=[FORM5[0], 0.9, FORM5[2]]), k(0.0, toon={**ONCTR, 'face': {'lid': 0.45}}, toonDur=0.0),
            k(ST5, toon={**ONCTR, 'scl': {'handR': [1.7, 0.3, 1.5]}, 'face': {'lid': 0.45}}, toonDur=0.02, toonEase='out'),   # the hand under the stamp: flat as a pancake...
            k(round(ST5 + 0.3, 3), toon={**ONCTR, 'scl': {'handR': [1.7, 0.3, 1.5]}, 'face': {'lid': 1.0}}, toonDur=0.04), k(round(ST5 + 0.4, 3), toon={**ONCTR, 'scl': {'handR': [1.7, 0.3, 1.5]}, 'face': {'lid': 0.45}}, toonDur=0.05),   # ...he blinks...
            k(round(ST5 + 0.55, 3), toon={**ONCTR, 'scl': {'handR': [0.85, 1.3, 0.9]}, 'face': {'lid': 0.45}}, toonDur=0.05, toonEase='outBack'), k(round(ST5 + 0.68, 3), toon={**ONCTR, 'face': {'lid': 0.45}}, toonDur=0.1),   # ...and it pops back
            k(round(ST5 + 0.62, 3), look='camera')])],
        props=[P('form5', 'lossForm', pos=FORM5, rot=[-PI / 2, 0, 0.25], opts={'s': 1.6, 'stamp': {'text': 'REFUSÉ', 'at': ST5, 'rot': -0.2}}),
               P('stamp5', 'rubberStamp', on={'actor': 'guichet', 'hand': 'R', 'offset': [0, -0.06, 0.02]}, scale=2.2, opts={'color': '#C23A2E'}),
               P('shelf5', 'lostShelf', pos=[-0.4, 0, -2.3], opts={'sign': ''})],
        fx=[{'type': 'shake', 'at': ST5, 'dur': 0.12, 'amount': 0.008}],
        cams=[FC(0.0, [0.75, 1.75, 1.3], [[CLK[0], 2.3, CLK[2]], [ME4[0], 2.4, ME4[2]], [FORM5[0], 0.86, FORM5[2]], [FLATH[0], 0.86, FLATH[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:cuff', 'S05', ST5, 0.45)

# 6: a boomerang is not lost: it comes back. She takes a little boomerang from her desk and throws it over his head: it loops round the room behind him; his
#    head follows it all the way round, a full turn on his neck
D6 = st.dur('S06'); TH6 = 0.3; RV7 = round(st.at('S07', 'L04', 6) - st.SH['S07'][0] + 0.0, 3)
LOOP = [[-0.05, 1.5, -1.35], [1.0, 1.95, -1.05], [2.0, 1.95, -0.2], [1.75, 1.85, 0.75], [0.5, 1.8, 0.95], [-0.7, 1.7, 0.35], [-0.75, 1.6, -0.75], [-0.05, 1.5, -1.35]]
SEG = round((D6 - TH6 + RV7) / (len(LOOP) - 1), 3)
st.shot('S06', 'mairie', setOpts=OFC, actors=[
        act('guichet', CLK, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[ME4[0], 1.9, ME4[2]]), k(0.0, toon={'reach': {'R': [r(CLK[0] + 0.25), 1.2, r(CLK[2] + 0.25), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5}}, toonDur=0.0),
            k(round(TH6 - 0.15, 3), toon={'reach': {'R': [r(CLK[0] + 0.35), 1.55, r(CLK[2] - 0.1), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5}}, toonDur=0.12),
            k(TH6, toon={'reach': {'R': [r(CLK[0] + 0.6), 1.75, r(CLK[2] + 0.45), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.5}}, toonDur=0.05, toonEase='out'), k(round(TH6 + 0.3, 3), toon={'face': {'lid': 0.55}}, toonDur=0.2),   # a flick of the wrist
            k(round(TH6 + 0.2, 3), look='camera')]),
        act('mec', ME4, RYME, 'stand', 'unimpressed', keys=[k(0.0, look=[CLK[0], 1.6, CLK[2]]), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0), k(round(TH6 + 0.05, 3), look=None),
            k(round(TH6 + 0.1, 3), toon={'bend': {'neck': [0, 0.0, 0, 1, None]}, 'face': {'lid': 0.2, 'brow': 0.3}}, toonDur=0.05),
            k(round(TH6 + 0.2, 3), toon={'bend': {'neck': [0, round(2 * PI, 4), 0, 1, None]}, 'face': {'lid': 0.2, 'brow': 0.3}}, toonDur=round(D6 - TH6 - 0.25, 3), toonEase='linear')])],   # his head follows it all the way round
        props=[BOOM('boom6', pos=LOOP[0], scale=0.8, opts={'spin': [[TH6, 6.0]], 'wobble': 0.2, 'color': '#D9A35E', 'bands': ['#2F6FB5', '#F2C80F']}, keys=[k(0.0, visible=False), k(TH6, visible=True), *[k(r(TH6 + SEG * i), to=LOOP[i + 1], dur=SEG, ease='linear') for i in range(len(LOOP) - 1)]]),
               P('shelf6', 'lostShelf', pos=[-0.4, 0, -2.3], opts={'sign': ''})],
        cams=[FC(0.0, [0.55, 1.65, 3.4], [[CLK[0], 2.35, CLK[2]], [ME4[0], 2.45, ME4[2]], [2.05, 1.95, -0.2], [-0.8, 1.7, 0.35], [r(ME4[0] + 0.3), 0.6, ME4[2]]], top=0.12, bottom=0.74)])
st.cue('whoosh', 'S06', TH6, 0.35, 1.2, 500, 2200)

# 7: it comes back. Close on her: it lands back in her hand on « revient » without her looking; his head finishes its turn and springs back past front,
#    wobbling; deadpan
D7 = st.dur('S07')
st.shot('S07', 'mairie', setOpts=OFC, actors=[
        act('guichet', CLK, 15, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [r(CLK[0] + 0.45), 1.45, r(CLK[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.6}}, toonDur=0.0),
            k(RV7, toon={'reach': {'R': [r(CLK[0] + 0.45), 1.42, r(CLK[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'grip'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 1.0, 'mouth': 'smirk'}}, toonDur=0.02),   # caught, eyes shut, smug
            k(round(RV7 + 0.3, 3), toon={'reach': {'R': [r(CLK[0] + 0.45), 1.45, r(CLK[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.12)]),
        act('mec', ME4, RYME, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'bend': {'neck': [0, round(2 * PI - 0.5, 4), 0, 1, None]}, 'face': {'lid': 0.2, 'brow': 0.3}}, toonDur=0.0),
            k(0.05, toon={'bend': {'neck': [0, round(2 * PI + 0.35, 4), 0, 1, None]}, 'face': {'lid': 0.2, 'brow': 0.3}}, toonDur=round(max(0.05, RV7 - 0.05), 3), toonEase='out'),   # the end of the turn, past front...
            k(round(RV7 + 0.05, 3), toon={'bend': {'neck': [0, round(2 * PI - 0.15, 4), 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.1), k(round(RV7 + 0.18, 3), toon={'bend': {'neck': [0, round(2 * PI, 4), 0, 1, None]}, 'face': {'lid': 0.45}}, toonDur=0.1),   # ...springs back
            k(round(RV7 + 0.3, 3), look='camera'), k(round(RV7 + 0.45, 3), toon={'face': {'lid': 1.0}}, toonDur=0.05), k(round(RV7 + 0.55, 3), toon={'face': {'lid': 0.45}}, toonDur=0.07)])],
        props=[BOOM('boom7', pos=[1.2, 1.7, -0.3], scale=0.8, opts={'spin': [[0.0, 6.0], [RV7, 0.0]], 'wobble': 0.2, 'color': '#D9A35E', 'bands': ['#2F6FB5', '#F2C80F']}, keys=[k(0.0, to=[r(CLK[0] + 0.45), 1.5, r(CLK[2] + 0.4)], dur=RV7, ease='out'), k(RV7, visible=False)]),
               BOOM('boom7h', on={'actor': 'guichet', 'hand': 'R', 'offset': [0, 0.04, 0.05], 'rot': [PI / 2, 0, 0]}, scale=0.8, opts={'color': '#D9A35E', 'bands': ['#2F6FB5', '#F2C80F']}, keys=[k(0.0, visible=False), k(RV7, visible=True)]),
               P('shelf7', 'lostShelf', pos=[-0.4, 0, -2.3], opts={'sign': ''})],
        cams=[FC(0.0, [0.4, 1.7, 1.6], [[CLK[0], 2.3, CLK[2]], [ME4[0], 2.4, ME4[2]], [r(CLK[0] + 0.45), 1.3, r(CLK[2] + 0.35)], [r(CLK[0] - 0.4), 1.4, CLK[2]]], top=0.12, bottom=0.7)])
st.cue('clack', 'S07', RV7, 0.35)

# 8: the air-traffic controllers opened it an air corridor. The control room: on his radar the boomerang's blip goes round a dashed loop; he sways round in
#    circles following it, then draws the corridor: two white lines along the loop
D8 = st.dur('S08'); CO8 = round(st.at('S08', 'L05', 7) - st.SH['S08'][0] - 0.55, 3)
RADW = [0.0, 1.62, -3.38]; CTL = [0.95, 0, -2.6]                    # (first look) the radar on the wall facing us, the controller beside it facing us (on a console the screen faced away from the camera)
SW = lambda a, d=0.22: {'bend': {'spine': [r(d * math.cos(a)), 0, r(d * math.sin(a)), 1, None]}}
DRAW = lambda dx, dy: {'reach': {'R': [r(RADW[0] + dx), r(RADW[1] + dy), r(RADW[2] + 0.07), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.12, 'face': {'lid': 0.3, 'brow': 0.6}}
st.shot('S08', 'office', setOpts={'door': False}, actors=[
        act('aiguilleur', CTL, -20, 'stand', 'neutral', keys=[k(0.0, look=[RADW[0], RADW[1], RADW[2]]),
            *[k(round(0.05 + 0.12 * i, 3), toon={**SW(i * PI / 2), 'face': {'lid': 0.3, 'brow': 0.5}}, toonDur=0.12, toonEase='inOut') for i in range(6)],   # he sways round in circles with the blip
            k(round(CO8 - 0.12, 3), toon=DRAW(0.38, 0.12), toonDur=0.1), k(round(CO8 + 0.15, 3), toon=DRAW(0.05, -0.22), toonDur=0.2), k(round(CO8 + 0.42, 3), toon=DRAW(-0.32, 0.05), toonDur=0.2),   # draws the corridor on the screen with a marker
            k(round(CO8 + 0.72, 3), look='camera'), k(round(CO8 + 0.72, 3), toon={'reach': {'R': [r(CTL[0] + 0.1), 1.6, r(CTL[2] + 0.4), 1, 0.05]}, 'hands': {'R': 'thumbUp'}, 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.12)])],   # a thumbs up to us
        props=[P('radar8', 'radarScope', pos=RADW, opts={'wall': True, 'r': 0.62, 'corridor': CO8, 'label': 'SECTEUR 4'}), P('marker8', 'marker', on={'actor': 'aiguilleur', 'hand': 'R', 'offset': [0, -0.05, 0.03]}, scale=1.3)],
        cams=[FC(0.0, [0.6, 1.6, 0.9], [[r(RADW[0] - 0.74), r(RADW[1] + 0.74), RADW[2]], [r(RADW[0] + 0.74), r(RADW[1] - 0.8), RADW[2]], [CTL[0], 2.45, CTL[2]], [CTL[0], 0.6, CTL[2]], [r(CTL[0] + 0.45), 1.6, CTL[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:beep', 'S08', 0.1, 0.25); st.cue('sfx:beep', 'S08', 0.8, 0.25); st.cue('sfx:scratch', 'S08', CO8, 0.3)

# 9: an air corridor. Above the clouds: two rows of orange cones standing on the cloud tops, a lane into the distance; the boomerang comes down it toward us
#    and whips past the lens
D9 = st.dur('S09')
CONES = [P(f'cone9_{s}{i}', 'skyCone', pos=[r(s * 1.3), 0.1, r(-2.0 - 4.5 * i)], scale=1.3, opts={'puff': True}) for s in (-1, 1) for i in range(7)]
st.shot('S09', 'skyHigh', setOpts={'seed': 9}, actors=[],
        props=[*CONES, BOOM('boom9', pos=[0.0, 1.4, -34.0], scale=2.2, opts={'spin': [[0.0, 8.0]], 'wobble': 0.2}, keys=[k(0.05, to=[0.25, 1.2, 4.2], dur=round(D9 - 0.2, 3), ease='in')])],
        cams=[cam(0.0, [0.55, 1.5, 5.2], [0.5, 1.45, 4.9], [0.0, 0.9, -20.0], [0.0, 0.9, -20.0], lens=34)])
st.cue('whoosh', 'S09', round(D9 - 0.45, 3), 0.45, 0.35, 400, 2600)

# 10: planes give way to it. A zebra crossing painted on the clouds: an airliner comes in and brakes like a car before it, nose down, squashed; the boomerang
#     crosses in front of its nose; the plane sets off again
D10 = st.dur('S10'); BR10 = round(st.at('S10', 'L06', 3) - st.SH['S10'][0] - 0.2, 3); X10 = 1.2
st.shot('S10', 'skyHigh', setOpts={'seed': 10}, actors=[],
        props=[P('zebra10', 'skyCrossing', pos=[X10, 0.15, 0.0], ry=90, opts={'w': 9.0, 'l': 3.2, 'n': 7}),
               P('plane10', 'plane', pos=[-34.0, 3.0, 0.0], opts={'livery': '#2F6FB5'}, keys=[k(0.0, to=[r(X10 - 10.5), 3.0, 0.0], dur=BR10, ease='out'),
                   k(round(BR10 - 0.12, 3), rotTo=[0, 0, -0.16], dur=0.12, ease='out'), k(round(BR10 - 0.05, 3), squash=[0.86, 1.1, 1.0], dur=0.0), k(round(BR10 + 0.12, 3), squash=[1.04, 0.97, 1.0], dur=0.0), k(round(BR10 + 0.2, 3), squash=[1, 1, 1], dur=0.1),
                   k(round(BR10 + 0.15, 3), rotTo=[0, 0, 0.03], dur=0.15, ease='inOut'), k(round(BR10 + 0.3, 3), rotTo=[0, 0, 0], dur=0.1),
                   k(round(D10 - 0.55, 3), to=[18.0, 3.4, 0.0], dur=0.55, ease='in'), k(round(D10 - 0.55, 3), squash=[1.12, 0.94, 1.0], dur=0.0)]),
               BOOM('boom10', pos=[X10, 3.6, 9.0], scale=4.0, opts={'spin': [[0.0, 7.0]], 'wobble': 0.15}, keys=[k(0.0, visible=False), k(round(BR10 + 0.08, 3), visible=True), k(round(BR10 + 0.08, 3), to=[X10, 3.5, -9.0], dur=0.5, ease='linear')])],
        cams=[cam(0.0, [9.5, 4.6, 15.5], [9.2, 4.6, 15.0], [-3.5, 2.8, 0.0], [-3.2, 2.8, 0.0], lens=30)])
st.cue('sfx:brake', 'S10', round(BR10 - 0.15, 3), 0.4); st.cue('whoosh', 'S10', round(BR10 + 0.1, 3), 0.4, 0.3, 500, 2500); st.cue('sfx:jet', 'S10', round(D10 - 0.55, 3), 0.3)

# 11: yesterday, it came back. The town-hall square from low down: the steps, the flag, a wedding party posing far below; high in the sky a whistling speck
#     grows, spinning, coming down
TH = [0.0, 0, -30.0]; STEP = [0.0, 0.25, -27.6]
D11 = st.dur('S11')
st.shot('S11', 'parisStreet', setOpts={'eiffel': False, 'clear': [-40, 0]}, actors=[
        act('mariee', [-0.55, 0.25, -27.3], 0, 'stand', 'happy', keys=[k(0.0, look='camera')]),
        act('mec', [0.05, 0.25, -27.3], 0, 'stand', 'happy', keys=[k(0.0, look='camera')]),
        act('mamie', [-1.25, 0.25, -27.5], 10, 'stand', 'happy', keys=[k(0.0, look='camera')]), act('voisin', [0.85, 0.25, -27.5], -10, 'stand', 'happy', keys=[k(0.0, look='camera')])],
        props=[P('th11', 'townHall', pos=TH, opts={'w': 8, 'h': 5.5, 'd': 4, 'gable': 'v2'}),
               BOOM('boom11', pos=[3.0, 26.0, -36.0], scale=3.0, opts={'spin': [[0.0, 6.0]], 'wobble': 0.2}, keys=[k(0.0, to=[0.6, 9.0, -29.0], dur=round(D11 - 0.05, 3), ease='in')])],
        cams=[cam(0.0, [2.2, 0.9, -15.5], [2.0, 0.95, -16.2], [0.3, 6.5, -30.0], [0.3, 6.8, -30.0], lens=30)])
st.cue('whoosh', 'S11', 0.05, 1.4, 0.6, 1200, 3200)

# 12: right during his wedding photo. Behind the photographer under his black cloth: the party on the steps, everyone smiling stiffly for the camera, the groom
#     deadpan, the bride with her bouquet
D12 = st.dur('S12')
WED = [('mariee', [-0.55, 0.25, -27.3], 8, 'happy'), ('mamie', [-1.3, 0.25, -27.55], 15, 'happy'), ('voisin', [0.9, 0.25, -27.55], -15, 'happy'), ('gamin', [-0.95, 0.25, -26.9], 10, 'happy')]
SMILE = {'face': {'mouth': 'bigsmile', 'lid': 0.15}}
def WEDS(extra=None, react_at=None):
    out = []
    for nm, p, ry, ex in WED:
        ks = [k(0.0, look='camera'), k(0.0, toon=SMILE, toonDur=0.0)]
        if extra: ks += extra(nm, p)
        out.append(act(nm, p, ry, 'stand', ex, keys=ks))
    return out
GROOM = [0.05, 0.25, -27.3]
VEIL = lambda pid: P(pid, 'brideVeil', on={'actor': 'mariee', 'joint': 'head', 'offset': [0, 0.42, -0.05]})
BOUQ = lambda pid: P(pid, 'bouquet', on={'actor': 'mariee', 'hand': 'R', 'offset': [0, 0.02, 0.04]}, scale=1.6)
HOLDB = {'reach': {'R': [-0.42, 1.3, -26.95, 1, 0.05]}, 'hands': {'R': 'grip'}}
PHOTOG = [1.35, 0, -23.6]                                             # (first look) to the side: in the middle he hid the groom (78 %)
st.shot('S12', 'parisStreet', setOpts={'eiffel': False, 'clear': [-40, 0]}, actors=[
        *WEDS(lambda nm, p: [k(0.0, toon={**SMILE, **HOLDB}, toonDur=0.0), k(0.55, toon={**HOLDB, 'face': {'mouth': 'bigsmile', 'lid': 1.0}}, toonDur=0.05), k(0.66, toon={**SMILE, **HOLDB}, toonDur=0.06)] if nm == 'mariee' else
                   [k(round(0.3 + 0.1 * len(nm) % 0.4, 3), toon={'face': {'mouth': 'bigsmile', 'lid': 1.0}}, toonDur=0.05), k(round(0.42 + 0.1 * len(nm) % 0.4, 3), toon=SMILE, toonDur=0.06)]),
        act('mec', GROOM, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'mouth': 'smile', 'lid': 0.45}}, toonDur=0.0), k(0.6, toon={'face': {'mouth': 'smile', 'lid': 1.0}}, toonDur=0.05), k(0.72, toon={'face': {'mouth': 'smile', 'lid': 0.45}}, toonDur=0.07)]),   # a polite smile, heavy lids
        act('photographe', PHOTOG, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.5, -27.3]), k(0.0, toon={'bend': {'spine': [0.35, 0, 0, 1, None]}, 'reach': {'R': [1.62, 1.55, -24.0, 1, 0.05]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(0.35, toon={'bend': {'spine': [0.35, 0, 0, 1, None]}, 'reach': {'R': [1.62, 1.95, -24.0, 1, 0.05]}, 'hands': {'R': 'spread'}}, toonDur=0.1), k(0.5, toon={'bend': {'spine': [0.35, 0, 0, 1, None]}, 'reach': {'R': [1.62, 1.55, -24.0, 1, 0.05]}, 'hands': {'R': 'grip'}}, toonDur=0.1)])],   # « souriez » with his free hand
        props=[P('th12', 'townHall', pos=TH, opts={'w': 8, 'h': 5.5, 'd': 4, 'gable': 'v2'}), P('cam12', 'bellowsCamera', pos=[1.35, 0, -24.05], ry=200), VEIL('veil12'), BOUQ('bq12'),
               P('flower12', 'bouquet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.12, 0.42, 0.13]}, scale=0.45)],
        cams=[FC(0.0, [0.9, 1.75, -21.6], [[-1.3, 2.3, -27.55], [0.9, 2.3, -27.55], [-1.3, 0.25, -27.3], [0.9, 0.25, -27.3], [PHOTOG[0], 1.2, PHOTOG[2]]], top=0.18, bottom=0.74)])

# 13: his wedding. Closer on the couple: the boomerang drops onto his head on « mariage », squashes it flat as a disc and keeps turning on top like a rotor;
#     the downdraft blows the guests' hair up and the veil out; his smile does not move
D13 = st.dur('S13'); LD13 = round(st.at('S13', 'L08', 5) - st.SH['S13'][0] + 0.02, 3)
DISC = {'scl': {'head': [1.45, 0.42, 1.45]}}
st.shot('S13', 'parisStreet', setOpts={'eiffel': False, 'clear': [-40, 0]}, actors=[
        *WEDS(lambda nm, p: [k(round(LD13 + 0.04, 3), toon={**({**SMILE, **HOLDB} if nm == 'mariee' else SMILE), 'hairUp': 1.0, 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.6}}, toonDur=0.05),   # the downdraft: hair up, the smiles still on
                                  k(round(LD13 + 0.12, 3), look=[GROOM[0], 3.0, GROOM[2]])]),
        act('mec', GROOM, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'mouth': 'smile', 'lid': 0.45}}, toonDur=0.0),
            k(round(LD13 - 0.05, 3), toon={'face': {'mouth': 'smile', 'lid': 0.45}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.03),
            k(LD13, toon={**DISC, 'sq': [1.08, 0.9, 1.08], 'face': {'mouth': 'smile', 'lid': 0.3}}, toonDur=0.02, toonEase='out'),   # the head squashed flat as a disc...
            k(round(LD13 + 0.1, 3), toon={**DISC, 'sq': [0.98, 1.03, 0.98], 'face': {'mouth': 'smile', 'lid': 0.45}}, toonDur=0.08),   # ...still smiling
            *[k(round(LD13 + 0.2 + 0.08 * i, 3), toon={**DISC, 'sq': [1.0, round(1.0 + (0.02 if i % 2 else -0.02), 3), 1.0], 'face': {'mouth': 'smile', 'lid': 0.45}}, toonDur=0.04) for i in range(6)]])],   # the rotor shaking him
        props=[P('th13', 'townHall', pos=TH, opts={'w': 8, 'h': 5.5, 'd': 4, 'gable': 'v2'}), VEIL('veil13'), BOUQ('bq13'), P('flower13', 'bouquet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.12, 0.42, 0.13]}, scale=0.45),
               BOOM('boom13', pos=[0.4, 6.0, -27.6], scale=1.6, opts={'spin': [[0.0, 6.0], [LD13, 9.0]], 'wobble': 0.1}, keys=[k(0.0, to=[GROOM[0], 2.6, GROOM[2]], dur=LD13, ease='in'), k(LD13, visible=False)]),
               BOOM('boom13h', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.34, 0.0]}, scale=1.6, opts={'spin': [[0.0, 9.0]], 'wobble': 0.05}, keys=[k(0.0, visible=False), k(LD13, visible=True)])],
        cams=[FC(0.0, [0.35, 1.75, -23.9], [[GROOM[0], 2.75, GROOM[2]], [-0.55, 0.9, -27.3], [0.55, 0.9, -27.3], [-0.95, 2.1, -27.3]], top=0.14, bottom=0.74)])
st.cue('sfx:bonk', 'S13', LD13, 0.45); st.cue('sfx:rotor', 'S13', round(LD13 + 0.05, 3), 0.25)

# 14: he left with it. Wider: he lifts off the steps, deadpan, still smiling for the photo, his body turning slowly the other way under the rotor; the bride
#     looks up holding her bouquet; the photographer's camera tilts up after him; the flash goes off; hats fly
D14 = st.dur('S14'); FL14 = round(st.at('S14', 'L09', 3) - st.SH['S14'][0], 3)
st.shot('S14', 'parisStreet', setOpts={'eiffel': False, 'clear': [-40, 0]}, actors=[
        *WEDS(lambda nm, p: [k(0.0, toon={**({**SMILE, **HOLDB} if nm == 'mariee' else SMILE), 'hairUp': 0.8}, toonDur=0.0), k(0.15, look=[GROOM[0], 3.4, GROOM[2]]), k(0.6, look=[GROOM[0], 5.0, GROOM[2]])]),
        act('mec', GROOM, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**DISC, 'face': {'mouth': 'smile', 'lid': 0.45}}, toonDur=0.0),
            k(0.1, to=[GROOM[0], 4.6, GROOM[2]], dur=round(D14 - 0.15, 3), glide=True, ease='in', face='keep'),   # up he goes
            *[k(round(0.1 + 0.25 * i, 3), to=[GROOM[0], r(0.25 + 4.35 * ((0.25 * i) / (D14 - 0.15)) ** 2), GROOM[2]], dur=0.25, clip='stand', then='stand', face=r(-35 * (i + 1), 1)) for i in range(0)],
            k(0.3, toon={**DISC, 'bend': {'legL': [0.15, 0, 0, 1, None], 'legR': [-0.1, 0, 0, 1, None]}, 'face': {'mouth': 'smile', 'lid': 0.45}}, toonDur=0.3), k(0.95, toon={**DISC, 'face': {'mouth': 'smile', 'lid': 1.0}}, toonDur=0.05), k(1.05, toon={**DISC, 'face': {'mouth': 'smile', 'lid': 0.45}}, toonDur=0.07)]),   # legs dangling, a blink
        act('photographe', PHOTOG, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 2.0, -27.3]), k(0.0, toon={'bend': {'spine': [0.35, 0, 0, 1, None]}, 'reach': {'R': [1.62, 1.55, -24.0, 1, 0.05]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(0.4, toon={'bend': {'spine': [-0.1, 0, 0, 1, None]}, 'reach': {'R': [1.62, 1.75, -24.0, 1, 0.05]}, 'hands': {'R': 'grip'}}, toonDur=0.4)])],   # he straightens up after him
        props=[P('th14', 'townHall', pos=TH, opts={'w': 8, 'h': 5.5, 'd': 4, 'gable': 'v2'}), VEIL('veil14'), BOUQ('bq14'), P('flower14', 'bouquet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.12, 0.42, 0.13]}, scale=0.45),
               P('cam14', 'bellowsCamera', pos=[1.35, 0, -24.05], ry=200, opts={'flashAt': 0.35}, keys=[k(0.4, rotTo=[-0.35, 0, 0], dur=0.5, ease='inOut')]),
               BOOM('boom14h', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.34, 0.0]}, scale=1.6, opts={'spin': [[0.0, 9.0]], 'wobble': 0.05}),
               P('hat14', 'fedoraHat', pos=[0.9, 2.2, -27.55], keys=[k(0.12, to=[2.4, 3.8, -26.5], dur=0.9, ease='out'), k(0.12, rotTo=[1.2, 0.6, 2.4], dur=0.9)])],
        cams=[FC(0.0, [1.3, 1.5, -20.6], [[GROOM[0], 4.2, GROOM[2]], [-1.3, 0.25, -27.3], [0.9, 0.25, -27.3], [PHOTOG[0], 1.4, PHOTOG[2]]], top=0.08, bottom=0.74, drift=(0.0, 0.25, 0.0))])
st.cue('sfx:rotor', 'S14', 0.05, 0.3); st.cue('sfx:shutter', 'S14', 0.35, 0.35)

# 15: his wife is waiting for him. The park again: the bride in her dress and veil, her hand held out, eyes on the sky, deadpan, where he stood
D15 = st.dur('S15')
st.shot('S15', 'grassland', setOpts=PARK, actors=[
        act('mariee', P0, RY0, 'stand', 'unimpressed', keys=[k(0.0, look=[-6, 6.5, 3.5]), k(0.0, toon={**OUT(P0, RY0), 'face': {'lid': 0.45}}, toonDur=0.0),
            k(0.55, toon={**OUT(P0, RY0), 'face': {'lid': 1.0}}, toonDur=0.05), k(0.66, toon={**OUT(P0, RY0), 'face': {'lid': 0.45}}, toonDur=0.07), k(0.9, look=[-4, 7.5, 2.0])])],
        props=[P('veil15', 'brideVeil', on={'actor': 'mariee', 'joint': 'head', 'offset': [0, 0.42, -0.05]}), P('bq15', 'bouquet', on={'actor': 'mariee', 'hand': 'L', 'offset': [0, 0.02, 0.04]}, scale=1.6),
               P('lamp15', 'streetLamp', pos=[-2.6, 0, -2.4])],
        cams=[FC(0.0, [-1.2, 1.45, 2.9], [[P0[0], 2.45, P0[2]], [P0[0], 0.55, P0[2]], [HAND3[0], 1.0, HAND3[2]], [r(P0[0] + 0.55), 1.6, P0[2]], [r(P0[0] - 0.6), 1.6, P0[2]]], top=0.12, bottom=0.74, drift=(0.04, 0.0, -0.08))])

# 16: in ten years. A child runs past and drops a coin in her hand; she looks at it; far up in the sky, unseen by her, a speck with a rotor goes by
D16 = st.dur('S16'); CN16 = round(st.at('S16', 'L10', 4) - st.SH['S16'][0] + 0.05, 3)
st.shot('S16', 'grassland', setOpts=PARK, actors=[
        act('mariee', P0, RY0, 'stand', 'unimpressed', keys=[k(0.0, look=[-4, 7.5, 2.0]), k(0.0, toon={**OUT(P0, RY0), 'face': {'lid': 0.45}}, toonDur=0.0),
            k(round(CN16 + 0.12, 3), look=[HAND3[0], 1.0, HAND3[2]]), k(round(CN16 + 0.12, 3), toon={**OUT(P0, RY0), 'bend': {'neck': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.5}}, toonDur=0.1),
            k(round(D16 - 0.5, 3), toon={**OUT(P0, RY0), 'bend': {'neck': [0.25, 0, 0, 1, None]}, 'face': {'lid': 1.0}}, toonDur=0.08), k(round(D16 - 0.36, 3), toon={**OUT(P0, RY0), 'bend': {'neck': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.5}}, toonDur=0.1)]),   # she looks at the coin, a slow blink
        act('passante', [1.9, 0, 0.85], -95, 'stand', 'neutral', keys=[k(0.0, look=[P0[0], 1.3, P0[2]]), k(0.0, to=[-2.2, 0, 1.05], dur=round(D16 - 0.1, 3), clip='walk', then='walk', ease='linear', face='move'),   # an old lady this time
            k(round(CN16 - 0.12, 3), toon={'reach': {'L': [HAND3[0], r(HAND3[1] + 0.1), HAND3[2], 1, 0.05]}, 'hands': {'L': 'pinch'}}, toonDur=0.08), k(round(CN16 + 0.06, 3), toon={}, toonDur=0.12)])],
        props=[P('veil16', 'brideVeil', on={'actor': 'mariee', 'joint': 'head', 'offset': [0, 0.42, -0.05]}), P('bq16', 'bouquet', on={'actor': 'mariee', 'hand': 'L', 'offset': [0, 0.02, 0.04]}, scale=1.6),
               P('coin16', 'coin', pos=[HAND3[0], r(HAND3[1] + 0.3), HAND3[2]], scale=1.6, keys=[k(0.0, visible=False), k(round(CN16 - 0.05, 3), visible=True), k(round(CN16 - 0.05, 3), to=[HAND3[0], r(HAND3[1] + 0.03), HAND3[2]], dur=0.07, ease='in')]),
               BOOM('speck16', pos=[-26.0, 15.0, -40.0], scale=5.0, opts={'spin': [[0.0, 9.0]]}, keys=[k(0.0, to=[22.0, 17.0, -40.0], dur=round(D16 - 0.05, 3), ease='linear')]),
               P('lamp16', 'streetLamp', pos=[-2.6, 0, -2.4])],
        cams=[FC(0.0, [-1.2, 1.45, 2.9], [[P0[0], 2.45, P0[2]], [P0[0], 0.55, P0[2]], [HAND3[0], 1.0, HAND3[2]], [r(P0[0] + 0.55), 1.6, P0[2]], [r(P0[0] - 0.6), 1.6, P0[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:ding', 'S16', CN16, 0.3); st.cue('sfx:rotor', 'S16', 0.3, 0.06)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 0.5, 'mec', 'windup'), ('S01', round(REL1 + 0.06, 3), 'mec', 'whip'), ('S02', 0.55, 'mec', 'dizzy'), ('S03', round(CN3 + 0.3, 3), 'mec', 'coin'),
           ('S04', 0.75, 'guichet', 'reads'), ('S05', round(ST5 + 0.15, 3), 'mec', 'flat_hand'), ('S06', round(D6 * 0.55, 3), 'guichet', 'throw'), ('S07', round(RV7 + 0.1, 3), 'guichet', 'catch'),
           ('S08', 0.4, 'aiguilleur', 'sway'), ('S12', 0.4, 'mec', 'pose'), ('S13', round(LD13 + 0.15, 3), 'mec', 'rotor'), ('S14', 0.8, 'mec', 'lift'), ('S15', 0.4, 'mariee', 'waits'), ('S16', round(CN16 + 0.3, 3), 'mariee', 'coin')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S04', 0.5, 'form4', 'declaration'), ('S05', round(ST5 + 0.3, 3), 'form5', 'refuse'), ('S08', round(CO8 + 0.6, 3), 'radar8', 'radar'), ('S11', 0.6, 'th11', 'mairie')]:
    st.text(t_[0], t_[1], t_[2], t_[3])

st.write("Le boomerang", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'passante': {'preset': 'mamie', 'seed': 521, 'build': {'width': 0.92, 'headWidth': 1.2}},
    'guichet': {'preset': 'madame', 'seed': 522, 'suit': '#3F8A7A', 'hair': 'bun', 'hairColor': '#B8B8B8', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'aiguilleur': {'preset': 'boss', 'seed': 523, 'suit': '#E8E4DA', 'build': {'width': 0.95, 'headWidth': 1.25}},
    'mariee': {'preset': 'madame', 'seed': 524, 'suit': '#F7F4EE', 'hair': 'bun', 'hairColor': '#5A3A22', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'mamie': {'preset': 'mamie', 'seed': 525, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'voisin': {'preset': 'boss', 'seed': 526, 'suit': '#6B4E8A', 'build': {'width': 0.95, 'headWidth': 1.2}},
    'gamin': {'preset': 'gamin', 'seed': 527},
    'photographe': {'preset': 'worker', 'seed': 528, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
})
