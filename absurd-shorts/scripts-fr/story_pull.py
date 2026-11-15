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

for g_ in [('S02', 0.6, 'mec', 'label'), ('S05', 0.6, 'mec', 'office'), ('S13', 1.1, 'mec', 'reflection'), ('S14', 0.95, 'mec', 'flip'), ('S16', 1.2, 'mec', 'arrest'), ('S19', 0.5, 'mec', 'end')]:
    st.gag(*g_)
st.card('S07', 'DEHORS', at=0.5)
st.card('S12', "À L'ENVERS", at=0.5)
st.card('S16', 'INDÉCENT', at=0.8)

# 1: the hook. Out of his building door onto the street, a red knitted jumper over his suit, the label up over his shoulder, deadpan
D1 = st.dur('S01'); ME1 = [4.6, 0, 0.6]
st.shot('S01', 'parisStreet', setOpts=PARIS, actors=[act('mec', [6.6, 0, 0.6], -90, 'walk', 'neutral', keys=[k(0.0, to=ME1, dur=r(D1 - 0.2), clip='walk', then='stand', ease='out'), k(0.0, look=[0.0, 1.8, 0.6]), k(r(D1 - 0.3), look='camera')])],
        props=[MJ('pull1', tagSway=0.14, tagRate=9.0, tagKick=[r(D1 - 0.2)])],
        cams=[FC(0.0, [2.6, 1.5, 3.2], [[ME1[0], 2.45, ME1[2]], [ME1[0], 0.0, ME1[2]], [6.6, 2.45, 0.6], [6.6, 0.0, 0.6]], top=0.14, bottom=0.78)])
st.cue('sfx:stepSoft', 'S01', 0.3, 0.15); st.cue('sfx:stepSoft', 'S01', 0.7, 0.15)

# 2: ...inside out. Close from behind his shoulder: the white care label standing up over it, the pale seams outside; a burst points at it
D2 = st.dur('S02'); L2 = LBL(ME1, -90)
st.shot('S02', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -90, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 0.6]), k(0.6, toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.2), k(0.95, toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.25)])],
        props=[MJ('pull2', tagKick=[0.35]), BURST('etiq2', [r(L2[0] + 0.12), 2.42, r(L2[2] + 0.16)], 0.35, "L'ÉTIQUETTE !", 0.44, 0.5)],
        cams=[FC(0.0, [5.9, 2.0, 1.75], [[ME1[0], 2.45, ME1[2]], [ME1[0], 1.4, ME1[2]], [L2[0], 1.95, r(L2[2] + 0.12)], [L2[0], 1.58, r(L2[2] - 0.1)], [r(L2[0] + 0.12), 2.66, r(L2[2] + 0.16)], [r(L2[0] + 0.12), 2.42, r(L2[2] + 0.42)]], top=0.12, bottom=0.74)])   # (review 1) the burst inside the frame, over the label
st.cue('sfx:sting', 'S02', 0.35, 0.15)

# 3: nobody dared tell him. On the pavement: two passers-by stare at the label as he walks past, open their mouths, then look away whistling
D3 = st.dur('S03'); PASS3 = [('pass1', 5.45, -0.4, 90), ('pass2', 6.95, 0.3, -110)]
st.shot('S03', 'parisStreet', setOpts={**PARIS, 'clouds': 0}, actors=[act('mec', [6.2, 0, -1.2], 0, 'walk', 'neutral', keys=[k(0.0, to=[6.2, 0, 0.9], dur=D3, clip='walk', ease='linear'), k(0.0, look='camera')]),
        *[act(pid, [px, 0, pz], pry, 'stand', 'neutral', keys=[k(0.0, look=[6.5, 1.8, -0.9]), k(0.3, look=[6.5, 1.8, 0.1]), k(0.3, toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.08, toonEase='out'),
            k(r(0.8 + 0.12 * j), look=[r(px + (-1.2 if j == 0 else 1.2)), 3.4, r(pz + 2.5)], lookDur=0.15), k(r(0.8 + 0.12 * j), toon={'face': {'lid': 0.4, 'mouth': 'whistle', 'brow': 0.4}}, toonDur=0.12),
            k(r(1.25 + 0.1 * j), toon={'face': {'lid': 1.0, 'mouth': 'whistle', 'brow': 0.4}}, toonDur=0.05), k(r(1.36 + 0.1 * j), toon={'face': {'lid': 0.4, 'mouth': 'whistle', 'brow': 0.4}}, toonDur=0.07)]) for j, (pid, px, pz, pry) in enumerate(PASS3)]],
        props=[MJ('pull3', tagSway=0.14, tagRate=9.0), *[JUMP(f'pj3{j}', pid, COLS[j], inside=False) for j, (pid, px, pz, pry) in enumerate(PASS3)]],
        cams=[FC(0.0, [5.9, 1.5, 4.4], [[6.2, 2.5, 0.9], [6.2, 0.0, 0.9], [5.1, 2.45, -0.4], [7.3, 2.45, 0.3], [5.1, 0.0, -0.4], [7.3, 0.0, 0.3]], top=0.14, bottom=0.76)])   # (review 1) both passers-by whole in the frame
st.cue('sfx:whistle', 'S03', 0.8, 0.2)

# 4: the next day his colleague did the same. The office, waist up: the colleague comes in beside him, his blue jumper inside out, label up; they
#    look at each other; a nod, one after the other
D4 = st.dur('S04'); M4 = [-0.45, 0, -0.6]; C4 = [0.6, 0, -0.3]
NOD = lambda t_: [k(t_, toon={'bend': {'neck': [0.4, 0, 0, 1, None]}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1, toonEase='out'), k(r(t_ + 0.2), toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.14)]
st.shot('S04', 'office', actors=[act('mec', M4, 35, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0), k(0.5, look=[1.6, 1.9, 0.2]), k(1.0, look=[C4[0], 2.0, C4[2]]),
            k(0.3, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.05), k(0.42, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.07), *NOD(1.3), k(1.95, look='camera')]),
        act('coll', [2.3, 0, 0.3], -100, 'walk', 'neutral', keys=[k(0.0, to=C4, dur=1.0, clip='walk', then='stand', ease='out'), k(1.0, face=-40, turn=0.25), k(0.0, look=[M4[0], 2.0, M4[2]]), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            *NOD(1.55), k(2.0, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.05), k(2.12, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.07)])],
        props=[MJ('pull4', tagKick=[1.32]), JUMP('pj4', 'coll', '#2F62B5', tagSway=0.12, tagRate=8.0, tagKick=[1.0, 1.57])],
        cams=[FC(0.0, [0.25, 1.6, 2.5], [[M4[0], 2.5, M4[2]], [C4[0], 2.5, C4[2]], [r(M4[0] - 0.4), 1.05, M4[2]], [r(C4[0] + 0.45), 1.05, C4[2]], LBL(C4, -40, 1, 0.66, 1.92)], top=0.14, bottom=0.82)])   # (review 1) a waist-up two-shot, both labels in frame

# 5: then the whole office. From behind the rows, three-quarter back: every worker in a jumper inside out, a field of white labels bobbing over the
#    shoulders with the typing; he stands at the far end, facing them (review 1: from the front the labels hid behind the necks)
D5 = st.dur('S05'); W5 = [(-0.5, 1.3), (0.5, 1.3), (-0.5, 0.2), (0.5, 0.2), (-1.1, -1.9), (1.1, -1.9)]; M5 = [0.0, 0, -1.15]   # two columns down an aisle, backs to us: in a tall frame the rows stack up to him
st.shot('S05', 'office', setOpts={'printer': False}, actors=[act('mec', M5, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.7, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06), k(0.83, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.08)]),
        *[act(f'emp{j + 1}', [x, 0, z], 180, 'sitWrite', 'neutral', keys=[k(0.0, look=[x, 0.8, r(z - 0.5)]), k(r(0.25 + 0.15 * j), look=[x, 1.1, r(z - 0.6)]), k(r(0.7 + 0.1 * j), look=[x, 0.8, r(z - 0.5)])]) for j, (x, z) in enumerate(W5)]],
        props=[MJ('pull5'), *[JUMP(f'pj5{j}', f'emp{j + 1}', COLS[j % len(COLS)], tagSide=1 if j % 2 else -1, tagSway=0.12, tagRate=r(7.0 + 0.6 * j), tagPhase=r(1.1 * j), tagKick=[r(0.25 + 0.15 * j), r(0.75 + 0.1 * j)]) for j in range(len(W5))],   # the labels on the aisle side
               *[P(f'ch5{j}', 'chair', pos=[x, 0, z]) for j, (x, z) in enumerate(W5)], *[P(f'dk5{j}', 'desk', pos=[x, 0, r(z - 0.55)], opts={'w': 0.9}) for j, (x, z) in enumerate(W5)]],
        cams=[FC(0.0, [0.3, 2.5, 4.3], [[-0.86, 1.3, 1.3], [0.86, 1.3, 1.3], [M5[0], 2.55, M5[2]], [0.0, 0.95, 1.3]], top=0.14, bottom=0.8)])

# 6: then the whole town. A street: everyone walking by in jumpers inside out, labels up; him in the middle
D6 = st.dur('S06'); CROWD6 = [(3.4, -0.4, 180), (5.6, -0.9, 180), (3.0, -2.2, 0), (5.9, -2.6, 180), (4.1, -3.6, 180), (6.3, 0.2, 180)]
st.shot('S06', 'parisStreet', setOpts=PARIS, actors=[act('mec', [4.6, 0, -1.8], 0, 'walk', 'neutral', keys=[k(0.0, to=[4.6, 0, -0.2], dur=D6, clip='walk', ease='linear'), k(0.0, look='camera')]),
        *[act(f'ville{j + 1}', [x, 0, z], ry, 'walk', 'neutral', keys=[k(0.0, to=[x, 0, r(z + (1.6 if ry == 0 else -1.6))], dur=D6, clip='walk', ease='linear')]) for j, (x, z, ry) in enumerate(CROWD6)]],
        props=[MJ('pull6', tagSway=0.14, tagRate=9.0), *[JUMP(f'pj6{j}', f'ville{j + 1}', COLS[(j + 2) % len(COLS)], tagSide=1 if j % 2 else -1, tagSway=0.14, tagRate=r(8.0 + 0.5 * j), tagPhase=r(0.9 * j)) for j in range(len(CROWD6))]],
        cams=[FC(0.0, [4.4, 3.0, 8.6], [[4.6, 2.45, -1.8], [4.6, 0.0, -0.2], [3.4, 2.4, -0.4], [5.6, 2.4, -0.9]], top=0.16, bottom=0.76, lenses=range(16, 40))])   # long lens: the crowd packs up behind him

# 7: the shops sewed their labels on the outside. A clothes shop: with an oversized needle and a red thread the seamstress sews a label onto the
#    chest of a jumper, stitch after stitch; a pile of jumpers, labels out, on the table (DEHORS)
D7 = st.dur('S07'); J7 = [0.05, 1.12, -1.45]; SEW7 = [r(J7[0] + 0.07), r(J7[1] + 0.2), r(J7[2] + 0.2)]
ST7 = lambda far, f: {'reach': {'R': [r(SEW7[0] + 0.02 + 0.2 * far), r(SEW7[1] + 0.02 + 0.2 * far), r(SEW7[2] + 0.05 + 0.16 * far), 1, 0.04], 'L': [r(J7[0] - 0.24), r(J7[1] + 0.46), r(J7[2] + 0.02), 1, 0.04]}, 'hands': {'R': 'pinch', 'L': 'grip'}, 'face': f}
K7 = [k(0.0, look=SEW7), k(0.0, toon=ST7(1, {'lid': 0.3, 'mouth': 'smile'}), toonDur=0.0)]
for j in range(5):
    K7 += [k(r(0.22 + 0.44 * j), toon={**ST7(0, {'lid': 0.4, 'mouth': 'smile', 'brow': -0.2}), 'sq': [1.02, 0.98, 1.02]}, toonDur=0.1, toonEase='in'), k(r(0.42 + 0.44 * j), toon=ST7(1, {'lid': 0.3, 'mouth': 'smile'}), toonDur=0.16, toonEase='out')]
K7 += [k(1.6, look='camera', lookDur=0.15), k(2.05, look=SEW7)]
st.shot('S07', 'poste', setOpts={'title': ' ', 'guichets': False}, actors=[act('coutu', [0.0, 0, -1.9], 0, 'stand', 'happy', keys=K7)],
        props=[P('pull7', 'knitJumper', pos=J7, scale=0.8, opts={'color': '#2F8F6B', 'inside': False, 'tie': False, 'sewn': 0.5}), P('tas7', 'jumperPile', pos=[1.4, 0, -1.6]),
               P('aiguille7', 'sewNeedle', on={'actor': 'coutu', 'hand': 'R', 'offset': [0.0, -0.12, 0.04], 'rot': [3.1416, 0, 0]}, opts={'s': 1.3}),   # the point out past her fingers (the hand's +y runs up the arm)
               P('ens7', 'signBoard', pos=[1.5, 2.2, -3.3], opts={'text': 'PRÊT-À-PORTER', 'bg': '#F2C230', 'fg': '#2C4A8A', 'w': 1.5, 'h': 0.3, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [0.55, 1.6, 0.45], [[0.0, 2.5, -1.9], [J7[0], r(J7[1] - 0.02), J7[2]], [-0.45, 1.5, -1.5], [0.6, 1.5, -1.2], [1.0, 1.0, -1.6]], top=0.24, bottom=0.76)])   # (review 1) tighter: the stitch and the label on the chest
st.cue('sfx:tick', 'S07', 0.22, 0.12); st.cue('sfx:tick', 'S07', 0.66, 0.12); st.cue('sfx:tick', 'S07', 1.1, 0.12); st.cue('sfx:tick', 'S07', 1.54, 0.12)

# 8: the news presenter... The news desk: the presenter reads the news, a big JOURNAL backdrop, the label up over his shoulder
D8 = st.dur('S08'); PRES = [0.0, 0, 0.3]; NEWS = {'backdrop': 'LE JOURNAL', 'fontScale': 0.6, 'podium': False, 'chairs': False, 'flags': False, 'bg': '#5878A8', 'wall': '#4C6A96'}
st.shot('S08', 'pressRoom', setOpts=NEWS, actors=[act('presentateur', PRES, 0, 'sitTalk', 'neutral', keys=[k(0.0, look='camera'), k(0.9, look=[0.25, 0.8, 0.85], lookDur=0.15), k(1.25, look='camera', lookDur=0.15)])],
        props=[P('desk8', 'desk', pos=[0.0, 0, 0.85], opts={'w': 1.6}), P('ch8', 'chair', pos=PRES), JUMP('pj8', 'presentateur', '#E8A33C', tagKick=[0.92]), P('feuille8', 'paperSheet', pos=[0.25, 0.77, 0.9], rot=[-PI / 2, 0, 0], opts={'w': 0.25, 'h': 0.32, 'lines': ['INFOS']})],
        cams=[FC(0.0, [0.3, 1.5, 3.2], [[0.0, 2.2, 0.3], [0.0, 0.8, 0.75], [-0.75, 1.2, 0.75], [0.75, 1.2, 0.75], [0.5, 1.7, 0.2]], top=0.14, bottom=0.8)])

# 9: ...wore it live. From behind, at his shoulder: the white label standing between his head and the red EN DIRECT light of the camera in front
D9 = st.dur('S09'); TV9 = [0.95, 0, 2.5]
st.shot('S09', 'pressRoom', setOpts=NEWS, actors=[act('presentateur', PRES, 0, 'sitTalk', 'neutral', keys=[k(0.0, look=[TV9[0], 1.5, TV9[2]]), k(0.7, toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.15), k(1.0, toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.2)])],
        props=[P('desk9', 'desk', pos=[0.0, 0, 0.85], opts={'w': 1.6}), P('ch9', 'chair', pos=PRES), JUMP('pj9', 'presentateur', '#E8A33C', tagKick=[0.3, 0.75]), P('tv9', 'tvCamera', pos=TV9, ry=180),
               P('direct9', 'signBoard', pos=[r(TV9[0] + 0.1), 1.6, r(TV9[2] - 0.35)], ry=180, opts={'text': 'EN DIRECT', 'bg': '#D22B2B', 'fg': '#FFFFFF', 'w': 0.7, 'h': 0.2, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [-0.3, 1.55, -1.2], [[0.0, 2.05, 0.3], [-0.2, 1.1, 0.3], [0.5, 1.25, 0.2], [r(TV9[0] + 0.5), 1.75, r(TV9[2] - 0.35)], [0.0, 0.78, 0.85]], top=0.16, bottom=0.74, inside=(-5.0, 5.0, 0.5, 3.0, -2.8, 6.0))])   # (review 1) the label between the head and the red light, above the caption band

# 10: the president gave his wishes... At the lectern between two flags, the president, solemn
D10 = st.dur('S10'); PR10 = [0.0, 0, -0.3]; ELY = {'backdrop': 'PRÉSIDENCE', 'fontScale': 0.6, 'podium': False, 'bg': '#5878A8', 'wall': '#4C6A96'}
st.shot('S10', 'pressRoom', setOpts=ELY, actors=[act('president', PR10, 0, 'podiumTalk', 'neutral', keys=[k(0.0, look='camera'), k(0.45, toon={'face': {'lid': 1.0}}, toonDur=0.06), k(0.58, toon={'face': {'lid': 0.2}}, toonDur=0.08)])],
        props=[P('pod10', 'podium', pos=[0.0, 0, 0.2], opts={'text': 'RÉPUBLIQUE'}), JUMP('pj10', 'president', '#2F62B5', tag=1.25), *[P(f'fl10{j}', 'flag', pos=[r(-0.85 + 1.7 * j), 0, -0.6], opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A'], 'vertical': True}) for j in range(2)]],
        cams=[FC(0.0, [0.95, 0.7, 2.9], [[0.0, 2.6, PR10[2]], [0.0, 0.55, 0.46], [-1.0, 2.2, -0.6], [1.0, 2.2, -0.6]], top=0.14, bottom=0.74)])   # (review 1) the RÉPUBLIQUE plate above the captions, both flags in

# 11: ...in a jumper inside out. Close on him: the big label standing beside his solemn face, the seams on his shoulders; it flops when he nods
D11 = st.dur('S11'); L11 = LBL(PR10, 0, 1, 0.66, 1.95)
st.shot('S11', 'pressRoom', setOpts=ELY, actors=[act('president', PR10, 0, 'podiumTalk', 'neutral', keys=[k(0.0, look='camera'), k(0.5, toon={'bend': {'neck': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.5}}, toonDur=0.12, toonEase='out'), k(0.72, toon={'face': {'lid': 0.2}}, toonDur=0.15),
            k(1.15, toon={'face': {'lid': 1.0}}, toonDur=0.07), k(1.27, toon={'face': {'lid': 0.2}}, toonDur=0.08)])],
        props=[P('pod11', 'podium', pos=[0.0, 0, 0.2], opts={'text': 'RÉPUBLIQUE'}), JUMP('pj11', 'president', '#2F62B5', tag=1.25, tagKick=[0.55])],
        cams=[FC(0.0, [0.7, 2.1, 1.3], [[0.0, 2.6, PR10[2]], [0.0, 1.6, PR10[2]], [L11[0], 2.15, L11[2]], [r(L11[0] + 0.18), 1.75, L11[2]], [-0.35, 2.0, PR10[2]]], top=0.16, bottom=0.74)])

# 12: the fashion shows went inside out. A catwalk, from the end of it, low: a model strides at us in a jumper inside out, its head-tall label flopping
#     at each step, another behind her; flashes on both sides (À L'ENVERS)
D12 = st.dur('S12'); M12 = [('mod1', 0.0, -1.1), ('mod2', 0.0, -3.0)]
st.shot('S12', 'pressRoom', setOpts={'backdrop': 'PARIS', 'fontScale': 0.9, 'podium': False, 'chairs': False, 'bg': '#2B2E3A', 'wall': '#23252E'}, actors=[
        *[act(mid, [mx, 0, mz], 0, 'strut', 'smug', keys=[k(0.0, to=[mx, 0, r(mz + 1.5)], dur=D12, clip='strut', ease='linear'), k(0.0, look='camera')]) for mid, mx, mz in M12],
        *[act(f'photo{j + 1}', [r(-1.3 if j % 2 else 1.3), 0, r(-0.4 + 0.8 * (j // 2))], 90 if j % 2 else -90, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 0.0]), k(0.0, toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            *[k(r(fa), toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 0.97, 1.0]}, toonDur=0.06) for fa in [0.2 + 0.3 * j, 0.9 + 0.25 * j]],
            *[k(r(fa + 0.12), toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.15) for fa in [0.2 + 0.3 * j, 0.9 + 0.25 * j]],
            k(r(1.5 + 0.1 * j), look=[0.0, 1.8, 0.6], lookDur=0.3)]) for j in range(4)]],
        props=[P('podium12', 'floorSlab', pos=[0.0, 0.04, -1.0], opts={'w': 1.2, 'd': 6.0, 'h': 0.08, 'color': '#F4F1E8'}),
               JUMP('pj12a', 'mod1', '#C255C8', tag=2.0, tagSway=0.32, tagRate=9.4), JUMP('pj12b', 'mod2', '#F2C94E', tag=2.0, tagSide=-1, tagSway=0.32, tagRate=9.4, tagPhase=1.6),
               *[P(f'cam12{j}', 'pressCamera', on={'actor': f'photo{j + 1}', 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': [r(0.2 + 0.3 * j), r(0.9 + 0.25 * j)], 'burst': 0.5}) for j in range(4)]],
        cams=[FC(0.0, [0.3, 0.9, 3.0], [[0.0, 2.75, 0.4], [0.0, 0.0, 0.4], [-0.75, 2.2, 0.4], [0.75, 2.2, 0.4]], top=0.2, bottom=0.76)])   # (review 1) low at the end of the catwalk: she fills the frame as she comes
st.cue('sfx:click', 'S12', 0.2, 0.15); st.cue('sfx:click', 'S12', 0.5, 0.15); st.cue('sfx:click', 'S12', 0.8, 0.15); st.cue('sfx:click', 'S12', 1.1, 0.15)

# 13: yesterday he saw himself in a shop window. On the pavement at a big shop window, both of them and both labels in frame: his reflection looks
#     back at him, lifts a finger and taps its own label, twice; his take; he looks at his own shoulder
D13 = st.dur('S13'); ZW = -1.0; ME13 = [0.4, 0, -0.1]; L13 = LBL(ME13, 180); R13 = [L13[0], L13[1], r(2 * ZW - L13[2])]; TAKE13 = 1.1
SRC13 = act('mec', ME13, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.4, 2.0, -2.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
        k(TAKE13, toon={'sq': [0.92, 1.1, 0.92], 'face': {'lid': 0.0, 'pop': 0.6, 'popLen': 0.12, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.06, toonEase='out'),   # the take
        k(r(TAKE13 + 0.4), look=[L13[0], 1.85, L13[2]], lookDur=0.1), k(r(TAKE13 + 0.45), toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.1),   # he looks at his own shoulder
        k(r(D13 - 0.35), look=[0.4, 2.0, -2.0]), k(r(D13 - 0.3), toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.12)])
REF13 = reflection(SRC13, zm=ZW, shift=0.0, id='mec_reflet')
TAP13 = lambda near, f: {'reach': {'L': [r(R13[0] + (0.1 if near else 0.22)), r(1.8 if near else 1.9), r(R13[2] + (0.08 if near else 0.2)), 1, 0.03]}, 'hands': {'L': 'point'}, 'face': f}
REF13['keys'] = REF13['keys'] + [k(0.3, toon=TAP13(0, {'lid': 0.3, 'mouth': 'smirk'}), toonDur=0.15, toonEase='out'), k(0.5, toon=TAP13(1, {'lid': 0.3, 'mouth': 'smirk'}), toonDur=0.06, toonEase='in'), k(0.62, toon=TAP13(0, {'lid': 0.3, 'mouth': 'smirk'}), toonDur=0.08),
                                 k(0.75, toon=TAP13(1, {'lid': 0.3, 'mouth': 'smirk'}), toonDur=0.06, toonEase='in'), k(0.9, toon=TAP13(0, {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.4}), toonDur=0.1)]   # the reflection taps its own label, twice
st.shot('S13', 'parisStreet', setOpts=PARIS, actors=[SRC13, REF13],
        props=[MJ('pull13', tagKick=[r(TAKE13 + 0.02)]), JUMP('pullref13', 'mec_reflet', '#C8322A', True, 0.6, tagSide=-1, tagKick=[0.52, 0.77, r(TAKE13 + 0.02)]),
               P('vitre13', 'slab', pos=[0.4, 1.5, ZW], opts={'w': 2.6, 'h': 2.8, 'd': 0.02, 'color': '#CFE6F2', 'opacity': 0.25}), P('cadre13', 'slab', pos=[0.4, 3.0, ZW], opts={'w': 2.8, 'h': 0.25, 'd': 0.1, 'color': '#2E4563'})],
        cams=[FC(0.0, [-1.15, 1.9, 1.55], [[0.4, 2.5, -0.1], [L13[0], 1.95, L13[2]], [0.78, 1.45, -0.1], [0.4, 1.15, -0.1], [0.4, 2.5, -1.9], [R13[0], 1.95, R13[2]], [0.4, 1.15, -1.9]], top=0.14, bottom=0.78)])   # (review 1) from his label's side: both figures and both labels inside the frame
st.cue('sfx:tick', 'S13', 0.5, 0.2); st.cue('sfx:tick', 'S13', 0.75, 0.2); st.cue('sfx:sting', 'S13', TAKE13, 0.15)

# 14: he turned his jumper right side out. A crouch, then he hauls it up over his head: it stretches over him, head and arms lost inside, bulges
#     twice as he fights it, changes side, snaps down with a squash and wobbles; he smooths it down, pleased (review 1: a texture swap)
D14 = st.dur('S14'); T14 = 0.3; TD14 = 0.8; POP14 = r(T14 + 0.8 * TD14); FW = (-0.866, 0.5); LW = (0.5, 0.866)   # his facing (ry -60) and his left, on the ground
HEM = lambda s_, y=1.08: [r(ME1[0] + FW[0] * 0.27 + LW[0] * 0.2 * s_), y, r(ME1[2] + FW[1] * 0.27 + LW[1] * 0.2 * s_), 1, 0.04]
UP14 = lambda s_, y=2.74: [r(ME1[0] + FW[0] * 0.05 + LW[0] * 0.15 * s_), y, r(ME1[2] + FW[1] * 0.05 + LW[1] * 0.15 * s_), 1, 0.04]
GR = {'L': 'grip', 'R': 'grip'}
SMOOTH = lambda y: {'touch': {'R': ['torso', -0.13, y, 0.27, 1, 0.02], 'L': ['torso', 0.13, y, 0.27, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}}   # the hands on the knit, not through it
st.shot('S14', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.08, toon={'reach': {'L': HEM(1), 'R': HEM(-1)}, 'hands': GR, 'sq': [1.1, 0.86, 1.1], 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.4}}, toonDur=0.16, toonEase='out'),   # a crouch, both hands on the hem...
            k(T14, toon={'reach': {'L': UP14(1), 'R': UP14(-1)}, 'hands': GR, 'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.3, 'mouth': 'clench'}}, toonDur=0.2, toonEase='out'),   # ...and up over his head
            k(r(T14 + 0.3), toon={'reach': {'L': UP14(1, 2.8), 'R': UP14(-1, 2.66)}, 'hands': GR, 'lay': [0.0, 0.14], 'sq': [0.96, 1.06, 0.96], 'face': {'lid': 0.3, 'mouth': 'clench'}}, toonDur=0.1),   # the fight inside
            k(r(T14 + 0.42), toon={'reach': {'L': UP14(1, 2.66), 'R': UP14(-1, 2.8)}, 'hands': GR, 'lay': [0.0, -0.14], 'sq': [0.96, 1.06, 0.96], 'face': {'lid': 0.3, 'mouth': 'clench'}}, toonDur=0.1),
            k(r(T14 + 0.68 * TD14), toon={'reach': {'L': HEM(1), 'R': HEM(-1)}, 'hands': GR, 'sq': [1.2, 0.72, 1.2], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.09, toonEase='in'),   # the snap down
            k(r(POP14 + 0.08), toon={**SMOOTH(0.4), 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.1), k(r(POP14 + 0.32), toon={**SMOOTH(0.16), 'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.24),   # he smooths it down
            k(r(POP14 + 0.6), toon={**SMOOTH(0.16), 'face': {'lid': 1.0, 'mouth': 'smile'}}, toonDur=0.1)])],   # pleased, eyes closed
        props=[MJ('pull14', True, turn={'at': T14, 'dur': TD14})],
        cams=[FC(0.0, [2.6, 1.7, 2.6], [[ME1[0], 3.0, ME1[2]], [ME1[0], 0.75, ME1[2]], [r(ME1[0] - 0.45), 2.2, ME1[2]], [r(ME1[0] + 0.45), 2.2, ME1[2]]], top=0.12, bottom=0.78)])
st.cue('sfx:zip', 'S14', T14, 0.2); st.cue('pop', 'S14', POP14, 0.25)

# 15: the whole street turned round. Behind him the street has its back to us; head after head whips round, then the bodies, to stare at him; a woman's
#     shopping bag hangs in the air a beat, then drops; gasps
D15 = st.dur('S15')
ST15 = [(r(ME1[0] - FW[0] * t + LW[0] * l, 2), r(ME1[2] - FW[1] * t + LW[1] * l, 2)) for t, l in [(1.25, -0.85), (1.3, 1.0), (2.6, -0.3), (2.7, 0.7), (4.0, 0.385)]]
BAG15 = [r(ST15[0][0] + LW[0] * 0.4), r(ST15[0][1] + LW[1] * 0.4)]; DROP15 = 0.62   # beside her, on our side of her: her right hand with her back to us, her left once she has turned
st.shot('S15', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.0), k(0.55, look=[ST15[1][0], 1.9, ST15[1][1]], lookDur=0.12),
            k(0.6, toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.1), k(1.1, look='camera', lookDur=0.12)]),
        *[act(f'rue{j + 1}', [x, 0, z], 120, 'stand', 'neutral', keys=[k(0.0, look=[r(x + 2.6), 1.8, r(z - 1.5)]), *([k(0.0, toon={'reach': {'R': [BAG15[0], 1.22, BAG15[1], 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0)] if j == 0 else []),
            k(r(0.12 + 0.1 * j), look=[ME1[0], 1.9, ME1[2]], lookDur=0.07),   # the head whips round first...
            k(r(0.2 + 0.1 * j), face=r(math.degrees(math.atan2(ME1[0] - x, ME1[2] - z))), turn=0.14),   # ...then the body
            k(r(0.2 + 0.1 * j), toon={**({'reach': {'L': [BAG15[0], 1.3, BAG15[1], 1, 0.04]}, 'hands': {'L': 'spread'}} if j == 0 else {}), 'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}, 'sq': [0.94, 1.07, 0.94]}, toonDur=0.08, toonEase='out')]) for j, (x, z) in enumerate(ST15)]],
        props=[MJ('pull15', False), *[JUMP(f'pj15{j}', f'rue{j + 1}', COLS[(j + 4) % len(COLS)], tagSide=1 if j % 2 else -1, tagKick=[r(0.22 + 0.1 * j)]) for j in range(len(ST15))],
               P('sac15', 'shoppingBag', pos=[BAG15[0], 0.72, BAG15[1]], scale=0.9, keys=[k(0.3, to=[BAG15[0], 0.84, BAG15[1]], dur=0.16, ease='out'), k(DROP15, to=[BAG15[0], 0.0, BAG15[1]], dur=0.2, ease='in'), k(r(DROP15 + 0.2), squash=[1.2, 0.7, 1.2], dur=0.25)])],   # it hangs a beat, then drops
        cams=[FC(0.0, [r(ME1[0] + FW[0] * 2.3 - LW[0] * 0.5), 3.3, r(ME1[2] + FW[1] * 2.3 - LW[1] * 0.5)], [[ME1[0], 2.5, ME1[2]], [ME1[0], 0.3, ME1[2]], *[[x, 2.5, z] for x, z in ST15],
                          [r(ST15[0][0] - LW[0] * 0.2), 1.6, r(ST15[0][1] - LW[1] * 0.2)], [r(ST15[1][0] + LW[0] * 0.2), 1.6, r(ST15[1][1] + LW[1] * 0.2)], [BAG15[0], 0.1, BAG15[1]]], top=0.14, bottom=0.86)])   # (review 1) closer, from above his eye line: the street stacks up behind him
st.cue('sfx:gasp', 'S15', 0.3, 0.3); st.cue('thud', 'S15', r(DROP15 + 0.2), 0.2)

# 16: the police arrested him for indecent dress. Two policemen in jumpers inside out, upright either side of him: one snaps the cuffs on the wrists he
#     holds up; the other stands in front with a hand flat over his eyes, and peeks once (INDÉCENT)
D16 = st.dur('S16'); CUFF16 = 0.6
F1 = [r(ME1[0] - LW[0] * 0.74 + FW[0] * 0.2), 0, r(ME1[2] - LW[1] * 0.74 + FW[1] * 0.2)]; F2 = [r(ME1[0] + LW[0] * 0.78 + FW[0] * 0.34), 0, r(ME1[2] + LW[1] * 0.78 + FW[1] * 0.34)]
WR = lambda s_, y=1.34: [r(ME1[0] + FW[0] * 0.34 + LW[0] * 0.075 * s_), y, r(ME1[2] + FW[1] * 0.34 + LW[1] * 0.075 * s_), 1, 0.04]
OFFER = lambda f: {'reach': {'L': WR(1), 'R': WR(-1)}, 'hands': {'L': 'fist', 'R': 'fist'}, 'face': f}
EYES = {'touch': {'R': ['face', 0.0, 0.12, 0.22, 1, 0.02]}, 'hands': {'R': 'open'}}
CLAMP = lambda f, out=0.0, sq=None: {'reach': {'L': [r(WR(-1)[0] - LW[0] * (0.1 + out) + FW[0] * 0.04), r(1.38 + out), r(WR(-1)[2] - LW[1] * (0.1 + out) + FW[1] * 0.04), 1, 0.04], 'R': [r(WR(-1)[0] - LW[0] * (0.2 + out)), r(1.28 + out), r(WR(-1)[2] - LW[1] * (0.2 + out)), 1, 0.04]},
                                     'hands': {'L': 'grip', 'R': 'grip'}, 'face': f, **({'sq': sq} if sq else {})}
st.shot('S16', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.3, toon=OFFER({**DEAD, 'mouth': 'line'}), toonDur=0.2, toonEase='out'), k(CUFF16, toon={**OFFER({'lid': 0.3, 'mouth': 'line'}), 'sq': [1.02, 0.97, 1.02]}, toonDur=0.06),   # he holds his wrists up; the cuffs snap on
            k(1.0, look=[F1[0], 2.0, F1[2]], lookDur=0.2), k(1.6, look='camera'), k(1.9, toon=OFFER({'lid': 1.0, 'mouth': 'line'}), toonDur=0.1), k(2.05, toon=OFFER({**DEAD, 'mouth': 'line'}), toonDur=0.12)]),
        act('flic1', F1, -22, 'stand', 'determined', keys=[k(0.0, look=WR(-1)[:3]), k(0.0, toon=CLAMP({'lid': 0.3, 'brow': -0.5, 'mouth': 'line'}, 0.2), toonDur=0.0),
            k(r(CUFF16 - 0.12), toon=CLAMP({'lid': 0.3, 'brow': -0.5, 'mouth': 'line'}, 0.28), toonDur=0.1, toonEase='out'), k(CUFF16, toon=CLAMP({'lid': 0.4, 'brow': -0.7, 'mouth': 'clench'}, 0.0, [1.04, 0.96, 1.04]), toonDur=0.05, toonEase='in'),   # a wind-up, snap
            k(1.3, look='camera', lookDur=0.15), k(1.35, toon=CLAMP({'lid': 0.4, 'brow': -0.5, 'mouth': 'line'}), toonDur=0.12), k(2.1, toon=CLAMP({'lid': 1.0, 'brow': -0.5, 'mouth': 'line'}), toonDur=0.06), k(2.22, toon=CLAMP({'lid': 0.4, 'brow': -0.5, 'mouth': 'line'}), toonDur=0.08)]),
        act('flic2', F2, -100, 'stand', 'neutral', keys=[k(0.0, look=[ME1[0], 1.6, ME1[2]]), k(0.3, toon={**EYES, 'face': {'lid': 1.0, 'mouth': 'O'}}, toonDur=0.12),
            k(1.2, toon={'touch': {'R': ['face', 0.0, -0.02, 0.24, 1, 0.02]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.08), k(1.25, look=[ME1[0], 1.3, ME1[2]], lookDur=0.1),
            k(1.6, toon={**EYES, 'face': {'lid': 1.0, 'mouth': 'O'}, 'sq': [0.96, 1.04, 0.96]}, toonDur=0.08), k(2.1, toon={**EYES, 'face': {'lid': 1.0, 'mouth': 'wavy'}}, toonDur=0.15)])],   # covering his eyes, one peek
        props=[MJ('pull16', False), JUMP('pj16a', 'flic1', '#2F4A8A', tagSide=-1, tagKick=[CUFF16]), JUMP('pj16b', 'flic2', '#2F4A8A', tagKick=[0.35, 1.62]),
               P('menottes16', 'bigCuffs', on={'actor': 'mec', 'hand': 'R', 'offset': [0.07, 0.0, 0.06], 'face': 'camera'}, opts={'r': 0.075, 'thick': 0.24, 'color': '#D2D6DB'}, keys=[k(0.0, visible=False), k(CUFF16, visible=True, scale=1.4), k(r(CUFF16 + 0.12), scale=1.0)])],
        cams=[FC(0.0, [r(ME1[0] + FW[0] * 2.4 + LW[0] * 0.1), 1.3, r(ME1[2] + FW[1] * 2.4 + LW[1] * 0.1)], [[ME1[0], 2.6, ME1[2]], [F1[0], 2.55, F1[2]], [F2[0], 2.55, F2[2]], [r(F1[0] - LW[0] * 0.4), 1.5, r(F1[2] - LW[1] * 0.4)], [r(F2[0] + LW[0] * 0.4), 1.5, r(F2[2] + LW[1] * 0.4)],
                          [ME1[0], 0.0, ME1[2]], [F1[0], 0.0, F1[2]], [F2[0], 0.0, F2[2]]], top=0.215, bottom=0.765)])   # (review 1) the three upright and whole, the cuffed wrists high above the captions
st.cue('sfx:click', 'S16', CUFF16, 0.3); st.cue('sfx:whistle', 'S16', 0.2, 0.2)

# 17: he was sentenced... The courtroom, close: the judge, a label standing beside his wig, winds the gavel up out to the side and brings it down; the
#     bench, the wig and the label bounce
D17 = st.dur('S17'); BANG17 = 0.34; JG = [0.0, 0.3, -4.0]
GAV = lambda x, y, z, f, sq=None: {'reach': {'R': [x, y, z, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': f, **({'sq': sq} if sq else {})}
st.shot('S17', 'courtroom', actors=[act('juge', JG, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=GAV(-0.72, 2.7, -3.6, {'lid': 0.2, 'brow': -0.5, 'mouth': 'line'}), toonDur=0.0),
            k(0.1, toon=GAV(-0.8, 2.95, -3.75, {'lid': 0.2, 'brow': -0.7, 'mouth': 'line'}, [0.95, 1.07, 0.95]), toonDur=0.12, toonEase='out'),   # the wind-up, out beside his head...
            k(BANG17, toon=GAV(-0.5, 1.72, -3.3, {'lid': 0.0, 'brow': -0.8, 'mouth': 'open'}, [1.1, 0.88, 1.1]), toonDur=0.07, toonEase='in'),   # ...the hit
            k(r(BANG17 + 0.1), toon=GAV(-0.5, 1.9, -3.3, {'lid': 0.0, 'brow': -0.8, 'mouth': 'open'}, [0.97, 1.04, 0.97]), toonDur=0.08), k(r(BANG17 + 0.24), toon=GAV(-0.5, 1.76, -3.3, {'lid': 0.3, 'brow': -0.6, 'mouth': 'line'}), toonDur=0.1)])],   # the bounce
        props=[P('gav17', 'gavel', on={'actor': 'juge', 'hand': 'R', 'offset': [0.0, -0.02, 0.05]}), P('etiq17', 'careLabel', on={'actor': 'juge', 'joint': 'torso', 'offset': [0.32, 0.58, -0.08]}, opts={'s': 1.3, 'lean': -0.3, 'kick': [r(BANG17 + 0.02)]})],
        cams=[FC(0.0, [0.75, 2.25, -1.5], [[0.0, 2.95, -4.0], [0.0, 1.5, -3.5], [-0.95, 2.9, -3.7], [0.75, 2.3, -4.0]], top=0.16, bottom=0.76)], fx=[{'type': 'shake', 'at': BANG17, 'dur': 0.2, 'amount': 0.012}])
st.cue('clang', 'S17', BANG17, 0.4)

# 18: ...to wear his jumper inside out. On the pavement, the jumper right side out: a sigh; one hand to his collar, one resigned yank over his
#     head: inside out again, and the label springs up over his shoulder and goes on wobbling; his head tilted (review 1: it opened already inside out)
D18 = st.dur('S18'); T18 = 0.4; TD18 = 0.5; POP18 = r(T18 + 0.8 * TD18)
Y18 = lambda a, y, f, sq=None, **more: {'reach': {'R': [r(ME1[0] + FW[0] * a), y, r(ME1[2] + FW[1] * a), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': f, **({'sq': sq} if sq else {}), **more}
SAD = {'lid': 0.6, 'mouth': 'line', 'brow': -0.2}
st.shot('S18', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look=[r(ME1[0] + FW[0] * 1.2), 0.9, r(ME1[2] + FW[1] * 1.2)]), k(0.0, toon={'face': SAD}, toonDur=0.0),
            k(0.1, toon={'sq': [1.03, 0.96, 1.03], 'face': SAD}, toonDur=0.14),   # a sigh
            k(0.27, toon=Y18(-0.14, 1.74, SAD), toonDur=0.12, toonEase='out'),   # one hand to the collar at his nape
            k(T18, toon=Y18(0.08, 2.78, SAD, [0.93, 1.1, 0.93]), toonDur=0.14, toonEase='out'),   # one yank up...
            k(r(T18 + 0.68 * TD18), toon=Y18(0.36, 1.25, SAD, [1.16, 0.78, 1.16]), toonDur=0.09, toonEase='in'),   # ...and down in front
            k(r(POP18 + 0.16), toon={'bend': {'neck': [0.0, 0.0, 0.22, 1, None]}, 'sq': [0.98, 1.03, 0.98], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.16),   # the arm drops, the head tilted
            k(1.2, look='camera', lookDur=0.15), k(1.42, toon={'bend': {'neck': [0.0, 0.0, 0.22, 1, None]}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(1.56, toon={'bend': {'neck': [0.0, 0.0, 0.22, 1, None]}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1)])],
        props=[MJ('pull18', False, turn={'at': T18, 'dur': TD18}, tagKick=[r(POP18 + 0.35), r(POP18 + 0.7)])],
        cams=[FC(0.0, [2.5, 2.0, 0.45], [[ME1[0], 3.0, ME1[2]], [ME1[0], 1.2, ME1[2]], LBL(ME1, -60, 1, 0.6, 2.0), [r(ME1[0] + 0.3), 2.2, r(ME1[2] - 0.2)]], top=0.12, bottom=0.76)])
st.cue('sfx:zip', 'S18', T18, 0.2); st.cue('pop', 'S18', POP18, 0.2)

# 19: for life. Close on him: deadpan, the label up beside his head, still wobbling; a look at us; a slow blink
D19 = st.dur('S19'); L19 = LBL(ME1, -60, 1, 0.6, 1.9)
st.shot('S19', 'parisStreet', setOpts=PARIS, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.12, toonEase='inOut'), k(0.55, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12, toonEase='inOut'),
            k(0.9, toon={'face': {**DEAD, 'mouth': 'line', 'gx': 0.7}}, toonDur=0.1), k(1.2, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1),   # his eyes go to the label, and back to us
            k(1.4, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08), k(1.54, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1)])],
        props=[MJ('pull19', tagSway=0.1, tagKick=[0.05, 0.95])],
        cams=[FC(0.0, [2.9, 2.1, 1.6], [[ME1[0], 2.6, ME1[2]], [ME1[0], 1.55, ME1[2]], [L19[0], 2.1, L19[2]], [r(ME1[0] - 0.3), 2.0, ME1[2]]], top=0.16, bottom=0.74)])

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
# (review 1) the jumpers' sleeves: each wearer's jacket in the colour of his jumper (and trousers of his own): the arms read as knitted sleeves
SL = lambda preset, col, seed, pants=None, **kw: {'preset': preset, 'seed': seed, 'suit': col, 'lapel': col, **({'pants': pants} if pants else {}), 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX, **kw}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'suit': '#C8322A', 'lapel': '#C8322A', 'pants': '#1F3550', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}
st.write("Le pull", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec', 'presentateur', 'president', 'juge', 'mod1'], extra_cast={
    'mec': MEC, 'mec_reflet': dict(MEC),
    'pass1': SL('madame', COLS[0], 761, build={'width': 0.92, 'headWidth': 1.25}),
    'pass2': SL('tourist', COLS[1], 762),
    'coll': SL('lemec_beige', '#2F62B5', 763, '#3A3D44'),
    **{f'emp{j + 1}': SL(['boss', 'femme', 'lemec_brown', 'madame', 'journaliste', 'femme'][j], COLS[j % len(COLS)], 764 + j, '#3A3D44' if j in (0, 2) else None) for j in range(6)},
    **{f'ville{j + 1}': SL(['madame', 'tourist', 'lemec_charcoal', 'femme', 'journaliste', 'gamin'][j], COLS[(j + 2) % len(COLS)], 771 + j, '#3A3D44' if j == 2 else None, **({'build': {'height': 0.62, 'width': 0.85, 'headScale': 1.15}} if j == 5 else {})) for j in range(6)},
    'coutu': {'preset': 'madame', 'seed': 778, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'presentateur': SL('journaliste', '#E8A33C', 779),
    'president': SL('politique', '#2F62B5', 780, '#4A4D55', tie='#9A1F2E', hairColor='#D2D2D2'),
    'mod1': SL('femme', '#C255C8', 781, build={'width': 0.85, 'headWidth': 1.2}),
    'mod2': SL('mecBeau', '#F2C94E', 782, '#2B2E3A', build={'width': 0.9, 'headWidth': 1.2}),
    **{f'photo{j + 1}': {'preset': 'journaliste', 'seed': 783 + j, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(4)},
    **{f'rue{j + 1}': SL(['femme', 'boss', 'madame', 'tourist', 'journaliste'][j], COLS[(j + 4) % len(COLS)], 788 + j, '#3A3D44' if j == 1 else None) for j in range(5)},
    'flic1': SL('cop', '#2F4A8A', 794),
    'flic2': SL('cop2', '#2F4A8A', 795),
    'juge': {'preset': 'judge', 'seed': 796, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
