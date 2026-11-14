#!/usr/bin/env python3
"""La grimace (story 59, cycle 21 of the cartoon staging): this man pulled a face. The wind turned. He stayed like that. The town hall refuses his
identity photo. The carnival hired him as a mask. Yesterday the wind turned again. The whole town stayed in a grimace. Except him. The carnival fired
him: he is too scary.
Staging: on a Paris pavement he hooks his fingers in the corners of his mouth and pulls the face of the century (the mouth stretched wide, the tongue
out, the eyes crossed, one eye big, his head pulled wide, his ears out); cut to a weathervane on a roof: the iron rooster creaks, then whirls in a gust
of leaves; back on him the gust hits, he lets go: the face stays; he presses his cheeks back to normal, lets go: BOING, it springs back. At the town
hall the clerk holds his identity photo beside his face (the same grimace), looks twice, her head shoots up; she slams her big stamp on it: REFUSÉE.
In the carnival street a carnival boss in a party hat lights up at the sight of him and shakes his hand so hard the grimace flaps; on a float he
stands as its mask, his head blown up to a carnival big head, waving to the children. The weathervane again, the other way round: it unscrews and
takes off like a helicopter. In the carnival street the gust runs through the crowd and each face snaps into a grimace of its own, one after the
other. Except him: his tongue zips back in, his head springs back to normal, he blinks. The boss, grimacing, points him out of the carnival, his arm
stretching across the street; the grimacing children look at his plain face, scream, jump out of their skins and run; he stays alone, deadpan.
Natural look; cycle 21 tools: props_grimace.js (weathervane with roof, ghosts and take-off, carnivalFloat, grimacePhoto, leafGust)."""
from story_kit import *
import math

st = Story('grimace', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L04', 4), ('S06', 'L05', 0), ('S07', 'L05', 4),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L09', 0), ('S12', 'L09', 4)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)

STREET = {'eiffelStyle': 'v2', 'clear': [-4.0, 4.0], 'sky': ['#8CC4EA', '#C9E5F2']}   # no tree or lamp on the right pavement around him; (pass 2) the series' pastel sky
ME = [7.2, 0, 0.0]; RY = -90                                             # on the right pavement, facing the road (-X); his left is +Z
DEAD = {'lid': 0.45}
# his grimace: the mouth stretched wide, the tongue out and aside, the eyes crossed, one eye big and one small, one brow up and one down, big pupils
GH = {'expr': 'shocked', 'exprW': 1.0, 'cross': 1.0, 'pupilSize': 0.7, 'eyeL': 0.45, 'eyeR': 0.05, 'browL': 1.0, 'browR': -0.9, 'lid': 0.0,   # (pass 2) wide eyes, crossed pupils
      'mouth': 'teeth', 'mouthW': 1.0, 'mouthH': 0.9, 'mouthTilt': -8, 'tongue': 1.0, 'tongueLen': 0.3, 'tongueYaw': -0.55, 'tongueDip': 0.35}   # a mouth of teeth twice as wide, the tongue long and aside
GHEAD = [1.45, 0.82, 1.08]                                               # his head pulled wide with it ((stills 1) 1.28 hardly showed)
GF = lambda extra=None: {**GH, **(extra or {})}
BURST = lambda pid, pos, at_, text, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
POLE = {'L': [1.0, 0.25, -0.2], 'R': [-1.0, 0.25, -0.2]}                 # the elbows out to the sides
def PULL(k_, across=0.8):
    """his fingers hooked in the corners of his mouth, pulling them out (k_: 0 at the corners, 1 pulled wide)"""
    a = r(0.55 + (across - 0.55) * k_)                                       # (pass 2) outside the mouth: the hands covered its corners
    return {'touch': {'L': ['face', a, 0.2, 0.03, 1, 0.04, POLE['L']], 'R': ['face', -a, 0.2, 0.03, 1, 0.04, POLE['R']]}, 'hands': {'L': 'point', 'R': 'point'}}
# the other faces of the town, each its own
# (pass 2) every face of the town pushed as far as his: a wide mouth or a long tongue, eyes at odds, on its own painted base
G_BOSS = {'expr': 'angry', 'exprW': 0.8, 'mouth': 'teeth', 'mouthW': 0.9, 'mouthH': 0.6, 'eyeL': 0.8, 'lidR': 1.0, 'browL': 1.0, 'browR': -0.9, 'pupilSize': 0.6, 'tongue': 1.0, 'tongueLen': 0.2, 'tongueYaw': 0.6}
G_K1 = {'expr': 'shocked', 'exprW': 0.8, 'mouth': 'scream', 'mouthW': 0.6, 'cross': 1.0, 'tongue': 1.0, 'tongueLen': 0.18, 'tongueYaw': -0.6, 'brow': 0.9, 'pupilSize': 0.8}
G_W1 = {'expr': 'disgusted', 'exprW': 0.8, 'mouth': 'kiss', 'mouthW': 0.4, 'puff': 1.0, 'cheeks': 1.0, 'cross': 1.0, 'eyeL': 0.5, 'brow': -0.6, 'pupilSize': 0.6}
G_M1 = {'expr': 'shocked', 'exprW': 0.8, 'mouth': 'zigzag', 'mouthW': 0.8, 'mouthH': 0.6, 'mouthDx': 25, 'eyeR': 0.7, 'eyeL': -0.3, 'browTiltL': 25, 'browR': 0.9, 'pupilSize': 0.6}
G_MAM = {'expr': 'suspicious', 'exprW': 0.8, 'mouth': 'teeth', 'mouthW': 0.7, 'mouthTilt': 18, 'eye': 0.5, 'cross': 0.8, 'brow': 1.0, 'pupilSize': 0.4, 'tongue': 1.0, 'tongueLen': 0.15, 'tongueYaw': 0.5}
G_K2 = {'expr': 'scared', 'exprW': 0.8, 'mouth': 'scream', 'mouthTilt': 18, 'eyeL': -0.3, 'eyeR': 0.6, 'browTiltR': -20, 'pupilSize': 0.8}

# 1: the hook. A Paris pavement: deadpan, a squint, his fingers to the corners of his mouth: he pulls the face of the century (the mouth wide, the
#    tongue out, the eyes crossed, his head pulled wide, his ears out), and holds it, the tongue wagging
D1 = st.dur('S01'); PULL1 = 0.42
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.08, toon={'sq': [1.05, 0.93, 1.05], **PULL(0.0), 'touch': {'L': ['face', 0.32, 0.3, 0.14, 1, 0.04, POLE['L']], 'R': ['face', -0.32, 0.3, 0.14, 1, 0.04, POLE['R']]}, 'hands': {'L': 'point', 'R': 'point'},
                           'face': {'lid': 0.65, 'brow': -0.5, 'cheeks': 0.3}}, toonDur=0.16, toonEase='inOut'),   # a squint, a dip, his fingers up to his mouth...
            k(0.28, toon={**PULL(0.0), 'sq': [1.03, 0.96, 1.03], 'face': {'lid': 0.5, 'brow': -0.3, 'mouth': 'clench'}}, toonDur=0.1, toonEase='out'),   # ...hooked in its corners...
            k(PULL1, toon={**PULL(1.0), 'sq': [0.97, 1.06, 0.97], 'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.1, toonEase='outBack'),   # ...and PULLED
            *[k(r(PULL1 + 0.2 + 0.14 * i), toon={**PULL(1.0 if i % 2 else 0.94), 'sq': [0.97, 1.06, 0.97], 'scl': {'head': ([1.31, 0.84, 1.05] if i % 2 else [1.26, 0.88, 1.05])}, 'ears': (0.75 if i % 2 else 0.6),
                                            'face': GF({'tongueYaw': (0.2 if i % 2 else -0.45)})}, toonDur=0.12, toonEase='inOut') for i in range(7)]])],   # held, the tongue wagging, his head pulsing
        cams=[FC(0.0, [r(ME[0] - 1.25), 1.95, 0.3], [[ME[0], 2.38, ME[2]], [ME[0], 1.5, ME[2]], [r(ME[0] - 0.2), 1.9, r(ME[2] + 0.7)], [r(ME[0] - 0.2), 1.9, r(ME[2] - 0.7)]], top=0.14, bottom=0.6, drift=(0.08, 0.0, -0.03))])   # (pass 2) his head 30 % of the frame
st.cue('sfx:squeak', 'S01', 0.3, 0.2); st.cue('sfx:stretch', 'S01', PULL1, 0.35)

# 2: the wind turned. A weathervane on a slate roof against the sky: the iron rooster creaks, shudders, then whirls up in a gust of leaves
D2 = st.dur('S02')
WV = [0.0, 22.0, -12.0]                                                  # the roof ridge, high over the street: only the sky behind it
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('vane2', 'weathervane', pos=WV, opts={'roof': {'len': 3.2}, 'spin': [[0.0, 0.0], [0.15, 0.0], [0.35, 0.7], [0.8, 3.2]], 'wobble': [0.12], 'yaw0': 0.6}),
               P('leaf2', 'leafGust', pos=[r(WV[0] - 3.2), r(WV[1] - 0.6), r(WV[2] + 1.2)], scale=2.5, opts={'n': 22, 'w': 2.6, 'h': 1.0, 'd': 0.6, 'startAt': 0.25, 'dur': 0.85})],
        cams=[FC(0.0, [r(WV[0] - 1.3), r(WV[1] + 0.1), r(WV[2] + 2.2)], [[WV[0], r(WV[1] + 1.66), WV[2]], [r(WV[0] - 0.7), WV[1], WV[2]], [r(WV[0] + 0.7), WV[1], WV[2]], [WV[0], r(WV[1] - 0.35), r(WV[2] + 0.4)]],
                 top=0.16, bottom=0.74, drift=(0.12, 0.0, -0.08))])   # (stills 1) the vane the subject (the roof filled the frame)
st.cue('gust', 'S02', 0.1, 0.45, 1.1); st.cue('sfx:squeak', 'S02', 0.14, 0.3); st.cue('whoosh', 'S02', 0.4, 0.25, 0.7, 300, 1400)

# 3: he stayed like that. Closer: the gust hits him (leaves, his hair and tie blown flat); he lets go of his mouth: the face stays; he presses his cheeks
#    back to normal with both palms (his head squeezed narrow, his face plain), a hopeful beat; he lets go: BOING, it springs back, wobbling
D3 = st.dur('S03'); LET3 = 0.2; PRESS3 = 0.42; REL3 = 0.76
WIND3 = [-10.0, 1.0, 0.0]                                                 # from his left to his right
PRESS = lambda: {'touch': {'L': ['face', 0.44, 0.45, 0.02, 1, 0.02, [0.6, -0.8, 0.2]], 'R': ['face', -0.44, 0.45, 0.02, 1, 0.02, [-0.6, -0.8, 0.2]]}, 'hands': {'L': 'open', 'R': 'open'}}   # (pass 2) the elbows down
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**PULL(1.0), 'scl': {'head': GHEAD}, 'ears': 0.7, 'wind': WIND3, 'face': GF()}, toonDur=0.0),
            k(LET3, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'wind': WIND3, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': GF()}, toonDur=0.08, toonEase='out'),   # he lets go: it stays
            k(r(LET3 + 0.1), toon={'scl': {'head': [1.32, 0.84, 1.05]}, 'ears': 0.7, 'wind': WIND3, 'face': GF({'tongueYaw': 0.3})}, toonDur=0.06),   # (a shiver of the tongue)
            k(PRESS3, toon={**PRESS(), 'scl': {'head': [0.8, 1.14, 1.0]}, 'wind': [-3.0, 0.0, 0.0], 'face': {'lid': 0.45, 'cheeks': 0.7, 'mouth': 'pout'}}, toonDur=0.1, toonEase='inOut'),   # palms on his cheeks: plain again...
            k(r(PRESS3 + 0.14), toon={**PRESS(), 'scl': {'head': [0.82, 1.12, 1.0]}, 'face': {'lid': 0.35, 'cheeks': 0.7, 'brow': 0.5, 'mouth': 'pout'}}, toonDur=0.12),   # ...a hopeful beat...
            k(REL3, toon={'scl': {'head': [1.45, 0.76, 1.08]}, 'ears': 0.85, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [1.04, 0.95, 1.04], 'face': GF()}, toonDur=0.05, toonEase='out'),   # ...BOING: back, past it...
            k(r(REL3 + 0.09), toon={'scl': {'head': [1.18, 0.92, 1.03]}, 'ears': 0.6, 'face': GF({'tongueYaw': 0.35})}, toonDur=0.07),
            k(r(REL3 + 0.18), toon={'scl': {'head': [1.34, 0.83, 1.06]}, 'ears': 0.75, 'face': GF({'tongueYaw': -0.4})}, toonDur=0.08),
            k(r(REL3 + 0.3), toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.1)])],   # ...wobbling to a stop
        props=[P('leaf3', 'leafGust', pos=[r(ME[0] - 0.7), 0.4, r(ME[2] + 3.0)], ry=90, scale=1.6, opts={'n': 20, 'w': 4.0, 'h': 1.3, 'd': 0.8, 'startAt': 0.0, 'dur': 0.6})],
        cams=[FC(0.0, [r(ME[0] - 1.4), 1.85, -0.6], [[ME[0], 2.38, ME[2]], [ME[0], 1.35, ME[2]], [r(ME[0] - 0.3), 1.7, r(ME[2] + 0.6)], [r(ME[0] - 0.3), 1.7, r(ME[2] - 0.6)]], top=0.14, bottom=0.62, drift=(0.08, 0.0, 0.04))])   # (stills 1) closer
st.cue('gust', 'S03', 0.0, 0.3, 0.6); st.cue('sfx:squeak', 'S03', PRESS3, 0.2); st.cue('sfx:boing', 'S03', REL3, 0.4)

# 4: the town hall refuses... At the counter the clerk holds his identity photo up beside his face, at the end of her arm: the same grimace; her eyes
#    go to the photo, to him, to the photo, to him: a double take, her head shoots up
D4 = st.dur('S04')
OFFICE = {'title': 'MAIRIE', 'plate': False}                               # (pass 2) the ÉTAT CIVIL plate sat in the caption band
VIS = [0.0, 0, 0.0]; CLERK = [0.25, 0, -1.4]                             # him in front of the desk, the clerk behind it
PH4 = [0.32, 1.84, -0.4]                                                  # (pass 2) her hand under the photo: the photo itself beside his face, at its height; (stills 2) it sat at his collar: raised to his face
HOLD4 = lambda: {'reach': {'R': [PH4[0], r(PH4[1] - 0.15), PH4[2], 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}
st.shot('S04', 'mairie', setOpts=OFFICE, actors=[
        act('mec', VIS, -75, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.0),   # (check) cheated toward us: at 180 his face was in profile
            k(0.5, toon={'scl': {'head': [1.31, 0.84, 1.05]}, 'ears': 0.7, 'face': GF({'tongueYaw': 0.2})}, toonDur=0.12), k(0.8, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.12)]),
        act('agent', CLERK, -40, 'stand', 'neutral', keys=[k(0.0, look=[PH4[0], PH4[1], PH4[2]]), k(0.0, toon={**HOLD4(), 'face': {'lid': 0.4, 'gx': 0.4}}, toonDur=0.0),
            k(0.16, toon={**HOLD4(), 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.0, 0.18, 0, 1, None]}, 'face': {'lid': 0.35, 'gx': -0.6}}, toonDur=0.06), k(0.24, look=[VIS[0], 1.85, VIS[2]]),   # her eyes to him first, then her head...
            k(0.36, toon={**HOLD4(), 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.0, -0.18, 0, 1, None]}, 'face': {'lid': 0.3, 'gx': 0.6}}, toonDur=0.06), k(0.42, look=[PH4[0], PH4[1], PH4[2]]),   # ...back to the photo...
            k(0.54, toon={**HOLD4(), 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.0, 0.2, 0, 1, None]}, 'face': {'lid': 0.3, 'gx': -0.7}}, toonDur=0.05), k(0.58, look=[VIS[0], 1.85, VIS[2]]),   # ...to him again...
            k(0.64, toon={**HOLD4(), 'scl': {'head': [0.84, 1.42, 0.86]}, 'hairUp': 1.0, 'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.0, 'eye': 0.8, 'pupil': 0.45, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # ...the take: her head shoots up
            k(r(0.64 + 0.12), toon={**HOLD4(), 'scl': {'head': [0.94, 1.12, 0.95]}, 'hairUp': 0.8, 'face': {'lid': 0.0, 'eye': 0.6, 'pupil': 0.5, 'brow': 0.9, 'mouth': 'O'}}, toonDur=0.08),
            k(r(0.64 + 0.24), toon={**HOLD4(), 'scl': {'head': [1.0, 1.04, 1.0]}, 'hairUp': 0.6, 'face': {'lid': 0.1, 'eye': 0.5, 'pupil': 0.5, 'brow': 0.8, 'mouth': 'o'}}, toonDur=0.12)])],
        props=[P('photo4', 'grimacePhoto', on={'actor': 'agent', 'hand': 'R', 'offset': [0.0, 0.36, 0.05], 'face': 'camera'}, scale=4.6, opts={'face': {k_: v_ for k_, v_ in GH.items() if not k_.startswith('tongue')}})],   # (pass 2) his very face, held by its lower edge
        cams=[FC(0.0, [-2.2, 1.65, 0.6], [[VIS[0], 2.38, VIS[2]], [VIS[0], 1.3, VIS[2]], [VIS[0], 2.0, r(VIS[2] + 0.42)], [VIS[0], 2.0, r(VIS[2] - 0.42)], [CLERK[0], 2.55, CLERK[2]], [PH4[0], 2.4, PH4[2]], [PH4[0], 1.65, PH4[2]]], top=0.12, bottom=0.7, drift=(0.06, 0.0, -0.05))])   # (stills 2) his whole head in (cut by the right edge)   # (stills 1) his face and the photo side by side to us, her face three-quarters behind
st.cue('sfx:paper', 'S04', 0.05, 0.15); st.cue('sfx:gasp', 'S04', 0.64, 0.3)

# 5: ...his identity photo. Low over the desk: the photo lies there, his grimace on it, him behind it pulling the same face; the clerk's big stamp
#    rises (her arm stretched up), comes down: BAM, the desk's papers jump, his tongue flaps; REFUSÉE on the photo
D5 = st.dur('S05'); HIT5 = 0.42
PH5 = [0.0, 0.836, -0.85]                                                 # the photo flat on the desk
STK = 0.8                                                                 # the stamp's scale: its face 0.336 m under the knob
SUP = [0.0, 1.32, -0.9]; STOP5 = [0.0, 1.52, -0.98]; SDOWN = [0.0, r(PH5[1] + 0.42 * STK + 0.004), PH5[2]]
SREACH = lambda p_: {'reach': {'R': [p_[0], p_[1], p_[2], 1, 0.05]}, 'hands': {'R': 'grip'}}
st.shot('S05', 'mairie', setOpts=OFFICE, actors=[
        act('mec', VIS, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[PH5[0], 0.9, PH5[2]]), k(0.0, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.0),
            k(HIT5, toon={'scl': {'head': [1.36, 0.8, 1.07]}, 'sq': [1.04, 0.95, 1.04], 'ears': 0.9, 'face': GF({'tongueYaw': 0.6})}, toonDur=0.04, toonEase='out'),   # BAM: the jolt, his tongue flaps...
            k(r(HIT5 + 0.1), toon={'scl': {'head': [1.22, 0.9, 1.04]}, 'ears': 0.6, 'face': GF({'tongueYaw': -0.5})}, toonDur=0.08), k(r(HIT5 + 0.22), toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF({'tongueYaw': 0.15})}, toonDur=0.1)]),
        act('agent', CLERK, 0, 'stand', 'determined', keys=[k(0.0, look=[PH5[0], PH5[1], PH5[2]]), k(0.0, toon={**SREACH(SUP), 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'brow': -0.6}}, toonDur=0.0),
            k(0.06, toon={**SREACH(STOP5), 'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'sq': [0.96, 1.06, 0.96], 'face': {'lid': 0.6, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.22, toonEase='inOut'),   # the stamp up high, on her toes...
            k(r(HIT5 - 0.06), toon={**SREACH(SDOWN), 'bend': {'spine': [0.55, 0, 0, 1, None]}, 'sq': [1.05, 0.94, 1.05], 'face': {'lid': 0.5, 'brow': -1.0, 'mouth': 'clench'}}, toonDur=0.06, toonEase='in'),   # ...BAM
            k(r(HIT5 + 0.2), toon={**SREACH([0.0, 1.38, -0.95]), 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'brow': 0.3, 'mouth': 'smirk'}}, toonDur=0.16, toonEase='out')])],   # ...and up: done
        props=[P('photo5', 'grimacePhoto', pos=PH5, rot=[round(-PI / 2, 4), 0, 0], scale=2.6, opts={'face': {k_: v_ for k_, v_ in GH.items() if not k_.startswith('tongue')}}, keys=[k(r(HIT5 + 0.03), visible=False)]),
               P('photo5b', 'grimacePhoto', pos=PH5, rot=[round(-PI / 2, 4), 0, 0], scale=2.6, opts={'face': {k_: v_ for k_, v_ in GH.items() if not k_.startswith('tongue')}, 'stamp': 'REFUSÉE'}, keys=[k(0.0, visible=False), k(r(HIT5 + 0.03), visible=True)]),   # (pass 2) the imprint on the photo
               P('stamp5', 'bigStamp', pos=SUP, scale=STK, keys=[k(0.06, to=STOP5, dur=0.22, ease='inOut'), k(r(HIT5 - 0.06), to=SDOWN, dur=0.06, ease='in'),
                                                                 k(r(HIT5 + 0.2), to=[0.0, 1.38, -0.95], dur=0.16, ease='out')]),
               # (pass 2) no stampPop: its mark lay under the photo
               P('pap5', 'paperSheet', pos=[0.55, 0.83, -0.72], rot=[round(-PI / 2, 4), 0, 0.3], opts={'w': 0.3, 'h': 0.4}, keys=[k(HIT5, to=[0.57, 0.98, -0.72], dur=0.06, ease='out'), k(r(HIT5 + 0.07), to=[0.58, 0.83, -0.71], dur=0.1, ease='in')])],   # the desk's papers jump
        fx=[{'type': 'shake', 'at': HIT5, 'dur': 0.15, 'amount': 0.012}],
        cams=[FC(0.0, [0.3, 2.05, -0.2], [[0.19, 0.836, -0.64], [-0.19, 0.836, -1.06], [0.19, 0.836, -1.06], [-0.19, 0.836, -0.64], [STOP5[0], 1.56, STOP5[2]]], top=0.08, bottom=0.88, level=False)])   # (stills 1) an insert from above: the photo big, the stamp coming down into it
st.cue('clack', 'S05', HIT5, 0.5); st.cue('sfx:thud', 'S05', HIT5, 0.4)

# 6: the carnival hired him. The carnival street (garlands over it, balloons): the carnival boss in a party hat sees his face and lights up (his eyes
#    huge), grabs his hand and pumps it: the shake ripples up the man's arm, his body jiggles, the grimace flaps; confetti
D6 = st.dur('S06'); GRAB6 = 0.28
CARN = {**STREET, 'eiffel': False}                                       # (pass 2) no tower stump behind the heads
MC = [-0.5, 0, 0.0]; BOSS = [0.55, 0, 0.15]
HS = [0.03, 1.05, 0.38]                                                   # where the hands meet
DECOR = lambda sid, z0=0.0: [P(f'ban{sid}', 'carnivalBanner', pos=[0.0, 3.6, r(z0 - 4.0)], opts={'w': 4.6, 'h': 0.85, 'span': 15}),   # (pass 2) the institution named
                             P(f'bunA{sid}', 'bunting', pos=[0.0, 4.6, r(z0 - 2.5)], opts={'len': 14, 'sag': 0.6, 'n': 22}), P(f'bunB{sid}', 'bunting', pos=[0.0, 5.0, r(z0 - 7.5)], opts={'len': 14, 'sag': 0.7, 'n': 22}),
                             P(f'bunC{sid}', 'bunting', pos=[0.0, 5.2, r(z0 - 13.0)], opts={'len': 14, 'sag': 0.7, 'n': 22}), P(f'bal{sid}', 'balloonBunch', pos=[2.6, 1.0, r(z0 - 1.6)], opts={'n': 7, 'len': 1.3})]
SHAKE = lambda i: {'reach': {'R': [HS[0], r(HS[1] + (0.12 if i % 2 else -0.12)), HS[2], 1, 0.05]}, 'hands': {'R': 'grip'}}
st.shot('S06', 'parisStreet', setOpts=CARN, actors=[
        act('mec', MC, 40, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [BOSS[0], 1.8, BOSS[2]], 'cheat': 0.5}), k(0.0, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.0),
            *[k(r(GRAB6 + 0.12 * i), toon={**SHAKE(i), 'scl': {'head': ([1.34, 0.82, 1.06] if i % 2 else [1.22, 0.9, 1.03])}, 'ears': (0.9 if i % 2 else 0.5), 'sq': ([1.03, 0.96, 1.03] if i % 2 else [0.97, 1.04, 0.97]),
                                           'wave': {'armR': [0.07, 1.5, r(0.5 * i), 0, 0.0], 'spine': [0.03, 1.0, r(0.5 * i), 1, 0.0]}, 'bend': {'neck': [(0.12 if i % 2 else -0.08), 0, 0, 1, None]},
                                           'face': GF({'tongueYaw': (0.55 if i % 2 else -0.5)})}, toonDur=0.08, toonEase='inOut') for i in range(8)]]),   # the shake ripples up his arm, the grimace flaps
        act('patron', BOSS, -35, 'stand', 'happy', keys=[k(0.0, look={'point': [MC[0], 1.8, MC[2]], 'cheat': 0.6}),   # (pass 2) three-quarters to us: his face lighting up was turned away
            k(0.0, toon={'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.3, 'mouth': 'o'}}, toonDur=0.0),
            k(0.06, toon={'sq': [0.94, 1.09, 0.94], 'hairUp': 0.6, 'face': {'lid': 0.0, 'eye': 0.6, 'pupil': 1.5, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.06, toonEase='out'),   # he sees the face: his eyes light up...
            *[k(r(GRAB6 + 0.12 * i), toon={**SHAKE(i), 'sq': ([1.02, 0.98, 1.02] if i % 2 else [0.98, 1.03, 0.98]), 'face': {'lid': 0.1, 'eye': 0.3, 'pupil': 1.3, 'brow': 0.8, 'mouth': 'bigsmile'}}, toonDur=0.08, toonEase='inOut') for i in range(8)]])],   # ...and pumps his hand
        props=[*DECOR('6'), P('cf6a', 'confetti', pos=[HS[0], 1.3, HS[2]], opts={'n': 26, 'at': GRAB6, 'dur': 0.9, 'color': '#F5C33B', 's': 1.5, 'fall': 1.2, 'seed': 3}),
               P('cf6b', 'confetti', pos=[HS[0], 1.3, HS[2]], opts={'n': 26, 'at': GRAB6, 'dur': 0.9, 'color': '#E8463A', 's': 1.5, 'fall': 1.2, 'seed': 8}),
               P('cf6c', 'confetti', pos=[HS[0], 1.3, HS[2]], opts={'n': 26, 'at': GRAB6, 'dur': 0.9, 'color': '#3A9BDC', 's': 1.5, 'fall': 1.2, 'seed': 13})],
        cams=[FC(0.0, [0.45, 1.65, 2.6], [[MC[0], 2.38, MC[2]], [BOSS[0], 2.6, BOSS[2]], [MC[0], 0.85, MC[2]], [BOSS[0], 0.85, BOSS[2]], [HS[0], HS[1], HS[2]]], top=0.14, bottom=0.7, drift=(-0.08, 0.0, -0.1))])   # (stills 1) a medium two-shot
st.cue('sfx:fanfare', 'S06', 0.12, 0.18); st.cue('sfx:pop', 'S06', GRAB6, 0.25)

# 7: as a mask. A carnival float rolls in: he stands at its front as its mask, his head blown up to a carnival big head, bobbing, waving to the children
#    cheering at its foot; confetti
D7 = st.dur('S07')
FL0 = [0.0, 0, -1.7]; FL1 = [0.0, 0, -1.25]; DECK = 0.79
BIGH = 2.55
WAVE7 = lambda i: {'reach': {'R': [r(FL0[0] - (0.75 if i % 2 else 0.2)), r(DECK + 2.0), r(FL0[2] + 0.3), 1, 0.05]}, 'hands': {'R': 'open'}}   # (pass 2) a big wave side to side (parked at his temple it read as a salute)
KID7 = lambda i, s_: {'reach': {'L': [0.0, 2.0, 0.0, 0, 0.05]}, 'sq': ([0.95, 1.07, 0.95] if (i + s_) % 2 else [1.03, 0.96, 1.03]), 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.7}}
st.shot('S07', 'parisStreet', setOpts=CARN, actors=[
        act('mec', [FL0[0], DECK, FL0[2]], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.0),
            k(0.0, to=[FL1[0], DECK, FL1[2]], dur=D7, clip='stand', then='stand', ease='linear', face='keep'),
            k(0.16, toon={**WAVE7(0), 'scl': {'head': [2.8, 2.8, 2.8]}, 'sq': [0.95, 0.93, 0.95], 'ears': 0.9, 'face': GF()}, toonDur=0.26, toonEase='out'),   # (pass 2) the normal head five frames, then it inflates over eight...
            k(0.44, toon={**WAVE7(1), 'scl': {'head': [2.35, 2.45, 2.4]}, 'sq': [0.96, 0.94, 0.96], 'ears': 0.8, 'face': GF()}, toonDur=0.1, toonEase='inOut'),   # ...past it, wobbling down to 2.5
            *[k(r(0.56 + 0.12 * i), toon={**WAVE7(i), 'scl': {'head': ([r(BIGH * 1.03), r(BIGH * 0.97), BIGH] if i % 2 else [r(BIGH * 0.97), r(BIGH * 1.03), BIGH])}, 'sq': [0.96, 0.94, 0.96], 'ears': 0.8,
                                       'face': GF({'tongueYaw': (0.3 if i % 2 else -0.35)})}, toonDur=0.13, toonEase='inOut') for i in range(3)]]),   # bobbing with the float, waving like a mascot
        act('k1', [-0.95, 0, -0.35], 160, 'stand', 'happy', keys=[k(0.0, look=[FL0[0], 2.6, FL0[2]]), *[k(r(0.04 + 0.14 * i), toon={**KID7(i, 0), 'reach': {'L': [-1.05, 1.75, -0.45, 1, 0.05], 'R': [-0.8, 1.8, -0.5, 1, 0.05]}}, toonDur=0.12) for i in range(6)]]),
        act('k2', [0.95, 0, -0.4], -160, 'stand', 'happy', keys=[k(0.0, look=[FL0[0], 2.6, FL0[2]]), *[k(r(0.1 + 0.14 * i), toon={**KID7(i, 1), 'reach': {'L': [1.05, 1.75, -0.5, 1, 0.05], 'R': [0.8, 1.8, -0.55, 1, 0.05]}}, toonDur=0.12) for i in range(6)]])],
        props=[*DECOR('7'), P('float7', 'carnivalFloat', pos=FL0, opts={'w': 2.6, 'd': 1.4, 'h': 0.75}, keys=[k(0.0, to=FL1, dur=D7, ease='linear')]),
               *[P(f'cf7{c_}', 'confetti', pos=[r(-1.4 + 1.4 * i) if i != 1 else 1.6, 3.6, -1.0], opts={'n': 22, 'at': 0.0, 'dur': 1.0, 'color': c_, 's': 1.4, 'fall': 2.6, 'seed': 4 + i}) for i, c_ in enumerate(['#F5C33B', '#E8463A', '#C255C8'])]],
        cams=[FC(0.0, [0.4, 0.75, 3.4], [[FL0[0], 3.85, FL0[2]], [-1.3, 0.0, r(FL0[2] + 0.7)], [1.3, 0.0, r(FL0[2] + 0.7)], [-0.95, 1.5, -0.35], [0.95, 1.5, -0.4]], top=0.1, bottom=0.82, drift=(0.0, 0.05, -0.15))])
st.cue('sfx:stretch', 'S07', 0.16, 0.3); st.cue('sfx:pop', 'S07', 0.42, 0.3); st.cue('sfx:tada', 'S07', 0.12, 0.18)

# 8: yesterday the wind turned again. The weathervane from the other side (a garland on the roof now): the rooster whirls the other way, faster and
#    faster, its rod unscrews and the whole vane takes off like a helicopter out of the frame; leaves and a party hat blown past
D8 = st.dur('S08'); LIFT8 = 0.5                                             # (pass 2) the repeat whirl short: it unscrews sooner
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('vane8', 'weathervane', pos=WV, opts={'roof': {'len': 3.2}, 'spin': [[0.0, 0.0], [0.12, -1.5], [0.45, -4.0], [1.9, -4.6]], 'wobble': [0.08], 'yaw0': 2.2, 'lift': [LIFT8, 0.45, 0.6, 0.32, 30.0]}),
               P('bun8', 'bunting', pos=[r(WV[0] + 0.1), r(WV[1] + 0.32), r(WV[2] + 0.2)], opts={'len': 3.0, 'sag': 0.25, 'n': 8}),
               P('leaf8', 'leafGust', pos=[r(WV[0] - 3.4), r(WV[1] - 0.8), r(WV[2] + 1.4)], scale=2.5, opts={'n': 26, 'w': 2.8, 'h': 1.2, 'd': 0.7, 'startAt': 0.2, 'dur': 1.2}),
               P('hat8', 'partyHat', pos=[r(WV[0] - 3.2), r(WV[1] - 0.5), r(WV[2] + 1.0)], scale=2.0, keys=[k(0.3, to=[r(WV[0] + 3.4), r(WV[1] + 0.9), r(WV[2] + 1.0)], dur=1.0, ease='inOut'), k(0.3, rotTo=[3.0, 2.0, 7.0], dur=1.0)])],
        cams=[FC(0.0, [r(WV[0] + 1.4), r(WV[1] + 0.05), r(WV[2] + 2.3)], [[WV[0], r(WV[1] + 2.0), WV[2]], [r(WV[0] - 0.8), WV[1], WV[2]], [r(WV[0] + 0.8), WV[1], WV[2]], [WV[0], r(WV[1] - 0.35), r(WV[2] + 0.4)]],
                 top=0.1, bottom=0.76, drift=(-0.12, 0.7, -0.08))])   # (stills 1) closer, room over it for the take-off; (pass 2) rising with it
st.cue('gust', 'S08', 0.05, 0.5, 1.8); st.cue('sfx:squeak', 'S08', 0.1, 0.3); st.cue('whoosh', 'S08', 0.45, 0.3, 0.9, 250, 1300); st.cue('sfx:twang', 'S08', LIFT8, 0.3); st.cue('sfx:zip', 'S08', r(LIFT8 + 0.8), 0.35)

# 9: the whole town stayed in a grimace. (pass 2) A medium close-up of three carnival-goers cheering, arms up, more behind them; the gust runs through
#    them from left to right (hair, hats and ties whipped one after another, leaves); each face snaps into a grimace of its own as it passes, the head
#    squashed four frames, overshooting, set wide, the arms dropping
D9 = st.dur('S09')
TOWN = [('patron', [-0.62, 0, 0.35], 14, G_BOSS, 'happy'), ('w1', [0.0, 0, 0.15], 0, G_W1, 'happy'), ('mamie', [0.6, 0, 0.4], -14, G_MAM, 'happy'),
        ('k1', [-1.5, 0, -1.6], 10, G_K1, 'happy'), ('m1', [1.5, 0, -1.7], -10, G_M1, 'happy')]   # three big faces, two behind
SNAP9 = [0.42, 0.62, 0.82, 1.0, 1.12]
CHEER = lambda p_: {'reach': {'L': [r(p_[0] + 0.32), 2.25, r(p_[2] + 0.1), 1, 0.05], 'R': [r(p_[0] - 0.32), 2.25, r(p_[2] + 0.1), 1, 0.05]}, 'hands': {'L': 'open', 'R': 'open'}}
def SNAPKEYS(ts, g_, i, p_):
    wind = {'wind': [12.0, 1.5, 0.0], 'hairUp': 0.5}
    return [k(0.0, toon={**CHEER(p_), 'sq': [1.0, 1.02, 1.0], 'face': {'mouth': 'bigsmile', 'lid': 0.1}}, toonDur=0.0),
            k(r(0.06 + 0.05 * i), toon={**CHEER(p_), 'sq': [0.98, 1.04, 0.98], 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.5}}, toonDur=0.15, toonEase='inOut'),   # cheering, a bounce
            k(r(ts - 0.06), toon={**CHEER(p_), **wind, 'face': {'mouth': 'bigsmile', 'lid': 0.3, 'brow': 0.6}}, toonDur=0.05),   # the gust reaches him: hair and tie whipped...
            k(ts, toon={**wind, 'scl': {'head': [1.38, 0.7, 1.15]}, 'sq': [1.06, 0.92, 1.06], 'ears': 0.8, 'face': g_}, toonDur=0.04, toonEase='out'),   # ...CLAC: the face snaps, the head squashed, the arms drop...
            k(r(ts + 0.13), toon={**wind, 'scl': {'head': [1.36, 0.72, 1.14]}, 'ears': 0.8, 'face': g_}, toonDur=0.1),   # ...held four frames...
            k(r(ts + 0.2), toon={'scl': {'head': [0.9, 1.16, 0.95]}, 'ears': 0.4, 'face': g_}, toonDur=0.06),   # ...overshooting tall...
            k(r(ts + 0.3), toon={'scl': {'head': [1.22, 0.86, 1.08]}, 'face': g_}, toonDur=0.08), k(r(ts + 0.5), toon={'scl': {'head': [1.2, 0.87, 1.07]}, 'sq': [1.0, 1.015, 1.0], 'face': g_}, toonDur=0.25, toonEase='inOut')]   # ...and set wide
st.shot('S09', 'parisStreet', setOpts=CARN, actors=[
        act(n_, p_, ry_, 'stand', ex_, keys=[k(0.0, look='camera'), *SNAPKEYS(SNAP9[i], g_, i, p_)]) for i, (n_, p_, ry_, g_, ex_) in enumerate(TOWN)],
        props=[*DECOR('9'), P('leaf9', 'leafGust', pos=[-2.4, 0.6, 1.0], scale=1.3, opts={'n': 34, 'w': 3.8, 'h': 1.8, 'd': 1.2, 'startAt': 0.3, 'dur': 1.0})],
        cams=[FC(0.0, [0.0, 1.85, 2.3], [[-0.62, 2.5, 0.35], [0.6, 2.2, 0.4], [-0.95, 1.9, 0.35], [0.95, 1.9, 0.4], [0.0, 1.45, 0.15]], top=0.16, bottom=0.6, drift=(0.0, 0.0, -0.08))])   # (pass 2) three faces each a quarter of the frame
st.cue('gust', 'S09', 0.25, 0.4, 1.2)
for t_ in SNAP9[:3]: st.cue('sfx:pop', 'S09', t_, 0.3)

# 10: except him. (pass 2) Tight between two extreme grimaces: the gust reaches him: his tongue zips back in, his head springs back to its size, his
#     eyes uncross: his plain deadpan face; a blink
D10 = st.dur('S10'); BACK10 = 0.1
st.shot('S10', 'parisStreet', setOpts=CARN, actors=[
        act('mec', [0.0, 0, 0.0], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.0),
            k(BACK10, toon={'scl': {'head': [0.86, 1.14, 0.95]}, 'ears': 0.0, 'wind': [10.0, 1.0, 0.0], 'face': {'lid': 0.2, 'tongue': 0.0, 'tongueLen': 0.3, 'pupilSize': 0.4}}, toonDur=0.06, toonEase='out'),   # ZIP: it all springs back...
            k(r(BACK10 + 0.1), toon={'scl': {'head': [1.06, 0.95, 1.02]}, 'face': {'lid': 0.35}}, toonDur=0.08), k(r(BACK10 + 0.2), toon={'scl': {'head': [1.0, 1.0, 1.0]}, 'face': DEAD}, toonDur=0.1),   # ...wobbling to his plain face
            k(0.58, toon={'face': {'lid': 1.0}}, toonDur=0.05), k(0.66, toon={'face': DEAD}, toonDur=0.08)]),   # a blink
        act('patron', [-0.48, 0, -0.4], 20, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': [1.2, 0.87, 1.07]}, 'face': G_BOSS}, toonDur=0.0), k(0.3, toon={'scl': {'head': [1.22, 0.85, 1.07]}, 'sq': [1.0, 1.02, 1.0], 'face': G_BOSS}, toonDur=0.3, toonEase='inOut')]),
        act('mamie', [0.5, 0, -0.35], -20, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': [1.2, 0.87, 1.07]}, 'face': G_MAM}, toonDur=0.0), k(0.2, toon={'scl': {'head': [1.18, 0.88, 1.07]}, 'sq': [1.0, 1.02, 1.0], 'face': G_MAM}, toonDur=0.3, toonEase='inOut')])],
        props=[*DECOR('10'), P('leaf10', 'leafGust', pos=[-2.0, 1.6, -1.2], scale=1.3, opts={'n': 16, 'w': 3.6, 'h': 1.2, 'd': 0.6, 'startAt': 0.0, 'dur': 0.5})],   # (stills 2) behind the heads: a leaf crossed his face on the beat
        cams=[FC(0.0, [0.05, 1.95, 1.5], [[0.0, 2.42, 0.0], [0.0, 1.5, 0.0], [-0.76, 2.2, -0.4], [0.78, 2.15, -0.35]], top=0.16, bottom=0.66, drift=(0.0, 0.0, -0.06))])   # (stills 2) his head a third of the frame, the two grimaces cut by its edges (his head was as small as theirs on « Sauf lui »); (stills 3) their whole faces in: the boss's was out of frame
st.cue('sfx:zip', 'S10', r(BACK10 - 0.02), 0.35); st.cue('sfx:pop', 'S10', BACK10, 0.2)

# 11: the carnival fired him. (pass 2) The boss beside him, both three-quarters to us: grimacing, he cocks his arm and flings it out away from the man,
#     the finger pointing down the street inside the frame, a flick, an overshoot and a settle, a tremble in the hold; the man's eyes go along the arm
#     first, then his head, his face still toward us
D11 = st.dur('S11'); PT11 = 0.32
MC11 = [0.4, 0, 0.05]; BOSS11 = [-0.5, 0, -0.1]
OUTPT = [-1.7, 2.15, 0.35]                                                 # where the finger points: out of the carnival, down the street, in the frame
PTK = lambda x_, y_, hand='point': {'reach': {'R': [r(x_), r(y_), OUTPT[2], 1, 0.08], 'L': [r(BOSS11[0] + 0.25), 1.0, r(BOSS11[2] + 0.12), 1, 0.05]}, 'hands': {'R': hand, 'L': 'fist'}}   # his other fist on his hip
st.shot('S11', 'parisStreet', setOpts=CARN, actors=[
        act('mec', MC11, -20, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [BOSS11[0], 1.8, BOSS11[2]], 'cheat': 0.6}), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(r(PT11 + 0.06), toon={'face': {'lid': 0.4, 'gx': -0.9, 'pupilSize': 0.3}}, toonDur=0.06), k(r(PT11 + 0.22), look={'point': OUTPT, 'cheat': 0.6}),   # his eyes along the arm first, then his head, his face kept to us
            k(0.95, toon={'face': {'lid': 1.0, 'gx': -0.6}}, toonDur=0.05), k(1.03, toon={'face': {'lid': 0.45, 'gx': -0.4}}, toonDur=0.08)]),
        act('patron', BOSS11, 25, 'stand', 'determined', keys=[k(0.0, look={'point': [MC11[0], 1.8, MC11[2]], 'cheat': 0.6}), k(0.0, toon={'scl': {'head': [1.2, 0.87, 1.07]}, 'face': G_BOSS}, toonDur=0.0),
            k(0.08, toon={**PTK(r(BOSS11[0] + 0.3), 1.55, 'fist'), 'scl': {'head': [1.2, 0.87, 1.07]}, 'bend': {'spine': [-0.15, 0, -0.12, 1, None]}, 'sq': [1.04, 0.95, 1.04], 'face': G_BOSS}, toonDur=0.15, toonEase='inOut'),   # the arm cocked across...
            k(PT11, toon={**PTK(OUTPT[0] - 0.22, OUTPT[1] + 0.06), 'scl': {'head': [1.2, 0.87, 1.07]}, 'bend': {'spine': [0.08, 0, 0.1, 1, None]}, 'sq': [0.97, 1.05, 0.97], 'face': G_BOSS}, toonDur=0.07, toonEase='out'),   # ...OUT, past the point...
            k(r(PT11 + 0.1), toon={**PTK(OUTPT[0] + 0.06, OUTPT[1] - 0.02), 'scl': {'head': [1.2, 0.87, 1.07]}, 'face': G_BOSS}, toonDur=0.08), k(r(PT11 + 0.2), look={'point': OUTPT, 'cheat': 0.5}),   # ...back...
            *[k(r(PT11 + 0.2 + 0.08 * j), toon={**PTK(OUTPT[0] + (0.015 if j % 2 else -0.015), OUTPT[1] + (0.01 if j % 2 else -0.01)), 'scl': {'head': [1.2, 0.87, 1.07]}, 'sq': [1.0, 1.01 if j % 2 else 1.0, 1.0], 'face': G_BOSS}, toonDur=0.07) for j in range(11)]])],   # ...and held, trembling
        props=[*DECOR('11')],
        cams=[FC(0.0, [-0.2, 1.75, 2.9], [[MC11[0], 2.38, MC11[2]], [BOSS11[0], 2.62, BOSS11[2]], [MC11[0], 1.0, MC11[2]], [BOSS11[0], 1.0, BOSS11[2]], [r(OUTPT[0] - 0.12), r(OUTPT[1] + 0.12), OUTPT[2]], [r(OUTPT[0] - 0.12), r(OUTPT[1] - 0.15), OUTPT[2]]], top=0.14, bottom=0.68, drift=(-0.05, 0.0, -0.06))])   # (pass 2) the pointing hand in the frame
st.cue('sfx:stretch', 'S11', PT11, 0.3); st.cue('sfx:whistle', 'S11', r(PT11 + 0.02), 0.15)

# 12: he is too scary. (pass 2) Close on his plain face turning to the children (the reveal); the grimacing children and the mamie, three-quarters to
#     us with him at the frame's edge, see it: their eyes, then their heads snap to him, a squash of fright, and they jump out of their skins (hang time,
#     hair on end, the mamie's cap flying off for good, the kid's eyes out on stalks), drop and run off; he stays alone; closer: his eyes come to us,
#     a slow blink
D12 = st.dur('S12'); SEE12 = 0.5; JUMP12 = 0.6; DROP12 = 0.84; RUN12 = 1.0; CUT12 = 1.55; REV12 = 0.4
MC12 = [-0.9, 0, 0.2]
CROWD = [('k1', [0.4, 0, 0.0], -70, G_K1, {'pop': 0.8, 'popLen': 0.22}), ('w1', [1.2, 0, -0.55], -60, G_W1, {}), ('mamie', [1.0, 0, 0.6], -80, G_MAM, {}), ('k2', [2.0, 0, 0.1], -70, G_K2, {})]
def FRIGHT(i, p_, g_, extra):
    sc = {**g_, 'mouth': 'scream', 'lid': 0.0, 'brow': 1.0, **extra}
    up = [p_[0], 0.62, p_[2]]
    run = [r(p_[0] + 4.5), 0, r(p_[2] - 1.5 + 0.8 * i)]
    hat = {'hat': [3.6, 2.2, 7.0]} if i == 2 else {}   # (pass 2) the cap flies up out of the frame and stays gone (it came back on her head)
    return [k(0.0, look=[1.0, 1.6, 3.0]), k(0.0, toon={'face': {**g_, 'gx': 0.3}}, toonDur=0.0),
            k(r(REV12 + 0.0), toon={'face': {**g_, 'gx': -0.8}}, toonDur=0.05), k(r(REV12 + 0.06), look=[MC12[0], 1.8, MC12[2]]),   # (pass 2) their eyes, then their heads, snap to him
            k(r(SEE12 - 0.06), toon={'sq': [1.1, 0.88, 1.1], 'face': {**g_, 'lid': 0.0, 'brow': 0.8}}, toonDur=0.06, toonEase='in'),   # a squash of fright...
            k(JUMP12, to=up, dur=0.12, ease='out', face='keep'), k(DROP12, to=p_, dur=0.1, ease='in', face='keep'),   # ...up out of their skins, a hang, down...
            k(JUMP12, toon={'sq': [0.84, 1.26, 0.84], 'hairUp': 1.0, **hat, 'reach': {'L': [r(p_[0] + 0.2), 2.3, r(p_[2] + 0.3), 1, 0.05], 'R': [r(p_[0] + 0.2), 2.3, r(p_[2] - 0.3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': sc}, toonDur=0.06, toonEase='out'),
            *[k(r(JUMP12 + 0.08 + 0.04 * j), toon={'sq': ([0.86, 1.22, 0.86] if j % 2 else [0.83, 1.27, 0.83]), 'hairUp': 1.0, **hat, 'reach': {'L': [r(p_[0] + 0.2), 2.3, r(p_[2] + 0.3), 1, 0.05], 'R': [r(p_[0] + 0.2), 2.3, r(p_[2] - 0.3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': sc}, toonDur=0.04) for j in range(4)],   # ...shivering up there
            k(r(DROP12 + 0.08), toon={'sq': [1.15, 0.85, 1.15], 'hairUp': 0.8, **hat, 'face': sc}, toonDur=0.04, toonEase='out'),   # ...a landing squash...
            k(r(RUN12 + 0.04 * i), to=run, dur=0.6, clip='run', then='stand', ease='in', face='move'), k(r(RUN12 + 0.04 * i), toon={'sq': [0.95, 1.05, 0.95], 'hairUp': 0.9, **hat, 'face': sc}, toonDur=0.08)]   # ...and they run
st.shot('S12', 'parisStreet', setOpts=CARN, actors=[
        act('mec', MC12, 40, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.12, toon={'face': {'lid': 0.45, 'gx': 0.7}}, toonDur=0.06), k(0.2, look={'point': [1.0, 1.4, 0.0], 'cheat': 0.5}),   # (pass 2) the reveal: his plain face turns to them, eyes first
            k(r(RUN12 + 0.3), toon={'face': {'lid': 0.45, 'gx': 0.6}}, toonDur=0.1),   # his eyes after them
            k(1.75, toon={'face': {'lid': 0.45, 'gx': -0.3}}, toonDur=0.1), k(1.9, look='camera'), k(1.92, toon={'sq': [1.0, 1.02, 1.0], 'face': DEAD}, toonDur=0.25, toonEase='inOut'),   # his eyes to us first, then his head
            k(2.3, toon={'sq': [1.0, 0.99, 1.0], 'face': {'lid': 0.45}}, toonDur=0.25, toonEase='inOut'),
            k(2.45, toon={'face': {'lid': 1.0}}, toonDur=0.12), k(2.66, toon={'sq': [1.0, 1.015, 1.0], 'face': DEAD}, toonDur=0.16)]),   # a slow blink
        *[act(n_, p_, ry_, 'stand', 'happy', keys=FRIGHT(i, p_, g_, ex_)) for i, (n_, p_, ry_, g_, ex_) in enumerate(CROWD)]],
        props=[*DECOR('12')],
        cams=[FC(0.0, [-0.3, 1.85, 1.6], [[MC12[0], 2.38, MC12[2]], [MC12[0], 1.5, MC12[2]], [r(MC12[0] + 0.4), 1.9, MC12[2]], [r(MC12[0] - 0.4), 1.9, MC12[2]]], top=0.16, bottom=0.6),   # (pass 2) close on his plain face turning to them...
              FC(REV12, [-0.6, 1.45, 2.4], [[r(MC12[0] - 0.28), 2.35, MC12[2]], [r(MC12[0] - 0.28), 0.5, MC12[2]], [1.2, 3.0, -0.55], [2.0, 2.6, 0.1], [2.0, 0.3, 0.1], [0.4, 2.7, 0.0]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.12)),   # ...them seeing it, his face three-quarters at the edge...
              FC(CUT12, [-0.6, 1.75, 2.6], [[MC12[0], 2.3, MC12[2]], [MC12[0], 1.0, MC12[2]], [r(MC12[0] + 0.5), 1.6, MC12[2]], [r(MC12[0] - 0.5), 1.6, MC12[2]]], top=0.16, bottom=0.68, drift=(0.0, 0.0, -0.35))])   # ...alone: a slow push-in
st.cue('sfx:gasp', 'S12', SEE12, 0.35); st.cue('sfx:boing', 'S12', JUMP12, 0.3); st.cue('sfx:thud', 'S12', r(DROP12 + 0.08), 0.25); st.cue('sfx:zip', 'S12', RUN12, 0.3)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 0.9, 'mec', 'grimace'), ('S03', 0.6, 'mec', 'press'), ('S04', 0.7, 'agent', 'take'), ('S05', 0.5, 'mec', 'stamp'), ('S06', 0.6, 'mec', 'shake'),
           ('S07', 0.5, 'mec', 'mask'), ('S09', 1.2, 'w1', 'town'), ('S10', 0.5, 'mec', 'except'), ('S11', 0.7, 'patron', 'fired'), ('S12', 0.7, 'k1', 'scare'), ('S12', 2.1, 'mec', 'alone')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S05', 0.7, 'photo5b', 'refusee')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S05', 'REFUSÉE', at=0.45)
st.card('S11', 'VIRÉ', at=0.32)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("La grimace", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'agent': {'preset': 'madame', 'seed': 591, 'suit': '#6E7F9E', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'patron': {'preset': 'boss', 'seed': 592, 'suit': '#C8402E', 'hat': 'party', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'k1': {'preset': 'gamin', 'seed': 593, 'suit': '#3A9BDC', 'hat': 'party', 'toon': EX},
    'k2': {'preset': 'gamin', 'seed': 594, 'suit': '#52B76A', 'toon': EX},
    'w1': {'preset': 'madame', 'seed': 595, 'suit': '#C255C8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'm1': {'preset': 'sportif', 'seed': 596, 'suit': '#F5A030', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'mamie': {'preset': 'mamie', 'seed': 597, 'hat': 'beanie', 'hatColor': '#C8452E', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
})
