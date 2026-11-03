#!/usr/bin/env python3
"""ACTU 10 — LE CHAT. He loses the neighbourhood pétanque tournament by 28 points, to his cat -> he calls the cops
(motif: escroquerie en bande organisée) -> doping test: the cat is positive for tuna -> suspended, the cat apologises
in three languages; like Mbappé it loses its sponsors (milk, tuna, kibble) -> custody, in the same cell as him ->
aura battle: the cat wins. By 28 points (it gets a Ballon d'Or)."""
from actu_common import *

def hops(start, end, anchor, off, n=4, step=0.4, h=0.28):
    out = []
    for i in range(1, n + 1):
        f = i / n
        out.append(k(f"{anchor}{off + (i - 1) * step:+.2f}", to=[start[j] + (end[j] - start[j]) * f for j in range(3)], dur=step * 0.92, arc=h, ease='inOut'))
    return out

scenes = []
JACK = [0.2, 0.0, -1.6]
BOULES = [[0.32, 0, -1.55], [0.05, 0, -1.72], [-1.2, 0, -0.4], [1.5, 0, 0.2]]
scenes.append({
  'id': 'petanque', 'set': 'park', 'ambience': 'park',
  'lines': [L('B1', "Ce mec a perdu le tournoi de pétanque du quartier. À vingt-huit points.", highlight=['pétanque', 'vingt-huit']),
            L('B2', "Contre son chat.", highlight=['chat.']),
            L('B3', "Il a appelé les flics. Motif : escroquerie en bande organisée.", highlight=['Motif', 'escroquerie'])],
  'actors': [
    act('mec', [-1.4, 0, 0.6], 40, 'stand', 'neutral', keys=[k('B1:perdu', clip='facepalm', expr='sad'), k('B2', clip='point', expr='angry', face='chat', turn=0.2), k('B3', clip='phoneCall', expr='angry', face=-20, turn=0.2)]),
    act('chat', [0.9, 0, 0.7], -60, 'sit', 'smug', scale=1.4, keys=[k('B1:points', clip='celebrate', expr='happy'), k('B2', clip='sit', expr='smug', face=-40, turn=0.2)]),
  ],
  'props': [*[P(f'b{i}', 'boule', scale=1.6, pos=p) for i, p in enumerate(BOULES)],
            P('cochonnet', 'boule', scale=1.6, pos=JACK, opts={'r': 0.018, 'color': '#E6B84A'}),
            P('score', 'signBoard', pos=[2.6, 0, -2.2], opts={'text': 'CHAT 41 — MEC 13', 'bg': '#26302C', 'fg': '#F6F1E3', 'w': 1.8, 'h': 0.5, 'height': 1.3}),
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('B3', visible=True)])],
  'cams': [cam(0, ['mec', 'chat'], 'fs', worldAngle=10, elev=8),
           cam('B1:points', [[2.6, 1.55, -2.2]], 'cu', worldAngle=0, noOcclusion=True, zoom=1.4),
           cam('B2', 'chat', 'cu', angle=0),
           cam('B3', 'mec', 'cu', angle=-35),
           cam('B3:escroquerie', 'chat', 'ms', angle=10)],
  'tail': 0.2,
})

scenes.append({
  'id': 'dopage', 'set': 'park', 'ambience': 'park',
  'lines': [L('B4', "Contrôle antidopage. Le chat était positif au thon.", highlight=['positif', 'thon.'])],
  'actors': [
    act('docteur', [0.2, 0, 0.9], -60, 'lookItem', 'neutral', keys=[k('B4:positif', clip='showPhone', expr='suspicious', face=0, turn=0.2)]),
    act('chat', [-0.6, 0, 0.6], 60, 'sit', 'smug', scale=1.4, keys=[k('B4:thon', clip='angry', expr='shocked')]),
    act('flic1', [1.4, 0, 0.2], -80, 'armsCrossed', 'suspicious'),
  ],
  'props': [P('test', 'notebook', scale=1.8, opts={'text': 'ANTIDOPAGE\n—\nPOSITIF\nAU THON', 'bg': '#B5302A'}, on={'actor': 'docteur', 'hand': 'R', **HAND_FLAT})],
  'cams': [cam(0, ['docteur', 'chat'], 'ms', worldAngle=0),
           cam('B4:positif', 'test', 'cu', worldAngle=0, noOcclusion=True, zoom=1.7),
           cam('B4:thon', 'chat', 'cu', angle=0)],
  'tail': 0.2,
})

POD_TOP = [0, 1.15, -2.0]
scenes.append({
  'id': 'excuses', 'set': 'pressRoom', 'setOpts': {'backdrop': 'PARDON|SORRY|LO SIENTO|SCUSATE|MIAOU|EXCUSES'}, 'ambience': 'station',
  'crowd': [journalists()],
  'lines': [L('B5', "Suspendu, le chat s'est excusé en trois langues.", highlight=['trois', 'langues.']),
            L('B6', "Comme Mbappé, il a perdu ses sponsors : le lait, le thon et les croquettes.", highlight=['Mbappé,', 'sponsors'])],
  'actors': [act('chat', [POD_TOP[0], POD_TOP[1], POD_TOP[2] - 0.05], 0, 'talk', 'sad', scale=1.4, keys=[k('B6', clip='sit', expr='sad')])],
  'props': [P('lait', 'milkCarton', scale=1.4, pos=[-0.5, 0, -1.4], keys=hops([-0.5, 0, -1.4], [-4.5, 0, 1.5], 'B6:lait', 0.0)),
            P('thon', 'drinkCan', scale=1.8, pos=[0.0, 0, -1.3], opts={'color': '#3E6FB5', 'text': 'THON'}, keys=hops([0.0, 0, -1.3], [-4.2, 0, 2.2], 'B6:thon', 0.0)),
            P('croq', 'foodSack', scale=0.55, pos=[0.55, 0, -1.4], opts={'text': 'CROQUETTES', 'color': '#C9A86A'}, keys=hops([0.55, 0, -1.4], [-4.0, 0, 2.9], 'B6:croquettes', 0.0))],
  'sfx': [{'at': 'B5', 'name': 'shutter', 'vol': 0.5}],
  'cams': [cam(0, 'chat', 'ms', angle=0),
           cam('B5:trois', 'chat', 'cu', angle=10),
           cam('B6', ['chat', 'lait', 'thon', 'croq'], 'fs', worldAngle=0, elev=8, withProps=True),
           cam('B6:croquettes', 'croq', 'ms', worldAngle=20, move='track', withProps=True)],
  'tail': 0.2,
})

scenes.append({
  'id': 'cellule', 'set': 'prisonCell', 'ambience': None,
  'lines': [L('B7', "Il a fini en garde à vue. Dans la même cellule que ce mec.", highlight=['même', 'cellule']),
            L('B8', "Ils ont fait une bataille d'aura. Le chat a gagné.", highlight=["d'aura.", 'gagné.']),
            L('B9', "À vingt-huit points.", pre=0.3, highlight=['vingt-huit'])],
  'actors': [
    act('mec', [0.9, 0, -1.6], -40, 'stand', 'sad', keys=[k('B8', clip='auraPose', expr='smug'), k('B8:aura', clip='auraPose2', expr='angry'), k('B8:gagné', clip='cry', expr='sad'), k('B9', clip='stareCamera', expr='unimpressed')]),
    act('chat', [-0.2, 0, -1.9], 40, 'sit', 'smug', scale=1.4, keys=[k('B8:gagné', clip='celebrate', expr='happy'), k('B9', clip='sit', expr='smug')]),
  ],
  'props': [P('ballon', 'ballonDor', scale=1.2, pos=[-0.55, 0, -1.75], visible=False, keys=[k('B8:gagné+0.2', visible=True, sfx='bell')])],
  'cams': [POV(0, [0.45, 1.8, 1.7], [0.35, 1.05, -1.75], 54),
           POV('B8', [-0.7, 1.75, 1.4], [0.35, 1.05, -1.75], 54),
           cam('B8:gagné', 'chat', 'cu', angle=0),
           cam('B9', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu10_chat', 'Le chat', scenes, {
  'chat': {'type': 'creature', 'name': 'cat', 'opts': {'seed': 6}},
  'docteur': {'preset': 'doctor'},
})
