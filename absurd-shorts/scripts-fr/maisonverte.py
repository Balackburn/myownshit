#!/usr/bin/env python3
"""LA MAISON VERTE (viral-video-writing loop, score_fr.py 95/100). Hook (paint the house green to blend in) -> it blends: nobody
finds it in two days -> the postman searches for three weeks, his wife leaves (can't find the door) -> the firemen take it for a
bush and trim it: it is shaped like a rabbit -> he repaints it red -> the firemen think it's a fire -> loop: hosed down, green again."""
from actu_common import *

H = [0, 0, -6.6]
HOUSE = {'w': 6.5, 'd': 5, 'h': 2.9}
GREEN = {**HOUSE, 'color': '#5E9A4A', 'roof': '#4E8A3E', 'door': '#4E8A3E', 'frame': '#4E8A3E'}
RABBIT_S = 1.15
FIRE = {'preset': 'lemec_charcoal', 'outfit': 'worker', 'hat': 'firehelmet', 'suit': '#2C3A5A'}
WIDE = lambda at, fov=56: POV(at, [1.2, 2.2, 8.5], [0, 2.4, -5.5], fov)
def jet(id_, frm, vis_at, end_at): return P(id_, 'beerStream', visible=False, pos=frm, rot=[1.45, 0, 0], opts={'length': 3.2, 'r': 0.03, 'flare': 2.5, 'color': '#BFE3EE'},
                                            keys=[k(vis_at, visible=True), k(end_at, visible=False)])
scenes = []
scenes.append({
  'id': 'maison', 'set': 'pavillon', 'setOpts': {'house': False}, 'ambience': 'park', 'ambienceVol': 0.45,
  'daynight': {'from': 'MV3', 'period': 0.45},
  'lines': [L('MV1', "Ce mec a peint sa maison en vert pour qu'elle se fonde dans la nature.", highlight=['vert', 'nature.']),
            L('MV2', "Elle s'est fondue. En deux jours, plus personne ne l'a retrouvée.", highlight=['fondue.', 'deux']),
            L('MV3', "Le facteur a cherché pendant trois semaines.", highlight=['facteur', 'trois']),
            L('MV4', "Sa femme est partie. Elle ne trouvait plus la porte.", highlight=['partie.', 'porte.'])],
  'actors': [act('mec', [-1.4, 0, -3.62], 180, 'drawOn', 'happy', keys=[k('MV1:vert', face=80, turn=0.3, clip='stand', expr='grin'), k('MV2', visible=False)]),   # proud, turns to us as the wall goes green
             act('facteur', [-3.0, 0, 3.4], 90, 'stand', 'suspicious', visible=False, keys=[k('MV3', visible=True), k('MV3', to=[3.2, 0, 3.4], glide=True, dur=2.34, clip='walk', then='lookAround', face='keep')]),
             act('femme', [1.6, 0, -3.5], 180, 'stand', 'angry', visible=False, keys=[k('MV4', visible=True), k('MV4:partie', face=90, turn=0.3, clip='walk'),
                                                                                      k('MV4:partie+0.1', to=[5.5, 0, -1.0], clip='walk', speed=1.6, then='walk')])],
  'props': [P('maisonB', 'house', pos=H, opts={**HOUSE, 'color': '#EDE3CF', 'roof': '#7A3A2A', 'door': '#2F5E58', 'frame': '#2F5E58'}, keys=[k('MV1:vert', visible=False)]),
            P('maisonV', 'house', visible=False, pos=H, opts=GREEN, keys=[k('MV1:vert', visible=True)]),
            P('pinceau', 'marker', scale=1.6, on={'actor': 'mec', 'hand': 'R'}),
            P('lettre', 'notebook', scale=0.9, opts={'text': 'COURRIER', 'bg': '#F2C230'}, on={'actor': 'facteur', 'hand': 'R', **HAND_FLAT}),
            P('valise', 'briefcase', scale=1.4, on={'actor': 'femme', 'hand': 'L'})],
  'sfx': [{'at': 'MV1:vert', 'name': 'splat', 'vol': 0.5}, {'at': 'MV3', 'name': 'step', 'vol': 0.3}, {'at': 'MV4:porte', 'name': 'thud', 'vol': 0.4}],
  'cams': [POV(0, [1.5, 1.65, -3.2], [-1.4, 1.5, -3.85], 42),   # profile: he faces the wall, the brush hand towards us
           {**WIDE('MV2', 62), 'grade': 'saturate(0.8)'},
           {'at': 'MV3', 'from': [-2.4, 1.6, 8.0], 'to': [3.8, 1.6, 8.0], 'lookAt': [-3.0, 1.3, 3.4], 'lookAt2': [3.2, 1.3, 3.4], 'lens': 42, 'ease': 'linear'},  # tracking from the street
           cam('MV4', 'femme', 'ms', worldAngle=30)],
  'tail': 0.2,
})
scenes.append({
  'id': 'pompiers', 'set': 'pavillon', 'setOpts': {'house': False}, 'ambience': 'park', 'ambienceVol': 0.45,
  'lines': [L('MV5', "Alors ce con a appelé les pompiers.", highlight=['pompiers.']),
            L('MV6', "Ils ont cru que c'était un buisson. Ils l'ont taillée.", highlight=['buisson.', 'taillée.']),
            L('MV7', "Depuis, sa maison a la forme d'un lapin.", highlight=['lapin.'])],
  'actors': [act('mec', [2.6, 0, 0.3], -20, 'phoneCall', 'angry', keys=[k('MV7', clip='stand', expr='shocked')]),
             act('pompier1', [-2.2, 0, -3.3], 180, 'holdOut', 'neutral', keys=[k('MV7', face=20, turn=0.3, clip='celebrate', expr='grin')]),
             act('pompier2', [1.0, 0, -3.3], 180, 'holdOut', 'neutral', keys=[k('MV7', face=-20, turn=0.3, clip='celebrate', expr='grin')])],
  'props': [P('maisonV', 'house', pos=H, opts=GREEN, keys=[k('MV6:taillée', visible=False)]),
            P('lapin', 'topiaryRabbit', scale=RABBIT_S, visible=False, pos=[H[0], 0, H[2] + 0.4], keys=[k('MV6:taillée', visible=True)]),
            P('tel', 'phone911', on={'actor': 'mec', 'hand': 'R'}, keys=[k('MV7', visible=False)]),
            P('scie1', 'chainsaw', on={'actor': 'pompier1', 'hand': 'R'}, opts={'runAt': 'MV6', 'stopAt': 'MV7'}),
            P('scie2', 'chainsaw', on={'actor': 'pompier2', 'hand': 'R'}, opts={'runAt': 'MV6', 'stopAt': 'MV7'}),
            P('feuilles', 'dustPuff', scale=4.0, visible=False, pos=[0, 1.5, -4.2], opts={'color': '#5E9A4A', 'once': True, 'period': 1.2, 'startAt': 'MV6:taillée-0.3'}, keys=[k('MV6:taillée-0.3', visible=True)])],
  'sfx': [{'at': 'MV5:pompiers', 'name': 'siren', 'vol': 0.35}, {'at': 'MV6', 'name': 'chainsaw', 'vol': 0.5}, {'at': 'MV6:taillée', 'name': 'poof', 'vol': 0.6}, {'at': 'MV7:lapin', 'name': 'tada', 'vol': 0.4}],
  'cams': [cam(0, 'mec', 'ms', angle=0),
           cam('MV6', ['pompier1', 'pompier2'], 'ms', worldAngle=-90),
           WIDE('MV6:taillée', 60)],
  'tail': 0.2,
})
scenes.append({
  'id': 'rouge', 'set': 'pavillon', 'setOpts': {'house': False}, 'ambience': 'park', 'ambienceVol': 0.45,
  'lines': [L('MV8', "Hier, il l'a repeinte en rouge pour qu'on la voie de loin.", highlight=['rouge']),
            L('MV9', "Putain, les pompiers ont cru à un incendie.", highlight=['incendie.']),
            L('MV10', "Ils l'ont arrosée. Elle est redevenue verte.", highlight=['arrosée.', 'verte.'])],
  'actors': [act('mec', [2.4, 0, -1.6], 200, 'drawOn', 'grin', keys=[k('MV9', face=20, turn=0.3, clip='stand', expr='shocked'), k('MV10:redevenue', clip='stareCamera', expr='unimpressed')]),
             act('pompier1', [-2.6, 0, 1.4], 180, 'holdOut', 'angry', visible=False, keys=[k('MV9:pompiers', visible=True)]),
             act('pompier2', [0.6, 0, 1.6], 180, 'holdOut', 'angry', visible=False, keys=[k('MV9:pompiers', visible=True)])],
  'props': [P('lapinR', 'topiaryRabbit', scale=RABBIT_S, pos=[H[0], 0, H[2] + 0.4], opts={'color': '#C23A2E', 'color2': '#D9534A'}, keys=[k('MV10:redevenue', visible=False)]),
            P('lapinV', 'topiaryRabbit', scale=RABBIT_S, visible=False, pos=[H[0], 0, H[2] + 0.4], keys=[k('MV10:redevenue', visible=True)]),
            P('pinceau', 'marker', scale=1.6, on={'actor': 'mec', 'hand': 'R'}, keys=[k('MV9', visible=False)]),
            jet('jet1', [-2.6, 1.15, 1.0], 'MV9:incendie', 'MV10.end+0.6'), jet('jet2', [0.6, 1.15, 1.2], 'MV9:incendie', 'MV10.end+0.6'),
            P('eclabous', 'dustPuff', scale=3.0, visible=False, pos=[-1.0, 1.6, -3.4], opts={'color': '#DDEFF5', 'period': 0.8}, keys=[k('MV9:incendie', visible=True), k('MV10.end+0.6', visible=False)])],
  'sfx': [{'at': 'MV9:pompiers', 'name': 'siren', 'vol': 0.45}, {'at': 'MV9:incendie', 'name': 'splash', 'vol': 0.6}, {'at': 'MV10:arrosée', 'name': 'splash', 'vol': 0.6},
          {'at': 'MV10:redevenue', 'name': 'poof', 'vol': 0.5}],
  'cams': [WIDE(0, 58), cam('MV8:rouge', 'mec', 'ms', angle=0),
           POV('MV9', [4.2, 2.0, 5.6], [-1.0, 1.8, -3.5], 56),
           WIDE('MV10:redevenue-0.3', 58), cam('MV10:verte', 'mec', 'cu', angle=0)],
  'tail': 1.4,
})
write('maisonverte', 'La maison verte', scenes, {'facteur': {'preset': 'lemec_beige', 'hat': 'copcap', 'hatColor': '#2C4A8A', 'seed': 15}, 'femme': {'preset': 'femme', 'seed': 21},
                                                 'pompier1': {**FIRE, 'seed': 3}, 'pompier2': {**FIRE, 'seed': 5}})
