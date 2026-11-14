#!/usr/bin/env python3
"""Le café (story 63, cycle 25 of the cartoon staging): this man drank ten coffees in a row. He started to vibrate. So fast that he goes through walls.
The town hall hired him as a jackhammer. He dug a metro line in one night. Yesterday he was served a decaf. He stopped dead, in the middle of the
tunnel. The line has been blocked ever since. The passengers bring him coffees.
Staging: at a café terrace his arm is a blur between his mouth and a tower of empty cups that grows to ten beside his head, his eyes a notch wider and
his hair a notch higher at each cup. He starts to vibrate: ghost copies of him, chattering teeth, the cups rattling on each other. He walks out of a
neighbour's wall, which ripples like jelly round him, the old lady's eyes popping. The mayor shakes his hand to hire him and the vibration goes up the
mayor's arm: hair on end, tie flapping, teeth chattering. A worker holds him by the shoulders like a jackhammer: he drills down into the road, the
asphalt cracking out round him. In the tunnel the rock face crumbles in front of him; then the ground cut open like a cartoon cutaway, the tunnel
shooting across under the street while the moon runs over the sky and the sun comes up, a train already following him. A waiter brings him a cup on a
tray in the tunnel: DÉCA. He gulps it and stops dead: the ghosts snap into one, his hair drops, a record scratch; a pebble taps his helmet. The train
runs into his back and folds up like an accordion; he does not budge. On the platform the passengers crane their necks down the tunnel under a board
counting the minutes in the thousands. In the tunnel they lay coffees at his feet like candles; one holds a cup to his lips: his eyelid twitches.
Natural look; cycle 25 tools: the buzz channel and the shot blur (ghost copies), a hand on another actor's joint (touch '@id.joint'), props_cafe.js
(cupTower, decaCup, jellyWall, roadCracks, metroTunnel, groundCut, metroNose, departureBoard, serviceTray, pebble, slab), sounds rattle, scratch, crunch."""
from story_kit import *
import math

st = Story('cafe', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L04', 4), ('S06', 'L05', 0), ('S07', 'L05', 7),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L07', 4), ('S11', 'L08', 0), ('S12', 'L09', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
DEAD = {'lid': 0.45}
WIRED = {'expr': 'surprised', 'exprW': 0.85, 'eye': 0.5, 'pupil': 0.35, 'brow': 0.5, 'lid': 0.0, 'mouth': 'line'}   # ten coffees: eyes wide open, pinhead pupils ((stills 2) on his heavy-lidded face 'eye' alone did not open them: the painted face pulled toward 'surprised')
CHATTER = {**WIRED, 'mouth': 'teeth', 'tremble': 1.0, 'pupilShake': 1.0}
BURST = lambda pid, pos, at_, text, w=0.62: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.74, 'fit': 0.72, 'bold': True})   # (review 1) the series' size, bold outlined letters (thin black type at 14 % of the width)
STREET = {'eiffelStyle': 'v2', 'clear': [-34.0, -15.0]}                   # no tree or lamp on the right pavement round the terrace and the roadworks
BZ = 0.028                                                               # how far he jitters (m) once the coffee has kicked in
VIB = 0.016                                                              # the shutter that spreads the jitter into ghost copies (s, 5 samples) ((stills 1) 0.022 made a mush in the medium shots)
FACE = 12.6                                                              # (S08-S12) where the tunnel's rock face stands once he has stopped ((script) 2.2 m further: the cameras looking back up the tunnel had lenses of 80)
TUNNEL = lambda **o: P('tun', 'metroTunnel', pos=[0, 0, 0], opts={'face': FACE, 'lampEvery': 1.6, **o})   # (review 1) a lamp every 1.6 m (one ever showed)
TIN = (-19.0, FACE - 0.25, 0.3, 3.3, -2.1, 2.1)                           # a camera stays inside the tunnel's bore
TLOOK = {'sun': 0.32, 'fill': 1.15, 'exposure': 1.5}   # (review 1: mean luma 27-30, the navy suit and the black tux at 1.1:1 on the walls) lamp-lit, not dark: the figures the darkest shapes on mid walls
RIM = lambda pid, pos, k_=4.5, dist=4.5: P(pid, 'glowLight', pos=pos, opts={'color': '#FFD9A6', 'k': k_, 'dist': dist})   # (review 1) a warm lamp behind a figure: its navy or black outline catches it
GLOW = lambda pid, pos, k_=3.0, dist=8.0, col='#FFE2A6': P(pid, 'glowLight', pos=pos, opts={'color': col, 'k': k_, 'dist': dist})

# 1: the hook. At a café terrace he sits by a round table; his left arm is a blur between his mouth and a tower of empty cups: at each cup the tower
#    grows a storey (ten, up beside his head), his eyes open a notch, his pupils shrink a notch, his hair rises a notch; a ding on the tenth, wired
D1 = st.dur('S01'); T0 = 0.12; DT = 0.125                                # ten gulps, an eighth of a second each
ME1 = [8.3, 0, -20.0]; RY1 = -90                                         # his back to the café front, facing the street
TB1 = [8.12, 0, -19.36]                                                  # the table at his left (+Z)
TOWER = [8.12, 0.745, -19.36]
SIP = lambda: {'touch': {'L': ['face', 0.06, 0.22, 0.1, 1, 0.03]}, 'hands': {'L': 'grip'}}
TS1 = 1.75                                                               # (review 1) the tower's scale: at 1.35 it ended level with his head; now well over his hair
STACK = lambda i: {'reach': {'L': [TOWER[0], r(TOWER[1] + TS1 * 0.078 * (i + 1) + 0.08), r(TOWER[2] - 0.02), 1, 0.04]}, 'hands': {'L': 'grip'}}
UP1 = lambda i: {'hairUp': r(0.1 * (i + 1)), 'face': {'expr': 'surprised', 'exprW': r(0.085 * (i + 1)), 'eye': r(0.05 * (i + 1)), 'pupil': r(1.0 - 0.065 * (i + 1)), 'brow': r(0.05 * (i + 1)), 'lid': 0.0}}   # (stills 2) the face opens a notch per cup
K1 = []
for i in range(10):
    K1 += [k(r(T0 + i * DT), toon={**SIP(), **UP1(i)}, toonDur=0.05, toonEase='inOut'), k(r(T0 + i * DT + DT / 2), toon={**STACK(i), **UP1(i)}, toonDur=0.05, toonEase='inOut')]
END1 = r(T0 + 10 * DT)
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME1, RY1, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**STACK(-1), 'face': {'lid': 0.3}}, toonDur=0.0), *K1,
            k(r(END1 + 0.02), toon={'reach': {'L': [r(TOWER[0] + 0.1), 0.8, r(TOWER[2] - 0.12), 1, 0.04]}, 'hands': {'L': 'grip'}, 'hairUp': 1.0, 'sq': [0.93, 1.1, 0.93], 'scl': {'head': [0.92, 1.14, 0.92]}, 'face': {**WIRED, 'eye': 0.7, 'pop': 0.5, 'popLen': 0.12, 'pupil': 0.3}}, toonDur=0.05, toonEase='out'),   # ding: (review 1) a take: stretched up, the eyes out on stalks, pinhead pupils...
            k(r(END1 + 0.16), toon={'reach': {'L': [r(TOWER[0] + 0.1), 0.8, r(TOWER[2] - 0.12), 1, 0.04]}, 'hands': {'L': 'grip'}, 'hairUp': 1.0, 'sq': [1.02, 0.98, 1.02], 'face': {**WIRED, 'eye': 0.6}}, toonDur=0.08, toonEase='inOut'),   # ...back in with an overshoot: wired
            k(r(END1 + 0.3), toon={'reach': {'L': [r(TOWER[0] + 0.1), 0.8, r(TOWER[2] - 0.12), 1, 0.04]}, 'hands': {'L': 'grip'}, 'hairUp': 1.0, 'face': {**WIRED, 'eye': 0.55, 'pupilShake': 0.7}}, toonDur=0.15)])],
        props=[P('chair1', 'chair', pos=ME1, ry=RY1), P('table1', 'bistroTable', pos=TB1),
               P('tower1', 'cupTower', pos=TOWER, opts={'size': TS1, 'n': 10, 'at': [r(T0 + DT / 2), r(T0 + DT / 2 + 10 * DT)], 'sway': 1.4}),   # (stills 1) bigger: the tower ends above his head; (review 1) bigger still, wobbling
               P('cup1', 'cup', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.08, 0.03]})],
        cams=[FC(0.0, [5.7, 1.2, -21.7], [[ME1[0], 2.3, ME1[2]], [r(ME1[0] - 0.3), 0.05, r(ME1[2] + 0.1)], [TOWER[0], r(TOWER[1] + TS1 * 0.82), TOWER[2]], [TB1[0], 0.0, r(TB1[2] + 0.4)]],   # (stills 1) room for his hair standing up; (review 1) the taller tower
                 top=0.12, bottom=0.74, drift=(0.08, 0.0, 0.03))])
for i in range(10): st.cue('sfx:clink', 'S01', r(T0 + i * DT + DT / 2), 0.12)
st.cue('sfx:ding', 'S01', r(END1 + 0.02), 0.3)

# 2: he started to vibrate. Closer at the table: the jitter starts and grows, spread into ghost copies by the shutter; his teeth chatter, his pupils
#    shiver; the cups rattle on each other in the tower beside him; VRRR
D2 = st.dur('S02'); BZ2 = 0.16
HOLD2 = {'touch': {'L': ['torso', 0.14, 0.45, 0.27, 1, 0.03]}, 'hands': {'L': 'grip'}}
st.shot('S02', 'parisStreet', setOpts=STREET, blur=[[r(BZ2 + 0.06), D2, VIB]], blurSamples=5, actors=[
        act('mec', ME1, RY1, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD2, 'hairUp': 1.0, 'face': {**WIRED, 'eye': 0.55}}, toonDur=0.0),
            k(BZ2, toon={**HOLD2, 'hairUp': 1.0, 'buzz': 0.008, 'face': {**WIRED, 'eye': 0.55, 'mouth': 'teeth', 'tremble': 0.5}}, toonDur=0.04),
            k(r(BZ2 + 0.3), toon={**HOLD2, 'hairUp': 1.0, 'buzz': BZ, 'face': {**CHATTER, 'eye': 0.55}}, toonDur=0.22, toonEase='in')])],
        props=[P('chair2', 'chair', pos=ME1, ry=RY1), P('table2', 'bistroTable', pos=TB1),
               P('tower2', 'cupTower', pos=TOWER, opts={'size': TS1, 'n': 10, 'at': [-2.0, -1.0], 'sway': 1.4, 'rattle': [r(BZ2 + 0.1), 0.014]}),
               P('cup2', 'cup', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.08, 0.03]}),
               BURST('vrrr2', [r(ME1[0] - 0.2), 2.12, r(ME1[2] - 0.2)], r(BZ2 + 0.22), 'VRRR !', 0.5)],   # (review 1) inside the frame (the left edge cut it), bigger
        cams=[FC(0.0, [6.7, 1.35, -21.0], [[ME1[0], 2.3, ME1[2]], [ME1[0], 0.7, r(ME1[2] + 0.1)], [TOWER[0], r(TOWER[1] + TS1 * 0.82), TOWER[2]], [r(ME1[0] - 0.2), 2.45, r(ME1[2] - 0.45)]],
                 top=0.1, bottom=0.8, drift=(0.06, 0.0, 0.0))])
st.cue('sfx:rattle', 'S02', BZ2, 0.3)

# 3: so fast that he goes through walls. A neighbour's sitting room: the wall behind bulges and ripples like jelly in rings round the spot where he walks
#    out of it, his cup in his hand, vibrating, deadpan; the rings run out to the framed seascape, which wobbles; the old lady on her sofa looks up from
#    her tea, looks back, and her eyes pop
D3 = st.dur('S03'); WX = -0.75; WZ = -3.47
RIP = [[0.0, WX, 1.25, 0.3], [0.12, WX, 1.4, 0.3], [0.4, WX, 1.05, 0.22], [0.66, WX, 0.55, 0.14]]   # (stills 1) stronger rings: at 0.13 m they were a faint shading; (review 1) stronger still, from the first frame (the bulge read as a floating ball)
MAM3 = [1.12, 0, -2.0]; TEA3 = [0.89, 0.9, -1.65]                        # (stills 1) her face to us: turned toward the spot of the wall where he comes out; (review 1) further in (her eye-pop happened at the right edge)
st.shot('S03', 'livingRoom', setOpts={'sofa': False, 'picture': False, 'plant': False, 'carpet': False}, blur=[[0.0, D3, VIB]], blurSamples=5, actors=[
        act('mec', [WX, 0, -3.95], 8, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD2, 'hairUp': 1.0, 'buzz': BZ, 'face': CHATTER}, toonDur=0.0),
            k(0.0, to=[r(WX - 0.05), 0, -3.0], dur=0.8, clip='walk', ease='linear', face='keep'), k(0.8, to=[r(WX - 0.25), 0, -2.45], dur=r(D3 - 0.8), clip='walk', then='stand', ease='out', face='keep')]),   # (script) a slow deadpan walk: out of the wall and a step on
        act('mamie', MAM3, -58, 'sit', 'neutral', keys=[k(0.0, look=TEA3), k(0.0, toon={'reach': {'R': [TEA3[0], 0.95, TEA3[2], 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'gy': 0.5}}, toonDur=0.0),
            k(0.42, look=[WX, 1.7, -3.2]), k(0.44, toon={'reach': {'R': [TEA3[0], 0.95, TEA3[2], 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.2, 'gy': 0.0}}, toonDur=0.08),   # she looks up...
            k(0.62, look=TEA3), k(0.64, toon={'reach': {'R': [TEA3[0], 0.95, TEA3[2], 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'gy': 0.5}}, toonDur=0.06),   # ...back to her tea...
            k(0.86, look=[-1.0, 1.7, -2.4]), k(0.88, toon={'reach': {'R': [TEA3[0], 1.05, TEA3[2], 1, 0.03]}, 'hands': {'R': 'pinch'}, 'sq': [0.95, 1.06, 0.95], 'hairUp': 0.6, 'face': {'pop': 0.75, 'popLen': 0.22, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # ...and her eyes pop
            k(1.35, toon={'reach': {'R': [TEA3[0], 1.0, TEA3[2], 1, 0.03]}, 'hands': {'R': 'pinch'}, 'hairUp': 0.4, 'face': {'pop': 0.5, 'popLen': 0.2, 'brow': 0.8, 'mouth': 'O'}}, toonDur=0.3)])],
        props=[P('wall3', 'jellyWall', pos=[0.0, 0, WZ], opts={'w': 7.2, 'h': 4.4, 'picture': [0.65, 1.85, 1.0, 0.7], 'ripple': RIP}),
               P('sofa3', 'sofaProp', pos=MAM3, ry=-58), P('cup3', 'cup', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.08, 0.03]}),
               P('tea3', 'cup', on={'actor': 'mamie', 'hand': 'R', 'offset': [0.0, -0.06, 0.02]})],
        cams=[FC(0.0, [0.8, 1.2, 1.2], [[WX, 2.45, WZ], [r(WX - 0.25), 0.05, -2.45], [r(MAM3[0] + 0.55), 1.75, MAM3[2]], [MAM3[0], 0.35, MAM3[2]], [0.65, 2.25, WZ]],   # (stills 2) lower: less empty floor, more of the wall; (review 1) room right of her for the stalks
                 top=0.08, bottom=0.8, inside=(-6.5, 6.5, 0.3, 3.0, -3.0, 13.0), drift=(-0.1, 0.0, 0.0))])
st.cue('sfx:rattleShort', 'S03', 0.0, 0.18); st.cue('sfx:spring', 'S03', 0.12, 0.3); st.cue('sfx:spring', 'S03', 0.4, 0.2); st.cue('sfx:gasp', 'S03', 0.88, 0.3)

# 4: the town hall hired him. ((stills 2) both three-quarter to us: in profile the mayor's take did not read)
#    In the mayor's office the mayor, all smiles, shakes his hand; his hand is on the vibrating one and the vibration runs up
#    his arm: he vibrates too, harder, hair on end, tie flapping, eyes bulging, teeth chattering; EMBAUCHÉ
D4 = st.dur('S04'); GRIP4 = 0.2
ME4 = [-0.36, 0, 0.15]; MA4 = [0.44, 0, 0.15]
SHAKE = {'touch': {'R': ['torso', -0.02, 0.42, 0.45, 1, 0.03]}, 'hands': {'R': 'grip'}}
st.shot('S04', 'mairie', setOpts={'plate': 'MAIRIE', 'map': False}, blur=[[0.0, D4, 0.01]], blurSamples=5, actors=[   # (stills 1) no map from another story; a shorter shutter (a mush at 0.022)
        act('mec', ME4, 28, 'stand', 'unimpressed', keys=[k(0.0, look=[MA4[0], 1.9, MA4[2]]), k(0.0, toon={**SHAKE, 'hairUp': 1.0, 'buzz': BZ, 'face': CHATTER}, toonDur=0.0)]),
        act('maire', MA4, -28, 'stand', 'happy', keys=[k(0.0, look=[ME4[0], 1.9, ME4[2]]), k(0.0, toon={'reach': {'R': [0.06, 1.02, 0.6, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0}}, toonDur=0.0),
            k(r(GRIP4 - 0.06), toon={'touch': {'R': ['@mec.handR', 0.0, 0.0, 0.0, 1, 0.0]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0}}, toonDur=0.06, toonEase='in'),   # the grip...
            k(GRIP4, toon={'touch': {'R': ['@mec.handR', 0.0, 0.0, 0.0, 1, 0.0]}, 'hands': {'R': 'grip'}, 'buzz': 0.02, 'hairUp': 0.6, 'wind': [0.0, 7.0, 2.0], 'face': {'mouth': 'bigsmile', 'eye': 0.4}}, toonDur=0.04),   # ...the vibration runs up his arm...
            k(r(GRIP4 + 0.1), look='camera'),   # (review 1: both heads in profile, his take never showed) his face to us...
            *[k(r(GRIP4 + 0.18 + 0.07 * j), toon={'touch': {'R': ['@mec.handR', 0.0, 0.0, 0.0, 1, 0.0]}, 'hands': {'R': 'grip'}, 'buzz': 0.055, 'hairUp': 1.0, 'wind': [0.0, 9.0, 3.0], 'sq': ([0.94, 1.08, 0.94] if j % 2 else [1.04, 0.95, 1.04]),
                'face': {'expr': 'surprised', 'exprW': 0.9, 'eye': 0.8, 'pop': 0.6, 'popLen': 0.16, 'pupil': 0.4, 'mouth': 'teeth', 'tremble': 1.0, 'pupilShake': 1.0, 'brow': 1.0}}, toonDur=0.05, toonEase='out') for j in range(8)]])],   # ...all over him, harder than on him: eyes out on stalks, his body rattling up and down
        props=[], cams=[FC(0.0, [0.1, 1.45, 3.0], [[ME4[0], 2.6, ME4[2]], [MA4[0], 2.75, MA4[2]], [ME4[0], 0.6, ME4[2]], [MA4[0], 0.6, MA4[2]]], top=0.21, bottom=0.8,   # (review 1) the hair under the card's band
                 inside=(-3.8, 3.8, 0.3, 3.2, -2.3, 6.0), drift=(0.0, 0.0, -0.08))])
st.cue('sfx:rattle', 'S04', GRIP4, 0.32); st.cue('sfx:gasp', 'S04', r(GRIP4 + 0.05), 0.2)

# 5: as a jackhammer. In the road, his helmet on: a worker behind him holds him by the shoulders like the handles of a jackhammer, both vibrating; he
#    drills straight down into the asphalt, cracks running out round him, bits of road flying, dust; the worker's teeth chatter and his helmet hops
D5 = st.dur('S05'); R5 = [2.1, 0, -30.0]; SINK = 0.95   # (review 1) to the knees (shin-deep did not say a drill)
W5 = [R5[0], 0, r(R5[2] - 0.5)]                                          # (stills 1) further aside: his face hid behind the helmet; (review 1) right behind him, over him, seen from the side
HANDLES = lambda w: {'touch': {'L': ['@mecC.torso', 0.2, 0.58, -0.06, w, 0.02, [1.0, 0.1, -0.2]], 'R': ['@mecC.torso', -0.2, 0.58, -0.06, w, 0.02, [-1.0, 0.1, -0.2]]}, 'hands': {'L': 'grip', 'R': 'grip'}}   # (review 1) elbows out: the handles of a jackhammer
st.shot('S05', 'parisStreet', setOpts=STREET, blur=[[0.0, D5, VIB]], blurSamples=5, actors=[
        act('mecC', R5, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, to=[R5[0], -SINK, R5[2]], dur=D5, ease='linear', face='keep'),
            k(0.0, toon={'buzz': 0.034, 'face': {**WIRED, 'lid': 0.3}}, toonDur=0.0)]),
        act('ouv', W5, 0, 'stand', 'neutral', keys=[k(0.0, look=[R5[0], 0.0, r(R5[2] + 0.6)]), k(0.0, toon={**HANDLES(1), 'buzz': 0.03, 'hat': [0.04, 0.05, 0.0], 'face': {'mouth': 'teeth', 'tremble': 1.0, 'eye': 0.5, 'cheeks': 0.6}}, toonDur=0.0),
            k(r(D5 * 0.5), toon={**HANDLES(1), 'buzz': 0.03, 'hat': [0.07, -0.08, 0.0], 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'mouth': 'teeth', 'tremble': 1.0, 'eye': 0.6, 'cheeks': 0.8}}, toonDur=r(D5 * 0.5)),
            k(D5, toon={**HANDLES(1), 'buzz': 0.03, 'hat': [0.05, 0.06, 0.0], 'bend': {'spine': [0.4, 0, 0, 1, None]}, 'face': {'mouth': 'teeth', 'tremble': 1.0, 'eye': 0.7, 'cheeks': 1.0}}, toonDur=r(D5 * 0.5))])],
        props=[P('cracks5', 'roadCracks', pos=[R5[0], 0.0, R5[2]], opts={'r': 1.7, 'at': [0.04, D5], 'hole': 0.38}),
               ],   # (stills 1) no dust puffs: their grey balls read as boulders round his feet
        cams=[FC(0.0, [-1.0, 0.9, -28.4], [[R5[0], 2.35, R5[2]], [R5[0], -0.35, r(R5[2] + 0.5)], [W5[0], 2.4, W5[2]], [R5[0], 0.0, r(R5[2] - 1.4)], [R5[0], 0.0, r(R5[2] + 1.4)]],   # (review 1) three-quarter from his side: the worker behind and over him reads as the handles
                 top=0.1, bottom=0.82, drift=(0.0, -0.1, 0.0))])
st.cue('sfx:rattle', 'S05', 0.0, 0.4); st.cue('sfx:rattleShort', 'S05', 0.75, 0.3)

# 6: he dug a metro line... In the tunnel, from the side: he leans into the rock face, vibrating, and it crumbles in front of him; he goes forward with
#    it, dust boiling off it, the lamps coming on behind him one by one
D6 = st.dur('S06'); FX6 = [6.6, 8.0]
DIG = {'bend': {'spine': [0.22, 0, 0, 1, None]}, 'touch': {'L': ['torso', 0.2, 0.5, 0.46, 1, 0.02], 'R': ['torso', -0.2, 0.52, 0.46, 1, 0.02]}, 'hands': {'L': 'open', 'R': 'open'}}
st.shot('S06', 'spaceDark', look=TLOOK, blur=[[0.0, D6, VIB]], blurSamples=5, actors=[
        act('mecC', [r(FX6[0] - 0.45), 0, 0], 90, 'stand', 'unimpressed', keys=[k(0.0, look=[FACE, 1.5, 0.0]), k(0.0, to=[r(FX6[1] - 0.45), 0, 0], dur=D6, ease='linear', face='keep'),
            k(0.0, toon={**DIG, 'buzz': 0.034, 'face': {**WIRED, 'lid': 0.25}}, toonDur=0.0)])],
        props=[TUNNEL(face=FX6[0], faceMove=[[0.0, FX6[0]], [D6, FX6[1]]], dust=[[0.0, D6]], litFollow=1.0), GLOW('glow6', [FX6[0] - 1.2, 2.3, 1.4], 3.5, 9.0),
               P('key6', 'glowLight', pos=[r(FX6[0] - 0.9), 1.9, 1.3], opts={'color': '#FFC98A', 'k': 7.0, 'dist': 4.5}, keys=[k(0.0, to=[r(FX6[1] - 0.9), 1.9, 1.3], dur=D6, ease='linear')]),   # (review 1) a lamp at the face: the rock lit, him dark against it
               RIM('rim6', [r(FX6[0] - 2.2), 2.4, -0.6], 4.0, 4.0),
               *[P(f'chunk6{i}', 'pebble', pos=[r(FX6[0] + 1.4 * (0.1 + 0.2 * i) / D6 - 0.05), r(0.9 + 0.25 * (i % 3)), r(-0.5 + 0.35 * (i % 4))], opts={'r': 0.16, 'color': '#8C7A64'},
                   keys=[k(0.0, visible=False), k(r(0.1 + 0.2 * i), visible=True), k(r(0.1 + 0.2 * i), to=[r(FX6[0] + 1.4 * (0.1 + 0.2 * i) / D6 - 0.7), 0.12, r(-0.7 + 0.45 * (i % 4))], dur=0.34, ease='in')]) for i in range(6)]],   # (review 1) big chunks breaking off the face
        cams=[FC(0.0, [4.3, 1.45, 1.95], [[r(FX6[0] - 0.45), 2.35, 0], [r(FX6[0] - 0.45), 0.55, 0.2], [r(FX6[0] + 0.75), 2.2, 0], [r(FX6[0] - 1.05), 1.0, 0]],   # (stills 1) the camera stays behind the face's plane (inside the rock the frame was black); (review 1) the face mid-frame, him driving in from the left
                 top=0.1, bottom=0.84, lenses=range(24, 70), inside=(-19.0, 19.0, 0.3, 3.3, -2.1, 2.15), drift=(1.1, 0.0, 0.0))])   # his left profile, the rock face to the right (a vertical frame inside a 4.8 m bore: from the knees up)
st.cue('sfx:rattle', 'S06', 0.0, 0.35); st.cue('thud', 'S06', 0.5, 0.2); st.cue('thud', 'S06', 1.0, 0.2)

# 7: ...in one night. The ground cut open like a cartoon cutaway: under the street at night the tunnel shoots across the frame behind him, the lamps
#    coming on, a train already following him; the moon runs over the sky, the windows go out, the sun comes up
D7 = st.dur('S07'); DUG = [0.0, r(D7 - 0.1)]; GX = [-4.2, 4.6]; GY = -3.72; GZ = -0.7
C7 = FC(0.0, [0.25, -1.0, 14.0], [[-3.3, -7.4, 0.0], [3.6, 5.2, 0.0], [-3.3, 5.2, 0.0], [3.6, -7.4, 0.0]], top=0.03, bottom=0.97, lenses=range(20, 60))   # (script) down to 7.4 m under the street: the tunnel above the caption band
SKYZ = -(45 + 12)
def on_sky(u, v):
    """the point of the sky plane seen at frame fraction (u across from the left, v down from the top)"""
    fr, lk, ln = C7['from'], C7['lookAt'], C7['lens']; d = fr[2] - SKYZ; w, h = frame_size(ln, d)
    return [r(lk[0] + (fr[0] - lk[0]) * (SKYZ / -fr[2] if fr[2] else 0) + (u - 0.5) * w, 2), r(fr[1] + (lk[1] - fr[1]) * d / max(1e-3, fr[2] - lk[2]) + (0.5 - v) * h, 2)]
MOON = [on_sky(0.18, 0.13), on_sky(0.5, 0.06), on_sky(0.86, 0.2)]
SUNX = on_sky(0.33, 0.2)[0]; SUNY = [on_sky(0.33, 0.42)[1], on_sky(0.33, 0.16)[1]]   # (stills 1) clear of the lamp post that crossed it
st.shot('S07', 'spaceDark', look={'sun': 0.3, 'sunColor': '#9DB0E8', 'fill': 0.7, 'exposure': 1.0}, actors=[
        act('mecC', [r(GX[0] - 0.4), GY, GZ], 90, 'stand', 'unimpressed', keys=[k(0.0, look=[GX[1], -2.4, GZ]), k(0.0, to=[r(GX[1] - 0.4), GY, GZ], dur=DUG[1], clip='walk', then='stand', ease='linear', face='keep'),
            k(0.0, toon={'buzz': 0.03, 'face': {**WIRED, 'lid': 0.25}}, toonDur=0.0)])],
        props=[P('cut7', 'groundCut', pos=[0, 0, 0], opts={'len': 40, 'depth': 3.8, 'th': 2.6, 'bottom': 10.0, 'at': DUG, 'x0': GX[0], 'x1': GX[1], 'dawn': [r(D7 - 0.5), r(D7 - 0.12)], 'far': 45, 'frontH': [7, 11],
                                                        'moon': MOON, 'sunX': SUNX, 'sunY': SUNY}),
               P('nose7', 'metroNose', pos=[r(GX[0] - 3.4), GY, GZ], opts={'len': 8}, keys=[k(0.0, to=[r(GX[1] - 3.4), GY, GZ], dur=DUG[1], ease='linear')])],
        cams=[cam(0.0, [r(C7['from'][0] - 1.8), C7['from'][1], C7['from'][2]], [r(C7['from'][0] + 2.6), C7['from'][1], C7['from'][2]], [r(C7['lookAt'][0] - 1.8), C7['lookAt'][1], C7['lookAt'][2]], [r(C7['lookAt'][0] + 2.6), C7['lookAt'][1], C7['lookAt'][2]], lens=C7['lens'])])   # (pass 2 stills) further: a 1.7 m pan still left him at the right edge at dawn   # (review 1) the camera follows him (at dawn the right edge cut him)
st.cue('whoosh', 'S07', 0.0, 0.35, 0.9, 300, 1200); st.cue('sfx:ding', 'S07', r(D7 - 0.15), 0.25)

# 8: yesterday he was served a decaf. In the tunnel, from in front of him (the rock face behind us): vibrating, facing us, he waits; out of the dark
#    behind him a waiter, white napkin, tray on his flat hand, walks up the rails to his shoulder, a little bow, the tray held out; he takes the cup
#    and brings it up in front of him: DÉCA on it
#    (script: a two-shot across a 4.8 m bore does not fit a vertical frame: the camera looks down the tunnel instead, the waiter coming up behind him)
D8 = st.dur('S08'); TAKE8 = 1.05
ME8 = [8.55, 0, 0.0]; SV8 = [7.75, 0, 1.0]                               # (stills 1) at his right shoulder, on our side: behind him the tray was hidden; (review 1) further aside: their heads overlapped
TRAY = lambda w=1: {'touch': {'L': ['torso', 0.24, 0.58, 0.44, w, 0.0]}, 'hands': {'L': 'open', 'R': 'open'}, 'bend': {'armR': [0.0, 0.0, 0, 1, None], 'foreR': [-1.2, 0.0, 0, 1, None]}}
st.shot('S08', 'spaceDark', look=TLOOK, blur=[[0.0, D8, VIB]], blurSamples=5, actors=[
        act('mecC', ME8, 96, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'buzz': 0.042, 'face': {**WIRED, 'lid': 0.2}}, toonDur=0.0),   # (review 1) the ghosts wider (a faint double outline here made the stop small)
            k(0.72, look=[SV8[0], 1.8, r(SV8[2] - 0.3)]), k(r(TAKE8 - 0.2), toon={'buzz': BZ, 'touch': {'R': ['@serveur.handL', 0.0, 0.0, 0.0, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {**WIRED, 'lid': 0.2}}, toonDur=0.16, toonEase='inOut'),
            k(r(TAKE8 + 0.1), look='camera'), k(r(TAKE8 + 0.12), toon={'buzz': BZ, 'touch': {'R': ['torso', -0.1, 0.47, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {**WIRED, 'lid': 0.2, 'gy': 0.5}}, toonDur=0.25, toonEase='inOut')]),   # the cup up in front of him, his eyes down on it
        act('serveur', [5.5, 0, SV8[2]], 90, 'stand', 'smug', keys=[k(0.0, look=[ME8[0], 1.9, ME8[2]]), k(0.0, to=SV8, dur=0.62, clip='walk', then='stand', ease='out', face='keep'),
            k(0.0, toon={**TRAY(), 'face': {'lid': 0.5, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.68, toon={**TRAY(), 'bend': {'spine': [0.26, 0, 0, 1, None]}, 'face': {'lid': 0.6, 'mouth': 'smirk'}}, toonDur=0.16, toonEase='inOut'),   # a little bow, the tray held out
            k(r(TAKE8 + 0.3), toon={**TRAY(), 'face': {'lid': 0.5, 'mouth': 'smirk'}}, toonDur=0.25)])],
        props=[TUNNEL(), GLOW('glow8', [9.6, 2.3, 1.0], 3.5, 9.0), RIM('rim8a', [6.6, 2.3, 1.3]), RIM('rim8b', [7.4, 2.4, -0.9], 3.5, 4.0),   # (review 1) lamps behind them: the tux and the suit apart from the dark
               P('tray8', 'serviceTray', on={'actor': 'serveur', 'joint': 'torso', 'offset': [0.24, 0.62, 0.44]}, scale=1.3),   # (review 1) at his chest, held out (edge-on at the shoulder it read as a stick into his head)
               P('nap8', 'slab', on={'actor': 'serveur', 'hand': 'R', 'offset': [0.0, -0.14, 0.0]}, opts={'w': 0.05, 'h': 0.32, 'd': 0.18, 'color': '#FBFBF7'}),   # the white napkin over his arm
               P('deca8', 'decaCup', scale=1.25, on={'actor': 'tray8', 'offset': [0.0, 0.016, 0.0]}, keys=[k(TAKE8, attach='mecC', hand='R', offset=[0.0, -0.08, 0.04], face='camera')])],
        cams=[FC(0.0, [11.9, 1.6, 0.9], [[ME8[0], 2.5, ME8[2]], [SV8[0], 2.4, SV8[2]], [ME8[0], 0.55, ME8[2]], [r(SV8[0] - 0.4), 1.2, SV8[2]]],   # (stills 1) from the knees up: his feet sat in the captions
                 top=0.1, bottom=0.76, lenses=range(22, 60), inside=TIN, drift=(-0.08, 0.0, -0.04))])
st.cue('sfx:step', 'S08', 0.15, 0.15); st.cue('sfx:step', 'S08', 0.42, 0.15); st.cue('sfx:clink', 'S08', TAKE8, 0.25)

# 9: he stopped dead... Close: he gulps the decaf down; and stops dead: the ghosts snap into one man, his hair drops, his eyes shrink back, a record
#    scratch; silence; a pebble falls from the vault and taps his helmet: his eyes roll up to it
D9 = st.dur('S09'); SIP9 = 0.1; STOP9 = 0.44; PEB9 = 0.84
ME9 = [8.55, 0, 0.0]; HEAD9 = [8.55, 2.38, 0.0]
DRINK = lambda w=1: {'touch': {'R': ['face', -0.05, 0.22, 0.09, w, 0.03]}, 'hands': {'R': 'grip'}}   # (stills 1) the right hand, the one that took the cup
st.shot('S09', 'spaceDark', look=TLOOK, blur=[[0.0, STOP9, 0.02]], blurSamples=5, actors=[   # (review 1) a wider shutter until the stop: the ghosts at their widest just before it
        act('mecC', ME9, 100, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'buzz': 0.05, 'hairUp': 1.0, 'hat': [0.05, 0.0, 0.0], 'touch': {'R': ['torso', -0.1, 0.47, 0.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': WIRED}, toonDur=0.0),
            k(SIP9, toon={**DRINK(), 'buzz': 0.055, 'hairUp': 1.0, 'hat': [0.05, 0.0, 0.0], 'bend': {'neck': [-0.32, 0, 0, 1, None]}, 'face': {**WIRED, 'lid': 0.5}}, toonDur=0.08, toonEase='inOut'),   # the decaf down in one...
            k(r(SIP9 + 0.12), toon={**DRINK(), 'buzz': 0.06, 'hairUp': 1.0, 'hat': [0.05, 0.0, 0.0], 'bend': {'neck': [-0.36, 0, 0, 1, None]}, 'face': {**WIRED, 'lid': 0.6, 'gulp': 1.0}}, toonDur=0.2),
            k(STOP9, toon={'touch': {'R': ['torso', -0.1, 0.42, 0.26, 1, 0.03]}, 'hands': {'R': 'grip'}, 'buzz': 0.0, 'hairUp': -0.15, 'hat': [-0.035, 0.0, 0.0], 'sq': [1.04, 0.96, 1.04], 'face': {'eye': -0.1, 'pupil': 1.1, 'lid': 0.45}}, toonDur=0.0),   # ...STOP: all at once, one crisp man, (review 1) the helmet dropping onto him, a squash...
            k(r(STOP9 + 0.07), toon={'touch': {'R': ['torso', -0.1, 0.42, 0.26, 1, 0.03]}, 'hands': {'R': 'grip'}, 'hairUp': -0.1, 'hat': [-0.02, 0.0, 0.0], 'sq': [0.99, 1.01, 0.99], 'face': {'eye': -0.1, 'pupil': 1.0, 'lid': 0.45}}, toonDur=0.04),   # ...settling in two frames
            k(r(STOP9 + 0.12), toon={'touch': {'R': ['torso', -0.1, 0.42, 0.26, 1, 0.03]}, 'hands': {'R': 'grip'}, 'hairUp': 0.0, 'face': DEAD}, toonDur=0.12, toonEase='out'),
            k(r(PEB9 + 0.02), toon={'touch': {'R': ['torso', -0.1, 0.42, 0.26, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.1, 'eye': 0.15, 'gy': -0.62}}, toonDur=0.05, toonEase='out'),   # tap: (review 1) his eyes rolled up to it, open (half-lidded they read as closed)
            k(r(D9 - 0.05), toon={'touch': {'R': ['torso', -0.1, 0.42, 0.26, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'gy': -0.55}}, toonDur=0.2)])],
        props=[TUNNEL(), GLOW('glow9', [9.4, 2.3, 1.2], 3.5, 9.0),
               P('cup9', 'decaCup', scale=1.25, on={'actor': 'mecC', 'hand': 'R', 'offset': [0.0, -0.08, 0.04]}),
               P('peb9', 'pebble', pos=[r(HEAD9[0] + 0.03), 3.6, HEAD9[2]], opts={'r': 0.085, 'color': '#CFC6B4'}, keys=[k(r(PEB9 - 0.3), to=[r(HEAD9[0] + 0.03), HEAD9[1], HEAD9[2]], dur=0.3, ease='in'),
                   k(PEB9, to=[r(HEAD9[0] + 0.2), r(HEAD9[1] + 0.32), r(HEAD9[2] + 0.12)], dur=0.12, ease='out'), k(r(PEB9 + 0.12), to=[r(HEAD9[0] + 0.45), 0.05, r(HEAD9[2] + 0.35)], dur=0.25, ease='in')]), RIM('rim9', [7.4, 2.5, -0.8], 4.0, 4.0)],   # (review 1) bigger and pale against the vault, a bounce off the helmet
        cams=[FC(0.0, [10.4, 1.75, 0.75], [[ME9[0], 2.5, ME9[2]], [ME9[0], 1.15, ME9[2]], [r(ME9[0] + 0.35), 1.7, r(ME9[2] + 0.2)], [ME9[0], 2.75, ME9[2]]], top=0.1, bottom=0.8, lenses=range(24, 56), inside=TIN)])
st.cue('sfx:rattleShort', 'S09', 0.0, 0.3); st.cue('sfx:gulp', 'S09', r(SIP9 + 0.12), 0.3); st.cue('sfx:scratch', 'S09', STOP9, 0.4); st.cue('sfx:bonk', 'S09', PEB9, 0.2)

# 10: ...in the middle of the tunnel. From in front of him: he stands frozen on the track; the train's headlights rush up behind him and it runs into his
#     back and folds up like an accordion; he does not budge an inch; his helmet hops; dust; a slow blink
D10 = st.dur('S10'); HIT10 = 0.4; ME10 = [8.3, 0, 0.0]
st.shot('S10', 'spaceDark', look=TLOOK, actors=[
        act('mecC', ME10, 90, 'stand', 'unimpressed', keys=[k(0.0, look=[FACE, 1.9, 0.6]), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(HIT10, toon={'hat': [0.16, 0.12, 0.0], 'face': {'lid': 0.45}}, toonDur=0.04, toonEase='out'), k(r(HIT10 + 0.22), toon={'hat': [0.0, 0.0, 0.0], 'face': DEAD}, toonDur=0.12, toonEase='in'),   # only his helmet hops
            k(r(D10 - 0.3), toon={'face': {'lid': 1.0}}, toonDur=0.12), k(r(D10 - 0.12), toon={'face': DEAD}, toonDur=0.1)])],
        props=[TUNNEL(), GLOW('glow10', [9.4, 2.3, -1.2], 3.0, 9.0),
               P('nose10', 'metroNose', pos=[-12.0, 0, 0.0], opts={'len': 8, 'crumple': [HIT10, 0.38, 0.09]}, keys=[k(0.0, to=[r(ME10[0] - 0.25), 0, 0.0], dur=HIT10, ease='in')]),
               *[P(f'flare10{j}', 'halo', pos=[-11.8, 0.72, zz], face='camera', opts={'r': 0.85, 'k': 0.95, 'core': '#FFFFFF', 'color': '#FFE6A8'}, keys=[k(0.0, to=[r(ME10[0] - 0.05), 0.72, zz], dur=HIT10, ease='in')]) for j, zz in enumerate([-0.82, 0.82])],   # (review 1) the headlights rushing up as big flares
               P('hl10', 'glowLight', pos=[-11.6, 1.1, 0.0], opts={'color': '#FFF0CC', 'k': 9.0, 'dist': 9.0}, keys=[k(0.0, to=[r(ME10[0] - 0.05), 1.1, 0.0], dur=HIT10, ease='in')]),   # ...and the light that rims him from behind
               BURST('scr10', [r(ME10[0] - 0.4), 2.55, -0.5], r(HIT10 + 0.02), 'SCRONCH !', 0.62)],
        cams=[FC(0.0, [11.6, 1.45, -1.9], [[ME10[0], 2.45, ME10[2]], [ME10[0], -0.15, ME10[2]], [5.6, 2.35, 0.0], [5.6, 0.0, 1.25], [r(ME10[0] - 0.6), 2.8, -0.55]],
                 top=0.1, bottom=0.74, lenses=range(24, 60), inside=TIN)])
st.cue('sfx:brake', 'S10', 0.05, 0.25); st.cue('sfx:crunch', 'S10', HIT10, 0.45)

# 11: the line has been blocked ever since. On the platform the passengers lean out over the edge in a row and crane their necks down the dark tunnel;
#     above them the board counts the minutes to the next train, faster and faster, into the thousands; BLOQUÉE
D11 = st.dur('S11')
MOUTH = [-5.6, 1.9, 1.7]                                                 # (stills 3) their eyes level down the tunnel: aimed at its floor the heads drooped; (review 1) the mouth nearer, in the frame
CRANE = lambda w: {'bend': {'spine': [r(0.18 * w), r(-0.22 * w), 0, 1, None], 'neck': [r(0.95 * w), r(-0.42 * w), 0, r(1 + 3.6 * w), None]}, 'face': {'eye': r(0.3 * w), 'lid': 0.0}}   # (review 1: hooked down, heads drooping toward a grey wall) level out toward the mouth   # (stills 2) a neck four times its length out over the track: at 2.1 they only bowed; (stills 3) out sideways over the track, not bowed down
VOY = [('voy1', [-4.7, 0, -0.55]), ('voy2', [-3.65, 0, -0.6]), ('voy3', [-2.6, 0, -0.55]), ('voy4', [-1.55, 0, -0.62])]   # (pass 2 stills) nearer the tunnel mouth: with it in the frame the camera had backed off and they were small
BOARD = [-3.3, 3.75, -1.6]                                               # (stills 2) clear of the right edge
st.shot('S11', 'spaceDark', look={'sun': 0.2, 'fill': 0.9, 'exposure': 1.0}, actors=[
        act(vid, pos, -90, 'stand', 'neutral', keys=[k(0.0, look=MOUTH), k(0.0, toon={'face': {'lid': 0.5}}, toonDur=0.0),
            k(r(0.16 + 0.05 * i), toon=CRANE(1.15), toonDur=0.12, toonEase='out'), k(r(0.34 + 0.05 * i), toon=CRANE(1.0), toonDur=0.12, toonEase='inOut'),   # all lean out, the necks overshoot...
            k(r(0.95 + 0.04 * i), look=[BOARD[0], BOARD[1] - 0.3, BOARD[2]]), k(r(0.97 + 0.04 * i), toon={**CRANE(0.85), 'face': {'lid': 0.2, 'eye': 0.15}}, toonDur=0.15)])   # ...and up at the board
        for i, (vid, pos) in enumerate(VOY)],
        props=[P('quai11', 'metroPlatform', pos=[0, 0, 0], opts={'len': 15, 'name': 'MAIRIE', 'bench': False}),
               P('vault11', 'slab', pos=[0, 4.45, -0.5], opts={'w': 16, 'h': 0.3, 'd': 9.0, 'color': '#2E3036', 'noShadow': True}),
               P('end11', 'slab', pos=[-5.95, 1.6, -0.5], opts={'w': 0.3, 'h': 6.0, 'd': 9.0, 'color': '#D9D4C8'}),
               P('mouth11', 'slab', pos=[-5.78, 0.6, 1.7], opts={'w': 0.05, 'h': 3.2, 'd': 3.2, 'color': '#050608'}),   # (review 1) the tunnel mouth nearer, in the frame
               P('board11', 'departureBoard', pos=BOARD, ry=0, opts={'at': [0.12, 1.0], 'from': 4, 'to': 3427})],
        cams=[FC(0.0, [-1.6, 1.3, 3.0], [[-4.7, 2.4, -0.55], [-1.55, -0.1, -0.62], [-4.7, -0.1, -0.55], [BOARD[0], r(BOARD[1] + 0.05), BOARD[2]], [-5.6, 2.2, 1.6]],
                 top=0.06, bottom=0.74, lenses=range(24, 60), drift=(-0.1, 0.0, 0.0))])   # (stills 1) from across the track: from the platform we saw their backs
st.cue('sfx:stretch', 'S11', 0.18, 0.25); st.cue('sfx:ticks', 'S11', 0.15, 0.2)

# 12: the passengers bring him coffees. In the tunnel, the folded train behind him: takeaway cups round his feet like candles at a shrine, two more laid
#     down, a woman holds one up to his lips; he sips; his eyelid twitches, his helmet rattles, and the train behind him lurches an inch
D12 = st.dur('S12'); SIP12 = 1.45; TW12 = 1.75; LURCH = 1.8   # (review 1) the lurch with the reprise
ME12 = [8.3, 0, 0.0]
PILE = [[8.62, -0.42], [8.7, -0.18], [8.74, 0.08], [8.7, 0.32], [8.6, 0.52], [8.86, -0.3], [8.9, 0.0], [8.88, 0.28], [8.48, -0.58], [8.47, 0.66]]
NEW = [(0.42, [9.12, 0.42]), (1.08, [9.06, 0.2])]   # (review 1) her cup laid in front, at the left of the frame
LIPS = lambda w: {'touch': {'R': ['@mecC.head', 0.0, 0.11, 0.17, w, 0.03]}, 'hands': {'R': 'grip'}}
TWITCH = [r(TW12 + 0.08 * j) for j in range(8)]
st.shot('S12', 'spaceDark', look=TLOOK, blur=[[TW12, r(TW12 + 0.14), VIB]], blurSamples=5, actors=[
        act('mecC', ME12, 90, 'stand', 'unimpressed', keys=[k(0.0, look=[FACE, 1.9, -0.7]), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.62, toon={'face': {'lid': 1.0}}, toonDur=0.08), k(0.74, toon={'sq': [1.0, 1.008, 1.0], 'face': DEAD}, toonDur=0.12),   # (audit) a slow blink, a breath
            k(SIP12, toon={'face': {'lid': 0.5, 'mouth': 'kiss'}}, toonDur=0.06), k(r(SIP12 + 0.18), toon={'face': {**DEAD, 'gulp': 1.0}}, toonDur=0.12),   # he sips...
            k(TW12, toon={'buzz': 0.04, 'hairUp': 0.9, 'hat': [0.05, 0.0, 0.0], 'face': {**WIRED, 'eye': 0.6}}, toonDur=0.02),   # (review 1) a mini reprise: four frames of ghosts, wired pinhead eyes, the helmet up...
            k(r(TW12 + 0.14), toon={'buzz': 0.0, 'hairUp': 0.0, 'hat': [0.0, 0.0, 0.0], 'face': DEAD}, toonDur=0.03),   # ...and dead still again...
            *[k(t_, toon={'buzz': 0.004 + 0.001 * j, 'hat': [r(0.015 * (j % 2)), 0.0, 0.0], 'face': {'lid': 0.45, 'lidR': (0.55 if j % 2 == 0 else 0.0), 'eyeR': 0.1}}, toonDur=0.03) for j, t_ in enumerate(TWITCH[3:], 3)],   # ...his eyelid twitches, his helmet rattles
            k(r(TWITCH[-1] + 0.1), toon={'buzz': 0.008, 'face': {'lid': 0.45, 'lidR': 0.4, 'eyeR': 0.15}}, toonDur=0.08)]),
        act('voy1', [9.62, -0.26, 0.62], -110, 'stand', 'neutral', keys=[k(0.0, look=[9.12, 0.0, 0.42]), k(0.0, toon={'reach': {'R': [9.12, 0.4, 0.42, 1, 0.03]}, 'bend': {'spine': [0.6, 0, 0, 1, None], 'legL': [-0.9, 0, 0, 1, None], 'shinL': [1.6, 0, 0, 1, None], 'legR': [-0.9, 0, 0, 1, None], 'shinR': [1.6, 0, 0, 1, None]}, 'hands': {'R': 'grip'}}, toonDur=0.0),   # (review 1: a toppling diagonal across him) crouched in front at the left...
            k(0.4, toon={'reach': {'R': [9.12, 0.2, 0.42, 1, 0.03]}, 'bend': {'spine': [0.7, 0, 0, 1, None], 'legL': [-0.9, 0, 0, 1, None], 'shinL': [1.6, 0, 0, 1, None], 'legR': [-0.9, 0, 0, 1, None], 'shinR': [1.6, 0, 0, 1, None]}, 'hands': {'R': 'open'}}, toonDur=0.12),   # she lays her cup down...
            k(0.7, to=[10.6, 0, 1.2], dur=0.9, clip='walk', then='stand', ease='inOut', face='keep'), k(0.7, toon={'face': {'lid': 0.4}}, toonDur=0.2)]),   # ...and walks off at the left   # ...and goes back down the tunnel ((script) toward the camera her head left the frame)
        act('voy2', [6.6, 0, 1.55], 90, 'stand', 'neutral', keys=[k(0.0, look=[9.06, 0.0, 0.2]), k(0.0, to=[9.15, 0, 0.95], dur=0.8, clip='walk', then='stand', ease='out', face='keep'),   # (review 1) inside the frame (the left edge cut him)
            k(0.85, toon={'reach': {'R': [9.06, 0.3, 0.2, 1, 0.03]}, 'bend': {'spine': [0.75, 0, 0, 1, None]}, 'hands': {'R': 'grip'}}, toonDur=0.2), k(1.1, toon={'reach': {'R': [9.06, 0.2, 0.2, 1, 0.03]}, 'bend': {'spine': [0.8, 0, 0, 1, None]}, 'hands': {'R': 'open'}}, toonDur=0.1),
            k(1.45, toon={'face': {'lid': 0.3}}, toonDur=0.3)]),
        act('voy3', [8.62, 0, 0.72], -125, 'stand', 'neutral', keys=[   # (stills 1) at his right side: in front of him she hid him; (stills 2) her face turned more to usk(0.0, look=[ME12[0], 2.0, ME12[2]]), k(0.0, toon={**LIPS(0), 'face': {'lid': 0.3}}, toonDur=0.0),
            k(r(SIP12 - 0.35), toon={**LIPS(1), 'face': {'lid': 0.2, 'brow': 0.4}}, toonDur=0.3, toonEase='inOut'), k(r(SIP12 + 0.35), toon={**LIPS(0), 'face': {'lid': 0.2, 'eye': 0.3, 'brow': 0.6}}, toonDur=0.25)])],
        props=[TUNNEL(), GLOW('glow12', [9.5, 2.3, -1.2], 3.2, 9.0), RIM('rim12', [7.2, 2.5, -0.9], 4.0, 4.0),
               P('nose12', 'metroNose', pos=[r(ME12[0] - 0.25), 0, 0.0], opts={'len': 8, 'crumple': [-1.0, 0.38, 0.09]}, keys=[k(LURCH, to=[r(ME12[0] - 0.13), 0, 0.0], dur=0.06, ease='out')]),
               *[P(f'tc12_{i}', 'takeawayCup', pos=[x_, 0.0, z_], ry=r(-90 + 40 * ((i % 3) - 1)), scale=1.4, opts={'steam': i % 3 == 0}) for i, (x_, z_) in enumerate(PILE)],   # (stills 1) bigger: small dark lids at his feet
               *[P(f'nc12_{i}', 'takeawayCup', pos=[x_, 0.0, z_], ry=-90, opts={'steam': True}, keys=[k(0.0, scale=0.01, dur=0.0), k(t_, scale=1.4, dur=0.1, ease='outBack')]) for i, (t_, (x_, z_)) in enumerate(NEW)],
               P('lip12', 'takeawayCup', on={'actor': 'voy3', 'hand': 'R'}, opts={'steam': True}),
               P('vcup12', 'takeawayCup', on={'actor': 'voy2', 'hand': 'R'}, keys=[k(1.1, scale=0.01, dur=0.0)])],
        cams=[FC(0.0, [11.4, 1.6, -1.7], [[ME12[0], 2.5, ME12[2]], [8.6, 0.0, 0.66], [8.62, 2.2, 0.72], [7.4, 2.35, 0.0], [9.62, 0.0, 0.62]],
                 top=0.1, bottom=0.74, lenses=range(24, 60), inside=TIN, drift=(-0.05, 0.0, 0.05)),
              FC(r(TW12 - 0.12), [10.4, 1.95, -0.8], [[ME12[0], 2.55, ME12[2]], [ME12[0], 1.25, ME12[2]], [r(ME12[0] - 0.4), 2.3, -0.3], [r(ME12[0] + 0.3), 1.6, 0.5]], top=0.12, bottom=0.78, lenses=range(24, 60), inside=TIN)])   # (review 1) closer for the reprise and the twitch (his face was 12 % of the width)
st.cue('sfx:stepSoft', 'S12', 0.2, 0.12); st.cue('pop', 'S12', 0.42, 0.15); st.cue('pop', 'S12', 1.08, 0.15); st.cue('sfx:sniff', 'S12', SIP12, 0.2)
st.cue('sfx:rattleShort', 'S12', TW12, 0.28); st.cue('clang', 'S12', LURCH, 0.2)


# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 1.6, 'mec', 'tower'), ('S02', 1.0, 'mec', 'buzz'), ('S03', 0.9, 'mec', 'wall'), ('S04', 0.5, 'maire', 'shake'), ('S05', 0.8, 'mecC', 'drill'),
           ('S09', 0.6, 'mecC', 'stop'), ('S10', 0.6, 'mecC', 'crumple'), ('S12', 1.9, 'mecC', 'twitch')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
st.card('S04', 'EMBAUCHÉ', at=0.4)
st.card('S08', 'DÉCA', at=1.28)
st.card('S11', 'BLOQUÉE', at=0.55)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}
st.write("Le café", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec', 'mecC'], extra_cast={
    'mec': MEC,
    'mecC': {**MEC, 'hat': 'hardhat'},
    'mamie': {'preset': 'mamie', 'seed': 631, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 632, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ouv': {'preset': 'worker', 'seed': 633, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'serveur': {'preset': 'serveur', 'seed': 634, 'build': {'width': 0.9, 'headWidth': 1.2}, 'toon': EX},
    'voy1': {'preset': 'madame', 'seed': 635, 'suit': '#3A9BDC', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'voy2': {'preset': 'lyceen', 'seed': 636, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'voy3': {'preset': 'femme', 'seed': 637, 'suit': '#C255C8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'voy4': {'preset': 'tourist', 'seed': 638, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
