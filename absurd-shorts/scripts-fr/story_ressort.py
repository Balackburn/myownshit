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
Natural look; cycle 23 tools: props_ressort.js (springCoil, regSticker, formCheck, clipboardX, lampShade) and the 'aviator' cap (human.js).
Pass 2 (reviews 6.5 / 6.0): the squashes on seats pivot on the seat (no more sinking to the floor) and the BOING eye-pop held five frames; the
launch seen whole from lower; soft tapered streaks; the ride with hands and a wind-blown face; side on, the hop right over the woman's head; a
white cup and a bistro table; the form insert higher (OBJET VOLANT clear of the captions) with a flat ink tick and her red pen, him bouncing whole
first; the sticker slapped on a landing, CLAC; ball bounces in the chair, the examiner's head nodding after him, his face and the new cap to us;
CLONK into the lamp, the bare bulb swinging; three rising bounces and a stop 7 m up with the onlookers below; a twig nest on his hair seen from
above with the street far below, three eggs on its near rim (props_ressort.js: twigNest, bistroTable; props_echo.js: soft streaks;
props_hoquet.js: a lamp whose shade comes off)."""
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
STREET = {'eiffelStyle': 'v2', 'clear': [-6.0, 14.0]}                      # no tree or lamp on the right pavement around him ((pass 2) further down: a lamp sat on his crown in the first frame)
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
#    (pass 2, reviews 6.5 / 6.0: the squash sank through the seat to the pavement, slits for eyes, two frames; he left the frame at once; the speed
#    lines read as bench legs) the squash pivots on the seat (lifted by what it takes off his height), the head stretched against it so the eyes
#    pop, held five frames, quivering; cut wider and lower: he goes up stretched, arms up, hands open, in the frame three frames, then gone; the
#    spring kicks up after him and boings on the empty bench; soft streaks beside him
D2 = st.dur('S02'); SPR2 = 0.24; GO2 = 0.42
SPRING = [BENCH[0] - 0.05, 0.47, 0.0]
POP2 = {'lid': 0.0, 'eye': 1.0, 'eyeScale': 1.7, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'O'}
SQS = lambda sq, hs, face: {'sq': sq, 'scl': {'head': hs}, 'hairUp': 1.0, 'face': face}
UPARMS = {'touch': {'L': ['torso', 0.24, 1.32, 0.05, 1, 0.05], 'R': ['torso', -0.24, 1.32, 0.05, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}   # (pass 2) hands open just over his head (reaching for a point 12 m up, the arms were two pillars)
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', SEAT, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.55, 'cheeks': 0.3}}, toonDur=0.0),
            k(SPR2, to=[SEAT[0], 0.12, SEAT[2]], dur=0.03, ease='out', clip='sit', glide=True, face='keep'),   # (pass 2) lifted by what the squash takes off: his seat stays on the bench
            k(SPR2, toon=SQS([1.24, 0.74, 1.24], [0.84, 1.28, 0.84], POP2), toonDur=0.03, toonEase='out'),   # BOING: squashed into the seat, the head stretched against it, eyes popping...
            k(r(SPR2 + 0.06), toon=SQS([1.2, 0.78, 1.2], [0.86, 1.25, 0.86], {**POP2, 'tremble': 1.0}), toonDur=0.04), k(r(SPR2 + 0.12), toon=SQS([1.24, 0.74, 1.24], [0.84, 1.28, 0.84], {**POP2, 'tremble': 1.0}), toonDur=0.04),   # ...held five frames, quivering...
            k(GO2, clip='stand', blend=0.04),
            k(GO2, to=[SEAT[0], 0.9, SEAT[2]], dur=0.1, ease='in', face='keep'), k(r(GO2 + 0.1), to=[SEAT[0], 7.0, SEAT[2]], dur=0.24, ease='out', face='keep'),   # ...shot up, slow for three frames, then gone...
            k(GO2, toon={**UPARMS, 'sq': [0.72, 1.4, 0.72], 'hairUp': 1.0, 'face': {'lid': 0.0, 'eye': 0.8, 'eyeScale': 1.3, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.04, toonEase='out')])],   # ...stretched like a rubber band, arms up, hands open
        props=[P('bench2', 'bench', pos=BENCH, ry=RY), P('spring2', 'springCoil', pos=SPRING, opts={'at': r(GO2 - 0.02), 'len': 0.75, 'r': 0.1, 'wire': 0.02}),   # (pass 2) it kicks up as he leaves (out under him it stood through his body)
               BURST('boing2', [r(SPRING[0] - 0.5), 1.05, r(SPRING[2] - 0.55)], SPR2, 'BOING !', 0.46),
               P('spd2', 'speedLines', **FLY([[GO2, SEAT[0], 1.2, SEAT[2]], [r(GO2 + 0.3), SEAT[0], 4.6, SEAT[2]]]), face='camera', opts={'n': 6, 'len': 1.2, 'w': 1.15, 'angle': 1.57, 'soft': True, 'taper': True, 'alpha': 0.6, 'at': [[GO2, r(GO2 + 0.4)]]})],   # (pass 2) soft wedges beside him (outlined, from the seat to the pavement, they read as bench legs)
        cams=[FC(0.0, [6.3, 0.72, -1.15], [[SEAT[0], 2.05, SEAT[2]], [SEAT[0], 0.45, SEAT[2]], [r(SEAT[0] - 0.4), 0.9, -0.55], [r(SEAT[0] - 0.4), 0.9, 0.55]], top=0.2, bottom=0.76),   # low and close on the squash...
              FC(GO2, [5.4, 0.45, -2.3], [[SEAT[0], 3.7, SEAT[2]], [SEAT[0], 0.0, SEAT[2]], [BENCH[0], 0.9, -0.85], [BENCH[0], 0.9, 0.85]], top=0.06, bottom=0.82, level=False)])   # (pass 2) ...wider, looking up: the stretched launch in the frame, then the empty bench and its spring
st.cue('sfx:boing', 'S02', SPR2, 0.5); st.cue('whoosh', 'S02', GO2, 0.4, 0.6, 300, 1500)

# 3: he bounced... Low on the pavement, the camera rising with him as he shoots up past the windows, stretched, speed lines under him
#    (pass 2: arms like pillars without hands, half-lidded eyes. Decision: the wind of the ride blows his face (wide eyes, blown cheeks) without being
#    a take: the BOING stays his only one) his hands open just over his head, cheeks blown, eyes wide in the wind, soft streaks below him
D3 = st.dur('S03')
RIDE = {**UPARMS, 'sq': [0.86, 1.18, 0.86], 'wind': [0.0, -14.0, 0.0]}
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [SEAT[0], 0.6, SEAT[2]], RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.0, to=[SEAT[0], 18.0, SEAT[2]], dur=D3, ease='linear', face=RY),   # (stills 3) the facing given: with 'keep' on a straight-up move he turned side on (a stripe with no face)
            k(0.0, toon={**RIDE, 'face': {'lid': 0.0, 'eye': 0.9, 'eyeScale': 1.25, 'pupilSize': -0.3, 'brow': 1.0, 'mouth': 'O', 'puff': 0.8, 'cheeks': 1.0}}, toonDur=0.0),
            k(0.35, toon={**RIDE, 'face': {'lid': 0.0, 'eye': 1.0, 'eyeScale': 1.3, 'pupilSize': -0.4, 'brow': 1.0, 'mouth': 'scream', 'puff': 0.4, 'cheeks': 1.0}}, toonDur=0.1)])],
        props=[P('spd3', 'speedLines', **FLY([[0.0, SEAT[0], -0.8, SEAT[2]], [D3, SEAT[0], 14.6, SEAT[2]]]), face='camera', opts={'n': 7, 'len': 2.0, 'w': 0.9, 'angle': 1.57, 'soft': True, 'taper': True, 'alpha': 0.65, 'at': [[0.0, D3]]})],   # (pass 2) streaks under him (there were none in the frame)
        cams=[cam(0.0, [5.55, 3.4, -2.1], [5.55, 20.8, -2.1], [SEAT[0], 3.5, 0.0], [SEAT[0], 20.9, 0.0], lens=42)])   # (stills 4) riding up with him on his head and shoulders, the windows streaming down (whole and far he was a stripe 4 % wide)
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

# 5: since then he bounces... Along the pavement he bounces like a pogo stick, feet together, squashing at each landing, stretching at each take-off;
#    a woman in his way ducks as he hops right over her head, then comes up staring after him
#    (pass 2: he passed beside and behind her with his head cut at the top: her duck had no cause) side on: she stands in his path facing us, he
#    sails right over her head in the middle of the frame, whole at the top of the hop, his face to us; she ducks under him and comes up staring
D5 = st.dur('S05')
PATH5 = [[7.2, 6.4], [7.2, 4.2], [7.2, 1.9], [7.2, -0.3]]
K5, T5 = HOPS(0.0, PATH5, [1.2, 2.5, 1.1], r(D5 / 3))
W5 = [7.2, 0, 3.05]                                                      # (pass 2) right under the middle hop
DUCK5 = {'sq': [1.12, 0.8, 1.12], 'bend': {'spine': [0.5, 0, 0, 1, None]}, 'touch': {'L': ['face', 0.3, 0.9, 0.05, 1, 0.03], 'R': ['face', -0.3, 0.9, 0.05, 1, 0.03]}, 'hands': {'L': 'open', 'R': 'open'},
         'hairUp': 0.8, 'face': {'lid': 1.0, 'brow': -0.8, 'mouth': 'clench'}}
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [PATH5[0][0], 0, PATH5[0][1]], 140, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K5, *T5]),   # (audit) turned to us: side on his box head had no face
        act('passante', W5, -90, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.3}}, toonDur=0.0), k(0.2, look=[7.2, 3.2, 4.6]),   # she sees him coming...
            k(0.28, toon=DUCK5, toonDur=0.05, toonEase='out'), k(0.48, toon={**DUCK5, 'sq': [1.1, 0.82, 1.1]}, toonDur=0.1),   # ...ducks under him...
            k(0.56, look=[7.2, 1.8, 0.4]), k(0.56, toon={'sq': [0.96, 1.05, 0.96], 'hairUp': 0.6, 'face': {'lid': 0.0, 'eye': 0.6, 'brow': 0.9, 'mouth': 'O'}}, toonDur=0.08, toonEase='out'),   # ...and comes up staring after him
            k(0.72, toon={'sq': [1.0, 1.0, 1.0], 'hairUp': 0.4, 'face': {'lid': 0.0, 'eye': 0.5, 'brow': 0.8, 'mouth': 'o'}}, toonDur=0.1)])],
        cams=[FC(0.0, [3.6, 1.6, 3.05], [[7.2, 4.95, 3.05], [7.2, 0.0, 1.9], [7.2, 0.0, 4.2], [7.2, 1.75, 3.05]], top=0.08, bottom=0.8)])   # (pass 2) side on across the road: the middle hop over her, whole
for i in range(3): st.cue('sfx:boing', 'S05', r(D5 / 3 * (i + 1) - 0.03), 0.22)

# 6: ...everywhere. At a café, his coffee cup in his hand: a squash, and he bounces straight up out of the frame; the cup stays hanging in the air where
#    his hand was; he drops back into the frame and his hand closes on it again; he looks at us, deadpan, and squashes for the next one
#    (pass 2: a teal cup on a teal window, a plank table, a heap for a landing) a white cup, a round bistro table and a chair, the camera lower (the
#    awning out of the top), a smaller landing squash, his look back to us
D6 = st.dur('S06'); UP6 = 0.14; DOWN6 = 0.6
C6 = [7.4, 0, -9.0]
CUP6 = [r(C6[0] - 0.36), 1.22, r(C6[2] - 0.14)]
HOLD6 = lambda w: {'reach': {'R': [CUP6[0], r(CUP6[1] - 0.04), r(CUP6[2] + 0.02), w, 0.05]}, 'hands': {'R': 'grip'}}
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('mec', C6, RY, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD6(1), 'face': DEAD}, toonDur=0.0),
            k(r(UP6 - 0.06), toon={**HOLD6(1), 'sq': SQ, 'face': {'lid': 0.5}}, toonDur=0.04, toonEase='in'),   # a squash...
            k(UP6, to=[C6[0], 2.4, C6[2]], dur=0.23, ease='out', face='keep'), k(UP6, toon={**HOLD6(0), 'sq': ST, 'hairUp': 0.6, 'face': DEAD}, toonDur=0.04, toonEase='out'),   # ...up and out, the cup left behind...
            k(r(UP6 + 0.23), to=C6, dur=r(DOWN6 - UP6 - 0.23), ease='in', face='keep'),
            k(DOWN6, toon={**HOLD6(1), 'sq': [1.12, 0.88, 1.12], 'face': DEAD}, toonDur=0.03, toonEase='in'),   # ...back down, his hand round it again ((pass 2) a small squash: the big one was a heap)...
            k(r(DOWN6 + 0.06), look='camera'), k(r(DOWN6 + 0.08), toon={**HOLD6(1), 'sq': [0.97, 1.03, 0.97], 'face': {'lid': 0.45, 'gx': 0.0}}, toonDur=0.08),   # ...a look to us...
            k(r(D6 - 0.12), toon={**HOLD6(1), 'sq': SQ, 'face': DEAD}, toonDur=0.06, toonEase='in')])],   # ...and the next squash
        props=[P('mug6', 'mug', pos=CUP6, ry=RY, opts={'color': '#FFFFFF'}), P('table6', 'bistroTable', pos=[r(C6[0] - 0.7), 0, r(C6[2] + 0.1)]),   # (pass 2) a white cup (teal on the teal window it vanished), a bistro table
               P('chair6', 'chair', pos=[r(C6[0] - 0.75), 0, r(C6[2] + 0.75)], ry=200)],   # the cup never moves
        cams=[FC(0.0, [5.9, 1.05, r(C6[2] - 1.4)], [[C6[0], 2.5, C6[2]], [C6[0], 0.6, C6[2]], [r(C6[0] + 0.3), 1.8, r(C6[2] - 0.3)], [CUP6[0], CUP6[1], CUP6[2]], [r(C6[0] - 0.7), 0.74, r(C6[2] + 0.4)]], top=0.12, bottom=0.8)])   # (stills p2) his head in the frame when he is down (it was cut at the top)   # (pass 2) lower: the awning out of the top; his head out of the top when he is up
st.cue('sfx:boing', 'S06', UP6, 0.25); st.cue('sfx:boing', 'S06', DOWN6, 0.15)

# 7: the town hall declared him... From the side: he bounces whole in front of the counter, the clerk's red pen over the form; cut to the form from
#    above: DÉCLARATION, OISEAU, AVION, OBJET VOLANT; her pen goes down the boxes and ticks OBJET VOLANT
#    (pass 2: the payoff line sat in the caption band, a red 3D stick for a tick, no pen, only his trouser legs bobbing at the top) two shots: him
#    whole first, then the insert from higher, the form whole with margins, OBJET VOLANT at two thirds of the height, a flat ink tick, the pen in hand
D7 = st.dur('S07'); TICK7 = 0.72; INS7 = 0.42
OFFICE = {'title': 'MAIRIE', 'plate': False, 'map': False}
VIS = [0.0, 0, 0.45]; CLERK = [0.3, 0, -1.65]
FORM = [0.05, 0.836, -0.88]
BOXZ = [r(FORM[2] + 0.09 - 0.12 * i) for i in range(3)]
PEN7 = lambda i, y=0.9: {'reach': {'R': [r(FORM[0] + 0.2), y, BOXZ[i], 1, 0.04]},   # (stills 1) beside the boxes: over them her arm hid the words
              'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}}
K7, T7 = HOPS(0.0, [[VIS[0], VIS[2]]] * 4, [1.1, 1.1, 1.1], r(D7 / 3))
st.shot('S07', 'mairie', setOpts=OFFICE, actors=[
        act('mec', VIS, 140, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K7, *T7]),   # (audit) cheated to the side camera
        act('agent', CLERK, 0, 'stand', 'neutral', keys=[k(0.0, look=[VIS[0], 2.6, VIS[2]]), k(0.0, toon={**PEN7(0), 'face': {'lid': 0.4, 'gy': -0.3}}, toonDur=0.0),   # (pass 2) her eyes on him first...
            k(0.2, look=[FORM[0], FORM[1], FORM[2]]), k(0.24, toon={**PEN7(1), 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.12, toonEase='inOut'),   # ...then on the form: OISEAU... AVION...
            k(0.5, toon={**PEN7(2), 'face': {'lid': 0.5, 'gy': 0.6}}, toonDur=0.12, toonEase='inOut'),
            k(r(TICK7 - 0.04), toon={**PEN7(2, 0.85), 'face': {'lid': 0.4, 'gy': 0.6, 'brow': 0.4}}, toonDur=0.04, toonEase='in')])],   # ...OBJET VOLANT: tick
        props=[P('form7', 'formCheck', pos=FORM, rot=[round(-PI / 2, 4), 0, round(PI, 4)], opts={'w': 0.42, 'tickAt': TICK7}),
               P('pen7', 'marker', on={'actor': 'agent', 'hand': 'R'}, opts={'color': '#C8202A'})],   # (pass 2) her red pen
        cams=[FC(0.0, [2.4, 1.45, -0.2], [[VIS[0], 3.75, VIS[2]], [VIS[0], 0.0, VIS[2]], [CLERK[0], 2.45, CLERK[2]], [FORM[0], 0.84, FORM[2]]], top=0.12, bottom=0.8),   # (pass 2) from the side: him bouncing whole, her pen over the form...
              cam(INS7, [FORM[0], 2.05, -1.3], [FORM[0], 2.03, -1.28], [FORM[0], 0.83, -0.9], [FORM[0], 0.83, -0.89], lens=42)])   # (pass 2) ...the form from higher: whole, OBJET VOLANT at 63 % of the height (at the bottom it sat in the caption band)
st.cue('sfx:paper', 'S07', TICK7, 0.25)

# 8: ...a flying object. In front of the counter: the clerk leans out with a sticker, her head going up and down with his bounces, times it and slaps
#    « F-MEC » on his chest at the bottom of one; he bounces on with it
#    (pass 2: the slap fell on him in mid-air, her hand at his thigh; the room said nothing of a town hall) the slap on the landing, her hand on the
#    squashed chest, held two frames, CLAC; MAIRIE on the desk front
D8 = st.dur('S08'); SLAP8 = 0.6
CHEST = [VIS[0], 1.16, r(VIS[2] + 0.16)]                                  # (pass 2) his chest squashed on the landing
K8, T8 = HOPS(0.0, [[VIS[0], VIS[2]]] * 4, [1.0, 1.0, 1.0], r(D8 / 3))
SLAPK = lambda: {'reach': {'R': [CHEST[0], CHEST[1], r(CHEST[2] + 0.02), 1, 0.03]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.3, 'brow': -0.6, 'mouth': 'clench'}}
st.shot('S08', 'mairie', setOpts={**OFFICE, 'plate': 'MAIRIE'}, actors=[   # (pass 2) the town hall named on the desk
        act('mec', VIS, -140, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K8, *T8]),   # (audit) cheated to the side camera
        act('agent', [0.15, 0, -1.25], -40, 'stand', 'determined', keys=[k(0.0, look=[VIS[0], 2.4, VIS[2]]),
            k(0.0, toon={'reach': {'R': [0.25, 1.65, -0.55, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'brow': -0.3, 'gy': -0.5}}, toonDur=0.0),
            k(0.12, look=[VIS[0], 2.6, VIS[2]]), k(0.3, look=[VIS[0], 1.3, VIS[2]]), k(0.45, look=[VIS[0], 2.6, VIS[2]]),   # her head goes up and down with him...
            k(r(SLAP8 - 0.06), toon=SLAPK(), toonDur=0.06, toonEase='in'), k(r(SLAP8 + 0.07), toon=SLAPK(), toonDur=0.02),   # ...SLAP on the landing, held two frames
            k(r(SLAP8 + 0.18), toon={'reach': {'R': [0.25, 1.2, -0.7, 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.4, 'mouth': 'smirk'}}, toonDur=0.12)])],
        props=[P('stkA8', 'regSticker', on={'actor': 'agent', 'hand': 'R', 'offset': [0.0, 0.05, 0.03], 'face': 'camera'}, opts={'w': 0.34}, keys=[k(SLAP8, visible=False)]),
               P('stkB8', 'regSticker', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.3, 0.16]}, opts={'w': 0.34}, keys=[k(0.0, visible=False), k(SLAP8, visible=True)]),
               BURST('clac8', [r(VIS[0] - 0.45), 1.75, r(VIS[2] + 0.2)], SLAP8, 'CLAC !', 0.34)],   # (pass 2) the impact accent
        cams=[FC(0.0, [-2.6, 1.6, -0.3], [[VIS[0], 2.45, VIS[2]], [VIS[0], 0.0, VIS[2]], [VIS[0], 3.4, VIS[2]], [0.15, 2.3, -1.25]], top=0.08, bottom=0.8)])
st.cue('clack', 'S08', SLAP8, 0.35)

# 9: he must pass the pilot's licence. The exam room: in a leather cap and goggles he bounces in his chair in front of the examiner's desk; the
#    examiner, clipboard in hand, follows him up and down with his head over his glasses
#    (pass 2: the bounces hovered, the squash went through the chair, his face turned away, the goggles unreadable, the sign cut to « ILOTE », the
#    examiner's head never followed) ball bounces (fast off the seat, round at the top, three frames squashed on the seat, lifted so his seat stays
#    on it), the camera in front of him three-quarters, the new round cap with big goggles, no wall sign, the examiner's head nodding up and down two
#    frames behind him
D9 = st.dur('S09')
EXAMSET = {'title': 'PERMIS DE PILOTE', 'plate': False, 'map': False, 'banner': False}   # (pass 2) no sign rather than half of one
PIL = [0.0, 0, 0.3]; EXM = [0.25, 0, -1.6]
SQS9 = [1.16, 0.84, 1.16]
def SEATHOPS(t0, n, dt, h, p=PIL):
    """(pass 2) n ball bounces in a chair from t0, dt each: up on an ease-out (0.4 of it), down on an ease-in (0.4), three frames squashed on the seat
    (0.2), lifted by what the squash takes off so his seat stays on the chair"""
    keys, toon = [], []
    for i in range(n):
        t = r(t0 + dt * i); tu = r(dt * 0.4)
        keys += [k(t, to=[p[0], h, p[2]], dur=tu, ease='out', clip='sit', glide=True, face='keep'), k(r(t + tu), to=[p[0], 0.08, p[2]], dur=tu, ease='in', clip='sit', glide=True, face='keep')]
        toon += [k(t, toon={'sq': ST, 'face': DEAD}, toonDur=0.04, toonEase='out'), k(r(t + tu * 0.6), toon={'sq': [1.0, 1.0, 1.0], 'face': DEAD}, toonDur=0.05),
                 k(r(t + 2 * tu - 0.02), toon={'sq': SQS9, 'face': {'lid': 0.6}}, toonDur=0.02, toonEase='in')]
    return keys, toon
K9, T9 = SEATHOPS(0.0, 4, r(D9 / 4), 0.42)
CLIPR = {'reach': {'L': [r(EXM[0] + 0.2), 1.25, r(EXM[2] + 0.35), 1, 0.05]}, 'hands': {'L': 'grip'}}
NOD9 = lambda up: {**CLIPR, 'bend': {'neck': [(-0.32 if up else 0.22), 0, 0, 1, None]}, 'face': {'lid': (0.3 if up else 0.55), 'gy': (-0.5 if up else 0.3)}}
st.shot('S09', 'mairie', setOpts=EXAMSET, actors=[
        act('pilote', PIL, 165, 'sit', 'unimpressed', keys=[k(0.0, look={'point': [EXM[0], 1.6, EXM[2]], 'cheat': 0.45}), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K9, *T9]),   # (pass 2) cheated to us
        act('exam', EXM, -30, 'stand', 'unimpressed', keys=[k(0.0, look=[PIL[0], 1.5, PIL[2]]), k(0.0, toon=NOD9(False), toonDur=0.0),
            *[k(r(D9 / 4 * i + 0.1 + 0.07), toon=NOD9(True), toonDur=0.08, toonEase='out') for i in range(4)],   # his head up after him, two frames late...
            *[k(r(D9 / 4 * i + 0.3 + 0.07), toon=NOD9(False), toonDur=0.08, toonEase='in') for i in range(4)]])],   # ...and down
        props=[P('chair9', 'chair', pos=[PIL[0], 0, r(PIL[2] + 0.05)], ry=180), P('clip9', 'clipboardX', on={'actor': 'exam', 'hand': 'L', 'offset': [0.0, 0.05, 0.05]}, opts={'w': 0.26})],
        cams=[FC(0.0, [-1.6, 1.4, -1.2], [[PIL[0], 2.85, PIL[2]], [PIL[0], 0.3, PIL[2]], [EXM[0], 2.35, EXM[2]], [EXM[0], 0.9, EXM[2]]], top=0.12, bottom=0.76, drift=(0.05, 0.0, 0.04))])   # (pass 2) in front of him, between them: his face and the goggles (from behind his face was turned away)
for i in range(4): st.cue('sfx:squeak', 'S09', r(D9 / 4 * (i + 1) - 0.03), 0.12)

# 10: he failed it... One bounce too many: he shoots up into the ceiling lamp, CLONK, and drops back into his chair wearing its shade, deadpan
#     (pass 2: the hit happened above the frame, the shade went through his chest) his head into the shade, held two frames, CLONK; the bare bulb
#     swinging after it; the lamp in the frame
D10 = st.dur('S10'); HIT10 = 0.16; BACK10 = 0.4
LAMP = [PIL[0], 3.0, PIL[2]]
st.shot('S10', 'mairie', setOpts=EXAMSET, actors=[
        act('pilote', PIL, 165, 'sit', 'unimpressed', keys=[k(0.0, look={'point': [EXM[0], 1.6, EXM[2]], 'cheat': 0.45}), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.0, to=[PIL[0], 0.62, PIL[2]], dur=HIT10, ease='out', clip='sit', glide=True, face='keep'), k(0.0, toon={'sq': ST}, toonDur=0.03),   # up into the lamp...
            k(HIT10, toon={'sq': [1.14, 0.84, 1.14], 'face': {'lid': 1.0, 'brow': -0.5, 'mouth': 'clench'}}, toonDur=0.03, toonEase='out'),   # ...CLONK, held two frames...
            k(r(HIT10 + 0.07), to=[PIL[0], 0.08, PIL[2]], dur=r(BACK10 - HIT10 - 0.07), ease='in', clip='sit', glide=True, face='keep'),
            k(BACK10, toon={'sq': SQS9, 'face': DEAD}, toonDur=0.03, toonEase='in'), k(r(BACK10 + 0.08), toon={'sq': [1.0, 1.0, 1.0], 'face': DEAD}, toonDur=0.08)]),   # ...back in the chair, wearing its shade
        act('exam', EXM, -30, 'stand', 'unimpressed', keys=[k(0.0, look=[PIL[0], 2.6, PIL[2]]), k(0.0, toon=NOD9(True), toonDur=0.0),
            k(r(BACK10 + 0.04), look=[PIL[0], 1.6, PIL[2]]), k(r(BACK10 + 0.06), toon={**CLIPR, 'face': {'lid': 0.55, 'brow': -0.4}}, toonDur=0.08)])],
        props=[P('chair10', 'chair', pos=[PIL[0], 0, r(PIL[2] + 0.05)], ry=180), P('lamp10', 'pendantLamp', pos=LAMP, opts={'drop': 0.55, 'swing': [[HIT10, 0.6]], 'shadeOff': HIT10}),   # (pass 2) the bare bulb swings on
               P('shade10', 'lampShade', pos=[LAMP[0], r(LAMP[1] - 0.55 - 0.15), LAMP[2]], rot=[round(PI, 4), 0, 0], keys=[k(0.0, visible=False), k(HIT10, visible=True), k(HIT10, attach='pilote', joint='head', offset=[0.0, 0.5, 0.0], rot=[0.0, 0.0, 0.1])]),   # (stills 1) a drum shade with its flex: the cone read as a straw hat
               BURST('clonk10', [r(PIL[0] - 0.55), 2.55, r(PIL[2] - 0.3)], HIT10, 'CLONK !', 0.42),   # (pass 2) the hit named, like the BOING
               P('clip10', 'clipboardX', on={'actor': 'exam', 'hand': 'L', 'offset': [0.0, 0.05, 0.05]}, opts={'w': 0.26})],
        cams=[cam(0.0, [-1.55, 1.45, -1.25], [-1.5, 1.45, -1.2], [0.05, 1.85, 0.3], [0.05, 1.86, 0.3], lens=56)])   # (pass 2) the lamp and the CLONK in the frame; (stills p2) fixed: backed off, it went into a filing cabinet
st.cue('clack', 'S10', HIT10, 0.4)

# 11: ...three times. On the examiner's clipboard (EXAMEN DE PILOTE), three red crosses slash ESSAI 1, 2, 3, one after the other (RECALÉ card)
D11 = st.dur('S11')
CB = [0.0, 1.3, -0.9]
st.shot('S11', 'mairie', setOpts=EXAMSET, actors=[],
        props=[P('clip11', 'clipboardX', pos=CB, rot=[-0.35, 0, 0], opts={'w': 0.3, 'marks': [0.08, 0.26, 0.44]})],
        cams=[FC(0.0, [0.0, 1.55, -0.2], [[r(CB[0] - 0.17), r(CB[1] + 0.22), CB[2]], [r(CB[0] + 0.17), r(CB[1] - 0.24), CB[2]]], top=0.16, bottom=0.7, level=False)])
for i, t_ in enumerate([0.08, 0.26, 0.44]): st.cue('sfx:paper', 'S11', t_, 0.25)

# 12: yesterday he stopped bouncing. Down the street he bounces toward us, higher and higher, three bounces; at the top of the third he stops dead in
#     mid-air: his hair settles, a blink; in front, a woman and a boy look up at him
#     (pass 2: one small hop and one big rise; the woman and the boy missing; the tower's top faded into the haze; a 0.73 s freeze) three bounces,
#     each higher, the third up past the first floors, then the stop, with small moves after it; the two onlookers big in the lower third, faces up;
#     no haze
D12 = st.dur('S12'); STOP12 = 1.1
AIR = [0.5, 7.0, 1.0]                                                     # (pass 2) higher: the stop reads as up in the air (on 4.2 m he seemed to stand in the road)
K12, T12 = HOPS(0.0, [[0.5, -6.0], [0.5, -4.2], [0.5, -2.4]], [1.4, 3.0], 0.34)
CLEAR = {'haze': False}                                                   # (pass 2) the tower's top was a ghost in the haze
LOOKUP = lambda t: [AIR[0], r(min(AIR[1] + 1.5, 1.6 + 6.0 * t)), r(-6.0 + 6.5 * min(1.0, t / STOP12))]
st.shot('S12', 'parisStreet', setOpts=STREET, look=CLEAR, actors=[
        act('mec', [0.5, 0, -6.0], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0), *K12, *T12,
            k(0.68, to=AIR, dur=r(STOP12 - 0.68), ease='out', face='keep'), k(0.68, toon={'sq': ST, 'hairUp': 0.7, 'face': DEAD}, toonDur=0.04, toonEase='out'),   # ...the third, way up...
            k(STOP12, toon={'sq': [1.04, 0.97, 1.04], 'hairUp': 0.5, 'face': {'lid': 0.3}}, toonDur=0.06, toonEase='out'),   # ...and stops dead up there
            k(r(STOP12 + 0.12), toon={'sq': [0.99, 1.01, 0.99], 'hairUp': 0.3, 'face': DEAD}, toonDur=0.1),   # a jiggle...
            k(r(STOP12 + 0.3), toon={'sq': [1.0, 1.0, 1.0], 'hairUp': 0.12, 'face': DEAD}, toonDur=0.2, toonEase='inOut'),   # ...his hair settling...
            k(r(STOP12 + 0.5), toon={'face': {'lid': 1.0}}, toonDur=0.12), k(r(STOP12 + 0.68), toon={'sq': [1.0, 1.012, 1.0], 'face': DEAD}, toonDur=0.15)]),   # ...a slow blink, a breath
        act('voisine', [-0.9, 0, 4.4], 165, 'stand', 'neutral', keys=[*[k(r(0.2 * j), look=LOOKUP(0.2 * j)) for j in range(7)],
            k(r(STOP12 + 0.15), toon={'face': {'lid': 0.0, 'eye': 0.5, 'brow': 0.9, 'mouth': 'O'}}, toonDur=0.1)]),   # (pass 2) in front of us, following him up
        act('gamin', [1.3, 0, 4.6], -165, 'stand', 'happy', scale=0.62, keys=[*[k(r(0.03 + 0.2 * j), look=LOOKUP(0.03 + 0.2 * j)) for j in range(7)],
            k(r(STOP12 + 0.22), toon={'face': {'lid': 0.0, 'eye': 0.6, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.1)])],
        cams=[FC(0.0, [0.3, 0.7, 7.4], [[AIR[0], r(AIR[1] + 2.5), AIR[2]], [0.5, 0.0, -6.0], [-0.9, 1.75, 4.4], [1.3, 1.25, 4.6], [-0.9, 0.3, 4.4]], top=0.08, bottom=0.84, lenses=range(28, 64))])   # (pass 2) low behind the two onlookers, him up the street; (stills p2) level: backed off along the 3D line it went under the road (black frames)
st.cue('sfx:boing', 'S12', 0.31, 0.2); st.cue('sfx:boing', 'S12', 0.65, 0.25); st.cue('sfx:squeak', 'S12', STOP12, 0.2)

# 13: in mid-flight. From below, against the sky: he hangs there; he looks down (his eyes first) at the nothing under his feet, then at us, deadpan
D13 = st.dur('S13')
st.shot('S13', 'parisStreet', setOpts=STREET, look=CLEAR, actors=[
        act('mec', AIR, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.1, toon={'face': {'lid': 0.3, 'gy': 0.8}}, toonDur=0.06), k(0.18, look=[AIR[0], 0.0, r(AIR[2] + 0.6)]),   # his eyes down, then his head...
            k(0.55, toon={'face': {'lid': 0.3, 'gy': 0.0}}, toonDur=0.06), k(0.62, look='camera'), k(0.7, toon={'sq': [1.0, 1.015, 1.0], 'face': DEAD}, toonDur=0.2)])],   # ...then to us
        cams=[FC(0.0, [-0.5, 4.3, 3.6], [[AIR[0], r(AIR[1] + 2.45), AIR[2]], [AIR[0], r(AIR[1] - 0.1), AIR[2]], [r(AIR[0] - 0.5), r(AIR[1] + 1.5), AIR[2]], [r(AIR[0] + 0.5), r(AIR[1] + 1.5), AIR[2]]], top=0.14, bottom=0.74, level=False, drift=(0.0, 0.0, 0.1))])   # (pass 2) from below, the sky behind him

# 14: the pigeons built their nest on his head. From above: far over the street (the two onlookers tiny below), a pigeon lands on his head, then
#     another; a nest drops onto his hair; closer from above: eggs pop in, one, two, three, on the near rim, his eyes going up at each; a pigeon pecks;
#     a slow blink
#     (pass 2: the nest floated over his hair, no egg showed, the pigeons hid the nest, he seemed to stand in the road) seen from above with the
#     street far below; a twig nest sat on his hair (his head squashed under it), the eggs on the near rim, the pigeons on its sides
D14 = st.dur('S14'); HEAD14 = [AIR[0], r(AIR[1] + 2.5), AIR[2]]; NEST14 = 0.8; LAY14 = [1.25, 1.55, 1.85]; CUT14 = 1.05
NEST_Y = 0.62                                                             # (pass 2) the bowl on his hair, in the frame of his head
st.shot('S14', 'parisStreet', setOpts=STREET, look=CLEAR, actors=[
        act('mec', AIR, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.25, toon={'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.5, 'gy': -0.5}}, toonDur=0.05), k(0.4, toon={'face': {'lid': 0.45, 'gy': 0.0}}, toonDur=0.1),   # a pigeon lands: his eyes up...
            k(0.5, toon={'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.5, 'gy': -0.4}}, toonDur=0.05), k(0.66, toon={'face': DEAD}, toonDur=0.1),
            k(NEST14, toon={'scl': {'head': [1.06, 0.9, 1.06]}, 'sq': [1.03, 0.96, 1.03], 'face': {'lid': 0.6, 'gy': -0.6}}, toonDur=0.04, toonEase='out'),   # (pass 2) the nest lands: his head squashed under it...
            k(r(NEST14 + 0.1), toon={'scl': {'head': [0.98, 1.03, 0.98]}, 'face': {'lid': 0.5, 'gy': -0.4}}, toonDur=0.08), k(r(NEST14 + 0.2), toon={'face': DEAD}, toonDur=0.1),
            *[k(r(t_ + 0.04), toon={'sq': [1.0, 1.012 if i % 2 else 0.996, 1.0], 'face': {'lid': 0.4, 'gy': -0.75, 'gx': (0.2 if i % 2 else -0.2)}}, toonDur=0.08) for i, t_ in enumerate(LAY14)],   # his eyes up at each egg...
            k(2.05, toon={'sq': [1.0, 1.01, 1.0], 'face': DEAD}, toonDur=0.15), k(2.25, toon={'face': {'lid': 1.0}}, toonDur=0.14), k(2.5, toon={'sq': [1.0, 1.01, 1.0], 'face': DEAD}, toonDur=0.18)]),   # ...a slow blink
        act('pig1', [r(HEAD14[0] + 2.2), r(HEAD14[1] + 1.2), r(HEAD14[2] + 1.0)], -120, 'fly', 'neutral', scale=0.8, keys=[k(0.0, to=[r(HEAD14[0] + 0.24), r(HEAD14[1] + 0.15), r(HEAD14[2] - 0.06)], dur=0.25, clip='fly', then='idle', ease='out', face='keep'), k(1.0, clip='peck', blend=0.1)]),   # (pass 2) on the rim's side (on top it hid the nest)
        act('pig2', [r(HEAD14[0] - 2.0), r(HEAD14[1] + 1.0), r(HEAD14[2] + 0.8)], 110, 'fly', 'neutral', scale=0.8, keys=[k(0.0, to=[r(HEAD14[0] - 1.0), r(HEAD14[1] + 0.6), r(HEAD14[2] + 0.4)], dur=0.3, clip='fly', then='fly', ease='linear', face='keep'),
                                                                                                                   k(0.3, to=[r(HEAD14[0] - 0.24), r(HEAD14[1] + 0.15), r(HEAD14[2] - 0.06)], dur=0.2, clip='fly', then='idle', ease='out', face='keep')]),
        act('voisine', [-1.2, 0, 2.6], 30, 'stand', 'neutral', keys=[k(0.0, look=[AIR[0], r(AIR[1] + 2.0), AIR[2]]), k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.4, 'brow': 0.8, 'mouth': 'o'}}, toonDur=0.0)]),   # (pass 2) far below, looking up
        act('gamin', [1.4, 0, 2.2], -30, 'stand', 'happy', scale=0.62, keys=[k(0.0, look=[AIR[0], r(AIR[1] + 2.0), AIR[2]]), k(0.0, toon={'face': {'lid': 0.0, 'eye': 0.5, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.0)])],
        props=[P('nest14', 'twigNest', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, NEST_Y, 0.0]}, opts={'r': 0.3, 'layAt': LAY14, 'max': 3}, keys=[k(0.0, scale=0.001, dur=0.0), k(NEST14, scale=1.0, dur=0.12, ease='outBack')]),   # (pass 2) twigs, on his hair (a smooth dish floated over it)
               P('fth14', 'feather', pos=[r(HEAD14[0] + 0.3), r(HEAD14[1] + 0.3), r(HEAD14[2] + 0.2)], opts={'at': 0.3, 'fall': 1.6, 'dur': 2.0, 's': 1.2})],
        cams=[FC(0.0, [0.35, 12.6, 2.4], [[AIR[0], r(AIR[1] + 2.8), AIR[2]], [AIR[0], r(AIR[1] + 2.15), r(AIR[2] + 0.25)], [AIR[0], AIR[1], AIR[2]], [AIR[0], 0.0, 0.6], [1.4, 0.0, 2.2], [-1.2, 0.0, 2.6]], top=0.12, bottom=0.74, level=False, lenses=range(28, 60)),   # (pass 2) from above: him high over the street, the two tiny below...
              FC(CUT14, [0.45, 10.9, 2.75], [[AIR[0], r(AIR[1] + 3.1), AIR[2]], [r(AIR[0] - 0.32), r(AIR[1] + 2.8), AIR[2]], [r(AIR[0] + 0.32), r(AIR[1] + 2.8), AIR[2]], [AIR[0], r(AIR[1] + 2.15), r(AIR[2] + 0.25)], [AIR[0], r(AIR[1] + 1.85), r(AIR[2] + 0.2)], [r(AIR[0] - 0.4), r(AIR[1] + 1.7), AIR[2]], [r(AIR[0] + 0.4), r(AIR[1] + 1.7), AIR[2]]],
                 top=0.14, bottom=0.74, level=False, lenses=range(28, 60))])   # ...closer from above: the nest, the eggs, his eyes
st.cue('whoosh', 'S14', 0.15, 0.18, 0.3, 700, 2000); st.cue('whoosh', 'S14', 0.4, 0.14, 0.3, 700, 2000); st.cue('sfx:pop', 'S14', NEST14, 0.2)
for t_ in LAY14: st.cue('sfx:pop', 'S14', t_, 0.12)

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
