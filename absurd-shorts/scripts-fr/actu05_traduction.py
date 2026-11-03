#!/usr/bin/env python3
"""ACTU 05 — LA TRADUCTION. He posts sushi with sauce algérienne -> a Japanese reply, machine-translated: "your sauce
insulted my grandfather the rice" -> he calls the cops (motif: grand-père insulté par une sauce) -> the cops question
his phone, the translation answers for it and confesses to eating the Eiffel Tower -> ten years -> a great Japanese
chef tastes the sauce and wants to marry it -> Franco-Japanese peace treaty: France returns Luffy's flag, Japan keeps
the sauce -> he stays in prison: nobody translated his release.
The joke is on the machine translation, never on Japanese people (gag bank rule)."""
from actu_common import *

scenes = []
CT = (-0.55, 0.95, -3.25)   # kitchen counter top, in front of the cabinets
scenes.append({
  'id': 'cuisine', 'set': 'kitchenNight', 'lighting': 'interior', 'ambience': None,
  'lines': [L('T1', "Ce mec a posté une photo : sushis, sauce algérienne.", highlight=['sushis,', 'algérienne.']),
            L('T2', "Un Japonais lui a répondu. Traduction automatique.", highlight=['Traduction']),
            L('T3', "Ce con a appelé les flics. Motif : cyberharcèlement et menaces de mort.", highlight=['Motif', 'mort.'])],
  'actors': [act('mec', [-1.3, 0, -2.6], 150, 'pour', 'happy', keys=[
      k('T1:photo', clip='readPhone', expr='smug', face=140, turn=0.15),
      k('T2', clip='readPhone', expr='suspicious', face=0, turn=0.2),
      k('T2:Traduction', expr='shocked'),
      k('T3', clip='phoneCall', expr='angry', face=-25, turn=0.2)])],
  'props': [P('sushi', 'sushiPlate', pos=[CT[0] - 0.1, CT[1], CT[2] + 0.12]), P('sauce', 'sauceBottle', scale=1.2, pos=[CT[0] + 0.32, CT[1], CT[2] + 0.1]),
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('T1:photo', visible=True)]),
            tweet_on_table('post', 2.4, 0.0, 1.6, name='ce mec', handle='@cemec_officiel', via='Publication', initial='C', avatar='#2C4A8A', text="Sushis + sauce algérienne. Les Japonais, vous allez rien faire.", likes='12 likes'),
            tweet_on_table('rep', 3.4, 0.0, 1.6, name='Hiro', handle='@hiro_tokyo', initial='H', text="Votre sauce a insulté mon grand-père le riz.", likes='0 rire · 3 likes')],
  'sfx': [{'at': 'T1:photo+0.1', 'name': 'shutter', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'ms', worldAngle=60),
           cam('T1:sushis', [[CT[0] + 0.05, CT[1] + 0.1, CT[2] + 0.12]], 'cu', worldAngle=20, elev=25, noOcclusion=True),
           tweet_cam('T1:algérienne', 2.4, 0.0, 1.6),
           cam('T2', 'mec', 'cu', angle=10),
           tweet_cam('T2:Traduction', 3.4, 0.0, 1.6),
           cam('T3', 'mec', 'cu', angle=-35)],
  'tail': 0.2,
})

TB = (0.05, 0.785, -0.5)
scenes.append({
  'id': 'gav', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('T4', "Les flics ont interrogé le téléphone.", highlight=['téléphone.']),
            L('T5', "Vous reconnaissez les faits ?", 'commissaire'),
            L('T6', "La traduction a répondu.", highlight=['traduction']),
            L('T7', "Dix ans.", 'commissaire', highlight=['Dix', 'ans.'])],
  'actors': [
    act('commissaire', IR_COP, -90, 'leanTable', 'suspicious', keys=[k('T5', clip='leanTable', expr='angry'), k('T7', clip='slamTable', expr='angry', sfx='thud', sfxAt=0.12)]),
    act('flic2', IR_COP2, 115, 'armsCrossed', 'unimpressed', keys=[k('T6', clip='lookDown', expr='shocked')]),
  ],
  'props': [P('aveu0', 'tweetPhone', pos=[TB[0], TB[1] + 0.008, TB[2]], rot=[-1.5708, 0, 0], opts={'name': 'ce mec', 'handle': '@cemec_officiel', 'via': 'Publication', 'initial': 'C', 'avatar': '#2C4A8A', 'text': 'Sushis + sauce algérienne.', 'likes': ''}, keys=[k('T6', visible=False)]),
            P('aveu', 'tweetPhone', pos=[TB[0], TB[1] + 0.009, TB[2]], rot=[-1.5708, 0, 0], visible=False, opts={'name': 'ce mec', 'handle': '@cemec_officiel', 'via': 'Traduit automatiquement', 'initial': 'C', 'avatar': '#2C4A8A', 'text': "J'avoue avoir mangé la tour Eiffel avec de la mayonnaise.", 'likes': ''}, keys=[k('T6', visible=True)])],
  'cams': [cam(0, ['commissaire', [TB[0], 0.9, TB[2]]], 'fs', worldAngle=10, elev=14),
           cam('T5', 'commissaire', 'mcu', angle=60),
           tweet_cam('T6:répondu', *TB),
           cam('T7', 'commissaire', 'mcu', angle=50, move='push', amount=0.05)],
  'tail': 0.2,
})

scenes.append({
  'id': 'chef', 'set': 'restaurant', 'setOpts': {'brand': 'SUSHI'}, 'ambience': None,
  'lines': [L('T8', "Puis un grand chef japonais a goûté la sauce.", highlight=['goûté']),
            L('T9', "Traduction : délicieux, je veux épouser cette sauce.", highlight=['épouser'])],
  'actors': [act('chef', [0, 0, -3.15], 0, 'idle', 'neutral', keys=[k('T8:goûté', clip='eatHands', expr='suspicious'), k('T8.end', clip='celebrate', expr='happy')])],
  'props': [P('sushi', 'sushiPlate', pos=[-0.15, 0.79, -2.6]), P('sauce', 'sauceBottle', scale=1.2, pos=[0.3, 0.79, -2.55]),
            tweet_on_table('post', 2.6, 0.0, 1.5, name='Chef Takumi', handle='@chef_takumi', initial='T', avatar='#3F8A84', text="Délicieux. Je veux épouser cette sauce.", likes='3 M likes')],
  'cams': [cam(0, 'chef', 'ms', angle=10),
           cam('T8.end', 'chef', 'mcu', angle=-15),
           tweet_cam('T9', 2.6, 0.0, 1.5)],
  'tail': 0.2,
})

TT = (0, 0.76, -1.55)
scenes.append({
  'id': 'traite', 'set': 'pressRoom', 'setOpts': {'backdrop': 'TRAITÉ DE PAIX|FRANCE|JAPON|SAUCE', 'bg': '#D9E2E8', 'fg': '#2E4563', 'podium': False, 'flags': False}, 'ambience': 'station',
  'lines': [L('T10', "Traité de paix franco-japonais. Clause un : la France rend le drapeau de Luffy.", highlight=['Luffy.']),
            L('T11', "Clause deux : le Japon garde la sauce.", highlight=['sauce.'])],
  'actors': [
    act('dipFR', [-0.5, 0.12, -2.05], 0, 'sitWrite', 'neutral', keys=[k('T10:rend', clip='sitGive', expr='sad')]),
    act('dipJP', [0.5, 0.12, -2.05], 0, 'sitWrite', 'neutral', keys=[k('T10:Luffy', clip='sitTake', expr='happy'), k('T11:garde', clip='sitShow', expr='happy')]),
  ],
  'props': [P('table', 'table', pos=[0, 0, -1.55], opts={'w': 1.6, 'd': 0.8, 'color': '#7A5C3A'}),
            P('c1', 'chair', pos=[-0.5, 0, -2.15]), P('c2', 'chair', pos=[0.5, 0, -2.15]),
            P('fFR', 'flag', pos=[-1.7, 0, -2.6], opts={'colors': ['#2C4A8A', '#F6F1E3', '#C23A2E']}), P('fJP', 'flag', pos=[1.4, 0, -2.6], opts={'colors': ['#F6F1E3'], 'disc': '#C23A2E'}),
            P('sushi', 'sushiPlate', pos=[0.05, 0.765, -1.5]),
            P('sauce', 'sauceBottle', scale=1.2, pos=[-0.15, 0.765, -1.35], keys=[k('T11:garde', attach='dipJP', hand='R')]),
            P('luffy', 'flag', scale=0.7, opts={'colors': ['#141A22'], 'disc': '#F6F1E3', 'skull': True, 'grip': True}, on={'actor': 'dipFR', 'hand': 'R'}, visible=False, keys=[k('T10:rend', visible=True), k('T10:Luffy+0.2', attach='dipJP', hand='L')])],
  'cams': [cam(0, ['dipFR', 'dipJP'], 'fs', worldAngle=0, elev=8),
           cam('T10:rend', ['dipFR', 'dipJP', 'luffy'], 'ms', worldAngle=0, withProps=True),
           cam('T11', 'dipJP', 'mcu', angle=-10)],
  'tail': 0.2,
})

scenes.append({
  'id': 'cellule', 'set': 'prisonCell', 'ambience': None,
  'lines': [L('T12', "Ce mec est resté en prison. Personne n'a traduit sa libération.", highlight=['traduit', 'libération.'])],
  'actors': [act('mec', [2.0, 0.24, -2.3], 0, 'sit', 'sad', keys=[k('T12:Personne', clip='stareCamera', expr='unimpressed')])],
  'props': [tweet_on_table('tel', 1.35, 0.0, -1.55, name='Ministère', handle='@justice', initial='J', avatar='#B5302A', via='Traduit du japonais par X', text="Libération : traduction indisponible.", likes='')],
  'cams': [cam(0, 'mec', 'ms', worldAngle=-20),
           tweet_cam('T12:traduit', 1.35, 0.0, -1.55),
           cam('T12.end', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu05_traduction', 'La traduction', scenes, {
  'chef': {'preset': 'chef', 'hairColor': '#17181B', 'hair': 'crew', 'facial': 'none'},
  'dipFR': {'preset': 'lemec_charcoal', 'tie': '#2C4A8A', 'seed': 31}, 'dipJP': {'preset': 'politique', 'hair': 'crew', 'hairColor': '#17181B', 'suit': '#3A3D44', 'seed': 32},
})
