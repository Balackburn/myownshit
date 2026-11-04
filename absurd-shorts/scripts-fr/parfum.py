#!/usr/bin/env python3
"""LE PARFUM. Ce mec empties a whole bottle of perfume for his first date -> a bee follows him, then the whole swarm ->
they elect him queen -> ce con calls the fire brigade -> they send a beekeeper -> too late: he is already laying eggs,
forty a day -> the girl married the beekeeper -> they sell his honey at the market. (Classic formula.)"""
from actu_common import *

SINK = [3.2, 0, -2.15]
MIRROR = lambda at, y=1.62: POV(at, [3.2, 1.7, -3.3], [3.2, y, -2.15], 72)
CROWN = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.56, 0]}
BEES0 = [[-0.6, 1.5, 0.2], [0.5, 1.9, -0.3], [-0.3, 2.2, 0.5], [0.7, 1.4, 0.6], [-0.8, 2.0, -0.4], [0.2, 2.4, 0.1]]
def bee_actors(start, end, at, dur, vis=True):
    out = []
    for i, (dx, y, dz) in enumerate(BEES0):
        ks = [k((at + i * 0.12) if isinstance(at, (int, float)) else f'{at}+{i * 0.12:.2f}', to=[end[0] + dx, y, end[2] + dz], glide=True, dur=dur, clip='fly', then='fly')] if end else []
        out.append(act(f'b{i}', [start[0] + dx, y, start[2] + dz], 90, 'fly', 'happy', scale=0.2, keys=ks))
    return out
scenes = []
scenes.append({
  'id': 'bain', 'set': 'bathroom', 'ambience': None,
  'lines': [L('F1', "Ce mec a mis du parfum pour son premier rendez-vous.", highlight=['parfum', 'rendez-vous.']),
            L('F2', "Toute la bouteille.", highlight=['bouteille.'])],
  'actors': [act('mec', SINK, 180, 'stand', 'happy', keys=[k('F1:parfum', clip='phoneCall', expr='smug'), k('F2', clip='wired', expr='happy')])],
  'props': [P('flacon', 'perfume', scale=1.6, on={'actor': 'mec', 'hand': 'R'}),
            P('nuage', 'dustPuff', scale=0.2, visible=False, pos=[3.2, 1.3, -2.05], opts={'color': '#F2B8D0'}, keys=[k('F2', visible=True), k('F2', scale=2.6, dur=1.4, ease='out')])],
  'sfx': [{'at': 'F1:parfum', 'name': 'poof', 'vol': 0.35}, {'at': 'F2', 'name': 'poof', 'vol': 0.4}, {'at': 'F2+0.3', 'name': 'poof', 'vol': 0.4}, {'at': 'F2+0.6', 'name': 'poof', 'vol': 0.4}],
  'cams': [MIRROR(0), POV('F2', [5.3, 1.5, -1.0], [3.2, 1.3, -2.3], 58)],
  'tail': 0.2,
})
scenes.append({
  'id': 'rue', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('F3', "Une abeille l'a suivi. Puis l'essaim entier.", highlight=['abeille', 'essaim']),
            L('F4', "Elles l'ont élu reine.", highlight=['reine.']),
            L('F5', "Alors ce con a appelé les pompiers.", highlight=['pompiers.']),
            L('F6', "Ils ont envoyé un apiculteur.", highlight=['apiculteur.'])],
  'actors': [act('mec', [-4.6, 0, 0.6], 90, 'idle', 'happy', keys=[k(0.05, to=[0.3, 0, 0.6], clip='walk', speed=1.7, faceEnd=0, then='stand'),
                                                                    k('F4', expr='shocked'), k('F5', clip='phoneCall', expr='angry')]),
             *bee_actors([-4.6, 0, 0.6], [0.3, 0, 0.6], 0.05, 2.9),
             act('apiculteur', [7.0, 0, 0.9], -90, 'idle', 'neutral', keys=[k('F6-0.4', to=[1.7, 0, 0.8], clip='walk', speed=3.0, faceEnd='mec', then='stand')])],
  'props': [P('couronne', 'crown', visible=False, on=CROWN, keys=[k('F4:reine', visible=True)]),
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('F5', visible=True)])],
  'sfx': [{'at': 0.2, 'name': 'squeak', 'vol': 0.25}, {'at': 'F3:essaim', 'name': 'squeak', 'vol': 0.35}, {'at': 'F4:reine', 'name': 'bell', 'vol': 0.6}, {'at': 'F6-0.4', 'name': 'siren', 'vol': 0.35}],
  'cams': [cam(0, 'mec', 'fs', angle=-70, move='track'),
           cam('F3:essaim', ['mec', 'b2', 'b4'], 'ms', worldAngle=10),
           cam('F4', 'mec', 'cu', angle=0),
           cam('F5', 'mec', 'cu', angle=-25),
           cam('F6', ['apiculteur', 'mec'], 'ms', worldAngle=15)],
  'tail': 0.2,
})
NEST = [0.0, 0, -1.4]
scenes.append({
  'id': 'nid', 'set': 'park', 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('F7', "Trop tard : il pondait déjà des œufs.", highlight=['œufs.']),
            L('F8', "Putain, quarante par jour.", highlight=['quarante'])],
  'actors': [act('mec', [NEST[0], 0.1, NEST[2] - 0.05], 0, 'sitFloor', 'smug', keys=[k('F8', expr='unimpressed')]),
             *bee_actors([0, 0, -1.4], None, 0, 0),
             act('apiculteur', [1.6, 0, -0.6], -60, 'stand', 'shocked', keys=[k('F8', clip='facepalm')])],
  'props': [P('nid', 'nest', scale=1.3, pos=NEST, opts={'max': 14, 'layAt': ['F7', 'F7:pondait', 'F7:œufs', 'F8', 'F8:quarante', 'F8:jour', 'F8.end+0.1']}),
            P('couronne', 'crown', on=CROWN)],
  'sfx': [{'at': 'F7:pondait', 'name': 'pop', 'vol': 0.5}, {'at': 'F7:œufs', 'name': 'pop', 'vol': 0.5}, {'at': 'F8', 'name': 'pop', 'vol': 0.5}, {'at': 'F8:quarante', 'name': 'pop', 'vol': 0.5}, {'at': 'F8:jour', 'name': 'pop', 'vol': 0.5}],
  'cams': [cam(0, ['mec', 'apiculteur'], 'ms', worldAngle=20),
           cam('F7:œufs', [[NEST[0], 0.3, NEST[2]]], 'cu', worldAngle=0, elev=35, noOcclusion=True),
           cam('F8', 'mec', 'cu', angle=0)],
  'tail': 0.2,
})
STALL = [0.0, 0, -1.6]
scenes.append({
  'id': 'marche', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.4,
  'lines': [L('F9', "La fille a épousé l'apiculteur.", highlight=['épousé']),
            L('F10', "Ils vendent son miel au marché.", highlight=['miel'])],
  'actors': [act('femme', [-0.45, 0, -2.2], 0, 'stand', 'happy'),
             act('apiculteur', [0.45, 0, -2.2], 0, 'armsCrossed', 'happy'),
             act('mec', [STALL[0] + 0.55, 0.78, STALL[2] + 0.05], 0, 'sitFloor', 'unimpressed'),
             *bee_actors([0.5, 0.2, -1.6], None, 0, 0)],
  'props': [P('etal', 'table', pos=STALL, opts={'w': 1.6, 'd': 0.7, 'h': 0.78, 'color': '#C9A06A'}),
            P('parasol', 'parasol', pos=[-1.2, 0, -2.3], opts={'open': 1, 'colors': ['#F2C230', '#F6F1E3']}),
            P('enseigne', 'signBoard', pos=[0, 0, -2.75], opts={'text': 'GELÉE ROYALE', 'bg': '#F2C230', 'fg': '#5A3A1E', 'w': 1.6, 'h': 0.4, 'height': 1.85}),
            *[P(f'pot{i}', 'honeyJar', scale=1.2, pos=[-0.65 + i * 0.22, 0.78, -1.4 + (i % 2) * 0.08]) for i in range(5)],
            P('couronne', 'crown', on=CROWN)],
  'sfx': [{'at': 'F9', 'name': 'bell', 'vol': 0.4}, {'at': 'F10:miel', 'name': 'cash', 'vol': 0.5}],
  'cams': [cam(0, ['femme', 'apiculteur'], 'ms', worldAngle=0),
           cam('F10', ['mec', 'femme', 'apiculteur'], 'fs', worldAngle=0, elev=6),
           cam('F10:miel', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})
BEE = {'type': 'creature', 'name': 'bee', 'opts': {'seed': 3}}
write('parfum', 'Le parfum', scenes, {'apiculteur': {'preset': 'apiculteur'}, 'femme': {'preset': 'femme', 'seed': 21},
                                      **{f'b{i}': {**BEE, 'opts': {'seed': 3 + i}} for i in range(6)}})
