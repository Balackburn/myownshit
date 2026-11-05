#!/usr/bin/env python3
"""Le changement d'heure: he refuses the clock change, arrives an hour early everywhere, gets promoted; France splits into two time zones;
Europe abolishes the change, he is decorated, and the next day he switches to winter time: alone at the office again."""
from story_kit import *

st = Story('heure')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])
DOCCAM = [cam(0.0, [0.05, 1.55, 1.75], [0.05, 1.55, 1.55], [0, 1.5, 0], [0, 1.5, 0], lens=42)]
CLOCKCAM = [cam(0.0, [0.1, 1.15, 1.5], [0.1, 1.15, 1.3], [0, 1.05, 0], [0, 1.05, 0], lens=42)]
EMPTY = lambda: [P(f'ch{i}', 'officeChair', pos=[-1.4 + i * 1.4, 0, -0.8]) for i in range(3)]
COLL = [('c1', -0.9), ('c2', 0.0), ('c3', 0.9)]

st.shot('S01', 'chambre', actors=[act('mec', [0.35, 0, 0], -20, 'shakeHead', 'smug')], props=[P('clock', 'alarmClock', pos=[-0.45, 0.75, 0.2], scale=0.9, opts={'time': '02:59', 'time2': '03:00', 'switchAt': 0.6})],
        cams=WS(0, 0, h=1.4, d=3.6, look_h=1.1))
st.shot('S02', 'chambre', props=[P('clock', 'alarmClock', pos=[0, 0.7, 0], scale=1.2, opts={'time': '09:00'}), P('ete', 'noticeBoard', pos=[0.42, 1.25, 0.05], opts={'text': "HEURE D'ÉTÉ", 'style': 'tag', 'w': 0.5, 'h': 0.2, 'popAt': 0.3})], cams=CLOCKCAM)
st.shot('S03', 'office', actors=[act('mec', [0.4, 0, 2.0], 180, 'walk', 'happy', keys=[k(0.0, to=[0.3, 0, 0.3], dur=st.dur('S03'), clip='walk')])], props=EMPTY() + [P('clock', 'wallClock', pos=[1.2, 2.1, -1.4], scale=1.2)],
        cams=[cam(0.0, [1.3, 1.5, -2.4], [1.3, 1.5, -2.7], [0.4, 1.3, 2.0], [0.3, 1.3, 0.3], lens=44)])
st.shot('S04', 'office', actors=[act('mec', [0, 0, 0], 0, 'stand', 'unimpressed')], props=EMPTY(), cams=WS(0, 0, h=1.6, d=5.0, look_h=1.2))
st.shot('S05', 'office', actors=[act('mec', [0, 0, 0], 0, 'explain', 'worried')], props=[P(f'pp{i}', 'paperPile', pos=[-1.3 + i * 0.65, 0, 0.6 - (i % 2) * 1.4], scale=0.01, keys=[k(0.1 + i * 0.1, scale=1.4, dur=0.25, ease='outBack')]) for i in range(5)],
        cams=WS(0, 0, h=1.6, d=5.2, look_h=1.0))
st.shot('S06', 'office', actors=[act('mec', [0, 0, 0], 0, 'handsOnHips', 'smug')], props=[P('dir', 'noticeBoard', pos=[0.3, 1.15, 0.5], opts={'text': 'DIRECTEUR', 'style': 'sign', 'w': 0.6, 'h': 0.2, 'popAt': 0.2, 'fg': '#E8B830', 'frame': '#E8B830'})],
        cams=MS(0.15, 0, h=1.5, d=2.6))
st.shot('S07', 'office', actors=[act(a, [x, 0, 1.2], 180, 'stand', 'suspicious') for a, x in COLL] + [act('mec', [0, 0, -0.6], 0, 'stand', 'smug')],
        cams=[cam(0.0, [0.3, 1.6, -3.4], [0.28, 1.6, -3.2], [0, 1.4, 0.6], [0, 1.4, 0.6], lens=44)])
st.shot('S08', 'office', actors=[act(a, [x, 0, 0], 0, 'showPhone', 'happy') for a, x in COLL], props=[P(f'w{i}', 'bigWatch', on={'actor': a, 'hand': 'R'}, scale=1.4, opts={'time': '09:00'}) for i, (a, x) in enumerate(COLL)],
        cams=WS(0, 0, h=1.5, d=4.4, look_h=1.3))
st.shot('S09', 'parisStreet', actors=[act(f'p{i}', [6.4 + (i % 2) * 1.0, 0, -1 - i * 1.2], 0, 'walk', 'happy', keys=[k(0.0, to=[6.4 + (i % 2) * 1.0, 0, 0.4 - i * 1.2], dur=st.dur('S09'), clip='walk')]) for i in range(3)],
        props=[P('clock', 'wallClock', pos=[9.8, 4.2, -2], rot=[0, -1.5708, 0], scale=3.0)], cams=LOW(7, 0, d=5.2, look_h=2.2))
st.shot('S10', 'skyHigh', setOpts={'layer': False, 'fog': False}, props=[P('map', 'splitMap', pos=[0, 0, 0], opts={'k': 10, 'west': '#F2C94C', 'east': '#F2C94C'})],
        cams=[cam(0.0, [6, 190, 40], [5, 170, 34], [1, 0, -2], [1, 0, -2], lens=42)], fog=None)
st.shot('S11', 'skyHigh', setOpts={'layer': False, 'fog': False}, props=[P('map', 'splitMap', pos=[0, 0, 0], opts={'k': 10})],
        cams=[cam(0.0, [5, 165, 34], [4, 150, 30], [1, 0, -2], [1, 0, -2], lens=42)], fog=None)
st.shot('S12', 'parisStreet', actors=[act('flic', [3.9, 0, 31.3], 160, 'holdOut', 'unimpressed')],
        props=[P('gate', 'barrierGate', pos=[5.2, 0, 30.0], rot=[0, 3.1416, 0], opts={'length': 5.0, 'angle': 0, 'sign': 'FRONTIÈRE HORAIRE'}), P('w', 'bigWatch', on={'actor': 'flic', 'hand': 'R'}, scale=2.0, opts={'time': '10:00'})],
        cams=[cam(0.0, [1.6, 1.4, 36.0], [1.8, 1.4, 35.5], [3.8, 1.5, 30.5], [3.8, 1.5, 30.5], lens=44)])
st.shot('S13', 'runway', props=[P('train', 'train', pos=[-30, 0, -4], opts={'cars': 3, 'speed': 22}),
                                 P('board', 'noticeBoard', pos=[1.6, 2.2, 0.5], opts={'text': 'ARRIVÉE  9:00\nDÉPART  10:00', 'style': 'sign', 'w': 1.6, 'h': 0.7, 'popAt': 0.4})],
        cams=[cam(0.0, [3.0, 1.6, 8.5], [2.8, 1.6, 8.2], [-1.5, 1.4, -3.5], [-1.5, 1.4, -3.5], lens=44)])
st.shot('S14', 'grassland', actors=[act('vache', [-0.6, 0, 0], 30, 'idle'), act('vache2', [0.9, 0, -0.4], -30, 'idle')],
        props=[P('cl1', 'wallClock', pos=[-1.6, 1.8, -1.4], scale=1.4, opts={'rate': 0.2}), P('cl2', 'wallClock', pos=[1.8, 1.8, -1.6], scale=1.4, opts={'rate': -0.2})], cams=WS(0, 0, h=1.4, d=5.6, look_h=1.0))
st.shot('S15', 'pressRoom', actors=[act('euro', [0, 0, 0], 0, 'podiumTalk', 'suspicious')], props=[P('pod', 'podium', pos=[0, 0, 0.45]), P('flag', 'flag', pos=[-0.9, 0, -0.3], scale=1.3, opts={'colors': ['#003399', '#FFCC00', '#003399']})],
        cams=MS(0, 0, h=1.55, d=3.0))
st.shot('S16', 'office', props=[P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': "DIRECTIVE EUROPÉENNE\nCHANGEMENT D'HEURE", 'style': 'doc', 'w': 0.8, 'h': 1.0, 'textSize': 0.3}),
                                P('stamp', 'noticeBoard', pos=[0.05, 1.3, 0.03], opts={'text': 'ABOLI', 'style': 'sign', 'w': 0.5, 'h': 0.18, 'fg': '#C8322A', 'frame': '#C8322A', 'popAt': 0.3, 'tilt': 0.15})], cams=DOCCAM)
st.shot('S17', 'pressRoom', actors=[act('mec', [0, 0, 0], 0, 'heroPose', 'smug')], props=[P('medal', 'medal', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.08, 0.35, 0.16]}, scale=2.0)], cams=MS(0, 0, h=1.5, d=2.6))
st.shot('S18', 'chambre', actors=[act('mec', [0.35, 0, 0], -20, 'pointDown', 'smug')], props=[P('clock', 'alarmClock', pos=[-0.4, 0.75, 0.3], scale=0.9, opts={'time': '09:00', 'time2': '08:00', 'switchAt': 0.7})],
        cams=WS(0, 0, h=1.3, d=3.4, look_h=1.0))
st.shot('S19', 'office', actors=[act('mec', [0, 0, 0], 0, 'stand', 'unimpressed', keys=[k(1.0, expr='sad')])], props=EMPTY(), cams=WS(0, 0, h=1.6, d=6.0, look_h=1.2))
st.card('S04', 'SEUL'); st.card('S11', 'DEUX FRANCE')
st.cue('sfx:ring', 'S01', 0.6, 0.5); st.cue('pop', 'S02', 0.3, 0.5); [st.cue('sfx:step', 'S03', t, 0.4) for t in (0.2, 0.7, 1.2)]; st.cue('thud', 'S04', 0.07, 0.45)
[st.cue('pop', 'S05', 0.1 + 0.1 * i, 0.35) for i in range(5)]; st.cue('pop', 'S06', 0.2, 0.5); st.cue('sfx:fanfare', 'S06', 0.25, 0.3); st.cue('sfx:ticks', 'S08', 0.0, 0.35)
st.cue('whoosh', 'S10', 0.0, 0.35, 1.2, 200, 1800); st.cue('thud', 'S11', 0.07, 0.45); st.cue('clack', 'S12', 0.3, 0.4); st.cue('engine', 'S13', 0.0, 0.5, st.dur('S13')); st.cue('whoosh', 'S13', 0.4, 0.6, 0.8, 300, 3000)
st.cue('sfx:ticks', 'S14', 0.0, 0.35); st.cue('clack', 'S16', 0.3, 0.7); st.cue('sfx:fanfare', 'S17', 0.1, 0.4); st.cue('sfx:ring', 'S18', 0.7, 0.4)
st.write("Le changement d'heure", {'c1': {'preset': 'madame'}, 'c2': {'preset': 'boss'}, 'c3': {'preset': 'worker'}, 'p0': {'preset': 'femme'}, 'p1': {'preset': 'tourist'}, 'p2': {'preset': 'mamie'},
                                   'vache': {'type': 'creature', 'name': 'cow', 'opts': {'seed': 2}}, 'vache2': {'type': 'creature', 'name': 'cow', 'opts': {'seed': 7}}, 'euro': {'preset': 'politique', 'seed': 33}})
