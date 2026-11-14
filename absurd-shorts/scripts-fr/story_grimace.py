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
G_W1 = {'expr': 'disgusted', 'exprW': 0.9, 'mouth': 'teeth', 'mouthW': 0.95, 'mouthH': 0.7, 'mouthTilt': -14, 'cross': 1.0, 'eyeL': 0.6, 'eyeR': -0.2, 'browL': -0.9, 'browR': 1.0, 'pupilSize': 0.7, 'tongue': 1.0, 'tongueLen': 0.22, 'tongueYaw': 0.5}   # (final) as loud as his (pursed lips read almost neutral)
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
            k(PULL1, toon={**PULL(1.12), 'sq': [0.95, 1.08, 0.95], 'scl': {'head': [1.6, 0.74, 1.12]}, 'ears': 1.15, 'face': GF()}, toonDur=0.15, toonEase='out'),   # ...and PULLED, over five frames, past it ((pass 3) it popped in one)...
            k(r(PULL1 + 0.16), toon={**PULL(1.0), 'sq': [0.97, 1.06, 0.97], 'scl': {'head': GHEAD}, 'ears': 1.0, 'face': GF()}, toonDur=0.08, toonEase='inOut'),   # ...settling
            *[k(r(PULL1 + 0.26 + dt_), toon={**PULL(1.0 if i % 2 else 0.95), 'sq': ([0.97, 1.065, 0.97] if i % 2 else [0.985, 1.045, 0.985]), 'bend': {'spine': [0.0, 0, (0.03 if i % 2 else -0.03), 1, None]},
                                         'scl': {'head': ([1.5, 0.79, 1.09] if i % 2 else [1.42, 0.83, 1.07])}, 'ears': (1.05 if i % 2 else 0.9),
                                         'face': GF({'tongueYaw': yw_, 'tongueLen': 0.34})}, toonDur=0.1, toonEase='inOut') for i, (dt_, yw_) in enumerate([(0.0, -0.35), (0.16, 0.25), (0.3, -0.15), (0.48, 0.4), (0.6, -0.3), (0.78, 0.1), (0.92, -0.4)])]])],   # (pass 3) held, straining: the shoulders trembling, the tongue wagging off the beat
        cams=[FC(0.0, [r(ME[0] - 1.25), 1.95, 0.3], [[ME[0], 2.38, ME[2]], [ME[0], 1.5, ME[2]], [r(ME[0] - 0.2), 1.9, r(ME[2] + 0.7)], [r(ME[0] - 0.2), 1.9, r(ME[2] - 0.7)]], top=0.14, bottom=0.6, drift=(0.08, 0.0, -0.03)),   # (pass 2) his head 30 % of the frame...
              FC(0.74, [r(ME[0] - 1.05), 2.08, 0.22], [[ME[0], 2.46, ME[2]], [ME[0], 1.72, ME[2]]], top=0.2, bottom=0.66, drift=(0.04, 0.0, -0.02))])   # ...(pass 3) the hold in a close-up: the face about half the frame wide ((stills) chin to crown, not chest to crown)
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
D3 = st.dur('S03'); LET3 = 0.12; PRESS3 = 0.2; LIFT3 = 0.5; REL3 = 0.92              # (final) the press from 0.2, the plain face held thirteen frames with an exhale, then BOING   # (pass 3) the press twelve frames, the plain face held seven, then BOING
WIND3 = [-10.0, 1.0, 0.0]                                                 # from his left to his right
PRESS = lambda: {'touch': {'L': ['face', 0.5, 0.42, 0.02, 1, 0.02, [1.0, 0.05, 0.1]], 'R': ['face', -0.5, 0.42, 0.02, 1, 0.02, [-1.0, 0.05, 0.1]]}, 'hands': {'L': 'open', 'R': 'open'}}   # (final) both palms flat on his cheeks, the elbows out wide: the arms frame the squeezed head (with the elbows down it read as a chin scratch)
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**PULL(1.0), 'scl': {'head': GHEAD}, 'ears': 0.7, 'wind': WIND3, 'face': GF()}, toonDur=0.0),
            k(LET3, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'wind': WIND3, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': GF()}, toonDur=0.08, toonEase='out'),   # he lets go: it stays
            k(r(LET3 + 0.04), toon={'scl': {'head': [1.32, 0.84, 1.05]}, 'ears': 0.7, 'wind': WIND3, 'face': GF({'tongueYaw': 0.3})}, toonDur=0.03),   # (a shiver of the tongue; (stills F) before the press: after it, it undid it)
            k(PRESS3, toon={**PRESS(), 'scl': {'head': [0.76, 1.2, 1.0]}, 'sq': [1.04, 0.95, 1.04], 'wind': [-3.0, 0.0, 0.0], 'face': {'lid': 0.0, 'eye': 0.6, 'gy': -0.5, 'cheeks': 0.7, 'mouth': 'pout'}}, toonDur=0.08, toonEase='inOut'),   # palms on his cheeks, squeezing: plain again, the head tall and thin, his eyes bulging up...
            k(r(PRESS3 + 0.14), toon={**PRESS(), 'scl': {'head': [0.72, 1.24, 1.0]}, 'sq': [1.06, 0.93, 1.06], 'face': {'lid': 0.0, 'eye': 0.7, 'gy': -0.6, 'cheeks': 0.8, 'mouth': 'pout', 'tremble': 1.0}}, toonDur=0.1),   # ...pressing harder, his whole body straining down...
            k(LIFT3, toon={'hands': {'L': 'open', 'R': 'open'}, 'reach': {'L': [r(ME[0] - 0.35), 1.85, r(ME[2] + 0.42), 1, 0.05], 'R': [r(ME[0] - 0.35), 1.85, r(ME[2] - 0.42), 1, 0.05]}, 'scl': {'head': [0.98, 1.02, 1.0]}, 'face': {'lid': 0.3, 'brow': 0.6, 'mouth': 'flat'}}, toonDur=0.12, toonEase='inOut'),   # ...his hands lift slowly off a plain face...
            k(r(LIFT3 + 0.14), toon={'scl': {'head': [1.0, 1.0, 1.0]}, 'sq': [1.02, 0.97, 1.02], 'face': {'lid': 1.0, 'brow': 0.4}}, toonDur=0.06), k(r(LIFT3 + 0.22), toon={'scl': {'head': [1.0, 1.0, 1.0]}, 'sq': [1.02, 0.97, 1.02], 'face': {'lid': 0.25, 'brow': 0.7, 'mouth': 'smile'}}, toonDur=0.08),   # ...an exhale, the shoulders dropping, a blink of relief, hope...
            k(r(LIFT3 + 0.34), toon={'scl': {'head': [1.0, 1.0, 1.0]}, 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.2, 'brow': 0.75, 'mouth': 'smile'}}, toonDur=0.06),   # ...held...
            k(REL3, toon={'scl': {'head': [1.62, 0.7, 1.12]}, 'ears': 1.1, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [1.05, 0.94, 1.05], 'face': GF()}, toonDur=0.05, toonEase='out'),   # ...BOING: back, wider than ever...
            k(r(REL3 + 0.08), toon={'scl': {'head': [1.2, 0.92, 1.03]}, 'ears': 0.6, 'face': GF({'tongueYaw': 0.35})}, toonDur=0.07),
            k(r(REL3 + 0.16), toon={'scl': {'head': [1.52, 0.77, 1.1]}, 'ears': 0.95, 'face': GF({'tongueYaw': -0.4})}, toonDur=0.07),
            k(r(REL3 + 0.24), toon={'scl': {'head': GHEAD}, 'ears': 0.8, 'face': GF()}, toonDur=0.07)])],   # ...three wobbles dying down
        props=[P('leaf3', 'leafGust', pos=[r(ME[0] - 0.7), 0.4, r(ME[2] + 3.0)], ry=90, scale=1.6, opts={'n': 20, 'w': 4.0, 'h': 1.3, 'd': 0.8, 'startAt': 0.0, 'dur': 0.6})],
        cams=[FC(0.0, [r(ME[0] - 1.4), 1.85, -0.6], [[ME[0], 2.38, ME[2]], [ME[0], 1.35, ME[2]], [r(ME[0] - 0.3), 1.7, r(ME[2] + 0.6)], [r(ME[0] - 0.3), 1.7, r(ME[2] - 0.6)]], top=0.14, bottom=0.62, drift=(0.08, 0.0, 0.04))])   # (stills 1) closer
st.cue('gust', 'S03', 0.0, 0.3, 0.6); st.cue('sfx:squeak', 'S03', PRESS3, 0.2); st.cue('sfx:boing', 'S03', REL3, 0.45)

# 4: the town hall refuses... At the counter the clerk holds his identity photo up beside his face, at the end of her arm: the same grimace; her eyes
#    go to the photo, to him, to the photo, to him: a double take, her head shoots up
D4 = st.dur('S04')
OFFICE = {'title': 'MAIRIE', 'plate': False, 'bannerY': 2.8, 'bannerX': 2.5, 'clockX': -3.4}   # (final) the clock off the banner (it cut it to « MA »)   # (pass 2) the ÉTAT CIVIL plate sat in the caption band; (pass 3) the banner down where the shot sees it
VIS = [0.0, 0, 0.0]; CLERK = [0.25, 0, -1.4]                             # him in front of the desk, the clerk behind it
PH4 = [0.32, 1.84, -0.4]                                                  # (pass 2) her hand under the photo: the photo itself beside his face, at its height; (stills 2) it sat at his collar: raised to his face
PHC = [0.36, 2.05, -0.42]                                                 # (pass 3) the photo itself beside his face at its height, standing on its own
HOLD4 = lambda: {'reach': {'R': [0.22, 1.96, -0.63, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}   # (pass 3) her hand at its near edge, below its middle: her sleeve crossed its mouth
st.shot('S04', 'mairie', setOpts=OFFICE, actors=[
        act('mec', VIS, -75, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.0),   # (check) cheated toward us: at 180 his face was in profile
            k(0.5, toon={'scl': {'head': [1.31, 0.84, 1.05]}, 'ears': 0.7, 'face': GF({'tongueYaw': 0.2})}, toonDur=0.12), k(0.8, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.12)]),
        act('agent', CLERK, -40, 'stand', 'neutral', keys=[k(0.0, look={'point': PHC, 'cheat': 0.5}), k(0.0, toon={**HOLD4(), 'face': {'lid': 0.4, 'gx': 0.4}}, toonDur=0.0),
            k(0.16, toon={**HOLD4(), 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.0, 0.36, 0, 1, None]}, 'face': {'lid': 0.35, 'gx': -0.7}}, toonDur=0.06), k(0.24, look={'point': [VIS[0], 1.85, VIS[2]], 'cheat': 0.5}),   # her eyes to him first, then her head ((pass 3) cheated three-quarters to us)...
            k(0.36, toon={**HOLD4(), 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.0, -0.36, 0, 1, None]}, 'face': {'lid': 0.3, 'gx': 0.7}}, toonDur=0.06), k(0.42, look={'point': PHC, 'cheat': 0.5}),   # ...back to the photo...
            k(0.54, toon={**HOLD4(), 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.0, 0.38, 0, 1, None]}, 'face': {'lid': 0.3, 'gx': -0.8}}, toonDur=0.05), k(0.58, look={'point': [VIS[0], 1.85, VIS[2]], 'cheat': 0.6}),   # ...to him again...
            k(0.64, toon={**HOLD4(), 'scl': {'head': [0.84, 1.42, 0.86]}, 'hairUp': 1.0, 'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.0, 'eye': 0.9, 'eyeScale': 1.7, 'pupil': 0.45, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # ...the take: her head shoots up, her eyes bulging behind her glasses...
            k(0.76, toon={**HOLD4(), 'scl': {'head': [0.86, 1.4, 0.87]}, 'hairUp': 1.0, 'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.0, 'eye': 0.9, 'eyeScale': 1.65, 'pupil': 0.45, 'brow': 1.0, 'mouth': 'O', 'tremble': 1.0}}, toonDur=0.04),   # (final) ...hanging up there four frames...
            k(r(0.76 + 0.1), toon={**HOLD4(), 'scl': {'head': [0.94, 1.12, 0.95]}, 'hairUp': 0.8, 'face': {'lid': 0.0, 'eye': 0.6, 'pupil': 0.5, 'brow': 0.9, 'mouth': 'O'}}, toonDur=0.08),
            k(r(0.76 + 0.22), toon={**HOLD4(), 'scl': {'head': [1.0, 1.04, 1.0]}, 'hairUp': 0.6, 'face': {'lid': 0.1, 'eye': 0.5, 'pupil': 0.5, 'brow': 0.8, 'mouth': 'o'}}, toonDur=0.12)])],
        props=[P('photo4', 'grimacePhoto', pos=PHC, face='camera', scale=4.6, opts={'face': {k_: v_ for k_, v_ in GH.items() if not k_.startswith('tongue')}})],   # (pass 2) his very face; (pass 3) in the air beside his face, her hand at its edge
        cams=[FC(0.0, [-2.2, 1.65, 0.6], [[VIS[0], 2.38, VIS[2]], [VIS[0], 1.3, VIS[2]], [VIS[0], 2.0, r(VIS[2] + 0.42)], [VIS[0], 2.0, r(VIS[2] - 0.42)], [CLERK[0], 2.55, CLERK[2]], [r(CLERK[0] - 0.35), 2.3, CLERK[2]], [PHC[0], 2.35, PHC[2]], [PHC[0], 1.75, PHC[2]]], top=0.12, bottom=0.7, drift=(0.06, 0.0, -0.05))])   # (stills 2) his whole head in (cut by the right edge)   # (stills 1) his face and the photo side by side to us, her face three-quarters behind
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
               P('photo5b', 'grimacePhoto', pos=PH5, rot=[round(-PI / 2, 4), 0, 0], scale=2.6, opts={'face': {k_: v_ for k_, v_ in GH.items() if not k_.startswith('tongue')}, 'stamp': 'REFUSÉE'}, keys=[k(0.0, visible=False), k(r(HIT5 + 0.03), visible=True), k(r(HIT5 + 0.03), to=[PH5[0], r(PH5[1] + 0.05), PH5[2]], dur=0.04, ease='out'), k(r(HIT5 + 0.07), to=PH5, dur=0.06, ease='in')]),   # (pass 2) the imprint on the photo; (pass 3) it jumps under the blow
               P('stamp5', 'bigStamp', pos=SUP, scale=STK, keys=[k(0.06, to=STOP5, dur=0.22, ease='inOut'), k(r(HIT5 - 0.06), to=SDOWN, dur=0.06, ease='in'),
                                                                 k(r(HIT5 + 0.2), to=[0.0, 1.38, -0.95], dur=0.16, ease='out')]),
               # (pass 2) no stampPop: its mark lay under the photo
               P('pap5', 'paperSheet', pos=[0.55, 0.83, -0.72], rot=[round(-PI / 2, 4), 0, 0.3], opts={'w': 0.3, 'h': 0.4}, keys=[k(HIT5, to=[0.57, 0.98, -0.72], dur=0.06, ease='out'), k(r(HIT5 + 0.07), to=[0.58, 0.83, -0.71], dur=0.1, ease='in')])],   # the desk's papers jump
        fx=[{'type': 'shake', 'at': HIT5, 'dur': 0.1, 'amount': 0.024}],   # (final) a harder, shorter shake on the impact
        cams=[FC(0.0, [0.3, 2.05, -0.2], [[0.19, 0.836, -0.64], [-0.19, 0.836, -1.06], [0.19, 0.836, -1.06], [-0.19, 0.836, -0.64], [STOP5[0], 1.56, STOP5[2]]], top=0.08, bottom=0.88, level=False)])   # (stills 1) an insert from above: the photo big, the stamp coming down into it
st.cue('clack', 'S05', HIT5, 0.5); st.cue('sfx:thud', 'S05', HIT5, 0.4)

# 6: the carnival hired him. The carnival street (garlands over it, balloons): the carnival boss in a party hat sees his face and lights up (his eyes
#    huge), grabs his hand and pumps it: the shake ripples up the man's arm, his body jiggles, the grimace flaps; confetti
D6 = st.dur('S06'); GRAB6 = 0.28
CARN = {**STREET, 'eiffel': False, 'clearL': [-14.0, 8.0]}             # (pass 2) no tower stump behind the heads; (final) no tree behind his neck
MC = [-0.72, 0, 0.0]; BOSS = [0.76, 0, 0.15]                            # (final) further apart: the arms reach out of the bodies
HS = [0.03, 1.15, 0.62]                                                   # where the hands meet: (final) in the gap, forward of them, against the road (across his torso the arm vanished)
DECOR = lambda sid, z0=0.0: [P(f'ban{sid}', 'carnivalBanner', pos=[0.0, 3.6, r(z0 - 4.0)], opts={'w': 4.6, 'h': 0.85, 'span': 15}),   # (pass 2) the institution named
                             P(f'bunA{sid}', 'bunting', pos=[0.0, 4.6, r(z0 - 2.5)], opts={'len': 14, 'sag': 0.6, 'n': 22}), P(f'bunB{sid}', 'bunting', pos=[0.0, 5.0, r(z0 - 7.5)], opts={'len': 14, 'sag': 0.7, 'n': 22}),
                             P(f'bunC{sid}', 'bunting', pos=[0.0, 5.2, r(z0 - 13.0)], opts={'len': 14, 'sag': 0.7, 'n': 22}), P(f'bal{sid}', 'balloonBunch', pos=[2.6, 1.0, r(z0 - 1.6)], opts={'n': 7, 'len': 1.3})]
SHAKE = lambda i: {'reach': {'R': [HS[0], r(HS[1] + (0.26 if i % 2 else -0.22)), HS[2], 1, 0.05]}, 'hands': {'R': 'grip'}}   # (pass 3) big pumps (they were small)
DECOR_NB = lambda sid, z0=0.0: DECOR(sid, z0)[1:]                          # (pass 3) the decor without the banner (behind the big head, over the card band)
st.shot('S06', 'parisStreet', setOpts=CARN, actors=[
        act('mec', MC, 40, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [BOSS[0], 1.8, BOSS[2]], 'cheat': 0.5}), k(0.0, toon={'scl': {'head': GHEAD}, 'ears': 0.7, 'face': GF()}, toonDur=0.0),
            *[k(r(GRAB6 + 0.2 * i + dt_), toon={**SHAKE(i), 'scl': {'head': ([1.4, 0.78, 1.08] if (i + j) % 2 else [1.2, 0.92, 1.03])}, 'ears': (1.0 if (i + j) % 2 else 0.45),
                                                'sq': ([1.07, 0.93, 1.07] if (i + j) % 2 else [0.94, 1.07, 0.94]) if j else [1.0, 1.0, 1.0],
                                                'wave': {'armR': [0.14, 1.5, r(0.5 * i), 0, 0.0], 'spine': [0.07, 1.0, r(0.5 * i + 0.8), 1, 0.0]}, 'bend': {'neck': [((0.2 if i % 2 else -0.16) if j else 0.0), 0, 0, 1, None]},
                                                'face': GF({'tongueYaw': ((0.55 if i % 2 else -0.5) if j else 0.0)})}, toonDur=0.07, toonEase='inOut') for i in range(5) for j, dt_ in enumerate([0.0, 0.07])]]),   # (pass 3) each pump: the arm, then two frames later the body and the head jiggle, the grimace flaps
        act('patron', BOSS, -35, 'stand', 'happy', keys=[k(0.0, look={'point': [MC[0], 1.8, MC[2]], 'cheat': 0.6}),   # (pass 2) three-quarters to us: his face lighting up was turned away
            k(0.0, toon={'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.3, 'mouth': 'o'}}, toonDur=0.0),
            k(0.04, toon={'sq': [0.9, 1.12, 0.9], 'hairUp': 0.9, 'face': {'expr': 'surprised', 'exprW': 1.0, 'lid': 0.0, 'eye': 0.8, 'pupilSize': 0.6, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # (pass 3) he sees the face: a take, his eyes popping open...
            k(0.2, toon={'sq': [0.96, 1.05, 0.96], 'hairUp': 0.6, 'face': {'expr': 'surprised', 'exprW': 0.7, 'lid': 0.0, 'eye': 0.6, 'pupilSize': 0.5, 'brow': 0.9, 'mouth': 'bigsmile'}}, toonDur=0.06),   # ...lighting up...
            *[k(r(GRAB6 + 0.2 * i), toon={**SHAKE(i), 'sq': ([1.05, 0.95, 1.05] if i % 2 else [0.95, 1.05, 0.95]), 'face': {'expr': 'happy', 'exprW': 0.4, 'lid': 0.0, 'eye': 0.4, 'pupilSize': 0.4, 'brow': 0.8, 'mouth': 'bigsmile'}}, toonDur=0.07, toonEase='inOut') for i in range(5)]])],   # ...and pumps his hand, eyes open
        props=[*DECOR('6'), *[P(f'cf6{i}', 'confetti', pos=[r(HS[0] + dx_), 3.4, r(HS[2] - 0.3)], opts={'n': 30, 'at': r(GRAB6 - 0.05), 'dur': 0.95, 'color': c_, 's': 2.4, 'fall': 2.9, 'seed': 3 + 5 * i}) for i, (dx_, c_) in enumerate([(-0.6, '#F5C33B'), (0.0, '#E8463A'), (0.6, '#3A9BDC')])]],   # (pass 3) raining from above over them both (a clump riding with the hands)
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
        props=[*DECOR_NB('7'), P('float7', 'carnivalFloat', pos=FL0, opts={'w': 2.6, 'd': 1.4, 'h': 0.75}, keys=[k(0.0, to=FL1, dur=D7, ease='linear')]),
               *[P(f'cf7{c_}', 'confetti', pos=[r(-1.4 + 1.4 * i) if i != 1 else 1.6, 3.6, -1.0], opts={'n': 22, 'at': 0.0, 'dur': 1.0, 'color': c_, 's': 1.4, 'fall': 2.6, 'seed': 4 + i}) for i, c_ in enumerate(['#F5C33B', '#E8463A', '#C255C8'])]],
        cams=[FC(0.0, [0.4, 0.75, 3.4], [[FL0[0], 3.85, FL0[2]], [-1.3, 0.0, r(FL0[2] + 0.7)], [1.3, 0.0, r(FL0[2] + 0.7)], [-0.95, 1.5, -0.35], [0.95, 1.5, -0.4]], top=0.1, bottom=0.82, drift=(0.0, 0.05, -0.15))])
st.cue('sfx:stretch', 'S07', 0.16, 0.3); st.cue('sfx:pop', 'S07', 0.42, 0.3); st.cue('sfx:tada', 'S07', 0.12, 0.18)

# 8: yesterday the wind turned again. The weathervane from the other side (a garland on the roof now): the rooster whirls the other way, faster and
#    faster, its rod unscrews and the whole vane takes off like a helicopter out of the frame; leaves and a party hat blown past
D8 = st.dur('S08'); LIFT8 = 0.5                                             # (pass 2) the repeat whirl short: it unscrews sooner
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('vane8', 'weathervane', pos=WV, opts={'roof': {'len': 3.2}, 'spin': [[0.0, 0.0], [0.12, -1.5], [0.45, -4.0], [1.9, -4.6]], 'wobble': [0.08], 'yaw0': 2.2, 'lift': [LIFT8, 0.45, 0.6, 0.32, 30.0], 'dip': [r(LIFT8 - 0.14), 0.14, 0.14]}),   # (pass 3) a dip and a shudder first: it took off with no wind-up
               P('bun8', 'bunting', pos=[r(WV[0] + 0.1), r(WV[1] + 0.32), r(WV[2] + 0.2)], opts={'len': 3.0, 'sag': 0.25, 'n': 8}),
               P('leaf8', 'leafGust', pos=[r(WV[0] + 3.4), r(WV[1] - 0.8), r(WV[2] + 1.0)], ry=180, scale=2.5, opts={'n': 26, 'w': 2.8, 'h': 1.2, 'd': 0.7, 'startAt': 0.2, 'dur': 1.2}),
               P('hat8', 'partyHat', pos=[r(WV[0] - 3.2), r(WV[1] - 0.5), r(WV[2] + 1.0)], scale=2.0, keys=[k(0.3, to=[r(WV[0] + 3.4), r(WV[1] + 0.9), r(WV[2] + 1.0)], dur=1.0, ease='inOut'), k(0.3, rotTo=[3.0, 2.0, 7.0], dur=1.0)])],
        cams=[FC(0.0, [r(WV[0] + 1.4), r(WV[1] + 0.05), r(WV[2] + 2.3)], [[WV[0], r(WV[1] + 2.0), WV[2]], [r(WV[0] - 0.8), WV[1], WV[2]], [r(WV[0] + 0.8), WV[1], WV[2]], [WV[0], r(WV[1] - 0.35), r(WV[2] + 0.4)]],
                 top=0.1, bottom=0.76, drift=(-0.12, 0.7, -0.08))])   # (stills 1) closer, room over it for the take-off; (pass 2) rising with it
st.cue('gust', 'S08', 0.05, 0.5, 1.8); st.cue('sfx:squeak', 'S08', 0.1, 0.3); st.cue('whoosh', 'S08', 0.45, 0.3, 0.9, 250, 1300); st.cue('sfx:twang', 'S08', LIFT8, 0.3); st.cue('sfx:zip', 'S08', r(LIFT8 + 0.8), 0.35)

# 9: the whole town stayed in a grimace. (pass 2) A medium close-up of three carnival-goers cheering, arms up, more behind them; the gust runs through
#    them from left to right (hair, hats and ties whipped one after another, leaves); each face snaps into a grimace of its own as it passes, the head
#    squashed four frames, overshooting, set wide, the arms dropping
D9 = st.dur('S09')
TOWN = [('patron', [-0.74, 0, 0.35], 14, G_BOSS, 'happy'), ('w1', [0.0, 0, 0.15], 0, G_W1, 'happy'), ('mamie', [0.74, 0, 0.4], -14, G_MAM, 'happy'),   # (final) a head apart: no raised arm across a face
        ('k1', [-1.5, 0, -1.6], 10, G_K1, 'happy'), ('m1', [1.5, 0, -1.7], -10, G_M1, 'happy')]   # three big faces, two behind
SNAP9 = [0.42, 0.62, 0.82, 1.0, 1.12]
CHEER = lambda p_: {'reach': {'L': [r(p_[0] + 0.24), 2.4, r(p_[2] + 0.05), 1, 0.05], 'R': [r(p_[0] - 0.24), 2.4, r(p_[2] + 0.05), 1, 0.05]}, 'hands': {'L': 'open', 'R': 'open'}}   # (final) straight up over their own heads
def SNAPKEYS(ts, g_, i, p_):
    wind = {'wind': [12.0, 1.5, 0.0], 'hairUp': 0.5}
    return [k(0.0, toon={**CHEER(p_), 'sq': [1.0, 1.02, 1.0], 'face': {'mouth': 'bigsmile', 'lid': 0.1}}, toonDur=0.0),
            k(r(0.06 + 0.05 * i), toon={**CHEER(p_), 'sq': [0.98, 1.04, 0.98], 'face': {'mouth': 'bigsmile', 'lid': 0.0, 'brow': 0.5}}, toonDur=0.15, toonEase='inOut'),   # cheering, a bounce
            k(r(ts - 0.06), toon={**CHEER(p_), **wind, 'face': {'mouth': 'bigsmile', 'lid': 0.3, 'brow': 0.6}}, toonDur=0.05),   # the gust reaches him: hair and tie whipped...
            k(ts, toon={**wind, 'scl': {'head': [1.38, 0.7, 1.15]}, 'sq': [1.06, 0.92, 1.06], 'ears': 0.8, 'face': g_}, toonDur=0.04, toonEase='out'),   # ...CLAC: the face snaps, the head squashed, the arms drop...
            k(r(ts + 0.13), toon={**wind, 'scl': {'head': [1.36, 0.72, 1.14]}, 'ears': 0.8, 'face': g_}, toonDur=0.1),   # ...held four frames...
            k(r(ts + 0.2), toon={'scl': {'head': [0.9, 1.16, 0.95]}, 'ears': 0.4, 'face': g_}, toonDur=0.06),   # ...overshooting tall...
            k(r(ts + 0.3), toon={'scl': {'head': [1.34, 0.78, 1.1]}, 'face': g_}, toonDur=0.08), k(r(ts + 0.5), toon={'scl': {'head': [1.32, 0.79, 1.1]}, 'sq': [1.0, 1.015, 1.0], 'face': g_}, toonDur=0.25, toonEase='inOut')]   # ...and set wide ((final) as wide as his, not back to tall boxes)
st.shot('S09', 'parisStreet', setOpts=CARN, actors=[
        act(n_, p_, ry_, 'stand', ex_, keys=[k(0.0, look='camera'), *SNAPKEYS(SNAP9[i], g_, i, p_)]) for i, (n_, p_, ry_, g_, ex_) in enumerate(TOWN)],
        props=[*DECOR('9'), P('leaf9', 'leafGust', pos=[-2.4, 0.6, 1.0], scale=1.3, opts={'n': 34, 'w': 3.8, 'h': 1.8, 'd': 1.2, 'startAt': 0.3, 'dur': 1.0})],
        cams=[FC(0.0, [0.0, 1.85, 2.0], [[-0.74, 2.5, 0.35], [0.74, 2.3, 0.4], [-1.02, 2.0, 0.35], [1.02, 2.0, 0.4], [0.0, 1.55, 0.15]], top=0.16, bottom=0.62, drift=(0.0, 0.0, -0.08))])   # (final) closer: the three faces fill the width   # (pass 2) three faces each a quarter of the frame
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
        act('patron', [-0.72, 0, -0.4], 20, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': [1.32, 0.79, 1.1]}, 'face': G_BOSS}, toonDur=0.0), k(0.3, toon={'scl': {'head': [1.22, 0.85, 1.07]}, 'sq': [1.0, 1.02, 1.0], 'face': G_BOSS}, toonDur=0.3, toonEase='inOut')]),
        act('mamie', [0.74, 0, -0.35], -20, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': [1.32, 0.79, 1.1]}, 'face': G_MAM}, toonDur=0.0), k(0.2, toon={'scl': {'head': [1.18, 0.88, 1.07]}, 'sq': [1.0, 1.02, 1.0], 'face': G_MAM}, toonDur=0.3, toonEase='inOut')])],
        props=[*DECOR('10'), P('leaf10', 'leafGust', pos=[-2.0, 1.6, -1.2], scale=1.3, opts={'n': 16, 'w': 3.6, 'h': 1.2, 'd': 0.6, 'startAt': 0.0, 'dur': 0.5})],   # (stills 2) behind the heads: a leaf crossed his face on the beat
        cams=[FC(0.0, [0.05, 1.95, 1.5], [[0.0, 2.42, 0.0], [0.0, 1.5, 0.0], [-0.98, 2.2, -0.4], [1.0, 2.15, -0.35]], top=0.16, bottom=0.66, drift=(0.0, 0.0, -0.06))])   # (final) a head-width aside: the mamie sat right behind his head   # (stills 2) his head a third of the frame, the two grimaces cut by its edges (his head was as small as theirs on « Sauf lui »); (stills 3) their whole faces in: the boss's was out of frame
st.cue('sfx:zip', 'S10', r(BACK10 - 0.02), 0.35); st.cue('sfx:pop', 'S10', BACK10, 0.2)

# 11: the carnival fired him. (pass 3) Staged in depth, the street running away to the left: the man large in the foreground, three-quarters to us;
#     behind him the boss, grimacing, cocks his arm and flings it out down the street, the arm stretching along the road two and a half times, past the
#     point and back, the finger jabbing; the man's eyes go along the arm (four frames), then his head (eight), his face kept to us
D11 = st.dur('S11'); PT11 = 0.32
MC11 = [0.6, 0, 1.2]; BOSS11 = [1.5, 0, 0.4]                             # (stills F) the boss on the right, the man on the left: the arm crosses the frame past his nose (pointed down the street it was end-on to the lens, invisible)   # (final) the boss closer, bigger   # (stills) the boss clear of him (behind him the boss and the arm were hidden)
OUTPT = [-3.5, 2.15, 1.9]                                                  # (stills F) far off the left of the frame at his nose height: the arm runs out of the frame   # (final) far down the street at shoulder height (up at the awning it vanished)   # (pass 3) down the street (it pointed up into the air)
JAB = lambda j: [r(OUTPT[0] + (0.05 if j % 2 else -0.03)), r(OUTPT[1] + (0.02 if j % 2 else 0.0)), r(OUTPT[2] + (0.07 if j % 2 else -0.04))]
PTK = lambda p_, hand='point': {'reach': {'R': [r(p_[0]), r(p_[1]), r(p_[2]), 1, 0.08], 'L': [r(BOSS11[0] + 0.05), 1.0, r(BOSS11[2] + 0.28), 1, 0.05]}, 'hands': {'R': hand, 'L': 'fist'}}   # his other fist on his hip
BH = {'scl': {'head': [1.2, 0.87, 1.07]}, 'face': G_BOSS}
st.shot('S11', 'parisStreet', setOpts=CARN, actors=[
        act('mec', MC11, 28, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(r(PT11 + 0.04), toon={'face': {'lid': 0.4, 'gx': -0.9, 'pupilSize': 0.3}}, toonDur=0.13), k(r(PT11 + 0.17), look={'point': OUTPT, 'cheat': 0.55}),   # his eyes along the arm (four frames), then his head (eight)...
            k(0.62, toon={'sq': [1.0, 1.012, 1.0], 'face': {'lid': 0.45, 'gx': -0.7}}, toonDur=0.2), k(0.95, toon={'face': {'lid': 1.0, 'gx': -0.6}}, toonDur=0.05), k(1.03, toon={'sq': [1.0, 0.995, 1.0], 'face': {'lid': 0.45, 'gx': -0.4}}, toonDur=0.1)]),   # ...a breath, a blink
        act('patron', BOSS11, -95, 'stand', 'determined', keys=[k(0.0, look={'point': [MC11[0], 1.8, MC11[2]], 'cheat': 0.6}), k(0.0, toon=BH, toonDur=0.0),
            k(0.06, toon={**PTK([r(BOSS11[0] + 0.38), 1.75, r(BOSS11[2] - 0.1)], 'fist'), **BH, 'bend': {'spine': [-0.2, 0, -0.15, 1, None]}, 'sq': [1.06, 0.93, 1.06]}, toonDur=0.12, toonEase='inOut'),   # the arm cocked back across his chest (six frames)...
            k(PT11, toon={**PTK([r(OUTPT[0] - 0.3), r(OUTPT[1] + 0.08), r(OUTPT[2] - 0.4)]), **BH, 'bend': {'spine': [0.1, 0, 0.12, 1, None]}, 'sq': [0.96, 1.06, 0.96]}, toonDur=0.07, toonEase='out'),   # ...FLUNG down the street, past the point...
            k(r(PT11 + 0.1), toon={**PTK([r(OUTPT[0] + 0.08), r(OUTPT[1] - 0.02), r(OUTPT[2] + 0.1)]), **BH}, toonDur=0.08), k(r(PT11 + 0.2), look={'point': OUTPT, 'cheat': 0.5}),   # ...back...
            k(r(PT11 + 0.2), toon={**PTK(OUTPT), **BH, 'sq': [1.0, 1.01, 1.0]}, toonDur=0.05),   # (final) ...held stretched eight frames...
            *[k(r(PT11 + 0.47 + 0.07 * j), toon={**PTK(JAB(j)), **BH, 'sq': [1.0, 1.012 if j % 2 else 0.996, 1.0]}, toonDur=0.06) for j in range(9)]])],   # ...then the finger jabbing
        props=[*DECOR_NB('11')],   # (pass 3) no banner under the VIRÉ card
        cams=[FC(0.0, [2.3, 1.65, 4.3], [[MC11[0], 2.44, MC11[2]], [MC11[0], 1.1, MC11[2]], [BOSS11[0], 2.62, BOSS11[2]], [r(BOSS11[0] + 0.3), 2.45, BOSS11[2]], [BOSS11[0], 1.1, BOSS11[2]], [r(MC11[0] - 0.75), 2.05, r(MC11[2] + 0.35)]],   # (stills F2) the boss's whole head (it was cut by the edge)
                 top=0.2, bottom=0.72, drift=(-0.04, 0.0, -0.05))])   # (pass 3) the man whole from the cut (half out of the frame), the arm along the road
st.cue('sfx:stretch', 'S11', PT11, 0.35); st.cue('sfx:whistle', 'S11', r(PT11 + 0.02), 0.15)

# 12: he is too scary. Close on his plain face turning to them (the reveal); (pass 3) over his shoulder, closer: the grimacing children and the mamie hold
#     their grimaces eight frames, see him: their eyes, then their heads snap to him, a squash of fright, and they jump out of their skins at different
#     heights (hang time, hair on end, the mamie's cap sailing up in an arc against the sky, the kid's eyes out on stalks), drop and run off one after
#     the other; he stays alone; closer: his eyes come to us, a slow blink
D12 = st.dur('S12'); REV12 = 0.3; SEE12 = 0.62; JUMP12 = 0.72; DROP12 = 0.98; RUN12 = 1.12; CUT12 = 1.7
MC12 = [-0.9, 0, 0.2]
CROWD = [('k1', [0.55, 0, 0.35], -70, G_K1, {'pop': 0.8, 'popLen': 0.22}, 0.85), ('w1', [1.4, 0, -0.65], -60, G_W1, {}, 0.5), ('mamie', [1.2, 0, 1.0], -80, G_MAM, {}, 0.7), ('k2', [2.05, 0, 0.25], -70, G_K2, {}, 0.62)]
CAPK = [(0.0, 0.0), (0.06, 0.5), (0.14, 1.15), (0.24, 1.5), (0.36, 1.62), (0.6, 2.4)]   # (pass 3) the cap's arc after the jump: up, slowing, hanging, then gone up
def capAt(dt):
    for (a, la), (b, lb) in zip(CAPK, CAPK[1:]):
        if dt <= b: return r(la + (lb - la) * (dt - a) / (b - a))
    return CAPK[-1][1]
def FRIGHT(i, p_, g_, extra, jumpH):
    sc = {**g_, 'mouth': 'scream', 'lid': 0.0, 'brow': 1.0, **extra}
    up = [p_[0], jumpH, p_[2]]
    run = [r(p_[0] + 4.5), 0, r(p_[2] - 1.5 + 0.8 * i)]
    hat = (lambda t: {'hat': [capAt(t - JUMP12), r(0.6 + 2.2 * max(0.0, t - JUMP12)), r(5.0 * max(0.0, t - JUMP12))]}) if i == 2 else (lambda t: {})
    arms = {'reach': {'L': [r(p_[0] + 0.2), 2.3, r(p_[2] + 0.3), 1, 0.05], 'R': [r(p_[0] + 0.2), 2.3, r(p_[2] - 0.3), 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}
    tr = r(RUN12 + 0.1 * i)                                                 # (pass 3) the exits a few frames apart (one clump)
    return [k(0.0, look=[1.0, 1.6, 3.0]), k(0.0, toon={'face': {**g_, 'gx': 0.3}}, toonDur=0.0),
            k(r(REV12 + 0.12), toon={'sq': [1.0, 1.02, 1.0], 'face': {**g_, 'gx': -0.8}}, toonDur=0.05), k(r(REV12 + 0.18), look=[MC12[0], 1.8, MC12[2]]),   # their eyes, then their heads, snap to him (the grimaces held eight frames)
            k(r(SEE12 - 0.06), toon={'sq': [1.1, 0.88, 1.1], 'face': {**g_, 'lid': 0.0, 'brow': 0.8}}, toonDur=0.06, toonEase='in'),   # a squash of fright...
            k(JUMP12, to=up, dur=0.12, ease='out', face='keep'), k(DROP12, to=p_, dur=0.1, ease='in', face='keep'),   # ...up out of their skins, a hang, down...
            k(JUMP12, toon={'sq': [0.84, 1.26, 0.84], 'hairUp': 1.0, **hat(JUMP12), **arms, 'face': sc}, toonDur=0.06, toonEase='out'),
            *[k(r(JUMP12 + 0.08 + 0.04 * j), toon={'sq': ([0.86, 1.22, 0.86] if j % 2 else [0.83, 1.27, 0.83]), 'hairUp': 1.0, **hat(r(JUMP12 + 0.08 + 0.04 * j)), **arms, 'face': sc}, toonDur=0.04) for j in range(4)],   # ...shivering up there
            k(r(DROP12 + 0.08), toon={'sq': [1.15, 0.85, 1.15], 'hairUp': 0.8, **hat(r(DROP12 + 0.08)), 'face': sc}, toonDur=0.04, toonEase='out'),   # ...a landing squash...
            k(tr, to=run, dur=0.6, clip='run', then='stand', ease='in', face='move'), k(tr, toon={'sq': [0.95, 1.05, 0.95], 'hairUp': 0.9, **hat(tr), 'face': sc}, toonDur=0.08)]   # ...and they run
st.shot('S12', 'parisStreet', setOpts=CARN, actors=[
        act('mec', MC12, 40, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.1, toon={'face': {'lid': 0.45, 'gx': 0.7}}, toonDur=0.05), k(0.16, look={'point': [1.0, 1.4, 0.0], 'cheat': 0.5}),   # the reveal: his plain face turns to them, eyes first
            k(r(RUN12 + 0.3), toon={'face': {'lid': 0.45, 'gx': 0.6}}, toonDur=0.1),   # his eyes after them
            k(1.75, toon={'face': {'lid': 0.45, 'gx': -0.3}}, toonDur=0.1), k(1.9, look='camera'), k(1.92, toon={'sq': [1.0, 1.02, 1.0], 'face': DEAD}, toonDur=0.25, toonEase='inOut'),   # his eyes to us first, then his head
            k(2.3, toon={'sq': [1.0, 0.99, 1.0], 'face': {'lid': 0.45}}, toonDur=0.25, toonEase='inOut'),
            k(2.45, toon={'face': {'lid': 1.0}}, toonDur=0.12), k(2.66, toon={'sq': [1.0, 1.015, 1.0], 'face': DEAD}, toonDur=0.16)]),   # a slow blink
        *[act(n_, p_, ry_, 'stand', 'happy', keys=FRIGHT(i, p_, g_, ex_, jh_)) for i, (n_, p_, ry_, g_, ex_, jh_) in enumerate(CROWD)]],
        props=[*DECOR_NB('12')],   # (pass 3) no banner: the end hold read « CARNAV » behind his head
        cams=[FC(0.0, [-0.3, 1.85, 1.6], [[MC12[0], 2.38, MC12[2]], [MC12[0], 1.5, MC12[2]], [r(MC12[0] + 0.4), 1.9, MC12[2]], [r(MC12[0] - 0.4), 1.9, MC12[2]]], top=0.16, bottom=0.6),   # close on his plain face turning to them...
              FC(REV12, [-2.3, 1.95, -0.75], [[MC12[0], 2.4, MC12[2]], [0.55, 2.05, 0.35], [1.2, 2.25, 1.0], [2.05, 1.95, 0.25], [1.2, 0.9, 1.0], [0.55, 3.25, 0.35], [1.2, 3.1, 1.0], [1.4, 2.9, -0.65], [2.05, 2.75, 0.25]], top=0.12, bottom=0.78, drift=(0.0, 0.0, 0.06)),   # (final) room over their heads at the top of the leap (eyes and the mamie's head were cut)   # (pass 3) ...over his shoulder, close on them ((stills) a step back: his head filled half the frame)...
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
