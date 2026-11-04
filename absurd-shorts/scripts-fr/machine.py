#!/usr/bin/env python3
"""LA MACHINE. Ce mec washes his jeans at 90 degrees so they are really clean -> the jeans shrink -> so does he -> 30 cm ->
ce con sues the washing machine for aggravated assault -> the machine stays silent -> then spin-dries the lawyer -> now he
lives in the drum -> delicate programme, on Sundays. (Classic formula, no news gags.)"""
import math
from actu_common import *

JEAN = '#3E5A8A'
MW = [-0.3, 0, -3.07]                                  # bathroom: the machine against the back wall, next to the towel
DRUM_POV = lambda at, fov=40: POV(at, [MW[0], 0.46, MW[2] + 1.15], [MW[0], 0.4, MW[2] + 0.33], fov)
scenes = []
scenes.append({
  'id': 'buanderie', 'set': 'bathroom', 'ambience': None,
  'lines': [L('M1', "Ce mec a lavé son jean à quatre-vingt-dix degrés pour qu'il soit bien propre.", highlight=['jean', 'quatre-vingt-dix', 'propre.']),
            L('M2', "Le jean a rétréci.", highlight=['rétréci.']),
            L('M3', "Ce mec aussi.", highlight=['aussi.']),
            L('M4', "Il mesure maintenant trente centimètres.", highlight=['trente', 'centimètres.'])],
  'actors': [act('mec', [0.22, 0, -2.45], -120, 'stand', 'happy', keys=[
      k('M1:jean', clip='giveItem', expr='happy'),
      k('M1:degrés+0.2', clip='stand', expr='smug'),
      k('M2', face=15, turn=0.25, clip='holdOut', expr='shocked'),
      k('M3:aussi', scale=0.167, dur=0.35, clip='stand', expr='shocked'),
      k('M4', expr='sad'), k('M4:centimètres', clip='stareCamera', expr='unimpressed')])],
  'props': [P('machine', 'washingMachine', pos=MW, opts={'laundry': JEAN, 'laundryAt': 'M1:degrés', 'spinAt': ['M1:degrés+0.25', 'M2-0.3'], 'spinRates': [24, 0]}),
            P('jean', 'jean', on={'actor': 'mec', 'hand': 'R'}, keys=[k('M1:degrés', visible=False)]),
            P('jeanMini', 'jean', scale=0.3, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('M2', visible=True), k('M3:aussi', visible=False)])],
  'sfx': [{'at': 'M1:degrés', 'name': 'click', 'vol': 0.5}, {'at': 'M1:degrés+0.25', 'name': 'engine', 'vol': 0.35}, {'at': 'M1:degrés+0.3', 'name': 'pour', 'vol': 0.3},
          {'at': 'M2:rétréci', 'name': 'squeak', 'vol': 0.5}, {'at': 'M3:aussi', 'name': 'boing', 'vol': 0.6}],
  'cams': [cam(0, ['mec', 'machine'], 'ms', worldAngle=-45, withProps=True),
           DRUM_POV('M1:degrés+0.1', 38),
           cam('M2', 'mec', 'mcu', angle=0),
           POV('M3', [0.65, 1.1, 0.1], [0.15, 0.95, -2.45], 56),
           POV('M4', [0.65, 0.2, -1.65], [0.05, 0.32, -2.7], 48)],
  'tail': 0.2,
})
# the machine is the defendant; the lawyer gets pulled into the drum and tumbles there
MC, MRY = [-1.1, 0, -2.3], 30
fx, fz = math.sin(math.radians(MRY)), math.cos(math.radians(MRY))
LAW_S = 0.11
DOME = [MC[0] + 0.40 * fx, 0.42 - 0.95 * LAW_S, MC[2] + 0.40 * fz]          # hips at the drum centre, inside the glass dome
DRUMC = [MC[0] + 0.33 * fx, 0.42, MC[2] + 0.33 * fz]
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('M5', "Alors ce con a porté plainte contre la machine. Pour violences aggravées.", highlight=['plainte', 'violences', 'aggravées.']),
            L('M6', "La machine a gardé le silence.", highlight=['silence.']),
            L('M7', "Puis elle a essoré l'avocat.", highlight=['essoré'])],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('M6:silence', expr='suspicious')]),
             act('mec', [2.5, 1.11, -3.3], -75, 'stand', 'angry', scale=0.167, keys=[k('M5:plainte', clip='angryFist'), k('M5:machine', clip='point'),
                                                                                    k('M7:essoré+0.2', clip='startle', expr='shocked')]),
             act('avocat', [0.7, 0, -1.7], -108, 'stand', 'neutral', keys=[
                 k('M5:violences', clip='point', expr='angry'),
                 k('M6', clip='handsOnHips', expr='smug'),
                 k('M7', to=[-0.35, 0, -1.55], glide=True, dur=0.55, clip='walk', then='yell', face=-120, expr='angry'),
                 k('M7:essoré', to=DOME, glide=True, dur=0.25, clip='flail', then='tumble', face=MRY, expr='shocked'),
                 k('M7:essoré', scale=LAW_S, dur=0.25)])],
  'props': [P('machine', 'washingMachine', pos=MC, ry=MRY, opts={'spinAt': ['M7:essoré'], 'spinRates': [24]})],
  'sfx': [{'at': 'M5:plainte', 'name': 'paper', 'vol': 0.4}, {'at': 'M5:aggravées', 'name': 'gavel', 'vol': 0.5}, {'at': 'M6:silence', 'name': 'crickets', 'vol': 0.6},
          {'at': 'M7:essoré', 'name': 'whoosh', 'vol': 0.6}, {'at': 'M7:essoré+0.2', 'name': 'engine', 'vol': 0.45}, {'at': 'M7:essoré+0.25', 'name': 'splash', 'vol': 0.4}],
  'cams': [cam(0, ['juge', 'machine', 'avocat'], 'fs', worldAngle=10, elev=6, withProps=True),
           cam('M5:plainte', 'mec', 'cu', angle=0, noOcclusion=True),
           cam('M5:violences', ['avocat', 'machine'], 'ms', worldAngle=-30, withProps=True),
           POV('M6', [MC[0] + 1.6 * fx, 0.62, MC[2] + 1.6 * fz], [MC[0], 0.45, MC[2]], 40),
           cam('M7', ['avocat', 'machine'], 'ms', worldAngle=-30, withProps=True),
           POV('M7:essoré+0.3', [DRUMC[0] + 0.9 * fx, 0.46, DRUMC[2] + 0.9 * fz], DRUMC, 36)],
  'tail': 0.2,
})
# he lives in the drum; Sunday: delicate programme (he walks like a hamster in a wheel), then the end-of-cycle beeps
MEC_S = 0.15
IN_DRUM = [MW[0], 0.215, MW[2] + 0.36]
scenes.append({
  'id': 'tambour', 'set': 'bathroom', 'ambience': None,
  'lines': [L('M8', "Putain, il vit dans le tambour.", highlight=['tambour.']),
            L('M9', "Programme délicat, le dimanche.", highlight=['délicat,', 'dimanche.'])],
  'actors': [act('mec', IN_DRUM, 0, 'sitFloor', 'neutral', scale=MEC_S, keys=[
      k('M9', clip='stand', expr='unimpressed'), k('M9:délicat', clip='walk', expr='unimpressed'),
      k('M9.end+0.95', clip='stareCamera', expr='unimpressed')])],
  'props': [P('machine', 'washingMachine', pos=MW, opts={'spinAt': ['M9:délicat', 'M9.end+0.9'], 'spinRates': [1.7, 0], 'shake': 0}),
            P('tasse', 'mug', scale=MEC_S, on={'actor': 'mec', 'hand': 'R'}, keys=[k('M9', visible=False)])],
  'sfx': [{'at': 'M9:délicat', 'name': 'engine', 'vol': 0.2}, {'at': 'M9.end+0.45', 'name': 'beep', 'vol': 0.5}, {'at': 'M9.end+0.7', 'name': 'beep', 'vol': 0.5},
          {'at': 'M9.end+0.95', 'name': 'beep', 'vol': 0.5}],
  'cams': [POV(0, [0.7, 1.15, -0.7], [-0.3, 0.5, -2.95], 50),
           DRUM_POV('M8:tambour', 42)],
  'tail': 1.4,
})

write('machine', 'La machine à laver', scenes, {'juge': {'preset': 'judge'}, 'avocat': {'preset': 'avocat'}})
