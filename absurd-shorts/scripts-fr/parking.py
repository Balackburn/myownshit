#!/usr/bin/env python3
"""LA PLACE. Written with the viral-video-writing loop (5 hooks, 3 drafts, score_fr.py 100/100):
hook with a number (45 minutes) -> the decision (never leaves) -> the villain at 6 s (the parking warden) -> re-hooks every
few seconds (one ticket a day, three years, twelve years) -> low point (his wife leaves on foot) -> the turn (he goes for
bread) -> callback payoff (the warden is parked in his spot) -> the last shot is the first shot (he circles again): a loop."""
from actu_common import *

ROAD_Y = -0.14                                   # the street's road surface
LANE = -2.55                                     # parking lane (car centres), cars face +x
DRIVE = -4.4                                     # near traffic lane
RED = '#C9473A'
SEAT = (0.05, 0.12, -0.4)                        # driver seat offset of the 'car' prop (facing +x)
def seat(x, z): return [x + SEAT[0], ROAD_Y + SEAT[1], z + SEAT[2]]
PARKED = [(-13.6, '#3E6FB5', 'GH-404-KL'), (-9.0, '#E8C14A', 'BC-777-XZ'), (-4.6, '#5E8C7A', 'FR-312-ME'),
          (4.6, '#F2F2EC', 'TU-509-PO'), (9.0, '#2C4A8A', 'DD-118-AA'), (13.6, '#8A5A9A', 'LM-660-QS')]
def parked(): return [P(f'c{i}', 'car', pos=[x, ROAD_Y, LANE], opts={'color': c, 'plate': pl}) for i, (x, c, pl) in enumerate(PARKED)]
def walls(grow=None, gate_keys=()):
    """the three brick walls round the spot (road side + both ends); grow = 3 times when they pop up; gate_keys on the +x end"""
    out = []
    for n, (wid, pos, ry, w) in enumerate([('murA', [0, ROAD_Y, -3.62], 0, 4.9), ('murB', [-2.45, ROAD_Y, -2.62], 90, 2.05), ('murC', [2.45, ROAD_Y, -2.62], 90, 2.05)]):
        keys = [k(grow[n], scale=1, dur=0.25)] if grow else []
        if wid == 'murC': keys += list(gate_keys)
        out.append(P(wid, 'brickWall', pos=pos, ry=ry, scale=0.01 if grow else 1, opts={'w': w, 'h': 1.3}, keys=keys))
    return out
BEARD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.02, 0.1]}
SIDE = lambda at: POV(at, [2.8, 1.75, 3.6], [0, 0.75, -2.6], 52)            # the spot seen from the pavement
scenes = []
scenes.append({
  'id': 'rue', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'daynight': {'from': 'Q4', 'period': 0.42},
  'lines': [L('Q1', "Ce mec a tourné quarante-cinq minutes pour trouver une place de parking.", highlight=['quarante-cinq', 'parking.']),
            L('Q2', "Il l'a trouvée. Il n'est plus jamais reparti.", highlight=['jamais']),
            L('Q3', "Le lendemain, un contractuel lui a mis une amende.", highlight=['contractuel', 'amende.']),
            L('Q4', "Puis une par jour.", highlight=['jour.'])],
  'actors': [act('mec', seat(-13.0, DRIVE), 90, 'drive', 'angry', keys=[
                 k(0, to=seat(-3.4, DRIVE), glide=True, dur=3.9, ease='linear', clip='drive', then='drive', face='keep'),
                 k('Q2:trouvée', to=seat(0, LANE), glide=True, dur=0.8, ease='inOut', clip='drive', then='sit', face='keep', expr='grin'),
                 k('Q2:jamais', expr='smug'), k('Q4', expr='unimpressed')]),
             act('contractuel', [7.5, 0, -0.9], -90, 'idle', 'neutral', keys=[
                 k('Q3-0.4', to=[2.1, 0, -1.2], clip='walk', speed=2.4, faceEnd=-150, then='writeOnHeld'),
                 k('Q3:amende-0.3', clip='giveItem', expr='smug'),
                 k('Q4-0.1', to=[9.0, 0, -0.9], clip='walk', speed=3.0, faceEnd=90, then='walk')])],
  'props': [P('voiture', 'car', pos=[-13.0, ROAD_Y, DRIVE], opts={'color': RED}, keys=[k(0, to=[-3.4, ROAD_Y, DRIVE], dur=3.9, ease='linear'),
                                                                                    k('Q2:trouvée', to=[0, ROAD_Y, LANE], dur=0.8, ease='inOut')]),
            *parked(),
            P('pv', 'bill', scale=0.9, visible=False, pos=[1.55, 0.79, -2.35], rot=[-1.5708, 0, 0.3], opts={'title': 'AMENDE', 'total': '35,00 €', 'items': [['Stationnement', '35'], ['', ''], ['', '']]},
              keys=[k('Q3:amende', visible=True)]),
            P('carnet', 'notebook', scale=0.9, visible=False, opts={'text': 'PV', 'bg': '#2C4A8A'}, on={'actor': 'contractuel', 'hand': 'L', **HAND_FLAT}, keys=[k('Q3-0.4', visible=True)]),
            P('pvs', 'paperPile', scale=0.05, visible=False, pos=[1.6, 0.78, -2.75], opts={'count': 34, 'seed': 9}, keys=[k('Q4', visible=True), k('Q4', scale=1.0, dur=1.3, ease='linear')])],
  'sfx': [{'at': 0, 'name': 'engine', 'vol': 0.35}, {'at': 'Q2:trouvée+0.7', 'name': 'brake', 'vol': 0.5}, {'at': 'Q3:amende', 'name': 'paper', 'vol': 0.6},
          {'at': 'Q4', 'name': 'paper', 'vol': 0.4}, {'at': 'Q4+0.42', 'name': 'paper', 'vol': 0.4}, {'at': 'Q4+0.84', 'name': 'paper', 'vol': 0.4}],
  'cams': [POV(0, [2.0, 5.5, 1.5], [-8.0, 0.0, -4.4], 50),
           cam('Q1:minutes', 'mec', 'cu', worldAngle=65, move='track', noOcclusion=True),
           POV('Q1:place', [4.0, 1.8, 3.4], [-1.2, 0.6, -2.8], 55),
           cam('Q2:jamais', 'mec', 'cu', worldAngle=65, noOcclusion=True),
           POV('Q3-0.4', [3.8, 1.6, 2.2], [1.3, 0.9, -1.7], 54),
           POV('Q4', [3.6, 2.3, 1.0], [1.3, 0.85, -2.6], 46)],
  'tail': 0.2,
})
scenes.append({
  'id': 'mur', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('Q5', "Alors ce con a construit un mur autour de sa voiture.", highlight=['mur']),
            L('Q6', "Au bout de trois ans, la mairie lui a envoyé la taxe foncière.", highlight=['trois', 'foncière.'])],
  'actors': [act('mec', [0.6, 0, -1.25], 180, 'stand', 'smug', keys=[
                 k('Q5:construit', clip='holdOut', expr='grin'),
                 k('Q6', to=seat(0, LANE), glide=True, dur=0.05, face=90, clip='sit', then='sit', expr='neutral'),
                 k('Q6:mairie', clip='sitShow', expr='shocked')])],
  'props': [P('voiture', 'car', pos=[0, ROAD_Y, LANE], opts={'color': RED}), *parked(),
            *walls(grow=['Q5:construit', 'Q5:mur', 'Q5:voiture']),
            P('brique', 'brickWall', scale=0.12, opts={'w': 2.0, 'h': 0.8}, on={'actor': 'mec', 'hand': 'R'}, keys=[k('Q6', visible=False)]),
            P('boite', 'mailbox', visible=False, pos=[1.55, 0, -1.3], opts={'color': '#F2C230'}, keys=[k('Q6', visible=True)]),
            P('plante', 'plant', scale=0.45, visible=False, pos=[-0.35, 1.92, LANE], keys=[k('Q6', visible=True)]),
            P('taxe', 'bill', scale=1.6, visible=False, opts={'title': 'TAXE FONCIÈRE', 'items': [['Place de parking', '1 240'], ['Mur', '380'], ['', '']], 'total': '1 620,00 €'},
              on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('Q6:mairie', visible=True)])],
  'sfx': [{'at': 'Q5:construit', 'name': 'thud', 'vol': 0.6}, {'at': 'Q5:mur', 'name': 'thud', 'vol': 0.6}, {'at': 'Q5:voiture', 'name': 'thud', 'vol': 0.6},
          {'at': 'Q6:mairie', 'name': 'paper', 'vol': 0.5}, {'at': 'Q6:foncière', 'name': 'cash', 'vol': 0.5}],
  'cams': [SIDE(0),
           cam('Q6', 'mec', 'ms', worldAngle=40, elev=10, noOcclusion=True),
           cam('Q6:taxe', 'taxe', 'mcu', worldAngle=90, noOcclusion=True)],
  'tail': 0.2,
})
scenes.append({
  'id': 'femme', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('Q7', "Sa femme est partie. À pied. Pour ne pas perdre la place.", highlight=['pied.', 'place.'])],
  'actors': [act('mec', seat(0, LANE), 90, 'sit', 'sad'),
             act('femme', [0.4, 0, -1.2], -90, 'stand', 'angry', keys=[k('Q7', to=[-9.0, 0, -0.9], clip='walk', speed=1.5, faceEnd=-90, then='walk')])],
  'props': [P('voiture', 'car', pos=[0, ROAD_Y, LANE], opts={'color': RED}), *parked(), *walls(),
            P('boite', 'mailbox', pos=[1.55, 0, -1.3], opts={'color': '#F2C230'}), P('plante', 'plant', scale=0.45, pos=[-0.35, 1.92, LANE]),
            P('valise', 'briefcase', scale=1.4, on={'actor': 'femme', 'hand': 'R'})],
  'sfx': [{'at': 'Q7', 'name': 'step', 'vol': 0.4}, {'at': 'Q7:pied', 'name': 'step', 'vol': 0.4}],
  'cams': [POV('Q7', [3.2, 1.6, 3.4], [-1.6, 0.9, -1.6], 55),
           cam('Q7:pied', 'femme', 'fs', worldAngle=-35, move='track'),
           cam('Q7:Pour', 'mec', 'cu', worldAngle=65, noOcclusion=True)],
  'tail': 0.2,
})
scenes.append({
  'id': 'pain', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('Q8', "Douze ans plus tard, il est allé acheter du pain.", highlight=['Douze', 'pain.']),
            L('Q9', "Quand il est revenu, le contractuel était garé dessus.", highlight=['contractuel', 'dessus.'])],
  'actors': [act('mec', seat(0, LANE), 90, 'sit', 'neutral', keys=[
                 k('Q8:allé', to=seat(14, LANE), glide=True, dur=1.6, ease='in', clip='drive', then='drive', face='keep', expr='grin'),
                 k('Q9-0.2', to=seat(-14, DRIVE), glide=True, dur=0.02, clip='drive', then='drive', face='keep'),
                 k('Q9', to=seat(-0.6, DRIVE), glide=True, dur=0.9, ease='out', clip='drive', then='drive', face='keep'),
                 k('Q9:dessus', expr='shocked')]),
             act('contractuel', [0.5, 0, -1.2], 10, 'armsCrossed', 'smug', visible=False, keys=[k('Q9-0.2', visible=True)])],
  'props': [P('voiture', 'car', pos=[0, ROAD_Y, LANE], opts={'color': RED}, keys=[k('Q8:allé', to=[14, ROAD_Y, LANE], dur=1.6, ease='in'),
                                                                               k('Q9-0.2', to=[-14, ROAD_Y, DRIVE], dur=0.02), k('Q9', to=[-0.6, ROAD_Y, DRIVE], dur=0.9, ease='out')]),
            P('asvp', 'car', visible=False, pos=[0, ROAD_Y, LANE], opts={'color': '#F2F2EC', 'plate': 'PV-000-PV'}, keys=[k('Q9-0.2', visible=True)]),
            *parked(), *walls(gate_keys=[k('Q8:allé-0.1', visible=False)]),
            P('boite', 'mailbox', pos=[1.55, 0, -1.3], opts={'color': '#F2C230'}),
            P('barbe', 'beard', scale=2.3, opts={'color': '#E6E2D8'}, on=BEARD)],
  'sfx': [{'at': 'Q8:allé', 'name': 'engine', 'vol': 0.45}, {'at': 'Q9', 'name': 'engine', 'vol': 0.35}, {'at': 'Q9+0.85', 'name': 'brake', 'vol': 0.5},
          {'at': 'Q9:dessus', 'name': 'sting', 'vol': 0.35}],
  'cams': [cam(0, 'mec', 'cu', worldAngle=65, noOcclusion=True),
           SIDE('Q8:allé-0.2'),
           POV('Q9', [5.0, 2.2, 3.2], [0.2, 0.7, -3.0], 55),
           cam('Q9:contractuel', 'contractuel', 'ms', angle=0),
           cam('Q9:dessus', 'mec', 'cu', worldAngle=65, noOcclusion=True)],
  'tail': 0.2,
})
scenes.append({
  'id': 'fin', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('Q10', "Putain, ça fait quarante-cinq minutes qu'il tourne.", pre=0.2, highlight=['quarante-cinq', 'tourne.'])],
  'actors': [act('mec', seat(-15.0, DRIVE), 90, 'drive', 'unimpressed', keys=[k(0, to=seat(-1.0, DRIVE), glide=True, dur=4.4, ease='linear', clip='drive', then='drive', face='keep')])],
  'props': [P('voiture', 'car', pos=[-15.0, ROAD_Y, DRIVE], opts={'color': RED}, keys=[k(0, to=[-1.0, ROAD_Y, DRIVE], dur=4.4, ease='linear')]),
            P('asvp', 'car', pos=[0, ROAD_Y, LANE], opts={'color': '#F2F2EC', 'plate': 'PV-000-PV'}), *parked(), *walls(gate_keys=[k(0, visible=False)]),
            P('barbe', 'beard', scale=2.3, opts={'color': '#E6E2D8'}, on=BEARD)],
  'sfx': [{'at': 0, 'name': 'engine', 'vol': 0.35}],
  'cams': [cam(0, 'mec', 'cu', worldAngle=65, move='track', noOcclusion=True),
           POV('Q10:minutes', [2.0, 5.5, 1.5], [-8.0, 0.0, -4.4], 50)],
  'tail': 1.4,
})

write('parking', 'La place', scenes, {'contractuel': {'preset': 'cop', 'seed': 52}, 'femme': {'preset': 'femme', 'seed': 21}})
