#!/usr/bin/env python3
"""LE MOT DE PASSE (viral-video-writing loop, score_fr.py 100/100). Hook (change a password) -> four seconds later he forgot it
-> mails, bank, car, front door -> the villain: the door's voice ("plus que deux essais") -> the police ask him for his password
-> low point: three months on the doormat -> he remembers -> the system asks him to change it -> loop: already forgotten."""
from actu_common import *

LAP = [2.5, 0.77, -2.62]                          # chambre desk
SEAT = [2.5, 0.12, -1.95]
WEBCAM = lambda at: POV(at, [LAP[0], 1.5, LAP[2] - 0.25], [SEAT[0], 1.48, SEAT[2]], 58)
SCREEN = lambda at: POV(at, [LAP[0] + 0.25, 1.32, LAP[2] + 0.75], [LAP[0], 0.92, LAP[2]], 34)
DOOR = [0.975, 0, -4.1]
KEYPAD = [1.65, 1.25, -4.06]
KEY_POV = lambda at: POV(at, [KEYPAD[0], KEYPAD[1] + 0.02, KEYPAD[2] + 0.55], KEYPAD, 30)
BEARD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.02, 0.1]}
def lap(i, text, vis=False, keys=()): return P(f'lap{i}', 'laptop', pos=LAP, visible=vis, opts={'text': text}, keys=list(keys))
def pad(i, text, vis=False, keys=()): return P(f'pad{i}', 'doorKeypad', pos=KEYPAD, visible=vis, opts={'text': text}, keys=list(keys))
scenes = []
scenes.append({
  'id': 'chambre', 'set': 'chambre', 'setOpts': {'poster': 'SÉCURITÉ', 'posterBg': '#2C4A8A', 'posterFg': '#F2C230'}, 'ambience': None,
  'lines': [L('MP1', "Ce mec a changé son mot de passe pour être plus en sécurité.", highlight=['mot', 'passe', 'sécurité.']),
            L('MP2', "Quatre secondes plus tard, il l'avait oublié.", highlight=['Quatre', 'oublié.']),
            L('MP3', "Il ne pouvait plus ouvrir ses mails. Ni son compte en banque.", highlight=['mails.', 'banque.'])],
  'actors': [act('mec', SEAT, 180, 'sitWrite', 'smug', keys=[k('MP2:oublié', clip='sit', expr='shocked'), k('MP3', expr='worried')])],
  'props': [lap(0, 'NOUVEAU MOT\nDE PASSE : ●●●●●', vis=True, keys=[k('MP2', visible=False)]),
            lap(1, 'MOT DE PASSE\nINCORRECT', keys=[k('MP2', visible=True), k('MP3:mails', visible=False)]),
            lap(2, 'MAILS\nACCÈS REFUSÉ', keys=[k('MP3:mails', visible=True), k('MP3:banque', visible=False)]),
            lap(3, 'BANQUE\nACCÈS REFUSÉ', keys=[k('MP3:banque', visible=True)])],
  'sfx': [{'at': 'MP1:changé', 'name': 'click', 'vol': 0.4}, {'at': 'MP2:oublié', 'name': 'beep', 'vol': 0.5}, {'at': 'MP3:mails', 'name': 'beep', 'vol': 0.5}, {'at': 'MP3:banque', 'name': 'beep', 'vol': 0.5}],
  'cams': [WEBCAM(0), SCREEN('MP2:oublié-0.1'), WEBCAM('MP2:oublié+0.6'), SCREEN('MP3:mails-0.1')],
  'tail': 0.2,
})
CAR = [3.6, 0, -1.6]
scenes.append({
  'id': 'dehors', 'set': 'pavillon', 'ambience': 'park', 'ambienceVol': 0.4,
  'lines': [L('MP4', "Ni sa voiture. Ni sa porte d'entrée.", highlight=['voiture.', "d'entrée."]),
            L('MP5', "Mot de passe incorrect. Plus que deux essais.", 'porte')],
  'actors': [act('mec', [CAR[0] + 0.3, 0, CAR[2] + 1.15], 180, 'pokeFinger', 'angry', keys=[
                 k('MP4:porte', to=[KEYPAD[0] - 0.15, 0, KEYPAD[2] + 0.65], glide=True, dur=0.05, face=180, clip='pokeFinger', then='pokeFinger', expr='angry'),
                 k('MP5', clip='stand', expr='scared')])],
  'props': [P('voiture', 'car', pos=CAR, opts={'color': '#2C4A8A'}),
            P('padCar', 'doorKeypad', pos=[CAR[0] + 0.3, 1.25, CAR[2] + 0.93], opts={'text': 'MOT DE\nPASSE ?'}),
            pad(0, 'MOT DE\nPASSE ?', vis=True, keys=[k('MP5', visible=False)]), pad(1, 'INCORRECT\n2 ESSAIS', keys=[k('MP5', visible=True)])],
  'sfx': [{'at': 'MP4:voiture', 'name': 'beep', 'vol': 0.5}, {'at': 'MP4:porte', 'name': 'beep', 'vol': 0.5}, {'at': 'MP5', 'name': 'beep', 'vol': 0.6}],
  'cams': [cam(0, 'mec', 'ms', worldAngle=-90),
           cam('MP4:porte', 'mec', 'ms', worldAngle=-90),
           KEY_POV('MP5')],
  'tail': 0.2,
})
DESKP = [-2.7, 0, -2.1]
scenes.append({
  'id': 'police', 'set': 'policeStation', 'ambience': 'station',
  'lines': [L('MP6', "Alors ce con a appelé la police pour prouver qui il était.", highlight=['police', 'prouver']),
            L('MP7', "La police lui a demandé son mot de passe.", highlight=['mot', 'passe.'])],
  'actors': [act('commissaire', [DESKP[0], 0.12, DESKP[2] - 0.62], 0, 'sitWrite', 'neutral', keys=[k('MP7', clip='sitPoint', expr='suspicious')]),
             act('mec', [DESKP[0] + 0.9, 0, DESKP[2] + 0.9], -140, 'stand', 'worried', keys=[k('MP6:prouver', clip='pointSelf')])],
  'props': [P('lapP', 'laptop', pos=[DESKP[0], 0.76, DESKP[2] - 0.2], ry=180, opts={'text': 'MOT DE PASSE ?'})],
  'sfx': [{'at': 'MP7:passe', 'name': 'sting', 'vol': 0.3}],
  'cams': [cam(0, ['mec', 'commissaire'], 'ms', worldAngle=-50),
           cam('MP7', 'commissaire', 'cu', angle=0)],
  'tail': 0.2,
})
MAT = [DOOR[0], 0.012, DOOR[2] + 0.75]
scenes.append({
  'id': 'paillasson', 'set': 'pavillon', 'lighting': 'night', 'ambience': 'night', 'ambienceVol': 0.4,
  'lines': [L('MP8', "Depuis trois mois, il dort sur son paillasson.", highlight=['trois', 'paillasson.']),
            L('MP9', "Hier, il s'en est enfin souvenu.", highlight=['souvenu.']),
            L('MP10', "Putain, le système lui a demandé de le changer.", highlight=['changer.']),
            L('MP11', "Il l'a déjà oublié.", highlight=['oublié.'])],
  'actors': [act('mec', [MAT[0], 0.14, MAT[2]], 90, 'sleepSide', 'sleepy', keys=[
                 k('MP9', to=[KEYPAD[0] - 0.15, 0, KEYPAD[2] + 0.65], glide=True, dur=0.05, face=180, clip='pokeFinger', then='pokeFinger', expr='grin'),
                 k('MP10', clip='stand', expr='shocked'), k('MP11', face=10, turn=0.3, clip='stareCamera', expr='unimpressed')])],
  'props': [P('tapis', 'carpet', pos=MAT, opts={'w': 1.0, 'd': 0.6, 'color': '#8A5A3A', 'inner': '#B08A64'}), P('lampadaire', 'streetLamp', pos=[2.6, 0, -3.3], ry=-90, opts={'on': True, 'light': 6}),
            P('barbe', 'beard', scale=1.1, opts={'color': '#2A2420'}, on=BEARD),
            pad(0, 'MOT DE\nPASSE ?', vis=True, keys=[k('MP10', visible=False)]), pad(1, 'NOUVEAU\nMOT DE PASSE ?', keys=[k('MP10', visible=True)])],
  'sfx': [{'at': 0, 'name': 'crickets', 'vol': 0.35}, {'at': 'MP9:souvenu', 'name': 'ding', 'vol': 0.5}, {'at': 'MP10', 'name': 'beep', 'vol': 0.6}],
  'cams': [POV(0, [MAT[0] + 1.6, 1.4, MAT[2] + 1.8], [MAT[0], 0.3, MAT[2]], 48),
           cam('MP9:souvenu', 'mec', 'ms', worldAngle=-90),
           KEY_POV('MP10:système'),
           cam('MP11', 'mec', 'cu', angle=0, move='push', amount=0.04)],
  'tail': 1.4,
})
write('motdepasse', 'Le mot de passe', scenes, {})
