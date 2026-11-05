#!/usr/bin/env python3
"""Le sable: three grains of Sardinian sand in his shoe start a diplomatic crisis; one grain grows into an island (tornado style)."""
from story_kit import *

st = Story('sable')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L09', 0), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L12', 0), ('S13', 'L13', 0), ('S14', 'L13', 5),
         ('S15', 'L14', 0), ('S16', 'L15', 0), ('S17', 'L16', 0), ('S18', 'L17', 0), ('S19', 'L18', 0), ('S20', 'L19', 0), ('S21', 'L20', 0), ('S22', 'L21', 0)])
GRAIN = {'color': '#E7D7A8', 'color2': '#EFE2BA', 'face': 'happy', 'bob': 0.01}
SHOE = lambda stages, **kw: [P('shoe', 'bigShoe', pos=[0, 0, 0], scale=3.0), P('isle', 'growIsland', pos=[0.05, 0.36, 0], scale=3.0, opts={'stages': stages}, **kw)]
SHOECAM = [cam(0.0, [0.55, 0.85, 1.55], [0.5, 0.82, 1.4], [0.05, 0.38, 0], [0.05, 0.38, 0], lens=42)]
POL = lambda sid, lid: dict(set_='pressRoom', actors=[act('ministre', [0, 0, 0], 0, 'podiumTalk', 'angry', keys=st.talk(lid, sid, 'angry'))],
                            props=[P('pod', 'podium', pos=[0, 0, 0.45])], cams=MS(0, 0, h=1.55, d=2.6))

st.shot('S01', 'runway', actors=[act('mec', [0, 0, -3.0], 0, 'walk', 'happy', keys=[k(0.0, to=[0, 0, -0.8], dur=st.dur('S01'), clip='walk')])],
        props=[P('plane', 'plane', pos=[-2, 2.2, -16], rot=[0, 0.5, 0]), P('bag', 'briefcase', on={'actor': 'mec', 'hand': 'R'})],
        cams=[cam(0.0, [0.5, 0.5, 2.6], [0.5, 0.52, 3.6], [0, 1.6, -3.0], [0, 1.6, -0.8], lens=50)])
st.shot('S02', 'runway', props=[P('shoe', 'bigShoe', pos=[0, 0, 0], scale=2.2)] + [P(f'g{i}', 'growIsland', pos=[x, 0.29, z], scale=3.0, opts={'stages': [[0, 0]]}) for i, (x, z) in enumerate([(-0.08, 0.02), (0.02, -0.03), (0.1, 0.03)])],
        cams=[cam(0.0, [0.5, 0.75, 1.25], [0.46, 0.72, 1.12], [0.0, 0.24, 0], [0.0, 0.24, 0], lens=40)])
st.shot('S03', 'office', actors=[act('mec', [0.55, 0, -0.6], -20, 'stand', 'unimpressed'), act('chien', [-0.45, 0, 0.2], 60, 'angry')],
        cams=WS(0.0, -0.2, h=1.0, d=4.0, look_h=0.8))
st.shot('S04', 'office', actors=[act('flic', [0, 0, 0], 0, 'point', 'suspicious', keys=st.talk('L04', 'S04', 'suspicious'))], cams=CU(0, 0, dx=0.3))
st.shot('S05', 'office', props=[P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': 'REPUBBLICA ITALIANA\nRESTITUZIONE\n3 GRANI DI SABBIA', 'style': 'doc', 'w': 0.8, 'h': 1.0, 'popAt': 0.15, 'textSize': 0.4, 'stamp': 'URGENTE'})],
        cams=[cam(0.0, [0.05, 1.55, 1.75], [0.05, 1.55, 1.55], [0, 1.5, 0], [0, 1.5, 0], lens=42)])
st.shot('S06', 'runway', props=[P('jet', 'plane', pos=[-8, 2.0, -6], rot=[0, 0, 0], scale=0.55, opts={'livery': '#C9A227'}, keys=[k(0.0, to=[8, 5.0, -6], dur=st.dur('S06'), ease='linear'), k(0.3, rotTo=[0, 0, 0.25], dur=0.5)])],
        cams=[cam(0.0, [-2, 0.9, 10], [2, 1.2, 9], [-6, 2.4, -6], [8, 5.2, -6], lens=44)])
st.shot('S07', 'skyHigh', setOpts={'layer': True},
        props=[P('jet', 'plane', pos=[-20, 60, 0], scale=0.55, opts={'livery': '#C9A227'}, keys=[k(0.0, to=[20, 60, 0], dur=st.dur('S07'))]),
               P('f1', 'fighterJet', pos=[-24, 64.5, -8], rot=[0, 1.5708, 0], scale=0.7, keys=[k(0.0, to=[16, 64.5, -8], dur=st.dur('S07'))]),
               P('f2', 'fighterJet', pos=[-24, 55.8, -8], rot=[0, 1.5708, 0], scale=0.7, keys=[k(0.0, to=[16, 55.8, -8], dur=st.dur('S07'))])],
        cams=[cam(0.0, [-18, 61.0, 52], [22, 61.0, 52], [-21, 60.2, -3], [19, 60.2, -3], lens=40, shake=0.02)])
st.shot('S08', 'office', props=[P('tray', 'noticeBoard', pos=[0, 0.95, 0], rot=[-1.5708, 0, 0], opts={'text': ' ', 'style': 'sign', 'w': 0.7, 'h': 0.5, 'frame': '#C8322A'})] +
        [P(f'g{i}', 'growIsland', pos=[x, 0.97, z], scale=3.0, opts={'stages': [[0, 0]]}) for i, (x, z) in enumerate([(-0.08, 0.0), (0.08, 0.02)])] +
        [P('loupe', 'magnifyingGlass', pos=[0.18, 1.05, 0.12], rot=[0, 0, 0.4], scale=1.4)], cams=TOP(0, 0, h=1.75, look_h=0.95))
st.shot('S09', **POL('S09', 'L09'), fx=[{'type': 'flash', 'at': 0.2, 'dur': 0.08}])
st.shot('S10', 'parisStreet', actors=[act('mec', [7, 0, 0], 0, 'lookItem', 'surprised')],
        props=[P('grain', 'cloudChar', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.12, 0.1]}, scale=0.14, opts=GRAIN)], cams=CU(7, 0, h=1.62, dx=0.35))
st.shot('S11', 'parisStreet', actors=[act('mec', [7, 0, 0], 0, 'lookItem', 'sad', keys=st.talk('L11', 'S11', 'sad'))],
        props=[P('grain', 'cloudChar', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.12, 0.1]}, scale=0.14, opts={**GRAIN, 'face': 'grumpy'})], cams=MS(7, 0, h=1.5, d=2.2))
st.shot('S12', **JUDGE(0.45, 'GARDE PARTAGÉE'))
st.shot('S13', 'seaSurface', props=[P('grain', 'cloudChar', pos=[0, 0.02, 9.0], scale=0.12, opts={**GRAIN, 'face': 'happy'}), P('para', 'parasol', pos=[0.6, 0, 8.3], scale=0.12)],
        cams=[cam(0.0, [0.15, 0.12, 9.7], [0.12, 0.12, 9.6], [0, 0.08, 9.0], [0, 0.08, 9.0], lens=40)])
st.shot('S14', 'office', props=[P('shoe', 'bigShoe', pos=[0, 0, 0], scale=3.0), P('grain', 'cloudChar', pos=[0.05, 0.36, 0], scale=0.12, opts={**GRAIN, 'face': 'smug'})], cams=SHOECAM)
st.shot('S15', 'office', props=SHOE([[0, 0], [0.35, 1]]), cams=SHOECAM)
st.shot('S16', 'office', props=SHOE([[0, 1]]), cams=SHOECAM)
st.shot('S17', 'office', props=SHOE([[0, 1], [0.15, 2]]), cams=SHOECAM)
st.shot('S18', 'office', props=SHOE([[0, 2], [0.15, 3]]), cams=SHOECAM)
st.shot('S19', **POL('S19', 'L18'))
st.shot('S20', 'parisStreet', actors=[act('mec', [7, 0, 0], 10, 'stand', 'unimpressed')],
        props=[P('isle', 'growIsland', on={'actor': 'mec', 'joint': 'footR', 'offset': [0, 0.1, 0.05]}, scale=1.6, opts={'stages': [[0, 3]]})],
        cams=[cam(0.0, [7.45, 0.35, 1.5], [7.4, 0.36, 1.35], [7.0, 0.35, 0], [7.0, 0.37, 0], lens=44)])
st.shot('S21', 'parisStreet', actors=[act('mec', [7, 0, 2.5], 180, 'walk', 'sad', keys=[k(0.0, to=[7, 0, 0.2], dur=st.dur('S21'), clip='sneak')])],
        props=[P('isle', 'growIsland', on={'actor': 'mec', 'joint': 'footR', 'offset': [0, 0.1, 0.05]}, scale=1.6, opts={'stages': [[0, 3]]})],
        cams=[cam(0.0, [6.4, 0.6, -2.6], [6.4, 0.6, -2.8], [7, 0.9, 2.5], [7, 0.9, 0.2], lens=44)])
st.shot('S22', 'poste', actors=[act('mec', [0, 0, 0.6], 180, 'giveItem', 'unimpressed')],
        props=[P('tax', 'noticeBoard', pos=[0.22, 1.7, 0.0], rot=[0, 3.1416, 0], opts={'text': 'TAXE DE SÉJOUR\n2 €', 'style': 'tag', 'w': 0.6, 'h': 0.36, 'popAt': 0.5}),
               P('coin', 'coin', on={'actor': 'mec', 'hand': 'R'}, scale=2.0)],
        cams=[cam(0.0, [0.4, 1.6, -1.8], [0.38, 1.6, -1.6], [0.1, 1.5, 0.6], [0.1, 1.5, 0.6], lens=44)])
st.card('S04', 'CONTREBANDE'); st.card('S12', 'GARDE PARTAGÉE')
st.cue('engine', 'S01', 0.0, 0.25, st.dur('S01')); [st.cue('sfx:step', 'S01', t, 0.4) for t in (0.3, 0.8, 1.3)]
[st.cue('pop', 'S02', t, 0.25) for t in (0.2, 0.35, 0.5)]
st.cue('sfx:roar', 'S03', 0.35, 0.25); st.cue('sfx:roar', 'S03', 0.9, 0.25)
st.cue('thud', 'S04', 0.07, 0.45); st.cue('pop', 'S05', 0.15, 0.5); st.cue('sfx:paper', 'S05', 0.12, 0.5)
st.cue('sfx:jet', 'S06', 0.0, 0.5); st.cue('sfx:jet', 'S07', 0.0, 0.45); st.cue('whoosh', 'S07', 0.2, 0.35, 1.2, 300, 2500)
st.cue('sfx:gasp', 'S08', 0.4, 0.6); [st.cue('clack', 'S09', t, 0.35) for t in (0.2, 0.5, 0.75)]
st.cue('thud', 'S12', 0.07, 0.45); st.cue('thud', 'S12', 0.45, 0.8); st.cue('gust', 'S13', 0.0, 0.3, st.dur('S13'))
st.cue('pop', 'S15', 0.35, 0.6); st.cue('pop', 'S17', 0.15, 0.6); st.cue('thud', 'S17', 0.15, 0.5); st.cue('pop', 'S18', 0.15, 0.6); st.cue('gust', 'S18', 0.15, 0.25, 1.0)
[st.cue('sfx:step', 'S21', t, 0.45) for t in (0.2, 0.7, 1.2)]; st.cue('pop', 'S22', 0.5, 0.6); st.cue('sfx:cash', 'S22', 0.6, 0.5)
st.write('Le sable', {'ministre': {'preset': 'politique'}, 'chien': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 4}}})
