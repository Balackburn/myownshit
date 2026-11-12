#!/usr/bin/env python3
"""Le radar (story 46, cycle 8 of the cartoon staging): this man ran for his bus. A speed camera flashed him: thirty-one kilometres an hour, in a thirty
zone. He contested: he is on foot. The prefecture ruled: above thirty, a pedestrian is a vehicle. He got a number plate. Then a summons to the technical
inspection. The tyres, fine. The horn, fine. The brakes: refused. Since then he may no longer walk. The bus pushes him every morning. He never misses it.
Staging: every gag treats his body as a car: the flash freezes him mid-stride like a speed-camera photo, the plate screwed onto his back (a jolt per
screw), the lift that takes him up by the armpits, the tyre kick (his leg wobbles), the horn squeezed out of his nose, the brake rollers that throw him
through the wall (his outline left in it), the wheel chocks he rocks on, and the bus that pushes him along with his coffee.
Pass 2 (review 1: animation 5.5, art 5.5): the hook from the bus stop (he runs at us, the bus closes its doors and leaves); the freeze clear of the
pole and drained for its whole length; the display blinks inside a lit housing; the sole on the counter and the letter turned to us; a crank that
sticks at 30 then snaps past; the wheel at ten to two, frontal; the lift that really lifts him; a rubber-leg kick into his shoe and a thumbs-up to us;
he runs facing us on the rollers, the lever in view; the hole on impact; a real rock on the chocks; stiff in front of the bus, a sip; the stop at the
pole, the toast, the doors opening for the others."""
from story_kit import *
import math

st = Story('radar', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 4), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L05', 7),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L08', 4), ('S12', 'L09', 0), ('S13', 'L09', 2), ('S14', 'L10', 0),
         ('S15', 'L11', 0), ('S16', 'L12', 0)])

STREET = {'clear': [-60, 60], 'eiffel': False, 'paveW': 6.5}
def FC(t, frm, pts, top=0.14, bottom=0.82, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), inside=None, **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, inside=inside, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
PX = 6.4                                                           # he runs along the right-hand pavement (x 5..11.5), toward +Z
BUSX = 3.1
BUS = lambda z, keys=None, **o: P('bus', 'cityBus', pos=[BUSX, 0, z], ry=-90, opts={'len': 7.6, 'line': '12', 'dest': 'GARE', 'top': 2.65, **o}, **({'keys': keys} if keys else {}))
SHELTER = lambda z=6.0: P('shelter', 'busStop', pos=[7.9, 0, z], ry=-90)
CUP = lambda: P('cup', 'mug', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.02, 0.04]})
PLATE = lambda: P('plateB', 'licensePlate', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.42, -0.2], 'rot': [0, math.pi, 0]}, opts={'text': 'PI-031-ON', 'w': 0.48})   # on his back, (pass 2) turned to face backward (its dark back showed)

# 1: the hook. The street: his bus is at the stop down there, its doors closing; he comes running along the pavement, legs a blur, tie flying
D1 = st.dur('S01')
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [PX, 0, -3.5], 0, 'stand', 'determined', keys=[k(0.0, look=[BUSX, 1.6, 10.0]), k(0.0, to=[PX, 0, 5.2], dur=D1, clip='run', then='run', ease='linear', face=0, cadence=3.4),
            k(0.0, toon={'lay': [0.22, 0], 'face': {'tongue': 1, 'tongueYaw': 1.2, 'brow': 0.9, 'eye': 0.35}}, toonDur=0.0)])],   # (pass 2) leaning into the run, tongue blown aside, eyes on the bus
        props=[SHELTER(8.0), BUS(9.0, doors=[[0.0, 1], [0.35, 0]], keys=[k(0.75, to=[BUSX, 0, 17.0], dur=round(D1 - 0.75 + 0.6, 3), ease='in')])],   # (pass 2) the doors close in his face, it leaves
        cams=[cam(0.0, [4.75, 0.9, 14.2], [4.72, 0.92, 13.8], [6.2, 1.3, 2.0], [6.2, 1.3, 3.0], lens=52)])   # (pass 2) from behind the bus's right flank: the bus at the left closes its doors and goes; he runs at us
st.cue('sfx:stepRun', 'S01', 0.1, 0.3); st.cue('sfx:stepRun', 'S01', 0.4, 0.3); st.cue('sfx:stepRun', 'S01', 0.7, 0.3); st.cue('sfx:carDoor', 'S01', 0.5, 0.2); st.cue('engine', 'S01', 0.9, 0.2, 1.0)

# 2: a speed camera flashed him. He sprints past the camera on its pole: flash: the picture freezes on him in mid-air, legs split, tongue out (the
#    speed-camera photo, colours drained)
D2 = st.dur('S02'); FL2 = round(st.at('S02', 'L02', 3), 3)
RAD = [5.25, 0, 3.4]                                                # (pass 2) ahead of him: at the flash he is well clear of the pole
st.shot('S02', 'parisStreet', setOpts=STREET, freeze={'at': FL2 + 0.03, 'filter': 'saturate(0.18) sepia(0.25) contrast(1.08) brightness(1.05)'}, actors=[   # (pass 2) the photo drained for the whole freeze
        act('mec', [PX, 0, -2.4], 0, 'stand', 'determined', keys=[k(0.0, look=[BUSX, 1.6, 12.0]), k(0.0, to=[PX, 0.0, 4.2], dur=round(D2 + 0.4, 3), clip='dashOff', then='dashOff', ease='linear', face=0),
            k(0.0, toon={'face': {'tongue': 1, 'tongueYaw': 1.3, 'brow': 0.9}}, toonDur=0.0), k(FL2 - 0.04, toon={'face': {'tongue': 1, 'tongueYaw': 1.3, 'brow': 1, 'pop': 0.5}}, toonDur=0.04)])],
        props=[P('radar', 'speedCamera', pos=RAD, ry=180, opts={'flashAt': FL2})],
        fx=[{'type': 'flash', 'at': FL2, 'dur': 0.18}],
        cams=[FC(0.0, [3.4, 1.35, -0.2], [[RAD[0], 2.95, RAD[2]], [RAD[0], 1.6, RAD[2]], [PX, 2.3, -0.3], [PX, 0.0, 0.6], [PX, 1.2, -1.2]], top=0.1, bottom=0.74)])   # (pass 2) close in front of the speed camera: its lens and flash to us, him beside it
st.cue('sfx:stepRun', 'S02', 0.05, 0.3); st.cue('sfx:stepRun', 'S02', 0.25, 0.3); st.cue('sfx:cash', 'S02', FL2, 0.0); st.cue('pop', 'S02', FL2, 0.5); st.cue('whoosh', 'S02', FL2 - 0.05, 0.1, 0.12, 2000, 6000)

# 3: thirty-one kilometres an hour. The speed display on its pole: 31 in big red digits, a smile... that turns down and blinks
D3 = st.dur('S03'); SAD3 = 0.55
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('display', 'speedDisplay', pos=[5.3, 0, 3.0], ry=180, opts={'speed': '31', 'showAt': 0.0, 'sadAt': SAD3}), P('radar', 'speedCamera', pos=RAD, ry=180)],
        cams=[cam(0.0, [3.75, 2.15, 1.25], [3.8, 2.17, 1.4], [5.3, 2.38, 3.0], [5.3, 2.38, 3.0], lens=30)])   # (first look) off the speed camera's box (inside it the frame was black)
st.cue('sfx:beep', 'S03', 0.05, 0.3); st.cue('sfx:beep', 'S03', SAD3, 0.3); st.cue('sfx:beep', 'S03', SAD3 + 0.25, 0.3)

# 4: in a thirty zone. He has stopped by the sign (ZONE 30): he looks up at it, points at it, then at himself, his eyebrows up: me?
D4 = st.dur('S04'); ME4 = [PX - 0.4, 0, 6.0]
SIGN4 = [5.35, 0, 6.6]
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME4, -60, 'stand', 'unimpressed', keys=[k(0.0, look=[SIGN4[0], 2.6, SIGN4[2]]),
            k(0.25, toon={'reach': {'R': [round(SIGN4[0] + 0.35, 3), 2.25, round(SIGN4[2] - 0.15, 3), 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.6}}, toonDur=0.12, toonEase='outBack'),
            k(0.62, look='camera'), k(0.62, toon={'reach': {'R': [round(ME4[0] - 0.12, 3), 1.45, round(ME4[2] + 0.22, 3), 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 1, 'eye': 0.45}}, toonDur=0.1, toonEase='out'),
            k(0.62, expr='surprised')])],
        props=[P('zone', 'zoneSign', pos=SIGN4, ry=-90, opts={'text': '30', 'top': 'ZONE'})],
        cams=[FC(0.0, [3.4, 1.6, 4.4], [[ME4[0], 2.35, ME4[2]], [ME4[0], 0.0, ME4[2]], [SIGN4[0], 3.3, SIGN4[2]]], top=0.1, bottom=0.74, drift=(0.06, 0, -0.06))])   # (pass 2) the feet above the caption band

# ---- the prefecture: the town-hall set repainted, PRÉFECTURE over the counter; the official in his sash behind the desk
PREF = {'wall': '#E8EEF2', 'band': '#2F5E9E', 'trim': '#1E3E7B', 'floor': '#B7B3AA', 'joint': '#9F9B92', 'banner': True, 'title': 'PRÉFECTURE', 'map': False, 'deskZ': -1.25, 'plate': 'PRÉFECTURE',
        'front': 3.6, 'frontSign': {'text': 'PRÉFECTURE', 'x': 0.0, 'y': 2.5, 'w': 1.9}}
OFFI = [0.0, 0, -1.85]; MEP = [0.15, 0, -0.2]
GAUGE = [-1.25, 1.6, -2.55]
IDLEO = [k(0.55, toon={'face': {'gy': -0.6}}, toonDur=0.08), k(0.8, toon={}, toonDur=0.1), k(1.3, toon={'face': {'lid': 0.4}}, toonDur=0.06), k(1.42, toon={}, toonDur=0.06)]   # (pass 2) a glance down, a slow blink: never a frozen hold
OFFICIAL = lambda keys=(), idle=True: act('prefet', OFFI, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[MEP[0], 1.9, MEP[2]]), *(IDLEO if idle else []), *keys])   # (toon keys are whole states: no idle keys under a hand that works)

# 5: he contested: he is on foot. At the counter he slaps down his letter, then lifts a foot and shows the official the sole of his shoe
D5 = st.dur('S05'); SL5, SH5 = 0.15, round(st.at('S05', 'L04', 4) - 0.08, 3)
st.shot('S05', 'mairie', setOpts=PREF, actors=[OFFICIAL(),
        act('mec', MEP, 180, 'stand', 'determined', keys=[k(0.0, look=[OFFI[0], 2.0, OFFI[2]]),
            k(0.0, toon={'reach': {'R': [0.25, 2.05, -0.35, 1, 0.06]}, 'hands': {'R': 'flat'}, 'lay': [-0.06, 0]}, toonDur=0.0),                       # (pass 2) wound up: the hand high, leaning back
            k(SL5 - 0.06, toon={'reach': {'R': [0.05, 0.9, -0.85, 1, 0.06]}, 'hands': {'R': 'flat'}, 'lay': [0.08, 0]}, toonDur=0.06, toonEase='in'),   # slap
            k(SL5 + 0.08, toon={'reach': {'R': [0.05, 0.95, -0.82, 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.08), k(SL5 + 0.3, toon={}, toonDur=0.15),
            k(SH5, clip='showSole', blend=0.12), k(SH5, look=[OFFI[0], 1.9, OFFI[2]]), k(round(SH5 + 0.35, 3), look='camera')])],   # (pass 2) the sole up on the counter, toward him and us
        props=[P('letter', 'paperSheet', pos=[0.05, 0.98, -0.85], face='camera', opts={'w': 0.3, 'h': 0.4, 'head': 'CONTESTATION', 'lines': ['Je suis à pied.'], 'lineSize': 0.09, 'bright': True}, keys=[k(0.0, scale=0.01, dur=0.0), k(SL5, scale=1.0, dur=0.05)]),   # (pass 2) turned to us
               P('sole5', 'shoeSole', on={'actor': 'mec', 'joint': 'footR', 'offset': [0.0, -0.06, 0.04]}, opts={'tread': True, 'color': '#E8DFC8', 'len': 0.3, 'w': 0.11}, keys=[k(0.0, visible=False), k(SH5, visible=True)])],
        cams=[FC(0.0, [0.8, 1.6, -2.4], [[MEP[0], 2.35, MEP[2]], [MEP[0], 0.0, MEP[2]], [0.05, 1.2, -0.85], [0.6, 1.0, -0.5]], top=0.12, bottom=0.74, lenses=range(22, 80), inside=(-3.0, 3.0, 0.3, 3.4, -2.45, 3.4))])   # (pass 2) over the official's shoulder: the slap, the letter and the sole come at us
st.cue('thud', 'S05', SL5, 0.35); st.cue('sfx:paper', 'S05', SL5, 0.3)

# 6: the prefecture ruled: above thirty... The official turns to the big gauge on the wall and cranks the needle: 10, 20, 30... past 30 the green lamp
#    PIÉTON goes out and the red VÉHICULE lights
D6 = st.dur('S06'); OV6 = round(st.at('S06', 'L05', 5) - 0.05, 3)   # (pass 2) the swap a word earlier: the red lamp held 0.7 s
CRK6 = lambda: [[0.35, round(OV6 - 0.2, 3), 4.0], [round(OV6 - 0.2, 3), OV6, 1.4]]   # the crank: four turns, then one and a half fast past the sticking point
def CRANKA(t):
    a = 0.0
    for a0, a1, n in CRK6():
        if t <= a0: break
        a += 2 * math.pi * n * min(1.0, max(0.0, (t - a0) / max(0.01, a1 - a0)))
    return a
CRANKH = lambda t: [round(GAUGE[0] + 0.62 + 0.12 * math.cos(CRANKA(t)), 3), round(GAUGE[1] - 0.35 + 0.12 * math.sin(CRANKA(t)), 3), round(GAUGE[2] + 0.14, 3), 1, 0.05]   # his hand on the knob
st.shot('S06', 'mairie', setOpts=PREF, actors=[
        OFFICIAL(idle=False, keys=[k(0.05, look=GAUGE), k(0.15, toon={'reach': {'R': CRANKH(0.0)}, 'hands': {'R': 'grip'}}, toonDur=0.15),
            *[k(t, toon={'reach': {'R': CRANKH(t)}, 'hands': {'R': 'grip'}, **({'lay': [0.1, 0], 'face': {'brow': 1, 'puff': 0.6}} if OV6 - 0.45 < t < OV6 else {})}, toonDur=0.06)
              for t in [round(0.35 + 0.07 * i, 3) for i in range(int((OV6 - 0.35) / 0.07) + 1)]],   # (pass 2) turning the crank (the hand on its knob); a heave where it sticks at 30
            k(OV6 + 0.1, look=[MEP[0], 1.9, MEP[2]]), k(OV6 + 0.15, toon={'reach': {'R': [round(GAUGE[0] + 0.4, 3), 2.0, round(GAUGE[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.6}}, toonDur=0.12)])],
        props=[P('gauge', 'speedGauge', pos=GAUGE, opts={'needle': [[0.35, 12.0], [round(0.35 + (OV6 - 0.35) * 0.4, 3), 24.0], [round(OV6 - 0.45, 3), 29.6], [round(OV6 - 0.2, 3), 30.0], [OV6, 36.0], [round(OV6 + 0.18, 3), 32.0]],   # (pass 2) stuck at 30, then past it with a jump
                 'crank': CRK6()})],
        cams=[FC(0.0, [-0.2, 1.7, -0.1], [[GAUGE[0] - 0.55, 2.4, GAUGE[2]], [GAUGE[0] + 0.55, 0.9, GAUGE[2]], [OFFI[0], 2.45, OFFI[2]], [OFFI[0] + 0.35, 2.3, OFFI[2]], [OFFI[0], 0.6, OFFI[2]]], top=0.12, bottom=0.76, margin=0.1)])   # (pass 2) the official's head well inside
st.cue('sfx:ticks', 'S06', 0.35, 0.25); st.cue('sfx:bell', 'S06', OV6, 0.4)

# 7: a pedestrian is a vehicle. Close on him under the red light: he looks at his hands, then holds an invisible steering wheel and turns it, puzzled
D7 = st.dur('S07')
WHEEL7 = lambda a: {'reach': {'L': [round(MEP[0] + 0.24 * math.cos(2 * math.pi / 3 - a), 3), round(1.38 + 0.24 * math.sin(2 * math.pi / 3 - a), 3), round(MEP[2] - 0.42, 3), 1, 0.06],
                               'R': [round(MEP[0] + 0.24 * math.cos(math.pi / 3 - a), 3), round(1.38 + 0.24 * math.sin(math.pi / 3 - a), 3), round(MEP[2] - 0.42, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}}   # (pass 2) ten to two (he faces -Z: his right is +X), a turns the wheel
st.shot('S07', 'mairie', setOpts=PREF, actors=[
        act('mec', MEP, 180, 'stand', 'worried', keys=[k(0.0, look=[MEP[0], 1.3, MEP[2] - 0.5]), k(0.0, toon={**WHEEL7(0.0), 'face': {'brow': 0.6}}, toonDur=0.0),
            *[k(round(0.2 + 0.24 * i, 3), toon={**WHEEL7(0.8 * (1 if i % 2 == 0 else -1)), 'face': {'brow': 0.7, 'gy': -0.4, 'gx': 0.5 * (1 if i % 2 == 0 else -1)}}, toonDur=0.2, toonEase='inOut') for i in range(6)],   # a quarter turn each way, the eyes after the hands
            k(0.7, look='camera')])],
        props=[],
        look={'fill': 1.6},
        cams=[FC(0.0, [round(MEP[0] + 0.25, 3), 1.7, round(MEP[2] - 2.0, 3)], [[MEP[0], 2.35, MEP[2]], [MEP[0], 1.0, MEP[2]], [MEP[0] - 0.35, 1.6, MEP[2] - 0.42], [MEP[0] + 0.35, 1.6, MEP[2] - 0.42]], top=0.14, bottom=0.7)])   # (pass 2) frontal; filled like the shots before

# 8: he got a number plate. Seen from behind: the official screws a plate onto his back with an electric screwdriver: four screws, a jolt at each
D8 = st.dur('S08'); SCR8 = (0.25, 0.5, 0.75, 1.0)
BACK8 = [MEP[0], 1.75, round(MEP[2] - 0.22, 3)]
st.shot('S08', 'mairie', setOpts=PREF, actors=[
        act('mec', MEP, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[MEP[0], 1.6, MEP[2] + 3.0]), *[k(t, toon={'sq': [0.95, 1.07, 0.95], 'face': {'brow': 0.9, 'eye': 0.4}}, toonDur=0.03) for t in SCR8],
            *[k(round(t + 0.08, 3), toon={'face': {'lid': 0.3}}, toonDur=0.06) for t in SCR8]]),
        act('prefet', [round(MEP[0] + 0.9, 3), 0, round(MEP[2] - 0.75, 3)], -55, 'stand', 'determined', keys=[k(0.0, look=BACK8),   # (pass 2) further out at his back-left: a gap between the two navy suits
            *[k(t, toon={'reach': {'R': [round(BACK8[0] + (0.15 if i % 2 else -0.15), 3), round(BACK8[1] + (0.06 if i < 2 else -0.06), 3), round(BACK8[2] - 0.08, 3), 1, 0.06]}, 'hands': {'R': 'grip'}, 'hose': 0.15}, toonDur=0.08) for i, t in enumerate(SCR8)]])],
        props=[PLATE(), P('drill', 'marker', on={'actor': 'prefet', 'hand': 'R', 'offset': [0, -0.02, 0.08]}, scale=2.2, opts={'color': '#F2C230'})],   # (pass 2) a screwdriver that reads
        look={'fill': 1.6},
        cams=[FC(0.0, [-1.3, 1.8, -2.2], [[MEP[0], 2.35, MEP[2]], [MEP[0], 0.9, MEP[2]], BACK8, [round(MEP[0] + 0.62, 3), 2.2, round(MEP[2] - 0.55, 3)]], top=0.14, bottom=0.7, inside=(-3.0, 3.0, 0.3, 3.4, -2.45, 3.4))])   # (first look) from his back-right: the plate and the official's face
[st.cue('sfx:zip', 'S08', t, 0.35) for t in SCR8]

# ---- the garage of the technical inspection (whiteVoid + garageBay): the lift at the middle, the brake rollers at the right, the back wall ahead
GZ = 0.0
LIFT = lambda keys=None, **o: P('lift', 'carLift', pos=[-1.2, 0, GZ], opts={'gap': 2.0, 'armIn': 0.55, **o})
ROLL = lambda **o: P('rollers', 'brakeRollers', pos=[1.9, 0, 0.6], opts=o)
GAR = lambda back=True: [P('garage', 'garageBay', noCamCheck=True, opts={'w': 8, 'd': 7, 'back': back}), LIFT(), ROLL()]
MECA = lambda pos, ry, keys=(): act('meca', pos, ry, 'stand', 'neutral', keys=list(keys))

# 9: then a summons to the technical inspection. The garage (CONTRÔLE TECHNIQUE): he stands between the posts of the lift, the arms under his armpits;
#    the lift takes him up, stiff as a post, his feet dangling; the mechanic with his clipboard
D9 = st.dur('S09'); UP9 = 0.35; RISE9 = round(D9 - UP9 - 0.2, 3)
_ss = lambda u: u * u * (3 - 2 * u)
LIFTK9 = [[round(UP9 + RISE9 * i / 10, 3), round(1.37 + 1.1 * _ss(i / 10), 3)] for i in range(11)]   # (pass 2) the carriage under his armpits all the way up (it sat at his waist: he floated)
st.shot('S09', 'whiteVoid', actors=[
        act('mec', [-1.2, 0, GZ], 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look='camera'), k(UP9, to=[-1.2, 1.1, GZ], dur=RISE9, clip='stiffStand', then='stiffStand', glide=True, ease='inOut'),
            k(UP9, toon={'sq': [1.06, 0.94, 1.06], 'face': {'eye': 0.4}}, toonDur=0.04), k(UP9 + 0.08, toon={'face': {'gy': -0.8, 'brow': 0.6}}, toonDur=0.1),   # a jolt as it catches him, his eyes go down
            k(round(UP9 + RISE9, 3), toon={'sq': [0.96, 1.04, 0.96], 'face': {'gy': -0.6, 'brow': 0.7}}, toonDur=0.05), k(round(UP9 + RISE9 + 0.1, 3), toon={'face': {'brow': 0.5}}, toonDur=0.08)]),   # a bounce at the top
        MECA([1.1, 0, 0.6], -110, keys=[k(0.0, look=[-1.2, 2.2, GZ]), k(0.4, look=[-1.2, 3.2, GZ]), k(0.9, toon={'reach': {'R': [0.85, 1.25, 0.45, 1, 0.06]}, 'hands': {'R': 'pinch'}}, toonDur=0.1),
            *[k(round(1.0 + 0.1 * i, 3), toon={'reach': {'R': [round(0.85 + (0.05 if i % 2 else -0.05), 3), 1.24, 0.45, 1, 0.06]}, 'hands': {'R': 'pinch'}}, toonDur=0.08) for i in range(6)], k(1.6, look=[-1.2, 3.6, GZ])])],   # (pass 2) beside the lift, writing, looking up   # (pass 2) he writes on his clipboard, looks up
        props=[P('garage', 'garageBay', noCamCheck=True, opts={'w': 8, 'd': 7, 'signY': 3.88, 'signX': -1.2, 'signW': 3.2}), LIFT(lift=LIFTK9, h0=1.37), ROLL(), P('clip', 'clipboardProp', on={'actor': 'meca', 'hand': 'L', 'offset': [0, 0, 0.05]})],
        cams=[FC(0.0, [-1.2, 1.3, 3.3], [[-2.8, 4.15, -3.5], [0.4, 3.6, -3.5], [-1.2, 0.0, GZ], [-1.2, 2.4, GZ]], top=0.05, bottom=0.78, margin=0.04, lenses=range(22, 84), inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 3.3)),   # (pass 2) the whole sign over the lift
              FC(0.5, [1.4, 2.0, 3.3], [[-1.2, 3.6, GZ], [-1.2, 1.0, GZ], [-2.0, 2.6, GZ], [-0.4, 2.6, GZ], [1.1, 1.8, 0.6]], top=0.1, bottom=0.76, lenses=range(22, 84), inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 3.3))])   # then the lift: its arms under his armpits all the way up   # (pass 2) inside the garage; the whole sign over the cross-bar
st.cue('engine', 'S09', UP9, 0.2, 1.4); st.cue('sfx:squeak', 'S09', UP9, 0.2)

# 10: the tyres, fine. Low, at his dangling shoes: the mechanic kicks one: the leg wobbles like rubber; a thumbs-up
D10 = st.dur('S10'); KK10 = (0.18, 0.62)
FOOT10 = [-1.08, 1.12, GZ + 0.12]
WAG10 = lambda t0: [k(round(t0 + d, 3), toon={'bend': {'legR': [a, 0, 0, 1.15, None], 'shinR': [-a * 0.9, 0, 0, 1.15, None]}, 'wave': {'legR': [0.06 * abs(a), 1.0, d * 3, 1], 'shinR': [0.06 * abs(a), 1.0, d * 3 + 0.3, 1]}}, toonDur=0.05)
                    for d, a in ((0.0, 0.0), (0.04, 0.95), (0.11, -0.72), (0.18, 0.5), (0.25, -0.3), (0.32, 0.14), (0.4, 0.0))]   # (pass 2) a rubber leg: four decaying swings
st.shot('S10', 'whiteVoid', actors=[
        act('mec', [-1.2, 1.1, GZ], 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look=[0.0, 1.6, 5.0]), *WAG10(KK10[0]), *WAG10(KK10[1])]),
        MECA([-0.55, 0, 0.78], -140, keys=[k(0.0, look=FOOT10),
            *[x for t in KK10 for x in (k(round(t - 0.12, 3), toon={'bend': {'legR': [0.5, 0, 0, 1, None], 'shinR': [0.6, 0, 0, 1, None]}, 'lay': [-0.05, 0]}, toonDur=0.07),                       # wind-up: the leg back
                                        k(round(t - 0.03, 3), toon={'bend': {'legR': [-1.7, 0, 0, 1.08, None], 'shinR': [0.0, 0, 0, 1.08, None]}, 'lay': [-0.12, 0]}, toonDur=0.03, toonEase='out'),   # the kick: straight up into the shoe
                                        k(round(t + 0.1, 3), toon={'bend': {'legR': [-1.2, 0, 0, 1, None]}, 'wave': {'legR': [0.05, 1.0, 0.5, 1]}}, toonDur=0.08), k(round(t + 0.22, 3), toon={}, toonDur=0.1))],
            k(0.85, face=15, turn=0.18), k(0.95, toon={'reach': {'R': [-0.25, 1.95, 1.12, 1, 0.06]}, 'hands': {'R': 'thumbUp'}, 'face': {'brow': 0.4}}, toonDur=0.08, toonEase='outBack'), k(0.95, look='camera')])],   # (pass 2) he turns to us: a thumbs-up at face height
        props=[P('garage', 'garageBay', noCamCheck=True, opts={'w': 8, 'd': 7, 'signY': 3.88, 'signX': -1.2, 'signW': 3.2}), LIFT(h0=2.47), ROLL()],
        cams=[FC(0.0, [-0.5, 1.05, 3.2], [[-1.2, 2.6, GZ], [-1.2, 1.0, GZ], [-0.55, 2.25, 0.78], [-0.55, 0.0, 0.78], [-0.25, 2.05, 1.12]], top=0.1, bottom=0.76, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])   # (pass 2) from the front, between the posts: the shoe, the rubber leg, the thumbs-up
[st.cue('sfx:bonk', 'S10', t, 0.35) for t in KK10]; [st.cue('sfx:twang', 'S10', t + 0.02, 0.25) for t in KK10]

# 11: the horn, fine. The mechanic squeezes his nose: HONK: his head squashes, his eyes pop, his cheeks blow out; again; a tick on the clipboard
D11 = st.dur('S11'); HN11 = (0.2, 0.68)
NOSE11 = [-1.2, 3.05, round(GZ + 0.2, 3)]
st.shot('S11', 'whiteVoid', actors=[
        act('mec', [-1.2, 1.1, GZ], 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look=[0.0, 3.0, 5.0]),
            *[x for i, t in enumerate(HN11) for x in (k(t, toon=({'scl': {'head': [1.3, 0.78, 1.15]}, 'face': {'pop': 0.6, 'brow': 1, 'puff': 1, 'cheeks': 1}} if i == 0 else
                                                               {'scl': {'head': [0.82, 1.38, 0.9]}, 'bend': {'neck': [0, 0, 0, 1.6, None]}, 'face': {'pop': 0.85, 'popLen': 0.3, 'brow': 1, 'jaw': 0.4}}), toonDur=0.03, toonEase='out'),   # (pass 2) the second honk: up, not out
                                                    k(round(t + 0.16, 3), toon={'face': {'lid': 0.35}}, toonDur=0.1))]]),
        MECA([-0.75, 1.15, 0.85], -150, keys=[k(0.0, look=NOSE11), *[k(round(t - 0.1, 3), toon={'reach': {'R': [*NOSE11, 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.1) for t in HN11],
            *[k(round(t + 0.12, 3), toon={'reach': {'R': [round(NOSE11[0] + 0.25, 3), 2.9, round(NOSE11[2] + 0.35, 3), 1, 0.06]}, 'hands': {'R': 'spread'}}, toonDur=0.1) for t in HN11]])],
        props=[P('garage', 'garageBay', noCamCheck=True, opts={'w': 8, 'd': 7, 'signY': 3.88, 'signX': -1.2, 'signW': 3.2}), LIFT(h0=2.47), P('step', 'cardboardBox', pos=[-0.75, 0, 0.85], opts={'w': 0.8, 'h': 1.15, 'd': 0.7}),
               *[P(f'ring{i}', 'impactStars', pos=[NOSE11[0], NOSE11[1], NOSE11[2] + 0.1], opts={'at': t, 'n': 6, 'r': 0.32, 'r0': 0.12, 'dur': 0.28, 'size': 0.06}) for i, t in enumerate(HN11)]],
        cams=[FC(0.0, [-2.6, 3.0, 2.2], [[-1.2, 3.75, GZ], [-1.2, 2.35, GZ], [-0.75, 3.3, 0.85]], top=0.14, bottom=0.7, margin=0.14, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])   # his face three-quarter, the mechanic in profile; (pass 2) off the left edge
[st.cue('sfx:honk', 'S11', t, 0.5) for t in HN11]

# 12: the brakes... On the brake rollers he runs like mad on the spot, legs a blur; the mechanic pulls the lever: the rollers stop dead
D12 = st.dur('S12'); STOP12 = round(D12 - 0.12, 3)
RX = 1.9
LEVER12 = lambda k_: [round(RX + 0.7 + 0.6, 3), round(1.1 + 0.56 * math.cos(-0.5 + 1.3 * k_), 3), round(0.62 + 0.56 * math.sin(-0.5 + 1.3 * k_), 3)]   # the lever's knob, up (0) and pulled (1)
st.shot('S12', 'whiteVoid', actors=[
        act('mec', [RX, 0.06, 0.6], 0, 'stand', 'determined', keys=[k(0.0, look='camera'), k(0.0, clip='scramble', params={'dur': 3.0, 'freq': 11, 'expr': 'determined'})]),   # (pass 2) facing us
        MECA([RX + 1.75, 0, 0.85], -105, keys=[k(0.0, look=[RX, 1.6, 0.6]), k(round(STOP12 - 0.16, 3), look=LEVER12(0.0)), k(round(STOP12 - 0.12, 3), toon={'reach': {'R': [*LEVER12(0.0), 1, 0.05]}, 'hands': {'R': 'grip'}}, toonDur=0.08, toonEase='in'),
            k(STOP12, toon={'reach': {'R': [*LEVER12(1.0), 1, 0.05]}, 'hands': {'R': 'grip'}, 'lay': [-0.06, 0]}, toonDur=0.08, toonEase='out')])],   # (pass 2) he pulls the lever, in view
        props=[P('garage', 'garageBay', noCamCheck=True, opts={'w': 8, 'd': 7, 'signY': 3.88, 'signX': -1.2, 'signW': 3.2}), LIFT(h0=0.15), ROLL(spin=[[0.0, 6.0], [STOP12, 0.0]], lampAt=STOP12, leverAt=STOP12)],
        cams=[FC(0.0, [round(RX - 0.5, 3), 1.35, 4.2], [[RX, 2.4, 0.6], [RX, 0.0, 0.6], [RX + 1.75, 2.2, 0.85], [RX + 1.3, 1.7, 0.62], [RX - 0.8, 0.0, 0.2]], top=0.12, bottom=0.76, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])   # (pass 2) from the front: his face, the rollers, the lever
st.cue('sfx:engine', 'S12', 0.0, 0.0); st.cue('engine', 'S12', 0.0, 0.25, D12); [st.cue('sfx:squeak', 'S12', round(0.1 + 0.15 * i, 3), 0.15) for i in range(4)]; st.cue('clang', 'S12', STOP12, 0.4)

# 13: refused. He shoots off the rollers, stiff, flat out, through the back wall: a hole in his shape; bricks; the mechanic stamps REFUSÉ on his sheet
D13 = st.dur('S13'); HIT13 = 0.12
st.shot('S13', 'whiteVoid', actors=[
        act('mec', [RX, 0.06, 0.6], 0, 'stiffStand', 'surprised', keys=[k(0.0, look=None), k(0.0, toon={'sq': [0.9, 1.05, 1.3], 'reach': {'L': [RX - 0.75, 2.7, 0.4, 1, 0.06], 'R': [RX + 0.75, 2.7, 0.4, 1, 0.06]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'pop': 0.6, 'brow': 1}}, toonDur=0.0),   # (pass 2) arms up: the shape of the hole
            k(0.0, to=[round(RX - 0.4, 3), 0.15, -3.3], dur=HIT13, glide=True, ease='in', face=0), k(HIT13, visible=False)]),   # backward into the wall, facing us
        MECA([RX + 1.75, 0, 0.85], -105, keys=[k(0.0, look=[RX - 0.4, 1.3, -3.6]), k(0.3, toon={'reach': {'L': [RX + 1.45, 1.62, 0.95, 1, 0.06]}, 'hands': {'L': 'pinch'}}, toonDur=0.12), k(0.45, look=[RX + 1.45, 1.6, 0.95]),
            k(0.5, toon={'reach': {'L': [RX + 1.45, 1.62, 0.95, 1, 0.06], 'R': [RX + 1.45, 1.72, 1.0, 1, 0.06]}, 'hands': {'L': 'pinch', 'R': 'flat'}}, toonDur=0.08, toonEase='in'),
            k(0.66, toon={'reach': {'L': [RX + 1.45, 1.62, 0.95, 1, 0.06]}, 'hands': {'L': 'pinch'}}, toonDur=0.1), k(0.7, look='camera')])],   # (pass 2) the sheet held up at chest height, stamped, shown
        props=[P('garage', 'garageBay', opts={'w': 8, 'd': 7, 'back': False, 'signY': 3.88, 'signX': -1.2, 'signW': 3.2}), P('wall13', 'burstWall', pos=[0.0, 0, -3.5], opts={'w': 8.0, 'h': 4.2, 'burstAt': HIT13, 'holeX': RX - 0.4, 'holeY': 1.4, 'holeScale': 1.05, 'color': '#E3E1DA'}),   # (pass 2) the hole the instant he hits
               LIFT(h0=0.15), ROLL(lampAt=0.0), P('sheet13', 'paperSheet', on={'actor': 'meca', 'hand': 'L', 'offset': [0, 0.02, 0.06], 'face': 'camera'}, opts={'w': 0.3, 'h': 0.4, 'head': 'CONTRÔLE', 'lines': ['Pneus : OK', 'Klaxon : OK', 'Freins :'], 'bright': True,
                 'stamp': {'text': 'REFUSÉ', 'at': 0.58, 'rot': -0.2, 'y': -0.12}})],
        fx=[{'type': 'shake', 'at': HIT13, 'dur': 0.18, 'amount': 0.02}],
        cams=[FC(0.0, [3.6, 1.5, 3.6], [[RX - 0.4, 3.1, -3.5], [RX - 0.4, 0.0, -3.5], [RX + 1.75, 2.2, 0.85], [RX + 1.45, 1.5, 0.95]], top=0.2, bottom=0.74, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])   # (pass 2) under the title band, the stamp above the caption band
st.cue('whoosh', 'S13', 0.0, 0.15, 0.2, 400, 2500); st.cue('thud', 'S13', HIT13, 0.6); st.cue('sfx:splat', 'S13', HIT13, 0.4); st.cue('sfx:cuff', 'S13', 0.58, 0.4)
st.card('S13', 'REFUSÉ', at=0.58)

# 14: since then he may no longer walk. The pavement: yellow wheel chocks under his shoes; he tries a step: he only rocks on them, forward, back, like
#     a rocking chair; he gives up
D14 = st.dur('S14'); ME14 = [PX, 0, 0.0]
ROCK14 = [(0.32, 0.42, 0.1, 'out'), (0.5, 0.4, 0.15, None), (0.68, -0.24, 0.16, 'inOut'), (0.86, 0.13, 0.14, 'inOut'), (1.02, -0.05, 0.12, 'inOut'), (1.16, 0.0, 0.1, 'inOut')]   # (pass 2) (t, lay forward, dur, ease): tips 24 degrees, hangs, rocks back, forward, settles
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME14, -25, 'stiffStand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.12, toon={'bend': {'legR': [-0.95, 0, 0, 1, None], 'shinR': [1.05, 0, 0, 1, None]}, 'face': {'brow': 0.6}}, toonDur=0.12, toonEase='out'),   # he tries a step: the knee up
            *[k(t, toon={'lay': [a, 0], 'face': {'brow': 0.9 if a > 0.3 else 0.6, 'pop': 0.3 if a > 0.3 else 0.0, 'gy': -0.4}}, toonDur=d, **({'toonEase': e} if e else {})) for t, a, d, e in ROCK14],
            k(1.32, toon={'bend': {'spine': [0.35, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'brow': -0.3, 'puff': 0.5}}, toonDur=0.25, toonEase='inOut'), k(1.32, expr='sad'),   # slumps, a sigh
            k(1.65, toon={'bend': {'spine': [0.38, 0, 0, 1, None], 'neck': [0.28, 0, 0, 1, None]}, 'face': {'lid': 0.6, 'brow': -0.3}}, toonDur=0.2)])],
        props=[*[P(f'chock{i}', 'wheelChock', pos=[round(ME14[0] + dx, 3), 0, round(ME14[2] + dz, 3)], ry=ry, opts={'s': 1.0}) for i, (dx, dz, ry) in enumerate(((-0.25, 0.22, -40), (0.18, 0.28, -40), (-0.2, -0.12, 140), (0.22, -0.06, 140)))],
               P('stamp14', 'paperSheet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.38, 0.18], 'face': 'camera'}, opts={'w': 0.34, 'h': 0.16, 'big': 'INTERDIT', 'bigSize': 0.45, 'lines': ['DE CIRCULER'], 'lineSize': 0.16, 'top': 0.08, 'paper': '#F4F1E8', 'bigInk': '#C8202A', 'bright': True})],   # (pass 2) turned to us
        cams=[FC(0.0, [4.4, 1.2, 2.4], [[ME14[0], 2.35, ME14[2]], [ME14[0] - 0.3, 0.0, ME14[2] + 0.3], [ME14[0] + 0.3, 0.0, ME14[2] - 0.2], [ME14[0] + 0.0, 2.6, ME14[2] + 0.9]], top=0.12, bottom=0.74, drift=(0.05, 0, -0.04))])   # (pass 2) the chocks above the caption band, room for the tip forward
st.cue('sfx:squeak', 'S14', 0.2, 0.25); st.cue('sfx:squeak', 'S14', 0.42, 0.2)

# 15: the bus pushes him every morning. The street, low: the bus comes up behind him and pushes him along: stiff in front of its bumper, his heels
#     sliding with sparks, his coffee in his hand, deadpan; the tie flies
D15 = st.dur('S15'); Z15 = (-6.0, 4.0)
B15 = {'wind': [0.0, 0.2, -1.0], 'lay': [-0.08, 0], 'face': {'lid': 0.4}}   # (pass 2) leaning back against the push, the wind of it in his tie
CHEST15 = {'R': ['torso', -0.06, 0.4, 0.26, 1, 0.05]}; SIP15 = {'R': ['face', 0.08, 0.2, 0.1, 1, 0.05]}   # the cup in front of his chest / at his mouth, in his own frame (he moves with the bus)
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [BUSX, 0, Z15[0] + 4.4], 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, to=[BUSX, 0, Z15[1] + 4.4], dur=D15, clip='stiffStand', then='stiffStand', glide=True, ease='linear', face=0),   # (pass 2) stiff as a board (the brake clip flailed)
            k(0.0, toon={**B15, 'touch': CHEST15, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(0.95, toon={**B15, 'touch': SIP15, 'hands': {'R': 'grip'}}, toonDur=0.2, toonEase='inOut'), k(1.3, toon={**B15, 'touch': CHEST15, 'hands': {'R': 'grip'}}, toonDur=0.2, toonEase='inOut')])],   # one deadpan sip
        props=[BUS(Z15[0], keys=[k(0.0, to=[BUSX, 0, Z15[1]], dur=D15, ease='linear')]), CUP(),
               P('sparks', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0.0, BUSX, Z15[0] + 4.25], [D15, BUSX, Z15[1] + 4.25]], 'from': 0.0, 'to': D15, 'every': 0.04, 'marks': True})],
        cams=[FC(0.0, [0.1, 0.8, Z15[0] + 7.6], [[BUSX, 2.35, Z15[0] + 4.2], [BUSX, 0.0, Z15[0] + 4.2], [BUSX, 3.0, Z15[0] + 1.5], [BUSX - 1.0, 0.0, Z15[0] + 3.0]], top=0.12, bottom=0.74, drift=(0.0, 0.0, Z15[1] - Z15[0]))])   # it travels with them; (pass 2) the heels above the caption band
st.cue('engine', 'S15', 0.0, 0.35, D15); st.cue('sfx:brake', 'S15', 0.0, 0.25)

# 16: he never misses it. The bus stop: the bus stops; he slides on, stops on his heels exactly at the stop, lifts his coffee to us; behind him, the
#     doors open for the others
D16 = st.dur('S16'); STP16 = 0.45; HALT16 = round(STP16 + 0.32, 3)
STOPZ = 8.0; SHX16 = 5.7                                            # (pass 2) the shelter at the kerb: he stops at its front post
POLE16 = [round(SHX16 - 0.75, 3), 0, round(STOPZ - 0.35, 3)]        # where he halts, beside the post
S16FROM = [BUSX, 0, round(STOPZ - 6.2 + 4.4, 3)]
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[
        act('mec', S16FROM, 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, to=POLE16, dur=HALT16, clip='stiffStand', then='stiffStand', glide=True, ease='out', face=0),
            k(0.0, toon={'lay': [-0.22, 0], 'touch': CHEST15, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.0),                                  # sliding on his heels, leaning back
            k(HALT16, toon={'lay': [0.1, 0], 'touch': CHEST15, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.06, toonEase='out'),                 # he halts: tips forward past upright
            k(round(HALT16 + 0.12, 3), toon={'lay': [-0.03, 0], 'touch': CHEST15, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.1),
            k(round(HALT16 + 0.25, 3), toon={'touch': CHEST15, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.1),
            k(round(HALT16 + 0.45, 3), toon={'touch': {'R': ['face', 0.42, 0.34, 0.32, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'browL': 0.6}}, toonDur=0.2, toonEase='outBack'),   # the cup lifted to us
            k(round(HALT16 + 1.3, 3), toon={'touch': {'R': ['face', 0.42, 0.36, 0.32, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.45, 'browL': 0.6}}, toonDur=0.3)]),
        act('voyageuse', [round(SHX16 + 0.1, 3), 0, round(STOPZ + 0.6, 3)], -90, 'stand', 'neutral', keys=[k(0.0, look=[BUSX, 1.6, STOPZ - 2.0]), k(round(STP16 + 0.55, 3), to=[4.55, 0, round(STOPZ - 1.6, 3)], dur=0.9, clip='walk', then='stand', ease='inOut')]),
        act('voyageur', [round(SHX16 + 0.25, 3), 0, round(STOPZ + 1.3, 3)], -90, 'stand', 'neutral', keys=[k(0.0, look=[BUSX, 1.6, STOPZ - 2.0]), k(round(STP16 + 0.75, 3), to=[4.7, 0, round(STOPZ - 0.8, 3)], dur=0.9, clip='walk', then='stand', ease='inOut')])],   # (pass 2) the others step on
        props=[BUS(STOPZ - 6.2, keys=[k(0.0, to=[BUSX, 0, STOPZ - 4.0], dur=STP16, ease='out')], doors=[[STP16 + 0.4, 1]]), P('shelter', 'busStop', pos=[SHX16, 0, round(STOPZ + 0.8, 3)], ry=-90), CUP(),
               P('smoke16', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0.0, S16FROM[0], S16FROM[2] + 0.05], [HALT16, POLE16[0], POLE16[2] + 0.05]], 'from': 0.0, 'to': HALT16, 'every': 0.04, 'marks': True})],
        cams=[FC(0.0, [4.05, 1.05, round(STOPZ + 2.5, 3)], [[POLE16[0], 2.45, POLE16[2]], [POLE16[0], 0.0, POLE16[2]], [round(BUSX + 1.2, 3), 2.2, round(STOPZ - 1.6, 3)], [round(SHX16 - 0.45, 3), 2.4, round(STOPZ - 0.35, 3)]], top=0.12, bottom=0.74, drift=(0.03, 0, -0.05))])   # (pass 2) close and low: he halts at the post, the bus doors and the others behind him
st.cue('sfx:brake', 'S16', 0.0, 0.35); st.cue('sfx:carDoor', 'S16', STP16 + 0.4, 0.3); st.cue('sfx:brake', 'S16', 0.05, 0.25)

st.write("Le radar", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'prefet': {'preset': 'prefet', 'seed': 461, 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'build': {'width': 0.95, 'headWidth': 1.25}},
    'meca': {'preset': 'worker', 'seed': 462, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'voyageuse': {'preset': 'madame', 'seed': 463, 'build': {'width': 0.9, 'headWidth': 1.25}},
    'voyageur': {'preset': 'fringant', 'seed': 464, 'build': {'width': 0.9, 'headWidth': 1.25}},
})
