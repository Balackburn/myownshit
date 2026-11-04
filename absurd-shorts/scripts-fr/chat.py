#!/usr/bin/env python3
"""LE CHAT (viral-video-writing loop, score_fr.py 100/100). Hook with a number (two minutes) -> the cat inflates and flies out
of the window -> re-hooks: the control tower at 3 000 m, the firemen's 3 m ladder, a stadium, sponsors, ten times his pay ->
low point: the cat buys the flat, he sleeps in the basket -> loop: the cat dries him with the hair dryer (he starts to swell)."""
from actu_common import *

CAT = {'type': 'creature', 'name': 'cat', 'opts': {'seed': 6}}
DRYER = {'actor': 'mec', 'hand': 'R'}
scenes = []
scenes.append({
  'id': 'salle', 'set': 'chambre', 'setOpts': {'poster': 'MIAOU', 'posterBg': '#F2C230', 'posterFg': '#B5302A'}, 'ambience': None,
  'lines': [L('CH1', "Ce mec a séché son chat au sèche-cheveux pour gagner deux minutes.", highlight=['sèche-cheveux', 'deux']),
            L('CH2', "Le chat a gonflé. Puis il s'est envolé par la fenêtre.", highlight=['gonflé.', 'envolé'])],
  'actors': [act('mec', [0.9, 0, -0.9], -115, 'holdOut', 'happy', keys=[k('CH2:gonflé', clip='startle', expr='shocked')]),
             act('chat', [-0.2, 0, -1.25], 70, 'idle', 'neutral', keys=[k('CH2', scale=3.2, dur=0.9, ease='out'), k('CH2:gonflé', expr='surprised'),
                                                                          k('CH2:envolé', to=[-4.0, 1.6, -0.6], glide=True, dur=1.0, ease='in', face='keep'),
                                                                          k('CH2:envolé+1.0', to=[-7.5, 2.8, -0.6], glide=True, dur=0.6, face='keep')])],
  'props': [P('seche', 'hairDryer', on=DRYER)],
  'sfx': [{'at': 'CH1:sèche', 'name': 'wind', 'vol': 0.4}, {'at': 'CH2:gonflé', 'name': 'spring', 'vol': 0.5}, {'at': 'CH2:envolé', 'name': 'whoosh', 'vol': 0.6}],
  'cams': [cam(0, ['mec', 'chat'], 'ms', worldAngle=-70),
           cam('CH2', ['mec', 'chat'], 'fs', worldAngle=25),
           POV('CH2:envolé', [0.8, 1.6, 2.6], [-2.8, 1.6, -0.6], 56)],
  'tail': 0.2,
})
scenes.append({
  'id': 'ciel', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('CH3', "La tour de contrôle l'a repéré à trois mille mètres.", highlight=['trois', 'mille']),
            L('CH4', "Alors ce con a appelé les pompiers. Ils ont sorti une échelle de trois mètres.", highlight=['pompiers.', 'trois'])],
  'actors': [act('chat', [-6, 9.5, -7], 90, 'idle', 'surprised', scale=3.2, keys=[k(0, to=[6, 10.5, -7], glide=True, dur=7.0, face='keep')]),
             act('mec', [0.4, 0, 0.6], 170, 'lookUp', 'shocked', visible=False, keys=[k('CH4', visible=True)]),
             act('pompier1', [-0.9, 0, 0.2], 160, 'lookUp', 'neutral', visible=False, keys=[k('CH4:pompiers', visible=True)]),
             act('pompier2', [1.6, 0, 0.1], -160, 'lookUp', 'neutral', visible=False, keys=[k('CH4:pompiers', visible=True)])],
  'props': [P('avion', 'plane', scale=0.6, pos=[-40, 13, -26], ry=90, keys=[k(0, to=[40, 13, -26], dur=4.0, ease='linear')]),
            P('echelle', 'ladder', visible=False, pos=[0.4, 0, -0.6], opts={'h': 3.0, 'lean': 0.08}, keys=[k('CH4:échelle', visible=True)])],
  'sfx': [{'at': 0.2, 'name': 'jet', 'vol': 0.4}, {'at': 'CH4:pompiers', 'name': 'siren', 'vol': 0.35}, {'at': 'CH4:échelle', 'name': 'thud', 'vol': 0.5}],
  'cams': [POV(0, [1.0, 1.5, 4.5], [0, 8.5, -7], 60),
           POV('CH4', [0.9, 1.0, 5.5], [0.2, 3.0, -2.0], 62)],
  'tail': 0.2,
})
scenes.append({
  'id': 'stade', 'set': 'fair', 'ambience': 'park', 'ambienceVol': 0.6,
  'crowd': [{'id': 'fans', 'count': 6, 'spec': {'preset': 'lemec_charcoal', 'seed': 81}, 'clip': 'celebrate', 'ry': 180,
             'positions': [[-2.4, 0, 1.6], [-1.2, 0, 1.9], [1.2, 0, 1.9], [2.4, 0, 1.6], [-3.4, 0, 1.0], [3.4, 0, 1.0]]}],
  'lines': [L('CH5', "Le chat a atterri dans un stade. Les sponsors ont adoré.", highlight=['stade.', 'sponsors']),
            L('CH6', "Depuis, il vole au-dessus des matchs, avec de la pub sur le ventre.", highlight=['pub']),
            L('CH7', "Il gagne dix fois plus que ce mec.", highlight=['dix', 'fois'])],
  'actors': [act('chat', [0, 3.6, -3.2], 0, 'idle', 'smug', scale=3.2, keys=[k(0, to=[0.6, 4.0, -3.4], glide=True, dur=6.0, face='keep')]),
             act('mec', [0.3, 0, 1.1], 180, 'lookUp', 'unimpressed', keys=[k('CH7', face=10, turn=0.3, clip='showPhone')])],
  'props': [P('pub', 'signBoard', opts={'text': 'CROQUETTES MIAOU', 'bg': '#F2C230', 'fg': '#B5302A', 'w': 1.5, 'h': 0.45, 'height': 0, 'posts': False}, on={'actor': 'chat', 'offset': [0, -0.25, 0.42]}),
            P('piece', 'coin', scale=1.4, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('CH7', visible=True)]),
            P('magot', 'moneySack', scale=1.3, visible=False, pos=[-1.6, 0.41, -3.4], keys=[k('CH7', visible=True)])],
  'sfx': [{'at': 'CH5:stade', 'name': 'whistle', 'vol': 0.4}, {'at': 'CH5:adoré', 'name': 'tada', 'vol': 0.4}, {'at': 'CH7:dix', 'name': 'cash', 'vol': 0.5}],
  'cams': [POV(0, [0.5, 2.2, 7.0], [0.2, 2.6, -2.5], 55),
           cam('CH6', 'chat', 'ms', worldAngle=0, noOcclusion=True),
           cam('CH7', 'mec', 'mcu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'appart', 'set': 'livingRoom', 'ambience': None,
  'lines': [L('CH8', "Le mois dernier, il a racheté l'appartement.", highlight=["l'appartement."]),
            L('CH9', "Putain, ce mec dort dans le panier.", highlight=['panier.']),
            L('CH10', "Le chat le sèche au sèche-cheveux.", highlight=['sèche-cheveux.'])],
  'actors': [act('chat', [0, 0.45, -2.85], 0, 'idle', 'smug', scale=2.4),
             act('mec', [1.3, 0.12, -0.7], 90, 'sleepSide', 'sleepy', keys=[k('CH10', expr='shocked'), k('CH10:sèche', scale=1.35, dur=1.4, ease='out')])],
  'props': [P('panier', 'catBasket', scale=2.7, pos=[1.3, 0, -0.75]), P('vendu', 'soldSign', pos=[2.6, 0, -2.4], ry=-30),
            P('papiers', 'documents', pos=[-0.6, 0.47, -2.7]),
            P('seche', 'hairDryer', scale=2.2, visible=False, on={'actor': 'chat', 'offset': [0.45, 0.25, 0.55]}, keys=[k('CH10', visible=True)])],
  'sfx': [{'at': 'CH8:racheté', 'name': 'cash', 'vol': 0.4}, {'at': 'CH10:sèche', 'name': 'wind', 'vol': 0.5}, {'at': 'CH10.end+0.3', 'name': 'spring', 'vol': 0.4}],
  'cams': [cam(0, 'chat', 'ms', angle=0),
           cam('CH9', 'mec', 'ms', worldAngle=10),
           cam('CH10', ['mec', 'chat'], 'fs', worldAngle=15),
           cam('CH10:sèche+0.3', 'mec', 'mcu', worldAngle=10, move='push', amount=0.04)],
  'tail': 1.4,
})
FIRE = {'preset': 'lemec_charcoal', 'outfit': 'worker', 'hat': 'firehelmet', 'suit': '#2C3A5A'}
write('chat', 'Le chat', scenes, {'chat': CAT, 'pompier1': {**FIRE, 'seed': 3}, 'pompier2': {**FIRE, 'seed': 5}})
