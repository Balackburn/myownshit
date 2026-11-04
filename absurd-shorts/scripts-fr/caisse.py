#!/usr/bin/env python3
"""LA CAISSE AUTOMATIQUE (viral-video-writing loop, score_fr.py 100/100). Hook with a number (five minutes) -> the villain at
4 s (the machine: "Article inattendu...") -> he IS the item -> scanned, 4,99 € -> sold to a granny -> the police check the
receipt -> low point: three years in her china cabinet -> expired, refunded as a voucher -> loop: the same alert, same kiosk."""
from actu_common import *

SC = [-0.8, 0, 0.2]                                   # self-checkout kiosk (faces +z); its bagging scale is 0.95 m to the right
SCALE_TOP = [SC[0] + 0.95, 0.2, SC[2] + 0.12]
FOREHEAD = {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.47, 0.105]}
SCREEN_POV = lambda at: POV(at, [SC[0], 1.56, SC[2] + 0.62], [SC[0], 1.42, SC[2] + 0.13], 34)
TICKET = {'title': 'TICKET DE CAISSE', 'items': [['Yaourts x2', '1,80'], ['Ce mec', '4,99'], ['', '']], 'total': '6,79 €'}
scenes = []
scenes.append({
  'id': 'caisse', 'set': 'supermarket', 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('CA1', "Ce mec a pris la caisse automatique pour gagner cinq minutes.", highlight=['automatique', 'cinq']),
            L('CA2', "Article inattendu dans la zone d'ensachage.", 'caisse'),
            L('CA3', "L'article, c'était lui.", highlight=['lui.']),
            L('CA4', "Alors la machine l'a scanné. Quatre euros quatre-vingt-dix-neuf.", highlight=['scanné.', 'quatre-vingt-dix-neuf.']),
            L('CA5', "Une mamie l'a acheté avec deux yaourts.", highlight=['mamie', 'yaourts.'])],
  'actors': [act('mec', [SC[0], 0, SC[2] + 0.68], 180, 'holdOut', 'happy', keys=[
                 k('CA1:minutes', to=SCALE_TOP, glide=True, dur=0.3, face=0, clip='sitFloor', then='sitFloor', expr='smug'),
                 k('CA2', expr='shocked'), k('CA3:lui', expr='unimpressed'), k('CA4:scanné', expr='shocked'),
                 k('CA5', to=[SC[0] + 1.25, 0, SC[2] + 0.75], glide=True, dur=0.05, face=90, clip='stand', then='stand', expr='sad'),
                 k('CA5:yaourts', to=[5.5, 0, SC[2] + 0.9], clip='walk', speed=1.4, then='walk', face='keep')]),
             act('mamie', [6.0, 0, SC[2] + 0.9], -90, 'idle', 'happy', keys=[k('CA5-0.6', to=[SC[0] + 2.0, 0, SC[2] + 0.8], clip='walk', speed=2.6, faceEnd=-90, then='giveItem'),
                                                                          k('CA5:yaourts', to=[6.5, 0, SC[2] + 0.9], clip='walk', speed=1.4, then='walk', face='keep')])],
  'props': [P('borne', 'selfCheckout', pos=SC, opts={'alertAt': 'CA2', 'alertEndAt': 'CA5'}),
            P('yaourt', 'yogurt', on={'actor': 'mec', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]}, keys=[k('CA1:minutes', visible=False)]),
            P('prix', 'priceTag', scale=0.8, visible=False, opts={'text': '4,99 €'}, on=FOREHEAD, keys=[k('CA4:Quatre', visible=True)]),
            P('laser', 'beerStream', visible=False, pos=[SCALE_TOP[0], 1.9, SCALE_TOP[2] + 0.35], rot=[0, 0, 1.5708], opts={'length': 1.1, 'r': 0.012, 'flare': 1, 'color': '#FF2A1A'},
              keys=[k('CA4:scanné-0.2', visible=True), k('CA4:scanné-0.2', to=[SCALE_TOP[0], 0.25, SCALE_TOP[2] + 0.35], dur=0.7, ease='linear'), k('CA4:Quatre', visible=False)]),
            P('panier', 'yogurt', scale=1.2, on={'actor': 'mamie', 'hand': 'L', 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]})],
  'sfx': [{'at': 'CA1:caisse', 'name': 'beep', 'vol': 0.4}, {'at': 'CA2', 'name': 'beep', 'vol': 0.5}, {'at': 'CA2+0.35', 'name': 'beep', 'vol': 0.5},
          {'at': 'CA4:scanné', 'name': 'beep', 'vol': 0.6}, {'at': 'CA5:acheté', 'name': 'cash', 'vol': 0.5}],
  'cams': [POV(0, [SC[0] - 0.35, 1.62, SC[2] - 0.95], [SC[0], 1.45, SC[2] + 0.68], 52),
           cam('CA1:minutes', 'mec', 'ms', worldAngle=10),
           SCREEN_POV('CA2'),
           cam('CA3', 'mec', 'ms', worldAngle=10, move='push', amount=0.05),
           cam('CA4', 'mec', 'ms', worldAngle=25),
           cam('CA4:Quatre', 'mec', 'cu', worldAngle=10),
           cam('CA5', ['mamie', 'mec'], 'ms', worldAngle=15)],
  'tail': 0.2,
})
VIT = [-2.2, 0, -3.28]
scenes.append({
  'id': 'salon', 'set': 'livingRoom', 'ambience': None,
  'lines': [L('CA6', "Alors ce con a appelé les flics pour séquestration.", highlight=['flics', 'séquestration.']),
            L('CA7', "Les flics ont vérifié le ticket. Tout était en règle.", highlight=['ticket.', 'règle.']),
            L('CA8', "Depuis trois ans, il vit dans son buffet, entre les assiettes.", highlight=['trois', 'buffet,'])],
  'actors': [act('mec', [0.9, 0, -1.2], -20, 'phoneCall', 'angry', keys=[k('CA7', clip='stand', expr='shocked'), k('CA8', visible=False)]),
             act('mecV', [VIT[0], 0.08, VIT[2]], 0, 'stand', 'unimpressed', visible=False, keys=[k('CA8', visible=True)]),
             act('mamie', [-0.3, 0.17, -2.85], 0, 'sit', 'smug'),
             act('flic1', [3.2, 0, -0.6], -90, 'idle', 'neutral', keys=[k('CA7-0.5', to=[1.9, 0, -0.9], clip='walk', speed=2.6, faceEnd=-30, then='showPhone')])],
  'props': [P('tel', 'phone911', on={'actor': 'mec', 'hand': 'R'}, keys=[k('CA7', visible=False)]),
            P('prix', 'priceTag', scale=0.8, opts={'text': '4,99 €'}, on=FOREHEAD),
            P('prixV', 'priceTag', scale=0.8, opts={'text': '4,99 €'}, on={**FOREHEAD, 'actor': 'mecV'}),
            P('ticket', 'bill', scale=1.7, opts=TICKET, on={'actor': 'flic1', 'hand': 'R', **HAND_FLAT}),
            P('vitrine', 'vitrine', pos=VIT)],
  'sfx': [{'at': 'CA7:ticket', 'name': 'paper', 'vol': 0.5}, {'at': 'CA7:règle', 'name': 'ding', 'vol': 0.4}],
  'cams': [cam(0, ['mec', 'mamie'], 'ms', worldAngle=10),
           cam('CA7:vérifié', 'ticket', 'mcu', worldAngle=-30, noOcclusion=True),
           cam('CA8', 'mecV', 'ms', angle=0, move='push', amount=0.05, noOcclusion=True)],
  'tail': 0.2,
})
scenes.append({
  'id': 'retour', 'set': 'supermarket', 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('CA9', "Hier, elle l'a rapporté au magasin. Date dépassée.", highlight=['magasin.', 'dépassée.']),
            L('CA10', "Putain, remboursé en bon d'achat.", highlight=["d'achat."]),
            L('CA11', "Article inattendu dans la zone d'ensachage.", 'caisse')],
  'actors': [act('mec', [2.3, 0, 0.9], 0, 'stand', 'sad', keys=[k('CA11', to=SCALE_TOP, glide=True, dur=0.05, face=0, clip='sitFloor', then='sitFloor', expr='unimpressed')]),
             act('mamie', [3.1, 0, 0.9], -30, 'stand', 'smug', keys=[k('CA10', clip='showPhone', expr='happy')])],
  'props': [P('borne', 'selfCheckout', pos=SC, opts={'alertAt': 'CA11'}),
            P('prix', 'priceTag', scale=0.8, opts={'text': '4,99 €'}, on=FOREHEAD),
            P('perime', 'stampMark', scale=0.55, visible=False, opts={'text': 'PÉRIMÉ', 'w': 0.3, 'h': 0.11}, on={**FOREHEAD, 'offset': [0, 0.33, 0.11]}, keys=[k('CA9:Date', visible=True)]),
            P('bon', 'bill', scale=1.6, visible=False, opts={'title': "BON D'ACHAT", 'items': [['Retour article', ''], ['Ce mec (périmé)', '4,99'], ['', '']], 'total': '4,99 €'},
              on={'actor': 'mamie', 'hand': 'R', **HAND_FLAT}, keys=[k('CA10', visible=True)])],
  'sfx': [{'at': 'CA9:Date', 'name': 'thud', 'vol': 0.5}, {'at': 'CA10:remboursé', 'name': 'cash', 'vol': 0.5}, {'at': 'CA11', 'name': 'beep', 'vol': 0.5}, {'at': 'CA11+0.35', 'name': 'beep', 'vol': 0.5}],
  'cams': [cam(0, ['mec', 'mamie'], 'ms', worldAngle=0),
           cam('CA9:Date', 'mec', 'cu', angle=0),
           cam('CA10:remboursé', 'bon', 'mcu', worldAngle=-20, noOcclusion=True),
           SCREEN_POV('CA11'),
           cam('CA11:zone', 'mec', 'ms', worldAngle=10)],
  'tail': 1.4,
})
write('caisse', 'La caisse automatique', scenes, {'mamie': {'preset': 'mamie'}, 'mecV': {'preset': 'lemec'}})
