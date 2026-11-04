#!/usr/bin/env python3
"""LA CANETTE. Ce mec shakes a can of soda to open it faster -> it explodes -> he takes off (soda jet) -> a speed camera
flashes him at 300 km/h -> in a 30 zone -> ce con contests the fine -> the judge suspends his pedestrian licence -> banned
from walking -> now he goes to work by can (and gets flashed again). (Classic formula, no news gags.)"""
from actu_common import *

COLA = '#6B3A1E'
CAN_DOWN = {'rot': [3.1416, 0, 0]}                                   # the can held upside down: the jet goes along the arm
JET = lambda hand, vis=True, keys=None: P(f'jet{hand}', 'beerStream', visible=vis, opts={'length': 1.1, 'r': 0.018, 'flare': 3.2, 'color': COLA},
                                          on={'actor': 'mec', 'hand': hand, 'offset': [0, -0.12, 0]}, keys=keys or [])
FLY_Y, FLY_Z = 2.5, 0.3                                               # flight line above the pavement, in front of the radar
RADAR = [1.4, 0, -1.25]                                               # trafficCamera pole (its head is 0.8 m to the right)
PASS_X = RADAR[0] + 0.8
DISPLAY = [3.6, 0, -1.25]
SIGN30 = [-1.8, 0, -1.25]
RADAR_POV = lambda at: POV(at, [2.6, 1.7, 7.2], [2.6, 2.2, -1.25], 52)
scenes = []
scenes.append({
  'id': 'rue', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('C1', "Ce mec a secoué une canette de soda pour l'ouvrir plus vite.", highlight=['canette', 'vite.']),
            L('C2', "Elle a explosé.", highlight=['explosé.']),
            L('C3', "Il a décollé.", highlight=['décollé.'])],
  'actors': [act('mec', [0, 0, 0.8], 0, 'stand', 'smug', keys=[
      k('C1:secoué', clip='shakeCan', expr='happy'),
      k('C2:explosé', clip='startle', expr='shocked'),
      k('C3', clip='stiff', expr='shocked'),
      k('C3:décollé', to=[0, 7.5, 0.8], glide=True, dur=0.9, ease='in', clip='stiff', then='stiff')])],
  'props': [P('canette', 'drinkCan', on={'actor': 'mec', 'hand': 'R'}, keys=[k('C3', attach='mec', hand='R', **CAN_DOWN)]),
            P('mallette', 'briefcase', on={'actor': 'mec', 'hand': 'L'}),
            P('gerbe', 'dustPuff', scale=1.2, visible=False, opts={'color': COLA, 'once': True, 'period': 0.7, 'startAt': 'C2:explosé'},
              on={'actor': 'mec', 'hand': 'R'}, keys=[k('C2:explosé', visible=True), k('C3', visible=False)]),
            JET('R', vis=False, keys=[k('C3', visible=True)]),
            P('flaque', 'dustPuff', scale=1.1, visible=False, pos=[0, 0, 0.8], opts={'color': '#C08A5A', 'once': True, 'period': 0.8, 'startAt': 'C3:décollé'},
              keys=[k('C3:décollé', visible=True)])],
  'sfx': [{'at': 'C1:secoué', 'name': 'pour', 'vol': 0.3}, {'at': 'C1:soda', 'name': 'pour', 'vol': 0.3},
          {'at': 'C2:explosé', 'name': 'pop', 'vol': 0.7}, {'at': 'C2:explosé', 'name': 'splash', 'vol': 0.6},
          {'at': 'C3:décollé', 'name': 'jet', 'vol': 0.6}],
  'cams': [cam(0, 'mec', 'ms', angle=15),
           cam('C1:canette', 'mec', 'mcu', angle=-15),
           POV('C3', [0.4, 1.1, 6.0], [0, 2.1, 0.8], 62)],
  'tail': 0.2,
})
# the flight: constant speed, timed so that the radar head is passed exactly on "flashé" (scene time ~0.87 s)
V = 9.4
scenes.append({
  'id': 'ciel', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('C4', "Un radar l'a flashé à trois cents kilomètres-heure.", highlight=['radar', 'trois', 'cents']),
            L('C5', "Dans une zone trente.", highlight=['trente.'])],
  'actors': [act('mec', [PASS_X - V * 0.87, FLY_Y, FLY_Z], 90, 'superman', 'happy', keys=[
      k(0, to=[PASS_X + V * 1.6, FLY_Y, FLY_Z], glide=True, dur=2.47, clip='superman', then='superman', face='keep')])],
  'props': [P('radar', 'trafficCamera', pos=RADAR, opts={'flashAt': 'C4:flashé'}),
            P('affichage', 'speedDisplay', pos=DISPLAY, opts={'value': 300, 'color': '#FF3B2E'}),
            P('zone30', 'speedSign', pos=SIGN30, opts={'value': 30}),
            P('canette', 'drinkCan', on={'actor': 'mec', 'hand': 'L', **CAN_DOWN}),
            JET('L')],
  'fx': [{'type': 'flash', 'at': 'C4:flashé', 'dur': 0.3}],
  'sfx': [{'at': 0, 'name': 'jet', 'vol': 0.5}, {'at': 'C4:flashé-0.25', 'name': 'whoosh', 'vol': 0.6}, {'at': 'C4:flashé', 'name': 'shutter', 'vol': 0.8},
          {'at': 'C4:trois', 'name': 'beep', 'vol': 0.4}, {'at': 'C5:trente', 'name': 'ding', 'vol': 0.4}],
  'cams': [cam(0, 'mec', 'ms', angle=-80, move='track'),
           RADAR_POV('C4:flashé-0.3'),
           POV('C4:trois', [DISPLAY[0], 2.2, 0.95], [DISPLAY[0], 2.2, -1.25], 30),
           POV('C5', [SIGN30[0], 2.3, 1.25], [SIGN30[0], 2.3, -1.25], 34)],
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('C6', "Alors ce con a contesté l'amende.", highlight=['contesté']),
            L('C7', "Le juge a suspendu son permis piéton.", highlight=['permis', 'piéton.']),
            L('C8', "Putain, interdit de marcher.", highlight=['marcher.'])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('C7:suspendu', clip='sitPoint', expr='angry')]),
             act('mec', [0.9, 0, -1.7], 180, 'stand', 'angry', keys=[
                 k('C6:contesté', clip='showPhone', expr='angry'),
                 k('C7:permis', clip='showPhone', expr='shocked'),
                 k('C8', face=60, turn=0.25, clip='stand', expr='unimpressed'),
                 k('C8:interdit-0.45', to=[1.45, 0, -1.4], glide=True, dur=0.45, clip='walk', then='stiff', expr='happy'),
                 k('C8:interdit', expr='shocked'),
                 k('C8:marcher', face=10, turn=0.25, clip='stareCamera', expr='unimpressed')]),
             act('flic1', [2.6, 0, -0.6], -120, 'stand', 'neutral', keys=[k('C8:interdit', clip='whistleBlow', expr='angry', sfx='whistle')])],
  'props': [P('amende', 'bill', scale=1.7, opts={'title': 'AMENDE', 'items': [['Vitesse : 300 km/h', ''], ['Zone : 30', ''], ['', '']], 'total': '1 500,00 €'},
              on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('C7:permis', visible=False)]),
            P('permis', 'notebook', scale=1.8, visible=False, opts={'text': 'PERMIS\nPIÉTON\n—\nSUSPENDU', 'bg': '#C2557A'},
              on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('C7:permis', visible=True), k('C8', visible=False)]),
            P('sifflet', 'whistle', on={'actor': 'flic1', 'hand': 'R'})],
  'sfx': [{'at': 'C6:amende', 'name': 'paper', 'vol': 0.5}, {'at': 'C7:suspendu', 'name': 'gavel', 'vol': 0.6}, {'at': 'C7:piéton', 'name': 'gavel', 'vol': 0.6}],
  'cams': [cam(0, ['juge', 'mec'], 'fs', worldAngle=0, elev=6),
           cam('C6:amende', 'amende', 'cu', worldAngle=180, noOcclusion=True, zoom=1.2),
           cam('C7', 'juge', 'mcu', angle=0),
           cam('C7:permis', 'permis', 'cu', worldAngle=180, noOcclusion=True, zoom=1.2),
           cam('C8', ['mec', 'flic1'], 'ms', worldAngle=-30),
           cam('C8:marcher', 'mec', 'cu', angle=0)],
  'tail': 0.2,
})
# the commute: tracked flight, then a second radar flashes him again in the tail
scenes.append({
  'id': 'fin', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('C9', "Depuis, il va au travail en canette.", pre=0.3, highlight=['travail', 'canette.'])],
  'actors': [act('mec', [-26, FLY_Y, FLY_Z], 90, 'superman', 'unimpressed', keys=[
      k(0, to=[-6, FLY_Y, FLY_Z], glide=True, dur=2.6, clip='superman', then='superman', face='keep'),
      k('C9.end+0.25', to=[-4.0, FLY_Y, FLY_Z], glide=True, dur=0.02, clip='superman', then='superman', face='keep'),
      k('C9.end+0.28', to=[-4.0 + V * 2.0, FLY_Y, FLY_Z], glide=True, dur=2.0, clip='superman', then='superman', face='keep')])],
  'props': [P('radar', 'trafficCamera', pos=RADAR, opts={'flashAt': f'C9.end+{0.28 + (PASS_X + 4.0) / V:.2f}'}),
            P('affichage', 'speedDisplay', pos=DISPLAY, opts={'value': 300, 'color': '#FF3B2E'}),
            P('canette', 'drinkCan', on={'actor': 'mec', 'hand': 'L', **CAN_DOWN}),
            P('mallette', 'briefcase', on={'actor': 'mec', 'hand': 'R'}),
            JET('L')],
  'fx': [{'type': 'flash', 'at': f'C9.end+{0.28 + (PASS_X + 4.0) / V:.2f}', 'dur': 0.3}],
  'sfx': [{'at': 0, 'name': 'jet', 'vol': 0.45}, {'at': 'C9.end+0.28', 'name': 'jet', 'vol': 0.5},
          {'at': f'C9.end+{0.28 + (PASS_X + 4.0) / V:.2f}', 'name': 'shutter', 'vol': 0.8}],
  'cams': [cam(0, 'mec', 'ms', angle=-70, move='track'),
           RADAR_POV('C9.end+0.25')],
  'tail': 1.4,
})

write('canette', 'La canette', scenes, {'juge': {'preset': 'judge'}})
