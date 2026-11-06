#!/usr/bin/env python3
"""La balance (the user's story): this idiot steps on the scale and sees 100 kilos. Tiptoes: 100. Holds his breath: 100.
He puts it in airplane mode so it is lighter; the scale takes off through the window; he jumps on it so as not to put the
weight back on; it flies over the gym, he waves; up high it reads zero, his ideal weight; it lands on a cloud that reads
"hors service"; he has never felt so light."""
from story_kit import *

st = Story('balance')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 8), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0), ('S08', 'L06', 6),
         ('S09', 'L07', 0), ('S10', 'L07', 3), ('S11', 'L08', 0), ('S12', 'L08', 3), ('S13', 'L09', 0), ('S14', 'L10', 0), ('S15', 'L11', 0), ('S16', 'L12', 0),
         ('S17', 'L13', 0), ('S18', 'L13', 5), ('S19', 'L14', 0)])
PI = math.pi
SW = 0.44                     # the scale's width (a real one is ~0.3: a little oversized so it reads in wide shots)
TOP = 0.056                   # standing height on it
SX, SZ = 0.3, -1.6            # the scale on the bathroom floor
DZ = SZ + 0.143               # its display (flat, near the front edge)
ON = [SX, TOP, SZ - 0.06]     # where he stands on it (toes short of the display)
WINDOW = P('win', 'window', pos=[-1.0, 1.15, -3.365], opts={'w': 1.0, 'h': 1.1, 'clouds': True, 'color': '#2F7F8C'})


def SCALE(pos=(SX, 0, SZ), ry=0, keys=None, **o):
    d = P('scale', 'bathScale', pos=list(pos), ry=ry, opts={'w': SW, **o})
    if keys: d['keys'] = keys
    return d


def DISPLAY(at=0.0):          # looking down at the display from in front, a little to the right
    return [cam(at, [SX + 0.06, 0.8, DZ + 0.5], [SX + 0.055, 0.76, DZ + 0.46], [SX, 0.05, DZ - 0.01], [SX, 0.05, DZ - 0.01], lens=40)]


# 1-6: 100 kilos; on tiptoe: 100; holding his breath: 100
st.shot('S01', 'bathroom', actors=[act('mec', [SX, 0, SZ - 0.5], 0, 'stand', 'neutral', keys=[k(st.at('S01', 'L01', 4) - 0.12, to=ON, dur=0.36, clip='walk', then='lookDown'), k(st.at('S01', 'L01', 7), expr='unimpressed')])],
        props=[WINDOW, SCALE()], cams=[cam(0.0, [1.3, 1.25, 2.2], [1.25, 1.24, 2.02], [SX, 0.92, SZ], [SX, 0.92, SZ], lens=50)])
st.shot('S02', 'bathroom', actors=[act('mec', ON, 0, 'lookDown', 'unimpressed')], props=[WINDOW, SCALE(show=[[st.at('S02', 'L01', 10) - 0.3, 100, 0]])], cams=DISPLAY())
st.shot('S03', 'bathroom', actors=[act('mec', ON, 0, 'lookDown', 'unimpressed', keys=[k(st.at('S03', 'L02', 5) - 0.3, clip='onTiptoes', expr='suspicious')])],
        props=[WINDOW, SCALE(show=[[0.0, 100]])], cams=[cam(0.0, [2.25, 1.2, 1.35], [2.2, 1.18, 1.2], [SX, 1.0, SZ], [SX, 0.98, SZ], lens=50)])
st.shot('S04', 'bathroom', actors=[act('mec', ON, 0, 'onTiptoes', 'suspicious')], props=[WINDOW, SCALE(show=[[0.0, 100, 0]])], cams=DISPLAY())
st.shot('S05', 'bathroom', actors=[act('mec', ON, 0, 'stand', 'neutral', keys=[k(st.at('S05', 'L04', 1) - 0.1, clip='holdBreath', expr='angry')])],
        props=[WINDOW, SCALE(show=[[0.0, 100]])], cams=[cam(0.0, [SX + 0.36, 1.92, SZ + 1.6], [SX + 0.34, 1.92, SZ + 1.42], [SX, 1.9, SZ], [SX, 1.9, SZ], lens=44, shake=0.004)])
st.shot('S06', 'bathroom', actors=[act('mec', ON, 0, 'holdBreath', 'angry')], props=[WINDOW, SCALE(show=[[0.0, 100, 0]])],
        cams=[cam(0.0, [SX - 0.08, 0.82, DZ + 0.5], [SX - 0.075, 0.78, DZ + 0.46], [SX, 0.05, DZ - 0.01], [SX, 0.05, DZ - 0.01], lens=40)])
# 7-10: airplane mode; the scale takes off, out of the window
KNEEL = [SX - 0.58, 0, SZ + 0.02]
st.shot('S07', 'bathroom', actors=[act('mec', KNEEL, 90, 'kneelPress', 'suspicious')], props=[WINDOW, SCALE(pressAt=st.at('S07', 'L06', 4))],
        cams=[cam(0.0, [0.75, 1.0, 1.35], [0.72, 0.98, 1.22], [0.0, 0.6, SZ], [0.0, 0.58, SZ], lens=50)])
st.shot('S08', 'bathroom', actors=[act('mec', KNEEL, 90, 'kneelPress', 'suspicious')], props=[WINDOW, SCALE(show=[[0.12, 'plane']], pressAt=0.0)], cams=DISPLAY())
YAW_WIN = math.degrees(math.atan2(-1.0 - SX, -3.3 - SZ))   # heading from the scale to the window
st.shot('S09', 'bathroom', actors=[act('mec', KNEEL, 90, 'kneel', 'suspicious', keys=[k(0.22, clip='sitFloor', expr='surprised')])],
        props=[WINDOW, SCALE(wingsAt=0.04, bob=[0.025, 1.6, 0.55], keys=[k(0.1, to=[SX, 0.72, SZ], dur=0.45, ease='out'), k(0.45, rotTo=[0, math.radians(YAW_WIN), 0], dur=0.35)])],
        cams=[cam(0.0, [0.75, 0.85, 1.2], [0.7, 0.88, 1.05], [-0.05, 0.75, -1.8], [-0.05, 0.8, -1.8], lens=50, shake=0.006)])
# 10-12: out of the window (seen from the street); he jumps on it from the sill; they fly off down the street
BX, BY, BZ = 10.15, 6.19, -2.0          # the open window on the facade (sill top), facade facing -X
HOV = [8.72, 5.72, -2.0]                # the scale waiting outside
BLD = [P('bld', 'haussmann', pos=[BX, 0, BZ], ry=-90, opts={'w': 12.6, 'h': 18, 'floors': 6, 'cols': 5, 'color': '#F2DCCB', 'awning': '#2F7F5C'}),
       P('ow', 'openWindow', pos=[BX - 0.015, BY, BZ], ry=-90, opts={'w': 1.2, 'h': 2.2})]
st.shot('S10', 'parisStreet', actors=[act('mec', [BX + 0.7, BY, BZ], -90, 'stand', 'surprised', keys=[k(0.42, to=[BX - 0.2, BY, BZ], dur=0.42, clip='walk', face='keep', then='stand')])],
        props=BLD + [SCALE(pos=[BX + 0.7, BY + 1.0, BZ], ry=-90, wingsAt=-1, bob=[0.015, 1.4, 0.85], keys=[k(0.0, path=[[BX - 0.45, BY + 1.0, BZ], [9.3, 6.4, BZ + 0.15], HOV], dur=0.8, ease='out')])],
        cams=[cam(0.0, [6.6, 3.6, 0.4], [6.65, 3.68, 0.3], [9.4, 6.9, BZ], [9.35, 6.85, BZ], lens=44, shake=0.006)])
st.shot('S11', 'parisStreet', actors=[act('mec', [BX - 0.2, BY, BZ], -90, 'stand', 'happy', keys=[k(0.12, to=[HOV[0], HOV[1] + TOP, HOV[2] + 0.04], dur=0.42, clip='airborne', arc=0.55, face='keep', then='surfRide')])],
        props=BLD + [SCALE(pos=HOV, ry=-90, wingsAt=-1, bob=[0.015, 1.4, 0.0])],
        cams=[cam(0.0, [4.7, 7.35, 1.35], [4.8, 7.3, 1.15], [9.2, 6.95, BZ], [9.15, 6.85, BZ], lens=44)])
F0, F1 = [4.0, 9.0, 1.0], [1.0, 10.0, -11.0]      # the flight down the street (1.55 s)
fy = math.degrees(math.atan2(F1[0] - F0[0], F1[2] - F0[2])); D12 = st.dur('S12')
off, lk = [1.5, 0.55, -3.3], [0, 1.25, 0]
st.shot('S12', 'parisStreet', actors=[act('mec', [F0[0], F0[1] + TOP, F0[2]], fy, 'surfRide', 'happy', keys=[k(0.0, to=[F1[0], F1[1] + TOP, F1[2]], dur=D12, glide=True, face='keep', ease='linear')])],
        props=[SCALE(pos=F0, ry=fy, wingsAt=-1, keys=[k(0.0, to=F1, dur=D12, ease='linear')])],
        cams=[cam(0.0, [F0[i] + off[i] for i in range(3)], [F1[i] + off[i] for i in range(3)], [F0[i] + lk[i] for i in range(3)], [F1[i] + lk[i] for i in range(3)], lens=44)])
# 13-14: over the gym; he waves
GYM = P('gym', 'gymBuilding', pos=[3.0, 0, -10.0], opts={'w': 26, 'd': 30, 'h': 9, 'text': 'SALLE DE SPORT'})
G0, G1 = [-0.8, 12.0, 26.0], [6.2, 12.0, 26.0]; D13 = st.dur('S13')
off13, lk13 = [0.3, -0.3, 8.6], [0.3, -0.3, -20.9]
st.shot('S13', 'aerialSuburb', actors=[act('mec', [G0[0], G0[1] + TOP, G0[2]], 90, 'surfRide', 'happy', keys=[k(0.0, to=[G1[0], G1[1] + TOP, G1[2]], dur=D13, glide=True, face='keep', ease='linear')])],
        props=[GYM, SCALE(pos=G0, ry=90, wingsAt=-1, keys=[k(0.0, to=G1, dur=D13, ease='linear')])],
        cams=[cam(0.0, [G0[i] + off13[i] for i in range(3)], [G1[i] + off13[i] for i in range(3)], [G0[i] + lk13[i] for i in range(3)], [G1[i] + lk13[i] for i in range(3)], lens=44)])
W0, W1 = [7.4, 12.0, 26.0], [10.6, 12.0, 26.0]; D14 = st.dur('S14')
off14, lk14 = [2.9, 1.9, 0.9], [0, 1.25, 0]
st.shot('S14', 'aerialSuburb', actors=[act('mec', [W0[0], W0[1] + TOP, W0[2]], 90, 'rideWave', 'happy', keys=[k(0.0, to=[W1[0], W1[1] + TOP, W1[2]], dur=D14, glide=True, face='keep', ease='linear')])],
        props=[GYM, SCALE(pos=W0, ry=90, wingsAt=-1, keys=[k(0.0, to=W1, dur=D14, ease='linear')])],
        cams=[cam(0.0, [W0[i] + off14[i] for i in range(3)], [W1[i] + off14[i] for i in range(3)], [W0[i] + lk14[i] for i in range(3)], [W1[i] + lk14[i] for i in range(3)], lens=44)])
# 15-16: up high it reads zero; his ideal weight
HY = 120.0
st.shot('S15', 'skyHigh', actors=[act('mec', [0, HY + TOP, -0.06], 0, 'surfRide', 'happy')], props=[SCALE(pos=(0, HY, 0), wingsAt=-1, show=[[0.0, 100], [st.at('S15', 'L11', 4) - 0.36, 0, 100]])],
        cams=[cam(0.0, [0.06, HY + 0.82, 0.64], [0.055, HY + 0.78, 0.6], [0, HY + 0.05, 0.132], [0, HY + 0.05, 0.132], lens=40)])
st.shot('S16', 'skyHigh', actors=[act('mec', [0, HY + TOP, -0.06], 0, 'rideCheer', 'happy')], props=[SCALE(pos=(0, HY, 0), wingsAt=-1, show=[[0.0, 0]])],
        cams=[cam(0.0, [0.75, HY + 0.55, 2.6], [0.7, HY + 0.6, 2.35], [0, HY + 1.25, 0], [0, HY + 1.28, 0], lens=44)])
# 17-19: it lands on a cloud that reads "hors service"; he has never felt so light
CY, CT = 100.0, 1.1
CLOUD = lambda **o: P('cloud', 'serviceCloud', pos=[0, CY, 0], opts={'w': 3.6, 'top': CT, 'text': 'HORS SERVICE', **o})
L0, L1 = [-2.4, CY + CT + 1.6, 1.8], [0.25, CY + CT, -0.2]; T17 = 0.55
st.shot('S17', 'skyHigh', actors=[act('mec', [L0[0], L0[1] + TOP, L0[2]], 125, 'surfRide', 'happy', keys=[k(0.0, to=[L1[0], L1[1] + TOP, L1[2]], dur=T17, glide=True, face='keep', ease='out'), k(T17, clip='land', expr='surprised')])],
        props=[CLOUD(squashAt=T17), SCALE(pos=L0, ry=125, wingsAt=-1, show=[[0.0, 0]], keys=[k(0.0, to=L1, dur=T17, ease='out')])],
        cams=[cam(0.0, [3.3, CY + 2.05, 5.4], [3.15, CY + 2.0, 5.1], [-0.15, CY + 1.85, 0.0], [0.0, CY + 1.75, 0.0], lens=44, shake=0.006)])
st.shot('S18', 'skyHigh', actors=[act('mec', [L1[0], L1[1] + TOP, L1[2]], 125, 'lookDown', 'surprised')],
        props=[CLOUD(blinkAt=0.12), SCALE(pos=L1, ry=125, wingsAt=-1, show=[[0.0, 0]])],
        cams=[cam(0.0, [0.15, CY + 1.58, 7.1], [0.15, CY + 1.56, 6.8], [0.08, CY + 1.55, 0.0], [0.08, CY + 1.53, 0.0], lens=44)])
st.shot('S19', 'skyHigh', actors=[act('mec', [-0.25, CY + CT, -0.25], 70, 'lieRelax', 'happy')],
        props=[CLOUD(blinkAt=0.0), SCALE(pos=[0.75, CY + CT, 0.1], ry=200, wingsAt=-1, show=[[0.0, 0]])],
        cams=[cam(0.0, [1.0, CY + 2.6, 2.5], [1.9, CY + 3.6, 5.2], [0.0, CY + 1.2, 0.0], [0.0, CY + 1.0, 0.0], lens=44, ease='inOut')])
st.card('S08', 'MODE AVION'); st.card('S16', 'POIDS IDÉAL')
st.cue('clack', 'S01', st.at('S01', 'L01', 4) + 0.24, 0.35); st.cue('sfx:beep', 'S02', st.at('S02', 'L01', 10) + 0.05, 0.3); st.cue('sfx:squeak', 'S03', st.at('S03', 'L02', 5) - 0.25, 0.25)
st.cue('sfx:beep', 'S04', 0.36, 0.3); st.cue('sfx:gasp', 'S05', st.at('S05', 'L04', 1) - 0.1, 0.35); st.cue('sfx:beep', 'S06', 0.36, 0.3); st.cue('thud', 'S06', 0.4, 0.3)
st.cue('sfx:click', 'S07', st.at('S07', 'L06', 4), 0.4); st.cue('pop', 'S08', 0.12, 0.35); st.cue('sfx:jet', 'S09', 0.08, 0.25); st.cue('whoosh', 'S10', 0.05, 0.5)
st.cue('whoosh', 'S11', 0.12, 0.45); st.cue('thud', 'S11', 0.56, 0.4); st.cue('gust', 'S12', 0.0, 0.35); st.cue('gust', 'S13', 0.0, 0.3); st.cue('sfx:beep', 'S15', st.at('S15', 'L11', 4) + 0.02, 0.3)
st.cue('sfx:fanfare', 'S16', 0.05, 0.25); st.cue('sfx:boing', 'S17', T17, 0.45); [st.cue('sfx:beep', 'S18', 0.12 + 0.5 * i, 0.22) for i in range(3)]; st.cue('gust', 'S19', 0.2, 0.2)
st.write('La balance', {'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.9, 'headWidth': 1.3, 'headScale': 1.0, 'belly': 0.1}}})
