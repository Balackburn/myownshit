#!/usr/bin/env python3
"""Le feu rouge (story 66, cycle 28; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man is waiting at a red light. The light never turned green. That was twelve years ago. His beard touches the pavement. The town hall built
him a house on the zebra crossing. The postman delivers his mail at the light. A policeman tried to make him cross. The policeman got a fine. The
pigeons nested in his beard. Tourists queue for the photo. The government decorated him for his patience. The president came to wait with him. He
left after ten minutes. Yesterday the light turned green. Television from all over the world was there. He crossed. The crowd wept. On the other
side there was a red light. He is waiting.
Staging: a Paris crossing, the red man of the pedestrian light across the road; a spider has spun its web over the green lens; his beard grows down
to the pavement in one shot and coils on the ground; a little house round him at the kerb, the mayor showing it off; the postman's letter taken
without a look away from the light; a policeman tugging his arm, stretching, while he does not budge; the policeman on the crossing booked by his
colleague; a nest in the beard, a pigeon, eggs popping in; tourists queuing, flashes; a medal pinned on; the president beside him, then a look at his
watch and off with his bodyguards; the light turns green, the spider drops; TV cameras; the first step, dust falling off him; the crowd in tears,
confetti; the far kerb: another red light; a pigeon lands on his head; a look at us.
Natural look; cycle 28: the beard grown by scale keys, trafficLight states, props reused (zebra, house, mailbox, nest, medal, wristWatch, tvCamera,
pressCamera, confetti, dustPuff), the creatures pigeon and spider."""
from story_kit import *
import math

st = Story('feu', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3, ink=None: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True, **({'ink': ink} if ink else {})})
DEAD = {'lid': 0.45}
STREET = {'eiffelStyle': 'v2', 'clear': [-6.0, 6.0], 'clearL': [-6.0, 6.0]}   # no tree or lamp of the set at the crossing
ME = [5.55, 0, 0.0]                                  # at the kerb of the right-hand pavement, facing the road (-X)
LIGHT = [-5.55, 0, 1.6]                              # the pedestrian light across the road, its lenses toward him (+X)
RED = lambda pid='feu', state=None, pos=LIGHT, ry=90, web=False, h=2.3: P(pid, 'pedSignal', pos=pos, ry=ry, opts={'h': h, 's': 1.25, 'state': state or [[0.0, 'r']], 'web': web})   # (review 1) a French pedestrian light, a red man over a green man (a three-lens car signal)
ZEBRA = lambda pid='zeb': P(pid, 'zebra', pos=[-5.0, 0.012, -1.5], opts={'n': 10})
BEARD = lambda pid='barbe', s=1.5, keys=None, swing=None: P(pid, 'beardHair', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.02, 0.1]}, scale=s, opts={'len': 1.2, 'coil': 0.3, **({'swing': swing} if swing else {})}, **({'keys': keys} if keys else {}))   # (review 1) clumps of hair, fuller at the chin, the tips curled on the paving (slats read as a rake)
HOUSE = lambda pid='maison': P(pid, 'kerbHouse', pos=[r(ME[0] + 0.05), 0, ME[2]], ry=-90, opts={'w': 2.4, 'd': 2.2, 'h': 2.8})   # (review 1) the house built round him: he stands in its doorway; it stays in the later shots
PILE = lambda pid='pile', n=30: P(pid, 'letterPile', pos=[r(ME[0] - 0.5), 0, 0.62], opts={'n': n, 'r': 0.32})   # the letters piling up at his door from S06
NEST = lambda pid='nid', lay=None: P(pid, 'twigNest', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.42, 0.3]}, scale=0.5, opts=({'layAt': lay} if lay else {}))   # a woven nest in the beard, kept from S09
MEDAL = lambda pid='med', keys=None: P(pid, 'medal', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.2, 0.62, 0.17]}, scale=1.4, **({'keys': keys} if keys else {}))   # beside the beard, kept from S11
SHADES = lambda pid, who: P(pid, 'shades', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.22, 0.19]})   # (review 1) dark glasses and an earpiece: bodyguards (red caps and grey jackets read as tourists)
PIN = lambda pid: P(pid, 'cockade', on={'actor': 'president', 'joint': 'torso', 'offset': [-0.15, 0.6, 0.17]})   # the president's tricolour pin
WAIT = lambda bl=None: [k(0.0, look=[LIGHT[0], 3.2, LIGHT[2]]), k(0.0, toon={'face': DEAD}, toonDur=0.0), *([k(bl, toon={'face': {'lid': 1.0}}, toonDur=0.07), k(round(bl + 0.13, 3), toon={'face': DEAD}, toonDur=0.1)] if bl else [])]   # (review 1) a slow blink somewhere in each long hold, never at the same moment   # his eyes on the light across the road
CAR = lambda pid, x, z0, z1, t0, dur, col: P(pid, 'car', pos=[x, 0, z0], ry=(90 if z1 < z0 else -90), opts={'color': col}, keys=[k(t0, to=[x, 0, z1], dur=dur, ease='linear')])

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S03', 1.0, 'mec', 'beard'), ('S07', 1.0, 'flic1', 'tug'), ('S09', 1.0, 'mec', 'nest'), ('S13', 1.0, 'president', 'watch'), ('S14', 0.8, 'mec', 'green'), ('S16', 0.8, 'mec', 'step'), ('S19', 0.6, 'mec', 'end')]:
    st.gag(*g_)
st.card('S08', 'AMENDE', at=0.35)
st.card('S11', 'BRAVO', at=0.45)
st.card('S14', 'VERT', at=0.25)

# 1: the hook. Over his shoulder at the kerb: across the road the little red man of the pedestrian light; a car goes by between them; he waits, deadpan
D1 = st.dur('S01')
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT(0.9))],
        props=[RED(), ZEBRA(), CAR('car1', -2.4, 14.0, -14.0, 0.2, 1.2, '#E0413A')],
        cams=[FC(0.0, [9.4, 2.35, 0.35], [[ME[0], 2.45, ME[2]], [ME[0], 1.85, ME[2]], [LIGHT[0], 3.55, LIGHT[2]], [LIGHT[0], 2.25, LIGHT[2]]], top=0.14, bottom=0.76, drift=(-0.12, 0.0, 0.0), lenses=range(16, 40))])   # (review 1) over his shoulder, the light big near the middle (41 x 93 px at the right edge); (stills 3) a long lens: the light a fifth of the frame
st.cue('sfx:engine', 'S01', 0.2, 0.3)

# 2: the light never turned green. Close on the light: the red man lit; the green lens below grey, a spider in its web across it
D2 = st.dur('S02'); SP2 = [r(LIGHT[0] + 0.24), 2.5, LIGHT[2]]
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('araignee', SP2, 90, 'idle', 'neutral', scale=0.5, keys=[k(0.0, look='camera'), k(0.6, expr='closed'), k(0.7, expr='neutral')])],
        props=[RED(web=True)],
        cams=[FC(0.0, [-3.9, 2.7, 2.3], [[LIGHT[0], 3.6, LIGHT[2]], [LIGHT[0], 2.25, LIGHT[2]]], top=0.18, bottom=0.72, drift=(0.0, 0.0, -0.15))])

# 3: that was twelve years ago. Chest-up on him: in one shot his beard grows down out of the frame, his eyes on the light, two slow blinks
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[*WAIT(), k(0.5, toon={'face': {'lid': 1.0}}, toonDur=0.15), k(0.75, toon={'face': DEAD}, toonDur=0.15)])],
        props=[RED(), BEARD(s=0.2, keys=[k(0.0, scale=1.5, dur=r(D3 - 0.1), ease='inOut')])],
        cams=[FC(0.0, [3.6, 1.95, 1.15], [[ME[0], 2.45, ME[2]], [ME[0], 1.2, ME[2]]], top=0.14, bottom=0.74)])
st.cue('sfx:stretch', 'S03', 0.1, 0.25)

# 4: his beard touches the pavement. Low on the pavement: the end of the beard coiled on the paving stones, a pigeon pecking at it
D4 = st.dur('S04')
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT(1.1)),
        act('pigeon', [r(ME[0] - 0.7), 0, 0.95], -150, 'eat', 'neutral', scale=1.6, keys=[k(0.0, look=[r(ME[0] - 0.5), 0.02, 0.1])])],   # (review 1) pecking at the tip, beside it (it stood in front of the point of the line)
        props=[RED(), ZEBRA(), BEARD()],
        cams=[FC(0.0, [3.6, 0.24, 1.4], [[r(ME[0] - 0.6), 0.0, 0.0], [r(ME[0] - 0.95), 0.0, 0.6], [ME[0], 2.45, ME[2]], [ME[0], 0.6, ME[2]]], top=0.12, bottom=0.82)])   # low on the stones, looking up the beard to his face
st.cue('sfx:cluck', 'S04', 0.4, 0.15)

# 5: the town hall built him a house on the crossing. A little house round him at the kerb, its door open on the road; the mayor in his sash shows it
#    off to us with a sweep of the hand
D5 = st.dur('S05'); MA5 = [r(ME[0] - 1.05), 0, -1.7]   # (audit) on the far side of the doorway: in front, he hid him
SHOW5 = lambda x, y, z, lid=0.0: {'reach': {'R': [r(x), y, z, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': lid}}
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT(1.6)),
        act('maire', MA5, -25, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.2, toon=SHOW5(ME[0] - 0.45, 1.7, -1.1), toonDur=0.3, toonEase='out'),
            k(1.2, toon=SHOW5(ME[0] - 0.4, 2.4, -0.9, 0.2), toonDur=0.45, toonEase='inOut'), k(2.1, toon=SHOW5(ME[0] - 0.45, 1.7, -1.1), toonDur=0.45, toonEase='inOut')])],   # (review 1) he shows it off: a sweep up to the roof and back
        props=[RED(), ZEBRA(), BEARD(), HOUSE()],
        cams=[FC(0.0, [1.4, 1.5, 5.4], [[ME[0], 2.45, ME[2]], [r(ME[0] + 0.05), 3.75, 0.0], [MA5[0], 2.45, MA5[2]], [MA5[0], 0.0, MA5[2]], [ME[0], 0.0, -1.3], [ME[0], 0.0, 1.3]], top=0.14, bottom=0.78)])   # (review 1) the house round him, him in its doorway, the mayor whole beside it (pressed to a house front, a lamp post and a tree behind the mayor's head)

# 6: the postman delivers his mail at the light. The postman holds out a letter; his hand takes it without his eyes leaving the light
D6 = st.dur('S06'); TAKE6 = 0.85
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -90, 'stand', 'neutral', keys=[*WAIT(), k(r(TAKE6 - 0.25), toon={'reach': {'R': [ME[0], 1.3, 0.5, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': DEAD}, toonDur=0.2, toonEase='inOut'),
            k(TAKE6, toon={'reach': {'R': [ME[0], 1.3, 0.5, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': DEAD}, toonDur=0.05), k(r(TAKE6 + 0.15), toon={'touch': {'R': ['torso', -0.36, 0.55, 0.3, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': DEAD}, toonDur=0.25)]),   # (stills 3) held out beside the beard (in front of his chest it vanished into it)
        act('facteur', [r(ME[0] - 0.25), 0, 1.3], 180, 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 1.9, ME[2]]), k(0.0, toon={'reach': {'R': [ME[0], 1.3, 0.55, 1, 0.03]}, 'hands': {'R': 'pinch'}}, toonDur=0.0),
            k(r(TAKE6 + 0.05), toon={'reach': {'R': [ME[0], 1.2, 0.8, 0, 0.03]}, 'hands': {'R': 'open'}}, toonDur=0.25)])],
        props=[RED(), BEARD(), HOUSE(), PILE(n=18), P('lettre6', 'envelope', on={'actor': 'facteur', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, face='camera', opts={'w': 0.34}, keys=[k(TAKE6, attach='mec', hand='R', offset=[0.0, 0.0, 0.03], face='camera')]),
               P('bal6', 'mailbox', pos=[r(ME[0] - 0.55), 0, -0.95], ry=-90)],
        cams=[FC(0.0, [3.2, 1.8, 0.9], [[ME[0], 2.45, ME[2]], [r(ME[0] - 0.25), 2.45, 1.3], [ME[0], 1.1, 0.6], [ME[0], 1.1, -0.5]], top=0.16, bottom=0.74)])   # (review 1) nearer the hand-over, the letter big between them (30 px, cut by the edge); (stills 3) more in front of him (he was cut by the edge)
st.cue('sfx:paper', 'S06', TAKE6, 0.25)

# 7: a policeman tried to make him cross. The policeman pulls him by the arm toward the road, leaning back, his arm stretching; he does not budge
D7 = st.dur('S07'); SNAP7 = 1.5
TUG = lambda a: {'lay': [r(-a), 0.0], 'touch': {'R': ['@mec.handR', 0.0, 0.0, 0.0, 1, 0.0], 'L': ['@mec.handR', 0.05, 0.02, 0.0, 1, 0.0]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'legL': [-0.3, 0, 0, 1, None], 'shinL': [0.4, 0, 0, 1, None]}, 'face': {'mouth': 'clench', 'brow': -0.7, 'sweat': 1.0, 'eye': 0.2}}
FX7 = [(0.0, 4.45), (0.25, 4.05), (0.55, 4.25), (0.8, 3.8), (1.15, 3.55)]   # where the policeman stands: heave, heave, a slip forward, heave, heave
ARM7 = lambda x: {'reach': {'R': [r(x + 0.55), 1.25, 0.12, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': DEAD}   # his hand held out in the policeman's grip, the arm stretching to it
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -60, 'stand', 'neutral', keys=[*WAIT(), k(0.0, toon=ARM7(FX7[0][1]), toonDur=0.0), *[k(t_, toon=ARM7(x_), toonDur=0.14, toonEase='out') for t_, x_ in FX7[1:]],
            k(SNAP7, toon={'reach': {'R': [r(ME[0] - 0.2), 1.05, 0.28, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': DEAD, 'settle': 0.6}, toonDur=0.06, toonEase='out')]),   # (review 1) the arm snaps home and wobbles (the stretch was on the policeman's arm)
        act('flic1', [FX7[0][1], 0, 0.15], 60, 'stand', 'determined', keys=[k(0.0, look=[ME[0], 1.9, ME[2]]), k(0.0, toon=TUG(0.2), toonDur=0.0),
            *[kk for t_, x_ in FX7[1:] for kk in (k(t_, to=[x_, 0, 0.15], dur=0.14, ease='out', face='keep'), k(t_, toon=TUG(0.38 if x_ < 4.2 else 0.12), toonDur=0.12, toonEase='out'))],
            k(SNAP7, to=[3.25, 0, 0.15], dur=0.12, ease='out', face='keep'), k(SNAP7, toon={'lay': [-0.9, 0.0], 'face': {'eye': 0.6, 'brow': 0.9, 'mouth': 'open'}}, toonDur=0.08, toonEase='out'),   # the grip goes: flung back...
            k(1.62, toon={'lay': [-1.5, 0.0], 'sq': [1.3, 0.32, 1.3], 'face': {'eye': 0.5, 'pop': 0.4, 'popLen': 0.12}}, toonDur=0.05, toonEase='in'),   # ...flat on his back...
            k(1.85, toon={'lay': [-1.5, 0.0], 'sq': [0.85, 1.22, 0.85], 'face': {'eye': 0.3}}, toonDur=0.1, toonEase='out'), k(2.0, toon={'lay': [-1.5, 0.0], 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.5}}, toonDur=0.12)])],   # ...re-inflating
        props=[RED(), ZEBRA(), BEARD(), HOUSE(), PILE()],
        cams=[FC(0.0, [4.3, 1.5, 4.6], [[ME[0], 2.45, ME[2]], [3.55, 2.4, 0.15], [3.0, 0.0, 0.15], [ME[0], 0.0, ME[2]]], top=0.16, bottom=0.78, drift=(-0.9, 0.0, 0.0))])   # side on, both faces in (the policeman's face left the frame); (stills 3) panning left with the fling
st.cue('sfx:stretch', 'S07', 0.25, 0.25); st.cue('sfx:stretch', 'S07', 0.8, 0.25); st.cue('sfx:grunt', 'S07', 1.15, 0.2); st.cue('sfx:boing', 'S07', SNAP7, 0.3); st.cue('thud', 'S07', 1.62, 0.3)

# 8: the policeman got a fine. On the crossing, red still lit: his colleague writes him a ticket and hands it over; his jaw drops (AMENDE)
D8 = st.dur('S08'); TIC8 = 0.6
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('flic1', [2.7, 0, 0.3], 70, 'stand', 'neutral', keys=[k(0.0, look=[3.5, 1.9, 0.9]),
            k(r(TIC8 + 0.02), toon={'sq': [1.12, 0.86, 1.12], 'face': {'eye': 0.3, 'brow': 0.6}}, toonDur=0.05, toonEase='out'),   # (review 1) slapped: squashed...
            k(r(TIC8 + 0.12), look='camera'), k(r(TIC8 + 0.12), toon={'sq': [0.94, 1.1, 0.94], 'bend': {'neck': [0, 0, 0, 1.25, None]}, 'face': {'jaw': 1.0, 'eye': 0.85, 'pop': 0.5, 'popLen': 0.14, 'brow': 1.0}}, toonDur=0.08, toonEase='out'),   # ...the jaw to his chest, eyes on stalks, to us
            k(r(TIC8 + 0.7), toon={'bend': {'neck': [0, 0, 0, 1.18, None]}, 'face': {'jaw': 0.9, 'eye': 0.7, 'pop': 0.3, 'popLen': 0.12, 'brow': 0.9}}, toonDur=0.2)]),   # (the closed arched eyes read as laughter)
        act('flic2', [3.55, 0, 0.95], -120, 'stand', 'neutral', keys=[k(0.0, look=[2.7, 1.9, 0.3]), k(0.0, toon={'reach': {'R': [3.25, 1.35, 0.6, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.4}}, toonDur=0.0),
            k(r(TIC8 - 0.12), toon={'reach': {'R': [2.95, 1.45, 0.42, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4}}, toonDur=0.1, toonEase='in'), k(r(TIC8 + 0.1), toon={'reach': {'R': [3.3, 1.2, 0.8, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45}}, toonDur=0.2)]),   # SLAP
        act('mec', ME, -90, 'stand', 'neutral', keys=WAIT(0.7))],
        props=[RED(), ZEBRA(), BEARD(), HOUSE(), PILE(n=24), P('pv8', 'bigTicket', on={'actor': 'flic2', 'hand': 'R', 'offset': [0.0, 0.0, 0.04]}, face='camera', opts={'title': 'CONTRAVENTION', 'sum': '135 €'}, keys=[k(TIC8, attach='flic1', joint='torso', offset=[0.0, 0.55, 0.34])])],   # (review 1) a big ticket stuck on his chest (20 x 10 px hidden in the clasped hands: a handshake)
        cams=[FC(0.0, [1.9, 1.75, 3.4], [[2.7, 2.6, 0.3], [3.55, 2.5, 0.95], [2.7, 1.15, 0.3]], top=0.2, bottom=0.78, lenses=range(26, 66))])   # (stills 3) waist up: the faces and the ticket
st.cue('thud', 'S08', TIC8, 0.3); st.cue('sfx:gasp', 'S08', r(TIC8 + 0.12), 0.25)

# 9: the pigeons nested in his beard. Close: a straw nest in the beard, a pigeon sitting in it, eggs popping in one after another; he blinks
D9 = st.dur('S09'); LAY9 = [0.3, 0.6, 0.9]
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[*WAIT(), k(1.0, toon={'face': {'lid': 1.0}}, toonDur=0.08), k(1.12, toon={'face': DEAD}, toonDur=0.1)]),
        act('pigeon', [r(ME[0] - 0.22), 1.6, 0.16], -110, 'idle', 'neutral', scale=1.3, keys=[k(0.0, look='camera'), *[kk for t_ in LAY9 for kk in (k(r(t_ + 0.02), toon={'sq': [1.15, 0.85, 1.15]}, toonDur=0.04, toonEase='out'), k(r(t_ + 0.1), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.08))]])],   # (review 1) on the rim of the nest, a jolt at each egg
        props=[RED(), BEARD(), HOUSE(), NEST('nid9', LAY9)],
        cams=[FC(0.0, [4.4, 1.45, -1.0], [[ME[0], 2.45, ME[2]], [ME[0], 1.0, ME[2]], [r(ME[0] - 0.3), 1.9, 0.0]], top=0.14, bottom=0.74)])   # (audit) from his other side and lower: not S03's frame
for t_ in LAY9: st.cue('pop', 'S09', t_, 0.15)

# 10: tourists queue for the photo. Along the pavement a queue of tourists; the first one photographs him: a flash; the next one steps up
D10 = st.dur('S10'); FL10 = [0.4, 1.1]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT(1.3)),
        *[act(f'tour{j + 1}', [r(ME[0] + 0.3 + 0.75 * j), 0, r(1.55 + 0.55 * j)], -150, 'stand', 'happy', keys=[k(0.0, look=[ME[0], 1.9, ME[2]]),
            *([k(0.0, toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0)] if j == 0 else []),
            *([kk for i_ in range(4) for kk in (k(r(0.2 + 0.45 * i_), to=[r(ME[0] + 2.55), 0.18, 3.2], dur=0.1, ease='out'), k(r(0.3 + 0.45 * i_), to=[r(ME[0] + 2.55), 0, 3.2], dur=0.1, ease='in'))] if j == 3 else [])]) for j in range(4)]],   # (review 1) the kid hops on the spot
        props=[RED(), ZEBRA(), BEARD(), HOUSE(), NEST(), PILE(), P('cam10', 'pressCamera', on={'actor': 'tour1', 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': FL10, 'burst': 0.5})],
        cams=[FC(0.0, [3.7, 1.35, 2.7], [[ME[0], 2.45, ME[2]], [r(ME[0] + 1.05), 2.45, 2.1], [ME[0], 0.6, ME[2]]], top=0.16, bottom=0.76)])   # (review 1) lower and nearer: the queue runs out of the frame (a third of the frame was empty road)
for t_ in FL10: st.cue('sfx:click', 'S10', t_, 0.25)

# 11: the government decorated him for his patience. A minister pins a medal on his chest and steps back to clap; he does not take his eyes off the
#     light (BRAVO)
D11 = st.dur('S11'); PIN11 = 0.5
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT(1.5)),
        act('ministre', [r(ME[0] - 0.7), 0, -0.65], 30, 'stand', 'happy', keys=[k(0.0, look=[ME[0], 1.55, ME[2]]), k(0.0, toon={'reach': {'R': [r(ME[0] - 0.2), 1.55, -0.15, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'smile'}}, toonDur=0.0),
            k(r(PIN11 + 0.15), look='camera'), k(r(PIN11 + 0.15), toon={'touch': {'R': ['torso', -0.05, 0.5, 0.3, 1, 0.03], 'L': ['torso', 0.05, 0.5, 0.3, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.15),
            *[k(r(PIN11 + 0.35 + 0.18 * j), toon={'touch': {'R': ['torso', r(-0.05 + (0.03 if j % 2 else 0.0)), 0.5, 0.3, 1, 0.03], 'L': ['torso', r(0.05 - (0.03 if j % 2 else 0.0)), 0.5, 0.3, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.06) for j in range(5)]])],   # clapping
        props=[RED(), BEARD(), HOUSE(), NEST(), PILE(), MEDAL('med11', keys=[k(0.0, scale=0.01, dur=0.0), k(PIN11, scale=1.4, dur=0.08, ease='outBack')])],
        cams=[FC(0.0, [3.6, 1.75, 2.4], [[ME[0], 2.45, ME[2]], [r(ME[0] - 0.7), 2.45, -0.65], [ME[0], 1.0, ME[2]]], top=0.2, bottom=0.74)])   # (stills 1) the minister beside him (from behind he hid the medal)
st.cue('sfx:clink', 'S11', PIN11, 0.3); st.cue('sfx:fanfare', 'S11', r(PIN11 + 0.3), 0.18)

# 12: the president came to wait with him. Side by side at the kerb, the president and him, both deadpan, eyes on the light; two bodyguards behind
D12 = st.dur('S12'); BL12 = 1.2; PR = [r(ME[0] - 0.1), 0, 1.0]
BACK = lambda lid: {'touch': {'R': ['torso', 0.0, 0.25, -0.25, 1, 0.03], 'L': ['torso', 0.0, 0.25, -0.27, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': lid}}
TWO = lambda: [k(0.0, toon=BACK(0.45), toonDur=0.0), k(BL12, toon=BACK(1.0), toonDur=0.08), k(r(BL12 + 0.12), toon=BACK(0.45), toonDur=0.1)]   # the same pose and the same blink, together
GU = [[r(ME[0] + 0.45), 0, 1.95], [r(ME[0] + 0.95), 0, 2.65]]
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 3.2, LIGHT[2]]), *TWO()]),
        act('president', PR, -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 3.2, LIGHT[2]]), *TWO()]),
        *[act(f'garde{j + 1}', GU[j], -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 2.0, LIGHT[2]])]) for j in range(2)]],
        props=[RED(), ZEBRA(), BEARD(), HOUSE(), NEST(), MEDAL(), PILE(), PIN('pin12'), SHADES('sh12a', 'garde1'), SHADES('sh12b', 'garde2')],
        cams=[FC(0.0, [r(ME[0] - 2.9), 1.65, 0.6], [[ME[0], 2.5, ME[2]], [PR[0], 2.5, PR[2]], [ME[0], 1.1, ME[2]], [PR[0], 1.1, PR[2]], [GU[0][0], 2.5, GU[0][2]]], top=0.16, bottom=0.76)])   # (review 1) from the front, the two of them side by side (him pushed to the edge, a guard between them)

# 13: he left after ten minutes. The president looks at his watch, puffs out his cheeks and walks off with his bodyguards; he stays
D13 = st.dur('S13'); GO13 = 1.05
WT = lambda dy: {'touch': {'L': ['face', 0.05, 0.05, 0.3, 1, 0.03], 'R': ['@president.handL', 0.0, r(dy), 0.0, 1, 0.0]}, 'hands': {'L': 'open', 'R': 'point'}, 'face': {'gy': 0.6, 'eye': 0.3}}
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT(0.8)),
        act('president', PR, -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 3.2, LIGHT[2]]),
            k(0.05, toon={'touch': {'L': ['face', 0.05, 0.05, 0.3, 1, 0.03]}, 'hands': {'L': 'open'}, 'face': {'gy': 0.6, 'eye': 0.3}}, toonDur=0.08, toonEase='out'),   # (review 1) the wrist whipped up to his eyes...
            k(0.17, toon=WT(0.03), toonDur=0.05), k(0.24, toon=WT(0.09), toonDur=0.04), k(0.3, toon=WT(0.03), toonDur=0.04),   # ...two taps on the glass...
            k(0.42, toon={'touch': {'L': ['face', 0.21, 0.12, -0.02, 1, 0.03]}, 'hands': {'L': 'open'}, 'face': {'gx': -0.5, 'lid': 0.3, 'brow': 0.5}}, toonDur=0.1, toonEase='inOut'),   # ...held to his ear...
            k(0.62, toon={'scl': {'head': [1.08, 1.04, 1.08]}, 'face': {'puff': 1.0, 'swell': 1.0, 'mouth': 'kiss', 'lid': 0.3}}, toonDur=0.12, toonEase='out'),   # ...the cheeks balloon...
            k(0.86, toon={'scl': {'head': [0.97, 0.99, 0.97]}, 'face': {'puff': 0.0, 'mouth': 'open', 'lid': 0.5}}, toonDur=0.06, toonEase='out'),   # ...a huff...
            k(GO13, to=[r(ME[0] + 3.0), 0, 3.8], dur=r(D13 - GO13), clip='walk', ease='in', face='keep'), k(GO13, toon={}, toonDur=0.15)]),   # ...and off with his guards in step
        *[act(f'garde{j + 1}', GU[j], -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 2.0, LIGHT[2]]), k(GO13, to=[r(GU[j][0] + 3.6), 0, r(GU[j][2] + 2.5)], dur=r(D13 - GO13), clip='walk', ease='in', face='keep')]) for j in range(2)]],
        props=[RED(), ZEBRA(), BEARD(), HOUSE(), NEST(), MEDAL(), PILE(), PIN('pin13'), SHADES('sh13a', 'garde1'), SHADES('sh13b', 'garde2'), P('montre13', 'wristWatch', on={'actor': 'president', 'hand': 'L', 'offset': [0.0, 0.04, 0.0]}, opts={'bright': True, 'both': True})],
        cams=[FC(0.0, [r(ME[0] - 2.3), 1.75, 2.2], [[PR[0], 2.55, PR[2]], [PR[0], 1.2, PR[2]], [ME[0], 2.45, ME[2]]], top=0.16, bottom=0.76)])   # (review 1) medium on the president with him in the frame (a wide shot: heads 5 % of the frame, no watch look, no cheeks)

# 14: yesterday the light turned green. Close on the light: the red goes out, the green lights up with a pop, the spider drops off on its thread (VERT)
D14 = st.dur('S14'); GREEN14 = 0.35; SPX14 = r(LIGHT[0] + 0.3); AN14 = 2.86
YS14 = [(r(GREEN14 + 0.03), 2.38, 0.08, 'out'), (1.2, 1.0, 0.12, 'in'), (1.32, 1.35, 0.12, 'out'), (1.44, 1.08, 0.12, 'in'), (1.56, 1.25, 0.12, 'out'), (1.68, 1.15, 0.15, 'inOut')]   # the spider's height: out, the drop, a bungee bounce
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[act('araignee', [r(LIGHT[0] + 0.24), 2.5, LIGHT[2]], 90, 'idle', 'neutral', scale=0.65, keys=[k(0.0, look='camera'),
            *[k(t_, to=[SPX14, y_, LIGHT[2]], dur=d_, ease=e_) for t_, y_, d_, e_ in YS14],
            k(YS14[0][0], toon={'sq': [0.75, 1.35, 0.75]}, toonDur=0.04, toonEase='out'), k(r(GREEN14 + 0.12), toon={'sq': [1.3, 0.75, 1.3]}, toonDur=0.08, toonEase='out'),   # (review 1) stretched as it jumps, then splayed in mid-air...
            k(1.2, toon={'sq': [0.8, 1.3, 0.8]}, toonDur=0.06), k(1.32, toon={'sq': [1.2, 0.85, 1.2]}, toonDur=0.05), k(1.6, toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.1),
            k(0.8, expr='closed'), k(0.9, expr='neutral')])],   # ...a look at us and a blink before the drop (it dropped out of the frame and nothing moved for 1.3 s)
        props=[RED(state=[[0.0, 'r'], [GREEN14, 'g']], web=True), P('fil14', 'thread', pos=[SPX14, AN14, LIGHT[2]], opts={'keys': [[0.0, 0.0, 0.0], *[[t_, r(AN14 - y_ - 0.12), d_, e_] for t_, y_, d_, e_ in YS14]]})],
        cams=[FC(0.0, [-3.6, 2.1, 2.2], [[LIGHT[0], 3.6, LIGHT[2]], [LIGHT[0], 0.95, LIGHT[2]]], top=0.2, bottom=0.74)])
st.cue('sfx:ding', 'S14', GREEN14, 0.4); st.cue('sfx:boing', 'S14', 1.32, 0.25)

# 15: television from all over the world was there. Behind barriers along the pavement, TV cameras on tripods and reporters, flashes going off
D15 = st.dur('S15'); FL15 = [0.3, 0.55, 0.8, 1.1, 1.4, 1.7]
MIC15 = [('INFO', '#C8322A'), ('JT', '#2F62B5'), ('DIRECT', '#E8A33C')]
REP15 = [[r(ME[0] - 1.25), 0, 0.75], [r(ME[0] - 1.45), 0, -0.55], [r(ME[0] - 1.8), 0, 1.6]]
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT(1.2)),
        *[act(f'jour{j + 1}', REP15[j], 90 - 25 * (j - 1), 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 2.0, ME[2]]), k(0.0, toon={'reach': {'R': [r(ME[0] - 0.5), 1.65, r(REP15[j][2] * 0.4), 1, 0.03]}, 'hands': {'R': 'grip'}}, toonDur=0.0)]) for j in range(3)],
        *[act(f'photo{j + 1}', [r(ME[0] - 2.3 - 0.3 * j), 0, r(-1.2 + 3.2 * j)], 90 - 40 * (j * 2 - 1), 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 2.0, ME[2]]),
            k(0.0, toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0)]) for j in range(2)]],
        props=[RED(state=[[0.0, 'g']]), ZEBRA(), BEARD(), HOUSE(), NEST(), MEDAL(), PILE(),
               *[P(f'tv15{j}', 'tvCamera', pos=[r(ME[0] - 2.0 - 0.35 * (j % 2)), 0, r(-1.9 + 0.75 * j)], ry=r(90 - 12 * (j - 3))) for j in range(7)],   # (review 1) a wall of cameras (two cameras and three reporters)
               *[P(f'mic15{j}', 'pressMic', on={'actor': f'jour{j + 1}', 'hand': 'R', 'offset': [0.0, -0.02, 0.04]}, opts={'text': MIC15[j][0], 'color': MIC15[j][1]}) for j in range(3)],
               P('boom15', 'boomMic', on={'actor': 'jour3', 'hand': 'L', 'offset': [0.0, -0.02, 0.0]}, opts={'len': 2.2, 'tilt': 0.65}),
               *[P(f'cam15{j}', 'pressCamera', on={'actor': f'photo{j + 1}', 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': FL15[j::2], 'burst': 0.6}) for j in range(2)]],
        cams=[FC(0.0, [r(ME[0] - 5.2), 1.7, 0.6], [[ME[0], 2.9, ME[2]], [ME[0], 0.0, ME[2]], [r(ME[0] - 2.0), 1.6, -1.9], [r(ME[0] - 2.0), 1.6, 2.6]], top=0.14, bottom=0.8)])   # behind the press pack, him framed in his doorway at the end of the lenses
for t_ in FL15: st.cue('sfx:click', 'S15', t_, 0.2)

# 16: he crossed. From the road: the first step off the kerb, slow, the beard dragging; dust falls off him; a crack of the knees
D16 = st.dur('S16'); STEP16 = 0.3
CREAK = lambda a, b: {'bend': {'spine': [r(a), 0, 0, 1, None], 'legL': [r(b), 0, 0, 1, None], 'shinL': [r(-b * 1.2), 0, 0, 1, None]}, 'face': DEAD}
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 3.2, LIGHT[2]]), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.04, toon=CREAK(0.04, 0.08), toonDur=0.03), k(0.1, toon=CREAK(0.0, 0.0), toonDur=0.03), k(0.16, toon=CREAK(0.06, 0.16), toonDur=0.03), k(0.22, toon=CREAK(0.02, 0.06), toonDur=0.03),   # (review 1) the joints unlock in jerks
            k(STEP16, to=[r(ME[0] - 1.3), 0, 0.0], dur=r(D16 - STEP16), clip='walk', ease='inOut', face='keep'), k(STEP16, toon={'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.3}}, toonDur=0.1)])],
        props=[RED(state=[[0.0, 'g']]), ZEBRA(), BEARD(swing=[STEP16, 1.3, 0.16]), HOUSE(), NEST(), MEDAL(), PILE(),
               P('dust16', 'dustFall', pos=[r(ME[0] - 0.05), 1.3, 0.0], opts={'at': 0.24, 'n': 22, 'floor': 1.28, 'life': 0.95})],   # once, solid, falling to the kerb (translucent shards fired twice at his shoulders)
        cams=[FC(0.0, [2.4, 0.9, 1.6], [[ME[0], 2.45, ME[2]], [r(ME[0] - 1.3), 0.0, 0.0], [ME[0], 0.0, ME[2]]], top=0.16, bottom=0.8, drift=(-0.6, 0.0, 0.0))])
st.cue('sfx:crunch', 'S16', 0.05, 0.25); st.cue('sfx:crunch', 'S16', 0.17, 0.25); st.cue('sfx:step', 'S16', r(STEP16 + 0.4), 0.2)

# 17: the crowd wept. Behind the barriers: the reporters and onlookers in tears, one blowing his nose, confetti coming down
D17 = st.dur('S17')
SOB = lambda w: {'face': {'tears': 1.0, 'mouth': 'sob', 'brow': 0.9, 'lid': 0.45}, 'sq': [r(1 + 0.03 * w), r(1 - 0.035 * w), r(1 + 0.03 * w)], 'bend': {'spine': [r(0.07 * w), 0, 0, 1, None]}}
CROWD17 = [('jour1', [3.3, 0, 2.2], 160), ('jour2', [4.1, 0, 2.65], 180), ('jour3', [4.9, 0, 2.25], -160)]
WRING = lambda a: {'face': {'tears': 1.0, 'mouth': 'sob', 'brow': 0.9, 'lid': 0.6}, 'touch': {'R': ['face', -0.06, 0.05, 0.22, 1, 0.02], 'L': ['face', 0.06, 0.05, 0.22, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [r(0.08 * a), 0, 0, 1, None]}}
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[*[act(pid_, pos_, ry_, 'stand', 'neutral', keys=[k(0.0, look=[4.6, 1.8, 0.0]), *[k(r(0.05 * j + 0.14 * i), toon=SOB(1.0 if i % 2 else 0.0), toonDur=0.07) for i in range(10)]]) for j, (pid_, pos_, ry_) in enumerate(CROWD17)],   # (review 1) sobs heaving their shoulders, three-quarters to us (profiles, faces edge on)
        act('tour1', [4.5, 0, 3.25], 175, 'stand', 'neutral', keys=[k(0.0, look=[4.6, 1.8, 0.0]), *[k(r(0.12 * i), toon=WRING(1.0 if i % 2 else 0.0), toonDur=0.06) for i in range(12)]])],   # wringing the handkerchief
        props=[*[P(f'tf17{j}', 'tearFountain', on={'actor': pid_, 'joint': 'head', 'offset': [0.0, 0.24, 0.17]}, opts={'at': r(0.05 * j), 'dx': 0.09}) for j, (pid_, _, _) in enumerate(CROWD17)],
               P('hk17', 'slab', on={'actor': 'tour1', 'hand': 'R', 'offset': [0.04, 0.0, 0.03]}, opts={'w': 0.2, 'h': 0.16, 'd': 0.01, 'color': '#FFFFFF'}, keys=[*[k(r(0.12 * i), rotTo=[0.0, 0.0, 0.5 if i % 2 else -0.5], dur=0.1, ease='inOut') for i in range(12)]]),
               P('conf17', 'confettiRain', pos=[4.1, 0.0, 1.3], opts={'w': 3.2, 'h': 3.4, 'd': 1.0, 'n': 170})],   # raining in front of the lens (specks in draft 1)
        cams=[FC(0.0, [4.1, 1.65, -0.4], [[3.3, 2.45, 2.2], [4.9, 2.45, 2.25], [4.1, 1.25, 2.65]], top=0.16, bottom=0.76)])
st.cue('sfx:sniff', 'S17', 0.3, 0.25); st.cue('sfx:sniff', 'S17', 0.9, 0.2)

# 18: on the other side there was a red light. On the far kerb he arrives under another pedestrian light, for the side street: red
D18 = st.dur('S18'); FAR18 = [-5.55, 0, 0.0]; FEU2 = [-6.9, 0, -0.5]
st.shot('S18', 'parisStreet', setOpts=STREET, actors=[act('mec', [-2.9, 0, 0.0], -90, 'walk', 'neutral', keys=[k(0.2, to=FAR18, dur=1.2, clip='walk', then='stand', ease='out', face='keep'), k(0.0, look=[-5.6, 1.8, -2.0]), k(1.45, look=[FEU2[0], 3.8, FEU2[2]]), k(1.45, toon={'face': DEAD}, toonDur=0.1)])],
        props=[RED('feu2', pos=FEU2, ry=40, h=2.9), ZEBRA(), BEARD(swing=[0.2, 1.5, 0.14]), MEDAL(), NEST()],   # (stills 3) the green light he crossed at, nearer the lens, read first: out of this shot
        cams=[FC(0.0, [-3.6, 2.0, 3.6], [[FEU2[0], 4.15, FEU2[2]], [FEU2[0], 0.0, FEU2[2]], [FAR18[0], 2.45, FAR18[2]], [FAR18[0], 0.0, FAR18[2]]], top=0.14, bottom=0.78)])   # (review 1) the red light first, high and to the side; he walks in under it (it merged with his head)
st.cue('sfx:ding', 'S18', 1.45, 0.15)

# 19: he is waiting. Him under the new red light, deadpan, the beard to the ground; a pigeon lands on his head; a look at us
D19 = st.dur('S19'); LAND19 = 0.82
st.shot('S19', 'parisStreet', setOpts=STREET, actors=[act('mec', FAR18, -25, 'stand', 'neutral', keys=[k(0.0, look=[FEU2[0], 3.8, FEU2[2]]), k(0.0, toon={'face': DEAD}, toonDur=0.0), k(0.55, look='camera'),
            k(r(LAND19 + 0.01), toon={'scl': {'head': [1.06, 0.88, 1.06]}, 'face': {'lid': 0.5}}, toonDur=0.04, toonEase='out'), k(r(LAND19 + 0.08), toon={'scl': {'head': [0.97, 1.05, 0.97]}, 'face': DEAD}, toonDur=0.06), k(r(LAND19 + 0.18), toon={'scl': {'head': [1.0, 1.0, 1.0]}, 'face': DEAD}, toonDur=0.08),   # (review 1) the pigeon lands: his head squashes and springs back
            k(1.18, toon={'face': {'lid': 1.0}}, toonDur=0.14, toonEase='inOut'), k(1.42, toon={'face': DEAD}, toonDur=0.14, toonEase='inOut')]),   # one slow blink in the end hold
        act('pigeon', [-3.9, 3.6, 1.6], -120, 'fly', 'neutral', scale=1.3, keys=[k(0.0, to=[FAR18[0], 2.5, FAR18[2]], dur=LAND19, ease='out'), k(LAND19, clip='idle'), k(0.6, look='camera'),
            k(LAND19, toon={'sq': [1.35, 0.65, 1.35]}, toonDur=0.04, toonEase='out'), k(r(LAND19 + 0.08), toon={'sq': [0.88, 1.15, 0.88]}, toonDur=0.06), k(r(LAND19 + 0.2), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.1)])],   # (review 1) it lands (it hung in the air to the cut): a squash, wings folded, a settle
        props=[RED('feu2', pos=FEU2, ry=40, h=2.9), BEARD(), MEDAL(), NEST()],
        cams=[FC(0.0, [-3.4, 1.7, 3.6], [[FAR18[0], 2.95, FAR18[2]], [FEU2[0], 4.15, FEU2[2]], [FAR18[0], 0.7, FAR18[2]]], top=0.14, bottom=0.76)])
st.cue('sfx:cluck', 'S19', LAND19, 0.2)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le feu rouge", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'araignee': {'type': 'creature', 'name': 'spider', 'opts': {'seed': 666}},
    'pigeon': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 667}},
    'maire': {'preset': 'politique', 'seed': 668, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'hairColor': '#BDBDBD', 'suit': '#A9A397', 'lapel': '#A9A397', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'facteur': {'preset': 'officiel', 'seed': 669, 'suit': '#2F5FA8', 'hat': 'copcap', 'hatColor': '#F2C230', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic1': {'preset': 'cop', 'seed': 670, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic2': {'preset': 'cop2', 'seed': 671, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'tour1': {'preset': 'tourist', 'seed': 672, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'tour2': {'preset': 'tourist', 'seed': 673, 'suit': '#E0813A', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'tour3': {'preset': 'femme', 'seed': 674, 'suit': '#3A9BDC', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'tour4': {'preset': 'gamin', 'seed': 675, 'suit': '#7CC25A', 'build': {'headScale': 1.25}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 676, 'suit': '#33363D', 'lapel': '#33363D', 'tie': '#2F62B5', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 677, 'suit': '#4A4D55', 'lapel': '#4A4D55', 'tie': '#9A1F2E', 'hairColor': '#D2D2D2', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'garde1': {'preset': 'politique', 'seed': 678, 'suit': '#15171C', 'lapel': '#15171C', 'tie': '#15171C', 'hairColor': '#2A2A2A', 'glasses': False, 'build': {'width': 1.15, 'headWidth': 1.2}, 'toon': EX},
    'garde2': {'preset': 'politique', 'seed': 679, 'suit': '#15171C', 'lapel': '#15171C', 'tie': '#15171C', 'hairColor': '#3A3530', 'glasses': False, 'build': {'width': 1.15, 'headWidth': 1.2}, 'toon': EX},
    'photo1': {'preset': 'journaliste', 'seed': 683, 'suit': '#5E7A54', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'photo2': {'preset': 'journaliste', 'seed': 684, 'suit': '#A0522D', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'jour1': {'preset': 'journaliste', 'seed': 680, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'jour2': {'preset': 'journaliste', 'seed': 681, 'suit': '#7A5C8E', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'jour3': {'preset': 'madame', 'seed': 682, 'suit': '#C255C8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
})
