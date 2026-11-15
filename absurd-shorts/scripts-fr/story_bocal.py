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
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
LIP = {'lid': 0.45, 'mouth': 'line'}
STREET = {'eiffelStyle': 'v2', 'clear': [-6.0, 6.0], 'clearL': [-6.0, 6.0]}
MUSEE = {'desk': False, 'banner': False, 'map': False, 'plate': 'MUSÉE'}

JS = 1.4; JH = r(0.204 * JS)                         # the jar's scale and the height of its lid above its base
TABLE = [0.0, 0, -1.2]; TH = 0.76                   # his kitchen table
MEK = [0.0, 0, -1.85]                               # him behind it, facing us

for g_ in [('S01', 1.6, 'mec', 'strain'), ('S06', 0.32, 'pompier1', 'snap'), ('S13', 0.45, 'savant1', 'burnt'), ('S16', 0.75, 'mamie', 'pop'), ('S17', 1.3, 'mec', 'end')]:
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
       k(r(SLIP1 + 0.3), toon={'reach': {'L': GRIP1()['reach']['L'], 'R': [r(JAR1[0] - 0.3), 1.45, r(JAR1[2] + 0.15), 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'rest'}, 'lay': [0.0, 0.0], 'face': {'lid': 0.45, 'mouth': 'line', 'blush': 0.6}}, toonDur=0.2)]
st.shot('S01', 'kitchenDay', actors=[act('mec', MEK, 0, 'stand', 'determined', keys=K1)],
        props=[P('jar1', 'picklesJar', pos=JAR1, scale=JS, opts={'shake': [[0.3, 2.1]]})],
        cams=[FC(0.0, [0.6, 1.6, 0.4], [[0.0, 2.38, -1.85], [0.0, 0.95, -1.85], [r(JAR1[0] - 0.25), JAR1[1], JAR1[2]], [r(JAR1[0] + 0.3), r(JAR1[1] + 0.4), JAR1[2]], [-0.6, 2.0, -1.6]], top=0.12, bottom=0.76)])
for t_ in STRAIN1: st.cue('sfx:squeak', 'S01', t_, 0.14)
st.cue('whoosh', 'S01', SLIP1, 0.3, 0.25, 1500, 500)

# 2: he tapped the lid with a spoon. Close on the jar on the table: his spoon taps the lid, tink, tink, then a big tap: the spoon bends flat
D2 = st.dur('S02'); JAR2 = [0.0, TH, -1.25]; TAPS2 = [0.35, 0.8, 1.3]
SPOON2 = lambda dy, f: {'reach': {'R': [0.05, r(TH + JH + dy), -1.27, 1, 0.03], 'L': [0.11, r(TH + 0.12), -1.22, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f}
K2 = [k(0.0, look=[JAR2[0], r(TH + JH), JAR2[2]]), k(0.0, toon=SPOON2(0.16, {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}), toonDur=0.0)]
for i, t_ in enumerate(TAPS2):
    up = 0.16 + 0.12 * (i == 2)
    K2 += [k(r(t_ - 0.14), toon=SPOON2(up, {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}), toonDur=0.1, toonEase='out'), k(t_, toon={**SPOON2(0.03, {'lid': 0.5, 'mouth': 'clench' if i == 2 else 'line', 'brow': -0.5}), 'sq': [1.03, 0.97, 1.03]}, toonDur=0.05, toonEase='in')]
K2 += [k(r(TAPS2[-1] + 0.2), look=[0.05, r(TH + JH + 0.2), -1.27]), k(r(TAPS2[-1] + 0.5), look='camera'), k(r(TAPS2[-1] + 0.5), toon=SPOON2(0.18, {'lid': 0.45, 'mouth': 'line'}), toonDur=0.15)]
st.shot('S02', 'kitchenDay', actors=[act('mec', MEK, 0, 'stand', 'neutral', keys=K2)],
        props=[P('table2', 'table', pos=TABLE, opts={'w': 1.0, 'd': 0.7, 'h': TH}), P('jar2', 'picklesJar', pos=JAR2, scale=JS),
               P('cuil2', 'spoon', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.05, 0.03]}, scale=1.8, keys=[k(TAPS2[-1], squash=[1.4, 0.45, 1.4], dur=0.25)])],   # the last tap folds the spoon
        cams=[FC(0.0, [0.32, 1.22, -0.5], [[JAR2[0], TH, JAR2[2]], [JAR2[0], r(TH + 0.5), JAR2[2]], [-0.18, r(TH + 0.2), JAR2[2]], [0.22, r(TH + 0.2), JAR2[2]], [0.0, 2.05, -1.85]], top=0.1, bottom=0.74)])
for t_ in TAPS2: st.cue('sfx:tick', 'S02', t_, 0.3)

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
               P('vap3', 'dustPuff', pos=[0.0, r(JAR3[1] + JH - 0.05), -1.36], scale=0.45, opts={'color': '#FFFFFF', 'period': 0.8, 'seed': 31}),
               P('vap3b', 'dustPuff', pos=[0.06, r(JAR3[1] + JH - 0.05), -1.4], scale=0.35, opts={'color': '#FFFFFF', 'period': 0.65, 'seed': 37})],
        cams=[FC(0.0, [1.55, 1.65, -2.5], [[0.0, 2.38, -0.72], [-0.32, 1.6, -0.72], [0.32, 1.6, -0.72], [0.0, 0.74, -1.38], [0.0, 1.22, -1.53]], top=0.12, bottom=0.76, inside=(-6.8, 6.8, 0.3, 4.0, -2.9, 13.0))])
st.cue('sfx:pour', 'S03', 0.0, 0.35)

# 4: he called the fire brigade. His street: the fire engine pulls up at his door with a bounce, siren going, two firemen jump down and run in
D4 = st.dur('S04'); TRK4 = [2.4, 0, -1.2]
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        *[act(f'pompier{j + 1}', [r(3.3 + 0.2 * j), 0, r(-0.9 - 0.9 * j)], 90, 'stand', 'determined', keys=[k(0.0, visible=False), k(r(0.7 + 0.08 * j), visible=True),
            k(r(0.72 + 0.08 * j), to=[r(5.0 - 0.05 * j), 0, r(-0.2 - 0.5 * j)], dur=0.55, clip='run', ease='linear'), k(0.0, look=[5.6, 1.6, 0.0])]) for j in range(2)]],
        props=[P('camion4', 'fireTruck', pos=[TRK4[0], 0, -12.0], ry=0, keys=[k(0.0, to=TRK4, dur=0.62, ease='out'), k(0.62, squash=[1.03, 0.9, 1.03], dur=0.4)])],
        cams=[FC(0.0, [-0.6, 1.1, 5.2], [[TRK4[0], 3.2, TRK4[2]], [TRK4[0], 0.0, 1.6], [5.6, 2.6, 0.0], [5.6, 0.0, 0.6], [1.0, 0.0, 0.0]], top=0.14, bottom=0.78)])
st.cue('sfx:siren', 'S04', 0.0, 0.35); st.cue('sfx:brake', 'S04', 0.5, 0.3)

# 5: they brought out the big jaws. In the kitchen: one fireman clamps the hydraulic jaws on the lid, straining, the other holds the jar steady
D5 = st.dur('S05'); JAR5 = [0.0, TH, -1.25]; JAWP = [0.72, r(TH + JH - 0.02), -0.48]; JAWRY = -137
OPEN5 = [[0.0, 1.0], [0.25, 1.0], [0.5, 0.22], [0.75, 0.28], [1.0, 0.16], [1.25, 0.22], [1.5, 0.14], [1.76, 0.18]]
HOLD5 = lambda f, sq=None: {'reach': {'R': [0.86, r(JAWP[1] + 0.12), -0.36, 1, 0.03], 'L': [0.66, r(JAWP[1] + 0.06), -0.56, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f, **({'sq': sq} if sq else {})}
STEADY = lambda f: {'reach': {'L': [-0.1, r(TH + 0.12), -1.24, 1, 0.03], 'R': [0.1, r(TH + 0.12), -1.24, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': f}
st.shot('S05', 'kitchenDay', actors=[
        act('pompier1', [1.15, 0, -0.05], JAWRY, 'stand', 'determined', keys=[k(0.0, look=[JAR5[0], r(TH + JH), JAR5[2]]), k(0.0, toon=HOLD5({'lid': 0.4, 'mouth': 'line', 'brow': -0.5}), toonDur=0.0),
            *[k(t_, toon=HOLD5({'lid': 0.75, 'mouth': 'clench', 'brow': -0.9, 'vein': 1.0, 'blush': 0.6}, [1.06, 0.93, 1.06] if i % 2 == 0 else [0.98, 1.03, 0.98]), toonDur=0.08) for i, t_ in enumerate([0.5, 0.75, 1.0, 1.25, 1.5])]]),
        act('pompier2', [-0.3, 0, -1.85], 15, 'stand', 'neutral', keys=[k(0.0, look=[JAR5[0], r(TH + JH), JAR5[2]]), k(0.0, toon=STEADY({'lid': 0.5, 'mouth': 'line'}), toonDur=0.0), k(1.3, toon=STEADY({'lid': 0.6, 'mouth': 'wavy', 'sweat': 1.0}), toonDur=0.1)])],
        props=[P('table5', 'table', pos=TABLE, opts={'w': 1.0, 'd': 0.7, 'h': TH}), P('jar5', 'picklesJar', pos=JAR5, scale=JS, opts={'shake': [[0.5, 1.76]]}),
               P('pince5', 'rescueJaws', pos=JAWP, ry=JAWRY, opts={'s': 1.2, 'open': OPEN5})],
        cams=[FC(0.0, [-0.9, 1.55, 0.55], [[JAR5[0], r(TH + JH + 0.1), JAR5[2]], [1.15, 2.4, -0.05], [-0.3, 2.4, -1.85], [JAWP[0], TH, JAWP[2]], [JAR5[0], TH, JAR5[2]], [1.15, 0.0, -0.05], [-0.3, 0.0, -1.85]], top=0.12, bottom=0.74)])
st.cue('sfx:rattle', 'S05', 0.45, 0.3); st.cue('sfx:squeak', 'S05', 1.0, 0.2)

# 6: the jaws broke. Tighter: CRAC, the arms snap off and fly apart in a puff; the fireman shoots back with his eyes out on stalks, the other freezes
D6 = st.dur('S06'); BRK6 = 0.25
st.shot('S06', 'kitchenDay', actors=[
        act('pompier1', [1.15, 0, -0.05], JAWRY, 'stand', 'determined', keys=[k(0.0, look=[JAR5[0], r(TH + JH), JAR5[2]]), k(0.0, toon=HOLD5({'lid': 0.75, 'mouth': 'clench', 'brow': -0.9, 'vein': 1.0}, [1.06, 0.93, 1.06]), toonDur=0.0),
            k(BRK6, toon={'reach': {'R': [1.0, 1.75, 0.2, 1, 0.03], 'L': [1.4, 1.7, 0.1, 1, 0.03]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'lay': [-0.3, 0.0], 'sq': [0.9, 1.12, 0.9],
                          'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.14, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05, toonEase='out'),   # thrown back, eyes on stalks
            k(r(BRK6 + 0.5), toon={'reach': {'R': [1.0, 1.4, 0.1, 1, 0.03], 'L': [1.35, 1.4, 0.05, 1, 0.03]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'lay': [-0.08, 0.0], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.2)]),
        act('pompier2', [-0.3, 0, -1.85], 15, 'stand', 'neutral', keys=[k(0.0, look=[JAR5[0], r(TH + JH), JAR5[2]]), k(0.0, toon=STEADY({'lid': 0.6, 'mouth': 'wavy', 'sweat': 1.0}), toonDur=0.0),
            k(r(BRK6 + 0.05), toon={**STEADY({'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}), 'sq': [0.95, 1.06, 0.95]}, toonDur=0.05), k(r(BRK6 + 0.4), look='camera')])],
        props=[P('table6', 'table', pos=TABLE, opts={'w': 1.0, 'd': 0.7, 'h': TH}), P('jar6', 'picklesJar', pos=JAR5, scale=JS),
               P('pince6', 'rescueJaws', pos=JAWP, ry=JAWRY, opts={'s': 1.2, 'open': [[0.0, 0.16]], 'breakAt': BRK6}),
               BURST('crac6', [0.35, r(TH + 0.75), -0.9], r(BRK6 + 0.02), 'CRAC !', 0.42, 0.3)],
        cams=[FC(0.0, [-0.55, 1.4, 0.15], [[JAR5[0], r(TH + JH + 0.15), JAR5[2]], [1.15, 2.4, -0.05], [JAR5[0], TH, JAR5[2]], [0.35, r(TH + 1.0), -0.9]], top=0.12, bottom=0.74)])
st.cue('sfx:crunch', 'S06', BRK6, 0.45); st.cue('clang', 'S06', r(BRK6 + 0.3), 0.2)

# 7: the army sent a tank. His street from the kerb, low: the jar stands in the middle of the road, big in the foreground; a tank rumbles down at it
D7 = st.dur('S07'); JR = [0.0, 0, 2.6]; TK = 4.5
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('jar7', 'picklesJar', pos=JR, scale=2.2), P('char7', 'armyTank', pos=[0.0, 0, -14.0], ry=0, scale=TK, keys=[k(0.0, to=[0.0, 0, -4.0], dur=D7, ease='linear')])],
        cams=[FC(0.0, [0.55, 0.32, 4.4], [[JR[0], 0.0, JR[2]], [JR[0], 0.55, JR[2]], [0.0, 2.6, -6.0], [-1.6, 0.0, -6.0], [1.6, 0.0, -6.0]], top=0.14, bottom=0.78)])
st.cue('engine', 'S07', 0.0, 0.35)

# 8: the tank drove over it. From the side, low: the tank's tracks roll over the jar; the whole tank bucks up over it and lands; the jar stands
D8 = st.dur('S08')
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('jar8', 'picklesJar', pos=JR, scale=2.2),
               P('char8', 'armyTank', pos=[0.0, 0, -2.6], ry=0, scale=TK, keys=[k(0.0, to=[0.0, 0, 0.9], dur=0.5, ease='linear'), k(0.5, to=[0.0, 0.45, 2.6], dur=0.3, ease='out'), k(0.8, to=[0.0, 0.45, 3.8], dur=0.28, ease='linear'),
                                                                                    k(1.08, to=[0.0, 0.0, 5.0], dur=0.2, ease='in'), k(1.28, to=[0.0, 0.0, 6.4], dur=0.4, ease='out'), k(1.28, squash=[1.04, 0.9, 1.04], dur=0.35)])],   # it bucks over the jar
        cams=[FC(0.0, [6.4, 0.75, 2.6], [[JR[0], 0.0, JR[2]], [JR[0], 0.6, JR[2]], [0.0, 2.9, 0.0], [0.0, 0.0, -1.0], [0.0, 0.0, 6.0]], top=0.14, bottom=0.78)])
st.cue('engine', 'S08', 0.0, 0.3); st.cue('clang', 'S08', 0.55, 0.35); st.cue('thud', 'S08', 1.28, 0.3)

# 9: the tank got a flat. Behind the jar in the foreground: the tank sags down on one side with a hiss, a puff of dust; the jar has not a scratch
D9 = st.dur('S09'); TK9 = [0.0, 0, 6.4]
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('jar9', 'picklesJar', pos=JR, scale=2.2), P('char9', 'armyTank', pos=TK9, ry=0, scale=TK, keys=[k(0.2, rotTo=[0.0, 0.0, -0.14], dur=0.45, ease='out'), k(0.2, to=[0.0, -0.18, TK9[2]], dur=0.45, ease='out')]),
               P('pff9', 'dustPuff', pos=[1.1, 0.3, TK9[2]], opts={'color': '#D9D2C4', 'count': 8, 'size': 0.5, 'period': 0.5, 'startAt': 0.2, 'once': True})],
        cams=[FC(0.0, [-0.9, 0.45, 0.4], [[JR[0], 0.0, JR[2]], [JR[0], 0.55, JR[2]], [0.0, 2.8, TK9[2]], [-1.8, 0.0, TK9[2]], [1.8, 0.0, TK9[2]]], top=0.2, bottom=0.78)])
st.cue('whoosh', 'S09', 0.2, 0.3, 0.6, 3000, 600)

# 10: it was sent into space. A launch pad in the fields, low: the rocket lifts off in a cloud of smoke and climbs out of the top of the frame
D10 = st.dur('S10'); RK = [0.0, 0, -4.0]
st.shot('S10', 'grassland', actors=[],
        props=[P('fusee10', 'rocket', pos=RK, opts={'flame': True}, keys=[k(0.3, to=[RK[0], 16.0, RK[2]], dur=r(D10 - 0.3), ease='in')]),
               P('fum10', 'dustPuff', pos=[RK[0], 0.3, RK[2]], opts={'color': '#F0EEEA', 'count': 16, 'size': 1.1, 'period': 0.9, 'startAt': 0.15})],
        cams=[FC(0.0, [3.8, 0.7, 4.0], [[RK[0], 0.0, RK[2]], [RK[0], 5.8, RK[2]], [-2.0, 0.0, RK[2]], [2.0, 0.0, RK[2]]], top=0.12, bottom=0.78)])
st.cue('engine', 'S10', 0.1, 0.4); st.cue('whoosh', 'S10', 0.3, 0.4, 1.2, 200, 1200)

# 11: six astronauts tried. Inside the space module: the jar floats in the middle, six astronauts round it in zero gravity, all pulling on the
#     lid together, leaning back on each heave; then all six spin round like tops
D11 = st.dur('S11'); JAR11 = [0.0, 1.95, -0.7]; N11 = 6; SPIN11 = 1.45
ASTRO = []
for j in range(N11):
    a = j / N11 * 2 * PI + 0.3; px = r(JAR11[0] + 1.0 * math.cos(a)); pz = r(JAR11[2] + 0.75 * math.sin(a)); py = r(0.75 + 0.35 * (j % 3) / 2)
    ry = r(math.degrees(math.atan2(JAR11[0] - px, JAR11[2] - pz)))
    ASTRO.append((f'astro{j + 1}', [px, py, pz], ry))
PULL11 = lambda pos, lay=0.0, sq=None: {'reach': {'R': [r(JAR11[0] + 0.25 * (pos[0] - JAR11[0])), r(JAR11[1] + JH), r(JAR11[2] + 0.25 * (pos[2] - JAR11[2])), 1, 0.03],
                                                 'L': [r(JAR11[0] + 0.3 * (pos[0] - JAR11[0])), r(JAR11[1] + 0.15), r(JAR11[2] + 0.3 * (pos[2] - JAR11[2])), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'},
                                        'lay': [lay, 0.0], 'face': {'lid': 0.6, 'mouth': 'clench', 'brow': -0.7}, **({'sq': sq} if sq else {})}
st.shot('S11', 'stationInside', actors=[*[act(n_, p_, ry_, 'stand', 'determined', keys=[k(0.0, look=[JAR11[0], r(JAR11[1] + 0.2), JAR11[2]]), k(0.0, toon=PULL11(p_), toonDur=0.0),
            *[kk for t_ in (0.4, 0.8, 1.2) for kk in (k(t_, toon=PULL11(p_, -0.25, [0.95, 1.07, 0.95]), toonDur=0.08, toonEase='out'), k(r(t_ + 0.18), toon=PULL11(p_, 0.0), toonDur=0.12))],
            k(SPIN11, toon={'yaw': 2 * PI * 2, 'lay': [0.15, 0.0], 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}}, toonDur=r(D11 - SPIN11), toonEase='linear')]) for n_, p_, ry_ in ASTRO]],   # they let go and spin like tops
        props=[P('jar11', 'picklesJar', pos=JAR11, scale=JS, keys=[k(0.0, rotTo=[0.15, 0.6, 0.1], dur=D11, ease='linear')]),
               *[P(f'casque11{j}', 'spaceHelmet', on={'actor': n_, 'joint': 'head', 'offset': [0.0, -0.02, 0.0]}, opts={'r': 0.34}) for j, (n_, p_, ry_) in enumerate(ASTRO)]],
        cams=[FC(0.0, [1.9, 2.05, 2.7], [[-1.1, 3.0, -0.7], [1.1, 3.0, -0.7], [0.0, 1.95, -1.6], [0.0, 1.95, 0.2], *[p_ for n_, p_, ry_ in ASTRO]], top=0.12, bottom=0.74, inside=(-3.0, 3.0, 0.4, 3.8, -2.2, 5.5))])
st.cue('sfx:squeak', 'S11', 0.4, 0.2); st.cue('sfx:squeak', 'S11', 0.8, 0.2); st.cue('sfx:squeak', 'S11', 1.2, 0.2); st.cue('whoosh', 'S11', SPIN11, 0.3, 0.6, 600, 1400)

# 12: the scientists fired a laser. In a lab: the jar on a stand; a scientist at a laser cannon presses the trigger, the red beam hits the lid
D12 = st.dur('S12'); JAR12 = [0.0, 0.9, -1.0]; GUN = [1.55, 1.0, -1.0]; FIRE12 = 0.6
GUNK = lambda f, press=False: {'reach': {'R': [r(GUN[0] + 0.12), r(GUN[1] + (0.14 if press else 0.2)), r(GUN[2] + 0.12), 1, 0.03], 'L': [r(GUN[0] + 0.12), r(GUN[1] + 0.1), r(GUN[2] - 0.15), 1, 0.03]}, 'hands': {'R': 'point', 'L': 'grip'}, 'face': f}
st.shot('S12', 'lab', actors=[
        act('savant1', [2.1, 0, -0.85], -95, 'stand', 'determined', keys=[k(0.0, look=[JAR12[0], r(JAR12[1] + 0.2), JAR12[2]]), k(0.0, toon=GUNK({'lid': 0.4, 'mouth': 'line', 'brow': -0.5}), toonDur=0.0),
            k(FIRE12, toon={**GUNK({'lid': 0.6, 'mouth': 'smirk', 'brow': -0.6}, True), 'sq': [1.03, 0.97, 1.03]}, toonDur=0.06), k(r(FIRE12 + 0.6), toon=GUNK({'lid': 0.5, 'mouth': 'smile', 'brow': -0.2}), toonDur=0.15)]),
        act('savant2', [1.2, 0, -2.0], -40, 'stand', 'neutral', keys=[k(0.0, look=[2.1, 1.9, -0.85]), k(r(FIRE12 + 0.05), look=[JAR12[0], r(JAR12[1] + 0.2), JAR12[2]]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(0.3, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06), k(0.42, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.08), k(r(FIRE12 + 0.1), toon={'face': {'lid': 0.1, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.08),
            k(1.45, toon={'face': {'lid': 1.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.06), k(1.57, toon={'face': {'lid': 0.1, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.08)])],
        props=[P('socle12', 'table', pos=[JAR12[0], 0, JAR12[2]], opts={'w': 0.5, 'd': 0.5, 'h': JAR12[1]}), P('jar12', 'picklesJar', pos=JAR12, scale=JS),
               P('canon12', 'slab', pos=GUN, opts={'w': 0.5, 'h': 0.26, 'd': 0.3, 'color': '#4A5560', 'outline': 0.006}), P('pied12', 'slab', pos=[GUN[0], r(GUN[1] / 2 - 0.07), GUN[2]], opts={'w': 0.08, 'h': r(GUN[1] - 0.14), 'd': 0.08, 'color': '#2E343A'}),
               P('laser12', 'laserBeam', pos=[r(GUN[0] - 0.25), GUN[1], GUN[2]], opts={'vec': [r(JAR12[0] - GUN[0] + 0.33), r(JAR12[1] + JH * 0.6 - GUN[1]), 0.0], 'r': 0.022}, keys=[k(0.0, visible=False), k(FIRE12, visible=True)])],
        cams=[FC(0.0, [0.9, 1.45, 1.6], [[JAR12[0], r(JAR12[1] + 0.4), JAR12[2]], [2.1, 2.4, -0.85], [JAR12[0], 0.0, JAR12[2]], [GUN[0], 0.6, GUN[2]]], top=0.12, bottom=0.76)])
st.cue('sfx:click', 'S12', FIRE12, 0.3); st.cue('whoosh', 'S12', FIRE12, 0.3, 0.8, 4000, 2000)

# 13: the laser bounced back. Closer on the scientist: the beam glints off the jar and comes straight back; his hair stands up, frizzled, his face
#     sooty, a puff of smoke; he blinks
D13 = st.dur('S13'); BACK13 = 0.3; HEAD13 = [2.1, 2.05, -0.85]
st.shot('S13', 'lab', actors=[act('savant1', [2.1, 0, -0.85], -95, 'stand', 'determined', keys=[k(0.0, look=[JAR12[0], r(JAR12[1] + 0.2), JAR12[2]]), k(0.0, toon=GUNK({'lid': 0.6, 'mouth': 'smirk', 'brow': -0.6}, True), toonDur=0.0),
            k(BACK13, toon={**GUNK({'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}, True), 'hairUp': 1.0, 'sq': [0.92, 1.1, 0.92], 'skin': {'color': '#3A3530', 'k': 0.55, 'fill': 1.0}}, toonDur=0.04, toonEase='out'),   # zapped
            k(r(BACK13 + 0.5), toon={**GUNK({'lid': 1.0, 'mouth': 'line'}), 'hairUp': 1.0, 'skin': {'color': '#3A3530', 'k': 0.55, 'fill': 1.0}}, toonDur=0.06),
            k(r(BACK13 + 0.62), toon={**GUNK({'lid': 0.3, 'mouth': 'line'}), 'hairUp': 1.0, 'skin': {'color': '#3A3530', 'k': 0.55, 'fill': 1.0}}, toonDur=0.08), k(r(BACK13 + 0.75), look='camera')])],
        props=[P('socle13', 'table', pos=[JAR12[0], 0, JAR12[2]], opts={'w': 0.5, 'd': 0.5, 'h': JAR12[1]}), P('jar13', 'picklesJar', pos=JAR12, scale=JS, opts={'glint': [[0.22, 0.45]]}),
               P('canon13', 'slab', pos=GUN, opts={'w': 0.5, 'h': 0.26, 'd': 0.3, 'color': '#4A5560', 'outline': 0.006}),
               P('laser13a', 'laserBeam', pos=[r(GUN[0] - 0.25), GUN[1], GUN[2]], opts={'vec': [r(JAR12[0] - GUN[0] + 0.33), r(JAR12[1] + JH * 0.6 - GUN[1]), 0.0], 'r': 0.022}, keys=[k(r(BACK13 + 0.05), visible=False)]),
               P('laser13b', 'laserBeam', pos=[r(JAR12[0] + 0.08), r(JAR12[1] + JH * 0.6), JAR12[2]], opts={'vec': [r(HEAD13[0] - JAR12[0] - 0.08), r(HEAD13[1] + 0.2 - JAR12[1] - JH * 0.6), r(HEAD13[2] - JAR12[2])], 'r': 0.022}, keys=[k(0.0, visible=False), k(0.22, visible=True), k(r(BACK13 + 0.1), visible=False)]),   # back at his head
               P('fumee13', 'dustPuff', pos=[HEAD13[0], r(HEAD13[1] + 0.5), HEAD13[2]], opts={'color': '#5A5650', 'count': 7, 'size': 0.3, 'period': 0.6, 'startAt': BACK13, 'once': True})],
        cams=[FC(0.0, [-0.6, 1.75, -0.3], [[2.1, 2.65, -0.85], [2.1, 1.1, -0.85], [JAR12[0], r(JAR12[1] + JH + 0.03), JAR12[2]], [JAR12[0], JAR12[1], JAR12[2]]], top=0.12, bottom=0.76)])
st.cue('sfx:ding', 'S13', 0.22, 0.25); st.cue('sfx:crunch', 'S13', BACK13, 0.25)

# 14: the jar became a historic monument. A museum hall: the jar alone in a lit display case on a white plinth, MONUMENT HISTORIQUE on its label;
#     two visitors admire it, one takes a photo; a guard stands by, hands behind his back (HISTORIQUE)
D14 = st.dur('S14'); CASE = [0.0, 0, -1.2]; JAR14 = [0.0, 1.0, -1.2]
st.shot('S14', 'mairie', setOpts=MUSEE, actors=[
        act('visiteur1', [-0.95, 0, -0.55], 40, 'stand', 'neutral', keys=[k(0.0, look=[JAR14[0], 1.15, JAR14[2]]), *[k(t_, toon={'reach': {'R': [-0.72, 1.7, -0.75, 1, 0.03], 'L': [-0.8, 1.7, -0.62, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': l_, 'mouth': 'line'}, **({'sq': [1.02, 0.97, 1.02]} if t_ == 0.5 else {})}, toonDur=0.06) for t_, l_ in ((0.0, 0.4), (0.5, 0.8), (0.62, 0.4), (1.6, 1.0), (1.72, 0.4))]]),   # a photo (squints at the click), a blink
        act('visiteur2', [0.95, 0, -0.5], -35, 'stand', 'happy', keys=[k(0.0, look=[JAR14[0], 1.15, JAR14[2]]), k(1.1, look=[-0.95, 1.9, -0.55]), k(1.8, look=[JAR14[0], 1.15, JAR14[2]]),
            *[k(t_, toon={'touch': {'R': ['face', 0.0, 0.18, 0.08, 1, 0.02]}, 'hands': {'R': 'rest'}, 'face': {'lid': l_, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.06) for t_, l_ in ((0.0, 0.2), (0.85, 1.0), (0.97, 0.2))]]),   # a blink, a glance at the photographer
        act('gardien', [1.5, 0, -1.9], -20, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.0)])],
        props=[P('vitrine14', 'displayCase', pos=CASE, opts={'w': 0.45, 'h': 1.0, 'text': 'MONUMENT HISTORIQUE'}), P('jar14', 'picklesJar', pos=JAR14, scale=1.2),
               P('photo14', 'handset', on={'actor': 'visiteur1', 'hand': 'R', 'offset': [0.0, -0.03, 0.03]}),
               P('casq14', 'copCap', on={'actor': 'gardien', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}, opts={'color': '#26365F'})],
        cams=[FC(0.0, [0.9, 1.6, 2.4], [[0.0, 2.35, -1.2], [0.0, 0.0, -1.2], [-1.1, 2.3, -0.75], [1.1, 2.3, -0.75]], top=0.12, bottom=0.78)])
st.cue('sfx:shutter', 'S14', 0.5, 0.2)

# 15: then his grandmother came by. In the museum: a little old lady with her handbag trots in past the guard, straight to the case; he follows
D15 = st.dur('S15'); NAN15 = [2.4, 0, -0.3]; NAN15E = [0.55, 0, -0.95]
st.shot('S15', 'mairie', setOpts=MUSEE, actors=[
        act('mamie', NAN15, -110, 'walk', 'happy', keys=[k(0.0, to=NAN15E, dur=1.15, clip='walk', then='stand', ease='out'), k(0.0, look=[JAR14[0], 1.2, JAR14[2]]), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0), k(1.25, look='camera')]),
        act('mec', [-0.9, 0, -0.4], 30, 'stand', 'neutral', keys=[k(0.0, look=[2.0, 1.6, -0.3]), k(0.0, toon={'face': LIP}, toonDur=0.0), k(0.6, look=[1.0, 1.4, -0.8])]),
        act('gardien', [1.5, 0, -1.9], -20, 'stand', 'neutral', keys=[k(0.0, look=[2.2, 1.4, -0.3]), k(0.7, look=[0.8, 1.4, -0.9]), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.0)])],
        props=[P('vitrine15', 'displayCase', pos=CASE, opts={'w': 0.45, 'h': 1.0, 'text': 'MONUMENT HISTORIQUE'}), P('jar15', 'picklesJar', pos=JAR14, scale=1.2),
               P('sac15', 'briefcase', on={'actor': 'mamie', 'hand': 'L', 'offset': [0.0, -0.1, 0.03]}, scale=0.55),
               P('casq15', 'copCap', on={'actor': 'gardien', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}, opts={'color': '#26365F'})],
        cams=[FC(0.0, [0.4, 1.5, 2.6], [[0.0, 2.3, -1.2], [2.4, 2.2, -0.3], [-0.9, 2.4, -0.4], [0.0, 0.0, -1.2]], top=0.12, bottom=0.78)])
st.cue('sfx:stepSoft', 'S15', 0.2, 0.15); st.cue('sfx:stepSoft', 'S15', 0.55, 0.15); st.cue('sfx:stepSoft', 'S15', 0.9, 0.15)

# 16: she opened it with one hand. Close: she lifts the glass, picks the jar up in her left hand and gives the lid one flick of the right: POP, the lid
#     flies; behind her the guard's jaw drops and the man's eyes pop out
D16 = st.dur('S16'); LIFT16 = 0.1; TAKE16 = 0.32; POP16 = 0.72
NANH = lambda f, rr: {'reach': {'L': [0.42, 1.32, -0.92, 1, 0.03], 'R': rr}, 'hands': {'L': 'grip', 'R': 'pinch'}, 'face': f}
st.shot('S16', 'mairie', setOpts=MUSEE, actors=[
        act('mamie', NAN15E, -110, 'stand', 'happy', keys=[k(0.0, look=[0.4, 1.4, -0.95]), k(0.0, toon={'reach': {'L': [0.08, 1.12, -1.2, 1, 0.03], 'R': [0.22, 1.3, -1.12, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
            k(TAKE16, toon=NANH({'lid': 0.3, 'mouth': 'smile'}, [0.4, 1.62, -0.88, 1, 0.03]), toonDur=0.15, toonEase='out'),
            k(r(POP16 - 0.06), toon=NANH({'lid': 0.4, 'mouth': 'smile'}, [0.36, 1.63, -0.9, 1, 0.03]), toonDur=0.05), k(POP16, toon=NANH({'lid': 0.2, 'mouth': 'smile', 'brow': 0.3}, [0.5, 1.7, -0.84, 1, 0.03]), toonDur=0.04, toonEase='out'),   # one flick
            k(r(POP16 + 0.35), look='camera')]),
        act('mec', [-0.9, 0, -0.4], 30, 'stand', 'neutral', keys=[k(0.0, look=[0.45, 1.4, -0.95]), k(0.0, toon={'face': LIP}, toonDur=0.0),
            k(r(POP16 + 0.04), toon={'sq': [0.93, 1.1, 0.93], 'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.14, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05, toonEase='out')]),
        act('gardien', [1.5, 0, -1.9], -20, 'stand', 'neutral', keys=[k(0.0, look=[0.45, 1.4, -0.95]), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.0),
            k(r(POP16 + 0.06), toon={'face': {'lid': 0.0, 'eye': 0.5, 'jaw': 0.8, 'jawBlock': 1, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.06, toonEase='out')])],   # his jaw drops
        props=[P('vitrine16', 'displayCase', pos=CASE, opts={'w': 0.45, 'h': 1.0, 'text': 'MONUMENT HISTORIQUE', 'liftAt': LIFT16}),
               P('jar16', 'picklesJar', pos=JAR14, scale=1.2, opts={'openAt': POP16}, keys=[k(TAKE16, attach='mamie', hand='L', offset=[0.0, -0.1, 0.04], face='camera', faceFlat=True)]),
               P('sac16', 'briefcase', on={'actor': 'mamie', 'joint': 'torso', 'offset': [0.22, -0.05, 0.05]}, scale=0.55),
               P('casq16', 'copCap', on={'actor': 'gardien', 'joint': 'head', 'offset': [0.0, 0.45, 0.0]}, opts={'color': '#26365F'}),
               BURST('pop16', [0.1, 2.05, -0.7], r(POP16 + 0.02), 'POP !', 0.36, 0.3)],
        cams=[FC(0.0, [0.65, 1.6, 1.1], [[0.55, 2.2, -0.95], [0.45, 1.25, -0.95], [-0.9, 2.4, -0.4], [0.1, 2.25, -0.7]], top=0.12, bottom=0.76)])
st.cue('sfx:zip', 'S16', LIFT16, 0.15); st.cue('sfx:pop', 'S16', POP16, 0.45)

# 17: he doesn't like pickles. Close on him: he holds the open jar she gave him, looks down into it, then at us, deadpan; a slow blink; he hands it back
D17 = st.dur('S17')
HOLD17 = lambda f, x=0.0, y=1.32, z=-0.05: {'reach': {'R': [x, y, z, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': f}
st.shot('S17', 'mairie', setOpts=MUSEE, actors=[act('mec', [-0.1, 0, -0.5], 10, 'stand', 'unimpressed', keys=[k(0.0, look=[0.0, 1.3, -0.05]), k(0.0, toon=HOLD17({'lid': 0.5, 'mouth': 'line', 'gy': 0.6}), toonDur=0.0),
            k(0.7, look='camera', lookDur=0.15), k(0.75, toon=HOLD17({'lid': 0.45, 'mouth': 'line'}), toonDur=0.12),
            k(1.3, toon=HOLD17({'lid': 1.0, 'mouth': 'line'}), toonDur=0.12, toonEase='inOut'), k(1.48, toon=HOLD17({'lid': 0.45, 'mouth': 'line'}), toonDur=0.14, toonEase='inOut'),   # a slow blink
            k(1.75, toon=HOLD17({'lid': 0.45, 'mouth': 'line'}, 0.3, 1.36, 0.15), toonDur=0.25, toonEase='inOut')])],   # he hands it back
        props=[P('jar17', 'picklesJar', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.1, 0.04], 'face': 'camera', 'faceFlat': True}, scale=1.2, opts={'lidGone': True})],
        cams=[FC(0.0, [0.45, 1.75, 1.0], [[-0.1, 2.4, -0.5], [-0.1, 1.15, -0.5], [0.15, 1.3, -0.05], [-0.4, 1.9, -0.5]], top=0.12, bottom=0.78)])

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
ASTROC = {'preset': 'worker', 'suit': '#F2F2EE', 'pants': '#F2F2EE', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
st.write("Le bocal", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'pompier1': {'preset': 'pompier', 'seed': 781, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'pompier2': {'preset': 'pompier', 'seed': 782, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'astro{j + 1}': {**ASTROC, 'seed': 783 + j} for j in range(6)},
    'savant1': {'preset': 'savant', 'seed': 790, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant2': {'preset': 'savant', 'seed': 791, 'hairColor': '#6B4A2E', 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'visiteur1': {'preset': 'boss', 'seed': 792, 'suit': '#5A6470', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'visiteur2': {'preset': 'madame', 'seed': 793, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'gardien': {'preset': 'cop', 'seed': 794, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'mamie': {'preset': 'mamie', 'seed': 795, 'suit': '#C77DA0', 'build': {'width': 0.92, 'headWidth': 1.25, 'height': 0.88}, 'toon': EX},
})
