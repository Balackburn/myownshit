#!/usr/bin/env python3
"""Le wifi (story 33): this man had no wifi. He put his modem on the wardrobe: one bar. On the roof: two bars. On a crane: three bars.
So he tied it to balloons. The balloons left: over Paris, above the clouds, up to the space station. Today the astronauts have wifi
and watch series all day. And he pays the subscription."""
from story_kit import *

st = Story('wifi')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 7), ('S04', 'L03', 0), ('S05', 'L03', 6)] + [(f'S{i + 2:02d}', f'L{i:02d}', 0) for i in range(4, 13)])
LR = {'sofa': False, 'tv': False}
BARS = lambda pid, n, pos, pop, ry=0, w=0.5: P(pid, 'signalBars', pos=pos, ry=ry, opts={'n': n, 'popAt': pop, 'w': w})
MODEM = lambda pos, pid='modem', ry=0, keys=None, **kw: P(pid, 'wifiModem', pos=pos, ry=ry, **({'keys': keys} if keys else {}), **kw)
ARM = [-0.75, 0, -2.0]                                     # the wardrobe against the back wall
HELMET = lambda a: P(f'helm_{a}', 'spaceHelmet', on={'actor': a, 'joint': 'head', 'offset': [0, 0.27, 0]})

# 1-3: no wifi; the modem on the wardrobe: one bar
st.shot('S01', 'livingRoom', setOpts=LR, actors=[act('mec', [0.35, 0, -1.5], -10, 'showPhone', 'rage')],
        props=[P('phone', 'smartPhone', pos=[0.25, 1.62, -0.98], ry=-10, scale=2.0), P('tbl', 'table', pos=[-0.45, 0, -1.6], opts={'w': 0.6, 'd': 0.45, 'h': 0.75}), MODEM([-0.45, 0.75, -1.6], ry=15),
               BARS('bars0', 0, [-0.3, 2.45, -1.25], 0.25, ry=4, w=0.42)],
        cams=[cam(0.0, [0.15, 1.75, 1.8], [0.14, 1.74, 1.6], [0.05, 1.65, -1.5], [0.05, 1.66, -1.5], lens=44)])
st.shot('S02', 'livingRoom', setOpts=LR, actors=[act('mec', [0.15, 0, -1.4], -55, 'armsUp', 'determined', keys=[k(0.55, clip='stand', expr='proud', to=[0.4, 0, -1.2], dur=0.3, face='keep')])],
        props=[P('arm', 'armoire', pos=ARM), MODEM([ARM[0] + 0.1, 2.03, ARM[2] + 0.05], ry=10)],
        cams=[cam(0.0, [-0.05, 1.75, 2.9], [-0.05, 1.76, 2.7], [-0.2, 1.5, -1.6], [-0.2, 1.52, -1.6], lens=44)])
T3 = st.at('S03', 'L02', 7)
st.shot('S03', 'livingRoom', setOpts=LR, props=[P('arm', 'armoire', pos=ARM), MODEM([ARM[0] + 0.1, 2.03, ARM[2] + 0.05], ry=10), BARS('bars1', 1, [ARM[0] + 0.1, 2.42, ARM[2] + 0.4], T3 - 0.05, w=0.3)],
        cams=[cam(0.0, [ARM[0] + 0.3, 2.3, ARM[2] + 1.55], [ARM[0] + 0.28, 2.3, ARM[2] + 1.42], [ARM[0] + 0.1, 2.25, ARM[2]], [ARM[0] + 0.1, 2.27, ARM[2]], lens=44)])
# 4-6: on the roof: two bars; on a crane: three bars
ROOF = [0.4, 0, -3.0]
st.shot('S04', 'rooftopPowerLine', actors=[act('mec', ROOF, 15, 'holdUp', 'squint')], props=[MODEM([ROOF[0], 2.55, ROOF[2] + 0.05], ry=10)],
        cams=[cam(0.0, [1.4, 1.15, 0.6], [1.36, 1.18, 0.4], [0.35, 1.75, -3.0], [0.35, 1.77, -3.0], lens=44)])
T5 = st.at('S05', 'L03', 6)
st.shot('S05', 'rooftopPowerLine', actors=[act('mec', ROOF, 15, 'holdUp', 'smirk')], props=[MODEM([ROOF[0], 2.55, ROOF[2] + 0.05], ry=10), BARS('bars2', 2, [ROOF[0] + 0.12, 2.92, ROOF[2] + 0.5], T5 - 0.05, w=0.3)],
        cams=[cam(0.0, [ROOF[0] + 0.45, 2.4, ROOF[2] + 2.3], [ROOF[0] + 0.43, 2.4, ROOF[2] + 2.15], [ROOF[0] + 0.1, 2.35, ROOF[2]], [ROOF[0] + 0.1, 2.36, ROOF[2]], lens=44)])
CRANE = [-4.0, 0, -40.0]; TOP = [CRANE[0] + 2.0, 24.66, CRANE[2]]   # the walkway at the jib root (towerCrane userData.top)
T6 = st.at('S06', 'L04', 3)
CRANE_P = P('crane', 'towerCrane', pos=CRANE, opts={'h': 24, 'jib': 16})
st.shot('S06', 'parisStreet', actors=[act('mec', TOP, 10, 'holdUp', 'nervous', fx={'sweat': True, 'shiver': True})], props=[CRANE_P, MODEM([TOP[0], TOP[1] + 2.55, TOP[2] + 0.05], ry=10), BARS('bars3', 3, [TOP[0] + 0.15, TOP[1] + 2.92, TOP[2] + 0.55], T6 - 0.05, w=0.3)],
        cams=[cam(0.0, [9.0, 2.0, -12.0], [8.6, 2.6, -12.6], [-2.0, 14.0, -40.0], [-2.0, 15.0, -40.0], lens=44), cam(T6 - 0.35, [TOP[0] + 1.6, TOP[1] + 1.9, TOP[2] + 3.4], [TOP[0] + 1.5, TOP[1] + 1.95, TOP[2] + 3.15], [TOP[0] + 0.2, TOP[1] + 2.15, TOP[2]], [TOP[0] + 0.2, TOP[1] + 2.17, TOP[2]], lens=44)])
# 7-8: he ties it to balloons; the balloons leave
HAND = [TOP[0] + 0.05, TOP[1] + 1.45, TOP[2] + 0.5]
D8 = st.dur('S08')
st.shot('S07', 'parisStreet', actors=[act('mec', TOP, 10, 'giveItem', 'proud')], props=[CRANE_P, MODEM(HAND, ry=10), P('bunch', 'balloonBunch', pos=[HAND[0], HAND[1] + 0.07, HAND[2]], opts={'len': 1.8}, scale=0.01, keys=[k(0.3, scale=1.0, dur=0.35, ease='outBack')])],
        cams=[cam(0.0, [TOP[0] + 1.3, TOP[1] + 1.5, TOP[2] + 4.0], [TOP[0] + 1.25, TOP[1] + 1.52, TOP[2] + 3.8], [TOP[0] + 0.05, TOP[1] + 2.35, TOP[2]], [TOP[0] + 0.05, TOP[1] + 2.37, TOP[2]], lens=44)])
UP8 = [HAND[0] + 0.6, HAND[1] + 4.5, HAND[2] - 0.6]
st.shot('S08', 'parisStreet', actors=[act('mec', TOP, 10, 'stand', 'proud', keys=[k(0.15, clip='armsUp', expr='shocked', look=UP8), k(0.75, expr='sob', fx={'tears': True})])],
        props=[CRANE_P, MODEM(HAND, ry=10, keys=[k(0.05, to=[UP8[0], UP8[1] - 0.07, UP8[2]], dur=D8, ease='in')]), P('bunch', 'balloonBunch', pos=[HAND[0], HAND[1] + 0.07, HAND[2]], opts={'len': 1.8}, keys=[k(0.05, to=UP8, dur=D8, ease='in')])],
        cams=[cam(0.0, [TOP[0] + 1.6, TOP[1] + 1.0, TOP[2] + 4.2], [TOP[0] + 1.55, TOP[1] + 1.1, TOP[2] + 4.1], [TOP[0] + 0.2, TOP[1] + 2.2, TOP[2]], [TOP[0] + 0.3, TOP[1] + 3.4, TOP[2]], lens=44)])
# 9-11: over Paris, above the clouds, up to the space station
CITY = P('city', 'cityBlocks', pos=[0, 0, 0], opts={'x0': -142, 'x1': 150, 'z0': -330, 'z1': 90, 'skip': [[-21, 21, -128, 120]], 'park': [-46, 32, -222, -132]})
D9 = st.dur('S09'); B9 = [2.0, 62.0, -62.0]; B9b = [0.5, 70.0, -50.0]
st.shot('S09', 'parisStreet', props=[CITY, MODEM(B9, keys=[k(0.0, to=B9b, dur=D9)]), P('bunch', 'balloonBunch', pos=[B9[0], B9[1] + 0.07, B9[2]], opts={'len': 1.2}, keys=[k(0.0, to=[B9b[0], B9b[1] + 0.07, B9b[2]], dur=D9)])],
        cams=[cam(0.0, [B9[0] + 1.6, B9[1] + 6.0, B9[2] - 6.5], [B9b[0] + 1.6, B9b[1] + 6.0, B9b[2] - 6.5], [B9[0], B9[1] - 12.0, B9[2] + 9.0], [B9b[0], B9b[1] - 12.0, B9b[2] + 9.0], lens=44)], far=900)
D10 = st.dur('S10'); B10 = [0.0, 128.0, -60.0]; B10b = [0.0, 136.0, -64.0]
st.shot('S10', 'parisStreet', setOpts={'sky': ['#2F5FA8', '#B9DDF2'], 'eiffel': False}, props=[P('clouds', 'cloudLayer', pos=[0, 118, -60], opts={'w': 500, 'd': 500, 'n': 200, 'h': 18}),
        MODEM(B10, keys=[k(0.0, to=B10b, dur=D10)]), P('bunch', 'balloonBunch', pos=[B10[0], B10[1] + 0.07, B10[2]], opts={'len': 1.2}, keys=[k(0.0, to=[B10b[0], B10b[1] + 0.07, B10b[2]], dur=D10)])],
        cams=[cam(0.0, [B10[0] + 2.4, B10[1] - 1.4, B10[2] + 4.2], [B10b[0] + 2.4, B10b[1] - 1.0, B10b[2] + 4.2], [B10[0], B10[1] + 0.4, B10[2]], [B10b[0], B10b[1] + 0.4, B10b[2]], lens=44)])
D11 = st.dur('S11'); T11 = st.at('S11', 'L09', 3) - 0.1   # « station »: docked, four bars
ST = [0.0, 0.0, -14.0]
st.shot('S11', 'spaceDark', props=[P('earth', 'earthGlobe', pos=[0, -124, -30], opts={'radius': 58}), P('iss', 'spaceStation', pos=ST, ry=20, opts={'size': 12, 'spin': 0.0}),
        MODEM([3.5, -3.0, -10.0], keys=[k(0.0, to=[0.6, 1.95, -13.6], dur=T11, ease='out')]), BARS('bars4', 4, [2.2, 3.3, -11.5], T11, w=1.6)],
        cams=[cam(0.0, [3.5, 6.5, 6.0], [3.2, 6.6, 5.2], [0.3, -2.5, -14.0], [0.3, -2.0, -14.0], lens=44)])
# 12-13: the astronauts have wifi; they watch series all day
WALLM = [0.95, 1.7, -2.33]
st.shot('S12', 'stationInside', setOpts={'winX': -1.2}, actors=[act('astro1', [-0.45, 0.55, -0.9], 15, 'celebrate', 'starEyes', keys=[k(0.0, to=[-0.45, 0.65, -0.9], dur=2.0, glide=True, face='keep')]),
        act('astro2', [0.55, 0.45, -1.15], -20, 'celebrate', 'bigGrin', keys=[k(0.0, to=[0.55, 0.57, -1.15], dur=2.0, glide=True, face='keep')])],
        props=[MODEM(WALLM, rot=[1.5708, 0, 0]), BARS('bars5', 4, [WALLM[0] - 0.05, 2.35, -2.2], 0.15, w=0.5)],
        cams=[cam(0.0, [0.15, 2.25, 3.2], [0.14, 2.26, 2.95], [0.05, 2.05, -1.0], [0.05, 2.06, -1.0], lens=44)])
st.shot('S13', 'stationInside', setOpts={'winX': 1.6}, actors=[act('astro1', [-0.5, 0.55, -0.2], 165, 'float', 'love', keys=[k(0.0, to=[-0.5, 0.65, -0.2], dur=2.0, glide=True, face='keep')]),
        act('astro2', [0.45, 0.45, -0.3], 195, 'float', 'laugh', keys=[k(0.0, to=[0.45, 0.53, -0.3], dur=2.0, glide=True, face='keep')])],
        props=[P('screen', 'seriesScreen', pos=[0.0, 1.75, -2.3], opts={'w': 1.3, 'h': 0.78})],
        cams=[cam(0.0, [0.55, 2.2, 2.6], [0.52, 2.2, 2.35], [0.0, 1.95, -1.2], [0.0, 1.96, -1.2], lens=44)])
# 14: and he pays the subscription (zero bars, the bill pops, push in)
T14 = st.at('S14', 'L12', 5) - 0.1   # « l'abonnement »
CAM14, LOOK14 = [0.1, 1.82, 0.55], [0.0, 1.75, -1.5]
def _onscreen(cam_, look, d, sx, sy):
    f = [look[i] - cam_[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)); f = [v / n for v in f]
    r = [-f[2], 0.0, f[0]]; n = math.sqrt(r[0] ** 2 + r[2] ** 2); r = [v / n for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    return [round(cam_[i] + d * (f[i] + 0.2272 * sx * r[i] + 0.4040 * sy * u[i]), 3) for i in range(3)]
BILL14 = _onscreen(CAM14, LOOK14, 1.25, 0.42, 0.34); BILL14_RY = round(math.degrees(math.atan2(CAM14[0] - BILL14[0], CAM14[2] - BILL14[2])), 1)
st.shot('S14', 'livingRoom', setOpts=LR, actors=[act('mec', [-0.1, 0, -1.5], 0, 'showPhone', 'unimpressed', keys=[k(T14 + 0.1, expr='sob', fx={'tears': True})])],
        props=[P('phone', 'smartPhone', pos=[-0.2, 1.62, -0.98], scale=2.0), BARS('bars6', 0, [0.3, 2.42, -1.2], 0.2, w=0.3),
               P('bill', 'waterBill', pos=BILL14, ry=BILL14_RY, opts={'w': 0.3, 'h': 0.23, 'popAt': T14, 'title': 'ABONNEMENT', 'amount': '49,99 €', 'sub': 'CHAQUE MOIS', 'stamp': 'PRÉLEVÉ'})],
        cams=[cam(0.0, [0.12, 1.75, 1.5], [0.12, 1.75, 1.3], [0.0, 1.7, -1.5], [0.0, 1.7, -1.5], lens=44), cam(T14 - 0.05, [0.12, 1.75, 1.3], CAM14, [0.0, 1.7, -1.5], LOOK14, lens=44, ease='out')])
st.card('S03', 'UNE BARRE'); st.card('S10', 'TOUJOURS PLUS HAUT'); st.card('S12', 'LE WIFI')
st.cue('sfx:beep', 'S03', T3, 0.35); st.cue('sfx:beep', 'S05', T5, 0.35); st.cue('sfx:beep', 'S06', T6, 0.4); st.cue('pop', 'S07', 0.3, 0.4); st.cue('sfx:whistle', 'S08', 0.1, 0.3)
st.cue('sfx:ding', 'S11', T11, 0.4); st.cue('sfx:fanfare', 'S12', 0.1, 0.25); st.cue('sfx:paper', 'S14', T14, 0.3); st.cue('sfx:cash', 'S14', T14 + 0.3, 0.3)
st.write('Le wifi', {'astro1': {'preset': 'worker', 'seed': 131, 'suit': '#2C4A8A', 'lapel': '#2C4A8A', 'shirt': '#F2F2EE', 'pants': '#3A3D44', 'hat': 'none'},
                     'astro2': {'preset': 'madame', 'seed': 132, 'suit': '#3E7D5A', 'lapel': '#F2EDE4', 'pants': '#3A3D44'}})
