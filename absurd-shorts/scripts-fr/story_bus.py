#!/usr/bin/env python3
"""Le bus (story 72, cycle 34; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man missed his bus by two seconds. So he ran after it. He never stopped. After an hour he had left the town. The gendarmes escorted him on
motorbikes. The villages cheered him from the roadside. The ministry of sport gave him a race number. The cycle race changed its route to follow him.
They threw him the yellow jersey. The driver never looked in his mirror. They crossed the Alps. In Italy a waiter held out pasta to him on the run.
He wore out four hundred pairs of shoes. Scientists measured his calves. After three years the bus stopped. He got on. It was not the right bus.
Staging (pass 2, after the first reviews: animation 5.2, art 5.6): his face opens the film, three-quarter front at the stop (line 12) while the bus
(21 ROME on its back) pulls away behind him; a wheel of legs on the spot, then a smear exit; the wheel again under a steady torso down the street;
the town sign crossed out; from there the travelling shots are filmed like a treadmill: he runs on the spot, the road dashes, the trees and the dust
slide back under him (the gags' hands and props stay on fixed points), the camera three-quarter front and close, the bus never between the lens and
him: two gendarmes on motorbikes, a blue beacon each, one thumbs-up; a village waving flags behind him; the minister pins a number on his chest;
the peloton banks off the main road after him (seen from the back of the bus); the riders crouched behind him; the yellow jersey drops out of the
sky onto his shoulders; the driver whistling (the scenery streams by), his big mirror turned to the sky and the man tiny in the rear window; a
road that zig-zags up an alp ahead of the bus and him; an Italian café front, a waiter running out with pasta; one noodle stretched like a rope
between the plate and his mouth, then it snaps; a mountain of shoes, a sole that flaps, new shoes that drop onto his feet; his calves swell like
balloons under two scientists' eyes; the bus brakes, he skids in behind it, a beard to his chest; he gets on (seen from inside); in the doorway
his ticket, LIGNE 12, the display over his head, 21 ROME; his eyes go from one to the other, then to us.
Natural look; props_bus.js (townSign, raceBib, jersey, pastaPlate, shoePile; pass 2: busPlate, busTicket, legWheel, bigCalf, beacon, noodleRope,
rearMirror, alpSlope, flapSole, newShoe, trattoria), props reused (cityBus, motorbike, bicycle, mountainRange, tapeMeasure, beardHair, floorSlab,
tree, flag, speedLines, dustPuff, signBoard, parasol, bistroTable)."""
from story_kit import *
import math

st = Story('bus', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L08', 7), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L10', 3), ('S13', 'L11', 0), ('S14', 'L12', 0),
         ('S15', 'L12', 4), ('S16', 'L13', 0), ('S17', 'L14', 0), ('S18', 'L15', 0), ('S19', 'L16', 0), ('S20', 'L17', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
DEAD = {'lid': 0.45}
FLAT = lambda t=0.0, dur=0.0: k(t, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=dur)   # his face: the same from the first shot to the last
V = 4.0                                              # his speed (m/s) where he really crosses the set (the street, the villages, the fork)
VS = 8.0                                             # (pass 2) the speed of the scenery under him where he runs on the spot (the treadmill shots)
BUS = lambda pid, pos, ry, keys=None, **o: P(pid, 'cityBus', pos=pos, ry=ry, opts={'len': 7.6, 'line': '21', 'dest': 'ROME', 'top': 3.0, **o}, **({'keys': keys} if keys else {}))   # (pass 2) top 3.0: a bus taller than the men (they stand 2.45)
PLQ = lambda pid, bus, w=1.9: P(pid, 'busPlate', on={'actor': bus, 'offset': [-3.86, 3.24, 0.0], 'rot': [0, -PI / 2, 0]}, opts={'text': '21  ROME', 'w': w, 'h': 0.44})   # (pass 2) the line and the destination, big, on the bus's back
PLQS = lambda pid, bus, x=-2.9, w=1.5, y=3.24: P(pid, 'busPlate', on={'actor': bus, 'offset': [x, y, 1.21]}, opts={'text': '21  ROME', 'w': w, 'h': 0.44})   # ...and on its flank, near the back
ROAD = lambda pid, z=0.0, w=3.4, x=0.0, ln=160.0: P(pid, 'slab', pos=[x, 0.02, z], opts={'w': ln, 'h': 0.04, 'd': w, 'color': '#8C8C88', 'noShadow': True})   # a country road along X ((stills 3) grey and flat: floorSlab is a parquet floor 0.28 thick, the roads were brown platforms)
LINE = lambda pid, z=0.0, x=0.0, ln=160.0: P(pid, 'slab', pos=[x, 0.046, z], opts={'w': ln, 'h': 0.012, 'd': 0.08, 'color': '#F2F0E8', 'noShadow': True})
TREES = lambda tag, z, x0, x1, n, s=1.2: [P(f'tr{tag}{i}', 'tree', pos=[r(x0 + (x1 - x0) * i / max(1, n - 1)), 0, r(z + 0.6 * ((i * 37) % 7 - 3) / 3)], scale=r(s * (0.85 + 0.3 * ((i * 53) % 5) / 4))) for i in range(n)]
RUNK = lambda p1, dur, t0=0.0, speed=1.6: [k(t0, to=p1, dur=dur, clip='run', ease='linear'), k(t0, clip='run', speed=speed)]   # legs fast: a blur
MJ = lambda pid: P(pid, 'jersey', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'w': 0.5, 'h': 0.62, 'd': 0.3})   # the yellow jersey from S10 on
PANT = lambda t0, n=4: [k(r(t0 + 0.22 * j), toon={'sq': [1.03, 0.96, 1.03] if j % 2 == 0 else [0.99, 1.02, 0.99], 'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.1) for j in range(n)]
def scroll(ps, D, v=None):
    """(pass 2) the treadmill: the scenery slides back along X under a hero who runs on the spot (the camera travels with him), v m/s"""
    v = VS if v is None else v
    for p in ps: p['keys'] = [*p.get('keys', []), k(0.0, to=[r(p['pos'][0] - v * D), p['pos'][1], p['pos'][2]], dur=D, ease='linear')]
    return ps
DASH = lambda tag, D, z=0.0, v=None, x0=-9.0, n=14, gap=3.2: scroll([P(f'ds{tag}{i}', 'slab', pos=[r(x0 + gap * i), 0.046, z], opts={'w': 1.5, 'h': 0.012, 'd': 0.1, 'color': '#F2F0E8', 'noShadow': True}) for i in range(n)], D, v)
STREAK = lambda pid, pos, n=6, ln=1.6, w=1.3, **o: P(pid, 'speedLines', pos=pos, face='camera', opts={'n': n, 'len': ln, 'w': w, 'soft': True, 'alpha': 0.8, **o})   # speed streaks behind him
DUST = lambda tag, x=0.0, z=0.0: [P(f'pous{tag}a', 'dustPuff', pos=[r(x - 0.6), 0.0, z], scale=0.5, opts={'period': 0.3, 'color': '#E9E2D2'}), P(f'pous{tag}b', 'dustPuff', pos=[r(x - 1.7), 0.0, z], scale=0.75, opts={'period': 0.45, 'color': '#E9E2D2', 'seed': 11})]   # a dust trail at his heels
WHEEL = lambda pid, at_=None, **o: P(pid, 'legWheel', on={'actor': 'mec', 'joint': 'hips', 'offset': [0.0, -0.5, 0.0], 'face': 'camera'}, opts={'r': 0.6, **({'at': at_} if at_ else {}), **o})   # (pass 2) the wheel of legs

for g_ in [('S01', 1.6, 'mec', 'hook'), ('S02', 0.6, 'mec', 'windup'), ('S07', 1.2, 'mec', 'bib'), ('S10', 0.8, 'mec', 'jersey'), ('S15', 0.7, 'mec', 'slurp'), ('S17', 1.1, 'mec', 'calves'), ('S20', 1.4, 'mec', 'end')]:
    st.gag(*g_)
st.card('S10', 'JAUNE', at=0.55)
st.card('S16', 'USÉES', at=0.5)
st.card('S20', 'RATÉ', at=0.75)

# 1: the hook. (pass 2) His face first: he sprints up the kerb toward us to the stop (the plate: 12) as the bus pulls out the other way behind him,
#    skids, looks round at it going (21 ROME on its back, the whole bus in the street behind him), then at us, deadpan, panting
D1 = st.dur('S01'); ME1 = [5.2, 0, 0.3]; ARR1 = 0.42
st.shot('S01', 'parisStreet', setOpts={'clear': [-14.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', [5.2, 0, -2.3], 0, 'run', 'determined', params={'bounce': 0.4}, keys=[*RUNK([5.2, 0, -0.3], ARR1, 0.0, 2.2), k(ARR1, clip='heelBrake'), k(ARR1, to=ME1, dur=0.3, ease='out', face='keep'),
            k(ARR1, toon={'lay': [-0.2, 0.0], 'sq': [1.06, 0.94, 1.06], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'open'}}, toonDur=0.08, toonEase='out'),
            k(r(ARR1 + 0.3), clip='stand'), k(r(ARR1 + 0.3), toon={'lay': [0.0, 0.0], 'face': {'lid': 0.2, 'mouth': 'open'}}, toonDur=0.15),
            k(r(ARR1 + 0.32), look=[3.5, 1.9, -16.0], lookDur=0.14), k(1.42, look='camera', lookDur=0.16), FLAT(1.5, 0.12), *PANT(1.66, 2),
            k(2.08, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06), FLAT(2.18, 0.07)])],   # the bus behind him... then us; one blink
        props=[BUS('bus1', [3.5, 0, -4.0], 90, keys=[k(0.0, to=[3.5, 0, -30.0], dur=D1, ease='in')], doors=[[0.0, 0.3], [0.2, 0.0]]), PLQ('plq1', 'bus1'),
               P('ligne1', 'signBoard', pos=[5.95, 0, -0.5], opts={'text': '12', 'bg': '#2F62B5', 'fg': '#FFFFFF', 'w': 0.62, 'h': 0.5, 'height': 2.95, 'posts': True}),
               P('dust1', 'dustPuff', pos=[5.2, 0.0, 0.1], scale=0.6, opts={'once': True, 'startAt': ARR1, 'period': 0.5, 'color': '#EFE8D8'})],
        cams=[FC(0.0, [4.9, 1.45, 5.2], [[ME1[0], 2.5, ME1[2]], [ME1[0], 0.0, ME1[2]], [6.3, 3.5, -0.5], [2.5, 1.8, -8.0]], top=0.1, bottom=0.76)])
st.cue('sfx:stepSoft', 'S01', 0.15, 0.15); st.cue('sfx:stepSoft', 'S01', 0.4, 0.15); st.cue('sfx:brake', 'S01', ARR1, 0.3); st.cue('engine', 'S01', 0.1, 0.35)

# 2: so he ran after it. (pass 2) Side on, half the height of the frame: leaning in on the spot, his legs a wheel under a still body, dust spinning
#    up; a crouch, a tall stretch, and he is gone to the right in a smear; the puff hangs to the cut
D2 = st.dur('S02'); GO2 = 1.26; ME2 = [3.6, 0, 1.0]; F2 = {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}
st.shot('S02', 'parisStreet', setOpts={'clear': [-14.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', ME2, 180, 'run', 'determined', params={'bounce': 0.0}, keys=[k(0.0, clip='run', speed=2.6), k(0.0, look=[3.6, 1.9, -12.0]), k(0.0, toon={'lay': [0.2, 0.0], 'face': F2}, toonDur=0.0),
            k(r(GO2 - 0.16), toon={'lay': [-0.1, 0.0], 'sq': [1.18, 0.78, 1.18], 'face': F2}, toonDur=0.12, toonEase='out'),
            k(GO2, toon={'lay': [0.3, 0.0], 'sq': [0.8, 1.25, 0.8], 'face': F2}, toonDur=0.05, toonEase='out'),
            k(r(GO2 + 0.06), toon={'lay': [0.35, 0.0], 'sq': [0.85, 0.92, 2.2], 'face': F2}, toonDur=0.05), k(r(GO2 + 0.04), to=[3.6, 0, -16.0], dur=0.22, ease='in')])],   # the crouch, the stretch... and the smear
        props=[WHEEL('roue2', [0.0, r(GO2 + 0.12)]), P('dust2', 'dustPuff', pos=[ME2[0], 0.0, r(ME2[2] + 0.3)], scale=0.7, opts={'period': 0.3, 'color': '#EFE8D8'}, keys=[k(r(GO2 + 0.2), visible=False)]),
               P('puff2', 'dustPuff', pos=[ME2[0], 0.0, r(ME2[2] - 0.3)], scale=1.3, opts={'once': True, 'startAt': GO2, 'period': 0.7, 'color': '#EFE8D8'}),
               STREAK('sl2', [3.6, 1.4, -0.8], at=[[r(GO2 + 0.04), D2]])],
        cams=[FC(0.0, [9.5, 1.35, -3.4], [[ME2[0], 2.5, ME2[2]], [ME2[0], 0.0, ME2[2]], [ME2[0], 1.2, 0.0], [ME2[0], 1.2, 2.0]], top=0.24, bottom=0.74, inside=(5.3, 9.8, 0.3, 4.0, -200.0, 200.0))])   # (stills 3) more from the front, him in the middle (the wheel was cut by the left edge)
st.cue('sfx:rattle', 'S02', 0.05, 0.3); st.cue('whoosh', 'S02', GO2, 0.4)

# 3: he never stopped. (pass 2) From the pavement, travelling with him left to right: the wheel of legs under a steady torso, his face deadpan, a
#    glance at us; the back of the bus (21 ROME) just ahead; streaks and dust behind him
D3 = st.dur('S03'); Z3 = 2.0; V3 = 7.0
st.shot('S03', 'parisStreet', setOpts={'clear': [-40.0, 30.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [3.6, 0, Z3], 180, 'run', 'determined', params={'bounce': 0.0},
            keys=[*RUNK([3.6, 0, r(Z3 - V3 * D3)], D3, 0.0, 2.6), k(0.0, look=[3.6, 1.9, -60.0]), FLAT(), k(0.75, look='camera', lookDur=0.14), k(1.2, look=[3.6, 1.9, -60.0], lookDur=0.14)])],
        props=[BUS('bus3', [3.5, 0, r(Z3 - 5.6)], 90, keys=[k(0.0, to=[3.5, 0, r(Z3 - 5.6 - V3 * D3)], dur=D3, ease='linear')]), PLQS('plq3', 'bus3', y=0.78), PLQ('plq3b', 'bus3'), WHEEL('roue3'),
               P('sl3', 'speedLines', on={'actor': 'mec', 'joint': 'hips', 'offset': [0.0, 0.35, -1.5], 'face': 'camera'}, opts={'n': 6, 'len': 1.6, 'w': 1.3, 'soft': True, 'alpha': 0.8}),
               P('dust3', 'dustPuff', on={'actor': 'mec', 'joint': 'hips', 'offset': [0.0, -1.0, -0.8]}, scale=0.5, opts={'period': 0.3, 'color': '#EFE8D8'})],
        cams=[FC(0.0, [9.6, 1.3, r(Z3 - 4.5)], [[3.6, 2.5, Z3], [3.6, 0.0, Z3], [4.7, 1.2, r(Z3 - 2.3)]], top=0.2, bottom=0.76, drift=(0.0, 0.0, r(-V3 * D3)), inside=(5.3, 9.8, 0.3, 4.0, -200.0, 200.0))])   # (stills 3) three-quarter front (in profile his box head has no face)
st.cue('engine', 'S03', 0.0, 0.3); st.cue('sfx:stepSoft', 'S03', 0.3, 0.15); st.cue('sfx:stepSoft', 'S03', 0.6, 0.15); st.cue('sfx:stepSoft', 'S03', 0.9, 0.15)

# 4: after an hour he had left the town. The road out of town: the town sign crossed out (SAINT-ARRÊT); the bus goes by it, then him; the last houses
D4 = st.dur('S04'); SG4 = [0.0, 0, 2.2]; B4 = 5.2
st.shot('S04', 'grassland', actors=[act('mec', [r(-B4 - 4.0), 0, 0.3], 90, 'run', 'determined', keys=[*RUNK([r(-B4 - 4.0 + V * D4), 0, 0.3], D4, 0.0, 2.0)])],
        props=[ROAD('road4'), LINE('line4'), BUS('bus4', [-4.0, 0, -0.3], 0, keys=[k(0.0, to=[r(-4.0 + V * D4), 0, -0.3], dur=D4, ease='linear')]), PLQ('plq4', 'bus4'),
               P('panneau4', 'townSign', pos=SG4, ry=-15, opts={'name': 'SAINT-ARRÊT', 'exit': True, 'w': 1.5, 'h': 1.4}),
               *[P(f'mais4{j}', 'cottage', pos=[r(-16.0 - 7.0 * j), 0, r(-7.0 + 3.0 * (j % 2))], ry=r(20 * j)) for j in range(3)], *TREES('4', -6.5, -14.0, 14.0, 6)],
        cams=[FC(0.0, [3.6, 1.2, 7.5], [[SG4[0], 2.2, SG4[2]], [SG4[0], 0.0, SG4[2]], [r(-B4 - 4.0 + V * D4 * 0.7), 2.4, 0.3], [r(-4.0 + V * D4 * 0.4), 3.5, -0.3]], top=0.16, bottom=0.78)])
st.cue('engine', 'S04', 0.0, 0.3); st.cue('whoosh', 'S04', 0.5, 0.25)

# 5: the gendarmes escorted him on motorbikes. (pass 2) Three-quarter front, the road streaming back: he runs between two gendarmes sitting on big
#    motorbikes, their hands on the bars, a small blue beacon turning on each (no light on the road); the near one looks at us, then a thumbs-up
#    by his face
D5 = st.dur('S05'); MS5 = 1.7; G5 = [('gend1', -0.95, -0.35), ('gend2', 0.95, -0.75)]
st.shot('S05', 'grassland', actors=[act('mec', [0, 0, 0], 90, 'run', 'determined', params={'bounce': 0.5}, keys=[k(0.0, clip='run', speed=2.2), k(0.0, look=[12.0, 1.9, 0.0]), FLAT()]),
        *[act(g_, [r(gx - 0.27), 0.57, gz], 90, 'ride', 'determined', params={'cadence': 0.0, 'lean': 0.3}, keys=[k(0.0, look=[12.0, 2.2, gz]),
            *([k(0.7, look='camera', lookDur=0.15), k(0.95, toon={'reach': {'R': [r(gx + 0.4), 2.05, r(gz + 0.5), 1, 0.04]}, 'hands': {'R': 'thumbUp'}, 'face': {'lid': 0.2, 'mouth': 'smirk'}}, toonDur=0.14, toonEase='out')] if gz > 0 else [])]) for g_, gz, gx in G5]],
        props=[ROAD('road5'), *DASH('5', D5), *scroll(TREES('5', -6.5, -10.0, 26.0, 9), D5),
               *[P(f'moto5{j}', 'motorbike', pos=[gx, 0, gz], scale=MS5, opts={'color': '#2F4A8A', 'roll': 40}) for j, (_, gz, gx) in enumerate(G5)],
               *[P(f'gyro5{j}', 'beacon', on={'actor': g_, 'joint': 'head', 'offset': [0.0, 0.52, -0.02]}, opts={'r': 0.09, 'rate': 2.0, 'phase': 2.0 * j}) for j, (g_, _, _) in enumerate(G5)],
               STREAK('sl5', [-2.4, 1.5, 0.3]), *DUST('5')],
        cams=[FC(0.0, [5.6, 1.3, 1.7], [[0, 2.5, 0], [0, 0.0, 0], [-0.35, 2.8, -0.95], [-0.75, 2.8, 0.95], [-0.9, 0.2, 1.4], [-0.5, 0.2, -1.4]], top=0.14, bottom=0.76)])   # (stills 3) more from the front and closer (three small figures in a wide field)
st.cue('sfx:siren', 'S05', 0.0, 0.25); st.cue('engine', 'S05', 0.1, 0.3)

# 6: the villages cheered him from the roadside. (pass 2) Low on the road ahead of him, travelling: he fills half the frame, deadpan, a glance at
#    us; behind him the villagers along the verge wave flags and arms, a kid jumps, the cottages beyond
D6 = st.dur('S06'); X6 = -1.5; Z6 = 1.3; FANS6 = [('fan1', -5.0, 0.9), ('fan2', -2.6, 0.62), ('fan3', -0.2, 1.0), ('fan4', 2.2, 1.0), ('fan5', 4.6, 1.0)]
st.shot('S06', 'cottageStreet', setOpts={'roadColor': '#8C8C88'}, actors=[act('mec', [X6, 0, Z6], 90, 'run', 'determined', keys=[*RUNK([r(X6 + V * D6), 0, Z6], D6, 0.0, 2.0), FLAT(), k(0.9, look='camera', lookDur=0.15), k(1.6, look=[40.0, 1.9, Z6], lookDur=0.15)]),
        *[act(fid, [fx, 0, -0.9], 0, 'stand', 'happy', keys=[k(0.0, look=[X6, 1.9, Z6]), k(r(D6 * 0.4), look=[r(X6 + V * D6), 1.9, Z6], lookDur=0.8), *[k(r(0.1 + 0.18 * i + 0.05 * j), toon={'reach': {'R': [r(fx + (0.14 if i % 2 else -0.14)), r(2.95 * fh), -0.6, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.08) for i in range(12)]] +
              ([k(0.3, to=[fx, 0.4, -0.9], dur=0.15, ease='out'), k(0.45, to=[fx, 0, -0.9], dur=0.15, ease='in'), k(0.9, to=[fx, 0.4, -0.9], dur=0.15, ease='out'), k(1.05, to=[fx, 0, -0.9], dur=0.15, ease='in'), k(1.5, to=[fx, 0.4, -0.9], dur=0.15, ease='out'), k(1.65, to=[fx, 0, -0.9], dur=0.15, ease='in')] if j == 1 else [])) for j, (fid, fx, fh) in enumerate(FANS6)]],
        props=[*[P(f'drap6{j}', 'flag', on={'actor': FANS6[j][0], 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=0.45, opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A']}) for j in (0, 2, 4)]],
        cams=[FC(0.0, [r(X6 + 5.0), 1.25, r(Z6 + 2.3)], [[X6, 2.5, Z6], [X6, 0.0, Z6], [r(X6 - 1.8), 2.6, -0.9], [r(X6 + 0.7), 1.2, r(Z6 + 0.7)]], top=0.14, bottom=0.76, drift=(r(V * D6), 0.0, 0.0))])
st.cue('sfx:fanfare', 'S06', 0.1, 0.35)

# 7: the ministry of sport gave him a race number. (pass 2) Three-quarter front, on the spot, the road streaming: the minister in a tracksuit
#    jogs half-turned beside him and pins a number on his chest; he does not look; the minister looks at us, then a thumbs-up by his face
D7 = st.dur('S07'); PIN7 = 0.9; MN7 = [0.75, 0, -0.85]
MP7 = lambda l, rr, f: {'reach': {'L': l + [1, 0.04], 'R': rr + [1, 0.04]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': f}
st.shot('S07', 'grassland', actors=[act('mec', [0, 0, 0], 90, 'run', 'determined', params={'bounce': 0.4}, keys=[k(0.0, clip='run', speed=2.0), k(0.0, look=[12.0, 1.9, 0.0]), FLAT(),
            k(r(PIN7 + 0.02), toon={'sq': [1.05, 0.95, 1.05], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.04), FLAT(r(PIN7 + 0.14), 0.1)]),
        act('ministre', MN7, -40, 'run', 'happy', keys=[k(0.0, clip='run', speed=1.8), k(0.0, look=[0.25, 1.5, 0.1]),
            k(0.0, toon=MP7([0.45, 1.78, -0.3], [0.3, 1.6, -0.25], {'lid': 0.2, 'mouth': 'smirk'}), toonDur=0.0),
            k(r(PIN7 - 0.25), toon=MP7([0.36, 1.56, 0.1], [0.22, 1.36, 0.14], {'lid': 0.2, 'mouth': 'smirk'}), toonDur=0.22, toonEase='inOut'),
            k(r(PIN7 + 0.2), toon={'face': {'lid': 0.1, 'mouth': 'bigsmile'}}, toonDur=0.15), k(r(PIN7 + 0.35), look='camera', lookDur=0.15),
            k(r(PIN7 + 0.65), toon={'reach': {'R': [1.25, 1.95, -0.35, 1, 0.04]}, 'hands': {'R': 'thumbUp'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.14, toonEase='out')])],
        props=[ROAD('road7'), *DASH('7', D7), *scroll(TREES('7', -6.5, -10.0, 28.0, 9), D7), STREAK('sl7', [-2.2, 1.5, 0.3]), *DUST('7'),
               P('dos7a', 'raceBib', pos=[0.38, 1.7, -0.27], face='camera', scale=1.5, opts={'num': '1'}, keys=[k(r(PIN7 - 0.25), to=[0.3, 1.42, 0.2], dur=0.22, ease='inOut'), k(PIN7, visible=False)]),
               P('dos7', 'raceBib', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.3, 0.175]}, scale=1.5, opts={'num': '1'}, keys=[k(0.0, visible=False), k(PIN7, visible=True), k(PIN7, squash=[1.3, 1.3, 1.0], dur=0.25)])],
        cams=[FC(0.0, [4.4, 1.5, 3.3], [[0, 2.5, 0], [0, 0.95, 0], [MN7[0], 2.5, MN7[2]], [1.35, 2.0, -0.4], [-0.6, 1.5, 0.3]], top=0.14, bottom=0.76)])
st.cue('sfx:click', 'S07', PIN7, 0.25)

# 8: the cycle race changed its route... (pass 2) From the back of the bus, looking down the road behind: he runs after us, big in the frame; behind
#    him the fork: the sign points along the main road (ARRIVÉE), and the peloton banks off it into our road, after him
D8 = st.dur('S08'); RID8 = ['#E0413A', '#2F62B5', '#F2C94E', '#2F8F6B', '#8E5AA8', '#E0813A']; F8 = -6.0; X8 = -1.0; VP8 = 7.0; HM8 = (0.866, -0.5)
def rider(aid, x, z, ry, col, keys=None, bike_keys=None, params=None):
    a = ry * PI / 180
    return (act(aid, [r(x - 0.16 * math.sin(a)), 0.5, r(z - 0.16 * math.cos(a))], ry, 'ride', 'determined', keys=keys or [], params=params or {'cadence': 1.8, 'lean': 0.8}),
            P(f'bk_{aid}', 'bicycle', pos=[x, 0, z], rot=[0, r(a - PI / 2), 0], opts={'color': col}, **({'keys': bike_keys} if bike_keys else {})))
R8 = []
for j in range(6):
    s8 = 5.0 + 1.7 * (j // 2); oz = -0.5 + 1.0 * (j % 2); t1 = r(s8 / VP8, 2); x2 = r(F8 + VP8 * (D8 - t1))
    R8 += rider(f'cyc{j + 1}', r(F8 - s8 * HM8[0]), r(oz - s8 * HM8[1]), 120, RID8[j], params={'cadence': 2.4, 'lean': 0.9},
                keys=[k(0.0, to=[r(F8 - 0.16), 0.5, oz], dur=t1, ease='linear'), k(t1, to=[r(x2 - 0.16), 0.5, oz], dur=r(D8 - t1), ease='linear'),
                      k(r(t1 - 0.3), toon={'lay': [0.0, 0.3]}, toonDur=0.25), k(r(t1 + 0.25), toon={'lay': [0.0, 0.0]}, toonDur=0.3)],
                bike_keys=[k(0.0, to=[F8, 0, oz], dur=t1, ease='linear'), k(t1, to=[x2, 0, oz], dur=r(D8 - t1), ease='linear'),
                           k(r(t1 - 0.3), rotTo=[0.3, 0.26, 0.0], dur=0.3), k(t1, rotTo=[0.18, 0.0, 0.0], dur=0.2), k(r(t1 + 0.25), rotTo=[0.0, 0.0, 0.0], dur=0.3)])
st.shot('S08', 'grassland', actors=[act('mec', [X8, 0, 0], 90, 'run', 'determined', keys=[*RUNK([r(X8 + V * D8), 0, 0], D8, 0.0, 2.0), FLAT()]), *[x for x in R8 if x.get('clip') == 'ride']],
        props=[P('road8a', 'slab', pos=[F8, 0.016, 0.0], ry=30, opts={'w': 80.0, 'h': 0.04, 'd': 3.4, 'color': '#8C8C88', 'noShadow': True}), ROAD('road8b', 0.0, 3.4, 17.0, 46.0), LINE('line8', 0.0, 17.0, 46.0),
               *[x for x in R8 if x.get('name') == 'bicycle'],
               P('fl8', 'signBoard', pos=[-4.5, 0, 3.0], ry=90, opts={'text': 'ARRIVÉE →', 'bg': '#F4F4F0', 'fg': '#2F62B5', 'w': 2.2, 'h': 0.62, 'height': 1.7}),
               *TREES('8', 9.0, -30.0, 6.0, 6), *TREES('8b', -10.0, -24.0, 14.0, 6)],
        cams=[FC(0.0, [r(X8 + 6.2), 3.0, -1.3], [[X8, 2.5, 0], [X8, 0.0, 0], [-4.5, 2.6, 3.0], [-12.0, 2.0, 3.8]], top=0.14, bottom=0.76, drift=(r(V * D8), 0.0, 0.0))])
st.cue('sfx:bell', 'S08', 0.2, 0.2); st.cue('whoosh', 'S08', 0.5, 0.25)

# 9: ...to follow him. (pass 2) Low, three-quarter front, the road streaming: he leads, deadpan, a glance at us; right behind him the riders in a
#    tight bunch, crouched on their bars, pedalling flat out
D9 = st.dur('S09')
R9 = [x for j in range(6) for x in rider(f'cyc{j + 1}', r(-1.7 - 1.15 * (j // 2)), r(-0.5 + 1.0 * (j % 2)), 90, RID8[j], params={'cadence': 2.6, 'lean': 0.95})]
st.shot('S09', 'grassland', actors=[act('mec', [0, 0, 0], 90, 'run', 'determined', params={'bounce': 0.5}, keys=[k(0.0, clip='run', speed=2.2), k(0.0, look=[12.0, 1.9, 0.0]), FLAT(), k(0.45, look='camera', lookDur=0.15)]), *[x for x in R9 if x.get('clip') == 'ride']],
        props=[ROAD('road9'), *DASH('9', D9), *[x for x in R9 if x.get('name') == 'bicycle'], *scroll(TREES('9', -6.5, -12.0, 20.0, 8), D9), STREAK('sl9', [-5.4, 1.4, 0.6], n=7, ln=1.8), *DUST('9')],
        cams=[FC(0.0, [4.4, 0.75, 2.9], [[0, 2.5, 0], [0, 0.0, 0], [0.8, 1.5, 0.3], [-4.0, 2.3, 0.5], [-1.7, 2.3, -0.5]], top=0.14, bottom=0.76)])
st.cue('sfx:bell', 'S09', 0.3, 0.15)

# 10: they threw him the yellow jersey. (pass 2) Low, three-quarter front, his shoulders against the sky: a spectator on the verge slides away
#     behind, waving; the jersey tumbles down out of the sky and drops onto him, squashing on his shoulders; he runs on in it, deadpan (JAUNE)
D10 = st.dur('S10'); ON10 = 0.5
st.shot('S10', 'grassland', actors=[act('mec', [0, 0, 0], 90, 'run', 'determined', params={'bounce': 0.4}, keys=[k(0.0, clip='run', speed=2.0), k(0.0, look=[12.0, 1.9, 0.0]), FLAT(),
            k(ON10, toon={'sq': [1.14, 0.84, 1.14], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.05, toonEase='out'), k(r(ON10 + 0.16), toon={'sq': [0.96, 1.05, 0.96], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1), FLAT(r(ON10 + 0.3), 0.12)]),
        act('lanceur', [-0.5, 0, -2.4], 20, 'wave', 'happy', keys=[k(0.0, to=[r(-0.5 - VS * D10), 0, -2.4], dur=D10, ease='linear', face='keep', glide=True), k(0.0, look=[0.0, 2.0, 0.0]), k(0.0, toon={'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.0)])],
        props=[ROAD('road10'), *DASH('10', D10), *scroll(TREES('10', -6.5, -10.0, 26.0, 9), D10), STREAK('sl10', [-2.2, 1.5, 0.3]), *DUST('10'),
               P('mj10a', 'jersey', pos=[-1.9, 4.3, -1.2], rot=[0.4, 0.0, 0.9], scale=0.9, keys=[k(0.0, to=[0.12, 3.1, 0.0], dur=r(ON10 - 0.12), ease='inOut', arc=0.4), k(0.0, rotTo=[0.0, 1.57, 0.0], dur=r(ON10 - 0.12)), k(r(ON10 - 0.12), visible=False)]),   # it tumbles down...
               P('mj10', 'jersey', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'at': r(ON10 - 0.12), 'w': 0.5, 'h': 0.62, 'd': 0.3})],   # ...and drops onto him
        cams=[FC(0.0, [3.8, 1.0, 2.8], [[0, 3.2, 0], [0, 0.5, 0], [0.3, 2.5, 0.0]], top=0.22, bottom=0.76)])
st.cue('whoosh', 'S10', 0.15, 0.25); st.cue('thud', 'S10', ON10, 0.25); st.cue('sfx:fanfare', 'S10', r(ON10 + 0.1), 0.2)

# 11: the driver, though... Inside the bus, behind the driver: his cap, his arms on the big wheel, whistling; (pass 2) the road and the trees
#     stream toward us through the windscreen
D11 = st.dur('S11')
st.shot('S11', 'grassland', actors=[act('chauffeur', [2.75, 0.45, -0.5], 90, 'drive', 'neutral', keys=[k(0.0, look=[12.0, 2.2, -0.5]), *[k(r(0.1 + 0.2 * j), toon={'face': {'lid': 0.3, 'mouth': 'whistle'}, 'sq': [1.0, 1.02 if j % 2 else 0.99, 1.0]}, toonDur=0.1) for j in range(5)]])],
        props=[ROAD('road11'), *DASH('11', D11, x0=2.0, n=18), BUS('bus11', [0.0, 0, 0.0], 0), *scroll(TREES('11', -5.0, 8.0, 64.0, 10), D11), *scroll(TREES('11b', 5.0, 10.0, 66.0, 10), D11)],
        cams=[cam(0.0, [1.1, 2.55, -0.15], [1.1, 2.55, -0.15], [3.8, 1.9, -0.45], lens=60)])   # (stills 3) over his shoulder from the aisle: his cap, the wheel, the whole windscreen (a pole stood across the lens)
st.cue('sfx:whistle', 'S11', 0.15, 0.2)

# 12: ...never looked in his mirror. (pass 2) From in front of the windscreen (clear glass): the driver whistling, his eyes on the road; over the
#     dashboard his big mirror, turned to the sky; far behind, through the rear window, the man in yellow, tiny, running
D12 = st.dur('S12')
st.shot('S12', 'grassland', actors=[act('chauffeur', [2.75, 0.45, -0.5], 90, 'drive', 'neutral', keys=[k(0.0, look=[30.0, 2.2, -0.5]), *[k(r(0.1 + 0.2 * j), toon={'face': {'lid': 0.35, 'mouth': 'whistle'}}, toonDur=0.1) for j in range(10)]]),
        act('mec', [-17.0, 0, -0.6], 90, 'run', 'determined', keys=[k(0.0, clip='run', speed=2.0)])],
        props=[MJ('mjr12'), ROAD('road12'), *DASH('12', D12, x0=-40.0, n=24), BUS('bus12', [0.0, 0, 0.0], 0, glass=0.04), P('retro12', 'rearMirror', pos=[3.35, 2.98, 0.25], ry=100, opts={'w': 0.62, 'h': 0.3}),
               *scroll(TREES('12', -6.0, -40.0, 30.0, 12), D12), *scroll(TREES('12b', 6.5, -36.0, 34.0, 12), D12)],
        cams=[cam(0.0, [5.7, 2.35, 0.35], [5.62, 2.35, 0.35], [1.76, 2.3, -0.31], lens=50)])
st.cue('sfx:whistle', 'S12', 0.1, 0.2); st.cue('engine', 'S12', 0.0, 0.25)

# 13: they crossed the Alps. (pass 2) Low behind him, looking up the road: he runs in yellow a constant gap behind the bus (21 ROME over his
#     head); beyond them the road zig-zags up an alp to the snow, the peaks at the top of the frame
D13 = st.dur('S13')
st.shot('S13', 'grassland', actors=[act('mec', [-1.2, 0, 0.0], 90, 'run', 'determined', params={'bounce': 0.5}, keys=[k(0.0, clip='run', speed=2.0)])],
        props=[MJ('mjr13'), P('alpes13', 'mountainRange', pos=[58.0, 16.0, 0.0], ry=-90, opts={'n': 7, 'w': 110, 'h': 30, 'd': 10, 'seed': 13}), P('pente13', 'alpSlope', pos=[22.0, 0, 0.0], ry=-90, opts={'w': 70, 'up': 46, 'slope': 0.6, 'legs': 5}),
               ROAD('road13', 0.0, 3.4, 2.0, 40.0), *DASH('13', D13, x0=-16.0, n=14), BUS('bus13', [5.4, 0, 0.0], 0), PLQ('plq13', 'bus13'),
               *scroll([P(f'sapin13{j}', 'tree', pos=[r(-14.0 + 4.6 * j), 0, r(4.6 + 1.2 * (j % 2)) if j % 2 else r(-4.6 - 1.2 * (j % 3))], scale=1.5, opts={'kind': 'pine'}) for j in range(9)], D13, 5.0), *DUST('13', -1.2)],
        cams=[cam(0.0, [-4.8, 0.4, 1.0], [-4.8, 0.4, 1.0], [10.0, 3.0, -0.2], lens=62)])   # (stills 3) lower and closer, looking up: him half the frame, the peaks over the bus
st.cue('engine', 'S13', 0.0, 0.25); st.cue('gust', 'S13', 0.2, 0.2)

# 14: in Italy a waiter... (pass 2) A warm village street, an ochre café front with a red and white striped awning: he runs by, big in the frame;
#     behind him the waiter dashes out from under the awning with a plate of spaghetti held high
D14 = st.dur('S14'); X14 = -1.6; Z14 = 1.3
IT14 = [{'x': -7.2, 'color': '#E9B569', 'roof': '#B5522F', 'door': '#6B3F26', 'shutters': '#2E7D4F'}, {'x': 1.6, 'color': '#E8946A', 'roof': '#A8452C', 'door': '#2E7D4F'}, {'x': 9.6, 'color': '#F0D08A', 'roof': '#B5522F', 'door': '#6B3F26'},
        {'x': -15.4, 'color': '#E7A77A', 'roof': '#A8452C'}, {'x': 17.6, 'color': '#F2DFA6', 'roof': '#B5522F'}, {'x': -23.6, 'color': '#E9B569', 'roof': '#B5522F'}, {'x': 25.6, 'color': '#E8946A', 'roof': '#A8452C'}]
st.shot('S14', 'cottageStreet', setOpts={'seed': 23, 'roadColor': '#8C8C88', 'houses': IT14}, actors=[act('serveur', [-0.4, 0, -2.3], 40, 'run', 'happy', keys=[k(0.0, to=[1.7, 0, 0.7], dur=r(D14 - 0.1), clip='run', ease='linear'),
            k(0.0, toon={'reach': {'R': [-0.1, 2.7, -2.0, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.0),
            k(0.0, toon={'reach': {'R': [2.0, 2.7, 1.0, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=r(D14 - 0.1), toonEase='linear'), k(0.0, look=[4.0, 1.9, Z14])]),   # (stills 3) the plate held up travels with him (aimed at one far point his arm was a pole)
        act('mec', [X14, 0, Z14], 90, 'run', 'determined', keys=[*RUNK([r(X14 + V * D14), 0, Z14], D14, 0.0, 2.0), FLAT(), k(0.7, look='camera', lookDur=0.15)])],
        props=[MJ('mjr14'), P('caffe14', 'trattoria', pos=[-0.4, 0, -2.75]), P('pates14', 'pastaPlate', on={'actor': 'serveur', 'hand': 'R', 'offset': [0.0, 0.05, 0.0]}, scale=1.6),
               P('tab14', 'bistroTable', pos=[1.6, 0, -1.6], opts={'r': 0.35, 'h': 0.75}), P('para14', 'parasol', pos=[3.9, 0, -1.5], opts={'openAt': -1.0, 'colors': ['#2E9A4A', '#F4F4F0', '#D23A2E']}),
               P('it14', 'flag', pos=[-3.9, 0, -1.2], opts={'colors': ['#2E9A4A', '#F4F4F0', '#D23A2E'], 'vertical': True})],
        cams=[FC(0.0, [r(X14 + 4.8), 1.3, r(Z14 + 2.6)], [[X14, 2.5, Z14], [X14, 0.0, Z14], [r(X14 + 0.8), 1.2, r(Z14 + 0.6)], [-0.4, 4.5, -2.75], [-2.2, 2.9, -1.2]], top=0.12, bottom=0.76, drift=(r(V * D14), 0.0, 0.0))])
st.cue('sfx:bell', 'S14', 0.05, 0.15)

# 15: ...held out pasta to him on the run. (pass 2) A two-shot from the roadside at chest height, the road streaming: the waiter runs backwards in
#     front of him, the plate between them; one noodle flies up to his mouth and stretches, a thick yellow rope, trembling; it snaps off the plate
#     and whips in; he has not broken step
D15 = st.dur('S15'); N15 = [0.25, 0.4, 0.95]; PL15 = [1.2, 1.56, -0.2]; MO15 = [0.47, 1.78, -0.1]
WP15 = lambda p, f, **o: {'reach': {'R': p + [1, 0.04]}, 'hands': {'R': 'open'}, 'face': f, **o}
st.shot('S15', 'grassland', actors=[act('mec', [0, 0, 0], 90, 'run', 'determined', params={'bounce': 0.3}, keys=[k(0.0, clip='run', speed=2.0), k(0.0, look=[12.0, 1.9, 0.0]), FLAT(),
            k(N15[0], toon={'face': {'lid': 0.4, 'mouth': 'kiss', 'cheeks': 0.6}}, toonDur=0.08), k(N15[2], toon={'sq': [1.06, 0.94, 1.06], 'face': {'lid': 0.0, 'eye': 0.2, 'mouth': 'kiss', 'cheeks': 1.0}}, toonDur=0.06, toonEase='out'),
            k(r(N15[2] + 0.22), toon={'face': {'lid': 0.45, 'mouth': 'line', 'cheeks': 0.5}}, toonDur=0.12), FLAT(r(N15[2] + 0.5), 0.15)]),
        act('serveur', [2.05, 0, -0.35], -90, 'run', 'happy', keys=[k(0.0, clip='run', speed=1.8), k(0.0, look=[0.3, 2.0, 0.0]), k(0.0, toon=WP15(PL15, {'lid': 0.1, 'mouth': 'bigsmile'}), toonDur=0.0),
            k(N15[1], toon=WP15(PL15, {'lid': 0.1, 'mouth': 'bigsmile'}, lay=[-0.14, 0.0]), toonDur=0.3), k(N15[2], toon=WP15([1.5, 1.75, -0.2], {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}, sq=[0.96, 1.05, 0.96]), toonDur=0.06, toonEase='out'),
            k(r(N15[2] + 0.35), toon=WP15([1.3, 1.6, -0.2], {'lid': 0.1, 'mouth': 'bigsmile'}), toonDur=0.2)])],
        props=[MJ('mjr15'), P('pates15', 'pastaPlate', on={'actor': 'serveur', 'hand': 'R', 'offset': [0.0, 0.05, 0.0]}, scale=1.6),
               P('nouille15', 'noodleRope', pos=[PL15[0], r(PL15[1] + 0.12), PL15[2]], opts={'to': [r(MO15[0] - PL15[0]), r(MO15[1] - PL15[1] - 0.12), r(MO15[2] - PL15[2])], 'rise': N15[:2], 'snap': N15[2], 'r': 0.04}),
               ROAD('road15'), *DASH('15', D15), *scroll(TREES('15', -6.5, -10.0, 26.0, 9), D15), STREAK('sl15', [-2.0, 1.5, 0.3]), *DUST('15')],
        cams=[FC(0.0, [3.6, 1.7, 4.2], [[0, 2.5, 0], [0, 0.0, 0], [2.05, 2.5, -0.35], [2.3, 0.0, -0.35], [-0.5, 1.5, 0]], top=0.16, bottom=0.76)])   # three-quarter front on him, the waiter's back to us, the plate and the noodle between them
st.cue('sfx:slideUp', 'S15', N15[0], 0.3); st.cue('sfx:boing', 'S15', N15[2], 0.2)

# 16: he wore out four hundred pairs of shoes. (pass 2) Low, three-quarter front: behind him a mountain of worn-out shoes three times his height
#     slides by; his sole peels off and slaps at every stride; a new pair drops out of the sky onto his feet, the old one flies to the heap (USÉES)
D16 = st.dur('S16'); V16 = 3.5; PEEL16 = [0.4, 1.3]; NEW16 = 1.3
st.shot('S16', 'grassland', actors=[act('mec', [0, 0, 0.4], 90, 'run', 'determined', params={'bounce': 0.4}, keys=[k(0.0, clip='run', speed=1.6), k(0.0, look=[12.0, 1.9, 0.4]), FLAT(), k(0.7, look='camera', lookDur=0.15),
            k(NEW16, toon={'sq': [1.1, 0.9, 1.1], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.05, toonEase='out'), FLAT(r(NEW16 + 0.2), 0.12)])],
        props=[MJ('mjr16'), ROAD('road16', 0.4), *DASH('16', D16, 0.4, V16), *scroll([P('tas16', 'shoePile', pos=[-3.8, 0, 7.0], scale=2.2, opts={'n': 520, 'r': 2.0, 'h': 3.3, 'core': True})], D16, V16),
               P('semelle16', 'flapSole', on={'actor': 'mec', 'joint': 'footL', 'offset': [0.0, -0.05, 0.22]}, opts={'at': PEEL16, 'len': 0.5, 'w': 0.2}),
               *[P(f'neuve16{s}', 'newShoe', pos=[0.05, 5.4, r(0.4 + dz)], ry=90, keys=[k(r(NEW16 - 0.32), to=[0.05, 0.0, r(0.4 + dz)], dur=0.32, ease='in'), k(NEW16, squash=[1.4, 0.6, 1.4], dur=0.25), k(r(NEW16 + 0.03), attach='mec', joint=f'foot{s}', offset=[0.0, -0.13, -0.1])]) for s, dz in (('L', -0.13), ('R', 0.13))],
               P('chaus16', 'shoePile', pos=[0.0, 0.3, 0.4], scale=1.4, opts={'n': 2, 'r': 0.12, 'h': 0.1}, keys=[k(0.0, visible=False), k(NEW16, visible=True), k(NEW16, to=[-6.0, 2.6, 5.6], dur=0.45, ease='out', arc=0.8), k(r(NEW16 + 0.45), visible=False)]),
               *scroll(TREES('16', -7.0, -20.0, 10.0, 5), D16, V16), *DUST('16', 0.0, 0.4)],
        cams=[FC(0.0, [4.2, 0.9, -3.1], [[0, 2.4, 0.4], [0, 0.0, 0.4], [-7.9, 7.4, 7.0]], top=0.2, bottom=0.76)])   # from the other side of the road (S10's set-up otherwise)
st.cue('sfx:squeak', 'S16', 0.5, 0.2); st.cue('sfx:squeak', 'S16', 0.9, 0.2); st.cue('thud', 'S16', NEW16, 0.25)

# 17: scientists measured his calves. (pass 2) Low, at calf height, the road streaming: his calves swell like balloons, a tape round each; two
#     scientists in white coats bend in from either side with a tape measure, and their eyes pop
D17 = st.dur('S17'); GROW17 = [0.2, 0.6]; POP17 = 0.95
SV17 = lambda hand, hs, f: {'bend': {'spine': [0.35, 0, 0, 1, None]}, 'reach': {'R': hand + [1, 0.04]}, 'hands': {'R': hs}, 'face': f}
st.shot('S17', 'grassland', actors=[act('mec', [0, 0, 0], 90, 'run', 'determined', params={'bounce': 0.3}, keys=[k(0.0, clip='run', speed=1.0), k(0.0, look=[12.0, 1.9, 0.0]), FLAT()]),
        *[act(sid, [sx, 0, -0.9], sry, 'run', 'neutral', keys=[k(0.0, clip='run', speed=1.4), k(0.0, look=[0.0, 0.4, 0.3]),
            k(0.0, toon=SV17(hand, hs, {'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'brow': 0.8}), toonDur=0.0),
            k(r(POP17 + 0.08 * j), toon=SV17(hand, hs, {'lid': 0.0, 'eye': 0.5, 'pop': 0.9, 'popLen': 0.22, 'mouth': 'O', 'brow': 1.0}), toonDur=0.06, toonEase='out')])
          for j, (sid, sx, sry, hand, hs) in enumerate([('savant1', -0.95, 70, [-0.62, 0.5, 0.3], 'grip'), ('savant2', 1.0, -60, [0.55, 0.95, -0.2], 'point')])]],   # (stills 3) upright behind him, their faces down toward us (bent double their heads were boxes)
        props=[MJ('mjr17'), ROAD('road17'), *DASH('17', D17), *scroll(TREES('17', -6.5, -10.0, 28.0, 9), D17), *DUST('17'),
               *[P(f'mollet17{s}', 'bigCalf', on={'actor': 'mec', 'joint': f'knee{s}', 'offset': [0.0, 0.0, 0.0]}, opts={'r': 0.22, 'len': 0.5, 'tape': True, 'grow': GROW17, 'phase': ph, 'color': '#DB8F58'}) for s, ph in (('L', 0.0), ('R', 1.6))],   # bare calves, skin colour (navy on navy they were a black ball)
               P('metre17', 'tapeMeasure', pos=[-0.62, 0.46, 0.45], rot=[0, 0, -PI / 2], scale=2.0, opts={'len': [[0.0, 0.05], [GROW17[0], 0.55]]})],
        cams=[FC(0.0, [2.4, 0.45, 3.4], [[0, 2.35, 0], [0, 0.0, 0], [-0.95, 2.3, -0.9], [1.0, 2.3, -0.9], [-0.7, 0.4, 0.45], [0.6, 0.4, 0.45]], top=0.12, bottom=0.76)])
st.cue('sfx:stretch', 'S17', 0.3, 0.2); st.cue('sfx:boing', 'S17', 0.95, 0.2)

# 18: after three years the bus stopped. (pass 2) From the pavement, left to right: the bus brakes hard and stops, rocking, its back at the right
#     of the frame; he skids in behind it on his heels in the middle of the frame, smoke from his soles, his beard streaming, down to his chest
D18 = st.dur('S18'); STOP18 = 0.9
st.shot('S18', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [4.75, 0, 5.0], 180, 'run', 'determined', keys=[*RUNK([4.75, 0, 1.8], STOP18, 0.0, 2.2), k(STOP18, clip='heelBrake'), k(STOP18, to=[4.75, 0, 1.2], dur=0.35, ease='out'), k(r(STOP18 + 0.4), clip='stand'),
            k(STOP18, toon={'lay': [-0.2, 0.0], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'clench'}}, toonDur=0.06), k(r(STOP18 + 0.4), toon={'lay': [0.0, 0.0], 'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.15), *PANT(r(STOP18 + 0.62), 4), k(2.15, look='camera', lookDur=0.16)])],
        props=[MJ('mjr18'), BUS('bus18', [3.5, 0, 0.4], 90, keys=[k(0.0, to=[3.5, 0, -3.2], dur=STOP18, ease='out')], doors=[[0.0, 0.0]], rock=[[STOP18, 0.03]]), PLQ('plq18', 'bus18'), PLQS('plq18b', 'bus18', y=0.78),
               P('barbe18', 'beardHair', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.02, 0.1]}, scale=0.75, opts={'len': 1.2, 'coil': 0.0, 'depth': 0.1, 'swing': [0.0, r(STOP18 + 0.3), 0.18], 'whip': True}),
               P('fumee18', 'dustPuff', pos=[4.75, 0.0, 1.5], scale=0.9, opts={'once': True, 'startAt': STOP18, 'period': 0.7, 'color': '#E8E2D6'})],
        cams=[FC(0.0, [9.7, 0.55, -3.2], [[4.75, 2.4, 1.2], [4.75, 0.0, 1.2], [4.75, 1.2, 2.6], [4.66, 1.2, 0.1]], top=0.2, bottom=0.76, inside=(5.3, 9.8, 0.3, 4.0, -200.0, 200.0))])   # three-quarter front, the bus's flank and its plate at the right
st.cue('sfx:brake', 'S18', r(STOP18 - 0.4), 0.35); st.cue('sfx:brake', 'S18', STOP18, 0.3)

# 19: he got on. (pass 2) From inside the bus, through its open front door: he hops up onto the step toward us, panting, beard and jersey
D19 = st.dur('S19'); DZ19 = -5.45
st.shot('S19', 'parisStreet', setOpts={'clear': [-12.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [5.9, 0, DZ19], -90, 'walk', 'neutral', keys=[k(0.1, to=[4.6, 0.44, DZ19], dur=0.4, clip='walk', then='stand', ease='out'), k(0.0, look='camera'),
            k(0.1, toon={'sq': [0.95, 1.08, 0.95], 'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.1), k(0.5, toon={'sq': [1.05, 0.94, 1.05], 'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.06), k(0.62, toon={'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.12)])],
        props=[BUS('bus19', [3.5, 0, -3.2], 90, doors=[[0.0, 1.0]]), P('barbe19', 'beardHair', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.02, 0.16]}, scale=0.75, opts={'len': 1.2, 'coil': 0.0, 'depth': 0.1}), MJ('mj19')],
        cams=[cam(0.0, [2.55, 2.0, -5.15], [2.55, 2.0, -5.15], [4.6, 1.95, DZ19], lens=60)])
st.cue('sfx:stepSoft', 'S19', 0.3, 0.2)

# 20: it was not the right bus. (pass 2) In the doorway, facing us: his ticket flat to the lens beside his face, as big as a placard: LIGNE 12;
#     over his head the bus's display: 21 ROME; his eyes go from the ticket up to the display, then to us; one blink; he stares (RATÉ)
D20 = st.dur('S20'); ME20 = [2.25, 0.44, 1.12]; TK20 = [1.6, 2.42, 1.55]; HN20 = [1.8, 2.3, 1.5]
TKP = lambda f: {'reach': {'R': HN20 + [1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': f}
st.shot('S20', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', ME20, 0, 'stand', 'neutral', keys=[k(0.0, look=TK20), k(0.0, toon=TKP({'lid': 0.2, 'mouth': 'open'}), toonDur=0.0),
            k(0.5, look=[2.2, 3.5, 2.6], lookDur=0.12), k(0.52, toon=TKP({'lid': 0.0, 'gy': -1.0, 'brow': 0.6, 'mouth': 'open'}), toonDur=0.1),
            k(1.12, look='camera', lookDur=0.16), k(1.18, toon=TKP({'lid': 0.25, 'mouth': 'line', 'noBlink': True}), toonDur=0.12),
            k(1.62, toon=TKP({'lid': 1.0, 'mouth': 'line', 'noBlink': True}), toonDur=0.07), k(1.74, toon=TKP({'lid': 0.25, 'mouth': 'line', 'noBlink': True}), toonDur=0.08)])],   # the ticket, the display, us; one blink, then his eyes stay open
        props=[BUS('bus20', [0.0, 0, 0.0], 0, doors=[[0.0, 1.0]], top=2.85), P('ticket20', 'busTicket', pos=TK20, face='camera', opts={'w': 0.46, 'h': 0.33, 'title': 'LIGNE', 'num': '12'}, keys=[k(0.0, squash=[1.25, 1.25, 1.0], dur=0.3)]),
               P('plq20', 'busPlate', pos=[2.05, 3.09, 1.21], opts={'text': '21  ROME', 'w': 1.15, 'h': 0.4}, keys=[k(0.55, squash=[1.12, 1.12, 1.0], dur=0.3)]),
               P('barbe20', 'beardHair', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.02, 0.16]}, scale=0.75, opts={'len': 1.2, 'coil': 0.0, 'depth': 0.1}), MJ('mj20')],
        cams=[FC(0.0, [2.3, 2.7, 5.6], [[1.47, 3.31, 1.21], [2.63, 3.31, 1.21], [1.37, 2.42, 1.55], [2.7, 2.0, 1.12]], top=0.21, bottom=0.74)])
st.cue('sfx:paper', 'S20', 0.1, 0.15); st.cue('sfx:sting', 'S20', 0.75, 0.2)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le bus", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'gend1': {'preset': 'cop', 'seed': 722, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'gend2': {'preset': 'cop2', 'seed': 723, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'fan1': {'preset': 'mamie', 'seed': 724, 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'fan2': {'preset': 'gamin', 'seed': 725, 'suit': '#7CC25A', 'build': {'headScale': 1.25}, 'toon': EX},
    'fan3': {'preset': 'fermier', 'seed': 726, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'fan4': {'preset': 'madame', 'seed': 727, 'suit': '#3A9BDC', 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    'fan5': {'preset': 'tourist', 'seed': 728, 'suit': '#E0813A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'sportif', 'seed': 729, 'suit': '#2F62B5', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'cyc{j + 1}': {'preset': 'sportif', 'seed': 730 + j, 'suit': c_, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX} for j, c_ in enumerate(RID8)},
    'lanceur': {'preset': 'tourist', 'seed': 737, 'suit': '#5BB5A8', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chauffeur': {'preset': 'officiel', 'seed': 738, 'suit': '#2F5FA8', 'pants': '#2F5FA8', 'lapel': '#3B6FB8', 'hat': 'copcap', 'hatColor': '#2F5FA8', 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'serveur': {'preset': 'serveur', 'seed': 739, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant1': {'preset': 'savant', 'seed': 740, 'hair': 'receding', 'hairColor': '#EDEDED', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'savant2': {'preset': 'savant', 'seed': 741, 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
})
