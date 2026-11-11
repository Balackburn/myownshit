#!/usr/bin/env python3
"""L'élan (story 41, cycle 5 of the cartoon staging): this man ran to catch his bus. He could not stop. He passed the bus. Then the town. On the
third lap, people got on. The town hall settled it: "It is a line." Since then he comes by every eight minutes. He has a number. He has inspectors.
He asked to get off. He was told: "At the terminus." There is no terminus. Yesterday he finally managed to stop. Not his passengers. They arrived
early. That is a first.
Cartoon rig, cycle 5: follow-through (toon option `follow`), poses that settle (`settle`), props that rock on their carrier (`sway`), pupils that
grow and shrink (`pupilSize`); new clips heelBrake, flag, shoulderRide. Natural look."""
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
def pole_pt(base, h, a, s, ry=0.0, n=14):
    x = y = 0.0; seg = h / n; left = s
    for i in range(n):
        th = a * i / (n - 1) if i else 0.0; d = min(seg, left); x += d * math.sin(th); y += d * math.cos(th); left -= d
        if left <= 0: break
    r = math.radians(ry)
    return r3([base[0] + x * math.cos(r), base[1] + y, base[2] - x * math.sin(r)])

# ---- the street: he runs toward -Z (the tower at the far end). The bus runs in the lane along the right-hand pavement (x > 5), its doors on the pavement side
V = 8.0                                              # his speed, m/s
STREET = {'clear': [-60, 60], 'eiffel': True}
BX, BL = 2.6, 7.6                                    # the bus: the middle of its lane, its length
bus_at = lambda zc, lx, ly, lz: r3([BX + lz, ly, zc - lx])   # a point of the bus (its own frame: +X to its nose, +Z to its doors) in the world, its middle at z = zc
BUS = lambda zc, *keys, **kw: P('bus', 'cityBus', pos=[BX, 0, zc], ry=90, keys=list(keys), opts={'len': BL, 'line': '12', 'dest': 'GARE', **kw})
SEATL = (BL / 2 - 1.05, 0.3, -0.55)                  # the driver's seat, in the bus
RIDERL = [('p1', (BL / 2 - 1.5, 0.44, 0.62), 90), ('p2', (-0.1, 0.44, 0.6), 100), ('p3', (-1.9, 0.44, 0.55), 85)]   # three passengers on the door side: one behind the glass of the front door
STOPPOLE = lambda **kw: P('pole', 'busStopPole', pos=kw.pop('pos'), ry=kw.pop('ry', 90), opts={'line': '12', **kw})

# 1: the hook, seen from inside his bus, through the glass of the front door: he runs beside it and bangs on the glass, three times, a fist bigger each
#    time (stars on the glass, the bus rocks, the passenger at the door jumps); then the bus brakes: he slides out of the doorway, forward, his head turning
#    back to us; the passenger turns to us
X1 = 4.6; Z1 = 30.0                                  # his line, in the road beside the bus; where he is at 0
z1 = lambda t: round(Z1 - V * t, 3)
D1 = st.dur('S01'); BR1 = 1.55                       # the bus brakes
DOORL = BL / 2 - 1.55                                # the front door, in the bus: metres from its middle toward its nose
STOP1 = round(V * (D1 - BR1) / 3, 3)                 # how far the bus still goes: with an 'out' ease over the rest of the shot it starts braking at his speed and stops on the cut
ZCA, ZCB = round(Z1 + DOORL + 0.1, 3), round(z1(BR1) + DOORL + 0.1, 3); ZC2 = round(ZCB - STOP1, 3)   # the middle of the bus: at 0 (the door level with him), when it brakes, where it stops
RUN = {'freq': 4.4}
RUNC = {'freq': 4.4, 'bounce': 0.6, 'sq': 0.05}; CAD = 2.5   # seen close: a slower cadence (a contact every six frames), a smaller bounce, a squash at each contact: the face holds between two strides
SPRINT = lambda **kw: {'bend': {'spine': [0.42, 0, 0, 1.04, None], 'neck': [-0.3, 0, 0, 1.1, None]}, 'autoSq': 0.15, **kw}   # autoSq: at 4.4 strides a second the automatic squash of each footfall lands on one frame in three or four, never the same: seen close, his head drops 40 cm for a frame
SHOUT = {'jaw': 0.6, 'brow': 0.7, 'eye': 0.25}
NOLEGS = {k_: [0, 0, 0, 0.05, 0.3] for k_ in ('legL', 'legR', 'shinL', 'shinR')}   # his own legs shrunk away: the wheel of legs takes their place
WHEELB = {'spine': [0.42, 0, 0, 1.04, None], 'neck': [-0.3, 0, 0, 1.1, None], **NOLEGS}
WHEEL = lambda **kw: P('wheel', 'legWheel', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, -0.02, 0]}, opts=kw)
KT1 = (0.42, 0.78, 1.14)                             # the three knocks
GLASS1 = BX + 1.14                                   # the glass of the door (world x)
def knock1(t, on, face=SHOUT, big=1.0):              # his left fist on the glass of the door (on), or drawn back, at t (the door runs with him)
    tgt = [GLASS1 + 0.06, 1.8, z1(t) + 0.05] if on else [GLASS1 + 0.5, 1.9, z1(t) - 0.1]
    return SPRINT(hands={'L': 'fist'}, scl={'handL': [big, big, big]}, reach={'L': [*tgt, 1, 0.04]}, face=face)
KN1 = [(0.0, 0, 1.0), (KT1[0] - 0.07, 0, 1.0), (KT1[0], 1, 1.3), (KT1[0] + 0.07, 0, 1.0), (KT1[1] - 0.07, 0, 1.0), (KT1[1], 1, 1.45), (KT1[1] + 0.07, 0, 1.0), (KT1[2] - 0.08, 0, 1.0), (KT1[2], 1, 1.75), (KT1[2] + 0.07, 0, 1.0), (BR1 + 0.05, 0, 1.0)]   # (t, on the glass, the size of the fist): each contact is one frame, the recoil two
inbus1 = lambda loc: [k(0.0, to=bus_at(ZCB, *loc), dur=BR1, glide=True, ease='linear', cruise=True), k(BR1, to=bus_at(ZC2, *loc), dur=round(D1 - BR1, 3), glide=True, ease='out')]
CAML1, LOOKL1 = (DOORL - 0.5, 1.72, -0.95), (DOORL + 0.38, 1.52, 1.95)   # the camera, in the bus, against its far side; what it looks at, outside the door
P1L = (DOORL - 0.47, 0.44, 0.88); P1L2 = (DOORL - 0.25, 0.44, 0.88)   # the passenger at the door, over whose shoulder we look: half of her at the edge of the frame; the braking throws her forward, into the frame
st.shot('S01', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, look={'bloom': 0.06}, actors=[act('mec', [X1, 0, Z1], 180, 'run', 'scared', params=RUNC, keys=[*[k(t, look=bus_at(ZCA - V * t, CAML1[0] + 0.3, 1.7, 0.2)) for t in (-0.4, 0.0, 0.4, 0.8, 1.2)],   # his head turned to the door (from before the first frame: his face is to us on the first image of the film)
            k(0.0, to=[X1, 0, z1(D1)], dur=D1, clip='run', params=RUNC, cadence=CAD, ease='linear', face=180, cruise=True),
            k(0.0, toon=knock1(0.0, 0), toonDur=0.0), *[k(KN1[i][0], toon=knock1(KN1[i + 1][0], KN1[i + 1][1], {**SHOUT, 'jaw': 0.95, 'eye': 0.35} if KN1[i + 1][1] else SHOUT, KN1[i + 1][2]), toonDur=round(KN1[i + 1][0] - KN1[i][0], 3), toonEase='in' if KN1[i + 1][1] else 'out') for i in range(len(KN1) - 1)],
            k(BR1 + 0.05, toon=SPRINT(hands={'L': 'spread', 'R': 'spread'}, face={'brow': 1, 'eye': 0.4, 'jaw': 0.45}, sq=[0.97, 1.05, 0.97]), toonDur=0.08, toonEase='outBack'),   # the door is gone from under his fist
            k(BR1 + 0.08, look=bus_at(ZC2, DOORL, 1.7, 0.6))]),                                                                                      # his head turns back to it as he slides out of the doorway
        act('chauf', bus_at(ZCA, *SEATL), 180, 'drive', 'unimpressed', keys=[k(0.0, look=None), *inbus1(SEATL)]),
        act('p1', bus_at(ZCA, *P1L), 180, 'stand', 'surprised', keys=[k(0.0, look='mec'), inbus1(P1L)[0],   # facing the way the bus goes from the first frame (carried along, she turns that way: at 90 she spent the first three frames turning)
            k(BR1, to=bus_at(ZC2, *P1L2), dur=round(D1 - BR1, 3), glide=True, ease='out'), *[x for i, t in enumerate(KT1) for x in (k(t, toon={'sq': [1 + 0.05 * (i + 1), 1 - 0.07 * (i + 1), 1 + 0.05 * (i + 1)]}, toonDur=0.03), k(t + 0.05, toon={'settle': 0.6}, toonDur=0.1))],   # she jumps with the glass
            k(BR1 + 0.12, look=bus_at(ZC2, *CAML1)), k(BR1 + 0.12, expr='unimpressed')])],                                                             # then turns to us
        props=[BUS(ZCA, k(0.0, to=[BX, 0, ZCB], dur=BR1, ease='linear'), k(BR1, to=[BX, 0, ZC2], dur=round(D1 - BR1, 3), ease='out'), rock=[[KT1[0], 0.012], [KT1[1], 0.018], [KT1[2], 0.03], [BR1, 0.02]], doorGlass=0.08),
               *[P(f'kn{i}', 'impactStars', pos=[GLASS1 - 0.03, 1.8, z1(t) + 0.05], ry=90, opts={'at': t, 'n': 4 + i, 'r': 0.24 + 0.07 * i, 'r0': 0.09, 'dur': 0.24, 'size': 0.065 + 0.012 * i}, keys=[k(t, to=[GLASS1 - 0.03, 1.8, z1(t + 0.3) + 0.05], dur=0.3, ease='linear')]) for i, t in enumerate(KT1)]],   # stars on the glass at each knock, bigger each time
        cams=[cam(0.0, bus_at(ZCA, *CAML1), bus_at(ZCB, *CAML1), bus_at(ZCA, *LOOKL1), bus_at(ZCB, *LOOKL1), lens=55),
              cam(BR1, bus_at(ZCB, *CAML1), bus_at(ZC2, *CAML1), bus_at(ZCB, *LOOKL1), bus_at(ZC2, *LOOKL1), lens=55, ease='out')])   # the camera rides in the bus: it brakes with it
st.cue('engine', 'S01', 0.0, 0.22, BR1 + 0.25); st.cue('whoosh', 'S01', 0.0, 0.25, 0.5, 500, 1800); [st.cue('thud', 'S01', t, 0.4 + 0.08 * i) for i, t in enumerate(KT1)]; st.cue('sfx:squeak', 'S01', BR1, 0.5)

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
D3 = st.dur('S03'); W3 = 0.66                         # the whip
DRV3 = bus_at(ZC2, *SEATL)
st.shot('S03', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[
        act('chauf', DRV3, 180, 'drive', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gx': -0.9}}, toonDur=0.0), k(0.08, look=[6.5, 1.5, DRV3[2] - 0.8]), k(0.3, toon={'face': {'gx': -0.9, 'lid': 1}}, toonDur=0.04), k(0.38, toon={'face': {}}, toonDur=0.04),
               k(0.4, look=None), k(W3 - 0.1, toon={'sq': [1.06, 0.9, 1.06], 'face': {'lid': 0.6}}, toonDur=0.08),
               k(W3, look=[4.7, 1.3, DRV3[2] - 10.0], expr='surprised'), k(W3, toon={'scl': {'head': [1.5, 0.84, 1]}, 'sq': [0.95, 1.1, 0.95], 'hat': [0.04, 0, 3.1], 'face': {'pop': 0.7, 'jaw': 0.45}}, toonDur=0.06, toonEase='out'),
               k(W3 + 0.08, toon={'bend': {'neck': [0, 0, 0, 1.25, None]}, 'hat': [0.1, 0, 9.4], 'face': {'pop': 0.7, 'jaw': 0.45}}, toonDur=0.1, toonEase='outBack'),
               k(W3 + 0.3, toon={'bend': {'neck': [0, 0, 0, 1.15, None]}, 'hat': [0, 0, 12.566 + 3.1416], 'face': {'pop': 0.6, 'jaw': 0.4}}, toonDur=0.22, toonEase='out')]),   # the cap ends back to front
        *[act(n, bus_at(ZC2, *loc), ry, 'stand', 'surprised', keys=[k(0.0, look=[4.7, 1.3, DRV3[2] - 10.0])]) for n, loc, ry in RIDERL[:1]]],
        props=[BUS(ZC2, line=' ', dest=' ')],
        look={'fill': 1.7},
        cams=[cam(0.0, [2.6, 1.55, DRV3[2] - 2.35], [2.57, 1.55, DRV3[2] - 2.28], [2.1, 1.64, DRV3[2]], [2.1, 1.64, DRV3[2]], lens=44)])
st.cue('whoosh', 'S03', 0.0, 0.4, 0.3, 600, 2000); st.cue('sfx:boing', 'S03', W3, 0.4); st.cue('sfx:spring', 'S03', W3 + 0.08, 0.3)

# 4: the sign at the edge of town: he goes by it, still braking; it spins on its post
D4 = st.dur('S04'); V4 = 14.0; P4 = 0.35              # he passes the sign
A4 = [1.1, 0, round(V4 * P4, 3)]; B4 = [1.1, 0, round(V4 * (P4 - D4), 3)]
st.shot('S04', 'grassland', setOpts={'sky': ['#01ABF1', '#CFE7F1']}, look={'deepSky': False}, actors=[act('mec', A4, 180, 'heelBrake', 'worried', keys=[k(0.0, look=None), k(0.0, to=B4, dur=D4, clip='heelBrake', glide=True, ease='linear', face=180, cruise=True),
            k(0.0, toon={'face': {'gx': -0.8, 'gy': -0.4, 'brow': 0.8}}, toonDur=0.0), k(P4 + 0.1, toon={'face': {'brow': 1, 'mouth': 'wavy'}}, toonDur=0.08)])],
        props=[P('road', 'roadStrip', pos=[-1.3, 0, 0], opts={'len': 500, 'w': 6.5}), P('sign', 'townSign', pos=[2.45, 0, 0], ry=-118, opts={'name': 'PARIS', 'spinAt': P4 + 0.03, 'turns': 2.07, 'spinDur': 0.72}),
               P('tower', 'eiffelTower', pos=[-32, 0, 190], opts={'h': 60}),
               P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A4[0], A4[2] - 0.55], [D4, B4[0], B4[2] - 0.55]], 'from': 0.0, 'to': D4, 'every': 0.025, 'marks': True, 'marksY': 0.08})],
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

# 6: he comes through. Seen from the road: she winds up and brings the crook down on his collar. Three accents: the hook, held four frames (his feet
#    go on without him, his neck stays, her arms stretch, the shaft quivers); they leave one after the other, three frames apart, an arm stretching before the
#    feet leave the kerb; then the empty kerb: the lap board hangs in the air eight frames and drops
D6 = st.dur('S06'); V6 = 10.0; H6 = 0.42; R6 = H6 + 0.14; V6B = 11.0   # the hook; the release; their speed once they are a train
HOOK6 = [LANE, 1.3, 0.15]                             # his collar at the hook
YANK6 = [LANE, 0.13, round(HOOK6[2] - 0.48, 3)]       # where his hips are while he hangs by the collar, feet first
zh6 = lambda t: round(YANK6[2] - V6B * (t - R6), 3)   # his z once he is off again
def leave6(who, pos0, t0, arm, hold):                 # one of the three: the arm that holds the one in front stretches (2 frames), then the feet leave the kerb
    tgt = lambda t: [LANE + OFFX6[who], FLY6[who], round(zh6(t) + GAP6[who], 3)]
    return [k(t0 - 0.07, toon={**hold, 'reach': {**hold.get('reach', {}), arm[0]: [*arm[1], 1, 0.06]}, 'sq': [1.05, 0.95, 1.05], 'face': {'eye': 0.35, 'brow': 0.9, 'jaw': 0.3}}, toonDur=0.07, toonEase='out'), k(t0 - 0.07, expr='scared'),
            k(t0, to=tgt(t0 + 0.1), dur=0.1, glide=True, clip='flag', params={'phase': PH6[who], 'swing': 0.2}, ease='in', face=180, blend=0.03),
            k(t0, toon={'sq': [0.8, 0.8, 1.7]}, toonDur=0.04), k(t0 + 0.08, toon={}, toonDur=0.08),                              # a smear as the feet leave
            k(t0 + 0.1, to=tgt(D6), dur=round(D6 - t0 - 0.1, 3), glide=True, clip='flag', params={'phase': PH6[who], 'swing': 0.2}, ease='linear', face=180, blend=0, cruise=True)]
GAP6 = {'dame': 1.95, 't3': 3.3, 'tour': 4.65}; OFFX6 = {'dame': 0.12, 't3': -0.1, 'tour': 0.15}; FLY6 = {'dame': 0.3, 't3': 0.45, 'tour': 0.25}; PH6 = {'dame': 0.0, 't3': 2.0, 'tour': 4.0}
GACK6 = {'lid': 1, 'tongue': 1, 'tongueLen': 0.16, 'jaw': 0.7, 'brow': 0.9, 'cheeks': 0.7}
st.shot('S06', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[
        act('mec', [LANE, 0, round(HOOK6[2] + V6 * H6, 3)], 180, 'run', 'worried', params=RUN, keys=[k(0.0, look=None),
            k(0.0, to=[LANE, 0, HOOK6[2]], dur=H6, clip='run', params=RUN, ease='linear', face=180, cruise=True), k(0.0, toon=SPRINT(autoSq=0.2, face={'brow': 0.6}), toonDur=0.0),
            k(H6, to=YANK6, dur=0.07, glide=True, clip='flag', params={'dir': -1, 'droop': 0.25, 'swing': 0.0, 'flutter': 0.9, 'arms': 1.0, 'expr': 'scared'}, then='flag', ease='out', face=180, blend=0.04),   # the hook: his feet go on without him
            k(H6, toon={'bend': {'neck': [-0.2, 0, 0, 1.9, None], 'spine': [0, 0, 0, 1.22, None]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': GACK6, 'auto': 0.3}, toonDur=0.05, toonEase='out'), k(H6, expr='scared'),
            k(H6 + 0.07, toon={'bend': {'neck': [-0.25, 0, 0, 2.2, None], 'spine': [0, 0, 0, 1.3, None]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': GACK6, 'auto': 0.3}, toonDur=0.07),    # held: he goes on stretching
            k(R6, to=[LANE, 0, zh6(D6)], dur=round(D6 - R6, 3), clip='run', params=RUN, ease='linear', face=180, blend=0.07, cruise=True),                                          # off again, with a train
            k(R6, toon=SPRINT(autoSq=0.45, sq=[0.9, 0.95, 1.25], face={'eye': 0.4, 'pupilSize': -0.4, 'brow': 1, 'mouth': 'wavy'}), toonDur=0.06, toonEase='out'), k(R6 + 0.12, toon=SPRINT(autoSq=0.45, face={'eye': 0.3, 'brow': 1, 'mouth': 'wavy', 'gx': -0.8}), toonDur=0.1)]),
        act('dame', LADY5, -50, 'stand', 'determined', keys=[k(0.0, look=[LANE, 1.5, 5.0]), k(0.0, toon={**LADYHOLD, 'bend': {'spine': [-0.1, 0.2, 0.25, 1, None]}, 'face': {'brow': -0.5}}, toonDur=0.0),
            k(0.1, toon={**LADYH(0.34), 'bend': {'spine': [-0.2, 0.2, 0.3, 1.08, None]}, 'sq': [0.95, 1.1, 0.95], 'face': {'brow': -0.7, 'eye': 0.2}}, toonDur=0.16, toonEase='out'),                       # she winds up: the crook goes up over their heads
            k(H6 - 0.1, toon={**LADYHOLD, 'bend': {'spine': [0.35, -0.2, -0.3, 1.05, None]}, 'sq': [1.06, 0.92, 1.06], 'face': {'brow': -0.9, 'mouth': 'clench'}}, toonDur=0.1, toonEase='in'), k(H6 - 0.1, look=HOOK6),   # and comes down
            k(H6 + 0.02, toon={**LADYHOLD, 'bend': {'spine': [-0.3, 0, 0, 1.1, None], 'armL': [0, 0, 0, 1.35, None], 'armR': [0, 0, 0, 1.35, None]}, 'sq': [0.95, 1.06, 0.95], 'face': {'eye': 0.3, 'brow': 0.8, 'mouth': 'clench'}}, toonDur=0.06, toonEase='out'),   # she holds on: heels on the kerb, arms out of their sleeves
            *leave6('dame', LADY5, R6, ('R', [LANE + 0.3, 1.32, -0.5]), {'hands': {'L': 'grip', 'R': 'grip'}})]),
        act('t3', T35, 0, 'stand', 'scared', keys=[k(0.0, look=[LANE, 1.5, 5.0]), k(0.0, toon=T3HOLD, toonDur=0.0), k(H6, look=HOOK6), k(H6, toon={**T3HOLD, 'sq': [1.05, 0.94, 1.05], 'face': {'eye': 0.3, 'brow': 0.9}}, toonDur=0.08),
            *leave6('t3', T35, R6 + 0.1, ('L', [LANE + 0.5, 1.3, 0.3]), T3HOLD)]),
        act('tour', TOUR5, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[LANE, 1.5, 5.0]), k(0.0, toon=TOURHOLD(), toonDur=0.0), k(H6 + 0.06, look=HOOK6), k(H6 + 0.06, toon={**TOURHOLD(), 'face': {'browL': 0.7, 'eye': 0.2}}, toonDur=0.08),
            *leave6('tour', TOUR5, R6 + 0.2, ('R', [LANE + 0.45, 1.3, 0.9]), {'hands': {'L': 'open', 'R': 'grip'}})])],
        props=[UMB(-0.12, k(0.1, to=[HB5[0], HB5[1] + 0.34, HB5[2]], dur=0.16, ease='out'), k(0.1, rotTo=[0, 0, -0.22], dur=0.16, ease='out'), k(H6 - 0.1, to=HB5, dur=0.1, ease='in'), k(H6 - 0.1, rotTo=[0, 0, 1.5], dur=0.1, ease='in'), k(R6, attach='mec', joint='torso', offset=[0, 0.58, -1.38], rot=[1.5708, 0, 0]), shake=[[H6, 0.07], [H6 + 0.07, 0.05]]),
               P('board', 'lapBoard', pos=BOARD5, opts={'flips': [[0, '3']], 'w': 0.5}, keys=[k(R6 + 0.2, rotTo=[0, 3.5, 0.12], dur=0.1, ease='out'), k(R6 + 0.3, rotTo=[0, 3.5, -0.1], dur=0.09), k(R6 + 0.39, rotTo=[0, 3.5, 0.05], dur=0.08), k(R6 + 0.48, rotTo=[0, 3.5, -0.03], dur=0.1),   # left in the air: his hand spins it round to us; it hangs, rocking, eight frames
                    k(R6 + 0.6, to=[BOARD5[0] - 0.05, 0.03, BOARD5[2] - 0.1], dur=0.17, ease='in'), k(R6 + 0.6, rotTo=[0.3, 4.4, 1.45], dur=0.17, ease='in'),                                                       # and drops
                    k(R6 + 0.77, to=[BOARD5[0] - 0.08, 0.1, BOARD5[2] - 0.12], dur=0.05, ease='out'), k(R6 + 0.82, to=[BOARD5[0] - 0.1, 0.03, BOARD5[2] - 0.13], dur=0.06, ease='in')])],
        fx=[{'type': 'wind', 'at': R6 - 0.04, 'dur': 0.5, 'v': [0, 0, -12], 'attack': 0.05, 'release': 0.3}, {'type': 'shake', 'at': H6, 'dur': 0.12, 'amount': 0.015}],
        cams=[cam(0.0, [1.2, 1.1, -4.6], [1.25, 1.1, -4.5], [4.9, 1.5, 0.6], [4.9, 1.5, 0.6], lens=50),
              glide([cam(R6 + 0.3, [1.9, 1.15, -3.4], [1.95, 1.15, -3.3], [5.45, 1.25, 1.6], [5.45, 1.25, 1.6], lens=50)], 0.3)])   # then on to the board left in the air
st.cue('whoosh', 'S06', 0.08, 0.45, 0.4, 400, 2400); st.cue('whoosh', 'S06', H6 - 0.12, 0.35, 0.12, 900, 3000); st.cue('sfx:twang', 'S06', H6, 0.45); st.cue('sfx:stretch', 'S06', H6 + 0.02, 0.4)
st.cue('sfx:boing', 'S06', R6, 0.4); [st.cue('whoosh', 'S06', R6 + d, 0.3, 0.2, 600, 2200) for d in (0.0, 0.1, 0.2)]; st.cue('clack', 'S06', R6 + 0.77, 0.4)

# 7: the mayor settles it: his hand goes up like a blade, holds, comes down: the desk is cut in two
D7 = st.dur('S07'); C7 = 0.62                         # the blow
MAY7 = [0.0, 0, -1.62]; DESK7 = [0.0, 0, -0.9]
OFFICE = {'desk': False, 'map': False, 'plant': False}
UP7 = lambda dy=0.0: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [0.02, 2.74 + dy, -1.5, 1, 0.08, [1, 0.3, 0.4]], 'R': [-0.02, 2.74 + dy, -1.5, 1, 0.08, [-1, 0.3, 0.4]]}}   # both hands joined into one block over his head, elbows out: an axe
DOWN7 = lambda y: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [0.02, y, -0.98, 1, 0.08], 'R': [-0.02, y, -0.98, 1, 0.08]}}
DUST7 = lambda a: {'hands': {'L': 'open', 'R': 'open'}, 'reach': {'L': [0.06, 1.18 + 0.07 * a, -1.3, 1, 0.06], 'R': [-0.06, 1.18 - 0.07 * a, -1.3, 1, 0.06]}}   # he dusts his hands: one palm goes down the other
jump7 = lambda pid, name, pos, opts, dy, dx: P(pid, name, pos=pos, opts=opts, keys=[k(C7, to=[pos[0] + dx * 0.5, pos[1] + dy, pos[2]], dur=0.12, ease='out'), k(C7 + 0.12, to=[pos[0] + dx, pos[1] - 0.3, pos[2] + 0.05], dur=0.2, ease='in'), k(C7, rotTo=[0.3, 0.6, dx * 3], dur=0.32)])
st.shot('S07', 'mairie', setOpts=OFFICE, actors=[act('maire', MAY7, 0, 'stand', 'determined', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gy': 0.5}}, toonDur=0.0),
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
        cams=[cam(0.0, [0.35, 1.9, 2.3], [0.3, 1.9, 2.15], [0.0, 1.22, -1.2], [0.0, 1.22, -1.2], lens=60)])   # from higher, looking down: the desk at two thirds of the height, over the captions; his hands against the bare wall
st.cue('sfx:slideUp', 'S07', 0.05, 0.3); st.cue('whoosh', 'S07', C7 - 0.08, 0.4, 0.1, 700, 2600); st.cue('thud', 'S07', C7, 0.7); st.cue('clack', 'S07', C7 + 0.02, 0.5); st.cue('sfx:boing', 'S07', C7 + 0.26, 0.25); [st.cue('pop', 'S07', C7 + d, 0.2) for d in (0.44, 0.54, 0.64)]

# 8: « C'est une ligne. »: he says it, the map of the line in his hand: a loop, and on it a little head that goes round
D8 = st.dur('S08'); MAP8 = [0.61, 1.06, -1.2]; TAP8 = 0.52
st.shot('S08', 'mairie', setOpts={**OFFICE, 'banner': False}, actors=[act('maire', MAY7, 0, 'stand', 'smug', keys=st.talk('L05', 'S08', 'smug') + [k(0.0, look=None),
            k(0.0, toon={'hands': {'L': 'grip', 'R': 'point'}, 'reach': {'L': [MAP8[0] + 0.3, MAP8[1] + 0.5, MAP8[2] - 0.03, 1, 0.05], 'R': [MAP8[0] - 0.14, MAP8[1] + 0.36, MAP8[2] + 0.06, 1, 0.12]}, 'face': {'browL': 0.5}}, toonDur=0.0),
            k(TAP8 - 0.12, toon={'hands': {'L': 'grip', 'R': 'point'}, 'reach': {'L': [MAP8[0] + 0.3, MAP8[1] + 0.5, MAP8[2] - 0.03, 1, 0.05], 'R': [MAP8[0] - 0.2, MAP8[1] + 0.4, MAP8[2] + 0.2, 1, 0.12]}, 'face': {'brow': 0.6}}, toonDur=0.1, toonEase='out'),   # the finger draws back
            k(TAP8 - 0.02, toon={'hands': {'L': 'grip', 'R': 'point'}, 'scl': {'handR': [1.25, 1.25, 1.25]}, 'reach': {'L': [MAP8[0] + 0.3, MAP8[1] + 0.5, MAP8[2] - 0.03, 1, 0.05], 'R': [MAP8[0] - 0.02, MAP8[1] + 0.3, MAP8[2] + 0.03, 1, 0.12]}, 'bend': {'spine': [0.08, -0.05, 0, 1, None]}, 'face': {'brow': 0.7}}, toonDur=0.04, toonEase='in'),   # and taps the loop
            k(TAP8 + 0.06, toon={'hands': {'L': 'grip', 'R': 'point'}, 'reach': {'L': [MAP8[0] + 0.3, MAP8[1] + 0.5, MAP8[2] - 0.03, 1, 0.05], 'R': [MAP8[0] - 0.06, MAP8[1] + 0.32, MAP8[2] + 0.08, 1, 0.12]}, 'settle': 0.4, 'bend': {'spine': [0.06, -0.05, 0, 1, None]}, 'face': {'brow': 0.6}}, toonDur=0.1, toonEase='outBack')])],
        props=[P('desk', 'splitDesk', pos=DESK7, opts={'at': -1, 'w': 1.7}), P('map', 'lineMap', pos=MAP8, ry=-8, opts={'title': 'LIGNE 12 BIS', 'lap': 0.9}, keys=[k(TAP8, rotTo=[0.06, -0.14, 0], dur=0.04), k(TAP8 + 0.04, rotTo=[0, -0.14, 0], dur=0.12, ease='outBack')])],
        cams=[cam(0.0, [0.83, 1.62, 1.5], [0.8, 1.62, 1.38], [0.3, 1.72, -1.4], [0.3, 1.72, -1.4], lens=44)])   # the whole map in the frame, its loop over the caption band

# 9: the display of the stop: 1 MIN, 0 MIN; the pigeon on it looks up the street
D9 = st.dur('S09'); DISP = [5.6, 0, 1.2]; PIG = [DISP[0], 2.6 + 0.24, DISP[2]]
DISPLAY = lambda texts, **kw: P('disp', 'busDisplay', pos=DISP, ry=90, opts={'line': '12 BIS', 'texts': texts, **kw})
st.shot('S09', 'parisStreet', setOpts={**STREET, 'eiffel': False}, props=[DISPLAY([[0, '1 MIN'], [0.33, '0 MIN']]),
               P('pig', 'pigeon', pos=PIG, ry=90, keys=[k(0.12, rotTo=[0, math.radians(20), 0], dur=0.1, ease='outBack')])],
        cams=[cam(0.0, [7.95, 1.95, 1.8], [7.85, 1.97, 1.75], [5.62, 2.56, 1.21], [5.62, 2.56, 1.21], lens=44)])
st.cue('sfx:tick', 'S09', 0.33, 0.5)

# ---- the line: he runs along the lane, the three passengers fly behind him like a kite's tail (the lady hooked to his collar by her umbrella)
GAP = {'dame': 1.95, 't3': 3.3, 'tour': 4.65}; OFFX = {'dame': 0.12, 't3': -0.1, 'tour': 0.15}; FLY = {'dame': 0.3, 't3': 0.45, 'tour': 0.25}; PH = {'dame': 0.0, 't3': 2.0, 'tour': 4.0}
HEADSIGN = lambda texts=None, **kw: P('hs', 'headSign', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.56, 0.0], 'sway': 1}, opts={'texts': texts or [[0, '12 BIS']], 'w': 0.55, 'hh': 0.16, **kw})
COLLAR = {'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.58, -1.38], 'rot': [1.5708, 0, 0]}   # the grip 1.25 m behind his collar, the crook on it
HEADFWD, HEADDROP = 0.45, 0.3                        # running, his head is that far ahead of his feet and that much lower than standing: aim close cameras there
def rider(who, z0, v, dur, expr='scared', keys=(), **par):        # one passenger of the tail: z0 is the hero's z at 0
    a = [LANE + OFFX[who], FLY[who], round(z0 + GAP[who], 3)]; b = [a[0], a[1], round(a[2] - v * dur, 3)]; pr = {'phase': PH[who], 'swing': 0.16, **par}
    return act(who, a, 180, 'flag', expr, params=pr, keys=[k(0.0, look=None), k(0.0, to=b, dur=dur, clip='flag', params=pr, glide=True, ease='linear', face=180, cruise=True), *keys])
def runner(z0, v, dur, expr='unimpressed', keys=(), x=None, close=True, **opt):       # the hero (close: the run of a close-up: slow cadence, small bounce)
    x = LANE if x is None else x; par = RUNC if close else RUN; cad = {'cadence': CAD} if close else {}
    return act('mec', [x, 0, z0], 180, 'run', expr, params=par, keys=[k(0.0, look=None), k(0.0, to=[x, 0, round(z0 - v * dur, 3)], dur=dur, clip='run', params=par, ease='linear', face=180, cruise=True, **cad), *keys], **opt)
TAIL = lambda z0, v, dur, **kw: [rider(w, z0, v, dur, **kw) for w in ('dame', 't3', 'tour')]
UMBT = lambda: P('umb', 'crookUmbrella', on=COLLAR, opts=CROOK)
JOG = SPRINT   # his toon base while running
closeup = lambda z0, v, dur, side=1.2, back=2.75, h=1.6, dy=0.0, push=0.12: [cam(0.0, [LANE + side, h, z0 - back], [LANE + side - push, h, z0 - v * dur - back + push], [LANE, 1.72 + dy, z0 - HEADFWD], [LANE, 1.72 + dy, z0 - v * dur - HEADFWD], lens=44)]   # the camera running backward in front of him, on his head

# 10: he comes through the stop with his passengers: 0 MIN; the display goes back to 8 MIN, the pole of the stop bends after him and rings, the pigeon is gone
D10 = st.dur('S10'); P10 = 0.3; V10 = 10.0            # he is level with the pole
z10 = round(1.5 + V10 * P10, 3)
POLE10 = [5.45, 0, -0.15]
st.shot('S10', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[runner(z10, V10, D10, close=False, keys=[k(0.0, toon=SPRINT(autoSq=0.2, bend=WHEELB), toonDur=0.0)]), *TAIL(z10, V10, D10)],
        props=[WHEEL(), DISPLAY([[0, '0 MIN'], [P10 + 0.22, '8 MIN']]), STOPPOLE(pos=POLE10, bend=[[P10 - 0.02, 0], [P10 + 0.12, 0.55]], spring=[[P10 + 0.12, 0.55, 14, 3.4]]), HEADSIGN(), UMBT(),
               P('pig', 'pigeon', pos=PIG, ry=110, keys=[k(P10 + 0.02, to=[PIG[0] - 0.3, PIG[1] + 0.9, PIG[2] - 2.6], dur=0.3, ease='out'), k(P10 + 0.02, rotTo=[0.8, 3.0, 2.2], dur=0.3), k(P10 + 0.32, to=[PIG[0] - 0.6, PIG[1] + 1.6, PIG[2] - 7.0], dur=0.5, ease='linear')]),
               *[P(f'feather{i}', 'feather', pos=[PIG[0] + dx, PIG[1] + 0.25 + dy, PIG[2] - 0.15 + dz], ry=90, opts={'at': P10 + 0.1 + 0.05 * i, 'dur': D10 - P10 - 0.1 - 0.05 * i + 0.3 * (i > 0), 'fall': fl, 'sway': sw, 'swings': n, 's': sz}) for i, (dx, dy, dz, fl, sw, n, sz) in enumerate([(0, 0, 0, 1.3, 0.3, 2.2, 2.6), (0.05, 0.2, -0.45, 1.2, 0.24, 2.6, 2.0), (-0.05, 0.1, 0.4, 1.5, 0.36, 1.8, 2.3)])]],   # what is left of the pigeon: a feather comes down through the empty end of the shot
        fx=[{'type': 'wind', 'at': P10 - 0.08, 'dur': 0.7, 'v': [0, 0, -12], 'attack': 0.05, 'release': 0.3}],
        cams=[cam(0.0, [8.6, 1.55, -1.9], [8.5, 1.55, -1.8], [5.5, 1.8, 0.5], [5.5, 1.8, 0.5], lens=44)])
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

# 12: his inspectors. Seen from below, beside the lane (the hero is out of the frame at our right): the inspector surfs on the back of the lady, three
#     quarters to us, his head against the sky; a passenger's arm comes forward, long, with one ticket, up into the sky; an oversized punch: clack; one
#     confetti leaves in the wind; he nods
D12 = st.dur('S12'); Z12 = 12.0; T12 = 0.2; PU12 = 0.64
SURF = [LANE + OFFX['dame'], FLY['dame'] + 1.05 + 0.1, round(Z12 + GAP['dame'] - 0.3, 3)]       # the inspector's feet: on the lady's back
TK12 = [LANE + 0.72, 2.32, round(Z12 + 1.15, 3)]                                               # the ticket, held up in front of the inspector, in the sky
mv12 = lambda p_, t: [p_[0], p_[1], round(p_[2] - V * t, 3)]                                    # a point that travels with them
ARM12 = lambda t, dy=0.0: {'hands': {'L': 'pinch', 'R': 'grip'}, 'reach': {'L': [TK12[0] + 0.04, TK12[1] - 0.16 + dy, mv12(TK12, t)[2] + 0.03, 1, 0.05]}}
_a12 = math.radians(160)                                                                          # the ticket is turned 160 degrees: its face to the camera
N12, DJ12 = (math.sin(_a12), 0.0, math.cos(_a12)), (-math.cos(_a12), 0.0, math.sin(_a12))       # the ticket's face; the way the jaws point: along the ticket, away from the inspector (screen left)
HOLE12 = [TK12[0] + 0.168 * math.cos(_a12), TK12[1] + 0.027, TK12[2] - 0.168 * math.sin(_a12)]  # where the hole is punched (bigTicket: 0.3 w from its middle)
_c12, _s12 = math.cos(math.radians(50)), math.sin(math.radians(50))                              # rolled 50 degrees about its length: both jaws show
_X12 = (N12[0] * _c12, _s12, N12[2] * _c12); _Z12 = (_X12[1] * DJ12[2] - _X12[2] * DJ12[1], _X12[2] * DJ12[0] - _X12[0] * DJ12[2], _X12[0] * DJ12[1] - _X12[1] * DJ12[0])
PROT12 = (round(math.atan2(-_Z12[1], _Z12[2]), 4), round(math.degrees(math.asin(max(-1.0, min(1.0, _Z12[0])))), 2), round(math.atan2(-DJ12[0], _X12[0]), 4))   # that frame as rot x, ry (deg), rot z (jaws = +Y)
pv12 = lambda back, dy=0.0: [round(HOLE12[0] - (0.26 + back) * DJ12[0], 3), round(HOLE12[1] + dy, 3), round(HOLE12[2] - (0.26 + back) * DJ12[2], 3)]   # the pivot of the punch, `back` metres short of the bite
REST12, READY12, BITE12, BACK12 = pv12(0.34, -0.3), pv12(0.13), pv12(0.0), pv12(0.26, -0.06)
PK12 = [(0.0, REST12), (T12 + 0.1, REST12), (PU12 - 0.1, READY12), (PU12, BITE12), (PU12 + 0.1, BITE12), (round(PU12 + 0.22, 3), BACK12), (D12, BACK12)]   # (t, where the punch is): it comes up open, bites, holds three frames, draws back
XTR12 = [{'face': {'browL': 0.6}}, {'face': {'browL': 0.6, 'lid': 0.3}}, {'sq': [1.04, 0.95, 1.04], 'face': {'browL': 0.8, 'mouth': 'clench'}}, {'sq': [1.04, 0.95, 1.04], 'face': {'browL': 0.8, 'mouth': 'clench'}},
         {'face': {'lid': 1}}, {'bend': {'neck': [0.25, 0, 0, 1, None]}, 'face': {'browL': 0.4}}]   # his face on each leg of it: the bite, a slow blink, a nod
PUN12 = lambda i, **kw: {'hands': {'L': 'grip', 'R': 'open'}, 'reach': {'L': [round(PK12[i][1][0] - 0.17 * DJ12[0], 3), PK12[i][1][1], round(PK12[i][1][2] - 0.17 * DJ12[2] - V * PK12[i][0], 3), 1, 0.05]}, **kw}   # his near fist on its handles
st.shot('S12', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z12, V, D12, keys=[k(0.0, toon=JOG(face={'gy': -0.2}), toonDur=0.0)]),
            rider('dame', Z12, V, D12, expr='worried', swing=0.05, flutter=0.5),
            rider('t3', Z12, V, D12, expr='worried', keys=[k(0.0, toon=ARM12(0.0, -0.9), toonDur=0.0), k(T12 - 0.12, toon={**ARM12(T12), 'face': {'brow': 0.8, 'eye': 0.2}}, toonDur=0.12, toonEase='outBack'),   # his arm comes forward, long, with the ticket
                 *[k(round(T12 + 0.1 * i, 3), toon=ARM12(round(T12 + 0.1 * (i + 1), 3)), toonDur=0.1, toonEase='linear') for i in range(int((D12 - T12) / 0.1) + 1)]]),
            rider('tour', Z12, V, D12, expr='worried'),
            act('ctrl', SURF, 100, 'surfRide', 'unimpressed', keys=[k(0.0, look=mv12(TK12, 0.0)), k(0.0, to=mv12(SURF, D12), dur=D12, clip='surfRide', glide=True, ease='linear', face=100, cruise=True),
                 *[k(round(0.1 * i, 3), look=mv12(TK12, 0.1 * i + 0.05)) for i in range(1, 9)],                                                         # his eyes on the ticket
                 k(0.0, toon=PUN12(0, **XTR12[0]), toonDur=0.0),
                 *[k(PK12[i][0], toon=PUN12(i + 1, **XTR12[i]), toonDur=round(PK12[i + 1][0] - PK12[i][0], 3), toonEase='linear') for i in range(len(PK12) - 1)],   # his hand goes with the punch
                 k(PU12 + 0.3, look=[SURF[0] + 2.0, 1.4, round(SURF[2] - V * (PU12 + 0.3) - 3.0, 3)])])],                                                # then his eyes come to us
        props=[HEADSIGN(), UMBT(),
               P('tk0', 'bigTicket', pos=mv12(TK12, 0.0), ry=160, scale=0.01, opts={'w': 0.56, 'punchAt': PU12}, keys=[k(0.0, to=mv12(TK12, D12), dur=D12, ease='linear'), k(T12 - 0.04, scale=1.0, dur=0.08, ease='outBack')]),
               P('punch', 'ticketPunch', pos=mv12(REST12, 0.0), rot=[PROT12[0], 0, PROT12[2]], ry=PROT12[1], opts={'snapAt': PU12, 's': 1.5}, keys=[k(PK12[i][0], to=mv12(PK12[i + 1][1], PK12[i + 1][0]), dur=round(PK12[i + 1][0] - PK12[i][0], 3), ease='linear') for i in range(len(PK12) - 1)]),
               P('conf', 'confetti', pos=mv12([TK12[0] - 0.17, TK12[1] + 0.02, TK12[2]], PU12), opts={'at': PU12, 'n': 1, 's': 1.6, 'dur': D12 - PU12, 'fall': 0.5, 'drift': [0.2, 3.0]}, keys=[k(PU12, to=mv12([TK12[0] - 0.17, TK12[1] + 0.02, TK12[2]], D12), dur=D12 - PU12, ease='linear')])],
        cams=[trackcam(Z12, V, 0.0, D12, [LANE + 1.5, 0.85, -1.4], [LANE + 0.15, 2.1, 2.0], lens=50)])   # from below, far enough for his cap to be in the frame: the ticket and his head on the sky
st.cue('pop', 'S12', T12, 0.3); st.cue('sfx:stretch', 'S12', T12 - 0.1, 0.25); st.cue('clack', 'S12', PU12, 0.6); st.cue('sfx:tick', 'S12', PU12 + 0.02, 0.3)

# 13: he asks to get off, in three pictures: his face, the tongue in the wind, his eyes going down; an insert on the knot of his tie: the finger comes,
#     waits, trembling, and presses: the button gives, a ring of red; his face again: the display says ARRÊT DEMANDÉ, the tongue goes back in, hope
D13 = st.dur('S13'); Z13 = 4.0; PR13 = 0.62; IN13, FA13 = 0.3, 0.76   # the press; the cuts to the insert and back to his face
TIRED = {'tongue': 1, 'tongueLen': 0.42, 'tongueYaw': 1.5, 'tongueW': 1.2, 'sweat': 1}   # the tongue flies the way the tie flies
BUTTON = lambda at_=None: P('stopb', 'stopButton', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.47, 0.155]}, opts={'pressAt': at_, 's': 1.5})
FING13 = lambda z, dx=0.0, dy=0.0, **face: JOG(face={**TIRED, 'gy': 0.8, **face}, hands={'R': 'point'}, touch={'R': ['torso', dx, 0.47 + dy, z, 1, 0.15]})
st.shot('S13', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z13, V, D13, expr='tired', keys=[k(0.0, toon=JOG(face={**TIRED, 'lid': 0.4}), toonDur=0.0),
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
def bat(z0, dur, y0=None, keys=(), expr='unimpressed'):
    a = [BATX, BATY if y0 is None else y0, round(z0 - HEADFWD, 3)]
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
            bat(Z15, D15, expr='smug', keys=st.talk('L09', 'S15', 'smug') + [k(0.0, toon={'face': {'browL': 0.5}}, toonDur=0.0),
                 *[x for t in W15 for x in (k(max(0.0, t), toon={'face': {'jaw': 0.75, 'browL': 0.8}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.05, toonEase='out'), k(max(0.0, t) + 0.14, toon={'face': {'browL': 0.5}}, toonDur=0.08))],
                 k(0.88, toon={'face': {'lid': 1, 'browL': 0.5}}, toonDur=0.04), k(0.96, toon={'face': {'browL': 0.5}}, toonDur=0.04)])],
        props=[HEADSIGN([[0, 'ARRÊT DEMANDÉ']]), BUTTON(-1), UMBT()],
        cams=[trackcam(Z15, V, 0.0, D15, [LANE + 0.2, 1.55, -3.0], [LANE - 0.21, 1.74, -HEADFWD])])   # far enough for the display on his head to be whole

# 16: there is no terminus. The inspector goes back up out of the frame, the display goes back to 12 BIS, his eyes go up to it; then very close, on his
#     eyes: the pupils, wide with hope, go down to pinpricks; a brow gives, the lower lids come up, a tear
D16 = st.dur('S16'); Z16 = round(Z15 - V * D15, 3); R16 = 0.5
EYES16 = lambda ps, **kw: JOG(face={'pupilSize': ps, 'eye': 0.45, 'brow': 1, **kw}, autoSq=0.0)
st.shot('S16', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[
            act('mec', [LANE, 0, Z16], 180, 'run', 'worried', params={'freq': 4.4, 'bounce': 0.3}, keys=[k(0.0, look=None), k(0.0, to=[LANE, 0, round(Z16 - V * D16, 3)], dur=D16, clip='run', params={'freq': 4.4, 'bounce': 0.3}, cadence=CAD, ease='linear', face=180, cruise=True),
                 k(0.0, toon=JOG(face={'brow': 0.9, 'eye': 0.3, 'pupilSize': 1.5}, autoSq=0.0), toonDur=0.0),
                 k(0.34, toon=JOG(face={'gy': -0.75, 'brow': 0.7, 'eye': 0.3, 'pupilSize': 1.5}, autoSq=0.0), toonDur=0.06),                # his eyes go up: 12 BIS again
                 k(R16 - 0.04, toon=EYES16(1.5), toonDur=0.04), k(R16 + 0.2, toon=EYES16(-1.15, mouth='wavy'), toonDur=0.2, toonEase='inOut'),   # very close: six frames of wide pupils, then they go down to pinpricks
                 k(R16 + 0.5, toon=EYES16(-1.15, browL=0.0, browR=-0.7, low=0.25, mouth='wavy'), toonDur=0.16),                            # a brow gives, the lower lids come up
                 k(R16 + 0.68, toon=EYES16(-1.15, browL=0.0, browR=-0.7, low=0.3, mouth='wavy', tear=1), toonDur=0.1),                       # a tear
                 k(R16 + 0.9, toon=EYES16(-1.15, browL=0.0, browR=-0.7, low=0.3, mouth='wavy', tear=1, lid=1), toonDur=0.05), k(R16 + 0.98, toon=EYES16(-1.15, browL=0.0, browR=-0.7, low=0.3, mouth='wavy', tear=1), toonDur=0.05)], blink=0),
            act('ctrl', [BATX, BATY, round(Z16 - HEADFWD, 3)], 180, 'batHang', 'smug', keys=[k(0.0, look=None), k(0.0, to=[BATX, BATY + 1.4, round(Z16 - V * 0.16 - HEADFWD, 3)], dur=0.16, clip='batHang', glide=True, ease='in', face=180),
                 k(0.16, to=[BATX, BATY + 1.4, round(Z16 - V * D16 - HEADFWD, 3)], dur=round(D16 - 0.16, 3), glide=True, ease='linear', face=180, cruise=True)])],
        props=[HEADSIGN([[0, 'ARRÊT DEMANDÉ'], [0.3, '12 BIS']]), BUTTON(-1), UMBT()],
        cams=[trackcam(Z16, V, 0.0, R16, [LANE + 1.1, 1.62, -2.5], [LANE, 1.82, -HEADFWD]),
              trackcam(Z16, V, R16, D16, [LANE + 0.42, 1.8, -1.42], [LANE + 0.0, 1.84, -HEADFWD], lens=46)])   # his eyes in the upper third, his mouth over the caption band
st.cue('sfx:slideUp', 'S16', 0.0, 0.3); st.cue('sfx:tick', 'S16', 0.3, 0.35); st.cue('sfx:slideDownSlow', 'S16', R16 + 0.2, 0.3)

# 17: yesterday: a traffic light goes to red
D17 = st.dur('S17'); TL = [5.55, 0, -60.0]; RED17 = 0.2
LIGHT = lambda state, **kw: P('light', 'trafficLight', pos=TL, ry=90, opts={'state': state, 'headRy': -90, **kw})   # it bends down the street (-Z); its lenses face up the street
st.shot('S17', 'parisStreet', setOpts={**STREET, 'eiffel': False}, props=[LIGHT([[0, 'a'], [RED17, 'r']])],
        cams=[cam(0.0, [6.2, 1.5, TL[2] + 2.6], [6.15, 1.5, TL[2] + 2.45], [TL[0], 2.55, TL[2]], [TL[0], 2.55, TL[2]], lens=44)])
st.cue('clack', 'S17', RED17, 0.45)

# 18: he stops. From the side, the pole at four tenths of the width: he takes it low, in both hands; his body goes on, feet first, flat in the air, and the
#     pole bends over him like a rod; it holds eight frames, trembling, his eyes come to us; it whips back in three frames and throws him at its foot:
#     flat for five frames; he comes back up past his height and settles, seeing stars. Then close, the red lamp over him: steam, a look up at it
D18 = st.dur('S18'); G18, FB18, HE18, BK18, FE18, UP18 = 0.14, 0.3, 0.57, 0.67, 0.84, 1.04   # he takes the pole; full bend; the hold ends; flat at its foot; the flat ends; he is up again
CU18 = 1.32                                           # the close shot
PH18 = 2.1                                            # the height of the bending part of the pole
A18 = 0.9                                             # how far it bends
hand18 = lambda a, s_: pole_pt(TL, PH18, a, s_, ry=90)
X18 = 5.02; AT18 = [X18, 0, TL[2] + 0.35]; IN18 = [LANE + 0.5, 0, round(AT18[2] + V * G18, 3)]
OUT18 = [X18 + 0.03, 0.05, round(TL[2] - 1.15, 3)]     # his hips at full bend: flat in the air on his back, feet first, the pole in his hands behind his head
HOLD18 = lambda a, **kw: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [*hand18(a, 1.18), 1, 0.05], 'R': [*hand18(a, 1.0), 1, 0.05]}, **kw}
LEAN18 = {'hands': {'L': 'grip'}, 'reach': {'L': [*hand18(0.0, 1.5), 1, 0.05]}}   # a hand left on the pole
BEND18 = [[G18, 0.0], [FB18, A18], [FB18 + 0.07, A18 - 0.06], [FB18 + 0.14, A18 + 0.02], [FB18 + 0.2, A18 - 0.04], [HE18, A18], [BK18 - 0.02, -0.14], [BK18 + 0.08, 0.0]]   # the pole: over with him, trembling while it holds, back past upright
CAMW18 = [10.0, 1.9, round(TL[2] - 0.35, 3)]
FLAG18 = {'dir': -1, 'droop': 0.05, 'swing': 0.0, 'flutter': 0.5, 'expr': 'scared'}
STRETCH18 = {'sq': [0.9, 0.9, 1.28], 'auto': 0.2}
st.shot('S18', 'parisStreet', setOpts={**STREET, 'eiffel': False}, look={'fill': 1.35}, actors=[act('mec', IN18, 180, 'run', 'scared', params=RUN, keys=[k(0.0, look=None), k(0.0, to=AT18, dur=G18, clip='run', params=RUN, ease='linear', face=180, cruise=True),
            k(0.0, toon=JOG(autoSq=0.45, **HOLD18(0.0, face={'gy': -0.6, 'brow': 0.9, 'mouth': 'clench'})), toonDur=0.0),                                        # his arms out ahead of him to the pole
            k(G18, to=OUT18, dur=round(FB18 - G18, 3), clip='flag', params=FLAG18, then='flag', glide=True, ease='out', face=180, blend=0.04),                                 # the body goes on, feet first
            k(G18, toon=HOLD18(A18, **STRETCH18, face={'pop': 0.5, 'jaw': 0.5}), toonDur=round(FB18 - G18, 3), toonEase='inOut'),                               # the pole comes over with him
            k(FB18, toon=HOLD18(A18 - 0.06, **STRETCH18, face={'eye': 0.35, 'brow': 0.9, 'mouth': 'clench', 'sweat': 1}), toonDur=0.07, toonEase='inOut'), k(FB18 + 0.02, look=CAMW18), k(FB18 + 0.02, expr='worried'),   # it holds: his eyes come to us
            k(FB18 + 0.07, toon=HOLD18(A18 + 0.02, **STRETCH18, face={'eye': 0.35, 'brow': 0.9, 'mouth': 'clench', 'sweat': 1}), toonDur=0.07, toonEase='inOut'),
            k(FB18 + 0.14, toon=HOLD18(A18 - 0.04, **STRETCH18, face={'eye': 0.35, 'brow': 1, 'mouth': 'wavy', 'sweat': 1}), toonDur=0.06, toonEase='inOut'),
            k(FB18 + 0.2, toon=HOLD18(A18, **STRETCH18, face={'eye': 0.4, 'brow': 1, 'mouth': 'wavy', 'sweat': 1, 'pupilSize': -0.4}), toonDur=round(HE18 - FB18 - 0.2, 3), toonEase='inOut'),
            k(HE18, to=AT18, dur=round(BK18 - HE18, 3), clip='stand', then='stand', glide=True, ease='in', arc=0.5, face=90, blend=0.05), k(HE18, look=None),                 # it whips back: three frames, over the top
            k(HE18, toon=HOLD18(-0.14, sq=[0.8, 0.8, 1.6], auto=0.2, face={'pop': 0.6, 'jaw': 0.6}), toonDur=round(BK18 - HE18 - 0.02, 3), toonEase='inOut'),
            k(BK18 - 0.01, toon={'sq': [1.55, 0.26, 1.55], 'auto': 0, 'face': {'lid': 1, 'mouth': 'clench'}}, toonDur=0.03, toonEase='in'),                       # thrown at its foot: flat, five frames
            k(FE18, toon={'sq': [0.87, 1.15, 0.87], 'auto': 0, 'face': {'eye': 0.45, 'brow': 1, 'pupilSize': -0.4}}, toonDur=0.07, toonEase='out'), k(FE18, expr='dizzy'),   # he comes back up past his height
            k(FE18 + 0.07, toon={**LEAN18, 'sq': [1.07, 0.92, 1.07], 'auto': 0, 'face': {'stars': 0.9, 'cross': 0.5}}, toonDur=0.06),
            k(FE18 + 0.13, toon={**LEAN18, 'settle': 0.8, 'bend': {'neck': [0, 0.14, 0, 1, None]}, 'face': {'stars': 0.9, 'cross': 0.5}}, toonDur=0.1, toonEase='outBack'),   # and settles, a hand on the pole, seeing stars
            k(UP18 + 0.1, toon={**LEAN18, 'bend': {'neck': [0, -0.14, 0, 1, None]}, 'face': {'stars': 0.8, 'cross': 0.4, 'lid': 0.5}}, toonDur=0.14),
            k(CU18 - 0.02, toon={**LEAN18, 'face': {'steam': 1, 'eye': 0.3, 'brow': 0.8}}, toonDur=0.04), k(CU18 - 0.02, expr='worried'), k(CU18 - 0.02, look=[7.3, 1.7, TL[2] + 2.3]),   # close: steam out of his ears
            k(CU18 + 0.2, toon={**LEAN18, 'face': {'steam': 0.9, 'gy': -0.85, 'gx': 0.5, 'brow': 0.6, 'eye': 0.2}}, toonDur=0.07), k(CU18 + 0.28, look=[TL[0], 3.0, TL[2] + 0.6]),                     # his eyes, then his head, go up to the red lamp
            k(CU18 + 0.5, toon={**LEAN18, 'face': {'steam': 0.6, 'gy': -0.85, 'gx': 0.5, 'brow': 0.6, 'lid': 1}}, toonDur=0.05), k(CU18 + 0.58, toon={**LEAN18, 'face': {'steam': 0.4, 'gy': -0.85, 'gx': 0.5, 'brow': 0.3}}, toonDur=0.05)], blink=0),   # a blink: it is true
        act('ctrl', [IN18[0] - 0.44, BATY + 1.5, IN18[2] - HEADFWD], 180, 'batHang', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[AT18[0] - 0.44, BATY + 1.5, AT18[2] - HEADFWD], dur=G18, clip='batHang', glide=True, ease='linear', face=180, cruise=True),
            k(G18, to=[LANE + 0.3, 1.3, TL[2] - 7.0], dur=0.55, clip='superman', glide=True, ease='linear', face=180, blend=0.04, cruise=True), k(G18, expr='surprised')])],   # the inspector, who hung over him, goes on, straight ahead
        props=[LIGHT([[0, 'r']], bend=BEND18, spring=[[BK18 + 0.08, 0.1, 15, 5]]), HEADSIGN(), BUTTON(-1)],
        fx=[{'type': 'shake', 'at': BK18, 'dur': 0.18, 'amount': 0.025}],
        cams=[cam(0.0, CAMW18, [9.95, 1.9, CAMW18[2]], [5.5, 1.3, CAMW18[2]], [5.5, 1.3, CAMW18[2]], lens=66),   # across the pavement, from a little above: the road and the far pavement behind him, not the shop fronts
              glide([cam(BK18, [8.3, 1.5, round(TL[2] + 0.1, 3)], [8.25, 1.5, round(TL[2] + 0.1, 3)], [5.3, 1.12, round(TL[2] + 0.1, 3)], [5.3, 1.12, round(TL[2] + 0.1, 3)], lens=60)], 0.22),   # in on the foot of the pole as he lands there
              cam(CU18, [7.3, 1.7, TL[2] + 2.3], [7.2, 1.7, TL[2] + 2.25], [5.2, 2.05, TL[2] + 0.25], [5.2, 2.05, TL[2] + 0.25], lens=44)])   # three quarters: his face, and the red lamp over him, lit, toward us
st.cue('sfx:stretch', 'S18', G18, 0.4); st.cue('whoosh', 'S18', G18, 0.4, 0.2, 500, 2200); st.cue('sfx:twang', 'S18', HE18, 0.45); st.cue('whoosh', 'S18', HE18, 0.4, 0.1, 900, 3000); st.cue('thud', 'S18', BK18, 0.6)
st.cue('sfx:boing', 'S18', FE18, 0.35); st.cue('sfx:whistle', 'S18', CU18, 0.4)

# 19: not his passengers: from the side again: he stands at the pole and they cross the frame one after the other, still flat in the air; his head goes with them
D19 = st.dur('S19'); V19 = 9.0
def pass19(who, t0, y, dx, ph):                       # one passenger: level with him at t0
    z0 = round(AT18[2] + V19 * t0, 3)
    return act(who, [LANE + dx, y, z0], 180, 'flag', 'scared', params={'phase': ph, 'swing': 0.12}, keys=[k(0.0, look=None), k(0.0, to=[LANE + dx, y, round(z0 - V19 * D19, 3)], dur=D19, clip='flag', params={'phase': ph, 'swing': 0.12}, glide=True, ease='linear', face=180, cruise=True)])
st.shot('S19', 'parisStreet', setOpts={**STREET, 'eiffel': False}, look={'fill': 1.35}, actors=[act('mec', AT18, 90, 'stand', 'relieved', blink=0, keys=[k(0.0, look=[8.2, 1.65, TL[2] + 0.2]), k(0.0, toon={**LEAN18, 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.12, toon={**LEAN18, 'sq': [0.97, 1.05, 0.97], 'face': {'brow': 0.9, 'eye': 0.3}}, toonDur=0.06, toonEase='outBack'), k(0.12, look=[LANE, 1.5, AT18[2] + 2.5], expr='surprised'),   # his head turns up the street: something is coming
            k(0.3, look=[LANE, 1.5, AT18[2] - 1.0]), k(0.55, look=[LANE, 1.5, AT18[2] - 6.0]),                                              # and goes with them, down the street
            k(0.62, toon={**LEAN18, 'face': {'brow': 0.9, 'eye': 0.3, 'lid': 1}}, toonDur=0.04), k(0.7, toon={**LEAN18, 'face': {'brow': 0.9, 'eye': 0.3}}, toonDur=0.04),   # a blink
            k(0.8, toon={**LEAN18, 'face': {'brow': 0.7, 'eye': 0.3, 'mouth': 'wavy'}}, toonDur=0.08), k(0.84, look=[9.95, 1.6, TL[2] - 0.3])]),       # then to us, eyes open
        pass19('dame', 0.2, 0.45, 0.0, 0.0), pass19('t3', 0.36, 0.7, -0.25, 2.0), pass19('tour', 0.52, 0.3, 0.15, 4.0)],
        props=[LIGHT([[0, 'r']]), HEADSIGN(), BUTTON(-1), P('umb', 'crookUmbrella', on={'actor': 'dame', 'hand': 'R', 'offset': [0, 0.0, 0.0], 'rot': [3.1416, 0, 0]}, opts=CROOK)],
        fx=[{'type': 'wind', 'at': 0.15, 'dur': 0.6, 'v': [0, 0, -11], 'attack': 0.05, 'release': 0.3}],
        cams=[cam(0.0, [10.0, 1.6, TL[2] - 0.3], [9.95, 1.6, TL[2] - 0.3], [5.5, 1.7, TL[2] - 0.3], [5.5, 1.7, TL[2] - 0.3], lens=50)])   # him at the left quarter, whole; they cross behind him
[st.cue('whoosh', 'S19', t, 0.4, 0.25, 500, 2400) for t in (0.2, 0.36, 0.52)]

# 20: they arrive early: at the station, the four of them come down on the bench one after the other; four wrists come up, four pairs of eyes go wide
D20 = st.dur('S20'); ZB = -100.0; BENCH = [9.45, 0, ZB]; W20 = 0.66; E20 = 0.9
SEATS = {'dame': 0.78, 't3': 0.26, 'tour': -0.26, 'ctrl': -0.78}; LAND = {'dame': 0.04, 't3': 0.13, 'tour': 0.22, 'ctrl': 0.31}
def lands20(who):
    zs = round(ZB + SEATS[who], 3); t0 = LAND[who]; seat = [BENCH[0] + 0.05, 0.02, zs]
    return act(who, [seat[0] - 0.3, 3.6, round(zs + 2.8, 3)], -90, 'sit', 'scared', keys=[k(0.0, look=None), k(0.0, clip='sit'), k(t0, to=seat, dur=0.13, clip='sit', glide=True, ease='in', face=-90), k(t0 + 0.13, clip='sit', blend=0.02),
            k(t0 + 0.13, toon={'sq': [1.25, 0.7, 1.25]}, toonDur=0.03), k(t0 + 0.17, toon={'sq': [0.95, 1.08, 0.95], 'settle': 0.6}, toonDur=0.08, toonEase='outBack'), k(t0 + 0.17, expr='dizzy'), k(t0 + 0.28, toon={}, toonDur=0.08),
            k(W20, clip='sitWatch', blend=0.08), k(W20, expr='neutral'), k(E20, toon={'sq': [0.96, 1.06, 0.96], 'face': {'eye': 0.4, 'brow': 0.9}}, toonDur=0.08, toonEase='outBack'), k(E20, expr='surprised')])
st.shot('S20', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[lands20(w) for w in ('dame', 't3', 'tour', 'ctrl')],
        props=[*[P(f'watch_{w}', 'wristWatch', on={'actor': w, 'hand': 'L', 'offset': [0, 0.075, 0.0], 'rot': [0, 0, 0]}, opts={'s': 1.5}) for w in ('dame', 't3', 'tour', 'ctrl')],
               P('bench', 'bench', pos=BENCH, ry=-90, opts={'w': 2.4}), P('gare', 'stationSign', pos=[10.12, 2.95, ZB + 0.25], ry=-90, opts={'text': 'GARE', 'w': 1.5}), P('clock', 'wallClock', pos=[10.12, 2.95, ZB - 0.95], ry=-90, opts={'rate': 0})],
        fx=[{'type': 'shake', 'at': LAND['dame'] + 0.13, 'dur': 0.45, 'amount': 0.012}],
        cams=[cam(0.0, [3.9, 1.45, ZB], [4.1, 1.45, ZB], [9.45, 1.5, ZB], [9.45, 1.5, ZB], lens=44)])
[st.cue('thud', 'S20', LAND[w] + 0.13, 0.4) for w in LAND]; st.cue('sfx:tick', 'S20', W20, 0.3); st.cue('sfx:gasp', 'S20', E20, 0.3)

# 21: a first: at the red light, seen from up the street (the light above him, red): he has turned round, a hand on the pole; the display on his head turns
#     to HORS SERVICE; he shuts his eyes, breathes in, breathes out
D21 = st.dur('S21'); HS21 = 0.3
HELD21 = LEAN18
CAM21 = lambda t, b: cam(t, [4.64, 1.6, TL[2] + 3.3 - b], [4.67, 1.6, TL[2] + 3.15 - b], [5.2, 1.85, TL[2] + 0.2], [5.2, 1.85, TL[2] + 0.2], lens=44)
PANT = lambda a, **face: {**HELD21, 'sq': [1 - 0.5 * a, 1 + a, 1 - 0.5 * a], 'face': {'brow': 0.6, **face}}   # a breath: the chest up (a > 0) or down
st.shot('S21', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[act('mec', AT18, 0, 'stand', 'neutral', blink=0, keys=[k(0.0, look=None), k(0.0, toon=PANT(-0.02, mouth='o'), toonDur=0.0),
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
D22 = st.dur('S22'); P22 = 0.5; V22 = 11.0; G22 = 1.25
X22 = 4.45                                            # his path: half a metre from the hero's shoulder
A22 = [X22, 0, round(AT18[2] - V22 * P22, 3)]; M22 = [X22, 0, AT18[2]]; C22 = [X22 - 1.3, 0, round(AT18[2] + V22 * 0.55, 3)]   # from down the street, level with him at P22, then past the camera at its left
BR22 = {'expr': 'scared'}
st.shot('S22', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[act('mec', AT18, 0, 'stand', 'relieved', blink=0, keys=[k(0.0, look=None), k(0.0, toon={**HELD21, 'sq': [1.01, 0.98, 1.01], 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.02, toon={**HELD21, 'sq': [0.985, 1.03, 0.985], 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.2, toonEase='inOut'), k(0.24, toon={**HELD21, 'sq': [1.01, 0.98, 1.01], 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.2, toonEase='inOut'),   # he breathes, slowly, eyes shut
            k(P22 - 0.02, toon={**HELD21, 'sq': [0.97, 1.05, 0.97], 'face': {'eye': 0.3, 'brow': 0.8, 'gx': -0.8}}, toonDur=0.06, toonEase='outBack'), k(P22 - 0.02, expr='surprised'),   # the wind of him: his eyes open
            k(P22 + 0.08, look=[X22 - 1.2, 1.4, AT18[2] + 5.0]), k(P22 + 0.5, look=None),                                                    # his head goes after him, past us, and comes back
            k(P22 + 0.5, toon={**HELD21, 'face': {'brow': 0.3}}, toonDur=0.1), k(P22 + 0.5, expr='neutral'),
            k(P22 + 0.58, toon={**HELD21, 'face': {'lid': 1}}, toonDur=0.05), k(P22 + 0.69, toon={**HELD21, 'face': {}}, toonDur=0.05),         # to us; a slow blink
            k(G22 + 0.08, toon={**HELD21, 'face': {'gy': -0.9, 'gx': 0.6}}, toonDur=0.08), k(G22 + 0.3, toon={**HELD21, 'face': {'mouth': 'smirk', 'browL': 0.4}}, toonDur=0.1)]),   # the green light: a look up at it, back to us: no
        act('mec2', A22, 0, 'heelBrake', 'scared', params=BR22, keys=[k(0.0, look=None), k(0.0, path=[M22, C22], dur=P22 + 0.55, clip='heelBrake', params=BR22, glide=True, ease='linear', face=0, cruise=True),   # one move, two legs: his arms do not start again as he passes
            k(0.0, toon={'face': {'mouth': 'clench', 'brow': 0.9, 'sweat': 1}}, toonDur=0.0)])],
        props=[LIGHT([[0, 'r'], [G22, 'g']]), HEADSIGN([[0, 'HORS SERVICE']]), BUTTON(-1),
               P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A22[0], A22[2] + 0.55], [P22, M22[0], M22[2] + 0.55], [P22 + 0.55, C22[0], C22[2] + 0.55]], 'from': 0.0, 'to': P22 + 0.55, 'every': 0.03, 'marks': True})],
        fx=[{'type': 'wind', 'at': P22 - 0.05, 'dur': 0.4, 'v': [0, 0, 10], 'attack': 0.05, 'release': 0.25}],
        cams=[cam(0.0, [4.6, 1.6, TL[2] + 4.6], [4.6, 1.6, TL[2] + 4.55], [5.0, 1.8, TL[2] + 0.2], [5.0, 1.8, TL[2] + 0.2], lens=44),
              glide([cam(P22 + 0.42, [4.75, 1.62, TL[2] + 3.3], [4.76, 1.62, TL[2] + 3.25], [5.2, 1.85, TL[2] + 0.2], [5.2, 1.85, TL[2] + 0.2], lens=44)], 0.6)])   # wide enough to see him come and pass; then in on the one who stays
st.cue('sfx:squeak', 'S22', 0.05, 0.4); st.cue('whoosh', 'S22', P22 - 0.3, 0.45, 0.6, 400, 2200); st.cue('clack', 'S22', G22, 0.35)

st.card('S08', 'UNE LIGNE')   # one line of card: its band stops at 18 % of the height, over his head
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("L'élan", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'chauf': {'preset': 'officiel', 'seed': 111, 'suit': '#31557F', 'tie': '#1F2A3D', 'hat': 'copcap', 'hatColor': '#31557F', 'glasses': False, 'facial': 'mustache', 'build': {'width': 0.9, 'headWidth': 1.3}},
    'ctrl': CITIZEN('officiel', 131, suit='#34507A', tie='#F2C230', hat='copcap', hatColor='#34507A', glasses=False, facial='stubble', clothTie=True), 'mec2': CITIZEN('lemec_brown', 133),
    'dame': CITIZEN('madame', 121, suit='#C8553D'), 'tour': CITIZEN('fermier', 123), 't3': CITIZEN('lyceen', 125, suit='#3F7A5A'),
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'p1': {'preset': 'femme', 'seed': 113, 'build': {'width': 0.86, 'headWidth': 1.3}}, 'p2': {'preset': 'lyceen', 'seed': 115, 'build': {'width': 0.86, 'headWidth': 1.3}}, 'p3': {'preset': 'mamie', 'seed': 117, 'build': {'width': 0.86, 'headWidth': 1.3}}})
