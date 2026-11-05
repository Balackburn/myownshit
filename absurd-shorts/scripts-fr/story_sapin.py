#!/usr/bin/env python3
"""Le sapin: his Christmas tree is too tall, pierces the clouds, becomes a building with tenants, sheds, and ends up doing community service."""
from story_kit import *

st = Story('sapin')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 22)])
FIR = lambda h=2.6, **o: {'h': h, **o}
POLICE = P('police', 'noticeBoard', pos=[0.05, 2.2, -1.6], opts={'text': 'POLICE', 'style': 'sign', 'w': 1.1, 'h': 0.38, 'fg': '#FFFFFF', 'frame': '#FFFFFF'})
DOCCAM = [cam(0.0, [0.05, 1.55, 1.75], [0.05, 1.55, 1.55], [0, 1.5, 0], [0, 1.5, 0], lens=42)]
TALL = lambda sid, h=30, **kw: dict(set_='cottageStreet', props=[P('fir', 'giantFir', pos=[2, 0, -14], opts=FIR(h, windows=True, **kw))])

st.shot('S01', 'livingRoom', actors=[act('mec', [0.7, 0, 0.3], -20, 'handsOnHips', 'happy')], props=[P('fir', 'giantFir', pos=[-0.5, 0, -0.4], opts=FIR(2.5))], cams=WS(0.1, 0, h=1.4, d=4.2, look_h=1.3))
st.shot('S02', 'livingRoom', actors=[act('mec', [0.8, 0, 0.6], -20, 'lookUp', 'shocked')],
        props=[P('fir', 'giantFir', pos=[-0.4, 0, -0.4], opts=FIR(2.5), keys=[k(0.25, scale=1.7, dur=0.4, ease='outBack')]), P('rubble', 'rubble', pos=[-0.4, 2.7, -0.4], scale=0.25, opts={'n': 10, 'fly': 1, 'r': 1})],
        cams=[cam(0.0, [0.6, 0.5, 2.6], [0.55, 0.5, 2.4], [-0.3, 2.4, -0.4], [-0.3, 2.8, -0.4], lens=50, shake=0.04)])
st.shot('S03', 'cottageStreet', props=[P('fir', 'giantFir', pos=[2, 0, -14], opts=FIR(12), keys=[k(0.0, scale=0.55), k(0.1, scale=1.0, dur=0.6, ease='outBack')])],
        cams=[cam(0.0, [-1, 1.0, 6], [-1, 1.1, 5.4], [1.5, 6, -14], [1.5, 7, -14], lens=46, shake=0.02)])
st.shot('S04', 'skyHigh', setOpts={'layer': True}, props=[P('fir', 'giantFir', pos=[0, -14, 0], opts=FIR(48), keys=[k(0.0, to=[0, -4, 0], dur=st.dur('S04'), ease='out')])],
        cams=[cam(0.0, [9, 50, 34], [8.5, 51, 32], [0, 40, 0], [0, 43, 0], lens=44)])
st.shot('S05', 'office', actors=[act('maire', [0, 0, 0], 0, 'holdOut', 'suspicious')], props=[P('permis', 'noticeBoard', pos=[0.05, 1.4, 0.45], opts={'text': 'PERMIS\nDE CONSTRUIRE', 'style': 'doc', 'w': 0.55, 'h': 0.7, 'popAt': 0.15, 'textSize': 0.4})],
        cams=MS(0, 0, h=1.5, d=2.4))
st.shot('S06', 'office', props=[P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': 'ARRÊTÉ MUNICIPAL\nLE SAPIN DE M. DUPONT\nEST CLASSÉ', 'style': 'doc', 'w': 0.8, 'h': 1.0, 'textSize': 0.42}),
                                P('ok', 'noticeBoard', pos=[0.05, 1.3, 0.03], opts={'text': 'IMMEUBLE', 'style': 'sign', 'w': 0.55, 'h': 0.17, 'fg': '#C8322A', 'frame': '#C8322A', 'popAt': 0.3, 'tilt': 0.15})], cams=DOCCAM)
st.shot('S07', **TALL('S07'), cams=[cam(0.0, [-1.5, 1.2, 10], [-1.4, 1.4, 9.2], [1.5, 10, -14], [1.5, 13, -14], lens=46)])
st.shot('S08', 'cottageStreet', actors=[act('locataire', [0.7, 0, 0.2], -20, 'handsOnHips', 'smug')], props=[P('fir', 'giantFir', pos=[-1.2, -6, -1.6], opts=FIR(14, windows=True))], cams=MS(0.5, 0.2, h=1.6, d=2.8))
st.shot('S09', 'cottageStreet', props=[P('fir', 'giantFir', pos=[0, 0, -2], opts=FIR(10)), P('ph', 'noticeBoard', pos=[0.62, 9.3, -1.6], opts={'text': 'PENTHOUSE', 'style': 'sign', 'w': 1.0, 'h': 0.32, 'popAt': 0.25})],
        cams=[cam(0.0, [0.6, 9.6, 3.8], [0.5, 9.7, 3.4], [0.2, 9.6, -2], [0.2, 9.7, -2], lens=44)])
st.shot('S10', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'celebrate', 'happy')], props=[P(f'm{i}', 'moneySack', pos=[-0.7 + i * 0.7, 0, 0.5], opts={'color': '#5BB06E'}) for i in range(3)], cams=WS(0, 0, h=1.3, d=3.8, look_h=1.1))
st.shot('S11', 'cottageStreet', actors=[act('mec', [1.2, 0, 0.5], 90, 'pushCartWalk', 'smug', keys=[k(0.0, to=[1.9, 0, 0.5], dur=st.dur('S11'), clip='pushCartWalk')])],
        props=[P('fir', 'giantFir', pos=[0.75, 0.4, 0.5], rot=[0, 0, 1.5708], opts=FIR(2.2), keys=[k(0.0, to=[1.45, 0.4, 0.5], dur=st.dur('S11'))]), P('date', 'noticeBoard', pos=[-0.2, 2.0, -0.6], opts={'text': '7 JANVIER', 'style': 'sign', 'w': 0.9, 'h': 0.3, 'popAt': 0.2})],
        cams=WS(0.4, 0.3, h=1.3, d=5.2, look_h=0.9))
st.shot('S12', 'cottageStreet', actors=[act(a, [x, 0, 0], 0, 'holdSign', 'angry') for a, x in [('locataire', -0.75), ('locataire2', 0), ('locataire3', 0.75)]],
        props=[P(f's{i}', 'protestSign', opts={'text': t}, on={'actor': a, 'hand': 'R', **SIGN_UP}) for i, (a, t) in enumerate([('locataire', 'TOUCHE PAS\nÀ MON SAPIN'), ('locataire2', 'NON À\nL\'EXPULSION'), ('locataire3', 'SAPIN\nPOUR TOUS')])] +
              [P('fir', 'giantFir', pos=[2, 0, -14], opts=FIR(30, windows=True))], cams=WS(0, 0, h=1.6, d=6.5, look_h=1.6))
st.shot('S13', 'cottageStreet', actors=[act('locataire', [0, 0, 0], 0, 'angryFist', 'angry', keys=st.talk('L13', 'S13', 'angry'))], cams=CU(0, 0))
st.shot('S14', 'pressRoom', actors=[act('prefet', [0, 0, 0], 0, 'podiumTalk', 'suspicious')],
        props=[P('pod', 'podium', pos=[0, 0, 0.45]), P('decret', 'noticeBoard', pos=[0.42, 1.8, 0.35], opts={'text': 'ARRÊTÉ\nINTERDIT DE PERDRE\nSES AIGUILLES', 'style': 'doc', 'w': 0.62, 'h': 0.62, 'popAt': 0.3, 'textSize': 0.36})],
        cams=MS(0.2, 0, h=1.55, d=2.9))
st.shot('S15', 'cottageStreet', props=[P('fir', 'giantFir', pos=[0, 0, -2], opts=FIR(9, shed=[[0.05, True]]))], cams=[cam(0.0, [1.2, 0.4, 3.5], [1.1, 0.45, 3.2], [0, 4.0, -2], [0, 4.5, -2], lens=50)])
st.shot('S16', 'cottageStreet', actors=[act('locataire', [-1.0, 0, -0.5], 20, 'carryBox', 'sad', keys=[k(0.0, to=[-0.6, 0, 1.0], dur=st.dur('S16'), clip='carryBox')]),
                                        act('locataire2', [0.2, 0, -1.2], 10, 'carryBox', 'sad', keys=[k(0.0, to=[0.4, 0, 0.4], dur=st.dur('S16'), clip='carryBox')]),
                                        act('flic', [1.4, 0, 0.2], -40, 'point', 'suspicious')],
        props=[P('b1', 'cardboardBox', on={'actor': 'locataire', 'hand': 'R'}, scale=0.8), P('b2', 'cardboardBox', on={'actor': 'locataire2', 'hand': 'R'}, scale=0.8), P('fir', 'giantFir', pos=[2, 0, -14], opts=FIR(30, windows=True))],
        cams=WS(0.2, 0, h=1.5, d=6.8, look_h=1.2))
st.shot('S17', 'cottageStreet', actors=[act('noel', [0, 0, 0], 0, 'sit', 'worried', keys=[k(0.0, to=[0, 0.05, 0], dur=0.01)]), act('g1', [-0.62, 0, 0.1], 20, 'sit', 'happy', scale=0.7), act('g2', [0.62, 0, 0.1], -20, 'sit', 'smug', scale=0.7)],
        props=[P('bench', 'bench', pos=[0, 0, -0.15], scale=1.2)], cams=WS(0, 0, h=1.2, d=4.2, look_h=0.9))
st.shot('S18', 'office', actors=[act('noel', [-0.55, 0, 0.3], 40, 'explain', 'angry'), act('flic', [0.6, 0, -0.2], -40, 'clipboard', 'unimpressed')], props=[POLICE], cams=WS(0, 0, h=1.5, d=4.0, look_h=1.4))
st.shot('S19', **JUDGE(0.5, 'CONDAMNÉ', extra_props=[P('fir', 'giantFir', pos=[0.75, 0, -12.6], opts=FIR(1.3))]))
st.shot('S20', 'grassland', props=[P('fir', 'giantFir', pos=[0, 0, 0], opts=FIR(1.5, sway=0.06)), P('broom', 'broom', pos=[0.45, 0, 0.1], rot=[0, 0, 0.3]), P('cone', 'trafficCone', pos=[-0.7, 0, 0.4])],
        cams=[cam(0.0, [0.4, 0.9, 2.8], [0.35, 0.9, 2.6], [0, 0.8, 0], [0, 0.8, 0], lens=44)])
st.shot('S21', 'office', actors=[act('flic', [0.5, 0, 0.1], -20, 'stand', 'happy'), act('flic2', [-0.5, 0, 0.0], 20, 'stand', 'happy')],
        props=[POLICE, P('fir', 'giantFir', pos=[0, 0, -1.0], opts=FIR(1.6))], cams=WS(0, 0, h=1.5, d=4.4, look_h=1.3))
st.card('S05', 'PERMIS DE CONSTRUIRE'); st.card('S16', 'EXPULSION')
st.cue('thud', 'S02', 0.25, 0.8); st.cue('clang', 'S02', 0.3, 0.3); st.cue('thud', 'S03', 0.1, 0.7); st.cue('gust', 'S04', 0.0, 0.5, st.dur('S04'))
st.cue('thud', 'S05', 0.07, 0.45); st.cue('clack', 'S06', 0.3, 0.7); st.cue('sfx:bell', 'S07', 0.2, 0.3); st.cue('pop', 'S09', 0.25, 0.5)
st.cue('sfx:cash', 'S10', 0.2, 0.6); st.cue('pop', 'S11', 0.2, 0.5); st.cue('sfx:static', 'S12', 0.0, 0.2); st.cue('pop', 'S14', 0.3, 0.5)
st.cue('rain', 'S15', 0.05, 0.4, st.dur('S15')); st.cue('thud', 'S16', 0.07, 0.45); [st.cue('sfx:step', 'S16', t, 0.35) for t in (0.2, 0.6, 1.0)]
st.cue('thud', 'S19', 0.07, 0.45); st.cue('thud', 'S19', 0.5, 0.8); st.cue('gust', 'S20', 0.0, 0.25, st.dur('S20')); st.cue('sfx:sniff', 'S21', 0.4, 0.6)
st.write('Le sapin', {'maire': {'preset': 'boss'}, 'prefet': {'preset': 'commissaire'}, 'locataire': {'preset': 'femme'}, 'locataire2': {'preset': 'madame'}, 'locataire3': {'preset': 'worker'},
                      'noel': {'preset': 'lemec', 'atlas': 'lemec', 'atlasBody': False, 'suit': '#C8322A', 'pants': '#C8322A', 'lapel': '#F4F4F0', 'tie': '#F4F4F0', 'facial': 'beard', 'hairColor': '#F4F4F0', 'hair': 'curly', 'build': {'width': 0.95, 'belly': 0.14, 'headWidth': 1.3}},
                      'g1': {'preset': 'gamin'}, 'g2': {'preset': 'gamin', 'seed': 9}})
