#!/usr/bin/env python3
"""Le bus (story 72, cycle 34; in the manner of the first stories: a hook, an institutional escalation, a twist, a dry last line).
This man missed his bus by two seconds. So he ran after it. He never stopped. After an hour he had left the town. The gendarmes escorted him on
motorbikes. The villages cheered him from the roadside. The ministry of sport gave him a race number. The cycle race changed its route to follow him.
They threw him the yellow jersey. The driver never looked in his mirror. They crossed the Alps. In Italy a waiter held out pasta to him on the run.
He wore out four hundred pairs of shoes. Scientists measured his calves. After three years the bus stopped. He got on. It was not the right bus.
Staging: the stop (line 12), the bus (line 21) pulling away; a wind-up on the spot and he is off; the town sign crossed out behind him; two gendarmes
on motorbikes beside him; a village cheering with flags; the minister jogging beside him pins a number on his back; the peloton swerves after him;
the yellow jersey thrown onto him mid-run; the driver whistling, the man tiny in the rear window; a hairpin under snowy peaks; a waiter running beside
him with a plate, a noodle slurped on the run; a mountain of worn-out shoes; scientists measuring his huge calves; the bus brakes, he skids behind it,
a long beard grown; the door opens, he gets on; his ticket says 12, the display 21; a look at us.
Natural look; cycle 34: props_bus.js (townSign, raceBib, jersey, pastaPlate, shoePile), props reused (cityBus, busStop, motorbike, bicycle,
mountainRange, tapeMeasure, beardHair, bigTicket, floorSlab, tree, flag, speedLines, dustPuff)."""
from story_kit import *
import math

st = Story('bus', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L08', 7), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L10', 3), ('S13', 'L11', 0), ('S14', 'L12', 0),
         ('S15', 'L12', 4), ('S16', 'L13', 0), ('S17', 'L14', 0), ('S18', 'L15', 0), ('S19', 'L16', 0), ('S20', 'L17', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.76, 'fit': 0.6, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
V = 4.0                                              # running speed (m/s): the bus keeps BUSD ahead of him
BUSD = 5.2                                           # the bus's middle ahead of him (its back about 1.4 m ahead of his nose)
BUS = lambda pid, pos, ry, keys=None, **o: P(pid, 'cityBus', pos=pos, ry=ry, opts={'len': 7.6, 'line': '21', 'dest': 'ROME', **o}, **({'keys': keys} if keys else {}))
ROAD = lambda pid, z=0.0, w=3.4, x=0.0, ln=160.0: P(pid, 'floorSlab', pos=[x, 0.03, z], ry=90, opts={'w': w, 'd': ln, 'h': 0.04, 'color': '#8C8C88'})   # a country road along X
LINE = lambda pid, z=0.0, x=0.0, ln=160.0: P(pid, 'floorSlab', pos=[x, 0.052, z], ry=90, opts={'w': 0.08, 'd': ln, 'h': 0.004, 'color': '#F2F0E8'})
TREES = lambda tag, z, x0, x1, n, s=1.2: [P(f'tr{tag}{i}', 'tree', pos=[r(x0 + (x1 - x0) * i / max(1, n - 1)), 0, r(z + 0.6 * ((i * 37) % 7 - 3) / 3)], scale=r(s * (0.85 + 0.3 * ((i * 53) % 5) / 4))) for i in range(n)]
RUNK = lambda p1, dur, t0=0.0, speed=1.6: [k(t0, to=p1, dur=dur, clip='run', ease='linear'), k(t0, clip='run', speed=speed)]   # legs fast: a blur
PANT = lambda t0, n=4: [k(r(t0 + 0.22 * j), toon={'sq': [1.03, 0.96, 1.03] if j % 2 == 0 else [0.99, 1.02, 0.99], 'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.1) for j in range(n)]

for g_ in [('S02', 0.4, 'mec', 'windup'), ('S07', 1.2, 'mec', 'bib'), ('S10', 0.9, 'mec', 'jersey'), ('S15', 0.9, 'mec', 'slurp'), ('S17', 1.0, 'mec', 'calves'), ('S20', 1.2, 'mec', 'end')]:
    st.gag(*g_)
st.card('S10', 'JAUNE', at=0.55)
st.card('S16', 'USÉES', at=0.5)
st.card('S20', 'RATÉ', at=0.75)

# 1: the hook. At the stop (line 12) in a Paris street: he sprints in from behind us and skids to a stop at the kerb, an arm out, as the bus pulls away
#    (its rear display: 21); he stands there, panting, deadpan
D1 = st.dur('S01'); ME1 = [4.8, 0, 0.6]; ARR1 = 0.85
st.shot('S01', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', [5.0, 0, 6.5], 180, 'run', 'determined', keys=[*RUNK(ME1, ARR1), k(ARR1, clip='heelBrake'), k(ARR1, toon={'reach': {'R': [4.3, 1.9, -0.4, 1, 0.04]}, 'hands': {'R': 'open'}, 'sq': [1.06, 0.94, 1.06], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'open'}}, toonDur=0.08, toonEase='out'),
            k(r(ARR1 + 0.3), clip='stand'), k(r(ARR1 + 0.35), toon={'reach': {'R': [4.3, 1.75, -0.4, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.2), *PANT(r(ARR1 + 0.5), 4), k(0.0, look=[3.5, 1.6, -4.0])]),
        act('passant1', [6.9, 0, -1.2], -110, 'stand', 'neutral', keys=[k(0.0, look=[ME1[0], 1.8, ME1[2]]), k(1.4, look='camera')])],
        props=[BUS('bus1', [3.5, 0, -0.6], 90, keys=[k(0.0, to=[3.5, 0, -15.0], dur=D1, ease='in')], doors=[[0.0, 0.3], [0.25, 0.0]]),
               P('abri1', 'busStop', pos=[6.6, 0, 0.0], ry=-90), P('ligne1', 'signBoard', pos=[5.9, 0, -1.3], ry=-90, opts={'text': '12', 'bg': '#2F62B5', 'fg': '#FFFFFF', 'w': 0.42, 'h': 0.42, 'height': 2.2, 'posts': True}),
               P('dust1', 'dustPuff', pos=[ME1[0], 0.0, ME1[2]], scale=0.5, opts={'once': True, 'startAt': ARR1, 'period': 0.5, 'color': '#EFE8D8'})],
        cams=[FC(0.0, [6.4, 1.25, 4.4], [[ME1[0], 2.45, ME1[2]], [ME1[0], 0.0, ME1[2]], [3.5, 2.8, -3.0], [3.5, 0.3, -3.0], [5.9, 2.75, -1.3]], top=0.14, bottom=0.78)])
st.cue('sfx:stepSoft', 'S01', 0.2, 0.15); st.cue('sfx:stepSoft', 'S01', 0.5, 0.15); st.cue('sfx:skid', 'S01', ARR1, 0.3); st.cue('engine', 'S01', 0.1, 0.35)

# 2: so he ran after it. Side on at the kerb: a Looney wind-up on the spot, his legs a whirl, dust spinning up; then he is off down the street in a
#    puff, speed lines behind
D2 = st.dur('S02'); GO2 = 0.62; ME2 = [4.6, 0, 0.0]
st.shot('S02', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[
        act('mec', ME2, 180, 'windUp', 'determined', keys=[k(0.0, look=[4.0, 1.7, -8.0]), k(0.0, toon={'lay': [0.22, 0.0], 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.0),
            k(GO2, toon={'lay': [0.0, 0.0], 'sq': [0.8, 1.25, 0.8], 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.05, toonEase='out'), *RUNK([4.6, 0, -9.0], r(D2 - GO2), GO2, 2.0)])],   # leaning in, whirling... and off
        props=[P('dust2', 'dustPuff', pos=[ME2[0], 0.0, ME2[2]], scale=0.6, opts={'period': 0.3, 'color': '#EFE8D8'}, keys=[k(r(GO2 + 0.25), visible=False)]),
               P('puff2', 'dustPuff', pos=[ME2[0], 0.0, r(ME2[2] - 0.4)], scale=1.0, opts={'once': True, 'startAt': GO2, 'period': 0.5, 'color': '#EFE8D8'}),
               P('sl2', 'speedLines', pos=[ME2[0], 1.3, 0.6], rot=[0, PI / 2, 0], opts={'count': 7, 'length': 1.6, 'dir': -1}, keys=[k(0.0, visible=False), k(GO2, visible=True), k(r(GO2 + 0.35), visible=False)])],
        cams=[FC(0.0, [8.6, 1.3, -1.2], [[ME2[0], 2.5, ME2[2]], [ME2[0], 0.0, ME2[2]], [ME2[0], 2.5, -2.4], [ME2[0], 0.0, 1.0]], top=0.16, bottom=0.78)])
st.cue('sfx:windup', 'S02', 0.05, 0.3); st.cue('whoosh', 'S02', GO2, 0.4)

# 3: he never stopped. Low behind him in the street, travelling with him: his legs a blur, the bus always just ahead, its rear display 21
D3 = st.dur('S03'); Z3 = 2.0
st.shot('S03', 'parisStreet', setOpts={'clear': [-30.0, 30.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [3.6, 0, Z3], 180, 'run', 'determined', keys=[*RUNK([3.6, 0, r(Z3 - V * D3)], D3, 0.0, 2.0), k(0.0, look=[3.6, 1.7, -8.0])])],
        props=[BUS('bus3', [3.5, 0, r(Z3 - BUSD)], 90, keys=[k(0.0, to=[3.5, 0, r(Z3 - BUSD - V * D3)], dur=D3, ease='linear')])],
        cams=[FC(0.0, [4.4, 0.75, r(Z3 + 3.2)], [[3.6, 2.4, Z3], [3.6, 0.0, Z3], [3.5, 3.0, r(Z3 - BUSD + 3.8)], [3.5, 0.3, r(Z3 - BUSD + 3.8)]], top=0.14, bottom=0.78, drift=(0.0, 0.0, r(-V * D3)))])
st.cue('engine', 'S03', 0.0, 0.3); st.cue('sfx:stepSoft', 'S03', 0.3, 0.15); st.cue('sfx:stepSoft', 'S03', 0.6, 0.15); st.cue('sfx:stepSoft', 'S03', 0.9, 0.15)

# 4: after an hour he had left the town. The road out of town: the town sign crossed out (SAINT-ARRÊT); the bus goes by it, then him; the last houses
D4 = st.dur('S04'); SG4 = [0.0, 0, 2.2]
st.shot('S04', 'grassland', actors=[act('mec', [r(-BUSD - 4.0), 0, 0.3], 90, 'run', 'determined', keys=[*RUNK([r(-BUSD - 4.0 + V * D4), 0, 0.3], D4, 0.0, 2.0)])],
        props=[ROAD('road4'), LINE('line4'), BUS('bus4', [-4.0, 0, -0.3], 0, keys=[k(0.0, to=[r(-4.0 + V * D4), 0, -0.3], dur=D4, ease='linear')]),
               P('panneau4', 'townSign', pos=SG4, ry=-15, opts={'name': 'SAINT-ARRÊT', 'exit': True, 'w': 1.5, 'h': 1.4}),
               *[P(f'mais4{j}', 'pavilion', pos=[r(-16.0 - 7.0 * j), 0, r(-7.0 + 3.0 * (j % 2))], ry=r(20 * j)) for j in range(3)], *TREES('4', 5.0, -14.0, 14.0, 6)],
        cams=[FC(0.0, [3.6, 1.2, 7.5], [[SG4[0], 2.2, SG4[2]], [SG4[0], 0.0, SG4[2]], [r(-BUSD - 4.0 + V * D4 * 0.7), 2.4, 0.3], [r(-4.0 + V * D4 * 0.4), 2.8, -0.3]], top=0.16, bottom=0.78)])
st.cue('engine', 'S04', 0.0, 0.3); st.cue('whoosh', 'S04', 0.5, 0.25)

# 5: the gendarmes escorted him on motorbikes. On the country road, travelling with them from in front: two gendarmes on motorbikes either side of him,
#    blue lights turning; one gives us a thumbs-up
D5 = st.dur('S05'); X5 = 0.0
MOTO5 = [(-1.2, 'gend1'), (1.2, 'gend2')]
st.shot('S05', 'grassland', actors=[act('mec', [X5, 0, 0.0], 90, 'run', 'determined', keys=[*RUNK([r(X5 + V * D5), 0, 0.0], D5, 0.0, 2.0), k(0.0, look=[8.0, 1.7, 0.0])]),
        *[act(g_, [r(X5 - 0.9 - 0.16), 0.5, zz], 90, 'ride', 'determined', keys=[k(0.0, to=[r(X5 - 0.9 - 0.16 + V * D5), 0.5, zz], dur=D5, ease='linear'), k(0.0, look=[8.0, 1.6, zz]),
            *([k(0.9, look='camera'), k(0.9, toon={'reach': {'R': [r(X5 - 0.7 + V * 0.9), 1.6, r(zz + 0.45), 1, 0.04]}, 'hands': {'R': 'thumb'}, 'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.15)] if zz > 0 else [])]) for zz, g_ in MOTO5]],
        props=[ROAD('road5'), LINE('line5'), BUS('bus5', [r(X5 + BUSD), 0, 0.0], 0, keys=[k(0.0, to=[r(X5 + BUSD + V * D5), 0, 0.0], dur=D5, ease='linear')]),
               *[P(f'moto5{j}', 'motorbike', pos=[r(X5 - 0.9), 0, zz], opts={'color': '#2F4A8A', 'roll': 40}, keys=[k(0.0, to=[r(X5 - 0.9 + V * D5), 0, zz], dur=D5, ease='linear')]) for j, (zz, _) in enumerate(MOTO5)],
               *[P(f'gyro5{j}', 'policeFlash', on={'actor': g_, 'joint': 'head', 'offset': [0.0, 0.35, -0.2]}, scale=0.6) for j, (zz, g_) in enumerate(MOTO5)], *TREES('5', -6.0, -6.0, 18.0, 6)],
        cams=[FC(0.0, [r(X5 + 3.8), 1.2, 1.9], [[X5, 2.45, 0.0], [X5, 0.0, 0.0], [r(X5 - 0.9), 2.2, -1.2], [r(X5 - 0.9), 2.2, 1.2], [r(X5 - 0.9), 0.0, 1.2]], top=0.16, bottom=0.78, drift=(r(V * D5), 0.0, 0.0))])
st.cue('sfx:siren', 'S05', 0.0, 0.25); st.cue('engine', 'S05', 0.1, 0.3)

# 6: the villages cheered him from the roadside. A village street: villagers along the verge clap and wave flags, a kid jumps; he runs by, deadpan
D6 = st.dur('S06'); X6 = -3.0; FANS6 = [('fan1', -1.6, 'mamie'), ('fan2', -0.5, 'gamin'), ('fan3', 0.7, 'farmer'), ('fan4', 1.9, 'madame'), ('fan5', 3.1, 'tourist')]
st.shot('S06', 'cottageStreet', actors=[act('mec', [X6, 0, 0.6], 90, 'run', 'determined', keys=[*RUNK([r(X6 + V * D6), 0, 0.6], D6, 0.0, 2.0)]),
        *[act(fid, [fx, 0, 2.3], 180, 'stand', 'happy', keys=[k(0.0, look=[r(X6 + V * 0.4 * (j + 1)), 1.6, 0.6]), *[k(r(0.1 + 0.18 * i + 0.05 * j), toon={'reach': {'R': [r(fx + (0.12 if i % 2 else -0.12)), 2.25, 2.0, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.08) for i in range(10)]] +
              ([k(0.3, to=[fx, 0.35, 2.3], dur=0.15, ease='out'), k(0.45, to=[fx, 0, 2.3], dur=0.15, ease='in'), k(0.9, to=[fx, 0.35, 2.3], dur=0.15, ease='out'), k(1.05, to=[fx, 0, 2.3], dur=0.15, ease='in')] if j == 1 else [])) for j, (fid, fx, _) in enumerate(FANS6)]],
        props=[*[P(f'drap6{j}', 'flag', on={'actor': FANS6[j][0], 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=0.35, opts={'colors': ['#2F62B5', '#F4F4F0', '#E0413A']}) for j in (0, 2, 4)],
               BUS('bus6', [r(X6 + BUSD), 0, 0.0], 0, keys=[k(0.0, to=[r(X6 + BUSD + V * D6), 0, 0.0], dur=D6, ease='linear')])],
        cams=[FC(0.0, [0.4, 1.3, -3.4], [[r(X6 + V * D6 * 0.5), 2.45, 0.6], [-1.6, 2.4, 2.3], [3.1, 2.4, 2.3], [r(X6 + V * D6 * 0.5), 0.0, 0.6]], top=0.14, bottom=0.76, drift=(1.6, 0.0, 0.0))])
st.cue('sfx:cheer', 'S06', 0.1, 0.35)

# 7: the ministry of sport gave him a race number. Jogging beside him on the road, the minister in a tracksuit pins a number on his back; he does not
#    look; the minister gives us a thumbs-up
D7 = st.dur('S07'); X7 = 0.0; PIN7 = 1.0
st.shot('S07', 'grassland', actors=[act('mec', [X7, 0, 0.0], 90, 'run', 'determined', keys=[*RUNK([r(X7 + V * D7), 0, 0.0], D7, 0.0, 2.0), k(r(PIN7 + 0.02), toon={'sq': [1.04, 0.96, 1.04], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.04), k(r(PIN7 + 0.12), toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1)]),
        act('ministre', [r(X7 - 0.8), 0, -0.75], 90, 'run', 'happy', keys=[*RUNK([r(X7 - 0.8 + V * D7), 0, -0.75], D7, 0.0, 2.0), k(0.0, look=[X7, 1.4, 0.0]),
            k(r(PIN7 - 0.3), toon={'reach': {'L': [r(X7 - 0.35 + V * (PIN7 - 0.3)), 1.45, -0.18, 1, 0.04], 'R': [r(X7 - 0.35 + V * (PIN7 - 0.3)), 1.5, -0.12, 1, 0.04]}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {'lid': 0.2, 'mouth': 'smirk'}}, toonDur=0.25, toonEase='inOut'),
            k(r(PIN7 + 0.25), look='camera'), k(r(PIN7 + 0.25), toon={'reach': {'R': [r(X7 - 0.6 + V * (PIN7 + 0.25)), 1.7, -0.4, 1, 0.04]}, 'hands': {'R': 'thumb'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.15)])],
        props=[ROAD('road7'), LINE('line7'), BUS('bus7', [r(X7 + BUSD), 0, 0.0], 0, keys=[k(0.0, to=[r(X7 + BUSD + V * D7), 0, 0.0], dur=D7, ease='linear')]),
               P('dos7', 'raceBib', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.42, -0.17]}, rot=[0, PI, 0], scale=1.3, opts={'num': '1'}, keys=[k(0.0, visible=False), k(PIN7, visible=True)]), *TREES('7', -5.0, -4.0, 16.0, 5)],
        cams=[FC(0.0, [r(X7 - 3.0), 1.6, 1.0], [[X7, 2.45, 0.0], [X7, 1.0, 0.0], [r(X7 - 0.8), 2.45, -0.75], [r(X7 - 0.8), 1.0, -0.75]], top=0.16, bottom=0.76, drift=(r(V * D7), 0.0, 0.0))])   # from behind his other shoulder: the number on his back, the minister beyond him
st.cue('sfx:click', 'S07', PIN7, 0.25)

# 8: the cycle race changed its route... From above a fork in the road: the peloton was going left; it swerves right after him and the bus
D8 = st.dur('S08'); RID8 = ['#E0413A', '#2F62B5', '#F2C94E', '#2F8F6B', '#8E5AA8', '#E0813A']
def rider(aid, x, z, ry, col, keys=None, bike_keys=None):
    a = ry * PI / 180; return (act(aid, [r(x - 0.16 * math.sin(a)), 0.5, r(z - 0.16 * math.cos(a))], ry, 'ride', 'determined', keys=keys or [], params={'cadence': 1.8, 'lean': 0.8}),
                               P(f'bk_{aid}', 'bicycle', pos=[x, 0, z], rot=[0, r(a - PI / 2), 0], opts={'color': col}, **({'keys': bike_keys} if bike_keys else {})))
PEL8 = [(r(-4.0 - 1.1 * (j // 2)), r(-0.5 + 1.0 * (j % 2)), RID8[j]) for j in range(6)]
R8 = [x for j, (px, pz, c_) in enumerate(PEL8) for x in rider(f'cyc{j + 1}', px, pz, 90, c_, keys=[k(0.0, to=[r(px + 2.0), 0.5, r(pz + 1.6)], dur=0.7, ease='inOut'), k(0.7, to=[r(px + 6.0), 0.5, r(pz + 4.6)], dur=r(D8 - 0.7), ease='linear')],
                                                                 bike_keys=[k(0.0, to=[r(px + 2.0), 0, r(pz + 1.6)], dur=0.7, ease='inOut'), k(0.7, to=[r(px + 6.0), 0, r(pz + 4.6)], dur=r(D8 - 0.7), ease='linear')])]
st.shot('S08', 'grassland', actors=[act('mec', [3.0, 0, 3.5], 55, 'run', 'determined', keys=[*RUNK([r(3.0 + 3.4), 0, r(3.5 + 2.4)], D8, 0.0, 2.0)]), *[x for x in R8 if x.get('clip') == 'ride']],
        props=[ROAD('road8a', 0.0, 3.0, -10.0, 30.0), P('road8b', 'floorSlab', pos=[4.0, 0.03, 4.0], ry=55, opts={'w': 3.0, 'd': 26.0, 'h': 0.04, 'color': '#8C8C88'}), *[x for x in R8 if x.get('name') == 'bicycle'],
               P('fl8', 'signBoard', pos=[1.2, 0, -2.4], ry=-20, opts={'text': '→ ARRIVÉE', 'bg': '#F4F4F0', 'fg': '#2F62B5', 'w': 1.0, 'h': 0.3, 'height': 1.4}),
               BUS('bus8', [r(3.0 + 4.3), 0, r(3.5 + 3.0)], -35, keys=[k(0.0, to=[r(3.0 + 7.7), 0, r(3.5 + 5.4)], dur=D8, ease='linear')]), *TREES('8', -6.0, -12.0, 8.0, 5)],
        cams=[FC(0.0, [-1.0, 15.0, 13.0], [[-6.0, 1.5, -0.5], [3.0, 2.0, 3.5], [8.0, 2.4, 6.5], [-2.0, 1.5, 1.5]], top=0.14, bottom=0.76, lenses=range(26, 70))])
st.cue('sfx:bell', 'S08', 0.2, 0.2); st.cue('whoosh', 'S08', 0.5, 0.25)

# 9: ...to follow him. Side on, travelling: he leads the peloton, the riders in a tight bunch behind him, the bus ahead
D9 = st.dur('S09'); X9 = 0.0
R9 = [x for j in range(6) for x in rider(f'cyc{j + 1}', r(X9 - 1.6 - 1.0 * (j // 2)), r(-0.45 + 0.9 * (j % 2)), 90, RID8[j], keys=[k(0.0, to=[r(X9 - 1.6 - 1.0 * (j // 2) + V * D9), 0.5, r(-0.45 + 0.9 * (j % 2))], dur=D9, ease='linear')],
                                    bike_keys=[k(0.0, to=[r(X9 - 1.6 - 1.0 * (j // 2) + V * D9), 0, r(-0.45 + 0.9 * (j % 2))], dur=D9, ease='linear')])]
st.shot('S09', 'grassland', actors=[act('mec', [X9, 0, 0.0], 90, 'run', 'determined', keys=[*RUNK([r(X9 + V * D9), 0, 0.0], D9, 0.0, 2.0)]), *[x for x in R9 if x.get('clip') == 'ride']],
        props=[ROAD('road9'), LINE('line9'), *[x for x in R9 if x.get('name') == 'bicycle'], BUS('bus9', [r(X9 + BUSD), 0, 0.0], 0, keys=[k(0.0, to=[r(X9 + BUSD + V * D9), 0, 0.0], dur=D9, ease='linear')]), *TREES('9', -5.5, -10.0, 14.0, 6)],
        cams=[FC(0.0, [r(X9 - 1.0), 1.1, 5.6], [[X9, 2.45, 0.0], [r(X9 - 3.6), 1.6, 0.45], [r(X9 + BUSD - 1.0), 2.8, 0.0], [X9, 0.0, 0.0]], top=0.16, bottom=0.78, drift=(r(V * D9), 0.0, 0.0))])
st.cue('sfx:bell', 'S09', 0.3, 0.15)

# 10: they threw him the yellow jersey. On the road a spectator throws it; it flies over and drops onto him mid-run, squashing onto his shoulders;
#     he runs on in it, deadpan (JAUNE)
D10 = st.dur('S10'); X10 = 0.0; ON10 = 0.6
st.shot('S10', 'grassland', actors=[act('mec', [X10, 0, 0.0], 90, 'run', 'determined', keys=[*RUNK([r(X10 + V * D10), 0, 0.0], D10, 0.0, 2.0), k(r(ON10 + 0.02), toon={'sq': [1.06, 0.93, 1.06], 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.04), k(r(ON10 + 0.12), toon={'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.1)]),
        act('lanceur', [1.0, 0, 2.4], -170, 'stand', 'happy', keys=[k(0.0, look=[r(X10 + V * 0.4), 1.6, 0.0]), k(0.0, toon={'reach': {'R': [0.85, 2.4, 2.2, 1, 0.04]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(0.15, toon={'reach': {'R': [0.9, 2.0, 1.8, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.1, toonEase='out'),
            *[k(r(0.7 + 0.2 * j), toon={'reach': {'R': [r(0.9 + (0.12 if j % 2 else -0.12)), 2.55, 2.2, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.1) for j in range(5)]])],   # waving after him
        props=[ROAD('road10'), LINE('line10'), BUS('bus10', [r(X10 + BUSD), 0, 0.0], 0, keys=[k(0.0, to=[r(X10 + BUSD + V * D10), 0, 0.0], dur=D10, ease='linear')]),
               P('mj10a', 'jersey', pos=[0.9, 2.0, 1.8], scale=0.9, keys=[k(0.15, to=[r(X10 + V * ON10), 2.1, 0.0], dur=r(ON10 - 0.15), ease='inOut', arc=0.8), k(ON10, visible=False)]),   # it flies over...
               P('mj10', 'jersey', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'at': ON10, 'w': 0.5, 'h': 0.62, 'd': 0.3}),   # ...and drops onto him
               *TREES('10', -5.0, -8.0, 14.0, 5)],
        cams=[FC(0.0, [r(X10 + 3.4), 1.45, 2.9], [[X10, 2.45, 0.0], [X10, 0.8, 0.0], [1.0, 2.4, 2.4], [r(X10 + V * 0.8), 2.45, 0.0]], top=0.16, bottom=0.76, drift=(r(V * D10 * 0.8), 0.0, 0.0))])   # three-quarter front: his face, not a box side
st.cue('whoosh', 'S10', 0.2, 0.25); st.cue('thud', 'S10', ON10, 0.25); st.cue('sfx:fanfare', 'S10', r(ON10 + 0.1), 0.2)

# 11: the driver, though... Inside the bus, behind the driver: his cap, his arms on the big wheel, whistling, the road ahead through the windscreen
D11 = st.dur('S11')
st.shot('S11', 'grassland', actors=[act('chauffeur', [2.75, 0.45, -0.5], 90, 'drive', 'neutral', keys=[k(0.0, look=[12.0, 1.8, -0.5]), *[k(r(0.1 + 0.2 * j), toon={'face': {'lid': 0.3, 'mouth': 'whistle'}, 'sq': [1.0, 1.02 if j % 2 else 0.99, 1.0]}, toonDur=0.1) for j in range(5)]])],
        props=[ROAD('road11'), LINE('line11'), BUS('bus11', [0.0, 0, 0.0], 0, top=2.8), *TREES('11', -5.0, 4.0, 30.0, 6), *TREES('11b', 5.0, 4.0, 30.0, 6)],
        cams=[FC(0.0, [1.6, 1.85, -0.15], [[2.75, 2.2, -0.5], [2.75, 1.2, -0.5], [6.0, 1.8, 0.0]], top=0.14, bottom=0.78, inside=(-3.6, 3.6, 0.6, 2.2, -1.0, 1.0), lenses=range(30, 70))])
st.cue('sfx:whistle', 'S11', 0.15, 0.2)

# 12: ...never looked in his mirror. From the front, through the windscreen: the driver whistling, his eyes on the road; his mirror turned away; far
#     behind, through the rear window, him running, tiny
D12 = st.dur('S12'); X12 = 0.0
st.shot('S12', 'grassland', actors=[act('chauffeur', [r(X12 + 2.75), 0.45, -0.5], 90, 'drive', 'neutral', keys=[k(0.0, to=[r(X12 + 2.75 + V * D12), 0.45, -0.5], dur=D12, ease='linear'), k(0.0, look=[30.0, 1.8, -0.5]), *[k(r(0.1 + 0.2 * j), toon={'face': {'lid': 0.35, 'mouth': 'whistle'}}, toonDur=0.1) for j in range(10)]]),
        act('mec', [r(X12 - BUSD), 0, 0.7], 90, 'run', 'determined', keys=[*RUNK([r(X12 - BUSD + V * D12), 0, 0.7], D12, 0.0, 2.0)])],   # off the driver's line: seen beside him through the rear window
        props=[ROAD('road12'), LINE('line12'), BUS('bus12', [X12, 0, 0.0], 0, top=2.8, keys=[k(0.0, to=[r(X12 + V * D12), 0, 0.0], dur=D12, ease='linear')]), *TREES('12', -5.0, -20.0, 20.0, 8)],
        cams=[FC(0.0, [r(X12 + 7.6), 1.75, -2.6], [[r(X12 + 2.75), 2.3, -0.5], [r(X12 + 2.75), 1.2, -0.5], [r(X12 - BUSD), 2.4, 0.7]], top=0.16, bottom=0.78, lenses=range(16, 50), drift=(r(V * D12), 0.0, 0.0))])
st.cue('sfx:whistle', 'S12', 0.1, 0.2); st.cue('engine', 'S12', 0.0, 0.25)

# 13: they crossed the Alps. A hairpin road under snowy peaks: the bus climbs round the bend, he follows, small, the peaks huge behind
D13 = st.dur('S13')
st.shot('S13', 'grassland', setOpts={'ground': '#9DB88C'}, actors=[act('mec', [-3.2, 0, 1.6], 90, 'run', 'determined', keys=[*RUNK([r(-3.2 + V * D13), 0, 1.6], D13, 0.0, 2.0)])],
        props=[P('alpes13', 'mountainRange', pos=[0.0, 0, -40.0], opts={'n': 8, 'w': 90, 'h': 30, 'd': 18, 'seed': 13}), ROAD('road13', 1.6, 3.0), P('road13b', 'floorSlab', pos=[6.0, 0.03, -1.6], ry=90, opts={'w': 3.0, 'd': 30.0, 'h': 0.04, 'color': '#8C8C88'}),
               P('lacet13', 'floorSlab', pos=[-2.0, 0.03, 0.0], opts={'w': 3.0, 'd': 6.0, 'h': 0.04, 'color': '#8C8C88'}),
               BUS('bus13', [6.0, 0, -1.6], 180, keys=[k(0.0, to=[r(6.0 - V * D13), 0, -1.6], dur=D13, ease='linear')]), *[P(f'sapin13{j}', 'tree', pos=[r(-12.0 + 4.0 * j), 0, r(-6.0 - 2.0 * (j % 3))], scale=1.5, opts={'kind': 'pine'}) for j in range(7)]],
        cams=[FC(0.0, [1.5, 3.2, 16.0], [[-5.0, 0.0, 1.6], [7.0, 0.0, -1.6], [0.0, 14.0, -40.0], [-3.2, 2.4, 1.6]], top=0.12, bottom=0.78, lenses=range(26, 70))])
st.cue('engine', 'S13', 0.0, 0.25); st.cue('gust', 'S13', 0.2, 0.2)

# 14: in Italy a waiter... A village street with striped awnings: a waiter in an apron dashes out of a café with a plate of spaghetti held high
D14 = st.dur('S14'); X14 = -2.0
st.shot('S14', 'cottageStreet', setOpts={'seed': 23}, actors=[act('serveur', [1.6, 0, 2.6], -160, 'run', 'happy', keys=[k(0.0, to=[0.8, 0, 0.9], dur=r(D14 - 0.1), clip='run', ease='out'), k(0.0, toon={'reach': {'R': [1.75, 2.35, 2.5, 1, 0.04]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.0, 'mouth': 'bigsmile'}}, toonDur=0.0), k(0.0, look=[X14, 1.6, 0.6])]),
        act('mec', [X14, 0, 0.6], 90, 'run', 'determined', keys=[*RUNK([r(X14 + V * D14), 0, 0.6], D14, 0.0, 2.0)])],
        props=[P('pates14', 'pastaPlate', on={'actor': 'serveur', 'hand': 'R', 'offset': [0.0, 0.05, 0.0]}, scale=1.4), P('tab14', 'bistroTable', pos=[2.6, 0, 3.0], opts={'r': 0.35, 'h': 0.75}),
               BUS('bus14', [r(X14 + BUSD), 0, 0.0], 0, keys=[k(0.0, to=[r(X14 + BUSD + V * D14), 0, 0.0], dur=D14, ease='linear')])],
        cams=[FC(0.0, [-0.6, 1.4, -3.2], [[1.6, 2.5, 2.6], [0.8, 2.5, 0.9], [X14, 2.45, 0.6], [r(X14 + V * D14), 2.45, 0.6], [0.8, 0.0, 0.9]], top=0.14, bottom=0.78, drift=(1.2, 0.0, 0.0))])
st.cue('sfx:bell', 'S14', 0.05, 0.15)

# 15: ...held out pasta to him on the run. Side by side, travelling: the waiter holds out the plate; he sucks up one long noodle without breaking step
D15 = st.dur('S15'); X15 = 0.0; SL15 = [0.45, 1.25]
st.shot('S15', 'grassland', actors=[act('mec', [X15, 0, 0.0], 90, 'run', 'determined', keys=[*RUNK([r(X15 + V * D15), 0, 0.0], D15, 0.0, 2.0), k(SL15[0], toon={'face': {'lid': 0.4, 'mouth': 'kiss', 'cheeks': 0.6}}, toonDur=0.08), k(SL15[1], toon={'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.1)]),
        act('serveur', [X15, 0, 0.75], 90, 'run', 'happy', keys=[*RUNK([r(X15 + V * D15), 0, 0.75], D15, 0.0, 2.0), k(0.0, look=[X15, 1.9, 0.0]), k(0.0, toon={'reach': {'L': [r(X15 + 0.1), 1.75, 0.38, 1, 0.04]}, 'hands': {'L': 'open'}, 'face': {'lid': 0.1, 'mouth': 'bigsmile'}}, toonDur=0.0)])],
        props=[P('pates15', 'pastaPlate', on={'actor': 'serveur', 'hand': 'L', 'offset': [0.0, 0.05, 0.0]}, scale=1.3, opts={'noodle': [0.0, 0.3, -0.32], 'slurp': SL15}), ROAD('road15'), LINE('line15'),
               BUS('bus15', [r(X15 + BUSD), 0, -0.1], 0, keys=[k(0.0, to=[r(X15 + BUSD + V * D15), 0, -0.1], dur=D15, ease='linear')]), *TREES('15', -5.0, -8.0, 14.0, 5)],
        cams=[FC(0.0, [r(X15 + 2.5), 1.85, -1.5], [[X15, 2.45, 0.0], [X15, 1.3, 0.0], [X15, 2.4, 0.75], [r(X15 + 0.1), 1.6, 0.4]], top=0.16, bottom=0.74, drift=(r(V * D15), 0.0, 0.0))])   # three-quarter front on the slurp
st.cue('sfx:slurp', 'S15', SL15[0], 0.3)

# 16: he wore out four hundred pairs of shoes. By the road a mountain of worn-out shoes; as he runs past, a sole flaps off and a new pair lands on
#     his feet (USÉES)
D16 = st.dur('S16'); X16 = -4.0
st.shot('S16', 'grassland', actors=[act('mec', [X16, 0, 0.6], 90, 'run', 'determined', keys=[*RUNK([r(X16 + V * D16), 0, 0.6], D16, 0.0, 2.0)])],
        props=[ROAD('road16', 0.4), P('tas16', 'shoePile', pos=[1.0, 0, -2.4], scale=2.0, opts={'n': 90, 'r': 1.0, 'h': 0.9}, keys=[k(0.0, scale=1.6, dur=0.0), k(0.4, scale=2.0, dur=1.2, ease='out')]),
               P('chaus16', 'shoePile', pos=[r(X16 + V * 0.9), 0.4, 0.6], scale=0.4, opts={'n': 2, 'r': 0.1, 'h': 0.1}, keys=[k(0.0, visible=False), k(0.9, visible=True), k(0.9, to=[r(X16 + V * 0.9 - 0.6), 1.6, -1.2], dur=0.35, ease='out', arc=0.8)]),
               P('fume16', 'dustPuff', on={'actor': 'mec', 'joint': 'footL', 'offset': [0.0, 0.0, 0.0]}, scale=0.3, opts={'period': 0.4, 'color': '#D9D2C4'}), *TREES('16', -6.0, -12.0, 12.0, 5)],
        cams=[FC(0.0, [-0.4, 1.4, 5.4], [[1.0, 1.9, -2.4], [r(X16 + V * D16 * 0.5), 2.45, 0.6], [r(X16 + V * D16 * 0.5), 0.0, 0.6], [-1.0, 0.0, -2.4], [3.0, 0.0, -2.4]], top=0.16, bottom=0.78, drift=(0.8, 0.0, 0.0))])
st.cue('sfx:squeak', 'S16', 0.9, 0.2)

# 17: scientists measured his calves. Running beside him, two scientists in white coats hold a tape measure round his calves, swollen huge; one
#     writes on a clipboard; their eyes pop
D17 = st.dur('S17'); X17 = 0.0
CALF = {'scl': {'shinL': [1.9, 1.05, 1.9], 'shinR': [1.9, 1.05, 1.9]}}
st.shot('S17', 'grassland', actors=[act('mec', [X17, 0, 0.0], 90, 'run', 'determined', keys=[*RUNK([r(X17 + V * D17), 0, 0.0], D17, 0.0, 1.6), k(0.0, toon={**CALF, 'face': {**DEAD, 'mouth': 'line'}}, toonDur=0.0)]),
        *[act(sid, [r(X17 - 0.1), 0, zz], 90, 'run', 'neutral', keys=[*RUNK([r(X17 - 0.1 + V * D17), 0, zz], D17, 0.0, 1.6), k(0.0, look=[X17, 0.5, 0.0]),
            k(0.0, toon={'bend': {'spine': [0.45, 0, 0, 1, None]}, 'reach': {'R': [r(X17 - 0.05), 0.55, r(zz * 0.4), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'brow': 0.8}}, toonDur=0.0),
            k(r(0.9 + 0.1 * j), toon={'bend': {'spine': [0.45, 0, 0, 1, None]}, 'reach': {'R': [r(X17 - 0.05), 0.55, r(zz * 0.4), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.5, 'pop': 0.6, 'popLen': 0.14, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.06, toonEase='out')])
          for j, (sid, zz) in enumerate([('savant1', -0.75), ('savant2', 0.75)])]],
        props=[ROAD('road17'), LINE('line17'), P('metre17', 'tapeMeasure', on={'actor': 'savant1', 'hand': 'R', 'offset': [0.0, 0.0, 0.03]}, scale=1.2),
               P('ruban17', 'slab', pos=[r(X17 - 0.05), 0.5, 0.0], opts={'w': 0.02, 'h': 0.03, 'd': 1.5, 'color': '#F2C230'}, keys=[k(0.0, to=[r(X17 - 0.05 + V * D17), 0.5, 0.0], dur=D17, ease='linear')]),
               BUS('bus17', [r(X17 + BUSD), 0, 0.0], 0, keys=[k(0.0, to=[r(X17 + BUSD + V * D17), 0, 0.0], dur=D17, ease='linear')]), *TREES('17', -5.5, -8.0, 14.0, 5)],
        cams=[FC(0.0, [r(X17 + 2.4), 1.0, 2.6], [[X17, 2.45, 0.0], [X17, 0.0, 0.0], [r(X17 - 0.1), 2.2, -0.75], [r(X17 - 0.1), 2.2, 0.75]], top=0.14, bottom=0.78, drift=(r(V * D17), 0.0, 0.0))])
st.cue('sfx:stretch', 'S17', 0.3, 0.2); st.cue('sfx:boing', 'S17', 0.95, 0.2)

# 18: after three years the bus stopped. In a town square: the bus brakes hard at a stop, rocking; he skids in behind it on his heels, smoke from his
#     soles; three years have passed: his beard down to his chest
D18 = st.dur('S18'); STOP18 = 1.0; ME18 = [-1.0, 0, 0.0]
st.shot('S18', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [3.6, 0, 6.5], 180, 'run', 'determined', keys=[*RUNK([3.6, 0, 1.8], r(STOP18 + 0.1), 0.0, 2.0), k(r(STOP18 + 0.1), clip='heelBrake'), k(r(STOP18 + 0.1), to=[3.6, 0, 1.2], dur=0.3, ease='out'), k(r(STOP18 + 0.45), clip='stand'),
            k(r(STOP18 + 0.1), toon={'lay': [-0.2, 0.0], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'clench'}}, toonDur=0.06), k(r(STOP18 + 0.45), toon={'lay': [0.0, 0.0], 'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.15), *PANT(r(STOP18 + 0.65), 4)])],
        props=[BUS('bus18', [3.5, 0, 2.0], 90, keys=[k(0.0, to=[3.5, 0, -3.2], dur=STOP18, ease='out')], doors=[[0.0, 0.0]]), P('arret18', 'busStop', pos=[6.6, 0, -3.6], ry=-90),
               P('barbe18', 'beardHair', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.02, 0.1]}, scale=0.75, opts={'len': 1.2, 'coil': 0.0, 'swing': [0.0, r(STOP18 + 0.3), 0.18], 'whip': True}),
               P('fumee18', 'dustPuff', pos=[3.6, 0.0, 1.4], scale=0.7, opts={'once': True, 'startAt': r(STOP18 + 0.1), 'period': 0.6, 'color': '#E8E2D6'})],
        cams=[FC(0.0, [2.0, 0.95, -0.9], [[3.6, 2.5, 1.2], [3.6, 0.0, 1.2], [3.6, 2.5, 3.5], [2.35, 2.8, 0.4], [2.35, 0.3, 0.4]], top=0.14, bottom=0.78)])   # low beside the bus's back: he skids in at us
st.cue('sfx:brake', 'S18', r(STOP18 - 0.3), 0.35); st.cue('sfx:skid', 'S18', r(STOP18 + 0.1), 0.3)

# 19: he got on. At the open doors: he climbs the step, panting, beard and jersey and number, and gets on
D19 = st.dur('S19'); DOOR19 = [4.65, 0, -3.9]
st.shot('S19', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', [5.4, 0, -3.9], -90, 'walk', 'neutral', keys=[k(0.15, to=[4.75, 0.45, -3.9], dur=0.35, clip='walk', then='stand', ease='out'), k(0.0, look=[4.0, 1.8, -3.9]), k(0.15, toon={'sq': [1.04, 0.96, 1.04], 'face': {**DEAD, 'mouth': 'open'}}, toonDur=0.1)])],
        props=[BUS('bus19', [3.5, 0, -3.2], 90, doors=[[0.0, 1.0]]), P('barbe19', 'beardHair', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.02, 0.1]}, scale=0.75, opts={'len': 1.2, 'coil': 0.0}),
               P('mj19', 'jersey', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'w': 0.5, 'h': 0.62, 'd': 0.3})],
        cams=[FC(0.0, [6.8, 1.5, -1.4], [[5.4, 2.45, -3.9], [5.4, 0.0, -3.9], [4.55, 2.6, -3.0], [4.55, 0.3, -4.6]], top=0.14, bottom=0.78)])
st.cue('sfx:stepSoft', 'S19', 0.25, 0.2)

# 20: it was not the right bus. At the open front door, three-quarter front: on the step, in his jersey and beard, he holds up his ticket: LIGNE 12;
#     his eyes go up to the bus's front display: 21 ROME; then to us (RATÉ)
D20 = st.dur('S20'); ME20 = [2.25, 0.44, 0.92]; TK20 = [2.62, 2.05, 1.22]
TKP = lambda f: {'reach': {'R': TK20 + [1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': f}
st.shot('S20', 'parisStreet', setOpts={'clear': [-8.0, 8.0], 'eiffelStyle': 'v2'}, actors=[act('mec', ME20, 0, 'stand', 'neutral', keys=[k(0.0, look=TK20), k(0.0, toon=TKP({**DEAD, 'mouth': 'open'}), toonDur=0.0),
            k(0.6, look=[3.85, 2.55, 0.0]), k(1.1, look=TK20), k(1.5, look='camera'), k(1.55, toon=TKP({**DEAD, 'mouth': 'line'}), toonDur=0.15),
            k(1.85, toon=TKP({'lid': 1.0, 'mouth': 'line'}), toonDur=0.12), k(2.05, toon=TKP({**DEAD, 'mouth': 'line'}), toonDur=0.12)])],   # ticket, display, ticket, us; a slow blink
        props=[BUS('bus20', [0.0, 0, 0.0], 0, doors=[[0.0, 1.0]]), P('ticket20', 'bigTicket', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, 0.04, 0.03]}, face='camera', scale=0.6, opts={'title': 'TICKET', 'sum': 'LIGNE 12', 'color': '#DCEBF6'}),
               P('barbe20', 'beardHair', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.02, 0.1]}, scale=0.75, opts={'len': 1.2, 'coil': 0.0}), P('mj20', 'jersey', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, -0.05, 0.0]}, opts={'w': 0.5, 'h': 0.62, 'd': 0.3})],
        cams=[FC(0.0, [4.6, 1.9, 4.2], [[ME20[0], 2.95, ME20[2]], [ME20[0], 1.5, ME20[2]], TK20, [3.85, 2.75, 0.0], [3.85, 2.35, 0.0]], top=0.18, bottom=0.74)])
st.cue('sfx:paper', 'S20', 0.1, 0.15); st.cue('sfx:sting', 'S20', 0.75, 0.2)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("Le bus", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'passant1': {'preset': 'madame', 'seed': 721, 'suit': '#C255C8', 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    'gend1': {'preset': 'cop', 'seed': 722, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'gend2': {'preset': 'cop2', 'seed': 723, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'fan1': {'preset': 'mamie', 'seed': 724, 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'fan2': {'preset': 'gamin', 'seed': 725, 'suit': '#7CC25A', 'build': {'headScale': 1.25}, 'toon': EX},
    'fan3': {'preset': 'farmer', 'seed': 726, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'fan4': {'preset': 'madame', 'seed': 727, 'suit': '#3A9BDC', 'build': {'width': 0.92, 'headWidth': 1.25}, 'toon': EX},
    'fan5': {'preset': 'tourist', 'seed': 728, 'suit': '#E0813A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'tracksuit', 'seed': 729, 'suit': '#2F62B5', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'cyc{j + 1}': {'preset': 'sportif', 'seed': 730 + j, 'suit': c_, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX} for j, c_ in enumerate(RID8)},
    'lanceur': {'preset': 'tourist', 'seed': 737, 'suit': '#5BB5A8', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'chauffeur': {'preset': 'officiel', 'seed': 738, 'suit': '#2F5FA8', 'hat': 'copcap', 'hatColor': '#2F5FA8', 'build': {'width': 1.1, 'headWidth': 1.2}, 'toon': EX},
    'serveur': {'preset': 'waiter', 'seed': 739, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'savant1': {'preset': 'savant', 'seed': 740, 'hair': 'receding', 'hairColor': '#EDEDED', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'savant2': {'preset': 'savant', 'seed': 741, 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.25}, 'toon': EX},
})
