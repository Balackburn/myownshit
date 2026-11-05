#!/usr/bin/env python3
"""Le burger vegan: he loves his burger until the waiter says it is vegan; he calls the police for identity theft; the burger is
arrested and analysed: soy. The soy (a living bean) had a network: entered France without a label, it passed itself off as steak,
milk, cheese and nuggets, working day and night in place of the cows (who went on holiday). Ten years for illegal work and identity
theft; the man gets six months for an abusive call, finds the soy running the prison canteen, and takes seconds."""
from story_kit import *

st = Story('burger')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 7), ('S06', 'L04', 0), ('S07', 'L05', 0),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L09', 0), ('S12', 'L10', 0), ('S13', 'L11', 0), ('S14', 'L12', 0),
         ('S15', 'L13', 0), ('S16', 'L14', 0), ('S17', 'L15', 0), ('S18', 'L16', 0), ('S19', 'L17', 0), ('S20', 'L18', 0), ('S21', 'L18', 5),
         ('S22', 'L19', 0), ('S23', 'L20', 0), ('S24', 'L21', 0), ('S25', 'L21', 7), ('S26', 'L22', 0), ('S27', 'L23', 0), ('S28', 'L24', 0), ('S29', 'L25', 0)])
TT = 0.79                                             # restaurant table top
BURGER = lambda **kw: P('burger', 'burger', pos=[0, TT, -2.6], scale=1.3, **kw)
SOY = lambda aid='soja', pos=(0, 0, 0), ry=0, clip='idle', expr='happy', **kw: act(aid, list(pos), ry, clip, expr, **kw)
COSTUME = lambda aid, kind, **kw: P(f'cos_{aid}', 'soyCostume', on={'actor': aid, 'joint': 'head', 'offset': [0, 0.3, 0]}, opts={'kind': kind, **kw})
TOQUE = lambda aid='soja': P('toque', 'chefHat', on={'actor': aid, 'joint': 'head', 'offset': [0, 0.6, 0]})
CUFFS = lambda a: P(f'cuffs_{a}', 'bigCuffs', on={'actor': a, 'hand': 'R'}, opts={'r': 0.062, 'thick': 0.2, 'color': '#D2D6DB'})
SHOP = [cam(0.0, [0.25, 0.95, 0.35], [0.22, 0.95, 0.12], [0, 0.72, -2.0], [0, 0.73, -2.0], lens=44)]
CHALK = '#2F4A3A'

# 1-7: the restaurant
st.shot('S01', 'restaurant', actors=[act('mec', [0.45, 0, -2.0], -12, 'phoneCall', 'angry')], props=[BURGER(), P('ph', 'phone911', on={'actor': 'mec', 'hand': 'R'}, opts={'text': '17', 'sub': 'POLICE'})],
        cams=[cam(0.0, [0.75, 1.55, 0.7], [0.72, 1.55, 0.45], [0.38, 1.5, -2.0], [0.38, 1.5, -2.0], lens=44)])
st.shot('S02', 'restaurant', props=[BURGER()], cams=[cam(0.0, [0.16, 1.0, -1.68], [0.12, 0.99, -1.82], [0, 0.9, -2.6], [0, 0.9, -2.6], lens=42)])
st.shot('S03', 'restaurant', actors=[act('mec', [0.4, 0, -2.0], 0, 'eatHands', 'happy')], props=[P('b', 'burger', on={'actor': 'mec', 'hand': 'R'}, scale=0.65)], cams=MS(0.4, -2.0, h=1.62, d=2.3))
st.shot('S04', 'restaurant', actors=[act('serveur', [-0.35, 0, -1.9], 18, 'explain', 'smug')], props=[BURGER()], cams=MS(-0.35, -1.9, h=1.62, d=2.8))
st.shot('S05', 'restaurant', props=[BURGER(opts={'pick': 'VEGAN', 'pickAt': st.at('S05', 'L03', 9) - 0.08})],
        cams=[cam(0.0, [0.14, 1.06, -1.6], [0.12, 1.05, -1.74], [0, 1.0, -2.6], [0, 1.0, -2.6], lens=42)])
st.shot('S06', 'restaurant', actors=[act('mec', [0.3, 0, -1.9], 0, 'tantrum', 'angry')], props=[BURGER()], cams=MS(0.3, -1.9, h=1.5, d=2.8, shake=0.03), fx=[{'type': 'shake', 'at': 0.25, 'dur': 0.3, 'amount': 0.03}])
st.shot('S07', 'restaurant', props=[BURGER(), P('moust', 'mustache3d', pos=[0, TT + 0.128, -2.6 + 0.162], scale=1.3), P('specs', 'glasses', pos=[0, TT + 0.175, -2.6 + 0.14], opts={'r': 0.03, 'dx': 0.045})],
        cams=[cam(0.0, [0.12, 1.02, -1.7], [0.1, 1.01, -1.82], [0, 0.95, -2.6], [0, 0.95, -2.6], lens=42)])
# 8-10: arrested, analysed, soy
st.shot('S08', 'policeStation', props=[P('wall', 'mugshotBoard', pos=[0, 0, -3.45]), P('stool', 'barStool', pos=[0, 0, -2.9]), P('burger', 'burger', pos=[0, 0.75, -2.9], scale=1.6),
                                      P('plac', 'placard', pos=[0, 0.84, -2.62], rot=[-0.15, 0, 0], opts={'text': 'BURGER\n2026-042'})],
        cams=[cam(0.0, [0.04, 1.05, -1.0], [0.04, 1.05, -1.15], [0, 0.98, -2.9], [0, 0.98, -2.9], lens=44)], fx=[{'type': 'flash', 'at': 0.45, 'dur': 0.08}])
st.shot('S09', 'lab', actors=[act('savant', [0.3, 0, -1.45], -10, 'lookItem', 'suspicious')],
        props=[P('t', 'table', pos=[0, 0, -0.8], opts={'w': 1.1, 'd': 0.7, 'h': 0.9, 'color': '#B9C0C2', 'legs': '#8E9698'}), P('burger', 'burger', pos=[-0.1, 0.9, -0.75], scale=1.3),
               P('dome', 'glassDome', pos=[-0.1, 0.9, -0.75], opts={'radius': 0.24, 'height': 0.5, 'base': False}), P('loupe', 'magnifyingGlass', on={'actor': 'savant', 'hand': 'R'}, scale=0.45)],
        cams=[cam(0.0, [0.35, 1.72, 2.1], [0.32, 1.7, 1.85], [0.05, 1.48, -1.0], [0.05, 1.48, -1.0], lens=44)])
st.shot('S10', 'lab', actors=[SOY('soja', (0.22, 0.9, -0.72), -15, 'wave', 'scared', scale=0.42, keys=[k(0.9, expr='smug')])],
        props=[P('t', 'table', pos=[0, 0, -0.8], opts={'w': 1.1, 'd': 0.7, 'h': 0.9, 'color': '#B9C0C2', 'legs': '#8E9698'}), P('burger', 'burger', pos=[-0.12, 0.9, -0.78], scale=1.3, opts={'openAt': 0.1})],
        cams=[cam(0.0, [0.12, 1.22, 0.32], [0.1, 1.2, 0.18], [0.05, 1.08, -0.78], [0.05, 1.08, -0.78], lens=42)])
# 11-16: the network: no label, fake steak, milk, cheese, nuggets
st.shot('S11', 'policeStation', actors=[act('flic', [-0.25, 0, -2.0], -40, 'point', 'suspicious')], props=[P('board', 'conspiracyBoard', pos=[-1.15, 1.65, -3.48], opts={'drawAt': 0.2})],
        cams=[cam(0.0, [-0.66, 1.62, 0.15], [-0.7, 1.62, -0.1], [-0.88, 1.55, -3.2], [-0.88, 1.55, -3.2], lens=44)])
st.shot('S12', 'airport', actors=[act('flic', [0.55, 0, -1.75], 0, 'clipboard', 'unimpressed'),
                                  SOY('soja', (-1.6, 0.7, -1.0), 0, 'stiff', 'smug', scale=0.55, keys=[k(0.0, to=[0.65, 0.7, -1.0], dur=st.dur('S12'), ease='linear')])],
        props=[P('belt', 'table', pos=[0, 0, -1.0], opts={'w': 5.0, 'd': 0.6, 'h': 0.7, 'color': '#3A3D44', 'legs': '#2A2A2E'})] +
              [P(f'box{i}', 'cardboardBox', pos=[x, 0.7, -1.0], scale=0.6, keys=[k(0.0, to=[x + 2.25, 0.7, -1.0], dur=st.dur('S12'), ease='linear')]) for i, x in enumerate((-2.6, -0.65))] +
              [P(f'lab{i}', 'noticeBoard', pos=[x, 0.98, -0.72], opts={'text': t, 'style': 'tag', 'w': 0.32, 'h': 0.12}, keys=[k(0.0, to=[x + 2.25, 0.98, -0.72], dur=st.dur('S12'), ease='linear')]) for i, (x, t) in enumerate(((-2.6, 'MAÏS'), (-0.65, 'BLÉ')))] +
              [P('douane', 'noticeBoard', pos=[0.1, 2.25, -2.0], opts={'text': 'DOUANE', 'style': 'sign', 'w': 0.7, 'h': 0.2})],
        cams=[cam(0.0, [-0.15, 1.3, 1.95], [0.15, 1.3, 1.75], [-0.3, 1.22, -1.0], [0.3, 1.22, -1.0], lens=46)])
for sid, kind in (('S13', 'steak'), ('S14', 'milk'), ('S15', 'cheese')):
    st.shot(sid, 'supermarket', actors=[SOY('soja', (0, 0, -2.0), 0, 'stiff', 'smug', keys=[k(0.45, expr='suspicious')])], props=[COSTUME('soja', kind, popAt=0.0)], cams=SHOP)
st.shot('S16', 'supermarket', actors=[SOY(a, (x, 0, z), 0, 'stiff', 'smug', scale=0.66) for a, x, z in (('soja2', -0.36, -2.55), ('soja', 0.0, -1.9), ('soja3', 0.36, -2.55))],
        props=[COSTUME(a, 'nugget') for a in ('soja', 'soja2', 'soja3')], cams=[cam(0.0, [0.25, 0.95, 0.75], [0.22, 0.95, 0.55], [0, 0.66, -2.1], [0, 0.67, -2.1], lens=44)])
# 17-19: working day and night in place of the cows, who went on holiday
st.shot('S17', 'supermarket', actors=[SOY('soja', (-1.3, 0, -2.2), 90, 'carryBox', 'sad', keys=[k(0.0, to=[1.0, 0, -2.2], dur=st.dur('S17'), clip='carryBox')])],
        props=[P('box', 'cardboardBox', on={'actor': 'soja', 'hand': 'R'}, scale=0.45), P('clock', 'wallClock', pos=[0.2, 2.3, -3.94], scale=1.1, opts={'rate': 5})],
        cams=[cam(0.0, [-0.45, 1.2, 1.2], [0.35, 1.2, 1.1], [-0.6, 1.1, -2.5], [0.6, 1.1, -2.5], lens=46)])
st.shot('S18', 'farm', actors=[SOY('soja', (0.15, 0, -1.0), 90, 'pour', 'happy'), act('vache', [-1.25, 0, -1.6], 75, 'idle'), act('vache2', [-0.55, 0, -2.6], 60, 'idle')],
        props=[P('jug', 'milkCarton', on={'actor': 'soja', 'hand': 'R'}, scale=1.4)] + [P(f'm{i}', 'milkCarton', pos=[0.52 + 0.16 * (i % 3), 0, -1.12 + 0.18 * (i // 3)], scale=1.2) for i in range(6)],
        cams=[cam(0.0, [0.95, 1.15, 3.3], [0.9, 1.18, 3.0], [0.0, 0.8, -1.4], [0.0, 0.82, -1.4], lens=46)])
st.shot('S19', 'beach', actors=[act('vache', [-0.7, 0, -1.5], 25, 'idle'), act('vache2', [0.85, 0, -1.9], -25, 'idle')],
        props=[P('para1', 'parasol', pos=[-1.15, 0, -2.25], opts={'openAt': 0}), P('para2', 'parasol', pos=[1.35, 0, -2.6], opts={'openAt': 0, 'colors': ['#2F62B5', '#F6F1E3']})],
        cams=[cam(0.0, [0.3, 1.0, 3.3], [0.28, 1.02, 3.0], [0.05, 0.95, -1.8], [0.05, 0.97, -1.8], lens=46)])
# 20-23: trial, prison
st.shot('S20', **JUDGE(0.42, 'TRIBUNAL'))
st.shot('S21', 'courtroom', actors=[SOY('soja', (0, 0, 0.8), 180, 'stand', 'sad'), act('flic', [0.75, 0, 1.0], 180, 'stand', 'unimpressed')],
        cams=[cam(0.0, [0.4, 1.35, -2.3], [0.38, 1.35, -2.05], [0.3, 1.05, 0.9], [0.3, 1.06, 0.9], lens=44)])
st.shot('S22', 'courtroom', props=[P('t', 'table', pos=[0, 0, 0.0], opts={'w': 2.0, 'd': 0.6})] + [P(f'ev{i}', 'soyCostume', pos=[x, 0.76 + 0.18, 0.0], scale=0.42, opts={'kind': k_}) for i, (x, k_) in enumerate(((-0.72, 'steak'), (-0.24, 'milk'), (0.24, 'cheese'), (0.72, 'nugget')))] +
        [P(f'tag{i}', 'noticeBoard', pos=[x, 0.84, 0.32], opts={'text': f'PIÈCE N° {i + 1}', 'style': 'tag', 'w': 0.26, 'h': 0.07}) for i, x in enumerate((-0.72, -0.24, 0.24, 0.72))],
        cams=[cam(0.0, [-0.55, 1.2, 1.55], [0.55, 1.2, 1.55], [-0.45, 0.98, 0.0], [0.45, 0.98, 0.0], lens=44, ease='inOut')])
st.shot('S23', 'brightCell', actors=[SOY('soja', (0, 0, 0.95), 0, 'stand', 'sad')], cams=[cam(0.0, [0.25, 0.95, 3.4], [0.22, 0.95, 3.15], [0, 0.72, 0.95], [0, 0.72, 0.95], lens=46)])
# 24-29: the man's turn, the canteen
st.shot('S24', 'policeStation', actors=[act('mec', [0.1, 0, 0.2], 0, 'cuffedFront', 'shocked'), act('flic', [-0.48, 0, 0.0], 40, 'cuffOther', 'smug')], props=[CUFFS('mec')], cams=MS(0, 0.2, h=1.55, d=2.8))
st.shot('S25', 'policeStation', props=[P('phone', 'phone911', pos=[0, 1.12, 0], rot=[0, 0, 0.06], scale=3.0, opts={'text': '17', 'sub': 'POLICE'}),
                                      P('abusif', 'noticeBoard', pos=[0, 1.45, 0.12], opts={'text': 'APPEL ABUSIF', 'style': 'sign', 'w': 0.62, 'h': 0.17, 'fg': '#C8322A', 'frame': '#C8322A', 'popAt': st.at('S25', 'L21', 8) - 0.05, 'tilt': -0.18})],
        cams=[cam(0.0, [0.02, 1.52, 1.62], [0.02, 1.52, 1.45], [0, 1.5, 0], [0, 1.5, 0], lens=42)])
CANTEEN = lambda: [P('menuwall', 'noticeBoard', pos=[-1.6, 1.7, -3.15], opts={'text': 'CANTINE', 'style': 'sign', 'w': 0.9, 'h': 0.25, 'bg': CHALK, 'fg': '#F4F4F0', 'frame': '#8A5A34'})]
st.shot('S26', 'proKitchen', actors=[act('mecP', [-0.5, 0, -0.05], 55, 'holdOut', 'surprised', keys=[k(0.35, expr='shocked')]), SOY('soja', (0.3, 0.32, -1.3), -40, 'stand', 'smug')],
        props=CANTEEN() + [P('tray', 'canteenTray', on={'actor': 'mecP', 'hand': 'R', **HAND_FLAT}), TOQUE()],
        cams=[cam(0.0, [0.62, 1.62, 2.95], [0.6, 1.62, 2.75], [-0.15, 1.35, -0.6], [-0.15, 1.35, -0.6], lens=46)])
st.shot('S27', 'proKitchen', actors=[SOY('soja', (0.3, 0.32, -1.35), 0, 'present', 'smug')], props=[TOQUE(), P('ladle', 'spoon', on={'actor': 'soja', 'hand': 'L'}, scale=2.0)],
        cams=[cam(0.0, [0.42, 1.38, 0.35], [0.4, 1.38, 0.18], [0.3, 1.22, -1.35], [0.3, 1.22, -1.35], lens=44)])
MENU_T = [('STEAK', 1.76, 3), ('LAIT', 1.54, 4), ('FROMAGE', 1.32, 5)]
st.shot('S28', 'proKitchen', props=[P('board', 'noticeBoard', pos=[0, 1.55, 0], opts={'text': ' ', 'style': 'sign', 'w': 0.9, 'h': 1.25, 'bg': CHALK, 'frame': '#8A5A34'}),
                                   P('title', 'noticeBoard', pos=[0, 2.02, 0.03], opts={'text': 'MENU', 'style': 'tag', 'w': 0.5, 'h': 0.15, 'bg': CHALK, 'fg': '#F4F4F0', 'frame': CHALK})] +
        [P(f'it{i}', 'noticeBoard', pos=[0, y, 0.03], opts={'text': t, 'style': 'tag', 'w': 0.6, 'h': 0.15, 'bg': CHALK, 'fg': '#F4F4F0', 'frame': CHALK, 'popAt': st.at('S28', 'L24', w) - 0.04}) for i, (t, y, w) in enumerate(MENU_T)] +
        [P('soy100', 'noticeBoard', pos=[0, 1.08, 0.03], opts={'text': '(100 % SOJA)', 'style': 'tag', 'w': 0.56, 'h': 0.11, 'bg': CHALK, 'fg': '#F2C94C', 'frame': CHALK, 'popAt': 2.2})],
        cams=[cam(0.0, [0.03, 1.56, 2.45], [0.03, 1.56, 2.3], [0, 1.55, 0], [0, 1.55, 0], lens=42)])
st.shot('S29', 'proKitchen', actors=[act('mecP', [-0.5, 0, -0.05], 60, 'holdOut', 'happy'), SOY('soja', (0.3, 0.32, -1.3), -45, 'present', 'smug')],
        props=CANTEEN() + [P('tray', 'canteenTray', on={'actor': 'mecP', 'hand': 'R', **HAND_FLAT}, opts={'extra': True}), TOQUE(), P('ladle', 'spoon', on={'actor': 'soja', 'hand': 'L'}, scale=2.0)],
        cams=[cam(0.0, [0.66, 1.62, 3.0], [0.62, 1.62, 2.75], [-0.15, 1.33, -0.6], [-0.15, 1.35, -0.6], lens=46)])
st.card('S07', "USURPATION D'IDENTITÉ"); st.card('S10', 'SOJA'); st.card('S21', 'TRAVAIL ILLÉGAL')
st.cue('sfx:ring', 'S01', 0.1, 0.3); st.cue('pop', 'S02', 0.3, 0.2); st.cue('sfx:gulp', 'S03', 0.5, 0.4); st.cue('sfx:gulp', 'S03', 1.1, 0.35)
st.cue('pop', 'S05', st.at('S05', 'L03', 9) - 0.08, 0.55); st.cue('sfx:gasp', 'S05', 0.7, 0.35); st.cue('sfx:grunt', 'S06', 0.2, 0.4); st.cue('thud', 'S06', 0.3, 0.5)
st.cue('thud', 'S07', 0.07, 0.45); st.cue('clack', 'S08', 0.45, 0.6); st.cue('sfx:beep', 'S09', 0.3, 0.25); st.cue('thud', 'S10', 0.07, 0.45); st.cue('pop', 'S10', 0.15, 0.5)
[st.cue('pop', 'S11', 0.2 + 0.18 * i, 0.22) for i in range(4)]; st.cue('engine', 'S12', 0.0, 0.2, st.dur('S12')); st.cue('sfx:tick', 'S12', 0.5, 0.25)
[st.cue('pop', s, 0.02, 0.4) for s in ('S13', 'S14', 'S15', 'S16')]; st.cue('sfx:ticks', 'S17', 0.0, 0.4); [st.cue('sfx:step', 'S17', t, 0.3) for t in (0.2, 0.6, 1.0)]
st.cue('sfx:pour', 'S18', 0.1, 0.4); st.cue('gust', 'S19', 0.0, 0.3, st.dur('S19')); st.cue('sfx:splash', 'S19', 0.6, 0.15)
st.cue('thud', 'S20', 0.42, 0.8); st.cue('thud', 'S21', 0.07, 0.45); st.cue('whoosh', 'S22', 0.1, 0.25, 1.2, 300, 1800); st.cue('clang', 'S23', 0.2, 0.5)
st.cue('sfx:cuff', 'S24', 0.3, 0.6); st.cue('clack', 'S25', st.at('S25', 'L21', 8) - 0.05, 0.6); st.cue('sfx:gasp', 'S26', 0.35, 0.4)
st.cue('sfx:bell', 'S27', 0.2, 0.25); [st.cue('pop', 'S28', st.at('S28', 'L24', w) - 0.04, 0.4) for w in (3, 4, 5)]; st.cue('pop', 'S28', 2.2, 0.3); st.cue('sfx:pour', 'S29', 0.4, 0.35)
st.write('Le burger vegan', {
    'serveur': {'preset': 'serveur'}, 'savant': {'preset': 'savant'},
    'flic': {'preset': 'cop', 'hair': 'crew', 'facial': 'mustache', 'seed': 41},
    'soja': {'type': 'creature', 'name': 'soja', 'opts': {'seed': 3}}, 'soja2': {'type': 'creature', 'name': 'soja', 'opts': {'seed': 5}},
    'soja3': {'type': 'creature', 'name': 'soja', 'opts': {'seed': 9}},
    'vache': {'type': 'creature', 'name': 'cow', 'opts': {'seed': 2}}, 'vache2': {'type': 'creature', 'name': 'cow', 'opts': {'seed': 7}},
    'mecP': {'preset': 'mecPrisonnier', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}})
