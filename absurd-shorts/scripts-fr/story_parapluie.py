#!/usr/bin/env python3
"""Le parapluie (story 31): this man ordered an umbrella online. He received the rain: a little cloud, in a box. The cloud followed him
everywhere: to the office, to the bus stop, to the cinema in the middle of the film, to his sister's wedding. He tried to send it back:
the post office was flooded; the postman left by boat. So he kept it. Today he no longer pays for water."""
from story_kit import *

st = Story('parapluie')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 14)])
PI = math.pi
LR = {'sofa': False, 'tv': False}
CLOUD = lambda pos, h=2.55, size=0.75, mood='happy', rain=True, puddle=True, keys=None, pid='cloud', ry=0: P(pid, 'rainCloud', pos=list(pos), ry=ry, opts={'h': h, 'size': size, 'mood': mood, 'rain': rain, 'puddle': puddle}, **({'keys': keys} if keys else {}))
BOAT = '/assets/models/rowboat-objaverse-19091/model.glb'   # sand3d (objaverse row 19091), CC BY 4.0: credits in stories7/parapluie/credits.txt

# 1-3: he orders an umbrella on his phone (his thumb taps COMMANDER); he receives the rain (the cloud pops up out of the box: double take); a little cloud in a box
T1 = st.at('S01', 'L01', 3)   # « commandé »
TP = st.at('S01', 'L01', 6) - 0.05   # « sur internet »: punch in
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', [0.0, 0, -1.3], 0, 'showPhone', 'smirk', keys=[k(T1 + 0.1, expr='proud')])],
        props=[P('phone', 'shopPhone', pos=[-0.12, 1.66, -0.62], scale=2.2, opts={'tapAt': T1})],
        cams=[cam(0.0, [0.1, 1.85, 0.75], [0.09, 1.84, 0.6], [-0.04, 1.72, -1.3], [-0.04, 1.72, -1.3], lens=44), cam(TP, [0.06, 1.86, 0.35], [0.05, 1.86, 0.25], [-0.06, 1.8, -1.3], [-0.06, 1.8, -1.3], lens=44)])
TR = st.at('S02', 'L02', 3)   # « la pluie »: the cloud pops up
st.shot('S02', 'livingRoom', setOpts=LR, actors=[act('mec', [0.55, 0, -1.6], -25, 'stand', 'neutral', keys=[k(0.0, look=[-0.2, 0.4, -1.05]), k(TR + 0.08, clip='startle', expr='shocked', to=[0.85, 0, -1.8], dur=0.28, face='keep', look=[-0.2, 1.1, -1.05])])],
        props=[P('box', 'cardboardBox', pos=[-0.2, 0, -1.05], opts={'text': ''}), CLOUD((-0.2, -0.45, -1.05), 0.6, 0.62, 'happy', True, False, keys=[k(TR, to=[-0.2, 0.45, -1.05], dur=0.42, ease='outBack')])],
        cams=[cam(0.0, [0.3, 1.3, 2.9], [0.29, 1.3, 2.7], [0.2, 1.25, -1.3], [0.2, 1.27, -1.3], lens=44)])
st.shot('S03', 'livingRoom', setOpts=LR, props=[P('box', 'cardboardBox', pos=[0.0, 0, -1.0], opts={'text': ''}), CLOUD((0.0, 0, -1.0), 0.95, 0.55, 'happy', True, False)],
        cams=[cam(0.0, [0.12, 0.75, 0.0], [0.11, 0.74, -0.1], [0.0, 0.72, -1.0], [0.0, 0.74, -1.0], lens=44)])
# 4-8: it followed him everywhere: the street (a passer-by dry under her red umbrella), the office (a colleague staring), the bus stop, the cinema (the row turns round), the wedding (it rains on the bride)
D4 = st.dur('S04')
st.shot('S04', 'parisStreet', actors=[act('mec', [1.4, 0, -2.6], 0, 'stand', 'unimpressed', fx={'wet': True}, keys=[k(0.0, to=[1.42, 0, -1.0], dur=D4, clip='walk')]),
        act('passante', [0.5, 0, -0.4], 20, 'readPhone', 'smirk', keys=[k(0.0, look=[1.4, 1.9, -1.8])])],
        props=[CLOUD((1.4, 0, -2.6), keys=[k(0.0, to=[1.42, 0, -1.0], dur=D4)]), P('umb', 'umbrella', pos=[0.56, 1.0, -0.15], opts={'radius': 0.55, 'height': 1.05})],
        cams=[cam(0.0, [1.05, 1.6, 2.6], [1.03, 1.6, 2.35], [0.9, 1.55, -1.6], [0.9, 1.55, -1.6], lens=44)])
st.shot('S05', 'office', setOpts={'door': False}, actors=[act('mec', [0.0, 0, -1.95], 0, 'sitWrite', 'squint', fx={'wet': True}), act('collegue', [-0.45, 0, -2.75], 25, 'scared', 'shocked', keys=[k(0.0, look=[0.0, 2.3, -1.85])])],
        props=[P('desk', 'desk', pos=[0, 0, -1.4]), P('chair', 'chair', pos=[0, 0, -1.95], opts={'color': '#3A3D44'}), CLOUD((0.0, 0, -1.85), 2.3, 0.7)],
        cams=[cam(0.0, [0.25, 1.85, 1.6], [0.23, 1.83, 1.35], [0.05, 1.55, -1.8], [0.05, 1.55, -1.8], lens=44)])
st.shot('S06', 'parisStreet', actors=[act('mec', [0.85, 0, -1.4], -15, 'stand', 'unimpressed', fx={'wet': True}), act('passante', [-0.35, 0, -1.75], 10, 'stand', 'whistle'), act('collegue', [-0.95, 0, -1.6], 20, 'readPhone', 'neutral')],
        props=[P('stop', 'busStop', pos=[-0.6, 0, -2.0]), CLOUD((0.85, 0, -1.4))],
        cams=[cam(0.0, [0.45, 1.6, 2.9], [0.43, 1.6, 2.65], [0.3, 1.5, -1.6], [0.3, 1.5, -1.6], lens=44)])
HEAD7 = [1.4, 1.55, -4.65]
st.shot('S07', 'cinema', actors=[act('mec', [1.4, 0.0, -4.65], 180, 'sit', 'unimpressed', fx={'wet': True}), act('passante', [0.8, 0.0, -4.65], 180, 'sit', 'disgusted', keys=[k(0.0, look=HEAD7)]),
        act('collegue', [2.0, 0.0, -4.65], 180, 'sit', 'rage', keys=[k(0.0, look=HEAD7)]), act('spect1', [0.8, 0.0, -3.4], 180, 'sit', 'eyeRoll', keys=[k(0.0, look=HEAD7)]), act('spect2', [2.0, 0.0, -3.4], 180, 'sit', 'awe', keys=[k(0.0, look=HEAD7)])],
        props=[CLOUD((1.4, 0, -4.65), 2.05, 0.6, ry=180), P('screenlight', 'flickerLight', pos=[1.4, 2.6, -7.2], opts={'color': '#CFE0FF', 'intensity': 14, 'distance': 9})],
        cams=[cam(0.0, [1.45, 1.55, -7.75], [1.44, 1.55, -7.55], [1.4, 1.4, -4.4], [1.4, 1.4, -4.4], lens=44)])
st.shot('S08', 'church', actors=[act('soeur', [0.0, 0.22, -1.25], 0, 'stand', 'cry', fx={'wet': True, 'tears': True}), act('marie', [0.55, 0.22, -1.95], -10, 'stand', 'shocked'), act('mec', [-0.42, 0.0, 0.05], 30, 'stand', 'whistle')],
        props=[P('veil', 'brideVeil', on={'actor': 'soeur', 'joint': 'head', 'offset': [0, 0.42, 0]}), CLOUD((0.0, 0.22, -1.25), 2.4, 0.7, 'smug')],
        cams=[cam(0.0, [0.05, 1.85, 3.4], [0.04, 1.85, 3.15], [0.0, 1.75, -1.0], [0.0, 1.75, -1.0], lens=44)])
# 9-11: he tried to send it back (the post office); flooded (water to the clerk's chest, parcels and letters afloat); the postman left by boat
st.shot('S09', 'poste', setOpts={'guichets': False}, actors=[act('mec', [0.0, 0, -1.65], 180, 'giveItem', 'puppy'), act('guichet', [0.0, 0, -2.85], 0, 'stand', 'disgusted')],
        props=[P('parcel', 'cardboardBox', pos=[0.0, 1.0, -2.3], scale=0.6, opts={'text': ''}), CLOUD((0.0, 1.0, -2.3), 0.75, 0.45, 'smug', True, False)],
        cams=[cam(0.0, [1.45, 1.85, 0.0], [1.35, 1.84, -0.2], [0.0, 1.62, -2.3], [0.0, 1.62, -2.3], lens=44)])
D10 = st.dur('S10')
FLOAT10 = [{'kind': 'parcel', 'x': -0.9, 'z': -0.4, 'ry': 0.4}, {'kind': 'parcel', 'x': 0.95, 'z': 0.1, 'ry': -0.3, 's': 0.8}, {'kind': 'parcel', 'x': -0.35, 'z': 0.5, 'ry': 1.1, 's': 0.7},
           {'kind': 'letter', 'x': 0.45, 'z': 0.55, 'ry': 0.3}, {'kind': 'letter', 'x': -0.6, 'z': 0.05, 'ry': -0.6}, {'kind': 'letter', 'x': 0.1, 'z': -0.25, 'ry': 1.2}, {'kind': 'letter', 'x': 0.8, 'z': -0.6, 'ry': 0.9},
           {'kind': 'stool', 'x': 1.15, 'z': -0.85, 'ry': 0.5, 'tilt': 0.35}]
st.shot('S10', 'poste', setOpts={'guichets': False}, actors=[act('guichet', [0.0, 0, -2.85], 0, 'scared', 'sob', fx={'wet': True})],
        props=[CLOUD((0.35, 0, -2.0), 2.4, 0.85, 'happy'), P('flood', 'floodWater', pos=[0, 0, -1.0], opts={'w': 12, 'd': 10, 'y0': 0.3, 'y1': 1.42, 't0': 0.0, 't1': D10 * 0.9,
               'ripples': [[0.35, -1.0], [0.2, -0.85], [0.5, -1.15]], 'floaters': FLOAT10})],
        cams=[cam(0.0, [0.55, 1.75, 2.6], [0.5, 1.74, 2.35], [0.15, 1.65, -2.2], [0.15, 1.65, -2.2], lens=44)])
D11 = st.dur('S11')
st.shot('S11', 'parisStreet', actors=[act('facteur', [0.0, 0.19, -2.0], -45, 'sitWave', 'bigGrin', keys=[k(0.0, to=[1.0, 0.19, -3.0], dur=D11, glide=True, face='keep')])],   # seated on the middle bench, facing the stern, waving goodbye as the boat drifts off
        props=[P('flood', 'floodWater', pos=[0, 0, -2.0], opts={'w': 14, 'd': 30, 'y0': 0.55, 'y1': 0.55}),
               P('boat', 'glbModel', pos=[0.0, 0.42, -2.0], ry=45, opts={'src': BOAT, 'size': 2.2, 'outline': 0.012, 'lay': True}, keys=[k(0.0, to=[1.0, 0.42, -3.0], dur=D11)]),
               *[P(f'pk{i}', 'cardboardBox', pos=[0.42 + dx, 0.62 + dy, -2.42 + dz], ry=45 + 12 * i, scale=0.3, opts={'text': ''}, keys=[k(0.0, to=[1.42 + dx, 0.62 + dy, -3.42 + dz], dur=D11)]) for i, (dx, dy, dz) in enumerate([(0, 0, 0), (0.1, 0, 0.12), (0.04, 0.16, 0.05)])]],   # parcels stacked at the bow
        cams=[cam(0.0, [0.55, 1.7, 1.7], [0.6, 1.68, 1.45], [0.4, 1.1, -2.4], [0.6, 1.05, -2.7], lens=44)])
# 12-13: so he kept it (it waters his plant, on a plant stand); today he no longer pays for water (he bathes under it; a big « 0,00 € » bill pops in on « l'eau », the camera pushes in)
st.shot('S12', 'livingRoom', setOpts={'sofa': True, 'tv': False}, actors=[act('mec', [0.35, 0, -1.55], -10, 'present', 'proud')],
        props=[P('stand', 'table', pos=[-0.45, 0, -1.4], opts={'w': 0.55, 'd': 0.5, 'h': 0.95}), P('plant', 'plant', pos=[-0.45, 0.95, -1.4], scale=0.7), CLOUD((-0.45, 0.95, -1.4), 1.35, 0.65, 'happy', True, False)],
        cams=[cam(0.0, [-0.12, 1.65, 1.6], [-0.12, 1.63, 1.35], [-0.12, 1.55, -1.5], [-0.12, 1.55, -1.5], lens=44)])
T13 = st.at('S13', 'L13', 5) - 0.1   # « l'eau »
CAM13, LOOK13 = [-1.5, 1.72, -0.95], [-2.5, 1.55, -3.0]   # end of the push-in
def _onscreen(cam_, look, d, sx, sy):   # world point at distance d along the view, at screen offset (sx, sy) in half-widths / half-heights (lens 44, 9:16)
    f = [look[i] - cam_[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)); f = [v / n for v in f]
    r = [-f[2], 0.0, f[0]]; n = math.sqrt(r[0] ** 2 + r[2] ** 2); r = [v / n for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    return [round(cam_[i] + d * (f[i] + 0.2272 * sx * r[i] + 0.4040 * sy * u[i]), 3) for i in range(3)]
BILL13 = _onscreen(CAM13, LOOK13, 1.7, 0.45, 0.35)   # upper right, clear of the face and the cloud: a pop-in document facing the lens
BILL13_RY = round(math.degrees(math.atan2(CAM13[0] - BILL13[0], CAM13[2] - BILL13[2])), 1)
st.shot('S13', 'bathroom', actors=[act('mec', [-2.85, 0.19, -2.95], 70, 'sitFloor', 'relieved', fx={'wet': True}, keys=[k(T13 + 0.05, expr='starEyes')])],   # sitting in the bath under his own rain, facing the camera at 3/4
        props=[CLOUD((-2.8, 0, -2.95), 2.3, 0.7, 'happy', True, False), P('bill', 'waterBill', pos=BILL13, ry=BILL13_RY, opts={'w': 0.4, 'h': 0.31, 'popAt': T13})],
        cams=[cam(0.0, [-1.2, 1.62, -0.3], [-1.24, 1.62, -0.42], [-2.5, 1.5, -3.0], [-2.5, 1.5, -3.0], lens=44), cam(T13 - 0.04, [-1.24, 1.62, -0.42], CAM13, [-2.5, 1.5, -3.0], LOOK13, lens=44, ease='out')])
st.card('S02', 'LA PLUIE'); st.card('S10', 'INONDÉE')
st.cue('sfx:click', 'S01', T1, 0.35); st.cue('sfx:paper', 'S02', 0.1, 0.3); st.cue('pop', 'S02', TR, 0.45); st.cue('sfx:gasp', 'S02', TR + 0.1, 0.3); st.cue('sfx:splash', 'S03', 0.3, 0.25); st.cue('sfx:step', 'S04', 0.2, 0.25)
st.cue('sfx:gasp', 'S08', 0.3, 0.3); st.cue('sfx:splash', 'S10', 0.3, 0.4); st.cue('sfx:splash', 'S11', 0.4, 0.3); st.cue('sfx:paper', 'S13', T13, 0.3); st.cue('sfx:ding', 'S13', T13 + 0.3, 0.3)
st.write('Le parapluie', {'passante': {'preset': 'madame', 'seed': 91}, 'collegue': {'preset': 'boss', 'seed': 92}, 'soeur': {'preset': 'madame', 'seed': 93, 'suit': '#F7F5F0', 'lapel': '#FFFFFF'},
                          'marie': {'preset': 'politique', 'seed': 94}, 'guichet': {'preset': 'serveur', 'seed': 95}, 'facteur': {'preset': 'cop', 'seed': 96, 'suit': '#2F62B5', 'hatColor': '#F2C94C'},
                          'spect1': {'preset': 'boss', 'seed': 97}, 'spect2': {'preset': 'madame', 'seed': 98}})
