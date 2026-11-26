#!/usr/bin/env python3
"""La tartine (story 102, cycle 54; a hook, an institutional escalation, a reversal, a dry last line).
This man picks his toast up in six seconds and an inspector crawls out from under his table, stopwatch in hand: the rule is five. The toast is
confiscated, and the inspector lives under the table (nobody knows why). A law follows (five seconds on the floor and it belongs to the State),
every kitchen gets its agent, butter side down is taxed double, the takings soar and the ministers, to save money, eat off the floor; then the
country becomes deft and the takings crash, not the toasts. The State has every floor waxed: four million toasts a day, all butter side down, three
ministers slip and are seized, and nobody sees the difference. Yesterday he slipped in his own kitchen and got up in six seconds: he belongs to the
State, assigned under a table, the inspector's, in his own kitchen. The inspector, it was seven seconds.
Running gags: the big brown luggage tag round the neck (ttTag: kraft card, eyelet, string, ruled lines; its back carries a stopwatch drawing with
the owner's own time) on the inspector in every shot he is in (S01b, S02, S02b, S03, S14b, S16, S17), on every agent (S05, S05b, S10, S11, S12b, S15),
on the bagged toast (S02b, S06), slapped on the three ministers when they slip (S12b) and on the hero (S15); in S17 the inspector turns his round to
the lens: the needle deep in the red. The stopwatch (ttStopwatch: green wedge up to five, red zone after, no digits) is held up to the lens the same
way in S02 and S14b (« en six secondes » comes back word for word). The toast always shows its buttered side (ttToast: a thick yellow butter layer and
a pat; ttSplat: the yellow ring when it lands butter side down); the bagged toast from S02b sits on the minister's desk in S06; the wall clock ticks
six jumping ticks in S01 and again in S14. The question opened in S03 (« Personne ne sait pourquoi ») is answered by the tag in S17.
Staging: S01 low in his peach kitchen: the toast slips, lands butter side down (splat, squash), his jaw drops to his chest, the clock ticks six times,
his eyes go to it (eyes only), he dives (stretched smear into a crouch) on « six », snatches it and turns its butter to us. S01b the cloth flap lifts,
the small grey inspector (scale 0.68, flat cap, moustache) slides out on his knees, straightens with a stretch; the hero's double take. S02 the
stopwatch thrust at the lens (squash), two taps on the bezel on « cinq ». S02b his arm shoots up like rubber, snatches the toast and drops it in a
clear bag (zip, squash); CONFISQUÉE; the hero's empty mitten stays at mouth height, eyes sliding down. S03 under the table, curtains drawn: pillow,
mug, little lamp, he wriggles, pats the pillow and snaps the cloth shut on « pourquoi ». S04 the council room (straight benches, two rows, a plain
SALLE DU CONSEIL sign): stopwatches lifted to the chest, a trembling wait, one click on « l'État », everyone jolts with the hair up. S05 two kitchens of
a cut-away block, a whip pan from one to the other past the hatched section: a stiff couple, an agent popping up from under the near cloth edge.
S05b a toast lands butter side down; the agent raises a rubber stamp (held, trembling), slams it, the form flies up to the lens: a red stamp with two
toast icons. S06 the minister rubs his mittens, the chart's arrow shoots up and he stretches after it. S07 three ministers with napkins sit on the
carpet before the empty table and bow down to bite their floor toasts in unison, nod on « budget ». S08 a café terrace: an old lady catches her
falling croissant with both mittens, a waiter walks past with a steady tower of plates. S09 the chart drops off its nail, turns over and lands
upside down; the minister folds like an accordion; the camera glides to a toast standing on its edge on the desk, perfectly still. S10 three floor
polishers advance down a gleaming corridor, the agents buzzing with them, sparkles. S11 a shiny kitchen: a cascade of toasts lands butter side down
in a row, the couple glides sideways on their chairs, the agent clicks at each landing. S12 three ministers slide toward us on their backs, arms
streaming. S12b tags slapped on their chests (a squash each); they spring up like boards and walk to their offices. S13 the hero walks in with a toast,
his feet shoot out, he hangs, drops flat as a rug (stars), the toast lands butter side down by his head. S14 he springs back up and rubs his back,
the clock ticks six; S14b the stopwatch at the lens as in S02. S15 an agent slaps a tag on his chest (he deflates and re-inflates), NATIONALISÉ,
the other hands him a stopwatch. S16 under the table: the inspector shifts over, the hero (now in grey) crawls in, his head squashed by the table
top. S17 the inspector turns his tag round (seven: deep red), then both stare up at a toast teetering on a plate over the table's edge; deadpan.
Natural look; cycle 54: props_tartine.js (ttToast, ttStopwatch, ttTag, ttTable, ttPlate, ttPillow, ttNookLamp, ttMug, ttForm, ttChart, ttPolisher,
ttSparkle, ttShine, ttNapkin, ttPlateTower, ttCafeFront, ttCouncilDesk, ttSign, ttCutWall, ttFill, ttNoShadow, ttImpact, ttSplat, ttWallClock, ttPanel,
ttFloor); reused: chvBag (props_cheveu), bistroTable (props_ressort), grinOfficeWall and grinDesk (props_grincement), corridor (props_distributeur),
tacheBox (props_tache), rubberStamp, croissant, chair, bench, table, carpet (props.js); sets kitchenDay, mairie (no banner, no map, the flag outside
the room), whiteVoid.
Lessons applied from the start: Looney deformation on every gag accent (the toast's splat squash, the jaw drop, the dive smear, the double take, the
rubber-arm snatch, the bag's squash, the council's jolt, the stamp's hold and slam, the minister's stretch and accordion, the board stand-up, the
rug flatten and spring-back, the deflate on the tag); every action starts in the first 0.3 s of its shot; the hero's reactions framed with nobody
in front of them; look targets at head height or 'camera' (eyes only for the clock); blinks and breathing on holds; word timings from timeline.json
through st.at (words from 0, printed beside their times); cameras placed with a grid search against per-point boxes (tools/camsearch.py) and checked
with project() (CHECKS); no transparent layer drawn without depth test (ttShine is depth-tested with a polygon offset); flat floor props with a
polygon offset (ttSplat, ttShine); carried objects (toasts, stopwatches, stamp, form, tray, croissant) are world props moved with the hands' reach
times; new props prefixed tt; sound names checked against audio3.py/audio.py/mix.py; no raised arm held still, no hand at the face; no real flag,
emblem, organisation or brand; stamps held up to the lens; no digits or currency on screen; French only on screen; nobody hurt."""
from story_kit import *
import math

st = Story('tartine', look='natural')
st.plan([('S01', 'L01', 0), ('S01b', 'L01', 9), ('S02', 'L02', 0), ('S02b', 'L02', 4), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S05b', 'L05', 5),
         ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L08', 0), ('S09', 'L09', 0), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L12', 0), ('S12b', 'L12', 4),
         ('S13', 'L13', 0), ('S14', 'L14', 0), ('S14b', 'L14', 4), ('S15', 'L15', 0), ('S16', 'L16', 0), ('S17', 'L17', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def lerp3(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))
def chkc(sid, c, pts, end=False):
    frm, look = (c.get('to') or c['from'], c.get('lookAt2') or c['lookAt']) if end else (c['from'], c['lookAt'])
    chk(sid + ('>' if end else ''), frm, look, c['lens'], pts)
def W(sid, lid, i):
    # (cycle 51) word timings from timeline.json: st.at counts the words from 0; the word is printed beside its time
    t = st.at(sid, lid, i); CHECKS.append(f"{sid} « {st.L[lid]['words'][i]['w']} » at {t}"); return t

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
def R5(p, w=1, s=0.04): return [*p, w, s]
def blink(t, face, keep=None): return [k(t, toon={**(keep or {}), 'face': {**face, 'lid': 1.0}}, toonDur=0.05), k(r(t + 0.1), toon={**(keep or {}), 'face': face}, toonDur=0.06)]
def life(t0, t1, face, keep=None, ph=0.0, blinks=(), period=0.9, amp=0.013):
    # a moving hold: slow breathing keys that carry the face and the hands (a toon key is a whole state), clear of the blinks
    out, bl, t_, i = [], sorted(blinks), t0 + ph, 0
    while t_ < t1 - 0.1:
        if not any(-0.04 < t_ - b < 0.2 for b in bl):
            q = [r(1 - amp * 0.4, 4), r(1 + amp, 4), r(1 - amp * 0.4, 4)] if i % 2 == 0 else [r(1 + amp * 0.3, 4), r(1 - amp * 0.6, 4), r(1 + amp * 0.3, 4)]
            out.append(k(r(t_), toon={**(keep or {}), 'sq': q, 'face': face}, toonDur=r(period * 0.8), toonEase='inOut'))
        t_ += period / 2; i += 1
    for b in bl: out += blink(r(b), face, keep)
    return out
def blinks_in(t0, t1, every=2.4, ph=0.0):
    # (cycle 54) a blink every 2-3 s on every hold
    out, t_ = [], t0 + 0.5 + ph
    while t_ < t1 - 0.15: out.append(r(t_)); t_ += every
    return out

# ============================== the State's mark: the big brown luggage tag round the neck (torso frame: origin at the waist, chest front z 0.14)
TAGOFF = [0.0, 0.47, 0.165]
def TAG(pid, who, needle=7.0, flip=None, swing=None, w=0.26, h=0.36, cord=(0.1, 0.17, -0.1), keys=None, scale=None, dz=0.0):
    o = {'w': w, 'h': h, 'needle': needle, 'cord': list(cord)}
    if flip: o['flip'] = flip
    if swing: o['swing'] = swing
    kw = {**({'keys': keys} if keys else {}), **({'scale': scale} if scale is not None else {})}
    # (stills 3) dz: the kneeling agents at scale 0.78 swallowed the card inside the jacket at the usual depth
    return P(pid, 'ttTag', on={'actor': who, 'joint': 'torso', 'offset': [TAGOFF[0], TAGOFF[1], r(TAGOFF[2] + dz)]}, opts=o, **kw)
def WATCH(pid, pos, needle=None, at_=None, clicks=(), rad=0.16, keys=None, ry=0, rot=None, scale=None):
    o = {'r': rad}
    if needle: o['needle'] = needle
    if at_ is not None: o['at'] = at_
    if clicks: o['clicks'] = list(clicks)
    kw = {**({'keys': keys} if keys else {}), **({'rot': rot} if rot else {}), **({'scale': scale} if scale is not None else {})}
    return P(pid, 'ttStopwatch', pos=list(pos), ry=ry, opts=o, **kw)
def CLICKS(sid, ts, g=0.32):
    for t_ in ts: st.cue('sfx:click', sid, r(t_), g)
# the toast's thickness (w 0.34); butter side down its centre sits about 0.045 over the floor
TOAST_T = 0.051
def TOAST(pid, pos, rot=(0.0, 0.0, 0.0), keys=None, scale=None, **o):
    kw = {**({'keys': keys} if keys else {}), **({'scale': scale} if scale is not None else {})}
    return P(pid, 'ttToast', pos=list(pos), rot=list(rot), opts={'w': 0.34, **o}, **kw)
def track(p0, moves):
    # where a prop moved by `to` keys is at t (each move starts where the last one ended; eases as the engine's): hands follow it exactly
    EZ = {'linear': lambda u: u, 'inOut': lambda u: 2 * u * u if u < 0.5 else 1 - (-2 * u + 2) ** 2 / 2, 'out': lambda u: 1 - (1 - u) ** 3, 'in': lambda u: u ** 3}
    def at_(t):
        p = list(p0)
        for t0, to, d, e in sorted(moves, key=lambda m: m[0]):
            if t < t0: break
            u = EZ[e](1.0 if d <= 0 else min(1.0, (t - t0) / d)); p = [p[i] + (to[i] - p[i]) * u for i in range(3)]
        return [r(v) for v in p]
    return at_
def MOVES(moves): return [k(t0, to=list(to), dur=d, ease=e) for t0, to, d, e in moves]

# ============================== the hero's kitchen (kitchenDay: back wall z -3.6, counter along it, a hanging lamp at (0, 2.7, -1.0))
KSET = {}
TBL = [-0.2, 0.0, -1.0]; TH = 1.1; TW, TD = 1.6, 0.95
# the cloth's front plane
TFRONT = r(TBL[2] + TD / 2 + 0.05)
CLOCK = [-1.6, 2.05, -3.5]
def TABLE(pid, pos=TBL, **o): return P(pid, 'ttTable', pos=list(pos), opts={'w': TW, 'd': TD, 'h': TH, **o})
LOOKK = {'sunDir': [0.35, 0.85, 0.75]}
# (review 3) under the table (S03, S16, S17 and the end hold): less bloom and glow, no light shafts, a little more contrast and a lower exposure, so
# the pink-on-pink separates and the bottom quarter does not wash out
LOOKU = {**LOOKK, 'sun': 1.4, 'exposure': 0.92, 'bloom': 0.1, 'shafts': 0.12, 'contrast': 1.14, 'lift': 0.0}
# and a soft darker tint on the tiles between the lens and the table (the near floor washed out the bottom quarter)
def NEARFLOOR(n): return P(f'solproche{n}', 'ttShine', pos=[TBL[0], 0, r(TFRONT + 1.5)], opts={'w': 5.0, 'd': 3.0, 'tint': '#6E5048', 'tintA': 0.42, 'k': 0, 'n': 0, 'glints': 0})

for g_ in [('S01', 0.45, 'mec', 'splat jaw drop'), ('S01', 1.9, 'mec', 'dive for the toast'), ('S01b', 0.95, 'mec', 'double take'), ('S01b', 1.3, 'inspecteur', 'out from under'),
           ('S02', 0.9, 'inspecteur', 'stopwatch'), ('S02b', 0.6, 'mec', 'empty mitten'), ('S03', 2.2, 'inspecteur', 'curtains')]:
    st.gag(*g_)

# 1: the hook. Low on the kitchen tiles, looking up at him in front of his table: the toast is already slipping out of his mitten, spinning, and
#    lands butter side down with a splat (a squash, the butter squeezed out round it); his jaw drops to his chest; the wall clock behind him ticks
#    six times, jumping and pulsing; he looks up at it, back at the toast, squints; on « six » he dives (a stretched smear down into a crouch),
#    snatches the toast and stands with it, its buttered side turned to us, and blows on it, pleased
D1 = st.dur('S01'); RAM1 = W('S01', 'L01', 3); SIX1 = W('S01', 'L01', 7); SEC1 = W('S01', 'L01', 8)
H1 = [0.45, 0.0, -0.05]; RY1 = -12
LAND1 = 0.27
TO1A = [0.3, 1.2, 0.42]; TO1B = [0.15, r(TOAST_T / 2 + 0.002), 0.9]
# (review 1) six ticks after the jaw-drop hold, each one with its own head snap and squint; the last one just before « six »
TICK1 = [r(0.66 + 0.165 * j) for j in range(6)]
GRAB1 = r(SEC1 - 0.03)
HAND1 = off(H1, RY1, 0.42, -0.18, 1.5)
UP1 = off(H1, RY1, 0.5, -0.34, 1.22)
# (review 2) pulled back and tilted up: his whole head in frame through the jaw drop; a big clock nearer him on the wall (camsearch)
F1 = [-0.1, 0.8, 4.9]; L1 = [-0.2, 0.85, 0.5]
CLOCK1 = [-0.42, 2.17, -3.18]
C1 = cam(0.0, F1, add(F1, [0.02, -0.03, -0.3]), L1, add(L1, [0, 0.02, 0]), lens=48, ease='inOut')
chkc('S01', C1, {'headTop': add(H1, [0, 2.38, 0]), 'chin': add(H1, [0, 1.75, 0]), 'feet': H1, 'toastLand': TO1B, 'toastAir': TO1A, 'clock': CLOCK1, 'clockB': add(CLOCK1, [0, -0.44, 0]), 'clockL': add(CLOCK1, [-0.44, 0, 0]), 'tableL': [TBL[0] - 0.8, TH, TFRONT]})
HF1 = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}
def HB1(reach=None, hand='open', sp=0.0, **x):
    d = {'reach': {'R': R5(reach, 1, 0.0)} if reach else {}, 'hands': {'R': hand, 'L': 'rest'}, 'bend': {'spine': [sp, 0, 0, 1, None]}, 'hip': 0}
    d.update(x); return d
JAWF = {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 1.0, 'jaw': 1.0, 'jawLen': 1.3, 'jawBlock': 1, 'jawFwd': 0.4, 'noBlink': 1}
TB1 = add(TO1B, [0.0, 0.08, 0.0])
HERO1 = [k(-0.0, look=add(TO1A, [0, -0.2, 0])), k(0.0, toon={**HB1(HAND1), 'sq': [1.0, 1.02, 1.0], 'face': {**HF1, 'mouth': 'o', 'brow': 0.6, 'gy': 0.6}}, toonDur=0.0),
         k(0.12, look=TB1, lookDur=0.1),
         *beat(r(LAND1 + 0.06), {**HB1(add(HAND1, [0, -0.15, 0.05])), 'sq': [0.94, 1.08, 0.94], 'face': JAWF},
               antic={**HB1(HAND1), 'sq': [1.06, 0.93, 1.06], 'face': {**HF1, 'mouth': 'o', 'brow': 0.8, 'gy': 0.7}}, hold=0.22, settle_f=2,
               over={**HB1(add(HAND1, [0, -0.25, 0])), 'sq': [1.04, 0.96, 1.04], 'face': {**HF1, 'mouth': 'line', 'brow': 0.6, 'gy': 0.6}},
               settle={**HB1(add(HAND1, [0, -0.32, 0])), 'face': {**HF1, 'mouth': 'line', 'brow': 0.4, 'gy': 0.6}}),
         # (review 1) a head snap toward the clock at each tick, with a squint, then back to the toast (the head jerks up and turns a little,
         # the eyes do the rest), more irritated at each tick
         *[kk_ for j, t_ in enumerate(TICK1) for kk_ in (
             k(r(t_ - 0.01), look='camera', lookDur=0.03),
             # (review 2) a bigger snap: the head whips round and up to the clock, the body stretches after it, a hard squint
             k(r(t_ - 0.01), toon={**HB1(add(HAND1, [0, -0.32, 0])), 'sq': [0.94, 1.08, 0.94], 'bend': {'spine': [-0.12, 0.12, 0, 1, None], 'neck': [-0.5 - 0.03 * j, 0.62, 0.32, 1, None]}, 'face': {'lid': 0.62 + 0.05 * j, 'low': 0.55, 'mouth': 'line' if j < 3 else 'clench', 'brow': -0.7 - 0.05 * j, 'gx': 1.0, 'gy': -1.0}}, toonDur=0.033, toonEase='out'),
             k(r(t_ + 0.085), look=TB1, lookDur=0.05),
             k(r(t_ + 0.085), toon={**HB1(add(HAND1, [0, -0.32, 0])), 'sq': [1.03, 0.97, 1.03], 'bend': {'spine': [0.06, -0.04, 0, 1, None], 'neck': [0.22, -0.1, -0.08, 1, None]}, 'face': {'lid': 0.45 + 0.04 * j, 'low': 0.3, 'mouth': 'smirk' if j < 3 else 'clench', 'brow': -0.4 - 0.05 * j, 'gy': 0.8}}, toonDur=0.05))],
         # the dive: a rise (stretched up) then a smear down into a crouch, the mitten on the toast on « secondes »
         k(r(SIX1 - 0.14), toon={**HB1(add(HAND1, [0, -0.1, 0])), 'sq': [0.9, 1.14, 0.9], 'face': {'lid': 0.1, 'mouth': 'clench', 'brow': 0.6, 'gy': 0.7}}, toonDur=0.08, toonEase='out'),
         k(r(SIX1 - 0.02), clip='kneel'),
         # (review 1) two smear frames: the whole body stretched down to the floor, the arm a long rubber reach, then the crouch on the toast
         k(r(SIX1 - 0.02), toon={**HB1(add(TB1, [0.0, 0.05, 0.0]), 'open', 1.15), 'sq': [0.72, 1.5, 0.72], 'hose': 0.45, 'face': {'lid': 0.0, 'mouth': 'clench', 'brow': 0.8, 'gy': 0.8}}, toonDur=0.033, toonEase='linear'),
         k(r(SIX1 + 0.05), toon={**HB1(add(TB1, [0.0, 0.03, 0.0]), 'open', 1.0), 'sq': [0.8, 1.32, 0.8], 'hose': 0.3, 'face': {'lid': 0.0, 'mouth': 'clench', 'brow': 0.8, 'gy': 0.8}}, toonDur=0.033, toonEase='linear'),
         k(r(GRAB1 - 0.05), toon={**HB1(TB1, 'grip', 0.9), 'sq': [1.12, 0.88, 1.12], 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4, 'gy': 0.8}}, toonDur=0.05),
         k(r(GRAB1 + 0.16), clip='stand'),
         k(r(GRAB1 + 0.16), toon={**HB1(UP1, 'grip', 0.0), 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.14, toonEase='out'),
         k(r(GRAB1 + 0.2), look=add(UP1, [0, 0.15, 0]), lookDur=0.1),
         k(r(GRAB1 + 0.36), toon={**HB1(add(UP1, [0, 0.03, 0]), 'grip', 0.0), 'face': {'lid': 0.4, 'mouth': 'o', 'brow': 0.3, 'puff': 0.8, 'gy': 0.5}}, toonDur=0.08)]
TK1 = [k(0.0, to=TO1B, dur=LAND1, ease='in'), k(0.0, rotTo=[PI, 0.4, 0.0], dur=LAND1, ease='inOut'), k(LAND1, squash=[1.3, 0.55, 1.3], dur=0.5),
       k(GRAB1, to=TB1, dur=0.02, ease='linear'),
       k(r(GRAB1 + 0.16), to=add(UP1, [0.0, 0.02, 0.04]), dur=0.16, ease='out'), k(r(GRAB1 + 0.05), rotTo=[PI / 2, 0.0, 0.0], dur=0.25, ease='out')]
st.shot('S01', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('mec', H1, RY1, 'stand', 'neutral', keys=HERO1)],
        props=[TABLE('table1'), P('horloge1', 'ttWallClock', pos=CLOCK1, opts={'ticks': TICK1, 'r': 0.42, 'pulse': 0.3, 'jump': 0.1}), TOAST('tartine1', TO1A, rot=[0.6, 0.0, 0.3], keys=TK1),
               P('beurre1', 'ttSplat', pos=[TO1B[0], 0.0, TO1B[2]], opts={'r': 0.3, 'at': [[LAND1, 0.0], [r(LAND1 + 0.12), 1.0]]}),
               P('choc1', 'ttImpact', pos=[TO1B[0], 0.02, TO1B[2]], face='camera', opts={'at': LAND1, 'r': 0.42}),
               P('assiette1', 'ttPlate', pos=[TBL[0] + 0.4, TH + 0.012, TBL[2] + 0.1])],
        cams=[C1])
st.cue('sfx:splat', 'S01', LAND1, 0.4); st.cue('thud', 'S01', LAND1, 0.2)
for t_ in TICK1: st.cue('sfx:tick', 'S01', t_, 0.4)
st.cue('sfx:whoosh', 'S01', r(SIX1 - 0.05), 0.15); st.cue('sfx:pop', 'S01', GRAB1, 0.2)

# 1b: out from under the table. Wider, a little from the left: he stands right of his table about to bite the toast; the front of the cloth
#     twitches, lifts like a flap and a small grey inspector in a flat cap crawls out on his knees, bent low, a stopwatch in his mitten and a big
#     brown tag hanging from his neck; the cloth drops behind him; he straightens up tall on his knees (a stretch and a settle) and stares up at
#     him; the hero's double take, frozen with the toast at his open mouth
D1b = st.dur('S01b'); INSP1b = W('S01b', 'L01', 10); SOUS1b = W('S01b', 'L01', 14)
INS = [-0.3, 0.0, 0.0]; INS0 = [-0.3, 0.0, -0.78]; RYI = 12; SI = 0.68
H1b = [0.8, 0.0, 0.05]; RY1b = -28
OUT1b = (0.22, 0.6)
# (review 2) reframed to the right: the hero whole, shoulder included (he was half cut at the right edge)
F1b = [-0.2, 1.0, 5.0]; L1b = [0.1, 1.1, 0.2]
C1b = cam(0.0, F1b, add(F1b, [0.05, 0.0, -0.3]), L1b, add(L1b, [0, 0.0, 0]), lens=50, ease='inOut')
chkc('S01b', C1b, {'hTop': add(H1b, [0, 2.42, 0]), 'hChin': add(H1b, [0, 1.75, 0]), 'iTop': add(INS, [0, 1.25, 0]), 'iKnee': add(INS, [0, 0.05, 0.3]), 'clothL': [-1.0, TH, TFRONT], 'iStart': add(INS0, [0, 0.7, 0.3])})
# (stills 1) the toast held at mouth height but out to his right (frame left), so it never covers his face
MOUTH1b = off(H1b, RY1b, 0.4, -0.42, 1.78)
CHEST1b = off(H1b, RY1b, 0.42, -0.3, 1.3)
HF1b = {'lid': 0.3, 'mouth': 'open', 'jaw': 0.35, 'brow': 0.3}
HK1b = lambda p, hand='grip': {'reach': {'R': R5(p, 1, 0.0)}, 'hands': {'R': hand, 'L': 'rest'}, 'hip': 0}
HERO1b = [k(0.0, look='camera'), k(0.0, toon={**HK1b(CHEST1b), 'face': {**HF1b, 'mouth': 'smile', 'jaw': 0.0}}, toonDur=0.0),
          k(0.08, toon={**HK1b(MOUTH1b), 'sq': [0.97, 1.04, 0.97], 'face': HF1b}, toonDur=0.2, toonEase='out'),
          *doubleTake(0.36, add(INS, [0, 0.9, 0.2]), keep={**HK1b(MOUTH1b), 'face': HF1b}, pop=0.65, blank=0.2, hold=0.4),
          k(1.45, toon={**HK1b(MOUTH1b), 'face': {**HF1b, 'lid': 0.1, 'brow': 0.7}}, toonDur=0.12), *blink(1.6, {**HF1b, 'lid': 0.1, 'brow': 0.7}, HK1b(MOUTH1b))]
TK1b = [k(0.0, to=add(MOUTH1b, [0.0, 0.0, 0.03]), dur=0.25, ease='out')]
# the inspector: bent low under the cloth, he slides out on his knees (glide), the stopwatch at his chest, then straightens up tall
IF = {'lid': 0.35, 'mouth': 'line', 'brow': -0.35}
def IK(watch, sp=0.0, neck=0.0, **x):
    d = {'reach': {'R': R5(watch, 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'bend': {'spine': [sp, 0, 0, 1, None], 'neck': [neck, 0, 0, 1, None]}, 'hip': 0}
    d.update(x); return d
# (stills 1) the stopwatch held low at his right side, so the tag on his chest stays clear
WOFF = lambda p, h=0.42: off(p, RYI, 0.18, -0.42, h)
WM1b = [(OUT1b[0], WOFF(INS, 0.32), r(OUT1b[1] - OUT1b[0]), 'inOut'), (0.75, WOFF(INS), 0.25, 'out')]
WT1b = track(WOFF(INS0, 0.3), WM1b)
INSK1b = [k(0.0, look='camera'), k(0.0, clip='kneel'), k(0.0, toon={**IK(WT1b(0.0), 0.75, -0.55), 'face': IF}, toonDur=0.0),
          k(OUT1b[0], to=INS, dur=r(OUT1b[1] - OUT1b[0]), glide=True, face=RYI, ease='inOut'),
          *[k(r(OUT1b[0] + 0.1 * j), toon={**IK(WT1b(r(OUT1b[0] + 0.1 * j + 0.05)), 0.75 - 0.1 * j, -0.55 + 0.08 * j), 'sq': [1.04, 0.95, 1.04] if j % 2 else [0.97, 1.04, 0.97], 'face': IF}, toonDur=0.08) for j in range(5)],
          *beat(0.8, {**IK(WT1b(0.85)), 'sq': [0.9, 1.16, 0.9], 'face': {**IF, 'lid': 0.2, 'brow': 0.1}}, antic={**IK(WT1b(0.75), 0.3, -0.2), 'sq': [1.1, 0.88, 1.1], 'face': IF}, hold=0.2,
                over={**IK(WT1b(1.0)), 'sq': [1.04, 0.96, 1.04], 'face': IF}, settle={**IK(WT1b(1.1)), 'face': IF}),
          k(1.15, look=add(H1b, [0, 1.95, 0]), lookDur=0.15),
          *life(1.2, D1b, {**IF, 'gy': -0.3}, IK(WT1b(1.2)), blinks=[1.5])]
st.shot('S01b', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('mec', H1b, RY1b, 'stand', 'neutral', keys=HERO1b), act('inspecteur', INS0, RYI, 'kneel', 'neutral', scale=SI, keys=INSK1b)],
        props=[TABLE('table1b', lift=[[0.05, 0.0], [0.1, 0.08], [0.16, 0.02], [0.24, 0.0], [0.4, 0.62], [0.68, 0.66], [0.95, 0.0]]), P('horloge1b', 'ttWallClock', pos=CLOCK),
               TOAST('tartine1b', CHEST1b, rot=[PI / 2, 0.0, 0.0], keys=TK1b), P('beurre1b', 'ttSplat', pos=[0.15, 0.0, 0.9], opts={'r': 0.3}),
               WATCH('chrono1b', WT1b(0.0), at_=6.0, keys=MOVES(WM1b), ry=10), TAG('etiq1b', 'inspecteur', needle=7.0, swing=[[0.6, 0.25, 10, 3], [0.95, 0.15, 10, 3]])],
        cams=[C1b])
st.cue('sfx:rattleShort', 'S01b', 0.06, 0.12); st.cue('sfx:stepSoft', 'S01b', 0.35, 0.15); st.cue('sfx:stepSoft', 'S01b', 0.55, 0.15); st.cue('sfx:boing', 'S01b', 0.8, 0.12); st.cue('sfx:pop', 'S01b', 0.72, 0.15)

# 2: « La règle, c'est cinq. » Close and low in front of him, at his eye level: he thrusts the big stopwatch right up to the lens (it shoots in
#    from his chest with a squash, the arm stretching), the needle stopped just past the green wedge, in the first red; on « cinq » he taps the
#    glass twice with the other mitten; behind it his face, flat cap, moustache, deadpan, and the brown tag on his chest
D2 = st.dur('S02'); REG2 = W('S02', 'L02', 1); CINQ2 = W('S02', 'L02', 3)
INS2 = [-0.3, 0.0, 0.0]
F2 = [-0.6, 0.75, 1.3]; L2 = [-0.45, 0.8, 0.2]
C2 = cam(0.0, F2, add(F2, [0.0, 0.0, -0.06]), L2, L2, lens=44, ease='out')
SW2A = WOFF(INS2); SW2 = [-0.53, 0.75, 0.35]
chkc('S02', C2, {'watch': SW2, 'watchT': add(SW2, [0, 0.19, 0]), 'watchB': add(SW2, [0, -0.17, 0]), 'watchL': add(SW2, [-0.19, 0, 0]), 'face': add(INS2, [0.0, 1.06, 0.12]), 'cap': add(INS2, [0, 1.26, 0.0]), 'tag': add(INS2, [0.0, 0.62, 0.17])})
WM2 = [(0.04, SW2, 0.14, 'out')]
WT2 = track(SW2A, WM2)
# (review 1) the gripping mitten holds the watch from below and behind (on the watch centre it covered the hub and read as a toast); the tapping
# mitten hits the upper right rim, never the middle, so the needle reads
GRIP2 = lambda w_, rad=0.14: add(w_, [0.0, r(-rad * 1.15), r(-rad * 0.45)])
TAP2 = lambda w_, rad=0.14, out=0.0: add(w_, [r(rad * 1.05 + out), r(rad * 0.55 + out * 0.4), r(0.04 + out * 0.3)])
def IK2(w_, tap=None, rad=0.14, **x):
    d = IK(GRIP2(w_, rad), **x)
    if tap is not None: d = {**d, 'reach': {'R': R5(GRIP2(w_, rad), 1, 0.0), 'L': R5(tap, 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'point'}}
    return d
INSK2 = [k(0.0, look='camera'), k(0.0, clip='kneel'), k(0.0, toon={**IK2(SW2A), 'face': IF}, toonDur=0.0),
         k(0.04, toon={**IK2(SW2, hose=0.1), 'sq': [0.94, 1.07, 0.94], 'bend': {'spine': [0.12, 0, 0, 1, None], 'neck': [0.0, 0, 0, 1, None]}, 'face': {**IF, 'lid': 0.15, 'brow': 0.4}}, toonDur=0.1, toonEase='out'),
         k(0.24, toon={**IK2(SW2), 'face': {**IF, 'brow': -0.5, 'mouth': 'line'}}, toonDur=0.12),
         k(r(CINQ2 - 0.12), toon={**IK2(SW2, TAP2(SW2, out=0.07)), 'face': {**IF, 'mouth': 'open', 'brow': -0.2}}, toonDur=0.08),
         k(r(CINQ2), toon={**IK2(SW2, TAP2(SW2)), 'face': {**IF, 'mouth': 'o', 'brow': 0.3}}, toonDur=0.05),
         k(r(CINQ2 + 0.12), toon={**IK2(SW2, TAP2(SW2, out=0.07)), 'face': {**IF, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.06),
         k(r(CINQ2 + 0.22), toon={**IK2(SW2, TAP2(SW2)), 'face': {**IF, 'mouth': 'o', 'brow': 0.3}}, toonDur=0.05),
         k(r(CINQ2 + 0.36), toon={**IK2(SW2), 'face': {**IF, 'lid': 0.45, 'brow': -0.6, 'mouth': 'line'}}, toonDur=0.12), *blink(r(D2 - 0.25), {**IF, 'lid': 0.45, 'brow': -0.6}, IK2(SW2))]
st.shot('S02', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('inspecteur', INS2, RYI, 'kneel', 'neutral', scale=SI, keys=INSK2)],
        props=[TABLE('table2'), WATCH('chrono2', SW2A, at_=5.75, keys=[*MOVES(WM2), k(0.04, squash=[1.25, 0.8, 1.0], dur=0.35), k(r(CINQ2), squash=[1.06, 0.95, 1.0], dur=0.2), k(r(CINQ2 + 0.22), squash=[1.06, 0.95, 1.0], dur=0.2)], ry=8, rad=0.14),
               TAG('etiq2', 'inspecteur', needle=7.0, swing=[[0.05, 0.2, 10, 3]])],
        cams=[C2])
CLICKS('S02', [0.06]); st.cue('sfx:tick', 'S02', r(CINQ2), 0.3); st.cue('sfx:tick', 'S02', r(CINQ2 + 0.22), 0.3)

# 2b: « Tartine confisquée. » Front and a little from the right: his arm shoots up like rubber, snatches the toast from the hero's mitten at
#     mouth height and drops it in a clear bag he holds open in the other mitten (its own big brown tag); the bag seals with a zip and squashes;
#     CONFISQUÉE stamps; the hero's empty mitten stays at his open mouth, his eyes slide down to it
D2b = st.dur('S02b'); CONF2b = W('S02b', 'L02', 5)
H2b = H1b; RY2b = RY1b; INS2b = INS
MOUTH2b = MOUTH1b
SNATCH = 0.1; DROP2b = 0.34
BAG2b = off(INS2b, RYI, 0.42, -0.28, 0.62)
TOP2b = add(BAG2b, [0.0, 0.38, 0.02])
# (review 1) wider and from the front so the inspector stays whole inside the frame (camsearch)
F2b = [0.6, 0.62, 4.8]; L2b = [0.22, 1.1, 0.2]
C2b = cam(0.0, F2b, add(F2b, [0.0, 0.0, -0.2]), L2b, add(L2b, [0, 0.0, 0]), lens=48, ease='inOut')
chkc('S02b', C2b, {'hTop': add(H2b, [0, 2.42, 0]), 'hChin': add(H2b, [0, 1.75, 0]), 'mitt': MOUTH2b, 'iTop': add(INS2b, [0, 1.25, 0]), 'bag': BAG2b, 'bagBot': add(BAG2b, [0, -0.26, 0]), 'iKnee': add(INS2b, [0, 0.05, 0.3])})
TKM2b = [(SNATCH, add(MOUTH2b, [0.0, -0.02, 0.0]), 0.02, 'linear'), (r(SNATCH + 0.05), add(TOP2b, [0.0, 0.25, 0.0]), 0.16, 'out'), (DROP2b, TOP2b, 0.06, 'in'), (r(DROP2b + 0.06), add(BAG2b, [0.0, 0.11, -0.01]), 0.08, 'in')]
TT2b = track(MOUTH2b, TKM2b)
# (review 1) a delayed double take: he keeps blowing on the empty mitten, eyes half shut, pauses, his eyes slide down to it, then pop
BLOW2b = {'lid': 0.65, 'mouth': 'o', 'puff': 0.85, 'brow': 0.25}
HERO2b = [k(0.0, look='camera'), k(0.0, toon={**HK1b(MOUTH2b), 'face': BLOW2b}, toonDur=0.0),
          k(r(SNATCH + 0.03), toon={**HK1b(MOUTH2b, 'open'), 'sq': [1.02, 0.98, 1.02], 'face': {**BLOW2b, 'puff': 0.5}}, toonDur=0.04),
          *[k(r(0.2 + 0.12 * j), toon={**HK1b(MOUTH2b, 'open'), 'sq': [1.0, 1.0 + 0.012 * (j % 2), 1.0], 'face': {**BLOW2b, 'puff': 0.9 if j % 2 == 0 else 0.45}}, toonDur=0.06) for j in range(3)],
          k(0.55, toon={**HK1b(MOUTH2b, 'open'), 'face': {**BLOW2b, 'lid': 0.75, 'puff': 0.6}}, toonDur=0.06),
          k(0.64, toon={**HK1b(MOUTH2b, 'open'), 'face': {'lid': 0.15, 'mouth': 'o', 'puff': 0.25, 'brow': 0.35, 'gy': 0.85, 'gx': 0.45}}, toonDur=0.07),
          *beat(0.8, {**HK1b(MOUTH2b, 'open'), 'sq': [0.9, 1.14, 0.9], 'hairUp': 1.1, 'face': {'pop': 0.6, 'popLen': 0.28, 'brow': 1.0, 'jaw': 0.45, 'mouth': 'O', 'gy': 0.6, 'gx': 0.3}},
                antic={**HK1b(MOUTH2b, 'open'), 'sq': [1.06, 0.94, 1.06], 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'o', 'brow': 0.6, 'gy': 0.85, 'gx': 0.45}}, hold=0.22,
                over={**HK1b(MOUTH2b, 'open'), 'sq': [1.04, 0.97, 1.04], 'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'jaw': 0.4, 'brow': 0.9, 'gy': 0.6}},
                settle={**HK1b(MOUTH2b, 'open'), 'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'jaw': 0.4, 'brow': 0.9, 'gy': 0.6}})]
BAGK = lambda hand: {'reach': {'R': R5(hand, 1, 0.0), 'L': R5(add(BAG2b, [0.0, 0.26, 0.0]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0}
INSK2b = [k(0.0, look=add(MOUTH2b, [0, 0.0, 0])), k(0.0, clip='kneel'), k(0.0, toon={**BAGK(WOFF(INS2b)), 'face': IF}, toonDur=0.0),
          k(r(SNATCH - 0.06), toon={**BAGK(add(WOFF(INS2b), [0, -0.05, 0])), 'sq': [1.06, 0.93, 1.06], 'face': {**IF, 'lid': 0.2}}, toonDur=0.04),
          k(r(SNATCH - 0.02), toon={**BAGK(MOUTH2b), 'hose': 0.12, 'sq': [0.92, 1.1, 0.92], 'face': {**IF, 'lid': 0.1, 'brow': 0.2}}, toonDur=0.04, toonEase='out'),
          *[k(r(SNATCH + 0.05 + 0.04 * j), toon={**BAGK(TT2b(r(SNATCH + 0.09 + 0.04 * j))), 'face': IF}, toonDur=0.04) for j in range(5)],
          k(r(DROP2b + 0.02), look=BAG2b, lookDur=0.08),
          k(r(DROP2b + 0.04), toon={**BAGK(add(TOP2b, [0.12, 0.12, 0.05])), 'hands': {'R': 'open', 'L': 'grip'}, 'face': IF}, toonDur=0.08),
          k(r(DROP2b + 0.25), look='camera', lookDur=0.12),
          k(r(DROP2b + 0.25), toon={**BAGK(add(WOFF(INS2b), [0.05, 0.1, 0.05])), 'hands': {'R': 'open', 'L': 'grip'}, 'face': {**IF, 'lid': 0.45, 'brow': -0.55}}, toonDur=0.15),
          *life(r(DROP2b + 0.45), D2b, {**IF, 'lid': 0.45, 'brow': -0.55}, {**BAGK(add(WOFF(INS2b), [0.05, 0.1, 0.05])), 'hands': {'R': 'open', 'L': 'grip'}})]
st.shot('S02b', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('mec', H2b, RY2b, 'stand', 'neutral', keys=HERO2b), act('inspecteur', INS2b, RYI, 'kneel', 'neutral', scale=SI, keys=INSK2b)],
        props=[TABLE('table2b'), P('horloge2b', 'ttWallClock', pos=CLOCK), TOAST('tartine2b', MOUTH2b, rot=[PI / 2, 0.0, 0.0], keys=[*MOVES(TKM2b), k(r(SNATCH + 0.05), rotTo=[PI / 2, 0.0, 0.25], dur=0.2), k(r(DROP2b + 0.04), scale=0.66, dur=0.1)]),
               P('sachet2b', 'chvBag', pos=BAG2b, ry=RYI, opts={'w': 0.44, 'h': 0.52, 'text': 'SAISIE', 'num': ' '}, keys=[k(r(DROP2b + 0.12), squash=[1.12, 0.86, 1.0], dur=0.4)]),
               P('etiqsac2b', 'ttTag', pos=add(BAG2b, [0.2, 0.2, 0.04]), ry=RYI, opts={'w': 0.16, 'h': 0.22, 'needle': 6.0, 'cord': [-0.06, 0.04, -0.01]}, keys=[k(r(DROP2b + 0.12), squash=[1.1, 0.9, 1.0], dur=0.4)]),
               TAG('etiq2b', 'inspecteur', needle=7.0, swing=[[SNATCH, 0.3, 10, 3]])],
        cams=[C2b])
st.card('S02b', 'CONFISQUÉE', at=r(CONF2b + 0.06))
st.cue('sfx:whoosh', 'S02b', r(SNATCH - 0.04), 0.15); st.cue('sfx:zip', 'S02b', r(DROP2b + 0.1), 0.3); st.cue('thud', 'S02b', r(CONF2b + 0.06), 0.2)

# 3: « Il habite sous la table. » Low on the tiles in front of the table, the cloth drawn aside like curtains: under it, lit by a little lamp,
#    the inspector lies back on a big pillow, a big mug beside him, his tag on his chest; he wriggles comfortably, pats the pillow, looks at us
#    smugly and on « pourquoi » pulls both halves of the cloth shut like curtains (a snap, a wobble; the lamp's glow at the gap)
D3 = st.dur('S03'); HAB3 = W('S03', 'L03', 1); POUR3 = W('S03', 'L03', 8)
INS3 = [-0.22, 0.0, -1.18]; RY3 = 0
SHUT3 = (r(POUR3 - 0.2), r(POUR3 + 0.12))
hw3 = (TW + 0.1) / 2
def EDGE3(s, op): sx = max(0.16, 1 - 0.84 * op); return [r(TBL[0] + s * (hw3 - hw3 * sx)), 0.55, r(TFRONT - 0.03)]
F3 = [-0.1, 0.32, 1.25]; L3 = [-0.2, 0.5, -1.0]
C3 = cam(0.0, F3, add(F3, [0.0, 0.0, -0.18]), L3, L3, lens=52, ease='inOut')
chkc('S03', C3, {'head': add(INS3, [0, 0.8, 0.1]), 'tag': add(INS3, [0, 0.45, 0.3]), 'tableTop': [TBL[0], TH, TFRONT], 'cornerL': [TBL[0] - hw3, TH, TFRONT], 'cornerR': [TBL[0] + hw3, TH, TFRONT], 'lamp': [-0.62, 0.3, -1.1], 'mug': [0.14, 0.1, -0.85], 'floorF': [TBL[0], 0.0, TFRONT]})
OPEN3 = [[0.0, 1.0], [SHUT3[0], 1.0], [SHUT3[1], 0.0, 'lin'], [r(SHUT3[1] + 0.06), 0.06], [r(SHUT3[1] + 0.14), 0.0]]
def op3(t_):
    if t_ <= SHUT3[0]: return 1.0
    if t_ >= SHUT3[1]: return 0.0
    return r(1 - (t_ - SHUT3[0]) / (SHUT3[1] - SHUT3[0]))
IF3 = {'lid': 0.45, 'mouth': 'smile', 'brow': 0.1}
def IK3(hl=None, hr=None, **x):
    rc = {}
    if hl: rc['L'] = R5(hl, 1, 0.0)
    if hr: rc['R'] = R5(hr, 1, 0.0)
    d = {'reach': rc, 'hands': {'L': 'grip' if hl else 'rest', 'R': 'grip' if hr else 'rest'}, 'hip': 0}
    d.update(x); return d
# (review 2) he lounges sideways on a big plump cushion at his left (tipping him back hid his face behind the tag from this low lens, and a
# pillow behind him hid his head), wriggles into it and pats it three times (it squashes at each pat); he sits up straight for the curtains
REC3 = {'lay': [0.0, -0.12], 'bend': {'spine': [-0.08, 0, 0, 1, None], 'neck': [0.1, 0, 0.12, 1, None]}}
CUSH3 = add(INS3, [0.66, 0.27, -0.12])
PAT3 = add(CUSH3, [-0.02, 0.31, 0.08])
PATS3 = [0.8, 1.02, 1.24]
INSK3 = [k(0.0, look='camera'), k(0.0, clip='reclineBack'), k(0.0, toon={**IK3(**REC3), 'face': IF3}, toonDur=0.0),
         k(0.08, toon={**IK3(**REC3, yaw=0.14), 'sq': [1.08, 0.93, 1.08], 'face': {**IF3, 'lid': 0.8, 'mouth': 'bigsmile'}}, toonDur=0.12),
         k(0.24, toon={**IK3(**REC3, yaw=-0.14), 'sq': [0.95, 1.06, 0.95], 'face': {**IF3, 'lid': 0.8, 'mouth': 'bigsmile'}}, toonDur=0.12),
         k(0.4, toon={**IK3(**REC3, yaw=0.1), 'sq': [1.06, 0.95, 1.06], 'face': {**IF3, 'lid': 0.85, 'mouth': 'bigsmile'}}, toonDur=0.12),
         k(0.56, toon={**IK3(**REC3, yaw=0.0), 'face': {**IF3, 'lid': 0.7}}, toonDur=0.12),
         *[kk_ for t_ in PATS3 for kk_ in (k(r(t_ - 0.1), toon={**IK3(hl=add(PAT3, [0.0, 0.12, 0.03]), **REC3), 'face': {**IF3, 'lid': 0.6}}, toonDur=0.07),
                                             k(t_, toon={**IK3(hl=add(PAT3, [0.0, -0.05, 0.0]), **REC3), 'sq': [1.02, 0.98, 1.02], 'face': {**IF3, 'lid': 0.75, 'mouth': 'bigsmile'}}, toonDur=0.04))],
         k(1.36, toon={**IK3(**REC3), 'face': {**IF3, 'lid': 0.35, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.15), *blink(1.5, {**IF3, 'lid': 0.35, 'mouth': 'smirk', 'brow': 0.4}, IK3(**REC3)),
         k(r(SHUT3[0] - 0.22), toon={**IK3(EDGE3(-1, 1.0), EDGE3(1, 1.0)), 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'sq': [1.04, 0.97, 1.04], 'hose': 0.1, 'face': {**IF3, 'lid': 0.3, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.18, toonEase='out'),
         *[k(r(SHUT3[0] + j * 0.05), toon={**IK3(EDGE3(-1, op3(r(SHUT3[0] + j * 0.05 + 0.05))), EDGE3(1, op3(r(SHUT3[0] + j * 0.05 + 0.05)))), 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'hose': 0.1, 'face': {**IF3, 'lid': 0.3, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.05) for j in range(7)]]
st.shot('S03', 'kitchenDay', setOpts=KSET, look=LOOKU, actors=[act('inspecteur', INS3, RY3, 'reclineBack', 'neutral', scale=SI, keys=INSK3)],
        props=[TABLE('table3', open=OPEN3), NEARFLOOR(3), P('oreiller3', 'ttPillow', pos=CUSH3, rot=[0.0, -0.35, 0.0], opts={'w': 0.56, 'h': 0.56, 'd': 0.44, 'puffy': True}, keys=[k(r(t_), squash=[1.05, 0.88, 1.0], dur=0.3) for t_ in PATS3]),
               P('lampe3', 'ttNookLamp', pos=[-0.62, 0.0, -1.1], opts={'power': 1.6}), P('tasse3', 'ttMug', pos=[0.14, 0.0, -0.85], opts={'r': 0.075}),
               P('lumiere3', 'ttFill', pos=[-0.15, 0.65, -0.35], opts={'I': 1.0, 'R': 1.8, 'color': '#FFE2B8'}),
               # (review 3) the stopwatch moved off to his other side: in front of the mug the mug seemed to stand on it
               P('chrono3', 'ttStopwatch', pos=[-0.45, 0.08, -0.74], rot=[-1.3, 0.0, 0.0], opts={'r': 0.12, 'at': 6.0}),
               TAG('etiq3', 'inspecteur', needle=7.0)],
        cams=[C3])
st.cue('sfx:poof', 'S03', 0.12, 0.12)
for t_ in PATS3: st.cue('sfx:poof', 'S03', t_, 0.08)
st.cue('sfx:zip', 'S03', SHUT3[0], 0.12); st.cue('thud', 'S03', SHUT3[1], 0.12)

# ============================== the town hall's council room (mairie set: no banner, no map, no desk, the flag left outside the room) and the
# ministry office (whiteVoid with the formal office wall: no flag, no emblem)
MAIRIE = {'banner': False, 'map': False, 'desk': False, 'plate': False, 'flagX': 40, 'clockX': 3.4, 'wall': '#EFE3CF', 'band': '#9A6A44', 'floor': '#B98E5E'}
LOOKM = {'sunDir': [0.3, 0.85, 0.75]}
SIGN = lambda pid, pos, text='SALLE DU CONSEIL', w=2.3: P(pid, 'ttSign', pos=list(pos), opts={'text': text, 'w': w, 'h': w * 0.2, 'bg': '#2F5E86', 'fg': '#F4EFE2'})
def SIT_LIFE(t0, t1, face, keep=None, ph=0.0, every=2.4):
    return life(t0, t1, face, keep, ph=ph, blinks=blinks_in(t0, t1, every, ph))

# 4: the new law. The council room, frontal and a little high: two straight rows of councillors behind long desks (the back row on a step), a
#    plain blue sign SALLE DU CONSEIL; they lift big stopwatches to their chests together, lean in, thumbs ready, trembling; on « l'État » one
#    single click: they all jolt (a squash, then a stretch with the hair up) and the needles start running; they settle with a grave nod
D4 = st.dur('S04'); LOI4 = W('S04', 'L04', 1); TER4 = W('S04', 'L04', 5); ETAT4 = W('S04', 'L04', 9)
CLK4 = r(ETAT4 + 0.02)
ROW1 = [[-0.64, 0.0, -0.6], [0.0, 0.0, -0.6], [0.64, 0.0, -0.6]]
ROW2 = [[-0.33, 0.42, -1.75], [0.33, 0.42, -1.75]]
SEATS4 = ROW1 + ROW2
NAMES4 = ['cons1', 'cons2', 'cons3', 'cons4', 'cons5']
# (review 1) tighter: the desk front under a quarter of the frame, the sign at the top (camsearch)
F4 = [0.0, 1.55, 4.3]; L4 = [0.0, 1.44, -0.3]
C4 = cam(0.0, F4, add(F4, [0.0, -0.02, -0.25]), L4, add(L4, [0, -0.02, 0]), lens=36, ease='inOut')
chkc('S04', C4, {**{f'h{i}': add(p_, [0, 2.0, 0]) for i, p_ in enumerate(SEATS4)}, **{f'w{i}': add(p_, [0, 1.25, 0.42]) for i, p_ in enumerate(SEATS4)}, 'sign': [0, 3.38, -2.55], 'signB': [0, 3.12, -2.55], 'deskL': [-1.6, 0.8, -0.1]})
CF4 = {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}
def CONSK(i, p_):
    ph = 0.03 * i; wt = add(p_, [0.0, 1.22, 0.42]); rest = add(p_, [0.0, 0.84, 0.45])
    kp = lambda w_, lean=0.0, th=0.06: {'reach': {'R': R5(add(w_, [0.06, -0.1, 0.0]), 1, 0.0), 'L': R5(add(w_, [-0.04, th + 0.12, 0.02]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'point'}, 'bend': {'spine': [lean, 0, 0, 1, None]}, 'hip': 0}
    ks = [k(0.0, look=add(wt, [0, 0.0, 0.3])), k(0.0, clip='sit'), k(0.0, toon={**kp(rest), 'face': CF4}, toonDur=0.0),
          k(r(0.22 + ph), toon={**kp(add(wt, [0, -0.05, 0])), 'sq': [1.04, 0.97, 1.04], 'face': {**CF4, 'brow': 0.3}}, toonDur=0.22, toonEase='out'),
          k(r(0.5 + ph), toon={**kp(wt, 0.12), 'face': {**CF4, 'lid': 0.5, 'brow': -0.5, 'gy': 0.6}}, toonDur=0.25)]
    # (review 2) the wait: they lean further and further in over their stopwatches, trembling harder (body, hands, head), sweating
    t_ = r(0.8 + ph); j = 0; t0w = t_
    while t_ < CLK4 - 0.14:
        u = (t_ - t0w) / max(0.1, CLK4 - 0.14 - t0w); sg = 1 if j % 2 else -1; a = 0.008 + 0.014 * u
        ks.append(k(t_, toon={**kp(add(wt, [a * sg, 0.006 * sg, 0.03 * u]), 0.16 + 0.3 * u + 0.025 * sg, 0.05 if j % 2 else 0.07), 'sq': [1.0 + 0.012 * sg, 1.0 - 0.018 * sg, 1.0 + 0.012 * sg], 'buzz': 0.006 + 0.01 * u,
                              'bend': {'spine': [0.16 + 0.3 * u + 0.025 * sg, 0.02 * sg, 0, 1, None], 'neck': [-0.18 * u, 0.04 * sg, 0.03 * sg, 1, None]}, 'face': {**CF4, 'lid': 0.55 if j % 9 else 1.0, 'brow': -0.6 - 0.2 * u, 'gy': 0.6, 'sweat': 0.6 + 0.4 * u, 'mouth': 'clench' if u > 0.5 else 'line'}}, toonDur=0.04))
        t_ = r(t_ + 0.067); j += 1
    ks += beat(CLK4, {**kp(wt, -0.05, 0.0), 'sq': [0.9, 1.15, 0.9], 'hairUp': 1.0 if i < 3 else 0.55, 'face': {**CF4, 'lid': 0.0, 'eye': 0.4, 'brow': 1.0, 'mouth': 'o'}},
               antic={**kp(wt, 0.46, 0.0), 'sq': [1.12, 0.86, 1.12], 'face': {**CF4, 'lid': 0.6, 'brow': -0.6}}, hold=0.22, over={**kp(wt, 0.05, 0.0), 'sq': [1.05, 0.95, 1.05], 'face': CF4}, settle={**kp(wt, 0.0, 0.0), 'face': CF4})
    ks += [k(r(CLK4 + 0.35), look='camera', lookDur=0.15), k(r(CLK4 + 0.42), toon={**kp(wt, 0.0, 0.0), 'bend': {'spine': [0.0, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'face': {**CF4, 'lid': 0.55, 'mouth': 'smirk'}}, toonDur=0.12),
           k(r(CLK4 + 0.56), toon={**kp(wt, 0.0, 0.0), 'face': {**CF4, 'lid': 0.45, 'mouth': 'smirk', 'brow': 0.1}}, toonDur=0.12)]
    return ks
W4 = lambda i, p_: WATCH(f'chrono4_{i}', add(p_, [0.0, 1.22, 0.42]), needle=[[0.0, 0.0], [CLK4, 0.0], [D4, r(2.2 * (D4 - CLK4)), 'lin']], clicks=[CLK4], rad=0.12, keys=[k(0.0, to=add(p_, [0.0, 0.84, 0.45]), dur=0.0), k(r(0.22 + 0.03 * i), to=add(p_, [0.0, 1.17, 0.42]), dur=0.22, ease='out'), k(r(0.5 + 0.03 * i), to=add(p_, [0.0, 1.22, 0.42]), dur=0.25, ease='inOut'), k(CLK4, squash=[1.15, 0.88, 1.0], dur=0.35)])
st.shot('S04', 'mairie', setOpts=MAIRIE, look=LOOKM, actors=[act(n, p_, 0, 'sit', 'neutral', keys=CONSK(i, p_)) for i, (n, p_) in enumerate(zip(NAMES4, SEATS4))],
        props=[P('estrade4', 'tacheBox', pos=[0, 0.21, -1.95], opts={'w': 3.4, 'h': 0.42, 'd': 1.5, 'color': '#8E6440'}), SIGN('panneau4', [0, 3.36, -2.55]),
               P('pupitre4a', 'ttCouncilDesk', pos=[0, 0, -0.08], opts={'w': 2.8}), P('pupitre4b', 'ttCouncilDesk', pos=[0, 0.42, -1.25], opts={'w': 2.2}),
               *[P(f'banc4_{i}', 'bench', pos=[0, y, z - 0.02], opts={'w': w}) for i, (y, z, w) in enumerate([(0.0, -0.6, 2.8), (0.42, -1.75, 2.2)])],
               *[W4(i, p_) for i, p_ in enumerate(SEATS4)]],
        cams=[C4])
st.cue('sfx:click', 'S04', CLK4, 0.6); st.cue('thud', 'S04', CLK4, 0.12)
for t_ in (0.25, 0.55): st.cue('sfx:paper', 'S04', t_, 0.08)

# ============================== the cut-away block of flats: two kitchens side by side in the kitchen set, a section wall between them
CUTX = 0.9
KA = [-0.35, 0.0, -1.3]; KB = [2.2, 0.0, -1.3]
def FAMK(p_, ry, ph, hold_at, face, agent_head, take_t=None):
    keep = {'reach': {'R': R5(hold_at, 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'hip': 0}
    ks = [k(0.0, look='camera'), k(0.0, clip='sit'), k(0.0, toon={**keep, 'face': face}, toonDur=0.0)]
    ks += [k(r(0.25 + ph), look=agent_head, lookDur=0.15), k(r(0.25 + ph), toon={**keep, 'face': {**face, 'gy': 0.7, 'gx': 0.3 if p_[0] > 0 else -0.3}}, toonDur=0.12)]
    ks += life(r(0.45 + ph), 2.0, {**face, 'gy': 0.7}, keep, blinks=[r(0.9 + ph)])
    return ks
def AGENTK(p_, ry, watch, face, lift_dip=0.0, ph=0.0):
    # (stills 2) he pops up from below the cloth's near edge, upright on his knees (bent forward, his tag faced the floor): sunk low, then up with
    # a stretch and a settle, the stopwatch held up beside his face, his eyes darting from one diner to the other
    # (stills 3) the stopwatch in the mitten on its own side (the far mitten crossed his chest and hid the tag)
    keep = lambda w_, sp=0.0: {'reach': {'L': R5(w_, 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'rest'}, 'bend': {'spine': [sp, 0, 0, 1, None]}, 'hip': 0}
    ks = [k(0.0, look='camera'), k(0.0, clip='kneel'), k(0.0, toon={**keep(add(watch, [0, -0.25, 0]), 0.2), 'sq': [1.1, 0.72, 1.1], 'face': face}, toonDur=0.0)]
    ks += beat(r(0.12 + ph), {**keep(watch), 'sq': [0.92, 1.12, 0.92], 'face': {**face, 'lid': 0.2, 'brow': 0.2}}, antic={**keep(add(watch, [0, -0.25, 0]), 0.2), 'sq': [1.12, 0.7, 1.12], 'face': face}, hold=0.12,
               settle={**keep(watch), 'face': face})
    ks += [k(r(0.45 + ph), toon={**keep(watch), 'face': {**face, 'gx': 0.6, 'gy': -0.5}}, toonDur=0.08), k(r(0.75 + ph), toon={**keep(watch), 'face': {**face, 'gx': -0.6, 'gy': -0.5}}, toonDur=0.08),
           k(r(1.05 + ph), toon={**keep(watch), 'face': face}, toonDur=0.1), *blink(r(1.25 + ph), face, keep(watch))]
    return ks

# 5: every kitchen has its agent. At table height in a cut-away block: kitchen A (peach, red cloth), a stiff couple at breakfast, toast held still,
#    eyes sliding down: a grey agent half out from under the cloth's near edge, bent forward, stopwatch at his side, the same big brown tag on his
#    chest; the camera whips right past the hatched section of the wall into kitchen B (blue, blue cloth): the same couple, the same agent
D5 = st.dur('S05'); AG5 = W('S05', 'L05', 4)
WH5 = r(0.55)
def KITCHEN(n, c, cloth, lift):
    tb = add(c, [0, 0, 0])
    return [P(f'table{n}', 'ttTable', pos=tb, opts={'w': 1.4, 'd': 0.85, 'h': TH, 'cloth': cloth, 'lift': lift}), P(f'assA{n}', 'ttPlate', pos=add(tb, [-0.32, TH + 0.012, -0.12])), P(f'assB{n}', 'ttPlate', pos=add(tb, [0.32, TH + 0.012, -0.12])),
            P(f'chA{n}', 'chair', pos=add(tb, [-0.36, 0, -0.68])), P(f'chB{n}', 'chair', pos=add(tb, [0.36, 0, -0.68]))]
def FAMPOS(c): return [add(c, [-0.36, 0.0, -0.68]), add(c, [0.36, 0.0, -0.68])]
def AGPOS(c): return add(c, [0.05, 0.0, 0.62])
F5A = [-0.3, 1.25, 3.0]; L5A = [-0.3, 1.0, -1.0]
F5B = [2.25, 1.25, 3.0]; L5B = [2.25, 1.0, -1.0]
C5 = [cam(0.0, F5A, add(F5A, [0.05, 0, -0.1]), L5A, add(L5A, [0.05, 0, 0]), lens=46, ease='linear'), glide([cam(WH5, F5B, add(F5B, [0.05, 0, -0.12]), L5B, add(L5B, [0.05, 0, 0]), lens=46, ease='out')], 0.32)]
chkc('S05', C5[0], {'fa1': add(FAMPOS(KA)[0], [0, 2.0, 0]), 'fa2': add(FAMPOS(KA)[1], [0, 2.0, 0]), 'agHead': add(AGPOS(KA), [0, 0.95, 0]), 'agTag': add(AGPOS(KA), [0, 0.55, 0.15]), 'tableL': add(KA, [-0.75, TH, 0.45]), 'cut': [CUTX, 1.5, 0.6]})
chkc('S05', C5[1], {'fb1': add(FAMPOS(KB)[0], [0, 2.0, 0]), 'fb2': add(FAMPOS(KB)[1], [0, 2.0, 0]), 'agHead': add(AGPOS(KB), [0, 0.95, 0]), 'cut': [CUTX, 1.5, 0.6]})
FF5 = {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}
AF5 = {'lid': 0.4, 'mouth': 'line', 'brow': -0.4}
def KIT_ACTORS(sfx_, c, pre, ph):
    f1, f2 = FAMPOS(c); ag = AGPOS(c)
    agh = add(ag, [0, 1.3, 0.1]); w_ = off(ag, 0, 0.3, -0.32, 1.05)
    return [act(f'{pre}pere', f1, 0, 'sit', 'neutral', keys=FAMK(f1, 0, ph, add(f1, [0.12, 1.25, 0.45]), FF5, agh)),
            act(f'{pre}mere', f2, 0, 'sit', 'neutral', keys=FAMK(f2, 0, ph + 0.05, add(f2, [-0.12, 1.25, 0.45]), FF5, agh)),
            act(f'{pre}agent', ag, 0, 'kneel', 'neutral', scale=0.78, keys=AGENTK(ag, 0, w_, AF5, ph=ph))], w_
def KIT_PROPS(n, c, pre, cloth, w_):
    f1, f2 = FAMPOS(c)
    # (stills 3) the cloth stays down: lifted, its front flap swung out over the agent's chest and hid his tag
    return [*KITCHEN(n, c, cloth, [[0.0, 0.0]]), WATCH(f'chrono{n}', w_, at_=0.0, rad=0.1, ry=0), TAG(f'etiq{n}', f'{pre}agent', needle=6.5, dz=0.1),
            TOAST(f'tA{n}', add(f1, [0.12, 1.25, 0.47]), rot=[PI / 2, 0.0, 0.0], scale=0.85), TOAST(f'tB{n}', add(f2, [-0.12, 1.25, 0.47]), rot=[PI / 2, 0.0, 0.0], scale=0.85)]
AA, wa = KIT_ACTORS('S05', KA, 'a', 0.0)
AB, wb = KIT_ACTORS('S05', KB, 'b', 0.35)
st.shot('S05', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[*AA, *AB],
        props=[P('coupe5', 'ttCutWall', pos=[CUTX, 0.0, 0.6], opts={'d': 4.25, 'h': 3.0, 'slabW': 12}), P('papier5', 'ttPanel', pos=[2.4, 0.0, -3.52], opts={'w': 3.0, 'h': 3.0, 'color': '#CFE0EE', 'band': '#9CC0DE', 'bandH': 1.05}),
               *KIT_PROPS('5a', KA, 'a', '#D9473E', wa), *KIT_PROPS('5b', KB, 'b', '#3A7BD5', wb)],
        cams=C5)
st.cue('sfx:whoosh', 'S05', r(WH5 - 0.05), 0.18); st.cue('sfx:tick', 'S05', 0.2, 0.15); st.cue('sfx:tick', 'S05', 0.9, 0.15)

# 5b: butter side down, taxed double. Low in kitchen B: a toast drops in and lands butter side down by the agent (a splat, a squash); his head
#     snaps to it; he raises a rubber stamp high (held, trembling) over a form on the floor, slams it on « taxé » (his whole body squashes, the
#     toast hops) and the form flies up into his other mitten, held up to the lens: a big red stamp mark with two toast icons; on « double »
#     he jabs it at us
D5b = st.dur('S05b'); TAX5b = W('S05b', 'L05', 7); DBL5b = W('S05b', 'L05', 8)
AG5b = add(KB, [-0.2, 0.0, 0.75]); RY5b = 15
LAND5b = 0.14
# (review 2) the toast lands beside him, further from the lens: at about 68 % of the height, above the caption band
TO5b = off(AG5b, RY5b, 0.0, 0.35, 0.0); TO5b[1] = 0.045
FORM0 = off(AG5b, RY5b, 0.55, -0.05, 0.03)
# (review 2) the stamped form held up on his left (frame right), clear of the tag on his chest
FORM1 = off(AG5b, RY5b, 0.6, -0.3, 0.95)
SLAM5b = r(TAX5b - 0.02); UP5b = r(SLAM5b + 0.1)
# (review 1) the agent's head and the raised stamp inside the frame
F5b = [2.15, 1.75, 3.05]; L5b = [2.08, 0.78, 0.0]
C5b = cam(0.0, F5b, add(F5b, [0.0, -0.02, -0.12]), L5b, L5b, lens=44, ease='out')
chkc('S05b', C5b, {'head': add(AG5b, [0, 1.15, 0.1]), 'toast': TO5b, 'form0': FORM0, 'form1': FORM1, 'form1T': add(FORM1, [0, 0.3, 0]), 'form1B': add(FORM1, [0, -0.3, 0]), 'tag': add(AG5b, [0, 0.62, 0.15]), 'stampUp': off(AG5b, RY5b, 0.35, 0.3, 1.5)})
STAMPHI = off(AG5b, RY5b, 0.25, 0.5, 1.4); STAMPLO = add(FORM0, [0.05, 0.08, 0.0])
AK5b = lambda r_, l_, sp=0.3, hr='grip', hl='rest': {'reach': {'R': R5(r_, 1, 0.0), **({'L': R5(l_, 1, 0.0)} if l_ else {})}, 'hands': {'R': hr, 'L': hl}, 'bend': {'spine': [sp, 0, 0, 1, None]}, 'hip': 0}
AGK5b = [k(0.0, look=add(TO5b, [0, 0.3, 0])), k(0.0, clip='kneel'), k(0.0, toon={**AK5b(off(AG5b, RY5b, 0.3, 0.25, 0.6), None), 'face': AF5}, toonDur=0.0),
         *beat(r(LAND5b + 0.06), {**AK5b(off(AG5b, RY5b, 0.3, 0.25, 0.65), None, 0.2), 'sq': [0.92, 1.1, 0.92], 'face': {**AF5, 'lid': 0.0, 'eye': 0.4, 'brow': 0.9, 'gx': -0.6, 'gy': 0.5}}, hold=0.12,
               settle={**AK5b(off(AG5b, RY5b, 0.3, 0.25, 0.65), None, 0.2), 'face': {**AF5, 'brow': 0.2}}),
         k(0.36, look='camera', lookDur=0.12),
         k(0.38, toon={**AK5b(STAMPHI, add(FORM0, [-0.12, 0.05, 0.0]), 0.0, 'grip', 'grip'), 'sq': [0.94, 1.08, 0.94], 'face': {**AF5, 'lid': 0.5, 'brow': -0.6, 'mouth': 'clench'}}, toonDur=0.12, toonEase='out'),
         *[k(r(0.52 + 0.05 * j), toon={**AK5b(add(STAMPHI, [0.01 * (1 if j % 2 else -1), 0, 0]), add(FORM0, [-0.12, 0.05, 0.0]), 0.0, 'grip', 'grip'), 'sq': [0.94, 1.08, 0.94], 'face': {**AF5, 'lid': 0.6, 'brow': -0.7, 'mouth': 'clench'}}, toonDur=0.03) for j in range(int((SLAM5b - 0.6) / 0.05))],
         k(r(SLAM5b - 0.05), toon={**AK5b(STAMPLO, add(FORM0, [-0.12, 0.05, 0.0]), 0.6, 'grip', 'grip'), 'sq': [1.16, 0.84, 1.16], 'face': {**AF5, 'lid': 0.9, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.05, toonEase='in'),
         k(r(UP5b), toon={**AK5b(add(STAMPHI, [0.15, -0.5, 0]), add(FORM1, [-0.1, -0.18, -0.03]), 0.0, 'grip', 'grip'), 'sq': [0.95, 1.06, 0.95], 'face': {**AF5, 'lid': 0.3, 'brow': 0.3, 'mouth': 'smirk'}}, toonDur=0.1, toonEase='out'),
         k(r(DBL5b - 0.05), toon={**AK5b(add(STAMPHI, [0.15, -0.5, 0]), add(FORM1, [-0.1, -0.18, 0.12]), 0.0, 'grip', 'grip'), 'sq': [0.97, 1.03, 0.97], 'face': {**AF5, 'lid': 0.4, 'brow': -0.2, 'mouth': 'smirk'}}, toonDur=0.06),
         k(r(DBL5b + 0.15), toon={**AK5b(add(STAMPHI, [0.15, -0.5, 0]), add(FORM1, [-0.1, -0.18, -0.03]), 0.0, 'grip', 'grip'), 'face': {**AF5, 'lid': 0.45, 'brow': -0.4, 'mouth': 'smirk'}}, toonDur=0.15)]
FK5b = [k(r(UP5b - 0.02), to=FORM1, dur=0.12, ease='out'), k(r(UP5b - 0.02), rotTo=[0.0, 0.0, 0.05], dur=0.12, ease='out'), k(r(DBL5b - 0.05), to=add(FORM1, [0, 0, 0.15]), dur=0.06, ease='out'), k(r(DBL5b + 0.15), to=FORM1, dur=0.15, ease='inOut')]
SK5b = [k(0.38, to=STAMPHI, dur=0.12, ease='out'), k(r(SLAM5b - 0.05), to=add(STAMPLO, [0, 0.02, 0]), dur=0.05, ease='in'), k(r(UP5b), to=add(STAMPHI, [0.15, -0.5, 0]), dur=0.1, ease='out')]
st.shot('S05b', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('bagent', AG5b, RY5b, 'kneel', 'neutral', scale=0.78, keys=AGK5b)],
        props=[P('coupe5b', 'ttCutWall', pos=[CUTX, 0.0, 0.6], opts={'d': 4.25, 'h': 3.0, 'slabW': 12}), P('papier5b', 'ttPanel', pos=[2.4, 0.0, -3.52], opts={'w': 3.0, 'h': 3.0, 'color': '#CFE0EE', 'band': '#9CC0DE', 'bandH': 1.05}),
               P('table5b', 'ttTable', pos=KB, opts={'w': 1.4, 'd': 0.85, 'h': TH, 'cloth': '#3A7BD5'}),
               TOAST('tartine5b', add(TO5b, [0.05, 1.3, -0.1]), rot=[0.8, 0, 0.4], keys=[k(0.0, to=add(TO5b, [0, 0.0, 0]), dur=LAND5b, ease='in'), k(0.0, rotTo=[PI, 0.3, 0.0], dur=LAND5b), k(LAND5b, squash=[1.3, 0.55, 1.3], dur=0.4), k(r(SLAM5b), to=add(TO5b, [0, 0.12, 0]), dur=0.06, ease='out'), k(r(SLAM5b + 0.06), to=TO5b, dur=0.07, ease='in')]),
               P('beurre5b', 'ttSplat', pos=[TO5b[0], 0.0, TO5b[2]], opts={'r': 0.3, 'at': [[LAND5b, 0.0], [r(LAND5b + 0.12), 1.0]]}),
               P('formulaire5b', 'ttForm', pos=FORM0, ry=RY5b, rot=[-PI / 2, 0.0, 0.0], opts={'stampAt': SLAM5b, 'w': 0.5, 'h': 0.64}, keys=FK5b),
               P('tampon5b', 'rubberStamp', pos=off(AG5b, RY5b, 0.3, 0.25, 0.6), scale=1.6, keys=SK5b),
               TAG('etiq5b', 'bagent', needle=6.5, swing=[[r(SLAM5b), 0.3, 10, 3]], dz=0.1)],
        cams=[C5b])
st.cue('sfx:splat', 'S05b', LAND5b, 0.35); st.cue('sfx:whoosh', 'S05b', 0.38, 0.1); st.cue('thud', 'S05b', SLAM5b, 0.35); st.cue('sfx:gavel', 'S05b', SLAM5b, 0.25); st.cue('sfx:paper', 'S05b', UP5b, 0.15)

# 6: the State's takings took off. The minister's office (formal wall, no flag, no emblem): behind the minister a wall chart whose huge green
#    arrow shoots up steeply on « décollé », out through its top corner; he rubs his mittens together, eyes narrowed, and on the arrow's rise he
#    stretches up on his toes after it (a long stretch, hair up, held), then settles with a greedy grin; on his desk the bagged toast stands
D6 = st.dur('S06'); REC6 = W('S06', 'L06', 1); DEC6 = W('S06', 'L06', 5)
MIN6 = [0.6, 0.0, -1.35]; DESK6 = [0.0, 0.0, -0.75]; DT6 = 0.78
# (review 1) a clean board left of him: its thick arrow bursts out of the top edge and up past his head
CH6 = [-0.3, 3.0, -2.2]
# (review 2) a mid-tone ochre board with its grid in a thick dark frame: the cream board read as the cream window behind it, a blue-grey one as its glass
CHART = {'w': 1.9, 'h': 1.4, 'thick': 1.5, 'burst': 1.0, 'frameW': 0.26, 'paper': '#D9B26A', 'frame': '#1E1612', 'plain': False}
BAG6 = [-0.12, r(DT6 + 0.27), -0.6]
# (review 2) further back and a little lower in the frame: the stretched head and the arrow tip stay in, the bag above the captions (camsearch)
# (review 3) pushed in: his torso about half the frame height, the board's ochre face and grid beside him from the first frame (the curtains and
# the window gone: they read as a window with a blind), the bag nearer him on the desk; on the arrow's rise the camera glides back and up after
# his stretch and the arrow (camsearch); a taller wall, so no flat brown band at the top
F6 = [0.2, 1.64, 3.1]; L6 = [0.24, 1.6, -0.5]
F6B = [0.1, 2.0, 4.0]; L6B = [0.1, 1.9, -0.5]
C6 = cam(0.0, F6, add(F6, [0.0, 0.0, -0.12]), L6, L6, lens=36, ease='out')
C6S = [C6, glide([cam(r(DEC6 - 0.2), F6B, add(F6B, [0.0, 0.0, -0.1]), L6B, add(L6B, [0.0, 0.05, 0.0]), lens=44, ease='out')], 0.2)]
chkc('S06', C6, {'hips': add(MIN6, [0, 1.0, 0]), 'headClose': add(MIN6, [0, 2.42, 0]), 'bag': BAG6, 'board': add(CH6, [0.1, -0.6, 0])})
chkc('S06', C6S[1], {'head': add(MIN6, [0, 2.4, 0]), 'headUp': add(MIN6, [0, 3.6, 0]), 'tip': add(CH6, [1.05, 0.85, 0.05]), 'chin': add(MIN6, [0, 1.75, 0]), 'chartTL': add(CH6, [-0.95, -0.06, 0]), 'chartBR': add(CH6, [0.95, -1.5, 0]), 'bag': BAG6, 'bagB': add(BAG6, [0, -0.25, 0]), 'deskL': [-1.1, DT6, -0.3]})
MF6 = {'lid': 0.55, 'low': 0.25, 'mouth': 'smirk', 'brow': -0.3}
def RUB(t_, j, lift=0.0):
    # (review 3) a big rub (the mittens sweep past each other and bob), the shoulders working with it
    a = (0.13 if lift < 0.5 else 0.1) * (1 if j % 2 else -1); dy = 0.035 * (1 if j % 2 else -1) if lift < 0.5 else 0.0
    return {'reach': {'R': R5(add(MIN6, [-0.04 + a, 1.42 + lift + dy, 0.42]), 1, 0.0), 'L': R5(add(MIN6, [0.04 - a, 1.42 + lift - dy, 0.42]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0,
            **({'bend': {'spine': [0.04, 0.05 * (1 if j % 2 else -1), 0, 1, None]}} if lift < 0.5 else {})}
MINK6 = [k(0.0, look='camera'), k(0.0, toon={**RUB(0, 0), 'face': MF6}, toonDur=0.0)]
t_, j = 0.06, 0
while t_ < D6 - 0.05:
    # (review 1) the stretch after the arrow: a squash before, then about 1.5 times his height on tiptoe, held trembling, the rubbing mittens
    # carried up after the arrow, then a settle with a greedy grin
    pre = DEC6 - 0.14 <= t_ < DEC6 - 0.04
    up = DEC6 - 0.04 <= t_ < DEC6 + 0.5
    sq_ = min(1.0, t_ / max(0.1, DEC6 - 0.2))
    fc = {**MF6, 'lid': 0.0, 'eye': 0.35, 'brow': 1.0, 'mouth': 'bigsmile', 'gy': -0.9} if up else ({**MF6, 'mouth': 'evil'} if t_ > DEC6 else {**MF6, 'lid': r(0.5 + 0.35 * sq_), 'low': r(0.25 + 0.3 * sq_), 'brow': r(-0.3 - 0.4 * sq_), 'mouth': 'evil' if sq_ > 0.5 else 'smirk'})
    kk = {**RUB(t_, j, 1.15 if up else 0.0), 'face': fc}
    if pre: kk.update({'sq': [1.1, 0.88, 1.1], 'face': {**MF6, 'lid': 0.2, 'brow': 0.6, 'gy': -0.6}})
    if up: kk.update({'sq': [0.8, 1.5 + (0.03 if j % 2 else -0.02), 0.8], 'hairUp': 1.3, 'hose': 0.15})
    MINK6.append(k(r(t_), toon=kk, toonDur=0.04 if up or pre else 0.07))
    t_ = r(t_ + 0.09 if not (pre or up) else t_ + 0.05); j += 1
st.shot('S06', 'whiteVoid', setOpts={'color': '#5A3E2E'}, look={'sunDir': [0.25, 0.9, 0.8]}, actors=[act('ministre', MIN6, 0, 'stand', 'neutral', keys=MINK6)],
        props=[P('murs6', 'ttOfficeWall', pos=[0, 0, -2.3], opts={'h': 4.8}), P('bureau6', 'grinDesk', pos=DESK6, opts={'w': 2.2, 'd': 0.9}),
               P('courbe6', 'ttChart', pos=CH6, opts={**CHART, 'grow': [r(DEC6 - 0.12), r(DEC6 + 0.22)], 'floor': 3.0}),
               P('sachet6', 'chvBag', pos=BAG6, ry=12, opts={'w': 0.38, 'h': 0.48, 'text': 'SAISIE', 'num': ' '}), TOAST('tartine6', add(BAG6, [0.0, 0.1, -0.01]), rot=[PI / 2, 0.21, 0.2], scale=0.62),
               P('etiqsac6', 'ttTag', pos=add(BAG6, [0.17, 0.17, 0.04]), ry=12, opts={'w': 0.15, 'h': 0.21, 'needle': 6.0, 'cord': [-0.05, 0.04, -0.01]})],
        cams=C6S)
st.cue('sfx:slideUp', 'S06', r(DEC6 - 0.1), 0.3); st.cue('sfx:kaching', 'S06', r(DEC6 + 0.25), 0.15)

# 7: the ministers eat off the floor; it's the budget. The council room again, low and frontal: three ministers in dark suits, napkins tucked in,
#    sit on the carpet in a straight row before the big empty table, a toast on the carpet before each; together they bow down to the floor to
#    take a bite (a dignified dip, chew, back up straight, chewing with closed eyes), twice; on « budget » they nod together, gravely
D7 = st.dur('S07'); MAN7 = W('S07', 'L07', 3); TER7 = W('S07', 'L07', 7); BUD7 = W('S07', 'L07', 10)
MINS7 = [[-0.62, 0.0, 0.1], [0.0, 0.0, 0.22], [0.62, 0.0, 0.1]]
NAMES7 = ['ministreA', 'ministreB', 'ministreC']
DIPS7 = [0.3, r(TER7 - 0.15)]
F7 = [0.0, 1.75, 4.4]; L7 = [0.0, 0.55, -0.4]
C7 = cam(0.0, F7, add(F7, [0.0, 0.0, -0.3]), L7, L7, lens=44, ease='inOut')
chkc('S07', C7, {**{f'h{i}': add(p_, [0, 1.6, 0]) for i, p_ in enumerate(MINS7)}, **{f't{i}': add(p_, [0, 0.03, 0.48]) for i, p_ in enumerate(MINS7)}, 'tableTop': [0, 1.1, -1.4], 'tableL': [-1.6, 1.1, -1.0], 'sign': [0, 3.05, -2.55]})
NF7 = {'lid': 0.45, 'mouth': 'line', 'brow': 0.2}
def MINK7(i, p_):
    ph = 0.04 * i; ks = [k(0.0, look='camera'), k(0.0, clip='sitFloor'), k(0.0, toon={'hip': 0, 'face': NF7}, toonDur=0.0)]
    for d_ in DIPS7:
        t0 = r(d_ + ph)
        ks += [k(t0, look=add(p_, [0, 0.0, 0.48]), lookDur=0.1), k(t0, toon={'bend': {'spine': [1.05, 0, 0, 1, None], 'neck': [0.35, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'hip': 0, 'face': {**NF7, 'mouth': 'O', 'lid': 0.2}}, toonDur=0.18, toonEase='inOut'),
               k(r(t0 + 0.24), toon={'bend': {'spine': [1.1, 0, 0, 1, None], 'neck': [0.4, 0, 0, 1, None]}, 'sq': [1.06, 0.94, 1.06], 'hip': 0, 'face': {**NF7, 'mouth': 'clench', 'lid': 0.3}}, toonDur=0.05),
               k(r(t0 + 0.3), look='camera', lookDur=0.2), k(r(t0 + 0.3), toon={'bend': {'spine': [-0.05, 0, 0, 1, None]}, 'sq': [0.96, 1.05, 0.96], 'hip': 0, 'face': {**NF7, 'lid': 1.0, 'mouth': 'line', 'noBlink': 1}}, toonDur=0.2, toonEase='out')]
        for c_ in range(4): ks.append(k(r(t0 + 0.5 + 0.13 * c_), toon={'hip': 0, 'face': {**NF7, 'lid': 1.0, 'mouth': 'line' if c_ % 2 else 'o', 'noBlink': 1, 'cheeks': 0.6}}, toonDur=0.06))
        ks.append(k(r(t0 + 1.05), toon={'hip': 0, 'face': NF7}, toonDur=0.1))
    ks += [k(r(BUD7 - 0.05 + ph), toon={'bend': {'neck': [0.42, 0, 0, 1, None]}, 'hip': 0, 'face': {**NF7, 'lid': 0.65}}, toonDur=0.12), k(r(BUD7 + 0.25 + ph), toon={'bend': {'neck': [0.0, 0, 0, 1, None]}, 'hip': 0, 'face': {**NF7, 'lid': 0.45}}, toonDur=0.15)]
    return ks
NAP = lambda pid, who: P(pid, 'ttNapkin', on={'actor': who, 'joint': 'torso', 'offset': [0.0, 0.6, 0.16]}, opts={'w': 0.34, 'h': 0.4})
st.shot('S07', 'mairie', setOpts=MAIRIE, look=LOOKM, actors=[act(n, p_, 0, 'sitFloor', 'neutral', keys=MINK7(i, p_)) for i, (n, p_) in enumerate(zip(NAMES7, MINS7))],
        props=[SIGN('panneau7', [0, 3.05, -2.55]), P('tapis7', 'carpet', pos=[0, 0, -0.3], opts={'w': 4.2, 'd': 3.0, 'color': '#8E2E34', 'inner': '#C9A55A'}),
               P('grandetable7', 'table', pos=[0, 0.0, -1.35], opts={'w': 3.2, 'd': 1.1, 'h': 1.1, 'color': '#6A4428', 'legs': '#4A2E1C'}),
               *[TOAST(f'tartine7_{i}', add(p_, [0.0, 0.04, 0.48]), rot=[0.0, 0.3 * (i - 1), 0.0]) for i, p_ in enumerate(MINS7)],
               *[NAP(f'serviette7_{i}', n) for i, n in enumerate(NAMES7)]],
        cams=[C7])
for d_ in DIPS7: st.cue('sfx:crunch', 'S07', r(d_ + 0.26), 0.2)

# 8: then the country became deft. A café terrace (striped awning, CAFÉ board, a pale pavement): an old lady at a bistro table knocks her
#    croissant off the plate with her elbow; it tumbles; her arms shoot out (a smear) and both mittens catch it cleanly a hand above the
#    pavement; she lifts it, smug; behind her a waiter walks past carrying a tall tower of plates, perfectly steady
D8 = st.dur('S08'); PAYS8 = W('S08', 'L08', 2); ADR8 = W('S08', 'L08', 5)
MAMIE = [0.1, 0.0, 0.2]; RYM8 = -20
TAB8 = [0.55, 0.0, 0.45]
# (review 1) the croissant hops off the table's front edge, clear of it, and tumbles down; she catches it low, a hand above the pavement
CR0 = [0.42, 0.79, 0.55]; CATCH8 = r(PAYS8 + 0.25); CRC = off(MAMIE, RYM8, 0.62, -0.22, 0.2)
CRH = [0.62, 1.0, 0.95]
SERV0 = [-1.6, 0.0, -1.2]; SERV1 = [1.8, 0.0, -1.2]
# (stills 3) the tray carried out ahead of him at shoulder height (on his near side the plates hid his face)
TRAY = lambda p_: add(p_, [0.5, 1.6, 0.05])
# (review 1) a little lower and tilted down so the low catch stays above the caption band
F8 = [0.15, 1.0, 4.4]; L8 = [0.15, 0.9, -0.5]
C8 = cam(0.0, F8, add(F8, [0.0, 0.0, -0.25]), L8, L8, lens=46, ease='inOut')
chkc('S08', C8, {'head': add(MAMIE, [0, 1.75, 0]), 'catch': CRC, 'cr0': CR0, 'crh': CRH, 'servMid': add(lerp3(SERV0, SERV1, 0.45), [0, 2.4, 0]), 'tower': add(TRAY(lerp3(SERV0, SERV1, 0.45)), [0, 0.5, 0]), 'sign': [-0.9, 3.55, -2.4]})
GF8 = {'lid': 0.4, 'mouth': 'smile', 'brow': 0.1}
MK8 = lambda l_=None, r_=None, sp=0.0: {'reach': {**({'L': R5(l_, 1, 0.0)} if l_ else {}), **({'R': R5(r_, 1, 0.0)} if r_ else {})}, 'hands': {'L': 'open' if l_ else 'rest', 'R': 'open' if r_ else 'rest'}, 'bend': {'spine': [sp, 0, 0, 1, None]}, 'hip': 0}
CRK8 = [k(0.05, to=CRH, dur=0.16, ease='out'), k(0.21, to=add(CRC, [0.0, 0.14, 0.0]), dur=r(CATCH8 - 0.24), ease='in'), k(0.05, rotTo=[3.4, 0.9, 5.0], dur=r(CATCH8 - 0.05), ease='linear'), k(r(CATCH8 - 0.03), to=CRC, dur=0.03, ease='linear'),
        k(r(CATCH8 + 0.15), to=add(CRC, [0.18, 0.6, 0.12]), dur=0.2, ease='out'), k(r(CATCH8 + 0.15), rotTo=[0.0, 0.3, 0.0], dur=0.2, ease='out')]
CRT = track(CR0, [(0.05, CRH, 0.16, 'out'), (0.21, add(CRC, [0.0, 0.14, 0.0]), r(CATCH8 - 0.24), 'in'), (r(CATCH8 - 0.03), CRC, 0.03, 'linear'), (r(CATCH8 + 0.15), add(CRC, [0.18, 0.6, 0.12]), 0.2, 'out')])
MAMK8 = [k(0.0, look=add(CR0, [0, 0.0, 0])), k(0.0, toon={**MK8(None, add(TAB8, [-0.1, 0.8, 0.0])), 'face': GF8}, toonDur=0.0),
         k(0.04, toon={**MK8(None, add(TAB8, [-0.05, 0.85, 0.12])), 'face': {**GF8, 'mouth': 'o'}}, toonDur=0.06),
         k(0.14, look=add(CRC, [0, 0.1, 0]), lookDur=0.08),
         # (review 1) two smear frames: both arms shoot out long and rubbery, the body stretched down after them, then the catch low
         k(r(CATCH8 - 0.16), toon={**MK8(add(CRT(CATCH8 - 0.12), [-0.1, 0.1, 0.1]), add(CRT(CATCH8 - 0.12), [0.1, 0.1, 0.1]), 0.5), 'sq': [1.08, 0.92, 1.08], 'face': {**GF8, 'lid': 0.0, 'eye': 0.4, 'mouth': 'o', 'brow': 0.9}}, toonDur=0.04),
         k(r(CATCH8 - 0.1), toon={**MK8(add(CRT(CATCH8 - 0.04), [-0.12, 0.0, 0.08]), add(CRT(CATCH8 - 0.04), [0.12, 0.0, 0.08]), 0.95), 'sq': [0.82, 1.3, 0.82], 'hose': 0.4, 'face': {**GF8, 'lid': 0.0, 'mouth': 'o', 'brow': 0.8}}, toonDur=0.033, toonEase='linear'),
         k(r(CATCH8 - 0.05), toon={**MK8(add(CRC, [-0.09, 0.05, 0.04]), add(CRC, [0.09, 0.05, 0.04]), 0.95), 'sq': [0.88, 1.18, 0.88], 'hose': 0.25, 'face': {**GF8, 'lid': 0.0, 'mouth': 'o', 'brow': 0.8}}, toonDur=0.033, toonEase='linear'),
         *beat(CATCH8, {**MK8(add(CRC, [-0.07, 0.03, 0]), add(CRC, [0.07, 0.03, 0]), 0.95), 'sq': [1.1, 0.9, 1.1], 'face': {**GF8, 'lid': 0.1, 'mouth': 'smile', 'brow': 0.6}}, hold=0.16,
               settle={**MK8(add(CRC, [0.11, 0.63, 0.12]), add(CRC, [0.25, 0.63, 0.12]), 0.1), 'face': {**GF8, 'lid': 0.5, 'mouth': 'smirk', 'brow': 0.5}}),
         k(r(CATCH8 + 0.45), look='camera', lookDur=0.12), *blink(r(CATCH8 + 0.8), {**GF8, 'lid': 0.5, 'mouth': 'smirk', 'brow': 0.5}, MK8(add(CRC, [0.11, 0.63, 0.12]), add(CRC, [0.25, 0.63, 0.12]), 0.1))]
SV = lambda t_: lerp3(SERV0, SERV1, max(0.0, min(1.0, t_ / D8)))
SERVK8 = [k(0.0, look=[3.0, 2.0, -1.2]), k(0.0, to=SERV1, dur=D8, clip='walk', face=90, ease='linear'), k(0.0, look=[3.0, 2.0, -1.2])]
t_ = 0.0
while t_ < D8:
    SERVK8.append(k(r(t_), toon={'reach': {'R': R5(add(TRAY(SV(t_ + 0.1)), [0.0, -0.03, 0.0]), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'rest'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.3}, 'hip': 0}, toonDur=0.2)); t_ = r(t_ + 0.2)
st.shot('S08', 'whiteVoid', setOpts={'color': '#B9C9D6'}, look={'sunDir': [0.4, 0.85, 0.7]},
        actors=[act('mamie', MAMIE, RYM8, 'sit', 'neutral', keys=MAMK8), act('serveur', SERV0, 90, 'stand', 'neutral', keys=SERVK8)],
        props=[P('sol8', 'ttFloor', pos=[0, 0, 0], opts={'w': 14, 'd': 10, 'tile': 0.45, 'colors': ['#E2D9C8', '#D2C8B4']}), P('cafe8', 'ttCafeFront', pos=[0.0, 0.0, -2.4], opts={'w': 7.0, 'h': 4.6, 'sign': False, 'glass': 'CAFÉ'}),
               P('tableC8', 'bistroTable', pos=TAB8, opts={'h': 0.76}), P('chaise8', 'chair', pos=MAMIE, ry=RYM8, opts={'color': '#2E5A3E'}), P('assiette8', 'ttPlate', pos=[0.5, 0.765, 0.45]),
               P('croissant8', 'croissant', pos=CR0, scale=2.5, keys=CRK8), P('tasse8', 'ttMug', pos=[0.7, 0.765, 0.35], opts={'r': 0.045, 'color': '#F4F1E8'}),
               P('pile8', 'ttPlateTower', pos=TRAY(SERV0), opts={'n': 14}, keys=[k(0.0, to=TRAY(SERV1), dur=D8, ease='linear')])],
        cams=[C8])
st.cue('sfx:whoosh', 'S08', 0.08, 0.1); st.cue('sfx:pop', 'S08', CATCH8, 0.3); st.cue('sfx:clink', 'S08', 0.6, 0.06); st.cue('sfx:clink', 'S08', 1.4, 0.06)

# 9: takings crashed, not the toasts. The minister's office again, the minister seated at his desk on the right: the chart shivers on its nail on
#    « ont », drops on « chuté », turns over and crashes upside down against the wall, its arrow now plunging; he folds down like an accordion
#    (held, trembling) and pops back; the camera slides in onto his desk, where a toast stands on its edge, butter side to us, perfectly still
#    while everything else still shakes; his eyes slide to it
D9 = st.dur('S09'); CHU9 = W('S09', 'L09', 3); PAS9 = W('S09', 'L09', 4)
MIN9 = [0.5, 0.02, -1.4]
FALL9 = (r(CHU9 - 0.08), r(CHU9 + 0.24))
# (review 3) the chart a little further left for this shot: once it has turned over, its big arrowhead points down left of the minister
CH9 = add(CH6, [-0.3, 0.0, 0.0])
TOE9 = [-0.25, r(DT6 + 0.17 + 0.012), -0.55]
# (review 1) tighter on the minister and the chart, which now lands upside down in view above the desk
F9 = [0.12, 1.45, 3.4]; L9 = [0.15, 1.42, -0.5]
# (review 2) the still toast framed with the minister's trembling hand at the right edge and the fallen chart at the top left (camsearch),
# then a cut in to his eyes sliding to it
F9B = [-0.3, 1.3, 1.3]; L9B = [-0.02, 1.06, -0.75]
EYES9 = r(D9 - 0.42)
F9C = [0.28, 1.74, 0.15]; L9C = [0.5, 1.66, -1.4]
HAND9 = [0.22, 0.86, -0.8]
C9 = [cam(0.0, F9, add(F9, [0.0, 0.0, -0.1]), L9, L9, lens=40, ease='out'), glide([cam(r(PAS9 - 0.12), F9B, add(F9B, [0.0, 0.0, -0.08]), L9B, L9B, lens=40, ease='out')], 0.3),
      cam(EYES9, F9C, add(F9C, [0.0, 0.0, -0.06]), L9C, L9C, lens=40, ease='out')]
chkc('S09', C9[0], {'head': add(MIN9, [0, 1.95, 0]), 'chin': add(MIN9, [0, 1.4, 0]), 'chartTL': add(CH9, [-0.95, -0.06, 0]), 'chartBR': add(CH9, [0.95, -1.5, 0]), 'chartFloor': [CH9[0], 0.8, -2.15], 'toast': TOE9})
chkc('S09', C9[1], {'toastT': add(TOE9, [0, 0.18, 0]), 'toastB': add(TOE9, [0, -0.17, 0]), 'hand': HAND9, 'chart': [-0.3, 1.75, -2.15]})
chkc('S09', C9[2], {'face': add(MIN9, [0, 1.64, 0.05]), 'top': add(MIN9, [0, 2.0, 0.0]), 'chin': add(MIN9, [0, 1.35, 0.05])})
MF9 = {'lid': 0.4, 'mouth': 'smirk', 'brow': 0.1}
MK9 = {'reach': {'R': R5(add(MIN9, [-0.1, 0.82, 0.5]), 1, 0.0), 'L': R5(add(MIN9, [0.2, 0.82, 0.5]), 1, 0.0)}, 'hands': {'R': 'rest', 'L': 'rest'}, 'hip': 0}
# (review 2) after the accordion his right mitten grips the desk beside the toast and trembles (every frame), still shaken; in the cut-in his eyes
# slide sideways to the toast, the lids low, sweating, then a slow squint
MK9H = lambda j: {**MK9, 'reach': {'R': R5(add(HAND9, [0.012 * (1 if j % 2 else -1), 0.008 * (j % 3 - 1), 0.0]), 1, 0.0), 'L': MK9['reach']['L']}, 'hands': {'R': 'grip', 'L': 'rest'}, 'buzz': 0.01}
SH9 = {**MF9, 'lid': 0.2, 'mouth': 'o', 'brow': 0.6}
MINK9 = [k(0.0, look='camera'), k(0.0, toon={**MK9, 'face': MF9}, toonDur=0.0), *life(0.05, r(FALL9[1] - 0.1), MF9, MK9, blinks=[0.3]),
         *take(r(FALL9[1] + 0.02), 'accordion', keep={**MK9, 'face': {'lid': 0.8, 'mouth': 'grimace', 'brow': -0.6}}, hold=0.3),
         k(r(FALL9[1] + 0.5), look='camera', lookDur=0.15),
         *[k(r(FALL9[1] + 0.5 + 0.05 * j), toon={**MK9H(j), 'face': {**SH9, 'sweat': 0.8}}, toonDur=0.03) for j in range(int((EYES9 - FALL9[1] - 0.5) / 0.05))],
         k(EYES9, toon={**MK9H(0), 'face': {**SH9, 'lid': 0.45, 'gx': 0.0, 'gy': 0.1, 'sweat': 0.8}}, toonDur=0.03),
         k(r(EYES9 + 0.1), toon={**MK9H(1), 'face': {**SH9, 'lid': 0.5, 'gx': 0.95, 'gy': 0.35, 'sweat': 0.9}}, toonDur=0.18, toonEase='inOut'),
         k(r(EYES9 + 0.3), toon={**MK9H(0), 'face': {**SH9, 'lid': 0.68, 'low': 0.4, 'gx': 0.95, 'gy': 0.35, 'brow': -0.3, 'sweat': 1.0}}, toonDur=0.08)]
st.shot('S09', 'whiteVoid', setOpts={'color': '#5A3E2E'}, look={'sunDir': [0.25, 0.9, 0.8]}, actors=[act('ministre', MIN9, 0, 'sit', 'neutral', keys=MINK9)],
        props=[P('murs9', 'grinOfficeWall', pos=[0, 0, -2.3]), P('bureau9', 'grinDesk', pos=DESK6, opts={'w': 2.2, 'd': 0.9}), P('fauteuil9', 'chair', pos=add(MIN9, [0, -0.02, -0.1]), opts={'color': '#6A2A22'}),
               P('courbe9', 'ttChart', pos=CH9, opts={**CHART, 'fall': list(FALL9), 'floor': 1.6, 'flip': True}, keys=[k(r(CHU9 - 0.35), squash=[1.0, 1.0, 1.0], dur=0.1)]),
               TOAST('tartine9', TOE9, rot=[PI / 2, 0.0, 0.0])],
        cams=C9, fx=[{'type': 'shake', 'at': FALL9[1], 'dur': 0.3, 'amount': 0.03}])
st.cue('sfx:rattleShort', 'S09', r(CHU9 - 0.35), 0.12); st.cue('sfx:slideDown', 'S09', FALL9[0], 0.25); st.cue('clang', 'S09', FALL9[1], 0.3); st.cue('sfx:crunch', 'S09', FALL9[1], 0.2)

# ============================== the ministry corridor (whiteVoid + the corridor wall; two side walls): pale lino, doors, light panels
COR = lambda n, **o: P(f'couloir{n}', 'corridor', pos=[0, 0, -3.0], opts={'len': 4.0, 'depth': 16, 'h': 3.2, 'doorX': -1.2, 'boardX': 1.2, 'plantX': -1.75, 'wall': '#B9C8D8', 'dado': '#7E96B2', **o})
def SIDEWALLS(n): return [P(f'murG{n}', 'ttPanel', pos=[-2.0, 0, 5.0], ry=90, opts={'w': 16, 'h': 3.2, 'color': '#B9C8D8', 'band': '#7E96B2', 'bandH': 0.95}), P(f'murD{n}', 'ttPanel', pos=[2.0, 0, 5.0], ry=-90, opts={'w': 16, 'h': 3.2, 'color': '#B9C8D8', 'band': '#7E96B2', 'bandH': 0.95})]
def SIDEDOORS(n, zs):
    out = []
    for i, (sd, z) in enumerate(zs): out += [P(f'porte{n}_{i}', 'tacheBox', pos=[sd * 1.97, 1.07, z], opts={'w': 0.06, 'h': 2.14, 'd': 1.0, 'color': '#6E5A48'})]
    return out
LOOKC = {'sunDir': [0.3, 0.9, 0.6]}

# 10: the State had every floor polished. Low in the ministry corridor: three big round floor polishers advance side by side toward the lens, each
#     pushed by a grey agent with the brown tag, the machines humming and buzzing (the agents' arms buzz with them); behind them the floor gleams
#     with sheen streaks and sparkles pop
D10 = st.dur('S10'); CIR10 = W('S10', 'L10', 3); SOL10 = W('S10', 'L10', 6)
PX10 = [-0.85, -0.2, 0.45]; Z10A = 1.2; Z10B = 4.2
# (review 2) a gag: the three buzz forward in unison, stop dead together on « sols » (sparkles pop, a frozen beat, hair settling), then the right
# one bucks back to life and drags its agent away sideways out of frame, his arms stretched like rubber, while the other two turn their heads
# (review 3) the dead stop at 0.9 s, so the buck-and-drag gets 0.8 s, all inside the frame (the lineup shifted left, the drag ends at the right
# edge); a little higher and wider so the polisher bases sit well above the captions
STOP10 = 0.9; BUCK10 = r(STOP10 + 0.38); ZS10 = r(Z10A + (Z10B - Z10A) * STOP10 / D10 * 1.05)
OUT10 = [1.05, 0.0, r(ZS10 + 0.35)]
F10 = [-0.1, 1.5, 8.4]; L10 = [0.0, 1.0, 3.0]
C10 = cam(0.0, F10, add(F10, [0.0, 0.0, 0.3]), L10, add(L10, [0.0, 0.0, 0.3]), lens=44, ease='out')
chkc('S10', C10, {**{f'pol{i}': [x, 0.3, ZS10] for i, x in enumerate(PX10)}, **{f'ag{i}': [x, 2.3, ZS10 - 0.95] for i, x in enumerate(PX10)}, 'out': [OUT10[0], 1.0, OUT10[2]], 'shineFar': [0, 0.0, 0.0], 'ceil': [0, 3.2, 1.0]})
AGF10 = {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}
def POLK(i, x):
    p1 = [x, 0.0, r(ZS10 - 0.95)]
    hd = lambda t_: [x, 1.12, round(Z10A + (ZS10 - Z10A) * max(0.0, min(1.0, t_ / STOP10)) - 0.62, 3)]
    ks = [k(0.0, look='camera'), k(0.0, to=p1, dur=STOP10, clip='walk', face=0, ease='linear', speed=0.55)]
    t_ = 0.0; j = 0
    # they buzz with the machines: the whole body jitters, the head and the hair shake every frame, the arms rattle on the handle
    while t_ < STOP10 - 0.02:
        sg = 1 if j % 2 else -1
        # (review 3) bigger: the arms rattle on the handle, the head bobs (a slower nod under the jitter), the body bounces
        bob = 1 if j % 4 < 2 else -1
        ks.append(k(r(t_), toon={'reach': {'R': R5(add(hd(t_ + 0.05), [-0.24, 0.045 * sg, 0]), 1, 0.0), 'L': R5(add(hd(t_ + 0.05), [0.24, -0.045 * sg, 0]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'buzz': 0.035, 'hip': 0,
                                 'bend': {'neck': [0.16 * bob, 0.08 * sg, 0, 1, None], 'armL': [0.16 * sg, 0, 0, 1, None], 'armR': [-0.16 * sg, 0, 0, 1, None], 'foreL': [0.12 * sg, 0, 0, 1, None], 'foreR': [-0.12 * sg, 0, 0, 1, None]}, 'hairUp': 0.9 if j % 2 else 0.4,
                                 'sq': [1.0 + 0.025 * sg, 1.0 - 0.04 * sg, 1.0 + 0.025 * sg], 'face': {**AGF10, 'lid': 1.0 if (j + i) % 24 == 9 else 0.35, 'pupilShake': 0.8, 'mouth': 'wavy' if j % 4 < 2 else 'line'}}, toonDur=0.04))
        t_ = r(t_ + 0.05); j += 1
    hs = hd(STOP10); grip = {'R': R5(add(hs, [-0.24, 0, 0]), 1, 0.0), 'L': R5(add(hs, [0.24, 0, 0]), 1, 0.0)}
    # the dead stop: thrown forward over the handle (a stretch), back (a squash), then stock-still, the hair falling, eyes wide
    ks += [k(STOP10, clip='stand', blend=0.04),
           k(STOP10, toon={'reach': grip, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0, 'auto': 0, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'sq': [0.92, 1.1, 0.92], 'hairUp': 1.2, 'face': {**AGF10, 'lid': 0.0, 'eye': 0.4, 'brow': 0.8}}, toonDur=0.04, toonEase='out'),
           k(r(STOP10 + 0.1), toon={'reach': grip, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0, 'auto': 0, 'bend': {'spine': [-0.08, 0, 0, 1, None]}, 'sq': [1.06, 0.94, 1.06], 'hairUp': 0.6, 'face': {**AGF10, 'lid': 0.0, 'eye': 0.4, 'brow': 0.6}}, toonDur=0.06),
           k(r(STOP10 + 0.2), toon={'reach': grip, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0, 'auto': 0, 'face': {**AGF10, 'lid': 0.1, 'brow': 0.4}}, toonDur=0.08)]
    if i == 2:
        # bucked off sideways: dragged out of frame right, leaning back against it, heels sliding, arms stretched after the handle
        ks += [k(r(BUCK10 + 0.06), to=[OUT10[0] - 0.55, 0.0, r(OUT10[2] - 0.95)], dur=r(D10 - BUCK10 - 0.06), glide=True, face='keep', ease='in')]
        for jj, tt in enumerate([BUCK10, r(BUCK10 + 0.08), r(BUCK10 + 0.2), r(BUCK10 + 0.34), r(BUCK10 + 0.5)]):
            fr = min(1.0, (tt - BUCK10) / max(0.1, D10 - BUCK10)); hx = x + (OUT10[0] - x) * fr ** 2.2 + 0.08
            gp = {'R': R5([hx - 0.24, 1.12, r(ZS10 - 0.62)], 1, 0.0), 'L': R5([hx + 0.24, 1.12, r(ZS10 - 0.62)], 1, 0.0)}
            ks.append(k(tt, toon={'reach': gp, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0, 'auto': 0, 'hose': 0.3, 'lay': [0.0, -0.32], 'hairUp': 1.3, 'sq': [0.92, 1.08, 0.92] if jj % 2 else [0.96, 1.04, 0.96],
                                  'face': {'lid': 0.0, 'eye': 0.45, 'pop': 0.45, 'popLen': 0.2, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05))
    else:
        ks += [k(r(BUCK10 + 0.12), look=[1.6, 2.0, ZS10 - 0.95], lookDur=0.12), k(r(BUCK10 + 0.12), toon={'reach': grip, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0, 'auto': 0, 'face': {**AGF10, 'lid': 0.3, 'brow': 0.2, 'gx': -0.8}}, toonDur=0.1),
               *blink(r(D10 - 0.25 - 0.06 * i), {**AGF10, 'lid': 0.3, 'brow': 0.2, 'gx': -0.8}, {'reach': grip, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0, 'auto': 0})]
    return ks
SPK10 = [[x + (j % 3 - 1) * 0.4, 0.06, z, r(0.1 + 0.27 * j + 0.05 * i), 0.42] for i, x in enumerate(PX10) for j, z in enumerate([0.3, 0.9, 0.5, 1.4, 0.2, 1.1, 0.7])]
SPK10 += [[x + 0.3 * (1 if j % 2 else -1), 0.06, r(Z10A + (ZS10 - Z10A) * (0.15 + 0.17 * j) - 0.6), r(STOP10 * (0.15 + 0.17 * j) + 0.04 * i), 0.5] for i, x in enumerate(PX10) for j in range(5)]
# the sparkles that pop on the sound hits: a ring round each machine at the dead stop, a burst round the bucking one
POP10 = [[x + dx, dy, r(ZS10 + dz), STOP10, 0.55] for x in PX10 for dx, dy, dz in [(-0.45, 0.5, 0.1), (0.45, 0.65, 0.0), (0.0, 1.0, 0.2), (-0.3, 0.15, 0.35), (0.35, 0.2, 0.3)]]
POP10 += [[PX10[2] + dx, dy, r(ZS10 + dz), r(BUCK10 + 0.02 * n), 0.8] for n, (dx, dy, dz) in enumerate([(-0.4, 0.6, 0.2), (0.5, 0.9, 0.1), (0.2, 0.2, 0.4), (-0.2, 1.2, 0.0)])]
RUN10 = lambda i: [[0.0, 1.0], [r(STOP10 - 0.01), 1.0], [r(STOP10 + 0.03), 0.0, 'lin']] + ([[r(BUCK10 - 0.02), 0.0], [r(BUCK10 + 0.04), 2.2, 'lin']] if i == 2 else [])
def POLKEYS(i, x):
    ks = [k(0.0, to=[x, 0.0, ZS10], dur=STOP10, ease='linear')]
    if i == 2: ks.append(k(BUCK10, to=OUT10, dur=r(D10 - BUCK10), ease='in'))
    return ks
st.shot('S10', 'whiteVoid', setOpts={'color': '#9EB0C4'}, look=LOOKC, actors=[act(f'agent{i + 1}', [x, 0.0, Z10A - 0.95], 0, 'stand', 'neutral', keys=POLK(i, x)) for i, x in enumerate(PX10)],
        props=[COR(10), *SIDEWALLS(10), *SIDEDOORS(10, [(-1, 3.0), (1, 5.5), (-1, 7.5)]), P('brillant10', 'ttShine', pos=[0, 0, 3.0], opts={'w': 4.0, 'd': 12.0, 'tint': '#FFFFFF', 'k': 1.6, 'n': 9, 'glints': 14}),
               *[P(f'cireuse10_{i}', 'ttPolisher', pos=[x, 0.0, Z10A], opts={'color': ['#D8452F', '#E8A93A', '#2F8A6A'][i], 'run': RUN10(i)}, keys=POLKEYS(i, x)) for i, x in enumerate(PX10)],
               *[TAG(f'etiq10_{i}', f'agent{i + 1}', needle=[6.4, 6.8, 6.2][i], dz=0.1) for i in range(3)],
               P('etincelles10', 'ttSparkle', pos=[0, 0, 0], opts={'pts': SPK10, 'period': 1.9}), P('pops10', 'ttSparkle', pos=[0, 0, 0], opts={'pts': POP10})],
        cams=[C10])
st.cue('engine', 'S10', 0.0, 0.22, STOP10); st.cue('sfx:ding', 'S10', STOP10, 0.2); st.cue('thud', 'S10', STOP10, 0.15)
st.cue('engine', 'S10', BUCK10, 0.28, r(D10 - BUCK10)); st.cue('sfx:ding', 'S10', BUCK10, 0.15); st.cue('sfx:whoosh', 'S10', r(BUCK10 + 0.08), 0.15)

# 11: four million toasts a day, all butter side down. A kitchen with a mirror-shiny floor (sheen streaks), frontal and a little high: a couple at
#     breakfast; on the shiny floor their chairs creep sideways in one direction, the two of them surprised, gripping their seats; the stack of
#     toasts on the table slides off its edge in a cascade, every toast flipping to land butter side down (splats in a row); the agent in front
#     of the table clicks his stopwatch at each landing, his head bobbing after them
D11 = st.dur('S11'); MIL11 = W('S11', 'L11', 1); TOU11 = W('S11', 'L11', 6); BEU11 = W('S11', 'L11', 8)
KC = [0.0, 0.0, -1.4]
FAM11 = [add(KC, [-0.36, 0.0, -0.68]), add(KC, [0.36, 0.0, -0.68])]
AG11 = add(KC, [0.78, 0.0, 1.1]); RYA11 = -25
# (review 2) the cascade accelerates (gaps shrinking) into a final burst of five at once; the toasts land half a metre nearer the table, above the
# caption band, each with fat butter blobs squeezed out round its edge and a wide yellow ring; the chairs stay put until one clear slide
# sideways (the couple's grip-and-gasp take); the floor a step darker with the legs and the cloth mirrored in it and bright streaks
N11 = 11
LAND11 = [0.45, 0.92, 1.3, 1.6, 1.83, 2.0, 2.16, 2.19, 2.22, 2.25, 2.28]
# (review 3) the landings on a staggered grid (three rows, a gap round every toast and its own small halo: the row read as one zigzag strip),
# all left of the agent's stopwatch so no toast flies across it; the camera a little higher so the rows separate; the chairs slide left
FX11 = [-0.85, -0.48, -0.11, 0.26, -0.665, -0.295, 0.075, -0.85, -0.48, -0.11, 0.26]
FZ11 = [-0.92] * 4 + [-0.61] * 3 + [-0.3] * 4
SLIDE11 = -0.32; SLT11 = 1.12
F11 = [-0.3, 2.0, 4.4]; L11 = [0.05, 0.75, -1.1]
C11 = cam(0.0, F11, add(F11, [0.02, -0.02, -0.25]), L11, L11, lens=40, ease='inOut')
chkc('S11', C11, {'f1': add(FAM11[0], [SLIDE11, 2.0, 0]), 'f2': add(FAM11[1], [SLIDE11, 2.0, 0]), 'ag': add(AG11, [0, 1.35, 0]), 'agTag': add(AG11, [0, 0.62, 0.15]), **{f't{j}': [FX11[j], 0.04, FZ11[j]] for j in (0, 5, 6, 10)}, 'stack': add(KC, [0.0, TH + 0.2, 0.15])})
FF11 = {'lid': 0.4, 'mouth': 'line', 'brow': 0.1}
GASP11 = {'lid': 0.0, 'eye': 0.45, 'pop': 0.4, 'popLen': 0.18, 'mouth': 'O', 'brow': 1.0}
def FAMK11(p_, ph):
    keep = lambda d=0.0: {'reach': {'R': R5(add(p_, [0.22 + d, 0.5, 0.15]), 1, 0.0), 'L': R5(add(p_, [-0.22 + d, 0.5, 0.15]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0}
    ks = [k(0.0, look='camera'), k(0.0, clip='sit'), k(0.0, toon={**keep(), 'face': FF11}, toonDur=0.0)]
    ks += [k(r(0.5 + ph), look=[FX11[0], 0.3, -0.6], lookDur=0.2), *life(0.1, r(SLT11 - 0.12), {**FF11, 'gy': 0.6}, keep(), ph=ph, blinks=[r(0.75 + ph)])]
    # the slide: a squash as the chair goes, the grip tightens (knuckles in), stretched up with the eyes out and the mouth an O, held, settling
    ks += [k(r(SLT11 - 0.04), toon={**keep(), 'sq': [1.08, 0.9, 1.08], 'face': {**FF11, 'lid': 0.6, 'brow': -0.3}}, toonDur=0.04),
           k(SLT11, to=add(p_, [SLIDE11, 0.0, 0.0]), dur=0.3, glide=True, face='keep', ease='out'),
           k(r(SLT11 + 0.06), look='camera', lookDur=0.08),
           k(r(SLT11 + 0.06), toon={**keep(-0.03), 'sq': [0.88, 1.16, 0.88], 'hairUp': 1.2, 'lay': [0.0, 0.12], 'face': GASP11}, toonDur=0.05, toonEase='out'),
           k(r(SLT11 + 0.3), toon={**keep(-0.03), 'sq': [1.04, 0.96, 1.04], 'hairUp': 0.6, 'lay': [0.0, -0.04], 'face': {**GASP11, 'pop': 0.2}}, toonDur=0.08),
           k(r(SLT11 + 0.42), toon={**keep(-0.03), 'hairUp': 0.3, 'face': {**GASP11, 'pop': 0.0, 'mouth': 'o'}}, toonDur=0.1),
           k(r(LAND11[5] - 0.2), look=[0.0, 0.3, -0.5], lookDur=0.15),
           *life(r(SLT11 + 0.55), D11, {'lid': 0.1, 'eye': 0.4, 'mouth': 'o', 'brow': 0.8, 'gy': 0.6}, keep(-0.03), ph=ph, blinks=[r(2.6 + ph)])]
    return ks
def AGK11():
    # (review 1) the stopwatch in his right mitten, held out toward the row (inside the frame)
    w_ = off(AG11, RYA11, 0.3, 0.15, 1.15)
    keep = lambda w2, look_x=0.0: {'reach': {'R': R5(w2, 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'hip': 0}
    ks = [k(0.0, look='camera'), k(0.0, clip='kneel'), k(0.0, toon={**keep(w_), 'face': AF5}, toonDur=0.0)]
    for j, t_ in enumerate(LAND11[:6]):
        ks += [k(r(t_ - 0.08), look=[FX11[j], 0.3, FZ11[j]], lookDur=0.06), k(r(t_), toon={**keep(add(w_, [0, -0.03, 0])), 'sq': [1.05, 0.95, 1.05], 'face': {**AF5, 'lid': 0.6}}, toonDur=0.03), k(r(t_ + 0.07), toon={**keep(w_), 'face': AF5}, toonDur=0.05)]
    # the burst: he clicks frantically, eyes wide, the head jerking from one to the next
    for j, t_ in enumerate(LAND11[6:]):
        ks += [k(r(t_ - 0.02), look=[FX11[6 + j], 0.3, FZ11[6 + j]], lookDur=0.02), k(r(t_), toon={**keep(add(w_, [0, -0.04 * (j % 2), 0])), 'sq': [1.06, 0.94, 1.06] if j % 2 else [0.96, 1.05, 0.96], 'hairUp': 0.8, 'face': {**AF5, 'lid': 0.0, 'eye': 0.4, 'brow': 0.8, 'sweat': 1.0}}, toonDur=0.02)]
    ks += [k(r(LAND11[-1] + 0.3), look='camera', lookDur=0.15), k(r(LAND11[-1] + 0.3), toon={**keep(w_), 'face': {**AF5, 'lid': 0.5, 'sweat': 0.8}}, toonDur=0.15)]
    return ks, w_
AGK11_, W11 = AGK11()
TOASTS11 = []
for j in range(N11):
    t1 = LAND11[j]; t0 = r(t1 - 0.42); burst = j >= 6
    st0 = add(KC, [r(-0.1 + 0.02 * j), r(TH + 0.04 + 0.04 * (N11 - 1 - j)), 0.1])
    edge = [FX11[j] * 0.6, r(TH + 0.02 + (0.12 if burst else 0.0)), r(KC[2] + 0.48)]
    TOASTS11.append(TOAST(f'tartine11_{j}', st0, rot=[0.0, 0.2 * j, 0.0], scale=0.66, splat=[[t1, 0.0], [r(t1 + 0.1), 1.0]], ooze=[[t1, 0.0], [r(t1 + 0.12), 1.0]],
                          keys=[k(t0, to=edge, dur=0.14, ease='in' if not burst else 'out'), k(r(t0 + 0.14), to=[FX11[j], 0.04, FZ11[j]], dur=0.28, ease='in'), k(r(t0 + 0.1), rotTo=[PI, 0.2 * j + 0.4, 0.0], dur=0.32, ease='linear'), k(t1, squash=[1.35, 0.5, 1.35], dur=0.4)]))
    TOASTS11.append(P(f'beurre11_{j}', 'ttSplat', pos=[FX11[j], 0.0, FZ11[j]], opts={'r': 0.155, 'at': [[t1, 0.0], [r(t1 + 0.12), 1.0]]}))
# the mirror images in the waxed floor, painted into the sheen for this camera: the four table legs under the short cloth, the cloth's front,
# the agent (the sheen is drawn under the butter rings so their yellow shows)
CAM11 = add(F11, [0.01, -0.01, -0.12])
tz0, tz1 = r(KC[2] + 0.425 - 0.1), r(KC[2] - 0.425 + 0.1)
MIRROR11 = [[r(KC[0] + sx * 0.6), z_, 0.08, 0.0, 0.62, '#2A170C'] for sx in (-1, 1) for z_ in (tz0, tz1)]
# (review 3) the cloth's and the agent's mirror images left out: near the lens they smeared across the bottom of the frame
st.shot('S11', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('apere', FAM11[0], 0, 'sit', 'neutral', keys=FAMK11(FAM11[0], 0.0)), act('amere', FAM11[1], 0, 'sit', 'neutral', keys=FAMK11(FAM11[1], 0.03)),
                                                              act('aagent', AG11, RYA11, 'kneel', 'neutral', scale=0.78, keys=AGK11_)],
        props=[P('table11', 'ttTable', pos=KC, opts={'w': 1.4, 'd': 0.85, 'h': TH, 'cloth': '#D9473E', 'gap': 0.62}),
               P('brillant11', 'ttShine', pos=[0, 0, -0.4], opts={'w': 7.0, 'd': 6.5, 'tint': '#4E4440', 'tintA': 0.36, 'k': 1.3, 'n': 7, 'wide': 0.7, 'glints': 10, 'under': True, 'refl': {'cam': CAM11, 'origin': [0.0, -0.4], 'items': MIRROR11, 'alpha': 1.0}}),
               *[P(f'chaise11_{i}', 'chair', pos=p_, keys=[k(SLT11, to=add(p_, [SLIDE11, 0.0, 0.0]), dur=0.3, ease='out')]) for i, p_ in enumerate(FAM11)],
               P('plat11', 'ttPlate', pos=add(KC, [0.0, TH + 0.012, 0.1]), opts={'r': 0.22}), *TOASTS11,
               WATCH('chrono11', W11, at_=6.0, clicks=LAND11, rad=0.1), TAG('etiq11', 'aagent', needle=6.5, dz=0.1),
               P('etincelles11', 'ttSparkle', pos=[0, 0, 0], opts={'pts': [[x, 0.06, z, r(0.12 + 0.17 * i), 0.4] for i, (x, z) in enumerate([(-1.6, -0.6), (1.4, -1.2), (-1.3, -1.6), (1.8, -0.2), (-1.9, -0.4), (1.0, -1.9), (-1.1, -1.0), (1.3, -1.5), (0.5, -2.2), (-0.5, -2.0)])], 'period': 1.7})],
        cams=[C11])
for j, t_ in enumerate(LAND11): st.cue('sfx:splat', 'S11', t_, 0.22 if j < 6 else 0.14); st.cue('sfx:click', 'S11', t_, 0.25 if j < 6 else 0.14)
st.cue('sfx:slideDown', 'S11', SLT11, 0.2); st.cue('sfx:boing', 'S11', r(SLT11 + 0.06), 0.1)

# 12: three ministers slipped. (review 1) Low on the gleaming floor, close, a little from the side: three ministers come sliding feet first on their
#     backs, heads up, straight past the lens one after the other (each about a third of the frame as he passes), arms streaming up like
#     ribbons, hair blown back, mouths in an O (surprised, unhurt), turning slowly as they glide; sparkles in their wake
D12 = st.dur('S12'); GL12 = W('S12', 'L12', 3)
# (review 3) from high at the end of the corridor (layout searched for gaps between the three bodies, fix3/tools/s12search.py): three
# parallel bodies tipped across the frame (a toon yaw), in echelon, each with a clear gap round it, sliding feet first and coasting to a stop
# well inside the frame (low and close they merged into one tangled mass and the nearest one filled the frame)
T12 = [0.0, 0.12, 0.24]; YAW12 = 0.5; SL12 = 0.9; OFF12 = 1.32
F12 = [0.5, 3.0, 7.0]; L12 = [-0.05, 0.3, -0.3]
C12 = cam(0.0, F12, add(F12, [0.0, -0.05, -0.2]), L12, L12, lens=56, ease='linear')
def FEET12(i, u):
    sg = [1, 0, -1][i]; fx, fz = math.sin(YAW12), math.cos(YAW12)
    cx, cz = -0.1 - fz * sg * OFF12 + fx * SL12 * (u - 0.5), -0.3 + fx * sg * OFF12 + fz * SL12 * (u - 0.5)
    return [r(cx + fx), 0.12, r(cz + fz)]
HEAD12 = lambda i, u: [r(FEET12(i, u)[0] - math.sin(YAW12) * 2.0), 0.9, r(FEET12(i, u)[2] - math.cos(YAW12) * 2.0)]
chkc('S12', C12, {**{f'feet{i}': FEET12(i, 0.0) for i in range(3)}, **{f'head{i}': HEAD12(i, 0.0) for i in range(3)}, **{f'feetEnd{i}': FEET12(i, 1.0) for i in range(3)}, **{f'headEnd{i}': HEAD12(i, 1.0) for i in range(3)}})
MSF = {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 1.0}
SLIDEPOSE = lambda yaw_=0.0, f=None: {'lay': [-1.42, 0.0], 'bend': {'spine': [0.28, 0, 0, 1, None], 'neck': [0.62, 0, 0, 1, None]}, 'hairUp': 1.2, 'yaw': r(YAW12 + yaw_, 3), 'hip': 0, 'face': f or MSF}
def SLIDEK(i, x):
    t0 = T12[i]; dur_ = r(D12 + 0.15 - t0)
    sg = 1 if i % 2 else -1
    return [k(0.0, look='camera'), k(0.0, clip='fallDrag'), k(0.0, toon=SLIDEPOSE(), toonDur=0.0),
            k(0.0, to=FEET12(i, 1.0), dur=r(D12 + 0.1), glide=True, face='keep', ease='out'),
            k(r(t0 + 0.25), toon=SLIDEPOSE(0.12 * sg, {**MSF, 'mouth': 'scream' if i == 1 else 'O'}), toonDur=0.45),
            k(r(t0 + 0.75), toon=SLIDEPOSE(-0.1 * sg, {**MSF, 'pop': 0.3}), toonDur=0.45), *[x_ for x_ in blink(r(t0 + 1.1), MSF, SLIDEPOSE(-0.1 * sg))]]
st.shot('S12', 'whiteVoid', setOpts={'color': '#9EB0C4'}, look=LOOKC, actors=[act(n, FEET12(i, 0.0), 0, 'fallDrag', 'neutral', keys=SLIDEK(i, 0)) for i, n in enumerate(NAMES7)],
        props=[COR(12), *SIDEWALLS(12), P('brillant12', 'ttShine', pos=[0, 0, 2.5], opts={'w': 4.0, 'd': 13.0, 'tint': '#FFFFFF', 'k': 1.6, 'n': 10, 'glints': 16}),
               P('etincelles12', 'ttSparkle', pos=[0, 0, 0], opts={'pts': [[r(FEET12(i, 0.18 * j)[0] + 0.25 * (1 if j % 2 else -1)), 0.06, r(FEET12(i, 0.18 * j)[2] - 0.3), r(0.1 + 0.2 * j + 0.05 * i), 0.3] for i in range(3) for j in range(6)]})],
        cams=[C12])
for i, t_ in enumerate(T12): st.cue('sfx:slideDown', 'S12', r(t_ + 0.05), 0.15)

# 12b: seized; nobody saw the difference. (review 1) Frontal and a little high: the three ministers lie side by side on their backs, feet toward us,
#      dazed faces up; the two agents at their sides slap a big brown tag on each chest (the left one stretches a rubber arm to the middle one; a
#      pop, the chest squashed); on « Personne » the three spring up stiff as boards (a squash, the snap, an overshoot, a wobble), straighten their
#      ties and walk on toward us exactly as before, deadpan, tags swinging, the agents falling in beside them in the same walk
D12b = st.dur('S12b'); SAI12 = W('S12b', 'L12', 4); PER12 = W('S12b', 'L12', 5); DIF12 = W('S12b', 'L12', 9)
MZ = 0.4
MLY = [[-0.5, 0.0, MZ], [0.0, 0.0, MZ], [0.5, 0.0, MZ]]
TAGT12 = [0.12, 0.34, 0.22]
UP12 = r(PER12 - 0.12)
WALK12 = r(DIF12 - 0.25)
AGP12 = [[-1.0, 0.0, -0.75], [1.0, 0.0, -0.75]]
F12b = [0.0, 1.85, 5.2]; L12b = [0.0, 1.0, -0.6]
C12b = cam(0.0, F12b, add(F12b, [0.0, -0.05, 0.5]), L12b, add(L12b, [0.0, 0.05, 0.3]), lens=46, ease='inOut')
chkc('S12b', C12b, {**{f'ly{i}': add(p_, [0, 0.6, -1.7]) for i, p_ in enumerate(MLY)}, **{f'up{i}': add(p_, [0, 2.45, 0]) for i, p_ in enumerate(MLY)}, **{f'ag{i}': add(p_, [0, 2.35, 0]) for i, p_ in enumerate(AGP12)}})
chkc('S12b', C12b, {**{f'walk{i}': add(p_, [0, 2.45, 0.5]) for i, p_ in enumerate(MLY)}, **{f'agW{i}': add(p_, [0, 2.35, 0.5]) for i, p_ in enumerate(AGP12)}, 'walkFeet': add(MLY[2], [0, 0, 0.5])}, end=True)
MF12 = {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}
LYING = lambda f, **x: {'lay': [-1.5, 0.0], 'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.4, 0, 0, 1, None]}, 'hip': 0, 'face': f, **x}
DAZE = {'lid': 0.3, 'eye': 0.35, 'mouth': 'o', 'brow': 0.6}
def MINK12(i, p_):
    sg = 1 if i % 2 else -1
    ks = [k(0.0, look='camera'), k(0.0, toon=LYING(DAZE), toonDur=0.0),
          k(TAGT12[i], toon=LYING({**DAZE, 'lid': 0.9, 'mouth': 'grimace', 'brow': -0.4}, sq=[1.12, 0.92, 0.7]), toonDur=0.03),
          k(r(TAGT12[i] + 0.12), toon=LYING({**DAZE, 'lid': 0.15, 'eye': 0.4, 'brow': 0.8, 'gy': 0.6}), toonDur=0.08),
          # the board spring-up: a squash, the snap past upright, an overshoot back, a wobble, upright (about eight frames)
          k(r(UP12 - 0.067), toon=LYING({**MF12, 'lid': 0.6}, lay=[-1.58, 0.0], sq=[1.08, 0.9, 1.08]), toonDur=0.05),
          k(r(UP12 - 0.033), toon={'lay': [-0.75, 0.0], 'sq': [0.86, 1.18, 0.86], 'hip': 0, 'face': {**MF12, 'lid': 0.0, 'eye': 0.4, 'brow': 0.8}}, toonDur=0.02, toonEase='linear'),
          k(UP12, toon={'lay': [0.14, 0.0], 'sq': [0.88, 1.16, 0.88], 'hip': 0, 'face': {**MF12, 'lid': 0.0, 'eye': 0.4, 'brow': 0.7}}, toonDur=0.033, toonEase='linear'),
          k(r(UP12 + 0.067), toon={'lay': [-0.08, 0.0], 'sq': [1.06, 0.95, 1.06], 'hip': 0, 'face': {**MF12, 'lid': 0.1}}, toonDur=0.033),
          k(r(UP12 + 0.133), toon={'lay': [0.04, 0.0], 'sq': [0.98, 1.03, 0.98], 'hip': 0, 'face': MF12}, toonDur=0.033),
          k(r(UP12 + 0.2), toon={'lay': [-0.015, 0.0], 'hip': 0, 'face': MF12}, toonDur=0.033),
          k(r(UP12 + 0.267), toon={'lay': [0.0, 0.0], 'hip': 0, 'face': MF12}, toonDur=0.05),
          k(r(UP12 + 0.34), toon={'touch': {'R': ['torso', 0.0, 0.62, 0.17, 1, 0.0]}, 'hands': {'R': 'grip'}, 'hip': 0, 'face': {**MF12, 'mouth': 'smirk'}}, toonDur=0.1),
          k(r(UP12 + 0.44), toon={'touch': {'R': ['torso', 0.02, 0.58, 0.17, 1, 0.0]}, 'hands': {'R': 'grip'}, 'hip': 0, 'face': {**MF12, 'mouth': 'smirk'}}, toonDur=0.06),
          k(r(WALK12 - 0.05), toon={'hip': 0, 'face': MF12}, toonDur=0.1),
          k(WALK12, to=add(p_, [0.0, 0.0, 0.5]), dur=r(D12b - WALK12), clip='walk', face=0, ease='linear', speed=0.7)]
    # (review 2) they walk off still stiff as boards: a lurch forward at the start (overshoot, back), then a plank's waddle, rocking from side
    # to side at each step, the tags swinging
    ks += [k(r(WALK12 + 0.02), toon={'lay': [0.16, 0.0], 'sq': [0.95, 1.05, 0.95], 'hip': 0, 'face': {**MF12, 'brow': 0.5}}, toonDur=0.06, toonEase='out'),
           k(r(WALK12 + 0.12), toon={'lay': [-0.07, 0.0], 'sq': [1.03, 0.97, 1.03], 'hip': 0, 'face': MF12}, toonDur=0.07)]
    t_ = r(WALK12 + 0.22); j = 0
    while t_ < D12b - 0.08:
        w = 1 if (j + i) % 2 else -1
        ks.append(k(t_, toon={'lay': [0.02, 0.11 * w], 'sq': [1.0 + 0.02 * (j % 2), 1.0 - 0.025 * (j % 2), 1.0], 'hip': 0, 'face': {**MF12, 'lid': 1.0 if j == 3 - i % 2 else 0.4}}, toonDur=0.12, toonEase='inOut'))
        t_ = r(t_ + 0.18); j += 1
    return ks
def AGK12(j, p_):
    who = (0, 1) if j == 0 else (2,)
    ks = [k(0.0, look=add(MLY[who[0]], [0, 0.4, -1.1])), k(0.0, toon={'hip': 0, 'face': AF5}, toonDur=0.0)]
    for i in who:
        hp = add(MLY[i], [0.0, 0.42, -1.1]); t_ = TAGT12[i]; far = abs(MLY[i][0] - p_[0]) > 0.7
        ks += [k(r(t_ - 0.12), look=hp, lookDur=0.06),
               k(r(t_ - 0.1), toon={'reach': {('R' if j == 0 else 'L'): R5(add(hp, [0, 0.4, 0]), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'hose': 0.2 if far else 0.0, 'hip': 0, 'face': AF5}, toonDur=0.06),
               k(t_, toon={'reach': {('R' if j == 0 else 'L'): R5(hp, 1, 0.0)}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.7, 0, 0, 1, None]}, 'sq': [1.06, 0.94, 1.06], 'hose': 0.25 if far else 0.0, 'hip': 0, 'face': {**AF5, 'mouth': 'clench'}}, toonDur=0.03)]
    ks += [k(r(max(TAGT12[i] for i in who) + 0.14), toon={'hip': 0, 'face': AF5}, toonDur=0.15), k(r(max(TAGT12[i] for i in who) + 0.2), look='camera', lookDur=0.2),
           *blink(r(UP12 + 0.3), AF5, {'hip': 0}),
           k(r(WALK12 + 0.08), to=add(p_, [0.0, 0.0, 0.5]), dur=r(D12b - WALK12 - 0.08), clip='walk', face=0, ease='linear', speed=0.7)]
    return ks
# (review 2) the tags a little further out (the middle minister's belly swallowed his)
TAGS12 = [TAG(f'etiq12_{i}', n, needle=[6.2, 6.6, 6.4][i], scale=0.01, dz=[0.05, 0.12, 0.05][i], swing=[[TAGT12[i], 0.3, 10, 3.0], [r(UP12 + 0.02), 0.4, 9, 2.0], [r(WALK12 + 0.1), 0.25, 8, 1.2]], keys=[k(TAGT12[i], scale=1.0, dur=0.06)]) for i, n in enumerate(NAMES7)]
st.shot('S12b', 'whiteVoid', setOpts={'color': '#9EB0C4'}, look=LOOKC,
        actors=[*[act(n, p_, 0, 'stand', 'neutral', keys=MINK12(i, p_)) for i, (n, p_) in enumerate(zip(NAMES7, MLY))], *[act(f'agent{j + 1}', p_, [90, -90][j], 'stand', 'neutral', keys=AGK12(j, p_)) for j, p_ in enumerate(AGP12)]],
        props=[COR('12b', doorX=-1.2), P('porte12b_m', 'tacheBox', pos=[0.0, 1.07, -2.97], opts={'w': 1.0, 'h': 2.14, 'd': 0.06, 'color': '#7A8C9A'}), P('porte12b_d', 'tacheBox', pos=[1.2, 1.07, -2.97], opts={'w': 1.0, 'h': 2.14, 'd': 0.06, 'color': '#7A8C9A'}),
               *SIDEWALLS('12b'), P('brillant12b', 'ttShine', pos=[0, 0, 1.5], opts={'w': 4.0, 'd': 9.0, 'tint': '#FFFFFF', 'k': 1.5, 'n': 9, 'glints': 12}), *TAGS12,
               TAG('etiqA12b', 'agent1', needle=6.4, dz=0.05), TAG('etiqB12b', 'agent2', needle=6.8, dz=0.05)],
        cams=[C12b])
for t_ in TAGT12: st.cue('clack', 'S12b', t_, 0.3)
st.cue('sfx:spring', 'S12b', UP12, 0.2)
for j in range(4): st.cue('sfx:step', 'S12b', r(WALK12 + 0.15 + 0.3 * j), 0.08)

# 13: yesterday he slipped in his own kitchen, now gleaming. From high in front: he walks in toward us with a toast in his mitten on the shiny
#     tiles; on « glissé » his feet shoot out forward, he hangs in the air flat (eyes out, arms streaming, the toast flying up, spinning) and
#     drops flat on his back like a rug, squashed paper-thin (stars), then springs back to his own thickness; the toast lands butter side down
#     beside his head
D13 = st.dur('S13'); GLI13 = W('S13', 'L13', 4); CUI13 = W('S13', 'L13', 7)
H13A = [0.15, 0.0, -2.0]; H13B = [0.15, 0.0, -0.6]
SLIP13 = r(GLI13 - 0.08)
# (review 2) the drop re-timed on whole frames (the shot starts on a frame): the hang to HANG13, two stretched fall frames, the impact frame on
# DOWN13, the rug from the next frame; the camera never moves closer
HANG13 = 1.4333; DOWN13 = 1.5333
TO13 = [0.62, 0.045, -2.0]
# lying by `lay` he pivots about his feet, the splat clip about his hips: the feet are kept a hip-length ahead (+Z) of the rug's place so the
# body does not jump toward the lens when the clip takes over (that jump read as a huge face); the root then steps back between two frames
RUG13 = [0.15, 0.0, -0.45]; HIPL = 0.95
AIR13 = [RUG13[0], 0.85, r(RUG13[2] + HIPL)]
# (review 3) the hang tipped across the frame: a toon yaw turns him so his feet shoot out to the right and toward the lens, tipped past flat
# (feet higher than the head) at hip height over the tiles, a contact shadow under him; his head comes forward off the arms
YAW13 = 0.7; LAY13 = -1.86; HC13 = [0.15, 0.0, -0.9]
FEET13 = [r(HC13[0] + math.sin(YAW13) * 1.05), 1.3, r(HC13[2] + math.cos(YAW13) * 1.05)]
F13 = [0.1, 3.3, 2.8]; L13 = [0.1, 0.78, -1.4]
C13 = cam(0.0, F13, add(F13, [0.0, -0.1, -0.2]), L13, L13, lens=46, ease='inOut')
chkc('S13', C13, {'headWalk': add(H13A, [0, 2.4, 0]), 'feetWalk': H13A, 'headSlip': add(H13B, [0, 2.4, 0]), 'feetAir': FEET13, 'headAir': [-0.6, 0.7, -1.75], 'shadow': HC13, 'feetLie': add(RUG13, [0, 0, 0.95]), 'headLie': add(RUG13, [0, 0.2, -1.4]), 'toast': TO13, 'toastHigh': [0.45, 2.6, -1.2]})
HF13 = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}
TH13 = lambda t_: lerp3(H13A, H13B, min(1.0, t_ / SLIP13))
POPF = {'lid': 0.0, 'eye': 0.5, 'pop': 0.75, 'popLen': 0.32, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}
AIRK = lambda j=0, **x: {'lay': [LAY13, 0.0], 'yaw': YAW13, 'hairUp': 1.3 if j % 2 else 1.1, 'auto': 0, 'sq': [1.0 + 0.03 * (j % 2), 1.0 - 0.02 * (j % 2), 1.0], 'face': {**POPF, 'pop': 0.75 + 0.08 * (j % 2)},
                         'bend': {'neck': [0.7, 0, 0, 1, None], 'spine': [0.25, 0, 0, 1, None]}, **x}
HERO13 = [k(0.0, look='camera'), k(0.0, to=H13B, dur=SLIP13, clip='walk', face=0, ease='linear'),
          *[k(r(t_), toon={'reach': {'R': R5(add(TH13(t_ + 0.1), [-0.3, 1.25, 0.42]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'face': HF13}, toonDur=0.15) for t_ in [0.0, 0.2, 0.4, 0.6, 0.8]],
          k(SLIP13, clip='fallDrag', params={'expr': 'take', 'jaw': 0.8, 'stretch': 1.0}, blend=0.04),
          # the feet shoot out ahead and up: he hangs flat in the air, eyes out on stalks, trembling, the toast spinning above him
          k(SLIP13, to=FEET13, dur=0.12, glide=True, face='keep', ease='out'),
          k(SLIP13, toon=AIRK(0), toonDur=0.06, toonEase='out'),
          *[k(r(SLIP13 + 0.12 + 0.067 * j), toon=AIRK(j + 1), toonDur=0.03) for j in range(int((HANG13 - SLIP13 - 0.14) / 0.067))],
          # two stretched fall frames (long along the body, thin), the impact frame squashed flat with the lines round him, then the rug
          # (stills r2) the impact frame lies a hand over the floor: laid flat about his feet at the floor, half of him (the head) sank under it
          # (review 3) the two fall frames keep him across the frame (laid along Z for a frame he read as standing up again): only the impact
          # frame lays him straight
          k(HANG13, to=[FEET13[0], 0.45, FEET13[2]], dur=0.07, glide=True, face='keep', ease='in'),
          k(r(DOWN13 - 0.03), to=[AIR13[0], 0.12, AIR13[2]], dur=0.02, glide=True, face='keep', ease='linear'),
          k(r(HANG13 - 0.01), toon={'lay': [LAY13, 0.0], 'yaw': YAW13, 'hairUp': 1.5, 'auto': 0, 'sq': [0.82, 1.26, 0.82], 'face': POPF}, toonDur=0.02, toonEase='linear'),
          k(r(DOWN13 - 0.025), toon={'lay': [-1.5708, 0.0], 'hairUp': 1.5, 'auto': 0, 'sq': [1.9, 1.04, 0.45], 'face': {'lid': 1.0, 'mouth': 'grimace', 'brow': -0.9, 'noBlink': 1}}, toonDur=0.02, toonEase='linear'),
          k(DOWN13, to=RUG13, dur=0.02, glide=True, face='keep', ease='linear'),
          k(DOWN13, clip='splat', params={'popAt': 99, 'stars': 1.6, 'blinkAt': 0.2}, blend=0.02),
          k(DOWN13, toon={'auto': 0, 'sq': [1.12, 1.0, 0.7]}, toonDur=0.02, toonEase='linear'),
          k(r(DOWN13 + 0.1), toon={'auto': 0}, toonDur=0.12, toonEase='out')]
TK13 = [k(SLIP13, to=[0.42, 2.25, -1.3], dur=0.42, ease='out'), k(SLIP13, rotTo=[3.5 + 2 * PI, 1.0, 6.0], dur=r(DOWN13 + 0.45 - SLIP13), ease='linear'), k(r(SLIP13 + 0.42), to=TO13, dur=r(DOWN13 + 0.45 - SLIP13 - 0.42), ease='in'),
        k(r(DOWN13 + 0.45), rotTo=[PI, 0.3, 0.0], dur=0.0), k(r(DOWN13 + 0.45), squash=[1.3, 0.55, 1.3], dur=0.4)]
st.shot('S13', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('mec', H13A, 0, 'stand', 'neutral', keys=HERO13)],
        props=[TABLE('table13', pos=[-0.9, 0.0, -2.6]), P('brillant13', 'ttShine', pos=[0, 0, -1.2], opts={'w': 7.0, 'd': 5.0, 'tint': '#FFFFFF', 'k': 1.9, 'n': 11, 'wide': 1.3, 'glints': 22}),
               TOAST('tartine13', add(H13A, [-0.3, 1.25, 0.42]), rot=[0.0, 0.0, 0.0], keys=[k(0.0, to=add(H13B, [-0.3, 1.25, 0.42]), dur=SLIP13, ease='linear'), *TK13]),
               P('ombre13', 'ttShadow', pos=HC13, ry=r(math.degrees(YAW13), 1), opts={'w': 0.8, 'd': 2.3, 'a': 0.5, 'at': [[r(SLIP13 + 0.02), 0.0], [r(SLIP13 + 0.12), 1.0], [r(DOWN13 - 0.01), 1.0], [r(DOWN13 + 0.03), 0.0]]}),
               P('beurre13', 'ttSplat', pos=[TO13[0], 0.0, TO13[2]], opts={'r': 0.3, 'at': [[r(DOWN13 + 0.45), 0.0], [r(DOWN13 + 0.57), 1.0]]}),
               P('choc13', 'ttImpact', pos=add(RUG13, [0.0, 0.1, -0.2]), face='camera', opts={'at': r(DOWN13 - 0.01), 'r': 1.15, 'ring': True, 'n': 14, 'dur': 0.2}),
               P('etincelles13', 'ttSparkle', pos=[0, 0, 0], opts={'pts': [[x, 0.06, z, r(0.08 + 0.16 * i), 0.4] for i, (x, z) in enumerate([(-1.0, 0.2), (1.2, -0.3), (-0.4, 0.8), (0.9, 0.9), (-1.3, -1.2), (1.4, -1.9), (-0.6, -1.6), (0.5, -2.4), (1.0, 0.3), (-1.4, 0.6)])], 'period': 1.6})],
        cams=[C13], fx=[{'type': 'shake', 'at': DOWN13, 'dur': 0.25, 'amount': 0.03}])
for t_ in (0.15, 0.45, 0.75): st.cue('sfx:stepSoft', 'S13', t_, 0.12)
st.cue('sfx:slideUp', 'S13', SLIP13, 0.25); st.cue('sfx:splat', 'S13', DOWN13, 0.3); st.cue('thud', 'S13', DOWN13, 0.25); st.cue('sfx:splat', 'S13', r(DOWN13 + 0.45), 0.25)

# 14: he got up in six... Closer and frontal: flat on the tiles he springs back up like a board, wobbles, rubs the small of his back, wincing,
#     and his eyes slide down to the toast at his feet
D14 = st.dur('S14')
H14 = [0.15, 0.0, -0.6]
# (review 3) the toast bigger and tipped on its edge toward the lens (still butter side down, the yellow face now reads); lying flat it was an
# orange sliver
TO14 = [TO13[0], 0.2, TO13[2]]
F14 = [0.3, 1.4, 3.3]; L14 = [0.15, 1.3, -0.8]
C14 = cam(0.0, F14, add(F14, [0.0, 0.0, -0.15]), L14, L14, lens=44, ease='out')
chkc('S14', C14, {'head': add(H14, [0, 2.4, 0]), 'feet': H14, 'toast': TO13})
# (stills 3) he starts flat as in S13's last frame (the splat clip) and springs up out of it, then rubs his back
RUB14 = lambda y, sp: {'touch': {'R': ['torso', -0.12, y, -0.16, 1, 0.0], 'L': ['torso', 0.12, y, -0.16, 1, 0.0]}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [sp, 0, 0, 1, None]}}
HERO14 = [k(0.0, look='camera'), k(0.0, clip='splat', params={'popAt': 0.06, 'stars': 1.2, 'blinkAt': 0.02}),
          k(0.36, clip='stand', blend=0.06),
          k(0.36, toon={**RUB14(0.18, -0.25), 'face': {'lid': 0.7, 'mouth': 'grimace', 'brow': -0.6}}, toonDur=0.08),
          k(0.48, toon={**RUB14(0.26, -0.3), 'face': {'lid': 0.6, 'mouth': 'grimace', 'brow': -0.5}}, toonDur=0.07),
          k(0.6, toon={**RUB14(0.15, -0.25), 'face': {'lid': 0.5, 'mouth': 'grimace', 'brow': -0.4, 'gy': 0.8, 'gx': -0.5}}, toonDur=0.07),
          k(0.72, toon={**RUB14(0.24, -0.28), 'face': {'lid': 0.5, 'mouth': 'grimace', 'brow': -0.4, 'gy': 0.8, 'gx': -0.5}}, toonDur=0.07)]
st.shot('S14', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('mec', H14, 0, 'splat', 'neutral', keys=HERO14)],
        props=[TABLE('table14', pos=[-0.9, 0.0, -2.6]), P('brillant14', 'ttShine', pos=[0, 0, -1.2], opts={'w': 7.0, 'd': 5.0, 'tint': '#FFFFFF', 'k': 1.9, 'n': 11, 'wide': 1.3, 'glints': 22}), TOAST('tartine14', TO14, rot=[2.25, 0.3, 0.0], scale=1.35),
               P('beurre14', 'ttSplat', pos=[TO13[0], 0.0, TO13[2]], opts={'r': 0.3}), P('horloge14', 'ttWallClock', pos=CLOCK, opts={'ticks': [0.05, 0.18, 0.31, 0.44, 0.57, 0.7]})],
        cams=[C14])
st.cue('sfx:spring', 'S14', 0.08, 0.2)
for t_ in [0.05, 0.18, 0.31, 0.44, 0.57, 0.7]: st.cue('sfx:tick', 'S14', t_, 0.3)

# 14b: « secondes. » (review 1) Not a copy of line 2: a low two-shot. The cloth flap is up behind him: the inspector, already out on his knees, has
#      shot his stopwatch up at the hero on a rubber arm, its face to us, the needle a notch further than in line 2; he taps the rim, taps
#      again harder, then slaps it (the watch squashes, the needle jumps further into the red, his tag swings); the hero, still rubbing his
#      back, lets his eyes slide down to it and then shrinks with his eyes popping
D14b = st.dur('S14b')
H14b = [0.45, 0.0, -1.0]; RYH14b = -15; I14b = [-0.5, 0.0, -1.25]; RYI14b = 25
SW14b = [-0.02, 1.4, -0.1]; SW14b0 = off(I14b, RYI14b, 0.25, -0.2, 0.62)
TAPS14b = [0.12, 0.27, 0.46]
F14b = [0.1, 1.1, 2.6]; L14b = [0.0, 1.0, -0.4]
C14b = cam(0.0, F14b, add(F14b, [0.0, 0.0, -0.12]), L14b, L14b, lens=52, ease='out')
chkc('S14b', C14b, {'hTop': add(H14b, [0, 2.42, 0]), 'hChin': add(H14b, [0, 1.75, 0]), 'iTop': add(I14b, [0, 1.3, 0]), 'iKnee': add(I14b, [0, 0.05, 0.3]), 'watch': SW14b, 'watchT': add(SW14b, [0, 0.2, 0])})
RAD14b = 0.19
def IK14b(tap=None, hand='point', sp=0.1, **x):
    d = {'reach': {'R': R5(GRIP2(SW14b, RAD14b), 1, 0.0), **({'L': R5(tap, 1, 0.0)} if tap else {})}, 'hands': {'R': 'grip', 'L': hand if tap else 'rest'}, 'bend': {'spine': [sp, 0, 0, 1, None], 'neck': [-0.2, 0, 0, 1, None]}, 'hose': 0.12, 'hip': 0}
    d.update(x); return d
# (review 3) the slap winds up above the watch on his own side (out past the hero the long arm bent at right angles across his body)
WIND14b = add(SW14b, [-0.12, 0.42, 0.18])
INSK14b = [k(0.0, look=add(H14b, [0, 1.95, 0])), k(0.0, clip='kneel'), k(0.0, toon={**IK14b(), 'face': IF}, toonDur=0.0),
           k(r(TAPS14b[0] - 0.06), toon={**IK14b(TAP2(SW14b, RAD14b, 0.08)), 'face': {**IF, 'brow': -0.2}}, toonDur=0.04),
           k(TAPS14b[0], toon={**IK14b(TAP2(SW14b, RAD14b)), 'face': {**IF, 'mouth': 'o'}}, toonDur=0.03),
           k(r(TAPS14b[1] - 0.07), toon={**IK14b(TAP2(SW14b, RAD14b, 0.14)), 'face': {**IF, 'brow': -0.5}}, toonDur=0.04),
           k(TAPS14b[1], toon={**IK14b(TAP2(SW14b, RAD14b)), 'sq': [1.04, 0.96, 1.04], 'face': {**IF, 'mouth': 'open', 'brow': -0.6}}, toonDur=0.03),
           # the slap: a wide wind-up of the open mitten, then a smack on the rim with the whole body behind it
           k(r(TAPS14b[2] - 0.1), toon={**IK14b(WIND14b, 'open', -0.05), 'sq': [0.95, 1.06, 0.95], 'face': {**IF, 'lid': 0.1, 'brow': 0.5, 'mouth': 'clench'}}, toonDur=0.06, toonEase='out'),
           k(TAPS14b[2], toon={**IK14b(TAP2(SW14b, RAD14b, -0.02), 'open', 0.25), 'sq': [1.1, 0.9, 1.1], 'face': {**IF, 'lid': 0.8, 'brow': -0.8, 'mouth': 'clench'}}, toonDur=0.03),
           k(r(TAPS14b[2] + 0.12), toon={**IK14b(TAP2(SW14b, RAD14b, 0.05), 'open'), 'face': {**IF, 'lid': 0.45, 'brow': -0.6, 'mouth': 'line'}}, toonDur=0.08),
           *blink(r(D14b - 0.16), {**IF, 'lid': 0.45, 'brow': -0.6}, IK14b(TAP2(SW14b, RAD14b, 0.05), 'open'))]
RUB14b = lambda y, f: {**RUB14(y, -0.25), 'hip': 0, 'face': f}
HF14b = {'lid': 0.5, 'mouth': 'grimace', 'brow': -0.4}
HERO14b = [k(0.0, look='camera'), k(0.0, toon=RUB14b(0.18, HF14b), toonDur=0.0),
           k(0.1, toon=RUB14b(0.26, {**HF14b, 'gy': 0.6, 'gx': -0.4}), toonDur=0.06),
           k(0.22, toon=RUB14b(0.16, {**HF14b, 'lid': 0.3, 'gy': 0.85, 'gx': -0.6, 'mouth': 'line'}), toonDur=0.06),
           k(0.34, toon=RUB14b(0.24, {**HF14b, 'lid': 0.2, 'gy': 0.85, 'gx': -0.6, 'mouth': 'line', 'brow': 0.2}), toonDur=0.06),
           *beat(r(TAPS14b[2] + 0.04), {**RUB14b(0.2, {'pop': 0.45, 'popLen': 0.2, 'brow': 1.0, 'mouth': 'wavy', 'sweat': 1.0, 'gy': 0.6, 'gx': -0.5}), 'sq': [1.08, 0.88, 1.08], 'scl': {'head': [0.94, 0.94, 0.94]}},
                 antic={**RUB14b(0.2, {'lid': 0.0, 'eye': 0.4, 'brow': 0.6, 'mouth': 'o', 'gy': 0.8, 'gx': -0.6}), 'sq': [0.96, 1.05, 0.96]}, hold=0.24,
                 settle={**RUB14b(0.2, {'lid': 0.1, 'eye': 0.4, 'brow': 0.8, 'mouth': 'wavy', 'sweat': 1.0, 'gy': 0.6, 'gx': -0.5}), 'sq': [1.05, 0.92, 1.05]})]
st.shot('S14b', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('mec', H14b, RYH14b, 'stand', 'neutral', keys=HERO14b), act('inspecteur', I14b, RYI14b, 'kneel', 'neutral', scale=SI, keys=INSK14b)],
        props=[TABLE('table14b', pos=[-0.9, 0.0, -2.6], lift=[[0.0, 0.62]]), P('brillant14b', 'ttShine', pos=[0, 0, -1.2], opts={'w': 7.0, 'd': 5.0, 'tint': '#FFFFFF', 'k': 1.9, 'n': 11, 'wide': 1.3, 'glints': 22}),
               TOAST('tartine14b', TO14, rot=[2.25, 0.3, 0.0], scale=1.35), P('beurre14b', 'ttSplat', pos=[TO13[0], 0.0, TO13[2]], opts={'r': 0.3}),
               WATCH('chrono14b', SW14b, needle=[[0.0, 6.25], [r(TAPS14b[2] - 0.01), 6.25], [r(TAPS14b[2] + 0.05), 6.75], [r(TAPS14b[2] + 0.12), 6.6]], ry=12, rad=RAD14b,
                     keys=[k(0.0, squash=[1.08, 0.94, 1.0], dur=0.2), k(TAPS14b[0], squash=[1.06, 0.95, 1.0], dur=0.15), k(TAPS14b[1], squash=[1.1, 0.92, 1.0], dur=0.18), k(TAPS14b[2], squash=[1.35, 0.72, 1.0], dur=0.35)]),
               TAG('etiq14b', 'inspecteur', needle=7.0, swing=[[TAPS14b[1], 0.15, 12, 4], [TAPS14b[2], 0.45, 10, 2.5]])],
        cams=[C14b])
for t_ in TAPS14b[:2]: st.cue('sfx:tick', 'S14b', t_, 0.3)
st.cue('clack', 'S14b', TAPS14b[2], 0.3)

# 15: he belongs to the State, assigned under a table. Frontal, the hero between two grey agents (tags on): the left agent slaps a big brown tag
#     onto his chest (it pops, swings; he deflates, squashed and drooping, then re-inflates stiff); NATIONALISÉ stamps; the right agent puts a
#     stopwatch into his mitten; he looks down at the tag, then at us; on « table » both agents point down at the floor, briefly
D15 = st.dur('S15'); ETAT15 = W('S15', 'L15', 3); AFF15 = W('S15', 'L15', 6); TAB15 = W('S15', 'L15', 9)
H15 = [0.0, 0.0, -0.4]; AL15 = [-0.85, 0.0, -0.7]; AR15 = [0.85, 0.0, -0.7]
SLAP15 = r(ETAT15 - 0.1); GIVE15 = r(AFF15 - 0.05)
F15 = [0.0, 1.45, 5.1]; L15 = [0.0, 1.3, -0.6]
C15 = cam(0.0, F15, add(F15, [0.0, 0.0, -0.3]), L15, L15, lens=42, ease='inOut')
chkc('S15', C15, {'head': add(H15, [0, 2.4, 0]), 'chin': add(H15, [0, 1.75, 0]), 'tag': add(H15, [0, 1.3, 0.2]), 'aL': add(AL15, [0, 2.35, 0]), 'aR': add(AR15, [0, 2.35, 0]), 'aLs': add(AL15, [-0.35, 1.0, 0]), 'aRs': add(AR15, [0.35, 1.0, 0])})
WG15 = off(H15, 0, 0.42, -0.3, 1.2)
HF15 = {'lid': 0.4, 'mouth': 'line', 'brow': 0.0}
HERO15 = [k(0.0, look='camera'), k(0.0, toon={'face': HF15}, toonDur=0.0),
          *beat(SLAP15, {'sq': [1.14, 0.84, 1.14], 'bend': {'spine': [0.35, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'scl': {'head': [1.12, 0.86, 1.0]}, 'face': {'lid': 0.85, 'mouth': 'wavy', 'brow': -0.7}},
                antic={'sq': [0.96, 1.05, 0.96], 'face': {**HF15, 'brow': 0.4}}, hold=0.36, over={'sq': [0.95, 1.07, 0.95], 'face': {**HF15, 'lid': 0.2}}, settle={'face': HF15}, settle_f=6),
          k(r(SLAP15 + 0.55), look=add(H15, [0, 1.3, 0.35]), lookDur=0.12), k(r(SLAP15 + 0.55), toon={'face': {**HF15, 'gy': 0.7}, 'bend': {'neck': [0.3, 0, 0, 1, None]}}, toonDur=0.12),
          k(r(GIVE15), toon={'reach': {'R': R5(WG15, 1, 0.0)}, 'hands': {'R': 'grip'}, 'face': {**HF15, 'gy': 0.5}}, toonDur=0.1),
          k(r(GIVE15 + 0.4), look='camera', lookDur=0.15), k(r(GIVE15 + 0.4), toon={'reach': {'R': R5(WG15, 1, 0.0)}, 'hands': {'R': 'grip'}, 'face': {**HF15, 'lid': 0.5, 'brow': -0.2}}, toonDur=0.12),
          *blink(r(TAB15 - 0.3), {**HF15, 'lid': 0.5, 'brow': -0.2}, {'reach': {'R': R5(WG15, 1, 0.0)}, 'hands': {'R': 'grip'}})]
def AGK15(side, p_):
    hand = 'L' if side > 0 else 'R'
    ks = [k(0.0, look=add(H15, [0, 1.95, 0])), k(0.0, toon={'hip': 0, 'face': AF5}, toonDur=0.0)]
    if side < 0:
        ks += [k(r(SLAP15 - 0.14), toon={'reach': {hand: R5(add(H15, [0.0, 1.45, 0.75]), 1, 0.0)}, 'hands': {hand: 'open'}, 'hip': 0, 'face': AF5}, toonDur=0.1),
               k(SLAP15, toon={'reach': {hand: R5(add(H15, [0.0, 1.32, 0.22]), 1, 0.0)}, 'hands': {hand: 'open'}, 'sq': [1.04, 0.96, 1.04], 'hip': 0, 'face': {**AF5, 'mouth': 'clench'}}, toonDur=0.03),
               k(r(SLAP15 + 0.25), toon={'hip': 0, 'face': AF5}, toonDur=0.15), *life(r(SLAP15 + 0.4), r(TAB15 - 0.15), AF5, {'hip': 0}, blinks=[r(SLAP15 + 0.9)])]
    else:
        ks += [k(r(GIVE15 - 0.25), toon={'reach': {hand: R5(add(WG15, [0.1, 0.05, 0.05]), 1, 0.0)}, 'hands': {hand: 'grip'}, 'hip': 0, 'face': AF5}, toonDur=0.15),
               k(r(GIVE15 + 0.12), toon={'reach': {hand: R5(add(WG15, [0.25, -0.05, 0.1]), 1, 0.0)}, 'hands': {hand: 'open'}, 'hip': 0, 'face': AF5}, toonDur=0.1),
               k(r(GIVE15 + 0.35), toon={'hip': 0, 'face': AF5}, toonDur=0.15)]
    ks += [k(r(TAB15 - 0.12), look=add(H15, [0, 0.2, 0.5]), lookDur=0.1), k(r(TAB15 - 0.12), toon={'reach': {hand: R5(off(p_, 0, 0.5, 0.0, 0.7), 1, 0.0)}, 'hands': {hand: 'point'}, 'hip': 0, 'face': AF5}, toonDur=0.08),
           k(r(TAB15 + 0.3), toon={'hip': 0, 'face': AF5}, toonDur=0.15)]
    return ks
WK15 = [k(0.0, to=add(AR15, [-0.25, 1.15, 0.4]), dur=0.0), k(r(GIVE15 - 0.25), to=add(WG15, [0.1, 0.05, 0.05]), dur=0.15, ease='out'), k(r(GIVE15), to=WG15, dur=0.1, ease='out')]
st.shot('S15', 'kitchenDay', setOpts=KSET, look=LOOKK, actors=[act('mec', H15, 0, 'stand', 'neutral', keys=HERO15), act('agent1', AL15, 25, 'stand', 'neutral', keys=AGK15(-1, AL15)), act('agent2', AR15, -25, 'stand', 'neutral', keys=AGK15(1, AR15))],
        props=[TABLE('table15', pos=[-0.9, 0.0, -2.6]), P('brillant15', 'ttShine', pos=[0, 0, -1.2], opts={'w': 7.0, 'd': 5.0, 'tint': '#FFFFFF', 'k': 1.9, 'n': 11, 'wide': 1.3, 'glints': 22}),
               TAG('etiq15', 'mec', needle=6.0, scale=0.01, swing=[[SLAP15, 0.4, 9, 2.2]], keys=[k(SLAP15, scale=1.0, dur=0.05)]), TAG('etiqA15', 'agent1', needle=6.4), TAG('etiqB15', 'agent2', needle=6.8),
               WATCH('chrono15', add(AR15, [-0.25, 1.15, 0.4]), at_=0.0, rad=0.11, keys=WK15)],
        cams=[C15])
st.card('S15', 'NATIONALISÉ', at=r(ETAT15 + 0.05))
st.cue('clack', 'S15', SLAP15, 0.35); st.cue('sfx:slideDown', 'S15', r(SLAP15 + 0.05), 0.12); st.cue('thud', 'S15', r(ETAT15 + 0.05), 0.2); st.cue('sfx:click', 'S15', GIVE15, 0.2)

# 16: the inspector's. (review 1) Low on the tiles before his own table, the cloth drawn aside: the inspector shuffles over on his pillow first
#     (two little hops); the hero, now in grey with his tag, crawls in from the right BEHIND the table's front plane, low on his knees and in
#     profile, the stopwatch in his mitten; arrived, he turns to us, straightens and bumps his head on the underside of the table top (it
#     squashes flat, an impact), then sits back into the same squashed pose as line 17; both look at us
D16 = st.dur('S16')
IN16A = [-0.22, 0.0, -1.18]; IN16B = [-0.52, 0.0, -1.18]
HE16B = [0.22, -0.06, -1.12]
ZC16 = -1.1; YC16 = -0.06
# (review 2) the crawl spread over about 0.55 s, sunk the whole way (rising with the crawl had put his head above the top line); arrived he
# turns to us and rises in one vertical move (automatic layers off: no lean toward it), straight into the underside of the top: the head
# squashes flat (wider, shorter, eyes squeezed, cheeks bulging) and stays squashed into line 17
# (review 3) the crawl stops a little further right: his head no longer crosses the inspector's face
HE16A = [1.5, -0.5, ZC16]; HE16M = [0.92, -0.5, ZC16]; HE16C = [0.22, YC16, ZC16]; HE16T = HE16C
CRAWL16 = (0.05, 0.62); TURN16 = 0.62; BUMP16 = 0.78; SIT16 = 0.92
F16 = [0.0, 0.36, 1.9]; L16 = [-0.1, 0.55, -1.0]
C16 = cam(0.0, F16, add(F16, [0.0, 0.0, -0.12]), L16, L16, lens=50, ease='inOut')
chkc('S16', C16, {'insp': add(IN16B, [0, 0.8, 0.1]), 'hero': add(HE16B, [0, 1.0, 0.1]), 'crawlIn': [0.75, 0.75, ZC16], 'crawlEnd': [0.0, 0.75, ZC16], 'top': [TBL[0], TH, TFRONT], 'under': [HE16T[0], TH - 0.06, ZC16], 'tagH': add(HE16B, [0, 0.6, 0.3])})
GF16 = {'lid': 0.4, 'mouth': 'line', 'brow': -0.1}
INSK16 = [k(0.0, look=[1.0, 0.7, -1.0]), k(0.0, clip='reclineBack'), k(0.0, toon={'hip': 0, 'face': {**IF3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
          k(0.02, to=lerp3(IN16A, IN16B, 0.5), dur=0.12, glide=True, face=0, ease='inOut'), k(0.16, to=IN16B, dur=0.12, glide=True, face=0, ease='inOut'),
          k(0.02, toon={'sq': [1.1, 0.9, 1.1], 'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.5}}, toonDur=0.04), k(0.08, toon={'sq': [0.94, 1.07, 0.94], 'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.5}}, toonDur=0.04),
          k(0.16, toon={'sq': [1.1, 0.9, 1.1], 'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.5}}, toonDur=0.04), k(0.22, toon={'sq': [0.95, 1.06, 0.95], 'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.45}}, toonDur=0.04),
          k(0.3, toon={'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.4}}, toonDur=0.08),
          k(r(BUMP16 + 0.02), toon={'sq': [1.04, 0.96, 1.04], 'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.9}}, toonDur=0.03), k(r(BUMP16 + 0.12), toon={'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.4}}, toonDur=0.08),
          k(0.98, look='camera', lookDur=0.15), *blink(1.12, {**IF3, 'mouth': 'line', 'lid': 0.4}, {'hip': 0})]
HC16 = lambda t_: lerp3(HE16A, HE16M, min(1.0, max(0.0, (t_ - CRAWL16[0]) / (CRAWL16[1] - CRAWL16[0]))))
WLAP = off(HE16B, 0, 0.4, 0.06, 0.2)
# (stills r1fix) the bent spine alone kept him too tall for the space: the whole kneeling body tips forward over his knees (lay), the head up
CR16 = lambda kneel=1.0, **x: {'lay': [0.56 * kneel, 0.0], 'bend': {'spine': [0.5 * kneel, 0, 0, 1, None], 'neck': [-1.0 * kneel, 0, 0, 1, None]}, 'hip': 0, 'auto': 0, **x}
def HAND16(t_, side, j):
    p_ = HC16(t_); step = 0.12 if (j % 2 == 0) == (side == 'R') else -0.04
    return off([p_[0], 0.0, p_[2]], -90, r(0.62 + step), 0.16 if side == 'R' else -0.16, 0.06)
Y16 = {'yaw': r(PI / 2, 4)}
SQH = {'scl': {'head': [1.55, 0.5, 1.18]}}
SQF = {'lid': 0.85, 'low': 0.5, 'mouth': 'wavy', 'brow': -0.7, 'cheeks': 1.0}
HSIT = lambda **x: {'reach': {'R': R5(WLAP, 1, 0.0)}, 'hands': {'R': 'grip'}, 'bend': {'neck': [0.2, 0, 0, 1, None]}, 'hip': 0, 'auto': 0, **Y16, **SQH, **x}
NCR16 = int((CRAWL16[1] - CRAWL16[0]) / 0.09) + 1
HEROK16 = [k(0.0, look='camera'), k(0.0, clip='kneel'),
           k(0.0, toon={**CR16(), 'reach': {'R': R5(HAND16(0.0, 'R', 0), 1, 0.0), 'L': R5(HAND16(0.0, 'L', 0), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'face': GF16}, toonDur=0.0),
           k(CRAWL16[0], to=HE16M, dur=r(CRAWL16[1] - CRAWL16[0]), glide=True, face=-90, ease='inOut'),
           *[k(r(CRAWL16[0] + 0.09 * j), toon={**CR16(), 'reach': {'R': R5(HAND16(r(CRAWL16[0] + 0.09 * j + 0.05), 'R', j), 1, 0.0), 'L': R5(HAND16(r(CRAWL16[0] + 0.09 * j + 0.05), 'L', j), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'},
                                                  'sq': ([1.03, 0.97, 1.03] if j % 2 else [0.98, 1.02, 0.98]) if j > 1 else [1.06, 0.86, 1.06], 'face': {**GF16, 'gx': -0.4}}, toonDur=0.07) for j in range(NCR16)],
           # arrived: he turns to us and rises straight up into the nook (one vertical move, no lean), the head meets the underside of the top
           k(TURN16, to=HE16C, dur=r(BUMP16 - TURN16), glide=True, face='keep', ease='out'),
           k(TURN16, clip='reclineBack', blend=0.14),
           k(TURN16, toon=HSIT(scl={'head': [1.15, 0.8, 1.05]}, face={**GF16, 'lid': 0.2, 'brow': 0.4}), toonDur=r(BUMP16 - TURN16 - 0.02), toonEase='out'),
           k(r(BUMP16 - 0.01), toon=HSIT(scl={'head': [1.75, 0.38, 1.22]}, sq=[1.06, 0.92, 1.06], face={'lid': 1.0, 'mouth': 'grimace', 'brow': -0.9, 'cheeks': 1.0}), toonDur=0.02, toonEase='linear'),
           k(r(BUMP16 + 0.07), toon=HSIT(scl={'head': [1.45, 0.56, 1.16]}, face={**SQF, 'lid': 0.95}), toonDur=0.05),
           k(r(BUMP16 + 0.13), toon=HSIT(scl={'head': [1.6, 0.47, 1.19]}, face=SQF), toonDur=0.05),
           k(SIT16, toon=HSIT(face=SQF), toonDur=0.08),
           k(r(SIT16 + 0.08), look='camera', lookDur=0.15), *life(r(SIT16 + 0.12), D16, {**SQF, 'lid': 0.75}, HSIT())]
WM16 = [(r(CRAWL16[0] + 0.09 * j), add(HAND16(r(CRAWL16[0] + 0.09 * j + 0.05), 'R', j), [0.0, 0.1, 0.0]), 0.07, 'out') for j in range(NCR16)] + [(TURN16, WLAP, 0.14, 'out')]
UNDER = lambda n: [P(f'oreiller{n}', 'ttPillow', pos=[-0.15, 0.5, -1.6], rot=[-0.3, 0, 0], opts={'w': 1.3, 'h': 0.6, 'd': 0.24}), P(f'lampe{n}', 'ttNookLamp', pos=[-0.9, 0.0, -1.2], opts={'power': 1.6}),
                   P(f'tasse{n}', 'ttMug', pos=[0.62, 0.0, -0.8], opts={'r': 0.075}), P(f'lumiere{n}', 'ttFill', pos=[-0.15, 0.7, -0.25], opts={'I': 1.1, 'R': 1.9, 'color': '#FFE2B8'})]
st.shot('S16', 'kitchenDay', setOpts=KSET, look=LOOKU, actors=[act('inspecteur', IN16A, 0, 'reclineBack', 'neutral', scale=SI, keys=INSK16), act('mecGris', HE16A, -90, 'kneel', 'neutral', keys=HEROK16)],
        props=[TABLE('table16', open=[[0.0, 1.0]], sides=[True, False]), NEARFLOOR(16), *UNDER(16), TAG('etiq16i', 'inspecteur', needle=7.0, dz=0.06), TAG('etiq16h', 'mecGris', needle=6.0),
               P('choc16', 'ttImpact', pos=[HE16B[0], r(TH - 0.05), r(HE16B[2] + 0.15)], face='camera', opts={'at': BUMP16, 'r': 0.36}),
               WATCH('chrono16', add(HAND16(0.0, 'R', 0), [0.0, 0.1, 0.0]), at_=0.0, rad=0.1, keys=MOVES(WM16))],
        cams=[C16])
for t_ in (0.14, 0.32, 0.5): st.cue('sfx:stepSoft', 'S16', t_, 0.15)
st.cue('sfx:boing', 'S16', r(BUMP16 + 0.02), 0.12); st.cue('thud', 'S16', BUMP16, 0.25)

# 17: he, it was seven seconds. The same frame, a little wider and higher so the table's edge shows at the top: both in grey, tags side by side;
#     the inspector lifts his tag and turns it round to the lens: on its back a big stopwatch drawing, the needle deep in the red; then both stare
#     up at a toast teetering on the edge of a plate over the table's edge, rocking; a slow blink each; hold, deadpan
D17 = st.dur('S17'); SEPT17 = W('S17', 'L17', 2); SEC17 = W('S17', 'L17', 3)
FLIP17 = (0.35, r(SEPT17 - 0.08))
UP17 = r(SEC17 + 0.45)
# (stills 3) the plate hangs over the table's edge and the toast over the plate's rim, tilted toward us: it plainly teeters
PL17 = [-0.05, r(TH + 0.012), r(TFRONT - 0.06)]
TT17 = [0.0, r(TH + 0.075), r(TFRONT + 0.06)]
F17 = [-0.05, 0.48, 1.95]; L17 = [-0.15, 0.62, -1.0]
C17 = cam(0.0, F17, add(F17, [0.0, 0.0, -0.18]), L17, add(L17, [0, 0.03, 0]), lens=50, ease='inOut')
chkc('S17', C17, {'insp': add(IN16B, [0, 0.8, 0.1]), 'hero': add(HE16B, [0, 1.0, 0.1]), 'tagI': add(IN16B, [0, 0.5, 0.3]), 'toast': TT17, 'toastTop': add(TT17, [0, 0.15, 0]), 'cornerL': [TBL[0] - hw3, TH, TFRONT]})
IN17 = {'hip': 0}
TAGLIFT = add(IN16B, [0.0, 0.42, 0.42])
def sblink(t, face, keep):
    # (review 2) a slow deadpan blink: the lids come down over 0.16 s, stay shut, open over 0.22 s
    return [k(r(t), toon={**keep, 'face': {**face, 'lid': 1.0}}, toonDur=0.16, toonEase='inOut'), k(r(t + 0.34), toon={**keep, 'face': face}, toonDur=0.22, toonEase='inOut')]
def hold_sblink(t0, t1, tb, face, keep):
    return [*life(t0, r(tb - 0.05), face, keep), *sblink(tb, face, keep), *life(r(tb + 0.6), t1, face, keep)]
# (review 2) the final look: the eyes alone roll straight up to the toast teetering over the table's edge above them (a head tipped back showed
# only the cap and the top of the squashed head), then one slow blink each, a beat apart
# (review 3) the pupils pinned right up under the brows, the brows raised with them (they read as side glances)
UPF = {'lid': 0.0, 'gy': -1.0, 'gx': 0.0, 'brow': 0.8, 'eye': 0.6, 'low': 0.0}
BLI17 = r(D17 - 1.05); BLH17 = r(D17 - 0.7)
INSK17 = [k(0.0, look='camera'), k(0.0, clip='reclineBack'), k(0.0, toon={**IN17, 'face': {**IF3, 'mouth': 'line', 'lid': 0.4}}, toonDur=0.0),
          k(r(FLIP17[0] - 0.1), toon={'reach': {'R': R5(TAGLIFT, 1, 0.0)}, 'hands': {'R': 'grip'}, 'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.3, 'brow': 0.2}}, toonDur=0.12),
          k(r(FLIP17[1] + 0.05), toon={'reach': {'R': R5(add(TAGLIFT, [0.0, 0.04, 0.06]), 1, 0.0)}, 'hands': {'R': 'grip'}, 'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.45, 'brow': -0.2}}, toonDur=0.1),
          *blink(r(SEC17 + 0.05), {**IF3, 'mouth': 'line', 'lid': 0.45, 'brow': -0.2}, {'reach': {'R': R5(add(TAGLIFT, [0.0, 0.04, 0.06]), 1, 0.0)}, 'hands': {'R': 'grip'}, 'hip': 0}),
          k(r(UP17 - 0.1), toon={'hip': 0, 'face': {**IF3, 'mouth': 'line', 'lid': 0.3}}, toonDur=0.15),
          k(UP17, look='camera', lookDur=0.2), k(UP17, toon={'hip': 0, 'bend': {'neck': [-0.08, 0, 0, 1, None]}, 'face': {**IF3, 'mouth': 'line', **UPF}}, toonDur=0.25),
          *hold_sblink(r(UP17 + 0.3), D17, BLI17, {**IF3, 'mouth': 'line', **UPF}, {'hip': 0, 'bend': {'neck': [-0.08, 0, 0, 1, None]}})]
HK17 = {'reach': {'R': R5(WLAP, 1, 0.0)}, 'hands': {'R': 'grip'}, 'scl': {'head': [1.55, 0.5, 1.18]}, 'bend': {'neck': [0.2, 0, 0, 1, None]}, 'hip': 0}
HF17 = {**SQF, 'lid': 0.75}
HEROK17 = [k(0.0, look='camera'), k(0.0, clip='reclineBack'), k(0.0, toon={**HK17, 'face': HF17}, toonDur=0.0),
           # (review 3) the glance at the tag with the eyes alone, the squashed head kept square to us (a look target tipped it back like a lid)
           k(r(FLIP17[1] - 0.05), look='camera', lookDur=0.12), k(r(FLIP17[1]), toon={**HK17, 'face': {**HF17, 'lid': 0.45, 'gx': 0.6, 'gy': 0.4}}, toonDur=0.1),
           k(r(SEC17 + 0.2), look='camera', lookDur=0.15), k(r(SEC17 + 0.2), toon={**HK17, 'face': HF17}, toonDur=0.1),
           k(r(UP17 + 0.1), look='camera', lookDur=0.2), k(r(UP17 + 0.1), toon={**HK17, 'face': {**HF17, **UPF, 'lid': 0.0, 'low': 0.0, 'eye': 0.85, 'pupilSize': 0.3}}, toonDur=0.25),
           *hold_sblink(r(UP17 + 0.4), D17, BLH17, {**HF17, **UPF, 'lid': 0.0, 'low': 0.0, 'eye': 0.85, 'pupilSize': 0.3}, HK17)]
st.shot('S17', 'kitchenDay', setOpts=KSET, look=LOOKU, actors=[act('inspecteur', IN16B, 0, 'reclineBack', 'neutral', scale=SI, keys=INSK17), act('mecGris', HE16B, 0, 'reclineBack', 'neutral', keys=HEROK17)],
        props=[TABLE('table17', open=[[0.0, 1.0]]), NEARFLOOR(17), *UNDER(17),
               # (review 1) the inspector's tie hidden (it lay across the drawing like a fat needle): the drawn needle deep in the red, clear of twelve
               P('etiq17i', 'ttTag', on={'actor': 'inspecteur', 'joint': 'torso', 'offset': [TAGOFF[0], TAGOFF[1], r(TAGOFF[2] + 0.06)]}, opts={'w': 0.32, 'h': 0.44, 'needle': 15.4, 'backFull': 20, 'cord': [0.1, 0.17, -0.1], 'flip': [[FLIP17[0], 0.0], [FLIP17[1], 1.0]]}), TAG('etiq17h', 'mecGris', needle=6.0),
               WATCH('chrono17', WLAP, at_=0.0, rad=0.1),
               P('assiette17', 'ttPlate', pos=PL17), TOAST('tartine17', TT17, rot=[0.95, 0.2, 0.0], wob=[[r(UP17 - 0.3), 0.22, 8, 0.45]])],
        cams=[C17])
st.cue('sfx:paper', 'S17', FLIP17[0], 0.15); st.cue('sfx:rattleShort', 'S17', r(UP17 - 0.3), 0.08); st.cue('sfx:tick', 'S17', r(D17 - 0.4), 0.15)

# (review 1) the inspector's tie hidden in every shot: it hung over his tag (and over the S17 drawing); the same for the grey hero and the
# seized ministers, whose tags must read
for sc_ in st.scenes:
    for a_ in sc_.get('actors', []):
        if a_['id'] in ('inspecteur', 'mecGris') or (sc_['id'] == 'S12b' and a_['id'] in NAMES7) or (sc_['id'] == 'S15' and a_['id'] in ('agent1', 'agent2')):
            a_['keys'] = [({**kk, 'toon': {**kk['toon'], 'tieHide': 1}} if 'toon' in kk else kk) for kk in a_['keys']]
print('\n'.join(CHECKS))

TOON = {'breathe': 1.7, 'holdLife': 1.6}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': TOON}
GREY = {'suit': '#8A8E96', 'pants': '#7A7E86', 'lapel': '#6E727A', 'shirt': '#F2F2EE', 'tie': '#3E4450', 'cuff': '#8A8E96', 'glasses': False}
for sid in st.SH:
    if not any(s_['id'] == sid for s_ in st.scenes): st.shot(sid, 'whiteVoid', setOpts={'color': '#C9C6B6'}, cams=[cam(0.0, [0, 1.5, 6], [0, 1.5, 6], [0, 1.2, 0], lens=44)])
st.scenes.sort(key=lambda s_: s_['start'])
# (flicker fix) kitchenDay lays its tiles 3 mm over one 300 m floor quad with no offset: on single frames (draft 4: S01 0, 2, 35, S01b, S11, S17)
# the whole floor came out plain beige; every kitchen shot draws the tiles with a polygon offset (ttTileOffset)
for s_ in st.scenes:
    if s_['set'] == 'kitchenDay': s_['props'].append(P('carrelage', 'ttTileOffset'))
st.write("La tartine", rig='toon', fingers=False, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'cons1': {'preset': 'boss', 'seed': 10202, 'suit': '#3E4A5C', 'tie': '#8A2E3A', 'hair': 'bald', 'facial': 'mustache', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'cons2': {'preset': 'femme', 'seed': 10203, 'suit': '#6A3E5E', 'lapel': '#4E2E46', 'hair': 'bun', 'hairColor': '#5A3A28', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'cons3': {'preset': 'politique', 'seed': 10204, 'suit': '#2E4A3A', 'tie': '#C9A55A', 'hairColor': '#9A9A96', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'cons4': {'preset': 'madame', 'seed': 10205, 'suit': '#8E5A3A', 'toon': EX},
    'cons5': {'preset': 'avocat', 'seed': 10206, 'suit': '#4A4E58', 'hair': 'receding', 'hairColor': '#2A2420', 'facial': 'beard', 'glasses': False, 'toon': EX},
    'apere': {'preset': 'pyjama', 'seed': 10207, 'suit': '#E8A94E', 'hair': 'curly', 'hairColor': '#3A2418', 'facial': 'none', 'toon': EX},
    'amere': {'preset': 'femme', 'seed': 10208, 'suit': '#7AB8A8', 'lapel': '#5A9888', 'hair': 'long', 'hairColor': '#8A4A28', 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'bpere': {'preset': 'pyjama', 'seed': 10209, 'suit': '#8EA8D8', 'hair': 'bald', 'facial': 'mustache', 'toon': EX},
    'bmere': {'preset': 'femme', 'seed': 10210, 'suit': '#E8B4C4', 'lapel': '#C894A4', 'hair': 'bun', 'hairColor': '#2A1E18', 'skin': '#8A5A3A', 'faceRim': True, 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'aagent': {'preset': 'boss', 'seed': 10211, **GREY, 'hair': 'slick', 'hairColor': '#2A2420', 'facial': 'none', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'bagent': {'preset': 'boss', 'seed': 10212, **GREY, 'hair': 'curly', 'hairColor': '#4A3A2A', 'facial': 'stubble', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 10213, 'suit': '#23262E', 'lapel': '#16181E', 'tie': '#7A2E3A', 'hairColor': '#D8D2C4', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'ministreA': {'preset': 'politique', 'seed': 10214, 'suit': '#23262E', 'lapel': '#16181E', 'tie': '#2F62B5', 'hairColor': '#5A3A28', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministreB': {'preset': 'politique', 'seed': 10213, 'suit': '#23262E', 'lapel': '#16181E', 'tie': '#7A2E3A', 'hairColor': '#D8D2C4', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'ministreC': {'preset': 'femme', 'seed': 10215, 'suit': '#2A2C34', 'lapel': '#B9BEC6', 'hair': 'bun', 'hairColor': '#9A9A96', 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'mamie': {'preset': 'mamie', 'seed': 10216, 'suit': '#8E5AA8', 'toon': EX},
    'serveur': {'preset': 'serveur', 'seed': 10217, 'toon': EX},
    'agent1': {'preset': 'boss', 'seed': 10218, **GREY, 'hair': 'crew', 'hairColor': '#2A2420', 'facial': 'mustache', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'agent2': {'preset': 'femme', 'seed': 10219, **GREY, 'outfit': 'suit', 'hair': 'bun', 'hairColor': '#3A2A20', 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'agent3': {'preset': 'boss', 'seed': 10220, **GREY, 'hair': 'afro', 'hairColor': '#1E1A18', 'skin': '#6A4430', 'faceRim': True, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    # (stills 3) the lemec preset keeps its navy atlas suit whatever the colour: the charcoal variant takes the grey
    'mecGris': {**MEC, 'preset': 'lemec_charcoal', 'atlas': 'lemec', 'atlasBody': False, **GREY, 'tie': '#3E4450'},
    'inspecteur': {'preset': 'boss', 'seed': 10201, **GREY, 'hat': 'maocap', 'hatColor': '#6E727A', 'hair': 'crew', 'hairColor': '#5A5048', 'facial': 'mustache', 'build': {'width': 1.0, 'headWidth': 1.25, 'belly': 0.06}, 'toon': EX},
})
