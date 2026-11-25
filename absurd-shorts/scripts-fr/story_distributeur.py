#!/usr/bin/env python3
"""Le distributeur (story 95, cycle 51; an institutional escalation, a reversal and a dry last line, as the first stories).
This man put a coin in the corridor's drinks machine. Nothing fell. The minister ruled: it is a bank. It got its licence; this man is its first
client. The whole country placed its savings in it. It never gave anything back, like a real one. It bought the coffee machine, then the
photocopier. It named a director. Bankrupt: the director had drunk it all in coffees. It started to lean; leaning, it crushed the sandwich machine.
Too big to fall. The State bailed it out: two billion in coins. The sandwich machine got nothing. The can finally fell: it was the director's
bonus. This man claimed his coin. Refused: it is invested for forty years. The bank had been out of order from the start; it was in small print.
Staging: one office corridor (blue-grey wall, lino) holds the whole story but the press room. A tall red drinks machine (no brand, no word) stands
against the wall; at the front end of its bottom spiral one big bright can (one and a half times a can, plain colour bands) hangs tilted and stuck
from the first shot to S14; a small yellowed EN PANNE sticker sits on the glass's right edge at the coin slot's height in every shot of the machine.
The hero kneels at its left with his left arm in the delivery flap the whole film (body turned about thirty degrees off the lens, his face to us),
until S15. S01: low at slot height, he pushes a coin in, waits, drops to his knees and shoves his arm in the flap; the can rocks with a click and
stays. S02: the press room, a minister in a plain gold sash flips a chart: a drawn vending machine, an equals sign, a drawn bank with columns; snap
zoom on the equals sign; BANQUE. S03: the minister pops a brass BANQUE plate on the machine's header, cuts a ribbon, bends and shakes the hero's free
hand. S04: a queue of savers with piggy banks runs along the corridor and out of frame; the first feeds coins into the slot (slow lateral track).
S05: close on the slot swallowing coin after coin, the can above the flap unmoved, the hero's fingers wiggling in the empty flap. S06: wide along the
wall: BANQUE plates pop onto the coffee machine, then the photocopier: a little skyline. S07: the director drops into an armchair beside the hero,
a fat briefcase on his lap, and puts his feet up on the hero's back. S08: the director tips the machine's coin box at us: empty, a moth flutters
out; a tower of empty cups taller than him leans on the coffee machine; FAILLITE. S09: low and wide, the machine starts to lean with a creak, the
savers step back. S10: the machine falls further and flattens the sandwich machine into a drawn flat shape; one big bright sandwich slides out at
us; the hero's arm stretches with the flap. S11: soldiers and a minister rush in and stop it at forty-five degrees with their shoulders. S12: two
soldiers empty plain sacks into a giant funnel jammed in the slot, coins heap on the floor, the machine slowly rights itself. S13: low on the
flattened sandwich machine: one coin rolls off the heap toward it, stops short and falls flat; nobody looks. S14: close on the spiral: it turns, the
can drops into the flap; the director takes it from the hero's hand and holds it at chest height to the flashes. S15: a small counter with a glass
window stands before the machine; the hero pulls his arm out at last, stands and slaps his palm on it; a clerk behind the glass. S16: the clerk stamps
REFUSÉ on a sheet and slides it under the glass; behind him a wall chart: one thick line climbing very slowly to a small piggy bank, no labels. S17:
slow push-in on the glass's corner ending on the EN PANNE sticker, upright, square to the lens, wider than forty percent of the frame, above the
caption band, the hero's box head reflected in the glass; held.
Natural look; cycle 51: props_distributeur.js (drinkMachine with the stuck can, the sticker, the flap, the coin box, the plate, the lean and the
funnel; bigCan, banquePlaque, corridor, sandwichMachine, bigSandwich, bankChart, goldHeap, coinStream, rollCoin, plainSack, coinBox, glassCounter,
riseChart, glassGhost); coffeeMachine (props.js), photocopier (props_photocopie), piggyBank (props_centime), armchair (props_ascenseur), briefcase
(props_news), cupTower (props_cafe), moth (props_place), plainPodium (props_flaque), ribbonCut and bigScissors (props_baillement), flashBursts
(props_moustache), roundStamp (props_rambarde) reused; pressRoom (no flags) and whiteVoid sets.
Lessons applied from the start: one shot per line (no split ids); `lens` is the vertical field; characters about 2.3 m tall with the box head; faces
and key props above the caption band (0.77-0.83), heads below the card band (0.07-0.18) on the two card shots; every camera checked with project()
(CHECKS printed); every extra cast entry has a preset; the reach and hands of each actor carried forward key to key before writing (a one-hand key
replaced the whole reach); animated materials unique; no insignia, rank or flag on soldiers (plain olive, bare heads: no helmet shadow on faces), the
ministers' sashes one plain colour; no brand, logo, digit or English word anywhere (BANQUE, EN PANNE, REFUSÉ only); the chart drawn without labels;
nobody hurt (the machine stopped by shoulders, the hero beside it, the soldiers straining, not crushed); the director holds the can at chest height;
the flattened sandwich machine stays in every later corridor shot, untouched; cameras at least 20 degrees off the glass planes except the last
push-in (square to the sticker, as asked); slow drifts and blinks in every hold (the freeze check)."""
from story_kit import *
import math

st = Story('distributeur', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 18)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
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

# ================================================================= the corridor and the machines (world): the wall's face at z -0.45
WALLZ = -0.45
M = [0.0, 0, 0.0]; FZ = 0.4                     # the drinks machine, front at z 0.4, 1.0 wide, 2.15 tall
SLOT = [0.215, 1.2, 0.412]; FLAP = [-0.17, 0.44, 0.4]; CAN = [-0.095, 0.895, 0.31]; STK = [0.34, 1.2, 0.4145]; PLATE = [0.0, 2.065, 0.42]   # STK: the small paper EN PANNE sticker beside the slot
SWP = [1.22, 0, -0.09]                          # the sandwich machine (0.78 wide, 1.5 tall)
CMP = [-1.8, 0, -0.2]                           # the coffee machine (0.5 wide, 1.5 tall, front at z 0.025)
PCP = [-2.95, 0, -0.08]                         # the photocopier (1.1 wide, 0.95 tall)
HERO = [-0.85, 0, 0.72]; HRY = 50               # kneeling on one knee at the machine's left (far knee planted, shin flat), his left arm stretched into the flap
FLAPIN = [-0.16, 0.28, 0.24]                    # the reach target of his left hand: inside the flap's black opening (the kneel lowers the body after the arm is solved: the hand lands ~0.17 m higher, at the opening's middle)
def tilted(p, th):
    """a point of the machine (world, upright) once it leans th degrees to its right about its bottom right edge (x 0.5, y 0)"""
    a = math.radians(th); dx, y = p[0] - 0.5, p[1]
    return [r(0.5 + dx * math.cos(a) + y * math.sin(a)), r(-dx * math.sin(a) + y * math.cos(a)), p[2]]
def SETV(): return {'color': '#C9C6B6'}
def kvp(keys, t):
    """the drinkMachine's keyed value (props_distributeur kv): smoothstep from key to key"""
    if t <= keys[0][0]: return keys[0][1]
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if t < b: u = (t - a) / max(1e-4, b - a); u = u * u * (3 - 2 * u); return va + (vb - va) * u
    return keys[-1][1]
def CORR(sid, **o): return P(f'couloir{sid}', 'corridor', pos=[0, 0, WALLZ], opts={'len': 18, 'depth': 12, 'h': 3.5, 'doorX': -5.2, 'boardX': 4.6, 'plantX': -3.9, **o})
def MACH(sid, **o): return P(f'distrib{sid}', 'drinkMachine', pos=M, opts={'flapIn': 1, 'plaque': True, **o})
def SANDW(sid, **o): return P(f'sandw{sid}', 'sandwichMachine', pos=SWP, opts=o)
def COFFEE(sid, keys=None): return P(f'cafe{sid}', 'coffeeMachine', pos=CMP, **({'keys': keys} if keys else {}))
def COPIER(sid, keys=None): return P(f'copieur{sid}', 'photocopier', pos=PCP, **({'keys': keys} if keys else {}))
def PLATE_C(sid, **o): return P(f'plaqueC{sid}', 'banquePlaque', pos=[CMP[0], 0.88, CMP[2] + 0.245], opts={'w': 0.56, 'h': 0.16, **o})
def PLATE_P(sid, **o): return P(f'plaqueP{sid}', 'banquePlaque', pos=[PCP[0] - 0.1, 0.58, PCP[2] + 0.36], opts={'w': 0.78, 'h': 0.22, **o})
LOOKC = {'sunDir': [0.55, 0.9, 0.7]}            # light from the upper right: the leaning machine's shade falls toward the hero
def CORRIDOR(sid, crushed=False, mopts=None, extra=()):
    """the corridor's standing props after a shot: the wall, the drinks machine, the sandwich machine (flat from S10 on), the coffee machine and the copier"""
    return [CORR(sid), MACH(sid, **(mopts or {})), SANDW(sid, flat=crushed), COFFEE(sid), COPIER(sid), *extra]

HCALM = {'lid': 0.35, 'mouth': 'line', 'brow': 0.0}
HREST = off(HERO, HRY, 0.32, 0.2, 0.5)          # his right hand on his front knee
HBEND = {'spine': SP(0.1, -0.35), 'neck': SP(-0.2, 0.35)}   # leaning toward the machine, the head kept up and turned to us
def HERO_K(keys=(), flap=FLAPIN, face=HCALM, look='camera', rest=None, bend=None, pid='mec', blinks=(), breathe=None):
    """the hero in his one locked pose: on one knee (the clip set by a key: as a start clip only the reach applied and he half stood), left arm in the
    flap to the elbow, bowed toward the machine; blinks at the given times, a slow breath over [t0, t1] (breathe)"""
    ks = [k(0.0, clip='kneel'), k(0.0, look=look), TK(0.0, {'L': R5(flap, 1, 0.06), 'R': R5(rest or HREST)}, {'L': 'grip', 'R': 'rest'}, face, bend=bend or HBEND, d=0.0), *keys]
    for t in blinks: ks += blink(t, face)
    if breathe: ks += BREATHE(breathe[0], breathe[1], 0.6, 0.014)
    return act(pid, HERO, HRY, 'kneel', 'neutral', keys=ks)

for g_ in [('S01', 2.25, 'mec', 'canWobble'), ('S02', 0.4, 'ministre', 'flip'), ('S03', 1.5, 'ministre', 'handshake'), ('S07', 0.6, 'directeur', 'feetUp'),
           ('S08', 1.0, 'directeur', 'moth'), ('S10', 1.15, 'mec', 'crush'), ('S11', 0.35, 'sold1', 'shoulder'), ('S13', 1.9, 'mec', 'coinFlat'),
           ('S14', 0.75, 'mec', 'canDrop'), ('S15', 1.0, 'mec', 'slap'), ('S16', 0.12, 'guichet', 'stamp'), ('S17', 3.0, 'mec', 'sticker')]:
    st.gag(*g_)

# ================================================================= S01
# 1: the hook. Low at the coin slot's height: he stands at the machine and pushes a coin into the slot, waits, looks down at the flap, drops to his
#    knees at the machine's left and shoves his arm into the delivery flap to the elbow, rummages; on « Rien » the big bright can at the end of the
#    bottom spiral rocks with a click and stays put; his eyes go up to it, then to us
D1 = st.dur('S01'); HST = [0.78, 0, 0.86]; RYST = -35
C1 = fcam(0.0, [0.75, 1.15, 4.4], {'standTop': add(HST, [0, 2.35, 0]), 'standR': add(HST, [0.42, 1.7, 0.1]), 'kneelTop': add(HERO, [0, 1.8, 0]), 'heroL': add(HERO, [-0.42, 1.0, 0]), 'mtop': [0, 2.15, 0.4], 'flap': [FLAP[0], 0.3, 0.4], 'slot': SLOT}, push=0.2)
C1b = fcam(1.32, [0.35, 1.05, 3.4], {'kneelTop': add(HERO, [0, 1.85, 0]), 'heroL': add(HERO, [-0.42, 1.0, 0]), 'can': CAN, 'sticker': STK, 'slot': add(SLOT, [0.08, 0, 0]), 'flap': [FLAP[0], 0.3, 0.4]}, top=0.1, bottom=0.74, push=0.35)
chk('S01b', C1b, {'kneelFace': add(HERO, [0, 1.6, 0]), 'can': CAN, 'sticker': STK, 'slot': SLOT, 'flap': FLAP})
chk('S01', C1, {'standFace': add(HST, [0, 2.05, 0]), 'standTop': add(HST, [0, 2.3, 0]), 'kneelFace': add(HERO, [0, 1.6, 0]), 'can': CAN, 'sticker': STK, 'slot': SLOT, 'flap': FLAP, 'top': [0, 2.15, 0.4], 'feet': HST})
SLOTH = add(SLOT, [0.0, 0.0, 0.06])
EXPECT = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.3}
STRAIN = {'lid': 0.35, 'mouth': 'clench', 'brow': -0.5, 'gx': 0.4, 'gy': 0.4}
DROP1, IN1, WOB1 = 0.78, 1.4, 2.25
k1 = [k(0.0, look=SLOT), TK(0.0, {'R': R5(off(HST, RYST, 0.25, 0.3, 1.1)), 'L': R5(off(HST, RYST, 0.05, -0.3, 0.98))}, {'R': 'grip', 'L': 'rest'}, EXPECT, d=0.0),
      TK(0.16, {'R': R5(add(SLOTH, [0, 0, 0.03]))}, {'R': 'grip'}, EXPECT, d=0.16, keep=True),
      TK(0.34, {'R': R5(SLOTH)}, {'R': 'point'}, {**EXPECT, 'brow': 0.5}, (0.98, 1.02, 0.98), d=0.08, keep=True),
      TK(0.58, {'R': R5(off(HST, RYST, 0.2, 0.3, 1.0))}, {'R': 'rest'}, {**EXPECT, 'gy': 0.8}, (1, 1, 1), d=0.2, keep=True),
      k(0.55, look=[FLAP[0], 0.4, 0.9], lookDur=0.15),
      k(DROP1, clip='kneel', blend=0.18), k(DROP1, to=HERO, dur=0.42, glide=True, face=HRY), TK(DROP1, sq=(0.88, 1.12, 0.88), d=0.06, keep=True),
      TK(r(DROP1 + 0.05), {'L': R5(add(FLAPIN, [0.05, 0.12, 0.12]))}, {'L': 'open'}, STRAIN, (1.06, 0.92, 1.06), HBEND, d=0.3, keep=True),
      TK(IN1, {'L': R5(FLAPIN, 1, 0.06), 'R': R5(HREST)}, {'L': 'grip', 'R': 'rest'}, STRAIN, (1, 1, 1), HBEND, d=0.12, keep=True),
      *[TK(r(IN1 + 0.12 + 0.13 * i), {'L': R5(add(FLAPIN, [0.05 * (1 if i % 2 else -1), 0.03 * (1 if i % 3 else -1), -0.02 * (i % 2)]), 1, 0.06)}, {'L': 'grip'},
           {**STRAIN, 'gx': 0.5 if i % 2 else 0.1}, (1.03, 0.97, 1.03) if i % 2 else (0.98, 1.02, 0.98), {'spine': SP(0.2, -0.42 if i % 2 else -0.28), 'neck': SP(-0.2, 0.4)}, d=0.11, keep=True) for i in range(6)],
      TK(2.12, {'L': R5(FLAPIN, 1, 0.06)}, {'L': 'grip'}, {'lid': 0.05, 'mouth': 'clench', 'brow': -0.7, 'gx': 0.3, 'gy': 0.4}, (1, 1, 1), HBEND, d=0.08, keep=True),
      TK(r(WOB1 + 0.02), face={'lid': 0.0, 'mouth': 'clench', 'brow': -0.5, 'gx': 0.8, 'gy': -0.9}, d=0.03, keep=True),
      k(r(WOB1 + 0.12), look=CAN, lookDur=0.12), TK(r(WOB1 + 0.12), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.6, 'gy': -0.4, 'gx': 0.5}, sq=(0.96, 1.05, 0.96), d=0.06, keep=True),
      TK(r(WOB1 + 0.35), sq=(1, 1, 1), d=0.12, keep=True),
      TK(2.62, face={'lid': 0.1, 'mouth': 'line', 'brow': -0.6, 'gx': -0.4}, d=0.05, keep=True), k(2.72, look='camera', lookDur=0.15), TK(2.72, face={'lid': 0.15, 'mouth': 'line', 'brow': -0.7}, bend={'spine': SP(0.28, -0.22), 'neck': SP(0.0, 0.15)}, d=0.12, keep=True),
      *blink(1.9, STRAIN)]
st.shot('S01', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[act('mec', HST, RYST, 'stand', 'happy', keys=k1)],
        props=CORRIDOR('S01', mopts={'plaque': False, 'flapIn': [[1.2, 0], [IN1, 1]], 'coinsAt': [0.3], 'canWobble': [WOB1]}), cams=[C1, C1b])
st.cue('sfx:clink', 'S01', 0.42, 0.3); st.cue('sfx:rattleShort', 'S01', 0.5, 0.2); st.cue('thud', 'S01', r(DROP1 + 0.35), 0.25); st.cue('sfx:squeak', 'S01', IN1, 0.2); st.cue('sfx:click', 'S01', WOB1, 0.35)

# ================================================================= S02 the press room
# 2: the minister ruled: it is a bank. A minister in a plain gold sash at a podium flips the cover of a chart on an easel beside him: a drawn red
#    vending machine, a big equals sign, a drawn bank with columns; a snap zoom onto the equals sign; BANQUE stamps over it
D2 = st.dur('S02'); FLIP2 = 0.42; ZOOM2 = 1.28
MIN2 = [-0.5, 0, -1.55]; POD2 = [-0.5, 0, -1.15]; CH2 = [0.55, 0, -1.75]; RYCH = -12
EQ2 = [CH2[0] + 0.0, 0.75 + 1.5 * (1 - 0.42), CH2[2] + 0.12]
C2 = cam(0.0, [0.05, 1.7, 2.7], [0.05, 1.7, 2.55], [0.03, 1.5, -1.4], [0.03, 1.5, -1.4], lens=44)
EQAIM = [EQ2[0] - 0.03, EQ2[1] + 0.01, EQ2[2]]
def zcam(at, d, d2=None):   # a camera square on the chart, d metres from it, aimed a little above the equals sign
    a = math.radians(RYCH); f = [math.sin(a), 0, math.cos(a)]; fr = [r(EQAIM[0] + f[0] * d), r(EQAIM[1] - 0.02), r(EQAIM[2] + f[2] * d)]
    to = [r(EQAIM[0] + f[0] * (d2 or d)), r(EQAIM[1] - 0.02), r(EQAIM[2] + f[2] * (d2 or d))]
    return cam(at, fr, to, EQAIM, EQAIM, lens=40)
C2b = glide([zcam(ZOOM2, 2.45)], 0.09)                        # the snap: past the mark
C2c = glide([zcam(r(ZOOM2 + 0.12), 2.95, 2.8)], 0.22)        # back and settle, then a slow push to the end
chk('S02c', C2c, {'eq': EQ2, 'vendTop': [CH2[0], 0.75 + 1.5 * 0.96, CH2[2] + 0.1], 'bankBot': [CH2[0], 0.75 + 1.5 * 0.18, CH2[2] + 0.1]})
chk('S02', C2, {'minFace': add(MIN2, [0, 2.05, 0]), 'minTop': add(MIN2, [0, 2.3, 0]), 'chartTop': [CH2[0], 2.27, CH2[2]], 'chartBot': [CH2[0], 0.75, CH2[2]], 'eq': EQ2})
chk('S02b', C2b, {'eq': EQ2, 'vendBot': [CH2[0], 0.75 + 1.5 * 0.68, CH2[2] + 0.1], 'bankTop': [CH2[0], 0.75 + 1.5 * 0.42, CH2[2] + 0.1]})
RYM2 = 15
MINF = {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}
CORNER = [CH2[0] - 0.42, 2.18, CH2[2] + 0.16]
k2 = [k(0.0, look='camera'), TK(0.0, {'R': R5(off(MIN2, RYM2, 0.35, 0.18, 1.18)), 'L': R5(off(MIN2, RYM2, 0.35, -0.2, 1.18))}, {'R': 'rest', 'L': 'rest'}, MINF, d=0.0),
      TK(0.2, {'L': R5(add(CORNER, [0, -0.08, 0]))}, {'L': 'grip'}, {**MINF, 'gx': 0.6}, d=0.18, keep=True), k(0.18, look=CORNER, lookDur=0.12),
      TK(FLIP2, {'L': R5(add(CORNER, [0.05, 0.12, -0.05]))}, {'L': 'grip'}, {'lid': 0.15, 'mouth': 'O', 'brow': 0.4}, (0.96, 1.05, 0.96), d=0.1, keep=True),
      TK(r(FLIP2 + 0.25), {'L': R5(off(MIN2, RYM2, 0.4, -0.35, 1.3))}, {'L': 'point'}, {'lid': 0.2, 'mouth': 'smile', 'brow': 0.3}, (1, 1, 1), d=0.18, keep=True),
      k(r(FLIP2 + 0.25), look='camera', lookDur=0.12), TK(0.95, face={'lid': 0.2, 'mouth': 'smile', 'brow': 0.4, 'gx': 0.6}, bend={'neck': SP(0.0, 0.2)}, d=0.1, keep=True), *blink(1.1, MINF), *BREATHE(0.8, D2, 0.45, 0.015)]
st.shot('S02', 'pressRoom', setOpts={'flags': False, 'podium': False, 'chairs': False, 'backdrop': ' '}, look={'sunDir': [0.3, 0.9, 0.8]}, actors=[
        act('ministre', MIN2, RYM2, 'stand', 'neutral', keys=k2)],
        props=[P('pupitre2', 'plainPodium', pos=POD2, ry=RYM2), P('tableau2', 'bankChart', pos=CH2, ry=RYCH, opts={'w': 1.0, 'flipAt': FLIP2})],
        cams=[C2, C2b, C2c])
st.card('S02', 'BANQUE', at=st.at('S02', 'L02', 6))
st.cue('sfx:paper', 'S02', FLIP2, 0.35); st.cue('whoosh', 'S02', r(ZOOM2 - 0.05), 0.25, 0.12, 500, 2500)

# ================================================================= S03
# 3: it got its licence; this man is its first client. Three-quarter from the left: the minister presses the brass BANQUE plate onto the machine's
#    header (it pops on with a glint), cuts a red ribbon stretched before the machine with giant scissors, then bends and shakes the free hand of the
#    hero, still kneeling with his arm in the flap
D3 = st.dur('S03'); PLQ3, CUT3, SHK3 = 0.42, 1.0, 1.5
MIN3 = [0.62, 0, 1.02]; RYM3 = -58
C3 = fcam(0.0, [-0.9, 1.5, 5.2], {'minTop': add(MIN3, [0, 2.35, 0]), 'heroL': add(HERO, [-0.3, 1.2, 0]), 'kneelTop': add(HERO, [0, 1.8, 0]), 'plate': PLATE, 'ribR': [0.85, 0.95, 1.45], 'ribL': [-0.15, 0.6, 1.45]}, push=0.25)
SHAKE = off(HERO, HRY, 0.55, 0.05, 0.98)
chk('S03', C3, {'minFace': add(MIN3, [0, 2.05, 0]), 'minTop': add(MIN3, [0, 2.3, 0]), 'heroFace': add(HERO, [0, 1.6, 0]), 'plate': PLATE, 'shake': SHAKE, 'can': CAN, 'sticker': STK, 'ribbonL': [-0.15, 0.95, 1.45], 'ribbonR': [0.85, 0.95, 1.45]})
MINS = {'lid': 0.25, 'mouth': 'smile', 'brow': 0.3}
PRES3 = off(MIN3, RYM3, 0.38, 0.22, 1.45)
k3 = [k(0.0, look=PLATE), TK(0.0, {'R': R5(off(MIN3, RYM3, 0.25, 0.25, 1.1)), 'L': R5(off(MIN3, RYM3, 0.1, -0.3, 1.0))}, {'R': 'open', 'L': 'grip'}, MINS, d=0.0),
      TK(r(PLQ3 - 0.12), {'R': R5(add(PRES3, [0.0, -0.08, 0.0]))}, {'R': 'open'}, MINS, (1.0, 1.03, 1.0), d=0.15, keep=True),
      TK(PLQ3, {'R': R5(PRES3)}, {'R': 'open'}, {**MINS, 'lid': 0.4, 'mouth': 'bigsmile'}, (1.03, 0.97, 1.03), d=0.06, keep=True),
      TK(0.68, {'R': R5(off(MIN3, RYM3, 0.45, 0.05, 1.0)), 'L': R5(off(MIN3, RYM3, 0.45, -0.1, 1.0))}, {'R': 'grip', 'L': 'grip'}, MINS, (1, 1, 1), d=0.2, keep=True),
      k(0.6, look=[0.35, 0.95, 1.45], lookDur=0.15),
      TK(CUT3, {'R': R5(off(MIN3, RYM3, 0.5, 0.0, 0.98)), 'L': R5(off(MIN3, RYM3, 0.5, -0.05, 0.98))}, {'R': 'grip', 'L': 'grip'}, {**MINS, 'mouth': 'O'}, (1.02, 0.98, 1.02), d=0.06, keep=True),
      k(r(CUT3 + 0.15), look='camera', lookDur=0.15),
      k(r(SHK3 - 0.42), to=add(SHAKE, [0.5, -0.98, 0.18]), dur=0.3, glide=True, face=-80),
      TK(r(SHK3 - 0.2), {'R': R5(add(SHAKE, [0.05, 0.05, 0.05])), 'L': R5(off(MIN3, RYM3, 0.1, -0.3, 1.0))}, {'R': 'open', 'L': 'rest'}, MINS, (1, 1, 1), {'spine': SP(0.5)}, d=0.25, keep=True),
      *[TK(r(SHK3 + 0.2 * i), {'R': R5(add(SHAKE, [0, 0.14 if i % 2 else -0.1, 0]))}, {'R': 'grip'}, {**MINS, 'mouth': 'bigsmile' if i % 2 else 'smile'}, (0.97, 1.04, 0.97) if i % 2 else (1.03, 0.96, 1.03), {'spine': SP(0.5)}, d=0.1, keep=True) for i in range(6)],
      TK(r(SHK3 + 1.25), {'R': R5(add(SHAKE, [0, 0.02, 0]))}, {'R': 'grip'}, {**MINS, 'lid': 0.5}, (1, 1, 1), {'spine': SP(0.45)}, d=0.15, keep=True), *blink(r(SHK3 + 1.0), MINS),
      k(r(SHK3 + 0.1), look='camera', lookDur=0.12)]
kh3 = [TK(0.2, face={**HCALM, 'gy': -0.4}, d=0.1, keep=True), *blink(1.05, HCALM), TK(r(SHK3 - 0.15), {'R': R5(add(SHAKE, [-0.02, 0.0, -0.02]))}, {'R': 'open'}, {**HCALM, 'gx': 0.6}, d=0.2, keep=True), k(r(SHK3 - 0.2), look=add(MIN3, [0, 1.6, 0]), lookDur=0.15),
       *[TK(r(SHK3 + 0.2 * i), {'R': R5(add(SHAKE, [-0.02, 0.14 if i % 2 else -0.1, -0.02]))}, {'R': 'grip'}, {**HCALM, 'gx': 0.4, 'lid': 0.1 if i % 2 else 0.4}, sq=(0.97, 1.05, 0.97) if i % 2 else (1.03, 0.95, 1.03), d=0.1, keep=True) for i in range(6)],
       TK(r(SHK3 + 1.25), {'R': R5(add(SHAKE, [-0.02, 0.02, -0.02]))}, {'R': 'grip'}, HCALM, sq=(1, 1, 1), d=0.15, keep=True),
       k(2.6, look='camera', lookDur=0.15), *blink(0.7, HCALM)]
st.shot('S03', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[act('ministre', MIN3, RYM3, 'stand', 'happy', keys=k3), HERO_K(kh3, look='camera')],
        props=[*CORRIDOR('S03', mopts={'plaque': PLQ3, 'glint': [0.75]}), P('ruban3', 'ribbonCut', pos=[0.35, 0, 1.45], opts={'w': 1.0, 'h': 0.95, 'cutAt': CUT3}),
               P('ciseaux3', 'bigScissors', on={'actor': 'ministre', 'hand': 'R', 'offset': [0.0, -0.02, 0.05], 'rot': [0, -PI / 2, 0]}, opts={'len': 0.4, 'snip': [[0, 1], [r(CUT3 - 0.05), 1], [CUT3, 0], [r(CUT3 + 0.3), 0.6]]}, keys=[k(0.0, visible=False), k(0.55, visible=True), k(r(SHK3 - 0.25), visible=False)])],
        cams=[C3])
st.cue('clack', 'S03', PLQ3, 0.3); st.cue('sfx:ding', 'S03', 0.78, 0.2); st.cue('sfx:click', 'S03', CUT3, 0.35); st.cue('sfx:fanfare', 'S03', r(CUT3 + 0.05), 0.15)

# ================================================================= S04 the queue
# 4: the whole country placed its savings in it. Savers with pink piggy banks under their arms queue along the corridor and out of frame; the first
#    feeds coin after coin into the slot; they shuffle forward; slow lateral track; the hero kneels at the left
D4 = st.dur('S04')
QUEUE = [[0.78, 0, 0.92], [1.38, 0, 1.12], [1.98, 0, 1.28], [2.58, 0, 1.42], [3.18, 0, 1.55], [3.78, 0, 1.66]]
RYQ = [-78, -66, -62, -60, -58, -58]
C4 = cam(0.0, [-0.95, 1.55, 5.3], [-0.5, 1.55, 5.3], [0.05, 1.3, 0.7], [0.5, 1.3, 0.7], lens=46)
chk('S04', C4, {**{f'sav{i}': add(QUEUE[i], [0, 2.05, 0]) for i in range(4)}, 'heroFace': add(HERO, [0, 1.6, 0]), 'slot': SLOT, 'sticker': STK, 'can': CAN})
SAVF = {'lid': 0.3, 'mouth': 'line', 'brow': 0.1}
FEEDS = [0.25, 0.75, 1.25, 1.75]
def saver(i):
    p = QUEUE[i]; ry = RYQ[i]; ks = [k(0.0, look=SLOT if i == 0 else 'camera'), TK(0.0, {'L': R5(off(p, ry, 0.2, -0.24, 1.15)), 'R': R5(off(p, ry, 0.12, 0.28, 0.98))}, {'L': 'grip', 'R': 'rest'}, SAVF, d=0.0)]
    if i == 0:
        for t in FEEDS:
            ks += [TK(r(t - 0.15), {'R': R5(add(SLOT, [0.03, 0.0, 0.1]))}, {'R': 'point'}, SAVF, d=0.15, keep=True), TK(r(t + 0.12), {'R': R5(off(p, ry, 0.3, 0.1, 1.15))}, {'R': 'grip'}, SAVF, d=0.15, keep=True)]
    else:
        ks += [k(r(0.35 + 0.22 * i), to=add(p, [-0.12, 0, -0.03]), dur=0.25, glide=True, face=ry), TK(r(0.35 + 0.22 * i), sq=(1.03, 0.97, 1.03), d=0.1, keep=True), TK(r(0.5 + 0.22 * i), sq=(1, 1, 1), d=0.1, keep=True),
               *blink(r(0.9 + 0.17 * i), SAVF), k(r(1.2 + 0.1 * i), look=SLOT, lookDur=0.2)]
    ks += BREATHE(0.1 * i, D4, 0.5, 0.012)
    return act(f'epargnant{i + 1}', p, ry, 'stand', 'neutral', keys=ks)
PIGS4 = [P(f'cochon4{i}', 'piggyBank', on={'actor': f'epargnant{i + 1}', 'hand': 'L', 'offset': [0.0, -0.08, 0.06]}, opts={'s': 1.5}) for i in range(6)]
st.shot('S04', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[*[saver(i) for i in range(6)], HERO_K([TK(0.55, face={**HCALM, 'gx': 0.8, 'gy': -0.5}, d=0.06, keep=True), TK(1.15, face={**HCALM, 'gx': 0.0, 'lid': 0.45}, d=0.1, keep=True), TK(1.6, face={**HCALM, 'gx': 0.7, 'gy': -0.4}, d=0.06, keep=True)], blinks=(1.35,), breathe=(0.0, 2.1))],
        props=[*CORRIDOR('S04', mopts={'coinsAt': [r(t + 0.02) for t in FEEDS]}), *PIGS4], cams=[C4])
for t in FEEDS: st.cue('sfx:clink', 'S04', r(t + 0.1), 0.25)

# ================================================================= S05 close on the slot
# 5: it never gave anything back. Like a real one. Close on the panel and the glass: coins slide into the slot one after another (a saver's hand at
#    the top right); below, the big can never moves; at the bottom the hero's fingers wiggle in the empty flap
D5 = st.dur('S05'); COINS5 = [0.3, 0.85, 1.4, 1.95]
C5 = cam(0.0, [-0.08, 0.95, 2.05], [-0.09, 0.95, 1.92], [-0.02, 0.83, 0.4], [-0.02, 0.83, 0.4], lens=46)
chk('S05', C5, {'slot': SLOT, 'sticker': STK, 'can': CAN, 'flapTop': [FLAP[0], 0.58, 0.4], 'flapBot': [FLAP[0], 0.3, 0.4], 'flapL': [-0.42, 0.44, 0.4], 'panelR': [0.5, 1.0, 0.4]})
SV5 = [0.78, 0, 0.92]
k5 = [k(0.0, look=SLOT), TK(0.0, {'L': R5(off(SV5, -78, 0.2, -0.24, 1.15)), 'R': R5(add(SLOT, [0.03, 0.0, 0.12]))}, {'L': 'grip', 'R': 'point'}, SAVF, d=0.0)]
for t in COINS5: k5 += [TK(r(t - 0.1), {'R': R5(add(SLOT, [0.03, 0.0, 0.07]))}, {'R': 'point'}, SAVF, d=0.08, keep=True), TK(r(t + 0.08), {'R': R5(add(SLOT, [0.06, 0.02, 0.16]))}, {'R': 'point'}, SAVF, d=0.12, keep=True)]
kh5 = [*[TK(r(0.2 + 0.22 * i), {'L': R5(add(FLAPIN, [0.1 * (1 if i % 2 else -1), 0.05 * (1 if i % 3 else -1), 0.03 * (i % 2)]), 1, 0.06)}, {'L': 'open' if i % 2 else 'point'}, d=0.14, keep=True) for i in range(10)]]
st.shot('S05', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[act('epargnant1', SV5, -78, 'stand', 'neutral', keys=k5), HERO_K(kh5)],
        props=[*CORRIDOR('S05', mopts={'coinsAt': COINS5}), P('cochon5', 'piggyBank', on={'actor': 'epargnant1', 'hand': 'L', 'offset': [0.0, -0.08, 0.06]}, opts={'s': 1.5})], cams=[C5])
for t in COINS5: st.cue('sfx:clink', 'S05', r(t + 0.05), 0.2)

# ================================================================= S06 the skyline
# 6: it bought the coffee machine, then the photocopier. Wide along the wall from the right: brass BANQUE plates pop onto the coffee machine on
#    « café », then onto the photocopier on « photocopieuse »: three machines in a row stepping down like a little skyline; the hero kneels small
D6 = st.dur('S06'); POPC6 = r(st.at('S06', 'L06', 6) - 0.05); POPP6 = r(st.at('S06', 'L06', 9) - 0.05)
C6 = fcam(0.0, [-1.6, 0.95, 4.6], {'copL': [PCP[0] - 0.55, 0.95, 0.27], 'copL0': [PCP[0] - 0.55, 0.05, 0.27], 'cofTop': [CMP[0], 1.55, 0.03], 'mtopL': [-0.5, 2.15, 0.4], 'mtopR': [0.5, 2.15, 0.4], 'heroTop': add(HERO, [0, 1.85, 0]), 'plateP': [PCP[0] - 0.1, 0.58, 0.28]}, top=0.1, bottom=0.86, margin=0.05, push=0.9, lenses=range(30, 66))
chk('S06x', C6, {'copierL': [PCP[0] - 0.55, 0.95, PCP[2] + 0.35], 'coffeeTop': [CMP[0], 1.5, CMP[2]], 'machTopL': [-0.5, 2.15, 0.4], 'plateP': [PCP[0] - 0.1, 0.58, PCP[2] + 0.36], 'heroFace': add(HERO, [0, 1.6, 0])})
chk('S06', C6, {'copierL': [PCP[0] - 0.55, 0.95, PCP[2] + 0.35], 'copierTop': [PCP[0], 0.95, PCP[2]], 'coffeeTop': [CMP[0], 1.5, CMP[2]], 'machTop': [0, 2.15, 0.4], 'sandw': [SWP[0] + 0.39, 1.5, 0.22], 'heroFace': add(HERO, [0, 1.6, 0]), 'plateC': [CMP[0], 0.88, CMP[2] + 0.245], 'sticker': STK})
st.shot('S06', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[HERO_K([TK(r(POPC6 - 0.06), face={**HCALM, 'gx': -0.7}, d=0.04, keep=True), k(r(POPC6 + 0.06), look=[CMP[0], 1.0, 0.6], lookDur=0.2), TK(r(POPC6 + 0.06), face={'lid': 0.1, 'mouth': 'O', 'brow': 0.6}, sq=(0.96, 1.05, 0.96), d=0.06, keep=True),
                  TK(r(POPC6 + 0.4), face=HCALM, sq=(1, 1, 1), d=0.12, keep=True), TK(r(POPP6 - 0.06), face={**HCALM, 'gx': -0.8}, d=0.04, keep=True), k(r(POPP6 + 0.06), look=[PCP[0], 0.7, 0.6], lookDur=0.25),
                  TK(r(POPP6 + 0.06), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, sq=(0.95, 1.06, 0.95), d=0.06, keep=True), TK(r(POPP6 + 0.4), face=HCALM, sq=(1, 1, 1), d=0.12, keep=True), k(2.6, look='camera', lookDur=0.2)],
                 blinks=(0.3, 1.5, 2.75), breathe=(0.0, 2.9))],
        props=[CORR('S06'), MACH('S06', glint=[0.2]), SANDW('S06'), COFFEE('S06', [k(r(POPC6 + 0.12), squash=[1.06, 0.92, 1.06], dur=0.35)]), COPIER('S06', [k(r(POPP6 + 0.12), squash=[1.08, 0.9, 1.08], dur=0.35)]), PLATE_C('S06', popAt=POPC6, glint=[r(POPC6 + 0.4)]), PLATE_P('S06', popAt=POPP6, glint=[r(POPP6 + 0.4)])], cams=[C6])
st.cue('clack', 'S06', POPC6, 0.3); st.cue('sfx:ding', 'S06', r(POPC6 + 0.4), 0.15); st.cue('clack', 'S06', POPP6, 0.3); st.cue('sfx:ding', 'S06', r(POPP6 + 0.4), 0.15)

# ================================================================= S07 the director
# 7: it named a director. A box-headed director in an anthracite suit drops into a red armchair beside the hero (the seat squashes), a fat briefcase
#    on his lap, and swings his feet up onto the kneeling hero's back (the hero squashes under them); smug look at us
D7 = st.dur('S07'); SIT7, FEET7 = 0.12, 0.5
ARM = [-1.85, 0, 1.35]; RYA = 50                  # the armchair at the hero's left, a little in front of him
DIR7 = add(ARM, [0, 0.0, 0])
BACK = off(HERO, HRY, -0.04, 0.08, 1.12)          # the top of his bowed back and shoulders (a footstool)
HB7 = {'spine': SP(0.55, -0.15)}
C7 = fcam(0.0, [-0.3, 1.95, 4.4], {'dirTop': add(ARM, [0, 2.65, 0]), 'arm': add(ARM, [-0.45, 0.0, 0.3]), 'kneelTop': add(HERO, [0, 1.8, 0]), 'heroR': add(HERO, [0.35, 0.3, 0.2]), 'stk': STK}, top=0.08, bottom=0.86, push=0.2)
chk('S07', C7, {'dirFace': add(ARM, [0, 1.62, 0]), 'dirDrop': add(ARM, [0, 2.4, 0]), 'heroFace': add(HERO, [0, 1.45, 0]), 'back': BACK, 'can': CAN, 'sticker': STK, 'armchairFoot': ARM})
SMUG = {'lid': 0.45, 'mouth': 'smile', 'brow': 0.2}
def FEET(dy): return {'L': [*add(BACK, [-0.06, 0.06 + dy, 0.09]), 1], 'R': [*add(BACK, [0.06, 0.08 + dy, -0.07]), 1]}
HANDS7 = {'R': R5(off(ARM, RYA, 0.3, 0.16, 0.82)), 'L': R5(off(ARM, RYA, 0.3, -0.16, 0.82))}
k7 = [k(0.0, look='camera'), k(0.0, clip='sit'), k(0.0, to=DIR7, dur=SIT7, ease='in', glide=True, face=RYA),
      TK(0.0, HANDS7, {'R': 'grip', 'L': 'grip'}, {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}, (0.8, 1.25, 0.8), d=0.0),
      TK(SIT7, sq=(1.28, 0.7, 1.28), face={'lid': 0.7, 'mouth': 'line', 'brow': -0.2}, d=0.03, e='out', keep=True),
      TK(r(SIT7 + 0.13), sq=(0.93, 1.08, 0.93), face=SMUG, d=0.08, keep=True), TK(r(SIT7 + 0.26), sq=(1, 1, 1), d=0.1, keep=True),
      TK(r(FEET7 - 0.16), plant=FEET(0.3), bend={'spine': SP(-0.18)}, d=0.16, keep=True),
      TK(FEET7, plant=FEET(0.0), bend={'spine': SP(-0.22)}, face={**SMUG, 'lid': 0.55}, d=0.05, e='in', keep=True),
      TK(r(FEET7 + 0.04), plant=FEET(-0.2), d=0.04, keep=True), TK(r(FEET7 + 0.2), plant=FEET(-0.2), d=0.1, keep=True),
      TK(r(FEET7 + 0.3), plant=FEET(0.08), d=0.08, keep=True), TK(r(FEET7 + 0.42), plant=FEET(-0.02), d=0.08, keep=True), TK(r(FEET7 + 0.55), plant=FEET(0.0), d=0.08, keep=True),
      *blink(1.2, SMUG)]
kh7 = [TK(r(FEET7 + 0.02), sq=(1.16, 0.8, 1.16), face={'lid': 0.85, 'mouth': 'clench', 'brow': -0.6}, d=0.03, e='out', keep=True), TK(r(FEET7 + 0.2), sq=(1.15, 0.81, 1.15), d=0.1, keep=True),
       TK(r(FEET7 + 0.3), sq=(0.9, 1.13, 0.9), face={'lid': 0.0, 'pop': 0.25, 'mouth': 'O', 'brow': 0.6}, d=0.08, e='out', keep=True), TK(r(FEET7 + 0.42), sq=(1.04, 0.96, 1.04), d=0.08, keep=True),
       TK(r(FEET7 + 0.55), sq=(1, 1, 1), face={**HCALM, 'lid': 0.5}, d=0.1, keep=True), k(r(FEET7 + 0.45), look='camera', lookDur=0.12)]
st.shot('S07', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[act('directeur', add(DIR7, [0, 0.75, 0]), RYA, 'sit', 'happy', keys=k7), HERO_K(kh7, bend=HB7, blinks=(0.25,))],
        props=[*CORRIDOR('S07'), P('fauteuil7', 'armchair', pos=ARM, ry=RYA, opts={'color': '#A8352C', 'doily': False, 'sinkAt': SIT7}),
               P('mallette7', 'briefcase', pos=off(ARM, RYA, 0.34, 0.0, 0.92), ry=RYA, rot=[-0.2, 0, 0], scale=1.3, keys=[k(0.0, visible=False), k(r(SIT7 + 0.02), visible=True)])], cams=[C7])
st.cue('thud', 'S07', SIT7, 0.3); st.cue('sfx:boing', 'S07', FEET7, 0.2)

# ================================================================= S08 bankrupt
# 8: bankrupt: the director had drunk it all in coffees. Wide from the front: the coin-box door hangs open; the director holds the coin box at chest
#    height and tips it toward us: empty; a single moth flutters out; at the left a tower of empty coffee cups taller than him leans on the coffee
#    machine beside his armchair; FAILLITE stamps
D8 = st.dur('S08'); TIP8, MOTH8 = 0.75, 0.95
DIR8 = [-2.0, 0, 1.95]; RYD8 = 18
BOX8 = off(DIR8, RYD8, 0.42, 0.0, 1.22)
TOWER = [-1.36, 0, 0.16]
C8 = fcam(0.0, [-0.8, 1.6, 4.6], {'dirTop': add(DIR8, [0, 2.35, 0]), 'dirL': add(DIR8, [-0.33, 1.2, 0]), 'tower': add(TOWER, [-0.24, 3.38, 0]), 'towerL': add(TOWER, [-0.1, 0.5, 0]), 'kneelR': add(HERO, [0.3, 1.8, 0]), 'can': CAN}, top=0.1, bottom=0.8, push=0.25)
chk('S08', C8, {'dirFace': add(DIR8, [0, 2.05, 0]), 'dirTop': add(DIR8, [0, 2.3, 0]), 'box': BOX8, 'mothTop': add(BOX8, [0.75, 0.55, 0.45]), 'towerTop': add(TOWER, [-0.24, 3.35, 0]), 'heroFace': add(HERO, [0, 1.6, 0]), 'can': CAN, 'sticker': STK, 'machTop': [0, 2.15, 0.4]})
DIRF = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.1}
k8 = [k(0.0, look=BOX8), TK(0.0, {'R': R5(add(BOX8, [-0.15, -0.02, 0.0])), 'L': R5(add(BOX8, [0.15, -0.02, 0.0]))}, {'R': 'grip', 'L': 'grip'}, DIRF, d=0.0),
      TK(TIP8, {'R': R5(add(BOX8, [-0.15, 0.08, -0.05])), 'L': R5(add(BOX8, [0.15, 0.08, -0.05]))}, {'R': 'grip', 'L': 'grip'}, {**DIRF, 'gy': 0.5}, (0.98, 1.02, 0.98), d=0.15, keep=True),
      k(r(MOTH8 + 0.1), look=add(BOX8, [0.45, 0.35, 0.25]), lookDur=0.2), TK(r(MOTH8 + 0.15), face={'lid': 0.0, 'mouth': 'O', 'brow': 0.7, 'gy': -0.5}, d=0.08, keep=True),
      k(1.9, look='camera', lookDur=0.15), TK(1.9, face={'lid': 0.4, 'mouth': 'line', 'brow': -0.2}, d=0.12, keep=True), *blink(2.35, {'lid': 0.4, 'mouth': 'line', 'brow': -0.2})]
st.shot('S08', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[act('directeur', DIR8, RYD8, 'stand', 'happy', keys=k8), HERO_K([*blink(0.5, HCALM), k(1.1, look=add(BOX8, [0.45, 0.35, 0.25]), lookDur=0.2), k(1.8, look='camera', lookDur=0.2)])],
        props=[*CORRIDOR('S08', mopts={'boxOpen': 1}), P('fauteuil8', 'armchair', pos=ARM, ry=RYA, opts={'color': '#A8352C', 'doily': False}),
               P('gobelets8', 'cupStack', pos=TOWER, rot=[0, 0, 0.075], opts={'n': 17, 'size': 2.5}),
               P('caisse8', 'coinBox', pos=BOX8, ry=RYD8, rot=[1.0, 0, 0], keys=[k(TIP8, rotTo=[1.4, math.radians(RYD8), 0], dur=0.18, ease='out')]),
               P('mite8', 'moth', pos=[0, 0, 0], opts={'from': add(BOX8, [0.05, 0.04, 0.12]), 'to': add(BOX8, [0.75, 0.55, 0.45]), 'at': MOTH8, 'dur': 1.5, 's': 3.6})], cams=[C8])
st.card('S08', 'FAILLITE', at=0.05)
st.cue('sfx:rattleShort', 'S08', TIP8, 0.25); st.cue('sfx:sniff', 'S08', MOTH8, 0.0)

# ================================================================= S09 the lean starts
# 9: it started to lean. Low and wide: with a long creak the machine begins to lean to its right; the savers in front take one step back together;
#    the hero stays kneeling, arm in the flap
D9 = st.dur('S09'); TILT9 = [[0.0, 0.0], [0.18, -2.5], [0.36, 1.5], [0.52, 0.0], [D9, 16.0]]   # a wobble back, then the lean
SAV9 = [[0.85, 0, 1.3], [1.25, 0, 1.72]]
C9 = fcam(0.0, [0.0, 0.95, 4.2], {'mtopR': tilted([0.5, 2.15, 0.4], 16), 'mtopL': tilted([-0.5, 2.15, 0.4], 16), 'heroL': add(HERO, [-0.3, 1.0, 0]), 'kneelTop': add(HERO, [0, 1.85, 0]), 's0': add(SAV9[0], [0, 2.1, 0]), 'feet': add(HERO, [0, 0.0, 0.2])}, top=0.08, bottom=0.88, push=0.25)
chk('S09', C9, {'machTopR': tilted([0.5, 2.15, 0.4], 12), 'machTopL': tilted([-0.5, 2.15, 0.4], 12), 'heroFace': add(HERO, [0, 1.6, 0]), **{f'sav{i}': add(SAV9[i], [0, 2.05, 0]) for i in range(2)}, 'can': tilted(CAN, 6), 'sticker': tilted(STK, 6)})
def saver9(i):
    p = SAV9[i]; ry = yaw(p, [0.2, 0, 0.0]); back = add(p, [0.12 * math.copysign(1, p[0] - 0.2), 0, 0.32])
    return act(f'epargnant{i + 1}', p, ry, 'stand', 'neutral', keys=[k(0.0, look=[0.2, 1.8, 0.2]), TK(0.0, {'L': R5(off(p, ry, 0.2, -0.24, 1.15)), 'R': R5(off(p, ry, 0.12, 0.28, 0.98))}, {'L': 'grip', 'R': 'rest'}, SAVF, d=0.0),
        *HOP9(p, back), TK(0.55, face={'lid': 0.0, 'pop': 0.45, 'mouth': 'O', 'brow': 1.0}, d=0.04, keep=True), TK(1.1, face={'lid': 0.1, 'mouth': 'O', 'brow': 0.6}, d=0.12, keep=True)])
def HOP9(p, back):   # one hop back together: up on an ease-out, down on an ease-in, stretch on take-off, squash on landing (toon keys keep the hands)
    mk, tk = hops(0.55, [[p[0], p[2]], [back[0], back[2]]], [0.28], 0.34)
    return [*[dict(x, glide=True) for x in mk], *[dict(x, keepPose=True) for x in tk], TK(0.95, sq=(1, 1, 1), d=0.1, keep=True)]
kh9 = [*[TK(r(0.1 + 0.3 * i), {'L': R5(tilted(FLAPIN, kvp(TILT9, 0.1 + 0.3 * i)), 1, 0.06)}, {'L': 'grip'}, {**HCALM, 'gx': 0.7, 'gy': -0.8, 'brow': 0.4}, d=0.3, e='linear', keep=True) for i in range(5)], *blink(1.05, {**HCALM, 'gx': 0.7, 'gy': -0.8, 'brow': 0.4})]
st.shot('S09', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[*[saver9(i) for i in range(2)], HERO_K(kh9)],
        props=[*CORRIDOR('S09', mopts={'tilt': TILT9, 'creak': [[0.1, D9]]}), *[P(f'cochon9{i}', 'piggyBank', on={'actor': f'epargnant{i + 1}', 'hand': 'L', 'offset': [0.0, -0.08, 0.06]}, opts={'s': 1.5}) for i in range(2)]], cams=[C9])
st.cue('sfx:squeak', 'S09', 0.1, 0.3); st.cue('sfx:stretch', 'S09', 0.5, 0.2)

# ================================================================= S10 the crush
# 10: leaning, it crushed the sandwich machine. From the front right: the machine falls further onto the small teal sandwich machine and flattens it
#     into a drawn flat shape (a thud, dust); one big bright sandwich shoots out across the floor toward us; the hero's arm stretches with the flap
D10 = st.dur('S10'); FALL10 = r(st.at('S10', 'L10', 4) - 0.02)
TILT10 = [[0.0, 16.0], [r(FALL10 - 0.35), 18.0], [FALL10, 62.0], [r(FALL10 + 0.12), 59.0], [r(FALL10 + 0.25), 62.0]]
SAND0 = [1.15, 0, 0.45]; SAND1 = [1.72, 0, 1.0]
C10 = fcam(0.0, [1.5, 1.05, 4.6], {'mtop1': tilted([-0.5, 2.15, 0.4], 62), 'mcrush': tilted([0.5, 1.2, 0.4], 62), 'mtop0': tilted([-0.5, 2.15, 0.4], 12), 'heroL': add(HERO, [-0.3, 1.2, 0]), 'kneelTop': add(HERO, [0, 1.85, 0]), 'sand1': add(SAND1, [0.15, 0.05, 0.1])}, top=0.1, bottom=0.86, push=0.3)
chk('S10', C10, {'machTop0': tilted([0.5, 2.15, 0.4], 12), 'machTop1': tilted([-0.5, 2.15, 0.4], 62), 'machTopR1': tilted([0.5, 2.15, 0.4], 62), 'heroFace': add(HERO, [0, 1.6, 0]), 'sandwTop': [SWP[0], 1.5, 0.22], 'sandwich1': SAND1, 'flap62': tilted(FLAPIN, 62), 'sticker62': tilted(STK, 62)})
kh10 = [TK(0.0, {'L': R5(tilted(FLAPIN, 16), 1, 0.06)}, {'L': 'grip'}, {**HCALM, 'gx': 0.5, 'gy': -0.5}, d=0.0, keep=True),
        TK(r(FALL10 - 0.35), {'L': R5(tilted(FLAPIN, 18), 1, 0.06)}, {'L': 'grip'}, {**HCALM, 'gx': 0.5, 'gy': -0.5}, d=0.4, keep=True),
        TK(FALL10, {'L': R5(tilted(FLAPIN, 62), 1, 0.06)}, {'L': 'grip'}, {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.8}, (0.94, 1.06, 0.94), {'spine': SP(0.1, -0.45), 'neck': SP(-0.2, 0.42)}, d=0.3, e='in', keep=True),
        TK(r(FALL10 + 0.4), face={'lid': 0.3, 'mouth': 'line', 'brow': 0.0}, sq=(1, 1, 1), d=0.2, keep=True), k(r(FALL10 + 0.2), look=SAND1, lookDur=0.25), k(2.4, look='camera', lookDur=0.2), *blink(2.7, HCALM)]
st.shot('S10', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[HERO_K(kh10)],
        props=[CORR('S10'), MACH('S10', tilt=TILT10, creak=[[0.0, r(FALL10 - 0.1)], [r(FALL10 + 0.3), D10]]), SANDW('S10', crush=[[r(FALL10 - 0.12), 0.0], [r(FALL10 + 0.02), 1.0]]), COFFEE('S10'), COPIER('S10'),
               P('sandwich10', 'bigSandwich', pos=SAND0, ry=20, opts={'s': 1.3}, keys=[k(0.0, visible=False), k(r(FALL10 + 0.03), visible=True), k(r(FALL10 + 0.03), to=SAND1, dur=0.9, ease='out'), k(r(FALL10 + 0.03), rotTo=[0, math.radians(20 + 300), 0], dur=0.9, ease='out')]),
               P('poussiere10', 'softDust', pos=[1.2, 0.05, 0.1], opts={'at': FALL10, 'n': 10, 'r': 0.9})], cams=[C10])
st.cue('sfx:squeak', 'S10', 0.0, 0.25); st.cue('thud', 'S10', FALL10, 0.6); st.cue('sfx:crunch', 'S10', FALL10, 0.4); st.cue('whoosh', 'S10', r(FALL10 + 0.05), 0.2, 0.5, 300, 1500)

# ================================================================= S11 too big to fall
# 11: too big to fall. Front: two soldiers in plain olive (no insignia, bare heads) and a minister in a plain sash rush in from the right and push the
#     machine back to forty-five degrees with their shoulders and hands, straining; the hero still kneels at its foot, arm stretched into the flap
D11 = st.dur('S11'); STOP11 = 0.4
TILT11 = [[0.0, 62.0], [STOP11, 42.0], [r(STOP11 + 0.12), 49.0], [r(STOP11 + 0.26), 43.5], [r(STOP11 + 0.4), 45.5], [r(STOP11 + 0.55), 45.0]]   # the catch: past 45, back, settle
def underside(x, th=45.0, z=0.36): return [x, r((x - 0.5) / math.tan(math.radians(th))), z]
MIN11 = [1.2, 0, 0.98]; SOLD11 = [[1.86, 0, 0.55], [2.5, 0, 0.42]]
C11 = fcam(0.0, [1.5, 1.15, 4.0], {'mtopL': tilted([-0.5, 2.15, 0.4], 45), 'mtopR': tilted([0.5, 2.15, 0.4], 45), 'arm': tilted(FLAPIN, 45), 's1': add(SOLD11[0], [0, 1.95, 0]),
          's2r': add(SOLD11[1], [0.25, 1.2, 0]), 's2': add(SOLD11[1], [0, 2.1, 0]), 'min': add(MIN11, [0, 1.9, 0]), 'feet': add(MIN11, [0, 0.1, 0.2])}, top=0.08, bottom=0.86, push=0.3)
chk('S11', C11, {'machTopL45': tilted([-0.5, 2.15, 0.4], 45), 'machTopR45': tilted([0.5, 2.15, 0.4], 45), 'heroFace': add(HERO, [0, 1.45, 0]), 'minFace': add(MIN11, [0, 1.6, 0]), 's1face': add(SOLD11[0], [0, 1.75, 0]), 's2face': add(SOLD11[1], [0, 2.0, 0]), 'flap45': tilted(FLAPIN, 45), 'sticker45': tilted(STK, 45)})
PUSHF = {'lid': 0.4, 'mouth': 'clench', 'brow': -0.8}
def pusher(id_, p, ry, hands, crouch, ent, back=0.0):
    """one who rushes in and holds the leaning machine up: faces the lens, crouched under it (sq), both palms up against it, straining (shiver, a pumping squash)"""
    sq0 = (1 + (1 - crouch) * 0.5, crouch, 1 + (1 - crouch) * 0.5)
    ks = [k(0.0, look='camera'), k(0.0, to=p, dur=STOP11, ease='out', glide=True, face=ry), TK(0.0, {'R': R5(add(hands['R'], ent)), 'L': R5(add(hands['L'], ent))}, {'R': 'open', 'L': 'open'}, {'lid': 0.0, 'pop': 0.3, 'mouth': 'O', 'brow': 0.7}, (0.8, 1.2, 0.8), {'spine': SP(back + 0.35)}, d=0.0),
          TK(r(STOP11 - 0.06), {'R': R5(hands['R']), 'L': R5(hands['L'])}, {'R': 'open', 'L': 'open'}, sq=(0.86, 1.12, 0.86), bend={'spine': SP(back + 0.3)}, d=0.3, keep=True),
          TK(STOP11, sq=(sq0[0] * 1.16, crouch * 0.82, sq0[2] * 1.16), face={'lid': 0.0, 'pop': 0.45, 'mouth': 'clench', 'brow': -1.0}, bend={'spine': SP(back)}, d=0.04, e='out', keep=True), TK(r(STOP11 + 0.12), sq=(sq0[0] * 0.96, crouch * 1.05, sq0[2] * 0.96), d=0.08, keep=True), k(STOP11, fx={'shiver': True})]
    for n in range(4): ks.append(TK(r(STOP11 + 0.2 + 0.18 * n), sq=sq0 if n % 2 else (sq0[0] * 1.03, crouch * 0.97, sq0[2] * 1.03), face={'lid': 0.0, 'pop': 0.3 if n % 2 else 0.4, 'mouth': 'clench', 'brow': -1.0}, d=0.12, keep=True))
    return act(id_, add(p, ent), ry, 'stand', 'determined', keys=ks)
st.shot('S11', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[
        pusher('ministre', MIN11, -35, {'R': [1.02, 0.95, 0.42], 'L': [1.38, 1.0, 0.42]}, 0.84, [2.6, 0, 0.3], 0.45),
        pusher('sold1', SOLD11[0], -40, {'R': underside(1.68), 'L': underside(2.0)}, 0.8, [2.4, 0, 0.2], 0.5),
        pusher('sold2', SOLD11[1], -55, {'R': [2.06, 1.53, 0.36], 'L': [2.14, 1.42, 0.1]}, 0.9, [2.2, 0, 0.2], 0.6),
        HERO_K([TK(0.0, {'L': R5(tilted(FLAPIN, 62), 1, 0.06)}, {'L': 'grip'}, {**HCALM, 'gx': 0.6}, bend={'spine': SP(0.1, -0.45), 'neck': SP(-0.2, 0.42)}, d=0.0, keep=True),
                TK(STOP11, {'L': R5(tilted(FLAPIN, 45), 1, 0.06)}, {'L': 'grip'}, {**HCALM, 'gx': 0.6}, d=0.35, keep=True), k(0.3, look=[1.6, 1.6, 0.8], lookDur=0.2), k(1.0, look='camera', lookDur=0.15)], bend={'spine': SP(0.1, -0.45), 'neck': SP(-0.2, 0.42)}, blinks=(0.75,))],
        props=[CORR('S11'), MACH('S11', tilt=TILT11, creak=[[STOP11, D11]]), SANDW('S11', flat=True), COFFEE('S11'), COPIER('S11'), P('sandwich11', 'bigSandwich', pos=SAND1, ry=320, opts={'s': 1.3})], cams=[C11])
st.cue('sfx:stepRun', 'S11', 0.0, 0.3); st.cue('thud', 'S11', STOP11, 0.45); st.cue('sfx:grunt', 'S11', r(STOP11 + 0.05), 0.25)

# ================================================================= S12 the bailout
# 12: the State bailed it out: two billion in coins. Still in the corridor: a giant funnel jammed in the coin slot; two soldiers tip plain sacks into
#     its mouth, gold coins pour, heaps grow on the floor, and the machine slowly comes back upright
D12 = st.dur('S12'); TILT12 = [[0.0, 45.0], [0.5, 45.0], [1.0, 39.0], [1.55, 20.0], [2.05, 3.0], [2.22, -1.5], [2.38, 0.6], [r(D12), 0.0]]   # the coins first, then it rises with the heap, a settle
FMOUTH0 = [0.25, r(1.2 + math.cos(0.5) * 1.01), r(0.412 + math.sin(0.5) * 1.01)]   # the funnel's mouth (props_distributeur: tipped 0.5 rad, 1.01 m from the slot)
def mouth(th): return tilted(FMOUTH0, th)
def tilt_at(t): return kvp(TILT12, t)
CRATE = [0.98, 0, 1.08]; SOLDA = [0.98, 0.42, 1.08]; SOLDB = [1.62, 0, 1.3]
HEAP1 = [0.85, 0, 1.15]; HEAP2 = [0.2, 0, 1.35]
C12 = fcam(0.0, [-1.0, 1.55, 5.4], {'mouth0': add(mouth(0), [0, 0.15, 0]), 'mouthL': add(mouth(0), [-0.45, 0, 0]), 'sA': add(SOLDA, [0, 2.3, 0]), 'sAr': add(SOLDA, [0.3, 1.2, 0]), 'sB': add(SOLDB, [0, 2.3, 0]), 'sBr': add(SOLDB, [0.3, 1.0, 0]),
          'heroL': add(HERO, [-0.35, 1.0, 0]), 'mtop45': tilted([0.5, 2.15, 0.4], 45), 'heap': [0.75, 0.05, 1.45]}, top=0.08, bottom=0.86, push=0.2)
chk('S12', C12, {'mouth45': mouth(45), 'mouth0': mouth(0), 'sAface': add(SOLDA, [0, 2.05, 0]), 'sBface': add(SOLDB, [0, 2.05, 0]), 'heroFace': add(HERO, [0, 1.45, 0]), 'heap1': add(HEAP1, [0, 0.3, 0]), 'sandw': [SWP[0], 0.15, 0.22], 'sticker0': STK, 'can0': CAN, 'machTop0': [0, 2.15, 0.4]})
TIMES12 = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, r(D12)]
SKA = [[t, add(mouth(tilt_at(t)), [0.24, 0.16 + (0.14 if t == 0.0 else 0.0), 0.06])] for t in TIMES12]   # lifted at 0 (the anticipation), tipped from 0.25
HOLDB = off(SOLDB, -30, 0.3, 0.0, 0.95)
def pourerA():
    ry = -50; ks = [k(0.0, look=SKA[0][1])]
    for i_, (t, q) in enumerate(SKA): ks.append(TK(t, {'R': R5(add(q, [-0.08, -0.04, 0.12])), 'L': R5(add(q, [0.12, 0.02, 0.06]))}, {'R': 'grip', 'L': 'grip'}, PUSHF if t < 1.0 else {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, d=0.0 if i_ == 0 else 0.25, e='linear', keep=i_ > 0))
    ks += [k(1.6, look='camera', lookDur=0.2), *blink(2.1, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}), *BREATHE(0.0, D12, 0.4, 0.015)]
    return act('sold1', SOLDA, ry, 'stand', 'determined', keys=ks)
def holderB():
    ks = [k(0.0, look=mouth(10)), TK(0.0, {'R': R5(add(HOLDB, [-0.12, 0, 0])), 'L': R5(add(HOLDB, [0.12, 0, 0]))}, {'R': 'grip', 'L': 'grip'}, PUSHF, d=0.0),
          k(1.3, look='camera', lookDur=0.2), TK(1.3, face={'lid': 0.3, 'mouth': 'line', 'brow': -0.2}, d=0.1, keep=True), *blink(1.9, {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}), *BREATHE(0.0, D12, 0.45, 0.015)]
    return act('sold2', SOLDB, -30, 'stand', 'determined', keys=ks)
STREAMA = [[t, add(q, [-0.05, -0.12, -0.02]), add(mouth(tilt_at(t)), [0.0, -0.05, 0.0])] for t, q in SKA]
kh12 = [TK(0.0, {'L': R5(tilted(FLAPIN, 45), 1, 0.06)}, {'L': 'grip'}, HCALM, bend={'spine': SP(0.1, -0.45), 'neck': SP(-0.2, 0.42)}, d=0.0, keep=True),
        *[TK(t, {'L': R5(tilted(FLAPIN, tilt_at(t)), 1, 0.06)}, {'L': 'grip'}, HCALM, bend={'spine': SP(0.1 + 0.18 * min(1, t / 1.5), -0.45 + 0.23 * min(1, t / 1.5))}, d=0.25, e='linear', keep=True) for t in TIMES12[1:]],
        k(1.7, look=mouth(0), lookDur=0.25), *blink(1.2, HCALM), k(2.3, look='camera', lookDur=0.2)]
st.shot('S12', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[pourerA(), holderB(), HERO_K(kh12, bend={'spine': SP(0.1, -0.45), 'neck': SP(-0.2, 0.42)})],
        props=[CORR('S12'), MACH('S12', tilt=TILT12, funnel=True, creak=[[0.0, 1.0]]), SANDW('S12', flat=True), COFFEE('S12'), COPIER('S12'), P('sandwich12', 'bigSandwich', pos=SAND1, ry=320, opts={'s': 1.3}),
               P('caisse12', 'woodCrate', pos=CRATE, ry=-50, opts={'h': 0.42}),
               P('sacA12', 'plainSack', pos=SKA[0][1], rot=[1.4, 0, 0.3], opts={'open': True, 's': 0.95, 'color': '#6A4C2C'}, keys=[*[k(t, to=q, dur=0.25, ease='linear') for t, q in SKA[1:]], k(0.1, rotTo=[2.55, 0, 0.3], dur=0.16, ease='in'),
                *[k(r(0.3 + 0.12 * j), rotTo=[2.3 + (0.18 if j % 2 else -0.12), 0, 0.3 + (0.12 if j % 2 else -0.1)], dur=0.1) for j in range(14)]]),
               P('sacB12', 'plainSack', pos=add(HOLDB, [0, 0.12, 0.05]), opts={'s': 0.95, 'color': '#6A4C2C'}),
               P('flotA12', 'coinStream', pos=[0, 0, 0], opts={'path': STREAMA, 't0': 0.24, 't1': D12, 'n': 22}),
               P('tas12a', 'goldHeap', pos=HEAP1, opts={'R': 0.4, 'H': 0.3, 'grow': [0.45, 2.1], 'seed': 3}), P('tas12b', 'goldHeap', pos=HEAP2, opts={'R': 0.3, 'H': 0.2, 'grow': [0.6, 2.4], 'seed': 4})], cams=[C12])
st.cue('sfx:cash', 'S12', 0.1, 0.3); st.cue('sfx:rattle', 'S12', 0.3, 0.25); st.cue('sfx:squeak', 'S12', 1.0, 0.2)

# ================================================================= S13 nothing for the sandwich machine
# 13: the sandwich machine, it got nothing. Low and static on the flattened sandwich machine on the floor; behind it the drinks machine upright with
#     its funnel and the hero kneeling; one single coin rolls off the heap toward the flat machine, wobbles, stops just short and falls flat; nobody looks
D13 = st.dur('S13'); ROLL13 = [0.25, 1.45]
COIN0 = [0.5, 1.05]; COIN1 = [0.78, 0.56]                  # it stops 0.3 m short of the flat machine (its front at z 0.26)
C13 = cam(0.0, [2.8, 0.3, 1.7], [2.72, 0.3, 1.62], [-0.06, 0.33, 0.22], [-0.06, 0.34, 0.22], lens=54)   # at floor height, close on the flat machine; the coin crosses the frame
chk('S13', C13, {'sandwL': [SWP[0] - 0.5, 0.09, 0.22], 'sandwR': [SWP[0] + 0.5, 0.09, 0.22], 'coin0': [COIN0[0], 0.05, COIN0[1]], 'coin1': [COIN1[0], 0.05, COIN1[1]], 'heroFace': add(HERO, [0, 1.6, 0]), 'sticker': STK, 'can': CAN, 'heap': add(HEAP1, [0, 0.3, 0])})
st.shot('S13', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[HERO_K([TK(1.0, face={**HCALM, 'gx': -0.5, 'gy': -0.4}, d=0.1, keep=True), k(1.15, look=[-0.6, 2.4, 1.5], lookDur=0.4), TK(2.3, face=HCALM, d=0.1, keep=True), k(2.35, look='camera', lookDur=0.25)], look=[0.6, 1.8, 3.0], blinks=(0.6, 1.7), breathe=(0.0, 2.6))],
        props=[CORR('S13'), MACH('S13', funnel=True), SANDW('S13', flat=True), COFFEE('S13'), COPIER('S13'), P('sandwich13', 'bigSandwich', pos=[2.25, 0, 0.3], ry=320, opts={'s': 1.3}),
               P('tas13a', 'goldHeap', pos=HEAP1, opts={'R': 0.4, 'H': 0.3, 'seed': 3}), P('tas13b', 'goldHeap', pos=HEAP2, opts={'R': 0.3, 'H': 0.2, 'seed': 4}),
               P('piece13', 'rollCoin', pos=[0, 0, 0], opts={'from': COIN0, 'to': COIN1, 't0': ROLL13[0], 't1': ROLL13[1], 'r': 0.09, 'curve': 0.14, 'wob': 0.62})], cams=[C13])
st.cue('sfx:rattleShort', 'S13', r(ROLL13[1] + 0.62), 0.3); st.cue('sfx:tick', 'S13', r(ROLL13[1] + 0.2), 0.15); st.cue('sfx:tick', 'S13', r(ROLL13[1] + 0.42), 0.15)

# ================================================================= S14 the can
# 14: the can finally fell; it was the director's bonus. Close on the bottom spiral: it turns, the big bright can drops into the flap onto the hero's
#     hand; the camera pulls back as the director leans in, takes it out of the flap and stands holding it at chest height, label-less bands to the
#     flashes going off at the lens
D14 = st.dur('S14'); DROP14 = 0.15; TAKE14 = 1.35; SHOW14 = 1.95
DIR14 = [0.72, 0, 1.0]; RYD14 = -25; DIR14A = [1.2, 0, 1.25]; DIR14B = [0.2, 0, 1.5]   # B: where he ends, square to the lens
CANHOLD = off(DIR14B, 0, 0.3, 0.0, 1.3)
C14 = cam(0.0, [0.22, 0.82, 2.15], [0.2, 1.45, 4.6], [-0.04, 0.68, 0.32], [-0.2, 1.33, 0.9], lens=44, ease='inOut')   # one move: close on the spiral, pulling back to the bonus pose
C14b = C14
chk('S14', C14, {'can': CAN, 'flap': FLAP, 'sticker': STK, 'flapBot': [FLAP[0], 0.3, 0.4]})
chk('S14b', C14b, {'can': CANHOLD, 'dirFace': add(DIR14B, [0, 2.05, 0]), 'dirTop': add(DIR14B, [0, 2.3, 0]), 'heroFace': add(HERO, [0, 1.6, 0]), 'sticker': STK, 'flashL': [-0.3, 2.3, 1.5], 'flashR': [0.82, 2.3, 1.6], 'sandw': [SWP[0], 0.12, 0.22]})
INFLAP = add(FLAPIN, [0.04, -0.04, 0.03])
k14 = [k(0.0, look=FLAP), k(0.75, to=DIR14, dur=0.4, glide=True, face=RYD14), k(r(TAKE14 + 0.15), to=DIR14B, dur=0.4, glide=True, face=0), TK(0.0, {'R': R5(off(DIR14, RYD14, 0.05, 0.3, 0.98)), 'L': R5(off(DIR14, RYD14, 0.05, -0.3, 0.98))}, {'R': 'rest', 'L': 'rest'}, DIRF, d=0.0),
       TK(r(TAKE14 - 0.3), {'R': R5(add(INFLAP, [0.1, 0.02, 0.06]))}, {'R': 'open'}, DIRF, (1, 1, 1), {'spine': SP(0.7)}, d=0.3, keep=True),
       TK(TAKE14, {'R': R5(add(INFLAP, [0.1, 0.02, 0.06]))}, {'R': 'grip'}, DIRF, d=0.05, keep=True),
       TK(SHOW14, {'R': R5(add(CANHOLD, [-0.06, -0.03, 0.0])), 'L': R5(add(CANHOLD, [0.07, -0.03, 0.0]))}, {'R': 'grip', 'L': 'open'}, {'lid': 0.3, 'mouth': 'bigsmile', 'brow': 0.4}, (0.97, 1.04, 0.97), {'spine': SP(0.0), 'neck': SP(0.0)}, d=0.3, keep=True),
       k(r(SHOW14 - 0.1), look='camera', lookDur=0.2), TK(2.3, sq=(1, 1, 1), d=0.2, keep=True), *[TK(t, face={'lid': 0.6, 'mouth': 'bigsmile', 'brow': 0.6}, d=0.03, keep=True) for t in (2.06, 2.21, 2.39, 2.56, 2.73, 2.91)],
       *[TK(r(t + 0.08), face={'lid': 0.3, 'mouth': 'bigsmile', 'brow': 0.4}, d=0.05, keep=True) for t in (2.06, 2.21, 2.39, 2.56, 2.73, 2.91)]]
LAND14 = r(DROP14 + 0.7)
KEEP14 = {'reach': {'L': R5(add(FLAPIN, [0.0, -0.03, 0.0]), 1, 0.06), 'R': R5(HREST)}, 'hands': {'L': 'grip', 'R': 'rest'}, 'bend': HBEND}
kh14 = [TK(r(LAND14 + 0.02), {'L': R5(add(FLAPIN, [0.0, -0.03, 0.0]), 1, 0.06)}, {'L': 'grip'}, d=0.06, keep=True),
        *doubleTake(r(LAND14 + 0.04), FLAP, keep=KEEP14, back='camera', pop=0.6, blank=0.22, hold=0.3),
        TK(r(TAKE14 + 0.15), face={'lid': 0.4, 'mouth': 'line', 'brow': -0.3, 'gx': 0.6, 'gy': -0.3}, sq=(1, 1, 1), d=0.15, keep=True), k(r(TAKE14 + 0.1), look=add(DIR14, [0, 1.9, 0]), lookDur=0.2), k(2.6, look='camera', lookDur=0.2)]
st.shot('S14', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[act('directeur', DIR14A, RYD14, 'stand', 'happy', keys=k14), HERO_K(kh14)],
        props=[CORR('S14'), MACH('S14', canDrop=DROP14, canHide=TAKE14), SANDW('S14', flat=True), COFFEE('S14'), COPIER('S14'),
               P('canette14', 'bigCan', on={'actor': 'directeur', 'hand': 'R', 'offset': [0.0, -0.02, 0.06], 'rot': [0, 0, 0]}, keys=[k(0.0, visible=False), k(TAKE14, visible=True)]),
               P('bloom14a', 'camFlash', pos=[-0.5, 2.2, 1.9], opts={'w': 1.0, 'at': [2.05, 2.72]}), P('bloom14b', 'camFlash', pos=[0.85, 2.3, 1.8], opts={'w': 0.9, 'at': [2.38]}),
               P('flash14', 'flashBursts', pos=[-0.3, 2.3, 1.5], opts={'n': 3, 'w': 0.3, 'h': 0.6, 'at': [2.05, 2.38, 2.72], 'life': 0.12}), P('flash14b', 'flashBursts', pos=[0.82, 2.3, 1.6], opts={'n': 3, 'w': 0.3, 'h': 0.6, 'at': [2.2, 2.55, 2.9], 'life': 0.12})], cams=[C14])
st.cue('sfx:rattleShort', 'S14', DROP14, 0.3); st.cue('clang', 'S14', LAND14, 0.4); st.cue('sfx:boing', 'S14', r(LAND14 + 0.42), 0.2); st.cue('sfx:shutter', 'S14', 2.05, 0.3); st.cue('sfx:shutter', 'S14', 2.4, 0.3); st.cue('sfx:shutter', 'S14', 2.72, 0.3)

# ================================================================= S15 the counter
# 15: this man claimed his coin. A small counter with a glass window now stands before the machine's right side, a clerk behind the glass; the hero
#     pulls his arm out of the flap at last, stands, and slaps his palm on the counter (the counter jumps); he looks at us
D15 = st.dur('S15'); OUT15, UP15, SLAP15 = 0.12, 0.35, 0.95
CNT = [0.62, 0, 1.38]; RYC = -70
CLERK = off(CNT, RYC, -0.55, 0.0); RYK = RYC
HSTAND = [-0.02, 0, 1.5]; RYH15 = 0
PALM = off(CNT, RYC, 0.12, 0.25, 1.04)
C15 = fcam(0.0, [-0.6, 1.6, 5.2], {'heroTop': add(HSTAND, [0, 2.35, 0]), 'kneelTop': add(HERO, [0, 1.8, 0]), 'heroL': add(HERO, [-0.3, 1.0, 0]), 'clerkTop': add(CLERK, [0, 2.3, 0]), 'clerkR': add(CLERK, [0.3, 1.2, 0]), 'glassTop': add(CNT, [0, 1.85, 0]), 'stk': STK}, push=0.2)
chk('S15', C15, {'heroFace': add(HSTAND, [0, 2.05, 0]), 'heroTop': add(HSTAND, [0, 2.3, 0]), 'kneelFace': add(HERO, [0, 1.6, 0]), 'clerkFace': add(CLERK, [0, 2.05, 0]), 'palm': PALM, 'glassTop': add(CNT, [0, 1.83, 0]), 'sticker': STK, 'sandw': [SWP[0], 0.12, 0.22]})
CLF = {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}
CLERKKEYS = lambda extra=(): [k(0.0, look='camera'), TK(0.0, {'R': R5(off(CLERK, RYK, 0.38, 0.18, 1.02)), 'L': R5(off(CLERK, RYK, 0.38, -0.2, 1.02))}, {'R': 'rest', 'L': 'rest'}, CLF, d=0.0), *extra]
k15 = [TK(OUT15, {'L': R5(add(FLAPIN, [0.0, 0.0, 0.3]), 1, 0.06)}, {'L': 'grip'}, {'lid': 0.2, 'mouth': 'clench', 'brow': -0.6}, d=0.15, keep=True),
       k(UP15, clip='stand', blend=0.2), k(UP15, to=HSTAND, dur=0.4, glide=True, face=RYH15),
       TK(r(UP15 + 0.05), {'L': R5(off(HSTAND, RYH15, 0.2, -0.3, 1.0)), 'R': R5(off(HSTAND, RYH15, 0.05, 0.3, 0.98))}, {'L': 'open', 'R': 'rest'}, {'lid': 0.2, 'mouth': 'line', 'brow': -0.7}, (1, 1, 1), {'spine': SP(0.0)}, d=0.3, keep=True),
       TK(0.58, {'L': R5(add(PALM, [-0.2, 1.05, 0.25]))}, {'L': 'open'}, {'lid': 0.0, 'mouth': 'clench', 'brow': -0.9}, (0.86, 1.18, 0.86), {'spine': SP(-0.18)}, d=0.12, e='out', keep=True),
       TK(0.7, {'L': R5(add(PALM, [-0.2, 1.12, 0.25]))}, {'L': 'open'}, {'lid': 0.0, 'mouth': 'clench', 'brow': -1.0}, (0.85, 1.2, 0.85), {'spine': SP(-0.2)}, d=0.1, keep=True),
       TK(0.84, {'L': R5(add(PALM, [-0.18, 1.08, 0.25]))}, {'L': 'open'}, {'lid': 0.05, 'mouth': 'clench', 'brow': -1.0}, (0.86, 1.19, 0.86), {'spine': SP(-0.2)}, d=0.1, keep=True),
       TK(SLAP15, {'L': R5(PALM, 1, 0.08)}, {'L': 'open'}, {'lid': 0.1, 'mouth': 'scream', 'brow': -0.9, 'jaw': 0.5}, (1.12, 0.88, 1.12), {'spine': SP(0.25)}, d=0.04, e='in', keep=True),
       TK(r(SLAP15 + 0.12), sq=(0.97, 1.03, 0.97), d=0.08, keep=True),
       TK(r(SLAP15 + 0.25), face={'lid': 0.3, 'mouth': 'line', 'brow': -0.7}, sq=(1, 1, 1), bend={'spine': SP(0.1)}, d=0.15, keep=True), k(r(UP15 + 0.1), look=add(CLERK, [0, 2.0, 0]), lookDur=0.15), k(r(SLAP15 - 0.02), look='camera', lookDur=0.08), *blink(1.45, {'lid': 0.3, 'mouth': 'line', 'brow': -0.7})]
st.shot('S15', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[HERO_K(k15, look=FLAP), act('guichet', CLERK, RYK, 'stand', 'neutral', keys=CLERKKEYS([*react(r(SLAP15 + 0.02), 0.6), *blink(1.4, CLF)]))],
        props=[*CORRIDOR('S15', crushed=True, mopts={'canHide': 0.0, 'flapIn': [[0.0, 1.0], [0.3, 0.0]]}), P('comptoir15', 'glassCounter', pos=CNT, ry=RYC, opts={'w': 1.2}, keys=[k(SLAP15, squash=[1.03, 0.94, 1.03], dur=0.3)])], cams=[C15])
st.cue('sfx:squeak', 'S15', OUT15, 0.2); st.cue('sfx:stretch', 'S15', 0.58, 0.2); st.cue('thud', 'S15', SLAP15, 0.5)

# ================================================================= S16 refused
# 16: refused: it is invested for forty years. Closer on the clerk behind the glass: he stamps a sheet (REFUSÉ) and slides it under the glass toward
#     the hero; behind him on the wall a chart: one thick line climbing very slowly to a small piggy bank at its far end, no labels and no digits
D16 = st.dur('S16'); STAMP16 = 0.16; SLIDE16 = [0.45, 0.95]
CHART = [2.15, 1.8, WALLZ + 0.03]
C16 = fcam(0.0, [0.3, 2.0, 3.2], {'clerkTop': add(CLERK, [0, 2.3, 0]), 'clerkL': add(CLERK, [-0.3, 1.2, 0]), 'chL': add(CHART, [-0.55, 0.36, 0]), 'chR': add(CHART, [0.55, -0.36, 0]), 'sheet': add(CNT, [-0.25, 0.95, 0.15]), 'sheetL': add(CNT, [-0.62, 1.35, 0.25]), 'sheetTop': add(CNT, [0.0, 1.55, 0.1])}, top=0.1, bottom=0.76, margin=0.06, push=0.15)
chk('S16', C16, {'clerkFace': add(CLERK, [0, 2.05, 0]), 'chartL': add(CHART, [-0.55, 0, 0]), 'chartR': add(CHART, [0.55, 0, 0]), 'chartTop': add(CHART, [0, 0.36, 0]), 'sheet1': add(CNT, [0, 1.04, 0]), 'heroFace': add(HSTAND, [0, 2.05, 0]), 'sandw': [SWP[0], 0.12, 0.22]})
STAMPP = off(CNT, RYC, -0.15, 0.0, 1.06)
k16 = CLERKKEYS([TK(0.0, {'R': R5(add(STAMPP, [0, 0.42, 0.05]))}, {'R': 'grip'}, {**CLF, 'brow': -0.6}, (0.94, 1.08, 0.94), d=0.0, keep=True), TK(r(STAMP16 - 0.06), {'R': R5(add(STAMPP, [0, 0.48, 0.05]))}, {'R': 'grip'}, CLF, (0.92, 1.1, 0.92), d=0.08, keep=True),
                 TK(STAMP16, {'R': R5(add(STAMPP, [0, 0.12, 0]))}, {'R': 'grip'}, {**CLF, 'lid': 0.6}, (1.05, 0.95, 1.05), d=0.04, e='in', keep=True),
                 TK(0.3, {'R': R5(off(CLERK, RYK, 0.38, 0.18, 1.02))}, {'R': 'rest'}, CLF, (1, 1, 1), d=0.12, keep=True),
                 TK(SLIDE16[0], {'L': R5(off(CNT, RYC, -0.2, -0.05, 1.06))}, {'L': 'open'}, CLF, d=0.12, keep=True),
                 TK(SLIDE16[1], {'L': R5(off(CNT, RYC, 0.15, -0.05, 1.06))}, {'L': 'open'}, CLF, d=0.45, keep=True),
                 TK(1.3, {'L': R5(off(CLERK, RYK, 0.38, -0.2, 1.02))}, {'L': 'rest'}, CLF, d=0.2, keep=True), *blink(0.85, CLF), *blink(1.95, CLF), *BREATHE(0.2, D16, 0.5, 0.014),
                 TK(0.55, face={**CLF, 'gx': -0.6}, d=0.05, keep=True), k(0.62, look=add(HSTAND, [0, 2.0, 0]), lookDur=0.2), TK(1.05, bend={'neck': SP(0.25)}, d=0.1, keep=True), TK(1.22, bend={'neck': SP(0.0)}, d=0.12, keep=True),
                 TK(1.5, face={**CLF, 'gx': 0.5, 'mouth': 'smile'}, d=0.06, keep=True), k(1.58, look='camera', lookDur=0.2), TK(1.8, bend={'neck': SP(0.0, -0.15)}, d=0.2, keep=True)])
kh16 = [k(0.0, look=add(CLERK, [0, 2.0, 0])), TK(0.0, {'L': R5(PALM, 1, 0.08), 'R': R5(off(HSTAND, RYH15, 0.05, 0.3, 0.98))}, {'L': 'open', 'R': 'rest'}, {'lid': 0.3, 'mouth': 'line', 'brow': -0.7}, d=0.0),
        TK(r(STAMP16 + 0.03), face={'lid': 0.6, 'mouth': 'line', 'brow': -0.7}, d=0.04, keep=True), TK(0.3, face={'lid': 0.3, 'mouth': 'line', 'brow': -0.7, 'gy': 0.6}, d=0.1, keep=True), k(0.9, look=add(CNT, [0, 1.05, 0.35]), lookDur=0.2), TK(1.25, face={'lid': 0.0, 'mouth': 'O', 'brow': 0.6}, sq=(0.96, 1.05, 0.96), d=0.06, keep=True),
        TK(1.5, face={'lid': 0.35, 'mouth': 'line', 'brow': -0.4}, sq=(1, 1, 1), d=0.12, keep=True), k(1.6, look='camera', lookDur=0.2), *blink(2.05, {'lid': 0.35, 'mouth': 'line', 'brow': -0.4}), *BREATHE(0.0, D16, 0.55, 0.012)]
st.shot('S16', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[act('guichet', CLERK, RYK, 'stand', 'neutral', keys=k16), act('mec', HSTAND, RYH15, 'stand', 'neutral', keys=kh16)],
        props=[*CORRIDOR('S16', crushed=True, mopts={'canHide': 0.0, 'flapIn': 0}), P('comptoir16', 'glassCounter', pos=CNT, ry=RYC, opts={'w': 1.2, 'sheetAt': SLIDE16, 'sheetYaw': 70, 'sheetScale': 1.5}, keys=[k(STAMP16, squash=[1.04, 0.9, 1.04], dur=0.3)]),
               P('tampon16', 'roundStamp', on={'actor': 'guichet', 'hand': 'R', 'offset': [0.0, 0.02, 0.04]}, opts={'r': 0.09}),
               P('graphe16', 'riseChart', pos=CHART, opts={'w': 1.1, 'h': 0.72, 'grow': [0.3, 1.9]})], cams=[C16])
st.cue('clack', 'S16', STAMP16, 0.45); st.cue('sfx:paper', 'S16', SLIDE16[0], 0.3)

# ================================================================= S17 the small print
# 17: the bank had been out of order from the start; it was in small print. A slow push-in on the right corner of the glass, ending on the yellowed
#     EN PANNE sticker upright and square to the lens, wider than forty percent of the frame, above the caption band, clear of the BANQUE plate; the
#     hero's box head reflected faintly in the glass beside it; held one beat longer, still drifting
D17 = st.dur('S17')
STKC = [STK[0], STK[1], STK[2]]
GHOST = [0.29, 1.205, 0.4135]                     # his reflected face on the glossy black panel, just above and left of the sticker
ENDC = [0.34, 1.214, 0.41 + 0.355]                 # the end: square to the panel, 0.4 m off it (the sticker 42 % of the width, at 0.6 of the height)
C17 = cam(0.0, [0.25, 1.32, 2.2], ENDC, [0.15, 1.25, 0.41], [ENDC[0], ENDC[1], 0.41], lens=40, ease='linear')
chk('S17', C17, {'stkL': add(STKC, [-0.034, 0, 0]), 'stkR': add(STKC, [0.034, 0, 0]), 'stkBot': add(STKC, [0, -0.017, 0]), 'plate': PLATE, 'ghost': GHOST, 'ghostL': add(GHOST, [-0.017, 0, 0]), 'slot': SLOT, 'panelR': [0.465, 1.2, 0.41], 'glassR': [0.13, 1.2, 0.41]})
st.shot('S17', 'whiteVoid', setOpts=SETV(), look=LOOKC, actors=[],
        props=[*CORRIDOR('S17', crushed=True, mopts={'canHide': 0.0, 'flapIn': 0}),
               P('reflet17', 'glassGhost', pos=GHOST, opts={'w': 0.03, 'aspect': 1.75, 'box': True, 'alpha': 0.22, 'drift': [0.006, 0.004, 0.5, D17], 'blinkAt': [2.6, 4.25]})], cams=[C17])
st.cue('sfx:ding', 'S17', 2.0, 0.15)

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
SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'hair': 'crew', 'hairColor': '#3A3028',
        'gloves': '#E3A877', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 2.2, 'shift': 2.0, 'breathe': 2.0}}
SAV = {'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("Le distributeur", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'ministre': {'preset': 'politique', 'seed': 951, 'hat': 'none', 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#3A4A6A', 'hairColor': '#BDBDBD', 'sash': '#C9A646', 'sashW': 0.12, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'directeur': {'preset': 'commissaire', 'seed': 952, 'suit': '#33363D', 'lapel': '#22252B', 'tie': '#8A2A2A', 'shirt': '#F2F0EA', 'hat': 'none', 'hair': 'slick', 'hairColor': '#2A2420', 'facial': 'none', 'glasses': False, 'build': {'width': 1.08, 'headWidth': 1.2, 'belly': 0.16}, 'toon': EX},
    'guichet': {'preset': 'proviseur', 'seed': 953, 'hat': 'none', 'suit': '#7A8C9A', 'lapel': '#6A7C8A', 'tie': '#2E3A46', 'hair': 'receding', 'hairColor': '#8A8A8A', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'sold1': {**SOLD, 'preset': 'cop', 'seed': 961}, 'sold2': {**SOLD, 'preset': 'cop2', 'seed': 962, 'hair': 'bald'},
    'epargnant1': {**SAV, 'preset': 'madame', 'seed': 971, 'suit': '#2E7D4F'},
    'epargnant2': {**SAV, 'preset': 'worker', 'seed': 972, 'suit': '#1F4E8C', 'pants': '#22324A'},
    'epargnant3': {**SAV, 'preset': 'mamie', 'seed': 973, 'suit': '#7A2E4E', 'lapel': '#5A1E38'},
    'epargnant4': {**SAV, 'preset': 'femme', 'seed': 974, 'suit': '#E0A030'},
    'epargnant5': {**SAV, 'preset': 'fermier', 'seed': 975, 'suit': '#8A9A6A'},
    'epargnant6': {**SAV, 'preset': 'tourist', 'seed': 976, 'suit': '#5AA0C8', 'shirt': '#5AA0C8'},
})
