#!/usr/bin/env python3
"""La rambarde (story 84, cycle 46; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man got his head stuck in the railing. The firemen brought out the big ladder. He lives on the ground floor. Twelve firemen pulled his legs.
He grew twenty centimetres. The railing was declared a natural disaster. The president ordered the head to come out. The head held its ground.
The district was evacuated by helicopter. Except him. The bomb squad blew up the building. Around the railing. The building got a state funeral.
The railing was listed as a historic monument. Head included. He tilted his head. It came out. He was arrested for theft. His head was seized. He
rents his head from the State.
Staging: tight on his box head jammed between two bars of the railing, against the sky, no ground (L03 is the reveal); a fire engine skids up and
its ladder telescopes up into the clouds; wide and low: the railing is at pavement level, his feet on the ground a metre from the firemen, the giant
ladder towering for nothing; twelve firemen in a row lift him horizontal by the legs and heave like a tug of war; his body stretches like elastic,
the head stays put, all twelve fall flat on their backs (from then on he is twenty centimetres taller); a minister in a white hard hat at a pavement
podium slams a giant stamp onto the taped railing; nose to nose on the terrace, the president bellows into a megaphone and the bars ring like a
tuning fork; the bars go still, the head has not moved, the megaphone droops; helicopters winch the residents off the facades, one still in her
armchair; dusk, the empty street, him alone in the railing, the last helicopter leaves; behind a line of riot shields the bomb squad pushes the
plunger and the building goes up in a fireball; the dust clears on a crater where only the blackened railing stands, him still in it, sooty
(RÉUSSI); soldiers slow-march a brick on a velvet cushion with a band and a plain flag; on the crater rim an official cuts a ribbon and unveils a
bronze plaque beside the railing, a soldier salutes (CLASSÉE); the plaque fills half the frame, a thick arrow points at his head; he tilts his head
a quarter turn and it pops out; masked special forces slide down ropes from a helicopter and pin him face down on the rubble (ARRÊTÉ); in the
interrogation room a detective winds seal tape round his head and thumps a red wax seal on his forehead; at a government counter, stooping because
he is too tall for the window, he slides a banknote under the glass and the clerk's stretched arm stamps his forehead with a round seal (ink ring).
The fire ladder stays in the background of every shot from L02 to the end (through a painted window indoors).
Natural look; cycle 46: props_rambarde.js (skyLadder, balconyRail, hardHat, bombHelmet, bombVest, detonator, balaclava, brick, rifle, bronzePlaque,
ribbonCut, scissors, sealTape, waxSeal, inkRing, roundStamp, skyWindow, craterPit, dustCloud, winchCable); fireTruck, banknote (props_news),
helicopter (props_lunettes), velvetCushion, bandInstr (props_centime), riotShield, armyHelmet (props_guepe), megaphone, podium, rubberStamp, fireball,
smokeField, flag (props.js), armchair (props_ascenseur), kepi (props_conseiller), impactStars (props_interrupteur), toonPuff (props_bocal),
sootPatches, smokeRibbon, twinkle, smearArc (props_barbecue), timedBurst (props_flaque), rope (props_table), haussmann (props_vp) reused.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.86) and heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() before stills; flat
grounds raised 5 cm or more; soot in charcoal-grey patches; horizontal actions staged in depth (the 9:16 frame is only ~2 m wide at 4-5 m)."""
from story_kit import *
import math

st = Story('rambarde', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    """(round 1) where the points that must read fall in the frame of a camera (printed when the script runs)"""
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
SQUASHED = {'lid': 0.45, 'mouth': 'line', 'cheeks': 0.6, 'brow': -0.05}

# ---- (round 1) the street (parisStreet): the road along Z (x -5..5), the right-hand pavement x 5..10, the house fronts at x 10.2. His building is the
#      right-hand block round z 0; his terrace is a step at pavement level (floor 0.22) behind a CHEST-HIGH iron railing (top rail 1.75 m: the cast is
#      2.3 m tall with the box head). He stands on the pavement, bowed right over the rail, his neck between the two middle bars, which are bowed apart
#      round it; his head pokes out on the terrace side, its sides squeezed by the bars. One railing model in every shot
WALLX = 10.15                                          # the wall patch of the balcony prop (5 cm in front of the block's face)
TD = 1.1                                               # the terrace's depth
RAILX = r(WALLX - (TD - 0.04))                         # the railing's plane, x 9.09
FY = 0.15; RH = 1.6; TOP = r(FY + RH)                  # the top rail at 1.75
HEADC = [r(RAILX + 0.05), 1.42, 0.0]                   # the middle of his head, just through the bars
BOWY = r((1.40 - (FY + 0.07)) / (TOP - (FY + 0.07)))   # the bars bow out round the head
MAN = [r(RAILX - 0.82), 0, 0.0]; MRY = 90              # his feet on the pavement, facing the wall (+X)
FOOT_L = [MAN[0], 0, -0.14]; FOOT_R = [MAN[0], 0, 0.14]   # (facing +X his left is -Z)
STREET = {'eiffelStyle': 'v2', 'clear': [-12.0, 12.0], 'clearL': [-6.0, 6.0]}
CRATER_ST = {'eiffelStyle': 'v2', 'z0': 10.02, 'n': 12, 'clear': [-30.0, 30.0], 'clearL': [-30.0, 30.0]}   # no block for z < 3.5: his building is gone
RAIL = lambda pid='rambarde', **o: P(pid, 'balconyRail', pos=[WALLX, 0, 0.0], ry=-90, opts={'fy': FY, 'd': TD, 'w': 2.2, 'rh': RH, 'gap': 0.115, 'ww': 5.0, 'wh': 2.9, 'bow': 0.11, 'bowY': BOWY, **o})
TRUCK_P = [2.2, 0, 3.0]
LAD = {'len': 18, 'elev': 76, 'cloudR': 4.5}
def TRUCK(pid='camion', keys=None, lopts=None, start=None):
    """the fire engine parked in the right lane, cab toward -Z, and its giant ladder from the turntable on its back, leaning toward his building"""
    p0 = start or TRUCK_P
    return [P(pid, 'fireTruck', pos=p0, ry=90, keys=keys or []),
            P(pid + '_echelle', 'skyLadder', pos=add(p0, [0, 2.0, 1.2]), ry=90, opts={**LAD, **(lopts or {})},
              keys=[dict(kk, to=add(kk['to'], [0, 2.0, 1.2])) if 'to' in kk else kk for kk in (keys or [])])]
def LBG(pid, frm, look, lens, sx=0.74, sy=0.22, d=34.0, elev=80, side=1, top=None, drift=0.25, length=None):
    """(round 1: the ladder showed in 3 shots of 17) the same truck and ladder planted far off in the camera's own view, so that the ladder rises into
    its cloud at (sx, sy) of the frame: the base d metres out along the view, the ladder leaning across the frame (side 1: to the right)"""
    f = [look[0] - frm[0], 0, look[2] - frm[2]]; n = math.hypot(f[0], f[2]); f = [f[0] / n, 0, f[2] / n]
    rt = [-f[2], 0, f[0]]
    s = (sx - 0.5) * 2 * d * math.tan(math.radians(lens) / 2) * 9 / 16
    base = [r(frm[0] + f[0] * d + rt[0] * s), 0, r(frm[2] + f[2] * d + rt[2] * s)]
    lean = rt if side > 0 else [-rt[0], 0, -rt[2]]
    ry_ = r(math.degrees(math.atan2(lean[0], lean[2])), 1)
    tb = add(base, [0.0, 2.0, 0.0])                     # the turntable over the middle of the truck (seen from far)
    def tip(L): e = math.radians(elev); return [tb[0] + lean[0] * math.cos(e) * L * 0.95, tb[1] + 0.9 + math.sin(e) * L * 0.95, tb[2] + lean[2] * math.cos(e) * L * 0.95]
    if length is None:
        lo, hi = 6.0, 70.0
        for _ in range(40):
            mid = (lo + hi) / 2; p = project(frm, look, lens, tip(mid))
            if p is None or p[1] < sy: hi = mid
            else: lo = mid
        length = r((lo + hi) / 2, 2)
    return [P(pid + '_camion', 'fireTruck', pos=base, ry=r(ry_ + 90, 1)),
            P(pid, 'skyLadder', pos=tb, ry=ry_, opts={'len': length, 'elev': elev, 'cloudR': r(4.5 * d / 34, 2), 'drift': drift, **({'top': top} if top else {})})]

def HERO(cid, keys, pos=MAN, ry=MRY, clip='stand', expr='unimpressed', **kw): return act(cid, pos, ry, clip, expr, keys=keys, **kw)
BARS = {'reach': {'L': [r(RAILX - 0.05), 1.1, -0.34, 1, 0.03], 'R': [r(RAILX - 0.05), 1.1, 0.34, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}}
TOPR = {'reach': {'L': [r(RAILX - 0.04), r(TOP + 0.03), -0.42, 1, 0.03], 'R': [r(RAILX - 0.04), r(TOP + 0.03), 0.42, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}}
HANG = {}
def STUCK(t=0.0, face=None, hands=None, spine=1.2, neck=-0.85, extra=None, dur=0.15, at=None, plant=True):
    """his pose stuck in the railing: bowed right over the rail, the head pinned between the bars (pin), the feet held on the pavement (plant), the head
    squeezed narrow; hands: BARS (gripping two bars low), TOPR (on the top rail) or HANG (left to dangle)"""
    pose = {'pin': {'joint': 'head', 'off': [0, 0.2, 0.02], 'at': at or HEADC, 'w': 1}, 'bend': {'spine': [spine, 0, 0, 1, None], 'neck': [neck, 0, 0, 1, None]},
            'scl': {'head': [0.86, 1.07, 1.0]}, 'face': face or SQUASHED, **(BARS if hands is None else hands), **(extra or {})}
    if plant: pose['plant'] = {'L': [*FOOT_L, 1], 'R': [*FOOT_R, 1]}
    return k(t, toon=pose, toonDur=0.0 if t == 0 else dur)
def BLINK(t, face=None): f = face or DEAD; return [k(t, toon={'face': {**f, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.11), toon={'face': f}, toonDur=0.06, keepPose=True)]
def IDLE(t0, t1, face=None, hands=None, every=0.62, blinks=(), darts=()):
    """(round 1: he held dead still) breathing on the stuck pose (the spine rises and sinks), a blink at each time of blinks, the pupils darting
    (gx) at each (t, gx) of darts"""
    f = face or DEAD; ks = []; t = t0; i = 0
    while t < t1 - 0.05:
        ks.append(STUCK(r(t), f, hands, spine=1.2 + (0.05 if i % 2 else -0.03), dur=every * 0.9)); t += every; i += 1
    for b in blinks: ks += BLINK(b, f)
    for (td, gx) in darts: ks.append(k(td, toon={'face': {**f, 'gx': gx}}, toonDur=0.08, keepPose=True))
    return ks

POMP = [f'pomp{i}' for i in range(1, 13)]
FIRE_HAT = lambda pid, who: P(pid, 'hardHat', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'w': 0.27, 'color': '#D9DDE2'})

for g_ in [('S05', 0.45, 'mec', 'stretch'), ('S06', 1.25, 'ministre', 'stamp'), ('S07', 0.95, 'president', 'yell'), ('S11', 0.9, 'demineur1', 'plunger'),
           ('S16', 0.9, 'grand', 'pop'), ('S17', 0.85, 'forces1', 'pin'), ('S18', 1.0, 'detective', 'seal'), ('S19', 1.05, 'guichetier', 'stamp')]:
    st.gag(*g_)
st.card('S12', 'RÉUSSI', at=0.9)
st.card('S14', 'CLASSÉE', at=1.35)
st.card('S17', 'ARRÊTÉ', at=1.0)

# 1: the hook. Tight on his head from the terrace side, low, the sky and the tops of the houses across the street behind him: the head jammed between
#    the two bowed bars, cheeks squeezed; he heaves back once (the body pulls, the head stays: a squeak), then gives up and looks at us; no ground
D1 = st.dur('S01')
C1 = [9.74, 0.8, 0.44]; L1 = [9.17, 1.44, 0.0]
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        HERO('mec', [STUCK(0.0), k(0.0, look=[8.0, 1.3, 0.0]), k(0.3, look='camera', lookDur=0.25),
             STUCK(0.5, {**SQUASHED, 'lid': 0.6, 'gx': 0.4}, dur=0.25),
             STUCK(0.86, {**SQUASHED, 'cheeks': 0.85, 'brow': 0.4, 'mouth': 'clench', 'lid': 0.2}, spine=1.0, extra={'sq': [0.96, 1.06, 0.96]}, dur=0.08),
             STUCK(1.02, {**SQUASHED, 'cheeks': 0.95, 'brow': 0.55, 'mouth': 'grimace', 'lid': 0.1}, spine=0.9, extra={'sq': [0.94, 1.1, 0.94]}, dur=0.1),
             STUCK(1.2, {**SQUASHED, 'cheeks': 0.6}, dur=0.14), STUCK(1.45, {**SQUASHED, 'lid': 0.5}, spine=1.25, dur=0.3), *BLINK(1.75, SQUASHED)])],
        props=[RAIL()],
        cams=[cam(0.0, C1, add(C1, [-0.04, 0.01, -0.03]), L1, L1, lens=58)])
chk('S01', C1, L1, 58, {'head': HEADC, 'mouth': add(HEADC, [0.12, -0.1, 0]), 'chin': add(HEADC, [0.12, -0.22, 0]), 'topRail': [RAILX, TOP, 0.0]})
st.cue('sfx:squeak', 'S01', 0.9, 0.25)

# 2: the firemen brought out the big ladder. Low on the pavement by his wall: the fire engine skids up in the right lane and stops with a dip; its
#    arm swings up and the ladder telescopes out in three jerks, the camera tilting with it, until the tip vanishes into a bank of cloud
D2 = st.dur('S02'); ARR2 = 0.45; RAISE2 = [0.5, 0.3]; STEPS2 = [0.88, 1.18, 1.48]
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[HERO('mec', [STUCK(0.0), k(0.0, look=[2.0, 2.0, 3.0])])],
        props=[RAIL(), *TRUCK(keys=[k(0.0, to=add(TRUCK_P, [0, 0, -0.35]), dur=ARR2, ease='out'), k(ARR2, to=TRUCK_P, dur=0.22, ease='inOut')],
                              lopts={'raise': RAISE2, 'raise0': 6, 'steps': STEPS2, 'cloudFrom': 0.9}, start=add(TRUCK_P, [0, 0, 14.0])),
               P('crisse2', 'toonPuff', pos=add(TRUCK_P, [0.0, 0.1, 1.6]), opts={'at': r(ARR2 - 0.1), 'n': 6, 'size': 0.35, 'life': 0.7, 'rise': 0.5, 'spread': 0.9, 'color': '#D9D2C4'})],
        cams=[cam(0.0, [7.4, 0.9, -4.8], [7.2, 1.1, -4.6], [2.8, 2.0, 2.4], [4.4, 14.0, 5.0], lens=56, ease='inOut')])
st.cue('sfx:brake', 'S02', 0.1, 0.4); st.cue('sfx:rattle', 'S02', STEPS2[0], 0.35); st.cue('sfx:rattle', 'S02', STEPS2[1], 0.3); st.cue('sfx:rattle', 'S02', STEPS2[2], 0.3)

# 3: he lives on the ground floor. Wide and low from across the road: the terrace is a step at pavement level; he is bowed over its chest-high railing,
#    head through the bars, a metre from two firemen who look up at their ladder, which towers into the clouds over the whole building for nothing
D3 = st.dur('S03')
F3 = [('pomp1', [7.4, 0, 1.2]), ('pomp2', [6.75, 0, 2.1])]
C3 = [-4.6, 1.0, -15.0]; L3 = [7.6, 6.6, 1.6]
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        HERO('mec', [k(0.0, look=[11.0, 1.4, 0.0]), *IDLE(0.0, D3, SQUASHED, blinks=(0.75,), darts=((0.35, -0.5), (0.95, 0.0)))]),
        *[act(w, p, yaw(p, [9.0, 0, 3.6]), 'stand', 'neutral', keys=[k(0.0, look=[7.0, 30.0, 4.0]), k(r(0.45 + 0.2 * j), look=[7.0, 14.0, 4.0], lookDur=0.3), k(r(0.75 + 0.15 * j), look=HEADC, lookDur=0.25)]) for j, (w, p) in enumerate(F3)]],
        props=[RAIL(), *TRUCK(), *[FIRE_HAT(f'casque3{j}', w) for j, (w, _) in enumerate(F3)]],
        cams=[cam(0.0, C3, add(C3, [0.15, 0.0, 0.3]), L3, add(L3, [0, 0.15, 0]), lens=64)])
chk('S03', C3, L3, 64, {'head': HEADC, 'feet': MAN, 'railTop': [RAILX, TOP, 0.8], 'pomp1': [7.4, 2.3, 1.2], 'cloud': [6.42, 19.8, 4.2], 'tip15': [5.5, 15.0, 4.2]})
st.cue('sfx:wind', 'S03', 0.0, 0.2)

# 4: twelve firemen pulled his legs. From the terrace, past his strained face in the bars: his body lifted horizontal behind him by the legs, and
#    twelve firemen in a row along a hose tied to his ankles lean back and heave like a tug of war, faces to us, each on his own beat
D4 = st.dur('S04'); LIFT4 = [0.05, 0.4]
ANK4 = [r(HEADC[0] - 2.3), 1.38, 0.0]
ROPE_END = [-0.5, 1.12, 0.0]
def rope_pt(u): return [r(ANK4[i] + (ROPE_END[i] - ANK4[i]) * u) for i in range(3)]
ROPE_RZ = r(-(PI / 2 - math.atan2(ANK4[1] - ROPE_END[1], ANK4[0] - ROPE_END[0])), 3)
LEAN = [0.3, 0.38, 0.26, 0.42, 0.33, 0.24, 0.4, 0.3, 0.36, 0.28, 0.44, 0.32]
BEAT = [0.0, 0.06, 0.13, 0.03, 0.1, 0.17, 0.08, 0.02, 0.14, 0.05, 0.11, 0.19]
def pull_pos(j): u = (j + 0.5) / 12; hp = rope_pt(u); return hp, [r(hp[0] - 0.36), 0, r(0.3 * (1 if j % 2 else -1))]
def PULLER(j, who):
    hp, p = pull_pos(j); a = LEAN[j]
    grip = {'reach': {'R': [*add(hp, [0.08, 0, 0]), 1, 0.03], 'L': [*add(hp, [-0.12, 0, 0]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}}
    ks = [k(0.0, look=HEADC), k(0.0, toon={**grip, 'lay': [r(-0.5 * a), 0], 'bend': {'spine': [r(-0.4 * a), 0, 0, 1, None]}, 'face': {'mouth': 'clench', 'brow': -0.6, 'lid': 0.2}}, toonDur=0.0)]
    for t in (0.5, 1.0, 1.45):
        t0 = r(t + BEAT[j])
        ks += [k(t0, toon={**grip, 'lay': [r(-a), 0], 'bend': {'spine': [r(-0.9 * a), 0, 0, 1, None]}, 'sq': [1.05, 0.94, 1.05], 'face': {'mouth': 'grimace' if j % 3 else 'teeth', 'brow': -0.8, 'lid': 0.55}}, toonDur=0.12, toonEase='out'),
               k(r(t0 + 0.22), toon={**grip, 'lay': [r(-0.55 * a), 0], 'bend': {'spine': [r(-0.45 * a), 0, 0, 1, None]}, 'sq': [1, 1, 1], 'face': {'mouth': 'clench', 'brow': -0.6, 'lid': 0.2}}, toonDur=0.2)]
    return act(who, p, 90, 'stand', 'angry', keys=ks)
def HORIZ(t, k_=1.0, sq=(1, 1, 1), face=None, dur=0.3, hands=None):
    """him lifted horizontal by the legs, the head pinned in the bars: tipped forward about his feet, the neck bent back so the face stays on us; his
    hands clutch the bars beside his head"""
    hh = hands if hands is not None else {'reach': {'L': [r(RAILX - 0.06), 1.28, -0.28, 1, 0.03], 'R': [r(RAILX - 0.06), 1.28, 0.28, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'}}
    return k(t, toon={'pin': {'joint': 'head', 'off': [0, 0.2, 0.02], 'at': HEADC, 'w': 1}, 'lay': [r(PI / 2 * k_), 0], 'bend': {'neck': [r(-1.3 * k_), 0, 0, 1, None]},
                      'scl': {'head': [0.86, 1.07, 1.0]}, 'sq': list(sq), 'face': face or {**SQUASHED, 'cheeks': 0.85, 'brow': 0.35, 'lid': 0.3, 'mouth': 'clench'}, **hh}, toonDur=dur, toonEase='inOut')
C4 = [10.02, 1.92, 0.62]; L4 = [6.2, 1.02, -0.22]
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        HERO('mec', [STUCK(0.0), k(0.0, look='camera'), HORIZ(LIFT4[0], 0.15, dur=0.05), HORIZ(LIFT4[1], 1.0, dur=LIFT4[1] - LIFT4[0]),
             HORIZ(0.6, 1.0, (0.97, 1.07, 0.97), dur=0.1), HORIZ(0.82, 1.0, dur=0.15), HORIZ(1.1, 1.0, (0.96, 1.1, 0.96), dur=0.1), HORIZ(1.3, 1.0, dur=0.15),
             HORIZ(1.55, 1.0, (0.95, 1.13, 0.95), {**SQUASHED, 'cheeks': 0.95, 'brow': 0.55, 'lid': 0.6, 'mouth': 'grimace'}, dur=0.1)]),
        *[PULLER(j, w) for j, w in enumerate(POMP)]],
        props=[RAIL(), *TRUCK(), *[FIRE_HAT(f'casque4{j}', w) for j, w in enumerate(POMP)],
               P('tuyau4', 'rope', pos=ANK4, rot=[0, 0, ROPE_RZ], opts={'len': r(math.dist(ANK4, ROPE_END)), 'r': 0.045, 'color': '#C8322A', 'sway': 0.0})],
        cams=[cam(0.0, C4, add(C4, [0.0, 0.03, 0.04]), L4, L4, lens=56)])
chk('S04', C4, L4, 56, {'head': HEADC, 'ankles': ANK4, 'pomp1': pull_pos(0)[1], 'pomp12': add(pull_pos(11)[1], [0, 2.1, 0]), 'cloud': [6.42, 19.8, 4.2]})
for j_, t_ in enumerate((0.5, 1.0, 1.45)): st.cue('sfx:grunt', 'S04', t_, 0.3)

# 5: he grew twenty centimetres. From the side and above: they heave, his body stretches like elastic and holds stretched while the head stays in the
#    bars; the hose snaps, the twelve fall flat on their backs one after the other like dominoes; he hangs a beat in the air, drops onto his feet with
#    a squash and settles, visibly taller
D5 = st.dur('S05'); STR5 = 0.42; SNAP5 = 0.75; HANG5 = 0.86; DROP5 = 1.0; LAND5 = 1.14
def FALLER(j, who):
    hp, p = pull_pos(j); a = LEAN[j]; tf = r(SNAP5 + 0.035 * j)
    grip = {'reach': {'R': [*add(hp, [0.08, 0, 0]), 1, 0.03], 'L': [*add(hp, [-0.12, 0, 0]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}}
    return act(who, p, 90, 'stand', 'angry', keys=[k(0.0, look=HEADC),
        k(0.0, toon={**grip, 'lay': [r(-a), 0], 'bend': {'spine': [r(-0.9 * a), 0, 0, 1, None]}, 'face': {'mouth': 'grimace', 'brow': -0.8, 'lid': 0.5}}, toonDur=0.0),
        k(r(STR5 + 0.02 * j), toon={**grip, 'lay': [r(-a - 0.12), 0], 'bend': {'spine': [r(-a), 0, 0, 1, None]}, 'face': {'mouth': 'grimace', 'brow': -0.9, 'lid': 0.65}}, toonDur=0.12),
        k(tf, toon={'lay': [-1.52, 0], 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'sq': [1.1, 0.9, 1.1], 'face': {'pop': 0.5, 'mouth': 'O', 'brow': 0.8, 'lid': 0.0}}, toonDur=0.2, toonEase='in'),
        k(r(tf + 0.24), toon={'lay': [-1.45, 0], 'bend': {'spine': [0.0, 0, 0, 1, None]}, 'sq': [1.0, 1.0, 1.0], 'face': {'pop': 0.2, 'mouth': 'O', 'brow': 0.6, 'lid': 0.1}}, toonDur=0.08),
        k(r(tf + 0.34), toon={'lay': [-1.52, 0], 'face': {'mouth': 'wavy', 'brow': 0.4, 'lid': 0.5, 'stars': 0.6}}, toonDur=0.1)])
STRETCHED = {**SQUASHED, 'pop': 0.5, 'mouth': 'O', 'cheeks': 0.9, 'brow': 0.7, 'lid': 0.0}
C5 = [9.75, 2.9, 4.8]; L5 = [6.8, 1.0, -0.45]
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        HERO('mec', [k(0.0, look='camera'), HORIZ(0.0, 1.0, (0.95, 1.13, 0.95), dur=0.0),
             HORIZ(0.25, 1.0, (0.86, 1.36, 0.86), dur=0.15), HORIZ(STR5, 1.0, (0.78, 1.62, 0.78), STRETCHED, dur=0.12), HORIZ(r(SNAP5 - 0.02), 1.0, (0.77, 1.65, 0.77), STRETCHED, dur=0.3),
             HORIZ(r(SNAP5 + 0.06), 1.0, (1.08, 0.86, 1.08), {**STRETCHED, 'pop': 0.2}, dur=0.06), HORIZ(HANG5, 1.0, (0.97, 1.08, 0.97), {**SQUASHED, 'brow': 0.6, 'lid': 0.0}, dur=0.08),
             HORIZ(DROP5, 0.95, (0.97, 1.08, 0.97), {**SQUASHED, 'brow': 0.6, 'lid': 0.0}, dur=0.14),
             STUCK(LAND5, {**SQUASHED, 'lid': 0.2, 'brow': 0.4}, extra={'sq': [1.12, 0.86, 1.12]}, dur=0.14),
             STUCK(r(LAND5 + 0.12), {**SQUASHED, 'lid': 0.3}, extra={'sq': [0.95, 1.11, 0.95]}, dur=0.08),
             STUCK(r(LAND5 + 0.26), DEAD, extra={'sq': [0.96, 1.09, 0.96]}, dur=0.12)]),
        *[FALLER(j, w) for j, w in enumerate(POMP)]],
        props=[RAIL(), *TRUCK(), *[FIRE_HAT(f'casque5{j}', w) for j, w in enumerate(POMP)],
               P('tuyau5', 'rope', pos=ANK4, rot=[0, 0, ROPE_RZ], opts={'len': r(math.dist(ANK4, ROPE_END)), 'r': 0.045, 'color': '#C8322A', 'sway': 0.0}, keys=[k(SNAP5, visible=False)]),
               P('tuyau5b', 'rope', pos=add(ROPE_END, [2.5, 0.0, 0]), rot=[0, 0, -1.25], opts={'len': 3.0, 'r': 0.045, 'color': '#C8322A', 'sway': 0.12}, keys=[k(0.0, visible=False), k(SNAP5, visible=True)]),
               P('choc5', 'burstLines', pos=add(ANK4, [0.1, 0.0, 0.0]), ry=0, opts={'at': SNAP5, 'n': 8, 'r0': 0.15, 'r1': 0.55, 'len': 0.18, 'w': 0.03}),
               *LBG('echelle5', C5, L5, 56, sx=0.2, sy=0.12, d=30, side=-1)],
        fx=[{'type': 'shake', 'at': SNAP5, 'dur': 0.15, 'amount': 0.012}],
        cams=[cam(0.0, C5, add(C5, [-0.05, -0.05, -0.08]), L5, L5, lens=56)])
chk('S05', C5, L5, 56, {'head': HEADC, 'ankles': ANK4, 'stretched': [5.6, 1.4, 0], 'pomp1': pull_pos(0)[1], 'pomp12': pull_pos(11)[1]})
st.cue('sfx:stretch', 'S05', 0.25, 0.35); st.cue('sfx:boing', 'S05', SNAP5, 0.35); st.cue('thud', 'S05', r(SNAP5 + 0.3), 0.4); st.cue('thud', 'S05', LAND5, 0.35)

# 6: the railing was declared a natural disaster. From the terrace, past his face poking through the taped bars: behind him on the pavement a minister in
#    a white hard hat at a podium raises a giant rubber stamp and slams it onto the top rail beside his head: stars; he flinches, his eyes dart to it
D6 = st.dur('S06'); HIT6 = 1.25
MIN6 = [8.3, 0, 1.12]; MRY6 = yaw(MIN6, [9.1, 0, 0.42])
STAMP_TOP = [RAILX, TOP, 0.44]
def MK6(t, p, sq=(1, 1, 1), face=None, dur=0.12, ease='inOut', bend=0.0):
    return k(t, toon={'reach': {'R': [*p, 1, 0.05], 'L': [*off(MIN6, MRY6, 0.3, -0.2, 1.12), 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': list(sq), 'bend': {'spine': [bend, 0, 0, 1, None]},
                      'face': face or {'lid': 0.3, 'mouth': 'line', 'brow': -0.4}}, toonDur=dur, toonEase=ease)
C6 = [10.0, 1.3, -1.12]; L6 = [8.75, 1.66, 0.45]
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        HERO('grand', [STUCK(0.0, DEAD), k(0.0, look='camera'), *BLINK(0.55),
             STUCK(r(HIT6 + 0.02), {**DEAD, 'lid': 0.95, 'cheeks': 0.7, 'brow': 0.3}, extra={'sq': [1.04, 0.95, 1.04]}, dur=0.04),
             k(r(HIT6 + 0.12), toon={'face': {**DEAD, 'lid': 0.0, 'gx': 0.9, 'gy': -0.6, 'brow': 0.35}}, toonDur=0.06, keepPose=True),
             STUCK(r(HIT6 + 0.3), {**DEAD, 'gx': 0.9, 'gy': -0.6}, dur=0.15),
             k(r(HIT6 + 0.75), toon={'face': {**DEAD, 'gx': 0.0, 'gy': 0.0}}, toonDur=0.12, keepPose=True)]),
        act('ministre', MIN6, MRY6, 'stand', 'neutral', keys=[k(0.0, look=STAMP_TOP),
            MK6(0.0, off(MIN6, MRY6, 0.35, 0.25, 1.2), dur=0.0), MK6(0.45, off(MIN6, MRY6, 0.3, 0.25, 2.55), (0.94, 1.1, 0.94), {'lid': 0.1, 'mouth': 'clench', 'brow': -0.7}, 0.3, 'out', -0.1),
            MK6(r(HIT6 - 0.12), off(MIN6, MRY6, 0.32, 0.25, 2.65), (0.92, 1.12, 0.92), {'lid': 0.05, 'mouth': 'clench', 'brow': -0.8}, 0.1),
            MK6(HIT6, add(STAMP_TOP, [-0.08, 0.3, 0.0]), (1.12, 0.88, 1.12), {'lid': 0.0, 'mouth': 'clench', 'brow': -0.9, 'pop': 0.3}, 0.06, 'in', 0.25),
            MK6(r(HIT6 + 0.2), add(STAMP_TOP, [-0.1, 0.36, 0.0]), (0.97, 1.04, 0.97), {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, 0.15, bend=0.12),
            k(r(HIT6 + 0.45), look='camera', lookDur=0.15)])],
        props=[RAIL(tape=True), P('casque6', 'hardHat', on={'actor': 'ministre', 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}),
               P('pupitre6', 'podium', pos=off(MIN6, MRY6, -0.6, -0.6, 0.0), ry=MRY6),
               P('tampon6', 'rubberStamp', on={'actor': 'ministre', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'rot': [PI, 0, 0]}, scale=5.0, opts={'color': '#C23A2E'}),
               P('marque6', 'stampMark', pos=add(STAMP_TOP, [0.06, -0.26, 0.0]), ry=90, opts={'text': 'CATASTROPHE'}, scale=1.6, keys=[k(0.0, visible=False), k(HIT6, visible=True)]),
               P('etoiles6', 'impactStars', pos=add(STAMP_TOP, [0.05, 0.15, 0.0]), ry=90, opts={'at': HIT6, 'n': 6, 'r': 0.45}),
               *LBG('echelle6', C6, L6, 54, sx=0.25, sy=0.16, d=36, side=-1)],
        fx=[{'type': 'shake', 'at': HIT6, 'dur': 0.15, 'amount': 0.012}],
        cams=[cam(0.0, C6, add(C6, [0.0, 0.0, 0.05]), L6, L6, lens=54)])
chk('S06', C6, L6, 54, {'head': HEADC, 'stamp': STAMP_TOP, 'minHead': add(MIN6, [0, 2.1, 0]), 'stampUp': off(MIN6, MRY6, 0.3, 0.25, 2.65)})
st.cue('whoosh', 'S06', 0.45, 0.2); st.cue('thud', 'S06', HIT6, 0.55)

# 7: the president ordered the head to come out. From the end of the terrace, low, the sky down the street behind them: on the terrace the president
#    (sash) bends nose to nose with the head through the bars, raises a megaphone and bellows: the bars ring like a tuning fork, his cheeks ripple and
#    his hair blows back, shock lines burst from the horn
D7 = st.dur('S07'); UP7 = 0.6; YELL7 = 0.95
PHEAD7 = [9.86, 1.66, 0.04]
PRES7 = [10.02, 0.22, 0.06]; PRY7 = -90
MEGA7 = [9.58, 1.56, 0.17]
C7 = [9.44, 1.08, 2.25]; L7 = [9.5, 1.56, 0.0]
WIND = lambda w: {'wind': [0, 0, w]}
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        HERO('grand', [STUCK(0.0, DEAD), k(0.0, look=PHEAD7),
             STUCK(YELL7, {**DEAD, 'lid': 0.65, 'cheeks': 0.95}, extra={'buzz': 0.006, **WIND(-9)}, dur=0.05),
             *[STUCK(r(YELL7 + 0.07 * i), {**DEAD, 'lid': 0.65, 'cheeks': 0.35 if i % 2 else 0.95, 'mouthW': 0.1 if i % 2 else -0.15}, extra={'buzz': 0.006, **WIND(-9)}, dur=0.05) for i in range(1, 9)],
             STUCK(r(YELL7 + 0.75), {**DEAD, 'lid': 0.5}, extra={'buzz': 0.0, **WIND(0)}, dur=0.25), *BLINK(2.15)]),
        act('president', PRES7, PRY7, 'stand', 'angry', keys=[k(0.0, look=add(HEADC, [0.1, 0.05, 0])),
            k(0.0, toon={'pin': {'joint': 'head', 'off': [0, 0.2, 0.02], 'at': PHEAD7, 'w': 1}, 'plant': {'L': [10.0, 0.22, 0.2, 1], 'R': [10.0, 0.22, -0.08, 1]}, 'bend': {'spine': [0.95, 0, 0, 1, None], 'neck': [-0.6, 0, 0, 1, None]},
                         'reach': {'R': [10.0, 1.05, -0.12, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.5}}, toonDur=0.0),
            k(UP7, toon={'pin': {'joint': 'head', 'off': [0, 0.2, 0.02], 'at': add(PHEAD7, [0.05, 0.04, 0]), 'w': 1}, 'plant': {'L': [10.0, 0.22, 0.2, 1], 'R': [10.0, 0.22, -0.08, 1]}, 'bend': {'spine': [0.85, 0, 0, 1, None], 'neck': [-0.55, 0, 0, 1, None]},
                         'reach': {'R': [*MEGA7, 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.2, 'mouth': 'line', 'brow': -0.7, 'puff': 0.8}}, toonDur=0.3, toonEase='out'),
            k(YELL7, toon={'pin': {'joint': 'head', 'off': [0, 0.2, 0.02], 'at': add(PHEAD7, [-0.05, -0.02, 0]), 'w': 1}, 'plant': {'L': [10.0, 0.22, 0.2, 1], 'R': [10.0, 0.22, -0.08, 1]}, 'bend': {'spine': [1.0, 0, 0, 1, None], 'neck': [-0.6, 0, 0, 1, None]},
                         'reach': {'R': [*add(MEGA7, [-0.06, 0, 0]), 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [1.05, 0.96, 1.05], 'face': {'lid': 0.0, 'mouth': 'scream', 'brow': -0.9, 'vein': 0.8}}, toonDur=0.06, toonEase='out'),
            k(r(YELL7 + 0.9), toon={'pin': {'joint': 'head', 'off': [0, 0.2, 0.02], 'at': add(PHEAD7, [-0.04, -0.02, 0]), 'w': 1}, 'plant': {'L': [10.0, 0.22, 0.2, 1], 'R': [10.0, 0.22, -0.08, 1]}, 'bend': {'spine': [1.0, 0, 0, 1, None], 'neck': [-0.6, 0, 0, 1, None]},
                         'reach': {'R': [*add(MEGA7, [-0.05, 0, 0]), 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.1, 'mouth': 'scream', 'brow': -0.9, 'vein': 0.6}}, toonDur=0.3),
            k(r(YELL7 + 1.2), toon={'pin': {'joint': 'head', 'off': [0, 0.2, 0.02], 'at': PHEAD7, 'w': 1}, 'plant': {'L': [10.0, 0.22, 0.2, 1], 'R': [10.0, 0.22, -0.08, 1]}, 'bend': {'spine': [0.95, 0, 0, 1, None], 'neck': [-0.6, 0, 0, 1, None]},
                         'reach': {'R': [*MEGA7, 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.2)])],
        props=[RAIL(tape=True, quiver=[YELL7, 0.6, 0.14, 47]), P('megaphone7', 'megaphone', on={'actor': 'president', 'hand': 'R', 'offset': [0.0, 0.02, 0.06]}, scale=1.25),
               P('choc7', 'burstLines', pos=[9.43, 1.56, 0.12], ry=90, opts={'at': YELL7, 'n': 7, 'r0': 0.12, 'r1': 0.38, 'len': 0.14, 'w': 0.022, 'every': 0.2, 'until': r(YELL7 + 0.9)}),
               *LBG('echelle7', C7, L7, 48, sx=0.3, sy=0.14, d=40, side=-1)],
        cams=[cam(0.0, C7, add(C7, [0.0, 0.02, -0.06]), L7, L7, lens=48)])
chk('S07', C7, L7, 48, {'head': HEADC, 'pres': PHEAD7, 'mega': MEGA7, 'bar0': [RAILX, 1.4, 0.06], 'bar1': [RAILX, 1.4, 0.3]})
st.cue('sfx:siren', 'S07', YELL7, 0.45); st.cue('sfx:ring', 'S07', r(YELL7 + 0.05), 0.35)

# 8: the head held its ground. Locked camera, tight on the clean head in the bars from the terrace: it has not moved a millimetre and stares back
#    deadpan; one blink; the megaphone droops slowly down through the edge of the frame
D8 = st.dur('S08')
C8 = [9.84, 1.5, -0.34]; L8 = [9.16, 1.43, 0.02]
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[HERO('grand', [STUCK(0.0, DEAD), k(0.0, look='camera'), *BLINK(0.95)])],
        props=[RAIL(tape=True), P('megaphone8', 'megaphone', pos=[9.58, 1.74, -0.08], rot=[-0.25, 1.2, 0.0], scale=1.25,
                                   keys=[k(0.3, to=[9.6, 1.12, -0.12], dur=1.4, ease='inOut'), k(0.3, rotTo=[0.9, 1.25, 0.1], dur=1.4, ease='inOut')]),
               *LBG('echelle8', C8, L8, 46, sx=0.2, sy=0.12, d=40, side=-1)],
        cams=[cam(0.0, C8, C8, L8, L8, lens=46)])
chk('S08', C8, L8, 46, {'head': HEADC, 'mega0': [9.58, 1.74, -0.08], 'mega1': [9.6, 1.12, -0.12]})
st.cue('sfx:wind', 'S08', 0.0, 0.15)

# 9: the district was evacuated by helicopter. Low in the road looking up the street: helicopters hover over the roofs, searchlights on, and winch the
#    residents up on cables from their balconies, one still sitting in her armchair; the fire ladder still rises into its cloud behind them
D9 = st.dur('S09')
RES9 = [('mamie', [9.55, 6.8, 9.5], 'armchair'), ('voisin1', [9.5, 9.6, 14.0], 'hang'), ('voisin2', [9.5, 8.4, 19.0], 'hang')]
HELI9 = [[8.6, 19.0, 9.5], [6.2, 21.5, 14.0], [8.2, 20.0, 19.0]]
RISE9 = 3.2
C9 = [5.6, 5.4, 3.2]; L9 = [9.4, 9.2, 10.5]
acts9, props9 = [], []
for j, ((who, p, kind), hp) in enumerate(zip(RES9, HELI9)):
    up = add(p, [0, RISE9, 0])
    if kind == 'armchair':
        acts9.append(act(who, add(p, [0, 0.03, 0]), -90 if p[0] > 0 else 90, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, to=add(up, [0, 0.03, 0]), dur=D9, ease='linear', face='keep')]))
        props9.append(P(f'fauteuil9{j}', 'armchair', pos=p, ry=-90 if p[0] > 0 else 90, opts={'color': '#B5523A'}, keys=[k(0.0, to=up, dur=D9, ease='linear')]))
        props9.append(P(f'cable9{j}', 'winchCable', pos=add(p, [0, 1.95, 0]), opts={'len': r(hp[1] - p[1] - 1.95 - 0.6)}, keys=[k(0.0, to=add(up, [0, 1.95, 0]), dur=D9, ease='linear')]))
    else:
        acts9.append(act(who, p, -90 if p[0] > 0 else 90, 'hangBar', 'scared', keys=[k(0.0, look=hp), k(0.0, to=up, dur=D9, ease='linear', face='keep')]))
        props9.append(P(f'cable9{j}', 'winchCable', pos=add(p, [0, 2.55, 0]), opts={'len': r(hp[1] - p[1] - 2.55 - 0.6)}, keys=[k(0.0, to=add(up, [0, 2.55, 0]), dur=D9, ease='linear')]))
    props9.append(P(f'heli9{j}', 'helicopter', pos=hp, ry=0 if j != 1 else 150, opts={'beam': j == 0, 'tilt': 10}, keys=[k(0.0, to=add(hp, [0, RISE9, 0]), dur=D9, ease='linear')]))
st.shot('S09', 'parisStreet', setOpts=STREET, actors=acts9, props=[RAIL(tape=True), *props9, *LBG('echelle9', C9, L9, 52, sx=0.2, sy=0.2, d=44, side=-1, top='fireman')],
        cams=[cam(0.0, C9, add(C9, [0.02, 0.1, 0.15]), L9, add(L9, [0, 1.4, 0]), lens=52)])
chk('S09', C9, L9, 52, {'mamie': RES9[0][1], 'heli0': HELI9[0]})
st.cue('sfx:rotor', 'S09', 0.0, 0.45)

# 10: except him. Dusk on the same street, from the far pavement, low: him alone bowed over his railing, mid-frame; the last helicopter flies off
#     across the frame from the first frame; the giant ladder still up into its cloud, dark against the evening sky
D10 = st.dur('S10')
DUSK = {**STREET, 'sky': ['#3B3F72', '#E9A06E'], 'clouds': 4}
C10 = [2.6, 0.75, -4.6]; L10 = [8.9, 1.55, 0.3]
st.shot('S10', 'parisStreet', setOpts=DUSK, actors=[HERO('grand', [k(0.0, look=[11.0, 1.4, 0.0]), *IDLE(0.0, D10, DEAD, hands=HANG, every=0.4, darts=((0.3, -0.6),)), k(0.45, look='camera', lookDur=0.25)])],
        props=[RAIL(tape=True), P('heli10', 'helicopter', pos=[7.0, 5.2, 1.6], ry=-120, opts={'beam': False}, keys=[k(0.0, to=[1.5, 7.4, -3.0], dur=D10, ease='in')]),
               *LBG('echelle10', C10, L10, 56, sx=0.72, sy=0.16, d=30, side=1)],
        grade='brightness(0.8) contrast(1.05) saturate(0.9) sepia(0.28) hue-rotate(-12deg)',
        cams=[cam(0.0, C10, add(C10, [0.08, 0.0, 0.1]), L10, L10, lens=56)])
chk('S10', C10, L10, 56, {'head': HEADC, 'feet': MAN, 'heli0': [7.0, 5.2, 1.6], 'heli1': [1.5, 7.4, -3.0]})
st.cue('sfx:rotor', 'S10', 0.0, 0.25)

# ---- (round 1) after the blast: his block is gone and leaves a 5 m gap between two Haussmann neighbours (the near one of parisStreet's z0 row, which
#      starts at z 3.5, and NEIGH, which ends at z -1.5); the stub of his terrace and the blackened railing stand in it
NEIGHS = [P(f'immeubleD{j}', 'haussmann', pos=[10.2, 0, z], ry=-90, opts={'color': c, 'awning': a, 'h': h, 'floors': 6, 'cols': 5, 'w': 13.04, 'seed': 70 + j})
          for j, (z, c, a, h) in enumerate([(-8.0, '#F3E9C9', '#C9822E', 16), (-21.04, '#E2EAF0', '#B5302A', 17), (-34.08, '#EFE6D2', '#2F5E8C', 16)])]
LEFTS = [P(f'immeubleG{j}', 'haussmann', pos=[-10.2, 0, z], ry=90, opts={'color': c, 'awning': a, 'h': h, 'floors': 6, 'cols': 5, 'w': 13.04, 'seed': 60 + j})
         for j, (z, c, a, h) in enumerate([(2.0, '#F2DCCB', '#2F7F5C', 17), (-11.0, '#E8E1EE', '#2F5E8C', 16), (-24.0, '#EFE6D2', '#B5302A', 18)])]
CRATER = P('cratere', 'craterPit', pos=[14.5, 0, 1.0], opts={'r': 4.4, 'seed': 41})
RUIN = lambda pid='rambarde', **o: RAIL(pid, ruin=True, char=True, **o)
SOOT = lambda pid, who='grand': P(pid, 'sootPatches', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
WISP = lambda pid, who='grand': P(pid, 'smokeRibbon', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'pts': [[0, 0, 0], [0.05, 0.35, 0.0], [-0.06, 0.8, 0.02], [0.04, 1.3, 0.0]], 'n': 12, 's0': 0.03, 's1': 0.09, 'speed': 0.4, 'shrink': False, 'color': '#8A8580'})
SUNX = {'dir': [9.0, 11.0, 4.0]}                       # (round 1) the key light from the crater side, so his face (to +X) is lit

# 11: the bomb squad blew up the building. Low behind a line of riot police and their shields: two bomb-squad officers in padded suits by the
#     detonator; one pushes the plunger down: his building goes up in a giant fireball, its front blown out in flying bricks, the shields jolt
D11 = st.dur('S11'); PUSH11 = 0.9; BOOM11 = 1.02
DEM1 = [4.6, 0, -3.1]; DEM2 = [5.3, 0, -3.6]
DET11 = off(DEM1, 60, 0.45, 0.0, 0.0)
COPS11 = [('flic1', [3.4, 0, -2.0]), ('flic2', [4.3, 0, -1.25]), ('flic3', [5.25, 0, -0.55])]
C11 = [-1.2, 1.3, -7.6]; L11 = [8.8, 5.6, 0.5]
HOUSE = P('maison11', 'haussmann', pos=[10.2, 0, 1.01], ry=-90, opts={'color': '#EFE6D2', 'awning': '#2F7F5C', 'h': 17, 'floors': 6, 'cols': 2, 'w': 4.96, 'seed': 64},
          keys=[k(r(BOOM11 + 0.1), visible=False)])
st.shot('S11', 'parisStreet', setOpts=CRATER_ST, actors=[
        act('demineur1', DEM1, 60, 'stand', 'neutral', keys=[k(0.0, look=add(DET11, [0, 0.3, 0])),
            k(0.0, toon={'reach': {'R': [*add(DET11, [0.0, 0.66, 0.06]), 1, 0.03], 'L': [*add(DET11, [0.0, 0.66, -0.06]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}}, toonDur=0.0),
            k(r(PUSH11 - 0.15), toon={'reach': {'R': [*add(DET11, [0.0, 0.74, 0.06]), 1, 0.03], 'L': [*add(DET11, [0.0, 0.74, -0.06]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [0.95, 1.05, 0.95]}, toonDur=0.12),
            k(PUSH11, toon={'reach': {'R': [*add(DET11, [0.0, 0.38, 0.06]), 1, 0.03], 'L': [*add(DET11, [0.0, 0.38, -0.06]), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.6, 0, 0, 1, None]}, 'sq': [1.08, 0.93, 1.08]}, toonDur=0.08, toonEase='in'),
            k(r(BOOM11 + 0.05), look=[12.0, 8.0, 0.0], lookDur=0.1)]),
        act('demineur2', DEM2, 50, 'stand', 'neutral', keys=[k(0.0, look=[12.0, 6.0, 0.0]),
            k(0.0, toon={'reach': {'R': [*off(DEM2, 50, 0.3, 0.25, 1.95), 1, 0.04]}, 'hands': {'R': 'thumbUp'}}, toonDur=0.0),
            k(BOOM11, toon={'reach': {'R': [*off(DEM2, 50, 0.3, 0.25, 1.95), 1, 0.04]}, 'hands': {'R': 'thumbUp'}, 'sq': [1.08, 0.92, 1.08], 'lay': [-0.15, 0]}, toonDur=0.06, toonEase='out'),
            k(r(BOOM11 + 0.25), toon={'reach': {'R': [*off(DEM2, 50, 0.3, 0.25, 1.95), 1, 0.04]}, 'hands': {'R': 'thumbUp'}, 'sq': [1, 1, 1], 'lay': [0, 0]}, toonDur=0.2)]),
        *[act(w, p, 90, 'stand', 'neutral', keys=[k(0.0, look=[12.0, 2.0, p[2]]), k(0.0, toon={'reach': {'L': [*off(p, 90, 0.42, -0.12, 1.25), 1, 0.04]}, 'hands': {'L': 'grip'}}, toonDur=0.0),
              k(r(BOOM11 + 0.04 * j), to=add(p, [-0.25, 0, 0]), dur=0.12, ease='out', face='keep'), k(r(BOOM11 + 0.3 + 0.04 * j), to=add(p, [-0.15, 0, 0]), dur=0.3, face='keep')]) for j, (w, p) in enumerate(COPS11)]],
        props=[RAIL(tape=True), HOUSE, *NEIGHS, P('detonateur11', 'detonator', pos=DET11, ry=60, opts={'pushAt': PUSH11, 'wire': 6.5}),
               P('casqueD1', 'bombHelmet', on={'actor': 'demineur1', 'joint': 'head', 'offset': [0.0, 0.02, 0.0]}), P('casqueD2', 'bombHelmet', on={'actor': 'demineur2', 'joint': 'head', 'offset': [0.0, 0.02, 0.0]}),
               P('gilet1', 'bombVest', on={'actor': 'demineur1', 'joint': 'torso', 'offset': [0.0, 0.35, 0.0]}), P('gilet2', 'bombVest', on={'actor': 'demineur2', 'joint': 'torso', 'offset': [0.0, 0.35, 0.0]}),
               *[P(f'bouclier11{j}', 'riotShield', on={'actor': w, 'hand': 'L', 'offset': [0.0, -0.1, 0.12]}, opts={'w': 0.55, 'h': 1.05}) for j, (w, _) in enumerate(COPS11)],
               *[P(f'casqueF11{j}', 'hardHat', on={'actor': w, 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'w': 0.28, 'color': '#1E2D4A'}) for j, (w, _) in enumerate(COPS11)],
               P('boum11', 'fireball', pos=[12.0, 7.5, 1.0], opts={'t0': BOOM11, 'size': 6.5, 'n': 34}),
               P('briques11', 'brickBurst', pos=[10.1, 6.5, 1.0], ry=-90, opts={'at': r(BOOM11 + 0.04), 'n': 34, 'floor': 6.5, 'speed': 8, 'spread': 1.8}),
               P('briques11b', 'brickBurst', pos=[10.1, 2.8, 1.0], ry=-90, opts={'at': r(BOOM11 + 0.02), 'n': 22, 'floor': 2.8, 'speed': 6, 'spread': 1.4}),
               P('eclair11', 'timedBurst', pos=[10.4, 5.0, 1.0], ry=-90, opts={'at': BOOM11, 'size': 4.5, 'life': 0.5}),
               *LBG('echelle11', C11, L11, 62, sx=0.18, sy=0.14, d=40, side=-1)],
        fx=[{'type': 'shake', 'at': BOOM11, 'dur': 0.4, 'amount': 0.025}],
        cams=[cam(0.0, C11, add(C11, [0.15, 0.02, 0.2]), L11, add(L11, [0, 0.6, 0]), lens=62)])
chk('S11', C11, L11, 62, {'house': [10.2, 8.0, 1.0], 'houseTop': [10.2, 17.0, 1.0], 'dem1': add(DEM1, [0, 2.0, 0]), 'rail': [RAILX, 1.0, 0.0]})
st.cue('sfx:click', 'S11', PUSH11, 0.3); st.cue('thunder', 'S11', BOOM11, 0.7)

# 12: around the railing. Square across the street at the gap: the dust white-out clears on the stub of terrace and the blackened railing standing
#     alone between the two untouched neighbours, the crater behind, him still in it, his head sooty and smoking; RÉUSSI once the dust has settled
D12 = st.dur('S12')
C12 = [-2.4, 1.6, 0.9]; L12 = [10.0, 3.2, 0.55]
st.shot('S12', 'parisStreet', setOpts=CRATER_ST, light=SUNX, actors=[HERO('grand', [k(0.0, look=[11.0, 1.4, 0.0]), *IDLE(0.0, D12, {**DEAD, 'lid': 0.5}, every=0.5, blinks=(1.15,), darts=((0.6, -0.5),)), k(0.85, look='camera', lookDur=0.25)])],
        props=[CRATER, RUIN(), *LEFTS, *NEIGHS, SOOT('suie12'), WISP('fumee12'),
               P('poussiere12', 'dustCloud', pos=[10.5, 0, 0.6], opts={'r': 5.5, 'h': 6.5, 'n': 30, 'at': -0.4, 'clear': [0.05, 0.85]}),
               P('fumees12', 'smokeField', pos=[0, 0, 0], opts={'points': [[14.0, 0.0, 6], [16.0, 2.5, 5]], 'size': 0.8, 'color': '#A8A29A'}),
               *LBG('echelle12', C12, L12, 52, sx=0.7, sy=0.28, d=42, side=1)],
        cams=[cam(0.0, C12, add(C12, [0.3, 0.0, 0.0]), L12, L12, lens=52)])
chk('S12', C12, L12, 52, {'head': HEADC, 'rail': [RAILX, 1.0, 1.1], 'neighL_edge': [10.2, 6.0, 3.5], 'neighR_edge': [10.2, 6.0, -1.5]})
st.cue('sfx:crunch', 'S12', 0.0, 0.3); st.cue('sfx:wind', 'S12', 0.5, 0.2)

# 13: the building got a state funeral. On the road, low, tight on the first soldier's hands: a single brick, big, on a plump red velvet cushion;
#     behind it soldiers slow-march toward us, two with rifles, a flag bearer with a plain flag, a trumpet and a drum; the ladder towers over them
D13 = st.dur('S13')
MARCH = [('porteur', -0.6, 0.0), ('soldat1', -1.45, -0.75), ('soldat2', 0.25, -0.75), ('drapeau', -0.6, -1.6), ('musi1', -1.45, -2.35), ('musi2', 0.25, -2.35)]
Z13 = 7.6; STEP13 = 0.8
acts13, props13 = [], []
for j, (who, x, dz) in enumerate(MARCH):
    p0 = [x, 0, r(Z13 + dz)]; p1 = [x, 0, r(Z13 + dz + STEP13)]
    ks = [k(0.0, look='camera'), k(0.0, to=p1, dur=D13, ease='linear', clip='marchPomp', face='keep')]
    if who == 'porteur':
        hp = lambda q, d: [*off(q, 0, 0.42, d, 1.28), 1, 0.02]
        ks += [k(0.0, toon={'reach': {'R': hp(p0, 0.13), 'L': hp(p0, -0.13)}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
               k(r(D13 - 0.05), toon={'reach': {'R': hp(p1, 0.13), 'L': hp(p1, -0.13)}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}}, toonDur=r(D13 - 0.1), toonEase='linear')]
    acts13.append(act(who, p0, 0, 'stand', 'neutral', params={'freq': 0.9}, keys=ks))
props13 += [P('coussin13', 'velvetCushion', on={'actor': 'porteur', 'hand': 'R', 'offset': [-0.13, 0.02, 0.0]}, opts={'w': 0.5}),
            P('brique13', 'brick', on={'actor': 'porteur', 'hand': 'R', 'offset': [-0.13, 0.13, 0.0]}, opts={'s': 2.0}),
            P('fusil13a', 'rifle', on={'actor': 'soldat1', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'rot': [0.15, 0, 0]}),
            P('fusil13b', 'rifle', on={'actor': 'soldat2', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'rot': [0.15, 0, 0]}),
            P('drapeau13', 'flag', on={'actor': 'drapeau', 'hand': 'R', 'offset': [0.0, -0.6, 0.0]}, opts={'colors': ['#2E3A55'], 'poleR': 0.022, 'poleColor': '#C9A040'}, scale=1.5),
            P('trompette13', 'bandInstr', on={'actor': 'musi1', 'joint': 'head', 'offset': [0.0, 0.13, 0.11], 'rot': [-0.3, -0.85, 0.0]}, opts={'kind': 'trumpet', 'beat': [0.2, 0.75, 1.3, 1.85], 's': 1.15}),
            P('tambour13', 'bandInstr', on={'actor': 'musi2', 'joint': 'torso', 'offset': [0.0, 0.12, 0.3]}, opts={'kind': 'drum', 'beat': [0.1, 0.55, 1.0, 1.45, 1.9]}),
            *[P(f'casque13{j}', 'armyHelmet', on={'actor': w, 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95}) for j, (w, _, _) in enumerate(MARCH)]]
C13 = [-0.95, 1.05, 10.1]; L13 = [-0.5, 2.05, 6.0]
st.shot('S13', 'parisStreet', setOpts=CRATER_ST, actors=acts13, props=[CRATER, RUIN(), *LEFTS, *NEIGHS, *props13, *LBG('echelle13', C13, L13, 58, sx=0.72, sy=0.12, d=30, side=1, top='fireman')],
        cams=[cam(0.0, C13, add(C13, [0.0, 0.0, 0.75]), L13, add(L13, [0, 0, 0.75]), lens=58)])
chk('S13', C13, L13, 58, {'brick0': [-0.73, 1.45, 8.02], 'brick1': [-0.73, 1.45, 8.82], 'porteurHead': [-0.6, 2.1, 7.6], 'musi': [-1.45, 2.0, 5.25]})
st.cue('sfx:step', 'S13', 0.1, 0.4); st.cue('sfx:fanfare', 'S13', 0.2, 0.3)

# 14: the railing was listed as a historic monument. From the crater side, three-quarter: his face in the bars (still stuck), left of frame; right of the
#     bars on the rim an official cuts a red ribbon with big scissors, the drape slides off a big bronze plaque, a soldier snaps a salute at the left
D14 = st.dur('S14'); CUT14 = 0.75; DRAPE14 = 0.95
C14 = [11.25, 1.8, 1.25]
PLQ = [9.95, 0, -1.05]; PLQ_RY = yaw(PLQ, C14)
RIB14 = [10.35, 0, -0.55]
OFF14 = [10.55, 0, -1.5]; ORY14 = yaw(OFF14, add(RIB14, [0.0, 0, 0.1]))
SOL14 = [9.7, 0, 1.2]
L14 = [9.85, 1.5, -0.35]
st.shot('S14', 'parisStreet', setOpts=CRATER_ST, light=SUNX, actors=[
        HERO('grand', [k(0.0, look=[10.4, 1.5, -0.8]), *IDLE(0.0, D14, DEAD, every=0.55, blinks=(1.7,), darts=((0.6, 0.6), (1.2, 0.0))), k(1.15, look='camera', lookDur=0.2), k(2.25, look=add(PLQ, [0, 1.6, 0]), lookDur=0.25)]),
        act('officiel', OFF14, ORY14, 'stand', 'happy', keys=[k(0.0, look=add(RIB14, [0, 0.95, 0])),
            k(0.0, toon={'reach': {'R': [*off(OFF14, ORY14, 0.48, 0.12, 1.05), 1, 0.04]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}}, toonDur=0.0),
            k(r(CUT14 - 0.1), toon={'reach': {'R': [*off(OFF14, ORY14, 0.62, 0.05, 1.0), 1, 0.04]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.12),
            k(r(CUT14 + 0.25), toon={'reach': {'R': [*off(OFF14, ORY14, 0.3, 0.3, 1.9), 1, 0.04]}, 'hands': {'R': 'grip'}, 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.1, 'mouth': 'smile', 'brow': 0.6}}, toonDur=0.15, toonEase='out'),
            k(r(CUT14 + 0.6), look='camera', lookDur=0.2)]),
        act('soldat1', SOL14, yaw(SOL14, C14), 'stand', 'neutral', keys=[k(0.0, look=add(PLQ, [0, 1.3, 0])),
            k(r(DRAPE14 + 0.05), toon={'reach': {'R': [*off(SOL14, yaw(SOL14, C14), 0.12, 0.15, 2.18), 1, 0.03]}, 'hands': {'R': 'open'}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.07, toonEase='out'),
            k(r(DRAPE14 + 0.2), toon={'reach': {'R': [*off(SOL14, yaw(SOL14, C14), 0.12, 0.15, 2.18), 1, 0.03]}, 'hands': {'R': 'open'}, 'sq': [1, 1, 1]}, toonDur=0.1),
            k(1.9, toon={'reach': {'R': [*off(SOL14, yaw(SOL14, C14), 0.12, 0.15, 2.2), 1, 0.03]}, 'hands': {'R': 'open'}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.2),
            k(2.35, toon={'reach': {'R': [*off(SOL14, yaw(SOL14, C14), 0.12, 0.15, 2.18), 1, 0.03]}, 'hands': {'R': 'open'}, 'sq': [1, 1, 1]}, toonDur=0.2)])],
        props=[CRATER, RUIN(), *LEFTS, *NEIGHS, SOOT('suie14'),
               P('plaque14', 'bronzePlaque', pos=PLQ, ry=PLQ_RY, opts={'w': 1.15, 'h': 0.85, 'post': 1.15, 'dir': 160, 'drapeAt': [DRAPE14, 0.4]}),
               P('ruban14', 'ribbonCut', pos=RIB14, ry=PLQ_RY, opts={'w': 1.3, 'h': 0.95, 'cutAt': CUT14}),
               P('ciseaux14', 'scissors', on={'actor': 'officiel', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'rot': [-1.2, 0, 0]}, opts={'cutAt': CUT14}),
               P('casque14', 'armyHelmet', on={'actor': 'soldat1', 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95}),
               P('tinte14', 'twinkle', pos=off(PLQ, PLQ_RY, 0.1, 0.0, 1.65), opts={'at': r(DRAPE14 + 0.35), 's': 0.16}),
               *LBG('echelle14', C14, L14, 50, sx=0.25, sy=0.27, d=40, side=-1)],
        cams=[cam(0.0, C14, add(C14, [-0.1, 0.0, -0.08]), L14, L14, lens=50)])
chk('S14', C14, L14, 50, {'head': HEADC, 'plaque': add(PLQ, [0, 1.6, 0]), 'official': add(OFF14, [0, 2.1, 0]), 'soldier': add(SOL14, [0, 2.2, 0])})
st.cue('sfx:click', 'S14', CUT14, 0.35); st.cue('sfx:fanfare', 'S14', DRAPE14, 0.35)

# 15: head included. Tight from the crater side: the bronze plaque fills the right half of the frame, its huge thick engraved arrow pointing straight
#     at his lit, sooty head in the bars at the left; he does not move; a glint runs along the arrow
D15 = st.dur('S15')
C15 = [11.05, 1.62, 0.32]; L15 = [9.75, 1.52, -0.42]
PC15 = [PLQ[0], 1.15 + 0.85 / 2, PLQ[2]]
_pp, _ph = project(C15, L15, 46, PC15), project(C15, L15, 46, HEADC)
DIR15 = r(math.degrees(math.atan2(-(_ph[1] - _pp[1]), (_ph[0] - _pp[0]) * 9 / 16)), 1) if _pp and _ph else 180
st.shot('S15', 'parisStreet', setOpts=CRATER_ST, light=SUNX, actors=[HERO('grand', [k(0.0, look='camera'), STUCK(0.0, DEAD), *BLINK(0.7)])],
        props=[CRATER, RUIN(), *LEFTS, *NEIGHS, SOOT('suie15'),
               P('plaque15', 'bronzePlaque', pos=PLQ, ry=yaw(PLQ, C15), opts={'w': 1.15, 'h': 0.85, 'post': 1.15, 'dir': DIR15}),
               P('tinte15', 'twinkle', pos=off(PLQ, yaw(PLQ, C15), 0.12, 0.1, 1.5), opts={'at': 0.45, 's': 0.14}),
               *LBG('echelle15', C15, L15, 46, sx=0.3, sy=0.1, d=40, side=-1)],
        cams=[cam(0.0, C15, C15, L15, L15, lens=46)])
chk('S15', C15, L15, 46, {'head': HEADC, 'plaqueC': PC15, 'dir': [DIR15, 0, 0]})
st.cue('sfx:sting', 'S15', 0.3, 0.25)

# 16: he tilted his head; it came out. Through the bars from the crater side: he calmly turns his head a quarter turn and it pops out between the bars
#     in one go; he straightens up behind the rail with a stretch, blinks, free, sooty, a head taller than the official standing beside him
D16 = st.dur('S16'); TILT16 = 0.4; POP16 = 0.9
OFF16 = [8.35, 0, -0.85]
C16 = [10.75, 1.95, 0.75]; L16 = [8.65, 1.85, -0.25]
st.shot('S16', 'parisStreet', setOpts=CRATER_ST, light=SUNX, actors=[
        HERO('grand', [STUCK(0.0, DEAD), k(0.0, look='camera'),
             STUCK(TILT16, {**DEAD, 'lid': 0.5}, extra={'bend': {'spine': [1.2, 0, 0, 1, None], 'neck': [-0.85, 1.35, 0, 1, None]}}, dur=0.35),
             STUCK(r(POP16 - 0.06), {**DEAD, 'lid': 0.6}, extra={'bend': {'spine': [1.24, 0, 0, 1, None], 'neck': [-0.9, 1.45, 0, 1, None]}, 'sq': [0.97, 1.03, 0.97]}, dur=0.06),
             k(POP16, to=add(MAN, [-0.3, 0, 0]), dur=0.12, ease='out', face='keep'),
             k(POP16, toon={'bend': {'spine': [-0.08, 0, 0, 1, None], 'neck': [0.0, 0.0, 0, 1, None]}, 'scl': {'head': [1.08, 0.94, 1.0]}, 'sq': [0.9, 1.12, 0.9], 'face': {'lid': 0.0, 'pop': 0.3, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.1, toonEase='out'),
             k(r(POP16 + 0.16), toon={'sq': [1.06, 0.95, 1.06], 'scl': {'head': [1, 1, 1]}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.08),
             k(r(POP16 + 0.32), toon={'sq': [1, 1, 1], 'face': DEAD}, toonDur=0.12), *BLINK(1.5), *BLINK(1.86),
             k(1.25, look=add(OFF16, [0, 2.0, 0]), lookDur=0.2), k(1.65, look='camera', lookDur=0.2)]),
        act('officiel', OFF16, yaw(OFF16, [9.0, 0, 0.6]), 'stand', 'happy', keys=[k(0.0, look=HEADC), k(r(POP16 + 0.2), look=add(MAN, [-0.3, 2.45, 0]), lookDur=0.15),
            k(r(POP16 + 0.2), toon={'face': {'pop': 0.25, 'mouth': 'O', 'brow': 0.6, 'lid': 0.0}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.08), k(r(POP16 + 0.55), toon={'face': {'mouth': 'line', 'brow': 0.3, 'lid': 0.2}}, toonDur=0.2)])],
        props=[CRATER, RUIN(), *LEFTS, *NEIGHS, SOOT('suie16'), P('plaque16', 'bronzePlaque', pos=PLQ, ry=PLQ_RY, opts={'w': 1.15, 'h': 0.85, 'post': 1.15, 'dir': 160}),
               P('pop16', 'toonPuff', pos=add(HEADC, [0.0, 0.0, 0.0]), opts={'at': POP16, 'n': 5, 'size': 0.08, 'life': 0.4, 'rise': 0.1, 'spread': 0.3, 'color': '#E8E2D6'}),
               *LBG('echelle16', C16, L16, 46, sx=0.75, sy=0.12, d=40, side=1)],
        cams=[cam(0.0, C16, add(C16, [0.05, 0.0, 0.0]), L16, L16, lens=46)])
chk('S16', C16, L16, 46, {'headStuck': HEADC, 'headFree': add(MAN, [-0.3, 2.45, 0]), 'offHead': add(OFF16, [0, 2.15, 0]), 'feet': MAN})
st.cue('sfx:squeak', 'S16', TILT16, 0.2); st.cue('sfx:pop', 'S16', POP16, 0.45)

# 17: he was arrested for theft. Low on the pavement beside the empty railing, looking down the street: two special forces in black slide down ropes
#     from a helicopter and pin him face down, his flattened face toward us between them, one kneeling on his back, the other twisting his arm
D17 = st.dur('S17'); LAND17 = 0.55; PIN17 = 0.85
HEAD17 = [8.55, 0.0, 0.25]
LIE17 = [6.3, 0.0, 0.25]                               # his feet: he lies face down along X, his head toward the railing and the camera
SF = [('forces1', [6.9, 0, 1.1]), ('forces2', [6.8, 0, -0.65])]
PINP = [[7.25, 0, 0.82], [7.1, 0, -0.32]]
C17 = [9.55, 0.42, 1.15]; L17 = [6.6, 0.75, -0.1]
acts17 = [HERO('grand', [k(0.0, look='camera'), k(0.0, toon={'lay': [0.0, 0.0], 'face': DEAD}, toonDur=0.0),
                         k(r(PIN17 - 0.12), toon={'lay': [0.4, 0.0], 'face': {**DEAD, 'lid': 0.2, 'brow': 0.3}}, toonDur=0.1),
                         k(PIN17, toon={'lay': [1.52, 0.0], 'sq': [1.08, 0.92, 1.08], 'bend': {'neck': [-0.4, 0.9, 0, 1, None]}, 'scl': {'head': [1.12, 0.9, 1.0]}, 'face': {**DEAD, 'cheeks': 0.8, 'lid': 0.4}}, toonDur=0.08, toonEase='in'),
                         k(r(PIN17 + 0.15), toon={'lay': [1.5, 0.0], 'sq': [1.0, 1.0, 1.0], 'bend': {'neck': [-0.4, 0.9, 0, 1, None]}, 'scl': {'head': [1.1, 0.92, 1.0]}, 'face': {**DEAD, 'cheeks': 0.8}}, toonDur=0.1),
                         *BLINK(1.3, {**DEAD, 'cheeks': 0.8})], pos=LIE17, ry=90)]
for j, (who, p) in enumerate(SF):
    top = add(p, [0, 7.0, 0])
    acts17.append(act(who, top, yaw(p, [7.6, 0, 0.25]), 'hangBar', 'angry', keys=[k(0.0, look=add(LIE17, [1.5, 0, 0])), k(0.0, to=p, dur=r(LAND17 + 0.05 * j), ease='in', face='keep'), k(r(LAND17 + 0.05 * j), clip='stand'),
        k(r(LAND17 + 0.05 * j), toon={'sq': [1.15, 0.85, 1.15]}, toonDur=0.05), k(r(LAND17 + 0.12 + 0.05 * j), toon={'sq': [1, 1, 1]}, toonDur=0.08),
        k(PIN17, to=PINP[j], dur=0.15, ease='out', face='keep'),
        k(PIN17, clip='kneel' if j == 0 else 'stand'),
        k(r(PIN17 + 0.1), toon={'reach': {'R': [*[7.45 - 0.2 * j, 0.42, 0.42 - 0.3 * j], 1, 0.03], 'L': [*[7.25 - 0.2 * j, 0.42, 0.25 - 0.3 * j], 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}}, toonDur=0.12)]))
st.shot('S17', 'parisStreet', setOpts=CRATER_ST, light={'dir': [-4.0, 9.0, 6.0]}, actors=acts17,
        props=[CRATER, RUIN(), *LEFTS, *NEIGHS, SOOT('suie17'),
               P('heli17', 'helicopter', pos=[6.6, 9.6, 0.2], ry=180, opts={'beam': False}),
               *[P(f'corde17{j}', 'rope', pos=add(p, [0, 9.0, 0]), opts={'len': 9.0, 'r': 0.03, 'color': '#2A2C30', 'sway': 0.02}) for j, (_, p) in enumerate(SF)],
               *[P(f'cagoule17{j}', 'balaclava', on={'actor': w, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}) for j, (w, _) in enumerate(SF)],
               P('poussiere17', 'toonPuff', pos=add(HEAD17, [-0.6, 0.1, 0]), opts={'at': PIN17, 'n': 6, 'size': 0.18, 'life': 0.6, 'rise': 0.3, 'spread': 0.8, 'color': '#C9BFAA'}),
               *LBG('echelle17', C17, L17, 56, sx=0.68, sy=0.24, d=40, side=1)],
        fx=[{'type': 'shake', 'at': PIN17, 'dur': 0.12, 'amount': 0.01}],
        cams=[cam(0.0, C17, add(C17, [-0.1, 0.0, 0.0]), L17, L17, lens=56)])
chk('S17', C17, L17, 56, {'headLying': [8.55, 0.25, 0.25], 'sf1': add(PINP[0], [0, 1.4, 0]), 'sf2': add(PINP[1], [0, 2.1, 0]), 'heli': [6.6, 9.6, 0.2]})
st.cue('whoosh', 'S17', 0.1, 0.3); st.cue('thud', 'S17', PIN17, 0.5)

# 18: his head was seized. The interrogation room under the hanging lamp, from the front: he sits at the table, deadpan; beside him a detective winds
#     red-and-white seal tape round his head, band after band, then thumps a big red wax seal onto his forehead; a painted window on the wall at the
#     left shows the same ladder still rising into its cloud
D18 = st.dur('S18'); SEAL18 = 1.0
SIT18 = [-0.15, 0, -1.45]
DET18 = [0.62, 0, -1.7]
st.shot('S18', 'interrogation', actors=[
        HERO('grand', [k(0.0, look='camera'), k(0.0, toon={'face': DEAD, 'reach': {'L': [-0.45, 0.82, -0.95, 1, 0.03], 'R': [0.15, 0.82, -0.95, 1, 0.03]}, 'hands': {'L': 'rest', 'R': 'rest'}}, toonDur=0.0),
             k(SEAL18, toon={'sq': [1.05, 0.94, 1.05], 'face': {**DEAD, 'lid': 0.8}}, toonDur=0.04, keepPose=True), k(r(SEAL18 + 0.14), toon={'sq': [1, 1, 1], 'face': DEAD}, toonDur=0.12, keepPose=True),
             *BLINK(1.3)], pos=SIT18, ry=0, clip='sit'),
        act('detective', DET18, yaw(DET18, SIT18), 'stand', 'neutral', keys=[k(0.0, look=add(SIT18, [0, 1.8, 0])),
            k(0.0, toon={'touch': {'R': ['@grand.head', 0.2, 0.45, 0.1, 1, 0.0], 'L': ['@grand.head', 0.22, 0.2, -0.05, 1, 0.0]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.0),
            k(0.25, toon={'touch': {'R': ['@grand.head', -0.2, 0.42, 0.1, 1, 0.0], 'L': ['@grand.head', 0.2, 0.3, 0.0, 1, 0.0]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.2),
            k(0.5, toon={'touch': {'R': ['@grand.head', 0.2, 0.12, 0.12, 1, 0.0], 'L': ['@grand.head', 0.22, 0.25, -0.05, 1, 0.0]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.2),
            k(0.72, toon={'touch': {'R': ['@grand.head', -0.18, 0.25, 0.1, 1, 0.0], 'L': ['@grand.head', 0.22, 0.3, 0.0, 1, 0.0]}, 'hands': {'R': 'grip', 'L': 'grip'}}, toonDur=0.15),
            k(r(SEAL18 - 0.15), toon={'reach': {'R': [*add(SIT18, [0.3, 2.45, 0.3]), 1, 0.03]}, 'hands': {'R': 'fist'}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.1),
            k(SEAL18, toon={'touch': {'R': ['@grand.head', 0.0, 0.36, 0.22, 1, 0.0]}, 'hands': {'R': 'fist'}, 'sq': [1.06, 0.95, 1.06], 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.05, toonEase='in'),
            k(r(SEAL18 + 0.2), toon={'reach': {'R': [*add(DET18, [-0.1, 1.3, 0.3]), 1, 0.03]}, 'hands': {'R': 'rest'}, 'sq': [1, 1, 1]}, toonDur=0.2), k(r(SEAL18 + 0.3), look='camera', lookDur=0.2)])],
        props=[P('ruban18', 'sealTape', on={'actor': 'grand', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'at': 0.12, 'every': 0.28, 'wind': 0.24}),
               P('cachet18', 'waxSeal', on={'actor': 'grand', 'joint': 'head', 'offset': [0.0, 0.36, 0.155]}, opts={'at': SEAL18}),
               P('fenetre18', 'skyWindow', pos=[-1.25, 1.85, -3.15], opts={'w': 0.8, 'h': 1.0}),
               P('dossier18', 'photo', pos=[-0.3, 0.8, -0.65], rot=[-PI / 2, 0, 0.2], scale=3.0),
               P('etoiles18', 'impactStars', pos=add(SIT18, [0.0, 2.1, 0.3]), opts={'at': SEAL18, 'n': 5, 'r': 0.35})],
        cams=[cam(0.0, [-0.15, 1.65, 1.6], [-0.15, 1.66, 1.45], [-0.35, 1.75, -1.5], [-0.35, 1.75, -1.5], lens=46)])
chk('S18', [-0.15, 1.65, 1.6], [-0.35, 1.75, -1.5], 46, {'head': add(SIT18, [0, 1.75, 0]), 'window': [-1.25, 1.85, -3.15], 'detHead': add(DET18, [0, 2.1, 0])})
st.cue('sfx:zip', 'S18', 0.12, 0.3); st.cue('sfx:zip', 'S18', 0.4, 0.25); st.cue('sfx:zip', 'S18', 0.68, 0.25); st.cue('thud', 'S18', SEAL18, 0.45)

# 19: he rents his head from the State. Three-quarter on the post-office counter window, from the side: stooping under the top of the window because he
#     is too tall, he slides a banknote through the slot under the glass; the clerk (seated, face to us) sends his arm out through the slot like a hose,
#     up to his forehead, winds up and brings a big round seal down on it; he stays bent and turns to us with a violet ink ring on his forehead
D19 = st.dur('S19'); NOTE19 = [0.25, 0.65]; ARM19 = 0.75; WIND19 = 0.95; STAMP19 = 1.05
GLASSZ = -2.2
CUST = [0.0, 0, -1.48]; CLERK = [0.05, 0.3, -2.78]
FORE = [0.0, 1.88, -1.86]                              # his forehead when he stoops under the window
C19 = [1.85, 1.62, -1.62]; L19 = [-0.05, 1.62, -2.25]
SLOT = [0.0, 1.13, GLASSZ]
st.shot('S19', 'poste', setOpts={'guichets': False, 'title': 'ADMINISTRATION'}, actors=[
        HERO('grand', pos=CUST, ry=180, keys=[k(0.0, look=[0.0, 1.55, -2.6]),
             k(0.0, toon={'bend': {'spine': [0.55, 0, 0, 1, None], 'neck': [-0.4, 0, 0, 1, None]}, 'reach': {'R': [0.12, 1.12, -1.95, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0),
             k(NOTE19[0], toon={'bend': {'spine': [0.6, 0, 0, 1, None], 'neck': [-0.42, 0, 0, 1, None]}, 'reach': {'R': [0.1, 1.12, -2.1, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.35),
             k(r(NOTE19[1] + 0.05), toon={'bend': {'spine': [0.6, 0, 0, 1, None], 'neck': [-0.42, 0, 0, 1, None]}, 'reach': {'R': [0.25, 1.1, -1.85, 1, 0.03]}, 'hands': {'R': 'open'}, 'face': DEAD}, toonDur=0.2),
             k(STAMP19, toon={'bend': {'spine': [0.66, 0, 0, 1, None], 'neck': [-0.42, 0, 0, 1, None]}, 'reach': {'R': [0.25, 1.1, -1.85, 1, 0.03]}, 'hands': {'R': 'open'}, 'sq': [1.05, 0.93, 1.05], 'face': {**DEAD, 'lid': 0.9}}, toonDur=0.04),
             k(r(STAMP19 + 0.16), toon={'bend': {'spine': [0.6, 0, 0, 1, None], 'neck': [-0.42, 0, 0, 1, None]}, 'reach': {'R': [0.25, 1.1, -1.85, 1, 0.03]}, 'hands': {'R': 'open'}, 'sq': [1, 1, 1], 'face': DEAD}, toonDur=0.12),
             k(1.45, look='camera', lookDur=0.25), *BLINK(2.05)]),
        act('guichetier', CLERK, 0, 'sit', 'neutral', keys=[k(0.0, look=add(FORE, [0, -0.1, 0])),
            k(0.0, toon={'reach': {'R': [0.25, 1.12, -2.5, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.0}}, toonDur=0.0),
            k(r(ARM19 - 0.1), toon={'reach': {'R': [*add(SLOT, [0.0, 0.0, -0.05]), 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.08),
            k(ARM19, toon={'reach': {'R': [*add(SLOT, [0.0, 0.08, 0.25]), 1, 0.03, [0.2, -0.8, 0.5]]}, 'hands': {'R': 'grip'}, 'hose': 0.2, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.07),
            k(r(ARM19 + 0.07), toon={'reach': {'R': [*add(FORE, [0.05, 0.35, 0.35]), 1, 0.03, [0.2, -0.8, 0.5]]}, 'hands': {'R': 'grip'}, 'hose': 0.25, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.07),
            k(WIND19, toon={'reach': {'R': [*add(FORE, [0.05, 0.42, 0.3]), 1, 0.03, [0.2, -0.8, 0.5]]}, 'hands': {'R': 'grip'}, 'hose': 0.25, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.2, 'mouth': 'clench'}}, toonDur=0.08),
            k(STAMP19, toon={'reach': {'R': [*add(FORE, [0.0, 0.12, 0.2]), 1, 0.03, [0.2, -0.8, 0.5]]}, 'hands': {'R': 'grip'}, 'hose': 0.25, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.04, toonEase='in'),
            k(r(STAMP19 + 0.3), toon={'reach': {'R': [0.25, 1.12, -2.5, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'smile'}}, toonDur=0.25),
            k(1.6, look=[1.85, 1.62, -1.62], lookDur=0.3)])],
        props=[P('billet19', 'banknote', pos=[0.12, 1.11, -1.98], rot=[-PI / 2, 0, 0], opts={'w': 0.26}, keys=[k(NOTE19[0], to=[0.08, 1.11, -2.45], dur=NOTE19[1] - NOTE19[0], ease='inOut')]),
               P('fente19', 'slotArch', pos=[0.0, 1.1, r(GLASSZ + 0.012)], opts={'w': 0.34, 'h': 0.11}),
               P('tampon19', 'roundStamp', on={'actor': 'guichetier', 'hand': 'R', 'offset': [0.0, 0.0, 0.0], 'rot': [-PI / 2, 0, 0]}),
               P('encre19', 'inkRing', on={'actor': 'grand', 'joint': 'head', 'offset': [0.0, 0.36, 0.155]}, opts={'at': r(STAMP19 + 0.02)}),
               P('fenetre19', 'skyWindow', pos=[-1.55, 2.3, -3.36], opts={'w': 1.1, 'h': 1.1})],
        cams=[cam(0.0, C19, add(C19, [-0.05, 0.0, 0.03]), L19, L19, lens=48)])
chk('S19', C19, L19, 48, {'fore': FORE, 'clerkHead': add(CLERK, [0, 1.55, 0]), 'slot': SLOT, 'winTop': [0.0, 2.12, GLASSZ], 'window': [-1.55, 2.3, -3.36]})
st.cue('sfx:paper', 'S19', NOTE19[0], 0.25); st.cue('sfx:stretch', 'S19', ARM19, 0.25); st.cue('thud', 'S19', STAMP19, 0.45); st.cue('sfx:sting', 'S19', 1.45, 0.25)
print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
GRAND = {'preset': 'lemec', 'build': {'width': 0.76, 'headWidth': 1.3, 'headScale': 1.0, 'height': 1.12}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'hair': 'bald',
        'gloves': '#2E3320', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 2.2, 'shift': 2.0, 'breathe': 2.0}}
POMPC = {'preset': 'pompier', 'hat': 'none', 'hair': 'bald', 'suit': '#1F2A44', 'pants': '#1F2A44', 'bandColor': '#D8F03C', 'bandH': 0.05, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
RIOT = {'preset': 'cop', 'hat': 'none', 'hair': 'bald', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
SPEC = {'outfit': 'suit', 'suit': '#36404E', 'pants': '#2E3642', 'shirt': '#36404E', 'lapel': '#2A313C', 'tie': '#2A313C', 'cuff': '#36404E', 'hat': 'none', 'hair': 'bald', 'gloves': '#16171A',
        'facial': 'none', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
BOMB = {'outfit': 'suit', 'suit': '#56623F', 'pants': '#4E5A3A', 'shirt': '#56623F', 'lapel': '#4E5A3A', 'tie': '#4E5A3A', 'cuff': '#56623F', 'hat': 'none', 'hair': 'bald', 'gloves': '#2E3320',
        'build': {'width': 1.45, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX}
st.write("La rambarde", rig="toon", debugJoints=["mec", "grand"], fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC, 'grand': GRAND,
    **{w: {**POMPC, 'seed': 850 + i} for i, w in enumerate(POMP)},
    'ministre': {'preset': 'politique', 'seed': 870, 'suit': '#3A4F6E', 'lapel': '#3A4F6E', 'tie': '#C8A030', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 871, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'hairColor': '#BDBDBD', 'sash': ['#2F62B5', '#F4F4F0', '#E0413A'], 'sashW': 0.12,
                  'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'mamie': {'preset': 'mamie', 'seed': 872, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'voisin1': {'preset': 'worker', 'seed': 873, 'hat': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'voisin2': {'preset': 'madame', 'seed': 874, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'demineur1': {**BOMB, 'preset': 'worker', 'seed': 875}, 'demineur2': {**BOMB, 'preset': 'worker', 'seed': 876},
    'flic1': {**RIOT, 'seed': 877}, 'flic2': {**RIOT, 'seed': 878}, 'flic3': {**RIOT, 'seed': 879},
    'porteur': {**SOLD, 'preset': 'cop', 'seed': 880}, 'soldat1': {**SOLD, 'preset': 'cop2', 'seed': 881}, 'soldat2': {**SOLD, 'preset': 'cop', 'seed': 882},
    'drapeau': {**SOLD, 'preset': 'cop2', 'seed': 883}, 'musi1': {**SOLD, 'preset': 'cop', 'seed': 884}, 'musi2': {**SOLD, 'preset': 'cop2', 'seed': 885},
    'officiel': {'preset': 'politique', 'seed': 886, 'suit': '#4A3F5E', 'lapel': '#4A3F5E', 'tie': '#C8A030', 'facial': 'mustache', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'forces1': {**SPEC, 'preset': 'cop', 'seed': 887}, 'forces2': {**SPEC, 'preset': 'cop2', 'seed': 888},
    'detective': {'preset': 'commissaire', 'seed': 889, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'guichetier': {'preset': 'boss', 'seed': 890, 'suit': '#5A6470', 'tie': '#2E3640', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
})
