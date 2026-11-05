#!/usr/bin/env python3
"""Le sable: back from Sardinia with one grain of sand in his shoe; a 3,000 euro fine; two carabinieri search the shoe for three days
and find forty grains, thirty-nine from Brittany; France claims its own; a 39-for-1 swap at the border under fighter escort;
he auctions the shoe, Italy buys it, and he pays the fine with the money."""
from story_kit import *

st = Story('sable')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L08', 5), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L12', 0), ('S14', 'L13', 0),
         ('S15', 'L14', 0), ('S16', 'L15', 0), ('S17', 'L16', 0), ('S18', 'L17', 0), ('S19', 'L17', 7), ('S20', 'L18', 0), ('S21', 'L19', 0), ('S22', 'L20', 0)])
BZH, SARD = '#D6D0BE', '#E3BE6E'                       # Breton grains are pale grey-white, the Sardinian one golden
DESK = 0.76                                            # table top
TABLE = lambda x=0, z=0, **kw: P('table', 'table', pos=[x, 0, z], opts={'w': 1.2, 'd': 0.8, **kw})
TOPCAM = lambda x=0, z=0, h=0.62, d=0.16: [cam(0.0, [x, DESK + h, z + d], [x, DESK + h - 0.06, z + d - 0.02], [x, DESK, z], [x, DESK, z], lens=42)]
CARA = lambda aid, pos, ry, clip, expr='unimpressed', **kw: act(aid, pos, ry, clip, expr, **kw)
SHORE = 6.0

# 1-3: back from Sardinia, the grain, the law
st.shot('S01', 'runway', actors=[act('mec', [0, 0, -3.0], 0, 'walk', 'happy', keys=[k(0.0, to=[0, 0, -0.8], dur=st.dur('S01'), clip='walk')])],
        props=[P('plane', 'plane', pos=[-2, 2.2, -16], rot=[0, 0.5, 0]), P('bag', 'briefcase', on={'actor': 'mec', 'hand': 'R'})],
        cams=[cam(0.0, [0.5, 0.5, 2.6], [0.5, 0.52, 3.6], [0, 1.6, -3.0], [0, 1.6, -0.8], lens=50)])
st.shot('S02', 'runway', props=[P('shoe', 'bigShoe', pos=[0, 0, 0], scale=2.2), P('grain', 'sandGrain', pos=[0.04, 0.286, 0.0], scale=0.55, opts={'seed': 3, 'color': SARD, 'popAt': st.at('S02', 'L02', 2) - 0.05})],
        cams=[cam(0.0, [0.3, 0.5, 0.66], [0.26, 0.47, 0.56], [0.04, 0.3, 0], [0.04, 0.3, 0], lens=40)])
st.shot('S03', 'seaSurface', setOpts={'shore': SHORE},
        props=[P('sign', 'signBoard', pos=[0, 0, SHORE + 3.0], opts={'text': 'VIETATO\nPORTARE VIA\nLA SABBIA', 'w': 1.1, 'h': 0.72, 'height': 0.75, 'bg': '#F4F1E8', 'fg': '#C8322A', 'frame': '#C8322A'}),
               P('sard', 'regionFlag', pos=[-0.85, 0, SHORE + 2.2], scale=1.3, opts={'kind': 'sard'})],
        cams=[cam(0.0, [0.45, 1.25, SHORE + 7.0], [0.4, 1.28, SHORE + 6.4], [0, 1.2, SHORE + 3.0], [0, 1.22, SHORE + 3.0], lens=44)])
# 4-6: the fine, for one grain, he refuses
st.shot('S04', 'office', props=[P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': 'REPUBBLICA ITALIANA\nMULTA\n3 000 €', 'style': 'doc', 'w': 0.8, 'h': 1.0, 'popAt': 0.12, 'textSize': 0.36, 'stamp': '1 GRANO'})],
        cams=[cam(0.0, [0.05, 1.55, 2.05], [0.05, 1.55, 1.85], [0, 1.5, 0], [0, 1.5, 0], lens=42)])
st.shot('S05', 'office', props=[TABLE(), P('grain', 'sandGrain', pos=[-0.07, DESK, 0.0], scale=0.55, opts={'seed': 3, 'color': SARD}),
                               P('tag', 'priceTag', pos=[0.03, DESK + 0.004, 0.0], rot=[-1.5708, 0, 0.25], scale=0.35, opts={'text': '3 000 €'})],
        cams=TOPCAM(0.0, 0.0, h=0.62, d=0.12))
st.shot('S06', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'armsCrossed', 'smug', keys=[k(0.35, clip='shakeHead'), k(1.1, clip='armsCrossed')])], cams=MS(0, 0, h=1.5, d=2.6))
# 7-9: two carabinieri, the search, three days
st.shot('S07', 'parisStreet', actors=[CARA('c1', [6.6, 0, -2.2], 0, 'walk', keys=[k(0.0, to=[6.6, 0, -0.2], dur=st.dur('S07'), clip='walk')]),
                                     CARA('c2', [7.45, 0, -2.6], 0, 'walk', keys=[k(0.0, to=[7.45, 0, -0.6], dur=st.dur('S07'), clip='walk')])],
        cams=[cam(0.0, [7.3, 0.5, 4.4], [7.25, 0.52, 4.1], [7.0, 1.55, -1.2], [7.0, 1.55, -0.4], lens=46)])
st.shot('S08', 'office', actors=[CARA('c1', [-0.5, 0, 0.35], 55, 'lookItem', 'suspicious'), CARA('c2', [0.5, 0, 0.3], -55, 'lookItem', 'suspicious')],
        props=[TABLE(w=0.9), P('shoe', 'bigShoe', pos=[0, DESK, 0], rot=[0, 0.4, 0], scale=1.6),
               P('l1', 'magnifyingGlass', on={'actor': 'c1', 'hand': 'R'}, scale=0.45), P('l2', 'magnifyingGlass', on={'actor': 'c2', 'hand': 'R'}, scale=0.45)],
        cams=WS(0, 0, h=1.75, d=5.6, look_h=1.45))
st.shot('S09', 'office', props=[P('clock', 'wallClock', pos=[-0.2, 1.72, -0.1], scale=0.8, opts={'rate': 9}), P('cal', 'calendar', pos=[0.24, 1.6, -0.08], scale=0.85, opts={'rate': 2.4, 'start': st.at('S09', 'L08', 5) - 0.1})],
        cams=[cam(0.0, [0.0, 1.68, 2.4], [0.0, 1.68, 2.15], [0.0, 1.66, -0.1], [0.0, 1.66, -0.1], lens=42)])
# 10-11: forty grains, thirty-nine from Brittany
st.shot('S10', 'office', props=[TABLE(), P('tray', 'sandTray', pos=[0, DESK, 0], opts={'w': 0.5, 'd': 0.34, 'groups': [[39, 0, 0, BZH], [1, 0, 0, SARD]], 'countUp': [0.15, st.at('S10', 'L09', 3)], 'label': 'PIÈCE À CONVICTION'}),
                               P('n40', 'noticeBoard', pos=[0.075, DESK + 0.04, 0.05], rot=[-1.5708, 0, 0], opts={'text': '40', 'style': 'tag', 'w': 0.09, 'h': 0.06, 'popAt': st.at('S10', 'L09', 3)})],
        cams=TOPCAM(0, 0.02, h=0.62, d=0.2))
st.shot('S11', 'office', props=[TABLE(), P('tray', 'sandTray', pos=[0, DESK, 0], opts={'w': 0.5, 'd': 0.34, 'flagW': 0.09, 'groups': [[39, -0.06, 0.02, BZH, 'bzh'], [1, 0.1, -0.02, SARD, 'sard']], 'sortAt': [0.1, st.at('S11', 'L10', 3)], 'label': 'PIÈCE À CONVICTION'})],
        cams=[cam(0.0, [0.03, DESK + 0.95, 0.3], [0.03, DESK + 0.88, 0.27], [0.03, DESK, 0], [0.03, DESK, 0], lens=42)])
# 12-15: France claims its own, the swap at the border, 39 for 1, the escort
st.shot('S12', 'pressRoom', setOpts={'backdrop': 'RÉPUBLIQUE|FRANÇAISE', 'fontScale': 0.85, 'podium': False}, actors=[act('ministre', [0, 0, 0], 0, 'podiumTalk', 'angry', keys=st.talk('L11', 'S12', 'angry'))],
        props=[P('pod', 'podium', pos=[0, 0, 0.45]), P('flag', 'regionFlag', pos=[-0.75, 0, -0.35], scale=1.3, opts={'kind': 'fr'})], cams=MS(0, 0, h=1.55, d=2.8))
st.shot('S13', 'grassland', actors=[act('gendarme', [-0.95, 0, 0.4], 90, 'holdOut', 'suspicious'), CARA('c1', [0.95, 0, 0.4], -90, 'holdOut', 'suspicious')],
        props=[P('gate', 'barrierGate', pos=[-0.05, 0, -0.9], scale=1.25, opts={'length': 1.8, 'angle': 0, 'sign': 'FRONTIÈRE'}),
               P('t1', 'sandTray', pos=[-0.4, 1.2, 0.42], opts={'w': 0.3, 'd': 0.22, 'flagW': 0.09, 'groups': [[1, 0, 0, SARD, 'sard']]}),
               P('t2', 'sandTray', pos=[0.4, 1.2, 0.42], opts={'w': 0.3, 'd': 0.22, 'flagW': 0.09, 'groups': [[39, 0, 0, BZH, 'bzh']]})],
        cams=WS(0.0, 0, h=1.95, d=6.2, look_h=1.25))
st.shot('S14', 'grassland', props=[P('gate', 'barrierGate', pos=[-1.4, 0, -0.45], opts={'length': 3.0, 'angle': 0}), P('a', 'sandTray', pos=[0.42, 1.06, 0.1], opts={'w': 0.36, 'd': 0.24, 'groups': [[39, 0, 0, BZH, 'bzh']]}, keys=[k(0.0, to=[-0.3, 1.06, 0.1], dur=st.dur('S14'), ease='inOut')]),
                                   P('b', 'sandTray', pos=[-0.42, 1.06, -0.2], opts={'w': 0.36, 'd': 0.24, 'groups': [[1, 0, 0, SARD, 'sard']]}, keys=[k(0.0, to=[0.3, 1.06, -0.2], dur=st.dur('S14'), ease='inOut')])],
        cams=[cam(0.0, [0.05, 1.5, 1.05], [0.04, 1.47, 0.95], [0, 1.0, -0.05], [0, 1.0, -0.05], lens=44)])
st.shot('S15', 'skyHigh', setOpts={'layer': True},
        props=[P('jet', 'plane', pos=[-20, 60, 0], scale=0.55, opts={'livery': '#C9A227'}, keys=[k(0.0, to=[20, 60, 0], dur=st.dur('S15'))]),
               P('f1', 'fighterJet', pos=[-24, 64.5, -8], rot=[0, 1.5708, 0], scale=0.7, keys=[k(0.0, to=[16, 64.5, -8], dur=st.dur('S15'))]),
               P('f2', 'fighterJet', pos=[-24, 55.8, -8], rot=[0, 1.5708, 0], scale=0.7, keys=[k(0.0, to=[16, 55.8, -8], dur=st.dur('S15'))])],
        cams=[cam(0.0, [-18, 61.0, 52], [22, 61.0, 52], [-21, 60.2, -3], [19, 60.2, -3], lens=40, shake=0.02)])
# 16-17: home sweet home: the Sardinian grain among billions, the 39 welcomed as heroes in Brittany
st.shot('S16', 'seaSurface', setOpts={'shore': SHORE},
        props=[P('grain', 'sandGrain', pos=[0, 0.02, SHORE + 3.0], scale=0.5, opts={'seed': 3, 'color': SARD, 'flag': 'sard', 'flagW': 0.07}),
               P('beach', 'sandTray', pos=[0.02, 0.02, SHORE + 3.0], scale=1.7, opts={'noTray': True, 'seed': 8, 'groups': [[70, 0.0, 0.0, None]]})],
        cams=[cam(0.0, [0.1, 0.11, SHORE + 3.42], [0.9, 1.7, SHORE + 8.5], [0.0, 0.04, SHORE + 3.0], [0.0, 0.7, SHORE + 0.5], lens=42, ease='inOut')])
st.shot('S17', 'seaSurface', setOpts={'shore': SHORE, 'parasols': False, 'sand': '#E2DCCB', 'sky': ['#86AFCF', '#C8DAE6']},
        actors=[act(a, [x, 0, SHORE + 1.6 + dz], ry, 'celebrate', 'happy') for a, x, dz, ry in [('b1', -0.95, 0.0, 15), ('b2', -0.3, -0.25, 5), ('b3', 0.35, -0.25, -5), ('b4', 1.0, 0.0, -15)]],
        props=[TABLE(0, SHORE + 2.6, w=0.9, d=0.5), P('tray', 'sandTray', pos=[0, DESK, SHORE + 2.6], scale=1.4, opts={'w': 0.36, 'd': 0.24, 'groups': [[39, 0, 0, BZH, 'bzh']]}),
               P('ban', 'signBoard', pos=[0, 0, SHORE + 0.5], opts={'text': 'DEGEMER MAT !', 'w': 1.6, 'h': 0.48, 'height': 2.25, 'bg': '#F4F4F0', 'fg': '#17171B', 'frame': '#17171B'}),
               P('fl1', 'regionFlag', pos=[-1.2, 0, SHORE + 2.3], scale=0.8, opts={'kind': 'bzh'})],
        cams=WS(0, SHORE + 1.6, h=1.5, d=6.4, look_h=1.5))
# 18-22: the shoe at auction, 3,000 euros, bought by Italy, the fine paid with it
st.shot('S18', 'livingRoom', actors=[act('mec', [0.4, 0, 0], -35, 'showPhone', 'smug')], props=[P('shoe', 'bigShoe', on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, scale=1.1)], cams=MS(0.15, 0, h=1.5, d=2.8))
AUCTION = {'backdrop': 'VENTE|AUX ENCHÈRES', 'fontScale': 0.85, 'flags': False, 'podium': False}
st.shot('S19', 'pressRoom', setOpts=AUCTION, actors=[act('priseur', [0, 0, 0], 0, 'explain', 'happy')],
        props=[P('pod', 'podium', pos=[0, 0, 0.45], opts={'text': 'ENCHÈRES'}), P('ped', 'table', pos=[0.58, 0, 0.35], opts={'w': 0.4, 'd': 0.4, 'h': 0.95, 'color': '#3A2A22'}),
               P('shoe', 'bigShoe', pos=[0.58, 0.95, 0.35], rot=[0, 0.5, 0], scale=1.2), P('dome', 'glassDome', pos=[0.58, 0.95, 0.35], opts={'radius': 0.2, 'height': 0.45, 'base': False})],
        cams=MS(0.25, 0, h=1.35, d=3.4))
st.shot('S20', 'pressRoom', setOpts=AUCTION, actors=[act('priseur', [0, 0, 0], 0, 'gavelStrike', 'happy', params={'hit': 0.42})],
        props=[P('pod', 'podium', pos=[0, 0, 0.45], opts={'text': 'ENCHÈRES'}), P('gavel', 'gavel', on={'actor': 'priseur', 'hand': 'R'}),
               P('adj', 'noticeBoard', pos=[0.36, 1.95, 0.35], opts={'text': 'ADJUGÉ\n3 000 €', 'style': 'sign', 'w': 0.42, 'h': 0.28, 'fg': '#C8322A', 'frame': '#C8322A', 'popAt': 0.44})],
        cams=MS(0.12, 0, h=1.55, d=2.7), fx=[{'type': 'shake', 'at': 0.42, 'dur': 0.18, 'amount': 0.018}])
st.shot('S21', 'pressRoom', setOpts={'backdrop': 'REPUBBLICA|ITALIANA', 'fontScale': 0.85, 'flag': ['#2E8B4E', '#F4F4F0', '#C8322A'], 'podium': False}, actors=[CARA('c1', [0.4, 0, 0], -35, 'showPhone', 'smug')],
        props=[P('shoe', 'bigShoe', on={'actor': 'c1', 'hand': 'R', **HAND_FLAT}, scale=1.1), P('flag', 'regionFlag', pos=[0.1, 0, -0.5], scale=1.3, opts={'kind': 'it'})], cams=MS(0.15, 0, h=1.5, d=2.8))
st.shot('S22', 'livingRoom', actors=[act('mec', [-0.48, 0, 0.1], 90, 'giveItem', 'smug'), CARA('c1', [0.5, 0, 0.0], -90, 'takeItem', 'unimpressed')],
        props=[P('sack', 'moneySack', on={'actor': 'mec', 'hand': 'R'}, scale=0.6),
               P('paid', 'noticeBoard', pos=[0.15, 2.12, 0.2], opts={'text': 'AMENDE PAYÉE', 'style': 'tag', 'w': 0.7, 'h': 0.18, 'fg': '#2F7F4F', 'frame': '#2F7F4F', 'popAt': st.at('S22', 'L20', 3)})],
        cams=WS(0, 0, h=1.5, d=4.2, look_h=1.3))
st.card('S04', 'AMENDE'); st.card('S14', '39 CONTRE 1')
st.cue('engine', 'S01', 0.0, 0.25, st.dur('S01')); [st.cue('sfx:step', 'S01', t, 0.4) for t in (0.3, 0.8, 1.3)]
st.cue('pop', 'S02', st.at('S02', 'L02', 2) - 0.05, 0.45); st.cue('sfx:bell', 'S02', st.at('S02', 'L02', 2), 0.12)
st.cue('gust', 'S03', 0.0, 0.3, st.dur('S03')); st.cue('thud', 'S04', 0.07, 0.45); st.cue('sfx:paper', 'S04', 0.1, 0.5); st.cue('clack', 'S04', 0.6, 0.5)
st.cue('sfx:cash', 'S05', 0.2, 0.35); st.cue('sfx:grunt', 'S06', 0.4, 0.3)
[st.cue('sfx:step', 'S07', t, 0.45) for t in (0.15, 0.6, 1.05, 1.5)]; st.cue('sfx:sniff', 'S08', 0.5, 0.4); st.cue('sfx:ticks', 'S09', 0.0, 0.45)
[st.cue('pop', 'S10', 0.15 + 0.12 * i, 0.18) for i in range(6)]; st.cue('pop', 'S10', st.at('S10', 'L09', 3), 0.5); st.cue('whoosh', 'S11', 0.1, 0.25, 0.8, 600, 3000); st.cue('pop', 'S11', st.at('S11', 'L10', 3), 0.45)
st.cue('thud', 'S12', 0.3, 0.35); st.cue('gust', 'S13', 0.0, 0.25, st.dur('S13')); st.cue('thud', 'S14', 0.07, 0.45); st.cue('whoosh', 'S14', 0.2, 0.3, 1.0, 300, 2000)
st.cue('sfx:jet', 'S15', 0.0, 0.5); st.cue('whoosh', 'S15', 0.2, 0.35, 1.2, 300, 2500)
st.cue('gust', 'S16', 0.0, 0.3, st.dur('S16')); st.cue('whoosh', 'S16', 0.1, 0.3, 1.4, 200, 1500); st.cue('sfx:fanfare', 'S17', 0.1, 0.4); st.cue('gust', 'S17', 0.0, 0.2, st.dur('S17'))
st.cue('pop', 'S18', 0.2, 0.3); st.cue('thud', 'S20', 0.42, 0.8); st.cue('pop', 'S20', 0.44, 0.4); st.cue('sfx:cash', 'S21', 0.3, 0.4)
st.cue('sfx:cash', 'S22', 0.3, 0.45); st.cue('clack', 'S22', st.at('S22', 'L20', 3), 0.6)
st.write('Le sable', {'ministre': {'preset': 'politique'}, 'c1': {'preset': 'carabiniere'}, 'c2': {'preset': 'carabiniere', 'facial': 'none', 'hair': 'crew', 'seed': 17, 'build': {'belly': 0.06}},
                      'gendarme': {'preset': 'cop2', 'seed': 23}, 'priseur': {'preset': 'proviseur'},
                      'b1': {'preset': 'fermier', 'hat': 'none', 'seed': 31}, 'b2': {'preset': 'mamie'}, 'b3': {'preset': 'femme'}, 'b4': {'preset': 'tourist', 'seed': 9}})
