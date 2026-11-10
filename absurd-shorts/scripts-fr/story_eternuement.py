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
# (the following shots are staged one block at a time; until then each holds a simple view so the film renders end to end)
for sid in ('S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19'):
    st.shot(sid, 'parisStreet', setOpts=STREET, actors=[act('mec', [MX, 0, MZ], 0, 'stand', 'neutral')], cams=[cam(0.0, [MX + 0.4, 1.5, 4.5], [MX + 0.35, 1.5, 4.2], [MX, 1.3, 0], [MX, 1.3, 0], lens=44)])

CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("L'éternuement", rig='toon', fingers=True, cloth=True, idleShift=1, extra_cast={
    'p1': CITIZEN('femme', 31, glasses=False, hair='long', hairColor='#5A3A28'), 'p2': CITIZEN('serveur', 33, glasses=False), 'p3': CITIZEN('mamie', 35, suit='#D98A3C'),
    'meteo': CITIZEN('journaliste', 37, suit='#3E6E8C'), 'chef': CITIZEN('prefet', 39, build={'belly': 0.1})})
