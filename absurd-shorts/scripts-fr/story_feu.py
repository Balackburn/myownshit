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
RED = lambda pid='feu', state=None, pos=LIGHT, ry=90: P(pid, 'trafficLight', pos=pos, ry=ry, opts={'h': 2.7, 'state': state or [[0.0, 'r']]})
ZEBRA = lambda pid='zeb': P(pid, 'zebra', pos=[-5.0, 0.012, -1.5], opts={'n': 10})
BEARD = lambda pid='barbe', s=1.5, keys=None: P(pid, 'beard', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.05, 0.09]}, scale=s, flat=[1.35, 3.6, 1.0], opts={'color': '#A39C92'}, **({'keys': keys} if keys else {}))   # (stills 1) a scalar scale and `flat` (a list scale drew nothing)
WAIT = lambda: [k(0.0, look=[LIGHT[0], 2.5, LIGHT[2]]), k(0.0, toon={'face': DEAD}, toonDur=0.0)]   # his eyes on the light across the road
CAR = lambda pid, x, z0, z1, t0, dur, col: P(pid, 'car', pos=[x, 0, z0], ry=(90 if z1 < z0 else -90), opts={'color': col}, keys=[k(t0, to=[x, 0, z1], dur=dur, ease='linear')])

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S03', 1.0, 'mec', 'beard'), ('S07', 1.0, 'flic1', 'tug'), ('S09', 1.0, 'mec', 'nest'), ('S13', 1.0, 'president', 'watch'), ('S14', 0.8, 'mec', 'green'), ('S16', 0.8, 'mec', 'step'), ('S19', 0.6, 'mec', 'end')]:
    st.gag(*g_)
st.card('S08', 'AMENDE', at=0.35)
st.card('S11', 'BRAVO', at=0.45)
st.card('S14', 'VERT', at=0.25)

# 1: the hook. Over his shoulder at the kerb: across the road the little red man of the pedestrian light; a car goes by between them; he waits, deadpan
D1 = st.dur('S01')
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT())],
        props=[RED(), ZEBRA(), CAR('car1', -2.4, 14.0, -14.0, 0.2, 1.2, '#E0413A')],
        cams=[FC(0.0, [8.2, 2.05, -1.8], [[ME[0], 2.45, ME[2]], [ME[0], 0.9, ME[2]], [LIGHT[0], 2.7, LIGHT[2]], [LIGHT[0], 1.6, LIGHT[2]]], top=0.14, bottom=0.76, drift=(-0.2, 0.0, 0.1))])
st.cue('sfx:engine', 'S01', 0.2, 0.3)

# 2: the light never turned green. Close on the light: the red man lit; the green lens below grey, a spider in its web across it
D2 = st.dur('S02')
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[act('araignee', [r(LIGHT[0] + 0.16), 1.87, LIGHT[2]], 90, 'idle', 'neutral', scale=0.5, keys=[k(0.0, look='camera')])],
        props=[RED()],
        cams=[FC(0.0, [-3.9, 2.2, 2.3], [[LIGHT[0], 2.75, LIGHT[2]], [LIGHT[0], 1.75, LIGHT[2]]], top=0.18, bottom=0.72, drift=(0.0, 0.0, -0.15))])

# 3: that was twelve years ago. Chest-up on him: in one shot his beard grows down out of the frame, his eyes on the light, two slow blinks
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[*WAIT(), k(0.5, toon={'face': {'lid': 1.0}}, toonDur=0.15), k(0.75, toon={'face': DEAD}, toonDur=0.15)])],
        props=[RED(), BEARD(s=0.2, keys=[k(0.0, scale=1.5, dur=r(D3 - 0.1), ease='inOut')])],
        cams=[FC(0.0, [3.6, 1.95, 1.15], [[ME[0], 2.45, ME[2]], [ME[0], 1.2, ME[2]]], top=0.14, bottom=0.74)])
st.cue('sfx:stretch', 'S03', 0.1, 0.25)

# 4: his beard touches the pavement. Low on the pavement: the end of the beard coiled on the paving stones, a pigeon pecking at it
D4 = st.dur('S04')
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT()),
        act('pigeon', [r(ME[0] - 0.6), 0, 0.5], -130, 'eat', 'neutral', scale=1.6, keys=[k(0.0, look=[ME[0], 0.0, ME[2]])])],
        props=[RED(), ZEBRA(), BEARD()],
        cams=[FC(0.0, [3.8, 0.45, 1.6], [[ME[0], 2.4, ME[2]], [ME[0], 0.0, ME[2]], [r(ME[0] - 0.8), 0.0, 0.6]], top=0.14, bottom=0.8)])
st.cue('sfx:cluck', 'S04', 0.4, 0.15)

# 5: the town hall built him a house on the crossing. A little house round him at the kerb, its door open on the road; the mayor in his sash shows it
#    off to us with a sweep of the hand
D5 = st.dur('S05')
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT()),
        act('maire', [3.9, 0, -1.0], 20, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.2, toon={'reach': {'R': [4.6, 1.6, -0.5, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.3, toonEase='out')])],
        props=[RED(), ZEBRA(), BEARD(), P('maison5', 'house', pos=[r(ME[0] + 1.3), 0, 0.0], ry=-90, opts={'w': 3.0, 'd': 2.6, 'h': 2.2})],
        cams=[FC(0.0, [2.2, 1.6, 6.0], [[ME[0], 2.45, ME[2]], [r(ME[0] + 1.3), 3.4, 0.0], [3.9, 2.45, -1.0], [3.9, 0.0, -1.0], [ME[0], 0.0, ME[2]]], top=0.16, bottom=0.78)])   # (stills 1) the mayor beside him (in front he hid him)

# 6: the postman delivers his mail at the light. The postman holds out a letter; his hand takes it without his eyes leaving the light
D6 = st.dur('S06'); TAKE6 = 0.85
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -90, 'stand', 'neutral', keys=[*WAIT(), k(r(TAKE6 - 0.25), toon={'reach': {'R': [ME[0], 1.3, 0.5, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': DEAD}, toonDur=0.2, toonEase='inOut'),
            k(TAKE6, toon={'reach': {'R': [ME[0], 1.3, 0.5, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': DEAD}, toonDur=0.05), k(r(TAKE6 + 0.15), toon={'touch': {'R': ['torso', -0.14, 0.45, 0.3, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': DEAD}, toonDur=0.25)]),
        act('facteur', [ME[0], 0, 1.3], 180, 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 1.9, ME[2]]), k(0.0, toon={'reach': {'R': [ME[0], 1.3, 0.55, 1, 0.03]}, 'hands': {'R': 'pinch'}}, toonDur=0.0),
            k(r(TAKE6 + 0.05), toon={'reach': {'R': [ME[0], 1.2, 0.8, 0, 0.03]}, 'hands': {'R': 'open'}}, toonDur=0.25)])],
        props=[RED(), BEARD(), P('lettre6', 'envelope', on={'actor': 'facteur', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, keys=[k(TAKE6, attach='mec', hand='R', offset=[0.0, 0.0, 0.03], face='camera')]),
               P('bal6', 'mailbox', pos=[r(ME[0] + 0.7), 0, -0.6], ry=-90)],
        cams=[FC(0.0, [3.4, 1.7, 2.6], [[ME[0], 2.45, ME[2]], [ME[0], 2.45, 1.3], [ME[0], 0.8, 0.6]], top=0.16, bottom=0.76)])
st.cue('sfx:paper', 'S06', TAKE6, 0.25)

# 7: a policeman tried to make him cross. The policeman pulls him by the arm toward the road, leaning back, his arm stretching; he does not budge
D7 = st.dur('S07')
TUG = lambda a, s: {'lay': [r(-a), 0.0], 'touch': {'R': ['@mec.handR', 0.0, 0.0, 0.0, 1, 0.0], 'L': ['@mec.handR', 0.05, 0.02, 0.0, 1, 0.0]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'armR': [0, 0, 0, r(s), None], 'legL': [-0.3, 0, 0, 1, None], 'shinL': [0.4, 0, 0, 1, None]}, 'face': {'mouth': 'clench', 'brow': -0.7, 'sweat': 1.0}}
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -90, 'stand', 'neutral', keys=[*WAIT(), k(0.0, toon={'reach': {'R': [r(ME[0] - 0.5), 1.3, 0.0, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': DEAD}, toonDur=0.0)]),
        act('flic1', [r(ME[0] - 1.25), 0, 0.15], 90, 'stand', 'determined', keys=[k(0.0, look=[ME[0], 1.9, ME[2]]), k(0.0, toon=TUG(0.2, 1.0), toonDur=0.0),
            *[k(r(0.25 + 0.3 * j), toon=TUG(r(0.32 + 0.06 * (j % 2)), r(1.25 + 0.1 * j)), toonDur=0.12, toonEase='out') for j in range(4)]])],   # heave after heave, his arm a notch longer
        props=[RED(), ZEBRA(), BEARD()],
        cams=[FC(0.0, [3.6, 1.6, 4.4], [[ME[0], 2.45, ME[2]], [r(ME[0] - 1.6), 2.3, 0.15], [r(ME[0] - 1.6), 0.0, 0.15], [ME[0], 0.0, ME[2]]], top=0.16, bottom=0.78)])
st.cue('sfx:stretch', 'S07', 0.25, 0.25); st.cue('sfx:grunt', 'S07', 0.55, 0.2)

# 8: the policeman got a fine. On the crossing, red still lit: his colleague writes him a ticket and hands it over; his jaw drops (AMENDE)
D8 = st.dur('S08'); TIC8 = 0.6
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('flic1', [2.6, 0, 0.0], 60, 'stand', 'neutral', keys=[k(0.0, look=[3.5, 1.9, 0.9]), k(r(TIC8 + 0.1), toon={'reach': {'R': [3.05, 1.3, 0.45, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'jaw': 0.6, 'eye': 0.5, 'brow': 0.8}}, toonDur=0.08, toonEase='out')]),
        act('flic2', [3.5, 0, 0.9], -120, 'stand', 'neutral', keys=[k(0.0, look=[2.6, 1.9, 0.0]), k(0.0, toon={'reach': {'R': [3.2, 1.3, 0.55, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.4}}, toonDur=0.0)]),
        act('mec', ME, -90, 'stand', 'neutral', keys=WAIT())],
        props=[RED(), ZEBRA(), BEARD(), P('pv8', 'envelope', on={'actor': 'flic2', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, opts={'color': '#F2D0D8'}, keys=[k(TIC8, attach='flic1', hand='R', offset=[0.0, 0.0, 0.03], face='camera')])],
        cams=[FC(0.0, [1.4, 1.6, 4.6], [[2.6, 2.45, 0.0], [3.5, 2.45, 0.9], [2.6, 0.0, 0.0], [ME[0], 2.4, ME[2]]], top=0.2, bottom=0.78, lenses=range(26, 66))])
st.cue('sfx:paper', 'S08', TIC8, 0.25); st.cue('sfx:gasp', 'S08', r(TIC8 + 0.1), 0.25)

# 9: the pigeons nested in his beard. Close: a straw nest in the beard, a pigeon sitting in it, eggs popping in one after another; he blinks
D9 = st.dur('S09')
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[*WAIT(), k(1.0, toon={'face': {'lid': 1.0}}, toonDur=0.08), k(1.12, toon={'face': DEAD}, toonDur=0.1)]),
        act('pigeon', [r(ME[0] - 0.24), 1.42, 0.0], -90, 'idle', 'neutral', scale=1.3, keys=[k(0.0, look='camera')])],
        props=[RED(), BEARD(), P('nid9', 'nest', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.42, 0.24]}, scale=0.45, opts={'layAt': [0.3, 0.6, 0.9]})],
        cams=[FC(0.0, [4.4, 1.45, -1.0], [[ME[0], 2.45, ME[2]], [ME[0], 1.0, ME[2]], [r(ME[0] - 0.3), 1.9, 0.0]], top=0.14, bottom=0.74)])   # (audit) from his other side and lower: not S03's frame
for t_ in (0.3, 0.6, 0.9): st.cue('pop', 'S09', t_, 0.15)

# 10: tourists queue for the photo. Along the pavement a queue of tourists; the first one photographs him: a flash; the next one steps up
D10 = st.dur('S10'); FL10 = [0.4, 1.1]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT()),
        *[act(f'tour{j + 1}', [r(ME[0] + 0.3 + 0.75 * j), 0, r(1.4 + 0.55 * j)], -150, 'stand', 'happy', keys=[k(0.0, look=[ME[0], 1.9, ME[2]]),
            *([k(0.0, toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0)] if j == 0 else [])]) for j in range(4)]],
        props=[RED(), ZEBRA(), BEARD(), P('cam10', 'pressCamera', on={'actor': 'tour1', 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': FL10})],
        cams=[FC(0.0, [3.4, 1.7, 3.6], [[ME[0], 2.45, ME[2]], [r(ME[0] + 2.55), 2.45, 3.05], [r(ME[0] + 2.55), 0.0, 3.05], [ME[0], 0.0, ME[2]]], top=0.16, bottom=0.78)])   # (stills 1) nearer the queue
for t_ in FL10: st.cue('sfx:click', 'S10', t_, 0.25)

# 11: the government decorated him for his patience. A minister pins a medal on his chest and steps back to clap; he does not take his eyes off the
#     light (BRAVO)
D11 = st.dur('S11'); PIN11 = 0.5
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT()),
        act('ministre', [r(ME[0] - 0.7), 0, -0.65], 30, 'stand', 'happy', keys=[k(0.0, look=[ME[0], 1.55, ME[2]]), k(0.0, toon={'reach': {'R': [r(ME[0] - 0.2), 1.55, -0.15, 1, 0.03]}, 'hands': {'R': 'pinch'}, 'face': {'mouth': 'smile'}}, toonDur=0.0),
            k(r(PIN11 + 0.15), look='camera'), k(r(PIN11 + 0.15), toon={'touch': {'R': ['torso', -0.05, 0.5, 0.3, 1, 0.03], 'L': ['torso', 0.05, 0.5, 0.3, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.15),
            *[k(r(PIN11 + 0.35 + 0.18 * j), toon={'touch': {'R': ['torso', r(-0.05 + (0.03 if j % 2 else 0.0)), 0.5, 0.3, 1, 0.03], 'L': ['torso', r(0.05 - (0.03 if j % 2 else 0.0)), 0.5, 0.3, 1, 0.03]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'mouth': 'bigsmile'}}, toonDur=0.06) for j in range(5)]])],   # clapping
        props=[RED(), BEARD(), P('med11', 'medal', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.12, 0.62, 0.17]}, scale=1.4, keys=[k(0.0, scale=0.01, dur=0.0), k(PIN11, scale=1.4, dur=0.08, ease='outBack')])],
        cams=[FC(0.0, [3.6, 1.75, 2.4], [[ME[0], 2.45, ME[2]], [r(ME[0] - 0.7), 2.45, -0.65], [ME[0], 1.0, ME[2]]], top=0.2, bottom=0.74)])   # (stills 1) the minister beside him (from behind he hid the medal)
st.cue('sfx:clink', 'S11', PIN11, 0.3); st.cue('sfx:fanfare', 'S11', r(PIN11 + 0.3), 0.18)

# 12: the president came to wait with him. Side by side at the kerb, the president and him, both deadpan, eyes on the light; two bodyguards behind
D12 = st.dur('S12')
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT()),
        act('president', [ME[0], 0, 0.95], -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 2.5, LIGHT[2]]), k(0.0, toon={'touch': {'R': ['torso', 0.0, 0.25, -0.25, 1, 0.03], 'L': ['torso', 0.0, 0.25, -0.27, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': DEAD}, toonDur=0.0),
            k(0.9, toon={'touch': {'R': ['torso', 0.0, 0.25, -0.25, 1, 0.03], 'L': ['torso', 0.0, 0.25, -0.27, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 1.0}}, toonDur=0.08), k(1.02, toon={'touch': {'R': ['torso', 0.0, 0.25, -0.25, 1, 0.03], 'L': ['torso', 0.0, 0.25, -0.27, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': DEAD}, toonDur=0.1)]),   # hands behind his back
        *[act(f'garde{j + 1}', [r(ME[0] + 1.3), 0, r(-0.4 + 1.6 * j)], -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 2.0, LIGHT[2]])]) for j in range(2)]],
        props=[RED(), ZEBRA(), BEARD()],
        cams=[FC(0.0, [2.0, 1.55, 3.2], [[ME[0], 2.45, ME[2]], [ME[0], 2.45, 0.95], [r(ME[0] + 1.3), 2.45, 1.2], [ME[0], 0.6, 0.5]], top=0.16, bottom=0.76)])

# 13: he left after ten minutes. The president looks at his watch, puffs out his cheeks and walks off with his bodyguards; he stays
D13 = st.dur('S13'); LOOK13 = 0.25; GO13 = 0.95
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT()),
        act('president', [ME[0], 0, 0.95], -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 2.5, LIGHT[2]]),
            k(LOOK13, toon={'touch': {'L': ['torso', 0.25, 0.55, 0.35, 1, 0.03]}, 'hands': {'L': 'open'}, 'face': {'gy': 0.6, 'lid': 0.3}}, toonDur=0.15, toonEase='out'),   # his watch up...
            k(r(LOOK13 + 0.35), toon={'touch': {'L': ['torso', 0.25, 0.55, 0.35, 1, 0.03]}, 'hands': {'L': 'open'}, 'face': {'puff': 1.0, 'swell': 0.5, 'mouth': 'kiss', 'lid': 0.3}}, toonDur=0.12),   # ...cheeks puffed out...
            k(GO13, to=[r(ME[0] + 4.0), 0, 2.4], dur=r(D13 - GO13), clip='walk', ease='in', face='keep'), k(GO13, toon={}, toonDur=0.2)]),   # ...and off
        *[act(f'garde{j + 1}', [r(ME[0] + 1.3), 0, r(-0.4 + 1.6 * j)], -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 2.0, LIGHT[2]]), k(r(GO13 + 0.08), to=[r(ME[0] + 4.6), 0, r(1.8 + 1.4 * j)], dur=r(D13 - GO13), clip='walk', ease='in', face='keep')]) for j in range(2)]],
        props=[RED(), ZEBRA(), BEARD(), P('montre13', 'wristWatch', on={'actor': 'president', 'hand': 'L', 'offset': [0.0, 0.04, 0.0]}, opts={'bright': True, 'both': True})],
        cams=[FC(0.0, [1.6, 1.9, 5.4], [[ME[0], 2.45, ME[2]], [ME[0], 2.45, 0.95], [r(ME[0] + 4.6), 2.45, 3.2], [ME[0], 0.0, 0.5]], top=0.16, bottom=0.78)])   # (audit) wider, to see them walk off

# 14: yesterday the light turned green. Close on the light: the red goes out, the green lights up with a pop, the spider drops off on its thread (VERT)
D14 = st.dur('S14'); GREEN14 = 0.35
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[act('araignee', [r(LIGHT[0] + 0.16), 1.87, LIGHT[2]], 90, 'idle', 'neutral', scale=0.5, keys=[k(0.0, look='camera'), k(r(GREEN14 + 0.05), to=[r(LIGHT[0] + 0.16), 0.9, LIGHT[2]], dur=0.35, ease='in')])],
        props=[RED(state=[[0.0, 'r'], [GREEN14, 'g']])],
        cams=[FC(0.0, [-4.1, 2.15, 2.0], [[LIGHT[0], 2.75, LIGHT[2]], [LIGHT[0], 1.75, LIGHT[2]]], top=0.2, bottom=0.72)])
st.cue('sfx:ding', 'S14', GREEN14, 0.4)

# 15: television from all over the world was there. Behind barriers along the pavement, TV cameras on tripods and reporters, flashes going off
D15 = st.dur('S15'); FL15 = [0.3, 0.7, 1.1, 1.4]
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=WAIT()),
        *[act(f'jour{j + 1}', [r(ME[0] + 1.0 + 0.8 * j), 0, r(2.2 + 0.3 * (j % 2))], -150, 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 1.9, ME[2]]),
            k(0.0, toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0)]) for j in range(3)]],
        props=[RED(state=[[0.0, 'g']]), ZEBRA(), BEARD(), *[P(f'tv15{j}', 'tvCamera', pos=[r(ME[0] - 0.4 + 1.2 * j), 0, 3.6], ry=200) for j in range(2)],
               *[P(f'cam15{j}', 'pressCamera', on={'actor': f'jour{j + 1}', 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': FL15[j::3]}) for j in range(3)]],
        cams=[FC(0.0, [1.6, 2.0, 6.4], [[ME[0], 2.45, ME[2]], [r(ME[0] + 2.6), 2.45, 2.5], [r(ME[0] + 0.8), 0.0, 3.6], [ME[0], 0.0, ME[2]]], top=0.16, bottom=0.78)])
for t_ in FL15: st.cue('sfx:click', 'S15', t_, 0.2)

# 16: he crossed. From the road: the first step off the kerb, slow, the beard dragging; dust falls off him; a crack of the knees
D16 = st.dur('S16'); STEP16 = 0.2
st.shot('S16', 'parisStreet', setOpts=STREET, actors=[act('mec', ME, -90, 'stand', 'neutral', keys=[k(0.0, look=[LIGHT[0], 2.5, LIGHT[2]]), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(STEP16, to=[r(ME[0] - 1.3), 0, 0.0], dur=r(D16 - STEP16), clip='walk', ease='inOut', face='keep'), k(STEP16, toon={'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.3}}, toonDur=0.1)])],
        props=[RED(state=[[0.0, 'g']]), ZEBRA(), BEARD(), P('dust16', 'dustPuff', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.3, 0.0]}, opts={'period': 0.9})],
        cams=[FC(0.0, [2.4, 0.9, 1.6], [[ME[0], 2.45, ME[2]], [r(ME[0] - 1.3), 0.0, 0.0], [ME[0], 0.0, ME[2]]], top=0.16, bottom=0.8, drift=(-0.6, 0.0, 0.0))])
st.cue('sfx:crunch', 'S16', r(STEP16 + 0.05), 0.3); st.cue('sfx:step', 'S16', r(STEP16 + 0.4), 0.2)

# 17: the crowd wept. Behind the barriers: the reporters and onlookers in tears, one blowing his nose, confetti coming down
D17 = st.dur('S17')
CRY = lambda: {'face': {'tears': 1.0, 'mouth': 'sob', 'brow': 0.9, 'lid': 0.4}}
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[*[act(f'jour{j + 1}', [r(4.0 + 0.85 * j), 0, r(2.3 + 0.4 * (j % 2))], -160 + 20 * j, 'stand', 'neutral', keys=[k(0.0, look=[1.0, 1.6, 0.0]), k(0.0, toon=CRY(), toonDur=0.0)]) for j in range(3)],
        act('tour1', [3.3, 0, 3.2], -140, 'stand', 'neutral', keys=[k(0.0, look=[1.0, 1.6, 0.0]), k(0.0, toon={**CRY(), 'touch': {'R': ['face', 0.0, 0.18, 0.12, 1, 0.02]}, 'hands': {'R': 'grip'}}, toonDur=0.0)])],
        props=[P('conf17', 'confetti', pos=[4.8, 0, 2.6], opts={'w': 4.0, 'h': 3.5, 'd': 2.0, 'n': 120})],
        cams=[FC(0.0, [2.0, 1.6, 6.6], [[3.3, 2.45, 3.2], [6.0, 2.45, 2.7], [4.0, 0.0, 2.3]], top=0.16, bottom=0.76)])
st.cue('sfx:sniff', 'S17', 0.3, 0.25); st.cue('sfx:sniff', 'S17', 0.9, 0.2)

# 18: on the other side there was a red light. On the far kerb he arrives under another pedestrian light, for the side street: red
D18 = st.dur('S18'); FAR18 = [-5.55, 0, 0.0]
st.shot('S18', 'parisStreet', setOpts=STREET, actors=[act('mec', [-4.4, 0, 0.0], -90, 'walk', 'neutral', keys=[k(0.0, to=FAR18, dur=0.9, clip='walk', then='stand', ease='out', face='keep'), k(0.0, look=[-5.6, 1.8, -2.0]), k(0.95, look=[-6.6, 2.5, -1.6]), k(0.95, toon={'face': DEAD}, toonDur=0.1)])],
        props=[RED(state=[[0.0, 'g']]), RED('feu2', pos=[-6.6, 0, -1.6], ry=0), ZEBRA(), BEARD()],
        cams=[FC(0.0, [-3.0, 1.7, 3.0], [[-5.55, 2.45, 0.0], [-6.6, 2.75, -1.6], [-4.4, 0.0, 0.0]], top=0.16, bottom=0.76, drift=(-0.4, 0.0, 0.0))])
st.cue('sfx:ding', 'S18', 0.95, 0.15)

# 19: he is waiting. Him under the new red light, deadpan, the beard to the ground; a pigeon lands on his head; a look at us
D19 = st.dur('S19')
st.shot('S19', 'parisStreet', setOpts=STREET, actors=[act('mec', FAR18, 0, 'stand', 'neutral', keys=[k(0.0, look=[-6.6, 2.5, -1.6]), k(0.0, toon={'face': DEAD}, toonDur=0.0), k(0.55, look='camera')]),
        act('pigeon', [-4.6, 3.2, 1.2], -120, 'fly', 'neutral', scale=1.3, keys=[k(0.0, to=[FAR18[0], 2.52, FAR18[2]], dur=0.45, ease='out'), k(0.45, clip='idle')])],
        props=[RED('feu2', pos=[-6.6, 0, -1.6], ry=0), BEARD()],
        cams=[FC(0.0, [-4.5, 1.75, 2.6], [[FAR18[0], 2.8, 0.0], [-6.6, 2.75, -1.6], [FAR18[0], 0.7, 0.0]], top=0.16, bottom=0.76)])
st.cue('sfx:cluck', 'S19', 0.45, 0.2)

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
    'president': {'preset': 'politique', 'seed': 677, 'suit': '#1E2230', 'lapel': '#1E2230', 'tie': '#9A1F2E', 'hairColor': '#8A8A8A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'garde1': {'preset': 'infiltre', 'seed': 678, 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'garde2': {'preset': 'infiltre', 'seed': 679, 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'jour1': {'preset': 'journaliste', 'seed': 680, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'jour2': {'preset': 'journaliste', 'seed': 681, 'suit': '#7A5C8E', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'jour3': {'preset': 'madame', 'seed': 682, 'suit': '#C255C8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
})
