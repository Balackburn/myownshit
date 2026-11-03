#!/usr/bin/env python3
"""ACTU 04 — LE PARASOL. His closed parasol has more charisma than him -> everyone takes selfies with it -> he calls
the cops (motif: vol de charisme) -> in custody the parasol says nothing ("Il avoue ou il réfléchit ?") -> released,
it runs against Glucksmann in a charisma debate and wins on points -> Glucksmann gets floured, no reaction ("Il est
même pas énervé ?" "Si. Ça se voit pas.") -> the parasol celebrates (it opens); he is its stand.
Satire of a public image only (the closed-parasol line is our own gag, not attributed)."""
from actu_common import *

scenes = []
PA = [0.5, 0, -1.8]
scenes.append({
  'id': 'plage', 'set': 'beach', 'ambience': 'park',
  'lines': [L('G1', "Ce mec a acheté un parasol. Même fermé, il avait plus de charisme que lui.", highlight=['fermé,', 'charisme']),
            L('G2', "Sur la plage, tout le monde faisait des selfies avec le parasol.", highlight=['selfies']),
            L('G3', "Il a appelé les flics. Motif : vol de charisme.", highlight=['Motif', 'charisme.'])],
  'actors': [
    act('mec', [-0.55, 0, -1.25], 15, 'present', 'happy', keys=[
        k('G1:fermé', clip='posing', expr='smug'),
        k('G1:charisme', clip='stand', expr='sad'),
        k('G2:selfies', path=[[-0.8, 0, -0.95]], clip='walk', speed=1.4, faceEnd=0, then='present', expr='happy'),
        k('G2.end-0.3', clip='bigShrug', expr='unimpressed'),
        k('G3', clip='phoneCall', expr='angry', face=-25, turn=0.2)]),
    act('touriste', [4.5, 0, 0.6], -100, 'idle', 'happy', keys=[
        k('G2', to=[1.3, 0, -1.15], clip='walk', speed=2.2, faceEnd=0, then='showPhone'),
        k('G2:selfies+0.4', clip='showPhone', expr='happy')]),
    act('madame', [5.2, 0, 1.4], -100, 'idle', 'happy', keys=[
        k('G2+0.15', to=[-0.2, 0, -1.3], clip='walk', speed=2.3, faceEnd=0, then='posing')]),
  ],
  'props': [P('parasol', 'parasol', pos=PA),
            P('tel', 'phone911', on={'actor': 'touriste', 'hand': 'R', **HAND_FLAT}, opts={'screen': 'tiktok'}),
            P('tel2', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('G3', visible=True)])],
  'sfx': [{'at': 'G2:selfies', 'name': 'shutter', 'vol': 0.5}, {'at': 'G2:selfies+0.5', 'name': 'shutter', 'vol': 0.5}],
  'cams': [cam(0, ['mec', 'parasol'], 'fs', worldAngle=10, elev=6),
           cam('G1:fermé', 'parasol', 'ms', worldAngle=-15),
           cam('G1:charisme', 'mec', 'cu', angle=10),
           cam('G2', ['touriste', 'madame', 'parasol'], 'fs', worldAngle=20, elev=6),
           cam('G2:selfies', ['touriste', 'madame', 'parasol', 'mec'], 'ms', worldAngle=0),
           cam('G3', 'mec', 'cu', angle=-35)],
  'tail': 0.2,
})

scenes.append({
  'id': 'gav', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('G4', "En garde à vue, le parasol n'a rien dit.", highlight=['rien']),
            L('G5', "Il avoue ou il réfléchit ?", 'flic1'),
            L('G6', "Avec un parasol, on sait jamais.", 'commissaire', highlight=['jamais.'])],
  'actors': [
    act('commissaire', IR_COP, -90, 'leanTable', 'suspicious', keys=[k('G6', clip='stand', expr='unimpressed', face=150, turn=0.2)]),
    act('flic1', IR_COP2, 115, 'armsCrossed', 'suspicious', keys=[k('G5', clip='scratchHead', expr='suspicious')]),
  ],
  'props': [P('parasol', 'parasol', pos=[0, 0, -1.45])],
  'cams': [cam(0, ['commissaire', [0, 1.4, -1.45]], 'fs', worldAngle=10, elev=10),
           cam('G4:rien', [[0, 1.6, -1.45]], 'ms', worldAngle=0, noOcclusion=True),
           cam('G5', 'flic1', 'mcu', angle=10),
           cam('G6', 'commissaire', 'mcu', angle=20)],
  'tail': 0.2,
})

DEBATE = {'backdrop': 'DÉBAT|PRIMAIRE|CHARISME', 'bg': '#D9E2E8', 'fg': '#2E4563'}
scenes.append({
  'id': 'debat', 'set': 'pressRoom', 'setOpts': DEBATE, 'ambience': 'station',
  'lines': [L('G7', "Relâché, le parasol s'est présenté contre Glucksmann. Débat de charisme.", highlight=['Glucksmann.', 'charisme.']),
            L('G8', "Le parasol a gagné aux points.", highlight=['gagné'])],
  'actors': [act('glucksmann', [-1.1, 0, -2.45], 10, 'podiumTalk', 'neutral', keys=[k('G8', clip='stand', expr='neutral')])],
  'props': [P('pod1', 'podium', pos=[-1.1, 0, -2.0]), P('pod2', 'podium', pos=[1.1, 0, -2.0]), P('parasol', 'parasol', pos=[1.1, 0, -2.45])],
  'sfx': [{'at': 'G8:points', 'name': 'tada', 'vol': 0.35}],
  'cams': [cam(0, ['glucksmann', [1.1, 1.4, -2.45]], 'ms', worldAngle=0, elev=6),
           cam('G7:Glucksmann', 'glucksmann', 'mcu', angle=-10),
           cam('G7:Débat', [[1.1, 1.6, -2.45]], 'ms', worldAngle=-10, noOcclusion=True),
           cam('G8', ['glucksmann', [1.1, 1.4, -2.45]], 'ms', worldAngle=0, elev=8, move='push', amount=0.06)],
  'tail': 0.2,
})

scenes.append({
  'id': 'farine', 'set': 'street', 'ambience': 'street',
  'lines': [L('G9', "Glucksmann s'est fait enfariner. Aucune réaction.", highlight=['enfariner.', 'Aucune']),
            L('G10', "Il est même pas énervé ?", 'mili1'),
            L('G11', "Si. Ça se voit pas.", 'mili2', highlight=['voit'])],
  'actors': [
    act('glucksmann', [-1.2, 0, 0.6], 90, 'idle', 'neutral', keys=[k(0.0, to=[0.2, 0, 0.6], clip='walk', speed=1.2, then='stand'), k('G9:enfariner', clip='stand', expr='neutral', face=0, turn=0.3)]),
    act('mili1', [1.6, 0, 1.2], -100, 'idle', 'angry', keys=[k('G9:fait', clip='giveItem', expr='angry'), k('G10', clip='stand', expr='surprised', face='mili2', turn=0.2)]),
    act('mili2', [2.2, 0, 0.5], -110, 'idle', 'neutral', keys=[k('G11', clip='talk', expr='unimpressed', face='mili1', turn=0.2)]),
  ],
  'props': [P('farine', 'flourBag', on={'actor': 'mili1', 'hand': 'R'}, keys=[k('G9:fait+0.25', detach=True, fall=True, toss=[-3.2, 1.2, -1.2])]),
            P('nuage', 'dustPuff', pos=[0.2, 1.6, 0.6], opts={'color': '#FFFFFF', 'once': True, 'period': 1.0}, scale=1.5, visible=False, keys=[k('G9:enfariner', visible=True)]),
            P('blanc', 'baldCap', opts={'color': '#F4F4F0', 'w': 0.24, 'd': 0.22}, scale=1.1, visible=False, on={'actor': 'glucksmann', 'joint': 'head', 'offset': [0, 0.58, 0]}, keys=[k('G9:enfariner+0.1', visible=True)])],
  'sfx': [{'at': 'G9:enfariner', 'name': 'poof', 'vol': 0.6}],
  'cams': [cam(0, ['glucksmann', 'mili1'], 'fs', worldAngle=20, elev=6),
           cam('G9:enfariner', 'glucksmann', 'ms', angle=0),
           cam('G9:Aucune', 'glucksmann', 'cu', angle=0),
           cam('G10', ['mili1', 'mili2'], 'ms', worldAngle=20),
           cam('G11:voit', 'glucksmann', 'ecu', angle=0)],
  'tail': 0.2,
})

scenes.append({
  'id': 'fete', 'set': 'pressRoom', 'setOpts': DEBATE, 'ambience': 'station',
  'crowd': [{**journalists(4), 'clip': 'celebrate', 'positions': [[-2.7, 0, 1.4], [-1.7, 0, 1.9], [1.7, 0, 1.9], [2.7, 0, 1.4]]}],
  'lines': [L('G12', "Le soir, le parasol a fêté sa victoire. Ce mec lui servait de pied.", highlight=['victoire.', 'pied.'])],
  'actors': [act('mec', [0, 0, -1.2], 0, 'holdSign', 'unimpressed', keys=[k('G12:pied', clip='holdSign', expr='sad')])],
  'props': [P('parasol', 'parasol', opts={'openAt': 'G12:fêté'}, on={'actor': 'mec', 'hand': 'R', 'offset': [0, 1.0, 0], 'rot': [3.1416, 0, 0]})],
  'sfx': [{'at': 'G12:fêté', 'name': 'whoosh', 'vol': 0.5}, {'at': 'G12:victoire', 'name': 'tada', 'vol': 0.4}],
  'cams': [cam(0, ['mec', 'parasol'], 'fs', worldAngle=0, elev=6, withProps=True),
           cam('G12:victoire', ['mec', 'parasol'], 'fs', worldAngle=20, elev=10, withProps=True),
           cam('G12:pied', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu04_parasol', 'Le parasol', scenes, {
  'touriste': {'preset': 'tourist'}, 'madame': {'preset': 'madame', 'seed': 9},
  'glucksmann': {'preset': 'politique'},
  'mili1': {'preset': 'lyceen', 'suit': '#C23A2E', 'build': {'height': 1.0}, 'seed': 21}, 'mili2': {'preset': 'lyceenne', 'build': {'height': 0.98}, 'seed': 22},
})
