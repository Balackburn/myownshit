#!/usr/bin/env python3
"""L'éternuement (story 38, cycle 2 of the cartoon staging): this man sneezed and blew the whole town's hair about. The weather office
measured it: two hundred kilometres an hour. Above a hundred it is a storm, and a storm must have a first name: the next one on the
list was Josiane. Since then Josiane is on red alert; when Josiane sniffs, his street is evacuated; his insurer classed him as a natural
disaster. Then the wind turbines hired him: today Josiane lights three towns. He is allergic to pollen. Spring is coming.
Cartoon rig with the cycle 2 additions (fingers, a tie and hair that the wind takes, weight shifts): rig='toon', fingers, cloth, idleShift.
Gags: three breaths that blow him up like a balloon, the blast that pins the passers-by on a hairdresser's poster, the forecaster spun like a
top by her anemometer, the badge, the crowd that bends away, the street that empties on a sniff, the stamp that drives his head into his
shoulders, the sneeze that lights three towns, the grain of pollen he squints at. Natural look."""
from story_kit import *

st = Story('eternuement', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4), ('S03', 'L01', 8), ('S04', 'L02', 0), ('S05', 'L03', 0), ('S06', 'L04', 0), ('S07', 'L05', 0), ('S08', 'L06', 0), ('S09', 'L06', 5),
         ('S10', 'L07', 0), ('S11', 'L07', 2), ('S12', 'L08', 0), ('S13', 'L08', 3), ('S14', 'L09', 0), ('S15', 'L10', 0), ('S16', 'L11', 0), ('S17', 'L11', 2), ('S18', 'L12', 0), ('S19', 'L12', 5)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}   # a camera key that glides from the previous one instead of cutting
MX, MZ = 7.0, 0.0                                   # the man, on the right-hand pavement, facing down the street (+Z)
PX, PZ = 8.3, 4.6                                   # the advertising panel across the pavement, facing him
STREET = {'clear': [-45, 30], 'eiffelX': -30}
PANEL = P('panel', 'adPanel', pos=[PX, 0, PZ], ry=180, opts={'w': 2.9, 'h': 2.4, 'y0': 0.45})
WALKERS = [('p1', 7.65, 1.9, 0.06), ('p2', 8.35, 2.7, 0.1), ('p3', 9.0, 3.5, 0.14)]   # who, x, z, when the blast reaches him
HIGH = {'p1': 0.4, 'p2': 0.62, 'p3': 0.48}         # how high each one is pinned on the panel
MESSY = {'hairUp': 0.85}                            # hair left on end
DUST = lambda pid, pos, at_, per=0.7, s=0.7, **kw: P(pid, 'dustPuff', pos=pos, scale=s, opts={'once': True, 'startAt': at_, 'period': per, 'color': '#F6F3EC', **kw}, keys=[k(0.0, visible=False), k(at_, visible=True)])

# 1: he stops in the street: three breaths in, each one bigger; he swells, rises on his toes, off the ground; one finger under his nose
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', [MX, 0, MZ], 0, 'stand', 'worried', keys=[k(0.0, clip='sneezeUp', params={'dur': 1.0, 'float': 0.3}, blend=0.08)])],
        cams=[cam(0.0, [MX - 1.15, 2.3, 3.7], [MX - 1.05, 2.5, 3.4], [MX, 1.85, MZ], [MX, 2.2, MZ], lens=44)])
# 2: the sneeze, from behind him: the blast takes the passers-by off their feet and pins them on the hairdresser's poster; he is shot backward past us
B2 = 0.03
def walker(w, x, z, d, hit):
    return act(w, [x, 0, z + 0.3], 180, 'walk', 'neutral', keys=[k(0.0, to=[x, 0, z], dur=d, clip='walk', ease='linear'), k(d, clip='blownBack', blend=0.04),
        k(d + 0.02, to=[x, 0.0, PZ - 0.16], dur=hit - d - 0.02, glide=True, ease='in', face='keep'), k(hit, clip='poster', params={'high': HIGH[w], 'slideAt': 9.0, 'stars': 1}, blend=0.02, toon=MESSY, toonDur=0.05)])
HITS = {'p1': 0.3, 'p2': 0.36, 'p3': 0.42}
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', [MX, 0.3, MZ], 0, 'sneezeUp', 'worried', params={'dur': 1.0, 'float': 0.0}, keys=[k(B2, clip='sneeze', params={'hold': 0.5}, blend=0.03),
        k(B2 + 0.03, to=[MX - 1.3, 0.6, MZ - 6.0], dur=0.22, glide=True, ease='out', face='keep')])] + [walker(w, x, z, d, HITS[w]) for w, x, z, d in WALKERS],
        props=[PANEL, P('blast', 'sneezeBlast', pos=[MX, 0.2, MZ + 0.4], opts={'at': B2, 'dur': 0.42, 'len': 4.6, 'spread': 1.6})],
        fx=[{'type': 'wind', 'at': B2, 'dur': 0.42, 'v': [0, 0, 30], 'attack': 0.03, 'release': 0.3}, {'type': 'shake', 'at': B2, 'dur': 0.3, 'amount': 0.05}] + [{'type': 'shake', 'at': t, 'dur': 0.1, 'amount': 0.02} for t in HITS.values()],
        cams=[cam(0.0, [MX + 0.7, 2.0, -3.2], [MX + 0.75, 1.95, -2.9], [8.0, 1.3, 3.0], [8.05, 1.35, 3.4], lens=58), glide([cam(0.4, [8.15, 1.75, -0.9], [8.2, 1.75, -1.1], [PX, 1.7, PZ], [PX, 1.7, PZ], lens=50)], 0.3)])
# 3: the hairdresser's poster, and three more: pinned flat, hair on end; one peels off and slides down, then another
SLIDE = {'p2': 0.22, 'p1': 0.5}
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act(w, [x, 0, PZ - 0.16], 180, 'stand', 'dizzy',
        keys=[k(-0.05, clip='poster', params={'high': HIGH[w], 'slideAt': SLIDE.get(w, 9.0) + 0.05, 'slide': 1.2, 'stars': 1}, blend=0.001, toon=MESSY, toonDur=0)]) for w, x, z, d in WALKERS],
        props=[PANEL], cams=[cam(0.0, [PX + 0.2, 1.6, PZ - 5.9], [PX + 0.15, 1.6, PZ - 5.5], [PX, 1.85, PZ], [PX, 1.75, PZ], lens=44)])
# ---- the weather office (the town-hall set with its own banner): everybody's hair stays on end from now on
OFFICE = lambda bx, **kw: {'title': 'MÉTÉO', 'map': False, 'plate': False, 'bannerX': bx, 'bannerY': 2.95, 'flagX': 4.3, 'clockX': 4.6, **kw}
FX, FZ = -1.7, 0.1                                  # the forecaster, left of the desk
# 4: the forecaster holds up her anemometer: the gust arrives, the cups blur, and it is she who turns: three turns, like a top
G4 = 0.22
st.shot('S04', 'mairie', setOpts=OFFICE(FX), actors=[act('meteo', [FX, 0, FZ], 0, 'raiseOverhead', 'proud', keys=[k(0.0, look=[FX - 0.4, 2.9, 0.6]), k(G4, look=None, expr='surprised'),
        k(G4 + 0.06, clip='spinTop', params={'turns': [[0, 0], [0.2, 5], [0.575, 5], [0.825, 0]]}, blend=0.06, toon=MESSY, toonDur=0.15), k(G4 + 0.95, expr='dizzy')])],
        props=[P('anemo', 'anemometer', on={'actor': 'meteo', 'hand': 'R', 'offset': [0, -0.1, 0], 'rot': [3.1416, 0, 0]}, opts={'spin': [[0, 0.7], [G4, 0.9], [G4 + 0.08, 15], [G4 + 0.7, 15], [G4 + 1.0, 2]]}),
               P('gust', 'sneezeBlast', pos=[FX - 3.6, 0.35, FZ - 0.5], ry=90, opts={'at': G4 - 0.05, 'dur': 0.75, 'len': 7.5, 'spread': 1.7, 'n': 30, 'puff': 0.45}),
               P('pp1', 'flyingPaper', pos=[FX - 2.8, 1.2, FZ + 0.7], keys=[k(0.0, visible=False), k(G4, visible=True), k(G4, to=[FX + 2.8, 2.3, FZ + 0.9], dur=0.5, arc=0.5, ease='linear')]),
               P('pp2', 'flyingPaper', pos=[FX - 2.8, 2.2, FZ - 0.9], keys=[k(0.0, visible=False), k(G4 + 0.15, visible=True), k(G4 + 0.15, to=[FX + 2.8, 1.5, FZ - 0.7], dur=0.55, arc=0.4, ease='linear')])],
        fx=[{'type': 'wind', 'at': G4, 'dur': 0.7, 'v': [16, 0, 0], 'attack': 0.05, 'release': 0.3}, {'type': 'shake', 'at': G4, 'dur': 0.25, 'amount': 0.02}],
        cams=[cam(0.0, [FX + 0.35, 1.75, 4.7], [FX + 0.3, 1.75, 4.4], [FX, 1.6, FZ], [FX, 1.6, FZ], lens=44)])
# 5: the gauge: the needle slams against the stop; dizzy, hair on end, she reads it out
st.shot('S05', 'mairie', setOpts=OFFICE(FX), actors=[act('meteo', [FX, 0, FZ], 0, 'stand', 'dizzy', keys=[k(0.0, toon=MESSY, toonDur=0), k(-0.05, clip='jelly', params={'amp': 0.12, 'freq': 9, 'decay': 1.5}, blend=0.001)] + st.talk('L03', 'S05', 'dizzy'))],
        props=[P('anemo', 'anemometer', on={'actor': 'meteo', 'hand': 'R', 'offset': [0, -0.1, 0], 'rot': [3.1416, 0, 0]}, opts={'spin': [[0, 2.5], [1.2, 0.3]]}),
               P('gauge', 'windGauge', pos=[FX + 0.66, 2.3, FZ + 0.25], rot=[0.03, -0.1, 0.04], scale=0.01, opts={'at': 0.14, 'value': 200, 'r': 0.31}, keys=[k(0.02, scale=1.0, dur=0.16, ease='outBack')])],
        fx=[{'type': 'shake', 'at': 0.14, 'dur': 0.2, 'amount': 0.018}],
        cams=[cam(0.0, [FX + 0.5, 1.95, 3.5], [FX + 0.47, 1.97, 3.3], [FX + 0.32, 2.0, FZ], [FX + 0.32, 2.0, FZ], lens=44)])
# 6: the rule: above a hundred, it is a storm. The chief shows the scale; his finger pushes the rider up to the red band
BX = -0.5                                           # the boards on the back wall
CX, CZ = 0.5, -1.7                                  # the chief beside them
T6 = st.at('S06', 'L04', 5)
st.shot('S06', 'mairie', setOpts=OFFICE(4.6), actors=[act('chef', [CX, 0, CZ], -50, 'point', 'determined', keys=[k(0.0, toon={**MESSY, 'hands': {'R': 'point'}}, toonDur=0), k(T6 - 0.2, clip='raiseOverhead', expr='proud', blend=0.18),
        k(T6 + 0.3, clip='handsOnHips', face=15, blend=0.2, toon=MESSY, toonDur=0.1)])],
        props=[P('scale', 'windScale', pos=[BX, 1.95, -2.52], opts={'at': T6 - 0.12, 'w': 1.15, 'h': 1.6})],
        cams=[cam(0.0, [0.25, 1.85, 2.5], [0.2, 1.9, 2.0], [0.05, 1.85, -2.2], [0.0, 1.9, -2.2], lens=44)])
# 7: and a storm has a first name: he pulls the list down beside him
T7 = st.at('S07', 'L05', 6)
LIST = lambda at_, **kw: P('list', 'nameList', opts={'at': at_, 'w': 1.0, 'h': 1.7}, **kw)
P7 = round(T7 - 0.42, 3)                            # he pulls the cord
st.shot('S07', 'mairie', setOpts=OFFICE(4.6), actors=[act('chef', [CX, 0, CZ + 0.1], 10, 'oneHandHip', 'proud', keys=[k(0.0, toon={**MESSY, 'hands': {'R': 'point'}}, toonDur=0), k(P7 - 0.3, clip='reachUpL', expr='determined', blend=0.14),
        k(P7, clip='windUp', blend=0.08), k(P7 + 0.3, clip='point', expr='proud', face=-55, blend=0.15, toon={**MESSY, 'hands': {'R': 'point'}}, toonDur=0.1)])],
        props=[LIST(9.0, pos=[BX, 4.7, -2.52], keys=[k(P7 + 0.02, to=[BX, 2.0, -2.52], dur=0.26, ease='outBack')])],
        fx=[{'type': 'shake', 'at': P7 + 0.26, 'dur': 0.12, 'amount': 0.014}],
        cams=[cam(0.0, [0.25, 1.85, 2.4], [0.18, 1.9, 1.9], [0.05, 1.9, -2.2], [-0.05, 1.95, -2.2], lens=44)])
# 8: the next one on the list: his finger goes down the struck names
T8 = st.dur('S08')
st.shot('S08', 'mairie', setOpts=OFFICE(4.6), props=[LIST(T8 - 0.22, pos=[BX, 2.0, -2.52]),
        P('hand', 'pointerHand', pos=[BX + 0.27, 2.5, -2.42], keys=[k(0.05, to=[BX + 0.27, 1.5, -2.42], dur=T8 - 0.4, ease='inOut'), k(T8 - 0.3, to=[BX + 0.3, 1.36, -2.42], dur=0.12, ease='out')])],
        cams=[cam(0.0, [-0.35, 2.0, -0.3], [-0.37, 1.7, -0.5], [-0.42, 2.1, -2.5], [-0.42, 1.6, -2.5], lens=44)])
# 9: Josiane. The badge on his chest; he looks at it, then at us
B9 = 0.3
st.shot('S09', 'mairie', setOpts=OFFICE(0.2), actors=[act('mec', [0.2, 0, 0.3], 0, 'stand', 'worried', keys=[k(B9, clip='jelly', params={'amp': 0.3}, expr='surprised', blend=0.03), k(B9 + 0.25, look=[0.2, 1.3, 0.8], expr='lookDown'), k(B9 + 0.55, look=None, expr='deadpan')]),
        act('chef', [1.05, 0, 0.55], -75, 'stand', 'proud', keys=[k(0.0, toon=MESSY, toonDur=0), k(0.05, clip='point', blend=0.12), k(B9 + 0.1, clip='handsOnHips', blend=0.2)])],
        props=[P('badge', 'nameBadge', pos=[0.95, 1.45, 0.75], rot=[0, -1.2, 0], scale=1.0, keys=[k(B9 - 0.12, to=[0.14, 1.52, 0.46], dur=0.12, ease='in'), k(B9 - 0.12, rotTo=[0, 0, -0.06], dur=0.12), k(B9, attach='mec', joint='torso', offset=[-0.06, 0.47, 0.19], rot=[0, 0, -0.06])])],
        fx=[{'type': 'shake', 'at': B9, 'dur': 0.15, 'amount': 0.02}],
        cams=[cam(0.0, [0.5, 1.6, 3.3], [0.45, 1.62, 2.9], [0.3, 1.55, 0.3], [0.28, 1.6, 0.3], lens=44)])
# 10: the weather report: the storm on the map has his name; the forecaster, hair on end, reaches up: her arm goes out like a telescopic pointer to tap it
st.shot('S10', 'mairie', setOpts=OFFICE(4.6), actors=[act('meteo', [-0.85, 0, -1.5], 15, 'stand', 'happy', keys=[k(0.0, toon=MESSY, toonDur=0), k(0.12, clip='reachUpL', expr='proud', blend=0.12, look=[0.1, 2.5, -2.4]),
        k(0.28, toon={**MESSY, 'hands': {'L': 'point'}, 'bend': {'armL': [0, -0.5, 0, 1.5, 0.9], 'foreL': [0, -0.35, 0, 2.0, 0.9], 'spine': [0, -0.12, 0, 1, None]}}, toonDur=0.1, toonEase='outBack')])],
        props=[P('map', 'stormMap', pos=[0.1, 2.45, -2.5], opts={'w': 1.5, 'h': 1.9})],
        cams=[cam(0.0, [-0.3, 1.5, 3.4], [-0.28, 1.55, 3.0], [-0.3, 2.0, -2.0], [-0.28, 2.02, -2.0], lens=44)])
# 11: red alert: he walks down the street, a beacon turning on his head; the passers-by bend away from him one after the other, like wheat
SIDE11 = [('p1', MX - 0.72, 1.0, 1), ('p2', MX + 0.72, 0.0, -1), ('p3', MX - 0.72, -1.0, 1)]   # who, x, z, which way he bends (away from the middle)
V11 = 2.3                                           # his speed (m/s): he starts at z = -2.6
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[act('mec', [MX, 0, -2.6], 0, 'walk', 'worried', keys=[k(0.0, to=[MX, 0, -2.6 + V11 * st.dur('S11')], dur=st.dur('S11'), clip='walk', ease='linear')])] +
        [act(w, [x, 0, z], 90 * sd, 'stand', 'neutral', keys=[k(0.0, toon=MESSY, toonDur=0), k(0.0, look='mec'), k(round((z + 2.6 - 0.9) / V11, 3), clip='leanAway', params={'side': -sd, 'ph': i}, expr='scared', toon=MESSY, toonDur=0.05)]) for i, (w, x, z, sd) in enumerate(SIDE11)],
        props=[P('beacon', 'beacon', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.3, 0], 'rot': [0, 0, 0]}, opts={'r': 0.1}), P('badge', 'nameBadge', on={'actor': 'mec', 'joint': 'torso', 'offset': [-0.06, 0.47, 0.19], 'rot': [0, 0, -0.06]}),
               ],
        cams=[cam(0.0, [MX + 0.2, 1.7, 6.4], [MX + 0.15, 1.7, 6.0], [MX, 1.25, 0.0], [MX, 1.25, 0.3], lens=44)])
# 12: when Josiane sniffs: close on him: the nose goes up, twice; behind him three faces freeze, eyes wide
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[act('mec', [MX, 0, 0.6], 0, 'stand', 'worried', keys=[k(0.25, clip='sniff', params={'n': 2}, blend=0.06)])] +
        [act(w, [MX + dx, 0, -0.9 + dz], 0, 'stand', 'neutral', keys=[k(0.0, toon=MESSY, toonDur=0), k(0.0, look='mec'), k(0.3 + 0.05 * i, clip='startle', expr='scared', blend=0.05),
            k(0.3 + 0.05 * i, toon={**MESSY, 'face': {'pop': 0.5, 'popLen': 0.08, 'eyeScale': 1.2}}, toonDur=0.08, toonEase='outBack')]) for i, (w, dx, dz) in enumerate([('p1', -0.85, 0.0), ('p2', 0.8, -0.3), ('p3', -0.1, -0.9)])],
        props=[P('beacon', 'beacon', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.3, 0], 'rot': [0, 0, 0]}, opts={'r': 0.1}), P('badge', 'nameBadge', on={'actor': 'mec', 'joint': 'torso', 'offset': [-0.06, 0.47, 0.19], 'rot': [0, 0, -0.06]})],
        cams=[cam(0.0, [MX + 0.3, 1.75, 3.4], [MX + 0.25, 1.75, 3.0], [MX, 1.68, 0.3], [MX, 1.7, 0.3], lens=44)])
# 13: the street is evacuated: their legs spin on the spot, then they are gone, one after the other (a wig stays in the air, then follows); sandbags pop up
#     round him; he is alone, his finger under his nose
RUN13 = [('p1', MX - 0.85, -0.3, [MX - 9, 0, -3.0], 0.0), ('p2', MX + 0.8, -0.6, [MX + 6, 0, -9.0], 0.07), ('p3', MX - 0.1, -1.2, [MX - 2, 0, -14.0], 0.14)]
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[act('mec', [MX, 0, 0.6], 0, 'sniff', 'worried', params={'n': 2}, keys=[k(0.75, expr='deadpan', look=[MX + 0.4, 1.6, 6.0])])] +
        [act(w, [x, 0, z], 0, 'startle', 'scared', keys=[k(0.0, toon=MESSY, toonDur=0), k(d, clip='scramble', params={'dur': 0.3, 'expr': 'scared'}, blend=0.04, face=(-110 if to[0] < x else 110)),
            k(d + 0.3, to=to, dur=0.16, clip='dashOff', ease='in', blend=0.03), k(d + 0.47, visible=False)]) for w, x, z, to, d in RUN13],
        props=[P('beacon', 'beacon', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.3, 0], 'rot': [0, 0, 0]}, opts={'r': 0.1}), P('badge', 'nameBadge', on={'actor': 'mec', 'joint': 'torso', 'offset': [-0.06, 0.47, 0.19], 'rot': [0, 0, -0.06]}),
               P('wig', 'wig', pos=[MX - 0.85, 1.95, -0.3], keys=[k(0.0, visible=False), k(0.3, visible=True), k(0.62, to=[MX - 0.85, 0.02, -0.3], dur=0.2, ease='in')]),
               DUST('d13a', [MX - 1.6, 0.05, -0.5], 0.32, 0.6, 0.8), DUST('d13b', [MX + 1.4, 0.05, -1.2], 0.39, 0.6, 0.8), DUST('d13c', [MX - 0.3, 0.05, -2.2], 0.46, 0.6, 0.8),
               P('bags1', 'sandbags', pos=[MX - 0.05, 0, 1.45], scale=0.01, opts={'n': 4, 'rows': 2}, keys=[k(0.7, scale=1.0, dur=0.14, ease='outBack')]),
               P('bags2', 'sandbags', pos=[MX - 1.05, 0, 0.75], ry=70, scale=0.01, opts={'n': 3, 'rows': 2, 'seed': 7}, keys=[k(0.78, scale=1.0, dur=0.14, ease='outBack')]),
               P('bags3', 'sandbags', pos=[MX + 0.95, 0, 0.75], ry=-70, scale=0.01, opts={'n': 3, 'rows': 2, 'seed': 9}, keys=[k(0.86, scale=1.0, dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [MX + 0.5, 2.3, 6.4], [MX + 0.45, 2.35, 6.0], [MX, 1.1, -0.3], [MX, 1.1, -0.3], lens=44)])
# 14: his insurer: a very big stamp, raised with both feet off the floor, comes down on his head: the head is driven into his shoulders; CAT. NAT. on his
#     forehead; the certificate drops onto the wall
HIT14 = round(st.at('S14', 'L09', 3) + 0.1, 3)     # on « classé »
T14 = st.at('S14', 'L09', 4)                        # « catastrophe »
st.shot('S14', 'mairie', setOpts=OFFICE(4.6, title='ASSURANCE'), actors=[act('mec', [0.3, 0, 0.4], -8, 'stand', 'worried', keys=[k(0.0, look='assureur'), k(HIT14 - 0.3, expr='scared', look=[-0.3, 2.9, 0.5]),
            k(HIT14 - 0.02, clip='headHammer', params={'at': 0.02}, blend=0.02, look=None), k(HIT14 + 0.5, expr='dizzy'), k(HIT14 + 0.5, toon={'face': {'cross': 1}}, toonDur=0.1), k(T14 + 0.5, toon={}, toonDur=0.15), k(T14 + 0.55, expr='deadpan', look=[0.3, 1.6, 6.0])]),
        act('assureur', [-0.55, 0, 0.5], 82, 'stand', 'smug', keys=[k(HIT14 - 0.55, clip='stampDown', params={'hit': 0.55}, expr='determined', blend=0.08),
            k(HIT14 - 0.07, toon={'bend': {'armR': [0, 0, 0, 1.3, None], 'foreR': [0, 0, 0, 1.3, None]}}, toonDur=0.066, toonEase='in'), k(HIT14 + 0.25, toon={}, toonDur=0.15), k(HIT14 + 0.3, clip='handsOnHips', expr='proud', blend=0.2)])],
        props=[P('stamp', 'bigStamp', on={'actor': 'assureur', 'hand': 'R', 'offset': [0, -0.1, 0.0], 'rot': [2.33, 0, 0]}, keys=[k(HIT14 + 0.3, visible=False)]),
               P('mark', 'stampMark', pos=[0, 0, 0], opts={'w': 0.2, 'h': 0.11}, keys=[k(0.0, visible=False), k(HIT14 + 0.02, visible=True), k(HIT14 + 0.02, attach='mec', joint='head', offset=[0.0, 0.245, 0.128], rot=[0, 0, -0.12])]),
               P('diploma', 'catNatDiploma', pos=[-0.12, 4.6, -2.52], opts={'w': 1.15, 'h': 0.83}, keys=[k(T14 - 0.05, to=[-0.12, 2.25, -2.52], dur=0.2, ease='outBack')])],
        fx=[{'type': 'shake', 'at': HIT14, 'dur': 0.2, 'amount': 0.035}, {'type': 'shake', 'at': T14 + 0.15, 'dur': 0.1, 'amount': 0.012}],
        cams=[cam(0.0, [-0.05, 1.8, 3.9], [-0.08, 1.82, 3.5], [-0.12, 1.75, 0.4], [-0.12, 1.8, 0.4], lens=44)])
# ---- the wind farm: three turbines in a field. For the sneeze he faces the far right corner (ry 135): the turbines up there, three towns on the ridge beyond
FIELD = lambda **kw: {'clouds': 14, 'seed': 31, **kw}
TPOS = [(5.6, -7.2), (10.6, -9.2), (13.2, -15.2)]
TURB = lambda keys=None, **kw: [P(f'turb{i}', 'windTurbine', pos=[x, 0, z], ry=-45, opts={'h': 9, 'rpm': 0, 'phase': i * 0.7, **({'rpmKeys': keys(i)} if keys else {}), **kw}) for i, (x, z) in enumerate(TPOS)]
MAT = lambda **kw: P('mat', 'mattressWall', pos=[-1.4, 0, 1.4], ry=-45, opts={'n': 3, 'h': 1.15, **kw})
# 15: hired: the engineer shakes his hand so hard that the shake runs up his arm and through him like a wave; a thumb up
S15E = 1.15                                         # the shaking stops
st.shot('S15', 'grassland', setOpts=FIELD(), actors=[act('mec', [-0.42, 0, 0], 90, 'stand', 'worried', keys=[k(0.0, clip='shakeHands', params={'role': 'wave', 'stopAt': S15E}, blend=0.05), k(S15E + 0.3, clip='stand', expr='dizzy', blend=0.2)]),
        act('inge', [0.42, 0, 0], -90, 'stand', 'bigGrin', keys=[k(0.0, clip='shakeHands', params={'role': 'pump', 'stopAt': S15E, 'thumbAt': S15E + 0.1}, blend=0.05)])],
        props=[P(f'turb{i}', 'windTurbine', pos=[x, 0, z], opts={'h': 9, 'rpm': 0, 'phase': i * 0.7}) for i, (x, z) in enumerate([(-3.0, -13.0), (2.6, -19.0), (5.2, -27.0)])] +
              [P('badge', 'nameBadge', on={'actor': 'mec', 'joint': 'torso', 'offset': [-0.06, 0.47, 0.19], 'rot': [0, 0, -0.06]}), P('fl1', 'flowers', pos=[-1.4, 0, 1.0]), P('fl2', 'flowers', pos=[1.3, 0, 1.4])],
        cams=[cam(0.0, [0.5, 1.35, 5.2], [0.4, 1.35, 4.8], [0.1, 1.75, 0], [0.05, 1.78, 0], lens=44)])
# 16: at dusk, today: the engineer dangles a pepper pot in front of his nose at the end of a fishing rod: the three breaths again, facing the turbines
DUSK = {'sky': ['#33437A', '#F2A368'], 'grass': '#5E8A4E'}
st.shot('S16', 'grassland', setOpts=FIELD(**DUSK), lighting='dusk', actors=[act('mec', [0, 0, 0], 135, 'stand', 'worried', keys=[k(-0.05, clip='sneezeUp', params={'dur': 1.0, 'float': 0.25}, blend=0.001)]),
        act('inge', [-0.46, 0, -1.13], 22, 'dangleItem', 'bigGrin')],
        props=TURB() + [P('rod', 'pepperRod', pos=[-0.4, 1.95, -0.95], ry=37, opts={'swing': 0.3, 'len': 1.3, 'drop': 0.45}), MAT()],
        cams=[cam(0.0, [3.6, 1.85, 1.7], [3.3, 1.9, 1.6], [-0.09, 1.85, -0.41], [-0.12, 1.95, -0.41], lens=44)])
# 17: the sneeze, from behind his left shoulder: he is shot back into the mattresses; the blast runs up to the turbines, they spin up one after the other;
#     on the ridge three towns light up
SN17 = 0.08
st.shot('S17', 'grassland', setOpts=FIELD(**DUSK), lighting='dusk', actors=[act('mec', [0, 0.3, 0], 135, 'sneezeUp', 'worried', params={'dur': 1.0, 'float': 0.0}, keys=[k(SN17, clip='sneeze', params={'hold': 0.3}, blend=0.03),
            k(SN17 + 0.04, to=[-1.25, 0.25, 1.25], dur=0.1, glide=True, ease='out', face='keep'), k(SN17 + 0.14, clip='poster', params={'high': 0.25, 'slideAt': 0.7, 'slide': 0.25, 'stars': 1}, blend=0.02, face=135)])],
        props=TURB(lambda i: [[0, 0], [SN17 + 0.1 + 0.1 * i, 0], [SN17 + 0.35 + 0.1 * i, 95], [9, 95]], blur=0.8) +
              [MAT(hitAt=SN17 + 0.14), P('blast', 'sneezeBlast', pos=[0.3, 1.7, -0.3], ry=135, opts={'at': SN17, 'dur': 0.5, 'len': 14, 'spread': 2.4, 'n': 36}),
               P('towns', 'townLights', pos=[26, 0, -28], ry=-38, opts={'at': [SN17 + 0.5, SN17 + 0.68, SN17 + 0.86], 'spread': 9})],
        fx=[{'type': 'wind', 'at': SN17, 'dur': 0.5, 'v': [20, 0, -20], 'attack': 0.03, 'release': 0.3}, {'type': 'shake', 'at': SN17, 'dur': 0.3, 'amount': 0.04}],
        cams=[cam(0.0, [-4.2, 1.5, 7.6], [-4.0, 1.55, 7.3], [8.0, 4.3, -8.0], [8.0, 4.4, -8.0], lens=50)])
# 18: he is allergic to pollen: very close: one grain drifts down to the tip of his nose; his eyes follow it until they cross
G18 = 1.0                                           # the grain lands
st.shot('S18', 'grassland', setOpts=FIELD(), actors=[act('mec', [0, 0, 0], 0, 'stand', 'worried', keys=[k(0.0, look='grain', expr='surprised'), k(G18 - 0.35, toon={'face': {'cross': 1}}, toonDur=0.3, toonEase='inOut'), k(G18 - 0.05, look=None),
            k(G18 + 0.12, toon={'face': {'cross': 1}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.1), k(G18 + 0.3, toon={'face': {'cross': 1, 'lid': 0.45}}, toonDur=0.12)])],
        props=[P('grain', 'pollenGrain', pos=[0.55, 2.5, 0.9], opts={'r': 0.035}, keys=[k(0.0, to=[0.16, 2.18, 0.45], dur=0.55, arc=0.06, ease='inOut'), k(0.55, to=[0.0, 2.09, 0.2], dur=G18 - 0.55, arc=-0.04, ease='inOut')])],
        cams=[cam(0.0, [0.12, 2.02, 1.75], [0.1, 2.02, 1.5], [0, 2.02, 0], [0, 2.02, 0], lens=40)])
# 19: spring is coming: a hill in flower, a yellow cloud that drifts to him; the breaths again, bigger, bigger: he rises like a balloon, everything loose
#     flies to him; we leave before the sneeze
st.shot('S19', 'grassland', setOpts=FIELD(), actors=[act('mec', [0, 0, 0], 60, 'stand', 'scared', keys=[k(0.0, look=[6, 2, 1]), k(0.35, clip='sneezeUp', params={'dur': 2.2, 'breaths': 4, 'float': 1.3}, blend=0.08, look=None),
            k(0.6, toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.01), k(0.6, toon={'sq': [2.0, 1.75, 2.0]}, toonDur=1.95, toonEase='in')])],
        props=[P(f'turb{i}', 'windTurbine', pos=[x, 0, z], opts={'h': 9, 'rpm': -9, 'phase': i}) for i, (x, z) in enumerate([(-3.4, -24.0), (3.0, -32.0)])] + [P('cloud', 'pollenCloud', pos=[7.5, 2.0, 0.5], opts={'n': 150, 'size': [7, 3.4, 3.5], 'dir': [-2.3, -0.05, -0.1], 'seed': 12}),
               P('fl1', 'flowers', pos=[-1.3, 0, 1.2]), P('fl2', 'flowers', pos=[1.5, 0, 1.6]), P('fl3', 'flowers', pos=[0.4, 0, 2.3]), P('fl4', 'flowers', pos=[-2.4, 0, -0.8]), P('fl5', 'flowers', pos=[2.8, 0, -0.6]),
               P('alert', 'alertSign', pos=[-1.7, 0, 0.9], ry=15, opts={'text': 'VIGILANCE ROUGE', 'h': 2.0, 's': 0.8}, keys=[k(1.5, wobble=[0.25, 14, 0.5])]),
               P('pp1', 'flyingPaper', pos=[6.5, 0.6, 2.0], keys=[k(0.9, to=[0.6, 2.2, 0.3], dur=1.2, arc=0.8, ease='in')]), P('wig', 'wig', pos=[-6.0, 0.3, 1.5], keys=[k(1.3, to=[-0.5, 2.4, 0.2], dur=1.1, arc=1.0, ease='in')])],
        fx=[{'type': 'wind', 'at': 0.6, 'dur': 2.2, 'v': [-6, 0, 0], 'attack': 1.2, 'release': 0.1}],
        cams=[cam(0.0, [1.0, 1.5, 5.4], [1.4, 2.4, 8.4], [0.5, 1.5, 0], [0.2, 3.0, 0], lens=44, ease='inOut')])

# sound on the actions
st.cue('sfx:stretch', 'S01', 0.0, 0.3); st.cue('sfx:stretch', 'S01', 0.33, 0.35); st.cue('sfx:stretch', 'S01', 0.66, 0.4)
st.cue('thunder', 'S02', B2, 0.5); st.cue('whoosh', 'S02', B2, 0.5, 0.5, 300, 3000)
for w_, t_ in HITS.items(): st.cue('sfx:splat', 'S02', t_, 0.35)
for t_ in SLIDE.values(): st.cue('sfx:squeak', 'S03', t_, 0.35)
st.cue('whoosh', 'S04', G4, 0.4, 0.7, 400, 2500); st.cue('sfx:zip', 'S04', G4 + 0.08, 0.3)
st.cue('sfx:twang', 'S05', 0.14, 0.4); st.cue('pop', 'S05', 0.02, 0.3)
st.cue('sfx:slideUp', 'S06', T6 - 0.12, 0.35); st.cue('clack', 'S07', P7 + 0.26, 0.4); st.cue('sfx:tick', 'S08', T8 - 0.22, 0.4)
st.cue('sfx:splat', 'S09', B9, 0.4); st.cue('pop', 'S10', 0.3, 0.3)
for i, (_, _, z, _) in enumerate(SIDE11): st.cue('sfx:squeak', 'S11', round((z + 2.6 - 0.9) / V11, 3), 0.3)
st.cue('sfx:gasp', 'S12', 0.32, 0.35)
for _, _, _, _, d in RUN13: st.cue('sfx:zip', 'S13', d + 0.3, 0.35)
st.cue('sfx:poof', 'S13', 0.82, 0.3); st.cue('sfx:poof', 'S13', 0.7, 0.3)
st.cue('sfx:stretch', 'S14', HIT14 - 0.3, 0.35); st.cue('thud', 'S14', HIT14, 0.55); st.cue('sfx:spring', 'S14', HIT14 + 0.17, 0.4); st.cue('clack', 'S14', T14 + 0.15, 0.35)
st.cue('sfx:squeak', 'S15', 0.1, 0.3); st.cue('sfx:squeak', 'S15', 0.45, 0.3); st.cue('sfx:squeak', 'S15', 0.8, 0.3); st.cue('pop', 'S15', S15E + 0.2, 0.3)
st.cue('sfx:stretch', 'S16', 0.0, 0.3); st.cue('sfx:stretch', 'S16', 0.33, 0.35); st.cue('sfx:stretch', 'S16', 0.66, 0.4)
st.cue('thunder', 'S17', SN17, 0.5); st.cue('whoosh', 'S17', SN17, 0.45, 0.6, 300, 3000); st.cue('sfx:splat', 'S17', SN17 + 0.14, 0.35)
for i in range(3): st.cue('pop', 'S17', SN17 + 0.5 + 0.18 * i, 0.35)
st.cue('sfx:tick', 'S18', G18, 0.3)
for i in range(4): st.cue('sfx:stretch', 'S19', 0.35 + 0.55 * i, 0.3 + 0.04 * i)

st.card('S09', 'JOSIANE')
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("L'éternuement", rig='toon', fingers=True, cloth=True, idleShift=1, extra_cast={
    'p1': CITIZEN('femme', 31, glasses=False, hair='long', hairColor='#5A3A28'), 'p2': CITIZEN('serveur', 33, glasses=False), 'p3': CITIZEN('mamie', 35, suit='#D98A3C'),
    'meteo': CITIZEN('journaliste', 37, suit='#3E6E8C'), 'chef': CITIZEN('prefet', 39, build={'belly': 0.1}),
    'assureur': CITIZEN('boss', 41, suit='#6A5A4A', glasses=True), 'inge': CITIZEN('worker', 43, glasses=False)})
