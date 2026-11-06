#!/usr/bin/env python3
"""Le wifi (story 33): this man had no wifi. He put his modem on the wardrobe: one bar. On the roof: two bars. On a crane: three bars.
So he tied it to balloons. The balloons left: over Paris, above the clouds, up to the space station. Today the astronauts have wifi
and watch series all day. And he pays the subscription. Signal cards grow with the bars (45 -> 65 % of the frame width, 22-45 % high)."""
from story_kit import *

st = Story('wifi')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 7), ('S04', 'L03', 0), ('S05', 'L03', 6)] + [(f'S{i + 2:02d}', f'L{i:02d}', 0) for i in range(4, 13)])
LR = {'sofa': False, 'tv': False}
MODEM = lambda pos, pid='modem', ry=0, keys=None, **kw: P(pid, 'wifiModem', pos=pos, ry=ry, **({'keys': keys} if keys else {}), **kw)
ARM = [-0.75, 0, -2.0]


def onscreen(cam_, look, d, sx, sy):   # a world point d metres in front of the camera at screen offset (sx, sy) in half-widths / half-heights (lens 44, 9:16)
    f = [look[i] - cam_[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)); f = [v / n for v in f]
    r = [-f[2], 0.0, f[0]]; n = math.sqrt(r[0] ** 2 + r[2] ** 2); r = [v / n for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    return [round(cam_[i] + d * (f[i] + 0.2272 * sx * r[i] + 0.4040 * sy * u[i]), 3) for i in range(3)]
def yaw_to(p, cam_): return round(math.degrees(math.atan2(cam_[0] - p[0], cam_[2] - p[2])), 1)
def CARD(pid, n, cam_, look, pop, frac, sx=0.0, sy=0.34, d=1.0):   # a signal card frac of the frame width wide, facing the lens
    p = onscreen(cam_, look, d, sx, sy); return P(pid, 'signalBars', pos=p, ry=yaw_to(p, cam_), opts={'n': n, 'popAt': pop, 'w': round(frac * 2 * d * 0.2272, 3)})

# 1-3: no wifi (tight on his fury, the dead phone); he slides the modem onto the wardrobe; one bar
C1, K1 = [0.42, 1.98, 0.25], [0.3, 1.86, -1.5]
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.5], -10, 'showPhone', 'rage')],
        props=[P('phone', 'smartPhone', pos=[0.25, 1.62, -0.98], ry=-10, scale=2.0, opts={'call': False, 'label': 'AUCUN RÉSEAU'}), CARD('bars0', 0, C1, K1, 0.2, 0.42, sx=-0.38, sy=0.42)],
        cams=[cam(0.0, C1, [0.41, 1.98, 0.12], K1, K1, lens=44)])
FACE2 = -124
st.shot('S02', 'livingRoom', setOpts=LR, actors=[act('mec', [0.15, 0, -1.4], FACE2, 'placeHigh', 'determined', keys=[k(0.85, clip='stand', expr='proud', to=[0.5, 0, -1.15], dur=0.35, face='keep')])],
        props=[P('arm', 'armoire', pos=ARM), MODEM([-0.22, 2.04, -1.66], ry=-34, keys=[k(0.12, to=[-0.62, 2.03, -1.95], dur=0.6, ease='inOut')])],
        cams=[cam(0.0, [-0.05, 1.75, 2.9], [-0.05, 1.76, 2.7], [-0.2, 1.55, -1.6], [-0.2, 1.57, -1.6], lens=44)])
T3 = st.at('S03', 'L02', 7); C3, K3 = [ARM[0] + 0.3, 2.3, ARM[2] + 1.55], [ARM[0] + 0.1, 2.2, ARM[2]]
st.shot('S03', 'livingRoom', setOpts=LR, props=[P('arm', 'armoire', pos=ARM), MODEM([-0.62, 2.03, -1.95], ry=-34), CARD('bars1', 1, C3, K3, T3 - 0.05, 0.45, sy=0.36)],
        cams=[cam(0.0, C3, [ARM[0] + 0.28, 2.3, ARM[2] + 1.42], K3, K3, lens=44)])
# 4-6: on a Paris zinc roof (low angle, the roofscape behind), two bars; a tower crane (wide, then close: fear of heights), three bars
RF = [15.0, 23.04, -30.0]; UPM = lambda b: [b[0], b[1] + 2.4, b[2] + 0.04]
ROOFP = P('roof', 'zincRoof', pos=[RF[0], RF[1] - 0.04, RF[2]], opts={'w': 6})
st.shot('S04', 'parisStreet', actors=[act('mec', RF, 15, 'holdUp', 'squint')], props=[ROOFP, MODEM(UPM(RF), ry=15)],
        cams=[cam(0.0, [17.6, 24.9, -25.2], [17.4, 25.0, -25.6], [15.0, 25.0, -30.0], [15.0, 25.1, -30.0], lens=44)])
T5 = st.at('S05', 'L03', 6); C5, K5 = [16.1, 24.7, -28.3], [15.0, 25.7, -30.0]
st.shot('S05', 'parisStreet', actors=[act('mec', RF, 15, 'holdUp', 'smirk')], props=[ROOFP, MODEM(UPM(RF), ry=15), CARD('bars2', 2, C5, K5, T5 - 0.05, 0.5, sx=0.0, sy=0.42, d=0.9)],
        cams=[cam(0.0, C5, [16.05, 24.72, -28.45], K5, K5, lens=44)])
CRANE = [-4.0, 0, -40.0]; TOP = [CRANE[0] + 2.0, 24.66, CRANE[2]]
T6 = st.at('S06', 'L04', 3)
CRANE_P = P('crane', 'towerCrane', pos=CRANE, opts={'h': 24, 'jib': 16})
C6, K6 = [TOP[0] + 1.5, TOP[1] + 1.95, TOP[2] + 3.3], [TOP[0] + 0.15, TOP[1] + 2.2, TOP[2]]
st.shot('S06', 'parisStreet', actors=[act('mec', TOP, 10, 'holdUp', 'nervous', fx={'sweat': True, 'shiver': True})], props=[CRANE_P, MODEM(UPM(TOP), ry=10), CARD('bars3', 3, C6, K6, T6 - 0.05, 0.55, sy=0.4)],
        cams=[cam(0.0, [9.0, 2.0, -12.0], [8.6, 2.6, -12.6], [-2.0, 14.0, -40.0], [-2.0, 15.0, -40.0], lens=44), cam(T6 - 0.35, [C6[0] + 0.1, C6[1], C6[2] + 0.2], C6, K6, K6, lens=44)])
# 7-8: he ties it to balloons (the whole bunch in frame); they leave; front close-up on his tears
HAND = [TOP[0] + 0.05, TOP[1] + 1.45, TOP[2] + 0.5]
D8 = st.dur('S08')
st.shot('S07', 'parisStreet', actors=[act('mec', TOP, 10, 'giveItem', 'proud')], props=[CRANE_P, MODEM(HAND, ry=10), P('bunch', 'balloonBunch', pos=[HAND[0], HAND[1] + 0.07, HAND[2]], opts={'len': 1.6}, scale=0.01, keys=[k(0.3, scale=1.0, dur=0.35, ease='outBack')])],
        cams=[cam(0.0, [TOP[0] + 1.7, TOP[1] + 1.3, TOP[2] + 5.0], [TOP[0] + 1.65, TOP[1] + 1.35, TOP[2] + 4.8], [TOP[0] + 0.05, TOP[1] + 2.55, TOP[2]], [TOP[0] + 0.05, TOP[1] + 2.57, TOP[2]], lens=44)])
UP8 = [HAND[0] + 0.6, HAND[1] + 4.5, HAND[2] - 0.6]
st.shot('S08', 'parisStreet', actors=[act('mec', TOP, 10, 'stand', 'proud', keys=[k(0.15, clip='armsUp', expr='shocked', look=UP8), k(0.7, clip='stand', expr='sob', fx={'tears': True}, look=None)])],
        props=[CRANE_P, MODEM(HAND, ry=10, keys=[k(0.05, to=[UP8[0], UP8[1] - 0.07, UP8[2]], dur=D8, ease='out'), k(0.66, visible=False)]), P('bunch', 'balloonBunch', pos=[HAND[0], HAND[1] + 0.07, HAND[2]], opts={'len': 1.6}, keys=[k(0.05, to=UP8, dur=D8, ease='out'), k(0.66, visible=False)])],
        cams=[cam(0.0, [TOP[0] + 1.6, TOP[1] + 1.0, TOP[2] + 4.2], [TOP[0] + 1.55, TOP[1] + 1.1, TOP[2] + 4.1], [TOP[0] + 0.2, TOP[1] + 2.2, TOP[2]], [TOP[0] + 0.3, TOP[1] + 3.4, TOP[2]], lens=44),
              cam(0.68, [TOP[0] + 0.35, TOP[1] + 2.0, TOP[2] + 1.45], [TOP[0] + 0.33, TOP[1] + 2.0, TOP[2] + 1.35], [TOP[0] + 0.02, TOP[1] + 2.02, TOP[2]], [TOP[0] + 0.02, TOP[1] + 2.03, TOP[2]], lens=44)])
# 9-11: over Paris toward the Eiffel tower; above the clouds (a pigeon stares); the space station: the modem docks, four bars
CITY = P('city', 'cityBlocks', pos=[0, 0, 0], opts={'x0': -402, 'x1': 420, 'z0': -657, 'z1': 460, 'skip': [[-21, 21, -128, 120]], 'park': [-46, 32, -222, -132]})
D9 = st.dur('S09'); B9 = [1.0, 58.0, -40.0]; B9b = [0.0, 64.0, -55.0]
st.shot('S09', 'parisStreet', props=[CITY, MODEM(B9, keys=[k(0.0, to=B9b, dur=D9)]), P('bunch', 'balloonBunch', pos=[B9[0], B9[1] + 0.07, B9[2]], opts={'len': 1.6}, keys=[k(0.0, to=[B9b[0], B9b[1] + 0.07, B9b[2]], dur=D9)])],
        cams=[cam(0.0, [B9[0] + 1.4, B9[1] + 4.5, B9[2] + 7.5], [B9b[0] + 1.4, B9b[1] + 4.5, B9b[2] + 7.5], [B9[0], B9[1] - 4.0, B9[2] - 16.0], [B9b[0], B9b[1] - 4.0, B9b[2] - 16.0], lens=44)],
        far=900, shadow={'center': [0, 0, -60], 'size': 90, 'bias': -0.004})
D10 = st.dur('S10'); B10 = [0.0, 128.0, -60.0]; B10b = [0.0, 134.0, -63.0]
CLOUDS10 = [P(f'cl{i}', 'cloud', pos=[x, y, z], opts={'scale': sc, 'seed': 30 + i}, keys=[k(0.0, to=[x - 3.0, y, z], dur=D10)]) for i, (x, y, z, sc) in enumerate([(5.5, 129.5, -66.0, 1.6), (-4.5, 131.5, -70.0, 2.0), (7.0, 126.0, -58.0, 1.2)])]
st.shot('S10', 'parisStreet', setOpts={'sky': ['#2F5FA8', '#B9DDF2'], 'eiffel': False}, actors=[act('pigeon', [B10[0] + 1.1, B10[1] - 0.2, B10[2] + 0.6], -60, 'fly', 'surprised', scale=1.1, keys=[k(0.0, to=[B10b[0] + 1.1, B10b[1] - 0.2, B10b[2] + 0.6], dur=D10, glide=True, face='keep')])],
        props=[P('clouds', 'cloudLayer', pos=[0, 106, -60], opts={'w': 500, 'd': 500, 'n': 260, 'h': 16}), *CLOUDS10,
               MODEM(B10, keys=[k(0.0, to=B10b, dur=D10)]), P('bunch', 'balloonBunch', pos=[B10[0], B10[1] + 0.07, B10[2]], opts={'len': 1.6}, keys=[k(0.0, to=[B10b[0], B10b[1] + 0.07, B10b[2]], dur=D10)])],
        cams=[cam(0.0, [B10[0] + 2.6, B10[1] + 0.9, B10[2] + 5.6], [B10b[0] + 2.6, B10b[1] + 1.1, B10b[2] + 5.6], [B10[0], B10[1] + 1.1, B10[2]], [B10b[0], B10b[1] + 1.1, B10b[2]], lens=44)])
D11 = st.dur('S11'); T11 = st.at('S11', 'L09', 3) - 0.1
ST = [0.0, 0.0, -14.0]; DOCK = [2.96, 0.9, -15.08]
C11, K11 = [12.5, 6.5, -1.5], [0.8, -1.4, -15.0]
st.shot('S11', 'spaceDark', props=[P('earth', 'earthGlobe', pos=[-6.0, -102.0, -60.0], opts={'radius': 42}), P('iss', 'spaceStation', pos=ST, ry=20, opts={'size': 12, 'spin': 0.0}),
        MODEM([5.5, -2.5, -11.5], scale=1.6, keys=[k(0.0, to=[DOCK[0] + 0.35, DOCK[1], DOCK[2] + 0.1], dur=T11, ease='out')]), CARD('bars4', 4, C11, K11, T11, 0.48, sx=0.18, sy=0.58, d=1.3)],
        cams=[cam(0.0, C11, [12.1, 6.4, -2.1], K11, K11, lens=44)])
# 12-13: the cosy cabin: astronauts in flight suits float tilted (hair up), snacks drift; the series (S4 · É12) then their faces
WALLM = [-1.25, 2.35, -2.33]; C12, K12 = [0.15, 2.75, 3.9], [0.1, 2.5, -1.0]
PATCH = lambda a: P(f'patch_{a}', 'missionPatch', on={'actor': a, 'joint': 'torso', 'offset': [0.13, 0.42, 0.14]})
st.shot('S12', 'stationInside', setOpts={'winX': 1.4}, actors=[act('astro1', [-0.3, 0.55, -0.9], 20, 'floatTilt', 'starEyes', fx={'zeroG': True}, keys=[k(0.0, to=[-0.25, 0.67, -0.85], dur=2.2, glide=True, face='keep')]),
        act('astro2', [0.5, 0.42, -1.2], -25, 'floatTiltB', 'bigGrin', fx={'zeroG': True}, keys=[k(0.0, to=[0.45, 0.55, -1.15], dur=2.2, glide=True, face='keep')])],
        props=[PATCH('astro1'), PATCH('astro2'), MODEM(WALLM, rot=[1.5708, 0, 0]), P('snacks', 'floatSnacks', pos=[0.0, 2.1, -0.4], opts={'n': 8, 'r': 1.3}), CARD('bars5', 4, C12, K12, 0.15, 0.4, sx=-0.5, sy=0.42, d=1.2)],
        cams=[cam(0.0, C12, [0.15, 2.76, 3.65], K12, K12, lens=44)])
st.shot('S13', 'stationInside', setOpts={'winX': 1.9}, actors=[act('astro1', [-0.85, 0.35, 0.0], 170, 'floatTilt', 'love', fx={'zeroG': True}, keys=[k(0.0, to=[-0.8, 0.45, 0.0], dur=2.2, glide=True, face='keep')]),
        act('astro2', [0.8, 0.25, -0.1], 190, 'floatTiltB', 'laugh', fx={'zeroG': True}, keys=[k(0.0, to=[0.75, 0.33, -0.1], dur=2.2, glide=True, face='keep')])],
        props=[PATCH('astro1'), PATCH('astro2'), P('screen', 'seriesScreen', pos=[0.0, 2.25, -2.28], opts={'w': 1.9, 'h': 1.1}), P('snacks', 'floatSnacks', pos=[0.0, 2.3, 0.3], opts={'n': 10, 'r': 1.1, 'seed': 27})],
        cams=[cam(0.0, [0.0, 2.7, 2.2], [0.0, 2.68, 2.0], [0.0, 2.3, -2.3], [0.0, 2.3, -2.3], lens=44), cam(0.95, [0.0, 2.45, -2.2], [0.0, 2.45, -2.1], [0.0, 2.3, 0.2], [0.0, 2.31, 0.2], lens=62)])
# 14: and he pays the subscription (tight; the bill beside his face, the no-wifi card kept in frame through the push-in)
T14 = st.at('S14', 'L12', 5) - 0.1
C14a, C14, K14 = [0.3, 1.95, 0.95], [0.28, 1.95, 0.35], [0.1, 1.9, -1.5]
BILL = onscreen(C14, K14, 1.2, 0.48, 0.04)
st.shot('S14', 'livingRoom', setOpts=LR, actors=[act('mec', [-0.1, 0, -1.5], 0, 'showPhone', 'unimpressed', keys=[k(T14 + 0.1, expr='sob', fx={'tears': True})])],
        props=[P('phone', 'smartPhone', pos=[-0.2, 1.62, -0.98], scale=2.0, opts={'call': False, 'label': 'AUCUN RÉSEAU'}), CARD('bars6', 0, C14, K14, 0.2, 0.3, sx=-0.5, sy=0.6, d=1.0),
               P('bill', 'waterBill', pos=BILL, ry=yaw_to(BILL, C14), opts={'w': 0.3, 'h': 0.23, 'popAt': T14, 'title': 'ABONNEMENT', 'amount': '49,99 €', 'sub': 'CHAQUE MOIS', 'stamp': 'PRÉLEVÉ'})],
        cams=[cam(0.0, C14a, [0.29, 1.95, 0.8], K14, K14, lens=44), cam(T14 - 0.05, [0.29, 1.95, 0.8], C14, K14, K14, lens=44, ease='out')])
st.card('S03', 'UNE BARRE'); st.card('S10', 'TOUJOURS PLUS HAUT'); st.card('S12', 'LE WIFI')
st.cue('sfx:beep', 'S03', T3, 0.35); st.cue('sfx:beep', 'S05', T5, 0.35); st.cue('sfx:beep', 'S06', T6, 0.4); st.cue('pop', 'S07', 0.3, 0.4); st.cue('sfx:whistle', 'S08', 0.1, 0.3)
st.cue('sfx:ding', 'S11', T11, 0.4); st.cue('sfx:fanfare', 'S12', 0.1, 0.25); st.cue('sfx:paper', 'S14', T14, 0.3); st.cue('sfx:cash', 'S14', T14 + 0.3, 0.3)
st.write('Le wifi', {'astro1': {'preset': 'worker', 'seed': 131, 'suit': '#2C4A8A', 'lapel': '#2C4A8A', 'shirt': '#2C4A8A', 'pants': '#2C4A8A', 'hat': 'none'},
                     'astro2': {'preset': 'worker', 'seed': 132, 'suit': '#2C4A8A', 'lapel': '#2C4A8A', 'shirt': '#2C4A8A', 'pants': '#2C4A8A', 'hat': 'none', 'facial': 'none', 'lipstick': True, 'hair': 'bun', 'hairColor': '#3A2A20'},
                     'pigeon': {'type': 'creature', 'name': 'pigeon', 'opts': {'seed': 4}}})
