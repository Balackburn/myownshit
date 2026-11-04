#!/usr/bin/env python3
"""LE SERVICE CLIENT (viral-video-writing loop, score_fr.py 95/100). Hook (cancel a subscription) -> the villain at 4 s (the
robot voice) -> re-hooks: six months, one year (his wife leaves), the complaint put on hold too -> three years later a human
answers -> "un nouveau forfait ?" -> he says yes -> loop: he calls back to cancel (the first shot again)."""
from actu_common import *

SPOT = [0.4, 0, -1.3]
BEARD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.02, 0.1]}
HOLD = lambda until, vol=0.22: {'name': 'music:zouk', 'at': 0, 'until': until, 'vol': vol}
scenes = []
scenes.append({
  'id': 'salon', 'set': 'livingRoom', 'ambience': None,
  'daynight': {'from': 'SC4', 'period': 0.55},
  'lines': [L('SC1', "Ce mec a appelé le service client pour résilier son abonnement.", highlight=['service', 'résilier']),
            L('SC2', "Votre appel est important pour nous. Tapez 1.", 'robot'),
            L('SC3', "Il a tapé 1. Puis 2. Puis dièse.", highlight=['1.', '2.', 'dièse.']),
            L('SC4', "Au bout de six mois, il connaissait la musique d'attente par cœur.", highlight=['six', 'cœur.']),
            L('SC5', "Au bout d'un an, sa femme est partie avec le livreur de pizza.", highlight=['an,', 'pizza.'])],
  'actors': [act('mec', SPOT, 0, 'phoneCall', 'neutral', keys=[
                 k('SC3', clip='pokeFinger', expr='angry'), k('SC4', clip='nod', expr='sleepy', params={'freq': 1.6}), k('SC5', clip='phoneCall', expr='unimpressed')]),
             act('femme', [-2.4, 0, -2.2], 30, 'stand', 'neutral', visible=False, keys=[k('SC5-0.3', visible=True), k('SC5:partie', to=[4.5, 0, 0.6], clip='walk', speed=1.7, faceEnd=90, then='walk')]),
             act('livreur', [-1.6, 0, -2.4], 30, 'stand', 'happy', visible=False, keys=[k('SC5-0.3', visible=True), k('SC5:partie+0.15', to=[5.2, 0, 0.3], clip='walk', speed=1.7, faceEnd=90, then='walk')])],
  'props': [P('tel', 'phone911', on={'actor': 'mec', 'hand': 'R'}),
            P('barbe', 'beard', scale=0.2, opts={'color': '#2A2420'}, on=BEARD, keys=[k('SC4', scale=1.2, dur=2.6, ease='linear')]),
            P('pizza', 'pizza', scale=0.9, on={'actor': 'livreur', 'hand': 'L', **HAND_FLAT})],
  'sfx': [HOLD('SC5.end+0.2'), {'at': 'SC3:1.', 'name': 'beep', 'vol': 0.5}, {'at': 'SC3:2.', 'name': 'beep', 'vol': 0.5}, {'at': 'SC3:dièse', 'name': 'beep', 'vol': 0.5},
          {'at': 'SC5:partie', 'name': 'step', 'vol': 0.4}],
  'cams': [cam(0, 'mec', 'ms', angle=10),
           cam('SC2', 'mec', 'cu', angle=0),
           cam('SC3', 'mec', 'mcu', angle=-20),
           cam('SC4', 'mec', 'ms', angle=15, move='push', amount=0.04),
           cam('SC5', ['mec', 'femme', 'livreur'], 'fs', worldAngle=10)],
  'tail': 0.2,
})
DESK = [-2.7, 0, -2.1]
scenes.append({
  'id': 'police', 'set': 'policeStation', 'ambience': 'station',
  'lines': [L('SC6', "Alors ce con a porté plainte pour séquestration.", highlight=['plainte', 'séquestration.']),
            L('SC7', "La plainte aussi a été mise en attente.", highlight=['attente.'])],
  'actors': [act('commissaire', [DESK[0], 0.12, DESK[2] - 0.62], 0, 'sitWrite', 'neutral', keys=[k('SC7', clip='phoneCall', expr='unimpressed')]),
             act('mec', [DESK[0] + 0.9, 0, DESK[2] + 0.9], -140, 'phoneCall', 'angry')],
  'props': [P('tel', 'phone911', on={'actor': 'mec', 'hand': 'R'}), P('telC', 'phone911', visible=False, on={'actor': 'commissaire', 'hand': 'R'}, keys=[k('SC7', visible=True)]),
            P('barbe', 'beard', scale=1.4, opts={'color': '#2A2420'}, on=BEARD)],
  'sfx': [{'at': 'SC7:attente', 'name': 'music:zouk', 'until': 'SC7.end+0.2', 'vol': 0.22}],
  'cams': [cam(0, ['mec', 'commissaire'], 'ms', worldAngle=-50),
           cam('SC7', 'commissaire', 'cu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'fin', 'set': 'livingRoom', 'ambience': None,
  'lines': [L('SC8', "Trois ans plus tard, quelqu'un a décroché.", highlight=['Trois', 'décroché.']),
            L('SC9', "Bonjour, voulez-vous un nouveau forfait ?", 'conseillere'),
            L('SC10', "Putain, il a dit oui.", highlight=['oui.']),
            L('SC11', "Il rappelle pour résilier.", highlight=['résilier.'])],
  'actors': [act('mec', SPOT, 0, 'phoneCall', 'sleepy', keys=[k('SC8:décroché', clip='startle', expr='shocked'), k('SC9', clip='phoneCall', expr='shocked'),
                                                             k('SC10', clip='nod', expr='grin'), k('SC11', clip='pokeFinger', expr='unimpressed')]),
             act('conseillere', [-3.5, 0, -2.6], 30, 'phoneCall', 'happy', visible=False, keys=[k('SC9', visible=True), k('SC10', visible=False)])],
  'props': [P('tel', 'phone911', on={'actor': 'mec', 'hand': 'R'}), P('telK', 'phone911', on={'actor': 'conseillere', 'hand': 'R'}),
            P('barbe', 'beard', scale=2.6, opts={'color': '#E6E2D8'}, on=BEARD),
            P('toile', 'spiderWeb', pos=[-0.6, 1.9, -1.9], opts={'r': 0.45}), P('toile2', 'spiderWeb', pos=[1.6, 2.4, -3.5], opts={'r': 0.6})],
  'sfx': [{'at': 0, 'name': 'music:zouk', 'until': 'SC8:décroché', 'vol': 0.22}, {'at': 'SC8:décroché', 'name': 'needle', 'vol': 0.6},
          {'at': 'SC11:rappelle', 'name': 'beep', 'vol': 0.5}, {'at': 'SC11:pour', 'name': 'beep', 'vol': 0.5}, {'at': 'SC11.end+0.2', 'name': 'music:zouk', 'until': 'SC11.end+1.4', 'vol': 0.22}],
  'cams': [cam(0, 'mec', 'ms', angle=10),
           cam('SC9', 'conseillere', 'ms', angle=0),
           cam('SC10', 'mec', 'cu', angle=0),
           cam('SC11', 'mec', 'ms', angle=10)],
  'tail': 1.4,
})
write('service', 'Le service client', scenes, {'femme': {'preset': 'femme', 'seed': 21}, 'livreur': {'preset': 'lemec_beige', 'seed': 18, 'hat': 'copcap', 'hatColor': '#B5302A'},
                                                 'conseillere': {'preset': 'madame', 'seed': 52, 'glasses': True}})
