#!/usr/bin/env python3
"""LA SIESTE (viral-video-writing loop, score_fr.py 100/100). Hook with numbers (five minutes) -> twenty years later (time-lapse)
-> colleagues retired, the boss in an old people's home -> the office is a museum and he is the main exhibit -> complaint ->
the museum wins: listed as a historic monument -> can't move, can't yawn -> 15 € to watch him sleep -> loop: a five-minute
alarm, asleep again (the first shot)."""
from actu_common import *

DESK = [0.4, 0, -2.0]
SEAT = [DESK[0], 0.16, DESK[2] - 0.62]
BEARD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.02, 0.1]}
FRONT = lambda at, fov=48: POV(at, [DESK[0] + 0.6, 1.5, DESK[2] + 2.6], [DESK[0], 1.0, SEAT[2]], fov)
def office_props(old=True):
    return [P('bureau', 'desk', pos=DESK, ry=180, opts={'w': 1.6}), P('chaise', 'officeChair', pos=[SEAT[0], 0, SEAT[2] - 0.05]),
            P('ecran', 'pcMonitor', pos=[DESK[0] - 0.3, 0.76, DESK[2] + 0.05], ry=180)]
scenes = []
scenes.append({
  'id': 'bureau', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.5,
  'daynight': {'from': 'SI2', 'period': 0.22},
  'lines': [L('SI1', "Ce mec a fait une sieste de cinq minutes au bureau pour être plus productif.", highlight=['cinq', 'productif.']),
            L('SI2', "Il s'est réveillé vingt ans plus tard.", highlight=['vingt', 'ans']),
            L('SI3', "Ses collègues étaient à la retraite. Son patron, en Ehpad.", highlight=['retraite.', 'Ehpad.'])],
  'actors': [act('mec', SEAT, 0, 'sit', 'smug', keys=[k('SI1:sieste', clip='slumpDesk', expr='sleepy'), k('SI2:tard', clip='startle', expr='shocked'),
                                                       k('SI3', clip='lookAround', expr='worried')]),
             act('patron', [3.6, 0.12, -2.4], -20, 'sit', 'sleepy')],
  'props': [*office_props(), P('zzz', 'zzz', pos=[DESK[0] + 0.2, 1.2, SEAT[2]], visible=False, keys=[k('SI1:sieste', visible=True), k('SI2:tard', visible=False)]),
            P('barbe', 'beard', scale=0.05, opts={'color': '#E6E2D8'}, on=BEARD, keys=[k('SI2', scale=2.4, dur=1.6, ease='linear')]),
            P('toile1', 'spiderWeb', scale=0.05, pos=[DESK[0] - 0.75, 1.3, SEAT[2] + 0.1], opts={'r': 0.4}, keys=[k('SI2', scale=1, dur=1.6)]),
            P('toile2', 'spiderWeb', scale=0.05, pos=[DESK[0] + 0.7, 1.05, DESK[2] + 0.3], opts={'r': 0.3}, keys=[k('SI2', scale=1, dur=1.6)]),
            P('ehpad', 'signBoard', pos=[3.6, 0, -2.95], opts={'text': 'EHPAD', 'bg': '#F6F1E3', 'fg': '#2C4A8A', 'w': 0.9, 'h': 0.32, 'height': 1.75, 'posts': False}),
            P('fauteuil', 'sofaProp', scale=0.55, pos=[3.6, 0, -2.75], opts={'color': '#7A8C9A', 'color2': '#9AAAB8'}),
            P('patronBarbe', 'beard', scale=2.0, opts={'color': '#E6E2D8'}, on={'actor': 'patron', 'joint': 'head', 'offset': [0, 0.02, 0.1]})],
  'sfx': [{'at': 'SI1:sieste', 'name': 'tick', 'vol': 0.3}, {'at': 'SI2', 'name': 'ticks', 'vol': 0.5}, {'at': 'SI2:tard', 'name': 'gasp', 'vol': 0.6}],
  'cams': [FRONT(0), cam('SI2', 'mec', 'ms', angle=0, move='push', amount=0.05), FRONT('SI3', 56), POV('SI3:patron', [3.0, 1.6, -0.5], [3.6, 1.35, -2.6], 52)],
  'tail': 0.2,
})
scenes.append({
  'id': 'musee', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.5,
  'crowd': [{'id': 'visiteurs', 'count': 4, 'spec': {'preset': 'lemec_charcoal', 'seed': 91}, 'clip': 'stand', 'ry': 180,
             'positions': [[-1.9, 0, -0.7], [-2.7, 0, -1.3], [2.2, 0, -0.6], [3.0, 0, -1.2]]}],
  'lines': [L('SI4', "Le bureau était devenu un musée. Et ce mec, l'œuvre principale.", highlight=['musée.', "l'œuvre"]),
            L('SI5', "Alors ce con a porté plainte pour séquestration.", highlight=['plainte', 'séquestration.']),
            L('SI6', "Le musée a gagné. Il est classé monument historique.", highlight=['monument', 'historique.']),
            L('SI7', "Il n'a plus le droit de bouger. Ni de bâiller.", highlight=['bouger.', 'bâiller.']),
            L('SI8', "Les visiteurs paient quinze euros pour le voir dormir.", highlight=['quinze', 'dormir.']),
            L('SI9', "Hier, il a mis un réveil. Cinq minutes.", highlight=['réveil.', 'Cinq']),
            L('SI10', "Putain, il s'est rendormi.", highlight=['rendormi.'])],
  'actors': [act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k('SI5', clip='sitPoint', expr='angry'), k('SI7', clip='stiff', expr='scared'), k('SI7:bâiller', clip='yawnStretch', expr='sleepy'),
                                                             k('SI7.end', clip='sit', expr='unimpressed'), k('SI8', clip='slumpDesk', expr='sleepy'), k('SI9', clip='sit', expr='neutral'),
                                                             k('SI9:minutes', clip='slumpDesk', expr='sleepy')]),
             act('gardien', [2.2, 0, -1.6], -110, 'armsCrossed', 'unimpressed', keys=[k('SI7:bâiller', clip='whistleBlow', expr='angry', sfx='whistle'), k('SI7.end', clip='armsCrossed')])],
  'props': [*office_props(), P('barbe', 'beard', scale=2.4, opts={'color': '#E6E2D8'}, on=BEARD),
            P('cordon', 'stanchions', pos=[DESK[0], 0, DESK[2] + 0.95], opts={'w': 2.2}),
            P('plaque', 'signBoard', pos=[DESK[0] - 1.4, 0, DESK[2] + 0.9], ry=20, opts={'text': 'EMPLOYÉ DE BUREAU — 2026', 'bg': '#F6F1E3', 'fg': '#1E1E22', 'w': 0.9, 'h': 0.28, 'height': 0.95}),
            P('monument', 'signBoard', visible=False, pos=[DESK[0] + 1.3, 0, DESK[2] - 0.5], opts={'text': 'MONUMENT HISTORIQUE', 'bg': '#2C4A8A', 'fg': '#F6F1E3', 'w': 1.1, 'h': 0.34, 'height': 1.5},
              keys=[k('SI6:classé', visible=True)]),
            P('entree', 'signBoard', pos=[-2.6, 0, -1.4], ry=40, opts={'text': 'ENTRÉE 15 €', 'bg': '#F2C230', 'fg': '#1E1E22', 'w': 0.8, 'h': 0.3, 'height': 1.2}),
            P('reveil', 'alarmClock', scale=0.4, visible=False, pos=[DESK[0] + 0.45, 0.76, DESK[2] - 0.05], ry=180, opts={'time': '00:05'}, keys=[k('SI9', visible=True)]),
            P('zzz', 'zzz', pos=[DESK[0] + 0.2, 1.2, SEAT[2]], visible=False, keys=[k('SI8', visible=True), k('SI9', visible=False), k('SI10', visible=True)])],
  'sfx': [{'at': 'SI6:classé', 'name': 'gavel', 'vol': 0.5}, {'at': 'SI8:paient', 'name': 'cash', 'vol': 0.4}, {'at': 'SI8:dormir', 'name': 'shutter', 'vol': 0.5},
          {'at': 'SI9:réveil', 'name': 'click', 'vol': 0.5}, {'at': 'SI10:rendormi', 'name': 'shutter', 'vol': 0.5}],
  'cams': [POV(0, [DESK[0] + 1.2, 1.7, DESK[2] + 4.6], [DESK[0], 1.0, DESK[2]], 52),
           cam('SI5', 'mec', 'ms', angle=0),
           cam('SI6:classé', ['mec', 'monument'], 'ms', worldAngle=15, withProps=True),
           cam('SI7', ['mec', 'gardien'], 'ms', worldAngle=-15),
           POV('SI8', [DESK[0] + 1.2, 1.7, DESK[2] + 4.6], [DESK[0], 1.0, DESK[2]], 52),
           cam('SI9', 'mec', 'ms', angle=0),
           cam('SI10', 'mec', 'mcu', angle=0, move='push', amount=0.04)],
  'tail': 1.4,
})
write('sieste', 'La sieste', scenes, {'patron': {'preset': 'lemec_beige', 'seed': 33}, 'gardien': {'preset': 'cop', 'seed': 12}})
