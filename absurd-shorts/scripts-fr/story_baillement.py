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
DEAD = {'lid': 0.45, 'pupil': 1.0}                                         # (final pass) bigger pupils: 3 px slits disappeared on a phone
BURST = lambda pid, pos, at_, text, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
FACE = lambda extra=None: {**JAWDOWN, **DEAD, **(extra or {})}           # his face with the jaw on the pavement
TONGUE = lambda pid, unroll=None: P(pid, 'tongueSlide', pos=[r(CHINX - 0.02), 0.0, ME[2]], ry=-90, opts={'len': 1.55, 'w': 0.26, **({'unroll': unroll} if unroll else {})})
BUS = lambda pid: P(pid, 'busStop', pos=[r(ME[0] + 0.9), 0, r(ME[2] - 1.9)], ry=-90)

# 1: the hook. A Paris pavement, a bus stop: he waits; he stretches into a huge yawn: arms up, back arched, eyes screwed shut, his mouth opening wider
#    and wider, his hair rising
D1 = st.dur('S01'); Y1 = 0.35
YAWN = lambda k_: {'reach': {'L': [r(ME[0] - 0.05), r(1.9 + 0.55 * k_), r(ME[2] + 0.32), 1, 0.05], 'R': [r(ME[0] - 0.05), r(1.9 + 0.55 * k_), r(ME[2] - 0.32), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'},
                   'bend': {'spine': [r(-0.2 * k_), 0, 0, 1, None], 'neck': [r(-0.1 * k_), 0, 0, 1, None]}, 'sq': [r(1 - 0.06 * k_), r(1 + 0.1 * k_), r(1 - 0.06 * k_)]}
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.03, toon={'sq': [1.07, 0.9, 1.07], 'bend': {'spine': [0.2, 0, 0, 1, None], 'neck': [0.1, 0, 0, 1, None]}, 'face': {'lid': 0.7, 'cheeks': 0.5, 'brow': -0.3}}, toonDur=round(Y1 - 0.08, 3), toonEase='inOut'),   # (pass 3) a crouch and an inhale first (no crouch or arch before the stretch)...
            k(Y1, toon={**YAWN(0.5), 'face': {'lid': 0.9, 'jaw': 0.35, 'jawLen': 0.5, 'jawBlock': 1.0, 'jawFwd': 0.06, 'mouth': 'O', 'brow': -0.4}}, toonDur=0.3, toonEase='inOut'),   # ...up into the stretch...
            k(round(Y1 + 0.32, 3), toon={**YAWN(1.0), 'hairUp': 0.7, 'face': {'lid': 1.0, 'jaw': 0.9, 'jawLen': 0.7, 'jawBlock': 1.0, 'jawFwd': 0.1, 'mouth': 'O', 'brow': -0.6}}, toonDur=0.45, toonEase='inOut'),   # ...wider and wider...
            *[k(round(Y1 + 0.8 + 0.035 * i, 3), toon={**YAWN(1.0), 'hairUp': 0.8, 'face': {'lid': 1.0, 'jaw': round(0.95 + (0.04 if i % 2 else 0.0), 3), 'jawLen': 0.75, 'jawBlock': 1.0, 'jawFwd': 0.1, 'mouth': 'O', 'brow': -0.7}}, toonDur=0.035) for i in range(5)]])],   # ...a quiver at the top ((pass 2) the jaw in front of the tie)
        props=[BUS('bus1')],
        cams=[FC(0.0, [r(ME[0] - 2.5), 1.3, 0.85], [[ME[0], 2.85, ME[2]], [ME[0], 1.0, ME[2]], [ME[0], 2.4, r(ME[2] + 0.5)], [ME[0], 2.4, r(ME[2] - 0.5)]], top=0.1, bottom=0.72, drift=(0.15, 0.0, -0.06))])   # (stills 1) lower and more frontal: from above and the side the yawn was the top of a skull
st.cue('sfx:slideUp', 'S01', round(Y1 + 0.1, 3), 0.3)

# (pass 2) the tie and its knot hidden while the jaw is down (the knot showed as a bright square in the open mouth, the tie over the lower jaw)
def TH(a, until=None, after=None):
    for kk in a['keys']:
        if 'toon' in kk:
            on = (until is None or kk['at'] < until) and (after is None or kk['at'] >= after)
            kk['toon'] = {**kk['toon'], 'tieHide': 1 if on else 0}
    return a
XCAV = lambda y: r(ME[0] - 0.095 - (MOUTHTOP - y) / (MOUTHTOP - 0.1) * 0.2)   # the dark mouth's front at a height: it slants from his upper lip to the chin hung forward

# 2: his jaw fell to the ground. Full figure: (pass 2) at the top of the yawn the jaw hangs a beat, creaking, his eyes open and go down to it; then it
#    drops as a block to the pavement: CLONK, a puff of dust, his eyes pop out, his body squashed by the jolt; then deadpan above the long open mouth,
#    a glance down at it, a breath, a blink
D2 = st.dur('S02'); HANG2 = 0.3; HIT2 = 0.44
YAWNF = {'lid': 1.0, 'jaw': 0.95, 'jawLen': 0.75, 'jawBlock': 1.0, 'jawFwd': 0.1, 'mouth': 'O'}
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        TH(act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**YAWN(0.9), 'face': YAWNF}, toonDur=0.0),
            k(0.08, toon={**YAWN(0.75), 'face': {**YAWNF, 'jaw': 1.0, 'lid': 0.15, 'gy': 0.7, 'brow': 0.5}}, toonDur=0.08, toonEase='out'),   # his eyes open, down to it: a creak...
            k(0.17, toon={**YAWN(0.6), 'face': {**YAWNF, 'jaw': 0.97, 'lid': 0.0, 'gy': 0.8, 'brow': 0.7}}, toonDur=0.05),
            k(0.23, toon={**YAWN(0.5), 'face': {**YAWNF, 'jaw': 1.03, 'lid': 0.0, 'gy': 0.8, 'brow': 0.8}}, toonDur=0.05),   # ...it hangs, trembling...
            k(HANG2, toon={'face': {**JAWDOWN, 'jaw': 0.4, 'lid': 0.0, 'brow': 0.9, 'mouth': 'O'}}, toonDur=round(HIT2 - HANG2, 3), toonEase='in'),   # ...and goes
            k(HIT2, toon={'sq': [1.08, 0.9, 1.08], 'face': {**JAWDOWN, 'lid': 0.0, 'pop': 0.65, 'popLen': 0.24, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.03, toonEase='out'),   # CLONK: eyes out, the jolt
            k(round(HIT2 + 0.1, 3), toon={'sq': [0.97, 1.03, 0.97], 'face': {**JAWDOWN, 'lid': 0.0, 'pop': 0.5, 'popLen': 0.2, 'brow': 1.0}}, toonDur=0.06),
            k(round(HIT2 + 0.28, 3), toon={'face': FACE({'pop': 0.0})}, toonDur=0.12),   # ...back in, deadpan
            k(0.98, toon={'face': FACE({'gy': 0.7})}, toonDur=0.12), k(1.12, toon={'sq': [1.0, 1.035, 1.0], 'lay': [0.0, 0.025], 'face': FACE({'gy': 0.0})}, toonDur=0.2, toonEase='inOut'),   # a glance down at it, a breath ((pass 3) bigger: the hold froze)
            k(1.36, toon={'sq': [1.0, 0.99, 1.0], 'lay': [0.0, -0.01], 'face': FACE({'gx': 0.3})}, toonDur=0.2, toonEase='inOut'),
            k(round(D2 - 0.3, 3), toon={'face': FACE({'lid': 1.0})}, toonDur=0.05), k(round(D2 - 0.18, 3), toon={'face': FACE()}, toonDur=0.08)]))],
        props=[BUS('bus2'), P('dust2', 'dustPuff', pos=[CHINX, 0.0, ME[2]], opts={'once': True, 'startAt': HIT2, 'period': 0.6}), BURST('clonk2', [r(CHINX - 0.35), 0.75, r(ME[2] + 0.55)], HIT2, 'CLONK !', 0.55)],
        cams=[FC(0.0, [r(ME[0] - 3.0), 1.2, 1.4], [[ME[0], 2.4, ME[2]], [ME[0], 0.0, ME[2]], [r(CHINX - 0.4), 0.0, r(ME[2] + 0.5)], [ME[0], 2.0, r(ME[2] - 0.5)]], top=0.12, bottom=0.74)])
st.cue('sfx:squeak', 'S02', 0.12, 0.2); st.cue('sfx:slideDown', 'S02', HANG2, 0.3); st.cue('sfx:thud', 'S02', HIT2, 0.5); st.cue('clang', 'S02', HIT2, 0.35)

# 3: it never went back up. (pass 2) He squats (bending at the waist swung the jaw, fixed to his head, out behind his hips), his hands go to the chin on
#    the pavement, he rises with it to his face, the jaw closing as he goes up; a hopeful smile held nine frames; he opens his hands: the jaw hangs a
#    beat, creaking, his eyes go down; it drops: CRAC, the pavement cracks, he is yanked down, his eyes pop further; deadpan
D3 = st.dur('S03'); SQ3 = 0.22; UP3 = 0.55; LET3 = 0.85; FALL3 = 1.0; HIT3 = 1.1
HY3 = 1.64                                                               # his head joint standing ((cycle 18) measured on the same build: 1.64-1.65)
JAWAT = lambda hy: r(min(1.0, (hy - 0.02) / (JLEN * 0.5)))               # the jaw that keeps the chin on the pavement with his head at hy
PIN3 = lambda y: {'joint': 'head', 'off': [0.0, 0.0, 0.0], 'at': [r(ME[0] - 0.02), r(y), ME[2]], 'w': 1}
PLANT3 = {'L': [ME[0], 0.03, r(ME[2] + 0.09), 1], 'R': [ME[0], 0.03, r(ME[2] - 0.09), 1]}
CHINAT = lambda jaw, hy, jf: [r(ME[0] - 0.085 - jf - 0.02), r(max(0.08, hy - jaw * JLEN * 0.5 + 0.07)), ME[2]]   # the chin block's middle
HOLD3 = lambda jaw, hy, jf, grip='grip': {'reach': {'L': [CHINAT(jaw, hy, jf)[0], CHINAT(jaw, hy, jf)[1], r(ME[2] + 0.17), 1, 0.05], 'R': [CHINAT(jaw, hy, jf)[0], CHINAT(jaw, hy, jf)[1], r(ME[2] - 0.17), 1, 0.05]}, 'hands': {'L': grip, 'R': grip}}
SQY = 1.0
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        TH(act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'pin': PIN3(HY3), 'plant': PLANT3, 'face': FACE()}, toonDur=0.0),
            k(0.04, toon={'pin': PIN3(SQY), 'plant': PLANT3, **HOLD3(JAWAT(SQY), SQY, JF, 'open'), 'face': {**JAWDOWN, 'jaw': JAWAT(SQY), 'lid': 0.3, 'brow': -0.3, 'gy': 0.6}}, toonDur=0.18, toonEase='inOut'),   # down into a squat, the jaw on the ground... ((check stills) a blend runs after its key: keyed early)
            k(0.24, toon={'pin': PIN3(SQY + 0.03), 'plant': PLANT3, **HOLD3(JAWAT(SQY + 0.03), SQY + 0.03, JF), 'face': {**JAWDOWN, 'jaw': JAWAT(SQY + 0.03), 'lid': 0.3, 'brow': -0.5}}, toonDur=0.06),   # ...his hands on the chin, a heave...
            *[k(t_, toon={'pin': PIN3(r(SQY + 0.03 + (HY3 - SQY - 0.03) * u_)), 'plant': PLANT3, 'lay': [0.0, tl_], **HOLD3(r(JAWAT(SQY + 0.03) + (0.06 - JAWAT(SQY + 0.03)) * u_), r(SQY + 0.03 + (HY3 - SQY - 0.03) * u_), r(JF + (0.03 - JF) * u_)),
                              'face': {**JAWDOWN, 'jaw': r(JAWAT(SQY + 0.03) + (0.06 - JAWAT(SQY + 0.03)) * u_), 'jawFwd': r(JF + (0.03 - JF) * u_), 'lid': 0.85, 'brow': -0.7, 'cheeks': 0.7}}, toonDur=0.08, toonEase='inOut')
              for t_, u_, tl_ in ((0.31, 0.4, 0.045), (0.39, 0.75, -0.045), (0.47, 1.0, 0.02))],   # (pass 3) ...up with it, straining, wobbling (he rose with a heavy jaw in 0.15 s, no strain)
            k(UP3, toon={'pin': PIN3(HY3), 'plant': PLANT3, **HOLD3(0.06, HY3, 0.03), 'face': {**JAWDOWN, 'jaw': 0.0, 'jawFwd': 0.0, 'lid': 0.4, 'brow': 0.7, 'mouth': 'smile'}}, toonDur=0.06),   # a hopeful little smile, held ((pass 3) the jaw shut: at 0.1 the mouth still showed the dark slot and teeth)...
            k(round(LET3 - 0.02, 3), toon={'pin': PIN3(HY3), 'plant': PLANT3, **HOLD3(0.06, HY3, 0.03), 'face': {**JAWDOWN, 'jaw': 0.0, 'jawFwd': 0.0, 'lid': 0.4, 'brow': 0.75, 'mouth': 'smile'}}, toonDur=0.2),
            k(LET3, toon={'pin': PIN3(HY3), 'plant': PLANT3, 'reach': {'L': [r(ME[0] - 0.3), 1.35, r(ME[2] + 0.42), 1, 0.05], 'R': [r(ME[0] - 0.3), 1.35, r(ME[2] - 0.42), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {**JAWDOWN, 'jaw': 0.12, 'jawFwd': 0.05, 'lid': 0.3, 'brow': 0.7, 'gy': 0.5}}, toonDur=0.05),   # ...he lets go: it hangs...
            k(0.93, toon={'pin': PIN3(HY3), 'plant': PLANT3, 'face': {**JAWDOWN, 'jaw': 0.15, 'jawFwd': 0.06, 'lid': 0.1, 'brow': 0.9, 'gy': 0.8}}, toonDur=0.04),   # ...a creak, his eyes down to it...
            k(FALL3, toon={'pin': PIN3(HY3), 'plant': PLANT3, 'face': {**JAWDOWN, 'lid': 0.1, 'brow': 0.9, 'gy': 0.8}}, toonDur=round(HIT3 - FALL3, 3), toonEase='in'),   # ...and drops
            k(HIT3, toon={'pin': PIN3(HY3 - 0.14), 'plant': PLANT3, 'sq': [1.05, 0.94, 1.05], 'face': {**JAWDOWN, 'lid': 0.0, 'pop': 1.0, 'popLen': 0.44, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.03, toonEase='out'),   # CRAC: yanked down, eyes further out ((pass 3) on longer stalks than at the CLONK)
            k(round(HIT3 + 0.12, 3), toon={'pin': PIN3(HY3 + 0.03), 'plant': PLANT3, 'face': {**JAWDOWN, 'lid': 0.2, 'pop': 0.3, 'popLen': 0.15, 'brow': 0.6}}, toonDur=0.08, toonEase='outBack'),
            k(round(HIT3 + 0.24, 3), toon={'pin': PIN3(HY3), 'plant': PLANT3, 'face': FACE()}, toonDur=0.08)]))],
        props=[BUS('bus3'), P('dust3', 'dustPuff', pos=[CHINX, 0.0, ME[2]], opts={'once': True, 'startAt': HIT3, 'period': 0.5}),
               P('crack3', 'ceilingCracks', pos=[CHINX, 0.012, ME[2]], rot=[round(-PI / 2, 4), 0, 0], opts={'r': 0.7, 'thick': 3.0}, keys=[k(0.0, visible=False), k(HIT3, visible=True)]),   # (pass 2) the second drop cracks the pavement
               BURST('crac3', [r(CHINX - 0.4), 0.8, r(ME[2] - 0.6)], HIT3, 'CRAC !', 0.55)],
        fx=[{'type': 'shake', 'at': HIT3, 'dur': 0.2, 'amount': 0.014}],
        cams=[FC(0.0, [r(ME[0] - 2.9), 0.95, -0.9], [[ME[0], 2.3, ME[2]], [ME[0], 0.0, ME[2]], [r(CHINX - 0.3), 0.0, ME[2]], [ME[0], 1.8, r(ME[2] + 0.5)], [r(CHINX - 0.5), 0.9, r(ME[2] - 0.7)]], top=0.12, bottom=0.74)])
st.cue('sfx:stretch', 'S03', 0.32, 0.2); st.cue('sfx:squeak', 'S03', 0.93, 0.2); st.cue('sfx:thud', 'S03', HIT3, 0.5); st.cue('clang', 'S03', HIT3, 0.3)

# 4: the town hall classed it as a slide. The mayor (pass 2: a grey suit, the sash over his jacket, scissors half his height) snips a ribbon in front
#    of him: the TOBOGGAN sign pops up beside him (it showed full size before the snip, then shrank: a scale key with no duration), his tongue unrolls
#    along the pavement to the kerb like a carpet; the mayor claps, four wide claps
D4 = st.dur('S04'); SNIP4 = 0.35; UNR4 = (0.45, 1.05)
MAIRE = [r(ME[0] - 1.0), 0, r(ME[2] - 0.95)]
CLAP = lambda open_: {'reach': {'L': [r(MAIRE[0] - 0.19 + (0.17 if open_ else 0.02)), 1.48, r(MAIRE[2] + 0.23 + (0.14 if open_ else 0.02)), 1, 0.05], 'R': [r(MAIRE[0] - 0.19 - (0.17 if open_ else 0.02)), 1.48, r(MAIRE[2] + 0.23 - (0.14 if open_ else 0.02)), 1, 0.05]}, 'hands': {'L': 'open', 'R': 'open'}}   # (final pass) both hands meeting in front of his chest (one arm flung out read as presenting)
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        TH(act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE()}, toonDur=0.0), k(round(UNR4[0] + 0.1, 3), toon={'face': FACE({'gy': 0.6, 'gx': -0.3})}, toonDur=0.1), k(round(UNR4[0] + 0.2, 3), look=[r(CHINX - 1.4), 0.1, ME[2]]),   # his eyes down to his tongue, then his head ((final pass) a head turn)
            k(round(UNR4[1] + 0.05, 3), look='camera'),
            k(round(UNR4[1] + 0.1, 3), toon={'face': FACE()}, toonDur=0.1), k(1.45, toon={'face': FACE({'lid': 1.0})}, toonDur=0.05), k(1.55, toon={'sq': [1.0, 1.015, 1.0], 'face': FACE()}, toonDur=0.2)])),   # (pass 2) a blink, a breath (0.8 s still)
        act('maire', MAIRE, -40, 'stand', 'happy', keys=[k(0.0, look={'point': [r(CHINX - 0.3), 0.95, ME[2]], 'cheat': 0.4}),
            k(0.0, toon={'reach': {'R': [r(CHINX - 0.55), 1.0, r(ME[2] - 0.3), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.0),
            k(round(SNIP4 + 0.2, 3), toon={**CLAP(True), 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.6}}, toonDur=0.1),
            *[k(round(SNIP4 + 0.34 + 0.13 * i, 3), toon={**CLAP(i % 2 == 0), 'sq': ([0.97, 1.05, 0.97] if i % 2 == 0 else [1.03, 0.96, 1.03]), 'face': {'mouth': 'bigsmile', 'lid': 0.1}}, toonDur=0.06) for i in range(8)]])],   # (pass 2) four wide claps ((pass 3) bouncing on his heels)
        props=[BUS('bus4'), TONGUE('tong4', [[UNR4[0], 0.02], [UNR4[1], 1.0]]),
               P('rib4', 'ribbonCut', pos=[r(CHINX - 0.55), 0, ME[2]], ry=90, opts={'w': 1.3, 'h': 0.95, 'cutAt': SNIP4}),
               P('sash4', 'mayorSash', on={'actor': 'maire', 'joint': 'torso', 'offset': [0, 0.42, 0]}, opts={'z': 0.21, 'w': 0.17, 'len': 0.8}),   # (pass 2) over the jacket (at 0.135 it was buried in it)
               P('sci4', 'bigScissors', on={'actor': 'maire', 'hand': 'R', 'offset': [0, 0, 0.04]}, scale=2.2, opts={'handle': '#2A2C30', 'open': 0.5, 'snip': [[0.0, 1.0], [round(SNIP4 - 0.04, 3), 1.0], [SNIP4, 0.0], [round(SNIP4 + 0.2, 3), 0.0]]}, keys=[k(round(SNIP4 + 0.22, 3), visible=False)]),   # (pass 2) half his height
               P('sign4', 'signBoard', pos=[r(ME[0] - 0.1), 0, r(ME[2] + 1.0)], ry=-90, opts={'text': 'TOBOGGAN', 'w': 1.1, 'h': 0.42, 'height': 1.45, 'bg': '#F4F1E8', 'fg': '#1F3E99', 'frame': '#1F3E99'},
                 keys=[k(0.0, scale=0.001, dur=0.0), k(round(SNIP4 + 0.05, 3), scale=1.0, dur=0.18, ease='outBack')])],   # (pass 2) at nothing from the first frame, then it pops
        cams=[FC(0.0, [r(ME[0] - 3.4), 0.8, 2.0], [[ME[0], 2.35, ME[2]], [r(ME[0] - 1.7), 0.0, ME[2]], [MAIRE[0], 2.1, r(MAIRE[2] - 0.3)], [r(MAIRE[0] - 0.2), 1.3, r(MAIRE[2] - 0.55)], [r(ME[0] - 0.1), 1.9, r(ME[2] + 1.6)], [MAIRE[0], 0.0, MAIRE[2]]], top=0.24, bottom=0.74)])   # (pass 2) his elbow in the frame
st.cue('sfx:click', 'S04', SNIP4, 0.35); st.cue('sfx:pop', 'S04', round(SNIP4 + 0.05, 3), 0.3); st.cue('sfx:zip', 'S04', UNR4[0], 0.3); st.cue('sfx:fanfare', 'S04', round(SNIP4 + 0.1, 3), 0.15)
for i in range(4): st.cue('sfx:click', 'S04', round(SNIP4 + 0.47 + 0.26 * i, 3), 0.12)

# (pass 3) the granny's ride: from just under his upper lip, down the dark slot well in front of its back (her head sank into the jaw at the bottom),
# out over the chin, along the tongue to the kerb; at a constant speed the slot takes about seven frames (it jumped from top to bottom in one)
RIDE6 = [[r(XCAV(1.38) - 0.38), 1.38, ME[2]], [r(XCAV(1.05) - 0.38), 1.05, ME[2]], [r(XCAV(0.72) - 0.39), 0.72, ME[2]], [r(XCAV(0.45) - 0.42), 0.45, ME[2]],   # (stills p3) her head 0.39 m behind her seat: at -0.2 it sank into him
         [r(CHINX - 0.38), 0.37, ME[2]], [r(CHINX - 1.45), 0.34, ME[2]]]   # her seat (reclined: her feet hang 0.2-0.4 m under it)
MAMIE0 = RIDE6[0]
MAMRIDE = {'touch': {'L': ['torso', 0.28, 0.95, 0.12, 1], 'R': ['torso', -0.28, 0.95, 0.12, 1]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'hairUp': 0.8, 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.8}}

# 5: on Sundays there is a queue. (pass 2) The ladder leans against his cheek up to his upper lip; a queue of five in single file from its foot along
#    the pavement, beside his tongue, facing him; the granny at the top of the ladder, next to go
D5 = st.dur('S05')
LADH = 1.85; LADL = 0.32; LADB = [r(ME[0] - 0.09 - LADH * math.sin(LADL)), 0, r(ME[2] - 0.38)]   # its top at the upper lip, beside the mouth (ry -90: it leans toward +X)
QZ = r(ME[2] - 0.55); QX = [r(LADB[0] - 0.4 - 0.5 * i) for i in range(5)]
GO5 = r(D5 - 0.2)
MAM5 = lambda leg: {'face': {'mouth': 'bigsmile', 'lid': 0.1}, 'reach': {'R': [r(ME[0] - 0.2), 1.95, r(ME[2] - 0.3), 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'legL': [leg, 0, 0, 1, None], 'shinL': [0.4, 0, 0, 1, None]}}
def FIDGET5(i):
    """(pass 3) each queuer's own business in the 0.97 s: a watch checked, a shuffle forward, a bounce on the heels, a lean out to see, a glance back"""
    if i == 0: return [k(0.12, toon={'touch': {'L': ['torso', 0.05, 0.6, 0.34, 1]}, 'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': {'gy': 0.8}}, toonDur=0.14), k(0.62, toon={'sq': [1.0, 1.02, 1.0]}, toonDur=0.16)]
    if i == 1: return [k(0.28, to=[r(QX[1] + 0.18), 0, r(QZ + 0.06)], dur=0.26, clip='walk', then='stand', ease='inOut', face='keep'), k(0.6, toon={'sq': [1.0, 1.02, 1.0]}, toonDur=0.2)]
    if i == 2: return [k(round(0.06 + 0.17 * j, 3), toon={'sq': ([0.98, 1.05, 0.98] if j % 2 == 0 else [1.02, 0.97, 1.02])}, toonDur=0.12, toonEase='inOut') for j in range(5)]
    if i == 3: return [k(0.18, toon={'lay': [0.0, -0.16], 'face': {'brow': 0.5}}, toonDur=0.2, toonEase='inOut'), k(0.66, toon={'lay': [0.0, 0.0]}, toonDur=0.2, toonEase='inOut')]
    return [k(0.22, look=[QX[3], 1.6, QZ]), k(0.6, look=[ME[0], 1.6, ME[2]]), k(0.3, toon={'sq': [1.0, 1.025, 1.0]}, toonDur=0.25, toonEase='inOut')]
st.shot('S05', 'parisStreet', setOpts={**STREET, 'clouds': 3, 'cloudSeed': 21}, actors=[   # (final pass) a cloud slab floated at the top left
        TH(act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE()}, toonDur=0.0), k(0.45, toon={'face': FACE({'lid': 1.0})}, toonDur=0.05), k(0.55, toon={'face': FACE({'gx': 0.4})}, toonDur=0.08)])),
        act('mamie', [r(LADB[0] + 0.42), 1.05, r(ME[2] - 0.38)], 90, 'stand', 'happy', keys=[k(0.0, look=[ME[0], 1.7, ME[2]]), k(0.0, toon=MAM5(0.0), toonDur=0.0),
            k(0.08, toon=MAM5(-0.6), toonDur=0.14, toonEase='inOut'), k(0.26, toon=MAM5(0.35), toonDur=0.14, toonEase='inOut'), k(0.44, toon=MAM5(-0.5), toonDur=0.14, toonEase='inOut'),   # (pass 3) she swings a leg over the top rung...
            k(GO5, face=-90, turn=0.12), k(GO5, to=MAMIE0, dur=round(D5 - GO5, 3), clip='reclineBack', then='reclineBack', ease='in', face='keep'), k(GO5, toon=MAMRIDE, toonDur=0.12)]),   # ...and pushes off into his mouth
        *[act(f'q{i + 1}', [QX[i], 0, r(QZ + (0.06 if i % 2 else -0.04))], 90, 'stand', ('happy' if i % 2 == 0 else 'neutral'), keys=[k(0.0, look=[ME[0], 1.6, ME[2]]), *FIDGET5(i)]) for i in range(5)]],   # in single file, facing him ((pass 3) fidgeting: they stood frozen)
        props=[BUS('bus5'), TONGUE('tong5'), P('lad5', 'ladder', pos=LADB, ry=-90, opts={'h': LADH, 'lean': LADL})],
        cams=[FC(0.0, [r(ME[0] - 2.0), 1.45, 2.6], [[ME[0], 2.3, ME[2]], [ME[0], 1.5, r(ME[2] + 0.4)], [ME[0], 1.5, r(ME[2] - 0.4)], [r(ME[0] + 0.47), 2.7, r(ME[2] - 0.8)], [r(CHINX - 1.6), 0.0, ME[2]], [QX[2], 2.0, QZ], [QX[2], 0.0, QZ], [r(LADB[0] + 0.42), 3.0, LADB[2]]], top=0.1, bottom=0.76)])   # (final pass) his shoulders and the BUS sign whole   # the granny's head on the ladder in the frame
st.cue('sfx:street', 'S05', 0.0, 0.1)

# 6: the queue. (pass 2) The granny's ride on one arc: in at his upper lip, down the dark slot (his mouth stretched wide for her), out over his lower
#    teeth, along his tongue, a bump at the kerb, YOUPI ! on her; his eyes follow her down
D6 = st.dur('S06'); BOT6 = 0.28; OUT6 = 0.42; END6 = 0.68                 # (final pass) slower: the slot about eight frames                 # (pass 3) at a constant speed: the slot ~7 frames, then the chin and the tongue
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        TH(act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': [1.9, 1.0, 1.0]}, 'face': FACE({'gy': 0.3})}, toonDur=0.0),   # the mouth stretched wide for her
            k(BOT6, toon={'scl': {'head': [2.0, 1.0, 1.0]}, 'face': FACE({'gy': 0.8})}, toonDur=0.1), k(OUT6, toon={'scl': {'head': [0.85, 1.05, 1.0]}, 'face': FACE({'gy': 0.9, 'gx': -0.4})}, toonDur=0.06, toonEase='out'),   # ...it snaps back past its width
            k(round(OUT6 + 0.1, 3), toon={'scl': {'head': [1.0, 1.0, 1.0]}, 'face': FACE({'gy': 0.8, 'gx': -0.6})}, toonDur=0.08)])),   # his eyes follow her down and away
        act('mamie', MAMIE0, -90, 'reclineBack', 'happy', keys=[k(0.0, look=[r(ME[0] - 2.0), 0.4, ME[2]]), k(0.0, toon=MAMRIDE, toonDur=0.0),
            k(0.0, path=RIDE6[1:], dur=END6, glide=True, ease='linear', face='keep'),   # one arc: down the slot, out over the chin, along the tongue...
            k(END6, toon={'sq': [1.25, 0.75, 1.25], 'face': {'mouth': 'bigsmile', 'lid': 0.2, 'brow': 0.8}}, toonDur=0.04, toonEase='out'), k(round(END6 + 0.1, 3), toon={'sq': [0.95, 1.05, 0.95], 'face': {'mouth': 'bigsmile', 'lid': 0.2}}, toonDur=0.08)]),   # ...a bump at the kerb
        *[act(f'q{i + 1}', [r(QX[i] - 0.6 + (0.18 if i == 1 else 0.0)), 0, r(QZ + (0.06 if i % 2 else -0.04))], 90, 'stand', ('happy' if i % 2 == 0 else 'neutral'), keys=[k(0.0, look=[r(ME[0] - 0.4), 1.0, ME[2]]),
            k(round(0.1 + 0.06 * i, 3), toon={'sq': [0.98, 1.04, 0.98], **({'reach': {'L': [r(QX[i] - 0.6), 2.1, r(QZ + 0.2), 1, 0.05], 'R': [r(QX[i] - 0.6), 2.1, r(QZ - 0.2), 1, 0.05]}} if i in (0, 2) else {})}, toonDur=0.14, toonEase='out')]) for i in range(5)]],   # (pass 3) the queue behind, two cheering
        props=[BUS('bus6'), TONGUE('tong6'), P('lad6', 'ladder', pos=LADB, ry=-90, opts={'h': LADH, 'lean': LADL}),
               P('whee6', 'hicBurst', on={'actor': 'mamie', 'joint': 'torso', 'offset': [0.0, 0.85, 0.35], 'face': 'camera'}, opts={'at': [0.03], 'w': 0.55, 'text': 'YOUPI !', 'inner': 0.78, 'fit': 0.56, 'hold': 0.5})],   # (final pass) on her, beside her head, moving with her (fixed over his head, he seemed to shout it)
        cams=[FC(0.0, [r(ME[0] - 2.7), 1.25, 2.4], [[ME[0], 2.3, ME[2]], [r(ME[0] - 0.55), 2.72, r(ME[2] + 0.75)], [r(ME[0] - 0.55), 1.9, r(ME[2] + 1.1)], [r(CHINX - 1.6), 0.0, ME[2]], [r(CHINX - 1.6), 1.0, ME[2]], [ME[0], 0.0, ME[2]]], top=0.1, bottom=0.74, drift=(-0.2, 0.0, 0.0))])
st.cue('whoosh', 'S06', 0.02, 0.3, 0.6, 400, 1500); st.cue('sfx:boing', 'S06', END6, 0.3)

# 7: the postman drops the mail in it. The postman posts letters in at his upper lip, one after another, from his satchel: (pass 2) each one goes in
#    behind the lip and is gone (they fluttered down in front of his jacket)
D7 = st.dur('S07')
FAC = [r(ME[0] - 0.5), 0, r(ME[2] - 0.72)]                               # (final pass) on the far side: from the usual side the tongue runs to screen-left
SLOT = [r(XCAV(MOUTHTOP - 0.03) - 0.03), r(MOUTHTOP - 0.03), ME[2]]          # (pass 3) just under the upper teeth (his hand arrived at collar height)
PICK = [r(FAC[0] + 0.08), 1.05, r(FAC[2] - 0.2)]                          # each envelope taken from the satchel
POSTS = [0.12, 0.38, 0.62]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        TH(act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE()}, toonDur=0.0), *[k(round(t_ + 0.06, 3), toon={'face': FACE({'gy': 0.4, 'gx': 0.4})}, toonDur=0.06) for t_ in POSTS],
            k(0.16, look={'point': [FAC[0], 1.7, FAC[2]], 'cheat': 0.5}), k(0.85, look='camera')])),   # (final pass) his eyes, then his head, to the postman
        act('facteur', FAC, 35, 'stand', 'neutral', keys=[k(0.0, look=SLOT),
            *[x for t_ in POSTS for x in (k(round(t_ - 0.1, 3), toon={'reach': {'R': PICK + [1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.4}}, toonDur=0.08),
                                          k(t_, toon={'reach': {'R': [r(SLOT[0] - 0.1), r(SLOT[1] + 0.08), r(SLOT[2] - 0.06), 1, 0.08]}, 'hose': 0.1, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.4}}, toonDur=0.1, toonEase='out'))]])],
        props=[BUS('bus7'), TONGUE('tong7'), P('bag7', 'mailBag', on={'actor': 'facteur', 'joint': 'torso', 'offset': [0.12, 0.45, 0.0]}, scale=1.6),   # (final pass) a shoulder bag that reads
               *[P(f'let7{i}', 'envelope', pos=PICK, face='camera', opts={'w': 0.24}, keys=[k(0.0, visible=False), k(round(t_ - 0.04, 3), visible=True),   # (final pass) a big white envelope out of the satchel, facing us...
                   k(t_, to=[r(SLOT[0] - 0.06), r(SLOT[1] - 0.02), SLOT[2]], dur=0.1, ease='out'),   # ...up with his hand, held square over the top of the dark slot...
                   k(round(t_ + 0.16, 3), to=[r(SLOT[0] - 0.04), r(SLOT[1] - 0.24), SLOT[2]], dur=0.07, ease='in'), k(round(t_ + 0.23, 3), visible=False)])   # ...and down into it, gone
                 for i, t_ in enumerate(POSTS)]],
        cams=[FC(0.0, [r(ME[0] - 2.3), 1.6, 1.5], [[ME[0], 2.35, ME[2]], [ME[0], 0.9, ME[2]], [FAC[0], 2.05, FAC[2]], [FAC[0], 0.9, FAC[2]], [SLOT[0], 1.5, r(ME[2] + 0.3)]], top=0.12, bottom=0.7)])   # (final pass) a medium two-shot from the usual side (the tongue to screen-left)
for t_ in POSTS: st.cue('sfx:paper', 'S07', round(t_ + 0.05, 3), 0.2)

# 8: close on his face: deadpan, his eyes down; (pass 2) the letters fall inside his open mouth, pale in its dark, inside its edges
D8 = st.dur('S08')
INSIDE8 = lambda y, dz: [r(XCAV(y) - 0.012), r(y), r(ME[2] + dz)]
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        TH(act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE({'gy': 0.25})}, toonDur=0.0), k(0.1, toon={'face': FACE({'gy': 0.55})}, toonDur=0.15),   # (pass 3) his eyes track them down...
            k(0.28, toon={'face': FACE({'gy': 0.9})}, toonDur=0.18), k(0.5, toon={'face': FACE({'lid': 1.0, 'gy': 0.9})}, toonDur=0.06), k(0.62, toon={'face': FACE({'gy': 0.35})}, toonDur=0.12)]))],   # ...a blink down there, back up
        props=[BUS('bus8'), P('let8', 'slotLetters', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0, 0]}, opts={'n': 3, 'w': 0.11, 'top': 0.12, 'bot': -1.0, 'z0': 0.108, 'z1': 0.262, 'at': [0.04, 0.2, 0.36], 'dur': 0.5})],   # (final pass) in his head's frame: in the world they fell down his lapel as he swayed
        cams=[FC(0.0, [r(ME[0] - 1.5), 1.7, 0.2], [[ME[0], 2.25, ME[2]], [ME[0], 1.2, ME[2]], [r(CHINX - 0.1), 1.2, r(ME[2] + 0.2)]], top=0.16, bottom=0.66)])
st.cue('sfx:paper', 'S08', 0.1, 0.15)

# 9: yesterday he shut his mouth. (pass 2) In profile: the postman leans in head first with a parcel, his head and shoulders inside the mouth, then he
#    is lifted off his feet and hangs there by the head, legs kicking (he poked out of the man's far shoulder); the tongue slurps back in; SNAP: the jaw
#    springs shut, squashing the man's head three frames, then stretching it; the postman pulled in, his legs last; his cap (the one he wore) flutters
#    down; deadpan, cheeks full, a gulp, a blink
D9 = st.dur('S09'); IN9 = 0.32; LIFT9 = 0.42; SNAP9 = 0.72
HEADIN = [r(XCAV(1.5) - 0.14), 1.5, ME[2]]                                # (pass 3) his head joint 14 cm in front of the slot: the head itself behind it (at +0.06 it came out of the man's back)
FACP = [r(ME[0] - 0.95), 0, r(ME[2] + 0.04)]
PINF = lambda at_: {'pin': {'joint': 'head', 'off': [0.0, 0.0, 0.0], 'at': [r(at_[0]), r(at_[1]), r(at_[2])], 'w': 1}}
KICK = lambda i: {'bend': {'spine': [0.15, 0, 0, 1, None], 'legL': [round(0.55 if i % 2 else -0.35, 3), 0, 0, 1, None], 'legR': [round(-0.35 if i % 2 else 0.55, 3), 0, 0, 1, None], 'shinL': [0.5, 0, 0, 1, None], 'shinR': [0.5, 0, 0, 1, None]}}
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        TH(act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': FACE({'gy': 0.5})}, toonDur=0.0),
            k(round(SNAP9 - 0.06, 3), toon={'sq': [1.04, 0.95, 1.04], 'face': FACE({'lid': 0.6, 'brow': -0.3})}, toonDur=0.05, toonEase='in'),
            k(round(SNAP9 - 0.04, 3), toon={'scl': {'head': [0.84, 1.45, 0.88]}, 'face': {'jaw': 0.65, 'jawLen': JLEN, 'jawBlock': 1.0, 'jawFwd': 0.16, 'lid': 0.4, 'brow': 0.6}}, toonDur=0.015, toonEase='in'),   # (pass 3) a vertical smear up his body...
            k(round(SNAP9 - 0.01, 3), toon={'scl': {'head': [0.86, 1.25, 0.9]}, 'face': {'jaw': 0.35, 'jawLen': JLEN, 'jawBlock': 1.0, 'jawFwd': 0.12, 'lid': 0.4, 'brow': 0.6}}, toonDur=0.02, toonEase='in'),   # a two-frame smear as it springs up...
            k(SNAP9, toon={'scl': {'head': [1.32, 0.7, 1.25]}, 'sq': [0.94, 1.08, 0.94], 'face': {'jaw': 0.0, 'jawLen': JLEN, 'jawBlock': 1.0, 'jawFwd': 0.0, 'lid': 0.2, 'brow': 0.6, 'cheeks': 0.8}}, toonDur=0.03, toonEase='out'),   # ...SNAP: shut, his head squashed...
            k(round(SNAP9 + 0.1, 3), toon={'scl': {'head': [1.28, 0.73, 1.22]}, 'face': {'jaw': 0.0, 'lid': 0.3, 'cheeks': 0.9}}, toonDur=0.07),   # ...held three frames...
            k(round(SNAP9 + 0.17, 3), toon={'scl': {'head': [0.9, 1.12, 0.92]}, 'face': {'jaw': 0.0, 'lid': 0.4, 'cheeks': 0.9}}, toonDur=0.06), k(round(SNAP9 + 0.26, 3), toon={'face': {'jaw': 0.0, 'lid': 0.45, 'cheeks': 0.75}}, toonDur=0.08),   # ...stretched, then still, cheeks full
            k(round(SNAP9 + 0.45, 3), toon={'sq': [1.0, 0.97, 1.0], 'face': {'jaw': 0.0, 'lid': 0.45, 'cheeks': 0.5}}, toonDur=0.1), k(round(SNAP9 + 0.6, 3), toon={'face': {'jaw': 0.0, 'lid': 1.0, 'cheeks': 0.45}}, toonDur=0.05),   # a gulp, a blink
            k(round(SNAP9 + 0.7, 3), toon={'face': {'jaw': 0.0, 'lid': 0.45, 'cheeks': 0.45, 'gy': 0.6}}, toonDur=0.08), k(round(SNAP9 + 0.95, 3), toon={'sq': [1.0, 1.03, 1.0], 'face': {'jaw': 0.0, 'lid': 0.45, 'cheeks': 0.45, 'gy': 0.0}}, toonDur=0.2, toonEase='inOut'),   # a glance down at the cap, a breath
            k(round(SNAP9 + 1.06, 3), toon={'sq': [1.0, 1.03, 1.0], 'face': {'jaw': 0.0, 'lid': 1.0, 'cheeks': 0.45}}, toonDur=0.05), k(round(SNAP9 + 1.13, 3), toon={'sq': [1.0, 0.995, 1.0], 'face': {'jaw': 0.0, 'lid': 0.45, 'cheeks': 0.45}}, toonDur=0.08)]), until=SNAP9),   # (pass 3) a blink: the hold froze
        act('facteur', FACP, 90, 'stand', 'neutral', keys=[k(0.0, look=HEADIN),
            k(0.1, toon={'reach': {'L': [r(FACP[0] + 0.35), 1.45, r(FACP[2] + 0.12), 1, 0.05], 'R': [r(FACP[0] + 0.35), 1.45, r(FACP[2] - 0.12), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.15),
            k(IN9, toon={**PINF(HEADIN), 'reach': {'L': [r(HEADIN[0] - 0.05), 1.48, r(HEADIN[2] + 0.13), 1, 0.05], 'R': [r(HEADIN[0] - 0.05), 1.48, r(HEADIN[2] - 0.13), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.9, 0, 0, 1, None]}, 'face': {'lid': 0.4}}, toonDur=0.2, toonEase='inOut'),   # head first into his mouth...
            *[k(round(LIFT9 + 0.05 * i, 3), toon={**PINF(HEADIN), 'lay': [round(1.15 + 0.08 * (i % 2), 3), 0.0], **KICK(i), 'reach': {'L': [r(HEADIN[0] - 0.05), 1.48, r(HEADIN[2] + 0.13), 1, 0.05], 'R': [r(HEADIN[0] - 0.05), 1.48, r(HEADIN[2] - 0.13), 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}, toonDur=0.05) for i in range(6)],   # ...lifted off his feet, legs kicking...
            k(round(SNAP9 - 0.03, 3), toon={**PINF([r(HEADIN[0] + 0.1), 1.5, ME[2]]), 'lay': [1.3, 0.0], **KICK(1), 'sq': [0.8, 1.45, 0.8]}, toonDur=0.03, toonEase='in'),   # (final pass) stretched as he is sucked in...
            k(SNAP9, toon={**PINF([r(HEADIN[0] + 0.25), 1.5, ME[2]]), 'lay': [1.3, 0.0], **KICK(0), 'sq': [0.7, 1.7, 0.7]}, toonDur=0.04, toonEase='in'), k(round(SNAP9 + 0.07, 3), visible=False)])],   # ...SNAP: pulled in, legs last
        props=[BUS('bus9'), {**TONGUE('tong9', [[0.0, 1.0], [round(SNAP9 - 0.12, 3), 1.0], [round(SNAP9 - 0.02, 3), 0.02]]), 'keys': [k(round(SNAP9 + 0.01, 3), visible=False)]},   # (check stills) gone with the snap: rolled up on the pavement it was a red tin can   # the tongue slurped back in before the snap...
               P('box9', 'cardboardBox', on={'actor': 'facteur', 'hand': 'R', 'offset': [0.0, 0.0, 0.08]}, scale=0.45, keys=[k(IN9, visible=False)]),
               P('cap9', 'beanieHat', pos=[r(XCAV(1.6) - 0.15), 1.75, ME[2]], opts={'color': '#F2C230', 'bobble': False, 'boxy': [0.27, 0.12, 0.3]}, keys=[k(0.0, visible=False), k(SNAP9, visible=True), k(SNAP9, path=[[r(XCAV(1.6) - 0.35), 1.4, r(ME[2] + 0.2)], [r(XCAV(1.6) - 0.55), 0.6, ME[2]], [r(XCAV(1.6) - 0.7), 0.02, r(ME[2] + 0.15)]], dur=0.7, ease='out')]),   # (final pass) the shape of the cap he wore
               BURST('snap9', [r(ME[0] - 0.55), 2.15, r(ME[2] + 0.45)], SNAP9, 'CLAC !', 0.5)],   # (final pass) beside his head
        cams=[FC(0.0, [r(ME[0] - 1.9), 1.45, 2.1], [[ME[0], 2.4, ME[2]], [ME[0], 0.0, ME[2]], [r(FACP[0] - 0.6), 1.2, FACP[2]], [FACP[0], 0.0, FACP[2]], [r(ME[0] - 0.75), 2.45, ME[2]]], top=0.1, bottom=0.74, drift=(0.35, 0.05, -0.3))])   # (final pass) the snap on one angle, a push in over the shot (the cut at the snap hid it)   # (pass 3) a push-in at the snap: his head ~25 % of the frame   # (pass 2) three-quarters: the postman's dive across the frame, his face still painted on (in profile it was a blank box side)
st.cue('sfx:slideUp', 'S09', round(SNAP9 - 0.12, 3), 0.25); st.cue('clack', 'S09', SNAP9, 0.5); st.cue('sfx:gulp', 'S09', round(SNAP9 + 0.45, 3), 0.3)

# 10: with the postman inside. (pass 2) Three-quarters: a fist punches out his shirt beyond his outline at each knock, TOC ! on each punch; the fist
#     wanders between them; deadpan, he blinks
D10 = st.dur('S10'); KN10 = (0.36, 0.62, 0.96)
BULGE = [[0.0, 0.0, 0.2, 0.14], [0.32, 0.02, 0.26, 0.14], [0.36, 0.02, 0.26, 0.3], [0.46, 0.01, 0.22, 0.15], [0.58, -0.03, 0.14, 0.14], [0.62, -0.03, 0.14, 0.3], [0.72, -0.02, 0.16, 0.15],
         [0.92, 0.02, 0.24, 0.14], [0.96, 0.02, 0.24, 0.32], [1.06, 0.01, 0.22, 0.15], [1.4, 0.0, 0.18, 0.14]]   # (final pass) up the shirt between the lapels, travelling between the knocks
TOCAT = [[0.02, 0.26], [-0.03, 0.14], [0.02, 0.24]]                      # (final pass) where the fist punches out
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45, 'cheeks': 0.4}}, toonDur=0.0),
            *[x for i, t_ in enumerate(KN10) for x in (k(t_, toon={'sq': [0.95, 1.07, 0.95], 'bend': {'spine': [-0.14, 0, 0, 1, None]}, 'lay': [0.05 * (1 if i % 2 else -1), 0.0], 'face': {'lid': 0.3, 'cheeks': 0.3, 'brow': 0.3}}, toonDur=0.05, toonEase='out'),
                                                       k(round(t_ + 0.13, 3), toon={'face': {'lid': 0.45, 'cheeks': 0.3}}, toonDur=0.1, toonEase='inOut'),
                                                       k(t_, to=[ME[0], 0.07, ME[2]], dur=0.05, ease='out', face='keep'), k(round(t_ + 0.06, 3), to=ME, dur=0.07, ease='in', face='keep'))],   # (pass 3) each punch throws his belly out and hops him
            k(1.1, toon={'face': {'lid': 1.0, 'cheeks': 0.3}}, toonDur=0.06), k(1.22, toon={'face': {'lid': 0.45, 'cheeks': 0.3}}, toonDur=0.08)])],
        props=[BUS('bus10'), P('bul10', 'bellyBulge', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0, 0]}, opts={'r': 0.12, 'fist': True, 'color': '#F2F2EC', 'outline': 0.02, 'path': BULGE, 'size': [[0.0, 0.8], [0.36, 1.15], [0.46, 0.9], [0.62, 1.3], [0.72, 0.9], [0.96, 1.5], [1.06, 0.95]]}),   # (final pass) the white shirt pushed out, three knocks growing
               *[P(f'toc10{i}', 'hicBurst', on={'actor': 'mec', 'joint': 'torso', 'offset': [r(TOCAT[i][0] + (0.2 if TOCAT[i][0] >= 0 else -0.2)), r(TOCAT[i][1] + 0.02), 0.42], 'face': 'camera'}, opts={'at': [t_], 'w': [0.36, 0.42, 0.5][i], 'hold': 0.14, 'text': 'TOC !', 'inner': 0.78, 'fit': 0.56}) for i, t_ in enumerate(KN10)]],   # (pass 2) on each punch
        cams=[FC(0.0, [r(ME[0] - 1.5), 1.3, 1.25], [[ME[0], 2.25, ME[2]], [ME[0], 0.75, ME[2]], [r(ME[0] - 0.45), 1.4, ME[2]], [ME[0], 1.4, r(ME[2] - 0.45)]], top=0.32, bottom=0.74, drift=(0.1, 0.0, -0.04))])   # (pass 2) three-quarters: the fist out of his outline ((final pass) his head below the DEDANS band)
for t_ in KN10: st.cue('thud', 'S10', t_, 0.25)

# 11: he gets his mail from the inside. (pass 2) A letter pops straight up out of his lips like toast and hangs there five frames; he takes it by its
#     corner and reads it, his head down to it; his eyes come up to us, then his head; a slow blink; the bulge waves under his shirt
D11 = st.dur('S11'); OUT11 = 0.22; TAKE11 = 0.62
LIPS = [r(ME[0] + FX * 0.16), r(HEADY + 0.15), ME[2]]                     # (final pass) at his upper lip: half the letter over the dark open mouth reads as half in it
READ = [r(ME[0] - 0.4), 1.38, ME[2]]
RHOLD = lambda face: {'reach': {'R': [READ[0], READ[1], r(READ[2] - 0.12), 1, 0.05], 'L': [READ[0], READ[1], r(READ[2] + 0.12), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'pupil': 1.0, **face}}
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45, 'cheeks': 0.3, 'gy': 0.6}}, toonDur=0.0),
            k(round(OUT11 - 0.08, 3), toon={'face': {'lid': 0.45, 'cheeks': 0.2, 'gy': 0.6, 'pupil': 1.0, 'jaw': 0.6, 'jawLen': 0.42, 'jawBlock': 1.0, 'jawFwd': 0.0}}, toonDur=0.06),   # (pass 3) a slot opens in his mouth...
            k(round(TAKE11 + 0.05, 3), toon={'face': {'lid': 0.45, 'cheeks': 0.3, 'gy': 0.5, 'pupil': 1.0, 'jaw': 0.0, 'jawLen': 0.42, 'jawBlock': 1.0}}, toonDur=0.08),   # ...and shuts once the letter is taken
            k(round(TAKE11 - 0.2, 3), toon={'reach': {'R': [r(LIPS[0] - 0.06), r(LIPS[1] + 0.07), r(LIPS[2] - 0.05), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.45, 'cheeks': 0.3, 'gy': 0.5}}, toonDur=0.18, toonEase='inOut'),   # he takes it by its corner...
            k(round(TAKE11 + 0.15, 3), toon=RHOLD({'lid': 0.4, 'gy': 0.9, 'gx': 0.0}), toonDur=0.25, toonEase='inOut'), k(1.12, toon={**RHOLD({'lid': 0.4, 'gy': 0.85, 'gx': 0.15}), 'sq': [1.0, 1.025, 1.0]}, toonDur=0.25, toonEase='inOut'),   # (final pass) reading, eyes down on it; a breath (0.6 s froze)
            k(round(TAKE11 + 0.2, 3), look=[READ[0], READ[1], READ[2]]),   # ...and reads it, his head down to it...
            k(1.45, toon=RHOLD({'lid': 0.45, 'gy': -0.2}), toonDur=0.1), k(1.6, look='camera'),   # ...his eyes up to us first, then his head...
            k(1.95, toon=RHOLD({'lid': 1.0}), toonDur=0.12), k(2.17, toon=RHOLD({'lid': 0.45}), toonDur=0.16),   # ...a slow blink
            k(round(D11 - 0.24, 3), toon={**RHOLD({'lid': 0.4}), 'sq': [0.97, 1.04, 0.97], 'bend': {'spine': [-0.1, 0, 0, 1, None]}}, toonDur=0.05), k(round(D11 - 0.13, 3), toon=RHOLD({'lid': 0.45}), toonDur=0.1)])],   # (pass 3) one last knock jolts him
        props=[BUS('bus11'), P('let11', 'envelope', pos=[LIPS[0], r(LIPS[1] - 0.1), LIPS[2]], face='camera', scale=0.6, opts={'w': 0.2}, keys=[k(0.0, visible=False), k(round(OUT11 - 0.02, 3), visible=True),
               k(OUT11, to=[LIPS[0], LIPS[1], LIPS[2]], dur=0.12, ease='outBack'), k(OUT11, scale=1.0, dur=0.1, ease='outBack'),   # (final pass) up out of the slot like toast and held half out of his lips (over his head it read as a mail icon)...
               k(TAKE11, attach='mec', joint='handR', offset=[0.08, -0.06, 0.03], face='camera')]),   # ...into his hand by its corner, its face to us
               P('bul11', 'bellyBulge', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0, 0]}, opts={'r': 0.12, 'fist': True, 'path': [[0.0, 0.0, 0.1, 0.14], [2.6, 0.03, 0.1, 0.14]], 'size': [[0.0, 0.8], [1.6, 0.8], [1.75, 1.15], [1.9, 0.8], [2.05, 1.1], [2.2, 0.8], [round(D11 - 0.32, 3), 0.8], [round(D11 - 0.24, 3), 1.32], [round(D11 - 0.13, 3), 0.85]]})],   # (pass 3) one last knock
        cams=[FC(0.0, [r(ME[0] - 1.6), 1.6, 0.55], [[ME[0], 2.3, ME[2]], [ME[0], 0.95, ME[2]], [r(ME[0] - 0.45), 1.5, r(ME[2] + 0.35)]], top=0.16, bottom=0.68, drift=(0.15, 0.0, -0.05))])
st.cue('sfx:slideUp', 'S11', OUT11, 0.3); st.cue('sfx:ding', 'S11', round(OUT11 + 0.18, 3), 0.2); st.cue('sfx:paper', 'S11', TAKE11, 0.25); st.cue('thud', 'S11', round(D11 - 0.24, 3), 0.22)   # (pass 3) the last knock

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 1.1, 'mec', 'yawn'), ('S02', round(HIT2 + 0.05, 3), 'mec', 'clonk'), ('S03', 0.6, 'mec', 'lift'), ('S04', 0.9, 'maire', 'ribbon'), ('S05', 0.4, 'mec', 'queue'),
           ('S06', 0.5, 'mamie', 'slide'), ('S07', 0.5, 'facteur', 'post'), ('S08', 0.4, 'mec', 'letters'), ('S09', round(SNAP9 + 0.1, 3), 'mec', 'snap'), ('S10', 0.7, 'mec', 'bulge'),
           ('S11', 1.6, 'mec', 'mail')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S04', 0.8, 'sign4', 'toboggan')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S04', 'TOBOGGAN')
st.card('S10', 'DEDANS')

# (cycle 20) the extras get a fuller life in their holds (cast toon: holdLife, shift, breathe): at the defaults they stood frozen within 5 px
st.write("Le bâillement", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'maire': {'preset': 'politique', 'seed': 581, 'suit': '#5E636B', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.06}},   # (pass 2) grey: in navy he was the man's double
    # (final pass) the queue varied in silhouettes: they were near-clones of him (black hair, box head, one with his stubble)
    'q1': {'preset': 'tourist', 'seed': 582, 'hat': 'fedora', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}},
    'q2': {'preset': 'madame', 'seed': 583, 'suit': '#3E8E6E', 'hairColor': '#B8B8B8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}},
    'q3': {'preset': 'gamin', 'seed': 584, 'suit': '#C8642A', 'toon': {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}},
    'q4': {'preset': 'madame', 'seed': 587, 'suit': '#B0566A', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}},
    'q5': {'preset': 'fermier', 'seed': 588, 'hat': 'cap', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}},
    'mamie': {'preset': 'mamie', 'seed': 585, 'build': {'width': 0.9, 'headWidth': 1.25}},
    'facteur': {'preset': 'worker', 'seed': 586, 'suit': '#2E5AA8', 'hat': 'beanie', 'hatColor': '#F2C230', 'build': {'width': 1.0, 'headWidth': 1.2}},
})
