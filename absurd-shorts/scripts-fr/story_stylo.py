#!/usr/bin/env python3
"""Le stylo (story 92, cycle 50; a hook, an institutional escalation, a reversal, a dry last line).
This man pocketed the town hall's pen. The only pen of the State. Files piled up to the ceiling. Weddings were suspended. Births, put off to
Monday. Special edition: eleventh day without a pen. The president wanted to resign. Impossible: he had to sign. Customs searched every
schoolchild's pencil case. His mother turned him in. Special forces jumped onto his balcony. The balcony gave way, and the three below. The pen
was in his pocket. Chewed. It had been out of ink for ten years. His own new pen is chained at the counter. This man has visiting on Thursdays.
Staging (one oversized hero prop in every pen shot: a forearm-long polished brass ballpoint, styPen 'state', on a thick steel chain, with a big
cream ÉTAT tag; the hero's own pen is the same size in glossy red; both carry a hull so they read on every ground):
S01 from behind the town hall counter at counter height: he signs with the brass pen (the chain runs to an eyebolt), lifts it absently, the chain
snaps, he clips the pen into his breast pocket beside his red pen. S02 low at the counter's public side: the cut chain swings over the edge by the
ÉTAT tag while he strolls off, two pens in his pocket. S03 the counter top: a clean pen-shaped outline in the dust, the cut chain swinging, the clerk
behind frozen in a take, a slow push-in. S04 low and wide in the office: towers of files shoot up from every desk to the ceiling, a seated clerk
vanishes behind his. S05 the clerk peeks out between two towers pressed against the ceiling holding up the empty chain. S06 the wedding: the mayor
(sash in invented violet and gold) holds up the empty chain, slaps the register shut and a SUSPENDU sign drops onto it; bride and groom turn to us.
S07 hospital corridor, low dolly along the bench: a nurse slaps a LUNDI sign on the maternity door, three expectant fathers sit back down (REPORTÉ).
S08 the news studio: the unshaven anchor under ÉDITION SPÉCIALE, the brass pen's photo behind him. S09 the camera cranes down onto the desk: the
counter flips DIX to ONZE and the paper stack topples. S10 the press room from low: the president at the podium holds up a DÉMISSION letter (an
empty SIGNATURE line) and his sash (invented violet and gold), flashes. S11 a minister holds out the empty chain; the president lowers the letter and
another minister lowers the sash back over his head; he sags. S12 a school gate, low tracking: customs officers in blue gloves empty pencil cases on
a folding table (DOUANE), children queue with their schoolbags. S13 an officer holds a tiny pencil up against a cardboard cut-out of the brass pen,
shakes his head. S14 the police counter: his small mother slides his framed photo to the officer; the brass pen stands out of his pocket in it.
S15 night, low from the street: the helicopter over the block of flats, its searchlight on his fifth-floor balcony, commandos sliding down ropes.
S16 at the balcony: they drop onto it. S17 wide from the street: it shakes, gives way and takes the three empty balconies below down into a neat stack.
S18 the stack on the pavement, the commandos sitting on top unhurt, dusty, still aiming. S19 in the beam, against his wall in pyjamas: a gloved hand
pulls the brass pen from his pocket and holds it up (SAISI); cut in on the chewed, flattened cap; the red pen stays in his pocket. S20 top-down on
the forensic bench: a technician scribbles the pen across a white board, nothing; she shakes it, scribbles, nothing. S21 the counter: his red pen
on the chain now, the clerk signs with it; wider: a queue, he watches from the door, his pocket empty (ENCHAÎNÉ). S22 the prison visiting booth:
his red pen lies on a little stool on its chain beside a guard, he sits beyond the glass with the phone, JEUDI on the calendar behind him.
Natural look; cycle 50: props_stylo.js (new: styPen, styChain, styCounter, styFiles, styNotice, styCorridor, styStudio, styLetter, stySash,
styCutout, styPencilTable, styPencil, styPocket, styPhoto, styBlock, styBooth, styForensic, styRoom); reused: chvHeli, chvBeam (props_cheveu), register
(props_conseiller), desk, chair, bench, podium (props.js), flashBursts (props_moustache), balaclava, rifle (props_rambarde), tacHelmet (props_table),
handset (props_flaque), backpack (props_aimant); sets mairie, pressRoom, policeStation, whiteVoid; tethers for the chains and the ropes.
Lessons applied from the start: `lens` is the vertical field; characters about 2.3 m tall; faces and key props above the caption band (0.77-0.83) and
heads below the card band (0.07-0.18) in card shots; every camera checked with project() (CHECKS printed); every extra cast entry has a preset; no
English on screen, no real flags (the mairie's tricolour banner and flag removed, sashes in invented colours), no real organisation or insignia;
nobody hurt (the commandos sit unhurt on the slabs, the lower balconies are empty); box heads in a V, three-quarter to camera; horizontal actions in
depth for the 9:16 frame; thin pens and chains with a hull; animated materials unique; the idle weight shift off in the close hand shots (hip 0)."""
from story_kit import *
import math

st = Story('stylo', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 5), ('S06', 'L04', 0), ('S07', 'L05', 0),
         ('S08', 'L06', 0), ('S09', 'L06', 2), ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L09', 0), ('S13', 'L09', 5), ('S14', 'L10', 0),
         ('S15', 'L11', 0), ('S16', 'L11', 4), ('S17', 'L12', 0), ('S18', 'L12', 4), ('S19', 'L13', 0), ('S20', 'L14', 0), ('S21', 'L15', 0), ('S22', 'L16', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def sub(a, b): return [r(a[i] - b[i]) for i in range(3)]
def mul(a, s): return [r(a[i] * s) for i in range(3)]
def lerp(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))
def FC(sid, t, frm, pts, top=0.08, bottom=0.74, lenses=range(26, 67), drift=(0.0, 0.0, -0.12), margin=0.06, extra=None):
    """a camera at frm aimed and sized by fit() on the named points, drifting a little; extra: more points only checked"""
    look, lens, _ = fit(frm, pts, margin=margin, top=top, bottom=bottom, lenses=lenses)
    if lens is None: print(f'  FC {sid}: WARNING no lens fits'); lens = max(lenses)
    to = [r(frm[i] + drift[i]) for i in range(3)]; chk(sid, frm, look, lens, {**pts, **(extra or {})})
    return cam(t, frm, to, look, look, lens)
def CAM(sid, t, frm, look, lens, pts, to=None, look2=None, ease='linear'):
    """a hand-placed camera, checked"""
    chk(sid, frm, look, lens, pts)
    if to: chk(sid + 'e', to, look2 or look, lens, pts)
    return cam(t, frm, to or frm, look, look2 or look, lens, ease=ease)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]
def R5(p, w=1, s=0.04): return [*p, w, s]
def face_at(keys, t, dflt=None):
    f = dflt or DEAD
    for x in sorted((x for x in keys if 'toon' in x), key=lambda x: x['at']):
        if x['at'] <= t and 'face' in x['toon']: f = x['toon']['face']
    return f
def alive(keys, D, gap=0.8, t0=0.2, breath=True, blinks=True, amp=1.0, dflt=None):
    """blinks every ~gap s and breaths in the quiet windows (keepPose), never inside another key's tween"""
    busy = [(x['at'] - 0.1, x['at'] + (x.get('toonDur') or 0.0) + 0.06) for x in keys if 'toon' in x]
    free = lambda a, b: all(b < u0 or a > u1 for u0, u1 in busy)
    out = []
    if blinks:
        t, i = t0, 0
        while t < D - 0.2:
            if free(t - 0.02, t + 0.2): f = face_at(keys, t, dflt); out += blink(r(t), {**f, 'lid': f.get('lid', 0.4)} if f.get('lid', 0) < 0.9 else f); busy.append((t - 0.02, t + 0.22)); t += gap + 0.11 * (i % 3); i += 1
            else: t += 0.05
    if breath:
        t, j = 0.08, 0
        while t < D - 0.3:
            if free(t, t + 0.42):
                f = face_at(keys, t, dflt); q = [r(1 - 0.012 * amp), r(1 + 0.024 * amp), r(1 - 0.012 * amp)] if j % 2 == 0 else [r(1 + 0.006 * amp), r(1 - 0.01 * amp), r(1 + 0.006 * amp)]
                out.append(k(r(t), toon={'sq': q, 'face': f}, toonDur=0.4, toonEase='inOut', keepPose=True)); busy.append((t, t + 0.42)); t += 0.45; j += 1
            else: t += 0.05
    return out
def LIFE(a, D, **kw):
    a['keys'] = a['keys'] + alive(a['keys'], D, **kw); return a
def aim_rot(src, dst):
    """rot for a prop whose -Y must point from src to dst: (rx, ry deg, rz)"""
    Y = unit3([src[i] - dst[i] for i in range(3)]); X = unit3(cross3(Y, [0, 0, 1])) if abs(Y[2]) < 0.95 else unit3(cross3(Y, [1, 0, 0])); Z = cross3(X, Y)
    return axes_euler(X, Y, Z)

# ============================== the pens
PL, PRAD = 0.42, 0.024
RING = [0, r(PL / 2 + PRAD * 1.6), 0]                                    # the chain point at the top of the brass pen (local)
PEN_STATE = {'kind': 'state', 'len': PL}
PEN_RED = {'kind': 'red', 'len': PL}
POCK_S = [0.075, 0.33, 0.19]; POCK_R = [0.16, 0.33, 0.19]                 # breast pocket, torso frame (+X his left)
PATCH = lambda pid, who, color='#1F3550': P(pid, 'styPocket', on={'actor': who, 'joint': 'torso', 'offset': [0.118, 0.205, 0.226]}, opts={'w': 0.2, 'h': 0.19, 'color': color})
def POCKET(pid, who, kind, keys=None, **o):
    return P(pid, 'styPen', on={'actor': who, 'joint': 'torso', 'offset': POCK_S if kind == 'state' else POCK_R}, opts={**(PEN_STATE if kind == 'state' else PEN_RED), **o}, keys=keys or [])
def pen_at(tip, up, grip=0.13):
    """the pen's centre, its rot and the grip point for a tip and an axis direction (toward the cap)"""
    u = unit3(up); C = [r(tip[i] + u[i] * PL / 2) for i in range(3)]; G = [r(tip[i] + u[i] * grip) for i in range(3)]
    return C, aim_rot(C, tip), G
def ROT(a): return [r(a[0], 4), r(math.radians(a[1]), 4), r(a[2], 4)]
CHAINT = lambda pen, until=None, frm=None, anchor=None: {k_: v for k_, v in {'a': {'point': anchor}, 'b': {'prop': pen, 'offset': RING}, 'color': '#9AA2AC', 'sag': 0.12, 'radius': 0.014, 'minPx': 4, 'rim': 0.6, 'rimColor': '#101216', 'n': 14,
                                                    'until': until, 'from': frm}.items() if v is not None}

# ============================== the town hall (mairie set without its banner, map or flag) and the counter at the origin
MAIRIE = {'banner': False, 'map': False, 'flagX': 40, 'desk': False, 'wall': '#E9E2D2', 'band': '#9C7A56', 'clockX': -3.0}
CNT = [0.0, 0, 0.0]; CH = 1.05
ANCHOR = [0.3, r(CH + 0.045), 0.16]                                         # the eyebolt's ring (counter at the origin)
CLERK = [-0.05, 0, -0.75]

# 1: the hook. From behind the counter at its height: he signs with the brass pen chained to the eyebolt (quick scribbles), lifts it absently to his
#    chest: (round 1) the chain hangs from the raised pen, goes taut, two tugs hold it trembling while his eyes stay in the middle distance; it snaps
#    with a pop (shock lines, the pen and hand jolt up and overshoot), the cut end whips back down to the counter; he clips the pen into his pocket
D1 = st.dur('S01'); LIFT1 = 0.4; TAUT1 = 0.52; SNAP1 = 0.78; CLIP1 = 1.12
HERO1 = [0.05, 0, 0.74]
UP1 = [0.18, 1.0, 0.55]
W1 = [[0.14, 1.108, 0.1], [0.2, 1.108, 0.12], [0.13, 1.108, 0.14], [0.21, 1.108, 0.16], [0.15, 1.108, 0.17]]
PEN1 = [pen_at(w, UP1) for w in W1]
LIFT1C, LIFT1R, LIFT1G = pen_at([0.12, 1.5, 0.42], [0.08, 1.0, 0.3])
TUG1 = [pen_at([0.12, 1.5 + d, 0.42 + d * 0.3], [0.08, 1.0, 0.3]) for d in (0.05, 0.0, 0.06, 0.0, 0.14, 0.1)]
PK1 = [-0.03, 1.5, 0.53]                                                  # the pocket, world (he faces -Z: his left is -X)
PK1C, PK1R, PK1G = pen_at(add(PK1, [0, -0.21, 0]), [0, 1, 0], grip=0.33)
RING1 = add(LIFT1C, [0.02, 0.24, 0.06])
C1 = FC('S01', 0.0, [-0.55, 1.3, -1.35], {'headTop': [HERO1[0], 2.36, HERO1[2]], 'reg': [0.15, 1.1, 0.12], 'anchor': ANCHOR, 'lift': add(LIFT1C, [0, 0.35, 0]), 'pocket': PK1, 'chin': [HERO1[0], 1.75, HERO1[2]]}, top=0.07, bottom=0.74, drift=(0.05, 0.0, 0.1))
FW1 = {'lid': 0.55, 'mouth': 'line', 'gy': 0.8}
FAR1 = {'lid': 0.5, 'mouth': 'line', 'gx': 0.7, 'gy': -0.2, 'brow': 0.1}
HR = lambda g, f, extra=None: {'reach': {'R': R5(g, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': f, 'hip': 0, **(extra or {})}
TT1 = [0.58, 0.62, 0.68, 0.72, r(SNAP1 + 0.04), r(SNAP1 + 0.12)]
KEYS1 = [k(0.0, look=[0.15, 1.1, 0.14]), k(0.0, toon=HR(PEN1[0][2], FW1, {'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1, None]}}), toonDur=0.0),
         *[k(r(0.05 + 0.08 * i), toon=HR(PEN1[i][2], FW1, {'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1, None]}}), toonDur=0.07, toonEase='inOut') for i in range(1, 5)],
         k(LIFT1, toon=HR(LIFT1G, FAR1, {'bend': {'spine': [0.02, 0, 0, 1, None]}}), toonDur=TAUT1 - LIFT1, toonEase='out'),
         k(LIFT1, look=[-1.6, 1.95, 2.6], lookDur=0.2),
         *[k(t, toon=HR(TUG1[i][2], FAR1 if i < 4 else {**FAR1, 'brow': 0.4, 'lid': 0.35}, {'sq': [1.0, 1.03, 1.0] if i in (0, 2, 4) else [1, 1, 1]}), toonDur=0.04 if i in (0, 2, 4) else 0.05, toonEase='out' if i == 4 else 'inOut') for i, t in enumerate(TT1)],
         k(0.92, toon=HR(PK1G, {'lid': 0.5, 'mouth': 'smirk', 'gx': 0.6}), toonDur=0.2, toonEase='inOut'),
         k(r(CLIP1 + 0.04), toon={'face': {'lid': 0.45, 'mouth': 'smirk', 'gx': 0.5}, 'hip': 0}, toonDur=0.12)]
PENK1 = [*[k(r(0.05 + 0.08 * i), to=PEN1[i][0], dur=0.07, ease='inOut') for i in range(1, 5)], *[k(r(0.05 + 0.08 * i), rotTo=ROT(PEN1[i][1]), dur=0.07) for i in range(1, 5)],
         k(LIFT1, to=LIFT1C, dur=TAUT1 - LIFT1, ease='out'), k(LIFT1, rotTo=ROT(LIFT1R), dur=TAUT1 - LIFT1),
         *[k(t, to=TUG1[i][0], dur=0.04 if i in (0, 2, 4) else 0.05, ease='out' if i == 4 else 'inOut') for i, t in enumerate(TT1)],
         k(0.92, to=PK1C, dur=0.2, ease='inOut'), k(0.92, rotTo=ROT(PK1R), dur=0.2), k(CLIP1, visible=False)]
st.shot('S01', 'mairie', setOpts=MAIRIE, actors=[act('mec', HERO1, 180, 'stand', 'neutral', keys=KEYS1)],
        props=[P('guichet', 'styCounter', pos=CNT, opts={'cutAt': r(SNAP1 + 0.14), 'swing': [[r(SNAP1 + 0.14), 0.8]]}),
               P('registre1', 'register', pos=[0.15, CH + 0.005, 0.1], ry=180, rot=[-1.25, 0, 0], opts={'left': 'REGISTRE', 'right': 'SIGNATURES', 'w': 0.5, 'h': 0.34}),
               P('stylo1', 'styPen', pos=PEN1[0][0], ry=PEN1[0][1][1], rot=[PEN1[0][1][0], 0, PEN1[0][1][2]], opts=PEN_STATE, keys=PENK1),
               P('pop1', 'burstLines', pos=RING1, face='camera', opts={'at': SNAP1, 'n': 9, 'r0': 0.06, 'r1': 0.3, 'len': 0.1, 'w': 0.018, 'dur': 0.22}),
               POCKET('poche1s', 'mec', 'state', keys=[k(0.0, visible=False), k(CLIP1, visible=True)]), POCKET('poche1r', 'mec', 'red'), PATCH('patch1', 'mec')],
        tethers=[{**CHAINT('stylo1', anchor=ANCHOR), 'sag': [[0.0, 0.16], [LIFT1, 0.3], [TAUT1, 0.0]], 'wobble': [[TT1[0], 0.025, 46, 7], [TT1[2], 0.03, 46, 7]], 'snap': [SNAP1, 0.16, 0.35]}],
        cams=[C1])
st.cue('sfx:scratch', 'S01', 0.05, 0.25); st.cue('sfx:stretch', 'S01', TAUT1, 0.25); st.cue('sfx:twang', 'S01', r(SNAP1 - 0.02), 0.3); st.cue('pop', 'S01', SNAP1, 0.5); st.cue('sfx:rattleShort', 'S01', r(SNAP1 + 0.08), 0.3); st.cue('sfx:click', 'S01', CLIP1, 0.4)

# 2: low at the counter's public side: the cut chain swings over the edge beside the ÉTAT tag in the foreground while he strolls off toward the
#    door, deadpan, the brass and the red pens in his breast pocket
D2 = st.dur('S02'); SW2 = r(SNAP1 + 0.14 - D1)
HERO2a, HERO2b = [0.05, 0, 0.95], [-0.35, 0, 2.0]
C2 = FC('S02', 0.0, [1.2, 1.15, 4.6], {'chainBot': [0.3, 0.72, 0.42], 'tag': [0.42, 0.92, 0.4], 'head0': [HERO2a[0], 2.36, HERO2a[2]], 'head1': [HERO2b[0], 2.36, HERO2b[2]], 'feet1': [HERO2b[0], 0.3, HERO2b[2]]}, top=0.08, bottom=0.74, lenses=range(26, 76), drift=(0.0, 0.0, -0.1))
st.shot('S02', 'mairie', setOpts=MAIRIE, actors=[act('mec', HERO2a, -20, 'stand', 'neutral', keys=[k(0.0, to=HERO2b, dur=D2, clip='walk', ease='linear', face=-20), k(0.0, look='camera'),
            k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.0), k(0.55, toon={'face': {'lid': 0.45, 'mouth': 'whistle'}}, toonDur=0.1)])],
        props=[P('guichet', 'styCounter', pos=CNT, opts={'cutAt': -1, 'swing': [[SW2, 0.6]], 'tagSwing': [[SW2, 0.25]], 'tagS': 1.9}), P('registre2', 'register', pos=[0.15, CH + 0.005, 0.1], ry=180, rot=[-1.25, 0, 0], opts={'left': 'REGISTRE', 'right': 'SIGNATURES', 'w': 0.5, 'h': 0.34}),
               POCKET('poche2s', 'mec', 'state'), POCKET('poche2r', 'mec', 'red'), PATCH('patch2', 'mec')],
        cams=[C2])
st.cue('sfx:step', 'S02', 0.1, 0.2); st.cue('sfx:whistle', 'S02', 0.5, 0.25)

# 3: the only pen of the State. The counter top from the public side: a clean pen outline in the grey dust, the cut chain still swinging, the ÉTAT
#    tag; behind, the clerk frozen in a take (eyes wide, a slow blink, her pupils trembling); a slow push-in
D3 = st.dur('S03'); SW3 = r(SW2 - D2)
C3F, C3T = [0.6, 1.55, 2.3], [0.5, 1.52, 1.95]
C3 = FC('S03', 0.0, C3F, {'dustL': [-0.25, CH, 0.0], 'dustR': [0.35, CH, 0.2], 'tag': [0.42, 0.86, 0.4], 'clerkTop': [CLERK[0], 2.72, CLERK[2]], 'clerkChin': [CLERK[0], 1.75, CLERK[2]]}, top=0.07, bottom=0.74, lenses=range(26, 76), drift=sub(C3T, C3F))
FCL = {'lid': 0.0, 'mouth': 'O', 'brow': 0.8, 'eye': 0.2, 'pupilSize': -0.4}
# (round 1) a real take: anticipation squash, eyes out on stalks, head stretched tall, jaw down, hair up, a trembling hold, a settle with overshoot
TK3 = {'pop': 0.65, 'popLen': 0.24, 'brow': 1, 'jaw': 0.6, 'mouth': 'O', 'lid': 0.0, 'pupilSize': -0.3, 'eyePitch': 0.35}
K3 = lambda f, sq=None, hd=None, extra=None: {'face': f, 'hip': 0, 'auto': 0.0, **({'sq': sq} if sq else {}), **({'scl': {'head': hd}} if hd else {}), **(extra or {})}
KEYS3 = [k(0.0, look=[0.1, CH, 0.1]), k(0.0, toon=K3({'lid': 0.3, 'mouth': 'line', 'gy': 0.6}), toonDur=0.0),
         k(0.1, toon=K3({'lid': 0.6, 'mouth': 'line', 'gy': 0.7, 'brow': -0.3}, [1.08, 0.9, 1.08], [1.1, 0.88, 1.1]), toonDur=0.06, toonEase='in'),
         k(0.18, toon=K3(TK3, [0.88, 1.16, 0.88], [0.8, 1.34, 0.8], {'hairUp': 0.9}), toonDur=0.05, toonEase='outBack'),
         *[k(r(0.26 + 0.06 * i), toon=K3({**TK3, 'pupilShake': 1, 'jaw': 0.55 + 0.08 * (i % 2)}, [0.9 + 0.02 * (i % 2), 1.14 - 0.03 * (i % 2), 0.9 + 0.02 * (i % 2)], [0.82 + 0.03 * (i % 2), 1.3 - 0.04 * (i % 2), 0.82 + 0.03 * (i % 2)], {'hairUp': 0.8}), toonDur=0.05) for i in range(10)],
         k(0.9, toon=K3({'lid': 0.0, 'mouth': 'o', 'brow': 0.7, 'eye': 0.25, 'pupilSize': -0.5}, [1.07, 0.93, 1.07], [1.08, 0.92, 1.08], {'hairUp': 0.3}), toonDur=0.07, toonEase='in'),
         k(1.0, toon=K3({'lid': 0.0, 'mouth': 'wavy', 'brow': 0.7, 'eye': 0.25, 'pupilSize': -0.5, 'pupilShake': 1}, [0.98, 1.02, 0.98], [0.98, 1.03, 0.98]), toonDur=0.08),
         k(1.12, toon=K3({'lid': 0.0, 'mouth': 'wavy', 'brow': 0.7, 'eye': 0.25, 'pupilSize': -0.5}), toonDur=0.08), k(1.2, look='camera', lookDur=0.15)]
st.shot('S03', 'mairie', setOpts=MAIRIE, actors=[act('greffiere', CLERK, 0, 'stand', 'surprised', keys=KEYS3)],
        props=[P('guichet', 'styCounter', pos=CNT, opts={'cutAt': -1, 'swing': [[SW3, 0.6]], 'tagSwing': [[SW3, 0.25]], 'dust': [0.05, 0.08, -0.15]})],
        cams=[C3])
st.cue('sfx:tense', 'S03', 0.0, 0.2); st.cue('sfx:boing', 'S03', 0.18, 0.4); st.cue('sfx:rattleShort', 'S03', 0.3, 0.15); st.cue('sfx:gulp', 'S03', 1.0, 0.3)

# ============================== the office: three desks, towers of files from each desk to the ceiling (3.0 m)
OFF = {**MAIRIE}
DESKS = [[-1.45, 0, -1.2], [1.35, 0, -0.75], [0.05, 0, -2.0]]
TOW4 = lambda d, ph: [[d[0] - 0.42, d[2] + 0.05, ph], [d[0] + 0.1, d[2] - 0.1, ph + 0.04], [d[0] + 0.55, d[2] + 0.08, ph + 0.08]]
# 4: the files piled up. (round 2) Low and close beside the clerk's desk: his own towers shoot up beside him into the ceiling at the top of the frame, the
#    other desks' towers follow in a wave behind; his eyes, then his head, tilt up with his tower, mouth open, a little squash as it hits the ceiling
D4 = st.dur('S04')
CLERK2 = [1.0, 0.02, -1.38]
TOWC = [[1.62, -0.82, 0.0], [2.02, -0.66, 0.05]]
C4 = FC('S04', 0.0, [0.25, 0.85, 1.25], {'clerkTop': [CLERK2[0], 1.95, CLERK2[2]], 'clerkChin': [CLERK2[0], 1.3, CLERK2[2]], 'towTop': [1.82, 3.0, -0.75], 'towFoot': [1.82, 0.8, -0.75], 'backTow': [-0.3, 3.0, -2.0]}, top=0.04, bottom=0.74, lenses=range(30, 86), drift=(0.0, -0.03, -0.08))
GROW = [[0, 0.06], [0.12, 1.0]]
UPK = lambda t, h, f, sq=None: [k(t, look=[1.75, h, -0.75], lookDur=0.12), k(t, toon={'face': f, 'bend': {'neck': [-0.25 * (h - 1.5) / 1.5, 0, 0, 1, None]}, 'hip': 0, **({'sq': sq} if sq else {})}, toonDur=0.12)]
st.shot('S04', 'mairie', setOpts=OFF, actors=[act('commis', CLERK2, 15, 'sit', 'neutral', keys=[k(0.0, look=[1.75, 1.3, -0.75]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line', 'gx': -0.4}, 'hip': 0}, toonDur=0.0),
            *UPK(0.08, 1.8, {'lid': 0.1, 'mouth': 'o', 'brow': 0.5, 'gx': -0.5, 'gy': -0.5}), *UPK(0.22, 2.5, {'lid': 0.0, 'mouth': 'O', 'brow': 0.8, 'gx': -0.4, 'gy': -0.9}, [0.96, 1.05, 0.96]),
            *UPK(0.38, 3.0, {'lid': 0.0, 'mouth': 'O', 'jaw': 0.4, 'brow': 1.0, 'gx': -0.3, 'gy': -1.0}, [0.94, 1.07, 0.94]), *UPK(0.52, 3.0, {'lid': 0.1, 'mouth': 'o', 'brow': 0.8, 'gx': -0.3, 'gy': -1.0}, [1.05, 0.95, 1.05]),
            k(0.85, look='camera', lookDur=0.15), k(0.85, toon={'face': {'lid': 0.55, 'mouth': 'wavy', 'brow': -0.3}, 'hip': 0}, toonDur=0.15), *blink(1.05, {'lid': 0.55, 'mouth': 'wavy', 'brow': -0.3})])],
        props=[*[P(f'bureau4{i}', 'desk', pos=d, ry=180 if i == 1 else 0, opts={'color': '#7A5A3C', 'top': '#9C7A56'}) for i, d in enumerate(DESKS)], P('chaise4', 'chair', pos=[CLERK2[0], 0, CLERK2[2] - 0.2], ry=0, opts={'color': '#4A3A2A'}),
               P('dossiers4c', 'styFiles', pos=[0, 0.76, 0], opts={'towers': TOWC, 'ceil': 2.24, 'grow': GROW, 'blend': 0.3, 'ceiling': True, 'ceilW': 10, 'ceilD': 9, 'ceilZ': 0.5, 'ceilColor': '#F3E6CC', 'ceilGlow': '#6A5A40'}),
               *[P(f'dossiers4{i}', 'styFiles', pos=[0, 0.76, 0], opts={'towers': TOW4(d, 0.1 + 0.08 * i), 'ceil': 2.24, 'grow': GROW, 'blend': 0.3, 'ceiling': False}) for i, d in enumerate(DESKS) if i != 1]],
        cams=[C4])
for i in range(3): st.cue('sfx:files', 'S04', r(0.12 + 0.12 * i), 0.35)
st.cue('thud', 'S04', 0.65, 0.35)

# 5: up to the ceiling. Medium: two towers pressed against the ceiling, trembling; the clerk of shot 3 slides into the gap between them, squeezed,
#    holding up the empty chain by its ÉTAT tag end; she looks at us
D5 = st.dur('S05')
CL5a, CL5b = [-0.02, 0, -1.25], [-0.02, 0, -0.62]
C5 = FC('S05', 0.0, [0.35, 1.85, 2.25], {'headTop': [0, 2.4, CL5b[2]], 'chain': [-0.28, 1.45, -0.4], 'towL': [-0.7, 2.95, -0.62], 'towR': [0.7, 2.95, -0.62], 'chin': [0, 1.7, CL5b[2]]}, top=0.06, bottom=0.72, drift=(0.0, 0.0, -0.12))
HCH5 = R5([-0.24, 2.3, -0.28], 1, 0.06)
# (round 1) squashed between the towers: half her width, taller, her head pinched, cheeks puffed; she breathes in (thinner still), the towers shudder
SQ5 = lambda i, f: {'reach': {'R': R5(add(HCH5[:3], [0, 0.03 * i, 0]), 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': f, 'sq': [0.5 - 0.06 * i, 1.1 + 0.05 * i, 1.0], 'scl': {'head': [0.68 - 0.06 * i, 1.14 + 0.06 * i, 0.95]}, 'hip': 0, 'auto': 0.0}
st.shot('S05', 'mairie', setOpts=OFF, actors=[act('greffiere', CL5a, 0, 'stand', 'neutral', keys=[k(0.0, to=CL5b, dur=0.25, ease='out', glide=True, face=0), k(0.0, look='camera'),
            k(0.0, toon=SQ5(0, {'lid': 0.4, 'mouth': 'kiss', 'brow': -0.2, 'puff': 0.6, 'cheeks': 1}), toonDur=0.0),
            k(0.22, toon=SQ5(0, {'lid': 0.0, 'mouth': 'kiss', 'brow': 0.6, 'eye': 0.3, 'puff': 0.8, 'cheeks': 1}), toonDur=0.05, toonEase='outBack'),
            k(0.45, toon=SQ5(1, {'lid': 0.0, 'mouth': 'kiss', 'brow': 0.8, 'eye': 0.35, 'puff': 1, 'cheeks': 1, 'pupilShake': 1}), toonDur=0.12, toonEase='inOut'),
            k(0.72, toon=SQ5(0, {'lid': 0.55, 'mouth': 'wavy', 'brow': -0.3, 'puff': 0.4}), toonDur=0.12), *blink(0.86, {'lid': 0.55, 'mouth': 'wavy', 'brow': -0.3, 'puff': 0.4})])],
        props=[P('dossiers5', 'styFiles', pos=[0, 0, 0], opts={'towers': [[-0.38, -0.6, 0], [0.38, -0.62, 0], [-1.25, -1.4, 0], [1.3, -1.5, 0]], 'ceil': 3.0, 'grow': [[-1, 1.0]], 'ceiling': True, 'ceilW': 10, 'ceilD': 9, 'ceilZ': 0.5},
                 keys=[k(0.45, squash=[1.02, 0.99, 1.0], dur=0.08), k(0.53, squash=[0.99, 1.005, 1.0], dur=0.08), k(0.61, squash=[1.0, 1.0, 1.0], dur=0.1)]),
               P('chaine5', 'styChain', on={'actor': 'greffiere', 'hand': 'R', 'offset': [0.0, -0.06, 0.02], 'hang': True}, opts={'len': 0.22, 'tagS': 1.3, 'swing': [[0.25, 0.45]]})],
        cams=[C5])
st.cue('sfx:squeak', 'S05', 0.05, 0.25); st.cue('sfx:stretch', 'S05', 0.45, 0.3); st.cue('sfx:rattleShort', 'S05', 0.3, 0.3)

# ============================== the wedding hall (the mairie with its desk)
WED = {**{k_: v for k_, v in MAIRIE.items() if k_ != 'desk'}, 'deskZ': -0.9, 'plate': 'MARIAGES', 'wall': '#EDE6D6'}
MAYOR = [0.0, 0, -1.62]
BOOK = [-0.22, 0.82, -0.82]   # (round 2) on his right side: the slap no longer crosses the chain arm, the sign clear of the groom
# 6: weddings suspended. Frontal medium: the mayor behind the desk (sash in invented violet and gold) holds up the empty chain, slaps the open register shut
#    and a SUSPENDU sign drops onto it, swinging; bride and groom flank the desk in a V, turn to each other, then to us
D6 = st.dur('S06'); SHUT6 = 0.8; SIGN6 = 1.02
BRIDE, GROOM = [-1.02, 0, -0.42], [0.86, 0, -0.45]
C6 = FC('S06', 0.0, [0.15, 1.7, 3.6], {'mayorTop': [0, 2.42, MAYOR[2]], 'brideFace': [BRIDE[0] - 0.12, 2.05, BRIDE[2]], 'groomFace': [GROOM[0] + 0.12, 2.1, GROOM[2]], 'book': add(BOOK, [0, 0.0, 0]), 'sign': add(BOOK, [0, 0.2, 0.04]), 'chain': [0.55, 1.45, -1.45]}, top=0.07, bottom=0.74, lenses=range(26, 76), drift=(0, 0, -0.15))
HL6 = R5([0.5, 2.05, -1.4], 1, 0.06)
MK = lambda f, rr=None, extra=None: {'reach': {'L': HL6, **({'R': rr} if rr else {})}, 'hands': {'L': 'pinch', **({'R': 'open'} if rr else {})}, 'face': f, **(extra or {})}
KEYS6 = [k(0.0, look='camera'), k(0.0, toon=MK({'lid': 0.45, 'mouth': 'line', 'brow': -0.2}), toonDur=0.0),
         k(0.3, toon=MK({'lid': 0.5, 'mouth': 'wavy', 'brow': -0.4}, extra={'sq': [0.98, 1.03, 0.98]}), toonDur=0.15),
         k(0.62, toon=MK({'lid': 0.5, 'mouth': 'clench', 'brow': -0.6}, R5([-0.45, 1.55, -1.1], 1, 0.06), {'bend': {'spine': [0.1, 0, 0, 1, None]}}), toonDur=0.12, toonEase='out'),
         k(SHUT6, toon=MK({'lid': 0.6, 'mouth': 'clench', 'brow': -0.6}, R5([-0.32, 1.24, -0.8], 1, 0.06), {'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04]}), toonDur=0.07, toonEase='in'),
         k(1.15, toon=MK({'lid': 0.45, 'mouth': 'line', 'brow': -0.2}, extra={'bend': {'spine': [0.0, 0, 0, 1, None]}}), toonDur=0.2)]
def COUPLE(who, ry0, f0, f1):
    p, dt = (BRIDE, 0.0) if who == 'mariee' else (GROOM, 0.1)
    other = GROOM if who == 'mariee' else BRIDE
    return act(who, p, ry0, 'stand', 'neutral', keys=[k(0.0, look=[0, 1.95, MAYOR[2]]), k(0.0, toon={'face': f0}, toonDur=0.0),
            k(r(SHUT6 + 0.05), toon={'face': {**f0, 'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, 'sq': [1.06, 0.93, 1.06]}, toonDur=0.04), k(r(SHUT6 + 0.2), toon={'face': {**f0, 'lid': 0.0, 'mouth': 'o', 'brow': 0.6}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.08),
            # (round 2) clear beats: each turns to the other (head and body), then both turn to us
            k(r(1.12 + dt), to=p, dur=0.12, glide=True, face=r(yaw(p, other))), k(r(1.12 + dt), look=[other[0], 2.0, other[2]], lookDur=0.08),
            k(r(1.48 + dt), to=p, dur=0.12, glide=True, face=r(ry0 * 0.4)), k(r(1.48 + dt), look='camera', lookDur=0.1), k(r(1.48 + dt), toon={'face': f1}, toonDur=0.1)])
st.shot('S06', 'mairie', setOpts=WED, actors=[LIFE(act('maire', MAYOR, 0, 'stand', 'neutral', keys=KEYS6), D6, t0=1.4, breath=False),
        COUPLE('mariee', 55, {'lid': 0.2, 'mouth': 'smile', 'brow': 0.3}, {'lid': 0.5, 'mouth': 'wavy', 'brow': -0.3}), COUPLE('marie', -55, {'lid': 0.3, 'mouth': 'smile'}, {'lid': 0.55, 'mouth': 'line', 'brow': -0.2})],
        props=[P('registre6', 'register', pos=BOOK, opts={'left': 'REGISTRE', 'right': 'MARIAGES'}, keys=[k(SHUT6, visible=False)]),
               P('livre6', 'styNotice', pos=add(BOOK, [0, 0.21, 0]), opts={'text': 'REGISTRE', 'w': 0.3, 'h': 0.4, 'bg': '#8E1F24', 'fg': '#E8C766', 'border': '#5A1014'}, keys=[k(0.0, visible=False), k(SHUT6, visible=True), k(SHUT6, squash=[1.08, 0.92, 1.0], dur=0.12)]),
               P('suspendu6', 'styNotice', pos=add(BOOK, [0.0, 0.43, 0.04]), opts={'text': 'SUSPENDU', 'w': 0.72, 'h': 0.28, 'string': True, 'stringH': 0.08, 'popAt': SIGN6, 'swing': [[SIGN6, 0.35]]}),
               P('chaine6', 'styChain', on={'actor': 'maire', 'hand': 'L', 'offset': [0.0, -0.06, 0.02], 'hang': True}, opts={'len': 0.4, 'tagS': 1.2, 'swing': [[0.1, 0.3], [0.62, 0.3]]}),
               P('voile6', 'bridalVeil', on={'actor': 'mariee', 'joint': 'head', 'offset': [0, 0.5, -0.02]}, opts={'len': 0.8})],
        cams=[C6])
st.cue('sfx:rattleShort', 'S06', 0.1, 0.3); st.cue('thud', 'S06', SHUT6, 0.55); st.cue('sfx:pop', 'S06', SIGN6, 0.35); st.cue('sfx:gasp', 'S06', r(SHUT6 + 0.08), 0.2)

# ============================== the maternity corridor (whiteVoid + styCorridor at z 0, the door at x 0, the bench along the wall to the right)
CORR = {'color': '#DDE7E3'}
BENCH = [1.95, 0, 0.36]
FATHERS = [('pere1', 1.35, 0.55), ('pere2', 1.95, 0.65), ('pere3', 2.55, 0.75)]
NURSE = [-0.62, 0, 0.55]
# 7: births put off to Monday. Low dolly along the bench: the nurse slaps a big LUNDI sign on the maternity door; the three expectant fathers, up on
#    their feet, sink back onto the bench one after the other; card REPORTÉ (their heads stay under the card band)
D7 = st.dur('S07'); SLAP7 = 0.42
C7F, C7T = [3.0, 0.7, 5.2], [2.7, 0.7, 5.0]
C7 = FC('S07', 0.0, C7F, {'sign': [0.0, 1.2, 0.13], 'doorTop': [0.0, 2.6, 0.1], 'nurseTop': [NURSE[0], 2.3, NURSE[2]], 'p3top': [2.55, 2.3, 0.75], 'p1top': [1.35, 2.3, 0.55], 'bench': [3.0, 0.4, 0.4]}, top=0.22, bottom=0.74, lenses=range(30, 76), drift=sub(C7T, C7F))
def FATHER(who, x, t_sit, preset_face):
    z = 0.55 if who == 'pere1' else (0.62 if who == 'pere2' else 0.68)
    return act(who, [x, 0, r(z + 0.35)], 180 + (15 if x > 2 else -10), 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.5, 0.2]), k(0.0, toon={'face': {'lid': 0.0, 'mouth': 'smile', 'brow': 0.7}}, toonDur=0.0),
        k(r(SLAP7 + 0.05), toon={'face': {'lid': 0.3, 'mouth': 'o', 'brow': 0.3}, 'sq': [1.04, 0.96, 1.04]}, toonDur=0.08),
        k(t_sit, to=[x, 0.0, BENCH[2]], dur=0.3, ease='inOut', clip='sit', glide=True, face=0), k(r(t_sit + 0.3), clip='sit'), k(r(t_sit + 0.05), look='camera', lookDur=0.25),
        k(r(t_sit + 0.1), toon={'face': preset_face, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.2)])
st.shot('S07', 'whiteVoid', setOpts=CORR, actors=[
        LIFE(act('infirmiere', NURSE, 120, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.3, 0.1]), k(0.0, toon={'reach': {'L': R5([-0.2, 1.3, 0.2], 1, 0.06), 'R': R5([-0.25, 1.05, 0.2], 1, 0.06)}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.0),
            k(r(SLAP7 - 0.1), toon={'reach': {'L': R5([0.0, 1.25, 0.13], 1, 0.06), 'R': R5([0.12, 1.12, 0.13], 1, 0.06)}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.5, 'mouth': 'clench'}}, toonDur=0.1, toonEase='in'),
            k(0.85, toon={'reach': {'L': R5([-0.3, 1.0, 0.45], 1, 0.06)}, 'hands': {'L': 'open'}, 'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.2), k(0.9, look='camera', lookDur=0.2)]), D7, t0=1.25, breath=False),
        FATHER('pere1', 1.35, 0.7, {'lid': 0.6, 'mouth': 'wavy', 'brow': -0.3}), FATHER('pere2', 1.95, 0.82, {'lid': 0.65, 'mouth': 'line', 'brow': -0.4}), FATHER('pere3', 2.55, 0.94, {'lid': 0.6, 'mouth': 'grimace', 'brow': -0.2})],
        props=[P('couloir7', 'styCorridor', pos=[0, 0, 0], opts={'w': 9, 'doorX': 0.0}), P('banc7', 'bench', pos=BENCH, opts={'w': 2.2}),
               P('lundi7', 'styNotice', pos=[0.0, 1.2, 0.135], opts={'text': 'LUNDI', 'w': 0.74, 'h': 0.32, 'tape': True, 'popAt': r(SLAP7 - 0.02), 'slap': [SLAP7], 'fg': '#C8202A'})],
        cams=[C7])
st.card('S07', 'REPORTÉ', at=r(st.at('S07', 'L05', 2) + 0.02))
st.cue('thud', 'S07', SLAP7, 0.45); st.cue('sfx:zip', 'S07', r(SLAP7 + 0.05), 0.2); st.cue('sfx:slideDown', 'S07', 0.72, 0.2)

# ============================== the news studio (whiteVoid + styStudio at the origin)
STUDIO = {'color': '#16233A'}
ANCHOR_T = [-0.7, 0, -0.95]
STUD = lambda flip, topple: P('studio', 'styStudio', pos=[0, 0, 0], opts={'flipAt': flip, 'toppleAt': topple, 'stackX': -0.27, 'countX': 0.38, 'screenY': 2.2, 'screenW': 2.0, 'photoX': 0.42, 'bannerW': 2.0, 'bannerX': -0.2})
# 8: special edition. Frontal medium: the unshaven anchor standing behind the desk, tie askew, under the red ÉDITION SPÉCIALE banner, the photo of the
#    brass pen on the big screen behind him (RECHERCHÉ), the day counter at the right; he speaks to us, worn out
D8 = st.dur('S08')
C8 = FC('S08', 0.0, [0.1, 1.7, 3.9], {'bannerL': [-1.2, 3.15, -1.7], 'bannerR': [0.8, 3.15, -1.7], 'anchorTop': [ANCHOR_T[0], 2.36, ANCHOR_T[2]], 'photoR': [1.42, 2.05, -1.7], 'countR': [0.72, 1.6, -0.55], 'deskL': [-0.95, 1.2, -0.05]}, top=0.06, bottom=0.76, lenses=range(26, 76), drift=(-0.05, 0, -0.3))
# (round 1) a worn-out anchor who still performs: hands chop and spread on the beats, the head bobs and tilts, a squash on each stress
GEST = [([-0.22, 1.05, -0.62], [0.25, 1.05, -0.6], 'open', 'open'), ([-0.3, 1.38, -0.5], [0.22, 1.1, -0.6], 'point', 'open'), ([-0.2, 1.08, -0.6], [0.36, 1.35, -0.5], 'open', 'spread'), ([-0.34, 1.3, -0.52], [0.34, 1.3, -0.52], 'spread', 'spread')]
TALK = lambda t0, t1, f: [k(r(t0 + 0.15 * i), toon={'face': {**f, 'mouth': 'talk' if i % 2 == 0 else 'o', 'brow': f.get('brow', 0) + (0.4 if i % 4 == 1 else 0)}, 'reach': {'R': R5(add([ANCHOR_T[0], 0, 0], GEST[i % 4][0])), 'L': R5(add([ANCHOR_T[0], 0, 0], GEST[i % 4][1]))}, 'hands': {'R': GEST[i % 4][2], 'L': GEST[i % 4][3]},
                                           'bend': {'neck': [0.12 * (i % 2), 0.1 * (1 if i % 4 < 2 else -1), 0, 1, None]}, 'sq': [1.03, 0.97, 1.03] if i % 2 == 0 else [0.99, 1.02, 0.99]}, toonDur=0.08, toonEase='out') for i in range(int((t1 - t0) / 0.15))]
FA = {'lid': 0.62, 'low': 0.3, 'brow': -0.3}
st.shot('S08', 'whiteVoid', setOpts=STUDIO, actors=[LIFE(act('presentateur', ANCHOR_T, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), *TALK(0.05, 1.15, FA)]), D8, t0=0.5, breath=False)],
        props=[STUD(5.0, 9.0)], cams=[C8])
st.cue('sfx:sting', 'S08', 0.0, 0.35)

# 9: eleventh day without a pen. The camera cranes down from high over the desk onto the counter: the number flips from DIX to ONZE (clack), the tall
#    stack of paper beside it topples over the desk, sheets sliding off; the anchor's eyes go to it, deadpan
D9 = st.dur('S09'); FLIP9 = 0.32; TOP9 = 0.72
C9 = CAM('S09', 0.0, [0.75, 3.3, 2.0], [0.0, 1.4, -0.75], 58, {'countR': [0.69, 1.6, -0.55], 'stack': [-0.14, 1.3, -0.35], 'anchorFace': [ANCHOR_T[0] + 0.05, 2.05, ANCHOR_T[2]]}, to=[0.05, 1.85, 1.95], look2=[0.0, 1.55, -0.6], ease='out')
st.shot('S09', 'whiteVoid', setOpts=STUDIO, actors=[act('presentateur', ANCHOR_T, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), *TALK(0.0, 0.6, FA),
            k(r(TOP9 + 0.05), look=[0.3, 1.0, -0.2], lookDur=0.15), k(r(TOP9 + 0.05), toon={'face': {**FA, 'mouth': 'line', 'gx': -0.6, 'gy': 0.5}}, toonDur=0.1), *blink(1.15, {**FA, 'mouth': 'line', 'gx': -0.6, 'gy': 0.5})])],
        props=[STUD(FLIP9, TOP9)], cams=[C9])
st.cue('clack', 'S09', FLIP9, 0.4); st.cue('sfx:paper', 'S09', r(TOP9 + 0.1), 0.4); st.cue('thud', 'S09', r(TOP9 + 0.3), 0.3)

# ============================== the press room: the president at the podium
PRESS = {'backdrop': 'ÉTAT', 'flags': False, 'chairs': False, 'bg': '#2E4563', 'fg': 'rgba(255,255,255,0.3)', 'fontScale': 1.0}
PRES = [0.0, 0, -2.5]
LET10 = [0.52, 2.2, -2.28]; SASH10 = [-0.47, 1.5, -2.2]
# 10: the president wanted to resign. Low from the press seats: at the podium he holds a DÉMISSION letter high beside his head (an empty SIGNATURE line)
#     and his sash, taken off, dangling from the other hand; flashes pop in the foreground
D10 = st.dur('S10')
C10 = FC('S10', 0.0, [0.45, 0.95, 2.3], {'presTop': [0, 2.4, PRES[2]], 'letterTop': add(LET10, [0, 0.33, 0]), 'letterR': add(LET10, [0.26, 0, 0]), 'sashBot': add(SASH10, [0, -0.5, 0]), 'sashL': add(SASH10, [-0.1, 0, 0]), 'podium': [0, 1.0, -2.0]}, top=0.07, bottom=0.72, lenses=range(26, 76), drift=(0.0, 0.05, -0.2))
FP = {'lid': 0.4, 'mouth': 'line', 'brow': 0.3}
PK10 = lambda f, sq=None: {'reach': {'L': R5(add(LET10, [0.0, -0.26, -0.02]), 1, 0.06), 'R': R5(add(SASH10, [0, 0.42, 0]), 1, 0.06)}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': f, 'hip': 0, **({'sq': sq} if sq else {})}
st.shot('S10', 'pressRoom', setOpts=PRESS, actors=[LIFE(act('president', PRES, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=PK10(FP), toonDur=0.0),
            k(0.4, toon=PK10({**FP, 'brow': 0.5, 'mouth': 'smile'}, [0.97, 1.04, 0.97]), toonDur=0.2),
            # (round 2) a smug little shake of the letter on the beat (the hand follows it), a chin lift, a weight shift
            *[k(r(0.62 + 0.07 * i), toon={**PK10({**FP, 'mouth': 'smile', 'brow': 0.6, 'lid': 0.55}, [0.98, 1.03, 0.98]), 'reach': {'L': R5(add(LET10, [0.03 * (1 if i % 2 else -1), -0.22, -0.02]), 1, 0.06), 'R': R5(add(SASH10, [0, 0.42, 0]), 1, 0.06)}, 'bend': {'neck': [-0.12, 0.08, 0, 1, None]}}, toonDur=0.05) for i in range(5)],
            k(1.1, toon={**PK10({**FP, 'mouth': 'smirk', 'brow': 0.4}), 'hip': 0.9}, toonDur=0.3, toonEase='inOut'), k(1.5, toon={**PK10({**FP, 'mouth': 'smirk', 'brow': 0.5}), 'hip': 0.9, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.25)]), D10, t0=0.95, breath=False)],
        props=[P('lettre10', 'styLetter', pos=LET10, keys=[k(0.4, to=add(LET10, [0, 0.04, 0]), dur=0.2), *[k(r(0.62 + 0.07 * i), to=add(LET10, [0.03 * (1 if i % 2 else -1), 0.04, 0]), dur=0.05) for i in range(5)], *[k(r(0.62 + 0.07 * i), rotTo=[0, 0, 0.1 * (1 if i % 2 else -1) * (0 if i == 4 else 1)], dur=0.05) for i in range(5)]]), P('echarpe10', 'stySash', pos=SASH10, rot=[0, 0, 0.08]),
               P('flash10', 'flashBursts', pos=[0.35, 1.75, -1.3], face='camera', opts={'n': 5, 'w': 2.0, 'h': 0.9, 'at': [0.2, 0.55, 0.9, 1.25, 1.6], 'life': 0.15})],
        cams=[C10])
for t in [0.2, 0.55, 0.9, 1.25, 1.6]: st.cue('sfx:shutter', 'S10', t, 0.3)

# 11: impossible: he had to sign. Medium at the podium: a minister at the right holds out the empty chain (its ÉTAT tag, nothing at the end); the
#     president's eyes go to it, he lowers the letter; another minister at the left lowers the sash back over his head onto his chest; he sags
D11 = st.dur('S11'); LOW11 = 0.72; SASH11 = (1.08, 1.26)
MIN1, MIN2 = [0.92, 0, -2.15], [-0.95, 0, -2.45]
C11 = FC('S11', 0.0, [0.2, 1.75, 1.4], {'presTop': [0, 2.45, PRES[2]], 'min1Top': [MIN1[0], 2.4, MIN1[2]], 'min2Top': [MIN2[0], 2.4, MIN2[2]], 'sashHi': [-0.72, 2.1, -2.25], 'chain': [0.5, 1.45, -2.05], 'podium': [0, 1.1, -2.0], 'min1R': [MIN1[0] + 0.3, 1.5, MIN1[2]], 'min2L': [MIN2[0] - 0.3, 1.5, MIN2[2]]}, top=0.06, bottom=0.72, lenses=range(26, 76), drift=(0, 0, -0.1))
LET11a, LET11b = LET10, [0.42, 1.35, -2.18]
SA11a, SA11b, SA11c = [-0.72, 1.6, -2.25], [-0.3, 1.58, -2.24], [0.0, 1.52, -2.3]
PK11 = lambda lp, f, sq=None, extra=None: {'reach': {'L': R5(add(lp, [0.0, -0.26, -0.02]), 1, 0.06)}, 'hands': {'L': 'pinch'}, 'face': f, 'hip': 0, **({'sq': sq} if sq else {}), **(extra or {})}
SAGF = {'lid': 0.75, 'low': 0.3, 'mouth': 'wavy', 'brow': -0.5}
st.shot('S11', 'pressRoom', setOpts=PRESS, actors=[
        act('president2', PRES, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=PK11(LET11a, {**FP, 'mouth': 'smirk'}), toonDur=0.0),
            k(0.18, look=[0.55, 1.5, -2.0], lookDur=0.08),
            # (round 2) not a stalk-eye take: his jaw drops in a block down to the podium, then he melts, sagging slowly
            k(0.16, toon=PK11(LET11a, {'lid': 0.3, 'mouth': 'line', 'brow': 0.2, 'gx': -0.5, 'gy': 0.4}, [1.0, 1.02, 1.0]), toonDur=0.05),
            k(0.24, toon=PK11(LET11a, {'lid': 0.15, 'jaw': 1.0, 'jawLen': 0.72, 'jawBlock': 1, 'mouth': 'O', 'brow': 0.8, 'gx': -0.5, 'gy': 0.4}, [0.98, 1.03, 0.98], {'auto': 0.0}), toonDur=0.08, toonEase='in'),
            k(0.34, toon=PK11(LET11a, {'lid': 0.2, 'jaw': 1.0, 'jawLen': 0.78, 'jawBlock': 1, 'mouth': 'O', 'brow': 0.7, 'gx': -0.5, 'gy': 0.4}, [1.0, 1.0, 1.0], {'auto': 0.0}), toonDur=0.06, toonEase='out'),
            k(0.4, toon=PK11(LET11a, {'lid': 0.3, 'jaw': 1.0, 'jawLen': 0.74, 'jawBlock': 1, 'mouth': 'O', 'brow': 0.6, 'gx': -0.5, 'gy': 0.4}, [1.03, 0.97, 1.03], {'auto': 0.0}), toonDur=0.28, toonEase='inOut'),
            k(0.68, toon=PK11(LET11a, {'lid': 0.5, 'mouth': 'o', 'brow': 0.3, 'gx': -0.4, 'gy': 0.4}, [1.06, 0.94, 1.06]), toonDur=0.1, toonEase='in'),
            k(LOW11, toon=PK11(LET11b, {'lid': 0.5, 'mouth': 'wavy', 'brow': -0.3, 'gy': 0.4}, [1.02, 0.98, 1.02]), toonDur=0.35, toonEase='inOut'),
            k(r(SASH11[1] + 0.02), toon=PK11(LET11b, SAGF, [1.1, 0.88, 1.1], {'bend': {'spine': [0.12, 0, 0, 1, None], 'neck': [0.15, 0, 0, 1, None]}}), toonDur=0.12, toonEase='out'),
            k(1.45, look='camera', lookDur=0.2), *blink(1.62, SAGF)]),
        LIFE(act('ministre1', MIN1, -70, 'stand', 'neutral', keys=[k(0.0, look=[0, 1.95, PRES[2]]), k(0.0, toon={'reach': {'R': R5([0.55, 1.72, -2.0], 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
            k(0.3, toon={'reach': {'R': R5([0.5, 1.78, -2.0], 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.15)]), D11, t0=0.7, breath=False),
        LIFE(act('ministre2', MIN2, 55, 'stand', 'neutral', keys=[k(0.0, look=[0, 2.4, PRES[2]]),
            k(0.0, toon={'reach': {'R': R5(add(SA11a, [-0.12, -0.3, 0.05]), 1, 0.06), 'L': R5(add(SA11a, [0.05, 0.3, 0.05]), 1, 0.06)}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(SASH11[0], toon={'reach': {'R': R5(add(SA11c, [-0.3, -0.15, 0.1]), 1, 0.06), 'L': R5(add(SA11c, [-0.12, 0.3, 0.1]), 1, 0.06)}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=SASH11[1] - SASH11[0], toonEase='inOut'),
            k(1.45, toon={'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.25)]), D11, t0=0.4, breath=False)],
        props=[P('lettre11', 'styLetter', pos=LET11a, keys=[k(LOW11, to=LET11b, dur=0.35, ease='inOut'), k(LOW11, rotTo=[-0.5, 0, 0.15], dur=0.35)]),
               P('echarpe11', 'stySash', pos=SA11a, rot=[0, 0, 0.15], keys=[k(SASH11[0], to=SA11b, dur=0.08, ease='in'), k(r(SASH11[0] + 0.08), to=SA11c, dur=0.1, ease='out'), k(SASH11[0], rotTo=[0, 0, 0.62], dur=0.18)]),
               P('chaine11', 'styChain', on={'actor': 'ministre1', 'hand': 'R', 'offset': [0.0, -0.06, 0.02], 'hang': True}, opts={'len': 0.36, 'tagS': 1.2, 'swing': [[0.0, 0.3]]})],
        cams=[C11])
st.cue('sfx:rattleShort', 'S11', 0.05, 0.3); st.cue('sfx:slideDown', 'S11', 0.24, 0.35); st.cue('sfx:slideDownSlow', 'S11', LOW11, 0.2); st.cue('sfx:zip', 'S11', SASH11[0], 0.2)

# ============================== the school gate: the facade (ÉCOLE), the customs' folding table at z -0.6
SCHOOL = {'color': '#CFE3F0'}
YARD = lambda: P('cour', 'styRoom', pos=[0, 0, 0], opts={'w': 10, 'h': 3.6, 'back': -2.4, 'wall': '#EAD9B6', 'band': '#C98A5A', 'trim': '#8A5A3A', 'floor': '#6E7378', 'floorD': 9, 'posters': [{'text': 'ÉCOLE', 'x': 1.0, 'y': 2.9, 'w': 1.4, 'h': 0.42, 'bg': '#2E5E8A'}]})
TBL12 = [0.0, 0, -0.6]
DOU1, DOU2 = [-0.42, 0, -1.25], [0.5, 0, -1.2]
KIDS = [('enfant1', [1.25, 0, 0.15]), ('enfant2', [1.75, 0, 0.75]), ('enfant3', [2.25, 0, 1.35])]
CUT13 = [0.95, 0, -1.55]
# 12: customs searched every pencil case. Low tracking along the queue: two customs officers (blue gloves, caps) empty pencil cases onto a folding
#     table marked DOUANE, one holds a pencil up to his eye; the children wait in line with open schoolbags
D12 = st.dur('S12')
C12F, C12T = [-0.75, 0.85, 3.1], [-0.45, 0.85, 3.0]
C12 = FC('S12', 0.0, C12F, {'dou1Top': [DOU1[0], 2.55, DOU1[2]], 'dou2Top': [DOU2[0], 2.55, DOU2[2]], 'kid2Top': [1.75, 1.35, 0.75], 'kid1': [1.25, 1.25, 0.15], 'kidFeet': [1.25, 0.2, 0.15], 'table': [0.0, 0.6, -0.25], 'dou1L': [DOU1[0] - 0.3, 1.5, DOU1[2]]}, top=0.07, bottom=0.74, lenses=range(26, 90), drift=sub(C12T, C12F), extra={'sign': [1.0, 3.1, -2.4]})
SHAKE = lambda who, p, ry, f, hx: act(who, p, ry, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.8, -0.6]), *[k(r(0.15 * i), toon={'reach': {'R': R5([hx + 0.06 * (i % 2), 1.15 + 0.05 * (i % 2), -0.65], 1, 0.06), 'L': R5([hx + 0.25, 1.1, -0.62], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.12) for i in range(8)]])
st.shot('S12', 'whiteVoid', setOpts=SCHOOL, actors=[
        act('douanier1', DOU1, 15, 'stand', 'neutral', keys=[k(0.0, look=[-0.42, 0.9, -0.62]), k(0.0, toon={'reach': {'R': R5([-0.55, 1.12, -0.66], 1, 0.06), 'L': R5([-0.29, 1.12, -0.66], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.5}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.0),
            # (round 2) he upturns a pencil case and shakes it out in a burst of pencils
            *[k(r(0.15 + 0.08 * i), toon={'reach': {'R': R5([-0.55 + 0.03 * (i % 2), 1.08 + 0.04 * (i % 2), -0.66], 1, 0.06), 'L': R5([-0.29 + 0.03 * (i % 2), 1.08 + 0.04 * (i % 2), -0.66], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'clench', 'brow': -0.7}, 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'sq': [1.02, 0.98, 1.02] if i % 2 else [0.99, 1.02, 0.99]}, toonDur=0.07) for i in range(8)], *blink(0.95, {'lid': 0.4, 'mouth': 'line', 'brow': -0.6})]),
        LIFE(act('douanier2', DOU2, -15, 'stand', 'neutral', keys=[k(0.0, look=[0.3, 1.45, -0.35]), k(0.0, toon={'reach': {'R': R5([0.3, 1.4, -0.38], 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.65, 'lidR': 1.0, 'mouth': 'line', 'brow': -0.6}, 'bend': {'spine': [-0.1, 0, 0, 1, None]}}, toonDur=0.0),
            k(0.55, toon={'reach': {'R': R5([0.32, 1.48, -0.33], 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.75, 'lidR': 1.0, 'mouth': 'grimace', 'brow': -0.7}, 'bend': {'spine': [-0.16, 0, 0, 1, None]}}, toonDur=0.2)]), D12, t0=0.8, breath=True),
        *[LIFE(act(w, p, -135 + 10 * i, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.0, -0.6] if i else 'camera'), k(0.0, toon={'face': {'lid': 0.3 + 0.1 * i, 'mouth': ['wavy', 'line', 'o'][i]}, 'hip': 0.6 * (1 - i)}, toonDur=0.0)]), D12, t0=0.2 + 0.25 * i, amp=1.5) for i, (w, p) in enumerate(KIDS)]],
        props=[YARD(), P('table12', 'styPencilTable', pos=TBL12, opts={'n': 4, 'pencils': 16}), P('douane12', 'styNotice', pos=[0.0, 0.5, -0.24], opts={'text': 'DOUANE', 'w': 0.8, 'h': 0.24, 'bg': '#1B2A4A', 'fg': '#F4EEDC', 'border': '#C9A24B'}),
               P('crayon12', 'styPencil', pos=[0.32, 1.48, -0.3], rot=[0, 0, 1.2], opts={'s': 1.4, 'color': '#E8322A'}, keys=[k(0.55, to=[0.34, 1.56, -0.25], dur=0.2)]),
               P('trousse12', 'styNotice', pos=[-0.42, 1.18, -0.66], opts={'text': ' ', 'w': 0.26, 'h': 0.1, 'bg': '#2E8BC0', 'border': '#1B4A6A'}, keys=[k(0.15, rotTo=[0, 0, PI], dur=0.15), k(0.15, to=[-0.42, 1.12, -0.66], dur=0.15)]),
               P('averse12', 'styPencilBurst', pos=[-0.42, 1.1, -0.62], opts={'at': 0.28, 'n': 16, 'spread': 0.9, 'up': 0.7, 'floor': -0.35}), P('carton12', 'styCutout', pos=CUT13, ry=-20, opts={'s': 1.35}),
               *[P(f'sac_{w}', 'backpack', on={'actor': w, 'joint': 'torso', 'offset': [0, 0.2, -0.15]}, scale=0.8) for w, _ in KIDS]],
        cams=[C12])
st.cue('sfx:zip', 'S12', 0.05, 0.25); st.cue('sfx:rattle', 'S12', 0.28, 0.4)

# 13: an officer holds a tiny pencil up against the cardboard cut-out of the brass pen, compares, shakes his head; a child looks up at the cut-out
D13 = st.dur('S13')
OFF13 = [0.42, 0, -0.95]
PEN13a, PEN13 = [0.62, 1.35, -1.12], [0.74, 1.98, -1.36]   # (round 2) at his eye, beside the cut-out's cap
# (round 1) a bright red pencil raised to eye height beside the cut-out's cap, held 0.4 s while he squints, then a clear double head shake; the child
# off to the side
C13 = FC('S13', 0.0, [1.6, 1.7, 3.3], {'cutTop': [CUT13[0], 2.15, CUT13[2]], 'cutFoot': [CUT13[0], 0.5, CUT13[2]], 'offTop': [OFF13[0], 2.8, OFF13[2]], 'offL': [OFF13[0] - 0.4, 2.1, OFF13[2]], 'pencil': PEN13, 'kid': [1.6, 1.25, -0.55], 'kidR': [1.85, 0.8, -0.55]}, top=0.12, bottom=0.74, lenses=range(26, 76), drift=(-0.05, 0, -0.1))
GR13 = lambda p, f, extra=None: {'reach': {'R': R5(add(p, [-0.01, -0.07, 0.04]), 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': f, 'hip': 0, **(extra or {})}
SQ13 = {'lid': 0.65, 'lidR': 1.0, 'mouth': 'line', 'brow': -0.6}
NOD = [k(r(0.56 + 0.11 * i), toon=GR13(PEN13, {'lid': 0.5, 'mouth': 'grimace', 'brow': -0.7}, {'bend': {'neck': [0, 0.12 * (1 if i % 2 else -1) * (0.0 if i == 4 else 1), 0.75 * (1 if i % 2 else -1) * (0.0 if i == 4 else 1), 1, None]}}), toonDur=0.1, toonEase='inOut') for i in range(5)]   # (round 2) two wide shakes
st.shot('S13', 'whiteVoid', setOpts=SCHOOL, actors=[
        act('douanier2', OFF13, 30, 'stand', 'neutral', keys=[k(0.0, look=PEN13a), k(0.0, toon=GR13(PEN13a, {'lid': 0.45, 'mouth': 'line', 'brow': -0.3}), toonDur=0.0),
            k(0.05, toon=GR13(PEN13, SQ13, {'bend': {'spine': [-0.08, 0, 0, 1, None]}}), toonDur=0.14, toonEase='out'), k(0.05, look=add(PEN13, [0.12, 0, -0.1]), lookDur=0.12),
            k(0.3, toon=GR13(add(PEN13, [0.01, 0.01, 0]), {**SQ13, 'lid': 0.75}, {'bend': {'neck': [0.1, 0, 0, 1, None]}}), toonDur=0.2), *NOD, k(1.0, look='camera', lookDur=0.1)]),
        LIFE(act('enfant1', [1.6, 0, -0.55], -100, 'stand', 'neutral', keys=[k(0.0, look=[CUT13[0], 1.6, CUT13[2]]), k(0.0, toon={'face': {'lid': 0.0, 'mouth': 'o', 'brow': 0.6}}, toonDur=0.0)]), D13, t0=0.5)],
        props=[YARD(), P('table13', 'styPencilTable', pos=[-0.6, 0, -0.5], opts={'n': 3}), P('carton13', 'styCutout', pos=CUT13, ry=-20, opts={'s': 1.6}),
               P('crayon13', 'styPencil', pos=PEN13a, rot=[0, 0, 0.05], opts={'s': 1.7, 'color': '#E8322A', 'rim': '#1A0A06'}, keys=[k(0.05, to=PEN13, dur=0.14, ease='out'), k(0.3, to=add(PEN13, [0.01, 0.01, 0]), dur=0.2)]),
               P('sac13', 'backpack', on={'actor': 'enfant1', 'joint': 'torso', 'offset': [0, 0.2, -0.15]}, scale=0.8)],
        cams=[C13])
st.cue('sfx:slideUp', 'S13', 0.05, 0.2); st.cue('sfx:tick', 'S13', 0.6, 0.2); st.cue('sfx:tick', 'S13', 0.8, 0.2)

# ============================== the police station: a navy counter, the officer behind it, his mother in front
POL = {}
CNT14 = [0.0, 0, -0.4]
COP14, MUM = [-0.6, 0, -1.15], [0.12, 0, 0.45]
PH14a, PH14b = [0.1, 1.3, -0.05], [-0.08, 1.3, -0.42]
# 14: his mother turned him in. Over the officer's shoulder from behind the counter (a V): his small old mother slides his framed photo across the
#     counter toward the officer (and us): in it he stands deadpan with the brass pen out of his breast pocket; the officer's eyes go to it
D14 = st.dur('S14'); SL14 = (0.12, 0.5); CUT14 = 0.68; TAKE14 = 0.8
C14 = CAM('S14', 0.0, [0.3, 1.85, -2.5], [-0.12, 1.6, 0.0], 55, {'mumTop': [MUM[0], 2.1, MUM[2]], 'mumChin': [MUM[0], 1.55, MUM[2]], 'photo': add(PH14b, [0, 0.25, 0]), 'photoBot': add(PH14b, [0, -0.23, 0]), 'copHead': [COP14[0], 2.55, COP14[2]], 'copL': [COP14[0] - 0.25, 1.6, COP14[2]]}, to=[0.27, 1.85, -2.35])
# (round 1) cam B, the reverse over her shoulder: the officer's take at the photo (dip, eyes out, head up, hold), then his look at us
C14b = FC('S14b', CUT14, [-0.95, 1.85, 1.7], {'copTop': [COP14[0], 2.85, COP14[2]], 'copChin': [COP14[0], 1.6, COP14[2]], 'copL': [COP14[0] - 0.35, 2.1, COP14[2]], 'photo': add(PH14b, [0.1, 0.0, 0])}, top=0.1, bottom=0.74, lenses=range(26, 76), drift=(-0.03, 0, -0.1), extra={'mumHead': [MUM[0], 1.95, MUM[2]]})
TK14 = {'pop': 0.6, 'popLen': 0.22, 'lid': 0.0, 'jaw': 0.55, 'mouth': 'O', 'brow': 1, 'eyePitch': 0.6}
KC14 = lambda f, sq=None, hd=None, extra=None: {'reach': {'R': R5(add(PH14b, [-0.22, -0.05, -0.04]), 1, 0.05)}, 'hands': {'R': 'open'}, 'face': f, 'hip': 0, 'auto': 0.0, **({'sq': sq} if sq else {}), **({'scl': {'head': hd}} if hd else {}), **(extra or {})}
st.shot('S14', 'policeStation', setOpts=POL, actors=[
        LIFE(act('mere', MUM, 180, 'stand', 'neutral', keys=[k(0.0, look=[COP14[0], 1.95, COP14[2]]), k(0.0, toon={'reach': {'R': R5(add(PH14a, [0.17, -0.1, 0.05]), 1, 0.05), 'L': R5(add(PH14a, [-0.17, -0.1, 0.05]), 1, 0.05)}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.5, 'mouth': 'smirk', 'brow': -0.3}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.0),
            k(SL14[0], toon={'reach': {'R': R5(add(PH14b, [0.17, -0.1, 0.05]), 1, 0.05), 'L': R5(add(PH14b, [-0.17, -0.1, 0.05]), 1, 0.05)}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.55, 'mouth': 'smirk', 'brow': -0.4}, 'bend': {'spine': [0.45, 0, 0, 1, None]}}, toonDur=SL14[1] - SL14[0], toonEase='inOut'),
            k(0.85, toon={'face': {'lid': 0.5, 'mouth': 'smirk', 'brow': -0.4}, 'bend': {'spine': [0.1, 0, 0, 1, None]}}, toonDur=0.2), k(0.9, look='camera', lookDur=0.2)]), D14, t0=1.0, breath=False),
        act('flic', COP14, 25, 'stand', 'neutral', keys=[k(0.0, look=[MUM[0], 1.7, MUM[2]]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0), k(0.55, look=PH14b, lookDur=0.15),
            k(0.45, toon=KC14({'lid': 0.4, 'mouth': 'line', 'gy': 0.6}), toonDur=0.15, toonEase='out'),
            # (round 2) a double take, no stalks: a glance at the photo, back to her, then his head snaps back down to it, stretched, brows up, held
            k(r(TAKE14 - 0.08), look=[MUM[0], 1.7, MUM[2]], lookDur=0.06), k(r(TAKE14 - 0.08), toon=KC14({'lid': 0.4, 'mouth': 'line', 'brow': 0.1}), toonDur=0.06),
            k(TAKE14, look=PH14b, lookDur=0.04), k(TAKE14, toon=KC14({'lid': 0.0, 'mouth': 'O', 'jaw': 0.35, 'brow': 1.0, 'eye': 0.3, 'gy': 0.6}, [0.88, 1.16, 0.88], [0.9, 1.18, 0.9], {'hairUp': 0.6}), toonDur=0.04, toonEase='outBack'),
            *[k(r(TAKE14 + 0.08 + 0.07 * i), toon=KC14({'lid': 0.0, 'mouth': 'O', 'jaw': 0.3 + 0.06 * (i % 2), 'brow': 1.0, 'eye': 0.3, 'gy': 0.6}, [0.9, 1.13, 0.9], [0.92 + 0.02 * (i % 2), 1.15 - 0.03 * (i % 2), 0.92]), toonDur=0.06) for i in range(3)],
            k(1.12, toon=KC14({'lid': 0.1, 'mouth': 'o', 'brow': 0.6}, [1.05, 0.95, 1.05], [1.05, 0.95, 1.05]), toonDur=0.06, toonEase='in'), k(1.2, look='camera', lookDur=0.12),
            k(1.22, toon=KC14({'lid': 0.3, 'mouth': 'line', 'brow': 0.5}), toonDur=0.08)])],
        props=[P('guichet14', 'styCounter', pos=CNT14, opts={'plate': 'POLICE', 'tag': False, 'bolt': False, 'color': '#3E5578', 'panel': '#34496A', 'top': '#1E2A3E'}),
               P('photo14', 'styPhoto', pos=PH14a, ry=180, opts={'stand': True}, keys=[k(SL14[0], to=PH14b, dur=SL14[1] - SL14[0], ease='inOut')])],
        cams=[C14, C14b])
st.cue('sfx:scratch', 'S14', SL14[0], 0.2); st.cue('sfx:tick', 'S14', SL14[1], 0.25); st.cue('sfx:boing', 'S14', TAKE14, 0.3)

# ============================== the block of flats at night (whiteVoid navy + styBlock: facade at z 0, storeys of 2.9 m, his balcony on floor 5)
NIGHTX = {'color': '#141C33'}
NLOOK = {'sun': 0.3, 'fill': 0.55, 'exposure': 1.05}
S_ = 2.9; HF = 5; BAL = [0.0, HF * S_, 0.55]
HELI = [1.6, 20.6, 2.6]; HSC = 1.0
def heli_lamp(h, ry=-90, s=HSC):
    a = math.radians(ry); v = [0, -0.5, 0.62]; return [r(h[0] + s * (v[0] * math.cos(a) + v[2] * math.sin(a))), r(h[1] + s * v[1]), r(h[2] + s * (-v[0] * math.sin(a) + v[2] * math.cos(a)))]
LAMP = heli_lamp(HELI)
BEAMTO = [0.0, HF * S_ + 0.2, 0.6]
def HELIP(pid, on=None, r1=0.95, to=BEAMTO, op=0.14, heli=HELI):
    # (round 2) a solid navy machine (no halo sticker, a faint rotor disc) and a beam that stays bright all the way down onto the balcony, a spot there
    lamp = heli_lamp(heli); BR = aim_rot(lamp, to)
    return [P(pid, 'chvHeli', pos=heli, ry=-90, scale=HSC, opts={'spin': 1.15, 'discOpacity': 0.0, 'emissive': '#24407A'}),
            P(pid + 'b', 'chvBeam', pos=lamp, ry=BR[1], rot=[BR[0], 0, BR[2]], opts={'len': r(math.dist(lamp, to) + 0.15), 'r': r1, 'r0': 0.1, 'op': op, 'fade': 1.0, 'lampR': 0.1, 'flare': 1.1, 'on': on or [[0, 1]]}),
            P(pid + 's', 'chvPool', pos=[to[0], HF * S_ + 0.01, 0.6], opts={'r': 1.1, 'h': 2.0, 'power': 5, 'range': 4.0, 'color': '#EAF2FF'})]
SWAT = [('commando1', -0.62), ('commando2', 0.0), ('commando3', 0.62)]
MASKED = lambda who, color=None: [P(f'cagoule_{who}', 'balaclava', on={'actor': who, 'joint': 'head', 'offset': [0, 0, 0]}, opts={'color': color} if color else {}), P(f'casque_{who}', 'tacHelmet', on={'actor': who, 'joint': 'head', 'offset': [0, 0.47, 0]})]
def RIFLE(pid, grip, target, keys=None):
    a = aim_rot(target, grip); return P(pid, 'rifle', pos=grip, ry=a[1], rot=[a[0], 0, a[2]], scale=1.25, keys=keys or [])
Z16 = {-0.62: 0.32, 0.0: 0.62, 0.62: 0.92}   # (round 2) the commandos staggered in depth on the balcony
ROPE = lambda who, x: {'a': {'prop': 'heli', 'offset': [r(x * 0.5), -0.75, r(Z16.get(x, 0.62) - 0.62)]}, 'b': {'actor': who, 'hand': 'R'}, 'color': '#F2EBD6', 'sag': 0.0, 'radius': 0.022, 'minPx': 4, 'rim': 0.6, 'rimColor': '#2A2A2A'}
COOL = lambda pid, y, r_=1.1: P(pid, 'chvPool', pos=[0.0, y, 0.6], opts={'r': r_, 'h': 2.6, 'power': 7, 'range': 4.5, 'color': '#CFE2FF'})   # (round 1) the searchlight's cool rim on the commandos
# 15: special forces jumped onto his balcony. Night, low from the street: the block of flats, the navy helicopter high over the roof, its searchlight on
#     his fifth-floor balcony; (round 1) three masked commandos slide down their ropes from the helicopter, accelerating, staggered, legs together
D15 = st.dur('S15')
HELI15 = [3.6, 22.4, 3.6]   # (round 2) off to the side: the beam slants down onto the balcony
SX15 = [-0.9, 0.0, 0.9]
C15 = FC('S15', 0.0, [5.0, 1.2, 19.0], {'heliTop': [HELI15[0], HELI15[1] + 1.2, HELI15[2]], 'rotL': [HELI15[0] - 1.8, HELI15[1] + 0.8, HELI15[2]], 'heliTail': [HELI15[0] + 2.6, HELI15[1], HELI15[2]], 'bal': [0, HF * S_ - 0.4, 1.1], 'balL': [-1.4, HF * S_, 0.0], 'floor3': [-3.0, 3 * S_, 0]}, top=0.06, bottom=0.74, lenses=range(26, 76), drift=(-0.1, 0.05, -0.4))
def SLIDER(w, x, i):
    y0, y1 = r(21.6 - 0.7 * i), r(16.6 - 0.25 * i)
    return act(w, [x, y0, 0.85], 0, 'stand', 'angry', keys=[k(0.0, to=[x, y1, 0.85], dur=D15, ease='in', glide=True, face=0), k(0.0, look='camera'),
        k(0.0, toon={'reach': {'R': R5([x - 0.03, y0 + 2.45, 0.85], 1, 0.06), 'L': R5([x + 0.03, y0 + 2.1, 0.85], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.6}, 'sq': [0.92, 1.1, 0.92], 'auto': 0.0}, toonDur=0.0),
        k(0.6, toon={'reach': {'R': R5([x - 0.03, y1 + 2.45, 0.85], 1, 0.06), 'L': R5([x + 0.03, y1 + 2.1, 0.85], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.7}, 'sq': [0.88, 1.16, 0.88], 'auto': 0.0}, toonDur=D15 - 0.6, toonEase='in')])
ROPE15 = lambda who, x: {**ROPE(who, x), 'a': {'prop': 'heli', 'offset': [r(x * 0.6), -0.75, -0.3]}}
st.shot('S15', 'whiteVoid', setOpts=NIGHTX, look=NLOOK, actors=[SLIDER(w, SX15[i], i) for i, (w, _) in enumerate(SWAT)],
        props=[P('immeuble', 'styBlock', pos=[0, 0, 0], opts={'heroFloor': HF}), *HELIP('heli', heli=HELI15, op=0.16), *[q for w, _ in SWAT for q in MASKED(w)]],
        tethers=[ROPE15(w, SX15[i]) for i, (w, _) in enumerate(SWAT)], cams=[C15])
st.cue('engine', 'S15', 0.0, 0.35, D15); st.cue('sfx:rotor', 'S15', 0.0, 0.4); st.cue('sfx:slideDownLong', 'S15', 0.05, 0.3)

# 16: at the balcony, in the beam: they drop the last metre onto it, (round 1) a hard squash held three frames, a stretch, a settle, rifles up across
#     the chest; a cool pool of searchlight on the balcony rims them against the facade
D16 = st.dur('S16'); LAND16 = 0.3
C16 = FC('S16', 0.0, [3.3, HF * S_ + 0.6, 5.0], {'balL': [-1.15, HF * S_ - 0.3, 1.1], 'balR': [1.15, HF * S_ - 0.3, 1.1], 'c1Top': [-0.62, HF * S_ + 2.4, 0.6], 'c3Top': [0.62, HF * S_ + 2.4, 0.6], 'win': [0, HF * S_ + 2.2, 0.0], 'ropeHi': [0, HF * S_ + 3.4, 0.6]}, top=0.06, bottom=0.74, drift=(-0.1, 0.0, -0.25))
F16 = lambda i: 30 - 12 * (i - 1)
GRIP16 = lambda x, dy=0.0: [r(x + 0.12), r(HF * S_ + 1.25 + dy), r(Z16.get(x, 0.62) + 0.22)]
TIP16 = lambda x, dy=0.0: [r(x - 0.55), r(HF * S_ + 2.3 + dy), r(Z16.get(x, 0.62) + 0.48)]
AIM16 = lambda x, dy=0.0: {'reach': {'R': R5(GRIP16(x, dy), 1, 0.06), 'L': R5(lerp(GRIP16(x, dy), TIP16(x, dy), 0.35), 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.8}, 'auto': 0.0}
def LANDER(w, x, i):
    tl, dy0 = r(LAND16 + 0.05 * i), r(1.0 + 0.15 * i)
    z = Z16[x]
    return act(w, [x, HF * S_ + dy0, z], F16(i), 'stand', 'angry', keys=[
        k(0.0, to=[x, HF * S_, z], dur=tl, ease='in', glide=True, face=F16(i)), k(0.0, look='camera'),
        k(0.0, toon={**AIM16(x, dy0), 'sq': [0.9, 1.12, 0.9]}, toonDur=0.0), k(0.05, toon={**AIM16(x, dy0 * 0.5), 'sq': [0.88, 1.15, 0.88]}, toonDur=tl - 0.05, toonEase='in'),
        k(tl, toon={**AIM16(x, -0.35), 'sq': [1.42, 0.58, 1.42]}, toonDur=0.03), k(r(tl + 0.1), toon={**AIM16(x, 0.08), 'sq': [0.88, 1.14, 0.88]}, toonDur=0.07, toonEase='out'),
        k(r(tl + 0.2), toon={**AIM16(x), 'sq': [1.04, 0.97, 1.04]}, toonDur=0.08), k(r(tl + 0.3), toon=AIM16(x), toonDur=0.08), *blink(r(0.95 + 0.07 * i), {'lid': 0.5, 'mouth': 'line', 'brow': -0.8})])
def RIF16(w, x, i):
    tl, dy0 = r(LAND16 + 0.05 * i), r(1.0 + 0.15 * i)
    return RIFLE(f'fusil_{w}', GRIP16(x, dy0), TIP16(x, dy0), keys=[k(0.0, to=GRIP16(x), dur=tl, ease='in'), k(tl, to=GRIP16(x, -0.35), dur=0.03), k(r(tl + 0.1), to=GRIP16(x, 0.08), dur=0.07), k(r(tl + 0.2), to=GRIP16(x), dur=0.08)])
st.shot('S16', 'whiteVoid', setOpts=NIGHTX, look=NLOOK, actors=[LANDER(w, x, i) for i, (w, x) in enumerate(SWAT)],
        props=[P('immeuble', 'styBlock', pos=[0, 0, 0], opts={'heroFloor': HF}), *HELIP('heli', op=0.2), *[P(f'rim16_{i}', 'chvPool', pos=[x - 0.15, HF * S_ + 0.01, r(Z16[x] - 0.3)], opts={'r': 0.3, 'h': 2.1, 'power': 4.5, 'range': 1.6, 'color': '#BFD8FF'}) for i, (w, x) in enumerate(SWAT)], *[q for w, _ in SWAT for q in MASKED(w)],
               *[RIF16(w, x, i) for i, (w, x) in enumerate(SWAT)]],
        tethers=[{**ROPE(w, x), 'until': r(LAND16 + 0.05 * i)} for i, (w, x) in enumerate(SWAT)], cams=[C16])
for i in range(3): st.cue('thud', 'S16', r(LAND16 + 0.05 * i), 0.45)

# 17: the balcony gave way, and the three below. (round 1) Tight on the balcony column, the camera tilting down with each fall: it shakes, cracks,
#     hangs a beat, drops onto the empty one below (squash, dust burst, the pair hangs a beat), the pair onto the next, the three onto the last, and the
#     four come down onto the pavement in a stack, the commandos riding on top, arms flung up on each drop, squashed on each impact
D17 = st.dur('S17'); CRACK17, BREAK17 = 0.03, 0.12
TH = 0.28; STACK = {2: 0.05 + TH, 3: 0.05 + 2 * TH, 4: 0.05 + 3 * TH, 5: 0.05 + 4 * TH}
def fall(y0, y1, t0, t1):
    """keys of an accelerating fall (y = y0 - d u^2)"""
    return [[r(t0 + (t1 - t0) * u), r(y0 - (y0 - y1) * u * u)] for u in (0.0, 0.35, 0.6, 0.8, 1.0)]
SEG = [(0.17, 0.29), (0.35, 0.45), (0.5, 0.59), (0.64, 0.78)]   # each fall (start, impact); the hang before each start; (round 2) the last landing held 0.39 s
TG = SEG[3][1]
Y5 = [5 * S_, 4 * S_ + TH, 3 * S_ + 2 * TH, 2 * S_ + 3 * TH, STACK[5]]
SL = {5: [[0.0, 5 * S_]] + [q for j in range(4) for q in fall(Y5[j], Y5[j + 1], *SEG[j])],
      4: [[0.0, 4 * S_]] + [q for j in range(1, 4) for q in fall(Y5[j] - TH, Y5[j + 1] - TH, *SEG[j])],
      3: [[0.0, 3 * S_]] + [q for j in range(2, 4) for q in fall(Y5[j] - 2 * TH, Y5[j + 1] - 2 * TH, *SEG[j])],
      2: [[0.0, 2 * S_]] + fall(2 * S_, STACK[2], *SEG[3])}
for f_, ks_ in SL.items(): ks_ += [[r(TG + 0.07), r(ks_[-1][1] + 0.06)], [r(TG + 0.14), ks_[-1][1]]]   # (round 2) the stack bounces once on the pavement
LANDS = {4: SEG[0][1], 3: SEG[1][1], 2: SEG[2][1], 5: TG}
PUFFS = [[SEG[0][1], 4 * S_], [SEG[1][1], 3 * S_], [SEG[2][1], 2 * S_], [TG, 0.1]]
C17F = [3.6, 12.5, 11.5]; L17 = 44
C17 = [CAM('S17', 0.0, C17F, [0.0, 15.1, 0.5], L17, {'bal5': [0, 5 * S_ + 2.3, 0.6], 'bal4': [0, 4 * S_, 1.1]})]
for j, (a, b) in enumerate(SEG):
    ly = [12.6, 10.0, 7.3, 2.3][j]; fy = [10.6, 8.2, 5.8, 2.6][j]
    C17.append(glide([cam(a, [C17F[0], fy, C17F[2] + (1.5 if j == 3 else 0)], [C17F[0], fy, C17F[2] + (1.5 if j == 3 else 0)], [0.0, ly, 0.5], [0.0, ly, 0.5], L17 if j < 3 else 50)], r(b - a + 0.03)))
    chk(f'S17_{j}', [C17F[0], fy, C17F[2]], [0.0, ly, 0.5], L17, {'top': [0, Y5[j + 1] + 2.3, 0.6], 'impact': [0, Y5[j + 1] - TH * (j + 1), 1.1]})
def ride(t):
    ks = SL[5]
    if t <= ks[0][0]: return ks[0][1]
    for i in range(1, len(ks)):
        if t < ks[i][0]: a, b = ks[i - 1], ks[i]; return a[1] + (b[1] - a[1]) * (t - a[0]) / max(1e-6, b[0] - a[0])
    return ks[-1][1]
RIDE_T = sorted({r(x[0]) for x in SL[5]})
SITF = {'lid': 0.45, 'mouth': 'line', 'brow': -0.6}
FLAIL = lambda x, y: {'reach': {'R': R5([x - 0.3, r(y + 2.35), 0.75], 1, 0.06), 'L': R5([x + 0.3, r(y + 2.35), 0.75], 1, 0.06)}, 'hands': {'R': 'spread', 'L': 'spread'}}   # y: the slab top at that instant
def RIDER(w, x, i):
    keys = [k(0.0, look='camera')] + [k(RIDE_T[j], to=[x, r(ride(RIDE_T[j + 1])), 0.62], dur=r(RIDE_T[j + 1] - RIDE_T[j]), ease='linear', glide=True, face=F16(i)) for j in range(len(RIDE_T) - 1) if RIDE_T[j + 1] > RIDE_T[j]]
    keys += [k(0.0, toon={**AIM16(x), 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.8}}, toonDur=0.0),
             k(CRACK17, toon={**AIM16(x), 'face': {'lid': 0.0, 'mouth': 'o', 'brow': 0.6, 'gy': 0.8}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.05)]
    for j, (a, b) in enumerate(SEG):
        ya, yb = Y5[j], Y5[j + 1]
        # (round 2) the hands ride down with the slab (reach targets are world points): a key at each sample of the fall
        mids = [t for t in RIDE_T if a < t < b]
        for m_, tm in enumerate(mids):
            nxt = mids[m_ + 1] if m_ + 1 < len(mids) else b
            keys.append(k(tm, toon={**FLAIL(x, ride(nxt)), 'face': {'lid': 0.0, 'mouth': 'O', 'jaw': 0.5, 'brow': 1}, 'sq': [0.86, 1.18, 0.86], 'hairUp': 0, 'auto': 0.0}, toonDur=r(nxt - tm), toonEase='linear'))
        if j == 3:
            # (round 2) the last landing gets its own beat: a hard squash held three frames, a stretch back up, a settle, then they sit
            keys += [k(a, toon={**FLAIL(x, ride(min([t for t in RIDE_T if t > a] or [b]))), 'face': {'lid': 0.0, 'mouth': 'O', 'jaw': 0.6, 'brow': 1}, 'sq': [0.84, 1.2, 0.84], 'auto': 0.0}, toonDur=0.04),
                     k(b, toon={**FLAIL(x, ride(b) - 0.6), 'face': {'lid': 0.85, 'mouth': 'clench', 'brow': -0.5}, 'sq': [1.6, 0.45, 1.6], 'auto': 0.0}, toonDur=0.03),
                     k(r(b + 0.12), toon={**FLAIL(x, ride(b) + 0.15), 'face': {'lid': 0.0, 'mouth': 'o', 'brow': 0.6}, 'sq': [0.84, 1.22, 0.84], 'auto': 0.0}, toonDur=0.07, toonEase='out'),
                     k(r(b + 0.22), toon={**FLAIL(x, ride(b) - 0.1), 'face': {'lid': 0.4, 'mouth': 'wavy', 'brow': 0.2}, 'sq': [1.06, 0.95, 1.06], 'auto': 0.0}, toonDur=0.06)]
            continue
        keys += [k(a, toon={**FLAIL(x, ride(min([t for t in RIDE_T if t > a] or [b]))), 'face': {'lid': 0.0, 'mouth': 'O', 'jaw': 0.5, 'brow': 1}, 'sq': [0.86, 1.18, 0.86], 'hairUp': 0, 'auto': 0.0}, toonDur=0.04),
                 k(b, toon={**FLAIL(x, ride(b) - 0.4), 'face': {'lid': 0.7, 'mouth': 'clench', 'brow': -0.4}, 'sq': [1.35, 0.66, 1.35], 'auto': 0.0}, toonDur=0.03),
                 k(r(b + 0.05), toon={**FLAIL(x, ride(b) - 0.1), 'face': {'lid': 0.4, 'mouth': 'wavy', 'brow': 0.2}, 'sq': [0.97, 1.04, 0.97], 'auto': 0.0}, toonDur=0.03)]
    keys += [k(r(TG + 0.3), clip='sit'), k(r(TG + 0.3), to=[x, r(STACK[5] - 0.43), 0.85], dur=0.06, glide=True, face=F16(i)), k(r(TG + 0.32), toon={'reach': {'R': R5([x - 0.15, r(STACK[5] + 0.62), 1.15], 1, 0.06), 'L': R5([x + 0.15, r(STACK[5] + 0.62), 1.15], 1, 0.06)}, 'hands': {'R': 'open', 'L': 'open'}, 'face': SITF, 'sq': [1, 1, 1], 'auto': 0.2}, toonDur=0.06)]
    return act(w, [x, 5 * S_, 0.62], F16(i), 'stand', 'angry', keys=keys)
st.shot('S17', 'whiteVoid', setOpts=NIGHTX, look={**NLOOK, 'fill': 0.85, 'exposure': 1.15}, actors=[RIDER(w, x, i) for i, (w, x) in enumerate(SWAT)],
        props=[P('immeuble', 'styBlock', pos=[0, 0, 0], opts={'heroFloor': HF, 'slabs': {str(f): v for f, v in SL.items()}, 'land': {str(f): v for f, v in LANDS.items()}, 'crackAt': CRACK17, 'breakAt': BREAK17, 'dustAt': TG, 'puffs': PUFFS}),
               *HELIP('heli'), *[q for w, _ in SWAT for q in MASKED(w)], P('rim17', 'chvPool', pos=[0.0, 0.06, 1.6], opts={'r': 1.5, 'h': 3.0, 'power': 6, 'range': 5, 'color': '#CFE2FF'}),
               P('rim17b', 'chvPool', pos=[0.0, 13.0, 1.8], opts={'r': 0.01, 'h': 2.5, 'power': 5, 'range': 5, 'color': '#CFE2FF'})],
        cams=C17, fx=[{'type': 'shake', 'at': a, 'dur': 0.12, 'amount': 0.01 + 0.006 * j} for j, (_, a) in enumerate(SEG)])
st.cue('sfx:crunch', 'S17', CRACK17, 0.5)
for j, (a, b) in enumerate(SEG): st.cue('thud', 'S17', b, 0.45 + 0.15 * j)
st.cue('sfx:poof', 'S17', r(TG + 0.03), 0.45)

# 18: the stack on the pavement, (round 2) low and close: four separate slabs a little askew with shadow gaps and crumpled rails, pulled off the wall;
#     the three commandos sit spread along the top facing us, unhurt, arms down, rifles across their laps aimed off to the side; dark masks under a
#     light dust layer so the eyes read; one clear slow blink, then a big cough puff
D18 = st.dur('S18')
TH18 = 0.34; Z18 = 0.95
STACK18 = {2: 0.05 + TH18, 3: 0.05 + 2 * TH18, 4: 0.05 + 3 * TH18, 5: 0.05 + 4 * TH18}
SEAT18 = STACK18[5]
FINAL = {f: [[0.0, STACK18[f]]] for f in (2, 3, 4, 5)}
JIT18 = {'2': [0.05, 0.0, 0.03], '3': [-0.09, 0.05, -0.06], '4': [0.1, -0.04, 0.07], '5': [-0.04, 0.06, -0.04]}
SX18 = [-0.78, 0.0, 0.78]
C18 = FC('S18', 0.0, [1.3, 0.75, Z18 + 3.9], {'stackL': [-1.15, 0.3, Z18 + 1.1], 'stackR': [1.15, 0.3, Z18 + 1.1], 'c1': [SX18[0], SEAT18 + 1.95, Z18 + 0.85], 'c3': [SX18[2], SEAT18 + 1.95, Z18 + 0.85], 'top': [0, SEAT18 + 2.05, Z18 + 0.7]}, top=0.08, bottom=0.76, lenses=range(26, 76), drift=(-0.05, 0.0, -0.12))
LAP = lambda x: [r(x + 0.05), r(SEAT18 + 0.62), Z18 + 1.15]
SIT18 = lambda x, f: {'reach': {'R': R5(add(LAP(x), [-0.16, 0.02, 0.0]), 1, 0.06), 'L': R5(add(LAP(x), [0.16, 0.02, 0.0]), 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f, 'hip': 0, 'auto': 0.1}
FD = {'lid': 0.5, 'mouth': 'line', 'brow': -0.6}
COUGH = 0.62
def SITTER(w, x, i):
    keys = [k(0.0, look='camera' if i == 1 else [x * 1.8, 1.8, 7.0]), k(0.0, toon=SIT18(x, {**FD, 'lid': 0.45 + 0.1 * i}), toonDur=0.0)]
    if i == 0: keys += [k(0.25, toon=SIT18(x, {**FD, 'lid': 1.0}), toonDur=0.12, toonEase='inOut'), k(0.45, toon=SIT18(x, FD), toonDur=0.12), k(0.7, look='camera', lookDur=0.15)]
    if i == 1: keys += [k(r(COUGH - 0.12), toon={**SIT18(x, {'lid': 0.3, 'mouth': 'o', 'brow': 0.4, 'puff': 0.6}), 'sq': [0.95, 1.06, 0.95]}, toonDur=0.1),
                        k(COUGH, toon={**SIT18(x, {'lid': 1.0, 'mouth': 'O', 'brow': -0.4}), 'sq': [1.12, 0.88, 1.12]}, toonDur=0.03),
                        k(r(COUGH + 0.18), toon=SIT18(x, {'lid': 0.6, 'mouth': 'wavy', 'brow': -0.4}), toonDur=0.12)]
    if i == 2: keys += [k(0.4, look=[-3.0, 1.6, 6.0], lookDur=0.2), k(0.9, look='camera', lookDur=0.15)]
    return LIFE(act(f'{w}d', [x, r(SEAT18 - 0.43), Z18 + 0.82], 12 - 12 * i, 'sit', 'neutral', keys=keys), D18, t0=0.9 if i == 0 else 0.15 + 0.3 * i, blinks=i != 1, breath=True)
st.shot('S18', 'whiteVoid', setOpts=NIGHTX, look={**NLOOK, 'fill': 0.8, 'exposure': 1.12}, actors=[SITTER(w, SX18[i], i) for i, (w, _) in enumerate(SWAT)],
        props=[P('immeuble', 'styBlock', pos=[0, 0, 0], opts={'heroFloor': HF, 'slabs': {str(f): v for f, v in FINAL.items()}, 'land': {str(f): -1 for f in FINAL}, 'slabZ': {str(f): Z18 for f in FINAL}, 'stackJit': JIT18, 'dustAt': -0.4, 'dustOp': 0.3, 'litHero': True}),
               *[q for i, (w, _) in enumerate(SWAT) for q in MASKED(f'{w}d', '#4A4A4C')],
               *[RIFLE(f'fusil_{w}', LAP(SX18[i]), add(LAP(SX18[i]), [-1.0 if i < 2 else 1.0, 0.05, 0.25])) for i, (w, _) in enumerate(SWAT)],
               P('toux18', 'dustPuff', pos=[0.0, r(SEAT18 + 1.42), Z18 + 1.15], scale=1.5, opts={'once': True, 'startAt': COUGH, 'period': 0.55, 'color': '#E2DCCD'}),
               P('rim18', 'chvPool', pos=[0.0, 0.06, Z18 + 2.0], opts={'r': 1.6, 'h': 2.6, 'power': 5, 'range': 5, 'color': '#D6E6FF'})],
        cams=[C18])
st.cue('sfx:poof', 'S18', 0.0, 0.2); st.cue('sfx:poof', 'S18', COUGH, 0.45)

# ============================== his flat at night: the wall behind him, the searchlight through the window
FLAT = {'color': '#1A2238'}
HERO19 = [0.0, 0, -0.35]
COM19 = [0.9, 0, -0.12]
PK19 = [0.075, 1.46, -0.16]
# 19: the pen was in his pocket. Chewed. In striped pyjamas (round 1: no lapels) against his wall, hands up, in the white beam: the commando at his left reaches into his breast
#     pocket and pulls the brass pen out, holds it up in the beam (SAISI); his eyes follow it; cut in close on the cap: chewed flat, tooth marks; his
#     red pen stays clipped in the pocket
D19 = st.dur('S19'); GRAB19, PULL19 = 0.35, 0.62; CUT19 = r(st.at('S19', 'L13', 6) - 0.03)
UPP = [0.44, 1.98, -0.08]   # (round 2) in the gap between the two heads, against the lit wall patch
PU19C, PU19R, PU19G = pen_at(add(UPP, [0, -0.2, 0.0]), [0.05, 1, 0.12], grip=0.12)
PK19C, PK19R, PK19G = pen_at(add(PK19, [0, -0.21, 0]), [0, 1, 0], grip=0.33)
C19a = FC('S19a', 0.0, [-0.25, 1.75, 2.9], {'heroTop': [HERO19[0], 2.36, HERO19[2]], 'handsUpL': [-0.55, 2.4, -0.3], 'comTop': [COM19[0], 2.4, COM19[2]], 'pen': PU19C, 'pocket': PK19, 'chest': [0, 1.2, -0.2]}, top=0.08, bottom=0.72, lenses=range(26, 76), drift=(0, 0, -0.15))
CAP19 = add(PU19C, [0.01, 0.12, 0.02])
C19b = CAM('S19b', CUT19, add(CAP19, [0.32, 0.12, 0.78]), add(CAP19, [0, -0.02, 0]), 26, {'cap': add(CAP19, [0, 0.06, 0]), 'capL': add(CAP19, [-0.06, 0, 0]), 'band': add(CAP19, [0, -0.1, 0])}, to=add(CAP19, [0.27, 0.1, 0.66]))   # (round 1) the insert fills the frame with the bitten cap
BEAM19 = [-1.8, 4.8, 1.4]; BT19 = [0.4, 1.95, -0.55]; BR19 = aim_rot(BEAM19, BT19)
HUP = {'R': R5([-0.42, 2.1, -0.3], 1, 0.05), 'L': R5([0.22, 2.12, -0.33], 1, 0.05)}   # (round 2) under the card band
FH = {'lid': 0.5, 'mouth': 'line', 'brow': 0.3}
st.shot('S19', 'whiteVoid', setOpts=FLAT, look=NLOOK, actors=[
        act('mecPyj', HERO19, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': FH, 'hip': 0}, toonDur=0.0),
            k(r(GRAB19 + 0.05), toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {**FH, 'gx': -0.5, 'gy': 0.7, 'mouth': 'o'}, 'hip': 0}, toonDur=0.1),
            k(r(PULL19 + 0.05), look=add(PK19, [0, 0.2, 0.3]), lookDur=0.08), k(r(PULL19 + 0.15), look=add(PU19C, [0, 0.1, 0]), lookDur=0.2), k(r(PULL19 + 0.15), toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'o', 'brow': 0.6, 'gx': -0.5}, 'bend': {'neck': [-0.1, 0, -0.3, 1, None]}, 'hip': 0}, toonDur=0.15), k(r(PULL19 + 0.15), toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'wavy', 'brow': 0.6, 'gx': -0.4, 'gy': -0.2}, 'sq': [0.97, 1.03, 0.97], 'hip': 0}, toonDur=0.12),
            k(1.15, toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.4, 'mouth': 'gulp', 'brow': 0.4, 'gx': -0.4}, 'hip': 0}, toonDur=0.1),
            k(1.35, look='camera', lookDur=0.15), k(1.35, toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.55, 'mouth': 'line', 'brow': -0.2}, 'hip': 0}, toonDur=0.12),
            k(r(CUT19 + 0.1), look=add(PU19C, [0, 0.15, 0]), lookDur=0.1), k(r(CUT19 + 0.1), toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.2, 'gx': -0.6, 'gy': -0.4}, 'hip': 0}, toonDur=0.1)]),
        LIFE(act('commando4', COM19, -45, 'stand', 'neutral', keys=[k(0.0, look=PK19), k(0.0, toon={'reach': {'R': R5([0.55, 1.2, 0.2], 1, 0.06)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.7}, 'hip': 0}, toonDur=0.0),
            k(GRAB19, toon={'reach': {'R': R5(PK19G, 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.7}, 'hip': 0}, toonDur=0.2, toonEase='inOut'),
            k(PULL19, toon={'reach': {'R': R5(PU19G, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'smirk', 'brow': -0.5}, 'hip': 0}, toonDur=0.3, toonEase='out'), k(r(PULL19 + 0.1), look=PU19C, lookDur=0.2)]), D19, t0=1.0, breath=False)],
        props=[P('mur19', 'styRoom', pos=[0, 0, 0], opts={'w': 6, 'h': 3.2, 'back': -0.62, 'wall': '#9AA6BE', 'band': '#6E7A94', 'trim': '#3E4860', 'floor': '#4A4F5E'}),
               P('poche19s', 'styPen', on={'actor': 'mecPyj', 'joint': 'torso', 'offset': POCK_S}, opts={**PEN_STATE, 'chewed': True}, keys=[k(PULL19, visible=False)]), POCKET('poche19r', 'mecPyj', 'red'), PATCH('patch19', 'mecPyj', '#7F9FCC'),
               P('pyjama19', 'styPyjTop', on={'actor': 'mecPyj', 'joint': 'torso', 'offset': [0, 0, 0]}, opts={'w': 0.38, 'z': 0.172}),
               P('stylo19', 'styPen', pos=PK19C, ry=PK19R[1], rot=[PK19R[0], 0, PK19R[2]], opts={**PEN_STATE, 'chewed': True}, keys=[k(0.0, visible=False), k(PULL19, visible=True), k(PULL19, to=PU19C, dur=0.3, ease='out'), k(PULL19, rotTo=ROT(PU19R), dur=0.3)]),
               P('tache19', 'chvPool', pos=[0.42, 2.0, -0.6], rot=[PI / 2, 0, 0], opts={'r': 0.55, 'h': 0.6, 'power': 1.6, 'range': 2, 'color': '#F2F6FF', 'on': [[0, 1], [CUT19, 0.1]]}),
               P('faisceau19', 'chvBeam', pos=BEAM19, ry=BR19[1], rot=[BR19[0], 0, BR19[2]], opts={'on': [[0, 1], [CUT19, 0.25]], 'len': r(math.dist(BEAM19, BT19) + 0.6), 'r': 1.25, 'r0': 0.25, 'op': 0.11, 'fade': 0.75, 'lampR': 0.0, 'flare': 0.0}),
               *MASKED('commando4')],
        cams=[C19a, C19b])
st.card('S19', 'SAISI', at=r(PULL19 + 0.2))
st.cue('sfx:zip', 'S19', GRAB19, 0.25); st.cue('sfx:slideUp', 'S19', PULL19, 0.3); st.cue('sfx:gulp', 'S19', 1.15, 0.3); st.cue('sfx:ding', 'S19', r(CUT19 + 0.05), 0.3)

# ============================== the forensic lab: a pale room, the steel bench at the origin
LAB = {'color': '#DCE6EA'}
TECH = [0.05, 0, -0.72]
# 20: out of ink for ten years. Top-down on the bench: the technician in white scribbles the brass pen across the big white board: nothing; she lifts it,
#     shakes it hard, scribbles again: nothing; she looks up at us
D20 = st.dur('S20'); SHK20 = (0.68, 1.05)
UP20 = [0.2, 1.0, -0.75]
W20a = [[-0.2 + 0.08 * i, 0.93, 0.0 + 0.07 * (i % 2)] for i in range(6)]
W20b = [[-0.16 + 0.08 * i, 0.93, 0.1 - 0.07 * (i % 2)] for i in range(5)]
SH20 = [[0.1 + 0.28 * (i % 2 * 2 - 1), 1.5 + 0.12 * (i % 2), -0.08] for i in range(6)]   # (round 1) a wide shaking arc, held away from her head
def PK20(p, up=UP20): return pen_at(p, up)
C20 = FC('S20', 0.0, [0.85, 2.45, 1.75], {'boardL': [-0.46, 0.93, 0.31], 'boardR': [0.46, 0.93, -0.31], 'boardFR': [0.46, 0.93, 0.31], 'boardBL': [-0.46, 0.93, -0.31], 'techHead': [TECH[0], 2.3, TECH[2]], 'shake': add(SH20[0], [0, 0.3, 0]), 'shake2': add(SH20[1], [0, 0.3, 0])}, top=0.07, bottom=0.74, lenses=range(26, 76), drift=(-0.05, -0.02, -0.12))
pk = []; tk = []; hk = []
seq = [(r(0.04 + 0.1 * i), W20a[i], UP20, 0.08) for i in range(6)] + [(SHK20[0], [0.1, 1.2, -0.08], [0.15, 1, -0.2], 0.12)] + [(r(SHK20[0] + 0.14 + 0.05 * i), add(SH20[i], [0, -0.25, 0]), [0.6 * (1 if i % 2 else -1), 1, 0.0], 0.045) for i in range(6)] + [(r(1.1 + 0.1 * i), W20b[i], UP20, 0.08) for i in range(5)]
for t, tip, up, d in seq:
    C_, R_, G_ = pen_at(tip, up); pk += [k(t, to=C_, dur=d, ease='inOut'), k(t, rotTo=ROT(R_), dur=d)]
    shk = SHK20[0] <= t <= SHK20[1] + 0.05
    hk.append(k(t, toon={'reach': {'R': R5(G_, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3 if shk else 0.55, 'mouth': 'teeth' if shk else 'line', 'brow': -0.7 if shk else -0.4, 'gy': 0.3 if shk else 0.8}, 'bend': {'spine': [0.12, 0, 0, 1, None] if shk else [0.5, 0, 0, 1, None], 'neck': [0.0, 0, 0, 1, None] if shk else [0.3, 0, 0, 1, None]}, 'hip': 0}, toonDur=d, toonEase='inOut'))
P20C, P20R, P20G = pen_at(W20a[0], UP20)
st.shot('S20', 'whiteVoid', setOpts=LAB, actors=[act('technicienne', TECH, 0, 'stand', 'neutral', keys=[k(0.0, look=[0, 0.93, 0]), k(0.0, toon={'reach': {'R': R5(P20G, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.55, 'mouth': 'line', 'brow': -0.4, 'gy': 0.8}, 'bend': {'spine': [0.5, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'hip': 0}, toonDur=0.0), *hk,
            k(1.62, look='camera', lookDur=0.15), k(1.62, toon={'reach': {'R': R5(pen_at(W20b[-1], UP20)[2], 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.6, 'mouth': 'wavy', 'brow': -0.2}, 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'hip': 0}, toonDur=0.12)])],
        props=[P('labo20', 'styRoom', pos=[0, 0, 0], opts={'w': 6, 'back': -2.0, 'wall': '#E4EDF0', 'band': '#B9CCD4', 'trim': '#7A9AA8', 'floor': '#C9D3D6'}), P('paillasse20', 'styForensic', pos=[0, 0, 0]),
               P('stylo20', 'styPen', pos=P20C, ry=P20R[1], rot=[P20R[0], 0, P20R[2]], opts={**PEN_STATE, 'chewed': True}, keys=pk)],
        cams=[C20])
st.cue('sfx:scratch', 'S20', 0.04, 0.3); st.cue('sfx:rattle', 'S20', r(SHK20[0] + 0.1), 0.3); st.cue('sfx:scratch', 'S20', 1.1, 0.3); st.cue('sfx:sad', 'S20', 1.6, 0.15)

# 21: his new pen is chained at the counter. Cam A, the counter from the public side: the clerk signs a register with his glossy red pen on the State's
#     chain (the ÉTAT tag beside it); cam B, wider from the hall: a queue at the counter, and he stands by the door, his breast pocket empty (ENCHAÎNÉ)
D21 = st.dur('S21'); CUT21 = 1.05
UP21 = [0.15, 1.0, -0.5]
W21 = [[-0.02 + 0.06 * (i % 2), 1.108, 0.02 + 0.015 * i] for i in range(8)]
P21 = [pen_at(w, UP21) for w in W21]
C21a = FC('S21a', 0.0, [0.6, 1.5, 1.7], {'penTop': add(P21[0][0], [0, 0.22, 0]), 'penTip': add(P21[0][0], [0, -0.22, 0]), 'tag': [0.42, 0.86, 0.4], 'anchor': ANCHOR, 'clerkTop': [CLERK[0], 2.38, CLERK[2]]}, top=0.07, bottom=0.76, lenses=range(26, 80), drift=(-0.06, -0.02, -0.14))
HERO21 = [-0.95, 0, 3.3]; PAT21 = [-0.72, 1.36, 3.42]
QUEUE = [('client1', [0.15, 0, 0.75]), ('client2', [0.35, 0, 1.45]), ('client3', [0.2, 0, 2.15])]
C21b = FC('S21b', CUT21, [0.2, 1.6, 5.4], {'heroTop': [HERO21[0], 2.36, HERO21[2]], 'heroChest': [HERO21[0], 1.15, HERO21[2]], 'heroL': [HERO21[0] - 0.35, 1.6, HERO21[2]], 'q3': [0.2, 2.36, 2.15], 'q1': [0.15, 2.36, 0.75]}, top=0.22, bottom=0.74, lenses=range(26, 76), drift=(-0.05, 0, -0.1))
KW = []
for i, (C_, R_, G_) in enumerate(P21[1:], 1):
    KW.append(k(r(0.05 + 0.11 * i), toon={'reach': {'R': R5(G_, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.55, 'mouth': 'line', 'gy': 0.8}, 'bend': {'spine': [0.3, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'hip': 0}, toonDur=0.1, toonEase='inOut'))
st.shot('S21', 'mairie', setOpts=MAIRIE, actors=[
        act('greffiere', CLERK, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, CH, 0.05]), k(0.0, toon={'reach': {'R': R5(P21[0][2], 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.55, 'mouth': 'line', 'gy': 0.8}, 'bend': {'spine': [0.3, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'hip': 0}, toonDur=0.0), *KW]),
        *[LIFE(act(w, p, 180 + 15 * (i - 1), 'stand', 'neutral', keys=[k(0.0, visible=False), k(CUT21, visible=True), k(0.0, look=[0, 1.6, -0.5]), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.0)]), D21, t0=r(CUT21 + 0.15 * i), amp=1.4) for i, (w, p) in enumerate(QUEUE)],
        # (round 1) he pats his empty breast pocket twice, then looks at us
        LIFE(act('mec', HERO21, 40, 'stand', 'neutral', keys=[k(0.0, look=[0.0, CH, 0.1]), k(0.0, toon={'face': {'lid': 0.65, 'low': 0.3, 'mouth': 'wavy', 'brow': -0.4}}, toonDur=0.0),
            *[k(r(1.2 + 0.12 * i), toon={'reach': {'R': R5(add(PAT21, [0, 0, 0.06 if i % 2 == 0 else 0.0]), 1, 0.04)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.6, 'mouth': 'wavy', 'brow': -0.4, 'gy': 0.7}}, toonDur=0.08) for i in range(4)],
            k(1.25, look=[-0.8, 1.2, 4.0], lookDur=0.1), k(1.75, look='camera', lookDur=0.15), k(1.75, toon={'face': {'lid': 0.6, 'mouth': 'wavy', 'brow': -0.5}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.15)]), D21, t0=1.9, breath=False)],
        props=[P('guichet', 'styCounter', pos=CNT, opts={}), P('registre21', 'register', pos=[0.0, CH + 0.005, 0.02], rot=[-1.25, 0, 0], opts={'left': 'REGISTRE', 'right': 'MARIAGES', 'w': 0.5, 'h': 0.34}),
               P('stylo21', 'styPen', pos=P21[0][0], ry=P21[0][1][1], rot=[P21[0][1][0], 0, P21[0][1][2]], opts={**PEN_RED, 'color': '#E8121E'},
                 keys=[*[k(r(0.05 + 0.11 * i), to=C_, dur=0.1, ease='inOut') for i, (C_, R_, G_) in enumerate(P21[1:], 1)], *[k(r(0.05 + 0.11 * i), rotTo=ROT(R_), dur=0.1) for i, (C_, R_, G_) in enumerate(P21[1:], 1)]]),
               PATCH('patch21', 'mec'), P('porte21', 'door', pos=[-1.55, 0, 3.75], ry=50, opts={'w': 1.0, 'h': 2.3})],
        tethers=[CHAINT('stylo21', anchor=ANCHOR)],
        cams=[C21a, C21b])
st.card('S21', 'ENCHAÎNÉ', at=r(st.at('S21', 'L15', 4) + 0.03))
st.cue('sfx:scratch', 'S21', 0.05, 0.25); st.cue('sfx:rattleShort', 'S21', 0.5, 0.2); st.cue('clang', 'S21', r(st.at('S21', 'L15', 4)), 0.25)

# ============================== the prison visiting booth (styBooth: the glass at z 0, he sits beyond it at -Z, the camera on the inmate side +Z)
BOOTH = {'color': '#C9D3CC'}
HERO22 = [0.0, 0.0, -0.5]
GUARD = [0.78, 0, 0.18]
# 22: this man has visiting on Thursdays. Frontal and still, then a slow push-in: in the foreground his red pen lies on a little stool on its chain
#     (ÉTAT tag), a guard standing beside it at attention; beyond the glass he sits holding the phone, JEUDI on the calendar behind him; he looks at
#     his pen, sighs, gives it a tiny wave, then looks at us; a slow blink finished well before the end
D22 = st.dur('S22')
C22F, C22T = [-0.12, 1.42, 2.55], [-0.12, 1.42, 2.35]   # (round 2) closer to the glass: his sigh and wave own the frame
C22 = FC('S22', 0.0, C22F, {'heroTop': [HERO22[0], 1.95, HERO22[2]], 'cal': [-0.55, 2.3, -1.7], 'stool': [-0.4, 0.62, 0.7], 'pen': [-0.4, 0.68, 0.7], 'guardFace': [GUARD[0] - 0.05, 1.95, GUARD[2]], 'heroChest': [0, 1.2, -0.62], 'tag': [-0.62, 0.55, 0.75]}, top=0.07, bottom=0.74, lenses=range(26, 84), drift=sub(C22T, C22F))
EAR = {'touch': {'L': ['face', 0.62, 0.02, -0.04, 1, 0.0]}, 'hands': {'L': 'grip'}}
F22 = {'lid': 0.55, 'mouth': 'line', 'brow': -0.2}
# (round 1) eyes down to the pen, a big sigh (rise, sag), a small wave of the free hand, then to us by 1.45 s; the blink done 0.5 s before the end
W22 = lambda dx: {**EAR, 'reach': {'R': R5([-0.3 + dx, 1.5, -0.28], 1, 0.05)}, 'hands': {'L': 'grip', 'R': 'open'}, 'face': {**F22, 'mouth': 'smile', 'lid': 0.5, 'gy': 0.6}, 'hip': 0, 'auto': 0.2}
KEYS22 = [k(0.0, look=[-0.4, 0.7, 0.7]), k(0.0, toon={**EAR, 'face': {**F22, 'gy': 0.6}, 'hip': 0, 'auto': 0.2}, toonDur=0.0),
          k(0.3, toon={**EAR, 'face': {**F22, 'lid': 0.3, 'gy': 0.6, 'mouth': 'o', 'brow': 0.3}, 'sq': [0.96, 1.06, 0.96], 'hip': 0, 'auto': 0.2}, toonDur=0.18, toonEase='out'),
          k(0.5, toon={**EAR, 'face': {**F22, 'lid': 0.8, 'gy': 0.6, 'mouth': 'wavy', 'brow': -0.4}, 'sq': [1.07, 0.92, 1.07], 'hip': 0, 'auto': 0.2}, toonDur=0.25, toonEase='inOut'),
          k(0.8, toon=W22(0.0), toonDur=0.12, toonEase='out'), *[k(r(0.92 + 0.1 * i), toon=W22(0.1 if i % 2 == 0 else -0.02), toonDur=0.08) for i in range(4)],
          k(1.35, toon={**EAR, 'face': {**F22, 'gy': 0.0}, 'hip': 0, 'auto': 0.2}, toonDur=0.12), k(1.35, look='camera', lookDur=0.12),
          k(2.0, toon={**EAR, 'face': {**F22, 'lid': 1.0}, 'hip': 0, 'auto': 0.2}, toonDur=0.12), k(2.18, toon={**EAR, 'face': {**F22, 'lid': 0.55}, 'hip': 0, 'auto': 0.2}, toonDur=0.12)]
st.shot('S22', 'whiteVoid', setOpts=BOOTH, actors=[act('mec', HERO22, 0, 'sit', 'neutral', keys=KEYS22),
        LIFE(act('gardien', GUARD, -25, 'stand', 'neutral', scale=0.86, keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}, 'hip': 0, 'auto': 0.1}, toonDur=0.0), k(1.2, look=[-0.4, 0.7, 0.7], lookDur=0.2), k(1.75, look='camera', lookDur=0.2)]), D22, t0=0.6, breath=True)],
        props=[P('parloir', 'styBooth', pos=[0, 0, 0], opts={'stool': [-0.4, 0.7], 'calX': -0.55}), P('chaise22', 'chair', pos=[0, 0, -0.68], opts={'color': '#5A6068'}),
               P('tel22', 'handset', on={'actor': 'mec', 'joint': 'head', 'offset': [0.2, 0.2, 0.03]}, opts={'len': 0.32, 'rot': [-0.35, r(-PI / 2), 0.0], 'color': '#2A2D33'})],
        cams=[C22])
st.cue('sfx:sad', 'S22', 0.45, 0.2); st.cue('sfx:tick', 'S22', 0.92, 0.1); st.cue('sfx:tick', 'S22', 1.12, 0.1)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
BIG = {'width': 1.0, 'headWidth': 1.2}
KID = {'height': 0.5, 'width': 0.8, 'headScale': 1.12}   # (round 1) about 60 % of an adult
CUSTOMS = lambda seed: {'preset': 'cop', 'seed': seed, 'suit': '#3F5B4E', 'pants': '#2F453B', 'lapel': '#2F453B', 'tie': '#2F453B', 'shirt': '#DCE3DA', 'cuff': '#3F5B4E', 'hatColor': '#2F453B', 'hatBand': '#C9A24B', 'gloves': '#2E6FD8', 'build': BIG, 'toon': EX}
st.write("Le stylo", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecPyj': {'preset': 'mecPyjama', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}},
    'greffiere': {'preset': 'femme', 'seed': 921, 'suit': '#7A5A8A', 'lapel': '#F2EDE4', 'glasses': True, 'hair': 'bun', 'hairColor': '#4A3020', 'build': {'width': 0.92, 'headWidth': 1.22}, 'toon': EX},
    'commis': {'preset': 'boss', 'seed': 922, 'glasses': True, 'build': BIG, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 923, 'sash': ['#6A3D9A', '#E8C766', '#6A3D9A'], 'sashW': 0.14, 'hairColor': '#BDBDBD', 'suit': '#4A4F5A', 'lapel': '#4A4F5A', 'tie': '#7A2333', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'mariee': {'preset': 'madame', 'seed': 924, 'suit': '#F7F4EE', 'lapel': '#F7F4EE', 'pants': '#F7F4EE', 'shoes': '#F7F4EE', 'skin': '#E8C09A', 'hair': 'bun', 'hairColor': '#5A3A22', 'glasses': False, 'build': {'width': 0.88, 'headWidth': 1.22}, 'toon': EX},
    'marie': {'preset': 'politique', 'seed': 925, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#E8C766', 'hairColor': '#3A2A20', 'build': BIG, 'toon': EX},
    'infirmiere': {'preset': 'doctor', 'seed': 926, 'hair': 'bun', 'hairColor': '#6A4028', 'glasses': False, 'lipstick': True, 'build': {'width': 0.92, 'headWidth': 1.22}, 'toon': EX},
    'pere1': {'preset': 'worker', 'seed': 927, 'hat': 'none', 'build': BIG, 'toon': EX}, 'pere2': {'preset': 'sportif', 'seed': 928, 'build': BIG, 'toon': EX},
    'pere3': {'preset': 'boss', 'seed': 929, 'glasses': False, 'build': BIG, 'toon': EX},
    'presentateur': {'preset': 'politique', 'seed': 930, 'facial': 'stubble', 'hair': 'spiky', 'hairColor': '#2A2420', 'suit': '#3A4256', 'lapel': '#3A4256', 'tie': '#B5141C', 'build': BIG, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 931, 'hairColor': '#CFCFCF', 'suit': '#23262E', 'lapel': '#23262E', 'tie': '#5B2C83', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.06}, 'toon': EX},
    'president2': {'preset': 'politique', 'seed': 931, 'hairColor': '#CFCFCF', 'suit': '#23262E', 'lapel': '#23262E', 'tie': '#5B2C83', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.06}, 'toon': EX},
    'ministre1': {'preset': 'politique', 'seed': 932, 'suit': '#4A4F5A', 'lapel': '#4A4F5A', 'glasses': True, 'build': BIG, 'toon': EX},
    'ministre2': {'preset': 'politique', 'seed': 933, 'suit': '#5A4A3A', 'lapel': '#5A4A3A', 'hairColor': '#8A8A86', 'build': BIG, 'toon': EX},
    'douanier1': CUSTOMS(934), 'douanier2': CUSTOMS(935),
    'enfant1': {'preset': 'gamin', 'seed': 936, 'build': KID, 'toon': EX}, 'enfant2': {'preset': 'gamin', 'seed': 937, 'suit': '#E8463C', 'build': KID, 'toon': EX}, 'enfant3': {'preset': 'gamin', 'seed': 938, 'suit': '#F2B630', 'build': KID, 'toon': EX},
    'mere': {'preset': 'mamie', 'seed': 939, 'build': {'height': 0.86, 'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'flic': {'preset': 'cop', 'seed': 940, 'build': BIG, 'toon': EX},
    **{f'commando{i}': {'preset': 'swat', 'hat': 'none', 'hair': 'bald', 'seed': 940 + i, 'gloves': '#22252B', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for i in (1, 2, 3, 4)},
    **{f'commando{i}d': {'preset': 'swat', 'hat': 'none', 'hair': 'bald', 'seed': 940 + i, 'suit': '#6F6C66', 'pants': '#5E5B56', 'shirt': '#6F6C66', 'cuff': '#6F6C66', 'lapel': '#5E5B56', 'gloves': '#3A3A3C', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for i in (1, 2, 3)},   # (round 2) dark gear under a light dust layer
    'technicienne': {'preset': 'doctor', 'seed': 945, 'hair': 'bun', 'hairColor': '#3A2A20', 'glasses': True, 'lipstick': True, 'build': {'width': 0.92, 'headWidth': 1.22}, 'toon': EX},
    'client1': {'preset': 'madame', 'seed': 946, 'build': BIG, 'toon': EX}, 'client2': {'preset': 'worker', 'seed': 947, 'hat': 'none', 'build': BIG, 'toon': EX}, 'client3': {'preset': 'tourist', 'seed': 948, 'build': BIG, 'toon': EX},
    'gardien': {'preset': 'cop2', 'seed': 949, 'suit': '#3A3F48', 'pants': '#2A2E36', 'lapel': '#2A2E36', 'hatColor': '#2A2E36', 'build': {'width': 1.1, 'headWidth': 1.2, 'belly': 0.06}, 'toon': EX},
})
