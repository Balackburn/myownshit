#!/usr/bin/env python3
"""SON NOM DESSUS — original episode (python3 scripts-fr/marqueur.py -> marqueur.json)

french-lowpoly-absurd-shorts mechanics: a concrete incident (his yogurt gets stolen at the office), an absurd rule
(if your name is written on it, it is yours), the world obeys it (colleague's chair, the colleague himself, the boss's
door, the bank vault, the police car), then the rule turns against him (a granny with a marker writes HER name on him)
and a visual punchline (Monique eats his yogurt, his name crossed out).
The "name" he writes everywhere is CON (the narrator's "ce con" taken literally): people read it and call him "Con".

Scenes: FRIGO (office) -> CHAISE (office) -> PORTE (office) -> BANQUE -> FLICS (street) -> MONIQUE (street) -> SALON
Office geography (same in every office scene): fridge on the back wall at x 3.3 (door hinged right), the boss's door
(plaque DIRECTEUR) at x 4.7, the broom closet (ENTRETIEN) at x 6.2 where the printer was, the colleague's tall office
chair rolled out at (1.9, -1.6).
"""
import json, os

def L(id, text, speaker=None, **kw): return {'id': id, 'text': text, **({'speaker': speaker} if speaker else {}), **kw}
def act(id, pos, ry=0, clip='idle', expr=None, keys=None, **kw):
    d = {'id': id, 'pos': pos, 'ry': ry, 'clip': clip, 'keys': keys or [], **kw}
    if expr: d['expr'] = expr
    return d
def k(at, **kw): return {'at': at, **kw}
def cam(at, frame=None, size='ms', **kw):
    d = {'at': at, 'size': size, **kw}
    if frame is not None: d['frame'] = frame
    return d
def P(id, name, **kw): return {'id': id, 'name': name, **kw}
WM = lambda **kw: {'name': 'wmSign', 'id': 'wm', **kw}
HAND_FLAT = {'rot': [1.5708, 0, 0], 'offset': [0, -0.13, 0.02]}
FOREHEAD = [0, 0.455, 0.094]           # head joint -> forehead, just in front of the face panel
INK, RED_INK = '#15171C', '#B3261E'
OFFICE = {'door': False, 'printer': False}
CHAIR = [1.9, 0, -1.6]

def office_props(fridge=None, door=None):
    """the office furniture that changes between scenes is scene props (same place in every office scene)"""
    return [P('frigo', 'fridge', pos=[3.3, 0, -3.22], opts={'hinge': 'R', **(fridge or {})}),
            P('porte', 'door', pos=[4.7, 0, -3.6], opts={'color': '#D9C9A6', 'plaque': 'DIRECTEUR', **(door or {})}),
            P('placard', 'cupboard', pos=[6.2, 0, -3.25], opts={'sign': 'ENTRETIEN'}),
            P('chair', 'officeChair', pos=CHAIR),
            WM(pos=[-2.85, 1.85, -3.575])]

scenes = []

# ---------------------------------------------------------------- 1. le frigo : le vol quotidien, le nom sur le pot
Y_SHELF = [3.3, 1.365, -3.12]
CUP_L = lambda actor: {'actor': actor, 'hand': 'L', 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]}   # upright pot, name outwards
def FRIDGE_POV(at, look):   # camera inside the fridge, above the top shelf: the yogurt in the foreground, the person in the opening
    return {'at': at, 'from': [3.42, 1.6, -3.45], 'lookAt': look, 'lens': 62}
scenes.append({
  'id': 'frigo', 'set': 'office', 'setOpts': OFFICE, 'ambience': 'office',
  'lines': [L('M1', "Ce mec se faisait voler son yaourt au bureau. Tous les jours.", highlight=['yaourt', 'Tous', 'jours.']),
            L('M2', "Alors il a écrit son nom dessus. Putain, plus personne n'y a touché.", highlight=['nom', 'Putain,'])],
  'actors': [
    act('madame', [3.1, 0, -2.3], 180, 'lookAround', 'suspicious', keys=[
        k(0.4, clip='takeItem', expr='neutral'),
        k(0.85, clip='lookItem', expr='happy'),
        k('M1:voler', path=[[2.55, 0, -1.0], [0.5, 0, -0.4]], clip='walkEat', speed=1.0, faceEnd='mec', then='eatSpoon', expr='happy'),
        k('M2:écrit', path=[[2.6, 0, -1.0], [3.0, 0, -2.42]], clip='walk', speed=1.6, faceEnd=180, then='takeItem', expr='neutral'),
        k('M2:personne+0.15', clip='startle', expr='scared', sfx='gasp'),
        k('M2:touché+0.1', path=[[2.6, 0, -1.2], [0.6, 0, -0.5]], clip='walk', speed=1.7, expr='scared')]),
    act('mec', [5.2, 0, 0.4], -140, 'idle', 'happy', keys=[
        k(0.3, path=[[4.0, 0, -1.2], [3.15, 0, -2.25]], clip='walk', speed=1.55, faceEnd=180, then='idle'),
        k('M1:Tous', clip='takeItem'),
        k('M1:jours', clip='stareCamera', expr='sad', face=-20, turn=0.3),
        k('M2', clip='writeOnHeld', expr='smug', face=-30, turn=0.25),
        k('M2:dessus', clip='giveItem', face=180, turn=0.2, expr='happy'),
        k('M2:dessus+0.45', path=[[4.4, 0, -1.6], [5.8, 0, 0.4]], clip='walk', speed=1.5, expr='smug')]),
  ],
  'props': [*office_props(fridge={'openAt': [-0.6, 'M1:Tous-0.1', 'M2:Putain+0.55'], 'closeAt': ['M1:voler+0.25', 'M2:dessus+0.4']}),
            P('y1', 'yogurt', pos=Y_SHELF, scale=1.3, keys=[k(0.65, attach='madame', **CUP_L('madame')), k('M2', visible=False)]),
            P('spoonM', 'spoon', on={'actor': 'madame', 'hand': 'R'}, visible=False, keys=[k('M1:voler', visible=True), k('M2', visible=False)]),
            P('spoon', 'spoon', on={'actor': 'mec', 'hand': 'R'}, keys=[k('M2', visible=False)]),
            P('y2h', 'yogurt', opts={'name': 'CON', 'writeAt': 'M2:écrit', 'writeDur': 0.7}, scale=1.3, visible=False,
              on=CUP_L('mec'), keys=[k('M2', visible=True), k('M2:dessus+0.3', visible=False)]),
            P('y2', 'yogurt', opts={'name': 'CON'}, pos=Y_SHELF, scale=1.3, visible=False, keys=[k('M2:dessus+0.3', visible=True)]),
            P('marker', 'marker', on={'actor': 'mec', 'hand': 'R'}, visible=False, keys=[k('M2', visible=True)])],
  'sfx': [{'at': 'M2:écrit', 'name': 'squeak', 'vol': 0.6}, {'at': 'M2:écrit+0.45', 'name': 'squeak', 'vol': 0.5},
          {'at': 'M1:voler+0.6', 'name': 'carDoor', 'vol': 0.15}, {'at': 'M2:dessus+0.75', 'name': 'carDoor', 'vol': 0.18}],
  'cams': [FRIDGE_POV(0, [3.12, 1.78, -2.3]),
           cam('M1:voler', 'madame', 'fs', angle=-35, move='track'),
           FRIDGE_POV('M1:Tous-0.15', [3.15, 1.72, -2.25]),
           cam('M1:jours', ['mec', 'madame'], 'fs', worldAngle=-5, elev=6),
           cam('M2', 'mec', 'mcu', angle=25),
           cam('M2:écrit+0.1', 'y2h', 'cu', worldAngle=-45, noOcclusion=True),
           FRIDGE_POV('M2:dessus', [3.1, 1.75, -2.3]),
           cam('M2:touché+0.45', 'y2', 'cu', worldAngle=0, noOcclusion=True, zoom=1.35, move='push', amount=0.05)],
  'tail': 0.6,
})

# ---------------------------------------------------------------- 2. la chaise, puis le collègue lui-même
SCRAWL_CHAIR = {'actor': 'chair', 'offset': [0, 1.0, -0.183], 'rot': [-0.08, 0, 0]}
CX, CZ = CHAIR[0], CHAIR[2]
scenes.append({
  'id': 'chaise', 'set': 'office', 'setOpts': OFFICE, 'ambience': 'office',
  'lines': [L('M3', "Ce con en a conclu un truc. Si ton nom est dessus, c'est à toi.", highlight=['nom', 'toi.']),
            L('M4', "Il a écrit son nom sur la chaise de son collègue.", highlight=['chaise']),
            L('M5', "Ah, pardon. Elle est à toi.", 'coll1', highlight=['pardon.']),
            L('M6', "Puis sur le collègue.", pre=0.5, highlight=['collègue.']),
            L('M7', "Ton café, Con. Je te masse les pieds ?", 'coll1', pre=0.6, highlight=['Con.', 'pieds'])],
  'actors': [
    act('mec', [3.1, 0, -2.3], 180, 'idle', 'happy', keys=[
        k('M3:conclu', clip='think', expr='smug'),
        k('M3:Si', look='chair', expr='suspicious', face=-60, turn=0.3),
        k('M3:toi', clip='stareCamera', expr='smug', look=None, face=-10, turn=0.2),
        k('M3:toi+0.25', to=[CX + 0.5, 0, CZ + 0.3], clip='sneak', speed=1.15, faceEnd=-134, then='idle', expr='smug'),
        k('M4:sur', clip='drawMid'),
        k('M4:collègue+0.15', clip='handsOnHips', expr='smug', face='coll1', turn=0.25),
        k('M5:Elle', to=[CX, 0, CZ + 0.5], clip='walk', speed=1.2, faceEnd=0, then='idle'),
        k('M5.end', to=[CX, 0.14, CZ + 0.1], glide=True, dur=0.3, clip='sit', then='sit', face='keep', expr='happy'),
        k('M6', face='coll1', turn=0.35, expr='smug'),
        k('M6:sur', clip='sitDraw'),
        k('M6.end+0.3', clip='sit', expr='smug'),
        k('M7', face='coll1', turn=0.3),
        k('M7:café+0.15', clip='sitTake'),
        k('M7#2+0.2', clip='sitSip', expr='smug')]),
    act('coll1', [5.4, 0, 0.3], -90, 'idle', 'neutral', keys=[
        k('M4', to=[CX - 0.15, 0, CZ + 0.95], clip='walk', speed=1.6, faceEnd='chair', then='idle'),
        k('M5', clip='doubleTake', expr='surprised'),
        k('M5:Elle', clip='present', expr='happy', face='mec', turn=0.25),
        k('M5.end+0.1', to=[CX - 0.5, 0, CZ + 0.6], clip='walk', speed=1.2, faceEnd='mec', then='sitFloor', expr='neutral'),
        k('M6.end', face=10, turn=0.3, expr='unimpressed'),
        k('M7', clip='kneelGive', expr='happy', face='mec', turn=0.25),
        k('M7:Je', clip='kneelMassage', expr='happy')]),
  ],
  'props': [*office_props(fridge={'open': 1}),
            P('y2', 'yogurt', opts={'name': 'CON'}, pos=Y_SHELF, scale=1.3),
            P('marker', 'marker', on={'actor': 'mec', 'hand': 'R'}, visible=False, keys=[k('M3:toi', visible=True), k('M6.end+0.3', visible=False)]),
            P('nameChair', 'scrawl', opts={'text': 'CON', 'w': 0.36, 'h': 0.16, 'writeAt': 'M4:sur', 'writeDur': 0.7}, on=SCRAWL_CHAIR),
            P('mug', 'mug', opts={'color': '#F1E9D2'}, on={'actor': 'coll1', 'hand': 'R'}, keys=[k('M7#2', attach='mec', hand='R')]),
            P('nameColl', 'scrawl', opts={'text': 'CON', 'w': 0.16, 'h': 0.065, 'writeAt': 'M6:sur+0.15', 'writeDur': 0.6},
              on={'actor': 'coll1', 'joint': 'head', 'offset': FOREHEAD})],
  'sfx': [{'at': 'M4:sur', 'name': 'squeak', 'vol': 0.6}, {'at': 'M4:sur+0.5', 'name': 'squeak', 'vol': 0.5},
          {'at': 'M6:sur+0.15', 'name': 'squeak', 'vol': 0.6}, {'at': 'M6:sur+0.55', 'name': 'squeak', 'vol': 0.5}],
  'cams': [FRIDGE_POV(0, [3.1, 1.7, -2.3]),
           cam('M3:Si', ['mec', 'chair'], 'fs', worldAngle=-15, elev=8),
           cam('M3:toi', 'mec', 'ecu', angle=0, move='push', amount=0.05),
           cam('M3:toi+0.4', 'mec', 'fs', angle=60, move='track'),
           cam('M4:sur', ['mec', 'chair'], 'ms', worldAngle=-40),
           cam('M4:collègue+0.2', [[CX, 1.0, CZ - 0.183]], 'cu', worldAngle=-30, noOcclusion=True),
           cam('M5', 'coll1', 'mcu', angle=15),
           cam('M5:Elle', ['coll1', 'mec', 'chair'], 'fs', worldAngle=20, elev=6),
           cam('M6', ['mec', 'coll1'], 'ms', worldAngle=45),
           cam('M6.end+0.2', 'coll1', 'ecu', worldAngle=5),
           cam('M7', ['mec', 'coll1'], 'ms', worldAngle=45),
           cam('M7:masse', ['mec', 'coll1'], 'ms', worldAngle=-20, elev=30)],
  'tail': 0.5,
})

# ---------------------------------------------------------------- 3. la porte du patron -> le patron dans le placard
scenes.append({
  'id': 'porte', 'set': 'office', 'setOpts': OFFICE, 'ambience': 'office',
  'lines': [L('M8', "Puis sur la porte du patron. Le patron a déménagé dans le placard.", highlight=['porte', 'placard.'])],
  'actors': [
    act('mec', [4.3, 0, -2.95], 165, 'idle', 'smug', keys=[
        k('M8:sur', clip='drawOn'),
        k('M8:patron.end-0.15', to=[3.3, 0, -2.0], clip='walk', speed=1.3, faceEnd='porte', then='handsOnHips'),
        k('M8:déménagé', path=[[4.6, 0, -2.3], [4.7, 0, -3.3]], clip='strut', speed=1.1, then='idle'),
        k('M8.end+0.95', visible=False)]),
    act('patron', [4.7, 0, -3.35], 0, 'carry', 'sad', visible=False, keys=[
        k('M8:Le+0.15', visible=True),
        k('M8:Le+0.2', path=[[5.3, 0, -2.6], [6.2, 0, -2.55], [6.2, 0, -3.12]], clip='carryBox', speed=1.3, faceEnd=0, then='carry', expr='sad')]),
  ],
  'props': [*office_props(fridge={'open': 0}, door={'name': 'CON', 'writeAt': 'M8:sur+0.1', 'writeDur': 0.7, 'openAt': 'M8:Le', 'closeAt': 'M8.end+1.0'}),
            P('marker', 'marker', on={'actor': 'mec', 'hand': 'R'}),
            P('box', 'cardboardBox', opts={'text': ''}, scale=0.75, on={'actor': 'patron', 'joint': 'torso', 'offset': [0, 0.22, 0.34]}),
            P('plant', 'plant', scale=0.35, on={'actor': 'box', 'offset': [0.1, 0.25, 0]})],
  'sfx': [{'at': 'M8:sur+0.1', 'name': 'squeak', 'vol': 0.6}, {'at': 'M8:sur+0.6', 'name': 'squeak', 'vol': 0.5},
          {'at': 'M8:Le', 'name': 'carDoor', 'vol': 0.25}, {'at': 'M8.end+1.0', 'name': 'carDoor', 'vol': 0.3}],
  'cams': [cam(0, 'mec', 'ms', worldAngle=75),
           cam('M8:patron', [[4.7, 1.55, -3.55]], 'cu', worldAngle=45, noOcclusion=True),
           cam('M8:Le', ['porte', 'placard', 'mec'], 'fs', worldAngle=0, elev=6),
           cam('M8.end+0.2', 'patron', 'mcu', angle=0)],
  'tail': 1.3,
})

# ---------------------------------------------------------------- 4. la banque : le coffre
VAULT_TXT = [2.6, 1.52, -3.226]
scenes.append({
  'id': 'banque', 'set': 'bank', 'ambience': 'bank',
  'lines': [L('M9', "À la banque, il a écrit son nom sur le coffre.", highlight=['coffre.']),
            L('M10', "Tout est à vous, monsieur Con. Vous voulez un sac ?", 'banquier', highlight=['Con.', 'sac'])],
  'actors': [
    act('banquier', [-1.2, 0, -2.1], 0, 'idle', 'neutral', keys=[
        k('M9:coffre', clip='doubleTake', expr='surprised', face='mec', turn=0.3),
        k('M9.end-0.1', path=[[0.9, 0, -2.3], [2.65, 0, -2.35]], clip='run', speed=2.4, faceEnd='mec', then='present', expr='happy'),
        k('M10#5', clip='bow', expr='happy'),
        k('M10:voulez', clip='giveItem', expr='happy')]),
    act('mec', [2.6, 0, -1.65], 180, 'idle', 'smug', keys=[
        k(0.1, to=[2.6, 0, -2.72], clip='strut', speed=1.05, faceEnd=180, then='idle'),
        k('M9:écrit', clip='drawOn'),
        k('M9:coffre+0.2', to=[3.35, 0, -2.6], clip='walk', speed=1.2, faceEnd=-60, then='present', expr='smug'),
        k('M10', face='banquier', turn=0.3, clip='handsOnHips', expr='smug'),
        k('M10:sac', clip='takeItem', expr='happy')]),
  ],
  'props': [P('marker', 'marker', on={'actor': 'mec', 'hand': 'R'}, keys=[k('M10', visible=False)]),
            P('nameVault', 'scrawl', pos=VAULT_TXT, opts={'text': 'CON', 'w': 0.7, 'h': 0.28, 'writeAt': 'M9:écrit+0.1', 'writeDur': 0.7}),
            P('sack', 'moneySack', scale=0.8, visible=False, on={'actor': 'banquier', 'hand': 'R'}, keys=[k('M10:voulez', visible=True), k('M10:sac+0.35', attach='mec', hand='R')])],
  'sfx': [{'at': 'M9:écrit+0.1', 'name': 'squeak', 'vol': 0.6}, {'at': 'M9:écrit+0.6', 'name': 'squeak', 'vol': 0.5}, {'at': 'M10:sac+0.35', 'name': 'cash', 'vol': 0.45}],
  'cams': [cam(0, 'mec', 'fs', worldAngle=75),
           cam('M9:écrit', 'mec', 'ms', worldAngle=-80),
           cam('M9:coffre+0.3', ['nameVault', 'mec'], 'ms', worldAngle=-10, elev=4),
           cam('M10', 'banquier', 'fs', angle=-50, move='track'),
           cam('M10#5', 'banquier', 'ms', angle=-40),
           cam('M10:voulez', ['banquier', 'mec'], 'ms', worldAngle=20)],
  'tail': 0.5,
})

# ---------------------------------------------------------------- 5. les flics : la voiture de police
CAR_X = 0.6
scenes.append({
  'id': 'flics', 'set': 'street', 'ambience': 'street',
  'lines': [L('M11', "Les flics sont venus l'arrêter. Il a écrit son nom sur la voiture de police.", highlight=['flics', 'police.']),
            L('M12', "On vous dépose où, chef ?", 'flic1', highlight=['chef'])],
  'actors': [
    act('mec', [-1.9, 0, -1.0], 90, 'idle', 'smug', keys=[
        k(0.05, to=[-0.85, 0, -1.1], clip='strut', speed=1.1, faceEnd=60, then='idle'),
        k('M11:arrêter+0.2', clip='handsOnHips', expr='smug'),
        k('M11:Il', to=[-1.6, -0.14, -1.85], clip='walk', speed=1.3, faceEnd=160, then='drawLow'),
        k('M12', to=[-2.4, 0, -1.15], clip='walk', speed=1.4, faceEnd='flic1', then='handsOnHips', expr='smug')]),
    act('flic1', [CAR_X + 0.7, -0.14, -2.2], 180, 'idle', 'angry', visible=False, keys=[
        k(1.05, visible=True),
        k(1.1, path=[[CAR_X + 0.4, -0.14, -1.7], [1.0, 0, -0.65]], clip='run', speed=3.0, faceEnd='mec', then='holdOut', expr='angry'),
        k('M11:nom', clip='stand', expr='suspicious', face='mec', turn=0.3),
        k('M11:police', clip='startle', expr='shocked'),
        k('M12', clip='salute', expr='happy'),
        k('M12.end', clip='present', expr='happy')]),
    act('flic2', [CAR_X - 0.25, -0.14, -2.2], 180, 'idle', 'angry', visible=False, keys=[
        k(1.12, visible=True),
        k(1.15, path=[[0.15, -0.14, -1.7], [0.3, 0, -0.2]], clip='run', speed=3.0, faceEnd='mec', then='point', expr='angry'),
        k('M11:nom', clip='stand', expr='suspicious', face='mec', turn=0.3),
        k('M11:police', clip='startle', expr='shocked'),
        k('M12:dépose', clip='salute', expr='happy')]),
  ],
  'props': [P('car', 'policeCar', pos=[-14, -0.14, -3.4], keys=[k(0, to=[CAR_X, -0.14, -3.4], dur=1.0, ease='out')]),
            P('sack', 'moneySack', scale=0.8, on={'actor': 'mec', 'hand': 'L'}),
            P('marker', 'marker', on={'actor': 'mec', 'hand': 'R'}, visible=False, keys=[k('M11:Il', visible=True), k('M12', visible=False)]),
            P('cuffs', 'handcuffs', on={'actor': 'flic1', 'hand': 'R'}, visible=False, keys=[k(1.05, visible=True), k('M11:police', visible=False)]),
            P('nameCar', 'scrawl', opts={'text': 'CON', 'w': 1.0, 'h': 0.38, 'writeAt': 'M11:nom+0.2', 'writeDur': 0.7}, on={'actor': 'car', 'offset': [-1.4, 0.72, 0.915]}),
            P('bus', 'busStop', pos=[-5.6, 0, -1.2]), WM(pos=[-8.2, 0, -1.3], opts={'kind': 'stand'})],
  'sfx': [{'at': 0.0, 'name': 'siren', 'vol': 0.45}, {'at': 0.55, 'name': 'brake', 'vol': 0.5},
          {'at': 1.02, 'name': 'carDoor', 'vol': 0.45}, {'at': 1.1, 'name': 'carDoor', 'vol': 0.4},
          {'at': 'M11:nom+0.2', 'name': 'squeak', 'vol': 0.6}, {'at': 'M11:nom+0.7', 'name': 'squeak', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'fs', worldAngle=15),
           cam('M11:venus+0.25', ['car', 'flic1', 'flic2'], 'fs', worldAngle=20, elev=8),
           cam('M11:arrêter+0.35', ['flic1', 'flic2', 'mec'], 'ms', worldAngle=-25),
           cam('M11:nom', ['mec', 'nameCar'], 'ms', worldAngle=35),
           cam('M12', 'flic1', 'mcu', angle=10),
           cam('M12:chef', ['mec', 'flic1', 'flic2', 'nameCar'], 'fs', worldAngle=15, elev=6)],
  'tail': 0.6,
})

# ---------------------------------------------------------------- 6. Monique : la mamie au marqueur
MX = -6.0
scenes.append({
  'id': 'monique', 'set': 'street', 'ambience': 'street',
  'lines': [L('M13', "Puis dans la rue, il a croisé une mamie. Elle avait un marqueur.", highlight=['mamie.', 'marqueur.']),
            L('M14', "Toi, tu portes mes courses.", 'mamie', pre=1.9, highlight=['courses.']),
            L('M15', "Depuis, ce mec appartient à Monique.", highlight=['Monique.'])],
  'actors': [
    act('mec', [MX - 2.4, 0, 0.85], 90, 'idle', 'smug', keys=[
        k(0.05, to=[MX - 0.62, 0, 0.85], clip='strut', speed=1.1, faceEnd=90, then='idle'),
        k('M13:Elle', expr='suspicious'),
        k('M13:marqueur', expr='shocked'),
        k('M13.end', clip='scared', expr='shocked'),
        k('M14-1.35', clip='kneel', expr='scared'),
        k('M14', expr='sad'),
        k('M14.end+0.15', clip='holdBags', expr='sad'),
        k('M15+0.35', path=[[MX + 0.6, 0, 1.05], [MX + 4.4, 0, 1.0]], clip='carryBags', speed=0.95, expr='sad')]),
    act('mamie', [MX + 1.6, 0, 0.85], -90, 'idle', 'neutral', keys=[
        k(0.05, to=[MX, 0, 0.85], clip='carryBags', speed=1.0, faceEnd=-90, then='holdBags'),
        k('M13:Elle', clip='stand', expr='unimpressed'),
        k('M13:avait', clip='showMarkerL', expr='angry'),
        k('M14-1.5', clip='pointDown', expr='angry'),
        k('M14-1.05', clip='drawOn', expr='unimpressed'),
        k('M14', clip='point', expr='unimpressed'),
        k('M15', path=[[MX + 1.6, 0, 1.0], [MX + 5.2, 0, 0.95]], clip='walk', speed=0.95, expr='happy')]),
    act('flic1', [MX + 2.0, 0, -0.6], 0, 'idle', 'neutral', keys=[k('M15:ce', clip='salute', face='mamie', turn=0.3, expr='happy')]),
    act('flic2', [MX + 3.0, 0, -0.7], 0, 'handsOnHips', 'neutral', keys=[k('M15:ce+0.15', clip='salute', face='mamie', turn=0.3, expr='happy')]),
  ],
  'props': [P('car', 'policeCar', pos=[MX + 3.2, -0.14, -3.4]),
            P('nameCar', 'scrawl', opts={'text': 'CON', 'w': 1.0, 'h': 0.38}, on={'actor': 'car', 'offset': [-1.4, 0.72, 0.915]}),
            P('sack', 'moneySack', scale=0.8, on={'actor': 'mec', 'hand': 'L'}, keys=[k('M13:marqueur', detach=True, fall=True, impact='thud')]),
            P('bagL', 'shoppingBag', on={'actor': 'mamie', 'hand': 'L'}, keys=[k('M13:Elle', detach=True, fall=True, impact='paper'), k('M14.end+0.15', attach='mec', hand='L')]),
            P('bagR', 'shoppingBag', opts={'text': 'MARCHÉ'}, on={'actor': 'mamie', 'hand': 'R'}, keys=[k('M13:Elle+0.1', detach=True, fall=True, impact='paper'), k('M14.end+0.15', attach='mec', hand='R')]),
            P('bigMarker', 'marker', opts={'color': RED_INK}, scale=2.2, visible=False, on={'actor': 'mamie', 'hand': 'L', 'offset': [0, -0.05, 0], 'rot': [3.1416, 0, 0]}, keys=[k('M13:avait', visible=True), k('M14-1.1', attach='mamie', hand='R', offset=[0, -0.09, 0], rot=[0, 0, 0]), k('M14', visible=False)]),
            P('nameMec', 'scrawl', opts={'text': 'MONIQUE', 'w': 0.17, 'h': 0.05, 'color': RED_INK, 'writeAt': 'M14-1.0', 'writeDur': 0.8},
              on={'actor': 'mec', 'joint': 'head', 'offset': FOREHEAD}),
            P('bus', 'busStop', pos=[MX - 4.0, 0, -1.2])],
  'sfx': [{'at': 'M14-1.0', 'name': 'squeak', 'vol': 0.6}, {'at': 'M14-0.55', 'name': 'squeak', 'vol': 0.5}],
  'cams': [cam(0, 'mec', 'ms', angle=50, move='track'),
           cam('M13:mamie', 'mamie', 'ms', angle=25),
           cam('M13:avait', 'mamie', 'mcu', angle=50),
           cam('M13.end', 'mec', 'cu', angle=-55),
           cam('M14-1.55', ['mamie', 'mec'], 'ms', worldAngle=0),
           cam('M14-0.6', 'mec', 'ecu', angle=40),
           cam('M14', 'mamie', 'mcu', angle=60),
           cam('M15', ['mamie', 'mec', 'flic1', 'flic2'], 'fs', worldAngle=10, elev=6)],
  'tail': 0.4,
})

# ---------------------------------------------------------------- 7. le salon : Monique mange son yaourt
scenes.append({
  'id': 'salon', 'set': 'livingRoom', 'ambience': None, 'lighting': 'interior',
  'lines': [L('M16', "Et Monique mange son yaourt.", pre=0.3, highlight=['yaourt.'])],
  'actors': [
    act('mamie', [-0.45, 0.23, -2.72], 0, 'sitEatSpoon', 'happy'),
    act('mec', [0.95, 0, -2.2], -10, 'holdBags', 'sad', keys=[k('M16:yaourt', clip='stareCamera', expr='unimpressed')]),
  ],
  'props': [P('yF', 'yogurt', opts={'name': 'CON', 'strike': True, 'name2': 'MONIQUE', 'inkColor2': RED_INK, 'open': True}, scale=1.3, on=CUP_L('mamie')),
            P('spoonF', 'spoon', on={'actor': 'mamie', 'hand': 'R'}),
            P('bagL', 'shoppingBag', on={'actor': 'mec', 'hand': 'L'}), P('bagR', 'shoppingBag', opts={'text': 'MARCHÉ'}, on={'actor': 'mec', 'hand': 'R'}),
            P('nameMec', 'scrawl', opts={'text': 'MONIQUE', 'w': 0.17, 'h': 0.05, 'color': RED_INK}, on={'actor': 'mec', 'joint': 'head', 'offset': FOREHEAD})],
  'cams': [cam(0, ['mamie', 'mec'], 'fs', worldAngle=0, elev=6),
           cam('M16:mange', 'yF', 'cu', worldAngle=-30, noOcclusion=True),
           cam('M16:yaourt+0.1', ['mec', 'mamie'], 'ms', worldAngle=12, move='push', amount=0.06)],
  'tail': 1.8,
})

ep = {
  'version': 3, 'title': 'Son nom dessus', 'captionWords': 3, 'captionY': 0.66,
  'voice': {'name': 'allan tiktok', 'model': 'eleven_v4',
            'narrator': {'stability': 0.8, 'style': 0.0, 'rate': 1.07},
            'character': {'stability': 0.4, 'style': 0.4, 'rate': 1.02}},
  'music': {'mood': 'quirky', 'vol': 0.06},
  'cast': {
    'mec': {'preset': 'lemec'}, 'madame': {'preset': 'madame'}, 'coll1': {'preset': 'lemec_glasses'},
    'patron': {'preset': 'boss', 'facial': 'none'}, 'banquier': {'preset': 'lemec_charcoal', 'tie': '#2C4A8A', 'seed': 5},
    'flic1': {'preset': 'cop'}, 'flic2': {'preset': 'cop2', 'seed': 41}, 'mamie': {'preset': 'mamie'},
  },
  'scenes': scenes,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'marqueur.json')
json.dump(ep, open(out, 'w'), ensure_ascii=False, indent=1)
words = sum(len(l['text'].split()) for s in scenes for l in s['lines'])
print(out, len(scenes), 'scenes,', sum(len(s['lines']) for s in scenes), 'lines,', words, 'words,', sum(len(s['cams']) for s in scenes), 'camera setups')
