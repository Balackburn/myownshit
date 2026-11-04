#!/usr/bin/env python3
"""LE JOURNAL. Ce mec asks his dog to fetch the newspaper -> the dog fetches the journalist -> it was a kidnapping -> the
journalist sues -> the dog gets six months suspended -> but ce con pays -> he must walk the journalist twice a day ->
and pick up her articles. (Classic formula.)"""
from actu_common import *

scenes = []
scenes.append({
  'id': 'maison', 'set': 'pavillon', 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('J1', "Ce mec a demandé à son chien de rapporter le journal.", highlight=['chien', 'journal.']),
            L('J2', "Le chien a rapporté le journaliste.", highlight=['journaliste.']),
            L('J3', "C'était un enlèvement.", highlight=['enlèvement.'])],
  'actors': [act('mec', [0.97, 0, -2.5], 0, 'stand', 'happy', keys=[k('J1:rapporter', clip='point', expr='happy'), k('J2:journaliste', clip='stand', expr='shocked')]),
             act('chien', [1.7, 0, -2.0], 20, 'sit', 'happy', scale=1.2, keys=[k('J1:journal', to=[8.0, 0, 1.0], clip='run', speed=6.0, then='idle'),
                                                                               k('J2', path=[[5.0, 0, 0.6], [1.9, 0, -1.25]], clip='run', speed=4.5, faceEnd='mec', then='sit')]),
             act('journaliste', [8.6, 0, 1.2], -90, 'idle', 'scared', keys=[k('J2+0.15', path=[[5.6, 0, 0.75], [2.55, 0, -1.0]], clip='walk', speed=4.2, faceEnd='mec', then='scared')])],
  'props': [P('carnet', 'notebook', scale=1.5, opts={'text': 'PRESSE', 'bg': '#2E4563'}, on={'actor': 'journaliste', 'hand': 'R', **HAND_FLAT})],
  'sfx': [{'at': 'J1:journal', 'name': 'whoosh', 'vol': 0.4}, {'at': 'J2', 'name': 'whoosh', 'vol': 0.4}, {'at': 'J3', 'name': 'sting', 'vol': 0.3}],
  'cams': [cam(0, ['mec', 'chien'], 'ms', worldAngle=15),
           POV('J2+0.2', [3.2, 1.6, 2.6], [1.6, 1.0, -1.4], 55),
           cam('J3', 'journaliste', 'cu', angle=-15)],
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('J4', "Le journaliste a porté plainte.", highlight=['plainte.']),
            L('J5', "Le chien a pris six mois avec sursis.", highlight=['six', 'sursis.']),
            L('J6', "Mais putain, c'est ce con qui paie.", highlight=['paie.'])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('J5', clip='sitPoint', expr='angry')]),
             act('chien', [-0.7, 0, -1.8], 180, 'sit', 'smug', scale=1.2, keys=[k('J5-0.3', face=10, turn=0.3)]),
             act('mec', [0.6, 0, -1.7], 180, 'stand', 'neutral', keys=[k('J5.end', clip='showPhone', expr='shocked')]),
             act('journaliste', [2.2, 0, -1.4], -140, 'armsCrossed', 'angry')],
  'props': [P('amende', 'bill', scale=1.6, visible=False, opts={'title': 'AMENDE', 'items': [['Enlèvement', '9 800'], ['Frais de chien', '200'], ['', '']], 'total': '10 000,00 €'},
              on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('J5.end', visible=True)])],
  'sfx': [{'at': 'J5:sursis', 'name': 'gavel', 'vol': 0.6}, {'at': 'J6:paie', 'name': 'cash', 'vol': 0.5}],
  'cams': [cam(0, ['juge', 'chien', 'journaliste'], 'fs', worldAngle=0, elev=6),
           cam('J5', 'chien', 'cu', angle=0),
           cam('J5:sursis', 'juge', 'mcu', angle=0),
           cam('J6+0.15', 'amende', 'cu', worldAngle=180, noOcclusion=True, zoom=1.2)],
  'tail': 0.2,
})
scenes.append({
  'id': 'promenade', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('J7', "Il doit promener le journaliste. Deux fois par jour.", highlight=['promener', 'Deux']),
            L('J8', "Et ramasser ses articles.", highlight=['articles.'])],
  'actors': [act('journaliste', [-4.6, 0, 0.7], 90, 'idle', 'unimpressed', keys=[k(0.05, to=[0.9, 0, 0.7], clip='walk', speed=1.5, then='stand')]),
             act('mec', [-5.85, 0, 0.7], 90, 'idle', 'sad', keys=[k(0.05, to=[-0.35, 0, 0.7], clip='walk', speed=1.5, then='stand'), k('J8:ramasser', clip='kneel', expr='sad'), k('J8:articles', expr='unimpressed')]),
             act('chien', [-3.9, 0, 1.3], 90, 'idle', 'smug', scale=1.2, keys=[k(0.05, to=[1.6, 0, 1.3], clip='walk', speed=1.5, then='sit')])],
  'props': [P('laisse', 'leash', opts={'length': 1.25, 'elev': -0.42}, on={'actor': 'journaliste', 'joint': 'neck', 'offset': [0, 0.05, -0.08]}),
            P('papier', 'newspaper', scale=1.2, visible=False, pos=[0.15, 0.01, 0.75], rot=[-1.5708, 0, 0.4], keys=[k('J8', visible=True)])],
  'sfx': [{'at': 'J8', 'name': 'paper', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'fs', angle=-70, move='track'),
           cam('J7:Deux', ['mec', 'journaliste', 'chien'], 'ms', worldAngle=40),
           cam('J8', ['mec', [0.15, 0.2, 0.75]], 'ms', worldAngle=30),
           cam('J8:articles', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})
write('journal', 'Le journal', scenes, {'chien': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 4}}, 'journaliste': {'preset': 'journaliste', 'seed': 31}, 'juge': {'preset': 'judge'}})
