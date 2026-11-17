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
GEND = {'preset': 'cop', 'outfit': 'suit', 'suit': '#1E2A44', 'pants': '#1A2438', 'shirt': '#D9DEE8', 'lapel': '#141C30', 'tie': '#141C30', 'cuff': '#1E2A44', 'hat': 'none', 'hair': 'crew', 'facial': 'none',
        'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
def KEPI(pid, who): return P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#1A2438', 'band': '#C9CDD3'})
SALUTE = lambda p, ry: R5(off(p, ry, 0.08, 0.2, 2.02), 1, 0.03)
STREET = {'clouds': 0}   # (round 1) no clouds: in the street shots they read as floating beige slabs

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
    ps.append(P('demo', 'demoShredder', pos=DEMO, ry=-12, opts={'plinth': True, 'ph': PH}) if demo else P('socle', 'emptyPlinth', pos=DEMO, ry=-12, opts={'ph': PH, 'color': '#5A4632', 'dust': '#6E5A44', 'tagS': 3.0, 'tagUp': True, 'tagX': 0.22}))
    return ps
C1 = cam(0.0, [0.2, 2.45, 2.3], [0.19, 2.43, 2.15], [0.18, 1.36, -0.9], [0.18, 1.37, -0.9], lens=44)

# 1: the hook. Medium close-up across the counter: he is frozen over his raised right index finger, a thin red line on it, eyes wide on it; the
#    sheet lies on the counter at his left, dog-ear and tiny red smear; behind him the demo shredder with its price tag and the wall of boxes
D1 = st.dur('S01')
SH1 = [0.33, r(TOP + 0.004), -0.42]
FING1 = R5(off(HERO, 0, 0.5, 0.08, 1.78), 1, 0.06)
chk('S01', C1['from'], C1['lookAt'], 44, {'face': [HERO[0], 2.0, HERO[2]], 'finger': FING1[:3], 'sheet': SH1, 'demoTag': [DEMO[0] + 0.24, 1.6, DEMO[2] + 0.2], 'wallTop': [0, 2.6, WALL[2]]})
SHOCK = {'lid': 0.0, 'pop': 0.35, 'mouth': 'O', 'brow': 0.7}
# (round 1) the take is a rig take, not only an eye-pop: a squint and a sink (anticipation), the head shoots up 30 % taller and thinner with the
#            eyes out, a squash settle with a wobble, then the frozen stare on the finger with a breath, a blink and a deadpan glance to us
FROZEN = {'lid': 0.25, 'pop': 0.12, 'mouth': 'O', 'brow': 0.55}
st.shot('S01', 'office', setOpts=SHOP, actors=[
        act('mec', HERO, 0, 'stand', 'neutral', keys=[k(0.0, look=FING1[:3]),
            k(0.0, toon={'reach': {'R': FING1}, 'hands': {'R': 'point'}, 'face': {'lid': 0.15, 'mouth': 'line', 'brow': 0.2}, 'sq': [1, 1, 1], 'scl': {'head': [1, 1, 1]}}, toonDur=0.0),
            k(0.22, toon={'reach': {'R': FING1}, 'hands': {'R': 'point'}, 'face': {'lid': 0.55, 'mouth': 'line', 'brow': -0.2}, 'sq': [1.05, 0.93, 1.05], 'scl': {'head': [1.08, 0.9, 1.0]}}, toonDur=0.1, toonEase='inOut'),
            k(0.34, toon={'reach': {'R': R5(add(FING1[:3], [0, 0.03, 0.03]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': {**SHOCK, 'pop': 0.5}, 'sq': [0.93, 1.09, 0.93], 'scl': {'head': [0.82, 1.3, 1.0]}}, toonDur=0.07, toonEase='out'),
            k(0.5, toon={'reach': {'R': R5(add(FING1[:3], [0, 0.03, 0.03]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': SHOCK, 'sq': [1.04, 0.95, 1.04], 'scl': {'head': [1.12, 0.86, 1.0]}}, toonDur=0.08, toonEase='out'),
            k(0.62, toon={'reach': {'R': R5(add(FING1[:3], [0, 0.03, 0.03]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': SHOCK, 'sq': [0.99, 1.02, 0.99], 'scl': {'head': [0.95, 1.06, 1.0]}}, toonDur=0.07),
            k(0.74, toon={'reach': {'R': R5(add(FING1[:3], [0, 0.03, 0.03]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': FROZEN, 'sq': [1, 1, 1], 'scl': {'head': [1, 1, 1]}}, toonDur=0.1),
            *[k(r(0.86 + 0.12 * i), toon={'reach': {'R': R5(add(FING1[:3], [0.006 * (1 if i % 2 else -1), 0.03 + 0.008 * (i % 2), 0.03]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': FROZEN, 'sq': [1 + 0.012 * (i % 2), 1 - 0.015 * (i % 2), 1 + 0.012 * (i % 2)]}, toonDur=0.1) for i in range(5)],
            k(1.4, look='camera', lookDur=0.12), k(1.4, toon={'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.12, keepPose=True), *blink(1.62, {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}),
            k(1.85, look=FING1[:3], lookDur=0.12), k(1.85, toon={'face': FROZEN}, toonDur=0.1, keepPose=True)])],
        props=[*SHOP_PROPS(), P('feuille1', 'feuilleSheet', pos=SH1, rot=[-PI / 2, 0, 0.35], opts={**SHEET, 'smearS': 1.4}), CUT('coupure1')],
        cams=[C1])
st.cue('sfx:paper', 'S01', 0.05, 0.4); st.cue('sfx:gasp', 'S01', 0.35, 0.25); st.cue('sfx:heartbeat', 'S01', 0.8, 0.15)

# 2: she melted into the crowd. Over the counter, high three-quarter: the sheet lifts her dog-ear toward the demo shredder, flips smear down and
#    slides herself into the open ream lying on the counter, gone among the identical edges; his plastered finger hovers over the stack, lost
D2 = st.dur('S02')
STACK2 = [-0.2, TOP, -0.6]; SH2 = [0.34, r(TOP + 0.004), -0.55]
C2 = cam(0.0, [0.25, 2.3, 1.6], [0.24, 2.29, 1.5], [0.1, 1.5, -0.9], [0.1, 1.5, -0.9], lens=56)   # (round 1) wider and lower: his head, the counter and the shredder
HOV2 = R5([STACK2[0] + 0.04, 1.62, STACK2[2] + 0.04], 1, 0.06)
UP2 = R5(off(HERO, 0, 0.42, 0.2, 1.85), 1, 0.06)                     # his hand up by his face, the finger raised, well away from the counter
chk('S02', C2['from'], C2['lookAt'], 56, {'stack': add(STACK2, [0, 0.1, 0]), 'sheet': SH2, 'finger': HOV2[:3], 'up': UP2[:3], 'headTop': [HERO[0], 2.38, HERO[2]], 'demo': [DEMO[0], 1.6, DEMO[2]]})
TILT2, FLIP2, EDGE2, SLIDE2 = 0.12, 0.48, 0.66, 0.78
SIDE2 = [r(STACK2[0] + 0.5), r(TOP + 0.09), STACK2[2]]
st.shot('S02', 'office', setOpts=SHOP, actors=[
        act('mec', HERO, 0, 'stand', 'neutral', keys=[k(0.0, look=SH2),
            k(0.0, toon={'reach': {'R': UP2}, 'hands': {'R': 'point'}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
            k(TILT2, look=[DEMO[0], 1.5, DEMO[2]], lookDur=0.15), k(r(FLIP2 - 0.05), look=SH2, lookDur=0.1),
            k(r(SLIDE2 + 0.1), look=add(STACK2, [0, 0.15, 0]), lookDur=0.12),
            k(r(SLIDE2 + 0.3), toon={'reach': {'R': HOV2}, 'hands': {'R': 'point'}, 'face': {'lid': 0.15, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.2, toonEase='out'),
            *[k(r(SLIDE2 + 0.52 + 0.14 * i), toon={'reach': {'R': R5(add(HOV2[:3], [0.07 * (i % 2 * 2 - 1), 0.02 * (i % 2), 0.03 * (i % 2)]), 1, 0.06)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.25, 'mouth': 'wavy' if i % 2 else 'line', 'brow': 0.7}}, toonDur=0.11) for i in range(4)]])],
        props=[*SHOP_PROPS(), P('rame2', 'sheetStack', pos=STACK2, ry=0, opts={'riffleAt': r(SLIDE2 + 0.16)}), PLASTER('pansement2'),
               P('feuille2', 'feuilleSheet', pos=SH2, rot=[-PI / 2, 0, 0.35], opts={**SHEET, 'smearS': 1.4, 'earKeys': [[TILT2, 0.2], [r(TILT2 + 0.12), 0.45], [r(TILT2 + 0.2), 0.25], [FLIP2, 0.9]]},
                 keys=[k(TILT2, rotTo=[-PI / 2 + 0.55, -0.35, 0.75], dur=0.18, ease='out'), k(FLIP2, rotTo=[PI / 2, 0, 0], dur=0.16, ease='inOut'),
                       k(FLIP2, to=add(SIDE2, [0.12, 0.12, 0.0]), dur=0.16, ease='out'), k(EDGE2, to=SIDE2, dur=0.1, ease='in'),
                       k(SLIDE2, to=[STACK2[0], SIDE2[1], STACK2[2]], dur=0.3, ease='inOut'), k(r(SLIDE2 + 0.31), visible=False)])],
        cams=[C2])
st.cue('whoosh', 'S02', TILT2, 0.15, 0.25, 900, 3000); st.cue('sfx:paper', 'S02', FLIP2, 0.4); st.cue('sfx:zip', 'S02', SLIDE2, 0.35)

# ============================== the street (parisStreet): the road along Z (x -5..5), the right pavement x 5..10, the house fronts at x 10.2
# 3: description: white, rectangular. Low on the pavement: a policeman slaps a RECHERCHÉE poster (a blank white rectangle where the face should be)
#    on the nearest lamppost, the same poster already on every lamppost down the street; he walks beside him holding up his plastered finger
D3 = st.dur('S03'); SLAP3 = 0.55
LAMPS = [[5.7, z] for z in (1.6, -3.0, -7.6, -12.2, -16.8, -21.4)]   # (round 2) closer spacing: a poster on every lamppost reads down the street
COP3 = [6.25, 0, 1.25]; RYC3 = -90
HERO3a, HERO3b = [7.1, 0, -2.4], [7.1, 0, 0.6]
C3 = cam(0.0, [6.4, 1.8, 7.6], [6.4, 1.8, 7.3], [6.4, 1.3, -2.0], [6.4, 1.31, -2.0], lens=44)   # (round 1) closer, centred between the poster and the hero
POST = lambda z: [5.7, 1.85, r(z + 0.11)]
chk('S03', C3['from'], C3['lookAt'], 44, {'poster1': POST(1.6), 'poster2': POST(-5.0), 'poster3': POST(-11.6), 'copFace': [COP3[0], 2.0, COP3[2]], 'heroA': [HERO3a[0], 2.0, HERO3a[2]], 'heroB': [HERO3b[0], 2.0, HERO3b[2]], 'heroFeetB': HERO3b})
FING3 = lambda p: R5(off(p, 0, 0.42, 0.22, 2.05), 1, 0.06)
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('policier', COP3, RYC3, 'stand', 'neutral', keys=[k(0.0, look=POST(1.6)),
            k(0.0, toon={'reach': {'L': R5(add(POST(1.6), [0.45, -0.1, 0.25]))}, 'hands': {'L': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(r(SLAP3 - 0.3), toon={'reach': {'L': R5(add(POST(1.6), [0.75, 0.35, 0.5]))}, 'hands': {'L': 'open'}, 'sq': [0.96, 1.05, 0.96], 'bend': {'spine': [-0.12, 0.25, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.5}}, toonDur=0.22, toonEase='inOut'),
            k(SLAP3, toon={'reach': {'L': R5(add(POST(1.6), [0.03, 0, 0.03]), 1, 0.08)}, 'hands': {'L': 'open'}, 'sq': [1.06, 0.94, 1.06], 'bend': {'spine': [0.1, -0.2, 0, 1, None]}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.05, toonEase='in'),
            k(r(SLAP3 + 0.45), toon={'reach': {'L': R5(add(POST(1.6), [0.4, -0.5, 0.25]))}, 'hands': {'L': 'rest'}, 'sq': [1, 1, 1], 'bend': {'spine': [0, 0, 0, 1, None]}}, toonDur=0.3),
            k(r(SLAP3 + 0.6), look='camera', lookDur=0.2), *blink(1.6, {'lid': 0.45, 'mouth': 'line', 'brow': -0.2})]),
        act('mec', HERO3a, 0, 'walk', 'unimpressed', keys=[k(0.0, to=HERO3b, dur=1.75, clip='walk'), k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': FING3(HERO3a)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(1.75, toon={'reach': {'R': FING3(HERO3b)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.2), *blink(2.0, {'lid': 0.35, 'mouth': 'line', 'brow': -0.2})])],
        props=[*[P(f'lampe3{i}', 'streetLamp', pos=[x, 0, z]) for i, (x, z) in enumerate(LAMPS)],
               *[P(f'affiche3{i}', 'wantedPoster', pos=POST(z), ry=0 if i == 0 else 18, opts={'at': SLAP3 if i == 0 else -1, **({} if i == 0 else {'w': 0.85, 'h': 1.18})}) for i, (x, z) in enumerate(LAMPS)], PLASTER('pansement3'),
               P('affiche3main', 'wantedPoster', on={'actor': 'policier', 'hand': 'L', 'offset': [0.0, 0.0, 0.06], 'rot': [0, PI / 2, 0]}, opts={'at': 0.0, 'hideAt': SLAP3, 'w': 0.5, 'h': 0.7})],   # (round 1) the poster in his hand until the slap
        cams=[C3])
st.cue('sfx:splat', 'S03', SLAP3, 0.45); st.cue('sfx:step', 'S03', 0.3, 0.2); st.cue('sfx:step', 'S03', 0.75, 0.2); st.cue('sfx:step', 'S03', 1.2, 0.2); st.cue('sfx:step', 'S03', 1.65, 0.2)

# 4: the police took in all the paper in the country. Low in the road behind a police van with its back open: a single file of paper (reams,
#    newspapers, books, a rolled map, then the RECHERCHÉE posters) marches across the road and up its steel ramp, each holding a tiny numbered
#    mugshot board (EMBARQUÉ)
D4 = st.dur('S04')
VAN = [3.0, 0, -4.6]; VAN_RY = 90                      # nose -Z, its back (and the ramp) toward +Z
RAMP_TOP = [3.0, 0.47, r(VAN[2] + 2.72)]; RAMP_FOOT = [3.0, 0.02, r(VAN[2] + 2.72 + 2.6)]
PATH4 = [[3.0, 0.02, 4.6], RAMP_FOOT, RAMP_TOP, [3.0, 0.5, r(VAN[2] + 1.0)]]
C4 = cam(0.0, [7.6, 1.55, 1.2], [7.45, 1.56, 1.15], [3.0, 0.62, -0.5], [3.0, 0.63, -0.55], lens=50)   # (final) panned back toward the van: its open back and dark inside at the right edge swallow the file   # (round 2) panned toward the road: a full file from frame 1, the van only a ramp and a door edge   # (round 1) side-on: the file climbs the ramp across the frame into the van
chk('S04', C4['from'], C4['lookAt'], 42, {'rampFoot': RAMP_FOOT, 'rampTop': RAMP_TOP, 'vanTop': [3.0, 3.0, VAN[2] + 2.5], 'path0': PATH4[0], 'path1': PATH4[1], 'vanLabel': [4.12, 1.55, VAN[2]]})
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('fourgon4', 'paddyWagon', pos=VAN, ry=VAN_RY, opts={'doorA': 3.0}),
               P('defile4', 'paperParade', pos=[0, 0, 0], opts={'path': PATH4, 'at': 0.0, 'lead': 7.6, 'speed': 1.45, 'gap': 0.62, 'n': 18, 's': 1.45, 'hop': 0.16, 'hopF': 4.2, 'squash': 0.3, 'boardS': 0.85, 'yaw': -PI / 2, 'kinds': ['ream', 'news', 'book', 'map', 'notes', 'ream', 'news', 'book', 'map', 'notes', 'ream', 'news', 'book', 'notes', 'map', 'poster', 'poster', 'poster']})],
        cams=[C4])
st.card('S04', 'EMBARQUÉ', at=0.9)
st.cue('sfx:stepSoft', 'S04', 0.2, 0.25); st.cue('sfx:stepSoft', 'S04', 0.55, 0.25); st.cue('sfx:stepSoft', 'S04', 0.9, 0.25); st.cue('sfx:stepSoft', 'S04', 1.25, 0.25); st.cue('sfx:stepSoft', 'S04', 1.6, 0.25); st.cue('clang', 'S04', 0.9, 0.15)

# 5: and every banknote. Low in the road: from the bank's open door, stacks of banknotes march down its three steps, across the pavement and up the
#    same van's ramp, each with its mugshot board; a police dog sniffs the last stack; the director stands in the doorway staring at us
D5 = st.dur('S05')
BANK = [0.0, 0, -3.0]                                  # the bank's front faces +Z (us): three steps, the door far back under its BANQUE sign
# (round 1) the van in shot: parked at the right with a short ramp from its open back to the foot of the steps; the director in the open doorway
#            between the columns (his face clear); the stacks hop down the three steps in arcs with a squash on landing, cross to the ramp and
#            climb into the van; the dog at the ramp's foot sniffs each stack and double-takes at the last one
VAN5 = [4.4, 0, -0.9]; RL5 = 1.4                       # nose +X: its open back (x 1.7) and the short ramp toward -X
PATH5 = [[0.0, 0.87, -6.9], [0.0, 0.87, -4.3], [0.0, 0.62, -4.0], [0.0, 0.42, -3.6], [0.0, 0.22, -3.2], [0.1, 0.02, -2.75], [0.3, 0.02, -0.9], [1.7, 0.47, -0.9], [2.9, 0.5, -0.9]]
DIR5 = [0.0, 0.87, -6.7]
DOG5 = [0.62, 0, -1.75]
C5 = cam(0.0, [0.5, 1.5, 2.6], [0.52, 1.5, 2.5], [0.9, 1.15, -1.6], [0.88, 1.16, -1.6], lens=50)
chk('S05', C5['from'], C5['lookAt'], 50, {'dirFace': [DIR5[0], DIR5[1] + 2.0, DIR5[2]], 'sign': [0, 4.0, -6.95], 'step1': [0, 0.42, -3.6], 'stepFoot': [0.1, 0.05, -2.9], 'rampFoot': [0.3, 0.02, -0.9], 'rampTop': [1.7, 0.47, -0.9], 'vanBackTop': [1.7, 2.6, -0.9], 'dog': [DOG5[0], 0.6, DOG5[2]]})
LOOKD = lambda p: [0, r(math.atan2(p[0] - DOG5[0], p[2] - DOG5[2])), 0]
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('directeur', DIR5, 0, 'stand', 'scared', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': R5(off(DIR5, 0, 0.12, 0.28, 2.15)), 'L': R5(off(DIR5, 0, 0.12, -0.28, 2.15))}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.0, 'pop': 0.25, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.0),
            k(0.45, look=[0.2, 0.3, -2.8], lookDur=0.15), *blink(0.75, {'lid': 0.0, 'pop': 0.25, 'mouth': 'O', 'brow': 0.8}),
            k(1.0, toon={'reach': {'R': R5(off(DIR5, 0, 0.18, 0.22, 1.75)), 'L': R5(off(DIR5, 0, 0.18, -0.22, 1.75))}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.1, 'jaw': 0.7, 'mouth': 'O', 'brow': 0.9}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.1, toonEase='out')])],
        props=[P('banque5', 'courtFront', pos=BANK, opts={'title': 'BANQUE', 'steps': 3, 'w': 7, 'cols': 4, 'open': True, 'H': 4.4, 'doorH': 2.8, 'doorSign': 'BANQUE'}),
               P('fourgon5', 'paddyWagon', pos=VAN5, ry=0, opts={'rampLen': RL5, 'doorA': 3.0}),
               P('billets5', 'paperParade', pos=[0, 0, 0], opts={'path': PATH5, 'at': 0.0, 'lead': 5.6, 'speed': 1.7, 'gap': 0.85, 'n': 7, 's': 1.2, 'hop': 0.24, 'hopF': 3.6, 'squash': 0.35, 'boardS': 0.75, 'kinds': ['notes']}),
               P('chien5', 'voxelDog', pos=DOG5, ry=-150, opts={'color': '#3A3530', 'muzzle': '#1E1A18'},
                 keys=[k(0.0, rotTo=LOOKD([0.15, 0, -2.6]), dur=0.15), k(0.35, rotTo=LOOKD([0.25, 0, -1.6]), dur=0.12), k(0.6, rotTo=LOOKD([0.15, 0, -2.6]), dur=0.12),
                       k(0.82, rotTo=LOOKD([0.6, 0, 3.0]), dur=0.1), k(0.98, rotTo=LOOKD([0.3, 0, -1.2]), dur=0.06, ease='out'), k(1.06, rotTo=LOOKD([0.6, 0, 3.0]), dur=0.06), k(1.14, rotTo=LOOKD([0.6, 0.0, -1.0]), dur=0.05, ease='out')])],
        cams=[C5])
st.cue('sfx:stepSoft', 'S05', 0.15, 0.25); st.cue('sfx:stepSoft', 'S05', 0.45, 0.25); st.cue('sfx:sniff', 'S05', 0.38, 0.35); st.cue('sfx:sniff', 'S05', 0.62, 0.3); st.cue('sfx:stepSoft', 'S05', 0.75, 0.25)

# 6: and the intern, for harbouring a criminal. On the pavement by a police car: the intern (thirties, tie, lanyard, glasses), bent calmly over the
#    bonnet, his cheek on it, the empty green ream wrapper beside his face, his briefcase at his feet; a bored officer behind him clicks the cuffs on
D6 = st.dur('S06'); CLICK6 = 1.15
# (round 1) seen from the front of the police car (grille, headlights, light bar, wheel arch): the intern, a blond man in a mustard suit and
#            glasses (not the hero's navy), bent 90 degrees over the bonnet from its left side, his cheek squashed flat on the metal, facing us; the
#            officer behind him clicks the cuffs on, the intern jolts at the click; breathing and slow blinks in the hold
CAR6 = [3.6, 0, -1.0]                                 # nose -Z (ry 90): the bonnet at z -1.9..-3.1, top 0.92, x 2.7..4.5
INT6 = [2.62, 0, -2.6]; RYI6 = 90                     # he faces +X, toward the car
OFF6 = [2.05, 0, -2.0]; RYO6 = 60
C6 = cam(0.0, [3.2, 1.45, -7.0], [3.19, 1.45, -6.8], [3.1, 1.15, -2.3], [3.1, 1.16, -2.3], lens=48)
HEAD6 = [3.42, 1.13, -2.62]
chk('S06', C6['from'], C6['lookAt'], 48, {'intHead': HEAD6, 'intHips': [2.75, 1.05, -2.6], 'offFace': [OFF6[0], 2.0, OFF6[2]], 'lightbar': [3.6, 1.78, -0.8], 'headlightL': [3.05, 0.72, -3.12], 'wheel': [2.8, 0.36, -2.35], 'wrapper': [3.95, 1.0, -2.4]})
BACK6 = off(INT6, RYI6, -0.12, 0.0, 1.02)
BENT = {'reach': {'R': R5(add(BACK6, [0, 0.02, -0.07])), 'L': R5(add(BACK6, [0, 0.02, 0.07]))}, 'hands': {'R': 'rest', 'L': 'rest'}, 'bend': {'spine': [1.45, 0, 0, 1, None], 'neck': [-0.25, 1.5, 0, 1, None]}}
SQZ = {'head': [1.14, 0.84, 1.0]}
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('stagiaire', INT6, RYI6, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={**BENT, 'scl': SQZ, 'face': {'lid': 0.45, 'mouth': 'wavy', 'brow': 0.3, 'cheeks': 0.6}}, toonDur=0.0),
            *blink(0.55, {'lid': 0.45, 'mouth': 'wavy', 'brow': 0.3, 'cheeks': 0.6}),
            k(CLICK6, toon={**BENT, 'scl': {'head': [1.2, 0.78, 1.0]}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.0, 'pop': 0.2, 'mouth': 'O', 'brow': 0.8, 'cheeks': 0.8}}, toonDur=0.04, toonEase='out'),
            k(r(CLICK6 + 0.16), toon={**BENT, 'scl': SQZ, 'sq': [1, 1, 1], 'face': {'lid': 0.5, 'mouth': 'flat', 'brow': 0.4, 'cheeks': 0.6}}, toonDur=0.12),
            *blink(1.9, {'lid': 0.5, 'mouth': 'flat', 'brow': 0.4, 'cheeks': 0.6})]),
        act('officier', OFF6, RYO6, 'stand', 'unimpressed', keys=[k(0.0, look=BACK6),
            k(0.0, toon={'reach': {'R': R5(add(BACK6, [-0.15, 0.03, -0.08])), 'L': R5(add(BACK6, [-0.15, 0.03, 0.08]))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.6, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.0),
            k(r(CLICK6 - 0.12), toon={'reach': {'R': R5(add(BACK6, [-0.08, 0.0, -0.05])), 'L': R5(add(BACK6, [-0.1, 0.02, 0.07]))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.34, 0, 0, 1, None]}, 'face': {'lid': 0.65, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.1),
            k(r(CLICK6 + 0.04), toon={'reach': {'R': R5(add(BACK6, [-0.2, 0.06, -0.08])), 'L': R5(add(BACK6, [-0.2, 0.06, 0.08]))}, 'hands': {'R': 'open', 'L': 'grip'}, 'bend': {'spine': [0.26, 0, 0, 1, None]}}, toonDur=0.08, toonEase='out'),
            k(r(CLICK6 + 0.45), look='camera', lookDur=0.3), *blink(1.95, {'lid': 0.65, 'mouth': 'line', 'brow': -0.1})])],
        props=[P('voiture6', 'policeCar', pos=CAR6, ry=90), P('emballage6', 'sheetStack', pos=[3.95, 0.93, -2.4], ry=20, opts={'empty': True}),
               P('mallette6', 'briefcase', pos=[2.4, 0, -3.05], ry=-30), P('badge6', 'lanyard', on={'actor': 'stagiaire', 'joint': 'torso', 'offset': [0.0, 0.48, 0.0]}),
               P('menottes6', 'handcuffs', on={'actor': 'stagiaire', 'hand': 'R'}, keys=[k(0.0, visible=False), k(CLICK6, visible=True)])],
        cams=[C6])
st.cue('sfx:cuff', 'S06', CLICK6, 0.5); st.cue('sfx:static', 'S06', 0.2, 0.1)

# 7: the finger recognised her. Over his left shoulder from behind, through the tinted glass: five identical white sheets stand against the
#    height chart; his right arm rises on its own, the plastered index pointing at the third; an officer flips her: the red smear shows, the
#    dog-ear springs up
D7 = st.dur('S07'); RISE7, FLIP7 = 0.05, 0.32   # (final) the flip earlier: the smear holds about 0.65 s
# (round 1) closer: the five sheets bigger and spaced, on a dark dais against the dark height chart behind tinted glass; the suspect (the third)
#            centred; his arm rises on its own from the left edge; the officer flips her over 0.22 s, the red smear and the dog-ear spring into view
LINE_Z = -0.3; SHL = {'w': 0.42, 'h': 0.6}; GAP7 = 0.5; DY7 = 0.6   # (final) all five in one row in frame
HERO7 = [-0.7, 0, 3.5]; RYH7 = 180   # (final) his head and arm in the left third
COP7a, COP7b = [1.3, 0, -0.95], [0.75, 0, -0.95]   # (round 2) on the floor beside the dais: his head inside the frame   # (round 1) at the right, behind the line, so he no longer stands in front of the suspect
C7 = cam(0.0, [-0.3, 2.9, 5.6], [-0.3, 2.89, 5.5], [-0.15, 1.0, LINE_Z], [-0.15, 1.0, LINE_Z], lens=54)   # (final)   # (round 2) a little back and up: the officer's head inside the frame
PT7 = R5([-0.32, 1.5, 2.45], 1, 0.14)   # (final) the stretched arm aims straight at the third sheet   # (round 2) arm stretched forward-down, the index on the third sheet
chk('S07', C7['from'], C7['lookAt'], 54, {'sheet3top': [0.0, DY7 + 0.6, LINE_Z], 'sheet3bot': [0.0, DY7, LINE_Z], 'sheet1L': [-2 * GAP7 - 0.21, DY7 + 0.3, LINE_Z], 'sheet5R': [2 * GAP7 + 0.21, DY7 + 0.3, LINE_Z], 'heroHead': [HERO7[0], 2.15, HERO7[2]], 'hand': PT7[:3], 'copFace': [COP7b[0], DY7 + 2.0, COP7b[2]], 'chartTop': [0, 2.4, -0.9]})
st.shot('S07', 'whiteVoid', setOpts={'color': '#A58C6E'}, actors=[   # (final) a warmer room
        act('mec', HERO7, RYH7, 'stand', 'neutral', keys=[k(0.0, look=[0.0, DY7 + 0.5, LINE_Z]),
            k(0.0, toon={'reach': {'R': R5(off(HERO7, RYH7, 0.15, 0.3, 0.9))}, 'hands': {'R': 'rest'}}, toonDur=0.0),
            k(RISE7, toon={'reach': {'R': R5(add(PT7[:3], [0, -0.3, 0.25]), 1, 0.1)}, 'hands': {'R': 'point'}}, toonDur=0.2, toonEase='out'),
            k(r(RISE7 + 0.22), toon={'reach': {'R': PT7}, 'hands': {'R': 'point'}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.12, toonEase='out'),
            k(r(RISE7 + 0.2), look=PT7[:3], lookDur=0.12), k(r(RISE7 + 0.5), look=[0.0, DY7 + 0.5, LINE_Z], lookDur=0.12)]),
        act('policier', COP7a, -70, 'stand', 'neutral', keys=[k(0.0, to=COP7b, dur=0.22, clip='walk'), k(0.0, look=[0.0, DY7 + 0.5, LINE_Z]),
            k(r(FLIP7 - 0.1), toon={'reach': {'R': R5([0.2, DY7 + 0.42, LINE_Z - 0.05], 1, 0.12)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.2, 0, 0.25, 1, None]}}, toonDur=0.08, toonEase='out'),
            k(r(FLIP7 + 0.2), toon={'reach': {'R': R5([0.55, DY7 + 0.85, LINE_Z - 0.1])}, 'hands': {'R': 'open'}, 'bend': {'spine': [0, 0, 0, 1, None]}}, toonDur=0.08, toonEase='out'), k(r(FLIP7 + 0.35), look='camera', lookDur=0.15)])],
        props=[P('tapissage7', 'lineupWall', pos=[0, 0, -0.9], opts={'w': 5.2, 'gap': GAP7}), P('estrade7', 'dais', pos=[0, 0, -0.35], opts={'w': 5.2, 'h': DY7, 'd': 0.8}),
               P('vitre7', 'glassPane', pos=[0, 0, 0.9], opts={'w': 3.6, 'h': 1.4, 'y': 0.85, 'opacity': 0.16}),
               *[P(f'feuille7{i}', 'feuilleSheet', pos=[r((i - 2) * GAP7), r(DY7 + 0.3), LINE_Z], opts={**SHL, 'ear': 0, 'smear': False}) for i in (0, 1, 3, 4)],
               P('suspecte7', 'feuilleSheet', pos=[0.0, r(DY7 + 0.3), LINE_Z], opts={**SHL, 'smearSide': 'back', 'smearS': 1.8, 'ear0': 0.0, 'earKeys': [[r(FLIP7 + 0.22), 1.0], [r(FLIP7 + 0.3), 0.8]]}, keys=[k(FLIP7, rotTo=[0, PI, 0], dur=0.16, ease='out')]),   # (final) a snap
               PLASTER('pansement7')],
        cams=[C7])
st.cue('whoosh', 'S07', RISE7, 0.2, 0.25, 600, 2400); st.cue('sfx:paper', 'S07', FLIP7, 0.5); st.cue('sfx:spring', 'S07', r(FLIP7 + 0.17), 0.3)

# ============================== the courthouse: a stone front with six steps and columns (TRIBUNAL), a paved forecourt; the sheet between two
# gendarmes at the foot of the steps (they hold her top corners), the prosecutor at his microphones, the trolley shredder
CT = [-0.65, 0, -1.6]
# (round 1) the sheet stands ALONE on the portico landing (y 1.45) in front of the open, dark doorway, between the two middle columns, so the white
#            rectangle reads against black; the prosecutor in a red robe on the landing behind her at the right; the trolley rolls in on its own
LAND = 1.45
PLAZA = P('parvis', 'parkLot', pos=[0, 0, 4.0], opts={'w': 40, 'd': 24, 'rows': [], 'color': '#C9C2B2', 'y': 0.03})
SHC = {'w': 0.62, 'h': 0.82, 'smearS': 1.7}
SHEET_C = [-0.8, r(LAND + 0.41), -4.45]
PROC = [0.08, LAND, -6.35]; RYP = -165                # inside the doorway, right of the trolley, his face clear of the right column and of the shredder
TROLa, TROL = [0.9, LAND, -6.15], [-0.5, LAND, -6.15]   # it rolls out from behind the right column
MICS = [-0.05, LAND, -3.9]
CC = cam(0.0, [-0.45, 2.2, -1.6], [-0.45, 2.19, -1.7], [-0.5, 2.05, -5.2], [-0.5, 2.05, -5.2], lens=60)
COURT = lambda: [P('tribunal', 'courtFront', pos=CT, opts={'w': 13, 'steps': 6, 'cols': 6, 'open': True}), PLAZA]
EARFLAP = lambda t0, t1: [[r(t0 + 0.05 * i), 0.55 if i % 2 else 0.95] for i in range(int((t1 - t0) / 0.05))]

# 8: the prosecutor asked for the shredder. On the portico landing, medium close on the sheet standing alone against the dark doorway; behind her
#    at the right the prosecutor in his red robe; the price-tagged shredder on its trolley rolls in from the right, he winds up and whips the red
#    velvet cover off; she leans back, her top edge rolls into a C and she shivers, the dog-ear flapping
D8 = st.dur('S08'); OFF8 = 0.72
chk('S08', CC['from'], CC['lookAt'], 60, {'sheetTop': [SHEET_C[0], LAND + 0.82, SHEET_C[2]], 'sheetBot': [SHEET_C[0], LAND, SHEET_C[2]], 'procFace': [PROC[0], LAND + 2.0, PROC[2]], 'procFeet': PROC, 'trolley': [TROL[0], LAND + 1.65, TROL[2]], 'trolStart': [TROLa[0], LAND + 1.2, TROLa[2]]})
TT = lambda dx, dy, dz: [r(TROL[0] + dx), r(TROL[1] + dy), r(TROL[2] + dz)]
st.shot('S08', 'grassland', setOpts={'clouds': 26}, actors=[
        act('procureur', PROC, RYP, 'stand', 'angry', keys=[k(0.0, look='camera'), k(0.28, look=[TROL[0], LAND + 1.5, TROL[2]], lookDur=0.1), k(r(OFF8 - 0.04), look='camera', lookDur=0.08), 
            k(0.0, toon={'reach': {'R': R5(TT(0.3, 1.0, 0.0)), 'L': R5(off(PROC, RYP, 0.15, -0.25, 1.1))}, 'hands': {'R': 'open', 'L': 'rest'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': -0.4}}, toonDur=0.0),
            k(0.42, toon={'reach': {'R': R5(TT(0.22, 1.72, 0.1)), 'L': R5(off(PROC, RYP, 0.15, -0.25, 1.1))}, 'hands': {'R': 'grip', 'L': 'rest'}}, toonDur=0.1),
            k(r(OFF8 - 0.2), toon={'reach': {'R': R5(TT(0.12, 1.45, 0.05))}, 'hands': {'R': 'grip'}, 'sq': [1.06, 0.93, 1.06], 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'mouth': 'clench', 'brow': -0.6}}, toonDur=0.16, toonEase='inOut'),
            k(OFF8, toon={'reach': {'R': R5(TT(1.1, 2.6, 0.4), 1, 0.1)}, 'hands': {'R': 'grip'}, 'sq': [0.94, 1.08, 0.94], 'bend': {'spine': [-0.15, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.3}}, toonDur=0.08, toonEase='out'),
            k(r(OFF8 + 0.45), toon={'reach': {'R': R5(TT(0.8, 2.2, 0.3))}, 'hands': {'R': 'open'}, 'sq': [1, 1, 1], 'bend': {'spine': [0, 0, 0, 1, None]}}, toonDur=0.3),
            *blink(1.6, {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.3})])],
        props=[*COURT(), P('chariot8', 'shredderTrolley', pos=TROLa, ry=-20, opts={'offAt': OFF8, 'offDur': 0.36, 'coverColor': '#1F5A3A'}, keys=[k(0.0, to=TROL, dur=0.42, ease='out')]),
               P('feuille8', 'feuilleSheet', pos=SHEET_C, opts={**SHC, 'curlK': 1.25, 'ear0': 0.95, 'curl': [[r(OFF8 + 0.08), 0.0], [r(OFF8 + 0.2), 0.45], [r(OFF8 + 0.36), 1.05], [r(OFF8 + 0.46), 0.95]], 'tremble': [[r(OFF8 + 0.3), 1.6]],  'earKeys': EARFLAP(r(OFF8 + 0.25), D8)},
                 keys=[k(r(OFF8 + 0.02), rotTo=[-0.32, 0.08, 0], dur=0.12, ease='out'), k(r(OFF8 + 0.2), rotTo=[-0.12, 0.05, 0], dur=0.2, ease='inOut')])],
        cams=[CC])
st.cue('sfx:rattle', 'S08', 0.0, 0.25); st.cue('whoosh', 'S08', OFF8, 0.35, 0.3, 500, 2600); st.cue('sfx:gasp', 'S08', r(OFF8 + 0.18), 0.15)

# 9: the president put the shredder to a referendum. The press room: the president in his sash at the podium taps a pointer on the poster of the
#    same price-tagged shredder beside him, with its OUI and NON boxes
D9 = st.dur('S09')
# (round 1) he faces us three-quarter, his painted face readable; the hand stays near his body and the pointer stick does the reaching: a rhythmic
#            tap on the shredder drawing with a lean into each tap; glances at the poster between taps; the backdrop word smaller so it tiles cleanly
PRES9 = [0.05, 0, -2.4]; RYP9 = -12
POSTER9 = [0.95, 0, -2.3]
C9 = cam(0.0, [0.35, 1.9, 2.5], [0.35, 1.9, 2.4], [0.52, 1.75, -2.3], [0.52, 1.76, -2.3], lens=48)
HAND9 = [0.5, 1.42, -2.12]
chk('S09', C9['from'], C9['lookAt'], 48, {'presFace': [PRES9[0], 2.05, PRES9[2]], 'posterTop': [POSTER9[0], 2.5, POSTER9[2] + 0.1], 'posterOUI': [POSTER9[0] - 0.4, 1.35, POSTER9[2] + 0.1], 'posterNONright': [POSTER9[0] + 0.62, 1.35, POSTER9[2] + 0.2], 'hand': HAND9})
FACE9 = {'lid': 0.35, 'mouth': 'smile', 'brow': 0.3}
st.shot('S09', 'pressRoom', setOpts={'backdrop': 'RÉFÉRENDUM', 'fontScale': 0.62, 'flags': False, 'chairs': False}, actors=[
        act('president', PRES9, RYP9, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': R5(add(HAND9, [0.0, 0.2, 0.06]), 1, 0.06)}, 'hands': {'L': 'grip'}, 'bend': {'spine': [-0.1, 0, 0.1, 1, None]}, 'face': {**FACE9, 'mouth': 'smile'}}, toonDur=0.0),
            *[k(r(0.15 + 0.3 * i), toon={'reach': {'L': R5(add(HAND9, [0.0, 0.16 * (i % 2), 0.0]), 1, 0.06)}, 'hands': {'L': 'grip'}, 'bend': {'spine': [0.12 * (1 - i % 2), 0, -0.22 * (1 - i % 2), 1, None]},
                         'sq': [1.02, 0.98, 1.02] if i % 2 == 0 else [1, 1, 1], 'face': {**FACE9, 'mouth': 'open' if i % 2 == 0 else 'smile'}}, toonDur=0.06 if i % 2 == 0 else 0.16) for i in range(8)],
            k(0.75, look=[POSTER9[0], 1.9, POSTER9[2]], lookDur=0.12), k(1.15, look='camera', lookDur=0.12), *blink(1.5, FACE9), k(1.95, look=[POSTER9[0], 1.9, POSTER9[2]], lookDur=0.12), k(2.3, look='camera', lookDur=0.12)])],
        props=[P('affiche9', 'refPoster', pos=POSTER9, ry=-22, opts={}), P('baguette9', 'pointerStick', on={'actor': 'president', 'hand': 'L', 'offset': [0.0, -0.04, 0.02], 'rot': [PI * 0.5, 0, -0.55]}, opts={'len': 0.95})],
        cams=[C9])
for i_ in range(4): st.cue('clack', 'S09', r(0.15 + 0.6 * i_), 0.22)

# 10: fifty million ballots. A school gym buried waist-deep in white ballots; three officials wade through them pushing snow shovels
D10 = st.dur('S10')
OFFS10 = [('officiel1', [-0.75, 0, -0.6], 20), ('officiel2', [0.3, 0, -1.7], -10), ('officiel3', [0.95, 0, -0.1], -35)]
C10 = cam(0.0, [0.2, 2.75, 5.0], [0.2, 2.7, 4.75], [0.1, 1.15, -1.0], [0.1, 1.16, -1.0], lens=46)
chk('S10', C10['from'], C10['lookAt'], 46, {**{w: [p[0], 2.0, p[2]] for w, p, ry in OFFS10}, 'seaFront': [0, 0.95, 3.0], 'wallLabel': [0.8, 2.85, -3.6]})
def SHOVEL_K(p, ry, ph):
    # (round 1) real shovelling strokes: dig (bent, blade low and forward), heave (up and over the shoulder), with a breath between
    return [k(0.0, look='camera' if ph == 0 else off(p, ry, 1.5, 0, 0.9))] + [k(r(0.22 * j + ph), toon={'reach': {'R': R5(off(p, ry, 0.7 if j % 2 == 0 else 0.25, 0.15, 1.0 if j % 2 == 0 else 1.75)), 'L': R5(off(p, ry, 0.5 if j % 2 == 0 else 0.15, -0.2, 1.25 if j % 2 == 0 else 1.95))}, 'hands': {'R': 'grip', 'L': 'grip'},
            'bend': {'spine': [0.45 if j % 2 == 0 else -0.1, 0.25 * (j % 2), 0, 1, None]}, 'sq': [1.04, 0.95, 1.04] if j % 2 == 0 else [0.97, 1.04, 0.97], 'face': {'lid': 0.45, 'mouth': 'clench' if j % 2 == 0 else 'O', 'brow': -0.3}}, toonDur=0.18, toonEase='inOut') for j in range(8)]
st.shot('S10', 'gym', actors=[act(w, p, ry, 'stand', 'neutral', keys=SHOVEL_K(p, ry, 0.1 * i)) for i, (w, p, ry) in enumerate(OFFS10)],
        props=[P('mer10', 'ballotSea', pos=[0, 0, 0.5], opts={'w': 14, 'd': 12, 'h': 0.95, 'n': 1100}),
               *[P(f'pelle10{i}', 'snowShovel', on={'actor': w, 'hand': 'R', 'offset': [0.0, -0.05, 0.03], 'rot': [0.6, 0, 0]}, opts={'len': 1.0}) for i, (w, p, ry) in enumerate(OFFS10)],
               *[P(f'gerbe10{i}{j}', 'divingBallots', pos=[0, 0, 0], opts={'drops': [{'from': off(p, ry, 0.9, 0.1 * (b - 1), 0.95), 'to': off(p, ry, -0.6, 0.3 * (b - 1), 0.95), 't0': r(0.1 * i + 0.22 * (2 * j + 1) - 0.12), 'dur': 0.4, 'hold': 0.12, 'arc': 0.9, 'spin': 1 if b % 2 else -1} for b in range(3)]}) for i, (w, p, ry) in enumerate(OFFS10) for j in range(3)]],   # (round 1) ballots sprayed over their shoulders on each heave
        cams=[C10])
st.cue('sfx:paper', 'S10', 0.15, 0.35); st.cue('sfx:paper', 'S10', 0.6, 0.35); st.cue('sfx:paper', 'S10', 1.1, 0.35)

# 11: a whole forest. A hillside of fresh stumps to the top; in front, a log truck marked BULLETINS takes the last log; a gendarme with a chainsaw in
#     his left hand salutes beside it
D11 = st.dur('S11'); LOAD11 = 0.42   # (round 2) the last log swings on mid-shot, not before the eye lands
# (round 1) a real hillside of stumps filling the frame to the top (a steeper hill, the camera tilted up); the truck seen in depth (nose up the
#            hill) so it is whole, BULLETINS on its side toward us; the last log swung on with weight (it rises, hangs, drops with a bounce); the
#            gendarme fully in frame at the right, saluting with the chainsaw in his left hand, a breath and a blink
TRUCK11 = [-0.3, 0, -3.5]
GEN11 = [2.2, 0, 4.2]; RYG11 = 15
C11 = cam(0.0, [2.8, 1.5, 9.5], [2.78, 1.52, 9.3], [-0.3, 4.2, -6.0], [-0.3, 4.35, -6.0], lens=50)
chk('S11', C11['from'], C11['lookAt'], 50, {'genFace': [GEN11[0], 2.0, GEN11[2]], 'genFeet': GEN11, 'truckRear': [-0.3, 1.5, 0.5], 'truckNose': [-0.3, 2.5, -7.5], 'panel': [0.95, 2.6, -3.5]})
st.shot('S11', 'grassland', setOpts={'clouds': 30}, actors=[
        act('gendarme3', GEN11, RYG11, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': SALUTE(GEN11, RYG11)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
            *blink(0.9, {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}), k(r(LOAD11 + 0.62), toon={'sq': [1.02, 0.97, 1.02]}, toonDur=0.06, keepPose=True), k(r(LOAD11 + 0.8), toon={'sq': [1, 1, 1]}, toonDur=0.1, keepPose=True)])],
        props=[P('colline11', 'stumpField', pos=[0, 0, -4.0], opts={'w': 80, 'd': 46, 'rise': 36}), P('camion11', 'logTruck', pos=TRUCK11, ry=90, opts={'loadAt': LOAD11, 'side': 1}),
               P('tronconneuse11', 'chainsaw', on={'actor': 'gendarme3', 'hand': 'L', 'offset': [0.0, -0.1, 0.05]}), KEPI('kepi11', 'gendarme3')],
        cams=[C11])
st.cue('sfx:chainsaw', 'S11', 0.0, 0.18); st.cue('thud', 'S11', r(LOAD11 + 0.62), 0.5)

# ============================== the polling station (the town-hall room): a table with the OUI box (left) and the NON box (right), seen from the
# voters' far side: they stand behind the table facing us and reach over the boxes
TAB = [0.0, 0, -0.9]; BOXY = 0.95   # (round 1) a taller table: the box interiors (NON filling up) above the caption band
OUI = [-0.36, BOXY, -0.9]; NON = [0.36, BOXY, -0.9]
SLOT = lambda b: [b[0], r(b[1] + 0.72), b[2]]
VOTE = {'title': 'BUREAU DE VOTE', 'desk': False, 'map': False, 'clockX': 4.6, 'bannerY': 2.72}   # (round 1) the room's running clock moved out of shot (S13 has its own, stopped at eight)
def POLL_PROPS(fill_non, fill_oui=None):
    return [P('table', 'table', pos=TAB, opts={'w': 1.6, 'd': 0.7, 'h': BOXY, 'color': '#8A6A45', 'legs': '#5A3A28'}),
            P('urneOui', 'ballotBox', pos=OUI, opts={'text': 'OUI', 'fill': fill_oui or []}), P('urneNon', 'ballotBox', pos=NON, opts={'text': 'NON', 'fill': fill_non})]

# 12: the ballots all voted no. Across the table: three voters behind it hold their ballots up over the OUI box; one after the other the ballots
#     wriggle out of their fingers, hop over and dive into the NON box, which fills; the OUI box stays empty
D12 = st.dur('S12')
VOT12 = [('electeur1', [-0.5, 0, -1.7], 10), ('electeur2', [-0.95, 0, -2.25], 20), ('electeur3', [0.45, 0, -1.8], -15)]
HOLD12 = [[-0.32, 1.9, -0.95], [-0.55, 1.88, -1.4], [0.08, 1.88, -1.2]]
T12 = [0.15, 0.55, 0.95]
C12 = cam(0.0, [0.25, 1.85, 2.5], [0.24, 1.86, 2.3], [-0.1, 1.45, -1.3], [-0.1, 1.45, -1.3], lens=44)
chk('S12', C12['from'], C12['lookAt'], 44, {**{w: [p[0], 2.0, p[2]] for w, p, ry in VOT12}, 'oui': [OUI[0], 1.2, OUI[2] + 0.31], 'non': [NON[0], 1.2, NON[2] + 0.31], 'hold1': HOLD12[0]})
def VOTER_K(i, w, p, ry):
    h = HOLD12[i]; hand = 'R' if h[0] < p[0] else 'L'; t = T12[i]
    base = [k(0.0, look=SLOT(OUI)), k(0.0, toon={'reach': {hand: R5(h, 1, 0.06)}, 'hands': {hand: 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.0}}, toonDur=0.0)]
    if i == 0:   # (round 1) a double take: looks at the box, back at his empty fingers, back at the box
        return base + [k(r(t + 0.3), toon={'reach': {hand: R5(add(h, [0, 0.03, 0]), 1, 0.06)}, 'hands': {hand: 'open'}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.08),
                       k(r(t + 0.45), look=SLOT(NON), lookDur=0.1), k(r(t + 0.62), look=h, lookDur=0.07), k(r(t + 0.76), look=SLOT(NON), lookDur=0.06),
                       k(r(t + 0.76), toon={'face': {'lid': 0.0, 'pop': 0.25, 'mouth': 'O', 'brow': 0.8}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.06, keepPose=True)]
    if i == 1:   # a jaw drop
        return base + [k(r(t + 0.3), toon={'reach': {hand: R5(add(h, [0, 0.03, 0]), 1, 0.06)}, 'hands': {hand: 'open'}, 'face': {'lid': 0.1, 'jaw': 0.85, 'mouth': 'O', 'brow': 0.9}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.08),
                       k(r(t + 0.45), look=SLOT(NON), lookDur=0.15)]
    return base + [k(r(t + 0.3), toon={'reach': {hand: R5(add(h, [0, 0.08, 0.05]), 1, 0.06)}, 'hands': {hand: 'open'}, 'bend': {'spine': [-0.22, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'pop': 0.2, 'mouth': 'grimace', 'brow': 0.6}}, toonDur=0.08),   # a lean back
                   k(r(t + 0.45), look=SLOT(NON), lookDur=0.15)]
st.shot('S12', 'mairie', setOpts=VOTE, actors=[act(w, p, ry, 'stand', 'neutral', keys=VOTER_K(i, w, p, ry)) for i, (w, p, ry) in enumerate(VOT12)],
        props=[*POLL_PROPS([[r(T12[0] + 0.85), 1], [r(T12[1] + 0.85), 2], [r(T12[2] + 0.85), 3], [r(T12[2] + 1.0), 6]]),
               P('bulletins12', 'divingBallots', pos=[0, 0, 0], opts={'drops': [{'from': HOLD12[i], 'to': SLOT(NON), 't0': T12[i], 'dur': 0.5, 'hold': 0.3, 'arc': 0.45, 'spin': 1 if i % 2 else -1} for i in range(3)]})],
        cams=[C12])
for t_ in T12: st.cue('whoosh', 'S12', r(t_ + 0.3), 0.15, 0.3, 900, 3500); st.cue('sfx:paper', 'S12', r(t_ + 0.78), 0.3)

# 13: his first. Close on the boxes, the town-hall clock at eight behind: he holds his ballot over the OUI box (left hand, the plastered finger
#     raised well away); it twists out of his fingers and is the first into the NON box
D13 = st.dur('S13'); T13 = 0.1
HERO13 = [-0.15, 0, -1.65]
HOLD13 = [-0.3, 1.9, -0.98]
C13 = cam(0.0, [0.05, 1.8, 1.5], [0.05, 1.8, 1.42], [-0.02, 1.45, -1.2], [-0.02, 1.45, -1.2], lens=52)
chk('S13', C13['from'], C13['lookAt'], 46, {'face': [HERO13[0], 2.0, HERO13[2]], 'oui': [OUI[0], 1.15, OUI[2] + 0.31], 'non': [NON[0], 1.15, NON[2] + 0.31], 'hold': HOLD13, 'clock': [0.6, 2.55, -2.57]})
st.shot('S13', 'mairie', setOpts=VOTE, actors=[
        act('mec', HERO13, 0, 'stand', 'neutral', keys=[k(0.0, look=SLOT(OUI)),
            k(0.0, toon={'reach': {'L': R5(HOLD13, 1, 0.06), 'R': R5(off(HERO13, 0, 0.3, 0.35, 1.85))}, 'hands': {'L': 'pinch', 'R': 'point'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.0),
            k(r(T13 + 0.3), toon={'reach': {'L': R5(add(HOLD13, [0, 0.03, 0]), 1, 0.06), 'R': R5(off(HERO13, 0, 0.3, 0.35, 1.85))}, 'hands': {'L': 'open', 'R': 'point'}, 'face': {'lid': 0.3, 'jaw': 0.6, 'mouth': 'O', 'brow': 0.6}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.07),   # (round 1) a jaw drop, not another eye-pop
            k(r(T13 + 0.45), look=SLOT(NON), lookDur=0.12), k(r(T13 + 0.85), look='camera', lookDur=0.15)])],
        props=[*POLL_PROPS([[r(T13 + 0.78), 1]]), P('horloge13', 'wallClock', pos=[1.05, 2.6, -2.55], opts={'rate': 0, 'hours': 8}), PLASTER('pansement13'),
               P('bulletin13', 'divingBallots', pos=[0, 0, 0], opts={'drops': [{'from': HOLD13, 'to': SLOT(NON), 't0': T13, 'dur': 0.42, 'hold': 0.3, 'arc': 0.35, 'spin': 1}]})],
        cams=[C13])
st.cue('whoosh', 'S13', r(T13 + 0.3), 0.18, 0.3, 900, 3500); st.cue('sfx:paper', 'S13', r(T13 + 0.72), 0.35)

# 14: the shredder was abolished. The same shot as line 8: an usher steps in from the right, throws the velvet cover back over the shredder and
#     pulls the trolley out of frame; the sheet unrolls with an overshoot and settles, her shiver dying away (ABOLIE stamps once they are gone)
D14 = st.dur('S14'); ON14 = 0.2; GO14 = 0.38
HUI14a, HUI14b, HUI14c = [0.95, LAND, -6.45], [0.12, LAND, -6.45], [3.6, LAND, -6.45]   # (round 2) he walks right out of frame   # (round 1) inside the doorway gap, whole
chk('S14', CC['from'], CC['lookAt'], 60, {'sheetTop': [SHEET_C[0], LAND + 0.82, SHEET_C[2]], 'h1Face': [HUI14b[0], LAND + 2.0, HUI14b[2]], 'trolEnd': [2.0, LAND + 1.4, TROL[2]]})
st.shot('S14', 'grassland', setOpts={'clouds': 26}, actors=[
        act('huissier1', HUI14a, -90, 'stand', 'neutral', keys=[k(0.0, to=HUI14b, dur=0.18, clip='walk'), k(0.0, look=[TROL[0], LAND + 1.5, TROL[2]]),
            k(0.1, toon={'reach': {'R': R5(TT(0.15, 2.05, 0.1)), 'L': R5(TT(0.15, 2.05, -0.1))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.1),
            k(ON14, toon={'reach': {'R': R5(TT(0.2, 1.55, 0.12)), 'L': R5(TT(0.2, 1.55, -0.12))}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.04, 0.96, 1.04]}, toonDur=0.08),
            k(GO14, to=HUI14c, dur=0.55, clip='walk', ease='in'), k(GO14, toon={'reach': {'L': R5(off(HUI14b, 90, -0.45, -0.2, 0.95), 0), 'R': R5(off(HUI14b, 90, 0.2, 0.2, 0.95), 0)}, 'hands': {'L': 'rest', 'R': 'rest'}, 'sq': [1, 1, 1]}, toonDur=0.1)])],   # (round 2) both hands let go: no arm left behind
        props=[*COURT(), P('chariot14', 'shredderTrolley', pos=TROL, ry=-20, opts={'covered': False, 'onAt': ON14, 'coverColor': '#1F5A3A'}, keys=[k(GO14, to=[3.0, LAND, TROL[2]], dur=0.55, ease='in')]),
               P('feuille14', 'feuilleSheet', pos=SHEET_C, rot=[-0.12, 0.05, 0], opts={**SHC, 'curlK': 1.25, 'ear0': 0.95, 'curl': [[0.0, 1.0], [0.42, 1.0], [0.62, -0.2], [0.74, 0.08], [0.86, 0.0]], 'tremble': [[0.0, 1.2], [0.45, 0.4], [0.8, 0.0]],  'earKeys': EARFLAP(0.0, 0.5) + [[0.7, 1.0], [0.85, 0.9]]},
                 keys=[k(0.5, rotTo=[0.06, 0.0, 0], dur=0.2, ease='out'), k(0.75, rotTo=[0, 0, 0], dur=0.15, ease='inOut')])],
        cams=[CC])
st.card('S14', 'ABOLIE', at=0.95)
st.cue('whoosh', 'S14', ON14, 0.3, 0.25, 400, 2000); st.cue('sfx:rattle', 'S14', GO14, 0.25); st.cue('sfx:spring', 'S14', 0.66, 0.25)

# 15: the gendarmes flattened every shredder. Low on a vast square: a gendarme drives a steamroller with a big red bow along a row of price-tagged
#     shredders, flattening them one by one like biscuits with puffs of confetti; rows already flat behind; a line of gendarmes salutes
D15 = st.dur('S15')
# (round 1) low and wide three-quarter on the square: the roller crosses the frame left to right along the front row, each shredder pancakes in two
#            frames with a confetti pop; rows already flat behind it; one flattened shredder pops half back up; the saluting line far back left
ROLL0, ROLL1 = [-5.5, 0.03, 0.0], [2.0, 0.03, 0.0]
SPD15 = r((ROLL1[0] - ROLL0[0]) / D15, 3)
C15 = cam(0.0, [-3.0, 3.6, 11.5], [2.6, 3.6, 11.5], [-3.0, 0.6, -1.5], [2.6, 0.6, -1.5], lens=52)   # (round 2) side-on, panning with the drum across the front row   # (round 1) higher: the flattened rows read behind the standing ones
LINE15 = [(f'garde{i}', [r(-6.6 + 1.1 * i), 0.03, -6.5]) for i in range(5)]
chk('S15', C15['from'], C15['lookAt'], 56, {'rollerStart': [ROLL0[0] + 2.0, 1.2, 0], 'rollerEnd': [ROLL1[0] + 1.5, 1.2, 0], 'driverEnd': [ROLL1[0] - 0.7, 3.4, 0], 'row0a': [-3.0, 0.5, 0.0], 'row0e': [2.4, 0.5, 0.0], 'flatBehind': [-1.0, 0.1, -2.0], **{w: [p[0], 2.0, p[2]] for w, p in LINE15[1:4]}})
st.shot('S15', 'grassland', setOpts={'clouds': 30}, actors=[
        act('chauffeur', [ROLL0[0] - 0.7, 1.45, 0.0], 90, 'drive', 'neutral', keys=[k(0.0, to=[ROLL1[0] - 0.7, 1.45, 0.0], dur=D15, ease='linear', face='keep', clip='drive'), k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': SALUTE([ROLL0[0] - 0.7, 0.0, 0.0], 90)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0), *blink(1.2, {'lid': 0.4, 'mouth': 'line', 'brow': -0.3})]),
        *[act(w, p, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': SALUTE(p, 0)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0), *blink(r(0.5 + 0.37 * i), {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}), k(r(1.0 + 0.2 * i), look=[ROLL1[0], 1.8, 0.0], lookDur=0.3)]) for i, (w, p) in enumerate(LINE15)]],
        props=[P('place15', 'parkLot', pos=[0, 0, -4.0], opts={'w': 70, 'd': 50, 'rows': [], 'color': '#CFC8B8', 'y': 0.03}),
               P('rouleau15', 'steamroller', pos=ROLL0, ry=0, keys=[k(0.0, to=ROLL1, dur=D15, ease='linear')]),
               P('rangees15', 'shredderRows', pos=[0, 0, 0], opts={'rows': [[0.0, -3.0, 5, 1.35], [-2.0, -4.5, 7, 1.4], [-4.0, -6.0, 9, 1.4]], 'preFlat': [-2.0, -4.0], 'springIdx': 0, 'springDelay': 1.0, 'puffN': 30, 'puffBit': 0.2, 'puffR': 1.6,
                                                                  'at': 0.0, 'x0': ROLL0[0] + 2.25, 'speed': SPD15, 'rollZ0': -0.5, 'rollZ1': 0.5, 'y': 0.03, 's': 1.1}),
               KEPI('kepi15', 'chauffeur'), *[KEPI(f'kepi15{i}', w) for i, (w, p) in enumerate(LINE15)]],
        cams=[C15])
st.cue('engine', 'S15', 0.0, 0.3, D15)
for x_ in (-3.0, -1.65, -0.3, 1.05, 2.4): st.cue('sfx:crunch', 'S15', r(max(0.05, (x_ - (ROLL0[0] + 2.25)) / SPD15)), 0.3)   # (round 1) on each flattening
st.cue('sfx:spring', 'S15', r((-1.65 - (ROLL0[0] + 2.25)) / SPD15 + 0.5), 0.3)

# 16: the sheet was released. Straight down the portico at her: the gendarme by the dark doorway opens his fingers and she drifts toward us on a
#     draught, rocking, tilted and half-curled, the dog-ear and the smear showing, the doorway and his navy uniform behind her, then out at the
#     bottom right over the steps
D16 = st.dur('S16'); REL16 = 0.22
G16 = [-1.2, LAND, -4.75]
PATH16 = [[-0.7, 2.0, -3.8], [-0.95, 1.8, -3.1], [-0.7, 1.62, -2.4], [-0.2, 1.3, -1.6]]
C16 = cam(0.0, [-0.85, 1.95, 0.0], [-0.85, 1.95, -0.1], [-0.75, 1.9, -4.0], [-0.72, 1.85, -3.6], lens=50)
chk('S16', C16['from'], C16['lookAt'], 50, {'gFace': [G16[0], LAND + 2.0, G16[2]], 'sheet0': SHEET_C, 'p1': PATH16[0], 'p2': PATH16[1], 'p3': PATH16[2]})
st.shot('S16', 'grassland', setOpts={'clouds': 26}, actors=[
        act('gendarme2', G16, 30, 'stand', 'neutral', keys=[k(0.0, look=SHEET_C), k(0.0, toon={'reach': {'L': R5(add(SHEET_C, [-0.28, 0.36, 0.0]), 1, 0.06)}, 'hands': {'L': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(REL16, toon={'reach': {'L': R5(add(SHEET_C, [-0.3, 0.4, 0.0]), 1, 0.06)}, 'hands': {'L': 'open'}}, toonDur=0.08), k(r(REL16 + 0.25), look=PATH16[1], lookDur=0.3), k(1.05, look='camera', lookDur=0.2), *blink(1.3, {'lid': 0.5, 'mouth': 'line', 'brow': -0.2})])],
        props=[*COURT(), KEPI('kepi16', 'gendarme2'),
               P('feuille16', 'feuilleSheet', pos=SHEET_C, rot=[0, 0.25, 0.1], opts={**SHC, 'ear0': 0.7, 'curl': [[0.0, 0.0], [REL16, 0.22]], 'wiggle': [[REL16, 0.8]]},
                 keys=[k(REL16, path=PATH16, dur=1.3, ease='inOut'), k(REL16, rotTo=[0.35, 0.7, -0.35], dur=1.3, ease='inOut')])],
        cams=[C16])
st.cue('gust', 'S16', REL16, 0.35, 1.2)

# 17: turned into a dismissal letter. The shop's back office, by a bare paper shelf: the manager's typewriter hammers LICENCIEMENT across her, the
#     dog-ear and the tiny red smear beside the word
D17 = st.dur('S17'); TYPE17 = 0.2
DESK17 = [4.1, 0, -1.7]; TW17 = [4.1, 0.76, -1.62]   # (round 2) the whole desk group moved 1.5 m right: the wall clock no longer haloes his head
SHT17 = [4.1, 1.32, -1.86]
MAN17 = [4.1, 0, -2.55]
C17 = cam(0.0, [3.95, 1.35, 0.8], [3.96, 1.35, 0.7], [4.12, 1.45, -1.9], [4.12, 1.45, -1.9], lens=48)   # (round 1) lower and further: his head in frame, his dark suit behind the white sheet, the typing hands above the captions
chk('S17', C17['from'], C17['lookAt'], 48, {'sheetTop': [SHT17[0], 1.6, SHT17[2]], 'sheetMid': SHT17, 'keys': [TW17[0], 0.98, TW17[2] + 0.12], 'manFace': [MAN17[0], 2.0, MAN17[2]], 'shelf': [3.7, 1.2, -2.45]})
st.shot('S17', 'office', setOpts=SHOP, actors=[
        act('gerant', MAN17, 0, 'stand', 'neutral', keys=[k(0.0, look=[TW17[0], 1.0, TW17[2]])] + [k(r(TYPE17 + 0.09 * j), toon={'reach': {'R': R5([TW17[0] - 0.12 + 0.06 * (j % 3), 1.0 + 0.04 * (j % 2), TW17[2] + 0.1]), 'L': R5([TW17[0] + 0.12 - 0.05 * (j % 2), 1.0 + 0.04 * ((j + 1) % 2), TW17[2] + 0.1])},
            'hands': {'R': 'point', 'L': 'point'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.05) for j in range(14)]),
        ],
        props=[P('bureau17', 'table', pos=DESK17, opts={'w': 1.3, 'd': 0.75, 'h': 0.76, 'color': '#7A5A3C', 'legs': '#4A3424'}),
               P('machine17', 'typewriter', pos=TW17, opts={'hitFrom': TYPE17, 'hitTo': r(TYPE17 + 1.25)}),
               P('lettre17', 'feuilleSheet', pos=SHT17, rot=[-0.22, 0, 0], opts={**SHEET, 'text': 'LICENCIEMENT', 'typeAt': TYPE17, 'typeDur': 1.2}),
               P('etagere17', 'bareShelf', pos=[5.25, 0, -2.5], ry=-15)],
        cams=[C17])
for j in range(12): st.cue('clack', 'S17', r(TYPE17 + 0.1 * j), 0.12)
st.cue('sfx:bell', 'S17', r(TYPE17 + 1.28), 0.25)

# 18: addressed to this man. From the manager's side across the counter: the manager slides her, folded in three, toward him; he takes her at
#     arm's length by the far edge with his left hand, the plastered finger of the right lifted well away
D18 = st.dur('S18'); SLIDE18 = 0.05; TAKE18 = 0.55
# (round 1) over the manager's shoulder (his head and arm at the right edge): he holds the folded letter out over the counter at chest height, the
#            hero takes it at arm's length by the far edge with two fingers of his left hand, the plastered finger of his right hand held up and away
MAN18 = [-0.15, 0, 0.7]; RYM18 = 175                 # (round 1) at the left edge: his shoulder, his arm reaching in with the letter
L18a = [0.36, 1.36, 0.05]; L18b = [0.22, 1.5, -0.38]; L18c = [0.2, 1.56, -0.6]
C18 = cam(0.0, [0.55, 1.85, 1.8], [0.55, 1.85, 1.7], [-0.05, 1.62, -0.7], [-0.05, 1.63, -0.72], lens=46)
chk('S18', C18['from'], C18['lookAt'], 46, {'heroFace': [HERO[0], 2.0, HERO[2]], 'letter': L18b, 'manHead': [MAN18[0], 2.05, MAN18[2]], 'heroFinger': off(HERO, 0, 0.32, 0.42, 1.95)})
st.shot('S18', 'office', setOpts=SHOP, actors=[
        act('gerant', MAN18, RYM18, 'stand', 'neutral', keys=[k(0.0, look=[HERO[0], 2.0, HERO[2]]), k(0.0, toon={'reach': {'R': R5(add(L18a, [-0.12, 0, 0.02]))}, 'hands': {'R': 'pinch'}}, toonDur=0.0),
            k(SLIDE18, toon={'reach': {'R': R5(add(L18b, [-0.14, 0, 0.02]))}, 'hands': {'R': 'pinch'}}, toonDur=0.35, toonEase='out'),
            k(r(TAKE18 + 0.25), toon={'reach': {'R': R5(add(L18b, [-0.3, -0.15, 0.3]))}, 'hands': {'R': 'open'}}, toonDur=0.2)]),
        act('mec', HERO, 0, 'stand', 'unimpressed', keys=[k(0.0, look=L18b),
            k(0.0, toon={'reach': {'R': R5(off(HERO, 0, 0.32, 0.42, 1.95)), 'L': R5(off(HERO, 0, 0.25, -0.3, 1.0))}, 'hands': {'R': 'point', 'L': 'rest'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
            k(r(TAKE18 - 0.12), toon={'reach': {'R': R5(off(HERO, 0, 0.3, 0.5, 2.05)), 'L': R5(add(L18b, [0.18, 0.02, -0.02]), 1, 0.1)}, 'hands': {'R': 'point', 'L': 'pinch'}, 'bend': {'spine': [-0.1, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'wavy', 'brow': 0.5}}, toonDur=0.15),
            k(r(TAKE18 + 0.25), toon={'reach': {'R': R5(off(HERO, 0, 0.3, 0.5, 2.05)), 'L': R5(add(L18c, [0.18, 0.02, -0.02]), 1, 0.1)}, 'hands': {'R': 'point', 'L': 'pinch'}, 'bend': {'spine': [-0.12, 0, 0, 1, None]}}, toonDur=0.25),
            k(r(TAKE18 + 0.5), look='camera', lookDur=0.15), *blink(1.15, {'lid': 0.4, 'mouth': 'line', 'brow': 0.3})])],
        props=[*SHOP_PROPS(), PLASTER('pansement18'),
               P('lettre18', 'feuilleSheet', pos=L18a, rot=[0.1, 0.25, 0.05], opts={'w': 0.56, 'h': 0.75, 'folded': True}, keys=[k(SLIDE18, to=L18b, dur=0.36, ease='out'), k(r(TAKE18 + 0.25), to=L18c, dur=0.25, ease='inOut')])],
        cams=[C18])
st.cue('sfx:paper', 'S18', SLIDE18, 0.35); st.cue('sfx:paper', 'S18', TAKE18, 0.3)

# 19: he sold shredders. Exactly the framing of shot 1: the demo shredder is gone, only its price tag lies on the plinth, the wall behind is bare;
#     he holds the unfolded letter up to us in his left hand (LICENCIEMENT, the dog-ear, the tiny smear), the plastered finger raised away; a beat
D19 = st.dur('S19')
LET19 = [0.06, 1.42, -0.5]
chk('S19', C1['from'], C1['lookAt'], 42, {'face': [HERO[0], 2.0, HERO[2]], 'letterTop': [LET19[0], 1.7, LET19[2]], 'letterMid': LET19, 'plinthTag': [DEMO[0], 0.34, DEMO[2]], 'finger': off(HERO, 0, 0.32, 0.28, 1.95)})
st.shot('S19', 'office', setOpts=SHOP, actors=[
        act('mec', HERO, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': R5([LET19[0] + 0.19, 1.66, LET19[2] + 0.04], 1, 0.06), 'R': R5(off(HERO, 0, 0.32, 0.28, 1.95))}, 'hands': {'L': 'pinch', 'R': 'point'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.15}}, toonDur=0.0),
            k(0.75, toon={'sq': [1.015, 1.02, 1.015]}, toonDur=0.35, toonEase='inOut', keepPose=True), k(1.1, toon={'sq': [1, 1, 1]}, toonDur=0.3, keepPose=True),   # (round 2) a breath
            k(1.3, toon={'face': {'lid': 1.0, 'mouth': 'line', 'brow': -0.15}}, toonDur=0.14, keepPose=True), k(1.52, toon={'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.15}}, toonDur=0.14, keepPose=True),
            k(1.62, look=[DEMO[0], 1.1, DEMO[2]], lookDur=0.08), k(1.86, look='camera', lookDur=0.08), k(1.95, toon={'face': {'lid': 0.5, 'mouth': 'flat', 'brow': -0.25}}, toonDur=0.25, keepPose=True)])],
        props=[*SHOP_PROPS(empty=True, demo=False), PLASTER('pansement19'),   # (round 1) the plinth darker, its price tag propped up and three times bigger
               P('lettre19', 'feuilleSheet', pos=LET19, rot=[0, -0.08, 0.04], opts={**SHEET, 'text': 'LICENCIEMENT', 'smearS': 1.4})],
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
    'stagiaire': {'preset': 'boss', 'outfit': 'suit', 'suit': '#B08A3A', 'pants': '#6A5228', 'tie': '#7A2333', 'lapel': '#8E6E2C', 'shirt': '#F4F1E8', 'hair': 'slick', 'hairColor': '#D9B45A', 'facial': 'none', 'glasses': True, 'seed': 962,   # (round 1) mustard, blond, clean-shaven
                  'build': {'width': 0.92, 'headWidth': 1.2}, 'toon': EX},
    'directeur': {'preset': 'boss', 'seed': 963, 'suit': '#2E3A4E', 'tie': '#C8A030', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'procureur': {'preset': 'avocat', 'seed': 964, 'suit': '#9A2228', 'pants': '#7A1A20', 'lapel': '#7A1A20', 'cuff': '#F4F1E8', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},   # (round 1) a red robe
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
    'gerant': {'preset': 'boss', 'seed': 985, 'suit': '#5A606B', 'lapel': '#4A4F58', 'tie': '#7A2333', 'facial': 'mustache', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
})
