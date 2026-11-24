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
(sash in invented teal and gold) holds up the empty chain, slaps the register shut and a SUSPENDU sign drops onto it; bride and groom turn to us.
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

# 1: the hook. From behind the counter at its height: he signs with the brass pen chained to the eyebolt (scribbles), lifts it absently: the chain
#    goes taut and snaps (a pop, the cut chain drops over the edge), he clips the pen into his breast pocket beside his red pen without looking
D1 = st.dur('S01'); SNAP1 = 0.62; CLIP1 = 1.02
HERO1 = [0.05, 0, 0.74]
UP1 = [0.18, 1.0, 0.55]
W1 = [[0.14, 1.108, 0.1], [0.2, 1.108, 0.12], [0.13, 1.108, 0.14], [0.21, 1.108, 0.16], [0.15, 1.108, 0.17]]
PEN1 = [pen_at(w, UP1) for w in W1]
LIFT1C, LIFT1R, LIFT1G = pen_at([0.24, 1.36, 0.36], [0.05, 1.0, 0.25])
PK1 = [-0.03, 1.5, 0.53]                                                  # the pocket, world (he faces -Z: his left is -X)
PK1C, PK1R, PK1G = pen_at(add(PK1, [0, -0.21, 0]), [0, 1, 0], grip=0.33)
C1 = FC('S01', 0.0, [-0.55, 1.3, -1.35], {'headTop': [HERO1[0], 2.36, HERO1[2]], 'reg': [0.15, 1.1, 0.12], 'anchor': ANCHOR, 'lift': LIFT1C, 'pocket': PK1, 'chin': [HERO1[0], 1.75, HERO1[2]]}, top=0.07, bottom=0.74, drift=(0.05, 0.0, 0.1))
FW1 = {'lid': 0.55, 'mouth': 'line', 'gy': 0.8}
HR = lambda g, f, extra=None: {'reach': {'R': R5(g, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': f, 'hip': 0, **(extra or {})}
KEYS1 = [k(0.0, look=[0.15, 1.1, 0.14]), k(0.0, toon=HR(PEN1[0][2], FW1, {'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1, None]}}), toonDur=0.0),
         *[k(r(0.08 + 0.1 * i), toon=HR(PEN1[i][2], FW1, {'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.2, 0, 0, 1, None]}}), toonDur=0.09, toonEase='inOut') for i in range(1, 5)],
         k(0.5, toon=HR(LIFT1G, {**FW1, 'gy': 0.2, 'gx': 0.5}, {'bend': {'spine': [0.05, 0, 0, 1, None]}}), toonDur=0.12, toonEase='out'),
         k(0.55, look=[-1.2, 1.8, 2.0], lookDur=0.2),
         k(r(SNAP1 + 0.04), toon=HR(add(LIFT1G, [0, 0.05, 0]), {'lid': 0.5, 'mouth': 'line', 'brow': 0.1}, {'sq': [1.02, 0.98, 1.02]}), toonDur=0.05),
         k(0.72, toon=HR(PK1G, {'lid': 0.5, 'mouth': 'smirk', 'gx': 0.6}), toonDur=0.28, toonEase='inOut'),
         k(r(CLIP1 + 0.05), toon={'face': {'lid': 0.45, 'mouth': 'smirk', 'gx': 0.5}, 'hip': 0}, toonDur=0.2)]
st.shot('S01', 'mairie', setOpts=MAIRIE, actors=[act('mec', HERO1, 180, 'stand', 'neutral', keys=KEYS1)],
        props=[P('guichet', 'styCounter', pos=CNT, opts={'cutAt': SNAP1, 'swing': [[SNAP1, 0.6]]}),
               P('registre1', 'register', pos=[0.15, CH + 0.005, 0.1], ry=180, rot=[-1.25, 0, 0], opts={'left': 'REGISTRE', 'right': 'SIGNATURES', 'w': 0.5, 'h': 0.34}),
               P('stylo1', 'styPen', pos=PEN1[0][0], ry=PEN1[0][1][1], rot=[PEN1[0][1][0], 0, PEN1[0][1][2]], opts=PEN_STATE,
                 keys=[*[k(r(0.08 + 0.1 * i), to=PEN1[i][0], dur=0.09, ease='inOut') for i in range(1, 5)], *[k(r(0.08 + 0.1 * i), rotTo=ROT(PEN1[i][1]), dur=0.09) for i in range(1, 5)],
                       k(0.5, to=LIFT1C, dur=0.12, ease='out'), k(0.5, rotTo=ROT(LIFT1R), dur=0.12), k(r(SNAP1 + 0.04), to=add(LIFT1C, [0, 0.05, 0]), dur=0.05),
                       k(0.72, to=PK1C, dur=0.28, ease='inOut'), k(0.72, rotTo=ROT(PK1R), dur=0.28), k(CLIP1, visible=False)]),
               POCKET('poche1s', 'mec', 'state', keys=[k(0.0, visible=False), k(CLIP1, visible=True)]), POCKET('poche1r', 'mec', 'red'), PATCH('patch1', 'mec')],
        tethers=[CHAINT('stylo1', until=SNAP1, anchor=ANCHOR)],
        cams=[C1])
st.cue('sfx:scratch', 'S01', 0.08, 0.25); st.cue('sfx:twang', 'S01', r(SNAP1 - 0.04), 0.3); st.cue('clack', 'S01', SNAP1, 0.45); st.cue('sfx:click', 'S01', CLIP1, 0.4)

# 2: low at the counter's public side: the cut chain swings over the edge beside the ÉTAT tag in the foreground while he strolls off toward the
#    door, deadpan, the brass and the red pens in his breast pocket
D2 = st.dur('S02'); SW2 = r(SNAP1 - D1)
HERO2a, HERO2b = [0.05, 0, 0.95], [-0.35, 0, 2.0]
C2 = FC('S02', 0.0, [1.2, 1.15, 4.6], {'chainBot': [0.3, 0.72, 0.42], 'tag': [0.42, 0.92, 0.4], 'head0': [HERO2a[0], 2.36, HERO2a[2]], 'head1': [HERO2b[0], 2.36, HERO2b[2]], 'feet1': [HERO2b[0], 0.3, HERO2b[2]]}, top=0.08, bottom=0.74, lenses=range(26, 76), drift=(0.0, 0.0, -0.1))
st.shot('S02', 'mairie', setOpts=MAIRIE, actors=[act('mec', HERO2a, -20, 'stand', 'neutral', keys=[k(0.0, to=HERO2b, dur=D2, clip='walk', ease='linear', face=-20), k(0.0, look='camera'),
            k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.0), k(0.55, toon={'face': {'lid': 0.45, 'mouth': 'whistle'}}, toonDur=0.1)])],
        props=[P('guichet', 'styCounter', pos=CNT, opts={'cutAt': -1, 'swing': [[SW2, 0.6]], 'tagSwing': [[SW2, 0.25]]}), P('registre2', 'register', pos=[0.15, CH + 0.005, 0.1], ry=180, rot=[-1.25, 0, 0], opts={'left': 'REGISTRE', 'right': 'SIGNATURES', 'w': 0.5, 'h': 0.34}),
               POCKET('poche2s', 'mec', 'state'), POCKET('poche2r', 'mec', 'red'), PATCH('patch2', 'mec')],
        cams=[C2])
st.cue('sfx:step', 'S02', 0.1, 0.2); st.cue('sfx:whistle', 'S02', 0.5, 0.25)

# 3: the only pen of the State. The counter top from the public side: a clean pen outline in the grey dust, the cut chain still swinging, the ÉTAT
#    tag; behind, the clerk frozen in a take (eyes wide, a slow blink, her pupils trembling); a slow push-in
D3 = st.dur('S03'); SW3 = r(SW2 - D2)
C3F, C3T = [0.6, 1.55, 2.3], [0.5, 1.52, 1.95]
C3 = FC('S03', 0.0, C3F, {'dustL': [-0.25, CH, 0.0], 'dustR': [0.35, CH, 0.2], 'tag': [0.42, 0.86, 0.4], 'clerkTop': [CLERK[0], 2.36, CLERK[2]], 'clerkChin': [CLERK[0], 1.75, CLERK[2]]}, top=0.08, bottom=0.74, lenses=range(26, 76), drift=sub(C3T, C3F))
FCL = {'lid': 0.0, 'mouth': 'O', 'brow': 0.8, 'eye': 0.2, 'pupilSize': -0.4}
KEYS3 = [k(0.0, look=[0.1, CH, 0.1]), k(0.0, toon={'face': FCL, 'hip': 0, 'auto': 0.3, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.0),
         k(0.35, toon={'face': {**FCL, 'pupilShake': 1}, 'hip': 0, 'auto': 0.3, 'sq': [0.96, 1.06, 0.96]}, toonDur=0.1),
         k(0.85, toon={'face': {**FCL, 'lid': 1.0}, 'hip': 0, 'auto': 0.3}, toonDur=0.18, toonEase='inOut'),
         k(1.1, toon={'face': {**FCL, 'lid': 0.1, 'gx': -0.3, 'gy': -0.2}, 'hip': 0, 'auto': 0.3}, toonDur=0.15), k(1.15, look='camera', lookDur=0.2)]
st.shot('S03', 'mairie', setOpts=MAIRIE, actors=[act('greffiere', CLERK, 0, 'stand', 'surprised', keys=KEYS3)],
        props=[P('guichet', 'styCounter', pos=CNT, opts={'cutAt': -1, 'swing': [[SW3, 0.6]], 'tagSwing': [[SW3, 0.25]], 'dust': [0.05, 0.08, -0.15]})],
        cams=[C3])
st.cue('sfx:tense', 'S03', 0.05, 0.25); st.cue('sfx:tick', 'S03', 0.4, 0.15)

# ============================== the office: three desks, towers of files from each desk to the ceiling (3.0 m)
OFF = {**MAIRIE}
DESKS = [[-1.45, 0, -1.2], [1.35, 0, -0.75], [0.05, 0, -2.0]]
TOW4 = lambda d, ph: [[d[0] - 0.42, d[2] + 0.05, ph], [d[0] + 0.1, d[2] - 0.1, ph + 0.04], [d[0] + 0.55, d[2] + 0.08, ph + 0.08]]
# 4: the files piled up. Low wide angle from the floor: towers of files shoot up from every desk to the ceiling in a wave; a clerk seated at the right
#    desk disappears behind his own tower, his eyes going up with it
D4 = st.dur('S04')
CLERK2 = [1.3, 0.02, -1.38]
C4 = CAM('S04', 0.0, [0.6, 0.6, 2.6], [0.0, 2.2, -1.2], 72, {'ceilL': [-2.0, 3.0, -1.2], 'ceilR': [2.0, 3.0, -0.8], 'deskL': [-1.9, 0.76, -1.0], 'deskR': [1.9, 0.76, -0.4], 'clerk2': [CLERK2[0], 1.9, CLERK2[2]]}, to=[0.6, 0.55, 2.4], look2=[0.0, 2.3, -1.2])
GROW = [[0, 0.06], [0.12, 1.0]]
st.shot('S04', 'mairie', setOpts=OFF, actors=[act('commis', CLERK2, 0, 'sit', 'neutral', keys=[k(0.0, look=[1.35, 1.5, -0.75]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(0.25, look=[1.35, 3.0, -0.75], lookDur=0.35), k(0.25, toon={'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.15)])],
        props=[*[P(f'bureau4{i}', 'desk', pos=d, ry=180 if i == 1 else 0, opts={'color': '#7A5A3C', 'top': '#9C7A56'}) for i, d in enumerate(DESKS)], P('chaise4', 'chair', pos=[CLERK2[0], 0, CLERK2[2] - 0.2], ry=0, opts={'color': '#4A3A2A'}),
               *[P(f'dossiers4{i}', 'styFiles', pos=[0, 0.76, 0], opts={'towers': TOW4(d, 0.08 * i), 'ceil': 2.24, 'grow': GROW, 'blend': 0.3, 'ceiling': i == 0, 'ceilW': 10, 'ceilD': 9, 'ceilZ': 0.5}) for i, d in enumerate(DESKS)]],
        cams=[C4], look={'exposure': 1.15})
for i in range(3): st.cue('sfx:files', 'S04', r(0.12 + 0.12 * i), 0.35)
st.cue('thud', 'S04', 0.65, 0.35)

# 5: up to the ceiling. Medium: two towers pressed against the ceiling, trembling; the clerk of shot 3 slides into the gap between them, squeezed,
#    holding up the empty chain by its ÉTAT tag end; she looks at us
D5 = st.dur('S05')
CL5a, CL5b = [-0.02, 0, -1.25], [-0.02, 0, -0.62]
C5 = FC('S05', 0.0, [0.35, 1.85, 2.25], {'headTop': [0, 2.4, CL5b[2]], 'chain': [-0.28, 1.45, -0.4], 'towL': [-0.7, 2.95, -0.62], 'towR': [0.7, 2.95, -0.62], 'chin': [0, 1.7, CL5b[2]]}, top=0.06, bottom=0.72, drift=(0.0, 0.0, -0.12))
HCH5 = R5([-0.3, 2.1, -0.38], 1, 0.06)
st.shot('S05', 'mairie', setOpts=OFF, actors=[act('greffiere', CL5a, 0, 'stand', 'neutral', keys=[k(0.0, to=CL5b, dur=0.25, ease='out', glide=True, face=0), k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': HCH5}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.2}, 'sq': [0.82, 1.03, 1.0], 'hip': 0}, toonDur=0.0),
            k(0.45, toon={'reach': {'R': R5(add(HCH5[:3], [0, 0.06, 0]), 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.55, 'mouth': 'wavy', 'brow': -0.3}, 'sq': [0.8, 1.04, 1.0], 'hip': 0}, toonDur=0.15),
            *blink(0.78, {'lid': 0.55, 'mouth': 'wavy', 'brow': -0.3})])],
        props=[P('dossiers5', 'styFiles', pos=[0, 0, 0], opts={'towers': [[-0.5, -0.6, 0], [0.5, -0.62, 0], [-1.25, -1.4, 0], [1.3, -1.5, 0]], 'ceil': 3.0, 'grow': [[-1, 1.0]], 'ceiling': True, 'ceilW': 10, 'ceilD': 9, 'ceilZ': 0.5}),
               P('chaine5', 'styChain', on={'actor': 'greffiere', 'hand': 'R', 'offset': [0.0, -0.06, 0.02], 'hang': True}, opts={'len': 0.42, 'tagS': 1.3, 'swing': [[0.25, 0.45]]})],
        cams=[C5])
st.cue('sfx:squeak', 'S05', 0.05, 0.25); st.cue('sfx:rattleShort', 'S05', 0.3, 0.3)

# ============================== the wedding hall (the mairie with its desk)
WED = {**{k_: v for k_, v in MAIRIE.items() if k_ != 'desk'}, 'deskZ': -0.9, 'plate': 'MARIAGES', 'wall': '#EDE6D6'}
MAYOR = [0.0, 0, -1.62]
BOOK = [0.32, 0.82, -0.82]
# 6: weddings suspended. Frontal: the mayor behind the desk (sash in invented teal and gold) holds up the empty chain, slaps the open register shut
#    and a SUSPENDU sign drops onto it, swinging; bride and groom flank the desk in a V, turn to each other, then to us
D6 = st.dur('S06'); SHUT6 = 0.8; SIGN6 = 1.02
BRIDE, GROOM = [-0.82, 0, -0.5], [0.86, 0, -0.45]
C6 = FC('S06', 0.0, [0.2, 1.55, 4.4], {'mayorTop': [0, 2.4, MAYOR[2]], 'brideTop': [BRIDE[0], 2.3, BRIDE[2]], 'groomTop': [GROOM[0], 2.38, GROOM[2]], 'brideL': [BRIDE[0] - 0.35, 1.5, BRIDE[2]], 'groomR': [GROOM[0] + 0.35, 1.5, GROOM[2]], 'book': add(BOOK, [0, 0.0, 0]), 'chain': [0.55, 1.45, -1.45]}, top=0.07, bottom=0.74, lenses=range(26, 76), drift=(0, 0, -0.15))
HL6 = R5([0.5, 2.05, -1.4], 1, 0.06)
MK = lambda f, rr=None, extra=None: {'reach': {'L': HL6, **({'R': rr} if rr else {})}, 'hands': {'L': 'pinch', **({'R': 'open'} if rr else {})}, 'face': f, **(extra or {})}
KEYS6 = [k(0.0, look='camera'), k(0.0, toon=MK({'lid': 0.45, 'mouth': 'line', 'brow': -0.2}), toonDur=0.0),
         k(0.3, toon=MK({'lid': 0.5, 'mouth': 'wavy', 'brow': -0.4}, extra={'sq': [0.98, 1.03, 0.98]}), toonDur=0.15),
         k(0.62, toon=MK({'lid': 0.5, 'mouth': 'clench', 'brow': -0.6}, R5([-0.05, 1.45, -1.0], 1, 0.06), {'bend': {'spine': [0.1, 0, 0, 1, None]}}), toonDur=0.12, toonEase='out'),
         k(SHUT6, toon=MK({'lid': 0.6, 'mouth': 'clench', 'brow': -0.6}, R5([0.28, 1.24, -0.8], 1, 0.06), {'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04]}), toonDur=0.07, toonEase='in'),
         k(1.15, toon=MK({'lid': 0.45, 'mouth': 'line', 'brow': -0.2}, extra={'bend': {'spine': [0.0, 0, 0, 1, None]}}), toonDur=0.2)]
COUPLE = lambda who, ry0, f0, f1: act(who, BRIDE if who == 'mariee' else GROOM, ry0, 'stand', 'neutral', keys=[k(0.0, look=[0, 1.95, MAYOR[2]]), k(0.0, toon={'face': f0}, toonDur=0.0),
            k(r(SHUT6 + 0.05), toon={'face': {**f0, 'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.05), k(r(SHUT6 + 0.25), toon={'face': {**f0, 'lid': 0.0, 'mouth': 'o', 'brow': 0.6}}, toonDur=0.1),
            k(1.2, look=[0.0, 2.0, -0.7], lookDur=0.15), k(1.48, look='camera', lookDur=0.15), k(1.48, toon={'face': f1}, toonDur=0.12)])
st.shot('S06', 'mairie', setOpts=WED, actors=[LIFE(act('maire', MAYOR, 0, 'stand', 'neutral', keys=KEYS6), D6, t0=1.4, breath=False),
        COUPLE('mariee', 55, {'lid': 0.2, 'mouth': 'smile', 'brow': 0.3}, {'lid': 0.5, 'mouth': 'wavy', 'brow': -0.3}), COUPLE('marie', -55, {'lid': 0.3, 'mouth': 'smile'}, {'lid': 0.55, 'mouth': 'line', 'brow': -0.2})],
        props=[P('registre6', 'register', pos=BOOK, opts={'left': 'REGISTRE', 'right': 'MARIAGES'}, keys=[k(SHUT6, visible=False)]),
               P('livre6', 'styNotice', pos=add(BOOK, [0, 0.21, 0]), opts={'text': 'REGISTRE', 'w': 0.3, 'h': 0.4, 'bg': '#8E1F24', 'fg': '#E8C766', 'border': '#5A1014'}, keys=[k(0.0, visible=False), k(SHUT6, visible=True), k(SHUT6, squash=[1.08, 0.92, 1.0], dur=0.12)]),
               P('suspendu6', 'styNotice', pos=add(BOOK, [0.0, 0.43, 0.04]), opts={'text': 'SUSPENDU', 'w': 0.5, 'h': 0.2, 'string': True, 'stringH': 0.08, 'popAt': SIGN6, 'swing': [[SIGN6, 0.35]]}),
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
ANCHOR_T = [-0.72, 0, -0.95]
STUD = lambda flip, topple: P('studio', 'styStudio', pos=[0, 0, 0], opts={'flipAt': flip, 'toppleAt': topple, 'stackX': 0.32, 'countX': 1.02, 'screenY': 1.95})
# 8: special edition. Frontal medium: the unshaven anchor standing behind the desk, tie askew, under the red ÉDITION SPÉCIALE banner, the photo of the
#    brass pen on the big screen behind him (RECHERCHÉ), the day counter at the right; he speaks to us, worn out
D8 = st.dur('S08')
C8 = FC('S08', 0.0, [0.2, 1.75, 4.8], {'banner': [0, 3.05, -1.7], 'bannerL': [-1.45, 3.05, -1.7], 'bannerR': [1.45, 3.05, -1.7], 'anchorTop': [ANCHOR_T[0], 2.36, ANCHOR_T[2]], 'countR': [1.36, 1.6, -0.55], 'desk': [-0.9, 0.95, 0.0]}, top=0.06, bottom=0.74, lenses=range(26, 76), drift=(-0.05, 0, -0.3))
TALK = lambda t0, t1, f: [k(r(t0 + 0.15 * i), toon={'face': {**f, 'mouth': 'talk' if i % 2 == 0 else 'o'}, 'reach': {'R': R5([ANCHOR_T[0] - 0.2, 1.05, -0.62]), 'L': R5([ANCHOR_T[0] + 0.25, 1.05, -0.6])}, 'hands': {'R': 'open', 'L': 'open'}}, toonDur=0.07) for i in range(int((t1 - t0) / 0.15))]
FA = {'lid': 0.62, 'low': 0.3, 'brow': -0.3}
st.shot('S08', 'whiteVoid', setOpts=STUDIO, actors=[LIFE(act('presentateur', ANCHOR_T, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), *TALK(0.05, 1.15, FA)]), D8, t0=0.5, breath=False)],
        props=[STUD(5.0, 9.0)], cams=[C8])
st.cue('sfx:sting', 'S08', 0.0, 0.35)

# 9: eleventh day without a pen. The camera cranes down from high over the desk onto the counter: the number flips from DIX to ONZE (clack), the tall
#    stack of paper beside it topples over the desk, sheets sliding off; the anchor's eyes go to it, deadpan
D9 = st.dur('S09'); FLIP9 = 0.32; TOP9 = 0.72
C9 = CAM('S09', 0.0, [0.75, 3.3, 2.0], [0.35, 1.4, -0.75], 58, {'count': [1.02, 1.6, -0.55], 'stack': [0.32, 1.3, -0.35], 'anchor': [ANCHOR_T[0], 2.2, ANCHOR_T[2]]}, to=[1.0, 1.75, 1.3], look2=[0.85, 1.4, -0.5], ease='out')
st.shot('S09', 'whiteVoid', setOpts=STUDIO, actors=[act('presentateur', ANCHOR_T, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), *TALK(0.0, 0.6, FA),
            k(r(TOP9 + 0.05), look=[0.9, 1.0, -0.3], lookDur=0.15), k(r(TOP9 + 0.05), toon={'face': {**FA, 'mouth': 'line', 'gx': -0.6, 'gy': 0.5}}, toonDur=0.1), *blink(1.15, {**FA, 'mouth': 'line', 'gx': -0.6, 'gy': 0.5})])],
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
            k(0.4, toon=PK10({**FP, 'brow': 0.5, 'mouth': 'smile'}, [0.97, 1.04, 0.97]), toonDur=0.2), k(1.1, toon=PK10({**FP, 'mouth': 'smirk', 'brow': 0.4}), toonDur=0.2)]), D10, t0=0.7, breath=False)],
        props=[P('lettre10', 'styLetter', pos=LET10, keys=[k(0.4, to=add(LET10, [0, 0.04, 0]), dur=0.2)]), P('echarpe10', 'stySash', pos=SASH10, rot=[0, 0, 0.08]),
               P('flash10', 'flashBursts', pos=[0.3, 1.1, 0.0], face='camera', opts={'n': 5, 'w': 1.4, 'h': 0.6, 'at': [0.2, 0.55, 0.9, 1.25, 1.6], 'life': 0.15})],
        cams=[C10])
for t in [0.2, 0.55, 0.9, 1.25, 1.6]: st.cue('sfx:shutter', 'S10', t, 0.3)

# 11: impossible: he had to sign. Medium at the podium: a minister at the right holds out the empty chain (its ÉTAT tag, nothing at the end); the
#     president's eyes go to it, he lowers the letter; another minister at the left lowers the sash back over his head onto his chest; he sags
D11 = st.dur('S11'); LOW11 = 0.45; SASH11 = (0.95, 1.3)
MIN1, MIN2 = [0.92, 0, -2.15], [-0.95, 0, -2.45]
C11 = FC('S11', 0.0, [0.2, 1.75, 1.4], {'presTop': [0, 2.45, PRES[2]], 'min1Top': [MIN1[0], 2.4, MIN1[2]], 'min2Top': [MIN2[0], 2.4, MIN2[2]], 'sashHi': [0, 2.85, -2.45], 'chain': [0.5, 1.45, -2.05], 'podium': [0, 1.1, -2.0], 'min1R': [MIN1[0] + 0.3, 1.5, MIN1[2]], 'min2L': [MIN2[0] - 0.3, 1.5, MIN2[2]]}, top=0.06, bottom=0.72, lenses=range(26, 76), drift=(0, 0, -0.1))
LET11a, LET11b = LET10, [0.42, 1.35, -2.18]
SA11a, SA11b = [0.0, 2.9, -2.42], [0.0, 1.52, -2.33]
PK11 = lambda lp, f, sq=None, extra=None: {'reach': {'L': R5(add(lp, [0.0, -0.26, -0.02]), 1, 0.06)}, 'hands': {'L': 'pinch'}, 'face': f, 'hip': 0, **({'sq': sq} if sq else {}), **(extra or {})}
SAGF = {'lid': 0.75, 'low': 0.3, 'mouth': 'wavy', 'brow': -0.5}
st.shot('S11', 'pressRoom', setOpts=PRESS, actors=[
        act('president2', PRES, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=PK11(LET11a, {**FP, 'mouth': 'smirk'}), toonDur=0.0),
            k(0.22, look=[0.55, 1.5, -2.0], lookDur=0.15), k(0.22, toon=PK11(LET11a, {'lid': 0.1, 'mouth': 'o', 'brow': 0.6, 'gx': -0.5, 'gy': 0.4}), toonDur=0.1),
            k(LOW11, toon=PK11(LET11b, {'lid': 0.5, 'mouth': 'wavy', 'brow': -0.3, 'gy': 0.4}, [1.02, 0.98, 1.02]), toonDur=0.35, toonEase='inOut'),
            k(SASH11[1], toon=PK11(LET11b, SAGF, [1.06, 0.92, 1.06], {'bend': {'spine': [0.12, 0, 0, 1, None], 'neck': [0.15, 0, 0, 1, None]}}), toonDur=0.12, toonEase='out'),
            k(1.45, look='camera', lookDur=0.2), *blink(1.62, SAGF)]),
        LIFE(act('ministre1', MIN1, -70, 'stand', 'neutral', keys=[k(0.0, look=[0, 1.95, PRES[2]]), k(0.0, toon={'reach': {'R': R5([0.55, 1.72, -2.0], 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
            k(0.3, toon={'reach': {'R': R5([0.5, 1.78, -2.0], 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.15)]), D11, t0=0.7, breath=False),
        LIFE(act('ministre2', MIN2, 55, 'stand', 'neutral', keys=[k(0.0, look=[0, 2.4, PRES[2]]),
            k(0.0, toon={'reach': {'R': R5(add(SA11a, [-0.08, -0.35, 0.05]), 1, 0.06), 'L': R5(add(SA11a, [0.08, 0.25, 0.05]), 1, 0.06)}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(SASH11[0], toon={'reach': {'R': R5(add(SA11b, [-0.15, -0.2, 0.08]), 1, 0.06), 'L': R5(add(SA11b, [0.12, 0.3, 0.08]), 1, 0.06)}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=SASH11[1] - SASH11[0], toonEase='inOut'),
            k(1.45, toon={'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.25)]), D11, t0=0.4, breath=False)],
        props=[P('lettre11', 'styLetter', pos=LET11a, keys=[k(LOW11, to=LET11b, dur=0.35, ease='inOut'), k(LOW11, rotTo=[-0.5, 0, 0.15], dur=0.35)]),
               P('echarpe11', 'stySash', pos=SA11a, rot=[0, 0, 0.62], keys=[k(SASH11[0], to=SA11b, dur=SASH11[1] - SASH11[0], ease='inOut')]),
               P('chaine11', 'styChain', on={'actor': 'ministre1', 'hand': 'R', 'offset': [0.0, -0.06, 0.02], 'hang': True}, opts={'len': 0.36, 'tagS': 1.2, 'swing': [[0.0, 0.3]]})],
        cams=[C11])
st.cue('sfx:rattleShort', 'S11', 0.05, 0.3); st.cue('sfx:slideDownSlow', 'S11', LOW11, 0.2); st.cue('sfx:zip', 'S11', SASH11[0], 0.2)

# ============================== the school gate: the facade (ÉCOLE), the customs' folding table at z -0.6
SCHOOL = {'color': '#CFE3F0'}
YARD = lambda: P('cour', 'styRoom', pos=[0, 0, 0], opts={'w': 10, 'h': 3.6, 'back': -2.4, 'wall': '#EAD9B6', 'band': '#C98A5A', 'trim': '#8A5A3A', 'floor': '#A3A7AC', 'floorD': 9, 'posters': [{'text': 'ÉCOLE', 'x': 1.0, 'y': 2.9, 'w': 1.4, 'h': 0.42, 'bg': '#2E5E8A'}]})
TBL12 = [0.0, 0, -0.6]
DOU1, DOU2 = [-0.42, 0, -1.25], [0.5, 0, -1.2]
KIDS = [('enfant1', [1.25, 0, 0.15]), ('enfant2', [1.75, 0, 0.75]), ('enfant3', [2.25, 0, 1.35])]
CUT13 = [0.95, 0, -1.55]
# 12: customs searched every pencil case. Low tracking along the queue: two customs officers (blue gloves, caps) empty pencil cases onto a folding
#     table marked DOUANE, one holds a pencil up to his eye; the children wait in line with open schoolbags
D12 = st.dur('S12')
C12F, C12T = [-1.6, 1.1, 4.6], [-1.2, 1.1, 4.5]
C12 = FC('S12', 0.0, C12F, {'dou1Top': [DOU1[0], 2.4, DOU1[2]], 'dou2Top': [DOU2[0], 2.4, DOU2[2]], 'kid3Top': [2.25, 1.65, 1.35], 'kid1': [1.25, 1.5, 0.15], 'table': [0.0, 0.55, -0.25], 'dou1L': [DOU1[0] - 0.35, 1.5, DOU1[2]]}, top=0.07, bottom=0.74, lenses=range(26, 90), drift=sub(C12T, C12F), extra={'sign': [1.0, 3.1, -2.4]})
SHAKE = lambda who, p, ry, f, hx: act(who, p, ry, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 0.8, -0.6]), *[k(r(0.15 * i), toon={'reach': {'R': R5([hx + 0.06 * (i % 2), 1.15 + 0.05 * (i % 2), -0.65], 1, 0.06), 'L': R5([hx + 0.25, 1.1, -0.62], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': f, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.12) for i in range(8)]])
st.shot('S12', 'whiteVoid', setOpts=SCHOOL, actors=[
        SHAKE('douanier1', DOU1, 15, {'lid': 0.55, 'mouth': 'line', 'brow': -0.5}, -0.55),
        LIFE(act('douanier2', DOU2, -15, 'stand', 'neutral', keys=[k(0.0, look=[0.45, 1.95, -0.85]), k(0.0, toon={'reach': {'R': R5([0.42, 1.95, -0.85], 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.7, 'lidR': 1.0, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.0)]), D12, t0=0.6, breath=False),
        *[LIFE(act(w, p, -135 + 10 * i, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.0, -0.6] if i else 'camera'), k(0.0, toon={'face': {'lid': 0.3 + 0.1 * i, 'mouth': ['wavy', 'line', 'o'][i]}, 'hip': 0.6 * (1 - i)}, toonDur=0.0)]), D12, t0=0.2 + 0.25 * i, amp=1.5) for i, (w, p) in enumerate(KIDS)]],
        props=[YARD(), P('table12', 'styPencilTable', pos=TBL12, opts={'n': 4, 'pencils': 16}), P('douane12', 'styNotice', pos=[0.0, 0.5, -0.24], opts={'text': 'DOUANE', 'w': 0.8, 'h': 0.24, 'bg': '#1B2A4A', 'fg': '#F4EEDC', 'border': '#C9A24B'}),
               P('crayon12', 'styPencil', pos=[0.42, 1.98, -0.82], rot=[0, 0, 0.2]), P('carton12', 'styCutout', pos=CUT13, ry=-20),
               *[P(f'sac_{w}', 'backpack', on={'actor': w, 'joint': 'torso', 'offset': [0, 0.25, -0.18]}) for w, _ in KIDS]],
        cams=[C12])
st.cue('sfx:rattle', 'S12', 0.05, 0.3); st.cue('sfx:zip', 'S12', 0.5, 0.25)

# 13: an officer holds a tiny pencil up against the cardboard cut-out of the brass pen, compares, shakes his head; a child looks up at the cut-out
D13 = st.dur('S13')
OFF13 = [0.35, 0, -1.05]
PEN13 = [0.62, 1.28, -1.3]
C13 = FC('S13', 0.0, [1.75, 1.6, 3.2], {'cutTop': [CUT13[0], 1.55, CUT13[2]], 'cutFoot': [CUT13[0], 0.4, CUT13[2]], 'offTop': [OFF13[0], 2.8, OFF13[2]], 'pencil': PEN13, 'kid': [1.45, 1.45, -0.25]}, top=0.12, bottom=0.74, lenses=range(26, 76), drift=(-0.05, 0, -0.1))
NOD = [k(r(0.45 + 0.12 * i), toon={'reach': {'R': R5(add(PEN13, [-0.02, -0.06, 0.05]), 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.55, 'mouth': 'line', 'brow': -0.6}, 'bend': {'neck': [0, 0, 0.35 * (1 if i % 2 else -1), 1, None]}}, toonDur=0.1) for i in range(4)]
st.shot('S13', 'whiteVoid', setOpts=SCHOOL, actors=[
        act('douanier2', OFF13, 30, 'stand', 'neutral', keys=[k(0.0, look=PEN13), k(0.0, toon={'reach': {'R': R5(add(PEN13, [-0.02, -0.06, 0.05]), 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.6, 'lidR': 1.0, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.0), *NOD, k(1.0, look='camera', lookDur=0.15)]),
        LIFE(act('enfant1', [1.45, 0, -0.25], -110, 'stand', 'neutral', keys=[k(0.0, look=[CUT13[0], 1.3, CUT13[2]]), k(0.0, toon={'face': {'lid': 0.0, 'mouth': 'o', 'brow': 0.6}}, toonDur=0.0)]), D13, t0=0.5)],
        props=[YARD(), P('table13', 'styPencilTable', pos=[-0.6, 0, -0.5], opts={'n': 3}), P('carton13', 'styCutout', pos=CUT13, ry=-20), P('crayon13', 'styPencil', pos=PEN13, rot=[0, 0, 0.05]),
               P('sac13', 'backpack', on={'actor': 'enfant1', 'joint': 'torso', 'offset': [0, 0.25, -0.18]})],
        cams=[C13])
st.cue('sfx:tick', 'S13', 0.45, 0.2); st.cue('sfx:tick', 'S13', 0.69, 0.2)

# ============================== the police station: a navy counter, the officer behind it, his mother in front
POL = {}
CNT14 = [0.0, 0, -0.4]
COP14, MUM = [-0.78, 0, -1.2], [0.12, 0, 0.45]
PH14a, PH14b = [0.1, 1.3, -0.05], [-0.08, 1.3, -0.42]
# 14: his mother turned him in. Over the officer's shoulder from behind the counter (a V): his small old mother slides his framed photo across the
#     counter toward the officer (and us): in it he stands deadpan with the brass pen out of his breast pocket; the officer's eyes go to it
D14 = st.dur('S14'); SL14 = (0.15, 0.6)
C14 = CAM('S14', 0.0, [0.3, 1.85, -2.5], [-0.12, 1.6, 0.0], 55, {'mumTop': [MUM[0], 2.1, MUM[2]], 'mumChin': [MUM[0], 1.55, MUM[2]], 'photo': add(PH14b, [0, 0.25, 0]), 'photoBot': add(PH14b, [0, -0.23, 0]), 'copHead': [COP14[0], 2.55, COP14[2]], 'copL': [COP14[0] - 0.25, 1.6, COP14[2]]}, to=[0.27, 1.85, -2.35])
st.shot('S14', 'policeStation', setOpts=POL, actors=[
        LIFE(act('mere', MUM, 180, 'stand', 'neutral', keys=[k(0.0, look=[COP14[0], 1.95, COP14[2]]), k(0.0, toon={'reach': {'R': R5(add(PH14a, [0.17, -0.1, 0.05]), 1, 0.05), 'L': R5(add(PH14a, [-0.17, -0.1, 0.05]), 1, 0.05)}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.5, 'mouth': 'smirk', 'brow': -0.3}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.0),
            k(SL14[0], toon={'reach': {'R': R5(add(PH14b, [0.17, -0.1, 0.05]), 1, 0.05), 'L': R5(add(PH14b, [-0.17, -0.1, 0.05]), 1, 0.05)}, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.55, 'mouth': 'smirk', 'brow': -0.4}, 'bend': {'spine': [0.45, 0, 0, 1, None]}}, toonDur=SL14[1] - SL14[0], toonEase='inOut'),
            k(0.85, toon={'face': {'lid': 0.5, 'mouth': 'smirk', 'brow': -0.4}, 'bend': {'spine': [0.1, 0, 0, 1, None]}}, toonDur=0.2), k(0.9, look='camera', lookDur=0.2)]), D14, t0=1.0, breath=False),
        act('flic', COP14, 25, 'stand', 'neutral', keys=[k(0.0, look=[MUM[0], 1.7, MUM[2]]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0), k(0.55, look=PH14b, lookDur=0.15),
            k(0.5, toon={'reach': {'R': R5(add(PH14b, [-0.22, -0.05, -0.04]), 1, 0.05)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.2, toonEase='out')])],
        props=[P('guichet14', 'styCounter', pos=CNT14, opts={'plate': 'POLICE', 'tag': False, 'bolt': False, 'color': '#3E5578', 'panel': '#34496A', 'top': '#1E2A3E'}),
               P('photo14', 'styPhoto', pos=PH14a, ry=180, opts={'stand': True}, keys=[k(SL14[0], to=PH14b, dur=SL14[1] - SL14[0], ease='inOut')])],
        cams=[C14])
st.cue('sfx:scratch', 'S14', SL14[0], 0.2); st.cue('sfx:tick', 'S14', SL14[1], 0.25)

# ============================== the block of flats at night (whiteVoid navy + styBlock: facade at z 0, storeys of 2.9 m, his balcony on floor 5)
NIGHTX = {'color': '#141C33'}
NLOOK = {'sun': 0.3, 'fill': 0.55, 'exposure': 1.05}
S_ = 2.9; HF = 5; BAL = [0.0, HF * S_, 0.55]
HELI = [1.6, 20.6, 2.6]; HSC = 1.0
def heli_lamp(h, ry=-90, s=HSC):
    a = math.radians(ry); v = [0, -0.5, 0.62]; return [r(h[0] + s * (v[0] * math.cos(a) + v[2] * math.sin(a))), r(h[1] + s * v[1]), r(h[2] + s * (-v[0] * math.sin(a) + v[2] * math.cos(a)))]
LAMP = heli_lamp(HELI)
BEAMTO = [0.0, HF * S_ + 0.2, 0.6]
def HELIP(pid, on=None, r1=1.1, to=BEAMTO, op=0.12):
    BR = aim_rot(LAMP, to)
    return [P(pid, 'chvHeli', pos=HELI, ry=-90, scale=HSC, opts={'rim': '#A9C2E6', 'rimW': 0.05, 'spin': 1.15}),
            P(pid + 'b', 'chvBeam', pos=LAMP, ry=BR[1], rot=[BR[0], 0, BR[2]], opts={'len': r(math.dist(LAMP, to) + 0.3), 'r': r1, 'r0': 0.12, 'op': op, 'fade': 0.7, 'lampR': 0.08, 'flare': 0.9, 'on': on or [[0, 1]]})]
SWAT = [('commando1', -0.62), ('commando2', 0.0), ('commando3', 0.62)]
MASKED = lambda who: [P(f'cagoule_{who}', 'balaclava', on={'actor': who, 'joint': 'head', 'offset': [0, 0, 0]}), P(f'casque_{who}', 'tacHelmet', on={'actor': who, 'joint': 'head', 'offset': [0, 0.47, 0]})]
def RIFLE(pid, grip, target, keys=None):
    a = aim_rot(target, grip); return P(pid, 'rifle', pos=grip, ry=a[1], rot=[a[0], 0, a[2]], scale=1.25, keys=keys or [])
ROPE = lambda who, x: {'a': {'prop': 'heli', 'offset': [r(x * 0.5), -0.75, 0.0]}, 'b': {'actor': who, 'hand': 'R'}, 'color': '#E9E2CF', 'sag': 0.0, 'radius': 0.02, 'minPx': 3}
# 15: special forces jumped onto his balcony. Night, low from the street: the block of flats, the navy helicopter over the roof, its searchlight on
#     his fifth-floor balcony; three masked commandos slide down their ropes toward it
D15 = st.dur('S15')
C15 = FC('S15', 0.0, [5.0, 1.2, 19.0], {'heliTop': [HELI[0], HELI[1] + 1.2, HELI[2]], 'rotL': [HELI[0] - 1.8, HELI[1] + 0.8, HELI[2]], 'rotR': [HELI[0] + 1.8, HELI[1] + 0.8, HELI[2] + 1.8], 'heliTail': [HELI[0] + 2.6, HELI[1], HELI[2]], 'heliNose': [HELI[0] - 1.2, HELI[1], HELI[2]], 'bal': [0, HF * S_ - 0.4, 1.1], 'balL': [-1.4, HF * S_, 0.0], 'floor3': [-3.0, 3 * S_, 0]}, top=0.06, bottom=0.74, lenses=range(26, 76), drift=(-0.1, 0.05, -0.4))
def SLIDE(who, x, y0, y1, D, land=None):
    keys = [k(0.0, to=[x, y1, 0.75], dur=D if land is None else land, ease='in' if land else 'linear', glide=True, face=0), k(0.0, look='camera')]
    keys += [k(0.0, toon={'reach': {'R': R5([x - 0.05, y0 + 2.5, 0.75], 1, 0.06), 'L': R5([x + 0.05, y0 + 2.2, 0.75], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.6}, 'auto': 0.2}, toonDur=0.0)]
    return keys
st.shot('S15', 'whiteVoid', setOpts=NIGHTX, look=NLOOK, actors=[act(w, [x, 18.4 - 0.4 * i, 0.75], 0, 'stand', 'angry', keys=[k(0.0, to=[x, 16.6 - 0.4 * i, 0.75], dur=D15, ease='linear', glide=True, face=0), k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': R5([x - 0.04, 21.0, 0.75], 1, 0.06), 'L': R5([x + 0.04, 20.6, 0.75], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.6}, 'auto': 0.2}, toonDur=0.0)]) for i, (w, x) in enumerate(SWAT)],
        props=[P('immeuble', 'styBlock', pos=[0, 0, 0], opts={'heroFloor': HF}), *HELIP('heli'), *[q for w, _ in SWAT for q in MASKED(w)]],
        tethers=[ROPE(w, x) for w, x in SWAT], cams=[C15])
st.cue('engine', 'S15', 0.0, 0.35, D15); st.cue('sfx:rotor', 'S15', 0.0, 0.4); st.cue('sfx:slideDown', 'S15', 0.1, 0.25)

# 16: at the balcony, in the beam: they drop the last metre onto it, squash on landing, and aim at his lit French window
D16 = st.dur('S16'); LAND16 = 0.32
C16 = FC('S16', 0.0, [3.3, HF * S_ + 0.6, 5.0], {'balL': [-1.15, HF * S_ - 0.3, 1.1], 'balR': [1.15, HF * S_ - 0.3, 1.1], 'c1Top': [-0.62, HF * S_ + 2.4, 0.6], 'c3Top': [0.62, HF * S_ + 2.4, 0.6], 'win': [0, HF * S_ + 2.2, 0.0], 'ropeHi': [0, HF * S_ + 3.4, 0.6]}, top=0.06, bottom=0.74, drift=(-0.1, 0.0, -0.25))
AIM16 = lambda x: {'reach': {'R': R5([x - 0.1, HF * S_ + 1.25, 0.36], 1, 0.06), 'L': R5([x - 0.02, HF * S_ + 1.32, 0.05], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.8}, 'auto': 0.3}
st.shot('S16', 'whiteVoid', setOpts=NIGHTX, look=NLOOK, actors=[act(w, [x, HF * S_ + 1.0 + 0.15 * i, 0.62], 180 - 20 * (i - 1), 'stand', 'angry', keys=[
            k(0.0, to=[x, HF * S_, 0.62], dur=r(LAND16 + 0.05 * i), ease='in', glide=True, face=180 - 20 * (i - 1)), k(0.0, look=[0, HF * S_ + 1.6, 0.0]),
            k(0.0, toon={'reach': {'R': R5([x - 0.04, HF * S_ + 3.4, 0.62], 1, 0.06), 'L': R5([x + 0.04, HF * S_ + 3.1, 0.62], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.6}, 'auto': 0.2}, toonDur=0.0),
            k(r(LAND16 + 0.05 * i), toon={**AIM16(x), 'sq': [1.25, 0.72, 1.25]}, toonDur=0.04), k(r(LAND16 + 0.05 * i + 0.1), toon={**AIM16(x), 'sq': [0.95, 1.06, 0.95]}, toonDur=0.08), k(r(LAND16 + 0.05 * i + 0.22), toon=AIM16(x), toonDur=0.1),
            k(r(0.8 + 0.08 * i), look='camera', lookDur=0.15)]) for i, (w, x) in enumerate(SWAT)],
        props=[P('immeuble', 'styBlock', pos=[0, 0, 0], opts={'heroFloor': HF}), *HELIP('heli'), *[q for w, _ in SWAT for q in MASKED(w)],
               *[RIFLE(f'fusil_{w}', [x - 0.1, HF * S_ + 1.25, 0.36], [x * 0.3, HF * S_ + 1.3, -1.0], keys=[k(0.0, visible=False), k(r(LAND16 + 0.05 * i + 0.1), visible=True)]) for i, (w, x) in enumerate(SWAT)]],
        tethers=[{**ROPE(w, x), 'until': r(LAND16 + 0.05 * i + 0.1)} for i, (w, x) in enumerate(SWAT)], cams=[C16])
for i in range(3): st.cue('thud', 'S16', r(LAND16 + 0.05 * i), 0.4)

# 17: the balcony gave way, and the three below. Wide and still from the street: it shakes, cracks show on the wall, it drops onto the empty one below,
#     the pair onto the next, the three onto the last, and the four come down onto the pavement in a neat stack, the commandos riding on top; dust
D17 = st.dur('S17'); CRACK17, BREAK17 = 0.06, 0.24
TH = 0.28; STACK = {2: 0.05 + TH, 3: 0.05 + 2 * TH, 4: 0.05 + 3 * TH, 5: 0.05 + 4 * TH}
def fall(y0, y1, t0, t1):
    """keys of an accelerating fall (y = y0 - d u^2)"""
    return [[r(t0 + (t1 - t0) * u), r(y0 - (y0 - y1) * u * u)] for u in (0.0, 0.35, 0.6, 0.8, 1.0)]
T5, T4, T3, T2 = BREAK17, 0.42, 0.56, 0.68; TG = 0.84
SL = {5: [[0.0, 5 * S_]] + fall(5 * S_, 4 * S_ + TH, T5, T4) + fall(4 * S_ + TH, 3 * S_ + 2 * TH, T4 + 0.02, T3) + fall(3 * S_ + 2 * TH, 2 * S_ + 3 * TH, T3 + 0.02, T2) + fall(2 * S_ + 3 * TH, STACK[5], T2 + 0.02, TG),
      4: [[0.0, 4 * S_], [T4, 4 * S_]] + fall(4 * S_, 3 * S_ + TH, T4 + 0.02, T3) + fall(3 * S_ + TH, 2 * S_ + 2 * TH, T3 + 0.02, T2) + fall(2 * S_ + 2 * TH, STACK[4], T2 + 0.02, TG),
      3: [[0.0, 3 * S_], [T3, 3 * S_]] + fall(3 * S_, 2 * S_ + TH, T3 + 0.02, T2) + fall(2 * S_ + TH, STACK[3], T2 + 0.02, TG),
      2: [[0.0, 2 * S_], [T2, 2 * S_]] + fall(2 * S_, STACK[2], T2 + 0.02, TG)}
LANDS = {4: T4, 3: T3, 2: T2, 5: TG}
FINAL = {f: [[0.0, STACK[f]]] for f in (2, 3, 4, 5)}
C17 = FC('S17', 0.0, [6.5, 2.2, 25.0], {'top': [0, 18.2, 0], 'heli': [HELI[0], HELI[1] + 1.0, HELI[2]], 'pave': [0, 0.0, 3.0], 'left': [-5.0, 9.0, 0], 'right': [5.0, 9.0, 0]}, top=0.06, bottom=0.74, lenses=range(30, 76), drift=(0.0, 0.0, 0.0))
def ride(t):
    ks = SL[5]
    if t <= ks[0][0]: return ks[0][1]
    for i in range(1, len(ks)):
        if t < ks[i][0]: a, b = ks[i - 1], ks[i]; return a[1] + (b[1] - a[1]) * (t - a[0]) / max(1e-6, b[0] - a[0])
    return ks[-1][1]
RIDE_T = sorted({r(x[0]) for x in SL[5]})
SITF = {'lid': 0.45, 'mouth': 'line', 'brow': -0.6}
def RIDER(w, x, i):
    keys = [k(0.0, look='camera')] + [k(RIDE_T[j], to=[x, r(ride(RIDE_T[j + 1])), 0.62], dur=r(RIDE_T[j + 1] - RIDE_T[j]), ease='linear', glide=True, face=180 - 20 * (i - 1)) for j in range(len(RIDE_T) - 1) if RIDE_T[j + 1] > RIDE_T[j]]
    keys += [k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.8}, 'auto': 0.2}, toonDur=0.0)]
    keys += [k(r(BREAK17 + 0.02), toon={'face': {'pop': 0.5, 'popLen': 0.2, 'lid': 0.0, 'mouth': 'O', 'brow': 1}, 'sq': [0.9, 1.12, 0.9], 'hairUp': 0, 'auto': 0.0}, toonDur=0.05), k(TG, toon={'face': SITF, 'sq': [1.3, 0.7, 1.3], 'auto': 0.0}, toonDur=0.04),
             k(r(TG + 0.1), toon={'face': SITF, 'sq': [1, 1, 1], 'auto': 0.2}, toonDur=0.15)]
    return act(w, [x, 5 * S_, 0.62], 180 - 20 * (i - 1), 'stand', 'angry', keys=keys)
st.shot('S17', 'whiteVoid', setOpts=NIGHTX, look=NLOOK, actors=[RIDER(w, x, i) for i, (w, x) in enumerate(SWAT)],
        props=[P('immeuble', 'styBlock', pos=[0, 0, 0], opts={'heroFloor': HF, 'slabs': {str(f): v for f, v in SL.items()}, 'land': {str(f): v for f, v in LANDS.items()}, 'crackAt': CRACK17, 'breakAt': BREAK17, 'dustAt': TG}),
               *HELIP('heli'), *[q for w, _ in SWAT for q in MASKED(w)]],
        cams=[C17], fx=[{'type': 'shake', 'at': TG, 'dur': 0.25, 'amount': 0.02}])
st.cue('sfx:crunch', 'S17', BREAK17, 0.5); st.cue('thud', 'S17', T4, 0.4); st.cue('thud', 'S17', T3, 0.45); st.cue('thud', 'S17', T2, 0.5); st.cue('thud', 'S17', TG, 0.9); st.cue('sfx:poof', 'S17', r(TG + 0.03), 0.4)

# 18: the stack on the pavement, closer and low: four slabs with crumpled rails, the three commandos sitting on top, unhurt, grey with dust, rifles still
#     aimed; the dust drifting; one blinks, one coughs a puff
D18 = st.dur('S18')
SEAT18 = STACK[5]
C18 = FC('S18', 0.0, [2.6, 0.85, 4.9], {'stackL': [-1.15, 0.0, 1.1], 'stackR': [1.15, 0.0, 1.1], 'c1': [-0.62, SEAT18 + 1.95, 0.85], 'c3': [0.62, SEAT18 + 1.95, 0.85], 'top': [0, SEAT18 + 2.1, 0.7]}, top=0.12, bottom=0.74, drift=(-0.05, 0.0, -0.15))
AIMS = lambda x, i: {'reach': {'R': R5([x - 0.1, SEAT18 + 1.2, 1.25], 1, 0.06), 'L': R5([x - 0.04, SEAT18 + 1.27, 1.5], 1, 0.06)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.5 + 0.1 * i, 'mouth': 'line', 'brow': -0.7}}
st.shot('S18', 'whiteVoid', setOpts=NIGHTX, look=NLOOK, actors=[LIFE(act(w, [x, r(SEAT18 - 0.43), 0.85], 180 - 20 * (i - 1) + 180, 'sit', 'neutral', keys=[k(0.0, look=[x * 1.5, 1.5, 4.0] if i != 1 else 'camera'), k(0.0, toon=AIMS(x, i), toonDur=0.0)]), D18, t0=0.2 + 0.2 * i, breath=True) for i, (w, x) in enumerate(SWAT)],
        props=[P('immeuble', 'styBlock', pos=[0, 0, 0], opts={'heroFloor': HF, 'slabs': {str(f): v for f, v in FINAL.items()}, 'land': {str(f): -1 for f in FINAL}, 'dustAt': r(TG - D17), 'litHero': True}),
               *[q for w, _ in SWAT for q in MASKED(w)], *[RIFLE(f'fusil_{w}', [x - 0.1, r(SEAT18 + 1.2), 1.25], [x * 2.0 - 1.5, r(SEAT18 + 1.3), 4.5]) for i, (w, x) in enumerate(SWAT)]],
        cams=[C18])
st.cue('sfx:poof', 'S18', 0.0, 0.25); st.cue('sfx:crunch', 'S18', 0.6, 0.15)

# ============================== his flat at night: the wall behind him, the searchlight through the window
FLAT = {'color': '#1A2238'}
HERO19 = [0.0, 0, -0.35]
COM19 = [0.9, 0, -0.12]
PK19 = [0.075, 1.46, -0.16]
# 19: the pen was in his pocket. Chewed. In pyjamas against his wall, hands up, in the white beam: the commando at his left reaches into his breast
#     pocket and pulls the brass pen out, holds it up in the beam (SAISI); his eyes follow it; cut in close on the cap: chewed flat, tooth marks; his
#     red pen stays clipped in the pocket
D19 = st.dur('S19'); GRAB19, PULL19 = 0.35, 0.62; CUT19 = r(st.at('S19', 'L13', 6) - 0.03)
UPP = [0.47, 2.06, 0.22]
PU19C, PU19R, PU19G = pen_at(add(UPP, [0, -0.2, 0.0]), [0.05, 1, 0.12], grip=0.12)
PK19C, PK19R, PK19G = pen_at(add(PK19, [0, -0.21, 0]), [0, 1, 0], grip=0.33)
C19a = FC('S19a', 0.0, [-0.25, 1.75, 2.9], {'heroTop': [HERO19[0], 2.36, HERO19[2]], 'handsUpL': [-0.55, 2.4, -0.3], 'comTop': [COM19[0], 2.4, COM19[2]], 'pen': PU19C, 'pocket': PK19, 'chest': [0, 1.2, -0.2]}, top=0.08, bottom=0.72, lenses=range(26, 76), drift=(0, 0, -0.15))
C19b = CAM('S19b', CUT19, [0.75, 2.2, 1.45], [0.3, 2.16, -0.1], 38, {'cap': add(PU19C, [0, 0.22, 0]), 'tip': add(PU19C, [0, -0.2, 0]), 'eyes': [0.0, 2.08, -0.3]}, to=[0.76, 2.2, 1.3])
BEAM19 = [-1.8, 4.8, 1.4]; BT19 = [0.25, 1.75, -0.3]; BR19 = aim_rot(BEAM19, BT19)
HUP = {'R': R5([-0.42, 2.25, -0.3], 1, 0.05), 'L': R5([0.42, 2.25, -0.3], 1, 0.05)}
FH = {'lid': 0.5, 'mouth': 'line', 'brow': 0.3}
st.shot('S19', 'whiteVoid', setOpts=FLAT, look=NLOOK, actors=[
        act('mecPyj', HERO19, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': FH, 'hip': 0}, toonDur=0.0),
            k(r(GRAB19 + 0.05), toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {**FH, 'gx': -0.5, 'gy': 0.7, 'mouth': 'o'}, 'hip': 0}, toonDur=0.1),
            k(r(PULL19 + 0.15), look=[0.5, 2.25, 0.3], lookDur=0.15), k(r(PULL19 + 0.15), toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'wavy', 'brow': 0.6, 'gx': -0.4, 'gy': -0.2}, 'sq': [0.97, 1.03, 0.97], 'hip': 0}, toonDur=0.12),
            k(1.15, toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.4, 'mouth': 'gulp', 'brow': 0.4, 'gx': -0.4}, 'hip': 0}, toonDur=0.1),
            k(1.35, look='camera', lookDur=0.15), k(1.35, toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.55, 'mouth': 'line', 'brow': -0.2}, 'hip': 0}, toonDur=0.12),
            k(r(CUT19 + 0.1), look=[0.5, 2.3, 0.2], lookDur=0.1), k(r(CUT19 + 0.1), toon={'reach': HUP, 'hands': {'R': 'open', 'L': 'open'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.2, 'gx': -0.6, 'gy': -0.4}, 'hip': 0}, toonDur=0.1)]),
        LIFE(act('commando4', COM19, -45, 'stand', 'neutral', keys=[k(0.0, look=PK19), k(0.0, toon={'reach': {'R': R5([0.55, 1.2, 0.2], 1, 0.06)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.7}, 'hip': 0}, toonDur=0.0),
            k(GRAB19, toon={'reach': {'R': R5(PK19G, 1, 0.06)}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.7}, 'hip': 0}, toonDur=0.2, toonEase='inOut'),
            k(PULL19, toon={'reach': {'R': R5(PU19G, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'smirk', 'brow': -0.5}, 'hip': 0}, toonDur=0.3, toonEase='out'), k(r(PULL19 + 0.1), look=PU19C, lookDur=0.2)]), D19, t0=1.0, breath=False)],
        props=[P('mur19', 'styRoom', pos=[0, 0, 0], opts={'w': 6, 'h': 3.2, 'back': -0.62, 'wall': '#9AA6BE', 'band': '#6E7A94', 'trim': '#3E4860', 'floor': '#4A4F5E'}),
               P('poche19s', 'styPen', on={'actor': 'mecPyj', 'joint': 'torso', 'offset': POCK_S}, opts={**PEN_STATE, 'chewed': True}, keys=[k(PULL19, visible=False)]), POCKET('poche19r', 'mecPyj', 'red'), PATCH('patch19', 'mecPyj', '#8FA9C8'),
               P('stylo19', 'styPen', pos=PK19C, ry=PK19R[1], rot=[PK19R[0], 0, PK19R[2]], opts={**PEN_STATE, 'chewed': True}, keys=[k(0.0, visible=False), k(PULL19, visible=True), k(PULL19, to=PU19C, dur=0.3, ease='out'), k(PULL19, rotTo=ROT(PU19R), dur=0.3)]),
               P('faisceau19', 'chvBeam', pos=BEAM19, ry=BR19[1], rot=[BR19[0], 0, BR19[2]], opts={'len': r(math.dist(BEAM19, BT19) + 0.6), 'r': 1.25, 'r0': 0.25, 'op': 0.2, 'fade': 0.75, 'lampR': 0.0, 'flare': 0.0}),
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
SH20 = [[0.1 + 0.08 * (i % 2 * 2 - 1), 1.45, -0.32] for i in range(6)]
def PK20(p, up=UP20): return pen_at(p, up)
C20 = FC('S20', 0.0, [0.85, 2.45, 1.75], {'boardL': [-0.46, 0.93, 0.31], 'boardR': [0.46, 0.93, -0.31], 'boardFR': [0.46, 0.93, 0.31], 'boardBL': [-0.46, 0.93, -0.31], 'techHead': [TECH[0], 2.3, TECH[2]], 'shake': SH20[0]}, top=0.07, bottom=0.74, lenses=range(26, 76), drift=(-0.05, -0.02, -0.12))
pk = []; tk = []; hk = []
seq = [(r(0.04 + 0.1 * i), W20a[i], UP20, 0.08) for i in range(6)] + [(SHK20[0], [0.1, 1.15, -0.32], [0.15, 1, -0.2], 0.12)] + [(r(SHK20[0] + 0.14 + 0.05 * i), add(SH20[i], [0, -0.25, 0]), [0.05 * (1 if i % 2 else -1), 1, -0.2], 0.045) for i in range(6)] + [(r(1.1 + 0.1 * i), W20b[i], UP20, 0.08) for i in range(5)]
for t, tip, up, d in seq:
    C_, R_, G_ = pen_at(tip, up); pk += [k(t, to=C_, dur=d, ease='inOut'), k(t, rotTo=ROT(R_), dur=d)]
    hk.append(k(t, toon={'reach': {'R': R5(G_, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.55, 'mouth': 'clench' if SHK20[0] <= t <= SHK20[1] + 0.05 else 'line', 'brow': -0.4, 'gy': 0.8}, 'bend': {'spine': [0.5, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'hip': 0}, toonDur=d, toonEase='inOut'))
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
C21a = FC('S21a', 0.0, [0.75, 1.45, 1.6], {'pen': P21[0][0], 'tag': [0.42, 0.86, 0.4], 'clerkTop': [CLERK[0], 2.36, CLERK[2]], 'anchor': ANCHOR, 'reg': [0.0, CH, 0.0]}, top=0.08, bottom=0.74, lenses=range(26, 76), drift=(-0.04, 0, -0.1))
HERO21 = [-0.95, 0, 3.3]
QUEUE = [('client1', [0.15, 0, 0.75]), ('client2', [0.35, 0, 1.45]), ('client3', [0.2, 0, 2.15])]
C21b = FC('S21b', CUT21, [0.55, 1.6, 5.6], {'clerkTop': [CLERK[0], 2.36, CLERK[2]], 'heroTop': [HERO21[0], 2.36, HERO21[2]], 'heroChest': [HERO21[0], 1.2, HERO21[2]], 'heroL': [HERO21[0] - 0.3, 1.6, HERO21[2]], 'q3': [0.2, 2.36, 2.15], 'q1': [0.15, 2.36, 0.75], 'counter': [0.6, CH, 0.3]}, top=0.22, bottom=0.74, lenses=range(26, 76), drift=(-0.05, 0, -0.1))
KW = []
for i, (C_, R_, G_) in enumerate(P21[1:], 1):
    KW.append(k(r(0.05 + 0.11 * i), toon={'reach': {'R': R5(G_, 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.55, 'mouth': 'line', 'gy': 0.8}, 'bend': {'spine': [0.3, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'hip': 0}, toonDur=0.1, toonEase='inOut'))
st.shot('S21', 'mairie', setOpts=MAIRIE, actors=[
        act('greffiere', CLERK, 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, CH, 0.05]), k(0.0, toon={'reach': {'R': R5(P21[0][2], 1, 0.06)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.55, 'mouth': 'line', 'gy': 0.8}, 'bend': {'spine': [0.3, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'hip': 0}, toonDur=0.0), *KW]),
        *[LIFE(act(w, p, 180 + 15 * (i - 1), 'stand', 'neutral', keys=[k(0.0, visible=False), k(CUT21, visible=True), k(0.0, look=[0, 1.6, -0.5]), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.0)]), D21, t0=r(CUT21 + 0.15 * i), amp=1.4) for i, (w, p) in enumerate(QUEUE)],
        LIFE(act('mec', HERO21, 75, 'stand', 'neutral', keys=[k(0.0, look=[0.0, CH, 0.1]), k(0.0, toon={'face': {'lid': 0.65, 'low': 0.3, 'mouth': 'wavy', 'brow': -0.4}}, toonDur=0.0),
            k(1.5, look='camera', lookDur=0.2), k(1.5, toon={'face': {'lid': 0.6, 'mouth': 'wavy', 'brow': -0.5}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.2)]), D21, t0=1.25, breath=False)],
        props=[P('guichet', 'styCounter', pos=CNT, opts={}), P('registre21', 'register', pos=[0.0, CH + 0.005, 0.02], rot=[-1.25, 0, 0], opts={'left': 'REGISTRE', 'right': 'MARIAGES', 'w': 0.5, 'h': 0.34}),
               P('stylo21', 'styPen', pos=P21[0][0], ry=P21[0][1][1], rot=[P21[0][1][0], 0, P21[0][1][2]], opts=PEN_RED,
                 keys=[*[k(r(0.05 + 0.11 * i), to=C_, dur=0.1, ease='inOut') for i, (C_, R_, G_) in enumerate(P21[1:], 1)], *[k(r(0.05 + 0.11 * i), rotTo=ROT(R_), dur=0.1) for i, (C_, R_, G_) in enumerate(P21[1:], 1)]]),
               PATCH('patch21', 'mec'), P('porte21', 'door', pos=[-1.55, 0, 3.75], ry=50, opts={'w': 1.0, 'h': 2.3})],
        tethers=[CHAINT('stylo21', anchor=ANCHOR)],
        cams=[C21a, C21b])
st.card('S21', 'ENCHAÎNÉ', at=r(st.at('S21', 'L15', 4) + 0.03))
st.cue('sfx:scratch', 'S21', 0.05, 0.25); st.cue('sfx:rattleShort', 'S21', 0.5, 0.2); st.cue('clang', 'S21', r(st.at('S21', 'L15', 4)), 0.25)

# ============================== the prison visiting booth (styBooth: the glass at z 0, he sits beyond it at -Z, the camera on the inmate side +Z)
BOOTH = {'color': '#C9D3CC'}
HERO22 = [0.0, 0.0, -0.5]
GUARD = [0.62, 0, 0.22]
# 22: this man has visiting on Thursdays. Frontal and still, then a slow push-in: in the foreground his red pen lies on a little stool on its chain
#     (ÉTAT tag), a guard standing beside it at attention; beyond the glass he sits holding the phone, JEUDI on the calendar behind him; he looks at
#     his pen, sighs, gives it a tiny wave, then looks at us; a slow blink finished well before the end
D22 = st.dur('S22')
C22F, C22T = [-0.05, 1.45, 3.2], [-0.05, 1.47, 2.85]
C22 = FC('S22', 0.0, C22F, {'heroTop': [HERO22[0], 1.95, HERO22[2]], 'cal': [-0.55, 2.3, -1.7], 'stool': [-0.4, 0.62, 0.7], 'pen': [-0.4, 0.68, 0.7], 'guardTop': [GUARD[0], 2.6, GUARD[2]], 'heroChest': [0, 1.2, -0.62], 'guardR': [GUARD[0] + 0.33, 1.4, GUARD[2]], 'tag': [-0.75, 0.55, 0.75]}, top=0.07, bottom=0.74, lenses=range(26, 76), drift=sub(C22T, C22F))
EAR = {'touch': {'L': ['face', 0.62, 0.02, -0.04, 1, 0.0]}, 'hands': {'L': 'grip'}}
F22 = {'lid': 0.55, 'mouth': 'line', 'brow': -0.2}
KEYS22 = [k(0.0, look=[-0.4, 0.7, 0.7]), k(0.0, toon={**EAR, 'face': {**F22, 'gy': 0.5}, 'hip': 0}, toonDur=0.0),
          k(0.5, toon={**EAR, 'face': {**F22, 'lid': 0.7, 'gy': 0.6, 'mouth': 'wavy'}, 'sq': [1.04, 0.96, 1.04], 'hip': 0}, toonDur=0.3, toonEase='inOut'),
          k(1.0, toon={**EAR, 'reach': {'R': R5([-0.15, 1.15, -0.3], 1, 0.05)}, 'hands': {'L': 'grip', 'R': 'open'}, 'face': {**F22, 'mouth': 'smile', 'gy': 0.6}, 'hip': 0}, toonDur=0.15),
          k(1.18, toon={**EAR, 'reach': {'R': R5([-0.08, 1.2, -0.3], 1, 0.05)}, 'hands': {'L': 'grip', 'R': 'open'}, 'face': {**F22, 'mouth': 'smile', 'gy': 0.6}, 'hip': 0}, toonDur=0.1),
          k(1.32, toon={**EAR, 'reach': {'R': R5([-0.15, 1.15, -0.3], 1, 0.05)}, 'hands': {'L': 'grip', 'R': 'open'}, 'face': {**F22, 'mouth': 'smile', 'gy': 0.6}, 'hip': 0}, toonDur=0.1),
          k(1.6, toon={**EAR, 'face': {**F22, 'gy': 0.0}, 'hip': 0}, toonDur=0.2), k(1.7, look='camera', lookDur=0.25),
          k(2.2, toon={**EAR, 'face': {**F22, 'lid': 1.0}, 'hip': 0}, toonDur=0.12), k(2.38, toon={**EAR, 'face': {**F22, 'lid': 0.55}, 'hip': 0}, toonDur=0.12)]
st.shot('S22', 'whiteVoid', setOpts=BOOTH, actors=[act('mec', HERO22, 0, 'sit', 'neutral', keys=KEYS22),
        LIFE(act('gardien', GUARD, -25, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0), k(1.2, look=[-0.4, 0.7, 0.7], lookDur=0.2), k(1.75, look='camera', lookDur=0.2)]), D22, t0=0.6, breath=True)],
        props=[P('parloir', 'styBooth', pos=[0, 0, 0], opts={'stool': [-0.4, 0.7], 'calX': -0.55}), P('chaise22', 'chair', pos=[0, 0, -0.68], opts={'color': '#5A6068'}),
               P('tel22', 'handset', on={'actor': 'mec', 'joint': 'head', 'offset': [0.2, 0.2, 0.03]}, opts={'len': 0.32, 'rot': [-0.35, r(-PI / 2), 0.0], 'color': '#2A2D33'})],
        cams=[C22])
st.cue('sfx:sad', 'S22', 0.5, 0.2); st.cue('sfx:tick', 'S22', 1.0, 0.1); st.cue('sfx:tick', 'S22', 1.18, 0.1)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
BIG = {'width': 1.0, 'headWidth': 1.2}
CUSTOMS = lambda seed: {'preset': 'cop', 'seed': seed, 'suit': '#3F5B4E', 'pants': '#2F453B', 'lapel': '#2F453B', 'tie': '#2F453B', 'shirt': '#DCE3DA', 'cuff': '#3F5B4E', 'hatColor': '#2F453B', 'hatBand': '#C9A24B', 'gloves': '#2E6FD8', 'build': BIG, 'toon': EX}
st.write("Le stylo", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecPyj': {'preset': 'mecPyjama', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}},
    'greffiere': {'preset': 'femme', 'seed': 921, 'suit': '#7A5A8A', 'lapel': '#F2EDE4', 'glasses': True, 'hair': 'bun', 'hairColor': '#4A3020', 'build': {'width': 0.92, 'headWidth': 1.22}, 'toon': EX},
    'commis': {'preset': 'boss', 'seed': 922, 'glasses': True, 'build': BIG, 'toon': EX},
    'maire': {'preset': 'politique', 'seed': 923, 'sash': ['#1F8A7A', '#E8C330', '#1F8A7A'], 'sashW': 0.14, 'hairColor': '#BDBDBD', 'suit': '#4A4F5A', 'lapel': '#4A4F5A', 'tie': '#7A2333', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'mariee': {'preset': 'femme', 'seed': 924, 'suit': '#F7F4EE', 'lapel': '#F7F4EE', 'hair': 'bun', 'hairColor': '#5A3A22', 'build': {'width': 0.88, 'headWidth': 1.22}, 'toon': EX},
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
    'enfant1': {'preset': 'gamin', 'seed': 936, 'toon': EX}, 'enfant2': {'preset': 'gamin', 'seed': 937, 'suit': '#E8463C', 'toon': EX}, 'enfant3': {'preset': 'gamin', 'seed': 938, 'suit': '#F2B630', 'toon': EX},
    'mere': {'preset': 'mamie', 'seed': 939, 'build': {'height': 0.86, 'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'flic': {'preset': 'cop', 'seed': 940, 'build': BIG, 'toon': EX},
    **{f'commando{i}': {'preset': 'swat', 'hat': 'none', 'hair': 'bald', 'seed': 940 + i, 'gloves': '#22252B', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for i in (1, 2, 3, 4)},
    'technicienne': {'preset': 'doctor', 'seed': 945, 'hair': 'bun', 'hairColor': '#3A2A20', 'glasses': True, 'lipstick': True, 'build': {'width': 0.92, 'headWidth': 1.22}, 'toon': EX},
    'client1': {'preset': 'madame', 'seed': 946, 'build': BIG, 'toon': EX}, 'client2': {'preset': 'worker', 'seed': 947, 'hat': 'none', 'build': BIG, 'toon': EX}, 'client3': {'preset': 'tourist', 'seed': 948, 'build': BIG, 'toon': EX},
    'gardien': {'preset': 'cop2', 'seed': 949, 'suit': '#3A3F48', 'pants': '#2A2E36', 'lapel': '#2A2E36', 'hatColor': '#2A2E36', 'build': {'width': 1.1, 'headWidth': 1.2, 'belly': 0.06}, 'toon': EX},
})
