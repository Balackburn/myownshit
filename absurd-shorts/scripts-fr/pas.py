#!/usr/bin/env python3
"""LES DIX MILLE PAS. Written with the viral-video-writing loop (5 hooks, 3 drafts, score_fr.py 100/100):
hook with a number (10 000 steps) -> the doubter at 4 s (the doctor: "you won't last a week") -> the promise (straight ahead,
never turns) -> re-hooks every few seconds (a week: Poland, a month: Siberia, the ocean, the Sécu) -> three years later he
comes home over the roof -> callback (the doctor is waiting) -> the counter says 9 999 -> loop: he leaves again, over the roof."""
from actu_common import *

BEARD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.02, 0.1]}
def beard(sc, col='#3A2E26'): return P('barbe', 'beard', scale=sc, opts={'color': col}, on=BEARD)
def podo(**o): return P('podo', 'pedometer', scale=1.3, opts=o, on={'actor': 'mec', 'hand': 'R', **HAND_FLAT})
WALK_Z = 0.3
def stroll(x0, x1, dur, z=WALK_Z, extra=()):
    """the mec walking straight along +x, already moving on frame 0"""
    return act('mec', [x0, 0, z], 90, 'walk', 'neutral', keys=[k(0, to=[x1, 0, z], glide=True, dur=dur, clip='walk', then='walk', face='keep'), *extra])
scenes = []
scenes.append({
  'id': 'cabinet', 'set': 'hospital', 'ambience': 'office', 'ambienceVol': 0.4,
  'lines': [L('S1', "Ce mec a voulu faire dix mille pas par jour pour rester en forme.", highlight=['dix', 'mille']),
            L('S2', "Vous tiendrez pas une semaine.", 'medecin')],
  'actors': [act('mec', [1.3, 0, -1.0], -35, 'walk', 'grin', keys=[k('S2', clip='stand', expr='neutral')]),
             act('medecin', [0.2, 0, -2.0], 25, 'armsCrossed', 'unimpressed', keys=[k('S2', clip='point', expr='smug')])],
  'props': [podo(countAt=0.3, rate=3.2, start=0)],
  'sfx': [{'at': 0.3, 'name': 'step', 'vol': 0.35}, {'at': 0.75, 'name': 'step', 'vol': 0.35}, {'at': 1.2, 'name': 'step', 'vol': 0.35}, {'at': 1.65, 'name': 'step', 'vol': 0.35},
          {'at': 'S1:pas', 'name': 'beep', 'vol': 0.3}],
  'cams': [cam(0, ['mec', 'medecin'], 'ms', worldAngle=10),
           cam('S1:rester', 'mec', 'mcu', angle=10),
           cam('S2', 'medecin', 'cu', angle=0)],
  'tail': 0.2,
})
# straight ahead: over the car parked on the pavement, never around it
CAR_X = 0.0
OVER = [[CAR_X - 2.35, 0, WALK_Z], [CAR_X - 2.05, 0.92, WALK_Z], [CAR_X - 1.55, 2.07, WALK_Z], [CAR_X + 0.9, 2.07, WALK_Z], [CAR_X + 1.75, 0.92, WALK_Z], [CAR_X + 2.3, 0, WALK_Z], [CAR_X + 7.0, 0, WALK_Z]]
scenes.append({
  'id': 'tout_droit', 'set': 'street', 'ambience': 'street', 'ambienceVol': 0.5,
  'lines': [L('S3', "Alors ce con est parti tout droit et il n'a jamais tourné.", highlight=['droit', 'jamais'])],
  'actors': [act('mec', [CAR_X - 5.0, 0, WALK_Z], 90, 'walk', 'neutral', keys=[k(0, path=OVER, clip='walk', speed=1.6, then='walk', face='keep')])],
  'props': [P('voiture', 'car', pos=[CAR_X, 0, WALK_Z + 0.05], opts={'color': '#5E8C7A', 'plate': 'TROTTOIR'}), podo(value=4)],
  'sfx': [{'at': 'S3:droit', 'name': 'thud', 'vol': 0.4}, {'at': 'S3:jamais', 'name': 'thud', 'vol': 0.4}],
  'cams': [cam(0, 'mec', 'fs', worldAngle=12, move='track')],
  'tail': 0.15,
})
scenes.append({
  'id': 'pologne', 'set': 'farm', 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('S4', "Une semaine plus tard, il était en Pologne.", highlight=['Pologne.'])],
  'actors': [stroll(-3.2, 3.6, 2.6)],
  'props': [P('panneau', 'signBoard', pos=[0.8, 0, -0.75], opts={'text': 'POLSKA', 'bg': '#1C3F94', 'fg': '#F2C230', 'w': 1.2, 'h': 0.5, 'height': 1.3, 'frame': '#1C3F94'}),
            beard(0.8), podo(value='70 312')],
  'cams': [cam(0, 'mec', 'fs', worldAngle=15, move='track')],
  'tail': 0.15,
})
scenes.append({
  'id': 'siberie', 'set': 'snow', 'ambience': 'wind', 'ambienceVol': 0.5,
  'lines': [L('S5', "Un mois plus tard, en Sibérie.", highlight=['Sibérie.'])],
  'actors': [stroll(-2.8, 3.2, 2.2, extra=[k(0, expr='sad')])],
  'props': [P('panneau', 'signBoard', pos=[0.6, 0, -0.75], opts={'text': 'SIBÉRIE', 'bg': '#7A5A3A', 'fg': '#F6F1E3', 'w': 1.2, 'h': 0.45, 'height': 1.2, 'frame': '#5A3A2A'}),
            beard(1.3), podo(value='9 999')],
  'sfx': [{'at': 0, 'name': 'wind', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'fs', worldAngle=-15, move='track')],
  'tail': 0.15,
})
SEA = [[0.8, 0, -1.2], [0.2, 0, -6.6], [-0.4, -0.9, -8.8], [-1.0, -2.7, -11.6]]
scenes.append({
  'id': 'ocean', 'set': 'beach', 'ambience': 'beach', 'ambienceVol': 0.6,
  'lines': [L('S6', "Puis il y a eu l'océan. Il a continué par en dessous.", highlight=['océan.', 'dessous.'])],
  'actors': [act('mec', SEA[0], 180, 'walk', 'neutral', keys=[k(0, path=SEA[1:], clip='walk', speed=1.3, then='walk', face='keep')])],
  'props': [beard(1.5), P('bulles', 'dustPuff', scale=0.5, visible=False, pos=[-1.0, 0.0, -11.2], opts={'color': '#EAF7FA', 'once': True, 'period': 1.2, 'startAt': 'S6:dessous'},
                          keys=[k('S6:dessous', visible=True)])],
  'sfx': [{'at': 'S6:océan', 'name': 'splash', 'vol': 0.5}, {'at': 'S6:dessous', 'name': 'gulp', 'vol': 0.5}, {'at': 'S6:dessous+0.3', 'name': 'pop', 'vol': 0.35}, {'at': 'S6:dessous+0.6', 'name': 'pop', 'vol': 0.35}],
  'cams': [POV(0, [5.6, 1.7, 3.6], [-0.2, 0.4, -6.4], 55)],
  'tail': 0.15,
})
DOS = [0, 1.115, -2.15]
scenes.append({
  'id': 'secu', 'set': 'poste', 'setOpts': {'title': 'SÉCURITÉ SOCIALE'}, 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('S7', "Pendant ce temps, la Sécu l'a radié pour absence prolongée.", highlight=['radié', 'prolongée.'])],
  'actors': [act('agent', [0, 0, -2.85], 0, 'idle', 'unimpressed', keys=[k('S7:radié-0.2', clip='slamTable', expr='unimpressed')])],
  'props': [P('dossier', 'bill', scale=2.2, pos=DOS, rot=[-1.5708, 0, 0], opts={'title': 'DOSSIER 1 85 07', 'items': [['Absent depuis', '2 ans'], ['Pas', '7 300 000'], ['', '']], 'total': '0,00 €'}),
            P('tampon', 'stampMark', visible=False, pos=[DOS[0] + 0.02, DOS[1] + 0.006, DOS[2] - 0.03], rot=[-1.5708, 0, 0.25], opts={'text': 'RADIÉ', 'w': 0.28, 'h': 0.1},
              keys=[k('S7:radié', visible=True)]),
            P('encreur', 'rubberStamp', on={'actor': 'agent', 'hand': 'R'})],
  'sfx': [{'at': 'S7:radié', 'name': 'thud', 'vol': 0.7}, {'at': 'S7:Sécu', 'name': 'paper', 'vol': 0.4}],
  'cams': [cam(0, 'agent', 'ms', angle=0),
           POV('S7:radié-0.35', [0, 1.62, -1.9], DOS, 36)],
  'tail': 0.2,
})
# home, three years later: over the roof from behind, down the front, to the doctor waiting at the door
RX = -1.2
ROOF_IN = [[RX, 4.4, -6.6], [RX, 2.9, -3.85], [RX, 0, -3.3], [0.0, 0, -3.15]]
ROOF_OUT = [[0.0, 0, -3.6], [0.0, 2.9, -3.9], [0.0, 4.4, -6.6], [0.0, 2.9, -9.4], [0.0, 0, -9.8]]
FRONT = lambda at: POV(at, [0.4, 2.0, 6.5], [0, 2.4, -5.0], 58)
scenes.append({
  'id': 'retour', 'set': 'pavillon', 'ambience': 'park', 'ambienceVol': 0.45,
  'lines': [L('S8', "Trois ans plus tard, il est revenu chez lui. Par l'autre côté.", highlight=['Trois', 'côté.']),
            L('S9', "Son médecin l'attendait devant la porte.", highlight=['médecin']),
            L('S10', "Putain, le podomètre affichait neuf mille neuf cent quatre-vingt-dix-neuf pas.", highlight=['quatre-vingt-dix-neuf']),
            L('S11', "Il est reparti faire le dernier pas.", highlight=['dernier'])],
  'actors': [act('mec', [RX, 2.9, -9.35], 0, 'walk', 'neutral', keys=[
                 k('S8+0.3', to=ROOF_IN[0], glide=True, dur=1.9, clip='walk', then='walk', face='keep'),
                 k('S8:côté', path=ROOF_IN[1:], clip='walk', speed=2.8, then='stand', face='keep', faceEnd=90),
                 k('S10', face=10, turn=0.25, clip='showPhone', expr='unimpressed'),
                 k('S11', face=180, turn=0.3, clip='stand'),
                 k('S11+0.3', path=ROOF_OUT, clip='walk', speed=1.4, then='walk', face='keep')]),
             act('medecin', [1.0, 0, -3.5], -90, 'armsCrossed', 'unimpressed', keys=[k('S10:neuf', clip='lookItem', expr='shocked'), k('S11:dernier', clip='facepalm')])],
  'props': [beard(2.6, '#E6E2D8'), podo(value='9 999')],
  'sfx': [{'at': 'S8:côté', 'name': 'step', 'vol': 0.4}, {'at': 'S9', 'name': 'step', 'vol': 0.4}, {'at': 'S10:neuf', 'name': 'beep', 'vol': 0.5}, {'at': 'S11:dernier', 'name': 'step', 'vol': 0.4}],
  'cams': [FRONT(0),
           cam('S9', ['mec', 'medecin'], 'ms', worldAngle=5),
           cam('S10', 'mec', 'mcu', angle=0),
           cam('S10:neuf', 'podo', 'cu', worldAngle=10, noOcclusion=True),
           cam('S11', ['mec', 'medecin'], 'ms', worldAngle=10),
           FRONT('S11+0.9')],
  'tail': 1.4,
})

write('pas', 'Les dix mille pas', scenes, {'medecin': {'preset': 'doctor'}, 'agent': {'preset': 'madame', 'seed': 44, 'glasses': True}})
