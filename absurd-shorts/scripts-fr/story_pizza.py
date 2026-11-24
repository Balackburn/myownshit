#!/usr/bin/env python3
"""La pizza (story 91, cycle 50; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man got his pizza cold. The president spoke of national shame. The army re-delivered it by fighter jet. The pizza arrived in flames. It
braked with the street. The pavement arrived before it. This man found it overcooked. The general staff concluded: cool it on the way. A missile
took it up to space. It made a crater in his garden. His front door is what is left. At the bottom of the crater: sixty degrees. The president
opened the crater. The other countries order their pizzas cold. It took this man three hours to climb down. One star. It was cold.
Staging: at his front door he holds an open pizza box; the lid creaks up by itself, a frost cloud puffs out in his face (he squashes, shivers, his
breath steams) and the big dial of the stick thermometer in the pizza swings hard to blue; slow push-in to his flat stare. In the press room the
president in an invented violet-and-gold sash pounds the podium (wound up, stretched, then a squash) beside the open frosted box on a navy
exhibit stand, its dial blue; invented violet-and-gold flags behind. On an airbase two soldiers hang ONE pizza box on its edge under the wing of a plain jet
(no roundels, no lettering) like a missile, its printed lid to us; one slaps it twice, the other gives a thumbs up; the jet stretches like rubber, blasts off down the
runway into a pastel sky, the box glowing red then catching fire, the camera racing beside it. In front of his house the flaming box streaks in
from the sky and slams onto his doorstep (squash, bounce) while he waits in the doorway, napkin tucked in, knife and fork up: he jumps out of
his skin and lands back in the same pose (BRÛLÉE). From high above the street: a scorched furrow down the middle of the road swerves onto his
doorstep, the parked cars pushed askew, lampposts bent, the pavement peeled off to bare earth, nobody about; the nearest lamppost finishes
drooping with a wobble while a hubcap rolls away. The pavement lies rolled up like a carpet against his door, the smoking box on top; he rises
slowly from behind the roll, eyes popping over it. Close: he holds up a charred black slice, it crumbles to dust in his fingers, a black puff;
in the box beside him the dial reads red. In the war room a general's arm stretches like rubber to push a little pizza-box token up a chalk
arrow from a drawn house, past the clouds, to a big snowflake drawn in space at the top of the map; two generals across the table nod in sync.
In space a white missile with the box strapped to its nose climbs past a satellite, the Earth curving below; frost spreads over the box and
icicles shoot out; the satellite turns its head to watch (a double take). In front of his house: a flash and a towering dust cloud behind the
roof from the back garden, the camera shakes, he does not move. High above as the dust clears: a deep clean round crater where the house and
garden were, his door frame alone on the rim with him in it, the door creaking open on its own, nobody else around. At the very bottom: the
intact open box, the dial swinging down from red and settling exactly on green with a sparkle and steam, a kneeling soldier's thumbs up
(LIVRÉE). On the rim the president snips the ribbon with giant scissors (confetti), arms flung up, the band playing, him standing in his door
frame behind them. A row of foreign front doors under invented flags: each official holds a frosted box (dial blue), scribbles on the
courier's clipboard and nods, the three in sync. Time-lapse from very high: he climbs down the rope ladder into the crater, a dot, while the sun
races round the sky and the shadows sweep the crater (two day-night cycles). At the bottom in the low gold of evening: close on his phone, he
taps the first of five stars with the frozen slice (it clacks, the star pops yellow); then his deadpan face, the stiff frosted slice in his
hand, his breath steaming, and the dial in the box at his feet blue again.
Natural look; cycle 50: props_pizza.js (pizzaThermo, pizzaBox, pizzaSlice, ratingPhone, jetBox, pizzaMissile, pizzaWarMap, heroHouse, townLamp,
pavementRoll, pizzaTown, craterLadder, embassyDoor, exhibitStand, sunRacer); plainJet (props_chat, inside jetBox, its flank lettering hidden too),
cottage, tree, car, cumulus, flameField, speedLines, fork, knife (props.js), softDust, softWisp, twinkle (props_barbecue), timedBurst (props_flaque),
dustCloud, ribbonCut (props_rambarde), bigScissors (props_baillement), bandInstr, epaulettes (props_centime), kepi (props_conseiller), armyHelmet
(props_guepe), satellite (props_lunettes), earthGlobe (props_vp), confettiPuff (props_feuille), clipBoard (props_bus) reused; pressRoom, office,
runway, spaceDark, grassland, skyHigh (no cloud deck: the street world brings its own ground so the crater can go below it) sets.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.83) and heads below the card band (0.07-0.18) when a card stamps (the action is over before each card); every camera checked
with project() before stills; the thermometer is a big dial with a bulb in the state colour so the gag reads on a phone, turned to each camera;
every extra cast entry has a preset; nobody is shown hurt (the street, the garden and the crater are empty, the hero is never touched by fire or
blast); the jet is a plainJet with its lettering hidden too; flags and sashes are invented pairs (violet and gold, teal and pink, orange and
navy, lime and plum), no real flag, brand or organisation, no English on screen, no words on the boxes; animated materials unique; timedBurst, not
explosionBurst; one flash; the day-night flips at under three a second; real evening and time-lapse through per-shot settings; every end gag has
its own close camera; one clear cartoon extreme per shot (squash, stretch, takes, a rubber arm, a jet that stretches)."""
from story_kit import *
import math

st = Story('pizza', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 17)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, c, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(c['from'], c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
    if c.get('to'): CHECKS.append(f"{sid}(end): " + ' | '.join(f"{n} {project(c['to'], c.get('lookAt2') or c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
def R5(p, w=1, s=0.04): return [*p, w, s]
EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def TK(t, reach=None, hands=None, face=None, sq=None, bend=None, d=0.12, e='inOut', keep=False):
    tn = {}
    if reach: tn['reach'] = reach
    if hands: tn['hands'] = hands
    if face: tn['face'] = face
    if sq: tn['sq'] = list(sq)
    if bend: tn['bend'] = bend
    return k(t, toon=tn, toonDur=d, toonEase=e, **({'keepPose': True} if keep else {}))
def blink(t, face): return [k(t, toon={'face': {**face, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face}, toonDur=0.06, keepPose=True)]
def SP(a): return [a, 0, 0, 1, None]   # a bend value (pitch)
def BREATHE(t0, t1, every=0.55, a=0.012): return [k(r(t0 + i * every), toon={'sq': [1 - a * 0.5, 1 + a, 1 - a * 0.5] if i % 2 == 0 else [1, 1, 1]}, toonDur=r(every * 0.9), toonEase='inOut', keepPose=True) for i in range(int((t1 - t0) / every) + 1)]   # (review 1) a breath in the holds
def STEAM(sid, who, times, d=(0.28, -0.14, 0.12)): return P(f'souffle{sid}', 'breathPuffs', on={'actor': who, 'joint': 'head', 'offset': [0.06, 0.1, 0.19]}, opts={'times': times, 'dir': list(d), 's': 0.06, 'life': 0.8})   # (review 1) small puffs leaving the mouth, no glow

# ---------------------------------------------------------------- the street world (props_pizza.pizzaTown): road along X (z 0..8), near pavement z -2.6..0,
# his house at x 0 with its front wall at FZ, the door in the middle; the crater (later) centred at CC, radius CR, depth CD
SET = 'skyHigh'; SKY = ['#86C0DF', '#C6E3EF']
SETO = {'layer': False, 'sky': SKY, 'below': '#C6E3EF', 'fogNear': 300, 'fogFar': 1500}
FZ = -3.2; DOOR = [0.0, 0, FZ]
CC = [0.0, -14.8]; CR = 11.6; CD = 14.0
CRATER = {'c': CC, 'R': CR, 'D': CD}
LTOP = [0.0, 0.05, r(FZ - 0.35)]; LBOT = [0.0, -CD, -5.9]
SUN = {'sunDir': [0.55, 0.75, 0.75]}
def TOWN(sid, **o): return P(f'ville{sid}', 'pizzaTown', pos=[0, 0, 0], opts=o)
DONE = {'furrow': True, 'peel': [1.6, 46.0], 'nudge': True, 'bent': True, 'door': -1.3}   # the street after the landing (S05 on)
HERO_DOOR = [0.0, 0, -3.3]          # standing in his doorway, facing the road
BOXC = lambda tag, **o: {'thermo': -1, 'tR': 0.15, **o}

# ---------------------------------------------------------------- invented flags (checked: no real flag is violet and gold, teal and pink, orange over navy, lime and plum)
HOME = ['#6A3FA0', '#F2C94C']
FLAGS = [['#1E7A8C', '#E88AA8'], ['#E07A1F', '#1F2E5C'], ['#8DBE3A', '#6A2E5A']]

for g_ in [('S01', 0.55, 'mec', 'frost'), ('S02', 1.32, 'president', 'pound'), ('S03', 0.55, 'soldat1', 'bolt'), ('S04', 0.45, 'mec', 'jump'), ('S06', 0.9, 'mec', 'peek'),
           ('S07', 1.15, 'mec', 'crumble'), ('S08', 2.05, 'general1', 'push'), ('S12', 1.45, 'soldat3', 'thumb'), ('S13', 1.15, 'president', 'snip'), ('S16', 2.4, 'mec', 'deadpan')]:
    st.gag(*g_)

# 1: the hook. At his front door, facing us, he holds the closed pizza box at chest height; the lid creaks open on its own, a frost cloud bursts
#    out into his face: he squashes back (eyes wide, shiver, his breath steaming) while the big dial of the thermometer in the pizza swings hard to
#    blue with an overshoot; slow push-in to his flat stare at us
D1 = st.dur('S01'); OPEN1 = 0.3
HERO1 = list(HERO_DOOR)
BOX1 = [0.0, 1.24, -2.66]                                                # the box held out in front of him (pivot at its bottom middle)
C1 = cam(0.0, [0.35, 1.72, 0.75], [0.26, 1.78, 0.3], [0.0, 1.68, -3.0], [0.0, 1.74, -3.0], lens=40)
HB1 = {'L': R5(add(BOX1, [0.33, 0.06, 0.02])), 'R': R5(add(BOX1, [-0.33, 0.06, 0.02]))}
chk('S01', C1, {'face': add(HERO1, [0, 2.05, 0]), 'hairTop': add(HERO1, [0, 2.38, 0]), 'box': BOX1, 'dial': add(BOX1, [0.1, 0.56, 0.06]), 'lidTop': add(BOX1, [0, 0.62, -0.3])})
COLD = {'lid': 0.0, 'pop': 0.35, 'mouth': 'O', 'brow': 0.8}
FLAT = {'lid': 0.45, 'mouth': 'line', 'brow': -0.15}
st.shot('S01', SET, setOpts=SETO, lighting='day', look=SUN, actors=[
        act('mec', HERO1, 0, 'stand', 'neutral', keys=[k(0.0, look=add(BOX1, [0, 0.1, 0])),
            TK(0.0, HB1, {'L': 'grip', 'R': 'grip'}, {'lid': 0.25, 'mouth': 'smile', 'brow': 0.2}, d=0.0),
            TK(r(OPEN1 + 0.05), {'L': R5(add(HB1['L'][:3], [0, 0.04, 0.05])), 'R': R5(add(HB1['R'][:3], [0, 0.04, 0.05]))}, {'L': 'grip', 'R': 'grip'}, COLD, (1.12, 0.84, 1.12), {'spine': SP(-0.22), 'neck': SP(-0.25)}, d=0.06, e='out'),   # the frost hits: squashed back
            TK(r(OPEN1 + 0.32), HB1, {'L': 'grip', 'R': 'grip'}, {**COLD, 'pop': 0.15}, (0.97, 1.04, 0.97), {'spine': SP(-0.05)}, d=0.18),
            TK(0.95, HB1, {'L': 'grip', 'R': 'grip'}, FLAT, (1, 1, 1), {'spine': SP(0.0), 'neck': SP(0.0)}, d=0.25),
            k(r(OPEN1 + 0.05), fx={'shiver': True}), k(0.95, look='camera', lookDur=0.15), *blink(1.7, FLAT)])],
        props=[TOWN('S01', door=-1.3), STEAM('1', 'mec', [0.5, 1.1, 1.75]),
               P('boite1', 'pizzaBox', pos=BOX1, rot=[0.32, 0, 0], opts=BOXC('1', side=1, open=[[0, 0.0], [r(OPEN1 - 0.08), 0.12], [OPEN1, 1.8]], thermo=[[0, -0.5], [r(OPEN1 + 0.03), -1.05]], tBlend=0.1, tAt=[0.2, 0.08], tTilt=-0.32, tR=0.16, tLen=0.22, puffAt=OPEN1, puffS=0.16, frost=[[0, 0.0], [r(OPEN1 + 0.05), 0.95]]))],
        cams=[C1])
st.cue('sfx:squeak', 'S01', 0.12, 0.3); st.cue('sfx:poof', 'S01', OPEN1, 0.45); st.cue('whoosh', 'S01', OPEN1, 0.25, 0.4, 600, 3000); st.cue('sfx:boing', 'S01', r(OPEN1 + 0.1), 0.2)

# 2: the president spoke of national shame. The press room, low and frontal: the president in his violet-and-gold sash at the podium, the open
#    frosted box on a navy exhibit stand beside him tilted to the room, its dial blue; invented flags behind; on « honte » he winds up (stretched
#    tall, fist high) and pounds the podium: a squash, the podium and the box jump, a cold puff, the needle rattles in the blue
D2 = st.dur('S02'); POUND2 = 1.32
PRESS = {'backdrop': 'PRÉSIDENCE', 'fontScale': 0.7, 'fg': 'rgba(255,255,255,0.22)', 'chairs': False, 'flags': False}
PRES2 = [-0.12, 0, -2.45]; STAND2 = [0.86, 0, -2.0]; BOX2 = [0.86, 1.12, -2.0]
C2 = cam(0.0, [0.36, 1.5, 2.0], [0.36, 1.52, 1.65], [0.36, 1.66, -2.4], [0.36, 1.68, -2.4], lens=40)   # (review 1) higher and tighter: less empty navy podium at the bottom
chk('S02', C2, {'presFace': add(PRES2, [0, 2.05, 0]), 'presTop': add(PRES2, [0, 2.45, 0]), 'fistUp': add(PRES2, [0.05, 2.75, 0.45]), 'box': BOX2, 'dial': add(BOX2, [0.1, 0.52, 0.0]), 'podium': [0, 1.15, -2.0], 'flagL': [-1.5, 1.4, -2.6], 'flagR': [1.5, 1.4, -2.6]})
ANGRY = {'lid': 0.15, 'mouth': 'scream', 'brow': -0.9}
st.shot('S02', 'pressRoom', setOpts=PRESS, actors=[
        act('president', PRES2, 0, 'stand', 'angry', keys=[k(0.0, look='camera'),
            TK(0.0, {'R': R5([-0.42, 1.2, -2.05]), 'L': R5([0.2, 1.2, -2.05])}, {'R': 'rest', 'L': 'rest'}, {'lid': 0.3, 'mouth': 'line', 'brow': -0.6}, d=0.0),
            TK(0.55, {'R': R5([-0.45, 1.22, -2.05]), 'L': R5([0.55, 1.45, -2.1])}, {'R': 'rest', 'L': 'point'}, {'lid': 0.2, 'mouth': 'O', 'brow': -0.7}, d=0.2),   # points at the box
            k(0.5, look=add(BOX2, [0, 0.4, 0]), lookDur=0.15), k(0.95, look='camera', lookDur=0.1),
            TK(r(POUND2 - 0.3), {'R': R5([-0.3, 2.85, -2.2]), 'L': R5([0.25, 1.2, -2.05])}, {'R': 'fist', 'L': 'rest'}, ANGRY, (0.9, 1.14, 0.9), {'spine': SP(-0.12)}, d=0.18, e='out'),
            TK(r(POUND2 - 0.03), {'R': R5([-0.2, 1.3, -1.95])}, {'R': 'fist'}, ANGRY, (0.98, 1.02, 0.98), {'spine': SP(0.2)}, d=0.05, e='in'),
            TK(POUND2, {'R': R5([-0.2, 1.17, -1.95])}, {'R': 'fist'}, {**ANGRY, 'lid': 0.05}, (1.14, 0.84, 1.14), {'spine': SP(0.32)}, d=0.04, e='out'),
            TK(r(POUND2 + 0.3), {'R': R5([-0.3, 1.25, -1.98])}, {'R': 'fist'}, {'lid': 0.25, 'mouth': 'clench', 'brow': -0.8}, (1, 1, 1), {'spine': SP(0.08)}, d=0.2),
            *blink(2.1, {'lid': 0.25, 'mouth': 'clench', 'brow': -0.8})])],
        props=[*[P(f'drapeau2{j}', 'flag', pos=[x, 0, -2.78], scale=1.55, opts={'colors': HOME, 'poleColor': '#C9A646', 'poleR': 0.022}) for j, x in enumerate((-0.72, 1.38))],
               P('stand2', 'exhibitStand', pos=STAND2, ry=-14, keys=[k(POUND2, squash=[1.04, 0.92, 1.04], dur=0.3)]),
               P('boite2', 'pizzaBox', pos=BOX2, ry=-14, rot=[0.5, math.radians(-14), 0], opts=BOXC('2', open=2.0, frost=0.9, thermo=[[0, -1.0], [POUND2, -0.7], [r(POUND2 + 0.12), -1.0]], tTilt=-0.5, tAt=[0.1, 0.05], puffAt=r(POUND2 + 0.02)),
                 keys=[k(POUND2, to=add(BOX2, [0, 0.0, 0]), dur=0.25, arc=0.12), k(POUND2, squash=[1.1, 0.8, 1.1], dur=0.3)]),
               P('podiumHop2', 'softDust', pos=[-0.2, 1.2, -1.9], opts={'at': POUND2, 'n': 6, 'size': 0.18, 'rise': 0.2, 'spread': 0.4, 'life': 0.5, 'color': '#F2EEE6', 'opacity': 0.6})],
        fx=[{'type': 'shake', 'at': POUND2, 'dur': 0.15, 'amount': 0.012}],
        cams=[C2])
st.cue('whoosh', 'S02', r(POUND2 - 0.2), 0.2); st.cue('thud', 'S02', POUND2, 0.6); st.cue('sfx:rattle', 'S02', r(POUND2 + 0.05), 0.2)

# 3: the army re-delivered it by fighter jet. (a) Low under the left wing of a plain jet on the runway: a pizza box bolted on a pylon like a missile;
#    a soldier slaps it twice to check, another salutes with a thumbs up. (b) Racing beside it down the runway: the jet stretches like rubber and
#    blasts off, speed lines, the box glowing red-hot, then on fire as it climbs into a pastel sky
D3 = st.dur('S03'); GO3 = 0.95; CUT3 = 0.95
JS = 1.4                                                               # the jet's scale: its wing at 2.2 m, over the soldiers' heads
JET0 = [0.0, 0, 0.0]; JET1 = [0.0, 7.0, 95.0]   # (review 3) a shorter run: the chase camera no longer flies into the far hills
BOXJ = [r(3.1 * JS), r((1.1 - 0.403 - 0.02) * JS), r(-1.1 * JS)]       # the middle of the box hanging on its edge under the left wing (world, jet at rest)
SOL1 = [r(BOXJ[0] - 0.55), 0, r(BOXJ[2] - 0.6)]; SOL2 = [r(BOXJ[0] + 0.2), 0, r(BOXJ[2] - 1.4)]   # (review 3) soldier 1 beside the box, turned three-quarter to profile
# (review 1) (a) low, close and three-quarter on the pylon: the box a third of the frame, the soldiers' slap and thumbs up against the sky
C3a = cam(0.0, add(BOXJ, [2.0, -0.5, 2.8]), add(BOXJ, [1.88, -0.5, 2.62]), add(BOXJ, [-0.1, 0.3, -0.5]), add(BOXJ, [-0.1, 0.31, -0.5]), lens=50)
# (review 1) (b) side-on, locked beside the box as the jet takes off (same cubic ease as the jet's move): the stretch, the glow and the fire read on the sky
OFF3 = [9.0, 2.35, -12.0]; LOFF3 = [5.21, 1.5, -2.79]   # (review 2) a chase camera just behind and outside the wing: the box big at the right, the fuselage, canopy and nose ahead
C3b = cam(CUT3, add(JET0, OFF3), add(JET1, OFF3), add(JET0, LOFF3), add(JET1, LOFF3), lens=26, ease='in')
chk('S03a', C3a, {'box': BOXJ, 'boxTop': add(BOXJ, [0, 0.48, 0]), 'boxBot': add(BOXJ, [0, -0.48, 0]), 'sol1Face': add(SOL1, [0, 2.05, 0]), 'sol1Hand': add(BOXJ, [-0.15, 0.1, 0.12]), 'sol2Face': add(SOL2, [0, 2.05, 0]), 'sol2Thumb': off(SOL2, -30, 0.5, -0.3, 1.7)})
chk('S03b', C3b, {'box': BOXJ, 'boxTop': add(BOXJ, [0, 0.5, 0]), 'boxBot': add(BOXJ, [0, -0.5, 0]), 'canopy': [0, 3.2, 7.3], 'nose': [0, 2.2, 13.3], 'flameTop': add(BOXJ, [0, 1.3, 0])})
SAL3 = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.3}
TOPB = add(BOXJ, [-0.2, 0.2, 0.2]); UPB = add(BOXJ, [-0.4, 0.65, 0.35])
st.shot('S03', 'runway', setOpts={'sky': ['#F4C6D2', '#C6E6F4']}, look={'sunDir': [0.6, 0.7, 0.6]}, actors=[
        act('soldat1', SOL1, 80, 'stand', 'determined', keys=[k(0.0, look=TOPB),   # (review 3) one clear slap: wind-up high, slap, the box rocks
            TK(0.0, {'R': R5(add(BOXJ, [-0.3, 0.1, 0.05])), 'L': R5(add(BOXJ, [-0.4, -0.3, 0.3]))}, {'R': 'open', 'L': 'rest'}, {'lid': 0.3, 'mouth': 'line', 'brow': -0.4}, d=0.0),
            TK(0.25, {'R': R5(add(BOXJ, [-0.55, 0.75, 0.25]))}, {'R': 'open'}, {'lid': 0.2, 'mouth': 'line', 'brow': -0.6}, (0.94, 1.07, 0.94), d=0.15, e='out'),
            TK(0.42, {'R': R5(add(BOXJ, [-0.22, 0.12, 0.05]))}, {'R': 'open'}, {'lid': 0.1, 'mouth': 'O', 'brow': 0.2}, (1.1, 0.9, 1.1), d=0.05, e='in'),
            TK(0.6, {'R': R5(add(BOXJ, [-0.4, 0.15, 0.2]))}, {'R': 'open'}, {'lid': 0.1, 'mouth': 'smile', 'brow': 0.3}, (1, 1, 1), d=0.15),
            k(0.6, look='camera', lookDur=0.12), k(CUT3, visible=False)]),
        act('soldat2', SOL2, -30, 'stand', 'happy', keys=[k(0.0, look='camera'),
            TK(0.0, {'R': R5(off(SOL2, -30, 0.3, 0.3, 1.0)), 'L': R5(off(SOL2, -30, 0.45, -0.3, 1.5))}, {'R': 'rest', 'L': 'thumbUp'}, SAL3, d=0.0),
            TK(0.45, {'L': R5(off(SOL2, -30, 0.5, -0.3, 1.85))}, {'L': 'thumbUp'}, {'lid': 0.1, 'mouth': 'bigsmile', 'brow': 0.5}, (0.93, 1.08, 0.93), d=0.1, e='out'),
            TK(0.7, {'L': R5(off(SOL2, -30, 0.5, -0.3, 1.75))}, {'L': 'thumbUp'}, SAL3, (1, 1, 1), d=0.15), k(CUT3, visible=False)])],   # (review 3) the soldiers leave the frame with the cut (one walked through the chase)
        props=[P('jet3', 'jetBox', pos=JET0, scale=JS, opts={'gear': True, 'upright': True, 'boxYaw': 1.45, 'boxS': 1.3, 'slaps': [0.42], 'slapA': 0.4, 'burner': 0.0, 'glow': [[0, 0], [r(GO3 + 0.15), 0], [r(GO3 + 0.55), 0.55]], 'flames': [[r(GO3 + 0.68), 9]], 'smoke': True,
                 'stretch': [[0, 0], [r(GO3 - 0.08), -0.1], [GO3, 0.0], [r(GO3 + 0.05), 0.7], [r(GO3 + 0.14), 0.12], [r(GO3 + 0.26), 0.0]], 'shake': [[0.0, GO3]]},
                 keys=[k(GO3, to=JET1, dur=r(D3 - GO3), ease='in')]),
               P('vitesse3', 'speedLines', pos=[6.5, 1.2, -3.0], ry=90, scale=2.5, opts={'count': 10, 'length': 5.0, 'dir': -1}, keys=[k(0.0, visible=False), k(r(CUT3 + 0.08), visible=True), k(CUT3, to=[6.5, 9.2, 137.0], dur=r(D3 - CUT3), ease='in')])],
        cams=[C3a, C3b])
st.cue('sfx:bonk', 'S03', 0.32, 0.3); st.cue('sfx:bonk', 'S03', 0.55, 0.3); st.cue('sfx:boing', 'S03', r(GO3 + 0.1), 0.2); st.cue('sfx:jet', 'S03', GO3, 0.6); st.cue('whoosh', 'S03', CUT3, 0.4, 0.6, 300, 2500)

# 4: the pizza arrived in flames. Static wide from the road: he waits in his doorway, napkin tucked in his collar, knife and fork up; the flaming box
#    streaks down out of the sky and slams onto his doorstep (squash, bounce, sparks); he jumps out of his skin (stretched up, eyes out) and lands
#    back in exactly the same pose; the fire crackles a metre in front of him (BRÛLÉE once it has settled)
D4 = st.dur('S04'); HIT4 = 0.3
HERO4 = list(HERO_DOOR); STEP4 = [1.0, 0.14, -1.6]
C4 = cam(0.0, [1.35, 1.3, 5.6], [1.3, 1.3, 5.45], [0.0, 1.32, -3.0], [0.0, 1.32, -3.0], lens=40)
chk('S04', C4, {'face': add(HERO4, [0, 2.05, 0]), 'hairTop': add(HERO4, [0, 2.45, 0]), 'jumpTop': add(HERO4, [0, 2.95, 0]), 'box': STEP4, 'flameTop': add(STEP4, [0, 0.7, 0]), 'boxStart': [9.0, 8.0, 3.0]})
FORK4 = {'R': R5(off(HERO4, 0, 0.35, 0.28, 1.45)), 'L': R5(off(HERO4, 0, 0.35, -0.28, 1.45))}
READY = {'lid': 0.15, 'mouth': 'smile', 'brow': 0.35}
st.shot('S04', SET, setOpts={**SETO}, lighting='day', look=SUN, actors=[
        act('mec', HERO4, 0, 'stand', 'happy', keys=[k(0.0, look=[6, 6, 2]), k(0.12, look=STEP4, lookDur=0.12),
            TK(0.0, FORK4, {'R': 'grip', 'L': 'grip'}, READY, d=0.0),
            TK(r(HIT4 + 0.03), {'R': R5(off(HERO4, 0, 0.25, 0.45, 2.2)), 'L': R5(off(HERO4, 0, 0.25, -0.45, 2.2))}, {'R': 'grip', 'L': 'grip'}, {'lid': 0.0, 'pop': 0.6, 'mouth': 'O', 'brow': 1.0}, (0.84, 1.22, 0.84), d=0.05, e='out'),
            k(r(HIT4 + 0.03), to=add(HERO4, [0, 0.45, -0.05]), dur=0.12, ease='out', glide=True, face='keep'), k(r(HIT4 + 0.2), to=HERO4, dur=0.14, ease='in', glide=True, face='keep'),
            TK(r(HIT4 + 0.34), FORK4, {'R': 'grip', 'L': 'grip'}, {'lid': 0.1, 'pop': 0.2, 'mouth': 'O', 'brow': 0.6}, (1.12, 0.86, 1.12), d=0.05, e='in'),
            TK(r(HIT4 + 0.55), FORK4, {'R': 'grip', 'L': 'grip'}, READY, (1, 1, 1), d=0.15),
            k(0.85, look='camera', lookDur=0.15), *blink(1.25, READY), k(1.45, look=STEP4, lookDur=0.15), TK(1.45, face={'lid': 0.3, 'mouth': 'smile', 'brow': 0.6}, bend={'neck': SP(0.25)}, d=0.15, keep=True), k(1.75, look='camera', lookDur=0.12), TK(1.75, face=READY, bend={'neck': SP(0.0)}, d=0.12, keep=True), *BREATHE(0.95, D4, 0.5, 0.025)])],   # (review 2) a glance down at the fire and back: a beat in the hold
        props=[TOWN('S04', door=-1.3),
               P('boite4', 'pizzaBox', pos=[5.2, 7.2, -2.6], ry=25, opts={'pizza': False, 'fire': True, 'smoke': True, 'glow': 0.6},   # (review 1) it streaks in on an arc inside the frame, squashes, bounces once
                 keys=[k(0.0, path=[[3.6, 4.6, -2.2], [2.2, 2.2, -1.9], STEP4], dur=HIT4, ease='linear'), k(HIT4, squash=[1.4, 0.5, 1.4], dur=0.3), k(HIT4, rotTo=[0, math.radians(8), 0], dur=0.2),
                       k(r(HIT4 + 0.05), to=add(STEP4, [0.25, 0, 0.1]), dur=0.25, arc=0.4, ease='linear'), k(r(HIT4 + 0.3), squash=[1.15, 0.8, 1.15], dur=0.25)]),
               P('trainee4', 'smearArc', pos=[0, 0, 0], opts={'pts': [[3.6, 4.6, -2.2], [2.2, 2.2, -1.9], add(STEP4, [0, 0.1, 0])], 'win': [0.12, r(HIT4 + 0.04)], 'color': '#FF8A2A', 'r': 0.12, 'opacity': 0.8}),
               P('fourchette4', 'fork', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.02, 0.0], 'rot': [3.1416, 0, 0]}, scale=1.8),
               P('couteau4', 'knife', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, 0.02, 0.0], 'rot': [3.1416, 0, 0]}, scale=1.8),
               P('serviette4b', 'napkinBib', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.42, 0.2]}),
               P('etincelles4', 'softDust', pos=add(STEP4, [0, 0.1, 0]), opts={'at': HIT4, 'n': 12, 'size': 0.25, 'rise': 0.5, 'spread': 0.9, 'life': 0.6, 'color': '#FFB04A', 'opacity': 0.9})],
        cams=[C4])
st.card('S04', 'BRÛLÉE', at=1.0)
st.cue('whoosh', 'S04', 0.0, 0.3, 0.3, 400, 2000); st.cue('thud', 'S04', HIT4, 0.7); st.cue('sfx:boing', 'S04', r(HIT4 + 0.03), 0.25); st.cue('gust', 'S04', HIT4, 0.25, 1.6)

# 5: it braked with the street. From high above the road, looking down its length: a scorched furrow ploughed down the middle swerves onto his
#    doorstep, smoke rising from it; the parked cars pushed askew, the lampposts bent over, the pavement peeled off to bare earth, nobody about; the
#    nearest lamppost finishes drooping with a wobble while a hubcap rolls away across the road
D5 = st.dur('S05')
C5 = cam(0.0, [34.0, 27.0, 2.4], [27.0, 21.0, 2.0], [4.0, 0.0, 1.2], [3.0, 0.0, 0.6], lens=44)
LAMP5 = [15.5, 0.14, -0.45]
chk('S05', C5, {'doorstep': [0, 0.2, -2.6], 'roofTop': [0, 5.5, -6.7], 'furrowNear': [26, 0.1, 4.0], 'furrowFar': [8, 0.1, 3.4], 'lamp5top': add(LAMP5, [0, 4.3, 0]), 'lamp5droop': add(LAMP5, [0, 3.6, 2.4]), 'hubcap0': [21, 0.6, 6.2], 'hubcap1': [10, 0.6, 1.9]})
st.shot('S05', SET, setOpts=SETO, lighting='day', look=SUN, actors=[],
        props=[TOWN('S05', **DONE, roll=True, rollAt=[0.0, -1.15]),
               P('boite5', 'pizzaBox', pos=[0.0, 1.75, -1.15], ry=10, opts={'pizza': False, 'scorch': True, 'smoke': True, 'fire': True}),
               P('lampe5', 'townLamp', pos=LAMP5, opts={'droop': [[0, 0.15], [0.2, 0.15], [0.5, 1.45]], 'droopBlend': 0.3, 'droopWob': 0.3}),   # (review 1) the near lamppost droops over the road with a springy overshoot
               P('enjoliveur5', 'hubcap', pos=[19.0, 1.55, 6.6], ry=90, scale=7.0, opts={'spin': 5, 'wobble': 0.45}, keys=[k(0.0, to=[9.0, 1.55, 1.4], dur=D5, ease='out')])],   # (review 1) a big hubcap rolling across, the moving focus
        cams=[C5])
st.cue('sfx:squeak', 'S05', 0.15, 0.3); st.cue('sfx:boing', 'S05', 0.5, 0.15); st.cue('gust', 'S05', 0.0, 0.15, 1.5)

# 6: the pavement arrived before it. From the road, low: the pavement rolled up like a big carpet against his front door, the smoking box on top
#    of the roll; slowly he rises from behind it (stretched, eyes popping over the top), then stares at us
D6 = st.dur('S06'); UP6 = 0.75; HOLD6 = 1.12
ROLL = [0.0, -1.15]; ROLLR = 0.85   # (review 1) the roll a step out from the door: he rises behind it under the open sky, not into the lintel
HERO6 = [0.1, -0.75, -2.45]   # (control 4) a little left, the box further right: both eyes and the mouth clear
# (review 2) turned to the right so the roll's spiral end shows (a rolled carpet, not a wall); his head rises near frame centre
C6 = cam(0.0, [2.8, 1.6, 2.4], [2.68, 1.61, 2.25], [0.5, 1.75, -2.0], [0.5, 1.76, -2.0], lens=44)
BOX6 = [1.42, 1.74, -1.2]
chk('S06', C6, {'eyesPeek': add(HERO6, [0, 0.55 + 2.15, 0]), 'facePop': add(HERO6, [0, 0.8 + 2.05, 0]), 'hairPop': add(HERO6, [0, 0.8 + 2.6, 0]), 'rollTop': [0, 1.75, -1.15], 'rollEnd': [1.45, 0.85, -1.15], 'rollFoot': [0, 0.05, -0.3], 'box': BOX6, 'smokeTop': add(BOX6, [0, 1.6, 0])})
PEEK = {'lid': 0.0, 'pop': 0.4, 'mouth': 'flat', 'brow': 0.75}
STARE6 = {'lid': 0.35, 'mouth': 'line', 'brow': -0.1}
HANDS6 = {'R': R5([-0.25, 1.77, -1.75]), 'L': R5([0.4, 1.77, -1.75])}
st.shot('S06', SET, setOpts=SETO, lighting='day', look=SUN, actors=[
        act('mec', HERO6, 15, 'stand', 'neutral', keys=[k(0.0, look=add(BOX6, [0, 0.3, 0])),
            TK(0.0, {'R': R5([-0.25, 1.55, -1.8]), 'L': R5([0.4, 1.55, -1.8])}, {'R': 'grip', 'L': 'grip'}, {'lid': 0.3, 'mouth': 'line', 'autoSq': 0}, d=0.0),
            k(0.0, toon={'autoSq': 0}, keepPose=True),
            # (review 2) a slow rise, eyes first over the top; a pop up into a stretch held 7 frames; then he settles into the stare
            k(0.12, to=add(HERO6, [0, 0.55, 0]), dur=0.6, ease='inOut', glide=True, face='keep'), k(0.25, look=add(BOX6, [0.0, 0.8, 0.5]), lookDur=0.3),
            TK(0.6, HANDS6, {'R': 'grip', 'L': 'grip'}, {'lid': 0.1, 'pop': 0.15, 'mouth': 'line', 'brow': 0.5}, d=0.2),
            k(UP6, to=add(HERO6, [0, 0.98, 0]), dur=0.26, ease='inOut', glide=True, face='keep'),   # (review 3) eased over 8 frames
            TK(UP6, HANDS6, {'R': 'grip', 'L': 'grip'}, PEEK, (0.86, 1.2, 0.86), d=0.26, e='inOut'),
            TK(HOLD6, HANDS6, {'R': 'grip', 'L': 'grip'}, PEEK, (0.87, 1.19, 0.87), d=0.24, e='linear'),
            k(HOLD6, to=add(HERO6, [0, 0.94, 0]), dur=0.25, ease='inOut', glide=True, face='keep'),   # (review 3) he stays up: the face clear to the end
            TK(r(HOLD6 + 0.25), HANDS6, {'R': 'grip', 'L': 'grip'}, STARE6, (1, 1, 1), d=0.25),
            k(r(UP6 + 0.1), look='camera', lookDur=0.12), *blink(1.62, STARE6)])],
        props=[TOWN('S06', **DONE, roll=True, rollAt=[0.0, -1.15]),
               P('boite6', 'pizzaBox', pos=BOX6, ry=-35, rot=[0.3, math.radians(-35), 0], opts={'s': 1.25, 'pizza': False, 'scorch': True, 'open': 0.0, 'smoke': True, 'fire': True, 'fireK': [[0, 1.0], [0.18, 1.0], [0.42, 0.0]]})],   # (review 1) the fire dies over 7 frames into smoke   # (review 2) bigger, tilted to the lens, lid ajar: it reads as a box
        cams=[C6])
st.cue('sfx:scratch', 'S06', 0.15, 0.2); st.cue('sfx:boing', 'S06', UP6, 0.2)

# 7: this man found it overcooked. Close: standing behind the roll he holds up a charred black slice beside his face; on « cuite » it crumbles to dust
#    in his fingers (a black puff, crumbs raining); the open charred pizza in its box on the roll in front of him, the dial reading red; a blink
D7 = st.dur('S07'); CR7 = 1.1   # (review 3) the crumble at 13.20 s, after a lift-and-sniff
HERO7 = [-0.2, 0.05, -2.5]
BOX7 = [-0.5, 1.73, -1.3]   # (review 3) the dial further left and lower: a gap to his face
SLICE7 = off(HERO7, 0, 0.5, -0.34, 1.92)   # (review 2) in his left hand at shoulder height, against the pale hall wall
C7 = cam(0.0, [-0.12, 2.05, 0.85], [-0.14, 2.05, 0.6], [-0.22, 1.98, -2.15], [-0.22, 1.98, -2.15], lens=40)
chk('S07', C7, {'face': add(HERO7, [0, 2.05, 0]), 'hairTop': add(HERO7, [0, 2.4, 0]), 'slice': SLICE7, 'sliceTip': add(SLICE7, [0, 0.33, 0]), 'box': BOX7, 'dial': add(BOX7, [0.02, 0.42, 0.1])})
SNIFF = {'lid': 0.35, 'mouth': 'flat', 'brow': 0.1}
st.shot('S07', SET, setOpts=SETO, lighting='day', look=SUN, actors=[
        act('mec', HERO7, 0, 'stand', 'neutral', keys=[k(0.0, look=add(SLICE7, [0, 0.15, 0])),
            TK(0.0, {'L': R5(add(SLICE7, [0, -0.02, 0])), 'R': R5([-0.55, 1.8, -1.9])}, {'L': 'pinch', 'R': 'rest'}, SNIFF, d=0.0),
            TK(0.72, {'L': R5(add(SLICE7, [-0.04, 0.12, 0.02]), 1, 0.06)}, {'L': 'pinch'}, {'lid': 0.5, 'mouth': 'pout', 'brow': 0.3}, (0.98, 1.03, 0.98), {'neck': SP(0.18)}, d=0.2),   # (review 3) lift and sniff
            TK(0.92, {'L': R5(add(SLICE7, [-0.04, 0.14, 0.02]), 1, 0.06)}, {'L': 'pinch'}, {'lid': 0.6, 'mouth': 'pout', 'brow': 0.4}, (0.99, 1.02, 0.99), {'neck': SP(0.22)}, d=0.15),
            TK(r(CR7 - 0.02), {'L': R5(add(SLICE7, [0, 0.06, 0]), 1, 0.06)}, {'L': 'pinch'}, {'lid': 0.3, 'mouth': 'flat', 'brow': 0.3}, (1, 1, 1), {'neck': SP(0.0)}, d=0.12),
            TK(r(CR7 + 0.06), {'L': R5(add(SLICE7, [0, -0.06, 0]))}, {'L': 'open'}, {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.6}, (1.06, 0.93, 1.06), d=0.05, e='out'),
            TK(r(CR7 + 0.25), {'L': R5(add(SLICE7, [0, -0.08, 0]))}, {'L': 'open'}, {'lid': 0.05, 'pop': 0.2, 'mouth': 'O', 'brow': 0.5}, (1, 1, 1), d=0.12),
            *blink(0.3, SNIFF),
            k(0.45, look='camera', lookDur=0.15)])],
        props=[TOWN('S07', **DONE, roll=True, rollAt=[0.0, -1.15]),
               P('part7', 'pizzaSlice', pos=SLICE7, rot=[PI / 2, 0, -0.2], opts={'charred': True, 'crumbleAt': CR7, 'fall': 1.9, 'r': 0.46}, keys=[k(0.72, to=add(SLICE7, [-0.04, 0.12, 0.02]), dur=0.2), k(0.92, to=add(SLICE7, [-0.04, 0.14, 0.02]), dur=0.15), k(r(CR7 - 0.02), to=add(SLICE7, [0, 0.06, 0]), dur=0.12)]),   # the slice rides with the hand
               P('boite7', 'pizzaBox', pos=BOX7, ry=-8, rot=[0.25, math.radians(-8), 0], opts={'side': 1, 'open': 1.9, 'charred': True, 'missing': True, 'charredBox': True, 'smoke': True, 'thermo': 1.0, 'tR': 0.14, 'tLen': 0.06, 'tTilt': -0.25, 'tRoll': 0.3, 'tAt': [-0.05, 0.1]})],
        cams=[C7])
st.cue('sfx:crunch', 'S07', CR7, 0.4); st.cue('sfx:poof', 'S07', r(CR7 + 0.05), 0.2)

# 8: the general staff concluded: cool it on the way. The war room from high in front of the map table: a drawn elevation chart (houses at the
#    bottom, a band of clouds, space and a big snowflake at the far end) with a chalk arrow looping from his house up to the snowflake and back down;
#    the general at the near left lays his hand on the little pizza-box token and his arm stretches like rubber as he pushes it all the way up the
#    arrow to the snowflake; across the table two generals nod twice in sync
D8 = st.dur('S08'); P0, P1 = 1.3, 2.1
TAB = [0.0, 0, -1.25]
OFFICE = {'door': False, 'printer': False, 'picture': False, 'carpet': False, 'wall': '#4A5866', 'band': '#2E3A46', 'trim': '#1E262E'}
MAPP = [[[-0.05, 0.5], [-1.05, 0.35], [-0.95, -0.62], [-0.08, -0.56]]]
def bez(p, u): a = 1 - u; return [a ** 3 * p[0][i] + 3 * a * a * u * p[1][i] + 3 * a * u * u * p[2][i] + u ** 3 * p[3][i] for i in range(2)]
def TOKW(u): q = bez(MAPP[0], u); return [r(TAB[0] + q[0]), r(0.92 + 0.07), r(TAB[2] + q[1])]
GEN1 = [-1.3, 0, -1.2]; RYG1 = 75   # (review 1) at the left end of the table, three-quarter to us, his arm along the arrow
GEN2 = [-0.6, 0, -2.35]; GEN3 = [0.45, 0, -2.35]
C8 = cam(0.0, [0.0, 4.0, 1.9], [-0.03, 3.95, 1.75], [-0.355, -2.73, -5.488], [-0.355, -2.72, -5.488], lens=67)   # (review 2) high over the table, tilted down: the chart reads
chk('S08', C8, {'gen1Face': add(GEN1, [0, 2.05, 0]), 'gen2Face': add(GEN2, [0, 2.05, 0]), 'gen3Face': add(GEN3, [0, 2.05, 0]), 'tok0': TOKW(0), 'tok1': TOKW(1), 'snow': [0, 0.92, -1.25 - 0.62], 'mapNear': [0, 0.92, -0.4]})
GK = {'lid': 0.3, 'mouth': 'line', 'brow': -0.5}
NOD = lambda t: [TK(t, face={'lid': 0.4, 'mouth': 'smile', 'brow': 0.2}, bend={'neck': SP(0.6), 'spine': SP(0.12)}, sq=(1.04, 0.95, 1.04), d=0.09, keep=True), TK(r(t + 0.15), face={'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}, bend={'neck': SP(-0.1), 'spine': SP(0.0)}, sq=(1, 1, 1), d=0.11, keep=True)]   # (review 1) a deeper nod
def smooth_(u): return u * u * (3 - 2 * u)
# (review 2) the arm starts at his side, reaches the token (it starts to stretch), then grows all the way to the snowflake with a slow-in (the token's own easing)
reach8 = [TK(0.0, {'L': R5(off(GEN1, RYG1, 0.25, -0.3, 1.0), 0), 'R': R5(off(GEN1, RYG1, 0.3, 0.3, 1.0))}, {'L': 'rest', 'R': 'rest'}, GK, d=0.0),
          TK(0.55, {'L': R5(add(TOKW(0), [0, 0.06, 0]), 1, 0.02)}, {'L': 'open'}, GK, (0.97, 1.03, 0.97), d=0.55, e='inOut')]
for i in range(9):
    u = smooth_(i / 8); t = r(P0 + (P1 - P0) * i / 8)
    reach8.append(TK(t, {'L': R5(add(TOKW(u), [0, 0.02, 0]), 1, 0.02)}, {'L': 'open'}, {'lid': 0.15, 'mouth': 'clench', 'brow': -0.7} if i else GK, (1, 1, 1), {'spine': SP(0.08)}, d=r((P1 - P0) / 8), e='linear'))
st.shot('S08', 'office', setOpts=OFFICE, actors=[
        act('general1', GEN1, RYG1, 'stand', 'determined', keys=[k(0.0, look=add(TOKW(0), [0, 0.6, 0.6])), *reach8, k(r(P1 - 0.1), look='camera', lookDur=0.15),
            TK(r(P1 + 0.15), {'L': R5(add(TOKW(1), [0, 0.12, 0.1]))}, {'L': 'point'}, {'lid': 0.2, 'mouth': 'smile', 'brow': 0.3}, (1.05, 0.95, 1.05), d=0.12)]),
        act('general2', GEN2, 0, 'stand', 'neutral', keys=[k(0.0, look=TOKW(0)), k(P0, look=TOKW(0.5), lookDur=0.4), k(r(P1 - 0.1), look='camera', lookDur=0.15), TK(0.0, face=GK, d=0.0), *NOD(r(P1 + 0.05)), *NOD(r(P1 + 0.3))]),
        act('general3', GEN3, 0, 'stand', 'neutral', keys=[k(0.0, look=TOKW(0)), k(P0, look=TOKW(0.5), lookDur=0.4), k(r(P1 - 0.1), look='camera', lookDur=0.15), TK(0.0, face=GK, d=0.0), *NOD(r(P1 + 0.05)), *NOD(r(P1 + 0.3))])],
        props=[P('carte8', 'pizzaWarMap', pos=TAB, opts={'token': [[0, 0.0], [P0, 0.0], [P1, 1.0]], 'tokS': 0.75, 'tokGlow': 0.9}),
               *[P(f'kepi8{j}', 'kepi', on={'actor': f'general{j}', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#4E5730', 'band': '#2E3320'}) for j in (1, 2, 3)],
               *[P(f'epaul8{j}', 'epaulettes', on={'actor': f'general{j}', 'joint': 'torso', 'offset': [0.0, 0.42, 0.0]}, opts={'w': 0.52}) for j in (1, 2, 3)]],
        cams=[C8])
st.cue('sfx:scratch', 'S08', P0, 0.3); st.cue('sfx:stretch', 'S08', P0, 0.3); st.cue('sfx:ding', 'S08', P1, 0.25)

# 9: a missile took it up to space. A slow orbit round the climbing missile, the Earth curving below and the stars beyond: the box strapped on its
#    nose frosts over as it climbs, icicles shoot out (an icy « crack » at the peak); a satellite it passes turns its dish to follow it, a double take
D9 = st.dur('S09'); ICE9 = 1.25
M0, M1 = [0.0, -5.0, 0.0], [0.0, 9.0, 0.0]
SAT9 = [-3.6, 6.0, -2.4]
C9 = cam(0.0, [9.0, 5.0, 9.5], [-4.0, 13.0, 12.0], [0.0, 0.5, 0.0], [0.0, 11.0, 0.0], lens=42)
chk('S09', C9, {'missileStart': M0, 'boxStart': add(M0, [0, 3.5, 0]), 'boxEnd': add(M1, [0, 3.5, 0]), 'sat': SAT9, 'earthTop': [0, -22, -40]})
st.shot('S09', 'spaceDark', setOpts={'stars': 900}, look={'sunDir': [0.8, 0.5, 0.6], 'exposure': 1.15}, actors=[],
        props=[P('terre9', 'planetEarth', pos=[-20.0, -105.0, -85.0], opts={'r': 70, 'seed': 11}),   # (review 1) a planet with a curved horizon, blue oceans and white clouds
               P('missile9', 'pizzaMissile', pos=M0, opts={'frost': [[0, 0.0], [0.5, 0.35], [ICE9, 1.0]], 'trail': 22, 'boxS': 2.0}, keys=[k(0.0, to=M1, dur=D9, ease='linear'), k(ICE9, squash=[1.08, 0.95, 1.08], dur=0.3)]),
               P('glace9', 'twinkle', pos=add(M0, [0.0, 3.5 + (M1[1] - M0[1]) * ICE9 / D9, 0.8]), opts={'at': ICE9, 's': 0.9, 'dur': 0.4}),
               P('sat9', 'satellite', pos=SAT9, ry=200, scale=0.8, keys=[k(0.55, rotTo=[0.3, math.radians(120), 0.0], dur=0.25, ease='out'), k(0.95, rotTo=[0.0, math.radians(200), 0.0], dur=0.12), k(1.2, rotTo=[-0.5, math.radians(110), 0.2], dur=0.15, ease='out')])],
        cams=[C9])
st.cue('engine', 'S09', 0.0, 0.3, 2.0); st.cue('sfx:glass', 'S09', ICE9, 0.4); st.cue('sfx:boing', 'S09', 0.95, 0.15)

# 10: it made a crater in his garden. Low on the road in front of his house: he stands in his doorway; behind the roof a white flash and a towering
#     dust cloud from the back garden, the camera shakes hard, roof dust falls; he does not move at all (one late blink)
D10 = st.dur('S10'); BOOM10 = 0.42
HERO10 = list(HERO_DOOR)
C10 = cam(0.0, [1.7, 0.6, 3.2], [1.65, 0.62, 3.0], [0.0, 3.9, -6.0], [0.0, 4.0, -6.0], lens=52)
chk('S10', C10, {'face': add(HERO10, [0, 2.05, 0]), 'feet': HERO10, 'roof': [0, 5.0, -6.7], 'cloudTop': [0, 12.0, -14.8], 'burst': [0, 3.0, -14.8]})
st.shot('S10', SET, setOpts=SETO, lighting='day', look=SUN, actors=[
        act('mec', HERO10, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, {'R': R5(off(HERO10, 0, 0.1, 0.32, 1.05)), 'L': R5(off(HERO10, 0, 0.1, -0.32, 1.05))}, {'R': 'rest', 'L': 'rest'}, DEAD, d=0.0),
            *blink(1.12, DEAD), *BREATHE(0.0, D10, 0.6, 0.01)])],   # (review 1) breathing and one timed blink, nothing else moves
        props=[TOWN('S10', **DONE),
               P('flash10', 'timedBurst', pos=[0.0, 4.0, -14.8], opts={'at': BOOM10, 'size': 6.5, 'life': 0.3}),
               P('poussiere10', 'dustCloud', pos=[0.0, 0.0, -14.8], opts={'at': r(BOOM10 + 0.05), 'r': 9.0, 'h': 13.0, 'n': 30, 'opacity': 0.85, 'color': '#E8DCC4'}),
               P('toit10', 'softDust', pos=[0.0, 5.0, -4.5], opts={'at': r(BOOM10 + 0.08), 'n': 10, 'size': 0.6, 'rise': -1.2, 'spread': 3.0, 'life': 1.1, 'color': '#C9B79A', 'opacity': 0.7})],
        fx=[{'type': 'flash', 'at': BOOM10, 'dur': 0.12}, {'type': 'shake', 'at': BOOM10, 'dur': 0.7, 'amount': 0.05}],   # the one intended flash (a white frame, not a dark one)
        cams=[C10])
st.cue('thunder', 'S10', BOOM10, 0.8); st.cue('thud', 'S10', r(BOOM10 + 0.05), 0.7); st.cue('engine', 'S10', r(BOOM10 + 0.1), 0.25, 1.2)

# 11: his front door is what is left. High and wide as the dust clears: a deep, clean round crater where the house and the garden were, the street
#     intact in front, his door frame alone on the rim with him standing in it; the door creaks open on its own and bangs (a wobble); nobody else
D11 = st.dur('S11')
HERO11 = list(HERO_DOOR)
C11 = cam(0.0, [0.0, 36.0, 12.0], [0.0, 33.0, 10.5], [0.0, -6.0, -12.5], [0.0, -6.0, -12.2], lens=50)   # (review 1) higher and wider, the door frame centred on the near rim
chk('S11', C11, {'hero': add(HERO11, [0, 2.0, 0]), 'heroFeet': HERO11, 'craterFar': [0, 0, -26.4], 'craterL': [-11.6, 0, -14.8], 'craterR': [11.6, 0, -14.8], 'floor': [0, -14, -14.8], 'road': [0, 0, 6.0]})
st.shot('S11', SET, setOpts=SETO, lighting='day', look=SUN, actors=[
        act('mec', HERO11, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, face=DEAD, d=0.0), *blink(1.1, DEAD)])],
        props=[TOWN('S11', **DONE, crater=CRATER, frameDoor=[[0, -0.1], [0.45, -1.9]]),
               P('poussiere11', 'dustCloud', pos=[0.0, -4.0, -14.8], opts={'at': -1.0, 'r': 10.0, 'h': 14.0, 'n': 26, 'opacity': 0.7, 'clear': [0.0, 1.1], 'color': '#E8DCC4'})],
        cams=[C11])
st.cue('sfx:wind', 'S11', 0.0, 0.2, 1.5); st.cue('sfx:squeak', 'S11', 0.35, 0.3); st.cue('clack', 'S11', 0.68, 0.3)

# 12: at the bottom of the crater: sixty degrees. Close and low on the crater floor, the striped walls rising behind: the intact open box, its dial
#     swinging down from the red and settling EXACTLY on green (a sparkle, a curl of steam); behind it a kneeling soldier gives a big thumbs up
#     and grins (LIVRÉE once it has settled)
D12 = st.dur('S12'); GREEN12 = 1.22
ROCK12 = [0.55, -CD, -11.4]; BOX12 = [0.55, r(-CD + 0.37), -11.4]   # (review 3) on a lump of rubble: the pizza above the caption band
SOLD12 = [1.35, r(-CD - 0.62), -12.55]   # (review 1) kneeling for real: the root lowered by hand, the legs bent
KNEEL = {'legL': SP(-1.5), 'shinL': SP(1.5), 'legR': SP(0.05), 'shinR': SP(1.55)}
C12 = cam(0.0, [-0.3, -12.85, -7.9], [-0.25, -12.9, -8.1], [0.7, -13.12, -11.9], [0.7, -13.12, -11.9], lens=48)
chk('S12', C12, {'box': BOX12, 'dial': add(BOX12, [0.1, 0.62, 0.05]), 'soldFace': add(SOLD12, [0, 2.05, 0]), 'thumb': off(SOLD12, -25, 0.5, -0.28, 1.75), 'wallTop': [0.5, 0, -26.0]})
st.shot('S12', SET, setOpts=SETO, lighting='day', look={'sunDir': [0.3, 0.9, 0.5], 'fill': 1.3}, actors=[
        act('soldat3', SOLD12, -25, 'stand', 'neutral', keys=[k(0.0, look=add(BOX12, [0, 0.5, 0])), TK(0.0, {'L': R5(off(SOLD12, -25, 0.35, -0.3, 1.2)), 'R': R5(off(SOLD12, -25, 0.35, 0.3, 1.15))}, {'L': 'rest', 'R': 'rest'}, {'lid': 0.3, 'mouth': 'line', 'brow': 0.4}, bend=KNEEL, d=0.0),
            k(r(GREEN12 + 0.05), look='camera', lookDur=0.12),
            TK(r(GREEN12 + 0.12), {'L': R5(off(SOLD12, -25, 0.55, -0.34, 2.15))}, {'L': 'thumbUp'}, {'lid': 0.1, 'mouth': 'bigsmile', 'brow': 0.7}, (0.92, 1.1, 0.92), KNEEL, d=0.07, e='out'),
            TK(r(GREEN12 + 0.35), {'L': R5(off(SOLD12, -25, 0.55, -0.34, 2.08))}, {'L': 'thumbUp'}, {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.6}, (1, 1, 1), KNEEL, d=0.15),
            *blink(r(GREEN12 + 0.75), {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.6})]),
        ],
        props=[TOWN('S12', **DONE, crater=CRATER, ladder=True),
               P('boite12', 'pizzaBox', pos=BOX12, ry=12, rot=[0.18, math.radians(12), 0], opts={'open': 1.85, 'thermo': [[0, 1.0], [0.45, 0.7], [0.85, -0.25], [GREEN12, 0.0]], 'wobA': 0.12, 'tR': 0.17, 'tLen': 0.36, 'tTilt': -0.18, 'tAt': [0.1, 0.07], 'seed': 12}),
               P('vapeur12', 'softWisp', pos=add(BOX12, [-0.1, 0.12, 0.0]), opts={'n': 10, 'rise': 0.9, 'life': 1.4, 's0': 0.06, 's1': 0.25, 'color': '#FFFFFF', 'opacity': 0.55}),
               P('ding12', 'twinkle', pos=add(BOX12, [0.12, 0.78, 0.25]), opts={'at': GREEN12, 's': 0.25, 'dur': 0.45}),
               P('rocher12', 'rubbleRock', pos=ROCK12, ry=10, opts={'h': 0.35, 'w': 1.0}), P('epaul12', 'epaulettes', on={'actor': 'soldat3', 'joint': 'torso', 'offset': [0.0, 0.42, 0.0]}, opts={'w': 0.52}),
               P('casque12', 'armyHelmet', on={'actor': 'soldat3', 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95})],
        cams=[C12])
st.card('S12', 'LIVRÉE', at=1.5)
st.cue('sfx:tick', 'S12', 0.45, 0.15); st.cue('sfx:tick', 'S12', 0.85, 0.15); st.cue('sfx:ding', 'S12', GREEN12, 0.4)

# 13: the president opened the crater. On the rim, from the road: the president in his sash behind a red ribbon at the left snips it with giant
#     scissors (the halves drop, a burst of confetti) and flings both arms up, beaming; at the right the band blows and drums; between them, behind,
#     he stands in his lone door frame on the rim, the crater's far wall behind them
D13 = st.dur('S13'); SNIP13 = 0.9
PRES13 = [-1.05, 0, -2.75]; RIB13 = [-1.05, 0, -2.05]
MUS1 = [1.1, 0, -2.2]; MUS2 = [1.7, 0, -3.1]
HERO13 = list(HERO_DOOR)
C13 = cam(0.0, [0.25, 4.6, 7.0], [0.22, 4.5, 6.6], [0.1, 0.9, -4.5], [0.1, 0.9, -4.5], lens=46)   # (review 2) raised: the crater bowl opens behind the door frame
chk('S13', C13, {'presFace': add(PRES13, [0, 2.05, 0]), 'armsUp': add(PRES13, [0, 2.9, 0]), 'heroFace': add(HERO13, [0, 2.05, 0]), 'mus1': add(MUS1, [0, 2.05, 0]), 'mus2': add(MUS2, [0, 2.05, 0]), 'ribbon': add(RIB13, [0, 0.95, 0]), 'farRim': [0, 0, -26.4]})
BEAM = {'lid': 0.15, 'mouth': 'grin', 'brow': 0.6}
BEATS13 = [0.2, 0.55, 0.9, 1.25, 1.6, 1.95]
st.shot('S13', SET, setOpts=SETO, lighting='day', look=SUN, actors=[
        act('president', PRES13, 12, 'stand', 'happy', keys=[k(0.0, look=add(RIB13, [0, 0.95, 0])),
            TK(0.0, {'R': R5(add(RIB13, [0.0, 1.05, -0.12])), 'L': R5(off(PRES13, 0, 0.3, -0.3, 1.1))}, {'R': 'grip', 'L': 'rest'}, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}, d=0.0),
            TK(r(SNIP13 - 0.05), {'R': R5(add(RIB13, [0.0, 0.98, -0.1]))}, {'R': 'grip'}, {'lid': 0.2, 'mouth': 'O', 'brow': 0.4}, (1.04, 0.96, 1.04), d=0.1),
            TK(r(SNIP13 + 0.15), {'R': R5(off(PRES13, 12, 0.15, 0.45, 2.85)), 'L': R5(off(PRES13, 12, 0.15, -0.45, 2.85))}, {'R': 'grip', 'L': 'spread'}, BEAM, (0.88, 1.16, 0.88), d=0.08, e='out'),
            TK(r(SNIP13 + 0.45), {'R': R5(off(PRES13, 12, 0.15, 0.45, 2.7)), 'L': R5(off(PRES13, 12, 0.15, -0.45, 2.7))}, {'R': 'grip', 'L': 'spread'}, BEAM, (1, 1, 1), d=0.15),
            *[TK(r(SNIP13 + 0.6 + 0.16 * j), {'R': R5(off(PRES13, 12, 0.15, 0.45, 2.7 + (0.08 if j % 2 == 0 else -0.02))), 'L': R5(off(PRES13, 12, 0.15, -0.45, 2.7 + (0.08 if j % 2 == 0 else -0.02)))}, {'R': 'grip', 'L': 'spread'}, BEAM, (0.96, 1.05, 0.96) if j % 2 == 0 else (1.03, 0.97, 1.03), d=0.14) for j in range(4)],   # (review 2) a bounce on the arms-up hold
            k(r(SNIP13 + 0.04), look='camera', lookDur=0.08), *blink(1.7, BEAM)]),   # (review 1) his face to us as he beams
        act('mec', HERO13, 0, 'stand', 'neutral', keys=[k(0.0, look=add(PRES13, [0, 1.8, 0])), TK(0.0, face=DEAD, d=0.0), k(1.3, look='camera', lookDur=0.2), *blink(1.75, DEAD)]),
        act('musi1', MUS1, -20, 'stand', 'happy', keys=[k(0.0, look='camera'), *[TK(t, face={'lid': 0.2, 'mouth': 'O', 'brow': 0.5}, sq=(1.04, 0.96, 1.04) if i % 2 else (0.98, 1.03, 0.98), d=0.15, keep=True) for i, t in enumerate(BEATS13)]]),
        act('musi2', MUS2, -25, 'stand', 'happy', keys=[k(0.0, look='camera'), *[TK(t, face={'lid': 0.3, 'mouth': 'smile', 'brow': 0.4}, sq=(1.03, 0.97, 1.03) if i % 2 else (0.98, 1.02, 0.98), d=0.15, keep=True) for i, t in enumerate(BEATS13)]])],
        props=[TOWN('S13', **DONE, crater=CRATER, ladder=True, frameDoor=-1.7),
               P('ruban13', 'ribbonCut', pos=RIB13, opts={'w': 1.5, 'h': 0.95, 'cutAt': SNIP13}),
               P('ciseaux13', 'bigScissors', on={'actor': 'president', 'hand': 'R', 'offset': [0, 0, 0.04]}, scale=2.0, rot=[0, 0, 0], opts={'handle': '#E2B53C', 'open': 0.5, 'snip': [[0.0, 1.0], [r(SNIP13 - 0.04), 1.0], [SNIP13, 0.0], [r(SNIP13 + 0.25), 0.0]]}),
               P('confetti13', 'confettiPuff', pos=add(RIB13, [0, 1.1, 0.15]), opts={'at': SNIP13, 'n': 60, 'r': 1.3, 'bit': 0.13}),   # (review 2) bigger, brighter
               P('trompette13', 'bandInstr', on={'actor': 'musi1', 'joint': 'head', 'offset': [0.0, 0.13, 0.11], 'rot': [-0.3, -0.85, 0.0]}, opts={'kind': 'trumpet', 'beat': BEATS13, 's': 1.15}),
               P('tambour13', 'bandInstr', on={'actor': 'musi2', 'joint': 'torso', 'offset': [0.0, 0.12, 0.3]}, opts={'kind': 'drum', 'beat': BEATS13}),
               *[P(f'kepi13{j}', 'kepi', on={'actor': f'musi{j}', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#4E5730', 'band': '#2E3320'}) for j in (1, 2)]],
        cams=[C13])
st.cue('sfx:fanfare', 'S13', 0.1, 0.3); st.cue('sfx:clink', 'S13', SNIP13, 0.4); st.cue('pop', 'S13', r(SNIP13 + 0.03), 0.3)

# 14: the other countries order their pizzas cold. Down a street of foreign front doors, each under its own invented flag, one pair per doorstep with
#     space between them, both in profile: the official in his sash on his step holds a frosted box (dial blue, turned to us) and scribbles on the
#     clipboard the courier holds out; then the three officials nod twice in sync, pleased (review 1: the pairs no longer overlap)
D14 = st.dur('S14')
FX14 = -1.7; ZS14 = [0.8, -4.4, -9.6]   # (review 1) a high camera down the street: the pairs stack up the frame instead of overlapping
ROW14 = [[FX14, 0, z] for z in ZS14]
def offi(i): return [r(FX14 + 0.75), 0, ZS14[i]]
def cour(i): return [r(FX14 + 1.95), 0, ZS14[i]]
RYO, RYC = 90, -90
PTS14 = {**{f'o{i}': add(offi(i), [0, 2.4, 0]) for i in range(3)}, **{f'of{i}': offi(i) for i in range(3)}, **{f'c{i}': add(cour(i), [0, 2.4, 0]) for i in range(3)}, **{f'fl{i}': [FX14 + 1.1, 4.4, ZS14[i] + 1.2] for i in range(3)}}
FR14 = [1.5, 8.0, 8.0]
L14, LENS14, _ = fit(FR14, {**PTS14, **{f'cf{i}': cour(i) for i in range(3)}}, top=0.08, bottom=0.74)
C14 = cam(0.0, FR14, add(FR14, [-0.05, -0.1, -0.2]), [r(v) for v in L14], [r(v) for v in L14], lens=LENS14)
chk('S14', C14, {**PTS14, **{f'box{i}': add(offi(i), [0.42, 1.55, 0.2]) for i in range(3)}})
NODB = lambda t: [TK(t, face={'lid': 0.5, 'mouth': 'bigsmile', 'brow': 0.4}, bend={'neck': SP(1.2), 'spine': SP(0.28)}, sq=(1.14, 0.82, 1.14), d=0.09, keep=True), TK(r(t + 0.15), face={'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.5}, bend={'neck': SP(-0.15), 'spine': SP(0.0)}, sq=(0.96, 1.05, 0.96), d=0.1, keep=True)]   # (review 2) big nods with a squash, they read from up there
acts14, props14 = [], []
for i in range(3):
    O, Cq = offi(i), cour(i)
    BOXo = add(O, [0.42, 1.0, 0.18])
    CLIP = add(Cq, [-0.45, 1.3, -0.05])
    sc = [TK(r(0.35 + 0.12 * j), {'R': R5(add(CLIP, [0.03 * (-1) ** j, 0.05 + 0.04 * (j % 2), 0.06 * (-1) ** j]), 1, 0.02)}, {'R': 'pinch'}, d=0.1, keep=True) for j in range(6)]
    acts14.append(act(f'officiel{i + 1}', O, RYO, 'stand', 'happy', keys=[k(0.0, look=add(CLIP, [0, 0.05, 0])),
        TK(0.0, {'L': R5(add(BOXo, [-0.05, 0.05, 0.3])), 'R': R5(add(CLIP, [0, 0.05, -0.05]))}, {'L': 'grip', 'R': 'pinch'}, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, d=0.0), *sc,
        k(1.1, look=add(Cq, [0, 2.0, 0]), lookDur=0.15), *NODB(1.3), *NODB(1.62), k(1.95, look='camera', lookDur=0.15)]))
    acts14.append(act(f'courrier{i + 1}', Cq, RYC, 'stand', 'neutral', keys=[k(0.0, look=add(CLIP, [0, 0.1, 0])), TK(0.0, {'R': R5(add(CLIP, [0.08, -0.05, 0.12])), 'L': R5(add(CLIP, [0.08, -0.05, -0.15]))}, {'R': 'grip', 'L': 'grip'}, DEAD, d=0.0),
        k(1.1, look=add(O, [0, 2.0, 0]), lookDur=0.15), *blink(r(0.9 + 0.2 * i), DEAD), *BREATHE(0.0, D14, 0.6, 0.01)]))
    props14 += [P(f'porte14{i}', 'embassyDoor', pos=ROW14[i], ry=90, opts={'w': 3.2, 'colors': FLAGS[i], 'vertical': i != 1, 'open': -1.45, 'wall': ['#E8E0D0', '#F0D8C8', '#D8E4E8'][i], 'door': ['#6A2E3A', '#2E4A6A', '#3E5A2E'][i], 'seed': i}),
                P(f'boite14{i}', 'pizzaBox', pos=BOXo, rot=[0.45, 0, 0], opts={'side': 1, 'pizza': True, 'open': 1.8, 'frost': 1.0, 'thermo': -1.0, 'tR': 0.17, 'tTilt': -0.45, 'tAt': [0.08, 0.06], 'seed': 40 + i}),
                P(f'planchette14{i}', 'clipBoard', pos=CLIP, ry=90, rot=[0, math.radians(90), -0.6]),
                P(f'casque14{i}', 'armyHelmet', on={'actor': f'courrier{i + 1}', 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95})]
st.shot('S14', 'grassland', setOpts={'clouds': 30}, look=SUN, actors=acts14,
        props=[P('parvis14', 'roadStrip', pos=[1.6, 0, -6.0], opts={'len': 60, 'w': 6})] + props14,
        cams=[C14])
st.cue('sfx:scratch', 'S14', 0.35, 0.3); st.cue('sfx:pop', 'S14', 1.3, 0.15)

# 15: it took this man three hours to climb down. Extreme wide from very high: the round crater and his lone door frame on the rim; he is a dot on the
#     rope ladder climbing down the wall while the sun races round the sky (two day-night cycles) and the shadows sweep round inside the crater
D15 = st.dur('S15'); PER15 = 0.9
# (review 1) from behind the crater, across it: the door-side wall faces us with the pale rope ladder down it, the sky above with the sun disc racing
C15 = cam(0.0, [3.5, 9.0, -36.0], [3.2, 8.7, -34.5], [0.0, -2.6, -4.5], [0.0, -2.9, -4.5], lens=52)
def LAD(u): return [r(LTOP[0] + (LBOT[0] - LTOP[0]) * u), r(LTOP[1] + (LBOT[1] - LTOP[1]) * u), r(LTOP[2] + (LBOT[2] - LTOP[2]) * u - 0.35 * math.sin(PI * u))]
def HLAD(u): return add(LAD(u), [0, -2.15, -0.3])
STEPS15 = 6; H15a = HLAD(0.04)
climb15 = []
for i in range(STEPS15):
    t0 = r(i * D15 / STEPS15); climb15.append(k(t0, to=HLAD(0.04 + 0.8 * (i + 1) / STEPS15), dur=r(D15 / STEPS15 * 0.55), ease='inOut', glide=True, face='keep'))   # (review 1) down in steps: a move, a hold
chk('S15', C15, {'heroStart': add(H15a, [0, 1.5, 0]), 'heroEnd': add(HLAD(0.84), [0, 1.5, 0]), 'door': [0, 2.8, FZ], 'ladderTop': LTOP, 'ladderBot': LBOT, 'floor': [0, -CD, CC[1]], 'rimNear': [0, 0, CC[1] - CR], 'sky': [0, 60, 300]})
st.shot('S15', SET, setOpts=SETO, lighting='day', look={'sunDir': [0.2, 0.3, 0.9], 'fill': 1.45}, daynight={'from': 0.1, 'period': PER15},
        actors=[act('mec', H15a, 0, 'climbDown', 'neutral', keys=climb15)],
        props=[TOWN('S15', **DONE, crater=CRATER, ladder=True, ladderThick=3.0, frameDoor=-1.7), P('halo15', 'haloGlow', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.2, 0]}, opts={'s': 2.2, 'opacity': 0.45}),
               P('soleil15', 'sunRacer', pos=[0, 0, 0], opts={'from': 0.1, 'period': PER15, 'az0': 1.5708, 'maxEl': 0.35, 'minEl': 0.1, 'disc': True, 'discEl': 0.1})],
        cams=[C15])
st.cue('sfx:tick', 'S15', 0.1, 0.12); st.cue('sfx:tick', 'S15', 0.55, 0.12); st.cue('sfx:tick', 'S15', 1.0, 0.12); st.cue('sfx:tick', 'S15', 1.45, 0.12); st.cue('sfx:tick', 'S15', 1.9, 0.12)

# 16: one star; it was cold. The crater floor in the low gold light of evening. (a) Close on his phone: five grey stars; he taps the first one
#     with the stiff frozen slice (a clack), it pops yellow. (b) Close on him: deadpan stare at us, the frosted slice drooping stiffly in his hand,
#     his breath steaming, the open box at his feet with its dial blue again; one slow blink, held
D16 = st.dur('S16'); TAP16 = 0.3; CUT16 = 1.0
HERO16 = [0.35, -CD, -7.3]; RY16 = 180
PH16 = off(HERO16, RY16, 0.42, -0.12, 1.55)                        # the phone in his left hand, screen to the lens
TAPPOS = add(PH16, [0.065, -0.03, -0.06])                          # just in front of the first star
SLR = 0.42                                                          # the slice's length
SLhit = add(TAPPOS, [SLR, 0.0, 0.0])                               # (review 2) the crust in his fingers so that the slice's TIP lands on the star
SLup = add(SLhit, [0.12, 0.1, -0.1]); SLrest = add(SLhit, [0.2, -0.25, 0.05])
SL16b = off(HERO16, RY16, 0.45, 0.18, 1.38)                          # (review 2) end hold: held by the crust at his right, drooping sideways
BOX16 = off(HERO16, RY16, 0.55, -0.55, 0.0); BOX16[1] = r(-CD + 0.02)   # (review 3) on the floor in front of his left shoe, clear of his legs, tilted to us
THERMO16 = add(BOX16, [-0.04, 0.06, -0.05])
HIP16 = off(HERO16, RY16, 0.22, -0.38, 0.95)
C16a = cam(0.0, add(PH16, [-0.12, 0.02, -0.82]), add(PH16, [-0.11, 0.0, -0.74]), add(PH16, [0.04, 0.09, 0.0]), add(PH16, [0.04, 0.1, 0.0]), lens=40)   # (control 4) the phone runs off the bottom edge: nothing of his body shows below it
C16b = cam(CUT16, add(HERO16, [0.0, 1.55, -4.4]), add(HERO16, [0.0, 1.56, -4.25]), add(HERO16, [0.0, 1.25, 0.0]), add(HERO16, [0.0, 1.26, 0.0]), lens=42)   # (review 3) a step back: the box on the floor below the captions   # (review 1) him centred for the end hold
chk('S16a', C16a, {'phone': PH16, 'star1': TAPPOS, 'crustHit': SLhit, 'crustUp': SLup, 'phoneTop': add(PH16, [0, 0.24, 0])})
chk('S16b', C16b, {'face': add(HERO16, [0, 2.05, 0]), 'hairTop': add(HERO16, [0, 2.4, 0]), 'sliceCrust': SL16b, 'sliceTip': add(SL16b, [r(SLR * 0.81), -0.15, r(-SLR * 0.58)]), 'box': BOX16, 'boxLid': add(BOX16, [0, 0.55, 0.3]), 'dial': add(THERMO16, [0, 0.95, 0])})
DUSKSET = {**SETO, 'sky': ['#E7906A', '#FFD3A0'], 'below': '#FFD3A0'}
DUSKLOOK = {'sunColor': '#FFA868', 'sunDir': [-0.4, 0.35, -0.85], 'elevation': 18, 'warm': 0.55, 'hazeColor': '#F2B892', 'exposure': 1.12, 'fill': 1.45}
st.shot('S16', SET, setOpts=DUSKSET, lighting='day', look=DUSKLOOK, actors=[
        act('mec', HERO16, RY16, 'stand', 'neutral', keys=[k(0.0, look=PH16),
            TK(0.0, {'L': R5(add(PH16, [-0.13, -0.12, 0.06])), 'R': R5(add(SLrest, [0.0, -0.02, 0.0]))}, {'L': 'grip', 'R': 'pinch'}, DEAD, d=0.0),   # (review 3) the left hand on the phone's edge, behind it (its fingers had poked through the screen)
            TK(r(TAP16 - 0.14), {'R': R5(add(SLup, [0.0, -0.02, 0.0]))}, {'R': 'pinch'}, DEAD, d=0.1),
            TK(r(TAP16 - 0.04), {'R': R5(add(SLhit, [0.0, -0.02, 0.0]))}, {'R': 'pinch'}, DEAD, d=0.05, e='out'),
            TK(r(TAP16 + 0.42), {'R': R5(add(SLup, [0.0, -0.02, 0.0]))}, {'R': 'pinch'}, DEAD, d=0.2),
            TK(CUT16, {'L': R5(HIP16), 'R': R5(add(SL16b, [0.0, 0.0, 0.0]), 1, 0.05)}, {'L': 'rest', 'R': 'pinch'}, DEAD, d=0.0),   # the fingertips on the crust
            k(CUT16, look='camera', lookDur=0.05), *BREATHE(r(CUT16 + 0.1), D16, 0.6, 0.01), *blink(1.6, DEAD), TK(2.3, face={'lid': 0.55, 'mouth': 'line', 'brow': -0.2}, d=0.3, keep=True), *blink(2.75, {'lid': 0.55, 'mouth': 'line', 'brow': -0.2})])],
        props=[TOWN('S16', **DONE, crater=CRATER, ladder=True, frameDoor=-1.7),
               P('tel16', 'ratingPhone', pos=PH16, ry=r(RY16 - 8), opts={'rateAt': r(TAP16 + 0.02), 'tapAt': TAP16}, keys=[k(CUT16, visible=False)]),
               STEAM('16', 'mec', [1.25, 1.95, 2.65], d=(-0.26, -0.14, -0.12)),
               # (review 2) the slice for the tap: stiff, its tip pointing at the star from his right, its cheese turned to the lens
               P('part16a', 'pizzaSlice', pos=SLrest, rot=[-0.45, PI / 2, 0], opts={'frost': 1, 'droop': 0.05, 'r': SLR},
                 keys=[k(r(TAP16 - 0.14), to=SLup, dur=0.1), k(r(TAP16 - 0.04), to=SLhit, dur=0.05, ease='out'), k(TAP16, squash=[0.94, 1.0, 1.06], dur=0.15), k(r(TAP16 + 0.42), to=SLup, dur=0.2), k(CUT16, visible=False)]),
               # (review 2) the end hold: held by the crust, drooping sideways, frosted blue-white, toppings on it
               P('part16b', 'pizzaSlice', pos=SL16b, rot=[-0.55, -0.95, 0], opts={'frost': 1, 'droop': 0.5, 'r': 0.42}, keys=[k(0.0, visible=False), k(CUT16, visible=True)]),
               P('boite16', 'pizzaBox', pos=BOX16, ry=r(RY16 + 20), rot=[-0.35, math.radians(RY16 + 20), 0], opts={'open': 1.65, 'missing': True, 'frost': 0.3, 'seed': 16}),   # (review 3) a kraft box tilted to us, lid up behind it (no pale frosted slab)
               P('thermo16', 'pizzaThermo', pos=THERMO16, ry=r(RY16 + 10), opts={'temp': -1.0, 'r': 0.17, 'len': 0.78})],   # standing on its own: the blue dial at about two thirds of the height, clear of his legs],
        cams=[C16a, C16b])
st.cue('clack', 'S16', TAP16, 0.35); st.cue('sfx:ding', 'S16', r(TAP16 + 0.03), 0.2); st.cue('sfx:wind', 'S16', 1.2, 0.15, 1.8)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'hair': 'bald',
        'gloves': '#2E3320', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 2.2, 'shift': 2.0, 'breathe': 2.0}}
PRES = {'preset': 'politique', 'seed': 911, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'hairColor': '#BDBDBD', 'sash': HOME, 'sashW': 0.12, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("La pizza", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'president': PRES,
    'soldat1': {**SOLD, 'preset': 'cop', 'seed': 912, 'gloves': '#E3A877'},   # (review 2) bare hands: the thumbs up reads instead of a dark blob 'soldat2': {**SOLD, 'preset': 'cop2', 'seed': 913},
    **{f'general{j}': {**SOLD, 'preset': 'commissaire', 'seed': 913 + j, 'suit': '#4E5A34', 'lapel': '#3E4828', 'hair': ['receding', 'bald', 'receding'][j - 1], 'facial': ['mustache', 'none', 'beard'][j - 1], 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}} for j in (1, 2, 3)},
    'soldat3': {**SOLD, 'preset': 'commissaire', 'seed': 922, 'suit': '#4E5A34', 'lapel': '#3E4828', 'tie': '#4E5A34', 'shirt': '#4E5A34', 'gloves': '#E3A877', 'build': {'width': 1.05, 'headWidth': 1.2}},   # (review 3) an army jacket like the generals', bare hands
    'musi1': {**SOLD, 'preset': 'cop', 'seed': 920}, 'musi2': {**SOLD, 'preset': 'cop2', 'seed': 921},
    'officiel1': {'preset': 'politique', 'seed': 931, 'suit': '#4E4470', 'lapel': '#4E4470', 'tie': '#7A2333', 'sash': FLAGS[0], 'sashW': 0.12, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'officiel2': {'preset': 'politique', 'seed': 932, 'suit': '#3A4F6E', 'lapel': '#3A4F6E', 'tie': '#C8A030', 'sash': FLAGS[1], 'sashW': 0.12, 'hairColor': '#BDBDBD', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'officiel3': {'preset': 'madame', 'seed': 933, 'suit': '#4A3F5E', 'lapel': '#4A3F5E', 'sash': FLAGS[2], 'sashW': 0.12, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    **{f'courrier{j}': {**SOLD, 'preset': 'cop' if j % 2 else 'cop2', 'seed': 940 + j} for j in (1, 2, 3)},
})
