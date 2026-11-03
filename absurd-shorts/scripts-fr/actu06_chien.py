#!/usr/bin/env python3
"""ACTU 06 — LE CHIEN. He forgot the dog's kibble -> the dog calls the cops (motif: séquestration et privation de
nourriture) -> the cops take him away; the dog runs the interrogation, a cop translates the barks -> he lost an aura
battle in the supermarket aisle -> 48 hours -> on TV Mbappé apologises in three languages, he apologises in dog ->
the dog accepts in exchange for a promotion -> the dog is now the inspector and he is the one being walked."""
from actu_common import *

scenes = []
BOWL = [-0.95, 0, -1.25]
scenes.append({
  'id': 'salon', 'set': 'livingRoom', 'ambience': None,
  'lines': [L('C1', "Ce mec a oublié d'acheter les croquettes de son chien.", highlight=['croquettes']),
            L('C2', "Le chien a appelé les flics. Motif : séquestration et privation de nourriture.", highlight=['Motif', 'séquestration']),
            L('C3', "Les flics ont embarqué ce mec.", highlight=['embarqué'])],
  'actors': [
    act('mec', [0.45, 0.17, -2.75], 20, 'sit', 'happy', keys=[
        k('C3', to=[0.6, 0, -2.2], glide=True, dur=0.25, clip='startle', then='startle', face='keep', expr='shocked'),
        k('C3:embarqué', clip='handcuffed', expr='sad')]),
    act('chien', [-0.55, 0, -1.45], 60, 'sit', 'sad', scale=1.3, keys=[
        k('C1:croquettes', clip='angry', expr='angry'),
        k('C2', clip='talk', expr='angry', face=0, turn=0.2),
        k('C2:Motif', clip='talk', expr='smug')]),
    act('flic1', [-3.2, 0, -1.2], 90, 'idle', 'angry', keys=[k('C3-0.35', path=[[-1.6, 0, -1.6], [0.1, 0, -2.0]], clip='run', speed=4.5, faceEnd='mec', then='cuffOther')]),
    act('flic2', [-3.6, 0, -0.4], 90, 'idle', 'angry', keys=[k('C3-0.3', path=[[-1.2, 0, -0.8], [1.25, 0, -1.85]], clip='run', speed=4.8, faceEnd='mec', then='point')]),
  ],
  'props': [P('bol', 'dogBowl', pos=BOWL),
            P('tel', 'phone911', scale=1.2, visible=False, on={'actor': 'chien', 'joint': 'head', 'offset': [0.12, 0.05, 0.1], 'rot': [0, 0, 0.4]}, keys=[k('C2', visible=True), k('C3', visible=False)]),
            P('cuffs', 'handcuffs', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('C3:embarqué', visible=True)])],
  'sfx': [{'at': 'C3-0.4', 'name': 'siren', 'vol': 0.45}, {'at': 'C3:embarqué', 'name': 'cuff', 'vol': 0.6}],
  'cams': [cam(0, ['mec', 'chien'], 'fs', worldAngle=10, elev=6),
           cam('C1:croquettes', [[BOWL[0], 0.1, BOWL[2]]], 'cu', worldAngle=10, elev=30, noOcclusion=True),
           cam('C1:chien', 'chien', 'cu', angle=0),
           cam('C2', 'chien', 'ms', angle=10),
           cam('C2:Motif', 'chien', 'cu', angle=-10),
           cam('C2:privation', 'mec', 'ms', angle=0),
           cam('C3:embarqué-0.3', ['mec', 'flic1', 'flic2'], 'ms', worldAngle=10, elev=6)],
  'tail': 0.2,
})

DOG_T = [0.5, 0.785, -0.72]
scenes.append({
  'id': 'gav', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('C4', "C'est le chien qui menait l'interrogatoire.", highlight=['chien']),
            L('C5', "Wouf, wouf. Wouf !", 'chien'),
            L('C6', "Il demande où étaient les croquettes.", 'flic1'),
            L('C7', "Au supermarché. J'ai perdu une bataille d'aura au rayon.", 'mec', highlight=['bataille', "d'aura"]),
            L('C8', "Wouf.", 'chien', pre=0.2),
            L('C9', "Quarante-huit heures.", 'flic1', highlight=['Quarante-huit'])],
  'actors': [
    act('mec', IR_SUSPECT, 0, 'sitCuffed', 'sad', keys=[k('C7', expr='sad'), k('C9', expr='shocked')]),
    act('chien', DOG_T, -140, 'sit', 'angry', scale=1.3, keys=[k('C5', clip='talk', expr='angry', face=15, turn=0.15), k('C6', clip='sit', face=-140, turn=0.2), k('C8', clip='talk', expr='smug', face=15, turn=0.15), k('C9', clip='sit')]),
    act('flic1', IR_COP, -90, 'armsCrossed', 'neutral', keys=[k('C6', clip='point', expr='neutral'), k('C9', clip='armsCrossed', expr='unimpressed')]),
  ],
  'props': [P('cap', 'copCap', scale=1.1, on={'actor': 'chien', 'joint': 'head', 'offset': [0, 0.32, 0.02]})],
  'cams': [cam(0, ['chien', 'mec'], 'fs', worldAngle=10, elev=10),
           cam('C5', 'chien', 'cu', angle=0),
           cam('C6', 'flic1', 'mcu', angle=60),
           cam('C7', 'mec', 'cu', angle=0),
           cam('C8', 'chien', 'cu', angle=10),
           cam('C9', ['chien', 'flic1'], 'ms', worldAngle=20)],
  'tail': 0.2,
})

scenes.append({
  'id': 'tele', 'set': 'pressRoom', 'setOpts': {'backdrop': 'PARDON|SORRY|LO SIENTO|SCUSATE|ENTSCHULDIGUNG|DESCULPA|EXCUSES'}, 'ambience': 'station',
  'crowd': [journalists()],
  'lines': [L('C10', "À la télé, Mbappé s'excusait en trois langues.", highlight=['trois', 'langues.'])],
  'actors': [act('mbappe', PR_SPEAKER, 0, 'podiumTalk', 'sad', keys=[k('C10:excusait', clip='bowRepeat', params={'freq': 1.6})])],
  'sfx': [{'at': 'C10', 'name': 'shutter', 'vol': 0.5}],
  'cams': [cam(0, 'mbappe', 'ms', angle=0), cam('C10:trois', 'mbappe', 'mcu', angle=15)],
  'tail': 0.1,
})

scenes.append({
  'id': 'excuses', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('C11', "Ce mec s'est excusé en chien.", highlight=['chien.']),
            L('C12', "Wouf. Wouf, wouf.", 'mec'),
            L('C13', "Le chien a accepté. Contre une promotion.", highlight=['promotion.'])],
  'actors': [
    act('mec', [-0.2, 0, -0.1], 60, 'bowRepeat', 'sad', keys=[k('C12', clip='bowRepeat', params={'freq': 2.0}, expr='sad'), k('C13', clip='stand', expr='unimpressed')]),
    act('chien', DOG_T, -100, 'sit', 'smug', scale=1.3, keys=[k('C13', clip='celebrate', expr='happy')]),
  ],
  'props': [P('cap', 'copCap', scale=1.1, on={'actor': 'chien', 'joint': 'head', 'offset': [0, 0.32, 0.02]})],
  'cams': [cam(0, ['mec', 'chien'], 'ms', worldAngle=0),
           cam('C12', 'mec', 'ms', angle=20),
           cam('C13', 'chien', 'cu', angle=0)],
  'tail': 0.2,
})

scenes.append({
  'id': 'promenade', 'set': 'street', 'ambience': 'street',
  'lines': [L('C14', "Depuis, le chien est commissaire. Et c'est ce mec qu'on promène.", highlight=['commissaire.', 'promène.'])],
  'actors': [
    act('chien', [-4.4, 0, 0.9], 90, 'idle', 'smug', scale=1.3, keys=[k(0.05, to=[2.6, 0, 0.9], clip='walk', speed=1.3, then='sit')]),
    act('mec', [-5.75, 0, 0.9], 90, 'idle', 'sad', keys=[k(0.05, to=[1.25, 0, 0.9], clip='walk', speed=1.3, then='stareCamera')]),
    act('flic1', [0.6, 0, -0.7], 0, 'idle', 'neutral', keys=[k('C14:commissaire', clip='salute', face='chien', turn=0.2)]),
    act('flic2', [1.7, 0, -0.75], 0, 'idle', 'neutral', keys=[k('C14:commissaire+0.2', clip='salute', face='chien', turn=0.2)]),
  ],
  'props': [P('cap', 'copCap', scale=1.1, on={'actor': 'chien', 'joint': 'head', 'offset': [0, 0.32, 0.02]}),
            P('laisse', 'leash', opts={'length': 1.25, 'elev': 0.42}, on={'actor': 'chien', 'joint': 'head', 'offset': [0, 0.0, -0.05]})],
  'cams': [cam(0, 'mec', 'fs', angle=-70, move='track'),
           cam('C14:commissaire', ['chien', 'flic1', 'flic2'], 'fs', worldAngle=10, elev=6),
           cam('C14:promène', ['mec', 'chien'], 'ms', worldAngle=10, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu06_chien', 'Le chien', scenes, {
  'chien': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 4}},
  'mbappe': {'preset': 'footballeur'},
})
