#!/usr/bin/env python3
"""Les lunettes (story 69, cycle 31; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man lost his glasses. He looked everywhere. Under the sofa. In the fridge. He filed a complaint. The police searched the whole district. Divers
drained the river. The army sent helicopters. Satellites scanned the planet. The other countries sent their dogs. The government promised a million
euros. The whole world searched for a year. Yesterday a child found them. On his head. The child got the million. The man is looking for his keys.
Running gag (dramatic irony): the glasses sit pushed up on his head in every shot, in plain sight of everyone and of us; they glint now and then.
Staging: close, squinting, he pats his pockets; he throws the cushions of his sofa over his shoulder; on his knees he peers under the sofa; his head
in the fridge in the cold mist; at the police desk he mimes glasses round his eyes for the officer, who looks straight at the glasses on his head;
policemen with binoculars and a dog search the street, one with his head in a bin (FOUILLE); divers in masks dig the mud of a drained river, a fish
flopping; at night a helicopter's searchlight sweeps over him and the glasses flash; a satellite scans the Earth with a red fan; dogs of every colour
sniff round him, one sits and stares up at his head, tilts it, and goes on sniffing; a minister at a podium, a reward poster pops up (MILLION); an
office searched from top to bottom while a wall calendar sheds twelve months; a boy tugs his sleeve and points up; his eyes roll up to his head, the
glasses flash, his eyes pop (TROUVÉES); the boy holds up a giant cheque; he pats every pocket, his key ring hanging from his own mouth.
Natural look; cycle 31: props_lunettes.js (bigGlasses with glints, helicopter with a searchlight, satellite with a scan fan, diveMask, drainedRiver,
rewardPoster), bigFridge mist, monthCalendar, bigCheque, keyRing."""
from story_kit import *
import math

st = Story('lunettes', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L08', 0),
         ('S09', 'L09', 0), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L11', 4), ('S13', 'L12', 0), ('S14', 'L13', 0), ('S15', 'L14', 0), ('S16', 'L15', 0),
         ('S17', 'L16', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
SQUINT = {'lid': 0.35, 'low': 0.3, 'brow': -0.35, 'mouth': 'pout'}       # without his glasses: he squints
def GL(pid, glint=(), fc=0.0, s=1.0, tap=(), off=(0.0, 0.6, 0.045), lens=None, rot=None, dx=None, r_=None, keys=None):
    # pushed up on top of his head in every shot; (stills 1) at 0.47 they sat on his brow and read as worn. (pass 3) fc: how far they turn to the camera
    # (0..1: upright on a head seen in profile they went edge-on, black on black hair, review 2); tap [t, ...]: knocked, they rock; thicker rims
    # (final pass) rot: a roll on the head ([0, 0, rz]); dx / r_: the lenses' spacing and radius; keys: visibility keys (one pair swapped for another)
    on = {'actor': 'mec', 'joint': 'head', 'offset': list(off), **({'rot': list(rot)} if rot else {})}
    if fc: on.update({'face': 'camera', 'faceAmt': fc})
    return P(pid, 'bigGlasses', on=on, scale=s, opts={'glint': list(glint), 'tap': list(tap), 'rim': 0.26, **({'lens': lens} if lens is not None else {}), **({'dx': dx} if dx else {}), **({'r': r_} if r_ else {})},
             **({'keys': keys} if keys else {}))
DOGC = [{'body': '#C99A62', 'collar': '#2F62B5'}, {'body': '#3B2E26', 'collar': '#E0413A'}, {'body': '#E8E2D6', 'collar': '#2F8F6B'}, {'body': '#8A6A4A', 'collar': '#F2C94E'}]

for g_ in [('S01', 1.0, 'mec', 'squint'), ('S05', 0.8, 'mec', 'mime'), ('S10', 1.2, 'chien1', 'stare'), ('S14', 1.2, 'gamin', 'point'), ('S15', 0.6, 'mec', 'found'),
           ('S17', 1.2, 'mec', 'keys')]:
    st.gag(*g_)
st.card('S06', 'FOUILLE', at=0.5)
st.card('S12', 'MILLION', at=0.3)
st.card('S15', 'TROUVÉES', at=0.55)   # (review 1) on the pop, not before the glint


# 1: the hook. Close in his living room: squinting at nothing, he pats his shirt pocket, his trouser pockets, looks left and right; the glasses sit
#    on his head all along and glint once
D1 = st.dur('S01'); ME = [0.0, 0, 0.0]
POCK = lambda side, y: {'touch': {side: ['torso', (-0.1 if side == 'R' else 0.1), y, 0.12, 1, 0.02]}, 'hands': {side: 'open'}}
st.shot('S01', 'livingRoom', actors=[
        act('mec', ME, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': SQUINT}, toonDur=0.0),
            k(0.2, toon={**POCK('R', 0.42), 'face': SQUINT}, toonDur=0.12, toonEase='out'), k(0.45, toon={**POCK('L', 0.42), 'face': SQUINT}, toonDur=0.12, toonEase='out'),   # the shirt pockets...
            k(0.7, look=[-1.5, 2.0, 1.0]), k(0.7, toon={**POCK('R', -0.05), 'face': SQUINT}, toonDur=0.12, toonEase='out'), k(0.95, look=[1.5, 2.0, 1.0]), k(0.95, toon={**POCK('L', -0.05), 'face': SQUINT}, toonDur=0.12, toonEase='out'),   # ...the trousers, a look each side...
            k(1.25, look='camera'), k(1.25, toon={'face': {**SQUINT, 'brow': 0.3, 'mouth': 'line'}}, toonDur=0.15)])],   # ...nothing
        props=[GL('gl1', glint=[1.15])],
        cams=[FC(0.0, [0.3, 2.15, 1.4], [[0.0, 2.85, 0.0], [0.0, 1.55, 0.0], [0.35, 2.2, 0.1], [-0.35, 2.2, 0.1]], top=0.14, bottom=0.74)])
st.cue('sfx:stepSoft', 'S01', 0.2, 0.1); st.cue('sfx:stepSoft', 'S01', 0.45, 0.1); st.cue('sfx:ding', 'S01', 1.15, 0.15)

# 2: he looked everywhere. Wide on the living room: bent over the sofa he throws its cushions over his shoulder one after another; they fly across the
#    room in arcs, a sock and a book after them. (final pass, review 3: we saw the sofa's plain back, a teal slab over the bottom third, and flat brick
#    cushions: a man throwing things behind a counter) the sofa turned to us, seat, arms and back cushions in view, a little from above; he is
#    bent over its back, digging in the seat; the cushions are puffy
D2 = st.dur('S02'); ME2 = [0.2, 0, -2.2]; SOFA2 = [0.2, 0, -1.45]   # (build) facing us behind a sofa: his face, not his back
THROW = lambda j: [k(r(0.12 + 0.3 * j), toon={'reach': {'R': [0.25, 0.75, -1.6, 1, 0.04]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.7, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'open', 'brow': 0.7}}, toonDur=0.1, toonEase='in'),
                   k(r(0.26 + 0.3 * j), toon={'reach': {'R': [0.45, 2.75, -2.5, 1, 0.04]}, 'hands': {'R': 'open'}, 'bend': {'spine': [-0.1, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'open', 'brow': 0.7}}, toonDur=0.07, toonEase='out')]
FLY2 = [('cush1', 'puffCushion', [0.25, 0.7, -1.4], {'w': 0.5, 'h': 0.42, 'd': 0.2, 'color': '#E07A5F'}, 0.26, [-0.6, 3.3, -2.8], [-1.9, 0.2, -3.3]),
        ('cush2', 'puffCushion', [0.55, 0.7, -1.4], {'w': 0.5, 'h': 0.42, 'd': 0.2, 'color': '#F2C94E'}, 0.56, [1.0, 3.4, -2.9], [2.3, 0.2, -3.3]),
        ('sock2', 'slab', [0.0, 0.62, -1.55], {'w': 0.25, 'h': 0.06, 'd': 0.1, 'color': '#F2F2EE'}, 0.86, [-0.2, 3.5, -2.8], [-0.9, 0.05, -3.4]),
        ('book2', 'slab', [0.4, 0.62, -1.55], {'w': 0.3, 'h': 0.06, 'd': 0.22, 'color': '#2F62B5'}, 1.16, [0.6, 3.5, -2.9], [1.4, 0.05, -3.4])]
K2 = [k(0.0, look=[0.3, 0.6, -1.5]), k(0.0, toon={'bend': {'spine': [0.6, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'open'}}, toonDur=0.0)]
for j in range(4): K2 += THROW(j)
st.shot('S02', 'livingRoom', setOpts={'sofa': False}, actors=[act('mec', ME2, 0, 'stand', 'neutral', keys=K2 + [k(1.3, look='camera')])],
        props=[GL('gl2'), P('sofa2', 'sofaProp', pos=SOFA2, ry=0), *[P(pid, kind, pos=p0, opts=o, keys=[k(r(t0 - 0.02), to=mid, dur=0.22, ease='out'), k(r(t0 + 0.2), to=end, dur=0.28, ease='in'),
                                                                 k(r(t0 - 0.02), rot=[2.5, 1.5, 0.8], dur=0.5, ease='linear')]) for pid, kind, p0, o, t0, mid, end in FLY2]],
        cams=[FC(0.0, [0.9, 2.05, 1.6], [[0.2, 2.9, -2.2], [0.2, 0.42, -1.2], [-0.6, 3.4, -2.8], [1.0, 3.4, -2.9]], top=0.1, bottom=0.8)])   # (final pass) a little from above: the seat and its cushions read
for j in range(4): st.cue('whoosh', 'S02', r(0.26 + 0.3 * j), 0.2, 0.25, 500, 1500)

# 3: under the sofa. The camera under the sofa at floor level, looking out (review 1: from the side he read as a headless navy arch): the dark
#    underside frames the top, a coin, a sock and dust in front; he kneels bent right down, cheek to the floor, squinting into the dark, the glasses
#    on his head against the bright room; he looks left, right, blinks, then at us
D3 = st.dur('S03'); ME3 = [0.0, 0, -0.55]; SOFA3 = [0.0, 0, -2.2]   # (stills 7) a step back: his face filled the whole frame
LOW3 = lambda f, sq=(1.08, 0.62, 1.08): {'bend': {'spine': [1.25, 0, 0, 1, None], 'neck': [-0.55, 0, 0, 1, None]}, 'face': f, 'sq': list(sq)}   # (stills 6) squashed flat to the floor: bent, his head stayed at 0.73 m, over the gap
st.shot('S03', 'livingRoom', actors=[
        act('mec', ME3, 180, 'peerIn', 'neutral', keys=[k(0.0, look=[0.0, 0.2, -2.6]), k(0.0, toon=LOW3({**SQUINT, 'mouth': 'O'}), toonDur=0.0),
            k(0.3, look=[-0.6, 0.2, -2.6]), k(0.62, look=[0.6, 0.2, -2.6]), k(0.55, toon=LOW3({**SQUINT, 'mouth': 'pout'}, (1.1, 0.6, 1.1)), toonDur=0.2),
            k(0.85, toon=LOW3({**SQUINT, 'lid': 1.0, 'mouth': 'pout'}), toonDur=0.05), k(0.95, toon=LOW3({**SQUINT, 'mouth': 'pout'}), toonDur=0.07), k(r(D3 - 0.38), look='camera')])],
        props=[GL('gl3'), P('sofa3', 'sofaProp', pos=SOFA3, ry=0, opts={'legs': 0.46}), P('coin3', 'coin', pos=[0.16, 0.02, -2.05], rot=[PI / 2, 0, 0], scale=1.6),
               P('sock3', 'slab', pos=[-0.22, 0.03, -1.98], ry=25, opts={'w': 0.25, 'h': 0.05, 'd': 0.1, 'color': '#F2F2EE'}),
               P('dust3', 'dustPuff', pos=[0.3, 0.0, -1.9], scale=0.15, opts={'color': '#BDB4A6', 'period': 1.1})],
        cams=[FC(0.0, [0.06, 0.12, -1.93], [[0.0, 0.95, -1.2], [0.0, 0.0, -1.6], [-0.32, 0.55, -1.2], [0.32, 0.55, -1.2]], top=0.3, bottom=0.8, inside=(-0.8, 0.8, 0.05, 0.4, -2.6, -1.92), lenses=range(26, 86))])   # (stills 6) just behind the front edge: from deeper under, the rail hid his head
st.cue('sfx:scratch', 'S03', 0.35, 0.15)

# 4: in the fridge. The camera inside the fridge behind the food, looking out (review 1: from outside his head stayed in the fridge). (pass 3, review 2:
#    five beats in 1.17 s and the two that mattered hidden) two beats only: his face comes in between the shelves, squinting left and right, the
#    glasses on his head in the clear (no mist: its puffs sat on the lens as a pink dome); then one jolt of cold: a stretch straight into a squashed
#    pose, hair on end, teeth chattering, held to the cut. (final pass, review 3: no shelf, no food, no door edge: an empty kitchen; the squash took his
#    face out of the bottom of the frame; the glasses sank among the spikes) the fridge's own walls and door edge frame him left and right, a glass
#    shelf with a milk carton, a jar and a cheese along the bottom, cool blue light on his face; a smaller squash that keeps his chin above the
#    captions; when his hair shoots up the glasses ride up on the tips of the spikes; his breath puffs white
D4 = st.dur('S04'); FR4 = [0.0, 0, -2.4]; FR4F = [0.21, 0, -2.4]; IN4 = [0.1, 0, -1.12]; JOLT4 = 0.4   # (stills r3a) a step back: at -1.4 his face filled the lens and the shelf above the camera hid the glasses
IN4P = lambda f, sq=None, hair=0.0: {'bend': {'spine': [0.5, 0, 0, 1, None]}, 'face': f, **({'sq': list(sq)} if sq else {}), **({'hairUp': hair} if hair else {})}
COLD4 = {'lid': 0.0, 'eye': 0.45, 'mouth': 'zigzag', 'tremble': 1.0, 'brow': 0.8, 'pupilShake': 1.0, 'noBlink': 1}
st.shot('S04', 'kitchenDay', setOpts={'fridge': False}, actors=[
        act('mec', IN4, 180, 'peerIn', 'neutral', keys=[k(0.0, look=[0.1, 1.0, -2.8]), k(0.0, toon=IN4P(SQUINT), toonDur=0.0), k(0.14, look=[-0.3, 1.0, -2.8]), k(0.27, look=[0.35, 1.0, -2.8]), k(JOLT4, look='camera'),
            k(JOLT4, toon=IN4P({'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}, (0.88, 1.16, 0.88), 1.0), toonDur=0.05, toonEase='out'),   # the cold: a stretch...
            k(r(JOLT4 + 0.1), toon=IN4P(COLD4, (1.24, 0.9, 1.24), 1.0), toonDur=0.06, toonEase='in'),                                                 # ...into the squash, hair on end (final pass: 0.9, at 0.8 his chin sank into the captions)...
            *[k(r(JOLT4 + 0.22 + 0.07 * j), toon=IN4P(COLD4, (1.14 + 0.05 * (j % 2), 0.93, 1.14 + 0.05 * (j % 2)), 1.0), toonDur=0.06) for j in range(8)]])],   # ...and he shivers there to the cut
        props=[P('fr4', 'bigFridge', pos=FR4F, opts={'w': 0.5, 'open': 1.0, 'mode': 'lived', 'mist': False, 'light': True}),   # (final pass) a narrower cabin: its walls and the door edge now frame him (at 1.04 m they sat outside the lens)
               GL('gl4', glint=[0.2], fc=0.7, keys=[k(0.0, visible=True), k(r(JOLT4 + 0.04), visible=False)]),
               GL('gl4b', fc=0.8, s=1.1, off=(-0.07, 0.66, 0.16), tap=[r(JOLT4 + 0.05)], keys=[k(0.0, visible=False), k(r(JOLT4 + 0.04), visible=True)]),   # lifted by the spikes and pushed out in front of them (stills: on the tips they left the frame; black rims among black spikes vanish)
               P('shelf4', 'slab', pos=[0.21, 0.71, -2.17], opts={'w': 0.5, 'h': 0.018, 'd': 0.4, 'color': '#E4F4FA', 'outline': 0.004}),
               P('shelf4f', 'slab', pos=[0.21, 0.71, -1.98], opts={'w': 0.5, 'h': 0.03, 'd': 0.025, 'color': '#FFFFFF'}),
               P('lait4', 'milkCarton', pos=[0.43, 0.72, -2.18], ry=200), P('fromage4', 'cheeseWheel', pos=[0.0, 0.72, -2.12], ry=150, scale=0.55),
               P('bocal4', 'picklesJar', pos=[0.36, 0.72, -2.05], opts={'s': 0.7}),   # (stills) to the side and smaller: in the middle it hid his collar; (stills) no glow light here: by the lens it washed the frame white
               P('souffle4', 'dustPuff', pos=[0.1, 1.02, -1.86], scale=0.06, opts={'color': '#EEF6FF', 'startAt': r(JOLT4 + 0.25), 'period': 0.45, 'seed': 4})],
        cams=[FC(0.0, [0.25, 1.05, -2.76], [[0.1, 1.72, -1.72], [0.1, 0.7, -1.72], [-0.28, 1.1, -1.72], [0.48, 1.1, -1.72]], top=0.14, bottom=0.8, inside=(-0.45, 0.45, 0.86, 1.2, -2.78, -2.3), lenses=range(26, 86))])
st.cue('sfx:click', 'S04', 0.05, 0.15); st.cue('sfx:ding', 'S04', 0.2, 0.15); st.cue('whoosh', 'S04', JOLT4, 0.2, 0.25, 600, 1500); st.cue('sfx:sniff', 'S04', r(JOLT4 + 0.3), 0.2)

# 5: he filed a complaint. (pass 3, review 2: over the officer's shoulder the officer was a cap and the look up at the glasses did not read; fists over
#    the eyes read as rubbing them) from the front, three-quarters on both: the officer behind his desk, writing; the man at the end of the desk mimes
#    glasses, a ring of thumb and finger in front of each wide eye, twice; the officer's eyes go up to the glasses on his head (glint), hold there,
#    go back down, and he writes. (final pass, review 3: both hands bunched into one fist in front of his face, which read as rubbing his eyes; the
#    officer looked level at his chest; the glint sat on the POLICE sign) he turns almost to us, elbows out wide, a ring of thumb and finger held in
#    front of each wide-open eye (his crooked face: the right eye high, the left one low), twice, his face clear between his hands; the officer
#    tips his head back and his pupils go right up to the glasses for a held beat; the sign moved off behind the glint
D5 = st.dur('S05'); ME5 = [-1.75, 0, -2.3]; OFF5 = [-2.7, 0, -2.75]; GLP5 = [ME5[0], 2.35, ME5[2]]
OKH = [0.62, 0.05, 0.05, 0.05, 0.85, 0.55]   # (final pass) a ring of thumb and index, the other fingers up and fanned (« glasses »)
# (final pass) each ring right in front of its eye, the hands out at the sides of the face (elbows out), a small circle; wide open eyes, not the squint
RING5 = lambda a, b=0.5: {'touch': {'R': ['face', r(-0.42 - 0.07 * math.cos(a)), r(0.68 + 0.06 * math.sin(a)), 0.22, 1, 0.0, [-0.9, -0.2, 0.2]], 'L': ['face', r(0.42 + 0.07 * math.cos(a)), r(0.68 + 0.06 * math.sin(a)), 0.22, 1, 0.0, [0.9, -0.2, 0.2]]},   # (stills) level: at his crooked eyes' own heights the low hand read as a hand at his mouth
                          'hands': {'R': OKH, 'L': OKH}, 'face': {'lid': 0.0, 'low': 0.0, 'eye': 0.35, 'brow': b, 'mouth': 'o', 'noBlink': 1}}
st.shot('S05', 'policeStation', actors=[
        act('mec', ME5, -12, 'stand', 'neutral', keys=[k(0.0, look=[-2.1, 1.75, 0.2]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(0.08, toon=RING5(PI / 2), toonDur=0.1, toonEase='out'),
            *[k(r(0.18 + 0.075 * j), toon=RING5(PI / 2 + (j + 1) * PI / 2, r(0.35 + 0.35 * (j % 2))), toonDur=0.075, toonEase='linear') for j in range(4)],   # glasses!...
            k(0.5, toon={'touch': {'R': ['face', -0.42, 0.62, 0.2, 1, 0.0], 'L': ['face', 0.4, 0.45, 0.2, 1, 0.0]}, 'hands': {'R': OKH, 'L': OKH}, 'face': {'lid': 0.0, 'eye': 0.35, 'brow': 0.8, 'mouth': 'O', 'noBlink': 1}}, toonDur=0.08),   # (a pump)
            *[k(r(0.6 + 0.075 * j), toon=RING5(PI / 2 + (j + 1) * PI / 2, r(0.45 + 0.35 * (j % 2))), toonDur=0.075, toonEase='linear') for j in range(4)],   # ...glasses!
            k(1.02, toon={'face': {**SQUINT, 'brow': 0.3, 'mouth': 'line'}}, toonDur=0.14)]),
        act('flic', OFF5, 0, 'sitWrite', 'unimpressed', keys=[k(0.0, look=[-2.6, 0.9, -2.1]), k(0.0, toon={'face': {'lid': 0.5, 'gy': 0.6, 'mouth': 'line'}}, toonDur=0.0),
            k(0.28, look=[GLP5[0], r(GLP5[1] + 0.1), GLP5[2]], lookDur=0.16), k(0.28, toon={'bend': {'neck': [-0.3, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.3, 'gy': -1.0, 'gx': 0.7, 'brow': 0.45, 'mouth': 'line', 'noBlink': 1}}, toonDur=0.14),   # up to the glasses (final pass: the head tips back and the pupils go right up)...
            k(0.9, look=[-2.6, 0.9, -2.1], lookDur=0.14), k(0.9, toon={'face': {'lid': 0.5, 'gy': 0.6, 'mouth': 'line'}}, toonDur=0.12)])],                                      # ...a hold, and back to his form
        props=[GL('gl5', glint=[0.52], fc=0.6),
               P('pol5', 'signBoard', pos=[-3.35, 2.75, -3.5], opts={'text': 'POLICE', 'bg': '#1B2A4A', 'fg': '#FFFFFF', 'w': 1.3, 'h': 0.4, 'posts': False, 'height': 0})],   # (stills r3b) the set's own board is out of this frame; (final pass) to the left, off the glint
        cams=[FC(0.0, [-1.25, 1.75, 0.5], [[GLP5[0], 2.62, GLP5[2]], [GLP5[0], 1.25, GLP5[2]], [-2.7, 1.8, -2.75], [-3.05, 0.95, -2.3], [-1.35, 1.9, -2.3]], top=0.14, bottom=0.76, inside=(-6.8, 6.8, 0.3, 3.4, -3.3, 13.0))])
st.cue('sfx:ding', 'S05', 0.52, 0.15); st.cue('sfx:paper', 'S05', 1.05, 0.2)

# 6: the police searched the whole district. (pass 3, review 2: the three search gags sat on the frame edges and under the caption, he only walked,
#    arms hanging) a policeman in the foreground sweeps his big binoculars straight past us; behind him another has dived into a bin, his legs
#    kicking in the air, a brown dog sniffing at it; between them the man gropes his way along, arms out, straight into a lamp post: flat as paper
#    against it, he peels off, puffs back up and gropes on, the glasses on his head unmoved (FOUILLE). (final pass, review 3: he hit the post from its
#    far side, the post cut through him and the flattening read as a thin stretch behind it; he was a quarter of the frame tall between an oversized
#    policeman and oversized legs) three-quarters on him, about 40 % of the frame tall, the post beside him: he gropes in from the right and hits it
#    face first; flat as a sheet (the three-quarter view shows how thin), held, a stagger as he peels off, a pop back with an overshoot, and he gropes
#    on round it toward us; the binoculars policeman further left, a little smaller, sweeping right across the lens; the bin and its kicking legs
#    pushed back on the right, the dog at the bin
D6 = st.dur('S06'); LAMP6 = [5.75, 0, 1.0]; HIT6 = 0.8; POP6 = 1.3
S6 = [7.3, 0, 1.0]; E6 = [6.02, 0, 1.0]
GROPE = {'touch': {'R': ['torso', -0.2, 0.34, 0.6, 1, 0.0], 'L': ['torso', 0.2, 0.42, 0.6, 1, 0.0]}, 'hands': {'R': 'spread', 'L': 'spread'}, 'face': SQUINT}
st.shot('S06', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', S6, -90, 'walk', 'neutral', keys=[k(0.0, to=E6, dur=HIT6, clip='walk', ease='linear', face='keep'), k(0.0, look=[2.0, 2.1, 1.0]), k(0.0, toon=GROPE, toonDur=0.0),
            k(HIT6, clip='paperThin', params={'thin': 0.05, 'puffs': [[r(POP6 - HIT6 - 0.18), 0.35], [r(POP6 - HIT6), 1.12], [r(POP6 - HIT6 + 0.12), 1.0]]}, blend=0.02),   # flat as a sheet on the post (held), a first puff as he peels off, then the pop past full and back
            k(HIT6, toon={'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.9, 'cross': 0.7, 'noBlink': 1}}, toonDur=0.03),
            k(r(POP6 - 0.18), to=[6.12, 0, 1.08], dur=0.12, ease='out'),   # he peels off the post, lagging back
            k(r(POP6 + 0.3), to=[5.4, 0, 1.75], dur=r(D6 - POP6 - 0.3), clip='walk', ease='inOut'), k(r(POP6 + 0.3), look=[3.0, 2.0, 4.0]), k(r(POP6 + 0.3), toon=GROPE, toonDur=0.15)]),   # ...and gropes on round it, toward us
        act('flic1', [4.8, 0, 0.95], -22, 'binocs', 'neutral', scale=0.86, keys=[k(0.0, look=[-3.0, 2.2, 7.0]), k(0.35, look=[4.0, 1.5, 4.6], lookDur=0.6), k(1.0, look=[11.0, 2.2, 6.0], lookDur=0.7)]),   # sweeping right across the lens
        act('flic2', [7.3, 0.5, 0.2], 20, 'headStuck', 'neutral', scale=0.85, params={'sink': 0.2, 'decay': 0.45, 'freq': 15}),                                                          # in the bin, legs up, further back
        act('chien0', [6.85, 0, 0.55], 120, 'walk', 'neutral', scale=0.85, keys=[k(0.0, to=[7.05, 0, 0.45], dur=D6, clip='walk', ease='inOut', face='keep')])],
        props=[GL('gl6', fc=0.65), P('lamp6', 'streetLamp', pos=LAMP6, ry=180, opts={'color': '#3F5E4A'}), P('bin6', 'trashCan', pos=[7.3, 0, 0.2], scale=1.05, opts={'open': True}),
               P('bino6', 'bigBinoculars', on={'actor': 'flic1', 'joint': 'head', 'offset': [0.0, 0.31, 0.1]}),
               P('choc6', 'flashBursts', pos=[5.82, 1.95, 1.08], face='camera', opts={'n': 1, 'w': 0.0, 'h': 0.0, 'at': [HIT6], 'life': 0.25})],
        cams=[FC(0.0, [4.4, 1.2, 3.9], [[6.02, 2.4, 1.0], [6.02, 0.05, 1.0]], top=0.3, bottom=0.74, lenses=range(26, 70))])
st.cue('sfx:sniff', 'S06', 0.3, 0.2); st.cue('sfx:bonk', 'S06', HIT6, 0.3); st.cue('pop', 'S06', POP6, 0.2)

# 7: divers drained the river. In the mud of the emptied river between the stone quays: two divers in masks dig, one holds up an old boot; a fish
#    flops in a puddle; on the quay above, he looks down at them, the glasses on his head
D7 = st.dur('S07')
LEAN7 = lambda b, f, st_=1.0: {'bend': {'spine': [b, 0, 0, st_, None], 'neck': [0.25, 0, 0, 1, None]}, 'touch': {'R': ['torso', -0.24, 0.05, 0.3, 1, 0.0], 'L': ['torso', 0.24, 0.05, 0.3, 1, 0.0]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f}   # both hands on the rail
st.shot('S07', 'grassland', actors=[
        act('plong1', [-1.0, 0, 1.0], 20, 'pointDown', 'neutral', keys=[k(0.0, look=[-1.0, 0.0, 1.8]), k(0.4, look=[-1.2, 0.0, 0.6])]),
        act('plong2', [1.0, 0, 0.4], -30, 'holdUp', 'neutral', keys=[k(0.0, look='camera')]),
        act('mec', [-3.65, 2.76, 2.2], 25, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.0, 0.5]), k(0.0, toon=LEAN7(0.3, SQUINT), toonDur=0.0),
            k(0.25, toon=LEAN7(0.95, SQUINT, 1.1), toonDur=0.4, toonEase='inOut'),                                             # (pass 3) he leans out from the hips, further and further (review 2: a head-only tilt on a vertical body)...
            k(0.75, clip='teeter', params={'grow': 0.9, 'freq': 6.5}, blend=0.05), k(0.75, toon={'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 0.9, 'noBlink': 1}}, toonDur=0.05),   # ...too far: he windmills...
            k(1.35, clip='stand', blend=0.12), k(1.35, toon=LEAN7(0.2, {**SQUINT, 'mouth': 'line'}), toonDur=0.14), k(1.4, look=[1.0, 0.5, 0.4])]),   # ...and catches himself
        act('poisson7', [0.2, 0.0, 1.9], 0, 'stand', 'neutral', scale=0.35, keys=[*[k(r(0.1 + 0.3 * j), to=[r(0.2 + 0.05 * (j % 2)), 0.25 if j % 2 == 0 else 0.0, 1.9], dur=0.15, ease='out' if j % 2 == 0 else 'in') for j in range(6)]])],
        props=[P('river7', 'drainedRiver', pos=[0.0, 0.16, 0.0], opts={'w': 8, 'len': 40, 'qh': 2.45, 'bridgeZ': -16}), GL('gl7'),
               P('mask71', 'diveMask', on={'actor': 'plong1', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.28, 'y': 0.3}),
               P('mask72', 'diveMask', on={'actor': 'plong2', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.28, 'y': 0.3}),
               P('boot7', 'slab', on={'actor': 'plong2', 'hand': 'R', 'offset': [0.0, 0.12, 0.04]}, opts={'w': 0.13, 'h': 0.3, 'd': 0.13, 'color': '#3B2A20'}),
               P('boot7b', 'slab', on={'actor': 'plong2', 'hand': 'R', 'offset': [0.0, -0.02, 0.12]}, opts={'w': 0.13, 'h': 0.1, 'd': 0.3, 'color': '#3B2A20'}),   # (review 1) the shaft and the foot of a boot (one box read as a brick)
               *[P(f'tank7{j}', 'slab', on={'actor': f'plong{j}', 'joint': 'torso', 'offset': [0.0, 0.15, -0.2]}, opts={'w': 0.2, 'h': 0.55, 'd': 0.18, 'color': '#F2C21E', 'outline': 0.006}) for j in (1, 2)],   # air tanks
               P('tour7', 'eiffelTower', pos=[3.0, 0.0, -95.0], opts={'h': 30, 'style': 'v2'})],   # (review 1) nothing said Seine
        cams=[FC(0.0, [-2.9, 4.7, 3.7], [[-3.65, 5.5, 2.2], [-3.65, 4.0, 2.2], [-1.0, 2.4, 1.0], [1.0, 2.6, 0.4], [-1.0, 1.0, 1.0], [1.0, 1.0, 0.4]], top=0.12, bottom=0.78)])   # (stills 7) behind his shoulder on the quay, looking down at the divers
st.cue('sfx:splash', 'S07', 0.1, 0.15); st.cue('sfx:splash', 'S07', 0.7, 0.12); st.cue('sfx:splash', 'S07', 1.3, 0.12)

# 8: the army sent helicopters. At night in the street, from low: a helicopter hangs over the roofs, its searchlight sweeps the street, crosses him,
#    and the glasses on his head flash in the beam; the beam sweeps on
D8 = st.dur('S08'); PASS8 = 1.0
WASH8 = lambda lean, w: {'lay': [lean, 0], 'wind': [0, -2.0, w], 'touch': {'R': ['face', -0.05, 0.9, 0.12, 1, 0.0]}, 'hands': {'R': 'open'}, 'face': {**SQUINT, 'lid': 0.6, 'mouth': 'grimace'}}
st.shot('S08', 'parisStreet', setOpts={'night': True, 'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, look={'sun': 0.15, 'fill': 0.35, 'exposure': 1.1}, actors=[
        act('mec', [5.0, 0, 0.0], 20, 'stand', 'neutral', keys=[k(0.0, look=[3.0, 12.0, -10.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0),
            k(r(PASS8 - 0.45), toon=WASH8(0.42, 11.0), toonDur=0.3, toonEase='out'), k(r(PASS8 - 0.35), look=[5.8, 3.2, 3.0]), k(r(PASS8 + 0.15), look='camera'),   # (final pass) half to us under the beam (turned away, his head was a black silhouette)   # (pass 3, review 2: he stood arms at his sides for 2.27 s) the rotor wash bends him forward, tie and hair flying; he shades his eyes, and his hand knocks the glasses
            *[k(r(PASS8 - 0.1 + 0.16 * j), toon=WASH8(r(0.42 + 0.05 * (j % 2)), r(11.0 - 3.0 * (j % 2))), toonDur=0.12) for j in range(4)],
            k(r(PASS8 + 0.6), toon=WASH8(0.22, 6.0), toonDur=0.3), k(r(D8 - 0.3), toon=WASH8(0.12, 3.0), toonDur=0.25)])],
        props=[P('heli8', 'helicopter', pos=[2.5, 13.0, -9.0], ry=150, rot=[0.12, 0, 0], scale=0.9, opts={'spin': 5, 'beam': True, 'beamLen': 18, 'beamR': 2.4, 'tilt': 30, 'sweep': [[0.0, -40], [PASS8, -8], [D8, 30]],
                                   'bladeOpacity': 0.35, 'discOpacity': 0.1},   # (final pass) see-through blades: solid, they read as a grey saucer lid
                 keys=[k(0.0, to=[3.5, 13.5, -8.0], dur=D8, ease='linear')]), GL('gl8', glint=[r(PASS8 - 0.05)], tap=[r(PASS8 - 0.2)]), P('star8', 'flashBursts', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.68, 0.12], 'face': 'camera'}, opts={'n': 1, 'w': 0.0, 'h': 0.0, 'at': [r(PASS8 - 0.08)], 'life': 0.25}),   # (review 1) no flash registered
               P('spot8', 'glowLight', pos=[5.4, 2.6, 1.3], opts={'color': '#FFF4C8', 'k': 9.0, 'dist': 4.0}, keys=[k(0.0, visible=False), k(r(PASS8 - 0.3), visible=True), k(r(PASS8 + 0.35), visible=False)])],   # (final pass) in front of his face, longer: the beam lights it
        cams=[FC(0.0, [6.4, 0.9, 3.0], [[5.0, 2.9, 0.0], [5.0, 0.9, 0.0], [2.5, 16.0, -9.0], [6.0, 12.0, -8.0]], top=0.08, bottom=0.8)])
st.cue('sfx:engine', 'S08', 0.05, 0.4); st.cue('sfx:ding', 'S08', r(PASS8 - 0.05), 0.25)

# 9: satellites scanned the planet. Space, wide: the opaque blue Earth fills the lower half under a black starry sky; three satellites in orbit
#    over it, the nearest in the upper middle, each sweeping a saturated red fan down across the globe (review 1: the globe filled the whole frame
#    behind one big satellite and read as a glitch of translucent triangles)
D9 = st.dur('S09'); EARTH9 = [0.0, -9.0, -26.0]   # (stills 6) at -15 the globe filled the frame
SATS9 = [('sat9', [-0.2, 1.75, -3.2], [0.32, 0.3, 0.0], 0.3, 7.0, 0.1), ('sat9b', [-1.9, 2.9, -10.0], [0.3, -0.5, 0.15], 0.22, 29.0, 0.3), ('sat9c', [2.2, 2.2, -12.0], [0.32, 0.7, -0.15], 0.22, 28.0, 0.2)]   # (pass 3, review 2) shorter fans that end on the globe with a lit footprint (they ran past the planet to the bottom of the frame, red through the captions)
st.shot('S09', 'spaceDark', actors=[],
        props=[P('earth9', 'earthGlobe', pos=EARTH9, scale=7.0, opts={'spin': 0.06}),
               *[P(n_, 'satellite', pos=p_, rot=ro_, scale=s_, opts={'scan': [[t_, 9.0]], 'scanLen': L_, 'sweepDeg': 26, 'sweepSpeed': 4.6, 'lockAt': r(1.0 + 0.12 * j_), 'foot': True, 'fanOpacity': 0.34, 'fanBlend': 'normal', 'fanColor': '#FF2A1E', 'fanWidth': 0.11},   # (stills 7) narrow beams: wide ones hid the Earth; (final pass) they sweep the globe, then lock one after the other (review 3: they barely moved)
                   keys=[k(0.0, to=[r(p_[0] + 0.35), r(p_[1] + 0.08), p_[2]], dur=D9, ease='linear')]) for j_, (n_, p_, ro_, s_, L_, t_) in enumerate(SATS9)]],
        cams=[cam(0.0, [0.0, 1.0, 5.0], [0.12, 1.0, 4.85], [0.0, -0.3, -6.0], [0.08, -0.3, -6.0], lens=44)])
st.cue('sfx:static', 'S09', 0.1, 0.2); st.cue('sfx:click', 'S09', 1.0, 0.12); st.cue('sfx:click', 'S09', 1.12, 0.12); st.cue('sfx:ding', 'S09', 1.26, 0.15)

# 10: the other countries sent their dogs. (pass 3, review 2: the staring dog never sat and no tilt of its head read; the shot barely moved) low, at
#    dog height: in the foreground, in profile, a dog sniffs at his shoes, sits down with a bounce, stretches its neck right up at the glasses on his
#    head, tilts its head, ears flopping (glint), holds... and goes back to his shoe; behind, dogs of every colour sniff about; he looks down at it.
#    (final pass, review 3: the camera was at his hip and the stretch barely changed the dog's outline) the lens at the dog's height, the dog bigger
#    in the foreground, its neck growing to more than twice its length as it stares up
D10 = st.dur('S10'); STARE10 = 0.5; TILT10 = 0.85; BACK10 = 1.55; DOG10 = [4.7, 0, 1.15]
DOGP = [[5.55, 0, -0.75], [4.3, 0, -0.65], [5.95, 0, -0.15], [4.0, 0, 0.1]]
st.shot('S10', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.1], 20, 'stand', 'unimpressed', keys=[k(0.0, look=[5.6, 2.0, 3.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(r(TILT10 + 0.2), look=[DOG10[0], 0.8, DOG10[2]], lookDur=0.15),
            k(r(TILT10 + 0.2), toon={'bend': {'neck': [0.3, 0, 0, 1, None], 'spine': [0.12, 0, 0, 1, None]}, 'face': {**SQUINT, 'brow': 0.3}}, toonDur=0.15),   # he looks down at it: what?
            k(r(BACK10 + 0.15), look='camera'), k(r(BACK10 + 0.15), toon={'face': {**SQUINT, 'mouth': 'line'}}, toonDur=0.15),
            k(r(D10 - 0.3), toon={'face': {**SQUINT, 'lid': 1.0, 'mouth': 'line'}}, toonDur=0.04), k(r(D10 - 0.24), toon={'face': {**SQUINT, 'mouth': 'line'}}, toonDur=0.06)]),
        *[act(f'chien{j + 1}', DOGP[j], [120, -40, 30, 60][j], 'walk', 'neutral', scale=0.85, keys=[k(0.0, to=[r(DOGP[j][0] + [0.4, -0.3, 0.35, 0.3][j]), 0, r(DOGP[j][2] + [0.2, 0.4, 0.3, -0.3][j])], dur=D10, clip='walk', ease='inOut', face='keep')]) for j in range(4)]],
        props=[GL('gl10', glint=[r(TILT10 + 0.05)], fc=0.5),
               P('fixe10', 'stareDog', pos=DOG10, ry=165, scale=1.25, opts={'body': '#C99A62', 'ear': '#8A5A32', 'collar': '#2F62B5', 'sitAt': 0.15, 'lookAt': STARE10, 'tiltAt': TILT10, 'backAt': BACK10, 'up': 1.15, 'tilt': 0.65, 'stretch': 2.4})],   # (final pass) bigger, the neck stretched right up
        cams=[FC(0.0, [6.6, 0.3, 1.75], [[5.0, 2.62, 0.1], [DOG10[0], 0.05, DOG10[2]], [DOG10[0], 1.6, r(DOG10[2] - 0.2)], [r(DOG10[0] - 0.55), 0.6, DOG10[2]], [r(DOG10[0] + 0.45), 0.6, DOG10[2]]], top=0.1, bottom=0.8, lenses=range(26, 78))])   # (final pass) at dog height, the dog big in profile in front (review 3: the camera stood at his hip)
st.cue('sfx:sniff', 'S10', 0.1, 0.2); st.cue('sfx:boing', 'S10', STARE10, 0.2); st.cue('sfx:squeak', 'S10', TILT10, 0.2); st.cue('sfx:ding', 'S10', r(TILT10 + 0.05), 0.15); st.cue('sfx:sniff', 'S10', r(BACK10 + 0.1), 0.2)

# 11-12: the government promised a million euros. At the podium the minister announces it; a reward poster pops up at his side: RÉCOMPENSE, the
#    glasses drawn on it, « UN MILLION D'EUROS »; he points at it (MILLION). (pass 3, review 2: a navy suit on a navy backdrop, the raised arm across
#    his face, both arms crossed in an X: he raised the arm that is away from the camera) a pale backdrop; one hand flat on the lectern, the arm
#    on our side straight up beside his head, index out; the sash in every shot; no flag cut by the frame
D11 = st.dur('S11'); D12 = st.dur('S12')
PRESS = {'backdrop': 'GOUVERNEMENT', 'fontScale': 0.55, 'bg': '#A9C1D6', 'fg': 'rgba(255,255,255,0.92)', 'wall': '#93ADC6', 'band': '#7F9AB5', 'flags': False}
MIN = lambda keys: act('ministre', [0.0, 0, -2.45], 0, 'stand', 'neutral', keys=keys)
SASH = lambda pid: P(pid, 'mayorSash', on={'actor': 'ministre', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.21, 'w': 0.17, 'len': 0.8})
LECT = {'R': [-0.2, 1.17, -2.14, 1, 0.04], 'L': [0.2, 1.17, -2.14, 1, 0.04]}
UP11 = lambda f, y=2.72: {'reach': {'R': LECT['R'], 'L': [0.4, y, -2.42, 1, 0.05]}, 'hands': {'R': 'open', 'L': 'point'}, 'face': f}
st.shot('S11', 'pressRoom', setOpts=PRESS, actors=[MIN([k(0.0, look='camera'), k(0.0, toon={'reach': LECT, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0),
            k(0.22, toon={'reach': {'R': LECT['R'], 'L': [0.3, 1.0, -2.3, 1, 0.04]}, 'hands': {'R': 'open', 'L': 'point'}, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.1),   # a dip...
            k(0.35, toon={**UP11({'lid': 0.1, 'mouth': 'open', 'brow': 0.7}, 2.86), 'sq': [0.96, 1.06, 0.96]}, toonDur=0.12, toonEase='out'), k(0.5, toon=UP11({'lid': 0.2, 'mouth': 'open', 'brow': 0.6}), toonDur=0.1),   # ...and the arm shoots up, overshoots, settles
            k(0.9, toon=UP11({'lid': 1.0, 'mouth': 'open', 'brow': 0.6}), toonDur=0.05), k(1.0, toon=UP11({'lid': 0.2, 'mouth': 'open', 'brow': 0.6}), toonDur=0.07)])],
        props=[SASH('echarpe11'), *[P(f'fl11{j}', 'glowLight', pos=[r(-1.2 + 1.2 * j), 1.8, 1.2], opts={'color': '#FFFFFF', 'k': 6.0, 'dist': 6.0}, keys=[k(0.0, visible=False), k(r(0.3 + 0.35 * j), visible=True), k(r(0.36 + 0.35 * j), visible=False)]) for j in range(3)]],
        cams=[FC(0.0, [0.7, 1.7, 1.6], [[0.0, 2.6, -2.45], [0.45, 2.95, -2.42], [0.0, 0.9, -2.0], [-0.6, 1.3, -2.0]], top=0.14, bottom=0.78)])
# (final pass, review 3: once the poster popped he froze 0.8 s, his hand on its corner read as a thumbs-up) his index lands on the glasses drawn on
#    the poster and taps them twice; he turns to us, a nod, an eyebrow up, a blink, breathing
GLP12 = lambda dz=0.0: [0.95, 1.64, r(-2.25 + dz), 1, 0.06]   # the left lens drawn on the poster (pos 1.15, ry -15, 1.0 x 1.35 on a 0.9 m stand)
PT12 = lambda f, dz=0.0, extra=None: {'reach': {'R': LECT['R'], 'L': GLP12(dz)}, 'hands': {'R': 'open', 'L': 'point'}, 'face': f, **(extra or {})}
F12 = {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.5}
st.shot('S12', 'pressRoom', setOpts=PRESS, actors=[MIN([k(0.0, look=[1.0, 1.7, -2.3]), k(0.0, toon=PT12(F12, 0.12), toonDur=0.0),
            k(0.1, toon=PT12(F12), toonDur=0.08, toonEase='out'), k(0.22, toon=PT12(F12, 0.07), toonDur=0.06), k(0.3, toon=PT12(F12), toonDur=0.06, toonEase='in'),   # tap... tap, on the drawn glasses
            k(0.45, look='camera', lookDur=0.15), k(0.62, toon=PT12({**F12, 'brow': 0.95}, 0.0, {'bend': {'neck': [0.16, 0, 0, 1, None]}}), toonDur=0.08),   # to us: a nod, an eyebrow up...
            k(0.74, toon=PT12({**F12, 'brow': 0.8}), toonDur=0.1), k(0.95, toon=PT12({**F12, 'lid': 1.0}), toonDur=0.05), k(1.03, toon=PT12(F12), toonDur=0.08)])],   # ...a blink
        props=[SASH('echarpe12'), P('poster12', 'rewardPoster', pos=[1.15, 0, -2.3], ry=-15, opts={'at': 0.05, 'w': 1.0, 'h': 1.35, 'stand': 0.9})],
        cams=[FC(0.0, [0.5, 1.65, 1.5], [[0.0, 2.6, -2.45], [1.15, 2.35, -2.3], [1.15, 0.9, -2.3], [0.0, 1.0, -2.0], [1.72, 2.4, -2.45], [1.72, 0.9, -2.45]], top=0.2, bottom=0.78)])   # (stills 1) its right edge was cut
st.cue('sfx:click', 'S11', 0.3, 0.2); st.cue('sfx:click', 'S11', 0.65, 0.2); st.cue('sfx:boing', 'S12', 0.05, 0.25); st.cue('sfx:cash', 'S12', 0.25, 0.3)

# 13: the whole world searched for a year. (pass 3, review 2: three clerks in a clump, the calendar a stamp behind his head, the magnifying glass a
#    yellow arc) tighter, on three depths: on the back wall, top left, a big calendar sheds its twelve months toward us; in front on the left a
#    searcher crawls under a desk, legs sticking out; at the back on the right one holds the potted plant up and peers under the pot; and right at his
#    face a savant inspects him through a big magnifying glass, one huge eye an inch under the glasses on his head; he leans away from it, squinting
D13 = st.dur('S13'); MOIS = ['JANVIER', 'FÉVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN', 'JUILLET', 'AOÛT', 'SEPTEMBRE', 'OCTOBRE', 'NOVEMBRE', 'DÉCEMBRE']
ME13 = [0.1, 0, -1.6]; DESK13 = [-1.2, 0, -1.15]; POT13 = [1.6, 1.9, -2.7]; SAV13 = [0.82, 0, -1.35]
PLANTK = lambda f: {'reach': {'R': [r(POT13[0] - 0.16), r(POT13[1] + 0.16), POT13[2], 1, 0.03], 'L': [r(POT13[0] + 0.16), r(POT13[1] + 0.16), POT13[2], 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f}
AWAY13 = lambda f, b=-0.22: {'bend': {'spine': [b, 0.2, 0, 1, None], 'neck': [-0.1, 0.15, 0, 1, None]}, 'face': f}
PEER13 = lambda b: {'bend': {'spine': [b, 0, 0, 1, None], 'neck': [-0.25, 0, 0, 1, None]}, 'touch': {'R': ['head', -0.2, 0.12, 0.3, 1, 0.0]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'brow': 0.6, 'mouth': 'o'}}
st.shot('S13', 'office', setOpts={'picture': False, 'carpet': False, 'printer': False}, actors=[
        act('mec', ME13, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': SQUINT}, toonDur=0.0),
            k(0.3, look=[0.7, 2.0, -1.2], lookDur=0.12), k(0.3, toon=AWAY13({**SQUINT, 'brow': 0.4, 'mouth': 'wavy'}), toonDur=0.18, toonEase='out'),   # the big eye comes up to his face: he leans away from it
            k(1.2, look=[-1.0, 0.5, -0.7]), k(1.6, look='camera'), k(1.6, toon=AWAY13({**SQUINT, 'mouth': 'line'}, -0.12), toonDur=0.2),
            k(1.9, toon=AWAY13({**SQUINT, 'lid': 1.0, 'mouth': 'line'}, -0.12), toonDur=0.04), k(1.96, toon=AWAY13({**SQUINT, 'mouth': 'line'}, -0.12), toonDur=0.06)]),
        act('cherch1', [-1.0, 0, -1.15], -90, 'crawl', 'neutral', keys=[k(0.0, look=[-1.8, 0.2, -1.15])]),   # (final pass) the desk now stands over him: his legs come out from under it (they stuck out of bare floor)   # (stills r3b) further back: at -0.75 his legs lay in the caption band   # his head under the desk, his legs out
        act('cherch2', SAV13, -105, 'stand', 'neutral', keys=[k(0.0, look=[ME13[0], 2.1, ME13[2]]), k(0.0, toon=PEER13(0.1), toonDur=0.0), k(0.2, toon=PEER13(0.38), toonDur=0.2, toonEase='out'),   # he leans right in
            k(1.1, toon=PEER13(0.3), toonDur=0.2), k(1.5, toon=PEER13(0.42), toonDur=0.2)]),
        act('cherch3', [1.6, 0, -3.0], -15, 'stand', 'neutral', keys=[k(0.0, look=[POT13[0], r(POT13[1] - 0.05), POT13[2]]), k(0.0, toon=PLANTK({'lid': 0.3, 'mouth': 'O', 'brow': 0.4}), toonDur=0.0),
            k(1.2, toon=PLANTK({'lid': 1.0, 'mouth': 'O', 'brow': 0.4}), toonDur=0.05), k(1.32, toon=PLANTK({'lid': 0.3, 'mouth': 'O', 'brow': 0.4}), toonDur=0.07)])],
        props=[GL('gl13', glint=[1.0], fc=0.3), P('cal13', 'shedCalendar', pos=[-0.92, 2.35, -3.52], opts={'months': MOIS, 'w': 0.95, 'h': 1.2, 'flipAt': 0.12, 'dur': 0.185, 'fly': [-0.55, -1.2, 2.3], 'life': 0.55}),   # (stills r3a) the pages fly off to the left: toward +x they crossed his face
               P('bureau13', 'table', pos=[-0.68, 0, -1.15], ry=90, opts={'w': 1.25, 'd': 0.62, 'h': 0.74}),   # (stills) over the crawler's head and back: further left it was out of the frame and his legs lay on bare floor P('plante13', 'plant', pos=POT13, scale=0.8, opts={'seed': 21}),
               P('loupe13', 'eyeLens', on={'actor': 'cherch2', 'joint': 'head', 'offset': [0.0, 0.33, 0.3], 'face': 'camera', 'faceAmt': 0.8}, opts={'r': 0.17, 'blink': [0.7, 1.75], 'look': [[0.0, -0.6, 0.3], [0.4, 0.7, 0.5], [0.9, -0.7, 0.6], [1.3, 0.6, 0.2], [1.8, 0.0, 0.7], [2.3, -0.5, 0.4]]})],
        cams=[FC(0.0, [0.45, 1.6, 1.3], [[ME13[0], 2.65, ME13[2]], [-1.4, 2.95, -3.5], [r(POT13[0] + 0.05), 2.7, POT13[2]], [-0.3, 0.3, -1.15], [1.15, 1.0, -1.3]], top=0.1, bottom=0.78, lenses=range(26, 64))])   # (stills r3a) tighter: fitted on the far desk it backed off 2.25 m and half the frame was wall and floor
st.cue('sfx:paper', 'S13', 0.15, 0.2); st.cue('sfx:paper', 'S13', 0.7, 0.2); st.cue('sfx:paper', 'S13', 1.25, 0.2); st.cue('sfx:paper', 'S13', 1.8, 0.2); st.cue('sfx:squeak', 'S13', 0.3, 0.15)

# 14: yesterday a child found them. (pass 3, review 2: the boy seen from behind, the glasses edge-on and black on black hair, his finger ending a
#    head's height above them) three-quarters on both: the boy low on the left, facing us, tugs at the man's sleeve; the man looks down at him; the
#    boy winds up and his arm shoots up, past the mark, and comes down ON the glasses: a tap, they rock and glint; a second tap; his mouth wide open
D14 = st.dur('S14'); TUG14 = 0.3; TAP14 = 0.84; TAP14B = 1.32
ONGL = lambda dy=0.0, dz=0.0: ['@mec.head', -0.1, r(0.6 + dy), r(0.08 + dz), 1, 0.07]   # the near lens of the glasses on his head, in the frame of his head: the finger stays on it when he nods
BOYF = {'lid': 0.0, 'eye': 0.5, 'mouth': 'open', 'brow': 0.8}
st.shot('S14', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.0], 15, 'stand', 'unimpressed', keys=[k(0.0, look=[6.5, 2.0, 4.0]), k(0.0, toon={'face': SQUINT}, toonDur=0.0), k(r(TUG14 + 0.1), look=[4.3, 1.2, 0.5]),
            k(r(TUG14 + 0.12), toon={'bend': {'neck': [0.22, 0, 0, 1, None]}, 'face': {**SQUINT, 'brow': 0.3}}, toonDur=0.12),
            k(TAP14, toon={'bend': {'neck': [0.3, 0, 0, 1, None]}, 'sq': [1.03, 0.96, 1.03], 'face': {**SQUINT, 'brow': 0.5, 'mouth': 'o'}}, toonDur=0.05), k(r(TAP14 + 0.12), toon={'bend': {'neck': [0.22, 0, 0, 1, None]}, 'face': {**SQUINT, 'brow': 0.5, 'mouth': 'o'}}, toonDur=0.1),   # tapped: a dip of the knees
            k(1.55, toon={'bend': {'neck': [0.22, 0, 0, 1, None]}, 'face': {**SQUINT, 'lid': 1.0, 'brow': 0.5, 'mouth': 'o'}}, toonDur=0.04), k(1.61, toon={'bend': {'neck': [0.22, 0, 0, 1, None]}, 'face': {**SQUINT, 'brow': 0.5, 'mouth': 'o'}}, toonDur=0.06), k(1.85, look='camera')]),
        act('gamin', [4.3, 0, 0.5], 55, 'stand', 'neutral', keys=[k(0.0, look=[5.6, 2.1, 1.6]), k(0.0, toon={'touch': {'L': ['@mec.handR', 0.0, 0.0, 0.0, 1, 0.0]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.0),
            *[k(r(TUG14 * (j + 1) / 2), toon={'touch': {'L': ['@mec.handR', 0.0, r(-0.04 * (j % 2)), 0.0, 1, 0.0]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.06) for j in range(2)],   # two tugs at his sleeve...
            k(r(TAP14 - 0.32), toon={'reach': {'L': [4.25, 0.55, 0.75, 1, 0.05]}, 'hands': {'L': 'point'}, 'sq': [1.08, 0.88, 1.08], 'face': BOYF}, toonDur=0.12, toonEase='out'),                        # ...a wind-up...
            k(r(TAP14 - 0.14), toon={'touch': {'L': ONGL(0.28)}, 'hands': {'L': 'point'}, 'sq': [0.93, 1.12, 0.93], 'face': BOYF}, toonDur=0.08, toonEase='out'),                                          # ...the arm shoots up past the mark...
            k(r(TAP14 - 0.03), toon={'touch': {'L': ONGL()}, 'hands': {'L': 'point'}, 'face': BOYF}, toonDur=0.04, toonEase='in'),                                                                         # ...and down ON the glasses: tap
            k(r(TAP14B - 0.18), toon={'touch': {'L': ONGL(0.14, 0.05)}, 'hands': {'L': 'point'}, 'face': BOYF}, toonDur=0.1), k(r(TAP14B - 0.03), toon={'touch': {'L': ONGL()}, 'hands': {'L': 'point'}, 'face': BOYF}, toonDur=0.04, toonEase='in'),   # there! (again)
            k(1.7, toon={'touch': {'L': ONGL()}, 'hands': {'L': 'point'}, 'face': {**BOYF, 'lid': 1.0}}, toonDur=0.04), k(1.76, toon={'touch': {'L': ONGL()}, 'hands': {'L': 'point'}, 'face': BOYF}, toonDur=0.06), k(r(TAP14 + 0.3), look='camera')])],   # ...and he turns to us, mouth open: there!
        props=[GL('gl14', glint=[r(TAP14 + 0.02)], fc=0.75, s=1.2, tap=[TAP14, TAP14B])],
        cams=[FC(0.0, [6.0, 1.25, 3.0], [[5.0, 2.7, 0.0], [5.3, 1.0, 0.0], [4.25, 0.45, 0.5], [3.85, 1.5, 0.6], [5.35, 2.0, 0.0]], top=0.14, bottom=0.78)])
st.cue('sfx:stepSoft', 'S14', 0.1, 0.15); st.cue('sfx:gasp', 'S14', r(TAP14 - 0.3), 0.2); st.cue('sfx:clink', 'S14', TAP14, 0.25); st.cue('sfx:ding', 'S14', r(TAP14 + 0.02), 0.2); st.cue('sfx:clink', 'S14', TAP14B, 0.2)

# 15: on his head. Close: his eyes roll up to the top of his head; the glasses flash; his eyes pop (TROUVÉES)
D15 = st.dur('S15'); UP15 = 0.15; POP15 = 0.55
st.shot('S15', 'parisStreet', setOpts={'clear': [-12.0, 12.0], 'clearL': [-12.0, 12.0]}, actors=[
        act('mec', [5.0, 0, 0.0], 15, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': SQUINT}, toonDur=0.0),
            k(UP15, toon={'face': {'lid': 0.0, 'low': 0.0, 'gy': -1.0, 'eye': 0.6, 'brow': 0.7, 'mouth': 'line', 'noBlink': 1}}, toonDur=0.15, toonEase='inOut'),   # the eyes roll up, wide...
            k(r(POP15 - 0.08), toon={'sq': [1.1, 0.9, 1.1], 'face': {'lid': 0.0, 'gy': -1.0, 'eye': 0.6, 'brow': 0.9, 'mouth': 'line', 'noBlink': 1}}, toonDur=0.05, toonEase='in'),   # ...a squash...
            k(POP15, toon={'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.0, 'gy': -1.0, 'eyePitch': -0.5, 'pop': 1.0, 'popLen': 0.3, 'brow': 1.0, 'mouth': 'O', 'noBlink': 1}}, toonDur=0.04, toonEase='out'),   # ...POP, the eyes out on stalks...
            k(r(POP15 + 0.42), toon={'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.0, 'gy': -1.0, 'eyePitch': -0.5, 'pop': 1.0, 'popLen': 0.3, 'brow': 1.0, 'mouth': 'O', 'noBlink': 1}}, toonDur=0.1),   # ...held
            k(r(POP15 + 0.5), toon={'face': {'lid': 0.0, 'gy': -0.6, 'eye': 0.5, 'brow': 0.8, 'mouth': 'O'}}, toonDur=0.08)])],
        props=[GL('gl15', glint=[r(UP15 + 0.2)])],
        cams=[FC(0.0, [5.5, 2.35, 1.5], [[5.0, 3.0, 0.0], [5.0, 1.75, 0.0], [5.35, 2.3, 0.1], [4.65, 2.3, 0.1]], top=0.2, bottom=0.74)])
st.cue('sfx:ding', 'S15', r(UP15 + 0.2), 0.35); st.cue('pop', 'S15', POP15, 0.25)

# 16: the child got the million. A town-hall stage. (pass 3, review 2: the cheque cycled about his head, legible two frames at a time, cut by the
#    frame) one big jump: a squat, he goes up with the giant cheque flat over his head, the whole of it in frame, hangs, lands with a squash, then a
#    small second hop; the minister, sash on, claps at his side
D16 = st.dur('S16'); UP16 = 0.32; AIR16 = 0.72
BOY16 = {'lid': 0.0, 'eye': 0.3, 'mouth': 'bigsmile', 'brow': 0.8}
HOLD16 = {'touch': {'R': ['head', -0.45, 0.55, 0.04, 1, 0.0], 'L': ['head', 0.45, 0.55, 0.04, 1, 0.0]}, 'hands': {'R': 'grip', 'L': 'grip'}}   # (stills r3a) both hands on the cheque's lower edge all through the jump (the arms lagged behind and it floated)
CLAP16 = lambda j: {'touch': {'R': ['torso', r(-0.05 - 0.07 * (j % 2)), 0.42, 0.32, 1, 0.0], 'L': ['torso', r(0.05 + 0.07 * (j % 2)), 0.42, 0.32, 1, 0.0]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.4}}
st.shot('S16', 'mairie', setOpts={'desk': False, 'map': False}, actors=[   # (review 1) no map: its stamp from another episode showed behind the cheque
        act('gamin', [0.0, 0, -1.2], 0, 'holdUp', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD16, 'face': BOY16}, toonDur=0.0),
            k(0.12, toon={**HOLD16, 'sq': [1.2, 0.74, 1.2], 'face': BOY16}, toonDur=0.14, toonEase='out'),                                                                  # a squat...
            k(UP16, to=[0.0, 0.6, -1.2], dur=0.2, ease='out'),   # (final pass) 0.6: at 0.8 the cheque's top left the frame at the apex k(UP16, toon={**HOLD16, 'sq': [0.9, 1.15, 0.9], 'face': {**BOY16, 'mouth': 'scream'}}, toonDur=0.08, toonEase='out'),   # ...up...
            k(r(UP16 + 0.2), toon={**HOLD16, 'sq': [1.0, 1.0, 1.0], 'face': {**BOY16, 'mouth': 'scream'}}, toonDur=0.15),                                                     # ...he hangs...
            k(AIR16, to=[0.0, 0.0, -1.2], dur=0.16, ease='in'), k(r(AIR16 + 0.15), toon={**HOLD16, 'sq': [1.12, 0.86, 1.12], 'face': BOY16}, toonDur=0.04), k(r(AIR16 + 0.22), toon={**HOLD16, 'sq': [0.96, 1.05, 0.96], 'face': BOY16}, toonDur=0.1),   # ...lands, squashed
            k(1.18, to=[0.0, 0.25, -1.2], dur=0.14, ease='out'), k(1.32, to=[0.0, 0.0, -1.2], dur=0.12, ease='in'), k(1.44, toon={**HOLD16, 'sq': [1.08, 0.92, 1.08], 'face': BOY16}, toonDur=0.04), k(1.5, toon={**HOLD16, 'face': BOY16}, toonDur=0.1)]),   # a small second hop
        act('ministre', [1.15, 0, -1.55], -40, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.9, -1.2]), *[k(r(0.05 + 0.14 * j), toon=CLAP16(j), toonDur=0.06) for j in range(12)]])],
        props=[P('cheque16', 'bigCheque', on={'actor': 'gamin', 'joint': 'head', 'offset': [0.0, 0.93, 0.04], 'face': 'camera', 'faceFlat': True}, scale=1.65, opts={'text': 'RÉCOMPENSE', 'amount': '1 000 000 €'}),
               P('echarpe16', 'mayorSash', on={'actor': 'ministre', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.21, 'w': 0.17, 'len': 0.8}),
               P('conf16', 'confettiRain', pos=[0.2, 0.0, -1.1], opts={'w': 2.6, 'h': 3.4, 'd': 1.4, 'n': 170, 'size': 0.05})],   # (review 1) the cheque said ASSURANCE 3 000 € and the one-piece `confetti` showed nothing
        cams=[FC(0.0, [0.33, 1.45, 3.35], [[0.0, 3.42, -1.2], [0.0, 0.0, -1.2], [-0.9, 3.05, -1.2], [0.9, 3.05, -1.2], [1.5, 2.45, -1.55], [1.3, 0.0, -1.55]], top=0.07, bottom=0.78)])   # (final pass) fitted on the cheque's top at the apex
st.cue('sfx:fanfare', 'S16', 0.05, 0.3); st.cue('sfx:boing', 'S16', UP16, 0.2); st.cue('sfx:cash', 'S16', r(UP16 + 0.2), 0.2); st.cue('sfx:step', 'S16', r(AIR16 + 0.16), 0.2)

# 17: the man is looking for his keys. His living room by the door. (pass 3, review 2: the glasses still on his head and the same squint: nothing
#    said the first search was over) the glasses are on his nose now, his eyes big behind them: he pats every pocket, his big eyes sweep left, right,
#    down past the key ring that hangs from his own mouth, and on; he stops, a slow blink at us, the keys glint. (final pass, review 3: two mouths, eyes
#    as slits) the glasses tilt with his crooked painted face, a lens over each eye (the low eye peeped out under a level lens and read as a second
#    grin); wide eyes whose pupils dart ahead of the head; brows down, deadpan; one real slow blink
D17 = st.dur('S17')
WORN = {'lid': 0.0, 'low': 0.0, 'eye': 0.4, 'brow': 0.12, 'mouth': 'clench'}   # his eyes big behind the lenses; (final pass) brow down: deadpan, not a smirk
st.shot('S17', 'livingRoom', actors=[
        act('mec', [-0.4, 0, -0.6], 15, 'patPockets', 'unimpressed', keys=[k(0.0, toon={'face': {**WORN, 'gx': -0.9}}, toonDur=0.0), k(0.06, look=[-1.6, 2.3, 0.6]), k(0.45, toon={'face': {**WORN, 'gx': 0.9}}, toonDur=0.1), k(0.55, look=[1.6, 2.3, 0.6]),   # (final pass) the pupils lead, the head follows
            k(0.92, toon={'face': {**WORN, 'gy': 1.0, 'cross': 0.45}}, toonDur=0.1), k(1.0, look='camera'), k(1.3, toon={'face': {**WORN, 'gx': -0.7, 'gy': 0.35}}, toonDur=0.12),   # ...down past the keys in his mouth, and on
            k(1.55, to=[-0.4, 0, -0.6], dur=0.01, clip='stand', face='keep'), k(1.55, toon={'face': WORN}, toonDur=0.12), k(1.85, toon={'face': {**WORN, 'lid': 1.0}}, toonDur=0.16, toonEase='inOut'), k(2.12, toon={'face': WORN}, toonDur=0.2, toonEase='inOut')])],   # he stops: one real slow blink at us
        props=[GL('gl17', glint=[0.3], off=(-0.004, 0.321, 0.1), lens=0.18, rot=(0.0, 0.0, -0.645), dx=0.082, r_=0.06), P('keys17', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.1, 0.13], 'face': 'camera'}, scale=3.0),   # (review 1) twice the size; (final pass) the glasses: one lens over each eye of his crooked face (the painted right eye sits 0.1 m above the left: level, the low eye showed under the lens as a second grin, review 3)
               P('star17', 'flashBursts', on={'actor': 'mec', 'joint': 'head', 'offset': [0.06, -0.05, 0.2], 'face': 'camera'}, opts={'n': 1, 'w': 0.0, 'h': 0.0, 'at': [2.2], 'life': 0.22})],
        cams=[FC(0.0, [-1.1, 1.5, 1.5], [[-0.4, 2.55, -0.6], [-0.4, 1.2, -0.6], [0.0, 1.9, -0.4], [-0.8, 1.9, -0.4]], top=0.14, bottom=0.76, drift=(0.25, 0.12, -0.5))])   # a slow push-in for the end hold   # (pass 3) less from the side: his face and the lenses to us
st.cue('sfx:rattleShort', 'S17', 0.3, 0.15); st.cue('sfx:rattleShort', 'S17', 0.9, 0.15); st.cue('sfx:ding', 'S17', 2.2, 0.15)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.4}}
st.write("Les lunettes", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec', 'gamin'], extra_cast={
    'mec': MEC,
    'flic': {'preset': 'cop', 'seed': 691, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic1': {'preset': 'cop', 'seed': 692, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic2': {'preset': 'cop2', 'seed': 693, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chien0': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 701, 'colors': {'body': '#9A6B3F', 'collar': '#E0413A'}}},   # (pass 3) brown: near black it was a blob under the caption
    **{f'chien{j + 1}': {'type': 'creature', 'name': 'dog', 'opts': {'seed': 702 + j, 'colors': DOGC[j]}} for j in range(4)},
    'plong1': {'preset': 'worker', 'seed': 694, 'hat': 'none', 'suit': '#1C1C20', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'plong2': {'preset': 'worker', 'seed': 695, 'hat': 'none', 'suit': '#1C1C20', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'poisson7': {'type': 'creature', 'name': 'fish', 'opts': {'seed': 706, 'color': '#F28C28'}},
    'ministre': {'preset': 'politique', 'seed': 696, 'suit': '#2B3A55', 'lapel': '#2B3A55', 'tie': '#9A2A2A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'cherch1': {'preset': 'femme', 'seed': 697, 'suit': '#D9734E', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'cherch2': {'preset': 'savant', 'seed': 698, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'cherch3': {'preset': 'officiel', 'seed': 699, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'gamin': {'preset': 'gamin', 'seed': 700, 'suit': '#E0413A', 'build': {'headScale': 1.25}, 'toon': EX},
})
