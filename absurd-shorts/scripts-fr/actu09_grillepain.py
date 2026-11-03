#!/usr/bin/env python3
"""ACTU 09 — LE GRILLE-PAIN. He loses an aura battle against his toaster, which fires a toast at him -> he calls the
cops (motif: tentative d'homicide) -> the toaster in custody fires a toast at the inspector -> the inspector wants to
make a trend ("Attendez. Filmez-moi.") and the toaster escapes during the choreography -> it flees to Japan where
everything is clean and on time: it faints (reverse Paris syndrome) -> back in France it recovers at once: it goes on
strike -> he now eats his bread raw."""
from actu_common import *

scenes = []
TO = [0.3, 0.95, -3.3]      # kitchen counter, where the set's toaster usually is
scenes.append({
  'id': 'cuisine', 'set': 'kitchenNight', 'setOpts': {'toaster': False}, 'lighting': 'interior', 'ambience': None,
  'lines': [L('A1', "Ce mec a perdu une bataille d'aura contre son grille-pain.", highlight=["d'aura", 'grille-pain.']),
            L('A2', "Le grille-pain lui a éjecté un toast en pleine face.", highlight=['face.']),
            L('A3', "Il a appelé les flics. Motif : tentative d'homicide.", highlight=['Motif', "d'homicide."])],
  'actors': [act('mec', [-0.35, 0, -2.5], 150, 'auraPose', 'smug', keys=[
      k('A1:perdu', clip='auraPose2', expr='angry'),
      k('A1#9', clip='cry', expr='sad'),
      k('A2:face', clip='startle', expr='shocked'),
      k('A3', clip='phoneCall', expr='angry', face=-25, turn=0.2)])],
  'props': [P('gp', 'toaster', pos=TO, opts={'color': '#C23A2E', 'popAt': 'A2:éjecté-0.1'}),
            P('toast', 'toast', scale=1.4, pos=[TO[0], TO[1] + 0.2, TO[2]], visible=False, keys=[k('A2:éjecté', visible=True), k('A2:éjecté', to=[-0.3, 1.62, -2.6], dur=0.45, arc=0.5, ease='in'), k('A2:face+0.1', to=[-0.2, 0.02, -2.2], dur=0.5, ease='in')]),
            P('tel', 'phone911', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('A3', visible=True)])],
  'sfx': [{'at': 'A2:éjecté-0.1', 'name': 'boing', 'vol': 0.5}, {'at': 'A2:face', 'name': 'splat', 'vol': 0.6}],
  'cams': [cam(0, ['mec', [TO[0], 1.1, TO[2]]], 'ms', worldAngle=70),
           cam('A1#9', [[TO[0], 1.1, TO[2]]], 'cu', worldAngle=10, noOcclusion=True),
           cam('A1#9+0.6', 'mec', 'cu', angle=-60),
           cam('A2', ['mec', [TO[0], 1.1, TO[2]]], 'ms', worldAngle=80),
           cam('A2:face', 'mec', 'cu', angle=-50),
           cam('A3', 'mec', 'cu', angle=-35)],
  'tail': 0.2,
})

GT = [IR_ON_TABLE[0], IR_ON_TABLE[1], IR_ON_TABLE[2] + 0.1]
scenes.append({
  'id': 'gav', 'set': 'interrogation', 'ambience': 'station',
  'lines': [L('A4', "Les flics ont embarqué le grille-pain.", highlight=['grille-pain.']),
            L('A5', "Vous reconnaissez les faits ?", 'commissaire'),
            L('A6', "Le grille-pain a éjecté un toast.", highlight=['toast.']),
            L('A7', "Attendez. Filmez-moi.", 'commissaire', highlight=['Filmez-moi.']),
            L('A8', "Le grille-pain s'est évadé pendant la chorégraphie.", highlight=['évadé'])],
  'actors': [
    act('commissaire', IR_COP, -90, 'leanTable', 'suspicious', keys=[
        k('A5', clip='leanTable', expr='angry'), k('A6:éjecté+0.3', clip='startle', expr='shocked'),
        k('A7', clip='point', expr='happy', face='flic2', turn=0.2), k('A8', clip='dance', expr='happy', face=0, turn=0.2),
        k('A8:chorégraphie+0.3', clip='stand', expr='shocked', face=-90, turn=0.2)]),
    act('flic2', [-0.9, 0, 0.35], 150, 'armsCrossed', 'unimpressed', keys=[k('A7#1', clip='showPhone', expr='unimpressed')]),
  ],
  'props': [P('gp', 'toaster', pos=GT, opts={'color': '#C23A2E', 'popAt': 'A6:éjecté-0.1'}, keys=[k('A8:évadé', visible=False)]),
            P('toast', 'toast', scale=1.4, pos=[GT[0], GT[1] + 0.2, GT[2]], visible=False, keys=[k('A6:éjecté', visible=True), k('A6:éjecté', to=[0.85, 1.75, -0.75], dur=0.35, arc=0.3, ease='in'), k('A6:toast', to=[1.2, 0.02, -0.5], dur=0.45, ease='in')]),
            P('tel', 'phone911', visible=False, opts={'screen': 'tiktok'}, on={'actor': 'flic2', 'hand': 'R', **HAND_FLAT}, keys=[k('A7#1', visible=True)])],
  'sfx': [{'at': 'A6:éjecté-0.1', 'name': 'boing', 'vol': 0.5}, {'at': 'A8', 'name': 'sting', 'vol': 0.3}],
  'cams': [cam(0, ['commissaire', [GT[0], 0.95, GT[2]]], 'fs', worldAngle=10, elev=10),
           cam('A5', 'commissaire', 'mcu', angle=60),
           cam('A6', [[GT[0], 0.95, GT[2]]], 'cu', worldAngle=0, noOcclusion=True),
           cam('A6:toast', 'commissaire', 'cu', angle=50),
           cam('A7', ['commissaire', 'flic2'], 'ms', worldAngle=10),
           cam('A8', 'commissaire', 'fs', worldAngle=0, elev=6),
           cam('A8:chorégraphie', ['commissaire', [GT[0], 0.95, GT[2]]], 'ms', worldAngle=10)],
  'tail': 0.2,
})

scenes.append({
  'id': 'tokyo', 'set': 'street', 'ambience': 'street',
  'lines': [L('A9', "Il a fui au Japon. Là-bas, tout était propre et à l'heure. Il a fait un malaise.", highlight=['propre', "l'heure.", 'malaise.'])],
  'actors': [],
  'props': [P('torii', 'torii', pos=[0.4, 0, -1.6]),
            P('sign', 'signBoard', pos=[-2.2, 0, -1.3], opts={'text': 'TOKYO', 'bg': '#F6F1E3', 'fg': '#C23A2E', 'w': 1.2, 'h': 0.45, 'height': 1.6}),
            P('horloge', 'wallClock', pos=[2.6, 2.4, -1.25], opts={'rate': 0}),
            P('gp', 'toaster', pos=[0.4, 0, 0.6], opts={'color': '#C23A2E'}, alt={'opts': {'color': '#C23A2E'}, 'at': 'A9:malaise-0.1', 'rot': [0, 0, 1.5708]})],
  'sfx': [{'at': 'A9:malaise', 'name': 'thud', 'vol': 0.6}],
  'cams': [cam(0, ['torii', 'sign', 'gp'], 'fs', worldAngle=0, elev=6, withProps=True),
           cam('A9:propre', [[0.4, 0.15, 0.6]], 'ms', worldAngle=15, elev=10, noOcclusion=True),
           cam('A9:malaise', [[0.4, 0.15, 0.6]], 'cu', worldAngle=0, elev=20, noOcclusion=True)],
  'tail': 0.3,
})

scenes.append({
  'id': 'retour', 'set': 'kitchenNight', 'setOpts': {'toaster': False}, 'lighting': 'interior', 'ambience': None,
  'lines': [L('A10', "Rapatrié en France, il s'est remis tout de suite : il s'est mis en grève.", highlight=['grève.']),
            L('A11', "Depuis, ce mec mange son pain cru.", highlight=['cru.'])],
  'actors': [act('mec', [-0.4, 0, -2.4], 150, 'stand', 'sad', keys=[k('A11', clip='eatHands', expr='sad', face=10, turn=0.2), k('A11:cru', clip='stareCamera', expr='unimpressed')])],
  'props': [P('gp', 'toaster', pos=TO, opts={'color': '#C23A2E'}),
            P('greve', 'protestSign', scale=0.32, pos=[TO[0] + 0.32, TO[1], TO[2] + 0.05], opts={'text': 'GRÈVE', 'color': '#B3261E'}),
            P('pain', 'toast', opts={'raw': True}, scale=1.3, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('A11', visible=True)])],
  'cams': [cam(0, [[TO[0] + 0.15, 1.15, TO[2]]], 'cu', worldAngle=10, noOcclusion=True),
           cam('A11', 'mec', 'ms', angle=0),
           cam('A11:cru', 'mec', 'cu', angle=0, move='push', amount=0.05)],
  'tail': 1.4,
})

write('actu09_grillepain', 'Le grille-pain', scenes)
