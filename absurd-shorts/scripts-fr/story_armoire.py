#!/usr/bin/env python3
"""L'armoire (story 30): this man assembled a flat-pack wardrobe. At the end, one screw was left. He bought the same wardrobe again to
find out where it went: two screws left. He bought ten: twenty screws left. His flat became a furniture shop; the neighbours came to do
their shopping; the shop hired him. His first customer bought a wardrobe. The next day he came back: one screw left. The man said:
« C'est normal. »

Round 2 (critics 7.2 / 7.5): teal wardrobes that stand off the cream wall, big price cards; sand3d screws (CC BY 4.0) in the close-ups;
a fast push-in on the hook with the « ARMOIRE » box face-on; the second box carried face-on; a real top view of the twenty screws, clear
of the caption band; a scale reveal of the shop (aisles, « MEUBLES » sign); the neighbours outside under the sky; a hiring contract pops
in; a 3/4 sale with the box on the counter; the customer storms back toward the camera; the punchline bubble fully in frame."""
import random
from story_kit import *

st = Story('armoire')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 3), ('S04', 'L03', 0), ('S05', 'L03', 6)] + [(f'S{i + 2:02d}', f'L{i:02d}', 0) for i in range(4, 14)])
PI = math.pi
LR = {'sofa': False, 'tv': False}
ARM = lambda pid, x, z=-2.02, ry=0, tag=None: P(pid, 'armoire', pos=[x, 0, z], ry=ry, opts={'tag': tag} if tag else {})
BOX = lambda pid, x, z, ry=0, lying=False, s=1.0, y=0.0: P(pid, 'flatBox', pos=[x, y, z], ry=ry, scale=s, opts={'lying': lying})
SCREW_GLB = '/assets/models/screw-objaverse-21338/model.glb'   # sand3d (objaverse row 21338), CC BY 4.0: credits in stories7/armoire/credits.txt
SCREW = lambda pid, pos, size=0.3, ry=0, lying=True: P(pid, 'glbModel', pos=list(pos), ry=ry, opts={'src': SCREW_GLB, 'size': size, 'outline': 0.002, 'lay': lying, 'up': not lying, 'thick': 2.4})   # fattened for a phone screen
BUBBLE = lambda pid, text, pos, pop, w=0.9, tail='down': P(pid, 'speechBubble', pos=pos, opts={'text': text, 'popAt': pop, 'tail': tail, 'w': w, 'h': w * 0.42})
HELD = lambda pid, x, z: SCREW(pid, (x - 0.09, 1.93, z + 0.6), 0.24, 0, False)    # a screw pinched in a dangleItem hand, sticking up above the fist (actor at x, z facing +Z)
VEST = P('vest', 'storeVest', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0, 0]})
ROW = lambda z, tag='149 €', pre='w': [ARM(f'{pre}{i}{int(z * 10)}', x, z, 0, tag) for i, x in enumerate((-1.8, -0.6, 0.6, 1.8))]
SHOP = ROW(-2.02) + [ARM('ws1', -2.3, -0.7, 90, '149 €'), ARM('ws2', 2.2, -0.7, -90, '149 €')]
COUNTER = P('till', 'cashCounter', pos=[0.35, 0, -0.75], opts={'w': 1.3})
rnd = random.Random(30)
PILE = [SCREW(f'p{i}', (rnd.uniform(-0.6, 0.6), 0, rnd.uniform(-0.98, -0.5)), 0.26, rnd.uniform(0, 360)) for i in range(20)]

# 1-3: he assembled it (a fast push-in, the empty box face-on); one screw left (close-up on the floor, then held up to his face)
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', [0.3, 0, -1.25], -15, 'handsOnHips', 'happy')],
        props=[ARM('w0', -0.55, -2.02), BOX('fb', 0.85, -2.2, -8), P('ak', 'allenKey', pos=[0.95, 0.003, -0.35], rot=[1.5708, 0, 0])],
        cams=[cam(0.0, [0.35, 1.4, 3.1], [0.3, 1.45, 1.55], [0.15, 1.3, -1.6], [0.15, 1.33, -1.6], lens=44, ease='out')])
st.shot('S02', 'livingRoom', setOpts=LR, actors=[act('mec', [0.2, 0, -1.4], 0, 'lookDown', 'neutral')], props=[ARM('w0', -0.45, -2.02), SCREW('s1', (0.03, 0, -0.72), 0.3, 60)],
        cams=[cam(0.0, [0.12, 0.16, -0.22], [0.1, 0.15, -0.3], [0.04, 0.06, -0.8], [0.04, 0.06, -0.8], lens=40)])
st.shot('S03', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -1.3], 0, 'dangleItem', 'suspicious')], props=[ARM('w0', -0.9, -2.02), HELD('s1', 0.0, -1.3)],
        cams=[cam(0.0, [0.1, 1.95, 0.55], [0.09, 1.95, 0.4], [-0.08, 1.85, -1.3], [-0.08, 1.85, -1.3], lens=44)])
# 4-6: he bought the same one again (carries the box face-on); compares the two; two screws left
D4 = st.dur('S04')
st.shot('S04', 'livingRoom', setOpts=LR, actors=[act('mec', [1.6, 0, -0.9], -90, 'walk', 'neutral', keys=[k(0.0, to=[0.45, 0, -0.9], dur=D4 - 0.1, clip='walk')])],
        props=[ARM('w0', -0.55, -2.02), P('nb', 'flatBox', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.3, -0.72, 0.0], 'rot': [0, 1.5708, 0]}, scale=0.65)],
        cams=[cam(0.0, [0.65, 1.5, 2.9], [0.6, 1.48, 2.65], [0.85, 1.3, -1.0], [0.65, 1.3, -1.0], lens=44)])
st.shot('S05', 'livingRoom', setOpts=LR, actors=[act('mec', [0.05, 0, -1.25], 0, 'scratchHead', 'suspicious')], props=[ARM('w0', -0.65, -2.02), ARM('w1', 0.75, -2.02)],
        cams=[cam(0.0, [0.1, 1.55, 2.0], [0.1, 1.53, 1.75], [0.05, 1.38, -1.6], [0.05, 1.38, -1.6], lens=44)])
st.shot('S06', 'livingRoom', setOpts=LR, props=[ARM('w0', -0.65, -2.02), ARM('w1', 0.75, -2.02), SCREW('s1', (0.0, 0, -0.68), 0.26, 6), SCREW('s2', (0.04, 0, -0.92), 0.26, -14)],
        cams=[cam(0.0, [0.05, 0.24, 0.12], [0.04, 0.23, 0.02], [0.02, 0.05, -0.8], [0.02, 0.05, -0.8], lens=40)])
# 7-8: he bought ten (boxes everywhere); twenty screws left (a top view: he sits behind them, the screws clear of the caption band)
st.shot('S07', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -0.5], 0, 'handsOnHips', 'unimpressed')],
        props=[BOX(f'b{i}', -1.9 + i * 0.42, -2.2 + (i % 2) * 0.05, (i % 3 - 1) * 4) for i in range(10)],
        cams=[cam(0.0, [0.6, 1.7, 3.2], [0.55, 1.68, 2.9], [0.0, 1.2, -1.2], [0.0, 1.2, -1.2], lens=44)])
st.shot('S08', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -1.3], 0, 'sitFloor', 'sad')], props=[ARM(f'w{i}', -1.2 + i * 1.2, -2.02) for i in range(3)] + PILE,
        cams=[cam(0.0, [0.0, 3.5, 0.55], [0.0, 3.45, 0.45], [0.0, 0.2, -0.95], [0.0, 0.2, -0.95], lens=44)])
# 9-12: his flat became a furniture shop (a scale reveal); the neighbours shop there (outside, under the sky); the shop hired him (a contract
# pops in); his first customer (a 3/4 two-shot, the box on the counter)
st.shot('S09', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, 0.9], 0, 'present', 'happy')],
        props=ROW(-2.02) + ROW(-0.9, pre='m') + [P('sign', 'noticeBoard', pos=[0.0, 2.25, -2.32], opts={'text': 'MEUBLES', 'style': 'sign', 'w': 1.5, 'h': 0.38, 'bg': '#F2C94C', 'fg': '#1C252A', 'frame': '#1C252A'})],
        cams=[cam(0.0, [0.5, 3.3, 4.4], [0.45, 3.25, 4.0], [0.0, 0.9, -0.9], [0.0, 0.9, -0.9], lens=44)])
D10 = st.dur('S10')
st.shot('S10', 'parisStreet', actors=[act('voisine', [0.55, 0, -2.4], 0, 'stand', 'happy', keys=[k(0.0, to=[0.5, 0, -0.9], dur=D10, clip='walk')]),
        act('mamie', [-0.45, 0, -2.0], 0, 'stand', 'happy', keys=[k(0.15, to=[-0.4, 0, -0.75], dur=D10 - 0.15, clip='walk')])],
        props=[P('bag1', 'shoppingBag', on={'actor': 'voisine', 'hand': 'R'}), P('mb', 'flatBox', on={'actor': 'mamie', 'joint': 'torso', 'offset': [-0.3, -0.72, 0.0], 'rot': [0, -1.5708, 0]}, scale=0.55),
               P('shop', 'signBoard', pos=[1.0, 0, -2.4], opts={'text': 'MEUBLES 2E ÉTAGE', 'w': 0.9, 'h': 0.5, 'height': 1.3, 'bg': '#F2C94C', 'fg': '#1C252A', 'frame': '#1C252A'})],
        cams=[cam(0.0, [0.4, 1.55, 2.8], [0.38, 1.55, 2.55], [0.1, 1.45, -1.5], [0.1, 1.45, -1.5], lens=44)])
T11 = st.at('S11', 'L09', 3) - 0.1   # « embauché »
st.shot('S11', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.35], 0, 'present', 'happy')],
        props=SHOP + [COUNTER, VEST, P('contract', 'noticeBoard', pos=[0.02, 1.62, -0.5], ry=8, opts={'text': "CONTRAT\nD'EMBAUCHE\n✔ LE MEC", 'style': 'doc', 'w': 0.5, 'h': 0.64, 'popAt': T11})],
        cams=[cam(0.0, [0.4, 1.75, 1.55], [0.37, 1.75, 1.3], [0.12, 1.5, -1.3], [0.12, 1.5, -1.3], lens=44)])
st.shot('S12', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.35], 0, 'giveItem', 'happy'), act('client', [1.05, 0, -0.45], -66, 'stand', 'happy')],
        props=SHOP + [COUNTER, VEST, BOX('cb', 0.55, -0.8, 90, True, 0.5, 0.99)],
        cams=[cam(0.0, [0.75, 1.85, 2.1], [0.72, 1.83, 1.9], [0.75, 1.35, -0.8], [0.75, 1.35, -0.8], lens=44)])
# 13-15: the next day he came back (storming toward the camera); one screw left (held up, the callback); « C'est normal. »
D13 = st.dur('S13')
st.shot('S13', 'livingRoom', setOpts=LR, actors=[act('client', [-1.15, 0, -1.7], 0, 'stand', 'angry', keys=[k(0.0, to=[-0.95, 0, 0.15], dur=D13 - 0.15, clip='walk')])],
        props=SHOP + [COUNTER, VEST], cams=[cam(0.0, [-0.75, 1.7, 2.7], [-0.77, 1.68, 2.45], [-0.95, 1.45, -0.7], [-0.95, 1.45, -0.7], lens=44)])
st.shot('S14', 'livingRoom', setOpts=LR, actors=[act('client', [0.0, 0, -1.0], 0, 'dangleItem', 'angry')], props=SHOP + [HELD('s9', 0.0, -1.0)],
        cams=[cam(0.0, [0.1, 2.05, 0.85], [0.09, 2.05, 0.7], [-0.08, 1.96, -1.0], [-0.08, 1.96, -1.0], lens=44)])
T15 = st.at('S15', 'L13', 5)   # « normal »
st.shot('S15', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.35], 0, 'stand', 'unimpressed')], props=SHOP + [COUNTER, VEST, BUBBLE('cn', "C'EST NORMAL.", [0.15, 2.42, -1.2], T15 - 0.15, 0.5)],
        cams=[cam(0.0, [0.4, 2.05, 0.55], [0.39, 2.05, 0.4], [0.3, 1.95, -1.35], [0.3, 1.95, -1.35], lens=44)])
st.card('S03', 'UNE VIS'); st.card('S09', 'MAGASIN'); st.card('S14', 'UNE VIS')
st.cue('sfx:tick', 'S02', 0.15, 0.3); st.cue('sfx:clink', 'S02', 0.3, 0.3); st.cue('sfx:clink', 'S06', 0.2, 0.3); st.cue('thud', 'S07', 0.2, 0.35); st.cue('sfx:clink', 'S08', 0.25, 0.3)
st.cue('sfx:paper', 'S11', T11, 0.35); st.cue('sfx:cash', 'S12', 0.4, 0.35); st.cue('sfx:step', 'S13', 0.2, 0.3); st.cue('pop', 'S15', T15 - 0.15, 0.4)
st.write("L'armoire", {'voisine': {'preset': 'madame', 'seed': 71}, 'mamie': {'preset': 'mamie', 'seed': 72}, 'client': {'preset': 'fringant', 'seed': 73}})
