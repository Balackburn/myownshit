#!/usr/bin/env python3
"""vospapiers_tornado.py: "Vos papiers" remade in the style of the tornado replica (fast cuts, no pauses, low angles,
orbits and push-ins, bright sky, pastel facades, rain, pop-in signs, motion blur on fast moves).

The narration is the French script extracted from the earlier "vos-papiers" short (whisper), spoken by the series'
narrator voice and placed back to back (vospapiers_timeline.json: line and word times). Every cut lands one frame
before a line (or a word) starts; quoted lines move the speaker's mouth on the spoken words.
Render: node render/render3.mjs scripts-fr/vospapiers_tornado.json --timed --w 1080 --h 1920 --workers 4 --out out/vospapiers_3d.mp4
"""
import json, os, math
from actu_common import act, k, P, HAND_FLAT, SIGN_UP

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, 'vospapiers_timeline.json')))
LINES = {l['id']: l for l in TL['lines']}
TOTAL = TL['total']
FPS = 30
fr = lambda t: round(round(t * FPS) / FPS, 4)
def ls(lid, w=0): return LINES[lid]['words'][w]['s']   # time a word starts
def cut(lid, w=0): return fr(ls(lid, w) - 1 / FPS)       # a cut one frame before it


def cam(at, frm, to, look, look2=None, lens=50, ease='linear', shake=None, roll=None):
    c = {'at': at, 'from': frm, 'to': to, 'lookAt': look, 'lens': lens, 'ease': ease}
    if look2: c['lookAt2'] = look2
    if shake: c['shake'] = shake
    if roll: c['roll'] = roll
    return c


scenes = []
def scene(sid, t0, t1, set_, actors=(), props=(), cams=(), **kw):
    scenes.append({'id': sid, 'set': set_, 'lines': [], 'actors': list(actors), 'props': list(props), 'sfx': [], 'cams': list(cams),
                   'start': round(t0, 4), 'duration': round(t1 - t0, 4), **kw})


def talk(lid, t0, base='neutral'):
    """mouth keys for a quoted line, relative to the scene start t0: 'talk' on each word, the base face in between"""
    ks = []
    for w in LINES[lid]['words']:
        a, b = w['s'] - t0, w['e'] - t0
        if b < 0: continue
        ks += [k(round(max(0, a), 3), expr='talk'), k(round(max(0, b - 0.03), 3), expr=base)]
    return ks


# shot boundaries: one frame before the line (or word) that opens each shot
C = [0.0, cut('L02'), cut('L02', 5), cut('L03'), cut('L04'), cut('L05'), cut('L06'), cut('L07'), cut('L08'), cut('L09'), cut('L10'), cut('L10', 3),
     cut('L11'), cut('L12'), cut('L13'), cut('L14'), cut('L15'), cut('L16'), cut('L17'), cut('L18'), cut('L19'), cut('L20'), cut('L20', 4),
     cut('L21'), cut('L22'), cut('L23'), cut('L24'), cut('L25'), cut('L26'), cut('L27'), TOTAL]
SH = {f'A{i + 1:02d}': (C[i], C[i + 1]) for i in range(len(C) - 1)}
def span(sid): return SH[sid]
def dur(sid): return SH[sid][1] - SH[sid][0]

GREY = {'color': '#9AA4AE', 'color2': '#B0B9C2'}
WHITE = {'color': '#F2F5F8', 'color2': '#FFFFFF', 'face': 'happy'}
SIGN = {'text': 'ON VEUT\nDU SOLEIL'}

# A01 0.0: Paris, low and close in front of him: he chants under his sign, the street and the Eiffel tower behind; slow truck right
t0, t1 = span('A01')
scene('A01', t0, t1, 'parisStreet',
    actors=[act('mec', [7.0, 0, 0], 8, 'holdSign', 'angry', keys=[k(0.0, clip='chant'), k(0.7, clip='holdSign')])],
    props=[P('sign', 'protestSign', opts=SIGN, scale=1.5, on={'actor': 'mec', 'hand': 'R', **SIGN_UP})],
    cams=[cam(0.0, [5.5, 0.7, 4.1], [6.0, 0.75, 3.8], [6.8, 2.35, -1.0], [6.95, 2.4, -1.0], lens=52, shake=0.02)])

# A02: low angle straight up past him: the grey cloud slides in over his head and stops (frowning); he looks up
t0, t1 = span('A02')
scene('A02', t0, t1, 'parisStreet',
    actors=[act('mec', [7.0, 0, 0], 8, 'holdSign', 'neutral', keys=[k(0.3, clip='lookUp', expr='worried')])],
    props=[P('sign', 'protestSign', opts=SIGN, on={'actor': 'mec', 'hand': 'R', **SIGN_UP}),
           P('cloud', 'cloudChar', pos=[11.5, 3.9, -0.8], opts={**GREY, 'expr': [[0, 'grumpy'], [0.7, 'smug']], 'rain': [[0.75, True]]}, scale=1.2,
             keys=[k(0.0, to=[7.3, 3.7, -0.6], dur=0.65, ease='out')])],
    cams=[cam(0.0, [6.1, 0.4, 2.9], [6.2, 0.42, 2.75], [7.1, 3.35, -0.6], [7.1, 3.45, -0.6], lens=52)])

# A03: close on his face in the downpour: deadpan, soaked (the rain sheet falls right past the lens)
t0, t1 = span('A03')
scene('A03', t0, t1, 'parisStreet',
    actors=[act('mec', [7.0, 0, 0], 8, 'stand', 'unimpressed', keys=[k(0.55, expr='sad')])],
    props=[P('rain', 'rain', pos=[7.0, 0.2, 0.25], opts={'w': 1.6, 'd': 1.2, 'h': 3.2, 'n': 220, 'speed': 3.0, 'len': 0.26}),
           P('cloud', 'cloudChar', pos=[7.2, 3.9, -0.3], opts={**GREY, 'face': 'smug', 'raining': True}, scale=1.0)],
    cams=[cam(0.0, [6.95, 1.86, 1.45], [6.98, 1.85, 1.25], [7.0, 1.86, 0], [7.0, 1.86, 0], lens=46, shake=0.008)])

# A04 "Agression !": waist-up, he jabs a finger up at the cloud and yells (the AGRESSION card drops in over it)
t0, t1 = span('A04')
scene('A04', t0, t1, 'parisStreet',
    actors=[act('mec', [7.0, 0, 0], 8, 'pokeUp', 'angry', keys=talk('L03', t0, 'angry'))],
    props=[P('rain', 'rain', pos=[7.0, 0.2, 0.0], opts={'w': 2.4, 'd': 1.6, 'h': 3.6, 'n': 160, 'speed': 3.0}),
           P('cloud', 'cloudChar', pos=[7.6, 3.6, -0.6], opts={**GREY, 'face': 'smug', 'raining': True}, scale=1.0)],
    cams=[cam(0.0, [5.5, 1.05, 2.5], [5.65, 1.1, 2.25], [7.1, 2.0, -0.2], [7.1, 2.05, -0.2], lens=48, shake=0.015)])

# A05 "Il a appelé les flics.": phone to his ear in the rain, slow push-in
t0, t1 = span('A05')
scene('A05', t0, t1, 'parisStreet',
    actors=[act('mec', [7.0, 0, 0], 8, 'phoneCall', 'angry')],
    props=[P('tel', 'phone911', on={'actor': 'mec', 'hand': 'R'}),
           P('rain', 'rain', pos=[7.0, 0.2, 0.1], opts={'w': 2.2, 'd': 1.4, 'h': 3.6, 'n': 140, 'speed': 3.0}),
           P('cloud', 'cloudChar', pos=[7.5, 3.7, -0.8], opts={**GREY, 'face': 'smug', 'raining': True}, scale=1.0)],
    cams=[cam(0.0, [6.2, 1.62, 1.55], [6.4, 1.64, 1.2], [7.0, 1.72, 0], [7.0, 1.73, 0], lens=42)])

# A06 the border post in the street: a cop by a raised barrier lets white clouds float through (low angle)
CHK = [5.2, 0, 30.0]
t0, t1 = span('A06')
whites = [P(f'w{i}', 'cloudChar', pos=[11 + i * 4.2, 2.3 + 0.3 * (i % 2), 29.2 - 0.4 * i], opts={**WHITE, 'seed': i + 3}, scale=0.75,
            keys=[k(0.0, to=[-9 + i * 4.2, 2.3 + 0.3 * (i % 2), 29.2 - 0.4 * i], dur=round(dur('A06') + 0.4, 3), ease='linear')]) for i in range(3)]
scene('A06', t0, t1, 'parisStreet',
    actors=[act('flic', [3.9, 0, 31.3], 160, 'idle', 'unimpressed', keys=[k(0.4, clip='wave'), k(1.3, clip='idle')])],
    props=[P('gate', 'barrierGate', pos=CHK, rot=[0, 3.1416, 0], opts={'length': 5.0, 'angle': 78, 'sign': 'FRONTIÈRE'})] + whites,
    cams=[cam(0.0, [1.0, 0.85, 38.0], [1.5, 0.9, 37.4], [3.6, 2.0, 30.0], [3.7, 2.0, 30.0], lens=46)])

# A07 "Celui-là était gris.": the grey cloud drifts up to the post, the barrier drops in its face, the cop holds up a hand
t0, t1 = span('A07')
scene('A07', t0, t1, 'parisStreet',
    actors=[act('flic', [3.9, 0, 31.3], 120, 'idle', 'suspicious', keys=[k(0.45, clip='holdOut')])],
    props=[P('gate', 'barrierGate', pos=CHK, rot=[0, 3.1416, 0], opts={'length': 5.0, 'angle': 78, 'open': [[0.42, 0]], 'sign': 'FRONTIÈRE'}),
           P('cloud', 'cloudChar', pos=[11.5, 2.5, 29.4], opts={**GREY, 'expr': [[0, 'neutral'], [0.5, 'shocked']]}, scale=0.95,
             keys=[k(0.0, to=[2.6, 2.5, 29.4], dur=0.6, ease='out')])],
    cams=[cam(0.0, [2.2, 1.4, 37.4], [2.4, 1.4, 37.0], [3.4, 2.0, 30.0], [3.4, 2.0, 30.0], lens=46)])

# A08 "Vos papiers !": close on the cop, hand out, barking it (VOS PAPIERS card)
t0, t1 = span('A08')
scene('A08', t0, t1, 'parisStreet',
    actors=[act('flic', [3.9, 0, 31.3], 204, 'holdOut', 'angry', keys=talk('L07', t0, 'angry'))],
    props=[P('gate', 'barrierGate', pos=CHK, rot=[0, 3.1416, 0], opts={'length': 5.0, 'angle': 0, 'sign': 'FRONTIÈRE'})],
    cams=[cam(0.0, [3.15, 1.86, 29.35], [3.2, 1.86, 29.55], [3.9, 1.8, 31.3], [3.9, 1.8, 31.3], lens=44, shake=0.012)])

# A09 "Le nuage venait de Belgique.": aerial over the map, descending; the red route draws Brussels -> Paris and a tiny cloud rides it
t0, t1 = span('A09')
K = 10
pr = lambda lon, lat: [round((lon - 3) * K * 0.68, 2), round(-(lat - 47.5) * K, 2)]
bx, bz = pr(4.35, 50.85); px, pz = pr(2.35, 48.86)
scene('A09', t0, t1, 'skyHigh', setOpts={'layer': False, 'fog': False},
    props=[P('map', 'frMap', pos=[0, 0, 0], opts={'k': K}),
           P('route', 'dashRoute', pos=[0, 0, 0], opts={'k': K, 't0': 0.15, 'dur': 1.1}),
           P('mini', 'cloudChar', pos=[bx, 2.4, bz], opts={**GREY, 'face': 'happy', 'bob': 0.15}, scale=1.1,
             keys=[k(0.15, to=[px, 2.4, pz], dur=1.15, ease='inOut')])],
    cams=[cam(0.0, [6, 120, 34], [4, 96, 26], [3, 0, -10], [3, 0, -10], lens=42)], fog=None)

# A10 "Il avait suivi le vent.": tracking alongside the grey cloud as the wind hurls it along (streaks, motion blur)
t0, t1 = span('A10')
scene('A10', t0, t1, 'skyHigh', setOpts={'layer': True},
    props=[P('cloud', 'cloudChar', pos=[20, 60, 0], opts={**GREY, 'face': 'happy', 'bob': 0.25}, scale=1.0, keys=[k(0.0, to=[-24, 60.6, 0], dur=round(dur('A10'), 3), ease='linear')]),
           P('streaks', 'speedLines', pos=[20, 60.6, 0.5], rot=[0, 1.5708, 0], scale=2.4, keys=[k(0.0, to=[-24, 60.6, 0.5], dur=round(dur('A10'), 3), ease='linear')])],
    cams=[cam(0.0, [24, 60.4, 7.5], [-20, 60.6, 7.5], [20, 60.8, 0], [-24, 60.8, 0], lens=40, shake=0.03)],
    blur=[[0.0, dur('A10'), 0.012]], blurSamples=6)

# A11 "Encore un étranger.": the cop, arms crossed, squinting
t0, t1 = span('A11')
scene('A11', t0, t1, 'parisStreet',
    actors=[act('flic', [3.9, 0, 31.3], 204, 'armsCrossed', 'suspicious', keys=talk('L10', t0, 'suspicious'))],
    props=[P('gate', 'barrierGate', pos=CHK, rot=[0, 3.1416, 0], opts={'length': 5.0, 'angle': 0, 'sign': 'FRONTIÈRE'})],
    cams=[cam(0.0, [2.75, 1.45, 28.6], [2.85, 1.48, 28.85], [3.9, 1.65, 31.3], [3.9, 1.67, 31.3], lens=42)])

# A12 "On l'expulse.": the stamp slams EXPULSÉ onto the cloud's file (impact shake, the mark pops)
t0, t1 = span('A12')
hit = 0.28
scene('A12', t0, t1, 'office',
    props=[P('file', 'noticeBoard', pos=[0, 0.8, 0], rot=[-1.5708, 0, 0], opts={'text': 'FICHE\nNUAGE GRIS\nORIGINE : BELGIQUE', 'style': 'doc', 'w': 0.6, 'h': 0.8, 'textSize': 0.5}),
           P('mark', 'noticeBoard', pos=[0.06, 0.806, 0.12], rot=[-1.5708, 0, 0.2], opts={'text': 'EXPULSÉ', 'style': 'sign', 'w': 0.42, 'h': 0.14, 'fg': '#C8322A', 'frame': '#C8322A', 'popAt': hit, 'popDur': 0.18, 'textSize': 0.8}),
           P('stamp', 'rubberStamp', pos=[0.06, 1.25, 0.12], scale=1.5, keys=[k(0.0, to=[0.06, 0.82, 0.12], dur=hit, ease='in'), k(hit + 0.04, to=[0.06, 1.1, 0.12], dur=0.3, ease='out')])],
    cams=[cam(0.0, [0.05, 1.85, 0.85], [0.05, 1.8, 0.8], [0.05, 0.8, 0.02], [0.05, 0.8, 0.02], lens=42),
          cam(hit, [0.05, 1.8, 0.8], [0.05, 1.78, 0.76], [0.05, 0.8, 0.02], [0.05, 0.8, 0.02], lens=42, shake=0.06)],
    blur=[[0.15, hit + 0.02, 0.01]], blurSamples=6)

# A13 "Ils l'ont menotté à un avion.": on the runway, the cloud cuffed to the airliner's wing; low angle
t0, t1 = span('A13')
scene('A13', t0, t1, 'runway',
    actors=[act('flic', [3.6, 0, 1.4], 40, 'walk', 'smug', keys=[k(0.0, to=[4.9, 0, 3.0], dur=round(dur('A13'), 3), clip='walk')])],
    props=[P('plane', 'plane', pos=[0, 2.2, -6], rot=[0, 0.35, 0], opts={'livery': '#2F62B5'}),
           P('cuffs', 'bigCuffs', pos=[1.98, 1.45, 0.4], rot=[1.5708, 0, 0.35], scale=0.28),
           P('cloud', 'cloudChar', pos=[2.05, 0.3, 0.55], opts={**GREY, 'face': 'grumpy'}, scale=0.8)],
    cams=[cam(0.0, [8.2, 1.0, 6.8], [7.8, 1.05, 6.4], [1.2, 1.5, -1.5], [1.2, 1.55, -1.5], lens=40)])

# A14 "Le vent l'a ramené avant le décollage.": the plane rolls, a gust rips the cloud off and hurls it home past the lens (whip)
t0, t1 = span('A14')
d14 = dur('A14')
scene('A14', t0, t1, 'runway',
    props=[P('plane', 'plane', pos=[0, 2.2, -6], rot=[0, 0.35, 0], opts={'livery': '#2F62B5'}, keys=[k(0.0, to=[14, 2.2, -11], dur=round(d14, 3), ease='in')]),
           P('cloud', 'cloudChar', pos=[2.05, 0.3, 0.55], opts={**GREY, 'expr': [[0, 'grumpy'], [0.55, 'happy']]}, scale=0.8,
             keys=[k(0.0, to=[2.3, 0.45, 0.75], dur=0.5, ease='linear'), k(0.6, to=[-3, 3.5, 9], dur=round(d14 - 0.65, 3), ease='in')]),
           P('streaks', 'speedLines', pos=[6, 1.6, 0], rot=[0, -0.9, 0], scale=2.0, visible=False, keys=[k(0.45, visible=True)])],
    cams=[cam(0.0, [9.5, 1.3, 5.0], [9.0, 1.3, 5.0], [2.5, 1.8, -3], [2.5, 1.8, -3], lens=38),
          cam(0.6, [9.0, 1.3, 5.0], [8.4, 1.4, 5.4], [2.5, 1.8, -3], [-1.5, 3.0, 8.5], lens=38, ease='in')],
    blur=[[0.6, d14, 0.014]], blurSamples=8)

# A15 "Complicité.": the cop points after it, furious
t0, t1 = span('A15')
scene('A15', t0, t1, 'runway',
    actors=[act('flic', [0, 0, 0], 20, 'point', 'angry', keys=talk('L13', t0, 'angry'))],
    cams=[cam(0.0, [-1.4, 0.9, 2.3], [-1.3, 0.92, 2.1], [0.1, 1.7, 0], [0.1, 1.72, 0], lens=44, shake=0.015)])

# A16 "Ils ont arrêté le vent.": two cops close giant cuffs round a knot of spinning wind (push-in)
t0, t1 = span('A16')
scene('A16', t0, t1, 'parisStreet',
    actors=[act('flic', [6.15, 0, 24.0], 75, 'cuffOther', 'angry'), act('flic2', [7.85, 0, 24.0], -75, 'cuffOther', 'suspicious')],
    props=[P('wind', 'windSwirl', pos=[7.0, 0.35, 24.0], scale=1.0),
           P('cuffs', 'bigCuffs', pos=[7.0, 1.2, 24.3], scale=0.12, keys=[k(0.35, scale=0.3, dur=0.3, ease='outBack')])],
    cams=[cam(0.0, [6.9, 1.45, 30.0], [6.95, 1.4, 28.8], [7.0, 1.15, 24.0], [7.0, 1.15, 24.0], lens=42)])

# A17 "Sauf qu'il avait fait le tour du monde.": space, the Earth turning, the wind's streak looping round it
t0, t1 = span('A17')
scene('A17', t0, t1, 'spaceDark',
    props=[P('earth', 'earthGlobe', pos=[0, 0, 0], opts={'radius': 3, 'spin': 0.3}),
           P('trail', 'orbitTrail', pos=[0, 3, 0], opts={'r': 3.7, 'speed': 1.25, 'tilt': 0.32})],
    cams=[cam(0.0, [0.8, 3.9, 19.5], [0.5, 3.6, 17.0], [0, 3, 0], [0, 3, 0], lens=40)])

# A18 "Tout cet air est étranger !": from the ground, the cop throws his arms at the whole sky
t0, t1 = span('A18')
scene('A18', t0, t1, 'parisStreet',
    actors=[act('flic', [6.4, 0, 30.9], -40, 'armsUp', 'angry', keys=talk('L16', t0, 'angry'))],
    props=[P('c1', 'cloudChar', pos=[3.0, 9.5, 24.0], opts={**WHITE, 'seed': 4}, scale=1.4), P('c2', 'cloudChar', pos=[10.5, 11.0, 23.0], opts={**WHITE, 'seed': 7}, scale=1.2)],
    cams=[cam(0.0, [5.6, 0.35, 33.4], [5.7, 0.38, 33.1], [6.3, 3.4, 29.8], [6.3, 3.6, 29.8], lens=44)])

# A19 "Alors ils ont mis l'atmosphère en garde à vue.": the Earth in a cell of bars in space, slow orbit (GARDE À VUE card)
t0, t1 = span('A19')
scene('A19', t0, t1, 'spaceDark',
    props=[P('earth', 'earthGlobe', pos=[0, 0, 0], opts={'radius': 2.2, 'spin': 0.25}),
           P('bars', 'jailBars', pos=[0, -0.3, 2.9], opts={'width': 6.0, 'height': 5.0}),
           P('bars2', 'jailBars', pos=[3.0, -0.3, 0], rot=[0, 1.5708, 0], opts={'width': 6.0, 'height': 5.0}),
           P('bars3', 'jailBars', pos=[-3.0, -0.3, 0], rot=[0, 1.5708, 0], opts={'width': 6.0, 'height': 5.0})],
    cams=[cam(0.0, [3.5, 3.0, 10.5], [-1.5, 2.8, 10.8], [0, 2.2, 0], [0, 2.2, 0], lens=40)])

# A20 "Le flic a respiré.": the cop takes a huge breath: he swells (scale pop) and holds it, cheeks tight
t0, t1 = span('A20')
scene('A20', t0, t1, 'parisStreet',
    actors=[act('flic', [6.4, 0, 30.9], -40, 'stand', 'neutral', keys=[k(0.15, expr='surprised'), k(0.2, scale=1.12, dur=0.45, ease='outBack'), k(0.75, expr='grimace')])],
    cams=[cam(0.0, [5.75, 1.9, 33.3], [5.8, 1.9, 33.0], [6.35, 1.85, 30.9], [6.35, 1.88, 30.9], lens=42)])

# A21 "Putain, t'en caches dans tes poumons !": a colleague jabs his chest and yells; he is still puffed up
t0, t1 = span('A21')
scene('A21', t0, t1, 'parisStreet',
    actors=[act('flic', [6.4, 0, 30.9], -40, 'stand', 'grimace', scale=1.12),
            act('flic2', [5.5, 0, 31.5], 125, 'pokeFinger', 'angry', keys=talk('L19', t0, 'angry'))],
    cams=[cam(0.0, [7.3, 1.55, 35.4], [7.15, 1.55, 35.0], [5.95, 1.55, 31.2], [5.95, 1.57, 31.2], lens=40, shake=0.012)])

# A22 "Ses collègues l'ont coffré": two colleagues cuff him from both sides, push-in
t0, t1 = span('A22')
scene('A22', t0, t1, 'parisStreet',
    actors=[act('flic', [6.4, 0, 30.9], -10, 'cuffedBack', 'shocked'),
            act('flic2', [5.5, 0, 30.5], 60, 'cuffOther', 'angry'), act('flic3', [7.3, 0, 30.4], -80, 'cuffOther', 'suspicious')],
    cams=[cam(0.0, [6.1, 1.35, 35.2], [6.2, 1.4, 34.0], [6.4, 1.3, 30.8], [6.4, 1.35, 30.8], lens=42)])

# A23 "pour hébergement clandestin.": mugshot against the height chart, placard at his chest
t0, t1 = span('A23')
scene('A23', t0, t1, 'brightCell', setOpts={'bars': False},
    actors=[act('flic', [0, 0, -1.05], 0, 'stand', 'sad')],
    props=[P('wall', 'mugshotBoard', pos=[0, 0, -1.58], opts={'w': 2.4, 'h': 2.4}),
           P('placard', 'placard', pos=[0, 1.22, -0.78], opts={'text': 'HÉBERGEMENT\nCLANDESTIN'}, scale=1.7)],
    cams=[cam(0.0, [0.1, 1.5, 2.6], [0.1, 1.5, 2.45], [0.05, 1.42, -1.05], [0.05, 1.42, -1.05], lens=42, shake=0.01)])

# A24 "Vingt ans ferme.": the bars slam (shake), sign on the cell wall
t0, t1 = span('A24')
scene('A24', t0, t1, 'brightCell', setOpts={'sign': '20 ANS\nFERME'},
    actors=[act('flic', [0.1, 0, -0.4], 0, 'stand', 'sad')],
    cams=[cam(0.0, [0.1, 1.55, 4.4], [0.15, 1.55, 4.3], [0.35, 1.45, -0.8], [0.35, 1.45, -0.8], lens=46, shake=0.05),
          cam(0.25, [0.15, 1.55, 4.3], [0.2, 1.55, 4.15], [0.35, 1.45, -0.8], [0.35, 1.45, -0.8], lens=46)])

# A25 "Le nuage a racheté la prison.": outside the prison, the grey cloud hovers over the roof, VENDU pops on the wall
t0, t1 = span('A25')
scene('A25', t0, t1, 'grassland',
    props=[P('prison', 'prisonFront', pos=[0, 0, -8], opts={'sold': [[0.55, True]]}),
           P('cloud', 'cloudChar', pos=[1.5, 10.5, -6.5], opts={**GREY, 'face': 'smug'}, scale=1.8)],
    cams=[cam(0.0, [-6.5, 1.0, 12.5], [-5.8, 1.1, 11.8], [0, 6.0, -7], [0, 6.1, -7], lens=42)])

# A26 "Maintenant, il pleut dans sa cellule.": the cop on his bunk, a small cloud raining on him under the ceiling
t0, t1 = span('A26')
scene('A26', t0, t1, 'brightCell', setOpts={'sign': '20 ANS\nFERME'},
    actors=[act('flic', [-1.05, 0, -0.4], 90, 'sit', 'unimpressed', keys=[k(0.0, to=[-1.05, 0.13, -0.4], dur=0.01)])],
    props=[P('cloud', 'cloudChar', pos=[-1.0, 2.05, -0.4], opts={**GREY, 'face': 'smug', 'raining': True, 'rainH': 1.5, 'drops': 50}, scale=0.42)],
    cams=[cam(0.0, [0.9, 1.9, 4.0], [0.8, 1.85, 3.7], [-0.8, 1.2, -0.4], [-0.8, 1.2, -0.4], lens=44)])

# A27 "Vous n'avez pas le droit !": close through the bars, he grips them and yells
t0, t1 = span('A27')
scene('A27', t0, t1, 'brightCell', setOpts={'sign': '20 ANS\nFERME'},
    actors=[act('flic', [0.0, 0, 1.15], 0, 'pressGlass', 'angry', keys=talk('L24', t0, 'angry'))],
    props=[P('cloud', 'cloudChar', pos=[0.4, 2.1, 0.4], opts={**GREY, 'face': 'smug', 'raining': True, 'rainH': 1.6, 'drops': 50}, scale=0.42)],
    cams=[cam(0.0, [0.05, 1.98, 3.25], [0.05, 1.98, 3.05], [0.0, 1.9, 1.1], [0.0, 1.9, 1.1], lens=44, shake=0.012)])

# A28 "Le nuage a sorti ses papiers.": outside the bars the cloud shows its deed, which pops up at the lens
t0, t1 = span('A28')
scene('A28', t0, t1, 'brightCell', setOpts={'sign': '20 ANS\nFERME'},
    actors=[act('flic', [-0.45, 0, 0.6], 0, 'stand', 'shocked')],
    props=[P('cloud', 'cloudChar', pos=[0.7, 0.9, 2.5], opts={**GREY, 'face': 'smug'}, scale=0.55),
           P('deed', 'noticeBoard', pos=[0.12, 1.42, 2.78], rot=[0, 0, 0], opts={'text': 'ACTE DE PROPRIÉTÉ\nPRISON\nPROPRIÉTAIRE : NUAGE', 'style': 'doc', 'w': 0.6, 'h': 0.76, 'popAt': 0.35, 'textSize': 0.42, 'stamp': 'VALIDÉ'})],
    cams=[cam(0.0, [0.2, 1.5, 4.62], [0.2, 1.48, 4.42], [0.18, 1.36, 2.4], [0.18, 1.36, 2.4], lens=46)])

# A29 "Le flic était chez lui.": wide from the corridor: the landlord cloud smug outside, the cop small behind the bars
t0, t1 = span('A29')
scene('A29', t0, t1, 'brightCell', setOpts={'sign': '20 ANS\nFERME'},
    actors=[act('flic', [0.2, 0, 0.3], 0, 'handsOnHips', 'unimpressed')],
    props=[P('cloud', 'cloudChar', pos=[-0.75, 1.45, 2.2], opts={**GREY, 'face': 'smug'}, scale=0.5)],
    cams=[cam(0.0, [-0.05, 1.75, 4.6], [-0.05, 1.72, 4.4], [0.0, 1.3, 0.6], [0.0, 1.3, 0.6], lens=46)])

# A30 "Et la douche était en supplément.": the cloud rains on him; the price tag DOUCHE : 50 € pops on the wall; hold to the end
t0, t1 = span('A30')
scene('A30', t0, t1, 'brightCell', setOpts={'sign': '20 ANS\nFERME'},
    actors=[act('flic', [-0.1, 0, -0.3], 0, 'stand', 'unimpressed', keys=[k(0.9, expr='sad')])],
    props=[P('cloud', 'cloudChar', pos=[-0.1, 2.15, -0.3], opts={**GREY, 'face': 'smug', 'raining': True, 'rainH': 1.7, 'drops': 60}, scale=0.45),
           P('price', 'noticeBoard', pos=[-0.78, 1.72, -1.55], opts={'text': 'DOUCHE\n50 €', 'style': 'tag', 'w': 0.62, 'h': 0.5, 'popAt': 0.7, 'tilt': -0.08, 'textSize': 0.7})],
    cams=[cam(0.0, [0.25, 1.6, 4.4], [0.22, 1.58, 4.1], [0.2, 1.45, -0.6], [0.2, 1.45, -0.6], lens=46)])

for sc_ in scenes:
    for p_ in sc_['props']:
        if 'rot' in p_ and 'ry' not in p_:
            p_['ry'] = round(math.degrees(p_['rot'][1]), 3)

# grade and softness in the replica's range (outdoor day, interiors a touch brighter, space crisper); soften is in output px (1080 wide)
OUT_W = 1080; SOFT = 0.45 * OUT_W / 576
for sc_ in scenes:
    s = sc_['set']
    sc_['grade'] = {'spaceDark': 'contrast(0.95) saturate(1.1) brightness(1.02)', 'brightCell': 'contrast(0.9) saturate(1.05) brightness(1.1)',
                    'office': 'contrast(0.9) saturate(1.05) brightness(1.1)', 'interrogation': 'contrast(0.9) saturate(1.05) brightness(1.12)'}.get(s, 'contrast(0.9) saturate(1.08) brightness(1.08)')
    sc_['soften'] = round(SOFT * (0.7 if s == 'spaceDark' else 1.0), 2)

doc = {'version': 3, 'title': 'Vos papiers (tornado style)', 'grade': 'contrast(0.9) saturate(1.05) brightness(1.06)', 'captionWords': 0, 'captionY': 0.81, 'tempo': 1.0,
       'voice': None, 'music': None,
       'cast': {'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
                'flic': {'preset': 'cop', 'suit': '#1E2D4A', 'pants': '#1E2D4A', 'facial': 'none', 'atlas': 'lemec', 'atlasBody': False, 'build': {'width': 0.82, 'headWidth': 1.3}},
                'flic2': {'preset': 'cop', 'suit': '#1E2D4A', 'pants': '#1E2D4A', 'facial': 'mustache', 'hair': 'receding', 'seed': 41, 'build': {'width': 0.86, 'headWidth': 1.3, 'belly': 0.08}},
                'flic3': {'preset': 'cop', 'suit': '#1E2D4A', 'pants': '#1E2D4A', 'facial': 'stubble', 'hair': 'crew', 'seed': 77, 'build': {'width': 0.82, 'headWidth': 1.3}}},
       'scenes': scenes, 'total': TOTAL}
out = os.path.join(HERE, 'vospapiers_tornado.json')
json.dump(doc, open(out, 'w'), indent=1, ensure_ascii=False)
print(out, len(scenes), 'scenes', TOTAL, 's')
for sid, (a, b) in SH.items(): print(f'{sid} {a:6.3f}-{b:6.3f} ({b - a:4.2f}s)', end='  |  ' if int(sid[1:]) % 3 else '\n')
