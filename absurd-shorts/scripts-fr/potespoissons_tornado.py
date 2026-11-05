#!/usr/bin/env python3
"""potespoissons_tornado.py: the drowned man who built a city under the sea ("potes poissons", from the earlier short on the
person's TikTok), remade in the tornado-replica style (.claude/skills/lowpoly-story-style).

Narration: the earlier short's script (whisper, fixed against its captions), the series' narrator voice, time-stretched x1.10 and
placed back to back (potespoissons_timeline.json). Cuts land one frame before the opening word of each shot.
Render: node render/render3.mjs scripts-fr/potespoissons_render.json --timed --w 1080 --h 1920 --workers 4 --out out/potespoissons_3d.mp4
"""
import json, os, math
from actu_common import act, k, P

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, 'potespoissons_timeline.json')))
LINES = {l['id']: l for l in TL['lines']}
TOTAL = TL['total']
FPS = 30
fr = lambda t: round(round(t * FPS) / FPS, 4)
def ls(lid, w=0): return LINES[lid]['words'][w]['s']
def cut(lid, w=0): return fr(ls(lid, w) - 1 / FPS)


def cam(at, frm, to, look, look2=None, lens=50, ease='linear', shake=None, roll=None):
    c = {'at': at, 'from': frm, 'to': to, 'lookAt': look, 'lens': lens, 'ease': ease}
    if look2: c['lookAt2'] = look2
    if shake: c['shake'] = shake
    if roll: c['roll'] = roll
    return c


scenes = []
def scene(sid, set_, actors=(), props=(), cams=(), **kw):
    t0, t1 = SH[sid]
    scenes.append({'id': sid, 'set': set_, 'lines': [], 'actors': list(actors), 'props': list(props), 'sfx': [], 'cams': list(cams),
                   'start': round(t0, 4), 'duration': round(t1 - t0, 4), **kw})


def talk(lid, t0, base='neutral'):
    ks = []
    for w in LINES[lid]['words']:
        a, b = w['s'] - t0, w['e'] - t0
        if b < 0: continue
        ks += [k(round(max(0, a), 3), expr='talk'), k(round(max(0, b - 0.03), 3), expr=base)]
    return ks


C = [0.0, cut('L02'), cut('L03'), cut('L03', 4), cut('L04'), cut('L05'), cut('L06'), cut('L07'), cut('L08'), cut('L09'), cut('L10'), cut('L10', 3),
     cut('L11'), cut('L12'), cut('L12', 5), cut('L13'), cut('L14'), cut('L14', 5), cut('L15'), cut('L16'), cut('L17'), cut('L18'), cut('L18', 7),
     cut('L19'), cut('L20'), cut('L21'), cut('L22'), cut('L23'), cut('L24'), cut('L25'), cut('L26'), cut('L27'), TOTAL]
SH = {f'B{i + 1:02d}': (C[i], C[i + 1]) for i in range(len(C) - 1)}
def dur(sid): return SH[sid][1] - SH[sid][0]
def wt(lid, w, sid): return round(ls(lid, w) - SH[sid][0], 3)   # a word's time inside a shot

SEA = 'seaSurface'; BED = 'seabed'
FISH = lambda i: {'n': 6, 'rx': 4, 'rz': 2.5, 'y0': 0.8, 'y1': 3.0, 'seed': i, 'speed': 0.5}

# B01 "Ce mec est parti se baigner.": on the beach, low behind him as he strides into the waves
scene('B01', SEA, actors=[act('mec', [0.5, 0, 9.5], 180, 'walk', 'happy', keys=[k(0.0, to=[0.6, 0, 5.2], dur=round(dur('B01'), 3), clip='run')])],
      cams=[cam(0.0, [1.6, 0.6, 13.6], [1.5, 0.65, 11.2], [0.4, 0.9, 4.0], [0.5, 0.85, 1.0], lens=50, shake=0.02)])
# B02 "Il savait pas nager.": chest-deep, flailing, waves slapping round him
scene('B02', SEA, setOpts={'parasols': False},
      actors=[act('mec', [0, -1.15, -4], 10, 'flail', 'scared')],
      props=[P('splash', 'bubbles', pos=[0, 0.1, -3.7], opts={'rate': 2.5, 'h': 0.8, 'area': 1.2, 'speed': 2})],
      cams=[cam(0.0, [1.2, 0.5, -0.9], [1.0, 0.45, -1.2], [0, 0.6, -4], [0, 0.55, -4], lens=46, shake=0.03)])
# B03 "Il s'en est souvenu": water at the chin, the penny drops (eyes wide)
scene('B03', SEA, setOpts={'parasols': False},
      actors=[act('mec', [0, -1.4, -4], 10, 'stand', 'neutral', keys=[k(0.3, expr='surprised')])],
      cams=[cam(0.0, [0.35, 0.42, -2.2], [0.32, 0.4, -2.45], [0, 0.42, -4], [0, 0.42, -4], lens=44, shake=0.012)])
# B04 "au beau milieu de l'océan.": straight up and away: a dot in an endless sea (crane up)
scene('B04', SEA, setOpts={'parasols': False, 'shore': 160},
      actors=[act('mec', [0, -1.4, -4], 10, 'flail', 'shocked')],
      cams=[cam(0.0, [3, 9, 4], [5, 30, 12], [0, 0, -4], [0, 0, -4], lens=44)], far=900)
# B05 "Il s'est noyé.": from below, he sinks out of the bright surface trailing bubble rings
scene('B05', BED, actors=[act('mec', [0, 26, -6], 0, 'armsUp', 'scared', keys=[k(0.0, to=[0, 19, -6], dur=round(dur('B05'), 3), ease='out')])],
      props=[P('rings', 'bubbles', pos=[0, 20, -6], opts={'rate': 2, 'h': 8, 'area': 0.6, 'speed': 1.5})],
      cams=[cam(0.0, [2.5, 12, 4], [2.4, 12.3, 3.6], [0, 23, -6], [0, 21, -6], lens=50)])
# B06 "Au fond, il respirait.": on the sand, close: he breathes calmly, a ring rising from his nose each breath; fish drift by
scene('B06', BED, actors=[act('mec', [0, 0, 0], 0, 'idle', 'unimpressed', keys=[k(0.6, expr='neutral')])],
      props=[P('breath', 'bubbles', pos=[0.06, 1.86, 0.36], opts={'burst': [[0.3, 1], [0.95, 1]], 'h': 1.6, 'big': 0.05, 'facing': True}),
             P('school', 'fishSchool', pos=[0, 0, -2], opts=FISH(1))],
      cams=[cam(0.0, [0.25, 1.95, 1.75], [0.25, 1.95, 1.55], [0, 1.95, 0], [0, 1.95, 0], lens=44, shake=0.008)])
# B07 "Du coup, il s'est fait des potes poissons.": three fish round him, he waves; a school behind
scene('B07', BED, actors=[act('mec', [0, 0, 0], 0, 'wave', 'happy'),
                          act('p1', [-1.0, 1.5, 0.6], 90, 'swim', keys=[k(0.0, to=[-0.7, 1.7, 0.7], dur=round(dur('B07'), 3))]),
                          act('p2', [1.1, 1.2, 0.4], -90, 'swim', keys=[k(0.0, to=[0.8, 1.35, 0.5], dur=round(dur('B07'), 3))]),
                          act('p3', [0.3, 2.3, 0.8], -110, 'swim')],
      props=[P('school', 'fishSchool', pos=[0, 0, -3], opts={**FISH(2), 'n': 9})],
      cams=[cam(0.0, [0.2, 1.3, 4.6], [0.2, 1.35, 4.1], [0, 1.45, 0], [0, 1.5, 0], lens=46)])
# B08 "Trois bulles : bonjour.": close on a fish puffing three bubble rings at him
scene('B08', BED, actors=[act('p1', [0, 1.4, 0], -90, 'swim')],
      props=[P('hi', 'bubbles', pos=[-0.18, 1.98, 0.05], opts={'burst': [[0.3, 3]], 'gap': 0.18, 'h': 1.5, 'big': 0.06, 'life': 1.2, 'facing': True})],
      cams=[cam(0.0, [0.0, 2.05, 2.2], [0.0, 2.05, 1.95], [0, 1.95, 0], [0, 1.95, 0], lens=42)])
# B09 "Quatre : ta gueule.": he puffs four back at it, deadpan
scene('B09', BED, actors=[act('mec', [0, 0, 0], 20, 'stand', 'unimpressed'), act('p1', [-0.9, 1.75, 0.6], 90, 'swim')],
      props=[P('shut', 'bubbles', pos=[0.05, 1.86, 0.35], opts={'burst': [[0.15, 4]], 'gap': 0.13, 'h': 1.4, 'big': 0.06, 'life': 1.0, 'facing': True})],
      cams=[cam(0.0, [0.9, 1.9, 2.2], [0.85, 1.9, 2.0], [-0.2, 1.95, 0.2], [-0.2, 1.95, 0.2], lens=42)])
# B10 "Il a inventé le feu sous l'eau.": low angle, he holds up a flame; the fish recoil
scene('B10', BED, actors=[act('mec', [0, 0, 0], 0, 'raiseOverhead', 'smug'), act('p2', [1.2, 1.6, 0.4], -90, 'swim', keys=[k(0.25, to=[1.8, 1.7, 0.2], dur=0.4, ease='out')])],
      props=[P('fire', 'flame', on={'actor': 'mec', 'hand': 'R'}, scale=3.2)],
      cams=[cam(0.0, [0.4, 0.45, 3.0], [0.45, 0.48, 2.7], [0, 2.0, 0], [0, 2.05, 0], lens=50)])
# B11 "Premier barbecue :": the grill, a fish sizzling on it, he turns it over
scene('B11', BED, actors=[act('mec', [0.55, 0, -0.2], -60, 'holdOut', 'happy')],
      props=[P('bbq', 'barbecue', pos=[0, 0, 0.1])],
      cams=[cam(0.0, [0.9, 1.45, 3.3], [0.85, 1.45, 3.1], [0.25, 1.15, 0.0], [0.25, 1.15, 0.0], lens=44)])
# B12 "incident diplomatique.": reverse: the fish friends staring at the grill (INCIDENT DIPLOMATIQUE card)
scene('B12', BED, actors=[act('p1', [-0.6, 0.9, -0.9], 30, 'swim'), act('p2', [0.0, 1.05, -1.1], 0, 'swim'), act('p3', [0.6, 0.85, -0.9], -30, 'swim')],
      props=[P('bbq', 'barbecue', pos=[0, 0, 0.9])],
      cams=[cam(0.0, [0.0, 1.35, 2.6], [0.0, 1.35, 2.4], [0, 1.25, -0.9], [0, 1.25, -0.9], lens=44)])
# B13 "Un poisson l'a éteint.": a fish blows on the fire: it dies in a puff, he stands there
scene('B13', BED, actors=[act('mec', [0.75, 0, 0], -60, 'stand', 'unimpressed'), act('p3', [-0.6, 0.95, 0.2], 90, 'swim')],
      props=[P('bbq', 'barbecue', pos=[0, 0, 0.1], opts={'out': [[0.45, True]]}),
             P('gust', 'bubbles', pos=[-0.3, 0.95, 0.2], opts={'burst': [[0.2, 6]], 'gap': 0.04, 'h': 0.9, 'big': 0.05, 'life': 0.7}),
             P('puff', 'sandPuff', pos=[0, 0.85, 0.1], scale=0.18, opts={'t0': 0.45, 'n': 6})],
      cams=[cam(0.0, [0.1, 1.3, 3.0], [0.05, 1.3, 2.8], [0.05, 1.0, 0.05], [0.05, 1.0, 0.05], lens=44)])
# B14 "Ils ont planté des algues,": a field of seaweed popping up row by row
t14 = [0.1 + 0.12 * i for i in range(8)]
scene('B14', BED, actors=[act('mec', [1.4, 0, 0.8], -70, 'idle', 'smug')],
      props=[P(f'w{i}', 'seaweed', pos=[-1.4 + (i % 4) * 0.9, 0, -0.6 - (i // 4) * 0.9], scale=0.01, opts={'seed': 40 + i, 'n': 5, 'h': 1.1},
               keys=[k(t14[i], scale=1.0, dur=0.25, ease='outBack')]) for i in range(8)],
      cams=[cam(0.0, [0.0, 1.6, 3.6], [0.0, 1.55, 3.3], [-0.1, 0.7, -1.0], [-0.1, 0.7, -1.0], lens=44)])
# B15 "inventé la roue.": a fish in a wheeled cart rolls past the lens
scene('B15', BED, props=[P('cart', 'fishCart', pos=[-3.5, 0, 0], rot=[0, 0, 0], opts={'roll': 9, 'seed': 1}, keys=[k(0.0, to=[3.5, 0, 0], dur=round(dur('B15'), 3), ease='linear')])],
      cams=[cam(0.0, [-0.6, 0.6, 2.4], [0.6, 0.6, 2.4], [-1.0, 0.55, 0], [1.0, 0.55, 0], lens=44)])
# B16 "Puis les embouteillages.": a jam of fish carts nose to tail, creeping, one honking bubbles
scene('B16', BED, props=[P(f'c{i}', 'fishCart', pos=[-6 + i * 1.25, 0, -1.2 - 0.05 * (i % 2)], opts={'roll': 1.5, 'seed': i}, keys=[k(0.0, to=[-5.6 + i * 1.25, 0, -1.2 - 0.05 * (i % 2)], dur=round(dur('B16'), 3))]) for i in range(9)] +
      [P('honk', 'bubbles', pos=[0.35, 0.95, -1.2], opts={'burst': [[0.3, 2], [0.8, 2]], 'gap': 0.08, 'h': 1.2})],
      cams=[cam(0.0, [2.2, 0.55, 2.4], [2.0, 0.6, 2.2], [-1.5, 0.6, -1.2], [-1.5, 0.6, -1.2], lens=42)])
# B17 "Construire leur putain de ville": the huts go up one after another round him
hut = [(-2.6, -3.0), (0.4, -4.6), (3.0, -3.2), (-4.2, -6.4), (2.0, -7.6)]
scene('B17', BED, actors=[act('mec', [0.2, 0, -0.6], 0, 'carryBox', 'worried')],
      props=[P(f'h{i}', 'stoneHut', pos=[x, 0, z], scale=0.01, keys=[k(0.12 + i * 0.16, scale=1.0, dur=0.28, ease='outBack')]) for i, (x, z) in enumerate(hut)],
      cams=[cam(0.0, [0.6, 1.4, 4.6], [0.6, 1.5, 4.2], [0, 1.2, -3.0], [0, 1.25, -3.0], lens=44)])
# B18 "lui a pris un an.": the finished village, fish everywhere; crane up
scene('B18', BED, actors=[act('mec', [0.2, 0, -0.6], 0, 'handsOnHips', 'smug')],
      props=[P(f'h{i}', 'stoneHut', pos=[x, 0, z]) for i, (x, z) in enumerate(hut)] + [P('school', 'fishSchool', pos=[0, 1, -4], opts={**FISH(5), 'n': 12, 'rx': 6, 'rz': 4})],
      cams=[cam(0.0, [1.0, 1.8, 6.0], [1.2, 4.2, 6.8], [0, 1.0, -3.5], [0, 0.8, -3.5], lens=44)])
# B19 "Le courant défaisait les murs chaque soir.": a current sweeps through and flattens the walls; he facepalms
scene('B19', BED, actors=[act('mec', [0.9, 0, 0.8], -30, 'stand', 'sad', keys=[k(0.8, clip='facepalm')])],
      props=[P('h0', 'stoneHut', pos=[-0.8, 0, -1.6], opts={'collapse': [[0.45, True]]}),
             P('streaks', 'speedLines', pos=[-4, 1.2, -1.2], rot=[0, 1.5708, 0], scale=2.0, keys=[k(0.2, to=[3, 1.2, -1.2], dur=0.7, ease='linear')]),
             P('puff', 'sandPuff', pos=[-0.8, 0, -1.6], opts={'t0': 0.5})],
      cams=[cam(0.0, [0.4, 1.4, 5.6], [0.35, 1.4, 5.3], [0.0, 1.0, -0.8], [0.0, 1.0, -0.8], lens=44, shake=0.015)])
# B20 "Il a branché une anguille.": the eel undulating, he jams its cable into the socket
scene('B20', BED, actors=[act('mec', [-1.55, 0, 0.75], 70, 'holdOut', 'smug')],
      props=[P('eel', 'eelPlug', pos=[1.2, 0, 0], opts={'len': 1.5})],
      cams=[cam(0.0, [-0.65, 1.35, 5.6], [-0.7, 1.35, 5.3], [-0.75, 0.9, 0.2], [-0.75, 0.9, 0.2], lens=44)])
# B21 "Électricité.": sparks crackle off the eel, the huts' windows light up (pop)
scene('B21', BED, actors=[act('mec', [-1.55, 0, 0.75], 70, 'startle', 'shocked')],
      props=[P('eel', 'eelPlug', pos=[1.2, 0, 0], opts={'len': 1.5, 'zapAt': 0.05})],
      cams=[cam(0.0, [-0.1, 1.2, 4.2], [-0.15, 1.2, 4.0], [-0.1, 0.85, 0], [-0.1, 0.85, 0], lens=44, shake=0.03)])
# B22 "En dix minutes, ils avaient des gratte-ciel,": neon towers burst out of the sand one after another (tilt up)
tow = [(-4.0, -8, 18), (0.5, -11, 26), (4.5, -9, 21), (-1.8, -15, 30), (7.5, -14, 24), (-7.0, -13, 22)]
scene('B22', BED, setOpts={'fogFar': 110},
      props=[P(f't{i}', 'neonTower', pos=[x, 0, z], opts={'h': h, 'w': 3.2, 'd': 3.2, 'riseAt': 0.1 + i * 0.18, 'riseDur': 0.45}) for i, (x, z, h) in enumerate(tow)],
      cams=[cam(0.0, [0.4, 1.0, 21.0], [0.4, 1.2, 19.5], [0.2, 6.0, -10], [0.2, 10.0, -10], lens=46)])
# B23 "des robots et la 6G.": robots trundle past, the 6G mast lights up bar by bar
scene('B23', BED, setOpts={'fogFar': 110},
      actors=[act('r1', [-1.3, 0, 0.6], 90, 'walk', keys=[k(0.0, to=[0.3, 0, 0.6], dur=round(dur('B23'), 3), clip='walk')]),
              act('r2', [-2.0, 0, -0.5], 90, 'walk', keys=[k(0.0, to=[-0.4, 0, -0.5], dur=round(dur('B23'), 3), clip='walk')])],
      props=[P(f't{i}', 'neonTower', pos=[x, 0, z], opts={'h': h, 'w': 3.2, 'd': 3.2}) for i, (x, z, h) in enumerate(tow)] +
            [P('mast', 'signal6G', pos=[1.6, 1.6, -0.8], opts={'t0': wt('L18', 11, 'B23') - 0.1, 'w': 1.0, 'h': 1.3})],
      cams=[cam(0.0, [0.4, 1.4, 6.4], [0.35, 1.45, 6.0], [0.1, 1.4, -0.5], [0.1, 1.45, -0.5], lens=44)])
# B24 "Enfin du réseau.": close on him with his phone, full bars, delighted
scene('B24', BED, setOpts={'fogFar': 110},
      actors=[act('mec', [0, 0, 0], 0, 'readPhone', 'happy')],
      props=[P('tel', 'phone911', on={'actor': 'mec', 'hand': 'R'}), P('t1', 'neonTower', pos=[3, 0, -10], opts={'h': 26})],
      cams=[cam(0.0, [0.55, 1.65, 2.2], [0.5, 1.65, 2.0], [0.1, 1.6, 0], [0.1, 1.62, 0], lens=44)])
# B25 "Il a appelé les flics.": at the station the cop picks up (POLICE on the wall)
scene('B25', 'office', actors=[act('flic', [0, 0, -0.6], 0, 'phoneCall', 'unimpressed')],
      props=[P('tel', 'phone911', on={'actor': 'flic', 'hand': 'R'}), P('sign', 'noticeBoard', pos=[0.05, 2.2, -1.6], opts={'text': 'POLICE', 'style': 'sign', 'w': 1.1, 'h': 0.38, 'fg': '#FFFFFF', 'frame': '#FFFFFF'})],
      cams=[cam(0.0, [0.25, 1.55, 1.8], [0.25, 1.55, 1.6], [0.05, 1.55, -0.6], [0.05, 1.57, -0.6], lens=44)])
# B26 "L'océan a essayé de me tuer !": him on the phone under the sea, furious, towers behind
scene('B26', BED, setOpts={'fogFar': 110},
      actors=[act('mec', [0, 0, 0], 0, 'phoneCall', 'angry', keys=talk('L21', SH['B26'][0], 'angry'))],
      props=[P('tel', 'phone911', on={'actor': 'mec', 'hand': 'R'})] + [P(f't{i}', 'neonTower', pos=[x, 0, z], opts={'h': h}) for i, (x, z, h) in enumerate(tow[:4])],
      cams=[cam(0.0, [0.45, 1.6, 2.0], [0.4, 1.62, 1.8], [0.05, 1.8, 0], [0.05, 1.82, 0], lens=44, shake=0.012)])
# B27 "Tentative de meurtre.": the cop, grave, writing it down (TENTATIVE DE MEURTRE card)
scene('B27', 'office', actors=[act('flic', [0, 0, -0.6], 0, 'clipboard', 'suspicious')],
      props=[P('sign', 'noticeBoard', pos=[0.05, 2.2, -1.6], opts={'text': 'POLICE', 'style': 'sign', 'w': 1.1, 'h': 0.38, 'fg': '#FFFFFF', 'frame': '#FFFFFF'})],
      cams=[cam(0.0, [-0.3, 1.5, 1.6], [-0.25, 1.5, 1.45], [0.05, 1.6, -0.6], [0.05, 1.6, -0.6], lens=44)])
# B28 "Les poissons étaient là.": a fish lineup against the height chart
scene('B28', 'brightCell', setOpts={'bars': False},
      actors=[act('p1', [-0.7, 1.2, -1.2], 0, 'swim'), act('p2', [0.0, 1.3, -1.2], 0, 'swim'), act('p3', [0.7, 1.15, -1.2], 0, 'swim')],
      props=[P('wall', 'mugshotBoard', pos=[0, 0, -1.58], opts={'w': 2.4, 'h': 2.4})],
      cams=[cam(0.0, [0.0, 1.4, 2.4], [0.0, 1.4, 2.2], [0, 1.3, -1.2], [0, 1.3, -1.2], lens=44)])
# B29 "Complices.": push in on the middle fish, flash
scene('B29', 'brightCell', setOpts={'bars': False},
      actors=[act('p1', [-0.7, 1.2, -1.2], 0, 'swim'), act('p2', [0.0, 1.3, -1.2], 0, 'swim'), act('p3', [0.7, 1.15, -1.2], 0, 'swim')],
      props=[P('wall', 'mugshotBoard', pos=[0, 0, -1.58], opts={'w': 2.4, 'h': 2.4})],
      cams=[cam(0.0, [0.0, 1.9, 0.5], [0.0, 1.9, 0.2], [0, 1.85, -1.2], [0, 1.85, -1.2], lens=42, shake=0.03)])
# B30 "Les flics ont coffré l'océan et tous ses potes.": the whole sea in a tank on the sand, OCÉAN EN GARDE À VUE, a police car, a cop
scene('B30', BED, setOpts={'dry': True},
      actors=[act('flic', [3.0, 0, 1.0], -40, 'handsOnHips', 'smug')],
      props=[P('tank', 'oceanTank', pos=[0, 0, -1.5], opts={'w': 4.2, 'h': 2.7, 'd': 2.4}), P('car', 'policeCar', pos=[-4.2, 0, 0.8], rot=[0, 0.5, 0])],
      cams=[cam(0.0, [0.8, 1.8, 11.5], [0.6, 1.8, 10.5], [-0.3, 1.5, -0.6], [-0.3, 1.5, -0.6], lens=46)])
# B31 "La ville s'est asséchée.": the neon city high and dry on the sand under a hard sun; crane up
scene('B31', BED, setOpts={'dry': True},
      actors=[act('mec', [0, 0, 2.0], 0, 'stand', 'unimpressed')],
      props=[P(f't{i}', 'neonTower', pos=[x, 0, z], opts={'h': h, 'flicker': [[0, False]]}) for i, (x, z, h) in enumerate(tow)],
      cams=[cam(0.0, [1.0, 1.0, 8.0], [1.2, 3.0, 9.0], [0, 3.5, -6], [0, 4.0, -6], lens=46)])
# B32 "Le mec a inventé la soif.": close: an empty glass, deadpan, then the sad face; hold
scene('B32', BED, setOpts={'dry': True},
      actors=[act('mec', [0, 0, 0], 0, 'holdOut', 'unimpressed', keys=[k(1.0, expr='sad')])],
      props=[P('glass', 'waterGlass', on={'actor': 'mec', 'hand': 'R'}, scale=2.6)],
      cams=[cam(0.0, [0.75, 1.5, 2.3], [0.7, 1.52, 2.1], [0.2, 1.45, 0], [0.2, 1.47, 0], lens=44)])

for sc_ in scenes:
    for p_ in sc_['props']:
        if 'rot' in p_ and 'ry' not in p_:
            p_['ry'] = round(math.degrees(p_['rot'][1]), 3)

OUT_W = 1080; SOFT = 0.45 * OUT_W / 576
for sc_ in scenes:
    s = sc_['set']; under = s == 'seabed' and not sc_.get('setOpts', {}).get('dry')
    sc_['grade'] = ('contrast(0.92) saturate(1.12) brightness(1.06)' if under else
                    {'office': 'contrast(0.9) saturate(1.05) brightness(1.1)', 'brightCell': 'contrast(0.9) saturate(1.05) brightness(1.1)'}.get(s, 'contrast(0.9) saturate(1.08) brightness(1.08)'))
    sc_['soften'] = round(SOFT, 2)

FISHCOL = {'p1': {'body': '#F2C230', 'fin': '#E8A33C', 'belly': '#F8E2A0'}, 'p2': {'body': '#4FD1C5', 'fin': '#2FA89C', 'belly': '#C8F1EC'}, 'p3': {'body': '#E8742E', 'fin': '#C9562A', 'belly': '#F6C49A'}}
doc = {'version': 3, 'title': 'Potes poissons (tornado style)', 'grade': 'contrast(0.9) saturate(1.05) brightness(1.06)', 'captionWords': 0, 'captionY': 0.81, 'tempo': 1.0,
       'voice': None, 'music': None,
       'cast': {'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
                'flic': {'preset': 'cop', 'suit': '#1E2D4A', 'pants': '#1E2D4A', 'facial': 'none', 'atlas': 'lemec', 'atlasBody': False, 'build': {'width': 0.82, 'headWidth': 1.3}},
                **{f: {'type': 'creature', 'name': 'fish', 'opts': {'seed': i + 2, 'colors': c}} for i, (f, c) in enumerate(FISHCOL.items())},
                'r1': {'type': 'creature', 'name': 'robot', 'opts': {'seed': 3}}, 'r2': {'type': 'creature', 'name': 'robot', 'opts': {'seed': 8}}},
       'scenes': scenes, 'total': TOTAL}
out = os.path.join(HERE, 'potespoissons_tornado.json')
json.dump(doc, open(out, 'w'), indent=1, ensure_ascii=False)
print(out, len(scenes), 'scenes', TOTAL, 's')
for sid, (a, b) in SH.items(): print(f'{sid} {a:6.3f}-{b:6.3f} ({b - a:4.2f}s)', end='  |  ' if int(sid[1:]) % 4 else '\n')
