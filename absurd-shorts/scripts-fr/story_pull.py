#!/usr/bin/env python3
"""Le pull (story 74, cycle 36; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man went out with his jumper inside out. Nobody dared tell him. The next day his colleague did the same. Then the whole office. Then the whole
town. The shops sewed their labels on the outside. The news presenter wore it live. The president gave his new year wishes in a jumper inside out.
The fashion shows in Paris went inside out. Yesterday he saw himself in a shop window. He turned his jumper right side out. The whole street turned
round. The police arrested him for indecent dress. He was sentenced to wear his jumper inside out. For life.
Staging: a red knitted jumper over his suit, inside out: pale seams outside and a big white label sticking up out of the collar; passers-by stare
at it and look away; a colleague in the same state, then the whole open-plan office, then a street of them; a seamstress sewing a label on the
outside; the news desk, the label up behind the presenter's neck; the president at his lectern, the label sticking out; a catwalk of giant labels
under flashes; his reflection in a shop window taps its own label; he turns it right side out with a squash; the whole street turns to stare;
two policemen in inside-out jumpers handcuff him; the judge, a label out of his robe, brings the gavel down; he pulls it back on inside out; a look at
us.
Natural look; cycle 36: props_pull.js (knitJumper, jumperPile); the reflection helper; props reused."""
from story_kit import *
import math

st = Story('pull', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0),
         ('S08', 'L07', 0), ('S09', 'L07', 4), ('S10', 'L08', 0), ('S11', 'L08', 4), ('S12', 'L09', 0), ('S13', 'L10', 0), ('S14', 'L11', 0),
         ('S15', 'L12', 0), ('S16', 'L13', 0), ('S17', 'L14', 0), ('S18', 'L14', 4), ('S19', 'L15', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
def BL(t_, face, **more):
    """(review 2) A blink that keeps the pose: the previous toon key's reach, touch, hands and bends stay; the face is `face`, closed then open."""
    return [k(t_, toon={'face': {**face, 'lid': 1.0}, **more}, toonDur=0.06, keepPose=True), k(r(t_ + 0.12), toon={'face': face, **more}, toonDur=0.08, keepPose=True)]
# (review 1) the care label is the running gag: one design everywhere (props_pull.js careTag: white, a dark outline, a wash tub, two lines), half a
# head tall, standing above one shoulder (tagSide 1 = the wearer's left) so that it clears the head from the front and from behind; it sways and
# flops (tagKick). The jumpers' sleeves are the wearers' jacket sleeves recoloured in the cast (a box over a navy suit read as a knitted bib).
def JUMP(pid, who, color='#C8322A', inside=True, w=0.66, **o):
    return P(pid, 'knitJumper', on={'actor': who, 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'color': color, 'inside': inside, 'w': w, 'h': 0.62, 'd': 0.42, **o})
MJ = lambda pid, inside=True, **o: JUMP(pid, 'mec', '#C8322A', inside, 0.6, **o)   # his red jumper (his build is narrower)
def LBL(pos, ry, side=1, w=0.6, y=1.75):
    """Where the label of a standing wearer is, in the world (to frame it, to look at it, to tap it)."""
    a = math.radians(ry); lx, lz, fx, fz = math.cos(a), -math.sin(a), math.sin(a), math.cos(a)
    return [r(pos[0] + side * (w / 2 + 0.04) * lx - 0.07 * fx), y, r(pos[2] + side * (w / 2 + 0.04) * lz - 0.07 * fz)]
COLS = ['#2F62B5', '#2F8F6B', '#E8A33C', '#8E5AA8', '#3A9BDC', '#E0813A', '#C255C8', '#5BB5A8']
PARIS = {'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}
PARIS_CLR = {**PARIS, 'clear': [-40.0, 12.0], 'clearL': [-40.0, 12.0], 'clouds': 0}   # (final pass) no tree and no cloud behind his head (a tree crown read as a green hood; a cloud as a slab in the sky)

for g_ in [('S02', 0.6, 'mec', 'label'), ('S05', 0.95, 'mec', 'office'), ('S13', 1.1, 'mec', 'reflection'), ('S14', 0.95, 'mec', 'flip'), ('S16', 1.7, 'mec', 'arrest'), ('S19', 0.5, 'mec', 'end')]:
    st.gag(*g_)
st.card('S07', 'DEHORS', at=0.5)
st.card('S12', "À L'ENVERS", at=0.5)
st.card('S16', 'INDÉCENT', at=0.8)

# 1: the hook. Out of his building door onto the street, a red knitted jumper over his suit, its pale seams outside, deadpan
#    (review 2) no label yet: the first shot of the line must not show what the second reveals
D1 = st.dur('S01'); ME1 = [4.6, 0, 0.6]
st.shot('S01', 'parisStreet', setOpts=PARIS, actors=[act('mec', [6.6, 0, 0.6], -90, 'walk', 'neutral', keys=[k(0.0, to=ME1, dur=r(D1 - 0.2), clip='walk', then='stand', ease='out'), k(0.0, look=[0.0, 1.8, 0.6]), k(r(D1 - 0.3), look='camera')])],
        props=[MJ('pull1', tag=0)],
        cams=[FC(0.0, [2.6, 1.5, 3.2], [[ME1[0], 2.45, ME1[2]], [ME1[0], 0.0, ME1[2]], [6.6, 2.45, 0.6], [6.6, 0.0, 0.6]], top=0.14, bottom=0.78)])
st.cue('sfx:stepSoft', 'S01', 0.3, 0.15); st.cue('sfx:stepSoft', 'S01', 0.7, 0.15)

# 2: ...inside out. Close from behind his shoulder: the pale seams outside; (review 2) the white care label springs up out of the collar, and a
#    burst points at it; (final pass) a yellow shout bubble with its tail on the label, big letters (a star floating in the sky pointed at nothing)
D2 = st.dur('S02'); L2 = LBL(ME1, -90); POP2 = 0.3
TIP2 = [r(L2[0] + 0.01), 1.86, r(L2[2] + 0.06)]; RT2 = (0.66, -0.75)   # the tip of the tail on the label's top; the screen's right, on the ground
st.shot('S02', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -90, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 0.6]), k(r(POP2 + 0.05), toon={'sq': [0.98, 1.03, 0.98]}, toonDur=0.08), k(0.6, toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.2), k(0.95, toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.25)])],
        props=[MJ('pull2', tagPop=POP2, tagKick=[0.66]),
               P('etiq2', 'voiceBubble', pos=TIP2, face='camera', opts={'at': r(POP2 + 0.06), 'w': 0.66, 'side': -1, 'text': "L'ÉTIQUETTE !", 'fill': '#FFE14A', 'edge': '#1C1C1E', 'ink': '#D22B2B', 'jagK': 0.72})],   # (stills 1) up and to the left: to the right it sat on his head
        cams=[FC(0.0, [5.9, 2.0, 1.75], [[ME1[0], 2.45, ME1[2]], [ME1[0], 1.4, ME1[2]], [L2[0], 1.95, r(L2[2] + 0.12)], [L2[0], 1.58, r(L2[2] - 0.1)], TIP2, [r(TIP2[0] - RT2[0] * 0.68), 2.38, r(TIP2[2] - RT2[1] * 0.68)]], top=0.12, bottom=0.74)])   # (review 1) the burst inside the frame, over the label
st.cue('pop', 'S02', POP2, 0.2); st.cue('sfx:sting', 'S02', r(POP2 + 0.06), 0.15)

# 3: nobody dared tell him. (final pass) From behind him, close: he walks away from us down the pavement, the label big over his shoulder; two
#    passers-by walk toward us, toward him; as they come level their necks stretch out to twice their length after the label, eyes popping; a
#    held stare; then both snap their heads away, lips pursed, and a note pops from each mouth (side by side they read as walking with him)
D3 = st.dur('S03'); STARE3 = 0.42; AWAY3 = 1.08
PASS3 = [('pass1', 5.25, 0.2, 1.25), ('pass2', 7.15, 0.4, 1.4)]   # x, z at the start, z at the end: they stroll toward us
ZH3 = lambda t_: r(1.5 - 1.4 * t_ / D3)   # where he is along the pavement (walking away from us)
LB3 = lambda t_: [5.86, 1.85, r(ZH3(t_) + 0.07)]   # his label (over his left shoulder: the -x side, walking -z)
st.shot('S03', 'parisStreet', setOpts={**PARIS_CLR, 'eiffel': False}, actors=[act('mec', [6.2, 0, 1.5], 180, 'walk', 'neutral', keys=[k(0.0, to=[6.2, 0, 0.1], dur=D3, clip='walk', ease='linear'), k(0.0, look=[6.2, 1.7, -4.0]),
            k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0)]),
        *[act(pid, [px, 0, z0], 0, 'walk', 'neutral', keys=[k(0.0, to=[px, 0, z1], dur=D3, clip='walk', ease='linear'), k(0.0, look=[px, 1.7, 4.5]), k(0.0, toon={'face': {'lid': 0.2, 'mouth': 'line'}}, toonDur=0.0),
            k(0.22, look=LB3(0.5), lookDur=0.14),   # their eyes catch the label coming...
            k(r(STARE3 + 0.04 * j), toon={'bend': {'neck': [0.1, 0, 0, 2.2, None]}, 'face': {'lid': 0.0, 'eye': 0.45, 'pop': 0.5, 'popLen': 0.1, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}, 'sq': [0.95, 1.07, 0.95]}, toonDur=0.1, toonEase='out'),   # ...the necks shoot out after it
            k(0.62, look=LB3(0.85), lookDur=0.2), k(0.86, look=LB3(1.05), lookDur=0.15),   # held, following it as they pass
            k(r(AWAY3 + 0.06 * j), look=[r(px + (-2.4 if j == 0 else 2.4)), 3.0, r(z1 + 1.5)], lookDur=0.07),   # and they snap away
            k(r(AWAY3 + 0.06 * j), toon={'bend': {'neck': [0.0, 0, 0, 1.0, None]}, 'face': {'lid': 0.4, 'mouth': 'whistle', 'brow': 0.4}, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.07, toonEase='out'),
            k(r(AWAY3 + 0.06 * j + 0.2), toon={'face': {'lid': 0.4, 'mouth': 'whistle', 'brow': 0.4}}, toonDur=0.15),
            *BL(r(1.44 + 0.08 * j), {'lid': 0.4, 'mouth': 'whistle', 'brow': 0.4})]) for j, (pid, px, z0, z1) in enumerate(PASS3)]],
        props=[MJ('pull3', tagSway=0.14, tagRate=9.0), *[JUMP(f'pj3{j}', pid, COLS[j], inside=False) for j, (pid, px, z0, z1) in enumerate(PASS3)],
               *[P(f'note3{j}', 'whistleNotes', pos=[r(px + (-0.42 if j == 0 else 0.42)), 2.25, r(z0 + (z1 - z0) * 0.68)], face='camera', opts={'n': 2, 'from': r(AWAY3 + 0.06 * j + 0.04), 'every': 0.18, 'size': 0.3, 'dx': -0.6 if j == 0 else 0.6, 'dy': 0.8, 'life': 0.6}) for j, (pid, px, z0, z1) in enumerate(PASS3)]],
        cams=[FC(0.0, [6.45, 1.65, 4.6], [[5.25, 2.95, 1.25], [7.15, 2.95, 1.4], [5.25, 0.7, 1.25], [7.15, 0.7, 1.4], [6.2, 2.45, 0.1], [5.86, 2.15, 1.57]], top=0.12, bottom=0.84, lenses=range(24, 60))])
st.cue('sfx:whistle', 'S03', AWAY3, 0.2)

# 4: the next day his colleague did the same. The office, waist up, both three-quarters to us: the colleague walks in and stops beside him; as he
#    settles, his label springs up over his shoulder; his eyes pop a little; a real nod, down and up, one after the other, the labels bobbing late
D4 = st.dur('S04'); M4 = [-0.4, 0, -0.6]; C4 = [0.45, 0, -0.35]; STOP4 = 0.95
F4 = {**DEAD, 'mouth': 'line'}
def NOD4(t_, face):   # a nod down and up, with a little overshoot back
    return [k(t_, toon={'bend': {'neck': [0.55, 0, 0, 1, None]}, 'face': {**face, 'lid': 0.8}}, toonDur=0.1, toonEase='out', keepPose=True), k(r(t_ + 0.14), toon={'bend': {'neck': [-0.12, 0, 0, 1, None]}, 'face': face}, toonDur=0.1, keepPose=True),
            k(r(t_ + 0.28), toon={'bend': {'neck': [0.0, 0, 0, 1, None]}, 'face': face}, toonDur=0.1, keepPose=True)]
st.shot('S04', 'office', actors=[act('mec', M4, 35, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': F4}, toonDur=0.0),
            k(0.12, look=[1.5, 1.85, 1.0], lookDur=0.15), k(0.15, toon={'face': {**F4, 'gx': 0.7, 'brow': 0.3}, 'sq': [1.02, 0.98, 1.02]}, toonDur=0.12),   # his eyes, then his head, go to the man coming in
            k(0.55, look=[0.9, 1.9, 0.9], lookDur=0.3), *BL(0.6, {**F4, 'gx': 0.7}),
            k(r(STOP4 + 0.1), toon={'face': {'lid': 0.0, 'eye': 0.35, 'gx': 0.7, 'brow': 0.8, 'mouth': 'o'}, 'sq': [0.95, 1.07, 0.95]}, toonDur=0.07, toonEase='out'),   # the label springs up: a small take
            k(r(STOP4 + 0.32), toon={'face': {**F4, 'gx': 0.7}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.14), *NOD4(1.4, {**F4, 'gx': 0.7}), k(1.98, look='camera', lookDur=0.15), k(2.0, toon={'face': F4}, toonDur=0.1), *BL(2.1, F4)]),
        act('coll', [2.3, 0, 0.2], -100, 'walk', 'neutral', keys=[k(0.0, to=C4, dur=STOP4, clip='walk', then='stand', ease='out'), k(STOP4, face=-25, turn=0.2), k(0.0, look=[0.3, 1.85, 1.6]), k(0.0, toon={'face': F4}, toonDur=0.0),
            k(r(STOP4 - 0.02), toon={'face': F4, 'sq': [1.07, 0.91, 1.07]}, toonDur=0.08, toonEase='in'), k(r(STOP4 + 0.1), toon={'face': F4, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.1), k(r(STOP4 + 0.24), toon={'face': {**F4, 'gx': -0.7}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.12),   # he stops: a settle
            k(r(STOP4 + 0.1), look=[-0.25, 1.85, 0.8], lookDur=0.2), *NOD4(1.66, {**F4, 'gx': -0.7}), *BL(2.08, {**F4, 'gx': -0.7})])],
        props=[MJ('pull4', tagKick=[1.52]), JUMP('pj4', 'coll', '#2F62B5', tagPop=r(STOP4 + 0.04), tagKick=[1.78], tagKickAmp=1.2)],
        cams=[FC(0.0, [0.15, 1.5, 2.2], [[M4[0], 2.5, M4[2]], [C4[0], 2.5, C4[2]], [r(M4[0] - 0.42), 1.3, M4[2]], [r(C4[0] + 0.45), 1.3, C4[2]], LBL(C4, -25, 1, 0.66, 2.05), [1.04, 2.2, C4[2]], [0.0, 0.8, -0.45]], top=0.14, bottom=0.84)])   # (review 1) a waist-up two-shot, both labels in frame
st.cue('pop', 'S04', r(STOP4 + 0.04), 0.2)

# 5: then the whole office. From behind the rows, three-quarter back: every worker in a jumper inside out at a desk with a laptop; (review 2) as each
#    head drops to its keyboard its label springs up, one after another down the aisle, a wave of white labels; he stands at the far end, facing them;
#    (final pass) the desks staggered down a diagonal aisle, so that each label pops in its own place, front to back (they piled up in the middle)
D5 = st.dur('S05'); W5 = [(-0.55, 1.75), (0.55, 1.2), (-0.55, 0.65), (0.55, 0.1), (-0.55, -0.45), (0.55, -1.0)]; M5 = [0.2, 0, -1.95]   # one desk every 0.55 m down the room, left and right in turn
POP5 = lambda j: r(0.16 + 0.1 * j)
st.shot('S05', 'office', setOpts={'printer': False}, actors=[act('mec', M5, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': F4}, toonDur=0.0),
            k(0.2, toon={'face': {**F4, 'gx': -0.6}}, toonDur=0.1), k(0.5, toon={'face': {**F4, 'gx': 0.6}}, toonDur=0.15), k(0.82, toon={'face': {**F4, 'brow': 0.4}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.1), *BL(0.98, F4)]),   # his eyes run over the labels
        *[act(f'emp{j + 1}', [x, 0, z], 180, 'sitWrite', 'neutral', keys=[k(0.0, look=[x, 1.3, r(z - 0.9)]), k(r(POP5(j) - 0.04), look=[x, 0.8, r(z - 0.5)], lookDur=0.1),
            k(POP5(j), toon={'sq': [1.04, 0.94, 1.04]}, toonDur=0.07, toonEase='out'), k(r(POP5(j) + 0.14), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.12)]) for j, (x, z) in enumerate(W5)]],
        props=[MJ('pull5'), *[JUMP(f'pj5{j}', f'emp{j + 1}', COLS[j % len(COLS)], tagSide=1 if j % 2 else -1, tagSway=0.1, tagRate=r(7.0 + 0.6 * j), tagPhase=r(1.1 * j), tagPop=POP5(j)) for j in range(len(W5))],   # the labels on the aisle side
               *[P(f'ch5{j}', 'chair', pos=[x, 0, z], opts={'color': '#3A3F48'}) for j, (x, z) in enumerate(W5)], *[P(f'dk5{j}', 'desk', pos=[x, 0, r(z - 0.55)], opts={'w': 0.9, 'd': 0.6}) for j, (x, z) in enumerate(W5)],
               *[P(f'pc5{j}', 'laptop', pos=[x, 0.76, r(z - 0.66)], opts={'text': ' ', 'bg': '#2C6EB5'}) for j, (x, z) in enumerate(W5)]],   # (final pass) a laptop on each desk: the heads drop to a keyboard (bare desks read as a classroom)
        cams=[FC(0.0, [-1.4, 3.3, 6.6], [[-0.86, 1.45, 1.75], [0.86, 1.35, -1.0], [M5[0], 2.55, M5[2]], [0.0, 0.95, 1.75], [0.86, 1.45, 1.2]], top=0.14, bottom=0.8, lenses=range(26, 70))])   # (stills 1) further back on a longer lens: close, the front rows filled the frame   # high over the rows: he stands at the far end above the seated heads
st.cue('pop', 'S05', POP5(0), 0.15); st.cue('pop', 'S05', POP5(2), 0.15); st.cue('pop', 'S05', POP5(4), 0.15)

# 6: then the whole town. A street: everyone walking by in jumpers inside out; (review 2) the labels hop at each step, out of phase; him in the middle
D6 = st.dur('S06'); CROWD6 = [(3.4, -0.4, 180), (5.6, -0.9, 180), (3.0, -2.2, 0), (5.9, -2.6, 180), (4.1, -3.6, 180), (6.3, 0.2, 180)]
st.shot('S06', 'parisStreet', setOpts={**PARIS, 'eiffel': False}, actors=[act('mec', [4.6, 0, -1.8], 0, 'walk', 'neutral', keys=[k(0.0, to=[4.6, 0, -0.2], dur=D6, clip='walk', ease='linear'), k(0.0, look='camera'),
            k(0.0, toon={'face': F4}, toonDur=0.0), *BL(0.7, F4)]),
        *[act(f'ville{j + 1}', [x, 0, z], ry, 'walk', 'neutral', keys=[k(0.0, to=[x, 0, r(z + (1.6 if ry == 0 else -1.6))], dur=D6, clip='walk', ease='linear')]) for j, (x, z, ry) in enumerate(CROWD6)]],
        props=[MJ('pull6', tagSway=0.1, tagRate=11.5, tagHop=0.07), *[JUMP(f'pj6{j}', f'ville{j + 1}', COLS[(j + 2) % len(COLS)], tagSide=1 if j % 2 else -1, tagSway=0.1, tagRate=r(10.5 + 0.6 * j), tagPhase=r(0.9 * j), tagHop=0.08) for j in range(len(CROWD6))]],
        cams=[FC(0.0, [4.4, 3.0, 8.6], [[4.6, 2.45, -1.8], [4.6, 0.0, -0.2], [3.4, 2.4, -0.4], [5.6, 2.4, -0.9]], top=0.16, bottom=0.76, lenses=range(16, 40))])   # long lens: the crowd packs up behind him

# 7: the shops sewed their labels on the outside. A clothes shop: with an oversized needle and a red thread the seamstress sews a label onto the
#    chest of a jumper on its stand, stitch after stitch; a pile of jumpers, labels out, on the table (DEHORS); (final pass) the label hangs loose on
#    the chest and each stitch pulls it a corner flatter; at each pull the red thread runs tight from the label to her hand
D7 = st.dur('S07'); J7 = [0.42, 1.12, -1.45]; CO7 = [-0.32, 0, -1.9]; SEW7 = [0.47, 1.37, -1.28]   # the jumper on its stand beside her, and the label on its chest
ST7 = lambda far, f: {'reach': {'R': [r(0.05 - 0.19 * far), r(1.4 + 0.16 * far), r(-1.2 + 0.15 * far), 1, 0.04], 'L': [0.3, 1.64, -1.5, 1, 0.04]}, 'hands': {'R': 'pinch', 'L': 'grip'}, 'face': f}   # (review 2) the needle's point lands on the label on the chest (it sat at the shoulder)
K7 = [k(0.0, look=SEW7), k(0.0, toon=ST7(1, {'lid': 0.3, 'mouth': 'smile'}), toonDur=0.0)]
for j in range(5):
    K7 += [k(r(0.22 + 0.44 * j), toon={**ST7(0, {'lid': 0.4, 'mouth': 'smile', 'brow': -0.2}), 'sq': [1.02, 0.98, 1.02]}, toonDur=0.1, toonEase='in'), k(r(0.42 + 0.44 * j), toon=ST7(1, {'lid': 0.3, 'mouth': 'smile'}), toonDur=0.16, toonEase='out')]
K7 += [k(1.6, look='camera', lookDur=0.15), k(2.05, look=SEW7)]
st.shot('S07', 'poste', setOpts={'title': ' ', 'guichets': False}, actors=[act('coutu', CO7, 20, 'stand', 'happy', keys=K7)],
        props=[P('pull7', 'knitJumper', pos=J7, scale=0.8, opts={'color': '#2F8F6B', 'inside': False, 'tie': False, 'sewn': 0.0, 'sewnSteps': [0.24, 0.68, 1.12, 1.56], 'sleeves': True}), P('tas7', 'jumperPile', pos=[1.22, 0, -1.75]),
               P('pied7', 'slab', pos=[J7[0], 0.56, r(J7[2] - 0.02)], opts={'w': 0.05, 'h': 1.12, 'd': 0.05, 'color': '#3A3F48'}), P('socle7', 'slab', pos=[J7[0], 0.025, r(J7[2] - 0.02)], opts={'w': 0.42, 'h': 0.05, 'd': 0.32, 'color': '#3A3F48'}),   # (review 2) a stand under the jumper (it hung in the air)
               P('aiguille7', 'sewNeedle', on={'actor': 'coutu', 'hand': 'R', 'offset': [0.0, -0.12, 0.04], 'rot': [3.1416, 0, 0]}, opts={'s': 1.3, 'to': SEW7, 'taut': [[r(0.44 + 0.44 * j), r(0.63 + 0.44 * j)] for j in range(5)]}),   # the point out past her fingers (the hand's +y runs up the arm)
               P('ens7', 'signBoard', pos=[0.5, 2.25, -3.3], opts={'text': 'PRÊT-À-PORTER', 'bg': '#F2C230', 'fg': '#2C4A8A', 'w': 1.1, 'h': 0.26, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [0.5, 1.6, 0.6], [[CO7[0], 2.5, CO7[2]], [J7[0], r(J7[1] - 0.04), J7[2]], [-0.75, 1.5, -1.7], [0.85, 1.4, -1.4]], top=0.24, bottom=0.76)])   # (review 1) tighter: the needle, the thread and the label on the chest
st.cue('sfx:tick', 'S07', 0.32, 0.12); st.cue('sfx:tick', 'S07', 0.76, 0.12); st.cue('sfx:tick', 'S07', 1.2, 0.12); st.cue('sfx:tick', 'S07', 1.64, 0.12)

# 8: the news presenter... The news desk under the studio spots: the presenter reads the news in a jumper with its seams outside, a big JOURNAL
#    backdrop; (review 2) no label in sight from the front: the next shot shows it from behind; (final pass) a slate desk top: under the caption band
#    a white top left white letters unreadable
D8 = st.dur('S08'); PRES = [0.0, 0, 0.3]; NEWS = {'backdrop': 'LE JOURNAL', 'fontScale': 0.6, 'podium': False, 'chairs': False, 'flags': False, 'bg': '#5878A8', 'wall': '#4C6A96'}
st.shot('S08', 'pressRoom', setOpts=NEWS, actors=[act('presentateur', PRES, 0, 'sitTalk', 'neutral', keys=[k(0.0, look='camera'), k(0.42, look=[0.25, 0.8, 0.85], lookDur=0.12), k(0.45, toon={'bend': {'neck': [0.2, 0, 0, 1, None]}}, toonDur=0.1),
            k(0.78, look='camera', lookDur=0.12), k(0.8, toon={'bend': {'neck': [0.0, 0, 0, 1, None]}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.1), *BL(1.05, {'lid': 0.2})])],
        props=[P('desk8', 'desk', pos=[0.0, 0, 0.85], opts={'w': 1.6, 'top': '#3E5573'}), P('ch8', 'chair', pos=PRES), JUMP('pj8', 'presentateur', '#E8A33C', tag=0), P('feuille8', 'paperSheet', pos=[0.25, 0.77, 0.9], rot=[-PI / 2, 0, 0], opts={'w': 0.25, 'h': 0.32, 'lines': ['INFOS']}),
               P('truss8', 'lightTruss', pos=[0.0, 2.8, -1.3], opts={'w': 3.4, 'n': 4, 'len': 2.2, 'tilt': -0.35, 'sweep': 0.06, 'opacity': 0.14})],
        cams=[FC(0.0, [0.3, 1.5, 3.2], [[0.0, 2.2, 0.3], [0.0, 0.8, 0.75], [-0.75, 1.2, 0.75], [0.75, 1.2, 0.75], [0.5, 1.7, 0.2]], top=0.2, bottom=0.8, drift=(0.0, 0.0, -0.3))])

# 9: ...wore it live. From behind, at his shoulder, in the studio (a monitor, a softbox, a second camera, the spots): the white label stands between
#    his head and the EN DIRECT plate of the camera in front; (review 2) the plate lights up red and the label twangs; he sits up
D9 = st.dur('S09'); TV9 = [1.55, 0, 1.2]; DIR9 = [1.43, 1.44, 1.11]; LIT9 = 0.5   # a low studio camera at his left, its plate on top of it: just past the label as seen from behind him
st.shot('S09', 'pressRoom', setOpts=NEWS, actors=[act('presentateur', PRES, 0, 'sitTalk', 'neutral', keys=[k(0.0, look=[TV9[0], 1.5, TV9[2]]), k(r(LIT9 + 0.02), toon={'sq': [0.96, 1.07, 0.96]}, toonDur=0.07, toonEase='out'), k(r(LIT9 + 0.25), toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.15),
            k(r(LIT9 + 0.5), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.2)])],
        props=[P('desk9', 'desk', pos=[0.0, 0, 0.85], opts={'w': 1.6, 'top': '#3E5573'}), P('tab9', 'slab', pos=[PRES[0], 0.225, PRES[2]], opts={'w': 0.42, 'h': 0.45, 'd': 0.4, 'color': '#3A3F48'}),   # a stool: the chair's back hid the jumper
               JUMP('pj9', 'presentateur', '#E8A33C', tagKick=[r(LIT9 + 0.03)], tagKickAmp=1.7, tagSway=0.05), P('tv9', 'tvCamera', pos=TV9, ry=-125, opts={'h': 1.0}),
               P('direct9', 'signBoard', pos=DIR9, ry=-150, opts={'text': 'EN DIRECT', 'bg': '#5A2020', 'fg': '#8C5F5F', 'w': 0.5, 'h': 0.17, 'posts': False, 'height': 0}),
               P('direct9on', 'signBoard', pos=[r(DIR9[0] - 0.012), DIR9[1], r(DIR9[2] - 0.02)], ry=-150, opts={'text': 'EN DIRECT', 'bg': '#E62B2B', 'fg': '#FFFFFF', 'w': 0.5, 'h': 0.17, 'posts': False, 'height': 0}, keys=[k(0.0, visible=False), k(LIT9, visible=True, scale=1.25), k(r(LIT9 + 0.1), scale=1.0)]),
               P('proj9', 'studioLight', pos=[-1.35, 0, 1.9], ry=140, opts={'h': 2.1}), P('tv9b', 'tvCamera', pos=[-0.6, 0, 2.5], ry=165, opts={'h': 1.15}), P('moni9', 'studioMonitor', pos=[0.78, 0, 2.3], ry=-158, opts={'jumper': '#E8A33C', 'h': 1.2}),
               P('truss9', 'lightTruss', pos=[0.1, 2.75, 1.7], opts={'w': 3.2, 'n': 4, 'len': 2.0, 'tilt': 0.4, 'sweep': 0.06, 'opacity': 0.14})],
        cams=[FC(0.0, [-0.45, 1.8, -2.5], [[0.0, 1.95, 0.3], [-0.38, 1.5, 0.3], [0.6, 1.3, 0.2], [r(DIR9[0] + 0.32), 1.6, DIR9[2]], [0.0, 0.8, 0.85]], top=0.24, bottom=0.74, inside=(-5.0, 5.0, 0.5, 3.0, -2.8, 6.0))])   # (review 1) the label between the head and the red light, above the caption band
st.cue('sfx:click', 'S09', LIT9, 0.25)

# 10: the president gave his wishes... At the lectern between two flags, under warm spots, the president, solemn: (review 2) a slow push-in, he
#     straightens his collar, lifts his chin; no label in sight yet
D10 = st.dur('S10'); PR10 = [0.0, 0, -0.3]; ELY = {'backdrop': 'PRÉSIDENCE', 'fontScale': 0.6, 'podium': False, 'flags': False, 'chairs': False, 'bg': '#5878A8', 'wall': '#4C6A96', 'fg': 'rgba(255,255,255,0.45)'}   # no rows of chairs: the low camera of S10 backs up through them; paler lettering: his white hair merged with it
FLAGS10 = lambda: [P(f'fl10{j}', 'flag', pos=[x, 0, -0.6], scale=1.5, opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A'], 'vertical': True, 'poleColor': '#D8C27A'}) for j, x in enumerate([-1.3, 0.38])]   # a tricolour either side of him, above his shoulders
TRUSS10 = lambda: P('truss10', 'lightTruss', pos=[0.0, 3.05, -1.25], opts={'w': 3.0, 'n': 2, 'len': 2.4, 'tilt': -0.25, 'fan': 0.1, 'sweep': 0.08, 'color': '#FFE2A8', 'opacity': 0.17})   # behind him, a spot over each flag: in front, its cones veiled the close shot; a lamp in the middle sat on his head like a hat
st.shot('S10', 'pressRoom', setOpts=ELY, actors=[act('president', PR10, 0, 'podiumTalk', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.2}}, toonDur=0.0),
            k(0.15, toon={'touch': {'R': ['torso', 0.02, 0.52, 0.27, 1, 0.02]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.2}, 'sq': [1.02, 0.98, 1.02]}, toonDur=0.16, toonEase='out'),   # he straightens his collar...
            *BL(0.4, {'lid': 0.2}), k(0.62, toon={'face': {'lid': 0.2}, 'bend': {'neck': [-0.14, 0, 0, 1.04, None]}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.2)])],   # ...and lifts his chin
        props=[P('pod10', 'podium', pos=[0.0, 0, 0.2], opts={'text': 'RÉPUBLIQUE'}), JUMP('pj10', 'president', '#2F62B5', tag=0), *FLAGS10(), TRUSS10()],
        cams=[FC(0.0, [0.95, 0.7, 2.9], [[0.0, 2.6, PR10[2]], [0.0, 0.55, 0.46], [-1.3, 2.3, -0.6], [1.3, 2.3, -0.6]], top=0.14, bottom=0.74, drift=(-0.12, 0.0, -0.42))])   # (review 1) the RÉPUBLIQUE plate above the captions, both flags in

# 11: ...in a jumper inside out. Close on him, the seams on his shoulders: (review 2) the big label rises slowly beside his solemn face, like a flag
#     hoisted; he does not flinch; then he bows his head and it swings
D11 = st.dur('S11'); L11 = LBL(PR10, 0, 1, 0.66, 1.95)
st.shot('S11', 'pressRoom', setOpts=ELY, actors=[act('president', PR10, 0, 'podiumTalk', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.2}, 'bend': {'neck': [-0.14, 0, 0, 1.04, None]}}, toonDur=0.0), *BL(0.5, {'lid': 0.2}),
            k(1.05, toon={'bend': {'neck': [0.32, 0, 0, 1, None]}, 'face': {'lid': 0.5}}, toonDur=0.12, toonEase='out'), k(1.3, toon={'face': {'lid': 0.2}, 'bend': {'neck': [0.0, 0, 0, 1, None]}}, toonDur=0.15), *BL(1.5, {'lid': 0.2})])],
        props=[P('pod11', 'podium', pos=[0.0, 0, 0.2], opts={'text': 'RÉPUBLIQUE'}), JUMP('pj11', 'president', '#2F62B5', tag=1.25, tagRise={'at': 0.1, 'dur': 0.8}, tagSway=0.05, tagKick=[1.12]), *FLAGS10(), TRUSS10()],
        cams=[FC(0.0, [0.7, 2.1, 1.3], [[0.16, 2.6, PR10[2]], [0.16, 1.55, PR10[2]], [0.82, 2.4, L11[2]], [1.02, 2.2, L11[2]], [0.82, 1.6, L11[2]], [-0.2, 2.0, PR10[2]]], top=0.16, bottom=0.74)])

# 12: the fashion shows went inside out. A catwalk under the spots, from the end of it, low: a model strides at us in a jumper inside out, its
#     head-tall label flopping at each step, another behind her, two more posing by the backdrop; flashes on both sides (À L'ENVERS)
D12 = st.dur('S12'); M12 = [('mod1', 0.0, -1.1), ('mod2', 0.0, -3.0)]; POSE12 = [('mod3', -1.4, -2.4, 20, '#3FA36C'), ('mod4', 1.4, -2.4, -20, '#E0813A')]
st.shot('S12', 'pressRoom', setOpts={'backdrop': 'PARIS', 'fontScale': 0.9, 'podium': False, 'chairs': False, 'bg': '#2B2E3A', 'wall': '#23252E'}, actors=[
        *[act(mid, [mx, 0, mz], 0, 'strut', 'smug', keys=[k(0.0, to=[mx, 0, r(mz + 1.5)], dur=D12, clip='strut', ease='linear'), k(0.0, look='camera')]) for mid, mx, mz in M12],
        *[act(mid, [mx, 0, mz], mry, 'stand', 'smug', keys=[k(0.0, look='camera'), k(r(0.5 + 0.6 * j), toon={'sq': [0.97, 1.04, 0.97], 'lay': [0.0, 0.06 * (1 if j else -1)]}, toonDur=0.2), k(r(1.3 + 0.4 * j), toon={'sq': [1.0, 1.0, 1.0], 'lay': [0.0, -0.05 * (1 if j else -1)]}, toonDur=0.3)]) for j, (mid, mx, mz, mry, mc) in enumerate(POSE12)],
        *[act(f'photo{j + 1}', [r(-0.85 if j % 2 else 0.85), 0, r(-2.0 + 0.9 * (j // 2))], 90 if j % 2 else -90, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 0.0]), k(0.0, toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            *[k(r(fa), toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 0.97, 1.0]}, toonDur=0.06) for fa in [0.2 + 0.3 * j, 0.9 + 0.25 * j]],
            *[k(r(fa + 0.12), toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.15) for fa in [0.2 + 0.3 * j, 0.9 + 0.25 * j]],
            k(r(1.5 + 0.1 * j), look=[0.0, 1.8, 0.6], lookDur=0.3)]) for j in range(4)]],
        props=[P('podium12', 'floorSlab', pos=[0.0, 0.04, -1.0], opts={'w': 0.9, 'd': 6.0, 'h': 0.08, 'color': '#F4F1E8'}),
               JUMP('pj12a', 'mod1', '#C255C8', tag=2.0, tagSway=0.32, tagRate=9.4), JUMP('pj12b', 'mod2', '#F2C94E', tag=2.0, tagSide=-1, tagSway=0.32, tagRate=9.4, tagPhase=1.6),
               *[JUMP(f'pj12{mid}', mid, mc, tag=1.6, tagSide=-1 if j else 1, tagSway=0.12, tagRate=5.0, tagPhase=r(1.3 * j)) for j, (mid, mx, mz, mry, mc) in enumerate(POSE12)],
               P('truss12', 'lightTruss', pos=[0.0, 3.0, -2.75], opts={'w': 3.8, 'n': 5, 'len': 2.8, 'tilt': -0.12, 'fan': 0.5, 'sweep': 0.2, 'spread': 0.13, 'opacity': 0.13}),   # (review 2) spots and their beams in the black above the catwalk
               P('truss12b', 'lightTruss', pos=[0.0, 3.05, -1.5], opts={'w': 3.6, 'n': 4, 'len': 2.2, 'tilt': 0.12, 'fan': 0.3, 'sweep': 0.2, 'spread': 0.12, 'opacity': 0.11}),   # a nearer one, higher in the frame, its cones falling behind the first model
               P('band12', 'signBoard', pos=[0.0, 3.0, -2.93], opts={'text': 'COLLECTION HIVER', 'bg': '#F4F1E8', 'fg': '#23252E', 'frame': '#C9A227', 'w': 2.3, 'h': 0.3, 'posts': False, 'height': 0}),
               *[P(f'cam12{j}', 'pressCamera', on={'actor': f'photo{j + 1}', 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': [r(0.2 + 0.3 * j), r(0.9 + 0.25 * j)], 'burst': 0.5}) for j in range(4)]],
        cams=[FC(0.0, [0.12, 0.9, 3.4], [[0.0, 2.5, 0.4], [0.0, 0.75, 0.4], [-0.6, 1.5, 0.4], [0.9, 2.0, 0.4]], top=0.2, bottom=0.8)])   # (review 1) low at the end of the catwalk: she fills the frame as she comes
st.cue('sfx:click', 'S12', 0.2, 0.15); st.cue('sfx:click', 'S12', 0.5, 0.15); st.cue('sfx:click', 'S12', 0.8, 0.15); st.cue('sfx:click', 'S12', 1.1, 0.15)

# 13: yesterday he saw himself in a shop window. On the pavement at a big shop window, a dark shop behind the glass: (review 2) his reflection
#     takes its own label in one hand, holds it out and shakes it, and with the other arm, long and straight, points at him; a held beat; his take; he
#     looks at his own shoulder
D13 = st.dur('S13'); ZW = -1.0; ME13 = [0.4, 0, -0.1]; L13 = LBL(ME13, 180); R13 = [L13[0], L13[1], r(2 * ZW - L13[2])]; TAKE13 = 1.1; RZ13 = r(2 * ZW - ME13[2])
SRC13 = act('mec', ME13, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.4, 2.0, -2.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
        k(TAKE13, toon={'sq': [0.92, 1.1, 0.92], 'face': {'lid': 0.0, 'pop': 0.6, 'popLen': 0.12, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.06, toonEase='out'),   # the take
        k(r(TAKE13 + 0.4), look=[L13[0], 1.85, L13[2]], lookDur=0.1), k(r(TAKE13 + 0.45), toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.1),   # he looks at his own shoulder
        k(r(D13 - 0.35), look=[0.4, 2.0, -2.0]), k(r(D13 - 0.3), toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.12)])
REF13 = reflection(SRC13, zm=ZW, shift=0.0, id='mec_reflet')
SMUG13 = {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.5}
SHOW13 = lambda dx, dy, jab, f=SMUG13, sq=None: {'reach': {'R': [r(R13[0] - 0.2 + dx), r(2.05 + dy), r(R13[2] + 0.05), 1, 0.03], 'L': [0.55, 1.66, r(ZW - 0.1 + jab * 0.6), 1, 0.03]}, 'hands': {'R': 'pinch', 'L': 'point'}, 'face': f, **({'sq': sq} if sq else {})}   # (final pass) the pointing arm stretched out to the glass
REF13['keys'] = REF13['keys'] + [k(0.16, toon={'sq': [1.05, 0.93, 1.05], 'face': SMUG13}, toonDur=0.08),   # an anticipation...
                                 k(0.26, toon=SHOW13(0.0, 0.0, 0.0, sq=[0.96, 1.06, 0.96]), toonDur=0.1, toonEase='out'),   # ...one hand takes the label and holds it out, the other arm points at him
                                 k(0.42, toon=SHOW13(-0.06, 0.03, 0.0), toonDur=0.06), k(0.5, toon=SHOW13(0.05, -0.02, 0.0), toonDur=0.06), k(0.6, toon=SHOW13(-0.06, 0.03, 0.0), toonDur=0.06), k(0.68, toon=SHOW13(0.0, 0.0, 0.0), toonDur=0.07),   # it shakes the label
                                 k(0.8, toon=SHOW13(0.0, 0.0, 0.1), toonDur=0.05, toonEase='out'), k(0.9, toon=SHOW13(0.0, 0.0, 0.0), toonDur=0.07), k(0.98, toon=SHOW13(0.0, 0.0, 0.1, {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.7}), toonDur=0.05, toonEase='out')]   # two jabs of the finger at him
st.shot('S13', 'parisStreet', setOpts=PARIS, actors=[SRC13, REF13],
        props=[MJ('pull13', tagKick=[r(TAKE13 + 0.06)]), JUMP('pullref13', 'mec_reflet', '#C8322A', True, 0.6, tag=1.35, tagSide=-1, tagKick=[0.3, 0.44, 0.62, r(TAKE13 + 0.06)], tagKickAmp=1.3),
               P('vitre13', 'slab', pos=[0.4, 1.5, ZW], opts={'w': 2.6, 'h': 2.8, 'd': 0.02, 'color': '#BFE0F0', 'opacity': 0.1}), P('cadre13', 'slab', pos=[0.4, 3.0, ZW], opts={'w': 2.8, 'h': 0.25, 'd': 0.1, 'color': '#2E4563'}),
               P('glare13a', 'slab', pos=[-0.5, 1.6, r(ZW + 0.012)], rot=[0, 0, 0.55], opts={'w': 0.1, 'h': 2.3, 'd': 0.004, 'color': '#FFFFFF', 'opacity': 0.22, 'noShadow': True}),   # (final pass) two glints across the glass and a shop sign: the window
               P('glare13b', 'slab', pos=[-0.28, 1.6, r(ZW + 0.012)], rot=[0, 0, 0.55], opts={'w': 0.04, 'h': 2.3, 'd': 0.004, 'color': '#FFFFFF', 'opacity': 0.2, 'noShadow': True}),   # read as a navy board
               P('ens13', 'signBoard', pos=[0.4, 3.0, r(ZW + 0.065)], opts={'text': 'BOUTIQUE', 'bg': '#2E4563', 'fg': '#F2D27A', 'w': 1.3, 'h': 0.22, 'posts': False, 'height': 0}),
               P('fond13', 'slab', pos=[1.5, 1.6, r(RZ13 - 0.9)], opts={'w': 5.4, 'h': 3.4, 'd': 0.06, 'color': '#28303F', 'noShadow': True}), P('sol13', 'slab', pos=[1.5, 0.01, r(ZW - 0.9)], opts={'w': 5.4, 'h': 0.02, 'd': 1.8, 'color': '#3B4456', 'noShadow': True})],   # (review 2) a plain dark shop behind the reflection (a green tree sat behind its head)
        cams=[FC(0.0, [-1.75, 1.9, 1.75], [[0.4, 2.5, -0.1], [L13[0], 1.95, L13[2]], [0.78, 1.45, -0.1], [0.4, 1.15, -0.1], [0.4, 2.5, RZ13], [r(R13[0] - 0.45), 2.3, R13[2]], [0.4, 1.15, RZ13]], top=0.14, bottom=0.78)])   # (review 1) from his label's side: both figures and both labels inside the frame; (review 2) from further off: the reflection nearer the middle
st.cue('sfx:tick', 'S13', 0.44, 0.2); st.cue('sfx:tick', 'S13', 0.62, 0.2); st.cue('sfx:sting', 'S13', TAKE13, 0.15)

# 14: he turned his jumper right side out. A crouch, then he hauls it up over his head: it stretches over him, head and arms lost inside, bulges
#     twice as he fights it, changes side, snaps down with a squash and wobbles; he smooths it down, pleased (review 1: a texture swap); (review 2) the
#     camera glides in on him once it is on, his hands go on smoothing, a pleased sigh; (final pass) a longer turn: two clear lumps, one each side, with a
#     still beat between them, and his navy suit and white shirt showing under the rising jumper
D14 = st.dur('S14'); T14 = 0.3; TD14 = 1.0; POP14 = r(T14 + 0.8 * TD14); FW = (-0.866, 0.5); LW = (0.5, 0.866)   # his facing (ry -60) and his left, on the ground
HEM = lambda s_, y=1.08: [r(ME1[0] + FW[0] * 0.27 + LW[0] * 0.2 * s_), y, r(ME1[2] + FW[1] * 0.27 + LW[1] * 0.2 * s_), 1, 0.04]
UP14 = lambda s_, y=2.74: [r(ME1[0] + FW[0] * 0.05 + LW[0] * 0.15 * s_), y, r(ME1[2] + FW[1] * 0.05 + LW[1] * 0.15 * s_), 1, 0.04]
GR = {'L': 'grip', 'R': 'grip'}
SMOOTH = lambda y, dx=0.13: {'touch': {'R': ['torso', -dx, y, 0.27, 1, 0.02], 'L': ['torso', dx, y, 0.27, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}}   # the hands on the knit, not through it
st.shot('S14', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.08, toon={'reach': {'L': HEM(1), 'R': HEM(-1)}, 'hands': GR, 'sq': [1.1, 0.86, 1.1], 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.4}}, toonDur=0.16, toonEase='out'),   # a crouch, both hands on the hem...
            k(T14, toon={'reach': {'L': UP14(1), 'R': UP14(-1)}, 'hands': GR, 'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.3, 'mouth': 'clench'}}, toonDur=0.2, toonEase='out'),   # ...and up over his head
            k(r(T14 + 0.32), toon={'reach': {'L': UP14(1, 2.84), 'R': UP14(-1, 2.62)}, 'hands': GR, 'lay': [0.0, 0.17], 'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.3, 'mouth': 'clench'}}, toonDur=0.06, toonEase='out'),   # the fight inside: a lump...
            k(r(T14 + 0.44), toon={'reach': {'L': UP14(1, 2.74), 'R': UP14(-1, 2.74)}, 'hands': GR, 'lay': [0.0, 0.0], 'sq': [0.97, 1.05, 0.97], 'face': {'lid': 0.3, 'mouth': 'clench'}}, toonDur=0.06),   # ...a still beat...
            k(r(T14 + 0.53), toon={'reach': {'L': UP14(1, 2.62), 'R': UP14(-1, 2.84)}, 'hands': GR, 'lay': [0.0, -0.17], 'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.3, 'mouth': 'clench'}}, toonDur=0.06, toonEase='out'),   # ...a lump the other side
            k(r(T14 + 0.68 * TD14), toon={'reach': {'L': HEM(1), 'R': HEM(-1)}, 'hands': GR, 'sq': [1.2, 0.72, 1.2], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.09, toonEase='in'),   # the snap down
            k(r(POP14 + 0.08), toon={**SMOOTH(0.4), 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.1), k(r(POP14 + 0.24), toon={**SMOOTH(0.16), 'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.14),   # he smooths it down
            k(r(POP14 + 0.36), toon={**SMOOTH(0.3, 0.17), 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 1.0, 'mouth': 'smile'}}, toonDur=0.1),   # pleased, eyes closed: a breath in, the hands still smoothing...
            k(r(POP14 + 0.46), toon={**SMOOTH(0.1, 0.1), 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 1.0, 'mouth': 'smile'}}, toonDur=r(D14 - POP14 - 0.46))])],   # ...and a sigh to the cut
        props=[MJ('pull14', True, turn={'at': T14, 'dur': TD14, 'bulges': True}, under='#1F3550')],
        cams=[FC(0.0, [2.6, 1.7, 2.6], [[ME1[0], 3.4, ME1[2]], [ME1[0], 0.75, ME1[2]], [r(ME1[0] - 0.45), 2.2, ME1[2]], [r(ME1[0] + 0.45), 2.2, ME1[2]]], top=0.12, bottom=0.78),
              glide([FC(r(POP14 + 0.1), [2.9, 1.7, 2.3], [[ME1[0], 2.55, ME1[2]], [ME1[0], 0.6, ME1[2]], [r(ME1[0] - 0.45), 1.6, ME1[2]], [r(ME1[0] + 0.45), 1.6, ME1[2]]], top=0.2, bottom=0.92)], 0.4)])
st.cue('sfx:zip', 'S14', T14, 0.2); st.cue('pop', 'S14', POP14, 0.25)

# 15: the whole street turned round. Behind him the street has its back to us; head after head whips round, then the bodies, to stare at him; a woman's
#     shopping bag hangs in the air a beat, then drops; gasps; (review 2) his face stays to us: his eyes slide to them, his head a quarter turn only
D15 = st.dur('S15')
ST15 = [(r(ME1[0] - FW[0] * t + LW[0] * l, 2), r(ME1[2] - FW[1] * t + LW[1] * l, 2)) for t, l in [(1.25, -0.85), (1.3, 1.0), (2.6, -0.3), (2.7, 0.7), (4.0, 0.385)]]
BAG15 = [r(ST15[0][0] + LW[0] * 0.4), r(ST15[0][1] + LW[1] * 0.4)]; DROP15 = 0.62   # beside her, on our side of her: her right hand with her back to us, her left once she has turned
SIDE15 = [r(ME1[0] + LW[0] * 1.6 + FW[0] * 1.0), 1.8, r(ME1[2] + LW[1] * 1.6 + FW[1] * 1.0)]
st.shot('S15', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.0),
            k(0.5, toon={'face': {'lid': 0.0, 'eye': 0.3, 'gx': 0.9, 'mouth': 'line', 'brow': 0.6}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.08, toonEase='out'), k(0.58, look=SIDE15, lookDur=0.12),   # his eyes first, then a quarter turn of the head
            k(0.8, toon={'face': {'lid': 0.0, 'eye': 0.3, 'gx': -0.9, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.1), k(1.1, look='camera', lookDur=0.12), k(1.12, toon={'face': {'lid': 0.1, 'eye': 0.2, 'mouth': 'wavy', 'brow': 0.7}}, toonDur=0.1)]),
        *[act(f'rue{j + 1}', [x, 0, z], 120, 'stand', 'neutral', keys=[k(0.0, look=[r(x + 2.6), 1.8, r(z - 1.5)]), *([k(0.0, toon={'reach': {'R': [BAG15[0], 1.22, BAG15[1], 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0)] if j == 0 else []),
            k(r(0.12 + 0.1 * j), look=[ME1[0], 1.9, ME1[2]], lookDur=0.07),   # the head whips round first...
            k(r(0.2 + 0.1 * j), face=r(math.degrees(math.atan2(ME1[0] - x, ME1[2] - z))), turn=0.14),   # ...then the body
            k(r(0.2 + 0.1 * j), toon={**({'reach': {'L': [BAG15[0], 1.3, BAG15[1], 1, 0.04]}, 'hands': {'L': 'spread'}} if j == 0 else {}), 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}, 'sq': [0.94, 1.07, 0.94]}, toonDur=0.08, toonEase='out')]) for j, (x, z) in enumerate(ST15)]],
        props=[MJ('pull15', False), *[JUMP(f'pj15{j}', f'rue{j + 1}', COLS[(j + 4) % len(COLS)], tag=1.3, tagSide=1 if j % 2 else -1, tagKick=[r(0.22 + 0.1 * j)], tagKickAmp=1.2) for j in range(len(ST15))],
               P('sac15', 'shoppingBag', pos=[BAG15[0], 0.72, BAG15[1]], scale=0.9, keys=[k(0.3, to=[BAG15[0], 0.84, BAG15[1]], dur=0.16, ease='out'), k(DROP15, to=[BAG15[0], 0.0, BAG15[1]], dur=0.2, ease='in'), k(r(DROP15 + 0.2), squash=[1.2, 0.7, 1.2], dur=0.25)])],   # it hangs a beat, then drops
        cams=[FC(0.0, [r(ME1[0] + FW[0] * 2.3 - LW[0] * 0.5), 3.3, r(ME1[2] + FW[1] * 2.3 - LW[1] * 0.5)], [[ME1[0], 2.5, ME1[2]], [ME1[0], 0.3, ME1[2]], *[[x, 2.65, z] for x, z in ST15],
                          [r(ST15[0][0] - LW[0] * 0.25), 1.6, r(ST15[0][1] - LW[1] * 0.25)], [r(ST15[1][0] + LW[0] * 0.25), 1.6, r(ST15[1][1] + LW[1] * 0.25)], [BAG15[0], 0.1, BAG15[1]]], top=0.14, bottom=0.86)])   # (review 1) closer, from above his eye line: the street stacks up behind him
st.cue('sfx:gasp', 'S15', 0.3, 0.3); st.cue('thud', 'S15', r(DROP15 + 0.2), 0.2)

# 16: the police arrested him for indecent dress. Close on the three, two policemen in jumpers inside out, both three-quarters to us: one snaps the
#     cuffs on the wrists he holds out low, on the plain red; then pulls out a censor bar and holds it over the right-side-out jumper; the other, a hand
#     over his eyes, spreads his fingers, peeks with one eye, and snaps them shut; he looks down at the cuffs, at the bar, then at us (INDÉCENT)
D16 = st.dur('S16'); CUFF16 = 0.55; BAR16 = 1.25; PEEK16 = 1.0; WY16 = 1.12
F1 = [r(ME1[0] - LW[0] * 0.62 + FW[0] * 0.2), 0, r(ME1[2] - LW[1] * 0.62 + FW[1] * 0.2)]; F2 = [r(ME1[0] + LW[0] * 0.64 + FW[0] * 0.3), 0, r(ME1[2] + LW[1] * 0.64 + FW[1] * 0.3)]   # (review 2) shoulder to shoulder: three abreast in a tall frame
WR = lambda s_, y=WY16: [r(ME1[0] + FW[0] * 0.42 + LW[0] * 0.075 * s_), y, r(ME1[2] + FW[1] * 0.42 + LW[1] * 0.075 * s_), 1, 0.04]
OFFER = lambda f, **more: {'reach': {'L': WR(1), 'R': WR(-1)}, 'hands': {'L': 'fist', 'R': 'fist'}, 'face': f, **more}
CB16 = [r(ME1[0] + FW[0] * 0.36), 1.47, r(ME1[2] + FW[1] * 0.36)]   # the censor bar: flat in front of his chest, above the cuffed wrists
EYES = lambda hand: {'touch': {'R': ['face', 0.0, 0.3, 0.22, 1, 0.02]}, 'hands': {'R': hand}}   # (stills 2) over his eyes: 0.12 put the palm on his chin
EYES2 = lambda peek=False: {'touch': {'R': ['face', -0.12, 0.28 if peek else 0.43, 0.2, 1, 0.02], 'L': ['face', 0.12, 0.43, 0.2, 1, 0.02]}, 'hands': {'R': 'spread' if peek else 'open', 'L': 'open'}}   # (stills 1 of the final pass) at 0.3 both hands met over his mouth: the eyes are higher   # (final pass) both palms over both eyes; the peek: one hand slides down, fingers spread (one small hand sat on his nose between his eyes)
CR16 = lambda out=0.0: [r(WR(-1)[0] - LW[0] * (0.2 + out)), r(WY16 - 0.06 + out), r(WR(-1)[2] - LW[1] * (0.2 + out)), 1, 0.04]
CLAMP = lambda f, out=0.0, sq=None: {'reach': {'L': [r(WR(-1)[0] - LW[0] * (0.1 + out) + FW[0] * 0.04), r(WY16 + 0.04 + out), r(WR(-1)[2] - LW[1] * (0.1 + out) + FW[1] * 0.04), 1, 0.04], 'R': CR16(out)},
                                     'hands': {'L': 'grip', 'R': 'grip'}, 'face': f, **({'sq': sq} if sq else {})}
HOLD16 = lambda f, sq=None: {'reach': {'L': [r(CB16[0] - LW[0] * 0.36), 1.47, r(CB16[2] - LW[1] * 0.36), 1, 0.04], 'R': CR16()}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': f, **({'sq': sq} if sq else {})}   # one hand on the bar's edge, the other still on his wrist
FL1 = {'lid': 0.3, 'brow': -0.5, 'mouth': 'line'}
st.shot('S16', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.25, toon=OFFER({**DEAD, 'mouth': 'line'}), toonDur=0.2, toonEase='out'), k(CUFF16, toon=OFFER({'lid': 0.3, 'mouth': 'line'}, sq=[1.03, 0.96, 1.03]), toonDur=0.06),   # he holds his wrists out; the cuffs snap on
            k(0.82, look=WR(0)[:3], lookDur=0.2), k(0.85, toon=OFFER({'lid': 0.55, 'mouth': 'line', 'brow': 0.2}), toonDur=0.15),   # a slow look down at the cuffs...
            k(r(BAR16 + 0.1), toon=OFFER({'lid': 0.3, 'mouth': 'line', 'brow': 0.6}, sq=[0.97, 1.04, 0.97]), toonDur=0.08), k(r(BAR16 + 0.1), look=CB16, lookDur=0.1),   # ...at the bar...
            k(1.68, look='camera', lookDur=0.2), k(1.7, toon=OFFER({**DEAD, 'mouth': 'line'}), toonDur=0.15),   # ...then at us
            k(2.02, toon=OFFER({'lid': 1.0, 'mouth': 'line'}), toonDur=0.14), k(2.3, toon=OFFER({**DEAD, 'mouth': 'line'}), toonDur=0.14)]),
        act('flic1', F1, -35, 'stand', 'determined', keys=[k(0.0, look='camera'), k(0.0, toon=CLAMP({**FL1, 'gx': 0.6, 'gy': 0.7}, 0.2), toonDur=0.0),   # (stills 2) his eyes go down to the wrists, his head stays up: turned to them it leaned onto the hero's
            k(r(CUFF16 - 0.2), toon=CLAMP({**FL1, 'gx': 0.6, 'gy': 0.7}, 0.28), toonDur=0.1, toonEase='out'), k(r(CUFF16 - 0.05), toon=CLAMP({'lid': 0.4, 'brow': -0.7, 'mouth': 'clench', 'gx': 0.6, 'gy': 0.7}, 0.0, [1.04, 0.96, 1.04]), toonDur=0.05, toonEase='in'),   # a wind-up, snap
            k(0.85, toon=CLAMP({'lid': 0.4, 'brow': -0.5, 'mouth': 'line'}), toonDur=0.12),
            k(r(BAR16 - 0.14), toon=CLAMP({'lid': 0.4, 'brow': -0.7, 'mouth': 'line', 'gx': 0.7, 'gy': 0.3}, 0.0, [1.05, 0.94, 1.05]), toonDur=0.08),   # a dip...
            k(BAR16, toon=HOLD16({'lid': 0.3, 'brow': -0.7, 'mouth': 'clench', 'gx': 0.7, 'gy': 0.3}, [0.96, 1.05, 0.96]), toonDur=0.08, toonEase='out'),   # ...and the censor bar is on him
            k(r(BAR16 + 0.25), toon=HOLD16({**FL1, 'gx': 0.7, 'gy': 0.3}), toonDur=0.15), k(1.95, toon=HOLD16({'lid': 0.3, 'brow': -0.3, 'mouth': 'smirk'}), toonDur=0.12),
            k(2.2, toon=HOLD16({'lid': 1.0, 'brow': -0.3, 'mouth': 'smirk'}), toonDur=0.06), k(2.32, toon=HOLD16({'lid': 0.3, 'brow': -0.3, 'mouth': 'smirk'}), toonDur=0.08)]),
        act('flic2', F2, -80, 'stand', 'neutral', keys=[k(0.0, look=[ME1[0], 1.6, ME1[2]]), k(0.1, toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.9}, 'sq': [0.95, 1.07, 0.95]}, toonDur=0.08, toonEase='out'),   # he sees the jumper...
            k(0.28, look='camera', lookDur=0.12), k(0.3, toon={**EYES2(), 'face': {'lid': 1.0, 'mouth': 'O'}}, toonDur=0.12),   # ...and covers both eyes, his face to us
            k(PEEK16, toon={**EYES2(True), 'face': {'lid': 0.0, 'lidL': 1.0, 'eye': 0.42, 'gx': -0.85, 'mouth': 'o', 'brow': 0.6}}, toonDur=0.1, toonEase='out'),   # one hand slides down, fingers spread: one eye peeks...
            k(r(PEEK16 + 0.42), toon={**EYES2(), 'face': {'lid': 1.0, 'mouth': 'wavy'}, 'sq': [0.94, 1.07, 0.94]}, toonDur=0.05, toonEase='in'),   # ...and it snaps back up
            k(r(PEEK16 + 0.6), toon={**EYES2(), 'face': {'lid': 1.0, 'mouth': 'wavy'}}, toonDur=0.12), k(2.05, toon={**EYES2(), 'face': {'lid': 1.0, 'mouth': 'wavy', 'tremble': 0.8}, 'sq': [1.02, 0.98, 1.02]}, toonDur=0.15)])],
        props=[MJ('pull16', False), JUMP('pj16a', 'flic1', '#2F4A8A', tag=0.95, tagSide=1, tagLean=0.04, tagKick=[CUFF16, BAR16], tagKickAmp=0.6), JUMP('pj16b', 'flic2', '#2F4A8A', tag=0.95, tagSide=-1, tagLean=0.04, tagKick=[0.35, r(PEEK16 + 0.44)], tagKickAmp=0.6),   # upright labels, between the heads
               P('menottes16', 'bigCuffs', on={'actor': 'mec', 'hand': 'R', 'offset': [0.07, 0.0, 0.06], 'face': 'camera'}, opts={'r': 0.075, 'thick': 0.24, 'color': '#D2D6DB'}, keys=[k(0.0, visible=False), k(CUFF16, visible=True, scale=1.4), k(r(CUFF16 + 0.12), scale=1.0)]),
               P('censure16', 'censorBar', pos=CB16, face='camera', opts={'w': 0.7, 'h': 0.34}, keys=[k(0.0, visible=False), k(BAR16, visible=True, scale=1.3), k(r(BAR16 + 0.1), scale=1.0)]),
               P('paume16', 'bigPalm', on={'actor': 'flic2', 'hand': 'R', 'offset': [0.0, -0.05, 0.05], 'face': 'camera'}, opts={'w': 0.26, 'spread': [PEEK16, r(PEEK16 + 0.42)]}, keys=[k(0.0, visible=False), k(0.3, visible=True)])],   # (final pass) a big palm over both eyes, its fingers parting for the peek
        cams=[FC(0.0, [r(ME1[0] + FW[0] * 2.4 + LW[0] * 0.1), 1.3, r(ME1[2] + FW[1] * 2.4 + LW[1] * 0.1)], [[ME1[0], 2.6, ME1[2]], [F1[0], 2.55, F1[2]], [F2[0], 2.55, F2[2]],
                          [r(F1[0] - LW[0] * 0.32), 1.5, r(F1[2] - LW[1] * 0.32)], [r(F2[0] + LW[0] * 0.32), 1.5, r(F2[2] + LW[1] * 0.32)], [ME1[0], 0.5, ME1[2]]], top=0.2, bottom=0.95)])   # (review 2) closer: the three fill the frame under the card, the cuffs low on the plain red
st.cue('sfx:click', 'S16', CUFF16, 0.3); st.cue('sfx:whistle', 'S16', 0.2, 0.2); st.cue('pop', 'S16', BAR16, 0.2)

# 17: he was sentenced... The courtroom, close: the judge, a label standing beside his wig, winds the gavel up out to the side and brings it down on its
#     block; the bench, the wig and the label bounce; (review 2) a navy front on the bench: the caption sat on plain red
D17 = st.dur('S17'); BANG17 = 0.34; JG = [0.0, 0.3, -4.0]; BLK17 = [-0.19, 1.53, -3.45]   # (stills 3) under the point where the gavel's head lands (projected from the S17 camera: screen 0.37, 0.62); at x -0.72 it sat a quarter of the frame to the left
GAV = lambda x, y, z, f, sq=None: {'reach': {'R': [x, y, z, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': f, **({'sq': sq} if sq else {})}
st.shot('S17', 'courtroom', actors=[act('juge', JG, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=GAV(-0.72, 2.7, -3.6, {'lid': 0.2, 'brow': -0.5, 'mouth': 'line'}), toonDur=0.0),
            k(0.05, toon=GAV(-0.8, 2.95, -3.75, {'lid': 0.2, 'brow': -0.7, 'mouth': 'line'}, [0.95, 1.07, 0.95]), toonDur=0.12, toonEase='out'),   # the wind-up, out beside his head...
            k(r(BANG17 - 0.07), toon=GAV(-0.2, 1.64, -3.3, {'lid': 0.0, 'brow': -0.8, 'mouth': 'open'}, [1.08, 0.9, 1.08]), toonDur=0.07, toonEase='in'),   # ...the hit
            k(r(BANG17 + 0.03), toon=GAV(-0.22, 1.96, -3.3, {'lid': 0.0, 'brow': -0.8, 'mouth': 'open'}, [0.97, 1.04, 0.97]), toonDur=0.08), k(r(BANG17 + 0.15), toon=GAV(-0.2, 1.67, -3.3, {'lid': 0.3, 'brow': -0.6, 'mouth': 'line'}), toonDur=0.1),   # the bounce
            *BL(0.62, {'lid': 0.3, 'brow': -0.6, 'mouth': 'line'})])],
        props=[P('gav17', 'gavel', on={'actor': 'juge', 'hand': 'R', 'offset': [0.0, -0.02, 0.05]}), P('etiq17', 'careLabel', on={'actor': 'juge', 'joint': 'torso', 'offset': [0.32, 0.58, -0.08]}, opts={'s': 1.3, 'lean': -0.3, 'kick': [r(BANG17 + 0.02)], 'kickAmp': 1.3}),
               P('bloc17', 'soundBlock', pos=BLK17, scale=1.5, keys=[k(BANG17, squash=[1.25, 0.6, 1.25], dur=0.2)]),
               P('devant17', 'slab', pos=[0.0, 0.76, -2.925], opts={'w': 3.3, 'h': 1.5, 'd': 0.05, 'color': '#27374F', 'outline': 0.006})],
        cams=[FC(0.0, [0.75, 2.25, -1.5], [[0.0, 2.95, -4.0], [0.0, 1.5, -3.5], [-0.95, 2.9, -3.7], [0.75, 2.3, -4.0]], top=0.16, bottom=0.76)], fx=[{'type': 'shake', 'at': BANG17, 'dur': 0.2, 'amount': 0.012}])
st.cue('clang', 'S17', BANG17, 0.4)

# 18: ...to wear his jumper inside out. On the pavement, the jumper right side out: a sigh; one hand to his collar, (review 2) one flat, resigned yank
#     over his head: inside out again; then the label shoots up over his shoulder half as big again, stretched, and boings three times; his eyes
#     slide to it (review 1: it opened already inside out)
D18 = st.dur('S18'); T18 = 0.3; TD18 = 0.4; POP18 = r(T18 + 0.8 * TD18)
Y18 = lambda a, y, f, sq=None, **more: {'reach': {'R': [r(ME1[0] + FW[0] * a), y, r(ME1[2] + FW[1] * a), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': f, **({'sq': sq} if sq else {}), **more}
SAD = {'lid': 0.6, 'mouth': 'line', 'brow': -0.2}; TILT18 = {'bend': {'neck': [0.0, 0.0, 0.2, 1, None]}}
st.shot('S18', 'parisStreet', setOpts=PARIS_CLR, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look=[r(ME1[0] + FW[0] * 1.2), 0.9, r(ME1[2] + FW[1] * 1.2)]), k(0.0, toon={'face': SAD}, toonDur=0.0),
            k(0.06, toon={'sq': [1.03, 0.96, 1.03], 'face': SAD}, toonDur=0.12),   # a sigh
            k(0.2, toon=Y18(-0.14, 1.74, SAD), toonDur=0.1, toonEase='out'), k(0.22, look='camera', lookDur=0.1),   # one hand to the collar at his nape, his head up
            k(T18, toon=Y18(0.06, 2.5, SAD, [0.97, 1.04, 0.97]), toonDur=0.12, toonEase='out'),   # one flat yank up...
            k(r(T18 + 0.68 * TD18), toon=Y18(0.34, 1.3, SAD, [1.08, 0.9, 1.08]), toonDur=0.08, toonEase='in'),   # ...and down in front
            k(r(POP18 + 0.12), toon={**TILT18, 'sq': [0.98, 1.03, 0.98], 'face': {'lid': 0.1, 'eye': 0.25, 'gx': 0.9, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.12),   # the arm drops; his eyes slide to the label that boings beside him
            k(r(POP18 + 0.55), toon={**TILT18, 'face': {**DEAD, 'gx': 0.9, 'mouth': 'line'}}, toonDur=0.2), k(1.45, toon={**TILT18, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12),   # ...and come back to us
            *BL(1.56, {**DEAD, 'mouth': 'line'}, **TILT18)])],
        props=[MJ('pull18', False, turn={'at': T18, 'dur': TD18, 'amp': 0.45}, popS=1.5, popAmp=0.6, popDecay=3.4, popFreq=19.0, tagKickAmp=1.4, tagSway=0.05, under='#1F3550')],
        cams=[FC(0.0, [3.98, 1.8, 2.92], [[ME1[0], 3.0, ME1[2]], [ME1[0], 0.55, ME1[2]], LBL(ME1, -60, 1, 0.6, 2.5), [r(ME1[0] - 0.35), 2.0, r(ME1[2] + 0.2)], [r(ME1[0] + 0.55), 2.0, r(ME1[2] + 0.3)]], top=0.1, bottom=0.9)])   # (review 2) from his label's side, down to the knees: the caption falls on his navy trousers (it sat on the salmon knit)
st.cue('sfx:zip', 'S18', T18, 0.2); st.cue('pop', 'S18', POP18, 0.25)

# 19: for life. Close on him: deadpan, the label up beside his head, still wobbling; a look at us; a slow blink; (review 2) framed down to the hem: the
#     caption on his trousers; (final pass) the label stays as big as S18 made it (it shrank back on the last word), gives one small boing on « À vie »
#     and sags slowly; a breath and a shoulder settle under the blink
D19 = st.dur('S19'); L19 = LBL(ME1, -60, 1, 0.6, 1.9); SQ19 = lambda t_: [r(1 - 0.02 * math.sin(PI * min(1.0, t_ / 1.2))), r(1 + 0.03 * math.sin(PI * min(1.0, t_ / 1.2))), r(1 - 0.02 * math.sin(PI * min(1.0, t_ / 1.2)))]
st.shot('S19', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': SQ19(0.35)}, toonDur=0.12, toonEase='inOut'), k(0.55, toon={'face': {**DEAD, 'mouth': 'line'}, 'sq': SQ19(0.55)}, toonDur=0.12, toonEase='inOut'),   # a breath in...
            k(0.9, toon={'face': {**DEAD, 'mouth': 'line', 'gx': 0.7}, 'sq': SQ19(0.9)}, toonDur=0.1), k(1.2, toon={'face': {**DEAD, 'mouth': 'line'}, 'sq': [1.02, 0.97, 1.02]}, toonDur=0.14),   # his eyes go to the sagging label, and back to us; the shoulders settle
            k(1.4, toon={'face': {'lid': 1.0, 'mouth': 'line'}, 'sq': [1.02, 0.97, 1.02]}, toonDur=0.08), k(1.54, toon={'face': {**DEAD, 'mouth': 'line'}, 'sq': [1.01, 0.99, 1.01]}, toonDur=0.1)])],
        props=[MJ('pull19', tag=1.5, tagSway=0.06, tagKick=[0.05, 0.3], tagKickAmp=0.8, tagSag={'at': 0.45, 'dur': 0.9, 'amp': 0.38})],
        cams=[FC(0.0, [2.9, 2.1, 1.6], [[ME1[0], 2.5, ME1[2]], [ME1[0], 0.98, ME1[2]], [L19[0], 2.45, L19[2]], [r(L19[0] + 0.22), 2.3, L19[2]], [r(ME1[0] - 0.3), 2.0, ME1[2]]], top=0.05, bottom=0.66)])   # (stills 2) the snap push-in on his face (x 1.14) lowers the hem: framed higher, it stays above the caption band

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
# (review 1) the jumpers' sleeves: each wearer's jacket in the colour of his jumper (and trousers of his own): the arms read as knitted sleeves
SL = lambda preset, col, seed, pants=None, **kw: {'preset': preset, 'seed': seed, 'suit': col, 'lapel': col, **({'pants': pants} if pants else {}), 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX, **kw}
MEC = {'preset': 'lemec', 'atlasBody': False, 'tint': '#E6F2FF', 'suit': '#C8322A', 'lapel': '#C8322A', 'pants': '#1F3550', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}
st.write("Le pull", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'mec_reflet': dict(MEC),
    'pass1': SL('madame', COLS[0], 761, build={'width': 0.92, 'headWidth': 1.25}),
    'pass2': SL('tourist', COLS[1], 762),
    'coll': SL('lemec_beige', '#2F62B5', 763, '#3A3D44'),
    **{f'emp{j + 1}': SL(['journaliste', 'femme', 'lemec_brown', 'madame', 'boss', 'femme'][j], COLS[j % len(COLS)], 764 + j, '#3A3D44' if j in (2, 4) else None) for j in range(6)},   # (final pass) the bald one at the back: from behind, the front one's dropped head read as a blank flesh block
    **{f'ville{j + 1}': SL(['madame', 'tourist', 'lemec_charcoal', 'femme', 'journaliste', 'gamin'][j], COLS[(j + 2) % len(COLS)], 771 + j, '#3A3D44' if j == 2 else None, **({'build': {'height': 0.62, 'width': 0.85, 'headScale': 1.15}} if j == 5 else {})) for j in range(6)},
    'coutu': {'preset': 'madame', 'seed': 778, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'presentateur': SL('journaliste', '#E8A33C', 779),
    'president': SL('politique', '#2F62B5', 780, '#4A4D55', tie='#9A1F2E', hair='crew', hairColor='#C4C8CF'),   # (review 2) a solid block of grey hair (a slicked white sliver merged with the lettering behind)
    'mod1': SL('femme', '#C255C8', 781, build={'width': 0.85, 'headWidth': 1.2}),
    'mod2': SL('mecBeau', '#F2C94E', 782, '#2B2E3A', build={'width': 0.9, 'headWidth': 1.2}),
    'mod3': SL('femme', '#3FA36C', 797, build={'width': 0.85, 'headWidth': 1.2}),
    'mod4': SL('lemec_brown', '#E0813A', 798, '#2B2E3A', build={'width': 0.9, 'headWidth': 1.2}),
    **{f'photo{j + 1}': {'preset': 'journaliste', 'seed': 783 + j, 'suit': ['#C9B79A', '#9FB0C4', '#B9A7C9', '#A9C2A0'][j], 'lapel': ['#C9B79A', '#9FB0C4', '#B9A7C9', '#A9C2A0'][j], 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(4)},   # (review 2) pale suits: navy photographers on a navy wall
    **{f'rue{j + 1}': SL(['femme', 'boss', 'madame', 'tourist', 'journaliste'][j], COLS[(j + 4) % len(COLS)], 788 + j, '#3A3D44' if j == 1 else None) for j in range(5)},
    'flic1': SL('cop', '#2F4A8A', 794),
    'flic2': SL('cop2', '#2F4A8A', 795),
    'juge': {'preset': 'judge', 'seed': 796, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
