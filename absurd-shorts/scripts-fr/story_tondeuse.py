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
LAWN = [-2.5, 0, -0.9]; M0 = [-0.1, 0, -0.4]; ME0 = [1.0, 0, -0.4]; HEDGE = [-5.5, 0, -1.0]
LOC = lambda x, z: [r(x - LAWN[0]), r(z - LAWN[2])]   # world x, z in the lawn field's frame
LAWNF = lambda pid, h, path: P(pid, 'mowField', pos=LAWN, opts={'w': 5.4, 'd': 5.8, 'h': h, 'n': 2600, 'width': 0.6, 'path': path, 'stripCol': '#9FCF6E'})
HEDGEP = lambda pid, hole_at=None: P(pid, 'hedgeWall', pos=HEDGE, ry=90, opts={'l': 6.0, 'h': 1.45, 'holeX': -0.6, 'burstDir': -1, **({'holeAt': hole_at} if hole_at is not None else {})})
STRIPE = [[-1.0, *LOC(M0[0], M0[2])], [-0.01, *LOC(-5.6, M0[2])]]   # the one stripe across his lawn, already cut in the later shots

for g_ in [('S01', 1.2, 'mec', 'pull'), ('S03', 0.9, 'voisin', 'feet'), ('S05', 0.8, 'joueur1', 'clap'), ('S08', 1.0, 'savant1', 'ovni'), ('S10', 0.5, 'gend1', 'run'),
           ('S12', 1.6, 'president', 'thumb'), ('S13', 1.2, 'president', 'medal'), ('S17', 0.8, 'mec', 'mug'), ('S19', 1.4, 'mec', 'end')]:
    st.gag(*g_)
st.card('S07', 'CERCLES', at=0.5)
st.card('S10', 'À PIED', at=0.1)
st.card('S13', 'JARDINIÈRE', at=0.4)

# 1: the hook. His overgrown front lawn, the red push mower: he pulls the starter cord: a cough; again: a cough; a third time: it catches with a jolt and
#    sets off on its own across the lawn, mowing; his hand stays up, deadpan
D1 = st.dur('S01'); START1 = 1.15
PULL = lambda x, y, z: {'reach': {'R': [r(x), r(y), r(z), 1, 0.03], 'L': [0.75, 0.98, -0.6, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': DEAD}
CORD = [0.65, 0.86, -0.28]                                             # the cord's handle on the mower's handle (world)
st.shot('S01', 'pavillon', look=XLOOK, actors=[
        act('mec', ME0, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[M0[0], 0.4, M0[2]]), k(0.0, toon=PULL(*CORD), toonDur=0.0),
            *[kk for j, t_ in enumerate((0.18, 0.62, 1.05)) for kk in (k(t_, toon={**PULL(r(1.42 + 0.12 * j), r(1.45 + 0.15 * j), -0.32), 'bend': {'spine': [r(0.12 + 0.05 * j), 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.08, toonEase='out'),
                k(r(t_ + 0.24), toon=PULL(*CORD), toonDur=0.12, toonEase='inOut'))],   # (review 1) three pulls, bigger each time: the arm thrown back and up, the body leaning back
            k(r(START1 + 0.12), toon={**PULL(1.55, 1.95, -0.32), 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.06), k(r(START1 + 0.45), look='camera', lookDur=0.25)])],   # it catches and yanks his arm up: the hand stays there, a look to us
        props=[LAWNF('lawn1', 0.55, [[START1, *LOC(M0[0], M0[2])], [D1, *LOC(-2.6, M0[2])]]), HEDGEP('hedge1'),
               MOWER('mow1', M0, runAt=START1, cough=[0.3, 0.75, START1], startAt=START1, keys=[k(r(START1 + 0.05), to=[-2.6, 0, M0[2]], dur=r(D1 - START1 - 0.05), ease='in')])],
        tethers=[{'a': {'prop': 'mow1', 'offset': [0.12, 0.86, -0.75]}, 'b': {'actor': 'mec', 'hand': 'R'}, 'color': '#111111', 'radius': 0.018, 'radial': 6, 'sag': 0.02, 'n': 8, 'from': 0.15, 'snap': [START1, 0.12, 0.2]}],   # (review 1) a cord that reads
        cams=[FC(0.0, [-1.2, 1.35, 3.0], [[ME0[0], 2.45, ME0[2]], [ME0[0], 0.4, ME0[2]], [1.75, 2.0, -0.35], [1.6, 1.0, -0.4], [-1.2, 0.0, -0.4], [-1.2, 0.9, -0.4]], top=0.14, bottom=0.78)])   # (review 1) his thrown-back arm inside the frame
st.cue('sfx:zip', 'S01', 0.18, 0.25); st.cue('sfx:rattleShort', 'S01', 0.3, 0.3); st.cue('sfx:zip', 'S01', 0.62, 0.25); st.cue('sfx:rattleShort', 'S01', 0.75, 0.3); st.cue('sfx:engine', 'S01', START1, 0.45)

# 2: it never stopped. Wide over his lawn: the mower runs on alone, a clean stripe behind it, and bursts through the hedge into the neighbour's garden,
#    leaves flying; he watches it go, then looks at us
D2 = st.dur('S02'); HOLE2 = 0.9
st.shot('S02', 'pavillon', look=XLOOK, actors=[act('mec', ME0, -15, 'stand', 'unimpressed', keys=[k(0.0, look=[-3.5, 0.4, M0[2]]), k(0.0, toon={'reach': {'R': [1.161, 1.25, -0.616, 1, 0.03], 'L': [0.742, 0.98, -0.21, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': DEAD}, toonDur=0.0),   # body to us, head after the mower (the S01 hold turned with him)
            k(0.5, toon={'reach': {'R': [1.161, 1.1, -0.616, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.3, toonEase='inOut'), k(r(HOLE2 + 0.05), look=[-5.5, 0.6, M0[2]]), k(1.25, look='camera'),
            k(1.45, toon={'face': {'lid': 1.0}}, toonDur=0.06), k(1.57, toon={'face': DEAD}, toonDur=0.08)])],
        props=[LAWNF('lawn2', 0.55, [[-1.0, *LOC(M0[0], M0[2])], [0.0, *LOC(-2.6, M0[2])], [HOLE2, *LOC(-5.6, M0[2])]]), HEDGEP('hedge2', HOLE2),
               MOWER('mow2', [-2.6, 0, M0[2]], runAt=0.0, keys=[k(0.0, to=[-5.6, 0, M0[2]], dur=HOLE2, ease='linear'), k(HOLE2, to=[-8.6, 0, M0[2]], dur=r(D2 - HOLE2), ease='linear')])],
        cams=[FC(0.0, [2.7, 1.8, 1.5], [[ME0[0], 2.45, ME0[2]], [ME0[0], 0.0, ME0[2]], [-5.5, 1.5, -1.5], [-5.5, 0.0, 0.6]], top=0.14, bottom=0.76, lenses=range(26, 74))])   # inside the garden: the mailbox by the gate filled the foreground
st.cue('sfx:engine', 'S02', 0.0, 0.4); st.cue('sfx:crunch', 'S02', HOLE2, 0.35)

# 3: it mowed the neighbour's garden. Next door: the neighbour in pyjamas dozes in his deckchair with his paper; the mower bursts through the hedge,
#    passes under his lifted feet (the paper flies up), knocks the hat off his gnome and goes on
D3 = st.dur('S03'); HOLE3 = 0.2; FEET3 = 0.85; GN3 = [-2.75, 0, 1.05]   # (review 1) the gnome beside his chair, inside the frame
VX3 = lambda t: r(1.5 - 3.9 * t)                                         # the mower's x: 3.9 m/s
SIT3 = lambda up, eye=0.0: {'bend': {'legL': [r(-1.1 * up), 0, 0, 1, None], 'legR': [r(-1.1 * up), 0, 0, 1, None]}, 'face': {'lid': r(0.5 * (1 - up)), 'eye': eye, 'brow': r(0.9 * up), 'mouth': 'O' if up > 0.5 else 'line'}}
st.shot('S03', 'pavillon', setOpts={**HOUSE_N, 'fence': False, 'mailbox': False}, look=XLOOK, actors=[
        act('voisin', [-1.8, 0, 0.25], 0, 'sit', 'neutral', keys=[k(0.0, look=[-1.8, 0.9, 1.2]), k(0.0, toon=SIT3(0.0), toonDur=0.0),
            k(0.55, look=[1.0, 0.4, 1.0]), k(0.62, toon=SIT3(1.0, 0.6), toonDur=0.08, toonEase='out'), k(r(FEET3 + 0.25), toon=SIT3(0.0, 0.4), toonDur=0.2, toonEase='inOut'),   # (feet up as it passes under them)
            k(r(FEET3 + 0.3), look=[-5.0, 0.4, 1.0]), k(1.6, look='camera')])],
        props=[P('lawn3', 'mowField', pos=[-2.0, 0, -0.6], opts={'w': 6.4, 'd': 5.6, 'h': 0.18, 'n': 2200, 'width': 0.6, 'path': [[0.0, 3.5, 1.6], [D3, r(VX3(D3) + 2.0), 1.6]], 'stripCol': '#9FCF6E'}),
               P('hedge3', 'hedgeWall', pos=[0.6, 0, -1.0], ry=90, opts={'l': 6.0, 'h': 1.45, 'holeX': -2.0, 'burstDir': -1, 'holeAt': HOLE3}),
               P('chair3', 'deckChair', pos=[-1.8, 0, 0.05]), P('gnome3', 'gnome', pos=GN3, ry=20, opts={'s': 0.9, 'trimAt': r((1.5 - GN3[0]) / 3.9)}),
               P('paper3', 'newspaper', on={'actor': 'voisin', 'hand': 'R', 'offset': [0.05, 0.0, 0.05]}, keys=[k(0.62, detach=True, fall=True, toss=[0.2, 2.2, 0.4], spinFall=8.0)]),
               MOWER('mow3', [VX3(0.0), 0, 1.0], runAt=0.0, keys=[k(0.0, to=[VX3(D3), 0, 1.0], dur=D3, ease='linear')])],
        cams=[FC(0.0, [-1.0, 1.05, 3.1], [[-1.8, 1.9, 0.25], [-1.8, 0.0, 1.2], [GN3[0], 1.2, GN3[2]], [-0.2, 0.6, 1.0]], top=0.2, bottom=0.78)])   # (review 1) the neighbour fills the frame, the gnome's hat in it   # no fence: from low behind it the mower and the feet were hidden
st.cue('sfx:crunch', 'S03', HOLE3, 0.3); st.cue('sfx:engine', 'S03', 0.1, 0.35); st.cue('sfx:gasp', 'S03', 0.62, 0.25); st.cue('sfx:pop', 'S03', r((1.5 - GN3[0]) / 3.9), 0.25)

# 4: then the football stadium. From the stands: the mower runs up and down the pitch so fast it is a blur, and perfect stripes appear one after another;
#    the players at the touchline turn their heads to follow it
D4 = st.dur('S04'); PASS4 = 0.16; W4 = 34.0; D4P = 52.0; NS4 = 8
XS4 = lambda i: r(-W4 / 2 + (i + 0.5) * W4 / NS4)
PASSES4 = [[r(0.05 + PASS4 * i), r(0.05 + PASS4 * (i + 1))] for i in range(NS4)]
MK4 = [kk for i in range(NS4) for kk in (k(PASSES4[i][0], to=[XS4(i), 0, (1 if i % 2 == 0 else -1) * D4P / 2], dur=0.0), k(PASSES4[i][0], to=[XS4(i), 0, (-1 if i % 2 == 0 else 1) * D4P / 2], dur=PASS4, ease='linear'),
                                      k(PASSES4[i][0], rotTo=[0.0, 0.0 if i % 2 else PI, 0.0], dur=0.0))]
st.shot('S04', 'grassland', look=XLOOK, actors=[*[act(f'joueur{j + 1}', [r(-4.2 + 4.2 * j), 0, r(D4P / 2 + 2.6 + 0.5 * (j % 2))], 180, 'stand', 'neutral',
            keys=[k(0.0, look=[XS4(0), 0.3, 0.0]), *[k(PASSES4[i][0], look=[XS4(i), 0.3, (-12.0 if i % 2 == 0 else 12.0)], lookDur=0.08) for i in range(1, NS4)]]) for j in range(3)]],   # (review 1) heads whipping after it
        props=[P('pitch4', 'stripePitch', opts={'w': W4, 'd': D4P, 'n': NS4, 'passes': PASSES4}), P('stands4', 'bleachers', pos=[-W4 / 2 - 4.0, 0, 0], ry=90, opts={'l': 60, 'rows': 7}),
               P('stands4b', 'bleachers', pos=[W4 / 2 + 4.0, 0, 0], ry=-90, opts={'l': 60, 'rows': 7}), MOWER('mow4', [XS4(0), 0, D4P / 2], ry=180, s=4.0, runAt=0.0, speedLines=True, keys=MK4)],
        cams=[FC(0.0, [1.0, 6.5, 40.0], [[-8.0, 0.0, 14.0], [8.0, 0.0, 14.0], [0.0, 2.44, -D4P / 2], [0.0, 2.45, D4P / 2 + 2.6]], top=0.12, bottom=0.86, lenses=range(26, 80))])   # (review 1) low behind the players: the pitch, its lines and the stripes fill the frame
st.cue('whoosh', 'S04', 0.05, 0.3, 1.2, 300, 1500); st.cue('sfx:engine', 'S04', 0.0, 0.4)

# 5: the players applauded. At the touchline three players and the referee clap, the striped pitch gleaming behind them
D5 = st.dur('S05')
CLAP = lambda j, i: {'touch': {'R': ['torso', r(-0.03 if i % 2 else -0.24), 0.8, 0.38, 1, 0.02], 'L': ['torso', r(0.03 if i % 2 else 0.24), 0.8, 0.38, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': 0.1}}   # (review 1) at the chin, wide apart between claps (at the chest they read as praying)
st.shot('S05', 'grassland', look=XLOOK, actors=[*[act(f'joueur{j + 1}', [[-1.25, 0, 0.1], [0.05, 0, -0.55], [1.15, 0, 0.35]][j], [18, -4, -20][j], 'stand', 'happy', keys=[k(0.0, look='camera'), *[k(r(0.07 * j + (0.12 + 0.02 * j) * i), toon=CLAP(j, i), toonDur=0.05) for i in range(11)]]) for j in range(3)],
        act('arbitre', [2.0, 0, -0.4], -20, 'stand', 'neutral', keys=[k(0.0, look='camera'), *[k(r(0.04 + 0.15 * i), toon=CLAP(3, i), toonDur=0.05) for i in range(10)]])],
        props=[P('pitch5', 'stripePitch', pos=[0.0, 0, -20.0], ry=90, opts={'w': W4, 'd': D4P, 'n': NS4, 'passes': [[-2.0, -1.0]] * NS4})],   # (review 1) turned: the goals out of the frame, no crossbar through their heads
        cams=[FC(0.0, [0.4, 1.5, 4.6], [[-1.3, 2.45, 0.0], [2.3, 2.45, -0.4], [0.5, 0.9, 0.0]], top=0.18, bottom=0.78)])
for i in range(10): st.cue('sfx:click', 'S05', r(0.04 + 0.15 * i), 0.22)   # the claps of the referee, one click each (the mix has no applause)

# 6: it went through the forest in a straight line. Low in the forest: the mower comes straight at us; the trees in its way fall left and right as it
#    reaches them, a line of stumps behind it
D6 = st.dur('S06'); Z06 = -15.0; V6 = 7.0   # (stills 2) closer at the start: from -22 it showed only after the trees in its way had fallen
TREES6 = [-13.2, -11.0, -8.8, -6.6, -4.4, -2.2]   # (review 1) one falling every 0.3 s, left and right
st.shot('S06', 'grassland', look=XLOOK, actors=[],
        props=[*[P(f'ft6{i}', 'fallTree', pos=[0.0, 0, z_], opts={'s': 1.3, 'seed': i, 'dir': (PI / 2 if i % 2 else -PI / 2), 'fallAt': r((z_ - Z06) / V6)}) for i, z_ in enumerate(TREES6)],
               *[P(f'tr6{i}', 'fallTree', pos=[r((2.6 + 1.2 * (i % 3)) * (1 if i % 2 else -1)), 0, r(-2.0 - 2.6 * i)], opts={'s': r(1.1 + 0.25 * (i % 3)), 'seed': i + 9}) for i in range(10)],
               MOWER('mow6', [0.0, 0, Z06], ry=0, s=2.0, runAt=0.0, keys=[k(0.0, to=[0.0, 0, r(Z06 + V6 * D6)], dur=D6, ease='linear')])],
        cams=[cam(0.0, [0.0, 6.5, r(Z06 - 6.0)], [0.0, 6.5, r(Z06 + V6 * D6 - 6.0)], [0.0, 0.0, r(Z06 + 4.0)], [0.0, 0.0, r(Z06 + V6 * D6 + 4.0)], lens=52)])   # (stills 2b) higher and further back, above the treetops: the mower in the lower third, the trees ahead falling aside (at 4.2 m it sat below the frame among the trunks)   # (stills 2) chasing it from behind and above: the trees ahead fall aside as it reaches them (from in front they hid it)   # (review 1) high enough to see it between the trees from the first frame   # off the axis and higher: behind the trees in its way the mower was hidden
for i, z_ in enumerate(TREES6): st.cue('sfx:crunch', 'S06', r((z_ - Z06) / V6), 0.25)

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

# 8: the scientists talked about aliens. In the rings: one scientist peers at the sky through binoculars, the other kneels over the stubble with a
#    magnifying glass; OVNI ?
D8 = st.dur('S08'); OV8 = 0.9
st.shot('S08', 'grassland', look=XLOOK, actors=[
        act('savant1', [3.0, 0, 0.5], 200, 'stand', 'neutral', keys=[k(0.0, look=[1.0, 12.0, -8.0]), k(1.55, look='camera'), k(2.15, look=[1.0, 12.0, -8.0]),   # the binoculars on us, then back to the sky k(0.0, toon={'touch': {'R': ['face', -0.05, 0.17, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.17, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [-0.25, 0, 0, 1, None]}}, toonDur=0.0),
            k(r(OV8 - 0.1), toon={'touch': {'R': ['face', -0.05, 0.17, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.17, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [-0.3, 0, 0, 1, None]}, 'face': {'eye': 0.5, 'brow': 0.9}}, toonDur=0.1)]),
        act('savant2', [1.6, 0, -0.9], 160, 'kneelLook', 'neutral', keys=[k(0.0, look=[1.9, 0.0, -0.2]), k(r(OV8 + 0.2), look='camera'), k(r(OV8 + 0.2), toon={'face': {'eye': 0.5, 'brow': 0.8, 'mouth': 'O'}}, toonDur=0.1)])],
        props=[P('wheat8', 'mowField', opts={'w': 26.0, 'd': 26.0, 'h': 0.9, 'n': 6000, 'width': 1.1, 'path': [[p_[0] - 5.0, p_[1], p_[2]] for p_ in RP7], 'bw': 0.035, **WHEAT}),
               P('bino8', 'binoculars', on={'actor': 'savant1', 'hand': 'R', 'offset': [0.04, 0.02, 0.06]}), P('loupe8', 'magnifier', on={'actor': 'savant2', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}),
               BURST('ovni8', [2.2, 2.9, 0.4], OV8, 'OVNI ?', 0.75, 0.45)],
        cams=[FC(0.0, [2.3, 1.3, -4.6], [[3.0, 2.45, 0.5], [1.6, 0.35, -0.9], [2.2, 3.2, 0.4], [3.0, 0.4, 0.5]], top=0.12, bottom=0.9)])   # cut at the shins; (stills 1) from in front of them: from behind we saw two backs
st.cue('sfx:sting', 'S08', OV8, 0.3)

# 9: the gendarmerie gave chase. A gendarmerie in a pavillon: the mower trundles past along the pavement, slowly; two gendarmes burst out of the door and
#    run after it
D9 = st.dur('S09')
RUNK = lambda: {'face': {'sweat': 1.0, 'brow': -0.6, 'mouth': 'clench'}}
st.shot('S09', 'pavillon', setOpts={'houseColor': '#D8DDE6', 'roof': '#3A4A6A', 'door': '#1F3B73', 'frame': '#1F3B73'}, look=XLOOK, actors=[
        *[act(f'gend{j + 1}', [r(0.8 + 0.55 * j), 0, r(0.7 - 0.45 * j)], 0, 'stand', 'angry', keys=[k(0.0, look=[2.6, 0.5, 3.6]), k(r(0.35 + 0.12 * j), to=[r(-1.2 + 0.7 * j), 0, r(3.0 + 0.35 * j)], dur=r(D9 - 0.45 - 0.12 * j), ease='in', clip='run'),
            k(r(0.35 + 0.12 * j), look=[-3.0, 0.5, 3.6], lookDur=0.1), k(0.0, toon=RUNK(), toonDur=0.0)]) for j in range(2)]],   # (review 1) out of the door and after it, the same way it goes
        props=[P('sign9', 'signBoard', pos=[0.0, 0, -4.0], opts={'text': 'GENDARMERIE', 'w': 2.6, 'h': 0.5, 'height': 2.25, 'bg': '#1F3B73', 'fg': '#FFFFFF', 'frame': '#F4F4F0', 'posts': False}),
               P('flag9', 'regionFlag', pos=[2.6, 0, -3.8], opts={'kind': 'fr'}),
               MOWER('mow9', [3.4, 0, 3.6], ry=-90, runAt=0.0, keys=[k(0.0, to=[-2.8, 0, 3.6], dur=D9, ease='linear')])],
        cams=[FC(0.0, [0.6, 1.5, 10.5], [[0.97, 2.45, 0.6], [3.4, 0.0, 3.6], [-2.8, 0.0, 3.6], [-1.4, 2.7, -4.0], [1.4, 2.7, -4.0]], top=0.12, bottom=0.8)])   # (review 1) front on: everything runs screen-left; the whole GENDARMERIE sign   # closer: the gendarmes were specks at the door
st.cue('clack', 'S09', 0.05, 0.3); st.cue('sfx:whistle', 'S09', 0.4, 0.3)

# 10: on foot. A long lens down the pavement: the mower trundles toward us; behind it the two gendarmes pump their arms, sweating, tongues out, and gain
#     nothing (À PIED)
D10 = st.dur('S10')
RUN10 = lambda: {'face': {'sweat': 1.0, 'brow': 0.9, 'mouth': 'O', 'eye': 0.55}}   # (review 1) gasping, eyes wide (they looked content)
st.shot('S10', 'pavillon', look=XLOOK, actors=[*[act(f'gend{j + 1}', [r(-5.6 + 0.9 * j), 0, r(3.3 + 0.6 * j)], -90, 'run', 'angry', keys=[k(0.0, to=[r(-6.2 + 0.9 * j), 0, r(3.3 + 0.6 * j)], dur=D10, ease='linear', clip='run', face='keep'), k(0.0, look=[-12.0, 0.8, 3.6]), k(0.0, toon=RUN10(), toonDur=0.0)]) for j in range(2)]],
        props=[MOWER('mow10', [-10.8, 0, 3.6], ry=-90, runAt=0.0, keys=[k(0.0, to=[-11.4, 0, 3.6], dur=D10, ease='linear')])],   # (review 1) five metres ahead: at the lead gendarme's waist it read as pushed
        cams=[FC(0.0, [-16.5, 1.1, 3.9], [[-11.4, 0.0, 3.6], [-5.6, 2.45, 3.3], [-4.7, 2.45, 3.9], [-5.6, 0.0, 3.3]], top=0.21, bottom=0.76, lenses=range(14, 40))])   # under the À PIED band
st.cue('sfx:gasp', 'S10', 0.05, 0.3)

# 11: it mowed the lawn of the presidential palace. The palace, its flag, a great lawn: the mower finishes the last bands of a perfect striped lawn, the
#     guards at the steps watching
D11 = st.dur('S11'); ROWS11 = [-4.5, -3.0, -1.5, 0.0, 1.5, 3.0, 4.5]
def ROWPATH(rows, half, t_first, t_done, t_end):   # back and forth along x; the rows before the last two already cut (negative times)
    pts, n = [], len(rows)
    for i, z_ in enumerate(rows):
        a, b = (-half, half) if i % 2 == 0 else (half, -half)
        ta = t_first + (t_done - t_first) * i / (n - 2) if i < n - 2 else t_done + (t_end - t_done) * (i - (n - 2)) / 2
        tb = t_first + (t_done - t_first) * (i + 1) / (n - 2) if i < n - 3 else t_done + (t_end - t_done) * (i + 1 - (n - 2)) / 2
        pts += [[r(ta), a, z_], [r(tb), b, z_]]
    return pts
RP11 = ROWPATH(ROWS11, 4.6, -3.0, 0.1, r(D11 - 0.2))
st.shot('S11', 'grassland', look=XLOOK, actors=[*[act(f'garde{j + 1}', [r(-2.6 + 5.2 * j), 0, 4.6], 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 12.0]), k(r(0.5 + 0.3 * j), look=[r(-3.0 + 6.0 * j), 0.3, 1.5], lookDur=0.2), k(1.4, look=[4.5, 0.3, 1.5], lookDur=0.2)]) for j in range(2)]],   # (review 1) the two guards at attention framing the shot
        props=[P('palais11', 'townHall', pos=[0.0, 0, -12.0], opts={'text': 'PALAIS', 'w': 10, 'gable': 'v2'}),
               P('lawn11', 'mowField', pos=[0.0, 0, -3.0], opts={'w': 10.0, 'd': 10.5, 'h': 0.22, 'n': 4000, 'width': 1.5, 'path': RP11, 'stripCols': STRIPES, 'short': 0.25}),
               MOWER('mow11', [RP11[10][1], 0, r(RP11[10][2] - 3.0)], ry=90, s=1.4, runAt=0.0, keys=[k(RP11[j - 1][0], to=[RP11[j][1], 0, r(RP11[j][2] - 3.0)], dur=r(max(0.01, RP11[j][0] - RP11[j - 1][0])), ease='linear') for j in range(11, len(RP11))])],
        cams=[FC(0.0, [0.4, 3.4, 11.5], [[-2.6, 2.4, 4.6], [2.6, 2.4, 4.6], [-2.6, 0.0, 4.6], [-4.2, 6.6, -12.0], [4.2, 6.6, -12.0]], top=0.12, bottom=0.8, lenses=range(26, 74))])   # closer: the palace and its stripes were small
st.cue('sfx:engine', 'S11', 0.0, 0.35)

# 12: the president found it very neat. On the lawn the president kneels and runs his hand over the stripes, gets up, smiles: thumb up
D12 = st.dur('S12'); PR12 = [0.0, 0, 0.0]
st.shot('S12', 'grassland', look=XLOOK, actors=[
        act('president', PR12, 20, 'kneelLook', 'happy', keys=[k(0.0, look=[0.4, 0.0, 0.7]), k(0.0, toon={'reach': {'R': [0.2, 0.08, 0.7, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(0.35, toon={'reach': {'R': [0.55, 0.08, 0.6, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.3, toonEase='inOut'),   # his hand over the stripes...
            k(0.95, clip='stand'), k(1.05, look='camera'), k(1.3, toon={'reach': {'R': [-0.2, 2.15, 0.42, 1, 0.03]}, 'hands': {'R': 'thumbUp'}, 'face': {'mouth': 'bigsmile', 'lid': 0.15, 'brow': 0.4}}, toonDur=0.15, toonEase='out')])],   # (review 1) up beside his face, against the sky   # ...up, thumb up
        props=[P('lawn12', 'mowField', pos=[0.0, 0, -1.0], opts={'w': 10.0, 'd': 8.0, 'h': 0.22, 'n': 2600, 'width': 1.5, 'path': [[-1.0, -5.0, z_] if j % 2 == 0 else [-1.0, 5.0, z_] for j, z_ in enumerate([-3.0, -1.5, 0.0, 1.5, 3.0])], 'stripCols': STRIPES, 'short': 0.25}),
               P('palais12', 'townHall', pos=[0.0, 0, -14.0], opts={'text': 'PALAIS', 'w': 12, 'gable': 'v2'}), P('pin12', 'cockade', on={'actor': 'president', 'joint': 'torso', 'offset': [-0.15, 0.6, 0.17]}),
               MOWER('mow12', [1.4, 0, -0.4], ry=-60, runAt=0.0)],
        cams=[FC(0.0, [1.8, 1.3, 3.6], [[0.0, 2.5, 0.0], [0.0, 0.0, 0.0], [1.6, 0.0, -0.4], [0.6, 0.0, 0.8]], top=0.16, bottom=0.8)])

# 13: he named it national gardener. On the palace steps the president pins a medal on its handle and steps back to clap; the mower dips its nose: a bow;
#     a guard salutes (JARDINIÈRE)
D13 = st.dur('S13'); PIN13 = 0.6; MW13 = [0.0, 0, 1.2]   # (stills 1) re-staged: the mower in front of him, its handle toward him, he faces us
st.shot('S13', 'grassland', look=XLOOK, actors=[
        act('president', [-1.1, 0, -0.1], 44, 'stand', 'happy', keys=[k(0.0, look=[-0.5, 0.9, 0.5]), k(0.2, toon={'reach': {'R': [-0.5, 0.97, 0.5, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'smile'}}, toonDur=0.3, toonEase='inOut'),
            k(r(PIN13 + 0.15), look='camera'), *[k(r(PIN13 + 0.2 + 0.14 * i), toon=CLAP(0, i), toonDur=0.05) for i in range(8)]]),
        act('garde1', [1.5, 0, 0.0], -30, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.6, 1.2]), k(r(PIN13 + 0.3), toon={'touch': {'R': ['face', -0.14, 0.2, 0.1, 1, 0.02]}, 'hands': {'R': 'open'}}, toonDur=0.12, toonEase='out'), k(1.5, look='camera'), k(2.05, look=[0.6, 0.6, 0.0])])],   # a salute, a look to us
        props=[MOWER('mow13', MW13, ry=37, runAt=0.0, bowAt=r(PIN13 + 0.3)), P('med13', 'medal', scale=1.6, keys=[k(0.0, attach='mow13', offset=[0.0, 0.92, -0.85]), k(0.0, scale=0.01, dur=0.0), k(PIN13, scale=1.6, dur=0.08, ease='outBack')]),
               P('palais13', 'townHall', pos=[0.0, 0, -9.0], opts={'text': 'PALAIS', 'w': 12, 'gable': 'v2'}), P('flag13', 'regionFlag', pos=[-2.6, 0, -1.2], opts={'kind': 'fr'}), P('pin13', 'cockade', on={'actor': 'president', 'joint': 'torso', 'offset': [-0.15, 0.6, 0.17]})],
        cams=[FC(0.0, [0.9, 1.4, 4.6], [[-1.1, 2.5, -0.1], [0.0, 0.0, 1.2], [1.5, 2.45, 0.0], [-1.1, 0.0, -0.1]], top=0.2, bottom=0.76)])   # (review 1) the guard beside, not behind the president
st.cue('sfx:clink', 'S13', PIN13, 0.3); st.cue('sfx:fanfare', 'S13', r(PIN13 + 0.25), 0.2)

# 14: it mowed the whole country. From very high: fields and hills, and wide stripes sweeping across them one after another, the mower a dot
D14 = st.dur('S14'); ROWS14 = [r(-75.0 + 12.0 * i) for i in range(12)]   # (review 1) truly high: a patchwork of fields, roads and villages, bands 12 m wide
RP14 = [p_ for i, z_ in enumerate(ROWS14) for p_ in ([[r(0.05 + 1.85 * i / 12), -95.0, z_], [r(0.05 + 1.85 * (i + 1) / 12), 95.0, z_]] if i % 2 == 0 else [[r(0.05 + 1.85 * i / 12), 95.0, z_], [r(0.05 + 1.85 * (i + 1) / 12), -95.0, z_]])]
FIELDS14 = ['#8DBB5A', '#C9B45A', '#6E9E48', '#B8A060', '#A5C46A', '#7FA650', '#D2BC6E', '#94B05A']
VILL14 = [(-55.0, -40.0), (48.0, -58.0), (30.0, 22.0), (-38.0, 35.0)]
st.shot('S14', 'grassland', look=XLOOK, actors=[],
        props=[P('fr14', 'mowFrance', pos=[0.0, 0, 0.0], opts={'k': 10.0, 'n': 12, 'from': 0.12, 'to': r(D14 - 0.3)})],   # (stills 2) France itself mowed in stripes, band after band (the patchwork read as pale blocks)
        cams=[cam(0.0, [-8.8, 162.0, 22.0], [-8.8, 150.0, 19.0], [-8.8, 0.0, 6.0], [-8.8, 0.0, 6.0], lens=60)])
st.cue('whoosh', 'S14', 0.05, 0.3, 1.8, 200, 1000)

# 15: in three weeks. On his kitchen wall a calendar's days race by, 1 to 21
D15 = st.dur('S15')
st.shot('S15', 'kitchenDay', actors=[],
        props=[P('cal15', 'calendar', pos=[0.0, 1.55, -3.45], scale=1.6, opts={'rate': 24.0, 'start': 0.08, 'last': 20})],   # (review 1) it lands on 21 and holds
        cams=[FC(0.0, [0.4, 1.5, -1.6], [[0.0, 2.0, -3.45], [0.0, 1.1, -3.45], [-0.45, 1.55, -3.45], [0.45, 1.55, -3.45]], top=0.2, bottom=0.78)])
st.cue('sfx:slideUp', 'S15', 0.1, 0.3)

# 16: yesterday it ran out of petrol. Low by his gate: the mower comes along the pavement, splutters (TEUF... TEUF), coughs black, and stops dead right at his
#     gate; a last sigh, it sags
D16 = st.dur('S16'); SP16 = [0.6, 1.55]; STOP16 = 1.6
st.shot('S16', 'pavillon', look=XLOOK, actors=[],
        props=[MOWER('mow16', [6.0, 0, 3.4], ry=-90, runAt=0.0, stopAt=STOP16, sputter=SP16, cough=[1.0, 1.4], slumpAt=r(STOP16 + 0.05), keys=[k(0.0, to=[0.97, 0, 3.4], dur=STOP16, ease='out')]),
               BURST('teuf16a', [3.0, 1.25, 3.6], 0.75, 'TEUF', 0.8, 0.2), BURST('teuf16b', [1.8, 1.3, 3.6], 1.2, 'TEUF !', 0.95, 0.2), BURST('pff16', [0.7, 1.2, 3.8], r(STOP16 + 0.12), 'pfff...', 0.7, 0.35)],   # (stills 1) twice the size
        cams=[FC(0.0, [-0.2, 0.55, 6.8], [[0.97, 0.0, 3.4], [3.6, 0.0, 3.4], [0.97, 1.4, 2.2], [3.0, 1.4, 3.6]], top=0.16, bottom=0.82)])   # (review 1) its handle clear of the mailbox
st.cue('sfx:rattle', 'S16', SP16[0], 0.35); st.cue('sfx:rattleShort', 'S16', 1.0, 0.3); st.cue('sfx:poof', 'S16', 1.4, 0.3)

# 17: right in front of his house. Wider: the mower dead at his gate; behind the gate, on his garden path between tall grass, he stands with his coffee
#     mug, looks at it, then at us
D17 = st.dur('S17'); ME17 = [0.97, 0, 0.9]
st.shot('S17', 'pavillon', look=XLOOK, actors=[act('mec', ME17, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[0.97, 0.3, 3.4]), k(0.0, toon={'touch': {'R': ['torso', -0.12, 0.5, 0.32, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0),
            k(0.3, toon={'touch': {'R': ['torso', -0.12, 0.5, 0.32, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD, 'sq': [1.0, 1.015, 1.0]}, toonDur=0.25, toonEase='inOut'), k(0.55, look='camera'), k(0.85, toon={'touch': {'R': ['torso', -0.12, 0.5, 0.32, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0}}, toonDur=0.06), k(0.97, toon={'touch': {'R': ['torso', -0.12, 0.5, 0.32, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.08)])],
        props=[LAWNF('lawn17', 0.85, STRIPE), P('lawn17b', 'mowField', pos=[3.2, 0, -0.9], opts={'w': 3.0, 'd': 5.8, 'h': 0.85, 'n': 1400}), HEDGEP('hedge17', -5.0),
               MOWER('mow17', [0.97, 0, 3.4], ry=-90, dead=True), P('mug17', 'mug', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.02, 0.04]})],
        cams=[FC(0.0, [0.97, 1.5, 5.6], [[ME17[0], 2.45, ME17[2]], [ME17[0], 0.9, ME17[2]], [0.97, 0.0, 3.4], [0.2, 0.0, 3.4], [1.7, 0.0, 3.4]], top=0.14, bottom=0.78)])   # (review 1) closer: his face and the mug read

# 18: he put it back in the garage. By the house: he gives it a shove into the little garage, reaches up and pulls the door down (BANG), dusts off his hands
D18 = st.dur('S18'); GAR = [4.6, 0, -3.6]; CLOSE18 = 0.85
st.shot('S18', 'pavillon', look=XLOOK, actors=[act('mec', [4.6, 0, -1.9], 180, 'stand', 'unimpressed', keys=[k(0.0, look=[4.6, 0.4, -3.0]),
            k(0.0, toon={'reach': {'R': [4.4, 0.98, -2.55, 1, 0.03], 'L': [4.8, 0.98, -2.55, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': DEAD}, toonDur=0.0),
            k(0.18, toon={'reach': {'R': [4.45, 1.0, -2.95, 1, 0.03], 'L': [4.75, 1.0, -2.95, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.08, toonEase='out'),   # a shove...
            k(r(CLOSE18 - 0.25), toon={'reach': {'R': [4.6, 2.05, -3.55, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.15, toonEase='inOut'),   # ...up to the door...
            k(r(CLOSE18 + 0.05), toon={'reach': {'R': [4.6, 1.2, -3.45, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3}}, toonDur=0.12, toonEase='in'),   # ...down: BANG
            k(1.02, face=40, turn=0.2), k(1.15, look='camera'), *[k(r(1.25 + 0.1 * i), toon=CLAP(0, i), toonDur=0.04) for i in range(3)]])],   # turns round to us, dusts off his hands
        props=[P('gar18', 'garageShed', pos=GAR, opts={'w': 2.4, 'd': 3.0, 'h': 2.3, 'closeAt': CLOSE18}), MOWER('mow18', [4.6, 0, -2.85], ry=180, dead=True, keys=[k(0.2, to=[4.6, 0, -5.2], dur=0.5, ease='out')])],
        cams=[FC(0.0, [6.9, 1.55, 0.6], [[4.6, 2.45, -1.9], [4.6, 0.0, -1.9], [3.4, 2.5, -3.6], [5.8, 0.0, -3.6]], top=0.14, bottom=0.75)])
st.cue('thud', 'S18', 0.2, 0.25); st.cue('clang', 'S18', r(CLOSE18 + 0.25), 0.4)

# 19: his garden still isn't mowed. His front lawn waist-high, the one stripe across it from the first day; he stands in the grass, deadpan, looks at us;
#     a gnome pops up beside him and looks at us too; a blink; the end hold
D19 = st.dur('S19'); ME19 = [-1.4, 0, -0.4]   # (review 1) in the one stripe from the first day
st.shot('S19', 'pavillon', setOpts={'fence': False, 'mailbox': False}, look=XLOOK, actors=[act('mec', ME19, 10, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.6, look=[-3.5, 0.5, -0.4]), k(1.0, look='camera'), k(1.7, toon={'face': {'lid': 1.0}}, toonDur=0.12, toonEase='inOut'), k(1.95, toon={'face': DEAD}, toonDur=0.12, toonEase='inOut')])],
        props=[LAWNF('lawn19', 0.95, STRIPE), P('lawn19b', 'mowField', pos=[3.2, 0, -0.9], opts={'w': 3.0, 'd': 5.8, 'h': 0.95, 'n': 1400}), HEDGEP('hedge19', -5.0),
               P('gnome19', 'gnome', pos=[-0.72, 0.42, -0.15], ry=-15, opts={'s': 1.55, 'popAt': 1.05})],   # (review 1) bigger, standing in the grass: its head and hat above it, at his hand's height
        cams=[FC(0.0, [-0.2, 2.25, 2.9], [[ME19[0], 2.45, ME19[2]], [ME19[0], 0.4, ME19[2]], [-3.6, 0.0, -0.4], [-0.72, 1.45, -0.15], [-0.4, 0.95, 0.4]], top=0.14, bottom=0.74)])   # (review 1) from above: the trench of the stripe reads, him in it   # (stills 2) closer: him and the gnome   # no fence: the pickets hid the gnome and his legs
st.cue('sfx:pop', 'S19', 1.05, 0.2)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("La tondeuse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'voisin': {'preset': 'pyjama', 'seed': 701, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'joueur1': {'suit': '#2F62B5', 'preset': 'footballeur', 'seed': 702, 'faceRim': True, 'pants': '#F4F4F0', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'joueur2': {'suit': '#2F62B5', 'preset': 'footballeur', 'seed': 703, 'faceRim': True, 'pants': '#F4F4F0', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'joueur3': {'suit': '#2F62B5', 'preset': 'footballeur', 'seed': 704, 'faceRim': True, 'pants': '#F4F4F0', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'arbitre': {'preset': 'sportif', 'seed': 705, 'suit': '#16181C', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant1': {'preset': 'savant', 'seed': 706, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant2': {'preset': 'savant', 'seed': 707, 'hairColor': '#8A6A4A', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'gend1': {'preset': 'cop', 'seed': 708, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'gend2': {'preset': 'cop', 'seed': 709, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 710, 'suit': '#A3A8B0', 'lapel': '#A3A8B0', 'tie': '#2F62B5', 'hairColor': '#EFEFEF', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.05}, 'toon': EX},
    'garde1': {'preset': 'officiel', 'seed': 711, 'suit': '#1F2A44', 'lapel': '#1F2A44', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'garde2': {'preset': 'officiel', 'seed': 712, 'suit': '#1F2A44', 'lapel': '#1F2A44', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
})
