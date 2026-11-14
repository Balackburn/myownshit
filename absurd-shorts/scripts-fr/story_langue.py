#!/usr/bin/env python3
"""La langue (story 64, cycle 26 of the cartoon staging): this man stuck his tongue on a frozen lamp post. The firemen pulled for two hours. His
tongue now crosses the street. The town hall hung the Christmas lights on it. The mayor pressed the button. Everything blinks; him too. Yesterday,
the thaw. His tongue came back in one go. With the lights. He has been blinking ever since.
Staging: on a snowed-in street he leans in and licks the frosted lamp post: a frost star bursts round the tip, his eyes go wide; he pulls back, the
tongue stretches like gum, then yanks him back and his face splats flat on the pole (COLLÉ). Two firemen pull him by the waist, leaning back, while
snow piles up on their helmets; his neck and tongue stretch like rubber toward the pole. Across the whole street now: pigeons perched on the tongue,
a car drives under it and lifts it over its roof, yanking him onto his toes. A worker clips a garland of bulbs along it from the pole end; the tongue
sags under each bulb and his head bows with it, the mayor ticking his clipboard. Dusk: the mayor presses a big red button. The bulbs light up and
chase; his eyes blink with them, his face flashes red, green and gold, his hair stands up (NOËL). The thaw: the icicles drip, the frost star runs,
the tip of the tongue peels off the pole. It whips back across the street like a tape measure, the bulbs bunching on its end, the pigeons blown
off (DÉGEL); his cheeks balloon and he is knocked back. The plug slurps in last, a lump goes down his neck. At night, deadpan in the snow, his belly
blinks red, green and gold through his shirt; a passer-by stops and stares.
Natural look; cycle 26 tools: tether extras (td.lift, td.snap, td.bulbs, td.birds, td.plug, td.tip), props_langue.js (iceSleeve, bigButton,
bellyLights, snowCap), hold blinks."""
from story_kit import *
import math

st = Story('langue', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 8), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L04', 0), ('S06', 'L05', 0), ('S07', 'L06', 0),
         ('S08', 'L07', 0), ('S09', 'L08', 0), ('S10', 'L09', 0), ('S11', 'L10', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
BURST = lambda pid, pos, at_, text, w=0.5, hold=0.3: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56, 'hold': hold, 'bold': True})
DEAD = {'lid': 0.45}
PINK = '#E9788F'                                    # the tongue: a warm pink that stays apart from the white snow and the red bulbs
SNOW = {'snow': True, 'clear': [-8.0, 8.0], 'clearL': [-8.0, 8.0]}       # no tree or lamp of the set near the action on either pavement
NIGHT = {**SNOW, 'night': True}
NLOOK = {'sun': 0.12, 'sunColor': '#7F96D8', 'fill': 0.3, 'exposure': 0.9}   # a night look: the bulbs carry the street
DUSK = {'sun': 0.32, 'sunColor': '#A3A9D8', 'fill': 0.42, 'exposure': 0.95}
POLE = [-6.0, 0, 0]                                 # the frozen lamp post on the left pavement, its arm out over the road (+X)
LICK_Y = 1.88                                       # where his tongue touches it ((stills 1) level with his mouth: at 1.55 it ran down to the pole)
MOUTH = [0.0, 0.14, 0.08]                           # the mouth in the head joint's frame (head box 0.24 x 0.5 x 0.17 above the joint)
TIP = {'prop': 'lamp', 'offset': [0.1, LICK_Y, 0.0]}
TONGUE = lambda **kw: {'a': {'actor': 'mec', 'joint': 'head', 'offset': MOUTH}, 'b': TIP, 'color': PINK, 'radius': 0.045, 'radial': 8, 'tip': True, **kw}
LAMP = lambda melt=None, lick_at=None: [P('lamp', 'streetLamp', pos=POLE, opts={'height': 4.2}),
                                        P('ice', 'iceSleeve', pos=POLE, opts={'h': 4.2, 'lick': [LICK_Y, 90], 'collar': [r(LICK_Y + 0.3), 9], **({'lickAt': lick_at} if lick_at is not None else {}), **({'meltAt': melt} if melt is not None else {})})]
FAR = [5.6, 0, 0.0]                                 # where he ends up: the right-hand pavement, facing the pole across the street
COLS = ['#FF3B3B', '#3BD45A', '#FFC93B', '#3B8BFF']
BULBS = lambda **kw: {'n': 22, 'colors': COLS, 'size': 0.075, 'drop': 0.01, **kw}

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 1.45, 'mec', 'stuck'), ('S02', 0.75, 'mec', 'splat'), ('S03', 1.4, 'mec', 'pull'), ('S04', 0.7, 'mec', 'lift'), ('S05', 2.0, 'mec', 'bow'),
           ('S07', 1.1, 'mec', 'blink'), ('S09', 0.9, 'mec', 'cheeks'), ('S10', 0.8, 'mec', 'gulp'), ('S11', 1.4, 'mec', 'belly')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
st.card('S02', 'COLLÉ', at=0.45)
st.card('S07', 'NOËL', at=0.3)
st.card('S09', 'DÉGEL', at=0.25)


# 1: the hook. A snowed-in street, a frosted lamp post with icicles: he leans in, tongue out, and licks it: the frost star bursts round the tip; his
#    eyes go wide, a small tug: stuck
D1 = st.dur('S01'); LICK1 = st.at('S01', 'L01', 5)                    # on « langue »
NEAR = [r(POLE[0] + 0.52), 0, 0.0]
st.shot('S01', 'parisStreet', setOpts=SNOW, actors=[
        act('mec', NEAR, -90, 'stand', 'neutral', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.0),
            k(r(LICK1 - 0.4), toon={'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.18, 0, 0, 1.08, None]}, 'face': {'lid': 0.5, 'mouth': 'tongueout'}}, toonDur=0.3, toonEase='inOut'),   # leaning in, tongue out...
            k(r(LICK1 + 0.08), toon={'bend': {'spine': [0.24, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1.1, None]}, 'sq': [0.96, 1.04, 0.96], 'face': {'lid': 0.0, 'eye': 0.55, 'pupilSize': -0.4, 'brow': 0.9, 'mouth': 'tongueout'}}, toonDur=0.06, toonEase='out'),   # ...TSK: frozen on, eyes wide
            k(r(LICK1 + 0.3), toon={'bend': {'spine': [0.1, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1.25, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'pupilSize': -0.4, 'brow': 0.9, 'mouth': 'tongueout', 'sweat': 1.0}}, toonDur=0.12, toonEase='inOut'), k(r(LICK1 + 0.38), look='camera')])],   # a tug: the neck stretches, the tongue holds
        props=[*LAMP(lick_at=r(LICK1 + 0.05)), BURST('tsk1', [r(POLE[0] + 0.15), r(LICK_Y + 0.42), 0.35], r(LICK1 + 0.06), 'TSK !', 0.34, 0.25)],
        tethers=[TONGUE(**{'from': r(LICK1 - 0.02), 'radius': 0.03, 'sag': 0.0, 'n': 6})],
        cams=[FC(0.0, [-8.6, 2.0, 3.4], [[POLE[0], 2.5, 0.0], [NEAR[0], 2.35, 0.0], [NEAR[0], 0.9, 0.0], [POLE[0], 0.9, 0.0]], top=0.12, bottom=0.74, drift=(0.2, 0.0, -0.25))])   # (stills 1) farther and longer: the pole no nearer than him
st.cue('sfx:step', 'S01', 0.2, 0.12); st.cue('sfx:crunch', 'S01', r(LICK1 + 0.04), 0.25)

# 2: ...on a frozen post. Side on, close: he pulls back, the tongue stretches like gum, thinner and thinner; it yanks him back and his face splats
#    flat on the pole, eyes wide over the squashed cheeks (COLLÉ)
D2 = st.dur('S02'); PULL2 = 0.08; SPLAT2 = 0.44
st.shot('S02', 'parisStreet', setOpts=SNOW, actors=[
        act('mec', NEAR, -90, 'stand', 'neutral', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'bend': {'neck': [0.3, 0, 0, 1.25, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'pupilSize': -0.4, 'brow': 0.9, 'mouth': 'tongueout'}}, toonDur=0.0),
            k(PULL2, to=[r(NEAR[0] + 0.55), 0, 0.0], dur=0.28, ease='out', face='keep'), k(PULL2, toon={'bend': {'spine': [-0.35, 0, 0, 1, None], 'neck': [0.55, 0, 0, 1.55, None]}, 'face': {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'tongueout', 'sweat': 1.0}}, toonDur=0.24, toonEase='out'),   # pulling away, the neck like rubber...
            k(r(SPLAT2 - 0.06), to=[r(NEAR[0] - 0.14), 0, 0.0], dur=0.06, ease='in', face='keep'),   # ...the tongue yanks him back...
            k(SPLAT2, toon={'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.0, 0, 0, 0.9, None]}, 'scl': {'head': [1.32, 1.14, 0.5]}, 'face': {'lid': 0.0, 'eye': 0.8, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'tongueout', 'cheeks': 1.0}}, toonDur=0.03, toonEase='out'),   # ...SPLAT: flat on the pole
            k(r(SPLAT2 + 0.32), toon={'bend': {'spine': [0.22, 0, 0, 1, None]}, 'scl': {'head': [1.24, 1.1, 0.56]}, 'face': {'lid': 0.35, 'eye': 0.5, 'brow': 0.4, 'mouth': 'tongueout', 'cheeks': 0.8}}, toonDur=0.2)])],   # held, his lids drooping
        props=[*LAMP(lick_at=-1.0), BURST('splat2', [r(POLE[0] + 0.35), r(LICK_Y + 0.5), 0.3], SPLAT2, 'SPLAT !', 0.36, 0.3)],
        tethers=[TONGUE(**{'radius': 0.03, 'sag': 0.0, 'n': 8, 'thin': [0.12]})],
        cams=[FC(0.0, [-8.0, 1.8, 2.4], [[POLE[0], 2.4, 0.0], [r(NEAR[0] + 0.6), 2.4, 0.0], [r(NEAR[0] + 0.6), 1.15, 0.0], [POLE[0], 1.15, 0.0]], top=0.12, bottom=0.74)])   # (stills 1) farther and longer: his face against the pole, not behind it
st.cue('sfx:stretch', 'S02', PULL2, 0.3); st.cue('sfx:splat', 'S02', SPLAT2, 0.45)

# 3: the firemen pulled for two hours. From above the pole, down the line: the tongue rising up the frame to his face, his neck stretched, him leaning
#    back in the arms of the first fireman, the second holding the first; boots sliding; the snow piling up on the helmets (two hours)
D3 = st.dur('S03'); HOURS3 = st.at('S03', 'L02', 5)                   # on « deux »
MEC3 = [r(POLE[0] + 2.3), 0, 0.0]; F1 = [r(MEC3[0] + 0.85), 0, 0.0]; F2 = [r(MEC3[0] + 1.75), 0, 0.0]   # (stills 1) spread out: packed together they read as a hug
HOLD3 = lambda who: {'touch': {'R': [f'@{who}.torso', -0.14, 0.45, 0.06, 1, 0.05], 'L': [f'@{who}.torso', 0.14, 0.45, 0.06, 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}}
LEAN3 = lambda a: {'lay': [r(-a), 0.0], 'bend': {'spine': [0.18, 0, 0, 1, None], 'legL': [0.3, 0, 0, 1, None], 'legR': [-0.2, 0, 0, 1, None]}}   # (stills 1) tipped back from the feet: a bent spine alone did not read as pulling
HERO3 = lambda j: {'lay': [r(-0.42 - 0.04 * (j % 2)), 0.0], 'bend': {'spine': [0.1, 0, 0, 1, None], 'neck': [1.05, 0, 0, r(2.4 + 0.15 * (j % 2)), None]}, 'face': {'lid': 0.45, 'eye': 0.2, 'mouth': 'tongueout', 'brow': -0.3}}
st.shot('S03', 'parisStreet', setOpts=SNOW, actors=[
        act('mec', MEC3, -90, 'stand', 'neutral', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon=HERO3(0), toonDur=0.0),
            *[k(r(0.3 + 0.42 * j), toon=HERO3(j + 1), toonDur=0.2, toonEase='inOut') for j in range(4)]]),   # each heave stretches him a little more
        act('pomp1', F1, -90, 'stand', 'determined', keys=[k(0.0, look=[POLE[0], 1.2, 0.0]), k(0.0, toon={**HOLD3('mec'), **LEAN3(0.5), 'face': {'mouth': 'clench', 'brow': -0.6}}, toonDur=0.0),
            *[k(r(0.3 + 0.42 * j), toon={**HOLD3('mec'), **LEAN3(0.5 + 0.08 * (j % 2)), 'face': {'mouth': 'clench', 'brow': -0.6, 'sweat': 1.0}}, toonDur=0.2, toonEase='inOut') for j in range(4)]]),
        act('pomp2', F2, -90, 'stand', 'determined', keys=[k(0.0, look=[POLE[0], 1.2, 0.0]), k(0.0, toon={**HOLD3('pomp1'), **LEAN3(0.58), 'face': {'mouth': 'clench', 'brow': -0.6}}, toonDur=0.0),
            *[k(r(0.3 + 0.42 * j), toon={**HOLD3('pomp1'), **LEAN3(0.58 + 0.08 * (j % 2)), 'face': {'mouth': 'clench', 'brow': -0.6}}, toonDur=0.2, toonEase='inOut') for j in range(3)],
            k(r(HOURS3 - 0.1), look='camera'), k(r(HOURS3 - 0.05), toon={**HOLD3('pomp1'), **LEAN3(0.58), 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.15)])],   # a look to us: two hours
        props=[*LAMP(lick_at=-1.0), P('cap1', 'snowCap', on={'actor': 'pomp1', 'joint': 'head', 'offset': [0, 0.56, 0]}, opts={'t0': 0.0, 't1': D3, 'h': 0.24}),
               P('cap2', 'snowCap', on={'actor': 'pomp2', 'joint': 'head', 'offset': [0, 0.56, 0]}, opts={'t0': 0.0, 't1': D3, 'h': 0.24}),
               P('capm', 'snowCap', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.52, 0]}, opts={'t0': 0.0, 't1': D3, 'h': 0.2})],
        tethers=[TONGUE(**{'radius': 0.03, 'sag': 0.0, 'n': 10, 'taper': 0.35, 'wobble': [[0.3, 0.02, 30, 3], [0.72, 0.02, 30, 3], [1.14, 0.02, 30, 3]]})],
        cams=[FC(0.0, [-5.6, 2.9, 2.6], [[r(MEC3[0] - 0.6), 2.4, 0.0], [r(F2[0] + 0.5), 2.3, 0.0], [r(F2[0] + 0.5), 0.0, 0.0], [r(MEC3[0] - 0.6), 0.0, 0.0]], top=0.1, bottom=0.76)])   # (stills 1) from the front and above, the pole off the frame (in front of the lens it filled a third of it)
st.cue('sfx:stretch', 'S03', 0.3, 0.25); st.cue('sfx:stretch', 'S03', 1.14, 0.25); st.cue('sfx:tick', 'S03', HOURS3, 0.3)

# 4: his tongue now crosses the street. Behind his right shoulder, low: the pink tongue from his mouth across the road to the frosted pole; three
#    pigeons perched on it over the road; a little car drives under it and lifts it over its roof: he is yanked onto his toes, then dropped
D4 = st.dur('S04'); BUS4 = 0.65; GONE4 = 1.14                       # the bus under the tongue, from its front to its back (15.6 m/s)
U_CAR = r((FAR[0] - 0.12 - 2.2) / (FAR[0] - 0.12 - POLE[0] - 0.1))    # where lane x = 2.2 crosses the tongue
UP4 = 1.4; LOOK4 = r(GONE4 + 0.2); DROP4 = r(GONE4 + 0.32); LAND4 = r(DROP4 + 0.14)
HANG4 = lambda gy: {'bend': {'neck': [0.2, 0, 0, 1.4, None], 'legL': [0.3, 0, 0, 1, None], 'legR': [0.12, 0, 0, 1, None]}, 'reach': {'L': [5.75, r(1.6 + UP4), 0.8, 1, 0.05], 'R': [5.75, r(1.6 + UP4), -0.8, 1, 0.05]}, 'face': {'lid': 0.0, 'eye': 0.5, 'pupilSize': -0.4, 'mouth': 'tongueout', 'brow': 0.6, 'gy': gy}}
st.shot('S04', 'parisStreet', setOpts=SNOW, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0),
            k(r(BUS4 - 0.02), to=[FAR[0], UP4, 0.0], dur=0.16, ease='out', face='keep'), k(r(BUS4 - 0.02), toon=HANG4(0.0), toonDur=0.1, toonEase='out'), k(BUS4, look='camera'),   # yanked up behind the bus...
            k(LOOK4, toon=HANG4(0.85), toonDur=0.06), k(LOOK4, look=[FAR[0], 0.0, -0.6]),   # ...revealed hanging in the air: a look down...
            k(DROP4, to=FAR, dur=0.14, ease='in', face='keep'), k(LAND4, toon={'sq': [1.16, 0.8, 1.16], 'face': {'lid': 0.3, 'mouth': 'tongueout'}}, toonDur=0.04), k(LAND4, look='camera'),   # ...and down: squashed on landing
            k(r(LAND4 + 0.16), toon={'sq': [0.98, 1.03, 0.98], 'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.1)])],
        props=[*LAMP(lick_at=-1.0), P('bus4', 'cityBus', pos=[2.2, 0, -14.0], ry=-90, opts={'len': 7.6}, keys=[k(0.0, to=[2.2, 0, 14.0], dur=D4, ease='linear')])],
        tethers=[TONGUE(**{'sag': 0.022, 'n': 28, 'segments': 64, 'taper': 0.2, 'lift': [[BUS4, GONE4, U_CAR, 1.15, 0.1]],
                           'birds': [[0.17, r(BUS4 + 0.04), 120], [0.23, r(BUS4 + 0.08), 100], [0.3, r(BUS4 + 0.02), 140]], 'ripple': [[GONE4, 0.18, 2.0]]})],
        cams=[FC(0.0, [-1.0, 1.5, 3.4], [[FAR[0], r(2.45 + UP4), 0.0], [FAR[0], 0.0, 0.0], [3.4, 2.0, 0.0]], top=0.1, bottom=0.78)])   # (stills 2) from the road on the pole's side, facing him: the bus wipes across, then the hang
st.cue('sfx:engine', 'S04', 0.2, 0.35); st.cue('sfx:boing', 'S04', BUS4, 0.3); st.cue('sfx:slideDown', 'S04', DROP4, 0.25); st.cue('thud', 'S04', LAND4, 0.35)

# 5: the town hall hung the Christmas lights on it. A worker in the road clips bulbs onto the tongue from the pole end toward him; the tongue sags
#    deeper at each bulb and his head bows with it; the mayor beside him ticks his clipboard
D5 = st.dur('S05'); HANG5 = [-7.1, 3.8]   # (stills 1) the hanging front keeps up with the worker's hands (it ran ahead of him, off the frame)
WORK5 = [1.5, 0, -0.38]
st.shot('S05', 'parisStreet', setOpts=SNOW, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0),
            *[k(r(0.4 + 0.45 * j), toon={'bend': {'neck': [r(0.12 + 0.12 * j), 0, 0, 1, None], 'spine': [r(0.03 * j), 0, 0, 1, None]}, 'face': {'lid': r(0.45 + 0.05 * j), 'mouth': 'tongueout', 'gy': -0.4}}, toonDur=0.2, toonEase='inOut') for j in range(4)]]),   # bowing a notch at each bulb, eyes up
        act('ouv', WORK5, 90, 'stand', 'neutral', keys=[k(0.0, to=[4.0, 0, -0.38], dur=D5, ease='linear', clip='walk', then='stand', face='keep'),
            k(0.0, toon={'touch': {'R': ['torso', -0.16, 0.95, 0.4, 1, 0.05], 'L': ['torso', 0.16, 0.92, 0.4, 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'grip'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}}, toonDur=0.0)]),
        act('maire', [6.7, 0, -1.0], -120, 'stand', 'neutral', keys=[k(0.0, look=[2.0, 1.4, 0.0]), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.0),
            *[k(r(0.45 + 0.5 * j), toon={'touch': {'R': ['torso', 0.02, 0.62, 0.32, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'smirk', 'gy': 0.5}}, toonDur=0.1) for j in range(3)],
            k(r(D5 - 0.45), look='camera'), k(r(D5 - 0.4), toon={'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.1)])],   # ticking his board at each bulb, then a look to us
        props=[*LAMP(lick_at=-1.0), P('board5', 'clipboardProp', on={'actor': 'maire', 'hand': 'L'})],
        tethers=[TONGUE(**{'sag': [[0.0, 0.022], [HANG5[1], 0.05]], 'n': 24, 'segments': 56, 'taper': 0.2, 'bulbs': BULBS(hang=HANG5)})],
        cams=[FC(0.0, [0.6, 2.5, 4.8], [[FAR[0], 2.3, 0.0], [FAR[0], 0.0, 0.0], [6.7, 2.2, -1.0], [2.0, 2.3, -0.38], [2.0, 1.3, 0.0]], top=0.1, bottom=0.78)])   # (stills 2) higher and farther, the worker behind the tongue: the bulbs in front
st.cue('sfx:clink', 'S05', 0.5, 0.15); st.cue('sfx:clink', 'S05', 1.0, 0.15); st.cue('sfx:clink', 'S05', 1.5, 0.15)

# 6: the mayor pressed the button. Dusk: the mayor in his sash behind a pedestal with a big red button, two neighbours behind a red ribbon; the dark
#    garland in the sky behind; he presses: CLIC
D6 = st.dur('S06'); PRESS6 = st.at('S06', 'L05', 6)                    # on « bouton »
BTN6 = [6.2, 0, 1.4]
st.shot('S06', 'parisStreet', setOpts=NIGHT, look=DUSK, actors=[
        act('maire', [6.2, 0, 1.0], 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.25, 'mouth': 'smirk'}}, toonDur=0.0),
            k(r(PRESS6 - 0.3), toon={'reach': {'R': [6.2, 1.25, 1.4, 1, 0.05]}, 'hands': {'R': 'point'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.25, toonEase='in'),   # the finger up...
            k(PRESS6, toon={'reach': {'R': [6.2, 1.0, 1.4, 1, 0.05]}, 'hands': {'R': 'point'}, 'bend': {'spine': [0.22, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.05, toonEase='in')]),   # ...CLIC
        act('vois1', [5.3, 0, 0.3], 20, 'stand', 'neutral', keys=[k(0.0, look=BTN6), k(0.7, look=[2.0, 2.2, -1.0]), k(1.15, look=BTN6)]), act('vois2', [7.0, 0, 0.2], -20, 'stand', 'neutral', keys=[k(0.0, look=BTN6), k(0.5, look=[6.2, 2.0, 1.0]), k(r(PRESS6 - 0.1), look=BTN6), k(PRESS6, toon={'face': {'eye': 0.4, 'mouth': 'O'}}, toonDur=0.08)])],
        props=[P('btn6', 'bigButton', pos=BTN6, ry=180, opts={'pressAt': PRESS6, 'cable': 2.5}), BURST('clic6', [6.6, 1.65, 1.6], r(PRESS6 + 0.02), 'CLIC !', 0.32, 0.3)],
        cams=[FC(0.0, [6.4, 1.6, 4.2], [[6.2, 2.45, 1.0], [6.2, 0.5, 1.4], [5.3, 2.1, 0.3], [7.0, 1.7, 0.2]], top=0.18, bottom=0.76)])   # (stills 1) facing the mayor behind his button, the neighbours behind him
st.cue('sfx:click', 'S06', PRESS6, 0.4)

# 7: everything blinks; him too. Night: the garland lit and chasing on the tongue, glowing over the street; close on him: his eyes blink on the beat,
#    his face flashes red, green and gold, his hair stands up (NOËL)
D7 = st.dur('S07'); ON7 = 0.05; PER = 0.3; ALSO7 = st.at('S07', 'L06', 2)   # on « Lui »
SKINS7 = ['#FF5A5A', '#5AE070', '#FFD45A']
st.shot('S07', 'parisStreet', setOpts=NIGHT, look=NLOOK, dark=[[0.0, 0.68]], darkTint='#1E2747', darkFloor=0.16, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'bend': {'neck': [0.48, 0, 0, 1, None]}, 'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0),
            *[k(r(ALSO7 + PER * j), toon={'bend': {'neck': [0.48, 0, 0, 1, None]}, 'hairUp': 1.0, 'skin': {'color': SKINS7[j % 3], 'k': 0.85, 'glow': 0.5, 'fill': 1.0}, 'face': {'lid': 1.0 if j % 3 == 0 else 0.0, 'mouth': 'tongueout', 'eye': 0.2}}, toonDur=0.03) for j in range(int((D7 - ALSO7) / PER) + 1)]]),   # on the beat
        ],
        props=[*LAMP(lick_at=-1.0)],
        tethers=[TONGUE(**{'radius': 0.034, 'sag': 0.05, 'n': 24, 'segments': 56, 'taper': 0.25, 'bulbs': BULBS(on=ON7, period=PER)})],
        cams=[FC(0.0, [4.0, 1.7, 1.25], [[FAR[0], 2.18, 0.0], [FAR[0], 1.2, 0.0], [4.6, 1.5, 0.0]], top=0.12, bottom=0.72)])   # (stills 1) close in front of him, the lit garland leaving his mouth across the frame
st.cue('sfx:ding', 'S07', ON7, 0.3); st.cue('sfx:static', 'S07', ALSO7, 0.3)

# 8: yesterday, the thaw. Close on the pole in the sun: the icicles drip, the frost star runs, the tip of the tongue twitches and peels off
D8 = st.dur('S08'); PEEL8 = r(D8 - 0.18)
st.shot('S08', 'parisStreet', setOpts={**SNOW, 'sky': ['#62AEE2', '#A7D4EC'], 'snowN': 1}, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0)])],
        props=[*LAMP(melt=0.0, lick_at=-1.0)],
        tethers=[TONGUE(**{'sag': 0.05, 'n': 24, 'segments': 56, 'taper': 0.2, 'bulbs': BULBS(on=-1.0, period=PER), 'wobble': [[r(PEEL8 - 0.4), 0.03, 40, 2]], 'snap': [PEEL8, 1.2, 0.15]})],
        cams=[FC(0.0, [r(POLE[0] + 1.1), 1.95, 1.25], [[POLE[0], 2.4, 0.0], [POLE[0], 1.55, 0.0], [r(POLE[0] + 0.9), 1.8, 0.0]], top=0.12, bottom=0.72)])   # (stills 1) tight on the contact under the dripping collar (the icicles were up under the lamp)
st.cue('sfx:pop', 'S08', 0.2, 0.1); st.cue('sfx:pop', 'S08', 0.65, 0.1); st.cue('sfx:pop', 'S08', 1.05, 0.1); st.cue('sfx:squeak', 'S08', PEEL8, 0.25)

# 9: his tongue came back in one go. From the road, facing him: the tongue whips back across the street toward him like a tape measure, the bulbs
#    bunching on its end, the pigeons blown off; his cheeks balloon round it and he is knocked back (DÉGEL)
D9 = st.dur('S09'); SNAP9 = 0.12; DUR9 = 0.42; HOME9 = r(SNAP9 + DUR9)
st.shot('S09', 'parisStreet', setOpts={**SNOW, 'sky': ['#62AEE2', '#A7D4EC'], 'snowN': 1}, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0),
            k(r(SNAP9 + 0.1), toon={'face': {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.4, 'brow': 1.0, 'mouth': 'tongueout'}}, toonDur=0.05),   # it is coming...
            k(HOME9, to=[r(FAR[0] + 0.28), 0, 0.0], dur=0.12, ease='out', face='keep'),
            k(HOME9, look='camera'), k(HOME9, toon={'bend': {'spine': [-0.22, 0, 0, 1, None]}, 'scl': {'head': [1.62, 1.08, 1.2]}, 'face': {'lid': 0.0, 'eye': 0.7, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'O', 'puff': 1.0, 'cheeks': 1.0}}, toonDur=0.04, toonEase='out'),   # ...WHAP: cheeks full, knocked back
            k(r(HOME9 + 0.3), toon={'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'scl': {'head': [1.4, 1.05, 1.12]}, 'face': {'lid': 0.3, 'eye': 0.3, 'mouth': 'O', 'puff': 0.85, 'cheeks': 0.9}}, toonDur=0.2)])],
        props=[*LAMP(melt=-2.0, lick_at=-1.0), BURST('zip9', [2.8, 2.6, 0.6], r(SNAP9 + 0.12), 'ZIIIP !', 0.5, 0.3), P('lines9', 'speedLines', pos=[2.4, 1.7, 0.3], face='camera', opts={'n': 7, 'len': 1.6, 'w': 0.6, 'angle': 0.0, 'soft': True, 'alpha': 0.8, 'at': [[SNAP9, HOME9]]})],
        tethers=[TONGUE(**{'sag': 0.05, 'n': 24, 'segments': 56, 'taper': 0.2, 'snap': [SNAP9, DUR9, 0.45], 'bulbs': BULBS(on=-1.0, period=PER), 'birds': [[0.17, 99, 60], [0.23, 99, 40], [0.3, 99, 80]], 'plug': True})],
        cams=[FC(0.0, [3.7, 1.75, 2.2], [[FAR[0], 2.4, 0.0], [FAR[0], 0.75, 0.0], [r(FAR[0] + 0.55), 1.9, 0.0], [4.3, 1.85, 0.0]], top=0.12, bottom=0.76)])   # (stills 1) nearer, him in the middle: knocked back he left the frame
st.cue('sfx:zip', 'S09', SNAP9, 0.4); st.cue('whoosh', 'S09', r(SNAP9 + 0.15), 0.35, 0.35, 400, 1600); st.cue('sfx:boing', 'S09', HOME9, 0.4)

# 10: with the lights. Close: the plug end slurps in like the last of a spaghetti; GULP: a lump goes down his neck; his eyes cross
D10 = st.dur('S10'); SLURP10 = 0.15; GULP10 = 0.55
st.shot('S10', 'parisStreet', setOpts={**SNOW, 'sky': ['#62AEE2', '#A7D4EC'], 'snowN': 1}, actors=[
        act('mec', [r(FAR[0] + 0.45), 0, 0.0], -90, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': [1.28, 1.04, 1.08]}, 'face': {'lid': 0.3, 'mouth': 'O', 'puff': 0.8, 'cheeks': 0.9}}, toonDur=0.0),
            k(r(SLURP10 + 0.2), toon={'scl': {'head': [1.12, 1.02, 1.04]}, 'face': {'lid': 0.2, 'mouth': 'line', 'puff': 0.4, 'cheeks': 0.5}}, toonDur=0.1),
            k(GULP10, toon={'face': {'lid': 0.0, 'mouth': 'line', 'gulp': 1.0, 'cross': 0.7, 'eye': 0.3}}, toonDur=0.3, toonEase='inOut'),   # GULP
            k(r(GULP10 + 0.45), toon={'face': {**DEAD, 'mouth': 'line', 'gulp': 1.0}}, toonDur=0.15)])],
        props=[*LAMP(melt=-2.0, lick_at=-1.0), BURST('gulp10', [r(FAR[0] - 0.35), 2.05, 0.62], GULP10, 'GLOUPS !', 0.32, 0.3),
               P('lump10', 'bellyBulge', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.0, 0.0]}, opts={'r': 0.12, 'path': [[GULP10, 0.0, 0.66, 0.12], [r(GULP10 + 0.4), 0.0, 0.28, 0.14]], 'size': [[r(GULP10 - 0.01), 0.0], [r(GULP10 + 0.06), 1.0], [r(GULP10 + 0.4), 1.25], [r(GULP10 + 0.6), 0.5]]}),   # (stills 1) the lump going down shows on the chest (the neck is too short)
               P('belly10', 'bellyLights', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.28, 0.15]}, opts={'at': r(GULP10 + 0.45), 'period': PER, 'size': 0.2, 'spread': 0.09, 'k': 1.2})],
        tethers=[{'a': {'actor': 'mec', 'joint': 'head', 'offset': MOUTH}, 'b': {'actor': 'mec', 'joint': 'head', 'offset': [0.12, -0.12, 0.34]}, 'color': PINK, 'radius': 0.03, 'radial': 8, 'sag': 0.0, 'n': 6, 'snap': [SLURP10, 0.22, 0.12], 'plug': True, 'tip': True}],
        cams=[FC(0.0, [r(FAR[0] - 1.6), 1.65, 0.6], [[FAR[0], 2.35, 0.0], [FAR[0], 0.85, 0.0]], top=0.12, bottom=0.74)])   # (stills 1) his chest in the frame: the lump and the first blink go down there
st.cue('sfx:slideUp', 'S10', SLURP10, 0.3); st.cue('sfx:gulp', 'S10', GULP10, 0.4)

# 11: he has been blinking ever since. Night, the snowy pavement: deadpan, his belly blinks red, green and gold through his shirt, his eyes on the
#    beat; a passer-by stops and stares
D11 = st.dur('S11')
st.shot('S11', 'parisStreet', setOpts=NIGHT, look=NLOOK, dark=[[0.0, 0.62]], darkTint='#1E2747', darkFloor=0.18, actors=[
        act('mec', [r(FAR[0] + 0.45), 0, 0.0], -40, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            *[k(r(0.12 + PER * j), toon={'face': {'lid': 1.0 if j % 3 == 1 else 0.45}}, toonDur=0.03) for j in range(int(D11 / PER))]]),
        act('passante', [3.4, 0, -1.9], 60, 'stand', 'neutral', keys=[k(0.0, to=[4.3, 0, -1.5], dur=0.6, clip='walk', then='stand', ease='out', face='keep'), k(0.0, look=[r(FAR[0] + 0.45), 1.1, 0.0]),
            k(0.7, toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.12)])],
        props=[P('belly11', 'bellyLights', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.3, 0.14]}, opts={'at': 0.0, 'period': PER, 'size': 0.28, 'spread': 0.1, 'k': 2.6})],   # (stills 1) bigger and brighter: they were a speck on his tie
        cams=[FC(0.0, [4.5, 1.5, 2.0], [[r(FAR[0] + 0.45), 2.35, 0.0], [r(FAR[0] + 0.45), 0.8, 0.0], [4.3, 2.0, -1.5]], top=0.12, bottom=0.76)])   # (stills 2) nearer, him in the middle, his glowing belly big
st.cue('sfx:ding', 'S11', 0.12, 0.15); st.cue('sfx:ding', 'S11', 0.72, 0.12); st.cue('sfx:ding', 'S11', 1.32, 0.12)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.4}}
st.write("La langue", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, debugJoints=['mec'], extra_cast={
    'mec': MEC,
    'pomp1': {'preset': 'pompier', 'seed': 641, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'pomp2': {'preset': 'pompier', 'seed': 642, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ouv': {'preset': 'worker', 'seed': 643, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 644, 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12, 'hairColor': '#BDBDBD', 'suit': '#A9A397', 'lapel': '#A9A397', 'tie': '#7A2333', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'vois1': {'preset': 'madame', 'seed': 645, 'suit': '#8E5AA8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'vois2': {'preset': 'gamin', 'seed': 646, 'suit': '#F08A3C', 'hat': 'beanie', 'hatColor': '#3A9BDC', 'build': {'headScale': 1.25}, 'toon': EX},
    'passante': {'preset': 'femme', 'seed': 647, 'suit': '#3A9BDC', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
})
