#!/usr/bin/env python3
"""Le tonnerre (story 89, cycle 49; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man was woken by the thunder. He filed a complaint for noise nuisance. The thunder was arrested at three thousand metres. Two helicopters
were struck by lightning. In court, the thunder kept silent. It was its right. This man asked for nothing more. The judge insisted. It answered.
The district lost all its windows. The twelve jurors are deaf. Three experts confirmed: it was loud. It was put in a padded cell. In the cell
there already was a mime. The mime asked for a transfer. Out loud. On release, the thunder had no address. House arrest at the victim's home.
It took the window side.
Staging: the thunder is ONE character in every shot: a big black low-poly anvil cumulonimbus (flat wide top, puffy charcoal body), a lighter box
face plate (white eyes, thick black brows, a mouth that opens on a glowing yellow inside), small yellow zigzag bolt arms; it never rains. Night,
his bedroom: asleep in pyjamas and nightcap on the door side of a double bed, the window flashes white, the cloud's angry face fills the window
outside and roars; he jolts bolt upright, his nightcap flies off; close on the window: the face scowls in at him. A front desk at night (ACCUEIL):
in pyjamas he points up at the night window while a policeman types with one finger. High above a tiny town: two helicopters circle the cloud,
masked men slide down their ropes, its bolt arms swing together and oversized steel handcuffs snap shut on them (INTERPELLÉ). A bolt forks out of
its belly into both helicopters: they go black and smoking and spin gently down; in a field the two blackened helicopters smoke while their
sooty crews, hair on end, salute (nobody hurt). The courtroom: the cloud squeezed into the dock between two small gendarmes, its mouth pressed
tight shut, cheeks puffed. Its lawyer lays a hand on it and nods gravely to the judge. On the public bench, the man sleeps, smiling. The judge
leans over his bench, bangs the gavel and points. The cloud opens its mouth: a white flash and shockwave rings blast toward us, the man jolts
awake behind it; the judge's wig and papers fly. Outside, every window of the buildings round the court pops out at once and drops onto the
empty pavement in shards. The jury: twelve jurors on three tiers sit perfectly still and dignified while plaster dust falls, hair blown back;
one calmly turns a page. Three experts in white coats hold up a sound-level meter whose needle has bent through its case, and nod together.
Guards squeeze the cloud through the narrow door of an all-white quilted padded cell (COUPABLE). Inside, in the corner, a box-headed mime (white
face, striped shirt, beret) mimes an invisible wall, then gives a small wave. At the door hatch the mime points at the cloud, mimes packing a
suitcase and walking away while the guard watches blankly through the hatch. Close on the hatch: the mime shouts, mouth enormous, the guard's
cap flies off. Prison gate by day: the cloud floats outside with a tiny bundle; the clerk shows it an empty register (ADRESSE) and shrugs. Two
gendarmes walk the cloud, an electronic tag blinking on its bolt arm, up his garden path; he opens the door in pyjamas (ASSIGNÉ). Night, the
double bed: the cloud tucked under the duvet on the window side, eyes open and calm; the man on the door side, wide awake, staring at the
ceiling. No rumbling, no snoring, no rain.
Natural look; cycle 49: props_tonnerre.js (thunderCloud, shockRing, boltStrike, tonBedroom, popFacade, juryTiers, pageBook, soundMeter,
paddedCell, prisonGate, emptyRegister, mimeBeret, plasterFall, sootSmoke, frontCounter); helicopter (props_lunettes), rope, dockBox (props_table),
balaclava (props_rambarde), kepi (props_conseiller), nightCap (props_interrupteur), nightWindow (props_porte), typewriter, courtFront
(props_feuille), sootPatches (props_barbecue), wig, flyingPaper (props_eternuement), gavel, soundBlock, bench (props.js) reused; sets courtroom,
office, aerialSuburb, grassland, parisStreet, pavillon, whiteVoid.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.83) and heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() before stills; two faces
in a V; nobody shown hurt (the crews salute, the pavement is empty); one flash per shot at most; no English, no real insignia or brands."""
from story_kit import *
import math

st = Story('tonnerre', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
def loc(p, ry, lx, lz, y=0.0):
    """a point in the frame of a prop at p turned ry degrees (local +X, +Z), y up"""
    a = math.radians(ry); return [r(p[0] + lx * math.cos(a) + lz * math.sin(a)), r(p[1] + y), r(p[2] - lx * math.sin(a) + lz * math.cos(a))]
CHECKS = []
def chk(sid, c, pts):
    CHECKS.append(f"{sid}: lens {c['lens']} | " + ' | '.join(f"{n} {project(c['from'], c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
def FIT(t, frm, pts, top=0.1, bottom=0.75, lenses=range(28, 61), drift=(0, 0, 0), margin=0.06, inside=None, most=4.0):
    f0 = list(frm); frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, margin=margin, inside=inside, most=most)
    if lens is None: frm = f0; look, lens, _ = fit(f0, pts, top=top, bottom=bottom, lenses=lenses, margin=margin); print(f'  WARNING no lens fits at {frm} (kept)'); lens = lens or max(lenses)
    if lens > max(lenses): print(f'  WARNING lens {lens} at {frm}')
    return cam(t, list(frm), add(frm, drift), look, add(look, drift), lens=lens)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.45, 'mouth': 'line'}
NIGHT = {'sun': 0.35, 'sunColor': '#A9BCEB', 'fill': 0.6, 'exposure': 0.78}
# (pass 2) the cloud's charcoal brought back to neutral per set: the courtroom's warm light made it brown, the night and the blue sky navy
T_COURT = {'tint': '#BED9DD', 'emis': '#19191C'}; T_NIGHT = {'tint': '#F2DCC0', 'emis': '#08080A'}; T_DAY = {'tint': '#F6DCC4', 'emis': '#040404'}
# (final pass) the prison gate's daylight still read brown: a cool tint for S17 alone
T_GATE = {'tint': '#DBDCDE', 'emis': '#151517'}
def CLOUD(pid, pos, ry=0, s=1.0, keys=None, **o):
    d = P(pid, 'thunderCloud', pos=pos, ry=ry, opts={'s': s, **o})
    if keys: d['keys'] = keys
    return d
def CFACE(pos, ry, s):
    """the middle of the cloud's face plate (in the world)"""
    return loc(pos, ry, 0.0, 0.67 * s, 0.82 * s)
CAP = lambda pid, who='mec': P(pid, 'nightCap', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'side': -1})
KEPI = lambda pid, who: P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#1F2A44', 'band': '#1F2A44'})
BALA = lambda pid, who: P(pid, 'balaclava', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
SOOT = lambda pid, who: P(pid, 'sootPatches', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
def blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]

for g_ in [('S01', 0.75, 'mec', 'jolt'), ('S09', 0.2, 'mec', 'blast'), ('S13', 1.0, 'mec', 'squeeze'), ('S16', 0.35, 'mime', 'shout'), ('S19', 1.4, 'mec', 'awake')]:
    st.gag(*g_)

# ---- the bedroom (S01, S19): tonBedroom at the origin; the bed's middle at x 0 against the back wall (z -3); window on the left (x -1.45), door right
WINC = [-1.15, 1.72, -3.0]                            # the middle of the window
BEDTOP = 0.63
HEAD_PILLOW_Z = -2.6

# 1: woken by the thunder. Night: asleep on his back on the door side of the bed, nightcap on, a smile; the window flashes white and the cloud's
#    angry face, huge outside, roars into it; he jolts bolt upright (lying -> sitting in two frames), eyes out, hair on end, the nightcap flies
#    off and lands on the duvet. (b) Close on the window: the face scowls in at him
D1 = st.dur('S01'); FL1 = 0.6; JOLT1 = 0.74; CUT1 = 1.4
INBED = [0.45, BEDTOP, -1.68]; SIT1 = [0.45, 0.2, -1.68]
CA1P = [1.85, 2.35, 1.3]
CA1 = FIT(0.0, CA1P, {'headLie': [0.45, 0.85, -2.6], 'headUp': [0.45, 2.45, -1.68], 'winTL': [-1.65, 2.35, -3.0], 'winBL': [-1.65, 1.1, -3.0], 'foot': [0.95, 0.85, -0.85]}, top=0.1, bottom=0.74, drift=(-0.1, 0.0, -0.15))
# the cloud outside: its face on the line from camera A through the middle of the window, 3.8 m behind the wall
_d = [WINC[i] - CA1P[i] for i in range(3)]; _t = (WINC[2] - 3.8 - CA1P[2]) / _d[2]; FACE1 = [r(CA1P[i] + _d[i] * _t) for i in range(3)]
S1 = 1.55; RY1 = yaw(FACE1, CA1P); CL1 = [r(FACE1[0] - 0.67 * S1 * math.sin(math.radians(RY1))), r(FACE1[1] - 0.82 * S1), r(FACE1[2] - 0.67 * S1 * math.cos(math.radians(RY1)))]
_u = [WINC[i] - FACE1[i] for i in range(3)]; CB1P = [r(WINC[i] + 0.62 * _u[i]) for i in range(3)]
CB1 = cam(CUT1, CB1P, add(CB1P, [0.06, 0.0, 0.1]), FACE1, FACE1, lens=40)
chk('S01a', CA1, {'headLie': [0.45, 0.85, -2.6], 'headUp': [0.45, 2.1, -1.68], 'win': WINC, 'cloudFace': FACE1, 'foot': [0.95, 0.85, -0.85]})
chk('S01b', CB1, {'win': WINC, 'winT': [-1.45, 2.32, -3.0], 'winB': [-1.45, 1.15, -3.0], 'face': FACE1, 'faceL': add(FACE1, [-0.7, 0, 0]), 'anvil': add(CL1, [0, 1.72 * S1, 0])})
# (pass 2) the cap leaves on an arc: up and out to his left (away from his face), then down onto the duvet by the foot, lying on its side
CAPFLY1 = [k(0.0, visible=False), k(r(JOLT1 + 0.04), visible=True), k(r(JOLT1 + 0.04), to=[0.95, 2.95, -1.45], dur=0.2, ease='out'), k(r(JOLT1 + 0.24), to=[1.15, 0.97, -1.0], dur=0.3, ease='in'),
           k(r(JOLT1 + 0.04), rotTo=[1.5, 0.9, 1.7], dur=0.5, ease='out')]
st.shot('S01', 'whiteVoid', look=NIGHT, actors=[
        act('mec', INBED, 0, 'lieBack', 'sleepy', blink=0, keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 1, 'mouth': 'smile'}, 'bend': {'neck': [0.45, 0, 0, 1, None]}}, toonDur=0.0),
            k(r(FL1 + 0.04), toon={'face': {'lid': 1, 'mouth': 'clench', 'brow': -0.6}, 'bend': {'neck': [0.45, 0, 0, 1, None]}}, toonDur=0.04),
            k(JOLT1, to=SIT1, dur=0.07, glide=True, face=0, clip='sit', then='sit', blend=0.05),
            k(JOLT1, toon={'face': {'lid': 0, 'pop': 0.55, 'mouth': 'O', 'brow': 0.9}, 'hairUp': 1.4, 'sq': [0.9, 1.14, 0.9], 'auto': 0}, toonDur=0.05),
            k(r(JOLT1 + 0.12), toon={'face': {'lid': 0, 'pop': 0.6, 'mouth': 'O', 'brow': 1.0}, 'hairUp': 1.5, 'sq': [0.92, 1.1, 0.92], 'auto': 0}, toonDur=0.08),
            k(r(JOLT1 + 0.6), toon={'face': {'lid': 0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.6}, 'hairUp': 1.0, 'sq': [1, 1, 1], 'auto': 0}, toonDur=0.06),
            k(r(JOLT1 + 0.5), look=[WINC[0] + 0.5, 1.7, -2.4], lookDur=0.12)])],
        props=[P('chambre1', 'tonBedroom', pos=[0, 0, 0], opts={'winX': WINC[0], 'flash': [[FL1, 0.22]], 'skyZ': -12.5, 'feet': [[0.45, -0.8, 0.24]]}),
               CLOUD('nuage1', CL1, RY1, S1, keys=[k(CUT1, to=[r(CL1[i] + (CB1P[i] - CL1[i]) * 0.18) for i in range(3)], dur=0.6, ease='inOut')], mouth=[[r(CUT1 + 0.2), 0.0], [r(CUT1 + 0.3), 0.35], [r(CUT1 + 0.6), 0.12]], sq=[[0.0, 1, 1, 1], [r(CUT1 + 0.25), 1.06, 0.95, 1.0], [r(CUT1 + 0.5), 1, 1, 1]], expr=[[0.0, 'angry'], [r(FL1 - 0.04), 'shout'], [r(FL1 + 0.32), 'angry']], flash=[[FL1, 0.25]], glow=0.6, look=[[0.0, 0.0, 0.0], [1.0, 0.7, 0.3]], arms=[[0.0, 'up', 'up']], **T_NIGHT),
               P('bonnet1', 'nightCap', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'side': -1}, keys=[k(0.0, visible=True), k(r(JOLT1 + 0.06), visible=False)]),
               P('bonnet1v', 'nightCap', pos=[0.45, 2.3, -1.68], opts={'side': -1}, keys=CAPFLY1)],
        fx=[{'type': 'flash', 'at': FL1, 'dur': 0.12}, {'type': 'shake', 'at': FL1, 'dur': 0.25, 'amount': 0.012}],
        cams=[CA1, CB1])
st.cue('thunder', 'S01', FL1, 0.8); st.cue('sfx:gasp', 'S01', JOLT1, 0.35); st.cue('sfx:boing', 'S01', r(JOLT1 + 0.05), 0.15)

# 2: he filed a complaint for noise. A front desk by night (ACCUEIL), the night window behind it with the moon: in pyjamas and nightcap he stands
#    at the counter, three quarters to us, and stabs his finger up at the window again and again; behind the counter the policeman types on a
#    typewriter with one finger, bored, without looking up
D2 = st.dur('S02'); BACK2 = -3.6
CNT2 = [-0.7, 0, -1.7]; COP2 = [-1.0, 0, -2.4]; HERO2 = [0.3, 0, -1.0]; RYH2 = -35
TW2 = [-1.05, 1.16, -1.85]
WIN2 = [-1.75, 1.79, BACK2 + 0.04]
SH2 = off(HERO2, RYH2, 0.0, 0.24, 1.66)
def PT2(dy):
    """his right hand pointing up toward the window: 0.62 m from the shoulder"""
    v = [WIN2[0] - SH2[0], WIN2[1] + 0.9 + dy - SH2[1], WIN2[2] - SH2[2]]; n = math.sqrt(sum(x * x for x in v)); return [r(SH2[i] + v[i] / n * 0.62) for i in range(3)]
C2 = cam(0.0, [0.25, 1.7, 2.8], [0.15, 1.7, 2.55], [-0.25, 1.72, -1.6], [-0.25, 1.72, -1.6], lens=50)
chk('S02', C2, {'heroFace': [HERO2[0], 2.05, HERO2[2]], 'copFace': [COP2[0], 2.05, COP2[2]], 'win': WIN2, 'tw': TW2, 'hand': PT2(0)})
def TYPE2(t, down, x=0.0):
    hp = add(TW2, [0.05 + x, 0.36 if not down else 0.14, 0.14])
    return k(t, toon={'reach': {'R': [*hp, 1, 0.15]}, 'hands': {'R': 'point'}, 'bend': {'spine': [0.18, 0, 0, 1, None], 'neck': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.7, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.06 if down else 0.08, toonEase='in' if down else 'out')
def JAB2(t, dy, face):
    # (pass 1) each jab overshoots (the arm shoots past, 0.1 further) and settles back: a stab, not a drift
    return [k(t, toon={'reach': {'R': [*PT2(dy + 0.12), 1, 0.15]}, 'hands': {'R': 'point'}, 'face': face, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.06, toonEase='out'),
            k(r(t + 0.08), toon={'reach': {'R': [*PT2(dy - 0.06), 1, 0.15]}, 'hands': {'R': 'point'}, 'face': face, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.1, toonEase='inOut')]
st.shot('S02', 'office', setOpts={'door': False, 'printer': False, 'carpet': False, 'picture': False, 'wall': '#B9C4CE', 'band': '#5E6E80', 'trim': '#2E3A46'}, look={'exposure': 1.15, 'fill': 0.9},
        actors=[act('mec', HERO2, RYH2, 'stand', 'angry', keys=[k(0.0, look=[WIN2[0] + 0.6, 2.2, WIN2[2] + 1.0]),
                    *JAB2(0.0, 0.0, {'lid': 0.1, 'mouth': 'open', 'brow': -0.8}), *JAB2(0.32, 0.18, {'lid': 0.1, 'mouth': 'O', 'brow': -0.9}), *JAB2(0.62, 0.0, {'lid': 0.1, 'mouth': 'open', 'brow': -0.8}),
                    *JAB2(0.92, 0.2, {'lid': 0.1, 'mouth': 'O', 'brow': -0.9}), k(1.15, look='camera', lookDur=0.15), *JAB2(1.25, 0.05, {'lid': 0.2, 'mouth': 'open', 'brow': -0.9}), *JAB2(1.6, 0.22, {'lid': 0.2, 'mouth': 'O', 'brow': -1.0})]),
                act('flic', COP2, 0, 'stand', 'unimpressed', keys=[k(0.0, look=add(TW2, [0, 0.1, 0.1])), *[TYPE2(r(0.1 + 0.15 * i), i % 2 == 1, 0.04 * ((i // 2) % 3 - 1)) for i in range(14)]])],
        props=[P('comptoir2', 'frontCounter', pos=CNT2, opts={'sign': 'ACCUEIL', 'signY': 2.65}), P('fenetre2', 'nightWindow', pos=WIN2, opts={'w': 1.3, 'h': 1.3}),
               P('machine2', 'typewriter', pos=TW2, opts={'hitFrom': 0.15, 'hitTo': 2.2}), CAP('bonnet2')],
        cams=[C2])
for i in range(6): st.cue('sfx:tick', 'S02', r(0.17 + 0.36 * i), 0.18)
st.cue('sfx:grunt', 'S02', 0.35, 0.15)

# 3: arrested at three thousand metres. High over a tiny town far below: the black cloud in the middle of the sky, two helicopters hovering at
#    its sides, ropes hanging; two masked men slide down the ropes beside it; (b) closer: its bolt arms are swung together in front of it and two
#    oversized steel handcuffs snap shut on them, a masked man at the rope beside them; its face furious (INTERPELLÉ)
D3 = st.dur('S03'); CUFF3 = 1.25; CUT3 = 1.0
ALT = 120.0
CL3 = [0.0, ALT, 0.0]; S3 = 3.4
HE3 = [(-5.4, ALT + 7.2, 4.5, 70), (5.6, ALT + 7.6, 3.5, -105)]
ROPE3 = [(-4.4, ALT + 6.4, 4.6), (4.6, ALT + 6.8, 3.6)]
SL3 = [('forces1', ROPE3[0], 0.05), ('forces2', ROPE3[1], 0.2)]
def slide3(who, rp, d_, stop):
    x_, ytop, z_ = rp
    hold = lambda y: {'reach': {'L': [x_, r(y + 2.55), z_ + 0.12, 1, 0.03], 'R': [x_, r(y + 2.3), z_ + 0.12, 1, 0.03]}, 'hands': {'L': 'grip', 'R': 'grip'},
                      'bend': {'legL': [-0.3, 0.1, 0, 1, None], 'legR': [-0.2, -0.1, 0, 1, None], 'shinL': [0.5, 0, 0, 1, None], 'shinR': [0.4, 0, 0, 1, None]}, 'auto': 0}
    return act(who, [x_, r(ytop - 2.7), z_ - 0.1], 0, 'stand', 'determined', keys=[k(0.0, look='camera'), k(0.0, toon=hold(ytop - 2.7), toonDur=0.0),
               k(d_, to=[x_, stop, z_ - 0.1], dur=0.8, ease='out', glide=True, face='keep'), k(d_, toon=hold(stop), toonDur=0.8, toonEase='out')])
CA3 = cam(0.0, [2.0, ALT + 3.0, 30.0], [1.6, ALT + 3.2, 28.6], [0.3, ALT + 3.4, 2.0], [0.3, ALT + 3.5, 2.0], lens=50)
FACE3 = CFACE(CL3, 0, S3)
CB3P = [3.2, ALT + 2.2, 9.5]
CB3 = cam(CUT3, CB3P, add(CB3P, [-0.3, 0.05, -0.6]), [0.0, ALT + 1.9, 1.5], [0.0, ALT + 1.95, 1.5], lens=50)
chk('S03a', CA3, {'face': FACE3, 'base': CL3, 'h1': HE3[0][:3], 'h2': HE3[1][:3], 'f1stop': [ROPE3[0][0], ALT + 2.5, ROPE3[0][2]]})
chk('S03b', CB3, {'face': FACE3, 'faceTop': add(FACE3, [0, 0.4 * S3, 0]), 'cuffs': add(CL3, [0, 1.5, 2.2]), 'f2': [ROPE3[1][0], ALT + 4.4, ROPE3[1][2]], 'f2feet': [ROPE3[1][0], ALT + 2.2, ROPE3[1][2]]})
st.shot('S03', 'aerialSuburb', setOpts={'z0': -800, 'x': 500}, actors=[slide3('forces1', ROPE3[0], 0.05, r(ALT + 2.4)), slide3('forces2', ROPE3[1], 0.2, r(ALT + 2.1))],
        props=[CLOUD('nuage3', CL3, 0, S3, expr=[[0.0, 'angry'], [r(CUFF3 + 0.05), 'clench']], shadows=False, strain=[[0.0, 0.0], [r(CUFF3 + 0.05), 1.0], [r(CUFF3 + 0.5), 0.4]], arms=[[0.0, 'out', 'out'], [r(CUFF3 - 0.22), 'cuff', 'cuff']], cuffs=True, cuffsAt=CUFF3, look=[[0.0, -0.5, 0.0], [0.8, 0.5, 0.2]], seed=3),
               *[P(f'heli3{j}', 'helicopter', pos=[x_, y_, z_], ry=a_, scale=0.85, opts={'spin': 5, 'color': '#3E4A5C', 'bladeOpacity': 0.55}, keys=[k(0.0, to=[x_ + 0.6 * (1 - 2 * j), y_ + 0.3, z_ - 0.8], dur=D3, ease='linear')]) for j, (x_, y_, z_, a_) in enumerate(HE3)],
               *[P(f'corde3{j}', 'rope', pos=list(rp), opts={'len': 6.8, 'seed': j, 'sway': 0.02, 'r': 0.04}) for j, rp in enumerate(ROPE3)],
               BALA('bala3a', 'forces1'), BALA('bala3b', 'forces2')],
        cams=[CA3, CB3])
st.card('S03', 'INTERPELLÉ', at=r(CUFF3 + 0.12))
st.cue('sfx:rotor', 'S03', 0.0, 0.35); st.cue('sfx:slideDown', 'S03', 0.05, 0.15); st.cue('sfx:slideDown', 'S03', 0.2, 0.15); st.cue('sfx:cuff', 'S03', CUFF3, 0.6); st.cue('clack', 'S03', r(CUFF3 + 0.02), 0.4)

# 4: two helicopters were struck. Up there, wider: a bolt forks out of the cloud's belly into both helicopters (one white flash): they turn black,
#    smoke, and spin gently down; (b) a field: the two blackened helicopters sit on the grass smoking, rotors winding down, their sooty crews in
#    front of them, hair on end, saluting; nobody hurt
D4 = st.dur('S04'); HIT4 = 0.28; CUT4 = 0.95
CL4 = [0.0, 60.0, 0.0]; S4 = 2.6
HE4 = [(-3.2, 60.3, 3.2, 70), (3.3, 60.8, 2.8, -105)]
# (pass 2) tighter: the struck helicopters big enough to read as they fall
CA4 = cam(0.0, [1.0, 60.6, 18.5], [0.95, 60.5, 18.0], [0.1, 59.6, 2.0], [0.1, 59.3, 2.0], lens=50)
def heli_fall(j, x_, y_, z_, a_):
    """the struck helicopter, black: hidden until the hit, then it sinks slowly while it turns"""
    return P(f'helinoir4{j}', 'helicopter', pos=[x_, y_, z_], ry=a_, scale=0.88, opts={'spin': 1.5, 'color': '#26272B'},
             keys=[k(0.0, visible=False), k(HIT4, visible=True), k(r(HIT4 + 0.05), to=[x_ * 1.08, y_ - 3.6, z_ + 0.5], dur=r(CUT4 - HIT4), ease='inOut'), k(r(HIT4 + 0.05), rotTo=[0.25 * (1 - 2 * j), math.radians(a_) + 3.6 * (1 - 2 * j), 0.3 * (1 - 2 * j)], dur=r(CUT4 - HIT4), ease='inOut')])
FIELD4 = [(-2.0, -3.2, 100, 0.12), (2.1, -3.8, -75, -0.1)]   # x, z, ry, tilt of the landed helicopters
CREW4 = [('pilote1', [-0.85, 0, 0.35], 12), ('pilote2', [0.1, 0, 0.6], -3), ('pilote3', [1.0, 0, 0.3], -14)]
CB4P = [0.15, 1.6, 7.0]
CB4 = cam(CUT4, CB4P, add(CB4P, [0, -0.05, -0.4]), [0.1, 1.5, -1.5], [0.1, 1.5, -1.5], lens=46)
chk('S04a', CA4, {'face': CFACE(CL4, 0, S4), 'h1': HE4[0][:3], 'h2': HE4[1][:3], 'h1low': [HE4[0][0], HE4[0][1] - 3, HE4[0][2]]})
chk('S04b', CB4, {**{w: [p[0], 2.05, p[2]] for w, p, _ in CREW4}, 'feet1': CREW4[0][1], 'heli1': [-2.6, 1.5, -2.2], 'heli2': [2.9, 1.5, -3.4]})
SAL = lambda p, ry: [*off(p, ry, 0.12, 0.26, 2.06), 1, 0.03]
st.shot('S04', 'grassland', setOpts={'clouds': 26, 'grass': '#86BE5C'}, actors=[
        *[act(w, p, a_, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, visible=False), k(CUT4, visible=True),
            k(CUT4, toon={'reach': {'R': SAL(p, a_)}, 'hands': {'R': 'open'}, 'hairUp': 1.3, 'face': {'lid': 0.15, 'eye': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
            k(r(CUT4 + 0.35 + 0.08 * j), toon={'reach': {'R': SAL(p, a_)}, 'hands': {'R': 'open'}, 'hairUp': 1.3, 'face': {'lid': 1.0, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.04),
            k(r(CUT4 + 0.45 + 0.08 * j), toon={'reach': {'R': SAL(p, a_)}, 'hands': {'R': 'open'}, 'hairUp': 1.3, 'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.15, 'eye': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.06)])
          for j, (w, p, a_) in enumerate(CREW4)]],
        props=[CLOUD('nuage4', CL4, 0, S4, expr=[[0.0, 'angry'], [r(HIT4 - 0.05), 'shout'], [r(HIT4 + 0.3), 'smug']], arms=[[0.0, 'cuff', 'cuff']], cuffs=True, flash=[[HIT4, 0.3]], flashK=0.0, seed=3, shadows=False),
               *[P(f'heli4{j}', 'helicopter', pos=[x_, y_, z_], ry=a_, scale=0.88, opts={'spin': 5, 'color': '#3E4A5C', 'bladeOpacity': 0.55}, keys=[k(0.0, visible=True), k(HIT4, visible=False)]) for j, (x_, y_, z_, a_) in enumerate(HE4)],
               *[heli_fall(j, *h) for j, h in enumerate(HE4)],
               *[P(f'eclair4{j}', 'boltStrike', pos=[0, 0, 0], opts={'from': add(CL4, [1.0 * (2 * j - 1), 0.4, 1.1]), 'to': [x_, y_ - 0.2, z_], 'at': HIT4, 'dur': 0.36, 'w': 0.18, 'jag': 0.6, 'span': 0.6, 'n': 7, 'seed': 4 + j}) for j, (x_, y_, z_, _) in enumerate(HE4)],
               *[P(f'fumee4{j}', 'sootSmoke', pos=[x_, y_ + 0.6, z_], opts={'at': HIT4, 'rise': 4.5, 's0': 1.0, 's1': 3.0, 'speed': 0.9}, keys=[k(r(HIT4 + 0.05), to=[x_ * 1.08, y_ - 3.0, z_ + 0.5], dur=r(CUT4 - HIT4), ease='inOut')]) for j, (x_, y_, z_, _) in enumerate(HE4)],
               *[P(f'helisol4{j}', 'helicopter', pos=[x_, 0.82, z_], ry=a_, rot=[0, 0, tl], scale=0.6, opts={'spin': 0.3, 'color': '#232428', 'discOpacity': 0.0}) for j, (x_, z_, a_, tl) in enumerate(FIELD4)],
               *[P(f'fumees4{j}', 'sootSmoke', pos=[x_, 1.6, z_], opts={'rise': 3.0, 's0': 0.5, 's1': 1.8, 'speed': 0.5}) for j, (x_, z_, a_, tl) in enumerate(FIELD4)],
               *[SOOT(f'suie4{j}', w) for j, (w, _, _) in enumerate(CREW4)]],
        fx=[{'type': 'flash', 'at': HIT4, 'dur': 0.14}, {'type': 'shake', 'at': HIT4, 'dur': 0.3, 'amount': 0.015}],
        cams=[CA4, CB4])
st.cue('thunder', 'S04', HIT4, 0.85); st.cue('sfx:rotor', 'S04', 0.0, 0.3); st.cue('sfx:slideDownSlow', 'S04', r(HIT4 + 0.1), 0.25); st.cue('sfx:poof', 'S04', CUT4, 0.25)

# ---- the courtroom: the judge's bench at the back (z -3.4, the judge at 0, 0.3, -4.35), the dock at the front left facing the judge, the public
#      bench behind it, the jury on the right; the cloud in the dock faces the judge (-Z): most courtroom cameras stand on the judge's side
DOCK = [-1.5, 0, 1.3]; SD = 1.2; CLD = [-1.5, 0.1, 1.25]; RYD = 180
SQD = [0.84, 1.1, 0.92]
FACED = CFACE(CLD, RYD, SD)
GEND = [('gend1', [-2.45, 0, 0.5], 170), ('gend2', [-0.55, 0, 0.5], 190)]
PUB = [0.9, 0, 3.0]                                  # the public bench (the man sleeps on it), facing the judge
JUDGE = [0.0, 0.3, -4.35]
COURT = {'sign': 'TRIBUNAL'}
def DOCKBOX(pid): return P(pid, 'dockBox', pos=DOCK, ry=180, opts={'w': 1.7, 'd': 1.05, 'h': 0.95})
def PUBBENCH(pid): return P(pid, 'dockBox', pos=add(PUB, [0, 0, 0.45]), opts={'w': 2.6, 'd': 0.5, 'h': 0.45, 'color': '#6E4A2E'})
def gend_actors(extra=None):
    return [act(w, p, a_, 'stand', 'determined', scale=0.88, keys=[k(0.0, look='camera'), *((extra or {}).get(w, []))]) for w, p, a_ in GEND]
def GKEPIS(sid): return [KEPI(f'kepi{sid}{j}', w) for j, (w, _, _) in enumerate(GEND)]
def SLEEPER(keys=None, sid=''):
    return act('mec', PUB, 180, 'sit', 'sleepy', keys=keys or [k(0.0, look=None), k(0.0, toon={'face': {'lid': 1, 'mouth': 'smile'}, 'bend': {'neck': [0.25, 0.3, 0, 1, None]}}, toonDur=0.0)])

# 5: in court, the thunder kept silent. From the judge's side: the cloud squeezed into the dock, bulging over its rails, between two small
#    gendarmes; its mouth pressed tight shut, cheeks puffed, eyes sliding from side to side; the handcuffs still on; the public bench behind it
#    (b) closer on the pressed mouth: the cheeks puff once more, the brows knit
D5 = st.dur('S05'); CUT5 = 1.35
CA5 = cam(0.0, [-1.45, 2.0, -3.3], [-1.42, 1.94, -2.65], [-1.45, 1.35, 1.0], [-1.45, 1.38, 1.0], lens=64)   # (pass 2) a slow push
CB5P = add(FACED, [0.55, 0.15, -2.3])
CB5 = cam(CUT5, CB5P, add(CB5P, [0.05, 0.0, 0.25]), FACED, add(FACED, [0, 0.02, 0]), lens=40)
chk('S05a', CA5, {'face': FACED, 'g1': [-2.75, 2.0, 1.15], 'g2': [-0.22, 2.0, 1.15], 'pubHead': [PUB[0], 1.65, PUB[2]]})
chk('S05b', CB5, {'face': FACED, 'faceTop': add(FACED, [0, 0.45, 0]), 'mouth': add(FACED, [0, -0.2 * SD, 0]), 'g2': [-0.22, 2.0, 1.15]})
st.shot('S05', 'courtroom', setOpts=COURT, actors=[*gend_actors({'gend2': [k(0.6, look=FACED, lookDur=0.2), k(1.1, look='camera', lookDur=0.15)], 'gend1': [k(0.85, look=FACED, lookDur=0.2), k(1.25, look='camera', lookDur=0.15)]}), SLEEPER()],
        props=[DOCKBOX('box5'), PUBBENCH('banc5'), *GKEPIS('5'), CAP('bonnet5'),
               CLOUD('nuage5', CLD, RYD, SD, expr=[[0.0, 'shut']], sq=[[0.0, *SQD], [0.45, 0.97, 0.97, 1.0], [0.62, 0.95, 0.99, 1.0], [0.85, *SQD], [1.65, 1.0, 0.95, 1.02], [1.85, 0.97, 0.98, 1.0], [2.1, *SQD]], arms=[[0.0, 'cuffLow', 'cuffLow']], cuffs=True,
                     look=[[0.0, -0.8, 0.0], [0.55, 0.8, 0.0], [1.1, -0.8, 0.1], [1.7, 0.0, -0.3]], seed=5, strain=[[0.0, 0.5], [0.45, 1.0], [0.85, 0.4], [1.6, 1.0], [2.1, 0.6]], **T_COURT)],
        cams=[CA5, CB5])
st.cue('sfx:crickets', 'S05', 0.0, 0.08); st.cue('sfx:squeak', 'S05', 0.55, 0.12)

# 6: it was its right. The lawyer (black robe, box head) beside the dock lays a hand on the cloud and nods gravely toward the judge; the cloud's
#    eyes go to the hand, then to us
D6 = st.dur('S06')
# (pass 2) the lawyer in front of the anvil (his head clipped into it), his left hand flat on the cloud's cheek at the edge of the plate
LAW6 = [-0.2, 0, -0.2]; RYL6 = 205
HAND6 = [-1.2, 1.04, 0.29]
C6 = cam(0.0, [0.05, 1.75, -2.6], [0.01, 1.75, -2.4], [-0.9, 1.4, 0.6], [-0.9, 1.4, 0.6], lens=54)
chk('S06', C6, {'lawFace': [LAW6[0], 2.05, LAW6[2]], 'face': FACED, 'hand': HAND6, 'faceL': add(FACED, [-0.4, 0, 0]), 'anvilTop': add(CLD, [0, 2.0, 0])})
def NOD6(t, a, hp=None): return k(t, toon={'reach': {'L': [*(hp or HAND6), 1, 0.1]}, 'hands': {'L': 'open'}, 'hose': 0.05, 'bend': {'neck': [a, 0, 0, 1, None], 'spine': [0.06 + a * 0.2, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.12)
st.shot('S06', 'courtroom', setOpts=COURT, actors=[act('avocat', LAW6, RYL6, 'stand', 'neutral', keys=[k(0.0, look=[0.4, 2.0, -3.5]), NOD6(0.0, 0.0, off(LAW6, RYL6, 0.25, -0.3, 1.0)), NOD6(0.1, 0.0, add(HAND6, [0.12, 0.12, -0.2])), NOD6(0.24, 0.0), NOD6(0.42, 0.38), NOD6(0.6, 0.05), NOD6(0.76, 0.4), NOD6(0.95, 0.1)]), *gend_actors()[:1]],
        props=[DOCKBOX('box6'), *GKEPIS('6')[:1], CLOUD('nuage6', CLD, RYD, SD, expr=[[0.0, 'tight'], [0.6, 'flat']], sq=[[0.0, *SQD]], arms=[[0.0, 'cuff', 'cuff']], cuffs=True, look=[[0.0, 0.0, 0.0], [0.24, -0.9, 0.7], [0.68, 0.0, 0.0]], seed=5, **T_COURT)],
        cams=[C6])
st.cue('sfx:paper', 'S06', 0.1, 0.12)

# 7: this man asked for nothing more. On the public bench, the man in pyjamas and nightcap sleeps peacefully, head on his shoulder, smiling; the
#    pompom of his cap sways as his head nods lower
D7 = st.dur('S07')
C7P = [PUB[0] - 0.35, 1.55, 0.75]
C7 = cam(0.0, C7P, add(C7P, [0.05, -0.02, 0.3]), [PUB[0] - 0.12, 1.45, PUB[2]], [PUB[0] - 0.12, 1.45, PUB[2]], lens=50)
chk('S07', C7, {'face': [PUB[0], 1.65, PUB[2]], 'cap': [PUB[0], 2.05, PUB[2]], 'knees': [PUB[0], 0.5, PUB[2] - 0.5]})
st.shot('S07', 'courtroom', setOpts=COURT, actors=[SLEEPER([k(0.0, look=None), k(0.0, toon={'face': {'lid': 1, 'mouth': 'smile'}, 'bend': {'neck': [0.15, 0.2, 0, 1, None]}}, toonDur=0.0),
            k(0.45, toon={'face': {'lid': 1, 'mouth': 'bigsmile', 'cheeks': 0.4}, 'sq': [1.03, 0.98, 1.05], 'bend': {'neck': [0.3, 0.32, 0, 1, None]}}, toonDur=0.45, toonEase='inOut'),
            k(0.95, toon={'face': {'lid': 1, 'mouth': 'smile', 'cheeks': 0.3}, 'sq': [0.99, 1.01, 0.98], 'bend': {'neck': [0.42, 0.4, 0, 1, None]}}, toonDur=0.45, toonEase='inOut'),
            k(1.4, toon={'face': {'lid': 1, 'mouth': 'bigsmile', 'cheeks': 0.4}, 'sq': [1.03, 0.98, 1.05], 'bend': {'neck': [0.55, 0.46, 0, 1, None]}}, toonDur=0.32, toonEase='inOut')])],
        props=[PUBBENCH('banc7'), P('bonnet7', 'nightCap', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'side': 1})],
        cams=[C7])
st.cue('sfx:crickets', 'S07', 0.0, 0.1)

# 8: the judge insisted. From the dock side: the judge leans far over his bench, raises the gavel beside his wig and bangs it, then points at
#    the cloud (at us)
D8 = st.dur('S08'); HIT8 = 0.46
BLOCK8 = [0.33, 1.53, -3.0]
GAV8 = BLOCK8
C8 = cam(0.0, [-0.6, 2.25, -0.5], [-0.55, 2.25, -0.75], [0.15, 2.05, -3.8], [0.15, 2.05, -3.8], lens=50)
chk('S08', C8, {'face': [0.0, 2.25, -4.1], 'block': BLOCK8, 'gavelUp': [0.45, 3.2, -3.7], 'wig': [0.0, 2.75, -4.1]})
# (pass 1) the gavel is a free prop moved with his left hand (attached to the hand it vanished): rest, a slow anticipation lift beside the wig, a hold,
# a two-frame drop to a contact frame on the block (his body squashes, the bench shakes), then he points at the cloud with the other hand
G8 = [(0.0, [0.38, 1.85, -3.45], 1.7, 0.0, 'linear'), (0.06, [0.44, 2.72, -3.72], 0.45, 0.24, 'out'), (0.3, [0.46, 2.82, -3.76], 0.35, 0.08, 'inOut'),
      (r(HIT8 - 0.07), [0.33, 1.95, -3.35], 2.356, 0.07, 'in')]
def J8(t, lh, rh=None, lean=0.5, face=None, d=0.1, e='inOut', sq=(1, 1, 1)):
    tn = {'reach': {'L': [*lh, 1, 0.03], **({'R': [*rh, 1, 0.15]} if rh else {})}, 'hands': {'L': 'grip', **({'R': 'point'} if rh else {})}, 'bend': {'spine': [lean, 0, 0, 1, None], 'neck': [-0.25, 0, 0, 1, None]}, 'sq': list(sq), 'face': face or {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}}
    return k(t, toon=tn, toonDur=d, toonEase=e)
HIT_F8 = {'lid': 0.1, 'mouth': 'open', 'brow': -1.0}
st.shot('S08', 'courtroom', setOpts=COURT, actors=[act('juge', JUDGE, 0, 'stand', 'angry', keys=[k(0.0, look=[-0.9, 1.9, 0.6]),
            J8(0.0, G8[0][1], lean=0.3, d=0.0), J8(G8[1][0], G8[1][1], lean=0.4, d=G8[1][3], e='out', sq=(0.97, 1.04, 0.97)), J8(G8[2][0], G8[2][1], lean=0.38, d=G8[2][3], sq=(0.96, 1.05, 0.96)),
            J8(G8[3][0], G8[3][1], lean=0.62, d=0.07, e='in'), J8(HIT8, G8[3][1], lean=0.66, face=HIT_F8, d=0.03, sq=(1.08, 0.9, 1.08)),
            J8(r(HIT8 + 0.12), G8[3][1], lean=0.6, face=HIT_F8, d=0.1),
            J8(0.78, G8[3][1], [-0.5, 2.15, -2.9], lean=0.62, face=HIT_F8, d=0.14, e='out'),
            J8(1.05, G8[3][1], [-0.55, 2.2, -2.85], lean=0.6, face={'lid': 0.25, 'mouth': 'clench', 'brow': -0.9}, d=0.2)])],
        props=[P('marteau8', 'gavel', pos=G8[0][1], rot=[G8[0][2], 0, 0], keys=[*[k(t_, to=p_, dur=max(0.01, d_), ease=e_) for t_, p_, _, d_, e_ in G8[1:]], *[k(t_, rotTo=[a_, 0, 0], dur=max(0.01, d_), ease=e_) for t_, _, a_, d_, e_ in G8[1:]]]),
               P('socle8', 'soundBlock', pos=BLOCK8, keys=[k(HIT8, scale=0.8, dur=0.03), k(r(HIT8 + 0.05), scale=1.0, dur=0.12)]),
               P('choc8', 'impactStars', pos=add(BLOCK8, [0, 0.12, 0.05]), opts={'at': HIT8}),
               # (pass 2) the drop drawn as a smear: a wooden ribbon with speed lines from the raised gavel down to the block, two frames
               P('trainee8', 'smearTrail', pos=[0, 0, 0], opts={'pts': [[0.46, 2.85, -3.74], [0.47, 2.6, -3.66], [0.44, 2.32, -3.56], [0.39, 2.05, -3.44], [0.34, 1.82, -3.34]], 'at': r(HIT8 - 0.075), 'dur': 0.075, 'w': 0.32, 'normal': [-0.3, 0.1, 0.95], 'opacity': 0.8, 'color': '#6E4424'})],
        fx=[{'type': 'shake', 'at': HIT8, 'dur': 0.18, 'amount': 0.022}],
        cams=[C8])
st.cue('sfx:gavel', 'S08', HIT8, 0.6)

# 9: it answered. (a) On the cloud in the dock: its mouth opens on a glowing yellow inside, a white flash, shockwave rings blast out toward us;
#    behind it on the public bench the man jolts awake, nightcap flying; (b) the judge's bench: his wig flies off, papers whirl up, the rings pass
D9 = st.dur('S09'); BL9 = 0.12; CUT9 = 0.48
CA9P = [-1.0, 1.75, -2.6]
CA9 = cam(0.0, CA9P, add(CA9P, [0.0, 0.0, 0.2]), [-0.66, 1.35, 1.34], [-0.66, 1.35, 1.34], lens=66)
CB9P = [1.1, 2.1, -1.5]
CB9 = cam(CUT9, CB9P, add(CB9P, [-0.05, 0.02, -0.15]), [0.0, 2.3, -4.2], [0.0, 2.35, -4.2], lens=50)
chk('S09a', CA9, {'g2': [-0.4, 2.05, 1.15], 'g1': [-2.6, 2.05, 1.15], 'face': FACED, 'hero': [PUB[0], 1.65, PUB[2]], 'heroUp': [PUB[0], 2.3, PUB[2]]})
chk('S09b', CB9, {'judgeFace': [0.0, 2.05, -4.25], 'wig': [0.0, 3.3, -4.2]})
RING9 = loc(FACED, RYD, 0, 0.1, -0.2 * SD)
st.shot('S09', 'courtroom', setOpts=COURT, actors=[*gend_actors({w: [k(r(BL9 + 0.02), toon={'sq': [1.08, 0.88, 1.08], 'face': {'lid': 1.0, 'mouth': 'clench'}, 'hairUp': 1.0}, toonDur=0.04)] for w, _, _ in GEND}),
        SLEEPER([k(0.0, look=None), k(0.0, toon={'face': {'lid': 1, 'mouth': 'smile'}, 'bend': {'neck': [0.25, 0.3, 0, 1, None]}}, toonDur=0.0),
                 k(r(BL9 + 0.12), toon={'face': {'lid': 0, 'pop': 0.55, 'mouth': 'O', 'brow': 0.9}, 'hairUp': 1.4, 'sq': [0.88, 1.18, 0.88], 'auto': 0}, toonDur=0.05),
                 k(r(BL9 + 0.4), toon={'face': {'lid': 0, 'eye': 0.5, 'mouth': 'O', 'brow': 0.7}, 'hairUp': 1.0, 'sq': [1, 1, 1], 'auto': 0}, toonDur=0.15)]),
        act('juge', JUDGE, 0, 'stand', 'angry', keys=[k(0.0, look=[-1.2, 1.8, 1.0]),
            k(0.0, toon={'bend': {'spine': [0.5, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.0),
            # (pass 2) a proper take: blown back (spine and neck), eyes out on stalks, the head stretched tall, the jaw dropped open
            k(r(CUT9 - 0.06), toon={'bend': {'spine': [-0.32, 0, 0, 1, None], 'neck': [-0.25, 0, 0, 1, None]}, 'hat': [0.3, 0.4, 1.5], 'hairUp': 1.3, 'sq': [0.88, 1.14, 0.88], 'scl': {'head': [0.85, 1.4, 1.0]}, 'face': {'lid': 0, 'pop': 0.85, 'mouth': 'scream', 'jaw': 0.8, 'jawLen': 0.45, 'brow': 1.0}}, toonDur=0.05, toonEase='out'),
            k(r(CUT9 + 0.04), toon={'bend': {'spine': [-0.38, 0, 0, 1, None], 'neck': [-0.3, 0, 0, 1, None]}, 'hat': [0.55, 0.7, 3.0], 'hairUp': 1.4, 'sq': [0.86, 1.18, 0.86], 'scl': {'head': [0.8, 1.5, 1.0]}, 'face': {'lid': 0, 'pop': 0.9, 'mouth': 'scream', 'jaw': 0.9, 'jawLen': 0.5, 'brow': 1.0}}, toonDur=0.06, toonEase='out'),
            k(r(CUT9 + 0.14), toon={'bend': {'spine': [-0.3, 0, 0, 1, None], 'neck': [-0.22, 0, 0, 1, None]}, 'hat': [0.6, 0.8, 3.3], 'hairUp': 1.3, 'sq': [0.92, 1.1, 0.92], 'scl': {'head': [0.88, 1.36, 1.0]}, 'face': {'lid': 0, 'pop': 0.85, 'mouth': 'scream', 'jaw': 0.85, 'jawLen': 0.45, 'brow': 1.0}}, toonDur=0.12),
            k(r(CUT9 + 0.36), toon={'bend': {'spine': [-0.2, 0, 0, 1, None], 'neck': [-0.1, 0, 0, 1, None]}, 'hat': [0.8, 1.0, 5.0], 'hairUp': 1.2, 'scl': {'head': [0.95, 1.18, 1.0]}, 'face': {'lid': 0, 'pop': 0.7, 'mouth': 'O', 'jaw': 0.5, 'jawLen': 0.35, 'brow': 0.9}}, toonDur=0.16)])],
        props=[DOCKBOX('box9'), PUBBENCH('banc9'), *GKEPIS('9'),
               CLOUD('nuage9', CLD, RYD, SD, expr=[[0.0, 'angry'], [0.06, 'shout']], sq=[[0.0, *SQD], [0.06, 0.96, 1.18, 1.0]], arms=[[0.0, 'cuff', 'cuff']], cuffs=True, flash=[[BL9, 0.3]], flashK=0.35, seed=5, **T_COURT),
               P('onde9', 'shockRing', pos=RING9, ry=RYD, opts={'at': BL9, 'dur': 0.6, 'r': 6.5, 'travel': 4.5, 'n': 3, 'core': 0.6}),
               P('onde9b', 'shockRing', pos=[0.0, 2.0, -1.0], ry=RYD, opts={'at': r(CUT9 - 0.05), 'dur': 0.5, 'r': 5.0, 'travel': 3.0, 'n': 2, 'core': 0.01}),
               P('bonnet9', 'nightCap', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'side': -1}, keys=[k(0.0, visible=True), k(r(BL9 + 0.12), visible=False)]),
               P('bonnet9v', 'nightCap', pos=[PUB[0], 2.3, PUB[2]], opts={'side': -1}, keys=[k(0.0, visible=False), k(r(BL9 + 0.12), visible=True), k(r(BL9 + 0.12), to=[PUB[0] + 0.3, 3.1, PUB[2] + 0.6], dur=0.3, ease='out'), k(r(BL9 + 0.12), rotTo=[0.8, 0.0, 2.2], dur=0.4)]),
               *[P(f'papier9{j}', 'flyingPaper', pos=[-0.5 + 0.33 * j, 1.58, -3.6], scale=0.8, keys=[k(r(CUT9 - 0.04 + 0.02 * j), to=[[-1.5, -1.05, 1.05, 1.5][j], [1.75, 2.3, 2.5, 1.85][j], -4.05], dur=0.4, ease='out')]) for j in range(4)]],
        fx=[{'type': 'flash', 'at': BL9, 'dur': 0.25}, {'type': 'shake', 'at': BL9, 'dur': 0.4, 'amount': 0.03}, {'type': 'wind', 'at': CUT9, 'dur': 0.4, 'v': [0, 0, -10]}],
        cams=[CA9, CB9])
st.cue('thunder', 'S09', BL9, 0.95); st.cue('sfx:paper', 'S09', r(CUT9 + 0.05), 0.3); st.cue('whoosh', 'S09', CUT9, 0.3, 0.4, 300, 2000)

# 10: the district lost all its windows. Outside, the street of the court: the courthouse at the end, blocks on both sides; every window pops out
#     of the facades at once and drops onto the empty pavement; (b) low on the pavement: panes land and burst into shards, nobody there
D10 = st.dur('S10'); POP10 = 0.3; CUT10 = 1.15
FAC10 = [(9.3, -6.5, -90, 11), (9.3, -19.6, -90, 12), (-9.3, -3.0, 90, 13), (-9.3, -16.1, 90, 14)]
CA10P = [-6.0, 1.7, 6.0]
CA10 = cam(0.0, CA10P, add(CA10P, [0.3, 0.25, -0.9]), [7.0, 6.0, -17.0], [7.0, 6.2, -17.0], lens=50)   # (pass 2) from the far pavement, the right-hand facades at an angle, bigger windows: the pops read at phone size
CB10P = [5.8, 0.55, 2.0]
CB10 = cam(CUT10, CB10P, add(CB10P, [0.15, 0.05, -0.2]), [8.6, 2.6, -6.5], [8.6, 2.5, -6.5], lens=54)
chk('S10a', CA10, {'courtTop': [0, 9.0, -34.0], 'facR': [9.3, 13.0, -6.5], 'facL': [-9.3, 13.0, -3.0], 'paveR': [7.5, 0, -2.0]})
chk('S10b', CB10, {'win0': [9.3, 3.8, -6.5], 'land': [8.3, 0.0, -6.5], 'top': [9.3, 12.0, -6.5]})
st.shot('S10', 'parisStreet', setOpts={'eiffel': False, 'clear': [-40.0, 12.0], 'clearL': [-40.0, 12.0]}, actors=[],
        props=[*[P(f'facade10{j}', 'popFacade', pos=[x_, 0.0, z_], ry=a_, opts={'w': 12.6, 'h': 13.0, 'floors': 4, 'cols': 4, 'winW': 1.75, 'winH': 0.7, 'popAt': POP10, 'seed': s_, 'walk': 2.0, 'color': ['#EADFC8', '#F0D8C8', '#E8E2D0', '#E2DCE8'][j]}) for j, (x_, z_, a_, s_) in enumerate(FAC10)],
               P('tribunal10', 'courtFront', pos=[0.0, 0.0, -32.0], opts={'w': 14, 'steps': 4, 'cols': 6, 'title': 'TRIBUNAL'})],
        fx=[{'type': 'shake', 'at': POP10, 'dur': 0.3, 'amount': 0.012}],
        cams=[CA10, CB10])
st.cue('sfx:glass', 'S10', POP10, 0.6); st.cue('sfx:glass', 'S10', 0.95, 0.5); st.cue('sfx:glass', 'S10', 1.35, 0.6); st.cue('sfx:glass', 'S10', 1.7, 0.5)

# 11: the twelve jurors are deaf. The jury on three tiers (four to a tier) on the right of the courtroom: plaster dust drifts down over them, their
#     hair blown straight back; they sit perfectly still and dignified, hands folded, eyes calm on the dock; on the middle tier one of them turns
#     a page of her booklet
D11 = st.dur('S11'); FLIP11 = 0.55
JB = [4.4, 0, -2.4]; RYJ = -90; JST = 0.86; JDP = 0.85   # (pass 2) higher steps: the rows' heads no longer cross
JURORS = []
for i in range(3):
    for j in range(4):
        JURORS.append((f'jure{i * 4 + j + 1}', loc(JB, RYJ, -1.26 + 0.78 * j + 0.39 * (i % 2), -(i + 0.5) * JDP - 0.17, i * JST), i, j))   # every other row shifted half a seat
PAGE_J = JURORS[5]
RYJA = -74   # (pass 2) the jurors turned a little toward the lens: their hair, blown straight back, reads as swept back (square-on it read as standing up)
BOOK11 = off(PAGE_J[1], RYJA, 0.4, 0.0, 1.0)
C11P = [0.2, 2.45, -2.4]
C11 = FIT(0.0, C11P, {'tl': add(JURORS[8][1], [0, 2.0, 0]), 'tr': add(JURORS[11][1], [0, 2.0, 0]), 'bl': add(JURORS[0][1], [0, 0.55, -0.35]), 'br': add(JURORS[3][1], [0, 0.55, 0.35]), 'hl': add(JURORS[0][1], [0, 2.0, -0.35]), 'hr': add(JURORS[3][1], [0, 2.0, 0.35])}, top=0.1, bottom=0.76, margin=0.05, drift=(0.15, 0, 0.0))
chk('S11', C11, {**{w: add(p, [0, 1.65, 0]) for w, p, i, j in JURORS}, 'book': BOOK11})
# (pass 1) three clear tiers (0.62 m apart) of four, seen square-on; no spikes (hair blown back by the wind only); the jurors sit back on their benches
# (their knees stay behind the front panels); slow blinks one after another; the middle juror of the middle tier turns a page of a big white booklet
def SLOWBLINK(t, face): return [k(t, toon={'face': {**face, 'lid': 1.0}}, toonDur=0.12, keepPose=True), k(r(t + 0.22), toon={'face': face}, toonDur=0.14, keepPose=True)]
def juror(w, p, i, j):
    base = {'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}, 'wind': [0, -8, -9], 'reach': {'L': [*off(p, RYJA, 0.34, -0.08, 0.9), 1, 0.05], 'R': [*off(p, RYJA, 0.34, 0.08, 0.9), 1, 0.05]}, 'hands': {'L': 'rest', 'R': 'rest'}}
    ks = [k(0.0, look=[-1.5, 1.6 + i * 0.3, -1.0]), k(0.0, toon=base, toonDur=0.0)]
    if w == PAGE_J[0]:
        b2 = {**base, 'reach': {'L': [*off(p, RYJA, 0.4, -0.3, 1.04), 1, 0.05], 'R': [*off(p, RYJA, 0.4, 0.3, 1.04), 1, 0.05]}, 'hands': {'L': 'pinch', 'R': 'pinch'}}
        b3 = {**b2, 'reach': {'L': [*off(p, RYJA, 0.4, -0.3, 1.04), 1, 0.05], 'R': [*off(p, RYJA, 0.46, -0.15, 1.12), 1, 0.05]}}
        ks = [k(0.0, look=BOOK11), k(0.0, toon=b2, toonDur=0.0), k(r(FLIP11 - 0.08), toon=b3, toonDur=0.3), k(r(FLIP11 + 0.42), toon=b2, toonDur=0.25), *SLOWBLINK(1.15, base['face'])]
    else:
        ks += SLOWBLINK(r(0.15 + 0.11 * ((i * 4 + j) * 5 % 12)), base['face'])
        # (pass 2) a slow breath each, out of step with the others
        b0 = 0.1 + 0.13 * ((i * 4 + j) * 7 % 11)
        ks += [k(r(b0), toon={'sq': [1.015, 0.982, 1.015]}, toonDur=0.4, toonEase='inOut', keepPose=True), k(r(b0 + 0.5), toon={'sq': [1.0, 1.0, 1.0]}, toonDur=0.45, toonEase='inOut', keepPose=True)]
    return act(w, p, RYJA, 'sit', 'neutral', keys=ks)
st.shot('S11', 'courtroom', setOpts=COURT, actors=[juror(*x) for x in JURORS],
        props=[P('jury11', 'juryTiers', pos=JB, ry=RYJ, opts={'w': 3.9, 'step': JST, 'deep': JDP}), P('livret11', 'pageBook', pos=BOOK11, ry=RYJA, rot=[-0.3, 0, 0], scale=1.5, opts={'flipAt': FLIP11, 'flipDur': 0.4, 'cover': '#8E2E3A'}),
               P('poussiere11', 'plasterFall', pos=[JB[0] - 1.6, 0.0, JB[2]], opts={'w': 2.4, 'd': 4.2, 'top': 5.0, 'n': 80, 'size': 0.06, 'haze': 3, 'hazeOp': 0.14})],
        cams=[C11])
st.cue('sfx:paper', 'S11', FLIP11, 0.3); st.cue('sfx:crickets', 'S11', 0.0, 0.08)

# 12: three experts confirmed: it was loud. In front of the bench, three experts in white coats; the middle one holds up a big sound-level meter
#     whose red needle has bent through the top of its case and sticks out, quivering, smoking; the three nod together, twice; (b) insert on the
#     meter: the bent needle twangs
D12 = st.dur('S12'); CUT12 = 1.45
EXP = [('expert1', [-0.85, 0, -1.6], 12), ('expert2', [0.0, 0, -1.4], 0), ('expert3', [0.85, 0, -1.6], -12)]
MET12 = [0.0, 1.05, -0.8]
CA12P = [0.25, 1.65, 2.4]
CA12 = cam(0.0, [0.2, 1.7, 2.9], [0.2, 1.7, 2.6], [0.0, 1.62, -1.5], [0.0, 1.62, -1.5], lens=46)
CB12P = add(MET12, [0.35, 0.55, 1.25])
CB12 = cam(CUT12, CB12P, add(CB12P, [-0.03, 0, -0.15]), add(MET12, [0.05, 0.17, 0]), add(MET12, [0.05, 0.17, 0]), lens=54)
chk('S12a', CA12, {**{w: [p[0], 2.05, p[2]] for w, p, _ in EXP}, 'met': MET12})
chk('S12b', CB12, {'met': MET12, 'needle': add(MET12, [0.25, 0.6, 0.1]), 'face2': [0.0, 2.05, -1.4]})
def nods(t0, face, hold=None):
    ks = []
    for n, tt in enumerate([t0, t0 + 0.42]):
        ks += [k(r(tt), toon={**(hold or {}), 'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': face}, toonDur=0.12), k(r(tt + 0.2), toon={**(hold or {}), 'bend': {'neck': [-0.05, 0, 0, 1, None]}, 'face': face}, toonDur=0.14)]
    return ks
HOLD12 = {'reach': {'L': [MET12[0] + 0.44, MET12[1] - 0.05, MET12[2] + 0.02, 1, 0.05], 'R': [MET12[0] - 0.44, MET12[1] - 0.05, MET12[2] + 0.02, 1, 0.05]}, 'hands': {'L': 'grip', 'R': 'grip'}}
FX12 = {'lid': 0.3, 'mouth': 'line', 'brow': 0.5}
st.shot('S12', 'courtroom', setOpts=COURT, actors=[act(w, p, a_, 'stand', 'neutral', keys=[k(0.0, look='camera'), *(([k(0.0, toon={**HOLD12, 'face': FX12}, toonDur=0.0)] + nods(0.3, FX12, HOLD12)) if w == 'expert2' else nods(r(0.3 + 0.04 * j), FX12))])
                                               for j, (w, p, a_) in enumerate(EXP)],
        props=[P('sono12', 'soundMeter', pos=MET12, scale=1.35, opts={'twangAt': r(CUT12 + 0.15)})],
        cams=[CA12, CB12])
st.cue('sfx:twang', 'S12', r(CUT12 + 0.15), 0.35); st.cue('sfx:static', 'S12', 0.1, 0.08)

# ---- the padded cell (S13-S16): paddedCell at the origin (whiteVoid): inside x +-1.8, z -1.8..1.8, the door in the front wall (z 1.8) at x 0
MIMEKIT = lambda sid: [P(f'beret{sid}', 'mimeBeret', on={'actor': 'mime', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}), P(f'rayures{sid}', 'mimeStripes', on={'actor': 'mime', 'joint': 'torso', 'offset': [0.0, 0.0, 0.0]})]
CELL = {'w': 4.2, 'd': 4.2, 'h': 3.4, 'doorW': 0.95, 'doorH': 2.45}
FZ = 2.1

# 13: it was put in a padded cell. Inside the white quilted cell, low, facing the narrow door: the cloud is squeezed through the doorway toward us,
#     thin and tall, eyes out, then pops back to its size inside with a wobble; behind it in the corridor the two guards push, their heads over it
#     (COUPABLE)
D13 = st.dur('S13'); POP13 = 1.05
S13 = 0.72; CL13A = [0.0, 0.45, 3.3]; CL13B = [0.0, 0.45, 1.0]   # (pass 2) it pops in floating, nearer the door: its face clear of the captions
# (pass 2) the guards side by side at the same depth (one behind the other, their heads merged), the camera higher and more square to the door so
# the cloud's face sits well above the caption band
G13 = [('gardien1', [0.02, 0, 3.6], 180), ('gardien2', [0.4, 0, 3.6], 180)]
C13P = [0.35, 2.7, -1.85]
C13 = cam(0.0, C13P, add(C13P, [-0.05, 0, 0.12]), [0.05, 1.35, 1.5], [0.05, 1.35, 1.5], lens=62)
chk('S13', C13, {'g1': [0.02, 2.1, FZ + 0.5], 'g2': [0.4, 2.1, FZ + 0.5], 'face': CFACE(CL13B, 180, S13), 'doorTop': [0, 2.15, FZ]})
st.shot('S13', 'whiteVoid', setOpts={'color': '#C9CED4'}, actors=[act(w, p, a_, 'stand', 'determined', keys=[k(0.0, look=[0, 1.6, 0.0]), k(0.0, to=[p[0], 0, FZ + 0.5], dur=POP13, ease='inOut', glide=True, face='keep'),
            k(0.0, toon={'reach': {'L': [p[0] - 0.15, 1.2, FZ + 0.6, 1, 0.05], 'R': [p[0] + 0.15, 1.2, FZ + 0.6, 1, 0.05]}, 'hands': {'L': 'open', 'R': 'open'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.5}}, toonDur=0.0)]) for w, p, a_ in G13],
        props=[P('cellule13', 'paddedCell', pos=[0, 0, 0], opts={**CELL, 'open': [[-1.0, 1.0]]}),
               CLOUD('nuage13', CL13A, 180, S13, keys=[k(0.0, to=CL13B, dur=POP13, ease='inOut')], expr=[[0.0, 'surprised'], [r(POP13 + 0.05), 'angry']],
                     sq=[[0.0, 0.42, 1.18, 0.9], [r(POP13 - 0.05), 0.42, 1.18, 0.9], [POP13, 1.18, 0.85, 1.0], [r(POP13 + 0.15), 0.94, 1.05, 1.0], [r(POP13 + 0.3), 1, 1, 1]], arms=[[0.0, 'up', 'up'], [r(POP13 + 0.1), 'rest', 'rest']], seed=13)],
        cams=[C13])
st.card('S13', 'COUPABLE', at=r(POP13 + 0.15))
st.cue('sfx:stretch', 'S13', 0.2, 0.3); st.cue('pop', 'S13', POP13, 0.5); st.cue('thud', 'S13', r(POP13 + 0.1), 0.3)

# 14: in the cell there already was a mime. Inside, the far corner: a box-headed mime (white face, striped shirt, black beret) presses both
#     palms on an invisible wall, slides them along it, then gives a small wave to the cloud; the cloud, in the foreground on the right, stares
D14 = st.dur('S14'); WAVE14 = 1.45
MIME = [-1.0, 0, -1.3]
C14P = [1.1, 1.75, 1.85]
RYM = r(yaw(MIME, C14P) - 8)
CL14 = [0.6, 0.55, -1.3]
C14 = cam(0.0, C14P, add(C14P, [-0.05, 0, -0.2]), [-0.3, 1.35, -1.2], [-0.3, 1.35, -1.2], lens=56)
chk('S14', C14, {'mimeFace': [MIME[0], 2.05, MIME[2]], 'cloudFace': CFACE(CL14, -20, 0.6)})
# (pass 1) the invisible wall: the mime square to us, both palms flat on one plane 0.42 m in front of him at face height, sliding together along it
# (left, up, right), elbows out, forearms quiet; each stop a tiny press (the palms flatten on the glass); then a small wave to the cloud
def WALL14(t, a, b, face, d=0.18, press=0.0):
    f = 0.42 - press
    return k(t, toon={'reach': {'L': [*off(MIME, RYM, f, -0.36 + a, 1.72 + b), 1, 0.05], 'R': [*off(MIME, RYM, f, 0.36 + a, 1.72 + b), 1, 0.05]}, 'hands': {'L': 'open', 'R': 'open'}, 'hose': 0.25, 'face': face}, toonDur=d, toonEase='inOut')
FM14 = {'lid': 0.3, 'mouth': 'line', 'brow': 0.6}
st.shot('S14', 'whiteVoid', setOpts={'color': '#C9CED4'}, actors=[act('mime', MIME, RYM, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            WALL14(0.0, 0.0, 0.0, FM14, 0.0), WALL14(0.12, 0.0, 0.0, FM14, 0.06, press=0.03), WALL14(0.32, -0.2, 0.0, FM14), WALL14(0.5, -0.2, 0.0, FM14, 0.06, press=0.03),
            WALL14(0.68, -0.2, 0.18, FM14), WALL14(0.88, 0.2, 0.18, FM14, 0.22), WALL14(1.1, 0.2, 0.18, FM14, 0.06, press=0.03),
            k(WAVE14, toon={'reach': {'R': [*off(MIME, RYM, 0.25, 0.32, 2.0), 1, 0.05]}, 'hands': {'R': 'spread'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.7}}, toonDur=0.15),
            k(r(WAVE14 + 0.18), toon={'reach': {'R': [*off(MIME, RYM, 0.25, 0.42, 2.02), 1, 0.05]}, 'hands': {'R': 'spread'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.7}}, toonDur=0.12),
            k(r(WAVE14 + 0.34), toon={'reach': {'R': [*off(MIME, RYM, 0.25, 0.3, 2.0), 1, 0.05]}, 'hands': {'R': 'spread'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.7}}, toonDur=0.12)])],
        props=[P('cellule14', 'paddedCell', pos=[0, 0, 0], opts=CELL), *MIMEKIT('14'),
               CLOUD('nuage14', CL14, -20, 0.6, expr=[[0.0, 'angry'], [r(WAVE14 + 0.1), 'blank']], look=[[0.0, -0.8, 0.0], [r(WAVE14 + 0.2), 0.3, 0.0]], seed=14)],
        cams=[C14])
st.cue('sfx:squeak', 'S14', 0.12, 0.1); st.cue('sfx:squeak', 'S14', 0.5, 0.1); st.cue('sfx:squeak', 'S14', 1.1, 0.1)

# 15: the mime asked for a transfer. Inside, by the door: the guard's face blank in the open hatch; the mime, three quarters to us, points straight
#     across at the cloud (in the right foreground), then mimes a suitcase: folds a shirt into it, snaps it shut, lifts it by the handle, and walks
#     away on the spot
D15 = st.dur('S15'); PACK15 = 0.62; SNAP15 = 1.0; LIFT15 = 1.15; WALK15 = 1.38
MIME15 = [-0.4, 0, FZ - 0.6]; RYM15 = 155
GARD15 = [0.0, 0, FZ + 0.32]
CL15 = [0.8, 0.95, 1.05]; S15C = 0.5
C15P = [1.0, 1.75, -0.3]
RYC15 = r(yaw(CL15, C15P) + 35)   # (pass 2) a quarter turned to the lens: both eyes show
C15 = FIT(0.0, C15P, {'mime': [MIME15[0], 2.4, MIME15[2]], 'mimeFeet': [MIME15[0], 0.3, MIME15[2]], 'hatch': [0.0, 2.25, FZ], 'hatchB': [0.0, 1.8, FZ], 'cloudFace': CFACE(CL15, RYC15, S15C), 'cloudFaceO': loc(CL15, RYC15, -0.5 * S15C, 0.67 * S15C, 0.82 * S15C)}, top=0.1, bottom=0.76, drift=(0.0, 0, 0.15), lenses=range(30, 67), inside=(-1.95, 1.95, 0.3, 3.2, -1.95, 1.95))
chk('S15', C15, {'mimeFace': [MIME15[0], 2.05, MIME15[2]], 'guardFace': [0.0, 2.08, GARD15[2]], 'hatch': [0.0, 2.02, FZ], 'cloudFace': CFACE(CL15, RYC15, S15C), 'cfL': loc(CL15, RYC15, -0.5 * S15C, 0.67 * S15C, 0.82 * S15C), 'cfR': loc(CL15, RYC15, 0.5 * S15C, 0.67 * S15C, 0.82 * S15C)})
FM15 = {'lid': 0.2, 'mouth': 'line', 'brow': 0.7}
SH15 = off(MIME15, RYM15, 0.0, 0.24, 1.66)
_v = [CFACE(CL15, RYC15, S15C)[i] - SH15[i] for i in range(3)]; _n = math.sqrt(sum(x * x for x in _v)); PT15 = [r(SH15[i] + _v[i] / _n * 0.66) for i in range(3)]
def M15(t, L, R, hands=('spread', 'spread'), face=None, d=0.14, sq=(1, 1, 1)):
    rr = R if len(R) == 3 and isinstance(R, list) and R is PT15 else off(MIME15, RYM15, *R)
    return k(t, toon={'reach': {'L': [*off(MIME15, RYM15, *L), 1, 0.08], 'R': [*rr, 1, 0.12]}, 'hands': {'L': hands[0], 'R': hands[1]}, 'face': face or FM15, 'sq': list(sq)}, toonDur=d)
st.shot('S15', 'whiteVoid', setOpts={'color': '#C9CED4'}, actors=[
        act('mime', MIME15, RYM15, 'stand', 'neutral', keys=[k(0.0, look=CFACE(CL15, RYC15, S15C)),
            M15(0.0, (0.3, -0.25, 1.0), PT15, ('rest', 'point'), d=0.0), M15(0.18, (0.3, -0.25, 1.0), PT15, ('rest', 'point'), face={'lid': 0.1, 'mouth': 'O', 'brow': 0.9}, sq=(0.97, 1.04, 0.97)),
            M15(0.4, (0.3, -0.25, 1.0), PT15, ('rest', 'point'), face={'lid': 0.1, 'mouth': 'O', 'brow': 0.9}),
            k(r(PACK15 - 0.08), look='camera', lookDur=0.15),
            M15(PACK15, (0.42, -0.25, 1.3), (0.42, 0.25, 1.3), ('open', 'open')), M15(r(PACK15 + 0.16), (0.48, -0.05, 1.05), (0.48, 0.05, 1.05), ('open', 'open'), sq=(1.03, 0.97, 1.03)),
            M15(r(PACK15 + 0.3), (0.42, -0.28, 1.22), (0.42, 0.28, 1.22), ('open', 'open')),
            M15(SNAP15, (0.45, -0.06, 1.1), (0.45, 0.06, 1.1), ('fist', 'fist'), face={'lid': 0.3, 'mouth': 'smile', 'brow': 0.6}, d=0.05),
            M15(LIFT15, (0.15, -0.3, 1.0), (0.05, 0.36, 0.78), ('rest', 'grip'), d=0.12, sq=(0.98, 1.03, 0.98)),
            M15(WALK15, (0.15, -0.3, 1.0), (0.05, 0.36, 0.82), ('rest', 'grip')),
            k(WALK15, clip='walk', params={'speed': 1.0}), k(WALK15, to=MIME15, dur=0.6, glide=False, face=RYM15)]),
        act('gardien1', GARD15, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[MIME15[0], 1.9, MIME15[2]]), *blink(1.1)])],
        props=[P('cellule15', 'paddedCell', pos=[0, 0, 0], opts={**CELL, 'hatch': [[0.0, 1.0]], 'hatchW': 0.6, 'hatchH': 0.56, 'hatchY': 2.08}), *MIMEKIT('15'),
               CLOUD('nuage15', CL15, RYC15, S15C, expr=[[0.0, 'blank'], [0.5, 'angry']], look=[[0.0, -0.8, 0.0]], seed=15)],
        cams=[C15])
st.cue('clack', 'S15', SNAP15, 0.3)
st.cue('sfx:stepSoft', 'S15', r(WALK15 + 0.1), 0.12); st.cue('sfx:stepSoft', 'S15', r(WALK15 + 0.4), 0.12)

# 16: out loud. Close on the hatch from the corridor: the mime's face fills the hatch; a squash of anticipation, then the shout, mouth stretched to
#     most of the hatch; the guard beside the door, three quarters to us, does not move a muscle: his cap launches straight up on the shout, hangs
#     four frames, and goes; his hair streams back
D16 = st.dur('S16'); SQ16 = 0.1; SH16 = 0.22
# (pass 2) the mime's head alone shows (headOnly), wedged in a smaller hatch and scaled to fill it: a squash down and wide (2-3 frames), then the
# snap: stretched tall, forehead and chin past the hatch's edges, the mouth dropped open over most of it, held to the end (he only leaves after the
# cap); a shock ring and speed lines burst out of the hatch; the guard's cap launches, hangs in the upper third by his head, then goes
HW16, HH16, HY16 = 0.5, 0.62, 2.12
MIME16 = [-0.2, 0.07, FZ - 0.14]
GARD16 = [-0.18, 0, FZ + 0.36]; RYG16 = 25
C16P = [-0.16, 2.26, FZ + 1.85]
C16 = cam(0.0, C16P, add(C16P, [-0.02, -0.02, -0.18]), [-0.22, 2.24, FZ + 0.1], [-0.22, 2.24, FZ + 0.1], lens=56)
chk('S16', C16, {'mimeFace': [MIME16[0], HY16, MIME16[2]], 'guardFace': [GARD16[0], 2.05, GARD16[2]], 'capHang': [GARD16[0], 2.72, GARD16[2]], 'hatchTL': [-HW16 / 2, HY16 + HH16 / 2, FZ], 'hatchBR': [HW16 / 2, HY16 - HH16 / 2, FZ]})
FG16 = {'lid': 0.5, 'mouth': 'line', 'gx': -0.8}
HO = {'headOnly': 1}
SHOUT16 = lambda sx, sy, mh=1.0, j=0.8: {**HO, 'face': {'lid': 0.0, 'eye': 0.7, 'brow': 1.0, 'mouth': 'scream', 'mouthW': 1.7, 'mouthH': mh, 'mouthDy': -14, 'jaw': j, 'jawLen': 0.42, 'jawBlock': 1}, 'sq': [0.98, 1.03, 0.98], 'scl': {'head': [sx, sy, 1.0]}}
st.shot('S16', 'whiteVoid', setOpts={'color': '#C9CED4'}, actors=[
        act('mime', MIME16, 0, 'stand', 'angry', keys=[k(0.0, look=C16P),
            k(0.0, toon={**HO, 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.8, 'eye': 0.3}, 'scl': {'head': [1.9, 1.12, 1.0]}}, toonDur=0.0),
            k(SQ16, toon={**HO, 'face': {'lid': 0.9, 'mouth': 'clench', 'brow': -0.9, 'puff': 0.9, 'cheeks': 0.8}, 'sq': [1.05, 0.94, 1.05], 'scl': {'head': [2.25, 0.88, 1.0]}}, toonDur=0.09, toonEase='out'),
            k(SH16, toon=SHOUT16(1.7, 1.34, 3.4), toonDur=0.035, toonEase='out'),
            k(r(SH16 + 0.05), toon=SHOUT16(1.62, 1.42, 3.8), toonDur=0.04, toonEase='out'),
            *[k(r(SH16 + 0.12 + 0.07 * n), toon=SHOUT16(1.68 + 0.04 * (n % 2), 1.36 - 0.03 * (n % 2), 3.6), toonDur=0.05) for n in range(7)],
            k(0.8, toon=SHOUT16(1.75, 1.3, 3.0, 0.7), toonDur=0.15)]),
        act('gardien1', GARD16, RYG16, 'stand', 'unimpressed', keys=[k(0.0, look=C16P), k(0.0, toon={'face': FG16}, toonDur=0.0),
            k(r(SH16 + 0.02), toon={'face': FG16, 'hat': [0.22, 0.2, 0.8], 'wind': [-9, 0, -11]}, toonDur=0.05, toonEase='out'),
            k(r(SH16 + 0.08), toon={'face': FG16, 'hat': [0.32, 0.32, 1.3], 'wind': [-9, 0, -11]}, toonDur=0.12, toonEase='out'),
            k(r(SH16 + 0.2), toon={'face': FG16, 'hat': [0.36, 0.36, 1.6], 'wind': [-8, 0, -10]}, toonDur=0.3),
            k(0.78, toon={'face': FG16, 'hat': [1.5, 0.7, 3.4], 'wind': [-4, 0, -5]}, toonDur=0.22, toonEase='in')])],
        props=[P('cellule16', 'paddedCell', pos=[0, 0, 0], opts={**CELL, 'hatch': [[0.0, 1.0]], 'hatchW': HW16, 'hatchH': HH16, 'hatchY': HY16}),
               P('onde16', 'shockRing', pos=[0.0, HY16, FZ + 0.14], opts={'at': SH16, 'dur': 0.42, 'r0': 0.32, 'r': 1.5, 'travel': 0.9, 'n': 3, 'core': 0.25}),
               P('traits16', 'burstLines', pos=[0.0, HY16, FZ + 0.16], opts={'at': SH16, 'dur': 0.45, 'r0': 0.36, 'r1': 1.3, 'n': 16})],
        fx=[{'type': 'shake', 'at': SH16, 'dur': 0.4, 'amount': 0.02}, {'type': 'wind', 'at': SH16, 'dur': 0.6, 'v': [-14, 1, 2]}],
        cams=[C16])
st.cue('sfx:roar', 'S16', SH16, 0.6); st.cue('whoosh', 'S16', r(SH16 + 0.05), 0.25, 0.3, 400, 2500)

# 17: on release, the thunder had no address. Prison gate by day: the cloud floats outside holding a tiny red bundle, looking lost; the clerk at
#     the gate holds up an open register, blank under ADRESSE, and shrugs; (b) closer: the empty pages, the shrug
D17 = st.dur('S17'); SHRUG17 = 1.4; CUT17 = 1.2
# (pass 2) the clerk clear of the cloud (to its right, behind a lectern), the register open on the lectern square to the lens under a big ADRESSE
# heading; he taps the blank page, then a big two-beat shrug (head sunk into the shoulders, palms out, the head tilting one way then the other);
# the cloud holds its tiny red bundle up in front of it and looks down at it, droopy
GATE = [0.0, 0, -3.0]
CL17 = [-0.76, 1.12, -1.15]; RY17 = 30; S17 = 0.62
CLERK = [0.44, 0, -0.95]; RYC17 = -15
REG17 = [0.0, 1.05, -0.5]
CA17P = [0.05, 1.75, 3.7]
CA17 = cam(0.0, CA17P, add(CA17P, [0.02, 0, -0.3]), [0.05, 1.45, -0.9], [0.05, 1.45, -0.9], lens=48)
CB17P = [0.08, 1.72, 2.85]
CB17 = cam(CUT17, CB17P, add(CB17P, [0, 0, -0.2]), [0.02, 1.55, -0.9], [0.02, 1.55, -0.9], lens=52)
chk('S17a', CA17, {'cloudFace': CFACE(CL17, RY17, S17), 'bundle': loc(CL17, RY17, -0.55 * S17, 0.95 * S17, 0.35 * S17), 'clerkFace': [CLERK[0], 2.05, CLERK[2]], 'reg': REG17, 'regR': add(REG17, [0.46, 0, 0])})
chk('S17b', CB17, {'cloudFace': CFACE(CL17, RY17, S17), 'clerkFace': [CLERK[0], 2.05, CLERK[2]], 'clerkTop': [CLERK[0], 2.4, CLERK[2]], 'reg': REG17, 'palmL': off(CLERK, RYC17, 0.22, -0.5, 1.7), 'palmR': off(CLERK, RYC17, 0.22, 0.5, 1.7)})
RYR17 = yaw(REG17, CA17P)
def SHR(t, hy, sp, tilt, neck, up, face, d=0.12, look=None):
    return k(t, toon={'reach': {'L': [*off(CLERK, RYC17, 0.22, -sp, hy), 1, 0.06], 'R': [*off(CLERK, RYC17, 0.22, sp, hy), 1, 0.06]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': face,
                      'sq': [1 + 0.06 * up, 1 - 0.08 * up, 1 + 0.06 * up], 'bend': {'neck': [0, tilt, 0, neck, None], 'spine': [-0.05 * up, 0, 0, 1, None]}}, toonDur=d, toonEase='out')
TAP17 = lambda t, dz: k(t, toon={'reach': {'R': [*add(REG17, [0.2, 0.0, 0.08 + dz]), 1, 0.1]}, 'hands': {'R': 'point', 'L': 'rest'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.1)
F17 = {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}; F17b = {'lid': 0.3, 'mouth': 'line_m6', 'brow': 0.9}
st.shot('S17', 'grassland', setOpts={'clouds': 20, 'grass': '#BDB6A8'}, actors=[act('greffier', CLERK, RYC17, 'stand', 'neutral', keys=[k(0.0, look=[-0.6, 1.5, 2.5]),
            TAP17(0.0, 0.05), TAP17(0.35, 0.0), TAP17(0.5, 0.05), TAP17(0.75, 0.0), TAP17(0.9, 0.05),
            k(r(SHRUG17 - 0.15), look='camera', lookDur=0.15),
            SHR(SHRUG17, 1.62, 0.46, 0.26, 0.4, 1.0, F17b, 0.1), SHR(r(SHRUG17 + 0.2), 1.48, 0.44, 0.1, 0.65, 0.55, F17b, 0.12),
            SHR(r(SHRUG17 + 0.36), 1.7, 0.5, -0.28, 0.35, 1.2, F17b, 0.1), SHR(r(SHRUG17 + 0.66), 1.64, 0.48, -0.24, 0.4, 1.1, F17b, 0.2),
            SHR(r(SHRUG17 + 0.95), 1.2, 0.4, -0.08, 0.9, 0.0, F17, 0.18)])],
        props=[P('portail17', 'prisonGate', pos=GATE, opts={'gate': '#76828E'}), P('registre17', 'emptyRegister', pos=REG17, ry=RYR17, rot=[-0.22, 0, 0], scale=0.95, opts={'big': True, 'stand': True, 'standH': 1.05}),
               CLOUD('nuage17', CL17, RY17, S17, expr=[[0.0, 'droopy'], [r(SHRUG17 + 0.3), 'sad']], arms=[[0.0, 'cuff', 'rest']], bundle=True, bundleS=1.6, bundleStick=True, tag=False, look=[[0.0, -0.2, 0.95], [r(SHRUG17 + 0.1), 0.4, 0.2], [r(SHRUG17 + 0.7), -0.2, 0.95]], seed=17, bob=0.06, **T_GATE)],
        cams=[CA17, CB17])
st.cue('sfx:wind', 'S17', 0.0, 0.15); st.cue('sfx:paper', 'S17', 0.3, 0.2)

# 18: house arrest at the victim's home. His garden path by day: two gendarmes walk the cloud up to his door, an electronic tag blinking green on
#     its bolt arm; the door opens: the man in pyjamas and nightcap, deadpan (ASSIGNÉ)
D18 = st.dur('S18'); OPEN18 = 0.35; STOP18 = 1.0
# (pass 2) the front gendarme goes round to the hinge side before the door swings and the second walks in on that side too (he was a floating head
# behind the cloud): the doorway stays clear, his flat face held there to the end; the tag on the arm that faces us, big, blinking; the cloud's mouth flat
DOOR18 = [0.97, 0, -4.08]
HERO18 = [0.97, 0, -3.92]; HERO18IN = [0.97, 0, -4.5]
CL18A = [1.5, 0.35, -1.0]; CL18B = [1.75, 0.35, -2.75]; RY18 = -60; S18 = 0.8
GD18 = [('gend1', [0.6, 0, -1.2], [0.05, 0, -2.5], 0.9), ('gend2', [0.45, 0, -2.1], [-0.12, 0, -3.35], 0.3)]
C18P = [-1.25, 1.9, 1.9]
C18 = cam(0.0, C18P, add(C18P, [0.1, 0, -0.25]), [1.05, 1.45, -3.0], [1.05, 1.45, -3.0], lens=56)
chk('S18', C18, {'heroFace': [HERO18[0], 2.05, HERO18[2]], 'cloudFace': CFACE(CL18B, RY18, S18), 'g1': [0.05, 2.05, -2.5], 'g2': [-0.12, 2.05, -3.35], 'g2feet': [-0.12, 0, -3.35], 'tag': loc(CL18B, RY18, 0.9 * S18, 0.6 * S18, 0.45 * S18)})
st.shot('S18', 'pavillon', setOpts={'fence': False, 'mailbox': False}, actors=[
        *[act(w, a, 180, 'stand', 'determined', scale=0.92, keys=[k(0.0, to=b, dur=d_, clip='walk', then='stand', face=yaw(a, b)), k(0.0, look=[0.97, 2.0, -4.3]), k(r(max(d_, OPEN18) + 0.25), look='camera', lookDur=0.2)]) for w, a, b, d_ in GD18],
        act('mec', HERO18IN, 0, 'stand', 'unimpressed', keys=[k(0.0, look=CFACE(CL18B, RY18, S18)), k(r(OPEN18 + 0.12), to=HERO18, dur=0.28, ease='out', glide=True, face=15), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0), *blink(1.5, {'lid': 0.5, 'mouth': 'line', 'brow': -0.2})])],
        props=[P('porte18', 'door', pos=DOOR18, opts={'color': '#2F5E58', 'openAt': OPEN18}), CAP('bonnet18'), *GKEPIS('18'),
               CLOUD('nuage18', CL18A, RY18, S18, keys=[k(0.0, to=CL18B, dur=STOP18, ease='out')], expr=[[0.0, 'blank'], [r(STOP18 + 0.1), 'flat']], arms=[[0.0, 'rest', 'hold']], tag=True, tagSide=1, tagS=2.0, lampS=2.0, seed=18, **T_DAY)],
        cams=[C18])
st.card('S18', 'ASSIGNÉ', at=r(STOP18 + 0.1))
st.cue('sfx:stepSoft', 'S18', 0.2, 0.15); st.cue('sfx:stepSoft', 'S18', 0.55, 0.15); st.cue('sfx:carDoor', 'S18', OPEN18, 0.25); st.cue('sfx:beep', 'S18', r(STOP18 + 0.3), 0.15)

# 19: it took the window side. Night, the double bed seen from over its foot: the cloud tucked under the duvet up to its chin on the window side,
#     eyes open and calm, one slow blink; the man on the door side, flat on his back, wide awake, staring at the ceiling; a slow push-in; no sound
#     from the cloud
D19 = st.dur('S19'); DART19 = 0.95
# (pass 2) seen from high over the foot of the bed, the two faces side by side across the middle of the frame (no strip of duvet filling the bottom),
# a slow push-in; the cloud lifted on its pillow so the duvet's turned-down edge runs under its face (tucked to the chin); he stares at the ceiling,
# his eyes slide slowly to the cloud, stay, slide back; the cloud calm, mouth flat, one slow blink while he looks at it
# (final pass) raised and tilted down over the foot of the bed: bed length, both pillows, the window (night, curtains) on the cloud's side; the two
# heads apart on their own pillows (his face clear of its bolt arm); the duvet's edge at the chin (pulled down the bed so his whole face shows)
S19C = 0.31; CL19 = [-0.37, 0.77, -2.7]; RX19 = -0.6
HERO19 = [0.37, BEDTOP, -1.68]
C19P = [-0.2, 3.1, -0.45]
C19 = FIT(0.0, C19P, {'cloudTop': [-0.37, 1.3, -2.75], 'pilR': [0.62, 0.82, -2.67], 'pilL': [-0.62, 0.82, -2.67], 'heroChin': [0.37, 0.9, -2.45]}, top=0.36, bottom=0.74, margin=0.02, drift=(0.02, -0.06, -0.12))
C19['ease'] = 'inOut'; C19E = C19['to']; C19L = C19['lookAt']
def _rx(p, lx, ly, lz, a):
    return [r(p[0] + lx), r(p[1] + ly * math.cos(a) - lz * math.sin(a)), r(p[2] + ly * math.sin(a) + lz * math.cos(a))]
CF19 = _rx(CL19, 0, 0.82 * S19C, 0.75 * S19C, RX19)
chk('S19', C19, {'cloudFace': CF19, 'cfL': add(CF19, [-0.19, 0, 0]), 'cfLow': add(CF19, [0, -0.12, 0]), 'heroFace': [HERO19[0], 0.97, -2.62], 'hfR': [HERO19[0] + 0.15, 0.97, -2.62], 'chest': [HERO19[0], 0.93, -2.0], 'duvetEdge': [0, 0.95, -2.5]})
chk('S19end', cam(0.0, C19E, C19E, C19L, C19L, lens=C19['lens']), {'cloudFace': CF19, 'cfL': add(CF19, [-0.19, 0, 0]), 'heroFace': [HERO19[0], 0.97, -2.6], 'hfR': [HERO19[0] + 0.16, 0.97, -2.6]})
def FACE19(gx=0.0, gy=-1.0, lid=0.0, d=0.12, t=0.0):
    return k(t, toon={'face': {'lid': lid, 'eye': 0.55, 'mouth': 'line', 'brow': 0.35, 'pupilSize': -0.25, 'gx': gx, 'gy': gy}, 'bend': {'neck': [0.32, 0, 0, 1, None]}}, toonDur=d, toonEase='inOut')
st.shot('S19', 'whiteVoid', look=NIGHT, actors=[act('mec', HERO19, 0, 'lieBack', 'neutral', blink=0, keys=[k(0.0, look=None), FACE19(gy=-0.35, d=0.0), FACE19(gy=-1.0, t=0.4, d=0.1),
            FACE19(gx=-0.9, gy=-0.25, t=DART19, d=0.3), FACE19(gx=-0.9, gy=-0.25, t=r(DART19 + 0.75), d=0.0), FACE19(t=r(DART19 + 0.8), d=0.3),
            FACE19(lid=0.3, t=2.35, d=0.05), FACE19(t=2.45, d=0.06)])],
        props=[P('chambre19', 'tonBedroom', pos=[0, 0, 0], opts={'winX': -0.78, 'duvetZ': -2.27, 'duvetTop': 0.95, 'feet': [[HERO19[0], -0.8, 0.22]], 'chest': [[HERO19[0], -2.0, 0.22]], 'breath': 3.0}), CAP('bonnet19'),
               P('nuage19', 'thunderCloud', pos=CL19, ry=0, rot=[RX19, 0, 0], opts={'s': S19C, 'expr': [[0.0, 'flat']], 'arms': [[0.0, 'tuck', 'tuck']], 'blinks': [1.45], 'blinkDur': 0.34, 'look': [[0.0, 0.0, 0.1], [r(DART19 + 0.2), 0.3, 0.1], [2.1, 0.0, 0.1]], 'bob': 0.01, 'glow': 0.3, 'seed': 19, **T_NIGHT})],
        cams=[C19])
st.cue('sfx:crickets', 'S19', 0.0, 0.12); st.cue('sfx:tick', 'S19', 0.6, 0.08); st.cue('sfx:tick', 'S19', 1.6, 0.08); st.cue('sfx:tick', 'S19', 2.6, 0.08)

print('\n'.join(CHECKS))

MEC = {'preset': 'mecPyjama', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
SPEC = {'preset': 'cop', 'outfit': 'suit', 'suit': '#1C2430', 'pants': '#1C2430', 'shirt': '#1C2430', 'lapel': '#1C2430', 'tie': '#1C2430', 'cuff': '#1C2430', 'hat': 'none', 'hair': 'bald', 'gloves': '#14161A', 'glasses': False,
        'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
CREW = {'preset': 'worker', 'suit': '#6B7350', 'pants': '#5A6142', 'hat': 'none', 'hair': 'crew', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
GARD = {'preset': 'cop2', 'facial': 'mustache', 'suit': '#5C6670', 'pants': '#4A525A', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
JUR = [('madame', {}), ('boss', {'glasses': False}), ('mamie', {}), ('worker', {'hat': 'none', 'suit': '#4E6A8C'}), ('femme', {}), ('proviseur', {}), ('politique', {'suit': '#5A4A3A', 'lapel': '#5A4A3A'}),
       ('journaliste', {}), ('serveur', {'suit': '#3A4A3A', 'glasses': False}), ('prefet', {}), ('femme', {'suit': '#8C5A7A', 'hairColor': '#C9A060'}), ('fermier', {'hat': 'none'})]
st.write("Le tonnerre", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'flic': {'preset': 'cop', 'seed': 890, 'glasses': False, 'facial': 'mustache', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    **{f'forces{j + 1}': {**SPEC, 'seed': 891 + j} for j in range(2)},
    **{f'pilote{j + 1}': {**CREW, 'seed': 893 + j, 'facial': ['mustache', 'stubble', 'none'][j]} for j in range(3)},
    **{f'gend{j + 1}': {'preset': 'cop', 'seed': 896 + j, 'suit': '#1F2A44', 'pants': '#1F2A44', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for j in range(2)},
    'avocat': {'preset': 'avocat', 'seed': 898, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'juge': {'preset': 'judge', 'seed': 899, 'facial': 'none', 'build': {'width': 0.95, 'headWidth': 1.25, 'headScale': 1.05}, 'toon': EX},
    **{f'jure{i + 1}': {'preset': p, 'seed': 900 + i, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX, **o} for i, (p, o) in enumerate(JUR)},
    'expert1': {'preset': 'savant', 'seed': 913, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'expert2': {'preset': 'doctor', 'seed': 914, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'expert3': {'preset': 'doctor', 'seed': 915, 'facial': 'mustache', 'hair': 'bald', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    **{f'gardien{j + 1}': {**GARD, 'seed': 916 + j} for j in range(2)},
    'mime': {'preset': 'sportif', 'lapel': '#22232A', 'shirt': '#22232A', 'seed': 918, 'suit': '#22232A', 'pants': '#22232A', 'skin': '#F6F4EF', 'hair': 'slick', 'hairColor': '#17161A', 'facial': 'none', 'lipstick': True, 'glasses': False,
             'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'greffier': {'preset': 'proviseur', 'seed': 919, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
