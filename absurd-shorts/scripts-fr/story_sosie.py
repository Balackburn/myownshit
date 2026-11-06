#!/usr/bin/env python3
"""Le sosie: he enters a lookalike contest... of himself, and finishes third: the two winners looked more like him than he
does. He complains; the jury asks for proof; he shows his ID card; the jury recognises the winner, who leaves with the trophy
and with his life: his job, his flat; his wife finds he has changed, for the better. Today the man is a professional lookalike
of the winner. Last weekend he entered the contest again: third."""
from story_kit import *

st = Story('sosie')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(2, 19)])
PI = math.pi
STAGE = {'backdrop': 'CONCOURS DE SOSIES|SOSIES|CONCOURS', 'podium': False, 'flags': False}
BK = -3.0
BADGE = lambda aid, text, w=0.22: P(f'badge_{aid}', 'noticeBoard', on={'actor': aid, 'joint': 'torso', 'offset': [0.09, 0.5, 0.135]}, opts={'text': text, 'style': 'tag', 'w': w, 'h': 0.08})
POD = lambda: P('pod', 'winnersPodium', pos=[0, 0, -1.6], opts={'w': 0.75, 'hs': 1.0})
ONPOD = lambda clip1='celebrate', clip2='celebrate', clip3='stand', e3='unimpressed': [act('gagnant', [0, 0.6, -1.6], 0, clip1, 'smug'), act('second', [-0.78, 0.42, -1.6], 0, clip2, 'happy'),
                                                                                  act('mec', [0.78, 0.28, -1.6], 0, clip3, e3)]
JURY = lambda clips=('sitHoldUp', 'sitHoldUp', 'sitHoldUp'), exprs=('suspicious', 'suspicious', 'suspicious'): [act(f'juge{i}', [x, 0, 1.6], 180, c, e) for i, (x, c, e) in enumerate(zip((-0.62, 0.0, 0.62), clips, exprs))]
JURY_PROPS = [P('jtab', 'table', pos=[0, 0, 1.2], opts={'w': 2.0, 'd': 0.6, 'h': 0.75, 'color': '#2C4A8A'}),
              P('jsign', 'noticeBoard', pos=[0, 0.5, 0.88], rot=[0, PI, 0], opts={'text': 'JURY', 'style': 'tag', 'w': 0.5, 'h': 0.14})]
CARDS = [P(f'sc{i}', 'scoreCard', on={'actor': f'juge{i}', 'hand': 'R', **HAND_FLAT}, opts={'text': t}) for i, t in enumerate(('10', '10', '10'))]

# 1-5: the contest, of himself; third; the two first looked more like him
st.shot('S01', 'pressRoom', setOpts=STAGE, actors=[act('mec', [0, 0, -1.9], 0, 'wave', 'happy')], props=[BADGE('mec', 'N° 3')],
        cams=[cam(0.0, [0.25, 1.62, 0.3], [0.23, 1.62, 0.05], [0.0, 1.55, -1.9], [0.0, 1.56, -1.9], lens=44)])
st.shot('S02', 'pressRoom', setOpts=STAGE, props=[P('ban', 'signBoard', pos=[0, 0, BK + 0.4], opts={'text': 'CONCOURS DE SOSIES', 'w': 2.6, 'h': 0.5, 'height': 2.0, 'bg': '#F2C94C', 'fg': '#1C252A', 'frame': '#1C252A'})],
        cams=[cam(0.0, [0.1, 1.9, 1.2], [0.1, 2.05, 0.85], [0.0, 2.15, BK + 0.4], [0.0, 2.2, BK + 0.4], lens=44)])
LINE = [(-1.05, 'sosie4', 'N° 1'), (-0.35, 'gagnant', 'N° 2'), (0.35, 'mec', 'N° 3'), (1.05, 'second', 'N° 4')]
st.shot('S03', 'pressRoom', setOpts=STAGE, actors=[act(a, [x, 0, -1.9], 0, 'stand', 'unimpressed') for x, a, n in LINE], props=[BADGE(a, n) for x, a, n in LINE],
        cams=[cam(0.0, [0.05, 1.5, 2.3], [0.05, 1.5, 2.0], [0.0, 1.3, -1.9], [0.0, 1.3, -1.9], lens=46)])
st.shot('S04', 'pressRoom', setOpts=STAGE, actors=ONPOD(), props=[POD(), BADGE('mec', 'LE VRAI', 0.3)],
        cams=[cam(0.0, [0.1, 1.45, 2.4], [0.1, 1.47, 2.1], [0.0, 1.55, -1.6], [0.0, 1.57, -1.6], lens=46)])
st.shot('S05', 'pressRoom', setOpts=STAGE, actors=JURY() + [act('mec', [0.0, 0, -0.4], 0, 'shrug', 'sad')], props=JURY_PROPS + CARDS[:2] + [P('sc2', 'scoreCard', on={'actor': 'juge2', 'hand': 'R', **HAND_FLAT}, opts={'text': '4', 'color': '#C8322A'})],
        cams=[cam(0.0, [0.3, 1.5, -1.6], [0.28, 1.5, -1.35], [0.0, 1.25, 1.4], [0.0, 1.26, 1.4], lens=46)])
# 6-9: the complaint, proof, the ID card, the jury recognises the winner
st.shot('S06', 'pressRoom', setOpts=STAGE, actors=JURY(('sit', 'sit', 'sit'), ('unimpressed', 'unimpressed', 'unimpressed')) + [act('mec', [0.05, 0, 0.45], 180, 'slamTable', 'angry')], props=JURY_PROPS,
        cams=[cam(0.0, [1.1, 1.5, -0.6], [1.05, 1.5, -0.4], [0.0, 1.25, 1.1], [0.0, 1.25, 1.1], lens=44)])
st.shot('S07', 'pressRoom', setOpts=STAGE, actors=JURY(('sit', 'pointSelf', 'sit'), ('suspicious', 'suspicious', 'suspicious')), props=JURY_PROPS + [P('proof', 'noticeBoard', pos=[0.0, 2.25, 1.6], rot=[0, PI, 0], opts={'text': 'PREUVE ?', 'style': 'tag', 'w': 0.55, 'h': 0.16, 'popAt': 0.25})],
        cams=[cam(0.0, [0.15, 1.45, -0.7], [0.14, 1.45, -0.5], [0.0, 1.45, 1.4], [0.0, 1.46, 1.4], lens=44)])
st.shot('S08', 'pressRoom', setOpts=STAGE, props=[P('idc', 'idCard', pos=[0, 1.5, 0], scale=5.0)], cams=[cam(0.0, [0.02, 1.5, 0.95], [0.02, 1.5, 0.85], [0, 1.5, 0], [0, 1.5, 0], lens=40)])
st.shot('S09', 'pressRoom', setOpts=STAGE, actors=JURY(('sitPoint', 'sitPoint', 'sitPoint'), ('happy', 'happy', 'happy')) + [act('gagnant', [0.0, 0.6, -1.6], 0, 'celebrate', 'smug')], props=JURY_PROPS + [POD()],
        cams=[cam(0.0, [1.1, 1.75, 2.9], [1.05, 1.75, 2.7], [0.0, 1.35, -0.4], [0.0, 1.35, -0.4], lens=46)])
# 10-15: the winner leaves with the trophy, and with his life: job, flat, wife
st.shot('S10', 'pressRoom', setOpts=STAGE, actors=[act('gagnant', [0.3, 0, -1.4], 0, 'holdOut', 'smug', keys=[k(0.0, to=[0.3, 0, 0.4], dur=st.dur('S10'), clip='walk')])],
        props=[P('cup', 'trophy', on={'actor': 'gagnant', 'hand': 'R', **HAND_FLAT}, scale=1.6)], cams=[cam(0.0, [0.45, 1.5, 2.4], [0.44, 1.5, 2.3], [0.3, 1.35, -0.5], [0.3, 1.35, 0.3], lens=44)])
st.shot('S11', 'parisStreet', actors=[act('gagnant', [6.6, 0, 0.0], 160, 'takeItem', 'smug'), act('mec', [6.85, 0, 0.8], -20, 'giveItem', 'sad')],
        props=[P('case', 'briefcase', on={'actor': 'gagnant', 'hand': 'R'}), P('cup', 'trophy', on={'actor': 'gagnant', 'hand': 'L', **HAND_FLAT}, scale=1.4)],
        cams=MS(6.72, 0.4, h=1.5, d=3.2))
st.shot('S12', 'office', actors=[act('gagnant', [0.0, 0, -1.9], 0, 'sitTalk', 'smug')],
        props=[P('d', 'desk', pos=[0, 0, -1.4]), P('np', 'noticeBoard', pos=[0.0, 0.84, -0.98], opts={'text': 'LE MEC', 'style': 'tag', 'w': 0.42, 'h': 0.12}), P('ch', 'chair', pos=[0, 0, -1.9], opts={'color': '#3A3D44'})],
        cams=[cam(0.0, [0.3, 1.35, 1.0], [0.28, 1.36, 0.75], [0.0, 1.1, -1.5], [0.0, 1.1, -1.5], lens=44)])
st.shot('S13', 'livingRoom', actors=[act('gagnant', [0.0, 0, -2.8], 0, 'sit', 'smug')], props=[P('mat', 'doormat', pos=[1.6, 0, -1.2], opts={'text': 'CHEZ LE MEC'})],
        cams=[cam(0.0, [0.35, 1.35, 0.4], [0.33, 1.36, 0.1], [0.0, 1.0, -2.8], [0.0, 1.0, -2.8], lens=44)])
st.shot('S14', 'livingRoom', actors=[act('gagnant', [0.25, 0, -2.75], 0, 'sit', 'smug'), act('femme', [-0.7, 0, -1.9], 60, 'handsOnHips', 'suspicious')],
        cams=[cam(0.0, [0.4, 1.5, 0.8], [0.38, 1.5, 0.55], [-0.15, 1.2, -2.3], [-0.15, 1.2, -2.3], lens=44)])
st.shot('S15', 'livingRoom', actors=[act('gagnant', [0.15, 0, -2.0], -40, 'stand', 'smug'), act('femme', [-0.35, 0, -1.7], 120, 'giveItem', 'happy')],
        props=[P(f'h{i}', 'heart', pos=[x, y, -1.6], scale=0.3, keys=[k(0.0, scale=0.01), k(0.1 + 0.15 * i, scale=0.3, dur=0.25, ease='outBack')]) for i, (x, y) in enumerate(((-0.55, 2.2), (0.0, 2.45), (0.45, 2.15)))],
        cams=[cam(0.0, [0.0, 1.55, 0.9], [-0.02, 1.56, 0.65], [-0.1, 1.6, -1.85], [-0.1, 1.62, -1.85], lens=44)])
# 16-19: a professional lookalike of the winner; the contest again: third
BALLOONS = [P(f'bl{i}', 'balloon', pos=[x, 0, z], opts={'color': c, 'string': 1.3 + 0.2 * (i % 2)}) for i, (x, z, c) in enumerate(((-1.4, -2.6, '#C8322A'), (1.3, -2.7, '#2F62B5'), (-0.9, -3.0, '#F2C94C'), (0.9, -3.05, '#2F7F5C')))]
st.shot('S16', 'livingRoom', setOpts={'sofa': False, 'tv': False}, actors=[act('mec', [0.0, 0, -1.6], 0, 'present', 'happy'), act('k1', [-0.75, 0, -0.6], 160, 'celebrate', 'happy'), act('k2', [0.75, 0, -0.6], -160, 'celebrate', 'happy')],
        props=BALLOONS + [P('pro', 'noticeBoard', pos=[0.0, 2.45, -2.4], opts={'text': 'SOSIE PRO', 'style': 'sign', 'w': 0.9, 'h': 0.24, 'bg': '#F2C94C', 'fg': '#1C252A', 'frame': '#1C252A'})],
        cams=[cam(0.0, [0.25, 1.4, 1.8], [0.24, 1.42, 1.55], [0.0, 1.4, -1.6], [0.0, 1.42, -1.6], lens=46)])
st.shot('S17', 'livingRoom', setOpts={'sofa': False, 'tv': False}, actors=[act('mec', [0.55, 0, -2.6], -15, 'pointSelf', 'unimpressed')],
        props=BALLOONS + [P('poster', 'portraitPoster', pos=[-0.3, 1.55, -3.5], opts={'text': "L'ORIGINAL", 'w': 0.75})],
        cams=[cam(0.0, [0.25, 1.55, -0.3], [0.24, 1.56, -0.5], [0.12, 1.5, -3.2], [0.12, 1.51, -3.2], lens=44)])
st.shot('S18', 'pressRoom', setOpts=STAGE, actors=[act('mec', [0.0, 0, -1.9], 0, 'wave', 'happy')],
        props=[BADGE('mec', 'N° 3'), P('ed', 'noticeBoard', pos=[0.0, 2.55, BK + 0.1], opts={'text': 'ÉDITION 2027', 'style': 'sign', 'w': 1.1, 'h': 0.26, 'bg': '#F2C94C', 'fg': '#1C252A', 'frame': '#1C252A'})],
        cams=[cam(0.0, [0.25, 1.62, 0.6], [0.23, 1.62, 0.3], [0.0, 1.7, -1.9], [0.0, 1.71, -1.9], lens=44)])
st.shot('S19', 'pressRoom', setOpts=STAGE, actors=ONPOD('celebrate', 'celebrate', 'stand', 'unimpressed'), props=[POD(), BADGE('mec', 'LE VRAI', 0.3)],
        cams=[cam(0.0, [0.55, 1.5, 1.4], [0.6, 1.48, 1.15], [0.6, 1.5, -1.6], [0.68, 1.48, -1.6], lens=44)])
st.card('S03', 'DE LUI-MÊME'); st.card('S11', 'SA VIE')
st.cue('sfx:fanfare', 'S01', 0.1, 0.3); st.cue('pop', 'S03', 0.2, 0.35); st.cue('sfx:choir', 'S04', 0.1, 0.25); [st.cue('clack', 'S05', 0.15 + 0.2 * i, 0.35) for i in range(3)]
st.cue('thud', 'S06', 0.35, 0.5); st.cue('pop', 'S07', 0.25, 0.4); st.cue('sfx:paper', 'S08', 0.1, 0.4); st.cue('sfx:cash', 'S10', 0.3, 0.3); st.cue('sfx:step', 'S10', 0.5, 0.3)
st.cue('sfx:spring', 'S13', 0.2, 0.25); st.cue('sfx:bell', 'S15', 0.15, 0.35); st.cue('sfx:fanfare', 'S16', 0.1, 0.25); st.cue('sfx:fanfare', 'S18', 0.1, 0.25)
st.write('Le sosie', {
    'gagnant': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'second': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'sosie4': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'juge0': {'preset': 'politique', 'seed': 31}, 'juge1': {'preset': 'madame', 'seed': 32, 'glasses': True}, 'juge2': {'preset': 'chef', 'seed': 33},
    'femme': {'preset': 'femme'}, 'k1': {'preset': 'gamin', 'seed': 41}, 'k2': {'preset': 'gamin', 'seed': 42, 'suit': '#C9822E'}})
