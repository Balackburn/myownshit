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
st.plan([('S01', 'L01', 0), ('S02', 'L01', 8), ('S03', 'L02', 0), ('S04', 'L02', 5), ('S05', 'L03', 0), ('S06', 'L03', 3), ('S07', 'L04', 0), ('S08', 'L05', 0),
         ('S09', 'L06', 0), ('S10', 'L06', 1), ('S11', 'L07', 0), ('S12', 'L07', 4), ('S13', 'L08', 0), ('S14', 'L08', 5), ('S15', 'L09', 0), ('S16', 'L10', 0),
         ('S17', 'L11', 0), ('S18', 'L11', 1), ('S19', 'L12', 0), ('S20', 'L13', 0), ('S21', 'L13', 5), ('S22', 26.2, 0)])

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

# 1: the hook: he runs beside his bus, which is leaving, and bangs on its door; close, three quarters front, the camera running backward with them; a
#    passenger waves at him through the glass. Then the bus brakes
X1 = 5.35; Z1 = 30.0                                 # his line on the pavement, at the kerb; where he is at 0
z1 = lambda t: round(Z1 - V * t, 3)
D1 = st.dur('S01'); BR1 = 1.55                       # the bus brakes
ZC1 = lambda t: round(z1(min(t, BR1)) + 3.15, 3)     # the bus keeps its front door 0.9 m behind him; then it falls back
ZC2 = round(ZC1(BR1) - 4.8, 3)                       # where it stops
RUN = {'freq': 4.4}
SPRINT = lambda **kw: {'bend': {'spine': [0.42, 0, 0, 1.04, None], 'neck': [-0.3, 0, 0, 1.1, None]}, 'autoSq': 0.3, **kw}   # autoSq: at 4.4 strides a second the automatic squash of each footfall lands on one frame in three or four, never the same: seen close, his head drops 40 cm for a frame; a third of it is a bounce
SHOUT = {'gx': 0.9, 'jaw': 0.6, 'brow': 0.7, 'eye': 0.25}
def knock1(t, on, face=SHOUT):                       # his left hand on the glass of the door (on), or drawn back, at t (the door runs with him)
    tgt = [3.84, 1.55, z1(t) + 0.9] if on else [4.35, 1.62, z1(t) + 0.6]
    return SPRINT(hands={'L': 'open'}, reach={'L': [*tgt, 1, 0.06]}, face=face)
KN1 = [(0.0, 0), (0.3, 0), (0.42, 1), (0.5, 1), (0.66, 0), (0.78, 1), (0.86, 1), (1.02, 0), (1.14, 1), (1.22, 1), (1.42, 0), (BR1 + 0.08, 0)]   # three knocks
inbus1 = lambda loc: [k(0.0, to=bus_at(ZC1(BR1), *loc), dur=BR1, glide=True, ease='linear'), k(BR1, to=bus_at(ZC2, *loc), dur=1.2, glide=True, ease='out')]
st.shot('S01', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[act('mec', [X1, 0, Z1], 180, 'run', 'scared', params=RUN, keys=[*[k(t, look=[X1 + 1.5, 1.6, z1(t) - 2.6]) for t in (0.0, 0.35, 0.7, 1.05, 1.4, 1.75)], k(0.0, to=[X1, 0, z1(D1)], dur=D1, clip='run', params=RUN, ease='linear', face=180),   # his head three quarters to us (looking where he runs, the face was a sliver)
            k(0.0, toon=knock1(0.0, 0), toonDur=0.0), *[k(KN1[i][0], toon=knock1(KN1[i + 1][0], KN1[i + 1][1]), toonDur=round(KN1[i + 1][0] - KN1[i][0], 3), toonEase='linear') for i in range(len(KN1) - 1)],
            k(BR1 + 0.08, toon=SPRINT(hands={'L': 'spread', 'R': 'spread'}, face={'gx': 0.9, 'brow': 1, 'eye': 0.35, 'jaw': 0.3}, sq=[0.97, 1.05, 0.97]), toonDur=0.1, toonEase='outBack'),   # the door is gone from under his hand: a look after it
            k(BR1 + 0.3, toon=SPRINT(hands={'L': 'spread', 'R': 'spread'}, face={'gx': 0.0, 'brow': 1, 'eye': 0.4, 'mouth': 'wavy'}), toonDur=0.08)]),   # then ahead: and me?
        act('chauf', bus_at(ZC1(0), *SEATL), 180, 'drive', 'unimpressed', keys=[k(0.0, look=None), *inbus1(SEATL)]),
        act('p1', bus_at(ZC1(0), *RIDERL[0][1]), 90, 'wave', 'happy', keys=[k(0.0, look='mec'), *inbus1(RIDERL[0][1])])],
        props=[BUS(ZC1(0), k(0.0, to=[BX, 0, ZC1(BR1)], dur=BR1, ease='linear'), k(BR1, to=[BX, 0, ZC2], dur=1.2, ease='out'), rock=[[BR1, 0.02]])],
        cams=[cam(0.0, [X1 + 1.8, 1.5, Z1 - 2.2], [X1 + 1.7, 1.5, z1(D1) - 2.1], [X1, 1.55, Z1 - 0.4], [X1, 1.55, z1(D1) - 0.4], lens=44)])   # he leans across the frame, his head up at the right, the door behind his shoulders
st.cue('whoosh', 'S01', 0.0, 0.25, 0.5, 500, 1800); [st.cue('thud', 'S01', t, 0.45) for t in (0.42, 0.78, 1.14)]; st.cue('sfx:squeak', 'S01', BR1, 0.5)

# 2: he brakes with his heels and does not stop: the camera runs backward in front of him; behind him the bus, stopped, gets smaller
D2 = st.dur('S02'); V2 = 7.5
A2, B2 = [5.3, 0, z1(D1)], [5.2, 0, round(z1(D1) - V2 * D2, 3)]
st.shot('S02', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[act('mec', A2, 180, 'heelBrake', 'scared', keys=[k(0.0, look=None), k(0.0, to=B2, dur=D2, clip='heelBrake', glide=True, ease='linear', face=180),
            k(0.0, toon={'face': {'gy': 0.4, 'brow': 0.8, 'mouth': 'clench'}}, toonDur=0.0),                                 # his eyes on his heels
            k(0.5, toon={'face': {'gy': 0.4, 'brow': 0.9, 'mouth': 'clench', 'sweat': 1}}, toonDur=0.1),
            k(0.9, toon={'face': {'brow': 1, 'eye': 0.3, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.08), k(1.12, toon={'face': {'brow': 1, 'eye': 0.3, 'mouth': 'wavy', 'sweat': 1, 'lid': 1}}, toonDur=0.04), k(1.2, toon={'face': {'brow': 1, 'eye': 0.3, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.04)]),   # then on us; a blink
        act('chauf', bus_at(ZC2, *SEATL), 180, 'drive', 'unimpressed', keys=[k(0.0, look='mec')]), *[act(n, bus_at(ZC2, *loc), ry, 'stand', 'surprised', keys=[k(0.0, look='mec')]) for n, loc, ry in RIDERL]],
        props=[BUS(ZC2), P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A2[0], A2[2] - 0.55], [D2, B2[0], B2[2] - 0.55]], 'from': 0.0, 'to': D2, 'every': 0.03, 'marks': True})],
        cams=[cam(0.0, [6.9, 1.15, A2[2] - 3.4], [6.8, 1.15, B2[2] - 3.4], [A2[0], 1.25, A2[2]], [B2[0], 1.25, B2[2]], lens=44)])
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
        cams=[cam(0.0, [2.7, 1.55, DRV3[2] - 2.6], [2.66, 1.55, DRV3[2] - 2.5], [2.1, 1.55, DRV3[2]], [2.1, 1.55, DRV3[2]], lens=44)])
st.cue('whoosh', 'S03', 0.0, 0.4, 0.3, 600, 2000); st.cue('sfx:boing', 'S03', W3, 0.4); st.cue('sfx:spring', 'S03', W3 + 0.08, 0.3)

# 4: the sign at the edge of town: he goes by it, still braking; it spins on its post
D4 = st.dur('S04'); V4 = 14.0; P4 = 0.55              # he passes the sign
A4 = [1.1, 0, round(V4 * P4, 3)]; B4 = [1.1, 0, round(V4 * (P4 - D4), 3)]
st.shot('S04', 'grassland', actors=[act('mec', A4, 180, 'heelBrake', 'worried', keys=[k(0.0, look=None), k(0.0, to=B4, dur=D4, clip='heelBrake', glide=True, ease='linear', face=180),
            k(0.0, toon={'face': {'gx': -0.8, 'gy': -0.4, 'brow': 0.8}}, toonDur=0.0), k(P4 + 0.1, toon={'face': {'brow': 1, 'mouth': 'wavy'}}, toonDur=0.08)])],
        props=[P('road', 'roadStrip', pos=[-1.3, 0, 0], opts={'len': 500, 'w': 6.5}), P('sign', 'townSign', pos=[2.45, 0, 0], opts={'name': 'PARIS', 'spinAt': P4 + 0.03, 'turns': 3.5, 'spinDur': 1.6}),
               P('tower', 'eiffelTower', pos=[-32, 0, 190], opts={'h': 60}),
               P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A4[0], A4[2] - 0.55], [D4, B4[0], B4[2] - 0.55]], 'from': 0.0, 'to': D4, 'every': 0.025, 'marks': True})],
        cams=[cam(0.0, [1.7, 0.8, -7.0], [1.7, 0.84, -6.8], [1.75, 1.75, 0.5], [1.75, 1.75, 0.5], lens=44)])
st.cue('whoosh', 'S04', P4 - 0.3, 0.5, 0.5, 500, 2200); st.cue('sfx:spring', 'S04', P4 + 0.03, 0.35)

# ---- the stop, laps later: he runs in the bus lane along the kerb (x = LANE), people wait on the pavement
LANE = 4.3
zrun = lambda z0, v, t: round(z0 - v * t, 3)
# 5: the third lap: three people in a line at the kerb, each holding the coat of the one in front; the middle one flips his lap board: 2, 3. A wind rises
D5 = st.dur('S05'); F5 = 0.4                          # the board flips
LADY5, T35, TOUR5 = [5.75, 0, 0.0], [5.3, 0, 1.0], [5.9, 0, 2.0]   # the lady in front (with the hook), the second, the board man last (nearest the camera of S05)
HOOK5 = [4.3, 1.42, 0.0]                             # the crook of her umbrella, out over the lane
BOARD5 = [6.22, 1.2, 2.06]                          # the foot of the board's stick, in his left fist
UMB = lambda *keys: P('umb', 'umbrella', pos=HOOK5, rot=[0, 0, -1.5708], opts={'open': 0.0, 'colors': ['#2F7F5C', '#F2EDE4'], 'height': 0.95}, keys=list(keys))   # held out flat, the crook over the lane
LADYHOLD = {'hands': {'R': 'grip'}, 'reach': {'R': [HOOK5[0] + 0.98, HOOK5[1], HOOK5[2], 1, 0.05]}}
TOURHOLD = {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [BOARD5[0], BOARD5[1] + 0.06, BOARD5[2], 1, 0.05], 'R': [T35[0] + 0.2, 1.2, T35[2] + 0.2, 1, 0.06]}}
T3HOLD = {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [LADY5[0] + 0.05, 1.15, LADY5[2] + 0.2, 1, 0.06], 'R': [LADY5[0] - 0.12, 1.25, LADY5[2] + 0.18, 1, 0.06]}, 'bend': {'spine': [-0.2, 0, 0, 1, None]}}
st.shot('S05', 'parisStreet', setOpts={**STREET, 'eiffelX': 12}, actors=[
        act('dame', LADY5, 0, 'stand', 'determined', keys=[k(0.0, look=[5.0, 1.5, 9.0]), k(0.0, toon={**LADYHOLD, 'bend': {'spine': [0, 0.14, 0, 1, None]}}, toonDur=0.0), k(0.55, toon={**LADYHOLD, 'bend': {'spine': [0.1, 0.22, 0, 1, None]}, 'sq': [1.05, 0.93, 1.05], 'face': {'brow': -0.5, 'eye': 0.15}}, toonDur=0.2)]),   # she braces
        act('tour', TOUR5, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[5.0, 1.5, 9.0]), k(0.0, toon=TOURHOLD, toonDur=0.0), k(F5 - 0.03, toon={**TOURHOLD, 'scl': {'handL': [1.25, 0.8, 1.25]}, 'face': {'browL': 0.6}}, toonDur=0.05), k(F5 + 0.1, toon=TOURHOLD, toonDur=0.08),
            k(F5 + 0.26, toon={**TOURHOLD, 'face': {'lid': 1}}, toonDur=0.04), k(F5 + 0.34, toon=TOURHOLD, toonDur=0.04)]),   # a flick of the wrist, no look at the board; a blink
        act('t3', T35, 0, 'stand', 'worried', keys=[k(0.0, look=[5.0, 1.5, 9.0]), k(0.0, toon=T3HOLD, toonDur=0.0), k(0.5, toon={**T3HOLD, 'sq': [1.06, 0.92, 1.06], 'face': {'eye': 0.3, 'brow': 0.8}}, toonDur=0.25), k(0.6, expr='scared')])],
        props=[UMB(), P('board', 'lapBoard', pos=BOARD5, opts={'flips': [[0, '2'], [F5, '3']], 'w': 0.5})],
        fx=[{'type': 'wind', 'at': 0.45, 'dur': 0.6, 'v': [0, 0, -9], 'attack': 0.3, 'release': 0.1}],
        cams=[cam(0.0, [5.3, 1.5, 5.6], [5.33, 1.5, 5.4], [5.9, 1.6, 1.0], [5.9, 1.6, 1.0], lens=44)])
st.cue('sfx:tick', 'S05', F5, 0.5); st.cue('gust', 'S05', 0.4, 0.3, 0.6)

# 6: he comes through: her crook takes him by the collar and the three of them leave one after the other, past the camera; the board stays in the air, falls
D6 = st.dur('S06'); V6 = 10.0; H6 = 0.36              # the hook
zh6 = lambda t: zrun(V6 * H6, V6, t)                  # he is at z = 0 at H6
fly6 = lambda who, pos0, lag, gap, ph: act(who, pos0, 0, 'stand', 'scared', keys=[k(0.0, look=[LANE, 1.5, 6.0]),
            k(H6 + lag, to=[LANE + 0.12, 0.3, zh6(H6 + lag + 0.1) + gap], dur=0.1, glide=True, clip='flag', params={'phase': ph, 'swing': 0.2}, ease='in', face=180, blend=0.03),
            k(H6 + lag, toon={'sq': [0.8, 0.8, 1.7]}, toonDur=0.04), k(H6 + lag + 0.08, toon={}, toonDur=0.08),            # a smear as she leaves
            k(H6 + lag + 0.1, to=[LANE + 0.12, 0.3, zh6(D6) + gap], dur=D6 - H6 - lag - 0.1, glide=True, ease='linear', face=180)])
st.shot('S06', 'parisStreet', setOpts={**STREET, 'eiffelX': 12}, actors=[
        act('mec', [LANE, 0, zh6(0)], 180, 'run', 'worried', params=RUN, keys=[k(0.0, look=None), k(0.0, to=[LANE, 0, zh6(D6)], dur=D6, clip='run', params=RUN, ease='linear', face=180), k(0.0, toon=SPRINT(face={'gx': -0.7, 'brow': 0.6}), toonDur=0.0),
            k(H6, toon=SPRINT(sq=[0.94, 1.0, 1.12], face={'pop': 0.5, 'jaw': 0.4}, bend={'spine': [0.1, 0, 0, 1.04, None], 'neck': [-0.5, 0, 0, 1.3, None]}), toonDur=0.05, toonEase='out'),   # caught by the collar: his neck stays behind a frame
            k(H6 + 0.12, toon=SPRINT(face={'brow': 0.9, 'mouth': 'wavy'}), toonDur=0.1)]),
        fly6('dame', LADY5, 0.0, 1.95, 0.0), fly6('t3', T35, 0.07, 3.3, 2.0), fly6('tour', TOUR5, 0.14, 4.65, 4.0)],
        props=[UMB(k(H6, attach='mec', joint='torso', offset=[0, 0.5, -0.14], rot=[-1.5708, 0, 0])),
               P('board', 'lapBoard', pos=BOARD5, opts={'flips': [[0, '3']], 'w': 0.5}, keys=[k(H6 + 0.14, rotTo=[0.4, 9.0, 1.2], dur=0.5, ease='out'), k(H6 + 0.14, to=[BOARD5[0], BOARD5[1] + 0.35, BOARD5[2]], dur=0.16, ease='out'), k(H6 + 0.3, to=[BOARD5[0] + 0.1, 0.03, BOARD5[2] - 0.3], dur=0.34, ease='in')])],
        fx=[{'type': 'wind', 'at': H6 - 0.1, 'dur': 0.5, 'v': [0, 0, -12], 'attack': 0.05, 'release': 0.3}],
        cams=[cam(0.0, [4.98, 1.3, -5.5], [4.98, 1.3, -5.3], [4.85, 1.4, 0.5], [4.85, 1.4, 0.5], lens=44)])
st.cue('whoosh', 'S06', H6 - 0.25, 0.5, 0.5, 400, 2400); st.cue('sfx:boing', 'S06', H6, 0.4); st.cue('whoosh', 'S06', H6 + 0.5, 0.35, 0.3, 600, 2000); st.cue('clack', 'S06', H6 + 0.57, 0.3)

# 7: the mayor settles it: his hand goes up like a blade, holds, comes down: the desk is cut in two
D7 = st.dur('S07'); C7 = 0.62                         # the blow
MAY7 = [0.0, 0, -1.62]; DESK7 = [0.0, 0, -0.9]
OFFICE = {'desk': False, 'map': False, 'plant': False}
UP7 = {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [0.05, 2.78, -1.52, 1, 0.08, [1, 0.3, 0.4]], 'R': [-0.05, 2.78, -1.52, 1, 0.08, [-1, 0.3, 0.4]]}}   # both hands joined over his head, elbows out: an axe
jump7 = lambda pid, name, pos, opts, dy, dx: P(pid, name, pos=pos, opts=opts, keys=[k(C7, to=[pos[0] + dx * 0.5, pos[1] + dy, pos[2]], dur=0.12, ease='out'), k(C7 + 0.12, to=[pos[0] + dx, pos[1] - 0.3, pos[2] + 0.05], dur=0.2, ease='in'), k(C7, rotTo=[0.3, 0.6, dx * 3], dur=0.32)])
st.shot('S07', 'mairie', setOpts=OFFICE, actors=[act('maire', MAY7, 0, 'stand', 'determined', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gy': 0.5}}, toonDur=0.0),
            k(0.06, toon={**UP7, 'sq': [0.93, 1.12, 0.93], 'bend': {'spine': [-0.3, 0, 0, 1.06, None]}, 'face': {'gy': 0.5, 'brow': -0.6, 'cheeks': 0.6}}, toonDur=0.26, toonEase='outBack'),   # up on his toes, a breath, the hands high behind his head
            k(0.4, toon={**UP7, 'sq': [0.93, 1.12, 0.93], 'bend': {'spine': [-0.36, 0.03, 0, 1.06, None]}, 'face': {'gy': 0.5, 'brow': -0.7, 'cheeks': 0.8}}, toonDur=0.16),   # held: it trembles
            k(C7 - 0.05, toon={'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [0.05, 0.84, -0.98, 1, 0.08], 'R': [-0.05, 0.84, -0.98, 1, 0.08]}, 'sq': [1.2, 0.78, 1.2], 'bend': {'spine': [0.55, 0, 0, 0.95, None]}, 'face': {'gy': 0.6, 'brow': -0.9, 'mouth': 'clench'}}, toonDur=0.05, toonEase='in'),   # down in two frames
            k(C7 + 0.12, toon={'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [0.05, 0.55, -0.98, 1, 0.08], 'R': [-0.05, 0.55, -0.98, 1, 0.08]}, 'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.5, 0, 0, 1, None]}, 'face': {'gy': 0.6}}, toonDur=0.1),
            k(C7 + 0.32, toon={'settle': 0.6, 'face': {'brow': 0.3}}, toonDur=0.2, toonEase='outBack'), k(C7 + 0.32, expr='smug'), k(C7 + 0.6, toon={'face': {'lid': 1}}, toonDur=0.04), k(C7 + 0.68, toon={'face': {'browL': 0.5}}, toonDur=0.05)])],   # he straightens, pleased; a blink
        props=[P('desk', 'splitDesk', pos=DESK7, opts={'at': C7, 'w': 1.7}),
               jump7('pot', 'mug', [-0.5, 0.76, -0.85], {}, 0.45, -0.25), jump7('paper', 'paperPile', [0.45, 0.765, -0.8], {'count': 8}, 0.6, 0.3),
               P('crack', 'impactStars', pos=[0.0, 0.85, -0.6], opts={'at': C7, 'n': 5, 'r': 0.42, 'r0': 0.16, 'dur': 0.26, 'size': 0.085})],
        fx=[{'type': 'shake', 'at': C7, 'dur': 0.2, 'amount': 0.03}],
        cams=[cam(0.0, [0.35, 1.42, 2.05], [0.3, 1.42, 1.9], [0.0, 1.52, -1.2], [0.0, 1.52, -1.2], lens=44)])
st.cue('sfx:slideUp', 'S07', 0.06, 0.3); st.cue('whoosh', 'S07', C7 - 0.08, 0.4, 0.1, 700, 2600); st.cue('thud', 'S07', C7, 0.7); st.cue('clack', 'S07', C7 + 0.02, 0.5); st.cue('sfx:boing', 'S07', C7 + 0.3, 0.25)

# 8: « C'est une ligne. »: he says it, the map of the line in his hand: a loop, and on it a little head that goes round
D8 = st.dur('S08'); MAP8 = [0.5, 1.14, -1.22]
st.shot('S08', 'mairie', setOpts=OFFICE, actors=[act('maire', MAY7, 0, 'stand', 'smug', keys=st.talk('L05', 'S08', 'smug') + [k(0.0, look=None),
            k(0.0, toon={'hands': {'L': 'grip', 'R': 'point'}, 'reach': {'L': [MAP8[0] + 0.3, MAP8[1] + 0.5, MAP8[2] - 0.03, 1, 0.05], 'R': [MAP8[0] - 0.14, MAP8[1] + 0.36, MAP8[2] + 0.06, 1, 0.12]}, 'face': {'browL': 0.5}}, toonDur=0.0),
            k(0.5, toon={'hands': {'L': 'grip', 'R': 'point'}, 'reach': {'L': [MAP8[0] + 0.3, MAP8[1] + 0.5, MAP8[2] - 0.03, 1, 0.05], 'R': [MAP8[0] - 0.1, MAP8[1] + 0.44, MAP8[2] + 0.06, 1, 0.12]}, 'bend': {'spine': [0.06, -0.05, 0, 1, None]}, 'face': {'brow': 0.6}}, toonDur=0.15, toonEase='outBack')])],
        props=[P('desk', 'splitDesk', pos=DESK7, opts={'at': -1, 'w': 1.7}), P('map', 'lineMap', pos=MAP8, ry=-8, opts={'title': 'LIGNE 12 BIS', 'lap': 0.9})],
        cams=[cam(0.0, [0.75, 1.62, 1.25], [0.72, 1.62, 1.12], [0.22, 1.77, -1.4], [0.22, 1.77, -1.4], lens=44)])

# 9: the display of the stop: 1 MIN, 0 MIN; the pigeon on it looks up the street
D9 = st.dur('S09'); DISP = [5.6, 0, 1.2]; PIG = [DISP[0], 2.6 + 0.24, DISP[2]]
DISPLAY = lambda texts, **kw: P('disp', 'busDisplay', pos=DISP, ry=90, opts={'line': '12 BIS', 'texts': texts, **kw})
st.shot('S09', 'parisStreet', setOpts={**STREET, 'eiffel': False}, props=[DISPLAY([[0, '1 MIN'], [0.33, '0 MIN']]),
               P('pig', 'pigeon', pos=PIG, ry=90, keys=[k(0.36, rotTo=[0, math.radians(20), 0], dur=0.1, ease='outBack')])],
        cams=[cam(0.0, [7.95, 1.95, 1.8], [7.85, 1.97, 1.75], [5.62, 2.56, 1.21], [5.62, 2.56, 1.21], lens=44)])
st.cue('sfx:tick', 'S09', 0.33, 0.5)

# ---- the line: he runs along the lane, the three passengers fly behind him like a kite's tail (the lady hooked to his collar by her umbrella)
GAP = {'dame': 1.95, 't3': 3.3, 'tour': 4.65}; OFFX = {'dame': 0.12, 't3': -0.1, 'tour': 0.15}; FLY = {'dame': 0.3, 't3': 0.45, 'tour': 0.25}; PH = {'dame': 0.0, 't3': 2.0, 'tour': 4.0}
HEADSIGN = lambda texts=None, **kw: P('hs', 'headSign', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.56, 0.0], 'sway': 1}, opts={'texts': texts or [[0, '12 BIS']], 'w': 0.55, 'hh': 0.16, **kw})
COLLAR = {'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.58, -0.13], 'rot': [-1.5708, 0, 0]}
HEADFWD, HEADDROP = 0.45, 0.3                        # running, his head is that far ahead of his feet and that much lower than standing: aim close cameras there
def rider(who, z0, v, dur, expr='scared', keys=(), **par):        # one passenger of the tail: z0 is the hero's z at 0
    a = [LANE + OFFX[who], FLY[who], round(z0 + GAP[who], 3)]; b = [a[0], a[1], round(a[2] - v * dur, 3)]; pr = {'phase': PH[who], 'swing': 0.16, **par}
    return act(who, a, 180, 'flag', expr, params=pr, keys=[k(0.0, look=None), k(0.0, to=b, dur=dur, clip='flag', params=pr, glide=True, ease='linear', face=180), *keys])
def runner(z0, v, dur, expr='unimpressed', keys=(), x=None):       # the hero
    x = LANE if x is None else x
    return act('mec', [x, 0, z0], 180, 'run', expr, params=RUN, keys=[k(0.0, look=None), k(0.0, to=[x, 0, round(z0 - v * dur, 3)], dur=dur, clip='run', params=RUN, ease='linear', face=180), *keys])
TAIL = lambda z0, v, dur, **kw: [rider(w, z0, v, dur, **kw) for w in ('dame', 't3', 'tour')]
UMBT = lambda: P('umb', 'umbrella', on=COLLAR, opts={'open': 0.0, 'colors': ['#2F7F5C', '#F2EDE4'], 'height': 0.95})
JOG = SPRINT   # his toon base while running
closeup = lambda z0, v, dur, side=1.2, back=2.75, h=1.6, dy=0.0, push=0.12: [cam(0.0, [LANE + side, h, z0 - back], [LANE + side - push, h, z0 - v * dur - back + push], [LANE, 1.72 + dy, z0 - HEADFWD], [LANE, 1.72 + dy, z0 - v * dur - HEADFWD], lens=44)]   # the camera running backward in front of him, on his head

# 10: he comes through the stop with his passengers: 0 MIN; the display goes back to 8 MIN, the pole of the stop bends after him and rings, the pigeon is gone
D10 = st.dur('S10'); P10 = 0.3; V10 = 10.0            # he is level with the pole
z10 = round(1.5 + V10 * P10, 3)
POLE10 = [5.45, 0, -0.15]
st.shot('S10', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[runner(z10, V10, D10), *TAIL(z10, V10, D10)],
        props=[DISPLAY([[0, '0 MIN'], [P10 + 0.22, '8 MIN']]), STOPPOLE(pos=POLE10, bend=[[P10 - 0.02, 0], [P10 + 0.12, 0.55]], spring=[[P10 + 0.12, 0.55, 14, 3.4]]), HEADSIGN(), UMBT(),
               P('pig', 'pigeon', pos=PIG, ry=110, keys=[k(P10 + 0.02, to=[PIG[0] - 0.3, PIG[1] + 0.9, PIG[2] - 2.6], dur=0.3, ease='out'), k(P10 + 0.02, rotTo=[0.8, 3.0, 2.2], dur=0.3), k(P10 + 0.32, to=[PIG[0] - 0.6, PIG[1] + 1.6, PIG[2] - 7.0], dur=0.5, ease='linear')])],
        fx=[{'type': 'wind', 'at': P10 - 0.08, 'dur': 0.7, 'v': [0, 0, -12], 'attack': 0.05, 'release': 0.3}],
        cams=[cam(0.0, [8.6, 1.55, -1.9], [8.5, 1.55, -1.8], [5.5, 1.8, 0.5], [5.5, 1.8, 0.5], lens=44)])
st.cue('whoosh', 'S10', P10 - 0.25, 0.5, 0.8, 400, 2400); st.cue('sfx:tick', 'S10', P10 + 0.22, 0.5); st.cue('sfx:spring', 'S10', P10 + 0.12, 0.4)

# 11: his number: close, the camera running backward in front of him: the display on his head rocks at each stride; his eyes go up to it, come back to us
D11 = st.dur('S11'); Z11 = 20.0
st.shot('S11', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z11, V, D11, keys=[k(0.0, toon=JOG(face={'gy': -0.9, 'brow': 0.5}), toonDur=0.0), k(0.4, toon=JOG(face={'brow': -0.2}), toonDur=0.1), k(0.62, toon=JOG(face={'lid': 1}), toonDur=0.04), k(0.7, toon=JOG(face={'browL': 0.4}), toonDur=0.05)]),
            *TAIL(Z11, V, D11)],
        props=[HEADSIGN(), UMBT()],
        cams=closeup(Z11, V, D11, side=1.3, back=2.5, h=1.7, dy=0.08))
st.cue('sfx:tick', 'S11', 0.0, 0.3)

# 12: his inspectors: one surfs on the back of the lady, sideways, a hand held out to the two behind; their tickets come up one after the other; he
#     punches the first. Seen from the pavement side, level with the hero (who is out of the frame): the inspector large at the right, the tail goes away to the left
D12 = st.dur('S12'); Z12 = 12.0; T12 = [0.28, 0.4]; PU12 = 0.8
def tick12(i, who):                                   # a ticket held up over a passenger: (the prop, his toon keys)
    a = [LANE + OFFX[who] + 0.1, FLY[who] + 1.05 + 0.8, round(Z12 + GAP[who] - 0.65, 3)]; b = [a[0], a[1], round(a[2] - V * D12, 3)]; at_ = lambda t: lerp3(a, b, t / D12)
    prop = P(f'tk{i}', 'bigTicket', pos=a, ry=160, scale=0.01, opts={'w': 0.5, 'punchAt': PU12 if i == 0 else None}, keys=[k(0.0, to=b, dur=D12, ease='linear'), k(T12[i], scale=1.0, dur=0.08, ease='outBack')])
    hold = lambda t: {'hands': {'L': 'pinch', 'R': 'grip'}, 'reach': {'L': [at_(t)[0] - 0.02, at_(t)[1] - 0.14, at_(t)[2], 1, 0.05]}}
    return prop, [k(T12[i] - 0.1, toon=hold(T12[i]), toonDur=0.1, toonEase='out'), k(T12[i], toon=hold(D12), toonDur=round(D12 - T12[i], 3), toonEase='linear')]
TK12 = [tick12(0, 't3'), tick12(1, 'tour')]
SURF = [LANE + OFFX['dame'], FLY['dame'] + 1.05 + 0.1, round(Z12 + GAP['dame'] - 0.3, 3)]       # the inspector's feet: on the lady's back
punch12 = lambda t: lerp3([LANE + OFFX['t3'] + 0.1, FLY['t3'] + 1.05 + 0.82, Z12 + GAP['t3'] - 0.7], [LANE + OFFX['t3'] + 0.1, FLY['t3'] + 1.05 + 0.82, Z12 + GAP['t3'] - 0.7 - V * D12], t / D12)
st.shot('S12', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z12, V, D12, keys=[k(0.0, toon=JOG(face={'gy': -0.2}), toonDur=0.0)]),
            rider('dame', Z12, V, D12, expr='worried', swing=0.05, flutter=0.5), rider('t3', Z12, V, D12, expr='worried', keys=TK12[0][1]), rider('tour', Z12, V, D12, expr='worried', keys=TK12[1][1]),
            act('ctrl', SURF, 95, 'surfRide', 'unimpressed', keys=[k(0.0, look=[SURF[0] + 0.6, 2.0, SURF[2] + 2.0]), k(0.0, to=[SURF[0], SURF[1], round(SURF[2] - V * D12, 3)], dur=D12, clip='surfRide', glide=True, ease='linear', face=95),
                 k(0.0, toon={'hands': {'L': 'open'}, 'reach': {'L': [*punch12(0.0), 0.0, 0.05]}}, toonDur=0.0),
                 k(0.1, toon={'hands': {'L': 'open'}, 'reach': {'L': [punch12(0.22)[0], punch12(0.22)[1] - 0.25, punch12(0.22)[2] - 0.5, 1, 0.05]}, 'face': {'browL': 0.6}}, toonDur=0.12, toonEase='outBack'),   # a hand held out: tickets
                 k(0.22, toon={'hands': {'L': 'open'}, 'reach': {'L': [punch12(PU12 - 0.1)[0], punch12(PU12 - 0.1)[1] - 0.25, punch12(PU12 - 0.1)[2] - 0.5, 1, 0.05]}, 'face': {'browL': 0.6}}, toonDur=round(PU12 - 0.32, 3), toonEase='linear'),
                 k(PU12 - 0.1, toon={'hands': {'L': 'pinch'}, 'reach': {'L': [punch12(PU12)[0], punch12(PU12)[1] - 0.05, punch12(PU12)[2] - 0.08, 1, 0.05]}}, toonDur=0.1, toonEase='in'),   # he punches the first one
                 k(PU12, toon={'hands': {'L': 'pinch'}, 'reach': {'L': [punch12(D12)[0], punch12(D12)[1] - 0.05, punch12(D12)[2] - 0.08, 1, 0.05]}, 'face': {'lid': 0.4}}, toonDur=round(D12 - PU12, 3), toonEase='linear')])],
        props=[HEADSIGN(), UMBT(), TK12[0][0], TK12[1][0]],
        cams=[cam(0.0, [LANE + 1.9, 2.2, Z12 - 1.0], [LANE + 1.83, 2.2, Z12 - V * D12 - 0.95], [LANE - 0.1, 2.5, Z12 + 3.0], [LANE - 0.1, 2.5, Z12 - V * D12 + 3.0], lens=50)])   # from beside him (he is out of the frame, at our right: only the umbrella goes to him): the inspector at the right, the two tickets going away to the left
[st.cue('pop', 'S12', t, 0.3) for t in T12]; st.cue('clack', 'S12', PU12, 0.5)

# 13: he asks to get off: his tongue flies beside his head; his eyes go down to the red button on the knot of his tie, he presses it: ARRÊT DEMANDÉ
D13 = st.dur('S13'); Z13 = 4.0; PR13 = 0.62
TIRED = {'tongue': 1, 'tongueLen': 0.42, 'tongueYaw': -1.5, 'sweat': 1}
BUTTON = lambda at_=None: P('stopb', 'stopButton', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.47, 0.155]}, opts={'pressAt': at_, 's': 1.5})
st.shot('S13', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z13, V, D13, expr='tired', keys=[k(0.0, toon=JOG(face={**TIRED, 'lid': 0.5}), toonDur=0.0),
                 k(0.3, toon=JOG(face={**TIRED, 'gy': 0.8}), toonDur=0.08), k(PR13 - 0.2, toon=JOG(face={**TIRED, 'gy': 0.8}, hands={'R': 'point'}, touch={'R': ['torso', 0.0, 0.47, 0.3, 1, 0.1]}), toonDur=0.14, toonEase='out'),   # the finger over the button: a beat
                 k(PR13 - 0.03, toon=JOG(face={**TIRED, 'gy': 0.8}, hands={'R': 'point'}, touch={'R': ['torso', 0.0, 0.47, 0.19, 1, 0.1]}), toonDur=0.03, toonEase='in'),
                 k(PR13 + 0.14, toon=JOG(face={**TIRED, 'gy': -0.9, 'brow': 0.8}, hands={'R': 'point'}, touch={'R': ['torso', 0.0, 0.47, 0.26, 1, 0.1]}), toonDur=0.1),   # his eyes go up to the display
                 k(PR13 + 0.42, toon=JOG(face={**TIRED, 'brow': 0.9, 'eye': 0.2}), toonDur=0.12)]),                                  # then to us: hope
            *TAIL(Z13, V, D13)],
        props=[HEADSIGN([[0, '12 BIS'], [PR13 + 0.03, 'ARRÊT DEMANDÉ']]), BUTTON(PR13), UMBT()],
        cams=closeup(Z13, V, D13, side=1.2, back=2.75, h=1.6))
st.cue('sfx:tick', 'S13', PR13, 0.4); st.cue('sfx:ding', 'S13', PR13 + 0.03, 0.5)

# 14: the answer: the inspector comes down into the frame beside his head, hanging head down like a bat: two faces, one the wrong way up
D14 = st.dur('S14'); Z14 = -6.0; F14 = 0.26
BATX, BATY = LANE - 0.58, 1.62 - HEADDROP + 0.48     # where he hangs: his head level with the hero's, at his left (our right) (+0.36: measured on stills once the run no longer squashed him)
def bat(z0, dur, y0=None, keys=(), expr='unimpressed'):
    a = [BATX, BATY if y0 is None else y0, round(z0 - HEADFWD, 3)]
    return act('ctrl', a, 180, 'batHang', expr, keys=[k(0.0, look=None), k(0.0, to=[a[0], a[1], round(a[2] - V * dur, 3)], dur=dur, clip='batHang', glide=True, ease='linear', face=180), *keys])
st.shot('S14', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z14, V, D14, expr='tired', keys=[k(0.0, toon=JOG(face={**TIRED, 'brow': 0.9, 'eye': 0.2}), toonDur=0.0),
                 k(F14 + 0.1, toon=JOG(face={'gx': 0.9, 'brow': 0.9, 'eye': 0.3}), toonDur=0.08), k(F14 + 0.5, toon=JOG(face={'gx': 0.9, 'brow': 0.9, 'eye': 0.3, 'lid': 1}), toonDur=0.04), k(F14 + 0.58, toon=JOG(face={'gx': 0.9, 'brow': 0.9, 'eye': 0.3}), toonDur=0.04)]),   # his eyes go to it; a blink
            act('ctrl', [BATX, BATY + 1.3, round(Z14 - HEADFWD, 3)], 180, 'batHang', 'unimpressed', keys=[k(0.0, look=None),
                 k(0.0, to=[BATX, BATY + 1.3, round(Z14 - V * F14 + 0.4 - HEADFWD, 3)], dur=round(F14 - 0.05, 3), clip='batHang', glide=True, ease='linear', face=180),
                 k(round(F14 - 0.05, 3), to=[BATX, BATY - 0.08, round(Z14 - V * (F14 + 0.07) - HEADFWD, 3)], dur=0.12, glide=True, ease='out', face=180),       # he drops into the frame
                 k(round(F14 + 0.07, 3), to=[BATX, BATY, round(Z14 - V * D14 - HEADFWD, 3)], dur=round(D14 - F14 - 0.07, 3), glide=True, ease='linear', face=180),
                 k(F14 + 0.07, toon={'sq': [1.08, 0.9, 1.08]}, toonDur=0.04), k(F14 + 0.14, toon={'settle': 0.5}, toonDur=0.1, toonEase='outBack'), k(F14 + 0.6, toon={'face': {'gx': -0.8}}, toonDur=0.08)])],
        props=[HEADSIGN([[0, 'ARRÊT DEMANDÉ']]), BUTTON(-1), UMBT()],
        cams=[cam(0.0, [LANE + 0.6, 1.55, Z14 - 2.85], [LANE + 0.55, 1.55, Z14 - V * D14 - 2.75], [LANE - 0.27, 1.69, Z14 - HEADFWD], [LANE - 0.27, 1.69, Z14 - V * D14 - HEADFWD], lens=44)])
st.cue('sfx:slideDown', 'S14', F14 - 0.05, 0.35); st.cue('sfx:boing', 'S14', F14 + 0.07, 0.3)

# 15: « Au terminus. »: he says it head down, to us; the hero's eyes on him, then ahead
D15 = st.dur('S15'); Z15 = round(Z14 - V * D14, 3)
st.shot('S15', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z15, V, D15, expr='tired', keys=[k(0.0, toon=JOG(face={'gx': 0.9, 'brow': 0.9, 'eye': 0.3}), toonDur=0.0), k(0.62, toon=JOG(face={'brow': 0.9, 'eye': 0.3, 'gy': 0.1}), toonDur=0.1)]),
            bat(Z15, D15, expr='smug', keys=st.talk('L09', 'S15', 'smug') + [k(0.0, toon={'face': {'browL': 0.5}}, toonDur=0.0), k(0.7, toon={'face': {'lid': 1}}, toonDur=0.04), k(0.78, toon={'face': {'browL': 0.5}}, toonDur=0.04)])],
        props=[HEADSIGN([[0, 'ARRÊT DEMANDÉ']]), BUTTON(-1), UMBT()],
        cams=[cam(0.0, [LANE + 0.55, 1.55, Z15 - 2.75], [LANE + 0.5, 1.55, Z15 - V * D15 - 2.65], [LANE - 0.27, 1.69, Z15 - HEADFWD], [LANE - 0.27, 1.69, Z15 - V * D15 - HEADFWD], lens=44)])

# 16: there is no terminus: the inspector goes back up out of the frame; his pupils go down to pinpricks, a brow gives, his lip shakes; the display goes back to 12 BIS
D16 = st.dur('S16'); Z16 = round(Z15 - V * D15, 3); R16 = 0.5
st.shot('S16', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[runner(Z16, V, D16, expr='worried', keys=[k(0.0, toon=JOG(face={'brow': 0.6, 'eye': 0.2}), toonDur=0.0),
                 k(R16, toon=JOG(face={'pupilSize': -0.62, 'eye': 0.5, 'brow': 1, 'mouth': 'wavy'}, sq=[0.97, 1.04, 0.97]), toonDur=0.1, toonEase='out'),      # it sinks in
                 k(R16 + 0.45, toon=JOG(face={'pupilSize': -0.62, 'eye': 0.5, 'browL': 1, 'browR': 0.3, 'mouth': 'wavy', 'tear': 1}), toonDur=0.2),
                 k(R16 + 0.8, toon=JOG(face={'pupilSize': -0.62, 'eye': 0.5, 'browL': 1, 'browR': 0.3, 'mouth': 'wavy', 'tear': 1, 'lid': 1}), toonDur=0.04), k(R16 + 0.88, toon=JOG(face={'pupilSize': -0.62, 'eye': 0.5, 'browL': 1, 'browR': 0.3, 'mouth': 'wavy', 'tear': 1}), toonDur=0.04)]),
            act('ctrl', [BATX, BATY, round(Z16 - HEADFWD, 3)], 180, 'batHang', 'smug', keys=[k(0.0, look=None), k(0.0, to=[BATX, BATY + 1.4, round(Z16 - V * 0.16 - HEADFWD, 3)], dur=0.16, clip='batHang', glide=True, ease='in', face=180),
                 k(0.16, to=[BATX, BATY + 1.4, round(Z16 - V * D16 - HEADFWD, 3)], dur=round(D16 - 0.16, 3), glide=True, ease='linear', face=180)])],
        props=[HEADSIGN([[0, 'ARRÊT DEMANDÉ'], [R16, '12 BIS']]), BUTTON(-1), UMBT()],
        cams=closeup(Z16, V, D16, side=1.1, back=2.5, h=1.62, dy=0.1, push=0.35))
st.cue('sfx:slideUp', 'S16', 0.0, 0.3); st.cue('sfx:tick', 'S16', R16, 0.35); st.cue('sfx:slideDownSlow', 'S16', R16, 0.3)

# 17: yesterday: a traffic light goes to red
D17 = st.dur('S17'); TL = [5.55, 0, -60.0]; RED17 = 0.3
LIGHT = lambda state, **kw: P('light', 'trafficLight', pos=TL, ry=90, opts={'state': state, 'headRy': -90, **kw})   # it bends down the street (-Z); its lenses face up the street
st.shot('S17', 'parisStreet', setOpts={**STREET, 'eiffel': False}, props=[LIGHT([[0, 'a'], [RED17, 'r']])],
        cams=[cam(0.0, [6.2, 1.5, TL[2] + 2.6], [6.15, 1.5, TL[2] + 2.45], [TL[0], 2.55, TL[2]], [TL[0], 2.55, TL[2]], lens=44)])
st.cue('clack', 'S17', RED17, 0.45)

# 18: he gets to the red light and takes its pole in both hands: the inspector goes on without him, his own body swings past the pole, feet first,
#     the pole bends after him, brings him back and stands him on his feet (seen from the side: a wide lens). Then close: stopped, steam out of his ears
D18 = st.dur('S18'); G18, SW18, BK18 = 0.24, 0.42, 0.72   # his hands close on the pole; the swing at its furthest; back on his feet
CU18 = BK18 + 0.1                                     # the close shot
PH18 = 2.1                                            # the height of the bending part of the pole
A18 = 0.75                                            # how far it bends
hand18 = lambda a, s_: pole_pt(TL, PH18, a, s_, ry=90)
X18 = 5.02; IN18 = [LANE + 0.5, 0, round(TL[2] + 0.35 + V * G18, 3)]; AT18 = [X18, 0, TL[2] + 0.35]; OUT18 = [X18 + 0.03, 0.8, TL[2] - 1.55]
HOLD18 = lambda a, **kw: {'hands': {'L': 'grip', 'R': 'grip'}, 'reach': {'L': [*hand18(a, 1.62), 1, 0.05], 'R': [*hand18(a, 1.42), 1, 0.05]}, **kw}
LEAN18 = {'hands': {'L': 'grip'}, 'reach': {'L': [*hand18(0.0, 1.5), 1, 0.05]}}   # a hand left on the pole
SIDE18 = lambda t=0.0: cam(t, [10.0, 1.6, TL[2] - 0.7], [9.95, 1.6, TL[2] - 0.7], [5.5, 1.7, TL[2] - 0.7], [5.5, 1.7, TL[2] - 0.7], lens=60)   # across the pavement: the pole at the left, the road to swing over
st.shot('S18', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[act('mec', IN18, 180, 'run', 'scared', params=RUN, keys=[k(0.0, look=None), k(0.0, to=AT18, dur=G18, clip='run', params=RUN, ease='linear', face=180),
            k(0.0, toon=JOG(face={'gy': -0.8, 'brow': 0.9, 'eye': 0.3}), toonDur=0.0),                                             # his eyes on the red light
            k(0.06, toon=JOG(**HOLD18(0.0, face={'gy': -0.6, 'brow': 0.9, 'mouth': 'clench'})), toonDur=0.12, toonEase='in'),         # his arms go out ahead of him to the pole
            k(G18, to=OUT18, dur=SW18 - G18, clip='flag', params={'dir': -1, 'droop': 0.05, 'swing': 0.0, 'flutter': 0.4, 'expr': 'scared'}, glide=True, ease='out', face=180, blend=0.04),
            k(G18, toon=HOLD18(A18, sq=[0.9, 0.9, 1.25], face={'pop': 0.5, 'jaw': 0.5}), toonDur=SW18 - G18, toonEase='out'),          # the body goes on, feet first; the pole comes with it
            k(SW18, toon=HOLD18(A18, sq=[0.88, 0.88, 1.3], face={'pop': 0.6, 'jaw': 0.6}), toonDur=0.1),                                 # held, quivering
            k(SW18 + 0.1, to=AT18, dur=BK18 - SW18 - 0.1, clip='stand', glide=True, ease='in', face=90, blend=0.06),
            k(SW18 + 0.1, toon=HOLD18(0.0), toonDur=BK18 - SW18 - 0.1, toonEase='in'),                                                  # the pole stands up again and him with it
            k(BK18, toon={**LEAN18, 'sq': [1.25, 0.72, 1.25], 'face': {'lid': 1, 'mouth': 'clench'}}, toonDur=0.04),                       # on his feet: flat for two frames
            k(BK18 + 0.08, toon={**LEAN18, 'sq': [0.95, 1.07, 0.95], 'settle': 0.7, 'face': {'steam': 1, 'eye': 0.3, 'brow': 0.8}}, toonDur=0.1, toonEase='outBack'),
            k(BK18 + 0.08, look=[8.2, 1.65, TL[2] + 0.2]),
            k(CU18 + 0.36, toon={**LEAN18, 'face': {'steam': 0.9, 'gy': -0.9, 'gx': -0.5, 'brow': 0.6}}, toonDur=0.12),                    # his eyes go up to the red light
            k(CU18 + 0.66, toon={**LEAN18, 'sq': [1.04, 0.95, 1.04], 'settle': 0.4, 'face': {'steam': 0.4, 'lid': 1, 'mouth': 'smirk'}}, toonDur=0.2, toonEase='out'), k(CU18 + 0.66, expr='relieved')]),   # and he breathes out
        act('ctrl', [IN18[0] - 0.44, BATY + 1.5, IN18[2] - HEADFWD], 180, 'batHang', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[AT18[0] - 0.44, BATY + 1.5, AT18[2] - HEADFWD], dur=G18, clip='batHang', glide=True, ease='linear', face=180),
            k(G18, to=[LANE + 0.3, 1.3, TL[2] - 7.0], dur=0.55, clip='superman', glide=True, ease='linear', face=180, blend=0.04), k(G18, expr='surprised')])],   # the inspector, who hung over him, goes on, straight ahead
        props=[LIGHT([[0, 'r']], bend=[[G18, 0], [SW18, A18], [SW18 + 0.1, A18], [BK18, 0]], spring=[[BK18, 0.12, 15, 5]]), HEADSIGN(), BUTTON(-1)],
        fx=[{'type': 'shake', 'at': BK18, 'dur': 0.15, 'amount': 0.02}],
        cams=[SIDE18(), cam(CU18, [8.2, 1.65, TL[2] + 0.25], [8.05, 1.65, TL[2] + 0.26], [5.05, 1.8, TL[2] + 0.3], [5.05, 1.8, TL[2] + 0.3], lens=44)])
st.cue('sfx:stretch', 'S18', G18, 0.4); st.cue('whoosh', 'S18', G18, 0.4, 0.3, 500, 2200); st.cue('sfx:twang', 'S18', SW18 + 0.1, 0.4); st.cue('thud', 'S18', BK18, 0.5); st.cue('sfx:whistle', 'S18', BK18 + 0.1, 0.4)

# 19: not his passengers: from the side again: he stands at the pole and they cross the frame one after the other, still flat in the air; his head goes with them
D19 = st.dur('S19'); V19 = 9.0
def pass19(who, t0, y, dx, ph):                       # one passenger: level with him at t0
    z0 = round(AT18[2] + V19 * t0, 3)
    return act(who, [LANE + dx, y, z0], 180, 'flag', 'scared', params={'phase': ph, 'swing': 0.12}, keys=[k(0.0, look=None), k(0.0, to=[LANE + dx, y, round(z0 - V19 * D19, 3)], dur=D19, clip='flag', params={'phase': ph, 'swing': 0.12}, glide=True, ease='linear', face=180)])
st.shot('S19', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[act('mec', AT18, 90, 'stand', 'relieved', keys=[k(0.0, look=[8.2, 1.65, TL[2] + 0.2]), k(0.0, toon={**LEAN18, 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.12, toon={**LEAN18, 'sq': [0.97, 1.05, 0.97], 'face': {'brow': 0.9, 'eye': 0.3}}, toonDur=0.06, toonEase='outBack'), k(0.12, look=[LANE, 1.5, AT18[2] + 2.5], expr='surprised'),   # his head turns up the street: something is coming
            k(0.3, look=[LANE, 1.5, AT18[2] - 1.0]), k(0.55, look=[LANE, 1.5, AT18[2] - 6.0]),                                              # and goes with them, down the street
            k(0.84, toon={**LEAN18, 'face': {'brow': 0.6, 'mouth': 'wavy'}}, toonDur=0.08), k(0.84, look=[9.95, 1.6, TL[2] - 0.3])]),       # then to us
        pass19('dame', 0.2, 0.45, 0.0, 0.0), pass19('t3', 0.36, 0.7, -0.25, 2.0), pass19('tour', 0.52, 0.3, 0.15, 4.0)],
        props=[LIGHT([[0, 'r']]), HEADSIGN(), BUTTON(-1), P('umb', 'umbrella', on={'actor': 'dame', 'hand': 'R', 'offset': [0, 0.0, 0.0], 'rot': [3.1416, 0, 0]}, opts={'open': 0.0, 'colors': ['#2F7F5C', '#F2EDE4'], 'height': 0.95})],
        fx=[{'type': 'wind', 'at': 0.15, 'dur': 0.6, 'v': [0, 0, -11], 'attack': 0.05, 'release': 0.3}],
        cams=[cam(0.0, [10.0, 1.6, TL[2] - 0.3], [9.95, 1.6, TL[2] - 0.3], [5.5, 1.7, TL[2] - 0.3], [5.5, 1.7, TL[2] - 0.3], lens=50)])   # him at the left quarter, whole; they cross behind him
[st.cue('whoosh', 'S19', t, 0.4, 0.25, 500, 2400) for t in (0.2, 0.36, 0.52)]

# 20: they arrive early: at the station, the four of them come down on the bench one after the other; four wrists come up, four pairs of eyes go wide
D20 = st.dur('S20'); ZB = -100.0; BENCH = [9.45, 0, ZB]; W20 = 0.86; E20 = 1.12
SEATS = {'dame': 0.78, 't3': 0.26, 'tour': -0.26, 'ctrl': -0.78}; LAND = {'dame': 0.1, 't3': 0.22, 'tour': 0.34, 'ctrl': 0.46}
def lands20(who):
    zs = round(ZB + SEATS[who], 3); t0 = LAND[who]; seat = [BENCH[0] + 0.05, 0.02, zs]
    return act(who, [seat[0] - 0.3, 3.6, round(zs + 2.8, 3)], -90, 'sit', 'scared', keys=[k(0.0, look=None), k(0.0, clip='sit'), k(t0, to=seat, dur=0.16, clip='sit', glide=True, ease='in', face=-90), k(t0 + 0.16, clip='sit', blend=0.02),
            k(t0 + 0.16, toon={'sq': [1.25, 0.7, 1.25]}, toonDur=0.03), k(t0 + 0.2, toon={'sq': [0.95, 1.08, 0.95], 'settle': 0.6}, toonDur=0.1, toonEase='outBack'), k(t0 + 0.2, expr='dizzy'), k(t0 + 0.34, toon={}, toonDur=0.1),
            k(W20, clip='sitWatch', blend=0.08), k(W20, expr='neutral'), k(E20, toon={'sq': [0.96, 1.06, 0.96], 'face': {'eye': 0.4, 'brow': 0.9}}, toonDur=0.08, toonEase='outBack'), k(E20, expr='surprised')])
st.shot('S20', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[lands20(w) for w in ('dame', 't3', 'tour', 'ctrl')],
        props=[P('bench', 'bench', pos=BENCH, ry=-90, opts={'w': 2.4}), P('gare', 'stationSign', pos=[10.12, 2.95, ZB + 0.25], ry=-90, opts={'text': 'GARE', 'w': 1.5}), P('clock', 'wallClock', pos=[10.12, 2.95, ZB - 0.95], ry=-90, opts={'rate': 0})],
        fx=[{'type': 'shake', 'at': LAND['dame'] + 0.16, 'dur': 0.5, 'amount': 0.012}],
        cams=[cam(0.0, [3.9, 1.45, ZB], [4.1, 1.45, ZB], [9.45, 1.5, ZB], [9.45, 1.5, ZB], lens=44)])
[st.cue('thud', 'S20', LAND[w] + 0.16, 0.4) for w in LAND]; st.cue('sfx:tick', 'S20', W20, 0.3); st.cue('sfx:gasp', 'S20', E20, 0.3)

# 21: a first: at the red light, seen from up the street (the light above him, red): he has turned round, a hand on the pole; the display on his head turns
#     to HORS SERVICE; he shuts his eyes, breathes in, breathes out
D21 = st.dur('S21'); HS21 = 0.3
HELD21 = LEAN18
CAM21 = lambda t, b: cam(t, [4.75, 1.6, TL[2] + 3.3 - b], [4.78, 1.6, TL[2] + 3.15 - b], [5.2, 1.85, TL[2] + 0.2], [5.2, 1.85, TL[2] + 0.2], lens=44)
st.shot('S21', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[act('mec', AT18, 0, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={**HELD21, 'face': {'brow': 0.6, 'mouth': 'wavy'}}, toonDur=0.0),
            k(HS21 + 0.1, toon={**HELD21, 'face': {'gy': -0.9, 'brow': 0.7}}, toonDur=0.08),                                           # his eyes go up to the display
            k(HS21 + 0.4, toon={**HELD21, 'sq': [0.97, 1.06, 0.97], 'face': {'lid': 1, 'cheeks': 0.7}}, toonDur=0.14),                     # a breath in
            k(HS21 + 0.62, toon={**HELD21, 'sq': [1.05, 0.93, 1.05], 'settle': 0.4, 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.3, toonEase='out'), k(HS21 + 0.62, expr='relieved')])],   # and out: his shoulders come down
        props=[LIGHT([[0, 'r']]), HEADSIGN([[0, '12 BIS'], [HS21, 'HORS SERVICE']]), BUTTON(-1)],
        cams=[CAM21(0.0, 0.0)])
st.cue('clack', 'S21', HS21, 0.4); st.cue('sfx:slideDownSlow', 'S21', HS21 + 0.62, 0.3)

# 22: and behind him another man comes up the street, heels smoking, who cannot stop: we see him come, he does not (his eyes are shut); the wind of him
#     opens them; his head goes after him, past us, and comes back; a slow blink; the light goes green: a look up at it, back at us: he stays
D22 = st.dur('S22'); P22 = 0.5; V22 = 11.0; G22 = 1.25
X22 = 4.45                                            # his path: half a metre from the hero's shoulder
A22 = [X22, 0, round(AT18[2] - V22 * P22, 3)]; M22 = [X22, 0, AT18[2]]; C22 = [X22 - 0.45, 0, round(AT18[2] + V22 * 0.55, 3)]   # from down the street, level with him at P22, then past the camera at its left
BR22 = {'expr': 'scared'}
st.shot('S22', 'parisStreet', setOpts={**STREET, 'eiffel': False}, actors=[act('mec', AT18, 0, 'stand', 'relieved', keys=[k(0.0, look=None), k(0.0, toon={**HELD21, 'face': {'lid': 1, 'mouth': 'smirk'}}, toonDur=0.0),
            k(P22 - 0.02, toon={**HELD21, 'sq': [0.97, 1.05, 0.97], 'face': {'eye': 0.3, 'brow': 0.8, 'gx': -0.8}}, toonDur=0.06, toonEase='outBack'), k(P22 - 0.02, expr='surprised'),   # the wind of him: his eyes open
            k(P22 + 0.08, look=[X22 - 0.6, 1.4, AT18[2] + 6.0]), k(P22 + 0.5, look=None),                                                    # his head goes after him, past us, and comes back
            k(P22 + 0.5, toon={**HELD21, 'face': {'brow': 0.3}}, toonDur=0.1), k(P22 + 0.5, expr='neutral'),
            k(P22 + 0.58, toon={**HELD21, 'face': {'lid': 1}}, toonDur=0.05), k(P22 + 0.69, toon={**HELD21, 'face': {}}, toonDur=0.05),         # to us; a slow blink
            k(G22 + 0.08, toon={**HELD21, 'face': {'gy': -0.9, 'gx': 0.6}}, toonDur=0.08), k(G22 + 0.3, toon={**HELD21, 'face': {'mouth': 'smirk', 'browL': 0.4}}, toonDur=0.1)]),   # the green light: a look up at it, back to us: no
        act('mec2', A22, 0, 'heelBrake', 'scared', params=BR22, keys=[k(0.0, look=None), k(0.0, to=M22, dur=P22, clip='heelBrake', params=BR22, glide=True, ease='linear', face=0),
            k(P22, to=C22, dur=0.55, clip='heelBrake', params=BR22, glide=True, ease='linear', face=0), k(0.0, toon={'face': {'mouth': 'clench', 'brow': 0.9, 'sweat': 1}}, toonDur=0.0)])],
        props=[LIGHT([[0, 'r'], [G22, 'g']]), HEADSIGN([[0, 'HORS SERVICE']]), BUTTON(-1),
               P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A22[0], A22[2] + 0.55], [P22, M22[0], M22[2] + 0.55], [P22 + 0.55, C22[0], C22[2] + 0.55]], 'from': 0.0, 'to': P22 + 0.55, 'every': 0.03, 'marks': True})],
        fx=[{'type': 'wind', 'at': P22 - 0.05, 'dur': 0.4, 'v': [0, 0, 10], 'attack': 0.05, 'release': 0.25}],
        cams=[cam(0.0, [4.6, 1.6, TL[2] + 4.6], [4.75, 1.62, TL[2] + 3.3], [5.0, 1.8, TL[2] + 0.2], [5.2, 1.85, TL[2] + 0.2], lens=44, ease='inOut')])   # wide enough to see him come and pass; then in on the one who stays
st.cue('sfx:squeak', 'S22', 0.05, 0.4); st.cue('whoosh', 'S22', P22 - 0.3, 0.45, 0.6, 400, 2200); st.cue('clack', 'S22', G22, 0.35)

st.card('S08', "C'EST UNE LIGNE")
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("L'élan", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, extra_cast={
    'chauf': {'preset': 'officiel', 'seed': 111, 'suit': '#31557F', 'tie': '#1F2A3D', 'hat': 'copcap', 'hatColor': '#31557F', 'glasses': False, 'facial': 'mustache', 'build': {'width': 0.9, 'headWidth': 1.3}},
    'ctrl': CITIZEN('officiel', 131, suit='#34507A', tie='#F2C230', hat='copcap', hatColor='#34507A', glasses=False, facial='stubble'), 'mec2': CITIZEN('lemec_brown', 133),
    'dame': CITIZEN('madame', 121, suit='#C8553D'), 'tour': CITIZEN('fermier', 123), 't3': CITIZEN('lyceen', 125, suit='#3F7A5A'),
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'p1': {'preset': 'femme', 'seed': 113, 'build': {'width': 0.86, 'headWidth': 1.3}}, 'p2': {'preset': 'lyceen', 'seed': 115, 'build': {'width': 0.86, 'headWidth': 1.3}}, 'p3': {'preset': 'mamie', 'seed': 117, 'build': {'width': 0.86, 'headWidth': 1.3}}})
