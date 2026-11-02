#!/usr/bin/env python3
"""LE CHRONO — v3 storyboard (python3 scripts-fr/chrono3.py -> chrono3.json)

Original French adaptation of the "stopwatch that stops time" premise, written to the french-lowpoly-absurd-shorts
skill: ~45 s, ~150 words, real lines spoken by the characters (same voice, other intonation), three escalations
(moustache, bank, dropping the watch) and a visual punchline (he finally has someone who listens: a frozen guard,
for 3,000 years — day/night cycling, his beard growing, spider webs on the guard).

Découpage (every narrated action is shown, characters face who they talk to, all moves face their direction):
  S1 PAUSE CAFÉ  L1-2   he talks non-stop; a colleague escapes, the other faints; he keeps talking to him
  S2 PATRON      L3-6   walks in proud, 400 ideas, "on fabrique des yaourts", fired, leaves with his box
  S3 BAR         L7-12  everybody leaves, the drunk gives the watch, click: frozen mid-fall, "Putain…", hero pose
  S4 MOUSTACHE   L13    draws a moustache on the frozen boss
  S5 BANQUE      L14-15 pushes a cart of cash through a frozen bank; the watch drops and breaks
  S6 RUE         L16-18 frozen forever; "Bon… je vous raconte ma vie ?" — time-lapse punchline
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
WM = lambda **kw: {'name': 'wmSign', 'id': 'wm', **kw}

scenes = []

# ---------------------------------------------------------------- S1 la pause café ----------------
scenes.append({
  'id': 'pause', 'set': 'office', 'ambience': 'office',
  'lines': [L('C1', "Ce mec était le plus gros relou de toute l'entreprise.", highlight=['relou']),
            L('C2', "Il détenait le record du monde de mots inutiles à la pause café.", highlight=['record', 'inutiles'])],
  'actors': [
    act('mec', [1.3, 0, -1.0], 0, 'talk', 'happy', face='coll1', keys=[k('C2', clip='talk', speed=1.7), k('C2#8', look='coll1')]),
    act('coll1', [2.35, 0, -0.55], 0, 'holdOut', 'unimpressed', face='mec', keys=[
        k('C1#4', clip='nod', expr='unimpressed'), k('C2#3', expr='sleepy', clip='stand'),
        k('C2.end-0.55', clip='faint', params={'dur': 0.45}, expr='dead', sfx='thud', sfxAt=0.45)]),
    act('coll2', [0.35, 0, -0.35], 0, 'stand', 'happy', face='mec', keys=[
        k('C1.end', expr='unimpressed', clip='lookAround'), k('C2#3', clip='lookItem', expr='suspicious'),
        k('C2#5', to=[-2.6, 0, 1.6], clip='tiptoe', speed=0.9, then='idle')]),
  ],
  'props': [{'id': 'machine', 'name': 'coffeeMachine', 'pos': [2.7, 0, -3.0]},
            {'id': 'mug', 'name': 'mug', 'on': {'actor': 'coll1', 'hand': 'R'}, 'keys': [k('C2.end-0.5', detach=True, fall=True, impact='clink')]},
            WM(anchor='picture', offset=[1.5, -0.7, 0.03])],
  'cams': [
    cam(0, ['mec', 'coll1', 'coll2'], 'fs', worldAngle=15, elev=8, move='push', amount=0.08),
    cam('C1#4', 'mec', 'ms', angle=30),
    cam('C1.end-0.2', 'coll1', 'mcu', angle=-25),
    cam('C2', 'coll2', 'cu', angle=35),
    cam('C2#5', 'coll2', 'fs', angle=60, move='track'),
    cam('C2#8', 'mec', 'cu', angle=25, move='push'),
    cam('C2.end-0.6', ['coll1', 'mec'], 'fs', angle=-35),
  ],
  'tail': 0.6,
})

# ---------------------------------------------------------------- S2 le patron --------------------
scenes.append({
  'id': 'patron', 'set': 'office', 'ambience': 'office',
  'lines': [L('C3', "Un jour, son patron l'a convoqué."),
            L('C4', "Quatre cents idées dans la boîte à suggestions ?", 'patron', highlight=['Quatre', 'cents']),
            L('C5', "Merci, patron !", 'mec'),
            L('C6', "On fabrique des yaourts. Vous êtes viré.", 'patron', highlight=['yaourts.', 'viré.'])],
  'actors': [
    act('patron', [-4.75, 0.12, -2.05], 0, 'sit', 'unimpressed', keys=[
        k('C3#2', clip='beckon'), k('C4', clip='sitShow', expr='suspicious'), k('C5', clip='sit', expr='unimpressed'),
        k('C6', clip='sitShow', expr='unimpressed'), k('C6:viré', clip='sitPoint', expr='angry')]),
    act('mec', [-1.8, 0, 0.9], 0, 'idle', 'happy', keys=[
        k('C3', to=[-4.35, 0, -0.65], clip='strut', faceEnd='patron'),
        k('C4', clip='handsOnHips', expr='smug'), k('C5', clip='present', expr='happy'),
        k('C6:viré', clip='stareCamera', expr='shocked'),
        k('C6.end+0.55', to=[-1.2, 0, 2.2], clip='carryBox', expr='sad')]),
  ],
  'props': [{'id': 'pile', 'name': 'paperPile', 'pos': [-5.3, 0.76, -1.3], 'opts': {'count': 150}},
            {'id': 'paper', 'name': 'documents', 'on': {'actor': 'patron', 'hand': 'R'}, 'opts': {'count': 1}, 'keys': [k('C6', visible=False)]},
            {'id': 'yaourt', 'name': 'mug', 'opts': {'color': '#FFFFFF'}, 'visible': False, 'on': {'actor': 'patron', 'hand': 'R'}, 'keys': [k('C6', visible=True), k('C6:viré', visible=False)]},
            {'id': 'box', 'name': 'cardboardBox', 'opts': {'text': ''}, 'visible': False, 'pos': [-3.9, 0, -0.2], 'keys': [k('C6.end+0.5', visible=True, attach='mec', joint='torso', offset=[0, 0.28, 0.42])]}],
  'cams': [
    cam(0, 'patron', 'ms', angle=10),
    cam('C3#4', 'mec', 'fs', angle=35, move='track'),
    cam('C4', ots=['mec', 'patron', -1]),
    cam('C4#2', 'pile', 'mls', angle=-15),
    cam('C5', 'mec', 'cu', angle=15),
    cam('C6', 'patron', 'mcu', angle=-35),
    cam('C6:viré', 'mec', 'ecu', angle=5, move='push'),
    cam('C6.end+0.5', 'mec', 'fs', angle=35, move='track', withProps=True),
  ],
  'tail': 1.5,
})

# ---------------------------------------------------------------- S3 le bar (freeze) -------------
STOOL_Y = 0.15
scenes.append({
  'id': 'bar', 'set': 'bar', 'ambience': 'bar', 'lighting': 'interior',
  'freeze': {'at': 'C10.end', 'except': ['mec', 'watch']},
  'lines': [L('C7', "Alors ce con est allé raconter sa vie au bar."),
            L('C8', "En dix minutes, tout le monde était parti. Sauf un vieux complètement bourré.", highlight=['parti.', 'bourré.']),
            L('C9', "Tiens, petit. Ça arrête le temps.", 'vieux', highlight=['arrête', 'temps.']),
            L('C10', "Il a appuyé."),
            L('C11', "Putain…", 'mec', pre=0.45),
            L('C12', "Le pouvoir absolu. Il aurait pu sauver le monde.", highlight=['absolu.', 'sauver'])],
  'actors': [
    act('mec', [0.5, STOOL_Y, -1.25], -90, 'sitTalk', 'happy', face='client1', keys=[
        k('C8:Sauf', face='vieux', turn=0.3, clip='sit', expr='neutral'),
        k('C9.end-0.35', clip='sitTake', expr='suspicious'), k('C10', clip='sitLookItem', expr='neutral', sfx='click', sfxAt=0.55),
        k('C11', expr='shocked', clip='sitLookItem', look='vieux'),
        k('C12', to=[1.2, 0, 0.6], clip='strut', speed=1.0, look=None, expr='happy'),
        k('C12:sauver', clip='heroPose', expr='smug', face=0, turn=0.35)]),
    act('client1', [-0.5, STOOL_Y, -1.25], 90, 'sit', 'unimpressed', face='mec', keys=[
        k('C7#4', expr='sleepy'), k('C8', to=[-6.6, 0, 2.0], clip='walk', speed=1.6, expr='unimpressed')]),
    act('client2', [-1.5, STOOL_Y, -1.25], 90, 'sit', 'unimpressed', keys=[
        k('C8#2', to=[-6.9, 0, 2.7], clip='flee', speed=2.6, expr='scared')]),
    act('barman', [0.6, 0, -2.6], 0, 'wipeGlass', 'unimpressed', keys=[
        k('C8#5', path=[[-3.3, 0, -2.6], [-3.8, 0, -0.5], [-6.2, 0, 1.5]], clip='tiptoe', speed=1.3, expr='suspicious')]),
    act('vieux', [2.5, STOOL_Y, -1.25], -90, 'drunk', 'sleepy', face='mec', keys=[
        k('C9', clip='sitGive', expr='happy'), k('C9.end', clip='drunk', expr='sleepy'),
        k('C10.end-0.4', clip='tipOverSit', params={'dur': 1.0}, expr='surprised')]),
  ],
  'props': [{'id': 'watch', 'name': 'stopwatch', 'scale': 1.5, 'on': {'actor': 'vieux', 'hand': 'R'}, 'visible': False,
             'keys': [k('C9', visible=True), k('C9.end-0.2', attach='mec', hand='R')]},
            {'id': 'glass', 'name': 'beerGlass', 'on': {'actor': 'vieux', 'hand': 'L'}},
            {'id': 'stream', 'name': 'beerStream', 'opts': {'length': 0.5}, 'visible': False, 'on': {'actor': 'vieux', 'joint': 'handL', 'offset': [0, -0.22, 0.02]},
             'keys': [k('C10.end-0.15', visible=True)]},
            WM(anchor='sign', offset=[2.0, -0.55, 0.03], opts={'bg': '#2A1E1A', 'fg': '#C9A86A'})],
  'cams': [
    cam(0, ['mec', 'client1', 'client2'], 'fs', worldAngle=15, elev=10),
    cam('C7#4', 'mec', 'ms', angle=35),
    cam('C7.end-0.3', 'client1', 'mcu', angle=-30),
    cam('C8', ['mec', [-1.5, 1.0, -1.25]], 'fs', worldAngle=0, elev=8, move='push', amount=0.06),
    cam('C8#5', 'barman', 'fs', angle=20, move='track'),
    cam('C8:Sauf', 'vieux', 'ms', angle=35),
    cam('C9', ots=['mec', 'vieux', 1]),
    cam('C9#3', 'watch', 'cu', angle=-35, elev=12),
    cam('C10', 'mec', 'cu', angle=30),
    cam('C10.end', ['vieux', 'mec'], 'fs', worldAngle=10, move='push', amount=0.08),
    cam('C11', 'mec', 'ecu', angle=15),
    cam('C12', 'mec', 'fs', angle=-35, move='track'),
    cam('C12+1.1', 'vieux', 'mcu', angle=15),
    cam('C12:sauver', 'mec', 'ms', angle=10, elev=-14, lens=34),
  ],
  'tail': 0.5,
})

# ---------------------------------------------------------------- S4 la moustache (frozen) -------
scenes.append({
  'id': 'moustache', 'set': 'office', 'ambience': None,
  'freeze': {'at': 0, 'except': ['mec', 'moustache', 'marker']},
  'lines': [L('C13', "Il a dessiné une moustache à son ancien patron.", highlight=['moustache'])],
  'actors': [
    act('patron', [-4.75, 0.12, -2.05], 0, 'sitPoint', 'angry'),
    act('mec', [-3.3, 0, -1.9], 0, 'idle', 'smug', face='patron', keys=[
        k(0.05, path=[[-3.55, 0, -2.45], [-4.31, 0, -2.36]], clip='walk', speed=1.6, faceEnd='patron'), k('C13#4', clip='drawOn', expr='happy', sfx='squeak'),
        k('C13.end-0.3', clip='heroPose', expr='smug', face=25, turn=0.35)]),
  ],
  'props': [{'id': 'marker', 'name': 'marker', 'on': {'actor': 'mec', 'hand': 'R'}},
            {'id': 'moustache', 'name': 'mustache3d', 'scale': 0.01, 'on': {'actor': 'patron', 'joint': 'head', 'offset': [0, 0.13, 0.115]},
             'keys': [k('C13#4', scale=1.5, dur=0.9)]},
            WM(anchor='picture', offset=[1.5, -0.7, 0.03])],
  'cams': [
    cam(0, 'patron', 'ms', angle=-40),
    cam('C13#4', 'patron', 'ecu', angle=0, move='push', amount=0.06),
    cam('C13.end-0.2', ['mec', 'patron'], 'ms', worldAngle=20, elev=6),
  ],
  'tail': 0.9,
})

# ---------------------------------------------------------------- S5 la banque (frozen) ----------
scenes.append({
  'id': 'banque', 'set': 'bank', 'ambience': 'bank',
  'freeze': {'at': 0, 'except': ['mec', 'cart', 'cash', 'watch']},
  'lines': [L('C14', "Puis il a braqué une banque.", highlight=['braqué']),
            L('C15', "Mais en sortant, ce con a fait tomber le chrono.", highlight=['tomber', 'chrono.'])],
  'actors': [
    act('guichetier', [-1.2, 0, -2.15], 0, 'giveItem', 'neutral'),
    act('vigile', [-2.6, 0, 1.0], 60, 'yawnStretch', 'sleepy'),
    act('cliente', [-0.4, 0, 0.9], 120, 'walk', 'neutral', params={'freq': 1.6}),
    act('mec', [2.4, 0, -2.0], 0, 'idle', 'happy', keys=[
        k(0.05, path=[[1.9, 0, -0.6], [0.9, 0, 1.4], [0.4, 0, 3.0]], clip='pushCartWalk', speed=1.15, then='idle'),
        k('C15:tomber', expr='surprised'), k('C15.end+0.25', face=-150, clip='scared', expr='shocked')]),
  ],
  'props': [{'id': 'cart', 'name': 'shoppingCart', 'on': {'actor': 'mec', 'joint': 'hips', 'offset': [0, -1.02, 0.78]}},
            {'id': 'cash', 'name': 'money', 'opts': {'stacks': 6}, 'on': {'actor': 'cart', 'offset': [0, 0.55, 0.05]}},
            {'id': 'watch', 'name': 'stopwatch', 'scale': 1.5, 'on': {'actor': 'mec', 'joint': 'hips', 'offset': [0.16, 0.02, -0.14]},
             'keys': [k('C15:tomber', detach=True, fall=True, impact='glass', spinFall=6)], 'alt': {'opts': {'broken': True}, 'at': 'C15:tomber+0.5', 'rot': [-1.5708, 0, 0.4]}},
            {'id': 'coin', 'name': 'coin', 'pos': [-0.25, 1.2, 1.05]},
            WM(anchor='sign', offset=[2.3, -0.95, 0.03])],
  'sfx': [{'at': 'C15:tomber+0.62', 'name': 'spring', 'vol': 0.5}],
  'cams': [
    cam(0, ['mec', 'cliente'], 'fs', worldAngle=35, elev=12, move='crane', amount=-6),
    cam('C14#3', 'mec', 'ms', angle=30, move='track'),
    cam('C14.end', 'cliente', 'mcu', angle=-10),
    cam('C15', 'mec', 'fs', angle=-30, move='track'),
    cam('C15:tomber-0.1', 'mec', 'mls', angle=160, elev=10, allowBack=True),
    cam('C15:tomber+0.55', 'watch', 'ecu', angle=0, elev=45),
    cam('C15.end+0.3', 'mec', 'cu', angle=15),
  ],
  'tail': 1.3,
})

# ---------------------------------------------------------------- S6 la rue (frozen forever) ------
scenes.append({
  'id': 'rue', 'set': 'street', 'ambience': None, 'music': None,
  'freeze': {'at': 0, 'except': ['mec', 'beard', 'web1', 'web2', 'bench']},
  'daynight': {'from': 'C18', 'period': 0.7},
  'lines': [L('C16', "Le temps ne repartira plus jamais.", highlight=['jamais.']),
            L('C17', "Bon… Je vous raconte ma vie ?", 'mec', pre=0.5),
            L('C18', "Pour la première fois, quelqu'un l'a écouté jusqu'au bout.", highlight=["jusqu'au", 'bout.'])],
  'actors': [
    act('vigile', [-0.55, 0, -0.55], 25, 'handsOnHips', 'unimpressed'),
    act('passant', [2.4, 0, 0.6], -90, 'walk', 'neutral', params={'freq': 1.7}),
    act('pigeon', [0.9, 2.5, -0.9], -90, 'fly', 'neutral'),
    act('mec', [1.6, 0, 2.4], 0, 'idle', 'neutral', keys=[
        k(0.1, to=[0.35, 0, -0.1], clip='walk', faceEnd='vigile'), k('C16#3', clip='waveFace', expr='suspicious'),
        k('C16.end', clip='pokeFinger', expr='unimpressed'),
        k('C17-0.4', to=[0.6, 0, 0.35], clip='walk', speed=0.8, faceEnd='vigile'),
        k('C17', clip='sitTalk', expr='happy', look='vigile'),
        k('C18', clip='sitTalk', speed=2.2)]),
  ],
  'props': [{'id': 'bench', 'name': 'bench', 'pos': [0.75, 0, 0.55], 'ry': -55},
            {'id': 'beard', 'name': 'beard', 'opts': {'color': '#E8E4DA'}, 'scale': 0.02, 'on': {'actor': 'mec', 'joint': 'head', 'offset': [0, 0.06, 0.1]}, 'keys': [k('C18', scale=2.6, dur=3.2, ease='linear')]},
            {'id': 'web1', 'name': 'spiderWeb', 'visible': False, 'on': {'actor': 'vigile', 'joint': 'head', 'offset': [0.12, 0.3, 0.1], 'rot': [0, 0.3, 0]}, 'keys': [k('C18+1.0', visible=True)]},
            {'id': 'web2', 'name': 'spiderWeb', 'opts': {'r': 0.25}, 'visible': False, 'on': {'actor': 'vigile', 'joint': 'elbowR', 'offset': [0, -0.15, 0.08]}, 'keys': [k('C18+2.0', visible=True)]},
            WM(pos=[3.8, 0, -1.3], opts={'kind': 'stand'})],
  'cams': [
    cam(0, ['mec', 'vigile', 'passant'], 'fs', worldAngle=15, elev=12, move='crane', amount=-6),
    cam('C16#3', ['mec', 'vigile'], 'fs', angle=40),
    cam('C16.end', 'vigile', 'cu', angle=0),
    cam('C17', ots=['vigile', 'mec', 1]),
    cam('C18', ['mec', 'vigile', 'bench'], 'fs', worldAngle=30, elev=8),
    cam('C18:bout', 'mec', 'cu', angle=20),
    cam('C18.end+0.5', 'vigile', 'mcu', angle=-10, move='push', amount=0.06),
  ],
  'tail': 2.2,
})

ep = {
  'version': 3, 'title': 'Le chrono', 'captionWords': 3, 'captionY': 0.66,
  'voice': {'name': 'allan tiktok', 'model': 'eleven_v4',
            'narrator': {'stability': 0.8, 'style': 0.0, 'rate': 1.06},
            'character': {'stability': 0.4, 'style': 0.4, 'rate': 1.02}},
  'music': {'mood': 'quirky', 'vol': 0.06},
  'cast': {
    'mec': {'preset': 'lemec'}, 'coll1': {'preset': 'lemec_glasses'}, 'coll2': {'preset': 'madame'},
    'patron': {'preset': 'boss', 'facial': 'none'},
    'vieux': {'preset': 'lemec_beige', 'hair': 'receding', 'hairColor': '#D8D8D8', 'facial': 'beard', 'beardColor': '215,215,210', 'redNose': True, 'build': {'height': 0.92}},
    'barman': {'preset': 'serveur'}, 'client1': {'preset': 'fermier'}, 'client2': {'preset': 'mamie'},
    'guichetier': {'preset': 'lemec_charcoal'}, 'vigile': {'preset': 'cop2'}, 'cliente': {'preset': 'madame', 'seed': 9},
    'passant': {'preset': 'tourist'}, 'pigeon': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 2}},
  },
  'scenes': scenes,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrono3.json')
json.dump(ep, open(out, 'w'), ensure_ascii=False, indent=1)
words = sum(len(l['text'].split()) for s in scenes for l in s['lines'])
print(out, len(scenes), 'scenes,', sum(len(s['lines']) for s in scenes), 'lines,', words, 'words,', sum(len(s['cams']) for s in scenes), 'camera setups')
