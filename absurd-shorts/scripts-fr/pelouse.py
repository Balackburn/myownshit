#!/usr/bin/env python3
"""LA PELOUSE (viral-video-writing loop, score_fr.py 100/100). Hook with a number (6 a.m.) -> the villain at 5 s (the neighbour:
"encore une fois et j'appelle les flics") -> he mows again -> the lawn sues for assault -> sentenced to water it every day ->
four metres of grass -> the neighbour's house and the neighbour disappear in it -> loop: at 6 a.m., a mower... the neighbour."""
from actu_common import *

DAWN = 'sepia(0.22) saturate(0.85) brightness(0.88) hue-rotate(-8deg)'
NB_HOUSE = [-10.2, 0, -6.0]
NB_DOOR = [-5.0, 0, -1.5]
def mower(id_, x0, z, keys=()): return P(id_, 'lawnmower', pos=[x0, 0, z], ry=90, opts={'runAt': ['PE9']}, keys=list(keys))
scenes = []
scenes.append({
  'id': 'jardin', 'set': 'pavillon', 'grade': DAWN, 'ambience': 'park', 'ambienceVol': 0.4,
  'lines': [L('PE1', "Ce mec a tondu sa pelouse à six heures du matin pour avoir le plus beau jardin du quartier.", highlight=['six', 'heures', 'jardin']),
            L('PE2', "Le voisin a crié par la fenêtre.", highlight=['voisin']),
            L('PE3', "Encore une fois et j'appelle les flics !", 'voisin'),
            L('PE4', "Alors ce con a tondu une deuxième fois.", highlight=['deuxième'])],
  'actors': [act('mec', [-0.4, 0, -1.4], -90, 'pushCart', 'smug', keys=[k(0.05, to=[-3.8, 0, -1.4], glide=True, dur=4.4, clip='pushCart', then='stand', face='keep'),
                                                                       k('PE2', face=-60, turn=0.3, clip='stand', expr='neutral'),
                                                                       k('PE4', face=90, turn=0.25, clip='pushCart', expr='grin'), k('PE4+0.25', to=[0.2, 0, -1.4], glide=True, dur=2.0, clip='pushCart', then='stand', face='keep')]),
             act('voisin', NB_DOOR, 55, 'stand', 'sleepy', keys=[k('PE2', clip='yell', expr='angry'), k('PE3', clip='angryFist', expr='angry')])],
  'props': [P('tondeuse', 'lawnmower', pos=[-1.1, 0, -1.4], ry=-90, opts={'runAt': [0], 'stopAt': ['PE2']}, keys=[k(0.05, to=[-4.5, 0, -1.4], dur=4.4, ease='linear'), k('PE4', visible=False)]),
            P('tondeuse2', 'lawnmower', visible=False, pos=[-3.1, 0, -1.4], ry=90, opts={'runAt': ['PE4']}, keys=[k('PE4', visible=True), k('PE4+0.25', to=[0.9, 0, -1.4], dur=2.0, ease='linear')]),
            P('maisonV', 'house', pos=NB_HOUSE, opts={'w': 4.5, 'd': 4, 'h': 2.6, 'color': '#D8CFBA', 'roof': '#5A4A6A'})],
  'sfx': [{'at': 0, 'name': 'engine', 'vol': 0.55}, {'at': 'PE2', 'name': 'grunt', 'vol': 0.4}, {'at': 'PE4:tondu', 'name': 'engine', 'vol': 0.55}],
  'cams': [{'at': 0, 'from': [-5.2, 1.5, 1.0], 'to': [-6.6, 1.5, 0.9], 'lookAt': [-0.6, 1.0, -1.4], 'lookAt2': [-3.6, 1.0, -1.4], 'lens': 40, 'ease': 'linear'},  # front 3/4, he mows towards us
           cam('PE2', 'voisin', 'ms', angle=0),
           cam('PE3', 'voisin', 'cu', angle=0),
           cam('PE4', 'mec', 'ms', angle=-60, move='track')],
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('PE5', "La pelouse a porté plainte pour coups et blessures.", highlight=['pelouse', 'blessures.']),
            L('PE6', "Le juge l'a condamné à l'arroser tous les jours.", highlight=["l'arroser", 'jours.'])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('PE6', clip='sitPoint', expr='angry')]),
             act('mec', [0.9, 0, -1.7], 180, 'stand', 'shocked', keys=[k('PE6:arroser', face=20, turn=0.3, clip='showPhone', expr='sad')])],
  'props': [P('herbe', 'grassPatch', pos=[2.5, 1.11, -3.35]), P('yeux', 'googlyEyes', opts={'r': 0.05, 'sep': 0.07}, on={'actor': 'herbe', 'offset': [0, 0.23, 0.22]}),
            P('pansement', 'faceLumps', scale=0.6, on={'actor': 'herbe', 'offset': [0.1, 0.18, 0.2]}),
            P('arrosoir', 'wateringCan', scale=1.3, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('PE6:arroser', visible=True)])],
  'sfx': [{'at': 'PE5:blessures', 'name': 'sting', 'vol': 0.3}, {'at': 'PE6:condamné', 'name': 'gavel', 'vol': 0.6}],
  'cams': [POV(0, [2.6, 1.5, -2.2], [2.5, 1.25, -3.35], 40), cam('PE6', 'juge', 'mcu', angle=0), cam('PE6:arroser', 'mec', 'ms', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'jungle', 'set': 'pavillon', 'ambience': 'park', 'ambienceVol': 0.45,
  'lines': [L('PE7', "En trois mois, l'herbe a fait quatre mètres de haut.", highlight=['quatre', 'mètres']),
            L('PE8', "La maison du voisin a disparu dedans. Le voisin aussi.", highlight=['disparu', 'aussi.']),
            L('PE9', "Putain, à six heures du matin, on a entendu une tondeuse.", highlight=['six', 'tondeuse.']),
            L('PE10', "C'était le voisin.", highlight=['voisin.'])],
  'actors': [act('mec', [1.8, 0, 2.3], 20, 'stand', 'neutral', keys=[k('PE7', expr='shocked'), k('PE9', expr='suspicious'), k('PE10', clip='stareCamera', expr='unimpressed')]),
             act('voisin', [-4.6, 0, 1.4], 60, 'stand', 'angry', keys=[k('PE8:voisin', to=[-6.5, 0, -1.6], clip='walk', speed=1.4, faceEnd=-130, then='walk', expr='scared'),
                                                                       k('PE8.end+0.1', visible=False), k('PE10', visible=True),
                                                                       k('PE10', to=[-3.2, 0, 1.2], glide=True, dur=0.05, face=90, clip='pushCart', then='pushCart', expr='grin'),
                                                                       k('PE10+0.1', to=[0.2, 0, 1.2], glide=True, dur=2.2, clip='pushCart', then='stand', face='keep')])],
  'props': [P('herbe', 'tallGrass', scale=0.05, pos=[-3.5, 0, -3.6], opts={'w': 14, 'd': 8, 'h': 4, 'count': 900}, keys=[k('PE7', scale=1, dur=2.2, ease='out')]),
            P('maisonV', 'house', pos=NB_HOUSE, opts={'w': 4.5, 'd': 4, 'h': 2.6, 'color': '#D8CFBA', 'roof': '#5A4A6A'}, keys=[k('PE8:disparu', to=[NB_HOUSE[0], -5.5, NB_HOUSE[2]], dur=1.2, ease='in')]),
            P('arrosoir', 'wateringCan', scale=1.3, on={'actor': 'mec', 'hand': 'R'}),
            mower('tondeuse', -2.5, 1.2, [k('PE10+0.1', to=[0.9, 0, 1.2], dur=2.2, ease='linear')])],
  'sfx': [{'at': 'PE7:herbe', 'name': 'whoosh', 'vol': 0.4}, {'at': 'PE8:disparu', 'name': 'gulp', 'vol': 0.4}, {'at': 'PE9:tondeuse', 'name': 'engine', 'vol': 0.6}, {'at': 'PE10', 'name': 'engine', 'vol': 0.6}],
  'cams': [POV(0, [4.2, 1.7, 7.6], [-1.0, 2.0, -1.0], 58),
           POV('PE8', [-2.0, 9.0, 7.0], [-8.5, 1.0, -5.5], 50),
           {**POV('PE9', [4.2, 1.7, 7.6], [-1.0, 2.0, -1.0], 58), 'grade': DAWN},
           {**cam('PE10', 'voisin', 'ms', angle=-60, move='track'), 'grade': DAWN},
           {**cam('PE10.end+0.4', 'mec', 'cu', angle=0), 'grade': DAWN}],
  'tail': 1.4,
})
write('pelouse', 'La pelouse', scenes, {'voisin': {'preset': 'mecPyjama', 'seed': 9}, 'juge': {'preset': 'judge'}})
