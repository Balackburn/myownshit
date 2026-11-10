#!/usr/bin/env python3
"""Le trou (story 37, cycle 1 of the cartoon staging): this man fell into a hole on his way to work. He called the town hall; the town hall
answered that the hole did not exist. It sent an officer to check: he fell in. Then a fireman: same. Then the mayor: with dignity.
Officially they were nowhere, so they stopped paying taxes. So the whole town jumped into the hole. Today the hole is full (COMPLET).
Cartoon rig for everyone (rig='toon'): hang time before each fall (four ways to fall), flat as a rug and popped back, a double look and a
take, eyes sent down the hole on stalks, a stretched arm, euro eyes, dives, a neck like a hose. Natural look (engine/look.js).
Second pass after the animation review: one-shot clips are keyed (a base clip starts in the distant past), hard hits have no blend,
falls trail, every payoff sits above the caption band."""
from story_kit import *

st = Story('trou', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 1.1333, 0), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0), ('S08', 'L07', 0), ('S09', 'L07', 3),
         ('S10', 'L08', 0), ('S11', 'L09', 0), ('S12', 'L09', 1), ('S13', 15.7333, 0), ('S14', 'L10', 2), ('S15', 'L11', 0), ('S16', 'L11', 5), ('S17', 'L12', 0), ('S18', 'L12', 3)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}   # a camera key that glides from the previous one instead of cutting
HX, HZ = 7.0, 0.0                                  # the hole, in the right-hand pavement of the Paris street
STREET = {'hole': [HX, HZ, 0.9, 5], 'clear': [-45, 25], 'eiffelX': -26}   # nothing on the pavement behind the action; the tower beside his head, not on it
PHONE = lambda who='mec', hand='R', **kw: P(f'ph_{who}', 'smartPhone', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.08, 0.03], 'rot': [0, 0, 0]}, opts={'case': '#F2C230'}, scale=1.25, **kw)   # a yellow case, a little big: it reads from behind
DUST = lambda pid, pos, at_, per=0.7, s=0.7, **kw: P(pid, 'dustPuff', pos=pos, scale=s, opts={'once': True, 'startAt': at_, 'period': per, 'color': '#F6F3EC', **kw}, keys=[k(0.0, visible=False), k(at_, visible=True)])   # small white puffs (the big beige ones read as rubble)
BLUE, WHITE, RED = '#2A4B9B', '#F4F1E8', '#C8202A'
LEGS = lambda s, f=0.75: {'legL': [0, 0, 0, s, f], 'legR': [0, 0, 0, s, f], 'shinL': [0, 0, 0, s, f], 'shinR': [0, 0, 0, s, f]}

# 1: he walks to work, eyes on his phone, straight onto the hole, and keeps walking on the air (quick small steps: four of them over the void)
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', [HX, 0, -1.6], 0, 'walkRead', 'lookDown', keys=[k(0.0, to=[HX, 0, 0.15], dur=1.02, clip='walkRead', cadence=2.1, ease='linear', blend=0.001, then='walkRead')])],
        props=[PHONE()], cams=[cam(0.0, [8.35, 2.75, 5.5], [8.15, 2.55, 5.0], [HX, 0.95, -0.55], [HX, 0.9, 0.0], lens=44)])
# 2: hang time: he stops; his eyes leave the phone, then his head goes down past it; he looks at us and gulps (held); the legs leave first, the head
#    stays behind on its neck, then snaps down; the phone waits where the hand left it, over the hole, then follows
D2 = 0.78                                          # the drop
LEG2, NECK2 = 2.7, 9.0                             # legs x2.7: the feet go 1.6 m down below the body (a stretched leg grows downward from the hip: no move needed);
                                                   # then the body drops 1.22 m while the spine (x1.7) and the neck (x9) grow upward by as much: the head stays
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('mec', [HX, 0, 0.15], 0, 'walkRead', 'lookDown', keys=[k(0.0, clip='hangPhone', params={'downAt': 0.12, 'usAt': 0.36, 'expr': 'uhoh'}, blend=0.06), k(0.36, expr='uhoh'),
        k(D2, clip='fallDrag', params={'expr': 'take', 'jaw': 0.9, 'stretch': 1.0}, blend=0.1), k(D2 - 0.03, toon={'auto': 0}, toonDur=0.03), k(D2, toon={'auto': 0, 'bend': LEGS(LEG2)}, toonDur=0.12, toonEase='in'),
        k(D2 + 0.12, to=[HX, -1.22, 0.15], dur=0.1, glide=True, ease='linear', face='keep'), k(D2 + 0.12, toon={'auto': 0, 'bend': {**LEGS(LEG2), 'spine': [0, 0, 0, 1.7, 0.8], 'neck': [0, 0, 0, NECK2, 0.45]}}, toonDur=0.1, toonEase='linear'),
        k(D2 + 0.22, to=[HX, -8.0, 0.15], dur=0.12, glide=True, ease='in', face='keep'), k(D2 + 0.22, toon={}, toonDur=0.05)])],
        props=[PHONE(keys=[k(D2, detach=True, worldRot=[0.15, 3.35, 0.1], wobble=[0.6, 24, 4.0]), k(D2 + 0.02, scale=1.9, dur=0.1, ease='outBack'), k(D2 + 0.5, to=[None, -6.5, None], dur=0.1, ease='in')]), DUST('d2', [HX, -0.35, 0.2], D2 + 0.34)],
        cams=[cam(0.0, [7.6, 1.5, 2.85], [7.56, 1.52, 2.7], [HX, 1.86, 0.15], [HX, 1.84, 0.15], lens=44), glide([cam(D2 - 0.14, [8.1, 2.4, 5.6], [8.05, 2.4, 5.5], [HX, 0.82, 0.15], [HX, 0.82, 0.15], lens=44)], 0.22)])
# 3: the hole in cross-section, seen from above: he lands flat as a rug (stars, a blink), springs back; the phone lands on his skull (a bump), bounces,
#    and he catches it at his ear
POP3 = 0.4
st.shot('S03', 'holeSection', actors=[act('mec', [0, 4.4, 0], 0, 'fallDrag', 'scared', keys=[k(0.0, to=[0, 0, 0], dur=0.12, glide=True, ease='linear', face='keep'), k(0.12, clip='splat', params={'popAt': POP3 - 0.12, 'stars': 1, 'blinkAt': 0.11}, blend=0.02),
        k(0.74, toon={'scl': {'head': [1.3, 0.62, 1.3]}, 'face': {'expr': 'pain', 'exprW': 1, 'bump': 0.3}}, toonDur=0.05), k(0.76, clip='phoneEar', expr='pain', blend=0.16), k(0.84, toon={'face': {'bump': 1}}, toonDur=0.2), k(0.96, toon={'face': {'bump': 1}, 'sq': [1.05, 0.93, 1.05]}, toonDur=0.05), k(1.02, toon={'face': {'bump': 1}}, toonDur=0.16), k(0.98, expr='unimpressed'), k(1.1, look=[1.0, 2.4, 2.5]), k(1.24, look=None)])],
        props=[P('ph_mec', 'smartPhone', pos=[0.05, 5.2, 0.12], rot=[0.4, 3.4, 0.2], opts={'case': '#F2C230'}, scale=1.25, keys=[k(0.0, visible=False), k(0.6, visible=True), k(0.6, to=[0.03, 2.44, 0.12], dur=0.14, ease='in'), k(0.74, to=[-0.36, 1.98, 0.2], dur=0.2, arc=0.5, ease='linear'),
               k(0.74, rotTo=[0.4, 3.4, 6.5], dur=0.2, ease='linear'), k(0.94, attach='mec', hand='R', offset=[0.0, -0.08, 0.03], rot=[0, 0, 0])])],
        fx=[{'type': 'shake', 'at': 0.12, 'dur': 0.22, 'amount': 0.04}, {'type': 'shake', 'at': 0.74, 'dur': 0.1, 'amount': 0.012}],
        cams=[cam(0.0, [0.2, 2.9, 4.3], [0.2, 2.85, 4.2], [0, 0.15, -0.05], [0, 0.15, -0.05], lens=44), glide([cam(POP3 - 0.03, [0.25, 3.0, 5.4], [0.22, 2.9, 5.2], [0, 1.1, -0.1], [0, 1.12, -0.1], lens=44)], 0.26)])
# 4: the town hall: the clerk listens, glances at the official map (AUCUN TROU), winds up and stamps the file: INEXISTANT. The sheet jumps up to show it
HIT4 = round(st.at('S04', 'L03', 3) + 0.14, 3)
HOP = lambda pid, name, pos, h=0.14, d=0.0, **kw: P(pid, name, pos=pos, keys=[k(HIT4 + d, to=[pos[0], pos[1] + h, pos[2]], dur=0.07, ease='out'), k(HIT4 + d + 0.07, to=pos, dur=0.09, ease='in')], **kw)   # things on the desk hop on the hit
st.shot('S04', 'mairie', setOpts={'mapX': -0.48, 'mapY': 2.32, 'bannerX': -0.1, 'bannerY': 3.12, 'flagX': 1.7, 'plate': False}, actors=[act('employee', [-0.34, 0, -1.65], 0, 'sit', 'unimpressed',
        keys=[k(0.0, clip='stampDesk', params={'hit': HIT4}, blend=0.04), k(0.05, expr='lookUp', look=[-1.4, 2.9, 0.4]), k(0.27, look=None, expr='determined'), k(HIT4, expr='smug'), k(HIT4 + 0.3, look='form')])],
        props=[PHONE('employee'), P('chair', 'officeChair', pos=[-0.34, 0, -1.75]), P('stamp', 'rubberStamp', on={'actor': 'employee', 'hand': 'L', 'offset': [0, -0.12, 0.02], 'rot': [1.5708, 0, 0]}),
               HOP('mug', 'mug', [-0.72, 0.815, -0.78], 0.16), HOP('mug2', 'mug', [0.3, 0.815, -0.66], 0.11, 0.02, opts={'color': '#C8202A'}),
               P('form', 'stampedForm', pos=[-0.02, 0.83, -1.02], rot=[-1.5708, 0, 0.12], scale=0.3, keys=[k(HIT4 + 0.03, to=[0.3, 1.47, 0.3], dur=0.24, arc=0.28, ease='out'), k(HIT4 + 0.03, rotTo=[-0.08, -0.12, -0.07], dur=0.2, ease='out'), k(HIT4 + 0.04, scale=0.92, dur=0.24, ease='outBack')])],
        fx=[{'type': 'shake', 'at': HIT4, 'dur': 0.18, 'amount': 0.03}],
        cams=[cam(0.0, [0.1, 1.52, 2.6], [0.08, 1.5, 2.3], [0.06, 1.58, -1.7], [0.06, 1.56, -1.7], lens=44)])
# 5: at the bottom: « ce trou n'existe pas »: he looks at the wall on his left, at the wall on his right, and takes it full in the face
T5 = st.at('S05', 'L04', 3)
st.shot('S05', 'holeSection', actors=[act('mec', [0, 0, 0], 0, 'phoneEar', 'hmm', keys=[k(0.0, toon={'face': {'bump': 0.8}}, toonDur=0), k(0.06, expr='sideL', look=[-1.0, 1.75, 1.35], toon={'face': {'bump': 0.8}, 'bend': {'spine': [0, 0, -0.14, 1, None]}}, toonDur=0.2), k(0.42, expr='side', look=[1.0, 1.75, 1.35], toon={'face': {'bump': 0.8}, 'bend': {'spine': [0, 0, 0.14, 1, None]}}, toonDur=0.2),
        k(T5 - 0.22, look=None, toon={'face': {'bump': 0.8}}, toonDur=0.1),
        k(T5 - 0.12, clip='take', params={'hold': 0.5, 'pop': 0.55, 'jaw': 0.9}, expr='take')])],
        props=[PHONE()], cams=[cam(0.0, [0.22, 1.85, 3.5], [0.2, 1.85, 3.35], [0, 1.82, 0], [0, 1.82, 0], lens=44), glide([cam(T5 - 0.12, [0.25, 1.95, 5.4], [0.22, 2.0, 5.2], [0, 2.0, 0], [0, 2.05, 0], lens=44)], 0.2)])
# 6: the officer comes to check, ticking his form, and walks out onto the hole without looking
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[act('agent', [HX, 0, -4.9], 0, 'walkWrite', 'determined', keys=[k(0.0, to=[HX, 0, 0.05], dur=1.5, clip='walkWrite', then='clipboard'), k(1.62, expr='proud')])],
        props=[P('cb', 'clipboardProp', on={'actor': 'agent', 'hand': 'L', 'offset': [0, -0.1, 0.06], 'rot': [1.2, 0, 0]})],
        cams=[cam(0.0, [4.3, 2.0, 4.4], [4.5, 2.0, 4.0], [HX, 0.95, -0.7], [HX, 0.9, -0.1], lens=44)])
# 7: seen from the side: he looks down without bending: his head tips over, his eyes go down to the hole on their stalks, have a look round, come back;
#    he turns to us, and drops like a stone; the cap and the clipboard stay behind, then follow
E7, B7, D7 = 0.2, 0.52, 0.67                       # the eyes leave, come back, the drop
NECK7 = lambda w=0: {'neck': [1.48 + w, w, 0, 1.6, 0.8]}   # the head tips right over (the neck bends, the body stays a post): the stalks go down along his front
EYES7 = lambda L, w=0: {'face': {'pop': 1, 'popLen': L, 'eyeScale': 1.6, 'expr': 'lookDown', 'exprW': 1}, 'bend': NECK7(w)}
CAM7 = [2.0, 1.0, 0.9]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[act('agent', [HX, 0, 0.05], 0, 'clipboard', 'proud', keys=[k(0.08, clip='stiff', expr='lookDown', blend=0.1), k(0.08, toon={'bend': NECK7()}, toonDur=0.12),
        k(E7, toon=EYES7(1.3), toonDur=0.11, toonEase='outBack'), k(E7 + 0.14, toon=EYES7(1.25, 0.14), toonDur=0.08, toonEase='inOut'), k(E7 + 0.23, toon=EYES7(1.3, -0.12), toonDur=0.08, toonEase='inOut'),
        k(B7, toon={'hat': [0.3, 0, 0], 'face': {'expr': 'take', 'exprW': 1}}, toonDur=0.06, toonEase='in'), k(B7 + 0.03, expr='take', look=[CAM7[0], 1.7, CAM7[2]]), k(D7, toon={'hat': [60, 0, 0]}, toonDur=0), k(D7, clip='fallDrag', blend=0.05), k(D7, to=[HX, -7.0, 0.05], dur=0.13, glide=True, ease='in', face='keep')])],
        props=[P('cb', 'clipboardProp', on={'actor': 'agent', 'hand': 'L', 'offset': [0, -0.1, 0.06], 'rot': [1.2, 0, 0]}, keys=[k(D7, detach=True, wobble=[0.4, 22, 5]), k(D7 + 0.2, to=[None, -6.5, None], dur=0.16, ease='in')]),
               P('cap', 'copCap', pos=[HX, 2.62, 0.05], spin=7, scale=1.25, keys=[k(0.0, visible=False), k(D7, visible=True), k(D7 + 0.3, to=[HX, -1.2, 0.05], dur=0.2, ease='in')]), DUST('d7', [HX, -0.35, 0.2], D7 + 0.26)],
        cams=[cam(0.0, CAM7, [CAM7[0] + 0.15, CAM7[1], CAM7[2]], [HX, 1.0, 0.35], [HX, 1.0, 0.35], lens=44)])
# 8: a fireman at a sprint: he brakes on the very edge and windmills
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[act('pompier', [HX, 0, -8.5], 0, 'dashOff', 'determined', keys=[k(0.0, to=[HX, 0, -1.1], dur=0.36, clip='dashOff', ease='out', then='skidStop', thenParams={'dur': 0.24}),
        k(0.58, clip='teeter', params={'grow': 1.6, 'spin': 37, 'pop': 0.8, 'jaw': 0.55, 'fallAt': st.dur('S08') - 0.58 - 0.17})])],
        props=[DUST('d8', [HX, 0.05, -1.6], 0.3, 0.8, 0.8)],
        cams=[cam(0.0, [7.95, 2.25, 5.4], [7.85, 2.25, 5.1], [HX, 0.72, -0.4], [HX, 0.72, -0.4], lens=46)])
# 9: « pareil »: at the bottom the two others watch him arrive: a hard landing, the bellows of an accordion
st.shot('S09', 'holeSection', actors=[act('mec', [-0.6, 0, 0.1], 0, 'lookUp', 'worried', keys=[k(0.0, toon={'face': {'bump': 0.6}}, toonDur=0), k(0.14, clip='jelly', params={'amp': 0.28}, expr='pain', blend=0.03)]),
        act('agent', [0.62, 0, -0.1], 0, 'lookUp', 'scared', keys=[k(0.14, clip='jelly', params={'amp': 0.34, 'freq': 23}, expr='pain', blend=0.03)]),
        act('pompier', [0.02, 6.2, 0.25], 0, 'fallDrag', 'scared', keys=[k(0.0, to=[0.02, 0, 0.25], dur=0.14, glide=True, ease='linear', face='keep'), k(0.14, clip='accordion', params={'hit': True, 'expr': 'dizzy', 'stars': 1}, blend=0.02)])],
        props=[DUST('d9', [0, 0.02, 0.5], 0.14, 0.5)], fx=[{'type': 'shake', 'at': 0.14, 'dur': 0.2, 'amount': 0.04}],
        cams=[cam(0.0, [0.2, 1.55, 6.3], [0.15, 1.5, 6.0], [0, 1.4, 0], [0, 1.4, 0], lens=44)])
# 10: the mayor, chest out: he steps onto nothing, smiles at us, waves from the wrist and goes down slowly, like a lift; the hand stays last
W10, G10, V10 = 0.92, 1.05, 3.33                   # the wave, the descent starts, its speed (m/s)
END10 = st.dur('S10')
FORE10 = lambda t: max(1.0, (V10 * (t - G10) - 1.42) / 0.33)   # the forearm stretches so that the hand stays 0.5 m above the rim while the body goes on down
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[act('maire', [HX, 0, -2.8], 0, 'marchPomp', 'proud', keys=[k(0.0, to=[HX, 0, 0.05], dur=0.85, clip='marchPomp', then='stand'),
        k(W10, clip='royalWave', params={'flickAt': END10 - 0.2 - W10}, expr='teeth', blend=0.14), k(G10, to=[HX, -V10 * (END10 - G10), 0.05], dur=END10 - G10, glide=True, ease='linear', face='keep'),
        k(G10 - 0.04, toon={'auto': 0}, toonDur=0.04), k(1.575, toon={'auto': 0, 'bend': {'foreR': [0, 0, 0, FORE10(END10 - 0.09), 0.6]}}, toonDur=END10 - 0.09 - 1.575, toonEase='linear'), k(END10 - 0.08, toon={'auto': 0}, toonDur=0.05, toonEase='in')])],
        cams=[cam(0.0, [5.3, 1.9, 4.6], [5.5, 1.9, 4.3], [HX, 1.05, 0.0], [HX, 0.3, 0.05], lens=46, ease='in')])   # the camera tilts down with him: the hole climbs clear of the captions
# 11: officially: the board at the town hall
st.shot('S11', 'mairie', setOpts={'map': False, 'plate': False, 'board': {'at': [0.05, 0.2, 0.35, 0.5]}, 'boardX': 0.05, 'bannerX': 4.0, 'flagX': 3.5}, actors=[act('employee', [-0.92, 0, -1.75], 55, 'point', 'smug', keys=[k(0.58, clip='handsOnHips', face=15, expr='proud')])],
        cams=[cam(0.0, [-0.26, 1.85, 2.85], [-0.28, 1.87, 2.6], [-0.3, 1.85, -2.5], [-0.3, 1.85, -2.5], lens=44)])
# 12: they were nowhere: four men at the bottom of a hole, packed like sardines
SQ = {'sq': [0.74, 1.08, 0.9]}
ROW = [('mec', -0.66, 0.05, 0.35, 'unimpressed', 0.0), ('agent', -0.22, -0.08, -0.3, 'worried', 1.1), ('pompier', 0.22, 0.08, 0.4, 'sad', 2.3), ('maire', 0.66, -0.05, -0.35, 'proud', 3.4)]
# (they breathe in one after the other: no room, so each one goes thinner and taller, cheeks full, eyes on the neighbour; the two at the ends are pushed
#  against the walls; then they let go together)
IN = lambda i: {'sq': [0.6, 1.26, 0.9], 'face': {'expr': 'puffed', 'exprW': 1}, 'bend': {'spine': [0, 0.2 if i == 0 else -0.2 if i == 3 else 0, 0, 1, None]}}
NEIGH = ['agent', 'pompier', 'agent', 'pompier']
st.shot('S12', 'holeSection', actors=[act(w, [x, 0, z], 0, 'squeezed', e, params={'look': lk, 'ph': ph},
        keys=[k(0.0, toon=SQ, toonDur=0), k(0.1 + 0.08 * i, toon=IN(i), toonDur=0.2, toonEase='inOut'), k(0.16 + 0.08 * i, look=NEIGH[i]), k(0.68, toon={**SQ, 'sq': [0.8, 0.98, 0.9]}, toonDur=0.1), k(0.68, look=None, expr='relieved'), k(0.78, toon=SQ, toonDur=0.18)]) for i, (w, x, z, lk, e, ph) in enumerate(ROW)],
        cams=[cam(0.0, [0.1, 1.5, 5.6], [0.08, 1.52, 5.25], [0, 1.45, 0], [0, 1.45, 0], lens=44)])
# 13: a letter comes down the hole: their heads follow it; his arm goes all the way up the shaft to fetch it, fumbles, snaps back: the row rocks
A13, G13, B13 = 0.2, 0.3, 0.5                      # the arm leaves, the grab, the snap back
ARM13 = lambda s, f=0.6: {**SQ, 'bend': {'armL': [0, 0, 0, s, f], 'foreL': [0, 0, 0, s, f]}}
ROCK = lambda i, a: {**SQ, 'sq': [0.78, 1.0, 0.9], 'bend': {'spine': [0, a, 0, 1, None]}}
st.shot('S13', 'holeSection', actors=[act('mec', [-0.66, 0, 0.05], 0, 'squeezed', 'lookUp', params={'look': 0.2}, keys=[k(0.0, toon=SQ, toonDur=0), k(0.0, look='bill'), k(A13 - 0.1, toon={**SQ, 'sq': [0.84, 0.92, 0.95]}, toonDur=0.09),
        k(A13, clip='reachHigh', expr='determined', blend=0.07), k(A13, toon=ARM13(3.7), toonDur=0.1, toonEase='outBack'), k(B13, toon=ARM13(1.0, None), toonDur=0.06, toonEase='in'), k(B13 + 0.05, clip='holdOut', expr='surprised', blend=0.1),
        k(B13 + 0.07, toon={**SQ, 'sq': [0.9, 0.8, 0.95]}, toonDur=0.04), k(B13 + 0.12, toon=SQ, toonDur=0.14)])] +
        [act(w, [x, 0, z], 0, 'squeezed', 'lookUp', params={'look': lk, 'ph': ph}, keys=[k(0.0, toon=SQ, toonDur=0), k(0.0, look='bill'), k(B13 + 0.06 + 0.03 * i, toon=ROCK(i, -0.22), toonDur=0.05), k(B13 + 0.12 + 0.03 * i, toon=ROCK(i, 0.13), toonDur=0.07), k(B13 + 0.2 + 0.03 * i, toon=SQ, toonDur=0.12), k(B13 + 0.1, expr='surprised')])
         for i, (w, x, z, lk, e, ph) in enumerate(ROW[1:], 1)],
        props=[P('bill', 'taxBill', pos=[-0.3, 5.5, 0.3], rot=[0.5, 0.2, 0.3], scale=0.6, keys=[k(0.0, to=[-0.45, 4.32, 0.3], dur=G13, ease='out'), k(0.0, rotTo=[-0.4, -0.3, -0.35], dur=G13), k(G13, attach='mec', hand='L', offset=[0, -0.2, 0.02], rot=[0, 0, 0])])],
        cams=[cam(0.0, [0.1, 2.5, 7.5], [0.1, 2.45, 7.2], [0, 2.4, 0], [0, 2.35, 0], lens=44)])
# 14: the bill: nowhere, nothing to pay. Four pairs of eyes turn to euros
T14 = st.at('S14', 'L10', 4)
EUR = {'pop': 1, 'popLen': 0.07, 'euro': 1, 'eyeScale': 1.05}   # money eyes: out on stalks, a euro sign on each
GRIN14 = ['teeth', 'bigGrin', 'laugh', 'smug']   # four ways to be pleased
st.shot('S14', 'holeSection', actors=[act(w, [x, 0, z], 0, 'squeezed', 'surprised', params={'look': -x * 0.5, 'ph': ph}, keys=[k(0.0, toon=SQ, toonDur=0), k(T14 + i * 0.05, expr=GRIN14[i], toon={**SQ, 'sq': [0.74, 1.2 + 0.05 * (i % 2), 0.9], 'face': EUR}, toonDur=0.1), k(T14 + i * 0.05 + 0.14, toon={**SQ, 'face': EUR}, toonDur=0.2)])
        for i, (w, x, z, lk, e, ph) in enumerate(ROW)],
        props=[P('bill', 'taxBill', pos=[0.0, 1.42, 0.75], rot=[-0.08, 0, 0.03], scale=1.0)],
        cams=[cam(0.0, [0.05, 1.78, 3.75], [0.04, 1.78, 3.55], [0, 1.74, 0.1], [0, 1.74, 0.1], lens=44)])
# 15: so the whole town jumped in: an orderly queue; one after the other they run up, hang over the hole in their own pose and drop; the queue moves up
#     one place each time (seen from the side, each silhouette on the plain facade)
STEP = 0.9
Q0 = [(8.5, -3.3), (8.6, -4.2), (8.7, -5.1)]
JUMP = [('c1', 0.0, 'noseJump', 0.25), ('c2', 0.3, 'cannonball', 0.4), ('c3', 0.6, 'swanDive', 0.3)]
def jumper(i, w, t0, c, h):
    ks = [k(JUMP[j][1], to=[Q0[i - j - 1][0], 0, Q0[i - j - 1][1]], dur=0.22, clip='walk', ease='inOut') for j in range(i)]   # shuffle up one place per jump before his turn
    ks += [k(t0, to=[7.6, 0, -1.25], dur=0.2, clip='run', ease='linear'), k(t0 + 0.2, to=[HX, 0.6, HZ], dur=0.2, clip=c, arc=h, ease='out', then=c, blend=0.06), k(t0 + 0.47, to=[HX, -5.0, HZ], dur=0.16, glide=True, ease='in', face='keep')]
    return act(w, [Q0[i][0], 0, Q0[i][1]], 0, 'idle', 'bigGrin', keys=ks)
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[jumper(i, *j) for i, j in enumerate(JUMP)],
        props=[DUST('d15a', [HX, -0.35, 0.1], 0.66, 0.4, 0.6), DUST('d15b', [HX, -0.35, 0.1], 0.96, 0.4, 0.6, seed=3),
               P('queue', 'queueFigures', pos=[0, 0, 0], opts={'path': [[8.8, -6.0], [9.0, -44]], 'people': True, 'gap': 0.85, 'size': 1.2, 'seed': 5},
                 keys=[k(t0, to=[0.03 * (n + 1), 0, STEP * (n + 1)], dur=0.24, arc=0.07, ease='inOut') for n, (_, t0, _, _) in enumerate(JUMP)])],
        cams=[cam(0.0, [2.1, 1.4, 2.7], [2.3, 1.4, 2.5], [HX + 0.3, 1.2, -0.8], [HX + 0.3, 1.15, -0.7], lens=46)])
# 16: seen from below: it rains citizens. Each one arrives in the pose he left with (feet first holding his nose, in a ball, head first: that one sticks),
#     everybody underneath is pressed a little flatter each time, the column climbs out of the shaft
T16 = [0.14, 0.32, 0.5, 0.7]                      # the landings (c1, c2, c3, then c4 and c5 together)
SY0 = [1.08, 1.0, 0.92, 0.84, 0.74]                # the bottom row, flatter after each landing
SQN = lambda sy, w0=0.74: {'sq': [round(w0 * (1.08 / sy) ** 0.5, 3), round(sy, 3), 0.9]}
Y2 = lambda sy: round(2.0 * sy, 3)                 # where the second storey stands (on the shoulders of the first)
def press(seq, first=0):
    """the keys of somebody who is landed on: a dip on each hit, a small rebound (toon sq), from landing number `first` on"""
    ks = []
    for n in range(first, len(T16)):
        ks += [k(T16[n], toon=SQN(seq[n + 1] - 0.1), toonDur=0.04, toonEase='out'), k(T16[n] + 0.05, toon=SQN(seq[n + 1]), toonDur=0.09, toonEase='inOut')]
    return ks
def ride(x, z, first):
    """the moves of somebody standing on the bottom row: he goes down with it at each later landing"""
    ks = []
    for n in range(first, len(T16)):
        ks += [k(T16[n], to=[x, Y2(SY0[n + 1] - 0.1), z], dur=0.04, glide=True, ease='out', face='keep'), k(T16[n] + 0.05, to=[x, Y2(SY0[n + 1]), z], dur=0.09, glide=True, ease='inOut', face='keep')]
    return ks
SY2 = [1.08, 1.08, 1.08, 1.08, 0.88]               # the second storey is pressed by the third
C1X, C2X, C3X = -0.5, 0.0, 0.52
st.shot('S16', 'holeSection', actors=[act(w, [x, 0, z], 0, 'squeezed', 'scared', params={'look': lk, 'ph': ph}, keys=[k(0.0, clip='lookUp', toon=SQ, toonDur=0)] + press(SY0)) for w, x, z, lk, e, ph in ROW] + [
        act('c1', [C1X, 7.5, 0.1], 0, 'noseJump', 'puffed', keys=[k(0.0, visible=False), k(T16[0] - 0.14, visible=True), k(T16[0] - 0.14, to=[C1X, Y2(SY0[1] - 0.1), 0.1], dur=0.14, glide=True, ease='linear', face='keep'),
            k(T16[0], clip='squeezed', expr='relieved', blend=0.08), k(T16[0], toon={'sq': [0.95, 0.72, 0.95]}, toonDur=0.03), k(T16[0] + 0.05, toon=SQ, toonDur=0.1)] + ride(C1X, 0.1, 0)[1:] + press(SY2, 3)),
        act('c2', [C2X, 7.5, 0.25], 0, 'airborne', 'laugh', keys=[k(0.0, visible=False), k(T16[1] - 0.14, visible=True), k(T16[1] - 0.14, clip='cannonball', blend=0.001), k(T16[1] - 0.14, to=[C2X, Y2(SY0[2] - 0.1), 0.25], dur=0.14, glide=True, ease='linear', face='keep'),
            k(T16[1], clip='squeezed', expr='bigGrin', blend=0.12), k(T16[1], toon={'sq': [1.25, 0.55, 1.25]}, toonDur=0.03), k(T16[1] + 0.05, toon=SQ, toonDur=0.12)] + ride(C2X, 0.25, 1)[1:] + press(SY2, 3)),
        act('c3', [C3X, 8.2, 0.42], 0, 'swanDive', 'bigGrin', params={'k': 1}, keys=[k(0.0, visible=False), k(T16[2] - 0.14, visible=True), k(T16[2] - 0.14, to=[C3X, 2.3 * SY0[3] - 0.15, 0.42], dur=0.14, glide=True, ease='linear', face='keep'),
            k(T16[2], clip='headStuck', expr='dizzy', blend=0.02), k(T16[3], to=[C3X, 2.3 * (SY0[4] - 0.1) - 0.15, 0.42], dur=0.04, glide=True, ease='out', face='keep'), k(T16[3] + 0.05, to=[C3X, 2.3 * SY0[4] - 0.15, 0.42], dur=0.09, glide=True, ease='inOut', face='keep')]),
        act('c4', [C1X - 0.02, 9.5, 0.2], 0, 'fallDrag', 'scared', keys=[k(0.0, visible=False), k(T16[3] - 0.14, visible=True), k(T16[3] - 0.14, to=[C1X - 0.02, Y2(SY0[4]) + 2.0 * SY2[4], 0.2], dur=0.14, glide=True, ease='linear', face='keep'),
            k(T16[3], clip='squeezed', expr='pain', blend=0.05), k(T16[3], toon={'sq': [0.95, 0.7, 0.95]}, toonDur=0.03), k(T16[3] + 0.05, toon=SQ, toonDur=0.12)]),
        act('c5', [C2X + 0.1, 9.5, 0.35], 0, 'fallDrag', 'scared', keys=[k(0.0, visible=False), k(T16[3] - 0.11, visible=True), k(T16[3] - 0.11, to=[C2X + 0.1, Y2(SY0[4]) + 1.32 * SY2[4], 0.35], dur=0.14, glide=True, ease='linear', face='keep'),
            k(T16[3] + 0.03, clip='squeezed', expr='pain', blend=0.05), k(T16[3] + 0.03, toon={'sq': [0.95, 0.7, 0.95]}, toonDur=0.03), k(T16[3] + 0.08, toon=SQ, toonDur=0.12)])],
        fx=[{'type': 'shake', 'at': t, 'dur': 0.12, 'amount': 0.022} for t in T16],
        cams=[cam(0.0, [0.1, 2.6, 9.3], [0.1, 2.9, 9.5], [0, 2.6, 0], [0, 3.0, 0], lens=44)])
# 17: today: a hole full to the brim, a sign, a latecomer with his suitcase
FULL = [('mec', [HX - 0.3, -1.5, 0.4], 15, 'squeezed', 'unimpressed'), ('agent', [HX + 0.5, -1.4, -0.1], -25, 'squeezed', 'worried'), ('pompier', [HX - 0.65, -1.3, -0.15], 30, 'squeezed', 'sad'), ('maire', [HX + 0.55, -1.25, -0.6], -15, 'royalWave', 'teeth'),
        ('c1', [HX + 0.45, -1.75, 0.45], -30, 'squeezed', 'bigGrin'), ('c3', [HX + 0.08, -1.9, 0.6], -5, 'squeezed', 'happy')]
SIGN = lambda at_: P('sign', 'completSign', pos=[7.0, 0, -1.55], ry=-22, opts={'onAt': at_, 'h': 1.85, 'w': 1.1})
LATE = [8.15, 0, -0.35]
CAM18 = [5.0, 1.85, 4.45]
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[act(w, p, ry, c, e, params={'ph': i * 1.3}, keys=[k(0.3 + 0.06 * i, look='late')]) for i, (w, p, ry, c, e) in enumerate(FULL)] +
        [act('late', [9.5, 0, -8.5], 0, 'run', 'bigGrin', keys=[k(0.1, to=LATE, dur=0.75, clip='run', then='skidStop', thenParams={'dur': 0.25, 'expr': 'surprised'})])],
        props=[SIGN(99), P('case', 'briefcase', on={'actor': 'late', 'hand': 'L'})],
        cams=[cam(0.0, [4.75, 2.0, 5.0], [4.85, 1.95, 4.8], [HX + 0.25, 1.1, -0.6], [HX + 0.25, 1.1, -0.6], lens=40)])
# 18: COMPLET. The latecomer melts from the top down, his hat left in the air for a moment; the pile looks at him; a neck comes up like a hose to have a
#     look at the puddle, then at us; so does everybody
T18 = st.at('S18', 'L12', 4)
M18, MD = round(T18 + 0.15, 3), 0.45               # the melt and its length
HAT18 = M18 + MD + 0.1                             # the hat lets go
N18 = round(HAT18 + 0.26, 3)                       # the neck comes up
US18 = round(N18 + 0.62, 3)                        # everybody looks at us
def pile(i, w):
    if w == 'mec': return [k(0.0, look='late'), k(M18 + 0.2, look=[LATE[0], 0.3, LATE[2]]), k(N18, clip='hoseNeck', params={'len': 8.5, 'sway': 0.5}, expr='deadpan', blend=0.05), k(US18, look=CAM18)]
    return [k(0.0, look='late'), k(M18 + 0.16 + 0.05 * i, look=[LATE[0], 0.3, LATE[2]]), k(US18 + 0.06 + 0.05 * i, look=CAM18)]
st.shot('S18', 'parisStreet', setOpts=STREET, actors=[act(w, p, ry, c, e, params={'ph': i * 1.3}, keys=pile(i, w)) for i, (w, p, ry, c, e) in enumerate(FULL)] +
        [act('late', LATE, -25, 'stand', 'surprised', keys=[k(0.0, look='sign'), k(T18 + 0.05, expr='shocked'), k(M18, look=None, clip='meltDown', params={'dur': MD, 'spread': 0.7, 'landAt': HAT18 + 0.14 - M18}, expr='cry', blend=0.05), k(M18, toon={'hat': [60, 0, 0]}, toonDur=0)])],
        props=[SIGN(T18), P('case', 'briefcase', on={'actor': 'late', 'hand': 'L'}, keys=[k(M18 + 0.12, detach=True, fall=True, floor=0.02)]),
               P('hat', 'fedoraHat', pos=[LATE[0], 2.31, LATE[2]], ry=-25, keys=[k(0.0, visible=False), k(M18, visible=True), k(HAT18 - 0.1, rotTo=[0, -0.44, 0.2], dur=0.1), k(HAT18, to=[LATE[0] + 0.02, 0.5, LATE[2] + 0.1], dur=0.14, ease='in')])],
        cams=[cam(0.0, [4.85, 1.95, 4.8], CAM18, [HX + 0.25, 1.1, -0.6], [HX + 0.25, 1.25, -0.6], lens=40)])

# sound on the actions: steps that stop when the ground does, a slide whistle for every fall, wood and rubber for the gags
for t in (0.08, 0.3): st.cue('sfx:stepSoft', 'S01', t, 0.5)   # two steps on the pavement, then none: he is on the air
st.cue('sfx:gulp', 'S02', 0.52, 0.45); st.cue('sfx:stretch', 'S02', D2, 0.45); st.cue('sfx:slideDown', 'S02', D2 + 0.2, 0.55); st.cue('sfx:slideDown', 'S02', D2 + 0.5, 0.25)
st.cue('sfx:splat', 'S03', 0.12, 0.5); st.cue('sfx:spring', 'S03', POP3, 0.4); st.cue('sfx:bonk', 'S03', 0.74, 0.42); st.cue('sfx:beep', 'S03', 1.06, 0.2)
st.cue('sfx:ring', 'S04', 0.0, 0.16); st.cue('sfx:stretch', 'S04', HIT4 - 0.4, 0.3); st.cue('thud', 'S04', HIT4, 0.55); st.cue('pop', 'S04', HIT4 + 0.06, 0.3)
st.cue('sfx:tick', 'S05', st.at('S05', 'L04', 2), 0.3); st.cue('sfx:tick', 'S05', st.at('S05', 'L04', 2) + 0.22, 0.3); st.cue('sfx:slideUp', 'S05', T5 - 0.1, 0.3); st.cue('sfx:gasp', 'S05', T5 + 0.03, 0.4)
for t in (0.2, 0.55, 0.9, 1.25): st.cue('sfx:step', 'S06', t, 0.4)
st.cue('sfx:tick', 'S06', 1.6, 0.35)
st.cue('sfx:stretch', 'S07', E7, 0.4); st.cue('sfx:twang', 'S07', B7, 0.32); st.cue('sfx:slideDown', 'S07', D7, 0.55); st.cue('sfx:slideDown', 'S07', D7 + 0.3, 0.22)
st.cue('sfx:zip', 'S08', 0.0, 0.45); st.cue('sfx:brake', 'S08', 0.32, 0.4); st.cue('whoosh', 'S08', 0.58, 0.24, 0.5, 500, 2500)
st.cue('sfx:slideDown', 'S09', -0.28, 0.5); st.cue('sfx:splat', 'S09', 0.14, 0.42); st.cue('sfx:twang', 'S09', 0.17, 0.38)
for t in (0.14, 0.42, 0.7): st.cue('sfx:stepHeavy', 'S10', t, 0.4)
st.cue('sfx:slideDownSlow', 'S10', G10 + 0.05, 0.42); st.cue('sfx:zip', 'S10', END10 - 0.08, 0.25)
for t in (0.05, 0.2, 0.35, 0.5): st.cue('pop', 'S11', t, 0.3)
for i in range(4): st.cue('sfx:stretch', 'S12', 0.1 + 0.08 * i, 0.3)
st.cue('sfx:poof', 'S12', 0.68, 0.4)
st.cue('sfx:paper', 'S13', 0.0, 0.3); st.cue('sfx:stretch', 'S13', A13, 0.45); st.cue('sfx:twang', 'S13', B13 + 0.04, 0.34)
st.cue('sfx:cash', 'S14', T14, 0.6)
for _, t0, _, _ in JUMP: st.cue('sfx:slideUp', 'S15', t0 + 0.2, 0.22); st.cue('sfx:slideDown', 'S15', t0 + 0.47, 0.3); st.cue('sfx:poof', 'S15', t0 + 0.63, 0.3)
st.cue('whoosh', 'S15', 0.0, 0.2, 0.9, 300, 1500)
for t in T16: st.cue('thud', 'S16', t, 0.42); st.cue('sfx:squeak', 'S16', t + 0.02, 0.4)
st.cue('sfx:twang', 'S16', T16[2] + 0.03, 0.3)
st.cue('sfx:stepRun', 'S17', 0.3, 0.4); st.cue('sfx:stepRun', 'S17', 0.5, 0.4); st.cue('sfx:stepRun', 'S17', 0.7, 0.4); st.cue('sfx:brake', 'S17', 0.82, 0.35)
st.cue('clack', 'S18', T18, 0.5); st.cue('sfx:beep', 'S18', T18 + 0.02, 0.25); st.cue('sfx:slideDownSlow', 'S18', M18, 0.26); st.cue('sfx:poof', 'S18', HAT18 + 0.14, 0.3); st.cue('sfx:stretch', 'S18', N18, 0.4)

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
    'c1': CITIZEN('mamie', 17), 'c2': CITIZEN('gamin', 19, build={'height': 0.66}, suit='#D9482B', pants='#D9482B'), 'c3': CITIZEN('chef', 22), 'c4': CITIZEN('sportif', 23, skin='#8A5A3C', suit='#7A3FA0', pants='#7A3FA0'), 'c5': CITIZEN('serveur', 26),
    'late': CITIZEN('tourist', 29)})
