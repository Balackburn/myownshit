#!/usr/bin/env python3
"""Le ressort (story 61, cycle 23 of the cartoon staging): this man sat on a spring. He bounced up to the roof. Since then he bounces everywhere. The
town hall declared him a flying object. He must pass the pilot's licence. He failed it three times. Yesterday he stopped bouncing. In mid-flight. The
pigeons built their nest on his head.
Staging: on a Paris pavement he sits down on a bench, deadpan; a spring bursts out of the seat under him, BOING, he squashes into it, his eyes pop,
and he is shot up stretched like a rubber band, arms up; low on the pavement the camera tilts up the facade as he shoots past the windows; on a roof
ridge he lands like an accordion, squashed flat and springing back, the pigeons scattering. Down the street he bounces along like a pogo stick, hopping
over a woman who ducks; at a café he bounces straight up out of the frame and his coffee cup stays hanging in the air where his hand was, until he
drops back into it. At the town hall the clerk's pen goes down a form, OISEAU, AVION, and ticks OBJET VOLANT while he bounces behind the counter; she
times his bounces with her eyes and slaps a registration sticker « F-MEC » on his chest. At the pilot's exam, in a leather cap and goggles, he bounces
in his chair while the examiner's head goes up and down with him; one bounce takes him into the ceiling lamp and he comes down wearing its shade; on
the examiner's clipboard three red crosses slash ESSAI 1, 2, 3 (RECALÉ). In the street he bounces higher and higher and, at the top of a bounce, stops
dead in mid-air; from below he looks down at nothing, then at us; the pigeons land on his head, build a nest and lay eggs; a slow blink.
Natural look; cycle 23 tools: props_ressort.js (springCoil, regSticker, formCheck, clipboardX, lampShade) and the 'aviator' cap (human.js)."""
from story_kit import *
import math

st = Story('ressort', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 4), ('S03', 'L02', 0), ('S04', 'L02', 3), ('S05', 'L03', 0), ('S06', 'L03', 2), ('S07', 'L04', 0), ('S08', 'L04', 4),
         ('S09', 'L05', 0), ('S10', 'L06', 0), ('S11', 'L06', 3), ('S12', 'L07', 0), ('S13', 'L08', 0), ('S14', 'L09', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
def FLY(pts):
    """a flight through timed points [[t, x, y, z], ...] as prop keys in world space"""
    return {'pos': list(pts[0][1:]), 'keys': [k(pts[i][0], to=list(pts[i + 1][1:]), dur=round(pts[i + 1][0] - pts[i][0], 3), ease='linear') for i in range(len(pts) - 1)]}
DEAD = {'lid': 0.45}
BURST = lambda pid, pos, at_, text, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
STREET = {'eiffelStyle': 'v2', 'clear': [-6.0, 6.0]}                       # no tree or lamp on the right pavement around him
ME = [7.2, 0, 0.0]; RY = -90                                             # on the right pavement, facing the road (-X); his left is +Z
SQ = [1.22, 0.76, 1.22]; ST = [0.84, 1.22, 0.84]                          # a landing squash, a take-off stretch
HOPS = lambda t0, pts, peak, dt: hops(t0, pts, peak, dt, SQ, ST)          # (cycle 23) the bounces: story_kit.hops

# 1: the hook. A Paris pavement: he walks up to a bench and sits down on it, deadpan, settling
D1 = st.dur('S01')
BENCH = [7.75, 0, 0.0]; SEAT = [7.7, 0, 0.0]
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [7.05, 0, 0.0], RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.22, to=SEAT, dur=0.3, clip='sit', then='sit', glide=True, ease='inOut', face=RY, blend=0.12),   # he sits down ((stills 1) then='sit': without it he stood up again)...
            k(0.5, toon={'sq': [1.04, 0.95, 1.04], 'face': DEAD}, toonDur=0.05, toonEase='out'), k(0.58, toon={'sq': [0.99, 1.01, 0.99], 'face': {'lid': 0.5}}, toonDur=0.1),   # ...a little settle...
            k(0.75, toon={'face': {'lid': 0.55, 'cheeks': 0.3}}, toonDur=0.12)])],   # ...content
        props=[P('bench1', 'bench', pos=BENCH, ry=RY)],
        cams=[FC(0.0, [5.9, 0.95, -1.6], [[7.3, 2.35, 0.0], [7.3, 0.2, 0.0], [BENCH[0], 0.9, -0.85], [BENCH[0], 0.9, 0.85]], top=0.16, bottom=0.74, drift=(0.06, 0.0, 0.05))])
st.cue('sfx:squeak', 'S01', 0.5, 0.15)

# 2: ...on a spring. Low and close: BOING, a spring bursts out of the seat under him: he squashes into the bench, his eyes pop, his hair shoots up...
#    and he is shot straight up out of the frame, stretched like a rubber band, arms up; the spring boings on, dust
D2 = st.dur('S02'); SPR2 = 0.24; GO2 = 0.3
SPRING = [BENCH[0] - 0.05, 0.47, 0.0]
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', SEAT, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.55, 'cheeks': 0.3}}, toonDur=0.0),
            k(SPR2, toon={'sq': [1.24, 0.74, 1.24], 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 0.7, 'pupilSize': -0.3, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.03, toonEase='out'),   # BOING: squashed into it, eyes popping...
            k(GO2, clip='stand', blend=0.04),
            k(GO2, to=[SEAT[0], 7.0, SEAT[2]], dur=0.34, ease='out', face='keep'),   # ...shot up...
            k(GO2, toon={'sq': [0.6, 1.75, 0.6], 'reach': {'L': [r(SEAT[0] - 0.2), 12.0, 0.3, 1, 0.05], 'R': [r(SEAT[0] - 0.2), 12.0, -0.3, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'hairUp': 1.0,
                          'face': {'lid': 0.0, 'eye': 0.5, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.04, toonEase='out')])],   # ...stretched like a rubber band, arms up
        props=[P('bench2', 'bench', pos=BENCH, ry=RY), P('spring2', 'springCoil', pos=SPRING, opts={'at': SPR2, 'len': 0.75, 'r': 0.1, 'wire': 0.02}),   # (stills 1) bigger, no dust (the puff hid it)
               BURST('boing2', [r(SPRING[0] - 0.5), 1.05, r(SPRING[2] - 0.55)], SPR2, 'BOING !', 0.46),
               P('spd2', 'speedLines', **FLY([[GO2, SEAT[0], 0.6, SEAT[2]], [r(GO2 + 0.3), SEAT[0], 4.5, SEAT[2]]]), face='camera', opts={'n': 6, 'len': 1.4, 'w': 0.7, 'angle': 1.57, 'at': [[GO2, r(GO2 + 0.4)]]})],
        cams=[FC(0.0, [6.3, 0.72, -1.15], [[SEAT[0], 2.05, SEAT[2]], [SEAT[0], 0.35, SEAT[2]], [r(SEAT[0] - 0.4), 0.9, -0.55], [r(SEAT[0] - 0.4), 0.9, 0.55]], top=0.2, bottom=0.8)])
st.cue('sfx:boing', 'S02', SPR2, 0.5); st.cue('whoosh', 'S02', GO2, 0.4, 0.6, 300, 1500)

# 3: he bounced... Low on the pavement, the camera tilting up the facade as he shoots up past the windows, stretched, speed lines under him
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [SEAT[0], 0.6, SEAT[2]], RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.0, to=[SEAT[0], 18.0, SEAT[2]], dur=D3, ease='linear', face='keep'),
            k(0.0, toon={'sq': [0.72, 1.42, 0.72], 'reach': {'L': [r(SEAT[0] - 0.2), 30.0, 0.3, 1, 0.05], 'R': [r(SEAT[0] - 0.2), 30.0, -0.3, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'hairUp': 1.0,
                          'face': {'lid': 0.0, 'eye': 0.4, 'brow': 0.9, 'mouth': 'O'}}, toonDur=0.0)])],   # (stills 1) stretched less: at 1.7 he was a dark stripe
        props=[P('spd3', 'speedLines', **FLY([[0.0, SEAT[0], 0.0, SEAT[2]], [D3, SEAT[0], 15.5, SEAT[2]]]), face='camera', opts={'n': 7, 'len': 2.2, 'w': 0.8, 'angle': 1.57, 'at': [[0.0, D3]]})],
        cams=[cam(0.0, [3.9, 1.8, -3.7], [3.9, 16.2, -3.7], [SEAT[0], 2.6, 0.3], [SEAT[0], 18.8, 0.3], lens=50)])   # (audit) riding up beside him, the windows streaming down behind (tilting from the street he was 8 % of the frame)
st.cue('whoosh', 'S03', 0.0, 0.35, 0.7, 400, 1800)

# 4: ...up to the roof. A slate roof ridge high over the city: he drops onto it and lands like an accordion, squashed flat and springing back up past
#    his height, wobbling; the pigeons on the ridge scatter; feathers
D4 = st.dur('S04'); LAND4 = 0.18
ROOF = [0.0, 22.0, -12.0]; ONR = [r(ROOF[0] - 1.6), ROOF[1], ROOF[2]]
PIGS4 = [(-0.9, 0.35), (-2.3, 0.25), (-0.4, -0.3)]
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [ONR[0], r(ONR[1] + 3.0), ONR[2]], RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'sq': [0.85, 1.2, 0.85], 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 0.3, 'brow': 0.6}}, toonDur=0.0),
            k(0.0, to=ONR, dur=LAND4, ease='in', face='keep'),
            k(LAND4, toon={'sq': [1.55, 0.38, 1.55], 'hairUp': 0.2, 'face': {'lid': 1.0, 'brow': -0.6, 'mouth': 'clench'}}, toonDur=0.03, toonEase='out'),   # the accordion: squashed flat...
            k(r(LAND4 + 0.1), toon={'sq': [1.5, 0.42, 1.5], 'face': {'lid': 1.0, 'brow': -0.6, 'mouth': 'clench'}}, toonDur=0.06),   # ...held three frames...
            k(r(LAND4 + 0.16), toon={'sq': [0.82, 1.28, 0.82], 'hairUp': 0.8, 'face': {'lid': 0.2, 'eye': 0.3}}, toonDur=0.06, toonEase='out'),   # ...springing back past his height...
            k(r(LAND4 + 0.26), toon={'sq': [1.1, 0.9, 1.1], 'face': DEAD}, toonDur=0.07), k(r(LAND4 + 0.36), toon={'sq': [0.97, 1.03, 0.97], 'face': DEAD}, toonDur=0.08),
            k(r(LAND4 + 0.48), toon={'face': DEAD}, toonDur=0.1)]),   # ...wobbling to a stop, deadpan
        *[act(f'pig{i + 1}', [r(ROOF[0] + dx), r(ROOF[1] + 0.02), r(ROOF[2] + dz)], 160 + 40 * i, 'idle', 'neutral', scale=0.8,
              keys=[k(r(LAND4 + 0.02 + 0.04 * i), to=[r(ROOF[0] + dx + (2.4 if i % 2 else -2.0)), r(ROOF[1] + 2.6 + 0.4 * i), r(ROOF[2] + dz + 1.5)], dur=0.55, clip='fly', then='fly', ease='out', face='move')]) for i, (dx, dz) in enumerate(PIGS4)]],
        props=[P('vane4', 'weathervane', pos=ROOF, opts={'roof': {'len': 6.0}, 'spin': [[0.0, 0.0]], 'yaw0': 0.6}),
               *[P(f'fth4{i}', 'feather', pos=[r(ROOF[0] + dx), r(ROOF[1] + 0.6), r(ROOF[2] + dz)], opts={'at': r(LAND4 + 0.1), 'fall': 0.8, 'dur': 0.8, 's': 1.0}) for i, (dx, dz) in enumerate(PIGS4[:2])]],
        fx=[{'type': 'shake', 'at': LAND4, 'dur': 0.15, 'amount': 0.014}],
        cams=[FC(0.0, [r(ROOF[0] - 3.4), r(ROOF[1] + 0.9), r(ROOF[2] + 3.6)], [[ONR[0], r(ONR[1] + 2.45), ONR[2]], [ONR[0], r(ONR[1] - 0.3), ONR[2]], [r(ROOF[0] + 0.3), r(ROOF[1] + 1.6), ROOF[2]], [r(ROOF[0] - 2.6), ROOF[1], ROOF[2]]], top=0.14, bottom=0.74, drift=(0.08, 0.0, -0.06))])
st.cue('sfx:thud', 'S04', LAND4, 0.45); st.cue('sfx:boing', 'S04', r(LAND4 + 0.16), 0.3); st.cue('whoosh', 'S04', r(LAND4 + 0.04), 0.25, 0.35, 700, 2000)

# 5: since then he bounces... Down the pavement toward us he bounces along like a pogo stick, feet together, squashing at each landing, stretching at
#    each take-off; a woman walking the other way ducks as he hops right over her
D5 = st.dur('S05')
PATH5 = [[7.2, 6.4], [7.2, 4.2], [7.2, 1.9], [7.2, -0.3]]
K5, T5 = HOPS(0.0, PATH5, [1.2, 2.5, 1.1], r(D5 / 3))
W5 = [6.1, 0, 1.6]                                                       # (audit) beside his path: in it she hid him
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [PATH5[0][0], 0, PATH5[0][1]], 180, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K5, *T5]),
        act('passante', W5, 0, 'stand', 'neutral', keys=[k(0.0, look=[7.2, 2.4, 3.0]), k(0.0, to=[W5[0], 0, r(W5[2] + 0.9)], dur=D5, clip='walk', then='walk', ease='linear', face='keep'),
            k(0.24, toon={'sq': [1.12, 0.8, 1.12], 'bend': {'spine': [0.5, 0, 0, 1, None]}, 'touch': {'L': ['face', 0.3, 0.9, 0.05, 1, 0.03], 'R': ['face', -0.3, 0.9, 0.05, 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'},
                           'hairUp': 0.8, 'face': {'lid': 1.0, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.06, toonEase='out'),   # she ducks under him...
            k(0.62, toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.0, 'eye': 0.5, 'brow': 0.9, 'mouth': 'O'}}, toonDur=0.12)])],   # ...and comes up, staring
        cams=[FC(0.0, [6.3, 0.55, -3.8], [[7.2, 2.4, -0.3], [7.2, 3.7, 3.0], [7.2, 0.0, 4.2], [7.2, 0.0, -0.3]], top=0.1, bottom=0.8)])
for i in range(3): st.cue('sfx:boing', 'S05', r(D5 / 3 * (i + 1) - 0.03), 0.22)

# 6: ...everywhere. At a café, his coffee cup in his hand: a squash, and he bounces straight up out of the frame; the cup stays hanging in the air where
#    his hand was; he drops back into the frame and his hand closes on it again; he looks at us, deadpan, and squashes for the next one
D6 = st.dur('S06'); UP6 = 0.14; DOWN6 = 0.6
C6 = [7.4, 0, -9.0]
CUP6 = [r(C6[0] - 0.36), 1.22, r(C6[2] - 0.14)]
HOLD6 = lambda w: {'reach': {'R': [CUP6[0], r(CUP6[1] - 0.04), r(CUP6[2] + 0.02), w, 0.05]}, 'hands': {'R': 'grip'}}
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('mec', C6, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD6(1), 'face': DEAD}, toonDur=0.0),
            k(r(UP6 - 0.06), toon={**HOLD6(1), 'sq': SQ, 'face': {'lid': 0.5}}, toonDur=0.04, toonEase='in'),   # a squash...
            k(UP6, to=[C6[0], 2.4, C6[2]], dur=0.23, ease='out', face='keep'), k(UP6, toon={**HOLD6(0), 'sq': ST, 'hairUp': 0.6, 'face': DEAD}, toonDur=0.04, toonEase='out'),   # ...up and out, the cup left behind...
            k(r(UP6 + 0.23), to=C6, dur=r(DOWN6 - UP6 - 0.23), ease='in', face='keep'),
            k(DOWN6, toon={**HOLD6(1), 'sq': SQ, 'face': DEAD}, toonDur=0.03, toonEase='in'),   # ...back down, his hand on it again...
            k(r(DOWN6 + 0.08), toon={**HOLD6(1), 'sq': [0.97, 1.03, 0.97], 'face': {'lid': 0.45, 'gx': 0.0}}, toonDur=0.08),
            k(r(D6 - 0.12), toon={**HOLD6(1), 'sq': SQ, 'face': DEAD}, toonDur=0.06, toonEase='in')])],   # ...and the next squash
        props=[P('mug6', 'mug', pos=CUP6, ry=RY), P('table6', 'table', pos=[r(C6[0] - 0.75), 0, r(C6[2] + 0.1)])],   # the cup never moves
        cams=[FC(0.0, [5.9, 1.3, r(C6[2] - 1.5)], [[C6[0], 2.25, C6[2]], [C6[0], 0.6, C6[2]], [CUP6[0], CUP6[1], CUP6[2]], [r(C6[0] - 0.6), 1.2, r(C6[2] + 0.5)]], top=0.06, bottom=0.8)])   # his head out of the top when he is up
st.cue('sfx:boing', 'S06', UP6, 0.25); st.cue('sfx:boing', 'S06', DOWN6, 0.15)

# 7: the town hall declared him... Over the clerk's shoulder, a form on the counter: DÉCLARATION, OISEAU, AVION, OBJET VOLANT; her pen goes down the boxes
#    while behind the counter he bobs up and down; she ticks OBJET VOLANT
D7 = st.dur('S07'); TICK7 = 0.72
OFFICE = {'title': 'MAIRIE', 'plate': False, 'map': False}
VIS = [0.0, 0, 0.45]; CLERK = [0.3, 0, -1.65]
FORM = [0.05, 0.836, -0.88]
BOXZ = [r(FORM[2] + 0.09 - 0.12 * i) for i in range(3)]
PEN7 = lambda i, y=0.9: {'reach': {'R': [r(FORM[0] + 0.2), y, BOXZ[i], 1, 0.04]},   # (stills 1) beside the boxes: over them her arm hid the words
              'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}}
K7, T7 = HOPS(0.0, [[VIS[0], VIS[2]]] * 4, [1.1, 1.1, 1.1], r(D7 / 3))
st.shot('S07', 'mairie', setOpts=OFFICE, actors=[
        act('mec', VIS, 180, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K7, *T7]),
        act('agent', CLERK, 0, 'stand', 'neutral', keys=[k(0.0, look=[FORM[0], FORM[1], FORM[2]]), k(0.0, toon={**PEN7(0), 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.0),
            k(0.24, toon={**PEN7(1), 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.12, toonEase='inOut'),   # OISEAU... AVION...
            k(0.5, toon={**PEN7(2), 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.12, toonEase='inOut'),
            k(r(TICK7 - 0.04), toon={**PEN7(2, 0.85), 'face': {'lid': 0.4, 'gy': 0.6, 'brow': 0.4}}, toonDur=0.04, toonEase='in')])],   # ...OBJET VOLANT: tick
        props=[P('form7', 'formCheck', pos=FORM, rot=[round(-PI / 2, 4), 0, round(PI, 4)], opts={'w': 0.42, 'tickAt': TICK7})],
        cams=[cam(0.0, [-0.15, 1.42, -1.42], [-0.12, 1.4, -1.36], [FORM[0], 0.98, r(FORM[2] + 0.28)], [FORM[0], 0.98, r(FORM[2] + 0.3)], lens=46)])   # (stills 1) an insert: the form big, him bobbing behind the counter (with him in the fit the form was a speck)
st.cue('sfx:paper', 'S07', TICK7, 0.25)

# 8: ...a flying object. In front of the counter: the clerk leans out with a sticker, her head going up and down with his bounces, times it and slaps
#    « F-MEC » on his chest at the bottom of one; he bounces on with it
D8 = st.dur('S08'); SLAP8 = 0.5
CHEST = [VIS[0], 1.5, r(VIS[2] + 0.13)]
K8, T8 = HOPS(0.0, [[VIS[0], VIS[2]]] * 4, [1.0, 1.0, 1.0], r(D8 / 3))
st.shot('S08', 'mairie', setOpts=OFFICE, actors=[
        act('mec', VIS, -140, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K8, *T8]),   # (audit) cheated to the side camera
        act('agent', [0.15, 0, -1.25], -40, 'stand', 'determined', keys=[k(0.0, look=[VIS[0], 2.4, VIS[2]]),
            k(0.0, toon={'reach': {'R': [0.25, 1.65, -0.55, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'brow': -0.3, 'gy': -0.5}}, toonDur=0.0),
            k(0.12, look=[VIS[0], 1.4, VIS[2]]), k(0.26, look=[VIS[0], 2.6, VIS[2]]), k(0.4, look=[VIS[0], 1.4, VIS[2]]),   # her head goes up and down with him...
            k(r(SLAP8 - 0.06), toon={'reach': {'R': [CHEST[0], CHEST[1], r(CHEST[2] + 0.02), 1, 0.03]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.3, 'brow': -0.6, 'mouth': 'clench'}}, toonDur=0.06, toonEase='in'),   # ...SLAP
            k(r(SLAP8 + 0.16), toon={'reach': {'R': [0.25, 1.2, -0.7, 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.14)])],
        props=[P('stkA8', 'regSticker', on={'actor': 'agent', 'hand': 'R', 'offset': [0.0, 0.05, 0.03], 'face': 'camera'}, opts={'w': 0.34}, keys=[k(SLAP8, visible=False)]),
               P('stkB8', 'regSticker', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.3, 0.16]}, opts={'w': 0.34}, keys=[k(0.0, visible=False), k(SLAP8, visible=True)])],
        cams=[FC(0.0, [-2.6, 1.6, -0.3], [[VIS[0], 2.45, VIS[2]], [VIS[0], 0.0, VIS[2]], [VIS[0], 3.4, VIS[2]], [0.15, 2.3, -1.25]], top=0.08, bottom=0.8)])
st.cue('clack', 'S08', SLAP8, 0.35)

# 9: he must pass the pilot's licence. The exam room: in a leather cap and goggles he bounces in his chair in front of the examiner's desk; the
#    examiner, clipboard in hand, follows him up and down with his head over his glasses
D9 = st.dur('S09')
EXAMSET = {'title': 'PERMIS DE PILOTE', 'plate': False, 'map': False}
PIL = [0.0, 0, 0.3]; EXM = [0.25, 0, -1.6]
def SEATHOPS(t0, n, dt, h, p=PIL):
    keys, toon = [], []
    for i in range(n):
        t = r(t0 + dt * i)
        keys += [k(t, to=[p[0], h, p[2]], dur=r(dt / 2), ease='out', clip='sit', glide=True, face='keep'), k(r(t + dt / 2), to=p, dur=r(dt / 2), ease='in', clip='sit', glide=True, face='keep')]
        toon += [k(t, toon={'sq': ST}, toonDur=0.04, toonEase='out'), k(r(t + dt - 0.03), toon={'sq': SQ}, toonDur=0.03, toonEase='in')]
    return keys, toon
K9, T9 = SEATHOPS(0.0, 4, r(D9 / 4), 0.45)
st.shot('S09', 'mairie', setOpts=EXAMSET, actors=[
        act('pilote', PIL, 180, 'sit', 'unimpressed', keys=[k(0.0, look=[EXM[0], 1.6, EXM[2]]), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K9, *T9]),
        act('exam', EXM, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[PIL[0], 1.5, PIL[2]]), k(0.0, toon={'reach': {'L': [r(EXM[0] + 0.2), 1.25, r(EXM[2] + 0.35), 1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.5, 'gy': -0.2}}, toonDur=0.0),
            *[k(r(0.12 + D9 / 4 * i), look=[PIL[0], 2.0, PIL[2]]) for i in range(4)], *[k(r(0.12 + D9 / 8 + D9 / 4 * i), look=[PIL[0], 1.45, PIL[2]]) for i in range(4)]])],   # his head going up and down
        props=[P('chair9', 'chair', pos=[PIL[0], 0, r(PIL[2] + 0.05)], ry=180), P('clip9', 'clipboardX', on={'actor': 'exam', 'hand': 'L', 'offset': [0.0, 0.05, 0.05]}, opts={'w': 0.26})],
        cams=[FC(0.0, [-1.9, 1.4, 0.8], [[PIL[0], 2.85, PIL[2]], [PIL[0], 0.3, PIL[2]], [EXM[0], 2.35, EXM[2]], [EXM[0], 0.9, EXM[2]]], top=0.12, bottom=0.76, drift=(0.06, 0.0, -0.05))])
for i in range(4): st.cue('sfx:squeak', 'S09', r(D9 / 4 * (i + 1) - 0.03), 0.12)

# 10: he failed it... One bounce too many: he shoots up into the ceiling lamp, CLONK, and drops back into his chair wearing its shade, deadpan
D10 = st.dur('S10'); HIT10 = 0.16; BACK10 = 0.36
LAMP = [PIL[0], 3.0, PIL[2]]
st.shot('S10', 'mairie', setOpts=EXAMSET, actors=[
        act('pilote', PIL, 180, 'sit', 'unimpressed', keys=[k(0.0, look=[EXM[0], 1.6, EXM[2]]), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.0, to=[PIL[0], 0.8, PIL[2]], dur=HIT10, ease='out', clip='sit', glide=True, face='keep'), k(0.0, toon={'sq': ST}, toonDur=0.03),   # up into the lamp...
            k(HIT10, toon={'sq': [1.12, 0.86, 1.12], 'face': {'lid': 1.0, 'brow': -0.5}}, toonDur=0.03, toonEase='out'),   # ...CLONK...
            k(r(HIT10 + 0.02), to=PIL, dur=r(BACK10 - HIT10 - 0.02), ease='in', clip='sit', glide=True, face='keep'),
            k(BACK10, toon={'sq': SQ, 'face': DEAD}, toonDur=0.03, toonEase='in'), k(r(BACK10 + 0.08), toon={'sq': [1.0, 1.0, 1.0], 'face': DEAD}, toonDur=0.08)]),   # ...back in the chair, wearing its shade
        act('exam', EXM, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[PIL[0], 2.6, PIL[2]]), k(0.0, toon={'reach': {'L': [r(EXM[0] + 0.2), 1.25, r(EXM[2] + 0.35), 1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.4}}, toonDur=0.0),
            k(r(BACK10 + 0.04), look=[PIL[0], 1.6, PIL[2]]), k(r(BACK10 + 0.06), toon={'reach': {'L': [r(EXM[0] + 0.2), 1.25, r(EXM[2] + 0.35), 1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.55, 'brow': -0.4}}, toonDur=0.08)])],
        props=[P('chair10', 'chair', pos=[PIL[0], 0, r(PIL[2] + 0.05)], ry=180), P('lamp10', 'pendantLamp', pos=LAMP, opts={'drop': 0.55}, keys=[k(HIT10, visible=False)]),
               P('shade10', 'lampShade', pos=[LAMP[0], r(LAMP[1] - 0.55 - 0.15), LAMP[2]], rot=[round(PI, 4), 0, 0], keys=[k(0.0, visible=False), k(HIT10, visible=True), k(HIT10, attach='pilote', joint='head', offset=[0.0, 0.5, 0.0], rot=[0.0, 0.0, 0.1])]),   # (stills 1) a drum shade with its flex: the cone read as a straw hat
               P('clip10', 'clipboardX', on={'actor': 'exam', 'hand': 'L', 'offset': [0.0, 0.05, 0.05]}, opts={'w': 0.26})],
        cams=[FC(0.0, [-1.6, 1.5, 1.1], [[PIL[0], 3.05, PIL[2]], [PIL[0], 0.5, PIL[2]], [EXM[0], 2.3, EXM[2]]], top=0.06, bottom=0.78)])
st.cue('clack', 'S10', HIT10, 0.4)

# 11: ...three times. On the examiner's clipboard (EXAMEN DE PILOTE), three red crosses slash ESSAI 1, 2, 3, one after the other (RECALÉ card)
D11 = st.dur('S11')
CB = [0.0, 1.3, -0.9]
st.shot('S11', 'mairie', setOpts=EXAMSET, actors=[],
        props=[P('clip11', 'clipboardX', pos=CB, rot=[-0.35, 0, 0], opts={'w': 0.3, 'marks': [0.08, 0.26, 0.44]})],
        cams=[FC(0.0, [0.0, 1.55, -0.2], [[r(CB[0] - 0.17), r(CB[1] + 0.22), CB[2]], [r(CB[0] + 0.17), r(CB[1] - 0.24), CB[2]]], top=0.16, bottom=0.7, level=False)])
for i, t_ in enumerate([0.08, 0.26, 0.44]): st.cue('sfx:paper', 'S11', t_, 0.25)

# 12: yesterday he stopped bouncing. Down the street he bounces higher and higher toward us, the passers-by stopping; at the top of a bounce he stops
#     dead in mid-air: his tie and hair settle; below, a woman and a boy look up
D12 = st.dur('S12'); STOP12 = 0.95
AIR = [7.0, 4.2, 1.0]
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [7.0, 0, 7.5], 180, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.0, to=[7.0, 2.6, 6.0], dur=0.22, ease='out', face='keep'), k(0.22, to=[7.0, 0, 4.5], dur=0.22, ease='in', face='keep'),
            k(0.0, toon={'sq': ST, 'hairUp': 0.5}, toonDur=0.04), k(0.41, toon={'sq': SQ}, toonDur=0.03, toonEase='in'),
            k(0.45, to=AIR, dur=r(STOP12 - 0.45), ease='out', face='keep'), k(0.45, toon={'sq': ST, 'hairUp': 0.6}, toonDur=0.04, toonEase='out'),   # higher...
            k(STOP12, toon={'sq': [1.03, 0.98, 1.03], 'hairUp': 0.3, 'face': {'lid': 0.4}}, toonDur=0.08, toonEase='out'),   # ...and stops dead up there
            k(r(STOP12 + 0.25), toon={'sq': [1.0, 1.0, 1.0], 'face': DEAD}, toonDur=0.2, toonEase='inOut')]),
        act('voisine', [5.7, 0, -0.6], 30, 'stand', 'neutral', keys=[k(0.0, look=[7.0, 1.6, 4.0]), k(r(STOP12 + 0.15), look=AIR), k(r(STOP12 + 0.2), toon={'face': {'lid': 0.0, 'eye': 0.4, 'brow': 0.8, 'mouth': 'o'}}, toonDur=0.1)]),
        act('gamin', [8.4, 0, -0.4], -30, 'stand', 'happy', keys=[k(0.0, look=[7.0, 1.6, 4.0]), k(r(STOP12 + 0.25), look=AIR), k(r(STOP12 + 0.3), toon={'face': {'lid': 0.0, 'eye': 0.5, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.1)])],
        cams=[FC(0.0, [7.0, 0.6, -3.4], [[AIR[0], r(AIR[1] + 2.45), AIR[2]], [AIR[0], AIR[1], AIR[2]], [5.7, 2.2, -0.6], [8.4, 1.6, -0.4], [7.0, 2.4, 6.0]], top=0.08, bottom=0.86, drift=(0.0, 0.0, 0.15))])   # (audit) low and closer, them at the sides
st.cue('sfx:boing', 'S12', 0.41, 0.2); st.cue('sfx:boing', 'S12', 0.45, 0.25); st.cue('sfx:squeak', 'S12', STOP12, 0.2)

# 13: in mid-flight. From below, against the sky: he hangs there; he looks down (his eyes first) at the nothing under his feet, then at us, deadpan
D13 = st.dur('S13')
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[
        act('mec', AIR, 180, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.1, toon={'face': {'lid': 0.3, 'gy': 0.8}}, toonDur=0.06), k(0.18, look=[AIR[0], 0.0, r(AIR[2] - 0.6)]),   # his eyes down, then his head...
            k(0.55, toon={'face': {'lid': 0.3, 'gy': 0.0}}, toonDur=0.06), k(0.62, look='camera'), k(0.7, toon={'sq': [1.0, 1.015, 1.0], 'face': DEAD}, toonDur=0.2)])],   # ...then to us
        cams=[FC(0.0, [6.0, 1.3, -1.6], [[AIR[0], r(AIR[1] + 2.45), AIR[2]], [AIR[0], r(AIR[1] - 0.1), AIR[2]], [r(AIR[0] - 0.5), r(AIR[1] + 1.5), AIR[2]], [r(AIR[0] + 0.5), r(AIR[1] + 1.5), AIR[2]]], top=0.14, bottom=0.74, drift=(0.0, 0.0, 0.1))])

# 14: the pigeons built their nest on his head. Closer, up in the sky: a pigeon lands on his head, then another; a nest appears under them, eggs pop in
#     one, two, three; a pigeon pecks; a slow blink
D14 = st.dur('S14'); HEAD14 = [AIR[0], r(AIR[1] + 2.5), AIR[2]]
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[
        act('mec', AIR, 180, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.25, toon={'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.5, 'gy': -0.5}}, toonDur=0.05), k(0.4, toon={'face': {'lid': 0.45, 'gy': 0.0}}, toonDur=0.1),   # the landing presses his head, his eyes up...
            k(0.5, toon={'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.5, 'gy': -0.4}}, toonDur=0.05), k(0.7, toon={'face': DEAD}, toonDur=0.1),
            k(1.2, toon={'sq': [1.0, 1.012, 1.0], 'face': {'lid': 0.45, 'gy': -0.6, 'gx': 0.2}}, toonDur=0.12), k(1.62, toon={'sq': [1.0, 0.996, 1.0], 'face': {'lid': 0.5, 'gy': -0.5, 'gx': -0.2}}, toonDur=0.12),   # his eyes up at each egg...
            k(1.95, toon={'sq': [1.0, 1.01, 1.0], 'face': DEAD}, toonDur=0.15),
            k(2.15, toon={'face': {'lid': 1.0}}, toonDur=0.14), k(2.45, toon={'sq': [1.0, 1.01, 1.0], 'face': DEAD}, toonDur=0.18)]),   # ...a slow blink
        act('pig1', [r(HEAD14[0] + 2.2), r(HEAD14[1] + 1.2), r(HEAD14[2] + 1.0)], -120, 'fly', 'neutral', scale=0.8, keys=[k(0.0, to=[r(HEAD14[0] + 0.06), HEAD14[1], r(HEAD14[2] + 0.06)], dur=0.25, clip='fly', then='idle', ease='out', face='keep'), k(1.0, clip='peck', blend=0.1)]),
        act('pig2', [r(HEAD14[0] - 2.0), r(HEAD14[1] + 1.0), r(HEAD14[2] + 0.8)], 110, 'fly', 'neutral', scale=0.8, keys=[k(0.0, to=[r(HEAD14[0] - 1.0), r(HEAD14[1] + 0.6), r(HEAD14[2] + 0.4)], dur=0.3, clip='fly', then='fly', ease='linear', face='keep'),
                                                                                                                   k(0.3, to=[r(HEAD14[0] - 0.08), HEAD14[1], r(HEAD14[2] - 0.05)], dur=0.2, clip='fly', then='idle', ease='out', face='keep')])],
        props=[P('nest14', 'nest', pos=[HEAD14[0], r(HEAD14[1] - 0.06), HEAD14[2]], scale=0.42, opts={'layAt': [1.25, 1.55, 1.85], 'max': 3}, keys=[k(0.0, scale=0.001, dur=0.0), k(0.8, scale=0.42, dur=0.12, ease='outBack')]),
               P('fth14', 'feather', pos=[r(HEAD14[0] + 0.3), r(HEAD14[1] + 0.3), r(HEAD14[2] + 0.2)], opts={'at': 0.3, 'fall': 1.6, 'dur': 2.0, 's': 1.2})],
        cams=[FC(0.0, [r(AIR[0] - 1.1), r(AIR[1] + 0.7), r(AIR[2] - 1.5)], [[HEAD14[0], r(HEAD14[1] + 1.1), HEAD14[2]], [AIR[0], r(AIR[1] + 1.25), AIR[2]], [r(AIR[0] - 0.4), r(AIR[1] + 2.0), AIR[2]], [r(AIR[0] + 0.4), r(AIR[1] + 2.0), AIR[2]]], top=0.12, bottom=0.7, drift=(0.08, 0.0, 0.06))])   # (stills 1) from below his head: the sky behind (at his height a facade made him stand on the ground)
st.cue('whoosh', 'S14', 0.15, 0.18, 0.3, 700, 2000); st.cue('whoosh', 'S14', 0.4, 0.14, 0.3, 700, 2000); st.cue('sfx:pop', 'S14', 0.8, 0.2)
for t_ in [1.25, 1.55, 1.85]: st.cue('sfx:pop', 'S14', t_, 0.12)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 0.7, 'mec', 'sit'), ('S02', 0.27, 'mec', 'boing'), ('S04', 0.3, 'mec', 'accordion'), ('S05', 0.4, 'mec', 'pogo'), ('S06', 0.3, 'mec', 'cup'), ('S08', 0.7, 'mec', 'sticker'),
           ('S09', 0.6, 'pilote', 'exam'), ('S10', 0.45, 'pilote', 'shade'), ('S12', 1.4, 'mec', 'stop'), ('S13', 0.4, 'mec', 'down'), ('S14', 2.0, 'mec', 'nest')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S07', 0.85, 'form7', 'form'), ('S08', 0.75, 'stkB8', 'sticker'), ('S11', 0.6, 'clip11', 'clipboard')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S11', 'RECALÉ', at=0.5)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}
st.write("Le ressort", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'pilote': {**MEC, 'hat': 'aviator'},   # the same man in his pilot's cap
    'agent': {'preset': 'madame', 'seed': 611, 'suit': '#6E7F9E', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'exam': {'preset': 'proviseur', 'seed': 612, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'passante': {'preset': 'madame', 'seed': 613, 'suit': '#C255C8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'voisine': {'preset': 'madame', 'seed': 614, 'suit': '#3A9BDC', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'gamin': {'preset': 'gamin', 'seed': 615, 'suit': '#52B76A', 'build': {'height': 0.55, 'headScale': 1.35}, 'toon': EX},
    **{f'pig{i}': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': i}} for i in range(1, 4)},
})
