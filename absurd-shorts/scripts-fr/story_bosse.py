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
Natural look; cycle 18 tools: the tip and the pin set before the guided hands (held hands stay on their points), the bump that grows into a hill
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
SNOWY = {'grass': '#EEF2F6', 'sky': ['#A7BED0', '#E6EDF3'], 'seed': 31}
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
st.shot('S01', 'livingRoom', setOpts={'carpet': False, 'picture': False, 'tv': False}, look=LOOKI, actors=[
        act('mec', [0.0, 0, -2.3], 0, 'stand', 'unimpressed', keys=[k(0.0, look=[0.0, 1.9, 2.0]), k(0.0, toon={'face': DEADPAN}, toonDur=0.0),
            k(0.0, to=[0.0, 0, -0.3], dur=HIT1, clip='walk', then='stand', ease='linear', face='keep'),
            k(HIT1, toon={'scl': {'head': [1.26, 0.7, 1.26]}, 'bend': {'neck': [0.25, 0, 0, 0.35, None]}, 'sq': [1.12, 0.86, 1.12], 'face': {'lid': 0.2, 'cross': 0.9, 'brow': 0.9, 'mouth': 'O', 'stars': 1.0}}, toonDur=0.033, toonEase='out'),   # BONG: the head into his shoulders...
            k(round(HIT1 + 0.08, 3), to=[0.0, 0, -0.75], dur=0.22, ease='out', face='keep'),                                            # ...he staggers back...
            k(round(HIT1 + 0.1, 3), toon={'scl': {'head': [0.9, 1.14, 0.9]}, 'bend': {'neck': [-0.1, 0, 0, 1.18, None]}, 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.3, 'cross': 0.8, 'stars': 1.0}}, toonDur=0.08, toonEase='outBack'),   # ...the head pops back up past its place...
            k(round(HIT1 + 0.24, 3), toon={'bend': {'neck': [0.0, 0, 0, 1.0, None]}, 'lay': [0.05, 0.04], 'face': {'lid': 0.4, 'cross': 0.7, 'stars': 1.0}}, toonDur=0.1)])],   # ...swaying, cross-eyed, stars round it
        props=[P('beam1', 'lowBeam', pos=[0.0, 0, 0.0], opts={'h': BEAMH, 'w': 1.3, 'shake': [[HIT1, 0.05]]}), BURST('bong1', [0.55, 2.35, 0.35], HIT1, 'BONG !', 0.5)],
        cams=[FC(0.0, [0.45, 0.85, 2.6], [[0.0, 2.2, -0.3], [0.0, 0.0, -0.3], [-0.8, 2.1, 0.0], [0.8, 2.1, 0.0], [0.0, 0.0, -1.5]], top=0.1, bottom=0.78, drift=(0.0, 0.0, -0.1))])
        # low and in front: his face shows under the beam until the blow, the sign on the beam's face reads
st.cue('sfx:bonk', 'S01', HIT1, 0.5); st.cue('sfx:boing', 'S01', round(HIT1 + 0.1, 3), 0.25)

# 2: the bump. Close: the head springs up and the bump pops out of his skull in three throbs, POC, POC, POC, each bigger; his eyes roll up to it
D2 = st.dur('S02'); POPS = (0.16, 0.42, 0.68)
ME2 = [0.0, 0, -0.75]
GROW2 = [[0.0, 0.0001], [0.1, 0.0001]]
for i_, t_ in enumerate(POPS):
    big = 0.05 * (i_ + 1) + 0.01 * i_
    GROW2 += [[t_, r(big * 0.82)], [r(t_ + 0.05), r(big * 1.12)], [r(t_ + 0.12), r(big)]]   # each pop overshoots and settles
st.shot('S02', 'livingRoom', setOpts={'carpet': False, 'picture': False, 'tv': False}, look=LOOKI, actors=[
        act('mec', ME2, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'lay': [0.05, 0.04], 'face': {'lid': 0.4, 'cross': 0.7, 'stars': 1.0}}, toonDur=0.0),
            *[x for t_ in POPS for x in (k(t_, toon={'scl': {'head': [1.06, 0.93, 1.06]}, 'face': {'lid': 0.3, 'gy': -0.8, 'cross': 0.45, 'brow': 0.7, 'stars': 0.7}}, toonDur=0.033, toonEase='out'),
                                         k(round(t_ + 0.1, 3), toon={'face': {'lid': 0.35, 'gy': -0.85, 'cross': 0.45, 'brow': 0.5, 'stars': 0.6}}, toonDur=0.08))],   # each POC jolts his head; his eyes roll up to it
            k(round(D2 - 0.2, 3), toon={'face': {'lid': 0.45, 'gy': -0.6, 'stars': 0.0}}, toonDur=0.15)])],
        props=[P('b2', 'skullBump', on=HEAD(), opts={'grow': GROW2, 'red': 0.45}),
               *[BURST(f'poc2{i_}', [[-0.45, 2.55, -0.5], [0.45, 2.7, -0.5], [-0.15, 2.95, -0.5]][i_], t_, 'POC !', 0.3) for i_, t_ in enumerate(POPS)]],
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
        props=[P('chair3', 'chair', pos=ME3, ry=0), P('b3', 'skullBump', on=HEAD(), opts={'grow': [[0.0, 0.17], [0.4, 0.26], [0.85, 0.4], [1.35, 0.55]], 'throb': [0.1, 2.4], 'red': 0.4}),
               P('cal3', 'monthCalendar', pos=[1.15, 1.45, -2.98], scale=1.4)],
        cams=[FC(0.0, [0.4, 1.4, 1.4], [[0.0, 3.0, ME3[2]], [0.0, 0.4, ME3[2]], [-0.65, 2.0, ME3[2]], [0.65, 2.0, ME3[2]]], top=0.1, bottom=0.76, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:static', 'S03', 0.1, 0.1)

# 4: the doctor measured it. His front garden: the ball of skin three metres high on his head; the doctor in a white coat, up a ladder against it,
#    lays a yellow tape measure down its front from the top to his skull; he waits under it, his neck sunk, deadpan
D4 = st.dur('S04')
ME4 = [0.0, 0, -1.0]; DOC = [1.35, 2.35, -0.95]
TAPEU = [[0.0, 0.0], [0.15, 0.0], [0.95, 1.0]]
REACHTOP = {'reach': {'R': [0.12, r(BALLTOP + 0.02), -0.85, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.1}
st.shot('S04', 'pavillon', actors=[
        act('mec', ME4, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.0),
            k(0.7, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': {'lid': 1.0}}), toonDur=0.05), k(0.8, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.45, 'gy': -0.5}}), toonDur=0.1)]),
        act('medecin', DOC, -90, 'stand', 'determined', keys=[k(0.0, look=[0.0, BALLTOP, -1.0]), k(0.0, toon={**REACHTOP, 'face': {'tongue': 0.5, 'tongueLen': 0.07}}, toonDur=0.0),
            k(0.5, toon={**REACHTOP, 'bend': {'spine': [-0.1, 0.12, 0, 1, None]}, 'face': {'tongue': 0.6, 'tongueLen': 0.08, 'brow': -0.3}}, toonDur=0.3, toonEase='inOut'),
            k(0.9, look={'point': [0.0, 3.4, -0.5], 'cheat': 0.3})])],
        props=[P('b4', 'skullBump', on=HEAD(), opts={'r': BALL, 'throb': [0.03, 1.4], 'red': 0.3, 'tape': {'phi': round(PI / 2, 4), 'u': TAPEU, 'readout': ['3,00 M', 0.95, 9.0], 'tagW': 0.55}}),
               P('lad4', 'ladder', pos=[1.62, 0, -0.95], ry=90, opts={'h': 3.5, 'lean': 0.18})],
        cams=[FC(0.0, [0.9, 2.4, 6.0], [[0.0, r(BALLTOP + 0.1), ME4[2]], [0.0, 0.0, ME4[2]], [-1.45, BALLC, ME4[2]], [r(DOC[0] + 0.35), r(DOC[1] + 2.2), DOC[2]], [r(DOC[0] + 0.3), 0.0, DOC[2]]], top=0.06, bottom=0.8, drift=(0.0, 0.0, -0.15))])
st.cue('sfx:zip', 'S04', 0.2, 0.25)

# 5: three metres. Close at the top: the reading 3,00 M by the doctor's face; he lets go: CLAC, the tape whips back up and its hook hits him on the
#    nose, his head knocked back and squashed, his glasses askew; he rocks on the ladder
D5 = st.dur('S05'); SN5 = 0.46
st.shot('S05', 'pavillon', actors=[
        act('medecin', DOC, -90, 'stand', 'determined', keys=[k(0.0, look={'point': [0.0, r(BALLTOP - 0.3), -0.6], 'cheat': 0.5}), k(0.0, toon={**REACHTOP, 'face': {'brow': 0.6, 'mouth': 'smile'}}, toonDur=0.0),
            k(round(SN5 - 0.08, 3), toon={**REACHTOP, 'face': {'brow': 0.7, 'mouth': 'smile', 'lid': 0.2}}, toonDur=0.05),
            k(SN5, toon={'reach': {'R': [0.3, r(BALLTOP + 0.4), -0.7, 1, 0.05]}, 'hands': {'R': 'spread'}, 'bend': {'neck': [-0.55, 0, 0, 1, None], 'spine': [-0.2, 0, 0, 1, None]}, 'scl': {'head': [1.2, 0.8, 1.2]},
                         'lay': [0.0, -0.18], 'face': {'cross': 0.9, 'brow': 1.0, 'mouth': 'O', 'stars': 0.8}}, toonDur=0.033, toonEase='out'),   # CLAC: the hook in his face...
            *[k(round(SN5 + 0.1 + 0.1 * i, 3), toon={'reach': {'R': [0.3, r(BALLTOP + 0.2), -0.7, 1, 0.05]}, 'hands': {'R': 'spread'}, 'bend': {'neck': [round(-0.3 * 0.6 ** i, 3), 0, 0, 1, None]},
                         'lay': [0.0, round(0.16 * (0.6 ** i) * (1 if i % 2 == 0 else -1), 3)], 'face': {'cross': 0.6, 'brow': 0.8, 'mouth': 'wavy', 'stars': 0.6}}, toonDur=0.09) for i in range(4)]]),   # ...he rocks on the ladder
        act('mec', ME4, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.0)])],
        props=[P('b5', 'skullBump', on=HEAD(), opts={'r': BALL, 'throb': [0.03, 1.4], 'red': 0.3, 'tape': {'phi': round(PI / 2, 4), 'u': [[0.0, 1.0]], 'snap': SN5, 'readout': ['3,00 M', 0.0, 9.0], 'tagW': 0.55}}),
               P('lad5', 'ladder', pos=[1.62, 0, -0.95], ry=90, opts={'h': 3.5, 'lean': 0.18}), BURST('clac5', [0.85, r(BALLTOP + 0.55), -0.4], round(SN5 + 0.02, 3), 'CLAC !', 0.42)],
        cams=[FC(0.0, [0.75, r(BALLTOP - 0.1), 1.6], [[0.0, r(BALLTOP + 0.3), -1.0], [-0.45, r(BALLTOP - 0.5), -0.6], [r(DOC[0] + 0.25), r(DOC[1] + 2.25), DOC[2]], [r(DOC[0] - 0.2), r(DOC[1] + 1.4), DOC[2]]], top=0.2, bottom=0.66)])
        # close on the top of the ball: the reading and the doctor's face, the card band clear
st.cue('sfx:twang', 'S05', SN5, 0.4); st.cue('clack', 'S05', round(SN5 + 0.02, 3), 0.45)

# 6: the land registry. A meadow: the surveyor in his hard hat sights the man and his ball through a level on its tripod, bends to the eyepiece,
#    straightens and waves him an inch to the left; the man does not move
D6 = st.dur('S06')
ME6 = [0.0, 0, -2.2]; SUR = [1.95, 0, 0.75]; LEV = [1.6, 0, 0.6]   # (audit) the surveyor off to the right: in line with the man he covered two thirds of him
st.shot('S06', 'grassland', actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[SUR[0], 1.8, SUR[2]]), k(0.0, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.0),
            k(0.8, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': {'lid': 1.0}}), toonDur=0.05), k(0.9, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.08)]),
        act('geometre', SUR, -150, 'stand', 'neutral', keys=[k(0.0, look=[ME6[0], 3.0, ME6[2]]), k(0.0, toon={'bend': {'spine': [0.55, 0, 0, 1, None]}, 'reach': {'L': [r(LEV[0] + 0.1), 1.5, r(LEV[2] - 0.05), 1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'lidL': 0.9, 'brow': -0.3}}, toonDur=0.0),
            k(0.45, toon={'bend': {'spine': [0.05, 0, 0, 1, None]}, 'face': {'brow': 0.5}}, toonDur=0.15, toonEase='out'), k(0.5, look={'actor': 'mec', 'cheat': 0.4}),
            *[k(round(0.62 + 0.1 * i, 3), toon={'bend': {'spine': [0.05, 0, 0, 1, None]}, 'reach': {'R': [r(SUR[0] - 0.5 - (0.12 if i % 2 else 0.0)), 1.7, r(SUR[2] - 0.3), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'brow': 0.6, 'mouth': 'flat'}}, toonDur=0.08) for i in range(4)]])],   # a little to the left, please
        props=[P('b6', 'skullBump', on=HEAD(), opts={'r': BALL, 'throb': [0.03, 1.4], 'red': 0.3}), P('lev6', 'theodolite', pos=LEV, ry=round(math.degrees(math.atan2(ME6[0] - LEV[0], ME6[2] - LEV[2])), 1))],
        cams=[FC(0.0, [0.9, 1.55, 3.3], [[ME6[0], r(BALLTOP + 0.1), ME6[2]], [ME6[0], 0.0, ME6[2]], [-1.45, BALLC, ME6[2]], [r(SUR[0] + 0.3), 2.25, SUR[2]], [SUR[0], 0.0, SUR[2]], [LEV[0], 1.5, LEV[2]]], top=0.1, bottom=0.8)])
        # over the surveyor's shoulder: the level near, the man under his ball beyond it
st.cue('sfx:beep', 'S06', 0.3, 0.15)

# 7: classed as a hill. THUNK: a blue enamel plate COLLINE drops onto the top of the ball and sinks in; his knees buckle; grass spreads down from it
D7 = st.dur('S07'); PL7 = 0.12
st.shot('S07', 'grassland', actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.0),
            k(round(PL7 + 0.02, 3), toon=SUNK(0.4, {'sq': [1.16, 0.83, 1.16], 'face': {'lid': 0.2, 'cross': 0.6, 'brow': 0.5}}), toonDur=0.033, toonEase='out'),   # THUNK: his knees buckle...
            k(round(PL7 + 0.16, 3), toon=SUNK(0.6, {'sq': [0.98, 1.03, 0.98], 'face': {'lid': 0.35, 'cross': 0.3}}), toonDur=0.1, toonEase='outBack'),
            k(round(PL7 + 0.34, 3), toon=SUNK(0.55, {'sq': [1.05, 0.95, 1.05], 'face': DEADPAN}), toonDur=0.12)])],   # ...and he takes the weight again, deadpan
        props=[P('b7', 'skullBump', on=HEAD(), opts={'r': BALL, 'red': 0.3, 'grass': 0.62, 'grassAt': round(PL7 + 0.08, 3), 'plaque': ['COLLINE'], 'plaqueAt': PL7, 'mode': 'ball'}),
               BURST('thunk7', [0.75, r(BALLTOP + 0.4), r(ME6[2] + 0.4)], round(PL7 + 0.02, 3), 'TCHAC !', 0.42)],
        cams=[FC(0.0, [0.7, 2.3, 4.2], [[ME6[0], r(BALLTOP + 0.5), ME6[2]], [ME6[0], 0.0, ME6[2]], [-1.45, BALLC, ME6[2]], [1.45, BALLC, ME6[2]]], top=0.22, bottom=0.8)])
        # the card COLLINE drops in over it: the plate stays under the card band
st.cue('sfx:thud', 'S07', round(PL7 + 0.02, 3), 0.45); st.cue('sfx:slideUp', 'S07', round(PL7 + 0.1, 3), 0.15)

# 8: on Sundays, hikers. The hill on his head: grass, trees, a path winding up to the plate and a flag; hikers with backpacks climb it; he stands
#    under it in the meadow, his neck sunk, deadpan, a breath
D8 = st.dur('S08')
HILLOPTS = {'r': HILL, 'hr': HR, 'grass': 0.93, 'trees': 11, 'path': True, 'flag': True, 'plaque': ['COLLINE'], 'seed': 5, 'mode': 'hill'}
st.shot('S08', 'grassland', actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': DEADPAN}), toonDur=0.0),
            k(0.45, toon=SUNK(0.5, {'sq': [1.05, 0.96, 1.05], 'face': DEADPAN}), toonDur=0.3, toonEase='inOut'), k(0.85, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {'lid': 1.0}}), toonDur=0.05),
            k(0.95, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': DEADPAN}), toonDur=0.08)])],
        props=[P('b8', 'skullBump', on=HEAD(), opts={**HILLOPTS, 'hikers': [[0.08, 0.07], [0.3, 0.06], [0.55, 0.07], [0.78, 0.05]]})],
        cams=[FC(0.0, [0.4, 2.4, 6.5], [[ME6[0], r(HILLTOP + 0.45), ME6[2]], [ME6[0], 0.0, ME6[2]], [r(ME6[0] - HILL), TOP, ME6[2]], [r(ME6[0] + HILL), TOP, ME6[2]]], top=0.1, bottom=0.8, drift=(0.0, 0.0, -0.15))])
st.cue('sfx:ding', 'S08', 0.1, 0.12)

# 9: hikers. Close on the summit from above: a hiker reaches the plate and waves, another climbs the last turn; the flag flutters
D9 = st.dur('S09')
st.shot('S09', 'grassland', actors=[act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': DEADPAN}), toonDur=0.0)])],
        props=[P('b9', 'skullBump', on=HEAD(), opts={**HILLOPTS, 'hikers': [[0.975, 0.0], [0.86, 0.06], [0.7, 0.07]]})],
        cams=[FC(0.0, [0.9, r(HILLTOP + 1.1), r(ME6[2] + 2.3)], [[ME6[0], r(HILLTOP + 0.45), ME6[2]], [r(ME6[0] - 0.8), r(HILLTOP - 0.25), ME6[2]], [r(ME6[0] + 0.8), r(HILLTOP - 0.25), ME6[2]], [ME6[0], r(HILLTOP - 0.35), r(ME6[2] + 0.8)]], top=0.16, bottom=0.72)])
st.cue('sfx:ding', 'S09', 0.15, 0.15)

# 10: in winter, a ski resort. The hill under snow: skiers come down it, a chair lift goes up; snow falls; he stands under it with a red nose,
#     shivering, deadpan
D10 = st.dur('S10')
SNOWOPTS = {'r': HILL, 'hr': HR, 'grass': 0.93, 'snow': 0.8, 'trees': 9, 'path': True, 'lift': True, 'chairs': 6, 'seed': 6, 'mode': 'hill'}
COLD = {'cheeks': 0.9, 'blush': 0.8, 'tremble': 0.6, 'lid': 0.5}
st.shot('S10', 'grassland', setOpts=SNOWY, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': COLD}), toonDur=0.0),
            *[k(round(0.1 + 0.07 * i, 3), toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'lay': [0.0, (0.012 if i % 2 else -0.012)], 'face': COLD}), toonDur=0.06) for i in range(12)]])],   # shivering
        props=[P('b10', 'skullBump', on=HEAD(), opts={**SNOWOPTS, 'skiers': [[0.0, 0.32], [0.35, 0.28], [0.62, 0.34], [0.85, 0.3]]}),
               P('snow10', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 9, 'h': 7, 'd': 8, 'n': 700})],
        cams=[FC(0.0, [0.4, 2.4, 6.5], [[ME6[0], r(HILLTOP + 0.4), ME6[2]], [ME6[0], 0.0, ME6[2]], [r(ME6[0] - HILL), TOP, ME6[2]], [r(ME6[0] + HILL), TOP, ME6[2]]], top=0.1, bottom=0.8, drift=(0.0, 0.0, -0.15))])
st.cue('whoosh', 'S10', 0.1, 0.2, 0.6, 300, 900)

# 11: a ski resort. Closer: a skier shoots off the rim of the hill beside his ear and flies past his face; his eyes follow it across; deadpan
D11 = st.dur('S11'); JMP11 = 0.12
SKPATH = [[1.9, 2.2, -1.95], [1.0, 2.25, -1.35], [-0.2, 1.75, -1.15], [-1.4, 0.6, -1.3]]
st.shot('S11', 'grassland', setOpts=SNOWY, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'gx': 0.8}}), toonDur=0.0),
            k(round(JMP11 + 0.25, 3), toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'gx': 0.0, 'gy': 0.1}}), toonDur=0.15),
            k(round(JMP11 + 0.5, 3), toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'gx': -0.85, 'gy': 0.4}}), toonDur=0.15),   # his eyes follow it across...
            k(round(D11 - 0.15, 3), toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'gx': 0.0, 'lid': 1.0}}), toonDur=0.06)])],   # ...and a blink
        props=[P('b11', 'skullBump', on=HEAD(), opts={**SNOWOPTS, 'skiers': [[0.2, 0.3], [0.6, 0.26]]}),
               P('jump11', 'miniFigure', pos=SKPATH[0], ry=-60, opts={'kind': 'skier', 'h': 0.32, 'poses': [[0.0, 'ski'], [round(JMP11 + 0.05, 3), 'hang']], 'color': '#E0A030'},
                 keys=[k(JMP11, path=SKPATH[1:], dur=0.65, ease='inOut'), k(JMP11, rotTo=[0.0, -1.2, 0.6], dur=0.65)]),
               P('snow11', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 6, 'h': 5, 'd': 6, 'n': 450})],
        cams=[FC(0.0, [0.55, 1.95, 1.4], [[ME6[0], 2.6, ME6[2]], [ME6[0], 1.35, ME6[2]], [1.9, 2.25, -1.95], [-1.1, 1.6, -1.3]], top=0.14, bottom=0.72)])
st.cue('whoosh', 'S11', round(JMP11 + 0.15, 3), 0.35, 0.4, 500, 2000)

# 12: yesterday it went down. Close on his face under the white rim: PSCHHH: the hill goes down like a balloon, wobbling; his neck springs back up past
#     its length; a plaster on his skull; deadpan
D12 = st.dur('S12'); DF12 = 0.2; DFD = 0.62
st.shot('S12', 'grassland', setOpts=SNOWY, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.5, {'sq': [1.06, 0.94, 1.06], 'face': {**COLD, 'gy': -0.4}}), toonDur=0.0),
            k(round(DF12 + 0.3, 3), toon=SUNK(0.75, {'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.3, 'gy': -0.8, 'brow': 0.5}}), toonDur=0.25, toonEase='in'),
            k(round(DF12 + DFD, 3), toon=SUNK(1.4, {'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.3, 'gy': -0.6, 'brow': 0.7}}), toonDur=0.08, toonEase='outBack'),   # the neck springs up past its length...
            k(round(DF12 + DFD + 0.12, 3), toon=SUNK(0.9, {'face': {'lid': 0.4, 'gy': -0.3}}), toonDur=0.08), k(round(DF12 + DFD + 0.22, 3), toon=SUNK(1.0, {'face': DEADPAN}), toonDur=0.08)])],   # ...and settles, deadpan
        props=[P('b12', 'skullBump', on=HEAD(), opts={**SNOWOPTS, 'deflate': [DF12, DFD], 'plaster': True}), BURST('psch12', [-0.55, 2.75, r(ME6[2] + 0.5)], round(DF12 + 0.05, 3), 'PSCHHH !', 0.5),
               P('snow12', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 6, 'h': 5, 'd': 6, 'n': 450})],
        cams=[FC(0.0, [0.35, 1.7, 1.3], [[ME6[0], 2.95, ME6[2]], [ME6[0], 1.3, ME6[2]], [-0.7, 2.2, ME6[2]], [0.7, 2.2, ME6[2]]], top=0.12, bottom=0.72)])
st.cue('sfx:slideDown', 'S12', DF12, 0.4); st.cue('whoosh', 'S12', DF12, 0.25, DFD, 900, 200)

# 13: it went down. Wide: no hill; above him the skiers hang in the air where the slope was, looking down; he looks up at them; a blink
D13 = st.dur('S13')
SKA = [1.05, r(TOP + 1.42), r(ME6[2] + 0.35)]; SKB = [-1.8, r(TOP + 0.95), r(ME6[2] - 0.3)]; SKC = [r(0.4), r(TOP + 1.58), r(ME6[2] - 0.6)]
HANGER = lambda pid, pos, ry, col, poses, keys=None, h=0.32: P(pid, 'miniFigure', pos=pos, ry=ry, opts={'kind': 'skier', 'h': h, 'color': col, 'poses': poses}, keys=keys or [])
st.shot('S13', 'grassland', setOpts=SNOWY, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(1.0, {'face': {'lid': 0.4, 'gy': -0.9}}), toonDur=0.0),
            k(0.45, toon=SUNK(1.0, {'face': {'lid': 1.0, 'gy': -0.9}}), toonDur=0.05), k(0.55, toon=SUNK(1.0, {'face': {'lid': 0.4, 'gy': -0.9}}), toonDur=0.08)])],
        props=[P('b13', 'skullBump', on=HEAD(), opts={'r': 0.0001, 'plaster': True, 'deflate': [-1.0, 0.1]}),
               HANGER('ska13', SKA, 20, '#E04A3A', [[0.0, 'hang'], [0.3, 'look']]), HANGER('skb13', SKB, -40, '#3A8FE0', [[0.0, 'hang'], [0.4, 'look']]), HANGER('skc13', SKC, 0, '#2EA86A', [[0.0, 'look']]),
               P('snow13', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 9, 'h': 7, 'd': 8, 'n': 600})],
        cams=[FC(0.0, [0.3, 2.0, 6.2], [[ME6[0], r(TOP + 1.9), ME6[2]], [ME6[0], 0.0, ME6[2]], [-2.1, 2.6, ME6[2]], [1.4, 2.6, ME6[2]]], top=0.1, bottom=0.8)])

# 14: the skiers fell from a height. Close on them in the air: they look down, one looks at us and waves weakly; on « tombés » they drop, flailing
D14 = st.dur('S14'); FALL = round(st.at('S14', 'L08', 3) - 0.03, 3)   # « tombés »
st.shot('S14', 'grassland', setOpts=SNOWY, actors=[act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[SKA[0], SKA[1], SKA[2]]), k(0.0, toon=SUNK(1.0, {'face': {'lid': 0.4, 'gy': -0.9}}), toonDur=0.0)])],
        props=[HANGER('ska14', SKA, 20, '#E04A3A', [[0.0, 'look'], [0.35, 'wave'], [FALL, 'flail']], [k(FALL, to=[SKA[0], 0.05, SKA[2]], dur=0.42, ease='in'), k(FALL, squash=[0.8, 1.35, 0.8], dur=0.42)]),
               HANGER('skb14', SKB, -40, '#3A8FE0', [[0.0, 'look'], [round(FALL + 0.04, 3), 'flail']], [k(round(FALL + 0.04, 3), to=[SKB[0], 0.05, SKB[2]], dur=0.38, ease='in'), k(round(FALL + 0.04, 3), squash=[0.8, 1.35, 0.8], dur=0.38)]),
               HANGER('skc14', SKC, 0, '#2EA86A', [[0.0, 'look'], [round(FALL + 0.08, 3), 'flail']], [k(round(FALL + 0.08, 3), to=[SKC[0], 0.05, SKC[2]], dur=0.45, ease='in'), k(round(FALL + 0.08, 3), squash=[0.8, 1.35, 0.8], dur=0.45)]),
               P('snow14', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 9, 'h': 7, 'd': 8, 'n': 600})],
        cams=[FC(0.0, [0.5, r(TOP + 1.0), r(ME6[2] + 3.2)], [[SKA[0], r(SKA[1] + 0.45), SKA[2]], [SKB[0], r(SKB[1] + 0.4), SKB[2]], [SKC[0], r(SKC[1] + 0.45), SKC[2]], [SKA[0], r(SKA[1] - 0.2), SKA[2]], [SKB[0], r(SKB[1] - 0.2), SKB[2]]], top=0.18, bottom=0.72)])
st.cue('whoosh', 'S14', FALL, 0.4, 0.4, 1600, 300)

# 15: from a height. They land round him in the snow: two head first, skis up; the third on his head, sitting on it; his head squashed, a blink
D15 = st.dur('S15'); LAND = 0.1
st.shot('S15', 'grassland', setOpts=SNOWY, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(1.0, {'face': {'lid': 0.4, 'gy': -0.6}}), toonDur=0.0),
            k(LAND, toon=SUNK(0.55, {'scl': {'head': [1.2, 0.78, 1.2]}, 'sq': [1.08, 0.92, 1.08], 'face': {'lid': 0.2, 'cross': 0.5}}), toonDur=0.033, toonEase='out'),   # a skier lands on his head...
            k(round(LAND + 0.12, 3), toon=SUNK(0.9, {'face': {'lid': 0.4}}), toonDur=0.1, toonEase='outBack'), k(round(D15 - 0.2, 3), toon=SUNK(0.9, {'face': {'lid': 1.0}}), toonDur=0.05),
            k(round(D15 - 0.1, 3), toon=SUNK(0.9, {'face': DEADPAN}), toonDur=0.08)])],   # ...deadpan, a blink
        props=[P('b15', 'skullBump', on=HEAD(), opts={'r': 0.0001, 'plaster': True, 'deflate': [-1.0, 0.1]}),
               P('ska15', 'miniFigure', pos=[0.0, 3.2, ME6[2]], opts={'kind': 'skier', 'h': 0.32, 'color': '#E04A3A', 'poses': [[0.0, 'flail'], [LAND, 'sit']]},
                 keys=[k(0.0, to=[0.0, r(TOP + 0.05), ME6[2]], dur=LAND, ease='in'), k(LAND, attach='mec', joint='head', offset=[0.0, 0.53, 0.0], rot=[0.0, 0.0, 0.0])]),
               P('skb15', 'miniFigure', pos=[-1.0, 0.0, r(ME6[2] + 0.3)], rot=[round(PI, 4), 0.0, 0.2], opts={'kind': 'skier', 'h': 0.32, 'color': '#3A8FE0', 'pose': 'flail'}, keys=[k(0.0, visible=False), k(0.06, visible=True)]),
               P('skc15', 'miniFigure', pos=[0.95, 0.0, r(ME6[2] + 0.45)], rot=[round(PI, 4), 0.0, -0.25], opts={'kind': 'skier', 'h': 0.32, 'color': '#2EA86A', 'pose': 'flail'}, keys=[k(0.0, visible=False), k(0.12, visible=True)]),
               BURST('pof15', [0.55, 2.8, r(ME6[2] + 0.4)], LAND, 'POF !', 0.36), P('snow15', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 6, 'h': 5, 'd': 6, 'n': 450})],
        cams=[FC(0.0, [0.35, 1.55, 3.0], [[ME6[0], 2.75, ME6[2]], [ME6[0], 0.0, ME6[2]], [-1.25, 0.6, r(ME6[2] + 0.3)], [1.2, 0.6, r(ME6[2] + 0.45)]], top=0.12, bottom=0.8)])
st.cue('sfx:thud', 'S15', LAND, 0.45); st.cue('sfx:thud', 'S15', 0.06, 0.3); st.cue('sfx:thud', 'S15', 0.12, 0.3)

# 16: the resort wants its passes. The resort's man in a red jacket walks in and holds out a bill to him; he takes it; the skier still on his head
D16 = st.dur('S16'); GIVE16 = 0.75
EMP = [1.5, 0, r(ME6[2] + 0.35)]; BILL16 = [0.55, 1.25, r(ME6[2] + 0.45)]
st.shot('S16', 'grassland', setOpts=SNOWY, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look={'actor': 'employe'}), k(0.0, toon=SUNK(0.9, {'face': DEADPAN}), toonDur=0.0),
            k(round(GIVE16 - 0.2, 3), toon=SUNK(0.9, {'reach': {'L': [r(BILL16[0] - 0.05), r(BILL16[1] - 0.02), BILL16[2], 1, 0.05]}, 'hands': {'L': 'pinch'}, 'face': DEADPAN}), toonDur=0.2, toonEase='inOut'),
            k(round(GIVE16 + 0.2, 3), toon=SUNK(0.9, {'reach': {'L': [-0.05, 1.25, r(ME6[2] + 0.4), 1, 0.05]}, 'hands': {'L': 'pinch'}, 'face': DEADPAN}), toonDur=0.25, toonEase='inOut'), k(round(GIVE16 + 0.25, 3), look='camera')]),
        act('employe', [2.6, 0, r(ME6[2] + 0.5)], -90, 'stand', 'happy', keys=[k(0.0, look={'actor': 'mec'}), k(0.0, to=EMP, dur=0.5, clip='walk', then='stand', ease='out', face='move'),
            k(0.4, toon={'reach': {'R': [r(BILL16[0] + 0.05), r(BILL16[1] + 0.02), BILL16[2], 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.2, toonEase='out'),
            k(round(GIVE16 + 0.1, 3), toon={'reach': {'R': [r(EMP[0] - 0.3), 1.1, r(EMP[2] + 0.15), 0, 0.05]}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.25)])],
        props=[P('b16', 'skullBump', on=HEAD(), opts={'r': 0.0001, 'plaster': True, 'deflate': [-1.0, 0.1]}),
               P('ska16', 'miniFigure', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.53, 0.0]}, opts={'kind': 'skier', 'h': 0.32, 'color': '#E04A3A', 'pose': 'sit'}),
               P('bill16', 'billScroll', pos=BILL16, opts={'len': [[0.0, 0.3]], 'top': BILL16[1]}, keys=[k(0.0, to=BILL16, dur=0.01), k(round(GIVE16 + 0.2, 3), to=[-0.05, 1.27, r(ME6[2] + 0.4)], dur=0.25, ease='inOut')]),
               P('skb16', 'miniFigure', pos=[-1.0, 0.0, r(ME6[2] + 0.3)], rot=[round(PI, 4), 0.0, 0.2], opts={'kind': 'skier', 'h': 0.32, 'color': '#3A8FE0', 'pose': 'flail'}),
               P('snow16', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 7, 'h': 5, 'd': 7, 'n': 450})],
        cams=[FC(0.0, [0.9, 1.6, 2.9], [[ME6[0], 2.75, ME6[2]], [ME6[0], 0.0, ME6[2]], [EMP[0], 2.2, EMP[2]], [r(EMP[0] + 0.35), 0.0, EMP[2]], [-0.6, 1.4, ME6[2]]], top=0.12, bottom=0.8)])
st.cue('sfx:paper', 'S16', GIVE16, 0.3)

# 17: the passes. He holds the bill: it unrolls down to the snow and runs away along it toward us, on and on; he looks at us, deadpan, a slow blink
D17 = st.dur('S17')
BILL17 = [-0.05, 1.27, r(ME6[2] + 0.4)]
st.shot('S17', 'grassland', setOpts=SNOWY, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': DEADPAN}), toonDur=0.0),
            k(0.2, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {'lid': 0.4, 'gy': 0.6}}), toonDur=0.15),   # he looks down at it...
            k(1.0, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': DEADPAN}), toonDur=0.2),   # ...back at us...
            k(1.6, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {'lid': 1.0}}), toonDur=0.08),
            k(1.78, toon=SUNK(0.9, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': DEADPAN}), toonDur=0.14),   # ...a slow blink
            k(2.05, toon=SUNK(0.92, {'reach': {'L': [-0.1, 1.25, BILL17[2], 1, 0.05], 'R': [0.0, 1.25, BILL17[2], 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'sq': [1.0, 1.02, 1.0], 'face': DEADPAN}), toonDur=0.25, toonEase='inOut')])],
        props=[P('b17', 'skullBump', on=HEAD(), opts={'r': 0.0001, 'plaster': True, 'deflate': [-1.0, 0.1]}),
               P('ska17', 'miniFigure', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.53, 0.0]}, opts={'kind': 'skier', 'h': 0.32, 'color': '#E04A3A', 'poses': [[0.0, 'sit'], [1.2, 'wave']]}),
               P('bill17', 'billScroll', pos=BILL17, opts={'len': [[0.1, 0.3], [1.8, 9.0]], 'top': BILL17[1]}),
               P('skb17', 'miniFigure', pos=[-1.0, 0.0, r(ME6[2] + 0.3)], rot=[round(PI, 4), 0.0, 0.2], opts={'kind': 'skier', 'h': 0.32, 'color': '#3A8FE0', 'pose': 'flail'}),
               P('snow17', 'snowfall', pos=[ME6[0], 0, ME6[2]], opts={'w': 7, 'h': 5, 'd': 9, 'n': 500})],
        cams=[FC(0.0, [0.55, 1.45, 2.9], [[ME6[0], 2.85, ME6[2]], [ME6[0], 0.0, ME6[2]], [-0.7, 1.4, ME6[2]], [0.7, 1.4, ME6[2]], [0.0, 0.0, r(ME6[2] + 1.6)]], top=0.12, bottom=0.8, drift=(0.0, 0.0, -0.1))])
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

st.write("La bosse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'medecin': {'preset': 'savant', 'seed': 561, 'hair': 'receding', 'hairColor': '#5A4632', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'geometre': {'preset': 'worker', 'seed': 562, 'facial': 'mustache', 'build': {'width': 1.0, 'headWidth': 1.2}},
    'employe': {'preset': 'worker', 'seed': 563, 'hat': 'beanie', 'hatColor': '#C8302A', 'suit': '#C8302A', 'facial': 'none', 'build': {'width': 0.95, 'headWidth': 1.2}},
})
