#!/usr/bin/env python3
"""Le serrurier (story 29): this man lost his keys and called a locksmith. The locksmith had lost his. He called a locksmith, who
called a locksmith, who called a locksmith. At noon there were forty of them at the door; in the evening the queue went round the
neighbourhood. The police came: they had lost their keys. The firemen too. Then the man put his hand in his pocket. His keys were
right there. He said nothing. He moved house."""
from story_kit import *

st = Story('serrurier')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(2, 15)])
PI = math.pi
MEC_DOOR = [0.0, 0, -7.55]
DOOR = P('door', 'door', pos=[0.0, 0, -8.29], opts={'w': 1.0, 'h': 2.35, 'color': '#7FC8C0'})   # light teal: the navy suit and the keys read against it
PHONE = lambda who: P(f'ph_{who}', 'smartPhone', on={'actor': who, 'hand': 'R', 'offset': [0.0, -0.08, 0.03], 'rot': [0, 0, 0]})
BUBBLE = lambda pid, text, pos, pop, w=0.5: P(pid, 'speechBubble', pos=pos, opts={'text': text, 'popAt': pop, 'tail': 'down', 'w': w, 'h': w * 0.5})
VAN = lambda pos, band='#2F62B5', ry=0: P('van', 'serrurierVan', pos=list(pos), ry=ry, opts={'band': band})
TOOLS = lambda pid, pos, ry=0: P(pid, 'toolbox', pos=list(pos), ry=ry)
DUSK = {'sky': ['#7A86C8', '#FFC48E']}   # a bright pastel golden hour (lilac top, peach horizon), not a dark dusk
EVENING = {'hemi': 1.05, 'sky': '#FFE6CC', 'ground': '#8C7C86', 'keyI': 1.15, 'key': '#FFD4A8', 'dir': [2.0, 6.0, 9.0]}   # warm key in front of the faces
# the queue: from the door down the garden path, then along the pavement
QUEUE_DAY = P('queue', 'queueFigures', pos=[0, 0, 0], opts={'path': [[0.0, -5.2], [0.0, -0.7], [26.0, -0.7]], 'gap': 0.78, 'seed': 3})
QUEUE_LONG = P('queue', 'queueFigures', pos=[0, 0, 0], opts={'path': [[0.0, -5.2], [0.0, -0.7], [70.0, -0.7], [70.0, -40.0], [-30.0, -40.0]], 'gap': 0.8, 'seed': 5, 'max': 260})
CROWD = lambda ids, z0=-6.6: [act(a, [x, 0, z0 + dz], 180 + ry, 'stand', 'neutral') for a, (x, dz, ry) in zip(ids, ((-0.75, 0.0, 15), (0.75, 0.1, -15), (-1.4, 0.7, 25), (1.35, 0.8, -20), (-0.4, 1.0, 5), (0.5, 1.3, -8)))]

# 1-2: he has lost his keys (pats his pockets at his door), calls a locksmith
T1 = st.at('S01', 'L01', 5)    # « clés »
st.shot('S01', 'suburbDay', actors=[act('mec', MEC_DOOR, 0, 'patPockets', 'shocked')], props=[DOOR, BUBBLE('q0', '?', [0.3, 2.2, -7.45], T1 - 0.1)],
        cams=[cam(0.0, [0.35, 1.85, -5.55], [0.33, 1.85, -5.85], [0.0, 1.62, -7.55], [0.0, 1.62, -7.55], lens=44, shake=0.005)])
st.shot('S02', 'suburbDay', actors=[act('mec', MEC_DOOR, -15, 'phoneEar', 'neutral')], props=[DOOR, PHONE('mec')],
        cams=[cam(0.0, [-1.05, 1.9, -5.4], [-0.98, 1.9, -5.55], [0.0, 1.75, -7.6], [0.0, 1.75, -7.6], lens=44)])
# 3-6: the locksmith had lost his (pats his pockets at his van); he calls a locksmith, who calls a locksmith, who calls a locksmith
T3 = st.at('S03', 'L02', 5)    # « siennes »
st.shot('S03', 'suburbDay', actors=[act('serr1', [-0.75, 0, 2.0], 0, 'patPockets', 'worried')], props=[VAN((1.0, 0, 0.55)), TOOLS('tb1', (-0.25, 0, 2.15), 20), BUBBLE('q1', '?', [-0.75, 2.55, 2.0], T3 - 0.1)],
        cams=[cam(0.0, [-0.1, 1.6, 6.3], [-0.1, 1.6, 6.0], [-0.25, 1.4, 1.5], [-0.25, 1.4, 1.5], lens=44)])
st.shot('S04', 'suburbDay', actors=[act('serr1', [-0.75, 0, 2.0], 10, 'phoneEar', 'neutral')], props=[VAN((1.0, 0, 0.55)), TOOLS('tb1', (-0.25, 0, 2.15), 20), PHONE('serr1')],
        cams=[cam(0.0, [0.0, 1.9, 4.6], [-0.05, 1.9, 4.4], [-0.85, 1.75, 1.9], [-0.85, 1.75, 1.9], lens=44)])
# the chain builds up: the earlier callers wait behind each new one
st.shot('S05', 'parisStreet', actors=[act('serr2', [0.0, 0, -1.3], 0, 'phoneEar', 'neutral'), act('serr1', [-0.75, 0, -2.5], 15, 'armsCrossed', 'unimpressed')],
        props=[VAN((2.7, 0, -3.4), '#2E8B57'), PHONE('serr2'), TOOLS('tw1', (-0.3, 0, -2.4), 30)],
        cams=[cam(0.0, [0.9, 0.75, 2.8], [0.85, 0.75, 2.55], [0.1, 1.55, -1.6], [0.1, 1.55, -1.6], lens=44)])
st.shot('S06', 'park', actors=[act('serr3', [0.0, 0, -1.2], -10, 'phoneEar', 'neutral'), act('serr1', [0.85, 0, -2.7], -20, 'armsCrossed', 'unimpressed'), act('serr2', [-0.9, 0, -2.9], 20, 'armsCrossed', 'unimpressed')],
        props=[VAN((-3.2, 0, -4.2), '#E07A2E'), PHONE('serr3')],
        cams=[cam(0.0, [-0.45, 1.95, 1.6], [-0.4, 1.95, 1.4], [0.0, 1.75, -1.6], [0.0, 1.75, -1.6], lens=44, roll=8)])
# 7-8: forty at the door by noon (a crowd on the path, the queue along the pavement); in the evening the queue goes round the neighbourhood
st.shot('S07', 'suburbDay', actors=[act('mec', MEC_DOOR, 0, 'shrug', 'unimpressed')] + CROWD(['serr1', 'serr2', 'serr3', 'serr4', 'serr5', 'serr6']),
        props=[DOOR, QUEUE_DAY] + [TOOLS(f'tc{i}', (x, 0, z), r) for i, (x, z, r) in enumerate(((-0.45, -6.4, 10), (1.05, -6.3, -30), (-1.1, -5.7, 40), (0.95, -5.5, 5)))],
        cams=[cam(0.0, [5.0, 6.2, 5.0], [4.7, 6.0, 4.6], [0.0, 0.9, -4.2], [0.0, 0.9, -4.3], lens=44)])
HOODS = [P(f'hc{i}', 'cottage', pos=[x, 0, z], ry=r, opts={'seed': 50 + i}) for i, (x, z, r) in enumerate([(x, -9.5, 0) for x in range(18, 67, 9)] + [(x, 9.0, 180) for x in range(-12, 67, 9)]
         + [(80.0, z, -90) for z in range(-8, -37, -9)] + [(x, -50.0, 0) for x in range(60, -25, -10)])]
st.shot('S08', 'suburbDay', setOpts=DUSK, light=EVENING, props=[QUEUE_LONG] + HOODS,
        cams=[cam(0.0, [-9.0, 21.0, 15.0], [-7.5, 21.5, 14.0], [14.0, 0.0, -6.0], [16.0, 0.0, -7.0], lens=44)])
# 9-11: the police came (they had lost their keys); the firemen too
D9 = st.dur('S09')
st.shot('S09', 'suburbDay', setOpts=DUSK, light=EVENING, props=[QUEUE_DAY, P('pcar', 'policeCar', pos=[-15.0, 0, 0.9], keys=[k(0.0, to=[-4.5, 0, 0.9], dur=min(0.9, D9 - 0.1), ease='out')])],
        cams=[cam(0.0, [1.2, 0.8, 4.4], [1.05, 0.8, 4.25], [-4.2, 0.9, 0.7], [-4.5, 0.9, 0.7], lens=44)])
T10 = st.at('S10', 'L09', 4)   # « clés »
st.shot('S10', 'suburbDay', setOpts=DUSK, light=EVENING, actors=[act('flic', [-3.4, 0, 2.3], 10, 'patPockets', 'worried')], props=[QUEUE_DAY, P('pcar', 'policeCar', pos=[-4.5, 0, 0.9]), BUBBLE('q2', '?', [-3.4, 2.55, 2.3], T10 - 0.15)],
        cams=[cam(0.0, [-2.6, 1.7, 6.0], [-2.65, 1.7, 5.75], [-3.45, 1.45, 1.8], [-3.45, 1.45, 1.8], lens=44)])
T11 = st.at('S11', 'L10', 2)   # « aussi »
st.shot('S11', 'suburbDay', setOpts=DUSK, light=EVENING, actors=[act('pompier', [-7.1, 0, 2.5], 10, 'patPockets', 'sad')], props=[P('ftruck', 'fireTruck', pos=[-9.0, 0, 0.6]), QUEUE_DAY, BUBBLE('q3', '?', [-7.1, 2.55, 2.5], T11 - 0.15)],
        cams=[cam(0.0, [-6.4, 1.7, 7.4], [-6.5, 1.7, 7.1], [-7.9, 1.55, 1.8], [-7.9, 1.55, 1.8], lens=44)])
# 12-15: his hand in his pocket; the keys were right there; he said nothing (the crowd stares); he moved house
T12a, T12b = st.at('S12', 'L11', 6), st.at('S12', 'L11', 9)   # « main », « poche »
st.shot('S12', 'suburbDay', setOpts=DUSK, light=EVENING, actors=[act('mec', MEC_DOOR, 0, 'stand', 'neutral', keys=[k(T12a - 0.2, clip='handInPocket'), k(T12b, expr='surprised')])], props=[DOOR, BUBBLE('ex', '!', [0.3, 2.25, -7.45], T12b)],
        cams=[cam(0.0, [0.25, 1.75, -4.75], [0.24, 1.75, -4.95], [0.0, 1.43, -7.6], [0.0, 1.43, -7.6], lens=44)])
st.shot('S13', 'suburbDay', setOpts=DUSK, light=EVENING, actors=[act('mec', MEC_DOOR, 0, 'dangleItem', 'grimace')],
        props=[DOOR, P('keys', 'keyRing', pos=[-0.09, 1.84, -6.98], scale=1.6, opts={'bare': True, 'swing': 0.05})]
              + [P(f'key{i}', 'glbModel', pos=[-0.09 + dx, 1.77, -6.97 + 0.005 * i], ry=ry, rot=[1.4, 0, tz], opts={'src': f'/assets/models/key-objaverse-{row}/model.glb', 'size': 0.105, 'outline': 0.0012})
                 for i, (row, dx, ry, tz) in enumerate(((4643, -0.04, 15, 0.3), (18162, 0.0, 0, 3.1416), (16286, 0.04, -15, -0.3)))],   # sand3d keys (CC BY 4.0, credits in tools/credits.txt)
        cams=[cam(0.0, [0.05, 1.95, -5.75], [0.04, 1.95, -5.9], [-0.12, 1.87, -7.55], [-0.12, 1.87, -7.55], lens=44)])
st.shot('S14', 'suburbDay', setOpts=DUSK, light=EVENING, actors=[act('mec', MEC_DOOR, 0, 'stand', 'unimpressed')] + [act(a, [x, 0, z], 180 + r, 'stand', 'neutral') for a, (x, z, r) in zip(['serr1', 'serr2', 'flic', 'pompier'], ((-0.5, -6.4, 10), (0.52, -6.3, -10), (-1.1, -5.9, 15), (1.15, -5.8, -15)))],
        props=[DOOR], cams=[cam(0.0, [0.25, 1.95, -4.4], [0.24, 1.95, -4.55], [0.0, 1.62, -7.6], [0.0, 1.62, -7.6], lens=44)])
D15, T15 = st.dur('S15'), st.at('S15', 'L14', 2) - 0.05   # « déménagé »: the big sign pops in
st.shot('S15', 'suburbDay', setOpts=DUSK, light=EVENING, actors=[act('mec', [0.0, 0, -1.2], 160, 'carry', 'unimpressed', keys=[k(0.0, to=[-0.45, 0, 0.3], dur=D15 - 0.15, clip='carryBox')])],
        props=[QUEUE_DAY, P('box', 'cardboardBox', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.3, 0.42]}, scale=0.75, opts={'text': ''}), P('boxplant', 'plant', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.06, 0.62, 0.42]}, scale=0.45),
               P('sale2', 'noticeBoard', pos=[0.62, 1.6, 0.3], ry=-12, opts={'text': 'À VENDRE', 'style': 'sign', 'w': 0.78, 'h': 0.33, 'bg': '#F4F1E8', 'fg': '#C8322A', 'frame': '#1C2E4A', 'popAt': T15})],
        cams=[cam(0.0, [0.7, 1.6, 4.6], [0.6, 1.6, 4.4], [0.2, 1.3, -0.5], [0.2, 1.3, -0.5], lens=44)])
st.card('S07', '40 SERRURIERS'); st.card('S13', 'DANS SA POCHE')
st.cue('sfx:ring', 'S02', 0.05, 0.25); st.cue('pop', 'S03', T3 - 0.1, 0.35); st.cue('sfx:ring', 'S04', 0.05, 0.22); st.cue('sfx:ring', 'S05', 0.05, 0.2); st.cue('sfx:ring', 'S06', 0.05, 0.2)
st.cue('gust', 'S08', 0.0, 0.3); st.cue('engine', 'S09', 0.0, 0.4); st.cue('sfx:brake', 'S09', min(0.85, D9 - 0.15), 0.35); st.cue('pop', 'S10', T10 - 0.15, 0.35); st.cue('sfx:carDoor', 'S11', 0.1, 0.3)
st.cue('pop', 'S01', T1 - 0.1, 0.35); st.cue('pop', 'S11', T11 - 0.15, 0.35); st.cue('sfx:clink', 'S12', T12b - 0.1, 0.35); st.cue('pop', 'S12', T12b, 0.4); st.cue('pop', 'S15', T15, 0.45); st.cue('sfx:bell', 'S13', 0.12, 0.3); st.cue('sfx:clink', 'S13', 0.2, 0.3); st.cue('sfx:paper', 'S15', 0.2, 0.25)
LOCK = lambda seed: {'preset': 'worker', 'hat': 'beanie', 'hatColor': '#1C2E4A', 'suit': '#2F5E9E', 'pants': '#22385E', 'cuff': '#2F5E9E', 'lapel': '#F2C94C', 'seed': seed}
st.write('Le serrurier', {**{f'serr{i}': LOCK(40 + i) for i in range(1, 7)}, 'flic': {'preset': 'cop', 'seed': 21}, 'pompier': {'preset': 'pompier', 'seed': 31, 'hatColor': '#D5DBE0'}})
