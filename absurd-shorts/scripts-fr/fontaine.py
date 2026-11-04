#!/usr/bin/env python3
"""LA FONTAINE (viral-video-writing loop, score_fr.py 100/100). Hook with a number (a two-euro coin) -> the villain at 4 s (the
fountain sends the coin back with an invoice) -> the wish cost 2 000 € -> a cheque, a bounced cheque -> the bank seizes the house
-> the fountain buys it at auction -> low point: he sleeps in the fountain -> loop: a coin to get his house back, the fountain
asks for interest (the opening gesture again)."""
from actu_common import *

FT = [1.8, 0, -3.9]
ME = [0.4, 0, -1.9]
FACE_POV = lambda at: POV(at, [2.9, 1.55, -1.3], [ME[0], 1.3, ME[2]], 50)     # front-right of him, the fountain at the edge of frame
def bill(id_, title, items, total, vis_at): return P(id_, 'bill', scale=1.7, visible=False, opts={'title': title, 'items': items, 'total': total},
                                                    on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k(vis_at, visible=True)])
scenes = []
scenes.append({
  'id': 'parc', 'set': 'park', 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('FO1', "Ce mec a jeté une pièce de deux euros dans une fontaine pour faire un vœu.", highlight=['deux', 'euros', 'vœu.']),
            L('FO2', "La fontaine a rendu la pièce. Avec une facture.", highlight=['rendu', 'facture.']),
            L('FO3', "Le vœu coûtait deux mille euros.", highlight=['deux', 'mille']),
            L('FO4', "Alors ce con a payé par chèque.", highlight=['chèque.'])],
  'actors': [act('mec', ME, 145, 'stand', 'happy', keys=[k('FO1:jeté', clip='giveItem', expr='grin'), k('FO2:rendu', clip='startle', expr='shocked'),
                                                       k('FO2:facture', clip='showPhone', expr='shocked'), k('FO4', clip='writeOnHeld', expr='angry'), k('FO4:chèque', clip='giveItem')])],
  'props': [P('fontaine', 'fountain', pos=FT),
            P('piece', 'coin', scale=1.6, on={'actor': 'mec', 'hand': 'R'}, keys=[k('FO1:jeté+0.15', detach=True, fall=True, toss=[1.2, 2.6, -1.6], impact='splash')]),
            P('retour', 'coin', scale=1.6, visible=False, pos=[FT[0] - 0.5, 1.8, FT[2] + 0.6], keys=[k('FO2:rendu', visible=True), k('FO2:rendu', to=[ME[0] + 0.1, 1.2, ME[2] - 0.2], dur=0.5, ease='out'),
                                                                                                  k('FO2:facture', visible=False)]),
            bill('facture', 'FACTURE', [['Vœu', '2 000,00'], ['Fontaine', 'TTC'], ['', '']], '2 000,00 €', 'FO2:facture'),
            P('cheque', 'cheque', scale=2.2, visible=False, on={'actor': 'mec', 'hand': 'R', **HAND_FLAT}, keys=[k('FO4', visible=True), k('FO4:chèque+0.15', detach=True, fall=True, toss=[1.0, 2.2, -1.5], impact='splash')])],
  'sfx': [{'at': 'FO2:rendu', 'name': 'pop', 'vol': 0.6}, {'at': 'FO2:facture', 'name': 'paper', 'vol': 0.5}, {'at': 'FO3:mille', 'name': 'cash', 'vol': 0.4}],
  'cams': [FACE_POV(0),
           cam('FO1:fontaine', 'fontaine', 'fs', worldAngle=30, withProps=True),
           FACE_POV('FO2'),
           cam('FO3', 'facture', 'mcu', worldAngle=145, noOcclusion=True),
           FACE_POV('FO4')],
  'tail': 0.2,
})
scenes.append({
  'id': 'banque', 'set': 'bank', 'ambience': 'office', 'ambienceVol': 0.5,
  'lines': [L('FO5', "Le chèque était sans provision.", highlight=['provision.']),
            L('FO6', "La banque a saisi sa maison.", highlight=['saisi', 'maison.'])],
  'actors': [act('banquier', [-1.2, 0, -2.5], 0, 'showPhone', 'unimpressed', keys=[k('FO6', clip='point', expr='angry')]),
             act('mec', [-0.4, 0, -1.2], -150, 'stand', 'worried', keys=[k('FO6:maison', expr='shocked')])],
  'props': [P('cheque', 'cheque', scale=2.4, on={'actor': 'banquier', 'hand': 'R', **HAND_FLAT}, keys=[k('FO6', visible=False)]),
            P('tampon', 'stampMark', scale=0.6, visible=False, opts={'text': 'SANS PROVISION', 'w': 0.36, 'h': 0.09}, on={'actor': 'banquier', 'hand': 'R', **HAND_FLAT, 'offset': [0, -0.13, 0.03]},
              keys=[k('FO5:provision', visible=True), k('FO6', visible=False)])],
  'sfx': [{'at': 'FO5:provision', 'name': 'thud', 'vol': 0.6}, {'at': 'FO6:saisi', 'name': 'gavel', 'vol': 0.5}],
  'cams': [cam(0, 'cheque', 'mcu', worldAngle=0, noOcclusion=True), cam('FO6', ['banquier', 'mec'], 'ms', worldAngle=-80)],
  'tail': 0.2,
})
scenes.append({
  'id': 'encheres', 'set': 'courtroom', 'setOpts': {'sign': 'VENTE AUX ENCHÈRES'}, 'ambience': 'station',
  'lines': [L('FO7', "La fontaine l'a rachetée aux enchères.", highlight=['fontaine', 'enchères.'])],
  'actors': [act('commissaire', [0, 0.42, -4.3], 0, 'sit', 'neutral', keys=[k('FO7:rachetée', clip='sitPoint', expr='happy')])],
  'props': [P('fontaine', 'fountain', scale=0.6, pos=[0.4, 0, -1.4]), P('maison', 'house', scale=0.18, pos=[-1.3, 0.79, -3.3], opts={'w': 4, 'd': 3.4, 'h': 2.5})],
  'sfx': [{'at': 'FO7:enchères', 'name': 'gavel', 'vol': 0.7}],
  'cams': [POV(0, [1.4, 1.6, 2.6], [0.1, 1.2, -2.6], 52)],
  'tail': 0.2,
})
scenes.append({
  'id': 'parc2', 'set': 'park', 'ambience': 'park', 'ambienceVol': 0.5,
  'lines': [L('FO8', "Depuis trois ans, ce mec dort dans la fontaine.", highlight=['trois', 'fontaine.']),
            L('FO9', "Hier, il a jeté une pièce pour récupérer sa maison.", highlight=['pièce', 'maison.']),
            L('FO10', "Putain, la fontaine a demandé des intérêts.", highlight=['intérêts.'])],
  'actors': [act('mec', [FT[0] + 0.2, 0.42, FT[2] + 0.75], 90, 'lieBack', 'sleepy', keys=[   # lying across, in front of the column, head on the left
                 k('FO9', to=[FT[0] - 0.3, 0.38, FT[2] + 0.75], glide=True, dur=0.05, face=0, clip='stand', then='stand', expr='grin'),
                 k('FO9:pièce-0.25', clip='wave'),   # over the shoulder, back into the fountain
                 k('FO10', clip='showPhone', expr='shocked')])],
  'props': [P('fontaine', 'fountain', pos=FT),
            P('piece', 'coin', scale=1.6, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('FO9', visible=True), k('FO9:pièce+0.1', detach=True, fall=True, toss=[0.4, 2.2, -0.8], impact='splash')]),
            bill('interets', 'INTÉRÊTS', [['Vœu (3 ans)', '2 000,00'], ['Intérêts', '340,00'], ['', '']], '2 340,00 €', 'FO10')],
  'sfx': [{'at': 'FO8', 'name': 'splash', 'vol': 0.3}, {'at': 'FO10', 'name': 'pop', 'vol': 0.6}, {'at': 'FO10:intérêts', 'name': 'paper', 'vol': 0.5}],
  'cams': [POV(0, [FT[0] - 1.2, 2.2, FT[2] + 3.4], [FT[0] - 0.1, 0.5, FT[2] + 0.7], 45),
           cam('FO9', 'mec', 'ms', angle=0),
           cam('FO10:intérêts', 'interets', 'mcu', worldAngle=0, noOcclusion=True)],
  'tail': 1.4,
})
write('fontaine', 'La fontaine', scenes, {'banquier': {'preset': 'lemec_glasses', 'seed': 21}, 'commissaire': {'preset': 'judge'}})
