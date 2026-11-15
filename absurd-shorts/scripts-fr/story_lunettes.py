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
GL = lambda pid, glint=(): P(pid, 'bigGlasses', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.6, 0.045]}, rot=[-0.55, 0.0, 0.0], opts={'glint': list(glint)})   # pushed up on top of his head, tilted back, in every shot; (stills 1) at 0.47 they sat on his brow and read as worn
DOGC = [{'body': '#C99A62', 'collar': '#2F62B5'}, {'body': '#3B2E26', 'collar': '#E0413A'}, {'body': '#E8E2D6', 'collar': '#2F8F6B'}, {'body': '#8A6A4A', 'collar': '#F2C94E'}]

for g_ in [('S01', 1.0, 'mec', 'squint'), ('S05', 0.8, 'mec', 'mime'), ('S10', 1.2, 'chien1', 'stare'), ('S14', 1.2, 'gamin', 'point'), ('S15', 0.6, 'mec', 'found'),
           ('S17', 1.2, 'mec', 'keys')]:
    st.gag(*g_)
st.card('S06', 'FOUILLE', at=0.5)
st.card('S12', 'MILLION', at=0.3)
st.card('S15', 'TROUVÉES', at=0.55)   # (review 1) on the pop, not before the glint


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

# 3: under the sofa. The camera under the sofa at floor level, looking out (review 1: from the side he read as a headless navy arch): the dark
#    underside frames the top, a coin, a sock and dust in front; he kneels bent right down, cheek to the floor, squinting into the dark, the glasses
#    on his head against the bright room; he looks left, right, blinks, then at us
D3 = st.dur('S03'); ME3 = [0.0, 0, -0.55]; SOFA3 = [0.0, 0, -2.2]   # (stills 7) a step back: his face filled the whole frame
LOW3 = lambda f, sq=(1.08, 0.62, 1.08): {'bend': {'spine': [1.25, 0, 0, 1, None], 'neck': [-0.55, 0, 0, 1, None]}, 'face': f, 'sq': list(sq)}   # (stills 6) squashed flat to the floor: bent, his head stayed at 0.73 m, over the gap
st.shot('S03', 'livingRoom', actors=[
        act('mec', ME3, 180, 'peerIn', 'neutral', keys=[k(0.0, look=[0.0, 0.2, -2.6]), k(0.0, toon=LOW3({**SQUINT, 'mouth': 'O'}), toonDur=0.0),
            k(0.3, look=[-0.6, 0.2, -2.6]), k(0.62, look=[0.6, 0.2, -2.6]), k(0.55, toon=LOW3({**SQUINT, 'mouth': 'pout'}, (1.1, 0.6, 1.1)), toonDur=0.2),
            k(0.85, toon=LOW3({**SQUINT, 'lid': 1.0, 'mouth': 'pout'}), toonDur=0.05), k(0.95, toon=LOW3({**SQUINT, 'mouth': 'pout'}), toonDur=0.07), k(r(D3 - 0.38), look='camera')])],
        props=[GL('gl3'), P('sofa3', 'sofaProp', pos=SOFA3, ry=0, opts={'legs': 0.46}), P('coin3', 'coin', pos=[0.16, 0.02, -2.05], rot=[PI / 2, 0, 0], scale=1.6),
               P('sock3', 'slab', pos=[-0.22, 0.03, -1.98], ry=25, opts={'w': 0.25, 'h': 0.05, 'd': 0.1, 'color': '#F2F2EE'}),
               P('dust3', 'dustPuff', pos=[0.3, 0.0, -1.9], scale=0.15, opts={'color': '#BDB4A6', 'period': 1.1})],
        cams=[FC(0.0, [0.06, 0.12, -1.93], [[0.0, 0.95, -1.2], [0.0, 0.0, -1.6], [-0.32, 0.55, -1.2], [0.32, 0.55, -1.2]], top=0.3, bottom=0.8, inside=(-0.8, 0.8, 0.05, 0.4, -2.6, -1.92), lenses=range(26, 86))])   # (stills 6) just behind the front edge: from deeper under, the rail hid his head
st.cue('sfx:scratch', 'S03', 0.35, 0.15)

# 4: in the fridge. The camera inside the fridge behind the food, looking out (review 1: from outside his head stayed in the fridge): his face
#    pushes in between the shelves, squinting, the cold mist round the glasses on his head; the cold jolts him out: he shoots back stretched,
#    hangs, drops squashed with his hair on end, and shivers outside, frosted, looking at us
D4 = st.dur('S04'); FR4 = [0.0, 0, -2.4]; IN4 = [0.1, 0, -1.4]; OUT4 = [0.1, 0, -1.08]; JOLT4 = 0.62
st.shot('S04', 'kitchenDay', setOpts={'fridge': False}, actors=[
        act('mec', IN4, 180, 'peerIn', 'neutral', keys=[k(0.0, look=[0.1, 1.0, -2.8]), k(0.0, toon={'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.0), k(0.28, look=[-0.3, 1.0, -2.8]), k(0.46, look=[0.35, 1.0, -2.8]),
            k(JOLT4, to=[0.1, 0.32, -1.25], dur=0.1, ease='out', face='keep'), k(r(JOLT4 + 0.2), to=OUT4, dur=0.08, ease='in', face='keep'),   # jolted out: up, a hang, down
            k(JOLT4, toon={'sq': [0.82, 1.3, 0.82], 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05, toonEase='out'),
            k(r(JOLT4 + 0.28), toon={'sq': [1.22, 0.8, 1.22], 'hairUp': 1.0, 'face': {**SQUINT, 'mouth': 'zigzag', 'tremble': 1.0}}, toonDur=0.05, toonEase='in'),
            k(r(JOLT4 + 0.4), toon={'hairUp': 1.0, 'face': {**SQUINT, 'mouth': 'zigzag', 'tremble': 1.0, 'blush': 0.0}}, toonDur=0.1), k(r(JOLT4 + 0.4), look='camera')])],
        props=[P('fr4', 'bigFridge', pos=FR4, opts={'open': 1.0, 'mode': 'full', 'mist': True, 'light': True}), GL('gl4', glint=[0.4])],
        cams=[FC(0.0, [0.28, 1.05, -2.76], [[0.1, 1.35, -2.05], [0.1, 0.72, -2.05], [-0.18, 1.0, -2.05], [0.38, 1.0, -2.05]], top=0.2, bottom=0.8, inside=(-0.45, 0.45, 0.86, 1.16, -2.78, -2.3), lenses=range(26, 86))])
st.cue('sfx:click', 'S04', 0.05, 0.15); st.cue('sfx:ding', 'S04', 0.4, 0.15); st.cue('whoosh', 'S04', JOLT4, 0.2, 0.25, 600, 1500); st.cue('sfx:sniff', 'S04', r(JOLT4 + 0.45), 0.2)

# 5: he filed a complaint. At the police desk, over the officer's shoulder (review 1: no officer, a white wall, one hand over one eye): a partition
#    behind him with POLICE and a flag; with both hands he rings his eyes (glasses!), twice; the officer's head tilts up to the glasses on his
#    head, holds there, and goes back down to write
D5 = st.dur('S05'); ME5 = [-2.7, 0, -1.05]
RINGS = lambda b: {'touch': {'R': ['face', -0.18, 0.62, 0.1, 1, 0.02], 'L': ['face', 0.18, 0.62, 0.1, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {**SQUINT, 'brow': b}}
st.shot('S05', 'policeStation', actors=[
        act('mec', ME5, 180, 'stand', 'neutral', keys=[k(0.0, look=[-2.7, 1.5, -2.75]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(0.12, toon=RINGS(0.4), toonDur=0.12, toonEase='out'),
            *[k(r(0.34 + 0.2 * j), toon={**RINGS(r(0.4 + 0.25 * (j % 2))), 'sq': [1.0, 1.03, 1.0] if j % 2 else [1.0, 0.98, 1.0]}, toonDur=0.08) for j in range(4)],
            k(1.05, toon={'face': {**SQUINT, 'brow': 0.3, 'mouth': 'line'}}, toonDur=0.12)]),   # glasses! glasses!
        act('flic', [-2.7, 0, -2.75], 0, 'sitWrite', 'unimpressed', keys=[k(0.0, look=[-2.7, 1.1, -2.2]), k(0.0, toon={'face': {'lid': 0.55, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, look=[-2.7, 2.7, -1.05], lookDur=0.2), k(0.45, toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.1), k(0.95, look=[-2.7, 1.1, -2.2], lookDur=0.15)])],   # up to the glasses, a hold, back to writing
        props=[GL('gl5', glint=[0.5]), P('mur5', 'slab', pos=[-2.7, 1.6, 0.5], opts={'w': 4.2, 'h': 3.2, 'd': 0.12, 'color': '#DCE3E6'}),
               P('bande5', 'slab', pos=[-2.7, 0.55, 0.43], opts={'w': 4.2, 'h': 1.1, 'd': 0.02, 'color': '#2B3A55'}),
               P('pol5', 'signBoard', pos=[-2.2, 2.7, 0.42], ry=180, opts={'text': 'POLICE', 'bg': '#1B2A4A', 'fg': '#FFFFFF', 'w': 1.5, 'h': 0.42, 'posts': False, 'height': 0}),
               P('drap5', 'flag', pos=[-3.75, 0, 0.25], scale=1.5, opts={'colors': ['#2A4B9B', '#F4F1E8', '#C8202A']})],
        cams=[FC(0.0, [-3.25, 1.85, -3.35], [[-2.7, 2.95, -1.05], [-2.7, 1.4, -1.05], [-3.25, 2.2, -1.05], [-2.15, 2.2, -1.05]], top=0.12, bottom=0.78, inside=(-6.8, 6.8, 0.3, 3.4, -3.45, 13.0))])
st.cue('sfx:paper', 'S05', 1.05, 0.2)

# 6: the police searched the whole district. A street: a policeman with binoculars scans the rooftops, another has his head in a bin, a dog noses
#    along the pavement; he walks between them, the glasses on his head (FOUILLE)
D6 = st.dur('S06')
st.shot('S06', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, -0.6], 0, 'walk', 'neutral', keys=[k(0.0, to=[5.0, 0, 1.6], dur=D6, clip='walk', ease='linear', face='keep'), k(0.0, look=[4.0, 1.0, 0.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(1.4, look='camera')]),
        act('flic1', [6.3, 0, 0.0], 25, 'binocs', 'neutral', keys=[k(0.0, look=[8.5, 6.0, 7.0]), k(0.9, look=[4.0, 6.0, 7.0])]),   # (review 1) he faced away: the binoculars hid behind his head
        act('flic2', [3.9, 0, -1.28], 180, 'peerIn', 'neutral', keys=[k(0.0, look=[3.9, 0.3, -1.8]), k(0.0, toon={'bend': {'spine': [0.85, 0, 0, 1, None]}}, toonDur=0.0)]),   # (review 1) his head right inside the bin
        act('chien0', [5.6, 0, 1.4], 180, 'walk', 'neutral', scale=0.9, keys=[k(0.0, to=[5.9, 0, -1.6], dur=D6, clip='walk', ease='linear', face='keep'), k(0.0, look=[5.9, 0.0, -1.0])])],
        props=[GL('gl6'), P('bin6', 'trashCan', pos=[3.9, 0, -1.78], scale=1.35, opts={'open': True}), P('bino6', 'binoculars', on={'actor': 'flic1', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]})],
        cams=[FC(0.0, [4.4, 1.5, 6.4], [[5.0, 2.9, 1.6], [5.0, 1.2, 1.6], [6.3, 2.6, 0.0], [3.9, 1.1, -1.75], [3.9, 2.0, -1.2]], top=0.12, bottom=0.76)])
st.cue('sfx:sniff', 'S06', 0.4, 0.2); st.cue('sfx:sniff', 'S06', 1.2, 0.2)

# 7: divers drained the river. In the mud of the emptied river between the stone quays: two divers in masks dig, one holds up an old boot; a fish
#    flops in a puddle; on the quay above, he looks down at them, the glasses on his head
D7 = st.dur('S07')
st.shot('S07', 'grassland', actors=[
        act('plong1', [-1.0, 0, 1.0], 20, 'pointDown', 'neutral', keys=[k(0.0, look=[-1.0, 0.0, 1.8]), k(0.4, look=[-1.2, 0.0, 0.6])]),
        act('plong2', [1.0, 0, 0.4], -30, 'holdUp', 'neutral', keys=[k(0.0, look='camera')]),
        act('mec', [-3.65, 2.76, 2.2], 25, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.0, 0.5]), k(0.0, toon={'bend': {'neck': [0.35, 0, 0, 1, None], 'spine': [0.25, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.0), k(0.9, look=[1.0, 0.5, 0.4]), k(1.3, toon={'bend': {'neck': [0.35, 0, 0, 1, None], 'spine': [0.25, 0, 0, 1, None]}, 'face': {**SQUINT, 'lid': 1.0}}, toonDur=0.04), k(1.36, toon={'bend': {'neck': [0.35, 0, 0, 1, None], 'spine': [0.25, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.06)]),
        act('poisson7', [0.2, 0.0, 1.9], 0, 'stand', 'neutral', scale=0.35, keys=[*[k(r(0.1 + 0.3 * j), to=[r(0.2 + 0.05 * (j % 2)), 0.25 if j % 2 == 0 else 0.0, 1.9], dur=0.15, ease='out' if j % 2 == 0 else 'in') for j in range(6)]])],
        props=[P('river7', 'drainedRiver', pos=[0.0, 0.16, 0.0], opts={'w': 8, 'len': 40, 'qh': 2.45, 'bridgeZ': -16}), GL('gl7'),
               P('mask71', 'diveMask', on={'actor': 'plong1', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.28, 'y': 0.3}),
               P('mask72', 'diveMask', on={'actor': 'plong2', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.28, 'y': 0.3}),
               P('boot7', 'slab', on={'actor': 'plong2', 'hand': 'R', 'offset': [0.0, 0.12, 0.04]}, opts={'w': 0.13, 'h': 0.3, 'd': 0.13, 'color': '#3B2A20'}),
               P('boot7b', 'slab', on={'actor': 'plong2', 'hand': 'R', 'offset': [0.0, -0.02, 0.12]}, opts={'w': 0.13, 'h': 0.1, 'd': 0.3, 'color': '#3B2A20'}),   # (review 1) the shaft and the foot of a boot (one box read as a brick)
               *[P(f'tank7{j}', 'slab', on={'actor': f'plong{j}', 'joint': 'torso', 'offset': [0.0, 0.15, -0.2]}, opts={'w': 0.2, 'h': 0.55, 'd': 0.18, 'color': '#F2C21E', 'outline': 0.006}) for j in (1, 2)],   # air tanks
               P('tour7', 'eiffelTower', pos=[3.0, 0.0, -95.0], opts={'h': 30, 'style': 'v2'})],   # (review 1) nothing said Seine
        cams=[FC(0.0, [-2.9, 4.7, 3.7], [[-3.65, 5.5, 2.2], [-3.65, 4.0, 2.2], [-1.0, 2.4, 1.0], [1.0, 2.6, 0.4], [-1.0, 1.0, 1.0], [1.0, 1.0, 0.4]], top=0.12, bottom=0.78)])   # (stills 7) behind his shoulder on the quay, looking down at the divers
st.cue('sfx:splash', 'S07', 0.1, 0.15); st.cue('sfx:splash', 'S07', 0.7, 0.12); st.cue('sfx:splash', 'S07', 1.3, 0.12)

# 8: the army sent helicopters. At night in the street, from low: a helicopter hangs over the roofs, its searchlight sweeps the street, crosses him,
#    and the glasses on his head flash in the beam; the beam sweeps on
D8 = st.dur('S08'); PASS8 = 1.0
st.shot('S08', 'parisStreet', setOpts={'night': True, 'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, look={'sun': 0.15, 'fill': 0.35, 'exposure': 1.1}, actors=[
        act('mec', [5.0, 0, 0.0], 20, 'stand', 'neutral', keys=[k(0.0, look=[3.0, 12.0, -10.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(r(PASS8 + 0.15), look='camera'), k(r(PASS8 + 0.15), toon={'face': {**SQUINT, 'lid': 0.6}}, toonDur=0.08)])],
        props=[P('heli8', 'helicopter', pos=[2.5, 13.0, -9.0], ry=150, rot=[0.12, 0, 0], scale=0.9, opts={'spin': 5, 'beam': True, 'beamLen': 18, 'beamR': 2.4, 'tilt': 30, 'sweep': [[0.0, -40], [PASS8, -8], [D8, 30]]},
                 keys=[k(0.0, to=[3.5, 13.5, -8.0], dur=D8, ease='linear')]), GL('gl8', glint=[r(PASS8 - 0.05)]), P('star8', 'flashBursts', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.68, 0.12], 'face': 'camera'}, opts={'n': 1, 'w': 0.0, 'h': 0.0, 'at': [r(PASS8 - 0.08)], 'life': 0.25}),   # (review 1) no flash registered
               P('spot8', 'glowLight', pos=[5.0, 3.0, 0.4], opts={'color': '#FFF4C8', 'k': 6.0, 'dist': 4.0}, keys=[k(0.0, visible=False), k(r(PASS8 - 0.15), visible=True), k(r(PASS8 + 0.2), visible=False)])],
        cams=[FC(0.0, [6.4, 0.9, 3.0], [[5.0, 2.9, 0.0], [5.0, 0.9, 0.0], [2.5, 16.0, -9.0], [6.0, 12.0, -8.0]], top=0.08, bottom=0.8)])
st.cue('sfx:engine', 'S08', 0.05, 0.4); st.cue('sfx:ding', 'S08', r(PASS8 - 0.05), 0.25)

# 9: satellites scanned the planet. Space, wide: the opaque blue Earth fills the lower half under a black starry sky; three satellites in orbit
#    over it, the nearest in the upper middle, each sweeping a saturated red fan down across the globe (review 1: the globe filled the whole frame
#    behind one big satellite and read as a glitch of translucent triangles)
D9 = st.dur('S09'); EARTH9 = [0.0, -9.0, -26.0]   # (stills 6) at -15 the globe filled the frame
SATS9 = [('sat9', [-0.2, 1.75, -3.2], [0.32, 0.3, 0.0], 0.3, 72.0, 0.1), ('sat9b', [-1.9, 2.9, -10.0], [0.3, -0.5, 0.15], 0.22, 70.0, 0.3), ('sat9c', [2.2, 2.2, -12.0], [0.32, 0.7, -0.15], 0.22, 64.0, 0.2)]
st.shot('S09', 'spaceDark', actors=[],
        props=[P('earth9', 'earthGlobe', pos=EARTH9, scale=7.0, opts={'spin': 0.06}),
               *[P(n_, 'satellite', pos=p_, rot=ro_, scale=s_, opts={'scan': [[t_, 9.0]], 'scanLen': L_, 'sweepDeg': 24, 'fanOpacity': 0.34, 'fanBlend': 'normal', 'fanColor': '#FF2A1E', 'fanWidth': 0.11},   # (stills 7) narrow beams: wide ones hid the Earth
                   keys=[k(0.0, to=[r(p_[0] + 0.35), r(p_[1] + 0.08), p_[2]], dur=D9, ease='linear')]) for n_, p_, ro_, s_, L_, t_ in SATS9]],
        cams=[cam(0.0, [0.0, 1.0, 5.0], [0.12, 1.0, 4.85], [0.0, -0.3, -6.0], [0.08, -0.3, -6.0], lens=44)])
st.cue('sfx:static', 'S09', 0.1, 0.2); st.cue('sfx:ding', 'S09', 1.2, 0.15)

# 10: the other countries sent their dogs. In the street: dogs of every colour, each with a collar of its own colour, sniff round his shoes and
#    legs; one sits, stares up at his head, tilts its own, and goes back to sniffing
D10 = st.dur('S10'); STARE10 = 0.55
DOGP = [[5.6, 0, 0.9], [4.3, 0, 0.7], [5.9, 0, -0.5], [4.4, 0, -0.6]]
st.shot('S10', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.1], 20, 'stand', 'unimpressed', keys=[k(0.0, look=[5.3, 0.3, 0.9]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(r(STARE10 + 0.2), look=[5.55, 0.65, 0.4], lookDur=0.12), k(1.1, look='camera'),
            k(1.4, toon={'face': {**SQUINT, 'lid': 1.0}}, toonDur=0.04), k(1.46, toon={'face': SQUINT}, toonDur=0.06)]),
        act('chien1', [5.6, 0, 0.4], -112, 'stand', 'neutral', scale=0.9, keys=[k(0.0, look=[5.0, 0.2, 0.1]), k(STARE10, look=[5.0, 2.75, 0.1]),   # (review 1) seen from behind: now in profile beside him
            k(r(STARE10 + 0.05), toon={'bend': {'neck': [0.0, 0.0, 0.35, 1, None]}, 'face': {'eye': 0.3}}, toonDur=0.15),
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
            k(0.35, toon={'reach': {'R': [0.72, 2.45, -2.05, 1, 0.05], 'L': [-0.25, 1.35, -1.85, 1, 0.04]}, 'hands': {'R': 'point', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'open', 'brow': 0.6}}, toonDur=0.2, toonEase='out'),
            k(0.9, toon={'reach': {'R': [0.72, 2.45, -2.05, 1, 0.05], 'L': [-0.25, 1.35, -1.85, 1, 0.04]}, 'hands': {'R': 'point', 'L': 'open'}, 'face': {'lid': 1.0, 'mouth': 'open', 'brow': 0.6}}, toonDur=0.05),
            k(1.0, toon={'reach': {'R': [0.72, 2.45, -2.05, 1, 0.05], 'L': [-0.25, 1.35, -1.85, 1, 0.04]}, 'hands': {'R': 'point', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'open', 'brow': 0.6}}, toonDur=0.07)])],   # (review 1) out to the side: the sleeve covered his face
        props=[P('echarpe11', 'mayorSash', on={'actor': 'ministre', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.21, 'w': 0.17, 'len': 0.8}), *[P(f'fl11{j}', 'glowLight', pos=[r(-1.2 + 1.2 * j), 1.8, 1.2], opts={'color': '#FFFFFF', 'k': 6.0, 'dist': 6.0}, keys=[k(0.0, visible=False), k(r(0.3 + 0.35 * j), visible=True), k(r(0.36 + 0.35 * j), visible=False)]) for j in range(3)]],
        cams=[FC(0.0, [0.7, 1.7, 1.6], [[0.0, 2.6, -2.45], [0.72, 2.55, -2.05], [0.0, 0.9, -2.0], [-0.6, 1.3, -2.0]], top=0.14, bottom=0.78)])
st.shot('S12', 'pressRoom', setOpts={'backdrop': 'GOUVERNEMENT', 'fontScale': 0.55}, actors=[MIN([k(0.0, look=[1.1, 1.9, -2.2]), k(0.0, toon={'reach': {'R': [0.8, 1.9, -2.2, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.0),
            k(0.6, look='camera')])],
        props=[P('poster12', 'rewardPoster', pos=[1.15, 0, -2.3], ry=-15, opts={'at': 0.05, 'w': 1.0, 'h': 1.35, 'stand': 0.9})],
        cams=[FC(0.0, [0.5, 1.65, 1.5], [[0.0, 2.6, -2.45], [1.15, 2.35, -2.3], [1.15, 0.9, -2.3], [0.0, 1.0, -2.0], [1.72, 2.4, -2.45], [1.72, 0.9, -2.45]], top=0.2, bottom=0.78)])   # (stills 1) its right edge was cut
st.cue('sfx:click', 'S11', 0.3, 0.2); st.cue('sfx:click', 'S11', 0.65, 0.2); st.cue('sfx:boing', 'S12', 0.05, 0.25); st.cue('sfx:cash', 'S12', 0.25, 0.3)

# 13: the whole world searched for a year. An office turned upside down, tight on him (review 1: beige wall and floor filled half the frame, the
#    searches did not read and the calendar showed its code name): one searcher crawls under a desk, his legs sticking out; one kneels with a big
#    magnifying glass at the floor; one holds the potted plant up over his head and peers at the bottom of the pot; on the wall beside his head a big
#    calendar sheds its twelve months, JANVIER to DÉCEMBRE; in the middle he stands, squinting, the glasses on his head
D13 = st.dur('S13'); MOIS = ['JANVIER', 'FÉVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN', 'JUILLET', 'AOÛT', 'SEPTEMBRE', 'OCTOBRE', 'NOVEMBRE', 'DÉCEMBRE']
DESK13 = [-1.0, 0, -0.85]; POT13 = [1.0, 1.86, -1.95]
PLANTK = lambda f: {'reach': {'R': [r(POT13[0] - 0.16), r(POT13[1] + 0.16), POT13[2], 1, 0.03], 'L': [r(POT13[0] + 0.16), r(POT13[1] + 0.16), POT13[2], 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f}
st.shot('S13', 'office', setOpts={'picture': False, 'carpet': False, 'printer': False}, actors=[
        act('mec', [0.0, 0, -1.4], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(1.0, look=[-1.0, 0.5, -0.9]), k(1.6, look='camera'),
            k(1.9, toon={'face': {**SQUINT, 'lid': 1.0}}, toonDur=0.04), k(1.96, toon={'face': SQUINT}, toonDur=0.06)]),
        act('cherch1', [-0.55, 0, -0.85], -90, 'crawl', 'neutral', keys=[k(0.0, look=[-1.3, 0.2, -0.85])]),   # his head under the desk, his legs out
        act('cherch2', [1.0, 0, -0.7], -70, 'peerIn', 'neutral', keys=[k(0.0, look=[0.3, 0.0, -0.4])]),
        act('cherch3', [1.0, 0, -2.25], -25, 'stand', 'neutral', keys=[k(0.0, look=[POT13[0], r(POT13[1] - 0.05), POT13[2]]), k(0.0, toon=PLANTK({'lid': 0.3, 'mouth': 'O', 'brow': 0.4}), toonDur=0.0),
            k(1.2, toon=PLANTK({'lid': 1.0, 'mouth': 'O', 'brow': 0.4}), toonDur=0.05), k(1.32, toon=PLANTK({'lid': 0.3, 'mouth': 'O', 'brow': 0.4}), toonDur=0.07)])],
        props=[GL('gl13'), P('cal13', 'monthCalendar', pos=[-0.62, 1.95, -3.55], opts={'months': MOIS, 'w': 0.7, 'h': 0.92, 'flipAt': 0.15, 'dur': 0.16}),
               P('bureau13', 'table', pos=DESK13, opts={'w': 1.0, 'd': 0.62, 'h': 0.74}), P('plante13', 'plant', pos=POT13, scale=0.8, opts={'seed': 21}),
               P('mag13', 'magnifier', on={'actor': 'cherch2', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=2.0)],
        cams=[FC(0.0, [0.35, 1.6, 2.2], [[0.0, 2.9, -1.4], [-0.55, 2.35, -3.55], [r(POT13[0] + 0.1), 2.7, POT13[2]], [r(DESK13[0] - 0.5), 0.74, DESK13[2]], [1.3, 0.0, -0.6], [-0.2, 0.0, -0.85]], top=0.12, bottom=0.78)])
st.cue('sfx:paper', 'S13', 0.2, 0.2); st.cue('sfx:paper', 'S13', 0.9, 0.2); st.cue('sfx:paper', 'S13', 1.6, 0.2)

# 14: yesterday a child found them. In the street a boy tugs at his sleeve and points up at his head, mouth open; he looks down at the boy
D14 = st.dur('S14'); TUG14 = 0.3
st.shot('S14', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.0], 15, 'stand', 'unimpressed', keys=[k(0.0, look=[3.0, 2.0, 2.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(r(TUG14 + 0.1), look=[4.35, 1.0, 0.45]), k(r(TUG14 + 0.12), toon={'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.12), k(1.3, toon={'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': {**SQUINT, 'lid': 1.0}}, toonDur=0.04), k(1.36, toon={'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': SQUINT}, toonDur=0.06), k(1.7, look='camera')]),
        act('gamin', [4.35, 0, 0.45], 70, 'stand', 'neutral', keys=[k(0.0, look=[5.0, 2.6, 0.0]), k(0.0, toon={'touch': {'R': ['@mec.handL', 0.0, 0.0, 0.0, 1, 0.0]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.0),
            *[k(r(TUG14 * (j + 1) / 2), toon={'touch': {'R': ['@mec.handL', 0.0, r(-0.03 * (j % 2)), 0.0, 1, 0.0]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.06) for j in range(2)],
            k(r(TUG14 + 0.35), toon={'reach': {'R': [4.5, 1.85, 0.32, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.15, toonEase='out'), k(1.5, toon={'reach': {'R': [4.5, 1.9, 0.32, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 1.0, 'mouth': 'open'}}, toonDur=0.04), k(1.56, toon={'reach': {'R': [4.85, 2.8, 0.2, 1, 0.05]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.06)])],   # ...then points up at his head
        props=[GL('gl14', glint=[r(TUG14 + 0.6)])],
        cams=[FC(0.0, [5.6, 1.4, 3.2], [[5.0, 2.95, 0.0], [5.0, 0.6, 0.0], [4.35, 0.6, 0.45], [4.85, 2.85, 0.2]], top=0.12, bottom=0.78)])
st.cue('sfx:stepSoft', 'S14', 0.1, 0.15); st.cue('sfx:gasp', 'S14', r(TUG14 + 0.35), 0.2)

# 15: on his head. Close: his eyes roll up to the top of his head; the glasses flash; his eyes pop (TROUVÉES)
D15 = st.dur('S15'); UP15 = 0.15; POP15 = 0.55
st.shot('S15', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.0], 15, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': SQUINT}, toonDur=0.0),
            k(UP15, toon={'face': {'lid': 0.0, 'low': 0.0, 'gy': -1.0, 'eye': 0.6, 'brow': 0.7, 'mouth': 'line', 'noBlink': 1}}, toonDur=0.15, toonEase='inOut'),   # the eyes roll up, wide...
            k(r(POP15 - 0.08), toon={'sq': [1.1, 0.9, 1.1], 'face': {'lid': 0.0, 'gy': -1.0, 'eye': 0.6, 'brow': 0.9, 'mouth': 'line', 'noBlink': 1}}, toonDur=0.05, toonEase='in'),   # ...a squash...
            k(POP15, toon={'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.0, 'gy': -0.6, 'pop': 1.0, 'popLen': 0.3, 'brow': 1.0, 'mouth': 'O', 'noBlink': 1}}, toonDur=0.04, toonEase='out'),   # ...POP, the eyes out on stalks...
            k(r(POP15 + 0.42), toon={'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.0, 'gy': -0.6, 'pop': 1.0, 'popLen': 0.3, 'brow': 1.0, 'mouth': 'O', 'noBlink': 1}}, toonDur=0.1),   # ...held
            k(r(POP15 + 0.5), toon={'face': {'lid': 0.0, 'gy': -0.6, 'eye': 0.5, 'brow': 0.8, 'mouth': 'O'}}, toonDur=0.08)])],
        props=[GL('gl15', glint=[r(UP15 + 0.2)])],
        cams=[FC(0.0, [5.5, 2.35, 1.5], [[5.0, 3.0, 0.0], [5.0, 1.75, 0.0], [5.35, 2.3, 0.1], [4.65, 2.3, 0.1]], top=0.2, bottom=0.74)])
st.cue('sfx:ding', 'S15', r(UP15 + 0.2), 0.35); st.cue('pop', 'S15', POP15, 0.25)

# 16: the child got the million. A town-hall stage: the boy holds a giant cheque over his head and jumps; the minister claps beside him
D16 = st.dur('S16')
st.shot('S16', 'mairie', setOpts={'desk': False, 'map': False}, actors=[   # (review 1) no map: its stamp from another episode showed behind the cheque
        act('gamin', [0.0, 0, -1.2], 0, 'holdUp', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'bigsmile', 'brow': 0.8}}, toonDur=0.0),
            *[k(r(0.15 + 0.4 * j), to=[0.0, 0.25 if j % 2 == 0 else 0.0, -1.2], dur=0.18, ease='out' if j % 2 == 0 else 'in') for j in range(4)]]),
        act('ministre', [1.1, 0, -1.5], -40, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.6, -1.2]), *[k(r(0.1 + 0.15 * j), toon={'reach': {'R': [r(0.85 + 0.05 * (j % 2)), 1.6, -1.15, 1, 0.04], 'L': [r(0.72 - 0.05 * (j % 2)), 1.6, -1.2, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'smirk'}}, toonDur=0.06) for j in range(8)]])],
        props=[P('cheque16', 'bigCheque', on={'actor': 'gamin', 'hand': 'R', 'offset': [0.0, 0.0, 0.05], 'face': 'camera', 'faceFlat': True}, scale=1.2, opts={'text': 'RÉCOMPENSE', 'amount': '1 000 000 €'}),
               P('conf16', 'confettiRain', pos=[0.2, 0.0, -1.1], opts={'w': 2.6, 'h': 3.4, 'd': 1.4, 'n': 170, 'size': 0.05})],   # (review 1) the cheque said ASSURANCE 3 000 € and the one-piece `confetti` showed nothing
        cams=[FC(0.0, [0.4, 1.5, 2.2], [[0.0, 2.6, -1.2], [0.0, 0.0, -1.2], [1.1, 2.5, -1.5], [-0.8, 2.4, -1.2], [1.5, 1.4, -1.5], [1.1, 0.0, -1.5]], top=0.14, bottom=0.78)])   # the minister whole
st.cue('sfx:fanfare', 'S16', 0.05, 0.3); st.cue('sfx:cash', 'S16', 0.4, 0.2)

# 17: the man is looking for his keys. His living room by the door: he pats every pocket, looks round, squinting; his key ring hangs from his own
#    mouth, jingling; a look at us
D17 = st.dur('S17')
st.shot('S17', 'livingRoom', actors=[
        act('mec', [-0.4, 0, -0.6], 15, 'patPockets', 'unimpressed', keys=[k(0.0, look=[-1.6, 2.3, 0.6]), k(0.0, toon={'face': {**SQUINT, 'mouth': 'clench'}}, toonDur=0.0), k(0.6, look=[1.6, 2.3, 0.6]), k(1.1, look='camera'),   # (review 1) looking at his pockets, his face went away
            k(1.45, to=[-0.4, 0, -0.6], dur=0.01, clip='stand', face='keep'), k(1.75, toon={'face': {**SQUINT, 'mouth': 'clench', 'lid': 1.0}}, toonDur=0.12, toonEase='inOut'), k(1.89, toon={'face': {**SQUINT, 'mouth': 'clench'}}, toonDur=0.14, toonEase='inOut')])],   # he stops: a slow blink at us, held
        props=[GL('gl17', glint=[2.1]), P('keys17', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.1, 0.13], 'face': 'camera'}, scale=3.0),   # (review 1) twice the size
               P('star17', 'flashBursts', on={'actor': 'mec', 'joint': 'head', 'offset': [0.06, -0.05, 0.2], 'face': 'camera'}, opts={'n': 1, 'w': 0.0, 'h': 0.0, 'at': [2.1], 'life': 0.22})],
        cams=[FC(0.0, [-1.5, 1.45, 1.2], [[-0.4, 2.95, -0.6], [-0.4, 1.2, -0.6], [0.0, 1.9, -0.4], [-0.8, 1.9, -0.4]], top=0.14, bottom=0.76, drift=(0.3, 0.12, -0.5))])   # a slow push-in for the end hold   # (build) low from his left (S01's set-up was repeated)
st.cue('sfx:rattleShort', 'S17', 0.3, 0.15); st.cue('sfx:rattleShort', 'S17', 0.9, 0.15); st.cue('sfx:ding', 'S17', 2.1, 0.15)

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
