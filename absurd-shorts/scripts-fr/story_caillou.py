#!/usr/bin/env python3
"""Le caillou: he adopts a rock and calls it Gérard. At school Gérard never chats: top of the class, French champion of "un, deux,
trois, soleil"; after the bac he becomes a security guard (nobody ever got past), then mayor: zero broken promises (he made none),
elected with 100 %. Then Gérard gets a big head (literally: a boulder), demands a statue, takes the living room, then the bedroom.
Today the man sleeps in the kennel; Gérard bought him a collar and named him Caillou."""
from story_kit import *

st = Story('caillou')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 7)] + [('S07', 'L06', 4)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(7, 20)])
PI = math.pi
ROCK = lambda pid, pos, scale=1.0, rot=None, keys=None, on=None, **o: P(pid, 'petRock', **({'pos': pos} if pos else {}), **({'on': on} if on else {}), scale=scale,
                                                                        **({'rot': rot} if rot else {}), opts=o, **({'keys': keys} if keys else {}))
TAG = lambda pid, text, pos, at_=None, rot=None, **kw: P(pid, 'noticeBoard', pos=pos, **({'rot': rot} if rot else {}), opts={'text': text, 'style': 'tag', 'w': kw.pop('w', 0.6), 'h': kw.pop('h', 0.16), **({'popAt': at_} if at_ is not None else {}), **kw})
DOC = lambda text, stamp, size=0.34: P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': text, 'style': 'doc', 'w': 0.72, 'h': 0.9, 'popAt': 0.1, 'textSize': size, 'stamp': stamp})
DOC_CAM = [cam(0.0, [0.05, 1.55, 2.15], [0.05, 1.55, 1.95], [0, 1.5, 0], [0, 1.5, 0], lens=42)]
BOARD = {'board': 'LUNDI 3 NOVEMBRE', 'board2': 'Dictée : le caillou', 'board3': 'Silence !'}
BIG, BSY = 7.0, 2.0                                                    # Gérard with a big head: a boulder about 2.3 m tall (taller than the man)

# 1-2: the adoption, the name
st.shot('S01', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'holdOut', 'happy')], props=[ROCK('rock', [0.02, 1.38, 0.52], 0.85, rot=[-0.3, 0, 0], look=[0.0, 0.1])],
        cams=[cam(0.0, [0.28, 1.62, 2.25], [0.26, 1.62, 2.05], [0.0, 1.58, 0.0], [0.0, 1.59, 0.0], lens=44)])
st.shot('S02', 'livingRoom', props=[P('tbl', 'table', pos=[0.35, 0, -1.0], opts={'w': 0.6, 'd': 0.5, 'h': 0.55, 'color': '#2F7F7A'}),
                                     ROCK('rock', [0.35, 0.55, -1.0], lookKeys=[[0.0, 0.0, -0.7], [0.4, 0.1, 0.05]])],
        cams=[cam(0.0, [0.5, 0.86, 0.25], [0.48, 0.85, 0.08], [0.35, 0.68, -1.0], [0.35, 0.68, -1.0], lens=40)])
# 3-7: school: never chats, top of the class, champion of "un, deux, trois, soleil"
st.shot('S03', 'classroom', setOpts=BOARD, actors=[act('e1', [-1.6, 0, -0.35], 180, 'sit', 'happy'), act('e2', [1.6, 0, -0.35], 180, 'sit', 'unimpressed'), act('e3', [0.0, 0, 1.0], 180, 'sit', 'happy')],
        props=[ROCK('rock', [0.0, 0.72, -0.9], rot=[0, PI, 0], look=[0.05, 0])],
        cams=[cam(0.0, [0.35, 1.4, -2.75], [0.32, 1.38, -2.55], [0.0, 0.85, -0.2], [0.0, 0.85, -0.2], lens=46)])
st.shot('S04', 'classroom', setOpts=BOARD, actors=[act('e1', [-0.6, 0, -0.4], 130, 'talk', 'happy'), act('e2', [0.6, 0, -0.4], -130, 'laugh', 'happy'), act('maitresse', [1.3, 0, -1.25], -110, 'point', 'angry')],
        props=[P('c1', 'chair', pos=[-0.6, 0, -0.4], rot=[0, PI, 0], opts={'color': '#2F62B5'}), P('c2', 'chair', pos=[0.6, 0, -0.4], rot=[0, PI, 0], opts={'color': '#2F62B5'}),
               ROCK('rock', [0.0, 0.72, -0.9], rot=[0, PI, 0], look=[0.0, 0.0])],
        cams=[cam(0.0, [-0.2, 1.4, -2.95], [-0.18, 1.4, -2.8], [0.25, 1.12, -0.6], [0.25, 1.12, -0.6], lens=54)])
st.shot('S05', 'office', props=[DOC('BULLETIN\nGÉRARD\n20 / 20', 'PREMIER', 0.3)], cams=DOC_CAM)
st.shot('S06', 'grassland', actors=[act('e1', [-0.62, 0.42, 0.0], 0, 'slump', 'sad'), act('e2', [0.62, 0.28, 0.0], 0, 'slump', 'sad')],
        props=[P('pod', 'winnersPodium', pos=[0, 0, 0]), ROCK('rock', [0.0, 0.6, 0.0], medal=True, look=[0.2, 0.0]), P('cup', 'trophy', pos=[0.22, 0.6, 0.15], scale=1.3),
               P('ban', 'signBoard', pos=[0, 0, -1.0], opts={'text': 'CHAMPIONNAT DE FRANCE', 'w': 2.5, 'h': 0.42, 'height': 2.25, 'bg': '#F4F4F0', 'fg': '#2F62B5', 'frame': '#2F62B5'})],
        cams=[cam(0.0, [0.2, 1.15, 4.6], [0.18, 1.17, 4.3], [0.0, 1.32, 0.0], [0.0, 1.34, 0.0], lens=46)])
SOLEIL = st.at('S07', 'L06', 7)
st.shot('S07', 'grassland', actors=[act('e1', [-0.62, 0, -3.3], 0, 'run', 'happy', keys=[k(0.0, to=[-0.62, 0, -2.75], dur=SOLEIL), k(SOLEIL, clip='statueRun')]),
                                     act('e2', [0.05, 0, -3.8], 0, 'run', 'happy', keys=[k(0.0, to=[0.05, 0, -3.25], dur=SOLEIL), k(SOLEIL, clip='flail', expr='scared')]),
                                     act('e3', [0.68, 0, -3.4], 0, 'run', 'happy', keys=[k(0.0, to=[0.68, 0, -2.85], dur=SOLEIL), k(SOLEIL, clip='statueRun')])],
        props=[ROCK('rock', [0.1, 0, -1.55], 1.15, medal=True, look=[0.15, 0.0])],
        cams=[cam(0.0, [0.2, 1.15, 1.7], [0.19, 1.15, 1.5], [0.05, 0.62, -2.3], [0.05, 0.62, -2.3], lens=46)])
# 8-9: security guard: nobody ever got past
SHOP = [P('door', 'door', pos=[10.12, 0, 3.0], rot=[0, -PI / 2, 0], opts={'color': '#2F5E58'}),
        P('stool', 'chair', pos=[9.62, 0, 3.0], rot=[0, -PI / 2, 0], opts={'color': '#3A3D44'}),
        P('shop', 'noticeBoard', pos=[10.06, 2.42, 3.0], rot=[0, -PI / 2, 0], opts={'text': 'SUPERMARCHÉ', 'style': 'sign', 'w': 1.8, 'h': 0.42, 'bg': '#2F7F5C', 'fg': '#FFFFFF', 'frame': '#1E4F3A'})]
st.shot('S08', 'parisStreet', props=SHOP + [ROCK('rock', [9.6, 0.46, 3.0], 1.3, rot=[0, -1.07, 0], cap='guard', brows='angry', look=[0.1, 0.0])],
        cams=[cam(0.0, [7.35, 1.05, 3.75], [7.47, 1.05, 3.7], [9.55, 1.02, 3.0], [9.55, 1.04, 3.0], lens=50)])
QUEUE = [act(f'q{i}', [8.85 - 0.85 * i, 0, 3.0 + (0.12 if i % 2 else -0.08)], 90, c, e) for i, (c, e) in enumerate((('armsCrossed', 'angry'), ('readPhone', 'unimpressed'), ('handsOnHips', 'angry'), ('armsCrossed', 'sad'), ('idle', 'unimpressed')))]
st.shot('S09', 'parisStreet', actors=QUEUE, props=SHOP + [ROCK('rock', [9.6, 0.46, 3.0], 1.3, rot=[0, -PI / 2, 0], cap='guard', brows='angry', look=[0.0, 0.0])],
        cams=[cam(0.0, [7.95, 0.95, 1.55], [8.02, 0.95, 1.65], [9.2, 0.78, 3.0], [9.2, 0.78, 3.0], lens=46)])
# 10-13: mayor: zero broken promises (none made), elected with 100 %
st.shot('S10', 'parisStreet', actors=[act('mec', [7.35, 0, -0.55], -35, 'present', 'smug')],
        props=[P('poster', 'rockPoster', pos=[6.55, 0, -1.0], opts={'popAt': st.at('S10', 'L09', 3) - 0.1, 'w': 0.85}), P('flagfr', 'regionFlag', pos=[5.75, 0, -1.6], scale=1.3, opts={'kind': 'fr'})],
        cams=[cam(0.0, [6.95, 1.45, 2.9], [6.93, 1.45, 2.65], [6.85, 1.35, -1.0], [6.85, 1.36, -1.0], lens=46)])
JOURN = [act('j1', [-0.65, 0, -0.55], 175, 'showPhone', 'happy'), act('j2', [0.7, 0, -0.45], -175, 'showPhone', 'happy')]
st.shot('S11', 'pressRoom', setOpts={'backdrop': 'GÉRARD|MAIRIE|2026'}, actors=JOURN,
        props=[ROCK('rock', [0.0, 1.15, -2.0], 1.0, sash=True, look=[0.1, 0.0]), P('cam1', 'pressCamera', on={'actor': 'j1', 'hand': 'R', **HAND_FLAT}, opts={'flashAt': [0.25, 0.95]}),
               P('cam2', 'pressCamera', on={'actor': 'j2', 'hand': 'R', **HAND_FLAT}, opts={'flashAt': [0.6, 1.3]})],
        cams=[cam(0.0, [0.15, 1.45, 0.3], [0.14, 1.44, 0.1], [0.0, 1.25, -2.0], [0.0, 1.25, -2.0], lens=44)],
        fx=[{'type': 'flash', 'at': t, 'dur': 0.05} for t in (0.25, 0.6)])
st.shot('S12', 'office', props=[DOC('PROGRAMME\n\n\n', 'APPROUVÉ')], cams=DOC_CAM)
st.shot('S13', 'office', props=[P('board', 'resultsBoard', pos=[0.0, 1.55, -0.2], opts={'fillAt': 0.15}), P('tbl', 'table', pos=[0.62, 0, 0.35], opts={'w': 0.55, 'd': 0.45, 'h': 0.75, 'color': '#2F62B5'}),
                                 ROCK('rock', [0.62, 0.75, 0.35], 0.9, sash=True, look=[0.15, 0.3])],
        cams=[cam(0.0, [0.15, 1.45, 3.55], [0.14, 1.46, 3.3], [0.12, 1.32, -0.1], [0.12, 1.33, -0.1], lens=48)])
# 14-17: the big head: statue, living room, bedroom
st.shot('S14', 'livingRoom', actors=[act('mec', [-0.95, 0, 0.75], 40, 'startle', 'surprised')],
        props=[ROCK('rock', [0.45, 0, -0.9], 1.0, brows='smug', lookKeys=[[0.0, 0.0, 0.0], [0.6, -0.3, -0.6]], sy=BSY, keys=[k(0.0, scale=1.0), k(0.2, scale=BIG, dur=1.0, ease='outBack')])],
        cams=[cam(0.0, [-0.25, 1.5, 5.6], [-0.26, 1.55, 5.35], [-0.2, 1.45, -0.6], [-0.2, 1.5, -0.6], lens=48, shake=0.012)])
st.shot('S15', 'parisStreet', props=[P('ped', 'pedestal', pos=[6.4, 0, -1.4], opts={'h': 1.5, 'w': 0.9, 'text': 'GÉRARD'}), ROCK('statue', [6.4, 1.5, -1.4], 2.1, eyes=False, color='#B9B2A4'),
                                      ROCK('rock', [8.1, 0, -2.4], BIG * 0.8, sy=BSY, rot=[0, -0.7, 0], brows='smug', look=[0.1, 0.7])],
        cams=[cam(0.0, [6.25, 0.7, 3.6], [6.27, 0.72, 3.3], [6.75, 1.75, -1.4], [6.75, 1.78, -1.4], lens=48)])
st.shot('S16', 'livingRoom', actors=[act('mec', [-1.62, 0, 0.35], 25, 'sit', 'sad')],
        props=[P('chairM', 'chair', pos=[-1.62, 0, 0.35], rot=[0, 0.4, 0], opts={'color': '#2F7F7A'}), ROCK('rock', [0.55, 0, -1.2], BIG * 1.1, sy=BSY, brows='smug', look=[-0.3, -0.6])],
        cams=[cam(0.0, [-0.6, 1.4, 4.6], [-0.62, 1.42, 4.4], [-0.9, 1.25, -0.6], [-0.9, 1.26, -0.6], lens=46)])
st.shot('S17', 'chambre', actors=[act('mec', [-1.55, 0, -0.95], -60, 'sitFloor', 'sad')],
        props=[ROCK('rock', [-2.6, 0.45, -1.95], 3.6, brows='smug', look=[-0.2, -0.6])],
        cams=[cam(0.0, [-0.9, 1.35, 1.9], [-0.92, 1.36, 1.7], [-2.0, 0.85, -1.6], [-2.0, 0.86, -1.6], lens=46)])
# 18-20: the kennel, the collar, the name
KEN = P('ken', 'doghouse', pos=[-1.6, 0, -0.6], scale=2.2)
st.shot('S18', 'pavillon', actors=[act('mec', [-1.6, 0, -0.35], 0, 'sitFloor', 'sad')], props=[KEN, ROCK('rock', [2.4, 0, -3.2], BIG, sy=BSY, rot=[0, -0.5, 0], brows='smug', look=[-0.2, 0.8])],
        cams=[cam(0.0, [-1.3, 2.5, 3.95], [-1.32, 2.46, 3.7], [-1.55, 0.95, -0.45], [-1.55, 0.95, -0.45], lens=46)])
st.shot('S19', 'pavillon', actors=[act('mec', [-0.35, 0, 0.6], 15, 'stand', 'sad')],
        props=[KEN, P('collar', 'collar', on={'actor': 'mec', 'joint': 'head', 'offset': [0, -0.05, 0.0]}, opts={'text': 'CAILLOU'}), ROCK('rock', [1.5, 0, -1.6], BIG, sy=BSY, rot=[0, -0.45, 0], brows='smug', look=[-0.35, 0.7])],
        cams=[cam(0.0, [0.15, 1.5, 4.9], [0.14, 1.52, 4.65], [-0.3, 1.25, -0.4], [-0.3, 1.26, -0.4], lens=48)])
st.shot('S20', 'pavillon', actors=[act('mec', [-0.35, 0, 0.6], 0, 'stand', 'unimpressed', keys=[k(1.0, expr='sad')])],
        props=[P('collar', 'collar', on={'actor': 'mec', 'joint': 'head', 'offset': [0, -0.05, 0.0]}, opts={'text': 'CAILLOU'})],
        cams=[cam(0.0, [-0.3, 1.62, 1.32], [-0.3, 1.62, 1.29], [-0.35, 1.62, 0.6], [-0.35, 1.62, 0.6], lens=40), cam(0.78, [-0.3, 1.62, 1.29], [-0.3, 1.86, 1.9], [-0.35, 1.62, 0.6], [-0.35, 1.86, 0.6], lens=40, ease='inOut'),
              cam(1.55, [-0.3, 1.86, 1.9], [-0.3, 1.87, 1.82], [-0.35, 1.86, 0.6], [-0.35, 1.87, 0.6], lens=40)])
st.card('S02', 'GÉRARD'); st.card('S14', 'LA GROSSE TÊTE')
st.cue('sfx:choir', 'S01', 0.2, 0.25); st.cue('pop', 'S02', 0.6, 0.4); st.cue('sfx:bell', 'S03', 0.1, 0.35); st.cue('sfx:static', 'S04', 0.0, 0.12)
st.cue('sfx:paper', 'S05', 0.1, 0.45); st.cue('clack', 'S05', 0.55, 0.5); st.cue('sfx:fanfare', 'S06', 0.1, 0.35); st.cue('sfx:whistle', 'S07', SOLEIL - 0.05, 0.35)
st.cue('sfx:step', 'S08', 0.3, 0.3); st.cue('sfx:grunt', 'S09', 0.5, 0.3); st.cue('pop', 'S10', st.at('S10', 'L09', 3) - 0.1, 0.45)
[st.cue('clack', 'S11', t, 0.3) for t in (0.25, 0.6, 0.95, 1.3)]; st.cue('sfx:paper', 'S12', 0.1, 0.45); st.cue('clack', 'S12', 0.55, 0.5); st.cue('sfx:cash', 'S13', 0.75, 0.35)
st.cue('whoosh', 'S14', 0.2, 0.5, 1.0, 120, 1500); st.cue('thud', 'S14', 0.9, 0.6); st.cue('sfx:choir', 'S15', 0.1, 0.25); st.cue('thud', 'S16', 0.07, 0.45); st.cue('thud', 'S17', 0.07, 0.45)
st.cue('sfx:sniff', 'S18', 1.0, 0.3); st.cue('clink', 'S19', 0.4, 0.35) if False else st.cue('sfx:clink', 'S19', 0.4, 0.35); st.cue('sfx:clink', 'S20', 0.3, 0.35)
st.write('Le caillou', {
    'e1': {'preset': 'lyceen', 'seed': 31}, 'e2': {'preset': 'lyceenne', 'seed': 32}, 'e3': {'preset': 'lyceen', 'seed': 33, 'suit': '#C9822E'},
    'maitresse': {'preset': 'madame', 'glasses': True},
    **{f'q{i}': {'preset': p, 'seed': 50 + i} for i, p in enumerate(('mamie', 'tourist', 'femme', 'fermier', 'worker'))},
    'j1': {'preset': 'journaliste'}, 'j2': {'preset': 'lemec_brown', 'seed': 7}})
