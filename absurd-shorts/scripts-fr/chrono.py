#!/usr/bin/env python3
"""Storyboard for "Le chrono" -> scripts-fr/chrono.json (python3 scripts-fr/chrono.py)
Original French narration (scripts-fr/chrono.txt) adapting the "stopwatch that stops time" premise.
One continuous take per location; frozen-time shots use shot.freeze (+ shot.moving = who still moves)."""
import json, os
M = 'mec'; shots = []
lines = [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrono.txt'), encoding='utf-8').read().split('\n')[2:] if l.strip()]
def S(actors=None, cam=None, cut=False, **kw):
    d = {'line': lines[len([x for x in shots if x.get('line')])] if not kw.get('silent') else '', 'actors': actors or [], 'camera': cam or {'preset': 'medium'}}
    kw.pop('silent', None)
    if not cut: d['cut'] = False
    d.update(kw); shots.append(d); return d
def A(id, pos=None, clip='idle', expr=None, **kw):
    d = {'id': id, 'clip': clip}
    if pos is not None: d['pos'] = pos
    if expr: d['expr'] = expr
    d.update(kw); return d
WM = lambda **kw: {'name': 'wmSign', **kw}
watch = {'name': 'stopwatch', 'hand': 'R', 'scale': 1.6}

# 1. office, coffee break -------------------------------------------------------------------------------
S([A(M, [0, 0, 0.4], 'talk', 'neutral', talk=True, ry=-20), A('coll1', [1.1, 0, -0.2], 'idle', 'unimpressed', ry=-60), A('coll2', [-1.1, 0, -0.1], 'idle', 'sleepy', ry=50), A('coll3', [0.3, 0, -1.2], 'armsCrossed', 'unimpressed', ry=-10)],
  {'preset': 'wide', 'target': [0, 1.4, -0.2], 'angle': 10, 'zoom': 0.7, 'push': 0.14}, cut=True, set='office', highlight=['relou'],
  props=[{'name': 'mug', 'pos': [0.25, 1.15, 0.6]}, WM(anchor='picture', offset=[1.5, -0.7, 0.03])])
S([A(M, None, 'talk', 'happy', talk=True, speed=1.6), A('coll1', None, 'faint', 'dead', params={'dur': 0.6}, actions=[{'at': 0, 'clip': 'idle', 'expr': 'sleepy'}, {'at': 1.6, 'clip': 'faint', 'expr': 'dead', 'params': {'dur': 0.6}}]), A('coll2', None, 'idle', 'blink')],
  {'preset': 'full', 'target': [0.4, 1.5, 0.1], 'angle': 0, 'zoom': 0.85, 'push': 0.1, 'glide': 0.8}, highlight=['record', 'inutiles'], sfx=[{'name': 'thud', 'at': 2.1, 'vol': 0.5}])
# 2. the boss --------------------------------------------------------------------------------------------
boss = A('patron', [-4.6, 0, -1.6], 'sit', 'unimpressed')
S([boss, A(M, [-4.6, 0, 0.6], 'walk', 'happy', ry=180, to=[-4.6, 0, -0.1], moveEnd=1.2, actions=[{'at': 1.3, 'clip': 'handsOnHips', 'expr': 'smug'}])],
  {'preset': 'wide', 'target': [-4.6, 1.3, -0.8], 'angle': 30, 'zoom': 0.7, 'push': 0.1}, cut=True, set='office', highlight=['patron'],
  props=[{'name': 'desk', 'pos': [-4.6, 0, -1.0]}, {'name': 'suggestionBox', 'pos': [-3.2, 0, -1.6]}])
S([A(M, None, 'shrug', 'smug')], {'preset': 'medium', 'target': M, 'angle': 160, 'push': 0.1, 'glide': 0.7}, highlight=['prime', 'suggestions'])
S([A('patron', None, 'sit', 'unimpressed')], {'preset': 'medium', 'target': 'patron', 'angle': 0, 'zoom': 1.2, 'push': 0.1, 'dy': -0.3, 'lookDy': -0.4, 'glide': 0.7}, highlight=['quatre', 'cents'],
  props=[{'name': 'paperPile', 'pos': [-4.9, 0.78, -0.95], 'opts': {'count': 120}}])
S([A('patron', None, 'facepalm', 'unimpressed')], {'preset': 'close', 'target': 'patron', 'angle': 10, 'push': 0.08, 'glide': 0.5}, highlight=['sous-marins'])
S([A('patron', None, 'sit', 'angry')], {'preset': 'close', 'target': 'patron', 'angle': -10, 'push': 0.05, 'glide': 0.5}, highlight=['yaourts'], hold=0.2)
S([A('patron', None, 'point', 'angry'), A(M, None, 'spinFall', 'shocked', ry=180, to=[-4.0, 0, 3.0], moveStart=0.3, moveEnd=1.0, params={'dur': 0.8})],
  {'preset': 'wide', 'target': [-4.4, 1.2, 0.4], 'angle': 20, 'zoom': 0.8, 'push': 0.05, 'glide': 0.5}, highlight=['virer'], sfx=[{'name': 'whoosh', 'at': 0.3, 'vol': 0.6}, {'name': 'thud', 'at': 1.0, 'vol': 0.6}])
# 3. the bar ----------------------------------------------------------------------------------------------
bar_people = [A('client1', [-1.6, 0, -0.9], 'sit', 'neutral', ry=0), A('client2', [-0.6, 0, -0.9], 'sit', 'neutral', ry=0), A('client3', [1.4, 0, -0.9], 'sit', 'neutral', ry=0)]
S([A(M, [0.4, 0, -0.9], 'talk', 'happy', talk=True, ry=-10), A('vieux', [2.4, 0, -0.9], 'drunk', 'sleepy'), A('barman', [0.4, 0, -2.7], 'idle', 'unimpressed')] + bar_people,
  {'preset': 'wide', 'target': [0.4, 1.3, -1.2], 'angle': 0, 'zoom': 0.75, 'push': 0.12}, cut=True, set='bar', highlight=['bar', 'vie'],
  props=[WM(anchor='sign', offset=[1.9, -0.6, 0.03], opts={'bg': '#2A1E1A', 'fg': '#C9A86A'})])
S([A(M, None, 'talk', 'happy', talk=True, speed=1.5)] + [A(f'client{i}', None, 'flail', 'scared', to=[[-6, 0, 3], [-5, 0, 4], [6, 0, 3]][i - 1], moveStart=0.3 + 0.4 * i, moveEnd=1.6 + 0.4 * i, ry=[200, 210, 150][i - 1]) for i in (1, 2, 3)],
  {'preset': 'wide', 'target': [0.4, 1.3, -1.0], 'angle': 0, 'zoom': 0.85, 'push': 0.05, 'glide': 0.6}, highlight=['dix', 'partis'], sfx=['whoosh'])
S([A('vieux', None, 'drunk', 'sleepy')], {'preset': 'medium', 'target': 'vieux', 'angle': -15, 'push': 0.12, 'glide': 0.7}, highlight=['bourré'], remove=['client1', 'client2', 'client3'])
S([A(M, None, 'sit', 'smug', hold={'name': 'beerGlass', 'hand': 'R'}), A('vieux', None, 'drunk', 'happy')],
  {'preset': 'full', 'target': [1.4, 1.3, -0.9], 'angle': 0, 'zoom': 0.8, 'push': 0.1, 'glide': 0.6}, highlight=['verre'])
S([A('vieux', None, 'present', 'happy', hold=watch)], {'preset': 'medium', 'target': 'vieux', 'angle': -20, 'push': 0.12, 'glide': 0.6}, highlight=['chronomètre'])
S([A(M, None, 'holdOut', 'suspicious', hold=watch)], {'preset': 'close', 'target': M, 'angle': 20, 'push': 0.1, 'glide': 0.6}, highlight=['appuyé'], sfx=[{'name': 'click', 'at': 0.9, 'vol': 0.7}])
S([A('barman', [0.4, 0, -2.7], 'facepalm', 'unimpressed'), A('vieux', None, 'drunk', 'happy'), A(M, None, 'holdOut', 'shocked', hold=watch)],
  {'preset': 'wide', 'target': [0.8, 1.3, -1.4], 'angle': 0, 'zoom': 0.8, 'push': 0.12, 'glide': 0.4}, highlight=['temps', 'arrêté'], freeze=True, freezeAt=0.15, moving=[M],
  sfx=[{'name': 'scratch', 'at': 0.0, 'vol': 0.4}])
S([A(M, None, 'stareCamera', 'shocked', hold=watch)], {'preset': 'extremeClose', 'target': M, 'angle': 10, 'push': 0.05, 'glide': 0.4}, highlight=['Putain'], freeze=True, freezeAt=0.15, moving=[M], hold=0.2)
S([A(M, [0.4, 0, 0.6], 'celebrate', 'happy', hold=watch)], {'preset': 'wide', 'target': [0.6, 1.4, -0.6], 'angle': 15, 'zoom': 0.8, 'push': 0.1, 'glide': 0.6}, highlight=['pouvoir', 'absolu'], freeze=True, freezeAt=0.15, moving=[M])
# 4. revenge at the office (frozen) -------------------------------------------------------------------
S([A('patron', [-4.6, 0, -1.6], 'point', 'angry'), A(M, [-3.6, 0, -0.4], 'thinkChin', 'suspicious', ry=-60, hold=watch)],
  {'preset': 'wide', 'target': [-4.1, 1.3, -1.0], 'angle': 25, 'zoom': 0.75, 'push': 0.1}, cut=True, set='office', highlight=['sauver', 'monde'], freeze=True, moving=[M],
  props=[{'name': 'desk', 'pos': [-4.6, 0, -1.0]}])
S([A('patronMoustache', [-4.6, 0, -1.6], 'point', 'angry'), A(M, [-4.2, 0, -0.9], 'point', 'smug', ry=-40, hold={'name': 'glueTube', 'hand': 'R'})],
  {'preset': 'close', 'target': 'patronMoustache', 'angle': 15, 'push': 0.08}, cut=True, set='office', highlight=['moustache'], freeze=True, moving=[M], remove=['patron'],
  props=[{'name': 'desk', 'pos': [-4.6, 0, -1.0]}])
# 5. the bank ---------------------------------------------------------------------------------------------
bank = [A('guichetier', [-1.2, 0, -2.1], 'idle', 'neutral', ry=0), A('vigile', [2.0, 0, 0.4], 'handsOnHips', 'unimpressed', ry=-40), A('cliente', [-0.2, 0, 0.6], 'walk', 'neutral', ry=-90)]
S([A(M, [0, 0, 3.2], 'strut', 'smug', ry=180, to=[0, 0, 1.6], hold=watch)] + bank,
  {'preset': 'wide', 'target': [0, 1.4, 0.2], 'angle': 0, 'zoom': 0.85, 'push': 0.1}, cut=True, set='bank', highlight=['braquer', 'banque'],
  props=[WM(anchor='sign', offset=[2.2, -0.9, 0.03])])
S([A(M, [2.0, 0, -1.6], 'pushCart', 'happy', ry=180, to=[0.4, 0, 2.0], moveStart=0.4)],
  {'preset': 'wide', 'target': [1.2, 1.3, 0.0], 'angle': 20, 'zoom': 0.85, 'push': 0.06, 'glide': 0.6}, highlight=['figé', 'billets'], freeze=True, moving=[M, 'shoppingCart', 'money'],
  props=[{'name': 'shoppingCart', 'pos': [2.0, 0, -1.0], 'ry': 180, 'to': [0.4, 0, 2.6], 'moveStart': 0.4, 'moving': True},
         {'name': 'money', 'pos': [2.0, 0.55, -1.0], 'opts': {'stacks': 6}, 'to': [0.4, 0.55, 2.6], 'moveStart': 0.4, 'moving': True}])
S([A(M, [0.4, 0, 2.0], 'scared', 'shocked')],
  {'preset': 'full', 'target': [0.4, 1.0, 2.2], 'angle': 30, 'zoom': 0.9, 'push': 0.05, 'glide': 0.4}, highlight=['tomber', 'chrono'], freeze=True, moving=[M, 'stopwatch'],
  props=[{'name': 'stopwatch', 'pos': [0.55, 1.1, 2.3], 'to': [0.6, 0.07, 2.5], 'moveStart': 0.6, 'moveEnd': 0.95, 'moveEase': 'in', 'moving': True, 'scale': 1.6}],
  sfx=[{'name': 'glass', 'at': 0.95, 'vol': 0.7}])
S([A(M, [0.4, 0, 2.0], 'kneel', 'shocked')], {'preset': 'feet', 'target': [0.6, 0.6, 2.5], 'angle': 0, 'zoom': 0.5, 'push': 0.15}, cut=True, set='bank', highlight=['cassé'], freeze=True, replaceProps=True,
  props=[{'name': 'stopwatch', 'pos': [0.6, 0.07, 2.5], 'opts': {'broken': True}, 'scale': 1.6}], moving=[M])
# 6. outside: time never restarts ---------------------------------------------------------------------
street = [A('passant1', [-2.0, 0, 0.6], 'walk', 'neutral', ry=90), A('passant2', [1.6, 0, -0.6], 'flail', 'scared', ry=-90), A('pigeon', [0.6, 2.4, 0.4], 'fly', 'neutral', ry=-90)]
S([A(M, [0, 0, 1.2], 'scared', 'shocked')] + street,
  {'preset': 'wide', 'target': [0, 1.5, 0.4], 'angle': 0, 'zoom': 0.8, 'push': 0.15, 'orbit': 25}, cut=True, set='street', highlight=['jamais'], freeze=True, freezeAt=0.2, moving=[M],
  props=[WM(pos=[4.0, 0, -1.4], opts={'kind': 'stand'})])
S([A(M, [0.9, 0, 1.0], 'talk', 'happy', talk=True, ry=-80), A('vigile', [-0.3, 0, 1.0], 'handsOnHips', 'unimpressed', ry=80)],
  {'preset': 'full', 'target': [0.3, 1.5, 1.0], 'angle': 0, 'zoom': 0.8, 'push': 0.1}, cut=True, set='street', highlight=['vigile'], freeze=True, moving=[M])
S([A(M, None, 'talk', 'happy', talk=True, speed=4)], {'preset': 'full', 'target': [0.3, 1.5, 1.0], 'angle': 30, 'orbit': 120, 'zoom': 0.85, 'push': 0.0, 'glide': 0.4}, highlight=['trois', 'mille'], freeze=True, moving=[M])
S([A('vigile', None, 'handsOnHips', 'unimpressed')], {'preset': 'close', 'target': 'vigile', 'angle': -20, 'push': 0.08, 'glide': 0.6}, highlight=['écoutait', 'bout'], freeze=True, moving=[M], hold=1.2)

# ---- framing pass after the contact sheet ----
def cam(i, **c): shots[i]['camera'] = c
cam(4, **{'from': [-2.9, 1.75, 0.9], 'to': [-3.1, 1.7, 0.5], 'lookAt': [-4.6, 1.15, -1.5], 'fov': 40})
cam(10, preset='medium', target=[2.4, 1.5, -0.9], angle=-15, push=0.12, glide=0.7)
cam(11, **{'from': [1.4, 1.8, 5.4], 'to': [1.4, 1.7, 4.8], 'lookAt': [1.4, 1.0, -0.9], 'fov': 40})
next(a for a in shots[18]['actors'] if a['id'] == 'patronMoustache')['attach'] = [{'name': 'mustache3d', 'joint': 'head', 'pos': [0, 0.15, 0.11], 'scale': 1.6}]
cam(18, preset='close', target='patronMoustache', angle=15, push=0.08, zoom=1.1)
cam(21, preset='full', target=[0.5, 1.7, 2.2], angle=30, zoom=1.0, push=0.05, glide=0.4)
cam(22, **{'from': [1.0, 0.5, 3.2], 'to': [0.85, 0.35, 2.95], 'lookAt': [0.6, 0.08, 2.5], 'fov': 34})
cam(24, preset='full', target=[0.3, 1.95, 1.0], angle=0, zoom=1.0, push=0.1)
cam(25, preset='full', target=[0.3, 1.95, 1.0], angle=30, orbit=120, zoom=1.05, push=0.0, glide=0.4)

assert len([x for x in shots if x['line']]) == len(lines), (len(shots), len(lines))
ep = {
    'title': 'Le chrono', 'captionWords': 3, 'minShot': 1.1,
    'music': {'mood': 'quirky', 'vol': 0.07},
    'voice': {'engine': 'elevenlabs', 'name': 'allan tiktok', 'model': 'eleven_v4', 'stability': 0.8, 'rate': 1.08, 'gap': 0.22},
    'cast': {
        M: {'preset': 'lemec'}, 'coll1': {'preset': 'lemec_glasses'}, 'coll2': {'preset': 'madame'}, 'coll3': {'preset': 'savant'},
        'patron': {'preset': 'boss', 'facial': 'none'}, 'patronMoustache': {'preset': 'boss', 'facial': 'mustache'},
        'vieux': {'preset': 'lemec_beige', 'hair': 'receding', 'hairColor': '#D8D8D8', 'facial': 'beard', 'build': {'height': 0.92}},
        'barman': {'preset': 'serveur'}, 'client1': {'preset': 'fermier'}, 'client2': {'preset': 'sportif'}, 'client3': {'preset': 'mamie'},
        'guichetier': {'preset': 'lemec_charcoal'}, 'vigile': {'preset': 'cop2'}, 'cliente': {'preset': 'madame'},
        'passant1': {'preset': 'tourist'}, 'passant2': {'preset': 'chef'}, 'pigeon': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 2}},
    },
    'shots': shots,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrono.json')
json.dump(ep, open(out, 'w'), ensure_ascii=False, indent=1)
print(out, len(shots), 'shots,', sum(len(s['line'].split()) for s in shots), 'words')
