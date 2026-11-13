#!/usr/bin/env python3
"""Le bâillement (story 58, cycle 20 of the cartoon staging): this man yawned too hard. His jaw fell to the ground. It never went back up. The town
hall classed it as a slide. On Sundays, there is a queue. The postman drops the mail in it. Yesterday he shut his mouth. With the postman inside.
He gets his mail from the inside.
Staging: at a bus stop on a Paris pavement he stretches into a huge yawn; his jaw drops as a block all the way to the pavement, CLONK, dust, his
eyes popping; he lifts it back up to his face in both hands and lets go: it drops again; the mayor in his sash cuts a ribbon, a TOBOGGAN sign pops up
and his tongue unrolls along the pavement like a carpet; on Sunday a queue waits at a ladder propped against him and a granny slides down his open
mouth and off the end of his tongue; the postman posts letters in at his upper lip and they flutter down inside; leaning in head first with a
parcel, the postman vanishes when the jaw springs shut, SNAP, his cap fluttering down; the man's belly bulges and the bulge wanders about, muffled
knocks from inside; a letter rises out between his lips like toast from a toaster; he takes it and reads it, deadpan.
Natural look; cycle 20 tools: the block jaw hung in front of the body (face.jawBlock, face.jawFwd), props_baillement.js (tongueSlide, envelope,
mailBag, bellyBulge, ribbonCut, bigScissors, mayorSash)."""
from story_kit import *
import math

st = Story('baillement', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L05', 4), ('S07', 'L06', 0),
         ('S08', 'L06', 4), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L09', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)

STREET = {'eiffelStyle': 'v2', 'clear': [-4.0, 4.0]}                    # no tree or lamp on the right pavement around him
ME = [7.2, 0, 0.0]; RY = -90                                             # on the right pavement, facing the road (-X)
FX = -1.0                                                                # his forward is -X
HEADY = 1.63                                                             # his head joint (the chin) standing
JF = 0.22                                                                # the dropped jaw hangs this far in front of the face: clear of his chest
JLEN = r(HEADY / 0.5 + 0.02)                                             # the drop in head heights that brings the chin to the pavement
JAWDOWN = {'jaw': 1.0, 'jawLen': JLEN, 'jawBlock': 1.0, 'jawFwd': JF}
CHINX = r(ME[0] + FX * (0.085 + JF))                                     # where the chin lands, in front of his feet
MOUTHTOP = 1.78                                                          # the top of the open mouth (under his nose)
DEAD = {'lid': 0.45}
BURST = lambda pid, pos, at_, text, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
FACE = lambda extra=None: {**JAWDOWN, **DEAD, **(extra or {})}           # his face with the jaw on the pavement
TONGUE = lambda pid, unroll=None: P(pid, 'tongueSlide', pos=[r(CHINX - 0.02), 0.0, ME[2]], ry=-90, opts={'len': 1.55, 'w': 0.26, **({'unroll': unroll} if unroll else {})})
BUS = lambda pid: P(pid, 'busStop', pos=[r(ME[0] + 0.9), 0, r(ME[2] - 1.9)], ry=-90)

# 1: the hook. A Paris pavement, a bus stop: he waits; he stretches into a huge yawn: arms up, back arched, eyes screwed shut, his mouth opening wider
#    and wider, his hair rising
D1 = st.dur('S01'); Y1 = 0.35
YAWN = lambda k_: {'reach': {'L': [r(ME[0] - 0.05), r(1.9 + 0.55 * k_), r(ME[2] + 0.32), 1, 0.05], 'R': [r(ME[0] - 0.05), r(1.9 + 0.55 * k_), r(ME[2] - 0.32), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'},
                   'bend': {'spine': [r(-0.3 * k_), 0, 0, 1, None], 'neck': [r(-0.35 * k_), 0, 0, 1, None]}, 'sq': [r(1 - 0.06 * k_), r(1 + 0.1 * k_), r(1 - 0.06 * k_)]}
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(round(Y1 - 0.12, 3), toon={'sq': [1.03, 0.96, 1.03], 'face': {'lid': 0.6}}, toonDur=0.12, toonEase='in'),   # a little sag first...
            k(Y1, toon={**YAWN(0.5), 'face': {'lid': 0.9, 'jaw': 0.35, 'jawLen': 0.5, 'mouth': 'O', 'brow': -0.4}}, toonDur=0.3, toonEase='inOut'),   # ...up into the stretch...
            k(round(Y1 + 0.32, 3), toon={**YAWN(1.0), 'hairUp': 0.7, 'face': {'lid': 1.0, 'jaw': 0.9, 'jawLen': 0.7, 'mouth': 'O', 'brow': -0.6}}, toonDur=0.45, toonEase='inOut'),   # ...wider and wider...
            *[k(round(Y1 + 0.8 + 0.035 * i, 3), toon={**YAWN(1.0), 'hairUp': 0.8, 'face': {'lid': 1.0, 'jaw': round(0.95 + (0.04 if i % 2 else 0.0), 3), 'jawLen': 0.75, 'mouth': 'O', 'brow': -0.7}}, toonDur=0.035) for i in range(5)]])],   # ...a quiver at the top
        props=[BUS('bus1')],
        cams=[FC(0.0, [r(ME[0] - 2.4), 1.6, 1.3], [[ME[0], 2.85, ME[2]], [ME[0], 1.0, ME[2]], [ME[0], 2.4, r(ME[2] + 0.5)], [ME[0], 2.4, r(ME[2] - 0.5)]], top=0.1, bottom=0.72, drift=(0.15, 0.0, -0.06))])
st.cue('sfx:slideUp', 'S01', round(Y1 + 0.1, 3), 0.3)

# 2: his jaw fell to the ground. Full figure: the jaw drops as a block down in front of him to the pavement: CLONK, a puff of dust, his eyes pop out;
#    then deadpan above it, a long dark open mouth from under his nose to the ground
D2 = st.dur('S02'); DROP2 = 0.18; HIT2 = 0.34
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**YAWN(0.9), 'face': {'lid': 1.0, 'jaw': 0.9, 'jawLen': 0.75, 'jawBlock': 1.0, 'jawFwd': JF, 'mouth': 'O'}}, toonDur=0.0),
            k(DROP2, toon={'face': {**JAWDOWN, 'jaw': 0.35, 'lid': 0.3, 'brow': 0.5, 'mouth': 'O'}}, toonDur=0.08, toonEase='in'),   # the arms down, the jaw going...
            k(round(DROP2 + 0.08, 3), toon={'face': {**JAWDOWN, 'lid': 0.2, 'brow': 0.6, 'mouth': 'O'}}, toonDur=round(HIT2 - DROP2 - 0.08, 3), toonEase='in'),   # ...all the way down...
            k(HIT2, toon={'sq': [1.04, 0.95, 1.04], 'face': {**JAWDOWN, 'lid': 0.0, 'pop': 0.6, 'popLen': 0.22, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.03, toonEase='out'),   # ...CLONK: his eyes pop...
            k(round(HIT2 + 0.25, 3), toon={'face': FACE({'pop': 0.0})}, toonDur=0.12),   # ...and back in, deadpan
            k(round(D2 - 0.3, 3), toon={'face': FACE({'lid': 1.0})}, toonDur=0.05), k(round(D2 - 0.18, 3), toon={'face': FACE()}, toonDur=0.08)])],
        props=[BUS('bus2'), P('dust2', 'dustPuff', pos=[CHINX, 0.0, ME[2]], opts={'once': True, 'startAt': HIT2, 'period': 0.6}), BURST('clonk2', [r(CHINX - 0.35), 0.75, r(ME[2] + 0.55)], HIT2, 'CLONK !', 0.55)],
        cams=[FC(0.0, [r(ME[0] - 3.0), 1.2, 1.4], [[ME[0], 2.4, ME[2]], [ME[0], 0.0, ME[2]], [r(CHINX - 0.4), 0.0, r(ME[2] + 0.5)], [ME[0], 2.0, r(ME[2] - 0.5)]], top=0.12, bottom=0.74)])
st.cue('sfx:slideDown', 'S02', DROP2, 0.3); st.cue('sfx:thud', 'S02', HIT2, 0.5); st.cue('clang', 'S02', HIT2, 0.35)

# 3: it never went back up. He crouches, lifts the chin back up to his face in both hands... lets go: it drops again, CLONK; deadpan
D3 = st.dur('S03'); UP3 = 0.55; LET3 = 0.78; HIT3 = round(LET3 + 0.14, 3)
CHIN = lambda jaw: [CHINX, r(max(0.07, HEADY - jaw * JLEN * 0.5 + 0.07)), ME[2]]   # the chin block's middle for a jaw value (block drop: jaw x jawLen head heights)
LIFT = lambda jaw: {'reach': {'L': [r(CHIN(jaw)[0] - 0.05), CHIN(jaw)[1], r(ME[2] + 0.17), 1, 0.05], 'R': [r(CHIN(jaw)[0] - 0.05), CHIN(jaw)[1], r(ME[2] - 0.17), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE()}, toonDur=0.0),
            k(0.08, toon={**LIFT(1.0), 'bend': {'spine': [0.9, 0, 0, 1, None]}, 'face': FACE({'brow': -0.3})}, toonDur=0.16, toonEase='inOut'),   # bent double to the chin...
            k(UP3, toon={**LIFT(0.12), 'bend': {'spine': [0.0, 0, 0, 1, None]}, 'face': {**JAWDOWN, 'jaw': 0.12, 'lid': 0.3, 'brow': 0.4}}, toonDur=round(UP3 - 0.24, 3), toonEase='inOut'),   # ...and up with it in both hands, to his face
            k(round(LET3 - 0.08, 3), toon={**LIFT(0.12), 'face': {**JAWDOWN, 'jaw': 0.12, 'lid': 0.45, 'brow': 0.6, 'mouth': 'smile'}}, toonDur=0.06),   # ...a hopeful little smile...
            k(LET3, toon={'reach': {'L': [r(ME[0] - 0.25), 1.4, r(ME[2] + 0.4), 1, 0.05], 'R': [r(ME[0] - 0.25), 1.4, r(ME[2] - 0.4), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {**JAWDOWN, 'jaw': 0.2, 'lid': 0.3, 'brow': 0.7}}, toonDur=0.04),   # ...he lets go...
            k(round(LET3 + 0.04, 3), toon={'face': {**JAWDOWN, 'lid': 0.3, 'brow': 0.7}}, toonDur=round(HIT3 - LET3 - 0.04, 3), toonEase='in'),   # ...it drops...
            k(HIT3, toon={'sq': [1.03, 0.96, 1.03], 'face': FACE({'lid': 0.6})}, toonDur=0.03, toonEase='out'), k(round(HIT3 + 0.15, 3), toon={'face': FACE()}, toonDur=0.1)])],   # ...CLONK, deadpan
        props=[BUS('bus3'), P('dust3', 'dustPuff', pos=[CHINX, 0.0, ME[2]], opts={'once': True, 'startAt': HIT3, 'period': 0.5}), BURST('clonk3', [r(CHINX - 0.35), 0.7, r(ME[2] - 0.55)], HIT3, 'CLONK !', 0.5)],
        cams=[FC(0.0, [r(ME[0] - 2.6), 1.1, -1.2], [[ME[0], 2.3, ME[2]], [ME[0], 0.0, ME[2]], [r(CHINX - 0.3), 0.0, ME[2]], [ME[0], 1.8, r(ME[2] + 0.5)]], top=0.12, bottom=0.74)])
st.cue('sfx:stretch', 'S03', 0.25, 0.2); st.cue('sfx:thud', 'S03', HIT3, 0.45)

# 4: the town hall classed it as a slide. The mayor in his sash snips a ribbon in front of him with giant scissors: a TOBOGGAN sign pops up beside
#    him, his tongue unrolls along the pavement to the kerb like a carpet; the mayor claps
D4 = st.dur('S04'); SNIP4 = 0.35; UNR4 = (0.45, 1.05)
MAIRE = [r(ME[0] - 1.0), 0, r(ME[2] - 0.95)]   # (audit) on the far side: on our side he covered the man
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE()}, toonDur=0.0), k(round(UNR4[0] + 0.1, 3), toon={'face': FACE({'gy': 0.6, 'gx': -0.3})}, toonDur=0.1),   # his eyes down to his tongue
            k(round(UNR4[1] + 0.1, 3), toon={'face': FACE()}, toonDur=0.1)]),
        act('maire', MAIRE, -40, 'stand', 'happy', keys=[k(0.0, look={'point': [r(CHINX - 0.3), 0.95, ME[2]], 'cheat': 0.4}),
            k(0.0, toon={'reach': {'R': [r(CHINX - 0.55), 1.0, r(ME[2] - 0.3), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.0),
            k(round(SNIP4 + 0.2, 3), toon={'reach': {'L': [r(MAIRE[0] - 0.12), 1.25, r(MAIRE[2] + 0.2), 1, 0.05], 'R': [r(MAIRE[0] - 0.22), 1.25, r(MAIRE[2] + 0.05), 1, 0.05]}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.6}}, toonDur=0.1),
            *[k(round(SNIP4 + 0.32 + 0.12 * i, 3), toon={'reach': {'L': [r(MAIRE[0] - 0.12), 1.25, r(MAIRE[2] + (0.14 if i % 2 else 0.2)), 1, 0.05], 'R': [r(MAIRE[0] - 0.22), 1.25, r(MAIRE[2] + (0.1 if i % 2 else 0.05)), 1, 0.05]}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'mouth': 'bigsmile', 'lid': 0.1}}, toonDur=0.06) for i in range(5)]])],   # he claps
        props=[BUS('bus4'), TONGUE('tong4', [[UNR4[0], 0.02], [UNR4[1], 1.0]]),
               P('rib4', 'ribbonCut', pos=[r(CHINX - 0.55), 0, ME[2]], ry=90, opts={'w': 1.3, 'h': 0.95, 'cutAt': SNIP4}),
               P('sash4', 'mayorSash', on={'actor': 'maire', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.135}),
               P('sci4', 'bigScissors', on={'actor': 'maire', 'hand': 'R', 'offset': [0, 0, 0.04]}, opts={'snip': [[0.0, 1.0], [round(SNIP4 - 0.04, 3), 1.0], [SNIP4, 0.0], [round(SNIP4 + 0.2, 3), 0.0]]}, keys=[k(round(SNIP4 + 0.22, 3), visible=False)]),
               P('sign4', 'signBoard', pos=[r(ME[0] - 0.1), 0, r(ME[2] + 1.0)], ry=-90, opts={'text': 'TOBOGGAN', 'w': 1.1, 'h': 0.42, 'height': 1.45, 'bg': '#F4F1E8', 'fg': '#1F3E99', 'frame': '#1F3E99'},
                 keys=[k(0.0, scale=0.001), k(round(SNIP4 + 0.05, 3), scale=1.0, dur=0.18, ease='outBack')])],   # pops up
        cams=[FC(0.0, [r(ME[0] - 3.3), 1.35, 2.2], [[ME[0], 2.35, ME[2]], [r(ME[0] - 1.7), 0.0, ME[2]], [MAIRE[0], 2.1, MAIRE[2]], [ME[0], 2.0, r(ME[2] + 1.0)], [MAIRE[0], 0.0, MAIRE[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:click', 'S04', SNIP4, 0.35); st.cue('sfx:pop', 'S04', round(SNIP4 + 0.05, 3), 0.3); st.cue('sfx:zip', 'S04', UNR4[0], 0.3); st.cue('sfx:fanfare', 'S04', round(SNIP4 + 0.1, 3), 0.15)

# 5: on Sundays there is a queue. Wide: a ladder propped against his chest, a queue of people waiting at its foot along the pavement, the sign, the
#    tongue down to the kerb; a man climbs the ladder; he stands under it all, deadpan
D5 = st.dur('S05')
LADB = [r(ME[0] - 0.6), 0, r(ME[2] - 0.62)]
Q = [[r(ME[0] - 0.85), 0, r(ME[2] - 1.25)], [r(ME[0] - 1.0), 0, r(ME[2] - 1.85)], [r(ME[0] - 1.15), 0, r(ME[2] - 2.45)]]   # along the pavement, in front of the bus stop
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE()}, toonDur=0.0), k(0.45, toon={'face': FACE({'lid': 1.0})}, toonDur=0.05), k(0.55, toon={'face': FACE()}, toonDur=0.08)]),
        act('q1', Q[0], 0, 'stand', 'happy', keys=[k(0.0, look=[ME[0], 1.7, ME[2]])]),
        act('q2', Q[1], 5, 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 1.7, ME[2]]), k(0.3, toon={'sq': [1.0, 1.015, 1.0]}, toonDur=0.3, toonEase='inOut')]),
        act('q3', Q[2], -5, 'stand', 'neutral', keys=[k(0.0, look=[ME[0], 1.7, ME[2]]), k(0.15, toon={'lay': [0.04, 0.0]}, toonDur=0.3, toonEase='inOut')])],
        props=[BUS('bus5'), TONGUE('tong5'), P('lad5', 'ladder', pos=LADB, ry=25, opts={'h': 1.9, 'lean': 0.32}),
               P('sign5', 'signBoard', pos=[r(ME[0] - 0.1), 0, r(ME[2] + 1.0)], ry=-90, opts={'text': 'TOBOGGAN', 'w': 1.1, 'h': 0.42, 'height': 1.45, 'bg': '#F4F1E8', 'fg': '#1F3E99', 'frame': '#1F3E99'})],
        cams=[FC(0.0, [r(ME[0] - 4.2), 1.5, 2.2], [[ME[0], 2.3, ME[2]], [r(ME[0] - 1.8), 0.0, ME[2]], [Q[2][0], 2.1, Q[2][2]], [Q[2][0], 0.0, Q[2][2]], [ME[0], 2.0, r(ME[2] + 1.0)]], top=0.1, bottom=0.74)])
st.cue('sfx:street', 'S05', 0.0, 0.1)

# 6: the queue. A granny in his open mouth slides down it, out over his chin and along his tongue to the kerb, her arms up: WHEE; at the end she lands
#    on her bottom, bounces; he looks down at her, deadpan
D6 = st.dur('S06'); GO6 = 0.12; BOT6 = 0.42; END6 = 0.78
MAMIE0 = [r(CHINX - 0.12), 1.12, r(ME[2] + 0.02)]
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE({'gy': 0.5})}, toonDur=0.0), k(0.5, toon={'face': FACE({'gy': 0.8, 'gx': -0.2})}, toonDur=0.12)]),
        act('mamie', MAMIE0, -90, 'sit', 'happy', keys=[k(0.0, look=[r(ME[0] - 2.0), 0.4, ME[2]]),
            k(0.0, toon={'reach': {'L': [r(MAMIE0[0] - 0.1), 1.95, r(MAMIE0[2] + 0.3), 1, 0.05], 'R': [r(MAMIE0[0] - 0.1), 1.95, r(MAMIE0[2] - 0.3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'hairUp': 0.6, 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.7}}, toonDur=0.0),
            k(GO6, to=[r(CHINX - 0.12), 0.06, ME[2]], dur=round(BOT6 - GO6, 3), glide=True, ease='in', face='keep'),   # down his mouth...
            k(BOT6, to=[r(CHINX - 1.5), 0.04, ME[2]], dur=round(END6 - BOT6, 3), glide=True, ease='linear', face='keep'),   # ...along his tongue...
            k(END6, to=[r(CHINX - 1.85), 0.0, ME[2]], dur=0.12, glide=True, ease='out', face='keep'),
            k(END6, toon={'sq': [1.25, 0.75, 1.25], 'face': {'mouth': 'bigsmile', 'lid': 0.2, 'brow': 0.8}}, toonDur=0.04, toonEase='out'), k(round(END6 + 0.1, 3), toon={'sq': [0.95, 1.05, 0.95], 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.08)])],   # ...a bump at the end
        props=[BUS('bus6'), TONGUE('tong6'), BURST('whee6', [r(CHINX - 0.85), 1.15, r(ME[2] + 0.5)], round(BOT6 - 0.05, 3), 'YOUPI !', 0.45)],
        cams=[FC(0.0, [r(ME[0] - 2.2), 1.0, 2.4], [[ME[0], 2.3, ME[2]], [MAMIE0[0], 2.45, MAMIE0[2]], [r(CHINX - 1.9), 0.0, ME[2]], [r(CHINX - 1.9), 1.0, ME[2]], [ME[0], 0.0, ME[2]]], top=0.1, bottom=0.74, drift=(-0.2, 0.0, 0.0))])
st.cue('whoosh', 'S06', GO6, 0.3, 0.6, 400, 1500); st.cue('sfx:boing', 'S06', END6, 0.3)

# 7: the postman drops the mail in it. The postman in his yellow cap posts letters in at his upper lip, one after another, from his satchel
D7 = st.dur('S07')
FAC = [r(ME[0] - 0.5), 0, r(ME[2] + 0.72)]   # (audit) to his side: in front he hid him whole
SLOT = [r(CHINX - 0.02), r(MOUTHTOP - 0.06), ME[2]]
POSTS = [0.12, 0.38, 0.62]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE()}, toonDur=0.0), *[k(round(t_ + 0.06, 3), toon={'face': FACE({'gy': 0.4})}, toonDur=0.06) for t_ in POSTS]]),
        act('facteur', FAC, 145, 'stand', 'neutral', keys=[k(0.0, look=SLOT),
            *[x for t_ in POSTS for x in (k(round(t_ - 0.1, 3), toon={'reach': {'R': [r(FAC[0] + 0.08), 1.05, r(FAC[2] + 0.2), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.4}}, toonDur=0.08),   # a letter from the satchel...
                                          k(t_, toon={'reach': {'R': [r(SLOT[0] - 0.08), SLOT[1], r(SLOT[2] + 0.06), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.4}}, toonDur=0.1, toonEase='out'))]])],   # ...into his mouth
        props=[BUS('bus7'), TONGUE('tong7'), P('bag7', 'mailBag', on={'actor': 'facteur', 'joint': 'torso', 'offset': [0.12, 0.45, 0.0]}),
               *[P(f'let7{i}', 'envelope', pos=[SLOT[0], r(SLOT[1] - 0.02), r(SLOT[2] + 0.04)], ry=-90, keys=[k(0.0, visible=False), k(round(t_ + 0.1, 3), visible=True), k(round(t_ + 0.1, 3), to=[r(SLOT[0] + 0.03), 0.12 + 0.03 * i, ME[2]], dur=0.3, ease='in')])
                 for i, t_ in enumerate(POSTS)]],
        cams=[FC(0.0, [r(ME[0] - 2.5), 1.45, -1.3], [[ME[0], 2.3, ME[2]], [ME[0], 0.0, ME[2]], [FAC[0], 2.0, FAC[2]], [FAC[0], 0.0, FAC[2]]], top=0.1, bottom=0.74)])
for t_ in POSTS: st.cue('sfx:paper', 'S07', round(t_ + 0.05, 3), 0.2)

# 8: close on his face: deadpan, his eyes down; letters flutter down inside his open mouth
D8 = st.dur('S08')
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE({'gy': 0.7})}, toonDur=0.0), k(0.4, toon={'face': FACE({'gy': 0.0})}, toonDur=0.12),
            k(round(D8 - 0.3, 3), toon={'face': FACE({'lid': 1.0})}, toonDur=0.06), k(round(D8 - 0.18, 3), toon={'face': FACE()}, toonDur=0.08)])],
        props=[BUS('bus8'), *[P(f'let8{i}', 'envelope', pos=[r(SLOT[0] - 0.01), r(MOUTHTOP - 0.05 - 0.1 * i), r(ME[2] + 0.05 * (i - 1))], ry=-90, rot=[0.0, round(-PI / 2, 4), round(0.4 * (i - 1), 3)],
                                  keys=[k(round(0.05 + 0.18 * i, 3), to=[r(SLOT[0] + 0.02), 0.6, r(ME[2] + 0.04 * (i - 1))], dur=0.5, ease='in')]) for i in range(3)]],
        cams=[FC(0.0, [r(ME[0] - 1.35), 1.85, 0.45], [[ME[0], 2.25, ME[2]], [ME[0], 1.2, ME[2]], [r(CHINX - 0.1), 1.2, r(ME[2] + 0.2)]], top=0.16, bottom=0.66)])
st.cue('sfx:paper', 'S08', 0.1, 0.15)

# 9: yesterday he shut his mouth. The postman leans in head first with a parcel; SNAP: the jaw springs up into place, his head squashed and
#    stretched by it; the postman gone; his yellow cap flutters down to the pavement
D9 = st.dur('S09'); IN9 = 0.4; SNAP9 = 0.72
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE({'gy': 0.5})}, toonDur=0.0),
            k(round(SNAP9 - 0.06, 3), toon={'sq': [1.04, 0.95, 1.04], 'face': FACE({'lid': 0.6, 'brow': -0.3})}, toonDur=0.05, toonEase='in'),   # a gulp of breath...
            k(SNAP9, toon={'scl': {'head': [1.25, 0.75, 1.2]}, 'sq': [0.94, 1.08, 0.94], 'face': {'jaw': 0.0, 'jawLen': JLEN, 'jawBlock': 1.0, 'jawFwd': JF, 'lid': 0.2, 'brow': 0.6, 'cheeks': 0.8}}, toonDur=0.04, toonEase='out'),   # ...SNAP: shut, his head squashed...
            k(round(SNAP9 + 0.08, 3), toon={'scl': {'head': [0.9, 1.12, 0.92]}, 'face': {'jaw': 0.0, 'lid': 0.4, 'cheeks': 0.9}}, toonDur=0.06), k(round(SNAP9 + 0.16, 3), toon={'face': {'jaw': 0.0, 'lid': 0.45, 'cheeks': 0.7}}, toonDur=0.08)]),   # ...stretched, then still, his cheeks full
        act('facteur', FAC, 135, 'stand', 'neutral', keys=[k(0.0, look=SLOT),
            k(0.1, toon={'reach': {'L': [r(FAC[0] + 0.35), 1.45, r(FAC[2] - 0.1), 1, 0.05], 'R': [r(FAC[0] + 0.35), 1.45, r(FAC[2] - 0.35), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.15),
            k(IN9, toon={'reach': {'L': [r(SLOT[0] + 0.05), 1.6, r(SLOT[2] + 0.12), 1, 0.05], 'R': [r(SLOT[0] + 0.05), 1.6, r(SLOT[2] - 0.12), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.7, 0, 0, 1, None]}, 'face': {'lid': 0.4}}, toonDur=0.2, toonEase='inOut'),   # head first into his mouth
            k(IN9, to=[r(FAC[0] + 0.32), 0, r(FAC[2] - 0.3)], dur=0.2, ease='inOut', face='keep'), k(SNAP9, visible=False)])],
        props=[BUS('bus9'), TONGUE('tong9', [[0.0, 1.0], [round(SNAP9 - 0.01, 3), 1.0], [round(SNAP9 + 0.06, 3), 0.02]]),
               P('box9', 'cardboardBox', on={'actor': 'facteur', 'hand': 'R', 'offset': [0.0, 0.0, 0.08]}, scale=0.45, keys=[k(SNAP9, visible=False)]),
               P('cap9', 'beanieHat', pos=[r(SLOT[0] - 0.15), 1.75, ME[2]], opts={'color': '#F2C230'}, keys=[k(0.0, visible=False), k(SNAP9, visible=True), k(SNAP9, path=[[r(SLOT[0] - 0.35), 1.4, r(ME[2] + 0.2)], [r(SLOT[0] - 0.55), 0.6, ME[2]], [r(SLOT[0] - 0.7), 0.02, r(ME[2] + 0.15)]], dur=0.7, ease='out')]),
               BURST('snap9', [r(CHINX - 0.45), 2.1, r(ME[2] - 0.45)], SNAP9, 'CLAC !', 0.5)],
        cams=[FC(0.0, [r(ME[0] - 2.6), 1.4, -1.3], [[ME[0], 2.35, ME[2]], [ME[0], 0.0, ME[2]], [FAC[0], 2.0, FAC[2]], [r(SLOT[0] - 0.8), 0.0, ME[2]]], top=0.1, bottom=0.74)])
st.cue('clack', 'S09', SNAP9, 0.5); st.cue('sfx:gulp', 'S09', round(SNAP9 + 0.1, 3), 0.3)

# 10: with the postman inside. His belly bulges and the bulge wanders about under his shirt, a knock, another; deadpan, he blinks
D10 = st.dur('S10')
BULGE = [[0.0, 0.0, 0.08, 0.14], [0.35, 0.08, 0.16, 0.15], [0.6, -0.07, 0.02, 0.15], [0.95, 0.04, 0.12, 0.15], [1.25, -0.02, 0.06, 0.14]]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45, 'cheeks': 0.4}}, toonDur=0.0),
            *[k(t_, toon={'sq': [1.03, 0.98, 1.03], 'lay': [0.03 * (1 if i % 2 else -1), 0.0], 'face': {'lid': 0.45, 'cheeks': 0.3}}, toonDur=0.06, toonEase='out') for i, t_ in enumerate((0.36, 0.62, 0.96))],   # each knock jolts him
            k(1.1, toon={'face': {'lid': 1.0, 'cheeks': 0.3}}, toonDur=0.06), k(1.22, toon={'face': {'lid': 0.45, 'cheeks': 0.3}}, toonDur=0.08)])],
        props=[BUS('bus10'), P('bul10', 'bellyBulge', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0, 0]}, opts={'r': 0.13, 'path': [[b[0], b[1], b[2], b[3]] for b in BULGE], 'size': [[0.0, 0.7], [0.36, 1.2], [0.45, 0.9], [0.62, 1.25], [0.7, 0.9], [0.96, 1.3], [1.05, 0.95]]}),
               BURST('toc10', [r(ME[0] - 0.55), 1.35, r(ME[2] + 0.45)], 0.36, 'TOC !', 0.32), BURST('toc10b', [r(ME[0] - 0.55), 1.05, r(ME[2] - 0.45)], 0.62, 'TOC !', 0.28)],
        cams=[FC(0.0, [r(ME[0] - 1.8), 1.35, 0.7], [[ME[0], 2.25, ME[2]], [ME[0], 0.75, ME[2]], [ME[0], 1.4, r(ME[2] + 0.45)], [ME[0], 1.4, r(ME[2] - 0.45)]], top=0.14, bottom=0.7, drift=(0.12, 0.0, -0.04))])
st.cue('thud', 'S10', 0.36, 0.25); st.cue('thud', 'S10', 0.62, 0.25); st.cue('thud', 'S10', 0.96, 0.2)

# 11: he gets his mail from the inside. A letter rises out between his lips like toast from a toaster; he takes it, unfolds it and reads it; he looks
#    up at us, deadpan, a slow blink; the bulge waves under his shirt
D11 = st.dur('S11'); OUT11 = 0.25; TAKE11 = 0.75
LIPS = [r(ME[0] + FX * 0.1), r(HEADY + 0.12), ME[2]]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45, 'cheeks': 0.3, 'gy': 0.6}}, toonDur=0.0),
            k(round(TAKE11 - 0.25, 3), toon={'reach': {'R': [r(LIPS[0] - 0.08), r(LIPS[1] + 0.2), r(LIPS[2] - 0.04), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.45, 'cheeks': 0.3, 'gy': 0.5}}, toonDur=0.2, toonEase='inOut'),   # he takes it...
            k(round(TAKE11 + 0.15, 3), toon={'reach': {'R': [r(ME[0] - 0.38), 1.35, r(ME[2] - 0.12), 1, 0.05], 'L': [r(ME[0] - 0.38), 1.35, r(ME[2] + 0.12), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.4, 'gy': 0.7}}, toonDur=0.25, toonEase='inOut'),   # ...reads it...
            k(1.5, toon={'reach': {'R': [r(ME[0] - 0.38), 1.35, r(ME[2] - 0.12), 1, 0.05], 'L': [r(ME[0] - 0.38), 1.35, r(ME[2] + 0.12), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.45, 'gy': 0.0}}, toonDur=0.15),   # ...looks up at us...
            k(1.95, toon={'reach': {'R': [r(ME[0] - 0.38), 1.35, r(ME[2] - 0.12), 1, 0.05], 'L': [r(ME[0] - 0.38), 1.35, r(ME[2] + 0.12), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 1.0}}, toonDur=0.1),
            k(2.15, toon={'reach': {'R': [r(ME[0] - 0.38), 1.35, r(ME[2] - 0.12), 1, 0.05], 'L': [r(ME[0] - 0.38), 1.35, r(ME[2] + 0.12), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.45}}, toonDur=0.16)])],   # ...a slow blink
        props=[BUS('bus11'), P('let11', 'envelope', pos=[LIPS[0], r(LIPS[1] - 0.06), LIPS[2]], ry=-90, opts={'w': 0.2}, keys=[k(OUT11, to=[LIPS[0], r(LIPS[1] + 0.1), LIPS[2]], dur=0.3, ease='outBack'),   # up out of his lips...
               k(TAKE11, attach='mec', joint='handR', offset=[0.0, -0.05, 0.03])]),   # ...into his hand
               P('bul11', 'bellyBulge', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0, 0]}, opts={'r': 0.12, 'path': [[0.0, 0.0, 0.1, 0.14], [2.6, 0.03, 0.1, 0.14]], 'size': [[0.0, 0.8], [1.6, 0.8], [1.75, 1.15], [1.9, 0.8], [2.05, 1.1], [2.2, 0.8]]})],
        cams=[FC(0.0, [r(ME[0] - 1.6), 1.6, 0.55], [[ME[0], 2.3, ME[2]], [ME[0], 0.95, ME[2]], [r(ME[0] - 0.45), 1.5, r(ME[2] + 0.35)]], top=0.16, bottom=0.68, drift=(0.15, 0.0, -0.05))])
st.cue('sfx:slideUp', 'S11', OUT11, 0.3); st.cue('sfx:ding', 'S11', round(OUT11 + 0.3, 3), 0.2); st.cue('sfx:paper', 'S11', TAKE11, 0.25)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 1.1, 'mec', 'yawn'), ('S02', round(HIT2 + 0.05, 3), 'mec', 'clonk'), ('S03', 0.6, 'mec', 'lift'), ('S04', 0.9, 'maire', 'ribbon'), ('S05', 0.4, 'mec', 'queue'),
           ('S06', 0.5, 'mamie', 'slide'), ('S07', 0.5, 'facteur', 'post'), ('S08', 0.4, 'mec', 'letters'), ('S09', round(SNAP9 + 0.1, 3), 'mec', 'snap'), ('S10', 0.7, 'mec', 'bulge'),
           ('S11', 1.6, 'mec', 'mail')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S04', 0.8, 'sign4', 'toboggan')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S04', 'TOBOGGAN')
st.card('S10', 'DEDANS')

st.write("Le bâillement", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'maire': {'preset': 'politique', 'seed': 581, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.06}},
    'q1': {'preset': 'boss', 'seed': 582, 'suit': '#6B5B45', 'build': {'width': 0.95, 'headWidth': 1.2}},
    'q2': {'preset': 'madame', 'seed': 583, 'suit': '#3E8E6E', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'q3': {'preset': 'sportif', 'seed': 584, 'suit': '#C8642A', 'build': {'width': 0.95, 'headWidth': 1.2}},
    'mamie': {'preset': 'mamie', 'seed': 585, 'build': {'width': 0.9, 'headWidth': 1.25}},
    'facteur': {'preset': 'worker', 'seed': 586, 'suit': '#2E5AA8', 'hat': 'beanie', 'hatColor': '#F2C230', 'build': {'width': 1.0, 'headWidth': 1.2}},
})
