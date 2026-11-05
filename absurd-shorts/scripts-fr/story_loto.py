#!/usr/bin/env python3
"""Le loto: he wins ten million, paid in one-cent coins (a billion of them, a hundred trucks, his street buried); the bank refuses
them, so he pays everything in coins (a baguette, a car: the seller is still counting); the tax office claims three million, he pays
in coins, the agents count for six years and find a cent missing: tax adjustment; he pays the fine in coins, they recount: one cent
too many; they refund it, with a fifteen-euro handling fee. He paid in coins."""
from story_kit import *

st = Story('loto')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0),
         ('S08', 'L07', 0), ('S09', 'L08', 0), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L12', 0), ('S14', 'L13', 0),
         ('S15', 'L14', 0), ('S16', 'L15', 0), ('S17', 'L16', 0), ('S18', 'L17', 0), ('S19', 'L18', 0), ('S20', 'L19', 0), ('S21', 'L20', 0),
         ('S22', 'L21', 0), ('S23', 'L22', 0)])
ST = 'parisStreet'
SACK = lambda a, **kw: P(f'sack_{a}', 'moneySack', on={'actor': a, 'hand': 'R'}, scale=0.7, opts={'color': '#B89462'}, **kw)
DOC = lambda text, stamp=None, **kw: P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': text, 'style': 'doc', 'w': 0.72, 'h': 0.9, 'popAt': 0.1, 'textSize': 0.4, **({'stamp': stamp} if stamp else {}), **kw})
DOCCAM = [cam(0.0, [0.05, 1.55, 2.15], [0.05, 1.55, 1.95], [0, 1.5, 0], [0, 1.5, 0], lens=42)]
TAX = lambda: P('taxsign', 'noticeBoard', pos=[0.75, 2.62, -3.5], opts={'text': 'CENTRE DES IMPÔTS', 'style': 'sign', 'w': 1.6, 'h': 0.3, 'bg': '#203447', 'fg': '#F4F4F0', 'frame': '#F4F4F0'})
BEARD = lambda a, s0, s1, dur: P(f'beard_{a}', 'beard', on={'actor': a, 'joint': 'head', 'offset': [0, 0.03, 0.16]}, scale=s0, opts={'color': '#E9E6DE'}, keys=[k(0.0, scale=s1, dur=dur, ease='linear')])
AGENTS = [('agent', -0.95, -0.6), ('agent2', 0.0, -1.1), ('agent3', 0.95, -0.6)]
COUNT_ROOM = lambda s0, s1, dur: dict(actors=[act(a, [x, 0, z], 0, 'clickCount', 'sad') for a, x, z in AGENTS],
                                      props=[TAX(), P('clock', 'wallClock', pos=[1.5, 2.3, -3.5], scale=0.9, opts={'rate': 6})] +
                                            [P(f'desk{i}', 'table', pos=[x, 0, z + 0.55], opts={'w': 0.9, 'd': 0.5}) for i, (a, x, z) in enumerate(AGENTS)] +
                                            [P(f'heap{i}', 'coinHeap', pos=[x, 0.76, z + 0.55], opts={'R': 0.3, 'H': 0.22, 'n': 40, 'seed': 30 + i}) for i, (a, x, z) in enumerate(AGENTS)] +
                                            [P(f'cc{i}', 'clickCounter', on={'actor': a, 'hand': 'R'}) for i, (a, x, z) in enumerate(AGENTS)] +
                                            [BEARD(a, s0, s1, dur) for a, x, z in AGENTS])

# 1-6: the jackpot, in cents
st.shot('S01', 'livingRoom', actors=[act('mec', [0.28, 0, 0], 0, 'lookItem', 'surprised', keys=[k(0.55, expr='shocked')])],
        props=[P('ticket', 'noticeBoard', on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, opts={'text': 'LOTO\n7 12 23 31 44', 'style': 'tag', 'w': 0.2, 'h': 0.13})], cams=CU(0.08, 0, h=1.66, dx=0.12, d=1.8))
st.shot('S02', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'celebrate', 'happy')],
        props=[P('jackpot', 'noticeBoard', pos=[0.05, 2.25, 0.3], opts={'text': '10 000 000 €', 'style': 'sign', 'w': 0.9, 'h': 0.22, 'fg': '#2F7F4F', 'frame': '#2F7F4F', 'popAt': st.at('S02', 'L01', 4) - 0.05})],
        cams=LOW(0, 0, d=3.0, look_h=1.6, lens=52))
st.shot('S03', 'livingRoom', props=[P('t', 'table', pos=[0, 0, 0], opts={'w': 1.0, 'd': 0.7}), P('coin', 'centCoin', pos=[0, 0.76, 0.05], opts={'r': 0.07, 'spin': [0.05, 1.5]})],
        cams=[cam(0.0, [0.1, 1.02, 0.62], [0.08, 1.0, 0.5], [0, 0.84, 0.05], [0, 0.83, 0.05], lens=42)])
st.shot('S04', ST, actors=[act('mec', [6.6, 0, 3.2], 200, 'lookUp', 'shocked')], props=[P('heap', 'coinHeap', pos=[3.0, 0, -5.0], opts={'R': 6.5, 'H': 5.0, 'n': 900, 'coinR': 0.09})],
        cams=[cam(0.0, [8.3, 0.5, 9.6], [8.25, 0.55, 9.3], [4.0, 3.0, -4.0], [4.0, 3.2, -4.0], lens=56)])
st.shot('S05', ST, props=[P(f'truck{i}', 'dumpTruck', pos=[2.4, 0, -10.0 - 7.5 * i], rot=[0, -1.5708, 0], keys=[k(0.0, to=[2.4, 0, -5.0 - 7.5 * i], dur=st.dur('S05'), ease='linear')]) for i in range(4)],
        cams=[cam(0.0, [5.2, 0.6, 3.0], [5.1, 0.62, 2.7], [2.6, 1.6, -7.0], [2.6, 1.65, -6.0], lens=46, shake=0.012)])
st.shot('S06', ST, actors=[act('mec', [6.0, 1.0, 1.5], -20, 'bigShrug', 'unimpressed')],
        props=[P('layer', 'coinLayer', pos=[0, 0, 0], opts={'w': 20, 'd': 44, 'h': 1.0}), P('car1', 'car', pos=[3.8, -0.75, -3.0], rot=[0, 1.5708, 0], opts={'color': '#2F62B5'}),
               P('car2', 'car', pos=[-3.6, -0.7, -9.0], rot=[0, -1.5708, 0], opts={'color': '#F2D06B'})],
        cams=[cam(0.0, [7.0, 2.3, 5.6], [6.95, 2.35, 5.3], [4.6, 1.5, -2.5], [4.6, 1.55, -2.5], lens=46)])
# 7-11: the bank says no, so he pays everything in coins
st.shot('S07', 'bank', actors=[act('banquiere', [-1.2, 0, -2.1], 20, 'shakeHead', 'unimpressed'), act('mec', [0.05, 0, -0.95], -125, 'holdOut', 'suspicious')],
        props=[SACK('mec'), P('refuse', 'stampMark', pos=[-1.0, 1.55, -1.32], opts={'text': 'REFUSÉ', 'w': 0.5, 'h': 0.17}, keys=[k(0.0, scale=0.01), k(st.at('S07', 'L06', 3) - 0.05, scale=1.0, dur=0.2, ease='outBack')])],
        cams=[cam(0.0, [-0.85, 1.5, 1.7], [-0.88, 1.5, 1.45], [-0.75, 1.35, -1.6], [-0.75, 1.35, -1.6], lens=46)])
st.shot('S08', 'office', actors=[act('mec', [0.45, 0, 0.35], -60, 'pour', 'smug')],
        props=[P('counter', 'table', pos=[-0.15, 0, 0.0], opts={'w': 1.2, 'd': 0.6, 'h': 0.95}), SACK('mec'), P('heap', 'coinHeap', pos=[-0.25, 0.95, 0.0], opts={'R': 0.36, 'H': 0.3, 'n': 60, 'grow': [0.15, 1.6]})],
        cams=MS(0.1, 0.1, h=1.45, d=2.8))
st.shot('S09', 'office', actors=[act('boulanger', [-0.2, 0, -0.45], 0, 'clickCount', 'sad')],
        props=[P('counter', 'table', pos=[-0.1, 0, 0.15], opts={'w': 1.3, 'd': 0.6, 'h': 0.95, 'color': '#C9A27A'}), P('heap', 'coinHeap', pos=[0.2, 0.95, 0.2], opts={'R': 0.22, 'H': 0.14, 'n': 30, 'seed': 21}),
               P('bag', 'baguette', pos=[-0.4, 0.98, 0.25], rot=[0, 0.3, 0]), P('cc', 'clickCounter', on={'actor': 'boulanger', 'hand': 'R'}),
               P('sign', 'noticeBoard', pos=[0.3, 2.42, -1.2], opts={'text': 'BOULANGERIE', 'style': 'sign', 'w': 1.0, 'h': 0.24, 'bg': '#C9822E', 'fg': '#FFFFFF', 'frame': '#7A4A1A'}),
               P('price', 'noticeBoard', pos=[0.45, 1.25, 0.45], opts={'text': '1,10 €', 'style': 'tag', 'w': 0.3, 'h': 0.13, 'popAt': st.at('S09', 'L08', 3) - 0.05})],
        cams=MS(0, 0.15, h=1.5, d=2.9))
st.shot('S10', ST, actors=[act('mec', [6.0, 0, 1.4], -25, 'handsOnHips', 'smug')],
        props=[P('car', 'car', pos=[6.4, 0, -1.2], rot=[0, 0.3, 0], opts={'color': '#C9473A'}), P('tag', 'priceTag', pos=[6.95, 1.5, -0.6], scale=2.2, opts={'text': '20 000 €'}),
               P('heap', 'coinHeap', pos=[8.1, 0, 0.6], opts={'R': 1.5, 'H': 1.3, 'n': 160, 'coinR': 0.05})],
        cams=[cam(0.0, [6.8, 1.2, 6.0], [6.75, 1.22, 5.7], [6.8, 1.0, -0.3], [6.8, 1.02, -0.3], lens=46)])
st.shot('S11', ST, actors=[act('vendeur', [6.6, 0, 0.6], -10, 'sitFloor', 'sad')],
        props=[P('heap', 'coinHeap', pos=[7.9, 0, -0.4], opts={'R': 1.5, 'H': 1.3, 'n': 160, 'coinR': 0.05}), P('cc', 'clickCounter', on={'actor': 'vendeur', 'hand': 'R'}), BEARD('vendeur', 0.4, 1.6, st.dur('S11')),
               P('cal', 'calendar', pos=[5.6, 1.4, -1.0], scale=1.2, opts={'rate': 12})],
        cams=[cam(0.0, [6.95, 1.0, 3.0], [6.92, 1.0, 2.8], [6.9, 0.75, -0.2], [6.9, 0.75, -0.2], lens=46)])
# 12-17: the tax office: three million, paid in coins, counted for six years, one cent missing
st.shot('S12', 'office', actors=[act('agent', [0, 0, -0.4], 0, 'point', 'smug')], props=[TAX()], cams=MS(0, -0.4, h=1.6, d=2.9))
st.shot('S13', 'office', props=[DOC("AVIS D'IMPOSITION\n3 000 000 €", stamp='À PAYER')], cams=DOCCAM)
st.shot('S14', ST, actors=[act('agent', [8.6, 0, -2.2], -70, 'scared', 'shocked')],
        props=[P('front', 'signBoard', pos=[8.3, 0, -3.7], opts={'text': 'CENTRE DES IMPÔTS', 'w': 2.0, 'h': 0.42, 'height': 2.15, 'bg': '#203447', 'fg': '#F4F4F0', 'frame': '#F4F4F0'}),
               P('truck', 'dumpTruck', pos=[4.0, 0, -1.4], rot=[0, 3.1416, 0], opts={'tipAt': 0.25}), P('heap', 'coinHeap', pos=[7.0, 0, -1.4], opts={'R': 1.6, 'H': 1.2, 'n': 140, 'grow': [0.6, 2.0], 'coinR': 0.05})],
        cams=[cam(0.0, [6.3, 1.1, 6.6], [6.25, 1.12, 6.3], [6.6, 1.5, -2.0], [6.6, 1.55, -2.0], lens=48)])
st.shot('S15', 'office', **COUNT_ROOM(0.2, 0.9, st.dur('S15')), cams=WS(0, -0.6, h=1.55, d=5.6, look_h=1.35))
st.shot('S16', 'office', actors=[act('agent', [-0.3, 0, 0.2], 25, 'lookItem', 'shocked')],
        props=[TAX(), P('total', 'noticeBoard', pos=[0.35, 1.75, -0.4], opts={'text': 'TOTAL\n2 999 999,99 €', 'style': 'sign', 'w': 0.8, 'h': 0.36}),
               P('miss', 'noticeBoard', pos=[0.42, 1.38, -0.3], opts={'text': '− 0,01 €', 'style': 'tag', 'w': 0.36, 'h': 0.13, 'fg': '#C8322A', 'frame': '#C8322A', 'popAt': st.at('S16', 'L15', 3) - 0.05}),
               P('loupe', 'magnifyingGlass', on={'actor': 'agent', 'hand': 'R'}, scale=0.45), BEARD('agent', 0.95, 0.95, 0.1)],
        cams=MS(0.1, 0.0, h=1.6, d=2.9))
st.shot('S17', 'office', props=[DOC('REDRESSEMENT\nFISCAL', stamp='0,01 €')], cams=DOCCAM)
# 18-23: the fine in coins, a recount, one cent too many, the refund and its fee
st.shot('S18', 'office', actors=[act('mec', [0.55, 0, 0.45], -70, 'pour', 'smug'), act('agent', [-0.55, 0, -0.35], 30, 'facepalm', 'sad')],
        props=[TAX(), P('desk', 'table', pos=[0, 0, 0.0], opts={'w': 1.1, 'd': 0.6}), SACK('mec'), P('heap', 'coinHeap', pos=[0.0, 0.76, 0.0], opts={'R': 0.4, 'H': 0.32, 'n': 70, 'grow': [0.2, 1.8]}), BEARD('agent', 0.95, 0.95, 0.1)],
        cams=WS(0, 0.1, h=1.55, d=4.6, look_h=1.3))
st.shot('S19', 'office', **COUNT_ROOM(0.9, 1.7, st.dur('S19')), cams=WS(0, -0.6, h=1.6, d=5.4, look_h=1.4))
st.shot('S20', 'office', props=[P('desk', 'table', pos=[0, 0, 0], opts={'w': 1.0, 'd': 0.7}), P('coin', 'centCoin', pos=[0, 0.765, 0.06], rot=[-1.5708, 0, 0], opts={'r': 0.06}),
                               P('plus', 'noticeBoard', pos=[0.0, 0.855, -0.1], opts={'text': '+ 0,01 €', 'style': 'tag', 'w': 0.13, 'h': 0.05, 'fg': '#2F7F4F', 'frame': '#2F7F4F', 'popAt': st.at('S20', 'L19', 8) - 0.05})],
        cams=[cam(0.0, [0.06, 1.06, 0.48], [0.05, 1.03, 0.4], [0.03, 0.8, 0.0], [0.03, 0.8, 0.0], lens=42)])
st.shot('S21', 'office', actors=[act('agent', [-0.45, 0, 0.0], 70, 'giveItem', 'unimpressed'), act('mec', [0.5, 0, 0.1], -70, 'takeItem', 'suspicious')],
        props=[TAX(), P('coin', 'centCoin', on={'actor': 'agent', 'hand': 'R'}, opts={'r': 0.03}), BEARD('agent', 1.7, 1.7, 0.1)], cams=WS(0, 0.05, h=1.55, d=4.2, look_h=1.35))
st.shot('S22', 'office', props=[DOC('FRAIS DE DOSSIER\n15 €', stamp='À PAYER')], cams=DOCCAM)
st.shot('S23', ST, actors=[act('mec', [5.35, 0, 2.3], 25, 'handsOnHips', 'smug'), act('agent', [7.7, 0, -1.8], -40, 'surrender', 'shocked')],
        props=[P('front', 'signBoard', pos=[8.3, 0, -3.7], opts={'text': 'CENTRE DES IMPÔTS', 'w': 2.0, 'h': 0.42, 'height': 2.15, 'bg': '#203447', 'fg': '#F4F4F0', 'frame': '#F4F4F0'}),
               P('truck', 'dumpTruck', pos=[4.4, 0, -1.6], rot=[0, 3.1416, 0], opts={'tipAt': 0.2}), P('heap', 'coinHeap', pos=[7.6, 0, -1.8], opts={'R': 1.8, 'H': 1.35, 'n': 160, 'grow': [0.4, 2.0], 'coinR': 0.05}),
               BEARD('agent', 1.7, 1.7, 0.1)],
        cams=[cam(0.0, [5.85, 1.2, 7.6], [5.85, 1.25, 7.2], [6.45, 1.5, -1.5], [6.45, 1.55, -1.5], lens=50)])
st.card('S03', 'UN CENTIME'); st.card('S17', 'REDRESSEMENT FISCAL')
st.cue('sfx:paper', 'S01', 0.3, 0.3); st.cue('sfx:gasp', 'S01', 0.55, 0.4); st.cue('pop', 'S02', st.at('S02', 'L01', 4) - 0.05, 0.5); st.cue('sfx:fanfare', 'S02', 0.2, 0.35)
st.cue('thud', 'S03', 0.07, 0.45); st.cue('sfx:clink', 'S03', 0.1, 0.4); st.cue('sfx:clink', 'S03', 1.45, 0.45); st.cue('gust', 'S04', 0.0, 0.25, st.dur('S04'))
st.cue('engine', 'S05', 0.0, 0.45, st.dur('S05')); st.cue('sfx:brake', 'S05', 1.4, 0.3); st.cue('gust', 'S06', 0.0, 0.3, st.dur('S06'))
st.cue('clack', 'S07', st.at('S07', 'L06', 3) - 0.05, 0.6); st.cue('sfx:cash', 'S08', 0.3, 0.4); [st.cue('sfx:clink', 'S08', t, 0.3) for t in (0.4, 0.7, 1.0, 1.3)]
[st.cue('sfx:tick', 'S09', 0.2 + 0.25 * i, 0.3) for i in range(6)]; st.cue('pop', 'S09', st.at('S09', 'L08', 3) - 0.05, 0.4); st.cue('sfx:cash', 'S10', 0.4, 0.35)
st.cue('sfx:ticks', 'S11', 0.0, 0.4); st.cue('sfx:paper', 'S13', 0.1, 0.45); st.cue('thud', 'S13', 0.12, 0.35)
st.cue('engine', 'S14', 0.0, 0.35, st.dur('S14')); st.cue('sfx:clink', 'S14', 0.7, 0.5); st.cue('sfx:clink', 'S14', 1.1, 0.5); st.cue('sfx:gasp', 'S14', 0.9, 0.35)
st.cue('sfx:ticks', 'S15', 0.0, 0.45); st.cue('pop', 'S16', st.at('S16', 'L15', 3) - 0.05, 0.5); st.cue('thud', 'S17', 0.07, 0.45); st.cue('clack', 'S17', 0.5, 0.6)
[st.cue('sfx:clink', 'S18', t, 0.3) for t in (0.3, 0.6, 0.9, 1.2)]; st.cue('sfx:ticks', 'S19', 0.0, 0.45); st.cue('pop', 'S20', st.at('S20', 'L19', 8) - 0.05, 0.5); st.cue('sfx:bell', 'S20', st.at('S20', 'L19', 8), 0.2)
st.cue('sfx:clink', 'S21', 0.6, 0.35); st.cue('thud', 'S22', 0.12, 0.35); st.cue('clack', 'S22', 0.55, 0.6)
st.cue('engine', 'S23', 0.0, 0.35, st.dur('S23')); [st.cue('sfx:clink', 'S23', t, 0.45) for t in (0.6, 0.9, 1.2, 1.5)]
st.write('Le loto', {
    'banquiere': {'preset': 'femme'}, 'boulanger': {'preset': 'chef'}, 'vendeur': {'preset': 'lemec_brown'},
    'agent': {'preset': 'proviseur'}, 'agent2': {'preset': 'lemec_glasses', 'seed': 19}, 'agent3': {'preset': 'journaliste'}})
