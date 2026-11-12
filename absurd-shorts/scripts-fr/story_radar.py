#!/usr/bin/env python3
"""Le radar (story 46, cycle 8 of the cartoon staging): this man ran for his bus. A speed camera flashed him: thirty-one kilometres an hour, in a thirty
zone. He contested: he is on foot. The prefecture ruled: above thirty, a pedestrian is a vehicle. He got a number plate. Then a summons to the technical
inspection. The tyres, fine. The horn, fine. The brakes: refused. Since then he may no longer walk. The bus pushes him every morning. He never misses it.
Staging: every gag treats his body as a car: the flash freezes him mid-stride like a speed-camera photo, the plate screwed onto his back (a jolt per
screw), the lift that takes him up by the armpits, the tyre kick (his leg wobbles), the horn squeezed out of his nose, the brake rollers that throw him
through the wall (his outline left in it), the wheel chocks he rocks on, and the bus that pushes him along with his coffee."""
from story_kit import *
import math

st = Story('radar', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 4), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L05', 7),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L08', 4), ('S12', 'L09', 0), ('S13', 'L09', 2), ('S14', 'L10', 0),
         ('S15', 'L11', 0), ('S16', 'L12', 0)])

STREET = {'clear': [-60, 60], 'eiffel': False, 'paveW': 6.5}
def FC(t, frm, pts, top=0.14, bottom=0.82, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), inside=None):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, inside=inside)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
PX = 6.4                                                           # he runs along the right-hand pavement (x 5..11.5), toward +Z
BUSX = 3.1
BUS = lambda z, keys=None, **o: P('bus', 'cityBus', pos=[BUSX, 0, z], ry=-90, opts={'len': 7.6, 'line': '12', 'dest': 'GARE', 'top': 2.65, **o}, **({'keys': keys} if keys else {}))
SHELTER = lambda z=6.0: P('shelter', 'busStop', pos=[7.9, 0, z], ry=-90)
CUP = lambda: P('cup', 'mug', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.02, 0.04]})
PLATE = lambda: P('plateB', 'licensePlate', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.42, -0.2]}, opts={'text': 'PI-031-ON', 'w': 0.48})   # on his back

# 1: the hook. The street: his bus is at the stop down there, its doors closing; he comes running along the pavement, legs a blur, tie flying
D1 = st.dur('S01')
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [PX, 0, -9.0], 0, 'stand', 'determined', keys=[k(0.0, look=[BUSX, 1.6, 10.0]), k(0.0, to=[PX, 0, -1.5], dur=D1, clip='run', then='run', ease='linear', face=0, cadence=3.2),
            k(0.0, toon={'face': {'tongue': 1, 'tongueYaw': 1.2, 'brow': 0.8}}, toonDur=0.0)])],
        props=[SHELTER(8.0), BUS(9.0, keys=[k(0.9, to=[BUSX, 0, 16.0], dur=D1 - 0.9 + 0.6, ease='in')])],
        cams=[FC(0.0, [3.9, 1.2, -6.2], [[PX, 2.3, -6.5], [PX, 0.0, -6.5], [BUSX, 3.0, 9.0], [PX, 0.0, -1.5]], top=0.12, bottom=0.82, drift=(0, 0, 1.2))])
st.cue('sfx:stepRun', 'S01', 0.1, 0.3); st.cue('sfx:stepRun', 'S01', 0.4, 0.3); st.cue('sfx:stepRun', 'S01', 0.7, 0.3); st.cue('sfx:carDoor', 'S01', 0.5, 0.2); st.cue('engine', 'S01', 0.9, 0.2, 1.0)

# 2: a speed camera flashed him. He sprints past the camera on its pole: flash: the picture freezes on him in mid-air, legs split, tongue out (the
#    speed-camera photo, colours drained)
D2 = st.dur('S02'); FL2 = round(st.at('S02', 'L02', 3), 3)
RAD = [5.25, 0, 1.4]
st.shot('S02', 'parisStreet', setOpts=STREET, freeze={'at': FL2 + 0.03}, actors=[
        act('mec', [PX, 0, -2.4], 0, 'stand', 'determined', keys=[k(0.0, look=[BUSX, 1.6, 12.0]), k(0.0, to=[PX, 0.0, 4.2], dur=round(D2 + 0.4, 3), clip='dashOff', then='dashOff', ease='linear', face=0),
            k(0.0, toon={'face': {'tongue': 1, 'tongueYaw': 1.3, 'brow': 0.9}}, toonDur=0.0), k(FL2 - 0.04, toon={'face': {'tongue': 1, 'tongueYaw': 1.3, 'brow': 1, 'pop': 0.5}}, toonDur=0.04)])],
        props=[P('radar', 'speedCamera', pos=RAD, ry=180, opts={'flashAt': FL2})],
        fx=[{'type': 'flash', 'at': FL2, 'dur': 0.18}],
        cams=[FC(0.0, [2.6, 1.0, 1.4], [[RAD[0], 2.9, RAD[2]], [RAD[0], 0.0, RAD[2]], [PX, 2.3, 0.6], [PX, 0.0, 1.6]], top=0.1, bottom=0.82)])
st.cue('sfx:stepRun', 'S02', 0.05, 0.3); st.cue('sfx:stepRun', 'S02', 0.25, 0.3); st.cue('sfx:cash', 'S02', FL2, 0.0); st.cue('pop', 'S02', FL2, 0.5); st.cue('whoosh', 'S02', FL2 - 0.05, 0.1, 0.12, 2000, 6000)

# 3: thirty-one kilometres an hour. The speed display on its pole: 31 in big red digits, a smile... that turns down and blinks
D3 = st.dur('S03'); SAD3 = 0.55
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('display', 'speedDisplay', pos=[5.3, 0, 3.0], ry=180, opts={'speed': '31', 'showAt': 0.0, 'sadAt': SAD3}), P('radar', 'speedCamera', pos=RAD, ry=180)],
        cams=[cam(0.0, [5.0, 2.3, 1.55], [5.0, 2.32, 1.75], [5.3, 2.38, 3.0], [5.3, 2.38, 3.0], lens=34)])
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
        cams=[FC(0.0, [3.4, 1.6, 4.4], [[ME4[0], 2.35, ME4[2]], [ME4[0], 0.1, ME4[2]], [SIGN4[0], 3.3, SIGN4[2]]], top=0.1, bottom=0.8, drift=(0.06, 0, -0.06))])

# ---- the prefecture: the town-hall set repainted, PRÉFECTURE over the counter; the official in his sash behind the desk
PREF = {'wall': '#E8EEF2', 'band': '#2F5E9E', 'trim': '#1E3E7B', 'floor': '#B7B3AA', 'joint': '#9F9B92', 'banner': True, 'map': False, 'deskZ': -1.25, 'plate': 'PRÉFECTURE',
        'front': 3.6, 'frontSign': {'text': 'PRÉFECTURE', 'x': 0.0, 'y': 2.5, 'w': 1.9}}
OFFI = [0.0, 0, -1.85]; MEP = [0.15, 0, -0.2]
GAUGE = [-1.25, 1.6, -2.55]
OFFICIAL = lambda keys=(): act('prefet', OFFI, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[MEP[0], 1.9, MEP[2]]), *keys])

# 5: he contested: he is on foot. At the counter he slaps down his letter, then lifts a foot and shows the official the sole of his shoe
D5 = st.dur('S05'); SL5, SH5 = 0.15, round(st.at('S05', 'L04', 4) - 0.08, 3)
st.shot('S05', 'mairie', setOpts=PREF, actors=[
        act('mec', MEP, 180, 'stand', 'determined', keys=[k(0.0, look=[OFFI[0], 2.0, OFFI[2]]),
            k(SL5 - 0.1, toon={'reach': {'R': [0.05, 1.25, -0.82, 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.1, toonEase='in'), k(SL5 + 0.2, toon={}, toonDur=0.15),
            k(SH5, toon={'bend': {'legR': [-1.25, 0, 0, 1, None], 'shinR': [0.3, 0, 0, 1, None]}, 'reach': {'R': [0.22, 0.95, -0.55, 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.7}}, toonDur=0.14, toonEase='outBack')])],
        props=[P('letter', 'paperSheet', pos=[0.05, 0.79, -0.85], rot=[-math.pi / 2, 0, 0.12], opts={'w': 0.3, 'h': 0.4, 'head': 'CONTESTATION', 'lines': ['Je suis à pied.'], 'bright': True}, keys=[k(0.0, scale=0.01, dur=0.0), k(SL5, scale=1.0, dur=0.05)])],
        cams=[FC(0.0, [1.9, 1.7, 1.2], [[MEP[0], 2.35, MEP[2]], [MEP[0], 0.0, MEP[2]], [OFFI[0], 2.3, OFFI[2]], [0.05, 0.8, -0.85]], top=0.12, bottom=0.8)])
st.cue('thud', 'S05', SL5, 0.35); st.cue('sfx:paper', 'S05', SL5, 0.3)

# 6: the prefecture ruled: above thirty... The official turns to the big gauge on the wall and cranks the needle: 10, 20, 30... past 30 the green lamp
#    PIÉTON goes out and the red VÉHICULE lights
D6 = st.dur('S06'); OV6 = round(st.at('S06', 'L05', 6) - 0.05, 3)
st.shot('S06', 'mairie', setOpts=PREF, actors=[
        OFFICIAL(keys=[k(0.05, look=GAUGE), k(0.15, toon={'reach': {'R': [round(GAUGE[0] + 0.62, 3), 1.25, round(GAUGE[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.15),
            *[k(round(0.35 + 0.22 * i, 3), toon={'reach': {'R': [round(GAUGE[0] + 0.62 + 0.08 * math.cos(i * 1.7), 3), round(1.25 + 0.08 * math.sin(i * 1.7), 3), round(GAUGE[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.1) for i in range(int((OV6 - 0.35) / 0.22) + 1)],
            k(OV6 + 0.1, look=[MEP[0], 1.9, MEP[2]]), k(OV6 + 0.15, toon={'reach': {'R': [round(GAUGE[0] + 0.4, 3), 2.0, round(GAUGE[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.6}}, toonDur=0.12)])],
        props=[P('gauge', 'speedGauge', pos=GAUGE, opts={'needle': [[0.35, 12.0], [round(0.35 + (OV6 - 0.35) * 0.5, 3), 24.0], [OV6, 31.0]]})],
        cams=[FC(0.0, [-0.2, 1.7, -0.1], [[GAUGE[0] - 0.55, 2.4, GAUGE[2]], [GAUGE[0] + 0.55, 0.9, GAUGE[2]], [OFFI[0], 2.3, OFFI[2]], [OFFI[0], 0.6, OFFI[2]]], top=0.12, bottom=0.78)])
st.cue('sfx:ticks', 'S06', 0.35, 0.25); st.cue('sfx:bell', 'S06', OV6, 0.4)

# 7: a pedestrian is a vehicle. Close on him under the red light: he looks at his hands, then holds an invisible steering wheel and turns it, puzzled
D7 = st.dur('S07')
WHEEL7 = lambda a: {'reach': {'L': [round(MEP[0] + 0.22 * math.cos(a), 3), round(1.45 + 0.18 * math.sin(a), 3), round(MEP[2] - 0.4, 3), 1, 0.06], 'R': [round(MEP[0] - 0.22 * math.cos(a), 3), round(1.45 - 0.18 * math.sin(a), 3), round(MEP[2] - 0.4, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}}
st.shot('S07', 'mairie', setOpts=PREF, actors=[
        act('mec', MEP, 180, 'stand', 'worried', keys=[k(0.0, look=[MEP[0], 1.3, MEP[2] - 0.5]), k(0.0, toon={**WHEEL7(0.0), 'face': {'brow': 0.6}}, toonDur=0.0),
            *[k(round(0.2 + 0.2 * i, 3), toon={**WHEEL7(0.5 * (1 if i % 2 == 0 else -1)), 'face': {'brow': 0.7, 'gy': 0.6}}, toonDur=0.18, toonEase='inOut') for i in range(7)],
            k(0.7, look='camera')])],
        props=[],
        cams=[FC(0.0, [0.75, 1.75, -1.5], [[MEP[0], 2.35, MEP[2]], [MEP[0], 1.15, MEP[2]], [MEP[0] - 0.4, 1.4, MEP[2] - 0.4], [MEP[0] + 0.4, 1.4, MEP[2] - 0.4]], top=0.14, bottom=0.66)])

# 8: he got a number plate. Seen from behind: the official screws a plate onto his back with an electric screwdriver: four screws, a jolt at each
D8 = st.dur('S08'); SCR8 = (0.25, 0.5, 0.75, 1.0)
BACK8 = [MEP[0], 1.75, round(MEP[2] - 0.22, 3)]
st.shot('S08', 'mairie', setOpts=PREF, actors=[
        act('mec', MEP, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[MEP[0], 1.6, MEP[2] + 3.0]), *[k(t, toon={'sq': [0.95, 1.07, 0.95], 'face': {'brow': 0.9, 'eye': 0.4}}, toonDur=0.03) for t in SCR8],
            *[k(round(t + 0.08, 3), toon={'face': {'lid': 0.3}}, toonDur=0.06) for t in SCR8]]),
        act('prefet', [round(MEP[0] + 0.15, 3), 0, round(MEP[2] - 0.75, 3)], 0, 'stand', 'determined', keys=[k(0.0, look=BACK8),
            *[k(t, toon={'reach': {'R': [round(BACK8[0] + (0.15 if i % 2 else -0.15), 3), round(BACK8[1] + (0.06 if i < 2 else -0.06), 3), round(BACK8[2] - 0.08, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.08) for i, t in enumerate(SCR8)]])],
        props=[PLATE(), P('drill', 'marker', on={'actor': 'prefet', 'hand': 'R', 'offset': [0, -0.02, 0.06]}, opts={'color': '#F2C230'})],
        cams=[FC(0.0, [1.3, 1.85, -2.9], [[MEP[0], 2.35, MEP[2]], [MEP[0], 0.9, MEP[2]], BACK8], top=0.14, bottom=0.7)])
[st.cue('sfx:zip', 'S08', t, 0.35) for t in SCR8]

# ---- the garage of the technical inspection (whiteVoid + garageBay): the lift at the middle, the brake rollers at the right, the back wall ahead
GZ = 0.0
LIFT = lambda keys=None, **o: P('lift', 'carLift', pos=[-1.2, 0, GZ], opts={'gap': 2.0, 'armIn': 0.55, **o})
ROLL = lambda **o: P('rollers', 'brakeRollers', pos=[1.9, 0, 0.6], opts=o)
GAR = lambda back=True: [P('garage', 'garageBay', opts={'w': 8, 'd': 7, 'back': back}), LIFT(), ROLL()]
MECA = lambda pos, ry, keys=(): act('meca', pos, ry, 'stand', 'neutral', keys=list(keys))

# 9: then a summons to the technical inspection. The garage (CONTRÔLE TECHNIQUE): he stands between the posts of the lift, the arms under his armpits;
#    the lift takes him up, stiff as a post, his feet dangling; the mechanic with his clipboard
D9 = st.dur('S09'); UP9 = 0.35
st.shot('S09', 'whiteVoid', actors=[
        act('mec', [-1.2, 0, GZ], 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look=[0.0, 1.6, 5.0]), k(UP9, to=[-1.2, 1.1, GZ], dur=round(D9 - UP9 - 0.2, 3), clip='stiffStand', then='stiffStand', glide=True, ease='inOut'),
            k(UP9 + 0.1, toon={'face': {'gy': 0.8, 'brow': 0.6}}, toonDur=0.1)]),
        MECA([0.9, 0, 1.6], -120, keys=[k(0.0, look=[-1.2, 2.2, GZ])])],
        props=[P('garage', 'garageBay', opts={'w': 8, 'd': 7}), LIFT(lift=[[UP9, 1.25]], h0=1.37), ROLL(), P('clip', 'clipboardProp', on={'actor': 'meca', 'hand': 'L', 'offset': [0, 0, 0.05]})],
        cams=[FC(0.0, [1.6, 1.7, 5.4], [[-2.4, 3.6, GZ], [0.2, 0.0, GZ], [0.0, 3.6, -3.5], [0.9, 0.0, 1.6]], top=0.1, bottom=0.82, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])
st.cue('engine', 'S09', UP9, 0.2, 1.4); st.cue('sfx:squeak', 'S09', UP9, 0.2)

# 10: the tyres, fine. Low, at his dangling shoes: the mechanic kicks one: the leg wobbles like rubber; a thumbs-up
D10 = st.dur('S10'); KK10 = (0.18, 0.62)
FOOT10 = [-1.08, 1.12, GZ + 0.12]
WAG10 = lambda t0: [k(round(t0 + d, 3), toon={'bend': {'legR': [a, 0, 0, 1, None], 'shinR': [-a * 0.8, 0, 0, 1, None]}}, toonDur=0.05) for d, a in ((0.0, 0.0), (0.04, 0.55), (0.1, -0.4), (0.16, 0.28), (0.22, -0.15), (0.3, 0.0))]
st.shot('S10', 'whiteVoid', actors=[
        act('mec', [-1.2, 1.1, GZ], 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look=[0.0, 1.6, 5.0]), *WAG10(KK10[0]), *WAG10(KK10[1])]),
        MECA([-0.4, 0, 0.75], -145, keys=[k(0.0, look=FOOT10), *[k(round(t - 0.08, 3), toon={'bend': {'legR': [-0.9, 0, 0, 1, None]}}, toonDur=0.08, toonEase='in') for t in KK10],
            *[k(round(t + 0.06, 3), toon={}, toonDur=0.1) for t in KK10], k(0.95, toon={'reach': {'R': [-0.3, 1.75, 0.55, 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.1)])],
        props=[P('garage', 'garageBay', opts={'w': 8, 'd': 7}), LIFT(h0=1.25), ROLL(), P('thumb', 'thumbsUp', pos=[-0.3, 1.82, 0.62], rot=[1.5708, 3.1416, 0], scale=1.6, keys=[k(0.0, visible=False), k(0.95, visible=True)])],
        cams=[FC(0.0, [0.5, 0.55, 2.4], [[-1.2, 2.5, GZ], [-1.2, 0.9, GZ], [-0.4, 2.2, 0.75], [-0.4, 0.0, 0.75]], top=0.1, bottom=0.82, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])
[st.cue('sfx:bonk', 'S10', t, 0.35) for t in KK10]; [st.cue('sfx:twang', 'S10', t + 0.02, 0.25) for t in KK10]

# 11: the horn, fine. The mechanic squeezes his nose: HONK: his head squashes, his eyes pop, his cheeks blow out; again; a tick on the clipboard
D11 = st.dur('S11'); HN11 = (0.2, 0.68)
NOSE11 = [-1.2, 3.05, round(GZ + 0.2, 3)]
st.shot('S11', 'whiteVoid', actors=[
        act('mec', [-1.2, 1.1, GZ], 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look=[0.0, 3.0, 5.0]),
            *[x for t in HN11 for x in (k(t, toon={'scl': {'head': [1.3, 0.78, 1.15]}, 'face': {'pop': 0.6, 'brow': 1, 'puff': 1, 'cheeks': 1}}, toonDur=0.03, toonEase='out'), k(round(t + 0.16, 3), toon={'face': {'lid': 0.35}}, toonDur=0.1))]]),
        MECA([-0.75, 1.15, 0.85], -150, keys=[k(0.0, look=NOSE11), *[k(round(t - 0.1, 3), toon={'reach': {'R': [*NOSE11, 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.1) for t in HN11],
            *[k(round(t + 0.12, 3), toon={'reach': {'R': [round(NOSE11[0] + 0.25, 3), 2.9, round(NOSE11[2] + 0.35, 3), 1, 0.06]}, 'hands': {'R': 'spread'}}, toonDur=0.1) for t in HN11]])],
        props=[P('garage', 'garageBay', opts={'w': 8, 'd': 7}), LIFT(h0=1.25), P('step', 'cardboardBox', pos=[-0.75, 0, 0.85], opts={'w': 0.8, 'h': 1.15, 'd': 0.7}),
               *[P(f'ring{i}', 'impactStars', pos=[NOSE11[0], NOSE11[1], NOSE11[2] + 0.1], opts={'at': t, 'n': 6, 'r': 0.32, 'r0': 0.12, 'dur': 0.28, 'size': 0.06}) for i, t in enumerate(HN11)]],
        cams=[FC(0.0, [0.4, 3.0, 2.6], [[-1.2, 3.55, GZ], [-1.2, 2.35, GZ], [-0.75, 3.3, 0.85]], top=0.14, bottom=0.7, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])
[st.cue('sfx:honk', 'S11', t, 0.5) for t in HN11]

# 12: the brakes... On the brake rollers he runs like mad on the spot, legs a blur; the mechanic pulls the lever: the rollers stop dead
D12 = st.dur('S12'); STOP12 = round(D12 - 0.12, 3)
RX = 1.9
st.shot('S12', 'whiteVoid', actors=[
        act('mec', [RX, 0.06, 0.6], 180, 'stand', 'determined', keys=[k(0.0, look=[RX, 1.6, -3.0]), k(0.0, clip='scramble', params={'dur': 3.0, 'freq': 11, 'expr': 'determined'})]),
        MECA([RX + 1.2, 0, 0.0], -90, keys=[k(0.0, look=[RX, 1.4, 0.6]), k(STOP12 - 0.1, toon={'reach': {'R': [RX + 0.7, 1.0, -0.15, 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.1, toonEase='in')])],
        props=[P('garage', 'garageBay', opts={'w': 8, 'd': 7}), LIFT(h0=0.15), ROLL(spin=[[0.0, 6.0], [STOP12, 0.0]], lampAt=STOP12)],
        cams=[FC(0.0, [-0.4, 1.4, 3.6], [[RX, 2.4, 0.6], [RX, 0.0, 0.6], [RX + 1.2, 2.2, 0.0], [RX - 0.8, 0.0, 0.2]], top=0.12, bottom=0.82, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])
st.cue('sfx:engine', 'S12', 0.0, 0.0); st.cue('engine', 'S12', 0.0, 0.25, D12); [st.cue('sfx:squeak', 'S12', round(0.1 + 0.15 * i, 3), 0.15) for i in range(4)]; st.cue('clang', 'S12', STOP12, 0.4)

# 13: refused. He shoots off the rollers, stiff, flat out, through the back wall: a hole in his shape; bricks; the mechanic stamps REFUSÉ on his sheet
D13 = st.dur('S13'); HIT13 = 0.12
st.shot('S13', 'whiteVoid', actors=[
        act('mec', [RX, 0.06, 0.6], 180, 'stand', 'surprised', keys=[k(0.0, look=None), k(0.0, toon={'sq': [0.86, 1.05, 1.5], 'face': {'pop': 0.6, 'brow': 1}}, toonDur=0.0),
            k(0.0, to=[RX - 0.4, 0.6, -4.5], dur=HIT13 + 0.12, clip='dashOff', then='dashOff', glide=True, ease='linear', face=180), k(HIT13 + 0.1, visible=False)]),
        MECA([RX + 1.2, 0, 0.0], -90, keys=[k(0.0, look=[RX - 0.4, 1.3, -3.6]), k(0.45, look=[RX + 1.0, 1.0, 0.25]),
            k(0.5, toon={'reach': {'R': [RX + 0.95, 1.25, 0.28, 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.08, toonEase='in')])],
        props=[P('garage', 'garageBay', opts={'w': 8, 'd': 7, 'back': False}), P('wall13', 'burstWall', pos=[0.0, 0, -3.5], opts={'w': 8.0, 'h': 4.2, 'burstAt': HIT13, 'holeX': RX - 0.4, 'holeY': 1.25, 'holeScale': 1.05, 'color': '#E3E1DA'}),
               LIFT(h0=0.15), ROLL(lampAt=0.0), P('sheet13', 'paperSheet', on={'actor': 'meca', 'hand': 'L', 'offset': [0, 0.02, 0.06], 'face': 'camera'}, opts={'w': 0.3, 'h': 0.4, 'head': 'CONTRÔLE', 'lines': ['Pneus : OK', 'Klaxon : OK', 'Freins :'], 'bright': True,
                 'stamp': {'text': 'REFUSÉ', 'at': 0.58, 'rot': -0.2, 'y': -0.12}})],
        fx=[{'type': 'shake', 'at': HIT13, 'dur': 0.18, 'amount': 0.02}],
        cams=[FC(0.0, [3.4, 1.6, 3.4], [[RX - 0.4, 3.0, -3.5], [RX - 0.4, 0.0, -3.5], [RX + 1.2, 2.2, 0.0], [RX + 0.9, 1.0, 0.28]], top=0.1, bottom=0.8, inside=(-3.9, 3.9, 0.2, 4.1, -3.4, 9.0))])
st.cue('whoosh', 'S13', 0.0, 0.15, 0.2, 400, 2500); st.cue('thud', 'S13', HIT13, 0.6); st.cue('sfx:splat', 'S13', HIT13, 0.4); st.cue('sfx:cuff', 'S13', 0.58, 0.4)
st.card('S13', 'REFUSÉ', at=0.58)

# 14: since then he may no longer walk. The pavement: yellow wheel chocks under his shoes; he tries a step: he only rocks on them, forward, back, like
#     a rocking chair; he gives up
D14 = st.dur('S14'); ME14 = [PX, 0, 0.0]
ROCK14 = [(0.2, 0.18), (0.42, -0.14), (0.62, 0.1), (0.8, -0.06), (0.98, 0.0)]
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME14, 50, 'stiffStand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.15, clip='statueRock', params={'hits': [0.05, 0.27, 0.47], 'amp': 0.16, 'freq': 9, 'damp': 3.2, 'dir': 1, 'axis': 'x'}),   # a step tried: he rocks on the chocks
            *[k(round(0.15 + t, 3), toon={'face': {'brow': 0.6, 'gy': 0.5}}, toonDur=0.06) for t in (0.05, 0.27, 0.47)],
            k(1.1, toon={'face': {'lid': 0.5, 'brow': 0.3}}, toonDur=0.15), k(1.1, expr='sad')])],
        props=[*[P(f'chock{i}', 'wheelChock', pos=[round(ME14[0] + dx, 3), 0, round(ME14[2] + dz, 3)], ry=ry, opts={'s': 1.0}) for i, (dx, dz, ry) in enumerate(((-0.25, 0.22, -40), (0.18, 0.28, -40), (-0.2, -0.12, 140), (0.22, -0.06, 140)))],
               P('stamp14', 'paperSheet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.38, 0.18]}, opts={'w': 0.3, 'h': 0.14, 'big': 'INTERDIT', 'bigSize': 0.45, 'lines': ['DE CIRCULER'], 'lineSize': 0.16, 'top': 0.08, 'paper': '#F4F1E8', 'bigInk': '#C8202A', 'bright': True})],
        cams=[FC(0.0, [4.4, 1.3, 2.4], [[ME14[0], 2.35, ME14[2]], [ME14[0] - 0.3, 0.0, ME14[2] + 0.3], [ME14[0] + 0.3, 0.0, ME14[2] - 0.2]], top=0.14, bottom=0.82, drift=(0.05, 0, -0.04))])
st.cue('sfx:squeak', 'S14', 0.2, 0.25); st.cue('sfx:squeak', 'S14', 0.42, 0.2)

# 15: the bus pushes him every morning. The street, low: the bus comes up behind him and pushes him along: stiff in front of its bumper, his heels
#     sliding with sparks, his coffee in his hand, deadpan; the tie flies
D15 = st.dur('S15'); Z15 = (-6.0, 4.0)
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [BUSX, 0, Z15[0] + 4.2], 0, 'stiffStand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, to=[BUSX, 0, Z15[1] + 4.2], dur=D15, clip='heelBrake', then='heelBrake', glide=True, ease='linear', face=0),
            k(0.0, toon={'wind': [0.0, 0.2, -1.0], 'face': {'lid': 0.4}}, toonDur=0.0)])],
        props=[BUS(Z15[0], keys=[k(0.0, to=[BUSX, 0, Z15[1]], dur=D15, ease='linear')]), CUP(),
               P('sparks', 'heelSmoke', pos=[0, 0, 0], opts={'path': [[0.0, BUSX, Z15[0] + 4.25], [D15, BUSX, Z15[1] + 4.25]], 'from': 0.0, 'to': D15, 'every': 0.04, 'marks': True})],
        cams=[FC(0.0, [0.1, 0.8, Z15[0] + 7.6], [[BUSX, 2.35, Z15[0] + 4.2], [BUSX, 0.0, Z15[0] + 4.2], [BUSX, 3.0, Z15[0] + 1.5], [BUSX - 1.0, 0.0, Z15[0] + 3.0]], top=0.12, bottom=0.8, drift=(0.0, 0.0, Z15[1] - Z15[0]))])   # it travels with them
st.cue('engine', 'S15', 0.0, 0.35, D15); st.cue('sfx:brake', 'S15', 0.0, 0.25)

# 16: he never misses it. The bus stop: the bus stops; he slides on, stops on his heels exactly at the stop, lifts his coffee to us; behind him, the
#     doors open for the others
D16 = st.dur('S16'); STP16 = 0.45
STOPZ = 8.0
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [BUSX, 0, STOPZ - 2.0], 0, 'heelBrake', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, to=[BUSX, 0, STOPZ + 0.6], dur=STP16 + 0.25, clip='heelBrake', then='stand', glide=True, ease='out', face=0),
            k(STP16 + 0.3, toon={'reach': {'R': [round(BUSX + 0.25, 3), 1.75, round(STOPZ + 0.95, 3), 1, 0.06]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'browL': 0.5}}, toonDur=0.2), k(STP16 + 0.3, look='camera')])],
        props=[BUS(STOPZ - 6.2, keys=[k(0.0, to=[BUSX, 0, STOPZ - 4.0], dur=STP16, ease='out')], doors=[[STP16 + 0.4, 1]]), SHELTER(STOPZ + 0.8), CUP()],
        cams=[FC(0.0, [-0.6, 1.4, STOPZ + 4.6], [[BUSX, 2.4, STOPZ + 0.6], [BUSX, 0.0, STOPZ + 0.6], [BUSX, 3.0, STOPZ - 4.0], [7.9, 2.6, STOPZ + 0.8]], top=0.12, bottom=0.8, drift=(0.05, 0, -0.08))])
st.cue('sfx:brake', 'S16', 0.0, 0.35); st.cue('sfx:carDoor', 'S16', STP16 + 0.4, 0.3)

st.write("Le radar", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'prefet': {'preset': 'prefet', 'seed': 461, 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'build': {'width': 0.95, 'headWidth': 1.25}},
    'meca': {'preset': 'worker', 'seed': 462, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
})
