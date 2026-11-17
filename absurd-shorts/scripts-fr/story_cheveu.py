#!/usr/bin/env python3
"""Le cheveu (story 88, cycle 49; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man found a hair in his soup. A police helicopter lit the soup. The hair was arrested with tweezers. Photographed from the front, then in
profile. Questioned twelve hours under the lamp. It curled; that was held against it. The dogs followed its trail to the cook. They broke down
his door. And every door in the street. The cook was bald. He was shaved anyway. Then the customers and the passers-by, for comparison. The police
dog too. This man, twice. Under the microscope: no match. The minister apologised to the hair. It was the last hair in the neighbourhood. The
helicopter put it back. In this man's soup.
Staging: at a bistro table at night (checked cloth, a big white bowl of pale golden soup, a SOUPE DU JOUR chalkboard, a window on the night behind
him) a thick black hair floats waving on the soup; he points at it, eyes down, then looks at us. Low from the table: through the window above his
head a navy police helicopter hovers and its searchlight cone drops onto the bowl, the soup flaring in a pool of light, he squints up. A gloved
policeman lifts the hair out with giant steel tweezers (it hangs, blinking) while his colleague holds an open evidence bag. Mugshot: the hair
stands on a little ledge against a pale height chart, a tiny number board hung on it; flash; it turns a quarter; flash; it looks exactly the same
(FICHÉ). In the interrogation room it stands alone on a pale metal chair under a big lamp bent down at it, an inspector leaning on the table, the
wall clock spinning. The lamp glows hot: the hair coils into a tight curl with a boing, sweating (FRISÉ); the inspector slams a stamp on its file:
RETENU. Two sniffer dogs drag their leaning handlers up the pavement toward us, then stop at the cook's feet on his doorstep, key in hand. From
inside his hallway at floor level his front door falls flat toward us, dust, masked officers with a ram in the doorway. Down the street every
front door falls inward one after the other as the ram team sprints along the pavement. The cook lifts his toque: bald, shining under an officer's
torch (CHAUVE). Tight on his head: clippers buzz across the bare scalp, nothing falls, a glint. On the pavement outside the restaurant a row of
customers and passers-by sit bald on chairs while officers buzz over their heads, piles of hair in their old colours growing at their feet, each
with a numbered evidence tag. The police dog sits shaved pink and smooth beside its handler, at attention, tongue out, its own tagged pile beside
it. He, bald, sits in the barber chair: the clippers pass, pause, pass again. In a pale lab a scientist peers into a microscope before shelves of
numbered hair bags; on the screen the two samples, a scan line, then a big red cross. In the press room the minister bows deeply to the hair
standing on a little red-cushioned stand beside the podium, flashes popping. Crane down over a square of shining bald heads (and the pink dog)
round the hair alone on its stand, which looks up at us. Night: the helicopter lowers the hair on its winch cable through the window toward the
bowl, searchlight on, he looks up, bald. The framing of the first shot: he, bald, before the same bowl; the hair drops onto the soup, a ripple,
it floats and opens two little eyes at him; he looks at us.
Natural look; cycle 49: props_cheveu.js (chvHair, chvBowl, chvTable, chvRoom, chvTweezers, chvMugWall, chvLamp, chvFile, chvRam, chvDoorWall,
chvHall, chvClippers, chvHairPile, chvShine, chvMicroscope, chvBagShelf, chvScreen, chvStand, chvPool, chvBeam); helicopter (props_lunettes),
voxelDog, chair, table, evidenceBag, wallClock (props.js), tableStamp, tacLight (props_table), balaclava (props_rambarde), shopFront (props_news),
flashBursts (props_moustache), bigKey (props_moustache) reused; tethers for the leashes and the winch cable.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.86) and heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() before stills; the
hair (black) always against a pale ground (cream soup, pale chart, pale chair back, light press backdrop, white stand panel); thin cords as
tethers with minPx; nobody hurt (shaving only, the ram hits doors, the dog fine and pleased); no English on screen, no brands, no real insignia
or organisation, no flags; flashes at most three a second."""
from story_kit import *
import math

st = Story('cheveu', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def lerp(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))

def FC(sid, t, frm, pts, top=0.08, bottom=0.74, lenses=range(30, 61), drift=(0.0, 0.0, -0.12), margin=0.06):
    """a camera at frm aimed and sized by fit() on the named points (between top and bottom of the height), drifting a little (drift)"""
    look, lens, _ = fit(frm, pts, margin=margin, top=top, bottom=bottom, lenses=lenses)
    if lens is None: print(f'  FC {sid}: WARNING no lens fits'); lens = max(lenses)
    to = [r(frm[i] + drift[i]) for i in range(3)]; chk(sid, frm, look, lens, pts)
    return cam(t, frm, to, look, look, lens)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]
def R5(p, w=1, s=0.04): return [*p, w, s]
def aim_rot(src, dst):
    """rot for a prop whose -Y must point from src to dst (the beam): (rx, ry deg, rz)"""
    Y = unit3([src[i] - dst[i] for i in range(3)]); X = unit3(cross3(Y, [0, 0, 1])) if abs(Y[2]) < 0.95 else unit3(cross3(Y, [1, 0, 0])); Z = cross3(X, Y)
    return axes_euler(X, Y, Z)
def BALD(pid, who, s=1.0, tw=(), tw0=0.35): return P(pid, 'chvShine', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.03]}, opts={'s': s, 'twinkle': list(tw), 'tw0': tw0})

# ============================== the bistro at night: a dark void outside, the room (back wall z -1.5, the window above his head), the table
NIGHT = {'color': '#1A2442'}
WIN = [0.75, 2.3, 1.4, 1.1]
TBL = [0.0, 0, 0.0]; TH = 0.76
BOWL = [0.0, TH, -0.2]; SOUP_Y = r(TH + 0.2 * 0.55 * 0.82 + 0.005)
HAIR1 = [0.0, SOUP_Y, -0.19]
HERO = [0.0, 0.03, -0.8]                               # seated (clip sit) behind the table, facing +Z
HEAD_S = [0.0, 1.72, -0.78]                            # his eyes, seated
ROOM = lambda: [P('salle', 'chvRoom', pos=[0, 0, 0], opts={'win': WIN, 'boardX': -1.55, 'picX': 2.6, 'sconces': [-0.55, 2.0]}),
                P('table', 'chvTable', pos=TBL, opts={'r': 0.5, 'h': TH, 'drop': 0.15}), P('chaise', 'chair', pos=[0.0, 0, -0.95], opts={'color': '#7A4A2A'}),
                P('bol', 'chvBowl', pos=BOWL, opts={'steam': True})]
HAIRF = {'L': 0.3, 'r': 0.0095, 'wig': 0.07}           # the floating hair
SIT = lambda face, reach=None, hands=None: {'face': face, **({'reach': reach} if reach else {}), **({'hands': hands} if hands else {})}

# 1: the hook. Low over the bowl: the thick black hair floating and waving on the pale soup in the foreground, he behind it, seated; he points
#    at it, eyes down on it, then looks up at us, deadpan
D1 = st.dur('S01')
PT1 = R5([0.06, 1.05, -0.32], 1, 0.12)
C1 = FC('S01', 0.0, [0.1, 1.08, 0.9], {'headTop': [0, 1.98, -0.8], 'hairL': add(HAIR1, [-0.16, 0, 0.05]), 'hairR': add(HAIR1, [0.16, 0, 0.05]), 'bowlFront': [0, TH + 0.05, 0.0], 'finger': PT1[:3]}, top=0.06, bottom=0.76, drift=(0, 0, -0.08))
st.shot('S01', 'whiteVoid', setOpts=NIGHT, actors=[
        act('mec', HERO, 0, 'sit', 'neutral', keys=[k(0.0, look=add(HAIR1, [0, 0.05, 0])),
            k(0.0, toon=SIT({'lid': 0.3, 'mouth': 'line', 'gy': 0.6}), toonDur=0.0),
            k(0.35, toon=SIT({'lid': 0.15, 'mouth': 'O', 'gy': 0.8, 'brow': 0.4}, {'R': PT1}, {'R': 'point'}), toonDur=0.2, toonEase='out'),
            *[k(r(0.6 + 0.14 * i), toon=SIT({'lid': 0.15, 'mouth': 'O', 'gy': 0.8, 'brow': 0.4}, {'R': R5(add(PT1[:3], [0.015 * (i % 2), 0.01 * (i % 2), 0]), 1, 0.12)}, {'R': 'point'}), toonDur=0.12) for i in range(4)],
            k(1.25, look='camera', lookDur=0.12), k(1.25, toon=SIT({'lid': 0.45, 'mouth': 'line', 'brow': -0.1}, {'R': PT1}, {'R': 'point'}), toonDur=0.12),
            *blink(1.75, {'lid': 0.45, 'mouth': 'line', 'brow': -0.1})])],
        props=[*ROOM(), P('cheveu1', 'chvHair', pos=HAIR1, ry=12, opts=HAIRF)],
        cams=[C1])
st.cue('sfx:clink', 'S01', 0.1, 0.2); st.cue('sfx:tense', 'S01', 0.45, 0.15)

# ============================== the helicopter outside the window: its searchlight runs from its nose through the window onto the bowl
HELI = [1.8, 4.0, -4.3]; HRY = yaw(HELI, BOWL)
LAMP = add(HELI, [r(0.5 * math.sin(math.radians(HRY)) * 1.6), -0.45, r(0.5 * math.cos(math.radians(HRY)) * 1.6)])
BR = aim_rot(LAMP, add(BOWL, [0, 0.09, 0])); BLEN = r(math.dist(LAMP, BOWL) + 0.2)
HELIP = lambda pid, on=None: [P(pid, 'helicopter', pos=HELI, ry=HRY, rot=[0.12, 0, 0], scale=0.5, opts={'color': '#DCE2EA', 'spin': 6, 'beam': False, 'bladeOpacity': 0.55}),
                              P(pid + 'b', 'chvBeam', pos=LAMP, ry=BR[1], rot=[BR[0], 0, BR[2]], opts={'len': BLEN, 'r': 0.42, 'on': on or [[0, 1]]})]

# 2: a police helicopter lit the soup. Low from the table, looking up: his face, and above his head through the window the navy helicopter
#    hovering, its searchlight sweeping down through the window and locking on the bowl, which flares in a pool of light; he squints up
D2 = st.dur('S02'); LOCK2 = 1.0
C2 = FC('S02', 0.0, [0.12, 0.85, 1.55], {'bowl': add(BOWL, [-0.1, 0.1, 0.1]), 'headTop': [0, 1.98, -0.8], 'heliTop': add(HELI, [0, 0.9, 0]), 'heliTail': add(HELI, [1.2, 0.3, -1.6]), 'eyesL': [-0.15, 1.72, -0.8]}, top=0.04, bottom=0.75, lenses=range(30, 70), drift=(0, 0, -0.1))
st.shot('S02', 'whiteVoid', setOpts=NIGHT, look={'sun': 0.35, 'fill': 0.6, 'exposure': 1.05}, actors=[
        act('mec', HERO, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon=SIT({'lid': 0.4, 'mouth': 'line', 'gy': -0.6}), toonDur=0.0),
            k(LOCK2, toon=SIT({'lid': 0.65, 'mouth': 'clench', 'gy': -0.9, 'brow': -0.5}, {'L': R5(off(HERO, 0, 0.25, -0.05, 1.86), 1, 0.06)}, {'L': 'open'}), toonDur=0.14, toonEase='out'),
            k(r(LOCK2 + 0.6), toon=SIT({'lid': 0.7, 'mouth': 'clench', 'gy': -0.9, 'brow': -0.5}, {'L': R5(off(HERO, 0, 0.27, -0.03, 1.88), 1, 0.06)}, {'L': 'open'}), toonDur=0.3)])],
        props=[*ROOM(), P('cheveu2', 'chvHair', pos=HAIR1, ry=12, opts={**HAIRF, 'waveF': 3.2}), *HELIP('heli2', [[0, 1]]),
               P('pool2', 'chvPool', pos=add(BOWL, [0, 0.01, 0]), opts={'r': 0.5, 'h': 0.7, 'power': 4, 'on': [[0, 0.25], [LOCK2, 1]]})],
        cams=[C2])
st.cue('engine', 'S02', 0.0, 0.3, D2); st.cue('sfx:rotor', 'S02', 0.0, 0.35); st.cue('clack', 'S02', LOCK2, 0.3)

# 3: the hair was arrested with tweezers. Across the table: a gloved policeman lifts the hair out of the soup with giant steel tweezers, held
#    at arm's length, the hair hanging and blinking; his colleague at the right holds an open evidence bag; he, seated behind, watches
D3 = st.dur('S03'); PICK3 = 0.55
COP3 = [-0.78, 0, -0.3]; RYC3 = 40; COP3b = [0.8, 0, -0.25]; RYB3 = -40
TW0 = [r(HAIR1[0] - 0.02), r(SOUP_Y + 0.65), HAIR1[2]]            # the tweezers' hinge with the tips at the hair
TW1 = [-0.62, 2.12, -0.1]; TW2 = [-0.1, 2.15, 0.1]
BAG3 = [0.52, 1.35, 0.0]
C3 = FC('S03', 0.0, [0.0, 1.45, 2.9], {'copTop': [COP3[0], 2.4, COP3[2]], 'cop2Top': [COP3b[0], 2.4, COP3b[2]], 'tw1top': add(TW1, [0, 0.05, 0]), 'bowl': add(BOWL, [0, 0.0, 0.35])}, top=0.05, bottom=0.78, lenses=range(30, 66), margin=0.03)
GRIP = lambda p: R5(add(p, [0.0, -0.24, 0.0]), 1, 0.06)
st.shot('S03', 'whiteVoid', setOpts=NIGHT, actors=[
        act('flic1', COP3, RYC3, 'stand', 'neutral', keys=[k(0.0, look=add(TW0, [0, -0.45, 0])),
            k(0.0, toon={'reach': {'R': GRIP(TW0)}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
            k(PICK3, toon={'reach': {'R': GRIP(TW1)}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.0, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.45, toonEase='inOut'),
            k(r(PICK3 + 0.15), look=add(TW1, [0, -0.6, 0]), lookDur=0.2),
            k(1.35, toon={'reach': {'R': GRIP(TW2)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.35, toonEase='inOut'), k(1.6, look='camera', lookDur=0.15)]),
        act('flic2', COP3b, RYB3, 'stand', 'neutral', keys=[k(0.0, look=add(TW1, [0, -0.6, 0])),
            k(0.0, toon={'reach': {'R': R5(add(BAG3, [-0.12, 0.14, 0.02])), 'L': R5(add(BAG3, [0.12, 0.14, 0.02]))}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.1}}, toonDur=0.0),
            *blink(1.1, {'lid': 0.4, 'mouth': 'line', 'brow': 0.1})]),
        act('mec', HERO, 0, 'sit', 'neutral', keys=[k(0.0, look=add(HAIR1, [0, 0.1, 0])), k(0.0, toon=SIT({'lid': 0.4, 'mouth': 'line'}), toonDur=0.0), k(r(PICK3 + 0.2), look=add(TW1, [0, -0.6, 0]), lookDur=0.3)])],
        props=[*ROOM(), P('cheveu3', 'chvHair', pos=HAIR1, ry=12, opts=HAIRF, keys=[k(PICK3 - 0.02, visible=False)]),
               P('pince3', 'chvTweezers', pos=TW0, scale=1.35, opts={'hairAt': PICK3 - 0.02, 'eyes': True, 'blinks': [1.2, 1.75], 'open': [[0, 0.2], [r(PICK3 - 0.1), 0.02]], 'swing': 0.5},
                 keys=[k(PICK3, to=TW1, dur=0.45, ease='inOut'), k(1.35, to=TW2, dur=0.35, ease='inOut')]),
               P('sachet3', 'evidenceBag', pos=BAG3, ry=-10, scale=2.2)],
        cams=[C3])
st.cue('sfx:squeak', 'S03', PICK3, 0.3); st.cue('sfx:slideUp', 'S03', r(PICK3 + 0.05), 0.2)

# 4: photographed from the front, then in profile. Locked frontal camera: the hair stands on the pale chart's ledge holding its tiny number
#    board; flash; a quarter turn; flash; it looks exactly the same (FICHÉ)
D4 = st.dur('S04'); FL4a, TURN4, FL4b = 0.42, 1.12, 1.55
HAIR4 = [0.0, 0.03, 0.0]
C4 = cam(0.0, [0.0, 0.2, 1.0], [0.0, 0.2, 0.97], [0.0, 0.165, 0.0], [0.0, 0.165, 0.0], lens=36)
chk('S04', C4['from'], C4['lookAt'], 36, {'hairTop': [0, 0.36, 0], 'eyes': [0, 0.33, 0.01], 'board': [0, 0.13, 0.02], 'hairFoot': HAIR4, 'wallTop': [0, 0.62, -0.01], 'wallL': [-0.4, 0.3, 0]})
st.shot('S04', 'whiteVoid', setOpts={'color': '#B9C2CC'}, actors=[],
        props=[P('toise4', 'chvMugWall', pos=[0, 0, -0.03]),
               P('cheveu4', 'chvHair', pos=HAIR4, opts={'L': 0.3, 'r': 0.0105, 'wig': 0.04, 'waveF': 1.4, 'stand': [[0, 1]], 'stand0': 1, 'eyes': True, 'brows': True, 'board': ['N° 0088', '17.11'], 'boardU': 0.62,
                                                     'yaw': [[TURN4, 90]], 'boardYaw': [[TURN4, -70]], 'blinks': [r(FL4a + 0.12), r(FL4b + 0.12)], 'gaze': [[0, 0, 0], [0.9, 0.6, 0], [1.05, 0, 0]], 'brow': [[0, 0.0], [r(FL4a + 0.1), -0.5]]})],
        cams=[C4], fx=[{'type': 'flash', 'at': FL4a, 'dur': 0.12}, {'type': 'flash', 'at': FL4b, 'dur': 0.12}])
st.card('S04', 'FICHÉ', at=r(FL4a + 0.25))
st.cue('sfx:shutter', 'S04', FL4a, 0.5); st.cue('sfx:squeak', 'S04', TURN4, 0.15); st.cue('sfx:shutter', 'S04', FL4b, 0.5)

# ============================== the interrogation room (grey walls): the hair on a pale metal chair beside the table, the lamp clamped at the
# table's corner bent down over it, the inspector leaning on the table, the clock on the back wall
CH5 = [1.4, 0, 0.2]; SEAT = 0.48
HAIR5 = [CH5[0], SEAT + 0.005, CH5[2] + 0.02]
LAMP5 = [0.66, 0.785, -0.42]
INSP = [-0.25, 0, -1.45]; RYI = 30
CLOCK = [1.8, 2.5, -3.12]   # over the set's own (still) clock
HAIR5O = {'L': 0.38, 'r': 0.013, 'eyeS': 1.25, 'wig': 0.04, 'waveF': 1.6, 'stand': [[0, 1]], 'stand0': 1, 'eyes': True, 'brows': True}
INTERRO = lambda heat=None: [P('chaise5', 'chair', pos=CH5, ry=-25, opts={'color': '#D9DEE3'}), P('lampe5', 'chvLamp', pos=LAMP5, ry=yaw(LAMP5, CH5), opts={'h': 0.55, 'reach': 0.86, 'tilt': 0.35, 'beamLen': 0.75, 'power': 3.5, 'heat': heat or []}),
                             P('horloge5', 'wallClock', pos=CLOCK, scale=1.04, opts={'rate': 3.0})]

# 5: questioned twelve hours under the lamp. Low, slow push-in: the hair alone on the pale chair under the bent lamp, the inspector leaning on
#    the table at the left, the clock spinning on the wall behind
D5 = st.dur('S05')
C5 = FC('S05', 0.0, [2.1, 0.95, 1.35], {'hairTop': add(HAIR5, [0, 0.45, 0]), 'hairFoot': add(HAIR5, [0, -0.05, 0]), 'inspTop': [INSP[0], 2.35, INSP[2]], 'inspL': [INSP[0] - 0.3, 1.6, INSP[2]]}, top=0.05, bottom=0.74, lenses=range(30, 66), drift=(-0.05, -0.02, -0.35))
PALMS = lambda: {'R': R5([INSP[0] + 0.25, 0.8, -0.95]), 'L': R5([INSP[0] - 0.2, 0.8, -1.0])}
st.shot('S05', 'interrogation', actors=[
        act('inspecteur', INSP, RYI, 'stand', 'suspicious', keys=[k(0.0, look=add(HAIR5, [0, 0.3, 0])),
            k(0.0, toon={'reach': PALMS(), 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.0),
            k(0.7, toon={'reach': PALMS(), 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.58, 0, 0, 1, None]}, 'face': {'lid': 0.65, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.4, toonEase='inOut'),
            *blink(1.45, {'lid': 0.65, 'mouth': 'clench', 'brow': -0.8})])],
        props=[*INTERRO([[0, 0.15]]), P('cheveu5', 'chvHair', pos=HAIR5, ry=-25, opts={**HAIR5O, 'blinks': [0.55, 1.5], 'gaze': [[0, -0.6, 0], [0.8, 0.0, -0.7], [1.2, -0.6, 0]], 'brow': [[0, -0.6]]})],
        cams=[C5])
st.cue('sfx:ticks', 'S05', 0.0, 0.25); st.cue('sfx:static', 'S05', 0.2, 0.08)

# 6: it curled; that was held against it. Close on the hair under the lamp gone hot orange: it coils into a tight curl with a boing, sweating
#    (FRISÉ); cut on the table: the inspector slams the stamp on its open file, RETENU
D6 = st.dur('S06'); CURL6 = 0.18; CUT6 = 1.05; STAMP6 = 1.48
FILE6 = [-0.15, 0.79, -0.7]
STAMPUP = add(FILE6, [0.04, 0.62, 0.02]); STAMPDN = add(FILE6, [0.04, 0.4, 0.02])
C6b = cam(CUT6, [-0.15, 1.75, 0.15], [-0.15, 1.72, 0.1], [-0.15, 0.8, -0.72], [-0.15, 0.8, -0.72], lens=50)
C6a = FC('S06a', 0.0, [1.25, 0.98, 1.2], {'hairTop': add(HAIR5, [0, 0.46, 0]), 'hairFoot': add(HAIR5, [0, -0.04, 0]), 'side': add(HAIR5, [0.2, 0.2, 0]), 'side2': add(HAIR5, [-0.2, 0.2, 0])}, top=0.22, bottom=0.72, lenses=range(24, 50), drift=(0.02, 0, -0.08))
chk('S06b', C6b['from'], C6b['lookAt'], 50, {'file': FILE6, 'stampUp': STAMPUP, 'inspFace': [INSP[0], 2.05, INSP[2]], 'fileL': add(FILE6, [-0.3, 0, 0])})
KNOB = lambda p: R5(add(p, [0.0, 0.0, 0.0]), 1, 0.06)
st.shot('S06', 'interrogation', actors=[
        act('inspecteur', INSP, RYI, 'stand', 'suspicious', keys=[k(0.0, look=add(HAIR5, [0, 0.3, 0])),
            k(0.0, toon={'reach': {'R': KNOB(STAMPUP), 'L': R5([INSP[0] - 0.2, 0.8, -1.0])}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [0.4, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.0),
            k(r(CUT6 - 0.1), look=FILE6, lookDur=0.15),
            k(r(STAMP6 - 0.2), toon={'reach': {'R': KNOB(add(STAMPUP, [0, 0.1, 0])), 'L': R5([INSP[0] - 0.2, 0.8, -1.0])}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.4, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.14),
            k(STAMP6, toon={'reach': {'R': KNOB(STAMPDN), 'L': R5([INSP[0] - 0.2, 0.8, -1.0])}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [0.55, 0, 0, 1, None]}, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.8}}, toonDur=0.05, toonEase='in'),
            k(r(STAMP6 + 0.3), look='camera', lookDur=0.15)])],
        props=[*INTERRO([[0, 0.3], [0.05, 1.0]]), P('dossier6', 'chvFile', pos=FILE6, ry=0, opts={'stampAt': r(STAMP6 + 0.02), 'stamp': 'RETENU'}),
               P('tampon6', 'tableStamp', pos=STAMPUP, opts={'squash': [[STAMP6, 1], [r(STAMP6 + 0.1), 0]]}, keys=[k(r(STAMP6 - 0.2), to=add(STAMPUP, [0, 0.1, 0]), dur=0.14), k(STAMP6, to=STAMPDN, dur=0.05, ease='in'), k(r(STAMP6 + 0.25), to=STAMPUP, dur=0.2)]),
               P('cheveu6', 'chvHair', pos=HAIR5, ry=-25, opts={**HAIR5O, 'curl': [[CURL6, 1]], 'curlDur': 0.3, 'hop': [[CURL6, 1], [r(CURL6 + 0.18), 0]], 'sweat': [0.45, 0.85], 'blinks': [0.75], 'gaze': [[0, 0, -0.8], [0.6, -0.7, 0]], 'brow': [[0, -0.9]]})],
        cams=[C6a, C6b])
st.card('S06', 'FRISÉ', at=0.52)
st.cue('sfx:boing', 'S06', CURL6, 0.45); st.cue('sfx:spring', 'S06', r(CURL6 + 0.05), 0.25); st.cue('thud', 'S06', STAMP6, 0.6)

# ============================== the street (parisStreet): the road along Z (x -5..5), the right pavement x 5..10; the cook's house front at x 8.6
STREET = {'clouds': 0, 'clear': [-30.0, 12.0], 'clearL': [-30.0, 12.0]}
DOGF = {'color': '#3A3530', 'muzzle': '#1E1A18', 'walk': True, 'tongue': True}
# 7: the dogs followed its trail to the cook. Low ahead of them, dollying back: two sniffer dogs pull their leaning handlers up the pavement
#    toward us; cut: they stop at the feet of the cook on his doorstep (white jacket, toque, his key in hand), sniffing up at him
D7 = st.dur('S07'); CUT7 = 1.25
DA0, DA1 = [6.6, 0, -4.6], [6.6, 0, -1.0]; DB0, DB1 = [7.4, 0, -4.1], [7.4, 0, -0.5]
H7a0, H7a1 = [6.45, 0, -5.9], [6.45, 0, -2.3]; H7b0, H7b1 = [7.55, 0, -5.4], [7.55, 0, -1.8]
C7a = cam(0.0, [7.0, 0.8, 1.6], [7.0, 0.85, 2.6], [7.0, 1.05, -3.5], [7.0, 1.05, -2.0], lens=48)
COOK = [7.95, 0, -12.0]; RYK = -90                     # on his doorstep, facing the street (-X)
DOGc1, DOGc2 = [7.25, 0, -11.55], [7.3, 0, -12.5]
chk('S07a', C7a['from'], C7a['lookAt'], 48, {'dogA1': add(DA1, [0, 0.6, 0]), 'dogB0': add(DB0, [0, 0.6, 0]), 'handA1': [H7a1[0], 2.0, H7a1[2]], 'handB0': [H7b0[0], 2.0, H7b0[2]]})
C7b = FC('S07b', CUT7, [5.0, 1.15, -11.0], {'cookTop': [COOK[0], 2.42, COOK[2]], 'dog1': add(DOGc1, [-0.3, 0.75, 0.2]), 'dog2': add(DOGc2, [-0.3, 0.75, -0.2]), 'dogFeet': add(DOGc2, [0, 0.05, 0])}, top=0.06, bottom=0.78, lenses=range(30, 66), drift=(0.08, 0, -0.05))
LEAN = lambda p: {'reach': {'R': R5(off(p, 0, 0.6, 0.15, 1.05)), 'L': R5(off(p, 0, 0.55, -0.15, 1.0))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [-0.35, 0, 0, 1, None]}}
def LEASH(hid, dog, frm=None, until=None):
    d = {'a': {'actor': hid, 'hand': 'R'}, 'b': {'prop': dog, 'offset': [0, 0.53, 0.3]}, 'color': '#C0392B', 'sag': 0.04, 'radius': 0.014, 'minPx': 4}
    if frm is not None: d['from'] = frm
    if until is not None: d['until'] = until
    return d
KEYOPT = {'len': 0.2}
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('maitre1', H7a0, 0, 'walk', 'scared', keys=[k(0.0, to=H7a1, dur=CUT7, clip='walk', ease='linear', cruise=True), k(0.0, look='camera'), k(0.0, toon={**LEAN(H7a0), 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.0),
            *[k(r(0.2 * i), toon={**LEAN(lerp(H7a0, H7a1, 0.2 * i / CUT7)), 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.2, toonEase='linear') for i in range(1, 7)], k(CUT7, visible=False)]),
        act('maitre2', H7b0, 0, 'walk', 'surprised', keys=[k(0.0, to=H7b1, dur=CUT7, clip='walk', ease='linear', cruise=True), k(0.0, look='camera'), k(0.0, toon={**LEAN(H7b0), 'face': {'lid': 0.0, 'mouth': 'wavy', 'brow': 0.8}}, toonDur=0.0),
            *[k(r(0.2 * i), toon={**LEAN(lerp(H7b0, H7b1, 0.2 * i / CUT7)), 'face': {'lid': 0.0, 'mouth': 'wavy', 'brow': 0.8}}, toonDur=0.2, toonEase='linear') for i in range(1, 7)], k(CUT7, visible=False)]),
        act('cuisinier', COOK, RYK, 'stand', 'neutral', keys=[k(0.0, look=add(DOGc1, [0, 0.5, 0])), k(0.0, toon={'reach': {'R': R5(off(COOK, RYK, 0.38, 0.15, 1.25))}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
            k(r(CUT7 + 0.55), look='camera', lookDur=0.2), *blink(r(CUT7 + 0.85), {'lid': 0.35, 'mouth': 'line', 'brow': 0.2})]),
        act('maitre3', [6.3, 0, -10.9], -120, 'stand', 'neutral', keys=[k(0.0, look=add(DOGc1, [0, 0.5, 0])), k(0.0, toon={'reach': {'R': R5([6.75, 1.0, -11.2])}, 'hands': {'R': 'grip'}, 'bend': {'spine': [-0.2, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'O', 'brow': 0.5}}, toonDur=0.0)])],
        props=[P('chien7a', 'voxelDog', pos=DA0, opts=DOGF, keys=[k(0.0, to=DA1, dur=CUT7, ease='linear'), k(CUT7, visible=False)]),
               P('chien7b', 'voxelDog', pos=DB0, opts=DOGF, keys=[k(0.0, to=DB1, dur=CUT7, ease='linear'), k(CUT7, visible=False)]),
               P('chien7c', 'voxelDog', pos=DOGc1, ry=60, opts={**DOGF, 'walk': False}, keys=[k(0.0, visible=False), k(CUT7, visible=True), k(r(CUT7 + 0.2), rotTo=[0.25, 1.05, 0], dur=0.1), k(r(CUT7 + 0.45), rotTo=[-0.05, 1.05, 0], dur=0.1), k(r(CUT7 + 0.7), rotTo=[0.25, 1.05, 0], dur=0.1)]),
               P('chien7d', 'voxelDog', pos=DOGc2, ry=80, opts={**DOGF, 'walk': False}, keys=[k(0.0, visible=False), k(CUT7, visible=True), k(r(CUT7 + 0.3), rotTo=[0.3, 1.4, 0], dur=0.1), k(r(CUT7 + 0.6), rotTo=[0.0, 1.4, 0], dur=0.1)]),
               P('maison7', 'chvDoorWall', pos=[8.6, 0, -12.0], ry=-90, opts={'facade': True, 'w': 3.4, 'num': 12, 'color': '#E7D2B0', 'door': '#2F5D8A'}),
               P('cle7', 'bigKey', on={'actor': 'cuisinier', 'hand': 'R', 'face': 'camera'}, opts=KEYOPT)],
        cams=[C7a, C7b],
        tethers=[LEASH('maitre1', 'chien7a', until=CUT7), LEASH('maitre2', 'chien7b', until=CUT7), {**LEASH('maitre3', 'chien7c', frm=CUT7), 'a': {'point': [6.75, 1.0, -11.2]}}])
st.cue('sfx:stepRun', 'S07', 0.1, 0.25); st.cue('sfx:sniff', 'S07', 0.4, 0.3); st.cue('sfx:sniff', 'S07', 0.8, 0.3); st.cue('sfx:sniff', 'S07', r(CUT7 + 0.2), 0.35); st.cue('sfx:sniff', 'S07', r(CUT7 + 0.5), 0.3)

# 8: they broke down his door. Inside his hallway, at floor level: the front door falls flat toward us in a puff of dust; in the bright doorway
#    two masked officers hold the ram, a third behind
D8 = st.dur('S08'); HIT8 = 0.32
RAM8a, RAM8b = [0.0, 1.05, -1.05], [0.0, 1.05, -0.62]
SW1, SW2 = [-0.32, 0, -0.95], [0.32, 0, -1.35]
C8 = cam(0.0, [0.28, 0.28, 3.7], [0.26, 0.28, 3.55], [0.0, 1.15, -0.6], [0.0, 1.15, -0.6], lens=46)
chk('S08', C8['from'], C8['lookAt'], 46, {'doorTop': [0, 2.15, 0.05], 'doorFlat': [0, 0.06, 2.1], 'sw1Face': [SW1[0], 2.05, SW1[2]], 'sw2Face': [SW2[0], 2.05, SW2[2]], 'ram': RAM8b, 'ceil': [0, 2.9, 2.0]})
def RAMHANDS(ram, side):
    g = [[0, 0.21, -0.28], [0, 0.21, 0.22]]
    return {'R': R5(add(ram, [side * 0.06, g[0][1], g[0][2]])), 'L': R5(add(ram, [side * 0.06, g[1][1], g[1][2]]))}
MASKED = lambda who: [P(f'cagoule_{who}', 'balaclava', on={'actor': who, 'joint': 'head', 'offset': [0, 0, 0]}), P(f'casque_{who}', 'tacHelmet', on={'actor': who, 'joint': 'head', 'offset': [0, 0.47, 0]})]
st.shot('S08', 'whiteVoid', setOpts={'color': '#E4ECF2'}, actors=[
        act('swat1', SW1, 0, 'stand', 'angry', keys=[k(0.0, look=[0, 1.2, 1.5]), k(0.0, toon={'reach': RAMHANDS(RAM8a, 1), 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.0),
            k(r(HIT8 - 0.12), toon={'reach': RAMHANDS(RAM8b, 1), 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}}, toonDur=0.12, toonEase='in'), k(r(HIT8 + 0.6), look='camera', lookDur=0.2)]),
        act('swat2', SW2, 0, 'stand', 'angry', keys=[k(0.0, look=[0, 1.2, 1.5]), k(0.0, toon={'reach': RAMHANDS(RAM8a, -1), 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.0),
            k(r(HIT8 - 0.12), toon={'reach': RAMHANDS(RAM8b, -1), 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}}, toonDur=0.12, toonEase='in'), *blink(1.1, {'lid': 0.3, 'mouth': 'line'})]),
        act('swat3', [0.75, 0, -2.4], -20, 'stand', 'neutral', keys=[k(0.0, look=[0, 1.2, 1.5])])],
        props=[P('couloir8', 'chvHall', pos=[0, 0, 0]), P('porte8', 'chvDoorWall', pos=[0, 0, 0], opts={'w': 1.9, 'h': 2.95, 'dir': 1, 'fallAt': HIT8, 'num': 12, 'color': '#D6C3A0', 'trim': '#F2EEE4'}),
               P('belier8', 'chvRam', pos=RAM8a, keys=[k(r(HIT8 - 0.12), to=RAM8b, dur=0.12, ease='in')]), *MASKED('swat1'), *MASKED('swat2'), *MASKED('swat3')],
        cams=[C8], fx=[{'type': 'shake', 'at': HIT8, 'dur': 0.2, 'amount': 0.02}])
st.cue('thud', 'S08', HIT8, 0.7); st.cue('sfx:crunch', 'S08', HIT8, 0.35); st.cue('thud', 'S08', r(HIT8 + 0.24), 0.6); st.cue('sfx:poof', 'S08', r(HIT8 + 0.26), 0.3)

# 9: and every door in the street. From the road, down the row of house fronts: the ram team sprints toward us along the pavement and each front
#    door falls inward as they pass, one after the other, a black doorway opening each time
D9 = st.dur('S09')
HZ = [-3.0, -5.6, -8.2, -10.8, -13.4, -16.0]
RUN0, RUN1 = -13.5, -5.2; SPD9 = (RUN1 - RUN0) / D9
FALL9 = lambda z: r((z - RUN0) / SPD9 - 0.05)
C9 = cam(0.0, [4.6, 1.55, 3.2], [4.7, 1.55, 3.0], [7.4, 1.5, -8.5], [7.4, 1.5, -8.0], lens=44)
chk('S09', C9['from'], C9['lookAt'], 44, {'door0': [8.5, 1.1, HZ[0]], 'door3': [8.5, 1.1, HZ[3]], 'door5': [8.5, 1.1, HZ[5]], 'run0': [7.2, 2.0, RUN0], 'run1': [7.2, 2.0, RUN1], 'roof0': [8.6, 6.0, HZ[0]]})
RUNNERS = [('swat1', 6.85, 0.0), ('swat2', 7.55, -0.9), ('swat3', 7.2, -2.0)]
def RAMAT(t): return [7.2, 1.05, r(RUN0 + SPD9 * t + 0.45)]
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        *[act(w, [x, 0, r(RUN0 + dz)], 0, 'run', 'angry', keys=[k(0.0, to=[x, 0, r(RUN1 + dz)], dur=D9, clip='run', ease='linear', cruise=True), k(0.0, look=[x, 1.8, 10]),
            *([k(r(0.15 * i), toon={'reach': {'R' if w == 'swat1' else 'L': R5(add(RAMAT(0.15 * i), [(-0.18 if w == 'swat1' else 0.18), 0.12, -0.05 if w == 'swat1' else 0.35]))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'autoSq': 0.3}, toonDur=0.15, toonEase='linear') for i in range(int(D9 / 0.15) + 1)] if w != 'swat3' else [])]) for w, x, dz in RUNNERS]],
        props=[*[P(f'maison9{i}', 'chvDoorWall', pos=[8.6, 0, z], ry=-90, opts={'facade': True, 'w': 2.6, 'dir': -1, 'dark': True, 'fallAt': FALL9(z), 'num': 2 + 2 * i, 'color': ['#E7D2B0', '#D9B8A0', '#CFD8C6', '#E4C9A8', '#C9D2DE', '#E8D9B8'][i], 'door': ['#2F5D8A', '#8A2E2E', '#2E6B4A', '#5A3E8A', '#B06A2A', '#2F5D8A'][i]}) for i, z in enumerate(HZ)],
               P('belier9', 'chvRam', pos=RAMAT(0), keys=[k(0.0, to=RAMAT(D9), dur=D9, ease='linear')]), *MASKED('swat1'), *MASKED('swat2'), *MASKED('swat3')],
        cams=[C9])
for z in HZ:
    if 0 <= FALL9(z) < D9: st.cue('thud', 'S09', r(FALL9(z) + 0.22), 0.4)
st.cue('sfx:stepRun', 'S09', 0.0, 0.3)

# ============================== the cook's doorstep (the fallen door behind him)
COOK10 = [7.85, 0, -12.0]
DOORSTEP = lambda: [P('maison10', 'chvDoorWall', pos=[8.6, 0, -12.0], ry=-90, opts={'facade': True, 'w': 3.4, 'dir': -1, 'dark': True, 'fallAt': -2.0, 'num': 12, 'color': '#E7D2B0', 'door': '#2F5D8A'})]
TOQUE_H = lambda p, ry: off(p, ry, 0.42, 0.28, 1.35)
# 10: the cook was bald. Medium, three-quarter front: on his doorstep he lifts his toque off: perfectly bald, the scalp shining under the torch
#     beam of an officer at the left (CHAUVE)
D10 = st.dur('S10'); LIFT10 = 0.3
OFF10 = [6.75, 0, -11.25]; RYO10 = yaw(OFF10, COOK10)
TORCH10 = off(OFF10, RYO10, 0.5, -0.15, 1.6)
HEADTOP = [COOK10[0], 2.3, COOK10[2]]
C10 = FC('S10', 0.0, [5.3, 1.75, -13.1], {'cookTop': [COOK10[0], 2.75, COOK10[2]], 'cookHips': [COOK10[0], 0.9, COOK10[2]], 'cookL': [COOK10[0], 1.6, COOK10[2] - 0.45], 'torch': TORCH10}, top=0.2, bottom=0.8, lenses=range(30, 66), drift=(0.06, 0, 0.04))
TR10 = aim_rot(TORCH10, HEADTOP)
TOQ = lambda pid, who, keys=None: P(pid, 'chefHat', on={'actor': who, 'hand': 'L', 'offset': [0.0, 0.0, 0.05], 'rot': [PI, 0, 0]}, keys=keys or [])
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('cuisinier', COOK10, RYK, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': R5(off(COOK10, RYK, 0.05, -0.05, 2.3), 1, 0.06)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.0),
            k(LIFT10, toon={'reach': {'L': R5(off(COOK10, RYK, 0.3, -0.25, 2.55), 1, 0.06)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.18, toonEase='out'),
            k(r(LIFT10 + 0.35), toon={'reach': {'L': R5(off(COOK10, RYK, 0.4, -0.3, 1.35), 1, 0.06)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.25),
            *blink(1.15, {'lid': 0.4, 'mouth': 'line', 'brow': -0.1})]),
        act('flic1', OFF10, RYO10, 'stand', 'neutral', keys=[k(0.0, look=HEADTOP), k(0.0, toon={'reach': {'R': R5(add(TORCH10, [0, -0.04, 0]))}, 'hands': {'R': 'grip'}}, toonDur=0.0)])],
        props=[*DOORSTEP(), TOQ('toque10', 'cuisinier'), BALD('brille10', 'cuisinier', 1.0, [r(LIFT10 + 0.22), 1.0], 0.5),
               P('lampe10', 'tacLight', pos=TORCH10, ry=r(TR10[1]), rot=[r(TR10[0] - PI / 2), 0, TR10[2]], opts={'len': r(math.dist(TORCH10, HEADTOP) - 0.3), 'r': 0.3, 'beam': 0.18})],
        cams=[C10])
st.card('S10', 'CHAUVE', at=0.82)
st.cue('sfx:ding', 'S10', r(LIFT10 + 0.22), 0.35)

# 11: he was shaved anyway. Tight on his head from a little above: the officer's hand runs the buzzing clippers across the bare scalp, left to
#     right; nothing falls; a glint; he blinks
D11 = st.dur('S11'); PASS11 = (0.25, 0.85)
OFF11 = [7.2, 0, -12.75]; RYO11 = yaw(OFF11, COOK10)
CLIP0 = [COOK10[0] - 0.05, 2.33, COOK10[2] + 0.13]; CLIP1 = [COOK10[0] - 0.05, 2.33, COOK10[2] - 0.13]
C11 = FC('S11', 0.0, [6.55, 2.45, -11.95], {'chin': [COOK10[0] - 0.09, 1.78, COOK10[2]], 'clip0': add(CLIP0, [0, 0.12, 0.08]), 'clip1': add(CLIP1, [0, 0.12, -0.08])}, top=0.08, bottom=0.74, lenses=range(26, 50), drift=(0.05, -0.02, 0))
CLIPROT = [0.0, 0, PI / 2 + 0.2]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('cuisinier', COOK10, RYK, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': R5(off(COOK10, RYK, 0.4, -0.3, 1.35), 1, 0.06)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'gy': -0.5}}, toonDur=0.0),
            k(0.3, toon={'reach': {'L': R5(off(COOK10, RYK, 0.4, -0.3, 1.35), 1, 0.06)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'gy': -0.8, 'gx': 0.4}}, toonDur=0.2),
            k(0.75, toon={'reach': {'L': R5(off(COOK10, RYK, 0.4, -0.3, 1.35), 1, 0.06)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'gy': -0.8, 'gx': -0.4}}, toonDur=0.25),
            *blink(1.15, {'lid': 0.45, 'mouth': 'line'})]),
        act('flic1', OFF11, RYO11, 'stand', 'neutral', keys=[k(0.0, look=HEADTOP), k(0.0, toon={'reach': {'R': R5(add(CLIP0, [0, -0.02, 0.0]), 1, 0.06)}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(PASS11[0], toon={'reach': {'R': R5(add(CLIP1, [0, -0.02, 0.0]), 1, 0.06)}, 'hands': {'R': 'grip'}}, toonDur=PASS11[1] - PASS11[0], toonEase='inOut'),
            k(1.05, toon={'reach': {'R': R5(add(CLIP1, [0.15, 0.1, -0.1]), 1, 0.06)}, 'hands': {'R': 'grip'}}, toonDur=0.25)])],
        props=[*DOORSTEP(), TOQ('toque11', 'cuisinier'), BALD('brille11', 'cuisinier', 1.0, [r(PASS11[1] + 0.05)], 0.4),
               P('tondeuse11', 'chvClippers', pos=CLIP0, rot=CLIPROT, opts={'buzz': [[0.0, 1.05]], 's': 1.3}, keys=[k(PASS11[0], to=CLIP1, dur=PASS11[1] - PASS11[0], ease='inOut'), k(1.05, to=add(CLIP1, [0.15, 0.1, -0.1]), dur=0.25)])],
        cams=[C11])
st.cue('engine', 'S11', 0.0, 0.18, 1.05); st.cue('sfx:ding', 'S11', r(PASS11[1] + 0.05), 0.3)

# ============================== the pavement outside the restaurant: the customers and passers-by on chairs facing the street (-X), officers behind
REST = lambda: [P('resto', 'shopFront', pos=[9.6, 0, -3.0], ry=-90, opts={'text': 'RESTAURANT', 'w': 6.0, 'h': 2.8, 'color': '#E9D9B8', 'signBg': '#7A3328'})]
SEATS = [('client1', -1.0, '#5A3A22'), ('client2', -2.3, '#D8B25A'), ('client3', -3.6, '#9A9A96'), ('client4', -4.9, '#1E1C1E')]
CX = 7.6
# 12: then the customers and the passers-by, for comparison. High and wide: a row of them sitting bald on chairs, officers buzzing clippers over
#     their heads, piles of hair in their old colours growing at their feet, each with a numbered tag; cut lower on the second customer
D12 = st.dur('S12'); CUT12 = 1.2
C12a = FC('S12a', 0.0, [3.4, 5.6, 0.2], {'c1head': [CX, 2.0, -1.0], 'c4head': [CX, 2.0, -4.9], 'pile1': [CX - 0.75, 0.1, -0.9], 'pile4': [CX - 0.75, 0.1, -4.9], 'barb1': [CX + 0.65, 2.2, -1.0], 'barb4': [CX + 0.65, 2.2, -4.9]}, top=0.06, bottom=0.74, drift=(0.1, -0.08, -0.1))
C12b = FC('S12b', CUT12, [4.9, 1.6, -1.0], {'barb2top': [CX + 0.62, 2.3, -2.3], 'c2face': [CX, 1.6, -2.3], 'pile2tag': [CX - 0.62, 0.5, -2.15], 'pile2': [CX - 0.75, 0.05, -2.3]}, top=0.06, bottom=0.76, lenses=range(30, 66), drift=(0.08, 0, -0.04))
def BARBER(i, who, z, t1):
    """the officer behind seat i: his hand and the clippers sweep over the head (front to back), in step"""
    p0, p1 = [CX + 0.03, 1.98, z - 0.12], [CX + 0.03, 1.98, z + 0.12]
    ts = [r(0.12 + 0.3 * j + 0.07 * i) for j in range(int(t1 / 0.3))]
    hand = [k(0.0, toon={'reach': {'R': R5(add(p0, [0.0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.0)]
    hand += [k(t, toon={'reach': {'R': R5(add(p1 if j % 2 == 0 else p0, [0.0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.28, toonEase='inOut') for j, t in enumerate(ts)]
    cl = [k(t, to=(p1 if j % 2 == 0 else p0), dur=0.28, ease='inOut') for j, t in enumerate(ts)]
    return act(who, [CX + 0.62, 0, z], -90, 'stand', 'neutral', keys=[k(0.0, look=[CX, 1.95, z]), *hand]), P(f'tond_{who}', 'chvClippers', pos=p0, rot=[0, 0, PI / 2], opts={'buzz': [[0, 3]], 'bits': [[0.0, t1, SEATS[i][2]]]}, keys=cl)
BARBERS = ['flic3', 'flic4', 'flic5', 'flic6']
def CUSTOMERS(D, grow0=0.15):
    acts, props = [], []
    for i, (who, z, col) in enumerate(SEATS):
        acts.append(act(who, [CX, 0.03, z], -90, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45 + 0.05 * i, 'mouth': 'line'}}, toonDur=0.0), *blink(r(0.5 + 0.35 * i), {'lid': 0.45 + 0.05 * i, 'mouth': 'line'})]))
        props += [P(f'chaise12{i}', 'chair', pos=[CX + 0.15, 0, z], ry=-90, opts={'color': '#7A4A2A'}), BALD(f'brille_{who}', who, 1.0, [r(0.3 + 0.4 * i)], 0.4),
                  P(f'tas12{i}', 'chvHairPile', pos=[CX - 0.72, 0.0, r(z + 0.05)], ry=-60, opts={'color': col, 'num': i + 1, 'tagS': 1.6, 'grow': [[0, grow0 + 0.1 * i], [0.3, grow0 + 0.15 + 0.1 * i], [D, 0.8 + 0.05 * i]]})]
        a, p = BARBER(i, BARBERS[i], z, D); acts.append(a); props.append(p)
    return acts, props
A12, P12 = CUSTOMERS(D12)
st.shot('S12', 'parisStreet', setOpts=STREET, actors=A12, props=[*REST(), *P12], cams=[C12a, C12b])
st.cue('engine', 'S12', 0.0, 0.2, D12); st.cue('sfx:poof', 'S12', 0.6, 0.15)

# 13: the police dog too. Low at its height on the pavement: the dog shaved pink and smooth, standing at attention beside its handler, tongue out,
#     pleased, a glint on its back; its own small tagged pile of dark fur beside it
D13 = st.dur('S13')
DOG13 = [6.6, 0, -6.4]; HAND13 = [7.15, 0, -6.95]
C13 = FC('S13', 0.0, [3.8, 0.9, -4.3], {'dogHead': [DOG13[0] - 0.3, 0.85, DOG13[2] + 0.1], 'dogFeet': [DOG13[0], 0.0, DOG13[2]], 'handTop': [HAND13[0], 2.65, HAND13[2]], 'pile': [DOG13[0] - 0.35, 0.45, DOG13[2] - 0.75]}, top=0.12, bottom=0.8, lenses=range(30, 66), drift=(0.06, 0, -0.05))
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[
        act('maitre1', HAND13, -110, 'stand', 'neutral', keys=[k(0.0, look=[DOG13[0], 0.7, DOG13[2]]), k(0.0, toon={'reach': {'R': R5(off(HAND13, -110, 0.2, 0.25, 2.05), 1, 0.03)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
            k(0.6, look='camera', lookDur=0.2), *blink(1.0, {'lid': 0.3, 'mouth': 'line', 'brow': 0.3})])],
        props=[P('chien13', 'voxelDog', pos=DOG13, ry=-70, opts={'color': '#F2A9B9', 'muzzle': '#E07F96', 'tongue': 'long', 'eyes': 1.15}, keys=[k(0.35, rotTo=[0, -1.0, 0.12], dur=0.12), k(0.75, rotTo=[0, -1.22, 0], dur=0.12), k(1.05, rotTo=[0, -1.0, 0.1], dur=0.1)]),
               P('brille13', 'chvShine', pos=[DOG13[0] + 0.05, 0.6, DOG13[2] + 0.1], face='camera', opts={'s': 1.4, 'twinkle': [0.3, 1.0], 'tw0': 0.3, 'opacity': 0.0}),
               P('tas13', 'chvHairPile', pos=[DOG13[0] - 0.35, 0.0, DOG13[2] - 0.75], ry=-60, opts={'color': '#3A3530', 'num': 5, 'tagS': 1.4, 'r': 0.2})],
        cams=[C13])
st.cue('sfx:ding', 'S13', 0.3, 0.3); st.cue('sfx:sniff', 'S13', 0.8, 0.2)

# 14: this man, twice. Frontal close-up: he, bald, sits in the chair; the officer's hand runs the clippers over his head, pauses, and passes
#     again; his eyes roll up to them between the passes, then back to us
D14 = st.dur('S14'); P14 = [(0.12, 0.5), (0.85, 1.22)]
HERO14 = [CX, 0.03, -6.8]
B14 = [CX + 0.05, 0, -7.6]
CL14a = [CX + 0.03, 1.98, -6.68]; CL14b = [CX + 0.03, 1.98, -6.92]
C14 = cam(0.0, [6.2, 1.82, -6.8], [6.27, 1.82, -6.8], [7.6, 1.64, -6.8], [7.6, 1.64, -6.8], lens=40)
chk('S14', C14['from'], C14['lookAt'], 40, {'eyes': [CX - 0.09, 1.7, -6.8], 'chin': [CX - 0.09, 1.38, -6.8], 'top': [CX, 1.98, -6.8], 'clipA': CL14a, 'clipB': CL14b, 'barbFace': [B14[0], 2.0, B14[2]]})
FACE14 = {'lid': 0.45, 'mouth': 'line'}
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[
        act('mecChauve', HERO14, -90, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**FACE14, 'gy': -0.7}}, toonDur=0.0),
            k(0.55, toon={'face': {**FACE14, 'gy': -0.9, 'gx': 0.3}}, toonDur=0.15), k(0.7, toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.4, 'gy': -0.9}}, toonDur=0.1),
            k(1.25, toon={'face': FACE14}, toonDur=0.15), *blink(1.4, FACE14)]),
        act('flic3', B14, -10, 'stand', 'neutral', keys=[k(0.0, look=[CX, 1.95, -6.8]), k(0.0, toon={'reach': {'R': R5(add(CL14a, [0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.0),
            k(P14[0][0], toon={'reach': {'R': R5(add(CL14b, [0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.38, toonEase='inOut'),
            k(0.55, toon={'reach': {'R': R5(add(CL14a, [0.05, 0.12, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.25),
            k(P14[1][0], toon={'reach': {'R': R5(add(CL14b, [0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.37, toonEase='inOut')])],
        props=[P('chaise14', 'chair', pos=[CX + 0.15, 0, -6.8], ry=-90, opts={'color': '#7A4A2A'}), BALD('brille14', 'mecChauve', 1.0, [0.55, r(P14[1][1] + 0.05)], 0.35),
               P('tondeuse14', 'chvClippers', pos=CL14a, rot=[0, 0, PI / 2], opts={'buzz': [[0.0, 0.52], [0.82, 1.3]]},
                 keys=[k(P14[0][0], to=CL14b, dur=0.38, ease='inOut'), k(0.55, to=add(CL14a, [0.05, 0.12, 0]), dur=0.25), k(P14[1][0], to=CL14b, dur=0.37, ease='inOut')])],
        cams=[C14])
st.cue('engine', 'S14', P14[0][0], 0.18, 0.4); st.cue('engine', 'S14', P14[1][0], 0.18, 0.4); st.cue('sfx:ding', 'S14', r(P14[1][1] + 0.05), 0.25)

# ============================== the lab (a pale void): the bench, the microscope, the comparison screen, the shelves of hair bags behind
LAB = {'color': '#DCE6EA'}
BENCH = [0.0, 0, 0.0]; BH = 0.9
MIC = [-0.3, BH, 0.05]; SCR = [0.5, BH, -0.1]
SAV = [-0.3, 0, -0.62]
# 15: under the microscope: no match. The scientist peers into the microscope, one eye shut, the shelves of numbered hair bags behind; cut: push
#     in on the screen: the two samples, a scan line sweeping, then a big red cross
D15 = st.dur('S15'); CUT15 = 1.15; CROSS15 = 1.62
C15a = FC('S15a', 0.0, [0.35, 1.8, 2.4], {'savTop': [SAV[0], 2.3, SAV[2]], 'micBase': add(MIC, [0, 0.0, 0.1]), 'scrR': add(SCR, [0.42, 0.5, 0]), 'savL': [SAV[0] - 0.35, 1.5, SAV[2]]}, top=0.05, bottom=0.74, drift=(0, 0, -0.1))
C15b = FC('S15b', CUT15, [0.65, 1.42, 1.9], {'scrL': add(SCR, [-0.42, 0.47, 0]), 'scrR': add(SCR, [0.42, 0.47, 0]), 'scrTop': add(SCR, [0, 0.82, 0]), 'scrBot': add(SCR, [0, 0.3, 0])}, top=0.15, bottom=0.72, drift=(-0.02, -0.01, -0.35))
st.shot('S15', 'whiteVoid', setOpts=LAB, actors=[
        act('savant', SAV, 0, 'stand', 'neutral', keys=[k(0.0, look=add(MIC, [0, 0.5, -0.1])),
            k(0.0, toon={'reach': {'R': R5(add(MIC, [0.12, 0.2, -0.05])), 'L': R5(add(MIC, [-0.12, 0.2, -0.05]))}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'bend': {'spine': [0.42, 0, 0, 1, None], 'neck': [-0.25, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'lidR': 1.0, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.0),
            k(0.6, toon={'reach': {'R': R5(add(MIC, [0.12, 0.17, -0.05])), 'L': R5(add(MIC, [-0.12, 0.2, -0.05]))}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'bend': {'spine': [0.42, 0, 0, 1, None], 'neck': [-0.25, 0, 0, 1, None]}, 'face': {'lid': 0.1, 'lidR': 1.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.2)])],
        props=[P('paillasse15', 'table', pos=BENCH, opts={'w': 1.9, 'd': 0.8, 'h': BH, 'color': '#F2F2EE', 'legs': '#9AA2AC'}), P('micro15', 'chvMicroscope', pos=MIC, opts={'s': 1.25}),
               P('ecran15', 'chvScreen', pos=SCR, ry=-12, opts={'w': 0.78, 'scan': 0.6, 'crossAt': CROSS15}), P('etageres15', 'chvBagShelf', pos=[0.0, 0, -1.65])],
        cams=[C15a, C15b])
st.cue('sfx:beep', 'S15', 0.65, 0.2); st.cue('sfx:beep', 'S15', 1.0, 0.2); st.cue('sfx:sting', 'S15', CROSS15, 0.35)

# 16: the minister apologised to the hair. From the press seats: the minister at the podium turns and bows deeply to the hair standing on its
#     little red-cushioned stand beside the podium; flashes pop in the foreground
D16 = st.dur('S16'); BOW16 = 0.45
MIN = [-0.1, 0, -2.35]; RYM = 62
STAND = [0.62, 0, -2.0]; SH16 = 1.12
C16 = FC('S16', 0.0, [1.75, 1.6, 1.55], {'minTop': [MIN[0], 2.55, MIN[2]], 'minL': [MIN[0] - 0.25, 1.5, MIN[2]], 'hairTop': [STAND[0], SH16 + 0.6, STAND[2]], 'standFoot': [STAND[0], 0.7, STAND[2]]}, top=0.06, bottom=0.74, drift=(-0.05, 0, -0.12))
BOWED = {'reach': {'R': R5(off(MIN, RYM, 0.18, 0.12, 1.0)), 'L': R5(off(MIN, RYM, 0.15, -0.14, 1.05))}, 'hands': {'R': 'open', 'L': 'open'}}
st.shot('S16', 'pressRoom', setOpts={'backdrop': 'EXCUSES', 'bg': '#E4E8EE', 'fg': 'rgba(46,69,99,0.35)', 'fontScale': 0.55, 'flags': False, 'chairs': False, 'wall': '#C9D2DE', 'band': '#AAB6C4'}, actors=[
        act('ministre', MIN, RYM, 'stand', 'neutral', keys=[k(0.0, look=[STAND[0], 1.5, STAND[2]]),
            k(0.0, toon={**BOWED, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
            k(BOW16, toon={**BOWED, 'bend': {'spine': [0.95, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.8, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.35, toonEase='inOut'),
            k(r(BOW16 + 0.85), toon={**BOWED, 'bend': {'spine': [0.95, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.8, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.2),
            k(r(BOW16 + 1.1), toon={**BOWED, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'lid': 0.35, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.3, toonEase='inOut'), k(r(BOW16 + 1.25), look='camera', lookDur=0.2)])],
        props=[P('socle16', 'chvStand', pos=STAND, opts={'h': SH16, 'panel': True}),
               P('cheveu16', 'chvHair', pos=[STAND[0], SH16 + 0.065, STAND[2] + 0.02], ry=-15, opts={'L': 0.42, 'r': 0.013, 'wig': 0.04, 'waveF': 1.5, 'stand': [[0, 1]], 'stand0': 1, 'eyes': True, 'eyeS': 1.3, 'brows': True, 'blinks': [0.3, 1.5], 'gaze': [[0, -0.8, 0], [r(BOW16 + 0.3), -0.8, 0.6], [r(BOW16 + 1.3), 0, 0]], 'brow': [[0, 0.2], [r(BOW16 + 0.4), -0.4]]}),
               P('flash16', 'flashBursts', pos=[1.2, 0.95, 0.2], face='camera', opts={'n': 5, 'w': 1.0, 'h': 0.35, 'at': [0.25, 0.65, 1.05, 1.45, 1.85], 'life': 0.15})],
        cams=[C16])
for t in [0.25, 0.65, 1.05, 1.45, 1.85]: st.cue('sfx:shutter', 'S16', t, 0.3)

# 17: it was the last hair in the neighbourhood. Crane down over a square of shining bald heads (the pink dog among them) packed round the hair
#     alone on its stand in the middle, which looks up at us
D17 = st.dur('S17')
SQ = [0.0, -0.14, -6.0]
CROWD = [('foule0', 'madame'), ('foule1', 'worker'), ('foule2', 'mamie'), ('foule3', 'sportif'), ('foule4', 'boss'), ('foule5', 'serveur'), ('foule6', 'tourist'), ('foule7', 'prefet'),
         ('foule8', 'cop'), ('foule9', 'pyjama'), ('foule10', 'doctor'), ('foule11', 'fermier'), ('foule12', 'cuisinier'), ('foule13', 'client2')]
def ring_pos(i):
    n0 = 6; rr, a0 = (1.25, 0.0) if i < n0 else (2.1, 0.3); n = n0 if i < n0 else len(CROWD) - n0; j = i if i < n0 else i - n0
    a = a0 + j / n * 2 * PI; return [r(SQ[0] + rr * math.sin(a)), SQ[1], r(SQ[2] + rr * math.cos(a))]
C17 = [cam(0.0, [0.6, 10.5, -1.2], [0.5, 4.6, -2.6], [0.0, 0.0, -6.0], [0.0, 0.6, -6.0], lens=48, ease='out')]
chk('S17s', C17[0]['from'], C17[0]['lookAt'], 48, {'stand': add(SQ, [0, 1.2, 0]), 'ringN': add(ring_pos(0), [0, 2.2, 0]), 'ringFar': add(ring_pos(9), [0, 2.2, 0])})
chk('S17e', C17[0]['to'], C17[0]['lookAt2'], 48, {'hairTop': add(SQ, [0, 1.95, 0]), 'stand': add(SQ, [0, 1.2, 0]), 'ringNear': add(ring_pos(0), [0, 2.2, 0]), 'ringBack': add(ring_pos(3), [0, 2.2, 0]), 'outer6': add(ring_pos(6), [0, 2.2, 0])})
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[
        *[act(w, ring_pos(i), yaw(ring_pos(i), SQ), 'stand', 'neutral', keys=[k(0.0, look=add(SQ, [0, 1.5, 0])), *blink(r(0.4 + 0.11 * i), {'lid': 0.4, 'mouth': 'line'})]) for i, (w, _) in enumerate(CROWD)]],
        props=[P('socle17', 'chvStand', pos=SQ, opts={'h': 1.12, 'panel': False}),
               P('cheveu17', 'chvHair', pos=add(SQ, [0, 1.185, 0]), ry=20, opts={'L': 0.62, 'r': 0.02, 'wig': 0.04, 'waveF': 1.3, 'stand': [[0, 1]], 'stand0': 1, 'eyes': True, 'eyeS': 2.0, 'brows': True, 'rim': '#F4F1E8', 'blinks': [1.5], 'gaze': [[0, 0, 0], [0.9, 0, -1.0]]}),
               *[BALD(f'brille17_{w}', w, 1.1, [r(0.2 + 0.09 * i)], 0.5) for i, (w, _) in enumerate(CROWD)],
               P('chien17', 'voxelDog', pos=add(SQ, [1.55, 0.0, 1.2]), ry=-130, opts={'color': '#F2A9B9', 'muzzle': '#E07F96', 'tongue': 'long'})],
        cams=C17)
st.cue('sfx:wind', 'S17', 0.0, 0.2); st.cue('sfx:choir', 'S17', 0.2, 0.15)

# 18: the helicopter put it back. Night, low from the table under the window: the helicopter outside lowers the hair on its winch cable through
#     the window toward the bowl, the searchlight on; he, bald, looks up
D18 = st.dur('S18')
HW0 = [0.62, 2.45, -1.55]; HW1 = [0.05, 1.36, -0.22]
C18 = FC('S18', 0.0, [-0.45, 0.9, 1.4], {'bowl': add(BOWL, [0.1, 0.05, 0.1]), 'heliTop': add(HELI, [0, 0.9, 0]), 'headTop': [0, 1.98, -0.8], 'hair0': add(HW0, [0, 0.1, 0])}, top=0.04, bottom=0.75, lenses=range(30, 66), drift=(0.04, 0, -0.08))
st.shot('S18', 'whiteVoid', setOpts=NIGHT, look={'sun': 0.35, 'fill': 0.6, 'exposure': 1.05}, actors=[
        act('mecChauve', HERO, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=SIT({'lid': 0.5, 'mouth': 'line', 'gy': -0.9, 'gx': -0.3}), toonDur=0.0),
            k(0.9, toon=SIT({'lid': 0.45, 'mouth': 'line', 'gy': 0.2, 'gx': -0.4}), toonDur=0.3)])],
        props=[*ROOM(), *HELIP('heli18'), P('pool18', 'chvPool', pos=add(BOWL, [0, 0.01, 0]), opts={'r': 0.5, 'h': 0.7, 'power': 4}), BALD('brille18', 'mecChauve', 1.0, [0.2], 0.6),
               P('cheveu18', 'chvHair', pos=HW0, rot=[PI, 0, 0], opts={'L': 0.3, 'r': 0.0105, 'wig': 0.05, 'stand': [[0, 1]], 'stand0': 1}, keys=[k(0.0, to=HW1, dur=D18 - 0.1, ease='out')])],
        cams=[C18],
        tethers=[{'a': {'prop': 'heli18', 'offset': [0.0, -1.0, 0.6]}, 'b': {'prop': 'cheveu18', 'offset': [0, 0, 0]}, 'color': '#2A2C30', 'sag': 0.0, 'radius': 0.012, 'minPx': 4, 'rim': 0.4}])
st.cue('engine', 'S18', 0.0, 0.3, D18); st.cue('sfx:rotor', 'S18', 0.0, 0.3); st.cue('sfx:slideDownSlow', 'S18', 0.1, 0.25)

# 19: in this man's soup. The framing of shot 1: he, bald, before the same bowl; the hair drops in from above onto the soup, a ripple, it floats
#     and opens two little eyes at him; he looks at it, then at us
D19 = st.dur('S19'); LAND19 = 0.3
st.shot('S19', 'whiteVoid', setOpts=NIGHT, actors=[
        act('mecChauve', HERO, 0, 'sit', 'neutral', keys=[k(0.0, look=add(HAIR1, [0, 0.05, 0])),
            k(0.0, toon=SIT({'lid': 0.45, 'mouth': 'line', 'gy': 0.6}), toonDur=0.0),
            k(r(LAND19 + 0.05), toon=SIT({'lid': 0.3, 'mouth': 'line', 'gy': 0.8, 'brow': 0.3}), toonDur=0.1),
            k(1.45, look='camera', lookDur=0.15), k(1.45, toon=SIT({'lid': 0.5, 'mouth': 'line', 'brow': -0.15}), toonDur=0.15), *blink(1.9, {'lid': 0.5, 'mouth': 'line', 'brow': -0.15})])],
        props=[*[p for p in ROOM() if p['id'] != 'bol'], P('bol', 'chvBowl', pos=BOWL, opts={'steam': True, 'ripple': [LAND19]}), BALD('brille19', 'mecChauve', 1.0, [1.6], 0.35),
               P('cheveu19', 'chvHair', pos=add(HAIR1, [0, 0.45, 0]), ry=12, opts={**HAIRF, 'eyes': True, 'eyesFloat': True, 'eyesOn': [[0, 0], [0.85, 1]], 'blinks': [1.3], 'gaze': [[0, 0, -0.8], [1.5, 0, 0]], 'eyeS': 0.9},
                 keys=[k(0.0, to=HAIR1, dur=LAND19, ease='in')])],
        cams=[C1])
st.cue('sfx:splash', 'S19', LAND19, 0.3); st.cue('sfx:pop', 'S19', 0.85, 0.2)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
BALDC = lambda preset, seed, **kw: {'preset': preset, 'hair': 'bald', 'hat': 'none', 'seed': seed, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX, **kw}
st.write("Le cheveu", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecChauve': {**MEC, 'hairColor': '#E2B48E'},
    'flic1': {'preset': 'cop', 'seed': 880, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic2': {'preset': 'cop2', 'seed': 881, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    **{f'flic{i}': {'preset': 'cop' if i % 2 else 'cop2', 'seed': 880 + i, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for i in range(3, 7)},
    'inspecteur': {'preset': 'commissaire', 'seed': 887, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'maitre1': {'preset': 'cop', 'seed': 888, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}, 'maitre2': {'preset': 'cop2', 'seed': 889, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'maitre3': {'preset': 'cop', 'seed': 890, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'cuisinier': {'preset': 'chef', 'hat': 'none', 'hair': 'bald', 'glasses': False, 'seed': 891, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    **{f'swat{i}': {'preset': 'swat', 'hat': 'none', 'hair': 'bald', 'seed': 892 + i, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for i in (1, 2, 3)},
    'client1': BALDC('madame', 900), 'client2': BALDC('worker', 901), 'client3': BALDC('mamie', 902), 'client4': BALDC('sportif', 903),
    'savant': {'preset': 'doctor', 'seed': 905, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 906, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{w: BALDC(p if p not in ('cuisinier', 'client2') else ('chef' if p == 'cuisinier' else 'worker'), 910 + i) for i, (w, p) in enumerate(CROWD)},
})
