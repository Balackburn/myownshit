#!/usr/bin/env python3
"""La bosse (story 56, cycle 18 of the cartoon staging): this man hit his head. The bump never stopped growing. The doctor measured it: three metres.
The land registry classed it as a hill. On Sundays there are hikers. In winter, a ski resort. Yesterday the bump went down. The skiers fell from a
height. The resort wants him to pay for their passes.
Staging: he walks under a low beam marked ATTENTION À LA TÊTE: BONG, his head driven down into his shoulders, stars; the bump pops out of his skull
in three throbs, his eyes rolling up to it; it grows in a time lapse while the days flick by, his neck sinking under its weight; in his front garden
the doctor, up a ladder, lays a tape measure down the ball of skin: 3,00 M, and the tape snaps back into his face; a surveyor sights it through
his level; a blue enamel plate COLLINE drops onto the top and grass spreads down from it; on Sunday hikers climb a path round the hill on his head;
in winter skiers come down it and a chair lift goes up; a skier jumps off the rim past his eyes; PSCHHH: the bump goes down like a balloon, his
neck springing back up; the skiers hang in the air where the slope was, look down, look at us, and fall; they land around him, one on his head;
the resort's man hands him a bill that unrolls down to the snow and away.
Natural look; (pass 2) the doorway in a wall, the hook that flies to a nose, the bump that sags as it empties; cycle 18 tools: the tip and the pin set before the guided hands (held hands stay on their points), the bump that grows into a hill
(props_bosse.js: skullBump, miniFigure, billScroll, lowBeam, theodolite)."""
from story_kit import *
import math

st = Story('bosse', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 2), ('S04', 'L03', 0), ('S05', 'L03', 4), ('S06', 'L04', 0), ('S07', 'L04', 4),
         ('S08', 'L05', 0), ('S09', 'L05', 6), ('S10', 'L06', 0), ('S11', 'L06', 2), ('S12', 'L07', 0), ('S13', 'L07', 4), ('S14', 'L08', 0),
         ('S15', 'L08', 4), ('S16', 'L09', 0), ('S17', 'L09', 5)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)

LOOKI = {'warm': 0.45}                                                  # interiors: the whites stay white
SNOWY = {'grass': '#EEF2F6', 'sky': ['#A7BED0', '#E6EDF3'], 'seed': 31, 'treeColors': ['#E9EEF2', '#F6F8FA', '#DCE3E8']}   # (pass 4) snow-laden trees: leafy summer trees stood in the winter field
LOOKS = {'warm': 0.45}                                                  # (pass 4) the snow shots: the whites stay white (from S11 they drifted to peach)
SUMMER = {'grass': '#A9C08E', 'sky': ['#8FC3E8', '#E2F1FA']}   # (pass 2) a paler meadow under a light sky: the hill's grass stands out (they matched, 92 and 93 degrees)
TOP = 2.13                                                              # the top of his skull, standing (the head joint at the chin, 0.5 below)
HEAD = lambda: {'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.5, 0.02]}   # the bump sits on the crown
BALL = 1.4; RB = 0.11; BALLC = r(TOP + math.sqrt(BALL * BALL - RB * RB)); BALLTOP = r(BALLC + BALL)   # the ball of skin at three metres, its centre, its top
HILL = 2.3; HR = 0.7; HILLTOP = r(TOP + HR * HILL)                      # the hill: base radius, height ratio, its summit
BURST = lambda pid, pos, at_, text, w=0.45: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
DEADPAN = {'lid': 0.45}
SUNK = lambda s_, extra=None: {'bend': {'neck': [0.0, 0, 0, r(s_), None]}, **(extra or {})}   # the neck sunk to s_ of its length under the weight

# 1: the hook. His living room: he walks briskly at us through a doorway with a low beam marked ATTENTION À LA TÊTE: BONG, his forehead on it, his
#    head driven down into his shoulders, his body squashed, stars; he staggers back a step, the head popping back up, cross-eyed
D1 = st.dur('S01'); HIT1 = round(st.at('S01', 'L01', 3) + 0.02, 3)   # « cogné »
BEAMH = 1.86
# (final pass) he walks AT us through the doorway, seen from above and three-quarters: his forehead meets the beam's edge in view, the squash held
# five frames with a shiver, then he ducks under it and staggers toward us, the head popping back up cross-eyed (from behind, the review saw no face
# and a 180-degree flip; pass 3 at eye level hid the contact behind the beam)
ME1 = [0.0, 0, -1.5]; HITZ = -0.3
st.shot('S01', 'livingRoom', setOpts={'carpet': False, 'picture': False, 'tv': False}, look=LOOKI, actors=[
        act('mec', ME1, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEADPAN}, toonDur=0.0),
            k(0.0, to=[0.0, 0, HITZ], dur=HIT1, clip='walk', then='stand', ease='linear', face='keep'),
            k(HIT1, toon={'scl': {'head': [1.3, 0.66, 1.3]}, 'bend': {'neck': [0.25, 0, 0, 0.35, None]}, 'sq': [1.12, 0.86, 1.12], 'face': {'lid': 0.2, 'cross': 0.9, 'brow': 0.9, 'mouth': 'O', 'stars': 1.0}}, toonDur=0.033, toonEase='out'),   # BONG
            *[k(round(HIT1 + 0.04 + 0.035 * i, 3), toon={'scl': {'head': [round(1.28 - 0.02 * (i % 2), 3), round(0.68 + 0.02 * (i % 2), 3), 1.28]}, 'bend': {'neck': [0.25, 0, 0, 0.36, None]}, 'sq': [1.1, 0.88, 1.1], 'lay': [0.0, (0.02 if i % 2 else -0.02)], 'face': {'lid': 0.2, 'cross': 0.9, 'brow': 0.9, 'mouth': 'O', 'stars': 1.0}}, toonDur=0.03) for i in range(4)],   # held five frames, shivering
            k(round(HIT1 + 0.17, 3), to=[0.0, 0, 0.55], dur=0.22, ease='out', face='keep'),   # under the beam and toward us...
            k(round(HIT1 + 0.18, 3), toon={'scl': {'head': [0.92, 1.12, 0.92]}, 'bend': {'neck': [-0.08, 0, 0, 1.14, None]}, 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.0, 'cross': 1.0, 'stars': 1.0}}, toonDur=0.06, toonEase='outBack'),   # ...the head pops back up...
            k(round(HIT1 + 0.25, 3), toon={'bend': {'neck': [0.0, 0, 0, 1.0, None]}, 'lay': [0.05, 0.04], 'face': {'lid': 0.0, 'cross': 1.0, 'stars': 1.0, 'eyeScale': 1.2}}, toonDur=0.06)])],   # ...cross-eyed at us
        props=[P('beam1', 'lowBeam', pos=[0.0, 0, 0.0], opts={'h': BEAMH, 'w': 1.3, 'shake': [[HIT1, 0.05]], 'wall': [1.8, 2.7, '#E9DCC6']}), BURST('bong1', [0.78, 2.25, 0.25], HIT1, 'BONG !', 0.46)],
        cams=[FC(0.0, [1.1, 2.35, 3.2], [[0.0, 2.4, HITZ], [0.0, 0.0, 0.55], [-0.75, 2.15, 0.0], [0.75, 2.15, 0.0], [0.78, 2.5, 0.25], [0.0, 2.3, 0.55]], top=0.1, bottom=0.78, drift=(0.0, -0.05, -0.08))])
st.cue('sfx:bonk', 'S01', HIT1, 0.5); st.cue('sfx:boing', 'S01', round(HIT1 + 0.1, 3), 0.25)

# 2: the bump. Close: the head springs up and the bump pops out of his skull in three throbs, POC, POC, POC, each bigger; his eyes roll up to it
D2 = st.dur('S02'); POPS = (0.16, 0.42, 0.68)
ME2 = [0.0, 0, -0.75]
GROW2 = [[0.0, 0.0001], [0.1, 0.0001]]
for i_, t_ in enumerate(POPS):
    big = 0.05 * (i_ + 1) + 0.01 * i_
    GROW2 += [[t_, r(big * 0.82)], [r(t_ + 0.05), r(big * 1.12)], [r(t_ + 0.12), r(big)]]   # each pop overshoots and settles
st.shot('S02', 'livingRoom', setOpts={'carpet': False, 'picture': False, 'tv': False}, look=LOOKI, actors=[
        act('mec', ME2, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'lay': [0.05, 0.04], 'face': {'lid': 0.2, 'cross': 0.7, 'stars': 1.0}}, toonDur=0.0),
            *[x for t_ in POPS for x in (k(t_, toon={'scl': {'head': [1.06, 0.93, 1.06]}, 'face': {'lid': 0.0, 'eyeScale': 1.35, 'gy': -0.6, 'cross': 0.3, 'brow': 0.9, 'stars': 0.7}}, toonDur=0.033, toonEase='out'),   # (pass 4) wide from the first POC
                                         k(round(t_ + 0.1, 3), toon={'face': {'lid': 0.05, 'eyeScale': 1.3, 'gy': -0.6, 'cross': 0.3, 'brow': 0.8, 'stars': 0.6}}, toonDur=0.08))],   # each POC jolts his head; his eyes roll up to it
            k(round(POPS[2] + 0.14, 3), toon={'face': {'lid': 0.0, 'eyeScale': 1.35, 'gy': -0.65, 'brow': 0.8, 'stars': 0.0}}, toonDur=0.06, toonEase='out'),   # (pass 2) the eyes wide, rolled up to it, held (half-lidded they never showed)
            k(round(D2 - 0.06, 3), toon={'face': {'lid': 0.05, 'eyeScale': 1.3, 'gy': -0.6, 'brow': 0.6}}, toonDur=0.06)])],
        props=[P('b2', 'skullBump', on=HEAD(), opts={'grow': GROW2, 'red': 0.12}),
               *[BURST(f'poc2{i_}', [[-0.36, 2.32, -0.4], [0.36, 2.46, -0.4], [-0.3, 2.6, -0.4]][i_], t_, 'POC !', 0.26) for i_, t_ in enumerate(POPS)]],   # (stills v1) inside the frame
        cams=[FC(0.0, [0.25, 1.85, 0.9], [[0.0, 2.75, ME2[2]], [0.0, 1.45, ME2[2]], [-0.55, 2.2, ME2[2]], [0.55, 2.2, ME2[2]]], top=0.12, bottom=0.7, drift=(0.0, 0.0, -0.08))])
for t_ in POPS: st.cue('pop', 'S02', t_, 0.4)

# 3: it never stopped growing. Time lapse: he sits on a chair in his living room, the days flick by (the light goes off and on), the bump swells
#    with every heartbeat and grows to a ball as big as his chest, his neck sinking under its weight; deadpan, he blinks
D3 = st.dur('S03')
ME3 = [0.0, 0, -1.6]
st.shot('S03', 'livingRoom', setOpts={'carpet': False, 'picture': False, 'tv': False, 'sofa': False}, look=LOOKI,
        dark=[[0.12, 0.7, 0.05], [0.32, 0.0, 0.05], [0.55, 0.7, 0.05], [0.75, 0.0, 0.05], [0.98, 0.7, 0.05], [1.18, 0.0, 0.05]], actors=[
        act('mec', [ME3[0], 0, r(ME3[2] + 0.05)], 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(1.0, {'face': DEADPAN}), toonDur=0.0),
            k(0.4, toon=SUNK(0.85, {'bend': {'neck': [0.0, 0, 0, 0.85, None], 'spine': [0.1, 0, 0, 1, None]}, 'face': DEADPAN}), toonDur=0.35, toonEase='inOut'),
            k(0.62, toon=SUNK(0.8, {'bend': {'neck': [0.0, 0, 0, 0.8, None], 'spine': [0.12, 0, 0, 1, None]}, 'face': {'lid': 1.0}}), toonDur=0.05),
            k(0.72, toon=SUNK(0.78, {'bend': {'neck': [0.0, 0, 0, 0.78, None], 'spine': [0.14, 0, 0, 1, None]}, 'face': DEADPAN}), toonDur=0.08),   # a blink
            k(1.1, toon=SUNK(0.6, {'bend': {'neck': [0.0, 0, 0, 0.6, None], 'spine': [0.22, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.5, 'gy': -0.4}}), toonDur=0.35, toonEase='inOut')])],   # sinking under it
        props=[P('chair3', 'chair', pos=ME3, ry=0), P('b3', 'skullBump', on=HEAD(), opts={'grow': [[0.0, 0.17], [0.4, 0.26], [0.85, 0.4], [1.35, 0.55]], 'throb': [0.1, 2.4], 'red': 0.1}),
               P('cal3', 'monthCalendar', pos=[1.15, 1.45, -2.98], scale=1.4, opts={'months': ['JUILLET', 'AOÛT', 'SEPTEMBRE', 'OCTOBRE'], 'flipAt': 0.14, 'dur': 0.43})],
        cams=[FC(0.0, [0.4, 1.4, 1.4], [[0.0, 3.0, ME3[2]], [0.0, 0.4, ME3[2]], [-0.65, 2.0, ME3[2]], [0.65, 2.0, ME3[2]]], top=0.1, bottom=0.76, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:static', 'S03', 0.1, 0.1)

# 4: the doctor measured it. His front garden: the ball of skin three metres high on his head; the doctor in a white coat, up a ladder against it,
#    lays a yellow tape measure down its front from the top to his skull; he waits under it, his neck sunk, deadpan
D4 = st.dur('S04')
ME4 = [0.0, 0, -1.0]
# (pass 3) the doctor kneels ON the top of the ball, bent over its front to the reading: up a ladder at its side his body was inside the ball (and the
# ladder's top went into it). The ladder now rests on the ball's front right at 17 degrees, where the ball's side leans as much: how he got up there
BSQ = (1.0, 1.0)                                                         # (measured) his squash does not reach the ball on his head
BCA = [0.0, 3.53, -0.98]; BTA = 4.93                                     # the ball's centre and top as he stands under it (debugJoints: his head joint at 1.64)
LADB = [1.8, 0, 0.82]; LADL = 0.3
DOC = [0.0, r(BTA - 0.13), -1.12]                                       # (pass 4) 12 cm lower: his knees on the ball's top, not above its outline
TAG = 0.55                                                               # the reading this far down the front, in radians from the top: clear of his shoes
NOSE = [0.0, r(DOC[1] + 1.31), -0.52]                                    # his nose as he peers down at it ((pass 4) debugJoints: his head joint 1.13 above him, at z -0.71)
HOOKTO = [r((NOSE[0] - BCA[0]) / (BALL * BSQ[0])), r((NOSE[1] - BCA[1]) / (BALL * BSQ[1])), r((NOSE[2] - BCA[2]) / (BALL * BSQ[0]))]   # his nose in the ball's own frame
TAPEU = [[0.0, 0.0], [0.15, 0.0], [0.95, 1.0]]
HOLDTOP = {'reach': {'R': [-0.06, r(BTA + 0.06), -0.9, 1, 0.05]}, 'hands': {'R': 'grip'}}   # the end of the tape held on the top of the ball
PEER = lambda extra=None: {**HOLDTOP, **(extra or {})}
LOOKTAG = [0.0, r(BTA - 0.2), -0.2]
# (pass 4) his free hand feeds the tape down the front of the ball (on its meridian), then he settles: he held one pose 1.2 s while it laid itself down
MER = lambda th: [0.02, r(BCA[1] + (BALL + 0.03) * math.cos(th)), r(BCA[2] + (BALL + 0.03) * math.sin(th))]
FEED = lambda th, sp, face: {'reach': {'R': HOLDTOP['reach']['R'], 'L': [*MER(th), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'pinch'}, 'bend': {'spine': [sp, 0, 0, 1, None]}, 'face': face}
st.shot('S04', 'pavillon', actors=[
        act('mec', ME4, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.0),
            k(0.7, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': {'lid': 1.0}}), toonDur=0.05), k(0.8, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.45, 'gy': -0.5}}), toonDur=0.1)]),
        act('medecin', DOC, 0, 'peerIn', 'determined', keys=[k(0.0, look=LOOKTAG), k(0.0, toon=PEER({'face': {'tongue': 0.5, 'tongueLen': 0.07}}), toonDur=0.0),
            k(0.15, toon=FEED(0.25, 0.25, {'tongue': 0.5, 'tongueLen': 0.07, 'brow': -0.2}), toonDur=0.12, toonEase='inOut'),   # (pass 4) he takes the tape...
            k(0.3, toon=FEED(0.45, 0.38, {'tongue': 0.6, 'tongueLen': 0.08, 'brow': -0.3}), toonDur=0.15, toonEase='inOut'),   # ...feeds it down the front...
            k(0.44, toon=FEED(0.64, 0.5, {'tongue': 0.65, 'tongueLen': 0.08, 'brow': -0.4}), toonDur=0.14, toonEase='inOut'),   # ...as far as his arm goes...
            k(0.75, toon=FEED(0.6, 0.38, {'tongue': 0.5, 'tongueLen': 0.07, 'brow': -0.2}), toonDur=0.3, toonEase='inOut')])],   # ...and settles back as it runs on by itself, his tongue out
        props=[P('b4', 'skullBump', on=HEAD(), opts={'r': BALL, 'throb': [0.03, 1.4], 'red': 0.08, 'tape': {'phi': round(PI / 2, 4), 'u': TAPEU, 'readout': ['3,00 M', 0.95, 9.0], 'tagW': 0.55, 'tagAt': TAG, 'tagDphi': 0.35}}),
               P('lad4', 'ladder', pos=LADB, ry=45, opts={'h': 4.1, 'lean': LADL})],
        cams=[FC(0.0, [0.9, 2.4, 7.0], [[0.0, r(BTA + 1.6), DOC[2]], [0.0, 0.0, ME4[2]], [-1.55, BCA[1], ME4[2]], [1.55, BCA[1], ME4[2]], [r(LADB[0] + 0.3), 0.0, LADB[2]]], top=0.06, bottom=0.8, drift=(0.0, 0.0, -0.15))])
st.cue('sfx:zip', 'S04', 0.2, 0.25)

# 5: three metres. Close at the top: the doctor on his knees on the ball, the reading 3,00 M under his nose; he lets it go: the tape whips back up,
#    his eyes pop, CLAC, its hook on his nose, his head knocked back and squashed; he rocks on his knees on top of the ball
D5 = st.dur('S05'); SN5 = 0.34; HITD = round(SN5 + 0.34, 3)   # (pass 4) the engine's whip: 0.2 s up the ball, 0.14 s to his nose, 8 frames on it   # (pass 2) the hook lands on his nose 0.3 s after he lets go (it flew off the top: no cause for the CLAC)
st.shot('S05', 'pavillon', actors=[
        act('medecin', DOC, 0, 'peerIn', 'determined', keys=[k(0.0, look=LOOKTAG), k(0.0, toon=PEER({'face': {'brow': 0.6, 'mouth': 'smile'}}), toonDur=0.0),
            k(round(SN5 - 0.08, 3), toon=PEER({'face': {'brow': 0.7, 'mouth': 'smile', 'lid': 0.2}}), toonDur=0.05),   # he reads it, pleased...
            k(round(SN5 + 0.1, 3), toon=PEER({'face': {'brow': 1.0, 'mouth': 'O', 'lid': 0.0, 'pop': 0.5}}), toonDur=0.05, toonEase='out'),   # ...the tape whips up at him: his eyes pop...
            k(HITD, toon={'touch': {'L': ['face', 0.42, 0.35, 0.06, 1, 0.03], 'R': ['face', -0.42, 0.35, 0.06, 1, 0.03]}, 'hands': {'L': 'spread', 'R': 'spread'},   # (final pass) his hands to his face (one flung to the cloud)
                          'bend': {'neck': [-0.55, 0, 0, 1, None], 'spine': [-0.35, 0, 0, 1, None]}, 'scl': {'head': [1.2, 0.8, 1.2]},
                         'lay': [0.0, -0.18], 'face': {'cross': 0.9, 'brow': 1.0, 'mouth': 'O', 'stars': 0.8}}, toonDur=0.033, toonEase='out'),   # ...CLAC: the hook on his nose, his head knocked back...
            *[k(round(HITD + 0.06 + 0.07 * i, 3), toon={'touch': {'L': ['face', 0.42, 0.35, 0.06, 1, 0.03], 'R': ['face', -0.42, 0.35, 0.06, 1, 0.03]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'bend': {'neck': [round(-0.3 * 0.6 ** i, 3), 0, 0, 1, None], 'spine': [-0.2, 0, 0, 1, None]},
                         'lay': [0.0, round(0.16 * (0.6 ** i) * (1 if i % 2 == 0 else -1), 3)], 'face': {'cross': 0.6, 'brow': 0.8, 'mouth': 'wavy', 'stars': 0.6}}, toonDur=0.06) for i in range(4)]]),   # ...he rocks on his knees on top of the ball
        act('mec', ME4, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.0)])],
        props=[P('b5', 'skullBump', on=HEAD(), opts={'r': BALL, 'throb': [0.03, 1.4], 'red': 0.08, 'tape': {'phi': round(PI / 2, 4), 'u': [[0.0, 1.0]], 'snap': SN5, 'readout': ['3,00 M', 0.0, 9.0], 'tagW': 0.55, 'tagAt': TAG, 'tagDphi': 0.35, 'hookTo': HOOKTO, 'hookOff': HITD}}),
               P('hook5', 'tapeHook', on={'actor': 'medecin', 'joint': 'head', 'offset': [0.0, 0.16, 0.13]}, keys=[k(0.0, visible=False), k(HITD, visible=True), k(round(HITD + 0.4, 3), visible=False)]),   # (final pass) on his nose, held
               P('lad5', 'ladder', pos=LADB, ry=45, opts={'h': 4.1, 'lean': LADL}), BURST('clac5', [r(NOSE[0] + 0.72), r(NOSE[1] - 0.35), r(NOSE[2] + 0.3)], HITD, 'CLAC !', 0.46)],   # (pass 4) clear of his head and his arm
        cams=[FC(0.0, [0.75, r(BTA + 0.95), 1.6], [[0.0, r(BTA + 1.6), DOC[2]], [0.0, r(BTA - 0.45), -0.15], [-0.6, r(BTA + 0.9), DOC[2]], [0.95, r(BTA + 1.5), r(NOSE[2] + 0.2)]], top=0.18, bottom=0.68)])   # (pass 4) above the top: the crown shows under his knees
        # close on the top of the ball: his face, the reading under it and the burst beside it, the card band clear
st.cue('sfx:twang', 'S05', SN5, 0.4); st.cue('clack', 'S05', HITD, 0.45)

# 6: the land registry. A meadow: the surveyor in his hard hat sights the man and his ball through a level on its tripod, bends to the eyepiece,
#    straightens and waves him an inch to the left; the man does not move
D6 = st.dur('S06')
ME6 = [0.0, 0, -2.2]; SUR = [1.95, 0, 0.75]; LEV = [1.6, 0, 0.6]   # (audit) the surveyor off to the right: in line with the man he covered two thirds of him
st.shot('S06', 'grassland', setOpts=SUMMER, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[SUR[0], 1.8, SUR[2]]), k(0.0, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.0),
            k(0.8, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': {'lid': 1.0}}), toonDur=0.05), k(0.9, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.08)]),
        act('geometre', SUR, -150, 'stand', 'neutral', keys=[k(0.0, look=[ME6[0], 3.0, ME6[2]]), k(0.0, toon={'bend': {'spine': [0.55, 0, 0, 1, None]}, 'reach': {'L': [r(LEV[0] + 0.1), 1.5, r(LEV[2] - 0.05), 1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'lidL': 0.9, 'brow': -0.3}}, toonDur=0.0),
            k(0.45, toon={'bend': {'spine': [0.05, 0, 0, 1, None]}, 'face': {'brow': 0.5}}, toonDur=0.15, toonEase='out'), k(0.45, face=-40, turn=0.15), k(0.5, look={'actor': 'mec', 'cheat': 0.65}),   # (stills v1) he straightens up turned to us (his back, 114 degrees; pass 3: in profile at -75, 86 degrees)
            *[k(round(0.62 + 0.1 * i, 3), toon={'bend': {'spine': [0.05, 0, 0, 1, None]}, 'reach': {'R': [r(SUR[0] - 0.42 - (0.32 if i % 2 else 0.0)), (1.6 if i % 2 else 1.78), r(SUR[2] - 0.3), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'brow': 0.6, 'mouth': 'flat'}}, toonDur=0.08) for i in range(4)]])],   # a little to the left, please (pass 2: a wave you can see)
        props=[P('b6', 'skullBump', on=HEAD(), opts={'r': BALL, 'throb': [0.03, 1.4], 'red': 0.08}), P('lev6', 'theodolite', pos=LEV, ry=round(math.degrees(math.atan2(ME6[0] - LEV[0], ME6[2] - LEV[2])), 1))],
        cams=[FC(0.0, [0.9, 1.55, 3.3], [[ME6[0], r(BALLTOP + 0.1), ME6[2]], [ME6[0], 0.0, ME6[2]], [-1.45, BALLC, ME6[2]], [r(SUR[0] + 0.3), 2.25, SUR[2]], [SUR[0], 0.0, SUR[2]], [LEV[0], 1.5, LEV[2]]], top=0.1, bottom=0.8)])
        # over the surveyor's shoulder: the level near, the man under his ball beyond it
st.cue('sfx:beep', 'S06', 0.3, 0.15)

# 7: classed as a hill. THUNK: a blue enamel plate COLLINE drops onto the top of the ball and sinks in; his knees buckle; grass spreads down from it
D7 = st.dur('S07'); PL7 = 0.12
# (pass 4) the knees buckle: his head pinned lower, his feet planted, the legs bend (the squash and the bent legs lifted his feet: 1 % of the frame)
PIN7 = lambda y: {'joint': 'head', 'off': [0.0, 0.0, 0.0], 'at': [0.13, r(y), -2.2], 'w': 1}   # (debugJoints) his head joint at [0.13, 1.65, -2.2]
PLANT7 = {'L': [0.07, 0.02, -2.2, 1], 'R': [-0.11, 0.05, -2.19, 1]}
st.shot('S07', 'grassland', setOpts=SUMMER, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.55, {'face': DEADPAN}), toonDur=0.0),
            k(round(PL7 + 0.02, 3), toon=SUNK(0.4, {'sq': [1.32, 0.64, 1.32], 'face': {'lid': 0.0, 'cross': 0.8, 'brow': 0.6}}), toonDur=0.033, toonEase='out'),   # (final pass) TCHAC: squashed to 64 % of his height...
            k(round(PL7 + 0.13, 3), toon=SUNK(0.42, {'sq': [1.28, 0.67, 1.28], 'face': {'lid': 0.0, 'cross': 0.8, 'brow': 0.6}}), toonDur=0.1),   # ...held four frames...
            k(round(PL7 + 0.19, 3), toon=SUNK(0.6, {'sq': [0.9, 1.12, 0.9], 'face': {'lid': 0.35, 'cross': 0.3}}), toonDur=0.06, toonEase='outBack'),   # ...up past his height...
            k(round(PL7 + 0.34, 3), toon=SUNK(0.55, {'face': DEADPAN}), toonDur=0.12)])],   # ...and he takes the weight again, deadpan
        props=[P('b7', 'skullBump', on=HEAD(), opts={'r': BALL, 'red': 0.08, 'grass': 0.62, 'grassAt': round(PL7 + 0.08, 3), 'plaque': ['COLLINE'], 'plaqueAt': PL7, 'plaqueScale': 2.0, 'mode': 'ball'}),   # (stills v1) the plate twice as big: from this far it barely read
               BURST('thunk7', [0.95, r(BALLTOP + 0.2), r(ME6[2] + 0.6)], round(PL7 + 0.02, 3), 'TCHAC !', 0.8)],   # (pass 2) the size of the BONG at that distance (6 px letters)
        cams=[FC(0.0, [0.7, 3.1, 4.2], [[ME6[0], r(BALLTOP + 0.5), ME6[2]], [ME6[0], 0.0, ME6[2]], [-1.45, BALLC, ME6[2]], [1.45, BALLC, ME6[2]]], top=0.32, bottom=0.8)])   # (pass 4) higher: tilted steeply up, the top of the sky was a black spot   # (pass 2) the plate at about a third of the height, under the COLLINE card
        # the card COLLINE drops in over it: the plate stays under the card band
st.cue('sfx:thud', 'S07', round(PL7 + 0.02, 3), 0.45); st.cue('sfx:slideUp', 'S07', round(PL7 + 0.1, 3), 0.15)

# 8: on Sundays, hikers. The hill on his head: grass, trees, a path winding up to the plate and a flag; hikers with backpacks climb it; he stands
#    under it in the meadow, his neck sunk, deadpan, a breath
D8 = st.dur('S08')
HILLOPTS = {'r': HILL, 'hr': HR, 'grass': 0.93, 'trees': 11, 'path': True, 'flag': True, 'plaque': ['COLLINE'], 'seed': 5, 'mode': 'hill'}
st.shot('S08', 'grassland', setOpts=SUMMER, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': DEADPAN}), toonDur=0.0),
            k(0.45, toon=SUNK(0.5, {'sq': [1.05, 0.96, 1.05], 'face': DEADPAN}), toonDur=0.3, toonEase='inOut'), k(0.85, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {'lid': 1.0}}), toonDur=0.05),
            k(0.95, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': DEADPAN}), toonDur=0.08)])],
        props=[P('b8', 'skullBump', on=HEAD(), opts={**HILLOPTS, 'figH': 0.26, 'hikers': [[0.08, 0.07], [0.3, 0.06], [0.55, 0.07], [0.78, 0.05]]})],
        cams=[FC(0.0, [0.3, 1.3, 6.0], [[ME6[0], r(HILLTOP + 0.45), ME6[2]], [ME6[0], 0.0, ME6[2]], [r(ME6[0] - 2.45), r(TOP + 0.1), ME6[2]], [r(ME6[0] + 2.45), r(TOP + 0.1), ME6[2]]], top=0.08, bottom=0.8, drift=(0.0, 0.0, -0.6))])   # (final pass) at his chest height, the whole dome with sky on both sides (from below it was a brown ceiling)
st.cue('sfx:ding', 'S08', 0.1, 0.12)

# 9: hikers. Close on the summit from above: a hiker reaches the plate and waves, another climbs the last turn; the flag flutters
D9 = st.dur('S09')
st.shot('S09', 'grassland', setOpts=SUMMER, actors=[act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': DEADPAN}), toonDur=0.0)])],
        props=[P('b9', 'skullBump', on=HEAD(), opts={**HILLOPTS, 'hikers': [[0.975, 0.0], [0.86, 0.06], [0.7, 0.07]]})],
        cams=[FC(0.0, [0.9, r(HILLTOP + 1.1), r(ME6[2] + 2.3)], [[ME6[0], r(HILLTOP + 0.45), ME6[2]], [r(ME6[0] - 0.8), r(HILLTOP - 0.25), ME6[2]], [r(ME6[0] + 0.8), r(HILLTOP - 0.25), ME6[2]], [ME6[0], r(HILLTOP - 0.35), r(ME6[2] + 0.8)]], top=0.16, bottom=0.72)])
st.cue('sfx:ding', 'S09', 0.15, 0.15)

# 10: in winter, a ski resort. The hill under snow: skiers come down it, a chair lift goes up; snow falls; he stands under it with a red nose,
#     shivering, deadpan
D10 = st.dur('S10')
SNOWOPTS = {'r': HILL, 'hr': HR, 'grass': 0.93, 'snow': 1.0, 'trees': 9, 'path': True, 'lift': True, 'chairs': 6, 'seed': 6, 'mode': 'hill'}   # (pass 2) snow down to the rim (a lime band read as summer)
COLD = {'cheeks': 0.9, 'blush': 0.8, 'tremble': 0.6, 'lid': 0.5}
st.shot('S10', 'grassland', setOpts=SNOWY, look=LOOKS, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': COLD}), toonDur=0.0),
            *[k(round(0.1 + 0.07 * i, 3), toon=SUNK(0.5, {'sq': ([1.08, 0.92, 1.08] if i % 2 else [1.04, 0.96, 1.04]), 'lay': [0.0, (0.035 if i % 2 else -0.035)], 'face': {**COLD, 'cross': (0.15 if i % 2 else 0.0)}}), toonDur=0.06) for i in range(12)]])],   # (final pass) a big chattering shiver
        props=[P('b10', 'skullBump', on=HEAD(), opts={**SNOWOPTS, 'figH': 0.26, 'skiers': [[0.0, 0.32], [0.35, 0.28], [0.62, 0.34], [0.85, 0.3]]}),
               P('snow10', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 9, 'h': 7, 'd': 8, 'n': 700})],
        cams=[FC(0.0, [0.3, 1.3, 6.0], [[ME6[0], r(HILLTOP + 0.4), ME6[2]], [ME6[0], 0.0, ME6[2]], [r(ME6[0] - 2.45), r(TOP + 0.1), ME6[2]], [r(ME6[0] + 2.45), r(TOP + 0.1), ME6[2]]], top=0.08, bottom=0.8, drift=(0.0, 0.0, -0.6))])   # (final pass) as S08
st.cue('whoosh', 'S10', 0.1, 0.2, 0.6, 300, 900)

# 11: a ski resort. Closer: a skier shoots off the rim of the hill above him like off a ski jump and sails down past his face, in profile, into the
#     snow in front of him; his eyes and then his head follow it across and down; deadpan, a blink
D11 = st.dur('S11'); JMP11 = 0.1; HANG11 = 0.27; LAND11 = 0.6   # (pass 4) five frames hanging on the lip before the drop
# (pass 3) the rim is 2.4 m in front of his face (the hill is that wide): the skier leaves it at its lip and comes down in front of it, the whole flight
# in view (pass 2 started inside the hill: the rim hid its head and it left the frame in four frames)
SKTOP = [0.75, 2.47, -0.2]; SKLIP = [0.5, 2.03, 0.26]
SKFLY = [[0.38, 2.22, 0.5], [0.22, 2.0, 0.72], [0.08, 1.55, 0.88], [-0.04, 0.85, 1.0], [-0.12, 0.02, 1.08]]   # (stills 3) down in front of him, not across: a vertical frame is narrow
GAZE11 = [(0.0, 0.3, -0.6), (JMP11, 0.28, -0.6), (round(HANG11 - 0.02, 3), 0.25, -0.55), (round(HANG11 + 0.05, 3), 0.12, -0.05), (0.42, 0.02, 0.3), (round(LAND11 - 0.04, 3), -0.05, 0.72), (0.72, -0.05, 0.68)]   # (t, gx, gy): (pass 4) the eyes alone follow; the head stays level (the hill on it tipped over his face)
st.shot('S11', 'grassland', setOpts=SNOWY, look=LOOKS, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'lid': 0.15, 'gx': 0.3, 'gy': -0.6}}), toonDur=0.0),
            *[k(t_, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'lid': 0.1, 'gx': gx_, 'gy': gy_}}), toonDur=0.07) for t_, gx_, gy_ in GAZE11[1:]],
            k(round(D11 - 0.12, 3), toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'gx': -0.5, 'lid': 1.0}}), toonDur=0.05)])],   # a blink
        props=[P('b11', 'skullBump', on=HEAD(), opts={**SNOWOPTS, 'skiers': [[0.2, 0.3], [0.6, 0.26]]}),
               P('jump11', 'miniFigure', pos=SKTOP, ry=-90, opts={'kind': 'skier', 'h': 0.45, 'poses': [[0.0, 'ski'], [JMP11, 'flail'], [LAND11, 'ski']], 'color': '#E0A030'},   # (final pass) windmilling on the lip   # (pass 4) half the size (it stood half his height: the hill stopped reading as a hill)
                 keys=[k(0.0, to=SKLIP, dur=JMP11, ease='in'), k(JMP11, rotTo=[0.0, round(-PI / 2, 4), 0.3], dur=0.06), k(round(JMP11 + 0.06, 3), rotTo=[0.0, round(-PI / 2, 4), -0.25], dur=0.06), k(round(JMP11 + 0.12, 3), rotTo=[0.0, round(-PI / 2, 4), 0.2], dur=0.05),   # it teeters...
                       k(HANG11, path=SKFLY, dur=round(LAND11 - HANG11, 3), ease='in'), k(HANG11, rotTo=[0.0, round(-PI / 2, 4), 0.35], dur=0.25),
                       k(HANG11, squash=[0.85, 1.25, 0.85], dur=0.16), k(LAND11, squash=[1.35, 0.65, 1.35], dur=0.2)]),   # on the lip it looks down (hang time), then drops   # in profile; stretched as it leaves the lip, squashed as it lands
               P('snow11', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 6, 'h': 5, 'd': 7, 'n': 450})],
        cams=[FC(0.0, [0.3, 1.6, 2.6], [[ME6[0], 2.0, ME6[2]], [ME6[0], 0.95, ME6[2]], [0.62, 2.95, 0.22], [0.62, 2.0, 0.26], [-0.35, 2.05, 0.26]], top=0.05, bottom=0.8, lenses=range(26, 45))])   # (stills 4) the skier whole on the lip (it was cut by the top)
        # low, in front of the rim: the brim of the hill across the top of the frame, his face under it, the skier dropping off its lip
st.cue('whoosh', 'S11', round(HANG11 + 0.02, 3), 0.35, 0.4, 500, 2000); st.cue('sfx:thud', 'S11', LAND11, 0.3)

# 12: yesterday it went down. Close on his face under the white rim: PSCHHH: the hill goes down like a balloon, wobbling; his neck springs back up past
#     its length; a plaster on his skull; deadpan
D12 = st.dur('S12'); DF12 = 0.08; DFD = 0.68   # (pass 4) 20 frames of deflation (the engine's wobble is slower and bigger), the spring and the settle in the shot
st.shot('S12', 'grassland', setOpts=SNOWY, look=LOOKS, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'gy': -0.4}}), toonDur=0.0),
            k(round(DF12 + 0.3, 3), toon=SUNK(0.75, {'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.3, 'gy': -0.8, 'brow': 0.5}}), toonDur=0.25, toonEase='in'),
            k(round(DF12 + DFD, 3), toon=SUNK(1.4, {'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.3, 'gy': -0.6, 'brow': 0.7}}), toonDur=0.08, toonEase='outBack'),   # the neck springs up past its length...
            k(round(DF12 + DFD + 0.12, 3), toon=SUNK(0.9, {'face': {'lid': 0.4, 'gy': -0.3}}), toonDur=0.08), k(round(DF12 + DFD + 0.22, 3), toon=SUNK(1.0, {'face': DEADPAN}), toonDur=0.08)])],   # ...and settles, deadpan
        props=[P('b12', 'skullBump', on=HEAD(), opts={**SNOWOPTS, 'deflate': [DF12, DFD], 'plaster': True}), BURST('psch12', [-0.22, 2.75, r(ME6[2] + 0.5)], round(DF12 + 0.05, 3), 'PSCHHH !', 0.5),
               P('snow12', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 6, 'h': 5, 'd': 6, 'n': 450})],
        cams=[FC(0.0, [0.35, 1.7, 1.3], [[ME6[0], 2.95, ME6[2]], [ME6[0], 1.3, ME6[2]], [-0.7, 2.2, ME6[2]], [0.7, 2.2, ME6[2]]], top=0.12, bottom=0.72)])
st.cue('sfx:slideDown', 'S12', DF12, 0.4); st.cue('whoosh', 'S12', DF12, 0.25, DFD, 900, 200)

# 13: it went down. Wide: no hill; above him the skiers hang in the air where the slope was, looking down; he looks up at them; a blink
D13 = st.dur('S13')
SKA = [0.9, r(TOP + 1.17), r(ME6[2] + 1.3)]; SKB = [-1.3, r(TOP + 1.17), r(ME6[2] + 0.9)]; SKC = [0.3, r(TOP + 1.58), r(ME6[2] + 0.3)]   # (stills v1) on the old slope, nearer the lens (behind him they were specks)
HANGER = lambda pid, pos, ry, col, poses, keys=None, h=0.5: P(pid, 'miniFigure', pos=pos, ry=ry, opts={'kind': 'skier', 'h': h, 'color': col, 'poses': poses}, keys=keys or [])
st.shot('S13', 'grassland', setOpts=SNOWY, look=LOOKS, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [0.0, r(TOP + 1.4), r(ME6[2] + 0.9)], 'cheat': 0.35}), k(0.0, toon=SUNK(1.0, {'face': {'lid': 0.4, 'gy': -0.9}}), toonDur=0.0),   # (pass 4) his head tilts up to them
            k(0.12, toon=SUNK(1.0, {'face': {'lid': 0.1, 'gy': -1.0, 'brow': 0.5}}), toonDur=0.1),   # (pass 2) his eyes open, up at them (half-lidded they never moved)
            k(0.45, toon=SUNK(1.0, {'face': {'lid': 1.0, 'gy': -0.9}}), toonDur=0.05), k(0.55, toon=SUNK(1.0, {'face': {'lid': 0.1, 'gy': -1.0, 'brow': 0.5}}), toonDur=0.08)])],
        props=[P('b13', 'skullBump', on=HEAD(), opts={'r': 0.0001, 'plaster': True, 'deflate': [-1.0, 0.1]}),
               HANGER('ska13', SKA, 20, '#E04A3A', [[0.0, 'hang'], [0.3, 'look']]), HANGER('skb13', SKB, -40, '#3A8FE0', [[0.0, 'hang'], [0.4, 'look']]), HANGER('skc13', SKC, 0, '#2EA86A', [[0.0, 'look']]),
               P('snow13', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 9, 'h': 7, 'd': 8, 'n': 600})],
        cams=[FC(0.0, [0.3, 2.0, 5.2], [[ME6[0], r(TOP + 1.95), ME6[2]], [ME6[0], 0.0, ME6[2]], [r(SKB[0] - 0.3), SKB[1], SKB[2]], [r(SKA[0] + 0.3), SKA[1], SKA[2]]], top=0.1, bottom=0.8)])

# 14: the skiers fell from a height. Close on them in the air: they look down, one looks at us and waves weakly; on « tombés » they drop, flailing
D14 = st.dur('S14'); FALL = round(min(st.at('S14', 'L08', 3) - 0.03, D14 - 0.48), 3)   # « tombés »; (pass 4) at the latest 0.48 s before the cut: the three falls end in the shot (at 0.8 s two of them fell across the cut)
st.shot('S14', 'grassland', setOpts=SNOWY, look=LOOKS, actors=[act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[SKA[0], SKA[1], SKA[2]]), k(0.0, toon=SUNK(1.0, {'face': {'lid': 0.4, 'gy': -0.9}}), toonDur=0.0)])],
        props=[HANGER('ska14', SKA, 20, '#E04A3A', [[0.0, 'look'], [0.15, 'wave'], [round(FALL - 0.15, 3), 'flail']], [k(FALL, to=[SKA[0], 0.05, SKA[2]], dur=0.3, ease='in'), k(FALL, squash=[0.8, 1.35, 0.8], dur=0.3)]),   # (pass 4) flailing in the air before the drop; the falls in the shot
               HANGER('skb14', SKB, -40, '#3A8FE0', [[0.0, 'look'], [round(FALL - 0.12, 3), 'flail']], [k(round(FALL + 0.03, 3), to=[SKB[0], 0.05, SKB[2]], dur=0.3, ease='in'), k(round(FALL + 0.03, 3), squash=[0.8, 1.35, 0.8], dur=0.3)]),
               HANGER('skc14', SKC, 0, '#2EA86A', [[0.0, 'look'], [round(FALL - 0.1, 3), 'flail']], [k(round(FALL + 0.06, 3), to=[SKC[0], 0.05, SKC[2]], dur=0.3, ease='in'), k(round(FALL + 0.06, 3), squash=[0.8, 1.35, 0.8], dur=0.3)]),
               P('snow14', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 9, 'h': 7, 'd': 8, 'n': 600})],
        cams=[FC(0.0, [0.5, 1.15, r(ME6[2] + 3.4)], [[SKA[0], r(SKA[1] + 0.45), SKA[2]], [SKB[0], r(SKB[1] + 0.4), SKB[2]], [SKC[0], r(SKC[1] + 0.45), SKC[2]], [SKA[0], r(SKA[1] - 0.2), SKA[2]], [SKB[0], r(SKB[1] - 0.2), SKB[2]], [ME6[0], 1.75, ME6[2]]], top=0.14, bottom=0.7)])   # (pass 4) from below: sky under their skis (level, they stood on the far snow mounds); his face over the caption band
st.cue('whoosh', 'S14', FALL, 0.4, 0.4, 1600, 300)

# 15: from a height. They land round him in the snow: two head first, skis up; the third on his head, sitting on it; his head squashed, a blink
D15 = st.dur('S15'); LAND = 0.1
st.shot('S15', 'grassland', setOpts=SNOWY, look=LOOKS, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(1.0, {'face': {'lid': 0.4, 'gy': -0.6}}), toonDur=0.0),
            k(LAND, toon=SUNK(0.55, {'scl': {'head': [1.22, 0.76, 1.22]}, 'sq': [1.08, 0.92, 1.08], 'face': {'lid': 0.2, 'cross': 0.5}}), toonDur=0.033, toonEase='out'),   # a skier lands on his head...
            k(round(LAND + 0.2, 3), toon=SUNK(0.58, {'scl': {'head': [1.18, 0.79, 1.18]}, 'sq': [1.07, 0.93, 1.07], 'face': {'lid': 0.2, 'cross': 0.5}}), toonDur=0.17),   # ...(pass 4) held six frames...
            k(round(LAND + 0.28, 3), toon=SUNK(1.05, {'scl': {'head': [0.93, 1.09, 0.93]}, 'face': {'lid': 0.35}}), toonDur=0.07, toonEase='outBack'),   # ...an overshoot...
            k(round(LAND + 0.38, 3), toon=SUNK(0.9, {'face': {'lid': 0.4}}), toonDur=0.08), k(0.55, toon=SUNK(0.9, {'face': {'lid': 1.0}}), toonDur=0.05),
            k(0.63, toon=SUNK(0.9, {'face': DEADPAN}), toonDur=0.06)])],   # ...deadpan, a blink
        props=[P('b15', 'skullBump', on=HEAD(), opts={'r': 0.0001, 'plaster': True, 'deflate': [-1.0, 0.1]}),
               P('ska15', 'miniFigure', pos=[0.0, 3.2, ME6[2]], opts={'kind': 'skier', 'h': 0.45, 'color': '#E04A3A', 'poses': [[0.0, 'flail'], [LAND, 'sit']]},
                 keys=[k(0.0, to=[0.0, r(TOP + 0.05), ME6[2]], dur=LAND, ease='in'), k(LAND, attach='mec', joint='head', offset=[0.0, 0.53, 0.0], rot=[0.0, round(PI / 2, 4), 0.0])]),   # (pass 4) in profile: facing us its skis were two posts over his face
               P('skb15', 'miniFigure', pos=[-0.62, 2.6, r(ME6[2] + 0.3)], rot=[round(PI, 4), 0.0, 0.2], opts={'kind': 'skier', 'h': 0.62, 'color': '#3A8FE0', 'pose': 'flail'}, keys=[k(0.0, to=[-0.62, 0.3, r(ME6[2] + 0.3)], dur=0.06, ease='in')]),   # (final pass) falls in and plants, higher in the frame
               P('puff15b', 'dustPuff', pos=[-0.62, 0.0, r(ME6[2] + 0.3)], opts={'once': True, 'startAt': 0.06, 'period': 0.5, 'color': '#FFFFFF'}),
               P('skc15', 'miniFigure', pos=[0.64, 2.6, r(ME6[2] + 0.32)], rot=[round(PI, 4), 0.0, -0.25], opts={'kind': 'skier', 'h': 0.62, 'color': '#2EA86A', 'pose': 'flail'}, keys=[k(0.0, visible=False), k(0.05, visible=True), k(0.05, to=[0.64, 0.3, r(ME6[2] + 0.32)], dur=0.07, ease='in')]),
               P('puff15c', 'dustPuff', pos=[0.64, 0.0, r(ME6[2] + 0.32)], opts={'once': True, 'startAt': 0.12, 'period': 0.5, 'color': '#FFFFFF'}),
               BURST('pof15', [0.55, 2.8, r(ME6[2] + 0.4)], LAND, 'POF !', 0.36), P('snow15', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 6, 'h': 5, 'd': 6, 'n': 450})],
        cams=[FC(0.0, [0.3, 1.4, 1.7], [[ME6[0], 2.8, ME6[2]], [ME6[0], 0.0, ME6[2]], [-0.85, 0.75, r(ME6[2] + 0.3)], [0.88, 0.75, r(ME6[2] + 0.32)]], top=0.12, bottom=0.72)])   # (pass 4) closer (0.7 s wide: the landing was small marks in the corners)
st.cue('sfx:thud', 'S15', LAND, 0.45); st.cue('sfx:thud', 'S15', 0.06, 0.3); st.cue('sfx:thud', 'S15', 0.12, 0.3)

# 16: the resort wants its passes. The resort's man in a red jacket walks in and holds out a bill to him; he takes it; the skier still on his head
D16 = st.dur('S16'); GIVE16 = 0.75
EMP = [1.5, 0, r(ME6[2] + 0.35)]; BILL16 = [0.55, 1.25, r(ME6[2] + 0.45)]
st.shot('S16', 'grassland', setOpts=SNOWY, look=LOOKS, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look={'actor': 'employe'}), k(0.0, toon=SUNK(0.9, {'face': DEADPAN}), toonDur=0.0),
            k(round(GIVE16 - 0.2, 3), toon=SUNK(0.9, {'reach': {'L': [r(BILL16[0] - 0.05), r(BILL16[1] - 0.02), BILL16[2], 1, 0.05]}, 'hands': {'L': 'pinch'}, 'face': DEADPAN}), toonDur=0.2, toonEase='inOut'),
            k(round(GIVE16 + 0.2, 3), toon=SUNK(0.9, {'reach': {'L': [-0.05, 1.25, r(ME6[2] + 0.4), 1, 0.05]}, 'hands': {'L': 'pinch'}, 'face': DEADPAN}), toonDur=0.25, toonEase='inOut'), k(round(GIVE16 + 0.25, 3), look='camera')]),
        act('employe', [2.6, 0, r(ME6[2] + 0.5)], -90, 'stand', 'happy', keys=[k(0.0, look={'actor': 'mec'}), k(0.0, to=EMP, dur=0.5, clip='walk', then='stand', ease='out', face='move'),
            k(0.4, toon={'reach': {'R': [r(BILL16[0] + 0.05), r(BILL16[1] + 0.02), BILL16[2], 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.2, toonEase='out'),
            k(round(GIVE16 + 0.1, 3), toon={'reach': {'R': [r(EMP[0] - 0.3), 1.1, r(EMP[2] + 0.15), 0, 0.05]}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.25)])],
        props=[P('b16', 'skullBump', on=HEAD(), opts={'r': 0.0001, 'plaster': True, 'deflate': [-1.0, 0.1]}),
               P('ska16', 'miniFigure', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.53, 0.0], 'rot': [0.0, round(PI / 2, 4), 0.0]}, opts={'kind': 'skier', 'h': 0.45, 'color': '#E04A3A', 'pose': 'sit'}),
               P('bill16', 'billScroll', pos=BILL16, opts={'len': [[0.0, 0.3]], 'top': BILL16[1]}, keys=[k(0.0, attach='employe', joint='handR', offset=[0.0, -0.03, 0.05]), k(GIVE16, attach='mec', joint='handL', offset=[0.0, -0.03, 0.05])]),   # (pass 2) carried in by him, passed at the hands (it hung in the air before he came)
               P('skb16', 'miniFigure', pos=[-0.95, 0.24, r(ME6[2] + 0.9)], rot=[round(PI, 4), 0.0, 0.2], opts={'kind': 'skier', 'h': 0.5, 'color': '#3A8FE0', 'pose': 'flail'}),
               P('snow16', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 7, 'h': 5, 'd': 7, 'n': 450})],
        cams=[FC(0.0, [0.9, 1.6, 2.9], [[ME6[0], 2.75, ME6[2]], [ME6[0], 0.0, ME6[2]], [EMP[0], 2.2, EMP[2]], [r(EMP[0] + 0.35), 0.0, EMP[2]], [-0.6, 1.4, ME6[2]]], top=0.12, bottom=0.8)])
st.cue('sfx:paper', 'S16', GIVE16, 0.3)

# 17: the passes. He holds the bill: it unrolls down to the snow and runs away along it toward us, on and on; he looks at us, deadpan, a slow blink
D17 = st.dur('S17')
BILL17 = [-0.05, 1.27, r(ME6[2] + 0.4)]
st.shot('S17', 'grassland', setOpts=SNOWY, look=LOOKS, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': DEADPAN}), toonDur=0.0),
            k(0.2, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {'lid': 0.4, 'gy': 0.6}}), toonDur=0.15),   # he looks down at it...
            k(0.6, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'sq': [1.0, 1.02, 1.0], 'face': {'lid': 0.4, 'gy': 0.7}}), toonDur=0.3, toonEase='inOut'),   # (final pass) a breath
            k(1.0, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': DEADPAN}), toonDur=0.2),   # ...back at us...
            k(1.6, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {'lid': 1.0}}), toonDur=0.08),
            k(1.78, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': DEADPAN}), toonDur=0.14),   # ...a slow blink
            k(2.05, toon=SUNK(0.92, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'sq': [1.0, 1.02, 1.0], 'face': DEADPAN}), toonDur=0.25, toonEase='inOut')])],
        props=[P('b17', 'skullBump', on=HEAD(), opts={'r': 0.0001, 'plaster': True, 'deflate': [-1.0, 0.1]}),
               P('ska17', 'miniFigure', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.53, 0.0], 'rot': [0.0, round(PI / 2, 4), 0.0]}, opts={'kind': 'skier', 'h': 0.45, 'color': '#E04A3A', 'pose': 'sit'}),   # (pass 2) seated (standing up to wave it rose into the FORFAITS band)
               P('bill17', 'billScroll', pos=BILL17, opts={'len': [[0.1, 0.3], [1.8, 9.0], [round(D17, 3), 12.0]], 'top': BILL17[1]}),   # (final pass) still running out through the hold
               P('skb17', 'miniFigure', pos=[-0.95, 0.24, r(ME6[2] + 0.9)], rot=[round(PI, 4), 0.0, 0.2], opts={'kind': 'skier', 'h': 0.5, 'color': '#3A8FE0', 'pose': 'flail'}),
               P('snow17', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 7, 'h': 5, 'd': 9, 'n': 500})],
        cams=[FC(0.0, [0.55, 2.3, 3.2], [[ME6[0], 2.85, ME6[2]], [ME6[0], 0.0, ME6[2]], [-0.7, 1.4, ME6[2]], [0.7, 1.4, ME6[2]], [0.0, 0.0, r(ME6[2] + 2.6)]], top=0.22, bottom=0.8, drift=(0.0, -0.25, -0.7))])   # (pass 4) the seated skier under the FORFAITS card; (final pass) higher, the strip on the snow in view, a slow push in
st.cue('sfx:paper', 'S17', 0.15, 0.25); st.cue('sfx:zip', 'S17', 0.3, 0.2, 1.4)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', round(HIT1 + 0.05, 3), 'mec', 'bong'), ('S02', 0.8, 'mec', 'bump'), ('S03', 1.2, 'mec', 'growing'), ('S04', 1.1, 'mec', 'measured'), ('S05', round(SN5 + 0.1, 3), 'medecin', 'snap'),
           ('S06', 0.7, 'geometre', 'survey'), ('S07', 0.4, 'mec', 'colline'), ('S08', 0.8, 'mec', 'hill'), ('S10', 0.6, 'mec', 'winter'), ('S11', 0.5, 'mec', 'skier_eyes'),
           ('S12', 0.75, 'mec', 'deflate'), ('S13', 0.5, 'mec', 'hang'), ('S15', 0.3, 'mec', 'landing'), ('S16', 0.9, 'mec', 'bill'), ('S17', 1.7, 'mec', 'unroll')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S01', 0.3, 'beam1', 'sign'), ('S07', 0.5, 'b7', 'plaque'), ('S17', 0.9, 'bill17', 'bill')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S07', 'COLLINE')
st.card('S17', 'FORFAITS')

st.write("La bosse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=1.0,   # (final pass) full pupils: at 0.5 his eyes read as pale slivers
         hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'medecin': {'preset': 'savant', 'seed': 561, 'hair': 'receding', 'hairColor': '#5A4632', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'geometre': {'preset': 'worker', 'seed': 562, 'facial': 'mustache', 'build': {'width': 1.0, 'headWidth': 1.2}},
    'employe': {'preset': 'worker', 'seed': 563, 'hat': 'beanie', 'hatColor': '#C8302A', 'suit': '#C8302A', 'facial': 'none', 'build': {'width': 0.95, 'headWidth': 1.2}},
})
