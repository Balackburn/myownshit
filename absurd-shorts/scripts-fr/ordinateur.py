#!/usr/bin/env python3
"""L'ORDINATEUR (viral-video-writing loop, score_fr.py 100/100). Hook with a number (three hits) -> the computer hits back, he
crosses the open space -> complaint -> self-defence with the webcam video, the judge watches it twice -> fired, the computer gets
his job and a raise -> low point: he is its intern -> loop: he "lags", the computer hits him (the opening shot reversed)."""
from actu_common import *

DESK = [0.4, 0, -2.0]
MON = [DESK[0], 0.76, DESK[2] - 0.15]
SEAT = [DESK[0], 0.16, DESK[2] + 0.62]
WEBCAM = lambda at: POV(at, [MON[0], 1.62, MON[2] - 0.25], [SEAT[0], 1.5, SEAT[2]], 64)              # him seated (head ~1.66), fists in the bottom of frame
WEBCAM_UP = lambda at: POV(at, [MON[0], 1.9, MON[2] - 0.25], [DESK[0] + 0.05, 1.8, DESK[2] + 0.8], 55)  # him standing beside the desk
SIDE = lambda at: POV(at, [DESK[0] + 0.6, 1.7, 7.6], [DESK[0], 1.0, -1.2], 55)     # he flies at the camera
def monitor(angry):
    return P('pc', 'pcMonitor', pos=MON, opts={'angryAt': angry}, keys=[k(a, to=[MON[0], MON[1], MON[2] + 0.42], dur=0.09, ease='out') for a in angry] +
                                                                 [k(f'{a}+0.12', to=MON, dur=0.3) for a in angry])
scenes = []
scenes.append({
  'id': 'bureau', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('OR1', "Ce mec a tapé trois fois sur son ordinateur pour qu'il marche plus vite.", highlight=['trois', 'ordinateur']),
            L('OR2', "L'ordinateur a tapé aussi. Ce mec a traversé l'open space.", highlight=['aussi.', 'traversé'])],
  'actors': [act('mec', SEAT, 180, 'sit', 'angry', keys=[k('OR1:tapé', clip='sitPunch'), k('OR1:fois', clip='sitPunch'), k('OR1:marche', clip='sitPunch'),
                                                        k('OR2:tapé+0.05', to=[DESK[0] + 0.3, 0, 4.2], glide=True, dur=0.75, arc=0.7, clip='hitFly', then='koFloor', face='keep', expr='shocked')])],
  'props': [P('bureau', 'desk', pos=DESK, opts={'w': 1.6}), monitor(['OR2:tapé']), P('chaise', 'officeChair', pos=[SEAT[0], 0, SEAT[2] + 0.05], ry=180)],
  'sfx': [{'at': 'OR1:tapé', 'name': 'thud', 'vol': 0.5}, {'at': 'OR1:fois', 'name': 'thud', 'vol': 0.5}, {'at': 'OR1:marche', 'name': 'thud', 'vol': 0.5},
          {'at': 'OR2:tapé', 'name': 'punch', 'vol': 0.8}, {'at': 'OR2:Ce', 'name': 'whoosh', 'vol': 0.5}, {'at': 'OR2:space', 'name': 'thud', 'vol': 0.7}],
  'cams': [WEBCAM(0), POV('OR1:tapé', [3.2, 1.5, -1.6], [0.4, 1.25, -1.75], 45), WEBCAM('OR1:pour'), SIDE('OR2:tapé-0.2')],   # profile for the three punches
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('OR3', "Alors ce con a porté plainte pour coups et blessures.", highlight=['plainte', 'blessures.']),
            L('OR4', "L'ordinateur a plaidé la légitime défense, avec la vidéo de la webcam.", highlight=['légitime', 'webcam.']),
            L('OR5', "Le juge a regardé la vidéo deux fois. Il a donné raison à l'ordinateur.", highlight=['deux', "l'ordinateur."])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('OR5:raison', clip='sitPoint', expr='neutral')]),
             act('mec', [-0.9, 0, -1.7], 180, 'stand', 'sad'),
             act('avocat', [1.6, 0, -2.2], -150, 'stand', 'smug', keys=[k('OR4', face=-100, turn=0.25, clip='point')])],
  'props': [P('pc', 'pcMonitor', pos=[2.5, 1.11, -3.35], ry=-20), P('bosses', 'faceLumps', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.3, 0.1]}),
            P('ecran', 'tv', pos=[-2.6, 0, -2.9], ry=40, opts={'text': '● WEBCAM', 'on': True})],
  'sfx': [{'at': 'OR5:deux', 'name': 'click', 'vol': 0.4}, {'at': 'OR5:raison', 'name': 'gavel', 'vol': 0.6}],
  'cams': [cam(0, ['juge', 'mec'], 'fs', worldAngle=0, elev=6),
           cam('OR3:plainte', 'mec', 'cu', worldAngle=180, noOcclusion=True),
           cam('OR4', ['avocat', 'pc'], 'ms', worldAngle=-20, withProps=True),
           cam('OR5', 'juge', 'mcu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'bureau2', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('OR6', "Ce mec a été viré. L'ordinateur a pris son poste.", highlight=['viré.', 'poste.']),
            L('OR7', "Au bout de trois semaines, il a été augmenté.", highlight=['trois', 'augmenté.']),
            L('OR8', "Maintenant, ce mec est le stagiaire de l'ordinateur.", highlight=['stagiaire']),
            L('OR9', "Ce matin, ce mec ramait.", highlight=['ramait.']),
            L('OR10', "Putain, l'ordinateur lui a tapé dessus.", highlight=['dessus.'])],
  'actors': [act('mec', [DESK[0] + 0.9, 0, DESK[2] + 0.9], -90, 'carryBox', 'sad', keys=[
                 k('OR6', to=[4.5, 0, 0.6], clip='walk', speed=1.4, faceEnd=90, then='walk'),
                 k('OR8', to=[DESK[0] + 0.05, 0, DESK[2] + 0.8], glide=True, dur=0.05, face=180, clip='holdOut', then='holdOut', expr='unimpressed'),
                 k('OR9', clip='idle', expr='sleepy', speed=0.25),
                 k('OR10:tapé+0.05', to=[DESK[0] + 0.3, 0, 4.2], glide=True, dur=0.75, arc=0.7, clip='hitFly', then='koFloor', face='keep', expr='shocked')]),
             act('patron', [-2.5, 0, -0.5], 70, 'idle', 'happy', visible=False, keys=[k('OR7', visible=True), k('OR7', to=[DESK[0] - 0.9, 0, DESK[2] + 0.4], clip='walk', speed=2.4, faceEnd=20, then='giveItem'),
                                                                                    k('OR8', visible=False)])],
  'props': [P('bureau', 'desk', pos=DESK, opts={'w': 1.6}), monitor(['OR10:tapé']), P('chaise', 'officeChair', pos=[SEAT[0], 0, SEAT[2] + 0.05], ry=180),
            P('carton', 'cardboardBox', scale=0.5, opts={'text': 'AFFAIRES'}, on={'actor': 'mec', 'hand': 'R', 'offset': [0.2, -0.1, 0.1]}, keys=[k('OR8', visible=False)]),
            P('plaque', 'signBoard', pos=[DESK[0] + 0.45, 0, DESK[2] + 0.3], opts={'text': 'DIRECTEUR', 'w': 0.5, 'h': 0.12, 'height': 0.76, 'posts': False, 'bg': '#2A2A2E', 'fg': '#F2C230', 'frame': '#C9A06A'}),
            P('magot', 'moneySack', visible=False, pos=[DESK[0] - 0.55, 0.76, DESK[2]], keys=[k('OR7:augmenté', visible=True)]),
            P('cafe', 'mug', visible=False, on={'actor': 'mec', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]}, keys=[k('OR8', visible=True), k('OR10:tapé', visible=False)]),
            P('badge', 'stampMark', scale=0.45, visible=False, opts={'text': 'STAGIAIRE', 'color': '#2C4A8A', 'w': 0.36, 'h': 0.11}, on={'actor': 'mec', 'joint': 'torso', 'offset': [0.08, 0.32, 0.17]},
              keys=[k('OR8', visible=True)])],
  'sfx': [{'at': 'OR6:viré', 'name': 'sting', 'vol': 0.35}, {'at': 'OR7:augmenté', 'name': 'cash', 'vol': 0.5}, {'at': 'OR10:tapé', 'name': 'punch', 'vol': 0.8},
          {'at': 'OR10:dessus', 'name': 'thud', 'vol': 0.7}],
  'cams': [cam(0, 'mec', 'ms', angle=-20),
           cam('OR7', ['patron', 'pc'], 'ms', worldAngle=20, withProps=True),
           WEBCAM_UP('OR8'),
           SIDE('OR10:tapé-0.2')],
  'tail': 1.4,
})
write('ordinateur', "L'ordinateur", scenes, {'juge': {'preset': 'judge'}, 'avocat': {'preset': 'avocat'}, 'patron': {'preset': 'lemec_beige', 'seed': 33}})
