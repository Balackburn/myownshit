#!/usr/bin/env python3
"""LE RÉVEIL. Ce mec buys a very powerful alarm clock to get up on time -> it rings -> the sun rises -> at 3 a.m. -> the
prefecture demands explanations -> ce con presses snooze -> night falls -> it has been night for nine minutes -> for three
years (beard, cobwebs, the clock still says 03:09). (Classic formula, no news gags.)"""
from actu_common import *

ROOM = {'poster': 'BONJOUR\nSOLEIL', 'posterBg': '#F2C230', 'posterFg': '#B5302A'}
BED_LIE = [-2.6, 0.64, -1.9]                     # chambre: single bed along z, headboard at the back wall
NS = [-1.72, 0, -2.6]                            # nightstand by the pillow
CLOCK = [NS[0], 0.55, NS[2]]
AT_NS = [-1.15, 0, -2.55]                        # standing at the nightstand, facing the clock (ry -90: a profile from the front)
NS_RY = -90
CLOCK_RY = 20
BEARD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.02, 0.1]}
BED_POV = lambda at: POV(at, [-1.5, 2.2, -0.9], [-2.5, 0.75, -2.5], 52)
CLOCK_POV = lambda at, fov=44: POV(at, [CLOCK[0] + 0.95 * 0.342, 0.82, CLOCK[2] + 0.95 * 0.94], [CLOCK[0], 0.78, CLOCK[2]], fov)
NIGHT = 'brightness(0.62) saturate(0.75) contrast(1.1)'
SUNNY = 'brightness(1.28) saturate(1.15) contrast(1.05)'
def nightstand(): return P('chevet', 'table', pos=NS, opts={'w': 0.5, 'd': 0.42, 'h': 0.55, 'color': '#C9A06A'})
def clock(time, **kw): return P('reveil', 'alarmClock', pos=CLOCK, ry=CLOCK_RY, opts={'time': time, **kw})
scenes = []
scenes.append({
  'id': 'nuit', 'set': 'chambre', 'setOpts': ROOM, 'lighting': 'night', 'ambience': 'night', 'ambienceVol': 0.35,
  'lines': [L('W1', "Ce mec a acheté un réveil très puissant pour se lever à l'heure.", highlight=['réveil', 'puissant']),
            L('W2', "Il a sonné.", highlight=['sonné.'])],
  'actors': [act('mec', AT_NS, NS_RY, 'stand', 'happy', keys=[k(0.25, clip='giveItem', expr='happy'), k('W1:lever', visible=False)]),
             act('mecLit', BED_LIE, 0, 'lieBack', 'sleepy', visible=False, keys=[k('W1:lever', visible=True), k('W2:sonné', expr='shocked')])],
  'props': [nightstand(), clock('23:00', time2='03:00', switchAt='W2-0.2', ringAt='W2:sonné'),
            P('zzz', 'zzz', visible=False, pos=[-2.45, 1.0, -2.55], keys=[k('W1:lever', visible=True), k('W2:sonné', visible=False)])],
  'sfx': [{'at': 'W1:réveil', 'name': 'click', 'vol': 0.4}, {'at': 'W2:sonné', 'name': 'ring', 'vol': 0.9}, {'at': 'W2:sonné+0.6', 'name': 'ring', 'vol': 0.9}],
  'cams': [cam(0, ['mec', 'reveil'], 'ms', worldAngle=15, withProps=True),
           CLOCK_POV('W1:puissant'),
           BED_POV('W1:lever'),
           CLOCK_POV('W2')],
  'tail': 0.2,
})
scenes.append({
  'id': 'soleil', 'set': 'pavillon', 'ambience': 'park', 'ambienceVol': 0.3,
  'daynight': {'from': 'W3:soleil', 'period': 1.8, 'rise': True},
  'lines': [L('W3', "Le soleil s'est levé.", highlight=['soleil'])],
  'actors': [],
  'props': [P('soleil', 'sun', pos=[1.6, -5.0, -16], opts={'r': 3.2}, keys=[k('W3:soleil', to=[1.6, 7.6, -16], dur=1.1, ease='out')])],
  'sfx': [{'at': 'W3:soleil', 'name': 'choir', 'vol': 0.6}],
  'cams': [POV(0, [0, 1.5, 7.5], [0.6, 3.6, -8], 62)],
  'tail': 0.1,
})
scenes.append({
  'id': 'trois_h', 'set': 'chambre', 'setOpts': ROOM, 'lighting': 'day', 'grade': SUNNY, 'ambience': None,
  'lines': [L('W4', "À trois heures du matin.", highlight=['trois', 'matin.'])],
  'actors': [act('mecLit', BED_LIE, 0, 'lieBack', 'shocked', keys=[k('W4:matin', expr='sleepy')])],
  'props': [nightstand(), clock('03:00')],
  'sfx': [{'at': 'W4:trois', 'name': 'tick', 'vol': 0.5}],
  'cams': [CLOCK_POV(0, 40),
           BED_POV('W4:matin')],
  'tail': 0.2,
})
scenes.append({
  'id': 'prefecture', 'set': 'pressRoom', 'setOpts': {'backdrop': 'PRÉFECTURE', 'fontScale': 1.0}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('W5', "La préfecture a exigé des explications.", highlight=['préfecture', 'explications.'])],
  'actors': [act('prefet', PR_SPEAKER, 0, 'podiumTalk', 'angry', keys=[k('W5:exigé', clip='slamTable', expr='angry'), k('W5:explications', clip='point', expr='angry')])],
  'props': [],
  'sfx': [{'at': 'W5:préfecture', 'name': 'shutter', 'vol': 0.4}, {'at': 'W5:exigé+0.15', 'name': 'thud', 'vol': 0.6}, {'at': 'W5:explications', 'name': 'shutter', 'vol': 0.4}],
  'cams': [POV(0, [0, 1.6, 0.9], [0, 1.45, -2.45], 42),
           cam('W5:explications', 'prefet', 'cu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'snooze', 'set': 'chambre', 'setOpts': ROOM, 'ambience': None,
  'daynight': {'from': 'W6:snooze', 'period': 0.7, 'once': True},
  'lines': [L('W6', "Alors ce con a appuyé sur snooze.", highlight=['snooze.']),
            L('W7', "Putain.", pre=0.3),
            L('W8', "Il fait nuit depuis neuf minutes.", highlight=['nuit', 'neuf'])],
  'actors': [act('mec', AT_NS, NS_RY, 'stand', 'angry', keys=[k('W6:appuyé', clip='slamTable', expr='angry'), k('W6:snooze+0.2', clip='stand', expr='unimpressed'),
                                                             k('W7', face=0, turn=0.25, clip='stareCamera', expr='unimpressed')])],
  'props': [nightstand(), clock('03:00', time2='03:09', switchAt='W8', ringAt=0, stopAt='W6:snooze')],
  'sfx': [{'at': 0, 'name': 'ring', 'vol': 0.7}, {'at': 0.7, 'name': 'ring', 'vol': 0.7}, {'at': 'W6:appuyé', 'name': 'ring', 'vol': 0.7},
          {'at': 'W6:snooze', 'name': 'click', 'vol': 0.7}, {'at': 'W6:snooze', 'name': 'punch', 'vol': 0.5}, {'at': 'W6:snooze+0.5', 'name': 'crickets', 'vol': 0.4}],
  'cams': [cam(0, ['mec', 'reveil'], 'ms', worldAngle=15, withProps=True),
           {**cam('W7', 'mec', 'cu', angle=0), 'grade': NIGHT},
           {**CLOCK_POV('W8', 40), 'grade': NIGHT}],
  'tail': 0.3,
})
scenes.append({
  'id': 'trois_ans', 'set': 'chambre', 'setOpts': ROOM, 'lighting': 'night', 'grade': 'sepia(0.25) brightness(0.92) contrast(1.05)', 'ambience': 'night', 'ambienceVol': 0.35,
  'lines': [L('W9', "Ça fait trois ans.", pre=0.4, highlight=['trois', 'ans.'])],
  'actors': [act('mec', AT_NS, NS_RY, 'stand', 'unimpressed', keys=[k('W9:trois', face=0, turn=0.35, clip='stareCamera', expr='unimpressed')])],
  'props': [nightstand(), clock('03:09'),
            P('barbe', 'beard', scale=2.3, opts={'color': '#E6E2D8'}, on=BEARD),
            P('toile1', 'spiderWeb', pos=[-1.42, 0.98, -2.42], opts={'r': 0.3}),
            P('toile2', 'spiderWeb', pos=[-3.6, 2.6, -2.97], opts={'r': 0.7}),
            P('toile3', 'spiderWeb', pos=[-0.95, 1.95, -2.75], opts={'r': 0.35}),
            P('toile4', 'spiderWeb', pos=[-1.15, 0.55, -2.32], opts={'r': 0.22})],
  'sfx': [{'at': 0, 'name': 'crickets', 'vol': 0.35}],
  'cams': [cam(0, ['mec', 'reveil'], 'ms', worldAngle=15, withProps=True),
           cam('W9:ans', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('reveil', 'Le réveil', scenes, {'mec': {'preset': 'mecPyjama'}, 'mecLit': {'preset': 'mecPyjama'}, 'prefet': {'preset': 'prefet'}})
