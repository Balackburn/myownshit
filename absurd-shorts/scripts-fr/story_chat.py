#!/usr/bin/env python3
"""Le chat (story 87, cycle 49; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man has a cat that will not come down. The cat was holding the tree hostage. No demands. The special forces stormed it. They do not come down
either. A tank aimed at the cat, at point-blank range. The cat ducked; the street opposite did not. Three days of air strikes. Toll: the hostage
lost a twig. This man was arrested for feeding the enemy. The cat was charged with the damage, tried at the foot of the tree, in absentia. The
hostage asked to stay with the cat. Sentenced to come down. Escorted by the soldiers. That night the cat came down to eat the seized evidence.
Then it went back up to bed.
Staging: one lone tall tree on the lawn across the road from a row of blocks of flats; a ginger cat on its bare top branch, against the sky. He
points up at it and shakes a full bowl of croquettes. Two police cars skid round the tree, an officer winds striped NE PAS FRANCHIR tape round the
trunk while he stands behind it with his bowl. A negotiator under the branch raises a megaphone; the cat licks its paw; the megaphone sinks. A
helicopter hovers, a masked commando slides down a rope and lands squatting on the branch beside the sleeping cat, which does not open its eyes;
the branch sags. Wide: four masked commandos cling to the branches, the cat calm at the top, the helicopter reels in its empty ropes and leaves
(COINCÉS). From behind a tank, its gun rises and telescopes all the way to the treetop; side close-up: the muzzle stops a hand's width from the
cat's nose; it blinks. From behind the muzzle: the cat lowers its head, the shell passes through the empty spot, the blocks across the road fold
down one after another into smoking heaps. Jets dive past the tree, bursts behind it, the sky flips day-night-day. A spokesman at a podium reads
the toll while two medics in white helmets carry a single twig on a stretcher under a foil blanket, the cat grooming at the top. He crawls through
the rubble with his bowl, two riot police pile on him, an officer holds the bowl up to the press flashes (SAISI). A bailiff staples a summons to
the trunk; close: the cat's ear twitches. At the foot of the tree a judge's bench in the rubble, the bowl on it with a red SCELLÉ tag, the bailiff
reads to an empty dock, the cat's tail dangles above the judge's wig. Close on the branch: a leafy shoot curls round the sleeping cat like an arm,
the clerk's microphone held up to the bark in the foreground. The judge bangs the gavel and points down; the cat yawns (CONDAMNÉ). From the foot of
the tree the bailiff staple-guns an ESCORTE order on each commando's boot; one salutes and nearly slips. Night: the cat walks head first down the
trunk past the commandos (their eyes follow it), hops on the empty bench and crunches the sealed croquettes. Dawn, held wide: it climbs back up
past the commandos (one still saluting, the orders flapping on their boots) and curls up inside the curled shoot; the empty sealed bowl below.
Natural look; cycle 49: props_chat.js (loneTree, treeCat, kibbleBowl, trunkTape, foldRow, extendTank, shellStreak, reelRope, twigStretcher,
fieldBench, stapleGun, stapledSheet, clerkArm, plainJet); the series' creature cat (creatures.js) driven inside treeCat; plainTank (props_place),
holedBlock (props_table, inside foldRow), helicopter (props_lunettes), policeCar, megaphone, dock, gavel, soundBlock, smokeField (props.js),
timedBurst, plainPodium (props_flaque), stretcher (props_barbecue, inside twigStretcher), tacHelmet, tacVest (props_table), balaclava (props_rambarde),
riotHelmet, riotShield, rubbleHeap (props_guepe), flashBursts (props_moustache), handMic (props_centime, inside clerkArm) reused.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.83) and heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() before stills; the cat is
the high-contrast ginger creature against the sky and never touched by anything (the shell crosses the spot its head has just left, the commando
lands beside it, the shoot curls over it without touching); nobody hurt (the blocks are empty, the pile is a comic heap, his face annoyed); the
tank is the unmarked plainTank, the jets have no roundels; no English on screen, no real organisation or flag; animated materials unique; timedBurst,
not explosionBurst; the day-night flips at under three a second."""
from story_kit import *
import math

st = Story('chat', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 18)])

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
def R5(p, w=1, s=0.04): return [*p, w, s]
EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
def blink(t, face): return [k(t, toon={'face': {**face, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face}, toonDur=0.06, keepPose=True)]

# ============================== the place: cottageStreet without its cottages (the road along X, z 0..9; the near pavement z 9..12); the lone
# tree on the near lawn at TREE; across the road the row of blocks of flats (foldRow) whose fronts stand at z ROWZ
SET = 'cottageStreet'; SETO = {'houses': []}
TX, TZ = 0.0, 14.0
def tw(x, y, z=0.0): return [r(TX + x), r(y), r(TZ + z)]
ROWZ = -5.5
SEAT = tw(0.8, 5.62)                       # the cat's place on the top branch (the branch's top surface there)
CATS = 1.6
HEADC = add(SEAT, [0.0, 0.62, 0.22])        # the sitting cat's head (measured on a still)
NOSE = add(SEAT, [0.0, 0.6, 0.42])          # its nose when it faces +Z
def TREE(sid, **o): return P(f'arbre{sid}', 'loneTree', pos=[TX, 0, TZ], opts=o)
def CAT(sid, pos=None, ry=0, keys=None, rot=None, **o):
    return P(f'chat{sid}', 'treeCat', pos=pos or SEAT, ry=ry, opts={'s': CATS, **o}, **({'keys': keys} if keys else {}), **({'rot': rot} if rot else {}))
def ROW(sid, **o): return P(f'rue{sid}', 'foldRow', pos=[0.0, 0, ROWZ], opts={'n': 5, 'w': 5.4, 'h': 12.0, **o})
LATER = {'twig': False, 'curl': [[0, 1.0]]}   # the tree after the strikes (no twig) and after the hostage's request (the shoot curled)

# the commandos clinging to the tree (from shot 5 on): cdo1 squats on the top branch beyond the cat holding on with both hands, cdo2 and cdo3 hang
# from the upper left branch, cdo4 from the right branch; each has a black helmet and a balaclava
def L1(s): return tw(-2.1 * s, 4.4 + 0.7 * s, 0.2 * s)
def R1(s): return tw(2.0 * s, 3.6 + 0.6 * s, -0.2 * s)
HANG = {'cdo2': (L1(0.33), L1(0.47), 12), 'cdo3': (L1(0.72), L1(0.86), -14), 'cdo4': (R1(0.5), R1(0.65), -18)}
CDO1 = tw(1.72, 5.62 - 0.5, 0.0)            # squatting (the toon leg bends do not lower the hips: the root goes down by hand)
SQUAT = {'legL': [-1.5, 0.25, 0, 1, None], 'legR': [-1.5, -0.25, 0, 1, None], 'shinL': [1.9, 0, 0, 1, None], 'shinR': [1.9, 0, 0, 1, None], 'spine': [0.35, 0, 0, 1, None]}
CDO1H = (tw(1.5, 5.6, 0.14), tw(1.98, 5.6, 0.14))
SCARED = {'lid': 0.0, 'pop': 0.15, 'mouth': 'wavy', 'brow': 0.8, 'sweat': 1.0}
def hang_root(a, b): return [r((a[0] + b[0]) / 2), r((a[1] + b[1]) / 2 - 2.28), r((a[2] + b[2]) / 2 - 0.02)]
def KIT(sid, who): return [P(f'casque{sid}{who}', 'tacHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}),
                          P(f'cagoule{sid}{who}', 'balaclava', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})]
def ORDER(sid, who, at=None, flap=0.25, foot='footR'):
    return P(f'ordre{sid}{who}', 'stapledSheet', on={'actor': who, 'joint': foot, 'offset': [0.0, 0.02, 0.1], 'face': 'camera'}, opts={'text': 'ESCORTE', 'w': 0.34, 'h': 0.44, 'flap': flap, 'seed': len(who), **({'at': at} if at is not None else {})})
def commandos(sid, orders=False, look=None, extra=None, salute=None, skip=(), salute1=False):
    """the four clinging commandos for a shot: legs kicking a little, scared faces; look: a point (or 'camera') for their eyes; extra: {who: [keys]};
    salute: (who, t): that one lets go with his right hand at t and salutes; orders: True (stapled from the start) or {who: time}"""
    D = st.dur(sid); acts, props = [], []
    for who, (a, b, ry) in HANG.items():
        if who in skip: continue
        root = hang_root(a, b); ph = len(who) * 0.37 + ry * 0.01
        kk = [k(0.0, look=look or 'camera')]
        for i in range(int(D / 0.42) + 2):
            t = r(i * 0.42); sw = 0.34 * math.sin(i * 1.7 + ph); sway = 0.14 * math.sin(i * 1.15 + ph * 2.3)   # (review 2) bigger kicks and a sway, each on its own phase
            hands = {'L': R5(a, 1, 0.03), 'R': R5(b, 1, 0.03)}
            if salute and salute[0] == who and t >= salute[1]: hands['R'] = R5(off(root, ry, 0.12, 0.2, 2.04), 1, 0.03)
            kk.append(k(t, toon={'reach': hands, 'hands': {'L': 'grip', 'R': 'open' if (salute and salute[0] == who and t >= salute[1]) else 'grip'},
                                 'bend': {'legL': [0.25 + sw, 0.06, 0, 1, None], 'legR': [0.1 - sw, -0.06, 0, 1, None], 'shinL': [0.5 + 0.4 * max(0, -sw), 0, 0, 1, None], 'shinR': [0.35 + 0.6 * max(0, sw), 0, 0, 1, None], 'spine': [0.05, sway, 0, 1, None]},
                                 'face': SCARED}, toonDur=0.0 if i == 0 else 0.4))
        kk += [x for bt in (0.35 + (len(who) * 0.31 + ry * 0.017) % 0.6, 1.45 + (ry * 0.013) % 0.5) if bt < D - 0.15 for x in blink(r(bt), SCARED)]   # (review 1) blinks in the holds
        if extra and who in extra: kk += extra[who]
        acts.append(act(who, root, ry, 'hangBar', 'scared', keys=kk))
        props += KIT(sid, who)
        if orders: props.append(ORDER(sid, who, at=(orders.get(who) if isinstance(orders, dict) else None)))
    if 'cdo1' not in skip:
        kk = [k(0.0, look=look or 'camera'), k(0.0, toon={'reach': {'L': R5(CDO1H[0], 1, 0.03), 'R': R5(CDO1H[1], 1, 0.03)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': SQUAT, 'face': SCARED}, toonDur=0.0)]
        for i in range(1, int(D / 0.5) + 2):
            kk.append(k(r(i * 0.5), toon={'reach': {'L': R5(add(CDO1H[0], [0, 0.0, 0.01 * (i % 2)]), 1, 0.03), 'R': R5(CDO1H[1], 1, 0.03)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': SQUAT, 'sq': [1 + 0.02 * (i % 2), 1 - 0.02 * (i % 2), 1], 'face': SCARED}, toonDur=0.5))
        if salute1:   # (review 2) the top one lets go with his right hand and salutes, wobbling on his heels
            kk = [k(0.0, look=look or 'camera')] + [k(r(i * 0.3), toon={'reach': {'L': R5(CDO1H[0], 1, 0.03), 'R': R5(off(CDO1, -8, 0.14, 0.18, 1.62), 1, 0.03)}, 'hands': {'L': 'grip', 'R': 'open'}, 'bend': {**SQUAT, 'spine': [0.3, 0.16 * (-1) ** i, 0, 1, None]}, 'sq': [1 + 0.04 * (-1) ** i, 1 - 0.04 * (-1) ** i, 1], 'face': {**SCARED, 'mouth': 'line'}}, toonDur=0.0 if i == 0 else 0.28) for i in range(int(D / 0.3) + 2)]
        if extra and 'cdo1' in extra: kk += extra['cdo1']
        acts.append(act('cdo1', CDO1, -8, 'stand', 'scared', keys=kk))
        props += KIT(sid, 'cdo1')
        if orders: props.append(ORDER(sid, 'cdo1', at=(orders.get('cdo1') if isinstance(orders, dict) else None), foot='footL'))
    return acts, props

for g_ in [('S01', 1.0, 'mec', 'bowl'), ('S03', 0.5, 'nego', 'megaphone'), ('S04', 1.2, 'cdo1', 'landing'), ('S09', 1.4, 'porte', 'toll'), ('S10', 1.6, 'officier', 'seized'),
           ('S12', 1.4, 'juge', 'trial'), ('S14', 0.5, 'juge', 'sentence'), ('S15', 1.0, 'cdo3', 'salute')]:
    st.gag(*g_)

# 1: the hook. Low and wide from the lawn: he stands at the foot of the lone tree, right arm up pointing at the cat sitting on the top branch against
#    the sky, the full bowl of croquettes shaken in his left hand; the cat looks down at him, then turns its head away
D1 = st.dur('S01')
HERO1 = tw(-0.3, 0, 2.9); RYH1 = 18
C1 = cam(0.0, [0.75, 1.25, 21.6], [0.7, 1.27, 21.3], [-0.2, 3.55, 14.3], [-0.2, 3.6, 14.3], lens=52)
PT1 = R5(off(HERO1, RYH1, 0.3, 0.32, 2.75), 1, 0.06)
BOWL1 = off(HERO1, RYH1, 0.42, -0.3, 1.6)
chk('S01', C1['from'], C1['lookAt'], 50, {'heroFace': add(HERO1, [0, 2.05, 0]), 'heroFeet': HERO1, 'hand': PT1[:3], 'bowl': BOWL1, 'cat': HEADC, 'treeTop': tw(-1.0, 7.6, -0.5), 'branchTip': tw(2.3, 5.9)})
PLEAD = {'lid': 0.1, 'mouth': 'wavy', 'brow': 0.75}
st.shot('S01', SET, setOpts=SETO, actors=[
        act('mec', HERO1, RYH1, 'stand', 'worried', keys=[k(0.0, look=HEADC),
            *[k(r(0.1 * i), toon={'reach': {'R': PT1, 'L': R5(add(BOWL1, [0.13 * (1 if i % 2 else -1), 0.1 * (i % 2), 0]), 1, 0.04)}, 'hands': {'R': 'point', 'L': 'grip'}, 'face': PLEAD, 'sq': [0.9, 1.13, 0.9] if i < 11 else [1, 1, 1], 'auto': 0}, toonDur=0.0 if i == 0 else 0.07) for i in range(int(D1 / 0.1))],   # (review 1) on tiptoe, stretched tall, the bowl shaken wide
            k(1.15, look='camera', lookDur=0.15), *blink(1.6, PLEAD)])],
        props=[TREE('S01'), ROW('S01'), CAT('S01', ry=-8, clips=[[0, 'sit']], expr=[[0, 'sleepy']], head=[[0, 0.0], [0.95, -0.9]], blinks=[0.6, 1.5]),
               P('bol1', 'kibbleBowl', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.06, 0.06], 'face': 'camera', 'faceFlat': True}, opts={'shake': [[0.0, D1]]})],
        cams=[C1])
st.cue('sfx:rattle', 'S01', 0.05, 0.3); st.cue('sfx:rattleShort', 'S01', 0.6, 0.25)

# 2: the cat was holding the tree hostage. High three-quarter: two police cars skid in round the tree, beacons flashing; an officer behind the trunk
#    winds the striped tape round it and out to four posts; he stands outside the tape with his bowl, the cat sitting calm on top
D2 = st.dur('S02')
C2 = cam(0.0, [5.6, 4.2, 25.8], [5.4, 4.2, 25.4], [-0.5, 2.8, 15.0], [-0.5, 2.8, 15.0], lens=50)
CAR2a0, CAR2a = tw(11.5, 0, 6.5), tw(3.4, 0, 3.6)
CAR2b0, CAR2b = tw(-11.0, 0, 2.0), tw(-4.2, 0, 0.6)
FLIC2 = tw(0.15, 0, -0.75); HERO2 = tw(-1.15, 0, 3.7)
POSTS = [[2.5, 1.8], [-2.6, 1.7], [2.4, -1.9], [-2.4, -1.8]]
chk('S02', C2['from'], C2['lookAt'], 50, {'cat': HEADC, 'carA': add(CAR2a, [0, 1.6, 0]), 'carB': add(CAR2b, [0, 1.6, 0]), 'flicFace': add(FLIC2, [0, 2.05, 0]), 'heroFace': add(HERO2, [0, 2.05, 0]), 'heroFeet': HERO2, 'treeTop': tw(-1.0, 7.6, -0.5)})
TAPE_H = [tw(0.3, 1.25, 0.25), tw(-0.3, 1.25, 0.25)]
st.shot('S02', SET, setOpts=SETO, actors=[
        act('flic', FLIC2, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            *[k(r(0.25 * i), toon={'reach': {'R': R5(add(TAPE_H[0], [0.05 * math.sin(i * 1.5), 0.06 * (i % 2), 0])), 'L': R5(add(TAPE_H[1], [0.05 * math.cos(i * 1.5), 0.06 * ((i + 1) % 2), 0]))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0 if i == 0 else 0.22) for i in range(8)]]),
        act('mec', HERO2, 20, 'stand', 'worried', keys=[k(0.0, look=HEADC),
            k(0.0, toon={'reach': {'L': R5(off(HERO2, 20, 0.4, -0.25, 1.3), 1, 0.04)}, 'hands': {'L': 'grip'}, 'face': PLEAD}, toonDur=0.0), k(1.2, look='camera', lookDur=0.2), *blink(1.55, PLEAD)])],
        props=[TREE('S02'), ROW('S02'), CAT('S02', ry=10, clips=[[0, 'sit']], expr=[[0, 'sleepy']], blinks=[1.1]),
               P('bol2', 'kibbleBowl', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.06, 0.06], 'face': 'camera', 'faceFlat': True}, opts={}),
               P('ruban2', 'trunkTape', pos=[TX, 0, TZ], opts={'posts': POSTS, 'wrap': [0.25, 1.3]}),
               P('voiture2a', 'policeCar', pos=CAR2a0, ry=150, keys=[k(0.0, to=CAR2a, dur=0.6, ease='out'), k(0.0, rotTo=[0, math.radians(205), 0], dur=0.6, ease='out')]),
               P('voiture2b', 'policeCar', pos=CAR2b0, ry=20, keys=[k(0.1, to=CAR2b, dur=0.6, ease='out'), k(0.1, rotTo=[0, math.radians(-30), 0], dur=0.6, ease='out')])],
        cams=[C2])
st.cue('sfx:siren', 'S02', 0.0, 0.3); st.cue('sfx:brake', 'S02', 0.15, 0.35); st.cue('sfx:brake', 'S02', 0.3, 0.3); st.cue('sfx:zip', 'S02', 0.5, 0.2)

# 3: no demands. Low in front of the negotiator standing under the branch: he raises the megaphone toward the cat above him; the cat, facing us,
#    licks its paw; the megaphone slowly sinks and he looks at us
D3 = st.dur('S03')
NEGO = tw(0.45, 0, 1.45); RYN = 10
C3 = cam(0.0, [1.15, 0.85, 19.4], [1.1, 0.87, 19.2], [0.65, 3.5, 14.5], [0.65, 3.55, 14.5], lens=58)
MEG_UP = R5(off(NEGO, RYN, 0.3, 0.38, 2.7), 1, 0.06); MEG_DN = R5(off(NEGO, RYN, 0.35, 0.22, 1.25), 1, 0.06)
chk('S03', C3['from'], C3['lookAt'], 56, {'negoFace': add(NEGO, [0, 2.05, 0]), 'megUp': MEG_UP[:3], 'cat': HEADC, 'negoFeet': NEGO, 'branch': tw(1.6, 5.6)})
NF = {'lid': 0.2, 'mouth': 'O', 'brow': 0.5}
st.shot('S03', SET, setOpts=SETO, actors=[
        act('nego', NEGO, RYN, 'stand', 'neutral', keys=[k(0.0, look=add(NEGO, [0.2, 4.0, 0.9])),
            k(0.0, toon={'reach': {'R': MEG_UP}, 'hands': {'R': 'grip'}, 'face': NF, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.0),
            k(0.55, toon={'reach': {'R': MEG_UP}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}}, toonDur=0.2),
            k(0.75, toon={'reach': {'R': MEG_DN}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.6, 'mouth': 'flat', 'brow': -0.3}, 'sq': [1.14, 0.8, 1.14], 'bend': {'spine': [0.35, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}}, toonDur=0.4, toonEase='inOut'),   # (review 1) he deflates with the megaphone
            k(0.95, look='camera', lookDur=0.2)])],
        props=[TREE('S03'), ROW('S03'), CAT('S03', ry=5, clips=[[0, 'sit']], expr=[[0, 'sleepy']], lick=[[0.15, 1.3]]),
               P('megaphone3', 'megaphone', on={'actor': 'nego', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'rot': [-1.2, 0, 0]}, scale=1.7)],
        cams=[C3])
st.cue('sfx:static', 'S03', 0.05, 0.25); st.cue('sfx:sniff', 'S03', 0.5, 0.15)

# 4: the special forces stormed it. At branch height: the helicopter hovers over the tree, a rope hangs from it, a masked commando slides down and lands
#    squatting on the branch beside the sleeping cat; the branch sags and wobbles; the cat does not open its eyes
D4 = st.dur('S04'); LAND4 = 1.0
HELI = tw(1.3, 10.6, 0.0)
C4 = cam(0.0, [2.6, 6.35, 19.6], [2.55, 6.4, 19.3], [1.15, 7.2, 14.0], [1.15, 7.15, 14.0], lens=52)
TOP4 = add(CDO1, [0, 3.1, 0])
chk('S04', C4['from'], C4['lookAt'], 52, {'cat': add(SEAT, [0, 0.3, 0.1]), 'cdoFaceLanded': add(CDO1, [0, 1.6, 0]), 'cdoFaceTop': add(TOP4, [0, 2.0, 0]), 'heli': HELI, 'heliSkid': add(HELI, [0, -1.2, 0])})
SLIDE = {'L': R5(add(TOP4, [0.0, 2.55, 0.05]), 1, 0.03), 'R': R5(add(TOP4, [0.0, 2.3, 0.05]), 1, 0.03)}
st.shot('S04', SET, setOpts=SETO, actors=[
        act('cdo1', TOP4, -8, 'stand', 'determined', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': SLIDE, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'legL': [-0.4, 0.1, 0, 1, None], 'legR': [-0.25, -0.1, 0, 1, None], 'shinL': [0.6, 0, 0, 1, None], 'shinR': [0.5, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.0),
            k(0.0, to=CDO1, dur=LAND4, ease='in', glide=True, face='keep'),
            k(0.0, toon={'reach': {'L': R5(add(CDO1, [0.0, 2.55, 0.05]), 1, 0.03), 'R': R5(add(CDO1, [0.0, 2.3, 0.05]), 1, 0.03)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'legL': [-0.4, 0.1, 0, 1, None], 'legR': [-0.25, -0.1, 0, 1, None], 'shinL': [0.6, 0, 0, 1, None], 'shinR': [0.5, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.6}}, toonDur=LAND4, toonEase='in'),
            k(LAND4, toon={'reach': {'L': R5(off(CDO1, -8, 0.4, -0.42, 1.75)), 'R': R5(off(CDO1, -8, 0.4, 0.42, 1.75))}, 'hands': {'L': 'open', 'R': 'open'}, 'bend': SQUAT, 'sq': [1.12, 0.85, 1.12], 'face': {'lid': 0.0, 'pop': 0.2, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.05, toonEase='out'),
            k(r(LAND4 + 0.12), toon={'reach': {'L': R5(off(CDO1, -8, 0.35, -0.5, 2.0)), 'R': R5(off(CDO1, -8, 0.3, 0.45, 1.4))}, 'hands': {'L': 'open', 'R': 'open'}, 'bend': SQUAT, 'sq': [0.97, 1.04, 0.97], 'face': SCARED}, toonDur=0.12),
            k(r(LAND4 + 0.3), toon={'reach': {'L': R5(off(CDO1, -8, 0.3, -0.45, 1.4)), 'R': R5(off(CDO1, -8, 0.35, 0.5, 2.0))}, 'hands': {'L': 'open', 'R': 'open'}, 'bend': SQUAT, 'face': SCARED}, toonDur=0.15),
            k(r(LAND4 + 0.45), toon={'reach': {'L': R5(CDO1H[0], 1, 0.03), 'R': R5(CDO1H[1], 1, 0.03)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': SQUAT, 'face': SCARED}, toonDur=0.2),
            k(r(LAND4 + 0.3), look=add(SEAT, [0, 0.3, 0]), lookDur=0.15), k(r(LAND4 + 0.7), look='camera', lookDur=0.12)])],
        props=[TREE('S04', sag=[[0, 0], [LAND4, 0.1]], wobAt=[LAND4]), ROW('S04'), CAT('S04', ry=-20, clips=[[0, 'sleep']]),
               P('heli4', 'helicopter', pos=HELI, ry=90, scale=0.85, opts={'spin': 6}),
               P('corde4', 'reelRope', pos=add(HELI, [0.42, -0.9, 0.0]), opts={'len': [[0, 3.1]], 'r': 0.035}), *KIT('4', 'cdo1')],
        cams=[C4])
st.cue('sfx:rotor', 'S04', 0.0, 0.45); st.cue('sfx:slideDown', 'S04', 0.1, 0.3); st.cue('thud', 'S04', LAND4, 0.45); st.cue('sfx:boing', 'S04', r(LAND4 + 0.03), 0.2)

# 5: they do not come down either. Wide from the lawn: the whole tree with four masked commandos clinging to it, the cat calm at the top; the
#    helicopter reels in its empty ropes and flies off to the right
D5 = st.dur('S05')
C5 = cam(0.0, [-1.6, 1.0, 27.2], [-1.5, 1.05, 26.9], [0.35, 4.9, 14.0], [0.35, 4.9, 14.0], lens=42)   # (review 2) low: the cat stands against the sky above the facades
HELI5 = tw(1.0, 10.8, -1.0)
acts5, props5 = commandos('S05')
chk('S05', C5['from'], C5['lookAt'], 42, {'cat': HEADC, 'cdo1': add(CDO1, [0, 1.6, 0]), **{w: add(hang_root(a, b), [0, 2.05, 0]) for w, (a, b, _) in HANG.items()}, 'heli': HELI5, 'heliOut': add(HELI5, [7.5, 3.0, -2.0]), 'base': tw(0, 0, 0)})
st.shot('S05', SET, setOpts=SETO, actors=acts5,
        props=[TREE('S05', sag=[[0, 0.1]]), ROW('S05'), CAT('S05', ry=-15, clips=[[0, 'sit']], expr=[[0, 'sleepy']], blinks=[0.9]), *props5,
               P('heli5', 'helicopter', pos=HELI5, ry=90, scale=0.85, opts={'spin': 6}, keys=[k(0.15, to=add(HELI5, [9.0, 4.5, -2.0]), dur=0.7, ease='in'), k(0.15, rotTo=[0, PI / 2, 0.25], dur=0.3)]),
               *[P(f'corde5{j}', 'reelRope', pos=add(HELI5, [0.42 + 0.3 * j, -0.9, 0.0]), opts={'len': [[0, 3.3], [0.05, 0.3]], 'seed': j}, keys=[k(0.15, to=add(HELI5, [9.42 + 0.3 * j, 3.6, -2.0]), dur=0.7, ease='in')]) for j in range(2)]],
        cams=[C5])
st.card('S05', 'COINCÉS', at=0.9)   # (review 1) after the helicopter and its ropes have left the card band
st.cue('sfx:rotor', 'S05', 0.0, 0.4); st.cue('whoosh', 'S05', 0.55, 0.3, 0.9, 300, 1500)

# 6: a tank aimed at the cat, at point-blank range. From behind the tank on the lawn: its gun rises toward the treetop and slides out in sleeves all
#    the way to the cat; then side close-up at the branch: the muzzle arrives and stops a hand's width from the cat's nose; the cat blinks
D6 = st.dur('S06'); CUT6 = r(st.at('S06', 'L06', 6) - 0.12)
TANK = [SEAT[0], 0, 34.0]
GUNP = [TANK[0], 1.34, r(TANK[2] - 0.65)]            # the gun's pivot (tank turned 180: its front toward -Z)
dy, dz = NOSE[1] - GUNP[1], GUNP[2] - NOSE[2]
PITCH = -r(math.atan2(dy, dz), 4); DIST = math.hypot(dy, dz)
GAP = 0.24
EXT = r(DIST - 2.95 - 0.31 - GAP, 2)                # the brake's mouth a hand's width from the nose (a big cartoon hand)
UNIT = [0.0, dy / DIST, -dz / DIST]
MUZ = [r(GUNP[i] + UNIT[i] * (DIST - GAP)) for i in range(3)]
C6a = cam(0.0, [2.6, 4.0, 46.0], [2.5, 4.05, 45.6], [0.5, 3.5, 20.0], [0.5, 3.7, 20.0], lens=26)   # (review 1) the barrel crosses the frame diagonally to a bigger treetop
C6b = cam(CUT6, add(HEADC, [2.0, 0.2, 2.35]), add(HEADC, [1.9, 0.19, 2.25]), add(HEADC, [-0.05, -0.15, 0.2]), add(HEADC, [-0.05, -0.15, 0.2]), lens=40)   # (review 1) the cat's face 3/4 to the lens, the street behind
chk('S06a', C6a['from'], C6a['lookAt'], 26, {'tankTop': [TANK[0], 2.4, TANK[2]], 'tankFoot': [TANK[0] + 1.6, 0, TANK[2] - 2.4], 'cat': HEADC, 'mid': [GUNP[i] + UNIT[i] * DIST * 0.5 for i in range(3)]})
chk('S06b', C6b['from'], C6b['lookAt'], 40, {'catHead': HEADC, 'nose': NOSE, 'muzzle': MUZ, 'barrelBack': [GUNP[i] + UNIT[i] * (DIST - 2.2) for i in range(3)], 'seat': SEAT})
EXTK6 = [[0.0, 0.0], [0.45, 2.0], [0.7, 6.0], [0.95, 10.5], [1.2, 14.5], [r(CUT6 + 0.15), r(EXT + 0.25)], [r(CUT6 + 0.4), EXT]]
TANKP = lambda sid, ext, gun, **o: P(f'char{sid}', 'extendTank', pos=TANK, ry=180, opts={'ext': ext, 'gun': gun, 'segs': 9, **o})
st.shot('S06', SET, setOpts=SETO, actors=commandos('S06', skip=('cdo1',), extra={w: [k(CUT6, visible=False)] for w in ('cdo2', 'cdo3', 'cdo4')})[0],   # (review 1) no commando clutter in the close-up
        props=[TREE('S06', sag=[[0, 0.1]], tip=False), ROW('S06'), CAT('S06', ry=0, clips=[[0, 'sit']], expr=[[0, 'neutral'], [r(CUT6 + 0.5), 'sleepy']], blinks=[r(CUT6 + 0.75), r(CUT6 + 1.05)]),
               TANKP('S06', EXTK6, [[0.0, 0.0], [0.1, PITCH]], rumble=[[0.0, 1.3, 0.015]]), *commandos('S06', skip=('cdo1',))[1]],
        cams=[C6a, C6b])
st.cue('engine', 'S06', 0.0, 0.3, 1.3); st.cue('sfx:stretch', 'S06', 0.4, 0.35); st.cue('clang', 'S06', r(CUT6 + 0.15), 0.3); st.cue('sfx:gulp', 'S06', r(CUT6 + 0.75), 0.0)

# 7: the cat ducked; the street opposite did not. From behind the muzzle, past it: the cat calmly lowers its head flat on the branch, the gun fires,
#    the shell crosses the empty spot where its head was and flies on to the blocks across the road, which fold down one after another into smoking
#    heaps; the cat lifts its head again and looks at us
D7 = st.dur('S07'); DUCK7, FIRE7 = 0.4, 0.62; SHELL7 = 0.08; FOLD7 = r(FIRE7 + SHELL7 + 0.06)   # (review 1) the head stays down until the shell is through; the burst and the fold come on its arrival
HIT = [r(MUZ[i] + UNIT[i] * ((ROWZ - MUZ[2]) / UNIT[2])) for i in range(3)]
C7 = cam(0.0, add(MUZ, [-1.1, 0.7, 2.6]), add(MUZ, [-1.08, 0.69, 2.5]), [1.2, 6.0, 10.0], [1.2, 5.95, 10.0], lens=60)
chk('S07', C7['from'], C7['lookAt'], 60, {'catHead': HEADC, 'muzzle': MUZ, 'hit': HIT, 'blockFoot': [0, 0.5, ROWZ], 'blockTopL': [-8, 11, ROWZ], 'blockTopR': [8, 11, ROWZ]})
st.shot('S07', SET, setOpts=SETO, actors=[],
        props=[TREE('S07', sag=[[0, 0.1]]), ROW('S07', foldAt=FOLD7, stagger=0.1, h=13.5), TANKP('S07', [[0, EXT]], [[0, PITCH]], fireAt=FIRE7, flashS=0.35, puffS=0.01),
               CAT('S07', ry=0, clips=[[0, 'sit']], expr=[[0, 'sleepy']], duck=[[0, 0], [DUCK7, 1.0], [1.05, 0.0]], flat=1.0, duckBlend=0.1, blinks=[1.9], head=[[1.3, 0.0], [1.5, 0.35]]),
               P('obus7', 'shellStreak', pos=[0, 0, 0], opts={'from': MUZ, 'to': HIT, 't0': FIRE7, 'dur': SHELL7, 'r': 0.055, 'len': 0.3}),
               P('boum7', 'timedBurst', pos=add(HIT, [0, -0.8, 0.5]), opts={'at': r(FIRE7 + SHELL7), 'size': 2.2, 'life': 0.45})],
        cams=[C7])
st.cue('thud', 'S07', FIRE7, 0.6); st.cue('whoosh', 'S07', FIRE7, 0.35, 0.2, 800, 4000); st.cue('thunder', 'S07', r(FIRE7 + SHELL7), 0.4); st.cue('thud', 'S07', FOLD7, 0.4); st.cue('thud', 'S07', r(FOLD7 + 0.2), 0.4); st.cue('thud', 'S07', r(FOLD7 + 0.4), 0.4)

# 8: three days of air strikes. Low on the lawn: the tree and the cat against the sky, jets dive past behind it, bursts go up in the ruins across
#    the road, the sky flips day-night-day; the cat grooms
D8 = st.dur('S08')
C8 = cam(0.0, [2.2, 1.25, 27.5], [2.1, 1.3, 27.0], [0.3, 4.8, 10.0], [0.3, 4.9, 10.0], lens=46)
JETS = [([-30, 30, -18], [30, 9, -14], 0.0, 0.9), ([30, 34, -24], [-30, 12, -20], 0.55, 0.9), ([-28, 30, -12], [32, 10, -10], 1.0, 0.8)]
BURSTS = [(4.4, 1.2, 0.35), (2.6, 1.0, 0.75), (4.9, 1.4, 1.15), (3.4, 0.9, 1.5)]   # (review 2) at ground level in the ruins   # (review 1) all in the ruins beside the tree in the frame, none behind the commandos
chk('S08', C8['from'], C8['lookAt'], 46, {'cat': HEADC, 'treeTop': tw(-1.0, 7.6, -0.5), **{f'burst{i}': [x, y, ROWZ - 1] for i, (x, y, _) in enumerate(BURSTS)}, 'jetMid': [0, 20, -16]})
st.shot('S08', SET, setOpts=SETO, daynight={'from': 0.05, 'period': 0.85}, actors=commandos('S08')[0],
        props=[TREE('S08', sag=[[0, 0.1]]), ROW('S08', ruined=True), CAT('S08', ry=-10, clips=[[0, 'sit']], expr=[[0, 'sleepy']], lick=[[0.3, 1.7]]), *commandos('S08')[1],
               *[P(f'jet8{i}', 'plainJet', pos=a, ry=yaw(a, b), rot=[0, math.radians(yaw(a, b)), 0.5 if b[0] > a[0] else -0.5], scale=0.4, opts={'burner': 0.7, 'glow': 0.4}, keys=[k(t0, to=b, dur=d, ease='linear')]) for i, (a, b, t0, d) in enumerate(JETS)],
               *[P(f'boum8{i}', 'timedBurst', pos=[x, y, ROWZ - 1.0], opts={'at': t, 'size': 2.6, 'life': 0.5, 'seed': i + 3}) for i, (x, y, t) in enumerate(BURSTS)]],
        cams=[C8])
for i, (_, _, t0, _) in enumerate(JETS): st.cue('sfx:jet', 'S08', t0, 0.35)
for (_, _, t) in BURSTS: st.cue('thud', 'S08', t, 0.45)

# 9: toll: the hostage lost a twig. On the lawn: the spokesman at his podium (left foreground) reads the toll off a sheet; behind him two medics in
#    white helmets carry the stretcher toward us with one twig under a shining foil blanket; the tree behind with the cat grooming at the top; the
#    ruins smoking across the road
D9 = st.dur('S09')
C9 = cam(0.0, [-0.9, 2.2, 27.0], [-0.85, 2.2, 26.7], [-0.5, 2.6, 16.0], [-0.5, 2.6, 16.0], lens=48)
PORTE = tw(-0.2, 0, 8.2); RYP = -12
MED_DIR = [0.6, 0, 0.8]; MED1a = tw(-2.0, 0, 2.3); WALK9 = 1.5   # (review 2) they end beside the podium, not behind the spokesman   # (review 1) diagonally toward us in a clear lane left of the podium
MED1b = [r(MED1a[0] + MED_DIR[0] * WALK9), 0, r(MED1a[2] + MED_DIR[2] * WALK9)]
GAP9 = 2.2
def back9(p): return [r(p[0] - MED_DIR[0] * GAP9), 0, r(p[2] - MED_DIR[2] * GAP9)]
MRY = yaw([0, 0, 0], MED_DIR)
STR9a = [r((MED1a[0] + back9(MED1a)[0]) / 2), 0.98, r((MED1a[2] + back9(MED1a)[2]) / 2)]; STR9b = [r((MED1b[0] + back9(MED1b)[0]) / 2), 0.98, r((MED1b[2] + back9(MED1b)[2]) / 2)]
def handles(c, sgn): return [[r(c[0] + sgn * MED_DIR[0] * 1.02 + MED_DIR[2] * sd * 0.27), 0.98, r(c[2] + sgn * MED_DIR[2] * 1.02 - MED_DIR[0] * sd * 0.27)] for sd in (1, -1)]
chk('S09', C9['from'], C9['lookAt'], 48, {'porteFace': add(PORTE, [0, 2.05, 0]), 'cat': HEADC, 'med1aFace': add(MED1a, [0, 2.05, 0]), 'med1bFace': add(MED1b, [0, 2.05, 0]), 'med2bFace': add(back9(MED1b), [0, 2.05, 0]), 'twigA': STR9a, 'twigB': STR9b, 'ruins': [3, 4, ROWZ]})
MEDK = lambda sgn: [k(0.0, toon={'reach': {'R': R5(handles(STR9a, sgn)[0], 1, 0.03), 'L': R5(handles(STR9a, sgn)[1], 1, 0.03)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
                    k(D9, toon={'reach': {'R': R5(handles(STR9b, sgn)[0], 1, 0.03), 'L': R5(handles(STR9b, sgn)[1], 1, 0.03)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=D9, toonEase='linear')]
SPK = {'lid': 0.35, 'mouth': 'line', 'brow': 0.2}
PAGE9 = off(PORTE, RYP, 0.42, 0.0, 1.16); FLIP9 = 1.25   # the sheets on the podium top; he turns the page
st.shot('S09', SET, setOpts=SETO, actors=[
        act('porte', PORTE, RYP, 'stand', 'neutral', keys=[k(0.0, look=PAGE9), k(0.0, toon={'reach': {'L': R5(add(PAGE9, [0.18, 0.03, 0.02])), 'R': R5(add(PAGE9, [-0.2, 0.03, 0.02]))}, 'hands': {'R': 'rest', 'L': 'rest'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': SPK}, toonDur=0.0),
            *st.talk('L09', 'S09', 'neutral'), k(0.55, look='camera', lookDur=0.15), k(r(FLIP9 - 0.25), look=PAGE9, lookDur=0.12),
            k(r(FLIP9 - 0.15), toon={'reach': {'L': R5(add(PAGE9, [0.25, 0.06, 0.0]), 1, 0.05), 'R': R5(add(PAGE9, [-0.2, 0.03, 0.02]))}, 'hands': {'L': 'pinch', 'R': 'rest'}, 'bend': {'spine': [0.16, 0, 0, 1, None]}, 'face': SPK}, toonDur=0.12),
            k(r(FLIP9 + 0.2), toon={'reach': {'L': R5(add(PAGE9, [-0.1, 0.14, 0.0]), 1, 0.05), 'R': R5(add(PAGE9, [-0.2, 0.03, 0.02]))}, 'hands': {'L': 'pinch', 'R': 'rest'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': SPK}, toonDur=0.22),
            k(r(FLIP9 + 0.35), look='camera', lookDur=0.15), *blink(0.9, SPK), *blink(2.05, SPK)]),
        act('medic1', MED1a, MRY, 'walk', 'neutral', keys=[k(0.0, to=MED1b, dur=D9, clip='walk'), k(0.0, look='camera'), *MEDK(1)]),
        act('medic2', back9(MED1a), MRY, 'walk', 'neutral', keys=[k(0.0, to=back9(MED1b), dur=D9, clip='walk'), k(0.0, look=STR9a), *MEDK(-1)]),
        *commandos('S09')[0]],
        props=[TREE('S09', sag=[[0, 0.1]], twig=False), ROW('S09', ruined=True), CAT('S09', ry=-10, clips=[[0, 'sit']], expr=[[0, 'sleepy']], lick=[[0.2, 2.2]]), *commandos('S09')[1],
               P('pupitre9', 'plainPodium', pos=off(PORTE, RYP, 0.55, 0, 0), ry=RYP + 180, opts={}),
               P('page9a', 'flipPage', pos=add(PAGE9, [-0.0, -0.01, 0.0]), ry=RYP, opts={'text': 'BILAN'}), P('page9b', 'flipPage', pos=PAGE9, ry=RYP, opts={'text': 'BILAN', 'flipAt': FLIP9}),
               *[P(f'bande9{j}', 'medicStripe', on={'actor': f'medic{j}', 'joint': 'torso', 'offset': [0.0, 0.32, 0.0]}) for j in (1, 2)],
               P('civiere9', 'twigStretcher', pos=STR9a, ry=MRY, opts={'twigS': 2.0, 'twigUp': 1.45}, keys=[k(0.0, to=STR9b, dur=D9, ease='linear')]),
               P('casqueM1', 'tacHelmet', on={'actor': 'medic1', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'color': '#F2F2EE'}),
               P('casqueM2', 'tacHelmet', on={'actor': 'medic2', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'color': '#F2F2EE'}),
               *[P(f'gravats9{i}', 'rubbleHeap', pos=tw(x, 0, z), ry=a, opts={'r': 1.3, 'h': 0.6}) for i, (x, z, a) in enumerate([(-3.4, -1.0, 20), (3.6, -1.6, 70)])]],
        cams=[C9])
for j in range(6): st.cue('sfx:stepSoft', 'S09', r(0.1 + 0.4 * j), 0.18)

# 10: this man was arrested for feeding the enemy. Low on the lawn at the foot of the tree: he sneaks in crouching with his bowl; at the edges two
#     riot police in light helmets crouch (four frames) and pounce from both sides; they lift him clear of the ground by the arms, legs kicking over
#     the grass, his face annoyed (nobody hurt); the bowl drops; at the right the officer picks it up and raises it over his head with both hands,
#     against the sky, to three press flashes (SAISI)
D10 = st.dur('S10'); PILE10 = 0.7; LIFT10 = 1.05; UPH = 0.62
C10 = cam(0.0, [0.3, 1.0, 25.6], [0.29, 1.01, 25.4], [0.2, 2.05, 18.5], [0.2, 2.1, 18.5], lens=46)
RY10 = 0
HERO10a, HERO10b = tw(-0.3, 0, 3.4), tw(-0.3, 0, 4.2)
HERO10c = add(HERO10b, [0, UPH, 0])
BOWL10 = tw(0.55, 0, 4.6)
OFFC = tw(1.3, 0, 4.0); RYO = -18
UP10 = add(OFFC, [-0.05, 2.62, 0.18])
CR1, CR2 = add(HERO10b, [-0.68, 0, -0.05]), add(HERO10b, [0.68, 0, -0.05])
CR1a, CR2a = add(CR1, [-0.45, 0, 0.3]), add(CR2, [0.4, 0, 0.45])
chk('S10', C10['from'], C10['lookAt'], 46, {'heroFace': add(HERO10c, [0, 2.05, 0]), 'heroFeet': HERO10c, 'bowlGround': BOWL10, 'offFace': add(OFFC, [0, 2.05, 0]), 'bowlUp': UP10, 'crs1Face': add(CR1, [0, 2.05, 0]), 'crs2Face': add(CR2, [0, 2.05, 0]), 'crs1a': add(CR1a, [0, 1.6, 0]), 'crs2a': add(CR2a, [0, 1.6, 0])})
ANNOY = {'lid': 0.55, 'mouth': 'flat', 'brow': -0.5}
HOLDA = {'R': R5(add(HERO10c, [-0.42, 1.45, 0.05]), 1, 0.05), 'L': R5(add(HERO10c, [0.42, 1.45, 0.05]), 1, 0.05)}
def KICK(i): return {'legL': [0.35 * (-1) ** i, 0.1, 0, 1, None], 'legR': [-0.35 * (-1) ** i, -0.1, 0, 1, None], 'shinL': [0.5 + 0.3 * (i % 2), 0, 0, 1, None], 'shinR': [0.8 - 0.3 * (i % 2), 0, 0, 1, None]}
st.shot('S10', SET, setOpts=SETO, actors=[
        act('mec', HERO10a, RY10, 'sneak', 'determined', keys=[k(0.0, to=HERO10b, dur=PILE10, clip='sneak', face='keep'), k(0.0, look=add(HERO10b, [0, 0, 1.5])),
            k(0.0, toon={'reach': {'R': R5(add(HERO10a, [-0.15, 1.15, 0.4]), 1, 0.05), 'L': R5(add(HERO10a, [0.15, 1.15, 0.4]), 1, 0.05)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.0),
            k(r(PILE10 - 0.05), toon={'reach': {'R': R5(add(HERO10b, [-0.15, 1.15, 0.4]), 1, 0.05), 'L': R5(add(HERO10b, [0.15, 1.15, 0.4]), 1, 0.05)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.4}}, toonDur=r(PILE10 - 0.05), toonEase='linear'),
            k(PILE10, clip='stand', blend=0.02), k(PILE10, to=HERO10c, dur=0.12, ease='out', glide=True, face='keep'),
            k(PILE10, toon={'reach': HOLDA, 'hands': {'R': 'open', 'L': 'open'}, 'bend': KICK(0), 'face': {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.8}, 'sq': [0.92, 1.1, 0.92]}, toonDur=0.06, toonEase='out'),
            *[k(r(PILE10 + 0.16 + 0.17 * i), toon={'reach': HOLDA, 'hands': {'R': 'open', 'L': 'open'}, 'bend': KICK(i + 1), 'face': ANNOY, 'sq': [1, 1, 1]}, toonDur=0.14) for i in range(10)],
            k(r(PILE10 + 0.2), look=UP10, lookDur=0.15), k(r(LIFT10 + 0.7), look='camera', lookDur=0.15), *blink(2.25, ANNOY)]),
        *[act(w, pa, ry, 'stand', 'determined', keys=[k(0.0, look=HERO10b),
            k(0.0, toon={'reach': {'R': R5(add(pa, [-0.25, 1.0, 0.3])), 'L': R5(add(pa, [0.25, 1.0, 0.3]))}, 'hands': {'R': 'fist', 'L': 'fist'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.0),
            k(r(PILE10 - 0.14), toon={'reach': {'R': R5(add(pa, [-0.25, 0.85, 0.35])), 'L': R5(add(pa, [0.25, 0.85, 0.35]))}, 'hands': {'R': 'fist', 'L': 'fist'}, 'sq': [1.12, 0.84, 1.12], 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.06),   # (review 2) a crouch before the pounce
            k(r(PILE10 - 0.02), to=p, dur=0.12, ease='out', glide=True, face='keep'),
            k(r(PILE10 - 0.02), toon={'reach': {('L' if sd > 0 else 'R'): R5(add(HERO10c, [-sd * 0.3, 1.5, 0.08]), 1, 0.05), ('R' if sd > 0 else 'L'): R5(add(HERO10c, [-sd * 0.28, 1.2, 0.14]), 1, 0.05)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [0.94, 1.08, 0.94], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.12, toonEase='out'),
            k(r(PILE10 + 0.2), toon={'reach': {('L' if sd > 0 else 'R'): R5(add(HERO10c, [-sd * 0.3, 1.5, 0.08]), 1, 0.05), ('R' if sd > 0 else 'L'): R5(add(HERO10c, [-sd * 0.28, 1.2, 0.14]), 1, 0.05)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1, 1, 1], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.12),
            k(r(PILE10 + 0.35), look='camera', lookDur=0.15), *blink(r(1.6 + 0.2 * sd), {'lid': 0.3, 'mouth': 'line', 'brow': -0.6})])
          for w, pa, p, ry, sd in (('crs1', CR1a, CR1, 25, -1), ('crs2', CR2a, CR2, -25, 1))],
        act('officier', OFFC, RYO, 'stand', 'smug', keys=[k(0.0, look=BOWL10),
            k(0.0, toon={'reach': {'R': R5(off(OFFC, RYO, 0.2, 0.3, 1.0)), 'L': R5(off(OFFC, RYO, 0.2, -0.3, 1.0))}, 'hands': {'R': 'rest', 'L': 'rest'}}, toonDur=0.0),
            k(r(LIFT10 - 0.3), toon={'reach': {'R': R5(add(BOWL10, [-0.18, 0.1, 0])), 'L': R5(add(BOWL10, [0.18, 0.1, 0]))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [1.0, 0, 0, 1, None]}}, toonDur=0.2),
            k(LIFT10, toon={'reach': {'R': R5(add(UP10, [-0.2, -0.02, 0]), 1, 0.06), 'L': R5(add(UP10, [0.2, -0.02, 0]), 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [0.93, 1.09, 0.93], 'face': {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.4}}, toonDur=0.2, toonEase='out'),
            *[k(r(LIFT10 + 0.35 + 0.35 * i), toon={'reach': {'R': R5(add(UP10, [-0.2, -0.02 + 0.05 * (i % 2), 0]), 1, 0.06), 'L': R5(add(UP10, [0.2, -0.02 + 0.05 * (i % 2), 0]), 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1, 1, 1], 'face': {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.4}}, toonDur=0.25) for i in range(4)],
            k(r(LIFT10 + 0.2), look='camera', lookDur=0.15), *blink(2.1, {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.4})])],
        props=[TREE('S10', **LATER, sag=[[0, 0.1]]), ROW('S10', ruined=True),
               P('bol10m', 'kibbleBowl', on={'actor': 'mec', 'hand': 'L', 'offset': [0.0, -0.06, 0.08], 'face': 'camera', 'faceFlat': True}, keys=[k(PILE10, visible=False)]),
               P('bol10', 'kibbleBowl', pos=add(BOWL10, [-0.4, 1.0, -0.3]), ry=0, keys=[k(0.0, visible=False), k(PILE10, visible=True), k(PILE10, to=BOWL10, dur=0.22, ease='in'),
                   k(r(LIFT10 - 0.1), to=add(UP10, [0, -0.1, 0]), dur=0.3, ease='out'), k(r(LIFT10 - 0.1), rotTo=[0.5, 0, 0], dur=0.3)]),
               P('flashs10', 'flashBursts', pos=add(UP10, [0.0, 0.1, 0.4]), opts={'n': 3, 'w': 0.8, 'h': 0.5, 'at': [r(LIFT10 + 0.22), r(LIFT10 + 0.57), r(LIFT10 + 0.92)]}),   # the flashes pop on the held-up bowl
               *[P(f'casqueC{j}', 'visorHelmet', on={'actor': f'crs{j}', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}) for j in (1, 2)],
               *[P(f'gravats10{i}', 'rubbleHeap', pos=tw(x, 0, z), ry=a, opts={'r': 1.2, 'h': 0.5}) for i, (x, z, a) in enumerate([(-2.6, 2.2, 15), (3.1, 1.8, 80)])]],
        cams=[C10])
st.card('S10', 'SAISI', at=r(LIFT10 + 0.24))
st.cue('sfx:stepSoft', 'S10', 0.1, 0.2); st.cue('sfx:stepSoft', 'S10', 0.4, 0.2); st.cue('whoosh', 'S10', r(PILE10 - 0.02), 0.3, 0.15, 600, 2500); st.cue('sfx:grunt', 'S10', PILE10, 0.3); st.cue('clang', 'S10', r(PILE10 + 0.22), 0.25)
for j in range(3): st.cue('sfx:shutter', 'S10', r(LIFT10 + 0.22 + 0.35 * j), 0.35)

# 11: the cat was charged with the damage. At the trunk: the bailiff in black staples the summons to the bark with a staple gun (two clacks); then
#     close on the cat sitting on the branch: one ear flicks, then the other
D11 = st.dur('S11'); STAP11 = [0.45, 0.72]; CUT11 = r(st.at('S11', 'L11', 4) - 0.1)
HUIS = tw(0.95, 0, 0.75); RYHU = -55
SUM = tw(0.04, 1.75, 0.31)
C11a = cam(0.0, [-1.3, 1.8, 17.6], [-1.25, 1.8, 17.4], [0.7, 1.8, 14.3], [0.7, 1.8, 14.3], lens=46)
C11b = cam(CUT11, add(HEADC, [0.9, 0.25, 1.9]), add(HEADC, [0.85, 0.24, 1.75]), add(HEADC, [0.0, -0.05, 0.0]), add(HEADC, [0.0, -0.05, 0.0]), lens=44)
chk('S11a', C11a['from'], C11a['lookAt'], 46, {'huisFace': add(HUIS, [0, 2.05, 0]), 'sheet': SUM, 'sheetTop': add(SUM, [0, 0.29, 0])})
chk('S11b', C11b['from'], C11b['lookAt'], 44, {'catHead': HEADC, 'seat': SEAT, 'ear': add(HEADC, [0.1, 0.25, 0])})
GUN11 = R5(add(SUM, [0.08, 0.12, 0.12]), 1, 0.05)
st.shot('S11', SET, setOpts=SETO, actors=[*commandos('S11')[0],
        act('huissier', HUIS, RYHU, 'stand', 'unimpressed', keys=[k(0.0, look=SUM),
            k(0.0, toon={'reach': {'R': R5(add(SUM, [0.2, 0.0, 0.35])), 'L': R5(add(SUM, [-0.12, 0.05, 0.08]), 1, 0.05)}, 'hands': {'R': 'grip', 'L': 'open'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            *[x for t_ in STAP11 for x in (k(r(t_ - 0.12), toon={'reach': {'R': GUN11, 'L': R5(add(SUM, [-0.12, 0.05, 0.08]), 1, 0.05)}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': [1.04, 0.97, 1.04]}, toonDur=0.1),
                                           k(r(t_ + 0.06), toon={'reach': {'R': R5(add(GUN11[:3], [0.02, 0.0, 0.08]), 1, 0.05), 'L': R5(add(SUM, [-0.12, 0.05, 0.08]), 1, 0.05)}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': [1, 1, 1]}, toonDur=0.08))],
            k(0.95, look='camera', lookDur=0.15)])],
        props=[TREE('S11', twig=False, sag=[[0, 0.1]], summons={'at': STAP11[0], 'text': 'CONVOCATION'}), ROW('S11', ruined=True), *commandos('S11')[1],
               CAT('S11', ry=-15, clips=[[0, 'sit']], expr=[[0, 'sleepy']], ear=[r(CUT11 + 0.3), r(CUT11 + 0.62)], blinks=[r(CUT11 + 0.8)]),
               P('agrafeuse11', 'stapleGun', on={'actor': 'huissier', 'hand': 'R', 'offset': [0.0, -0.05, 0.03]}, opts={'clacks': STAP11})],
        cams=[C11a, C11b])
for t_ in STAP11: st.cue('clack', 'S11', t_, 0.5)
st.cue('sfx:paper', 'S11', 0.3, 0.25)

# 12: tried at the foot of the tree, in absentia. Low and wide over the empty dock: the judge's bench in the rubble at the foot of the tree, the bowl
#     on it with its big red SCELLÉ tag; the bailiff reads the charge at the left; the judge behind the bench; high above him the cat's tail dangles
#     from the top branch, right over his wig
D12 = st.dur('S12')
BENCH = tw(0.45, 0, 1.3); JUGE = tw(0.43, 0, 0.65); BH = 1.3   # (review 1) the bench raised and the judge right under the tail
BOWL12 = add(BENCH, [0.6, BH + 0.035, 0.12])
HUIS12 = tw(-0.05, 0, 3.4); RYH12 = 25   # (review 2) at the right, his head in clear sky
JUGE12 = add(JUGE, [0, 0.4, 0]); BOWL12S = add(BENCH, [-0.55, BH + 0.035, 0.12])   # (review 2) the judge on a step, his torso above the bench; the bowl at the left end
DOCK = tw(-0.1, 0, 5.8)
C12 = cam(0.0, [0.8, 1.5, 21.5], [0.78, 1.5, 21.3], [0.4, 2.3, 14.8], [0.4, 2.35, 14.8], lens=46)   # (review 1) on the wig, the long tail swinging down into the gap above it
TAIL = tw(0.43, 3.0, 0.0)
chk('S12', C12['from'], C12['lookAt'], 46, {'jugeFace': add(JUGE12, [0, 2.05, 0]), 'wigTop': add(JUGE12, [0, 2.45, 0]), 'tail': TAIL, 'cat': add(SEAT, [0, 0.25, 0]), 'bowlTag': add(BOWL12, [0.2, 0.2, 0.25]), 'huisFace': add(HUIS12, [0, 2.05, 0]), 'dockFront': add(DOCK, [0, 1.0, 0.7])})
JF = {'lid': 0.45, 'mouth': 'line', 'brow': -0.3}
st.shot('S12', SET, setOpts=SETO, actors=[
        act('juge', JUGE12, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': R5(add(BENCH, [-0.3, BH + 0.08, -0.15])), 'L': R5(add(BENCH, [0.3, BH + 0.08, -0.15]))}, 'hands': {'R': 'rest', 'L': 'rest'}, 'face': JF}, toonDur=0.0), *blink(0.6, JF),
            k(0.75, look=add(JUGE12, [0.0, 3.3, 0.6]), lookDur=0.08), k(1.0, look='camera', lookDur=0.1), k(1.55, look=add(JUGE12, [0.0, 3.3, 0.6]), lookDur=0.08), k(1.85, look='camera', lookDur=0.1), *blink(2.15, JF)]),   # (review 2) his eyes flick up to the tail
        act('huissier', HUIS12, RYH12, 'stand', 'neutral', keys=[k(0.0, look=off(HUIS12, RYH12, 0.45, 0.0, 1.55)),
            *[k(r(0.4 * i), toon={'reach': {'R': R5(off(HUIS12, RYH12, 0.45, 0.17, 1.55 - 0.03 * (i % 2)), 1, 0.05), 'L': R5(off(HUIS12, RYH12, 0.45, -0.17, 1.55 - 0.03 * (i % 2)), 1, 0.05)}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'bend': {'neck': [0.25 + 0.08 * (i % 2), 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0 if i == 0 else 0.35) for i in range(7)],
            *st.talk('L12', 'S12', 'neutral'), k(1.95, look='camera', lookDur=0.15)]),   # (review 1) he reads the sheet, head bobbing
        *commandos('S12', orders=False, skip=('cdo2', 'cdo3', 'cdo4'))[0]],   # (review 2) only the top one: clear space round the bailiff and the judge
        props=[TREE('S12', twig=False, sag=[[0, 0.1]], summons={'text': 'CONVOCATION'}), ROW('S12', ruined=True), *commandos('S12', skip=('cdo2', 'cdo3', 'cdo4'))[1],
               CAT('S12', ry=90, clips=[[0, 'sleep']], tail='dangle', tailS=10.5, tailW=2.4, tailFur=True, swing=0.55, swingF=1.7),
               P('estrade12', 'dais', pos=add(JUGE, [0, 0, -0.05]), opts={'w': 1.1, 'h': 0.4, 'd': 0.7}),
               P('banc12', 'fieldBench', pos=BENCH, opts={'w': 2.2, 'h': BH}), P('bol12', 'kibbleBowl', pos=add(BOWL12, [0.15, 0, 0]), ry=-5, opts={'tag': True, 'tagS': 1.35}),
               P('feuille12', 'stapledSheet', on={'actor': 'huissier', 'hand': 'R', 'offset': [-0.12, 0.12, 0.06], 'face': 'camera'}, opts={'text': 'ACTE', 'w': 0.42, 'h': 0.56}),
               P('marteau12', 'gavel', pos=add(BENCH, [-0.6, BH + 0.04, 0.1]), rot=[0, 0, PI / 2]), P('socle12', 'soundBlock', pos=add(BENCH, [-0.35, BH + 0.04, 0.15])),
               *[P(f'gravats12{i}', 'rubbleHeap', pos=tw(x, 0, z), ry=a, opts={'r': 1.3, 'h': 0.55}) for i, (x, z, a) in enumerate([(-2.6, 1.0, 20), (3.4, 1.4, 70), (2.6, 4.6, 35)])]],
        cams=[C12])
st.cue('sfx:paper', 'S12', 0.1, 0.25)

# 13: the hostage asked to stay with the cat. Close at the top branch: the leafy shoot rises and curls slowly round the sleeping cat like a
#     protective arm; in the foreground at the left, only the clerk's arm holding a microphone up to the bark
D13 = st.dur('S13')
C13 = cam(0.0, [-0.75, 5.95, 16.9], [-0.7, 5.95, 16.75], [0.75, 5.85, 14.0], [0.75, 5.85, 14.0], lens=42)
MIC = tw(-0.12, 5.0, 0.95)
chk('S13', C13['from'], C13['lookAt'], 42, {'cat': add(SEAT, [0, 0.25, 0]), 'curlTip': tw(1.3, 5.9), 'curlTop': tw(0.75, 6.65), 'micHead': add(MIC, [0.15, 0.75, -0.25]), 'armFoot': MIC})
st.shot('S13', SET, setOpts=SETO, actors=[],
        props=[TREE('S13', twig=False, sag=[[0, 0.1]], curl=[[0, 0.0], [0.35, 0.4], [1.0, 0.75], [1.6, 1.0]]), ROW('S13', ruined=True, noSmoke=True),
               CAT('S13', ry=-25, clips=[[0, 'sleep']]),
               P('greffe13', 'clerkArm', pos=MIC, ry=150, opts={'lean': 0.75, 'len': 0.55, 'push': [[0, 0.0], [0.4, 0.08]], 'micS': 1.6})],
        cams=[C13])
st.cue('sfx:stretch', 'S13', 0.3, 0.2); st.cue('sfx:stretch', 'S13', 1.1, 0.18)

# 14: sentenced to come down. Low and close on the judge, standing on his step at the right end of the bench: he winds the gavel high against the
#     sky (stretched tall), smashes it on the block (a squash, the bench and bowl jump), then thrusts his left arm straight down beside the bench end,
#     finger to the ground, held, his head turned up to the cat; cut in on the cat at the top: a huge yawn (CONDAMNÉ)
D14 = st.dur('S14'); HIT14 = 0.26; CUT14 = 0.72; PT14 = 0.38
JUGE14 = tw(1.4, 0.4, 0.65)
C14a = cam(0.0, [2.0, 1.0, 19.4], [1.98, 1.01, 19.3], [1.35, 2.0, 14.8], [1.35, 2.05, 14.8], lens=50)   # (review 2) lower and closer, the wind-up against the sky
C14b = cam(CUT14, add(HEADC, [-0.15, 0.3, 1.3]), add(HEADC, [-0.14, 0.29, 1.22]), add(HEADC, [0.05, -0.08, 0.0]), add(HEADC, [0.05, -0.08, 0.0]), lens=54)
BLOCK14 = add(BENCH, [0.72, BH + 0.04, 0.12])
GUP14 = add(JUGE14, [-0.32, 2.75, -0.05])
POINT14 = add(JUGE14, [0.62, 1.15, 0.2])   # (review 2) the arm out from the robe, the finger against the lawn
chk('S14a', C14a['from'], C14a['lookAt'], 50, {'jugeFace': add(JUGE14, [0, 2.05, 0]), 'wig': add(JUGE14, [0, 2.45, 0]), 'gavelUp': GUP14, 'block': BLOCK14, 'point': POINT14, 'pointTip': add(POINT14, [0, -0.25, 0]), 'tag': add(BOWL12S, [0.05, 0.2, 0.25]), 'benchEnd': add(BENCH, [1.1, BH, 0.4])})
chk('S14b', C14b['from'], C14b['lookAt'], 54, {'catHead': HEADC, 'seat': SEAT, 'ear': add(HEADC, [0.1, 0.25, 0])})
JA = {'lid': 0.15, 'mouth': 'clench', 'brow': -0.8}
JP = {'lid': 0.1, 'mouth': 'line', 'brow': -0.9}
st.shot('S14', SET, setOpts=SETO, actors=[
        act('juge', JUGE14, 0, 'stand', 'angry', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': R5(add(BLOCK14, [0.0, 0.5, -0.05]), 1, 0.06), 'L': R5(add(JUGE14, [0.3, 1.0, 0.2]))}, 'hands': {'R': 'grip', 'L': 'rest'}, 'face': JA}, toonDur=0.0),
            k(0.02, toon={'reach': {'R': R5(GUP14, 1, 0.08), 'L': R5(add(JUGE14, [0.3, 1.0, 0.2]))}, 'hands': {'R': 'grip', 'L': 'rest'}, 'sq': [0.88, 1.16, 0.88], 'bend': {'spine': [-0.15, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'mouth': 'O', 'brow': -0.9}, 'auto': 0}, toonDur=0.15, toonEase='out'),
            k(r(HIT14 - 0.05), toon={'reach': {'R': R5(add(BLOCK14, [0.0, 0.12, 0.0]), 1, 0.08), 'L': R5(add(JUGE14, [0.3, 1.0, 0.2]))}, 'hands': {'R': 'grip', 'L': 'rest'}, 'sq': [1.16, 0.85, 1.16], 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.9}, 'auto': 0}, toonDur=0.05, toonEase='in'),
            k(r(PT14 - 0.04), toon={'reach': {'R': R5(add(BLOCK14, [0.0, 0.14, 0.0]), 1, 0.08), 'L': R5(POINT14, 1, 0.08)}, 'hands': {'R': 'grip', 'L': 'point'}, 'sq': [0.97, 1.05, 0.97], 'face': JP, 'auto': 0}, toonDur=0.08, toonEase='out'),   # (review 2) a vertical arm, finger down beside the bench end
            k(r(PT14 + 0.1), toon={'reach': {'R': R5(add(BLOCK14, [0.0, 0.14, 0.0]), 1, 0.08), 'L': R5(add(POINT14, [0.0, -0.04, 0.0]), 1, 0.08)}, 'hands': {'R': 'grip', 'L': 'point'}, 'sq': [1, 1, 1], 'face': JP}, toonDur=0.1),
            k(r(PT14 - 0.02), look=add(JUGE14, [0.0, 4.0, 0.9]), lookDur=0.1)]),
        *commandos('S14', skip=('cdo4',))[0]],
        props=[TREE('S14', twig=False, sag=[[0, 0.1]], curl=[[0, 1.0]], summons={'text': 'CONVOCATION'}), ROW('S14', ruined=True), *commandos('S14', skip=('cdo4',))[1],
               CAT('S14', ry=-12, clips=[[0, 'sit']], expr=[[0, 'sleepy']], yawn=[[r(CUT14 + 0.06), r(D14 - 0.04)]]),
               P('estrade14', 'dais', pos=add(JUGE14, [0, -0.4, -0.05]), opts={'w': 1.0, 'h': 0.4, 'd': 0.7}),
               P('banc14', 'fieldBench', pos=BENCH, opts={'w': 2.2, 'h': BH}, keys=[k(HIT14, to=add(BENCH, [0, 0.06, 0]), dur=0.04), k(r(HIT14 + 0.05), to=BENCH, dur=0.08)]),
               P('bol14', 'kibbleBowl', pos=BOWL12S, ry=-5, opts={'tag': True, 'tagS': 1.35}, keys=[k(HIT14, to=add(BOWL12S, [0, 0.12, 0]), dur=0.05), k(r(HIT14 + 0.06), to=BOWL12S, dur=0.1, ease='in')]),
               P('marteau14', 'gavel', on={'actor': 'juge', 'hand': 'R'}, scale=1.5), P('socle14', 'soundBlock', pos=BLOCK14)],
        fx=[{'type': 'shake', 'at': HIT14, 'dur': 0.15, 'amount': 0.02}],
        cams=[C14a, C14b])
st.card('S14', 'CONDAMNÉ', at=0.28)
st.cue('sfx:gavel', 'S14', HIT14, 0.6); st.cue('sfx:stretch', 'S14', r(CUT14 + 0.1), 0.2)

# 15: escorted by the soldiers. Low at the foot of the tree looking up at the dangling boots: the bailiff on tiptoe staple-guns an ESCORTE order onto
#     one boot, then the next; the second commando lets go with one hand to salute and nearly slips (a drop and a grab)
D15 = st.dur('S15'); ST15 = {'cdo2': 0.15, 'cdo3': 0.45}; SAL15 = 0.68; SLIP15 = 0.9
C15 = cam(0.0, [-0.2, 1.0, 18.9], [-0.25, 1.02, 18.7], [-1.0, 3.05, 14.2], [-1.0, 3.1, 14.2], lens=54)
HU15 = tw(-0.6, 0, 1.25); RYH15 = -15
r2, r3 = hang_root(*HANG['cdo2'][:2]), hang_root(*HANG['cdo3'][:2])
chk('S15', C15['from'], C15['lookAt'], 54, {'huisFace': add(HU15, [0, 2.05, 0]), 'cdo2Face': add(r2, [0, 2.0, 0]), 'cdo3Face': add(r3, [0, 2.0, 0]), 'boot2': add(r2, [0, 0.15, 0.1]), 'boot3': add(r3, [0, 0.15, 0.1]), 'cat': HEADC})
B2, B3 = add(r2, [-0.1, 0.2, 0.2]), add(r3, [-0.1, 0.2, 0.2])
slip = [k(SLIP15, to=add(r3, [0, -0.6, 0]), dur=0.07, ease='in', glide=True, face='keep'), k(r(SLIP15 + 0.27), to=add(r3, [0, 0.12, 0]), dur=0.06, ease='out', glide=True, face='keep'),   # (review 1) a long hang on one stretched arm, then a snap back that overshoots
        k(r(SLIP15 + 0.36), to=r3, dur=0.1, ease='inOut', glide=True, face='keep'),
        k(SLIP15, toon={'face': {'lid': 0.0, 'pop': 0.5, 'mouth': 'O', 'brow': 0.9, 'sweat': 1.0}}, toonDur=0.04, keepPose=True)]
acts15, props15 = commandos('S15', orders={'cdo2': ST15['cdo2'], 'cdo3': ST15['cdo3'], 'cdo1': -1, 'cdo4': -1}, look=[-0.8, 1.6, 15.6], salute=('cdo3', SAL15), extra={'cdo3': slip})
st.shot('S15', SET, setOpts=SETO, actors=[
        act('huissier', HU15, RYH15, 'stand', 'unimpressed', keys=[k(0.0, look=B2),
            k(0.0, toon={'reach': {'R': R5(B2, 1, 0.05)}, 'hands': {'R': 'grip'}, 'sq': [0.95, 1.08, 0.95], 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.0),
            k(0.3, look=B3, lookDur=0.12), k(0.3, toon={'reach': {'R': R5(B3, 1, 0.05)}, 'hands': {'R': 'grip'}, 'sq': [0.93, 1.1, 0.93]}, toonDur=0.18),
            k(0.85, toon={'reach': {'R': R5(off(HU15, RYH15, 0.3, 0.3, 1.1))}, 'hands': {'R': 'grip'}, 'sq': [1, 1, 1]}, toonDur=0.25), k(SLIP15, look=add(r3, [0, 2.0, 0]), lookDur=0.1)]),
        *acts15],
        props=[TREE('S15', twig=False, sag=[[0, 0.1]], curl=[[0, 1.0]], summons={'text': 'CONVOCATION'}), ROW('S15', ruined=True), *props15,
               CAT('S15', ry=-10, clips=[[0, 'sleep']]),
               P('agrafeuse15', 'stapleGun', on={'actor': 'huissier', 'hand': 'R', 'offset': [0.0, -0.05, 0.03]}, opts={'clacks': [ST15['cdo2'], ST15['cdo3']]})],
        cams=[C15])
for t_ in ST15.values(): st.cue('clack', 'S15', t_, 0.5)
st.cue('sfx:squeak', 'S15', SLIP15, 0.3)

# 16: that night the cat came down to eat the seized evidence. Night, beside the trunk: the cat walks head first down the bark past the clinging
#     commandos and their orders, their eyes following it; then at the bench: it hops on and crunches the croquettes in the sealed bowl
D16 = st.dur('S16'); CUT16 = r(st.at('S16', 'L16', 6) - 0.25); HOP16 = r(CUT16 + 0.05)
DOWN = axes_euler([1, 0, 0], [0, 0, 1], [0, -1, 0])
TRUNKF = 0.27
CATD0, CATD1 = tw(0.0, 5.0, TRUNKF), tw(0.0, 0.7, TRUNKF + 0.08)
C16a = cam(0.0, [2.7, 3.1, 19.6], [2.6, 2.9, 19.4], [-0.1, 3.3, 14.0], [-0.1, 2.6, 14.0], lens=50)
C16b = cam(CUT16, [2.15, 1.95, 18.1], [2.05, 1.93, 17.95], [0.75, 1.55, 15.35], [0.75, 1.55, 15.35], lens=44)
BOWL16 = BOWL12
CATB = add(BOWL16, [-0.52, 0.0, 0.02])
chk('S16a', C16a['from'], C16a['lookAt'], 50, {'catTop': CATD0, 'catLow': CATD1, 'cdo2': add(r2, [0, 2.0, 0]), 'cdo4': add(hang_root(*HANG['cdo4'][:2]), [0, 2.0, 0]), 'boot2': add(r2, [0, 0.15, 0.1])})
chk('S16b', C16b['from'], C16b['lookAt'], 44, {'bowl': BOWL16, 'tag': add(BOWL16, [0.05, 0.2, 0.25]), 'cat': add(CATB, [0, 0.5, 0]), 'benchFoot': add(BENCH, [0, 0, 0.4])})
# (review 2) a real night: deep navy sky, a moon, a low warm key on the cat and the bowl (a lamp off frame), a faint cool fill, haze to navy
NIGHTSET = {**SETO, 'sky': ['#081028', '#1A2850'], 'lawn': '#2F4A30', 'roadColor': '#383C46'}
NIGHTLOOK = {'sun': 0.62, 'sunColor': '#FFB066', 'sunDir': [0.75, 0.42, 0.85], 'fill': 0.38, 'exposure': 0.95, 'sunDisc': False, 'shafts': False, 'hazeColor': '#141C38', 'warm': 0.2}
acts16, props16 = commandos('S16', orders=True, look=CATD1)
st.shot('S16', SET, setOpts=NIGHTSET, look=NIGHTLOOK, actors=acts16,
        props=[TREE('S16', twig=False, sag=[[0, 0.1]], curl=[[0, 1.0]], summons={'text': 'CONVOCATION'}), ROW('S16', ruined=True), *props16, P('lune16', 'moon', pos=[-10.0, 8.0, -14.0], opts={'radius': 1.5}),
               P('banc16', 'fieldBench', pos=BENCH, opts={'w': 2.2, 'h': BH}), P('bol16', 'kibbleBowl', pos=BOWL16, ry=80, opts={'tag': True, 'tagS': 1.35, 'eat': [r(HOP16 + 0.45), r(D16 - 0.1)]}),   # the tag to the side: the head dips in view
               CAT('S16', pos=CATD0, ry=DOWN[1], keys=[k(0.0, to=CATD1, dur=r(CUT16 - 0.05), ease='linear'), k(HOP16, to=add(CATB, [0, 0.0, 0]), dur=0.3, ease='out'),
                   k(HOP16, rotTo=[0, PI / 2 - 0.3, 0], dur=0.08)], rot=[DOWN[0], 0, DOWN[2]],
                   clips=[[0, 'walk'], [HOP16, 'run'], [r(HOP16 + 0.32), 'eat']], expr=[[0, 'neutral'], [r(HOP16 + 0.4), 'closed']], crunch=[[r(HOP16 + 0.4), D16]])],
        cams=[C16a, C16b])
st.cue('sfx:crickets', 'S16', 0.0, 0.25); st.cue('sfx:scratch', 'S16', 0.2, 0.15); st.cue('sfx:boing', 'S16', HOP16, 0.15)
for j in range(4): st.cue('sfx:crunch', 'S16', r(HOP16 + 0.45 + 0.28 * j), 0.35)

# 17: then it went back up to bed. Held dawn wide from the lawn: the cat climbs the trunk past the commandos (one still saluting, the orders
#     flapping on their boots), steps onto the top branch and curls up asleep inside the curled shoot; the empty sealed bowl on the bench below
D17 = st.dur('S17'); UP17 = 1.2
UPR = axes_euler([-1, 0, 0], [0, 0, 1], [0, 1, 0])
CATU0, CATU1 = tw(0.0, 2.2, TRUNKF + 0.06), tw(0.0, 5.0, TRUNKF)
C17 = cam(0.0, [1.25, 1.45, 23.5], [1.2, 1.45, 23.2], [0.65, 2.75, 14.0], [0.65, 2.8, 14.0], lens=54)   # (review 2) at bowl height: the bowl at 65 %, the shoot near the top   # (review 1) closer: the climb, the flop into the shoot, a saluting commando, the empty bowl
chk('S17', C17['from'], C17['lookAt'], 54, {'catLow': CATU0, 'catHigh': CATU1, 'seat': add(SEAT, [0, 0.3, 0]), 'bowl': BOWL16, 'cdo3': add(r3, [0, 2.0, 0]), 'treeTop': tw(-1.0, 7.6, -0.5), 'bench': add(BENCH, [0, 1.2, 0])})
WOB17 = [k(r(0.3 + 0.35 * i), toon={'sq': [1 + 0.04 * (-1) ** i, 1 - 0.05 * (-1) ** i, 1], 'bend': {'spine': [0, 0.12 * (-1) ** i, 0, 1, None]}}, toonDur=0.3, keepPose=True) for i in range(7)]   # the saluting one wobbles
acts17, props17 = commandos('S17', orders=True, salute=('cdo3', -1.0), look=CATU1, extra={'cdo3': WOB17}, salute1=True)
DAWNSET = {**SETO, 'sky': ['#C98AA8', '#FFC48A']}   # (review 2) a warm dawn: pink-violet high, orange low, a low sun from the side, long shadows
DAWNLOOK = {'sunColor': '#FFAA70', 'sunDir': [0.95, 0.18, 0.3], 'elevation': 12, 'warm': 0.5, 'hazeColor': '#F2B892', 'exposure': 1.04}
st.shot('S17', SET, setOpts=DAWNSET, look=DAWNLOOK, actors=acts17,
        props=[TREE('S17', twig=False, sag=[[0, 0.1]], curl=[[0, 1.0]], summons={'text': 'CONVOCATION'}), ROW('S17', ruined=True), *props17,
               P('banc17', 'fieldBench', pos=BENCH, opts={'w': 2.2, 'h': BH}), P('bol17', 'kibbleBowl', pos=BOWL16, ry=90, rot=[0.6, PI / 2, 0], opts={'tag': True, 'tagS': 1.35, 'empty': True}),   # (review 2) tilted to the lens, the empty inside showing, the tag beside it
               CAT('S17', pos=CATU0, ry=UPR[1], rot=[UPR[0], 0, UPR[2]], keys=[k(0.0, to=CATU1, dur=UP17, ease='linear'), k(UP17, to=SEAT, dur=0.25, ease='out'), k(UP17, rotTo=[0, math.radians(200), 0], dur=0.3), k(r(UP17 + 0.35), rotTo=[0, math.radians(-25), 0], dur=0.25)],
                   clips=[[0, 'walk'], [UP17, 'walk'], [r(UP17 + 0.62), 'sleep']], duck=[[r(UP17 + 0.6), 0.0], [r(UP17 + 0.66), 1.0], [r(UP17 + 0.8), 0.25]], flat=0.4, duckBlend=0.08)],   # (review 1) it turns round on the branch and flops asleep in the shoot
        cams=[C17])
st.cue('sfx:scratch', 'S17', 0.1, 0.15); st.cue('sfx:scratch', 'S17', 0.7, 0.15); st.cue('sfx:bell', 'S17', r(UP17 + 0.5), 0.0)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
CDO = {'preset': 'swat', 'outfit': 'suit', 'hat': 'none', 'suit': '#2C3A4E', 'pants': '#283446', 'shirt': '#2C3A4E', 'lapel': '#202A38', 'tie': '#202A38', 'cuff': '#2C3A4E', 'gloves': '#14161A', 'glasses': False,
       'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
st.write("Le chat", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'flic': {'preset': 'cop', 'seed': 870, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'nego': {'preset': 'commissaire', 'seed': 871, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'cdo{j}': {**CDO, 'seed': 872 + j} for j in range(1, 5)},
    'porte': {'preset': 'politique', 'seed': 877, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'hairColor': '#BDBDBD', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'medic1': {'preset': 'doctor', 'seed': 878, 'suit': '#F1F1EC', 'lapel': '#DCDCD4', 'cuff': '#F1F1EC', 'pants': '#E6E6DE', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'medic2': {'preset': 'doctor', 'seed': 879, 'suit': '#F1F1EC', 'lapel': '#DCDCD4', 'cuff': '#F1F1EC', 'pants': '#E6E6DE', 'glasses': False, 'facial': 'mustache', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'crs1': {'preset': 'boss', 'outfit': 'suit', 'facial': 'none', 'seed': 880, 'suit': '#4C5058', 'pants': '#3E4148', 'shirt': '#4C5058', 'lapel': '#3E4148', 'tie': '#2E3036', 'cuff': '#4C5058', 'hat': 'none', 'glasses': False, 'gloves': '#1A1B1E', 'build': {'width': 1.12, 'headWidth': 1.2}, 'toon': EX},
    'crs2': {'preset': 'boss', 'outfit': 'suit', 'facial': 'mustache', 'seed': 881, 'suit': '#4C5058', 'pants': '#3E4148', 'shirt': '#4C5058', 'lapel': '#3E4148', 'tie': '#2E3036', 'cuff': '#4C5058', 'hat': 'none', 'glasses': False, 'gloves': '#1A1B1E', 'build': {'width': 1.12, 'headWidth': 1.2}, 'toon': EX},
    'officier': {'preset': 'cop2', 'seed': 882, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'huissier': {'preset': 'boss', 'seed': 883, 'suit': '#5B4636', 'pants': '#4A392C', 'tie': '#C9CDD3', 'lapel': '#45342A', 'hair': 'receding', 'facial': 'none', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'juge': {'preset': 'judge', 'seed': 884, 'facial': 'stubble', 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
})
