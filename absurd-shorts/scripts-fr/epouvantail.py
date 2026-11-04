#!/usr/bin/env python3
"""L'ÉPOUVANTAIL (viral-video-writing loop, score_fr.py 100/100). Hook with a number (200 crows) -> the villain at 5 s (the crows
hire a lawyer) -> the scarecrow says nothing, looks guilty -> two years (in a cell) -> the field and the barn eaten -> low point:
he stands in the field himself, all summer -> the crows nest in his hat -> callback: the lawyer too. The last image is the
first one (a scarecrow in a field)."""
import math
from actu_common import *

CROW = {'type': 'creature', 'name': 'pigeon', 'opts': {'color': '#26262C'}}
SCARE = [0.6, 0, -1.6]
def crows(n, spots, clip='idle', vis=True, keys_for=None):
    return [act(f'c{i}', p, ry, clip, 'angry', scale=0.9, visible=vis, keys=(keys_for(i) if keys_for else [])) for i, (p, ry) in enumerate(spots[:n])]
FENCE_SPOTS = [([-2.2 + i * 0.75, 0.85, -4.0], 10 + i * 7) for i in range(7)]
GROUND = [([-1.6, 0, -0.6], 30), ([1.9, 0, -0.9], -40), ([-0.4, 0, 0.3], 10), ([2.6, 0, -2.4], -20), ([-2.5, 0, -1.8], 60), ([1.0, 0, 0.6], 0)]
HAT = {'actor': 'mecE', 'joint': 'head', 'offset': [0, 0.62, 0]}
scenes = []
scenes.append({
  'id': 'champ', 'set': 'farm', 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('EP1', "Ce mec a planté un épouvantail dans son champ pour faire peur à deux cents corbeaux.", highlight=['épouvantail', 'deux', 'cents']),
            L('EP2', "Les corbeaux ont pris un avocat. Pour harcèlement moral.", highlight=['avocat.', 'harcèlement'])],
  'actors': [act('mec', [-0.4, 0, -1.2], 20, 'handsOnHips', 'smug', keys=[k('EP2', expr='shocked')]),
             *crows(7, FENCE_SPOTS),
             act('avocat', [3.5, 0, -0.4], -90, 'idle', 'smug', scale=1.0, visible=False, keys=[k('EP2-0.2', visible=True), k('EP2-0.2', to=[1.4, 0, -0.5], clip='walk', speed=1.5, faceEnd=-60, then='idle')])],
  'props': [P('epouvantail', 'scarecrow', pos=SCARE),
            P('mallette', 'briefcase', scale=0.45, visible=False, on={'actor': 'avocat', 'offset': [0.12, 0.08, 0.05]}, keys=[k('EP2-0.2', visible=True)])],
  'sfx': [{'at': 0.3, 'name': 'cluck', 'vol': 0.25}, {'at': 'EP1:corbeaux', 'name': 'cluck', 'vol': 0.3}, {'at': 'EP2:avocat', 'name': 'sting', 'vol': 0.3}],
  'cams': [cam(0, ['mec', 'epouvantail'], 'ms', worldAngle=15, withProps=True),
           cam('EP1:deux', ['c1', 'c3', 'c5'], 'ms', worldAngle=5),
           cam('EP2', 'avocat', 'cu', angle=0, noOcclusion=True)],
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('EP3', "Au tribunal, l'épouvantail n'a rien dit. Il avait l'air coupable.", highlight=['rien', 'coupable.'])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('EP3:coupable', clip='sitPoint', expr='angry')]),
             act('avocat', [-0.9, 0.79, -1.9], 180, 'idle', 'smug', scale=1.0)],
  'props': [P('epouvantail', 'scarecrow', pos=[0.9, 0, -1.8], ry=180), P('table', 'table', pos=[-0.9, 0, -1.9], opts={'w': 0.9, 'd': 0.6, 'h': 0.79})],
  'sfx': [{'at': 'EP3:rien', 'name': 'crickets', 'vol': 0.5}],
  'cams': [cam(0, ['juge', 'epouvantail'], 'fs', worldAngle=0, elev=6, withProps=True),
           POV('EP3:dit', [0.9, 1.8, -3.05], [0.9, 1.72, -1.8], 40)],
  'tail': 0.15,
})
scenes.append({
  'id': 'prison', 'set': 'prisonCell', 'ambience': None,
  'lines': [L('EP4', "Deux ans ferme.", highlight=['Deux', 'ferme.'])],
  'actors': [],
  'props': [P('epouvantail', 'scarecrow', pos=[0.0, 0, 1.4], ry=0)],
  'sfx': [{'at': 'EP4', 'name': 'gavel', 'vol': 0.6}, {'at': 'EP4:ferme', 'name': 'cuff', 'vol': 0.5}],
  'cams': [POV(0, [0.3, 1.5, 4.6], [0.0, 1.2, 1.4], 48)],
  'tail': 0.2,
})
scenes.append({
  'id': 'champ2', 'set': 'farm', 'ambience': 'park', 'ambienceVol': 0.5,
  'daynight': {'from': 'EP7', 'period': 0.6},
  'lines': [L('EP5', "Sans épouvantail, les corbeaux ont mangé tout le champ. Puis la grange.", highlight=['mangé', 'grange.']),
            L('EP6', "Alors ce con s'est planté lui-même au milieu du champ.", highlight=['lui-même']),
            L('EP7', "Les bras en croix et un chapeau de paille, pendant tout l'été.", highlight=['croix', "l'été."]),
            L('EP8', "Les corbeaux se sont posés sur lui.", highlight=['lui.']),
            L('EP9', "Putain, ils ont fait leur nid dans son chapeau.", highlight=['nid', 'chapeau.']),
            L('EP10', "L'avocat aussi.", highlight=["L'avocat"])],
  'actors': [act('mecE', SCARE, 0, 'scarecrowPose', 'unimpressed', visible=False, keys=[k('EP6', visible=True)]),
             act('mec', [-1.5, 0, 0.2], 30, 'stand', 'shocked', keys=[k('EP6', visible=False)]),
             *crows(6, GROUND, clip='walk', keys_for=lambda i: [k('EP8', to=[[-0.75, 1.42, -1.6], [1.95, 1.42, -1.6], [-0.5, 1.45, -1.6], [1.7, 1.45, -1.6], [0.95, 1.5, -1.6], [0.25, 1.5, -1.6]][i],
                                                                glide=True, dur=0.5 + i * 0.08, clip='fly', then='idle', face=0)]),
             act('avocat', [3.6, 2.4, -0.8], -90, 'fly', 'smug', visible=False, keys=[k('EP10', visible=True), k('EP10', to=[0.6, 2.42, -1.6], glide=True, dur=0.45, clip='fly', then='idle', face=0)])],
  'props': [P('ble', 'tallGrass', pos=[0.4, 0, -2.4], opts={'w': 9, 'd': 4, 'h': 0.55, 'count': 360}, keys=[k('EP5:mangé', scale=0.04, dur=0.9, ease='in')]),
            P('nid', 'nest', scale=0.55, visible=False, opts={'max': 5, 'layAt': ['EP9:nid', 'EP9:chapeau', 'EP10']}, on={**HAT, 'offset': [0, 0.66, 0]}, keys=[k('EP9:nid', visible=True)]),
            P('mallette', 'briefcase', scale=0.45, visible=False, on={'actor': 'avocat', 'offset': [0.12, 0.08, 0.05]}, keys=[k('EP10', visible=True)])],
  'sfx': [{'at': 'EP5', 'name': 'cluck', 'vol': 0.4}, {'at': 'EP5:mangé', 'name': 'poof', 'vol': 0.4}, {'at': 'EP8', 'name': 'cluck', 'vol': 0.4}, {'at': 'EP9:nid', 'name': 'pop', 'vol': 0.4},
          {'at': 'EP10', 'name': 'whoosh', 'vol': 0.4}],
  'cams': [POV(0, [1.0, 2.2, 4.8], [0.4, 0.6, -2.4], 50),
           cam('EP6', 'mecE', 'fs', worldAngle=10),
           cam('EP8', 'mecE', 'ms', worldAngle=10),
           cam('EP9', 'mecE', 'mcu', worldAngle=5),
           cam('EP10', 'mecE', 'ms', worldAngle=10, move='push', amount=0.04)],
  'tail': 1.4,
})
write('epouvantail', "L'épouvantail", scenes, {**{f'c{i}': CROW for i in range(7)}, 'avocat': CROW, 'juge': {'preset': 'judge'},
                                              'mecE': {'preset': 'lemec', 'hat': 'cowboy', 'hatColor': '#E6C46A'}})
