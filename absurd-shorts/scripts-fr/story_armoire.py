#!/usr/bin/env python3
"""L'armoire (story 30): this man assembled a flat-pack wardrobe. At the end, one screw was left. He bought the same wardrobe again to
find out where it went: two screws left. He bought ten: twenty screws left. His flat became a furniture shop; the neighbours came to do
their shopping; the shop hired him. His first customer bought a wardrobe. The next day he came back: one screw left. The man said:
« C'est normal. »"""
from story_kit import *

st = Story('armoire')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 3), ('S04', 'L03', 0), ('S05', 'L03', 6)] + [(f'S{i + 2:02d}', f'L{i:02d}', 0) for i in range(4, 14)])
PI = math.pi
LR = {'sofa': False, 'tv': False}
ARM = lambda pid, x, z=-2.02, ry=0, tag=None: P(pid, 'armoire', pos=[x, 0, z], ry=ry, opts={'tag': tag} if tag else {})
BOX = lambda pid, x, z, ry=0, lying=False: P(pid, 'flatBox', pos=[x, 0, z], ry=ry, opts={'lying': lying})
SCREW = lambda pid, pos, s=3.0, ry=0, lying=True: P(pid, 'screw', pos=list(pos), ry=ry, scale=s, opts={'lying': lying})
BUBBLE = lambda pid, text, pos, pop, w=0.9: P(pid, 'speechBubble', pos=pos, opts={'text': text, 'popAt': pop, 'tail': 'down', 'w': w, 'h': w * 0.42})
HELD = lambda pid, x, z: SCREW(pid, (x - 0.09, 2.08, z + 0.6), 5.0, 0, False)    # a screw (cartoon size) pinched in a dangleItem hand, sticking up above the fist (actor at x, z facing +Z)
VEST = P('vest', 'storeVest', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0, 0]})
SHOP = [ARM(f'w{i}', x, z, ry, tag='149 €') for i, (x, z, ry) in enumerate(((-1.85, -2.02, 0), (-0.65, -2.02, 0), (0.55, -2.02, 0), (1.75, -2.02, 0), (-2.3, -0.7, 90), (2.2, -0.7, -90)))]

# 1-3: he assembled it; one screw left (a close-up on the floor, then held up to his face)
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', [0.45, 0, -1.25], -15, 'handsOnHips', 'happy')],
        props=[ARM('w0', -0.45, -2.02), BOX('fb', 0.3, -0.6, 15, True), P('ak', 'allenKey', pos=[0.95, 0.003, -0.35], rot=[1.5708, 0, 0])],
        cams=[cam(0.0, [0.3, 1.5, 2.2], [0.27, 1.48, 1.9], [0.0, 1.35, -1.6], [0.0, 1.35, -1.6], lens=44)])
st.shot('S02', 'livingRoom', setOpts=LR, actors=[act('mec', [0.2, 0, -1.4], 0, 'lookDown', 'neutral')], props=[ARM('w0', -0.45, -2.02), SCREW('s1', (0.05, 0, -0.72), 7.0, 30)],
        cams=[cam(0.0, [0.12, 0.16, -0.22], [0.1, 0.15, -0.3], [0.04, 0.06, -0.8], [0.04, 0.06, -0.8], lens=40)])
st.shot('S03', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -1.3], 0, 'dangleItem', 'suspicious')], props=[ARM('w0', -0.9, -2.02), HELD('s1', 0.0, -1.3)],
        cams=[cam(0.0, [0.1, 1.95, 0.55], [0.09, 1.95, 0.4], [-0.08, 1.85, -1.3], [-0.08, 1.85, -1.3], lens=44)])
# 4-6: he bought the same one again (carries the new box in); compares the two; two screws left
D4 = st.dur('S04')
st.shot('S04', 'livingRoom', setOpts=LR, actors=[act('mec', [1.6, 0, -0.9], -90, 'carry', 'neutral', keys=[k(0.0, to=[0.4, 0, -0.9], dur=D4 - 0.1, clip='carryBox')])],
        props=[ARM('w0', -0.45, -2.02), P('nb', 'flatBox', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, -0.45, 0.32]}, scale=0.8)],
        cams=[cam(0.0, [0.3, 1.5, 2.7], [0.25, 1.48, 2.45], [0.6, 1.35, -1.0], [0.4, 1.35, -1.0], lens=44)])
st.shot('S05', 'livingRoom', setOpts=LR, actors=[act('mec', [0.05, 0, -1.25], 0, 'scratchHead', 'suspicious')], props=[ARM('w0', -0.65, -2.02), ARM('w1', 0.75, -2.02)],
        cams=[cam(0.0, [0.1, 1.55, 2.0], [0.1, 1.53, 1.75], [0.05, 1.38, -1.6], [0.05, 1.38, -1.6], lens=44)])
st.shot('S06', 'livingRoom', setOpts=LR, props=[ARM('w0', -0.65, -2.02), ARM('w1', 0.75, -2.02), SCREW('s1', (0.0, 0, -0.68), 5.0, 95), SCREW('s2', (0.03, 0, -0.92), 5.0, 75)],
        cams=[cam(0.0, [0.05, 0.24, 0.12], [0.04, 0.23, 0.02], [0.02, 0.05, -0.8], [0.02, 0.05, -0.8], lens=40)])
# 7-8: he bought ten (boxes everywhere); twenty screws left (he sits among them)
st.shot('S07', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -0.5], 0, 'handsOnHips', 'unimpressed')],
        props=[BOX(f'b{i}', -1.9 + i * 0.42, -2.2 + (i % 2) * 0.05, (i % 3 - 1) * 4) for i in range(10)],
        cams=[cam(0.0, [0.6, 1.7, 3.2], [0.55, 1.68, 2.9], [0.0, 1.2, -1.2], [0.0, 1.2, -1.2], lens=44)])
st.shot('S08', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -1.0], 0, 'sitFloor', 'sad')],
        props=[ARM(f'w{i}', -1.2 + i * 1.2, -2.02) for i in range(3)] + [P('pile', 'screwPile', pos=[0.0, 0, -0.3], opts={'n': 20, 'r': 0.62, 'k': 4.5, 'seed': 8})],
        cams=[cam(0.0, [0.05, 2.6, 0.9], [0.05, 2.55, 0.8], [0.0, 0.3, -0.75], [0.0, 0.3, -0.75], lens=44)])
# 9-12: his flat became a furniture shop; the neighbours shop there; the shop hired him; his first customer
st.shot('S09', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -0.9], 0, 'present', 'happy')], props=SHOP,
        cams=[cam(0.0, [0.4, 1.9, 3.6], [0.35, 1.85, 3.25], [0.0, 1.2, -1.2], [0.0, 1.2, -1.2], lens=44)])
D10 = st.dur('S10')
st.shot('S10', 'livingRoom', setOpts=LR, actors=[act('voisine', [0.95, 0, -0.3], -90, 'stand', 'happy', keys=[k(0.0, to=[0.38, 0, -0.45], dur=D10, clip='walk', face='keep')]),
        act('mamie', [-0.95, 0, -0.1], 90, 'stand', 'happy', keys=[k(0.2, to=[-0.38, 0, -0.2], dur=D10 - 0.2, clip='walk', face='keep')])],
        props=SHOP + [P('bag1', 'shoppingBag', on={'actor': 'voisine', 'hand': 'R'}), P('bag2', 'shoppingBag', on={'actor': 'mamie', 'hand': 'L'})],
        cams=[cam(0.0, [0.0, 1.6, 3.5], [0.0, 1.6, 3.2], [0.0, 1.25, -0.8], [0.0, 1.25, -0.8], lens=44)])
COUNTER = P('till', 'cashCounter', pos=[0.35, 0, -0.75], opts={'w': 1.3})
st.shot('S11', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.35], 0, 'present', 'happy')], props=SHOP + [COUNTER, VEST],
        cams=[cam(0.0, [0.55, 1.75, 1.6], [0.5, 1.75, 1.35], [0.3, 1.5, -1.3], [0.3, 1.5, -1.3], lens=44)])
st.shot('S12', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.35], 0, 'giveItem', 'happy'), act('client', [0.6, 0, 0.0], 180, 'stand', 'happy')],
        props=SHOP + [COUNTER, VEST, BOX('cb', 1.25, -0.25, -25)],
        cams=[cam(0.0, [-1.0, 1.7, 1.9], [-0.92, 1.7, 1.7], [0.45, 1.4, -0.6], [0.45, 1.4, -0.6], lens=44)])
# 13-15: the next day he came back; one screw left (held up, the callback); « C'est normal. »
D13 = st.dur('S13')
st.shot('S13', 'livingRoom', setOpts=LR, actors=[act('client', [1.5, 0, 0.6], -120, 'stand', 'angry', keys=[k(0.0, to=[0.5, 0, 0.05], dur=D13 - 0.2, clip='walk')]), act('mec', [0.35, 0, -1.35], 0, 'stand', 'neutral')],
        props=SHOP + [COUNTER, VEST], cams=[cam(0.0, [-0.3, 1.7, 3.4], [-0.25, 1.7, 3.15], [0.6, 1.4, -0.3], [0.5, 1.4, -0.3], lens=44)])
st.shot('S14', 'livingRoom', setOpts=LR, actors=[act('client', [0.0, 0, -1.0], 0, 'dangleItem', 'angry')], props=SHOP + [HELD('s9', 0.0, -1.0)],
        cams=[cam(0.0, [0.1, 1.95, 0.85], [0.09, 1.95, 0.7], [-0.08, 1.85, -1.0], [-0.08, 1.85, -1.0], lens=44)])
T15 = st.at('S15', 'L13', 5)   # « normal »
st.shot('S15', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.35], 0, 'stand', 'unimpressed')], props=SHOP + [COUNTER, VEST, BUBBLE('cn', "C'EST NORMAL.", [0.32, 2.45, -1.15], T15 - 0.15, 0.55)],
        cams=[cam(0.0, [0.4, 2.0, 0.55], [0.39, 2.0, 0.4], [0.32, 1.85, -1.35], [0.32, 1.85, -1.35], lens=44)])
st.card('S03', 'UNE VIS'); st.card('S09', 'MAGASIN'); st.card('S14', 'UNE VIS')
st.cue('sfx:tick', 'S02', 0.15, 0.3); st.cue('sfx:clink', 'S02', 0.3, 0.3); st.cue('sfx:clink', 'S06', 0.2, 0.3); st.cue('thud', 'S07', 0.2, 0.35); st.cue('sfx:clink', 'S08', 0.25, 0.3)
st.cue('sfx:cash', 'S12', 0.4, 0.35); st.cue('sfx:step', 'S13', 0.2, 0.3); st.cue('pop', 'S15', T15 - 0.15, 0.4)
st.write("L'armoire", {'voisine': {'preset': 'madame', 'seed': 71}, 'mamie': {'preset': 'mamie', 'seed': 72}, 'client': {'preset': 'fringant', 'seed': 73}})
