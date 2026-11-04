#!/usr/bin/env python3
"""LA PLANTE. Ce mec talks to his plant so it grows better -> it answers -> "Je veux être payée." -> thirty years of oxygen
at the going rate -> ce con stops breathing -> he holds out forty seconds (red, then purple) -> the plant sends a bailiff:
a cactus -> it seizes everything, even the sofa (with him on it) -> now he breathes on credit. (Classic formula, no news.)"""
from actu_common import *

LR = {'sofa': False, 'plant': False, 'tv': False, 'lamp': False}
SOFA = [0, 0, -3.05]
SEAT = [0.5, 0.2, -2.86]
PLANT = [-1.55, 0, -2.85]
EYES = {'actor': 'plante', 'offset': [0, 0.26, 0.18]}
KNEEL = [-0.85, 0, -2.45]
scenes = []
scenes.append({
  'id': 'salon', 'set': 'livingRoom', 'setOpts': LR, 'ambience': None,
  'lines': [L('V1', "Ce mec a parlé à sa plante pour qu'elle pousse mieux.", highlight=['plante']),
            L('V2', "Elle a répondu.", highlight=['répondu.']),
            L('V3', "Je veux être payée.", 'plante'),
            L('V4', "Trente ans d'oxygène, au tarif en vigueur.", highlight=["d'oxygène,"]),
            L('V5', "Alors ce con a arrêté de respirer.", highlight=['respirer.']),
            L('V6', "Il a tenu quarante secondes.", highlight=['quarante'])],
  'actors': [
    act('mec', KNEEL, -110, 'kneel', 'happy', keys=[
        k('V2', clip='startle', expr='shocked'),
        k('V4', face=0, turn=0.2, clip='showPhone', expr='shocked'),
        k('V5', face=-110, turn=0.2, clip='kneel'),
        k('V5:respirer', expr='angry', clip='stiff'),
        k('V5:respirer+0.35', visible=False)]),
    act('mecR', KNEEL, -110, 'stiff', 'angry', visible=False, keys=[k('V5:respirer+0.35', visible=True), k('V6:quarante', visible=False)]),
    act('mecV', KNEEL, -110, 'stiff', 'scared', visible=False, keys=[k('V6:quarante', visible=True), k('V6.end+0.1', visible=False)]),
    act('mec2', KNEEL, -110, 'startle', 'shocked', visible=False, keys=[k('V6.end+0.1', visible=True)]),
  ],
  'props': [P('canape', 'sofaProp', pos=SOFA),
            P('plante', 'plant', scale=1.5, pos=PLANT, keys=[k('V3', scale=1.68, dur=0.1), k('V3+0.18', scale=1.5, dur=0.1), k('V3+0.36', scale=1.68, dur=0.1), k('V3+0.54', scale=1.5, dur=0.1),
                                                          k('V3+0.72', scale=1.68, dur=0.1), k('V3+0.9', scale=1.5, dur=0.1)]),
            P('yeux', 'googlyEyes', visible=False, opts={'r': 0.05, 'sep': 0.06}, on=EYES, keys=[k('V2:répondu', visible=True)]),
            P('facture', 'bill', scale=1.7, visible=False, opts={'title': 'FACTURE', 'items': [['Oxygène (30 ans)', '84 312'], ['Frais de dossier', '15'], ['', '']], 'total': '84 327,00 €'},
              on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('V4', visible=True), k('V5', visible=False)])],
  'sfx': [{'at': 'V2:répondu', 'name': 'pop', 'vol': 0.5}, {'at': 'V4:oxygène', 'name': 'paper', 'vol': 0.5}, {'at': 'V5:respirer', 'name': 'gulp', 'vol': 0.5},
          {'at': 'V6', 'name': 'ticks', 'vol': 0.5}, {'at': 'V6.end+0.1', 'name': 'gasp', 'vol': 0.8}],
  'cams': [cam(0, ['mec', 'plante'], 'ms', worldAngle=-20, withProps=True),
           cam('V2', [[-1.55, 0.5, -2.6]], 'cu', worldAngle=10, noOcclusion=True),
           cam('V3+0.1', ['mec', 'plante'], 'ms', worldAngle=-25, withProps=True),
           cam('V4+0.2', 'facture', 'cu', worldAngle=0, noOcclusion=True, zoom=1.2),
           cam('V5', 'mec', 'cu', angle=-30),
           cam('V6', 'mecR', 'cu', angle=-30),
           cam('V6:quarante', 'mecV', 'cu', angle=-30, move='push', amount=0.05),
           cam('V6.end+0.1', 'mec2', 'ms', angle=-20)],
  'tail': 0.3,
})
scenes.append({
  'id': 'saisie', 'set': 'livingRoom', 'setOpts': LR, 'ambience': None,
  'lines': [L('V7', "La plante a envoyé un huissier. Un cactus.", highlight=['huissier.', 'cactus.']),
            L('V8', "Il a tout saisi.", highlight=['saisi.']),
            L('V9', "Putain, même le canapé.", highlight=['canapé.'])],
  'actors': [act('mec', SEAT, 0, 'sit', 'neutral', keys=[k('V7:cactus', expr='shocked'), k('V9:canapé', to=[0.5, 0, -2.75], glide=True, dur=0.25, clip='sitFloor', then='sitFloor', face='keep', expr='shocked')])],
  'props': [P('canape', 'sofaProp', pos=SOFA, keys=[k('V9:même', to=[8.5, 0, -3.05], dur=0.7, ease='in')]),
            P('tele', 'tv', pos=[3.0, 0, -1.6], ry=-40, keys=[k('V8', to=[9.0, 0, -1.6], dur=0.6, ease='in')]),
            P('chaise', 'chair', pos=[-3.0, 0, -0.9], ry=60, keys=[k('V8+0.3', to=[9.0, 0, -0.9], dur=0.8, ease='in')]),
            P('plante', 'plant', scale=1.5, pos=PLANT), P('yeux', 'googlyEyes', opts={'r': 0.05, 'sep': 0.06}, on=EYES),
            P('cactus', 'cactusPot', pos=[6.0, 0, -1.3], ry=-70, keys=[k('V7:huissier-0.2', to=[2.0, 0, -1.6], dur=0.9, ease='out', sfx='squeak')]),
            P('cyeux', 'googlyEyes', opts={'r': 0.04, 'sep': 0.05}, on={'actor': 'cactus', 'offset': [0, 1.0, 0.13]}),
            P('chapeau', 'porkpieHat', opts={'r': 0.17}, on={'actor': 'cactus', 'offset': [0, 1.24, 0]}),
            P('mallette', 'briefcase', scale=0.7, on={'actor': 'cactus', 'offset': [0.32, 0.12, 0.05]})],
  'sfx': [{'at': 'V7:cactus', 'name': 'sting', 'vol': 0.3}, {'at': 'V8', 'name': 'whoosh', 'vol': 0.5}, {'at': 'V8+0.3', 'name': 'whoosh', 'vol': 0.5},
          {'at': 'V9:même', 'name': 'whoosh', 'vol': 0.6}, {'at': 'V9:canapé+0.25', 'name': 'thud', 'vol': 0.6}],
  'cams': [cam(0, ['mec', 'cactus'], 'fs', worldAngle=10, elev=6, withProps=True),
           cam('V7:cactus', 'cactus', 'ms', worldAngle=-60, withProps=True),
           cam('V8', ['mec', [2.5, 1.0, -1.6]], 'fs', worldAngle=10, elev=6),
           cam('V9', 'mec', 'ms', angle=0)],
  'tail': 0.25,
})
scenes.append({
  'id': 'fin', 'set': 'livingRoom', 'setOpts': LR, 'ambience': None,
  'lines': [L('V10', "Maintenant, ce mec respire à crédit.", pre=0.3, highlight=['crédit.'])],
  'actors': [act('mec', [0.4, 0, -2.6], 0, 'sitFloor', 'sad', keys=[k('V10:crédit', clip='stareCamera', expr='unimpressed')])],
  'props': [P('compteur', 'oxyMeter', pos=[0.4, 1.75, -3.56], opts={'countAt': 'V10', 'rate': 1.6}),
            P('plante', 'plant', scale=1.5, pos=PLANT), P('yeux', 'googlyEyes', opts={'r': 0.05, 'sep': 0.06}, on=EYES)],
  'sfx': [{'at': 'V10', 'name': 'tick', 'vol': 0.5}, {'at': 'V10+0.62', 'name': 'tick', 'vol': 0.5}, {'at': 'V10+1.25', 'name': 'tick', 'vol': 0.5}, {'at': 'V10:crédit', 'name': 'cash', 'vol': 0.5}],
  'cams': [cam(0, ['mec', 'compteur'], 'fs', worldAngle=0, withProps=True),
           cam('V10:respire', 'compteur', 'cu', worldAngle=0, noOcclusion=True, zoom=1.2),
           cam('V10:crédit', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('plante', 'La plante', scenes, {
  'mecR': {'preset': 'lemec', 'tint': '#FF8A80'},
  'mecV': {'preset': 'lemec', 'tint': '#A890FF'},
  'mec2': {'preset': 'lemec'},
})
