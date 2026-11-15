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
JUMP = lambda pid, who, color='#C8322A', inside=True, w=0.66, flip=None: P(pid, 'knitJumper', on={'actor': who, 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'color': color, 'inside': inside, 'w': w, 'h': 0.62, 'd': 0.42, **({'flipAt': flip} if flip is not None else {})})   # (stills 1) wider and deeper: over the jacket, not a board on the chest
MJ = lambda pid, inside=True, flip=None: JUMP(pid, 'mec', '#C8322A', inside, 0.6, flip)   # his red jumper (his build is narrower)
TAG = lambda pid, keys=None: P(pid, 'slab', on={'actor': 'mec', 'joint': 'torso', 'offset': [-0.18, 0.63, -0.17]}, rot=[-0.25, 0, 0.75], opts={'w': 0.18, 'h': 0.17, 'd': 0.006, 'color': '#FFFFFF', 'outline': 0.004}, **({'keys': keys} if keys else {}))   # (stills 2) the label sticking out of his collar, readable beside his head
COLS = ['#2F62B5', '#2F8F6B', '#E8A33C', '#8E5AA8', '#3A9BDC', '#E0813A', '#C255C8', '#5BB5A8']

for g_ in [('S02', 0.6, 'mec', 'label'), ('S05', 0.6, 'mec', 'office'), ('S13', 1.2, 'mec', 'reflection'), ('S14', 0.9, 'mec', 'flip'), ('S16', 1.2, 'mec', 'arrest'), ('S19', 0.5, 'mec', 'end')]:
    st.gag(*g_)
st.card('S07', 'DEHORS', at=0.5)
st.card('S12', "À L'ENVERS", at=0.5)
st.card('S16', 'INDÉCENT', at=0.8)

# 1: the hook. Out of his building door onto the street, a red knitted jumper over his suit, deadpan
D1 = st.dur('S01'); ME1 = [4.6, 0, 0.6]
st.shot('S01', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [6.6, 0, 0.6], -90, 'walk', 'neutral', keys=[k(0.0, to=ME1, dur=r(D1 - 0.2), clip='walk', then='stand', ease='out'), k(0.0, look=[0.0, 1.8, 0.6]), k(r(D1 - 0.3), look='camera')])],
        props=[MJ('pull1')],
        cams=[FC(0.0, [2.6, 1.5, 3.2], [[ME1[0], 2.45, ME1[2]], [ME1[0], 0.0, ME1[2]], [6.6, 2.45, 0.6], [6.6, 0.0, 0.6]], top=0.14, bottom=0.78)])
st.cue('sfx:stepSoft', 'S01', 0.3, 0.15); st.cue('sfx:stepSoft', 'S01', 0.7, 0.15)

# 2: ...inside out. Close from behind his shoulder: the white care label sticking up out of the collar, the pale seams outside
D2 = st.dur('S02')
st.shot('S02', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', ME1, -90, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 0.6]), k(0.6, toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.2)])],
        props=[MJ('pull2'), BURST('etiq2', [r(ME1[0] + 0.25), 2.25, 1.0], 0.35, "L'ÉTIQUETTE !", 0.5, 0.4)],
        cams=[FC(0.0, [5.8, 2.0, 1.5], [[ME1[0], 2.45, ME1[2]], [ME1[0], 1.45, ME1[2]], [r(ME1[0] + 0.15), 1.95, r(ME1[2] - 0.2)], [r(ME1[0] + 0.15), 1.95, r(ME1[2] + 0.3)]], top=0.18, bottom=0.74)])
st.cue('sfx:sting', 'S02', 0.35, 0.15)

# 3: nobody dared tell him. On the pavement: two passers-by stare at the label as he walks past, open their mouths, then look away whistling
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [6.2, 0, -1.2], 0, 'walk', 'neutral', keys=[k(0.0, to=[6.2, 0, 0.9], dur=D3, clip='walk', ease='linear'), k(0.0, look='camera')]),
        *[act(pid, [px, 0, pz], pry, 'stand', 'neutral', keys=[k(0.0, look=[6.2, 2.2, -0.6]), k(0.3, look=[6.2, 2.2, 0.4]), k(0.3, toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.08, toonEase='out'),
            k(r(0.8 + 0.12 * j), look=[r(px + 1.0), 3.4, r(pz - 2.5)], lookDur=0.15), k(r(0.8 + 0.12 * j), toon={'face': {'lid': 0.4, 'mouth': 'whistle', 'brow': 0.4}}, toonDur=0.12)]) for j, (pid, px, pz, pry) in enumerate([('pass1', 5.0, -0.5, 90), ('pass2', 7.3, 0.2, -110)])]],
        props=[MJ('pull3'), *[JUMP(f'pj3{j}', pid, COLS[j], inside=False) for j, pid in enumerate(['pass1', 'pass2'])]],
        cams=[FC(0.0, [5.0, 1.55, 4.6], [[6.2, 2.45, -1.2], [6.2, 2.45, 0.9], [6.2, 0.0, 0.9], [5.0, 2.4, -0.5], [7.3, 2.4, 0.2], [6.2, 0.0, -1.2]], top=0.14, bottom=0.76)])
st.cue('sfx:whistle', 'S03', 0.8, 0.2)

# 4: the next day his colleague did the same. The office: the colleague comes in, his blue jumper inside out, label up; a nod between them
D4 = st.dur('S04')
st.shot('S04', 'office', actors=[act('mec', [-0.6, 0, -0.9], 30, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.5, look=[1.8, 1.9, 0.4]), k(0.95, look=[0.9, 1.9, 0.2]), k(1.4, toon={'sq': [1.0, 0.98, 1.0]}, toonDur=0.1)]),
        act('coll', [2.4, 0, 0.6], -110, 'walk', 'neutral', keys=[k(0.0, to=[0.8, 0, 0.0], dur=1.1, clip='walk', then='stand', ease='out'), k(0.0, look=[-0.6, 2.0, -0.9]), k(1.3, toon={'sq': [1.0, 0.97, 1.0], 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.1)])],
        props=[MJ('pull4'), JUMP('pj4', 'coll', '#2F62B5')],
        cams=[FC(0.0, [0.4, 1.6, 3.2], [[-0.6, 2.45, -0.9], [0.8, 2.45, 0.0], [2.4, 2.45, 0.6], [0.0, 0.2, -0.4]], top=0.14, bottom=0.78)])

# 5: then the whole office. Wide over the desks: every worker in a jumper inside out, labels up, typing
D5 = st.dur('S05'); W5 = [(-1.8, -1.6), (-0.6, -1.6), (0.6, -1.6), (1.8, -1.6), (-1.2, -0.4), (1.2, -0.4)]
st.shot('S05', 'office', setOpts={'printer': False}, actors=[act('mec', [0.0, 0, 0.6], 0, 'stand', 'neutral', keys=[k(0.0, look='camera')]),
        *[act(f'emp{j + 1}', [x, 0, z], 0, 'sitWrite', 'neutral', keys=[k(0.0, look=[x, 0.8, r(z + 0.4)]), k(r(0.4 + 0.2 * j), look='camera'), k(r(0.9 + 0.15 * j), look=[x, 0.8, r(z + 0.4)])]) for j, (x, z) in enumerate(W5)]],
        props=[MJ('pull5'), *[JUMP(f'pj5{j}', f'emp{j + 1}', COLS[j % len(COLS)]) for j in range(len(W5))], *[P(f'ch5{j}', 'chair', pos=[x, 0, z]) for j, (x, z) in enumerate(W5)],
               *[P(f'dk5{j}', 'desk', pos=[x, 0, r(z + 0.55)], opts={'w': 0.9}) for j, (x, z) in enumerate(W5)]],
        cams=[FC(0.0, [0.0, 2.6, 3.2], [[-1.8, 2.0, -1.6], [1.8, 2.0, -1.6], [0.0, 2.45, 0.6], [0.0, 0.3, 0.6]], top=0.14, bottom=0.78)])

# 6: then the whole town. A street: everyone walking by in jumpers inside out, labels up; him in the middle
D6 = st.dur('S06'); CROWD6 = [(3.4, -0.4, 180), (5.6, -0.9, 180), (3.0, -2.2, 0), (5.9, -2.6, 180), (4.1, -3.6, 180), (6.3, 0.2, 180)]
st.shot('S06', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [4.6, 0, -1.8], 0, 'walk', 'neutral', keys=[k(0.0, to=[4.6, 0, -0.2], dur=D6, clip='walk', ease='linear'), k(0.0, look='camera')]),
        *[act(f'ville{j + 1}', [x, 0, z], ry, 'walk', 'neutral', keys=[k(0.0, to=[x, 0, r(z + (1.6 if ry == 0 else -1.6))], dur=D6, clip='walk', ease='linear')]) for j, (x, z, ry) in enumerate(CROWD6)]],
        props=[MJ('pull6'), *[JUMP(f'pj6{j}', f'ville{j + 1}', COLS[(j + 2) % len(COLS)]) for j in range(len(CROWD6))]],
        cams=[FC(0.0, [4.4, 3.0, 8.6], [[4.6, 2.45, -1.8], [4.6, 0.0, -0.2], [3.4, 2.4, -0.4], [5.6, 2.4, -0.9]], top=0.16, bottom=0.76, lenses=range(16, 40))])   # long lens: the crowd packs up behind him

# 7: the shops sewed their labels on the outside. A clothes shop: the seamstress sews a big label on the outside of a jumper; a pile of jumpers,
#    labels out, on the table (DEHORS)
D7 = st.dur('S07')
st.shot('S07', 'poste', setOpts={'title': 'PRÊT-À-PORTER', 'guichets': False}, actors=[act('coutu', [0.0, 0, -1.9], 0, 'stand', 'happy', keys=[k(0.0, look=[0.1, 1.3, -1.45]),
            *[k(r(0.1 + 0.22 * j), toon={'reach': {'R': [r(0.15 + (0.08 if j % 2 else -0.04)), r(1.35 + (0.1 if j % 2 else 0.0)), -1.45, 1, 0.04], 'L': [-0.1, 1.3, -1.45, 1, 0.04]}, 'hands': {'R': 'pinch', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.12) for j in range(9)]])],
        props=[P('pull7', 'knitJumper', pos=[0.05, 1.12, -1.45], scale=0.8, opts={'color': '#2F8F6B', 'inside': True}), P('tas7', 'jumperPile', pos=[1.4, 0, -1.6]),
               P('fil7', 'slab', on={'actor': 'coutu', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, opts={'w': 0.006, 'h': 0.12, 'd': 0.006, 'color': '#C9CDD2'})],
        cams=[FC(0.0, [0.6, 1.6, 0.6], [[0.0, 2.45, -1.9], [0.05, 1.12, -1.45], [1.4, 1.0, -1.6], [-0.3, 1.0, -1.6]], top=0.2, bottom=0.76)])

# 8: the news presenter... The news desk: the presenter reads the news, a big JOURNAL backdrop
D8 = st.dur('S08'); PRES = [0.0, 0, 0.3]; NEWS = {'backdrop': 'LE JOURNAL', 'fontScale': 0.6, 'podium': False, 'chairs': False, 'flags': False, 'bg': '#5878A8', 'wall': '#4C6A96'}
st.shot('S08', 'pressRoom', setOpts=NEWS, actors=[act('presentateur', PRES, 0, 'sitTalk', 'neutral', keys=[k(0.0, look='camera'), k(0.9, look=[0.25, 0.8, 0.85], lookDur=0.15), k(1.25, look='camera', lookDur=0.15)])],
        props=[P('desk8', 'desk', pos=[0.0, 0, 0.85], opts={'w': 1.6}), P('ch8', 'chair', pos=PRES), JUMP('pj8', 'presentateur', '#E8A33C'), P('feuille8', 'paperSheet', pos=[0.25, 0.77, 0.9], rot=[-PI / 2, 0, 0], opts={'w': 0.25, 'h': 0.32, 'lines': ['INFOS']})],
        cams=[FC(0.0, [0.3, 1.5, 3.4], [[0.0, 2.2, 0.3], [0.0, 0.8, 0.75], [-0.75, 1.2, 0.75], [0.75, 1.2, 0.75], [0.0, 2.6, -3.0]], top=0.14, bottom=0.76)])

# 9: ...wore it live. From behind, low: the label up out of his collar, the red EN DIRECT light on the camera in front of him
D9 = st.dur('S09')
st.shot('S09', 'pressRoom', setOpts=NEWS, actors=[act('presentateur', PRES, 0, 'sitTalk', 'neutral', keys=[k(0.0, look=[0.3, 1.6, 2.6]), k(0.7, toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.15)])],
        props=[P('desk9', 'desk', pos=[0.0, 0, 0.85], opts={'w': 1.6}), P('ch9', 'chair', pos=PRES), JUMP('pj9', 'presentateur', '#E8A33C'), P('tv9', 'tvCamera', pos=[0.3, 0, 2.6], ry=180),
               P('direct9', 'signBoard', pos=[0.3, 1.95, 2.55], ry=180, opts={'text': 'EN DIRECT', 'bg': '#D22B2B', 'fg': '#FFFFFF', 'w': 0.6, 'h': 0.16, 'posts': False, 'height': 0})],
        cams=[FC(0.0, [-0.6, 1.95, -1.4], [[0.0, 2.25, 0.3], [0.0, 1.3, 0.3], [0.3, 2.1, 2.55], [0.3, 0.9, 2.6]], top=0.16, bottom=0.76, inside=(-5.0, 5.0, 0.5, 3.0, -2.8, 6.0))])

# 10: the president gave his wishes... At the lectern between two flags, the president, solemn
D10 = st.dur('S10'); PR10 = [0.0, 0, -0.3]
st.shot('S10', 'pressRoom', setOpts={'backdrop': 'PRÉSIDENCE', 'fontScale': 0.6, 'podium': False, 'bg': '#5878A8', 'wall': '#4C6A96'}, actors=[act('president', PR10, 0, 'podiumTalk', 'neutral', keys=[k(0.0, look='camera')])],
        props=[P('pod10', 'podium', pos=[0.0, 0, 0.2], opts={'text': 'RÉPUBLIQUE'}), JUMP('pj10', 'president', '#2F62B5'), *[P(f'fl10{j}', 'flag', pos=[r(-1.0 + 2.0 * j), 0, -0.9], opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A'], 'vertical': True}) for j in range(2)]],
        cams=[FC(0.0, [0.2, 1.6, 2.6], [[0.0, 2.5, PR10[2]], [0.0, 1.0, 0.2], [-1.0, 2.4, -0.9], [1.0, 2.4, -0.9]], top=0.16, bottom=0.78)])

# 11: ...in a jumper inside out. Close on him: the label sticking up behind his solemn face, the seams on his shoulders
D11 = st.dur('S11')
st.shot('S11', 'pressRoom', setOpts={'backdrop': 'PRÉSIDENCE', 'fontScale': 0.6, 'podium': False, 'bg': '#5878A8', 'wall': '#4C6A96'}, actors=[act('president', PR10, 0, 'podiumTalk', 'neutral', keys=[k(0.0, look='camera'), k(0.8, toon={'face': {'lid': 1.0}}, toonDur=0.07), k(0.92, toon={'face': {'lid': 0.2}}, toonDur=0.08)])],
        props=[P('pod11', 'podium', pos=[0.0, 0, 0.2], opts={'text': 'RÉPUBLIQUE'}), JUMP('pj11', 'president', '#2F62B5')],
        cams=[FC(0.0, [0.55, 2.15, 1.2], [[0.0, 2.55, PR10[2]], [0.0, 1.65, PR10[2]], [0.3, 2.1, r(PR10[2] - 0.2)], [-0.35, 2.0, PR10[2]]], top=0.16, bottom=0.74)])

# 12: the fashion shows went inside out. A catwalk: models stride toward us in jumpers inside out with giant labels; flashes on both sides (À L'ENVERS)
D12 = st.dur('S12')
st.shot('S12', 'pressRoom', setOpts={'backdrop': 'PARIS', 'fontScale': 0.9, 'podium': False, 'chairs': False, 'bg': '#2B2E3A', 'wall': '#23252E'}, actors=[
        *[act(mid, [mx, 0, mz], 0, 'strut', 'smug', keys=[k(0.0, to=[mx, 0, r(mz + 1.3)], dur=D12, clip='strut', ease='linear'), k(0.0, look='camera')]) for mid, mx, mz in [('mod1', 0.0, -0.9), ('mod2', 0.0, -2.6)]],
        *[act(f'photo{j + 1}', [r(-1.3 if j % 2 else 1.3), 0, r(-0.4 + 0.8 * (j // 2))], 90 if j % 2 else -90, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.8, 0.0]), k(0.0, toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            *[k(r(fa), toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 0.97, 1.0]}, toonDur=0.06) for fa in [0.2 + 0.3 * j, 0.9 + 0.25 * j]],
            *[k(r(fa + 0.12), toon={'touch': {'R': ['face', -0.05, 0.22, 0.2, 1, 0.02], 'L': ['face', 0.05, 0.2, 0.2, 1, 0.02]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.15) for fa in [0.2 + 0.3 * j, 0.9 + 0.25 * j]],
            k(r(1.5 + 0.1 * j), look=[0.0, 1.8, 0.6], lookDur=0.3)]) for j in range(4)]],
        props=[P('podium12', 'floorSlab', pos=[0.0, 0.04, -1.0], opts={'w': 1.2, 'd': 6.0, 'h': 0.08, 'color': '#F4F1E8'}), JUMP('pj12a', 'mod1', '#C255C8'), JUMP('pj12b', 'mod2', '#F2C94E'),
               *[P(f'cam12{j}', 'pressCamera', on={'actor': f'photo{j + 1}', 'hand': 'R', 'offset': [0.06, 0.0, 0.08]}, opts={'flashAt': [r(0.2 + 0.3 * j), r(0.9 + 0.25 * j)], 'burst': 0.5}) for j in range(4)]],
        cams=[FC(0.0, [0.0, 1.7, 3.6], [[0.0, 2.45, -0.9], [0.0, 2.45, 0.4], [0.0, 0.0, 0.4], [-1.3, 2.4, 0.4], [1.3, 2.4, 0.4], [0.0, 0.0, -2.6]], top=0.14, bottom=0.76)])
st.cue('sfx:click', 'S12', 0.2, 0.15); st.cue('sfx:click', 'S12', 0.5, 0.15); st.cue('sfx:click', 'S12', 0.8, 0.15); st.cue('sfx:click', 'S12', 1.1, 0.15)

# 13: yesterday he saw himself in a shop window. On the pavement, at a big shop window: his reflection looks back at him, then taps its own label;
#     he looks down at his collar
D13 = st.dur('S13'); ZW = -1.0; ME13 = [0.4, 0, -0.1]
SRC13 = act('mec', ME13, 180, 'stand', 'neutral', keys=[k(0.0, look=[0.4, 2.0, -2.0]), k(0.8, toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.2), k(1.1, toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.25), k(r(D13 - 0.7), look=[0.55, 1.95, 0.05]), k(r(D13 - 0.6), toon={'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'gy': 0.5}}, toonDur=0.1)])
REF13 = reflection(SRC13, zm=ZW, shift=0.0, id='mec_reflet')
REF13['keys'] = REF13['keys'] + [k(0.55, toon={'touch': {'L': ['torso', -0.12, 0.62, -0.12, 1, 0.02]}, 'hands': {'L': 'point'}, 'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.15), k(1.1, toon={'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.2)]   # the reflection points at its label
st.shot('S13', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[SRC13, REF13],
        props=[MJ('pull13'), P('pullref13', 'knitJumper', on={'actor': 'mec_reflet', 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'color': '#C8322A', 'inside': True, 'w': 0.6, 'h': 0.62, 'd': 0.42}),
               P('vitre13', 'slab', pos=[0.4, 1.5, ZW], opts={'w': 2.6, 'h': 2.8, 'd': 0.02, 'color': '#CFE6F2', 'opacity': 0.25}), P('cadre13', 'slab', pos=[0.4, 3.0, ZW], opts={'w': 2.8, 'h': 0.25, 'd': 0.1, 'color': '#2E4563'})],
        cams=[FC(0.0, [1.8, 1.85, 1.4], [[0.4, 2.45, -0.1], [0.4, 1.3, -0.1], [0.4, 2.45, -1.9], [0.4, 1.3, -1.9]], top=0.14, bottom=0.76)])
st.cue('sfx:click', 'S13', 0.6, 0.15)

# 14: he turned his jumper right side out. He tugs it over his head and back: it flips right side out with a squash; he smooths it down, pleased
D14 = st.dur('S14'); FLIP14 = 0.75
st.shot('S14', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.2, toon={'reach': {'R': [r(ME1[0] - 0.1), 2.6, 0.75, 1, 0.04], 'L': [r(ME1[0] - 0.1), 2.6, 0.45, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'clench'}}, toonDur=0.2, toonEase='out'),
            k(FLIP14, toon={'touch': {'R': ['torso', -0.12, 0.3, 0.2, 1, 0.02], 'L': ['torso', 0.12, 0.3, 0.2, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.12, toonEase='out'),
            k(r(FLIP14 + 0.35), toon={'touch': {'R': ['torso', -0.12, 0.15, 0.2, 1, 0.02], 'L': ['torso', 0.12, 0.15, 0.2, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'smile'}}, toonDur=0.25)])],
        props=[MJ('pull14', True, FLIP14)],
        cams=[FC(0.0, [2.6, 1.7, 2.6], [[ME1[0], 2.75, ME1[2]], [ME1[0], 0.9, ME1[2]], [r(ME1[0] - 0.4), 2.2, ME1[2]], [r(ME1[0] + 0.4), 2.2, ME1[2]]], top=0.14, bottom=0.76)])
st.cue('sfx:zip', 'S14', 0.3, 0.2); st.cue('pop', 'S14', FLIP14, 0.25)

# 15: the whole street turned round. Everyone on the pavement, labels up, turns to stare at him; a woman drops her bag; gasps
D15 = st.dur('S15'); FW = (-0.866, 0.5); LW = (0.5, 0.866)   # his facing (ry -60) and his left, on the ground
ST15 = [(r(ME1[0] - FW[0] * t + LW[0] * l, 2), r(ME1[2] - FW[1] * t + LW[1] * l, 2)) for t, l in [(1.6, -1.5), (1.2, 1.2), (2.7, -0.95), (2.4, 2.3), (3.4, 1.0)]]
st.shot('S15', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.6, look=[3.0, 1.9, 0.2])]),
        *[act(f'rue{j + 1}', [x, 0, z], 180 if j % 2 else 0, 'stand', 'neutral', keys=[k(0.0, look=[x, 1.8, r(z + (-3 if j % 2 else 3))]), k(r(0.15 + 0.08 * j), turn=r(math.degrees(math.atan2(ME1[0] - x, ME1[2] - z)))), k(r(0.2 + 0.08 * j), look=[ME1[0], 1.8, ME1[2]]),
            k(r(0.25 + 0.08 * j), toon={'face': {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.08, toonEase='out')]) for j, (x, z) in enumerate(ST15)]],
        props=[MJ('pull15', False), *[JUMP(f'pj15{j}', f'rue{j + 1}', COLS[(j + 4) % len(COLS)]) for j in range(len(ST15))]],
        cams=[FC(0.0, [r(ME1[0] + FW[0] * 3.6), 1.6, r(ME1[2] + FW[1] * 3.6)], [[ME1[0], 2.45, ME1[2]], [ME1[0], 0.0, ME1[2]], *[[x, 2.4, z] for x, z in ST15]], top=0.14, bottom=0.76)])
st.cue('sfx:gasp', 'S15', 0.3, 0.3)

# 16: the police arrested him for indecent dress. Two policemen in jumpers inside out grab him; one covers his own eyes; handcuffs (INDÉCENT)
D16 = st.dur('S16')
F1 = [r(ME1[0] - FW[0] * 0.45 - LW[0] * 0.75), 0, r(ME1[2] - FW[1] * 0.45 - LW[1] * 0.75)]; F2 = [r(ME1[0] - FW[0] * 0.5 + LW[0] * 0.62), 0, r(ME1[2] - FW[1] * 0.5 + LW[1] * 0.62)]   # (stills 2) flic1 further to his right: leaning in, his head no longer covers the man's face
EYES = {'touch': {'R': ['face', 0.0, 0.12, 0.22, 1, 0.02]}, 'hands': {'R': 'open'}}
st.shot('S16', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.5, toon={'sq': [0.98, 1.02, 0.98], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1),
            k(1.0, look=[F1[0], 1.4, F1[2]], lookDur=0.2), k(1.6, look='camera'), k(1.9, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.1), k(2.05, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12)]),
        act('flic1', F1, -4, 'cuffOther', 'determined', keys=[k(0.0, look=[ME1[0], 1.3, ME1[2]])]),
        act('flic2', F2, -80, 'stand', 'neutral', keys=[k(0.0, look=[ME1[0], 1.6, ME1[2]]), k(0.3, toon={**EYES, 'face': {'lid': 1.0, 'mouth': 'O'}}, toonDur=0.12),
            k(1.2, toon={**EYES, 'face': {'lid': 0.3, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.08), k(1.25, look=[ME1[0], 1.3, ME1[2]], lookDur=0.1), k(1.6, toon={**EYES, 'face': {'lid': 1.0, 'mouth': 'O'}, 'sq': [0.97, 1.03, 0.97]}, toonDur=0.08)])],   # covering his eyes, one peek
        props=[MJ('pull16', False), JUMP('pj16a', 'flic1', '#2F4A8A'), JUMP('pj16b', 'flic2', '#2F4A8A'), P('menottes16', 'tapeRoll', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.0, 0.0]}, scale=0.7)],
        cams=[FC(0.0, [2.2, 1.0, 1.0], [[ME1[0], 2.6, ME1[2]], [ME1[0], 1.0, ME1[2]], [F1[0], 2.5, F1[2]], [F2[0], 2.5, F2[2]]], top=0.2, bottom=0.76)])
st.cue('sfx:click', 'S16', 0.6, 0.3); st.cue('sfx:whistle', 'S16', 0.2, 0.2)

# 17: he was sentenced... The courtroom: the judge, a label sticking up out of his robe, brings the gavel down
D17 = st.dur('S17'); BANG17 = 0.7
st.shot('S17', 'courtroom', actors=[act('juge', [0.0, 0.3, -4.0], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [0.4, 2.6, -3.4, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'brow': -0.5}}, toonDur=0.0),
            k(BANG17, toon={'reach': {'R': [0.4, 1.5, -3.3, 1, 0.03]}, 'hands': {'R': 'grip'}, 'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.0, 'brow': -0.7, 'mouth': 'open'}}, toonDur=0.05, toonEase='in')])],
        props=[P('gav17', 'gavel', on={'actor': 'juge', 'hand': 'R', 'offset': [0.0, -0.02, 0.05]}), P('etiq17', 'slab', on={'actor': 'juge', 'joint': 'torso', 'offset': [0.0, 0.68, -0.14]}, rot=[-0.35, 0, 0], opts={'w': 0.12, 'h': 0.1, 'd': 0.005, 'color': '#FFFFFF'})],
        cams=[FC(0.0, [1.0, 2.3, -0.8], [[0.0, 2.85, -4.0], [0.0, 1.7, -4.0], [0.6, 2.7, -3.4], [-0.6, 2.7, -3.4], [-1.25, 3.25, -5.1], [1.25, 3.25, -5.1]], top=0.14, bottom=0.76)])   # (stills 2) the whole TRIBUNAL sign in frame
st.cue('clang', 'S17', BANG17, 0.4)

# 18: ...to wear his jumper inside out. On the pavement he pulls it back on inside out: the label pops back up out of the collar
D18 = st.dur('S18'); FLIP18 = 0.8
st.shot('S18', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look=[r(ME1[0] - 0.45), 1.1, r(ME1[2] + 0.25)]),
            k(0.2, toon={'reach': {'R': [r(ME1[0] - 0.1), 2.6, 0.75, 1, 0.04], 'L': [r(ME1[0] - 0.1), 2.6, 0.45, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.2, toonEase='out'),
            k(FLIP18, toon={'touch': {'R': ['torso', -0.12, 0.3, 0.2, 1, 0.02], 'L': ['torso', 0.12, 0.3, 0.2, 1, 0.02]}, 'hands': {'R': 'open', 'L': 'open'}, 'sq': [1.04, 0.96, 1.04], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12, toonEase='out')])],
        props=[P('pull18', 'knitJumper', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'color': '#C8322A', 'inside': False, 'w': 0.6, 'h': 0.62, 'd': 0.42}, keys=[k(FLIP18, visible=False)]), MJ('pull18b'), TAG('etiq18', [k(0.0, visible=False), k(FLIP18, visible=True, scale=0.2), k(r(FLIP18 + 0.1), scale=1.2), k(r(FLIP18 + 0.2), scale=1.0)]),
               P('pull18bv', 'slab', pos=[0, -9, 0], opts={'w': 0.01, 'h': 0.01, 'd': 0.01})],
        cams=[FC(0.0, [2.4, 2.15, 0.35], [[ME1[0], 2.75, ME1[2]], [ME1[0], 1.25, ME1[2]], [r(ME1[0] - 0.35), 2.2, r(ME1[2] + 0.2)], [r(ME1[0] + 0.3), 2.2, r(ME1[2] - 0.2)]], top=0.16, bottom=0.74)])
st.cue('sfx:zip', 'S18', 0.3, 0.2); st.cue('pop', 'S18', FLIP18, 0.2)

# 19: for life. Close on him: deadpan, the label up behind his head; a look at us; a slow blink
D19 = st.dur('S19')
st.shot('S19', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', ME1, -60, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0),
            k(0.35, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.12, toonEase='inOut'), k(0.55, toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.12, toonEase='inOut')])],
        props=[MJ('pull19'), TAG('etiq19')],
        cams=[FC(0.0, [2.9, 2.1, 1.6], [[ME1[0], 2.6, ME1[2]], [ME1[0], 1.6, ME1[2]], [r(ME1[0] + 0.15), 2.05, r(ME1[2] - 0.2)], [r(ME1[0] - 0.3), 2.0, ME1[2]]], top=0.16, bottom=0.74)])

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le pull", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'mec_reflet': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'pass1': {'preset': 'madame', 'seed': 761, 'suit': '#C255C8', 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    'pass2': {'preset': 'tourist', 'seed': 762, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'coll': {'preset': 'avocat', 'seed': 763, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'emp{j + 1}': {'preset': ['boss', 'femme', 'avocat', 'madame', 'journaliste', 'femme'][j], 'seed': 764 + j, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(6)},
    **{f'ville{j + 1}': {'preset': ['madame', 'tourist', 'avocat', 'femme', 'journaliste', 'gamin'][j], 'seed': 771 + j, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(6)},
    'coutu': {'preset': 'madame', 'seed': 778, 'suit': '#8E6CC4', 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
    'presentateur': {'preset': 'journaliste', 'seed': 779, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 780, 'suit': '#4A4D55', 'lapel': '#4A4D55', 'tie': '#9A1F2E', 'hairColor': '#D2D2D2', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'mod1': {'preset': 'femme', 'seed': 781, 'suit': '#2B2E3A', 'build': {'width': 0.85, 'headWidth': 1.2}, 'toon': EX},
    'mod2': {'preset': 'mecBeau', 'seed': 782, 'build': {'width': 0.9, 'headWidth': 1.2}, 'toon': EX},
    **{f'photo{j + 1}': {'preset': 'journaliste', 'seed': 783 + j, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(4)},
    **{f'rue{j + 1}': {'preset': ['femme', 'boss', 'madame', 'tourist', 'journaliste'][j], 'seed': 788 + j, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(5)},
    'flic1': {'preset': 'cop', 'seed': 794, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic2': {'preset': 'cop2', 'seed': 795, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'juge': {'preset': 'judge', 'seed': 796, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
