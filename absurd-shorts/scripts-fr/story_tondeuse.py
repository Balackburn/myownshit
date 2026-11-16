#!/usr/bin/env python3
"""La tondeuse (story 70, cycle 32; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man started his lawnmower. It never stopped. It mowed the neighbour's garden. Then the football stadium. The players applauded. It went
through the forest in a straight line. The wheat fields got circles. The scientists talked about aliens. The gendarmerie gave chase. On foot.
It mowed the lawn of the presidential palace. The president found it very neat. He named it national gardener. It mowed the whole country. In
three weeks. Yesterday it ran out of petrol. Right in front of his house. He put it back in the garage. His garden still isn't mowed.
Staging: his overgrown front lawn, three pulls on the starter cord, coughs, then it takes off on its own, one stripe across his lawn and through
the hedge; the neighbour in his deckchair lifting his feet, the gnome's hat knocked off; a football pitch mown in perfect stripes in a blink, the
players applauding; trees falling left and right in a straight line through the forest; circles in the wheat seen from above; two scientists in
the circles (OVNI ?); two gendarmes running after it on foot, never gaining; the palace lawn in stripes, the president's thumb up, a medal on its
handle and a bow; the country in stripes from the sky; a calendar racing to day 21; it splutters to a stop at his gate; he pushes it into the
garage; his lawn waist-high, the one stripe across it, the gnome popping up beside him.
Natural look; cycle 32 tools: props_tondeuse.js (mowField: grass cut where and when the mower passes; mowerLive: trembles, sprays clippings,
coughs, splutters, slumps, bows; fallTree, stripePitch, bleachers, gnome, hedgeWall, garageShed)."""
from story_kit import *
import math

st = Story('tondeuse', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3, ink=None: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True, **({'ink': ink} if ink else {})})
DEAD = {'lid': 0.45}
XLOOK = {'sat': 1.05, 'contrast': 1.12, 'warm': 1.15}   # (review 1) warmer and punchier: the draft was cooler and flatter than the series
HOUSE_N = {'houseColor': '#F2D6C9', 'roof': '#5A6E8C', 'door': '#8C2F39', 'frame': '#8C2F39'}   # the neighbour's house: another colour
WHEAT = {'cols': ['#E2C25A', '#D4B048', '#EBD27A', '#C9A43E'], 'cutCol': '#C8B07A', 'ground': '#B8964E', 'stripCol': '#D9C88E'}
STRIPES = ['#8DC05E', '#74AE4C']                     # a mown lawn: light and dark bands in turn
MOWER = lambda pid, pos, ry=-90, s=1.0, keys=None, **o: P(pid, 'mowerLive', pos=pos, ry=ry, scale=s, opts=o, **({'keys': keys} if keys else {}))

# his front lawn (the pavillon set: the house at z -6.6, the fence at z 2.2, the gate at x 0.97): the left lawn, the mower's line across it
LAWN = [-2.5, 0, -0.9]; M0 = [0.45, 0, -0.4]; ME0 = [1.55, 0, -0.4]; HEDGE = [-5.5, 0, -1.0]; EDGE0 = 0.2   # (review 2) the mower starts on the path, clear of the tall grass; EDGE0: the lawn's edge, where the stripe begins
LOC = lambda x, z: [r(x - LAWN[0]), r(z - LAWN[2])]   # world x, z in the lawn field's frame
LAWNF = lambda pid, h, path, **o: P(pid, 'mowField', pos=LAWN, opts={'w': 5.4, 'd': 5.8, 'h': h, 'n': 2600, 'width': 0.6, 'path': path, 'stripCol': '#9FCF6E', **o})
HEDGEP = lambda pid, hole_at=None, **o: P(pid, 'hedgeWall', pos=HEDGE, ry=90, opts={'l': 6.0, 'h': 1.45, 'holeX': -0.6, 'burstDir': -1, 'holeShape': 'mower', **({'holeAt': hole_at} if hole_at is not None else {}), **o})
STRIPE = [[-1.0, *LOC(EDGE0, M0[2])], [-0.01, *LOC(-5.6, M0[2])]]   # the one stripe across his lawn, already cut in the later shots
# (review 2) the palace: a lawn in the pitch's two-tone bands running to the steps (stripePitch without lines or goals); a stone slab that covers the
# black hull of the town hall's main box (its outline read as a dark box behind the pediment); the guards' plumed helmets
PLAWN = lambda pid, z, d, passes=None, w=11.2, n=7: P(pid, 'stripePitch', pos=[0.0, 0, z], opts={'w': w, 'd': d, 'n': n, 'lines': False, 'goals': False, 'over': True, 'passes': passes or [[-3.0, -2.0]] * n})
COVER = lambda pid, w, z: P(pid, 'slab', pos=[0.0, r((4.5 * 1.03 + 0.04) / 2), z], opts={'w': r(w * 1.03 + 0.04), 'h': r(4.5 * 1.03 + 0.04), 'd': r(4 * 1.03 + 0.06), 'color': '#EDE4D0'})
HELMET = lambda pid, who, keys=None: P(pid, 'guardHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, scale=1.1, **({'keys': keys} if keys else {}))

for g_ in [('S01', 1.2, 'mec', 'pull'), ('S03', 0.9, 'voisin', 'feet'), ('S05', 0.8, 'joueur1', 'clap'), ('S08', 1.0, 'savant1', 'ovni'), ('S10', 0.5, 'gend1', 'run'),
           ('S12', 1.6, 'president', 'thumb'), ('S13', 1.2, 'president', 'medal'), ('S17', 0.8, 'mec', 'mug'), ('S19', 1.4, 'mec', 'end')]:
    st.gag(*g_)
st.card('S07', 'CERCLES', at=0.5)
st.card('S10', 'À PIED', at=0.1)
st.card('S13', 'JARDINIÈRE', at=0.4)

# 1: the hook. His overgrown front lawn, the red push mower on the path: he pulls the starter cord (a black cord from the engine to a yellow T-handle in
#    his fist): a cough; again: a cough; a third time: it squashes like a spring, catches with a jolt and shoots off on its own into the tall grass,
#    mowing; the camera glides up and left after it: a pale cut lane opens behind it; his hand stays up in the air to the end, deadpan
D1 = st.dur('S01'); START1 = 1.15; Z1 = M0[2]
_f1, _l1, _n1 = fitBack([-1.3, 2.3, 4.0], [[ME0[0], 2.45, Z1], [ME0[0], 0.6, Z1], [2.15, 2.1, -0.35], [-1.2, 0.0, Z1], [-0.4, 0.0, 0.4]], top=0.1, bottom=0.84, lenses=range(26, 66))
GL1 = cam(r(START1 + 0.22), list(_f1), list(_f1), _l1, _l1, lens=_n1)
PULL = lambda x, y, z: {'reach': {'R': [r(x), r(y), r(z), 1, 0.03], 'L': [r(M0[0] + 0.85), 0.98, -0.6, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': DEAD}
CORD = [r(M0[0] + 0.75), 0.86, -0.28]                                  # the cord's handle on the mower's handle (world)
UP1 = [r(M0[0] + 1.65), 1.95, -0.32]                                   # where the start throws his hand: it stays there
st.shot('S01', 'pavillon', setOpts={'fence': False, 'mailbox': False}, look=XLOOK, actors=[
        act('mec', ME0, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[M0[0], 0.4, Z1]), k(0.0, toon=PULL(*CORD), toonDur=0.0),
            *[kk for j, t_ in enumerate((0.18, 0.62, 1.05)) for kk in (k(t_, toon={**PULL(r(M0[0] + 1.52 + 0.12 * j), r(1.45 + 0.15 * j), -0.32), 'bend': {'spine': [r(0.12 + 0.05 * j), 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.08, toonEase='out'),
                *([k(r(t_ + 0.24), toon=PULL(*CORD), toonDur=0.12, toonEase='inOut')] if j < 2 else []))],   # (review 2) no return after the third pull: its key fell after the start's and brought the hand back down
            k(r(START1 + 0.12), toon={**PULL(*UP1), 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.06), k(r(START1 + 0.42), look='camera', lookDur=0.22),
            k(r(START1 + 0.58), toon={'face': {'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(START1 + 0.68), toon={'face': DEAD}, toonDur=0.07, keepPose=True)])],
        props=[LAWNF('lawn1', 0.55, [[r(START1 + 0.17), *LOC(EDGE0, Z1)], [D1, *LOC(-1.9, Z1)]]), HEDGEP('hedge1'),
               MOWER('mow1', M0, runAt=START1, cough=[0.3, 0.75, START1], startAt=START1, startK=2.2, whip=[[r(START1 + 0.05), 0.7]],
                     keys=[k(r(START1 + 0.05), to=[EDGE0, 0, Z1], dur=0.12, ease='linear'), k(r(START1 + 0.17), to=[-1.9, 0, Z1], dur=r(D1 - START1 - 0.17), ease='linear')]),   # (stills 1) to -1.9: at the cut it is still inside the frame, its lane behind it
               P('tee1', 'cordHandle', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.09, 0.0]})],
        tethers=[{'a': {'prop': 'mow1', 'offset': [0.0, 0.5, -0.04]}, 'b': {'actor': 'mec', 'hand': 'R'}, 'color': '#111111', 'radius': 0.024, 'radial': 6, 'sag': 0.02, 'n': 8, 'from': 0.0, 'snap': [START1, 0.12, 0.2]}],   # (final pass) from the engine, thicker: from the handle's top it read as the handlebar
        cams=[FC(0.0, [-0.9, 1.45, 4.0], [[ME0[0], 2.45, Z1], [ME0[0], 0.0, Z1], [r(UP1[0] + 0.2), 2.1, -0.35], [r(M0[0] - 0.45), 0.0, Z1], [-0.3, 0.5, Z1]], top=0.14, bottom=0.76, lenses=range(26, 68)),   # (review 2) no fence: the mower in the clear, three quarters on his face
              glide([GL1], 0.5)])   # (final pass) after the start it rises and pans left: over the foreground grass the pale lane opens behind the mower (it left half out of frame, hidden in the grass)
st.cue('sfx:zip', 'S01', 0.18, 0.25); st.cue('sfx:rattleShort', 'S01', 0.3, 0.3); st.cue('sfx:zip', 'S01', 0.62, 0.25); st.cue('sfx:rattleShort', 'S01', 0.75, 0.3); st.cue('sfx:engine', 'S01', START1, 0.45)

# 2: it never stopped. Behind the mower, down the stripe it cuts: it runs on alone and bursts through the hedge, leaves flying, leaving a hole of its
#    own shape; then on him, his hand still up where the cord left it: he looks at us and slowly lowers it
D2 = st.dur('S02'); HOLE2 = 0.75; CUT2 = 1.0
UP2 = {'reach': {'R': [r(ME0[0] + 0.3), 2.05, -0.9, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}
st.shot('S02', 'pavillon', setOpts={'fence': False, 'mailbox': False}, look=XLOOK, actors=[act('mec', ME0, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[-5.5, 0.6, M0[2]]), k(0.0, toon=UP2, toonDur=0.0),
            k(r(CUT2 + 0.06), look='camera', lookDur=0.12),
            k(1.3, toon={'reach': {'R': [r(ME0[0] - 0.05), 1.0, -0.72, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.32, toonEase='inOut'),
            k(1.5, toon={'face': {'lid': 1.0}}, toonDur=0.06, keepPose=True), k(1.62, toon={'face': DEAD}, toonDur=0.08, keepPose=True)])],
        props=[LAWNF('lawn2', 0.55, [[-1.0, *LOC(EDGE0, M0[2])], [0.0, *LOC(-2.6, M0[2])], [HOLE2, *LOC(-5.6, M0[2])]]), HEDGEP('hedge2', HOLE2, leaves=70, leafS=1.7),
               MOWER('mow2', [-2.6, 0, M0[2]], runAt=0.0, keys=[k(0.0, to=[-5.6, 0, M0[2]], dur=HOLE2, ease='linear'), k(HOLE2, to=[-8.6, 0, M0[2]], dur=r(D2 - HOLE2), ease='linear')])],
        cams=[cam(0.0, [-0.2, 1.25, M0[2]], [-1.1, 1.15, M0[2]], [-5.5, 0.75, M0[2]], [-5.5, 0.75, M0[2]], lens=38),
              FC(CUT2, [-1.3, 1.45, 0.2], [[ME0[0], 2.5, M0[2]], [ME0[0], 0.7, M0[2]], [r(ME0[0] + 0.3), 2.2, -1.0], [ME0[0], 1.4, 0.15]], top=0.15, bottom=0.76)])   # from the stripe, in front of him
st.cue('sfx:engine', 'S02', 0.0, 0.4); st.cue('sfx:crunch', 'S02', HOLE2, 0.35)

# 3: it mowed the neighbour's garden. Next door: the neighbour in pyjamas dozes in his deckchair with his paper; the mower bursts through the hedge: he is
#    launched off the chair, hangs in the air pedalling while it passes under him (the paper flies up), drops back (the chair folds flat and springs
#    back); the mower knocks the hat off his gnome: it spins up and lands askew
D3 = st.dur('S03'); HOLE3 = 0.2; FEET3 = 0.85; GN3 = [-2.6, 0, 1.3]; UP3 = 0.64; DOWN3 = 1.2; HAT3 = r((1.5 - GN3[0]) / 3.9)
VX3 = lambda t: r(1.5 - 3.9 * t)                                         # the mower's x: 3.9 m/s
SIT3 = lambda up, eye=0.0: {'bend': {'legL': [r(-1.1 * up), 0, 0, 1, None], 'legR': [r(-1.1 * up), 0, 0, 1, None]}, 'face': {'lid': r(0.5 * (1 - up)), 'eye': eye, 'brow': r(0.9 * up), 'mouth': 'O' if up > 0.5 else 'line'}}
PED3 = lambda i: {'bend': {'legL': [-1.4 if i % 2 else -0.3, 0, 0, 1, None], 'legR': [-0.3 if i % 2 else -1.4, 0, 0, 1, None]}, 'sq': [0.93, 1.1, 0.93], 'hairUp': 1.0, 'face': {'pop': 0.5, 'popLen': 0.22, 'brow': 1.0, 'mouth': 'O', 'jaw': 0.3}}
st.shot('S03', 'pavillon', setOpts={**HOUSE_N, 'fence': False, 'mailbox': False}, look=XLOOK, actors=[
        act('voisin', [-1.8, 0, 0.25], 0, 'sit', 'neutral', keys=[k(0.0, look=[-1.8, 0.9, 1.2]), k(0.0, toon=SIT3(0.0), toonDur=0.0),
            k(0.5, look=[1.0, 0.4, 1.0]), k(r(UP3 - 0.07), toon={**SIT3(0.0, 0.3), 'sq': [1.15, 0.8, 1.15]}, toonDur=0.05),
            k(UP3, to=[-1.8, 0.95, 0.25], dur=0.14, ease='out', clip='sit', face='keep'), k(UP3, toon={**SIT3(1.0, 0.6), 'sq': [0.9, 1.14, 0.9], 'hairUp': 1.0}, toonDur=0.05, toonEase='out'),
            *[k(r(UP3 + 0.1 + 0.066 * i), toon=PED3(i), toonDur=0.05) for i in range(6)],
            k(r(DOWN3 - 0.14), to=[-1.8, 0.0, 0.25], dur=0.14, ease='in', clip='sit', face='keep'),
            k(DOWN3, toon={**SIT3(0.0, 0.4), 'sq': [1.22, 0.72, 1.22]}, toonDur=0.03), k(r(DOWN3 + 0.1), toon={**SIT3(0.0, 0.4), 'sq': [0.95, 1.06, 0.95]}, toonDur=0.08), k(r(DOWN3 + 0.24), toon=SIT3(0.0, 0.4), toonDur=0.1),
            k(r(DOWN3 + 0.06), look=[GN3[0], 1.6, GN3[2]], lookDur=0.12), k(1.66, look='camera', lookDur=0.14)])],
        props=[P('lawn3', 'mowField', pos=[-2.0, 0, -0.6], opts={'w': 6.4, 'd': 5.6, 'h': 0.18, 'n': 2200, 'width': 0.6, 'path': [[0.0, 3.5, 1.6], [D3, r(VX3(D3) + 2.0), 1.6]], 'stripCol': '#9FCF6E'}),
               P('hedge3', 'hedgeWall', pos=[0.6, 0, -1.0], ry=90, opts={'l': 6.0, 'h': 1.45, 'holeX': -2.0, 'burstDir': -1, 'holeAt': HOLE3, 'holeShape': 'mower', 'leaves': 50, 'leafS': 1.4}),
               P('chair3', 'deckChair', pos=[-1.8, 0, 0.05], keys=[k(r(UP3 - 0.07), squash=[1.1, 0.72, 1.1], dur=0.2), k(DOWN3, squash=[1.3, 0.2, 1.3], dur=0.5)]),
               P('gnome3', 'gnome', pos=GN3, ry=20, opts={'s': 1.7, 'hatAt': HAT3, 'hatUp': 0.8, 'hatT': 0.62}),
               P('paper3', 'newspaper', on={'actor': 'voisin', 'hand': 'R', 'offset': [0.05, 0.0, 0.05]}, keys=[k(UP3, detach=True, fall=True, toss=[0.2, 2.6, 0.4], spinFall=8.0)]),
               MOWER('mow3', [VX3(0.0), 0, 1.0], runAt=0.0, keys=[k(0.0, to=[VX3(D3), 0, 1.0], dur=D3, ease='linear')])],
        cams=[FC(0.0, [-1.0, 1.05, 3.1], [[-1.8, 2.85, 0.25], [-1.8, 0.0, 1.2], [GN3[0], 2.3, GN3[2]], [r(GN3[0] - 0.3), 0.5, GN3[2]], [-0.2, 0.6, 1.0]], top=0.14, bottom=0.78, lenses=range(26, 80))])   # his launch and the hat's flight inside the frame
st.cue('sfx:crunch', 'S03', HOLE3, 0.3); st.cue('sfx:engine', 'S03', 0.1, 0.35); st.cue('sfx:gasp', 'S03', UP3, 0.25); st.cue('sfx:pop', 'S03', HAT3, 0.25); st.cue('thud', 'S03', DOWN3, 0.25)

# 4: then the football stadium. From the stands: the mower runs up and down the pitch so fast it is a blur, and perfect stripes appear one after another;
#    the players at the touchline turn their heads to follow it
D4 = st.dur('S04'); PASS4 = 0.16; W4 = 34.0; D4P = 52.0; NS4 = 8
XS4 = lambda i: r(-W4 / 2 + (i + 0.5) * W4 / NS4)
PASSES4 = [[r(0.05 + PASS4 * i), r(0.05 + PASS4 * (i + 1))] for i in range(NS4)]
MK4 = [kk for i in range(NS4) for kk in (k(PASSES4[i][0], to=[XS4(i), 0, (1 if i % 2 == 0 else -1) * D4P / 2], dur=0.0), k(PASSES4[i][0], to=[XS4(i), 0, (-1 if i % 2 == 0 else 1) * D4P / 2], dur=PASS4, ease='linear'),
                                      k(PASSES4[i][0], rotTo=[0.0, 0.0 if i % 2 else PI, 0.0], dur=0.0))]
PL4 = lambda j: [r(-4.2 + 4.2 * j), 0, r(D4P / 2 + 2.6 + 0.5 * (j % 2))]
def YAW4(j, x, z):   # how far his shoulders turn after the mower at (x, z): 0.45 of the angle from straight ahead (he faces -Z)
    a = math.atan2(x - PL4(j)[0], z - PL4(j)[2]) - PI
    return r(0.45 * ((a + PI) % (2 * PI) - PI))
st.shot('S04', 'grassland', look=XLOOK, actors=[*[act(f'joueur{j + 1}', PL4(j), 180, 'stand', 'neutral',
            keys=[k(0.0, look=[XS4(0), 0.3, D4P / 2]), k(0.0, toon={'yaw': YAW4(j, XS4(0), D4P / 2)}, toonDur=0.0),
                  *[k(PASSES4[i][0], look=[XS4(i), 0.3, (-1 if i % 2 == 0 else 1) * D4P / 2], lookDur=r(PASS4 - 0.02)) for i in range(NS4)],
                  *[k(r(PASSES4[i][0] + 0.04 + 0.03 * j), toon={'yaw': YAW4(j, XS4(i), (-1 if i % 2 == 0 else 1) * D4P / 2), 'sq': [1.0, 1.02, 1.0] if i % 2 else [1.02, 0.97, 1.02]}, toonDur=PASS4, toonEase='inOut') for i in range(NS4)]]) for j in range(3)]],   # (review 2) heads on the mower all the way down each band and back: a tennis match
        props=[P('pitch4', 'stripePitch', opts={'w': W4, 'd': D4P, 'n': NS4, 'passes': PASSES4, 'over': True}), P('stands4', 'bleachers', pos=[-W4 / 2 - 4.0, 0, 0], ry=90, opts={'l': 60, 'rows': 7}),
               P('stands4b', 'bleachers', pos=[W4 / 2 + 4.0, 0, 0], ry=-90, opts={'l': 60, 'rows': 7}), MOWER('mow4', [XS4(0), 0, D4P / 2], ry=180, s=4.0, runAt=0.0, speedLines=True, keys=MK4)],
        cams=[FC(0.0, [1.0, 6.5, 40.0], [[-8.0, 0.0, 14.0], [8.0, 0.0, 14.0], [0.0, 2.44, -D4P / 2], [0.0, 2.45, D4P / 2 + 2.6]], top=0.12, bottom=0.86, lenses=range(26, 80))])   # (review 1) low behind the players: the pitch, its lines and the stripes fill the frame
st.cue('whoosh', 'S04', 0.05, 0.3, 1.2, 300, 1500); st.cue('sfx:engine', 'S04', 0.0, 0.4)

# 5: the players applauded. At the touchline three players clap, each his own way (at the chest, over the head, hopping), the referee a step clear of
#    them, the striped pitch gleaming behind them
D5 = st.dur('S05'); POS5 = [[-0.85, 0, 0.25], [0.0, 0, -0.5], [0.85, 0, 0.3]]; REF5 = [-1.8, 0, -1.2]; DT5 = [0.075, 0.09, 0.065, 0.11]; OFF5 = [0.0, 0.06, 0.03, 0.1]
SMILE5 = {'mouth': 'bigsmile', 'lid': 0.1, 'brow': 0.3}
CLAP = lambda j, i: {'touch': {'R': ['torso', r(-0.03 if i % 2 else -0.24), 0.8, 0.38, 1, 0.02], 'L': ['torso', r(0.03 if i % 2 else 0.24), 0.8, 0.38, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': 0.1}}   # the president's clap (S13) and the hero dusting his hands (S18)
def CLAP5(j, i):   # one key of a clap: even i apart, odd i together; whole poses
    a = 0.03 if i % 2 else 0.27
    if j == 1: return {'touch': {'R': ['face', r(-0.06 if i % 2 else -0.6), 1.3, 0.06, 1, 0.02], 'L': ['face', r(0.06 if i % 2 else 0.6), 1.3, 0.06, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': SMILE5}   # over his head
    q = {'touch': {'R': ['torso', -a, [0.45, 0, 0.41, 0.43][j], 0.42, 1, 0.02], 'L': ['torso', a, [0.45, 0, 0.41, 0.43][j], 0.42, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': SMILE5}
    if j == 2: q['sq'] = [0.95, 1.08, 0.95] if i % 2 else [1.06, 0.92, 1.06]   # he bounces with each clap
    return q
st.shot('S05', 'grassland', look=XLOOK, actors=[*[act(f'joueur{j + 1}', POS5[j], [14, -3, -16][j], 'stand', 'happy', keys=[k(0.0, look='camera'), *[k(r(OFF5[j] + DT5[j] * i), toon=CLAP5(j, i), toonDur=0.05) for i in range(int((D5 - OFF5[j]) / DT5[j]))]]) for j in range(3)],
        act('arbitre', REF5, 16, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.6, 0.0]), k(0.7, look='camera', lookDur=0.2), *[k(r(OFF5[3] + DT5[3] * i), toon=CLAP5(3, i), toonDur=0.06) for i in range(int((D5 - OFF5[3]) / DT5[3]))]])],
        props=[P('pitch5', 'stripePitch', pos=[0.0, 0, -20.0], ry=90, opts={'w': W4, 'd': D4P, 'n': NS4, 'passes': [[-2.0, -1.0]] * NS4, 'over': True}),
               *[P(f'num5{j}', 'raceBib', on={'actor': f'joueur{j + 1}', 'joint': 'torso', 'offset': [0.0, 0.26, 0.19]}, scale=1.25, opts={'num': ['7', '10', '9'][j]}) for j in range(3)]],
        cams=[FC(0.0, [-0.7, 1.3, 5.2], [[-0.85, 2.45, 0.25], [0.85, 2.45, 0.3], [-0.85, 0.0, 0.25], [0.85, 0.0, 0.3], [1.25, 1.2, 0.3], [-2.15, 1.2, -1.2], [-1.8, 2.45, -1.2]], top=0.2, bottom=0.87)])   # (review 2) pushed in; (final pass) further: heads about 15 % of the height, their feet at the foot of the frame (the bottom third was plain green)
for i in range(1, int(D5 / DT5[0]), 2): st.cue('sfx:click', 'S05', r(DT5[0] * i), 0.22)   # the first player's claps, one click each (the mix has no applause)

# 6: it went through the forest in a straight line. Chasing it down its lane over a dark mossy floor: it hops over three roots, its handle whipping; the
#    brown trunks either side tip outward ahead of it, faster and faster, a domino that runs away up the lane; at the end one big tree in its way tips,
#    hangs, and crashes aside as it arrives; behind it stumps and a pale straight lane
D6 = st.dur('S06'); Z06 = -15.0; V6 = 7.0; LEN6 = 3.2; LX6 = 1.35
TREES6 = [r(-10.6 + 1.7 * i) for i in range(14)]   # the lane's trees, left and right in turn: each starts to fall when the mower is LEN6 short of it
GAPS6 = [0.26, 0.23, 0.2, 0.17, 0.14, 0.12, 0.1, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05]   # (final pass) the felling speeds up: an even left-right metronome became a domino that outruns the mower
FALL6 = [r(0.15 + sum(GAPS6[:i])) for i in range(14)]
ROOTS6 = [-9.0, -4.6, -0.6]; HOP6 = [r((z_ + 15.0) / 7.0 - 0.1) for z_ in ROOTS6]   # the roots across the lane and when it takes off for each (0.1 s short of it); BIG6: the last tree, in its way
BIG6 = [0.0, 0, 6.6]
CAM6 = lambda z: ([0.0, 3.6, r(z - 6.0)], [0.0, -0.4, r(z + 6.0)])
st.shot('S06', 'grassland', setOpts={'grass': '#3D5A2E'}, look=XLOOK, actors=[],
        props=[*[P(f'ft6{i}', 'fallTree', pos=[LX6 if i % 2 else -LX6, 0, z_], opts={'s': 1.25, 'seed': i, 'crown': 1.1, 'dir': (PI / 2 if i % 2 else -PI / 2), 'fallAt': FALL6[i]}) for i, z_ in enumerate(TREES6)],
               P('big6', 'fallTree', pos=BIG6, opts={'s': 2.3, 'seed': 77, 'crown': 0.6, 'dir': PI / 2, 'fallAt': 1.58, 'hang': 0.22}),   # (stills 1) in the lane itself, nearer: at 13 m and off the axis it was one more tree at the top of the frame
               *[P(f'root6{i}', 'rootHump', pos=[0.0, 0, z_], ry=[8, -12, 5][i], opts={'l': 2.3, 'r': 0.14}) for i, z_ in enumerate(ROOTS6)],
               *[P(f'fb6{i}', 'fallTree', pos=[LX6 if i % 2 else -LX6, 0, r(-24.2 + 1.7 * i)], opts={'s': 1.25, 'seed': i + 40, 'crown': 1.1, 'dir': (PI / 2 if i % 2 else -PI / 2), 'fallAt': -2.0}) for i in range(8)],
               *[P(f'tr6{i}', 'fallTree', pos=[r((3.4 + 1.5 * (i % 3)) * (1 if i % 2 else -1)), 0, r(-25.0 + 1.75 * i)], opts={'s': r(1.2 + 0.25 * (i % 3)), 'seed': i + 9, 'crown': r(0.9 + 0.3 * (i % 2))}) for i in range(22)],
               P('lane6', 'mowField', pos=[0.0, 0, -6.0], opts={'w': 2.6, 'd': 40.0, 'h': 0.24, 'n': 700, 'width': 1.6, 'path': [[-1.5, 0.0, r(Z06 - 10.5 + 6.0)], [D6, 0.0, r(Z06 + V6 * D6 + 6.0)]],
                                                                 'cols': ['#4E7A3A', '#5B8A44', '#44703A'], 'cutCol': '#B9A26A', 'stripCol': '#C2AE7A', 'ground': 'none', 'over': True}),   # (final pass) the lane a shade darker under the white captions
               MOWER('mow6', [0.0, 0, Z06], ry=0, s=2.0, runAt=0.0, hops=[[t_, 0.15, 0.2] for t_ in HOP6], whip=[[0.0, 0.5], *[[r(t_ + 0.2), 0.45] for t_ in HOP6]], keys=[k(0.0, to=[0.0, 0, r(Z06 + V6 * D6)], dur=D6, ease='linear')])],
        cams=[cam(0.0, CAM6(Z06)[0], CAM6(Z06 + V6 * D6)[0], CAM6(Z06)[1], CAM6(Z06 + V6 * D6)[1], lens=54)])   # (review 2) behind and above it: the mower at two thirds of the frame's height on its pale lane, stumps either side, the trees ahead tipping aside
for i in range(0, 14, 2): st.cue('sfx:crunch', 'S06', r(FALL6[i] + 0.3), 0.25)   # every other tree of the domino
for t_ in HOP6: st.cue('sfx:boing', 'S06', t_, 0.2)
st.cue('sfx:crunch', 'S06', 2.2, 0.4)   # the big one

# 7: the wheat fields got circles. From high above a golden field: the mower draws ring after ring, the stubble pale, the wheat standing between (CERCLES)
D7 = st.dur('S07'); RINGS7 = [3.0, 6.0, 9.0]
def RINGPATH(t0, t1):
    pts, tot = [], sum(2 * PI * R_ for R_ in RINGS7) + 2 * (RINGS7[-1] - RINGS7[0])
    t, x0 = t0, RINGS7[0]
    for j, R_ in enumerate(RINGS7):
        if j: t += (R_ - RINGS7[j - 1]) / tot * (t1 - t0); pts.append([r(t), R_, 0.0])
        for s in range(25):
            a = s / 24 * 2 * PI; pts.append([r(t + (2 * PI * R_ * s / 24) / tot * (t1 - t0)), r(R_ * math.cos(a)), r(R_ * math.sin(a))])
        t += 2 * PI * R_ / tot * (t1 - t0)
    return pts
RP7 = RINGPATH(0.1, r(D7 - 0.1))
st.shot('S07', 'grassland', look=XLOOK, actors=[],
        props=[P('wheat7', 'mowField', opts={'w': 46.0, 'd': 46.0, 'h': 0.9, 'n': 17000, 'width': 1.1, 'path': RP7, 'bw': 0.06, **WHEAT, 'ground': '#C9A646', 'stripCol': '#F2E8BE'}),   # the field to the frame's edges, golden from above
               MOWER('mow7', [RP7[0][1], 0, RP7[0][2]], s=3.0, runAt=0.0, keys=[k(RP7[i - 1][0], to=[RP7[i][1], 0, RP7[i][2]], dur=r(RP7[i][0] - RP7[i - 1][0]), ease='linear') for i in range(1, len(RP7))])],
        cams=[FC(0.0, [0.0, 38.0, 1.2], [[-10.0, 0.0, -10.0], [10.0, 0.0, 10.0], [-10.0, 0.0, 10.0], [10.0, 0.0, -10.0]], top=0.14, bottom=0.8, lenses=range(26, 72))])   # (review 1) steeper: no ground beyond the field
st.cue('sfx:engine', 'S07', 0.0, 0.35)

# 8: the scientists talked about aliens. In a ring: in profile, one scientist scans the sky through head-wide binoculars, the other kneels behind him
#    over the stubble with a big magnifying glass; OVNI ?: both turn to us, the binoculars on us, one eye huge in the glass, and hold
D8 = st.dur('S08'); OV8 = 0.9; S18 = [0.7, 0, 0.0]; S28 = [-0.85, 0, 0.05]
BINO8 = {'touch': {'R': ['face', -0.42, 0.62, 0.2, 1, 0.02], 'L': ['face', 0.42, 0.62, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}
LOUPE8 = lambda ac, up, fr: {'touch': {'R': ['face', ac, up, fr, 1, 0.03]}, 'hands': {'R': 'grip'}}
BIG8 = {'eyeR': 0.9, 'brow': 0.8, 'mouth': 'O'}
st.shot('S08', 'grassland', look=XLOOK, actors=[
        act('savant1', S18, 125, 'stand', 'neutral', keys=[k(0.0, look=[6.0, 9.0, -3.5]), k(0.0, toon={**BINO8, 'bend': {'spine': [-0.28, 0, 0, 1, None]}}, toonDur=0.0),
            k(0.4, look=[5.0, 8.0, -5.5], lookDur=0.3), k(r(OV8 + 0.08), face=165, turn=0.16), k(r(OV8 + 0.08), look='camera', lookDur=0.12),
            k(r(OV8 + 0.1), toon={**BINO8, 'sq': [0.95, 1.07, 0.95]}, toonDur=0.06, toonEase='out'), k(r(OV8 + 0.3), toon=BINO8, toonDur=0.1),
            k(1.75, toon={**BINO8, 'bend': {'spine': [0.14, 0, 0, 1, None]}}, toonDur=0.3, toonEase='inOut'),   # ...and leans toward us behind them
            k(2.08, toon={**BINO8, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'sq': [1.0, 1.02, 1.0]}, toonDur=r(D8 - 2.08), toonEase='inOut')]),   # (final pass) ...and goes on leaning to the cut (the last third of a second was still)
        act('savant2', S28, 125, 'kneelLook', 'neutral', keys=[k(0.0, look=[-0.3, 0.0, -0.35]), k(0.0, toon={**LOUPE8(0.0, 0.05, 0.42), 'face': {'lid': 0.2, 'brow': -0.3}}, toonDur=0.0),
            k(0.4, toon={**LOUPE8(0.0, 0.0, 0.5), 'face': {'lid': 0.2, 'brow': -0.3}}, toonDur=0.3, toonEase='inOut'),
            k(r(OV8 + 0.2), face=180, turn=0.16), k(r(OV8 + 0.2), look='camera', lookDur=0.12),
            k(r(OV8 + 0.24), toon={**LOUPE8(-0.22, -0.03, 0.3), 'face': BIG8, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.1, toonEase='out'), k(r(OV8 + 0.5), toon={**LOUPE8(-0.22, -0.03, 0.3), 'face': BIG8}, toonDur=0.1),
            k(1.9, toon={'face': {**BIG8, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(2.0, toon={'face': BIG8}, toonDur=0.07, keepPose=True),
            k(2.12, toon={'face': BIG8, 'sq': [1.0, 1.025, 1.0]}, toonDur=r(D8 - 2.12), toonEase='inOut', keepPose=True)])],   # (final pass) a breath to the cut
        props=[P('wheat8', 'mowField', pos=[0.0, 0, 3.0], opts={'w': 26.0, 'd': 26.0, 'h': 0.9, 'n': 9000, 'width': 2.0, 'path': [[p_[0] - 5.0, p_[1], p_[2]] for p_ in RP7], 'bw': 0.04, **WHEAT, 'ground': '#C9A646', 'stripCol': '#F2E8BE', 'over': True}),   # the first ring passes under them; gold as from above
               P('bino8', 'binoculars', on={'actor': 'savant1', 'joint': 'head', 'offset': [0.0, 0.33, 0.35]}, scale=3.0),
               P('loupe8', 'magnifier', on={'actor': 'savant2', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'face': 'camera', 'faceFlat': True}, scale=2.2),
               BURST('ovni8', [-0.1, 3.0, 0.2], OV8, 'OVNI ?', 0.75, 0.6)],
        cams=[FC(0.0, [0.3, 2.0, -4.6], [[S18[0], 2.5, 0.0], [1.45, 2.3, 0.0], [S28[0], 0.55, 0.05], [-1.3, 1.2, 0.05], [-0.1, 3.3, 0.2], [S18[0], 0.0, 0.0], [S28[0], 0.0, 0.05]], top=0.12, bottom=0.76)])   # a little above: the wheat in front hides only their shins
st.cue('sfx:sting', 'S08', OV8, 0.3)

# 9: the gendarmerie gave chase. From the lawn, three quarters on the gendarmerie's front: the mower trundles across the lawn toward the left of the frame;
#    when it is two metres past the path the door is slammed flat against the wall and the two gendarmes burst out one after the other, squashed in the
#    doorway, scrambling on the spot, then away after it, half a body apart and one behind the other, their faces to us; the camera drifts left with them
D9 = st.dur('S09'); MZ9 = 0.2; OPEN9 = 0.5; OUT9 = [OPEN9, r(OPEN9 + 0.13)]; SCR9 = 0.14   # (final pass) OUT9: when each appears in the doorway; SCR9: his scramble on the spot (4 frames)
MX9 = lambda t: r(1.0 - 2.85 * t)                                         # the mower's x: at OPEN9 it is 1.5 m past the path (they came out on top of it)
RUNK = lambda: {'face': {'sweat': 1.0, 'brow': -0.6, 'mouth': 'clench'}}
END9 = [[-1.35, 0, 0.2], [0.45, 0, -1.2]]                                   # where each is at the cut: the first on the left and nearer, the second on the right, two metres deeper, both whole in the frame
MID9 = [[-0.5, 0, -1.5], [0.7, 0, -2.4]]                                    # (stills 2) the first veers left as he comes out, the second stays right: seen from the camera they never cross
CF9 = [-2.6, 1.2, 5.2]; CL9 = [0.45, 1.2, -3.0]; DR9 = [-0.35, 0.0, 0.15]      # (stills 1) the camera set by hand (lens 44): the sign at 0.28 of the height, the door in the middle, the mower along the foot of the frame, the gendarmes run up to it
st.shot('S09', 'pavillon', setOpts={'houseColor': '#D8DDE6', 'roof': '#3A4A6A', 'door': '#1F3B73', 'frame': '#1F3B73', 'fence': False, 'mailbox': False}, look=XLOOK, fx=[{'type': 'shake', 'at': OPEN9, 'dur': 0.2, 'amount': 0.014}], actors=[
        *[act(f'gend{j + 1}', [r(0.85 + 0.25 * j), 0, -3.85], 0, 'run', 'angry', keys=[k(0.0, visible=False), k(OUT9[j], visible=True), k(0.0, look=[-2.6, 1.2, 5.2]),
            k(0.0, toon={**RUNK(), 'sq': [1.16, 0.76, 1.16]}, toonDur=0.0),                                                  # squashed in the doorway...
            k(r(OUT9[j] + SCR9), toon={**RUNK(), 'sq': [0.9, 1.13, 0.9]}, toonDur=0.07, toonEase='out'), k(r(OUT9[j] + SCR9 + 0.2), toon=RUNK(), toonDur=0.12),   # ...a stretch as he launches
            k(r(OUT9[j] + SCR9), to=MID9[j], dur=0.3, ease='out', clip='run'),
            k(r(OUT9[j] + SCR9 + 0.3), to=END9[j], dur=r(D9 - OUT9[j] - SCR9 - 0.3), ease='linear', clip='run'),
            k(r(OUT9[j] + SCR9 + 0.2), look=[-5.5, 0.5, 1.5], lookDur=0.1)]) for j in range(2)]],
        props=[P('sign9', 'signBoard', pos=[0.97, 0, -4.0], opts={'text': 'GENDARMERIE', 'w': 2.6, 'h': 0.5, 'height': 2.62, 'bg': '#1F3B73', 'fg': '#FFFFFF', 'frame': '#F4F4F0', 'posts': False}),
               P('door9', 'slamDoor', pos=[0.975, 0, -4.03], opts={'w': 1.0, 'h': 2.05, 'openAt': OPEN9}),   # (final pass) a door that is seen to slam open (the set's stayed shut in every frame)
               P('dust9a', 'dustPuff', pos=[0.95, 0, -3.7], scale=0.8, opts={'once': True, 'startAt': OPEN9, 'period': 0.7, 'seed': 3}),
               P('dust9b', 'dustPuff', pos=[1.1, 0, -3.5], scale=0.7, opts={'once': True, 'startAt': r(OUT9[1] + SCR9), 'period': 0.9, 'seed': 8}),
               P('flag9', 'regionFlag', pos=[2.9, 0, -3.8], opts={'kind': 'fr'}),
               MOWER('mow9', [MX9(0.0), 0, MZ9], ry=-90, runAt=0.0, keys=[k(0.0, to=[MX9(D9), 0, MZ9], dur=D9, ease='linear')])],
        cams=[cam(0.0, CF9, [r(CF9[i] + DR9[i]) for i in range(3)], CL9, [r(CL9[i] + DR9[i]) for i in range(3)], lens=44)])   # (final pass) from the side the mower goes to: their faces three quarters to us all the way, the sign still read
st.cue('clack', 'S09', OPEN9, 0.4); st.cue('sfx:whistle', 'S09', r(OPEN9 + 0.15), 0.3)

# 10: on foot. A long lens down the pavement: the mower trundles toward us; behind it the two gendarmes pump their arms, sweating, tongues out, necks
#     stretched, squashing on each footfall, out of step with each other, and gain nothing (À PIED)
D10 = st.dur('S10')
RUN10 = lambda i=0, j=0: {'face': {'sweat': 1.0, 'brow': 0.9, 'mouth': 'O', 'eye': 0.55, 'tongue': 1, 'tongueLen': 0.34, 'tongueYaw': 1.25 if j else -1.25, 'tongueW': 1.5, 'jaw': 0.5}, 'sq': ([1.08, 0.9, 1.08] if i % 2 == 0 else [0.93, 1.1, 0.93]),   # (final pass) tongueYaw: a pink ribbon blown aside, off the centreline (hanging straight down they read as ties)
                     'bend': {'neck': [0.3 if i % 2 == 0 else -0.08, 0, 0, 1.25 if i % 2 == 0 else 1.55, None]}}
st.shot('S10', 'pavillon', look=XLOOK, actors=[*[act(f'gend{j + 1}', [r(-5.6 + 0.9 * j), 0, r(3.3 + 0.6 * j)], -90, 'run', 'angry', keys=[k(0.0, to=[r(-6.2 + 0.9 * j), 0, r(3.3 + 0.6 * j)], dur=D10, ease='linear', clip='run', face='keep'), k(0.0, look=[-12.0, 0.8, 3.6]), k(0.0, toon=RUN10(j, j), toonDur=0.0),
            *[k(r(0.03 + 0.055 * j + 0.11 * i), toon=RUN10(i + j, j), toonDur=0.05) for i in range(8) if 0.03 + 0.055 * j + 0.11 * i < D10]]) for j in range(2)]],
        props=[MOWER('mow10', [-10.8, 0, 3.6], ry=-90, runAt=0.0, keys=[k(0.0, to=[-11.4, 0, 3.6], dur=D10, ease='linear')])],   # (review 1) five metres ahead: at the lead gendarme's waist it read as pushed
        cams=[FC(0.0, [-16.5, 1.1, 3.9], [[-11.4, 0.0, 3.6], [-5.6, 2.45, 3.3], [-4.7, 2.45, 3.9], [-5.6, 0.0, 3.3], [-5.6, 2.75, 3.3]], top=0.24, bottom=0.76, lenses=range(14, 40))])   # under the À PIED band; (final pass) their caps and stretched necks too (the caps touched the card)
st.cue('sfx:gasp', 'S10', 0.05, 0.3)

# 11: it mowed the lawn of the presidential palace. Pushed in on the palace lawn, its two-tone bands running from the steps to our feet: two helmeted
#     guards stand either side of the last two bands; the mower comes down one between them toward us (the first guard flinches, his eyes after it), leans
#     into a U-turn right in front of us, its handle whipping, and goes back up the other, shaving the second guard: his helmet is knocked askew
D11 = st.dur('S11'); LZ11 = -4.0; LD11 = 11.0; LW11 = 11.2; NB11 = 7
BX11 = lambda i: r(-LW11 / 2 + (i + 0.5) * LW11 / NB11)
PASS11 = [[0.1, 1.0] if i == 3 else [1.1, r(D11 - 0.15)] if i == 4 else [-3.0, -2.0] for i in range(NB11)]   # band 3 (odd: from the far end to the near one), then band 4 (back up)
GZ11 = -2.4; G11 = [[r(BX11(3) - 0.95), 0, GZ11], [r(BX11(4) + 0.78), 0, GZ11]]                                # (final pass) the guards on the lawn, either side of the two bands (at the steps they were 12 % of the frame)
TP11 = [r(0.1 + 0.9 * (GZ11 - (LZ11 - LD11 / 2)) / LD11), r(1.1 + (D11 - 1.25) * ((LZ11 + LD11 / 2) - GZ11) / LD11)]   # when it passes each guard (down band 3, back up band 4)
JOLT11 = lambda t_: [k(r(t_ - 0.04), toon={'sq': [1.1, 0.88, 1.1], 'face': {'pop': 0.35, 'brow': 0.9, 'mouth': 'o'}}, toonDur=0.05), k(r(t_ + 0.1), toon={'sq': [0.94, 1.08, 0.94], 'face': {'pop': 0.35, 'brow': 0.9, 'mouth': 'o'}}, toonDur=0.07, toonEase='out'),
                    k(r(t_ + 0.32), toon={'face': {'brow': 0.5, 'mouth': 'line'}}, toonDur=0.15)]
st.shot('S11', 'grassland', look=XLOOK, actors=[
        act('garde1', G11[0], 12, 'stand', 'neutral', keys=[k(0.0, look=[BX11(3), 0.3, -8.0]), k(0.1, look=[BX11(3), 0.3, r(LZ11 + LD11 / 2)], lookDur=0.9), *JOLT11(TP11[0]),
            k(1.1, look=[BX11(4), 0.3, r(LZ11 - LD11 / 2 + 1.0)], lookDur=r(D11 - 1.25)), k(1.9, toon={'face': {'lid': 1.0}}, toonDur=0.05, keepPose=True), k(2.0, toon={'face': {'brow': 0.5, 'mouth': 'line'}}, toonDur=0.07, keepPose=True),
            k(2.15, toon={'sq': [1.0, 1.02, 1.0]}, toonDur=0.3, toonEase='inOut', keepPose=True)]),
        act('garde2', G11[1], -12, 'stand', 'neutral', keys=[k(0.0, look=[BX11(3), 0.3, -8.0]), k(0.1, look=[BX11(3), 0.3, r(LZ11 + LD11 / 2)], lookDur=0.9),
            k(1.1, look=[BX11(4), 0.3, r(LZ11 - LD11 / 2 + 1.0)], lookDur=r(D11 - 1.25)), *JOLT11(TP11[1]),
            k(r(TP11[1] + 0.5), look='camera', lookDur=0.15), k(2.2, toon={'face': {'lid': 1.0, 'brow': 0.5, 'mouth': 'line'}}, toonDur=0.05, keepPose=True), k(2.3, toon={'face': {'brow': 0.5, 'mouth': 'line'}}, toonDur=0.07, keepPose=True)])],   # shaved: his helmet askew, a look to us
        props=[P('palais11', 'townHall', pos=[0.0, 0, -12.0], opts={'text': 'PALAIS', 'w': 10, 'gable': 'v2'}), COVER('cov11', 10, -12.0), HELMET('hel11a', 'garde1'),
               HELMET('hel11b', 'garde2', keys=[k(TP11[1], attach='garde2', joint='head', offset=[0.13, 0.42, 0.0], rot=[0.0, 0.0, -0.55]), k(TP11[1], squash=[1.12, 0.85, 1.12], dur=0.35)]),
               PLAWN('lawn11', LZ11, LD11, PASS11, w=LW11, n=NB11), PLAWN('lawn11f', r(LZ11 + LD11 / 2 + 3.5), 7.0, w=LW11, n=NB11),   # (final pass) the bands run on to our feet (a flat dark green third under them)
               MOWER('mow11', [BX11(3), 0, r(LZ11 - LD11 / 2)], ry=0, s=1.4, runAt=0.0, whip=[[0.1, 0.6], [1.12, 0.7]], lean=[[0.96, 1.16, -0.5]], keys=[k(0.1, to=[BX11(3), 0, r(LZ11 + LD11 / 2)], dur=0.9, ease='linear'),
                     k(1.0, to=[BX11(4), 0, r(LZ11 + LD11 / 2)], dur=0.1, ease='inOut'), k(1.0, rotTo=[0.0, PI, 0.0], dur=0.1), k(1.1, to=[BX11(4), 0, r(LZ11 - LD11 / 2)], dur=r(D11 - 1.25), ease='linear')])],
        cams=[FC(0.0, [0.9, 1.9, 6.6], [[G11[0][0], 3.15, GZ11], [G11[1][0], 3.15, GZ11], [r(G11[0][0] - 0.45), 1.5, GZ11], [r(G11[1][0] + 0.45), 1.5, GZ11], [BX11(3), 0.0, r(LZ11 + LD11 / 2)], [r(BX11(4) + 0.4), 0.0, r(LZ11 + LD11 / 2)]], top=0.2, bottom=0.82, lenses=range(26, 80))])   # (final pass) pushed in: the guards a third of the frame, the palace behind them, the turn at our feet
st.cue('sfx:engine', 'S11', 0.0, 0.35); st.cue('whoosh', 'S11', TP11[0], 0.2); st.cue('sfx:clink', 'S11', TP11[1], 0.3)

# 12: the president found it very neat. On the striped lawn the president drops to one knee with a squash and sweeps a flat palm across two bands, his
#     eyes ahead of his hand; he pops up with a stretch, smiles at us and his thumb goes up beside his head against the sky: a big skin-coloured fist, a
#     long thumb, a little too far then back, and held; behind him the mower rolls up, stops, and wags like a pleased dog, hopping
D12 = st.dur('S12'); PR12 = [0.0, 0, 0.0]; UP12 = 0.84; TH0 = 0.92                    # UP12: he pops up; TH0: the thumb appears
SM12 = {'mouth': 'bigsmile', 'lid': 0.15, 'brow': 0.4}; LK12 = {'lid': 0.25, 'mouth': 'smile', 'brow': 0.2}
PALM12 = lambda x, z, **o: {'reach': {'R': [x, 0.09, z, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': LK12, **o}
TH12 = lambda x, y, z, **o: {'reach': {'R': [x, y, z, 1, 0.03]}, 'hands': {'R': 'fist'}, 'face': SM12, **o}
THP12 = [-0.52, 2.2, 0.42]                                                              # where the thumb is held: beside his head, on the sky
st.shot('S12', 'grassland', look=XLOOK, actors=[
        act('president', PR12, 20, 'stand', 'happy', keys=[k(0.0, look=[0.5, 0.0, 0.8]), k(0.0, toon={'face': LK12}, toonDur=0.0),
            k(0.04, toon={'face': LK12, 'sq': [1.06, 0.92, 1.06]}, toonDur=0.06),                                     # a dip...
            k(0.1, clip='kneelBow', blend=0.14),                                                                       # ...down on one knee, bent over the grass...
            k(0.22, toon=PALM12(0.3, 0.85, sq=[1.14, 0.84, 1.14]), toonDur=0.07), k(0.32, toon=PALM12(0.3, 0.85), toonDur=0.08),   # ...with a squash, the palm flat on it
            k(0.3, look=[-0.6, 0.0, 0.8], lookDur=0.1),                                                                # his eyes go first...
            k(0.4, toon=PALM12(-0.5, 0.8), toonDur=0.32, toonEase='inOut'),                                            # ...the palm follows, outward, across the edge of two bands (stills 2: reaching across his body laid him flat)
            k(0.76, toon=PALM12(-0.5, 0.8, sq=[1.08, 0.9, 1.08]), toonDur=0.06),
            k(UP12, clip='stand', blend=0.12), k(r(UP12 + 0.04), look='camera', lookDur=0.1),                          # up...
            k(r(UP12 + 0.05), toon=TH12(-0.6, 2.5, 0.46, sq=[0.9, 1.15, 0.9]), toonDur=0.1, toonEase='out'),           # ...with a stretch, the thumb past its place...
            k(r(UP12 + 0.2), toon=TH12(*THP12), toonDur=0.1, toonEase='inOut'),                                         # ...and back: held
            k(1.5, toon=TH12(THP12[0], r(THP12[1] + 0.07), THP12[2], sq=[1.0, 1.02, 1.0]), toonDur=0.18, toonEase='inOut'), k(1.72, toon=TH12(*THP12), toonDur=0.18, toonEase='inOut'),   # a little pump of the thumb
            k(1.9, toon={'face': {**SM12, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(2.0, toon={'face': SM12}, toonDur=0.07, keepPose=True),
            k(2.05, toon={'sq': [1.0, 1.02, 1.0]}, toonDur=r(D12 - 2.05), toonEase='inOut', keepPose=True)])],
        props=[P('lawn12', 'stripePitch', pos=[0.55, 0, -4.0], opts={'w': 11.2, 'd': 16.0, 'n': 7, 'lines': False, 'goals': False, 'over': True, 'passes': [[-3.0, -2.0]] * 7}),   # the bands shifted: an edge between two of them under his palm
               P('palais12', 'townHall', pos=[0.0, 0, -14.0], opts={'text': 'PALAIS', 'w': 12, 'gable': 'v2'}), COVER('cov12', 12, -14.0), P('pin12', 'cockade', on={'actor': 'president', 'joint': 'torso', 'offset': [-0.15, 0.6, 0.17]}),
               P('thumb12', 'bigThumb', on={'actor': 'president', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'face': 'camera', 'faceFlat': True}, scale=0.001, opts={'sleeve': '#A3A8B0'},
                 keys=[k(TH0, scale=1.45, dur=0.1, ease='outBack'), k(1.5, scale=1.6, dur=0.15, ease='inOut'), k(1.72, scale=1.45, dur=0.18, ease='inOut')]),   # (final pass) a thumb that reads: a big fist with a long thumb, turned to the lens (the rig's was a pale cube)
               MOWER('mow12', [3.4, 0, -0.9], ry=-90, runAt=0.0, whip=[[0.0, 0.4], [0.8, -0.5]], wag=[1.05, D12, 0.32], hops=[[1.25, 0.1, 0.2], [1.6, 0.13, 0.2]],
                     keys=[k(0.0, to=[1.35, 0, -0.9], dur=0.8, ease='out')])],   # (final pass) it rolls up behind him, stops, and wags when the thumb goes up (it sat still, spitting grass)
        cams=[FC(0.0, [1.8, 1.3, 3.6], [[0.0, 2.6, 0.0], [0.0, 0.0, 0.0], [1.85, 0.3, -0.9], [1.15, 0.0, 0.7], [-0.75, 2.75, 0.45]], top=0.14, bottom=0.8, lenses=range(26, 68))])   # the thumb beside his head inside the frame, on blue sky
st.cue('sfx:pop', 'S12', TH0, 0.3); st.cue('sfx:boing', 'S12', 1.25, 0.15); st.cue('sfx:boing', 'S12', 1.6, 0.15)

# 13: he named it national gardener. On the striped lawn before the palace the president pins a medal on its handle and steps back to clap; the mower
#     dips its nose: a bow; a helmeted guard salutes (JARDINIÈRE)
D13 = st.dur('S13'); PIN13 = 0.6; MW13 = [0.0, 0, 1.2]   # (stills 1) re-staged: the mower in front of him, its handle toward him, he faces us
SAL13 = {'touch': {'R': ['face', -0.2, 0.47, 0.12, 1, 0.02]}, 'hands': {'R': 'open'}}   # (final pass) the flat hand at the helmet's rim, the elbow out (a straight raised arm read as a wave and hid the end of PALAIS)
st.shot('S13', 'grassland', look=XLOOK, actors=[
        act('president', [-1.1, 0, -0.1], 44, 'stand', 'happy', keys=[k(0.0, look=[-0.5, 0.9, 0.5]), k(0.2, toon={'reach': {'R': [-0.5, 0.97, 0.5, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'smile'}}, toonDur=0.3, toonEase='inOut'),
            k(r(PIN13 + 0.15), look='camera'), *[k(r(PIN13 + 0.2 + 0.14 * i), toon=CLAP(0, i), toonDur=0.05) for i in range(8)]]),
        act('garde1', [1.25, 0, 0.0], -30, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.6, 1.2]), k(0.3, look=[-1.1, 1.9, -0.1], lookDur=0.15), k(0.3, toon={'sq': [1.0, 1.03, 1.0]}, toonDur=0.2, toonEase='inOut'), k(0.62, look=[0.0, 0.9, 1.2], lookDur=0.12),
            k(r(PIN13 + 0.22), toon={'sq': [1.05, 0.94, 1.05]}, toonDur=0.05), k(r(PIN13 + 0.3), toon={**SAL13, 'sq': [0.95, 1.08, 0.95]}, toonDur=0.08, toonEase='out'), k(r(PIN13 + 0.48), toon=SAL13, toonDur=0.1),
            k(1.5, look='camera'), k(1.8, toon={'face': {'lid': 1.0}}, toonDur=0.05, keepPose=True), k(1.9, toon={'face': {}}, toonDur=0.07, keepPose=True), k(2.05, look=[0.6, 0.6, 0.0])])],   # eyes on the medal, a stiff salute at the helmet's rim, a look to us
        props=[MOWER('mow13', MW13, ry=37, runAt=0.0, bowAt=r(PIN13 + 0.3)), P('med13', 'medal', scale=1.6, keys=[k(0.0, attach='mow13', offset=[0.0, 0.92, -0.85]), k(0.0, scale=0.01, dur=0.0), k(PIN13, scale=1.6, dur=0.08, ease='outBack')]),
               # (final pass) the palace further back: its roof flag came down out of the card band
               PLAWN('lawn13', -2.5, 16.0), HELMET('hel13', 'garde1'),
               P('palais13', 'townHall', pos=[0.0, 0, -13.5], opts={'text': 'PALAIS', 'w': 12, 'gable': 'v2'}), COVER('cov13', 12, -13.5), P('flag13', 'regionFlag', pos=[-2.6, 0, -1.2], opts={'kind': 'fr'}), P('pin13', 'cockade', on={'actor': 'president', 'joint': 'torso', 'offset': [-0.15, 0.6, 0.17]})],
        cams=[FC(0.0, [0.9, 1.4, 4.6], [[-1.1, 2.5, -0.1], [0.0, 0.0, 1.2], [1.25, 2.95, 0.0], [0.7, 2.1, -0.2], [1.65, 1.5, 0.0], [-1.1, 0.0, -0.1], [-1.6, 1.5, -0.1]], top=0.2, bottom=0.76, lenses=range(26, 68))])   # (review 2) the guard's helmet, his salute and his elbow inside the frame
st.cue('sfx:clink', 'S13', PIN13, 0.3); st.cue('sfx:fanfare', 'S13', r(PIN13 + 0.25), 0.2)

# 14: it mowed the whole country. From very high: fields and hills, and wide stripes sweeping across them one after another, the mower a dot
D14 = st.dur('S14'); ROWS14 = [r(-75.0 + 12.0 * i) for i in range(12)]   # (review 1) truly high: a patchwork of fields, roads and villages, bands 12 m wide
RP14 = [p_ for i, z_ in enumerate(ROWS14) for p_ in ([[r(0.05 + 1.85 * i / 12), -95.0, z_], [r(0.05 + 1.85 * (i + 1) / 12), 95.0, z_]] if i % 2 == 0 else [[r(0.05 + 1.85 * i / 12), 95.0, z_], [r(0.05 + 1.85 * (i + 1) / 12), -95.0, z_]])]
FIELDS14 = ['#8DBB5A', '#C9B45A', '#6E9E48', '#B8A060', '#A5C46A', '#7FA650', '#D2BC6E', '#94B05A']
VILL14 = [(-55.0, -40.0), (48.0, -58.0), (30.0, 22.0), (-38.0, 35.0)]
st.shot('S14', 'grassland', look=XLOOK, actors=[],
        props=[P('fr14', 'mowFrance', pos=[0.0, 14.0, 0.0], opts={'k': 10.0, 'n': 12, 'from': 0.12, 'to': r(D14 - 0.3)})],   # (stills 2) France itself mowed in stripes, band after band; (review 2) raised 14 m: the set's trees stood in its sea like bushes
        cams=[cam(0.0, [-8.8, 176.0, 22.0], [-8.8, 164.0, 19.0], [-8.8, 14.0, 6.0], [-8.8, 14.0, 6.0], lens=60)])
st.cue('whoosh', 'S14', 0.05, 0.3, 1.8, 200, 1000)

# 15: in three weeks. On his kitchen wall a calendar's days race by, 1 to 21
D15 = st.dur('S15')
st.shot('S15', 'kitchenDay', actors=[],
        props=[P('cal15', 'calendar', pos=[0.0, 1.55, -3.45], scale=1.6, opts={'rate': 24.0, 'start': 0.08, 'last': 20})],   # (review 1) it lands on 21 and holds
        cams=[FC(0.0, [0.4, 1.5, -1.6], [[0.0, 2.0, -3.45], [0.0, 1.1, -3.45], [-0.45, 1.55, -3.45], [0.45, 1.55, -3.45]], top=0.2, bottom=0.78)])
st.cue('sfx:slideUp', 'S15', 0.1, 0.3)

# 16: yesterday it ran out of petrol. Low and close, travelling with it along the pavement: the mower splutters (TEUF... TEUF), coughs black, and stops
#     dead right at his gate (two white posts, the leaf open); a last sigh, it sags flat
D16 = st.dur('S16'); SP16 = [0.6, 1.55]; STOP16 = 1.6; X016 = 4.4; GATE = [0.97, 0, 2.2]
MX16 = lambda t: r(X016 + (0.97 - X016) * min(1.0, t / STOP16))               # (final pass) at a steady speed, so that the camera can travel with it
C16 = lambda x: ([r(x + 0.3), 0.5, 9.0], [r(x + 0.3), 1.07, 3.4])                # 5.6 m from it with a 40 degree lens: the mower and its handle about half the width, the ground under it at three quarters
GATEP = lambda pid: P(pid, 'gardenGate', pos=GATE, opts={'w': 1.3, 'h': 1.25, 'open': 1.95})
st.shot('S16', 'pavillon', look=XLOOK, actors=[],
        props=[MOWER('mow16', [X016, 0, 3.4], ry=-90, runAt=0.0, stopAt=STOP16, sputter=SP16, cough=[1.0, 1.4], slumpAt=r(STOP16 + 0.05), slumpK=0.62, keys=[k(0.0, to=[0.97, 0, 3.4], dur=STOP16, ease='linear')]),   # (review 2) it goes flat like a tyre on the pfff
               GATEP('gate16'),
               BURST('teuf16a', [r(MX16(0.75) + 0.2), 1.3, 3.6], 0.75, 'TEUF', 0.8, 0.2), BURST('teuf16b', [r(MX16(1.2) + 0.1), 1.35, 3.6], 1.2, 'TEUF !', 0.95, 0.2), BURST('pff16', [0.75, 1.25, 3.8], r(STOP16 + 0.12), 'pfff...', 0.7, 0.35)],   # (stills 1) twice the size
        cams=[cam(0.0, C16(X016)[0], C16(0.97)[0], C16(X016)[1], C16(0.97)[1], lens=40), cam(STOP16, C16(0.97)[0], C16(0.97)[0], C16(0.97)[1], C16(0.97)[1], lens=40)])   # (final pass) it was a third of the width over a flat empty third of green
st.cue('sfx:rattle', 'S16', SP16[0], 0.35); st.cue('sfx:rattleShort', 'S16', 1.0, 0.3); st.cue('sfx:poof', 'S16', 1.4, 0.3)

# 17: right in front of his house. Wider: the mower dead at his open gate; behind the gate, on his garden path between tall grass, he stands with a big
#     white mug of coffee that steams, looks at it, then at us, a blink, a breath
D17 = st.dur('S17'); ME17 = [0.97, 0, 0.9]
MUG17 = lambda **o: {'touch': {'R': ['torso', -0.27, 0.3, 0.4, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD, **o}   # (final pass) the mug held off his chest, white on the navy jacket
st.shot('S17', 'pavillon', look=XLOOK, actors=[act('mec', ME17, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[0.97, 0.3, 3.4]), k(0.0, toon=MUG17(), toonDur=0.0),
            k(0.1, toon=MUG17(sq=[1.0, 1.018, 1.0]), toonDur=0.3, toonEase='inOut'), k(0.5, look='camera', lookDur=0.14), k(0.5, toon=MUG17(), toonDur=0.2, toonEase='inOut'),
            k(0.8, toon=MUG17(face={'lid': 1.0}), toonDur=0.06), k(0.92, toon=MUG17(), toonDur=0.08),
            k(1.0, toon=MUG17(sq=[1.0, 1.02, 1.0]), toonDur=r(D17 - 1.0), toonEase='inOut')])],   # (final pass) he breathes to the cut
        props=[LAWNF('lawn17', 0.85, STRIPE), P('lawn17b', 'mowField', pos=[3.2, 0, -0.9], opts={'w': 3.0, 'd': 5.8, 'h': 0.85, 'n': 1400}), HEDGEP('hedge17', -5.0), GATEP('gate17'),
               MOWER('mow17', [0.97, 0, 3.4], ry=-90, dead=True, slumpK=0.62), P('mug17', 'steamMug', scale=1.5, on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'face': 'camera', 'faceFlat': True})],   # (final pass) big, white, steaming (the small teal mug was hidden in his fist)
        cams=[FC(0.0, [0.97, 1.5, 5.6], [[ME17[0], 2.45, ME17[2]], [ME17[0], 0.9, ME17[2]], [0.97, 0.0, 3.4], [0.2, 0.0, 3.4], [1.7, 0.0, 3.4]], top=0.14, bottom=0.7)])   # (review 2) the dead mower above the caption band

# 18: he put it back in the garage. In front of the little garage, facing us, deadpan: a wind-up, the knee up, and he kicks the dead mower beside him into
#     the garage without a look (TOC: it skids in and bumps the back wall); he reaches up behind him and pulls the door down: BANG, the garage squashes, dust;
#     his shoulders jump; two quick claps to dust off his hands, a puff at each, and he looks at us
D18 = st.dur('S18'); GAR = [4.6, 0, -3.6]; ME18 = [3.95, 0, -2.7]; KICK18 = 0.15; BUMP18 = 0.44; CLOSE18 = 0.58; BANG18 = r(CLOSE18 + 0.25); MW18 = [4.75, 0, -3.15]
LEG18 = lambda bx, bz=0.0, ln=1.0, **o: {'bend': {'legL': [bx, bz, 0, ln, None], 'shinL': [0.2, r(0.4 * bz), 0, ln, None], **o.pop('bend', {})}, 'face': DEAD, **o}   # the leg's far end swung back (bx) and toward +X (bz), stretched
HANDS18 = [3.95, 1.38, -2.25]
CLAP18 = lambda i: {'touch': {'R': ['torso', r(-0.03 if i % 2 else -0.26), 0.5, 0.42, 1, 0.02], 'L': ['torso', r(0.03 if i % 2 else 0.26), 0.5, 0.42, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': DEAD}   # at the chest (at the height of S13's they hid his face)
st.shot('S18', 'pavillon', look=XLOOK, fx=[{'type': 'shake', 'at': BANG18, 'dur': 0.2, 'amount': 0.016}], actors=[act('mec', ME18, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.0, clip='windUp', params={'dur': 0.11}, blend=0.02), k(0.0, toon={'face': DEAD}, toonDur=0.0),                                                                    # a wind-up: the knee up, the arms wound (stills 2: the leg bent like a hose did not show from the front)...
            k(KICK18, clip='stand', blend=0.05), k(KICK18, toon=LEG18(0.35, 0.95, 1.25, sq=[0.97, 1.05, 0.97]), toonDur=0.04, toonEase='out'), k(r(KICK18 + 0.12), toon=LEG18(0.35, 0.95, 1.25), toonDur=0.04),   # ...and the leg is thrown out and back at the mower: it shoots in
            k(0.3, toon={'face': DEAD}, toonDur=0.12, toonEase='inOut'),
            k(r(CLOSE18 - 0.2), toon={'reach': {'R': [4.25, 2.1, -3.5, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.16, toonEase='inOut'),                           # the hand up behind him to the door...
            k(r(CLOSE18 + 0.02), toon={'reach': {'R': [4.25, 1.25, -3.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.18, toonEase='in'),                    # ...and down: BANG
            k(r(BANG18 + 0.01), toon={'face': {'lid': 1.0}, 'sq': [0.95, 1.07, 0.95]}, toonDur=0.04), k(r(BANG18 + 0.14), toon={'face': DEAD}, toonDur=0.1),                         # his shoulders jump, his eyes shut
            *[k(r(1.0 + 0.07 * i), toon=CLAP18(i + 1), toonDur=0.04) for i in range(4)],                                                                          # two quick claps: he dusts off his hands
            k(1.3, toon={'face': DEAD}, toonDur=0.14, toonEase='inOut'), k(1.4, toon={'face': DEAD, 'sq': [1.0, 1.02, 1.0]}, toonDur=r(D18 - 1.4), toonEase='inOut')])],
        props=[P('gar18', 'garageShed', pos=GAR, opts={'w': 2.4, 'd': 3.0, 'h': 2.3, 'closeAt': CLOSE18}, keys=[k(BANG18, squash=[1.07, 0.88, 1.07], dur=0.3)]),
               MOWER('mow18', MW18, ry=180, dead=True, slumpK=0.62, keys=[k(KICK18, to=[4.9, 0, -5.95], dur=r(BUMP18 - KICK18), ease='out'), k(BUMP18, squash=[1.25, 0.8, 0.7], dur=0.25), k(BUMP18, to=[4.9, 0, -5.75], dur=0.12, ease='out')]),
               BURST('bang18', [4.9, 2.95, -3.2], BANG18, 'BANG !', 1.0, 0.45), BURST('toc18', [4.85, 0.75, -2.8], KICK18, 'TOC', 0.55, 0.16),
               P('dust18a', 'dustPuff', pos=[4.3, 0, -3.45], scale=0.5, opts={'once': True, 'startAt': BANG18, 'period': 0.34, 'seed': 5}), P('dust18b', 'dustPuff', pos=[5.3, 0, -3.45], scale=0.5, opts={'once': True, 'startAt': BANG18, 'period': 0.38, 'seed': 11}),
               P('dust18c', 'dustPuff', pos=HANDS18, scale=0.3, opts={'once': True, 'startAt': 1.07, 'period': 0.3, 'seed': 21}), P('dust18d', 'dustPuff', pos=HANDS18, scale=0.3, opts={'once': True, 'startAt': 1.21, 'period': 0.3, 'seed': 23})],
        cams=[FC(0.0, [5.3, 1.35, 1.6], [[3.4, 2.55, -3.6], [5.8, 2.55, -3.6], [ME18[0], 2.5, ME18[2]], [ME18[0], 0.0, ME18[2]], [5.3, 0.0, -2.6], [4.9, 3.3, -3.2], [3.5, 1.2, -2.7]], top=0.12, bottom=0.76, lenses=range(26, 72))])   # (final pass) from the front: his face to us all the way (his back was to us until the claps)
st.cue('thud', 'S18', KICK18, 0.3); st.cue('thud', 'S18', BUMP18, 0.2); st.cue('clang', 'S18', BANG18, 0.45); st.cue('sfx:click', 'S18', 1.07, 0.22); st.cue('sfx:click', 'S18', 1.21, 0.22)

# 19: his garden still isn't mowed. His front lawn waist-high, the one pale stripe across it from the first day, seen from above; he stands in it,
#     deadpan, looking at us; a gnome pops up beside him, its hat rocking; a beat; his head goes down to it; a beat; back to us; a slow blink; the end hold
D19 = st.dur('S19'); ME19 = [-1.4, 0, -0.4]; GN19 = [-0.62, 0.0, -0.3]; POP19 = 0.6   # (review 1) in the one stripe from the first day
ST19 = {'width': 1.1, 'stripCol': '#D6EDA6', 'cutCol': '#C6E392', 'short': 0.06}   # (review 2) a wide pale trench that reads before the gnome pops
st.shot('S19', 'pavillon', setOpts={'fence': False, 'mailbox': False}, look=XLOOK, actors=[act('mec', ME19, 10, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.2, toon={'face': DEAD, 'sq': [1.0, 1.018, 1.0]}, toonDur=0.2, toonEase='inOut'), k(0.42, toon={'face': DEAD}, toonDur=0.15, toonEase='inOut'),
            k(r(POP19 + 0.5), look=[GN19[0], 0.85, GN19[2]], lookDur=0.16),                                 # (final pass) the gnome first; half a second later his head goes down to it...
            k(r(POP19 + 0.62), toon={'face': {'lid': 0.3, 'brow': 0.25}}, toonDur=0.1),
            k(r(POP19 + 1.1), look='camera', lookDur=0.18), k(r(POP19 + 1.15), toon={'face': DEAD}, toonDur=0.12),   # ...half a second more, and back to us
            k(2.1, toon={'face': {'lid': 1.0}}, toonDur=0.12, toonEase='inOut'), k(2.34, toon={'face': DEAD}, toonDur=0.12, toonEase='inOut'),   # a slow blink
            k(2.4, toon={'face': DEAD, 'sq': [1.0, 1.02, 1.0]}, toonDur=r(D19 - 2.4), toonEase='inOut')])],
        props=[LAWNF('lawn19', 0.8, STRIPE, **ST19), P('lawn19b', 'mowField', pos=[3.2, 0, -0.9], opts={'w': 3.0, 'd': 5.8, 'h': 0.8, 'n': 1400}), HEDGEP('hedge19', -5.0),
               P('gnome19', 'gnome', pos=GN19, ry=-15, opts={'s': 1.55, 'popAt': POP19, 'wobble': 0.5})],   # (review 2) in the stripe beside him, whole, at his hand's height; (final pass) its hat rocks to the end
        cams=[FC(0.0, [-0.6, 4.2, 2.2], [[ME19[0], 2.45, ME19[2]], [ME19[0], 0.0, ME19[2]], [-2.7, 0.0, -0.4], [GN19[0], 1.0, GN19[2]], [0.1, 0.0, -0.4]], top=0.14, bottom=0.72, lenses=range(26, 76))])   # (review 2) higher: we look down into the stripe, him in it
st.cue('sfx:pop', 'S19', POP19, 0.2)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("La tondeuse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'voisin': {'preset': 'pyjama', 'seed': 701, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'joueur1': {'suit': '#2F62B5', 'preset': 'footballeur', 'outfit': 'tracksuit', 'skin': '#AF8F7A', 'gloves': '#7A5038', 'seed': 702, 'faceRim': True, 'pants': '#F4F4F0', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'joueur2': {'suit': '#2F62B5', 'preset': 'footballeur', 'outfit': 'tracksuit', 'skin': '#B6957F', 'gloves': '#845840', 'seed': 703, 'faceRim': True, 'pants': '#F4F4F0', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'joueur3': {'suit': '#2F62B5', 'preset': 'footballeur', 'outfit': 'tracksuit', 'skin': '#A88972', 'gloves': '#704832', 'seed': 704, 'faceRim': True, 'pants': '#F4F4F0', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'arbitre': {'preset': 'sportif', 'seed': 705, 'suit': '#16181C', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant1': {'preset': 'savant', 'seed': 706, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant2': {'preset': 'savant', 'seed': 707, 'hairColor': '#8A6A4A', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'gend1': {'preset': 'cop', 'seed': 708, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'gend2': {'preset': 'cop', 'seed': 709, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 710, 'suit': '#A3A8B0', 'lapel': '#A3A8B0', 'tie': '#2F62B5', 'hairColor': '#EFEFEF', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.05}, 'toon': EX},
    'garde1': {'preset': 'officiel', 'seed': 711, 'suit': '#1F2A44', 'lapel': '#1F2A44', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'garde2': {'preset': 'officiel', 'seed': 712, 'suit': '#1F2A44', 'lapel': '#1F2A44', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
})
