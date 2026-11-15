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
DAY = {**SNOW, 'sky': ['#62AEE2', '#A7D4EC']}   # (review 1) white snow, a grey road (peach and beige under the warm default sky)
NLOOK = {'sun': 0.1, 'sunColor': '#8FA4E0', 'fill': 0.25, 'exposure': 1.05}   # a night look: the bulbs carry the street; (review 1) a cool fill, no darkening after the fact (99 % of the frame under luma 52); (review 2) a third of the ambient: the walls were only 6-10 % darker than by day
GLOW = lambda pid, pos, col, k_=2.5, dist=3.0: P(pid, 'glowLight', pos=pos, opts={'color': col, 'k': k_, 'dist': dist})
DUSK = {'sun': 0.5, 'sunColor': '#FFB585', 'elevation': 10, 'fill': 0.5, 'exposure': 1.0}   # (review 2) a low orange sun under an indigo sky (S06 was full night, with stars)
DUSKSET = {**SNOW, 'sky': ['#3B4A7A', '#E89A6A'], 'clear': [-60.0, 8.0], 'clearL': [-60.0, 8.0]}   # (review 2) and no lamp bracket rising behind the mayor's head
DLOOK = {'sunColor': '#F4F6FF', 'warm': 0.55}   # (review 2) a white sun by day: the snow measured (240, 212, 190) under the warm default (near white in S08-S10)
WLOOK = {'sunColor': '#FFE3B5', 'sun': 1.1, 'elevation': 20}   # (review 2) the thaw: a low warm sun on the pole
POLE = [-6.0, 0, 0]                                 # the frozen lamp post on the left pavement, its arm out over the road (+X)
LICK_Y = 1.88                                       # where his tongue touches it ((stills 1) level with his mouth: at 1.55 it ran down to the pole)
MOUTH = [0.0, 0.14, 0.08]                           # the mouth in the head joint's frame (head box 0.24 x 0.5 x 0.17 above the joint)
TIP = {'prop': 'lamp', 'offset': [0.1, LICK_Y, 0.0]}
TONGUE = lambda **kw: {'a': {'actor': 'mec', 'joint': 'head', 'offset': MOUTH}, 'b': TIP, 'color': PINK, 'radius': 0.045, 'radial': 8, 'tip': True, **kw}
# (review 2) the frost star inked and turned toward the cameras (white on the white post, edge on, behind his head: it never showed)
LAMP = lambda melt=None, lick_at=None: [P('lamp', 'streetLamp', pos=POLE, opts={'height': 4.2}),
                                        P('ice', 'iceSleeve', pos=POLE, opts={'h': 4.2, 'lick': [LICK_Y, 20], 'starInk': True, 'starSize': 0.42, 'collar': [r(LICK_Y + 0.3), 9], **({'lickAt': lick_at} if lick_at is not None else {}), **({'meltAt': melt} if melt is not None else {})})]
FAR = [5.6, 0, 0.0]                                 # where he ends up: the right-hand pavement, facing the pole across the street
COLS = ['#FF3B3B', '#3BD45A', '#FFC93B', '#3B8BFF']
BULBS = lambda **kw: {'n': 30, 'colors': COLS, 'size': 0.11, 'drop': 0.01, 'dim': 0.85, 'glow': 2.4, **kw}   # (stills 3) bigger and brighter while off: at 5 m they were dull specks

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
st.shot('S01', 'parisStreet', setOpts=DAY, look=DLOOK, actors=[
        act('mec', NEAR, -90, 'stand', 'neutral', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.3, toon={'bend': {'spine': [0.14, 0, 0, 1, None], 'neck': [0.1, 0, 0, 1.04, None]}, 'face': {'lid': 0.4, 'mouth': 'smirk', 'brow': 0.3}}, toonDur=0.45, toonEase='inOut'),   # (review 2) leaning from 0.3 s (he stood still for 0.8 s)...
            k(0.8, toon={'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.18, 0, 0, 1.08, None]}, 'face': {'lid': 0.5, 'mouth': 'tongueout'}}, toonDur=0.35, toonEase='inOut'),   # ...tongue out...
            k(r(LICK1 + 0.08), toon={'bend': {'spine': [0.24, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1.1, None]}, 'sq': [0.96, 1.04, 0.96], 'face': {'lid': 0.0, 'eye': 0.55, 'pupilSize': -0.4, 'brow': 0.9, 'mouth': 'tongueout'}}, toonDur=0.06, toonEase='out'),   # ...TSK: frozen on...
            k(r(LICK1 + 0.13), toon={'bend': {'spine': [0.24, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1.1, None]}, 'face': {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'tongueout', 'pop': 0.45, 'popLen': 0.12}}, toonDur=0.03, toonEase='out'),   # ...two frames on, the eyes pop...
            k(r(LICK1 + 0.2), toon={'lay': [-0.12, 0.0], 'bend': {'spine': [0.05, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1.6, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'pupilSize': -0.4, 'brow': 0.9, 'mouth': 'tongueout', 'sweat': 1.0, 'pop': 0.2, 'popLen': 0.12}}, toonDur=0.1, toonEase='out'),   # ...a tug: the neck like rubber, the tongue holds...
            k(r(LICK1 + 0.31), toon={'lay': [0.0, 0.0], 'bend': {'spine': [0.24, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1.1, None]}, 'sq': [1.06, 0.95, 1.06], 'face': {'lid': 0.45, 'eye': 0.0, 'mouth': 'tongueout', 'sweat': 1.0}}, toonDur=0.04, toonEase='in'), k(r(LICK1 + 0.29), look='camera')])],   # ...snapped back to the post: six frames of deadpan to us
        props=[*LAMP(lick_at=r(LICK1 + 0.05)), BURST('tsk1', [r(POLE[0] + 0.15), r(LICK_Y + 0.42), 0.35], r(LICK1 + 0.06), 'TSK !', 0.34, 0.25)],
        tethers=[TONGUE(**{'from': r(LICK1 - 0.02), 'radius': 0.03, 'sag': 0.0, 'n': 6})],
        cams=[FC(0.0, [-6.7, 1.95, 2.1], [[r(POLE[0] - 0.15), 2.5, 0.0], [r(NEAR[0] + 0.25), 2.45, 0.0], [r(NEAR[0] + 0.25), 0.9, 0.0], [r(POLE[0] - 0.15), 0.9, 0.0]], top=0.14, bottom=0.74, drift=(0.12, 0.0, -0.18))])   # (review 1) three-quarters in front of him, the pole at the left: the lick in view
st.cue('sfx:step', 'S01', 0.2, 0.12); st.cue('sfx:crunch', 'S01', r(LICK1 + 0.04), 0.25)

# 2: ...on a frozen post. Side on, close: he pulls back, the tongue stretches like gum, thinner and thinner; it yanks him back and his face splats
#    flat on the pole, eyes wide over the squashed cheeks (COLLÉ)
D2 = st.dur('S02'); PULL2 = 0.08; SPLAT2 = 0.44; POP2 = r(SPLAT2 + 0.18)
WIDE2 = {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'tongueout', 'sweat': 1.0}
st.shot('S02', 'parisStreet', setOpts=DAY, look=DLOOK, actors=[
        act('mec', NEAR, -90, 'stand', 'neutral', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'bend': {'neck': [0.3, 0, 0, 1.25, None]}, 'face': {'lid': 0.0, 'eye': 0.5, 'pupilSize': -0.4, 'brow': 0.9, 'mouth': 'tongueout'}}, toonDur=0.0),
            k(PULL2, toon={'lay': [-0.38, 0.0], 'bend': {'spine': [-0.15, 0, 0, 1, None], 'neck': [0.95, 0, 0, 2.8, None]}, 'face': WIDE2}, toonDur=0.26, toonEase='out'),   # (review 1) feet planted, leaning back: the neck like rubber (he walked back before)
            k(r(SPLAT2 - 0.06), toon={'lay': [0.06, 0.0], 'bend': {'spine': [0.2, 0, 0, 1, None], 'neck': [0.0, 0, 0, 0.9, None]}, 'face': WIDE2}, toonDur=0.06, toonEase='in'), k(r(SPLAT2 - 0.06), to=[r(NEAR[0] - 0.12), 0, 0.0], dur=0.06, ease='in', face='keep'),   # ...the tongue yanks him back...
            k(SPLAT2, toon={'lay': [0.0, 0.0], 'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.0, 0, 0, 0.9, None]}, 'scl': {'head': [1.36, 1.12, 0.46]}, 'face': {'lid': 0.0, 'eye': 0.7, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'tongueout', 'cheeks': 1.0, 'pop': 0.55, 'popLen': 0.12}}, toonDur=0.03, toonEase='out'),   # ...SPLAT: flat on the pole, eyes out
            k(POP2, toon={'bend': {'spine': [0.18, 0, 0, 1, None]}, 'scl': {'head': [0.88, 1.1, 1.22]}, 'face': {'lid': 0.0, 'eye': 0.4, 'brow': 0.6, 'mouth': 'tongueout'}}, toonDur=0.1, toonEase='out'), k(POP2, to=[r(NEAR[0] - 0.03), 0, 0.0], dur=0.08, ease='out', face='keep'),   # (review 2) the head re-inflates past round over three frames...
            k(r(POP2 + 0.1), toon={'bend': {'spine': [0.16, 0, 0, 1, None]}, 'scl': {'head': [1.06, 0.97, 0.95]}, 'face': {'lid': 0.2, 'eye': 0.3, 'brow': 0.4, 'mouth': 'tongueout'}}, toonDur=0.08, toonEase='inOut'),   # ...wobbles back...
            k(r(POP2 + 0.18), toon={'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'eye': 0.1, 'brow': 0.2, 'mouth': 'tongueout'}}, toonDur=0.12, toonEase='inOut')])],   # ...and the lids droop
        props=[*LAMP(lick_at=-1.0), BURST('splat2', [r(POLE[0] - 0.3), r(LICK_Y + 0.3), 0.4], SPLAT2, 'SPLAT !', 0.36, 0.3)],   # (review 1) beside his head, under the card's band; (review 2) against the post by his face (375 px off the impact)
        tethers=[TONGUE(**{'radius': 0.03, 'sag': 0.0, 'n': 8, 'thin': [0.12]})],
        cams=[FC(0.0, [-6.45, 1.75, 1.6], [[r(POLE[0] - 0.15), 2.5, 0.0], [r(NEAR[0] + 0.85), 2.3, 0.0], [r(NEAR[0] + 0.35), 1.2, 0.0], [r(POLE[0] - 0.15), 1.2, 0.0]], top=0.24, bottom=0.74)])   # (review 1) nearer, in front at three-quarters: the flat face in view, room under the card
st.cue('sfx:stretch', 'S02', PULL2, 0.3); st.cue('sfx:splat', 'S02', SPLAT2, 0.45); st.cue('pop', 'S02', POP2, 0.2)

# 3: the firemen pulled for two hours. From above the pole, down the line: the tongue rising up the frame to his face, his neck stretched, him leaning
#    back in the arms of the first fireman, the second holding the first; boots sliding; the snow piling up on the helmets (two hours)
D3 = st.dur('S03'); HOURS3 = st.at('S03', 'L02', 5)                   # on « deux »
MEC3 = [r(POLE[0] + 2.3), 0, 0.0]; F1 = [r(MEC3[0] + 0.85), 0, 0.0]; F2 = [r(MEC3[0] + 1.75), 0, 0.0]   # (stills 1) spread out: packed together they read as a hug
HOLD3 = lambda who: {'touch': {'R': [f'@{who}.torso', -0.14, 0.45, 0.06, 1, 0.05], 'L': [f'@{who}.torso', 0.14, 0.45, 0.06, 1, 0.05]}, 'hands': {'R': 'grip', 'L': 'grip'}}
LEAN3 = lambda a, st_=0.0: {'lay': [r(-a), 0.0], 'bend': {'spine': [r(0.18 + 0.12 * st_), 0, 0, 1, None], 'neck': [r(0.4 * st_), 0, 0, 1, None], 'legL': [r(0.3 - 0.4 * st_), 0, 0, 1, None], 'shinL': [r(0.6 * st_), 0, 0, 1, None], 'legR': [r(-0.2 - 0.2 * st_), 0, 0, 1, None], 'shinR': [r(0.45 * st_), 0, 0, 1, None]}}   # (review 1) straining: knees bent, head down
HERO3 = lambda a, ln, lid=0.45: {'lay': [r(-a), 0.0], 'bend': {'spine': [0.1, 0, 0, 1, None], 'neck': [1.05, 0, 0, r(ln), None]}, 'face': {'lid': lid, 'eye': 0.2, 'mouth': 'tongueout', 'brow': -0.3}}
H3 = [0.25, 0.85, 1.45]                                                 # (review 1) three heaves on a beat
K3m = [k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon=HERO3(0.42, 2.4), toonDur=0.0)]
K3a = [k(0.0, look=[POLE[0], 1.2, 0.0]), k(0.0, toon={**HOLD3('mec'), **LEAN3(0.5), 'face': {'mouth': 'clench', 'brow': -0.6}}, toonDur=0.0)]
K3b = [k(0.0, look=[POLE[0], 1.2, 0.0]), k(0.0, toon={**HOLD3('pomp1'), **LEAN3(0.58), 'face': {'mouth': 'clench', 'brow': -0.6}}, toonDur=0.0)]
for j, h in enumerate(H3):
    ln = r(2.9 + 0.5 * j); sl = r(0.1 * (j + 1))
    K3m += [k(r(h - 0.12), toon=HERO3(0.36, r(ln - 0.5)), toonDur=0.1, toonEase='inOut'), k(h, toon=HERO3(0.58, ln), toonDur=0.08, toonEase='out'),   # eased forward, then yanked: the neck a notch longer...
            k(h, to=[r(MEC3[0] + sl), 0, 0.0], dur=0.12, ease='out', face='keep'), k(r(h + 0.2), toon=HERO3(0.47, ln), toonDur=0.24, toonEase='inOut'),   # ...his heels sliding; settle...
            k(r(h + 0.36), toon=HERO3(0.47, ln, 1.0), toonDur=0.05), k(r(h + 0.44), toon=HERO3(0.47, ln), toonDur=0.06)]   # ...a blink
    K3a += [k(r(h - 0.12), toon={**HOLD3('mec'), **LEAN3(0.36, 0.3), 'face': {'mouth': 'clench', 'brow': -0.6}}, toonDur=0.1, toonEase='inOut'), k(h, toon={**HOLD3('mec'), **LEAN3(0.74, 1.0), 'face': {'mouth': 'clench', 'brow': -0.8, 'sweat': 1.0}}, toonDur=0.08, toonEase='out'),
            k(h, to=[r(F1[0] + sl), 0, 0.0], dur=0.12, ease='out', face='keep'), k(r(h + 0.2), toon={**HOLD3('mec'), **LEAN3(0.55, 0.6), 'face': {'mouth': 'clench', 'brow': -0.6, 'sweat': 1.0}}, toonDur=0.24, toonEase='inOut')]
    if j < 2: K3b += [k(r(h - 0.1), toon={**HOLD3('pomp1'), **LEAN3(0.42, 0.3), 'face': {'mouth': 'clench', 'brow': -0.6}}, toonDur=0.1, toonEase='inOut'), k(r(h + 0.02), toon={**HOLD3('pomp1'), **LEAN3(0.8, 1.0), 'face': {'mouth': 'clench', 'brow': -0.8}}, toonDur=0.08, toonEase='out'),
            k(r(h + 0.02), to=[r(F2[0] + sl), 0, 0.0], dur=0.12, ease='out', face='keep'), k(r(h + 0.22), toon={**HOLD3('pomp1'), **LEAN3(0.62, 0.6), 'face': {'mouth': 'clench', 'brow': -0.6}}, toonDur=0.24, toonEase='inOut')]
K3b += [k(r(HOURS3 - 0.12), look='camera'), k(r(HOURS3 - 0.12), toon={**HOLD3('pomp1'), **LEAN3(0.5, 0.0), 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.13, toonEase='inOut'),   # (review 2) he stops heaving, head up, a turn to us...
        k(r(HOURS3 + 0.35), toon={**HOLD3('pomp1'), **LEAN3(0.5, 0.0), 'face': {'lid': 1.0, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.04), k(r(HOURS3 + 0.41), toon={**HOLD3('pomp1'), **LEAN3(0.5, 0.0), 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.06),   # ...a blink...
        k(r(HOURS3 + 0.62), toon={**HOLD3('pomp1'), **LEAN3(0.5, 0.0), 'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.7}}, toonDur=0.1)]   # ...an eyebrow: two hours
K3b.sort(key=lambda kk: kk['at'])
st.shot('S03', 'parisStreet', setOpts=DAY, look=DLOOK, actors=[act('mec', MEC3, -90, 'stand', 'neutral', keys=K3m), act('pomp1', F1, -90, 'stand', 'determined', keys=K3a), act('pomp2', F2, -90, 'stand', 'determined', keys=K3b)],
        props=[*LAMP(lick_at=-1.0), P('cap1', 'snowCap', on={'actor': 'pomp1', 'joint': 'head', 'offset': [0, 0.56, 0]}, opts={'t0': 0.0, 't1': D3, 'h': 0.24}),
               P('cap2', 'snowCap', on={'actor': 'pomp2', 'joint': 'head', 'offset': [0, 0.56, 0]}, opts={'t0': 0.0, 't1': D3, 'h': 0.24}),
               P('capm', 'snowCap', on={'actor': 'mec', 'joint': 'head', 'offset': [0, 0.52, 0]}, opts={'t0': 0.0, 't1': D3, 'h': 0.2})],
        tethers=[TONGUE(**{'radius': 0.03, 'sag': 0.0, 'n': 10, 'taper': 0.35, 'wobble': [[h, 0.03, 30, 3] for h in H3]})],
        cams=[FC(0.0, [-5.6, 2.9, 2.6], [[r(MEC3[0] - 0.6), 2.4, 0.0], [r(F2[0] + 1.6), 2.3, 0.0], [r(F2[0] + 1.6), 0.0, 0.0], [r(MEC3[0] - 0.6), 0.0, 0.0]], top=0.1, bottom=0.76)])   # (review 1) room on the right: the second fireman was cut in half; (review 2) his helmet was still cut
for h_ in H3: st.cue('sfx:stretch', 'S03', h_, 0.25)
st.cue('sfx:tick', 'S03', HOURS3, 0.3)

# 4: his tongue now crosses the street. Behind his right shoulder, low: the pink tongue from his mouth across the road to the frosted pole; three
#    pigeons perched on it over the road; a little car drives under it and lifts it over its roof: he is yanked onto his toes, then dropped
D4 = st.dur('S04'); BUS4 = 0.49; GONE4 = 0.97                       # the bus under the tongue, from its front to its back (15.6 m/s); (stills 3) earlier: it clears the line of sight at 1.12
U_CAR = r((FAR[0] - 0.12 - 2.2) / (FAR[0] - 0.12 - POLE[0] - 0.1))    # where lane x = 2.2 crosses the tongue
UP4 = 1.4; LOOK4 = 0.75; LOOKUS4 = 0.95; DROP4 = 1.15; LAND4 = r(DROP4 + 0.14)   # (review 1) the hang in view from 0.65: a look down, a look to us, then the drop; (review 2) earlier: room for the landing before the cut
HANG4 = lambda gy, kick=0: {'bend': {'neck': [0.2, 0, 0, 1.4, None], 'legL': [r(0.3 - 0.75 * kick), 0, 0, 1, None], 'legR': [r(0.12 + 0.7 * kick), 0, 0, 1, None], 'shinL': [r(0.6 * abs(kick)), 0, 0, 1, None]}, 'reach': {'L': [5.75, r(1.6 + UP4), 0.8, 1, 0.05], 'R': [5.75, r(1.6 + UP4), -0.8, 1, 0.05]}, 'face': {'lid': 0.0, 'eye': 0.5, 'pupilSize': -0.4, 'mouth': 'tongueout', 'brow': 0.6, 'gy': gy}}
st.shot('S04', 'parisStreet', setOpts=DAY, look=DLOOK, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0),
            k(r(BUS4 - 0.02), to=[FAR[0], UP4, 0.0], dur=0.16, ease='out', face='keep'), k(r(BUS4 - 0.02), toon={**HANG4(0.0, 1.0), 'sq': [0.88, 1.18, 0.88]}, toonDur=0.08, toonEase='out'), k(BUS4, look='camera'),   # (review 1) yanked up, stretched, legs kicking...
            k(r(BUS4 + 0.1), toon=HANG4(0.0, -0.8), toonDur=0.07, toonEase='inOut'), k(r(BUS4 + 0.2), toon=HANG4(0.0, 0.5), toonDur=0.07, toonEase='inOut'), k(r(BUS4 + 0.3), toon=HANG4(0.0), toonDur=0.1),
            k(LOOK4, toon=HANG4(0.85), toonDur=0.06), k(LOOK4, look=[FAR[0], 0.0, -0.6]), k(LOOKUS4, look='camera'), k(LOOKUS4, toon=HANG4(0.0), toonDur=0.06),   # ...hanging in the air: a look down, a look to us...
            k(DROP4, to=FAR, dur=0.14, ease='in', face='keep'), k(LAND4, toon={'sq': [1.18, 0.78, 1.18], 'face': {'lid': 0.3, 'mouth': 'tongueout'}}, toonDur=0.04), k(LAND4, look='camera'),   # ...and down: (review 2) squashed for six frames...
            k(r(LAND4 + 0.2), toon={'sq': [0.92, 1.1, 0.92], 'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.06, toonEase='out'), k(r(LAND4 + 0.28), toon={'sq': [1.03, 0.97, 1.03], 'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.06, toonEase='inOut'),   # ...up through a stretch...
            k(r(LAND4 + 0.36), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 1.0, 'mouth': 'tongueout'}}, toonDur=0.04), k(r(LAND4 + 0.42), toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.06)])],   # ...settled, a blink
        props=[*LAMP(lick_at=-1.0), P('bus4', 'cityBus', pos=[2.2, 0, -11.4], ry=-90, opts={'len': 7.6, 'roof': '#8E959C'}, keys=[k(0.0, to=[2.2, 0, 16.6], dur=D4, ease='linear')])],
        tethers=[TONGUE(**{'sag': 0.022, 'n': 28, 'segments': 64, 'taper': 0.2, 'lift': [[BUS4, GONE4, U_CAR, 1.15, 0.1]],
                           'birds': [[0.17, r(BUS4 + 0.04), 120], [0.23, r(BUS4 + 0.08), 100], [0.3, r(BUS4 + 0.02), 140]], 'birdScale': 1.8, 'ripple': [[GONE4, 0.18, 2.0]]})],   # (review 1) bigger pigeons
        cams=[FC(0.0, [-0.4, 4.4, 3.9], [[FAR[0], r(2.45 + UP4), 0.0], [FAR[0], 0.0, 0.0], [r(FAR[0] + 0.9), r(2.6 + UP4), 0.0], [r(FAR[0] + 0.9), 0.0, 0.0], [3.4, 2.0, 0.0]], top=0.12, bottom=0.78)])   # (review 1) from high on the pole's side: we see over the bus's roof, the hang in view; (review 2) lower, room right of him (his arm was cut), a grey roof (white like the snow)
st.cue('sfx:engine', 'S04', 0.2, 0.35); st.cue('sfx:boing', 'S04', BUS4, 0.3); st.cue('sfx:slideDown', 'S04', DROP4, 0.25); st.cue('thud', 'S04', LAND4, 0.35)

# 5: the town hall hung the Christmas lights on it. A worker in the road clips bulbs onto the tongue from the pole end toward him; the tongue sags
#    deeper at each bulb and his head bows with it; the mayor beside him ticks his clipboard
D5 = st.dur('S05'); WORK5 = [3.0, 0, -0.38]; W5END = 4.5   # (review 2) the worker in frame from the first frame, already clipping (he came in at 1 s)
A5 = r(FAR[0] - 0.1); B5 = r(POLE[0] + 0.1); U5 = lambda x: (A5 - x) / (A5 - B5); U50 = U5(WORK5[0] + 0.35); U51 = U5(W5END + 0.35); DH5 = D5 / (U50 - U51)
HANG5 = [r(-(1 - U50) * DH5), r(-(1 - U50) * DH5 + DH5)]   # the hanging front keeps up with his hands (bulb u shows from hang[0] + (hang[1] - hang[0]) (1 - u))
st.shot('S05', 'parisStreet', setOpts=DAY, look=DLOOK, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0),
            *[kk for j in range(4) for kk in (k(r(0.4 + 0.45 * j), toon={'bend': {'neck': [r(0.12 + 0.12 * j), 0, 0, 1, None], 'spine': [r(0.03 * j), 0, 0, 1, None]}, 'face': {'lid': 0.12, 'eye': 0.15, 'mouth': 'tongueout', 'gy': -0.85}}, toonDur=0.12, toonEase='out'),
                                              k(r(0.62 + 0.45 * j), toon={'bend': {'neck': [r(0.12 + 0.12 * j), 0, 0, 1, None], 'spine': [r(0.03 * j), 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'tongueout', 'gy': -0.5}}, toonDur=0.16, toonEase='inOut'))]]),   # bowing a notch at each bulb; (review 2) his eyes roll up at each notch (they stayed shut)
        act('ouv', WORK5, 90, 'stand', 'neutral', keys=[k(0.0, to=[W5END, 0, -0.38], dur=D5, ease='linear', clip='walk', then='stand', face='keep'),
            k(0.0, toon={'touch': {'R': ['torso', -0.16, 0.72, 0.4, 1, 0.05], 'L': ['torso', 0.16, 0.7, 0.4, 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'grip'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}}, toonDur=0.0)]),
        act('maire', [6.2, 0, 0.62], -95, 'stand', 'neutral', keys=[k(0.0, look=[2.0, 1.4, 0.0]), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'smirk'}}, toonDur=0.0),
            *[k(r(0.45 + 0.5 * j), toon={'touch': {'R': ['torso', 0.02, 0.62, 0.32, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.3, 'mouth': 'smirk', 'gy': 0.5}}, toonDur=0.1) for j in range(3)],
            k(r(D5 - 0.45), look='camera'), k(r(D5 - 0.4), toon={'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.1)])],   # ticking his board at each bulb, then a look to us
        props=[*LAMP(lick_at=-1.0), P('board5', 'clipboardProp', on={'actor': 'maire', 'hand': 'L'})],
        tethers=[TONGUE(**{'sag': [[0.0, 0.03], [0.55, 0.05], [1.0, 0.075], [1.45, 0.1], [1.9, 0.12]], 'n': 24, 'segments': 56, 'taper': 0.2, 'bulbs': BULBS(hang=HANG5, size=0.18, wire='#2B2B2E')})],
        cams=[FC(0.0, [1.8, 1.85, 4.3], [[FAR[0], 2.4, 0.0], [FAR[0], 0.0, 0.0], [6.2, 2.3, 0.62], [6.2, 0.0, 0.62], [2.85, 2.1, -0.38]], top=0.12, bottom=0.78)])   # (review 1) nearer and lower: him and the mayor big, the worker coming along the tongue; (review 2) bulbs 1.6 times bigger (15 px dots)
st.cue('sfx:clink', 'S05', 0.5, 0.15); st.cue('sfx:clink', 'S05', 1.0, 0.15); st.cue('sfx:clink', 'S05', 1.5, 0.15)

# 6: the mayor pressed the button. Dusk: the mayor in his sash behind a pedestal with a big red button, two neighbours behind a red ribbon; the dark
#    garland in the sky behind; he presses: CLIC
D6 = st.dur('S06'); PRESS6 = st.at('S06', 'L05', 6)                    # on « bouton »
BTN6 = [5.65, 0, 1.3]   # (review 2) at his right hand: the press clear of his own grey jacket (the forearm crossed his torso)
st.shot('S06', 'parisStreet', setOpts=DUSKSET, look=DUSK, actors=[
        act('maire', [6.2, 0, 1.0], -20, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.25, 'mouth': 'smirk'}}, toonDur=0.0),
            k(0.45, toon={'reach': {'R': [5.45, 2.5, 1.05, 1, 0.05]}, 'hands': {'R': 'point'}, 'bend': {'spine': [-0.05, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.22, toonEase='out'),   # (review 2) the finger up against the sky...
            k(0.75, toon={'reach': {'R': [5.42, 2.58, 1.05, 1, 0.05]}, 'hands': {'R': 'point'}, 'bend': {'spine': [-0.06, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.6}}, toonDur=0.2, toonEase='inOut'),   # ...held twelve frames...
            k(r(PRESS6 - 0.08), toon={'reach': {'R': [5.65, 1.02, 1.3, 1, 0.05]}, 'hands': {'R': 'point'}, 'bend': {'spine': [0.22, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'mouth': 'open', 'brow': 0.8}}, toonDur=0.08, toonEase='in'),   # ...down onto the dome: CLIC
            k(r(PRESS6 + 0.12), toon={'reach': {'R': [5.65, 1.04, 1.3, 1, 0.05]}, 'hands': {'R': 'point'}, 'bend': {'spine': [0.18, 0, 0, 1, None]}, 'face': {'lid': 0.1, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.15)]),
        act('vois1', [4.85, 0, 0.35], 20, 'stand', 'neutral', keys=[k(0.0, look=BTN6), k(0.7, look=[2.0, 2.2, -1.0]), k(1.15, look=BTN6)]), act('vois2', [7.0, 0, 0.2], -20, 'stand', 'neutral', keys=[k(0.0, look=BTN6), k(0.5, look=[6.2, 2.0, 1.0]), k(r(PRESS6 - 0.1), look=BTN6), k(PRESS6, toon={'face': {'eye': 0.4, 'mouth': 'O'}}, toonDur=0.08)])],
        props=[P('btn6', 'bigButton', pos=BTN6, ry=180, opts={'pressAt': PRESS6, 'cable': 2.5}), BURST('clic6', [5.3, 1.2, 1.5], r(PRESS6 + 0.02), 'CLIC !', 0.32, 0.3)],
        cams=[FC(0.0, [6.4, 1.6, 4.2], [[6.2, 2.45, 1.0], [5.65, 1.05, 1.3], [5.42, 2.68, 1.05], [4.85, 2.1, 0.35], [7.0, 1.7, 0.2]], top=0.18, bottom=0.76)])   # (stills 1) facing the mayor behind his button, the neighbours behind him
st.cue('sfx:click', 'S06', PRESS6, 0.4)

# 7: everything blinks; him too. Night: the garland lit and chasing on the tongue, glowing over the street; close on him: his eyes blink on the beat,
#    his face flashes red, green and gold, his hair stands up (NOËL)
D7 = st.dur('S07'); ON7 = 0.05; PER = 0.3; ALSO7 = st.at('S07', 'L06', 2)   # on « Lui »
SKINS7 = ['#FF5A5A', '#5AE070', '#FFD45A']
BEATS7 = [r(ALSO7 + PER * j) for j in range(int((D7 - ALSO7) / PER) + 1)]
st.shot('S07', 'parisStreet', setOpts=NIGHT, look=NLOOK, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'bend': {'neck': [0.48, 0, 0, 1, None]}, 'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0),
            *[k(r(ALSO7 + PER * j), toon={'bend': {'neck': [0.48, 0, 0, 1, None]}, 'hairUp': 1.0, 'skin': {'color': SKINS7[j % 3], 'k': 0.85, 'glow': 0.5, 'fill': 1.0}, 'face': {'lid': 1.0 if j % 3 == 0 else 0.0, 'mouth': 'tongueout', 'eye': 0.2}}, toonDur=0.03) for j in range(int((D7 - ALSO7) / PER) + 1)]]),   # on the beat
        ],
        props=[*LAMP(lick_at=-1.0), GLOW('g7', [r(FAR[0] - 1.6), 1.95, 0.4], '#FFD9A0', 2.2, 4.0), GLOW('key7', [r(FAR[0] - 1.2), 2.6, 1.4], '#C8D4FF', 1.4, 4.5),   # (review 1) the street lit by the garland, not darkened after the fact
               *[P(f'fl7{c}', 'glowLight', pos=[r(FAR[0] - 0.6), 2.05, 0.55], opts={'color': SKINS7[c], 'k': 3.2, 'dist': 2.6}, keys=[k(0.0, visible=False), *[k(tb, visible=(j % 3 == c)) for j, tb in enumerate(BEATS7)]]) for c in range(3)]],   # its colour on his face, the tongue and the snow
        tethers=[TONGUE(**{'radius': 0.034, 'sag': 0.05, 'n': 24, 'segments': 56, 'taper': 0.25, 'bulbs': BULBS(on=ON7, period=PER)})],
        cams=[FC(0.0, [4.0, 1.45, 1.25], [[FAR[0], 2.68, 0.0], [FAR[0], 1.2, 0.0], [4.6, 1.5, 0.0]], top=0.2, bottom=0.72)])   # (stills 1) close in front of him, the lit garland leaving his mouth across the frame; (review 1) his standing hair under the card's band
st.cue('sfx:ding', 'S07', ON7, 0.3); st.cue('sfx:static', 'S07', ALSO7, 0.3)

# 8: yesterday, the thaw. Close on the pole in the sun: the icicles drip, the frost star runs, the tip of the tongue twitches and peels off
D8 = st.dur('S08'); PEEL8 = r(D8 - 0.3)   # (review 2) ten frames after the release before the cut (four)
st.shot('S08', 'parisStreet', setOpts={**SNOW, 'sky': ['#62AEE2', '#A7D4EC'], 'snowN': 1}, look=WLOOK, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0)])],
        props=[*LAMP(melt=0.0, lick_at=-1.0)],
        tethers=[TONGUE(**{'sag': 0.05, 'n': 24, 'segments': 56, 'taper': 0.2, 'bulbs': BULBS(on=-1.0, period=PER), 'wobble': [[r(PEEL8 - 0.45), 0.025, 40, 5], [r(PEEL8 - 0.24), 0.035, 40, 5], [r(PEEL8 - 0.07), 0.04, 60, 6]], 'snap': [PEEL8, 1.0, 0.15, 1.6]})],
        cams=[FC(0.0, [r(POLE[0] + 1.1), 1.95, 1.25], [[POLE[0], 2.4, 0.0], [POLE[0], 1.55, 0.0], [r(POLE[0] + 0.9), 1.8, 0.0]], top=0.12, bottom=0.72)])   # (stills 1) tight on the contact under the dripping collar (the icicles were up under the lamp); (review 2) two twitches, a tug, then the tip peels off fast
st.cue('sfx:pop', 'S08', 0.2, 0.1); st.cue('sfx:pop', 'S08', 0.65, 0.1); st.cue('sfx:pop', 'S08', 1.05, 0.1); st.cue('sfx:squeak', 'S08', PEEL8, 0.25)

# 9: his tongue came back in one go. From the road, facing him: the tongue whips back across the street toward him like a tape measure, the bulbs
#    bunching on its end, the pigeons blown off; his cheeks balloon round it and he is knocked back (DÉGEL)
D9 = st.dur('S09'); SNAP9 = 0.0; DUR9 = 0.62; HOME9 = r(SNAP9 + DUR9)   # (review 1) from the first frame, over 0.6 s
WHAP9 = lambda a, sw: {'lay': [r(-a), 0.0], 'bend': {'spine': [-0.16, 0, 0, 1, None], 'neck': [0.36, 0, 0, 1, None]}, 'reach': {'L': [r(FAR[0] + 0.7), 2.25, 0.95, 1, 0.05], 'R': [r(FAR[0] + 0.75), 2.35, -0.9, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'},
                       'face': {'lid': 0.0, 'eye': 0.7, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'kiss', 'puff': 1.0, 'cheeks': 1.0, 'swell': sw}}   # (review 2) the head kept level (it tipped away), the arms out and back, clear of his face
st.shot('S09', 'parisStreet', setOpts={**SNOW, 'sky': ['#62AEE2', '#A7D4EC'], 'snowN': 1}, look=DLOOK, actors=[
        act('mec', FAR, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[POLE[0], LICK_Y, 0.0]), k(0.0, toon={'face': {**DEAD, 'mouth': 'tongueout'}}, toonDur=0.0),
            k(r(SNAP9 + 0.1), toon={'bend': {'spine': [0.08, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'eye': 0.6, 'pupilSize': -0.4, 'brow': 1.0, 'mouth': 'tongueout'}}, toonDur=0.05),   # it is coming...
            k(r(HOME9 - 0.22), toon={'bend': {'spine': [0.04, 0, 0, 1, None]}, 'sq': [0.97, 1.03, 0.97], 'face': {'lid': 0.75, 'brow': -0.5, 'mouth': 'tongueout'}}, toonDur=0.1, toonEase='inOut'),   # ...(review 2) a wince...
            k(r(HOME9 - 0.03), toon={'sq': [1.1, 0.9, 1.1], 'face': {'lid': 0.0, 'eye': 0.7, 'pupilSize': -0.45, 'brow': 1.0, 'mouth': 'kiss', 'puff': 0.7, 'cheeks': 0.7, 'swell': 0.8}}, toonDur=0.03, toonEase='out'),   # ...WHAP: the cheeks fill...
            k(HOME9, to=[r(FAR[0] + 0.36), 0, 0.0], dur=0.14, ease='out', face='keep'), k(HOME9, look='camera'),
            k(HOME9, toon=WHAP9(0.26, 1.4), toonDur=0.11, toonEase='out'),   # ...knocked back on a 3-4 frame arc (two before), the head swollen to its fullest, turned to us...
            *[k(r(HOME9 + 0.13 + 0.06 * j), toon=WHAP9(r(0.26 + (0.03 if j % 2 else -0.03)), 1.4), toonDur=0.05) for j in range(4)],   # ...it judders...
            k(r(HOME9 + 0.4), toon={'lay': [0.07, 0.0], 'bend': {'spine': [0.1, 0, 0, 1, None], 'neck': [0.06, 0, 0, 1, None]}, 'face': {'lid': 0.1, 'eye': 0.5, 'brow': 0.8, 'mouth': 'kiss', 'puff': 0.9, 'cheeks': 0.95, 'swell': 1.0}}, toonDur=0.13, toonEase='out'),   # ...springs up past upright, the cheeks down a notch...
            k(r(HOME9 + 0.58), toon={'face': {'lid': 0.3, 'eye': 0.2, 'mouth': 'kiss', 'puff': 0.8, 'cheeks': 0.9, 'swell': 0.9}}, toonDur=0.16, toonEase='inOut'),
            k(r(HOME9 + 0.8), toon={'face': {'lid': 1.0, 'mouth': 'kiss', 'puff': 0.8, 'cheeks': 0.9, 'swell': 0.9}}, toonDur=0.04), k(r(HOME9 + 0.86), toon={'face': {'lid': 0.35, 'mouth': 'kiss', 'puff': 0.8, 'cheeks': 0.9, 'swell': 0.9}}, toonDur=0.06)])],   # ...settles, a blink (it froze for 0.7 s)
        props=[*LAMP(melt=-2.0, lick_at=-1.0), BURST('zip9', [r(FAR[0] - 0.85), 2.62, 0.3], r(SNAP9 + 0.12), 'ZIIIP !', 0.4, 0.3),
               P('lines9', 'speedLines', pos=[r(FAR[0] - 1.1), 2.05, 0.15], face='camera', opts={'n': 7, 'len': 1.0, 'w': 0.4, 'angle': 0.0, 'soft': True, 'alpha': 0.8, 'at': [[SNAP9, HOME9]]})],
        tethers=[TONGUE(**{'sag': 0.05, 'n': 24, 'segments': 56, 'taper': 0.2, 'snap': [SNAP9, DUR9, 0.6, 1.35], 'reel': True, 'ripple': [[0.0, 0.3, 2.2], [0.2, 0.2, 2.8]], 'bulbs': BULBS(on=-1.0, period=PER), 'birds': [[0.17, 99, 60], [0.23, 99, 40], [0.3, 99, 80]], 'plug': True})],
        cams=[FC(0.0, [4.05, 2.05, 1.35], [[r(FAR[0] + 0.2), 2.9, 0.0], [r(FAR[0] + 0.2), 1.05, 0.0], [r(FAR[0] + 0.9), 2.55, 0.0], [r(FAR[0] - 0.7), 2.1, 0.0]], top=0.14, bottom=0.74)])   # (review 1) the reel moves the bulbs from the first frame: near enough for his face, room for his arms; (review 2) pushed in at three-quarters (fitBack took it 3.75 m back: 30 % of the frame)
st.cue('sfx:zip', 'S09', SNAP9, 0.4); st.cue('whoosh', 'S09', r(SNAP9 + 0.15), 0.35, 0.35, 400, 1600); st.cue('sfx:boing', 'S09', HOME9, 0.4)

# 10: with the lights. Close: the plug end slurps in like the last of a spaghetti; GULP: a lump goes down his neck; his eyes cross
D10 = st.dur('S10'); SLURP10 = 0.15; GULP10 = 0.55
st.shot('S10', 'parisStreet', setOpts={**SNOW, 'sky': ['#62AEE2', '#A7D4EC'], 'snowN': 1}, look=DLOOK, actors=[
        act('mec', [r(FAR[0] + 0.45), 0, 0.0], -90, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'scl': {'head': [1.28, 1.04, 1.08]}, 'face': {'lid': 0.3, 'mouth': 'O', 'puff': 0.8, 'cheeks': 0.9}}, toonDur=0.0),
            k(r(SLURP10 + 0.2), toon={'scl': {'head': [1.12, 1.02, 1.04]}, 'face': {'lid': 0.2, 'mouth': 'line', 'puff': 0.4, 'cheeks': 0.5}}, toonDur=0.1),
            k(GULP10, toon={'face': {'lid': 0.0, 'mouth': 'line', 'gulp': 1.0, 'cross': 1.0, 'eye': 0.3}}, toonDur=0.08, toonEase='out'),   # GULP: (review 2) the eyes cross hard, held seven frames (they did not cross)
            k(r(GULP10 + 0.3), toon={'face': {'lid': 0.0, 'mouth': 'line', 'gulp': 1.0, 'cross': 0.9, 'eye': 0.3}}, toonDur=0.05),
            k(r(GULP10 + 0.45), toon={'face': {**DEAD, 'mouth': 'line', 'gulp': 1.0}}, toonDur=0.15)])],
        props=[*LAMP(melt=-2.0, lick_at=-1.0), BURST('gulp10', [r(FAR[0] + 0.16), 1.78, -0.42], GULP10, 'GLOUPS !', 0.3, 0.3),   # (review 1) by his shoulder, off his eyes
               P('belly10', 'bellyLights', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.28, 0.15]}, opts={'at': r(GULP10 + 0.45), 'period': PER, 'size': 0.2, 'spread': 0.09, 'k': 1.2})],
        tethers=[{'a': {'actor': 'mec', 'joint': 'head', 'offset': MOUTH}, 'b': {'actor': 'mec', 'joint': 'head', 'offset': [0.12, -0.12, 0.34]}, 'color': PINK, 'radius': 0.03, 'radial': 8, 'sag': 0.0, 'n': 6, 'snap': [SLURP10, 0.22, 0.12], 'plug': True, 'tip': True}],
        cams=[FC(0.0, [r(FAR[0] - 0.9), 1.8, 0.95], [[r(FAR[0] + 0.45), 2.42, 0.0], [r(FAR[0] + 0.45), 1.15, 0.0], [r(FAR[0] + 0.2), 1.75, -0.45]], top=0.14, bottom=0.74)])   # (review 1) chest up, on him (the frame was aimed 0.45 m off him, full length)
st.cue('sfx:slideUp', 'S10', SLURP10, 0.3); st.cue('sfx:gulp', 'S10', GULP10, 0.4)

# 11: he has been blinking ever since. Night, the snowy pavement: deadpan, his belly blinks red, green and gold through his shirt, his eyes on the
#    beat; a passer-by stops and stares
D11 = st.dur('S11')
st.shot('S11', 'parisStreet', setOpts=NIGHT, look=NLOOK, actors=[
        act('mec', [r(FAR[0] + 0.45), 0, 0.0], -40, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            *[k(r(0.12 + PER * j), toon={'face': {'lid': 1.0 if j % 3 == 1 else 0.45}}, toonDur=0.03) for j in range(int(D11 / PER))]]),
        act('passante', [4.2, 0, -1.7], 60, 'stand', 'neutral', keys=[k(0.0, to=[5.0, 0, -1.25], dur=0.6, clip='walk', then='stand', ease='out', face='keep'), k(0.0, look=[r(FAR[0] + 0.45), 1.1, 0.0]),
            k(0.7, toon={'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.12)])],
        props=[P('belly11', 'bellyLights', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.3, 0.14]}, opts={'at': 0.0, 'period': PER, 'size': 0.3, 'spread': 0.1, 'k': 3.6}), GLOW('key11', [5.2, 3.2, 1.6], '#FFE3B0', 1.6, 5.0)],   # (stills 1) bigger and brighter: they were a speck on his tie; (review 1) the brightest thing, a soft lamp on the faces
        cams=[FC(0.0, [4.6, 1.6, 2.7], [[r(FAR[0] + 0.45), 2.4, 0.0], [r(FAR[0] + 0.45), 0.0, 0.0], [5.0, 2.25, -1.25], [5.0, 0.0, -1.25]], top=0.12, bottom=0.78)])   # (review 1) both in, nearer each other (cut by opposite edges)
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
