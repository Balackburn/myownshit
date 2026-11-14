#!/usr/bin/env python3
"""L'écho (story 60, cycle 22 of the cartoon staging): this man shouted in the mountains. The echo never came back. He filed a complaint. The
gendarmerie put out a missing notice. It was reported in three valleys. Yesterday the echo came home. Two years late. It shouted for three days. The
gendarmerie fined the man for the noise.
Staging: on a rocky summit he cups his hands round his mouth, fills his chest and shouts: his jaw stretches down, his own shout blows his hair and tie
forward, and big cut-out letters « OHÉ ! » burst out of his mouth and fly off over the valley; he waits with a hand cupped behind his ear, his ears
flapped out, leaning: crickets. At the gendarmerie he mimes his shout to a gendarme who takes it down; the gendarme slaps a missing notice (a speech
bubble « OHÉ ! ») on the wall; the notices are everywhere in town; a hiker and a farmer in two valleys point at the letters crossing their skies.
Yesterday, in his street, the letters come back down it, growing huge: his eyes go out on stalks; SPLAT, he is flattened on the pavement like a
sheet of paper, then peels himself up stiff as a board and pops back to his shape. At night the giant letters rattle between the buildings, people
holding their ears; by day he has rings under his eyes and holds his ears. The gendarme slaps a fine on his forehead; close on him, the ticket on his
forehead, a tiny « ohé » drifts down; a slow blink.
Natural look; cycle 22 tools: props_echo.js (shoutLetters, mountainRange, missingPoster, fineTicket, summitRock)."""
from story_kit import *
import math

st = Story('echo', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L04', 5), ('S06', 'L05', 0), ('S07', 'L05', 4),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L08', 3), ('S12', 'L09', 0), ('S13', 'L09', 4)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)

DEAD = {'lid': 0.45}
BURST = lambda pid, pos, at_, text, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
ALPS = {'grass': '#8DB86A', 'clouds': 28}
TOP = 3.0                                                                  # the summit's flat, 3 m over the field
ME_S = [0.0, TOP, 0.2]                                                     # him on the summit, facing the valley (-Z)
RING = lambda sid: [P(f'mtnN{sid}', 'mountainRange', pos=[0, 0, -62], opts={'n': 9, 'w': 150, 'h': 36, 'd': 22, 'seed': 7}),
                    P(f'mtnW{sid}', 'mountainRange', pos=[-62, 0, 0], ry=90, opts={'n': 8, 'w': 150, 'h': 30, 'd': 22, 'seed': 13}),
                    P(f'mtnE{sid}', 'mountainRange', pos=[62, 0, 0], ry=-90, opts={'n': 8, 'w': 150, 'h': 32, 'd': 22, 'seed': 19}),
                    P(f'mtnS{sid}', 'mountainRange', pos=[0, 0, 62], ry=180, opts={'n': 9, 'w': 150, 'h': 28, 'd': 22, 'seed': 23})]
SUMMIT = lambda sid: P(f'rock{sid}', 'summitRock', pos=[0, TOP, 0], opts={'r': 1.6, 'alt': '2 040 m'})
CUP = lambda k_: {'touch': {'L': ['face', 0.34, 0.24, r(0.05 + 0.04 * k_), 1, 0.03, [1.0, 0.2, 0.0]], 'R': ['face', -0.34, 0.24, r(0.05 + 0.04 * k_), 1, 0.03, [-1.0, 0.2, 0.0]]}, 'hands': {'L': 'open', 'R': 'open'}}
MOUTH_S = [ME_S[0], r(ME_S[1] + 1.72), r(ME_S[2] - 0.25)]

# 1: the hook. On a rocky summit (SOMMET 2 040 m) with mountains all round: he cups his hands round his mouth, fills his chest (cheeks puffed), and
#    SHOUTS: his jaw stretches down, his own shout blows his hair and tie forward, and the letters « OHÉ ! » burst out of his mouth and fly off over
#    the valley, shrinking
D1 = st.dur('S01'); SH1 = 0.5
st.shot('S01', 'grassland', setOpts=ALPS, actors=[
        act('mec', ME_S, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[0.0, r(TOP + 1.7), -10.0]), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.06, toon={**CUP(0.0), 'sq': [0.95, 1.07, 0.95], 'bend': {'spine': [-0.22, 0, 0, 1, None]}, 'face': {'lid': 0.6, 'puff': 1.0, 'cheeks': 1.0, 'brow': 0.3}}, toonDur=0.3, toonEase='inOut'),   # hands up, a big breath...
            k(SH1, toon={**CUP(1.0), 'sq': [1.04, 0.97, 1.04], 'bend': {'spine': [0.28, 0, 0, 1, None]}, 'wind': [0.0, 1.0, 14.0], 'hairUp': 0.6,
                          'face': {'lid': 1.0, 'brow': -0.8, 'jaw': 0.95, 'jawLen': 0.65, 'mouth': 'scream', 'tongue': 0.3}}, toonDur=0.06, toonEase='out'),   # ...SHOUT: the jaw stretched down, blown by his own shout
            *[k(r(SH1 + 0.1 + 0.06 * i), toon={**CUP(1.0), 'sq': ([1.05, 0.96, 1.05] if i % 2 else [1.02, 0.99, 1.02]), 'bend': {'spine': [0.28, 0, 0, 1, None]}, 'wind': [0.0, 1.0, 14.0], 'hairUp': 0.6,
                                              'face': {'lid': 1.0, 'brow': -0.8, 'jaw': (1.0 if i % 2 else 0.9), 'jawLen': 0.65, 'mouth': 'scream', 'tongue': 0.3}}, toonDur=0.05) for i in range(14)]])],   # ...held, quivering
        props=[*RING('1'), SUMMIT('1'),
               P('ohe1', 'shoutLetters', pos=[0, 0, 0], face='camera', opts={'text': 'OHÉ !', 'size': 0.45, 'show': [SH1, 99.0],
                 'path': [[SH1] + MOUTH_S, [r(SH1 + 0.3), -0.3, r(TOP + 2.1), -2.6], [r(SH1 + 0.7), -1.4, r(TOP + 3.0), -9.0], [D1, -3.5, r(TOP + 4.5), -26.0]],
                 'grow': [[SH1, 0.3], [r(SH1 + 0.15), 1.4], [r(SH1 + 0.35), 1.25], [D1, 2.2]]}),   # out of his mouth, big, then off over the valley
               P('spd1', 'speedLines', pos=[0, 0, 0], face='camera', opts={'n': 6, 'len': 0.9, 'w': 0.5, 'angle': 0.35, 'at': [[SH1, r(SH1 + 0.6)]], 'path': [[SH1] + MOUTH_S, [r(SH1 + 0.3), 0.2, r(TOP + 1.95), -1.6], [r(SH1 + 0.6), -0.6, r(TOP + 2.6), -5.0]]})],   # (cycle 22) speed lines behind it
        cams=[FC(0.0, [1.7, r(TOP + 1.55), -1.5], [[ME_S[0], r(TOP + 2.35), ME_S[2]], [ME_S[0], r(TOP + 0.9), ME_S[2]], [-0.3, r(TOP + 2.6), -2.6], [ME_S[0], r(TOP - 0.2), r(ME_S[2] + 0.8)]],
                 top=0.16, bottom=0.7, drift=(0.08, 0.0, 0.1))])
st.cue('sfx:gasp', 'S01', 0.08, 0.3); st.cue('whoosh', 'S01', SH1, 0.4, 1.1, 200, 900); st.cue('gust', 'S01', SH1, 0.35, 1.2)

# 2: the echo never came back. Closer: a hand cupped behind his ear, his ears flapped out, leaning toward the valley, his eyes up and aside: nothing;
#    leaning further; crickets; a blink, the ears fold back
D2 = st.dur('S02')
EAR = lambda lean, ears, face: {'touch': {'R': ['head', -0.95, 0.62, 0.0, 1, 0.03, [-1.0, 0.5, 0.0]]}, 'hands': {'R': 'open'}, 'ears': ears, 'bend': {'spine': [lean, 0, r(0.4 * lean), 1, None], 'neck': [r(0.5 * lean), 0, 0, 1, None]}, 'face': face}
st.shot('S02', 'grassland', setOpts=ALPS, actors=[
        act('mec', ME_S, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[-3.0, r(TOP + 1.2), -12.0]), k(0.0, toon=EAR(0.15, 0.9, {'lid': 0.3, 'gx': -0.6, 'gy': -0.3}), toonDur=0.0),
            k(0.25, toon=EAR(0.3, 1.25, {'lid': 0.2, 'gx': -0.8, 'gy': -0.4, 'brow': 0.5, 'mouth': 'o'}), toonDur=0.3, toonEase='inOut'),   # leaning in, listening...
            k(0.75, toon=EAR(0.36, 1.35, {'lid': 0.25, 'gx': -0.6, 'gy': -0.2, 'brow': 0.6, 'mouth': 'o'}), toonDur=0.25, toonEase='inOut'),   # ...further...
            k(1.08, toon=EAR(0.3, 1.2, {'lid': 1.0}), toonDur=0.05), k(1.16, toon=EAR(0.2, 0.3, {'lid': 0.45, 'gx': 0.2}), toonDur=0.2, toonEase='inOut')])],   # ...nothing: a blink, the ears fold back
        props=[*RING('2'), SUMMIT('2')],
        cams=[FC(0.0, [1.4, r(TOP + 1.75), -0.9], [[ME_S[0], r(TOP + 2.35), ME_S[2]], [ME_S[0], r(TOP + 1.2), ME_S[2]], [-0.45, r(TOP + 1.9), ME_S[2]], [0.45, r(TOP + 1.9), ME_S[2]]], top=0.16, bottom=0.64, drift=(0.06, 0.0, 0.06))])
st.cue('sfx:crickets', 'S02', 0.6, 0.2)

# 3: he filed a complaint. At the gendarmerie desk he mimes his shout (hands round his mouth, jaw down) to the gendarme, who writes it down
D3 = st.dur('S03')
GEND = {'title': 'GENDARMERIE', 'plate': 'PLAINTES', 'map': False}
VIS = [0.0, 0, 0.1]; GDM = [0.3, 0, -1.45]
st.shot('S03', 'mairie', setOpts=GEND, actors=[
        act('mec', VIS, -129, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [GDM[0], 1.7, GDM[2]], 'cheat': 0.4}),   # (check) between her and us: at -150 his face was in profile k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.12, toon={**CUP(0.5), 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.5, 'puff': 0.8, 'cheeks': 0.8}}, toonDur=0.18, toonEase='inOut'),   # the mime: a breath...
            k(0.42, toon={**CUP(1.0), 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': {'lid': 1.0, 'jaw': 0.7, 'jawLen': 0.5, 'mouth': 'scream', 'brow': -0.6}}, toonDur=0.08, toonEase='out'),   # ...the silent shout...
            k(0.85, toon={'face': {'lid': 0.45, 'mouth': 'o', 'gx': 0.4}}, toonDur=0.15)]),   # ...and back, deadpan
        act('gendarme', GDM, -30, 'stand', 'neutral', keys=[k(0.0, look=[GDM[0], 0.85, r(GDM[2] + 0.45)]), k(0.0, toon={'reach': {'R': [r(GDM[0] - 0.05), 0.86, r(GDM[2] + 0.5), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'gy': 0.6}}, toonDur=0.0),
            *[k(r(0.1 + 0.12 * i), toon={'reach': {'R': [r(GDM[0] - 0.05 + (0.06 if i % 2 else -0.04)), 0.86, r(GDM[2] + 0.5), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'gy': 0.6}}, toonDur=0.1) for i in range(4)],   # writing...
            k(0.5, look=[VIS[0], 1.75, VIS[2]]), k(0.55, toon={'reach': {'R': [r(GDM[0] - 0.05), 0.86, r(GDM[2] + 0.5), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'brow': 0.7, 'gx': -0.3}}, toonDur=0.08),   # ...a look up at the shout...
            k(0.8, look=[GDM[0], 0.85, r(GDM[2] + 0.45)]), k(0.8, toon={'reach': {'R': [r(GDM[0] + 0.02), 0.86, r(GDM[2] + 0.5), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'gy': 0.6}}, toonDur=0.12)])],   # ...and on writing
        props=[P('form3', 'paperSheet', pos=[r(GDM[0] - 0.05), 0.832, r(GDM[2] + 0.48)], rot=[round(-PI / 2, 4), 0, 0.2], opts={'w': 0.3, 'h': 0.4, 'head': 'PLAINTE'})],
        cams=[FC(0.0, [-1.6, 1.65, -0.4], [[VIS[0], 2.35, VIS[2]], [VIS[0], 1.2, VIS[2]], [GDM[0], 2.25, GDM[2]], [GDM[0], 0.8, r(GDM[2] + 0.5)]], top=0.14, bottom=0.72, drift=(0.06, 0.0, -0.05))])
st.cue('sfx:paper', 'S03', 0.1, 0.15)

# 4: the gendarmerie put out a missing notice. The gendarme winds up and slaps the notice on the board: a speech bubble « OHÉ ! », AVIS DE RECHERCHE
D4 = st.dur('S04'); SLAP4 = 0.4
BOARD = [1.2, 1.55, -2.55]                                                 # on the back wall
GD4 = [0.75, 0, -1.9]
st.shot('S04', 'mairie', setOpts=GEND, actors=[
        act('gendarme', GD4, 40, 'stand', 'determined', keys=[k(0.0, look=[BOARD[0], BOARD[1], BOARD[2]]),
            k(0.0, toon={'reach': {'R': [r(GD4[0] + 0.1), 1.9, r(GD4[2] + 0.25), 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'brow': -0.5}}, toonDur=0.0),
            k(0.1, toon={'reach': {'R': [r(GD4[0] - 0.05), 2.05, r(GD4[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [-0.18, 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.6, 'brow': -0.7, 'mouth': 'clench'}}, toonDur=0.18, toonEase='inOut'),   # the wind-up...
            k(r(SLAP4 - 0.06), toon={'reach': {'R': [BOARD[0], BOARD[1], r(BOARD[2] + 0.06), 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.5, 'brow': -0.9, 'mouth': 'clench'}}, toonDur=0.06, toonEase='in'),   # ...SLAP
            k(r(SLAP4 + 0.3), toon={'reach': {'R': [r(GD4[0] + 0.15), 1.05, r(GD4[2] + 0.25), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'brow': 0.3, 'mouth': 'smirk'}}, toonDur=0.2, toonEase='inOut'),   # ...and a step back, pleased
            k(r(SLAP4 + 0.3), look='camera')])],
        props=[P('poster4', 'missingPoster', pos=BOARD, opts={'w': 0.62, 'h': 0.86}, keys=[k(0.0, scale=0.001, dur=0.0), k(SLAP4, scale=1.0, dur=0.12, ease='outBack')]),
               BURST('slap4', [r(BOARD[0] - 0.55), r(BOARD[1] + 0.5), r(BOARD[2] + 0.2)], SLAP4, 'PAF !', 0.42)],
        cams=[FC(0.0, [-0.5, 1.6, 1.2], [[GD4[0], 2.3, GD4[2]], [GD4[0], 0.9, GD4[2]], [r(BOARD[0] - 0.35), r(BOARD[1] + 0.48), BOARD[2]], [r(BOARD[0] + 0.35), r(BOARD[1] - 0.48), BOARD[2]]], top=0.12, bottom=0.72, drift=(0.06, 0.0, -0.08))])
st.cue('sfx:punch', 'S04', SLAP4, 0.4)

# 5: ...a missing notice. In town the notices are on every lamp post and tree trunk; a passer-by stops to read one
D5 = st.dur('S05')
STREET = {'eiffelStyle': 'v2', 'clear': [-4.0, 4.0]}
POSTERS = [[6.95, 1.55, -1.0, -90], [6.95, 1.6, 2.2, -90], [-6.95, 1.5, 0.6, 90], [6.95, 1.5, -4.5, -90]]
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('passant', [6.3, 0, -1.05], -90, 'stand', 'neutral', keys=[k(0.0, look=[6.95, 1.55, -1.0]), k(0.0, toon={'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'gx': 0.3}}, toonDur=0.0),
            k(0.35, toon={'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'brow': 0.6, 'gx': 0.2, 'mouth': 'o'}}, toonDur=0.2), k(0.7, toon={'face': {'lid': 1.0}}, toonDur=0.05), k(0.78, toon={'face': {'lid': 0.3, 'brow': 0.6}}, toonDur=0.08)])],
        props=[*[P(f'pole5{i}', 'streetLamp', pos=[r(x_ + (0.12 if ry_ < 0 else -0.12)), 0, z_]) for i, (x_, y_, z_, ry_) in enumerate(POSTERS)],
               *[P(f'post5{i}', 'missingPoster', pos=[x_, y_, z_], ry=ry_, opts={'w': 0.42, 'h': 0.58}) for i, (x_, y_, z_, ry_) in enumerate(POSTERS)]],
        cams=[FC(0.0, [3.6, 1.7, 1.8], [[6.95, 2.0, -1.0], [6.95, 1.0, -1.0], [6.3, 2.2, -1.05], [6.3, 0.0, -1.05], [6.95, 1.9, 2.2]], top=0.16, bottom=0.76, drift=(0.1, 0.0, -0.15))])

# 6: it was reported... In a green valley a hiker stops and points up: the letters « OHÉ ! » crossing the sky over the peaks; his eyes pop
D6 = st.dur('S06')
HIK = [0.0, 0, 0.0]
st.shot('S06', 'grassland', setOpts=ALPS, actors=[
        act('rando', HIK, 160, 'stand', 'neutral', keys=[k(0.0, look=[-4.0, 9.0, -30.0]), k(0.0, toon={'face': {'lid': 0.3}}, toonDur=0.0),
            k(0.1, toon={'reach': {'R': [-0.5, 2.4, -0.6, 1, 0.08]}, 'hands': {'R': 'point'}, 'face': {'lid': 0.0, 'eye': 0.7, 'pupil': 0.5, 'brow': 1.0, 'mouth': 'O'}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.08, toonEase='outBack')])],   # he points, his eyes wide (the stalks kept for S08)
        props=[*RING('6'), P('ohe6', 'shoutLetters', pos=[0, 0, 0], face='camera', opts={'text': 'OHÉ !', 'size': 0.45, 'path': [[0.0, 6.0, 7.5, -22.0], [D6, -7.0, 8.5, -24.0]], 'grow': [[0.0, 3.0]]})],
        cams=[FC(0.0, [1.2, 1.1, 3.4], [[HIK[0], 2.1, HIK[2]], [HIK[0], 0.0, HIK[2]], [0.0, 10.5, -23.0], [-0.6, 2.5, -0.6]], top=0.1, bottom=0.8, drift=(-0.1, 0.0, 0.0), level=False)])
st.cue('sfx:boing', 'S06', 0.12, 0.2)

# 7: ...in three valleys. Another valley, from the other side: a farmer in his field looks up from under his cap, his jaw drops; the letters cross
#    the other way
D7 = st.dur('S07')
FARM = [0.0, 0, 0.0]
st.shot('S07', 'grassland', setOpts={**ALPS, 'grass': '#9CC46E'}, actors=[
        act('fermier', FARM, -150, 'stand', 'neutral', keys=[k(0.0, look=[5.0, 9.0, -28.0]), k(0.0, toon={'face': {'lid': 0.4}}, toonDur=0.0),
            k(0.08, toon={'face': {'lid': 0.0, 'brow': 1.0, 'jaw': 0.6, 'jawLen': 0.4, 'mouth': 'O', 'gy': -0.6}, 'hat': [0.25, 0.3, 0.0], 'sq': [0.97, 1.04, 0.97]}, toonDur=0.08, toonEase='outBack')])],   # his jaw drops, his cap lifts
        props=[*RING('7'), P('ohe7', 'shoutLetters', pos=[0, 0, 0], face='camera', opts={'text': 'OHÉ !', 'size': 0.45, 'path': [[0.0, -6.0, 8.5, -24.0], [D7, 7.0, 7.5, -22.0]], 'grow': [[0.0, 3.0]]})],
        cams=[FC(0.0, [-1.3, 1.0, 3.2], [[FARM[0], 2.2, FARM[2]], [FARM[0], 0.0, FARM[2]], [0.0, 10.5, -23.0]], top=0.1, bottom=0.8, drift=(0.1, 0.0, 0.0), level=False)])
st.cue('sfx:gasp', 'S07', 0.1, 0.2)

# 8: yesterday the echo came home. His street: he walks out on the pavement; far down the street the letters come back, growing huge as they come;
#    he turns, his eyes go out on stalks
D8 = st.dur('S08'); TURN8 = 0.7
ME = [7.2, 0, 0.0]
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [7.2, 0, 1.2], 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.0, to=ME, dur=0.55, clip='walk', then='stand', ease='out', face='keep'),
            k(r(TURN8 - 0.12), toon={'face': {'lid': 0.3, 'gx': -0.8, 'gy': -0.2}}, toonDur=0.06), k(TURN8, look=[0.0, 3.0, -20.0]),   # his eyes first, then his head...
            k(r(TURN8 + 0.3), toon={'face': {'lid': 0.0, 'pop': 0.95, 'popLen': 0.3, 'brow': 1.0, 'mouth': 'O'}, 'sq': [0.95, 1.06, 0.95], 'hairUp': 1.0}, toonDur=0.06, toonEase='out'),   # ...his eyes out on stalks
            k(r(TURN8 + 0.5), toon={'face': {'lid': 0.0, 'pop': 0.85, 'popLen': 0.26, 'brow': 1.0, 'mouth': 'O', 'tremble': 1.0}, 'sq': [0.98, 1.02, 0.98], 'hairUp': 1.0}, toonDur=0.08)])],
        props=[P('ohe8', 'shoutLetters', pos=[0, 0, 0], face='camera', opts={'text': 'OHÉÉÉ !', 'size': 0.6, 'path': [[0.0, 0.5, 4.0, -60.0], [r(TURN8 + 0.15), 2.5, 3.2, -22.0], [D8, 5.3, 2.4, -1.6]], 'grow': [[0.0, 1.0], [D8, 3.4]], 'wobble': 0.3}),
               P('spd8', 'speedLines', pos=[0, 0, 0], face='camera', opts={'n': 8, 'len': 2.2, 'w': 1.6, 'angle': 1.45, 'at': [[0.0, r(TURN8 + 0.2)]], 'path': [[0.0, 0.5, 4.0, -58.0], [r(TURN8 + 0.15), 2.5, 3.4, -19.0]]})],   # (cycle 22) streaks behind the word
        cams=[FC(0.0, [7.9, 2.0, 3.0], [[ME[0], 2.35, ME[2]], [r(ME[0] - 0.3), 1.2, ME[2]], [1.0, 5.0, -40.0], [4.0, 1.0, -30.0]], top=0.12, bottom=0.7, drift=(0.0, 0.0, 0.1)),   # over his shoulder: the letters far down the street...
              FC(r(TURN8 + 0.2), [r(ME[0] - 1.2), 1.85, -2.3], [[ME[0], 2.42, ME[2]], [ME[0], 1.2, ME[2]], [r(ME[0] - 0.45), 1.9, ME[2]], [r(ME[0] + 0.45), 1.9, ME[2]]], top=0.14, bottom=0.66, drift=(0.0, 0.0, 0.12))])   # ...a reverse on his face: eyes on stalks
st.cue('whoosh', 'S08', 0.4, 0.4, 1.3, 150, 700); st.cue('sfx:boing', 'S08', r(TURN8 + 0.3), 0.3)

# 9: two years late. SPLAT: the giant letters hit him and he is flattened on the pavement like a sheet of paper (the letters bounce off); he peels
#    himself up stiff as a board and, POP, back to his shape, his hair standing on end
D9 = st.dur('S09'); HIT9 = 0.08; UP9 = 0.8; POP9 = 1.05
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 0.0, 'pop': 0.85, 'popLen': 0.26, 'brow': 1.0, 'mouth': 'O'}, 'hairUp': 1.0}, toonDur=0.0),
            k(HIT9, toon={'lay': [round(-PI / 2, 4), 0.0], 'sq': [1.15, 1.08, 0.05], 'hairUp': 1.0, 'face': {'lid': 0.0, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # SPLAT: flat on his back, a sheet of paper...
            k(r(HIT9 + 0.12), toon={'lay': [round(-PI / 2, 4), 0.0], 'sq': [1.12, 1.06, 0.05], 'hairUp': 1.0, 'face': {'lid': 0.3, 'brow': 0.4, 'stars': 1.0, 'starsScale': 1.6}}, toonDur=0.1),   # ...held, stars...
            k(UP9, toon={'lay': [0.0, 0.0], 'sq': [1.05, 1.02, 0.06], 'hairUp': 1.0, 'face': {'lid': 0.45, 'stars': 1.0, 'starsScale': 1.6}}, toonDur=0.18, toonEase='inOut'),   # ...he swings up stiff as a board, still flat...
            k(POP9, toon={'sq': [0.88, 1.15, 1.3], 'hairUp': 1.0, 'face': {'lid': 0.2, 'brow': 0.6}}, toonDur=0.06, toonEase='outBack'),   # ...POP: back to his shape, past it...
            k(r(POP9 + 0.12), toon={'sq': [1.04, 0.97, 1.0], 'hairUp': 0.9, 'face': DEAD}, toonDur=0.1), k(r(POP9 + 0.24), toon={'hairUp': 0.85, 'face': DEAD}, toonDur=0.12)])],   # ...deadpan, hair on end
        props=[P('ohe9', 'shoutLetters', pos=[0, 0, 0], face='camera', opts={'text': 'OHÉÉÉ !', 'size': 0.6, 'path': [[0.0, r(ME[0] - 0.9), 1.7, -2.0], [HIT9, r(ME[0] - 0.15), 1.1, -0.35], [r(HIT9 + 0.3), r(ME[0] - 2.2), 3.0, -1.4], [D9, r(ME[0] - 6.5), 5.0, -8.0]],
                 'grow': [[0.0, 3.6], [D9, 2.6]], 'squash': [[0.0, 1.0, 1.0], [HIT9, 1.35, 0.6], [r(HIT9 + 0.1), 0.9, 1.15], [r(HIT9 + 0.2), 1.0, 1.0]], 'wobble': 0.35}),   # the letters squash on him and bounce off
               BURST('splat9', [r(ME[0] - 0.75), 0.55, -0.4], HIT9, 'SPLAT !', 0.55)],
        fx=[{'type': 'shake', 'at': HIT9, 'dur': 0.2, 'amount': 0.016}],
        cams=[FC(0.0, [r(ME[0] - 1.4), 2.6, -2.5], [[ME[0], 2.3, ME[2]], [ME[0], 0.0, ME[2]], [ME[0], 0.0, r(ME[2] + 1.8)], [r(ME[0] - 0.75), 0.9, -0.4]], top=0.14, bottom=0.78, drift=(0.06, 0.0, 0.08))])   # (check) from in front and high: flat on his back, his face up to us
st.cue('sfx:splat', 'S09', HIT9, 0.5); st.cue('sfx:stretch', 'S09', r(UP9 - 0.05), 0.25); st.cue('sfx:pop', 'S09', POP9, 0.4)

# 10: it shouted... Night: the giant letters rattle between the buildings of the street; a woman and a boy in the street hold their ears, hair on end
D10 = st.dur('S10')
NIGHT = {**STREET, 'night': True}
st.shot('S10', 'parisStreet', setOpts=NIGHT, actors=[
        act('voisine', [1.0, 0, 0.6], 160, 'stand', 'scared', keys=[k(0.0, look=[0.0, 4.0, -6.0]), k(0.0, toon={'touch': {'L': ['head', 0.9, 0.55, 0.0, 1, 0.02], 'R': ['head', -0.9, 0.55, 0.0, 1, 0.02]}, 'hands': {'L': 'open', 'R': 'open'}, 'hairUp': 1.0, 'face': {'lid': 1.0, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.0),
            *[k(r(0.08 * i), toon={'touch': {'L': ['head', 0.9, 0.55, 0.0, 1, 0.02], 'R': ['head', -0.9, 0.55, 0.0, 1, 0.02]}, 'hands': {'L': 'open', 'R': 'open'}, 'hairUp': 1.0, 'sq': ([0.97, 1.03, 0.97] if i % 2 else [1.02, 0.98, 1.02]), 'face': {'lid': 1.0, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.07) for i in range(1, 9)]]),
        act('gamin', [-0.6, 0, 1.0], -160, 'stand', 'scared', keys=[k(0.0, look=[0.0, 4.0, -6.0]), *[k(r(0.04 + 0.08 * i), toon={'touch': {'L': ['head', 0.9, 0.55, 0.0, 1, 0.02], 'R': ['head', -0.9, 0.55, 0.0, 1, 0.02]}, 'hands': {'L': 'open', 'R': 'open'}, 'hairUp': 1.0, 'sq': ([1.03, 0.97, 1.03] if i % 2 else [0.97, 1.03, 0.97]), 'face': {'lid': 0.0, 'eye': 0.6, 'pupilShake': 1.0, 'brow': 1.0, 'mouth': 'scream'}}, toonDur=0.07) for i in range(9)]])],
        props=[P('ohe10', 'shoutLetters', pos=[0, 0, 0], face='camera', opts={'text': 'OHÉÉÉ !', 'size': 0.6, 'path': [[0.0, -3.5, 5.5, -7.0], [0.25, 3.5, 4.0, -6.5], [0.5, -3.0, 6.0, -7.5], [D10, 3.0, 4.8, -6.5]], 'grow': [[0.0, 3.2]], 'wobble': 0.45})],
        cams=[FC(0.0, [0.3, 1.2, 4.6], [[1.0, 2.2, 0.6], [-0.6, 1.5, 1.0], [1.0, 0.0, 0.6], [-3.5, 7.2, -7.0], [3.5, 7.2, -7.0]], top=0.08, bottom=0.8, drift=(0.0, 0.0, -0.1), level=False)])
st.cue('sfx:whistle', 'S10', 0.05, 0.2); st.cue('whoosh', 'S10', 0.0, 0.3, 0.7, 300, 1100)

# 11: ...for three days. By day: he stands in his street with rings under his eyes, his hair wild, his hands over his ears; the letters still shouting
#     over the roofs behind him
D11 = st.dur('S11')
EARS = lambda face, sq=None: {'touch': {'L': ['head', 0.92, 0.55, 0.0, 1, 0.02], 'R': ['head', -0.92, 0.55, 0.0, 1, 0.02]}, 'hands': {'L': 'open', 'R': 'open'}, 'hairUp': 0.9, **({'sq': sq} if sq else {}), 'face': face}
TIRED = {'lid': 0.6, 'shadow': 1.0, 'brow': -0.3, 'mouth': 'wavy'}
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -50, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=EARS(TIRED), toonDur=0.0),
            *[k(r(0.1 + 0.1 * i), toon=EARS({**TIRED, 'tremble': 1.0}, [0.98, 1.02, 0.98] if i % 2 else [1.01, 0.99, 1.01]), toonDur=0.08) for i in range(6)],   # jolted by the noise
            k(0.8, toon=EARS({**TIRED, 'lid': 1.0}), toonDur=0.08), k(0.95, toon=EARS(TIRED), toonDur=0.12)])],   # a long blink
        props=[P('ohe11', 'shoutLetters', pos=[0, 0, 0], face='camera', opts={'text': 'OHÉÉÉ !', 'size': 0.6, 'path': [[0.0, 3.0, 9.0, -9.0], [0.4, 5.5, 8.0, -8.0], [0.8, 2.5, 9.5, -9.5], [D11, 5.0, 8.5, -8.5]], 'grow': [[0.0, 2.6]], 'wobble': 0.45})],
        cams=[FC(0.0, [5.6, 1.8, 1.4], [[ME[0], 2.4, ME[2]], [ME[0], 1.1, ME[2]], [r(ME[0] - 0.4), 1.7, ME[2]], [r(ME[0] + 0.4), 1.7, ME[2]], [4.0, 10.6, -9.0]], top=0.08, bottom=0.66, level=False)])
st.cue('sfx:whistle', 'S11', 0.1, 0.15)

# 12: the gendarmerie fined the man... The gendarme walks up, writes the ticket and slaps it on his forehead: his head knocked back
D12 = st.dur('S12'); STICK12 = 0.7
GD12 = [r(ME[0] - 0.85), 0, r(ME[2] + 0.35)]
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[GD12[0], 1.7, GD12[2]]), k(0.0, toon={'hairUp': 0.8, 'face': TIRED}, toonDur=0.0),
            k(STICK12, toon={'bend': {'neck': [-0.35, 0, 0, 1, None]}, 'sq': [1.03, 0.97, 1.03], 'hairUp': 0.8, 'face': {**TIRED, 'lid': 1.0}}, toonDur=0.04, toonEase='out'),   # the slap knocks his head back...
            k(r(STICK12 + 0.12), toon={'hairUp': 0.8, 'face': TIRED}, toonDur=0.12, toonEase='outBack')]),   # ...and it comes back, deadpan
        act('gendarme', GD12, 100, 'stand', 'neutral', keys=[k(0.0, look=[GD12[0], 1.1, r(GD12[2] + 0.3)]),
            *[k(r(0.05 + 0.1 * i), toon={'reach': {'R': [r(GD12[0] + 0.2 + (0.04 if i % 2 else -0.03)), 1.15, r(GD12[2] + 0.25), 1, 0.05], 'L': [r(GD12[0] + 0.18), 1.1, r(GD12[2] + 0.12), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'open'}, 'face': {'lid': 0.55, 'gy': 0.6}}, toonDur=0.08) for i in range(4)],   # writing on his pad...
            k(0.48, look=[ME[0], 1.95, ME[2]]), k(0.52, toon={'reach': {'R': [r(GD12[0] + 0.1), 1.75, r(GD12[2] - 0.05), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'brow': -0.4}}, toonDur=0.1),   # ...a wind-up...
            k(r(STICK12 - 0.04), toon={'reach': {'R': [r(ME[0] - 0.18), 1.98, ME[2], 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'brow': -0.5}}, toonDur=0.05, toonEase='in'),   # ...SLAP on his forehead
            k(r(STICK12 + 0.25), toon={'reach': {'R': [r(GD12[0] + 0.2), 1.2, r(GD12[2] + 0.2), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.15)])],
        props=[P('fine12', 'fineTicket', pos=[r(GD12[0] + 0.2), 1.18, r(GD12[2] + 0.28)], rot=[-1.2, 1.2, 0], opts={'w': 0.2}, keys=[k(STICK12, attach='mec', joint='head', offset=[0.0, 0.3, 0.2], rot=[0.0, 0.0, 0.08])]),
               BURST('paf12', [r(ME[0] - 0.4), 2.4, r(ME[2] + 0.4)], STICK12, 'PAF !', 0.4)],
        cams=[FC(0.0, [r(ME[0] - 1.6), 1.7, -2.0], [[ME[0], 2.4, ME[2]], [GD12[0], 2.3, GD12[2]], [ME[0], 1.0, ME[2]], [GD12[0], 1.0, GD12[2]]], top=0.14, bottom=0.72, drift=(0.06, 0.0, 0.06))])   # (check) from the other side: the gendarme covered him
st.cue('sfx:paper', 'S12', 0.1, 0.15); st.cue('sfx:punch', 'S12', STICK12, 0.35)

# 13: ...for the noise. Close on him: the fine stuck on his forehead, his hair on end, rings under his eyes; a tiny « ohé » drifts down past his face;
#     his eyes follow it, come back to us; a slow blink
D13 = st.dur('S13')
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -90, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'hairUp': 0.8, 'face': TIRED}, toonDur=0.0),
            k(0.5, toon={'hairUp': 0.8, 'face': {**TIRED, 'gy': 0.5, 'gx': -0.3}}, toonDur=0.25, toonEase='inOut'), k(1.3, toon={'hairUp': 0.8, 'face': {**TIRED, 'gy': 0.8}}, toonDur=0.3, toonEase='inOut'),   # his eyes follow the little shout down...
            k(1.85, toon={'hairUp': 0.8, 'sq': [1.0, 1.02, 1.0], 'face': {**TIRED, 'gy': 0.0}}, toonDur=0.2, toonEase='inOut'),   # ...back to us...
            k(2.35, toon={'hairUp': 0.8, 'face': {**TIRED, 'lid': 1.0}}, toonDur=0.14), k(2.6, toon={'hairUp': 0.8, 'sq': [1.0, 0.99, 1.0], 'face': TIRED}, toonDur=0.18)])],   # ...a slow blink
        props=[P('fine13', 'fineTicket', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.3, 0.2]}, rot=[0.0, 0.0, 0.08], opts={'w': 0.2}),
               P('ohe13', 'shoutLetters', pos=[0, 0, 0], face='camera', opts={'text': 'ohé', 'size': 0.07, 'colors': ['#F5C33B', '#F08A3C', '#E8463A'], 'path': [[0.0, r(ME[0] - 0.35), 2.6, 0.25], [1.4, r(ME[0] - 0.32), 1.55, 0.3], [D13, r(ME[0] - 0.3), 1.2, 0.3]], 'wobble': 0.25})],
        cams=[FC(0.0, [r(ME[0] - 1.5), 1.9, 0.7], [[ME[0], 2.42, ME[2]], [ME[0], 1.45, ME[2]], [r(ME[0] - 0.35), 2.0, 0.25]], top=0.14, bottom=0.62, drift=(0.15, 0.0, -0.08))])   # a slow push-in

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 0.7, 'mec', 'shout'), ('S02', 0.6, 'mec', 'listen'), ('S03', 0.5, 'mec', 'mime'), ('S04', 0.5, 'gendarme', 'slap'), ('S06', 0.3, 'rando', 'point'),
           ('S07', 0.3, 'fermier', 'gape'), ('S08', 1.2, 'mec', 'stalks'), ('S09', 0.3, 'mec', 'flat'), ('S10', 0.4, 'gamin', 'night'), ('S11', 0.5, 'mec', 'ears'), ('S12', 0.85, 'mec', 'fine'), ('S13', 2.0, 'mec', 'end')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S04', 0.7, 'poster4', 'avis'), ('S13', 1.0, 'fine13', 'amende')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S05', 'DISPARU')
st.card('S13', 'TAPAGE', at=0.3)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("L'écho", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'gendarme': {'preset': 'cop', 'seed': 601, 'suit': '#1F3E6E', 'hat': 'copcap', 'mustache': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'passant': {'preset': 'boss', 'seed': 602, 'suit': '#6B5B45', 'hat': 'fedora', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'rando': {'preset': 'tourist', 'seed': 603, 'suit': '#D8642E', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'fermier': {'preset': 'fermier', 'seed': 604, 'hat': 'cap', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'voisine': {'preset': 'madame', 'seed': 605, 'suit': '#8E5AA8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'gamin': {'preset': 'gamin', 'seed': 606, 'suit': '#3A9BDC', 'toon': EX},
})
