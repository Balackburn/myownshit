#!/usr/bin/env python3
"""DOCSTRING"""
from story_kit import *
import math

st = Story('sel', look='natural')
st.plan([('S01', 'L01', 0), ('S01b', 'L01', 4), ('S01c', 'L01', 10), ('S02', 'L02', 2), ('S03', 'L03', 0), ('S03b', 'L03', 4), ('S03c', 'L03', 7),
         ('S04', 'L04', 0), ('S04b', 'L04', 1), ('S05', 'L05', 0), ('S05b', 'L05', 3), ('S06', 'L06', 0), ('S06b', 'L06', 6), ('S07', 'L07', 0), ('S07b', 'L07', 4),
         ('S08', 'L08', 0), ('S08b', 'L08', 4), ('S09', 'L09', 0), ('S09b', 'L09', 7), ('S10', 'L10', 0), ('S10b', 'L10', 6), ('S10c', 'L10', 9),
         ('S11', 'L11', 0), ('S11b', 'L11', 4), ('S12', 'L12', 0), ('S12b', 'L12', 6), ('S13', 'L13', 0), ('S14', 38.3, 0), ('S15', 'L15', 1), ('S15b', 'L15', 7),
         ('S16', 'L16', 0), ('S16b', 'L16', 5)])
# every cut just under its frame: st.cut rounds to 4 decimals (53/30 -> 1.7667, after the frame: its first image would show the shot before); take the
# frame index and floor its time instead (1.7666: frame 53 belongs to the new shot)
FL = lambda v: math.floor(round(v * 30) / 30 * 10000) / 10000
st.SH = {sid: (FL(a), FL(b) if b < st.total else b) for sid, (a, b) in st.SH.items()}

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
    # word timings from timeline.json: st.at counts the words from 0; the word is printed beside its time
    t = st.at(sid, lid, i); CHECKS.append(f"{sid} « {st.L[lid]['words'][i]['w']} » at {t}"); return t
EZ = {'linear': lambda u: u, 'inOut': lambda u: 2 * u * u if u < 0.5 else 1 - (-2 * u + 2) ** 2 / 2, 'out': lambda u: 1 - (1 - u) ** 3, 'in': lambda u: u ** 3}
def track(p0, moves):
    # where a prop moved by `to` keys is at t (each move starts where the last one ended; eases as the engine's): hands follow it exactly
    def at_(t):
        p = list(p0)
        for t0, to, d, e in sorted(moves, key=lambda m: m[0]):
            if t < t0: break
            u = EZ[e](1.0 if d <= 0 else min(1.0, (t - t0) / d)); p = [p[i] + (to[i] - p[i]) * u for i in range(3)]
        return [r(v) for v in p]
    return at_
def MOVES(moves): return [k(t0, to=list(to), dur=d, ease=e) for t0, to, d, e in moves]
def FALL(t0, p0, p1, dur, n=4):
    # a drop by gravity: linear `to` keys at the u^2 positions
    return [(r(t0 + dur * (i - 1) / n), lerp3(p0, p1, (i / n) ** 2), r(dur / n), 'linear') for i in range(1, n + 1)]
def R5(p, w=1, s=0.0): return [*p, w, s]
def FIT(frm, pts, back=False, **kw):
    # the aim and the lens that hold every point (heads with a margin of 0.12 of the width, above the captions): fit() / fitBack() of the kit
    kw.setdefault('margin', 0.12); kw.setdefault('top', 0.12); kw.setdefault('bottom', 0.78); kw.setdefault('lenses', range(30, 57))
    if back: f, look, lens = fitBack(frm, pts, **kw)
    else: f = frm; look, lens, _ = fit(frm, pts, **kw)
    assert lens, f'no lens fits from {frm}'
    return [r(v) for v in f], [r(v) for v in look], lens
def HAND(R=None, L=None, hr='grip', hl='grip', tipR=0.0, tipL=0.0, **x):
    return {'reach': {**({'R': R5(R, 1, tipR)} if R else {}), **({'L': R5(L, 1, tipL)} if L else {})}, 'hands': {'R': hr, 'L': hl}, 'hip': 0, **x}
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
def TALK(t0, t1, face, keep=None, step=0.1, nod=0.05, tilt=0.0):
    # lip flaps (open / o / line shapes, small nods); keep: the hands (a toon key is a whole state)
    out, t_, i = [], t0, 0
    while t_ < t1 - 0.04:
        m = ['open', 'o', 'line', 'open', 'smirk'][i % 5]
        bd = {**(keep or {}).get('bend', {}), 'neck': [r(nod if i % 3 == 0 else -nod * 0.5), tilt, 0, 1, None]}
        out.append(k(r(t_), toon={**(keep or {}), 'bend': bd, 'face': {**face, 'mouth': m, 'jaw': 0.25 if m in ('open', 'o') else 0.0}}, toonDur=r(step * 0.7)))
        t_ += step; i += 1
    return out
def NOSHADOW(pid, who): return P(pid, 'poNoShadow', pos=[0, 0, 0], opts={'who': who})

# ============================== the shaker, the heaps, the cutlery
SH_H = 0.36; SH_GRIP = 0.13                  # the shaker (seShaker): its height, and where a mitten holds it above its base
FULL, Q3, HALF, EMPTY = 1.0, 0.75, 0.5, 0.0  # the running gag's four states (S01c a notch under full, S07b three quarters, S10c half, S14 empty)
def SHAKER(pid, pos, fill, keys=None, ry=0.0, rot=None, **o):
    return P(pid, 'seShaker', pos=list(pos), ry=ry, **({'rot': rot} if rot else {}), opts={'fill': fill, 'h': SH_H, **o}, **({'keys': keys} if keys else {}))
def HEAP(pid, pos, grow=None, r_=0.05): return P(pid, 'seHeap', pos=list(pos), opts={'r': r_, **({'grow': grow} if grow is not None else {})})
def GRAINS(pid, pos, on, ln=0.22): return P(pid, 'seGrains', pos=list(pos), opts={'on': on, 'len': ln})
KN_L = 0.46; KN_G = 0.0875                    # the cartoon knife and fork (seUtensil): their length, where the fist holds them
def UTENSIL(pid, kind, base, ry, keys=None, snow=None, rot=None):
    return P(pid, 'seUtensil', pos=list(base), ry=ry, **({'rot': rot} if rot else {}), opts={'kind': kind, 'len': KN_L, **({'snow': snow} if snow is not None else {})}, **({'keys': keys} if keys else {}))
def ubase(hand): return [hand[0], r(hand[1] - KN_G), hand[2]]   # the base of an upright utensil whose grip is in the fist at `hand`

# ============================== the hero: seated at his end of the table, knife and fork bolt upright in his two mittens (the waiting pose, S01 to S16)
HF = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}
def hero_hands(H, ry, f=0.42, s=0.19, y=0.93): return off(H, ry, f, s, y), off(H, ry, f, -s, y)   # (right: knife, left: fork) for a hero at H facing ry
def KF(H, ry, **x):
    # the waiting pose: both fists in front, knife (right) and fork (left) straight up
    R_, L_ = hero_hands(H, ry); return HAND(R_, L_, 'fist', 'fist', **x)
SIT = lambda: k(0.0, clip='sit')

# ============================== the family dining room (seDining on whiteVoid; the table runs along X at z 0, mamie at the -X end, he at the +X end)
DSET = {'color': '#E6DCC8'}
TH = 0.76                                     # table height
TW = 1.0                                      # table width
MAIN_C, MAIN_L = -0.5, 4.2                    # the first segment: x -2.6 .. 1.6
LEAF = 1.0                                    # each leaf
END_L = 1.0
HX0 = 3.0                                     # the hero's x before any leaf (his chair at x + 0.05, his end segment centred at x - 0.9)
MAMIE = [-3.0, 0.0, 0.0]; RYM = 90
SEAT = {'cA': [-2.2, 0.0, -0.75], 'cB': [-1.0, 0.0, 0.75], 'cD': [0.4, 0.0, -0.75], 'cC': [1.45, 0.0, -0.75]}
RYS = {n: (0 if p[2] < 0 else 180) for n, p in SEAT.items()}
PLACES_MAIN = [[-2.2 - MAIN_C, -1], [-1.0 - MAIN_C, 1], [0.4 - MAIN_C, -1], [1.3 - MAIN_C, -1], [-1.75 - MAIN_C, 1], [-0.2 - MAIN_C, 1], [0.9 - MAIN_C, 1], [-1.0 - MAIN_C, -1]]
CHAIRS_MAIN = [[-2.2 - MAIN_C, -1], [-1.0 - MAIN_C, 1], [0.4 - MAIN_C, -1], [1.45 - MAIN_C, -1], [-1.75 - MAIN_C, 1], [-0.2 - MAIN_C, 1], [0.9 - MAIN_C, 1], [-1.0 - MAIN_C, -1]]
def plate_at(sx, sd): return [r(sx), TH + 0.02, r(sd * (TW / 2 - 0.2))]   # the middle of a place's plate (world), its well
def DINING(n, **o): return P(f'salle{n}', 'seDining', pos=[0, 0, 0], opts=o)
def MAINSEG(n, **o): return P(f'table{n}', 'seTable', pos=[MAIN_C, 0, 0], opts={'len': MAIN_L, 'w': TW, 'places': PLACES_MAIN, 'chairs': CHAIRS_MAIN, **o})
def LEAFSEG(n, cx, keys=None, **o): return P(f'rallonge{n}', 'seLeaf', pos=[r(cx), TH - 0.03, 0], opts={'len': LEAF, 'w': TW, **o}, **({'keys': keys} if keys else {}))
def ENDSEG(n, hx, keys=None): return P(f'bout{n}', 'seTable', pos=[r(hx - 0.9), 0, 0], opts={'len': END_L, 'w': TW, 'inset': 0.12}, **({'keys': keys} if keys else {}))
def ROAST(n, hx, keys=None, snow=None, y=TH): return P(f'roti{n}', 'seRoast', pos=[r(hx - 0.72), y, 0.0], ry=-90, opts={'s': 1.0, **({'snow': snow} if snow is not None else {})}, **({'keys': keys} if keys else {}))
def HCHAIR(n, hx, keys=None): return P(f'chaiseMec{n}', 'seChair', pos=[r(hx + 0.05), 0, 0], ry=-90, opts={'color': '#6A4430', 'cushion': '#B8544A'}, **({'keys': keys} if keys else {}))
def MCHAIR(n): return P(f'chaiseMamie{n}', 'seChair', pos=[-3.05, 0, 0], ry=90, opts={'color': '#6A4430', 'cushion': '#8E5AA8'})
def hx_after(nleaves): return HX0 + LEAF * nleaves
def LEAVES(n, upto, extra=()):
    # the leaves already slotted in before this shot (leaf i is centred at 2.1 + i)
    return [LEAFSEG(f'{n}_{i}', 2.1 + i) for i in range(upto)] + list(extra)
def HERO_END(n, nleaves, keys_end=None, snow=None):
    # his end segment, his roast and his chair, where they are after `nleaves` leaves (keys_end: the same keys move all three)
    hx = hx_after(nleaves); return [ENDSEG(n, hx, keys_end), ROAST(n, hx, keys_end, snow), HCHAIR(n, hx, keys_end)]

GAGS = []
def GAG(*a): GAGS.append(a)

# 1: « Au repas de famille, » At his end of the table, low and three-quarter: he sits bolt upright, knife and fork straight up in his mittens, the big roast
#    untouched before him; an eager hop in his chair (a squash, a stretch, the cutlery lifted, a squash on landing), a lick of the lips, his eyes on the
#    roast then on us; the cousin beside him tucks his napkin in and sniffs the roast; the doorway to the hall behind him
D1 = st.dur('S01'); HX = hx_after(0); H1 = [HX, 0.0, 0.0]; RYH = -90
KR1, KL1 = hero_hands(H1, RYH)
F1, L1, LN1 = FIT([r(HX - 4.3), 1.38, -0.02], {'heroTop': add(H1, [0, 1.95, 0]), 'heroChin': add(H1, [0, 1.3, 0]), 'knifeTip': add(KR1, [0, 0.4, 0]), 'roast': [r(HX - 0.72), TH, 0.2],
                                            'cCtop': add(SEAT['cC'], [0, 1.95, 0]), 'cCknee': add(SEAT['cC'], [0, 0.75, 0.3])}, margin=0.14, top=0.13, bottom=0.76)
C1 = cam(0.0, F1, add(F1, [0.1, 0.0, -0.1]), L1, L1, lens=LN1, ease='inOut')
chkc('S01', C1, {'heroTop': add(H1, [0, 1.92, 0]), 'heroChin': add(H1, [0, 1.33, 0]), 'knifeTip': add(KR1, [0, 0.38, 0]), 'roast': [r(HX - 0.72), TH + 0.2, 0], 'cCtop': add(SEAT['cC'], [0, 1.95, 0]), 'cCchin': add(SEAT['cC'], [0, 1.4, 0]), 'door': [6.8, 2.6, 0]})
HOP1 = 0.06
def kfup(H, ry, dy=0.0):
    R_, L_ = hero_hands(H, ry); return HAND(add(R_, [0, dy, 0]), add(L_, [0, dy, 0]), 'fist', 'fist')
HK1 = [SIT(), k(-0.5, look=[r(HX - 0.72), TH + 0.15, 0]), k(0.0, toon={**KF(H1, RYH), 'face': HF}, toonDur=0.0),
       k(HOP1, toon={**kfup(H1, RYH, -0.02), 'sq': [1.08, 0.9, 1.08], 'face': {**HF, 'lid': 0.5}}, toonDur=0.04),
       k(r(HOP1 + 0.08), toon={**kfup(H1, RYH, 0.07), 'sq': [0.92, 1.12, 0.92], 'hairUp': 0.5, 'face': {**HF, 'lid': 0.0, 'brow': 0.9, 'eye': 0.25}}, toonDur=0.05, toonEase='outBack'),
       k(r(HOP1 + 0.22), toon={**kfup(H1, RYH, -0.01), 'sq': [1.07, 0.94, 1.07], 'face': {**HF, 'brow': 0.6}}, toonDur=0.04, toonEase='in'),
       k(r(HOP1 + 0.34), toon={**KF(H1, RYH), 'sq': [0.98, 1.02, 0.98], 'face': {**HF, 'mouth': 'tongueout', 'brow': 0.5}}, toonDur=0.08),
       k(r(HOP1 + 0.52), toon={**KF(H1, RYH), 'face': {**HF, 'brow': 0.5}}, toonDur=0.08),
       k(0.72, look='camera', lookDur=0.15), *life(0.75, D1, {**HF, 'brow': 0.4}, KF(H1, RYH), blinks=[0.92], period=0.5)]
UM1 = [(HOP1, ubase(add(KR1, [0, -0.02, 0])), 0.04, 'out'), (r(HOP1 + 0.08), ubase(add(KR1, [0, 0.07, 0])), 0.05, 'out'), (r(HOP1 + 0.22), ubase(add(KR1, [0, -0.01, 0])), 0.04, 'in'), (r(HOP1 + 0.34), ubase(KR1), 0.08, 'inOut')]
FM1 = [(t0, ubase(add(KL1, [0, dy, 0])), d, e) for (t0, _, d, e), dy in zip(UM1, [-0.02, 0.07, -0.01, 0.0])]
CCF = {'lid': 0.4, 'mouth': 'smile', 'brow': 0.2}
CC1 = SEAT['cC']; RYC1 = -50
CK1 = [SIT(), k(-0.5, look=lerp3([r(HX - 0.72), 1.6, 0], F1, 0.5)), k(0.0, toon={**HAND(off(CC1, RYC1, 0.3, 0.12, 1.55), off(CC1, RYC1, 0.3, -0.12, 1.55), 'pinch', 'pinch'), 'face': CCF}, toonDur=0.0),
       k(0.1, toon={**HAND(off(CC1, RYC1, 0.32, 0.1, 1.48), off(CC1, RYC1, 0.32, -0.1, 1.48), 'pinch', 'pinch'), 'sq': [0.97, 1.03, 0.97], 'face': {**CCF, 'brow': 0.6}}, toonDur=0.12),
       k(0.32, toon={**HAND(off(CC1, RYC1, 0.35, 0.22, 0.86), off(CC1, RYC1, 0.35, -0.22, 0.86), 'open', 'open'), 'bend': {'spine': [0.08, 0, 0, 1, None], 'neck': [0.05, 0, 0.25, 1, None]}, 'face': {**CCF, 'lid': 0.9, 'mouth': 'o', 'gx': 0.8}}, toonDur=0.18),
       k(0.55, toon={**HAND(off(CC1, RYC1, 0.35, 0.22, 0.86), off(CC1, RYC1, 0.35, -0.22, 0.86), 'open', 'open'), 'sq': [0.96, 1.05, 0.96], 'bend': {'spine': [0.1, 0, 0, 1, None], 'neck': [0.05, 0, 0.3, 1, None]}, 'face': {**CCF, 'lid': 1.0, 'mouth': 'smile', 'brow': 0.8, 'gx': 0.8}}, toonDur=0.1),
       *life(0.75, D1, {**CCF, 'gx': 0.6}, HAND(off(CC1, RYC1, 0.35, 0.22, 0.86), off(CC1, RYC1, 0.35, -0.22, 0.86), 'open', 'open'), blinks=[1.0], period=0.6)]
st.shot('S01', 'whiteVoid', setOpts=DSET, actors=[act('mec', H1, RYH, 'sit', 'neutral', keys=HK1), act('cC', CC1, RYC1, 'sit', 'neutral', keys=CK1)],
        props=[DINING(1), MAINSEG(1), *HERO_END(1, 0), UTENSIL('couteau1', 'knife', ubase(KR1), yaw(KR1, F1), keys=MOVES(UM1)), UTENSIL('fourchette1', 'fork', ubase(KL1), yaw(KL1, F1), keys=MOVES(FM1)),
               SHAKER('sel1', [-2.45, TH, 0.1], FULL), NOSHADOW('ns1', ['mec', 'cC'])],
        cams=[C1])
GAG('S01', 0.3, 'mec', 'eager hop')
st.cue('sfx:boing', 'S01', r(HOP1 + 0.08), 0.12); st.cue('clack', 'S01', r(HOP1 + 0.22), 0.15); st.cue('sfx:sniff', 'S01', 0.55, 0.15)

print('\n'.join(CHECKS))
TOON = {'breathe': 1.7, 'holdLife': 1.6}
EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': TOON}
for g_ in GAGS: st.gag(*g_)
st.scenes.sort(key=lambda s_: s_['start'])
st.write("Le sel", rig='toon', fingers=False, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    # mamie: a white bun, a lilac apron, big round glasses, small
    'mamie': {'preset': 'mamie', 'seed': 10901, 'suit': '#B48CD2', 'lapel': '#F4EEE2', 'hair': 'bun', 'hairColor': '#F2F2EE', 'glasses': True, 'build': {'height': 0.88, 'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    # the cousins: each his own model, colours and hair (none in navy, none with the hero's stubble and red tie)
    'cA': {'preset': 'boss', 'seed': 10902, 'suit': '#7A8E5A', 'lapel': '#6A7E4A', 'tie': '#E8C25A', 'hair': 'curly', 'hairColor': '#B0582A', 'facial': 'mustache', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'cB': {'preset': 'femme', 'seed': 10903, 'suit': '#D8708A', 'lapel': '#F2E6E8', 'hair': 'long', 'hairColor': '#2A1E18', 'glasses': False, 'toon': EX},
    'cC': {'preset': 'commissaire', 'seed': 10904, 'hat': 'none', 'suit': '#A8875E', 'lapel': '#8E7048', 'tie': '#3E6A9A', 'hair': 'receding', 'hairColor': '#4A3A2A', 'facial': 'mustache', 'glasses': True, 'toon': EX},
    'cD': {'preset': 'madame', 'seed': 10905, 'suit': '#E8A040', 'lapel': '#F4EEE2', 'hair': 'bun', 'hairColor': '#6A3A20', 'toon': EX},
    'cE': {'preset': 'sportif', 'seed': 10906, 'suit': '#4AA89A', 'hair': 'spiky', 'hairColor': '#D8B060', 'toon': EX},
})
