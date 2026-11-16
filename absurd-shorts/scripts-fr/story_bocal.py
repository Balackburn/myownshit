#!/usr/bin/env python3
"""Le bocal (story 78, cycle 40; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man couldn't open a jar of pickles. He tapped the lid with a spoon. He held it under hot water. He called the fire brigade. They brought out the
big jaws. The jaws broke. The army sent a tank. The tank drove over it. The tank got a flat. It was sent into space. Six astronauts tried. The
scientists fired a laser. The laser bounced back. The jar became a historic monument. Then his grandmother came by. She opened it with one hand.
He doesn't like pickles.
Staging: in his kitchen he strains at the lid, red in the face, until his hand slips off; a spoon taps the lid and bends; steam under the hot tap;
a fire engine pulls up, two firemen clamp the hydraulic jaws on the lid, the jaws snap and fly apart (CASSÉ); a tank comes down his street, rolls
over the jar on the road and bounces, then sags on a flat track (CREVÉ); a rocket lifts off; six astronauts in a space module pull the lid in
zero gravity and spin like tops; a scientist fires a laser, it bounces off the jar's glint and frizzes his hair; the jar in a museum display case,
MONUMENT HISTORIQUE (HISTORIQUE), visitors and a guard; his grandmother comes in with her handbag, lifts the glass and opens it with one hand: POP;
he holds the open jar, looks in, looks at us, deadpan.
Natural look; cycle 40: props_bocal.js (picklesJar, rescueJaws, spaceHelmet, displayCase); armyTank, rocket, laserBeam, fireTruck reused.
(pass 3, after review 2) props_bocal.js: bigJaws, bendSpoon, battleTank, toonPuff, spaceWindow, laserCannon, hexNut, camFlash, roadPebbles, labGoggles.
Lessons applied from the start: every toon key carries the pose of what the hands hold (a key replaces the whole pose); camera-facing goes in the
attach; the key props get inserts that fill the frame."""
from story_kit import *
import math

st = Story('bocal', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 18)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
def loc(p, ry, v, s=1.0):
    """(pass 3) the world position of the local point v of a prop standing at p, turned ry degrees about Y and scaled s"""
    a_ = math.radians(ry); return [r(p[0] + s * (v[0] * math.cos(a_) + v[2] * math.sin(a_))), r(p[1] + s * v[1]), r(p[2] + s * (-v[0] * math.sin(a_) + v[2] * math.cos(a_)))]
def bodyPt(feet, ry, pitch, roll, h):
    """(pass 3) where the point h metres up an actor's own axis is: feet [x, y, z], heading ry in degrees, 'lay' [pitch, roll] in radians (the engine
    turns the actor Y, then X, then Z about his feet): the hips of a man who leans back, the head of one who floats upside down"""
    y_ = math.radians(ry); x, yy, z = -math.sin(roll) * h, math.cos(roll) * math.cos(pitch) * h, math.cos(roll) * math.sin(pitch) * h
    return [r(feet[0] + x * math.cos(y_) + z * math.sin(y_)), r(feet[1] + yy), r(feet[2] - x * math.sin(y_) + z * math.cos(y_))]
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
LIP = {'lid': 0.45, 'mouth': 'line'}
STREET = {'eiffelStyle': 'v2', 'clear': [-6.0, 6.0], 'clearL': [-6.0, 6.0]}
MUSEE = {'desk': False, 'banner': False, 'map': False, 'plate': 'MUSÉE'}

JS = 1.4; JH = r(0.204 * JS)                         # the jar's scale and the height of its lid above its base
TABLE = [0.0, 0, -1.2]; TH = 0.76                   # his kitchen table
MEK = [0.0, 0, -1.85]                               # him behind it, facing us

for g_ in [('S01', 1.6, 'mec', 'strain'), ('S06', 0.32, 'pompier1', 'snap'), ('S13', 0.45, 'savant1', 'burnt'), ('S16', 0.45, 'mamie', 'pop'), ('S17', 1.3, 'mec', 'end')]:
    st.gag(*g_)
st.card('S06', 'CASSÉ', at=0.35)
st.card('S09', 'CREVÉ', at=0.3)
st.card('S14', 'HISTORIQUE', at=0.6)

# 1: the hook. His kitchen, close: he holds the jar against his belly and twists the lid with all he has: five strains, his body squashing, his
#    face going red, a vein, sweat; then his hand slips off the lid and flies up, he staggers back; a look at the jar
D1 = st.dur('S01'); SLIP1 = 2.15; JAR1 = [0.0, 1.22, -1.45]
GRIP1 = lambda a=0.0, dy=0.0: {'reach': {'L': [r(JAR1[0] + 0.1), r(JAR1[1] + 0.12), r(JAR1[2] + 0.03), 1, 0.03], 'R': [r(JAR1[0] - 0.02 + 0.035 * math.cos(a)), r(JAR1[1] + JH + 0.01 + dy), r(JAR1[2] + 0.035 * math.sin(a)), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}}
STRAIN1 = [0.3, 0.68, 1.06, 1.44, 1.82]
K1 = [k(0.0, look=[JAR1[0], r(JAR1[1] + JH), JAR1[2]]), k(0.0, toon={**GRIP1(), 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'mouth': 'clench', 'brow': -0.5}}, toonDur=0.0)]
for i, t_ in enumerate(STRAIN1):
    p = (i + 1) / len(STRAIN1)
    K1 += [k(t_, toon={**GRIP1(1.2 * (i + 1)), 'bend': {'spine': [r(0.16 + 0.04 * p), r(0.06 if i % 2 else -0.06), 0, 1, None]}, 'sq': [r(1.06 + 0.03 * p), r(0.92 - 0.03 * p), r(1.06 + 0.03 * p)],
                         'face': {'lid': r(0.6 + 0.3 * p), 'mouth': 'clench', 'brow': -0.9, 'cheeks': r(0.4 + 0.6 * p), 'blush': r(min(1.0, 1.2 * p)), 'vein': r(p), 'sweat': 1.0 if p > 0.5 else 0.0}}, toonDur=0.08, toonEase='out'),
           k(r(t_ + 0.18), toon={**GRIP1(1.2 * (i + 1) + 0.6), 'bend': {'spine': [0.14, 0, 0, 1, None]}, 'sq': [0.98, 1.03, 0.98],
                                'face': {'lid': r(0.5 + 0.3 * p), 'mouth': 'clench', 'brow': -0.8, 'cheeks': r(0.3 + 0.5 * p), 'blush': r(min(1.0, 1.2 * p)), 'vein': r(p), 'sweat': 1.0 if p > 0.5 else 0.0}}, toonDur=0.12)]
K1 += [k(SLIP1, toon={'reach': {'L': GRIP1()['reach']['L'], 'R': [r(JAR1[0] - 0.5), 2.05, r(JAR1[2] + 0.25), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'spread'}, 'lay': [-0.16, 0.08], 'sq': [0.92, 1.1, 0.92],
                    'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0, 'blush': 1.0}}, toonDur=0.05, toonEase='out'),   # the hand slips off: it flies up, he staggers
       k(r(SLIP1 + 0.07), toon={'reach': {'L': GRIP1()['reach']['L'], 'R': [r(JAR1[0] - 0.55), 2.25, r(JAR1[2] + 0.3), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'spread'}, 'lay': [-0.2, 0.1], 'sq': [0.88, 1.14, 0.88],
                    'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0, 'blush': 1.0}}, toonDur=0.05, toonEase='out'),   # (review 1) the overshoot...
       k(r(SLIP1 + 0.17), toon={'reach': {'L': GRIP1()['reach']['L'], 'R': [r(JAR1[0] - 0.42), 1.85, r(JAR1[2] + 0.22), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'spread'}, 'lay': [0.08, -0.06], 'sq': [1.04, 0.96, 1.04],
                    'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.8, 'blush': 0.9}}, toonDur=0.08),   # ...and a wobble forward
       k(r(SLIP1 + 0.3), toon={'reach': {'L': GRIP1()['reach']['L'], 'R': [r(JAR1[0] - 0.3), 1.45, r(JAR1[2] + 0.15), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'rest'}, 'lay': [0.0, 0.0], 'face': {'lid': 0.45, 'mouth': 'line', 'blush': 0.6}}, toonDur=0.2)]
st.shot('S01', 'kitchenDay', actors=[act('mec', MEK, 0, 'stand', 'determined', keys=K1)],
        props=[P('jar1', 'picklesJar', pos=JAR1, scale=JS, opts={'shake': [[0.3, 2.1]]})],
        cams=[FC(0.0, [0.55, 1.25, 0.45], [[0.0, 2.38, -1.85], [0.0, 0.95, -1.85], [r(JAR1[0] - 0.25), JAR1[1], JAR1[2]], [r(JAR1[0] + 0.3), r(JAR1[1] + 0.4), JAR1[2]], [-0.6, 2.0, -1.6]], top=0.12, bottom=0.76)])
for t_ in STRAIN1: st.cue('sfx:squeak', 'S01', t_, 0.14)
st.cue('whoosh', 'S01', SLIP1, 0.3, 0.25, 1500, 500)

# 2: he tapped the lid with a spoon. Low by the jar on the table, the jar big in front of him: a big spoon hanging bowl-down from his hand taps the
#    lid, a small tink, a bigger tink, then an overhead wind-up, held, and the blow: the spoon folds at a right angle and the shock runs up his arm
#    to his head; he lifts the bent spoon between the jar and his face, looks at it, then at us (review 2: the spoon never folded)
D2 = st.dur('S02'); JAR2 = [0.0, TH, -1.25]; LIDTOP2 = r(TH + 0.218 * JS); TAPS2 = [0.3, 0.62]; HIT2 = 1.22; WIND2 = 0.4; SPX = 0.04
GRIPY = lambda dy: r(LIDTOP2 + 0.45 + dy)                     # the spoon (0.45 m, hanging bowl down) touches the lid when its grip is at GRIPY(0)
SPOON2 = lambda dy, f, x=SPX, **kw: {'reach': {'R': [x, GRIPY(dy), -1.25, 1, 0.03], 'L': [0.11, r(TH + 0.12), -1.22, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f, **kw}
K2 = [k(0.0, look=[JAR2[0], r(TH + JH), JAR2[2]]), k(0.0, toon=SPOON2(0.1, {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}), toonDur=0.0)]
KS2 = []
for t_, up, sqz in ((TAPS2[0], 0.08, 1.0), (TAPS2[1], 0.2, 1.03)):
    K2 += [k(r(t_ - 0.13), toon=SPOON2(up, {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}), toonDur=0.09, toonEase='out'), k(r(t_ - 0.04), toon=SPOON2(0.0, {'lid': 0.5, 'mouth': 'line', 'brow': -0.5}, sq=[sqz, r(2 - sqz), sqz]), toonDur=0.04, toonEase='in')]
    KS2 += [k(r(t_ - 0.13), to=[SPX, GRIPY(up), -1.25], dur=0.09, ease='out'), k(r(t_ - 0.04), to=[SPX, GRIPY(0.0), -1.25], dur=0.04, ease='in')]
K2 += [k(0.72, toon=SPOON2(WIND2, {'lid': 0.3, 'mouth': 'clench', 'brow': -0.8}, x=-0.06, sq=[0.94, 1.08, 0.94], bend={'spine': [-0.12, 0, 0, 1, None]}), toonDur=0.22, toonEase='out'),   # the wind-up: up over his shoulder, a stretch...
       k(0.96, toon=SPOON2(r(WIND2 + 0.07), {'lid': 0.3, 'mouth': 'clench', 'brow': -0.9, 'vein': 1.0}, x=-0.08, sq=[0.92, 1.1, 0.92], bend={'spine': [-0.16, 0, 0, 1, None]}), toonDur=0.2),   # ...held
       k(r(HIT2 - 0.06), toon=SPOON2(0.0, {'lid': 0.7, 'mouth': 'clench', 'brow': -1.0}, sq=[1.1, 0.88, 1.1], bend={'spine': [0.2, 0, 0, 1, None]}), toonDur=0.06, toonEase='in')]   # the blow
for i, dt in enumerate((0.04, 0.08, 0.12, 0.16, 0.2)):   # the shock runs up his arm to his head
    K2.append(k(r(HIT2 + dt), toon=SPOON2(0.0, {'lid': 0.0, 'eye': 0.5, 'mouth': 'wavy', 'brow': 0.8}, lay=[0.0, r(0.06 * (-1) ** i * (1 - i / 6))], sq=[r(1.0 + 0.05 * (-1) ** i), r(1.0 - 0.05 * (-1) ** i), 1.0], hairUp=0.5), toonDur=0.03))
K2 += [k(r(HIT2 + 0.28), look=[r(SPX + 0.12), r(LIDTOP2 + 0.5), -1.25], lookDur=0.1),
       k(r(HIT2 + 0.3), toon=SPOON2(0.32, {'lid': 0.1, 'mouth': 'line', 'brow': 0.5}), toonDur=0.18, toonEase='out'),   # he lifts it between the jar and his face: bent at a right angle
       k(r(HIT2 + 0.72), look='camera', lookDur=0.12), k(r(HIT2 + 0.76), toon=SPOON2(0.32, {'lid': 0.5, 'mouth': 'line', 'brow': -0.1}), toonDur=0.1),
       k(r(HIT2 + 0.93), toon=SPOON2(0.32, {'lid': 1.0, 'mouth': 'line'}), toonDur=0.06), k(r(HIT2 + 1.03), toon=SPOON2(0.32, {'lid': 0.5, 'mouth': 'line'}), toonDur=0.08)]
KS2 += [k(0.72, to=[-0.06, GRIPY(WIND2), -1.25], dur=0.22, ease='out'), k(0.72, rotTo=[0.0, 0.0, 2.2], dur=0.22, ease='out'), k(0.96, to=[-0.08, GRIPY(WIND2 + 0.07), -1.25], dur=0.2), k(0.96, rotTo=[0.0, 0.0, 2.45], dur=0.2),
        k(r(HIT2 - 0.06), to=[SPX, GRIPY(0.0), -1.25], dur=0.06, ease='in'), k(r(HIT2 - 0.06), rotTo=[0.0, 0.0, 0.0], dur=0.06, ease='in'),
        k(r(HIT2 + 0.3), to=[SPX, GRIPY(0.32), -1.25], dur=0.18, ease='out')]
st.shot('S02', 'kitchenDay', actors=[act('mec', MEK, 0, 'stand', 'neutral', keys=K2)],
        props=[P('table2', 'table', pos=TABLE, opts={'w': 1.0, 'd': 0.7, 'h': TH}), P('jar2', 'picklesJar', pos=JAR2, scale=JS, opts={'hops': [[HIT2, 0.012]]}),
               P('cuil2', 'bendSpoon', pos=[SPX, GRIPY(0.1), -1.25], opts={'len': 0.45, 'foldAt': HIT2, 'angle': 1.5}, keys=KS2)],
        cams=[FC(0.0, [-0.38, 1.0, -0.42], [[JAR2[0], TH, JAR2[2]], [0.04, r(GRIPY(0.34) + 0.05), -1.25], [0.0, 2.38, -1.85], [-0.2, r(TH + 0.2), JAR2[2]], [0.45, r(TH + 0.2), JAR2[2]],
                                             [-0.08, r(GRIPY(WIND2 + 0.07) + 0.04), -1.25], [0.3, r(GRIPY(WIND2) + 0.27), -1.25]], top=0.08, bottom=0.76)])
for t_, v_ in zip(TAPS2, (0.2, 0.3)): st.cue('sfx:tick', 'S02', t_, v_)
st.cue('whoosh', 'S02', r(HIT2 - 0.1), 0.25, 0.25, 900, 400); st.cue('clang', 'S02', HIT2, 0.35)

# 3: he held it under hot water. At his sink, seen from beyond the tap (another angle than 1): he holds the jar under the hot stream, steam
#    billowing round it; he twists again, sweating in the steam; nothing; he looks up at us
D3 = st.dur('S03'); SINK3 = [0.0, 0, -1.3]; JAR3 = [0.0, 0.76, -1.38]; MEK3 = [0.0, 0, -0.72]; MOUTH3 = [0.0, 1.16, -1.38]   # the tap's mouth (islandSink d 0.6)
G3 = lambda f, a=0.0: {'reach': {'L': [-0.1, r(JAR3[1] + 0.12), r(JAR3[2] + 0.03), 1, 0.03], 'R': [r(0.02 - 0.035 * math.cos(a)), r(JAR3[1] + JH + 0.01), r(JAR3[2] + 0.035 * math.sin(a)), 1, 0.03]},
                       'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': f}
st.shot('S03', 'kitchenDay', actors=[act('mec', MEK3, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.0, r(JAR3[1] + 0.25), JAR3[2]]), k(0.0, toon=G3({'lid': 0.7, 'mouth': 'line', 'sweat': 1.0, 'blush': 0.4}), toonDur=0.0),
            k(0.6, toon={**G3({'lid': 0.85, 'mouth': 'clench', 'brow': -0.8, 'sweat': 1.0, 'blush': 0.8, 'vein': 1.0}, 2.0), 'sq': [1.06, 0.93, 1.06]}, toonDur=0.08, toonEase='out'),
            k(0.95, toon=G3({'lid': 0.5, 'mouth': 'line', 'sweat': 1.0, 'blush': 0.6}, 2.5), toonDur=0.15), k(1.15, look='camera')])],
        props=[P('evier3', 'islandSink', pos=SINK3, opts={'w': 1.2, 'd': 0.6}), P('jar3', 'picklesJar', pos=JAR3, scale=JS, opts={'shake': [[0.58, 0.9]]}),
               P('eau3', 'tapStream', pos=MOUTH3, opts={'len': r(MOUTH3[1] - JAR3[1] - JH - 0.02), 'r': 0.011}),
               *[P(f'vap3{j}', 'dustPuff', pos=[r(-0.06 + 0.06 * j), r(JAR3[1] + JH + 0.1 + 0.04 * j), r(-1.42 + 0.02 * j)], scale=0.28, opts={'color': '#F4F8FA', 'period': r(0.7 + 0.12 * j), 'seed': 31 + 6 * j}) for j in range(3)]],   # (stills 1) small wisps above the hands
        cams=[FC(0.0, [1.55, 1.65, -2.5], [[0.0, 2.38, -0.72], [-0.32, 1.6, -0.72], [0.32, 1.6, -0.72], [0.0, 0.74, -1.38], [0.0, 1.22, -1.53]], top=0.12, bottom=0.76, inside=(-6.8, 6.8, 0.3, 4.0, -2.9, 13.0))])
st.cue('sfx:pour', 'S03', 0.0, 0.35)

# 4: he called the fire brigade. His street, three-quarter front: the fire engine tears down the road at us, brakes with a dive (nose down, the back
#    up), rocks on its springs; two firemen shoot out of the cab onto the road and run off toward his door (review 2: a red box seen side-on that
#    slid to a stop)
D4 = st.dur('S04'); TRK4 = [2.3, 0, -1.6]; STOP4 = 0.58; OUT4 = 0.84
DIVE = lambda a: [0.0, r(-PI / 2), a]                  # the engine's front is its +X: turned to face us (ry -90), a dive is a turn about its own Z
FM4 = lambda j: [k(0.0, visible=False), k(r(OUT4 + 0.1 * j), visible=True),
                 k(r(OUT4 + 0.1 * j), toon={'sq': [0.78, 1.3, 0.78], 'lay': [0.25, 0.0], 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.0),
                 k(r(OUT4 + 0.1 * j), to=[r(0.7 - 0.5 * j), 0, r(1.9 - 0.9 * j)], dur=0.18, ease='out', glide=True, face='keep'),       # shot out of the cab door...
                 k(r(OUT4 + 0.18 + 0.1 * j), toon={'sq': [1.16, 0.8, 1.16], 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.04, toonEase='in'),   # ...lands in a squash...
                 k(r(OUT4 + 0.26 + 0.1 * j), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.08),
                 k(r(OUT4 + 0.3 + 0.1 * j), to=[r(-3.4 - 0.4 * j), 0, r(3.4 - 0.7 * j)], dur=0.5, clip='run', ease='in')]                 # ...and runs for the door
st.shot('S04', 'parisStreet', setOpts=STREET, fx=[{'type': 'shake', 'at': STOP4, 'dur': 0.2, 'amount': 0.012}], actors=[
        *[act(f'pompier{j + 1}', [1.5, 0.5, r(-0.1 - 0.6 * j)], -60, 'stand', 'determined', keys=FM4(j)) for j in range(2)]],
        props=[P('camion4', 'fireTruck', pos=[TRK4[0], 0, -17.0], ry=-90, keys=[k(0.0, to=TRK4, dur=STOP4, ease='out'),
                   k(0.34, rotTo=DIVE(-0.15), dur=0.2, ease='out'), k(STOP4, rotTo=DIVE(0.075), dur=0.13), k(r(STOP4 + 0.13), rotTo=DIVE(-0.035), dur=0.12), k(r(STOP4 + 0.25), rotTo=DIVE(0.012), dur=0.1), k(r(STOP4 + 0.35), rotTo=DIVE(0.0), dur=0.1),
                   k(r(STOP4 - 0.02), squash=[1.05, 0.9, 1.03], dur=0.4)]),
               P('frein4', 'toonPuff', pos=[TRK4[0], 0.15, r(TRK4[2] + 2.2)], opts={'n': 6, 'size': 0.28, 'life': 0.6, 'rise': 0.5, 'spread': 1.3, 'at': r(STOP4 - 0.12), 'color': '#EDEAE4'})],
        cams=[FC(0.0, [-1.0, 1.05, 6.0], [[TRK4[0], 2.9, r(TRK4[2] + 3.1)], [r(TRK4[0] + 0.9), 0.0, r(TRK4[2] + 3.2)], [r(TRK4[0] - 0.9), 2.2, r(TRK4[2] - 2.2)], [0.2, 0.0, 1.0], [-0.4, 2.45, 2.0], [0.7, 0.0, 2.2]], top=0.14, bottom=0.78)])
st.cue('sfx:siren', 'S04', 0.0, 0.35); st.cue('sfx:brake', 'S04', 0.36, 0.3); st.cue('thud', 'S04', r(OUT4 + 0.2), 0.2)

# 5: they brought out the big jaws. At table height, close: the jar and the toothed jaws on its lid in the foreground; behind them, facing us, the
#    fireman on the two grips heaves three times, each bigger: he leans back, red in the face, teeth bared, the steel arms bow; the other fireman hugs
#    the jar and is dragged a little further each time (review 2: a yellow box that floated by an open hand, nobody straining)
D5 = st.dur('S05'); JAR5 = [0.0, TH, -0.65]; T5 = [0.0, 0, -0.6]; JS5 = 1.5; JRY = 0   # the table nearer the camera; the jaws point at us
LID5 = [JAR5[0], r(TH + 0.204 * JS), JAR5[2]]
JAWP = lambda d=0.0: [LID5[0], LID5[1], r(LID5[2] - 0.05 - 0.915 * JS5 - d)]       # the handle end when the beak bites the lid's back edge; d: how far the tool is hauled back
GR5 = lambda d: loc(JAWP(d), JRY, [-0.17, 0.0, 0.12], JS5)                          # the grip under his right hand (he faces +Z: his right is -X), and under his left
GL5 = lambda d: loc(JAWP(d), JRY, [0.17, 0.0, 0.12], JS5)
FP1 = [0.0, 0, r(JAWP()[2] - 0.2)]; P2 = lambda d=0.0: [-0.52, 0, r(-1.2 - d)]
HEAVE5 = [(0.42, 0.04, 0.2, 0.4), (0.84, 0.08, 0.34, 0.7), (1.28, 0.13, 0.5, 1.0)]   # (when, how far the jar is dragged, how far back he leans, how far the arms bow)
F5 = lambda p: {'lid': r(0.6 + 0.3 * p), 'mouth': 'clench', 'brow': -0.9, 'cheeks': r(0.4 + 0.6 * p), 'blush': r(min(1.0, 0.5 + 0.6 * p)), 'vein': 1.0, 'sweat': 1.0 if p > 0.5 else 0.0}
PULL5 = lambda d, lean, f, sq=None: {'reach': {'R': [*GR5(d), 1, 0.03], 'L': [*GL5(d), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'lay': [r(-lean), 0.0], 'face': f, **({'sq': sq} if sq else {})}
HUG5 = lambda d, f, sq=None: {'reach': {'L': [0.11, r(TH + 0.15), r(JAR5[2] + 0.07 - d), 1, 0.03], 'R': [0.04, r(TH + 0.13), r(JAR5[2] - 0.12 - d), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.72, 0, 0, 1, None]}, 'face': f, **({'sq': sq} if sq else {})}
K5A = [k(0.0, look=[LID5[0], LID5[1], LID5[2]]), k(0.0, toon=PULL5(0.0, 0.04, {'lid': 0.4, 'mouth': 'line', 'brow': -0.5}), toonDur=0.0)]
K5B = [k(0.0, look=[LID5[0], LID5[1], LID5[2]]), k(0.0, toon=HUG5(0.0, {'lid': 0.5, 'mouth': 'line'}), toonDur=0.0)]
KJ5, KT5, BOW5 = [], [], [[0.0, 0.0]]
for i, (t_, d, lean, bw) in enumerate(HEAVE5):
    p = (i + 1) / 3
    K5A += [k(t_, toon=PULL5(d, lean, F5(p), [r(1.05 + 0.04 * p), r(0.94 - 0.05 * p), r(1.05 + 0.04 * p)]), toonDur=0.1, toonEase='out'),
            k(r(t_ + 0.24), toon=PULL5(r(d * 0.6), r(lean * 0.45), {**F5(p), 'mouth': 'O', 'lid': 0.4}, [0.98, 1.03, 0.98]), toonDur=0.14)]
    K5B += [k(t_, toon=HUG5(d, {'lid': 0.95, 'mouth': 'wavy', 'sweat': 1.0, 'brow': -0.4}, [1.05, 0.95, 1.05]), toonDur=0.1, toonEase='out'), k(t_, to=P2(d), dur=0.1, ease='out', glide=True, face='keep'),
            k(r(t_ + 0.24), toon=HUG5(r(d * 0.6), {'lid': 0.7, 'mouth': 'wavy', 'sweat': 1.0}), toonDur=0.14), k(r(t_ + 0.24), to=P2(r(d * 0.6)), dur=0.14, glide=True, face='keep')]
    KJ5 += [k(t_, to=[JAR5[0], JAR5[1], r(JAR5[2] - d)], dur=0.1, ease='out'), k(r(t_ + 0.24), to=[JAR5[0], JAR5[1], r(JAR5[2] - d * 0.6)], dur=0.14)]
    KT5 += [k(t_, to=JAWP(d), dur=0.1, ease='out'), k(r(t_ + 0.24), to=JAWP(r(d * 0.6)), dur=0.14)]
    BOW5 += [[t_, BOW5[-1][1]], [r(t_ + 0.1), bw], [r(t_ + 0.38), r(bw * 0.5)]]
st.shot('S05', 'kitchenDay', actors=[act('pompier1', FP1, 0, 'stand', 'determined', keys=K5A), act('pompier2', P2(), 48, 'stand', 'neutral', keys=K5B)],
        props=[P('table5', 'table', pos=T5, opts={'w': 1.0, 'd': 0.7, 'h': TH}), P('jar5', 'picklesJar', pos=JAR5, scale=JS, opts={'shake': [[t_, r(t_ + 0.24)] for t_, *_ in HEAVE5]}, keys=KJ5),
               P('pince5', 'bigJaws', pos=JAWP(), ry=JRY, opts={'s': JS5, 'vertical': True, 'open': [[0.0, 0.9], [0.12, 0.9], [0.26, -0.12]], 'bow': BOW5}, keys=KT5)],
        cams=[FC(0.0, [1.15, 1.12, 0.75], [[JAR5[0], TH, r(JAR5[2] + 0.12)], [0.16, r(TH + 0.2), JAR5[2]], [-0.16, r(TH + 0.2), JAR5[2]], [FP1[0], 2.42, FP1[2]], bodyPt(FP1, 0, -0.5, 0.0, 2.38),
                                             [-0.38, 2.28, -1.0], JAWP(0.13)], top=0.1, bottom=0.76, lenses=range(26, 66))])
st.cue('sfx:rattle', 'S05', 0.14, 0.25)
for t_, *_ in HEAVE5: st.cue('sfx:squeak', 'S05', t_, 0.22)

# 6: the jaws broke. Face on, tighter: CRAC, the two steel arms snap off and fly apart across the wall in a puff; the fireman is thrown
#    back, eyes out on stalks; the other lets go and stares; the jar slides back to its place without a scratch
D6 = st.dur('S06'); BRK6 = 0.25; D6M = 0.13
st.shot('S06', 'kitchenDay', actors=[
        act('pompier1', FP1, 0, 'stand', 'determined', keys=[k(0.0, look=[LID5[0], LID5[1], LID5[2]]), k(0.0, toon=PULL5(D6M, 0.5, F5(1.0), [1.09, 0.89, 1.09]), toonDur=0.0),
            k(0.1, toon=PULL5(r(D6M + 0.02), 0.56, F5(1.0), [1.11, 0.87, 1.11]), toonDur=0.12),
            k(BRK6, to=[FP1[0], 0, r(FP1[2] - 0.45)], dur=0.2, ease='out', glide=True, face='keep'),
            k(BRK6, toon={'reach': {'R': [-0.4, 2.3, r(FP1[2] - 0.3), 1, 0.03], 'L': [0.4, 2.25, r(FP1[2] - 0.3), 1, 0.03]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'lay': [-0.75, 0.0], 'sq': [0.88, 1.16, 0.88],
                          'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.3, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.05, toonEase='out'),   # thrown back, eyes on stalks...
            k(r(BRK6 + 0.24), toon={'reach': {'R': [-0.45, 2.0, r(FP1[2] - 0.6), 1, 0.03], 'L': [0.45, 1.95, r(FP1[2] - 0.6), 1, 0.03]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'lay': [-0.4, 0.0], 'sq': [1.06, 0.94, 1.06],
                          'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.3, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.14),   # ...lands, held
            k(r(BRK6 + 0.5), toon={'reach': {'R': [-0.45, 1.9, r(FP1[2] - 0.55), 1, 0.03], 'L': [0.45, 1.85, r(FP1[2] - 0.55), 1, 0.03]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'lay': [-0.3, 0.0],
                          'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.22, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.12),
            k(r(BRK6 + 0.75), toon={'hands': {'R': 'spread', 'L': 'spread'}, 'lay': [-0.12, 0.0], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.2), k(r(BRK6 + 0.8), look='camera')]),
        act('pompier2', P2(D6M), 48, 'stand', 'neutral', keys=[k(0.0, look=[LID5[0], LID5[1], LID5[2]]), k(0.0, toon=HUG5(D6M, {'lid': 0.95, 'mouth': 'wavy', 'sweat': 1.0}), toonDur=0.0),
            k(r(BRK6 + 0.04), toon={'touch': {'R': ['face', -0.12, 0.5, 0.0, 1, 0.02], 'L': ['face', 0.12, 0.5, 0.0, 1, 0.02]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [1.22, 0.6, 1.22], 'face': {'lid': 1.0, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.06, toonEase='out'),   # he ducks, flat as a pancake, hands on his helmet
            k(r(BRK6 + 0.3), toon={'touch': {'R': ['face', -0.12, 0.5, 0.0, 1, 0.02], 'L': ['face', 0.12, 0.5, 0.0, 1, 0.02]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [1.14, 0.7, 1.14], 'face': {'lid': 1.0, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.12),
            k(r(BRK6 + 0.62), toon={'touch': {'R': ['face', -0.12, 0.5, 0.0, 1, 0.02], 'L': ['face', 0.12, 0.5, 0.0, 1, 0.02]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [1.1, 0.78, 1.1], 'face': {'lid': 0.2, 'mouth': 'wavy', 'brow': 0.6}}, toonDur=0.12),   # and peeks
            k(r(BRK6 + 0.62), look=[JAR5[0], r(TH + 0.2), JAR5[2]]), k(r(BRK6 + 0.95), look='camera', lookDur=0.12),
            k(r(BRK6 + 0.95), toon={'hands': {'L': 'rest', 'R': 'rest'}, 'sq': [1.04, 0.9, 1.04], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.15)])],
        props=[P('table6', 'table', pos=T5, opts={'w': 1.0, 'd': 0.7, 'h': TH}),
               P('jar6', 'picklesJar', pos=[JAR5[0], JAR5[1], r(JAR5[2] - D6M)], scale=JS, opts={'shake': [[0.0, BRK6]]}, keys=[k(BRK6, to=JAR5, dur=0.1, ease='out'), k(r(BRK6 + 0.08), squash=[1.12, 0.9, 1.12], dur=0.35)]),
               P('pince6', 'bigJaws', pos=JAWP(D6M), ry=JRY, opts={'s': JS5, 'vertical': True, 'open': [[0.0, -0.12]], 'bow': [[0.0, 1.0], [BRK6, 1.3]], 'breakAt': BRK6},
                 keys=[k(BRK6, to=[JAWP()[0], 0.14, r(JAWP()[2] - 0.55)], dur=0.3, ease='in'), k(BRK6, rotTo=[0.0, 0.0, 1.3], dur=0.3)]),   # the body drops behind the table
               BURST('crac6', [0.3, r(TH + 0.92), -0.7], r(BRK6 + 0.02), 'CRAC !', 0.46, 0.34)],
        cams=[FC(0.0, [0.3, 1.05, 1.0], [[JAR5[0], TH, r(JAR5[2] + 0.12)], bodyPt([0.0, 0, r(FP1[2] - 0.45)], 0, -0.4, 0.0, 2.38), [0.62, r(TH + 1.0), -0.7], [-0.5, r(TH + 0.9), -0.7], [0.0, 2.4, FP1[2]]],
                 top=0.2, bottom=0.76, lenses=range(26, 66))])   # (stills 1 of pass 3) from the left, the fireman who hugs the jar hid the one thrown back
st.cue('sfx:crunch', 'S06', BRK6, 0.45); st.cue('clang', 'S06', r(BRK6 + 0.3), 0.2)

# 7: the army sent a tank. His street from the road, low: the jar stands in the middle of the road, big in the foreground; a tank rumbles down at
#    it, its long gun swinging down to aim at the jar; the ground shakes harder at every turn of its tracks: the jar hops, its lid rattles, pebbles
#    jump (review 2: the tank only grew, nothing reacted)
D7 = st.dur('S07'); JR = [0.0, 0, 2.6]
PULSE7 = [(0.2, 0.004), (0.55, 0.006), (0.85, 0.009), (1.1, 0.012), (1.3, 0.015), (1.47, 0.018), (1.62, 0.022)]   # (when, how hard): closer and harder
STREET7 = {**STREET, 'clear': [-60.0, 8.0], 'clearL': [-60.0, 8.0], 'clouds': 0}   # no tree behind the jar's lid
st.shot('S07', 'parisStreet', setOpts=STREET7, fx=[{'type': 'shake', 'at': t_, 'dur': 0.14, 'amount': r(a * 0.8)} for t_, a in PULSE7], actors=[],
        props=[P('jar7', 'picklesJar', pos=JR, scale=2.2, opts={'hops': [[t_, a] for t_, a in PULSE7]}),
               P('char7', 'battleTank', pos=[0.0, 0, -14.0], ry=0, keys=[k(0.0, to=[0.0, 0, -3.4], dur=D7, ease='linear')], opts={'rumble': [[0.0, 9.0, 0.025]], 'gun': [[0.0, -0.06], [0.85, -0.06], [1.4, 0.19]]}),
               P('cailloux7', 'roadPebbles', pos=[0.25, 0, 3.0], opts={'n': 9, 'w': 1.4, 'd': 1.0, 'hops': [[t_, r(a * 7)] for t_, a in PULSE7]})],
        cams=[FC(0.0, [-0.55, 0.32, 4.4], [[JR[0], 0.0, JR[2]], [JR[0], 0.58, JR[2]], [r(JR[0] - 0.22), 0.3, JR[2]], [r(JR[0] + 0.22), 0.3, JR[2]], [0.0, 2.6, -6.0], [-1.7, 0.0, -6.0], [1.7, 0.0, -6.0]], top=0.14, bottom=0.78)])
st.cue('engine', 'S07', 0.0, 0.35)
for t_, a in PULSE7[2:]: st.cue('thud', 'S07', t_, r(0.1 + a * 6))

# 8: the tank drove over it. From the side, low and close: the tank's tracks roll over the jar; the whole tank rears up over it, hangs, and slams
#    down; the jar hops once and stands
D8 = st.dur('S08')
st.shot('S08', 'parisStreet', setOpts=STREET7, fx=[{'type': 'shake', 'at': 1.28, 'dur': 0.3, 'amount': 0.02}], actors=[],
        props=[P('jar8', 'picklesJar', pos=JR, scale=2.2, opts={'hops': [[1.3, 0.03]]}),
               P('char8', 'battleTank', pos=[0.0, 0, -2.6], ry=0, opts={'rumble': [[0.0, 9.0, 0.015]], 'gun': [[0.0, 0.1], [0.42, 0.1], [0.62, -0.25], [1.05, -0.25], [1.3, 0.3], [1.55, 0.0]]},
                 keys=[k(0.0, to=[0.0, 0, 0.9], dur=0.5, ease='linear'), k(0.5, to=[0.0, 0.45, 2.6], dur=0.3, ease='out'), k(0.8, to=[0.0, 0.45, 3.8], dur=0.28, ease='linear'),
                       k(1.08, to=[0.0, 0.0, 5.0], dur=0.2, ease='in'), k(1.28, to=[0.0, 0.0, 6.4], dur=0.4, ease='out'), k(1.28, squash=[1.06, 0.84, 1.06], dur=0.35),
                       k(0.42, rotTo=[-0.3, 0.0, 0.0], dur=0.2, ease='out'), k(0.8, rotTo=[0.08, 0.0, 0.0], dur=0.25), k(1.08, rotTo=[0.2, 0.0, 0.0], dur=0.12, ease='in'), k(1.28, rotTo=[0.0, 0.0, 0.0], dur=0.18, ease='out')]),   # (review 1) it rears up, hangs, slams
               P('fill8', 'glowLight', pos=[2.6, 3.0, 3.4], opts={'color': '#FFF2DC', 'k': 4.0, 'dist': 9.0}),
               P('pouss8', 'toonPuff', pos=[0.3, 0.2, 5.2], opts={'n': 6, 'size': 0.4, 'life': 0.5, 'rise': 0.5, 'spread': 1.4, 'at': 1.28, 'color': '#EDEAE4'})],
        cams=[FC(0.0, [3.5, 0.5, 2.8], [[JR[0], 0.0, JR[2]], [JR[0], 0.62, JR[2]], [0.0, 2.3, JR[2]], [0.0, 0.0, r(JR[2] - 0.85)], [0.0, 0.0, r(JR[2] + 0.85)]], top=0.12, bottom=0.72, inside=(-4.4, 4.4, 0.2, 6.0, -40.0, 40.0), lenses=range(26, 86))])   # (review 2) nearer: the jar and the road in the middle, the tank through the frame
st.cue('engine', 'S08', 0.0, 0.3); st.cue('clang', 'S08', 0.55, 0.35); st.cue('thud', 'S08', 1.28, 0.3)

# 9: the tank got a flat. Behind the jar in the foreground: the tank has turned its gun back at the jar; its near track goes flat in three sags, a
#    white puff at each, the hull sinking and the gun drooping a little more each time, then a last drop; a nut rolls from it up to the jar and tips
#    over; the jar has not a scratch (review 2: one sag in 0.3 s, then a still picture)
D9 = st.dur('S09'); TK9 = [0.0, 0, 6.4]; SAG9 = [(0.12, 0.36), (0.44, 0.7), (0.78, 1.0)]
FLAT9 = [[0.0, 0.0]]
for t_, f_ in SAG9: FLAT9 += [[t_, FLAT9[-1][1]], [r(t_ + 0.15), f_]]
st.shot('S09', 'parisStreet', setOpts=STREET7, actors=[],
        props=[P('jar9', 'picklesJar', pos=JR, scale=2.2, opts={'hops': [[0.93, 0.012]]}),
               P('char9', 'battleTank', pos=TK9, ry=0, opts={'flat': FLAT9, 'flatSide': -1, 'turret': [[0.0, PI]], 'gun': [[0.0, 0.06]], 'droop': 0.22}, keys=[k(0.9, squash=[1.05, 0.9, 1.05], dur=0.3)]),
               P('fill9', 'glowLight', pos=[-1.5, 3.0, 3.5], opts={'color': '#FFF2DC', 'k': 4.0, 'dist': 9.0}),
               P('ecrou9', 'hexNut', pos=[-0.75, 0.1, 4.5], opts={'r': 0.1}, keys=[k(0.0, visible=False), k(0.9, visible=True), k(0.9, to=[-0.36, 0.1, 3.0], dur=0.26, ease='out'), k(0.9, rotTo=[-9.0, 0.0, 0.0], dur=0.26, ease='out'),
                                                                                       k(1.17, rotTo=[-9.0, 0.0, 1.5], dur=0.08, ease='in'), k(1.17, to=[-0.36, 0.04, 3.0], dur=0.08, ease='in')])],
        cams=[FC(0.0, [-0.9, 0.45, 0.4], [[JR[0], 0.0, JR[2]], [JR[0], 0.55, JR[2]], [0.0, 2.6, TK9[2]], [-1.9, 0.0, TK9[2]], [1.8, 0.0, TK9[2]]], top=0.2, bottom=0.78)])
for t_, f_ in SAG9: st.cue('whoosh', 'S09', t_, r(0.2 + 0.1 * f_), 0.3, 3000, 600)
st.cue('thud', 'S09', 0.9, 0.25); st.cue('sfx:tick', 'S09', 1.2, 0.25)

# 10: it was sent into space. A launch pad in the fields, low: a rumble, the rocket squashes, stretches and climbs out of the top of the frame; the
#     smoke keeps billowing up from the pad to the cut (review 2: an empty frame and frozen smoke at the end)
D10 = st.dur('S10'); RK = [0.0, 0, -4.0]
st.shot('S10', 'grassland', fx=[{'type': 'shake', 'at': 0.05, 'dur': 0.4, 'amount': 0.015}], actors=[],
        props=[P('fusee10', 'rocket', pos=[RK[0], 0.24, RK[2]], opts={'flame': True}, keys=[k(0.05, squash=[1.06, 0.92, 1.06], dur=0.2), k(0.3, squash=[0.93, 1.12, 0.93], dur=0.3), k(0.3, to=[RK[0], 16.0, RK[2]], dur=r(D10 - 0.3), ease='in')]),   # (review 1) a rumble and a squash, then a stretch
               P('pad10', 'slab', pos=[RK[0], 0.12, RK[2]], opts={'w': 2.6, 'h': 0.24, 'd': 2.6, 'color': '#9AA0A6', 'outline': 0.01}),
               P('tour10', 'slab', pos=[r(RK[0] - 1.45), 2.6, RK[2]], opts={'w': 0.35, 'h': 5.2, 'd': 0.35, 'color': '#C8452E', 'outline': 0.008}), P('bras10', 'slab', pos=[r(RK[0] - 0.95), 3.7, RK[2]], opts={'w': 0.9, 'h': 0.12, 'd': 0.2, 'color': '#C8452E', 'outline': 0.006}),
               P('fum10', 'toonPuff', pos=[RK[0], 0.35, r(RK[2] + 0.3)], opts={'n': 16, 'size': 0.5, 'life': 1.4, 'rise': 3.0, 'spread': 1.9, 'startAt': 0.12, 'color': '#F4F2EE'})],
        cams=[FC(0.0, [3.8, 0.7, 4.0], [[RK[0], 0.0, RK[2]], [RK[0], 5.8, RK[2]], [-2.0, 0.0, RK[2]], [2.0, 0.0, RK[2]]], top=0.12, bottom=0.78, drift=(0.0, 0.25, 0.0))])
st.cue('engine', 'S10', 0.1, 0.4); st.cue('whoosh', 'S10', 0.3, 0.4, 1.2, 200, 1200)

# 11: six astronauts tried. Inside the space module, a big window on the Earth behind: a tug of war in zero gravity. The jar floats on its side in
#     the middle; on the right one astronaut grips the lid and two more pull him by the waist, on the left one hugs the jar and two more pull him:
#     two chains going up and back, every body at its own tilt (one upside down), faces to us; three heaves, each bigger; then the hands slip and
#     all six fly off spinning, each on his own path; the jar is left in the middle, turning slowly, its lid on (review 2: a grey clump of backs)
D11 = st.dur('S11'); JS11 = 2.0; JB11 = [-0.2, 2.0, 1.0]; REL11 = 1.5      # the jar's base (it lies along +X: the lid on the right)
HEAVE11 = [(0.3, 0.14), (0.7, 0.26), (1.1, 0.4)]                              # (when, how far back they lean)
TEAM = [  # (id, feet, heading, roll, hands on: 'lid' / 'jar' / (leader index, height up his body), where he flies, the turn he takes [pitch, roll])
    ('astro1', [0.6, 0.5, 0.9], -35, 0.1, 'lid', [1.05, 2.45, 0.3], [-5.6, 0.6]),
    ('astro2', [0.95, 1.05, -0.3], -35, -0.08, (0, 1.05), [1.1, 0.5, -0.7], [2.6, -4.2]),
    ('astro3', [1.3, 1.6, -1.6], -30, -0.16, (1, 1.05), [0.9, 2.9, -1.9], [-3.6, 3.2]),
    ('astro4', [-0.6, 0.55, 0.9], 35, -0.12, 'jar', [-1.05, 0.45, 0.4], [5.2, -0.7]),
    ('astro5', [-0.95, 1.15, -0.3], 35, 0.08, (3, 1.05), [-1.1, 2.7, -0.6], [-2.9, 3.8]),
    ('astro6', [-1.3, 1.55, -1.6], 30, 0.16, (4, 1.05), [-0.9, 3.0, -1.9], [3.4, 4.6])]   # each chain goes up and back: three heads in a row, the far ones smaller
def hands11(i, lean):
    n_, feet, ry_, roll, on, *_ = TEAM[i]
    if on == 'lid': return [0.27, 2.07, 1.05], [0.27, 1.93, 0.96]
    if on == 'jar': return [-0.1, 2.09, 1.06], [-0.08, 1.92, 0.95]
    j, h = on; fj, ryj, rollj = TEAM[j][1], TEAM[j][2], TEAM[j][3]; c = bodyPt(fj, ryj, -lean, rollj, h); s_ = 1 if ry_ < 0 else -1
    return [r(c[0] + 0.1 * s_), r(c[1] + 0.02), r(c[2] + 0.1)], [r(c[0] + 0.02 * s_), r(c[1] - 0.02), r(c[2] - 0.12)]
def pull11(i, lean, f, sq=None):
    a, b = hands11(i, lean); roll = TEAM[i][3]
    return {'reach': {'R': [*a, 1, 0.03], 'L': [*b, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'lay': [r(-lean if abs(roll) < 1 else lean), roll], 'face': f, **({'sq': sq} if sq else {})}
ACT11 = []
for i, (n_, feet, ry_, roll, on, fly, turn) in enumerate(TEAM):
    ks = [k(0.0, look='camera' if i in (1, 4) else [0.0, 2.0, 1.0]), k(0.0, toon=pull11(i, 0.04, {'lid': 0.5, 'mouth': 'clench', 'brow': -0.6}), toonDur=0.0)]
    for h_, (t_, lean) in enumerate(HEAVE11):
        p = (h_ + 1) / 3
        lean = r(lean * (1.0, 0.75, 0.55)[i % 3])
        ks += [k(r(t_ + 0.02 * i), toon=pull11(i, lean, {'lid': r(0.6 + 0.3 * p), 'mouth': 'clench', 'brow': -0.9, 'cheeks': r(0.5 * p), 'blush': r(0.4 + 0.6 * p), 'vein': r(p), 'sweat': 1.0 if p > 0.6 else 0.0}, [r(0.97 - 0.03 * p), r(1.05 + 0.06 * p), r(0.97 - 0.03 * p)]), toonDur=0.1, toonEase='out'),
               k(r(t_ + 0.22 + 0.02 * i), toon=pull11(i, r(lean * 0.4), {'lid': 0.5, 'mouth': 'O', 'brow': -0.4, 'blush': r(0.4 + 0.5 * p)}, [1.02, 0.98, 1.02]), toonDur=0.12)]
    ks += [k(r(REL11 - 0.1), toon=pull11(i, r(0.46 * (1.0, 0.75, 0.55)[i % 3]), {'lid': 0.9, 'mouth': 'clench', 'brow': -1.0, 'blush': 1.0, 'vein': 1.0, 'sweat': 1.0}, [0.93, 1.12, 0.93]), toonDur=0.1, toonEase='out'),
           k(REL11, to=fly, dur=r(D11 - REL11 + 0.25), ease='out', glide=True, face='keep', clip='tumble'),                                    # the hands slip: he flies off...
           k(REL11, toon={'lay': [r(turn[0] * 0.25), r(roll + (turn[1] - roll) * 0.25)], 'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.12, toonEase='out'),
           k(r(REL11 + 0.12), toon={'lay': [turn[0], turn[1]], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}}, toonDur=r(D11 - REL11 - 0.1), toonEase='linear')]   # ...turning on his own axis
    ACT11.append(act(n_, feet, ry_, 'float', 'determined', keys=ks))
st.shot('S11', 'stationInside', actors=ACT11,
        props=[P('fond11', 'slab', pos=[0.0, 2.0, -2.27], opts={'w': 6.3, 'h': 4.0, 'd': 0.04, 'color': '#28304C'}),   # (review 2) a dark, cool wall: the suits were grey on grey
               P('sol11', 'slab', pos=[0.0, -0.01, 1.6], opts={'w': 6.4, 'h': 0.04, 'd': 8.2, 'color': '#39415A'}),
               P('hublot11', 'spaceWindow', pos=[0.0, 2.3, -2.2], opts={'r': 1.2}),
               P('cle11', 'glowLight', pos=[0.5, 2.9, 4.4], opts={'color': '#FFFFFF', 'k': 7.0, 'dist': 13.0, 'at': -1.0}), P('contre11', 'glowLight', pos=[-1.6, 3.4, -1.3], opts={'color': '#BFD8FF', 'k': 4.0, 'dist': 8.0, 'at': -1.0}),
               P('jar11', 'picklesJar', pos=JB11, rot=[0.0, 0.0, r(-PI / 2)], scale=JS11, opts={'shake': [[t_, r(t_ + 0.22)] for t_, _ in HEAVE11]},
                 keys=[*[k(t_, squash=[0.94, 1.14, 0.94], dur=0.3) for t_, _ in HEAVE11], k(REL11, squash=[1.12, 0.86, 1.12], dur=0.4), k(REL11, rotTo=[0.5, 0.9, r(-PI / 2 + 0.5)], dur=r(D11 - REL11 + 0.3), ease='out')]),
               *[P(f'casque11{j}', 'spaceHelmet', on={'actor': t_[0], 'joint': 'head', 'offset': [0.0, -0.02, 0.0]}, opts={'r': 0.34}) for j, t_ in enumerate(TEAM)]],
        cams=[FC(0.0, [0.0, 2.05, 5.3], [[0.0, 2.0, 1.0], *[bodyPt(t_[1], t_[2], -0.12, t_[3], 2.4) for t_ in TEAM], *[t_[1] for t_ in TEAM]],
                 top=0.1, bottom=0.76, inside=(-3.0, 3.0, 0.4, 3.8, -2.2, 5.6), lenses=range(26, 66))])
for t_, _ in HEAVE11: st.cue('sfx:squeak', 'S11', t_, 0.2)
st.cue('whoosh', 'S11', REL11, 0.3, 0.6, 600, 1400)

# 12: the scientists fired a laser. In a lab, low, from beside the jar: the jar on its stand big in the foreground; facing us behind his cannon, the
#     scientist smirks at us and snaps his goggles down; the cannon whines and swells; he fires: the kick shoves him back a step, the red beam
#     runs to the lid, which glows and smokes; beside him his colleague has his fingers in his ears (review 2: a wide side view, the jar tiny at
#     the edge, the beam simply on; nothing charged, nothing kicked)
D12 = st.dur('S12'); JAR12 = [0.0, 0.9, -1.0]; JS12 = 1.7; GUNP = [1.55, 0, -1.0]; GUN = [1.55, 1.0, -1.0]; FIRE12 = 1.0; CHG12 = [0.55, 0.98]
LENS12 = [r(GUNP[0] - 0.77), 1.04, GUNP[2]]; LID12 = [r(JAR12[0] + 0.08 * JS12), r(JAR12[1] + 0.204 * JS12), JAR12[2]]
BEAM12 = [r(LID12[0] - LENS12[0]), r(LID12[1] - LENS12[1]), 0.0]
SAV12 = [2.1, 0, -0.85]; SAV12B = [2.6, 0, -0.8]; COL12 = [2.75, 0, -1.95]
GUNK = lambda f, press=False, **kw: {'reach': {'R': [r(GUN[0] + 0.12), r(GUN[1] + (0.14 if press else 0.2)), r(GUN[2] + 0.12), 1, 0.03], 'L': [r(GUN[0] + 0.12), r(GUN[1] + 0.1), r(GUN[2] - 0.15), 1, 0.03]}, 'hands': {'R': 'point', 'L': 'grip'}, 'face': f, **kw}
EARS = lambda f, **kw: {'touch': {'R': ['face', -0.15, 0.24, 0.0, 1, 0.02], 'L': ['face', 0.15, 0.24, 0.0, 1, 0.02]}, 'hands': {'R': 'point', 'L': 'point'}, 'face': f, **kw}
st.shot('S12', 'lab', actors=[
        act('savant1', SAV12, -95, 'stand', 'determined', keys=[k(0.0, look=LID12), k(0.0, toon=GUNK({'lid': 0.4, 'mouth': 'line', 'brow': -0.5}), toonDur=0.0),
            k(0.18, look='camera', lookDur=0.1), k(0.2, toon=GUNK({'lid': 0.5, 'mouth': 'smirk', 'brow': -0.5}), toonDur=0.1),          # the smirk to us
            k(0.52, look=LID12, lookDur=0.08), k(CHG12[0], toon=GUNK({'lid': 0.6, 'mouth': 'smirk', 'brow': -0.8}, sq=[1.04, 0.95, 1.04], lay=[0.12, 0.0]), toonDur=0.3),   # he leans in as it charges
            k(r(FIRE12 - 0.04), toon=GUNK({'lid': 0.7, 'mouth': 'clench', 'brow': -0.9}, True, sq=[1.07, 0.92, 1.07], lay=[0.14, 0.0]), toonDur=0.04),
            k(FIRE12, to=SAV12B, dur=0.16, ease='out', glide=True, face='keep'),                                                         # the kick: a step back
            k(FIRE12, toon={'reach': {'R': [2.2, 1.85, -0.55, 1, 0.03], 'L': [2.2, 1.8, -1.15, 1, 0.03]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'lay': [-0.32, 0.0], 'sq': [0.9, 1.13, 0.9], 'hairUp': 0.7, 'face': {'lid': 0.1, 'mouth': 'O', 'brow': 0.9}}, toonDur=0.05, toonEase='out'),
            k(r(FIRE12 + 0.18), toon={'hands': {'L': 'spread', 'R': 'spread'}, 'lay': [0.07, 0.0], 'sq': [1.06, 0.94, 1.06], 'hairUp': 0.3, 'face': {'lid': 0.2, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.12),
            k(r(FIRE12 + 0.4), toon={'hands': {'L': 'rest', 'R': 'rest'}, 'lay': [0.0, 0.0], 'face': {'lid': 0.5, 'mouth': 'smile', 'brow': -0.3}}, toonDur=0.15),
            k(r(FIRE12 + 0.7), toon={'hands': {'L': 'rest', 'R': 'rest'}, 'lay': [0.1, 0.0], 'face': {'lid': 0.6, 'mouth': 'smirk', 'brow': -0.5}}, toonDur=0.2),
            k(r(FIRE12 + 0.92), toon={'hands': {'L': 'rest', 'R': 'rest'}, 'lay': [0.1, 0.0], 'face': {'lid': 1.0, 'mouth': 'smirk', 'brow': -0.5}}, toonDur=0.05), k(r(FIRE12 + 1.02), toon={'hands': {'L': 'rest', 'R': 'rest'}, 'lay': [0.1, 0.0], 'face': {'lid': 0.6, 'mouth': 'smirk', 'brow': -0.5}}, toonDur=0.07)]),
        act('savant2', COL12, -100, 'stand', 'neutral', keys=[k(0.0, look=[2.1, 1.9, -0.85]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(0.5, toon=EARS({'lid': 0.9, 'mouth': 'clench', 'brow': -0.6}, sq=[1.03, 0.96, 1.03]), toonDur=0.15, toonEase='out'), k(0.6, look=LID12),      # fingers in his ears before it fires
            k(FIRE12, toon=EARS({'lid': 1.0, 'mouth': 'clench', 'brow': -0.9}, sq=[1.08, 0.9, 1.08]), toonDur=0.05), k(r(FIRE12 + 0.2), toon=EARS({'lid': 1.0, 'mouth': 'clench', 'brow': -0.6}), toonDur=0.12),
            k(r(FIRE12 + 0.6), toon=EARS({'lid': 0.5, 'mouth': 'line', 'brow': 0.4}), toonDur=0.12)])],     # he peeks
        props=[P('socle12', 'table', pos=[JAR12[0], 0, JAR12[2]], opts={'w': 0.5, 'd': 0.5, 'h': JAR12[1]}), P('jar12', 'picklesJar', pos=JAR12, scale=JS12, opts={'lidGlow': [[r(FIRE12 + 0.03), 99.0]]}),
               P('canon12', 'laserCannon', pos=GUNP, ry=-90, opts={'charge': CHG12, 'fireAt': FIRE12}),
               P('laser12', 'laserBeam', pos=LENS12, opts={'vec': BEAM12, 'r': 0.024}, keys=[k(0.0, visible=False), k(FIRE12, visible=True)]),
               P('fum12', 'toonPuff', pos=[r(LID12[0] - 0.05), r(LID12[1] + 0.1), LID12[2]], opts={'n': 4, 'size': 0.075, 'life': 0.7, 'rise': 0.55, 'spread': 0.08, 'startAt': r(FIRE12 + 0.2), 'color': '#EFEFEF'}),
               P('lun12', 'labGoggles', on={'actor': 'savant1', 'joint': 'head', 'offset': [0.0, 0.4, 0.09]}, keys=[k(0.46, attach='savant1', joint='head', offset=[0.0, 0.235, 0.112])])],   # goggles down: one snap
        cams=[FC(0.0, [-1.9, 1.05, 0.9], [[JAR12[0], JAR12[1], JAR12[2]], [JAR12[0], r(JAR12[1] + 0.52), JAR12[2]], [-0.34, 1.1, -1.0], [SAV12[0], 2.47, SAV12[2]], [SAV12B[0], 2.35, r(SAV12B[2] + 0.2)], [COL12[0], 2.42, COL12[2]], [JAR12[0], 0.55, JAR12[2]]],
                 top=0.12, bottom=0.76, lenses=range(26, 66))])
st.cue('whoosh', 'S12', CHG12[0], 0.25, 0.42, 300, 2600); st.cue('sfx:click', 'S12', FIRE12, 0.3); st.cue('whoosh', 'S12', FIRE12, 0.3, 0.8, 4000, 2000)

# 13: the laser bounced back. Closer on the scientist: the beam glints off the jar and comes straight back; his hair stands up, frizzled, his face
#     sooty, a puff of smoke; he blinks; a wisp keeps smouldering off his hair
D13 = st.dur('S13'); BACK13 = 0.3; HEAD13 = [2.1, 2.05, -0.85]
st.shot('S13', 'lab', actors=[act('savant1', [2.1, 0, -0.85], -95, 'stand', 'determined', keys=[k(0.0, look=[JAR12[0], r(JAR12[1] + 0.2), JAR12[2]]), k(0.0, toon=GUNK({'lid': 0.6, 'mouth': 'smirk', 'brow': -0.6}, True), toonDur=0.0),
            k(BACK13, toon={**GUNK({'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}, True), 'hairUp': 1.0, 'sq': [0.92, 1.1, 0.92], 'skin': {'color': '#2E2A26', 'k': 0.8, 'fill': 1.0}}, toonDur=0.04, toonEase='out'),   # zapped
            k(r(BACK13 + 0.5), toon={**GUNK({'lid': 1.0, 'mouth': 'line'}), 'hairUp': 1.0, 'skin': {'color': '#2E2A26', 'k': 0.8, 'fill': 1.0}}, toonDur=0.06),
            k(r(BACK13 + 0.62), toon={**GUNK({'lid': 0.3, 'mouth': 'line'}), 'hairUp': 1.0, 'skin': {'color': '#2E2A26', 'k': 0.8, 'fill': 1.0}}, toonDur=0.08), k(r(BACK13 + 0.75), look='camera'),
            k(r(BACK13 + 1.1), toon={**GUNK({'lid': 1.0, 'mouth': 'line'}), 'hairUp': 1.0, 'skin': {'color': '#2E2A26', 'k': 0.8, 'fill': 1.0}}, toonDur=0.06),
            k(r(BACK13 + 1.22), toon={**GUNK({'lid': 0.3, 'mouth': 'wavy'}), 'hairUp': 1.0, 'skin': {'color': '#2E2A26', 'k': 0.8, 'fill': 1.0}}, toonDur=0.08)])],
        props=[P('socle13', 'table', pos=[JAR12[0], 0, JAR12[2]], opts={'w': 0.5, 'd': 0.5, 'h': JAR12[1]}), P('jar13', 'picklesJar', pos=JAR12, scale=JS12, opts={'glint': [[0.22, 0.45]], 'lidGlow': [[-1.0, 0.25]]}),
               P('canon13', 'laserCannon', pos=GUNP, ry=-90, opts={'fireAt': -0.4}),
               P('laser13a', 'laserBeam', pos=LENS12, opts={'vec': BEAM12, 'r': 0.024}, keys=[k(r(BACK13 + 0.05), visible=False)]),
               P('laser13b', 'laserBeam', pos=LID12, opts={'vec': [r(HEAD13[0] - LID12[0]), r(HEAD13[1] + 0.2 - LID12[1]), r(HEAD13[2] - LID12[2])], 'r': 0.024}, keys=[k(0.0, visible=False), k(0.22, visible=True), k(r(BACK13 + 0.1), visible=False)]),   # back at his head
               P('lun13', 'labGoggles', on={'actor': 'savant1', 'joint': 'head', 'offset': [0.0, 0.235, 0.112]}),
               P('fumee13', 'toonPuff', pos=[HEAD13[0], r(HEAD13[1] + 0.45), HEAD13[2]], opts={'n': 7, 'size': 0.2, 'life': 0.6, 'rise': 0.6, 'spread': 0.3, 'at': BACK13, 'color': '#6A6660'}),
               P('meche13', 'toonPuff', pos=[r(HEAD13[0] + 0.03), r(HEAD13[1] + 0.62), HEAD13[2]], opts={'n': 4, 'size': 0.06, 'life': 0.8, 'rise': 0.5, 'spread': 0.06, 'startAt': r(BACK13 + 0.45), 'color': '#8A8680'})],
        cams=[FC(0.0, [-0.6, 1.75, -0.3], [[2.1, 2.65, -0.85], [2.1, 1.1, -0.85], [JAR12[0], r(JAR12[1] + JH + 0.03), JAR12[2]], [JAR12[0], JAR12[1], JAR12[2]]], top=0.12, bottom=0.76)])
st.cue('sfx:ding', 'S13', 0.22, 0.25); st.cue('sfx:crunch', 'S13', BACK13, 0.25)

# 14: the jar became a historic monument. A museum hall: the jar alone in a lit display case on a white plinth, MONUMENT HISTORIQUE on its label;
#     the guard stands right behind it, proud; one visitor takes a photo (a flash), the other gasps, hands to her cheeks, and leans in (HISTORIQUE)
D14 = st.dur('S14'); CASE = [0.0, 0, -1.2]; JAR14 = [0.0, 0.95, -1.2]; CASEO = {'w': 0.6, 'h': 0.95, 'text': 'MONUMENT HISTORIQUE'}; JS14 = 1.6
PH14 = lambda y, f, **kw: {'reach': {'R': [-0.5, y, -1.3, 1, 0.03], 'L': [-0.38, y, -1.33, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f, **kw}
GASP = lambda f, **kw: {'touch': {'R': ['face', -0.13, 0.12, 0.06, 1, 0.02], 'L': ['face', 0.13, 0.12, 0.06, 1, 0.02]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'face': f, **kw}
st.shot('S14', 'mairie', setOpts=MUSEE, actors=[
        act('visiteur1', [-0.68, 0, -1.65], 18, 'stand', 'neutral', keys=[k(0.0, look=[JAR14[0], 1.15, JAR14[2]]), k(0.0, toon=PH14(1.5, {'lid': 0.4, 'mouth': 'line'}), toonDur=0.0),
            k(0.18, toon=PH14(1.72, {'lid': 0.4, 'mouth': 'line'}), toonDur=0.2, toonEase='out'), k(0.48, toon=PH14(1.72, {'lid': 0.85, 'mouth': 'line'}, sq=[1.03, 0.97, 1.03]), toonDur=0.04),   # he frames, squints, click
            k(0.62, toon=PH14(1.72, {'lid': 0.4, 'mouth': 'smile'}), toonDur=0.08), k(0.95, toon=PH14(1.45, {'lid': 0.5, 'mouth': 'smile', 'gy': 0.6}), toonDur=0.2), k(0.95, look=[-0.44, 1.45, -1.3]),   # he checks the picture
            k(1.45, look=[JAR14[0], 1.15, JAR14[2]]), k(1.45, toon=PH14(1.72, {'lid': 0.4, 'mouth': 'line'}), toonDur=0.18, toonEase='out'), k(1.76, toon=PH14(1.72, {'lid': 0.85, 'mouth': 'line'}, sq=[1.03, 0.97, 1.03]), toonDur=0.04),   # and another
            k(1.9, toon=PH14(1.72, {'lid': 0.4, 'mouth': 'smile'}), toonDur=0.08), k(2.25, toon=PH14(1.6, {'lid': 1.0, 'mouth': 'smile'}), toonDur=0.06), k(2.37, toon=PH14(1.6, {'lid': 0.4, 'mouth': 'smile'}), toonDur=0.08)]),
        act('visiteur2', [0.68, 0, -1.6], -20, 'stand', 'happy', keys=[k(0.0, look=[JAR14[0], 1.15, JAR14[2]]), k(0.0, toon={'face': {'lid': 0.2, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.0),
            k(0.56, toon=GASP({'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}, sq=[0.94, 1.09, 0.94]), toonDur=0.07, toonEase='out'),      # the flash: a gasp, hands to her cheeks...
            k(0.74, toon=GASP({'lid': 0.1, 'mouth': 'O', 'brow': 0.9}, sq=[1.03, 0.97, 1.03]), toonDur=0.1),
            k(1.1, toon=GASP({'lid': 0.2, 'mouth': 'smile', 'brow': 0.6}, bend={'spine': [0.3, 0, 0, 1, None]}), toonDur=0.3),                 # ...and she leans in to look
            k(1.6, toon=GASP({'lid': 1.0, 'mouth': 'smile', 'brow': 0.6}, bend={'spine': [0.3, 0, 0, 1, None]}), toonDur=0.06), k(1.72, toon=GASP({'lid': 0.2, 'mouth': 'smile', 'brow': 0.6}, bend={'spine': [0.3, 0, 0, 1, None]}), toonDur=0.08),
            k(1.95, look=[-0.68, 1.9, -1.65]), k(2.0, toon=GASP({'lid': 0.2, 'mouth': 'O', 'brow': 0.8}, bend={'spine': [0.12, 0, 0, 1, None]}), toonDur=0.2)]),
        act('gardien', [0.0, 0, -2.25], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.0),
            k(0.56, toon={'face': {'lid': 0.9, 'mouth': 'line'}, 'sq': [1.02, 0.97, 1.02]}, toonDur=0.05), k(0.7, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.1),      # he blinks at the flash
            k(1.0, toon={'face': {'lid': 0.4, 'mouth': 'smile', 'brow': 0.3}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.25), k(1.3, toon={'face': {'lid': 1.0, 'mouth': 'smile'}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.06),   # and straightens up, proud
            k(1.42, toon={'face': {'lid': 0.4, 'mouth': 'smile', 'brow': 0.3}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.08), k(1.9, toon={'face': {'lid': 0.4, 'mouth': 'smile', 'gx': -0.7}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.15),
            k(2.3, toon={'face': {'lid': 0.4, 'mouth': 'smile', 'gx': 0.0}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.15)])],
        props=[P('vitrine14', 'displayCase', pos=CASE, opts=CASEO), P('jar14', 'picklesJar', pos=JAR14, scale=JS14),
               P('photo14', 'handset', on={'actor': 'visiteur1', 'hand': 'R', 'offset': [0.0, -0.03, 0.03]}),
               P('flash14', 'camFlash', pos=[-0.4, 1.76, -1.24], face='camera', opts={'at': [0.52, 1.8], 'w': 0.5})],
        cams=[FC(0.0, [0.25, 1.15, 0.6], [[0.0, 1.6, -1.2], [-0.68, 0.4, -1.65], [0.68, 0.4, -1.6], [-0.68, 2.4, -1.65], [0.68, 2.4, -1.6], [0.0, 2.47, -2.25], [0.0, 0.72, -0.9]], top=0.22, bottom=0.76)])   # (review 2) tilted down: the heads under the title card, the label above the captions
st.cue('sfx:shutter', 'S14', 0.52, 0.2); st.cue('sfx:shutter', 'S14', 1.8, 0.18)

# 15: then his grandmother came by. Low, three-quarter front: a little old lady with her handbag trots in toward us, straight to the case, smiling
#     at us; she stops, reaches up and lifts the glass off the jar and puts it aside (review 2: far away, faceless; the glass lift is here now)
D15 = st.dur('S15'); NAN15 = [2.95, 0, -1.0]; NAN16 = [0.56, 0, -1.3]; ARR15 = 1.0; LIFT15 = 1.1; MEC16 = [-0.12, 0, -2.2]; GAR16 = [-0.74, 0, -2.32]
COVT = [0.14, r(0.95 + 0.6), -1.08]                              # the near top corner of the glass
NANU = lambda p_, f, hr='grip', **kw: {'reach': {'R': [*p_, 1, 0.03]}, 'hands': {'R': hr, 'L': 'grip'}, 'face': f, **kw}
C15 = [-1.35, 1.0, 0.25]
LK15A, LN15A, _ = fit(C15, [[2.7, 2.15, -1.0], [2.7, 0.6, -1.0], [1.6, 2.1, -1.1]], top=0.14, bottom=0.8)
LK15B, LN15B, _ = fit(C15, [[NAN16[0], 2.15, NAN16[2]], [0.82, 1.2, NAN16[2]], [0.0, 0.95, -1.2], [-0.28, 1.5, -1.2], [NAN16[0], 0.75, NAN16[2]], [0.2, 2.15, -1.1]], top=0.14, bottom=0.8)
LN15 = max(LN15A or 40, LN15B or 40)
st.shot('S15', 'mairie', setOpts=MUSEE, actors=[
        act('mamie', NAN15, -95, 'walk', 'happy', keys=[k(0.0, to=NAN16, dur=ARR15, clip='walk', then='stand', ease='out'), k(0.0, look='camera'), k(0.0, toon={'hands': {'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(0.55, look=[JAR14[0], 1.3, JAR14[2]]), k(r(ARR15 - 0.02), toon=NANU(COVT, {'lid': 0.3, 'mouth': 'smile'}), toonDur=0.1, toonEase='out'),                              # a hand on the glass...
            k(LIFT15, toon=NANU([COVT[0], r(COVT[1] + 0.42), COVT[2]], {'lid': 0.3, 'mouth': 'smile'}, sq=[0.97, 1.05, 0.97]), toonDur=0.22),                                      # ...up it goes...
            k(r(LIFT15 + 0.27), toon=NANU([0.3, 1.75, -1.45], {'lid': 0.3, 'mouth': 'smile'}, 'spread'), toonDur=0.14), k(r(LIFT15 + 0.3), look='camera', lookDur=0.12),             # ...and over her shoulder
            k(r(LIFT15 + 0.45), toon={'hands': {'R': 'rest', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.14)]),
        act('mec', MEC16, 0, 'stand', 'neutral', keys=[k(0.0, look=[JAR14[0], 1.2, JAR14[2]]), k(0.0, toon={'face': LIP}, toonDur=0.0), k(0.5, look=[1.6, 1.6, -1.1]), k(1.05, look=[NAN16[0], 1.8, NAN16[2]])]),
        act('gardien', GAR16, 10, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.0), k(0.4, look=[1.8, 1.6, -1.1], lookDur=0.1), k(0.75, look='camera', lookDur=0.1),
            k(0.95, look=[NAN16[0], 1.8, NAN16[2]], lookDur=0.06), k(0.95, toon={'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.9}, 'sq': [0.96, 1.06, 0.96]}, toonDur=0.05, toonEase='out')])],   # a double take
        props=[P('vitrine15', 'displayCase', pos=CASE, opts={**CASEO, 'liftAt': LIFT15, 'liftDur': 0.22, 'liftH': 0.42, 'coverAway': True}), P('jar15', 'picklesJar', pos=JAR14, scale=JS14),
               P('sac15', 'briefcase', on={'actor': 'mamie', 'hand': 'L', 'offset': [0.0, -0.1, 0.03]}, scale=0.55)],
        cams=[cam(0.0, C15, C15, LK15A, LK15B, lens=LN15, ease='inOut'), glide([cam(ARR15, C15, [r(C15[0] + 0.12), C15[1], r(C15[2] - 0.12)], LK15B, LK15B, lens=LN15)], 0.1)])
st.cue('sfx:stepSoft', 'S15', 0.15, 0.15); st.cue('sfx:stepSoft', 'S15', 0.45, 0.15); st.cue('sfx:stepSoft', 'S15', 0.75, 0.15); st.cue('sfx:zip', 'S15', LIFT15, 0.15)

# 16: she opened it with one hand. Waist up on her, three-quarters to us, smiling at us, her bag in the other hand: the jar on its plinth at her
#     elbow; her wrist cocks, one flick: POP, the lid tumbles up toward us, face-on; behind the jar the guard's jaw drops, then the man's eyes come
#     out on stalks; she has not even looked (review 2: far, her face hidden, the lid edge-on, the two reactions cut by the frame)
D16 = st.dur('S16'); COCK16 = 0.2; POP16 = 0.42; LIDC = [JAR14[0], r(JAR14[1] + 0.204 * JS14), JAR14[2]]
NANF = lambda p_, hr, f, **kw: {'reach': {'R': [*p_, 1, 0.03]}, 'hands': {'R': hr, 'L': 'grip'}, 'face': f, **kw}
SMILE = {'lid': 0.3, 'mouth': 'smile'}
WOB16 = [r(POP16 + 0.5 + 0.1 * i) for i in range(6)]
st.shot('S16', 'mairie', setOpts=MUSEE, actors=[
        act('mamie', NAN16, -22, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon=NANF([0.16, r(LIDC[1] + 0.06), -1.14], 'pinch', SMILE), toonDur=0.0),
            k(COCK16, toon=NANF([0.25, r(LIDC[1] + 0.13), -1.08], 'pinch', SMILE, sq=[1.02, 0.98, 1.02]), toonDur=0.08, toonEase='out'),          # the wrist cocks (held four frames)...
            k(r(POP16 - 0.04), toon=NANF([0.1, r(LIDC[1] + 0.1), -1.16], 'point', {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}), toonDur=0.04, toonEase='in'),   # ...one flick...
            k(r(POP16 + 0.02), toon=NANF([0.34, r(LIDC[1] + 0.2), -1.04], 'point', {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}), toonDur=0.1, toonEase='out'),   # ...and the follow-through, a finger up
            k(r(POP16 + 0.4), toon=NANF([0.26, 1.2, -1.1], 'rest', SMILE), toonDur=0.25),
            k(r(POP16 + 0.62), toon=NANF([0.26, 1.2, -1.1], 'rest', {'lid': 1.0, 'mouth': 'smile'}), toonDur=0.07), k(r(POP16 + 0.76), toon=NANF([0.26, 1.2, -1.1], 'rest', SMILE), toonDur=0.1),   # a slow blink at us
            k(r(POP16 + 0.9), toon={'hands': {'R': 'rest', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.15)]),
        act('gardien', GAR16, 10, 'stand', 'neutral', keys=[k(0.0, look=LIDC), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.0),
            k(r(POP16 + 0.11), toon={'face': {'lid': 0.0, 'eye': 0.5, 'jaw': 1.0, 'jawBlock': 1, 'mouth': 'O', 'brow': 1.0}, 'sq': [0.92, 1.12, 0.92]}, toonDur=0.05, toonEase='out'),   # three frames later: his jaw drops (overshoot)...
            k(r(POP16 + 0.25), toon={'face': {'lid': 0.0, 'eye': 0.5, 'jaw': 0.8, 'jawBlock': 1, 'mouth': 'O', 'brow': 1.0}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.1),                  # ...settles...
            *[k(t_, toon={'face': {'lid': 0.0, 'eye': 0.5, 'jaw': 0.9 if i % 2 else 0.74, 'jawBlock': 1, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.08) for i, t_ in enumerate(WOB16)],   # ...and quivers
            k(r(POP16 + 0.3), look=[0.1, 2.9, -0.6], lookDur=0.15), k(r(POP16 + 0.75), look=[NAN16[0], 1.9, NAN16[2]], lookDur=0.15)]),
        act('mec', MEC16, 0, 'stand', 'neutral', keys=[k(0.0, look=LIDC), k(0.0, toon={'face': LIP}, toonDur=0.0),
            k(r(POP16 + 0.2), toon={'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.2, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.05, toonEase='out'),   # six frames later: his eyes come out on stalks...
            k(r(POP16 + 0.34), toon={'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.14, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.1),
            *[k(t_, toon={'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.17 if i % 2 else 0.12, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.08) for i, t_ in enumerate(WOB16)],   # ...and wobble
            k(r(POP16 + 0.3), look=[0.1, 2.9, -0.6], lookDur=0.15), k(r(POP16 + 0.8), look=[NAN16[0], 1.9, NAN16[2]], lookDur=0.15)])],
        props=[P('vitrine16', 'displayCase', pos=CASE, opts={**CASEO, 'noCover': True}),
               P('jar16', 'picklesJar', pos=JAR14, scale=JS14, opts={'openAt': POP16, 'lidFace': True, 'lidOut': True, 'lidArc': 0.3, 'lidFar': -0.45, 'lidZ': 0.5, 'lidFly': 0.4, 'lidSize': 1.15, 'hops': [[POP16, 0.008]]}),
               P('sac16', 'briefcase', on={'actor': 'mamie', 'hand': 'L', 'offset': [0.0, -0.1, 0.03]}, scale=0.55),
               BURST('pop16', [-0.02, r(LIDC[1] + 0.22), -1.12], r(POP16 + 0.06), 'POP !', 0.32, 0.34)],
        cams=[FC(0.0, [0.3, 1.4, 1.5], [[-0.9, 2.47, -2.32], [0.86, 1.5, NAN16[2]], [NAN16[0], 2.14, NAN16[2]], [0.0, 0.93, -0.9], [-0.14, 1.3, -1.2], [0.2, 2.44, -2.2]], top=0.12, bottom=0.76, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:pop', 'S16', POP16, 0.45)

# 17: he doesn't like pickles. Close on him: he holds the open jar she gave him, looks down into it, then at us, deadpan; a slow blink; he hands it back
D17 = st.dur('S17')
HOLD17 = lambda f, x=0.0, y=1.32, z=-0.05: {'reach': {'R': [x, y, z, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': f}
st.shot('S17', 'mairie', setOpts=MUSEE, actors=[act('mec', [-0.1, 0, -0.5], 10, 'stand', 'unimpressed', keys=[k(0.0, look=[0.0, 1.3, -0.05]), k(0.0, toon=HOLD17({'lid': 0.5, 'mouth': 'line', 'gy': 0.6}), toonDur=0.0),
            k(0.7, look='camera', lookDur=0.15), k(0.75, toon=HOLD17({'lid': 0.45, 'mouth': 'line'}), toonDur=0.12),
            k(1.2, toon=HOLD17({'lid': 1.0, 'mouth': 'line'}), toonDur=0.16, toonEase='inOut'), k(1.56, toon=HOLD17({'lid': 0.45, 'mouth': 'line'}), toonDur=0.16, toonEase='inOut'),   # (review 1) a slow blink
            k(1.75, toon=HOLD17({'lid': 0.45, 'mouth': 'line'}, 0.14, 1.36, 0.1), toonDur=0.25, toonEase='inOut')])],   # he hands it back (review 2: not so far: the jar left the frame)
        props=[P('jar17', 'picklesJar', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.1, 0.04], 'face': 'camera', 'faceFlat': True}, scale=JS14, opts={'lidGone': True})],
        cams=[FC(0.0, [0.45, 1.75, 1.0], [[-0.1, 2.4, -0.5], [-0.1, 1.15, -0.5], [0.15, 1.3, -0.05], [-0.4, 1.9, -0.5], [0.3, 1.36, 0.1]], top=0.12, bottom=0.78)])

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
ASTROC = {'preset': 'worker', 'outfit': 'swat', 'hat': 'none', 'suit': '#F2F2EE', 'pants': '#F2F2EE', 'lapel': '#F2F2EE', 'shoes': '#F2F2EE', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}   # (review 1) a plain white suit (the business suit showed its lapels)
ASTROF = [('none', 'buzz', '#3A2A1E'), ('mustache', 'curly', '#6B4A2E'), ('beard', 'crew', '#1C1C1E'), ('none', 'slick', '#C9A15A'), ('mustache', 'receding', '#8A8A8A'), ('beard', 'buzz', '#5A3A22')]
st.write("Le bocal", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'pompier1': {'preset': 'pompier', 'seed': 781, 'suit': '#23304E', 'pants': '#23304E', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'pompier2': {'preset': 'pompier', 'seed': 782, 'suit': '#23304E', 'pants': '#23304E', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'astro{j + 1}': {**ASTROC, 'seed': 783 + j, 'facial': ASTROF[j][0], 'hair': ASTROF[j][1], 'hairColor': ASTROF[j][2]} for j in range(6)},
    'savant1': {'preset': 'savant', 'seed': 790, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant2': {'preset': 'savant', 'seed': 791, 'hairColor': '#6B4A2E', 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'visiteur1': {'preset': 'boss', 'seed': 792, 'suit': '#5A6470', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'visiteur2': {'preset': 'madame', 'seed': 793, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'gardien': {'preset': 'cop', 'seed': 794, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'mamie': {'preset': 'mamie', 'seed': 795, 'suit': '#C77DA0', 'build': {'width': 0.92, 'headWidth': 1.25, 'height': 0.88}, 'toon': EX},
})
