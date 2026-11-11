#!/usr/bin/env python3
"""L'élan (story 41, cycle 5 of the cartoon staging): this man ran to catch his bus. He could not stop. He passed the bus. Then the town. On the
third lap, people got on. The town hall settled it: "It is a line." Since then he comes by every eight minutes. He has a number. He has inspectors.
He asked to get off. He was told: "At the terminus." There is no terminus. Yesterday he finally managed to stop. Not his passengers. They arrived
early. That is a first.
Cartoon rig, cycle 5: follow-through (toon option `follow`), poses that settle (`settle`), props that rock on their carrier (`sway`), pupils that
grow and shrink (`pupilSize`); new clips heelBrake, flag, shoulderRide. Natural look.
Third staging (after the second review: animation 7.7, art direction 7.6), with what cycle 6 added: cameras aimed by calculation on measured
joints (`debugJoints`, `project`), a prop turned by `axes_euler`, a drawn tear that rolls (`drop`), inked steam (`steamInk`), a bus with a higher
ceiling (`top`), a hand-keyed snap-back that the follow-through does not remember (`auto: 0`).
Last pass (after the third review: animation 8.4, art direction 8.3; no further review): the ending played after the camera has stopped, with a
weight shift keyed by hand (`hip`) and 0.4 s more of tail; the half-turn of S19 in three times; the stop at the pole seen 46 degrees off his line,
the pole bowing from its foot (`bendGrip`), a hold of eleven frames; the tear rolls thirteen frames; the third knock launched from the clear half of
the pane; the inspectors seen from the pavement, low, against the sky; pavements that run under the house fronts (`paveW`)."""
from story_kit import *
import math

st = Story('elan', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 8), ('S03', 'L02', 0), ('S04', 'L02', 5), ('S05', 'L03', 0), ('S06', 6.67, 0), ('S07', 'L04', 0), ('S08', 'L05', 0),
         ('S09', 'L06', 0), ('S10', 'L06', 1), ('S11', 'L07', 0), ('S12', 'L07', 4), ('S13', 'L08', 0), ('S14', 'L08', 5), ('S15', 'L09', 0), ('S16', 'L10', 0),
         ('S17', 'L11', 0), ('S18', 20.33, 0), ('S19', 'L12', 0), ('S20', 'L13', 0), ('S21', 'L13', 5), ('S22', 26.2, 0)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}
r3 = lambda v: [round(x, 3) for x in v]
lerp3 = lambda a, b, u: r3([a[i] + (b[i] - a[i]) * u for i in range(3)])
# a point of a pole that bends as an arc (the same sum as arcPole in engine/props_elan.js): base [x, y, z], height h, lean a (rad), s metres up the pole,
# the pole turned ry degrees (it leans toward its own +X)
def pole_pt(base, h, a, s, ry=0.0, n=14, grip=0.0):   # grip (m): the pole is pulled by a hand at that height (prop option bendGrip): it bows from its foot, straight above
    x = y = 0.0; seg = h / n; left = s
    for i in range(n):
        th = (a * (1 - (1 - min(1.0, (i * seg) / grip)) ** 2)) if grip else (a * i / (n - 1) if i else 0.0); d = min(seg, left); x += d * math.sin(th); y += d * math.cos(th); left -= d
        if left <= 0: break
    r = math.radians(ry)
    return r3([base[0] + x * math.cos(r), base[1] + y, base[2] - x * math.sin(r)])

# ---- the street: he runs toward -Z (the tower at the far end). The bus runs in the lane along the right-hand pavement (x > 5), its doors on the pavement side
V = 8.0                                              # his speed, m/s
STREET = {'clear': [-60, 60], 'eiffel': True, 'paveW': 6.5}   # paveW: the pavements run under the house fronts (at 5 m a dark gutter showed along the foot of the walls)
BX, BL = 2.6, 7.6                                    # the bus: the middle of its lane, its length
bus_at = lambda zc, lx, ly, lz: r3([BX + lz, ly, zc - lx])   # a point of the bus (its own frame: +X to its nose, +Z to its doors) in the world, its middle at z = zc
BUS = lambda zc, *keys, **kw: P('bus', 'cityBus', pos=[BX, 0, zc], ry=90, keys=list(keys), opts={'len': BL, 'line': '12', 'dest': 'GARE', 'top': 2.65, **kw})   # top: a ceiling high enough for a cap that jumps and a passenger who hops (at 2.3 they went through it)
SEATL = (BL / 2 - 1.05, 0.3, -0.55)                  # the driver's seat, in the bus
RIDERL = [('p1', (BL / 2 - 1.5, 0.44, 0.62), 90), ('p2', (-0.1, 0.44, 0.6), 100), ('p3', (-1.9, 0.44, 0.55), 85)]   # three passengers on the door side: one behind the glass of the front door
STOPPOLE = lambda **kw: P('pole', 'busStopPole', pos=kw.pop('pos'), ry=kw.pop('ry', 90), opts={'line': '12', **kw})

# 1: the hook, seen from inside his bus, through the glass of the front door: he runs beside it and bangs on the glass, three times, a fist bigger each
#    time (stars on the glass, the bus rocks, the passenger at the door jumps); then the bus brakes: he slides out of the doorway, forward, his head turning
#    back to us; the passenger turns to us
X1 = 4.6; Z1 = 30.0                                  # his line, in the road beside the bus; where he is at 0
z1 = lambda t: round(Z1 - V * t, 3)
D1 = st.dur('S01'); BR1 = 1.5                        # the bus brakes (eleven frames after he hits the glass: the passenger needs the rest of the shot for her look at us)
DOORL = BL / 2 - 1.55                                # the front door, in the bus: metres from its middle toward its nose
STOP1 = round(V * (D1 - BR1) / 3, 3)                 # how far the bus still goes: with an 'out' ease over the rest of the shot it starts braking at his speed and stops on the cut
ZCA, ZCB = round(Z1 + DOORL + 0.1, 3), round(z1(BR1) + DOORL + 0.1, 3); ZC2 = round(ZCB - STOP1, 3)   # the middle of the bus: at 0 (the door level with him), when it brakes, where it stops
RUN = {'freq': 4.4}
RUNC = {'freq': 4.4, 'bounce': 0.9}; CAD = 2.5; RUNI = {'freq': 4.4, 'bounce': 0.06, 'sq': 0.02}   # seen close: a slower cadence (a contact every six frames), a smaller bounce, a squash at each contact: the face holds between two strides
SPRINT = lambda **kw: {'bend': {'spine': [0.42, 0, 0, 1.04, None], 'neck': [-0.3, 0, 0, 1.1, None]}, 'autoSq': 0.15, **kw}   # autoSq: at 4.4 strides a second the automatic squash of each footfall lands on one frame in three or four, never the same: seen close, his head drops 40 cm for a frame
SHOUT = {'jaw': 0.6, 'brow': 0.7, 'eye': 0.25}
NOLEGS = {k_: [0, 0, 0, 0.05, 0.3] for k_ in ('legL', 'legR', 'shinL', 'shinR')}   # his own legs shrunk away: the wheel of legs takes their place
WHEELB = {'spine': [0.42, 0, 0, 1.04, None], 'neck': [-0.3, 0, 0, 1.1, None], **NOLEGS}
WHEEL = lambda **kw: P('wheel', 'legWheel', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, -0.02, 0]}, opts=kw)
KT1 = (0.42, 0.78, 1.14)                             # the three knocks: a knuckle, the forearm, the whole man
GLASS1 = BX + 1.14                                   # the glass of the door (world x)
XP1 = round(GLASS1 + 0.2, 3)                         # his line when he is flat on the pane
def knock1(t, on, face=SHOUT, big=1.0):              # his left fist on the glass of the door (on), or drawn back, at t (the door runs with him)
    tgt = [GLASS1 + 0.06, 1.8, z1(t) + 0.05] if on else [GLASS1 + 0.5, 1.9, z1(t) - 0.1]
    return SPRINT(hands={'L': 'fist'}, scl={'handL': [big, big, big]}, reach={'L': [*tgt, 1, 0.04]}, face=face)
KN1 = [(0.0, 0, 1.0), (KT1[0] - 0.07, 0, 1.0), (KT1[0], 1, 1.0), (KT1[0] + 0.07, 0, 1.0), (KT1[1] - 0.1, 0, 1.6), (KT1[1], 1, 2.7), (KT1[1] + 0.08, 0, 1.0), (KT1[2] - 0.16, 0, 1.0)]   # (t, on the glass, the size of the fist): a tap of the knuckles, then the fist as big as his head
PRESS1 = lambda **face: {'sq': [1.22, 1.02, 0.5], 'scl': {'head': [1.3, 1.0, 0.5]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'auto': 0, 'face': {'eye': 0.5, 'brow': 1, 'cheeks': 1, 'mouth': 'o', 'mouthW': 0.5, **face}}   # flat on the pane: the body and the head half as deep, the cheek spread
inbus1 = lambda loc: [k(0.0, to=bus_at(ZCB, *loc), dur=BR1, glide=True, ease='linear', cruise=True), k(BR1, to=bus_at(ZC2, *loc), dur=round(D1 - BR1, 3), glide=True, ease='out')]
CAML1, LOOKL1 = (DOORL - 0.5, 1.72, -0.95), (DOORL + 0.38, 1.52, 1.95)   # the camera, in the bus, against its far side; what it looks at, outside the door
P1L = (DOORL - 0.47, 0.44, 0.88); P1L2 = (DOORL - 0.25, 0.44, 0.88)   # the passenger at the door, over whose shoulder we look: half of her at the edge of the frame; the braking throws her forward, into the frame
HOP1 = (0.03, 0.09, 0.2)                              # how high each knock throws her
EYES1 = {'eye': 0.6, 'pupilSize': 1.1, 'brow': 0.6}                         # the passenger's eyes on us: wide
AH1 = 0.3; LD1 = 0.2                                  # the third knock: he gets that far ahead of the door first (the clear half of the pane: at the door he sprang from behind the passenger); he lands that far ahead of its middle (the seam of the door ran through his eye)
LU1 = 0.1                                             # her lurch, that long after the brake: three frames in which his face is dragged along the glass in clear view
zc1 = lambda t: round(ZCB + (ZC2 - ZCB) * (1 - (1 - (t - BR1) / (D1 - BR1)) ** 3), 3)   # the middle of the bus while it brakes (the 'out' ease of the engine)
st.shot('S01', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, look={'bloom': 0.06}, actors=[act('mec', [X1, 0, Z1], 180, 'run', 'scared', params=RUNC, keys=[*[k(t, look=bus_at(ZCA - V * t, CAML1[0] + 0.3, 1.7, 0.2)) for t in (-0.4, 0.0, 0.4, 0.8)],   # his head turned to the door (from before the first frame: his face is to us on the first image of the film)
            k(0.0, to=[X1, 0, z1(KT1[1] + 0.06)], dur=round(KT1[1] + 0.06, 3), clip='run', params=RUNC, cadence=CAD, ease='linear', face=180, cruise='in'),
            k(KT1[1] + 0.06, to=[X1 + 0.1, 0, round(z1(KT1[2] - 0.16) - AH1, 3)], dur=round(KT1[2] - 0.16 - KT1[1] - 0.06, 3), clip='run', params=RUNC, cadence=CAD, ease='linear', face=180),   # he gets ahead of the door, and away from it: room to spring
            k(KT1[2] - 0.27, toon={**knock1(KT1[2] - 0.16, 0), 'sq': [1.1, 0.84, 1.1]}, toonDur=0.1, toonEase='out'),                                              # he gathers himself: three frames
            k(0.0, toon=knock1(0.0, 0), toonDur=0.0), *[k(KN1[i][0], toon=knock1(KN1[i + 1][0], KN1[i + 1][1], {**SHOUT, 'jaw': 0.95, 'eye': 0.35} if KN1[i + 1][1] else SHOUT, KN1[i + 1][2]), toonDur=round(KN1[i + 1][0] - KN1[i][0], 3), toonEase='in' if KN1[i + 1][1] else 'out') for i in range(len(KN1) - 1)],
            k(KT1[2] - 0.16, to=[XP1, 0.16, round(z1(KT1[2]) - LD1, 3)], dur=0.16, clip='pressGlass', then='pressGlass', glide=True, ease='in', face=-90, blend=0.06), k(KT1[2] - 0.16, look=None),   # the third: he throws his whole body at the glass, back toward the middle of the door
            k(KT1[2] - 0.16, toon={'sq': [0.9, 1.06, 1.2], 'hands': {'L': 'spread', 'R': 'spread'}, 'auto': 0, 'face': {**SHOUT, 'jaw': 0.9}}, toonDur=0.12, toonEase='in'),
            k(KT1[2] - 0.02, toon=PRESS1(), toonDur=0.03),                                                                                                              # flat on the pane, his cheek spread on it
            k(KT1[2], to=[XP1, 0.16, round(z1(BR1) - LD1, 3)], dur=round(BR1 - KT1[2], 3), clip='pressGlass', then='pressGlass', glide=True, ease='linear', face=-90, blend=0),         # he rides the glass, twelve frames
            k(KT1[2] + 0.12, toon=PRESS1(gx=0.7), toonDur=0.06), k(KT1[2] + 0.24, toon=PRESS1(gx=0.7, lid=1), toonDur=0.03), k(KT1[2] + 0.3, toon=PRESS1(gx=0.7), toonDur=0.03),   # his eyes slide to the passenger; a blink
            k(BR1, to=[XP1 + 0.5, 0, round(z1(D1) - LD1, 3)], dur=round(D1 - BR1, 3), clip='pressGlass', then='pressGlass', glide=True, ease='linear', face=-120, blend=0, cruise='out'),   # the bus brakes: he goes on, sliding off the pane
            k(BR1 + 0.02, toon={'sq': [1.5, 1.0, 0.5], 'scl': {'head': [1.4, 1.0, 0.5]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'auto': 0, 'face': {'eye': 0.5, 'brow': 1, 'cheeks': 1, 'mouth': 'wavy'}}, toonDur=0.1, toonEase='out'),   # smeared along it
            k(BR1 + 0.3, toon={'sq': [0.92, 1.06, 0.92], 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'brow': 1, 'eye': 0.4, 'jaw': 0.45}}, toonDur=0.1, toonEase='outBack')]),   # he peels off, round again
        act('chauf', bus_at(ZCA, *SEATL), 180, 'drive', 'unimpressed', keys=[k(0.0, look=None), *inbus1(SEATL)]),
        act('p1', bus_at(ZCA, *P1L), 180, 'stand', 'surprised', blink=0, keys=[k(0.0, look='mec'), inbus1(P1L)[0],   # facing the way the bus goes from the first frame (carried along, she turns that way: at 90 she spent the first three frames turning)
            k(BR1, to=bus_at(zc1(BR1 + LU1), *P1L), dur=LU1, glide=True, ease='linear'), k(BR1 + LU1, to=bus_at(ZC2, *P1L2), dur=round(D1 - BR1 - LU1, 3), glide=True, ease='out'),   # she rides the braking bus three frames, then it throws her forward
            *[x for i, t in enumerate(KT1) for x in (k(t, toon={'sq': [1 + 0.04 * (i + 1), 1 - 0.06 * (i + 1), 1 + 0.04 * (i + 1)]}, toonDur=0.03), k(t + 0.04, toon={'sq': [1 - 0.03 * (i + 1), 1 + 0.05 * (i + 1), 1 - 0.03 * (i + 1)], 'bend': {'spine': [0, 0, 0, 1 + HOP1[i] * 0.6, None]}}, toonDur=0.06, toonEase='out'), k(t + 0.12, toon={'settle': 0.6}, toonDur=0.1))],   # each knock throws her higher
            k(KT1[2] + 0.22, toon={'face': {'eye': 0.5, 'brow': 0.9, 'lid': 1}}, toonDur=0.04), k(KT1[2] + 0.29, toon={'face': {'eye': 0.5, 'brow': 0.9}}, toonDur=0.04),   # he is flat on the glass, a hand's breadth from her: she stays at the edge of the frame (leaning in, her head covered his face), and blinks
            k(BR1 + LU1, look=bus_at(ZC2, *CAML1)), k(BR1 + LU1, expr='neutral'), k(BR1 + LU1 + 0.02, toon={'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': {**EYES1, 'browL': 0.9}}, toonDur=0.1, toonEase='out'),
            k(BR1 + 0.44, toon={'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': {**EYES1, 'browL': 0.9, 'lid': 1}}, toonDur=0.03), k(BR1 + 0.5, toon={'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': {**EYES1, 'browL': 0.9}}, toonDur=0.03)])],   # the brake throws her forward, into the frame, bent double; her head comes round to us (the turn takes a blink with it, seven frames), and her eyes stay on us, wide, to the cut: ten frames
        props=[BUS(ZCA, k(0.0, to=[BX, 0, ZCB], dur=BR1, ease='linear'), k(BR1, to=[BX, 0, ZC2], dur=round(D1 - BR1, 3), ease='out'), rock=[[KT1[0], 0.006], [KT1[1], 0.022], [KT1[2], 0.05], [BR1, 0.02]], doorGlass=0.08),
               *[P(f'kn{i}', 'impactStars', pos=[GLASS1 - 0.03, 1.8, round(z1(t) + 0.05 - (LD1 if i == 2 else 0), 3)], ry=90, opts={'at': t, 'n': (3, 5, 8)[i], 'r': (0.16, 0.34, 0.66)[i], 'r0': (0.06, 0.2, 0.36)[i], 'dur': (0.2, 0.26, 0.34)[i], 'size': (0.045, 0.07, 0.1)[i]}, keys=[k(t, to=[GLASS1 - 0.03, 1.8, round(z1(t + 0.3) + 0.05 - (LD1 if i == 2 else 0), 3)], dur=0.3, ease='linear')]) for i, t in enumerate(KT1)]],   # stars on the glass at each knock, bigger each time
        fx=[{'type': 'shake', 'at': KT1[1], 'dur': 0.1, 'amount': 0.012}, {'type': 'shake', 'at': KT1[2], 'dur': 0.2, 'amount': 0.035}],
        cams=[cam(0.0, bus_at(ZCA, *CAML1), bus_at(ZCB, *CAML1), bus_at(ZCA, *LOOKL1), bus_at(ZCB, *LOOKL1), lens=55),
              cam(BR1, bus_at(ZCB, *CAML1), bus_at(ZC2, *CAML1), bus_at(ZCB, *LOOKL1), bus_at(ZC2, *LOOKL1), lens=55, ease='out')])   # the camera rides in the bus: it brakes with it
st.cue('engine', 'S01', 0.0, 0.22, BR1 + 0.25); st.cue('whoosh', 'S01', 0.0, 0.25, 0.5, 500, 1800); [st.cue('thud', 'S01', t, (0.25, 0.45, 0.75)[i]) for i, t in enumerate(KT1)]; st.cue('sfx:squeak', 'S01', KT1[2] + 0.02, 0.4); st.cue('sfx:squeak', 'S01', BR1, 0.5)

# 2: he brakes with his heels and does not stop: the camera runs backward in front of him; behind him the bus, stopped, gets smaller
D2 = st.dur('S02'); V2 = 7.5
A2, B2 = [5.0, 0, z1(D1)], [5.1, 0, round(z1(D1) - V2 * D2, 3)]
st.shot('S02', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[act('mec', A2, 180, 'heelBrake', 'scared', keys=[k(0.0, look=None), k(0.0, to=B2, dur=D2, clip='heelBrake', glide=True, ease='linear', face=180, cruise=True),
            k(0.0, toon={'face': {'gy': 0.4, 'brow': 0.8, 'mouth': 'clench'}}, toonDur=0.0),                                 # his eyes on his heels
            k(0.5, toon={'face': {'gy': 0.4, 'brow': 0.9, 'mouth': 'clench', 'sweat': 1}}, toonDur=0.1),
            k(0.9, toon={'face': {'brow': 1, 'eye': 0.3, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.08), k(1.12, toon={'face': {'brow': 1, 'eye': 0.3, 'mouth': 'wavy', 'sweat': 1, 'lid': 1}}, toonDur=0.04), k(1.2, toon={'face': {'brow': 1, 'eye': 0.3, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.04)]),   # then on us; a blink
        act('chauf', bus_at(ZC2, *SEATL), 180, 'drive', 'unimpressed', keys=[k(0.0, look='mec')]), *[act(n, bus_at(ZC2, *loc), ry, 'stand', 'surprised', keys=[k(0.0, look='mec')]) for n, loc, ry in RIDERL]],
        props=[BUS(ZC2), P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A2[0], A2[2] - 0.55], [D2, B2[0], B2[2] - 0.55]], 'from': 0.0, 'to': D2, 'every': 0.03, 'marks': True})],
        cams=[cam(0.0, [6.9, 1.15, A2[2] - 3.4], [6.8, 1.15, B2[2] - 3.4], [A2[0], 0.95, A2[2]], [B2[0], 0.95, B2[2]], lens=44)])
st.cue('sfx:squeak', 'S02', 0.0, 0.5); st.cue('whoosh', 'S02', 0.0, 0.3, D2, 300, 900)

# 3: the driver, through his windscreen: his head goes after what passed his windows, comes back to the road, and whips round: the cap spins on his
#    head like a top and stops back to front
D3 = st.dur('S03'); W3 = 0.7                         # the whip
DRV3 = bus_at(ZC2, *SEATL)
st.shot('S03', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[
        act('chauf', DRV3, 180, 'drive', 'unimpressed', blink=0, keys=[k(0.0, look=[6.6, 1.5, DRV3[2] + 0.6]), k(0.0, toon={'face': {'gx': -0.7, 'eye': 0.15}}, toonDur=0.0),   # his eyes, open, on what passes his windows
               k(0.06, look=[6.2, 1.45, DRV3[2] - 1.6]), k(0.06, toon={'face': {'gx': -0.9, 'eye': 0.15}}, toonDur=0.1), k(0.18, look=[5.2, 1.4, DRV3[2] - 6.0]), k(0.18, toon={'face': {'gx': -0.5, 'eye': 0.15}}, toonDur=0.1),   # they follow it, ahead
               k(0.3, look=None), k(0.32, toon={'face': {'lid': 0.5, 'brow': -0.2}}, toonDur=0.08),                                           # back to the road: bored, seven frames
               k(W3 - 0.1, toon={'sq': [1.06, 0.9, 1.06], 'face': {'lid': 1}}, toonDur=0.08),                                               # a dip
               k(W3, look=[4.7, 1.3, DRV3[2] - 10.0], expr='surprised'), k(W3, toon={'scl': {'head': [1.5, 0.84, 1]}, 'sq': [0.95, 1.08, 0.95], 'hat': [0.2, 0.1, 3.1], 'face': {'pop': 0.7, 'jaw': 0.45}}, toonDur=0.06, toonEase='out'),   # the whip: the cap jumps
               k(W3 + 0.06, toon={'bend': {'neck': [0, 0, 0, 1.18, None]}, 'hat': [0.24, -0.1, 7.0], 'face': {'pop': 0.7, 'jaw': 0.45}}, toonDur=0.12, toonEase='out'),                                                           # it hangs, spinning
               k(W3 + 0.18, toon={'bend': {'neck': [0, 0, 0, 1.12, None]}, 'hat': [0.0, 0, 10.0], 'face': {'pop': 0.65, 'jaw': 0.4}}, toonDur=0.1, toonEase='in'),                                                                 # lands
               k(W3 + 0.28, toon={'bend': {'neck': [0, 0, 0, 1.1, None]}, 'hat': [0, 0, 12.566 + 3.1416], 'face': {'pop': 0.6, 'jaw': 0.4}}, toonDur=0.24, toonEase='out')]),   # and spins on, to a stop, back to front
        *[act(n, bus_at(ZC2, *loc), ry, 'stand', 'surprised', keys=[k(0.0, look=[4.7, 1.3, DRV3[2] - 10.0])]) for n, loc, ry in RIDERL[:1]]],
        props=[BUS(ZC2, line=' ', dest=' ')],
        look={'fill': 1.7},
        cams=[cam(0.0, [2.62, 1.55, DRV3[2] - 2.6], [2.59, 1.55, DRV3[2] - 2.53], [2.1, 1.69, DRV3[2]], [2.1, 1.69, DRV3[2]], lens=44)])   # far enough for the cap's jump to stay in the frame
st.cue('whoosh', 'S03', 0.0, 0.4, 0.3, 600, 2000); st.cue('sfx:boing', 'S03', W3, 0.4); st.cue('sfx:spring', 'S03', W3 + 0.08, 0.3); st.cue('clack', 'S03', W3 + 0.28, 0.25)

# 4: the sign at the edge of town: he goes by it, still braking; it spins on its post
D4 = st.dur('S04'); V4 = 14.0; P4 = 0.35              # he passes the sign
A4 = [1.1, 0, round(V4 * P4, 3)]; B4 = [1.1, 0, round(V4 * (P4 - D4), 3)]
DROP4 = {'drop': 0.4}                                 # seen from the side: he sits down on his heels (they hung 0.4 m over the road, his skid marks under them)
st.shot('S04', 'grassland', setOpts={'sky': ['#01ABF1', '#CFE7F1']}, look={'deepSky': False}, actors=[act('mec', A4, 180, 'heelBrake', 'worried', params=DROP4, keys=[k(0.0, look=None), k(0.0, to=B4, dur=D4, clip='heelBrake', params=DROP4, glide=True, ease='linear', face=180, cruise=True),
            k(0.0, toon={'tie': [1, 0, 0], 'face': {'gx': -0.8, 'gy': -0.4, 'brow': 0.8}}, toonDur=0.0), k(P4 + 0.1, toon={'tie': [1, 0, 0], 'face': {'brow': 1, 'mouth': 'wavy'}}, toonDur=0.08)])],   # tie: it stays on his chest (thrown up by the wind it flew over his head, loose from his collar)
        props=[P('road', 'roadStrip', pos=[-1.3, 0, 0], opts={'len': 500, 'w': 6.5}), P('sign', 'townSign', pos=[2.45, 0, 0], ry=-118, opts={'name': 'PARIS', 'spinAt': P4 + 0.03, 'turns': 2.07, 'spinDur': 0.72}),
               P('tower', 'eiffelTower', pos=[-32, 0, 190], opts={'h': 60}),
               P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A4[0], A4[2] - 0.55], [D4, B4[0], B4[2] - 0.55]], 'from': 0.0, 'to': D4, 'every': 0.025, 'marks': True, 'marksY': 0.08})],
        fx=[{'type': 'wind', 'at': 0.0, 'dur': D4 + 0.2, 'v': [0, 0, -9.0], 'attack': 0.0, 'release': 0.0}],   # a tail wind of nine metres a second: at fourteen in still air his tie flew back over his head and read as loose from his collar; now it lifts off his chest and no more
        cams=[cam(0.0, [-3.5, 0.85, -2.5], [-3.4, 0.87, -2.45], [2.25, 1.75, 0.25], [2.25, 1.75, 0.25], lens=44)])   # across the road: the sign, then him in front of it for six frames, then the sign alone
st.cue('whoosh', 'S04', P4 - 0.3, 0.5, 0.5, 500, 2200); st.cue('sfx:spring', 'S04', P4 + 0.03, 0.35)

# ---- the stop, laps later: he runs in the bus lane along the kerb (x = LANE), people wait on the pavement
LANE = 4.3
zrun = lambda z0, v, t: round(z0 - v * t, 3)
# 5: the third lap: three people in a line at the kerb, each holding the coat of the one in front; the last one flips his lap board with a flick of the
#    wrist: 2, 3. At the head of the line the lady holds her furled umbrella like a shepherd's crook: its big red crook stands over their heads
D5 = st.dur('S05'); F5 = 0.3                          # the board flips
LADY5, T35, TOUR5 = [5.75, 0, 0.0], [5.3, 0, 1.0], [5.5, 0, 2.0]   # the lady in front (with the crook), the second, the board man last (nearest the camera of S05)
HB5 = [5.56, 1.35, 0.12]                             # the grip of her umbrella, in her two hands: the shaft turns about it
BOARD5 = [TOUR5[0] + 0.32, 1.2, 2.06]               # the foot of the board's stick, in his left fist
CROOK = {'len': 1.25, 'crook': 0.17, 'tube': 0.045, 'crookColor': '#FFC83D', 'colors': ['#2F7F5C', '#F2EDE4']}   # a yellow crook: his tie is red
UMB = lambda rz, *keys, **kw: P('umb', 'crookUmbrella', pos=HB5, rot=[0, 0, rz], opts={**CROOK, **kw}, keys=list(keys))
LADYH = lambda dy=0.0: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'R': [HB5[0], HB5[1] + 0.06 + dy, HB5[2], 1, 0.05], 'L': [HB5[0], HB5[1] - 0.08 + dy, HB5[2], 1, 0.05]}}; LADYHOLD = LADYH()
TOURHOLD = lambda dy=0.0: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [BOARD5[0], BOARD5[1] + 0.06 + dy, BOARD5[2], 1, 0.05], 'R': [T35[0] + 0.2, 1.2, T35[2] + 0.2, 1, 0.06]}}
T3HOLD = {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [LADY5[0] + 0.05, 1.15, LADY5[2] + 0.2, 1, 0.06], 'R': [LADY5[0] - 0.12, 1.25, LADY5[2] + 0.18, 1, 0.06]}, 'bend': {'spine': [-0.2, 0, 0, 1, None]}}
st.shot('S05', 'parisStreet', setOpts={**STREET, 'eiffel': False, 'clouds': 0}, actors=[
        act('dame', LADY5, -50, 'stand', 'determined', keys=[k(0.0, look=[5.0, 1.5, 9.0]), k(0.0, toon={**LADYHOLD, 'bend': {'spine': [0, 0.1, 0, 1, None]}}, toonDur=0.0), k(0.4, toon={**LADYHOLD, 'bend': {'spine': [0.08, 0.16, 0, 1, None]}, 'sq': [1.04, 0.94, 1.04], 'face': {'brow': -0.5, 'eye': 0.15}}, toonDur=0.2)]),   # she braces
        act('tour', TOUR5, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[5.0, 1.5, 9.0]), k(0.0, toon=TOURHOLD(), toonDur=0.0),
            k(F5 - 0.08, toon={**TOURHOLD(0.07), 'scl': {'handL': [1.2, 0.85, 1.2]}, 'face': {'browL': 0.6}}, toonDur=0.07, toonEase='out'), k(F5, toon={**TOURHOLD(-0.03), 'scl': {'handL': [1.25, 0.8, 1.25]}}, toonDur=0.04, toonEase='in'), k(F5 + 0.06, toon=TOURHOLD(), toonDur=0.1, toonEase='outBack'),
            k(F5 + 0.2, toon={**TOURHOLD(), 'face': {'lid': 1}}, toonDur=0.04), k(F5 + 0.28, toon=TOURHOLD(), toonDur=0.04)]),   # a flick of the wrist (the hand goes up, snaps down), no look at the board; a blink
        act('t3', T35, 0, 'stand', 'worried', keys=[k(0.0, look=[5.0, 1.5, 9.0]), k(0.0, toon=T3HOLD, toonDur=0.0), k(0.35, toon={**T3HOLD, 'sq': [1.06, 0.92, 1.06], 'face': {'eye': 0.3, 'brow': 0.8}}, toonDur=0.2), k(0.4, expr='scared')])],
        props=[UMB(0.1, k(0.42, rotTo=[0, 0, -0.12], dur=0.25, ease='inOut')),
               P('board', 'lapBoard', pos=BOARD5, opts={'flips': [[0, '2'], [F5, '3']], 'w': 0.5}, keys=[k(F5 - 0.08, to=[BOARD5[0], BOARD5[1] + 0.07, BOARD5[2]], dur=0.07, ease='out'), k(F5 - 0.01, to=[BOARD5[0], BOARD5[1] - 0.03, BOARD5[2]], dur=0.04, ease='in'), k(F5 + 0.06, to=BOARD5, dur=0.1, ease='outBack')])],
        fx=[{'type': 'wind', 'at': 0.35, 'dur': 0.4, 'v': [0, 0, -9], 'attack': 0.25, 'release': 0.1}],
        cams=[cam(0.0, [5.3, 1.5, 5.6], [5.33, 1.5, 5.4], [5.75, 1.75, 1.0], [5.75, 1.75, 1.0], lens=44)])
st.cue('sfx:tick', 'S05', F5, 0.5); st.cue('gust', 'S05', 0.3, 0.3, 0.5)

# 6: he comes through (third staging). Seen from the kerb, down the street: he runs at us; she has stepped out of the line, one stride down the street
#    (the others are behind her), wound up; she swings the crook across his way: it takes him by the neck. The hook holds four frames: he hangs by it,
#    his neck twice as long, his tongue out, his feet gone on without him, toward us; the umbrella crosses the empty middle of the frame from her hands
#    to his neck. Then it gives: they leave one after the other, past us, an arm stretching before the feet leave the kerb. Then the lap board, alone,
#    left in the air: turned to us, twelve frames; it drops and bounces once
D6 = st.dur('S06'); V6 = 10.0; H6 = 0.3; R6 = H6 + 0.14; V6B = 11.0   # the hook; the release; their speed once they are a train
B6 = round(R6 + 0.28, 3)                              # the cut to the board
CAML6, LOOKL6 = [4.55, 2.35, 1.25], [5.72, 0.05, 2.0]   # where the camera goes to see it land
_yl6 = unit3([LOOKL6[0] - CAML6[0], 0, LOOKL6[2] - CAML6[2]]); _zl6 = [0.0, 1.0, 0.0]; _xl6 = cross3(_yl6, _zl6)   # the landed board: flat, its face up, its header away from the camera
ROTL6 = axes_euler(_xl6, _yl6, _zl6)
LAND6 = r3([LOOKL6[0] - 0.62 * _yl6[0], 0.03, LOOKL6[2] - 0.62 * _yl6[2]])   # the foot of its stick, toward us
LUN6 = [5.3, 0, -1.1]                                 # where she stands for the hook
HOOK6 = [LANE + 0.14, 1.3, -2.3]                      # where he is stopped (his line; the height is no longer used)
NECK6 = [LANE, 1.93, -2.2]                            # the middle of his neck while he hangs (measured: debugJoints): the crook goes round it
_h6 = unit3([NECK6[0] - LUN6[0], 0, NECK6[2] - LUN6[2]]); _e6 = math.asin((NECK6[1] - 1.3) / 1.25)   # the shaft: from her toward him, rising from her hands (1.3 m) to his neck
_X6 = [-_h6[2], 0, _h6[0]]                            # the crook lies flat: it opens toward her, its far side across his throat
if _X6[0] < 0: _X6 = [-_X6[0], 0, -_X6[2]]            # (its start on the pavement side of his neck)
_Y6 = [math.cos(_e6) * _h6[0], math.sin(_e6), math.cos(_e6) * _h6[2]]; _Z6 = cross3(_X6, _Y6)
END6 = [NECK6[i] + 0.17 * _X6[i] for i in range(3)]   # the end of the shaft: beside his neck (the crook's radius from its middle)
GRIP6 = r3([END6[i] - 1.25 * _Y6[i] for i in range(3)])   # the other end, in her hands
ROT6 = axes_euler(_X6, _Y6, _Z6)                      # (rot x, ry in degrees, rot z)
RY6 = ROT6[1]
YANK6 = [LANE, 0.13, round(HOOK6[2] - 0.42, 3)]       # where his hips are while he hangs by the collar, feet first
zh6 = lambda t: round(YANK6[2] - V6B * (t - R6), 3)   # his z once he is off again
LADYH6 = lambda dy=0.0: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'R': [*r3([GRIP6[i] + 0.04 * _Y6[i] + (dy if i == 1 else 0) for i in range(3)]), 1, 0.05], 'L': [*r3([GRIP6[i] + 0.2 * _Y6[i] + (dy if i == 1 else 0) for i in range(3)]), 1, 0.05]}}   # her two hands on the shaft
T3HOLD6 = {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [LUN6[0] + 0.05, 1.15, LUN6[2] + 0.22, 1, 0.06], 'R': [LUN6[0] - 0.12, 1.25, LUN6[2] + 0.2, 1, 0.06]}, 'bend': {'spine': [0.3, 0, 0, 1, None]}}   # he has kept hold of her coat: his arms have followed her
def leave6(who, pos0, t0, arm, hold):                 # one of the three: the arm that holds the one in front stretches (2 frames), then the feet leave the kerb
    tgt = lambda t: [LANE + OFFX6[who], FLY6[who], round(zh6(t) + GAP6[who], 3)]
    return [k(t0 - 0.07, toon={**hold, 'reach': {**hold.get('reach', {}), arm[0]: [*arm[1], 1, 0.06]}, 'sq': [1.05, 0.95, 1.05], 'face': {'eye': 0.35, 'brow': 0.9, 'jaw': 0.3}}, toonDur=0.07, toonEase='out'), k(t0 - 0.07, expr='scared'),
            k(t0, to=tgt(t0 + 0.1), dur=0.1, glide=True, clip='flag', params={'phase': PH6[who], 'swing': 0.2}, ease='in', face=180, blend=0.03),
            k(t0, toon={'sq': [0.8, 0.8, 1.7]}, toonDur=0.04), k(t0 + 0.08, toon={}, toonDur=0.08),                              # a smear as the feet leave
            k(t0 + 0.1, to=tgt(D6), dur=round(D6 - t0 - 0.1, 3), glide=True, clip='flag', params={'phase': PH6[who], 'swing': 0.2}, ease='linear', face=180, blend=0, cruise='out')]
GAP6 = {'dame': 1.95, 't3': 3.3, 'tour': 4.65}; OFFX6 = {'dame': 0.12, 't3': -0.1, 'tour': 0.15}; FLY6 = {'dame': 0.3, 't3': 0.45, 'tour': 0.25}; PH6 = {'dame': 0.0, 't3': 2.0, 'tour': 4.0}
GACK6 = {'lid': 1, 'tongue': 1, 'tongueLen': 0.16, 'jaw': 0.7, 'brow': 0.9, 'cheeks': 0.7}
st.shot('S06', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[
        act('mec', [LANE, 0, round(HOOK6[2] + V6 * H6, 3)], 180, 'run', 'worried', params=RUN, keys=[k(0.0, look=None),
            k(0.0, to=[LANE, 0, HOOK6[2]], dur=H6, clip='run', params=RUN, ease='linear', face=180, cruise='in'), k(0.0, toon=SPRINT(autoSq=0.2, face={'brow': 0.6}), toonDur=0.0),
            k(H6, to=YANK6, dur=0.07, glide=True, clip='flag', params={'dir': -1, 'droop': 0.8, 'swing': 0.0, 'flutter': 0.9, 'arms': 1.0, 'expr': 'scared'}, then='flag', ease='out', face=180, blend=0.04),   # the hook: his feet go on without him
            k(H6, toon={'bend': {'neck': [-0.2, 0, 0, 1.9, None], 'spine': [0, 0, 0, 1.22, None]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': GACK6, 'auto': 0.3}, toonDur=0.05, toonEase='out'), k(H6, expr='scared'),
            k(H6 + 0.07, toon={'bend': {'neck': [-0.25, 0, 0, 2.2, None], 'spine': [0, 0, 0, 1.3, None]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': GACK6, 'auto': 0.3}, toonDur=0.07),    # held: he goes on stretching
            k(R6, to=[LANE, 0, zh6(D6)], dur=round(D6 - R6, 3), clip='run', params=RUN, ease='linear', face=180, blend=0.07, cruise='out'),                                          # off again, with a train
            k(R6, toon=SPRINT(autoSq=0.45, sq=[0.9, 0.95, 1.25], face={'eye': 0.4, 'pupilSize': -0.4, 'brow': 1, 'mouth': 'wavy'}), toonDur=0.06, toonEase='out'), k(R6 + 0.12, toon=SPRINT(autoSq=0.45, face={'eye': 0.3, 'brow': 1, 'mouth': 'wavy', 'gx': -0.8}), toonDur=0.1)]),
        act('dame', LUN6, -145, 'stand', 'determined', keys=[k(0.0, look=[LANE, 1.5, 2.0]), k(0.0, toon={**LADYH6(0.3), 'bend': {'spine': [-0.22, 0.1, 0.2, 1.08, None]}, 'sq': [0.95, 1.1, 0.95], 'face': {'brow': -0.7, 'eye': 0.2}}, toonDur=0.0),   # wound up: the crook over her head
            k(H6 - 0.1, toon={**LADYH6(), 'bend': {'spine': [0.4, -0.1, -0.2, 1.05, None]}, 'sq': [1.06, 0.92, 1.06], 'face': {'brow': -0.9, 'mouth': 'clench'}}, toonDur=0.1, toonEase='in'), k(H6 - 0.1, look=NECK6),   # and across
            k(H6 + 0.02, toon={**LADYH6(), 'bend': {'spine': [-0.3, 0, 0, 1.1, None], 'armL': [0, 0, 0, 1.35, None], 'armR': [0, 0, 0, 1.35, None]}, 'sq': [0.95, 1.06, 0.95], 'face': {'eye': 0.3, 'brow': 0.8, 'mouth': 'clench'}}, toonDur=0.06, toonEase='out'),   # she holds on: heels on the kerb, arms out of their sleeves
            *leave6('dame', LUN6, R6, ('R', [LANE + 0.3, 1.32, HOOK6[2] - 0.6]), {'hands': {'L': 'grip', 'R': 'grip'}})]),
        act('t3', T35, 0, 'stand', 'scared', keys=[k(0.0, look=[LANE, 1.5, 3.0]), k(0.0, toon=T3HOLD6, toonDur=0.0), k(H6, look=HOOK6), k(H6, toon={**T3HOLD6, 'sq': [1.05, 0.94, 1.05], 'face': {'eye': 0.3, 'brow': 0.9}}, toonDur=0.08),
            *leave6('t3', T35, R6 + 0.1, ('L', [LANE + 0.5, 1.3, HOOK6[2] + 0.2]), T3HOLD6)]),
        act('tour', TOUR5, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[LANE, 1.5, 3.0]), k(0.0, toon=TOURHOLD(), toonDur=0.0), k(H6 + 0.06, look=HOOK6), k(H6 + 0.06, toon={**TOURHOLD(), 'face': {'browL': 0.7, 'eye': 0.2}}, toonDur=0.08),
            *leave6('tour', TOUR5, R6 + 0.2, ('R', [LANE + 0.45, 1.3, HOOK6[2] + 0.9]), {'hands': {'L': 'open', 'R': 'grip'}})])],
        props=[P('umb', 'crookUmbrella', pos=[GRIP6[0], GRIP6[1] + 0.3, GRIP6[2]], ry=RY6, rot=[0, 0, -0.22], opts=CROOK, keys=[k(H6 - 0.1, to=GRIP6, dur=0.1, ease='in'), k(H6 - 0.1, rotTo=[ROT6[0], math.radians(RY6), ROT6[2]], dur=0.1, ease='in'), k(R6, attach='mec', joint='torso', offset=[0, 0.58, -1.38], rot=[1.5708, 0, 0])]),
               P('board', 'lapBoard', pos=BOARD5, opts={'flips': [[0, '3']], 'w': 0.5, 'bright': True}, keys=[k(R6 + 0.2, rotTo=[0, 3.5, 0.12], dur=0.1, ease='out'), k(R6 + 0.3, rotTo=[0, 3.5, -0.1], dur=0.09), k(R6 + 0.39, rotTo=[0, 3.5, 0.06], dur=0.09), k(R6 + 0.48, rotTo=[0, 3.5, -0.04], dur=0.1), k(R6 + 0.58, rotTo=[0, 3.5, 0.02], dur=0.1),   # left in the air: his hand spins it round to us; it hangs, rocking, twelve frames
                    k(R6 + 0.68, to=LAND6, dur=0.16, ease='in'), k(R6 + 0.68, rotTo=[ROTL6[0], math.radians(ROTL6[1]) + 6.2832, ROTL6[2]], dur=0.16, ease='in'),                                                   # and drops, turning once: flat on the pavement, its header away from us
                    k(R6 + 0.84, to=[LAND6[0], LAND6[1] + 0.17, LAND6[2]], dur=0.07, ease='out'), k(R6 + 0.91, to=LAND6, dur=0.08, ease='in')])],                             # one bounce
        fx=[{'type': 'wind', 'at': R6 - 0.04, 'dur': 0.5, 'v': [0, 0, -12], 'attack': 0.05, 'release': 0.3}, {'type': 'shake', 'at': H6, 'dur': 0.12, 'amount': 0.015}],
        cams=[cam(0.0, [5.1, 1.0, -6.3], [5.08, 1.0, -6.2], [4.8, 1.45, -2.0], [4.8, 1.45, -2.0], lens=50),   # from the kerb, down the street: she at the left third (the line behind her), he at the right third, hanging; the umbrella across the empty middle
              cam(B6, [3.3, 1.25, 0.05], [3.42, 1.25, 0.14], [5.82, 1.3, 2.06], [5.82, 1.3, 2.06], lens=50),      # the board left in the air: a third of the width, a board's width clear of the down-pipe of the house front
              glide([cam(R6 + 0.7, CAML6, CAML6, LOOKL6, LOOKL6, lens=50)], 0.2)])   # the camera goes up and looks down on it: it lands whole, its header readable
st.cue('whoosh', 'S06', 0.0, 0.45, 0.3, 400, 2400); st.cue('whoosh', 'S06', H6 - 0.12, 0.35, 0.12, 900, 3000); st.cue('sfx:twang', 'S06', H6, 0.45); st.cue('sfx:stretch', 'S06', H6 + 0.02, 0.4)
st.cue('sfx:boing', 'S06', R6, 0.4); [st.cue('whoosh', 'S06', R6 + d, 0.3, 0.2, 600, 2200) for d in (0.0, 0.1, 0.2)]; st.cue('clack', 'S06', R6 + 0.84, 0.45); st.cue('clack', 'S06', R6 + 0.99, 0.25)

# 7: the mayor settles it: his hand goes up like a blade, holds, comes down: the desk is cut in two
D7 = st.dur('S07'); C7 = 0.62                         # the blow
MAY7 = [0.0, 0, -1.62]; DESK7 = [0.0, 0, -0.9]
OFFICE = {'desk': False, 'map': False, 'plant': False}
UP7 = lambda dy=0.0: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [0.02, 2.74 + dy, -1.5, 1, 0.08, [1, -0.25, 0.1]], 'R': [-0.02, 2.74 + dy, -1.5, 1, 0.08, [-1, -0.25, 0.1]]}}   # both hands joined into one block over his head, elbows out: an axe
DOWN7 = lambda y: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [0.02, y, -0.98, 1, 0.08], 'R': [-0.02, y, -0.98, 1, 0.08]}}
DUST7 = lambda a: {'hands': {'L': 'open', 'R': 'open'}, 'reach': {'L': [0.06, 1.18 + 0.07 * a, -1.3, 1, 0.06], 'R': [-0.06, 1.18 - 0.07 * a, -1.3, 1, 0.06]}}   # he dusts his hands: one palm goes down the other
jump7 = lambda pid, name, pos, opts, dy, dx: P(pid, name, pos=pos, opts=opts, keys=[k(C7, to=[pos[0] + dx * 0.5, pos[1] + dy, pos[2]], dur=0.12, ease='out'), k(C7 + 0.12, to=[pos[0] + dx, pos[1] - 0.3, pos[2] + 0.05], dur=0.2, ease='in'), k(C7, rotTo=[0.3, 0.6, dx * 3], dur=0.32)])
st.shot('S07', 'mairie', setOpts={**OFFICE, 'bannerY': 3.3}, actors=[act('maire', MAY7, 0, 'stand', 'determined', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gy': 0.5}}, toonDur=0.0),
            k(0.05, toon={**UP7(), 'sq': [0.94, 1.1, 0.94], 'bend': {'spine': [-0.28, 0, 0, 1.05, None]}, 'face': {'gy': 0.5, 'brow': -0.6, 'cheeks': 0.6}}, toonDur=0.22, toonEase='outBack'),   # up on his toes, a breath, the hands high behind his head
            k(0.27, toon={**UP7(0.1), 'sq': [0.91, 1.15, 0.91], 'bend': {'spine': [-0.36, 0.04, 0, 1.1, None], 'armL': [0, 0, 0, 1.12, None], 'armR': [0, 0, 0, 1.12, None]}, 'settle': 0.5, 'face': {'gy': 0.5, 'brow': -0.75, 'cheeks': 0.9, 'lidL': 0.4}}, toonDur=0.2, toonEase='inOut'),   # the hold moves: he goes on rising, the arms go on stretching, it trembles
            k(0.47, toon={**UP7(0.13), 'sq': [0.9, 1.17, 0.9], 'bend': {'spine': [-0.4, -0.04, 0, 1.12, None], 'armL': [0, 0, 0, 1.16, None], 'armR': [0, 0, 0, 1.16, None]}, 'face': {'gy': 0.5, 'brow': -0.85, 'cheeks': 1, 'mouth': 'clench'}}, toonDur=0.1),
            k(C7 - 0.05, toon={**DOWN7(0.84), 'sq': [1.2, 0.78, 1.2], 'bend': {'spine': [0.55, 0, 0, 0.95, None]}, 'face': {'gy': 0.6, 'brow': -0.9, 'mouth': 'clench'}}, toonDur=0.05, toonEase='in'),   # down in two frames
            k(C7 + 0.1, toon={**DOWN7(0.55), 'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.5, 0, 0, 1, None]}, 'face': {'gy': 0.6}}, toonDur=0.1),
            k(C7 + 0.26, toon={**DUST7(1), 'sq': [0.94, 1.09, 0.94], 'bend': {'spine': [-0.1, 0, 0, 1.03, None], 'neck': [-0.2, 0, 0, 1, None]}, 'face': {'brow': 0.4}}, toonDur=0.14, toonEase='outBack'), k(C7 + 0.26, expr='smug'),   # he comes up past his height and back: chin up
            k(C7 + 0.42, toon={**DUST7(-1), 'settle': 0.4, 'bend': {'neck': [-0.22, 0, 0, 1, None]}, 'face': {'brow': 0.4, 'lid': 0.5}}, toonDur=0.08), k(C7 + 0.52, toon={**DUST7(1), 'bend': {'neck': [-0.22, 0, 0, 1, None]}, 'face': {'brow': 0.4, 'lid': 1}}, toonDur=0.08),   # he dusts his hands, twice; a slow blink
            k(C7 + 0.62, toon={**DUST7(-1), 'bend': {'neck': [-0.22, 0.06, 0, 1, None]}, 'face': {'browL': 0.6}}, toonDur=0.08), k(C7 + 0.74, toon={'bend': {'neck': [-0.2, 0.06, 0, 1, None]}, 'face': {'browL': 0.6}}, toonDur=0.12)])],
        props=[P('desk', 'splitDesk', pos=DESK7, opts={'at': C7, 'w': 1.7}),
               jump7('pot', 'mug', [-0.5, 0.76, -0.85], {}, 0.45, -0.25), jump7('paper', 'paperPile', [0.45, 0.765, -0.8], {'count': 8}, 0.6, 0.3),
               P('crack', 'impactStars', pos=[0.0, 0.85, -0.6], opts={'at': C7, 'n': 5, 'r': 0.42, 'r0': 0.16, 'dur': 0.26, 'size': 0.085})],
        fx=[{'type': 'shake', 'at': C7, 'dur': 0.2, 'amount': 0.03}],
        cams=[cam(0.0, [0.35, 1.9, 2.3], [0.3, 1.9, 2.15], [0.0, 1.4, -1.2], [0.0, 1.4, -1.2], lens=60)])   # from higher, looking down: the desk at two thirds of the height, over the captions; his hands against the bare wall
st.cue('sfx:slideUp', 'S07', 0.05, 0.3); st.cue('whoosh', 'S07', C7 - 0.08, 0.4, 0.1, 700, 2600); st.cue('thud', 'S07', C7, 0.7); st.cue('clack', 'S07', C7 + 0.02, 0.5); st.cue('sfx:boing', 'S07', C7 + 0.26, 0.25); [st.cue('pop', 'S07', C7 + d, 0.2) for d in (0.44, 0.54, 0.64)]

# 8: « C'est une ligne. »: he says it, the map of the line in his hand: a loop, and on it a little head that goes round
D8 = st.dur('S08'); MAP8 = [0.61, 1.06, -1.2]; TAP8 = 0.52
W8 = [round(w['s'] - st.SH['S08'][0], 3) for w in st.L['L05']['words']]   # his words
HAND8 = lambda r, **kw: {'hands': {'L': 'grip', 'R': 'point'}, 'reach': {'L': [MAP8[0] + 0.3, MAP8[1] + 0.5, MAP8[2] - 0.03, 1, 0.05], 'R': [*r, 1, 0.12]}, **kw}   # the map in his left hand, his right forefinger at r
R8A, R8B, R8C, R8D = [MAP8[0] - 0.14, MAP8[1] + 0.36, MAP8[2] + 0.06], [MAP8[0] - 0.22, MAP8[1] + 0.42, MAP8[2] + 0.24], [MAP8[0] - 0.02, MAP8[1] + 0.3, MAP8[2] + 0.03], [MAP8[0] - 0.06, MAP8[1] + 0.32, MAP8[2] + 0.08]   # over the loop; drawn back; on it; resting
st.shot('S08', 'mairie', setOpts={**OFFICE, 'banner': False}, actors=[act('maire', MAY7, 0, 'stand', 'smug', keys=st.talk('L05', 'S08', 'smug') + [k(0.0, look=None),
            k(0.0, toon=HAND8(R8A, face={'browL': 0.5}), toonDur=0.0),
            k(W8[0], toon=HAND8(R8A, sq=[0.98, 1.04, 0.98], face={'jaw': 0.6, 'browL': 0.8}), toonDur=0.05, toonEase='out'), k(W8[0] + 0.11, toon=HAND8(R8A, face={'browL': 0.5}), toonDur=0.07),   # « C'est »: the jaw long on each word
            k(W8[1], toon=HAND8(R8A, face={'jaw': 0.4, 'browL': 0.6}), toonDur=0.04, toonEase='out'), k(W8[1] + 0.07, toon=HAND8(R8A, face={'browL': 0.5}), toonDur=0.05),                          # « une »
            k(TAP8 - 0.12, toon=HAND8(R8B, bend={'spine': [-0.06, 0.05, 0, 1.02, None]}, face={'jaw': 0.75, 'brow': 0.7}), toonDur=0.09, toonEase='out'),                                         # « ligne »: the finger draws back, he draws breath
            k(TAP8 - 0.03, toon=HAND8(R8C, scl={'handR': [1.4, 1.4, 1.4]}, bend={'spine': [0.16, -0.08, 0, 1, None]}, sq=[1.03, 0.96, 1.03], face={'jaw': 0.75, 'brow': 0.8}), toonDur=0.03, toonEase='in'),   # and comes down on the loop: his whole body behind the finger
            k(TAP8 + 0.05, toon=HAND8(R8D, settle=0.7, bend={'spine': [0.07, -0.05, 0, 1, None]}, face={'jaw': 0.45, 'brow': 0.6}), toonDur=0.1, toonEase='outBack'),
            k(TAP8 + 0.22, toon=HAND8(R8D, bend={'spine': [0.04, -0.05, 0, 1, None]}, face={'browL': 0.6}), toonDur=0.1),                                                                           # his mouth shuts on it
            k(TAP8 + 0.36, toon=HAND8(R8D, bend={'spine': [-0.05, -0.05, 0, 1.03, None]}, face={'browL': 0.7, 'lid': 0.4}), toonDur=0.14)])],                                                       # he draws himself up: there
        props=[P('desk', 'splitDesk', pos=DESK7, opts={'at': -1, 'w': 1.7}), P('map', 'lineMap', pos=MAP8, ry=-8, opts={'title': 'LIGNE 12 BIS', 'lap': 0.9}, keys=[k(TAP8, rotTo=[0.09, -0.14, 0], dur=0.03), k(TAP8 + 0.03, rotTo=[0, -0.14, 0], dur=0.14, ease='outBack')]),
               P('tap', 'impactStars', pos=[MAP8[0] - 0.02, MAP8[1] + 0.3, MAP8[2] + 0.06], opts={'at': TAP8, 'n': 4, 'r': 0.2, 'r0': 0.06, 'dur': 0.24, 'size': 0.045})],   # the tap: the map gives, four stars
        cams=[cam(0.0, [0.83, 1.62, 1.5], [0.8, 1.62, 1.38], [0.3, 1.72, -1.4], [0.3, 1.72, -1.4], lens=44)])   # the whole map in the frame, its loop over the caption band
st.cue('clack', 'S08', TAP8, 0.4)

# 9: the display of the stop: 1 MIN, 0 MIN; the pigeon on it looks up the street
D9 = st.dur('S09'); DISP = [5.6, 0, 1.2]; PIG = [DISP[0], 2.6 + 0.24, DISP[2]]
DISPLAY = lambda texts, **kw: P('disp', 'busDisplay', pos=DISP, ry=90, opts={'line': '12 BIS', 'texts': texts, **kw})
st.shot('S09', 'parisStreet', setOpts={**STREET, 'eiffel': False}, props=[DISPLAY([[0, '1 MIN'], [0.33, '0 MIN']]),
               P('pig', 'pigeon', pos=PIG, ry=90, keys=[k(0.12, rotTo=[0, math.radians(20), 0], dur=0.1, ease='outBack')])],
        cams=[cam(0.0, [7.95, 1.95, 1.8], [7.85, 1.97, 1.75], [5.62, 2.56, 1.21], [5.62, 2.56, 1.21], lens=44)])
st.cue('sfx:tick', 'S09', 0.33, 0.5)

# ---- the line: he runs along the lane, the three passengers fly behind him like a kite's tail (the lady hooked to his collar by her umbrella)
GAP = {'dame': 1.95, 't3': 3.3, 'tour': 4.65}; OFFX = {'dame': 0.12, 't3': -0.1, 'tour': 0.15}; FLY = {'dame': 0.3, 't3': 0.45, 'tour': 0.25}; PH = {'dame': 0.0, 't3': 2.0, 'tour': 4.0}
HEADSIGN = lambda texts=None, **kw: P('hs', 'headSign', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.56, 0.0], 'sway': 1}, opts={'texts': texts or [[0, '12 BIS']], 'w': 0.55, 'hh': 0.16, 'frame': '#D8DCE2', 'posts': 0.014, **kw})
COLLAR = {'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.58, -1.38], 'rot': [1.5708, 0, 0]}   # the grip 1.25 m behind his collar, the crook on it
HEADFWD, HEADDROP = 0.45, 0.3                        # running, his head is that far ahead of his feet and that much lower than standing: aim close cameras there
def rider(who, z0, v, dur, expr='scared', keys=(), **par):        # one passenger of the tail: z0 is the hero's z at 0
    a = [LANE + OFFX[who], FLY[who], round(z0 + GAP[who], 3)]; b = [a[0], a[1], round(a[2] - v * dur, 3)]; pr = {'phase': PH[who], 'swing': 0.16, **par}
    return act(who, a, 180, 'flag', expr, params=pr, keys=[k(0.0, look=None), k(0.0, to=b, dur=dur, clip='flag', params=pr, glide=True, ease='linear', face=180, cruise=True), *keys])
def runner(z0, v, dur, expr='unimpressed', keys=(), x=None, close=True, par=None, **opt):       # the hero (close: the run of a close-up: slow cadence, small bounce)
    x = LANE if x is None else x; par = par or (RUNC if close else RUN); cad = {'cadence': CAD} if close else {}
    return act('mec', [x, 0, z0], 180, 'run', expr, params=par, keys=[k(0.0, look=None), k(0.0, to=[x, 0, round(z0 - v * dur, 3)], dur=dur, clip='run', params=par, ease='linear', face=180, cruise=True, **cad), *keys], **opt)
TAIL = lambda z0, v, dur, **kw: [rider(w, z0, v, dur, **kw) for w in ('dame', 't3', 'tour')]
UMBT = lambda: P('umb', 'crookUmbrella', on=COLLAR, opts=CROOK)
JOG = lambda **kw: SPRINT(**{'autoSq': 0.0, **kw})   # his toon base while running, seen close: no automatic squash on the footfalls (with it and the stride's own squash his head travelled 8 % of the frame height at each stride: the face could not be read; without, 3 %: the display, the tie and the arms carry the stride)
closeup = lambda z0, v, dur, side=1.2, back=2.75, h=1.6, dy=0.0, push=0.12: [cam(0.0, [LANE + side, h, z0 - back], [LANE + side - push, h, z0 - v * dur - back + push], [LANE, 1.72 + dy, z0 - HEADFWD], [LANE, 1.72 + dy, z0 - v * dur - HEADFWD], lens=44)]   # the camera running backward in front of him, on his head

# 10: he comes through the stop with his passengers: 0 MIN; the display goes back to 8 MIN, the pole of the stop bends after him and rings, the pigeon is gone
D10 = st.dur('S10'); P10 = 0.3; V10 = 10.0            # he is level with the pole
z10 = round(1.5 + V10 * P10, 3)
POLE10 = [5.45, 0, 0.1]
st.shot('S10', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[runner(z10, V10, D10, close=False, keys=[k(0.0, toon=SPRINT(autoSq=0.2, bend=WHEELB), toonDur=0.0)]), *TAIL(z10, V10, D10)],
        props=[WHEEL(), DISPLAY([[0, '0 MIN'], [P10 + 0.22, '8 MIN']]), STOPPOLE(pos=POLE10, h=3.05, plateOff=0.06, boardDy=-0.5, bend=[[P10 - 0.02, 0], [P10 + 0.12, 0.55]], spring=[[P10 + 0.12, 0.55, 14, 3.4]]), HEADSIGN(), UMBT(),
               P('pig', 'pigeon', pos=PIG, ry=110, keys=[k(P10 + 0.02, to=[PIG[0] - 0.3, PIG[1] + 0.9, PIG[2] - 2.6], dur=0.3, ease='out'), k(P10 + 0.02, rotTo=[0.8, 3.0, 2.2], dur=0.3), k(P10 + 0.32, to=[PIG[0] - 0.6, PIG[1] + 1.6, PIG[2] - 7.0], dur=0.5, ease='linear')]),
               *[P(f'feather{i}', 'feather', pos=[PIG[0] + dx, PIG[1] + 0.25 + dy, PIG[2] - 0.15 + dz], ry=90, opts={'at': P10 + 0.1 + 0.05 * i, 'dur': D10 - P10 - 0.1 - 0.05 * i + 0.3 * (i > 0), 'fall': fl, 'sway': sw, 'swings': n, 's': sz}) for i, (dx, dy, dz, fl, sw, n, sz) in enumerate([(0, 0, 0, 1.3, 0.3, 2.2, 2.6), (0.05, 0.2, -0.45, 1.2, 0.24, 2.6, 2.0), (-0.05, 0.1, 0.4, 1.5, 0.36, 1.8, 2.3)])]],   # what is left of the pigeon: a feather comes down through the empty end of the shot
        fx=[{'type': 'wind', 'at': P10 - 0.08, 'dur': 0.7, 'v': [0, 0, -12], 'attack': 0.05, 'release': 0.3}],
        cams=[cam(0.0, [8.6, 1.55, -1.9], [8.5, 1.55, -1.8], [5.5, 1.9, 0.5], [5.5, 1.9, 0.5], lens=44)])   # the plate of the stop whole, under the top of the frame
st.cue('whoosh', 'S10', P10 - 0.25, 0.5, 0.8, 400, 2400); st.cue('sfx:tick', 'S10', P10 + 0.22, 0.5); st.cue('sfx:spring', 'S10', P10 + 0.12, 0.4)

def trackcam(z0, v, t0, t1, cf, cl, lens=44):       # a camera that travels with him from t0 to t1 of the shot: cf = [x, y, dz] where it is, cl = [x, y, dz] what it looks at (dz from his feet)
    za, zb = z0 - v * t0, z0 - v * t1
    return cam(t0, [cf[0], cf[1], round(za + cf[2], 3)], [cf[0], cf[1], round(zb + cf[2], 3)], [cl[0], cl[1], round(za + cl[2], 3)], [cl[0], cl[1], round(zb + cl[2], 3)], lens=lens)
UPNECK = {'spine': [0.42, 0, 0, 1.04, None], 'neck': [-0.5, 0, 0, 1.1, None]}   # his chin up (the running base with the neck further back)

# 11: his number: close, the camera running backward in front of him: the display on his head; his eyes go up to it, his chin follows; back to us: a brow
D11 = st.dur('S11'); Z11 = 20.0
st.shot('S11', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z11, V, D11, expr='neutral', keys=[k(0.0, toon=JOG(face={'brow': 0.2}), toonDur=0.0),
                 k(0.1, toon=JOG(face={'gy': -0.75, 'brow': 0.6, 'eye': 0.2}), toonDur=0.06), k(0.18, toon=JOG(bend=UPNECK, face={'gy': -0.75, 'brow': 0.6, 'eye': 0.2}), toonDur=0.1, toonEase='out'),   # the eyes first, the chin three frames later
                 k(0.5, toon=JOG(bend=UPNECK, face={'brow': -0.3, 'eye': 0.1}), toonDur=0.06), k(0.58, toon=JOG(face={'brow': -0.3}), toonDur=0.1, toonEase='out'),                               # back to us: the eyes, then the head
                 k(0.74, toon=JOG(face={'lid': 1}), toonDur=0.04), k(0.82, toon=JOG(face={'browL': 0.5}), toonDur=0.05)], blink=0),
            *TAIL(Z11, V, D11)],
        props=[HEADSIGN(), UMBT()],
        cams=closeup(Z11, V, D11, side=1.3, back=2.5, h=1.7, dy=0.08))
st.cue('sfx:tick', 'S11', 0.0, 0.3)

# 12: his inspectors (fourth staging). From the pavement, low, looking up: the lady flies flat across the bottom of the frame; the inspector stands on
#     her back, knees bent, arms out: a surfer, his head against the sky: four frames. From the left a passenger's arm comes in, long, with one ticket,
#     up into the sky (the passenger himself is out of the frame); the inspector's head goes to it; an oversized punch comes up in his hand: clack; confetti
#     leave in the wind; he nods; his eyes come to us
D12 = st.dur('S12'); Z12 = 12.0; T12 = 0.24; PU12 = 0.66
SURF = [LANE + OFFX['dame'], FLY['dame'] + 1.05 + 0.1, round(Z12 + GAP['dame'] - 0.3, 3)]       # the inspector's feet: on the lady's back
TK12 = [LANE + 0.5, 2.8, round(Z12 + 2.37, 3)]                                                  # the ticket, held up at his right (the left of the picture), in the sky
CAM12, LOOK12 = [LANE + 2.9, 0.45, 1.85], [LANE + 0.2, 2.2, 1.8]                                 # the camera and what it looks at: x, y, metres behind the hero
mv12 = lambda p_, t: [p_[0], p_[1], round(p_[2] - V * t, 3)]                                    # a point that travels with them
ARM12 = lambda t, dy=0.0: {'hands': {'R': 'pinch', 'L': 'grip'}, 'reach': {'R': [TK12[0] - 0.02, TK12[1] - 0.16 + dy, mv12(TK12, t)[2] + 0.05, 1, 0.05]}}   # the passenger's near arm
_a12 = math.radians(90)                                                                           # the ticket is turned 90 degrees: its face to the camera
N12, DJ12 = (math.sin(_a12), 0.0, math.cos(_a12)), (-math.cos(_a12), 0.0, math.sin(_a12))       # the ticket's face; the way the jaws point: along the ticket, away from the inspector (screen left)
HOLE12 = [TK12[0] + 0.224 * math.cos(_a12), TK12[1] + 0.022, TK12[2] - 0.224 * math.sin(_a12)]  # where the hole is punched (bigTicket holeAt: 0.4 w from its middle, in the blank margin after the number)
_c12, _s12 = math.cos(math.radians(50)), math.sin(math.radians(50))                              # rolled 50 degrees about its length: both jaws show
_X12 = (N12[0] * _c12, _s12, N12[2] * _c12); _Z12 = (_X12[1] * DJ12[2] - _X12[2] * DJ12[1], _X12[2] * DJ12[0] - _X12[0] * DJ12[2], _X12[0] * DJ12[1] - _X12[1] * DJ12[0])
PROT12 = (round(math.atan2(-_Z12[1], _Z12[2]), 4), round(math.degrees(math.asin(max(-1.0, min(1.0, _Z12[0])))), 2), round(math.atan2(-DJ12[0], _X12[0]), 4))   # that frame as rot x, ry (deg), rot z (jaws = +Y)
pv12 = lambda back, dy=0.0: [round(HOLE12[0] - (0.26 + back) * DJ12[0], 3), round(HOLE12[1] + dy, 3), round(HOLE12[2] - (0.26 + back) * DJ12[2], 3)]   # the pivot of the punch, `back` metres short of the bite
REST12, READY12, BITE12, BACK12 = pv12(0.34, -0.3), pv12(0.13), pv12(0.0), pv12(0.26, -0.06)
PK12 = [(0.0, REST12), (T12 + 0.1, REST12), (PU12 - 0.1, READY12), (PU12, BITE12), (PU12 + 0.1, BITE12), (round(PU12 + 0.22, 3), BACK12), (D12, BACK12)]   # (t, where the punch is): it comes up open, bites, holds three frames, draws back
XTR12 = [{'face': {'browL': 0.6}}, {'face': {'browL': 0.6, 'lid': 0.3}}, {'sq': [1.04, 0.95, 1.04], 'face': {'browL': 0.8, 'mouth': 'clench'}}, {'sq': [1.04, 0.95, 1.04], 'face': {'browL': 0.8, 'mouth': 'clench'}},
         {'face': {'lid': 1}}, {'bend': {'neck': [0.25, 0, 0, 1, None]}, 'face': {'browL': 0.4}}]   # his face on each leg of it: the bite, a slow blink, a nod
PUN12 = lambda i, **kw: {'hands': {'R': 'grip', 'L': 'open'}, 'reach': {'R': [round(PK12[i][1][0] - 0.17 * DJ12[0], 3), PK12[i][1][1], round(PK12[i][1][2] - 0.17 * DJ12[2] - V * PK12[i][0], 3), 1, 0.05]}, **kw}   # his right fist on its handles (the ticket is at his right)
camat12 = lambda t: [CAM12[0], CAM12[1], round(Z12 - V * t + CAM12[2], 3)]
st.shot('S12', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z12, V, D12, keys=[k(0.0, toon=JOG(face={'gy': -0.2}), toonDur=0.0)]),
            rider('dame', Z12, V, D12, expr='worried', swing=0.05, flutter=0.5),
            rider('t3', Z12, V, D12, expr='worried', keys=[k(0.0, toon=ARM12(0.0, -1.4), toonDur=0.0), k(T12 - 0.12, toon={**ARM12(T12), 'face': {'brow': 0.8, 'eye': 0.2}}, toonDur=0.12, toonEase='outBack'),   # his arm comes forward, long, with the ticket
                 *[k(round(T12 + 0.1 * i, 3), toon=ARM12(round(T12 + 0.1 * (i + 1), 3)), toonDur=0.1, toonEase='linear') for i in range(int((D12 - T12) / 0.1) + 1)]]),
            act('ctrl', SURF, 100, 'surfRide', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=mv12(SURF, D12), dur=D12, clip='surfRide', glide=True, ease='linear', face=100, cruise=True),
                 k(0.0, toon={'sq': [1.04, 0.94, 1.04]}, toonDur=0.0), k(0.02, toon={'sq': [0.98, 1.03, 0.98]}, toonDur=0.1, toonEase='inOut'), k(0.12, toon={'sq': [1.02, 0.97, 1.02]}, toonDur=0.08),   # the surfer, arms out: four frames before the ticket
                 *[k(round(T12 - 0.06 + 0.1 * i, 3), look=mv12(TK12, T12 - 0.06 + 0.1 * i + 0.05)) for i in range(0, 5)],                                 # his head goes to the ticket
                 k(T12 - 0.02, toon=PUN12(1, **XTR12[0]), toonDur=0.1, toonEase='out'),                                                                   # his hand finds the punch
                 *[k(PK12[i][0], toon=PUN12(i + 1, **XTR12[i]), toonDur=round(PK12[i + 1][0] - PK12[i][0], 3), toonEase='linear') for i in range(1, len(PK12) - 1)],   # and goes with it
                 k(PU12 + 0.3, look=camat12(PU12 + 0.35))])],                                                                                             # then his eyes come to us
        props=[HEADSIGN(), UMBT(),
               P('tk0', 'bigTicket', pos=mv12(TK12, 0.0), ry=90, scale=0.01, opts={'w': 0.56, 'punchAt': PU12, 'hole': '#62AEE2', 'holeAt': [0.4, 0.08], 'textX': 0.41, 'textW': 0.62}, keys=[k(0.0, to=mv12(TK12, D12), dur=D12, ease='linear'), k(T12 - 0.04, scale=1.0, dur=0.08, ease='outBack')]),   # the hole shows the sky
               P('punch', 'ticketPunch', pos=mv12(REST12, 0.0), rot=[PROT12[0], 0, PROT12[2]], ry=PROT12[1], scale=0.01, opts={'snapAt': PU12, 's': 1.5, 'grip': '#F2C230', 'jaw': '#3A3F47'},
                 keys=[k(T12, scale=1.0, dur=0.08, ease='outBack'), *[k(PK12[i][0], to=mv12(PK12[i + 1][1], PK12[i + 1][0]), dur=round(PK12[i + 1][0] - PK12[i][0], 3), ease='linear') for i in range(len(PK12) - 1)]]),   # it pops into his hand
               P('conf', 'confetti', pos=mv12(HOLE12, PU12), opts={'at': PU12, 'n': 3, 's': 2.6, 'dur': D12 - PU12, 'fall': 0.5, 'drift': [0.2, 3.0]}, keys=[k(PU12, to=mv12(HOLE12, D12), dur=D12 - PU12, ease='linear')])],   # three confetti from the hole, big enough to be seen
        cams=[trackcam(Z12, V, 0.0, D12, CAM12, LOOK12, lens=65)])   # low on the pavement, looking up: the lady across the bottom, his head, the ticket and the punch against the sky
st.cue('pop', 'S12', T12, 0.3); st.cue('sfx:stretch', 'S12', T12 - 0.1, 0.25); st.cue('clack', 'S12', PU12, 0.6); st.cue('sfx:tick', 'S12', PU12 + 0.02, 0.3)

# 13: he asks to get off, in three pictures: his face, the tongue in the wind, his eyes going down; an insert on the knot of his tie: the finger comes,
#     waits, trembling, and presses: the button gives, a ring of red; his face again: the display says ARRÊT DEMANDÉ, the tongue goes back in, hope
D13 = st.dur('S13'); Z13 = 4.0; PR13 = 0.62; IN13, FA13 = 0.3, 0.76   # the press; the cuts to the insert and back to his face
TIRED = {'tongue': 1, 'tongueLen': 0.42, 'tongueYaw': 1.5, 'tongueW': 1.2, 'sweat': 1}   # the tongue flies the way the tie flies
BUTTON = lambda at_=None: P('stopb', 'stopButton', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.47, 0.155]}, opts={'pressAt': at_, 's': 1.5})
FING13 = lambda z, dx=0.0, dy=0.0, **face: JOG(face={**TIRED, 'gy': 0.8, **face}, hands={'R': 'point'}, touch={'R': ['torso', dx, 0.47 + dy, z, 1, 0.15]})
st.shot('S13', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z13, V, D13, expr='tired', par=RUNI, keys=[k(0.0, toon=JOG(face={**TIRED, 'lid': 0.4}), toonDur=0.0),
                 k(0.1, toon=JOG(face={**TIRED, 'gy': 0.8}), toonDur=0.07),                                                              # his eyes go down to the button
                 k(0.2, toon=FING13(0.31, -0.1, 0.02), toonDur=0.12, toonEase='out'),                                                    # the finger comes
                 k(0.36, toon=FING13(0.29, -0.085, 0.0), toonDur=0.06), k(0.42, toon=FING13(0.3, -0.097, 0.006), toonDur=0.06), k(0.48, toon=FING13(0.29, -0.082, -0.004), toonDur=0.06),   # its tip waits beside the button (toward his right: the left of the picture), trembling
                 k(0.54, toon=FING13(0.33, -0.13, 0.0, brow=0.6), toonDur=0.04, toonEase='out'),                                           # draws back
                 k(PR13 - 0.05, toon=FING13(0.235, -0.005, 0.0, brow=0.9), toonDur=0.05, toonEase='in'),                                    # and presses
                 k(PR13 + 0.1, toon=FING13(0.24, -0.005, 0.0, brow=0.9), toonDur=0.04),
                 k(FA13, toon=JOG(face={'gy': -0.75, 'brow': 0.9, 'eye': 0.25, 'sweat': 1}), toonDur=0.07, toonEase='out'), k(FA13, expr='neutral'),   # his face: the tongue goes back in, his eyes go up to the display
                 k(FA13 + 0.08, toon=JOG(bend=UPNECK, face={'gy': -0.75, 'brow': 0.9, 'eye': 0.25, 'sweat': 1}), toonDur=0.1, toonEase='out'),
                 k(FA13 + 0.22, toon=JOG(bend=UPNECK, face={'brow': 0.4, 'eye': 0.15, 'pupilSize': 1.5}), toonDur=0.06), k(FA13 + 0.28, toon=JOG(face={'brow': 0.4, 'eye': 0.15, 'pupilSize': 1.5, 'cheeks': 0.5}, sq=[0.98, 1.04, 0.98]), toonDur=0.1, toonEase='outBack'),
                 k(FA13 + 0.2, expr='surprisedHappy')], blink=0),                                                                                # then to us, pupils wide: hope
            *TAIL(Z13, V, D13)],
        props=[HEADSIGN([[0, '12 BIS'], [PR13, 'ARRÊT DEMANDÉ']]), BUTTON(PR13), UMBT()],
        cams=[trackcam(Z13, V, 0.0, IN13, [LANE + 1.2, 1.6, -2.75], [LANE, 1.72, -HEADFWD]),
              trackcam(Z13, V, IN13, FA13, [LANE + 0.38, 1.42, -1.22], [LANE + 0.0, 1.42, -0.36], lens=40),
              trackcam(Z13, V, FA13, D13, [LANE + 1.1, 1.62, -2.55], [LANE, 1.76, -HEADFWD])])
st.cue('sfx:tick', 'S13', PR13, 0.5); st.cue('sfx:ding', 'S13', PR13 + 0.03, 0.5); st.cue('pop', 'S13', FA13 + 0.02, 0.25)

# 14: the answer: the inspector comes down into the frame beside his head, hanging head down like a bat: two faces, one the wrong way up. His tie falls
#     over his face (he hangs the wrong way up); he flicks it away
D14 = st.dur('S14'); Z14 = -6.0; F14 = 0.24; TI14, FL14 = 0.42, 0.76   # he drops in; the tie falls over his face; he flicks it away
BATX, BATY = LANE - 0.58, 1.62 - HEADDROP + 0.48     # where he hangs: his head level with the hero's, at his left (our right)
TIEDOWN = [1.15, 1.3, 0.1]                           # the tie, swung up his chest and over his face (for him, hanging, that is down): toon channel `tie` [length, forward, aside]
def bat(z0, dur, y0=None, keys=(), expr='unimpressed', dx=0.0):
    a = [round(BATX + dx, 3), BATY if y0 is None else y0, round(z0 - HEADFWD, 3)]
    return act('ctrl', a, 180, 'batHang', expr, keys=[k(0.0, look=None), k(0.0, to=[a[0], a[1], round(a[2] - V * dur, 3)], dur=dur, clip='batHang', glide=True, ease='linear', face=180, cruise=True), *keys])
st.shot('S14', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z14, V, D14, expr='surprisedHappy', keys=[k(0.0, toon=JOG(face={'brow': 0.4, 'eye': 0.15, 'pupilSize': 1.5, 'cheeks': 0.5}), toonDur=0.0),
                 k(F14 + 0.08, toon=JOG(face={'gx': 0.9, 'brow': 0.9, 'eye': 0.3}), toonDur=0.07), k(F14 + 0.1, expr='neutral'), k(F14 + 0.5, toon=JOG(face={'gx': 0.9, 'brow': 0.9, 'eye': 0.3, 'lid': 1}), toonDur=0.04), k(F14 + 0.58, toon=JOG(face={'gx': 0.9, 'brow': 0.6, 'eye': 0.3}), toonDur=0.04)], blink=0),   # hope still; his eyes go to it; a blink
            act('ctrl', [BATX, BATY + 1.3, round(Z14 - HEADFWD, 3)], 180, 'batHang', 'unimpressed', keys=[k(0.0, look=None),
                 k(0.0, to=[BATX, BATY + 1.3, round(Z14 - V * F14 + 0.4 - HEADFWD, 3)], dur=round(F14 - 0.05, 3), clip='batHang', glide=True, ease='linear', face=180, cruise=True),
                 k(round(F14 - 0.05, 3), to=[BATX, BATY - 0.08, round(Z14 - V * (F14 + 0.07) - HEADFWD, 3)], dur=0.12, glide=True, ease='out', face=180),       # he drops into the frame
                 k(round(F14 + 0.07, 3), to=[BATX, BATY, round(Z14 - V * D14 - HEADFWD, 3)], dur=round(D14 - F14 - 0.07, 3), glide=True, ease='linear', face=180, cruise=True),
                 k(F14 + 0.07, toon={'sq': [1.08, 0.9, 1.08]}, toonDur=0.04), k(F14 + 0.14, toon={'settle': 0.5}, toonDur=0.1, toonEase='outBack'),
                 k(TI14 - 0.08, toon={'tie': TIEDOWN, 'face': {'lid': 0.6}}, toonDur=0.1, toonEase='in'),                                                     # the tie comes down over his face
                 k(FL14 - 0.14, toon={'tie': TIEDOWN, 'hands': {'R': 'open'}, 'touch': {'R': ['face', 0.0, 0.3, 0.12, 1, 0.1]}, 'face': {'lid': 1, 'browL': 0.5}}, toonDur=0.12, toonEase='out'),   # a hand comes to it
                 k(FL14, toon={'hands': {'R': 'open'}, 'touch': {'R': ['face', 0.9, 0.5, 0.25, 1, 0.1]}, 'tie': [1, 0, 0], 'face': {'browL': 0.5}}, toonDur=0.06, toonEase='out'),                # and flicks it away
                 k(FL14 + 0.12, toon={'face': {'gx': -0.8, 'browL': 0.5}}, toonDur=0.1)])],
        props=[HEADSIGN([[0, 'ARRÊT DEMANDÉ']]), BUTTON(-1), UMBT()],
        cams=[cam(0.0, [LANE + 0.6, 1.55, Z14 - 2.85], [LANE + 0.55, 1.55, Z14 - V * D14 - 2.75], [LANE - 0.27, 1.69, Z14 - HEADFWD], [LANE - 0.27, 1.69, Z14 - V * D14 - HEADFWD], lens=44)])
st.cue('sfx:slideDown', 'S14', F14 - 0.05, 0.35); st.cue('sfx:boing', 'S14', F14 + 0.07, 0.3); st.cue('whoosh', 'S14', FL14 - 0.04, 0.25, 0.1, 900, 3000)

# 15: « Au terminus. »: closer, on the face that hangs the wrong way up: he says it to us, the jaw long on each word; the hero's eyes on him, then ahead
D15 = st.dur('S15'); Z15 = round(Z14 - V * D14, 3)
W15 = [round(w['s'] - st.SH['S15'][0], 3) for w in st.L['L09']['words']]
st.shot('S15', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z15, V, D15, expr='neutral', keys=[k(0.0, toon=JOG(face={'gx': 0.9, 'brow': 0.6, 'eye': 0.3}), toonDur=0.0), k(0.7, toon=JOG(face={'brow': 0.9, 'eye': 0.3, 'gy': 0.1}), toonDur=0.1)], blink=0),
            bat(Z15, D15, expr='smug', dx=-0.09, keys=st.talk('L09', 'S15', 'smug') + [k(0.0, toon={'face': {'browL': 0.5}}, toonDur=0.0),
                 *[x for t in W15 for x in (k(max(0.0, t), toon={'face': {'jaw': 0.75, 'browL': 0.8}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.05, toonEase='out'), k(max(0.0, t) + 0.14, toon={'face': {'browL': 0.5}}, toonDur=0.08))],
                 k(0.88, toon={'face': {'lid': 1, 'browL': 0.5}}, toonDur=0.04), k(0.96, toon={'face': {'browL': 0.5}}, toonDur=0.04)])],
        props=[HEADSIGN([[0, 'ARRÊT DEMANDÉ']]), BUTTON(-1), UMBT()],
        cams=[trackcam(Z15, V, 0.0, D15, [LANE + 0.2, 1.55, -3.0], [LANE - 0.21, 1.74, -HEADFWD])])   # far enough for the display on his head to be whole

# 16: there is no terminus. The inspector goes back up out of the frame, the display goes back to 12 BIS, his eyes go up to it; then very close, on his
#     eyes: the pupils, wide with hope, go down to pinpricks; a brow gives, the lower lids come up, a tear
D16 = st.dur('S16'); Z16 = round(Z15 - V * D15, 3); R16 = 0.4   # the cut to the very close shot (0.5 left the tear three frames to roll)
EYES16 = lambda ps, **kw: JOG(face={'pupilSize': ps, 'eye': 0.45, 'brow': 1, **kw}, autoSq=0.0)
st.shot('S16', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[
            act('mec', [LANE, 0, Z16], 180, 'run', 'worried', params={'freq': 4.4, 'bounce': 0.3}, keys=[k(0.0, look=None), k(0.0, to=[LANE, 0, round(Z16 - V * D16, 3)], dur=D16, clip='run', params={'freq': 4.4, 'bounce': 0.3}, cadence=CAD, ease='linear', face=180, cruise=True),
                 k(0.0, toon=JOG(face={'brow': 0.9, 'eye': 0.3, 'pupilSize': 1.5, 'mouth': 'smirk'}, autoSq=0.0), toonDur=0.0),                              # what is left of his smile
                 k(0.23, toon=JOG(face={'gy': -0.75, 'brow': 0.7, 'eye': 0.3, 'pupilSize': 1.5, 'mouth': 'smirk'}, autoSq=0.0), toonDur=0.06),                # his eyes go up: 12 BIS again
                 k(R16 - 0.04, toon=EYES16(1.5, mouth='smirk'), toonDur=0.04),                                                                              # very close: wide pupils, the smile still there: four frames
                 k(R16 + 0.14, toon=EYES16(-0.8, mouth='smirk'), toonDur=0.2, toonEase='inOut'),                                                             # they go down to pinpricks
                 k(R16 + 0.34, toon=EYES16(-0.8, browL=0.3, browR=-0.4, mouth='wavy'), toonDur=0.08),                                                        # and the mouth gives
                 k(R16 + 0.46, toon=EYES16(-0.8, browL=0.0, browR=-0.7, low=0.25, mouth='wavy'), toonDur=0.12),                                              # a brow gives, the lower lids come up
                 k(R16 + 0.58, toon=EYES16(-0.8, browL=0.0, browR=-0.7, low=0.3, mouth='wavy', drop=0.12, dropSize=1.25), toonDur=0.1),                       # a tear wells under the eye nearest us: as tall as the eye
                 k(R16 + 0.7, toon=EYES16(-0.8, browL=0.0, browR=-0.7, low=0.3, mouth='wavy', drop=0.32, dropSize=1.25), toonDur=0.12),                       # and rolls: thirteen frames
                 k(R16 + 0.82, toon=EYES16(-0.8, browL=0.0, browR=-0.7, low=0.3, mouth='wavy', drop=0.52, dropSize=1.25, lid=1), toonDur=0.06), k(R16 + 0.9, toon=EYES16(-0.8, browL=0.0, browR=-0.7, low=0.3, mouth='wavy', drop=0.72, dropSize=1.25), toonDur=0.08),   # a blink on the way
                 k(R16 + 0.98, toon=EYES16(-0.8, browL=0.0, browR=-0.7, low=0.3, mouth='wavy', drop=1.0, dropSize=1.25), toonDur=0.15)], blink=0),
            act('ctrl', [BATX, BATY, round(Z16 - HEADFWD, 3)], 180, 'batHang', 'smug', keys=[k(0.0, look=None), k(0.0, to=[BATX, BATY + 1.4, round(Z16 - V * 0.16 - HEADFWD, 3)], dur=0.16, clip='batHang', glide=True, ease='in', face=180),
                 k(0.16, to=[BATX, BATY + 1.4, round(Z16 - V * D16 - HEADFWD, 3)], dur=round(D16 - 0.16, 3), glide=True, ease='linear', face=180, cruise=True)])],
        props=[HEADSIGN([[0, 'ARRÊT DEMANDÉ'], [0.2, '12 BIS']]), BUTTON(-1), UMBT()],
        cams=[trackcam(Z16, V, 0.0, R16, [LANE + 1.1, 1.62, -2.5], [LANE, 1.82, -HEADFWD]),
              trackcam(Z16, V, R16, D16, [LANE + 0.42, 1.8, -1.42], [LANE + 0.0, 1.84, -HEADFWD], lens=46)])   # his eyes in the upper third, his mouth over the caption band
st.cue('sfx:slideUp', 'S16', 0.0, 0.3); st.cue('sfx:tick', 'S16', 0.2, 0.35); st.cue('sfx:slideDownSlow', 'S16', R16 + 0.14, 0.3)

# 17: yesterday: a traffic light goes to red
D17 = st.dur('S17'); TL = [5.55, 0, -60.0]; RED17 = 0.2
STREETL = {**STREET, 'eiffel': False, 'clear': [-85, 60]}   # at the light: no tree on the right-hand pavement behind the light or behind his head
LIGHT = lambda state, **kw: P('light', 'trafficLight', pos=TL, ry=90, opts={'state': state, 'headRy': -90, 'poleColor': '#98A0A8', 'housing': '#2E4A3B', **kw})   # it bends down the street (-Z); its lenses face up the street
st.shot('S17', 'parisStreet', setOpts=STREETL, props=[LIGHT([[0, 'a'], [RED17, 'r']])],
        cams=[cam(0.0, [6.2, 1.5, TL[2] + 2.6], [6.15, 1.5, TL[2] + 2.45], [TL[0], 2.55, TL[2]], [TL[0], 2.55, TL[2]], lens=44)])
st.cue('clack', 'S17', RED17, 0.45)

# 18: he stops (second staging). From the road, low, three quarters, from down the street: he takes the pole in both hands and goes on: his hands stay
#     and his arms stretch, three metres, the pole bends after him; he runs on the spot at the end of them, eight frames, leaning, his eyes on us; they
#     snap: he flies back past the pole, over the kerb, and lands on the pavement, flat as a pancake: nine frames, a blink on the flat face; he comes
#     back up like an accordion and sees stars. Then close: steam, his eyes, then his head, go up to the red lamp
D18 = st.dur('S18'); G18, FB18, HE18, BK18, FE18, UP18 = 0.14, 0.36, 0.72, 0.82, 1.12, 1.3   # he takes the pole; his arms at full stretch; they snap (the hold: eleven frames); flat on the pavement; he comes up; he is up
CU18 = 1.42                                           # the close shot
PG18 = 1.3                                            # the height of his upper hand on the pole: it bows from its foot to there
PH18 = 2.1                                            # the height of the bending part of the pole
A18 = 0.62                                            # how far it bends
hand18 = lambda a, s_: pole_pt(TL, PH18, a, s_, ry=90, grip=PG18)
X18 = 5.02; GR18 = [X18, 0, TL[2] + 0.35]; IN18 = [LANE + 0.5, 0, round(GR18[2] + V * G18, 3)]   # where he takes the pole; where he comes from
STR18 = [4.9, 0, round(TL[2] - 3.5, 3)]               # where his arms stop him: three and a half metres past the pole
AT18 = [6.5, 0, round(TL[2] + 1.5, 3)]                # where they throw him back, and where he stays: on the pavement, a step up the street from the pole (the display on his head stands clear of the light)
HOLD18 = lambda a, **kw: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [*hand18(a, 1.3), 1, 0.05], 'R': [*hand18(a, 1.12), 1, 0.05]}, **kw}
LEAN18 = {}   # (first staging: a hand left on the pole; he now stands a step from it)
TR18 = [(0.0, 0.0), (0.06, -0.03), (0.12, 0.02), (0.18, -0.05), (0.24, 0.03), (0.3, -0.07), (0.36, 0.03)]   # the hold: (seconds after the full stretch, what the lean of the pole adds): it trembles more and more
BEND18 = [[G18, 0.0], *[[round(FB18 + t, 3), round(A18 + d, 3)] for t, d in TR18], [HE18 + 0.08, -0.16], [HE18 + 0.2, 0.0]]   # the pole: after him, trembling while it holds, back past upright
CAMW18 = [0.88, 0.75, round(TL[2] - 6.37, 3)]; LOOKW18 = [8.44, 1.84, round(TL[2] + 0.09, 3)]   # on the road, low, 46 degrees off his line, on his face side (fitted on his measured joints: display, head, feet at the left, the foot of the pole and the lamp at the right, 7 % of margin): his arms cross 55 % of the width (at 28 degrees, three quarters front, they went away from the lens: 30 %)
CAMW18A = lerp3(CAMW18, [5.3, 1.2, TL[2] - 0.5], 0.3); LOOKW18A = [5.6, 1.45, round(TL[2] - 0.2, 3)]   # it starts closer, on the pole: the frame widens as he goes
CAMB18 = [round(AT18[0] - 2.52, 3), 1.0, round(AT18[2] - 0.95, 3)]; LOOKB18 = [AT18[0], 0.3, AT18[2]]   # where he lands: the flat pose three quarters of the width, seen from a little above
CAMR18 = [round(AT18[0] - 3.4, 3), 1.0, round(AT18[2] - 1.32, 3)]; LOOKR18 = [round(AT18[0] - 0.1, 3), 1.25, round(AT18[2] - 0.15, 3)]   # and back as he comes up: the whole of him, display and feet
CAMC18 = [round(AT18[0] - 0.15, 3), 1.5, round(AT18[2] + 2.6, 3)]; LOOKC18 = [round(AT18[0] - 0.3, 3), 1.95, round(AT18[2] - 0.6, 3)]   # close, from up the street: his face at the right, the red lamp at the left, a gap of house front between it and his display
LAMP18 = [round(AT18[0] - 1.23, 3), 2.57, round(AT18[2] + 1.58, 3)]   # where his head turns in the close shot: up and to the lamp's side of the picture (the lamp itself is behind his shoulder: he would show us the back of his head)
SCRAB = {'freq': 7.0, 'bounce': 0.25}                 # the run of a man held back by his own arms
LEANF = lambda **kw: {'bend': {'spine': [0.62, 0, 0, 1.04, None], 'neck': [-0.45, 0, 0, 1.05, None]}, 'autoSq': 0.1, **kw}
FACE18 = -55
st.shot('S18', 'parisStreet', setOpts=STREETL, look={'fill': 1.35}, actors=[act('mec', IN18, 180, 'run', 'scared', params=RUN, keys=[k(0.0, look=None), k(0.0, to=GR18, dur=G18, clip='run', params=RUN, ease='linear', face=180, cruise='in'),
            k(0.0, toon=JOG(autoSq=0.45, **HOLD18(0.0, face={'gy': -0.6, 'brow': 0.9, 'mouth': 'clench'})), toonDur=0.0),                                        # his arms out ahead of him to the pole
            k(G18, to=STR18, dur=round(FB18 - G18, 3), clip='run', params=SCRAB, then='run', thenParams=SCRAB, ease='out', face=180, blend=0.03),                # he goes on: his hands stay
            k(G18, toon=LEANF(**HOLD18(A18, face={'pop': 0.4, 'jaw': 0.4})), toonDur=round(FB18 - G18, 3), toonEase='out'),                                     # the pole comes after him
            k(FB18 + 0.02, look=CAMW18), k(FB18 + 0.02, expr='worried'),                                                                       # it holds: he runs on the spot, his eyes come to us
            *[k(round(FB18 + TR18[i][0], 3), toon=LEANF(**HOLD18(A18 + TR18[i + 1][1], face={'eye': 0.35 + 0.02 * i, 'brow': 0.9 + 0.02 * i, 'mouth': 'clench' if i < 2 else 'wavy', 'sweat': 1, **({'pupilSize': -0.4} if i > 3 else {})}),
                                                              sq=[1 - 0.012 * i, 1 + 0.02 * i, 1 - 0.012 * i]), toonDur=round(TR18[i + 1][0] - TR18[i][0], 3), toonEase='inOut') for i in range(len(TR18) - 1)],   # eleven frames: the pole trembles more and more, he is pulled longer
            k(HE18, path=[[5.25, 0, round(TL[2] - 0.3, 3)], AT18], dur=round(BK18 - HE18, 3), clip='stand', then='stand', glide=True, ease='in', arc=0.9, face=FACE18, blend=0.04), k(HE18, look=None),   # they snap: back past the pole, over the kerb
            k(HE18, toon=HOLD18(-0.16, sq=[0.75, 0.75, 1.9], auto=0, face={'pop': 0.6, 'jaw': 0.6}), toonDur=0.05, toonEase='in'),   # auto 0 from the snap to the accordion: what is drawn by hand is not remembered by the follow-through
            k(HE18 + 0.06, toon={'sq': [0.75, 0.75, 1.9], 'auto': 0, 'face': {'pop': 0.6, 'jaw': 0.6}}, toonDur=0.02),                                        # his hands let go
            k(BK18 - 0.01, toon={'sq': [1.8, 0.2, 1.8], 'auto': 0, 'face': {'eye': 0.3, 'brow': 0.6, 'mouth': 'clench'}}, toonDur=0.03, toonEase='in'),         # flat on the pavement: nine frames
            k(BK18 + 0.12, toon={'sq': [1.84, 0.19, 1.84], 'auto': 0, 'face': {'lid': 1, 'mouth': 'clench'}}, toonDur=0.04), k(BK18 + 0.2, toon={'sq': [1.8, 0.2, 1.8], 'auto': 0, 'face': {'eye': 0.3, 'brow': 0.6, 'mouth': 'wavy'}}, toonDur=0.04),   # a blink on the flat face
            k(FE18, toon={'sq': [0.88, 1.18, 0.88], 'auto': 0, 'face': {'eye': 0.45, 'brow': 1, 'pupilSize': -0.4}}, toonDur=0.06, toonEase='out'), k(FE18, expr='dizzy'),   # up like an accordion (1.18: at 1.22 the display on his head left the top of the frame)
            k(FE18 + 0.06, toon={'sq': [1.12, 0.82, 1.12], 'auto': 0, 'face': {'stars': 0.9, 'cross': 0.5}}, toonDur=0.05),
            k(FE18 + 0.11, toon={'sq': [0.95, 1.08, 0.95], 'auto': 0, 'face': {'stars': 0.9, 'cross': 0.5}}, toonDur=0.05),
            k(FE18 + 0.16, toon={'settle': 0.6, 'bend': {'neck': [0, 0.14, 0, 1, None]}, 'face': {'stars': 0.9, 'cross': 0.5}}, toonDur=0.06, toonEase='outBack'),   # and he sees stars
            k(UP18 + 0.04, toon={'bend': {'neck': [0, -0.14, 0, 1, None]}, 'face': {'stars': 0.8, 'cross': 0.4, 'lid': 0.5}}, toonDur=0.08),
            k(CU18 - 0.02, face=-20, turn=0.02),                                                                                              # (on the cut: he faces up the street, a little toward the lamp's side)
            k(CU18 - 0.02, toon={'face': {'steam': 1, 'steamInk': 1, 'eye': 0.3, 'brow': 0.8}}, toonDur=0.04), k(CU18 - 0.02, expr='worried'), k(CU18 - 0.02, look=CAMC18),   # close: steam out of his ears
            k(CU18 + 0.14, toon={'face': {'steam': 0.9, 'steamInk': 1, 'gy': -0.85, 'gx': -0.6, 'brow': 0.6, 'eye': 0.2}}, toonDur=0.07), k(CU18 + 0.2, look=LAMP18),                     # his eyes, then his head, go up to the red lamp
            k(CU18 + 0.38, toon={'face': {'steam': 0.6, 'steamInk': 1, 'gy': -0.85, 'gx': -0.6, 'brow': 0.6, 'lid': 1}}, toonDur=0.05), k(CU18 + 0.46, toon={'face': {'steam': 0.4, 'steamInk': 1, 'gy': -0.85, 'gx': -0.6, 'brow': 0.3}}, toonDur=0.05)], blink=0),   # a blink: it is true
        act('ctrl', [IN18[0] - 0.44, BATY + 1.5, IN18[2] - HEADFWD], 180, 'batHang', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[GR18[0] - 0.44, BATY + 1.5, GR18[2] - HEADFWD], dur=G18, clip='batHang', glide=True, ease='linear', face=180, cruise=True),
            k(G18, to=[5.0, 4.7, TL[2] - 7.0], dur=0.5, clip='superman', glide=True, ease='linear', face=180, blend=0.04, cruise=True), k(G18, expr='surprised'), k(CU18 - 0.02, visible=False)])],   # the inspector, who hung over him, goes on, up and out
        props=[LIGHT([[0, 'r']], bend=BEND18, bendGrip=PG18, spring=[[HE18 + 0.2, 0.1, 15, 5]]), HEADSIGN(), BUTTON(-1)],   # (no pedestrian signal here: its box was behind his head when he takes the pole)
        fx=[{'type': 'shake', 'at': BK18, 'dur': 0.18, 'amount': 0.025}],
        cams=[cam(0.0, CAMW18A, CAMW18A, LOOKW18A, LOOKW18A, lens=56),                                    # on the pole until he has it in his hands (moving from the first frame, the frame left him behind at the right edge)
              glide([cam(G18, CAMW18A, CAMW18, LOOKW18A, LOOKW18, lens=56, ease='out')], 0.0),               # then it widens as he goes
              glide([cam(FB18, CAMW18, lerp3(CAMW18, [4.9, 1.5, TL[2] - 3.9], 0.03), LOOKW18, LOOKW18, lens=56)], 0.0),   # the frame has stopped when his arms are at full stretch: the hold is played in a still frame
              cam(round(BK18 - 0.02, 3), CAMB18, lerp3(CAMB18, LOOKB18, 0.06), LOOKB18, LOOKB18, lens=50),   # a cut two frames before he lands: he comes into the frame and goes flat; the camera leans in
              glide([cam(round(BK18 + 0.18, 3), CAMR18, CAMR18, LOOKR18, LOOKR18, lens=50)], 0.14),         # and back with him as he comes up
              cam(CU18, CAMC18, lerp3(CAMC18, [AT18[0], 1.8, AT18[2]], 0.12), LOOKC18, LOOKC18, lens=50)])   # it comes in on him, slowly
st.cue('sfx:stretch', 'S18', G18, 0.45); st.cue('whoosh', 'S18', G18, 0.4, 0.2, 500, 2200); st.cue('sfx:twang', 'S18', HE18, 0.45); st.cue('whoosh', 'S18', HE18, 0.4, 0.1, 900, 3000); st.cue('thud', 'S18', BK18, 0.6)
st.cue('sfx:boing', 'S18', FE18, 0.35); st.cue('sfx:whistle', 'S18', CU18, 0.4)

# 19: not his passengers: from the side again: he stands at the pole and they cross the frame one after the other, still flat in the air; his head goes with them
D19 = st.dur('S19'); V19 = 9.0
def pass19(who, t0, y, dx, ph):                       # one passenger: level with him at t0
    z0 = round(AT18[2] + V19 * t0, 3)
    return act(who, [LANE + dx, y, z0], 180, 'flag', 'scared', params={'phase': ph, 'swing': 0.12}, keys=[k(0.0, look=None), k(0.0, to=[LANE + dx, y, round(z0 - V19 * D19, 3)], dur=D19, clip='flag', params={'phase': ph, 'swing': 0.12}, glide=True, ease='linear', face=180, cruise=True)])
st.shot('S19', 'parisStreet', setOpts=STREETL, look={'fill': 1.35}, actors=[act('mec', AT18, -90, 'stand', 'relieved', blink=0, keys=[k(0.0, look=None), k(0.0, toon={**LEAN18, 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.12, toon={**LEAN18, 'sq': [0.97, 1.05, 0.97], 'face': {'brow': 0.9, 'eye': 0.3}}, toonDur=0.06, toonEase='outBack'), k(0.12, look=[LANE, 1.5, AT18[2] + 2.5], expr='surprised'),   # his head turns up the street: something is coming
            k(0.3, look=[LANE, 1.5, AT18[2] - 1.0]), k(0.55, look=[LANE, 1.5, AT18[2] - 6.0]),                                              # and goes with them, down the street
            k(0.5, toon={**LEAN18, 'face': {'brow': 0.9, 'eye': 0.3, 'lid': 1}}, toonDur=0.04), k(0.57, toon={**LEAN18, 'face': {'brow': 0.9, 'eye': 0.3, 'gx': -0.9}}, toonDur=0.04),   # a blink; his eyes go on, after them (to his right)
            k(0.6, look=[AT18[0] + 1.5, 1.55, AT18[2] - 5.0]),                                                                                 # then his head, as far round as it goes
            k(0.64, face=180, turn=0.14), k(0.76, face=70, turn=0.16),                                                                          # then his shoulders: he turns the way they went, round to us: nine frames (one key to 70 took the short way, in two frames)
            k(0.76, look=[9.8, 1.55, TL[2] + 1.9]), k(0.78, toon={**LEAN18, 'hip': 1.0, 'face': {'brow': 0.7, 'eye': 0.3, 'mouth': 'wavy'}}, toonDur=0.14, toonEase='out')]),   # to us, eyes open: his weight comes down on one leg (his left: toward the middle of the frame)
        pass19('dame', 0.2, 0.45, 0.0, 0.0), pass19('t3', 0.36, 0.7, -0.25, 2.0), pass19('tour', 0.52, 0.3, 0.15, 4.0)],
        props=[LIGHT([[0, 'r']]), HEADSIGN(), BUTTON(-1), P('umb', 'crookUmbrella', on={'actor': 'dame', 'hand': 'R', 'offset': [0, 0.0, 0.0], 'rot': [3.1416, 0, 0]}, opts=CROOK)],
        fx=[{'type': 'wind', 'at': 0.15, 'dur': 0.6, 'v': [0, 0, -11], 'attack': 0.05, 'release': 0.3}],
        cams=[cam(0.0, [9.8, 1.55, TL[2] + 1.9], [9.75, 1.55, TL[2] + 1.9], [5.0, 1.55, TL[2] + 0.9], [5.0, 1.55, TL[2] + 0.9], lens=50)])   # him at the left third, whole, display and all; they cross behind him, between him and the pole
[st.cue('whoosh', 'S19', t, 0.4, 0.25, 500, 2400) for t in (0.2, 0.36, 0.52)]

# 20: they arrive early: at the station, the four of them come down on the bench one after the other; four wrists come up, four pairs of eyes go wide
D20 = st.dur('S20'); ZB = -100.0; BENCH = [9.45, 0, ZB]; W20 = 0.6; E20 = 0.84; U20 = 1.16   # wrists up; the heads snap up to the clock; then to us
CLOCK20 = [10.12, 2.95, ZB - 0.95]
SEATS = {'dame': 0.78, 't3': 0.26, 'tour': -0.26, 'ctrl': -0.78}; LAND = {'dame': 0.04, 't3': 0.13, 'tour': 0.22, 'ctrl': 0.31}
def lands20(who):
    zs = round(ZB + SEATS[who], 3); t0 = LAND[who]; seat = [BENCH[0] + 0.05, 0.02, zs]
    return act(who, [seat[0] - 0.3, 3.6, round(zs + 2.8, 3)], -90, 'sit', 'scared', keys=[k(0.0, look=None), k(0.0, clip='sit'), k(t0, to=seat, dur=0.13, clip='sit', glide=True, ease='in', face=-90), k(t0 + 0.13, clip='sit', blend=0.02),
            k(t0 + 0.13, toon={'sq': [1.25, 0.7, 1.25]}, toonDur=0.03), k(t0 + 0.17, toon={'sq': [0.95, 1.08, 0.95], 'settle': 0.6}, toonDur=0.08, toonEase='outBack'), k(t0 + 0.17, expr='dizzy'), k(t0 + 0.28, toon={}, toonDur=0.08),
            k(W20, clip='sitWatch', blend=0.08), k(W20, expr='neutral'), k(E20 + 0.03 * list(LAND).index(who), look=CLOCK20), k(E20, toon={'sq': [0.96, 1.06, 0.96], 'face': {'eye': 0.4, 'brow': 0.9}}, toonDur=0.08, toonEase='outBack'), k(E20, expr='surprised'),
            k(U20 + 0.05 * list(LAND).index(who), toon={'sq': [0.96, 1.06, 0.96], 'face': {'eye': 0.4, 'brow': 0.9, 'lid': 1}}, toonDur=0.04), k(U20 + 0.05 * list(LAND).index(who) + 0.07, toon={'sq': [0.98, 1.03, 0.98], 'face': {'eye': 0.45, 'brow': 1, 'pupilSize': -0.3}}, toonDur=0.05)])   # they stay on the clock; a blink each, one after the other: their pupils have shrunk
st.shot('S20', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[lands20(w) for w in ('dame', 't3', 'tour', 'ctrl')],
        props=[*[P(f'watch_{w}', 'wristWatch', on={'actor': w, 'hand': 'L', 'offset': [0, 0.075, 0.0], 'rot': [0, 0, 0]}, opts={'s': 2.2, 'dialR': 0.03, 'both': True, 'bright': True}) for w in ('dame', 't3', 'tour', 'ctrl')],
               P('bench', 'bench', pos=BENCH, ry=-90, opts={'w': 2.4}), P('gare', 'stationSign', pos=[10.12, 2.95, ZB + 0.25], ry=-90, opts={'text': 'GARE', 'w': 1.5}), P('clock', 'wallClock', pos=CLOCK20, ry=-90, opts={'rate': 0})],
        fx=[{'type': 'shake', 'at': LAND['dame'] + 0.13, 'dur': 0.45, 'amount': 0.012}],
        cams=[cam(0.0, [3.9, 1.45, ZB], [4.1, 1.45, ZB], [9.45, 1.5, ZB], [9.45, 1.5, ZB], lens=44)])
[st.cue('thud', 'S20', LAND[w] + 0.13, 0.4) for w in LAND]; st.cue('sfx:tick', 'S20', W20, 0.3); st.cue('sfx:gasp', 'S20', E20, 0.3)

# 21: a first: at the red light, seen from up the street (the light above him, red): he has turned round, a hand on the pole; the display on his head turns
#     to HORS SERVICE; he shuts his eyes, breathes in, breathes out
D21 = st.dur('S21'); HS21 = 0.3
HELD21 = {**LEAN18, 'hip': 1.0}                       # as the shot at the pole left him: his weight on his left leg
CAM21 = lambda t, b: cam(t, [5.9, 1.6, TL[2] + 5.1 - b], [5.91, 1.6, TL[2] + 4.95 - b], [6.23, 1.85, TL[2] + 1.25], [6.23, 1.85, TL[2] + 1.25], lens=44)   # he stands on the pavement, a step up the street from the light: a gap of sky between his display and the light
PANT = lambda a, **face: {**HELD21, 'sq': [1 - 0.5 * a, 1 + a, 1 - 0.5 * a], 'face': {'brow': 0.6, **face}}   # a breath: the chest up (a > 0) or down
st.shot('S21', 'parisStreet', setOpts=STREETL, actors=[act('mec', AT18, 0, 'stand', 'neutral', blink=0, keys=[k(0.0, look=None), k(0.0, toon=PANT(-0.02, mouth='o'), toonDur=0.0),
            k(0.0, toon=PANT(0.035, mouth='o'), toonDur=0.06), k(0.06, toon=PANT(-0.025, mouth='o'), toonDur=0.06), k(0.12, toon=PANT(0.035, mouth='o'), toonDur=0.07), k(0.19, toon=PANT(-0.025, mouth='o'), toonDur=0.08),   # he pants, slower and slower
            k(0.27, toon=PANT(0.03, mouth='o', lid=1), toonDur=0.1), k(0.37, toon=PANT(-0.015, mouth='wavy'), toonDur=0.1),                         # a blink
            k(HS21 + 0.16, toon={**HELD21, 'face': {'gy': -0.9, 'brow': 0.7}}, toonDur=0.08),                                           # his eyes go up to the display
            k(HS21 + 0.4, toon={**HELD21, 'sq': [0.97, 1.06, 0.97], 'face': {'lid': 1, 'cheeks': 0.7}}, toonDur=0.14),                     # a breath in
            k(HS21 + 0.62, toon={**HELD21, 'sq': [1.05, 0.93, 1.05], 'settle': 0.4, 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.3, toonEase='out'), k(HS21 + 0.62, expr='relieved')])],   # and out: his shoulders come down
        props=[LIGHT([[0, 'r']]), HEADSIGN([[0, '12 BIS'], [HS21, 'HORS SERVICE']]), BUTTON(-1)],
        cams=[CAM21(0.0, 0.0)])
st.cue('clack', 'S21', HS21, 0.4); st.cue('sfx:slideDownSlow', 'S21', HS21 + 0.62, 0.3)

# 22: and behind him another man comes up the street, heels smoking, who cannot stop: we see him come, he does not (his eyes are shut); the wind of him
#     opens them; his head goes after him, past us, and comes back; a slow blink; the light goes green: a look up at it, back at us: he stays
D22 = st.dur('S22'); P22 = 0.5; V22 = 11.0; PU22, PD22 = 0.8, 0.45; G22 = 1.36   # he passes; the camera comes in (from, for); the light goes green: three frames after the camera has stopped
X22 = 4.3                                            # his path: half a metre from the hero's shoulder
A22 = [X22, 0, round(AT18[2] - V22 * P22, 3)]; M22 = [X22, 0, AT18[2]]; C22 = [X22 - 1.3, 0, round(AT18[2] + V22 * 0.55, 3)]   # from down the street, level with him at P22, then past the camera at its left
BR22 = {'expr': 'scared'}
H22 = HELD21                                          # as the last shot left him: his weight on his left leg
UP22, BK22, NO22 = round(G22 + 0.08, 3), round(G22 + 0.4, 3), round(G22 + 0.5, 3)   # his eyes go up to the green; come back to us; he settles: he stays
st.shot('S22', 'parisStreet', setOpts=STREETL, actors=[act('mec', AT18, 0, 'stand', 'relieved', blink=0, keys=[k(0.0, look=None), k(0.0, toon={**H22, 'sq': [1.01, 0.98, 1.01], 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.02, toon={**H22, 'sq': [0.985, 1.03, 0.985], 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.2, toonEase='inOut'), k(0.24, toon={**H22, 'sq': [1.01, 0.98, 1.01], 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.2, toonEase='inOut'),   # he breathes, slowly, eyes shut
            k(P22 - 0.02, toon={**H22, 'sq': [0.97, 1.05, 0.97], 'face': {'eye': 0.3, 'brow': 0.8, 'gx': -0.8}}, toonDur=0.06, toonEase='outBack'), k(P22 - 0.02, expr='surprised'),   # the wind of him: his eyes open
            k(P22 + 0.08, look=[X22 - 1.2, 1.4, AT18[2] + 5.0]), k(P22 + 0.45, look=None),                                                   # his head goes after him, past us, and comes back
            k(P22 + 0.45, toon={**H22, 'face': {'brow': 0.3}}, toonDur=0.1), k(P22 + 0.45, expr='neutral'),
            k(P22 + 0.55, toon={**H22, 'face': {'lid': 1}}, toonDur=0.05), k(P22 + 0.66, toon={**H22, 'face': {}}, toonDur=0.05),             # to us; a slow blink (the camera is coming in)
            k(UP22, toon={**H22, 'face': {'gy': -0.85, 'gx': -0.7, 'brow': 0.5, 'eye': 0.15}}, toonDur=0.06), k(UP22 + 0.06, look=LAMP18),      # the green light: his eyes go up to it, then his head: eight frames
            k(BK22 - 0.04, toon={**H22, 'face': {'brow': 0.2}}, toonDur=0.06), k(BK22, look=None),                                             # his eyes come back first, then his head: to us
            k(NO22, toon={**LEAN18, 'hip': -1.4, 'sq': [1.03, 0.96, 1.03], 'settle': 0.5, 'face': {'mouth': 'smirk', 'browL': 0.4}}, toonDur=0.24, toonEase='inOut')]),   # no: his weight goes over to the other leg, his shoulders come down: he stays (twelve frames to the end)
        act('mec2', A22, 0, 'heelBrake', 'scared', params=BR22, keys=[k(0.0, look=None), k(0.0, path=[M22, C22], dur=P22 + 0.55, clip='heelBrake', params=BR22, glide=True, ease='linear', face=0, cruise=True),   # one move, two legs: his arms do not start again as he passes
            k(0.0, toon={'face': {'mouth': 'clench', 'brow': 0.9, 'sweat': 1}}, toonDur=0.0)])],
        props=[LIGHT([[0, 'r'], [G22, 'g']]), HEADSIGN([[0, 'HORS SERVICE']]), BUTTON(-1),
               P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A22[0], A22[2] + 0.55], [P22, M22[0], M22[2] + 0.55], [P22 + 0.55, C22[0], C22[2] + 0.55]], 'from': 0.0, 'to': P22 + 0.55, 'every': 0.03, 'marks': True})],
        fx=[{'type': 'wind', 'at': P22 - 0.05, 'dur': 0.4, 'v': [0, 0, 10], 'attack': 0.05, 'release': 0.25}],
        cams=[cam(0.0, [4.4, 1.6, TL[2] + 9.3], [4.4, 1.6, TL[2] + 9.2], [5.7, 1.8, TL[2] + 1.35], [5.7, 1.8, TL[2] + 1.35], lens=44),
              glide([cam(PU22, [5.9, 1.62, TL[2] + 5.1], [5.9, 1.62, TL[2] + 5.1], [6.23, 1.85, TL[2] + 1.25], [6.23, 1.85, TL[2] + 1.25], lens=44)], PD22)])   # wide enough to see him come and pass; then in on the one who stays: the camera has stopped before the light changes
st.cue('sfx:squeak', 'S22', 0.05, 0.4); st.cue('whoosh', 'S22', P22 - 0.3, 0.45, 0.6, 400, 2200); st.cue('clack', 'S22', G22, 0.35)

st.card('S08', 'UNE LIGNE')   # one line of card: its band stops at 18 % of the height, over his head
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("L'élan", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'chauf': {'castShadow': False, 'preset': 'officiel', 'seed': 111, 'suit': '#31557F', 'tie': '#1F2A3D', 'hat': 'copcap', 'hatColor': '#31557F', 'glasses': False, 'facial': 'mustache', 'build': {'width': 0.9, 'headWidth': 1.3}},
    'ctrl': CITIZEN('officiel', 131, suit='#34507A', tie='#F2C230', hat='copcap', hatColor='#34507A', glasses=False, facial='stubble', clothTie=True), 'mec2': CITIZEN('lemec_brown', 133),
    'dame': CITIZEN('madame', 121, suit='#C8553D'), 'tour': CITIZEN('fermier', 123), 't3': CITIZEN('lyceen', 125, suit='#3F7A5A'),
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'p1': {'preset': 'femme', 'seed': 113, 'build': {'width': 0.86, 'headWidth': 1.3}}, 'p2': {'preset': 'lyceen', 'seed': 115, 'build': {'width': 0.86, 'headWidth': 1.3}}, 'p3': {'preset': 'mamie', 'seed': 117, 'build': {'width': 0.86, 'headWidth': 1.3}}})
