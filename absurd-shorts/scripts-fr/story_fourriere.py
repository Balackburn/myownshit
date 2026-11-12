#!/usr/bin/env python3
"""La fourrière (story 45, cycle 7 of the cartoon staging): this man double-parked "for one minute". The pound came: it took him, not the car. At the
pound they clamped him. To leave, the owner must pay. The owner is the car. It has no hands. It honked for three weeks. The neighbours complained:
against him. Yesterday the pound came back for the car. It parked it in its space. On him. He pays for the space.
Staging: the car is a character (headlight eyes, hazard lights, a honk that squashes it, wipers that flail like little arms); every gag is the logic of
the pound applied to a man: the hook that takes him by the collar (he stretches, his feet stay, then he dangles like a noodle), the clamp on his shoe
(he walks round it like a compass), the registration with the car's photo (double take), the man-balloon held down by his clamp, the car parked on him
(his flattened head sticks out, tongue out), and the arm that stretches to the pay machine.
Pass 2 (review 1: animation 6.8, art 6.5): the punchline seen from above the bonnet (his flat face right side up), then close on the ticket held up
beside it (FRAIS DE GARDE, big), then the car's face for the last tiny honk; the car tips onto two wheels and its wipers stretch to the keypad and stop
short; the hook's stretch lasts; the takes centred and the pound man on the open side; the balloon round; a four-strap sling; the pound and its sign
established; the clamp above the caption band."""
from story_kit import *
import math

st = Story('fourriere', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 7), ('S03', 'L02', 0), ('S04', 'L02', 4), ('S05', 'L02', 7), ('S06', 'L02', 8),
         ('S07', 'L03', 0), ('S08', 'L03', 3), ('S09', 'L04', 0), ('S10', 'L04', 2), ('S11', 'L05', 0), ('S12', 'L05', 2),
         ('S13', 'L06', 0), ('S14', 'L07', 0), ('S15', 'L07', 4), ('S16', 'L08', 0), ('S17', 'L08', 5), ('S18', 'L09', 0),
         ('S19', 'L09', 4), ('S20', 'L10', 0), ('S21', 'L11', 0), ('S22', 'L12', 0)])

STREET = {'clear': [-110, 110], 'eiffel': False, 'paveW': 6.5}
MINT = '#6CC4A4'
CAR0 = [1.9, 0, 0.0]; CRY = 90                                     # his car, double-parked beside the blue one, nose to -Z (its right side faces the pavement)
def CAR(pos=None, keys=None, pid='car', **o):                      # the car: hazards on from its arrival
    return P(pid, 'carToon', pos=pos or CAR0, ry=CRY, rotOrder='YXZ', opts={'color': MINT, 'eyes': True, 'hazard': [0.0, 99], **o}, **({'keys': keys} if keys else {}))
PARKED = lambda: [P('pk1', 'car', pos=[4.0, 0, 0.2], ry=90, opts={'color': '#3A6EA5'}), P('pk2', 'car', pos=[4.0, 0, -8.6], ry=90, opts={'color': '#C9473A'}),
                  P('pk3', 'car', pos=[4.0, 0, 6.0], ry=90, opts={'color': '#E8A33A'})]
METER = lambda **o: P('meter', 'parkingMeter', pos=[5.35, 0, -3.4], ry=-115, opts=o)   # (pass 2) clear of the blue car's nose, turned toward the street
FX = 8.6                                                           # the front of the flats (the street's house fronts stand at about x = 10.2: rooms behind 10.1 were inside them)
FLATS = lambda lit=None: P('flats', 'flatsWall', pos=[FX, 0, 0.0], ry=-90, opts={'w': 5.4, 'h': 9.4, 'cols': 3, 'rows': 2, 'depth': 1.25, 'y0': 3.0, 'lit': lit or []})
TIP = [-5.5, 6.2]; TIPY = round(TIP[1] - 0.15, 3)                  # the tow truck's long boom: its tip 2.4 m behind the bed, high enough to lift a car
TRUCK = lambda z, keys=None, **o: P('truck', 'towTruck', pos=[1.9, 0, z], ry=90, opts={'tip': TIP, **o}, **({'keys': keys} if keys else {}))
HOOKZ = lambda zt: round(zt - TIP[0], 3)                           # the world z under the tip of a truck at zt (its local -X points to +Z)
def FC(t, frm, pts, top=0.14, bottom=0.82, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):   # (pass 2) kw: margin=...
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
BAG = lambda: P('baguette', 'baguette', on={'actor': 'mec', 'hand': 'L', 'offset': [0, 0, 0.04]})

# ---- the pound: a fenced stretch of street; bays along the road; the cash booth on the right pavement; his bay is n° 12
ZP = 70.0
F12 = [4.28, 0, round(ZP + 0.1, 3)]                                # his clamped left foot (from S08 on)
def ROOT(th, foot=F12):                                             # where his root is when he faces th (deg) with his left foot on `foot`
    a = math.radians(th); return r3([foot[0] - 0.12 * math.cos(a) - 0.05 * math.sin(a), 0.0, foot[2] + 0.12 * math.sin(a) - 0.05 * math.cos(a)])
HB = ROOT(-30)                                                      # facing the camera side (-X, +Z)
POUND = lambda: [P('bay11', 'parkingBay', pos=[3.6, 0, ZP + 5.2], ry=90, opts={'num': '11'}), P('bay12', 'parkingBay', pos=[3.6, 0, ZP], ry=90, opts={'num': '12'}),
                 P('bay13', 'parkingBay', pos=[3.6, 0, ZP - 5.2], ry=90, opts={'num': '13'}),
                 P('bayL1', 'parkingBay', pos=[-1.4, 0, ZP + 5.2], ry=-90, opts={'num': '21'}), P('bayL2', 'parkingBay', pos=[-1.4, 0, ZP], ry=-90, opts={'num': '22'}),
                 P('bayL3', 'parkingBay', pos=[-1.4, 0, ZP - 5.2], ry=-90, opts={'num': '23'}),
                 P('pc1', 'car', pos=[3.6, 0, ZP + 5.2], ry=90, opts={'color': '#E6E3DA'}),   # (bay 13 stays empty: a car there stood in front of the low cameras of the end, one camera inside it)
                 P('pc3', 'car', pos=[-1.4, 0, ZP + 5.2], ry=-90, opts={'color': '#8A8F98'}), P('pc4', 'car', pos=[-1.4, 0, ZP], ry=-90, opts={'color': '#D9783A'}),
                 P('pc5', 'car', pos=[-1.4, 0, ZP - 5.2], ry=-90, opts={'color': '#3A6EA5'}),
                 P('fenceN', 'fence', pos=[0.0, 0, ZP - 9.0], opts={'length': 10.0, 'height': 2.0, 'color': '#2E5E4A', 'rail': '#2E5E4A'}),
                 P('fenceS', 'fence', pos=[0.0, 0, ZP + 13.0], opts={'length': 10.0, 'height': 2.0, 'color': '#2E5E4A', 'rail': '#2E5E4A'}),
                 P('psign', 'poundSign', pos=[0.0, 0, ZP - 9.3], opts={'text': 'FOURRIÈRE', 'sub': 'PRÉFECTURE', 'w': 3.6, 'h': 1.2, 'y': 2.1}),
                 P('booth', 'cashBooth', pos=[6.15, 0, ZP], ry=-90, opts={'notice': True})]
NOTICE = lambda: P('notice', 'paperSheet', pos=[5.27, 1.66, round(ZP - 0.36, 3)], ry=-90, opts={'w': 0.42, 'h': 0.52, 'head': 'FOURRIÈRE', 'big': 'PROPRIÉTAIRE', 'bigSize': 0.19,
                   'lines': ['DU VÉHICULE', 'UNIQUEMENT'], 'lineSize': 0.14, 'paper': '#FFFFFF', 'ink': '#14161A', 'bigInk': '#B0101A', 'bright': True})   # (pass 2) bigger, darker ink
CLAMP = lambda **o: P('clamp', 'wheelClamp', on={'actor': 'mec', 'joint': 'footL', 'offset': [0.0, -0.05, 0.06]}, opts={'s': 1.35, **o})
CLERK = lambda keys=(): act('caissiere', [5.78, 0, ZP], -90, 'stand', 'unimpressed', keys=[k(0.0, look=[4.3, 1.9, ZP + 0.2]), *keys])
PMETER = lambda **o: P('pmeter', 'parkingMeter', pos=[5.4, 0, round(ZP - 2.0, 3)], ry=-90, opts={'sticker': 'FRAIS DE GARDE', **o})

# 1: this man double-parked. Low on the road: his little mint car comes up the street and stops beside the parked blue one, rocks on its springs, and
#    its hazard lights start; its headlight eyes look round
D1 = st.dur('S01'); ST1 = 0.8
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[],
        props=[*PARKED(), METER(), CAR(pos=[1.9, 0, 12.0], keys=[k(0.0, to=CAR0, dur=ST1, ease='out')], hazard=[ST1 + 0.12, 99], bounce=[[ST1, 0.07]],
                                   gaze=[[0.0, 0.0, 0.0], [ST1 + 0.35, 0.7, 0.1], [ST1 + 0.75, -0.3, 0.0]], blink=[ST1 + 0.55])],
        cams=[FC(0.0, [-0.9, 0.62, -5.3], [[1.05, 0.0, -1.85], [2.75, 1.65, -1.85], [3.2, 1.75, 1.6], [1.05, 0.0, 1.8]], top=0.34, bottom=0.8, drift=(0.12, 0, 0.15))])
st.cue('engine', 'S01', 0.0, 0.25, 0.9); st.cue('sfx:brake', 'S01', ST1 - 0.3, 0.3); [st.cue('sfx:tick', 'S01', round(ST1 + 0.12 + 0.294 * i, 3), 0.2) for i in range(4)]

# 2: one minute. Beside the car he turns to us, holds up one finger, a wink; then he trots off round the nose of the car
D2 = st.dur('S02'); ME2 = [0.55, 0, 0.35]; RY2 = -128
F2 = (math.sin(math.radians(RY2)), math.cos(math.radians(RY2))); RT2 = (-F2[1], F2[0])
FING2 = r3([ME2[0] + 0.34 * F2[0] + 0.22 * RT2[0], 2.02, ME2[2] + 0.34 * F2[1] + 0.22 * RT2[1]])   # (pass 2) the index beside his face (at arm's length above it, it hailed a taxi)
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME2, RY2, 'stand', 'wink', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': [*FING2, 1, 0.06]}, 'hands': {'R': 'point'}, 'scl': {'handR': [1.45, 1.45, 1.45]}, 'face': {'lidR': 1, 'brow': 0.4}}, toonDur=0.1, toonEase='outBack'),
            k(0.3, toon={'reach': {'R': [*FING2, 1, 0.06]}, 'hands': {'R': 'point'}, 'scl': {'handR': [1.45, 1.45, 1.45]}, 'face': {'brow': 0.4}}, toonDur=0.06),
            k(0.42, toon={}, toonDur=0.1), k(0.42, look=None), k(0.42, to=[0.9, 0, -2.6], dur=0.3, clip='run', face=165, ease='in')])],
        props=[*PARKED(), METER(), CAR(hazard=[0.0, 99], gaze=[[0.0, -0.5, 0.2], [0.45, -0.2, -0.1]])],
        cams=[FC(0.0, [-1.9, 1.75, -1.6], [[ME2[0], 2.3, ME2[2]], [ME2[0], 0.55, ME2[2]], [1.9, 1.6, 0.6], [FING2[0], 1.95, FING2[2]]], top=0.16, bottom=0.66, drift=(0.06, 0, 0.04))])
st.cue('sfx:carDoor', 'S02', 0.02, 0.35); st.cue('sfx:stepRun', 'S02', 0.5, 0.25); st.cue('sfx:stepRun', 'S02', 0.62, 0.25)

# 3: the pound came by. The tow truck backs down the street, its lights flashing and beeping, and stops with its hook hanging in front of the car's
#    nose; the car's eyes follow it and go up to the hook
D3 = st.dur('S03'); ZT4 = -7.8; HZ4 = HOOKZ(ZT4); BK3 = 0.9
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[],
        props=[*PARKED(), METER(), CAR(gaze=[[0.0, 0.0, 0.0], [0.5, 0.2, 0.3], [0.8, 0.0, 0.5], [BK3 + 0.15, 0.0, 1.0]], lids=[[0.0, 0.0, 0.0], [BK3 + 0.15, 0.0, -0.4]], blink=[0.3]),
               TRUCK(-24.0, keys=[k(0.0, to=[1.9, 0, ZT4], dur=BK3, ease='out')]),
               P('hook', 'craneHook', pos=[1.9, 3.6, HOOKZ(-24.0)], opts={'top': TIPY}, keys=[k(0.0, to=[1.9, 3.6, HZ4], dur=BK3, ease='out'), k(BK3, to=[1.9, 3.2, HZ4], dur=0.3, ease='inOut')])],
        cams=[FC(0.0, [-2.7, 1.25, -0.4], [[1.05, 0.0, -1.85], [2.7, 1.6, -1.85], [1.9, 1.3, ZT4 + 3.1], [1.9, TIPY + 0.2, HZ4], [0.9, 0.0, ZT4 + 1.0]], top=0.1, bottom=0.86, drift=(0.1, 0, -0.1)),   # from the road, the truck coming
              FC(0.72, [0.1, 0.55, -4.3], [[1.15, 0.3, -1.8], [2.65, 1.0, -1.8], [1.9, 3.5, HZ4]], top=0.08, bottom=0.8, drift=(0.03, 0.04, 0.0))])   # (pass 2) low on the car's face: its eyes go up to the hook over it
[st.cue('sfx:beep', 'S03', round(0.05 + 0.24 * i, 3), 0.25) for i in range(4)]; st.cue('engine', 'S03', 0.0, 0.2, 1.0); st.cue('sfx:brake', 'S03', BK3 - 0.2, 0.2)

# 4: it took him. He comes back from the pavement with a baguette, passes under the hook: it drops and takes him by the collar; it goes up: his body
#    stretches, his feet stay on the road; then they let go and he goes up, limp as a noodle
D4 = st.dur('S04'); AR4, CT4, SH4, PP4 = 0.2, 0.2, 0.46, 0.58   # (pass 2) the stretch grows over eight frames, holds four, then snaps (it was over in three)
HX4 = 2.0; HKX4 = round(HX4 + 0.12, 3)                              # the hook behind his neck (he walks to -X)
LIFT4 = 0.68
STR4 = lambda k_=1.0, f=0.75: {'bend': {'legL': [0, 0, 0, 1 + 0.6 * k_, f], 'legR': [0, 0, 0, 1 + 0.6 * k_, f], 'shinL': [0, 0, 0, 1 + 0.6 * k_, f], 'shinR': [0, 0, 0, 1 + 0.6 * k_, f],
                               'spine': [0, 0, 0, 1 + 0.3 * k_, 0.8], 'neck': [0, 0, 0, 1 + 0.75 * k_, 0.72]}, 'face': {'pop': 0.65, 'jaw': 0.35, 'brow': 1}}
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [2.85, 0, HZ4], -90, 'stand', 'neutral', keys=[k(0.0, look=[0.6, 1.4, 0.3]), k(0.0, to=[HX4, 0, HZ4], dur=AR4, clip='walk', then='stand', ease='out'),
            k(CT4, toon={'sq': [1.06, 0.94, 1.06], 'face': {'brow': 1, 'eye': 0.5}}, toonDur=0.03), k(CT4, expr='surprised'),
            k(round(CT4 + 0.04, 3), toon=STR4(), toonDur=round(SH4 - CT4 - 0.04, 3), toonEase='out'),                                  # his feet stay on the road: he stretches
            k(SH4, toon={**STR4(1.08, 0.7), 'tremble': 1}, toonDur=0.05),                                                               # held, trembling, a little past
            k(PP4, to=[HX4, LIFT4, HZ4], dur=0.05, clip='noodle', then='noodle', glide=True, ease='out'),                               # the feet let go: he snaps up
            k(PP4, toon={'sq': [0.82, 1.24, 0.82], 'face': {'pop': 0.3}}, toonDur=0.03, toonEase='out'), k(round(PP4 + 0.06, 3), toon={'sq': [1.06, 0.95, 1.06], 'face': {'brow': 0.5}}, toonDur=0.08),
            k(round(PP4 + 0.06, 3), expr='dizzy')])],
        props=[*PARKED(), METER(), CAR(gaze=[[0.0, 0.3, 0.6], [CT4, 0.5, 0.4]], lids=[[0.0, 0.0, 0.0]], blink=[round(PP4 + 0.1, 3)]), TRUCK(ZT4), BAG(),
               P('hook', 'craneHook', pos=[HKX4, 3.2, HZ4], opts={'top': TIPY}, keys=[k(0.08, to=[HKX4, 2.05, HZ4], dur=round(CT4 - 0.08, 3), ease='in'),
                 k(round(CT4 + 0.04, 3), to=[HKX4, 2.05 + LIFT4 * 0.9, HZ4], dur=round(SH4 - CT4 - 0.04, 3), ease='out'), k(SH4, to=[HKX4, 2.05 + LIFT4, HZ4], dur=round(PP4 - SH4, 3), ease='inOut'),
                 k(PP4, to=[HKX4, 2.12 + LIFT4, HZ4], dur=0.2, ease='out')])],
        cams=[FC(0.0, [-1.8, 0.75, -4.4], [[2.85, 0.0, HZ4], [HKX4, 3.45, HZ4], [HX4, 0.0, HZ4], [1.1, 0.3, -1.75], [HX4, 0.0, round(HZ4 - 0.4, 3)]], top=0.08, bottom=0.84, drift=(0.06, 0.04, 0))])   # (pass 2) low and in front: his shoes planted on the road while he stretches
st.cue('sfx:stepSoft', 'S04', 0.05, 0.2); st.cue('sfx:stepSoft', 'S04', 0.15, 0.2); st.cue('clang', 'S04', CT4, 0.3); st.cue('sfx:stretch', 'S04', CT4 + 0.04, 0.4); st.cue('pop', 'S04', PP4, 0.35)

# 5: him. The truck drives off down the street; he dangles from the hook behind it, swinging, arms rippling
D5 = st.dur('S05'); ZT5 = -15.0
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [HX4, LIFT4 + 0.07, HZ4], -90, 'noodle', 'dizzy', keys=[k(0.0, look=None), k(0.0, to=[1.95, LIFT4 + 0.07, round(HOOKZ(ZT5) + 0.55, 3)], dur=D5, glide=True, ease='in', clip='noodle', then='noodle')])],
        props=[*PARKED(), METER(), CAR(), TRUCK(ZT4, keys=[k(0.0, to=[1.9, 0, ZT5], dur=D5, ease='in')]), BAG(),
               P('hook', 'craneHook', pos=[HKX4, 2.12 + LIFT4, HZ4], opts={'top': TIPY}, keys=[k(0.0, to=[1.98, 2.12 + LIFT4, HOOKZ(ZT5)], dur=D5, ease='in')])],
        cams=[FC(0.0, [-1.3, 2.7, 4.6], [[1.9, TIPY + 0.2, HZ4], [1.9, 0.0, ZT4 - 3.3], [1.9, 0.6, HZ4], [0.9, 0.0, HZ4]], top=0.1, bottom=0.78)])   # higher and to the left: he hangs clear of the car's roof
st.cue('engine', 'S05', 0.0, 0.3, 0.6); st.cue('whoosh', 'S05', 0.05, 0.25, 0.4, 300, 1200)

# 6: not the car. The car alone in the empty lane, hazards blinking; its eyes stare after the truck, come back to us; a slow blink
D6 = st.dur('S06')
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[],
        props=[*PARKED(), METER(), CAR(gaze=[[0.0, 0.0, 0.1], [0.45, -0.55, 0.0]], lids=[[0.0, 0.0, 0.0], [0.45, 0.25, -0.35]], blink=[0.62])],
        cams=[FC(0.0, [0.0, 0.95, -4.7], [[1.0, 0.0, -1.8], [2.8, 1.65, -1.8], [1.9, 1.65, 1.5]], top=0.3, bottom=0.72, drift=(0.05, 0, 0.12))])
[st.cue('sfx:tick', 'S06', round(0.1 + 0.294 * i, 3), 0.22) for i in range(3)]

# 7: at the pound. The fenced lot; the hook comes down out of the sky and sets him in bay 12 between two cars; he lands with a squash and stands
D7 = st.dur('S07'); LD7 = 0.38
CL7 = r3([HB[0] + 0.1 * 0.5, 0.0, HB[2] - 0.1 * 0.866])               # his collar, behind his neck (he faces -30 deg)
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [HB[0], 1.5, HB[2]], -30, 'noodle', 'dizzy', keys=[k(0.0, look=None), k(0.05, to=HB, dur=LD7 - 0.05, glide=True, ease='in', clip='noodle', then='stand'),
            k(LD7, toon={'sq': [1.3, 0.72, 1.3]}, toonDur=0.03, toonEase='out'), k(LD7 + 0.05, toon={'sq': [0.93, 1.08, 0.93]}, toonDur=0.07), k(LD7 + 0.14, toon={'settle': 0.5}, toonDur=0.12),
            k(LD7 + 0.1, expr='unimpressed'), k(LD7 + 0.2, look='camera')])],
        props=[*POUND(), BAG(), P('hook', 'craneHook', pos=[CL7[0], 3.55, CL7[2]], opts={'top': 30.0}, keys=[k(0.05, to=[CL7[0], 2.05, CL7[2]], dur=LD7 - 0.05, ease='in'),
               k(LD7 + 0.15, to=[CL7[0], 4.5, CL7[2]], dur=0.4, ease='in')])],
        cams=[FC(0.0, [0.2, 2.3, ZP + 6.2], [[HB[0], 2.45, HB[2]], [HB[0], 0.0, HB[2]], [HB[0], 3.6, HB[2]], [2.4, 0.0, ZP + 2.5], [4.8, 0.0, ZP + 2.5], [0.0, 3.4, ZP - 9.3], [-1.8, 2.0, ZP - 9.3]], top=0.08, bottom=0.84, drift=(0.08, 0, -0.12))])   # (pass 2) inside the lot, the FOURRIÈRE sign over the far gate in the frame
st.cue('sfx:slideDown', 'S07', 0.05, 0.25); st.cue('thud', 'S07', LD7, 0.4)

# 8: they put a clamp on him. Low, at his feet: the pound's man kneels and closes a big yellow clamp on his shoe: clack; he jumps out of his skin,
#    then looks down at it
D8 = st.dur('S08'); SN8 = round(st.at('S08', 'L03', 8), 3)
AG8 = [round(F12[0] + 0.72, 3), 0, round(F12[2] + 0.12, 3)]   # (pass 2) on the open side, kneeling in profile to us (behind his legs he was hidden)
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('mec', HB, -30, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.22, toon={'face': {'lid': 1}}, toonDur=0.04), k(0.28, toon={}, toonDur=0.05), k(0.42, toon={'face': {'gx': 0.6}}, toonDur=0.05), k(0.62, toon={}, toonDur=0.06),   # (pass 2) a blink, a glance: alive in the wait
            k(SN8, toon={'sq': [0.84, 1.24, 0.84], 'hairUp': 1, 'face': {'pop': 0.55, 'brow': 1, 'jaw': 0.3}}, toonDur=0.04, toonEase='out'), k(SN8, expr='surprised'),
            k(SN8 + 0.12, toon={'sq': [1.04, 0.97, 1.04], 'face': {'brow': 0.8}}, toonDur=0.1), k(SN8 + 0.22, look=[F12[0], 0.0, F12[2]]),
            k(SN8 + 0.3, toon={'face': {'gy': 0.9, 'brow': 0.6}, 'settle': 0.5}, toonDur=0.12), k(SN8 + 0.3, expr='worried')]),
        act('agent', AG8, -95, 'kneel', 'determined', keys=[k(0.0, look=[F12[0], 0.1, F12[2]]),
            k(0.0, toon={'reach': {'L': [round(F12[0] - 0.05, 3), 0.28, round(F12[2] + 0.14, 3), 1, 0.06], 'R': [round(F12[0] + 0.1, 3), 0.28, round(F12[2] - 0.06, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'},
                'bend': {'spine': [0.35, 0, 0, 1, None]}}, toonDur=0.0),
            k(SN8 - 0.1, toon={'reach': {'L': [round(F12[0] - 0.05, 3), 0.18, round(F12[2] + 0.14, 3), 1, 0.06], 'R': [round(F12[0] + 0.1, 3), 0.18, round(F12[2] - 0.06, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'},
                'bend': {'spine': [0.45, 0, 0, 1, None]}}, toonDur=0.1, toonEase='in'),
            k(SN8 + 0.2, toon={'bend': {'spine': [0.2, 0, 0, 1, None]}, 'hands': {'L': 'flat', 'R': 'flat'}}, toonDur=0.2)])],
        props=[*POUND(), BAG(), CLAMP(snapAt=SN8, rattle=[[SN8, 0.25]])],
        cams=[FC(0.0, [2.3, 0.4, round(ZP + 2.2, 3)], [[F12[0], 0.0, F12[2]], [HB[0], 3.15, HB[2]], [AG8[0], 1.35, AG8[2]], [AG8[0] + 0.35, 0.0, AG8[2]], [F12[0] - 0.4, 0.0, F12[2]]], top=0.06, bottom=0.72, drift=(0.05, 0, -0.04),
                 inside=(-0.3, 9.0, 0.1, 6.0, 60.0, round(ZP + 3.2, 3)))])   # (pass 2) low at his feet, room for the jump, the clamp above the caption band (the camera stays out of the parked cars)   # (pass 2) low at his feet, room for the jump, the clamp above the caption band
st.cue('clang', 'S08', SN8, 0.45); st.cue('sfx:twang', 'S08', SN8 + 0.02, 0.3)

# 9: to get out. He sets off for the exit: the clamped foot does not move, so he walks right round it like a compass, one full turn, and stops where he
#    started, seeing stars
D9 = st.dur('S09'); N9, T09, ST9 = 8, 0.04, 0.072
RING9 = []
for i in range(N9 + 1):
    th = -30 + 45 * i; t = round(T09 + ST9 * i, 3)
    RING9.append(k(t, to=ROOT(th), dur=ST9, glide=True, ease='linear', face=th, turn=ST9))
    if i < N9: RING9.append(k(t, toon={'bend': {'shinR': [0.9 if i % 2 == 0 else 0.15, 0, 0, 1, None], 'legR': [0, -0.35, 0, 1, None]}, 'lay': [0, -0.32], 'face': {'brow': 0.6}}, toonDur=ST9 * 0.5))   # (pass 2) leaning out hard, the free leg swung wide
END9 = round(T09 + ST9 * N9, 3)
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        act('mec', HB, -30, 'stand', 'determined', keys=[k(0.0, look=None), *RING9, k(END9, toon={'face': {'stars': 1}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.08), k(END9, expr='dizzy')])],
        props=[*POUND(), BAG(), CLAMP()],
        cams=[FC(0.0, [2.0, 3.5, round(ZP + 2.7, 3)], [[F12[0] - 0.55, 0.0, F12[2] - 0.55], [F12[0] + 0.55, 0.0, F12[2] + 0.55], [F12[0], 2.35, F12[2]], [3.6, 0.0, ZP - 1.8]], top=0.12, bottom=0.86)])
[st.cue('sfx:stepSoft', 'S09', round(T09 + ST9 * i, 3), 0.18) for i in range(0, N9, 2)]; st.cue('sfx:bonk', 'S09', END9, 0.2)

# 10: the owner must pay. At the cash desk: he holds his card out at the slot; the cashier pushes it back with one finger and taps the notice inside
#     the glass: PROPRIÉTAIRE DU VÉHICULE UNIQUEMENT
D10 = st.dur('S10'); HB10 = ROOT(90)
SLOT = [5.13, 1.12, round(ZP + 0.05, 3)]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('mec', HB10, 90, 'stand', 'puppy', keys=[k(0.0, look=[5.3, 1.8, ZP]), k(0.12, toon={'reach': {'R': [*SLOT, 1, 0.06]}, 'hands': {'R': 'grip'}, 'face': {'brow': 0.5}}, toonDur=0.2, toonEase='out'),
            k(0.58, toon={'reach': {'R': [round(SLOT[0] - 0.22, 3), 1.1, SLOT[2], 1, 0.06]}, 'hands': {'R': 'grip'}, 'face': {'brow': 0.7}}, toonDur=0.08), k(0.95, look=[5.27, 1.7, round(ZP - 0.36, 3)]),
            k(1.1, toon={'face': {'brow': 0.8, 'lid': 0.3}}, toonDur=0.15), k(1.1, expr='unimpressed')]),
        CLERK(keys=[k(0.45, toon={'reach': {'R': [round(SLOT[0] + 0.2, 3), 1.14, SLOT[2], 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.12, toonEase='out'),
            k(0.7, toon={'reach': {'R': [5.32, 1.62, round(ZP - 0.36, 3), 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.15),
            k(0.9, toon={'reach': {'R': [5.38, 1.62, round(ZP - 0.36, 3), 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.05), k(0.98, toon={'reach': {'R': [5.31, 1.62, round(ZP - 0.36, 3), 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.05),
            k(1.06, toon={'reach': {'R': [5.38, 1.62, round(ZP - 0.36, 3), 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.05), k(1.14, toon={'reach': {'R': [5.31, 1.62, round(ZP - 0.36, 3), 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.05)])],
        props=[*POUND(), BAG(), CLAMP(), NOTICE(), P('cbcard', 'paperSheet', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.02, 0.06]}, opts={'w': 0.24, 'h': 0.15, 'big': 'CB', 'bigSize': 0.5, 'top': 0.04, 'paper': '#F2C230', 'bigInk': '#1B1B1E', 'bright': True})],
        cams=[FC(0.0, [3.3, 1.9, round(ZP + 1.55, 3)], [[5.25, 0.98, round(ZP - 0.7, 3)], [5.25, 2.4, round(ZP + 0.7, 3)], [HB10[0], 2.3, HB10[2]], [5.78, 2.3, ZP]], top=0.12, bottom=0.8, drift=(0.08, 0, -0.05))])   # the cashier's face in the tall window
st.cue('sfx:paper', 'S10', 0.55, 0.2); [st.cue('sfx:tick', 'S10', t, 0.3) for t in (0.9, 1.06)]

# 11: his owner. The cashier slaps the registration against the glass: CARTE GRISE, PROPRIÉTAIRE: and the photo of the car
D11 = st.dur('S11'); SL11 = 0.18
SHEET11 = [5.29, 1.56, round(ZP + 0.14, 3)]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', HB10, 90, 'stand', 'unimpressed', keys=[k(0.0, look=SHEET11)]),
        CLERK(keys=[k(0.0, look=SHEET11), k(SL11 - 0.08, toon={'reach': {'R': [5.33, 1.48, round(ZP + 0.4, 3), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.08, toonEase='in')])],
        props=[*POUND(), BAG(), CLAMP(), NOTICE(),
               P('grise', 'paperSheet', pos=SHEET11, ry=-90, opts={'w': 0.62, 'h': 0.44, 'head': 'CARTE GRISE', 'headSize': 0.075, 'lines': ['PROPRIÉTAIRE :'], 'lineSize': 0.06, 'top': 0.03,
                 'paper': '#E7E2EE', 'bright': True}, keys=[k(0.0, scale=0.01, dur=0.0), k(SL11, scale=1.0, dur=0.06, ease='outBack')]),
               P('photo', 'carToon', pos=[5.27, 1.43, round(ZP + 0.14, 3)], ry=-90, scale=0.085, opts={'color': MINT, 'eyes': True, 'gaze': [[0, 0.0, 0.0]]}, keys=[k(0.0, scale=0.001, dur=0.0), k(SL11, scale=0.085, dur=0.06, ease='outBack')])],
        cams=[FC(0.0, [3.75, 1.95, round(ZP + 1.25, 3)], [[5.29, 1.3, round(ZP - 0.2, 3)], [5.29, 1.82, round(ZP + 0.48, 3)], [HB10[0], 2.2, HB10[2]]], top=0.16, bottom=0.72, drift=(0.05, 0, -0.03))])
st.cue('thud', 'S11', SL11, 0.35); st.cue('sfx:paper', 'S11', SL11, 0.3)

# 12: it's the car. From inside the cash desk, through the glass: he reads, looks away, unimpressed... and his head whips back to the photo, eyes out
D12 = st.dur('S12')
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[
        act('mec', HB10, 90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, clip='doubleTakeToon', params={'side': 1, 'beat': 0.24, 'pop': 0.85, 'jaw': 0.45}, blend=0.0)])],
        props=[*POUND(), BAG(), CLAMP()],   # (from inside the cash desk the notice and the registration showed their backs, the print mirrored: left out)
        cams=[FC(0.0, [6.25, 1.85, round(ZP + 0.45, 3)], [[HB10[0], 2.45, round(HB10[2] - 0.5, 3)], [HB10[0], 2.45, round(HB10[2] + 0.5, 3)], [HB10[0], 1.05, HB10[2]], [HB10[0], 1.9, round(HB10[2] - 0.75, 3)]], top=0.14, bottom=0.7, margin=0.14, inside=(5.35, 6.95, 0.3, 2.6, round(ZP - 1.1, 3), round(ZP + 1.1, 3)))])   # (pass 2) the double take in the middle of the frame (the camera stays in the booth)
st.cue('sfx:zip', 'S12', 0.48, 0.3)

# 13: it has no hands. Back in the street: the car leans over on two wheels toward the pay machine on the pavement, its wipers flailing and
#     stretching like little arms, its eyes straining; it cannot reach
D13 = st.dur('S13'); LN13 = 0.36; TP13, FL13 = 0.06, round(D13 - 0.2, 3)   # (pass 2) 20 degrees onto two wheels (10 did not lift a wheel)
KEYPAD = [5.2, 1.0, -3.47]                                          # the pay machine's keypad (turned toward the street)
RX = lambda a: [a, math.radians(CRY), 0]
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[],
        props=[*PARKED(), METER(screen='PAYEZ ICI'), CAR(pv=[[0.0, 2]], reach=[[0.3, FL13]], reachTo=KEYPAD, reachShort=0.16, gaze=[[0.0, 0.85, -0.15], [0.5, 0.95, -0.25]], lids=[[0.0, 0.2, 0.5], [0.5, 0.35, 0.9]],
               keys=[k(TP13, rotTo=RX(LN13), dur=0.22, ease='outBack'), k(TP13, to=[2.0, 0.3, 0.0], dur=0.22, ease='outBack'),                                  # up on its two right wheels
                     k(0.42, rotTo=RX(LN13 + 0.05), dur=0.1), k(0.56, rotTo=RX(LN13 - 0.03), dur=0.1), k(0.7, rotTo=RX(LN13 + 0.06), dur=0.1), k(0.84, rotTo=RX(LN13), dur=0.08),   # straining, wobbling
                     k(FL13, rotTo=RX(0.0), dur=0.1, ease='in'), k(FL13, to=CAR0, dur=0.1, ease='in')], bounce=[[round(FL13 + 0.1, 3), 0.1]])],                   # it flops back: boing
        cams=[FC(0.0, [0.75, 0.85, -4.6], [[1.05, 0.15, -1.8], [2.75, 1.25, -1.8], [2.8, 0.9, -1.0]], top=0.2, bottom=0.78, drift=(0.04, 0.03, 0.04)),   # (pass 2) close: its face as it tips over, straining
              FC(0.5, [0.35, 1.25, -6.6], [[1.0, 0.0, -1.8], [2.85, 1.85, -1.8], [KEYPAD[0], 1.95, -3.4], [KEYPAD[0], 0.0, -3.4]], top=0.14, bottom=0.8, drift=(0.05, 0, 0.08))])   # then wide: the wipers across the gap, a hand short of the keypad
[st.cue('sfx:squeak', 'S13', round(0.15 + 0.22 * i, 3), 0.18) for i in range(4)]
st.card('S13', 'PAS DE MAINS', at=st.at('S13', 'L06', 4))

# 14: it honked. Close on its face, low: it gathers itself, squashes, and HONKS: it jumps on its wheels, rings fly out of its grille; again, longer
D14 = st.dur('S14'); HK14 = [[0.2, 0.22], [0.62, 0.38]]
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[],
        props=[*PARKED(), METER(), CAR(pv=[[0.0, 3]], honk=HK14, lids=[[0.0, 0.1, 0.3], [0.15, 0.15, 0.9]], gaze=[[0.0, 0.0, 0.2]])],
        cams=[FC(0.0, [0.55, 0.75, -4.3], [[1.0, 0.0, -1.85], [2.8, 1.7, -1.85], [1.9, 0.75, -3.4], [1.9, 1.65, 0.6]], top=0.2, bottom=0.8, drift=(0.04, 0.03, 0.06))])
for t0, d in HK14: st.cue('sfx:honk' if d < 0.3 else 'sfx:honkLong', 'S14', t0 + 0.05, 0.45)

# 15: for three weeks. Wider, across the road: days and nights flicker past; it honks at every one, the fines pile up under its wiper, the leaves
#     cover it; over it, the windows light up and go out
D15 = st.dur('S15'); P15 = 0.15                                     # (pass 2) six days in 0.9 s (two read as two days)
HK15 = [[round(0.075 + P15 * i, 3), 0.06] for i in range(6)]
st.shot('S15', 'parisStreet', setOpts=STREET, daynight={'from': 0.0, 'period': P15}, actors=[],
        props=[*PARKED(), METER(), FLATS(lit=[[round(0.07 + P15 * i, 3), (i + 1) % 2] for i in range(6)]),
               CAR(pv=[[round(0.05 * i, 3), 4 + 3 * i] for i in range(15)], leaves=[[round(0.06 * i, 3), 2 * i] for i in range(16)], honk=HK15)],
        cams=[FC(0.0, [-0.6, 0.85, -5.3], [[1.0, 0.0, -1.85], [2.8, 1.75, -1.85], [2.7, 1.7, 1.2], [1.9, 5.5, -1.0], [FX, 6.0, -2.7]], top=0.06, bottom=0.82, drift=(0.06, 0, 0.08))])   # close and low on the car: the fines and the leaves read, the sky flickers over it
[st.cue('sfx:honk', 'S15', t0, 0.25) for t0, _ in HK15]; st.cue('sfx:ticks', 'S15', 0.0, 0.25)

# 16: the neighbours complained. At their windows, in their night things: a honk: they all jump, hair on end; another: they barely flinch, eyes
#     red; then, together, each holds up a sheet: PLAINTE, dead-eyed; the next honk does not even move them
D16 = st.dur('S16'); H16 = (0.12, 0.55, 1.3); PL16 = round(st.at('S16', 'L08', 4) - 0.06, 3)
NB = [('voisin1', 0, 0, 1.0), ('voisin2', 1, 0, 1.0), ('voisin3', 2, 0, 1.0), ('voisin4', 0, 1, 1.0), ('voisin5', 2, 1, 1.0)]   # (id, column, row, -)
COLZ = (-1.8, 0.0, 1.8); FLOOR = (3.0, 6.0)
def NEIGH(nid, c, r):
    z, fl = COLZ[c], FLOOR[r]; sill = fl + 0.95; ks = [k(0.0, look=[2.0, 1.0, 0.0]), k(0.0, toon={'face': {'lid': 0.35}}, toonDur=0.0)]
    j = 0.03 * c + 0.02 * r
    ks += [k(H16[0] + j, toon={'sq': [0.84, 1.26, 0.84], 'hairUp': 1, 'face': {'pop': 0.55, 'brow': 1}}, toonDur=0.04, toonEase='out'), k(H16[0] + j, expr='surprised'),
           k(H16[0] + j + 0.14, toon={'sq': [1.04, 0.96, 1.04], 'hairUp': 0.6, 'face': {'lid': 0.5}}, toonDur=0.12),
           k(H16[1] + j, toon={'sq': [0.96, 1.06, 0.96], 'hairUp': 0.7, 'face': {'lid': 0.65, 'brow': -0.3}}, toonDur=0.04), k(H16[1] + j + 0.1, toon={'hairUp': 0.7, 'face': {'lid': 0.7, 'brow': -0.4}}, toonDur=0.1),
           k(H16[1] + j, expr='sleepy'),
           k(PL16 + j, toon={'hairUp': 0.7, 'reach': {'L': [round(FX + 0.02, 3), round(sill + 0.38, 3), round(z + 0.27, 3), 1, 0.05], 'R': [round(FX + 0.02, 3), round(sill + 0.38, 3), round(z - 0.27, 3), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}, toonDur=0.08, toonEase='out'),
           k(PL16 + j, expr='dotEyes'), k(PL16 + j + 0.05, look='camera')]
    return act(nid, [round(FX + 0.62, 3), fl, z], -90, 'stand', 'neutral', keys=ks)
PLAINTE = lambda i, c, r, t0: P(f'pl{i}', 'paperSheet', pos=[round(FX - 0.04, 3), round(FLOOR[r] + 0.95 + 0.38, 3), COLZ[c]], ry=-90, opts={'w': 0.58, 'h': 0.4, 'big': 'PLAINTE', 'bigSize': 0.42, 'top': 0.06,
                                 'paper': '#F4F1E8', 'bigInk': '#C8202A', 'bright': True}, keys=[k(0.0, scale=0.01, dur=0.0), k(t0, scale=1.0, dur=0.07, ease='outBack')])
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[NEIGH(n, c, r) for n, c, r, _ in NB],
        props=[FLATS(lit=[[0.0, 0.6]]), *[PLAINTE(i, c, r, round(PL16 + 0.03 * c + 0.02 * r, 3)) for i, (n, c, r, _) in enumerate(NB)]],
        cams=[FC(0.0, [5.3, 4.3, -2.6], [[FX, 3.75, -2.4], [FX, 5.55, 2.4], [FX, 3.75, 2.4], [FX, 5.55, -2.4]], top=0.18, bottom=0.72, drift=(0.06, 0.03, 0.03))])   # (pass 2) tighter on the first floor: three windows, the neighbours bigger
[st.cue('sfx:honk', 'S16', t, 0.3) for t in H16]; st.cue('sfx:paper', 'S16', PL16, 0.35)

# 17: against him. At the pound, the pound's man slaps the complaints on his chest, one, two, three; he swells with outrage like a balloon and floats
#     up, his clamped leg stretched down to the ground like the balloon's string
D17 = st.dur('S17'); SL17 = (0.08, 0.18, 0.28); IN17 = 0.34
AG17 = [round(HB[0] - 0.85, 3), 0, round(HB[2] + 0.55, 3)]
SIDE17 = r3([-0.62 * math.cos(math.radians(-30)), 0.0, 0.62 * math.sin(math.radians(-30))])   # 0.62 m to his right (the inflate clip swings the left leg out)
FLOAT17 = r3([HB[0] + SIDE17[0], 0.95, HB[2] + SIDE17[2]])
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[
        act('mec', HB, -30, 'stand', 'unimpressed', keys=[k(0.0, look=[AG17[0], 1.7, AG17[2]]), *[k(t, toon={'sq': [1.04, 0.96, 1.04]}, toonDur=0.03) for t in SL17],
            k(IN17, look='camera'), k(IN17, to=FLOAT17, dur=0.4, glide=True, ease='out', clip='inflate', then='inflate', params={'dur': 0.3, 'expr': 'angry'}),
            k(IN17 + 0.02, toon={'bend': {'legL': [0, 0, 0, 1.9, 0.62], 'shinL': [0, 0, 0, 1.9, 0.62]}, 'scl': {'head': [1.25, 1.12, 1.25]}, 'face': {'puff': 1, 'cheeks': 1, 'vein': 1, 'brow': -0.6}}, toonDur=0.28, toonEase='outBack')]),   # (pass 2) round as a balloon, red in the face
        act('agent', AG17, 125, 'stand', 'unimpressed', keys=[k(0.0, look=[HB[0], 1.6, HB[2]]),
            *[x for t in SL17 for x in (k(round(t - 0.06, 3), toon={'reach': {'R': [round(HB[0] - 0.12, 3), 1.45, round(HB[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.06, toonEase='in'),
                                        k(round(t + 0.03, 3), toon={'reach': {'R': [round(HB[0] - 0.4, 3), 1.3, round(HB[2] + 0.35, 3), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.05))],
            k(SL17[-1] + 0.1, toon={}, toonDur=0.15), k(SL17[-1] + 0.06, to=[5.0, 0, round(ZP + 1.1, 3)], dur=0.4, clip='walk', then='stand', ease='out', face=100), k(IN17 + 0.1, look=[FLOAT17[0], 2.0, FLOAT17[2]])])],   # he backs off: the stretched leg must be seen
        props=[*POUND(), CLAMP(), *[P(f'cpl{i}', 'paperSheet', on={'actor': 'mec', 'joint': 'torso', 'offset': [round(0.05 * (i - 1), 3), round(0.36 - 0.05 * i, 3), 0.18 + 0.004 * i]},
                 opts={'w': 0.26, 'h': 0.18, 'big': 'PLAINTE', 'bigSize': 0.42, 'top': 0.02, 'paper': '#F4F1E8', 'bigInk': '#C8202A', 'bright': True}, keys=[k(0.0, scale=0.01, dur=0.0), k(t, scale=1.0, dur=0.05, ease='outBack'), k(IN17 + 0.1, visible=False)])
                 for i, t in enumerate(SL17)],
               P('ball17', 'balloonSuit', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.34, 0.04]}, opts={'r': 0.55}, keys=[k(0.0, scale=0.01, dur=0.0), k(IN17, scale=1.0, dur=0.28, ease='outBack')]),   # (pass 2) round as a balloon
               *[P(f'cpb{i}', 'paperSheet', on={'actor': 'mec', 'joint': 'torso', 'offset': [round(0.12 * (i - 1), 3), round(0.3 - 0.07 * i, 3), 0.6 + 0.005 * i], 'rot': [0, round(0.2 * (i - 1), 2), round(0.15 * (1 - i), 2)]},
                   opts={'w': 0.26, 'h': 0.18, 'big': 'PLAINTE', 'bigSize': 0.42, 'top': 0.02, 'paper': '#F4F1E8', 'bigInk': '#C8202A', 'bright': True}, keys=[k(0.0, scale=0.01, dur=0.0), k(IN17 + 0.1, scale=1.0, dur=0.12, ease='outBack')]) for i in range(3)]],
        cams=[FC(0.0, [1.4, 1.6, round(ZP + 4.4, 3)], [[F12[0], 0.0, F12[2]], [FLOAT17[0], 3.4, FLOAT17[2]], [AG17[0], 0.0, AG17[2]], [HB[0], 2.3, HB[2]]], top=0.1, bottom=0.86, drift=(0.06, 0.08, 0))])
[st.cue('thud', 'S17', t, 0.3) for t in SL17]; st.cue('sfx:slideUp', 'S17', IN17, 0.35)

# 18: yesterday the pound came back. In the street (three weeks of fines and leaves on the car): the tow truck backs up again, its hook and sling come
#     down over the roof; the car's eyes go up to it; a very small honk
D18 = st.dur('S18'); ZT18 = round(0.0 + TIP[0], 3); BK18 = 0.55; HK18 = 3.15
FULL = {'pv': [[0.0, 44]], 'leaves': [[0.0, 32]]}
st.shot('S18', 'parisStreet', setOpts=STREET, actors=[],
        props=[*PARKED(), METER(), CAR(**FULL, gaze=[[0.0, -0.3, 0.2], [BK18, 0.0, 1.0]], lids=[[0.0, 0.0, 0.0]], honk=[[0.92, 0.06]], blink=[0.25]),
               TRUCK(-20.0, keys=[k(0.0, to=[1.9, 0, ZT18], dur=BK18, ease='out')]),
               P('hook', 'craneHook', pos=[1.9, 5.4, HOOKZ(-20.0)], opts={'top': TIPY, 'sling': True, 'slingLen': 1.12, 'slingW': 1.1, 'slingD': 1.3},   # (pass 2) four straps to the roof's corners
                 keys=[k(0.0, to=[1.9, 5.4, 0.0], dur=BK18, ease='out'), k(BK18, to=[1.9, HK18, 0.0], dur=0.35, ease='out')])],
        cams=[FC(0.0, [-2.4, 1.0, -3.6], [[1.0, 0.0, -1.85], [2.8, 1.7, -1.85], [1.9, TIPY + 0.3, 0.0], [1.9, 1.3, ZT18 + 3.1]], top=0.08, bottom=0.84, drift=(0.06, 0, 0.08))])   # from the road, clear of the truck: the car's face and the hook over it
[st.cue('sfx:beep', 'S18', round(0.05 + 0.2 * i, 3), 0.22) for i in range(3)]; st.cue('sfx:honkTiny', 'S18', 0.93, 0.3)

# 19: to fetch the car. From under it: the car goes up into the sky on its sling, swinging, wipers flailing, honking a long sad honk; leaves rain
#     off it
D19 = st.dur('S19'); UP19 = 0.12; HI19 = 2.55
st.shot('S19', 'parisStreet', setOpts=STREET, actors=[],
        props=[*PARKED(), METER(), CAR(pv=[[0.0, 44]], leaves=[[0.0, 32], [0.35, 24], [0.5, 16], [0.65, 9], [0.8, 4]], wipe=[[0.2, D19]], wipeLen=1.8, honk=[[0.42, 0.62]],
                   gaze=[[0.0, 0.0, -0.8]], lids=[[0.0, 0.0, -0.4]],
                   keys=[k(UP19, to=[1.9, HI19, 0.0], dur=D19 - UP19, ease='inOut'), k(0.3, rotTo=[0.07, math.radians(CRY), 0.05], dur=0.3), k(0.6, rotTo=[-0.06, math.radians(CRY), -0.04], dur=0.3),
                         k(0.9, rotTo=[0.05, math.radians(CRY), 0.03], dur=0.3)]),
               TRUCK(ZT18), P('hook', 'craneHook', pos=[1.9, HK18, 0.0], opts={'top': TIPY, 'sling': True, 'slingLen': 1.12, 'slingW': 1.1, 'slingD': 1.3}, keys=[k(UP19, to=[1.9, HK18 + HI19, 0.0], dur=D19 - UP19, ease='inOut')])],
        cams=[FC(0.0, [-2.6, 0.7, -4.5], [[1.0, 0.0, -1.85], [2.8, 0.0, -1.85], [1.9, HI19 + 1.7, -1.6], [1.9, HI19 + 0.3, -1.85]], top=0.06, bottom=0.86)])   # from the road, clear of the truck: its face as it goes up
st.cue('sfx:honkLong', 'S19', 0.47, 0.45); st.cue('engine', 'S19', 0.0, 0.2, 1.2)

# 20: it parked it in its space. At the pound, low: he stands in bay 12, his clamp on; a shadow; his pupils go up, then his head: the car hangs over
#     him on its sling, sinking; it stops a hand above his hair; he gulps, a little wave; the car looks down at him and blinks
D20 = st.dur('S20'); DN20 = 0.45; CARZ = round(ZP, 3); CARX = 3.6; HANG = 2.42
UR20 = -150                                                         # (pass 2) turned to us (from behind the gulp did not read)
UNDER = ROOT(UR20, foot=[4.1, 0, round(ZP - 1.05, 3)])              # where he stands now: under the front half of the car-to-be
_r20 = (math.cos(math.radians(UR20)), -math.sin(math.radians(UR20)))   # his left
WAVE20 = lambda dx=0.0: [round(UNDER[0] - 0.4 * _r20[0] + dx, 3), 1.92, round(UNDER[2] - 0.4 * _r20[1], 3)]   # his right hand up beside his head
st.shot('S20', 'parisStreet', setOpts=STREET, actors=[
        act('mec', UNDER, UR20, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.18, toon={'face': {'gy': -1, 'brow': 0.7}}, toonDur=0.08),
            k(0.42, look=[UNDER[0], 4.0, UNDER[2] - 0.4]), k(0.42, toon={'face': {'brow': 0.9, 'eye': 0.4, 'sweat': 1}}, toonDur=0.1), k(0.42, expr='worried'),
            k(0.78, expr='gulp'), k(0.78, toon={'face': {'brow': 0.9, 'sweat': 1, 'gulp': 1}, 'sq': [1.03, 0.96, 1.03]}, toonDur=0.25),
            k(1.0, look='camera'), k(1.0, expr='nervous'), k(1.05, toon={'reach': {'R': [*WAVE20(), 1, 0.06]}, 'hands': {'R': 'spread'}, 'face': {'sweat': 1}}, toonDur=0.1),
            *[k(round(1.15 + 0.08 * i, 3), toon={'reach': {'R': [*WAVE20(0.07 if i % 2 else -0.07), 1, 0.06]}, 'hands': {'R': 'spread'}, 'face': {'sweat': 1}}, toonDur=0.06) for i in range(4)]])],   # a sheepish little wave
        props=[*POUND(), BAG(), CLAMP(),
               CAR(pos=[CARX, 5.6, CARZ], pid='car', pv=[[0.0, 44]], leaves=[[0.0, 4]], gaze=[[0.0, 0.0, -1.0], [0.9, -0.3, -1.0]], blink=[1.25],
                   keys=[k(0.0, to=[CARX, HANG, CARZ], dur=DN20, ease='out'), k(DN20, rotTo=[0.03, math.radians(CRY), -0.02], dur=0.3), k(DN20 + 0.3, rotTo=[-0.02, math.radians(CRY), 0.015], dur=0.3)]),
               P('hook', 'craneHook', pos=[CARX, 5.6 + 3.15, CARZ], opts={'top': 40.0, 'sling': True, 'slingLen': 1.12, 'slingW': 1.1, 'slingD': 1.3}, keys=[k(0.0, to=[CARX, HANG + 3.15, CARZ], dur=DN20, ease='out')])],
        cams=[FC(0.0, [2.15, 0.65, round(ZP - 4.1, 3)], [[UNDER[0], 0.0, UNDER[2]], [UNDER[0], 2.3, UNDER[2]], [CARX, HANG, round(CARZ - 1.75, 3)], [CARX, HANG + 1.65, round(CARZ - 1.0, 3)], [UNDER[0] - 0.35, 0.0, UNDER[2]]], top=0.08, bottom=0.74, drift=(0.05, 0, 0.05))])   # (pass 2) the clamp above the caption band
st.cue('sfx:slideDownSlow', 'S20', 0.0, 0.3); st.cue('sfx:gulp', 'S20', 0.8, 0.4)

# 21: on him. It drops: the car lands, bounces on its springs, dust; his head sticks out flattened in front of the bumper, tongue out, eyes spinning,
#     stars; the baguette, flat as a ruler, beside him
D21 = st.dur('S21'); HIT21 = 0.1
HEADZ = round(CARZ - 1.75 - 0.32, 3); LIE = [3.92, 0.0, round(HEADZ + 0.88, 3)]
FLATCAM = ([LIE[0], 1.6, round(HEADZ + 0.25, 3)], [LIE[0], 0.06, round(HEADZ - 0.2, 3)], 42)   # (pass 2) just in front of the bumper, looking down and forward: the top of his head points up the frame (from above the bonnet the bonnet hid him)
FLAT = {'sq': [1.3, 1.0, 0.1], 'scl': {'head': [1.45, 1.12, 0.34]}, 'face': {'tongue': 1, 'tongueLen': 1.5, 'stars': 1, 'brow': -0.2}}
st.shot('S21', 'parisStreet', setOpts=STREET, actors=[
        act('mec', UNDER, UR20, 'stand', 'worried', keys=[k(0.0, look=[UNDER[0], 4.0, UNDER[2] - 0.4]), k(0.0, toon={'face': {'pop': 0.5, 'brow': 1}}, toonDur=0.0),
            k(HIT21, to=LIE, dur=0.02, glide=True, clip='lieBack', then='lieBack', face=0), k(HIT21, clip='lieBack', blend=0.0), k(HIT21, look=None),
            k(HIT21, toon=FLAT, toonDur=0.0), k(HIT21, expr='dizzy')])],
        props=[*POUND(), CLAMP(),
               CAR(pos=[CARX, HANG, CARZ], pv=[[0.0, 44]], leaves=[[0.0, 4]], bounce=[[HIT21, 0.12]], sag=0.4, gaze=[[0.0, 0.0, -1.0], [0.4, 0.3, -0.6]], lids=[[0.0, 0.0, 0.0], [0.45, 0.1, -0.2]],
                   keys=[k(0.0, to=[CARX, 0.0, CARZ], dur=HIT21, ease='in')]),
               P('flatbag', 'baguette', pos=[round(LIE[0] + 0.55, 3), 0.02, round(HEADZ + 0.05, 3)], ry=20, scale=1.0, keys=[k(0.0, visible=False), k(HIT21, visible=True), k(HIT21, squash=[1.25, 0.25, 1.25], dur=0.0)]),
               P('dust21', 'dustPuff', pos=[CARX, 0.05, round(CARZ - 1.6, 3)], opts={'period': 0.7}, keys=[k(0.0, visible=False), k(HIT21, visible=True), k(HIT21 + 0.65, visible=False)]),
               P('stars21', 'impactStars', pos=[LIE[0], 0.25, HEADZ], opts={'n': 6, 'r': 0.35, 'at': HIT21, 'dur': 0.6, 'size': 0.08})],
        fx=[{'type': 'shake', 'at': HIT21, 'dur': 0.15, 'amount': 0.014}],
        cams=[FC(0.0, [0.6, 0.85, round(ZP - 3.9, 3)], [[2.75, 0.0, round(CARZ - 1.85, 3)], [4.45, 1.75, round(CARZ - 1.85, 3)], [LIE[0], 0.05, round(HEADZ - 0.3, 3)], [CARX, HANG + 1.0, round(CARZ - 0.6, 3)]], top=0.1, bottom=0.8),   # (pass 2) the drop, from the front-left
              cam(0.38, FLATCAM[0], r3([FLATCAM[0][0], FLATCAM[0][1] - 0.06, FLATCAM[0][2] - 0.04]), FLATCAM[1], FLATCAM[1], lens=FLATCAM[2])])   # then from above the bonnet: his flat face right side up
st.cue('splat', 'S21', HIT21, 0.55); st.cue('thud', 'S21', HIT21, 0.5); st.cue('sfx:spring', 'S21', HIT21 + 0.08, 0.25)

# 22: he pays for the space. His arm comes out from under the car and stretches all the way to the pay machine; a card at the slot: beep; the ticket
#     comes out; the hand brings it back and holds it up beside his flat face. The car looks down at him, blinks, and gives a tiny honk
D22 = st.dur('S22'); SLOT22 = [5.245, 0.74, round(ZP - 2.0, 3)]; TRAY22 = [5.24, 0.58, round(ZP - 2.0, 3)]
SHOW22 = [round(LIE[0] + 0.42, 3), 0.42, round(HEADZ - 0.22, 3)]
st.shot('S22', 'parisStreet', setOpts=STREET, actors=[
        act('mec', LIE, 0, 'lieBack', 'dizzy', keys=[k(0.0, look=None), k(0.0, toon=FLAT, toonDur=0.0),
            k(0.18, toon={**FLAT, 'face': {**FLAT['face'], 'stars': 0.4}, 'reach': {'L': [*SLOT22, 1, 0.07]}, 'hands': {'L': 'point'}}, toonDur=0.32, toonEase='outBack'),
            k(0.58, toon={**FLAT, 'face': {**FLAT['face'], 'stars': 0.0}, 'reach': {'L': [round(SLOT22[0] + 0.05, 3), SLOT22[1], SLOT22[2], 1, 0.07]}, 'hands': {'L': 'point'}}, toonDur=0.05),
            k(0.95, toon={**FLAT, 'face': {**FLAT['face'], 'stars': 0.0}, 'reach': {'L': [*TRAY22, 1, 0.07]}, 'hands': {'L': 'grip'}}, toonDur=0.12),
            k(1.15, toon={**FLAT, 'face': {**FLAT['face'], 'stars': 0.0, 'tongue': 0.6}, 'reach': {'L': [*SHOW22, 1, 0.07]}, 'hands': {'L': 'grip'}}, toonDur=0.32, toonEase='inOut'),
            k(1.6, expr='deadpan'), k(1.6, toon={**FLAT, 'face': {**FLAT['face'], 'stars': 0.0, 'tongue': 0.6, 'lid': 0.45}, 'reach': {'L': [*SHOW22, 1, 0.07]}, 'hands': {'L': 'grip'}}, toonDur=0.15)])],
        props=[*POUND(), PMETER(ticketAt=0.75, ticketGone=1.05, stickerW=0.4, stickerH=0.16, stickerY=0.32, stickerBg='#B0101A', stickerWrap=True), CLAMP(),
               CAR(pos=[CARX, 0.0, CARZ], pv=[[0.0, 44]], leaves=[[0.0, 4]], sag=0.4, gaze=[[0.0, 0.3, -0.6], [0.3, 0.85, -0.5], [0.9, 0.9, -0.55], [1.25, 0.1, -0.85], [2.3, 0.0, -0.9]], blink=[2.5], honk=[[2.8, 0.08]]),   # (pass 2) its pupils follow the arm out and back
               P('flatbag', 'baguette', pos=[round(LIE[0] + 0.55, 3), 0.02, round(HEADZ + 0.05, 3)], ry=20, keys=[k(0.0, squash=[1.25, 0.25, 1.25], dur=0.0)]),
               P('tick22', 'paperSheet', pos=TRAY22, face='camera', opts={'w': 0.36, 'h': 0.26, 'head': 'FRAIS DE GARDE', 'headSize': 0.14, 'big': '45 €', 'bigSize': 0.36, 'top': 0.06,
                 'paper': '#FFFFFF', 'ink': '#14161A', 'bigInk': '#B0101A', 'bright': True}, keys=[k(0.0, scale=0.01, dur=0.0), k(1.05, scale=1.0, dur=0.06, ease='out'),
                 k(1.15, to=[SHOW22[0], round(SHOW22[1] + 0.06, 3), round(SHOW22[2] - 0.19, 3)], dur=0.32, ease='inOut')])],   # (pass 2) a ticket that reads
        cams=[cam(0.0, [4.62, 3.3, round(HEADZ + 1.35, 3)], [4.62, 3.22, round(HEADZ + 1.3, 3)], [4.62, 0.0, round(HEADZ - 0.12, 3)], [4.62, 0.0, round(HEADZ - 0.12, 3)], lens=50),   # (lens = the vertical field of view in degrees)   # (pass 2) from above the bonnet: his face right side up, the arm to the machine
              cam(1.22, [round(LIE[0] + 0.36, 3), 1.36, round(HEADZ + 0.24, 3)], [round(LIE[0] + 0.36, 3), 1.31, round(HEADZ + 0.22, 3)], [round(LIE[0] + 0.38, 3), 0.1, round(HEADZ - 0.2, 3)], [round(LIE[0] + 0.38, 3), 0.1, round(HEADZ - 0.2, 3)], lens=52),   # close: the ticket beside his flat face
              FC(2.3, [2.2, 0.55, round(ZP - 4.4, 3)], [[2.75, 0.0, round(CARZ - 1.8, 3)], [4.45, 1.7, round(CARZ - 1.8, 3)], [LIE[0], 0.05, round(HEADZ - 0.3, 3)]], top=0.16, bottom=0.8)])   # the car's face: a blink, a tiny honk
st.cue('sfx:stretch', 'S22', 0.18, 0.35); st.cue('sfx:beep', 'S22', 0.6, 0.35); st.cue('sfx:paper', 'S22', 0.75, 0.25); st.cue('sfx:honkTiny', 'S22', 2.8, 0.35)

st.write("La fourrière", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'agent': {'preset': 'worker', 'seed': 451, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'caissiere': {'preset': 'madame', 'seed': 452, 'build': {'width': 0.9, 'headWidth': 1.25}},
    'voisin1': {'preset': 'mamie', 'seed': 453, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'voisin2': {'preset': 'gamin', 'seed': 454, 'build': {'height': 0.68, 'headWidth': 1.2}},
    'voisin3': {'preset': 'femme', 'seed': 455, 'build': {'width': 0.9, 'headWidth': 1.25}},
    'voisin4': {'preset': 'boss', 'seed': 456, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'voisin5': {'preset': 'fringant', 'seed': 457, 'build': {'width': 0.9, 'headWidth': 1.25}},
})
