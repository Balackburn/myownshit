#!/usr/bin/env python3
"""Le sosie: he enters a lookalike contest... of himself, and finishes third: the two winners looked more like him than he
does. He complains; the jury asks for proof; he shows his ID card; the jury recognises the winner, who leaves with the trophy
and with his life: his job, his flat; his wife finds he has changed, for the better. Today the man is a professional lookalike
of the winner. Last weekend he entered the contest again: third.
Who is who: the man always wears his contest badge « N° 3 »; the winner wears the gold medal and keeps the trophy near him."""
from story_kit import *

st = Story('sosie')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(2, 19)])
PI = math.pi
STAGE = {'backdrop': 'SOSIES|CONCOURS', 'fontScale': 0.66, 'bg': '#F6D77A', 'fg': 'rgba(200,50,42,0.55)', 'wall': '#8FC1DE', 'band': '#6FA3C4', 'trim': '#3E6E8E',
         'floor': '#C2554A', 'podium': False, 'flags': False, 'chairColor': '#2F62B5'}
BK = -3.0
BADGE = lambda aid, text='N° 3', w=0.22: P(f'badge_{aid}', 'noticeBoard', on={'actor': aid, 'joint': 'torso', 'offset': [0.09, 0.5, 0.135]}, opts={'text': text, 'style': 'tag', 'w': w, 'h': 0.08})
MEDAL = lambda aid='gagnant': P(f'medal_{aid}', 'medal', on={'actor': aid, 'joint': 'torso', 'offset': [0.0, 0.62, 0.14]}, scale=1.7)
POD = lambda: P('pod', 'winnersPodium', pos=[0, 0, -1.6], opts={'w': 0.75, 'hs': 1.0})
S1X, S2X, S3X = 0.0, -0.77, 0.77
ONPOD = lambda c1='celebrate', c2='celebrate', c3='stand', e3='unimpressed': [act('gagnant', [S1X, 0.6, -1.6], 0, c1, 'smug'), act('second', [S2X, 0.42, -1.6], 0, c2, 'happy'), act('mec', [S3X, 0.28, -1.6], 0, c3, e3)]
JZ = 1.6
JURY = lambda clips=('sit', 'sit', 'sit'), exprs=('suspicious', 'suspicious', 'suspicious'): [act(f'juge{i}', [x, 0, JZ], 180, c, e) for i, (x, c, e) in enumerate(zip((-0.62, 0.0, 0.62), clips, exprs))]
JURY_PROPS = [P('jtab', 'table', pos=[0, 0, 1.2], opts={'w': 2.0, 'd': 0.6, 'h': 0.75, 'color': '#2C4A8A'}), P(f'jch0', 'chair', pos=[-0.62, 0, JZ], ry=180, opts={'color': '#3A3D44'}),
              P('jch1', 'chair', pos=[0, 0, JZ], ry=180, opts={'color': '#3A3D44'}), P('jch2', 'chair', pos=[0.62, 0, JZ], ry=180, opts={'color': '#3A3D44'})]
SIGN = lambda pid, text, pos, bg='#F2C94C', fg='#1C252A', w=0.6, h=0.18, ry=0, pop=None: P(pid, 'noticeBoard', pos=pos, ry=ry, opts={'text': text, 'style': 'sign', 'w': w, 'h': h, 'bg': bg, 'fg': fg, 'frame': '#1C252A', **({'popAt': pop} if pop is not None else {})})

# 1-5: the contest, of himself; third; the two first looked more like him
st.shot('S01', 'pressRoom', setOpts=STAGE, actors=[act('mec', [0, 0, -1.9], 0, 'wave', 'happy')], props=[BADGE('mec')],
        cams=[cam(0.0, [0.3, 1.55, 0.7], [0.28, 1.55, 0.5], [0.0, 1.5, -1.9], [0.0, 1.5, -1.9], lens=44)])
st.shot('S02', 'pressRoom', setOpts=STAGE, props=[P('ban', 'signBoard', pos=[0, 0, BK + 0.4], opts={'text': 'CONCOURS DE SOSIES', 'w': 2.4, 'h': 0.62, 'height': 1.75, 'bg': '#C8322A', 'fg': '#FFFFFF', 'frame': '#F2C94C', 'posts': False})],
        cams=[cam(0.0, [0.12, 2.25, 0.9], [0.1, 2.12, 0.55], [0.0, 2.08, BK + 0.4], [0.0, 2.06, BK + 0.4], lens=44)])
LINE = [(-1.05, 'sosie4', 'N° 1'), (-0.35, 'gagnant', 'N° 2'), (0.35, 'mec', 'N° 3'), (1.05, 'second', 'N° 4')]
st.shot('S03', 'pressRoom', setOpts=STAGE, actors=[act(a, [x, 0, -1.9], 0, 'stand', 'unimpressed') for x, a, n in LINE], props=[BADGE(a, n) for x, a, n in LINE],
        cams=[cam(0.0, [0.1, 1.45, 3.8], [0.1, 1.45, 3.5], [0.0, 1.32, -1.9], [0.0, 1.32, -1.9], lens=44)])
st.shot('S04', 'pressRoom', setOpts=STAGE, actors=ONPOD(), props=[POD(), BADGE('mec')],
        cams=[cam(0.0, [1.55, 1.15, 2.3], [1.5, 1.17, 2.1], [0.6, 1.45, -1.6], [0.62, 1.47, -1.6], lens=44)])
D5 = st.dur('S05')
st.shot('S05', 'pressRoom', setOpts=STAGE, actors=ONPOD('stand', 'stand', 'stand', 'sad'), props=[POD(), BADGE('mec'),
        SIGN('p1', '99 %', [S1X, 3.0, -1.6], '#4CAF50', '#FFFFFF', pop=0.2), SIGN('p2', '98 %', [S2X, 2.82, -1.6], '#4CAF50', '#FFFFFF', pop=0.55), SIGN('p3', '41 %', [S3X, 2.68, -1.6], '#C8322A', '#FFFFFF', pop=1.15)],
        cams=[cam(0.0, [0.12, 1.6, 3.9], [0.12, 1.6, 3.6], [0.0, 1.6, -1.6], [0.0, 1.6, -1.6], lens=44)])
# 6-9: the complaint, proof, the ID card, the jury recognises the winner
st.shot('S06', 'pressRoom', setOpts=STAGE, actors=JURY() + [act('mec', [0.05, 0, 0.42], 0, 'slamTable', 'angry')], props=JURY_PROPS + [BADGE('mec'),
        P('form', 'noticeBoard', pos=[0.05, 0.765, 0.98], rot=[-PI / 2, 0, 0], opts={'text': 'RÉCLAMATION', 'style': 'tag', 'w': 0.3, 'h': 0.1})],
        cams=[cam(0.0, [3.4, 1.65, 1.05], [3.15, 1.65, 1.02], [0.0, 1.3, 1.0], [0.0, 1.3, 1.0], lens=44)])
st.shot('S07', 'pressRoom', setOpts=STAGE, actors=JURY(('sit', 'sitPoint', 'sit'), ('suspicious', 'suspicious', 'unimpressed')), props=JURY_PROPS + [SIGN('proof', 'PREUVE ?', [0.0, 2.15, JZ + 0.05], ry=180, pop=0.3)],
        cams=[cam(0.0, [0.12, 1.6, -2.3], [0.12, 1.6, -2.05], [0.0, 1.3, JZ], [0.0, 1.32, JZ], lens=44)])
st.shot('S08', 'pressRoom', setOpts=STAGE, actors=[act('mec', [0, 0, 0.42], 0, 'showPhoneFaceL', 'unimpressed')],
        props=[BADGE('mec'), P('idc', 'idCardMec', on={'actor': 'mec', 'hand': 'L', 'rot': [0, -1.5708, 3.1416], 'offset': [0, -0.17, 0.035]}, scale=2.2)],
        cams=[cam(0.0, [0.15, 1.72, 2.55], [0.14, 1.72, 2.35], [0.1, 1.68, 0.42], [0.1, 1.68, 0.42], lens=44)])
st.shot('S09', 'pressRoom', setOpts=STAGE, actors=JURY(('sitPoint', 'sitPoint', 'sitPoint'), ('happy', 'happy', 'happy')) + [act('gagnant', [0.35, 0, -0.35], 0, 'heroPose', 'smug'), act('mec', [1.05, 0, -0.3], -20, 'stand', 'sad')],
        props=JURY_PROPS + [BADGE('mec'), MEDAL(), SIGN('lui', "C'EST LUI !", [0.35, 2.5, -0.35], '#4CAF50', '#FFFFFF', w=0.7, h=0.2, pop=0.5)],
        cams=[cam(0.0, [0.3, 2.9, 3.6], [0.3, 2.86, 3.35], [0.6, 1.2, -0.3], [0.6, 1.22, -0.3], lens=44)])
# 10-15: the winner leaves with the trophy, and with his life: job, flat, wife
D10 = st.dur('S10')
CUP = lambda aid='gagnant', s=1.5: P('cup', 'trophy', on={'actor': aid, 'joint': 'torso', 'offset': [0.0, 0.18, 0.3]}, scale=s)
st.shot('S10', 'pressRoom', setOpts=STAGE, actors=[act('gagnant', [0.25, 0, -1.6], 0, 'stand', 'smug', keys=[k(0.0, to=[0.25, 0, 0.3], dur=D10, clip='carryBox', face='keep')])], props=[MEDAL(), CUP()],
        cams=[cam(0.0, [0.42, 1.45, 1.4], [0.4, 1.45, 2.7], [0.25, 1.35, -1.6], [0.25, 1.35, 0.3], lens=44)])
st.shot('S11', 'parisStreet', actors=[act('gagnant', [6.3, 0, 0.6], 75, 'takeItem', 'smug'), act('mec', [7.15, 0, 0.6], -75, 'giveItem', 'sad')],
        props=[MEDAL(), BADGE('mec'), P('case', 'briefcase', on={'actor': 'mec', 'hand': 'R'}), P('cup', 'trophy', pos=[5.85, 0, 0.75], scale=1.4)],
        cams=[cam(0.0, [6.85, 1.55, 4.6], [6.83, 1.55, 4.35], [6.72, 1.5, 0.6], [6.72, 1.5, 0.6], lens=44)])
st.shot('S12', 'office', actors=[act('gagnant', [0.0, 0, -1.95], 0, 'sitWrite', 'smug')],
        props=[MEDAL(), P('d', 'desk', pos=[0, 0, -1.4]), P('np', 'noticeBoard', pos=[0.12, 0.84, -0.98], opts={'text': 'LE MEC', 'style': 'tag', 'w': 0.42, 'h': 0.12}),
               P('ch', 'chair', pos=[0, 0, -1.95], opts={'color': '#3A3D44'}), P('cup', 'trophy', pos=[-0.45, 0.76, -1.45], scale=1.3)],
        cams=[cam(0.0, [0.32, 1.4, 1.05], [0.3, 1.4, 0.8], [0.0, 1.12, -1.6], [0.0, 1.12, -1.6], lens=44)])
SOFA_Z = -2.8
st.shot('S13', 'livingRoom', actors=[act('gagnant', [0.0, 0, SOFA_Z], 0, 'sit', 'smug')],
        props=[MEDAL(), P('st', 'table', pos=[0.85, 0, SOFA_Z + 0.1], opts={'w': 0.45, 'd': 0.45, 'h': 0.5, 'color': '#2F7F8C'}), P('cup', 'trophy', pos=[0.85, 0.5, SOFA_Z + 0.1], scale=1.3)],
        cams=[cam(0.0, [0.45, 1.3, 0.6], [0.42, 1.31, 0.35], [0.25, 1.0, SOFA_Z], [0.25, 1.0, SOFA_Z], lens=44)])
st.shot('S14', 'livingRoom', actors=[act('gagnant', [0.0, 0, SOFA_Z], 0, 'sit', 'smug'), act('femme', [-0.95, 0, SOFA_Z + 0.75], 50, 'handsOnHips', 'suspicious')],
        props=[MEDAL(), P('st', 'table', pos=[0.85, 0, SOFA_Z + 0.1], opts={'w': 0.45, 'd': 0.45, 'h': 0.5, 'color': '#2F7F8C'}), P('cup', 'trophy', pos=[0.85, 0.5, SOFA_Z + 0.1], scale=1.3),
               SIGN('q', '?', [-0.95, 2.2, SOFA_Z + 0.75], w=0.22, h=0.22, pop=0.45)],
        cams=[cam(0.0, [-0.15, 1.45, 1.4], [-0.16, 1.46, 1.15], [-0.45, 1.2, SOFA_Z + 0.3], [-0.45, 1.2, SOFA_Z + 0.3], lens=44)])
st.shot('S15', 'livingRoom', actors=[act('gagnant', [0.0, 0, SOFA_Z], 0, 'sit', 'smug'), act('femme', [-0.75, 0, SOFA_Z + 0.55], 60, 'celebrate', 'happy')],
        props=[MEDAL()] + [P(f'h{i}', 'heart', pos=[x, y, SOFA_Z + 0.4], scale=0.3, keys=[k(0.0, scale=0.01), k(0.06 + 0.12 * i, scale=0.3, dur=0.22, ease='outBack')]) for i, (x, y) in enumerate(((-0.75, 2.2), (-0.3, 2.36), (0.15, 2.16)))],
        cams=[cam(0.0, [-0.2, 1.55, 1.05], [-0.21, 1.56, 0.85], [-0.35, 1.45, SOFA_Z + 0.3], [-0.35, 1.47, SOFA_Z + 0.3], lens=44)])
# 16-19: a professional lookalike of the winner; the contest again: third
BALLOONS = [P(f'bl{i}', 'balloon', pos=[x, 0, z], opts={'color': c, 'string': 1.3 + 0.2 * (i % 2)}) for i, (x, z, c) in enumerate(((-1.25, -2.4, '#C8322A'), (1.2, -2.5, '#2F62B5'), (-0.75, -2.8, '#F2C94C'), (0.8, -2.85, '#2F7F5C')))]
PARTY = {'sofa': False, 'tv': False}
st.shot('S16', 'livingRoom', setOpts=PARTY, actors=[act('mec', [0.0, 0, -1.7], 0, 'present', 'happy'), act('k1', [-0.65, 0, -0.75], 150, 'celebrate', 'happy'), act('k2', [0.7, 0, -0.8], -150, 'celebrate', 'happy')],
        props=BALLOONS + [BADGE('mec', 'SOSIE PRO', 0.32), SIGN('pro', 'SOSIE PROFESSIONNEL', [0.0, 2.55, -2.9], w=1.3, h=0.26)],
        cams=[cam(0.0, [0.2, 1.4, 2.6], [0.19, 1.42, 2.3], [0.0, 1.35, -1.7], [0.0, 1.37, -1.7], lens=44)])
st.shot('S17', 'livingRoom', setOpts=PARTY, actors=[act('gagnant', [-0.42, 0, -1.8], 8, 'heroPose', 'smug'), act('mec', [0.42, 0, -1.8], -8, 'heroPose', 'smug')],
        props=BALLOONS + [MEDAL(), BADGE('mec', 'SOSIE PRO', 0.32), SIGN('o', "L'ORIGINAL", [-0.42, 2.5, -1.8], '#F2C94C', w=0.62, h=0.17), SIGN('s', 'LE SOSIE', [0.42, 2.5, -1.8], '#FFFFFF', w=0.62, h=0.17)],
        cams=[cam(0.0, [0.05, 1.5, 2.15], [0.05, 1.51, 1.9], [0.0, 1.55, -1.8], [0.0, 1.56, -1.8], lens=44)])
st.shot('S18', 'pressRoom', setOpts=STAGE, actors=[act('mec', [0.0, 0, -1.9], 0, 'wave', 'happy')],
        props=[BADGE('mec'), SIGN('ed', 'ÉDITION 2027', [0.0, 2.72, BK + 0.1], w=1.1, h=0.26)],
        cams=[cam(0.0, [0.3, 1.7, 0.95], [0.28, 1.7, 0.7], [0.0, 1.85, -1.9], [0.0, 1.85, -1.9], lens=44)])
st.shot('S19', 'pressRoom', setOpts=STAGE, actors=ONPOD('celebrate', 'celebrate', 'stand', 'unimpressed'), props=[POD(), BADGE('mec')],
        cams=[cam(0.0, [1.55, 1.15, 2.3], [1.05, 2.0, -0.2], [0.6, 1.45, -1.6], [0.77, 2.08, -1.6], lens=44, ease='inOut')])
st.card('S03', 'DE LUI-MÊME'); st.card('S11', 'SA VIE')
st.cue('sfx:fanfare', 'S01', 0.1, 0.3); st.cue('pop', 'S03', 0.2, 0.35); st.cue('sfx:choir', 'S04', 0.1, 0.25); [st.cue('clack', 'S05', t, 0.35) for t in (0.2, 0.55)]; st.cue('thud', 'S05', 1.15, 0.5)
st.cue('thud', 'S06', 0.12, 0.5); st.cue('pop', 'S07', 0.3, 0.4); st.cue('sfx:paper', 'S08', 0.1, 0.4); st.cue('sfx:ding', 'S09', 0.5, 0.35); st.cue('sfx:step', 'S10', 0.4, 0.3)
st.cue('sfx:cash', 'S11', 0.2, 0.3); st.cue('sfx:spring', 'S13', 0.15, 0.25); st.cue('pop', 'S14', 0.45, 0.3); st.cue('sfx:bell', 'S15', 0.1, 0.35); st.cue('sfx:fanfare', 'S16', 0.1, 0.25); st.cue('sfx:fanfare', 'S18', 0.1, 0.25)
st.write('Le sosie', {
    'gagnant': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'second': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'sosie4': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'juge0': {'preset': 'politique', 'seed': 31}, 'juge1': {'preset': 'madame', 'seed': 32, 'glasses': True}, 'juge2': {'preset': 'prefet', 'seed': 33},
    'femme': {'preset': 'femme'}, 'k1': {'preset': 'gamin', 'seed': 41}, 'k2': {'preset': 'gamin', 'seed': 42, 'suit': '#C9822E'}})
