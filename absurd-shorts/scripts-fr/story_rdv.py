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
def room(cal=(2026, 2026), flip=None, dur=1.0, extra_chairs=True):
    p = [P(f'ch{i}', 'chair', pos=[x, 0, BK + 0.55], opts={'color': '#2F7F7A'}) for i, x in enumerate(SEATS) if extra_chairs or x == 0.0]
    p += [P('sign', 'noticeBoard', pos=[-1.6, 2.15, BK + 0.06], opts={'text': "SALLE D'ATTENTE", 'style': 'sign', 'w': 1.25, 'h': 0.3, 'bg': '#F4F1E8', 'fg': '#2C4A8A', 'frame': '#2C4A8A'}),
          P('cal', 'yearCalendar', pos=[1.45, 1.8, BK + 0.04], opts={'years': list(cal), **({'flipAt': flip, 'dur': dur} if flip is not None else {})}),
          P('clock', 'wallClock', pos=[2.35, 2.25, BK + 0.03], opts={'rate': 0.6}), P('ltab', 'table', pos=[0.0, 0, BK + 1.45], opts={'w': 1.1, 'd': 0.5, 'h': 0.42, 'color': '#C9A27A'}),
          P('mag1', 'magazine', pos=[-0.25, 0.425, BK + 1.45], rot=[-PI / 2, 0, 0.3], opts={'w': 0.26}), P('mag2', 'magazine', pos=[0.18, 0.43, BK + 1.5], rot=[-PI / 2, 0, -0.5], opts={'w': 0.26, 'title': 'TÉLÉ MAG'}),
          P('pot', 'plant', pos=[-2.4, 0, BK + 0.45])]
    return p
BEARD = lambda s0, s1=None, at_=0.15, dur=1.0, col='#2A2420', actor='mec': P('beard', 'beard', on={'actor': actor, 'joint': 'head', 'offset': [0, 0.05, 0.12]}, opts={'color': col},
                                                                          keys=[k(0.0, scale=s0)] + ([k(at_, scale=s1, dur=dur)] if s1 is not None else []))
SEATCAM = lambda d=3.4, h=1.3, x=0.0, dx=0.25, ly=0.95, lens=44: [cam(0.0, [x + dx, h, BK + 0.55 + d], [x + dx * 0.9, h, BK + 0.55 + d - 0.3], [x, ly, BK + 0.55], [x, ly + 0.01, BK + 0.55], lens=lens)]
DOC = lambda text, stamp, size=0.3: P('doc', 'noticeBoard', pos=[0, 1.5, 0], opts={'text': text, 'style': 'doc', 'w': 0.72, 'h': 0.9, 'popAt': 0.1, 'textSize': size, 'stamp': stamp})
DOC_CAM = [cam(0.0, [0.05, 1.55, 2.15], [0.05, 1.55, 1.95], [0, 1.5, 0], [0, 1.5, 0], lens=42)]
SIT = lambda aid, x, clip='sit', expr='unimpressed', **kw: act(aid, [x, 0, BK + 0.55], 0, clip, expr, **kw)

# 1-4: the booking
st.shot('S01', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'phoneCall', 'happy')], cams=CU(0, 0, h=1.75, d=1.8))
st.shot('S02', 'livingRoom', setOpts=WR, props=[P('door', 'door', pos=[0, 0, BK], opts={'color': '#F4F1E8', 'frame': '#C9C2B2'}),
                                                 P('plq', 'noticeBoard', pos=[1.08, 1.55, BK + 0.05], opts={'text': 'DERMATOLOGUE', 'style': 'sign', 'w': 0.8, 'h': 0.22, 'bg': '#F4F1E8', 'fg': '#1C252A', 'frame': '#B9A06A'})],
        cams=[cam(0.0, [0.9, 1.5, BK + 2.9], [0.92, 1.5, BK + 2.6], [0.88, 1.42, BK], [0.9, 1.45, BK], lens=44)])
st.shot('S03', 'office', props=[DOC('RENDEZ-VOUS\nDERMATO\n\n2031', 'CONFIRMÉ', 0.28)], cams=DOC_CAM)
st.shot('S04', 'livingRoom', actors=[act('mec', [0, 0, 0], 0, 'nod', 'happy')], cams=MS(0, 0, h=1.5, d=2.6))
# 5-9: the waiting room; magazines from 1998; he celebrates alone
st.shot('S05', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0)], props=room(), cams=[cam(0.0, [0.45, 1.45, BK + 4.6], [0.42, 1.43, BK + 4.2], [0.0, 1.15, BK + 0.6], [0.0, 1.15, BK + 0.6], lens=44)])
st.shot('S06', 'livingRoom', setOpts=WR, props=room(), cams=[cam(0.0, [0.1, 1.05, BK + 2.3], [0.08, 1.0, BK + 2.2], [0.0, 0.42, BK + 1.45], [0.0, 0.42, BK + 1.45], lens=40)])
st.shot('S07', 'livingRoom', setOpts=WR, props=[P('mag', 'magazine', pos=[0, 1.3, BK + 1.2], opts={'w': 0.34})], cams=[cam(0.0, [0.02, 1.32, BK + 1.95], [0.02, 1.32, BK + 1.85], [0, 1.3, BK + 1.2], [0, 1.3, BK + 1.2], lens=40)])
st.shot('S08', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, 'sitLookItem', 'shocked', keys=[k(st.at('S08', 'L06', 5), expr='happy')])],
        props=room() + [P('mag', 'magazine', on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, opts={'w': 0.3})], cams=SEATCAM(2.6, 1.3))
st.shot('S09', 'livingRoom', setOpts=WR, actors=[act('mecP', [0.0, 0, BK + 1.0], 0, 'celebrate', 'happy')], props=room(),
        cams=[cam(0.0, [0.3, 1.4, BK + 4.8], [0.28, 1.42, BK + 4.5], [0.0, 1.3, BK + 1.0], [0.0, 1.32, BK + 1.0], lens=44)])
# 10-16: years go by: beard, plant, mail, the wedding, the son, the bac
st.shot('S10', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, expr='sad')], props=room((2026, 2027), 0.2, 0.6) + [BEARD(0.25, 1.2, 0.15, 1.0)], cams=SEATCAM(2.4, 1.3))
st.shot('S11', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0)], props=room((2027, 2028), 0.3, 0.6) + [BEARD(1.35), P('vine', 'plant', pos=[0.75, 0.46, BK + 0.6], keys=[k(0.0, scale=0.05), k(0.2, scale=1.1, dur=1.1, ease='outBack')])],
        cams=SEATCAM(2.6, 1.3, x=0.35))
st.shot('S12', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, 'sitTake'), act('facteur', [0.75, 0, BK + 1.5], -130, 'giveItem', 'unimpressed')],
        props=room() + [BEARD(1.5), P('env', 'envelope', on={'actor': 'facteur', 'hand': 'R', **HAND_FLAT}), P('box', 'mailbox', pos=[-0.55, 0, BK + 0.75], scale=0.75, opts={'color': '#F2C230'}),
                        P('mtag', 'noticeBoard', pos=[-0.55, 0.62, BK + 0.95], opts={'text': 'M. LE MEC', 'style': 'tag', 'w': 0.32, 'h': 0.1})],
        cams=[cam(0.0, [0.25, 1.35, BK + 4.2], [0.23, 1.35, BK + 3.95], [0.1, 0.95, BK + 0.9], [0.1, 0.96, BK + 0.9], lens=46)])
st.shot('S13', 'livingRoom', setOpts=WR, actors=[SIT('mec', 0.0, 'sitTalk', 'happy'), SIT('dame', 0.75, 'sitShow', 'happy')],
        props=room() + [BEARD(1.7), P('veil', 'veil', on={'actor': 'dame', 'joint': 'head', 'offset': [0, 0.42, -0.02]}), P('bq', 'flowers', on={'actor': 'dame', 'hand': 'R'}, scale=0.9)],
        cams=SEATCAM(3.0, 1.45, x=0.38, ly=1.15))
st.shot('S14', 'livingRoom', setOpts=WR, actors=[act('dame', [-1.15, 0, BK + 0.95], 152, 'lookItem', 'suspicious')],
        props=room() + [P('chart', 'eyeChart', pos=[-1.25, 1.55, BK + 0.04], opts={'w': 0.5}), P('oph', 'noticeBoard', pos=[-1.25, 2.28, BK + 0.06], opts={'text': 'OPHTALMO →', 'style': 'tag', 'w': 0.6, 'h': 0.13})],
        cams=[cam(0.0, [0.75, 1.75, BK + 1.4], [0.65, 1.75, BK + 1.35], [-1.2, 1.72, BK + 0.6], [-1.2, 1.72, BK + 0.6], lens=46)])
st.shot('S15', 'livingRoom', setOpts=WR, actors=[SIT('mec', -0.75, expr='happy'), SIT('fils', 0.0, expr='happy'), SIT('dame', 0.75, expr='happy')], props=room() + [BEARD(1.9)],
        cams=SEATCAM(3.4, 1.35, ly=1.0, lens=48))
st.shot('S16', 'livingRoom', setOpts=WR, actors=[act('ado', [0.0, 0, BK + 1.0], 0, 'sitWrite', 'suspicious'), SIT('mec', -0.75, expr='unimpressed'), SIT('dame', 0.75, expr='unimpressed')],
        props=room() + [BEARD(2.2), P('chA', 'chair', pos=[0.0, 0, BK + 1.0], opts={'color': '#2F7F7A'}),
                        P('exam', 'noticeBoard', pos=[0.0, 0.44, BK + 1.42], rot=[-1.25, 0, 0], opts={'text': 'BAC\n2031', 'style': 'doc', 'w': 0.3, 'h': 0.38, 'textSize': 0.26})],
        cams=[cam(0.0, [0.3, 1.5, BK + 4.2], [0.28, 1.5, BK + 3.9], [0.0, 0.9, BK + 1.1], [0.0, 0.9, BK + 1.1], lens=44)])
# 17-18: 2031
st.shot('S17', 'livingRoom', setOpts=WR, props=room((2028, 2031), 0.05, 0.75), cams=[cam(0.0, [1.47, 1.82, BK + 1.25], [1.46, 1.81, BK + 1.15], [1.45, 1.78, BK], [1.45, 1.78, BK], lens=42)])
st.shot('S18', 'livingRoom', setOpts=WR, actors=[act('secretaire', [1.45, 0, BK + 1.6], -90, 'yell', 'unimpressed'), act('mec', [0.0, 0, BK + 0.95], 70, 'startle', 'shocked')],
        props=room((2031, 2031)) + [BEARD(3.0, col='#B8B4AC'), P('rdesk', 'desk', pos=[1.75, 0, BK + 1.6], rot=[0, -PI / 2, 0], opts={'w': 1.2}),
                                    P('secr', 'noticeBoard', pos=[1.75, 1.32, BK + 2.25], opts={'text': 'SECRÉTARIAT', 'style': 'tag', 'w': 0.7, 'h': 0.15})],
        cams=[cam(0.0, [0.85, 1.5, BK + 5.3], [0.84, 1.5, BK + 5.0], [0.78, 1.3, BK + 1.2], [0.78, 1.32, BK + 1.2], lens=50)])
# 19-23: the doctor; the mole had gone; the bill
DOCSET = [P('ddesk', 'desk', pos=[0, 0, -1.6]), P('dchair', 'chair', pos=[0.35, 0, -0.55], rot=[0, PI + 0.3, 0], opts={'color': '#3A3D44'})]
st.shot('S19', 'office', actors=[act('docteur', [0, 0, -2.2], 0, 'explain', 'suspicious', keys=st.talk('L16', 'S19', 'suspicious')), act('mec', [0.35, 0, -0.55], 160, 'sit', 'unimpressed')],
        props=DOCSET + [BEARD(3.0, col='#B8B4AC')], cams=[cam(0.0, [1.55, 1.45, 1.4], [1.48, 1.45, 1.2], [0.2, 1.25, -1.4], [0.2, 1.25, -1.4], lens=44)])
st.shot('S20', 'office', actors=[act('mec', [0.0, 0, 0.0], 0, 'pointSelf', 'unimpressed')], props=[BEARD(3.0, col='#B8B4AC')], cams=CU(0, 0, h=1.72, d=1.9))
st.shot('S21', 'office', actors=[act('docteur', [-0.55, 0, 0.1], 60, 'lookItem', 'suspicious'), act('mec', [0.12, 0, 0.0], -20, 'stand', 'unimpressed')],
        props=[BEARD(3.0, col='#B8B4AC'), P('loupe', 'magnifyingGlass', on={'actor': 'docteur', 'hand': 'R'}, scale=0.7), P('qm', 'questionMark', pos=[-0.2, 2.15, 0.1], scale=0.6, keys=[k(0.0, scale=0.01), k(0.35, scale=0.6, dur=0.25, ease='outBack')])],
        cams=[cam(0.0, [0.05, 1.68, 2.3], [0.05, 1.7, 2.05], [-0.18, 1.6, 0.0], [-0.18, 1.62, 0.0], lens=44)])
st.shot('S22', 'office', actors=[act('docteur', [-0.45, 0, -0.1], 70, 'giveItem', 'smug'), act('mec', [0.45, 0, 0.0], -70, 'takeItem', 'sad')],
        props=[BEARD(3.0, col='#B8B4AC'), P('bill', 'envelope', on={'actor': 'docteur', 'hand': 'R', **HAND_FLAT}, opts={'to': 'FACTURE', 'addr': 'Dr — DERMATO'})],
        cams=MS(0, 0, h=1.45, d=3.0))
st.shot('S23', 'office', props=[DOC('FACTURE\n\n50 €', 'NON REMBOURSÉ', 0.34)], cams=DOC_CAM)
st.card('S03', '2031'); st.card('S13', 'LE MARIAGE')
st.cue('sfx:ring', 'S01', 0.05, 0.3); st.cue('sfx:paper', 'S03', 0.1, 0.45); st.cue('clack', 'S03', 0.55, 0.5); st.cue('sfx:step', 'S05', 0.2, 0.3)
st.cue('sfx:paper', 'S07', 0.1, 0.35); st.cue('sfx:gasp', 'S08', 0.3, 0.35); st.cue('sfx:fanfare', 'S09', 0.15, 0.3); st.cue('sfx:ticks', 'S10', 0.0, 0.3)
st.cue('pop', 'S11', 0.3, 0.35); st.cue('sfx:paper', 'S12', 0.5, 0.35); st.cue('sfx:bell', 'S13', 0.2, 0.35); st.cue('sfx:choir', 'S13', 0.25, 0.22)
st.cue('sfx:spring', 'S15', 0.2, 0.25); st.cue('sfx:tick', 'S17', 0.1, 0.3); st.cue('sfx:ring', 'S18', 0.6, 0.3); st.cue('pop', 'S21', 0.35, 0.4)
st.cue('sfx:cash', 'S22', 0.6, 0.4); st.cue('sfx:paper', 'S23', 0.1, 0.45); st.cue('clack', 'S23', 0.55, 0.5)
st.write('Le rendez-vous', {
    'mecP': {'preset': 'lemec', 'hat': 'party', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'facteur': {'preset': 'worker', 'atlasBody': False, 'suit': '#F2C230', 'pants': '#2C4A8A', 'hat': 'none'},
    'dame': {'preset': 'madame', 'glasses': True, 'seed': 12}, 'fils': {'preset': 'gamin', 'seed': 21}, 'ado': {'preset': 'lyceen', 'seed': 22},
    'secretaire': {'preset': 'femme', 'seed': 5, 'suit': '#C9729A'}, 'docteur': {'preset': 'doctor', 'glasses': True}})
