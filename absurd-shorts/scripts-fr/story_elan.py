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

# ---- the street: he runs toward -Z (the tower at the far end). The bus stands in the lane along the right-hand pavement (x > 5), its doors on the pavement side
V = 8.0                                              # his speed, m/s
STREET = {'clear': [-40, 40], 'eiffel': True}
BX, BL = 2.6, 7.6                                    # the bus: the middle of its lane, its length; its nose at z = 0
BUS = lambda **kw: P('bus', 'cityBus', pos=[BX, 0, BL / 2], ry=90, opts={'len': BL, 'line': '12', 'dest': 'GARE', **kw})
bus_pt = lambda lx, ly, lz: r3([BX + lz, ly, BL / 2 - lx])   # a point of the bus (its own frame: +X to its nose, +Z to its doors) in the world
DOOR1 = bus_pt(BL / 2 - 1.55, 0, 1.15)               # the middle of the front door, at the kerb
SEAT = bus_pt(BL / 2 - 1.05, 0.45, -0.55)            # the driver
DRIVER = lambda *keys, **kw: act('chauf', SEAT, 180, 'drive', kw.pop('expr', 'unimpressed'), keys=list(keys), **kw)
RIDERS = [('p1', bus_pt(1.3, 0.44, 0.55), 80), ('p2', bus_pt(-0.1, 0.44, 0.6), 100), ('p3', bus_pt(-1.9, 0.44, 0.55), 85)]   # three passengers standing at the windows of the door side
POLE0 = [5.75, 0, 7.4]                               # the pole of the stop, on the pavement beside the bus's tail
STOPPOLE = lambda **kw: P('pole', 'busStopPole', pos=kw.pop('pos', POLE0), ry=kw.pop('ry', 90), opts={'line': '12', **kw})

# 1: the hook. Close, three quarters front, the camera running backward in front of him: legs in a wheel, the tie flying, an arm thrown up at the bus.
#    Then from behind him: the bus at its stop, he runs at its front door, the doors close
X1 = 5.7; Z1 = 19.0                                  # his lane on the pavement; where he is at 0
CUT1 = 1.05                                          # the view from behind
z1 = lambda t: round(Z1 - V * t, 3)
RUN = {'freq': 4.4}
SPRINT = lambda **kw: {'bend': {'spine': [0.42, 0, 0, 1.04, None], 'neck': [-0.3, 0, 0, 1.1, None]}, **kw}
D1 = st.dur('S01'); END1 = [4.75, 0, 3.05]           # where the cut to S02 finds him: a stride from the front door
SHUT1 = CUT1 + 0.42                                  # the doors start to close
st.shot('S01', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[act('mec', [X1, 0, Z1], 180, 'run', 'scared', params=RUN, keys=[k(0.0, look=None), k(0.0, to=[X1, 0, z1(CUT1)], dur=CUT1, clip='run', params=RUN, ease='linear', face=180),
            k(0.0, toon=SPRINT(face={'jaw': 0.5, 'brow': 0.6, 'eye': 0.25}), toonDur=0.0),
            k(0.3, toon=SPRINT(face={'jaw': 0.75, 'brow': 0.8, 'eye': 0.4, 'gy': -0.2}, hands={'L': 'spread'}, reach={'L': [X1 - 0.75, 1.75, z1(0.3) - 1.5, 1, 0.1]}), toonDur=0.12, toonEase='outBack'),   # an arm thrown up at the bus
            k(0.42, toon=SPRINT(face={'jaw': 0.75, 'brow': 0.8, 'eye': 0.4, 'gy': -0.2}, hands={'L': 'spread'}, reach={'L': [X1 - 0.75, 1.75, z1(CUT1) - 1.5, 1, 0.1]}), toonDur=CUT1 - 0.42, toonEase='linear'),
            k(CUT1, to=END1, dur=D1 - CUT1, clip='run', params=RUN, ease='linear', face=180),
            k(CUT1, toon=SPRINT(face={'jaw': 0.75, 'brow': 0.8}, hands={'L': 'spread', 'R': 'spread'}, reach={'L': [X1 - 0.75, 2.1, z1(CUT1) - 1.2, 1, 0.1], 'R': [X1 + 0.5, 2.1, z1(CUT1) - 1.2, 1, 0.1]}), toonDur=0.0),
            k(CUT1, toon=SPRINT(face={'jaw': 0.75, 'brow': 0.8}, hands={'L': 'spread', 'R': 'spread'}, reach={'L': [END1[0] - 0.6, 2.1, END1[2] - 1.2, 1, 0.1], 'R': [END1[0] + 0.6, 2.1, END1[2] - 1.2, 1, 0.1]}), toonDur=D1 - CUT1, toonEase='linear')]),   # both arms up: wait
        DRIVER(k(0.0, look=None))],
        props=[BUS(doors=[[0, 1], [SHUT1, 1], [SHUT1 + 0.3, 0]], rock=[[SHUT1 + 0.3, 0.012]]), STOPPOLE()],
        cams=[cam(0.0, [X1 - 0.95, 1.5, Z1 - 3.1], [X1 - 0.95, 1.5, z1(CUT1) - 3.1], [X1, 1.52, Z1], [X1, 1.52, z1(CUT1)], lens=44),
              cam(CUT1, [7.4, 2.3, 13.5], [7.25, 2.25, 12.9], [4.2, 1.3, 3.0], [4.2, 1.3, 3.0], lens=44)])
st.cue('whoosh', 'S01', 0.0, 0.3, 0.5, 500, 1800); st.cue('sfx:slideUp', 'S01', 0.3, 0.25); st.cue('sfx:squeak', 'S01', SHUT1, 0.4); st.cue('thud', 'S01', SHUT1 + 0.3, 0.4)

# 2: he brakes with his heels along the bus and does not stop: the camera runs backward in front of him; the passengers' heads follow him; he passes its nose
D2 = st.dur('S02'); V2 = 7.5
A2, B2 = [4.75, 0, 3.0], [4.6, 0, round(3.0 - V2 * D2, 3)]
at2 = lambda u: lerp3(A2, B2, u / D2)
st.shot('S02', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[act('mec', A2, 180, 'heelBrake', 'scared', keys=[k(0.0, look=None), k(0.0, to=B2, dur=D2, clip='heelBrake', glide=True, ease='linear', face=180),
            k(0.0, toon={'face': {'gx': 0.9, 'brow': 0.7, 'mouth': 'clench'}}, toonDur=0.0),                              # his eyes on the door that goes by
            k(0.5, toon={'face': {'gx': 0.0, 'gy': 0.3, 'brow': 0.9, 'mouth': 'clench', 'sweat': 1}}, toonDur=0.1),        # down at his heels
            k(0.95, toon={'face': {'brow': 1, 'eye': 0.25, 'mouth': 'wavy', 'sweat': 1}}, toonDur=0.08), k(0.95, look=[6.1, 1.3, B2[2] - 3.4])]),   # then at us
        DRIVER(k(0.0, look='mec')), *[act(n, pos, ry, 'stand', 'surprised', keys=[k(0.0, look='mec')]) for n, pos, ry in RIDERS]],
        props=[BUS(), STOPPOLE(), P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A2[0], A2[2] - 0.55], [D2, B2[0], B2[2] - 0.55]], 'from': 0.0, 'to': D2, 'every': 0.03, 'marks': True})],
        cams=[cam(0.0, [6.2, 1.15, A2[2] - 3.4], [6.1, 1.15, B2[2] - 3.4], [A2[0], 1.25, A2[2]], [B2[0], 1.25, B2[2]], lens=44)])
st.cue('sfx:squeak', 'S02', 0.0, 0.5); st.cue('whoosh', 'S02', 0.0, 0.3, D2, 300, 900)

# 3: the driver: his head goes after what passed his windows, comes back to the road, and whips round: the cap turns on his head like a top
D3 = st.dur('S03'); W3 = 0.66                         # the whip
st.shot('S03', 'parisStreet', setOpts={**STREET, 'eiffelX': -25}, actors=[
        DRIVER(k(0.0, look=None), k(0.0, toon={'face': {'gx': -0.9}}, toonDur=0.0), k(0.08, look=[6.5, 1.5, 0.2]), k(0.3, toon={'face': {'gx': -0.9, 'lid': 1}}, toonDur=0.04), k(0.38, toon={'face': {}}, toonDur=0.04),
               k(0.4, look=None), k(W3 - 0.1, toon={'sq': [1.06, 0.9, 1.06], 'face': {'lid': 0.6}}, toonDur=0.08),
               k(W3, look=[4.7, 1.3, -9.0], expr='surprised'), k(W3, toon={'scl': {'head': [1.5, 0.84, 1]}, 'sq': [0.95, 1.1, 0.95], 'hat': [0.04, 0, 3.1], 'face': {'pop': 0.7, 'jaw': 0.45}}, toonDur=0.06, toonEase='out'),
               k(W3 + 0.08, toon={'bend': {'neck': [0, 0, 0, 1.35, None]}, 'hat': [0.1, 0, 9.4], 'face': {'pop': 0.7, 'jaw': 0.45}}, toonDur=0.1, toonEase='outBack'),
               k(W3 + 0.3, toon={'bend': {'neck': [0, 0, 0, 1.2, None]}, 'hat': [0, 0, 12.566 + 3.1416], 'face': {'pop': 0.6, 'jaw': 0.4}}, toonDur=0.22, toonEase='out')),   # the cap ends back to front
        *[act(n, pos, ry, 'stand', 'surprised', keys=[k(0.0, look=[4.7, 1.3, -9.0])]) for n, pos, ry in RIDERS[:1]]],
        props=[BUS()],
        cams=[cam(0.0, [3.1, 1.72, -2.4], [3.02, 1.72, -2.2], [2.05, 1.6, 1.05], [2.05, 1.6, 1.05], lens=44)])
st.cue('whoosh', 'S03', 0.0, 0.4, 0.3, 600, 2000); st.cue('sfx:boing', 'S03', W3, 0.4); st.cue('sfx:spring', 'S03', W3 + 0.08, 0.3)

# 4: the sign at the edge of town: he goes by it, still braking; it spins on its post
D4 = st.dur('S04'); V4 = 14.0; P4 = 0.62              # he passes the sign
A4 = [0.9, 0, round(V4 * P4, 3)]; B4 = [0.9, 0, round(V4 * (P4 - D4), 3)]
st.shot('S04', 'grassland', actors=[act('mec', A4, 180, 'heelBrake', 'worried', keys=[k(0.0, look=None), k(0.0, to=B4, dur=D4, clip='heelBrake', glide=True, ease='linear', face=180),
            k(0.0, toon={'face': {'gx': -0.8, 'gy': -0.4, 'brow': 0.8}}, toonDur=0.0), k(P4 + 0.1, toon={'face': {'brow': 1, 'mouth': 'wavy'}}, toonDur=0.08)])],
        props=[P('road', 'roadStrip', pos=[0, 0, 0], opts={'len': 400, 'w': 6.5}), P('sign', 'townSign', pos=[3.0, 0, 0], opts={'name': 'PARIS', 'spinAt': P4 + 0.03, 'turns': 3.5, 'spinDur': 1.6}),
               P('tower', 'eiffelTower', pos=[-14, 0, 190], opts={'h': 60}),
               P('smoke', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0, A4[0], A4[2] - 0.55], [D4, B4[0], B4[2] - 0.55]], 'from': 0.0, 'to': D4, 'every': 0.025, 'marks': True})],
        cams=[cam(0.0, [-0.6, 0.85, -5.2], [-0.55, 0.9, -5.0], [1.9, 1.9, 0.6], [1.9, 1.9, 0.6], lens=44)])
st.cue('whoosh', 'S04', P4 - 0.3, 0.5, 0.5, 500, 2200); st.cue('sfx:spring', 'S04', P4 + 0.03, 0.35)

st.write("L'élan", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, extra_cast={
    'chauf': {'preset': 'officiel', 'seed': 111, 'suit': '#31557F', 'tie': '#1F2A3D', 'hat': 'copcap', 'hatColor': '#31557F', 'glasses': False, 'facial': 'mustache', 'build': {'width': 0.9, 'headWidth': 1.3}},
    'p1': {'preset': 'femme', 'seed': 113, 'build': {'width': 0.86, 'headWidth': 1.3}}, 'p2': {'preset': 'lyceen', 'seed': 115, 'build': {'width': 0.86, 'headWidth': 1.3}}, 'p3': {'preset': 'mamie', 'seed': 117, 'build': {'width': 0.86, 'headWidth': 1.3}}})
