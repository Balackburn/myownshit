#!/usr/bin/env python3
"""La porte tournante (story 57, cycle 19 of the cartoon staging): this man went into a revolving door. He never came out. He has been turning for
three years. The power station plugged him into the grid. He lights the whole neighbourhood. The gym gave him a membership. Yesterday the door
stopped. He did not. The station bills him for the blackout.
Staging: on a Paris street he walks into an office building's revolving door and gives the wing a push; the door spins up and he turns with it at its
axis, his arms flung out, his tie straight out sideways, his hair on end, his face deadpan each time it comes round; a passer-by's hat is blown off by
the wind of it; a wall calendar flips from 2023 to 2026 while a beard grows on him as he turns; a technician plugs a fat cable into the door's base,
sparks; the meter's disc whirls and its counter rolls; at night the windows of the whole district light up in a wave while the door glows; a coach
clicks his laps on a stopwatch and blows his whistle, then holds out a membership card that the wing snatches and plasters on his face; a janitor's
broom jams the door: CLANG, it stops dead; he keeps turning in it like a top, drills out of it and spins away down the pavement in a whirl of wind,
spinning a passer-by round on the way; at night in the dark district he wobbles to a stop, dizzy, and the technician holds up the bill.
Natural look; cycle 19 tools: the yaw channel (a spin keyed in turns), the white void's floor under y 0, props_tournante.js (revolvingDoor,
powerCable, meterBox, nightSkyline, gymCard)."""
from story_kit import *
import math

st = Story('tournante', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 3), ('S06', 'L04', 0), ('S07', 'L04', 3),
         ('S08', 'L05', 0), ('S09', 'L06', 0), ('S10', 'L06', 6), ('S11', 'L07', 0), ('S12', 'L07', 2), ('S13', 'L08', 0), ('S14', 'L09', 0)])

PI = math.pi; TAU = 2 * PI
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)

STREET = {'eiffelStyle': 'v2', 'clear': [-6.0, 12.0]}                    # no tree or lamp on the right pavement around the door
NIGHT = {'color': '#141C30'}
DOOR = [8.85, 0, 2.0]; DRY = -90                                          # the door against the facade of the right-hand row, its openings up and down the pavement
DR = 1.3; DH = 2.6; INNER = 0.38                                          # the drum: radius, height, the room in the middle where he turns
FAST = 2.4                                                                # turns per second at full speed
BURST = lambda pid, pos, at_, text, w=0.45: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
DEADPAN = {'lid': 0.45}
DOORP = lambda pid, spin, pos=None, **o: P(pid, 'revolvingDoor', pos=pos or DOOR, ry=DRY, opts={'r': DR, 'h': DH, 'inner': INNER, 'text': 'BUREAUX', 'spin': spin, 'frame': '#C8A44A', 'glass': [0.05, 0.03], **o})   # (pass 2) brass frames, clearer glass

def lin(ks, t):
    if t <= ks[0][0]: return ks[0][1]
    for i in range(1, len(ks)):
        if t < ks[i][0]:
            (t0, v0), (t1, v1) = ks[i - 1], ks[i]; return v0 + (v1 - v0) * (t - t0) / max(1e-6, t1 - t0)
    return ks[-1][1]
def turns(ks, t, n=200):
    """the turns made from 0 to t at a rate keyed linearly (the door's own integral, prop revolvingDoor)"""
    if t <= 0: return 0.0
    h = t / n; return sum((lin(ks, i * h) + lin(ks, (i + 1) * h)) / 2 * h for i in range(n))
# the pose of a man turning fast at the axis: arms flung out and up a little, his tie straight out sideways, his hair on end; s doses it (0..1)
# (pass 2) a T: the hands held out at shoulder height in the frame of his torso (curving the arms with bends left them at his sides), the tie horizontal,
# stretched tall
FLUNG = lambda s: {'touch': {'L': ['torso', 0.8, 0.55, 0.05, r(s), 0.05], 'R': ['torso', -0.8, 0.55, 0.05, r(s), 0.05]}, 'tie': [1.2, r(0.2 * s), r(1.45 * s)], 'hairUp': r(s),
                   'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [r(1 - 0.05 * s), r(1 + 0.07 * s), r(1 - 0.05 * s)]}
BEARD = lambda pid, L, sweep=0.9, lift=0.8, keys=None: P(pid, 'longBeard', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.05, 0.1]}, opts={'len': L, 'w': 0.2, 'sweep': sweep, 'lift': lift, 'wave': [0.16, 9]}, keys=keys or [])   # (pass 2) the beard of three years, kept from S05 on and growing
def rideCam(t, rate, pid, yaw0=PI / 4, d=1.2, y=1.95, lens=58):
    """(stills 2) a camera inside the compartment he faces, turning with the door (cam key 'ride'): his face stays to us and the street whirls behind
    him (from outside, the wings crossed his face four times a turn). yaw0: his yaw at 0, a quarter of a wing from a wing (PI / 4) so that he faces the
    middle of a compartment; d: from the axis (inside the drum, DR - 0.1 at most)"""
    a = yaw0 + TAU * turns(rate, t); frm = [r(DOOR[0] - d * math.cos(a)), y, r(DOOR[2] + d * math.sin(a))]
    return {**cam(t, frm, frm, [MED[0], 1.82, MED[2]], [MED[0], 1.82, MED[2]], lens=lens), 'ride': {'prop': pid}}
def spinKeys(rate, t0, t1, pose=lambda t: {}, dt=0.1, yaw0=0.0):
    """toon keys that turn him with a door turning at `rate` from t0 to t1 (yaw from the same integral), each key a whole state from pose(t)"""
    ks = [k(t0, toon={**pose(t0), 'yaw': r(yaw0 + TAU * turns(rate, t0), 4)}, toonDur=0.0)]
    t = t0
    while t < t1 - 1e-6:
        tn = min(t1, t + dt); ks.append(k(r(t), toon={**pose(tn), 'yaw': r(yaw0 + TAU * turns(rate, tn), 4)}, toonDur=r(tn - t), toonEase='linear')); t = tn
    return ks

# 1: the hook. A Paris street, the door of an office building (BUREAUX over it): he walks up the pavement, deadpan, and pushes into the revolving door
D1 = st.dur('S01'); IN1 = 0.95
SP1 = [[0.0, 0.0], [IN1, 0.0], [r(IN1 + 0.1), 0.35]]
MEW = [r(DOOR[0] - 1.9), 0, r(DOOR[2] - 3.0)]; MED = [r(DOOR[0] - 0.05), 0, DOOR[2]]   # (check) up the pavement toward us, then into the door
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MEW, 10, 'stand', 'unimpressed', keys=[k(0.0, look=[DOOR[0], 1.5, DOOR[2]]), k(0.0, toon={'face': DEADPAN}, toonDur=0.0),
            k(0.0, to=[r(DOOR[0] - 1.45), 0, r(DOOR[2] - 0.35)], dur=IN1, clip='walk', then='walk', ease='linear', face='move'),
            k(IN1, to=MED, dur=0.25, clip='walk', then='stand', ease='out', face='move'),
            k(r(IN1 - 0.05), toon={'reach': {'R': [r(DOOR[0] - 0.75), 1.15, r(DOOR[2] - 0.25), 1, 0.05]}, 'hands': {'R': 'spread'}, 'face': DEADPAN}, toonDur=0.08)])],   # a push on the wing
        props=[DOORP('door1', SP1)],
        cams=[FC(0.0, [r(DOOR[0] - 5.2), 1.55, r(DOOR[2] + 3.6)], [[DOOR[0], r(DH + 0.45), DOOR[2]], [DOOR[0], 0.0, DOOR[2]], [DOOR[0], r(DH + 0.2), r(DOOR[2] + DR + 0.2)], [DOOR[0], r(DH + 0.2), r(DOOR[2] - DR - 0.2)], [r(MEW[0] - 0.3), 2.3, MEW[2]], [r(MEW[0] + 0.3), 0.0, MEW[2]]], top=0.12, bottom=0.74, drift=(0.1, 0.0, -0.15))])   # (stills v1) the drum and its sign whole (cut by the right edge)
st.cue('sfx:step', 'S01', 0.2, 0.15); st.cue('sfx:step', 'S01', 0.6, 0.15); st.cue('sfx:squeak', 'S01', r(IN1 + 0.05), 0.2)

# 2: a revolving door. Closer, through the opening: the door spins up and he turns with it at its axis, his arms flinging out, his tie straight out,
#    his hair rising, his face deadpan each time it comes round; a whoosh
D2 = st.dur('S02')
SP2 = [[0.0, 0.35], [0.25, 0.6], [0.85, FAST]]
FL2 = lambda t: {**FLUNG(min(1.0, max(0.0, (t - 0.15) / 0.6))), 'face': DEADPAN}
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys(SP2, 0.0, D2, FL2, yaw0=TAU * turns(SP1, D1))])],
        props=[DOORP('door2', SP2)],   # (pass 3) no wind ribbons: flat white strips read as paper scraps
        cams=[FC(0.0, [r(DOOR[0] - 2.9), 1.7, r(DOOR[2] + 0.9)], [[DOOR[0], 2.55, DOOR[2]], [DOOR[0], 0.35, DOOR[2]], [DOOR[0], 1.3, r(DOOR[2] - 1.1)], [DOOR[0], 1.3, r(DOOR[2] + 1.1)]], top=0.1, bottom=0.74, drift=(0.25, 0.0, 0.0))])
st.cue('whoosh', 'S02', 0.2, 0.3, 0.85, 300, 1300)

# 3: he never came out. Wide: the door a blur with him turning at its middle; people go by on the pavement; the wind of it blows a passer-by's hat off
D3 = st.dur('S03'); HAT3 = 0.55
SP3 = [[0.0, FAST]]
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys(SP3, 0.0, D3, lambda t: {**FLUNG(1.0), 'face': DEADPAN}, dt=0.12)]),
        act('passant', [r(DOOR[0] - 3.0), 0, r(DOOR[2] - 3.0)], 0, 'stand', 'neutral', keys=[k(0.0, look=[DOOR[0], 1.4, DOOR[2]]), k(0.0, to=[r(DOOR[0] - 3.0), 0, r(DOOR[2] + 3.2)], dur=r(D3 + 0.6), clip='walk', then='walk', ease='linear', face='move'),   # (pass 2) nearer us, under the hero in the frame (in front of the door he hid him)
            k(r(HAT3 - 0.04), toon={'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.2, 'brow': 0.8, 'mouth': 'O'}, 'hat': [0.45, 0.4, 1.0]}, toonDur=0.08, toonEase='out'),   # his hat lifts off in the wind...
            k(r(HAT3 + 0.04), toon={'face': {'lid': 0.0, 'brow': 1.0, 'mouth': 'O'}, 'hat': [0.55, 0.5, 1.4]}, toonDur=0.14),   # ...(pass 2) hangs there five frames...
            k(r(HAT3 + 0.18), toon={'reach': {'R': [r(DOOR[0] - 3.0), 2.3, r(DOOR[2] - 0.6), 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.1, 'brow': 1.0, 'mouth': 'O'}, 'hat': [3.2, 1.6, 9.0]}, toonDur=0.4, toonEase='in')])],   # ...and whips away while he grabs at the air
        props=[DOORP('door3', SP3)],
        cams=[FC(0.0, [r(DOOR[0] - 6.0), 2.4, r(DOOR[2] + 1.4)], [[DOOR[0], r(DH + 0.4), DOOR[2]], [DOOR[0], 0.0, DOOR[2]], [r(DOOR[0] - 3.0), 2.3, r(DOOR[2] - 1.0)], [r(DOOR[0] - 3.0), 0.0, r(DOOR[2] + 1.4)]], top=0.22, bottom=0.76, drift=(0.0, 0.0, -0.2))])   # (pass 2) higher (the passer-by under him in the frame); BUREAUX under the TOUJOURS card
st.cue('whoosh', 'S03', 0.0, 0.25, 1.3, 250, 1100)

# 4: for three years. The wall calendar beside the door flips its years, 2023 to 2026; the door a blur behind it
D4 = st.dur('S04')
CAL4 = [r(DOOR[0] + 0.15), 1.75, r(DOOR[2] + 1.75)]
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys(SP3, 0.0, D4, lambda t: {**FLUNG(1.0), 'face': DEADPAN}, dt=0.12)])],
        props=[DOORP('door4', SP3), P('cal4', 'yearCalendar', pos=CAL4, ry=-90, scale=1.6, opts={'years': [2023, 2026], 'flipAt': 0.08, 'dur': r(D4 - 0.2)})],
        cams=[FC(0.0, [r(DOOR[0] - 2.6), 1.7, r(DOOR[2] + 2.6)], [[CAL4[0], 2.35, r(CAL4[2] + 0.5)], [CAL4[0], 1.15, r(CAL4[2] - 0.5)], [DOOR[0], 2.4, DOOR[2]], [DOOR[0], 0.9, DOOR[2]]], top=0.12, bottom=0.74, drift=(0.1, 0.0, 0.0))])   # (stills v1) the calendar whole (cut by the right edge)
st.cue('sfx:paper', 'S04', 0.1, 0.25)

# 5: three years. Close on him turning: a beard has grown, long, and it trails as he turns; his face deadpan each time it comes round
D5 = st.dur('S05')
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys([[0.0, 0.8]], 0.0, D5, lambda t: {**FLUNG(0.75), 'face': DEADPAN}, dt=0.1, yaw0=PI / 4)])],   # (stills v1) his face to us mid-shot (the back of his head); (stills 2) to the riding camera
        props=[DOORP('door5', [[0.0, 0.8]]), BEARD('beard5', 0.75, 0.7, 0.6, keys=[k(0.0, scale=0.6), k(0.0, scale=1.0, dur=r(D5 - 0.1))])],   # (pass 2) one long mass to his belt, swept by the turn, growing (a comb of sticks)
        cams=[rideCam(0.0, [[0.0, 0.8]], 'door5', d=1.18, y=1.85)])   # (stills 2) inside, turning with him: the mullion of a wing crossed his face

# 6: the power station plugged him in. A technician in a hard hat pushes a fat cable's plug into a socket at the door's base: sparks
D6 = st.dur('S06'); PLUG6 = 0.42
SOCK = [r(DOOR[0] - 0.6), 0.0, r(DOOR[2] + DR + 0.25)]
TECH6 = [r(DOOR[0] + 0.15), 0, r(DOOR[2] + DR + 0.55)]   # (stills v1) beyond the socket, facing us (his back was to the lens)
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys(SP3, 0.0, D6, lambda t: {**FLUNG(1.0), 'face': DEADPAN}, dt=0.12)]),
        act('technicien', TECH6, -60, 'stand', 'neutral', keys=[k(0.0, look={'point': [SOCK[0], 0.2, SOCK[2]], 'cheat': 0.3}),
            k(0.0, toon={'reach': {'L': [r(SOCK[0] + 0.3), 0.45, r(SOCK[2] + 0.12), 1, 0.05]}, 'hands': {'L': 'grip'}, 'bend': {'spine': [0.6, 0, 0, 1, None]}, 'face': {'lid': 0.5}}, toonDur=0.0),
            k(r(PLUG6 - 0.28), toon={'reach': {'L': [r(SOCK[0] + 0.45), 0.5, r(SOCK[2] + 0.2), 1, 0.05]}, 'hands': {'L': 'grip'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'brow': -0.3}}, toonDur=0.12, toonEase='inOut'),   # (pass 2) a wind-up back...
            k(r(PLUG6 - 0.1), toon={'reach': {'L': [r(SOCK[0] + 0.1), 0.2, r(SOCK[2] + 0.04), 1, 0.05]}, 'hands': {'L': 'grip'}, 'bend': {'spine': [0.78, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'brow': -0.4}}, toonDur=0.1, toonEase='in'),   # ...in it goes...
            k(r(PLUG6 + 0.02), toon={'touch': {'L': ['torso', 0.85, 0.75, 0.0, 1, 0.05], 'R': ['torso', -0.85, 0.75, 0.0, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [0.84, 1.24, 0.84], 'hairUp': 1.0, 'hat': [0.75, 0.3, 0.0], 'face': {'lid': 0.0, 'brow': 1.0, 'mouth': 'grimace', 'pop': 0.55, 'popLen': 0.18}}, toonDur=0.033, toonEase='out'),   # (pass 3) BZZT: rigid, stretched, arms splayed, the hat rocketing up...
            *[k(r(PLUG6 + 0.06 + 0.035 * i), toon={'touch': {'L': ['torso', 0.85, 0.75, 0.0, 1, 0.05], 'R': ['torso', -0.85, 0.75, 0.0, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': ([0.9, 1.16, 0.9] if i % 2 else [0.82, 1.27, 0.82]), 'hairUp': 1.0, 'hat': [0.8, 0.35 + 0.05 * (i % 2), 0.0], 'face': {'lid': 0.0, 'brow': 1.0, 'mouth': 'grimace', 'pop': 0.55, 'popLen': 0.18}}, toonDur=0.03) for i in range(6)],   # ...six frames buzzing, the hat hanging over his hair...
            k(r(PLUG6 + 0.3), toon={'bend': {'spine': [0.1, 0, 0, 1, None]}, 'hairUp': 0.9, 'hat': [0.05, 0.1, 0.0], 'face': {'lid': 0.0, 'brow': 0.9, 'pop': 0.35, 'popLen': 0.14}}, toonDur=0.1, toonEase='in'),   # ...it drops back on his head...
            k(r(PLUG6 + 0.45), toon={'bend': {'spine': [0.1, 0, 0, 1, None]}, 'hairUp': 0.8, 'face': {'lid': 0.3, 'brow': 0.7}}, toonDur=0.15)])],
        props=[DOORP('door6', SP3), P('cable6', 'powerCable', pos=SOCK, opts={'r': 0.06, 'sag': 0.02, 'sparkSize': 3, 'to': [-6.5, 0.04, 4.5], 'sparkAt': [PLUG6], 'flow': [[PLUG6, 0.0], [r(PLUG6 + 0.2), 1.0]]}), BEARD('beard6', 0.8),
               BURST('bzzt6', [r(SOCK[0] - 0.35), 0.75, r(SOCK[2] + 0.35)], PLUG6, 'BZZT !', 0.55)],   # (pass 2) thick, running off to the grid; a burst you can read
        cams=[FC(0.0, [r(DOOR[0] - 3.4), 1.3, r(DOOR[2] + 3.8)], [[TECH6[0], 2.25, TECH6[2]], [r(TECH6[0] + 0.45), 2.1, TECH6[2]], [TECH6[0], 0.0, TECH6[2]], [SOCK[0], 0.0, SOCK[2]], [DOOR[0], 2.4, DOOR[2]]], top=0.12, bottom=0.74)])   # (stills 2) his head was cut by the right edge
st.cue('sfx:zip', 'S06', r(PLUG6 - 0.05), 0.2); st.cue('sfx:static', 'S06', PLUG6, 0.35)

# 7: to the grid. The meter on its post: its disc whirls and its counter rolls; the cable runs off to the grid behind it
D7 = st.dur('S07')
MET7 = [r(DOOR[0] - 1.1), 0, r(DOOR[2] + DR + 1.3)]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[],
        props=[DOORP('door7', SP3), P('meter7', 'meterBox', pos=MET7, ry=-60, opts={'h': 1.35, 'spin': [[0.0, 3.0], [0.3, 9.0]], 'count': [[0.0, 120], [r(D7), 98400]]}),
               P('cable7', 'powerCable', pos=SOCK, opts={'to': [-4.0, 0.0, 3.0], 'flow': [[0.0, 1.0]]})],
        cams=[FC(0.0, [r(MET7[0] - 1.3), 1.45, r(MET7[2] + 1.1)], [[MET7[0], 1.7, MET7[2]], [MET7[0], 1.0, MET7[2]]], top=0.22, bottom=0.66, drift=(0.1, 0.0, -0.1))])
st.cue('sfx:ticks', 'S07', 0.0, 0.25); st.cue('sfx:kaching', 'S07', r(D7 - 0.3), 0.15)

# 8: he lights the whole district. Night: the door glowing at the foot of the frame, him turning in it; behind, the windows of the town light up in a
#    wave from left to right
D8 = st.dur('S08'); WAVE8 = [0.15, 1.15]
ND = [0.0, 0, 0.0]
st.shot('S08', 'whiteVoid', setOpts=NIGHT, actors=[
        act('mec', ND, 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys(SP3, 0.0, D8, lambda t: {**FLUNG(1.0), 'face': DEADPAN}, dt=0.12)])],
        props=[DOORP('door8', SP3, pos=ND, bulbs=[[0.0, 1.0]]), BEARD('beard8', 0.82), P('town8', 'nightSkyline', pos=[0.0, 0, -9.0], opts={'n': 8, 'w': 18, 'wave': WAVE8}),
               P('pave8', 'carpet', pos=[0.0, 0, -1.5], opts={'w': 22, 'd': 9, 'color': '#3A4152', 'inner': '#3A4152'})],
        cams=[FC(0.0, [1.3, 0.6, 9.0], [[0.0, r(DH + 0.3), 0.0], [0.0, 0.0, 0.0], [-5.5, 7.5, -9.0], [5.5, 7.5, -9.0]], top=0.06, bottom=0.82, drift=(-0.12, 0.05, -0.4))])   # (pass 3) wide: the door small at the foot of the frame under the whole district   # (pass 2) low: the door at the foot of the frame, the town over it
st.cue('sfx:static', 'S08', 0.2, 0.15); st.cue('pop', 'S08', 0.4, 0.12); st.cue('pop', 'S08', 0.75, 0.12); st.cue('pop', 'S08', 1.05, 0.12)

# 9: the gym. Day: a coach in a red tracksuit beside the door clicks his laps on a stopwatch and blows his whistle, a thumb up
D9 = st.dur('S09')
COACH = [r(DOOR[0] - 1.45), 0, r(DOOR[2] - 1.7)]   # (stills v1) the far side of the opening, facing us (his back to the lens)
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys(SP3, 0.0, D9, lambda t: {**FLUNG(1.0), 'face': DEADPAN}, dt=0.12)]),
        act('coach', COACH, -30, 'stand', 'happy', keys=[k(0.0, look={'point': [DOOR[0], 1.4, DOOR[2]], 'cheat': 0.4}),
            *[k(r(0.08 + 0.21 * i), toon={'reach': {'R': [r(COACH[0] - 0.05), 1.4, r(COACH[2] + 0.3), 1, 0.05], 'L': [r(COACH[0] - 0.12), r(1.62 if i % 2 else 1.55), r(COACH[2] + 0.12), 1, 0.05]},
                                       'hands': {'R': 'grip', 'L': 'fist'}, 'face': {'lid': 0.2, 'mouth': 'O' if i % 2 else 'smile', 'cheeks': 1.0 if i % 2 else 0.0, 'gx': (0.5 if i % 2 else -0.5)}}, toonDur=0.06) for i in range(4)],   # click, click, the whistle, cheeks puffed; his eyes on each lap
            *[k(r(0.12 + 0.21 * i), look={'point': [DOOR[0], 1.4, r(DOOR[2] + (0.9 if i % 2 else -0.9))], 'cheat': 0.4}) for i in range(4)],   # (pass 3) his head follows each lap after his eyes
            k(0.92, toon={'reach': {'R': [r(COACH[0] + 0.05), 1.6, r(COACH[2] + 0.35), 1, 0.05]}, 'hands': {'R': 'thumbUp'}, 'face': {'lid': 0.15, 'mouth': 'bigsmile'}}, toonDur=0.1, toonEase='outBack')])],   # a thumb up
        props=[DOORP('door9', SP3), P('watch9', 'stopwatch', on={'actor': 'coach', 'hand': 'R', 'offset': [0, 0, 0.03]}, scale=2.8), BEARD('beard9', 0.84),   # (pass 2) twice as big: a beige disc
               P('whis9', 'whistle', on={'actor': 'coach', 'hand': 'L', 'offset': [0, 0.02, 0.03]}, scale=2.6)],
        cams=[FC(0.0, [r(DOOR[0] - 4.0), 1.55, r(DOOR[2] + 2.6)], [[COACH[0], 2.25, COACH[2]], [r(COACH[0] - 0.5), 2.1, COACH[2]], [COACH[0], 0.2, COACH[2]], [DOOR[0], 2.5, DOOR[2]], [DOOR[0], 0.3, DOOR[2]]], top=0.12, bottom=0.74)])   # (stills 2) his head was cut by the left edge
st.cue('sfx:click', 'S09', 0.08, 0.2); st.cue('sfx:click', 'S09', 0.5, 0.2); st.cue('sfx:whistle', 'S09', 0.29, 0.25)

# 10: gave him a membership. The coach holds out the card; a wing snatches it from his fingers; cut in: the card is stuck on his face as he turns,
#     deadpan behind it
D10 = st.dur('S10'); SN10 = 0.32; CUT10 = 0.5
CARD10 = [r(COACH[0] + 0.45), 1.45, r(COACH[2] + 0.55)]   # held out toward the opening, on our side of him
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys(SP3, 0.0, D10, lambda t: {**FLUNG(1.0), 'face': DEADPAN}, dt=0.12, yaw0=PI / 4)]),
        act('coach', COACH, -30, 'stand', 'happy', keys=[k(0.0, look={'point': CARD10, 'cheat': 0.3}), k(0.0, toon={'reach': {'R': [CARD10[0], r(CARD10[1] - 0.08), CARD10[2], 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.15, 'mouth': 'bigsmile'}}, toonDur=0.0),   # (stills 2) by its lower edge: his hand covered it
            k(SN10, toon={'reach': {'R': [r(CARD10[0] - 0.1), r(CARD10[1] + 0.05), r(CARD10[2] + 0.1), 1, 0.05]}, 'hands': {'R': 'open'}, 'sq': [0.97, 1.04, 0.97], 'hairUp': 0.8, 'face': {'lid': 0.0, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out')])],   # snatched: his hair blown up
        props=[DOORP('door10', SP3), BEARD('beard10', 0.86),
               P('card10', 'gymCard', pos=CARD10, face='camera', opts={'s': 1.8, 'bright': True}, keys=[k(SN10, to=[DOOR[0], 1.6, r(DOOR[2] + 0.5)], dur=0.12, ease='in'), k(r(SN10 + 0.12), visible=False)]),
               P('card10f', 'gymCard', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.28, 0.1]}, opts={'s': 1.9}, keys=[k(0.0, visible=False), k(r(SN10 + 0.12), visible=True)])],   # stuck on his face
        cams=[FC(0.0, [r(DOOR[0] - 3.6), 1.6, r(DOOR[2] + 2.9)], [[COACH[0], 2.25, COACH[2]], [COACH[0], 0.6, COACH[2]], CARD10, [DOOR[0], 2.4, DOOR[2]]], top=0.12, bottom=0.74),
              rideCam(CUT10, SP3, 'door10', d=1.18, y=1.85)])   # (stills 2) the cut-in inside, turning with him: the card on his face, the street a whirl
st.cue('whoosh', 'S10', SN10, 0.2, 0.2, 500, 1600); st.cue('sfx:splat', 'S10', r(SN10 + 0.12), 0.25)

# 11: yesterday. A janitor mopping by the door: the handle of his broom swings into the wing: CLANG, the door stops dead
D11 = st.dur('S11'); JAM = 0.42
JAN = [r(DOOR[0] - 1.55), 0, r(DOOR[2] - 1.5)]
SP11 = [[0.0, FAST], [r(JAM - 0.001), FAST], [JAM, 0.0]]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys([[0.0, FAST]], 0.0, D11, lambda t: {**FLUNG(1.0), 'face': DEADPAN}, dt=0.12)]),   # he does not stop
        act('concierge', JAN, -10, 'stand', 'neutral', keys=[k(0.0, look={'point': [r(JAN[0] + 0.3), 0.0, r(JAN[2] + 0.4)], 'cheat': 0.4}),   # (stills 2) turned to us (in profile at 30, 82 degrees)
            k(0.0, toon={'reach': {'R': [r(JAN[0] + 0.35), 0.9, r(JAN[2] + 0.35), 1, 0.05], 'L': [r(JAN[0] + 0.2), 1.25, r(JAN[2] + 0.2), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.6}}, toonDur=0.0),
            k(r(JAM - 0.26), toon={'reach': {'R': [r(JAN[0] - 0.15), 1.5, r(JAN[2] - 0.1), 1, 0.05], 'L': [r(JAN[0] - 0.05), 1.7, r(JAN[2] - 0.05), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [-0.15, 0.2, 0, 1, None]}, 'face': {'lid': 0.4, 'brow': -0.3}}, toonDur=0.14, toonEase='inOut'),   # (pass 3) a wind-up...
            k(r(JAM - 0.08), toon={'reach': {'R': [r(JAN[0] + 0.45), 1.05, r(JAN[2] + 0.6), 1, 0.05], 'L': [r(JAN[0] + 0.3), 1.3, r(JAN[2] + 0.5), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.2, -0.15, 0, 1, None]}, 'face': {'lid': 0.4}}, toonDur=0.07, toonEase='in'),   # ...and the swing, an arc into the wing
            k(JAM, toon={'sq': [1.05, 0.95, 1.05], 'reach': {'R': [r(JAN[0] + 0.25), 0.9, r(JAN[2] + 0.55), 1, 0.05], 'L': [r(JAN[0] + 0.1), 1.25, r(JAN[2] + 0.4), 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.0, 'brow': 1.0, 'pop': 0.45, 'popLen': 0.18}}, toonDur=0.04, toonEase='out')])],   # CLANG: his eyes out
        props=[DOORP('door11', SP11), BEARD('beard11', 0.88), P('broom11', 'broom', pos=[r(DOOR[0] - 0.95), 0.05, r(DOOR[2] - 0.75)], rot=[0.0, 0.0, -0.55], scale=1.1, keys=[k(0.0, visible=False), k(JAM, visible=True)]),
               P('broom11h', 'broom', on={'actor': 'concierge', 'hand': 'R', 'offset': [0.0, -0.4, 0.0]}, scale=1.1, keys=[k(JAM, visible=False)]),   # (stills v1) in his hands until it jams the door
               BURST('clang11', [r(DOOR[0] - 1.3), 2.0, r(DOOR[2] - 0.3)], JAM, 'CLANG !', 0.5)],
        fx=[{'type': 'shake', 'at': JAM, 'dur': 0.18, 'amount': 0.015}],
        cams=[FC(0.0, [r(DOOR[0] - 4.6), 1.45, r(DOOR[2] + 1.6)], [[DOOR[0], r(DH + 0.3), DOOR[2]], [DOOR[0], 0.0, DOOR[2]], [JAN[0], 2.25, JAN[2]], [JAN[0], 0.0, JAN[2]]], top=0.12, bottom=0.74)])
st.cue('clang', 'S11', JAM, 0.5)

# 12: the door stopped. Closer: the wings dead still, the broom jammed in; inside, at its middle, he goes on turning like a top
D12 = st.dur('S12')
# (pass 2) a top: squashed into a coil at the start (the door stopped dead), then stretched thin, the arms up together over his head, the tie and the
# beard flying out (a dark stick turning in place with its arms out)
TOP12 = lambda t: {'touch': {'L': ['torso', 0.1, 1.45, 0.05, 1, 0.05], 'R': ['torso', -0.1, 1.45, 0.05, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'tie': [1.2, 0.2, 1.45], 'hairUp': 1.0,
                   'sq': ([1.18, 0.82, 1.18] if t < 0.12 else [0.84, 1.18, 0.84]), 'face': DEADPAN}
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys([[0.0, FAST]], 0.0, D12, TOP12, dt=0.1)])],
        props=[DOORP('door12', [[0.0, 0.0]]), BEARD('beard12', 0.9, 1.1, 1.0), P('broom12', 'broom', pos=[r(DOOR[0] - 0.95), 0.05, r(DOOR[2] - 0.75)], rot=[0.0, 0.0, -0.55], scale=1.1)],   # (pass 3) no wind ribbons
        cams=[FC(0.0, [r(DOOR[0] - 2.8), 1.5, r(DOOR[2] - 0.9)], [[DOOR[0], 3.15, DOOR[2]], [DOOR[0], 0.3, DOOR[2]], [r(DOOR[0] - 0.95), 1.3, r(DOOR[2] - 0.75)]], top=0.2, bottom=0.76, drift=(0.15, 0.0, 0.08))])   # (pass 3) his raised hands and face in the frame (they were above its top edge)
st.cue('whoosh', 'S12', 0.0, 0.25, 1.1, 300, 1200)

# 13: he did not. He drills out of the door like a top and spins away down the pavement in a whirl of wind; a passer-by is spun round as he goes by
D13 = st.dur('S13')
OUT13 = [r(DOOR[0] - 1.2), 0, r(DOOR[2] - 5.6)]
PASS13 = [r(DOOR[0] - 2.4), 0, r(DOOR[2] - 2.8)]   # (pass 2) beside his path, on the road side (in front of the exit she hid it)
DRILL = lambda t: {'touch': {'L': ['torso', 0.08, 1.45, 0.1, 1, 0.05], 'R': ['torso', -0.08, 1.45, 0.1, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'tie': [1.2, 0.2, 1.45], 'hairUp': 1.0,
                   'lay': [0.3, 0.0], 'sq': ([1.15, 0.85, 1.15] if t < 0.08 else [0.8, 1.25, 0.8]), 'face': DEADPAN}   # (pass 2) a drill: squashed to wind up, then stretched and tilted at us
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[
        act('mec', MED, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys([[0.0, FAST], [0.5, 3.4]], 0.0, D13, DRILL, dt=0.08),
            k(0.1, to=[r(DOOR[0] - 1.2), 0, r(DOOR[2] - 1.4)], dur=0.22, glide=True, ease='in', face='keep'), k(0.32, to=OUT13, dur=r(D13 - 0.32), glide=True, ease='in', face='keep')]),
        act('passante', PASS13, 90, 'stand', 'neutral', keys=[k(0.0, look=[r(DOOR[0] - 1.0), 1.4, r(DOOR[2] - 1.0)]),
            k(0.55, toon={'yaw': 0.0, 'face': {'lid': 0.0, 'brow': 1.0}}, toonDur=0.0),
            k(0.55, toon={'yaw': r(TAU * 2.0 + PI / 2, 4), 'hairUp': 1.0, 'face': {'lid': 0.0, 'brow': 1.0, 'cross': 1.0, 'eyeScale': 1.25}}, toonDur=0.5, toonEase='out')])],   # (pass 3) she ends facing us (her back was to us)   # spun round twice as he passes, cross-eyed
        props=[DOORP('door13', [[0.0, 0.0]]), BEARD('beard13', 0.92, 1.3, 1.2), P('broom13', 'broom', pos=[r(DOOR[0] - 0.95), 0.05, r(DOOR[2] - 0.75)], rot=[0.0, 0.0, -0.55], scale=1.1)],   # (pass 3) no wind ribbons
        cams=[FC(0.0, [r(DOOR[0] - 1.6), 1.25, r(DOOR[2] - 8.2)], [[DOOR[0], r(DH + 0.3), DOOR[2]], [OUT13[0], 2.5, OUT13[2]], [OUT13[0], 0.0, OUT13[2]], [PASS13[0], 2.2, PASS13[2]]], top=0.12, bottom=0.76)])   # (pass 2) down the pavement, on his path: he drills out of the door at us
st.cue('whoosh', 'S13', 0.05, 0.4, 1.1, 200, 1000); st.cue('sfx:boing', 'S13', 0.55, 0.2)

# 14: the station bills him for the blackout. Night, the district dark: he wobbles to a stop, dizzy, stars round his head; the technician holds up
#     the bill; deadpan, a blink
D14 = st.dur('S14'); STOP14 = 0.9; BILL14 = 1.25
ME14 = [0.0, 0, 0.0]; TECH14 = [0.95, 0, 0.45]
WOB = lambda t: {'wave': {'spine': [r(0.06 * max(0.0, 1 - t / 1.8)), 1.0, r(t * 2.2), 0, 0.0]}, 'face': {'lid': 0.3, 'cross': r(0.8 * max(0.0, 1 - t / 1.6)), 'stars': r(min(1.0, max(0.0, (D14 - 0.45 - t) / 0.3))), 'starsScale': 2.2, 'starsY': -0.25}}   # (pass 2) big stars at his eyes, under the card, until the blink
st.shot('S14', 'whiteVoid', setOpts={'color': '#2A3A62'}, actors=[   # (pass 3) a lighter night behind him (navy on navy, 1.05:1)
        act('mec', ME14, 15, 'stand', 'unimpressed', keys=[k(0.0, look=None), *spinKeys([[0.0, 1.6], [STOP14, 0.0]], 0.0, r(STOP14 + 0.05), lambda t: {**FLUNG(max(0.0, 1 - t / STOP14)), **WOB(t)}, dt=0.1, yaw0=-TAU * turns([[0.0, 1.6], [STOP14, 0.0]], STOP14)),   # (stills v1) he comes to rest facing us (in profile)
            k(r(STOP14 + 0.05), toon={'yaw': 0.18, **WOB(STOP14), 'sq': [1.62, 0.47, 1.62]}, toonDur=0.05, toonEase='out'),   # (pass 3) flattened to half his height as he stops...
            k(r(STOP14 + 0.1), toon={'yaw': 0.18, **WOB(STOP14 + 0.05), 'sq': [1.58, 0.5, 1.58]}, toonDur=0.2),   # ...held eight frames...
            k(r(STOP14 + 0.32), toon={'yaw': -0.11, **WOB(STOP14 + 0.3), 'sq': [0.88, 1.16, 0.88]}, toonDur=0.07, toonEase='outBack'),   # ...a pop: re-inflated past his height...
            *[k(r(STOP14 + 0.42 + 0.2 * i), toon={'yaw': r(0.1 * (0.6 ** i) * (1 if i % 2 == 0 else -1), 3), **WOB(STOP14 + 0.4 + 0.2 * i)}, toonDur=0.18, toonEase='inOut') for i in range(4)],   # ...and a wobble back and forth to a stop
            k(round(STOP14 + 1.1, 3), look='camera'),
            k(r(D14 - 0.45), toon={'yaw': 0.0, 'face': {'lid': 1.0}}, toonDur=0.06), k(r(D14 - 0.3), toon={'yaw': 0.0, 'face': DEADPAN}, toonDur=0.1)]),
        act('technicien', TECH14, -60, 'stand', 'neutral', keys=[k(0.0, look={'actor': 'mec'}), k(0.3, toon={'sq': [1.0, 1.02, 1.0], 'face': {'lid': 0.4, 'gx': -0.3}}, toonDur=0.3, toonEase='inOut'), k(0.7, toon={'face': {'lid': 0.4, 'gx': 0.3}}, toonDur=0.15),   # (pass 3) his eyes follow the wobble, he breathes k(BILL14, toon={'reach': {'R': [0.8, 1.3, 0.8, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5}}, toonDur=0.15),   # (pass 2) by its corner: his fingers lay on the price
            k(1.9, toon={'reach': {'R': [0.8, 1.32, 0.8, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'sq': [1.0, 1.015, 1.0], 'face': {'lid': 1.0}}, toonDur=0.06), k(2.02, toon={'reach': {'R': [0.8, 1.3, 0.8, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'brow': 0.3}}, toonDur=0.1)])],
        props=[DOORP('door14', [[0.0, 0.0]], pos=[-2.6, 0, -2.4]), P('town14', 'nightSkyline', pos=[0.0, 0, -9.0], opts={'n': 8, 'w': 18, 'wave': [99.0, 99.0]}),
               P('pave14', 'carpet', pos=[0.0, 0, -1.5], opts={'w': 22, 'd': 9, 'color': '#3A4152', 'inner': '#3A4152'}),
               P('bill14', 'waterBill', pos=[0.5, 1.5, 0.82], face='camera', opts={'title': 'FACTURE', 'amount': '9 999 €', 'sub': 'PANNE DU QUARTIER', 'subTop': True, 'stampPos': [0.2, -0.35], 'stamp': 'À PAYER', 'popAt': BILL14, 'w': 0.6, 'h': 0.48}),   # (pass 2) the line on its own above the price; the stamp on the grey lines
               BEARD('beard14', 0.95, 0.25, 0.3)],
        cams=[FC(0.0, [0.55, 1.75, 3.4], [[ME14[0], 2.4, ME14[2]], [r(ME14[0] - 0.45), 1.8, ME14[2]], [ME14[0], 0.9, ME14[2]], [TECH14[0], 2.25, TECH14[2]], [r(TECH14[0] + 0.4), 1.8, TECH14[2]], [0.5, 1.2, 0.82], [0.85, 1.75, 0.82]], top=0.2, bottom=0.72, drift=(0.0, 0.0, -0.15))])   # (pass 2) the two-shot whole from the start (his face cut by the left edge), under the card
st.cue('sfx:twang', 'S14', 0.1, 0.15); st.cue('sfx:paper', 'S14', BILL14, 0.3); st.cue('sfx:crickets', 'S14', 0.0, 0.08)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S02', 0.7, 'mec', 'spin_up'), ('S03', 0.6, 'mec', 'blur'), ('S05', 0.45, 'mec', 'beard'), ('S06', round(PLUG6 + 0.1, 3), 'technicien', 'zap'), ('S09', 0.95, 'coach', 'thumb'),
           ('S10', 0.8, 'mec', 'card_face'), ('S11', round(JAM + 0.08, 3), 'concierge', 'clang'), ('S12', 0.5, 'mec', 'top'), ('S13', 0.7, 'mec', 'drill'), ('S14', round(D14 - 0.6, 3), 'mec', 'bill')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S01', 0.5, 'door1', 'bureaux'), ('S04', 0.5, 'cal4', 'calendar'), ('S10', 0.15, 'card10', 'abonnement'), ('S14', round(D14 - 0.6, 3), 'bill14', 'facture')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S03', 'TOUJOURS')
st.card('S14', 'PANNE')

st.write("La porte tournante", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'passant': {'preset': 'boss', 'seed': 571, 'suit': '#6B5B45', 'hat': 'fedora',   # (pass 2) 'bowler' is no hat of the rig: he had none
                 'mustache': True, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'technicien': {'preset': 'worker', 'seed': 572, 'suit': '#E07A2E', 'hat': 'hardhat', 'build': {'width': 1.0, 'headWidth': 1.2}},
    'coach': {'preset': 'worker', 'seed': 573, 'suit': '#C8322A', 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'concierge': {'preset': 'worker', 'seed': 574, 'suit': '#5C7A8A', 'hat': 'cap', 'mustache': True, 'build': {'width': 1.0, 'headWidth': 1.2}},
    'passante': {'preset': 'madame', 'seed': 575, 'suit': '#8E5AA8', 'hairColor': '#B8B8B8', 'build': {'width': 0.9, 'headWidth': 1.25}},
})
