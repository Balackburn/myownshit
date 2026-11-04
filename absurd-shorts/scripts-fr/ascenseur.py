#!/usr/bin/env python3
"""L'ASCENSEUR (viral-video-writing loop, score_fr.py 100/100). Hook with a number (third floor) -> it doesn't stop: tenth floor,
the roof, the clouds -> NASA tracks it for three days -> alarm button -> the villain: "un technicien passera entre 8 h et 18 h"
-> it stops on the Moon, "third floor" -> two years waiting -> callback: the technician came yesterday, to the third floor ->
loop: the "avis de passage" on the lobby's elevator door (the first location)."""
from actu_common import *

EL = [0, 0, -2.75]
IN = [EL[0], 0.12, EL[2] - 0.1]
BEARD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.02, 0.1]}
FLOORS = [0, 1, 2, 3, 4, 7, 10, 25, 99, '∞']
scenes = []
scenes.append({
  'id': 'hall', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('AS1', "Ce mec a pris l'ascenseur pour monter au troisième étage.", highlight=["l'ascenseur", 'troisième']),
            L('AS2', "L'ascenseur ne s'est pas arrêté.", highlight=['arrêté.'])],
  'actors': [act('mec', [2.6, 0, 0.4], -120, 'idle', 'neutral', keys=[k(0.05, to=IN, clip='walk', speed=1.9, faceEnd=0, then='stand'),
                                                                     k('AS1:troisième', clip='pokeFinger', expr='smug'), k('AS2', clip='stand', expr='shocked'),
                                                                     k('AS2:arrêté-0.3', to=[IN[0], 14.12, IN[2]], glide=True, dur=2.4, ease='in', clip='stand', then='stand', face='keep')])],
  'props': [P('cabine', 'elevator', pos=EL, opts={'glass': True, 'floors': FLOORS, 'openAt': 0, 'closeAt': 'AS1:étage', 'countAt': 'AS2', 'rate': 3.2},
              keys=[k('AS2:arrêté-0.3', to=[EL[0], 14, EL[2]], dur=2.4, ease='in')])],
  'sfx': [{'at': 'AS1:troisième', 'name': 'ding', 'vol': 0.5}, {'at': 'AS2', 'name': 'whoosh', 'vol': 0.4}, {'at': 'AS2:arrêté', 'name': 'jet', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'fs', worldAngle=25),
           POV('AS1:étage', [EL[0], 2.45, EL[2] + 1.65], [EL[0], 2.6, EL[2] + 0.76], 32),
           POV('AS2+0.3', [2.4, 1.6, 4.4], [0, 3.0, -2.75], 56)],
  'tail': 0.15,
})
scenes.append({
  'id': 'toit', 'set': 'rooftopPowerLine', 'ambience': 'wind', 'ambienceVol': 0.5,
  'lines': [L('AS3', "Il est passé au dixième. Puis sur le toit.", highlight=['dixième.', 'toit.'])],
  'actors': [act('mec', [0, -2.6, -2.0], 0, 'stand', 'shocked', keys=[k('AS3:Puis', to=[0, 6.12, -2.0], glide=True, dur=1.6, ease='out', clip='stand', then='lookDown', face='keep')])],
  'props': [P('cabine', 'elevator', pos=[0, -2.72, -1.9], opts={'glass': True, 'floors': [10, 10], 'countAt': 0}, keys=[k('AS3:Puis', to=[0, 6.0, -1.9], dur=1.6, ease='out')]),
            P('trou', 'dustPuff', scale=2.0, visible=False, pos=[0, 0.05, -1.9], opts={'color': '#9CA3A8', 'once': True, 'period': 1.0, 'startAt': 'AS3:Puis'}, keys=[k('AS3:Puis', visible=True)])],
  'sfx': [{'at': 'AS3:Puis', 'name': 'thud', 'vol': 0.7}, {'at': 'AS3:toit', 'name': 'whoosh', 'vol': 0.6}],
  'cams': [POV(0, [3.2, 1.7, 4.5], [0, 2.6, -1.9], 58)],
  'tail': 0.15,
})
scenes.append({
  'id': 'nuages', 'set': 'street', 'ambience': 'wind', 'ambienceVol': 0.5,
  'lines': [L('AS4', "Puis dans les nuages.", highlight=['nuages.'])],
  'actors': [act('mec', [0, 40.12, -3.0], 0, 'lookDown', 'scared', keys=[k(0, to=[0, 46.12, -3.0], glide=True, dur=1.6, clip='lookDown', then='lookDown', face='keep')])],
  'props': [P('cabine', 'elevator', pos=[0, 40, -2.9], opts={'glass': True, 'floors': [99, 99], 'countAt': 0}, keys=[k(0, to=[0, 46, -2.9], dur=1.6)]),
            *[P(f'nuage{i}', 'cloud', pos=p, opts={'seed': 30 + i, 'scale': 1.6}) for i, p in enumerate([[-3.5, 43, -5], [3.2, 45, -4], [-2.0, 47.5, -1.5], [2.6, 41.5, -1.0]])]],
  'sfx': [{'at': 0, 'name': 'wind', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'fs', worldAngle=20, move='track', noOcclusion=True)],
  'tail': 0.2,
})
scenes.append({
  'id': 'nasa', 'set': 'classroom', 'ambience': 'office', 'ambienceVol': 0.5,
  'daynight': {'from': 'AS5:pendant', 'period': 0.45},
  'lines': [L('AS5', "La NASA l'a suivi au radar pendant trois jours.", highlight=['NASA', 'radar', 'trois'])],
  'actors': [act('op1', [-1.0, 0.12, -0.3], 180, 'sitWrite', 'neutral'), act('op2', [1.0, 0.12, -0.3], 180, 'sitLookItem', 'surprised')],
  'props': [P('radar', 'tv', scale=2.2, pos=[0, 0.6, -2.9], opts={'text': '● ASCENSEUR', 'on': True}),
            P('controle', 'signBoard', pos=[0, 0, -3.1], opts={'text': 'CENTRE DE CONTRÔLE', 'bg': '#1E2A3A', 'fg': '#F2C230', 'w': 2.2, 'h': 0.36, 'height': 2.85, 'posts': False})],
  'sfx': [{'at': 'AS5:radar', 'name': 'beep', 'vol': 0.4}, {'at': 'AS5:radar+0.6', 'name': 'beep', 'vol': 0.4}, {'at': 'AS5:jours', 'name': 'beep', 'vol': 0.4}],
  'cams': [POV(0, [0.4, 1.7, 2.6], [0, 1.6, -2.5], 54)],
  'tail': 0.2,
})
scenes.append({
  'id': 'cabine', 'set': 'spaceVoid', 'ambience': None,
  'lines': [L('AS6', "Alors ce con a appuyé sur le bouton d'alarme.", highlight=["d'alarme."]),
            L('AS7', "Un technicien passera entre huit heures et dix-huit heures.", 'hautparleur')],
  'actors': [act('mec', [0, 0.12, -0.1], 0, 'stand', 'scared', keys=[k('AS6:appuyé', face=80, turn=0.2, clip='pokeFinger', expr='angry'), k('AS7', face=0, turn=0.3, clip='stand', expr='unimpressed')])],
  'props': [P('cabine', 'elevator', pos=[0, 0, 0], opts={'glass': True, 'floors': ['∞', '∞'], 'countAt': 0})],
  'sfx': [{'at': 'AS6:bouton', 'name': 'ring', 'vol': 0.7}, {'at': 'AS7', 'name': 'static', 'vol': 0.3}],
  'cams': [cam(0, 'mec', 'fs', worldAngle=20, noOcclusion=True), cam('AS7', 'mec', 'cu', angle=0, noOcclusion=True, move='push', amount=0.04)],
  'tail': 0.2,
})
scenes.append({
  'id': 'lune', 'set': 'spaceVoid', 'ambience': None,
  'lines': [L('AS8', "L'ascenseur s'est arrêté sur la Lune. Au troisième.", highlight=['Lune.', 'troisième.']),
            L('AS9', "Depuis deux ans, il attend le technicien.", highlight=['deux', 'technicien.'])],
  'actors': [act('mec', [0, 0.12, -2.1], 0, 'stand', 'shocked', keys=[k('AS8:troisième', to=[1.3, 0, -0.6], glide=True, dur=0.05, face=-20, clip='sitFloor', then='sitFloor', expr='unimpressed')])],
  'props': [P('sol', 'moonSurface', opts={'r': 30}), P('cabine', 'elevator', pos=[0, 0, -2.0], opts={'glass': True, 'floors': [3, 3], 'countAt': 0, 'openAt': 0}),
            P('etage', 'signBoard', pos=[-1.4, 0, -1.6], opts={'text': 'ÉTAGE 3', 'bg': '#F6F1E3', 'fg': '#1E1E22', 'w': 0.8, 'h': 0.3, 'height': 1.1}),
            P('barbe', 'beard', scale=0.1, opts={'color': '#E6E2D8'}, on=BEARD, keys=[k('AS9', scale=2.4, dur=1.8, ease='linear')])],
  'sfx': [{'at': 'AS8:Lune', 'name': 'ding', 'vol': 0.5}, {'at': 'AS9:deux', 'name': 'ticks', 'vol': 0.4}],
  'cams': [POV(0, [2.8, 1.6, 4.0], [0.2, 1.1, -1.8], 54), cam('AS9', 'mec', 'ms', angle=0, move='push', amount=0.04)],
  'tail': 0.2,
})
scenes.append({
  'id': 'terre', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('AS10', "Putain, il est passé hier. Au troisième étage.", highlight=['hier.', 'troisième']),
            L('AS11', "Il a laissé un avis de passage.", highlight=['avis', 'passage.'])],
  'actors': [act('technicien', [-2.4, 0, 0.6], 60, 'idle', 'neutral', keys=[k(0.1, to=[0.55, 0, -1.65], clip='walk', speed=2.0, faceEnd=180, then='pokeFinger'),
                                                                          k('AS11', to=[3.2, 0, 0.8], clip='walk', speed=2.0, faceEnd=60, then='walk')])],
  'props': [P('cabine', 'elevator', pos=EL, opts={'glass': False, 'floors': [3, 3], 'countAt': 0}),
            P('etage', 'signBoard', pos=[1.4, 0, -2.6], opts={'text': 'ÉTAGE 3', 'bg': '#F6F1E3', 'fg': '#1E1E22', 'w': 0.8, 'h': 0.3, 'height': 1.3}),
            P('avis', 'avisPassage', scale=2.2, visible=False, pos=[EL[0] + 0.2, 1.35, EL[2] + 0.79], keys=[k('AS10:troisième', visible=True)]),
            P('caisse', 'briefcase', scale=0.9, on={'actor': 'technicien', 'hand': 'L'})],
  'sfx': [{'at': 'AS10:troisième', 'name': 'paper', 'vol': 0.5}, {'at': 'AS11:passage', 'name': 'ding', 'vol': 0.4}],
  'cams': [cam(0, 'technicien', 'fs', worldAngle=20),
           POV('AS11', [EL[0] + 0.2, 1.38, EL[2] + 1.45], [EL[0] + 0.2, 1.35, EL[2] + 0.79], 30)],
  'tail': 1.4,
})
write('ascenseur', "L'ascenseur", scenes, {'op1': {'preset': 'lemec_glasses', 'seed': 4}, 'op2': {'preset': 'madame', 'seed': 13, 'glasses': True},
                                            'technicien': {'preset': 'lemec_charcoal', 'outfit': 'worker', 'hat': 'hardhat', 'seed': 7}})
