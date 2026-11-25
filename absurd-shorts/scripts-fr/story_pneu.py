#!/usr/bin/env python3
"""Le pneu (story 97, cycle 52; a medical escalation to a national epidemic, then the reversal on the hero and a dry last line).
This man took his flat tyre to the doctor. Diagnosis: flat, it is a depression. Three weeks off, no driving. Then the psychiatrist, pushing the
car: the tyre spoke of its childhood, a wheelbarrow. At a mountain spa it met an inner tube. In solidarity the three other tyres went off sick,
then every car in the country; the ambulances too, the patients push them. The minister declared the epidemic; national vaccination, one shot of
air per tyre. The vaccine is a pump, refunded at sixty-five percent; the minister patented it. The tyre came home pumped up; the inner tube moved
in. This man is flat. Sick leave refused: he has no valve.
Staging: S01 low at wheel height in the doctor's office (pale teal, no cross, no monitor): he rolls the pancake-flat tyre in with both mittens,
stooped, a small sweat drop on his head; the doctor looks up from his desk. S02: the tyre lies flat on the examination table, its big valve stem
sticking up toward us; the doctor holds the stethoscope on it, then takes its pulse at the valve, nods gravely; the hero by the door with his car
keys (the valve plant for S17). S03: the doctor tears a blank sick note off a pad and slaps it on the tyre; snap zoom down on it; ARRÊT. S04: a
side track along a cottage street: he pushes his open car, its front left wheel a bare rim scraping sparks, the flat tyre standing on the back
bench under a tartan blanket. S05: the psychiatrist's office: the tyre lies on the couch, the psychiatrist writes in an armchair; a thought bubble
pops with a one-wheeled wheelbarrow; slow push-in. S06: a steaming pool at a small mountain chalet: the tyre in a white towel and a thinner reddish
inner tube with its own valve drift together, a heart pops; far behind on a snowy road climbing the slope, the hero pushes his car, small. S07: his
house, low three-quarter: the three other tyres go flat one after the other, the car dropping and bouncing each time, a sick note slapped on each;
he watches, sweating more. S08: a low three-quarter along a motorway jam: car after car drops onto flat tyres with a dust puff, a wave rolling at
us; drivers lean out. S09: in front of a hospital street: a white van, a plain orange stripe and a blue beacon, no cross, on flat tyres; three
patients in pale gowns (one with a foot cast) push it from behind, heads turned to us; static wide. S10: the press room: a minister in a plain suit
at a podium, arms at his sides; behind him a chart whose one thick red curve climbs steeply as we watch (no figure, no word); flashes; ÉPIDÉMIE.
S11: a car park turned vaccination centre: three flat cars, three masked nurses kneeling in the gaps push giant syringes into the tyres, which pop
round one after the other; in the last ten frames only, the hero pushes his car into the right edge of the frame. S12: a pharmacy counter, frontal:
the pharmacist presents a plain foot pump on a red velvet cushion; a price tag (no figure) pops beside it, then a round sticker two thirds green.
S13: the same press room: the pump on a plinth under a glass dome; the minister cuts a ribbon before it, elbows bent; flashes. S14: his driveway:
the tyre rolls in on its own, plump and shiny, a towel round it like a scarf; the hero, drops all over him, looks up from beside his car on bare
rims. S15: the tyre side on, filling the frame: the reddish inner tube fills its hole, puffs up twice, a heart pops. S16: low as in S01, in the
driveway: the hero lies face down across his bonnet, arms dangling, a ring of big sweat drops round him; the plump tyre rolls past behind. S17: the
doctor's office, the framing of S02: the hero sits on the examination table; the doctor runs the stethoscope over him, looks behind his ear and
under his tie for a valve, taps his chest twice, shakes his head and hands him back his car keys; held.
Natural look; cycle 52: props_pneu.js (pnTyre, pnTube, pnCar, pnWave, pnVan, pnNote, pnPad, pnExam, pnSteth, pnStethNeck, pnKeys, pnCouch,
pnBubble, pnSpa, pnRamp, pnSyringe, pnPump, pnPie, pnChart, pnPlinth, pnCounter, pnMask); sweatDrop, priceTag and desk (props.js), velvetCushion
(props_centime), heartPop (props_chaussettes), blueBeacon (props_bus), footCast (props_table), armchair (props_ascenseur), plainPodium
(props_flaque), ribbonCut and bigScissors (props_baillement), flashBursts (props_moustache), parkLot (props_place) reused; hospital (no cross, no
monitor), office, cottageStreet, snow, pavillon, grassland, street, pressRoom (no flags) and whiteVoid sets.
Lessons applied from the start: one shot per line; characters about 2.3 m tall with the box head; faces above the caption band (0.77-0.83), heads
below the card band (0.07-0.18) when a card stamps; every camera checked with project() (CHECKS printed); every extra cast entry has a preset;
reach and hands carried forward key to key; a k(0.0, clip=...) key under the toon rig; no brand, logo, digit, cross or emblem (ARRÊT and ÉPIDÉMIE
only); the chart without labels; nobody hurt (patients push, nurses inject tyres)."""
from story_kit import *
import math

st = Story('pneu', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 18)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
def lerp3(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
CHECKS = []
def chk(sid, c, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(c['from'], c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
    if c.get('to'): CHECKS.append(f"{sid}(end): " + ' | '.join(f"{n} {project(c['to'], c.get('lookAt2') or c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
def fcam(at, frm, pts, top=0.08, bottom=0.76, margin=0.05, push=0.15, lenses=range(30, 61), ease='linear'):
    """a camera at frm (backed off along its bearing if needed) aimed and lensed by fit() to hold every point, pushing in `push` m over the shot"""
    f, look, lens = fitBack(frm, pts, top=top, bottom=bottom, margin=margin, lenses=lenses)
    d = [look[i] - f[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in d)); to = [r(f[i] + d[i] / n * push) for i in range(3)]
    return cam(at, f, to, look, look, lens=lens, ease=ease)
def R5(p, w=1, s=0.04): return [*p, w, s]
EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
def TK(t, reach=None, hands=None, face=None, sq=None, bend=None, d=0.12, e='inOut', keep=False, scl=None, plant=None):
    tn = {}
    if reach: tn['reach'] = reach
    if hands: tn['hands'] = hands
    if face: tn['face'] = face
    if sq: tn['sq'] = list(sq)
    if bend: tn['bend'] = bend
    if scl: tn['scl'] = scl
    if plant: tn['plant'] = plant
    return k(t, toon=tn, toonDur=d, toonEase=e, **({'keepPose': True} if keep else {}))
def blink(t, face): return [k(t, toon={'face': {**face, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face}, toonDur=0.06, keepPose=True)]
def SP(a, side=0.0): return [a, side, 0, 1, None]
def BREATHE(t0, t1, every=0.55, a=0.012): return [k(r(t0 + i * every), toon={'sq': [1 - a * 0.5, 1 + a, 1 - a * 0.5] if i % 2 == 0 else [1, 1, 1]}, toonDur=r(every * 0.9), toonEase='inOut', keepPose=True) for i in range(int((t1 - t0) / every) + 1)]
def DROP(pid, actor, offset, scale, t0=None):
    """a sweat drop on an actor's head (scale grows from shot to shot)"""
    return P(pid, 'sweatDrop', on={'actor': actor, 'joint': 'head', 'offset': offset}, scale=scale, **({'keys': [k(0.0, visible=False), k(t0, visible=True)]} if t0 else {}))

# faces
CALM = {'lid': 0.3, 'mouth': 'line', 'brow': 0.0}
TIRED = {'lid': 0.55, 'mouth': 'line', 'brow': 0.35}
WORRY = {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}
GRAVE = {'lid': 0.4, 'mouth': 'line', 'brow': -0.4}
STRAIN = {'lid': 0.45, 'mouth': 'clench', 'brow': 0.5}
SMUG = {'lid': 0.35, 'mouth': 'smile', 'brow': 0.2}

for g_ in [('S01', 1.2, 'mec', 'roll'), ('S02', 1.4, 'docteur', 'pulse'), ('S03', 1.0, 'docteur', 'slap'), ('S04', 1.2, 'mec', 'push'),
           ('S05', 1.9, 'psy', 'bubble'), ('S06', 1.9, 'mec', 'heart'), ('S07', 0.6, 'mec', 'pop'), ('S08', 0.9, 'mec', 'wave'),
           ('S09', 1.2, 'malade1', 'push'), ('S10', 1.6, 'ministre', 'chart'), ('S11', 0.8, 'inf1', 'shot'), ('S12', 2.4, 'pharma', 'pie'),
           ('S13', 1.0, 'ministre', 'ribbon'), ('S14', 1.3, 'mec', 'roll'), ('S15', 1.25, 'mec', 'heart'), ('S16', 0.8, 'mec', 'flat'),
           ('S17', 2.6, 'docteur', 'keys')]:
    st.gag(*g_)

# ================================================================= the doctor's office (S01, S02, S03, S17)
HOSP = {'cross': False, 'monitor': False}
TBL = [0.0, 0, -1.0]; TOP = 0.845                    # the examination table, long along X, its top at 0.845
TY2 = [0.12, TOP, -0.95]; TYRY = 180                # the tyre lying flat on it, the valve toward us
VALVE = add(TY2, [-0.1, 0.29, 0.21])                # the valve's red cap (see pnTyre: lying, flat, turned 180, valveS 2.2)
VALVEB = add(TY2, [-0.1, 0.075, 0.14])
DOC2 = [0.55, 0, -1.62]; DRY2 = -10
DESK = [1.05, 0, -2.55]
LOOKH = {'sunDir': [0.4, 0.9, 0.75]}
def TYRE_TABLE(sid, **o): return P(f'pneu{sid}', 'pnTyre', pos=TY2, ry=TYRY, opts={'lie': True, 'flat': 1, 'valveS': 2.2, **o})
def OFFICE(sid): return [P(f'table{sid}', 'pnExam', pos=TBL, opts={'head': False}), P(f'bureau{sid}', 'desk', pos=DESK, ry=0, opts={'w': 1.5})]

# ================================================================= S01
# 1: the hook. Low at wheel height: he rolls the pancake-flat tyre in with both mittens, stooped, a small drop on his head; the doctor looks up
D1 = st.dur('S01')
DIR1 = fwd(-60); H0 = [1.7, 0, -0.1]; H1 = [r(H0[0] + DIR1[0] * 1.0), 0, r(H0[2] + DIR1[2] * 1.0)]
T0 = off(H0, -60, 0.65); T1 = off(H1, -60, 0.65)
DOC1 = [1.05, 0, -3.15]; DRY1 = -5
C1 = cam(0.0, [0.3, 0.55, 4.6], [0.25, 0.55, 4.35], [0.9, 0.85, -0.6], [0.88, 0.85, -0.6], lens=50)   # low; the tyre above the captions   # low, at wheel height
chk('S01', C1, {'heroTop0': add(H0, [0, 2.3, 0]), 'tyreTop1': add(T1, [0, 0.55, 0]), 'tyreBot1': T1, 'heroFace0': add(H0, [0, 1.95, 0]), 'heroFace1': add(H1, [0, 1.95, 0]), 'tyre0': add(T0, [0, 0.25, 0]), 'tyre1': add(T1, [0, 0.25, 0]), 'docFace': add(DOC1, [0, 2.0, 0])})
def tyre_hands(T, ry, h=0.58):
    return {'L': R5(add(off(T, ry, -0.12, -0.16), [0, h, 0])), 'R': R5(add(off(T, ry, -0.12, 0.16), [0, h, 0]))}
STOOP = {'spine': SP(1.0, 0.0), 'neck': SP(-0.95, 0.0)}
k1 = [k(0.0, clip='walk'), k(0.0, to=H1, dur=D1, clip='walk', ease='linear', face='keep'), k(0.0, look='camera')]
for i in range(8):
    t = r(D1 * i / 7); T = lerp3(T0, T1, i / 7)
    k1.append(TK(t, tyre_hands(add(T, [DIR1[0] * 0.06 * (i % 2), 0, DIR1[2] * 0.06 * (i % 2)]), -60, 0.56 + 0.04 * (i % 2)), {'L': 'open', 'R': 'open'}, {**STRAIN, 'lid': 0.7 if i % 2 else 0.4, 'brow': 0.7},
                 (1.05, 0.94, 1.05) if i % 2 else (0.98, 1.03, 0.98), bend={'spine': SP(1.1 if i % 2 else 0.95), 'neck': SP(-1.0 if i % 2 else -0.9)}, d=r(D1 / 7), keep=i > 0))   # (pass 3) a shove per step on the tread
k1 += blink(1.5, STRAIN)
kd1 = [k(0.0, clip='stand'), k(0.0, look=add(DESK, [0.0, 0.8, 0.1])), TK(0.0, {'L': R5(add(DESK, [0.3, 0.8, -0.1])), 'R': R5(add(DESK, [-0.3, 0.8, -0.1]))}, {'L': 'open', 'R': 'open'}, CALM, bend={'spine': SP(0.25), 'neck': SP(0.3)}, d=0.0),
       TK(0.55, face={**CALM, 'gy': -0.8, 'gx': 0.4, 'brow': 0.3}, d=0.06, keep=True),   # eyes up first
       k(0.85, look=add(H1, [0, 1.6, 0]), lookDur=0.18), TK(0.85, face={'lid': 0.05, 'mouth': 'line', 'brow': 0.5}, bend={'spine': SP(0.05), 'neck': SP(0.0)}, d=0.15, keep=True), *blink(1.6, CALM)]
st.shot('S01', 'hospital', setOpts=HOSP, look=LOOKH, actors=[act('mec', H0, -60, 'walk', 'neutral', keys=k1), act('docteur', DOC1, DRY1, 'stand', 'neutral', keys=kd1)],
        props=[*OFFICE('S01'), P('pneuS01', 'pnTyre', pos=T0, ry=30, opts={'flat': 0.75, 'roll': [[0, 0], [D1, -1.0]]}, keys=[k(0.0, to=T1, dur=D1, ease='linear')]), DROP('gouttS01', 'mec', [0.22, 0.36, 0.0], 0.8)], cams=[C1])
st.cue('sfx:squeak', 'S01', 0.3, 0.15); st.cue('sfx:squeak', 'S01', 1.1, 0.15)

# ================================================================= S02
# 2: the tyre flat on the table, its valve sticking up toward us; the doctor's stethoscope on it, then two fingers on the valve (the pulse), a grave
#    nod; the hero by the door holding his car keys
D2 = st.dur('S02')
HER2 = [0.85, 0, 0.4]; HRY2 = -38
C2 = cam(0.0, [-0.85, 1.8, 3.9], [-0.8, 1.79, 3.8], [0.5, 1.22, -0.6], [0.5, 1.22, -0.6], lens=48)
C2b = glide([cam(0.8, [-0.35, 1.72, 2.25], [-0.33, 1.71, 2.15], [0.22, 1.24, -1.0], [0.22, 1.24, -1.0], lens=44)], 0.35)   # a push in (no cut) on the valve and his fingers, his face above
chk('S02b', C2b, {'valve': VALVE, 'docFace': add(DOC2, [0, 2.0, 0]), 'docTop': add(DOC2, [0, 2.3, 0]), 'tyreL': add(TY2, [-0.42, 0.05, 0]), 'tyreR': add(TY2, [0.42, 0.05, 0])})
chk('S02', C2, {'docFace': add(DOC2, [0, 2.0, 0]), 'docTop': add(DOC2, [0, 2.3, 0]), 'heroFace': add(HER2, [0, 1.95, 0]), 'heroTop': add(HER2, [0, 2.3, 0]), 'valve': VALVE, 'tyreFront': add(TY2, [0, 0.05, 0.42]), 'heroFeet': HER2})
STETH = add(TY2, [-0.2, 0.11, -0.08])
kd2 = [k(0.0, clip='stand'), k(0.0, look=STETH), TK(0.0, {'R': R5(add(STETH, [0.05, 0.3, 0.12])), 'L': R5(off(DOC2, DRY2, 0.25, -0.25, 1.05))}, {'R': 'grip', 'L': 'rest'}, GRAVE, bend={'spine': SP(0.3), 'neck': SP(0.2)}, d=0.0),
       TK(0.25, {'R': R5(add(STETH, [0.02, 0.04, 0.02]))}, {'R': 'grip'}, {**GRAVE, 'lid': 0.15}, (1.03, 0.97, 1.03), bend={'spine': SP(0.4), 'neck': SP(0.3)}, d=0.12, keep=True),
       TK(0.5, {'R': R5(add(STETH, [0.12, 0.04, 0.06]))}, {'R': 'grip'}, GRAVE, (1, 1, 1), d=0.2, keep=True),
       TK(0.85, {'L': R5(add(VALVE, [0.03, 0.04, -0.03]))}, {'L': 'pinch'}, {**GRAVE, 'gy': -0.3}, d=0.22, keep=True), k(0.85, look=VALVE, lookDur=0.15),
       TK(1.25, {'R': R5(off(DOC2, DRY2, 0.25, 0.22, 1.05))}, {'R': 'rest'}, {**GRAVE, 'lid': 0.5}, d=0.25, keep=True),
       TK(1.72, bend={'spine': SP(0.35), 'neck': SP(0.6)}, d=0.1, keep=True), TK(1.92, bend={'spine': SP(0.35), 'neck': SP(0.1)}, d=0.1, keep=True),   # nod one, held
       TK(2.08, bend={'spine': SP(0.4), 'neck': SP(0.7)}, d=0.1, keep=True), TK(2.36, bend={'spine': SP(0.3), 'neck': SP(0.1)}, d=0.12, keep=True),   # nod two, deeper, held
       k(2.42, look=add(HER2, [0, 1.9, 0]), lookDur=0.15), *blink(0.6, GRAVE)]
kh2 = [k(0.0, clip='stand'), k(0.0, look=TY2), TK(0.0, {'R': R5(off(HER2, HRY2, 0.32, 0.12, 1.25)), 'L': R5(off(HER2, HRY2, 0.1, -0.3, 0.95))}, {'R': 'grip', 'L': 'rest'}, WORRY, d=0.0),
       k(1.0, look='camera', lookDur=0.2), TK(1.0, face={**WORRY, 'brow': 0.8}, d=0.1, keep=True), k(2.0, look=TY2, lookDur=0.2), *blink(1.5, WORRY), *BREATHE(0.2, D2)]
st.shot('S02', 'hospital', setOpts=HOSP, look=LOOKH, actors=[act('docteur', DOC2, DRY2, 'stand', 'neutral', keys=kd2), act('mec', HER2, HRY2, 'stand', 'neutral', keys=kh2)],
        props=[*OFFICE('S02'), TYRE_TABLE('S02', breathe=0.25), P('steth2', 'pnSteth', on={'actor': 'docteur', 'hand': 'R', 'offset': [0, -0.08, 0.04]}, opts={'s': 1.9}),
               P('stcou2', 'pnStethNeck', on={'actor': 'docteur', 'joint': 'neck'}), P('cles2', 'pnKeys', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.08, 0.03]}),
               DROP('gouttS02', 'mec', [0.22, 0.36, 0.0], 0.9)], cams=[C2, C2b, glide([cam(1.55, [-0.85, 1.8, 3.9], [-0.82, 1.8, 3.85], [0.5, 1.22, -0.6], [0.5, 1.22, -0.6], lens=48)], 0.25)])   # back out: the hero in frame for the nod
st.cue('sfx:tick', 'S02', 1.0, 0.2); st.cue('sfx:tick', 'S02', 1.3, 0.2)

# ================================================================= S03
# 3: the doctor tears a blank sick note off the pad and slaps it on the tyre; snap zoom down on the note; ARRÊT
D3 = st.dur('S03'); TEAR3, SLAP3, SNAP3 = 0.35, 0.92, 1.05
HER3 = [0.42, 0, -1.95]; HRY3 = -15
PAD = [-0.62, TOP, -0.85]; DOC3 = [-0.25, 0, -1.65]; DRY3 = 5
NOTE3 = add(TY2, [0.0, 0.1, 0.12]); NRX = r(-PI / 2 + 0.5, 4)
C3 = cam(0.0, [-0.55, 1.75, 2.6], [-0.5, 1.72, 2.45], [-0.1, 1.42, -0.95], [-0.1, 1.42, -0.95], lens=44)   # the doctor's head under the card band when ARRÊT stamps
def zc(d): return add(NOTE3, [0.0, r(d * 0.78), r(d * 0.78)])
C3b = glide([cam(SNAP3, zc(1.45), zc(1.45), add(NOTE3, [0, 0.0, -0.03]), add(NOTE3, [0, 0.0, -0.03]), lens=42)], 0.08)   # the snap: past the mark
C3c = glide([cam(r(SNAP3 + 0.1), zc(2.05), zc(1.95), add(NOTE3, [0, 0.0, -0.03]), add(NOTE3, [0, 0.0, -0.03]), lens=42, shake=0.004)], 0.22)   # back out: the black ring reads round the note
chk('S03', C3, {'docFace': add(DOC3, [0, 2.0, 0]), 'docTop': add(DOC3, [0, 2.32, 0]), 'heroTop': add(HER3, [0, 2.32, 0]), 'heroFace': add(HER3, [0, 1.95, 0]), 'pad': PAD, 'note': NOTE3, 'tyre': TY2})
chk('S03c', C3c, {'note': NOTE3, 'ringL': add(TY2, [-0.45, 0.05, 0]), 'ringR': add(TY2, [0.45, 0.05, 0]), 'ringF': add(TY2, [0, 0.05, 0.45])})
chk('S03b', C3b, {'note': NOTE3, 'noteTop': add(NOTE3, [0, 0.06, -0.12]), 'noteBot': add(NOTE3, [0, -0.06, 0.12])})
kd3 = [k(0.0, clip='stand'), k(0.0, look=PAD), TK(0.0, {'R': R5(add(PAD, [0.02, 0.08, 0.1])), 'L': R5(off(DOC3, DRY3, 0.25, -0.25, 1.05))}, {'R': 'grip', 'L': 'rest'}, GRAVE, bend={'spine': SP(0.4), 'neck': SP(0.3)}, d=0.0),
       TK(TEAR3, {'R': R5(add(PAD, [0.1, 0.32, 0.15]))}, {'R': 'grip'}, {**GRAVE, 'brow': -0.6}, d=0.12, keep=True),
       k(0.6, look=NOTE3, lookDur=0.15), TK(0.62, {'R': R5(add(NOTE3, [0.05, 0.35, -0.1]))}, {'R': 'grip'}, GRAVE, d=0.2, keep=True),
       TK(SLAP3, {'R': R5(add(NOTE3, [0.0, 0.05, -0.02]))}, {'R': 'open'}, {**GRAVE, 'lid': 0.1}, (1.03, 0.97, 1.03), d=0.07, keep=True),
       TK(1.05, {'R': R5(add(NOTE3, [0.15, 0.45, -0.3]))}, {'R': 'rest'}, GRAVE, (1, 1, 1), d=0.18, keep=True), k(1.3, look='camera', lookDur=0.2)]
SQH = {'lid': 1.0, 'mouth': 'clench', 'brow': 0.9}
kh3 = [k(0.0, clip='stand'), k(0.0, look=NOTE3), TK(0.0, {'R': R5(off(HER3, HRY3, 0.32, 0.12, 1.25)), 'L': R5(off(HER3, HRY3, 0.1, -0.3, 0.95))}, {'R': 'grip', 'L': 'rest'}, WORRY, d=0.0),
       TK(r(SLAP3 - 0.06), face={**WORRY, 'brow': 0.9}, sq=(0.97, 1.05, 0.97), d=0.06, keep=True),
       TK(SLAP3, face=SQH, sq=(1.12, 0.88, 1.12), scl={'head': [1.65, 0.42, 1.4]}, d=0.04, e='out', keep=True),
       TK(r(SLAP3 + 0.12), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.9, 'pop': 0.8}, sq=(0.93, 1.08, 0.93), scl={'head': [0.85, 1.25, 0.9]}, d=0.08, keep=True),
       TK(r(SLAP3 + 0.26), face={**WORRY, 'pop': 0.0}, sq=(1, 1, 1), scl={'head': [1.0, 1.0, 1.0]}, d=0.14, keep=True), k(1.4, look='camera', lookDur=0.2), *blink(1.8, WORRY)]
st.shot('S03', 'hospital', setOpts=HOSP, look=LOOKH, actors=[act('docteur', DOC3, DRY3, 'stand', 'neutral', keys=kd3), act('mec', HER3, HRY3, 'stand', 'neutral', keys=kh3)],
        props=[*OFFICE('S03'), TYRE_TABLE('S03'), P('bloc3', 'pnPad', pos=PAD, ry=10, opts={'tearAt': TEAR3}),
               P('notemain3', 'pnNote', on={'actor': 'docteur', 'hand': 'R', 'offset': [0, -0.1, 0.06], 'rot': [0.3, 0, 0]}, opts={'from': TEAR3, 'until': SLAP3}),
               P('note3', 'pnNote', pos=NOTE3, rot=[NRX, 0, 0], opts={'slapAt': SLAP3}), P('stcou3', 'pnStethNeck', on={'actor': 'docteur', 'joint': 'neck'}), DROP('goutt3', 'mec', [0.22, 0.36, 0.0], 0.9)], cams=[C3, C3b, C3c])
st.card('S03', 'ARRÊT', at=st.at('S03', 'L03', 2))
st.cue('sfx:paper', 'S03', TEAR3, 0.4); st.cue('clack', 'S03', SLAP3, 0.45); st.cue('whoosh', 'S03', r(SNAP3 - 0.05), 0.25, 0.12, 500, 2500)

# ================================================================= S04
# 4: a side track along a cottage street: he pushes his open car, the front left wheel a bare rim scraping sparks, the flat tyre standing on the
#    back bench under a tartan blanket; two drops on his head
D4 = st.dur('S04'); ZC4 = 1.6; X40, X41 = -0.6, 1.9
CAR4_0, CAR4_1 = [X40, 0, ZC4], [X41, 0, ZC4]
def hero_behind(car, z=0.0): return [r(car[0] - 2.5), 0, r(car[2] + z)]   # far enough back to lean into it
HB0, HB1 = hero_behind(CAR4_0, 0.15), hero_behind(CAR4_1, 0.15)
def rear_hands(car, y=0.86):
    return {'L': R5([r(car[0] - 1.82), y, r(car[2] - 0.2)]), 'R': R5([r(car[0] - 1.82), y, r(car[2] + 0.5)])}   # (pass 3) facing +X his right is +Z: the hands no longer cross
C4 = cam(0.0, [r(X40 + 3.2), 2.3, r(ZC4 + 3.6)], [r(X41 + 3.2), 2.3, r(ZC4 + 3.6)], [r(X40 - 1.2), 0.32, ZC4], [r(X41 - 1.2), 0.32, ZC4], lens=50)   # above the open car: his body over it
chk('S04', C4, {'heroFace': add(HB0, [0, 1.95, 0]), 'heroTop': add(HB0, [0, 2.3, 0]), 'carFront': add(CAR4_0, [1.75, 0.6, 0.8]), 'cargo': add(CAR4_0, [-0.75, 1.6, 0]), 'rim': add(CAR4_0, [1.15, 0.2, 0.8])})
PUSH = {'spine': SP(0.62), 'neck': SP(-0.55, 0.35)}
k4 = [k(0.0, clip='pushCartWalk'), k(0.0, to=HB1, dur=D4, clip='pushCartWalk', ease='linear', face='keep'), k(0.0, look='camera')]
for i in range(9):   # straining shoves: the body dips and the cheeks puff on each one
    t = r(D4 * i / 8); c = lerp3(CAR4_0, CAR4_1, i / 8)
    k4.append(TK(t, rear_hands(c, 0.86), {'L': 'open', 'R': 'open'}, {**STRAIN, 'lid': 0.7 if i % 2 else 0.4, 'brow': 0.7}, (1.06, 0.93, 1.06) if i % 2 else (0.97, 1.04, 0.97), {'spine': SP(0.72 if i % 2 else 0.58), 'neck': SP(-0.62 if i % 2 else -0.5, 0.35)}, d=r(D4 / 8), keep=i > 0))
k4 += blink(1.3, STRAIN)
st.shot('S04', 'cottageStreet', look={'sunDir': [0.5, 0.9, 0.6]}, actors=[act('mec', HB0, 90, 'pushCartWalk', 'neutral', keys=k4)],
        props=[P('voit4', 'pnCar', pos=CAR4_0, opts={'open': True, 'color': '#6CC4A4', 'cargo': {'flat': 0.55, 'blanket': True}, 'wheels': [2, 0, 0, 0], 'roll': [[0, 0], [D4, X41 - X40]], 'sparks': [[0, D4]]},
                 keys=[k(0.0, to=CAR4_1, dur=D4, ease='linear')]),
               DROP('goutt4a', 'mec', [0.22, 0.36, 0.0], 1.1), DROP('goutt4b', 'mec', [-0.22, 0.3, 0.02], 0.9)], cams=[C4])
st.cue('sfx:scratch', 'S04', 0.0, 0.3)

# ================================================================= S05
# 5: the psychiatrist's office: the tyre lies on the couch; the psychiatrist writes in an armchair; a thought bubble pops with a one-wheeled
#    wheelbarrow; slow push-in
D5 = st.dur('S05'); POP5 = r(st.at('S05', 'L05', 7) - 0.05)
COUCH = [0.05, 0, -1.75]; TY5 = [-0.35, 0.45, -1.72]   # propped against the curled head end, reclining
ARM = [0.82, 0, -0.62]; ARY = -65
BUB = [-0.05, 1.85, -1.5]
C5 = cam(0.0, [0.5, 1.5, 3.3], [0.45, 1.5, 2.75], [0.32, 1.3, -1.3], [0.32, 1.33, -1.3], lens=44)
chk('S05', C5, {'psyFace': add(ARM, [0, 1.55, 0]), 'tyre': add(TY5, [0, 0.35, 0]), 'bubTop': add(BUB, [0, 0.62, 0]), 'bubL': add(BUB, [-0.68, 0, 0]), 'bubR': add(BUB, [0.68, 0, 0]), 'couchL': add(COUCH, [-0.95, 0.6, 0])})
kp5 = [k(0.0, clip='sit'), k(0.0, look=TY5), TK(0.0, {'L': R5(off(ARM, ARY, 0.45, -0.1, 0.95)), 'R': R5(off(ARM, ARY, 0.45, 0.12, 1.0))}, {'L': 'grip', 'R': 'grip'}, {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}, bend={'neck': SP(0.25)}, d=0.0),
       *[TK(r(0.2 + 0.18 * i), {'R': R5(off(ARM, ARY, 0.45, 0.08 + 0.05 * (i % 2), 1.0 + 0.01 * (i % 3)))}, {'R': 'grip'}, d=0.15, keep=True) for i in range(6)],
       k(1.5, look=add(BUB, [0, 0.1, 0]), lookDur=0.25), TK(1.5, face={'lid': 0.1, 'mouth': 'line', 'brow': 0.6}, d=0.15, keep=True),
       k(2.3, look='camera', lookDur=0.2), *blink(1.1, CALM)]
st.shot('S05', 'office', setOpts={'door': False, 'printer': False, 'carpet': False}, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[act('psy', ARM, ARY, 'sit', 'neutral', keys=kp5)],
        props=[P('divan5', 'pnCouch', pos=COUCH), P('pneu5', 'pnTyre', pos=TY5, ry=0, rot=[0, 0, 0.45], opts={'flat': 0.8, 'breathe': 0.3, 'blanket': True}), P('fauteuil5', 'armchair', pos=ARM, ry=ARY, opts={'color': '#6A7F5A'}),
               P('bloc5', 'clipboardProp', on={'actor': 'psy', 'hand': 'L', 'offset': [0.02, -0.08, 0.06], 'rot': [1.2, 0, 0]}),
               P('bulle5', 'pnBubble', pos=BUB, ry=yaw(BUB, C5['from']), opts={'w': 1.36, 'popAt': POP5})], cams=[C5])
st.cue('sfx:pop', 'S05', POP5, 0.4); st.cue('sfx:paper', 'S05', 0.2, 0.2)

# ================================================================= S06
# 6: the steaming pool at the mountain chalet: the tyre in its towel and the reddish inner tube drift together, a heart pops; far behind, on the
#    snowy road climbing the slope, the hero pushes his car, small
D6 = st.dur('S06'); HEART6 = r(st.at('S06', 'L06', 9) + 0.1)
SPA = [-0.9, 0, 1.2]
TY6_0, TY6_1 = add(SPA, [-0.78, 0.16, 0.25]), add(SPA, [-0.3, 0.16, 0.3])
TU6_0, TU6_1 = add(SPA, [0.85, 0.32, 0.3]), add(SPA, [0.2, 0.32, 0.32])
RAMPF = [10.0, 0, -15.0]; RL, RH = 18.0, 4.0; SLOPE = math.atan2(RH, RL)
def ramp_y(x): return r((RAMPF[0] - x) / RL * RH + 0.05)
CX6_0, CX6_1 = 0.0, -0.65
CAR6_0, CAR6_1 = [CX6_0, ramp_y(CX6_0), RAMPF[2]], [CX6_1, ramp_y(CX6_1), RAMPF[2]]
HX6_0, HX6_1 = CX6_0 + 2.3, CX6_1 + 2.3
HER6_0, HER6_1 = [HX6_0, ramp_y(HX6_0), RAMPF[2] + 0.1], [HX6_1, ramp_y(HX6_1), RAMPF[2] + 0.1]
C6 = cam(0.0, [-0.6, 1.65, 6.0], [-0.72, 1.62, 5.6], [-0.75, 0.6, -1.0], [-0.8, 0.6, -1.0], lens=42)
chk('S06', C6, {'tyre': add(TY6_1, [0, 0.4, 0]), 'tube': TU6_1, 'heart': add(SPA, [0.0, 1.15, 0.4]), 'heroFar': add(HER6_0, [0, 2.0, 0]), 'carFar': add(CAR6_0, [0, 0.8, 0])})
k6 = [k(0.0, clip='pushCartWalk'), k(0.0, to=HER6_1, dur=D6, clip='pushCartWalk', ease='linear', face='keep'), k(0.0, look='camera'),
      TK(0.0, {'L': R5([r(CX6_0 + 1.82), ramp_y(CX6_0 + 1.82) + 0.86, RAMPF[2] + 0.4]), 'R': R5([r(CX6_0 + 1.82), ramp_y(CX6_0 + 1.82) + 0.86, RAMPF[2] - 0.4])}, {'L': 'open', 'R': 'open'}, STRAIN, bend=PUSH, d=0.0),
      TK(D6, {'L': R5([r(CX6_1 + 1.82), ramp_y(CX6_1 + 1.82) + 0.86, RAMPF[2] + 0.4]), 'R': R5([r(CX6_1 + 1.82), ramp_y(CX6_1 + 1.82) + 0.86, RAMPF[2] - 0.4])}, {'L': 'open', 'R': 'open'}, STRAIN, bend=PUSH, d=D6, e='linear', keep=True)]
st.shot('S06', 'snow', look={'sunDir': [0.5, 0.9, 0.7]}, actors=[act('mec', HER6_0, -90, 'pushCartWalk', 'neutral', keys=k6)],
        props=[P('spa6', 'pnSpa', pos=SPA, opts={'r': 1.75, 'chaletX': -1.9, 'pines': [[-3.4, -2.6, 1.1]], 'ringAt': [0, 0.3]}),
               P('rampe6', 'pnRamp', pos=RAMPF, opts={'len': RL, 'rise': RH}),
               P('pneu6', 'pnTyre', pos=TY6_0, ry=12, opts={'towel': 'drape', 'sink': 0.22, 'bob': [0.02, 0.6]}, keys=[k(0.0, to=TY6_1, dur=1.8, ease='out')]),
               P('chambre6', 'pnTube', pos=TU6_0, ry=-15, opts={'bob': [0.02, 0.55]}, keys=[k(0.0, to=TU6_1, dur=1.8, ease='out')]),
               P('coeur6', 'heartPop', pos=add(SPA, [0.0, 1.1, 0.42]), opts={'at': HEART6, 'size': 0.28}),
               P('voit6', 'pnCar', pos=CAR6_0, ry=180, rotOrder='YXZ', rot=[0, 0, r(SLOPE, 4)], opts={'open': True, 'cargo': None, 'wheels': [0, 0, 2, 0], 'roll': [[0, 0], [D6, 0.7]]}, keys=[k(0.0, to=CAR6_1, dur=D6, ease='linear')])],
        cams=[C6])
st.cue('sfx:pop', 'S06', HEART6, 0.35)

# ================================================================= S07
# 7: his house, low three-quarter: the three other tyres go flat one after the other (pop, pop, pop), the car dropping and bouncing; a sick note
#    slapped on each; he watches, sweating
D7 = st.dur('S07'); P71, P72, P73 = 0.45, 1.25, 2.05          # three hard drops on even beats
CAR7 = [0.4, 0, -1.3]; CRY7 = -45; PAV = {'fence': False, 'mailbox': False}   # nose turned toward us: the car short in the narrow frame
def wpos(car, i, ry=0):   # a car wheel's outer centre (world), car facing +X turned ry: 0 FL (+Z), 1 FR, 2 RL, 3 RR
    lx, lz = [(1.15, 0.74), (1.15, -0.74), (-1.15, 0.74), (-1.15, -0.74)][i]
    a = math.radians(ry); return [r(car[0] + lx * math.cos(a) + lz * math.sin(a)), 0.3, r(car[2] - lx * math.sin(a) + lz * math.cos(a))]
def wout(car, i, ry, d):   # d metres outward from a wheel's side wall (local +-Z), at its hub height
    lx, lz = [(1.15, 0.74), (1.15, -0.74), (-1.15, 0.74), (-1.15, -0.74)][i]; lz += d if lz > 0 else -d
    a = math.radians(ry); return [r(car[0] + lx * math.cos(a) + lz * math.sin(a)), 0.36, r(car[2] - lx * math.sin(a) + lz * math.cos(a))]
W_RL, W_FR, W_RR = wpos(CAR7, 2, CRY7), wpos(CAR7, 1, CRY7), wpos(CAR7, 3, CRY7)
HER7 = [-0.85, 0, 0.55]; HRY7 = 25                                 # beside the car's left side, by the front door
C7F = [2.9, 0.75, 3.6]
NOTE_RL, NOTE_FR = wout(CAR7, 2, CRY7, 0.16), add(wpos(CAR7, 1, CRY7), [0.32, 0.06, 0.32])
C7 = fcam(0.0, [2.1, 0.5, 3.9], {'heroTop': add(HER7, [0, 2.32, 0]), 'heroFeet': HER7, 'heroL': add(HER7, [-0.9, 1.0, 0.4]), 'noteRL': add(NOTE_RL, [0, -0.3, 0]), 'wFL': add(wpos(CAR7, 0, CRY7), [0, -0.3, 0]), 'wRR': add(W_RR, [0, -0.3, 0]), 'roof': add(CAR7, [0, 1.5, 0])}, top=0.1, bottom=0.84, push=0.25)   # at wheel height   # at wheel height: the drops read on the tyres
chk('S07', C7, {'heroFace': add(HER7, [0, 1.95, 0]), 'noteRL': NOTE_RL, 'noteFR': NOTE_FR, 'wFL': wpos(CAR7, 0, CRY7), 'wRR': W_RR})
FLINCH = {'lid': 0.0, 'mouth': 'O', 'brow': 0.9, 'pop': 0.7}
k7 = [k(0.0, clip='stand'), k(0.0, look=add(CAR7, [0, 0.4, 0.6])), TK(0.0, {'L': R5(off(HER7, HRY7, 0.15, -0.3, 0.95)), 'R': R5(off(HER7, HRY7, 0.15, 0.3, 0.95))}, {'L': 'rest', 'R': 'rest'}, WORRY, d=0.0),
      TK(0.15, face={**WORRY, 'brow': 0.8}, bend={'spine': SP(0.1), 'neck': SP(0.25)}, d=0.2, keep=True)]
# (pass 3) the takes escalate: a small blink and flinch, then a big take with the eyes out, then the jaw drops and he flattens and reinflates
k7 += [k(r(P71 - 0.1), look=W_RL, lookDur=0.08), TK(P71, face={'lid': 1.0, 'mouth': 'line', 'brow': 0.6}, sq=(1.04, 0.96, 1.04), d=0.04, keep=True),
       TK(r(P71 + 0.1), face={**WORRY, 'brow': 0.8}, sq=(1, 1, 1), d=0.1, keep=True)]
k7 += [k(r(P72 - 0.1), look=W_FR, lookDur=0.06), TK(r(P72 - 0.05), sq=(1.06, 0.93, 1.06), d=0.05, keep=True),
       TK(P72, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 1.0}, sq=(0.86, 1.16, 0.86), scl={'head': [0.9, 1.15, 0.95]}, d=0.04, e='out', keep=True),
       TK(r(P72 + 0.14), sq=(1.03, 0.97, 1.03), scl={'head': [1, 1, 1]}, d=0.08, keep=True), TK(r(P72 + 0.4), face={**WORRY, 'pop': 0.0, 'brow': 0.9}, sq=(1, 1, 1), d=0.15, keep=True)]
k7 += [k(r(P73 - 0.1), look=W_RR, lookDur=0.06),
       TK(P73, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 1.0, 'jaw': 1.0}, sq=(1.3, 0.6, 1.3), scl={'head': [1.35, 0.6, 1.25]}, d=0.04, e='out', keep=True),
       TK(r(P73 + 0.1), sq=(1.3, 0.6, 1.3), d=0.06, keep=True),
       TK(r(P73 + 0.2), sq=(0.85, 1.18, 0.85), scl={'head': [0.88, 1.16, 0.92]}, d=0.07, keep=True),
       TK(r(P73 + 0.32), face={'lid': 0.1, 'mouth': 'O', 'brow': 0.9, 'pop': 0.5, 'jaw': 0.7}, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.12, keep=True)]
k7 += [k(2.6, look='camera', lookDur=0.2), TK(2.65, face={**TIRED, 'jaw': 0.5, 'pop': 0.0}, d=0.2, keep=True), *blink(2.9, TIRED), *BREATHE(0.0, D7, 0.5, 0.015)]
def drop(t): return [[t, 0], [r(t + 0.06), 1]]
st.shot('S07', 'pavillon', setOpts=PAV, look={'sunDir': [0.6, 0.9, 0.7]}, actors=[act('mec', HER7, HRY7, 'stand', 'neutral', keys=k7)],
        props=[P('voit7', 'pnCar', pos=CAR7, ry=CRY7, opts={'open': True, 'wheels': [2, drop(P72), drop(P71), drop(P73)], 'dust': True}),
               P('note7a', 'pnNote', pos=NOTE_RL, ry=yaw(NOTE_RL, C7['from']), opts={'slapAt': r(P71 + 0.22), 'w': 0.4, 'h': 0.52}),
               P('note7b', 'pnNote', pos=NOTE_FR, ry=yaw(NOTE_FR, C7['from']), opts={'slapAt': r(P72 + 0.22), 'w': 0.4, 'h': 0.52}),
               P('note7c', 'pnNote', pos=add(wout(CAR7, 3, CRY7, 0.16), [0, 0, 0]), ry=yaw(W_RR, C7['from']), opts={'slapAt': r(P73 + 0.22), 'w': 0.4, 'h': 0.52}),
               DROP('goutt7a', 'mec', [0.22, 0.36, 0.0], 1.25), DROP('goutt7b', 'mec', [-0.22, 0.3, 0.02], 1.1, P72), DROP('goutt7c', 'mec', [0.05, 0.52, -0.05], 1.2, P73), DROP('goutt7d', 'mec', [0.3, 0.12, 0.02], 1.0, P73)], cams=[C7])
for tp in (P71, P72, P73): st.cue('sfx:pop', 'S07', tp, 0.45); st.cue('thud', 'S07', r(tp + 0.06), 0.35)
for tp in (P71, P72, P73): st.cue('clack', 'S07', r(tp + 0.22), 0.25)

# ================================================================= S08
# 8: a low three-quarter along a motorway jam: car after car drops onto flat tyres with a dust puff, the wave rolling at us; drivers lean out
D8 = st.dur('S08')
LANES = [[7.2, 5.0, 9, 5.4], [3.6, 2.0, 9, 5.4], [0.0, -1.5, 8, 5.4]]   # (pass 3) the near lane on the drivers' side (+Z): they lean out toward us
C8 = cam(0.0, [12.0, 1.0, 12.0], [11.5, 1.0, 11.75], [2.73, 1.65, 8.26], [2.73, 1.65, 8.26], lens=51)   # on the hard shoulder, the lane receding to the left   # low on the drivers' side, down the jam: the near car at the right, the wave coming from the left   # (pass 3) low on the drivers' side: the cars fill down to the captions
chk('S08', C8, {'near': [5.0, 1.0, 7.2], 'near2': [2.0, 1.0, 3.6], 'far': [-25.0, 1.0, 3.6], 'near3': [-1.5, 1.0, 0.0], 'nearBot': [5.0, 0.0, 8.0]})
st.shot('S08', 'grassland', look={'sunDir': [0.6, 0.9, 0.5]}, actors=[],
        props=[P('bouchon8', 'pnWave', pos=[0, 0, 0], opts={'lanes': LANES, 'farX': -14.0, 'speed': 16.0, 't0': 0.2,   # (pass 3) the wave starts in the visible part of the jam: frame 6 to ~1.4 s
                                                                                       'drivers': 'all', 'len': 120, 'shoulder': 4.5})], cams=[C8])
for i in range(5): st.cue('thud', 'S08', r(0.3 + 0.18 * i), 0.2)

# ================================================================= S09
# 9: a hospital street: the white van with its plain orange stripe and blue beacon, on flat tyres; three patients in pale gowns push it from
#    behind, heads turned to us; static wide
D9 = st.dur('S09'); ZV = -4.4; XV0, XV1 = 0.8, 1.3
VAN0, VAN1 = [XV0, 0, ZV], [XV1, 0, ZV]
# two patients at the back doors, the third pushes the second's back (a chain); seen from the side, a little ahead of them, heads turned to us
PAT = [('malade1', -3.4, -3.85, 'door'), ('malade2', -3.4, -4.8, 'door'), ('malade3', -3.95, -3.05, 'back')]   # (pass 2) further back: leaning in
def pat_pos(xv, dx, z): return [r(xv + dx), 0, z]
C9 = fcam(0.0, [-0.2, 1.5, 2.6], {'p1': add(pat_pos(XV0, -3.4, -3.85), [0, 2.3, 0]), 'p3': add(pat_pos(XV0, -3.95, -3.05), [0, 2.3, 0]), 'p2': add(pat_pos(XV0, -3.4, -4.8), [0, 2.3, 0]), 'feet': pat_pos(XV0, -3.95, -3.05), 'beacon': [XV0 - 2.2, 2.75, ZV], 'wheel': [XV0 - 1.65, 0.0, ZV + 1.0], 'stripe': [XV0 - 1.4, 1.05, ZV + 1.0]}, top=0.08, bottom=0.84, margin=0.13, push=0.25)   # (pass 3) tighter: the three pushers, the back doors, a flat rear tyre, the stripe and beacon
chk('S09', C9, {**{n: add(pat_pos(XV0, dx, z), [0, 1.95, 0]) for n, dx, z, _ in PAT}, 'beacon': [XV0 - 2.2, 2.6, ZV], 'stripe': [XV0 - 1.0, 1.05, ZV + 1.0], 'feet1': pat_pos(XV0, -3.4, -3.85), 'vanFront': [XV0 + 2.6, 0.5, ZV + 1.0], 'pat3': add(pat_pos(XV0, -3.95, -3.05), [0, 1.95, 0])})
pats = []
for i, (pid, dx, z, how) in enumerate(PAT):
    a, b = pat_pos(XV0, dx, z), pat_pos(XV1, dx, z)
    if how == 'door':
        def hands(xv, z=z): return {'L': R5([r(xv - 2.66), 1.3, r(z - 0.2)]), 'R': R5([r(xv - 2.66), 1.25, r(z + 0.2)])}
    else:
        def hands(xv, z=z): return {'L': R5([r(xv - 3.55), 1.4, r(z - 0.95)]), 'R': R5([r(xv - 3.55), 1.35, r(z - 0.6)])}
    ks = [k(0.0, clip='pushCartWalk'), k(0.0, to=b, dur=D9, clip='pushCartWalk', ease='linear', face='keep'), k(0.0, look='camera'),
          TK(0.0, hands(XV0), {'L': 'open', 'R': 'open'}, [STRAIN, TIRED, {**STRAIN, 'brow': 0.2}][i], bend={'spine': SP(0.6), 'neck': SP(-0.55, 0.5)}, d=0.0),
          *[TK(r(0.35 + 0.5 * j), sq=(1.05, 0.94, 1.05) if j % 2 == 0 else (0.98, 1.03, 0.98), d=0.2, keep=True) for j in range(4)],
          TK(D9, hands(XV1), {'L': 'open', 'R': 'open'}, d=D9, e='linear', keep=True), *blink(0.6 + 0.4 * i, TIRED)]
    pats.append(act(pid, a, 90, 'pushCartWalk', 'neutral', keys=ks))
st.shot('S09', 'street', look={'sunDir': [0.5, 0.9, 0.7]}, actors=pats,
        props=[P('ambu9', 'pnVan', pos=VAN0, opts={'state': 1, 'driver': True, 'roll': [[0, 0], [D9, XV1 - XV0]]}, keys=[k(0.0, to=VAN1, dur=D9, ease='linear')]),
               P('gyro9', 'blueBeacon', pos=[XV0 - 2.2, 2.5, ZV], opts={'r': 0.14}, keys=[k(0.0, to=[XV1 - 2.2, 2.5, ZV], dur=D9, ease='linear')]),
               P('platre9', 'footCast', on={'actor': 'malade1', 'joint': 'footR'})], cams=[C9])
st.cue('sfx:scratch', 'S09', 0.0, 0.2)

# ================================================================= the press room (S10, S13)
PRESS = {'flags': False, 'podium': False, 'chairs': False, 'backdrop': ' '}
LOOKP = {'sunDir': [0.3, 0.9, 0.8]}
MINF = {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}

# ================================================================= S10
# 10: the minister in a plain suit at the podium, arms at his sides; behind him the chart whose one thick red curve climbs steeply; flashes; ÉPIDÉMIE
D10 = st.dur('S10'); CARD10 = st.at('S10', 'L10', 7)
MIN10 = [-0.15, 0, -2.0]; POD10 = [-0.15, 0, -1.6]; CH10 = [0.62, 0, -2.4]; RYCH = -12
C10 = cam(0.0, [0.2, 1.5, 3.1], [0.2, 1.5, 2.85], [0.18, 1.42, -2.0], [0.18, 1.42, -2.0], lens=42)
chk('S10', C10, {'minFace': add(MIN10, [0, 2.0, 0]), 'minTop': add(MIN10, [0, 2.3, 0]), 'chartTop': add(CH10, [0, 1.95, 0]), 'chartBot': add(CH10, [0, 0.95, 0]), 'chartL': add(CH10, [-0.5, 1.4, 0]), 'chartR': add(CH10, [0.5, 1.4, 0])})
km10 = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'L': R5(off(MIN10, 10, 0.12, -0.32, 0.92)), 'R': R5(off(MIN10, 10, 0.12, 0.32, 0.92))}, {'L': 'rest', 'R': 'rest'}, MINF, d=0.0),
        TK(0.9, face={**MINF, 'lid': 0.4}, bend={'neck': SP(0.1)}, sq=(1.01, 1.03, 1.01), d=0.3, keep=True),
        TK(1.5, face={**MINF, 'brow': 0.1, 'lid': 0.2, 'mouth': 'smirk'}, bend={'spine': SP(-0.06), 'neck': SP(-0.3)}, sq=(0.99, 1.04, 0.99), d=0.18, keep=True),   # chin up as the curve tops out
        *blink(0.45, MINF), *blink(2.15, MINF), *BREATHE(0.1, D10, 0.45, 0.03)]
st.shot('S10', 'pressRoom', setOpts=PRESS, look=LOOKP, actors=[act('ministre', MIN10, 10, 'stand', 'neutral', keys=km10)],
        props=[P('pupitre10', 'plainPodium', pos=POD10, ry=10), P('courbe10', 'pnChart', pos=CH10, ry=RYCH, opts={'grow': [0.15, 1.5], 'w': 1.0, 'h': 0.75, 'y0': 1.0}),
               P('flash10', 'flashBursts', pos=[0.85, 0.95, 0.4], opts={'n': 5, 'w': 0.6, 'h': 0.5, 'at': [0.3, 0.75, 1.1, 1.6, 1.95, 2.2]})], cams=[C10])
st.card('S10', 'ÉPIDÉMIE', at=CARD10)
st.cue('sfx:shutter', 'S10', 0.3, 0.3); st.cue('sfx:shutter', 'S10', 1.1, 0.3); st.cue('sfx:shutter', 'S10', 1.95, 0.3)

# ================================================================= S11
# 11: the car park turned vaccination centre: three flat cars nose to us; in each gap a masked nurse kneels and pushes a giant syringe into the
#    next car's front tyre, which pops round; in the last ten frames, the hero pushes his car into the right edge of the frame
D11 = st.dur('S11'); INJ = [0.55, 1.25, 1.95]
CARX = [-3.2, 0.0, 3.2]; CARZ = [2.2, 0.0, -2.2]; CRY11 = -90   # noses to +Z, staggered in depth so the row packs into the narrow frame
def car11(i): return [CARX[i], 0, CARZ[i]]
def fr_wheel(i): return wpos(car11(i), 0, CRY11)       # the front left wheel (world -X side: its nurse faces the camera)
SYRD = [-0.62, 0, -0.78]; SYS = 0.9                 # the syringe's scale                              # the syringe's axis from the tyre back toward its nurse (unit, xz)
NUR = []
for i in range(3):
    w = fr_wheel(i); tip = [r(w[0] - 0.1), 0.31, w[2]]
    NUR.append({'tip': tip, 'pos': [r(tip[0] + SYRD[0] * 1.26 * SYS - 0.25), 0, r(tip[2] + SYRD[2] * 1.26 * SYS + 0.05)]})
HDIR11 = [0.35, 0, 0.94]; HCAR11_1 = [-1.6, 0, 4.8];   # (pass 2) in from the right edge, toward the lens: he ends at the frame's right edge, face to us
HCAR11_0 = [r(HCAR11_1[0] - 0.6 * HDIR11[0]), 0, r(HCAR11_1[2] - 0.6 * HDIR11[2])]
HCRY11 = r(math.degrees(math.atan2(-HDIR11[2], HDIR11[0])), 1); HRY11 = yaw([0, 0, 0], HDIR11)
def hero11(c): return [r(c[0] - 2.25 * HDIR11[0]), 0, r(c[2] - 2.25 * HDIR11[2])]
def rear11(c, s): return [r(c[0] - 1.8 * HDIR11[0] + s * 0.4 * HDIR11[2]), 0.86, r(c[2] - 1.8 * HDIR11[2] - s * 0.4 * HDIR11[0])]
C11 = fcam(0.0, [-5.0, 2.2, 6.0], {**{f'n{i}': add(NUR[i]['pos'], [0, 1.55, 0]) for i in range(2)}, **{f't{i}': NUR[i]['tip'] for i in range(2)}, **{f'w{i}': add(fr_wheel(i), [0, -0.3, 0]) for i in range(2)}, 'car1top': add(car11(1), [0, 1.5, 0])}, top=0.12, bottom=0.8, margin=0.14, push=0.3)   # (pass 3) two cars and their nurses, tighter
chk('S11', C11, {**{f'nur{i}': add(NUR[i]['pos'], [0, 1.5, 0]) for i in range(3)}, **{f'tip{i}': NUR[i]['tip'] for i in range(3)}, 'heroCar': add(HCAR11_1, [-1.0, 0.9, 0]), 'heroIn': add(hero11(HCAR11_1), [0, 1.9, 0])})
nurses, syr = [], []
SYRY = r(math.degrees(math.atan2(-SYRD[2], SYRD[0])) + 180, 1)   # the syringe's +X (needle side) points from the nurse toward the tyre
for i in range(3):
    n = NUR[i]; tip = n['tip']; t = INJ[i]
    flange = [r(tip[0] + SYRD[0] * 0.99 * SYS), 0.14, r(tip[2] + SYRD[2] * 0.99 * SYS)]; thumb0 = [r(tip[0] + SYRD[0] * 1.68 * SYS), 0.14, r(tip[2] + SYRD[2] * 1.68 * SYS)]; thumb1 = [r(tip[0] + SYRD[0] * 1.04 * SYS), 0.14, r(tip[2] + SYRD[2] * 1.04 * SYS)]   # aimed 0.17 low: the kneel lowers the body after the arm is solved
    ry = yaw(n['pos'], tip)
    ks = [k(0.0, clip='kneel'), k(0.0, look=tip), TK(0.0, {'L': R5(add(flange, [0, 0.0, 0])), 'R': R5(add(thumb0, [0, 0.0, 0]))}, {'L': 'grip', 'R': 'open'}, {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}, bend={'spine': SP(0.25), 'neck': SP(0.1, 0.3)}, d=0.0),
          TK(r(t - 0.32), {'R': R5(thumb1)}, {'R': 'open'}, {'lid': 0.4, 'mouth': 'clench', 'brow': 0.4}, d=0.3, keep=True),
          TK(r(t + 0.2), {'R': R5(thumb0)}, {'R': 'open'}, {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}, d=0.3, keep=True), k(r(t + 0.25), look='camera', lookDur=0.2), *blink(r(t + 0.8), CALM)]
    nurses.append(act(f'inf{i + 1}', n['pos'], ry, 'kneel', 'neutral', keys=ks))
    syr.append(P(f'seringue11_{i}', 'pnSyringe', pos=tip, ry=SYRY, scale=SYS, opts={'rb': 0.13, 'pushAt': [[r(t - 0.32), r(t - 0.02)]]}))
HIN = r(D11 - 10 / 30)
kh11 = [k(0.0, clip='pushCartWalk'), k(0.0, look='camera'), k(0.0, visible=False), k(HIN, visible=True), k(HIN, to=hero11(HCAR11_1), dur=r(D11 - HIN), clip='pushCartWalk', ease='linear', face='keep'),
        TK(0.0, {'L': R5(rear11(HCAR11_0, 1)), 'R': R5(rear11(HCAR11_0, -1))}, {'L': 'open', 'R': 'open'}, STRAIN, bend=PUSH, d=0.0),
        TK(HIN, {'L': R5(rear11(HCAR11_0, 1)), 'R': R5(rear11(HCAR11_0, -1))}, {'L': 'open', 'R': 'open'}, STRAIN, bend=PUSH, d=0.0, keep=True),
        TK(D11, {'L': R5(rear11(HCAR11_1, 1)), 'R': R5(rear11(HCAR11_1, -1))}, {'L': 'open', 'R': 'open'}, d=r(D11 - HIN), e='linear', keep=True)]
st.shot('S11', 'grassland', look={'sunDir': [0.6, 0.9, 0.6]}, actors=[*nurses, act('mec', hero11(HCAR11_0), HRY11, 'pushCartWalk', 'neutral', keys=kh11)],
        props=[P('parking11', 'parkLot', pos=[0, 0, -1.0], opts={'w': 40, 'd': 24}),
               *[P(f'voit11_{i}', 'pnCar', pos=car11(i), ry=CRY11, opts={'color': ['#E05A47', '#F2C94C', '#5A7FB8'][i], 'state': [[r(INJ[i] - 0.26), 1], [r(INJ[i] - 0.02), 0]], 'dust': False, 'stretchAmp': 0.85}) for i in range(3)], *syr,
               P('voitmec11', 'pnCar', pos=HCAR11_0, ry=HCRY11, opts={'open': True, 'wheels': [0, 0, 0, 2]}, keys=[k(0.0, visible=False), k(HIN, visible=True), k(HIN, to=HCAR11_1, dur=r(D11 - HIN), ease='linear')]),
               DROP('goutt11', 'mec', [0.22, 0.36, 0.0], 1.35), *[P(f'masque11_{i}', 'pnMask', on={'actor': f'inf{i + 1}', 'joint': 'head'}) for i in range(3)]], cams=[C11])
for t in INJ: st.cue('sfx:pop', 'S11', r(t + 0.02), 0.4)

# ================================================================= S12
# 12: the pharmacy counter, frontal: the pharmacist presents the plain foot pump on a red velvet cushion; a price tag (no figure) pops beside it,
#    then the round sticker two thirds green
D12 = st.dur('S12'); TAG12 = r(st.at('S12', 'L12', 5) - 0.05); PIE12 = r(st.at('S12', 'L12', 7) - 0.05)
CNT = [0.0, 0, -0.6]; PH = [0.0, 0, -1.35]; CUSH = [0.0, 0.985, -0.42]   # (pass 3) the cushion held forward, clear of her body
C12 = cam(0.0, [0.12, 1.42, 2.55], [0.1, 1.4, 2.3], [0.0, 1.3, -0.8], [0.0, 1.3, -0.8], lens=40)
chk('S12', C12, {'phFace': add(PH, [0, 2.0, 0]), 'phTop': add(PH, [0, 2.3, 0]), 'pump': add(CUSH, [0, 0.2, 0]), 'tag': [-0.47, 1.3, -0.28], 'tagL': [-0.6, 1.2, -0.28], 'pie': [0.36, 1.33, -0.3], 'counter': [0, 0.96, -0.3]})
kph = [k(0.0, clip='stand'), k(0.0, look='camera'), TK(0.0, {'L': R5(add(CUSH, [0.33, -0.02, -0.02])), 'R': R5(add(CUSH, [-0.33, -0.02, -0.02]))}, {'L': 'open', 'R': 'open'}, SMUG, bend={'spine': SP(0.12)}, d=0.0),
       k(r(TAG12 + 0.05), look=[-0.38, 1.1, -0.3], lookDur=0.15), k(r(TAG12 + 0.5), look='camera', lookDur=0.15), k(r(PIE12 + 0.05), look=[0.36, 1.33, -0.3], lookDur=0.15), k(r(PIE12 + 0.5), look='camera', lookDur=0.2),
       TK(r(PIE12 + 0.5), face={**SMUG, 'brow': 0.5}, d=0.15, keep=True), *blink(1.0, SMUG), *blink(3.1, SMUG), *BREATHE(0.2, D12, 0.6, 0.012)]
st.shot('S12', 'whiteVoid', setOpts={'color': '#DDE9E2'}, look={'sunDir': [0.3, 0.9, 0.9]}, actors=[act('pharma', PH, 0, 'stand', 'neutral', keys=kph)],
        props=[P('comptoir12', 'pnCounter', pos=CNT, opts={'shelfZ': -1.25}), P('coussin12', 'velvetCushion', pos=CUSH, opts={'w': 0.56}),
               P('pompe12', 'pnPump', pos=add(CUSH, [0, 0.105, 0]), ry=0, opts={'s': 0.95, 'pumpAt': [0.6, 2.9]}),   # side on: the pedal pump's silhouette
               P('prix12', 'priceTag', pos=[-0.46, 1.16, -0.26], ry=8, scale=0.7, opts={'text': ' '}, keys=[k(0.0, visible=False), k(TAG12, visible=True), k(TAG12, squash=[1.4, 1.4, 1.4], dur=0.3)]),
               P('pastille12', 'pnPie', pos=[0.36, 1.33, -0.3], ry=-4, opts={'r': 0.17, 'popAt': PIE12})], cams=[C12])
st.cue('sfx:pop', 'S12', TAG12, 0.35); st.cue('sfx:pop', 'S12', PIE12, 0.45); st.cue('sfx:squeak', 'S12', 0.6, 0.15)

# ================================================================= S13
# 13: the same press room: the pump on a plinth under a glass dome; the minister cuts the ribbon in front of it, elbows bent; flashes
D13 = st.dur('S13'); CUT13 = 0.95
MIN13 = [-0.75, 0, -1.55]; MRY13 = 28; PLI = [0.4, 0, -1.75]; RIB = [0.4, 0, -1.05]
C13 = cam(0.0, [0.0, 1.5, 2.7], [0.0, 1.5, 2.45], [-0.05, 1.35, -1.5], [-0.05, 1.35, -1.5], lens=42)
chk('S13', C13, {'minFace': add(MIN13, [0, 2.0, 0]), 'minTop': add(MIN13, [0, 2.3, 0]), 'dome': add(PLI, [0, 1.6, 0]), 'pump': add(PLI, [0, 1.15, 0]), 'ribbon': add(RIB, [0, 0.95, 0])})
SNIP = add(RIB, [-0.12, 0.95, 0.0])
km13 = [k(0.0, clip='stand'), k(0.0, look=SNIP), TK(0.0, {'R': R5(add(SNIP, [-0.25, 0.25, 0.1])), 'L': R5(add(SNIP, [-0.35, 0.2, 0.15]))}, {'R': 'grip', 'L': 'grip'}, MINF, bend={'spine': SP(0.15)}, d=0.0),
        TK(0.5, {'R': R5(add(SNIP, [-0.2, 0.08, 0.08])), 'L': R5(add(SNIP, [-0.3, 0.05, 0.12]))}, {'R': 'grip', 'L': 'grip'}, {**MINF, 'brow': -0.5}, d=0.25, keep=True),
        TK(CUT13, {'R': R5(add(SNIP, [-0.16, 0.03, 0.05])), 'L': R5(add(SNIP, [-0.26, 0.02, 0.1]))}, {'R': 'grip', 'L': 'grip'}, {'lid': 0.1, 'mouth': 'smile', 'brow': 0.3}, (1.02, 0.98, 1.02), d=0.06, keep=True),
        k(r(CUT13 + 0.2), look='camera', lookDur=0.2), TK(r(CUT13 + 0.25), {'R': R5(off(MIN13, MRY13, 0.35, 0.25, 1.2)), 'L': R5(off(MIN13, MRY13, 0.25, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, SMUG, (1, 1, 1), d=0.3, keep=True), *blink(1.6, SMUG)]
st.shot('S13', 'pressRoom', setOpts=PRESS, look=LOOKP, actors=[act('ministre', MIN13, MRY13, 'stand', 'neutral', keys=km13)],
        props=[P('socle13', 'pnPlinth', pos=PLI, ry=-10), P('courbe13', 'pnChart', pos=[0.95, 0, -2.75], ry=-14, opts={'w': 1.0, 'h': 0.75, 'y0': 1.0}), P('ruban13', 'ribbonCut', pos=RIB, opts={'w': 1.0, 'h': 0.95, 'cutAt': CUT13}),
               P('ciseaux13', 'bigScissors', on={'actor': 'ministre', 'hand': 'R', 'offset': [0, -0.05, 0.06], 'rot': [0, -0.6, 0]}, opts={'snip': [[0, 1], [r(CUT13 - 0.05), 1], [CUT13, 0]]}),
               P('flash13', 'flashBursts', pos=[0.8, 0.9, 0.3], opts={'n': 5, 'w': 0.6, 'h': 0.5, 'at': [0.2, 0.6, 1.0, 1.05, 1.3, 1.65]})], cams=[C13])
st.cue('sfx:clink', 'S13', CUT13, 0.45); st.cue('sfx:shutter', 'S13', 1.0, 0.35)

# ================================================================= the driveway (S14, S15, S16)
CARD = [0.2, 0, -1.6]                     # his car parked before the house, nose to +X, on bare rims from S14

# ================================================================= S14
# 14: the tyre rolls in on its own, plump and shiny, a towel round it like a scarf; the hero, drops all over him, looks up from beside his car
D14 = st.dur('S14'); STOP14 = 1.5
TY14_0, TY14_1 = [4.3, 0, 0.6], [2.25, 0, 1.4]; TRY14 = r(math.degrees(math.atan2(-(TY14_1[2] - TY14_0[2]), -(TY14_1[0] - TY14_0[0]))), 1)   # it rolls along its local -X
HER14 = [0.85, 0, -0.1]; HRY14 = 30
C14 = fcam(0.0, [0.9, 1.05, 6.4], {'heroTop': add(HER14, [0, 2.6, 0]), 'heroFeet': HER14, 'tyreR': add(TY14_1, [0.45, 0.9, 0]), 'tyreB': add(TY14_1, [0, 0, 0.2])}, top=0.1, bottom=0.82, margin=0.16, push=0.2)
chk('S14', C14, {'heroFace': add(HER14, [0, 1.95, 0]), 'tyre1': add(TY14_1, [0, 0.4, 0]), 'tyre0': add(TY14_0, [0, 0.4, 0])})
TAKE14 = 1.62
k14 = [k(0.0, clip='stand'), k(0.0, look=add(CARD, [0, 0.3, 0.8])), TK(0.0, {'L': R5(add(CARD, [0.6, 0.85, 0.84])), 'R': R5(off(HER14, HRY14, 0.15, 0.3, 0.9))}, {'L': 'open', 'R': 'rest'}, TIRED, bend={'spine': SP(0.25, -0.2), 'neck': SP(0.35)}, d=0.0),
       k(0.9, look=TY14_1, lookDur=0.15), TK(0.9, face={**TIRED, 'lid': 0.45}, bend={'spine': SP(0.2, -0.15), 'neck': SP(0.1)}, d=0.15, keep=True),   # a glance, nothing
       k(1.2, look=add(CARD, [0, 0.3, 0.8]), lookDur=0.12), TK(1.2, face=TIRED, bend={'spine': SP(0.25, -0.2), 'neck': SP(0.35)}, d=0.12, keep=True),
       TK(r(TAKE14 - 0.08), sq=(1.06, 0.92, 1.06), d=0.06, keep=True),   # the double take: down, then up hard, eyes out on stalks
       k(TAKE14, look=add(TY14_1, [0, 0.5, 0]), lookDur=0.05), TK(TAKE14, face={'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'pop': 1.0, 'jaw': 0.4}, sq=(0.86, 1.16, 0.86), scl={'head': [0.9, 1.15, 0.95]}, bend={'spine': SP(-0.08, -0.1), 'neck': SP(-0.2)}, d=0.05, e='out', keep=True),
       TK(r(TAKE14 + 0.12), sq=(1.04, 0.97, 1.04), scl={'head': [1.03, 0.97, 1.0]}, d=0.08, keep=True),
       TK(r(TAKE14 + 0.24), sq=(1, 1, 1), scl={'head': [1, 1, 1]}, face={'lid': 0.0, 'mouth': 'O', 'brow': 0.9, 'pop': 0.8, 'jaw': 0.25}, d=0.12, keep=True), *blink(0.5, TIRED), *BREATHE(0.1, 1.5, 0.4, 0.02)]
st.shot('S14', 'pavillon', setOpts=PAV, look={'sunDir': [0.6, 0.9, 0.7]}, actors=[act('mec', HER14, HRY14, 'stand', 'neutral', keys=k14)],
        props=[P('voit14', 'pnCar', pos=CARD, opts={'open': True, 'state': 2}),
               P('pneu14', 'pnTyre', pos=TY14_0, ry=TRY14, opts={'shine': True, 'towel': 'scarf', 'R': 0.36, 'r': 0.14, 'roll': [[0, 0], [STOP14, -r(math.dist(TY14_0, TY14_1), 3)]]}, keys=[k(0.0, to=TY14_1, dur=STOP14, ease='out'), k(STOP14, squash=[1.18, 0.8, 1.18], dur=0.4)]),
               DROP('goutt14a', 'mec', [0.3, 0.5, -0.12], 1.5), DROP('goutt14b', 'mec', [-0.3, 0.46, -0.1], 1.35), DROP('goutt14c', 'mec', [0.0, 0.66, -0.16], 1.25)], cams=[C14])
st.cue('sfx:squeak', 'S14', STOP14, 0.25)

# ================================================================= S15
# 15: the tyre side on, filling the frame: the reddish inner tube fills its hole, puffs up twice; a heart pops
D15 = st.dur('S15'); PUFF15 = [0.45, 0.9]; HEART15 = 1.3
TY15 = [0.0, 0, 0.0]; TUBE15 = [0.0, 0.37, 0.0]
C15 = cam(0.0, [0.05, 0.58, 2.35], [0.04, 0.56, 2.15], [0.0, 0.47, 0.0], [0.0, 0.47, 0.0], lens=38)
chk('S15', C15, {'tyreTop': [0, 0.74, 0], 'tyreBot': [0, 0.0, 0], 'tyreL': [-0.37, 0.37, 0], 'tyreR': [0.37, 0.37, 0], 'heart': [0.12, 0.98, 0.1]})
st.shot('S15', 'pavillon', setOpts=PAV, look={'sunDir': [0.5, 0.9, 0.9]}, actors=[],
        props=[P('pneu15', 'pnTyre', pos=TY15, opts={'shine': True, 'rim': False, 'puff': [0.5, 0.95]}), P('chambre15', 'pnTube', pos=TUBE15, opts={'R': 0.118, 'r': 0.052, 'puff': PUFF15}),
               P('coeur15', 'heartPop', pos=[0.12, 0.98, 0.12], opts={'at': HEART15, 'size': 0.24})], cams=[C15])
st.cue('sfx:squeak', 'S15', 0.45, 0.25); st.cue('sfx:squeak', 'S15', 0.9, 0.25); st.cue('sfx:pop', 'S15', HEART15, 0.35)

# ================================================================= S16
# 16: low as in S01: the hero lies face down across the bonnet of his car, arms dangling, a ring of big sweat drops round him; the plump tyre rolls
#    past behind
D16 = st.dur('S16')
HER16 = [r(CARD[0] + 1.3), 0.8, r(CARD[2] - 1.22)]     # his feet past the bonnet's far edge: tipped forward flat (lay), he lies across it
TY16_0, TY16_1 = [4.2, 0, -4.4], [-2.6, 0, -4.4]          # behind the car (seen over it), crossing the frame
C16 = cam(0.0, [4.6, 0.45, 2.7], [4.45, 0.45, 2.55], [1.0, 0.95, -1.7], [1.0, 0.95, -1.7], lens=46)   # from the nose: his body a plank across the bonnet
chk('S16', C16, {'feet': HER16, 'head': add(HER16, [0, 0.1, 2.25]), 'tyre0': add(TY16_0, [0, 0.4, 0]), 'tyre1': add(TY16_1, [0, 0.4, 0]), 'tyreMid': [-3.6, 0.0, -1.6], 'bonnet': add(CARD, [1.95, 0.75, 0])})
FLATF = {'lid': 1.0, 'mouth': 'line', 'brow': 0.5}
k16 = [k(0.0, clip='stand'), k(0.0, toon={'lay': [1.52, 0]}, toonDur=0.0), k(0.0, look=[HER16[0], -1.0, 1.0]),
       TK(0.0, {'L': R5([r(HER16[0] + 0.3), 0.3, r(CARD[2] + 1.15)], 1, 0.0), 'R': R5([r(HER16[0] - 0.3), 0.3, r(CARD[2] + 1.15)], 1, 0.0)}, {'L': 'rest', 'R': 'rest'}, FLATF, bend={'neck': SP(0.6)}, d=0.0, keep=True),
       *[TK(r(0.25 + 0.5 * i), {'L': R5([r(HER16[0] + 0.3 + 0.04 * (i % 2)), 0.3, r(CARD[2] + 1.15)], 1, 0.0), 'R': R5([r(HER16[0] - 0.3 - 0.04 * (i % 2)), 0.3, r(CARD[2] + 1.15)], 1, 0.0)}, d=0.45, keep=True) for i in range(4)],
       *[k(r(0.1 + 0.6 * i), toon={'sq': [1.04, 0.94, 1.04] if i % 2 == 0 else [1, 1, 1]}, toonDur=0.55, keepPose=True) for i in range(4)],   # slow breaths
       TK(1.05, {'R': R5([r(HER16[0] - 0.3), 0.42, r(CARD[2] + 1.3)], 1, 0.0)}, {'R': 'spread'}, d=0.04, keep=True), TK(1.14, {'R': R5([r(HER16[0] - 0.3), 0.3, r(CARD[2] + 1.15)], 1, 0.0)}, {'R': 'rest'}, d=0.08, keep=True)]   # one hand twitches
RING = [[0, 1.45, -0.6], [0, 1.6, 0.2], [0, 1.55, 1.0], [0, 1.35, 1.75], [0, 1.0, 2.5], [0, 1.0, -1.15], [0.3, 1.85, 0.6]]
st.shot('S16', 'pavillon', setOpts=PAV, look={'sunDir': [0.6, 0.9, 0.7]}, actors=[act('mec', HER16, 0, 'stand', 'neutral', keys=k16)],
        props=[P('voit16', 'pnCar', pos=CARD, opts={'open': True, 'state': 2}),
               P('pneu16', 'pnTyre', pos=TY16_0, ry=0, opts={'shine': True, 'towel': 'scarf', 'R': 0.4, 'r': 0.15, 'roll': [[0, 0], [D16, r(TY16_1[0] - TY16_0[0])]]}, keys=[k(0.0, to=TY16_1, dur=D16, ease='linear')]),
               P('glisse16', 'sweatDrop', pos=add(HER16, [0.3, 1.2, 1.2]), scale=2.0, keys=[k(0.3, to=add(HER16, [0.3, 0.12, 1.45]), dur=0.7, ease='in'), k(1.0, squash=[2.2, 0.25, 2.2], dur=0.3), k(1.35, visible=False)]),   # a drop slides off and splats
               *[P(f'goutt16_{i}', 'sweatDrop', pos=add(HER16, p), ry=90, scale=2.3 - 0.15 * (i % 3)) for i, p in enumerate(RING)]], cams=[C16])
st.cue('sfx:poof', 'S16', 0.3, 0.35)

# ================================================================= S17
# 17: the framing of S02: the hero sits on the examination table; the doctor runs the stethoscope over him, looks behind his ear and under his
#    tie for a valve, taps his chest twice, shakes his head and hands back his car keys; held
D17 = st.dur('S17'); EAR17, TIE17, TAP17, SHAKE17, KEYS17 = 0.7, 1.3, 1.95, 2.35, 2.95
HER17 = [0.05, 0.36, -0.82]; HRY17 = 10
DOC17 = [0.95, 0, -1.3]; DRY17 = -40                    # (pass 3) behind him at his left, turned toward us: the glasses read, the arms reach forward
CHEST = add(HER17, [0.0, 1.15, 0.22]); EAR = add(HER17, [0.24, 1.72, -0.04]); TIE = add(HER17, [0.0, 1.05, 0.24])
C17 = cam(0.0, [-0.8, 1.8, 3.6], [-0.7, 1.78, 3.4], [0.6, 1.3, -0.7], [0.6, 1.32, -0.7], lens=46)
chk('S17', C17, {'heroFace': add(HER17, [0, 1.6, 0]), 'heroTop': add(HER17, [0, 1.95, 0]), 'docFace': add(DOC17, [0, 2.0, 0]), 'docTop': add(DOC17, [0, 2.3, 0]), 'chest': CHEST})
DRL = off(DOC17, DRY17, 0.22, 0.24, 1.0); DLL = off(DOC17, DRY17, 0.22, -0.24, 1.0)   # his hands at rest
kd17 = [k(0.0, clip='stand'), k(0.0, look=CHEST), TK(0.0, {'R': R5(add(CHEST, [0.06, 0.05, 0.03])), 'L': R5(DLL)}, {'R': 'grip', 'L': 'rest'}, GRAVE, bend={'spine': SP(0.25)}, d=0.0),
        TK(0.3, {'R': R5(add(CHEST, [0.0, -0.12, 0.03]))}, {'R': 'grip'}, d=0.22, keep=True),
        # behind the ear: the hand goes, he leans to peek, held
        k(EAR17, look=EAR, lookDur=0.12), TK(EAR17, {'R': R5(add(EAR, [0.04, 0.0, -0.06]))}, {'R': 'point'}, {**GRAVE, 'brow': -0.1, 'gx': -0.5}, bend={'spine': SP(0.3, 0.15), 'neck': SP(0.2, 0.2)}, d=0.16, keep=True),
        # the tie lifted: his left hand takes it and holds it up
        k(TIE17, look=TIE, lookDur=0.12), TK(TIE17, {'L': R5(add(TIE, [0.0, 0.18, 0.12])), 'R': R5(DRL)}, {'L': 'pinch', 'R': 'rest'}, {**GRAVE, 'gy': 0.4}, bend={'spine': SP(0.35, 0.0), 'neck': SP(0.35)}, d=0.18, keep=True),
        # tap, tap (each held)
        TK(r(TAP17 - 0.08), {'L': R5(add(CHEST, [0.02, 0.1, 0.16]))}, {'L': 'point'}, GRAVE, bend={'spine': SP(0.3), 'neck': SP(0.25)}, d=0.08, keep=True),
        TK(TAP17, {'L': R5(add(CHEST, [0.02, 0.1, 0.04]))}, {'L': 'point'}, d=0.05, keep=True), TK(r(TAP17 + 0.1), {'L': R5(add(CHEST, [0.02, 0.1, 0.16]))}, d=0.06, keep=True),
        TK(r(TAP17 + 0.2), {'L': R5(add(CHEST, [0.02, 0.1, 0.04]))}, d=0.05, keep=True), TK(r(TAP17 + 0.3), {'L': R5(DLL)}, {'L': 'rest'}, d=0.15, keep=True),
        # a slow no
        k(SHAKE17, look=add(HER17, [0, 1.6, 0]), lookDur=0.1), *[TK(r(SHAKE17 + 0.18 * i), bend={'spine': SP(0.15), 'neck': SP(0.05, 0.4 if i % 2 == 0 else -0.4)}, face={**GRAVE, 'lid': 0.55}, d=0.17, keep=True) for i in range(3)],
        TK(r(SHAKE17 + 0.54), bend={'spine': SP(0.15), 'neck': SP(0.0, 0.0)}, d=0.08, keep=True),
        TK(KEYS17, {'R': R5(add(HER17, [0.36, 0.95, 0.4]))}, {'R': 'grip'}, GRAVE, d=0.16, keep=True), TK(r(KEYS17 + 0.3), {'R': R5(DRL)}, {'R': 'rest'}, d=0.2, keep=True),
        k(r(KEYS17 + 0.3), look='camera', lookDur=0.15), *blink(1.75, GRAVE)]
SLUMP = {'lid': 0.65, 'mouth': 'line', 'brow': 0.35}
kh17 = [k(0.0, clip='sit'), k(0.0, look=CHEST), TK(0.0, {'L': R5(add(HER17, [0.3, 0.55, 0.3])), 'R': R5(add(HER17, [-0.3, 0.55, 0.3]))}, {'L': 'rest', 'R': 'rest'}, {**TIRED, 'gy': 0.5}, d=0.0),   # (pass 3) left hand at +X: no crossed arms
        k(EAR17, look=EAR, lookDur=0.15), TK(EAR17, face={**TIRED, 'gx': 0.7, 'lid': 0.3}, d=0.1, keep=True),       # his eyes follow the hand
        k(TIE17, look=add(TIE, [0, 0.2, 0.2]), lookDur=0.12), TK(TIE17, face={**TIRED, 'gy': 0.7, 'lid': 0.3}, d=0.1, keep=True),
        k(r(TIE17 + 0.08), toon={'tie': [1.15, 1.35, 0.1]}, toonDur=0.15, keepPose=True), k(r(TAP17 - 0.12), toon={'tie': [0.9, 0.0, 0.0]}, toonDur=0.08, keepPose=True), k(r(TAP17 - 0.04), toon={'tie': [1.0, 0.0, 0.0]}, toonDur=0.06, keepPose=True),
        TK(TAP17, sq=(1.03, 0.97, 1.03), d=0.04, keep=True), TK(r(TAP17 + 0.08), sq=(1, 1, 1), d=0.05, keep=True), TK(r(TAP17 + 0.2), sq=(1.03, 0.97, 1.03), d=0.04, keep=True), TK(r(TAP17 + 0.28), sq=(1, 1, 1), d=0.05, keep=True),
        k(SHAKE17, look=add(DOC17, [0, 1.95, 0]), lookDur=0.12), TK(SHAKE17, face={**TIRED, 'brow': 0.7, 'lid': 0.2}, d=0.1, keep=True),
        *blink(2.78, TIRED), k(KEYS17, look=add(HER17, [0.36, 0.95, 0.4]), lookDur=0.1),
        TK(r(KEYS17 + 0.08), {'L': R5(add(HER17, [0.36, 0.95, 0.4]))}, {'L': 'grip'}, d=0.14, keep=True),
        TK(r(KEYS17 + 0.3), {'L': R5(add(HER17, [0.28, 0.7, 0.32]))}, {'L': 'grip'}, SLUMP, (1.04, 0.93, 1.04), {'spine': SP(0.35), 'neck': SP(0.3)}, d=0.18, keep=True), k(r(KEYS17 + 0.3), look='camera', lookDur=0.15),
        *blink(1.05, TIRED), *BREATHE(0.2, 2.9, 0.6, 0.014)]
st.shot('S17', 'hospital', setOpts=HOSP, look=LOOKH, actors=[act('docteur', DOC17, DRY17, 'stand', 'neutral', keys=kd17), act('mec', HER17, HRY17, 'sit', 'neutral', keys=kh17)],
        props=[*OFFICE('S17'), P('steth17', 'pnSteth', on={'actor': 'docteur', 'hand': 'R', 'offset': [0, -0.08, 0.04]}), P('stcou17', 'pnStethNeck', on={'actor': 'docteur', 'joint': 'neck'}),
               P('clesdoc17', 'pnKeys', on={'actor': 'docteur', 'hand': 'R', 'offset': [0, -0.08, 0.03]}, keys=[k(0.0, visible=False), k(r(KEYS17 - 0.3), visible=True), k(r(KEYS17 + 0.16), visible=False)]),
               P('clesmec17', 'pnKeys', on={'actor': 'mec', 'hand': 'L', 'offset': [0, -0.08, 0.03]}, keys=[k(0.0, visible=False), k(r(KEYS17 + 0.16), visible=True)]),
               DROP('goutt17', 'mec', [0.22, 0.36, 0.0], 1.6)], cams=[C17])
st.cue('sfx:bonk', 'S17', TAP17, 0.25); st.cue('sfx:bonk', 'S17', r(TAP17 + 0.2), 0.25); st.cue('sfx:clink', 'S17', KEYS17, 0.3)

# a toon key that names one hand's reach replaces the whole reach (keepPose merges only the top level): carry the other hand's reach and hand
# pose from the previous keys of the same actor so a one-handed gesture never drops the other hand
for _sc in st.scenes:
    for _a in _sc['actors']:
        _run = {'reach': {}, 'hands': {}}
        for _kk in sorted((x for x in _a.get('keys', []) if isinstance(x, dict) and 'toon' in x), key=lambda x: x.get('at', 0)):
            for _n in ('reach', 'hands'):
                if _n in _kk['toon']: _kk['toon'][_n] = {**_run[_n], **_kk['toon'][_n]}; _run[_n] = dict(_kk['toon'][_n])
print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
GOWN = {'outfit': 'pajamas', 'suit': '#BFD9E8', 'pants': '#BFD9E8', 'shirt': '#BFD9E8', 'lapel': '#A9C8DA', 'tie': '#BFD9E8', 'cuff': '#BFD9E8', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
NURSE = {'outfit': 'doctor', 'suit': '#9FD0C0', 'pants': '#9FD0C0', 'shirt': '#9FD0C0', 'lapel': '#8CC0B0', 'tie': '#9FD0C0', 'cuff': '#9FD0C0', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("Le pneu", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'docteur': {'preset': 'doctor', 'seed': 971, 'hat': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'psy': {'preset': 'proviseur', 'seed': 972, 'hat': 'none', 'suit': '#8A6A4A', 'lapel': '#7A5A3A', 'tie': '#3A5A4A', 'hair': 'receding', 'hairColor': '#9A9A96', 'facial': 'beard', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 973, 'hat': 'none', 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#3C66B0', 'shirt': '#D8DEE6', 'hairColor': '#BDBDBD', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'pharma': {'preset': 'femme', 'seed': 974, 'outfit': 'doctor', 'suit': '#F4F4F0', 'lapel': '#F4F4F0', 'tie': '#4FA36A', 'hat': 'none', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'malade1': {**GOWN, 'preset': 'pyjama', 'seed': 981, 'hair': 'crew', 'hairColor': '#3A3028'},
    'malade2': {**GOWN, 'preset': 'mamie', 'seed': 982, 'outfit': 'pajamas'},
    'malade3': {**GOWN, 'preset': 'worker', 'seed': 983, 'hair': 'bald', 'facial': 'beard'},
    'inf1': {**NURSE, 'preset': 'femme', 'seed': 991}, 'inf2': {**NURSE, 'preset': 'doctor', 'seed': 992, 'hair': 'crew'}, 'inf3': {**NURSE, 'preset': 'journaliste', 'seed': 993},
})
