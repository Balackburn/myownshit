#!/usr/bin/env python3
"""LE GORILLE — v3 storyboard (python3 scripts-fr/gorille3.py -> gorille3.json)

Narration = the user's text, word for word (only two caption typos fixed: "pas du tout", "toits").
Real names kept at the user's request (satire): Karim Bouamrane (Gus-Fring-style restaurant boss), Master Poulet.
One line is spoken by a character, same authorised voice, other intonation:
  "Mais vous aussi, on vous appelle les poulets."  -> the prisoner (the narrator only says "Et là, un mec leur a dit :").
Story logic fixed vs v2: the OTHER bodybuilder (le gros muscu) calls the police, not the gorilla-man.
No overlays at all (no banners / dates / symbols); captions only. Hidden 3D watermark on a few sets.

Every narrated action has a visible movement; characters face what they look at or talk to; every move faces its
direction (the director turns them); cameras are framed from the real bounding boxes with occlusion checks.
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

scenes = []
GSC = 1.3     # gorilla scale (day 1); they look bigger each time he comes back
# zoo day layout: fence z=4.2, visitor at the fence z=4.9, gorillas in the enclosure
G0, G1, G2 = [-2.6, 0, 0.3], [0.3, 0, -0.7], [2.8, 0, 0.1]
SACK = [-0.9, 0, 0.9]

# ------------------------------------------------------------------ 1. salon : la muscu après un TikTok
scenes.append({
  'id': 'salon', 'set': 'livingRoom', 'ambience': 'office',
  'lines': [L('g0', "Ce con s'était mis à la musculation une semaine plus tôt après avoir regardé un TikTok de merde.", highlight=['musculation', 'TikTok', 'merde.'])],
  'actors': [act('mec', [0.3, 0, -0.5], 0, 'curls', 'angry', params={'freq': 1.4}, keys=[
      k('g0:semaine', clip='flex', expr='unimpressed'),
      k('g0:après', clip='holdPhoneFront', expr='happy')])],
  'props': [P('db', 'dumbbell', on={'actor': 'mec', 'hand': 'R'}, keys=[k('g0:semaine', visible=False)]),
            P('db2', 'dumbbell', on={'actor': 'mec', 'hand': 'L'}, keys=[k('g0:semaine', visible=False)]),
            P('phone', 'phone911', opts={'screen': 'tiktok'}, visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('g0:après', visible=True)]),
            WM(anchor='picture', offset=[1.6, -0.35, 0.03])],
  'cams': [cam(0, 'mec', 'fs', angle=25, move='push', amount=0.08),
           cam('g0#4', 'mec', 'mcu', angle=-20),
           cam('g0:semaine', 'mec', 'ms', angle=35),
           cam('g0:après', 'mec', 'cu', angle=12, move='push'),
           cam('g0:TikTok', 'mec', 'mcu', angle=-35)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 2. zoo, jour 1 : les gorilles, la bouffe
def gor(i, pos, ry, clip='idle', expr='neutral', scale=GSC, keys=None, **kw):
    return act(f'g{i}', pos, ry, clip, expr, keys, scale=scale, **kw)
scenes.append({
  'id': 'zoo1', 'set': 'zoo', 'ambience': 'zoo',
  'lines': [L('g1', "Puis il est allé au zoo et là, il a vu les gorilles.", highlight=['zoo', 'gorilles.']),
            L('g2', "Ces putains de gorilles étaient énormes, des bras trois fois plus gros que les siens.", highlight=['énormes,', 'trois']),
            L('g3', "Ce con est devenu terriblement jaloux.", highlight=['jaloux.']),
            L('g4', "Il croyait qu'ils contractaient leurs muscles pour le provoquer alors que pas du tout.", highlight=['provoquer', 'tout.']),
            L('g5', "Il a voulu comprendre leur secret.", highlight=['secret.']),
            L('g6', "Première hypothèse : leur bouffe.", highlight=['bouffe.']),
            L('g7', "Il les a regardés manger leurs sac de nourriture pour primates.", highlight=['nourriture']),
            L('g8', "Purina High Protein.", highlight=['Purina', 'High', 'Protein.']),
            L('g9', "Avec ça, de la viande de chèvre vivantes, des œufs, du lait et du yaourt.", highlight=['chèvre', 'œufs,', 'lait', 'yaourt.'])],
  'actors': [
    act('mec', [-3.6, 0, 6.5], 90, 'idle', 'neutral', keys=[
        k(0.05, path=[[-1.2, 0, 6.2], [0.3, 0, 4.95]], clip='walk', faceEnd=180),
        k('g2:siens-0.5', clip='flex', expr='unimpressed'),
        k('g3', clip='angryFist', expr='angry'),
        k('g5', clip='binocs', expr='suspicious'),
        k('g7.end', clip='idle', expr='neutral')]),
    gor(0, G0, 15, 'chestBeat', 'smug', keys=[k('g2.end', clip='flex'), k('g4:alors', clip='yawnStretch', expr='sleepy'),
        k('g6', clip='sitFloorEat', expr='happy'), k('g9:œufs', clip='eatHands', expr='happy')]),
    gor(1, G1, 0, 'flex', 'smug', scale=GSC * 1.12, keys=[k('g2:bras', clip='posing'), k('g4', clip='flex', expr='smug'),
        k('g4:alors', clip='scratchButt', expr='neutral'), k('g6', clip='eatHands', expr='happy'), k('g9:yaourt', clip='drinkUp', expr='happy')]),
    gor(2, G2, -20, 'posing', 'smug', keys=[k('g4:alors', clip='lookAround', expr='neutral'), k('g6', clip='sitFloorEat', expr='happy'),
        k('g9:lait', clip='drinkUp', expr='happy')]),
    act('chevre', [1.6, 0, 1.9], -140, 'idle', 'scared', visible=False, keys=[k('g9', visible=True), k('g9:chèvre', to=[0.6, 0, 2.6], clip='walk', speed=1.4, faceEnd='g0'),
        k('g9:œufs', clip='idle', expr='scared')]),
  ],
  'props': [P('sack', 'foodSack', pos=SACK, ry=10, opts={'text': 'PURINA HIGH PROTEIN'}),
            P('binocs', 'binoculars', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('g5', visible=True), k('g7.end', visible=False)]),
            P('eggs', 'eggs', pos=[-1.7, 0, 1.4]),
            P('milk', 'milkBottle', visible=False, on={'actor': 'g2', 'hand': 'R'}, keys=[k('g9:lait', visible=True)]),
            P('yaourt', 'mug', opts={'color': '#FFFFFF'}, visible=False, on={'actor': 'g1', 'hand': 'R'}, keys=[k('g9:yaourt', visible=True)]),
            WM(pos=[3.6, 0, 5.4], ry=-15, opts={'kind': 'stand'})],
  'cams': [
    cam(0, 'mec', 'fs', angle=70, move='track'),
    cam('g1:vu', ots=['mec', 'g1', 1]),
    cam('g2', 'g1', 'ms', angle=0, elev=-14, lens=32),
    cam('g2:bras', ['g0', 'g1', 'g2'], 'fs', worldAngle=0, elev=-6, move='push', amount=0.06),
    cam('g2:siens-0.5', 'mec', 'ms', angle=15),
    cam('g3', 'mec', 'cu', angle=10, move='push'),
    cam('g4', pov=['mec', 'g1']),
    cam('g4:provoquer', 'g0', 'ms', angle=-10),
    cam('g4:alors', ['g0', 'g1', 'g2'], 'fs', worldAngle=8, elev=4),
    cam('g5', 'mec', 'cu', angle=8, move='push', amount=0.05),
    cam('g6', ['g0', 'g1', 'g2', 'sack'], 'fs', worldAngle=-10, elev=10),
    cam('g7', 'mec', 'ms', angle=-30),
    cam('g7:manger', 'g1', 'ms', angle=15),
    cam('g8', 'sack', 'cu', worldAngle=10, elev=8, noOcclusion=True),
    cam('g9', 'chevre', 'fs', angle=40, move='track'),
    cam('g9:œufs', 'g0', 'ms', angle=-20),
    cam('g9:lait', 'g2', 'ms', angle=10),
    cam('g9:yaourt', 'g1', 'mcu', angle=-15),
  ],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 3. cuisine : il mange comme eux
scenes.append({
  'id': 'cuisine', 'set': 'kitchenNight', 'ambience': 'night',
  'lines': [L('g10', "Alors, il a acheté la même chose et s'est mis à manger exactement comme eux.", highlight=['même', 'exactement'])],
  'actors': [act('mec', [0.2, 0, -1.3], 0, 'sitFloorEat', 'happy', params={'freq': 1.6}),
             act('chevre', [1.35, 0, -1.0], -90, 'idle', 'scared', keys=[k('g10:manger', clip='eat', expr='neutral')])],
  'props': [P('sack', 'foodSack', pos=[-0.75, 0, -1.6], ry=20, opts={'text': 'PURINA HIGH PROTEIN'}),
            P('eggs', 'eggs', pos=[0.9, 0, -0.3]), P('milk', 'milkBottle', pos=[1.15, 0, -0.1]), P('yaourt', 'mug', pos=[-0.3, 0, -0.4], opts={'color': '#FFFFFF'})],
  'cams': [cam(0, ['mec', 'chevre', 'sack'], 'fs', worldAngle=12, elev=12),
           cam('g10:manger', 'mec', 'mcu', angle=20, move='push'),
           cam('g10:comme', 'chevre', 'ms', angle=10)],
  'tail': 0.35,
})

# ------------------------------------------------------------------ 4. zoo, jour 2 : encore plus gros, acrobaties
GSC2 = 1.45
scenes.append({
  'id': 'zoo2', 'set': 'zoo', 'ambience': 'zoo',
  'lines': [L('g11', "Il est revenu au zoo, toujours pas assez musclé.", highlight=['musclé.']),
            L('g12', "Les gorilles étaient encore plus gros que lui.", highlight=['encore', 'gros']),
            L('g13', "Ça le rendait fou.", highlight=['fou.']),
            L('g14', "Deuxième hypothèse : les gorilles étaient à poil et faisaient des acrobaties toute la journée.", highlight=['poil', 'acrobaties'])],
  'actors': [
    act('mec', [3.6, 0, 6.5], -90, 'idle', 'neutral', keys=[
        k(0.05, path=[[1.4, 0, 6.1], [0.3, 0, 4.95]], clip='walk', faceEnd=180),
        k('g11:pas', clip='flex', expr='unimpressed'), k('g13', clip='tantrum', expr='angry'), k('g14', clip='idle', expr='suspicious'),
        k('g14:poil', clip='lookItem', expr='suspicious')]),
    gor(0, [-3.4, 0, 0.6], 15, 'posing', 'smug', scale=GSC2, keys=[k('g14', path=[[-0.8, 0, 1.4]], clip='cartwheel', params={'dur': 0.8}, dur=0.8, face='keep'),
        k('g14:acrobaties', path=[[-3.0, 0, 1.0]], clip='cartwheel', params={'dur': 0.8}, dur=0.8, face='keep'), k('g14:journée', clip='chestBeat')]),
    gor(1, G1, 0, 'flex', 'smug', scale=GSC2 * 1.12, keys=[k('g12:gros', clip='chestBeat'), k('g14:poil', clip='flip', params={'dur': 0.8}),
        k('g14:poil+0.85', clip='heroPose')]),
    gor(2, [3.1, 0.62, -1.25], 0, 'pullUp', 'neutral', scale=GSC2, params={'freq': 1.0}),
  ],
  'props': [P('bar', 'pullUpBar', pos=[3.1, 0, -1.25], opts={'height': 3.25, 'width': 1.5})],
  'cams': [
    cam(0, 'mec', 'fs', angle=-70, move='track'),
    cam('g11:pas', 'mec', 'ms', angle=10),
    cam('g12', ['g0', 'g1', 'g2'], 'fs', worldAngle=0, elev=-8, lens=34, move='push', amount=0.06),
    cam('g12:gros', 'g1', 'ms', angle=0, elev=-16, lens=30),
    cam('g13', 'mec', 'ms', angle=20),
    cam('g14', ['g0', 'g1'], 'fs', worldAngle=5, elev=6),
    cam('g14:poil', 'mec', 'cu', angle=15),
    cam('g14:faisaient', 'g1', 'fs', angle=10),
    cam('g14:acrobaties', 'g0', 'fs', angle=-20, move='track'),
    cam('g14:journée', 'g2', 'fs', angle=15),
  ],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 5. la rue : à poil, street workout, lampadaires
scenes.append({
  'id': 'rue', 'set': 'street', 'ambience': 'street',
  'lines': [L('g15', "Il s'est donc mis à se balader complètement à poil, en pleine rue.", highlight=['poil,', 'rue.']),
            L('g16', "Les gens le voyaient arriver et se barraient en courant.", highlight=['courant.']),
            L('g17', "Il faisait du street workout partout, des tractions, des acrobaties", highlight=['tractions,', 'acrobaties']),
            L('g18a', "et il se balançait de lampadaire en lampadaire", highlight=['lampadaire'])],
  'actors': [
    act('mecNu', [-6.0, 0, 0.7], 90, 'idle', 'smug', keys=[
        k(0.05, to=[-2.6, 0, 0.7], clip='strut', speed=1.1),
        k('g16:voyaient', clip='handsOnHips', expr='happy', face=90),
        k('g17', to=[-1.5, 0.12, 0.55], clip='walk', speed=1.4, then='pullUp', thenParams={'freq': 1.4}, faceEnd=0),
        k('g17:acrobaties', to=[-0.2, 0, 0.9], clip='walk', speed=1.6, then='flip', thenParams={'dur': 0.75}),
        k('g18a', to=[-4.5, 0, -0.9], clip='run', faceEnd=0, then='swingPole'),
        k('g18a:lampadaire#2', to=[0.5, 0, -0.9], clip='airborne', glide=True, dur=0.75, arc=1.4, face='move', land='stepHeavy', then='swingPole'),
        k('g18a.end+0.25', clip='swingPole', params={'side': -1})]),
    act('madame', [2.6, 0, 0.9], -90, 'walk', 'neutral', keys=[k(0.05, to=[1.2, 0, 0.9], clip='walk', speed=1.1),
        k('g16:voyaient', clip='startle', expr='shocked', face='mecNu'), k('g16:barraient', to=[8.0, 0, 1.6], clip='flee', expr='scared')]),
    act('mamie', [3.4, 0, 0.2], -90, 'walk', 'neutral', keys=[k(0.05, to=[2.0, 0, 0.2], clip='walk', speed=1.0),
        k('g16:arriver', clip='startle', expr='shocked', face='mecNu'), k('g16:barraient+0.2', to=[8.5, 0, 0.6], clip='flee', expr='scared')]),
    act('gamin', [1.6, 0, 1.5], -100, 'idle', 'happy', keys=[k('g16:voyaient', clip='doubleTake', expr='shocked', face='mecNu'),
        k('g16:courant', to=[7.5, 0, 2.2], clip='flee', expr='scared')]),
  ],
  'props': [P('bar', 'pullUpBar', pos=[-1.5, 0, 0.55], opts={'height': 2.55, 'width': 1.3}),
            P('lamp2', 'streetLamp', pos=[0.5, 0, -1.25], ry=90)],
  'cams': [
    cam(0, 'mecNu', 'fs', angle=20, move='track'),
    cam('g15:complètement', 'mecNu', 'mcu', angle=-15),
    cam('g15:pleine', ['mecNu', 'madame'], 'ws', worldAngle=10, elev=6),
    cam('g16', ['madame', 'mamie'], 'ms', angle=10),
    cam('g16:voyaient', 'madame', 'cu', angle=0),
    cam('g16:barraient', ['madame', 'mamie', 'gamin'], 'fs', worldAngle=-10, move='track'),
    cam('g17', 'mecNu', 'fs', angle=15),
    cam('g17:tractions', 'mecNu', 'ms', angle=-10, elev=-10),
    cam('g17:acrobaties', 'mecNu', 'fs', angle=30),
    cam('g18a', 'mecNu', 'fs', angle=40, move='track'),
    cam('g18a:lampadaire#2', 'mecNu', 'ws', worldAngle=0, elev=8, move='track'),
  ],
  'tail': 0.2,
})

scenes.append({
  'id': 'toits', 'set': 'rooftopPowerLine', 'ambience': 'street',
  'lines': [L('g18b', "et sur les toits des maisons en marchant comme un gorille.", highlight=['toits', 'gorille.'])],
  'actors': [act('mecNu', [-5.2, 0, -0.4], 90, 'knuckleWalk', 'happy', keys=[k(0.0, to=[3.6, 0, 0.6], clip='knuckleWalk', speed=1.5),
      k('g18b:gorille+0.1', clip='chestBeat', expr='happy', face=0)])],
  'props': [],
  'cams': [cam(0, 'mecNu', 'fs', angle=60, elev=4, move='track'),
           cam('g18b:marchant', 'mecNu', 'ms', angle=10, elev=-10),
           cam('g18b:gorille+0.1', 'mecNu', 'fs', angle=0, elev=-12, lens=32)],
  'tail': 0.6,
})

# ------------------------------------------------------------------ 6. zoo, jour 3 : furieux, il saute la barrière
GSC3 = 1.6
scenes.append({
  'id': 'zoo3', 'set': 'zoo', 'ambience': 'zoo',
  'lines': [L('g19', "Puis, retour au zoo, toujours moins musclé.", highlight=['moins']),
            L('g20', "Il était tellement furieux que maintenant, même les visiteurs le craignaient.", highlight=['furieux', 'visiteurs']),
            L('g21', "Alors, il a sauté la barrière et s'est installé directement dans l'enclos des gorilles.", highlight=['sauté', 'enclos']),
            L('g22', "Il mangeait et dormait avec eux pour trouver leur putain de secret.", highlight=['mangeait', 'dormait', 'secret.'])],
  'actors': [
    act('mec', [0.2, 0, 4.95], 180, 'flex', 'unimpressed', keys=[
        k('g20', clip='growl', expr='angry', face='madame'),
        k('g21', face=180, turn=0.25),
        k('g21:sauté', to=[0.2, 0, 3.4], clip='vault', glide=True, dur=0.75, arc=1.0, face='move', land='stepHeavy'),
        k('g21:installé', to=[-0.6, 0, 1.4], clip='walk', speed=1.5, then='sitFloor', faceEnd='g1'),
        k('g22', clip='sitFloorEat', expr='happy', face='g0'),
        k('g22:dormait', clip='sleepSide', expr='blink')]),
    act('madame', [1.6, 0, 5.1], -100, 'idle', 'neutral', keys=[k('g20:visiteurs', clip='scared', expr='scared', face='mec'),
        k('g20:craignaient', to=[5.5, 0, 6.8], clip='flee', expr='scared')]),
    act('gamin', [-1.3, 0, 5.2], 100, 'idle', 'happy', keys=[k('g20:visiteurs', clip='startle', expr='shocked', face='mec'),
        k('g20:craignaient+0.15', to=[-5.5, 0, 7.0], clip='flee', expr='scared')]),
    gor(0, G0, 20, 'flex', 'smug', scale=GSC3, keys=[k('g22', clip='sitFloorEat', expr='happy'), k('g22:dormait', clip='sleepSide', expr='closed')]),
    gor(1, G1, 0, 'chestBeat', 'smug', scale=GSC3 * 1.12, keys=[k('g21:installé', clip='idle', expr='suspicious', face='mec'), k('g22', clip='eatHands', expr='happy'),
        k('g22:dormait', clip='sleepSide', expr='closed')]),
    gor(2, G2, -20, 'posing', 'smug', scale=GSC3, keys=[k('g22', clip='sitFloorEat', expr='happy'), k('g22:dormait', clip='sleepSide', expr='closed')]),
  ],
  'props': [P('sack', 'foodSack', pos=SACK, ry=10, opts={'text': 'PURINA HIGH PROTEIN'})],
  'cams': [
    cam(0, 'mec', 'ms', angle=160, elev=6, allowBack=True),
    cam('g19:toujours', ['g0', 'g1', 'g2'], 'fs', worldAngle=0, elev=-10, lens=32),
    cam('g20', 'mec', 'mcu', angle=-25),
    cam('g20:visiteurs', ['madame', 'gamin', 'mec'], 'fs', worldAngle=170, elev=8),
    cam('g21', 'mec', 'fs', angle=90, elev=4),
    cam('g21:installé', 'mec', 'fs', angle=20, move='track'),
    cam('g22', ['mec', 'g0', 'g1'], 'fs', worldAngle=15, elev=10),
    cam('g22:dormait', ['mec', 'g0', 'g1', 'g2'], 'ws', worldAngle=0, elev=30),
    cam('g22:secret', 'mec', 'cu', angle=0, elev=40),
  ],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 7. zoo : plus poilus -> dopés
scenes.append({
  'id': 'zoo4', 'set': 'zoo', 'ambience': 'zoo',
  'lines': [L('g23', "Et là, il a remarqué un truc.", highlight=['truc.']),
            L('g24', "Ils étaient beaucoup plus poilus que lui.", highlight=['poilus']),
            L('g25', "Pour lui, aucun doute, ces bâtards devaient être dopés.", highlight=['bâtards', 'dopés.'])],
  'actors': [
    act('mec', [-0.6, 0, 1.4], 30, 'sitFloor', 'neutral', face='g1', keys=[
        k('g23', expr='suspicious'), k('g24', clip='lookItem', expr='unimpressed'), k('g24:poilus', look='g1'),
        k('g25', clip='idle', look=None, expr='suspicious'), k('g25:dopés', clip='pokeFinger', expr='angry', face='g1')]),
    gor(1, [0.5, 0, 0.3], -130, 'sitFloor', 'neutral', scale=GSC3 * 1.12, keys=[k('g24', clip='scratchButt', expr='neutral')]),
    gor(0, [-2.6, 0, 0.2], 60, 'sitFloorEat', 'happy', scale=GSC3),
  ],
  'props': [],
  'cams': [cam(0, 'mec', 'ms', angle=20), cam('g23:remarqué', 'mec', 'cu', angle=10, move='push'),
           cam('g24', ['mec', 'g1'], 'ms', worldAngle=-60),
           cam('g24:poilus', 'g1', 'mcu', angle=10),
           cam('g25', 'mec', 'ecu', angle=0, move='push', amount=0.05),
           cam('g25:dopés', ['mec', 'g1'], 'fs', worldAngle=100)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 8. zoo, nuit : sauf un ; le carton
ROCK = [2.6, 0, -3.0]           # big hiding rock (added for the night scenes)
scenes.append({
  'id': 'nuit1', 'set': 'zoo', 'setOpts': {'night': True}, 'ambience': 'night',
  'lines': [L('g26', "Il a attendu la nuit jusqu'à ce que tous les gorilles aient l'air de dormir.", highlight=['nuit', 'dormir.']),
            L('g27', "Sauf un.", highlight=['un.']),
            L('g28', "Le plus gros s'est levé discrètement et s'est caché derrière un rocher.", highlight=['discrètement', 'rocher.']),
            L('g29', "Le mec s'est planqué sous un carton, comme Snake dans Metal Gear Solid, et l'a suivi à petits pas.", highlight=['carton,', 'Snake']),
            L('g30', "Quand le gorille regardait derrière lui, il s'arrêtait net.", highlight=['net.'])],
  'actors': [
    act('mec', [-0.6, 0, 1.3], 90, 'lieBack', 'suspicious', keys=[
        k('g28:levé', clip='crouchHide', expr='suspicious', face='g1'),
        k('g29:planqué', clip='boxFreeze'),
        k('g29:suivi', to=[1.0, 0, -0.9], clip='boxSneak', speed=0.6),
        k('g30:regardait+0.15', clip='boxFreeze'),
        k('g30.end', to=[1.6, 0, -1.8], clip='boxSneak', speed=0.6)]),
    gor(0, [-2.6, 0, 0.2], 60, 'sleepSide', 'closed', scale=GSC3),
    gor(2, [2.0, 0, 1.2], -60, 'sleepSide', 'closed', scale=GSC3),
    gor(1, [0.6, 0, 0.0], 90, 'sleepSide', 'closed', scale=GSC3 * 1.12, keys=[
        k('g27', expr='suspicious'),
        k('g28:levé', clip='idle', expr='suspicious', face=200),
        k('g28:discrètement', path=[[1.6, 0, -1.4], [2.9, 0, -4.4]], clip='tiptoe', speed=1.0, faceEnd=20),
        k('g30:regardait', clip='lookBack', expr='suspicious'), k('g30:net+0.4', clip='crouchHide', expr='neutral')]),
  ],
  'props': [P('rock', 'rock', pos=ROCK, opts={'size': 2.6}),
            P('box', 'boxHide', visible=False, on={'actor': 'mec', 'joint': 'hips', 'offset': [0, -0.62, 0], 'rot': [0, 0, 0]}, keys=[k('g29:planqué', visible=True)])],
  'cams': [
    cam(0, ['mec', 'g0', 'g1', 'g2'], 'fs', worldAngle=10, elev=24),
    cam('g26:dormir', 'mec', 'cu', angle=0, elev=50),
    cam('g27', 'g1', 'cu', angle=0, elev=20),
    cam('g28', 'g1', 'fs', angle=40, move='track'),
    cam('g28:caché', 'g1', 'fs', worldAngle=0, elev=8),
    cam('g29', 'mec', 'ms', angle=20),
    cam('g29:Snake', 'mec', 'fs', angle=50, elev=6),
    cam('g29:suivi', ['mec', 'rock'], 'fs', worldAngle=60, move='track'),
    cam('g30', 'g1', 'ms', angle=0),
    cam('g30:arrêtait', 'mec', 'ms', angle=10, elev=4),
  ],
  'tail': 0.5,
})

# ------------------------------------------------------------------ 9. derrière le rocher : stéroïdes, pré-workout, la grotte
scenes.append({
  'id': 'nuit2', 'set': 'zoo', 'setOpts': {'night': True}, 'ambience': 'night',
  'lines': [L('g31', "Derrière le rocher, le gorille se piquait aux stéroïdes.", highlight=['stéroïdes.']),
            L('g32', "Ensuite, il prenait un pré-workout interdit qui contenait un dérivé de méthamphétamine.", highlight=['interdit', 'méthamphétamine.']),
            L('g33', "Puis, il est entré dans une grotte.", highlight=['grotte.']),
            L('g34', "Le mec l'a suivi, toujours sous son carton.", highlight=['carton.'])],
  'actors': [
    gor(1, [2.9, 0, -4.5], 20, 'injectArm', 'neutral', scale=GSC3 * 1.12, keys=[
        k('g31:stéroïdes', clip='wired', expr='shocked'),
        k('g32', clip='drinkUp', expr='happy'), k('g32:dérivé', clip='wired', expr='shocked'),
        k('g33', to=[3.6, 0, -6.3], clip='knuckleWalk', speed=1.4), k('g33.end+0.1', visible=False)]),
    act('mec', [1.6, 0, -1.8], 160, 'boxFreeze', 'suspicious', keys=[
        k('g34', path=[[2.6, 0, -4.9], [3.6, 0, -6.3]], clip='boxSneak', speed=1.1), k('g34.end+0.1', visible=False)]),
  ],
  'props': [P('rock', 'rock', pos=ROCK, opts={'size': 2.6}),
            P('box', 'boxHide', on={'actor': 'mec', 'joint': 'hips', 'offset': [0, -0.62, 0]}),
            P('syr', 'syringeBig', on={'actor': 'g1', 'hand': 'R'}, keys=[k('g32', visible=False)]),
            P('pre', 'preWorkout', visible=False, on={'actor': 'g1', 'hand': 'R'}, keys=[k('g32', visible=True), k('g33', visible=False)])],
  'cams': [
    cam(0, 'g1', 'ms', angle=0, elev=4),
    cam('g31:piquait', 'g1', 'mcu', angle=30),
    cam('g31:stéroïdes', ['g1', 'mec'], 'fs', worldAngle=200, elev=10, allowBack=True),
    cam('g32', 'g1', 'mcu', angle=-20),
    cam('g32:interdit', 'pre', 'cu', worldAngle=20, noOcclusion=True),
    cam('g32:dérivé', 'g1', 'cu', angle=0, move='push'),
    cam('g33', 'g1', 'fs', angle=140, elev=8, allowBack=True),
    cam('g34', 'mec', 'fs', angle=150, elev=10, allowBack=True, move='track'),
  ],
  'tail': 0.4,
})

# ------------------------------------------------------------------ 10. la salle secrète : 12 h d'entraînement, le coach
CLOCK = {'id': 'clock', 'name': 'wallClock', 'pos': [-1.6, 2.6, -3.55]}
scenes.append({
  'id': 'salle1', 'set': 'secretGym', 'ambience': 'gym',
  'lines': [L('g35', "À l'intérieur, une salle de musculation ultra-moderne cachée sous le zoo avec un coach privé.", highlight=['ultra-moderne', 'coach']),
            L('g36', "Le gorille s'est entraîné douze heures d'affilée, toute la nuit, sans s'arrêter.", highlight=['douze', 'heures']),
            L('g37', "Le coach lui faisait enchaîner les exercices.", highlight=['enchaîner']),
            L('g38', "Le mec regardait tout depuis son carton.", highlight=['carton.']),
            L('g39', "Il avait enfin compris pourquoi ces cons étaient aussi musclés.", highlight=['compris', 'cons'])],
  'actors': [
    gor(1, [-4.6, 0, 1.6], 90, 'knuckleWalk', 'neutral', scale=1.35, keys=[
        k(0.0, to=[2.4, 0, -1.2], clip='knuckleWalk', speed=1.6, faceEnd='coach'),
        k('g36', to=[3.4, 0.05, -1.4], clip='walk', speed=1.4, then='benchPress', thenParams={'freq': 1.3}, faceEnd=0),
        k('g37:faisait', to=[0.9, 0, -1.0], clip='walk', speed=1.8, then='deadlift', thenParams={'freq': 1.5}, faceEnd=20),
        k('g37:exercices', clip='curls', params={'freq': 1.8})]),
    act('coach', [1.4, 0, -0.4], -40, 'clipboard', 'neutral', keys=[k('g36', clip='clipboard', face='g1'),
        k('g37', clip='whistleBlow', expr='angry', face='g1', sfx='whistle'), k('g37:exercices', clip='point', face='g1')]),
    act('mec', [-3.2, 0, 1.9], 120, 'boxFreeze', 'suspicious', keys=[
        k('g38', face='g1', turn=0.6), k('g39', clip='stand', expr='happy', face=30)]),
  ],
  'props': [CLOCK | {'opts': {'rate': 0.05}, 'keys': [k('g36', scale=1.0)]},
            P('clock2', 'wallClock', pos=[-1.6, 2.6, -3.55], opts={'rate': 2.5}, visible=False, keys=[k('g36', visible=True)]),
            P('box', 'boxHide', on={'actor': 'mec', 'joint': 'hips', 'offset': [0, -0.62, 0]},
              keys=[k('g39', detach=True, to=[-3.2, 2.4, 1.9], dur=0.45, sfx='paper')]),
            P('whistle', 'whistle', on={'actor': 'coach', 'hand': 'R'}), P('clip', 'clipboardProp', on={'actor': 'coach', 'hand': 'L'}),
            P('bb', 'barbell', visible=False, on={'actor': 'g1', 'hand': 'R'}, keys=[k('g36', visible=True), k('g37:exercices', visible=False)]),
            P('db', 'dumbbell', visible=False, on={'actor': 'g1', 'hand': 'R'}, keys=[k('g37:exercices', visible=True)]),
            P('db2', 'dumbbell', visible=False, on={'actor': 'g1', 'hand': 'L'}, keys=[k('g37:exercices', visible=True)]),
            WM(anchor='mirror', offset=[1.7, 0.75, 0.07], opts={'kind': 'sticker'})],
  'cams': [
    cam(0, ['g1', 'coach'], 'ws', worldAngle=10, elev=10, move='push', amount=0.08),
    cam('g35:cachée', 'g1', 'fs', angle=30, move='track'),
    cam('g35:coach', 'coach', 'ms', angle=10),
    cam('g36', 'g1', 'fs', angle=50),
    cam('g36:heures', 'clock2', 'cu', worldAngle=0, noOcclusion=True),
    cam('g36:nuit', 'g1', 'ms', angle=70, elev=12),
    cam('g37', 'coach', 'mcu', angle=15),
    cam('g37:enchaîner', 'g1', 'fs', angle=20),
    cam('g37:exercices', 'g1', 'ms', angle=-10),
    cam('g38', 'mec', 'fs', angle=20),
    cam('g38:carton', ['mec', 'g1'], 'ws', worldAngle=150, elev=10),
    cam('g39', 'mec', 'cu', angle=5, move='push'),
  ],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 11. il fait pareil -> transformation
scenes.append({
  'id': 'salle2', 'set': 'secretGym', 'ambience': 'gym',
  'lines': [L('g40', "Il a donc fait exactement pareil.", highlight=['pareil.']),
            L('g41', "Les mêmes produits, les mêmes entraînements, le même putain de programme.", highlight=['produits,', 'entraînements,', 'programme.']),
            L('g42', "Et à force, il s'est lui-même transformé en gorille.", highlight=['transformé', 'gorille.'])],
  'actors': [
    act('mec', [0.6, 0, -0.6], 0, 'injectArm', 'neutral', keys=[
        k('g41', clip='drinkUp', expr='happy'),
        k('g41:entraînements', to=[3.4, 0.05, -1.4], clip='walk', speed=1.8, then='benchPress', thenParams={'freq': 1.4}, faceEnd=0),
        k('g41:programme', to=[0.6, 0, -0.4], clip='walk', speed=1.9, then='curls', thenParams={'freq': 1.6}, faceEnd=0),
        k('g42:transformé', visible=False)]),
    act('mecG', [0.6, 0, -0.4], 0, 'curls', 'angry', scale=1.25, visible=False, keys=[k('g42:transformé', visible=True), k('g42:gorille', clip='heroPose', expr='smug')]),
    act('coach', [-1.2, 0, 0.4], 60, 'clipboard', 'neutral', face='mec', keys=[k('g41:programme', clip='whistleBlow', expr='angry', sfx='whistle')]),
  ],
  'props': [P('syr', 'syringeBig', on={'actor': 'mec', 'hand': 'R'}, keys=[k('g41', visible=False)]),
            P('pre', 'preWorkout', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('g41', visible=True), k('g41:entraînements', visible=False)]),
            P('bb', 'barbell', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('g41:entraînements', visible=True), k('g41:programme', visible=False)]),
            P('db', 'dumbbell', visible=False, on={'actor': 'mec', 'hand': 'R'}, keys=[k('g41:programme', visible=True), k('g42:transformé', visible=False)]),
            P('dbG', 'dumbbell', visible=False, on={'actor': 'mecG', 'hand': 'R'}, keys=[k('g42:transformé', visible=True), k('g42:gorille', visible=False)]),
            P('whistle', 'whistle', on={'actor': 'coach', 'hand': 'R'}), CLOCK | {'opts': {'rate': 1.0}}],
  'fx': [{'type': 'flash', 'at': 'g42:transformé', 'dur': 0.25}, {'type': 'shake', 'at': 'g42:transformé', 'dur': 0.3, 'amount': 0.04}],
  'sfx': [{'at': 'g42:transformé', 'name': 'poof', 'vol': 0.8}, {'at': 'g42:gorille', 'name': 'roar', 'vol': 0.5}],
  'cams': [
    cam(0, 'mec', 'ms', angle=20), cam('g40:fait', 'mec', 'cu', angle=-15),
    cam('g41', 'mec', 'mcu', angle=25),
    cam('g41:entraînements', 'mec', 'fs', angle=60),
    cam('g41:programme', ['mec', 'coach'], 'fs', worldAngle=-20),
    cam('g42', 'mec', 'ms', angle=10),
    cam('g42:transformé', 'mecG', 'ms', angle=10, move='pull'),
    cam('g42:gorille', 'mecG', 'fs', angle=0, elev=-12, lens=32),
  ],
  'tail': 0.5,
})

# ------------------------------------------------------------------ 12. zoo : un gorille parmi les autres
scenes.append({
  'id': 'zoo5', 'set': 'zoo', 'ambience': 'zoo',
  'lines': [L('g44', "Sauf qu'il ne voulait pas être un gorille parmi les autres.", highlight=['parmi']),
            L('g45', "Il voulait être le plus musclé de tous.", highlight=['plus', 'tous.'])],
  'actors': [
    gor(0, [-2.2, 0, 0.6], 0, 'idle', 'neutral', scale=1.25), gor(2, [2.2, 0, 0.6], 0, 'idle', 'neutral', scale=1.25),
    gor(1, [1.1, 0, -0.4], 0, 'idle', 'neutral', scale=1.25),
    act('mecG', [-0.6, 0, 0.3], 0, 'idle', 'unimpressed', scale=1.25, keys=[k('g44:gorille', clip='lookAround'),
        k('g45', clip='angryFist', expr='angry'), k('g45:musclé', clip='flex', expr='smug')]),
  ],
  'props': [],
  'cams': [cam(0, ['g0', 'mecG', 'g1', 'g2'], 'fs', worldAngle=0, elev=6, move='push', amount=0.08),
           cam('g44:gorille', 'mecG', 'mcu', angle=10),
           cam('g45', 'mecG', 'cu', angle=-10, move='push'),
           cam('g45:musclé', 'mecG', 'ms', angle=10, elev=-14, lens=32)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 13. triple dose, une semaine non-stop -> énorme
scenes.append({
  'id': 'salle3', 'set': 'secretGym', 'ambience': 'gym',
  'lines': [L('g46', "Alors, il a triplé la dose de chaque produit.", highlight=['triplé']),
            L('g47', "Puis, il s'est entraîné pendant une semaine entière sans aucune pause, jour et nuit.", highlight=['semaine', 'pause,']),
            L('g48', "Tout passait en accéléré.", highlight=['accéléré.']),
            L('g49', "Lui continuait.", highlight=['continuait.']),
            L('g50', "Il est devenu énorme.", highlight=['énorme.'])],
  'actors': [
    act('mecG', [0.6, 0, -0.6], 0, 'injectButt', 'shocked', scale=1.25, keys=[
        k('g46:dose', clip='drinkUp', expr='happy'), k('g46:produit', clip='wired', expr='shocked'),
        k('g47', to=[3.4, 0.05, -1.4], clip='walk', speed=1.7, then='benchPress', thenParams={'freq': 1.5}, faceEnd=0),
        k('g48', to=[0.6, 0, -0.6], clip='walk', speed=1.8, then='curls', thenParams={'freq': 1.4}, faceEnd=0),
        k('g50', scale=2.0, dur=1.1, ease='out', clip='heroPose', expr='smug', sfx='grunt')]),
    act('coach', [-1.4, 0, 0.6], 40, 'clipboard', 'neutral', face='mecG', keys=[
        k('g47:jour', clip='sleepSide', expr='blink'),
        k('g48', path=[[-3.0, 0, 1.6], [-1.0, 0, 2.4], [1.8, 0, 1.6], [-1.4, 0, 0.6]], clip='run', speed=6.0, faceEnd='mecG'),
        k('g49', clip='yawnStretch', speed=3.0, expr='sleepy'), k('g50', clip='scared', speed=1.0, expr='shocked', face='mecG')]),
  ],
  'props': [P('syr1', 'syringeBig', on={'actor': 'mecG', 'hand': 'R'}, keys=[k('g46:dose', visible=False)]),
            P('syr2', 'syringeBig', on={'actor': 'mecG', 'hand': 'R', 'offset': [0.06, 0, 0.05]}, keys=[k('g46:dose', visible=False)]),
            P('syr3', 'syringeBig', on={'actor': 'mecG', 'hand': 'R', 'offset': [-0.06, 0, 0.05]}, keys=[k('g46:dose', visible=False)]),
            P('pre', 'preWorkout', visible=False, on={'actor': 'mecG', 'hand': 'R'}, keys=[k('g46:dose', visible=True), k('g47', visible=False)]),
            P('bb', 'barbell', visible=False, on={'actor': 'mecG', 'hand': 'R'}, opts={'width': 2.0}, keys=[k('g47', visible=True), k('g48', visible=False)]),
            P('db', 'dumbbell', visible=False, on={'actor': 'mecG', 'hand': 'R'}, keys=[k('g48', visible=True), k('g50', visible=False)]),
            P('db2', 'dumbbell', visible=False, on={'actor': 'mecG', 'hand': 'L'}, keys=[k('g48', visible=True), k('g50', visible=False)]),
            CLOCK | {'opts': {'rate': 0.05}, 'keys': [k('g47', visible=False)]},
            P('clockFast', 'wallClock', pos=[-1.6, 2.6, -3.55], opts={'rate': 6.0}, visible=False, keys=[k('g47', visible=True)])],
  'daynight': {'from': 'g47:jour', 'period': 0.6},
  'cams': [
    cam(0, 'mecG', 'ms', angle=20), cam('g46:dose', 'mecG', 'mcu', angle=-20), cam('g46:produit', 'mecG', 'cu', angle=0, move='push'),
    cam('g47', 'mecG', 'fs', angle=50),
    cam('g47:semaine', 'clockFast', 'cu', worldAngle=0, noOcclusion=True),
    cam('g47:pause', 'mecG', 'ms', angle=80, elev=14),
    cam('g47:jour', ['mecG', 'coach'], 'ws', worldAngle=20, elev=12),
    cam('g48', ['mecG', 'coach'], 'fs', worldAngle=0, elev=8),
    cam('g49', 'mecG', 'mcu', angle=15, move='push'),
    cam('g50', 'mecG', 'fs', angle=0, elev=-16, lens=30, move='pull', amount=0.15),
  ],
  'tail': 0.6,
})

# ------------------------------------------------------------------ 14. zoo : débutants, la rouste, l'alpha
scenes.append({
  'id': 'zoo6', 'set': 'zoo', 'ambience': 'zoo',
  'lines': [L('g51', "Les autres gorilles avaient l'air de débutants.", highlight=['débutants.']),
            L('g52', "Il s'est battu contre eux et leur a foutu une rouste un par un.", highlight=['rouste']),
            L('g53', "Il a battu tout le monde, est devenu l'alpha et s'est mis à vivre comme le chef de l'enclos.", highlight=["l'alpha", 'chef'])],
  'actors': [
    act('mecG', [0.2, 0, -1.6], 0, 'chestBeat', 'smug', scale=2.0, keys=[
        k('g52', face='g0', turn=0.2, clip='windupPunch', sfx='punch', sfxAt=0.45),
        k('g52:rouste', face='g1', turn=0.2, clip='windupPunch', sfx='punch', sfxAt=0.45),
        k('g52:par', face='g2', turn=0.2, clip='windupPunch', sfx='punch', sfxAt=0.45),
        k('g53', to=[2.2, 0, -2.2], clip='strut', speed=1.2, then='sit', faceEnd=0),
        k('g53:chef', clip='heroPose', expr='smug')]),
    gor(0, [-1.6, 0, -0.4], 60, 'curls', 'worried', scale=1.25, params={'freq': 0.6}, keys=[
        k('g52+0.45', to=[-3.6, 0, 0.6], clip='hitFly', glide=True, dur=0.55, arc=0.8, face='keep', land='thud', then='koFloor'),
        k('g53:alpha', clip='kneelBow', expr='sad', face='mecG')]),
    gor(1, [0.3, 0, 0.4], 0, 'curls', 'worried', scale=1.25, params={'freq': 0.7}, keys=[
        k('g52:rouste+0.45', to=[0.6, 0, 2.6], clip='hitFly', glide=True, dur=0.55, arc=0.8, face='keep', land='thud', then='koFloor'),
        k('g53:mis', to=[1.6, 0, -1.2], clip='walk', speed=1.2, then='fan', faceEnd='mecG', expr='sad')]),
    gor(2, [2.0, 0, -0.2], -60, 'curls', 'worried', scale=1.25, params={'freq': 0.5}, keys=[
        k('g52:par+0.45', to=[4.0, 0, 0.8], clip='hitFly', glide=True, dur=0.55, arc=0.8, face='keep', land='thud', then='koFloor'),
        k('g53:vivre', to=[3.1, 0, -1.3], clip='walk', speed=1.2, then='giveItem', faceEnd='mecG', expr='sad')]),
  ],
  'props': [P('rock', 'rock', pos=[2.2, 0, -2.75], opts={'size': 1.1}),
            P('crown', 'crown', visible=False, on={'actor': 'mecG', 'joint': 'head', 'offset': [0, 0.42, 0.06]}, keys=[k('g53:alpha', visible=True)]),
            P('leaf', 'leafFan', visible=False, on={'actor': 'g1', 'hand': 'R'}, keys=[k('g53:mis', visible=True)]),
            P('banane', 'banana', visible=False, on={'actor': 'g2', 'hand': 'R'}, keys=[k('g53:vivre', visible=True)]),
            P('d0', 'dumbbell', on={'actor': 'g0', 'hand': 'R'}, scale=0.6, keys=[k('g52+0.45', visible=False)]),
            P('d1', 'dumbbell', on={'actor': 'g1', 'hand': 'R'}, scale=0.6, keys=[k('g52:rouste+0.45', visible=False)]),
            P('d2', 'dumbbell', on={'actor': 'g2', 'hand': 'R'}, scale=0.6, keys=[k('g52:par+0.45', visible=False)])],
  'cams': [
    cam(0, ['g0', 'g1', 'g2'], 'fs', worldAngle=0, elev=4),
    cam('g51:débutants', 'mecG', 'fs', angle=0, elev=-14, lens=30),
    cam('g52', ['mecG', 'g0'], 'fs', worldAngle=-40, elev=6),
    cam('g52+0.5', 'g0', 'fs', angle=60, move='track'),
    cam('g52:rouste', ['mecG', 'g1'], 'fs', worldAngle=30, elev=6),
    cam('g52:rouste+0.5', 'g1', 'fs', angle=0, move='track'),
    cam('g52:par', ['mecG', 'g2'], 'fs', worldAngle=60, elev=6),
    cam('g52:par+0.5', ['g0', 'g1', 'g2'], 'ws', worldAngle=0, elev=20),
    cam('g53', 'mecG', 'fs', angle=40, move='track'),
    cam('g53:alpha', 'mecG', 'ms', angle=0, elev=-10, lens=32),
    cam('g53:vivre', ['mecG', 'g1', 'g2'], 'fs', worldAngle=0, elev=8),
    cam('g53:chef', 'mecG', 'mcu', angle=10, move='push'),
  ],
  'tail': 0.4,
})

# ------------------------------------------------------------------ 15. le gros muscu arrive, jaloux, il appelle la police
scenes.append({
  'id': 'zoo7', 'set': 'zoo', 'ambience': 'zoo',
  'lines': [L('g54', "Puis, un autre gros muscu est arrivé au zoo.", highlight=['muscu']),
            L('g55', "Il a vu son physique, est devenu jaloux et a cru qu'il le provoquait.", highlight=['jaloux', 'provoquait.']),
            L('g56', "Alors, il a appelé la police.", highlight=['police.']),
            L('g57', "Les flics sont arrivés en urgence et ont arrêté tous les gorilles pour dopage et possession de stéroïdes.", highlight=['dopage', 'stéroïdes.'])],
  'actors': [
    act('muscu', [-5.5, 0, 6.6], 90, 'idle', 'smug', keys=[
        k(0.05, path=[[-1.6, 0, 6.2], [-0.4, 0, 4.95]], clip='strut', speed=1.2, faceEnd=180),
        k('g55:jaloux', clip='angryFist', expr='angry'),
        k('g55:provoquait', clip='flex', expr='angry'),
        k('g56:appelé', clip='phoneCall', expr='angry'),
        k('g57', clip='handsOnHips', expr='smug', face=90)]),
    act('mecG', [2.2, 0, -2.2], 0, 'sit', 'neutral', scale=2.0, keys=[
        k('g55', clip='yawnStretch', expr='sleepy'), k('g55:provoquait', clip='scratchButt', expr='neutral'),
        k('g57:arrêté', clip='cuffedBack', expr='unimpressed')]),
    gor(0, [-1.6, 0, -0.6], 30, 'kneelBow', 'sad', scale=1.25, keys=[k('g57:arrêté', clip='cuffedBack', expr='sad')]),
    gor(1, [1.0, 0, -1.4], 60, 'fan', 'sad', scale=1.25, keys=[k('g57:arrêté', clip='cuffedBack', expr='sad')]),
    act('flic1', [-8, 0, 7.4], 90, 'run', 'angry', visible=False, keys=[k('g57+0.6', visible=True),
        k('g57+0.6', path=[[-1.8, 0, 6.0], [-1.2, 0, 3.4], [-1.5, 0, 0.6]], clip='run', speed=3.6, faceEnd='g0'),
        k('g57:arrêté', clip='cuffOther', expr='angry', sfx='cuff', sfxAt=0.3)]),
    act('flic2', [-8.6, 0, 7.9], 90, 'run', 'angry', visible=False, keys=[k('g57+0.8', visible=True),
        k('g57+0.8', path=[[-0.8, 0, 6.2], [0.2, 0, 3.4], [1.1, 0, -0.5]], clip='run', speed=3.8, faceEnd='g1'),
        k('g57:arrêté+0.3', clip='cuffOther', expr='angry', sfx='cuff', sfxAt=0.3)]),
    act('flic3', [-9.2, 0, 8.3], 90, 'run', 'angry', visible=False, keys=[k('g57+1.0', visible=True),
        k('g57+1.0', path=[[0.6, 0, 6.3], [1.6, 0, 3.4], [2.2, 0, -1.2]], clip='run', speed=4.0, faceEnd='mecG'),
        k('g57:dopage', clip='clipboard', expr='suspicious')]),
  ],
  'props': [P('phone', 'phone911', opts={'text': '17'}, visible=False, on={'actor': 'muscu', 'hand': 'R'}, keys=[k('g56:appelé', visible=True), k('g57', visible=False)]),
            P('crown', 'crown', on={'actor': 'mecG', 'joint': 'head', 'offset': [0, 0.42, 0.06]}),
            P('leaf', 'leafFan', on={'actor': 'g1', 'hand': 'R'}, keys=[k('g57:arrêté', visible=False)]),
            P('car', 'policeCar', pos=[-16, 0, 8.2], ry=90, keys=[k('g57', to=[-3.2, 0, 8.2], dur=1.1, ease='out', sfx='brake')]),
            P('bag', 'evidenceBag', visible=False, on={'actor': 'flic3', 'hand': 'R'}, keys=[k('g57:possession', visible=True)])],
  'sfx': [{'at': 'g57', 'name': 'siren', 'vol': 0.5}],
  'cams': [
    cam(0, 'muscu', 'fs', angle=60, move='track'),
    cam('g54:arrivé', 'muscu', 'ms', angle=15, elev=-10, lens=32),
    cam('g55', ots=['muscu', 'mecG', 1]),
    cam('g55:jaloux', 'muscu', 'cu', angle=10, move='push'),
    cam('g55:provoquait', 'mecG', 'ms', angle=10),
    cam('g56', 'muscu', 'mcu', angle=-20),
    cam('g56:police', 'muscu', 'cu', angle=25),
    cam('g57', 'car', 'fs', worldAngle=20, elev=6, withProps=True),
    cam('g57:arrivés+0.4', ['flic1', 'flic2', 'flic3'], 'fs', worldAngle=170, elev=10, move='track', allowBack=True),
    cam('g57:arrêté', ['flic1', 'g0', 'flic2', 'g1'], 'fs', worldAngle=10, elev=6),
    cam('g57:dopage', 'mecG', 'ms', angle=0),
    cam('g57:stéroïdes', 'bag', 'cu', worldAngle=30, noOcclusion=True),
  ],
  'tail': 0.4,
})

# ------------------------------------------------------------------ 16. le labo : le chimiste (Walter White)
scenes.append({
  'id': 'labo', 'set': 'lab', 'ambience': 'lab',
  'lines': [L('g58', "En remontant l'affaire, ils ont trouvé le chimiste qui fabriquait les produits.", highlight=['chimiste']),
            L('g59', "Un gorille chauve avec des lunettes et un chapeau.", highlight=['chauve', 'lunettes', 'chapeau.']),
            L('g60', "Walter White.", highlight=['Walter', 'White.']),
            L('g61', "Ils l'ont arrêté aussi.", highlight=['arrêté'])],
  'actors': [
    act('chimiste', [0.0, 0, -1.8], 0, 'pour', 'neutral', scale=1.2, keys=[
        k('g58:trouvé', clip='idle', expr='suspicious', face='flic1'),
        k('g59:chauve', clip='raiseOverhead', expr='neutral', face=0), k('g59:lunettes', clip='idle'),
        k('g60', clip='stareCamera', expr='angry'), k('g61', clip='cuffedBack', expr='unimpressed')]),
    act('flic1', [-4.2, 0, 2.2], 60, 'run', 'angry', keys=[k(0.05, to=[-1.4, 0, -0.4], clip='run', speed=3.0, faceEnd='chimiste', then='point'),
        k('g61', to=[-0.55, 0, -1.6], clip='walk', speed=1.6, faceEnd='chimiste', then='cuffOther', sfx='cuff', vol=0.5)]),
    act('flic2', [-4.8, 0, 2.6], 60, 'run', 'angry', keys=[k(0.35, to=[-2.3, 0, 0.1], clip='run', speed=3.0, faceEnd='chimiste', then='surrender')]),
  ],
  'props': [P('hat', 'porkpieHat', on={'actor': 'chimiste', 'joint': 'head', 'offset': [0, 0.43, 0.06]},
              keys=[k('g59:chauve', detach=True, to=[0, 2.6, -1.62], dur=0.35), k('g59:chapeau', attach='chimiste', joint='head', offset=[0, 0.43, 0.06])]),
            P('bald', 'baldCap', on={'actor': 'chimiste', 'joint': 'head', 'offset': [0, 0.38, 0.06]}),
            P('lunettes', 'glasses', on={'actor': 'chimiste', 'joint': 'head', 'offset': [0, 0.27, 0.26]}, opts={'r': 0.055, 'dx': 0.075}),
            P('flask', 'milkBottle', opts={'color': '#9FE0D0'}, on={'actor': 'chimiste', 'hand': 'R'}, keys=[k('g58:trouvé', visible=False)])],
  'cams': [
    cam(0, ['flic1', 'flic2'], 'fs', angle=20, move='track'),
    cam('g58:trouvé', 'chimiste', 'ms', angle=10),
    cam('g58:fabriquait', ots=['flic1', 'chimiste', 1]),
    cam('g59', 'chimiste', 'mcu', angle=0),
    cam('g59:lunettes', 'chimiste', 'cu', angle=15, move='push'),
    cam('g60', 'chimiste', 'ecu', angle=0, move='push', amount=0.08),
    cam('g61', ['flic1', 'chimiste'], 'ms', worldAngle=20),
  ],
  'tail': 0.4,
})

# ------------------------------------------------------------------ 17. le réseau -> Karim Bouamrane, Master Poulet
scenes.append({
  'id': 'tableau', 'set': 'policeStation', 'ambience': 'station',
  'lines': [L('g62', "Walter White leur a permis de remonter jusqu'au réseau de distribution.", highlight=['réseau'])],
  'actors': [act('chimiste', [1.4, 0, -2.6], 30, 'cuffedFront', 'unimpressed', scale=1.2, keys=[k('g62:permis', clip='pokeFinger', face='board')]),
             act('flic1', [2.9, 0, -2.4], -60, 'drawOn', 'suspicious', face='board', keys=[k('g62:réseau', clip='thinkChin')])],
  'props': [P('board', 'mapBoard', pos=[2.1, 1.75, -3.52]),
            P('hat', 'porkpieHat', on={'actor': 'chimiste', 'joint': 'head', 'offset': [0, 0.43, 0.06]}),
            P('lunettes', 'glasses', on={'actor': 'chimiste', 'joint': 'head', 'offset': [0, 0.27, 0.26]}, opts={'r': 0.055, 'dx': 0.075})],
  'cams': [cam(0, ['chimiste', 'flic1'], 'fs', worldAngle=-10),
           cam('g62:remonter', 'board', 'ms', worldAngle=0, noOcclusion=True, move='push', amount=0.1)],
  'tail': 0.3,
})

scenes.append({
  'id': 'meeting', 'set': 'street', 'ambience': 'street',
  'lines': [L('g63', "Le responsable s'appelait Karim Bouamrane.", highlight=['Karim', 'Bouamrane.']),
            L('g64', "Il prétendait être opposé au restaurant de poulet.", highlight=['opposé'])],
  'actors': [act('karim', [0, 0, -0.4], 0, 'podium', 'unimpressed', keys=[k('g63:Karim', clip='stareCamera', expr='unimpressed'),
                 k('g64', clip='podium', expr='angry'), k('g64:opposé', clip='shakeHead', expr='angry'), k('g64:poulet', clip='point', expr='angry')]),
             act('madame', [-1.4, 0, 1.8], 150, 'holdOut', 'neutral', face='karim'),
             act('gamin', [1.3, 0, 2.0], -160, 'idle', 'neutral', face='karim')],
  'props': [P('pod', 'podium', pos=[0, 0, 0.15], opts={'text': 'NON AU POULET'}),
            P('mic', 'phone911', on={'actor': 'madame', 'hand': 'R'})],
  'cams': [cam(0, 'karim', 'ms', angle=0, move='push', amount=0.06),
           cam('g63:Karim', 'karim', 'cu', angle=0),
           cam('g64', ['karim', 'madame', 'gamin'], 'fs', worldAngle=160, elev=8, allowBack=True),
           cam('g64:opposé', 'karim', 'mcu', angle=-15)],
  'tail': 0.3,
})

scenes.append({
  'id': 'restaurant', 'set': 'restaurant', 'ambience': 'bar',
  'lines': [L('g65', "En réalité, il était derrière Master Poulet et faisait circuler les produits dans ce réseau.", highlight=['Master', 'Poulet']),
            L('g66', "Les flics l'ont arrêté, mais ils soupçonnaient un trafic beaucoup plus vaste.", highlight=['vaste.'])],
  'actors': [
    act('karim', [-0.3, 0, -1.4], 20, 'wipeGlass', 'unimpressed', keys=[
        k('g65:Master', clip='giveItem', expr='smug', face='serveur'),
        k('g66', clip='surrender', expr='shocked', face='flic1'), k('g66:arrêté+0.3', clip='cuffedBack', expr='unimpressed')]),
    act('serveur', [1.1, 0, -0.8], -110, 'idle', 'neutral', face='karim', keys=[
        k('g65:Master+0.4', clip='takeItem', expr='happy'), k('g65:circuler', to=[4.6, 0, 1.8], clip='walk', speed=1.4)]),
    act('flic1', [-4.5, 0, 2.6], 60, 'run', 'angry', visible=False, keys=[k('g66', visible=True),
        k('g66', to=[-1.1, 0, -0.9], clip='run', speed=3.6, faceEnd='karim', then='cuffOther', sfx='cuff', vol=0.5),
        k('g66:soupçonnaient', clip='thinkChin', expr='suspicious', face=0)]),
  ],
  'props': [P('bucket', 'chickenBucket', on={'actor': 'karim', 'hand': 'R'}, visible=False, keys=[k('g65:Master', visible=True), k('g65:Master+0.55', attach='serveur', hand='R')]),
            P('syrB', 'syringeBig', on={'actor': 'bucket', 'offset': [0.04, 0.32, 0.0], 'rot': [0.3, 0, 0.2]}, visible=False, keys=[k('g65:Master', visible=True)]),
            P('glass', 'beerGlass', on={'actor': 'karim', 'hand': 'L'}, keys=[k('g65:Master', visible=False)]),
            P('sign', 'signBoard', pos=[-1.6, 2.35, -3.5], opts={'text': 'MASTER POULET', 'bg': '#B5302A', 'fg': '#FFE7A0', 'w': 2.2, 'h': 0.55, 'posts': False, 'height': 0}),
            P('b2', 'chickenBucket', pos=[3.6, 0.79, -1.6]), P('b3', 'chickenBucket', pos=[-3.6, 0.79, -1.4]),
            WM(anchor='menu', offset=[0.0, -0.7, 0.07], opts={'kind': 'sticker'})],
  'cams': [
    cam(0, 'karim', 'ms', angle=10),
    cam('g65:derrière', ['karim', 'serveur'], 'fs', worldAngle=-20, elev=6),
    cam('g65:Master', 'bucket', 'cu', worldAngle=-30, noOcclusion=True),
    cam('g65:circuler', 'serveur', 'fs', angle=30, move='track'),
    cam('g66', ['karim', 'flic1'], 'fs', worldAngle=10, elev=6),
    cam('g66:arrêté+0.3', 'karim', 'mcu', angle=0),
    cam('g66:soupçonnaient', 'flic1', 'cu', angle=10, move='push'),
  ],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 18. les fermes : hormones, poulets trop musclés
CH = [[1.5, 0, -1.8], [-1.0, 0, -2.4], [3.4, 0, -1.0]]
scenes.append({
  'id': 'ferme', 'set': 'farm', 'ambience': 'farm',
  'lines': [L('g67', "Alors, ils sont allés dans les fermes.", highlight=['fermes.']),
            L('g68', "Les éleveurs donnaient des hormones de croissance aux poulets.", highlight=['hormones']),
            L('g69', "Les volailles étaient devenues beaucoup trop musclées.", highlight=['musclées.']),
            L('g70', "Les policiers ont arrêté les poulets, puis les gens qui en avaient mangé.", highlight=['poulets,', 'mangé.'])],
  'actors': [
    act('fermier', [0.4, 0, -0.9], 30, 'injectArm', 'happy', face='poulet0', keys=[k('g69', clip='surrender', expr='scared', face='flic1')]),
    act('poulet0', CH[0], -120, 'idle', 'neutral', scale=1.0, keys=[k('g69:devenues', scale=3.2, dur=0.9, ease='out'), k('g70:arrêté', clip='idle', expr='sad')]),
    act('poulet1', CH[1], 60, 'eat', 'neutral', scale=1.0, keys=[k('g69:devenues+0.2', scale=3.0, dur=0.9, ease='out')]),
    act('poulet2', CH[2], -60, 'eat', 'neutral', scale=1.0, keys=[k('g69:devenues+0.35', scale=3.4, dur=0.9, ease='out')]),
    act('flic1', [-6.5, 0, 3.0], 60, 'walk', 'suspicious', keys=[k(0.05, to=[-2.0, 0, 0.6], clip='walk', speed=1.6, faceEnd='fermier'),
        k('g69:musclées', clip='scared', expr='shocked', face='poulet0'),
        k('g70', to=[0.7, 0, -0.9], clip='run', speed=2.4, faceEnd='poulet0', then='cuffOther', sfx='cuff')]),
    act('flic2', [-7.3, 0, 3.6], 60, 'walk', 'suspicious', keys=[k(0.25, to=[-2.8, 0, 1.4], clip='walk', speed=1.6, faceEnd='fermier'),
        k('g69:musclées', clip='startle', expr='shocked', face='poulet2'),
        k('g70:gens', to=[-3.6, 0, 2.6], clip='run', speed=2.6, faceEnd='mangeur', then='cuffOther', sfx='cuff')]),
    act('mangeur', [-4.6, 0, 3.4], 30, 'shovelFood', 'happy', keys=[k('g70:gens+0.5', clip='cuffedFront', expr='shocked')]),
  ],
  'props': [P('syr', 'syringeBig', on={'actor': 'fermier', 'hand': 'R'}),
            P('car', 'policeCar', pos=[-12, 0, 4.6], ry=90, keys=[k(0, to=[-6.0, 0, 4.6], dur=1.0, ease='out', sfx='brake')]),
            P('cuisse', 'drumstick', on={'actor': 'mangeur', 'hand': 'R'})],
  'cams': [
    cam(0, 'car', 'fs', worldAngle=30, elev=8, withProps=True),
    cam('g67:fermes', ['flic1', 'flic2'], 'fs', angle=30, move='track'),
    cam('g68', 'fermier', 'ms', angle=20),
    cam('g68:hormones', ['fermier', 'poulet0'], 'ms', worldAngle=-10),
    cam('g68:poulets', ['poulet0', 'poulet1', 'poulet2'], 'fs', worldAngle=0, elev=4),
    cam('g69:devenues', ['poulet0', 'poulet2'], 'fs', worldAngle=10, elev=-10, lens=32),
    cam('g69:musclées', 'flic1', 'cu', angle=15),
    cam('g70', ['flic1', 'poulet0'], 'fs', worldAngle=20),
    cam('g70:gens', ['flic2', 'mangeur'], 'fs', worldAngle=-20, move='track'),
  ],
  'tail': 0.4,
})

# ------------------------------------------------------------------ 19. commissariat : "on vous appelle les poulets"
COPS = ['flic3', 'flic4', 'flic5', 'flic6', 'flic7']
scenes.append({
  'id': 'commissariat', 'set': 'policeStation', 'ambience': 'station',
  'lines': [L('g71', "Parmi eux, il y avait aussi des policiers qui avaient bouffé du poulet.", highlight=['policiers', 'poulet.']),
            L('g72a', "Et là, un mec leur a dit :"),
            L('g72b', "Mais vous aussi, on vous appelle les poulets.", 'prisonnier', highlight=['poulets.']),
            L('g73', "Les flics se sont regardés.", highlight=['regardés.']),
            L('g74', "Putain, il avait raison.", highlight=['Putain,', 'raison.']),
            L('g75', "Alors, ils ont commencé à arrêter les autres policiers.", highlight=['arrêter']),
            L('g76', "Pour être sûrs de n'oublier personne, ils ont appelé la Belgique, puis Montréal, puis tous les pays où les flics pouvaient être appelés les poulets en français.",
              highlight=['Belgique,', 'Montréal,', 'poulets']),
            L('g77', "Chaque policier arrêtait le suivant.", highlight=['suivant.'])],
  'actors': [
    act('flic1', [-2.0, 0, -1.2], 30, 'shovelFood', 'happy', keys=[
        k('g72a', clip='idle', face='prisonnier', expr='neutral'),
        k('g73', face='flic2', expr='worried', turn=0.35), k('g74', expr='shocked', clip='startle'),
        k('g75', to=[-0.85, 0, -0.75], clip='walk', speed=1.4, faceEnd='flic2', then='cuffOther', sfx='cuff', sfxAt=0.25),
        k('g76', to=[-2.7, 0, -1.25], clip='walk', speed=1.5, faceEnd=0, then='phoneCall'),
        k('g77', clip='handsOnHips', face=60, expr='unimpressed')]),
    act('flic2', [-0.3, 0, -0.6], -60, 'shovelFood', 'happy', keys=[
        k('g72a', clip='idle', face='prisonnier', expr='neutral'),
        k('g73', face='flic1', expr='worried', turn=0.35), k('g74', expr='shocked', clip='facepalm'),
        k('g75+0.4', clip='cuffedFront', expr='sad')]),
    act('prisonnier', [5.1, 0, -2.4], -20, 'idle', 'neutral', keys=[k('g72a:dit', clip='pokeFinger', face='flic1'), k('g72b', clip='talk', expr='smug'),
        k('g72b:poulets', clip='point', expr='smug')]),
  ] + [act(c, [0.6 + i * 0.95, 0, 1.6], -90, 'idle', 'neutral', visible=False, keys=[k('g77', visible=True),
        k(f'g77+{0.25 + i * 0.32:.2f}', clip='cuffOther' if i < 4 else 'handsOnHips', sfx='cuff' if i < 4 else None, vol=0.45)] +
        ([k(f'g77+{0.57 + (i - 1) * 0.32:.2f}', clip='cuffedFront', expr='sad')] if i > 0 else [])) for i, c in enumerate(COPS)],
  'props': [P('cuisse1', 'drumstick', on={'actor': 'flic1', 'hand': 'R'}, keys=[k('g72a', visible=False)]),
            P('cuisse2', 'drumstick', on={'actor': 'flic2', 'hand': 'R'}, keys=[k('g74', detach=True, fall=True, impact='thud')]),
            P('bucket', 'chickenBucket', pos=[-2.5, 0.78, -2.05]),
            P('phone', 'phone911', opts={'text': '17'}, visible=False, on={'actor': 'flic1', 'hand': 'R'}, keys=[k('g76', visible=True), k('g77', visible=False)]),
            P('f_be', 'flag', pos=[-3.6, 0, -2.6], opts={'colors': ['#1A1A1A', '#F2C230', '#D9332B']}, visible=False, keys=[k('g76:Belgique', visible=True, sfx='pop')]),
            P('f_qc', 'flag', pos=[-4.1, 0, -2.2], opts={'colors': ['#1F4FA8'], 'cross': '#FFFFFF'}, visible=False, keys=[k('g76:Montréal', visible=True, sfx='pop')]),
            P('f_ch', 'flag', pos=[-4.6, 0, -2.6], opts={'colors': ['#D52B1E'], 'cross': '#FFFFFF'}, visible=False, keys=[k('g76:pays', visible=True, sfx='pop')]),
            P('f_ci', 'flag', pos=[-5.1, 0, -2.2], opts={'colors': ['#F77F00', '#FFFFFF', '#009E60']}, visible=False, keys=[k('g76:flics', visible=True, sfx='pop')]),
            P('f_sn', 'flag', pos=[-5.6, 0, -2.6], opts={'colors': ['#00853F', '#FDEF42', '#E31B23']}, visible=False, keys=[k('g76:appelés', visible=True, sfx='pop')]),
            P('f_mc', 'flag', pos=[-6.0, 0, -2.2], opts={'colors': ['#CE1126', '#FFFFFF'], 'vertical': False}, visible=False, keys=[k('g76:français', visible=True, sfx='pop')]),
            WM(pos=[-1.0, 1.75, -3.53], opts={'kind': 'poster'})],
  'cams': [
    cam(0, ['flic1', 'flic2'], 'fs', worldAngle=10, elev=6),
    cam('g71:bouffé', 'flic2', 'mcu', angle=10),
    cam('g72a', 'prisonnier', 'ms', angle=10),
    cam('g72b', 'prisonnier', 'cu', angle=5, move='push'),
    cam('g73', ['flic1', 'flic2'], 'ms', worldAngle=30),
    cam('g73:regardés', ots=['flic2', 'flic1', 1]),
    cam('g74', ots=['flic1', 'flic2', 1]),
    cam('g74:raison', 'flic2', 'cu', angle=0),
    cam('g75', ['flic1', 'flic2'], 'fs', worldAngle=20),
    cam('g76', 'flic1', 'ms', angle=20),
    cam('g76:Belgique', ['flic1', 'f_be', 'f_qc'], 'fs', worldAngle=20, withProps=True),
    cam('g76:pays', ['f_ch', 'f_ci', 'f_sn', 'f_mc'], 'fs', worldAngle=10, noOcclusion=True),
    cam('g76:français', 'flic1', 'cu', angle=10),
    cam('g77', COPS, 'fs', worldAngle=0, elev=6, move='push', amount=0.08),
  ],
  'tail': 1.3,
})

# ------------------------------------------------------------------ 20. la cellule pleine de flics
scenes.append({
  'id': 'cellule', 'set': 'prisonCell', 'ambience': 'station',
  'lines': [L('g78', "Les commissariats se remplissaient de leurs propres employés.", highlight=['propres', 'employés.'])],
  'actors': [act(f'flic{i + 1}', [-2.0 + i * 0.8, 0, 1.9 - (i % 2) * 0.7], 180 if i % 3 else 160, 'cuffedFront', ['sad', 'unimpressed', 'neutral'][i % 3]) for i in range(7)],
  'props': [],
  'cams': [cam(0, ['flic1', 'flic4', 'flic7'], 'fs', worldAngle=0, elev=4, move='push', amount=0.08),
           cam('g78:remplissaient', 'flic4', 'cu', angle=0),
           cam('g78:propres', ['flic2', 'flic3', 'flic4'], 'ms', worldAngle=-10)],
  'tail': 0.3,
})

# ------------------------------------------------------------------ 21. le dernier flic : complicité
scenes.append({
  'id': 'final', 'set': 'policeStation', 'ambience': 'station',
  'lines': [L('g79', "À la fin, il ne restait qu'un seul flic libre.", highlight=['seul']),
            L('g80', "Il a menotté son premier poignet.", highlight=['premier']),
            L('g81', "L'autre main a essayé de le libérer.", highlight=['libérer.']),
            L('g82', "Complicité.", highlight=['Complicité.'], pre=0.5)],
  'actors': [act('flic8', [0.3, 0, -0.6], 0, 'lookAround', 'worried', keys=[
      k('g80', clip='lookItem', expr='neutral', sfx='cuff', sfxAt=0.3),
      k('g81', clip='selfStruggle', expr='angry'),
      k('g82', clip='cuffedFront', expr='unimpressed', sfx='cuff', sfxAt=0.1), k('g82.end+0.2', clip='stareCamera')])],
  'props': [P('cuffs', 'handcuffs', on={'actor': 'flic8', 'hand': 'L'}, visible=False, keys=[k('g80', visible=True)]),
            P('tumble', 'tumbleweed', pos=[-6.0, 0, 1.4], keys=[k('g79', to=[6.5, 0, 1.0], dur=3.2, ease='linear')])],
  'cams': [cam(0, 'flic8', 'ws', worldAngle=0, elev=8, move='push', amount=0.1),
           cam('g79:seul', 'flic8', 'ms', angle=10),
           cam('g80', 'flic8', 'mcu', angle=-20),
           cam('g81', 'flic8', 'ms', angle=15),
           cam('g82', 'flic8', 'cu', angle=0, move='push', amount=0.08)],
  'tail': 1.6,
})

ep = {
  'version': 3, 'title': 'Le gorille', 'captionWords': 3, 'captionY': 0.66,
  'voice': {'name': 'allan tiktok', 'model': 'eleven_v4',
            'narrator': {'stability': 0.8, 'style': 0.0, 'rate': 1.07},
            'character': {'stability': 0.4, 'style': 0.4, 'rate': 1.02}},
  'music': {'mood': 'quirky', 'vol': 0.06},
  'cast': {
    'mec': {'preset': 'lemec'}, 'mecNu': {'preset': 'lemec', 'naked': True},
    'mecG': {'type': 'creature', 'name': 'gorilla', 'opts': {'clothes': 'suit', 'seed': 21}},
    'g0': {'type': 'creature', 'name': 'gorilla', 'opts': {'seed': 30}}, 'g1': {'type': 'creature', 'name': 'gorilla', 'opts': {'seed': 31}},
    'g2': {'type': 'creature', 'name': 'gorilla', 'opts': {'seed': 32}},
    'chevre': {'type': 'creature', 'name': 'goat', 'opts': {'seed': 3}},
    'coach': {'preset': 'sportif'}, 'muscu': {'preset': 'sportif', 'build': {'width': 1.4, 'height': 1.05}, 'seed': 12},
    'madame': {'preset': 'madame'}, 'mamie': {'preset': 'mamie'}, 'gamin': {'preset': 'gamin'},
    'chimiste': {'type': 'creature', 'name': 'gorilla', 'opts': {'seed': 77, 'colors': {'body': '#4A4B52'}}},
    'karim': {'preset': 'fringant'}, 'serveur': {'preset': 'serveur'}, 'fermier': {'preset': 'fermier'},
    'mangeur': {'preset': 'tourist'}, 'prisonnier': {'preset': 'prisoner'},
    **{f'flic{i}': {'preset': 'cop' if i % 2 else 'cop2', 'seed': 40 + i} for i in range(1, 9)},
    **{f'poulet{i}': {'type': 'creature', 'name': 'chicken', 'opts': {'seed': 50 + i}} for i in range(3)},
  },
  'scenes': scenes,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gorille3.json')
json.dump(ep, open(out, 'w'), ensure_ascii=False, indent=1)
words = sum(len(l['text'].split()) for s in scenes for l in s['lines'])
print(out, len(scenes), 'scenes,', sum(len(s['lines']) for s in scenes), 'lines,', words, 'words,', sum(len(s['cams']) for s in scenes), 'camera setups')
