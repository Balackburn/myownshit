#!/usr/bin/env python3
"""LE TICKET. Ce mec takes a queue ticket at the post office to send a parcel -> number 4000 -> the counter is at 12 -> he
waits -> his beard grows, his hair falls out -> at sixty-five his number finally comes up -> "C'est midi. On ferme." ->
ce con sues for unlawful confinement -> the post office is ordered to pay his bloody pension -> by registered letter, to
collect at the counter -> he took a ticket. (Classic formula, no news gags.)"""
from actu_common import *

TM = [3.6, 0, -0.3]                            # ticket dispenser (faces front-left)
AT_TM = [3.25, 0, 0.32]                        # standing in front of it
CHAIR = [-0.8, 0.12, 0.78]                     # sitting on a waiting chair (chairs at z 0.9 face the counters)
WIN = [0, 0, -1.62]                            # at counter window 2
BEARD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.02, 0.1]}
CAP = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.545, -0.005]}
DISPLAY = [0, 2.72, -3.35]
scenes = []
scenes.append({
  'id': 'poste', 'set': 'poste', 'ambience': 'station', 'ambienceVol': 0.6,
  'daynight': {'from': 'P4', 'period': 0.55},
  'crowd': [{'id': 'att', 'count': 4, 'spec': {'preset': 'lemec_charcoal', 'seed': 71}, 'clip': 'sit', 'ry': 180, 'positions': [[-2.6, 0.12, 0.78], [1.0, 0.12, 0.78], [-1.7, 0.12, 1.98], [0.1, 0.12, 1.98]]}],
  'lines': [L('P1', "Ce mec a pris un ticket à la poste pour envoyer un colis.", highlight=['ticket', 'colis.']),
            L('P2', "Numéro quatre mille.", highlight=['quatre', 'mille.']),
            L('P3', "Au guichet, on en était au douze.", highlight=['douze.']),
            L('P4', "Il a attendu."),
            L('P5', "Sa barbe a poussé. Ses cheveux sont tombés.", highlight=['barbe', 'tombés.']),
            L('P6', "À soixante-cinq ans, son numéro est enfin sorti.", highlight=['soixante-cinq', 'sorti.']),
            L('P7', "C'est midi. On ferme.", 'guichetiere')],
  'actors': [
    act('mec', [5.4, 0, 2.0], -60, 'idle', 'happy', keys=[
        k(0.1, to=AT_TM, clip='walk', speed=1.8, faceEnd=151, then='stand'),
        k('P1:ticket', clip='takeItem', expr='happy'),
        k('P2', face=10, turn=0.2, clip='showPhone', expr='neutral'),
        k('P3', to=CHAIR, glide=True, dur=0.05, face=180, clip='sit', then='sit', expr='neutral'),
        k('P5', expr='sad'), k('P5:tombés', expr='sleepy'),
        k('P6:sorti', to=[-0.8, 0, 0.55], glide=True, dur=0.05, face=180, clip='stand', then='stand', expr='shocked'),
        k('P6:sorti+0.25', to=WIN, clip='sneak', speed=1.0, faceEnd=180, then='stand', expr='happy'),
        k('P7', expr='shocked')]),
    act('guichetiere', [0, 0, -2.85], 0, 'idle', 'neutral', keys=[k('P7', clip='talk', expr='unimpressed')]),
  ],
  'props': [P('colis', 'cardboardBox', scale=0.45, visible=True, opts={'text': 'FRAGILE'}, on={'actor': 'mec', 'hand': 'L', 'offset': [0, -0.15, 0.08]}, keys=[k('P2', visible=False)]),
            P('ticket', 'queueTicket', scale=1.6, visible=False, opts={'num': '4000'}, on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('P1:ticket+0.2', visible=True), k('P3', visible=False)]),
            P('ecran', 'queueDisplay', pos=DISPLAY, opts={'num': '12', 'num2': '4000', 'switchAt': 'P6:numéro'}),
            P('horloge', 'wallClock', scale=1.0, pos=[3.9, 2.4, -3.37], opts={'rate': 0}, alt={'opts': {'rate': 3}, 'at': 'P4'}),
            P('barbe', 'beard', scale=0.05, visible=False, opts={'color': '#E6E2D8'}, on=BEARD, keys=[k('P5', visible=True), k('P5', scale=2.3, dur=1.2, ease='out')]),
            P('crane', 'baldCap', visible=False, opts={'w': 0.235, 'd': 0.215, 'color': '#E8B88E'}, on=CAP, keys=[k('P5:cheveux', visible=True)]),
            P('ferme', 'signBoard', scale=0.6, visible=False, pos=[0, 1.12, -2.2], opts={'text': 'FERMÉ', 'bg': '#B5302A', 'fg': '#F6F1E3', 'w': 0.9, 'h': 0.35, 'height': 0.0}, keys=[k('P7:ferme', visible=True)])],
  'sfx': [{'at': 'P1:ticket', 'name': 'paper', 'vol': 0.5}, {'at': 'P4', 'name': 'ticks', 'vol': 0.6}, {'at': 'P4+1.4', 'name': 'ticks', 'vol': 0.6},
          {'at': 'P6:numéro', 'name': 'bell', 'vol': 0.7}, {'at': 'P7:ferme', 'name': 'thud', 'vol': 0.6}],
  'cams': [cam(0, 'mec', 'fs', angle=-60, move='track'),
           cam('P1:colis', 'mec', 'ms', angle=20),
           cam('P2+0.2', 'ticket', 'cu', worldAngle=10, noOcclusion=True, zoom=1.3),
           cam('P3', [DISPLAY], 'cu', worldAngle=0, noOcclusion=True, zoom=1.1),
           cam('P4', 'mec', 'ms', angle=0),
           cam('P5', 'mec', 'cu', angle=0),
           cam('P6', [DISPLAY], 'cu', worldAngle=0, noOcclusion=True, zoom=1.1),
           cam('P6:sorti+0.2', 'mec', 'fs', angle=40),
           cam('P7', 'guichetiere', 'mcu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('P8', "Alors ce con a porté plainte. Pour séquestration.", highlight=['plainte.', 'séquestration.']),
            L('P9', "La poste a été condamnée à lui verser sa putain de retraite.", highlight=['condamnée', 'retraite.'])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('P9:condamnée', clip='sitPoint', expr='angry')]),
             act('mec', [0.9, 0, -1.7], 180, 'stand', 'angry', keys=[k('P9:retraite', clip='celebrate', expr='happy')])],
  'props': [P('boite', 'mailbox', pos=[-1.0, 0, -2.0], ry=20, opts={'color': '#F2C230'}),
            P('barbe', 'beard', scale=2.3, opts={'color': '#E6E2D8'}, on=BEARD),
            P('crane', 'baldCap', opts={'w': 0.235, 'd': 0.215, 'color': '#E8B88E'}, on=CAP)],
  'sfx': [{'at': 'P9:condamnée', 'name': 'gavel', 'vol': 0.6}],
  'cams': [cam(0, ['juge', 'boite'], 'fs', worldAngle=0, elev=6, withProps=True),
           cam('P8:séquestration', 'mec', 'cu', angle=0),
           cam('P9', 'juge', 'mcu', angle=0),
           cam('P9:retraite', 'mec', 'cu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'fin', 'set': 'poste', 'ambience': 'station', 'ambienceVol': 0.6,
  'lines': [L('P10', "En recommandé. À retirer au guichet.", highlight=['recommandé.', 'guichet.']),
            L('P11', "Il a pris un ticket.", pre=0.4, highlight=['ticket.'])],
  'actors': [act('mec', AT_TM, 10, 'showPhone', 'neutral', keys=[k('P11-0.3', face=151, turn=0.2, clip='takeItem', expr='unimpressed'), k('P11:ticket', face=10, turn=0.2, clip='showPhone')])],
  'props': [P('avis', 'notebook', scale=1.8, opts={'text': 'AVIS DE\nPASSAGE\n—\nÀ RETIRER\nAU GUICHET', 'bg': '#2C4A8A'}, on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('P11', visible=False)]),
            P('ticket', 'queueTicket', scale=1.6, visible=False, opts={'num': '8000'}, on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('P11', visible=True)]),
            P('barbe', 'beard', scale=2.3, opts={'color': '#E6E2D8'}, on=BEARD),
            P('crane', 'baldCap', opts={'w': 0.235, 'd': 0.215, 'color': '#E8B88E'}, on=CAP)],
  'sfx': [{'at': 'P11', 'name': 'paper', 'vol': 0.5}],
  'cams': [cam(0, 'avis', 'cu', worldAngle=10, noOcclusion=True, zoom=1.2),
           cam('P11-0.3', 'mec', 'ms', worldAngle=40),
           cam('P11:ticket+0.25', 'ticket', 'cu', worldAngle=10, noOcclusion=True, zoom=1.3)],
  'tail': 1.4,
})

write('ticket', 'Le ticket', scenes, {
  'guichetiere': {'preset': 'madame', 'seed': 44, 'glasses': True},
  'juge': {'preset': 'judge'},
})
