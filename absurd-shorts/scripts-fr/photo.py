#!/usr/bin/env python3
"""LA PHOTO D'IDENTITÉ. Written with the viral-video-writing loop (5 hooks, 3 drafts, score_fr.py 100/100):
hook with a number (38 photos) -> the rule-villain at 5 s (the prefecture refuses: he smiles) -> the decision (never smiles
again) -> low point (his wife divorces him) -> the turn (promoted: he looks serious) -> the passport, the airport, one smile
-> arrested for identity theft (he no longer looks like his photo) -> callback payoff: the mugshot is the only photo where he
smiles. The last flash answers the photo-booth flashes of the first shot (loop)."""
from actu_common import *

BOOTH = [-4.4, 0, -2.0]                       # photo booth in the prefecture hall, opening towards +z
WIN = [0, 0, -1.62]                           # in front of window 2
CLERK = [0, 0, -2.85]
COUNTER_Y = 1.115
PHOTO_ON_DESK = [0, COUNTER_Y, -2.15]
def flashes(times): return [{'type': 'flash', 'at': t, 'dur': 0.16} for t in times]
scenes = []
FL = ['H1:photo', 'H1:fois', 'H1:passeport']
scenes.append({
  'id': 'photomaton', 'set': 'poste', 'setOpts': {'title': 'PRÉFECTURE'}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('H1', "Ce mec a refait sa photo d'identité trente-huit fois pour avoir son passeport.", highlight=['trente-huit', 'passeport.']),
            L('H2', "À chaque fois, la préfecture la refusait. Il souriait.", highlight=['préfecture', 'souriait.']),
            L('H3', "Alors ce con a arrêté de sourire. Pour toujours.", highlight=['toujours.'])],
  'actors': [act('mec', [BOOTH[0], 0.12, BOOTH[2] - 0.1], 0, 'sit', 'grin', keys=[
                 k('H2', to=WIN, glide=True, dur=0.05, face=180, clip='stand', then='stand', expr='grin'),
                 k('H3:sourire', expr='unimpressed')]),
             act('agent', CLERK, 0, 'idle', 'unimpressed', keys=[k('H2:refusait-0.2', clip='slamTable', expr='angry'), k('H2:souriait', clip='shakeHead')])],
  'props': [P('cabine', 'photoBooth', pos=BOOTH, opts={'flashAt': FL}),
            P('photoId', 'idPhoto', scale=3.0, pos=PHOTO_ON_DESK, rot=[-1.5708, 0, 0], opts={'smile': True}),
            P('refuse', 'stampMark', visible=False, pos=[PHOTO_ON_DESK[0], COUNTER_Y + 0.006, PHOTO_ON_DESK[2] + 0.02], rot=[-1.5708, 0, 0.3], opts={'text': 'REFUSÉ', 'w': 0.26, 'h': 0.09},
              keys=[k('H2:refusait', visible=True)]),
            P('pile', 'paperPile', scale=0.35, pos=[0.42, COUNTER_Y, -2.3], opts={'count': 38, 'seed': 4}),
            P('encreur', 'rubberStamp', on={'actor': 'agent', 'hand': 'R'})],
  'fx': flashes(FL),
  'sfx': [*[{'at': t, 'name': 'shutter', 'vol': 0.6} for t in FL], {'at': 'H2:refusait', 'name': 'thud', 'vol': 0.7}, {'at': 'H3:toujours', 'name': 'sting', 'vol': 0.3}],
  'cams': [cam(0, 'mec', 'ms', angle=0, noOcclusion=True),
           cam('H1:trente', 'mec', 'cu', angle=0, noOcclusion=True),
           cam('H2', 'agent', 'ms', angle=0),
           POV('H2:refusait-0.3', [0, 1.62, -1.9], PHOTO_ON_DESK, 34),
           cam('H2:souriait', 'mec', 'cu', angle=0),
           cam('H3', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 0.2,
})
ALTAR_Y, ALTAR_Z = 0.22, -4.3
scenes.append({
  'id': 'mariage', 'set': 'church', 'ambience': None,
  'lines': [L('H4', "À son mariage, il n'a pas souri. Sa femme a demandé le divorce.", highlight=['mariage,', 'divorce.'])],
  'actors': [act('mec', [-0.45, ALTAR_Y, ALTAR_Z], 90, 'stand', 'unimpressed'),
             act('mariee', [0.45, ALTAR_Y, ALTAR_Z], -90, 'stand', 'happy', keys=[
                 k('H4:femme', expr='angry'), k('H4:divorce', to=[1.4, 0, 2.5], clip='walk', speed=1.6, faceEnd=10, then='walk', expr='angry')])],
  'props': [],
  'fx': flashes(['H4:souri']),
  'sfx': [{'at': 'H4', 'name': 'choir', 'vol': 0.35}, {'at': 'H4:souri', 'name': 'shutter', 'vol': 0.6}, {'at': 'H4:divorce', 'name': 'sting', 'vol': 0.35}],
  'cams': [cam(0, ['mec', 'mariee'], 'fs', worldAngle=0),
           cam('H4:Sa', 'mariee', 'cu', angle=0),
           cam('H4:divorce', 'mec', 'cu', angle=-60)],
  'tail': 0.2,
})
scenes.append({
  'id': 'bureau', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('H5', "Au boulot, on l'a nommé directeur. Il avait l'air sérieux.", highlight=['directeur.', 'sérieux.'])],
  'actors': [act('mec', [0, 0.16, -2.75], 0, 'sit', 'unimpressed'),
             act('collegue1', [-1.4, 0, -1.5], 50, 'stand', 'happy', keys=[k('H5:directeur', clip='celebrate')]),
             act('collegue2', [1.4, 0, -1.5], -50, 'stand', 'happy', keys=[k('H5:directeur+0.15', clip='celebrate')])],
  'props': [P('bureau', 'desk', pos=[0, 0, -2.15], opts={'w': 1.6}),
            P('fauteuil', 'officeChair', pos=[0, 0, -2.85], opts={'color': '#2A2A2E'}),
            P('plaque', 'signBoard', pos=[0, 0, -1.82], opts={'text': 'DIRECTEUR', 'w': 0.62, 'h': 0.14, 'height': 0.76, 'posts': False, 'bg': '#2A2A2E', 'fg': '#F2C230', 'frame': '#C9A06A'})],
  'sfx': [{'at': 'H5:directeur', 'name': 'tada', 'vol': 0.4}],
  'cams': [cam(0, ['mec', 'collegue1', 'collegue2'], 'ms', worldAngle=0),
           cam('H5:sérieux-0.4', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 0.2,
})
MB = [2.8, 0, 2.5]                             # the pavillon's mailbox
scenes.append({
  'id': 'boite', 'set': 'pavillon', 'ambience': 'park', 'ambienceVol': 0.45,
  'lines': [L('H6', "Trois ans plus tard, son passeport est enfin arrivé.", highlight=['Trois', 'passeport'])],
  'actors': [act('mec', [2.35, 0, 3.15], 125, 'stand', 'unimpressed', keys=[k('H6:passeport', face=10, turn=0.25, clip='showPhone')])],
  'props': [P('passeport', 'notebook', scale=1.7, visible=False, opts={'text': 'PASSEPORT\n—\n2026', 'bg': '#6E1A2A'}, on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('H6:passeport', visible=True)])],
  'sfx': [{'at': 'H6:passeport', 'name': 'paper', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'ms', angle=-20),
           cam('H6:arrivé', 'passeport', 'mcu', worldAngle=10, noOcclusion=True)],
  'tail': 0.2,
})
CTR = [-3.4, 0, -3.2]                          # airport check-in / border counter
scenes.append({
  'id': 'aeroport', 'set': 'airport', 'ambience': 'station', 'ambienceVol': 0.5,
  'lines': [L('H7', "À l'aéroport, il était tellement content qu'il a souri.", highlight=['souri.']),
            L('H8', "La police l'a arrêté pour usurpation d'identité. Il ne ressemblait plus à sa photo.", highlight=['usurpation', 'photo.'])],
  'actors': [act('mec', [CTR[0], 0, -1.75], 180, 'stand', 'unimpressed', keys=[
                 k('H7:content', expr='grin'), k('H8:arrêté', face=20, turn=0.3, clip='cuffedFront', expr='grin')]),
             act('flic1', [CTR[0], 0, -3.95], 0, 'stand', 'neutral', keys=[k('H8', clip='point', expr='suspicious'), k('H8:ressemblait', clip='showPhone', expr='angry')]),
             act('flic2', [CTR[0] + 2.4, 0, -1.4], -110, 'idle', 'angry', keys=[k('H8-0.3', to=[CTR[0] + 0.75, 0, -1.4], clip='walk', speed=3.0, faceEnd='mec', then='cuffOther')])],
  'props': [P('valise', 'briefcase', scale=1.3, on={'actor': 'mec', 'hand': 'L'}, keys=[k('H8:arrêté', visible=False)]),
            P('menottes', 'handcuffs', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('H8:arrêté', visible=True)]),
            P('photoPass', 'idPhoto', scale=3.2, visible=False, opts={'smile': False}, on={'actor': 'flic1', 'hand': 'R', **HAND_FLAT}, keys=[k('H8:ressemblait', visible=True)])],
  'sfx': [{'at': 'H7:souri', 'name': 'ding', 'vol': 0.5}, {'at': 'H8:arrêté', 'name': 'cuff', 'vol': 0.6}, {'at': 'H8:police', 'name': 'siren', 'vol': 0.3}],
  'cams': [cam(0, ['mec', 'flic1'], 'ms', worldAngle=-70),
           cam('H7:souri-0.3', 'mec', 'cu', angle=-40, move='push', amount=0.04),
           cam('H8:arrêté', ['mec', 'flic2'], 'ms', worldAngle=-10),
           cam('H8:ressemblait', 'photoPass', 'cu', worldAngle=0, noOcclusion=True),
           cam('H8:photo', 'mec', 'cu', angle=-45)],
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('H9', "Putain, trois ans ferme.", highlight=['trois', 'ferme.'])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('H9:trois', clip='sitPoint', expr='angry')]),
             act('mec', [0.9, 0, -1.7], 180, 'cuffedFront', 'sad')],
  'props': [P('menottes', 'handcuffs', on={'actor': 'mec', 'hand': 'R'})],
  'sfx': [{'at': 'H9:trois', 'name': 'gavel', 'vol': 0.6}, {'at': 'H9:ferme', 'name': 'gavel', 'vol': 0.6}],
  'cams': [cam(0, 'juge', 'mcu', angle=0)],
  'tail': 0.15,
})
scenes.append({
  'id': 'casier', 'set': 'policeStation', 'ambience': 'station', 'ambienceVol': 0.4,
  'lines': [L('H10', "Sur la photo du casier, il sourit.", highlight=['casier,', 'sourit.'])],
  'actors': [act('mec', [-0.4, 0, -2.85], 0, 'showPhone', 'unimpressed', keys=[k('H10:sourit-0.15', expr='grin')])],
  'props': [P('toise', 'mugshotBoard', pos=[-0.4, 0, -3.52]),
            P('ardoise', 'placard', scale=1.4, opts={'text': 'POLICE\nN° 38'}, on={'actor': 'mec', 'hand': 'R', **HAND_FLAT})],
  'fx': flashes(['H10:sourit']),
  'sfx': [{'at': 'H10:sourit', 'name': 'shutter', 'vol': 0.8}],
  'cams': [cam(0, 'mec', 'ms', angle=0),
           cam('H10:sourit-0.2', 'mec', 'cu', angle=0, move='push', amount=0.04)],
  'tail': 1.4,
})

write('photo', "La photo d'identité", scenes, {'agent': {'preset': 'madame', 'seed': 44, 'glasses': True},
                                               'mariee': {'preset': 'femme', 'suit': '#F7F3EA', 'seed': 12},
                                               'collegue1': {'preset': 'lemec_beige', 'seed': 33}, 'collegue2': {'preset': 'madame', 'seed': 9},
                                               'juge': {'preset': 'judge'}})
