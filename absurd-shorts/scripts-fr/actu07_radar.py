#!/usr/bin/env python3
"""ACTU 07 — LE RADAR. Flashed at 67 km/h, on foot -> the cop: "Six-seven !" -> the whole station does the gesture
(ministry: 161 000, unions: 480 000) -> arrested (motif: rébellion en bande organisée) -> fine 67 €, cell 67, 67 hours ->
a Japanese post about it, machine-translated, nobody laughs -> at trial: "Vitesse ?" "Six-seven." -> the judge does
the gesture, released -> leaving court, the judge is flashed at 67, on foot."""
from actu_common import *

scenes = []
RADAR, DISPLAY = [1.4, 0, -1.25], [3.3, 0, -1.25]
scenes.append({
  'id': 'radar', 'set': 'street', 'ambience': 'street',
  'lines': [L('R1', "Ce mec s'est fait flasher à 67 kilomètres-heure. À pied.", highlight=['67', 'pied.']),
            L('R2', "Six-seven !", 'flic1', highlight=['Six-seven'])],
  'actors': [
    act('mec', [-7.5, 0, 0.55], 90, 'idle', 'happy', keys=[k(0.15, to=[7.5, 0, 0.55], clip='run', speed=6.5, then='idle')]),
    act('flic1', [4.0, 0, -0.55], -60, 'clipboard', 'neutral', keys=[k('R1:pied', clip='lookItem', face=-40, turn=0.2), k('R2', clip='sixSeven', expr='happy', face=0, turn=0.15)]),
  ],
  'props': [P('radar', 'trafficCamera', pos=RADAR, opts={'flashAt': ['R1:flasher', 'R1:flasher+0.18']}), P('affiche', 'speedDisplay', pos=DISPLAY, opts={'value': 67})],
  'sfx': [{'at': 'R1:flasher', 'name': 'shutter', 'vol': 0.7}],
  'cams': [cam(0, 'mec', 'fs', angle=-70, move='track'),
           cam('R1:flasher', ['radar', 'mec'], 'fs', worldAngle=10, elev=4),
           cam('R1:67', [[DISPLAY[0], 2.2, DISPLAY[2]]], 'cu', worldAngle=0, noOcclusion=True),
           cam('R2', 'flic1', 'ms', angle=10)],
  'tail': 0.15,
})

COPS = {'id': 'cops', 'count': 3, 'spec': {'preset': 'cop', 'seed': 51}, 'clip': 'sixSeven', 'ry': 10, 'positions': [[-1.6, 0, -1.2], [-0.5, 0, -1.5], [0.7, 0, -1.25]]}
scenes.append({
  'id': 'commissariat', 'set': 'policeStation', 'ambience': 'station',
  'crowd': [COPS],
  'lines': [L('R3', "Tout le commissariat a fait le geste.", highlight=['geste.']),
            L('R4', "Selon le ministère, cent soixante et un mille personnes. Selon les syndicats, quatre cent quatre-vingt mille.", highlight=['ministère,', 'syndicats,']),
            L('R5', "Ce mec a été arrêté. Motif : rébellion en bande organisée.", highlight=['Motif', 'organisée.']),
            L('R6', "Amende : 67 euros. Cellule 67. Garde à vue : 67 heures.", highlight=['67'])],
  'actors': [
    act('flic1', [1.7, 0, -0.9], -20, 'sixSeven', 'happy', keys=[k('R5', clip='cuffOther', expr='neutral', face='mec', turn=0.2)]),
    act('flic2', [-2.6, 0, -0.6], 30, 'sixSeven', 'happy'),
    act('commissaire', [2.7, 0, -1.4], -30, 'sixSeven', 'happy', keys=[k('R6', clip='showPhone', expr='smug', face='mec', turn=0.2)]),
    act('ministere', [-4.0, 0, 1.2], 60, 'clickCount', 'neutral'),
    act('syndicat', [4.0, 0, 1.3], -60, 'clickCount', 'happy'),
    act('mec', [2.2, 0, 0.3], -10, 'stand', 'shocked', keys=[k('R5:arrêté', clip='handcuffed', expr='sad'), k('R6:Cellule', to=[5.1, 0, -2.75], glide=True, dur=0.05, face=0, clip='stand')]),
  ],
  'props': [P('clic1', 'clickCounter', on={'actor': 'ministere', 'hand': 'R'}), P('clic2', 'clickCounter', on={'actor': 'syndicat', 'hand': 'R'}),
            P('cuffs', 'handcuffs', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('R5:arrêté', visible=True)]),
            P('pv', 'bill', scale=1.6, visible=False, opts={'title': 'AMENDE', 'items': [['Excès de vitesse à pied', '67,00'], ['Six-seven', '0,00']], 'total': '67,00 €'}, on={'actor': 'commissaire', 'hand': 'R', **HAND_FLAT}, keys=[k('R6', visible=True)]),
            P('num', 'signBoard', pos=[5.1, 0, -1.92], opts={'text': 'CELLULE 67', 'bg': '#F6F1E3', 'fg': '#141A22', 'w': 1.1, 'h': 0.3, 'posts': False, 'height': 2.2})],
  'cams': [cam(0, ['flic1', 'flic2', 'commissaire', 'cops1'], 'fs', worldAngle=0, elev=8),
           cam('R4', 'ministere', 'ms', angle=10),
           cam('R4:syndicats', 'syndicat', 'ms', angle=-10),
           cam('R5', ['mec', 'flic1'], 'ms', worldAngle=10),
           cam('R6', 'pv', 'cu', worldAngle=-30, noOcclusion=True, zoom=1.5),
           cam('R6:Cellule', [[5.1, 2.35, -1.9]], 'cu', worldAngle=0, noOcclusion=True, zoom=1.5),
           cam('R6:Garde', 'mec', 'ms', worldAngle=0)],
  'tail': 0.2,
})

TWD = (-2.55, 0.76, -1.85)
scenes.append({
  'id': 'tweet', 'set': 'policeStation', 'ambience': 'station',
  'lines': [L('R7', "Au Japon, un mec a tweeté une blague sur l'affaire.", highlight=['Japon,', 'blague']),
            L('R8', "Personne n'a ri.", highlight=['Personne'])],
  'actors': [act('flic2', [-2.7, 0.12, -2.7], 0, 'sit', 'neutral', keys=[k('R8', clip='sit', expr='unimpressed')]),
             act('flic1', [-1.6, 0, -1.6], -100, 'lookDown', 'neutral', keys=[k('R8', clip='stareCamera', expr='unimpressed', face=-20, turn=0.2)])],
  'props': [tweet_on_table('tw', *TWD, name='Kenji', handle='@kenji_lol', text="Le Français compte jusqu'à sept, puis il fait grève.", likes='0 rire · 1 like')],
  'sfx': [{'at': 'R8', 'name': 'crickets', 'vol': 0.7}],
  'cams': [tweet_cam('R7:tweeté', *TWD), cam('R8', ['flic2', 'flic1'], 'ms', worldAngle=10)],
  'tail': 0.4,
})

scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('R9', "Au procès, ce con a plaidé coupable.", highlight=['coupable.']),
            L('R10', "Vitesse ?", 'juge'),
            L('R11', "Six-seven.", 'mec', highlight=['Six-seven.']),
            L('R12', "Le juge a fait le geste. Relaxé.", highlight=['Relaxé.'])],
  'actors': [
    act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('R10', clip='sitPoint', expr='suspicious'), k('R12', to=[0, 0.3, -4.2], glide=True, dur=0.2, clip='sixSeven', then='sixSeven', face='keep', expr='happy')]),
    act('mec', [0.6, 0, -1.6], 180, 'handcuffed', 'sad', keys=[k('R11', clip='sixSeven', expr='smug'), k('R12:Relaxé', clip='celebrate', expr='happy')]),
  ],
  'props': [P('cuffs', 'handcuffs', on={'actor': 'mec', 'hand': 'R'}, keys=[k('R12:Relaxé', visible=False)])],
  'sfx': [{'at': 'R12:Relaxé', 'name': 'gavel', 'vol': 0.6}],
  'cams': [cam(0, 'juge', 'ms', worldAngle=0, elev=6),
           cam('R10', 'juge', 'mcu', angle=0),
           cam('R11', 'mec', 'ms', worldAngle=180, allowBack=True),
           cam('R12', 'juge', 'ms', angle=0)],
  'tail': 0.2,
})

scenes.append({
  'id': 'sortie', 'set': 'street', 'ambience': 'street',
  'lines': [L('R13', "En sortant, le juge s'est fait flasher à 67.", highlight=['67.']),
            L('R14', "Six-seven !", 'flic1', highlight=['Six-seven'])],
  'actors': [
    act('juge', [-7.5, 0, 0.55], 90, 'idle', 'happy', keys=[k(0.1, to=[7.5, 0, 0.55], clip='run', speed=6.5, then='idle')]),
    act('flic1', [4.0, 0, -0.55], -60, 'clipboard', 'neutral', keys=[k('R14', clip='sixSeven', expr='happy', face=0, turn=0.15)]),
  ],
  'props': [P('radar', 'trafficCamera', pos=RADAR, opts={'flashAt': ['R13:flasher', 'R13:flasher+0.18']}), P('affiche', 'speedDisplay', pos=DISPLAY, opts={'value': 67})],
  'sfx': [{'at': 'R13:flasher', 'name': 'shutter', 'vol': 0.7}],
  'cams': [cam(0, 'juge', 'fs', angle=-70, move='track'),
           cam('R13:67', [[DISPLAY[0], 2.2, DISPLAY[2]]], 'cu', worldAngle=0, noOcclusion=True),
           cam('R14', 'flic1', 'ms', angle=10, move='push', amount=0.05)],
  'tail': 1.3,
})

write('actu07_radar', 'Le radar', scenes, {
  'juge': {'preset': 'judge'}, 'ministere': {'preset': 'lemec_charcoal', 'glasses': True, 'seed': 61}, 'syndicat': {'preset': 'worker', 'seed': 62},
})
