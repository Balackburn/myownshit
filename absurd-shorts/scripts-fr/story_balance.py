#!/usr/bin/env python3
"""La balance (the user's story): this idiot steps on the scale and sees 100 kilos. Tiptoes: 100. Holds his breath: 100.
He puts it in airplane mode so it is lighter; the scale takes off through the window; he jumps on it so as not to put the
weight back on; it flies over the gym, he waves; up high it reads zero, his ideal weight; it lands on a cloud that reads
"hors service"; he has never felt so light.
Round-1 critic notes applied: the winged scale grows into a red-winged little plane with a dark underside and contrails, sits
at 55-72 % of the frame in the ride shots (a hero shot in S12); the title card band and the caption band stay clear of the
face and of the « HORS SERVICE » panel; the tiptoe and the held breath (puffed cheeks, red swelling head) read in the picture;
the opening lands his shoe on the scale, then tilts up to his face."""
from story_kit import *

st = Story('balance')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 8), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0), ('S08', 'L06', 6),
         ('S09', 'L07', 0), ('S10', 'L07', 3), ('S11', 'L08', 0), ('S12', 'L08', 3), ('S13', 'L09', 0), ('S14', 'L10', 0), ('S15', 'L11', 0), ('S16', 'L12', 0),
         ('S17', 'L13', 0), ('S18', 'L13', 5), ('S19', 'L14', 0)])
PI = math.pi
SW = 0.44                     # the scale's width (a real one is ~0.3: a little oversized so it reads in wide shots)
GROW = 1.3                    # it grows into a little plane when the wings come out
MAT = 0.027                   # the bath mat under it
TOP = 0.056                   # standing height on the scale (before it grows)
TOPF = TOP * GROW             # standing height on the grown, flying scale
SX, SZ = 0.3, -1.6            # the scale on the bathroom floor
DZ = SZ + 0.143               # its display (flat, near the front edge)
ON = [SX, MAT + TOP, SZ - 0.11]   # where he stands on it (toes short of the display)
WINDOW = P('win', 'window', pos=[-1.0, 1.15, -3.365], opts={'w': 1.0, 'h': 1.1, 'clouds': True, 'color': '#2F7F8C'})
BATHMAT = P('mat', 'carpet', pos=[SX, 0, SZ + 0.12], opts={'w': 1.5, 'd': 1.05, 'color': '#2F7F8C', 'inner': '#F4F1E8'})
BATH = [WINDOW, BATHMAT]


def SCALE(pos=(SX, MAT, SZ), ry=0, keys=None, **o):
    d = P('scale', 'bathScale', pos=list(pos), ry=ry, opts={'w': SW, **o})
    if keys: d['keys'] = keys
    return d


def FLY(pos, ry, keys=None, trail=2.6, **o):   # the flying scale: wings out, grown, contrails
    return SCALE(pos=pos, ry=ry, keys=keys, wingsAt=-1, grow=GROW, trail=trail, outline=0.009, **o)


def DISPLAY(at=0.0, back=0.5, lens=40, roll=None, dx=0.06):   # looking down at the display from in front
    return [cam(at, [SX + dx, MAT + 0.3 + back, DZ + back], [SX + dx * 0.9, MAT + 0.27 + back * 0.95, DZ + back * 0.92], [SX, MAT + 0.05, DZ - 0.01], [SX, MAT + 0.05, DZ - 0.01], lens=lens, roll=roll)]


def TRACK(p0, p1, off, lk, lens=44, shake=None):   # a camera locked to a moving subject (same linear motion)
    return [cam(0.0, [p0[i] + off[i] for i in range(3)], [p1[i] + off[i] for i in range(3)], [p0[i] + lk[i] for i in range(3)], [p1[i] + lk[i] for i in range(3)], lens=lens, shake=shake)]


def RIDE(aid, p0, p1, ry, clip, expr, dur, **kw):   # him standing on the flying scale, both moving together
    return act(aid, [p0[0], p0[1] + TOPF, p0[2]], ry, clip, expr, keys=[k(0.0, to=[p1[0], p1[1] + TOPF, p1[2]], dur=dur, glide=True, face='keep', ease='linear')], **kw)


# 1-6: 100 kilos; on tiptoe: 100; holding his breath: 100
T_STEP = 0.3
st.shot('S01', 'bathroom', actors=[act('mec', [SX, 0, SZ - 0.5], 0, 'stand', 'neutral', keys=[k(T_STEP, to=ON, dur=0.36, clip='walk', then='lookDown'), k(st.at('S01', 'L01', 7), expr='unimpressed')])],
        props=BATH + [SCALE()],
        cams=[cam(0.0, [SX + 0.35, 0.45, SZ + 0.95], [SX + 0.34, 0.44, SZ + 0.9], [SX, 0.12, SZ - 0.05], [SX, 0.13, SZ - 0.05], lens=44),
              {**cam(0.8, [SX + 0.4, 1.38, SZ + 1.55], [SX + 0.38, 1.4, SZ + 1.45], [SX, 1.75, SZ], [SX, 1.75, SZ], lens=44), 'cut': False, 'glide': 0.55}])
st.shot('S02', 'bathroom', actors=[act('mec', ON, 0, 'lookDown', 'unimpressed')], props=BATH + [SCALE(show=[[st.at('S02', 'L01', 10) - 0.3, 100, 0]])], cams=DISPLAY())
st.shot('S03', 'bathroom', actors=[act('mec', ON, 0, 'lookDown', 'unimpressed', keys=[k(st.at('S03', 'L02', 5) - 0.35, clip='onTiptoes', expr='suspicious')])],
        props=BATH + [SCALE(show=[[0.0, 100]])], cams=[cam(0.0, [SX + 4.5, 0.97, SZ - 0.05], [SX + 4.3, 0.97, SZ - 0.06], [SX, 0.95, SZ - 0.11], [SX, 0.96, SZ - 0.11], lens=44)])
st.shot('S04', 'bathroom', actors=[act('mec', ON, 0, 'onTiptoes', 'suspicious')], props=BATH + [SCALE(show=[[0.0, 100, 0]])], cams=DISPLAY(back=0.4, lens=36))
CHEEKS = lambda grow: [P(f'cheek{sd}', 'cheekPuff', on={'actor': 'mec', 'joint': 'head', 'offset': [sd * 0.09, 0.14, 0.072]}, opts={'growAt': grow, 'dur': 0.6, 'r': 0.046}) for sd in (-1, 1)]
T_BR = st.at('S05', 'L04', 1) - 0.1
st.shot('S05', 'bathroom', actors=[act('mec', ON, 0, 'stand', 'neutral', keys=[k(T_BR, clip='holdBreath', expr='angry')])],
        props=BATH + [SCALE(show=[[0.0, 100]])] + CHEEKS(T_BR + 0.1), cams=[cam(0.0, [SX + 0.36, 1.95, SZ + 1.6], [SX + 0.34, 1.95, SZ + 1.42], [SX, 1.95, SZ], [SX, 1.95, SZ], lens=44, shake=0.005)])
st.shot('S06', 'bathroom', actors=[act('mec', ON, 0, 'holdBreath', 'angry')], props=BATH + [SCALE(show=[[0.0, 100, 0]])] + CHEEKS(-1), cams=DISPLAY(back=0.34, lens=34, roll=8, dx=-0.08))
# 7-10: airplane mode; the scale takes off, out of the window
KNEEL = [SX - 0.58, 0, SZ + 0.02]
st.shot('S07', 'bathroom', actors=[act('mec', KNEEL, 90, 'kneelPress', 'suspicious')], props=BATH + [SCALE(pressAt=st.at('S07', 'L06', 4))],
        cams=[cam(0.0, [0.75, 1.0, 1.35], [0.72, 0.98, 1.22], [0.0, 0.6, SZ], [0.0, 0.58, SZ], lens=50)])
st.shot('S08', 'bathroom', actors=[act('mec', KNEEL, 90, 'kneelPress', 'suspicious')], props=BATH + [SCALE(show=[[0.12, 'plane']], pressAt=0.0)], cams=DISPLAY())
YAW_WIN = math.degrees(math.atan2(-1.0 - SX, -3.3 - SZ))   # heading from the scale to the window
Y9 = 1.05
UP9 = [SX - 0.35, 1.75, SZ - 0.55]
st.shot('S09', 'bathroom', actors=[act('mec', KNEEL, 35, 'kneel', 'suspicious', keys=[k(0.2, clip='sitFloor', expr='shocked', look=UP9)])],
        props=BATH + [SCALE(wingsAt=0.04, grow=GROW, show=[[0.0, 'plane']], bob=[0.025, 1.6, 0.6], keys=[k(0.08, to=UP9, dur=0.5, ease='out'), k(0.5, rotTo=[0, math.radians(YAW_WIN), 0], dur=0.35)])],
        cams=[cam(0.0, [1.9, 1.25, 1.6], [1.85, 1.27, 1.45], [-0.15, 1.15, -2.0], [-0.15, 1.2, -2.0], lens=44, shake=0.006)])
# 10-12: out of the window (seen from the street, against the sky); he jumps on it from the sill; they fly off down the street
BX, BY, BZ = 10.15, 6.19, -2.0          # the open window on the facade (sill top), facade facing -X
HOV = [8.5, 6.4, -2.0]                  # the scale waiting outside
BLD = [P('bld', 'haussmann', pos=[BX, 0, BZ], ry=-90, opts={'w': 12.6, 'h': 18, 'floors': 6, 'cols': 5, 'color': '#F2DCCB', 'awning': '#2F7F5C'}),
       P('ow', 'openWindow', pos=[BX - 0.015, BY, BZ], ry=-90, opts={'w': 1.2, 'h': 2.2})]
st.shot('S10', 'parisStreet', actors=[act('mec', [BX + 0.7, BY, BZ], -90, 'stand', 'surprised', keys=[k(0.42, to=[BX - 0.2, BY, BZ], dur=0.42, clip='walk', face='keep', then='stand')])],
        props=BLD + [FLY([BX + 0.7, BY + 1.0, BZ], -90, trail=0, bob=[0.015, 1.4, 0.85], keys=[k(0.0, path=[[BX - 0.45, BY + 1.0, BZ], [9.2, 6.9, BZ + 0.15], HOV], dur=0.8, ease='out')])],
        cams=[cam(0.0, [6.4, 4.9, 1.5], [6.5, 4.95, 1.35], [9.2, 6.85, BZ], [9.15, 6.85, BZ], lens=44, shake=0.006)])
st.shot('S11', 'parisStreet', actors=[act('mec', [BX - 0.2, BY, BZ], -90, 'stand', 'happy', keys=[k(0.12, to=[HOV[0], HOV[1] + TOPF, HOV[2] + 0.04], dur=0.42, clip='airborne', arc=0.5, face='keep', then='surfRide')])],
        props=BLD + [FLY(HOV, -90, trail=0, bob=[0.012, 1.4, 0.0])],
        cams=[cam(0.0, [4.7, 7.05, 1.35], [4.8, 7.0, 1.15], [9.2, 6.95, BZ], [9.15, 6.9, BZ], lens=44)])
F0, F1 = [4.0, 9.0, 1.0], [1.0, 10.0, -11.0]      # the flight down the street (1.55 s)
fy = math.degrees(math.atan2(F1[0] - F0[0], F1[2] - F0[2])); D12 = st.dur('S12')
dv, rv = [math.sin(math.radians(fy)), 0, math.cos(math.radians(fy))], [-math.cos(math.radians(fy)), 0, math.sin(math.radians(fy))]
off12 = [4.2 * dv[i] - 2.2 * rv[i] + (0.9 if i == 1 else 0) for i in range(3)]      # hero: ahead, on his left, a little above the scale
st.shot('S12', 'parisStreet', actors=[RIDE('mec', F0, F1, fy, 'surfRide', 'happy', D12)], props=[FLY(F0, fy, keys=[k(0.0, to=F1, dur=D12, ease='linear')])],
        cams=TRACK(F0, F1, off12, [0, 0.7, 0]))
# 13-14: over the gym; he waves
GYM = P('gym', 'gymBuilding', pos=[3.0, 0, -10.0], opts={'w': 26, 'd': 30, 'h': 9, 'text': 'SALLE DE SPORT'})
G0, G1 = [0.2, 12.0, 26.0], [5.2, 12.0, 26.0]; D13 = st.dur('S13')
st.shot('S13', 'aerialSuburb', actors=[RIDE('mec', G0, G1, 90, 'surfRide', 'happy', D13)], props=[GYM, FLY(G0, 90, keys=[k(0.0, to=G1, dur=D13, ease='linear')])],
        cams=TRACK(G0, G1, [0.25, -0.15, 6.6], [0.25, -0.15, -20.9]))
W0, W1 = [7.4, 12.0, 26.0], [10.6, 12.0, 26.0]; D14 = st.dur('S14')
st.shot('S14', 'aerialSuburb', actors=[RIDE('mec', W0, W1, 90, 'rideWave', 'happy', D14)], props=[GYM, FLY(W0, 90, keys=[k(0.0, to=W1, dur=D14, ease='linear')])],
        cams=TRACK(W0, W1, [5.4, 0.9, 1.8], [0, 0.4, 0]))
# 15-16: up high it reads zero (an airliner passes below him); his ideal weight
HY = 120.0
SKY = {'cloudColor': '#AFC0D2'}     # a slightly blue-grey cloud sea: the white captions keep their contrast
st.shot('S15', 'skyHigh', setOpts=SKY, actors=[act('mec', [0, HY + TOPF, -0.08], 0, 'surfRide', 'happy')],
        props=[FLY((0, HY, 0), 0, trail=0, show=[[0.0, 100], [st.at('S15', 'L11', 4) - 0.36, 0, 100]])],
        cams=[cam(0.0, [0.08, HY + 0.95, 0.75], [0.07, HY + 0.9, 0.7], [0, HY + 0.07, 0.17], [0, HY + 0.07, 0.17], lens=40)])
st.shot('S16', 'skyHigh', setOpts=SKY, actors=[act('mec', [0, HY + TOPF, -0.08], 0, 'rideCheer', 'grin')], props=[FLY((0, HY, 0), 0, show=[[0.0, 0]])],
        cams=[cam(0.0, [0.55, HY - 0.5, 1.8], [0.52, HY - 0.45, 1.65], [0, HY + 1.8, -0.05], [0, HY + 1.82, -0.05], lens=44)])
# 17-19: it lands on a cloud that reads "hors service"; he has never felt so light
CY, CT = 100.0, 1.1
CLOUD = lambda **o: P('cloud', 'serviceCloud', pos=[0, CY, 0], opts={'w': 3.6, 'top': CT, 'text': 'HORS SERVICE', 'panelY': 0.62, **o})
L0, L1 = [-2.4, CY + CT + 1.6, 1.8], [0.25, CY + CT, -0.2]; T17 = 0.55
st.shot('S17', 'skyHigh', setOpts=SKY, actors=[act('mec', [L0[0], L0[1] + TOPF, L0[2]], 125, 'surfRide', 'happy', keys=[k(0.0, to=[L1[0], L1[1] + TOPF, L1[2]], dur=T17, glide=True, face='keep', ease='out'), k(T17, clip='land', expr='surprised')])],
        props=[CLOUD(squashAt=T17, bootAt=99), FLY(L0, 125, trail=0, show=[[0.0, 0]], keys=[k(0.0, to=L1, dur=T17, ease='out')])],
        cams=[cam(0.0, [2.3, CY + 1.75, 6.6], [2.15, CY + 1.72, 6.25], [0.0, CY + 1.5, 0.0], [0.05, CY + 1.48, 0.0], lens=44, shake=0.006)])
T_HS = st.at('S18', 'L13', 7) - 0.05     # « hors service »: the panel boots on the words
st.shot('S18', 'skyHigh', setOpts=SKY, actors=[act('mec', [L1[0], L1[1] + TOPF, L1[2]], 125, 'lookDown', 'surprised')],
        props=[CLOUD(bootAt=T_HS, blinkAt=T_HS + 0.32), FLY(L1, 125, trail=0, show=[[0.0, 0]])],
        cams=[cam(0.0, [0.05, CY + 0.35, 5.5], [0.05, CY + 0.36, 5.25], [0.0, CY + 0.8, 0.0], [0.0, CY + 0.8, 0.0], lens=44)])
SEAT = [-0.42, CY + CT - 0.5, 0.92]     # post-review (round 3, both critics): end on a medium-wide tableau: him on the edge, the lit panel and the parked scale in frame
st.shot('S19', 'skyHigh', setOpts=SKY, actors=[act('mec', SEAT, 0, 'sitEdge', 'grin')],
        props=[CLOUD(blinkAt=0.0, panelX=0.55, panelY=0.75, dw=1.0), FLY([0.4, CY + CT, -0.3], 200, trail=0, show=[[0.0, 0]])],
        cams=[cam(0.0, [0.25, CY + 2.0, 6.3], [0.15, CY + 1.95, 5.3], [0.15, CY + 1.42, 0.5], [0.15, CY + 1.45, 0.5], lens=44, ease='out')])
st.card('S08', 'MODE AVION'); st.card('S16', 'POIDS IDÉAL')
st.cue('clack', 'S01', T_STEP + 0.3, 0.35); st.cue('sfx:beep', 'S02', st.at('S02', 'L01', 10) + 0.05, 0.3); st.cue('sfx:squeak', 'S03', st.at('S03', 'L02', 5) - 0.3, 0.25)
st.cue('sfx:beep', 'S04', 0.36, 0.3); st.cue('sfx:gasp', 'S05', T_BR, 0.35); st.cue('sfx:beep', 'S06', 0.36, 0.3); st.cue('thud', 'S06', 0.4, 0.3)
st.cue('sfx:click', 'S07', st.at('S07', 'L06', 4), 0.4); st.cue('pop', 'S08', 0.12, 0.35); st.cue('pop', 'S09', 0.04, 0.35); st.cue('sfx:jet', 'S09', 0.1, 0.25); st.cue('whoosh', 'S10', 0.05, 0.5)
st.cue('whoosh', 'S11', 0.12, 0.45); st.cue('thud', 'S11', 0.56, 0.4); st.cue('gust', 'S12', 0.0, 0.35); st.cue('gust', 'S13', 0.0, 0.3); st.cue('sfx:beep', 'S15', st.at('S15', 'L11', 4) + 0.02, 0.3)
st.cue('sfx:fanfare', 'S16', 0.05, 0.25); st.cue('sfx:boing', 'S17', T17, 0.45); [st.cue('sfx:beep', 'S18', 0.12 + 0.5 * i, 0.22) for i in range(3)]; st.cue('gust', 'S19', 0.2, 0.2)
st.write('La balance', {'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'shoes': True, 'build': {'width': 0.9, 'headWidth': 1.3, 'headScale': 1.0, 'belly': 0.1}}})
