#!/usr/bin/env python3
"""ACTU 01 — LE PIGEON. A pigeon steals his croissant -> he calls the cops (motif: pigeon trop confiant) -> the pigeon
in custody under the lamp ("Rou." = a confession) -> a Japanese post about it, machine-translated, nobody laughs except
the translator (a robot) who resigns -> trial: the pigeon has a pigeon lawyer, the man gets six months -> the pigeon
eats croissants at his cell window."""
from actu_common import *

scenes = []
BENCH = [0, 0.11, -2.3]
scenes.append({
  'id': 'parc', 'set': 'park', 'ambience': 'park',
  'lines': [L('P1', "Tous les matins, un pigeon volait le croissant de ce mec.", highlight=['pigeon', 'croissant']),
            L('P2', "Il a appelé les flics. Motif : vol avec violence, en récidive.", highlight=['Motif', 'récidive.']),
            L('P3', "Les flics sont arrivés en trois secondes.", highlight=['trois', 'secondes.'])],
  'actors': [
    act('mec', BENCH, 0, 'sitShow', 'happy', keys=[
        k('P1:croissant', expr='shocked', clip='sit'),
        k('P1:croissant+0.35', to=[0.25, 0, -1.6], glide=True, dur=0.22, clip='startle', then='startle', face='keep'),
        k('P2', clip='phoneCall', expr='angry', face=-25, turn=0.2),
        k('P3', clip='point', expr='smug', face='pigeon', turn=0.2)]),
    act('pigeon', [4.2, 2.4, -1.0], -90, 'fly', 'neutral', scale=1.8, keys=[
        k(0.25, to=[0.5, 1.02, -1.72], glide=True, dur=1.0, clip='fly', then='fly'),
        k('P1:croissant+0.12', to=[-1.8, 0, -0.7], glide=True, dur=0.75, arc=0.5, clip='fly', then='eat', expr='smug'),
        k('P3:secondes', clip='angry', expr='scared', face='flic1', turn=0.15)]),
    act('flic1', [-7.0, 0, 0.8], 90, 'idle', 'angry', keys=[
        k('P3', path=[[-4.5, 0, 0.6], [-2.75, 0, -0.3]], clip='run', speed=4.2, faceEnd='pigeon', then='point')]),
    act('flic2', [-7.6, 0, 1.6], 90, 'idle', 'angry', keys=[
        k('P3+0.1', path=[[-3.6, 0, 1.3], [-1.05, 0, 0.05]], clip='run', speed=4.4, faceEnd='pigeon', then='cuffOther')]),
  ],
  'props': [P('croissant', 'croissant', scale=1.6, on={'actor': 'mec', 'hand': 'R'},
              keys=[k('P1:croissant', attach='pigeon', joint='head', offset=[0, 0.02, 0.1]), k('P1:croissant+0.85', detach=True, fall=True)]),
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('P2', visible=True)])],
  'sfx': [{'at': 'P1:croissant', 'name': 'whoosh', 'vol': 0.5}, {'at': 'P3-0.25', 'name': 'siren', 'vol': 0.5}],
  'cams': [cam(0, ['mec', 'pigeon'], 'fs', worldAngle=20, elev=6),
           cam('P1:volait', ['mec', 'pigeon'], 'ms', worldAngle=30),
           cam('P1:croissant+0.25', 'pigeon', 'fs', angle=50, move='track'),
           cam('P2', 'mec', 'cu', angle=-35),
           cam('P2:Motif', 'pigeon', 'cu', angle=10),
           cam('P3', ['flic1', 'flic2', 'pigeon'], 'fs', worldAngle=10, elev=8),
           cam('P3:secondes', 'pigeon', 'cu', angle=-20)],
  'tail': 0.3,
})

scenes.append({
  'id': 'gav', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('P4', "Garde à vue pour le pigeon.", highlight=['Garde', 'vue']),
            L('P5', "Où étiez-vous ce matin à huit heures ?", 'commissaire'),
            L('P6', "Rou.", 'pigeon', pre=0.25),
            L('P7', "Il avoue.", 'commissaire', pre=0.2, highlight=['avoue.'])],
  'actors': [
    act('pigeon', IR_ON_TABLE, 0, 'idle', 'smug', scale=1.8, keys=[k('P6', clip='talk', expr='neutral'), k('P7', clip='idle', expr='scared')]),
    act('commissaire', IR_COP, -90, 'leanTable', 'suspicious', keys=[k('P5', clip='leanTable', expr='angry'), k('P7', clip='slamTable', expr='smug', sfx='thud', sfxAt=0.12)]),
    act('flic2', IR_COP2, 115, 'armsCrossed', 'unimpressed'),
  ],
  'props': [P('preuve', 'evidenceBag', pos=[-0.5, 0.785, -0.7])],
  'cams': [cam(0, ['commissaire', 'pigeon'], 'fs', worldAngle=10, elev=10),
           cam('P5', ots=['commissaire', 'pigeon', -1]),
           cam('P6', 'pigeon', 'cu', angle=0, elev=5),
           cam('P7', 'commissaire', 'mcu', angle=-25)],
  'tail': 0.2,
})

TW = (0.05, 0.785, -0.42)
scenes.append({
  'id': 'tweet', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('P8', "Au Japon, un mec a tweeté une blague sur l'affaire.", highlight=['Japon,', 'blague']),
            L('P9', "Personne n'a ri. Sauf le traducteur, qui a démissionné.", highlight=['traducteur,', 'démissionné.'])],
  'actors': [
    act('pigeon', IR_ON_TABLE, 0, 'eat', 'smug', scale=1.8),
    act('commissaire', IR_COP, -90, 'lookDown', 'neutral', keys=[k('P9', clip='stareCamera', expr='unimpressed', face=-30, turn=0.2)]),
    act('flic2', [-0.6, 0, -0.15], 160, 'lookDown', 'neutral', keys=[k('P9', clip='stareCamera', expr='unimpressed', face=10, turn=0.2)]),
    act('robot', [-3.3, 0, -2.4], 40, 'idle', 'neutral', keys=[
        k('P9:Sauf', clip='celebrate', expr='happy'),
        k('P9:démissionné', path=[[-1.5, 0, -2.25], [2.6, 0, -2.25], [4.2, 0, -1.25]], clip='walk', speed=1.6, expr='sad'),
        k('P9.end+0.9', visible=False)]),
  ],
  'props': [tweet_on_table('tw', *TW, name='Kenji', handle='@kenji_lol', text="Le pigeon français vole le croissant, puis il fait grève contre le pain.", likes='0 rire · 2 likes'),
            P('carton', 'cardboardBox', opts={'text': ''}, scale=0.6, visible=False, on={'actor': 'robot', 'joint': 'torso', 'offset': [0, 0.1, 0.3]}, keys=[k('P9:démissionné', visible=True)])],
  'sfx': [{'at': 'P9', 'name': 'crickets', 'vol': 0.7}],
  'cams': [tweet_cam('P8:tweeté', *TW),
           cam('P9', ['commissaire', 'flic2'], 'ms', worldAngle=-15),
           cam('P9:Sauf', 'robot', 'ms', angle=15),
           cam('P9:démissionné+0.1', 'robot', 'fs', angle=70, move='track')],
  'tail': 0.3,
})

scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('P10', "Au procès, le pigeon avait pris un avocat. Un autre pigeon.", highlight=['avocat.', 'pigeon.']),
            L('P11', "Le pigeon est libre. Six mois pour vous : nourrissage illégal.", 'juge', highlight=['Six', 'mois'])],
  'actors': [
    act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('P11', clip='sitPoint', expr='angry')]),
    act('pigeon', [-3.55, 0.76, 1.0], 180, 'idle', 'smug', scale=1.8, keys=[k('P11:libre', clip='celebrate', expr='happy')]),
    act('pigeon2', [-3.0, 0.76, 1.0], 180, 'idle', 'neutral', scale=1.8, keys=[k('P10:pigeon', clip='talk'), k('P11', clip='idle')]),
    act('mec', [3.3, 0, 1.8], 180, 'stand', 'neutral', keys=[k('P11:Six', expr='shocked', clip='scared')]),
  ],
  'sfx': [{'at': 'P11:libre', 'name': 'gavel', 'vol': 0.6}, {'at': 'P11:illégal', 'name': 'gavel', 'vol': 0.6}],
  'cams': [cam(0, 'juge', 'ms', worldAngle=0, elev=6),
           cam('P10:avocat', ['pigeon', 'pigeon2'], 'ms', worldAngle=180, allowBack=True),
           cam('P11', 'juge', 'mcu', angle=0),
           cam('P11:Six', 'mec', 'cu', worldAngle=180, allowBack=True)],
  'tail': 0.3,
})

scenes.append({
  'id': 'cellule', 'set': 'prisonCell', 'ambience': None,
  'lines': [L('P12', "Depuis, le pigeon vient manger son croissant devant sa cellule.", highlight=['croissant'])],
  'actors': [
    act('mec', [0.45, 0, -2.25], -25, 'stand', 'sad', keys=[k(0, look='pigeon'), k('P12:croissant', clip='stareCamera', expr='unimpressed', look=None)]),
    act('pigeon', [-0.6, 1.92, -2.86], 30, 'eat', 'smug', scale=1.8),
  ],
  'props': [P('croissant', 'croissant', scale=1.6, pos=[-0.42, 1.92, -2.8])],
  'cams': [cam(0, ['mec', 'pigeon'], 'ms', worldAngle=10, elev=4),
           cam('P12:manger', 'pigeon', 'cu', angle=0),
           cam('P12.end-0.2', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu01_pigeon', 'Le pigeon', scenes, {
  'pigeon': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 2}},
  'pigeon2': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 7}},
  'robot': {'type': 'creature', 'name': 'robot', 'opts': {'seed': 3}},
  'juge': {'preset': 'judge'},
})
