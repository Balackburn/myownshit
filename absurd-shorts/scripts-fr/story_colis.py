#!/usr/bin/env python3
"""L'avis de passage: he waits home all day and still gets a delivery slip; the court summons comes as a slip; eleven years in the post office
queue; he takes the clerk's place, becomes a postman, delivers his own parcel, and he isn't home."""
from story_kit import *

st = Story('colis')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 22)])
CAP = lambda a: P(f'cap_{a}', 'copCap', on={'actor': a, 'joint': 'head', 'offset': [0, 0.45, 0.0]}, opts={'color': '#2C4A8A'})
DOOR = lambda x=0, z=-1.2: P('door', 'door', pos=[x, 0, z], opts={'w': 0.95, 'h': 2.1})
DOCCAM = [cam(0.0, [0.05, 1.55, 1.75], [0.05, 1.55, 1.55], [0, 1.5, 0], [0, 1.5, 0], lens=42)]
QUEUE = lambda n=4, z0=0.8: [act(f'c{i}', [0.9 * (i % 2) - 0.3, 0, z0 + i * 0.9], 180, 'idle', 'unimpressed') for i in range(n)]

st.shot('S01', 'livingRoom', actors=[act('mec', [0.4, 0, 0], -10, 'stand', 'happy')], props=[DOOR(-0.6, -1.3)], cams=WS(0, 0, h=1.4, d=4.2, look_h=1.2))
st.shot('S02', 'livingRoom', actors=[act('mec', [0.4, 0, 0], -150, 'stand', 'neutral', keys=[k(0.8, expr='sleepy')])],
        props=[DOOR(-0.3, -1.3), P('clock', 'wallClock', pos=[1.0, 2.0, -1.35], scale=1.2, opts={'rate': 4})], cams=[cam(0.0, [1.4, 1.5, 2.6], [1.35, 1.5, 2.4], [0.2, 1.4, -0.8], [0.2, 1.4, -0.8], lens=44)])
st.shot('S03', 'livingRoom', props=[DOOR(0, -1.0), P('avis', 'avisPassage', pos=[0, 0.07, -0.95], rot=[-1.5708, 0, 0], scale=2.5, keys=[k(0.15, to=[0.05, 0.07, -0.5], dur=0.35, ease='out')])],
        cams=[cam(0.0, [0.3, 0.7, 0.9], [0.28, 0.68, 0.8], [0.0, 0.35, -0.9], [0.0, 0.33, -0.9], lens=44)])
st.shot('S04', 'cottageStreet', actors=[act('facteur', [0, 0, 0], 0, 'shrug', 'unimpressed', keys=st.talk('L04', 'S04', 'unimpressed'))], props=[CAP('facteur')], cams=CU(0, 0, h=1.8))
st.shot('S05', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'writeOnHeld', 'angry')], props=[P('clip', 'clipboardProp', on={'actor': 'mec', 'hand': 'L'})], cams=MS(0, 0, h=1.45, d=2.6))
st.shot('S06', 'office', props=[P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': 'CONVOCATION\nAU TRIBUNAL\nAFFAIRE : LA POSTE', 'style': 'doc', 'w': 0.8, 'h': 1.0, 'popAt': 0.15, 'textSize': 0.42})], cams=DOCCAM)
st.shot('S07', 'livingRoom', props=[DOOR(0, -1.0), P('avis', 'avisPassage', pos=[0, 0.07, -0.95], rot=[-1.5708, 0, 0], scale=2.5, opts={'title': 'TRIBUNAL'}, keys=[k(0.1, to=[0.05, 0.07, -0.5], dur=0.35, ease='out')])],
        cams=[cam(0.0, [0.3, 0.7, 0.9], [0.28, 0.68, 0.8], [0.0, 0.35, -0.9], [0.0, 0.33, -0.9], lens=44)])
st.shot('S08', 'poste', actors=[act('mec', [0.6, 0, 2.4], 180, 'walk', 'determined' if False else 'angry', keys=[k(0.0, to=[0.4, 0, 0.6], dur=st.dur('S08'), clip='walk')])],
        cams=[cam(0.0, [0.2, 1.5, 5.2], [0.2, 1.5, 4.8], [0.3, 1.2, 0], [0.3, 1.2, 0], lens=44)])
st.shot('S09', 'poste', props=[P('tk', 'queueTicket', pos=[0, 1.5, 0.6], scale=4.0, opts={'num': '4012'})],
        cams=[cam(0.0, [0.05, 1.5, 1.62], [0.05, 1.5, 1.46], [0, 1.5, 0.6], [0, 1.5, 0.6], lens=42)])
st.shot('S10', 'poste', props=[P('disp', 'queueDisplay', pos=[0, 2.0, -2.6], scale=1.2, opts={'num': '1'})], cams=[cam(0.0, [0.2, 1.8, 0.9], [0.2, 1.82, 0.6], [0, 1.95, -2.6], [0, 1.95, -2.6], lens=42)])
st.shot('S11', 'poste', setOpts={'clockRate': 6}, actors=[act('mec', [0, 0, 0.8], 180, 'idle', 'sleepy')] + QUEUE(3, 1.8), cams=[cam(0.0, [0.4, 1.5, -1.6], [0.38, 1.5, -1.4], [0.1, 1.4, 1.2], [0.1, 1.4, 1.2], lens=44)])
st.shot('S12', 'poste', actors=[act('mec', [-0.3, 0, 0.8], 160, 'stand', 'happy'), act('femme', [0.3, 0, 0.8], 200, 'stand', 'happy')],
        props=[P('h', 'heart', pos=[0, 2.25, 0.8], scale=0.6, keys=[k(0.0, scale=0.01), k(0.2, scale=0.6, dur=0.3, ease='outBack')])], cams=[cam(0.0, [0.3, 1.5, -1.6], [0.28, 1.5, -1.4], [0, 1.45, 0.8], [0, 1.45, 0.8], lens=44)])
st.shot('S13', 'poste', actors=[act('mec', [-0.3, 0, 0.8], 160, 'stand', 'happy'), act('femme', [0.3, 0, 0.8], 200, 'stand', 'happy'),
                                act('g1', [-0.6, 0, 1.5], 170, 'stand', 'happy', scale=0.45, keys=[k(0.2, scale=0.85, dur=0.8, ease='outBack')]),
                                act('g2', [0.6, 0, 1.5], 190, 'stand', 'smug', scale=0.4, keys=[k(0.35, scale=0.8, dur=0.8, ease='outBack')])],
        cams=[cam(0.0, [0.3, 1.5, -2.6], [0.28, 1.5, -2.4], [0, 1.2, 1.0], [0, 1.2, 1.0], lens=44)])
st.shot('S14', 'poste', props=[P('disp', 'queueDisplay', pos=[0, 2.0, -2.6], scale=1.2, opts={'num': '4010', 'num2': '4011', 'switchAt': 0.3})], cams=[cam(0.0, [0.2, 1.8, 0.9], [0.2, 1.82, 0.6], [0, 1.95, -2.6], [0, 1.95, -2.6], lens=42)])
st.shot('S15', 'poste', actors=[act('guichetiere', [0, 0, -2.0], 0, 'walk', 'unimpressed', keys=[k(0.0, to=[1.6, 0, -2.0], dur=st.dur('S15'), clip='walk')])],
        props=[P('pause', 'noticeBoard', pos=[-0.4, 1.55, -2.3], opts={'text': 'PAUSE', 'style': 'sign', 'w': 0.6, 'h': 0.22, 'popAt': 0.3})], cams=[cam(0.0, [0.0, 1.5, 1.4], [0.0, 1.5, 1.2], [0, 1.3, -2.2], [0, 1.3, -2.2], lens=44)])
st.shot('S16', 'poste', actors=[act('mec', [0, 0, -2.0], 0, 'handsOnHips', 'smug')], cams=[cam(0.0, [0.25, 1.6, 0.3], [0.22, 1.6, 0.1], [0, 1.5, -2.0], [0, 1.52, -2.0], lens=44)])
st.shot('S17', 'poste', actors=QUEUE(4, -0.6), cams=[cam(0.0, [0.25, 1.55, -3.3], [0.25, 1.55, -3.1], [0.15, 1.35, 0.8], [0.15, 1.35, 0.8], lens=54)])
st.shot('S18', 'cottageStreet', actors=[act('mecFacteur', [0, 0, 0], 0, 'heroPose', 'smug')], props=[CAP('mecFacteur'), P('bike', 'bicycle', pos=[0.9, 0, -0.2], rot=[0, 0.4, 0])], cams=LOW(0.2, 0, d=3.2, look_h=1.4))
st.shot('S19', 'cottageStreet', actors=[act('mecFacteur', [0, 0, 0.6], 180, 'holdOut', 'happy')], props=[CAP('mecFacteur'), DOOR(0, -0.2), P('box', 'cardboardBox', on={'actor': 'mecFacteur', 'hand': 'R'}, scale=0.8)],
        cams=[cam(0.0, [1.45, 1.65, 3.1], [1.35, 1.65, 2.9], [0, 1.45, 0.2], [0, 1.45, 0.2], lens=44)])
st.shot('S20', 'livingRoom', props=[DOOR(-0.6, -1.3)], cams=[cam(0.0, [0.5, 1.5, 3.2], [0.45, 1.5, 3.0], [0, 1.3, -1.0], [0, 1.3, -1.0], lens=44)])
st.shot('S21', 'cottageStreet', actors=[act('mecFacteur', [0, 0, 0.6], 180, 'writeOnHeld', 'unimpressed')],
        props=[CAP('mecFacteur'), DOOR(0, -0.2), P('avis', 'avisPassage', pos=[0.05, 1.3, -0.15], scale=2.0, keys=[k(0.0, scale=0.01), k(0.7, scale=2.0, dur=0.3, ease='outBack')])],
        cams=[cam(0.0, [1.85, 1.65, 2.5], [1.8, 1.65, 2.35], [0, 1.45, -0.1], [0, 1.45, -0.1], lens=44)])
st.card('S03', 'AVIS DE PASSAGE'); st.card('S09', 'N° 4012')
st.cue('sfx:ticks', 'S02', 0.0, 0.4); st.cue('sfx:paper', 'S03', 0.15, 0.6); st.cue('thud', 'S03', 0.07, 0.45); [st.cue('sfx:step', 'S04', t, 0.35) for t in (0.3, 0.8)]
st.cue('sfx:paper', 'S05', 0.3, 0.4); st.cue('pop', 'S06', 0.15, 0.5); st.cue('sfx:paper', 'S07', 0.1, 0.6); [st.cue('sfx:step', 'S08', t, 0.35) for t in (0.2, 0.7, 1.2)]
st.cue('thud', 'S09', 0.07, 0.45); st.cue('sfx:bell', 'S10', 0.15, 0.4); st.cue('sfx:ticks', 'S11', 0.0, 0.4); st.cue('sfx:choir', 'S12', 0.2, 0.25); st.cue('pop', 'S12', 0.2, 0.4)
st.cue('pop', 'S13', 0.2, 0.4); st.cue('pop', 'S13', 0.35, 0.4); st.cue('sfx:bell', 'S14', 0.3, 0.5); st.cue('pop', 'S15', 0.3, 0.5); st.cue('sfx:bell', 'S19', 0.5, 0.5)
st.cue('sfx:bell', 'S20', 0.2, 0.4); st.cue('pop', 'S21', 0.7, 0.6); st.cue('sfx:paper', 'S21', 0.7, 0.5)
st.write("L'avis de passage", {'facteur': {'preset': 'worker', 'atlasBody': False, 'suit': '#F2C230', 'pants': '#2C4A8A'}, 'femme': {'preset': 'femme'}, 'guichetiere': {'preset': 'madame', 'suit': '#2C4A8A'},
                               'g1': {'preset': 'gamin'}, 'g2': {'preset': 'lyceenne'}, 'c0': {'preset': 'mamie'}, 'c1': {'preset': 'tourist'}, 'c2': {'preset': 'worker', 'seed': 31}, 'c3': {'preset': 'boss'},
                               'mecFacteur': {'preset': 'lemec', 'atlas': 'lemec', 'atlasBody': False, 'suit': '#F2C230', 'pants': '#2C4A8A', 'lapel': '#2C4A8A', 'tie': '#2C4A8A', 'build': {'width': 0.82, 'headWidth': 1.3}}})
