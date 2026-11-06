#!/usr/bin/env python3
"""Le rendez-vous: he books an appointment with a dermatologist; next slot: 2031; he says yes and moves into the waiting room.
The magazines date from 1998 (he learns France won the World Cup and celebrates alone), his beard grows, a plant grows on his
chair, his mail is forwarded there, he marries the lady next to him (she was waiting for the eye doctor), they have a son who
passes his bac in the waiting room. In 2031 the secretary calls his name; the doctor asks what's wrong: a mole. It had gone.
The doctor billed him anyway: fifty euros, not reimbursed."""
from story_kit import *

st = Story('rdv')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5)] + [(f'S{i + 1:02d}', f'L{i:02d}', 0) for i in range(2, 6)] + [('S07', 'L05', 4)]
        + [(f'S{i + 2:02d}', f'L{i:02d}', 0) for i in range(6, 16)] + [('S18', 'L15', 2)] + [(f'S{i + 3:02d}', f'L{i:02d}', 0) for i in range(16, 21)])
PI = math.pi
WR = {'sofa': False, 'plant': False, 'tv': False, 'lamp': False}           # the waiting room: the living-room shell, furnished below
BK = -3.56                                                              # its back wall
SEATS = [-1.5, -0.75, 0.0, 0.75, 1.5]
CAL = [1.25, 2.45, BK + 0.04]                                           # the wall calendar, above the window
def room(cal=(2026, 2026), flip=None, dur=1.0, low_table=True):
    p = [P(f'ch{i}', 'chair', pos=[x, 0, BK + 0.55], opts={'color': '#2F7F7A'}) for i, x in enumerate(SEATS)]
    p += [P('sign', 'noticeBoard', pos=[-1.6, 2.15, BK + 0.06], opts={'text': "SALLE D'ATTENTE", 'style': 'sign', 'w': 1.25, 'h': 0.3, 'bg': '#F4F1E8', 'fg': '#2C4A8A', 'frame': '#2C4A8A'}),
          P('win', 'window', pos=[1.18, 1.0, BK + 0.01], opts={'w': 0.95, 'h': 0.72, 'clouds': True, 'color': '#2F7F7A'}),
          P('cal', 'yearCalendar', pos=CAL, opts={'years': list(cal), **({'flipAt': flip, 'dur': dur} if flip is not None else {})}),
          P('clock', 'wallClock', pos=[2.6, 2.3, BK + 0.03], opts={'rate': 0.6}), P('pot', 'plant', pos=[-2.4, 0, BK + 0.45])]
    if low_table: p += [P('ltab', 'table', pos=[0.0, 0, BK + 1.45], opts={'w': 1.1, 'd': 0.5, 'h': 0.42, 'color': '#C9A27A'}),
                        P('mag1', 'magazine', pos=[-0.25, 0.425, BK + 1.45], rot=[-PI / 2, 0, 0.3], opts={'w': 0.26}), P('mag2', 'magazine', pos=[0.18, 0.43, BK + 1.5], rot=[-PI / 2, 0, -0.5], opts={'w': 0.26, 'title': 'TÉLÉ MAG'})]
    return p
PLANT = lambda grow=False: P('vine', 'plant', pos=[-0.75, 0.46, BK + 0.6], **({'keys': [k(0.0, scale=0.05), k(0.2, scale=1.1, dur=1.1, ease='outBack')]} if grow else {'scale': 1.1}))
MAIL = [P('box', 'mailbox', pos=[-0.42, 0, BK + 1.15], scale=0.62, opts={'color': '#F2C230'}), P('mtag', 'noticeBoard', pos=[-0.42, 0.52, BK + 1.32], opts={'text': 'M. LE MEC', 'style': 'tag', 'w': 0.36, 'h': 0.1})]
BEARD = lambda s0, s1=None, at_=0.15, dur=1.0, col='#2A2420', actor='mec': P('beard', 'beard', on={'actor': actor, 'joint': 'head', 'offset': [0, 0.05, 0.12]}, opts={'color': col},
                                                                          keys=[k(0.0, scale=s0)] + ([k(at_, scale=s1, dur=dur)] if s1 is not None else []))
MASTER = [cam(0.0, [0.5, 1.45, BK + 5.6], [0.49, 1.45, BK + 5.45], [0.45, 1.32, BK + 0.6], [0.45, 1.32, BK + 0.6], lens=54)]   # the locked frame: years pile up in it
DOC = lambda text, stamp, size=0.3: P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': text, 'style': 'doc', 'w': 0.72, 'h': 0.9, 'popAt': 0.1, 'textSize': size, **({'stamp': stamp} if stamp else {})})
DOC_CAM = [cam(0.0, [0.05, 1.55, 2.15], [0.05, 1.55, 1.9], [0, 1.5, 0], [0, 1.5, 0], lens=42)]
SIT = lambda aid, x, clip='sit', expr='unimpressed', **kw: act(aid, [x, 0, BK + 0.55], 0, clip, expr, **kw)
MOLE = lambda: P('mole', 'mole', on={'actor': 'mec', 'joint': 'head', 'offset': [-0.075, 0.15, 0.135]})

# 1-4: the booking (the mole is on his right cheek)
st.shot('S01', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'phoneEar', 'happy')], props=[P('phone', 'handset', on={'actor': 'mec', 'hand': 'R'}), MOLE()], cams=CU(0, 0, h=1.78, d=1.75, dx=0.15))
st.shot('S02', 'livingRoom', setOpts=WR, props=[P('door', 'door', pos=[0, 0, BK], opts={'color': '#F4F1E8', 'frame': '#C9C2B2'}),
                                                 P('plq', 'noticeBoard', pos=[1.08, 1.55, BK + 0.05], opts={'text': 'DERMATOLOGUE', 'style': 'sign', 'w': 0.8, 'h': 0.22, 'bg': '#F4F1E8', 'fg': '#1C252A', 'frame': '#B9A06A'})],
        cams=[cam(0.0, [0.9, 1.5, BK + 2.9], [0.92, 1.5, BK + 2.6], [0.88, 1.42, BK], [0.9, 1.45, BK], lens=44)])
st.shot('S03', 'office', props=[DOC('RENDEZ-VOUS\nDERMATO\n\n2031', 'CONFIRMÉ', 0.28)], cams=DOC_CAM)
st.shot('S04', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'nod', 'grin')], props=[MOLE()], cams=MS(0, 0, h=1.55, d=2.4))
# 5-9: the waiting room; magazines from 1998; he celebrates alone
st.shot('S05', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0)], props=room(), cams=[cam(0.0, [0.45, 1.45, BK + 4.6], [0.42, 1.43, BK + 4.2], [0.25, 1.2, BK + 0.6], [0.25, 1.2, BK + 0.6], lens=46)])
st.shot('S06', 'livingRoom', setOpts=WR, props=room(), cams=[cam(0.0, [0.1, 1.05, BK + 2.3], [0.08, 1.0, BK + 2.2], [0.0, 0.42, BK + 1.45], [0.0, 0.42, BK + 1.45], lens=40)])
st.shot('S07', 'livingRoom', setOpts=WR, props=[P('mag', 'magazine', pos=[0, 1.3, BK + 1.2], opts={'w': 0.34})], cams=[cam(0.0, [0.02, 1.32, BK + 2.3], [0.02, 1.32, BK + 2.2], [0, 1.3, BK + 1.2], [0, 1.3, BK + 1.2], lens=40)])
GAGNE, COUPE = st.at('S08', 'L06', 7), st.at('S08', 'L06', 9)
st.shot('S08', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, 'sitLookItem', 'unimpressed', keys=[k(GAGNE, expr='surprised'), k(COUPE, expr='grin', clip='sitHoldUp')])],
        props=room() + [P('mag', 'magazine', on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, opts={'w': 0.3})],
        cams=[cam(0.0, [0.25, 1.32, BK + 3.15], [0.24, 1.32, BK + 2.95], [0.0, 1.25, BK + 0.55], [0.0, 1.25, BK + 0.55], lens=44),
              cam(round(COUPE, 3), [0.18, 1.55, BK + 2.2], [0.17, 1.55, BK + 2.1], [0.0, 1.55, BK + 0.55], [0.0, 1.56, BK + 0.55], lens=44)])
st.shot('S09', 'livingRoom', setOpts=WR, actors=[act('mecP', [0.0, 0, BK + 1.0], 0, 'celebrate', 'grin')], props=room(),
        cams=[cam(0.0, [0.3, 1.4, BK + 4.8], [0.28, 1.42, BK + 4.5], [0.0, 1.3, BK + 1.0], [0.0, 1.32, BK + 1.0], lens=44)])
# 10-16: years go by in one locked frame: beard, plant, mail, the wedding, the son, the bac
st.shot('S10', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, expr='sad')], props=room((2026, 2027), 0.2, 0.6) + [BEARD(0.25, 1.2, 0.15, 1.0)], cams=MASTER)
st.shot('S11', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0)], props=room((2027, 2028), 0.25, 0.6) + [BEARD(1.35), PLANT(grow=True)], cams=MASTER)
st.shot('S12', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, 'sitTake'), act('facteur', [0.75, 0, BK + 1.65], -120, 'giveItem', 'unimpressed')],
        props=room((2028, 2028)) + [BEARD(1.5), PLANT(), P('env', 'envelope', on={'actor': 'facteur', 'hand': 'R', **HAND_FLAT})] + MAIL, cams=MASTER)
st.shot('S13', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, 'sitTalk', 'grin'), SIT('mariee', 0.75, 'sitShow', 'happy')],
        props=room((2029, 2029)) + [BEARD(1.7), PLANT(), P('veil', 'veil', on={'actor': 'mariee', 'joint': 'head', 'offset': [0, 0.5, -0.02]}, scale=1.25), P('bq', 'flowers', on={'actor': 'mariee', 'hand': 'R'}, scale=1.0)] + MAIL,
        cams=[cam(0.0, [0.62, 1.55, BK + 3.3], [0.6, 1.56, BK + 3.05], [0.38, 1.32, BK + 0.55], [0.38, 1.33, BK + 0.55], lens=46)])
st.shot('S14', 'livingRoom', setOpts=WR, actors=[act('dame', [-0.95, 0, BK + 1.05], 200, 'lookItem', 'suspicious')],
        props=room() + [P('chart', 'eyeChart', pos=[-1.25, 1.55, BK + 0.04], opts={'w': 0.5}),
                        P('oph', 'noticeBoard', pos=[-0.32, 2.36, BK + 2.25], rot=[0, PI + 0.85, 0], opts={'text': 'OPHTALMO →', 'style': 'sign', 'w': 0.95, 'h': 0.24, 'bg': '#2C4A8A', 'fg': '#FFFFFF', 'frame': '#F4F1E8'})],
        cams=[cam(0.0, [-2.05, 1.78, BK + 0.3], [-2.0, 1.78, BK + 0.38], [-0.85, 1.9, BK + 1.3], [-0.85, 1.9, BK + 1.3], lens=48)])
st.shot('S15', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, expr='grin'), SIT('fils', 0.75, expr='happy'), SIT('dame', 1.5, expr='happy')],
        props=room((2030, 2030)) + [BEARD(1.9), PLANT()] + MAIL, cams=MASTER)
st.shot('S16', 'livingRoom', setOpts=WR, actors=[act('ado', [0.0, 0, BK + 0.95], 0, 'sitWrite', 'suspicious'), SIT('mec', -0.75, expr='unimpressed'), SIT('dame', 0.75, expr='unimpressed')],
        props=room(low_table=False) + [BEARD(2.2), P('chA', 'chair', pos=[0.0, 0, BK + 0.95], opts={'color': '#2F7F7A'}), P('desk16', 'table', pos=[0.0, 0, BK + 1.42], opts={'w': 0.8, 'd': 0.5, 'h': 0.72, 'color': '#C9A27A'}),
                                       P('pen', 'marker', on={'actor': 'ado', 'hand': 'R'}, opts={'color': '#2C4A8A'}),
                                       P('exam', 'noticeBoard', pos=[0.0, 0.735, BK + 1.42], rot=[-1.45, 0, 0], opts={'text': 'BAC\n2031', 'style': 'doc', 'w': 0.42, 'h': 0.5, 'textSize': 0.3})],
        cams=[cam(0.0, [0.3, 1.75, BK + 3.6], [0.28, 1.73, BK + 3.35], [0.0, 1.0, BK + 1.15], [0.0, 1.0, BK + 1.15], lens=46)])
# 17-18: 2031
st.shot('S17', 'livingRoom', setOpts=WR, props=room((2028, 2031), 0.05, 0.75), cams=[cam(0.0, [CAL[0] + 0.02, CAL[1] - 0.02, BK + 1.3], [CAL[0] + 0.01, CAL[1] - 0.03, BK + 1.18], [CAL[0], CAL[1] - 0.04, BK], [CAL[0], CAL[1] - 0.04, BK], lens=42)])
NOM = st.at('S18', 'L15', 7)
st.shot('S18', 'livingRoom', setOpts=WR, actors=[act('secretaire', [1.25, 0, BK + 1.5], -55, 'yell', 'unimpressed'), act('mec', [0.0, 0, BK + 0.95], 60, 'startle', 'shocked')],
        props=room((2031, 2031)) + [BEARD(3.0, col='#B8B4AC'), P('rdesk', 'desk', pos=[1.55, 0, BK + 1.5], rot=[0, -PI / 2, 0], opts={'w': 1.2}),
                                    P('secr', 'noticeBoard', pos=[1.62, 0.55, BK + 1.95], opts={'text': 'SECRÉTARIAT', 'style': 'tag', 'w': 0.7, 'h': 0.15}),
                                    P('call', 'noticeBoard', pos=[0.95, 2.35, BK + 1.55], opts={'text': 'M. LE MEC !', 'style': 'tag', 'w': 0.62, 'h': 0.17, 'popAt': round(NOM - 0.05, 3)})],
        cams=[cam(0.0, [0.75, 1.55, BK + 5.2], [0.74, 1.55, BK + 4.95], [0.65, 1.42, BK + 1.2], [0.65, 1.44, BK + 1.2], lens=48)])
# 19-23: the doctor; the mole had gone; the bill
DOCSET = [P('ddesk', 'desk', pos=[0, 0, -1.6]), P('dchair', 'chair', pos=[0.35, 0, -0.55], rot=[0, PI + 0.3, 0], opts={'color': '#3A3D44'})]
st.shot('S19', 'office', actors=[act('docteur', [0, 0, -2.2], 0, 'explain', 'suspicious', keys=st.talk('L16', 'S19', 'suspicious')), act('mec', [0.35, 0, -0.55], 160, 'sit', 'unimpressed')],
        props=DOCSET + [BEARD(3.0, col='#B8B4AC')], cams=[cam(0.0, [1.55, 1.45, 1.4], [1.48, 1.45, 1.2], [0.2, 1.25, -1.4], [0.2, 1.25, -1.4], lens=44)])
st.shot('S20', 'office', actors=[act('mec', [0.0, 0, 0.0], 0, 'pointCheek', 'unimpressed')],
        props=[BEARD(3.0, col='#B8B4AC'), P('ring', 'ringMark', on={'actor': 'mec', 'joint': 'head', 'offset': [-0.075, 0.15, 0.15]}, opts={'r': 0.05, 'popAt': 0.3})],
        cams=CU(0, 0, h=1.8, d=1.65, dx=0.1))
st.shot('S21', 'office', actors=[act('docteur', [-0.55, 0, 0.15], 60, 'lookItem', 'suspicious'), act('mec', [0.12, 0, 0.0], -20, 'stand', 'unimpressed')],
        props=[BEARD(3.0, col='#B8B4AC'), P('loupe', 'magnifyingGlass', pos=[0.02, 1.52, 0.33], scale=0.5),
               P('qm', 'questionMark', pos=[0.16, 1.98, 0.1], scale=0.5, keys=[k(0.0, scale=0.01), k(0.35, scale=0.5, dur=0.25, ease='outBack')])],
        cams=[cam(0.0, [0.1, 1.72, 2.3], [0.1, 1.73, 2.05], [-0.1, 1.72, 0.0], [-0.1, 1.73, 0.0], lens=44)])
st.shot('S22', 'office', actors=[act('docteur', [-0.45, 0, -0.1], 70, 'giveItem', 'smug'), act('mec', [0.45, 0, 0.0], -70, 'takeItem', 'sad')],
        props=[BEARD(3.0, col='#B8B4AC'), P('bill', 'envelope', on={'actor': 'docteur', 'hand': 'R', **HAND_FLAT}, scale=1.4, opts={'to': 'FACTURE', 'addr': '50 €'})],
        cams=[cam(0.0, [0.25, 1.55, 3.1], [0.24, 1.56, 2.85], [0.0, 1.55, 0.0], [0.0, 1.56, 0.0], lens=44)])
STAMP = st.at('S23', 'L20', 2)                                         # « Non remboursés »: the stamp slams in on the word
st.shot('S23', 'office', props=[DOC('FACTURE\n\n50 €', None, 0.34),
                                P('nr', 'stampMark', pos=[0.02, 1.2, 0.02], rot=[0, 0, 0.16], opts={'text': 'NON\nREMBOURSÉ', 'w': 0.56, 'h': 0.26},
                                  keys=[k(0.0, scale=0.01), k(round(STAMP - 0.03, 3), scale=0.01), k(round(STAMP, 3), scale=1.35, dur=0.07), k(round(STAMP + 0.07, 3), scale=1.0, dur=0.12)])],
        cams=DOC_CAM, fx=[{'type': 'shake', 'at': round(STAMP + 0.02, 3), 'dur': 0.16, 'amount': 0.02}])
st.card('S03', '2031'); st.card('S13', 'LE MARIAGE')
st.cue('sfx:ring', 'S01', 0.05, 0.3); st.cue('sfx:paper', 'S03', 0.1, 0.45); st.cue('clack', 'S03', 0.55, 0.5); st.cue('sfx:step', 'S05', 0.2, 0.3)
st.cue('sfx:paper', 'S07', 0.1, 0.35); st.cue('sfx:gasp', 'S08', GAGNE, 0.35); st.cue('pop', 'S08', COUPE, 0.3); st.cue('sfx:fanfare', 'S09', 0.15, 0.3); st.cue('sfx:ticks', 'S10', 0.0, 0.3)
st.cue('pop', 'S11', 0.3, 0.35); st.cue('sfx:paper', 'S12', 0.5, 0.35); st.cue('sfx:bell', 'S13', 0.2, 0.35); st.cue('sfx:choir', 'S13', 0.25, 0.22)
st.cue('sfx:spring', 'S15', 0.2, 0.25); st.cue('sfx:tick', 'S17', 0.1, 0.3); st.cue('pop', 'S18', NOM - 0.05, 0.4); st.cue('pop', 'S20', 0.3, 0.35); st.cue('pop', 'S21', 0.35, 0.4)
st.cue('sfx:cash', 'S22', 0.6, 0.4); st.cue('sfx:paper', 'S23', 0.1, 0.45); st.cue('thud', 'S23', STAMP, 0.6); st.cue('clack', 'S23', STAMP, 0.6)
st.write('Le rendez-vous', {
    'mecP': {'preset': 'lemec', 'hat': 'party', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'facteur': {'preset': 'worker', 'atlasBody': False, 'suit': '#F2C230', 'pants': '#2C4A8A', 'hat': 'none'},
    'dame': {'preset': 'madame', 'glasses': True, 'seed': 12}, 'mariee': {'preset': 'madame', 'glasses': True, 'seed': 12, 'suit': '#F4F2EC'},
    'fils': {'preset': 'gamin', 'seed': 21}, 'ado': {'preset': 'lyceen', 'seed': 22},
    'secretaire': {'preset': 'femme', 'seed': 5, 'suit': '#C9729A'}, 'docteur': {'preset': 'doctor', 'glasses': True}})
