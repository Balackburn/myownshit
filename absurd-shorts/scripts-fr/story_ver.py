#!/usr/bin/env python3
"""Le ver de terre (story 35, the user's story): this man was mowing the lawn when an earthworm told him he had no right to. The worm called
the police; he was arrested for « dégradation de bien personnel ». In prison he hired an avocat (a lawyer — here a real avocado in a robe) who
« raconte des salades » (lettuce flies out of its mouth). On the day of the trial the angry worm ate the avocat (a gulp, the lump goes down,
a burp, the stone spat out). Shader look (engine/look.js)."""
from story_kit import *

st = Story('ver', look='shaders')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L07', 6),
         ('S09', 'L08', 0), ('S10', 'L08', 3), ('S11', 'L09', 0), ('S12', 'L10', 0), ('S13', 'L10', 6)])


def onscreen(cam_, look, d, sx, sy):   # a world point d metres in front of the camera at screen offset (sx, sy) in half-widths / half-heights (lens 44, 9:16)
    f = [look[i] - cam_[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)); f = [v / n for v in f]
    r = [-f[2], 0.0, f[0]]; n = math.sqrt(r[0] ** 2 + r[2] ** 2); r = [v / n for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    return [round(cam_[i] + d * (f[i] + 0.2272 * sx * r[i] + 0.4040 * sy * u[i]), 3) for i in range(3)]
def yaw_to(p, cam_): return round(math.degrees(math.atan2(cam_[0] - p[0], cam_[2] - p[2])), 1)
def add(a, b): return [round(a[i] + b[i], 3) for i in range(3)]

# ---- the garden: he mows toward +Z (toward the road); mowed stripes behind him, tall grass ahead; the worm comes up in the tall grass
X = -2.0; Z0, Z1 = -2.3, -1.75          # the mec walks from Z0 to Z1 during S01, then stops
MOW = lambda z: [X + 0.02, 0, round(z + 0.95, 3)]   # the mower origin in front of him (its handle bar at his hands)
LAWN = P('lawn', 'mowedLawn', pos=[X, 0, -0.6], opts={'w': 4.6, 'd': 5.0, 'cut': 0.42, 'stripes': 8, 'h': 0.17})
W = [X + 0.12, 0, 0.6]                  # the worm's hole, 0.8 m ahead of the mower
HOLE = P('hole', 'dirtMound', pos=W)
D1 = st.dur('S01')
PEEK = [W[0], -0.5, W[2]]
st.shot('S01', 'pavillon', actors=[act('mec', [X, 0, Z0], 0, 'pushMower', 'whistle', keys=[k(0.0, to=[X, 0, Z1], dur=D1, glide=True, face='keep')]),
        act('ver', PEEK, 20, 'idle', 'scared', keys=[k(0.9, expr='surprised')])],
        props=[LAWN, HOLE, P('mower', 'mowerRun', pos=MOW(Z0), opts={'runAt': 0.0}, keys=[k(0.0, to=MOW(Z1), dur=D1)])],
        cams=[cam(0.0, [X + 0.32, 0.24, 2.12], [X + 0.29, 0.27, 1.95], [X + 0.02, 0.52, -1.4], [X + 0.02, 0.56, -1.4], lens=44)])   # in front of the fence rail (z 2.2): a path tracer sees inside the rail box
# 2: the worm pops out of the ground (dirt), surprised, then angry at the mower; the mower stops
TP = st.at('S02', 'L02', 3) - 0.05
st.shot('S02', 'pavillon', actors=[act('mec', [X, 0, Z1], 0, 'pushMowerStand', 'neutral', keys=[k(TP + 0.25, expr='surprised')]),
        act('ver', PEEK, 8, 'idle', 'surprised', keys=[k(TP, to=W, dur=0.32, ease='outBack', move=True), k(st.at('S02', 'L02', 7), expr='angry', clip='angry')])],
        props=[LAWN, HOLE, P('mower', 'mowerRun', pos=MOW(Z1), opts={'runAt': 0.0, 'stopAt': TP + 0.15}), P('burst', 'dirtBurst', pos=W, opts={'popAt': TP})],
        cams=[cam(0.0, add(W, [0.22, 0.16, 0.95]), add(W, [0.21, 0.17, 0.88]), add(W, [-0.02, 0.4, 0]), add(W, [-0.02, 0.42, 0]), lens=44)])
# 3: the worm turns to him and tells him off (bubble), then his face: shocked
T3 = st.at('S03', 'L03', 6) - 0.08
C3a = [X - 0.05, 0.62, -0.22]; L3a = add(W, [0.04, 0.47, 0])
BUB = onscreen(C3a, L3a, 0.62, 0.02, 0.72)
st.shot('S03', 'pavillon', actors=[act('mec', [X, 0, Z1], 0, 'stand', 'shocked', keys=[k(T3, expr='awe')]), act('ver', W, 180, 'talk', 'angry')],
        props=[LAWN, HOLE, P('mower', 'mowerRun', pos=MOW(Z1), opts={'runAt': 0.0, 'stopAt': 0.0}),
               P('bub', 'speechBubble', pos=BUB, ry=yaw_to(BUB, C3a), opts={'text': "MEC, T'AS PAS\nLE DROIT !", 'popAt': 0.04, 'tail': 'down', 'w': 0.22, 'h': 0.11})],
        cams=[cam(0.0, C3a, add(C3a, [0.02, -0.02, 0.06]), L3a, L3a, lens=44),
              cam(T3, [X + 0.22, 1.6, Z1 + 1.35], [X + 0.21, 1.6, Z1 + 1.22], [X, 1.82, Z1], [X, 1.83, Z1], lens=44)], look={'sunDir': [-0.35, 0.62, -0.7]})
# 4: the worm calls the police on a phone propped in the grass (« POLICE 17 »), smug
PH = add(W, [0.0, 0.02, 0.5])
st.shot('S04', 'pavillon', actors=[act('mec', [X, 0, Z1], 0, 'pushMowerStand', 'confused'), act('ver', W, 25, 'talk', 'smug')],
        props=[LAWN, HOLE, P('mower', 'mowerRun', pos=MOW(Z1), opts={'runAt': 0.0, 'stopAt': 0.0}),
               P('phone', 'phone17', on={'actor': 'ver', 'joint': 'head', 'offset': [-0.085, 0.07, 0.03], 'rot': [0, -0.35, 0.25]}, opts={'w': 0.085})],
        cams=[cam(0.0, add(W, [0.15, 0.5, 0.95]), add(W, [0.14, 0.5, 0.86]), add(W, [-0.02, 0.56, 0]), add(W, [-0.02, 0.57, 0]), lens=44)])
# 5: the arrest: the police car on the road, two cops, the mec cuffed; the worm in the foreground, smug at the camera
MZ = -0.9
VW5 = [X + 0.38, 0, 0.75]
st.shot('S05', 'pavillon', actors=[act('mec', [X, 0, MZ], 0, 'cuffedFront', 'sad', keys=[k(st.at('S05', 'L05', 3) - 0.05, to=[X, 0.2, MZ], dur=0.22, ease='outBack', move=True, face='keep', expr='shocked')]), act('flic', [X - 0.62, 0, MZ - 0.12], 20, 'giveItem', 'determined'),
        act('flic2', [X + 0.6, 0, MZ - 0.15], -25, 'giveItem', 'smug'), act('ver', VW5, -20, 'idle', 'smug')],
        props=[LAWN, P('hole2', 'dirtMound', pos=VW5), P('cuffs', 'handcuffs', on={'actor': 'mec', 'hand': 'R'}, scale=0.6), P('flash', 'policeFlash', pos=[X + 0.4, 1.9, 1.9], opts={'power': 28, 'dist': 9})],
        cams=[cam(0.0, [X + 0.45, 1.6, 2.75], [X + 0.43, 1.6, 2.62], [X, 1.3, MZ], [X, 1.32, MZ], lens=44)])
# 6: the mugshot (flash), the board, the charge on a card
FL = st.at('S06', 'L06', 1)
st.shot('S06', 'interrogation', actors=[act('mec', [0, 0, -2.72], 0, 'cuffedFront', 'pout', keys=[k(FL, expr='confused')])],
        props=[P('wallm', 'mugshotBoard', pos=[0, 0, -3.17], opts={'w': 1.7, 'h': 2.3}), P('plate', 'mugshotPlate', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.3, 0.26]}, opts={'lines': ['LE MEC', 'N° 0042']})],
        cams=[cam(0.0, [0.04, 1.78, -0.3], [0.04, 1.78, -0.4], [0, 1.76, -2.72], [0, 1.77, -2.72], lens=44)], look={'exposure': 1.45, 'fill': 1.3},
        fx=[{'type': 'flash', 'at': 0.12, 'dur': 0.25}, {'type': 'flash', 'at': FL, 'dur': 0.25}])
# 7: in the cell, slumped on the bunk
st.shot('S07', 'prisonCell', actors=[act('mec', [1.95, 0.08, -2.45], 0, 'sitSlump', 'worried')],
        cams=[cam(0.0, [1.72, 1.32, 3.9], [1.73, 1.31, 3.75], [1.95, 1.0, -2.4], [1.95, 1.0, -2.4], lens=60)], look={'exposure': 1.35, 'sunDir': [-0.5, 0.55, 0.65]})
# 8-10: the parlour: the avocat is an avocado in a robe, on the table; it talks lettuce (leaves fly, a salad bubble); his hopeful face under the leaves
AV = [-0.05, 0.785, -0.85]; MEC_T = [0.25, 0, -0.05]; MOUTH = add(AV, [0, 0.54, 0.09])
AVO = lambda clip, expr, keys=None: act('avocat', AV, 0, clip, expr, keys=keys or [])
TA = st.at('S08', 'L07', 7)
st.shot('S08', 'interrogation', actors=[act('mec', MEC_T, 180, 'sit', 'surprised'), AVO('stand', 'smug', [k(TA, clip='wave', expr='happy')])],
        props=[P('case', 'briefcase', on={'actor': 'avocat', 'hand': 'L'}, scale=0.55)],
        cams=[cam(0.0, [0.85, 1.42, 0.38], [0.8, 1.42, 0.28], add(AV, [0, 0.4, 0]), add(AV, [0, 0.41, 0]), lens=44)], look={'exposure': 1.55, 'fill': 1.4})
C9 = [-0.62, 1.38, 0.2]; L9 = add(AV, [0, 0.45, 0]); SB = onscreen(C9, L9, 0.8, 0.36, 0.66)
st.shot('S09', 'interrogation', actors=[act('mec', MEC_T, 180, 'sit', 'neutral'), AVO('talk', 'smug')],
        props=[P('case', 'briefcase', on={'actor': 'avocat', 'hand': 'L'}, scale=0.55), P('leaves', 'saladLeaves', pos=MOUTH, opts={'onAt': 0.05, 'n': 10}),
               P('sbub', 'saladBubble', pos=SB, ry=yaw_to(SB, C9), opts={'popAt': 0.08, 'w': 0.24, 'h': 0.15, 'tail': 'left'})],
        cams=[cam(0.0, C9, [-0.58, 1.38, 0.1], L9, L9, lens=44)], look={'exposure': 1.55, 'fill': 1.4})
C10 = [0.15, 1.58, -1.65]
st.shot('S10', 'interrogation', actors=[act('mec', MEC_T, 180, 'sit', 'confused', keys=[k(0.55, expr='awe')]), AVO('talk', 'smug')],
        props=[P('leaves', 'saladLeaves', pos=MOUTH, ry=180, opts={'onAt': -1.0, 'n': 12, 'seed': 19})],
        cams=[cam(0.0, C10, [-0.58, 1.5, -1.45], add(MEC_T, [0, 1.55, 0]), add(MEC_T, [0, 1.56, 0]), lens=44)], look={'exposure': 1.45, 'fill': 1.4, 'sunDir': [-0.35, 0.7, -0.62]})
# 11-13: the trial: the worm in its pot (bow tie) on the plaintiffs' desk, the avocat pleading on the same desk; the worm's rage; the gulp
DESK = [3.3, 0.79, 0.25]; AVC = [3.15, 0.79, 0.18]; POT = [3.47, 0.79, 0.55]; VW = [POT[0], 1.05, POT[2]]
dxw, dzw = AVC[0] - VW[0], AVC[2] - VW[2]; RYW = round(math.degrees(math.atan2(dxw, dzw)), 1); fn = math.hypot(dxw, dzw); FW = [dxw / fn, 0, dzw / fn]
WORM_C = lambda clip, expr, keys=None: act('verC', VW, RYW, clip, expr, keys=keys or [])
AVC_A = lambda clip, expr, keys=None: act('avocat', AVC, 180, clip, expr, keys=keys or [])
COURT = [P('pot', 'flowerPot', pos=POT)]; FRONT = {'sunDir': [0.35, 0.72, -0.6]}
HIT = 0.28; MOUTH_C = add(AVC, [0, 0.54, -0.09])
st.shot('S11', 'courtroom', actors=[act('juge', [0, 0.3, -4.2], 0, 'gavelStrikeL', 'determined', params={'hit': HIT}), act('mec', [2.75, 0, 1.05], 180, 'sit', 'nervous', fx={'sweat': True}),
        WORM_C('idle', 'angry'), AVC_A('talk', 'smug')],
        props=COURT + [P('leaves', 'saladLeaves', pos=MOUTH_C, ry=180, opts={'onAt': 0.0, 'n': 8})],
        cams=[cam(0.0, [0.35, 2.05, 0.6], [0.34, 2.07, 0.45], [0, 2.62, -4.2], [0, 2.63, -4.2], lens=44), cam(0.6, [2.72, 1.55, -1.65], [2.74, 1.55, -1.52], [3.25, 1.2, 0.35], [3.25, 1.21, 0.35], lens=44)], look=FRONT)
C12 = [3.05, 1.52, -0.95]
st.shot('S12', 'courtroom', actors=[WORM_C('angry', 'angry'), AVC_A('talk', 'smug')],
        props=COURT + [P('leaves', 'saladLeaves', pos=MOUTH_C, ry=180, opts={'onAt': -0.5, 'n': 8, 'seed': 23})],
        cams=[cam(0.0, C12, [3.07, 1.52, -0.85], add(VW, [-0.12, 0.45, -0.1]), add(VW, [-0.12, 0.46, -0.1]), lens=44)], look=FRONT)
TE = st.at('S13', 'L10', 6) + 0.02          # the gulp starts
GULP_AT = [round(VW[0] + FW[0] * 0.36, 3), 1.32, round(VW[2] + FW[2] * 0.36, 3)]   # the worm's mouth at the bottom of the lunge
MEC_C = [2.75, 0, 1.05]; EYE_C = [2.8, 1.6, 0.78]; TR = TE + 1.62; TS = TE + 2.2
HEADW = add(VW, [0, 0.6, 0]); dv = [HEADW[i] - EYE_C[i] for i in range(3)]; dl = math.sqrt(sum(v * v for v in dv)); DV = [v / dl for v in dv]
STONE0 = [round(HEADW[i] - DV[i] * 0.07, 3) for i in range(3)]; STONE1 = [round(EYE_C[i] + DV[i] * 0.16, 3) for i in range(3)]   # from the worm's mouth to just in front of the lens
st.shot('S13', 'courtroom', actors=[WORM_C('angry', 'angry', [k(TE, clip='eat', params={'reach': 0.17}), k(TR, face=round(math.degrees(math.atan2(EYE_C[0] - VW[0], EYE_C[2] - VW[2])), 1))]),
        AVC_A('talk', 'smug', [k(TE - 0.02, clip='stand', expr='scared'), k(TE + 0.24, to=add(GULP_AT, [0, -0.45, 0]), dur=0.16, ease='in', move=True, face='keep'), k(TE + 0.26, scale=0.3), k(TE + 0.42, visible=False)]),
        act('mec', MEC_C, 180, 'sit', 'neutral', keys=[k(TE + 0.3, expr='shocked'), k(TR, expr='unimpressed')])],
        props=COURT + [P('leafm', 'leaf', on={'actor': 'mec', 'joint': 'head', 'offset': [0.05, 0.6, 0.06], 'rot': [-1.2, 0.3, 0.4]}),
               P('stone', 'avocadoStone', pos=STONE0, opts={'still': True, 'r': 0.05}, keys=[k(0.0, visible=False), k(TS, visible=True), k(TS, to=STONE1, dur=0.26, ease='in')])],
        cams=[cam(0.0, [3.12, 1.5, -1.25], [3.13, 1.49, -1.15], [3.25, 1.32, 0.45], [3.25, 1.31, 0.45], lens=44),
              cam(TR - 0.02, [2.35, 1.55, 0.05], [2.37, 1.55, 0.12], add(MEC_C, [0, 1.62, 0]), add(MEC_C, [0, 1.63, 0]), lens=44),
              cam(TS - 0.12, EYE_C, add(EYE_C, [0.03, 0, -0.06]), add(VW, [0, 0.58, 0]), add(VW, [0, 0.58, 0]), lens=44)],
        look=FRONT, fx=[{'type': 'shake', 'at': TS + 0.26, 'dur': 0.35, 'amount': 0.035}])
st.card('S06', 'DÉGRADATION DE BIEN PERSONNEL'); st.card('S11', 'LE JUGEMENT')
st.cue('engine', 'S01', 0.0, 0.22, TP + st.dur('S01') + 0.2); st.cue('sfx:spring', 'S02', TP, 0.45); st.cue('pop', 'S02', TP + 0.02, 0.3)
st.cue('sfx:ring', 'S04', 0.05, 0.25); st.cue('sfx:carDoor', 'S05', 0.1, 0.35); st.cue('sfx:cuff', 'S05', st.at('S05', 'L05', 3), 0.45)
st.cue('clack', 'S06', 0.12, 0.4); st.cue('clack', 'S06', FL, 0.4); st.cue('clang', 'S07', 0.05, 0.35); st.cue('pop', 'S08', TA, 0.35)
st.cue('whoosh', 'S09', 0.05, 0.2, 1.0, 1500, 6000); st.cue('clack', 'S11', HIT, 0.5); st.cue('sfx:roar', 'S12', 0.25, 0.18)
st.cue('sfx:gulp', 'S13', TE + 0.4, 0.6); st.cue('sfx:grunt', 'S13', TE + 1.88, 0.35); st.cue('thud', 'S13', TS + 0.26, 0.6); st.cue('sfx:spring', 'S13', TS, 0.3)
st.write('Le ver de terre', {'ver': {'type': 'creature', 'name': 'worm', 'opts': {'seed': 5}},
                             'verC': {'type': 'creature', 'name': 'worm', 'opts': {'seed': 5, 'bowtie': True}},
                             'avocat': {'type': 'creature', 'name': 'avocat', 'opts': {'seed': 7}},
                             'juge': {'preset': 'judge', 'hat': 'none', 'hair': 'receding', 'facial': 'none', 'glasses': True, 'build': {'width': 0.86, 'headWidth': 1.3, 'headScale': 1.05}}})
