#!/usr/bin/env python3
"""Le trou (story 37, cycle 1 of the cartoon staging): this man fell into a hole on his way to work. He called the town hall; the town hall
answered that the hole did not exist. It sent an officer to check: he fell in. Then a fireman: same. Then the mayor: with dignity.
Officially they were nowhere, so they stopped paying taxes. So the whole town jumped into the hole. Today the hole is full (COMPLET).
Cartoon rig for everyone (rig='toon'): hang time before each fall (four ways to fall), flattened and popped back, a double look and a
take, a stretched arm, euro eyes, dives, a periscope neck. Natural look (engine/look.js)."""
from story_kit import *

st = Story('trou', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 7), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0), ('S08', 'L07', 0), ('S09', 'L07', 3),
         ('S10', 'L08', 0), ('S11', 'L09', 0), ('S12', 'L09', 1), ('S13', 'L10', 0), ('S14', 'L10', 2), ('S15', 'L11', 0), ('S16', 'L11', 5), ('S17', 'L12', 0), ('S18', 'L12', 3)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}   # a camera key that glides from the previous one instead of cutting
HX, HZ = 7.0, 0.0                                  # the hole, in the right-hand pavement of the Paris street
STREET = {'hole': [HX, HZ, 0.9, 5]}
PHONE = lambda who='mec', hand='R', **kw: P(f'ph_{who}', 'smartPhone', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.08, 0.03], 'rot': [0, 0, 0]}, **kw)
DUST = lambda pid, pos, at_, per=0.7, **kw: P(pid, 'dustPuff', pos=pos, opts={'once': True, 'startAt': at_, 'period': per, **kw}, keys=[k(0.0, visible=False), k(at_, visible=True)])
BLUE, WHITE, RED = '#2A4B9B', '#F4F1E8', '#C8202A'
LEGS = lambda s, f=0.75: {'legL': [0, 0, 0, s, f], 'legR': [0, 0, 0, s, f], 'shinL': [0, 0, 0, s, f], 'shinR': [0, 0, 0, s, f]}
TAFFY = {'bend': LEGS(2.7), 'face': {'expr': 'scared', 'exprW': 1}}                 # the legs leave first...
TAFFY2 = {'bend': {**LEGS(1.6), 'spine': [0, 0, 0, 1.7, 0.8], 'neck': [0, 0, 0, 9.0, 0.45]}, 'face': {'expr': 'take', 'exprW': 1}}   # ...the neck holds the head back a moment

# 1: he walks to work, eyes on his phone, straight onto the hole, and keeps walking on the air
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', [HX, 0, -3.1], 0, 'walkRead', 'lookDown', keys=[k(0.0, to=[HX, 0, -0.95], dur=0.74, clip='walkRead'), k(0.74, to=[HX, 0, 0.1], dur=0.62, clip='walkRead', then='walkRead')])],
        props=[PHONE()], cams=[cam(0.0, [7.65, 1.75, 5.3], [7.45, 1.45, 4.3], [HX, 0.95, -1.0], [HX, 0.85, -0.2], lens=44)])
# 2: hang time: his eyes go down, then his head; he looks at us and gulps; the legs leave first, the head last; the phone waits, then follows
D2 = 0.56
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', [HX, 0, 0.1], 0, 'hangAir', 'neutral', params={'downAt': 0.08, 'usAt': 0.32, 'expr': 'uhoh'},
        keys=[k(0.08, toon={'bend': {'spine': [0.4, 0, 0, 1, None]}}, toonDur=0.12), k(0.32, toon={'sq': [1.1, 0.86, 1.1]}, toonDur=0.08), k(D2, toon=TAFFY, toonDur=0.17, toonEase='in'), k(D2 + 0.19, toon=TAFFY2, toonDur=0.08, toonEase='linear'), k(D2 + 0.28, toon={}, toonDur=0.04), k(D2 + 0.19, to=[HX, -7.0, 0.1], dur=0.16, glide=True, ease='in', face='keep')])],
        props=[PHONE(keys=[k(D2, detach=True), k(D2 + 0.45, detach=True, fall=True, floor=-6.5)]), DUST('d2', [HX, 0.05, 0.3], D2 + 0.4)],
        cams=[cam(0.0, [5.7, 1.7, 2.95], [5.75, 1.7, 2.85], [HX, 1.75, 0.1], [HX, 1.72, 0.1], lens=44), glide([cam(D2 - 0.06, [5.0, 1.35, 4.6], [5.1, 1.25, 4.4], [HX, 0.9, 0.1], [HX, 0.75, 0.1], lens=44)], 0.24)])
# 3: the hole in cross-section: he lands flat as a pancake (stars), pops back, the phone lands on his skull (a bump), he calls
st.shot('S03', 'holeSection', actors=[act('mec', [0, 5.4, 0], 0, 'airborne', 'scared', keys=[k(0.0, to=[0, 0, 0], dur=0.14, glide=True, ease='in', face='keep'), k(0.14, clip='pancake', params={'popAt': 0.34, 'stars': 1}),
        k(0.8, toon={'scl': {'head': [1.3, 0.62, 1.3]}, 'face': {'expr': 'pain', 'exprW': 1, 'bump': 0.3}}, toonDur=0.05), k(0.9, toon={'face': {'bump': 1}}, toonDur=0.2), k(0.96, clip='phoneEar', expr='unimpressed')])],
        props=[P('ph_mec', 'smartPhone', pos=[0.05, 5.2, 0.12], rot=[0.4, 0.3, 0.2], keys=[k(0.0, visible=False), k(0.62, visible=True), k(0.62, to=[0.04, 2.42, 0.12], dur=0.18, ease='in'), k(0.8, to=[0.33, 1.75, 0.3], dur=0.16, arc=0.45, ease='linear'),
               k(0.97, attach='mec', hand='R', offset=[0.0, -0.08, 0.03], rot=[0, 0, 0])])],
        fx=[{'type': 'shake', 'at': 0.14, 'dur': 0.22, 'amount': 0.035}, {'type': 'shake', 'at': 0.8, 'dur': 0.1, 'amount': 0.012}],
        cams=[cam(0.0, [0.3, 2.5, 7.0], [0.3, 2.5, 7.0], [0, 3.0, 0], [0, 3.0, 0], lens=44), glide([cam(0.07, [0.28, 1.3, 4.9], [0.2, 1.35, 4.5], [0, 1.2, 0], [0, 1.3, 0], lens=44)], 0.16)])
# 4: the town hall: the clerk listens, glances at the official map (AUCUN TROU) and stamps the file: INEXISTANT
HIT4 = st.at('S04', 'L03', 3) + 0.1
st.shot('S04', 'mairie', setOpts={'mapX': -0.62, 'mapY': 2.32, 'bannerX': -0.1, 'bannerY': 3.12, 'flagX': 1.7}, actors=[act('employee', [-0.34, 0, -1.65], 0, 'stampPhone', 'unimpressed', params={'hit': HIT4},
        keys=[k(0.12, look=[-0.62, 2.32, -2.5]), k(0.55, look=None), k(HIT4, expr='smug')])],
        props=[PHONE('employee'), P('chair', 'officeChair', pos=[-0.34, 0, -1.75]), P('stamp', 'rubberStamp', on={'actor': 'employee', 'hand': 'L', 'offset': [0, -0.12, 0.02], 'rot': [1.5708, 0, 0]}),
               P('form', 'stampedForm', pos=[0.13, 1.37, -0.7], rot=[-0.1, -0.1, -0.07], scale=0.01, keys=[k(HIT4 + 0.03, scale=0.88, dur=0.2, ease='outBack')])],
        fx=[{'type': 'shake', 'at': HIT4, 'dur': 0.16, 'amount': 0.022}],
        cams=[cam(0.0, [-0.12, 1.55, 2.6], [-0.14, 1.52, 2.3], [-0.16, 1.6, -1.7], [-0.16, 1.58, -1.7], lens=44)])
# 5: at the bottom: « ce trou n'existe pas »: he looks at the wall on his left, at the wall on his right, and takes it full in the face
T5 = st.at('S05', 'L04', 3)
st.shot('S05', 'holeSection', actors=[act('mec', [0, 0, 0], 0, 'phoneEar', 'hmm', keys=[k(0.0, toon={'face': {'bump': 0.8}}, toonDur=0), k(0.06, expr='sideL', look=[-1.0, 1.75, 1.35], toon={'face': {'bump': 0.8}, 'bend': {'spine': [0, 0, -0.14, 1, None]}}, toonDur=0.2), k(0.42, expr='side', look=[1.0, 1.75, 1.35], toon={'face': {'bump': 0.8}, 'bend': {'spine': [0, 0, 0.14, 1, None]}}, toonDur=0.2),
        k(T5 - 0.22, look=None, toon={'face': {'bump': 0.8}}, toonDur=0.1),
        k(T5 - 0.12, clip='take', params={'hold': 0.5, 'pop': 0, 'jaw': 0.9}, expr='take')])],
        props=[PHONE()], cams=[cam(0.0, [0.22, 1.85, 3.5], [0.2, 1.85, 3.35], [0, 1.82, 0], [0, 1.82, 0], lens=44), glide([cam(T5 - 0.12, [0.25, 1.95, 5.4], [0.22, 2.0, 5.2], [0, 2.0, 0], [0, 2.05, 0], lens=44)], 0.2)])
# 6: the officer comes to check, ticking his form, and walks out onto the hole without looking
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[act('agent', [HX, 0, -4.9], 0, 'walkWrite', 'determined', keys=[k(0.0, to=[HX, 0, 0.05], dur=1.5, clip='walkWrite', then='clipboard'), k(1.62, expr='proud')])],
        props=[P('cb', 'clipboardProp', on={'actor': 'agent', 'hand': 'L', 'offset': [0, -0.1, 0.06], 'rot': [1.2, 0, 0]})],
        cams=[cam(0.0, [4.7, 1.15, 3.7], [4.9, 1.1, 3.3], [HX, 1.1, -0.9], [HX, 1.15, -0.1], lens=44)])
# 7: he looks down: his cap jumps, he drops like a stone; the cap stays behind, then goes too
D7 = 0.52
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[act('agent', [HX, 0, 0.05], 0, 'clipboard', 'proud', keys=[k(0.06, clip='lookDown', expr='lookDown', toon={'bend': {'neck': [0.5, 0, 0, 2.2, 0.8]}}, toonDur=0.14),
        k(0.3, clip='take', params={'hold': 0.12, 'jaw': 0.8}, toon={}, toonDur=0.06), k(D7, toon={'hat': [60, 0, 0]}, toonDur=0), k(D7, to=[HX, -7.0, 0.05], dur=0.13, glide=True, ease='in', face='keep')])],
        props=[P('cb', 'clipboardProp', on={'actor': 'agent', 'hand': 'L', 'offset': [0, -0.1, 0.06], 'rot': [1.2, 0, 0]}),
               P('cap', 'copCap', pos=[HX, 2.74, 0.05], spin=9, keys=[k(0.0, visible=False), k(D7, visible=True), k(D7 + 0.36, to=[HX, -6.5, 0.05], dur=0.22, ease='in')]), DUST('d7', [HX, 0.05, 0.3], D7 + 0.3)],
        cams=[cam(0.0, [5.0, 1.45, 4.0], [5.1, 1.4, 3.8], [HX, 1.7, 0.05], [HX, 1.6, 0.05], lens=44)])
# 8: a fireman at a sprint: he brakes on the very edge and windmills
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[act('pompier', [HX, 0, -8.5], 0, 'dashOff', 'determined', keys=[k(0.0, to=[HX, 0, -1.1], dur=0.38, clip='dashOff', ease='out', then='skidStop', thenParams={'dur': 0.3}),
        k(0.7, clip='teeter', params={'grow': 1.6, 'fallAt': st.dur('S08') - 0.7 - 0.17})])],
        props=[DUST('d8', [HX, 0.05, -1.5], 0.3, 0.8)],
        cams=[cam(0.0, [7.75, 0.6, 2.9], [7.65, 0.62, 2.6], [HX, 1.25, -1.1], [HX, 1.3, -1.1], lens=52)])
# 9: « pareil »: at the bottom the two others watch him arrive
st.shot('S09', 'holeSection', actors=[act('mec', [-0.6, 0, 0.1], 0, 'lookUp', 'worried', keys=[k(0.0, toon={'face': {'bump': 0.6}}, toonDur=0), k(0.17, clip='jelly', params={'amp': 0.28}, expr='pain')]),
        act('agent', [0.62, 0, -0.1], 0, 'lookUp', 'scared', keys=[k(0.17, clip='jelly', params={'amp': 0.34, 'freq': 23}, expr='pain')]),
        act('pompier', [0.02, 6.0, 0.25], 0, 'airborne', 'scared', keys=[k(0.0, to=[0.02, 0, 0.25], dur=0.16, glide=True, ease='in', face='keep'), k(0.16, clip='accordion', params={'amp': 0.5, 'freq': 21, 'decay': 4.5, 'expr': 'dizzy', 'stars': 1})])],
        props=[DUST('d9', [0, 0.02, 0.5], 0.16, 0.5)], fx=[{'type': 'shake', 'at': 0.16, 'dur': 0.2, 'amount': 0.035}],
        cams=[cam(0.0, [0.2, 1.55, 6.3], [0.15, 1.5, 6.0], [0, 1.4, 0], [0, 1.4, 0], lens=44)])
# 10: the mayor, chest out: he steps onto nothing, smiles at us, waves and goes down slowly, like a lift
T10 = st.at('S10', 'L08', 3)
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[act('maire', [HX, 0, -4.2], 0, 'marchPomp', 'proud', keys=[k(0.0, to=[HX, 0, 0.05], dur=0.95, clip='marchPomp', then='stand'),
        k(T10 - 0.05, clip='wave', expr='teeth'), k(T10 + 0.1, to=[HX, -3.3, 0.05], dur=st.dur('S10') - T10 - 0.12, glide=True, ease='linear', face='keep'),
        k(T10 + 0.55, toon={'bend': {'armR': [0, 0, 0, 1.9, 0.8], 'foreR': [0, 0, 0, 1.9, 0.8]}}, toonDur=0.4)])],
        cams=[cam(0.0, [5.75, 0.5, 3.0], [5.9, 0.55, 2.7], [HX, 1.5, 0.05], [HX, 0.95, 0.05], lens=50)])
# 11: officially: the board at the town hall
st.shot('S11', 'mairie', setOpts={'map': False, 'board': {'at': [0.05, 0.2, 0.35, 0.5]}, 'boardX': 0.2, 'bannerX': 4.0, 'flagX': 3.5}, actors=[act('employee', [-0.92, 0, -1.75], 55, 'point', 'smug', keys=[k(0.58, clip='handsOnHips', face=15, expr='proud')])],
        cams=[cam(0.0, [-0.1, 1.85, 2.75], [-0.12, 1.87, 2.45], [-0.15, 1.85, -2.5], [-0.15, 1.85, -2.5], lens=44)])
# 12: they were nowhere: four men at the bottom of a hole, packed like sardines
SQ = {'sq': [0.74, 1.08, 0.9]}
ROW = [('mec', -0.66, 0.05, 0.35, 'unimpressed', 0.0), ('agent', -0.22, -0.08, -0.3, 'worried', 1.1), ('pompier', 0.22, 0.08, 0.4, 'sad', 2.3), ('maire', 0.66, -0.05, -0.35, 'proud', 3.4)]
# (they breathe in one after the other: no room, so each one goes thinner and taller, cheeks full; then they let go together)
IN = {'sq': [0.6, 1.26, 0.9], 'face': {'expr': 'puffed', 'exprW': 1}}
st.shot('S12', 'holeSection', actors=[act(w, [x, 0, z], 0, 'squeezed', e, params={'look': lk, 'ph': ph},
        keys=[k(0.0, toon=SQ, toonDur=0), k(0.16 + 0.09 * i, toon=IN, toonDur=0.24, toonEase='inOut'), k(0.82, toon={**SQ, 'sq': [0.8, 0.98, 0.9]}, toonDur=0.1), k(0.92, toon=SQ, toonDur=0.2), k(0.84, expr='relieved')]) for i, (w, x, z, lk, e, ph) in enumerate(ROW)],
        cams=[cam(0.0, [0.1, 1.5, 5.6], [0.08, 1.52, 5.2], [0, 1.45, 0], [0, 1.45, 0], lens=44)])
# 13: a letter comes down the hole: his arm goes up to fetch it
G13 = 0.36
st.shot('S13', 'holeSection', actors=[act('mec', [-0.66, 0, 0.05], 0, 'squeezed', 'lookUp', params={'look': 0.2}, keys=[k(0.0, toon=SQ, toonDur=0), k(0.1, clip='reachUpL', toon={**SQ, 'bend': {'armL': [0, 0, 0, 3.0, 0.7], 'foreL': [0, 0, 0, 3.0, 0.7]}}, toonDur=0.24, toonEase='out'), k(G13 + 0.06, toon=SQ, toonDur=0.12)])] +
        [act(w, [x, 0, z], 0, 'squeezed', 'lookUp', params={'look': lk, 'ph': ph}, keys=[k(0.0, toon=SQ, toonDur=0)]) for w, x, z, lk, e, ph in ROW[1:]],
        props=[P('bill', 'taxBill', pos=[-0.2, 5.0, 0.3], rot=[0.5, 0.2, 0.3], scale=0.6, keys=[k(0.0, to=[-0.5, 3.75, 0.3], dur=G13, ease='linear'), k(0.0, rotTo=[-0.4, -0.3, -0.35], dur=G13), k(G13, attach='mec', hand='L', offset=[0, -0.2, 0.02], rot=[0, 0, 0])])],
        cams=[cam(0.0, [0.1, 2.3, 7.4], [0.1, 2.2, 7.0], [0, 2.2, 0], [0, 2.1, 0], lens=44)])
# 14: the bill: nowhere, nothing to pay. Four pairs of eyes turn to euros
T14 = st.at('S14', 'L10', 4)
st.shot('S14', 'holeSection', actors=[act(w, [x, 0, z], 0, 'squeezed', 'surprised', params={'look': -x * 0.5, 'ph': ph}, keys=[k(0.0, toon=SQ, toonDur=0), k(T14 + i * 0.05, expr='euros', toon={**SQ, 'sq': [0.74, 1.2, 0.9]}, toonDur=0.1), k(T14 + i * 0.05 + 0.14, toon=SQ, toonDur=0.2)])
        for i, (w, x, z, lk, e, ph) in enumerate(ROW)],
        props=[P('bill', 'taxBill', pos=[0.0, 1.36, 0.75], rot=[-0.08, 0, 0.03], scale=1.12)],
        cams=[cam(0.0, [0.06, 1.7, 3.9], [0.05, 2.0, 3.35], [0, 1.6, 0.2], [0, 2.0, 0.1], lens=44, ease='inOut')])
# 15: so the whole town jumped in
JUMP = [('c1', [HX, 0, -7.5], [HX, 0, -1.5], 0.0, 'noseJump'), ('c2', [3.6, 0, 2.6], [5.75, 0, 0.75], 0.1, 'cannonball'), ('c3', [7.6, 0, 8.0], [7.25, 0, 1.6], 0.22, 'swanDive'),
        ('c4', [9.7, 0, -5.5], [8.35, 0, -1.0], 0.34, 'cannonball'), ('c5', [HX - 0.3, 0, -9.5], [HX - 0.2, 0, -1.55], 0.5, 'swanDive')]
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[act(w, a, 0, 'run', 'bigGrin', keys=[k(t0, to=b, dur=0.3, clip='run', ease='linear'), k(t0 + 0.3, to=[HX, -5.0, HZ], dur=0.42, clip=c, arc=1.5, ease='linear')]) for w, a, b, t0, c in JUMP],
        props=[DUST('d15a', [HX, 0.05, 0.2], 0.72, 0.5), DUST('d15b', [HX, 0.05, 0.2], 0.96, 0.5, seed=3),
               P('queue', 'queueFigures', pos=[0, 0, 0], opts={'path': [[8.9, -2.4], [9.1, -40]], 'people': True, 'gap': 0.8, 'size': 1.2, 'seed': 5})],
        cams=[cam(0.0, [3.9, 3.0, 4.9], [4.1, 2.8, 4.5], [HX, 0.7, -0.2], [HX, 0.6, -0.1], lens=50)])
# 16: seen from below: it rains citizens, the column grows
L2 = [('c1', -0.45, 2.15, 0.1, 0.05), ('c2', 0.05, 2.2, 0.25, -0.05), ('c3', 0.5, 2.1, 0.42, 0.1)]
st.shot('S16', 'holeSection', actors=[act(w, [x, 0, z], 0, 'squeezed', 'scared', params={'look': lk, 'ph': ph}, keys=[k(0.0, clip='lookUp', toon=SQ, toonDur=0)] + [k(t0 + 0.14, toon={**SQ, 'sq': [0.8, 0.86, 0.95]}, toonDur=0.05) for _, _, _, t0, _ in L2] + [k(0.62, toon=SQ, toonDur=0.25)]) for w, x, z, lk, e, ph in ROW] +
        [act(w, [x, 7.0, z], 0, 'airborne', 'bigGrin', keys=[k(0.0, visible=False), k(t0, visible=True), k(t0, to=[x, y, z], dur=0.14, glide=True, ease='in', face='keep'), k(t0 + 0.14, clip='squeezed', toon=SQ, toonDur=0.08)]) for w, x, y, t0, z in L2],
        fx=[{'type': 'shake', 'at': t0 + 0.14, 'dur': 0.12, 'amount': 0.02} for _, _, _, t0, _ in L2],
        cams=[cam(0.0, [0.1, 2.3, 8.6], [0.1, 2.4, 8.2], [0, 2.3, 0], [0, 2.4, 0], lens=44)])
# 17: today: a hole full to the brim, a sign, a latecomer with his suitcase
FULL = [('mec', [HX - 0.1, -1.55, 0.3], 10, 'squeezed', 'unimpressed'), ('agent', [HX + 0.5, -1.4, -0.1], -25, 'squeezed', 'worried'), ('pompier', [HX - 0.55, -1.3, -0.25], 30, 'squeezed', 'sad'), ('maire', [HX + 0.1, -1.2, -0.55], -5, 'wave', 'teeth'),
        ('c1', [HX + 0.45, -1.75, 0.45], -30, 'squeezed', 'bigGrin'), ('c3', [HX - 0.5, -1.8, 0.4], 35, 'squeezed', 'happy')]
SIGN = lambda at_: P('sign', 'completSign', pos=[7.0, 0, -1.55], ry=-22, opts={'onAt': at_, 'h': 1.85, 'w': 1.1})
LATE = [8.3, 0, -1.0]
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[act(w, p, ry, c, e, params={'ph': i * 1.3}) for i, (w, p, ry, c, e) in enumerate(FULL)] +
        [act('late', [9.5, 0, -8.5], 0, 'run', 'bigGrin', keys=[k(0.1, to=LATE, dur=0.75, clip='run', then='skidStop', thenParams={'dur': 0.25, 'expr': 'surprised'})])],
        props=[SIGN(99), P('case', 'briefcase', on={'actor': 'late', 'hand': 'L'})],
        cams=[cam(0.0, [4.75, 2.0, 5.0], [4.85, 1.95, 4.8], [HX + 0.35, 1.1, -0.6], [HX + 0.35, 1.1, -0.6], lens=46)])
# 18: COMPLET. The latecomer melts; from the pile, a neck comes up to have a look
T18 = st.at('S18', 'L12', 4)
st.shot('S18', 'parisStreet', setOpts=STREET, actors=[act(w, p, ry, c, e, params={'ph': i * 1.3}, keys=([k(T18 + 0.55, clip='periscope', params={'len': 10}, expr='deadpan'), k(T18 + 0.85, look='late'), k(T18 + 1.25, look=None)] if w == 'mec' else [])) for i, (w, p, ry, c, e) in enumerate(FULL)] +
        [act('late', LATE, -25, 'stand', 'surprised', keys=[k(0.0, look='sign'), k(T18 + 0.12, clip='melt', params={'dur': 0.9}, expr='cry')])],
        props=[SIGN(T18), P('case', 'briefcase', on={'actor': 'late', 'hand': 'L'}, keys=[k(T18 + 0.3, detach=True, fall=True, floor=0.02)])],
        cams=[cam(0.0, [4.85, 1.95, 4.8], [5.0, 1.85, 4.45], [HX + 0.35, 1.1, -0.6], [HX + 0.35, 1.25, -0.6], lens=46)])

# sound on the actions: steps that stop when the ground does, a slide whistle for every fall, wood and rubber for the gags
for t in (0.1, 0.32, 0.54): st.cue('sfx:stepSoft', 'S01', t, 0.5)   # three steps on the pavement, then none: he is on the air
st.cue('sfx:gulp', 'S02', 0.34, 0.4); st.cue('sfx:stretch', 'S02', D2, 0.45); st.cue('sfx:slideDown', 'S02', D2 + 0.2, 0.42); st.cue('sfx:slideDown', 'S02', D2 + 0.47, 0.22)
st.cue('sfx:splat', 'S03', 0.14, 0.42); st.cue('sfx:spring', 'S03', 0.48, 0.4); st.cue('sfx:bonk', 'S03', 0.8, 0.42); st.cue('sfx:beep', 'S03', 1.08, 0.2)
st.cue('sfx:ring', 'S04', 0.0, 0.16); st.cue('thud', 'S04', HIT4, 0.5); st.cue('pop', 'S04', HIT4 + 0.05, 0.3)
st.cue('sfx:tick', 'S05', st.at('S05', 'L04', 2), 0.3); st.cue('sfx:tick', 'S05', st.at('S05', 'L04', 2) + 0.22, 0.3); st.cue('sfx:slideUp', 'S05', T5 - 0.1, 0.3); st.cue('sfx:gasp', 'S05', T5 + 0.03, 0.4)
for t in (0.2, 0.55, 0.9, 1.25): st.cue('sfx:step', 'S06', t, 0.4)
st.cue('sfx:tick', 'S06', 1.6, 0.35)
st.cue('sfx:stretch', 'S07', 0.08, 0.35); st.cue('sfx:slideUp', 'S07', 0.3, 0.3); st.cue('sfx:slideDown', 'S07', D7, 0.45); st.cue('sfx:slideDown', 'S07', D7 + 0.38, 0.2)
st.cue('sfx:zip', 'S08', 0.0, 0.45); st.cue('sfx:brake', 'S08', 0.34, 0.4); st.cue('whoosh', 'S08', 0.7, 0.22, 0.4, 500, 2500)
st.cue('sfx:slideDown', 'S09', -0.28, 0.4); st.cue('sfx:splat', 'S09', 0.16, 0.4); st.cue('sfx:twang', 'S09', 0.2, 0.35)
for t in (0.15, 0.45, 0.75): st.cue('sfx:stepHeavy', 'S10', t, 0.4)
st.cue('sfx:slideDownSlow', 'S10', T10 + 0.12, 0.3)
for t in (0.05, 0.2, 0.35, 0.5): st.cue('pop', 'S11', t, 0.3)
for i in range(4): st.cue('sfx:stretch', 'S12', 0.16 + 0.09 * i, 0.3)
st.cue('sfx:poof', 'S12', 0.82, 0.4)
st.cue('sfx:paper', 'S13', 0.0, 0.3); st.cue('sfx:stretch', 'S13', 0.1, 0.45); st.cue('sfx:twang', 'S13', G13 + 0.06, 0.3)
st.cue('sfx:cash', 'S14', T14, 0.5)
for i, (_, _, _, t0, _) in enumerate(JUMP): st.cue('sfx:slideDown', 'S15', t0 + 0.34, 0.26); st.cue('sfx:poof', 'S15', t0 + 0.72, 0.3)
st.cue('whoosh', 'S15', 0.0, 0.2, 0.9, 300, 1500)
for _, _, _, t0, _ in L2: st.cue('thud', 'S16', t0 + 0.14, 0.42); st.cue('sfx:squeak', 'S16', t0 + 0.16, 0.4)
st.cue('sfx:stepRun', 'S17', 0.3, 0.4); st.cue('sfx:stepRun', 'S17', 0.5, 0.4); st.cue('sfx:stepRun', 'S17', 0.7, 0.4); st.cue('sfx:brake', 'S17', 0.82, 0.35)
st.cue('clack', 'S18', T18, 0.5); st.cue('sfx:beep', 'S18', T18 + 0.02, 0.25); st.cue('sfx:slideDownSlow', 'S18', T18 + 0.14, 0.26); st.cue('thud', 'S18', T18 + 0.75, 0.3); st.cue('sfx:stretch', 'S18', T18 + 0.57, 0.4)

st.card('S17', "AUJOURD'HUI")
FACES = {   # the story's own expressions (recipes as in tools/face/gen_expressions.py)
    'euros': {'brows': {'L': {'dy': -24}, 'R': {'dy': -24}}, 'eyes': {'L': {'kind': 'euro', 's': 1.9}, 'R': {'kind': 'euro', 's': 1.9}}, 'mouth': {'kind': 'teeth'}},
    'uhoh': {'brows': {'L': {'dy': -34, 'rot': 18}, 'R': {'dy': -34, 'rot': -18}}, 'eyes': {'L': {'s': 1.4, 'psize': 0.6, 'pupil': [0, 0.1]}, 'R': {'s': 1.45, 'psize': 0.6, 'pupil': [0, 0.1]}}, 'mouth': {'kind': 'wavy', 'w': 0.7}, 'extras': ['sweat']},
}
CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write('Le trou', rig='toon', faces=FACES, extra_cast={
    'employee': {'preset': 'madame', 'suit': '#5B6F8C', 'glasses': True, 'build': {'width': 0.84, 'headWidth': 1.3}},
    'agent': {'preset': 'worker', 'hat': 'copcap', 'facial': 'mustache', 'hair': 'receding', 'glasses': False, 'seed': 7, 'build': {'width': 0.86, 'headWidth': 1.3, 'belly': 0.06}},
    'pompier': {'preset': 'pompier', 'glasses': False, 'seed': 11, 'skin': '#C98E62', 'build': {'width': 0.9, 'headWidth': 1.3}},
    'maire': {'preset': 'politique', 'sash': [BLUE, WHITE, RED], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3, 'belly': 0.14}},
    'c1': CITIZEN('mamie', 17), 'c2': CITIZEN('gamin', 19, build={'height': 0.66}), 'c3': CITIZEN('chef', 22), 'c4': CITIZEN('sportif', 23, skin='#8A5A3C'), 'c5': CITIZEN('serveur', 26),
    'late': CITIZEN('tourist', 29)})
