#!/usr/bin/env python3
"""La police contre la police: a cop fines him while the police car sits on a disabled bay; he calls 17; the police fine the police,
arrest the cop, then his chief, then the prefect; by noon the whole force is in custody; the town hires him as its only cop;
that evening someone calls 17 about a police car on a disabled bay: his own. He arrests himself."""
from story_kit import *

st = Story('police')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0),
         ('S08', 'L07', 0), ('S09', 'L08', 0), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L11', 2), ('S14', 'L12', 0),
         ('S15', 'L13', 0), ('S16', 'L14', 0), ('S17', 'L15', 0), ('S18', 'L15', 5), ('S19', 'L16', 0), ('S20', 'L17', 0), ('S21', 'L18', 0),
         ('S22', 'L19', 0), ('S23', 'L19', 3), ('S24', 'L20', 0), ('S25', 'L21', 0), ('S26', 'L22', 0)])
ST = 'parisStreet'
R90 = [0, 1.5708, 0]
BAY = lambda: [P('bay', 'disabledSpot', pos=[3.9, 0, -0.5], rot=R90, opts={'sign': True}), P('pcar', 'policeCar', pos=[3.9, 0, -0.5], rot=R90)]
MYCAR = lambda: P('mycar', 'car', pos=[3.9, 0, 6.4], rot=R90, opts={'color': '#C9473A'})
PHONE = lambda a: P('ph', 'phone911', on={'actor': a, 'hand': 'R'}, opts={'text': '17', 'sub': 'POLICE'})
PAD = lambda a: P('pad', 'notebook', on={'actor': a, 'hand': 'L'})
CELL_COPS = [('flic', -0.95, -0.55), ('flic2', -0.3, -0.7), ('flic3', 0.35, -0.6), ('flic4', 0.98, -0.5), ('chef', -0.62, 0.35), ('prefet', 0.05, 0.25), ('flic5', 0.7, 0.4)]
CELL = lambda expr='unimpressed', skip=(): [act(a, [x, 0, z], 0, 'stand', expr) for a, x, z in CELL_COPS if a not in skip]
CUFFS = lambda a: P(f'cuffs_{a}', 'bigCuffs', on={'actor': a, 'hand': 'R'}, opts={'r': 0.062, 'thick': 0.2, 'color': '#D2D6DB'})
ARREST = lambda: [act('flic', [6.1, 0, 0.3], 0, 'cuffedFront', 'shocked'), act('flic2', [5.5, 0, 0.05], 40, 'cuffOther', 'angry'), act('flic3', [6.75, 0, 0.0], -40, 'point', 'angry')]
DESK = (-2.7, -2.1)                      # the police station desk (chair behind it, facing +Z)
LIVE = lambda: P('live', 'noticeBoard', pos=[0.26, 2.02, 0.3], opts={'text': 'EN DIRECT', 'style': 'sign', 'w': 0.44, 'h': 0.13, 'fg': '#C8322A', 'frame': '#C8322A'})
PREF = {'backdrop': 'PRÉFECTURE|DE POLICE', 'fontScale': 0.68, 'podium': False}

# 1-2: the hook (he calls the police, the police arrest the police)
st.shot('S01', ST, actors=[act('mec', [6.2, 0, 1.6], -15, 'phoneCall', 'smug')], props=BAY() + [PHONE('mec')],
        cams=[cam(0.0, [6.75, 1.62, 4.0], [6.7, 1.62, 3.75], [6.1, 1.55, 1.6], [6.1, 1.55, 1.6], lens=44)])
st.shot('S02', ST, actors=ARREST(), props=BAY() + [CUFFS('flic')], cams=[cam(0.0, [6.55, 0.85, 4.3], [6.5, 0.9, 4.0], [6.1, 1.45, 0.1], [6.1, 1.45, 0.1], lens=46)])
# 3-6: the fine, and the police car on the disabled bay
st.shot('S03', ST, actors=[act('flic', [5.4, 0, 6.6], -70, 'writeOnHeld', 'smug'), act('mec', [6.3, 0, 7.4], -110, 'stand', 'angry')], props=BAY() + [MYCAR(), PAD('flic')],
        cams=[cam(0.0, [6.05, 1.5, 10.5], [6.0, 1.5, 10.2], [5.85, 1.2, 6.9], [5.85, 1.2, 6.9], lens=44)])
st.shot('S04', ST, props=BAY() + [MYCAR(), P('pv', 'noticeBoard', pos=[6.4, 1.5, 3.0], opts={'text': 'AMENDE\nSTATIONNEMENT GÊNANT\n35 €', 'style': 'doc', 'w': 0.7, 'h': 0.9, 'popAt': 0.1, 'textSize': 0.4, 'stamp': 'POLICE'})],
        cams=[cam(0.0, [6.45, 1.55, 5.25], [6.45, 1.55, 5.05], [6.4, 1.5, 3.0], [6.4, 1.5, 3.0], lens=42)])
st.shot('S05', ST, props=BAY() + [MYCAR()], cams=[cam(0.0, [7.6, 1.45, 3.0], [7.6, 1.5, 2.8], [3.9, 1.0, 6.2], [3.9, 1.0, -0.6], lens=44, ease='inOut')])
st.shot('S06', ST, props=BAY(), cams=[cam(0.0, [7.3, 1.95, -2.3], [9.2, 3.4, 2.4], [5.65, 1.9, -2.15], [4.3, 0.5, -0.9], lens=44, ease='inOut')])
# 7-11: 17, two cops, they fine the police car, the cop refuses, they arrest him
st.shot('S07', ST, props=BAY() + [P('phone', 'phone911', pos=[6.3, 1.12, 3.0], rot=[0, 0, 0.08], scale=3.0, opts={'text': '17', 'sub': 'POLICE'})],
        cams=[cam(0.0, [6.32, 1.52, 4.55], [6.32, 1.52, 4.35], [6.3, 1.5, 3.0], [6.3, 1.5, 3.0], lens=42)])
st.shot('S08', ST, actors=[act('flic2', [5.9, 0, -6.0], 0, 'walk', 'smug', keys=[k(0.0, to=[5.9, 0, -3.4], dur=st.dur('S08'), clip='walk')]),
                          act('flic3', [6.75, 0, -6.4], 0, 'walk', 'smug', keys=[k(0.0, to=[6.75, 0, -3.8], dur=st.dur('S08'), clip='walk')])],
        props=BAY() + [P('pcar2', 'policeCar', pos=[2.0, 0, -16.0], rot=[0, -1.5708, 0], keys=[k(0.0, to=[2.0, 0, -9.5], dur=st.dur('S08') * 0.8, ease='out')])],
        cams=[cam(0.0, [7.3, 0.95, 3.2], [7.2, 1.0, 2.9], [6.0, 1.35, -4.5], [6.0, 1.35, -4.0], lens=46)])
st.shot('S09', ST, actors=[act('flic2', [5.55, 0, -0.2], 35, 'writeOnHeld', 'smug'), act('flic3', [6.6, 0, 0.5], -20, 'handsOnHips', 'smug')],
        props=BAY() + [PAD('flic2'), P('fine', 'noticeBoard', pos=[3.95, 1.92, -0.6], rot=R90, opts={'text': 'AMENDE', 'style': 'tag', 'w': 0.6, 'h': 0.2, 'popAt': st.at('S09', 'L08', 2)})],
        cams=[cam(0.0, [8.1, 1.65, 3.1], [7.95, 1.65, 2.8], [5.0, 1.3, -0.6], [5.0, 1.3, -0.6], lens=44)])
st.shot('S10', ST, actors=[act('flic', [6.2, 0, 0.6], 0, 'armsCrossed', 'angry', keys=[k(0.35, clip='shakeHead'), k(1.25, clip='armsCrossed')])], props=BAY(), cams=MS(6.2, 0.6, h=1.55, d=2.6))
st.shot('S11', ST, actors=ARREST(), props=BAY() + [CUFFS('flic')], cams=[cam(0.0, [6.35, 1.75, 3.55], [6.3, 1.75, 3.3], [6.1, 1.52, 0.2], [6.1, 1.52, 0.2], lens=44)])
# 12-16: the chief takes his side (arrested), the prefect protests on TV (arrested)
st.shot('S12', 'policeStation', actors=[act('chef', [-1.1, 0, -1.0], 60, 'walk', 'angry', keys=[k(0.0, to=[-0.55, 0, -0.65], dur=st.dur('S12'), clip='walk')]),
                                       act('flic', [0.7, 0, -0.3], -20, 'cuffedFront', 'sad'), act('flic2', [1.35, 0, -0.5], -40, 'stand', 'smug')],
        cams=[cam(0.0, [0.4, 1.7, 5.2], [0.35, 1.72, 4.8], [0, 1.6, -2.0], [0, 1.62, -2.0], lens=46)])
st.shot('S13', 'policeStation', actors=[act('chef', [-0.55, 0, 0.3], 70, 'explain', 'angry'), act('flic2', [0.75, 0, 0.2], -70, 'stand', 'suspicious'), act('flic', [1.3, 0, -0.3], -40, 'cuffedFront', 'sad')],
        props=[CUFFS('flic')], cams=WS(0.25, 0.1, h=1.6, d=5.0, look_h=1.35))
st.shot('S14', 'policeStation', actors=[act('chef', [0, 0, 0.3], 0, 'cuffedFront', 'scared'), act('flic3', [0.05, 0, -0.35], 0, 'cuffOther', 'smug')], props=[CUFFS('chef')], cams=MS(0, 0.3, h=1.55, d=2.8))
st.shot('S15', 'pressRoom', setOpts=PREF, actors=[act('prefet', [0, 0, 0], 0, 'podiumTalk', 'angry', keys=st.talk('L13', 'S15', 'angry'))],
        props=[P('pod', 'podium', pos=[0, 0, 0.45]), LIVE()], cams=MS(0, 0, h=1.55, d=2.9))
st.shot('S16', 'pressRoom', setOpts=PREF, actors=[act('prefet', [0.15, 0, 0.2], 0, 'cuffedFront', 'shocked'), act('flic2', [0.2, 0, -0.42], 0, 'cuffOther', 'smug')],
        props=[P('pod', 'podium', pos=[-0.62, 0, 0.45]), P('live', 'noticeBoard', pos=[-0.2, 2.02, 0.3], opts={'text': 'EN DIRECT', 'style': 'sign', 'w': 0.44, 'h': 0.13, 'fg': '#C8322A', 'frame': '#C8322A'}), CUFFS('prefet')], cams=MS(0, 0, h=1.6, d=3.2))
# 17-19: noon, the whole force in custody, nobody left to guard the cells
st.shot('S17', 'policeStation', actors=[act(a, [x, 0, -0.6], 0, 'stand', 'unimpressed') for a, x in [('flic', -1.25), ('flic2', -0.75), ('flic3', -0.25), ('flic4', 0.25), ('flic5', 0.75), ('chef', 1.25)]],
        props=[P('clock', 'wallClock', pos=[-0.95, 2.2, -3.45], scale=1.1, opts={'rate': 0})], cams=WS(0, -0.6, h=1.6, d=7.2, look_h=1.65))
st.shot('S18', 'brightCell', actors=CELL(), cams=[cam(0.0, [0.3, 1.6, 4.5], [0.28, 1.6, 4.3], [0, 1.4, 0], [0, 1.42, 0], lens=52)])
st.shot('S19', 'policeStation', props=[P('chair', 'officeChair', pos=[DESK[0] + 0.45, 0, DESK[1] + 0.95], keys=[k(0.0, rotTo=[0, 4.0, 0], dur=st.dur('S19'), ease='out')]),
                                      P('tw', 'tumbleweed', pos=[-5.2, 0.35, -0.9], scale=0.9, keys=[k(0.0, to=[0.6, 0.35, -0.9], dur=st.dur('S19'), ease='linear')])],
        cams=[cam(0.0, [-1.75, 2.3, 1.2], [-1.85, 2.25, 0.95], [-2.65, 0.6, -2.5], [-2.65, 0.6, -2.5], lens=44)])
# 20-21: the town hires him, the only cop in town
st.shot('S20', 'office', actors=[act('maire', [-0.5, 0, 0.1], 55, 'giveItem', 'smug'), act('mec', [0.52, 0, 0.0], -55, 'takeItem', 'happy')],
        props=[P('cap', 'copCap', on={'actor': 'maire', 'hand': 'R'}, scale=1.0), P('fr', 'regionFlag', pos=[-1.05, 0, -0.7], opts={'kind': 'fr'}),
               P('rec', 'noticeBoard', pos=[0.05, 2.12, 0.2], opts={'text': 'RECRUTÉ', 'style': 'tag', 'w': 0.5, 'h': 0.16, 'popAt': st.at('S20', 'L17', 4)})],
        cams=WS(0, 0, h=1.5, d=4.4, look_h=1.35))
st.shot('S21', ST, actors=[act('mecFlic', [0.4, 0, 0], 0, 'heroPose', 'smug')],
        props=[P('tw', 'tumbleweed', pos=[-6.0, 0.4, -3.5], scale=1.1, keys=[k(0.0, to=[6.0, 0.4, -3.5], dur=st.dur('S21'), ease='linear')])], cams=LOW(0.4, 0, d=3.4, look_h=1.6))
# 22-26: that evening a call about a police car on a disabled bay: his own; he arrests himself
st.shot('S22', 'policeStation', actors=[act('mecFlic', [DESK[0], 0, DESK[1] - 0.62], 0, 'sit', 'unimpressed')],
        props=[P('chair', 'officeChair', pos=[DESK[0], 0, DESK[1] - 0.7]), P('mug', 'mug', pos=[DESK[0] + 0.35, 0.76, DESK[1] + 0.1]),
               P('clock', 'wallClock', pos=[DESK[0] + 0.55, 2.15, -3.45], scale=0.9, opts={'rate': 0, 'hours': 8})],
        cams=[cam(0.0, [-2.05, 1.35, 0.9], [-2.1, 1.35, 0.65], [-2.65, 1.05, -2.6], [-2.65, 1.05, -2.6], lens=44)])
st.shot('S23', 'policeStation', props=[P('ph', 'phone911', pos=[DESK[0] - 0.1, 0.79, DESK[1] + 0.32], rot=[-1.5708, 0, 0.3], scale=1.6, opts={'text': '17', 'sub': 'APPEL'},
                                         keys=[k(round(0.1 + 0.16 * i, 2), rotTo=[-1.5708, 0, 0.3 + (0.12 if i % 2 else -0.12)], dur=0.08) for i in range(8)])],
        cams=[cam(0.0, [DESK[0] - 0.1, 1.6, DESK[1] + 0.4], [DESK[0] - 0.1, 1.5, DESK[1] + 0.36], [DESK[0] - 0.1, 0.79, DESK[1] + 0.12], [DESK[0] - 0.1, 0.79, DESK[1] + 0.12], lens=42)])
st.shot('S24', ST, props=BAY(), cams=[cam(0.0, [9.3, 3.4, 2.5], [9.15, 3.3, 2.2], [4.3, 0.5, -0.9], [4.3, 0.5, -0.9], lens=44)])
st.shot('S25', 'policeStation', actors=[act('mecFlic', [0, 0, 0], 0, 'phoneCall', 'unimpressed', keys=[k(0.25, expr='shocked')])], props=[PHONE('mecFlic')], cams=CU(0, 0, d=1.9))
st.shot('S26', 'brightCell', actors=CELL('smug', skip=('prefet',)) + [act('mecFlic', [0.12, 0, 1.12], 0, 'cuffedFront', 'sad')], props=[CUFFS('mecFlic')],
        cams=[cam(0.0, [0.2, 1.78, 2.6], [0.3, 1.6, 4.4], [0.12, 1.75, 1.0], [0.05, 1.42, 0.3], lens=46, ease='inOut')])
st.card('S11', 'ARRÊTÉ'); st.card('S18', 'GARDE À VUE')
st.cue('sfx:ring', 'S01', 0.1, 0.3); st.cue('sfx:cuff', 'S02', 0.4, 0.5)
st.cue('sfx:paper', 'S03', 0.4, 0.4); st.cue('thud', 'S04', 0.07, 0.45); st.cue('sfx:paper', 'S04', 0.1, 0.45); st.cue('whoosh', 'S05', 0.1, 0.25, 0.7, 300, 2000)
st.cue('pop', 'S06', 0.3, 0.35); st.cue('sfx:gasp', 'S06', 1.1, 0.4); [st.cue('sfx:beep', 'S07', t, 0.35) for t in (0.15, 0.4)]; st.cue('sfx:ring', 'S07', 0.8, 0.3)
st.cue('engine', 'S08', 0.0, 0.3, st.dur('S08')); st.cue('sfx:brake', 'S08', 1.0, 0.35); [st.cue('sfx:step', 'S08', t, 0.35) for t in (0.2, 0.65, 1.1)]
st.cue('sfx:paper', 'S09', 0.3, 0.4); st.cue('pop', 'S09', st.at('S09', 'L08', 2), 0.5); st.cue('sfx:grunt', 'S10', 0.4, 0.35)
st.cue('sfx:cuff', 'S11', 0.3, 0.6); st.cue('thud', 'S11', 0.07, 0.45); [st.cue('sfx:step', 'S12', t, 0.4) for t in (0.1, 0.5)]
st.cue('sfx:cuff', 'S14', 0.25, 0.6); st.cue('sfx:static', 'S15', 0.0, 0.15); st.cue('sfx:cuff', 'S16', 0.3, 0.6); st.cue('sfx:gasp', 'S16', 0.5, 0.35)
st.cue('sfx:bell', 'S17', 0.1, 0.4); st.cue('thud', 'S18', 0.07, 0.45); st.cue('clang', 'S18', 0.3, 0.5); st.cue('sfx:squeak', 'S19', 0.1, 0.3); st.cue('gust', 'S19', 0.0, 0.3, st.dur('S19'))
st.cue('pop', 'S20', st.at('S20', 'L17', 4), 0.5); st.cue('sfx:fanfare', 'S20', st.at('S20', 'L17', 4), 0.25); st.cue('gust', 'S21', 0.0, 0.35, st.dur('S21')); st.cue('sfx:whistle', 'S21', 0.3, 0.25)
st.cue('sfx:ticks', 'S22', 0.0, 0.35); [st.cue('sfx:ring', 'S23', t, 0.45) for t in (0.1, 0.75)]; st.cue('sfx:gasp', 'S25', 0.25, 0.5)
st.cue('sfx:cuff', 'S26', 0.2, 0.6); st.cue('clang', 'S26', 0.9, 0.45)
COP = lambda **kw: {'preset': 'cop', **kw}
st.write('La police contre la police', {
    'flic': COP(hair='crew', facial='mustache', seed=41, build={'belly': 0.06}), 'flic2': COP(hair='receding', facial='stubble', seed=43),
    'flic3': COP(hair='buzz', facial='none', seed=47), 'flic4': COP(hair='curly', facial='beard', seed=53), 'flic5': COP(hair='slick', facial='none', seed=59, build={'height': 0.95}),
    'chef': {'preset': 'commissaire'}, 'prefet': {'preset': 'prefet'},
    'maire': {'preset': 'politique', 'hair': 'receding', 'hairColor': '#8A8A86', 'facial': 'mustache', 'sash': ['#24448E', '#F4F4F0', '#D03A34'], 'sashW': 0.14, 'build': {'belly': 0.1}},
    'mecFlic': {'preset': 'cop', 'hat': 'copcap', 'hair': 'crew', 'facial': 'stubble', 'atlas': 'lemec', 'atlasBody': False, 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}})
