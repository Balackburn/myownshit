#!/usr/bin/env python3
"""La feuille (story 86, cycle 48; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man cut himself on a sheet of paper. She melted into the crowd. Description: white, rectangular. The police took in all the paper in the
country. And every banknote. And the intern, for harbouring a criminal. The finger recognised her. The prosecutor asked for the shredder. The
president put the shredder to a referendum. Fifty million ballots. A whole forest. The ballots all voted no. His first. The shredder was
abolished. The gendarmes flattened every shredder. The sheet was released. Turned into a dismissal letter. Addressed to this man. He sold
shredders.
Staging: at his shop's sales counter he freezes over his raised index finger, a thin red line on it, the sheet with her dog-ear and tiny red smear
lying on the counter, a price-tagged demo shredder and a wall of boxed shredders behind him. The sheet tilts her dog-ear toward the shredder and
slides herself into the open ream, smear down, gone among identical edges, his plastered finger hovering over the stack. In the street a policeman
slaps RECHERCHÉE posters with a blank white rectangle on the lampposts while he walks beside him holding up his plastered finger. A single file of
paper (reams, newspapers, books, a map, the posters last), each with a tiny numbered mugshot board, marches up the ramp of a police van
(EMBARQUÉ). Stacks of banknotes march down the bank's steps and up the same ramp, a police dog sniffs the last one, the director stares from the
door. The intern (an adult: thirties, tie, lanyard, briefcase at his feet), the empty ream wrapper beside him, is bent calmly over a police car's
bonnet and cuffed by a bored officer. In the line-up five identical sheets stand against the height chart; behind the glass his bandaged finger
rises on its own and points at the third; an officer flips her: the smear shows, the dog-ear springs up. At the foot of the courthouse steps the
sheet is held upright between two gendarmes; the prosecutor, at the microphones, whips the velvet cover off the same price-tagged shredder on a
trolley; she curls back, trembling. In the press room the president taps a pointer on a poster of the shredder with OUI and NON boxes. A school
gym is buried waist-deep in white ballots, officials wading with snow shovels. A hillside of fresh stumps: a gendarme with a chainsaw salutes as
the last log is loaded onto a truck marked BULLETINS. At the polling station the ballots wriggle out of the voters' fingers over the OUI box and
dive into the NON box. Close: his own ballot, over the OUI box at eight o'clock, twists out of his fingers and is the first into NON. The ushers
throw the cover back over the shredder and wheel it away; between the gendarmes the sheet stops trembling (ABOLIE). On a vast square a gendarme
drives a ribboned steamroller over rows of price-tagged shredders, flattening them like biscuits with puffs of confetti, a line of gendarmes
saluting. A gendarme opens his fingers and the sheet drifts away down the steps on a draught past the microphones. In the shop's back office the
manager's typewriter hammers LICENCIEMENT across her, by a bare paper shelf. From the manager's side, he slides her, folded in three, across the
counter; the hero takes her at arm's length by the far edge, bandaged finger lifted away. The framing of the first shot: the demo shredder gone,
only its price tag left on the plinth, the wall behind empty; he holds the letter to us.
Natural look; cycle 48: props_feuille.js (feuilleSheet, sheetStack, demoShredder, confettiPuff, shredderWall, salesCounter, paddyWagon,
paperParade, wantedPoster, glassPane, courtFront, micCluster, shredderTrolley, refPoster, pointerStick, ballotSea, snowShovel, stumpField,
logTruck, ballotBox, divingBallots, steamroller, shredderRows, typewriter, fingerBandage, cutLine, lanyard, bareShelf, lineupWall, emptyPlinth);
parkLot (props_place), streetLamp, policeCar, handcuffs, briefcase, voxelDog, chainsaw, wallClock, placard, mugshotBoard (props.js), kepi
(props_conseiller) reused.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.86) and heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() before stills; big
ground slabs drawn as no-depth layers (parkLot); the sheet, a thin plane, always faces the lens within 60 degrees; the bandage on the index
finger follows the hand joint (offset to the index); nobody hurt beyond the paper cut; no English, no brands, no real organisation or flag."""
from story_kit import *
import math

st = Story('feuille', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]
def R5(p, w=1, s=0.04): return [*p, w, s]
# the index finger of the right hand, in the hand joint's frame: the plaster (from line 3 on) and the cut (lines 1-2)
FINGER = [-0.031, -0.105, 0.017]
def PLASTER(pid, who='mec'): return P(pid, 'fingerBandage', on={'actor': who, 'joint': 'handR', 'offset': FINGER})
def CUT(pid, who='mec'): return P(pid, 'cutLine', on={'actor': who, 'joint': 'handR', 'offset': [FINGER[0], FINGER[1], FINGER[2] + 0.001]})
SHEET = {'w': 0.42, 'h': 0.56}
GEND = {'outfit': 'suit', 'suit': '#1E2A44', 'pants': '#1A2438', 'shirt': '#D9DEE8', 'lapel': '#141C30', 'tie': '#141C30', 'cuff': '#1E2A44', 'hat': 'none', 'hair': 'crew', 'facial': 'none',
        'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
def KEPI(pid, who): return P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#1A2438', 'band': '#C9CDD3'})
SALUTE = lambda p, ry: R5(off(p, ry, 0.08, 0.2, 2.02), 1, 0.03)
STREET = {'clouds': 30}

for g_ in [('S01', 1.2, 'mec', 'finger'), ('S02', 1.2, 'mec', 'lost'), ('S06', 1.6, 'stagiaire', 'bonnet'), ('S13', 0.9, 'mec', 'ballot'), ('S18', 0.9, 'mec', 'take'), ('S19', 1.4, 'mec', 'letter')]:
    st.gag(*g_)

# ============================== the shop (office walls, a wall of boxed shredders, the sales counter); he stands behind the counter facing +Z
SHOP = {'door': False, 'printer': False, 'picture': False, 'carpet': False, 'wall': '#E9E4D6', 'band': '#2E6FB5', 'trim': '#1E3A6E', 'floor': '#CFC6B2'}
CNT = [0.0, 0, -0.4]; TOP = 1.01                       # the counter (customer side +Z) and its top
HERO = [0.0, 0, -1.15]
DEMO = [0.52, 0, -1.95]                                # the demo shredder on its display plinth (0.75 high), behind his left shoulder
PH = 0.75
WALL = [0.0, 0, -2.75]
def SHOP_PROPS(empty=False, demo=True):
    ps = [P('comptoir', 'salesCounter', pos=CNT, opts={'w': 2.2}), P('mur', 'shredderWall', pos=WALL, opts={'w': 4.6, 'empty': empty})]
    ps.append(P('demo', 'demoShredder', pos=DEMO, ry=-12, opts={'plinth': True, 'ph': PH}) if demo else P('socle', 'emptyPlinth', pos=DEMO, ry=-12, opts={'ph': PH}))
    return ps
C1 = cam(0.0, [0.2, 2.45, 2.3], [0.19, 2.43, 2.15], [0.18, 1.36, -0.9], [0.18, 1.37, -0.9], lens=44)

# 1: the hook. Medium close-up across the counter: he is frozen over his raised right index finger, a thin red line on it, eyes wide on it; the
#    sheet lies on the counter at his left, dog-ear and tiny red smear; behind him the demo shredder with its price tag and the wall of boxes
D1 = st.dur('S01')
SH1 = [0.33, r(TOP + 0.004), -0.42]
FING1 = R5(off(HERO, 0, 0.5, 0.08, 1.78), 1, 0.06)
chk('S01', C1['from'], C1['lookAt'], 44, {'face': [HERO[0], 2.0, HERO[2]], 'finger': FING1[:3], 'sheet': SH1, 'demoTag': [DEMO[0] + 0.24, 1.6, DEMO[2] + 0.2], 'wallTop': [0, 2.6, WALL[2]]})
SHOCK = {'lid': 0.0, 'pop': 0.35, 'mouth': 'O', 'brow': 0.7}
st.shot('S01', 'office', setOpts=SHOP, actors=[
        act('mec', HERO, 0, 'stand', 'neutral', keys=[k(0.0, look=FING1[:3]),
            k(0.0, toon={'reach': {'R': FING1}, 'hands': {'R': 'point'}, 'face': {'lid': 0.1, 'pop': 0.2, 'mouth': 'O', 'brow': 0.5}, 'sq': [1, 1, 1]}, toonDur=0.0),
            k(0.35, toon={'reach': {'R': R5(add(FING1[:3], [0, 0.03, 0.03]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': SHOCK, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.1, toonEase='out'),
            *[k(r(0.55 + 0.12 * i), toon={'reach': {'R': R5(add(FING1[:3], [0.006 * (1 if i % 2 else -1), 0.03, 0.03]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': SHOCK}, toonDur=0.05) for i in range(8)],
            *blink(1.55, SHOCK)])],
        props=[*SHOP_PROPS(), P('feuille1', 'feuilleSheet', pos=SH1, rot=[-PI / 2, 0, 0.35], opts={**SHEET}), CUT('coupure1')],
        cams=[C1])
st.cue('sfx:paper', 'S01', 0.05, 0.4); st.cue('sfx:gasp', 'S01', 0.35, 0.25); st.cue('sfx:heartbeat', 'S01', 0.8, 0.15)

# 2: she melted into the crowd. Over the counter, high three-quarter: the sheet lifts her dog-ear toward the demo shredder, flips smear down and
#    slides herself into the open ream lying on the counter, gone among the identical edges; his plastered finger hovers over the stack, lost
D2 = st.dur('S02')
STACK2 = [-0.18, TOP, -0.35]; SH2 = [0.36, r(TOP + 0.004), -0.32]
C2 = cam(0.0, [0.15, 2.95, 1.15], [0.14, 2.9, 1.05], [0.05, 1.15, -0.42], [0.05, 1.15, -0.42], lens=44)
HOV2 = R5([STACK2[0] + 0.05, 1.42, STACK2[2] + 0.05], 1, 0.06)
chk('S02', C2['from'], C2['lookAt'], 44, {'stack': STACK2, 'sheet': SH2, 'finger': HOV2[:3], 'face': [HERO[0], 2.0, HERO[2]], 'demo': [DEMO[0], 1.3, DEMO[2]]})
TILT2, FLIP2, SLIDE2 = 0.15, 0.55, 0.8
st.shot('S02', 'office', setOpts=SHOP, actors=[
        act('mec', HERO, 0, 'stand', 'neutral', keys=[k(0.0, look=SH2),
            k(0.0, toon={'reach': {'R': R5(add(HOV2[:3], [0.4, 0.1, 0.05]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.15, 'mouth': 'O', 'brow': 0.4}}, toonDur=0.0),
            k(r(SLIDE2 + 0.3), look=add(STACK2, [0, 0.15, 0]), lookDur=0.15),
            k(r(SLIDE2 + 0.25), toon={'reach': {'R': HOV2}, 'hands': {'R': 'point'}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.25),
            *[k(r(SLIDE2 + 0.6 + 0.15 * i), toon={'reach': {'R': R5(add(HOV2[:3], [0.06 * (i % 2 * 2 - 1), 0, 0.03 * (i % 2)]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.25, 'mouth': 'wavy' if i % 2 else 'line', 'brow': 0.7}}, toonDur=0.12) for i in range(4)]])],
        props=[*SHOP_PROPS(), P('rame2', 'sheetStack', pos=STACK2, ry=8, opts={}), PLASTER('pansement2'),
               P('feuille2', 'feuilleSheet', pos=SH2, rot=[-PI / 2, 0, 0.35], opts={**SHEET, 'earKeys': [[TILT2, 0.55], [FLIP2, 1.0]]},
                 keys=[k(TILT2, rotTo=[-PI / 2 + 0.35, 0.25, 0.6], dur=0.2, ease='out'), k(FLIP2, rotTo=[PI / 2, 0, 0.1], dur=0.2, ease='inOut'),
                       k(FLIP2, to=add(STACK2, [0.45, 0.16, 0.02]), dur=0.2, ease='out'), k(SLIDE2, to=add(STACK2, [0.0, 0.1, 0.0]), dur=0.22, ease='in'), k(r(SLIDE2 + 0.22), visible=False)])],
        cams=[C2])
st.cue('whoosh', 'S02', TILT2, 0.15, 0.25, 900, 3000); st.cue('sfx:paper', 'S02', FLIP2, 0.4); st.cue('sfx:zip', 'S02', SLIDE2, 0.35)

# ============================== the street (parisStreet): the road along Z (x -5..5), the right pavement x 5..10, the house fronts at x 10.2
# 3: description: white, rectangular. Low on the pavement: a policeman slaps a RECHERCHÉE poster (a blank white rectangle where the face should be)
#    on the nearest lamppost, the same poster already on every lamppost down the street; he walks beside him holding up his plastered finger
D3 = st.dur('S03'); SLAP3 = 0.55
LAMPS = [[5.7, z] for z in (1.6, -5.0, -11.6, -18.2, -24.8)]
COP3 = [6.25, 0, 1.25]; RYC3 = -90
HERO3a, HERO3b = [7.1, 0, -2.4], [7.1, 0, 0.6]
C3 = cam(0.0, [6.7, 1.6, 9.6], [6.68, 1.61, 9.3], [6.3, 1.75, -3.0], [6.3, 1.76, -3.0], lens=38)
POST = lambda z: [5.7, 1.85, r(z + 0.11)]
chk('S03', C3['from'], C3['lookAt'], 38, {'poster1': POST(1.6), 'poster2': POST(-5.0), 'poster3': POST(-11.6), 'copFace': [COP3[0], 2.0, COP3[2]], 'heroA': [HERO3a[0], 2.0, HERO3a[2]], 'heroB': [HERO3b[0], 2.0, HERO3b[2]], 'heroFeetB': HERO3b})
FING3 = lambda p: R5(off(p, 0, 0.42, 0.22, 2.05), 1, 0.06)
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('policier', COP3, RYC3, 'stand', 'neutral', keys=[k(0.0, look=POST(1.6)),
            k(0.0, toon={'reach': {'L': R5(add(POST(1.6), [0.45, -0.1, 0.25]))}, 'hands': {'L': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(r(SLAP3 - 0.18), toon={'reach': {'L': R5(add(POST(1.6), [0.55, 0.15, 0.3]))}, 'hands': {'L': 'open'}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.15),
            k(SLAP3, toon={'reach': {'L': R5(add(POST(1.6), [0.03, 0, 0.03]), 1, 0.08)}, 'hands': {'L': 'open'}, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.06, toonEase='in'),
            k(r(SLAP3 + 0.45), toon={'reach': {'L': R5(add(POST(1.6), [0.4, -0.5, 0.25]))}, 'hands': {'L': 'rest'}, 'sq': [1, 1, 1]}, toonDur=0.3),
            k(r(SLAP3 + 0.6), look='camera', lookDur=0.2)]),
        act('mec', HERO3a, 0, 'walk', 'unimpressed', keys=[k(0.0, to=HERO3b, dur=1.75, clip='walk'), k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': FING3(HERO3a)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(1.75, toon={'reach': {'R': FING3(HERO3b)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.2), *blink(2.0, {'lid': 0.35, 'mouth': 'line', 'brow': -0.2})])],
        props=[*[P(f'lampe3{i}', 'streetLamp', pos=[x, 0, z]) for i, (x, z) in enumerate(LAMPS)],
               *[P(f'affiche3{i}', 'wantedPoster', pos=POST(z), opts={'at': SLAP3 if i == 0 else -1}) for i, (x, z) in enumerate(LAMPS)], PLASTER('pansement3')],
        cams=[C3])
st.cue('sfx:splat', 'S03', SLAP3, 0.45); st.cue('sfx:step', 'S03', 0.3, 0.2); st.cue('sfx:step', 'S03', 0.75, 0.2); st.cue('sfx:step', 'S03', 1.2, 0.2); st.cue('sfx:step', 'S03', 1.65, 0.2)

# 4: the police took in all the paper in the country. Low in the road behind a police van with its back open: a single file of paper (reams,
#    newspapers, books, a rolled map, then the RECHERCHÉE posters) marches across the road and up its steel ramp, each holding a tiny numbered
#    mugshot board (EMBARQUÉ)
D4 = st.dur('S04')
VAN = [3.0, 0, -4.6]; VAN_RY = 90                      # nose -Z, its back (and the ramp) toward +Z
RAMP_TOP = [3.0, 0.47, r(VAN[2] + 2.72)]; RAMP_FOOT = [3.0, 0.02, r(VAN[2] + 2.72 + 2.6)]
PATH4 = [[5.9, 0.02, 3.2], [4.3, 0.02, 1.9], RAMP_FOOT, RAMP_TOP, [3.0, 0.5, r(VAN[2] + 1.0)]]
C4 = cam(0.0, [5.0, 1.15, 6.4], [4.92, 1.16, 6.2], [3.3, 0.95, -1.6], [3.3, 0.96, -1.6], lens=42)
chk('S04', C4['from'], C4['lookAt'], 42, {'rampFoot': RAMP_FOOT, 'rampTop': RAMP_TOP, 'vanTop': [3.0, 3.0, VAN[2] + 2.5], 'path0': PATH4[0], 'path1': PATH4[1], 'vanLabel': [4.12, 1.55, VAN[2]]})
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('fourgon4', 'paddyWagon', pos=VAN, ry=VAN_RY, opts={}),
               P('defile4', 'paperParade', pos=[0, 0, 0], opts={'path': PATH4, 'at': 0.0, 'lead': 3.4, 'speed': 1.35, 'gap': 0.72, 'n': 12, 's': 1.35, 'kinds': ['ream', 'news', 'book', 'map', 'ream', 'news', 'book', 'ream', 'news', 'map', 'poster', 'poster']})],
        cams=[C4])
st.card('S04', 'EMBARQUÉ', at=0.9)
st.cue('sfx:stepSoft', 'S04', 0.2, 0.25); st.cue('sfx:stepSoft', 'S04', 0.55, 0.25); st.cue('sfx:stepSoft', 'S04', 0.9, 0.25); st.cue('sfx:stepSoft', 'S04', 1.25, 0.25); st.cue('sfx:stepSoft', 'S04', 1.6, 0.25); st.cue('clang', 'S04', 0.9, 0.15)

# 5: and every banknote. Low in the road: from the bank's open door, stacks of banknotes march down its three steps, across the pavement and up the
#    same van's ramp, each with its mugshot board; a police dog sniffs the last stack; the director stands in the doorway staring at us
D5 = st.dur('S05')
BANK = [0.0, 0, -3.0]                                  # the bank's front faces +Z (us): three steps, the door far back under its BANQUE sign
VAN5 = [6.9, 0, -0.6]                                  # nose +X: its open back and the ramp toward -X, the ramp's foot at the frame's right edge
PATH5 = [[0.0, 0.87, -6.9], [0.0, 0.87, -4.25], [0.15, 0.02, -2.9], [1.0, 0.02, -1.4], [1.6, 0.02, -0.6], [4.2, 0.47, -0.6], [5.5, 0.5, -0.6]]
DIR5 = [0.55, 0.87, -6.75]
DOG5 = [1.05, 0, 0.55]
C5 = cam(0.0, [0.6, 1.7, 5.4], [0.62, 1.71, 5.2], [0.6, 1.25, -3.0], [0.62, 1.26, -3.0], lens=44)
chk('S05', C5['from'], C5['lookAt'], 44, {'door': [0, 1.5, -6.9], 'dirFace': [DIR5[0], DIR5[1] + 2.0, DIR5[2]], 'sign': [0, 4.0, -6.95], 'landing': [0, 0.87, -4.25], 'stepFoot': [0.15, 0.05, -2.9], 'rampFoot': [1.6, 0.02, -0.6], 'dog': [DOG5[0], 0.6, DOG5[2]]})
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('directeur', DIR5, 0, 'stand', 'scared', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': R5(off(DIR5, 0, 0.12, 0.28, 2.15)), 'L': R5(off(DIR5, 0, 0.12, -0.28, 2.15))}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.0),
            *blink(0.8, {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.8})])],
        props=[P('banque5', 'courtFront', pos=BANK, opts={'title': 'BANQUE', 'steps': 3, 'w': 7, 'cols': 4, 'open': True, 'H': 4.4, 'doorH': 2.8, 'doorSign': 'BANQUE'}),
               P('fourgon5', 'paddyWagon', pos=VAN5, ry=0, opts={}),
               P('billets5', 'paperParade', pos=[0, 0, 0], opts={'path': PATH5, 'at': 0.0, 'lead': 4.6, 'speed': 1.6, 'gap': 0.75, 'n': 8, 's': 1.3, 'kinds': ['notes']}),
               P('chien5', 'voxelDog', pos=DOG5, ry=-150, opts={'color': '#3A3530', 'muzzle': '#1E1A18'})],
        cams=[C5])
st.cue('sfx:stepSoft', 'S05', 0.15, 0.25); st.cue('sfx:stepSoft', 'S05', 0.5, 0.25); st.cue('sfx:sniff', 'S05', 0.7, 0.35); st.cue('sfx:stepSoft', 'S05', 0.9, 0.25)

# 6: and the intern, for harbouring a criminal. On the pavement by a police car: the intern (thirties, tie, lanyard, glasses), bent calmly over the
#    bonnet, his cheek on it, the empty green ream wrapper beside his face, his briefcase at his feet; a bored officer behind him clicks the cuffs on
D6 = st.dur('S06'); CLICK6 = 1.15
CAR6 = [3.6, 0, -1.0]                                 # nose -Z (ry 90): the bonnet at z -2.0..-3.0
INT6 = [4.95, 0, -2.5]; RYI6 = -90
OFF6 = [5.55, 0, -1.7]; RYO6 = -120
C6 = cam(0.0, [1.3, 1.5, -2.95], [1.4, 1.5, -2.9], [4.95, 1.3, -2.4], [4.95, 1.31, -2.4], lens=42)
chk('S06', C6['from'], C6['lookAt'], 42, {'intFace': off(INT6, RYI6, 0.55, 0.0, 1.25), 'offFace': [OFF6[0], 2.0, OFF6[2]], 'bonnet': [3.6, 0.95, -2.5], 'wrapper': [4.0, 1.0, -2.05], 'brief': [5.25, 0.3, -1.85], 'lanyard': off(INT6, RYI6, 0.4, 0, 1.2)})
BACK6 = off(INT6, RYI6, -0.2, 0.0, 1.0)
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('stagiaire', INT6, RYI6, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': R5(add(BACK6, [0, 0, -0.08])), 'L': R5(add(BACK6, [0, 0, 0.08]))}, 'hands': {'R': 'rest', 'L': 'rest'}, 'bend': {'spine': [1.05, 0, 0, 1, None], 'neck': [-0.55, 0, 0, 1, None]},
                         'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.1}}, toonDur=0.0),
            *blink(0.6, {'lid': 0.45, 'mouth': 'line', 'brow': 0.1}), *blink(1.9, {'lid': 0.5, 'mouth': 'flat', 'brow': 0.2}), k(r(CLICK6 + 0.05), toon={'face': {'lid': 0.5, 'mouth': 'flat', 'brow': 0.2}, 'sq': [1.02, 0.98, 1.02]}, toonDur=0.08, keepPose=True)]),
        act('officier', OFF6, RYO6, 'stand', 'unimpressed', keys=[k(0.0, look=BACK6),
            k(0.0, toon={'reach': {'R': R5(add(BACK6, [0.18, 0.02, -0.1])), 'L': R5(add(BACK6, [0.18, 0.02, 0.1]))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.6, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.0),
            k(r(CLICK6 - 0.1), toon={'reach': {'R': R5(add(BACK6, [0.12, 0.0, -0.06])), 'L': R5(add(BACK6, [0.15, 0.02, 0.1]))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.32, 0, 0, 1, None]}, 'face': {'lid': 0.65, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.1),
            k(r(CLICK6 + 0.5), look='camera', lookDur=0.3), *blink(1.9, {'lid': 0.65, 'mouth': 'line', 'brow': -0.1})])],
        props=[P('voiture6', 'policeCar', pos=CAR6, ry=90), P('emballage6', 'sheetStack', pos=[4.0, 0.96, -2.35], ry=20, opts={'empty': True}),
               P('mallette6', 'briefcase', pos=[5.3, 0, -1.85], ry=-60), P('badge6', 'lanyard', on={'actor': 'stagiaire', 'joint': 'torso', 'offset': [0.0, 0.48, 0.0]}),
               P('menottes6', 'handcuffs', on={'actor': 'stagiaire', 'hand': 'R'}, keys=[k(0.0, visible=False), k(CLICK6, visible=True)])],
        cams=[C6])
st.cue('sfx:cuff', 'S06', CLICK6, 0.5); st.cue('sfx:static', 'S06', 0.2, 0.1)

# 7: the finger recognised her. Over his left shoulder from behind, through the tinted glass: five identical white sheets stand against the
#    height chart; his right arm rises on its own, the plastered index pointing at the third; an officer flips her: the red smear shows, the
#    dog-ear springs up
D7 = st.dur('S07'); RISE7, FLIP7 = 0.05, 0.62
LINE_Z = -2.55; SHL = {'w': 0.6, 'h': 0.8}
HERO7 = [-0.62, 0, 2.0]; RYH7 = 180
COP7a, COP7b = [1.3, 0, -1.55], [0.45, 0, -1.95]
C7 = cam(0.0, [-0.25, 2.25, 4.7], [-0.24, 2.24, 4.6], [0.15, 1.1, -2.4], [0.15, 1.1, -2.4], lens=36)
PT7 = R5([-0.12, 1.95, 1.25], 1, 0.1)
chk('S07', C7['from'], C7['lookAt'], 36, {'sheet1': [-1.1, 0.4, LINE_Z], 'sheet3': [0.0, 0.4, LINE_Z], 'sheet5': [1.1, 0.4, LINE_Z], 'heroHead': [HERO7[0], 2.0, HERO7[2]], 'hand': PT7[:3], 'copFace': [COP7b[0], 2.0, COP7b[2]], 'glassTop': [0, 2.2, 0.7]})
st.shot('S07', 'whiteVoid', setOpts={'color': '#C9CED3'}, actors=[
        act('mec', HERO7, RYH7, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.6, LINE_Z]),
            k(0.0, toon={'reach': {'R': R5(off(HERO7, RYH7, 0.15, 0.3, 0.9))}, 'hands': {'R': 'rest'}}, toonDur=0.0),
            k(RISE7, toon={'reach': {'R': R5(add(PT7[:3], [0, -0.25, 0.2]), 1, 0.1)}, 'hands': {'R': 'point'}}, toonDur=0.2, toonEase='out'),
            k(r(RISE7 + 0.22), toon={'reach': {'R': PT7}, 'hands': {'R': 'point'}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.12, toonEase='out'),
            k(r(RISE7 + 0.2), look=PT7[:3], lookDur=0.12), k(r(RISE7 + 0.55), look=[0.0, 0.6, LINE_Z], lookDur=0.12)]),
        act('policier', COP7a, -60, 'stand', 'neutral', keys=[k(0.0, to=COP7b, dur=0.45, clip='walk'), k(0.0, look=[0.0, 0.5, LINE_Z]),
            k(r(FLIP7 - 0.12), toon={'reach': {'R': R5([0.2, 0.75, LINE_Z + 0.1])}, 'hands': {'R': 'grip'}}, toonDur=0.12),
            k(r(FLIP7 + 0.16), toon={'reach': {'R': R5([-0.15, 0.85, LINE_Z + 0.15])}, 'hands': {'R': 'open'}}, toonDur=0.12)])],
        props=[P('tapissage7', 'lineupWall', pos=[0, 0, -3.15], opts={'w': 4.4, 'gap': 0.55}), P('vitre7', 'glassPane', pos=[0, 0, 0.75], opts={'w': 3.6, 'h': 1.35, 'y': 0.85}),
               *[P(f'feuille7{i}', 'feuilleSheet', pos=[r((i - 2) * 0.55), 0.4, LINE_Z], opts={**SHL, 'ear': 0, 'smear': False}) for i in (0, 1, 3, 4)],
               P('suspecte7', 'feuilleSheet', pos=[0.0, 0.4, LINE_Z], opts={**SHL, 'smearSide': 'back', 'ear0': 0.0, 'earKeys': [[r(FLIP7 + 0.17), 0.72]]}, keys=[k(FLIP7, rotTo=[0, PI, 0], dur=0.16, ease='inOut')]),
               PLASTER('pansement7')],
        cams=[C7])
st.cue('whoosh', 'S07', RISE7, 0.2, 0.25, 600, 2400); st.cue('sfx:paper', 'S07', FLIP7, 0.5); st.cue('sfx:spring', 'S07', r(FLIP7 + 0.17), 0.3)

# ============================== the courthouse: a stone front with six steps and columns (TRIBUNAL), a paved forecourt; the sheet between two
# gendarmes at the foot of the steps (they hold her top corners), the prosecutor at his microphones, the trolley shredder
CT = [-0.65, 0, -1.6]
PLAZA = P('parvis', 'parkLot', pos=[0, 0, 4.0], opts={'w': 40, 'd': 24, 'rows': [], 'color': '#C9C2B2', 'y': 0.03})
SHC = {'w': 0.6, 'h': 0.8}
G1 = [-1.15, 0, 0.75]; G2 = [-0.15, 0, 0.75]
SHEET_C = [-0.65, 1.92, 0.82]
PROC = [1.05, 0, 1.9]; RYP = -115
TROL = [0.5, 0, 1.05]
MICS = [0.95, 0, 2.75]
CORNER = lambda s: [r(SHEET_C[0] + s * 0.29), r(SHEET_C[1] + 0.38), r(SHEET_C[2] + 0.02)]
def GKEYS(face=None):
    f = face or {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}
    return {'g1': [k(0.0, look='camera'), k(0.0, toon={'reach': {'L': R5(CORNER(-1), 1, 0.06)}, 'hands': {'L': 'pinch'}, 'face': f}, toonDur=0.0), *blink(0.7, f), k(1.2, look=SHEET_C, lookDur=0.25)],
            'g2': [k(0.0, look='camera'), k(0.0, toon={'reach': {'R': R5(CORNER(1), 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': f}, toonDur=0.0), *blink(1.05, f), k(0.5, look=SHEET_C, lookDur=0.25), k(1.4, look='camera', lookDur=0.25)]}
COURT = lambda: [P('tribunal', 'courtFront', pos=CT, opts={'w': 13, 'steps': 6, 'cols': 6}), PLAZA]

# 8: the prosecutor asked for the shredder. Low on the forecourt: the sheet upright between the two gendarmes; the prosecutor at his microphones
#    whips the red velvet cover off the price-tagged shredder on its trolley; she curls back, trembling
D8 = st.dur('S08'); OFF8 = 0.7
C8 = cam(0.0, [0.1, 1.05, 7.2], [0.08, 1.07, 6.9], [0.0, 1.95, 0.8], [0.0, 1.96, 0.8], lens=44)
chk('S08', C8['from'], C8['lookAt'], 42, {'sheetTop': CORNER(-1), 'sheetMid': SHEET_C, 'g1Face': [G1[0], 2.0, G1[2]], 'g2Face': [G2[0], 2.0, G2[2]], 'procFace': [PROC[0], 2.0, PROC[2]], 'trolley': [TROL[0], 1.4, TROL[2]], 'mics': [MICS[0], 1.35, MICS[2]], 'columnTop': [0, 7.5, -3.2]})
GK8 = GKEYS()
st.shot('S08', 'grassland', setOpts={'clouds': 26}, actors=[
        act('gendarme1', G1, 0, 'stand', 'neutral', keys=GK8['g1']), act('gendarme2', G2, 0, 'stand', 'neutral', keys=GK8['g2']),
        act('procureur', PROC, RYP, 'stand', 'angry', keys=[k(0.0, look=[TROL[0], 1.5, TROL[2]]),
            k(0.0, toon={'reach': {'R': R5(add(TROL, [0.25, 1.75, 0.15]))}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': -0.4}}, toonDur=0.0),
            k(r(OFF8 - 0.2), toon={'reach': {'R': R5(add(TROL, [0.15, 1.55, 0.05]))}, 'hands': {'R': 'grip'}, 'sq': [1.04, 0.96, 1.04]}, toonDur=0.15),
            k(OFF8, toon={'reach': {'R': R5(add(TROL, [1.0, 2.45, 0.35]), 1, 0.1)}, 'hands': {'R': 'grip'}, 'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.3}}, toonDur=0.12, toonEase='out'),
            k(r(OFF8 + 0.3), look='camera', lookDur=0.2), k(r(OFF8 + 0.5), toon={'reach': {'R': R5(add(TROL, [0.75, 2.1, 0.3]))}, 'hands': {'R': 'open'}, 'sq': [1, 1, 1]}, toonDur=0.3)])],
        props=[*COURT(), P('chariot8', 'shredderTrolley', pos=TROL, ry=-20, opts={'offAt': OFF8}), P('micros8', 'micCluster', pos=MICS, ry=180, opts={}),
               P('feuille8', 'feuilleSheet', pos=SHEET_C, opts={**SHC, 'curl': [[r(OFF8 + 0.15), 0.32]], 'tremble': [[r(OFF8 + 0.15), 1.0]]}),
               KEPI('kepi8a', 'gendarme1'), KEPI('kepi8b', 'gendarme2')],
        cams=[C8])
st.cue('whoosh', 'S08', OFF8, 0.35, 0.3, 500, 2600); st.cue('sfx:gasp', 'S08', r(OFF8 + 0.2), 0.15)

# 9: the president put the shredder to a referendum. The press room: the president in his sash at the podium taps a pointer on the poster of the
#    same price-tagged shredder beside him, with its OUI and NON boxes
D9 = st.dur('S09')
PRES9 = [-0.1, 0, -2.45]
POSTER9 = [0.95, 0, -2.25]
C9 = cam(0.0, [0.45, 1.95, 2.6], [0.43, 1.96, 2.4], [0.45, 1.85, -2.3], [0.45, 1.86, -2.3], lens=42)
TAP9 = [r(POSTER9[0] - 0.12), 2.15, r(POSTER9[2] + 0.3)]
chk('S09', C9['from'], C9['lookAt'], 42, {'presFace': [PRES9[0], 2.05, PRES9[2]], 'posterTop': [POSTER9[0], 2.5, POSTER9[2] + 0.1], 'posterOUI': [POSTER9[0] - 0.4, 1.35, POSTER9[2] + 0.1], 'posterNON': [POSTER9[0] + 0.25, 1.35, POSTER9[2] + 0.1], 'hand': TAP9})
st.shot('S09', 'pressRoom', setOpts={'backdrop': 'RÉFÉRENDUM', 'flags': False, 'chairs': False}, actors=[
        act('president', PRES9, 12, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            *[k(r(0.2 + 0.36 * i), toon={'reach': {'L': R5(add(TAP9, [-0.12 * (i % 2), -0.05 * (i % 2), -0.06 * (i % 2)]), 1, 0.06)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.35, 'mouth': 'open' if i % 2 else 'smile', 'brow': 0.3}}, toonDur=0.08 if i % 2 == 0 else 0.18) for i in range(6)],
            k(0.9, look=[POSTER9[0], 2.0, POSTER9[2]], lookDur=0.2), k(1.6, look='camera', lookDur=0.2)])],
        props=[P('affiche9', 'refPoster', pos=POSTER9, ry=-18, opts={}), P('baguette9', 'pointerStick', on={'actor': 'president', 'hand': 'L', 'offset': [0.0, -0.06, 0.02], 'rot': [PI * 0.62, 0, 0]}, opts={'len': 0.9})],
        cams=[C9])
st.cue('clack', 'S09', 0.2, 0.25); st.cue('clack', 'S09', 0.92, 0.25); st.cue('clack', 'S09', 1.64, 0.25)

# 10: fifty million ballots. A school gym buried waist-deep in white ballots; three officials wade through them pushing snow shovels
D10 = st.dur('S10')
OFFS10 = [('officiel1', [-0.75, 0, -0.6], 20), ('officiel2', [0.3, 0, -1.7], -10), ('officiel3', [0.95, 0, -0.1], -35)]
C10 = cam(0.0, [0.2, 2.75, 5.0], [0.2, 2.7, 4.75], [0.1, 1.15, -1.0], [0.1, 1.16, -1.0], lens=46)
chk('S10', C10['from'], C10['lookAt'], 46, {**{w: [p[0], 2.0, p[2]] for w, p, ry in OFFS10}, 'seaFront': [0, 0.95, 3.0], 'wallLabel': [0.8, 2.85, -3.6]})
def SHOVEL_K(p, ry, ph):
    return [k(0.0, look='camera' if ph == 0 else off(p, ry, 1.5, 0, 0.9))] + [k(r(0.12 * j + ph), toon={'reach': {'R': R5(off(p, ry, 0.55 + 0.2 * (j % 2), 0.12, 1.15)), 'L': R5(off(p, ry, 0.45 + 0.2 * (j % 2), -0.18, 1.35))}, 'hands': {'R': 'grip', 'L': 'grip'},
            'bend': {'spine': [0.25 + 0.1 * (j % 2), 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'clench' if j % 2 else 'line', 'brow': -0.3}}, toonDur=0.25) for j in range(8)]
st.shot('S10', 'gym', actors=[act(w, p, ry, 'stand', 'neutral', keys=SHOVEL_K(p, ry, 0.1 * i)) for i, (w, p, ry) in enumerate(OFFS10)],
        props=[P('mer10', 'ballotSea', pos=[0, 0, 0.5], opts={'w': 14, 'd': 12, 'h': 0.95, 'n': 1100}),
               *[P(f'pelle10{i}', 'snowShovel', on={'actor': w, 'hand': 'R', 'offset': [0.0, -0.05, 0.03], 'rot': [0.6, 0, 0]}, opts={'len': 1.0}) for i, (w, p, ry) in enumerate(OFFS10)]],
        cams=[C10])
st.cue('sfx:paper', 'S10', 0.15, 0.35); st.cue('sfx:paper', 'S10', 0.6, 0.35); st.cue('sfx:paper', 'S10', 1.1, 0.35)

# 11: a whole forest. A hillside of fresh stumps to the top; in front, a log truck marked BULLETINS takes the last log; a gendarme with a chainsaw in
#     his left hand salutes beside it
D11 = st.dur('S11'); LOAD11 = 0.15
TRUCK11 = [1.0, 0, -1.6]
GEN11 = [2.3, 0, 1.5]; RYG11 = -12
C11 = cam(0.0, [1.3, 1.5, 9.2], [1.25, 1.52, 8.9], [0.6, 2.6, -6.0], [0.6, 2.65, -6.0], lens=44)
chk('S11', C11['from'], C11['lookAt'], 44, {'genFace': [GEN11[0], 2.0, GEN11[2]], 'label': [TRUCK11[0] - 0.9, 2.6, TRUCK11[2] + 1.27], 'hillTop': [0, 9.0, -44.0], 'cab': [3.1, 2.2, TRUCK11[2]], 'logTop': [-0.9, 2.6, TRUCK11[2]]})
st.shot('S11', 'grassland', setOpts={'clouds': 30}, actors=[
        act('gendarme3', GEN11, RYG11, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': SALUTE(GEN11, RYG11)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
            *blink(1.0, {'lid': 0.4, 'mouth': 'line', 'brow': -0.3})])],
        props=[P('colline11', 'stumpField', pos=[0, 0, -4.0], opts={'w': 70, 'd': 46, 'rise': 10}), P('camion11', 'logTruck', pos=TRUCK11, opts={'loadAt': LOAD11, 'side': 1}),
               P('tronconneuse11', 'chainsaw', on={'actor': 'gendarme3', 'hand': 'L', 'offset': [0.0, -0.1, 0.05]}), KEPI('kepi11', 'gendarme3')],
        cams=[C11])
st.cue('sfx:chainsaw', 'S11', 0.0, 0.18); st.cue('thud', 'S11', r(LOAD11 + 0.62), 0.5)

# ============================== the polling station (the town-hall room): a table with the OUI box (left) and the NON box (right), seen from the
# voters' far side: they stand behind the table facing us and reach over the boxes
TAB = [0.0, 0, -0.9]; BOXY = 0.76
OUI = [-0.36, BOXY, -0.9]; NON = [0.36, BOXY, -0.9]
SLOT = lambda b: [b[0], r(b[1] + 0.72), b[2]]
VOTE = {'title': 'BUREAU DE VOTE', 'desk': False, 'map': False, 'clockX': 0.9}
def POLL_PROPS(fill_non, fill_oui=None):
    return [P('table', 'table', pos=TAB, opts={'w': 1.6, 'd': 0.7, 'h': BOXY, 'color': '#8A6A45', 'legs': '#5A3A28'}),
            P('urneOui', 'ballotBox', pos=OUI, opts={'text': 'OUI', 'fill': fill_oui or []}), P('urneNon', 'ballotBox', pos=NON, opts={'text': 'NON', 'fill': fill_non})]

# 12: the ballots all voted no. Across the table: three voters behind it hold their ballots up over the OUI box; one after the other the ballots
#     wriggle out of their fingers, hop over and dive into the NON box, which fills; the OUI box stays empty
D12 = st.dur('S12')
VOT12 = [('electeur1', [-0.5, 0, -1.7], 10), ('electeur2', [-0.95, 0, -2.25], 20), ('electeur3', [0.45, 0, -1.8], -15)]
HOLD12 = [[-0.32, 1.72, -0.95], [-0.55, 1.7, -1.4], [0.08, 1.7, -1.2]]
T12 = [0.15, 0.55, 0.95]
C12 = cam(0.0, [0.25, 1.85, 2.5], [0.24, 1.86, 2.3], [-0.15, 1.5, -1.3], [-0.15, 1.5, -1.3], lens=44)
chk('S12', C12['from'], C12['lookAt'], 44, {**{w: [p[0], 2.0, p[2]] for w, p, ry in VOT12}, 'oui': [OUI[0], 1.2, OUI[2] + 0.31], 'non': [NON[0], 1.2, NON[2] + 0.31], 'hold1': HOLD12[0]})
def VOTER_K(i, w, p, ry):
    h = HOLD12[i]; hand = 'R' if h[0] < p[0] else 'L'
    return [k(0.0, look=SLOT(OUI)), k(0.0, toon={'reach': {hand: R5(h, 1, 0.06)}, 'hands': {hand: 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.0}}, toonDur=0.0),
            k(r(T12[i] + 0.3), toon={'reach': {hand: R5(add(h, [0, 0.03, 0]), 1, 0.06)}, 'hands': {hand: 'open'}, 'face': {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.08),
            k(r(T12[i] + 0.45), look=SLOT(NON), lookDur=0.15)]
st.shot('S12', 'mairie', setOpts=VOTE, actors=[act(w, p, ry, 'stand', 'neutral', keys=VOTER_K(i, w, p, ry)) for i, (w, p, ry) in enumerate(VOT12)],
        props=[*POLL_PROPS([[r(T12[0] + 0.85), 1], [r(T12[1] + 0.85), 2], [r(T12[2] + 0.85), 3], [r(T12[2] + 1.0), 6]]),
               P('bulletins12', 'divingBallots', pos=[0, 0, 0], opts={'drops': [{'from': HOLD12[i], 'to': SLOT(NON), 't0': T12[i], 'dur': 0.5, 'hold': 0.3, 'arc': 0.45, 'spin': 1 if i % 2 else -1} for i in range(3)]})],
        cams=[C12])
for t_ in T12: st.cue('whoosh', 'S12', r(t_ + 0.3), 0.15, 0.3, 900, 3500); st.cue('sfx:paper', 'S12', r(t_ + 0.78), 0.3)

# 13: his first. Close on the boxes, the town-hall clock at eight behind: he holds his ballot over the OUI box (left hand, the plastered finger
#     raised well away); it twists out of his fingers and is the first into the NON box
D13 = st.dur('S13'); T13 = 0.1
HERO13 = [-0.15, 0, -1.65]
HOLD13 = [-0.3, 1.72, -0.98]
C13 = cam(0.0, [0.05, 1.8, 1.5], [0.05, 1.8, 1.42], [-0.02, 1.45, -1.2], [-0.02, 1.45, -1.2], lens=52)
chk('S13', C13['from'], C13['lookAt'], 46, {'face': [HERO13[0], 2.0, HERO13[2]], 'oui': [OUI[0], 1.15, OUI[2] + 0.31], 'non': [NON[0], 1.15, NON[2] + 0.31], 'hold': HOLD13, 'clock': [0.6, 2.55, -2.57]})
st.shot('S13', 'mairie', setOpts=VOTE, actors=[
        act('mec', HERO13, 0, 'stand', 'neutral', keys=[k(0.0, look=SLOT(OUI)),
            k(0.0, toon={'reach': {'L': R5(HOLD13, 1, 0.06), 'R': R5(off(HERO13, 0, 0.3, 0.35, 1.85))}, 'hands': {'L': 'pinch', 'R': 'point'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.0),
            k(r(T13 + 0.3), toon={'reach': {'L': R5(add(HOLD13, [0, 0.03, 0]), 1, 0.06), 'R': R5(off(HERO13, 0, 0.3, 0.35, 1.85))}, 'hands': {'L': 'open', 'R': 'point'}, 'face': {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.07),
            k(r(T13 + 0.45), look=SLOT(NON), lookDur=0.12), k(r(T13 + 0.85), look='camera', lookDur=0.15)])],
        props=[*POLL_PROPS([[r(T13 + 0.78), 1]]), P('horloge13', 'wallClock', pos=[0.6, 2.55, -2.55], opts={'rate': 0, 'hours': 8}), PLASTER('pansement13'),
               P('bulletin13', 'divingBallots', pos=[0, 0, 0], opts={'drops': [{'from': HOLD13, 'to': SLOT(NON), 't0': T13, 'dur': 0.42, 'hold': 0.3, 'arc': 0.35, 'spin': 1}]})],
        cams=[C13])
st.cue('whoosh', 'S13', r(T13 + 0.3), 0.18, 0.3, 900, 3500); st.cue('sfx:paper', 'S13', r(T13 + 0.72), 0.35)

# 14: the shredder was abolished. Back on the forecourt: two ushers throw the velvet cover back over the shredder and wheel the trolley away; between
#     the gendarmes the sheet stops trembling and uncurls (ABOLIE)
D14 = st.dur('S14'); ON14 = 0.12; GO14 = 0.42
HUI = [('huissier1', [0.35, 0, 1.55], 120), ('huissier2', [1.15, 0, 0.6], -110)]
TROL14b = [2.6, 0, 0.4]
C14 = cam(0.0, [1.4, 1.1, 6.6], [1.35, 1.11, 6.3], [-0.05, 1.9, 0.6], [0.1, 1.91, 0.6], lens=42)
chk('S14', C14['from'], C14['lookAt'], 42, {'sheetTop': CORNER(-1), 'g1Face': [G1[0], 2.0, G1[2]], 'g2Face': [G2[0], 2.0, G2[2]], 'h1Face': [HUI[0][1][0], 2.0, HUI[0][1][2]], 'trolEnd': [TROL14b[0], 1.4, TROL14b[2]]})
GK14 = GKEYS({'lid': 0.5, 'mouth': 'line', 'brow': -0.2})
st.shot('S14', 'grassland', setOpts={'clouds': 26}, actors=[
        act('gendarme1', G1, 0, 'stand', 'neutral', keys=GK14['g1']), act('gendarme2', G2, 0, 'stand', 'neutral', keys=GK14['g2']),
        *[act(w, p, ry, 'stand', 'neutral', keys=[k(0.0, look=[TROL[0], 1.5, TROL[2]]),
            k(0.0, toon={'reach': {'R': R5(add(TROL, [0.0, 1.9, 0.0])), 'L': R5(add(TROL, [0.1, 1.9, 0.2]))}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            k(ON14, toon={'reach': {'R': R5(add(TROL, [0.0, 1.3, 0.2])), 'L': R5(add(TROL, [0.1, 1.3, 0.3]))}, 'hands': {'R': 'open', 'L': 'open'}}, toonDur=0.12),
            k(GO14, to=add(TROL14b, [p[0] - TROL[0], 0, p[2] - TROL[2]]), dur=1.2, clip='walk', ease='inOut'),
            k(GO14, toon={'reach': {'R': R5(off(p, ry, 0.45, 0.2, 0.95)), 'L': R5(off(p, ry, 0.45, -0.2, 0.95))}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.15)]) for w, p, ry in HUI]],
        props=[*COURT(), P('chariot14', 'shredderTrolley', pos=TROL, ry=-20, opts={'covered': False, 'onAt': ON14}, keys=[k(GO14, to=TROL14b, dur=1.2, ease='inOut')]),
               P('micros14', 'micCluster', pos=MICS, ry=180, opts={}),
               P('feuille14', 'feuilleSheet', pos=SHEET_C, opts={**SHC, 'curl': [[0.0, 0.32], [0.85, 0.0]], 'tremble': [[0.0, 1.0], [0.85, 0.0]]}),
               KEPI('kepi14a', 'gendarme1'), KEPI('kepi14b', 'gendarme2')],
        cams=[C14])
st.card('S14', 'ABOLIE', at=0.95)
st.cue('whoosh', 'S14', ON14, 0.3, 0.25, 400, 2000); st.cue('sfx:rattle', 'S14', GO14, 0.25)

# 15: the gendarmes flattened every shredder. Low on a vast square: a gendarme drives a steamroller with a big red bow along a row of price-tagged
#     shredders, flattening them one by one like biscuits with puffs of confetti; rows already flat behind; a line of gendarmes salutes
D15 = st.dur('S15')
ROLL0, ROLL1 = [-5.5, 0.03, 0.0], [2.0, 0.03, 0.0]
SPD15 = r((ROLL1[0] - ROLL0[0]) / D15, 3)
C15 = cam(0.0, [8.2, 1.25, 2.9], [8.0, 1.27, 2.85], [-1.5, 1.5, -0.4], [-0.5, 1.55, -0.4], lens=44)
LINE15 = [(f'garde{i}', [r(-6.0 + 1.5 * i), 0.03, -1.8]) for i in range(5)]
chk('S15', C15['from'], C15['lookAt'], 40, {'rollerStart': [ROLL0[0] + 2.0, 1.5, 0], 'rollerEnd': [ROLL1[0] + 2.0, 1.5, 0], 'driverEnd': [ROLL1[0] - 0.7, 3.4, 0], 'row0': [-4.0, 0.6, 0.0], 'row6': [5.0, 0.6, 0.0], **{w: [p[0], 2.0, p[2]] for w, p in LINE15[1:4]}})
st.shot('S15', 'grassland', setOpts={'clouds': 30}, actors=[
        act('chauffeur', [ROLL0[0] - 0.7, 1.45, 0.0], 90, 'drive', 'neutral', keys=[k(0.0, to=[ROLL1[0] - 0.7, 1.45, 0.0], dur=D15, ease='linear', face='keep', clip='drive'), k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': SALUTE([ROLL0[0] - 0.7, 0.0, 0.0], 90)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0)]),
        *[act(w, p, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': SALUTE(p, 0)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0), *blink(r(0.5 + 0.37 * i), {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}), k(r(1.0 + 0.2 * i), look=[ROLL1[0], 1.8, 0.0], lookDur=0.3)]) for i, (w, p) in enumerate(LINE15)]],
        props=[P('place15', 'parkLot', pos=[0, 0, -4.0], opts={'w': 70, 'd': 50, 'rows': [], 'color': '#CFC8B8', 'y': 0.03}),
               P('rouleau15', 'steamroller', pos=ROLL0, ry=0, keys=[k(0.0, to=ROLL1, dur=D15, ease='linear')]),
               P('rangees15', 'shredderRows', pos=[0, 0, 0], opts={'rows': [[0.0, -3.0, 8, 1.4], [-2.0, -6.0, 10, 1.5]], 'at': 0.0, 'x0': ROLL0[0] + 2.25, 'speed': SPD15, 'rollZ0': -0.5, 'rollZ1': 0.5, 'y': 0.03, 's': 0.85}),
               P('aplaties15', 'shredderRows', pos=[0, 0, 0], opts={'rows': [[2.2, -7.0, 10, 1.5]], 'y': 0.03, 's': 0.85, 'speed': 1e9, 'at': -10, 'x0': -1e9}),
               KEPI('kepi15', 'chauffeur'), *[KEPI(f'kepi15{i}', w) for i, (w, p) in enumerate(LINE15)]],
        cams=[C15])
st.cue('engine', 'S15', 0.0, 0.3, D15); st.cue('sfx:crunch', 'S15', 0.4, 0.3); st.cue('sfx:crunch', 'S15', 0.75, 0.3); st.cue('sfx:crunch', 'S15', 1.1, 0.3); st.cue('sfx:crunch', 'S15', 1.45, 0.3); st.cue('sfx:crunch', 'S15', 1.8, 0.3)

# 16: the sheet was released. On the forecourt: one gendarme opens his fingers and the sheet drifts away on a draught, down past the microphones and
#     out over the steps, rocking
D16 = st.dur('S16'); REL16 = 0.25
G16 = [-0.15, 0, 0.75]
SH16 = [0.45, 1.85, 0.85]
PATH16 = [[0.6, 1.95, 1.45], [0.7, 1.65, 2.3], [0.85, 1.8, 3.2], [1.3, 1.4, 4.4]]
C16 = cam(0.0, [-1.0, 1.6, 5.3], [-0.95, 1.61, 5.1], [0.35, 1.7, 1.0], [0.55, 1.66, 1.6], lens=44)
chk('S16', C16['from'], C16['lookAt'], 44, {'gFace': [G16[0], 2.0, G16[2]], 'sheet0': SH16, 'p1': PATH16[0], 'p2': PATH16[1], 'p3': PATH16[2], 'mics': [MICS[0], 1.35, MICS[2]]})
st.shot('S16', 'grassland', setOpts={'clouds': 26}, actors=[
        act('gendarme2', G16, 0, 'stand', 'neutral', keys=[k(0.0, look=SH16), k(0.0, toon={'reach': {'L': R5(add(SH16, [-0.18, 0.3, -0.02]), 1, 0.06)}, 'hands': {'L': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(REL16, toon={'reach': {'L': R5(add(SH16, [-0.18, 0.32, -0.02]), 1, 0.06)}, 'hands': {'L': 'open'}}, toonDur=0.08), k(r(REL16 + 0.3), look=PATH16[1], lookDur=0.3), k(1.1, look='camera', lookDur=0.2)])],
        props=[*COURT(), P('micros16', 'micCluster', pos=MICS, ry=180, opts={}), KEPI('kepi16', 'gendarme2'),
               P('feuille16', 'feuilleSheet', pos=SH16, rot=[0, -0.2, 0], opts={**SHC, 'wiggle': [[REL16, 0.8]]}, keys=[k(REL16, path=PATH16, dur=1.3, ease='inOut'), k(REL16, rotTo=[0.3, 0.6, -0.4], dur=1.3, ease='inOut')])],
        cams=[C16])
st.cue('gust', 'S16', REL16, 0.35, 1.2)

# 17: turned into a dismissal letter. The shop's back office, by a bare paper shelf: the manager's typewriter hammers LICENCIEMENT across her, the
#     dog-ear and the tiny red smear beside the word
D17 = st.dur('S17'); TYPE17 = 0.2
DESK17 = [2.6, 0, -1.7]; TW17 = [2.6, 0.76, -1.62]
SHT17 = [2.6, 1.32, -1.86]
MAN17 = [2.6, 0, -2.55]
C17 = cam(0.0, [2.2, 1.75, 0.0], [2.22, 1.74, -0.1], [2.62, 1.3, -1.9], [2.62, 1.3, -1.9], lens=50)
chk('S17', C17['from'], C17['lookAt'], 50, {'sheetTop': [SHT17[0], 1.6, SHT17[2]], 'sheetMid': SHT17, 'keys': [TW17[0], 0.98, TW17[2] + 0.12], 'manFace': [MAN17[0], 2.0, MAN17[2]], 'shelf': [3.7, 1.2, -2.45]})
st.shot('S17', 'office', setOpts=SHOP, actors=[
        act('gerant', MAN17, 0, 'stand', 'neutral', keys=[k(0.0, look=[TW17[0], 1.0, TW17[2]])] + [k(r(TYPE17 + 0.09 * j), toon={'reach': {'R': R5([TW17[0] - 0.12 + 0.06 * (j % 3), 1.0 + 0.04 * (j % 2), TW17[2] + 0.1]), 'L': R5([TW17[0] + 0.12 - 0.05 * (j % 2), 1.0 + 0.04 * ((j + 1) % 2), TW17[2] + 0.1])},
            'hands': {'R': 'point', 'L': 'point'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.05) for j in range(14)]),
        ],
        props=[P('bureau17', 'table', pos=DESK17, opts={'w': 1.3, 'd': 0.75, 'h': 0.76, 'color': '#7A5A3C', 'legs': '#4A3424'}),
               P('machine17', 'typewriter', pos=TW17, opts={'hitFrom': TYPE17, 'hitTo': r(TYPE17 + 1.25)}),
               P('lettre17', 'feuilleSheet', pos=SHT17, rot=[-0.22, 0, 0], opts={**SHEET, 'text': 'LICENCIEMENT', 'typeAt': TYPE17, 'typeDur': 1.2}),
               P('etagere17', 'bareShelf', pos=[3.75, 0, -2.5], ry=-15)],
        cams=[C17])
for j in range(12): st.cue('clack', 'S17', r(TYPE17 + 0.1 * j), 0.12)
st.cue('sfx:bell', 'S17', r(TYPE17 + 1.28), 0.25)

# 18: addressed to this man. From the manager's side across the counter: the manager slides her, folded in three, toward him; he takes her at
#     arm's length by the far edge with his left hand, the plastered finger of the right lifted well away
D18 = st.dur('S18'); SLIDE18 = 0.1; TAKE18 = 0.7
MAN18 = [0.75, 0, 0.5]; RYM18 = 200
L18a = [0.25, r(TOP + 0.01), -0.12]; L18b = [0.05, r(TOP + 0.01), -0.52]
C18 = cam(0.0, [0.3, 1.8, 1.35], [0.29, 1.8, 1.25], [-0.08, 1.45, -1.0], [-0.08, 1.46, -1.0], lens=48)
chk('S18', C18['from'], C18['lookAt'], 44, {'heroFace': [HERO[0], 2.0, HERO[2]], 'letterB': L18b, 'manHead': [MAN18[0], 2.0, MAN18[2]], 'heroFinger': off(HERO, 0, 0.35, 0.45, 1.85)})
st.shot('S18', 'office', setOpts=SHOP, actors=[
        act('gerant', MAN18, RYM18, 'stand', 'neutral', keys=[k(0.0, look=[HERO[0], 2.0, HERO[2]]), k(0.0, toon={'reach': {'R': R5(add(L18a, [0, 0.05, 0.06]))}, 'hands': {'R': 'open'}}, toonDur=0.0),
            k(SLIDE18, toon={'reach': {'R': R5(add(L18b, [0.05, 0.05, 0.15]))}, 'hands': {'R': 'open'}}, toonDur=0.4)]),
        act('mec', HERO, 0, 'stand', 'unimpressed', keys=[k(0.0, look=L18b),
            k(0.0, toon={'reach': {'R': R5(off(HERO, 0, 0.35, 0.45, 1.85)), 'L': R5(off(HERO, 0, 0.25, -0.3, 1.0))}, 'hands': {'R': 'point', 'L': 'rest'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
            k(r(TAKE18 - 0.15), toon={'reach': {'R': R5(off(HERO, 0, 0.35, 0.5, 1.9)), 'L': R5(add(L18b, [0.12, 0.04, 0.02]), 1, 0.1)}, 'hands': {'R': 'point', 'L': 'pinch'}, 'bend': {'spine': [-0.08, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.15),
            k(r(TAKE18 + 0.3), look='camera', lookDur=0.2)])],
        props=[*SHOP_PROPS(), PLASTER('pansement18'),
               P('lettre18', 'feuilleSheet', pos=L18a, rot=[-PI / 2, 0, 0.1], opts={**SHEET, 'folded': True}, keys=[k(SLIDE18, to=L18b, dur=0.42, ease='out')])],
        cams=[C18])
st.cue('sfx:paper', 'S18', SLIDE18, 0.35); st.cue('sfx:paper', 'S18', TAKE18, 0.3)

# 19: he sold shredders. Exactly the framing of shot 1: the demo shredder is gone, only its price tag lies on the plinth, the wall behind is bare;
#     he holds the unfolded letter up to us in his left hand (LICENCIEMENT, the dog-ear, the tiny smear), the plastered finger raised away; a beat
D19 = st.dur('S19')
LET19 = [0.22, 1.42, -0.5]
chk('S19', C1['from'], C1['lookAt'], 42, {'face': [HERO[0], 2.0, HERO[2]], 'letterTop': [LET19[0], 1.7, LET19[2]], 'letterMid': LET19, 'plinthTag': [DEMO[0], 0.34, DEMO[2]], 'finger': off(HERO, 0, 0.32, 0.28, 1.95)})
st.shot('S19', 'office', setOpts=SHOP, actors=[
        act('mec', HERO, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': R5([LET19[0] + 0.19, 1.66, LET19[2] + 0.04], 1, 0.06), 'R': R5(off(HERO, 0, 0.32, 0.28, 1.95))}, 'hands': {'L': 'pinch', 'R': 'point'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.15}}, toonDur=0.0),
            *blink(1.2, {'lid': 0.45, 'mouth': 'line', 'brow': -0.15}), k(1.7, toon={'face': {'lid': 0.5, 'mouth': 'flat', 'brow': -0.25}}, toonDur=0.3, keepPose=True)])],
        props=[*SHOP_PROPS(empty=True, demo=False), PLASTER('pansement19'),
               P('lettre19', 'feuilleSheet', pos=LET19, rot=[0, -0.08, 0.04], opts={**SHEET, 'text': 'LICENCIEMENT'})],
        cams=[C1])
st.text('S19', 1.2, 'lettre19', 'LICENCIEMENT')
st.cue('sfx:paper', 'S19', 0.1, 0.25)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
SUITS = ['#3A3D44', '#5A4A3A', '#2E4563']
st.write("La feuille", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'policier': {'preset': 'cop', 'seed': 960, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'officier': {'preset': 'cop2', 'seed': 961, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'stagiaire': {'outfit': 'suit', 'suit': '#6E8CA8', 'pants': '#4A5E74', 'tie': '#2E4563', 'lapel': '#5E7A96', 'hair': 'crew', 'hairColor': '#4A3424', 'facial': 'stubble', 'glasses': True, 'seed': 962,
                  'build': {'width': 0.92, 'headWidth': 1.2}, 'toon': EX},
    'directeur': {'preset': 'boss', 'seed': 963, 'suit': '#2E3A4E', 'tie': '#C8A030', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'procureur': {'preset': 'avocat', 'seed': 964, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'gendarme1': {**GEND, 'seed': 965}, 'gendarme2': {**GEND, 'seed': 966, 'facial': 'mustache'}, 'gendarme3': {**GEND, 'seed': 967},
    'chauffeur': {**GEND, 'seed': 968, 'facial': 'mustache'},
    **{f'garde{i}': {**GEND, 'seed': 970 + i} for i in range(5)},
    'president': {'preset': 'politique', 'seed': 975, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'hairColor': '#BDBDBD', 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12,
                  'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'officiel{i + 1}': {'preset': 'prefet', 'seed': 976 + i, 'suit': SUITS[i], 'lapel': SUITS[i], 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for i in range(3)},
    'electeur1': {'preset': 'madame', 'seed': 980, 'suit': '#2E7D4F', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'electeur2': {'preset': 'worker', 'seed': 981, 'hat': 'none', 'suit': '#1F4E8C', 'pants': '#22324A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'electeur3': {'preset': 'mamie', 'seed': 982, 'suit': '#7A2E4E', 'lapel': '#5A1E38', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'huissier1': {'outfit': 'suit', 'suit': '#1B1B1E', 'pants': '#1B1B1E', 'tie': '#C9CDD3', 'lapel': '#1B1B1E', 'hair': 'receding', 'facial': 'none', 'seed': 983, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'huissier2': {'outfit': 'suit', 'suit': '#1B1B1E', 'pants': '#1B1B1E', 'tie': '#C9CDD3', 'lapel': '#1B1B1E', 'hair': 'slick', 'facial': 'mustache', 'seed': 984, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'gerant': {'preset': 'boss', 'seed': 985, 'suit': '#3A3D44', 'tie': '#7A2333', 'facial': 'mustache', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
})
