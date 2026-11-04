#!/usr/bin/env python3
"""LE VOISIN DU DESSUS. Written with the viral-video-writing loop (5 hooks, 3 drafts, score_fr.py 100/100):
hook = a universal situation (broom against the ceiling) -> the villain at 4 s ("Tape plus fort !") -> the ceiling falls with
the sofa and forty guests -> the party goes on at his place -> complaint -> the judge: the ceiling was the neighbour's, and
everything under it -> low point: he sleeps in the cellar -> loop: he taps the ceiling with a broom (the opening shot).
Staging: a dollhouse cross-section (the party upstairs on a floor slab over his living room) so the fall reads at once."""
from actu_common import *

UP, DOWN = 3.14, 0.28                       # upstairs floor level, then the fallen slab's top
SLAB_C, SLAB_DOWN = [0, 3.0, -1.9], [0, 0.14, -1.9]
BROOM_UP = {'actor': 'mec', 'hand': 'R', 'rot': [3.1416, 0, 0]}     # held overhead, bristles up (pokes the ceiling)
GUESTS = [('g1', [-1.9, -1.2], 30), ('g2', [-0.5, -2.6], 0), ('g3', [2.0, -2.4], -20), ('g4', [-1.1, -0.7], 15)]
PARTY = [('voisin', [0.9, -1.5], 10)] + GUESTS
WIDE = lambda at: POV(at, [0.6, 2.7, 6.4], [0.5, 2.5, -1.5], 50)       # both floors at once
def music(until, vol=0.32): return {'name': 'music:zouk', 'at': 0, 'until': until, 'vol': vol}
scenes = []
fall = 'V4:tombé'
scenes.append({
  'id': 'salon', 'set': 'livingRoom', 'setOpts': {'sofa': False, 'tv': False}, 'lighting': 'night', 'ambience': None,
  'lines': [L('V1', "Ce mec a tapé au plafond avec un balai pour que son voisin baisse la musique.", highlight=['balai', 'musique.']),
            L('V2', "À trois heures du matin, le voisin a répondu.", highlight=['trois']),
            L('V3', "Tape plus fort !", 'voisin'),
            L('V4', "Alors il a tapé plus fort et le plafond est tombé.", highlight=['plafond', 'tombé.'])],
  'actors': [act('mec', [0.4, 0, -0.9], 10, 'pokeUp', 'angry', keys=[
                 k('V2', clip='stand', expr='unimpressed'), k('V4', clip='pokeUp', expr='angry', params={'freq': 4.2}),
                 k('V4:plafond+0.1', to=[0.4, 0, 0.8], glide=True, dur=0.3, clip='startle', then='stand', face='keep', expr='shocked')]),
             *[act(i, [x, UP, z], ry, 'dance', 'grin',
                   keys=([k('V2:voisin', clip='lookDown', expr='smug'), k('V3', clip='yell', expr='angry'), k('V4', clip='dance', expr='grin')] if i == 'voisin' else []) +
                        [k(fall, to=[x, DOWN, z], glide=True, dur=0.35, ease='in', clip='startle', then='dance', face='keep')])
               for i, (x, z), ry in PARTY]],
  'props': [P('dalle', 'floorSlab', pos=SLAB_C, opts={'w': 5.4, 'd': 3.4, 'lampX': -1.4, 'swing': 0.18, 'shakeAt': ['V4:tapé', 'V4:plafond']}, keys=[k(fall, to=SLAB_DOWN, dur=0.35, ease='in')]),
            P('murHaut', 'signBoard', pos=[0, 0, -3.45], opts={'text': ' ', 'bg': '#5A3A7A', 'fg': '#5A3A7A', 'w': 5.6, 'h': 2.5, 'height': UP, 'posts': False, 'frame': '#3A2A4A'}),
            P('canape', 'sofaProp', pos=[-1.0, UP, -3.05], opts={'color': '#B5302A', 'color2': '#D9534A'}, keys=[k(fall, to=[-1.0, DOWN, -3.05], dur=0.35, ease='in')]),
            P('radio', 'boombox', pos=[1.9, UP, -3.2], opts={'playAt': 0}, keys=[k(fall, to=[1.9, DOWN, -3.2], dur=0.35, ease='in')]),
            P('balai', 'broom', on=BROOM_UP),
            P('chevet', 'table', pos=[-2.3, 0, -0.6], opts={'w': 0.5, 'd': 0.4, 'h': 0.55, 'color': '#C9A06A'}),
            P('reveil', 'alarmClock', scale=0.55, pos=[-2.3, 0.55, -0.6], ry=15, opts={'time': '03:00'}),
            P('poussiere', 'dustPuff', scale=2.6, visible=False, pos=[0.3, 0.3, -0.5], opts={'color': '#CFC6B4', 'once': True, 'period': 1.0, 'startAt': fall + '+0.35'},
              keys=[k(fall + '+0.3', visible=True)])],
  'sfx': [music(fall + '+0.4'), {'at': 'V1:plafond', 'name': 'thud', 'vol': 0.5}, {'at': 'V1:balai', 'name': 'thud', 'vol': 0.5}, {'at': 'V1:voisin', 'name': 'thud', 'vol': 0.5},
          {'at': 'V4:tapé', 'name': 'thud', 'vol': 0.7}, {'at': 'V4:plus', 'name': 'thud', 'vol': 0.7}, {'at': 'V4:plafond', 'name': 'glass', 'vol': 0.4},
          {'at': fall + '+0.35', 'name': 'thud', 'vol': 1.0}, {'at': fall + '+0.38', 'name': 'poof', 'vol': 0.6}],
  'cams': [WIDE(0),
           POV('V1:balai', [1.5, 1.75, 0.9], [0.45, 2.55, -0.9], 52),
           cam('V1:musique', 'voisin', 'ms', angle=0),
           POV('V2', [-1.6, 0.95, 0.4], [-2.3, 0.75, -0.6], 36),
           cam('V2:voisin', 'voisin', 'ms', angle=0),
           cam('V3', 'voisin', 'cu', angle=0),
           WIDE('V4')],
  'tail': 0.2,
})
FETE_POS = [(-2.0, -1.0), (0.2, -2.4), (1.8, -1.6), (0.9, -0.7)]
scenes.append({
  'id': 'fete', 'set': 'livingRoom', 'setOpts': {'sofa': False, 'tv': False}, 'lighting': 'night', 'ambience': None,
  'crowd': [{'id': 'foule', 'count': 6, 'spec': {'preset': 'lemec_charcoal', 'seed': 61}, 'clip': 'dance', 'ry': 0,
             'positions': [[-2.6, 0, 0.6], [2.4, 0, 0.4], [-1.4, 0, 1.5], [1.4, 0, 1.6], [2.9, 0, -0.7], [-3.0, 0, -0.9]]}],
  'lines': [L('V5', "Le voisin aussi, avec son canapé et quarante invités.", highlight=['quarante', 'invités.']),
            L('V6', "La fête a continué chez lui.", highlight=['fête'])],
  'actors': [act('mec', [0.1, 0, 0.75], 0, 'stand', 'unimpressed'),
             act('voisin', [-1.0, DOWN + 0.22, -2.95], 0, 'sitSip', 'grin'),
             *[act(i, [x, DOWN, z], 0, 'dance', 'grin') for (i, _, _), (x, z) in zip(GUESTS, FETE_POS)]],
  'props': [P('dalle', 'floorSlab', pos=SLAB_DOWN, opts={'w': 5.4, 'd': 3.4, 'lamp': False}),
            P('murHaut', 'signBoard', pos=[0, 0, -3.45], opts={'text': ' ', 'bg': '#5A3A7A', 'fg': '#5A3A7A', 'w': 5.6, 'h': 2.5, 'height': UP, 'posts': False, 'frame': '#3A2A4A'}),
            P('canape', 'sofaProp', pos=[-1.0, DOWN, -3.05], opts={'color': '#B5302A', 'color2': '#D9534A'}),
            P('radio', 'boombox', pos=[1.9, DOWN, -3.2], opts={'playAt': 0}),
            P('verre', 'beerGlass', on={'actor': 'voisin', 'hand': 'R'}),
            P('balai', 'broom', on={'actor': 'mec', 'hand': 'R', 'rot': [3.1416, 0, 0]}),
            P('poussiere', 'dustPuff', scale=2.6, pos=[0.3, 0.3, -0.5], opts={'color': '#CFC6B4', 'once': True, 'period': 1.2, 'startAt': -0.6})],
  'sfx': [music('V6.end+0.2', 0.5), {'at': 'V5:quarante', 'name': 'tada', 'vol': 0.35}],
  'cams': [cam(0, 'voisin', 'ms', angle=0),
           POV('V5:quarante', [0.4, 2.3, 6.0], [0.2, 1.0, -1.0], 52),
           cam('V6:chez', 'mec', 'cu', angle=0, move='push', amount=0.04)],
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('V7', "Alors ce con a porté plainte pour tapage nocturne.", highlight=['plainte', 'tapage']),
            L('V8', "Le juge a donné raison au voisin. Le plafond lui appartenait, et tout ce qu'il y avait dessous.", highlight=['raison', 'dessous.'])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('V8:raison', clip='sitPoint', expr='neutral')]),
             act('mec', [-0.8, 0, -1.7], 180, 'stand', 'angry', keys=[k('V7:plainte', face=90, turn=0.25, clip='point'), k('V8', face=180, turn=0.25, clip='stand'), k('V8:dessous', clip='startle', expr='shocked')]),
             act('voisin', [0.8, 0, -1.7], 180, 'armsCrossed', 'smug', keys=[k('V8:dessous', clip='celebrate', expr='grin')])],
  'props': [P('balai', 'broom', on={'actor': 'mec', 'hand': 'L', 'rot': [3.1416, 0, 0]})],
  'sfx': [{'at': 'V8:raison', 'name': 'gavel', 'vol': 0.6}, {'at': 'V8:dessous', 'name': 'gavel', 'vol': 0.6}],
  'cams': [cam(0, ['juge', 'mec', 'voisin'], 'fs', worldAngle=0, elev=6),
           cam('V7:plainte', 'mec', 'mcu', angle=-30),
           cam('V8', 'juge', 'mcu', angle=0),
           cam('V8:appartenait', 'voisin', 'ms', worldAngle=180, noOcclusion=True),
           cam('V8:dessous', 'mec', 'cu', worldAngle=180, noOcclusion=True)],
  'tail': 0.2,
})
scenes.append({
  'id': 'cave', 'set': 'cave', 'ambience': None,
  'lines': [L('V9', "Putain, depuis, ce mec dort à la cave.", highlight=['cave.']),
            L('V10', "Il tape au plafond avec un balai.", highlight=['balai.'])],
  'actors': [act('mec', [-1.5, 0.2, -1.65], 0, 'lieBack', 'unimpressed', keys=[
                 k('V10', to=[-0.3, 0, -1.0], glide=True, dur=0.05, face=10, clip='pokeUp', then='pokeUp', expr='angry')])],
  'props': [P('balai', 'broom', opts={'grip': 1.3}, on=BROOM_UP)],
  'sfx': [music('V10.end+1.4', 0.16), {'at': 'V10:tape', 'name': 'thud', 'vol': 0.6}, {'at': 'V10:tape+0.42', 'name': 'thud', 'vol': 0.6},
          {'at': 'V10:tape+0.84', 'name': 'thud', 'vol': 0.6}, {'at': 'V10:tape+1.26', 'name': 'thud', 'vol': 0.6}, {'at': 'V10:tape+1.68', 'name': 'thud', 'vol': 0.6},
          {'at': 'V10:tape+2.1', 'name': 'thud', 'vol': 0.6}, {'at': 'V10:tape+2.52', 'name': 'thud', 'vol': 0.6}],
  'cams': [POV(0, [1.6, 1.55, 2.4], [-0.9, 0.6, -1.6], 55),
           POV('V9:cave', [-1.45, 1.6, -2.05], [-1.5, 0.4, -2.35], 50),
           POV('V10', [0.9, 1.3, 2.2], [-0.3, 1.45, -1.0], 55)],
  'tail': 1.4,
})

write('voisin', 'Le voisin du dessus', scenes, {
  'mec': {'preset': 'mecPyjama'}, 'voisin': {'preset': 'lemec_brown', 'glasses': True, 'seed': 8},
  'g1': {'preset': 'lemec_charcoal', 'seed': 3}, 'g2': {'preset': 'femme', 'seed': 22}, 'g3': {'preset': 'lemec_beige', 'seed': 5}, 'g4': {'preset': 'madame', 'seed': 7},
  'juge': {'preset': 'judge'}})
