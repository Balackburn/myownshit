"""Shared helpers for the autumn-2026 news series (actu01..actu10).

Faster cut and faster acting than the earlier episodes: narrator 1.12, characters 1.08, episode tempo 1.35
(snappier gestures, blends and turns). Standard set-ups validated once and reused: the interrogation room, the
machine-translated post lying on a table, the press-room apology, the cell, the court, the police arrival.
Gag bank: .claude/skills/ce-mec-shorts/references/gags-actu-automne-2026.md
"""
import json, os

PI = 3.14159
P_NAVY, P_INK, RED_INK = '#1E2E44', '#141A22', '#B3261E'

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
def POV(at, frm, look, lens=50): return {'at': at, 'from': frm, 'lookAt': look, 'lens': lens}
WM = lambda **kw: {'name': 'wmSign', 'id': 'wm', **kw}
HAND_FLAT = {'rot': [1.5708, 0, 0], 'offset': [0, -0.13, 0.02]}
SIGN_UP = {'offset': [0.12, 0.3, 0], 'rot': [3.1416, 0, 0]}   # a sign held overhead (raised arm: the hand's +y points down)
def CUP(actor, hand='L'): return {'actor': actor, 'hand': hand, 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]}

VOICE = {'name': 'allan tiktok', 'model': 'eleven_v4',
         'narrator': {'stability': 0.8, 'style': 0.0, 'rate': 1.12},
         'character': {'stability': 0.4, 'style': 0.45, 'rate': 1.08}}
TEMPO = 1.35
CAST = {
    'mec': {'preset': 'lemec'},
    'flic1': {'preset': 'cop'}, 'flic2': {'preset': 'cop2', 'seed': 41},
    'commissaire': {'preset': 'commissaire'},
}

# ---- interrogation room (set 'interrogation'): suspect on the far chair facing +z, the inspector leaning on the near edge
IR_SUSPECT = [0, 0.12, -1.33]           # human suspect, clip 'sit' / 'sitCuffed'
IR_ON_TABLE = [0, 0.785, -0.85]         # small creature or object suspect sitting on the table
IR_COP = [0.98, 0, -0.78]               # inspector at the table's right end, ry -90 (profile from the front), 'leanTable' / 'slamTable'
IR_COP2 = [-1.35, 0, -0.35]             # second cop standing at the side, ry 115, 'armsCrossed'
def ir_cams(t0, suspect, extra=()):
    """wide, the suspect under the lamp, an over-the-shoulder from the inspector"""
    return [cam(t0, ['commissaire', suspect], 'fs', worldAngle=30, elev=10), *extra]

# ---- a post lying flat on the table, read from above (the machine-translation gag)
def tweet_on_table(id, x, y, z, **opts):
    return P(id, 'tweetPhone', pos=[x, y + 0.008, z], rot=[-1.5708, 0, 0], opts=opts)
def tweet_cam(at, x, y, z, h=0.42): return POV(at, [x, y + h, z + 0.06], [x, y, z], 40)

# ---- press-room apology (set 'pressRoom'): the speaker behind the podium, journalists seated facing him
PR_SPEAKER = [0, 0, -2.45]
def journalists(n=5):
    return {'id': 'journo', 'count': n, 'spec': {'preset': 'lemec_charcoal'}, 'clip': 'sit', 'ry': 180,
            'positions': [[-2.4 + i * 1.2, 0.12, 2.1] for i in range(n)]}

def write(ep_name, title, scenes, cast_extra=None, music='quirky'):
    ep = {'version': 3, 'title': title, 'captionWords': 3, 'captionY': 0.66, 'tempo': TEMPO, 'voice': VOICE,
          'music': {'mood': music, 'vol': 0.06}, 'cast': {**CAST, **(cast_extra or {})}, 'scenes': scenes}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), ep_name + '.json')
    json.dump(ep, open(out, 'w'), ensure_ascii=False, indent=1)
    words = sum(len(l['text'].split()) for s in scenes for l in s['lines'])
    print(out, len(scenes), 'scenes,', sum(len(s['lines']) for s in scenes), 'lines,', words, 'words,', sum(len(s['cams']) for s in scenes), 'camera setups')
