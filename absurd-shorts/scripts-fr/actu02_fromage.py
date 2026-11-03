#!/usr/bin/env python3
"""ACTU 02 — LE FROMAGE. He sticks a meme of himself as Mao on his fridge -> next morning his milk, his soda and his
cheese hop out of the fridge and leave, like Mbappé's sponsors -> Mbappé apologises on TV in three languages -> he
apologises in twelve (the Chinese people, the Chinese government, then the cheese) -> the cheese has no opinion on
Chinese history -> he calls the cops (motif: abandon de produits laitiers) -> they arrest the cheese, and him ->
"Votre mème préféré ?" -> in the cell only the bread is left, and the bread is on strike."""
from actu_common import *

def hops(start, end, anchor, off, n=5, step=0.42, h=0.3):
    """a prop hopping from start to end in n hops, starting at anchor+off"""
    out = []
    for i in range(1, n + 1):
        f = i / n
        p = [start[j] + (end[j] - start[j]) * f for j in range(3)]
        out.append(k(f"{anchor}{off + (i - 1) * step:+.2f}", to=p, dur=step * 0.92, arc=h, ease='inOut'))
    return out

scenes = []
FR = (-2.7, 0, -3.22)
DOOR = [2.8, 0, -3.35]
scenes.append({
  'id': 'frigo', 'set': 'kitchenNight', 'setOpts': {'fridge': False}, 'lighting': 'interior', 'ambience': None,
  'lines': [L('F1', "Ce mec a collé un mème de lui en Mao sur son frigo.", highlight=['Mao']),
            L('F2', "Le lendemain, son lait, son soda et son fromage sont partis.", highlight=['partis.']),
            L('F3', "Comme les sponsors de Mbappé.", highlight=['Mbappé.'])],
  'actors': [
    act('mec', [-2.15, 0, -2.25], -160, 'giveItem', 'smug', keys=[
        k('F1:Mao', to=[-1.2, 0, -1.7], clip='walk', speed=1.5, faceEnd=-150, then='handsOnHips', expr='smug'),
        k('F2:lait', expr='shocked', clip='startle', face=-130, turn=0.15),
        k('F2:fromage', clip='scared', face=60, turn=0.25),
        k('F3', clip='stareCamera', expr='sad', face=0, turn=0.2)]),
  ],
  'props': [P('frigo', 'fridge', pos=list(FR), opts={'notes': 7, 'openAt': 'F2-0.25'}),
            P('meme', 'memePoster', scale=0.5, pos=[-2.55, 1.32, -2.77], opts={'text': 'MÈME', 'skin': '#D9A877'},
              keys=[k('F2-0.2', to=[-2.4, 0.22, -2.62], dur=0.45, ease='in', sfx='paper')]),
            P('lait', 'milkCarton', scale=1.3, pos=[-2.95, 1.365, -3.0], keys=hops([-2.95, 1.365, -3.0], [-1.6, 0, -2.0], 'F2:lait', -0.1, n=2, h=0.25) + hops([-1.6, 0, -2.0], DOOR, 'F2:lait', 0.75, n=6) + [k('F2:lait+3.4', visible=False)]),
            P('soda', 'drinkCan', scale=1.5, pos=[-2.45, 1.365, -3.0], opts={'color': '#C23A2E', 'text': 'SODA'}, keys=hops([-2.45, 1.365, -3.0], [-1.3, 0, -2.3], 'F2:soda', -0.1, n=2, h=0.25) + hops([-1.3, 0, -2.3], DOOR, 'F2:soda', 0.75, n=6) + [k('F2:soda+3.4', visible=False)]),
            P('fromage', 'cheeseWheel', scale=1.1, pos=[-2.7, 0.565, -3.0], keys=hops([-2.7, 0.565, -3.0], [-1.9, 0, -1.6], 'F2:fromage', -0.1, n=2, h=0.25) + hops([-1.9, 0, -1.6], DOOR, 'F2:fromage', 0.75, n=7) + [k('F2:fromage+3.8', visible=False)])],
  'cams': [cam(0, 'mec', 'ms', worldAngle=90),
           cam('F1:sur', [[-2.55, 1.32, -2.77]], 'cu', worldAngle=0, noOcclusion=True),
           cam('F2', [[-2.7, 1.0, -2.9]], 'ms', worldAngle=25),
           cam('F2:soda', 'fromage', 'fs', worldAngle=20, move='track'),
           cam('F3', 'mec', 'ms', worldAngle=-25)],
  'tail': 0.2,
})

scenes.append({
  'id': 'tele', 'set': 'pressRoom', 'setOpts': {'backdrop': 'PARDON|SORRY|LO SIENTO|SCUSATE|ENTSCHULDIGUNG|DESCULPA|EXCUSES'}, 'ambience': 'station',
  'crowd': [journalists()],
  'lines': [L('F4', "À la télé, Mbappé s'excusait en trois langues.", highlight=['trois', 'langues.'])],
  'actors': [act('mbappe', PR_SPEAKER, 0, 'podiumTalk', 'sad', keys=[k('F4:excusait', clip='bowRepeat', params={'freq': 1.6})])],
  'sfx': [{'at': 'F4', 'name': 'shutter', 'vol': 0.5}, {'at': 'F4:trois', 'name': 'shutter', 'vol': 0.5}],
  'cams': [cam(0, 'mbappe', 'ms', angle=0),
           cam('F4:trois', 'mbappe', 'fs', worldAngle=10, elev=8)],
  'tail': 0.2,
})

CH = [0.9, 0, 0.6]
scenes.append({
  'id': 'rue', 'set': 'street', 'ambience': 'street',
  'lines': [L('F5', "Alors ce con s'est excusé en douze langues. Au peuple chinois, au gouvernement chinois, puis au fromage.", highlight=['douze', 'fromage.']),
            L('F6', "Le fromage n'avait pas d'avis sur l'histoire chinoise.", highlight=['avis']),
            L('F7', "Il a appelé les flics. Motif : abandon de produits laitiers.", highlight=['Motif', 'laitiers.']),
            L('F8', "Les flics ont embarqué le fromage. Et ce mec, pour complicité.", highlight=['complicité.'])],
  'actors': [
    act('mec', [-0.1, 0, 0.6], 90, 'bowRepeat', 'sad', keys=[
        k('F5:peuple', face=0, turn=0.15, clip='bowRepeat', params={'freq': 1.8}),
        k('F5:gouvernement', face=60, turn=0.15),
        k('F5:fromage', face='fromage', turn=0.15),
        k('F6', clip='stand', expr='unimpressed'),
        k('F7', clip='phoneCall', expr='angry', face=-20, turn=0.2),
        k('F8:mec', clip='handcuffed', expr='shocked')]),
    act('flic1', [7.5, 0, 1.2], -90, 'idle', 'angry', keys=[k('F8', path=[[3.5, 0, 1.1], [1.55, 0, 0.75]], clip='run', speed=4.2, faceEnd='fromage', then='cuffOther')]),
    act('flic2', [8.2, 0, 0.3], -90, 'idle', 'angry', keys=[k('F8+0.15', path=[[3.0, 0, 0.0], [0.4, 0, 0.25]], clip='run', speed=4.4, faceEnd='mec', then='cuffOther')]),
  ],
  'props': [P('fromage', 'cheeseWheel', scale=1.1, pos=list(CH), keys=hops(CH, [1.75, 0, 0.6], 'F6:avis', 0.0, n=2, h=0.2) + [k('F8:fromage', attach='flic1', hand='R', offset=[0, -0.12, 0.1])]),
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('F7', visible=True), k('F8', visible=False)]),
            P('cuffs', 'handcuffs', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('F8:mec', visible=True)])],
  'sfx': [{'at': 'F8-0.3', 'name': 'siren', 'vol': 0.45}, {'at': 'F8:mec', 'name': 'cuff', 'vol': 0.6}],
  'cams': [cam(0, 'mec', 'ms', angle=30),
           cam('F5:peuple', 'mec', 'ms', angle=0),
           cam('F5:gouvernement', 'mec', 'ms', angle=10),
           cam('F5:fromage', ['mec', 'fromage'], 'ms', worldAngle=0),
           cam('F6', 'fromage', 'cu', worldAngle=10),
           cam('F7', 'mec', 'cu', angle=-35),
           cam('F7:abandon', 'fromage', 'cu', worldAngle=10),
           cam('F8:fromage', ['flic1', 'flic2', 'mec'], 'ms', worldAngle=10, elev=6)],
  'tail': 0.2,
})

scenes.append({
  'id': 'gav', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('F9', "Votre mème préféré ?", 'commissaire'),
            L('F10', "Celui en Mao.", 'mec', highlight=['Mao.']),
            L('F11', "Mauvaise réponse. Quarante-huit heures.", 'commissaire', highlight=['Mauvaise', 'réponse.'])],
  'actors': [
    act('mec', IR_SUSPECT, 0, 'sitCuffed', 'sad', keys=[k('F10', expr='happy')]),
    act('commissaire', IR_COP, -90, 'leanTable', 'suspicious', keys=[k('F11', clip='slamTable', expr='angry', sfx='thud', sfxAt=0.12)]),
  ],
  'props': [P('fromage', 'cheeseWheel', scale=1.1, pos=[-0.45, 0.785, -0.62])],
  'cams': [cam(0, ['commissaire', 'mec'], 'fs', worldAngle=10, elev=10),
           cam('F10', 'mec', 'cu', angle=0),
           cam('F11', 'commissaire', 'mcu', angle=60)],
  'tail': 0.2,
})

scenes.append({
  'id': 'cellule', 'set': 'prisonCell', 'ambience': None,
  'lines': [L('F12', "En cellule, il ne lui restait que le pain.", highlight=['pain.']),
            L('F13', "Et le pain était en grève.", highlight=['grève.'])],
  'actors': [act('mec', [2.0, 0.24, -2.3], 0, 'sit', 'sad', keys=[k('F13', clip='stareCamera', expr='unimpressed')])],
  'props': [P('pain', 'baguette', scale=1.2, pos=[1.25, 0, -1.7]),
            P('greve', 'protestSign', scale=0.3, pos=[1.3, 0, -1.88], opts={'text': 'GRÈVE', 'color': '#B3261E'})],
  'cams': [cam(0, 'mec', 'ms', worldAngle=-20),
           cam('F13', [[1.28, 0.2, -1.8]], 'cu', worldAngle=0, elev=12, noOcclusion=True),
           cam('F13.end', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu02_fromage', 'Le fromage', scenes, {'mbappe': {'preset': 'footballeur'}})
