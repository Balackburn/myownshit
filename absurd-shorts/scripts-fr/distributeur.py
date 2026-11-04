#!/usr/bin/env python3
"""LE DISTRIBUTEUR. Ce mec puts two euros in a vending machine for crisps -> the packet gets stuck -> he shakes the machine
-> the machine shakes him back -> ce con calls the cops -> they take the machine's statement -> in court the judge sides
with the machine: twenty years, inside the vending machine -> row B4, two euros -> yesterday someone bought him. He got
stuck. (Classic formula, no news gags.)"""
from actu_common import *

VM = [0.4, 0, -3.15]                       # vending machine against the office back wall (front at z = -2.75)
B4 = [VM[0] - 0.025, 1.41, VM[2] + 0.28]   # row B, spiral 4 (local x -0.025)
FRONT = [0.8, 0, -2.15]                    # in front of the keypad, so the glass stays visible from the front-left
scenes = []
scenes.append({
  'id': 'bureau', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.6,
  'lines': [L('D1', "Ce mec a mis deux euros dans un distributeur pour avoir des chips.", highlight=['euros', 'chips.']),
            L('D2', "Le paquet est resté coincé.", highlight=['coincé.']),
            L('D3', "Alors il a secoué la machine.", highlight=['secoué']),
            L('D4', "La machine l'a secoué aussi.", highlight=['aussi.']),
            L('D5', "Ce con a appelé les flics.", highlight=['flics.']),
            L('D6', "Ils ont pris la déposition du distributeur.", highlight=['déposition'])],
  'actors': [
    act('mec', FRONT, 180, 'stand', 'happy', keys=[
        k('D1:euros', clip='giveItem', expr='happy'),
        k('D2', clip='stand', expr='shocked'),
        k('D3', clip='holdOut', expr='angry'),
        k('D4:secoué', to=[1.7, 0, -0.7], glide=True, dur=0.45, arc=0.45, clip='hitFly', then='koFloor', face='keep', expr='shocked'),
        k('D5', to=[1.6, 0, -0.9], glide=True, dur=0.05, face=-30, clip='phoneCall', then='phoneCall', expr='angry')]),
    act('flic1', [5.2, 0, -0.4], -90, 'idle', 'neutral', visible=False, keys=[k('D6-0.6', visible=True), k('D6-0.6', to=[1.25, 0, -2.2], clip='walk', speed=4.0, faceEnd=-150, then='clipboard')]),
  ],
  'props': [P('vm', 'vending', pos=VM, opts={'shakeAt': ['D3:secoué', 'D3:machine', 'D4:secoué']}),
            P('piece', 'coin', scale=1.4, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('D1', visible=True), k('D1:chips', visible=False)]),
            P('paquet', 'chipsPack', pos=[B4[0], B4[1] + 0.02, B4[2] + 0.02], visible=False, keys=[k('D1:chips', visible=True), k('D1:chips', to=[B4[0], B4[1] + 0.02, B4[2] + 0.1], dur=0.6, ease='out'),
                                                                                           k('D2:coincé', to=[B4[0], B4[1] + 0.03, B4[2] + 0.115], dur=0.15)]),
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('D5', visible=True)])],
  'sfx': [{'at': 'D1:euros', 'name': 'clink', 'vol': 0.6}, {'at': 'D1:chips', 'name': 'squeak', 'vol': 0.4}, {'at': 'D2:coincé', 'name': 'thud', 'vol': 0.4},
          {'at': 'D3:secoué', 'name': 'thud', 'vol': 0.6}, {'at': 'D3:machine', 'name': 'thud', 'vol': 0.6}, {'at': 'D4:secoué', 'name': 'boing', 'vol': 0.6}, {'at': 'D4:secoué+0.45', 'name': 'punch', 'vol': 0.6},
          {'at': 'D6:déposition', 'name': 'beep', 'vol': 0.4}, {'at': 'D6:déposition+0.25', 'name': 'beep', 'vol': 0.4}],
  'cams': [cam(0, ['mec', [VM[0], 1.3, VM[2]]], 'ms', worldAngle=40),
           cam('D1:chips', [[B4[0], B4[1] + 0.12, B4[2] + 0.1]], 'cu', worldAngle=-15, noOcclusion=True, zoom=1.3),
           cam('D3', ['mec', [VM[0], 1.3, VM[2]]], 'ms', worldAngle=55),
           cam('D4', ['mec', [VM[0], 1.3, VM[2]]], 'fs', worldAngle=25, elev=6),
           cam('D5+0.1', 'mec', 'cu', angle=-25),
           cam('D6', ['flic1', [VM[0], 1.3, VM[2]]], 'ms', worldAngle=-35)],
  'tail': 0.2,
})
scenes.append({
  'id': 'tribunal', 'set': 'courtroom', 'ambience': 'station',
  'lines': [L('D7', "Au tribunal, le juge a donné raison à la machine.", highlight=['raison']),
            L('D8', "Vingt ans ferme. Dans le distributeur.", 'juge'),
            L('D9', "Putain.", pre=0.3)],
  'actors': [act('juge', [0, 0.42, -4.3], 0, 'sit', 'unimpressed', keys=[k('D8', clip='sitPoint', expr='angry')]),
             act('mec', [0.9, 0, -1.7], 180, 'stand', 'neutral', keys=[k('D8:ferme', expr='shocked', clip='startle'), k('D9', clip='stareCamera', expr='unimpressed')])],
  'props': [P('vm', 'vending', pos=[-1.1, 0, -2.0], ry=25)],
  'sfx': [{'at': 'D8:ferme', 'name': 'gavel', 'vol': 0.6}, {'at': 'D8:distributeur', 'name': 'gavel', 'vol': 0.6}],
  'cams': [cam(0, ['juge', 'vm'], 'fs', worldAngle=0, elev=6, withProps=True),
           cam('D8', 'juge', 'mcu', angle=0),
           cam('D9', 'mec', 'cu', angle=0)],
  'tail': 0.2,
})
scenes.append({
  'id': 'prison', 'set': 'office', 'setOpts': {'printer': False}, 'ambience': 'office', 'ambienceVol': 0.6,
  'lines': [L('D10', "Rangée B4, deux euros.", highlight=['B4,']),
            L('D11', "Hier, quelqu'un l'a acheté. Il est resté coincé.", highlight=['coincé.'])],
  'actors': [
    act('mecMini', [B4[0], B4[1] + 0.006, B4[2] - 0.05], 0, 'stand', 'sad', scale=0.12, keys=[
        k('D11:acheté', to=[B4[0], B4[1] + 0.006, B4[2] + 0.07], glide=True, dur=0.6, clip='stand', then='stiff', face='keep', expr='shocked'),
        k('D11:coincé', expr='unimpressed', clip='stareCamera')]),
    act('collegue', [-2.6, 0, -0.6], 90, 'idle', 'happy', keys=[k('D10', to=[0.75, 0, -2.15], clip='walk', speed=2.6, faceEnd=180, then='stand'), k('D11', clip='giveItem')]),
  ],
  'props': [P('vm', 'vending', pos=VM, opts={'empty': True}),
            P('prix', 'priceTag', scale=0.35, pos=[B4[0] + 0.05, B4[1] - 0.045, VM[2] + 0.41], opts={'text': '2,00 €'})],
  'sfx': [{'at': 'D11', 'name': 'clink', 'vol': 0.6}, {'at': 'D11:acheté', 'name': 'squeak', 'vol': 0.4}, {'at': 'D11:coincé', 'name': 'thud', 'vol': 0.4}],
  'cams': [cam(0, 'mecMini', 'fs', angle=0, noOcclusion=True),
           cam('D11', ['collegue', [VM[0], 1.3, VM[2]]], 'ms', worldAngle=40),
           cam('D11:resté', 'mecMini', 'fs', angle=0, noOcclusion=True, move='push', amount=0.04)],
  'tail': 1.4,
})

write('distributeur', 'Le distributeur', scenes, {
  'juge': {'preset': 'judge'},
  'mecMini': {'preset': 'lemec'},
  'collegue': {'preset': 'lemec_beige', 'seed': 33},
})
