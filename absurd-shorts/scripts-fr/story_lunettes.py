#!/usr/bin/env python3
"""Les lunettes (story 69, cycle 31; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man lost his glasses. He looked everywhere. Under the sofa. In the fridge. He filed a complaint. The police searched the whole district. Divers
drained the river. The army sent helicopters. Satellites scanned the planet. The other countries sent their dogs. The government promised a million
euros. The whole world searched for a year. Yesterday a child found them. On his head. The child got the million. The man is looking for his keys.
Running gag (dramatic irony): the glasses sit pushed up on his head in every shot, in plain sight of everyone and of us; they glint now and then.
Staging: close, squinting, he pats his pockets; he throws the cushions of his sofa over his shoulder; on his knees he peers under the sofa; his head
in the fridge in the cold mist; at the police desk he mimes glasses round his eyes for the officer, who looks straight at the glasses on his head;
policemen with binoculars and a dog search the street, one with his head in a bin (FOUILLE); divers in masks dig the mud of a drained river, a fish
flopping; at night a helicopter's searchlight sweeps over him and the glasses flash; a satellite scans the Earth with a red fan; dogs of every colour
sniff round him, one sits and stares up at his head, tilts it, and goes on sniffing; a minister at a podium, a reward poster pops up (MILLION); an
office searched from top to bottom while a wall calendar sheds twelve months; a boy tugs his sleeve and points up; his eyes roll up to his head, the
glasses flash, his eyes pop (TROUVÉES); the boy holds up a giant cheque; he pats every pocket, his key ring hanging from his own mouth.
Natural look; cycle 31: props_lunettes.js (bigGlasses with glints, helicopter with a searchlight, satellite with a scan fan, diveMask, drainedRiver,
rewardPoster), bigFridge mist, monthCalendar, bigCheque, keyRing."""
from story_kit import *
import math

st = Story('lunettes', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L08', 0),
         ('S09', 'L09', 0), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L11', 4), ('S13', 'L12', 0), ('S14', 'L13', 0), ('S15', 'L14', 0), ('S16', 'L15', 0),
         ('S17', 'L16', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
SQUINT = {'lid': 0.35, 'low': 0.3, 'brow': -0.35, 'mouth': 'pout'}       # without his glasses: he squints
GL = lambda pid, glint=(): P(pid, 'bigGlasses', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.47, 0.095]}, opts={'glint': list(glint)})   # pushed up on his head, in every shot
DOGC = [{'body': '#C99A62', 'collar': '#2F62B5'}, {'body': '#3B2E26', 'collar': '#E0413A'}, {'body': '#E8E2D6', 'collar': '#2F8F6B'}, {'body': '#8A6A4A', 'collar': '#F2C94E'}]

for g_ in [('S01', 1.0, 'mec', 'squint'), ('S05', 0.8, 'mec', 'mime'), ('S10', 1.2, 'chien1', 'stare'), ('S14', 1.2, 'gamin', 'point'), ('S15', 0.6, 'mec', 'found'),
           ('S17', 1.2, 'mec', 'keys')]:
    st.gag(*g_)
st.card('S06', 'FOUILLE', at=0.5)
st.card('S12', 'MILLION', at=0.3)
st.card('S15', 'TROUVÉES', at=0.3)


# 1: the hook. Close in his living room: squinting at nothing, he pats his shirt pocket, his trouser pockets, looks left and right; the glasses sit
#    on his head all along and glint once
D1 = st.dur('S01'); ME = [0.0, 0, 0.0]
POCK = lambda side, y: {'touch': {side: ['torso', (-0.1 if side == 'R' else 0.1), y, 0.12, 1, 0.02]}, 'hands': {side: 'open'}}
st.shot('S01', 'livingRoom', actors=[
        act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': SQUINT}, toonDur=0.0),
            k(0.2, toon={**POCK('R', 0.42), 'face': SQUINT}, toonDur=0.12, toonEase='out'), k(0.45, toon={**POCK('L', 0.42), 'face': SQUINT}, toonDur=0.12, toonEase='out'),   # the shirt pockets...
            k(0.7, look=[-1.5, 2.0, 1.0]), k(0.7, toon={**POCK('R', -0.05), 'face': SQUINT}, toonDur=0.12, toonEase='out'), k(0.95, look=[1.5, 2.0, 1.0]), k(0.95, toon={**POCK('L', -0.05), 'face': SQUINT}, toonDur=0.12, toonEase='out'),   # ...the trousers, a look each side...
            k(1.25, look='camera'), k(1.25, toon={'face': {**SQUINT, 'brow': 0.3, 'mouth': 'line'}}, toonDur=0.15)])],   # ...nothing
        props=[GL('gl1', glint=[1.15])],
        cams=[FC(0.0, [0.3, 2.15, 1.4], [[0.0, 2.85, 0.0], [0.0, 1.55, 0.0], [0.35, 2.2, 0.1], [-0.35, 2.2, 0.1]], top=0.14, bottom=0.74)])
st.cue('sfx:stepSoft', 'S01', 0.2, 0.1); st.cue('sfx:stepSoft', 'S01', 0.45, 0.1); st.cue('sfx:ding', 'S01', 1.15, 0.15)

# 2: he looked everywhere. Wide on the living room: bent over the sofa he throws its cushions over his shoulder one after another; they fly across the
#    room in arcs, a sock and a book after them
D2 = st.dur('S02'); ME2 = [0.2, 0, -2.2]; SOFA2 = [0.2, 0, -1.45]   # (build) facing us behind a sofa: his face, not his back
THROW = lambda j: [k(r(0.12 + 0.3 * j), toon={'reach': {'R': [0.25, 0.75, -1.6, 1, 0.04]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.7, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'open', 'brow': 0.7}}, toonDur=0.1, toonEase='in'),
                   k(r(0.26 + 0.3 * j), toon={'reach': {'R': [0.45, 2.75, -2.5, 1, 0.04]}, 'hands': {'R': 'open'}, 'bend': {'spine': [-0.1, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'open', 'brow': 0.7}}, toonDur=0.07, toonEase='out')]
FLY2 = [('cush1', 'slab', [0.25, 0.62, -1.55], {'w': 0.55, 'h': 0.16, 'd': 0.45, 'color': '#E07A5F'}, 0.26, [-0.6, 3.3, -2.8], [-1.9, 0.1, -3.3]),
        ('cush2', 'slab', [0.55, 0.62, -1.55], {'w': 0.55, 'h': 0.16, 'd': 0.45, 'color': '#3D9A8B'}, 0.56, [1.0, 3.4, -2.9], [2.3, 0.1, -3.3]),
        ('sock2', 'slab', [0.0, 0.62, -1.55], {'w': 0.25, 'h': 0.06, 'd': 0.1, 'color': '#F2F2EE'}, 0.86, [-0.2, 3.5, -2.8], [-0.9, 0.05, -3.4]),
        ('book2', 'slab', [0.4, 0.62, -1.55], {'w': 0.3, 'h': 0.06, 'd': 0.22, 'color': '#2F62B5'}, 1.16, [0.6, 3.5, -2.9], [1.4, 0.05, -3.4])]
K2 = [k(0.0, look=[0.3, 0.6, -1.5]), k(0.0, toon={'bend': {'spine': [0.6, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'open'}}, toonDur=0.0)]
for j in range(4): K2 += THROW(j)
st.shot('S02', 'livingRoom', setOpts={'sofa': False}, actors=[act('mec', ME2, 0, 'stand', 'neutral', keys=K2 + [k(1.3, look='camera')])],
        props=[GL('gl2'), P('sofa2', 'sofaProp', pos=SOFA2, ry=180), *[P(pid, kind, pos=p0, opts=o, keys=[k(r(t0 - 0.02), to=mid, dur=0.22, ease='out'), k(r(t0 + 0.2), to=end, dur=0.28, ease='in'),
                                                                 k(r(t0 - 0.02), rot=[2.5, 1.5, 0.8], dur=0.5, ease='linear')]) for pid, kind, p0, o, t0, mid, end in FLY2]],
        cams=[FC(0.0, [0.9, 1.6, 1.6], [[0.2, 2.9, -2.2], [0.2, 0.6, -1.45], [-0.6, 3.4, -2.8], [1.0, 3.4, -2.9]], top=0.1, bottom=0.78)])
for j in range(4): st.cue('whoosh', 'S02', r(0.26 + 0.3 * j), 0.2, 0.25, 500, 1500)

# 3: under the sofa. Low beside the sofa: on his knees, cheek to the floor, he peers under it; the glasses on his head scrape its edge
D3 = st.dur('S03'); ME3 = [0.0, 0, -1.25]; SOFA3 = [0.0, 0, -2.2]   # (build) from under the sofa: his face peering in (from the side it was his back)
st.shot('S03', 'livingRoom', actors=[
        act('mec', ME3, 180, 'kneelLook', 'neutral', keys=[k(0.0, look=[0.0, 0.15, -2.6]), k(0.0, toon={'bend': {'spine': [0.6, 0, 0, 1, None], 'neck': [0.35, 0, 0, 1, None]}, 'face': {**SQUINT, 'mouth': 'O'}}, toonDur=0.0),
            k(0.45, look=[-0.6, 0.15, -2.6]), k(0.75, look=[0.6, 0.15, -2.6]), k(0.6, toon={'bend': {'spine': [0.66, 0, 0, 1, None], 'neck': [0.4, 0, 0, 1, None]}, 'face': {**SQUINT, 'mouth': 'pout'}}, toonDur=0.2), k(r(D3 - 0.25), look='camera')])],
        props=[GL('gl3'), P('sofa3', 'sofaProp', pos=SOFA3, ry=0), P('coin3', 'coin', pos=[0.35, 0.02, -2.35], rot=[PI / 2, 0, 0]), P('sock3', 'slab', pos=[-0.3, 0.03, -2.4], opts={'w': 0.25, 'h': 0.05, 'd': 0.1, 'color': '#F2F2EE'}),
               P('dust3', 'dustPuff', pos=[0.1, 0.0, -2.2], scale=0.5, opts={'color': '#BDB4A6', 'period': 1.1})],
        cams=[FC(0.0, [0.25, 0.22, -2.75], [[0.0, 1.35, -1.3], [0.0, 0.25, -1.3], [0.4, 0.8, -1.5], [-0.4, 0.8, -1.5]], top=0.12, bottom=0.8, inside=(-1.5, 1.5, 0.12, 3.0, -3.3, 2.0))])
st.cue('sfx:scratch', 'S03', 0.35, 0.15)

# 4: in the fridge. In the kitchen: the fridge door open, his head and shoulders inside, cold mist rolling out round him; he comes out with frost on
#    his eyebrows, the glasses still on his head, frosted
D4 = st.dur('S04'); FR4 = [0.0, 0, -2.4]
st.shot('S04', 'kitchenDay', setOpts={'fridge': False}, actors=[
        act('mec', [0.15, 0, -1.55], 180, 'peerIn', 'neutral', keys=[k(0.0, look=[0.0, 1.6, -2.6]), k(0.0, toon={'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.0),
            k(0.6, to=[0.15, 0, -1.25], dur=0.18, ease='out', clip='stand', face='keep'), k(0.62, look='camera'), k(0.62, toon={'face': {**SQUINT, 'mouth': 'zigzag', 'tremble': 1.0, 'blush': 0.0}}, toonDur=0.1)])],   # he backs out, shivering
        props=[P('fr4', 'bigFridge', pos=FR4, opts={'open': 1.0, 'mode': 'full', 'mist': True, 'light': True}), GL('gl4', glint=[0.75]),
               P('mist4', 'dustPuff', pos=[0.15, 1.5, -1.6], scale=1.4, opts={'color': '#E8F4FF', 'period': 0.9})],
        cams=[FC(0.0, [0.05, 1.55, -2.65], [[0.15, 2.95, -1.4], [0.15, 1.85, -1.4], [0.4, 2.3, -1.45], [-0.1, 2.3, -1.45]], top=0.14, bottom=0.74, inside=(-0.45, 0.45, 0.4, 2.4, -2.75, 0.5))])   # (build) from inside the fridge out at his face
st.cue('sfx:click', 'S04', 0.05, 0.15); st.cue('sfx:sniff', 'S04', 0.7, 0.2)

# 5: he filed a complaint. At the police desk, over the officer's shoulder: he makes rings of his fingers round his eyes (glasses!); the officer looks
#    up at him, straight at the glasses on his head, and writes
D5 = st.dur('S05')
RINGS = {'touch': {'R': ['face', -0.18, 0.62, 0.08, 1, 0.02], 'L': ['face', 0.18, 0.62, 0.08, 1, 0.02]}, 'hands': {'R': 'pinch', 'L': 'pinch'}}
st.shot('S05', 'policeStation', actors=[
        act('mec', [-2.7, 0, -1.05], 180, 'stand', 'neutral', keys=[k(0.0, look=[-2.7, 1.9, -2.6]), k(0.0, toon={'face': SQUINT}, toonDur=0.0),
            k(0.15, toon={**RINGS, 'face': {**SQUINT, 'brow': 0.4}}, toonDur=0.15, toonEase='out'), *[k(r(0.4 + 0.18 * j), toon={**RINGS, 'face': {**SQUINT, 'brow': r(0.4 + 0.2 * (j % 2))}}, toonDur=0.08) for j in range(4)]]),   # glasses! glasses!
        act('flic', [-2.7, 0, -2.75], 0, 'sitWrite', 'unimpressed', keys=[k(0.0, look=[-2.7, 1.1, -2.2]), k(0.0, toon={'face': {'lid': 0.55, 'mouth': 'line'}}, toonDur=0.0),
            k(0.45, look=[-2.7, 2.55, -1.05]), k(0.5, toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.1), k(1.0, look=[-2.7, 1.1, -2.2])])],   # he looks right at them, and writes
        props=[GL('gl5', glint=[0.55])],
        cams=[FC(0.0, [-0.9, 1.95, -3.35], [[-2.7, 2.95, -1.05], [-2.7, 1.65, -1.05]], top=0.12, bottom=0.78, inside=(-6.8, 6.8, 0.3, 3.4, -3.45, 13.0))])
st.cue('sfx:paper', 'S05', 1.05, 0.2)

# 6: the police searched the whole district. A street: a policeman with binoculars scans the rooftops, another has his head in a bin, a dog noses
#    along the pavement; he walks between them, the glasses on his head (FOUILLE)
D6 = st.dur('S06')
st.shot('S06', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, -0.6], 0, 'walk', 'neutral', keys=[k(0.0, to=[5.0, 0, 1.6], dur=D6, clip='walk', ease='linear', face='keep'), k(0.0, look=[4.0, 1.0, 0.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(1.4, look='camera')]),
        act('flic1', [6.3, 0, 0.0], -150, 'binocs', 'neutral', keys=[k(0.0, look=[8.0, 6.0, -6.0]), k(0.9, look=[3.0, 6.0, -6.0])]),
        act('flic2', [3.9, 0, -1.2], 180, 'peerIn', 'neutral', keys=[k(0.0, look=[3.9, 0.6, -1.75])]),
        act('chien0', [5.6, 0, 1.4], 180, 'walk', 'neutral', scale=0.9, keys=[k(0.0, to=[5.9, 0, -1.6], dur=D6, clip='walk', ease='linear', face='keep'), k(0.0, look=[5.9, 0.0, -1.0])])],
        props=[GL('gl6'), P('bin6', 'trashCan', pos=[3.9, 0, -1.75]), P('bino6', 'binoculars', on={'actor': 'flic1', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]})],
        cams=[FC(0.0, [4.4, 1.5, 6.4], [[5.0, 2.9, 1.6], [5.0, 1.2, 1.6], [6.3, 2.6, 0.0], [3.9, 1.1, -1.75], [3.9, 2.0, -1.2]], top=0.12, bottom=0.76)])
st.cue('sfx:sniff', 'S06', 0.4, 0.2); st.cue('sfx:sniff', 'S06', 1.2, 0.2)

# 7: divers drained the river. In the mud of the emptied river between the stone quays: two divers in masks dig, one holds up an old boot; a fish
#    flops in a puddle; on the quay above, he looks down at them, the glasses on his head
D7 = st.dur('S07')
st.shot('S07', 'grassland', actors=[
        act('plong1', [-1.0, 0, 1.0], 20, 'pointDown', 'neutral', keys=[k(0.0, look=[-1.0, 0.0, 1.8]), k(0.4, look=[-1.2, 0.0, 0.6])]),
        act('plong2', [1.0, 0, 0.4], -30, 'holdUp', 'neutral', keys=[k(0.0, look='camera')]),
        act('mec', [-3.9, 2.55, -0.2], 90, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.0, 0.5]), k(0.0, toon={'bend': {'neck': [0.35, 0, 0, 1, None], 'spine': [0.25, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.0), k(0.9, look=[1.0, 0.5, 0.4]), k(1.3, toon={'bend': {'neck': [0.35, 0, 0, 1, None], 'spine': [0.25, 0, 0, 1, None]}, 'face': {**SQUINT, 'lid': 1.0}}, toonDur=0.04), k(1.36, toon={'bend': {'neck': [0.35, 0, 0, 1, None], 'spine': [0.25, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.06)]),
        act('poisson7', [0.2, 0.0, 1.9], 0, 'stand', 'neutral', scale=0.35, keys=[*[k(r(0.1 + 0.3 * j), to=[r(0.2 + 0.05 * (j % 2)), 0.25 if j % 2 == 0 else 0.0, 1.9], dur=0.15, ease='out' if j % 2 == 0 else 'in') for j in range(6)]])],
        props=[P('river7', 'drainedRiver', pos=[0.0, 0, 0.0], opts={'w': 8, 'len': 40, 'qh': 2.45, 'bridgeZ': -16}), GL('gl7'),
               P('mask71', 'diveMask', on={'actor': 'plong1', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.28, 'y': 0.3}),
               P('mask72', 'diveMask', on={'actor': 'plong2', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.28, 'y': 0.3}),
               P('boot7', 'slab', on={'actor': 'plong2', 'hand': 'R', 'offset': [0.0, 0.08, 0.04]}, opts={'w': 0.12, 'h': 0.26, 'd': 0.28, 'color': '#3B2A20'})],
        cams=[FC(0.0, [1.4, 1.1, 5.2], [[-1.0, 2.4, 1.0], [1.0, 2.6, 0.4], [-3.9, 5.25, -0.2], [0.2, 0.0, 1.9]], top=0.12, bottom=0.78)])
st.cue('sfx:splash', 'S07', 0.1, 0.15); st.cue('sfx:splash', 'S07', 0.7, 0.12); st.cue('sfx:splash', 'S07', 1.3, 0.12)

# 8: the army sent helicopters. At night in the street, from low: a helicopter hangs over the roofs, its searchlight sweeps the street, crosses him,
#    and the glasses on his head flash in the beam; the beam sweeps on
D8 = st.dur('S08'); PASS8 = 1.0
st.shot('S08', 'parisStreet', setOpts={'night': True, 'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, look={'sun': 0.15, 'fill': 0.35, 'exposure': 1.1}, actors=[
        act('mec', [5.0, 0, 0.0], 20, 'stand', 'neutral', keys=[k(0.0, look=[3.0, 12.0, -10.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(r(PASS8 + 0.15), look='camera'), k(r(PASS8 + 0.15), toon={'face': {**SQUINT, 'lid': 0.6}}, toonDur=0.08)])],
        props=[P('heli8', 'helicopter', pos=[2.5, 13.0, -9.0], ry=150, rot=[0.12, 0, 0], scale=0.9, opts={'spin': 5, 'beam': True, 'beamLen': 18, 'beamR': 2.4, 'tilt': 30, 'sweep': [[0.0, -40], [PASS8, -8], [D8, 30]]},
                 keys=[k(0.0, to=[3.5, 13.5, -8.0], dur=D8, ease='linear')]), GL('gl8', glint=[r(PASS8 - 0.05)]),
               P('spot8', 'glowLight', pos=[5.0, 3.0, 0.4], opts={'color': '#FFF4C8', 'k': 6.0, 'dist': 4.0}, keys=[k(0.0, visible=False), k(r(PASS8 - 0.15), visible=True), k(r(PASS8 + 0.2), visible=False)])],
        cams=[FC(0.0, [6.4, 0.9, 3.0], [[5.0, 2.9, 0.0], [5.0, 0.9, 0.0], [2.5, 16.0, -9.0], [6.0, 12.0, -8.0]], top=0.08, bottom=0.8)])
st.cue('sfx:engine', 'S08', 0.05, 0.4); st.cue('sfx:ding', 'S08', r(PASS8 - 0.05), 0.25)

# 9: satellites scanned the planet. Space: a satellite over the Earth sweeps a red scanning fan across it
D9 = st.dur('S09')
st.shot('S09', 'spaceDark', actors=[],
        props=[P('earth9', 'earthGlobe', pos=[0.0, -9.0, -12.0], scale=9.0, opts={'spin': 0.06}),
               P('sat9', 'satellite', pos=[-0.6, 1.6, -3.5], rot=[0.15, 0.4, 0.0], scale=0.8, opts={'scan': [[0.1, 9.0]], 'scanLen': 7.5, 'sweepDeg': 30}, keys=[k(0.0, to=[0.6, 1.8, -3.8], dur=D9, ease='linear')])],
        cams=[FC(0.0, [0.4, 2.2, 3.6], [[-2.5, 2.4, -3.5], [2.5, 2.4, -3.5], [0.0, -3.5, -8.0], [0.0, 0.5, -4.0]], top=0.14, bottom=0.78)])
st.cue('sfx:static', 'S09', 0.1, 0.2); st.cue('sfx:ding', 'S09', 1.2, 0.15)

# 10: the other countries sent their dogs. In the street: dogs of every colour, each with a collar of its own colour, sniff round his shoes and
#    legs; one sits, stares up at his head, tilts its own, and goes back to sniffing
D10 = st.dur('S10'); STARE10 = 0.55
DOGP = [[5.6, 0, 0.9], [4.3, 0, 0.7], [5.9, 0, -0.5], [4.4, 0, -0.6]]
st.shot('S10', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.1], 20, 'stand', 'unimpressed', keys=[k(0.0, look=[5.3, 0.3, 0.9]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(1.1, look='camera'),
            k(1.4, toon={'face': {**SQUINT, 'lid': 1.0}}, toonDur=0.04), k(1.46, toon={'face': SQUINT}, toonDur=0.06)]),
        act('chien1', DOGP[0], -140, 'stand', 'neutral', scale=0.9, keys=[k(0.0, look=[5.0, 0.2, 0.1]), k(STARE10, look=[5.0, 2.7, 0.1]), k(r(STARE10 + 0.05), toon={'bend': {'neck': [0.0, 0.0, 0.35, 1, None]}, 'face': {'eye': 0.3}}, toonDur=0.15),
            k(r(STARE10 + 0.8), look=[5.2, 0.1, 0.4]), k(r(STARE10 + 0.8), toon={'face': {}}, toonDur=0.15)]),   # it stares up at his head, tilts its own... and sniffs on
        *[act(f'chien{j + 2}', DOGP[j + 1], [120, -40, 30][j], 'walk', 'neutral', scale=0.85, keys=[k(0.0, to=[r(DOGP[j + 1][0] + [0.4, -0.3, 0.4][j]), 0, r(DOGP[j + 1][2] + [0.2, 0.4, 0.3][j])], dur=D10, clip='walk', ease='inOut', face='keep'), k(0.0, look=[5.0, 0.15, 0.1])]) for j in range(3)]],
        props=[GL('gl10', glint=[r(STARE10 + 0.1)])],
        cams=[FC(0.0, [5.9, 1.2, 3.6], [[5.0, 2.85, 0.1], [5.0, 0.0, 0.1], [4.0, 0.0, 1.0], [6.2, 0.0, 1.0], [6.3, 0.0, -0.8], [4.0, 0.0, -0.8]], top=0.12, bottom=0.78)])
st.cue('sfx:sniff', 'S10', 0.2, 0.2); st.cue('sfx:sniff', 'S10', 0.9, 0.2); st.cue('sfx:squeak', 'S10', r(STARE10 + 0.05), 0.15)

# 11-12: the government promised a million euros. At the podium the minister announces it; a reward poster pops up at his side: RÉCOMPENSE, the
#    glasses drawn on it, « UN MILLION D'EUROS »; he points at it (MILLION)
D11 = st.dur('S11'); D12 = st.dur('S12')
MIN = lambda keys: act('ministre', [0.0, 0, -2.45], 0, 'stand', 'neutral', keys=keys)
st.shot('S11', 'pressRoom', setOpts={'backdrop': 'GOUVERNEMENT', 'fontScale': 0.55}, actors=[MIN([k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [0.25, 1.35, -1.85, 1, 0.04], 'L': [-0.25, 1.35, -1.85, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, toon={'reach': {'R': [0.32, 2.4, -1.95, 1, 0.05], 'L': [-0.25, 1.35, -1.85, 1, 0.04]}, 'hands': {'R': 'point', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'open', 'brow': 0.6}}, toonDur=0.2, toonEase='out')])],
        props=[*[P(f'fl11{j}', 'glowLight', pos=[r(-1.2 + 1.2 * j), 1.8, 1.2], opts={'color': '#FFFFFF', 'k': 6.0, 'dist': 6.0}, keys=[k(0.0, visible=False), k(r(0.3 + 0.35 * j), visible=True), k(r(0.36 + 0.35 * j), visible=False)]) for j in range(3)]],
        cams=[FC(0.0, [0.7, 1.7, 1.6], [[0.0, 2.6, -2.45], [0.32, 2.5, -1.95], [0.0, 0.9, -2.0], [-0.6, 1.3, -2.0]], top=0.14, bottom=0.78)])
st.shot('S12', 'pressRoom', setOpts={'backdrop': 'GOUVERNEMENT', 'fontScale': 0.55}, actors=[MIN([k(0.0, look=[1.1, 1.9, -2.2]), k(0.0, toon={'reach': {'R': [0.8, 1.9, -2.2, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.0),
            k(0.6, look='camera')])],
        props=[P('poster12', 'rewardPoster', pos=[1.15, 0, -2.3], ry=-15, opts={'at': 0.05, 'w': 1.0, 'h': 1.35, 'stand': 0.9})],
        cams=[FC(0.0, [0.5, 1.65, 1.5], [[0.0, 2.6, -2.45], [1.15, 2.35, -2.3], [1.15, 0.9, -2.3], [0.0, 1.0, -2.0]], top=0.2, bottom=0.78)])
st.cue('sfx:click', 'S11', 0.3, 0.2); st.cue('sfx:click', 'S11', 0.65, 0.2); st.cue('sfx:boing', 'S12', 0.05, 0.25); st.cue('sfx:cash', 'S12', 0.25, 0.3)

# 13: the whole world searched for a year. An office turned upside down: one searcher under a desk, one with a magnifying glass at the floor, one in a
#    drawer; on the wall a calendar sheds its twelve months; in the middle he stands, squinting, the glasses on his head
D13 = st.dur('S13')
st.shot('S13', 'office', setOpts={'picture': False, 'carpet': False, 'printer': False}, actors=[
        act('mec', [0.0, 0, -1.2], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(1.0, look=[-1.5, 0.5, -1.0]), k(1.6, look='camera'),
            k(1.9, toon={'face': {**SQUINT, 'lid': 1.0}}, toonDur=0.04), k(1.96, toon={'face': SQUINT}, toonDur=0.06)]),
        act('cherch1', [-1.4, 0, -0.6], 60, 'crouchHide', 'neutral', keys=[k(0.0, look=[-1.0, 0.0, -0.2])]),
        act('cherch2', [1.4, 0, -0.5], -60, 'peerIn', 'neutral', keys=[k(0.0, look=[1.0, 0.0, -0.1])]),
        act('cherch3', [0.9, 0, -2.4], 160, 'peerIn', 'neutral', keys=[k(0.0, look=[0.8, 0.8, -3.0])])],
        props=[GL('gl13'), P('cal13', 'monthCalendar', pos=[-1.0, 1.4, -3.55], opts={'months': 12, 'flipAt': 0.15, 'dur': 0.16}), P('mag13', 'magnifier', on={'actor': 'cherch2', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=1.3)],
        cams=[FC(0.0, [0.6, 1.8, 2.8], [[0.0, 2.85, -1.2], [0.0, 0.0, -1.2], [-1.4, 1.0, -0.6], [1.4, 1.5, -0.5], [-1.0, 2.6, -3.55], [0.9, 2.2, -2.4]], top=0.12, bottom=0.78)])
st.cue('sfx:paper', 'S13', 0.2, 0.2); st.cue('sfx:paper', 'S13', 0.9, 0.2); st.cue('sfx:paper', 'S13', 1.6, 0.2)

# 14: yesterday a child found them. In the street a boy tugs at his sleeve and points up at his head, mouth open; he looks down at the boy
D14 = st.dur('S14'); TUG14 = 0.3
st.shot('S14', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.0], 15, 'stand', 'unimpressed', keys=[k(0.0, look=[3.0, 2.0, 2.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(r(TUG14 + 0.1), look=[4.35, 1.0, 0.45]), k(r(TUG14 + 0.12), toon={'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.12), k(1.3, toon={'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': {**SQUINT, 'lid': 1.0}}, toonDur=0.04), k(1.36, toon={'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.06), k(1.7, look='camera')]),
        act('gamin', [4.35, 0, 0.45], 70, 'stand', 'neutral', keys=[k(0.0, look=[5.0, 2.6, 0.0]), k(0.0, toon={'touch': {'R': ['@mec.handL', 0.0, 0.0, 0.0, 1, 0.0]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.0),
            *[k(r(TUG14 * (j + 1) / 2), toon={'touch': {'R': ['@mec.handL', 0.0, r(-0.03 * (j % 2)), 0.0, 1, 0.0]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.06) for j in range(2)],
            k(r(TUG14 + 0.35), toon={'reach': {'R': [4.85, 2.75, 0.2, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.15, toonEase='out'), k(1.5, toon={'reach': {'R': [4.85, 2.8, 0.2, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 1.0, 'mouth': 'open'}}, toonDur=0.04), k(1.56, toon={'reach': {'R': [4.85, 2.8, 0.2, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.06)])],   # ...then points up at his head
        props=[GL('gl14', glint=[r(TUG14 + 0.6)])],
        cams=[FC(0.0, [5.6, 1.4, 3.2], [[5.0, 2.95, 0.0], [5.0, 0.6, 0.0], [4.35, 0.6, 0.45], [4.85, 2.85, 0.2]], top=0.12, bottom=0.78)])
st.cue('sfx:stepSoft', 'S14', 0.1, 0.15); st.cue('sfx:gasp', 'S14', r(TUG14 + 0.35), 0.2)

# 15: on his head. Close: his eyes roll up to the top of his head; the glasses flash; his eyes pop (TROUVÉES)
D15 = st.dur('S15'); UP15 = 0.15; POP15 = 0.55
st.shot('S15', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.0], 15, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': SQUINT}, toonDur=0.0),
            k(UP15, toon={'face': {'lid': 0.0, 'low': 0.0, 'gy': -1.0, 'eye': 0.2, 'brow': 0.7, 'mouth': 'line', 'noBlink': 1}}, toonDur=0.15, toonEase='inOut'),   # the eyes go up...
            k(POP15, toon={'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.0, 'gy': -0.6, 'pop': 0.5, 'popLen': 0.14, 'brow': 1.0, 'mouth': 'O', 'noBlink': 1}}, toonDur=0.05, toonEase='out'),   # ...POP
            k(r(POP15 + 0.3), toon={'face': {'lid': 0.0, 'gy': -0.6, 'eye': 0.4, 'brow': 0.8, 'mouth': 'O'}}, toonDur=0.15)])],
        props=[GL('gl15', glint=[r(UP15 + 0.2)])],
        cams=[FC(0.0, [5.5, 2.35, 1.5], [[5.0, 3.0, 0.0], [5.0, 1.75, 0.0], [5.35, 2.3, 0.1], [4.65, 2.3, 0.1]], top=0.2, bottom=0.74)])
st.cue('sfx:ding', 'S15', r(UP15 + 0.2), 0.35); st.cue('pop', 'S15', POP15, 0.25)

# 16: the child got the million. A town-hall stage: the boy holds a giant cheque over his head and jumps; the minister claps beside him
D16 = st.dur('S16')
st.shot('S16', 'mairie', actors=[
        act('gamin', [0.0, 0, -1.2], 0, 'holdUp', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'bigsmile', 'brow': 0.8}}, toonDur=0.0),
            *[k(r(0.15 + 0.4 * j), to=[0.0, 0.25 if j % 2 == 0 else 0.0, -1.2], dur=0.18, ease='out' if j % 2 == 0 else 'in') for j in range(4)]]),
        act('ministre', [1.1, 0, -1.5], -40, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.6, -1.2]), *[k(r(0.1 + 0.15 * j), toon={'reach': {'R': [r(0.85 + 0.05 * (j % 2)), 1.6, -1.15, 1, 0.04], 'L': [r(0.72 - 0.05 * (j % 2)), 1.6, -1.2, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'smirk'}}, toonDur=0.06) for j in range(8)]])],
        props=[P('cheque16', 'bigCheque', on={'actor': 'gamin', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, scale=1.2), P('conf16', 'confetti', pos=[0.3, 3.2, -1.2], opts={'at': 0.05})],
        cams=[FC(0.0, [0.4, 1.5, 2.2], [[0.0, 2.6, -1.2], [0.0, 0.0, -1.2], [1.1, 2.5, -1.5], [-0.8, 2.4, -1.2]], top=0.14, bottom=0.78)])
st.cue('sfx:fanfare', 'S16', 0.05, 0.3); st.cue('sfx:cash', 'S16', 0.4, 0.2)

# 17: the man is looking for his keys. His living room by the door: he pats every pocket, looks round, squinting; his key ring hangs from his own
#    mouth, jingling; a look at us
D17 = st.dur('S17')
st.shot('S17', 'livingRoom', actors=[
        act('mec', [-0.4, 0, -0.6], 15, 'patPockets', 'unimpressed', keys=[k(0.0, look=[-1.5, 1.0, 0.5]), k(0.0, toon={'face': {**SQUINT, 'mouth': 'clench'}}, toonDur=0.0), k(0.7, look=[1.5, 1.0, 0.5]), k(1.3, look='camera'),
            k(1.6, toon={'face': {**SQUINT, 'mouth': 'clench', 'lid': 1.0}}, toonDur=0.04), k(1.66, toon={'face': {**SQUINT, 'mouth': 'clench'}}, toonDur=0.06)])],
        props=[GL('gl17', glint=[1.85]), P('keys17', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.1, 0.12]}, scale=1.6)],
        cams=[FC(0.0, [-1.5, 1.45, 1.2], [[-0.4, 2.95, -0.6], [-0.4, 1.2, -0.6], [0.0, 1.9, -0.4], [-0.8, 1.9, -0.4]], top=0.14, bottom=0.76)])   # (build) low from his left (S01's set-up was repeated)
st.cue('sfx:rattleShort', 'S17', 0.3, 0.15); st.cue('sfx:rattleShort', 'S17', 0.9, 0.15); st.cue('sfx:ding', 'S17', 1.85, 0.12)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.4}}
st.write("Les lunettes", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': MEC,
    'flic': {'preset': 'cop', 'seed': 691, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic1': {'preset': 'cop', 'seed': 692, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic2': {'preset': 'cop2', 'seed': 693, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chien0': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 701, 'colors': {'body': '#2B2B2E', 'collar': '#2F62B5'}}},
    **{f'chien{j + 1}': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 702 + j, 'colors': DOGC[j]}} for j in range(4)},
    'plong1': {'preset': 'worker', 'seed': 694, 'hat': 'none', 'suit': '#1C1C20', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'plong2': {'preset': 'worker', 'seed': 695, 'hat': 'none', 'suit': '#1C1C20', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'poisson7': {'type': 'creature', 'name': 'fish', 'opts': {'seed': 706, 'color': '#F28C28'}},
    'ministre': {'preset': 'politique', 'seed': 696, 'suit': '#2B3A55', 'lapel': '#2B3A55', 'tie': '#9A2A2A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'cherch1': {'preset': 'femme', 'seed': 697, 'suit': '#D9734E', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'cherch2': {'preset': 'savant', 'seed': 698, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'cherch3': {'preset': 'officiel', 'seed': 699, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'gamin': {'preset': 'gamin', 'seed': 700, 'suit': '#E0413A', 'build': {'headScale': 1.25}, 'toon': EX},
})
