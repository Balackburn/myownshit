#!/usr/bin/env python3
"""L'indépendance: he declares his flat independent (flag with his face, anthem, customs at his door: visas for his wife and the
postman); the neighbour disputes three centimetres of doormat: war (her music, his accordion); a UN mediator cuts the doormat in
two; peace. No money: he prints his own, with his face; the supermarket refuses it; he imports his shopping and pays customs duties
to himself. Then the landlord claims the rent: he asks for political asylum at the neighbour's. She asks him for a visa."""
from story_kit import *

st = Story('independance')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(2, 26)])
LAND = {'sofa': False, 'plant': False, 'tv': False, 'lamp': False}          # the landing: the living-room shell without furniture
D1, D2, ZD = -1.1, 1.25, -3.56                                             # his door, her door, the wall
def landing(gate=False, mat_split=None, line=False, her_gate=False, her_open=None):
    p = [P('door1', 'door', pos=[D1, 0, ZD], opts={'color': '#2F62B5'}), P('door2', 'door', pos=[D2, 0, ZD], opts={'color': '#B5302A', **({'openAt': her_open} if her_open is not None else {})}),
         P('rep', 'noticeBoard', pos=[D1, 2.48, ZD + 0.06], opts={'text': 'RÉPUBLIQUE\nDU 3e GAUCHE', 'style': 'sign', 'w': 0.9, 'h': 0.32, 'bg': '#2F8F7A', 'fg': '#F2C94C', 'frame': '#F2C94C'}),
         P('plaque', 'noticeBoard', pos=[D2, 2.32, ZD + 0.06], opts={'text': 'Mme RICHARD', 'style': 'tag', 'w': 0.5, 'h': 0.12}),
         P('flag', 'regionFlag', pos=[D1 - 0.95, 0, ZD + 0.3], scale=1.2, opts={'kind': 'mec'}),
         P('mat1', 'doormat', pos=[D1 + 0.12, 0, ZD + 0.5], opts={'line': line, **({'splitAt': mat_split} if mat_split is not None else {})}),
         P('mat2', 'doormat', pos=[D2, 0, ZD + 0.5], opts={'text': 'ENTREZ'})]
    if gate: p.append(P('gate', 'barrierGate', pos=[D1 - 0.85, 0, ZD + 1.15], scale=0.85, opts={'length': 1.3, 'angle': 0, 'sign': 'DOUANE'}))
    if her_gate: p.append(P('gate2', 'barrierGate', pos=[D2 - 0.75, 0, ZD + 1.15], scale=0.85, opts={'length': 1.3, 'angle': 0, 'sign': 'DOUANE'}))
    return p
WIDE = [cam(0.0, [0.12, 1.5, 3.4], [0.1, 1.52, 3.0], [0.07, 1.3, -3.0], [0.07, 1.32, -3.0], lens=50)]
SEAL = lambda pid, text, pos, at_, **kw: P(pid, 'stampMark', pos=pos, opts={'text': text, **kw}, keys=[k(0.0, scale=0.01), k(at_, scale=1.0, dur=0.2, ease='outBack')])
TAG = lambda pid, text, pos, at_=None, rot=None, **kw: P(pid, 'noticeBoard', pos=pos, **({'rot': rot} if rot else {}), opts={'text': text, 'style': 'tag', 'w': kw.pop('w', 0.6), 'h': kw.pop('h', 0.16), **({'popAt': at_} if at_ is not None else {}), **kw})

# 1-4: the declaration, the flag, the anthem
st.shot('S01', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'podiumTalk', 'smug')], props=[P('pod', 'podium', pos=[0, 0, 0.45], opts={'text': 'MON APPART'})], cams=MS(0, 0, h=1.55, d=2.9))
st.shot('S02', 'livingRoom', setOpts=LAND, props=landing(), cams=[cam(0.0, [D1 + 0.15, 1.55, -0.2], [D1 + 0.15, 1.57, -0.45], [D1, 1.75, ZD], [D1, 1.78, ZD], lens=46)])
st.shot('S03', 'livingRoom', setOpts=LAND, props=landing(),
        cams=[cam(0.0, [D1 - 0.85, 1.55, ZD + 3.4], [D1 - 0.85, 1.6, ZD + 3.15], [D1 - 0.85, 1.5, ZD + 0.4], [D1 - 0.85, 1.55, ZD + 0.4], lens=46)])
st.shot('S04', 'livingRoom', actors=[act('mec', [0.25, 0, 0.3], 0, 'salute', 'smug', keys=st.talk('L03', 'S04', 'smug')), act('femme', [-0.75, 0, -0.9], 25, 'facepalm', 'unimpressed')], cams=WS(0, 0, h=1.5, d=4.2, look_h=1.3))
# 5-7: customs at his door: a visa for his wife, a passport for the postman
st.shot('S05', 'livingRoom', setOpts=LAND, actors=[act('mecD', [D1, 0, ZD + 0.75], 0, 'stand', 'smug')], props=landing(gate=True), cams=WS(D1 + 0.2, ZD + 0.8, h=1.45, d=4.2, look_h=1.3))
st.shot('S06', 'livingRoom', setOpts=LAND, actors=[act('femme', [D1 - 0.25, 0, ZD + 2.0], 160, 'showPhone', 'unimpressed'), act('mecD', [D1 - 0.1, 0, ZD + 0.75], 10, 'holdOut', 'smug')],
        props=landing(gate=True) + [P('pp', 'idCard', on={'actor': 'femme', 'hand': 'R', **HAND_FLAT}, scale=2.5), SEAL('visa', 'VISA', [D1 - 0.15, 1.45, ZD + 1.45], st.at('S06', 'L05', 6) - 0.05)],
        cams=[cam(0.0, [D1 + 2.0, 1.5, ZD + 3.0], [D1 + 1.9, 1.5, ZD + 2.8], [D1 - 0.3, 1.35, ZD + 1.35], [D1 - 0.3, 1.35, ZD + 1.35], lens=46)])
st.shot('S07', 'livingRoom', setOpts=LAND, actors=[act('facteur', [D1 - 0.2, 0, ZD + 2.0], 160, 'carryBox', 'unimpressed'), act('mecD', [D1 - 0.15, 0, ZD + 0.75], 10, 'lookItem', 'suspicious')],
        props=landing(gate=True) + [P('box', 'cardboardBox', on={'actor': 'facteur', 'hand': 'R'}, scale=0.5), P('pp', 'idCard', on={'actor': 'mecD', 'hand': 'R', **HAND_FLAT}, scale=2.2),
                                     P('loupe', 'magnifyingGlass', on={'actor': 'mecD', 'hand': 'L'}, scale=0.4)],
        cams=[cam(0.0, [D1 + 2.0, 1.5, ZD + 3.0], [D1 + 1.9, 1.5, ZD + 2.8], [D1 - 0.3, 1.35, ZD + 1.35], [D1 - 0.3, 1.35, ZD + 1.35], lens=46)])
# 8-12: three centimetres of doormat: war
st.shot('S08', 'livingRoom', setOpts=LAND, actors=[act('voisine', [D2 + 0.1, 0, ZD + 1.0], -25, 'point', 'angry', keys=st.talk('L07', 'S08', 'angry'))], props=landing(line=True),
        cams=MS(D2 + 0.1, ZD + 1.0, h=1.4, d=2.6))
st.shot('S09', 'livingRoom', setOpts=LAND, props=landing(line=True) + [TAG('cm', '3 cm', [D1 + 0.3, 0.05, ZD + 0.62], st.at('S09', 'L08', 1) - 0.05, rot=[-1.5708, 0, 0], w=0.24, h=0.1)],
        cams=[cam(0.0, [D1 + 0.2, 1.2, ZD + 0.95], [D1 + 0.2, 1.1, ZD + 0.9], [D1 + 0.2, 0.0, ZD + 0.5], [D1 + 0.2, 0.0, ZD + 0.5], lens=42)])
st.shot('S10', 'livingRoom', setOpts=LAND, actors=[act('mec', [-0.35, 0, ZD + 1.2], 60, 'angryFist', 'angry'), act('voisine', [0.45, 0, ZD + 1.2], -60, 'angryFist', 'angry')], props=landing(line=True),
        cams=[cam(0.0, [0.1, 0.6, ZD + 4.0], [0.1, 0.62, ZD + 3.7], [0.05, 1.45, ZD + 1.2], [0.05, 1.5, ZD + 1.2], lens=50, shake=0.02)])
st.shot('S11', 'livingRoom', setOpts=LAND, actors=[act('voisine', [D2, 0, ZD + 1.0], 0, 'dance', 'happy')], props=landing(her_open=0.0) + [P('boom', 'boombox', on={'actor': 'voisine', 'hand': 'R'}, scale=1.4, opts={'playAt': 0, 'bpm': 128, 'text': 'FORT'})],
        cams=MS(D2, ZD + 1.0, h=1.4, d=2.8, shake=0.025))
st.shot('S12', 'livingRoom', setOpts=LAND, actors=[act('mec', [D1, 0, ZD + 1.0], 0, 'holdOut', 'smug')], props=landing() + [P('acc', 'accordion', pos=[D1, 1.12, ZD + 1.48], scale=1.15)],
        cams=MS(D1, ZD + 1.0, h=1.45, d=2.8))
# 13-15: the UN mediator cuts the doormat in two; peace
st.shot('S13', 'livingRoom', setOpts=LAND, actors=[act('mediateur', [0.05, 0, ZD + 3.2], 180, 'walk', 'smug', keys=[k(0.0, to=[0.05, 0, ZD + 1.5], dur=st.dur('S13'), clip='walk')]),
                                                act('mec', [D1, 0, ZD + 1.0], 40, 'armsCrossed', 'angry'), act('voisine', [D2, 0, ZD + 1.0], -40, 'armsCrossed', 'angry')],
        props=landing(line=True) + [P('wf', 'whiteFlag', on={'actor': 'mediateur', 'hand': 'R'}, scale=0.8)], cams=WIDE)
st.shot('S14', 'livingRoom', setOpts=LAND, actors=[act('mediateur', [D1 + 0.12, 0, ZD + 1.25], 180, 'holdOut', 'smug')],
        props=landing(mat_split=st.at('S14', 'L13', 2)) + [P('saw', 'chainsaw', on={'actor': 'mediateur', 'hand': 'R'}, scale=0.9, opts={'runAt': 0.0})],
        cams=[cam(0.0, [D1 + 1.9, 1.15, ZD + 2.3], [D1 + 1.8, 1.15, ZD + 2.15], [D1 + 0.1, 0.55, ZD + 0.75], [D1 + 0.1, 0.55, ZD + 0.75], lens=46)])
st.shot('S15', 'livingRoom', setOpts=LAND, actors=[act('mec', [-0.42, 0, ZD + 1.45], 60, 'giveItem', 'happy'), act('voisine', [0.5, 0, ZD + 1.45], -60, 'takeItem', 'happy'), act('mediateur', [0.05, 0, ZD + 0.55], 0, 'present', 'smug')],
        props=landing(mat_split=-1.0) + [TAG('treaty', 'TRAITÉ DE PAIX', [0.05, 2.5, ZD + 0.9], 0.2, w=0.8, h=0.18)], cams=WS(0.05, ZD + 1.1, h=1.55, d=4.6, look_h=1.5))
# 16-18: no money: his own banknotes, with his face
st.shot('S16', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'lookDown', 'sad')], props=[P('box', 'cardboardBox', pos=[0.05, 0, 0.55], scale=0.8), TAG('tresor', 'TRÉSOR NATIONAL', [0.05, 0.5, 0.86], None, w=0.5, h=0.12)],
        cams=[cam(0.0, [0.3, 1.35, 3.0], [0.28, 1.35, 2.75], [0.02, 0.95, 0.2], [0.02, 0.95, 0.2], lens=46)])
st.shot('S17', 'livingRoom', actors=[act('mec', [0.1, 0, -0.2], 0, 'explain', 'happy')],
        props=[P('t', 'table', pos=[0, 0, 0.45], opts={'w': 1.1, 'd': 0.6}), P('pc', 'laptop', pos=[-0.3, 0.76, 0.4], opts={'text': 'IMPRESSION\n100 %', 'fg': '#2F7F5C'})] +
              [P(f'n{i}', 'banknote', pos=[0.05 + 0.1 * (i % 3), 0.78 + 0.004 * i, 0.4 + 0.05 * (i // 3)], rot=[-1.5708, 0, 0.2 * (i - 2)], keys=[k(0.0, scale=0.01), k(0.25 + 0.3 * i, scale=1.0, dur=0.2, ease='outBack')]) for i in range(6)],
        cams=MS(0.05, 0.2, h=1.55, d=2.9))
st.shot('S18', 'livingRoom', props=[P('note', 'banknote', pos=[0, 1.5, 0], rot=[0, 0, 0.06], scale=1.6)], cams=[cam(0.0, [0.02, 1.52, 1.45], [0.02, 1.52, 1.3], [0, 1.5, 0], [0, 1.5, 0], lens=42)])
# 19-22: refused at the supermarket, imported shopping, duties paid to himself
st.shot('S19', 'supermarket', actors=[act('caissiere', [3.75, 0, 0.3], -90, 'shakeHead', 'unimpressed'), act('mec', [2.55, 0, 0.35], 90, 'showPhone', 'suspicious')],
        props=[P('note', 'banknote', on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, scale=0.8), SEAL('ref', 'REFUSÉ', [3.15, 1.98, 0.5], st.at('S19', 'L18', 3) - 0.05, w=0.45, h=0.15)],
        cams=[cam(0.0, [3.15, 1.45, 3.6], [3.15, 1.45, 3.35], [3.15, 1.3, 0.3], [3.15, 1.3, 0.3], lens=46)])
st.shot('S20', 'livingRoom', setOpts=LAND, actors=[act('mec', [D1 + 0.4, 0, ZD + 3.4], 180, 'carryBags', 'sad', keys=[k(0.0, to=[D1 + 0.25, 0, ZD + 2.0], dur=st.dur('S20'), clip='carryBags')])],
        props=landing(gate=True) + [P('bag1', 'shoppingBag', on={'actor': 'mec', 'hand': 'R'}, scale=0.9), P('bag2', 'shoppingBag', on={'actor': 'mec', 'hand': 'L'}, scale=0.9)],
        cams=[cam(0.0, [D1 + 3.0, 1.3, ZD + 2.9], [D1 + 2.9, 1.3, ZD + 2.7], [D1 + 0.35, 1.1, ZD + 2.9], [D1 + 0.25, 1.1, ZD + 2.1], lens=46)])
st.shot('S21', 'livingRoom', setOpts=LAND, actors=[act('mecD', [D1 - 0.1, 0, ZD + 0.75], 10, 'clipboard', 'smug')],
        props=landing(gate=True) + [P('bag', 'shoppingBag', pos=[D1 + 0.15, 0, ZD + 1.75], scale=1.1), TAG('droits', 'DROITS DE DOUANE\n20 %', [D1 + 0.1, 1.95, ZD + 1.4], st.at('S21', 'L20', 2) - 0.05, w=0.62, h=0.24)],
        cams=MS(D1, ZD + 1.2, h=1.5, d=3.2))
st.shot('S22', 'livingRoom', setOpts=LAND, actors=[act('mec', [D1 + 0.55, 0, ZD + 1.75], -110, 'giveItem', 'smug'), act('mecD', [D1 - 0.35, 0, ZD + 1.3], 70, 'takeItem', 'smug')],
        props=landing(gate=True) + [P('note', 'banknote', on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, scale=0.7)],
        cams=[cam(0.0, [D1 + 0.25, 1.45, ZD + 4.9], [D1 + 0.22, 1.47, ZD + 4.6], [D1 + 0.1, 1.3, ZD + 1.5], [D1 + 0.1, 1.32, ZD + 1.5], lens=46)])
# 23-26: the landlord and the rent; asylum at the neighbour's; she asks for a visa
st.shot('S23', 'livingRoom', setOpts=LAND, actors=[act('proprio', [D1 + 0.75, 0, ZD + 1.3], -110, 'point', 'angry', keys=st.talk('L22', 'S23', 'angry')), act('mec', [D1 - 0.25, 0, ZD + 1.0], 50, 'scared', 'scared')],
        props=landing() + [TAG('loyer', 'LOYER\nIMPAYÉ', [D1 + 0.7, 2.12, ZD + 1.3], 0.25, w=0.5, h=0.26, fg='#C8322A', frame='#C8322A')],
        cams=[cam(0.0, [D1 + 0.35, 1.5, ZD + 4.6], [D1 + 0.33, 1.5, ZD + 4.3], [D1 + 0.25, 1.4, ZD + 1.15], [D1 + 0.25, 1.4, ZD + 1.15], lens=46)])
st.shot('S24', 'livingRoom', setOpts=LAND, actors=[act('mec', [D2 - 0.25, 0, ZD + 1.25], 25, 'point', 'sad')],
        props=landing() + [P('case', 'briefcase', on={'actor': 'mec', 'hand': 'L'}), TAG('asile', 'ASILE\nPOLITIQUE', [D2 + 0.45, 2.1, ZD + 0.8], st.at('S24', 'L23', 4) - 0.05, w=0.5, h=0.26)],
        cams=MS(D2, ZD + 1.2, h=1.5, d=3.0))
st.shot('S25', 'livingRoom', setOpts=LAND, actors=[act('voisine', [D2 + 0.05, 0, ZD + 0.55], 0, 'handsOnHips', 'smug')], props=landing(her_open=-1.0) + [P('cap', 'copCap', on={'actor': 'voisine', 'joint': 'head', 'offset': [0, 0.44, 0]}, scale=1.0)],
        cams=MS(D2 + 0.05, ZD + 0.55, h=1.4, d=2.6))
st.shot('S26', 'livingRoom', setOpts=LAND, actors=[act('voisine', [D2 + 0.1, 0, ZD + 0.75], -20, 'holdOut', 'smug'), act('mec', [D2 - 0.75, 0, ZD + 1.95], 140, 'facepalm', 'sad')],
        props=landing(her_gate=True, her_open=-1.0) + [P('case', 'briefcase', on={'actor': 'mec', 'hand': 'L'}), P('cap', 'copCap', on={'actor': 'voisine', 'joint': 'head', 'offset': [0, 0.44, 0]}, scale=1.0),
                                                        TAG('visa', 'VISA ?', [D2 + 0.25, 2.12, ZD + 1.0], st.at('S26', 'L25', 5) - 0.05, w=0.4, h=0.16)],
        cams=[cam(0.0, [D2 + 0.5, 1.5, ZD + 5.2], [D2 + 0.46, 1.52, ZD + 4.9], [D2 - 0.25, 1.35, ZD + 1.3], [D2 - 0.25, 1.37, ZD + 1.3], lens=46)])
st.card('S01', 'INDÉPENDANCE'); st.card('S10', 'LA GUERRE')
st.cue('sfx:fanfare', 'S01', 0.2, 0.3); st.cue('pop', 'S02', 0.1, 0.4); st.cue('gust', 'S03', 0.0, 0.2, st.dur('S03')); st.cue('sfx:choir', 'S04', 0.0, 0.25)
st.cue('clack', 'S05', 0.3, 0.4); st.cue('clack', 'S06', st.at('S06', 'L05', 6) - 0.05, 0.6); st.cue('sfx:paper', 'S07', 0.4, 0.4); st.cue('sfx:grunt', 'S08', 0.3, 0.3)
st.cue('pop', 'S09', st.at('S09', 'L08', 1) - 0.05, 0.45); st.cue('thud', 'S10', 0.07, 0.45); st.cue('thunder', 'S10', 0.1, 0.3)
[st.cue('thud', 'S11', 0.1 + 0.47 * i, 0.35) for i in range(4)]; st.cue('sfx:squeak', 'S12', 0.2, 0.3); st.cue('sfx:squeak', 'S12', 0.8, 0.3)
[st.cue('sfx:step', 'S13', t, 0.35) for t in (0.2, 0.7, 1.2)]; st.cue('sfx:chainsaw', 'S14', 0.0, 0.45); st.cue('sfx:choir', 'S15', 0.1, 0.25); st.cue('pop', 'S15', 0.2, 0.4)
st.cue('sfx:sniff', 'S16', 0.5, 0.3); [st.cue('pop', 'S17', 0.25 + 0.3 * i, 0.2) for i in range(6)]; st.cue('sfx:cash', 'S18', 0.2, 0.3)
st.cue('clack', 'S19', st.at('S19', 'L18', 3) - 0.05, 0.6); [st.cue('sfx:step', 'S20', t, 0.35) for t in (0.2, 0.65, 1.1)]; st.cue('clack', 'S21', st.at('S21', 'L20', 2) - 0.05, 0.5)
st.cue('sfx:cash', 'S22', 0.5, 0.35); st.cue('thud', 'S23', 0.3, 0.3); [st.cue('sfx:step', 'S24', t, 0.3) for t in (0.3, 0.8)]; st.cue('sfx:carDoor', 'S25', 0.05, 0.3); st.cue('pop', 'S26', st.at('S26', 'L25', 5) - 0.05, 0.45)
st.write("L'indépendance", {
    'femme': {'preset': 'femme'}, 'facteur': {'preset': 'worker', 'atlasBody': False, 'suit': '#F2C230', 'pants': '#2C4A8A', 'hat': 'none'},
    'voisine': {'preset': 'mamie'}, 'mediateur': {'preset': 'politique', 'hat': 'hardhat', 'hatColor': '#4A90D9'}, 'proprio': {'preset': 'boss'},
    'caissiere': {'preset': 'femme', 'seed': 33, 'suit': '#B5302A'},
    'mecD': {'preset': 'lemec', 'hat': 'copcap', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}})
