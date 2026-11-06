#!/usr/bin/env python3
"""Le parapluie (story 31): this man ordered an umbrella online. He received the rain: a little cloud, in a box. The cloud followed him
everywhere: to the office, to the bus stop, to the cinema in the middle of the film, to his sister's wedding. He tried to send it back:
the post office was flooded; the postman left by boat. So he kept it. Today he no longer pays for water."""
from story_kit import *

st = Story('parapluie')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 14)])
PI = math.pi
LR = {'sofa': False, 'tv': False}
CLOUD = lambda pos, h=2.55, size=0.75, mood='happy', rain=True, puddle=True, keys=None, pid='cloud': P(pid, 'rainCloud', pos=list(pos), opts={'h': h, 'size': size, 'mood': mood, 'rain': rain, 'puddle': puddle}, **({'keys': keys} if keys else {}))
BOAT = '/assets/models/rowboat-objaverse-19091/model.glb'   # sand3d (objaverse row 19091), CC BY 4.0: credits in stories7/parapluie/credits.txt

# 1-3: he orders an umbrella on his phone; he receives the rain (the cloud rises out of the box); a little cloud in a box
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -1.3], 0, 'showPhone', 'happy')], props=[P('phone', 'shopPhone', pos=[-0.12, 1.66, -0.62], scale=2.2)],
        cams=[cam(0.0, [0.1, 1.85, 0.75], [0.09, 1.84, 0.55], [-0.04, 1.72, -1.3], [-0.04, 1.72, -1.3], lens=44)])
D2 = st.dur('S02')
st.shot('S02', 'livingRoom', setOpts=LR, actors=[act('mec', [0.45, 0, -1.55], -20, 'stand', 'shocked')],
        props=[P('box', 'cardboardBox', pos=[-0.15, 0, -1.05], opts={'text': ''}), CLOUD((-0.15, 0, -1.05), 0.55, 0.6, 'happy', True, False, keys=[k(0.15, scale=1.0, dur=0.01)])],
        cams=[cam(0.0, [0.25, 1.55, 1.9], [0.22, 1.53, 1.65], [0.1, 1.28, -1.3], [0.1, 1.3, -1.3], lens=44)])
st.shot('S03', 'livingRoom', setOpts=LR, props=[P('box', 'cardboardBox', pos=[0.0, 0, -1.0], opts={'text': ''}), CLOUD((0.0, 0, -1.0), 0.95, 0.55, 'happy', True, False)],
        cams=[cam(0.0, [0.12, 0.75, 0.0], [0.11, 0.74, -0.1], [0.0, 0.72, -1.0], [0.0, 0.74, -1.0], lens=44)])
# 4-8: it followed him everywhere: the street, the office, the bus stop, the cinema, his sister's wedding
D4 = st.dur('S04')
st.shot('S04', 'parisStreet', actors=[act('mec', [0.1, 0, -2.6], 0, 'stand', 'unimpressed', keys=[k(0.0, to=[0.15, 0, -1.0], dur=D4, clip='walk')]),
        act('passante', [-0.9, 0, -0.6], 15, 'stand', 'surprised')],
        props=[CLOUD((0.1, 0, -2.6), keys=[k(0.0, to=[0.15, 0, -1.0], dur=D4)])],
        cams=[cam(0.0, [0.35, 1.6, 2.6], [0.33, 1.6, 2.35], [0.1, 1.55, -1.6], [0.1, 1.55, -1.6], lens=44)])
st.shot('S05', 'office', setOpts={'door': False}, actors=[act('mec', [0.0, 0, -1.95], 0, 'sitWrite', 'unimpressed'), act('collegue', [1.3, 0, -2.4], -25, 'stand', 'surprised')],
        props=[P('desk', 'desk', pos=[0, 0, -1.4]), P('chair', 'chair', pos=[0, 0, -1.95], opts={'color': '#3A3D44'}), CLOUD((0.0, 0, -1.85), 2.3, 0.7)],
        cams=[cam(0.0, [0.3, 1.75, 1.2], [0.28, 1.73, 0.95], [0.1, 1.35, -1.8], [0.1, 1.35, -1.8], lens=44)])
st.shot('S06', 'parisStreet', actors=[act('mec', [0.85, 0, -1.4], -15, 'stand', 'unimpressed'), act('passante', [-0.35, 0, -1.75], 10, 'stand', 'happy'), act('collegue', [-0.95, 0, -1.6], 20, 'readPhone', 'neutral')],
        props=[P('stop', 'busStop', pos=[-0.6, 0, -2.0]), CLOUD((0.85, 0, -1.4))],
        cams=[cam(0.0, [0.45, 1.6, 2.9], [0.43, 1.6, 2.65], [0.3, 1.5, -1.6], [0.3, 1.5, -1.6], lens=44)])
st.shot('S07', 'cinema', actors=[act('mec', [0.0, 0.0, -3.4], 180, 'sit', 'unimpressed'), act('passante', [-1.1, 0.0, -3.4], 180, 'sit', 'shocked'), act('collegue', [1.1, 0.0, -3.4], 180, 'sit', 'surprised')],
        props=[CLOUD((0.0, 0, -3.35), 2.05, 0.6)],
        cams=[cam(0.0, [0.15, 1.5, -6.9], [0.14, 1.5, -6.7], [0.0, 1.3, -3.4], [0.0, 1.3, -3.4], lens=44)])
st.shot('S08', 'church', actors=[act('soeur', [-0.35, 0.22, -1.2], 15, 'stand', 'shocked'), act('marie', [0.4, 0.22, -1.25], -15, 'stand', 'surprised'), act('mec', [0.9, 0.0, -0.2], -35, 'stand', 'unimpressed')],
        props=[P('veil', 'veil', on={'actor': 'soeur', 'joint': 'head', 'offset': [0, 0.42, 0]}), CLOUD((-0.35, 0.22, -1.2), 2.5, 0.7, 'smug')],
        cams=[cam(0.0, [0.6, 1.85, 3.3], [0.58, 1.85, 3.05], [0.45, 1.6, -0.9], [0.45, 1.6, -0.9], lens=44)])
# 9-11: he tried to send it back (the post office); flooded; the postman left by boat
st.shot('S09', 'poste', actors=[act('mec', [0.0, 0, -1.65], 180, 'giveItem', 'neutral'), act('guichet', [0.0, 0, -2.85], 0, 'stand', 'suspicious')],
        props=[P('parcel', 'cardboardBox', pos=[0.0, 1.0, -2.3], scale=0.6, opts={'text': ''}), CLOUD((0.0, 1.0, -2.3), 0.75, 0.45, 'smug', True, False)],
        cams=[cam(0.0, [1.4, 1.75, -0.2], [1.3, 1.74, -0.4], [0.0, 1.45, -2.3], [0.0, 1.45, -2.3], lens=44)])
D10 = st.dur('S10')
st.shot('S10', 'poste', actors=[act('guichet', [0.0, 0, -2.85], 0, 'scared', 'shocked')],
        props=[CLOUD((0.4, 0, -2.0), 2.7, 0.9, 'happy'), P('flood', 'floodWater', pos=[0, 0, -1.0], opts={'w': 12, 'd': 10, 'y0': 0.2, 'y1': 1.15, 't0': 0.0, 't1': D10}),
               P('pb', 'cardboardBox', pos=[-0.9, 0.9, -1.4], scale=0.45, opts={'text': ''}, keys=[k(0.0, to=[-0.6, 1.12, -1.2], dur=D10)])],
        cams=[cam(0.0, [0.6, 1.9, 1.6], [0.55, 1.88, 1.35], [0.1, 1.45, -2.2], [0.1, 1.45, -2.2], lens=44)])
D11 = st.dur('S11')
st.shot('S11', 'parisStreet', actors=[act('facteur', [0.0, 0.19, -2.0], -45, 'sitWave', 'happy', keys=[k(0.0, to=[1.0, 0.19, -3.0], dur=D11, glide=True, face='keep')])],   # seated on the middle bench, facing the stern, waving goodbye as the boat drifts off
        props=[P('flood', 'floodWater', pos=[0, 0, -2.0], opts={'w': 14, 'd': 30, 'y0': 0.55, 'y1': 0.55}),
               P('boat', 'glbModel', pos=[0.0, 0.42, -2.0], ry=45, opts={'src': BOAT, 'size': 2.2, 'outline': 0.012, 'lay': True}, keys=[k(0.0, to=[1.0, 0.42, -3.0], dur=D11)]),
               *[P(f'pk{i}', 'cardboardBox', pos=[0.42 + dx, 0.62 + dy, -2.42 + dz], ry=45 + 12 * i, scale=0.3, opts={'text': ''}, keys=[k(0.0, to=[1.42 + dx, 0.62 + dy, -3.42 + dz], dur=D11)]) for i, (dx, dy, dz) in enumerate([(0, 0, 0), (0.1, 0, 0.12), (0.04, 0.16, 0.05)])]],   # parcels stacked at the bow
        cams=[cam(0.0, [0.55, 1.7, 1.7], [0.6, 1.68, 1.45], [0.4, 1.1, -2.4], [0.6, 1.05, -2.7], lens=44)])
# 12-13: so he kept it (on the sofa with his cloud); today he no longer pays for water (it fills his bath; the water bill pops in)
st.shot('S12', 'livingRoom', setOpts={'sofa': True, 'tv': False}, actors=[act('mec', [0.3, 0, -1.5], 0, 'present', 'happy')], props=[CLOUD((-0.35, 0, -1.4), 1.9, 0.7, 'happy', True, True), P('plant', 'plant', pos=[-0.35, 0, -1.4], scale=0.9)],
        cams=[cam(0.0, [0.1, 1.6, 1.5], [0.1, 1.58, 1.25], [0.0, 1.35, -1.5], [0.0, 1.35, -1.5], lens=44)])
T13 = st.at('S13', 'L13', 5) - 0.1   # « l'eau »
st.shot('S13', 'bathroom', actors=[act('mec', [-2.85, 0.19, -2.95], 70, 'sitFloor', 'grin')],   # sitting in the bath under his own rain, facing the camera at 3/4
        props=[CLOUD((-2.8, 0, -2.95), 2.3, 0.7, 'happy', True, False), P('bill', 'noticeBoard', pos=[-2.3, 1.8, -3.33], ry=0, opts={'text': "FACTURE D'EAU\n0,00 €", 'style': 'doc', 'w': 0.46, 'h': 0.4, 'popAt': T13})],
        cams=[cam(0.0, [-1.2, 1.62, -0.3], [-1.25, 1.6, -0.5], [-2.5, 1.45, -3.0], [-2.5, 1.45, -3.0], lens=44)])
st.card('S02', 'LA PLUIE'); st.card('S10', 'INONDÉE')
st.cue('sfx:paper', 'S02', 0.1, 0.3); st.cue('pop', 'S02', 0.2, 0.4); st.cue('sfx:splash', 'S03', 0.3, 0.25); st.cue('sfx:step', 'S04', 0.2, 0.25); st.cue('sfx:gasp', 'S08', 0.3, 0.3)
st.cue('sfx:splash', 'S10', 0.3, 0.4); st.cue('sfx:splash', 'S11', 0.4, 0.3); st.cue('sfx:paper', 'S13', T13, 0.3)
st.write('Le parapluie', {'passante': {'preset': 'madame', 'seed': 91}, 'collegue': {'preset': 'boss', 'seed': 92}, 'soeur': {'preset': 'madame', 'seed': 93, 'suit': '#F7F5F0', 'lapel': '#FFFFFF'},
                          'marie': {'preset': 'politique', 'seed': 94}, 'guichet': {'preset': 'serveur', 'seed': 95}, 'facteur': {'preset': 'cop', 'seed': 96, 'suit': '#2F62B5', 'hatColor': '#F2C94C'}})
