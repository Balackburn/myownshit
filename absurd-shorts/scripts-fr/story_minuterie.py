#!/usr/bin/env python3
"""DOCSTRING"""
from story_kit import *
import math

st = Story('minuterie', look='natural')
st.plan([('S01', 'L01', 0), ('S01b', 'L01', 5), ('S02', 'L02', 0), ('S02b', 'L02', 6), ('S03', 'L03', 0), ('S03b', 'L03', 2), ('S04', 'L04', 0), ('S04b', 'L04', 7),
         ('S05', 'L05', 0), ('S05b', 'L05', 4), ('S06', 'L06', 0), ('S06b', 'L06', 6), ('S07', 'L07', 0), ('S07b', 'L07', 3), ('S07c', 'L07', 10),
         ('S08', 'L08', 0), ('S08b', 'L08', 5), ('S09', 'L09', 0), ('S09b', 'L09', 3), ('S10', 'L10', 0), ('S10b', 'L10', 4), ('S11', 'L11', 0), ('S11b', 'L11', 5),
         ('S12', 'L12', 0), ('S12b', 'L12', 3), ('S13', 'L13', 0), ('S13b', 'L13', 5), ('S14', 'L14', 0), ('S14b', 'L14', 7), ('S15', 'L15', 0), ('S15b', 'L15', 4),
         ('S16', 'L16', 0), ('S16b', 43.0, 0)])
# every cut just under its frame: st.cut rounds to 4 decimals (53/30 -> 1.7667, after the frame: its first image would show the shot before); take the
# frame index and floor its time instead
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
def chk(sid, frm, look, lens, pts, heads=(), card=False):
    pr = {n: project(frm, look, lens, p) for n, p in pts.items()}
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {v}" for n, v in pr.items()))
    for n in heads:
        v = pr.get(n)
        if not v or not (0.0 <= v[0] <= 1.0 and 0.0 <= v[1] <= 1.0): CHECKS.append(f"  BANDS {sid}: {n} out of the frame {v}")
        elif 0.765 <= v[1] <= 0.835: CHECKS.append(f"  BANDS {sid}: {n} in the caption band {v}")
        elif card and 0.07 <= v[1] <= 0.18: CHECKS.append(f"  BANDS {sid}: {n} in the card band {v}")
def chkc(sid, c, pts, heads=(), end=False, card=False):
    frm, look = (c.get('to') or c['from'], c.get('lookAt2') or c['lookAt']) if end else (c['from'], c['lookAt'])
    chk(sid + ('>' if end else ''), frm, look, c['lens'], pts, heads, card)
def chk2(sid, c, pts, heads=(), card=False): chkc(sid, c, pts, heads, card=card); chkc(sid, c, pts, heads, end=True, card=card)
def W(sid, lid, i):
    # word timings from timeline.json: st.at counts the words from 0; the word is printed beside its time
    t = st.at(sid, lid, i); CHECKS.append(f"{sid} « {st.L[lid]['words'][i]['w']} » at {t}"); return t
def R5(p, w=1, s=0.0): return [*p, w, s]
def FIT(frm, pts, back=False, **kw):
    # the aim and the lens that hold every point (heads with a margin of the width, above the captions): fit() / fitBack() of the kit
    kw.setdefault('margin', 0.14); kw.setdefault('top', 0.1); kw.setdefault('bottom', 0.75); kw.setdefault('lenses', range(28, 60))
    if back: f, look, lens = fitBack(frm, pts, **kw)
    else:
        f = frm; look, lens, _ = fit(frm, pts, **{k_: v for k_, v in kw.items() if k_ not in ('inside', 'level')})
        if not lens: f, look, lens = fitBack(frm, pts, **kw)
    assert lens, f'no lens fits from {frm}'
    return [r(v) for v in f], [r(v) for v in look], lens
def HAND(R=None, L=None, hr='rest', hl='rest', tipR=0.0, tipL=0.0, **x):
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

# ============================== the stairwell (engine/props_minuterie.js, mnStairwell: its numbers are in the prop's header)
FH = 2.8; BH = 1.8; G = 0.02; DOORX = 2.9
def LAND(k_, x=2.2, z=0.0): return [x, r(FH * k_ + (G if k_ == 0 else 0.0)), z]
def STA(k_, i, z=0.97): return [r(1.225 - 0.35 * i), r(FH * k_ + 0.175 * (i + 1)), z]
def STB(k_, i, z=-0.97): return [r(-1.225 + 0.35 * i), r(FH * k_ + 1.4 + 0.175 * (i + 1)), z]
def HALF(k_, x=-2.1, z=0.0): return [x, r(FH * k_ + 1.4), z]
def BTN(k_): return [1.26, r(FH * k_ + BH), 0.2]
BIG = [5.05, 1.35, -1.45]
LOCK7 = [2.54, r(FH * 7 + 1.05), -1.4]
SET = 'whiteVoid'; SETO = {'color': '#E7E1D3'}
DARK = {'darkFloor': 0.42, 'darkTint': '#5F86E0', 'darkEyes': 2.4}
LOOK_IN = {'exposure': 1.0}
def WELL(n, **o): return P(f'cage{n}', 'mnStairwell', pos=[0, 0, 0], opts=o)
def BTNS(n, **o): return P(f'boutons{n}', 'mnButtons', pos=[0, 0, 0], opts=o, inDark=True)
def LINES(n, on=None, off_=None, **o):
    # the pale lines of the dark (inDark): shown from `on` (s) until `off_`
    ks = [k(0.0, visible=on is not None and on <= 0.0)]
    if on is not None and on > 0: ks.append(k(on, visible=True))
    if off_ is not None: ks.append(k(off_, visible=False))
    return P(f'traits{n}', 'mnDarkLines', pos=[0, 0, 0], opts=o, inDark=True, keys=ks)
def BRIEF(n, who='mec'): return P(f'mallette{n}', 'briefcase', on={'actor': who, 'hand': 'L', 'hang': True})
def NOSHADOW(pid, who): return P(pid, 'poNoShadow', pos=[0, 0, 0], opts={'who': who})

# the neighbour's trolley: it trails behind her, its -Z side to her, tipped back by TT (rad); handle(p, ry) is where its handle is
TT = -0.32
def handle(p, ry, tilt=TT):
    # the handle sits 0.98 up and 0.08 behind the axle in the trolley's frame; the trolley faces away from her (ry + 180)
    y = 0.98 * math.cos(tilt) + 0.08 * math.sin(tilt); zl = 0.98 * math.sin(tilt) - 0.08 * math.cos(tilt)
    F = fwd(ry + 180); return [r(p[0] + F[0] * zl), r(p[1] + y), r(p[2] + F[2] * zl)]
def TROLLEY(n, p, ry, keys=None, bump=None, tilt=TT):
    return P(f'caddie{n}', 'mnTrolley', pos=list(p), ry=r(ry + 180, 1), rot=[tilt, 0, 0], rotOrder='YXZ', opts={**({'bump': bump} if bump else {})}, **({'keys': keys} if keys else {}))
VF = {'lid': 0.45, 'mouth': 'line', 'brow': 0.0}

GAGS = []
def GAG(*a): GAGS.append(a)

# ============================== the hero: a briefcase in his left mitten; HF his face
HF = {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}
HFD = {'lid': 0.0, 'mouth': 'line', 'brow': -0.5, 'eye': 0.2}         # determined
def SPLAT_FACE(**x): return {**HF, 'lid': 0.0, 'eye': 0.4, 'brow': 0.9, **x}

# 1: « Ce mec habite au septième. » The hall at night, deep blue: only his eyes and the big orange button by the front door glow; he winds his right arm
#    up high and slaps the button without looking (a squash, his hair jolts): the light comes on at the slap; he turns to us, a determined frown, crouches
#    and shoots off toward the stairs (a dashed hole of speed where he stood)
D1 = st.dur('S01'); SLAP1 = 0.3; GO1 = 0.74
H1 = [5.62, G, -1.0]; RY1 = -55
WIND1 = off(H1, RY1, 0.1, 0.4, 2.45); HIT1 = add(BIG, [0.0, 0.0, 0.08])
F1, L1, LN1 = FIT([3.75, 0.9, 2.95], {'head': add(H1, [0, 2.4, 0]), 'feet': add(H1, [0, 0.05, 0.2]), 'btn': BIG, 'wind': WIND1, 'door': [6.1, 2.2, -1.5]}, margin=0.16, top=0.12, bottom=0.74)
C1 = cam(0.0, F1, add(F1, [0.12, 0.05, -0.15]), L1, L1, lens=LN1, ease='inOut')
chk2('S01', C1, {'head': add(H1, [0, 2.35, 0]), 'feet': H1, 'btn': BIG, 'wind': WIND1}, heads=('head',))
HK1 = [k(-0.5, look='camera'), k(0.0, toon={**HAND(WIND1, None, 'open'), 'sq': [0.95, 1.06, 0.95], 'face': {**HF, 'brow': 0.4}}, toonDur=0.0),
       k(r(SLAP1 - 0.07), toon={**HAND(add(HIT1, [0.05, 0.12, 0.05]), None, 'open', hose=0.1), 'sq': [1.03, 0.98, 1.03], 'face': {**HF, 'lid': 0.1}}, toonDur=0.06, toonEase='in'),
       k(SLAP1, toon={**HAND(HIT1, None, 'open', tipR=0.1), 'sq': [1.14, 0.86, 1.14], 'hairUp': 0.9, 'face': SPLAT_FACE(mouth='o')}, toonDur=0.03),
       k(r(SLAP1 + 0.1), toon={**HAND(HIT1, None, 'open', tipR=0.1), 'sq': [0.95, 1.06, 0.95], 'hairUp': 0.4, 'face': {**HF, 'brow': 0.6}}, toonDur=0.07),
       k(r(SLAP1 + 0.22), toon={'sq': [1.0, 1.0, 1.0], 'hip': 0, 'face': HFD}, toonDur=0.1),
       k(r(GO1 - 0.14), toon={'sq': [1.16, 0.82, 1.16], 'hip': 0, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': HFD, 'auto': 0}, toonDur=0.08),
       k(r(GO1 - 0.14), face=-68, turn=0.08),
       k(GO1, to=[1.2, G, 0.75], dur=0.34, ease='linear', clip='run', face=-68),
       k(GO1, toon={'sq': [0.86, 1.2, 0.86], 'hip': 0, 'bend': {'spine': [0.4, 0, 0, 1, None]}, 'face': HFD, 'smear': 0.7}, toonDur=0.05)]
st.shot('S01', SET, setOpts=SETO, look=LOOK_IN, dark=[[0, 1, 0.0], [SLAP1, 0, 0.0]], **DARK,
        actors=[act('mec', H1, RY1, 'stand', 'neutral', keys=HK1)],
        props=[WELL('1', lit=[[0, 0], [SLAP1, 1]], top=2), BTNS('1', press=[[0, SLAP1]], floors=[0, 1, 2]), LINES('1', on=0.0, off_=SLAP1, top=2), BRIEF('1'),
               P('trou1', 'mnGhost', pos=H1, ry=RY1 + 55, opts={'at': r(GO1 + 0.06), 'dir': -1, 'dur': 0.6})],
        cams=[C1])
GAG('S01', SLAP1, 'mec', 'slaps the front-door button'); GAG('S01', r(GO1 - 0.1), 'mec', 'crouch, determined')
st.cue('clack', 'S01', SLAP1, 0.5); st.cue('sfx:click', 'S01', r(SLAP1 + 0.02), 0.3); st.cue('whoosh', 'S01', GO1, 0.25, 0.35, 500, 2600)

# 1b: « La minuterie dure trente secondes. » Up the stairwell from the foot of the well: the flights and landings stacked like a telescope, the top one
#     tiny; the camera rises and turns slowly; low in a corner, the first landing's orange button glows (the running gag starts, never said); his
#     footsteps race up
D1b = st.dur('S01b')
# (the camera has no roll, so the zenith, where the landings converge, stays on the frame's middle line: the column of buttons runs from the first
# landing's, low on the right, up toward it, small glows on a pale column, off the middle; S16 centres them and makes them big)
F1b = [-0.9, 1.15, 0.38]; L1b = [2.37, 10.49, -1.08]
C1b = cam(0.0, F1b, add(F1b, [0.0, 0.4, 0.0]), L1b, add(L1b, [0.0, 0.4, 0.25]), lens=56, ease='inOut')
chk2('S01b', C1b, {'btn0': BTN(0), 'btn1': BTN(1), 'btn2': BTN(2), 'btn3': BTN(3), 'top': [0, 22.0, 0]})
st.shot('S01b', SET, setOpts=SETO, look=LOOK_IN, actors=[],
        props=[WELL('1b', front=True), BTNS('1b', glow=0.55, size=0.85)], cams=[C1b])
GAG('S01b', 0.5, 'mec', 'the telescope of landings')
for i_ in range(6): st.cue('sfx:stepRun', 'S01b', r(0.08 + 0.16 * i_), 0.18)
st.cue('sfx:ticks', 'S01b', 0.55, 0.12)

# ============================== the neighbour du troisième (tiny, grey bun, purple coat, tartan trolley): she presses the button of every landing with one
# finger, deadpan, always in her own light; on a landing she stands by the newel column, the trolley behind her
VNOD = {**VF, 'lid': 0.5}
# walking with the trolley: her left mitten held behind her in her own frame (a world point would stay behind as she walks); the trolley follows by keys
VTT = {'touch': {'L': ['torso', 0.24, 0.12, -0.36, 1, 0.0]}, 'hands': {'L': 'grip', 'R': 'rest'}, 'hip': 0}
def VSTAND(p, ry, trolley_at=None, press=None, t_press=None, other=None):
    # her pose by the column: the left mitten on the trolley's handle, the right one at rest (or pressing BTN(press) at t_press)
    tp = trolley_at or off(p, ry, -0.5, -0.32)
    hd = handle(tp, yaw(tp, p))
    return tp, hd
def PRESS_KEYS(p, ry, k_, t0, hd, face=VF, dur=0.5):
    # one finger up to the button and back, without looking (her eyes stay ahead); a tiny rise on her toes at the press
    B = add(BTN(k_), [0.0, 0.0, 0.03])
    rest = HAND(None, hd, 'rest', 'grip')
    up = HAND(add(B, [0.12, -0.08, 0.08]), hd, 'point', 'grip', tipR=0.15, hose=0.12)
    push = HAND(B, hd, 'point', 'grip', tipR=0.15, hose=0.12)
    return [k(r(t0 - 0.22), toon={**up, 'face': face}, toonDur=0.16, toonEase='inOut'),
            k(r(t0 - 0.02), toon={**push, 'sq': [0.97, 1.04, 0.97], 'face': face}, toonDur=0.05),
            k(r(t0 + 0.12), toon={**push, 'face': face}, toonDur=0.05),
            k(r(t0 + 0.22), toon={**up, 'face': face}, toonDur=0.08),
            k(r(t0 + dur), toon={**rest, 'face': face}, toonDur=0.2, toonEase='inOut')]

# 2: « Il n'arrivait jamais avant le noir. » The cutaway, floors three to five: he sprints up the flights, legs a blur; on the fifth landing he skids, turns to
#    us, and the light cuts out on « noir »: everything drops to deep blue, the steps' noses and the handrails stay as pale lines, only his two big white eyes
#    hang there, blinking twice; two floors down, in a warm pool of her own, the neighbour presses the button of her landing with one finger, deadpan
D2 = st.dur('S02'); NOIR2 = W('S02', 'L02', 5)
V2 = [1.8, FH * 3, 0.62]; RYV2 = -18
TP2, HD2 = VSTAND(V2, RYV2)
RUN2 = [[2.6, FH * 4, 1.05], [1.45, FH * 4, 0.97], [-1.35, FH * 4 + 1.45, 0.97], [-2.05, FH * 4 + 1.4, 0.4], [-2.0, FH * 4 + 1.4, -0.75], [-1.35, FH * 4 + 1.45, -0.97], [1.45, FH * 5, -0.97], [2.35, FH * 5, -0.55]]
STOP2 = r(NOIR2 - 0.1)
H2 = RUN2[-1]
F2, L2, LN2 = FIT([0.4, 12.4, 11.5], {'vfeet': V2, 'vhead': add(V2, [0, 2.0, 0]), 'hhead': add(H2, [0, 2.4, 0]), 'half': [-2.4, FH * 4 + 3.8, 0.4], 'foot4': [2.7, FH * 4, 1.0], 'btn3': BTN(3)}, margin=0.1, top=0.1, bottom=0.74)
C2 = cam(0.0, F2, add(F2, [0.0, 0.25, -0.3]), L2, add(L2, [0.0, 0.25, 0.0]), lens=LN2, ease='inOut')
chk2('S02', C2, {'vhead': add(V2, [0, 1.95, 0]), 'vfeet': V2, 'hhead': add(H2, [0, 2.35, 0]), 'hfeet': H2, 'btn3': BTN(3), 'btn5': BTN(5)}, heads=('vhead', 'hhead'))
RUNT = {'hip': 0, 'autoSq': 0.3, 'smear': 0.6, 'face': HFD}
HK2 = [k(0.0, path=RUN2, dur=r(STOP2), clip='run', ease='linear', speed=1.6), k(0.0, toon={**RUNT, 'bend': {'spine': [0.3, 0, 0, 1, None]}}, toonDur=0.0),
       k(STOP2, clip='skidStop', blend=0.03), k(STOP2, toon={'hip': 0, 'sq': [1.12, 0.88, 1.12], 'hairUp': 0.6, 'face': {**HFD, 'eye': 0.3}}, toonDur=0.04),
       k(r(STOP2 + 0.02), face=8, turn=0.08), k(r(STOP2 - 0.3), look='camera', lookDur=0.1),
       k(r(NOIR2 + 0.02), toon={'hip': 0, 'face': {**HF, 'lid': 0.0, 'eye': 0.6, 'brow': 0.7, 'mouth': 'o'}}, toonDur=0.05),
       *blink(r(NOIR2 + 0.17), {**HF, 'lid': 0.0, 'eye': 0.6, 'brow': 0.7, 'mouth': 'o'}, {'hip': 0}), *blink(r(NOIR2 + 0.4), {**HF, 'lid': 0.0, 'eye': 0.6, 'brow': 0.7, 'mouth': 'o'}, {'hip': 0})]
PRESS2 = r(NOIR2 + 0.22)
VK2 = [k(-0.5, look=lerp3(add(V2, [0, 1.8, 0]), F2, 0.7)), k(0.0, toon={**HAND(None, HD2, 'rest', 'grip'), 'face': VF}, toonDur=0.0),
       *life(0.05, r(PRESS2 - 0.3), VF, HAND(None, HD2, 'rest', 'grip'), blinks=[0.5], period=0.7),
       *PRESS_KEYS(V2, RYV2, 3, PRESS2, HD2)]
st.shot('S02', SET, setOpts=SETO, look=LOOK_IN, dark=[[0, 0, 0.0], [NOIR2, 1, 0.0]], **DARK, darkPool={'actor': 'voisine', 'joint': 'torso', 'r': 1.2, 'k': 1.0, 'tint': '#FFD9A0'},
        actors=[act('mec', RUN2[0], -90, 'run', 'neutral', keys=HK2), act('voisine', V2, RYV2, 'stand', 'neutral', keys=VK2)],
        props=[WELL('2', lit=[[0, 1], [NOIR2, 0]], **{'from': 2}), BTNS('2', floors=[3, 4, 5, 6], big=False, press=[[3, PRESS2]]), LINES('2', on=NOIR2, **{'from': 2}), BRIEF('2'),
               TROLLEY('2', TP2, yaw(TP2, V2)), P('vitesse2', 'speedLines', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.2, -0.5]}, keys=[k(0.0, visible=True), k(STOP2, visible=False)])],
        cams=[C2])
GAG('S02', r(NOIR2 + 0.1), 'mec', 'only his eyes in the dark'); GAG('S02', PRESS2, 'voisine', 'presses her button in her own light')
for i_ in range(7): st.cue('sfx:stepRun', 'S02', r(0.05 + 0.15 * i_), 0.16)
st.cue('sfx:brake', 'S02', STOP2, 0.2); st.cue('sfx:click', 'S02', NOIR2, 0.35); st.cue('sfx:click', 'S02', PRESS2, 0.25)

# 2b: « Il s'est payé un entraîneur. » The next evening, in the hall: a coach in a plain blue tracksuit blows his whistle (cheeks puffed) and clicks a
#     stopwatch held up by his face (hands and ticks only); in his suit, ankle weights over his trousers, the hero skips with his own tie, a red cord
#     swung round him in hops (a stretch up, a squash down)
D2b = st.dur('S02b')
CO = [2.8, G, 0.45]; RYCO = 38
HB = [4.3, G, -0.3]; RYHB = -28
DT2b = 0.32; T02b = 0.04; NH = int((D2b - T02b) / DT2b) + 2
HOPK, HOPT = hops_ball(T02b, [[HB[0], HB[2]]] * (NH + 1), [0.34] * NH, DT2b, y0=G, hold=0.06)
PEAK0 = T02b + (DT2b - 0.06) / 2
TOUCH2b = {'touch': {'R': ['torso', -0.44, 0.3, 0.3, 1, 0.0], 'L': ['torso', 0.44, 0.3, 0.3, 1, 0.0]}, 'hands': {'R': 'fist', 'L': 'fist'}, 'hip': 0, 'tieHide': 1}
HK2b = [k(-0.5, look='camera'), k(0.0, toon={**TOUCH2b, 'face': HFD, 'autoSq': 0}, toonDur=0.0), *HOPK,
        *[k(x['at'], toon={**TOUCH2b, **x['toon'], 'autoSq': 0, 'face': {**HFD, 'mouth': 'clench'}}, toonDur=x.get('toonDur', 0.05), toonEase=x.get('toonEase', 'out')) for x in HOPT]]
F2b, L2b, LN2b = FIT([3.6, 1.3, 5.9], {'cohead': add(CO, [0, 2.6, 0]), 'cofeet': CO, 'hhead': add(HB, [0, 2.95, 0]), 'hfeet': add(HB, [0, -0.02, 0.3]), 'rope': off(HB, RYHB, 0.2, 0.6, 2.9)}, margin=0.15, top=0.12, bottom=0.74)
C2b = cam(0.0, F2b, add(F2b, [0.0, 0.0, -0.2]), L2b, L2b, lens=LN2b, ease='inOut')
chk2('S02b', C2b, {'cohead': add(CO, [0, 2.3, 0]), 'hhead': add(HB, [0, 2.7, 0]), 'hfeet': HB, 'watch': off(CO, RYCO, 0.25, -0.3, 2.05)}, heads=('cohead', 'hhead'))
WATCH = off(CO, RYCO, 0.34, -0.36, 1.78)
CF = {'lid': 0.2, 'mouth': 'whistle', 'brow': -0.4}
COK = [k(-0.5, look=lerp3(add(HB, [0, 1.8, 0]), F2b, 0.5)), k(0.0, toon={**HAND(WATCH, None, 'fist', 'rest', hose=0.2), 'face': {**CF, 'puff': 0.2}}, toonDur=0.0),
       *[k(r(t_), toon={**HAND(WATCH, None, 'fist', 'rest', hose=0.2), 'sq': sq_, 'face': {**CF, 'puff': pf, 'lid': ld}}, toonDur=0.05) for t_, sq_, pf, ld in
         [(0.08, [0.97, 1.04, 0.97], 1.0, 0.6), (0.42, [1.0, 1.0, 1.0], 0.15, 0.2), (0.62, [0.97, 1.04, 0.97], 1.0, 0.6), (0.95, [1.0, 1.0, 1.0], 0.15, 0.2)]],
       k(1.1, toon={**HAND(add(WATCH, [0, -0.04, 0]), None, 'fist', 'rest', hose=0.2), 'sq': [1.02, 0.98, 1.02], 'face': {**CF, 'puff': 0.1, 'mouth': 'smirk'}}, toonDur=0.05),
       *blink(1.25, {**CF, 'mouth': 'smirk'}, HAND(WATCH, None, 'fist', 'rest', hose=0.2))]
st.shot('S02b', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('coach', CO, RYCO, 'stand', 'neutral', keys=COK), act('mec', HB, RYHB, 'stand', 'neutral', keys=HK2b)],
        props=[WELL('2b', top=1), BTNS('2b', floors=[0, 1]), P('corde2b', 'mnTieRope', on={'actor': 'mec', 'joint': 'torso', 'offset': [0, 0.3, 0.3]}, opts={'half': 0.44, 'r': 1.26, 'spin': r(1 / DT2b, 3), 't0': 0.0, 'a0': r(-2 * PI * PEAK0 / DT2b, 3)}),
               P('lest2bL', 'mnAnkleWeight', on={'actor': 'mec', 'joint': 'footL', 'offset': [0, 0.0, 0]}), P('lest2bR', 'mnAnkleWeight', on={'actor': 'mec', 'joint': 'footR', 'offset': [0, 0.0, 0]}),
               P('sifflet2b', 'whistle', on={'actor': 'coach', 'joint': 'head', 'offset': [0.0, 0.1, 0.13], 'rot': [0, 1.5708, 0]}, scale=2.6),
               P('chrono2b', 'stopwatch', on={'actor': 'coach', 'hand': 'R', 'face': 'camera'}, scale=2.3)],
        cams=[C2b])
GAG('S02b', 0.5, 'mec', 'skips with his tie'); GAG('S02b', 0.1, 'coach', 'whistle')
st.cue('sfx:whistle', 'S02b', 0.08, 0.3); st.cue('sfx:tick', 'S02b', 1.1, 0.4)
for i_ in range(NH): st.cue('sfx:step', 'S02b', r(T02b + DT2b * (i_ + 1) - 0.06), 0.18)

# 3: « Un soir, » The hall again, lower and closer: dark, his hand already up; the slap, the light, a crouch and he is gone (a dashed hole of speed)
D3 = st.dur('S03'); SLAP3 = 0.07; GO3 = 0.3
H3 = [5.52, G, -0.98]; RY3 = -48
WIND3 = off(H3, RY3, 0.1, 0.42, 2.45); HIT3 = add(BIG, [0.0, 0.0, 0.08])
F3, L3, LN3 = FIT([4.3, 0.62, 1.75], {'head': add(H3, [0, 2.45, 0]), 'knee': add(H3, [0, 0.6, 0.2]), 'btn': BIG, 'wind': WIND3}, margin=0.16, top=0.1, bottom=0.74)
C3 = cam(0.0, F3, add(F3, [0.06, 0.0, -0.08]), L3, L3, lens=LN3, ease='inOut')
chk2('S03', C3, {'head': add(H3, [0, 2.35, 0]), 'btn': BIG, 'wind': WIND3}, heads=('head',))
HK3 = [k(-0.5, look='camera'), k(0.0, toon={**HAND(WIND3, None, 'open'), 'sq': [0.95, 1.06, 0.95], 'face': HFD}, toonDur=0.0),
       k(SLAP3, toon={**HAND(HIT3, None, 'open', tipR=0.1), 'sq': [1.14, 0.86, 1.14], 'hairUp': 0.9, 'face': {**HFD, 'eye': 0.3}}, toonDur=0.04, toonEase='in'),
       k(r(GO3 - 0.13), toon={'sq': [1.18, 0.8, 1.18], 'hip': 0, 'bend': {'spine': [0.4, 0, 0, 1, None]}, 'face': {**HFD, 'mouth': 'clench'}, 'auto': 0}, toonDur=0.07),
       k(r(GO3 - 0.13), face=-70, turn=0.06),
       k(GO3, to=[1.0, G, 0.8], dur=0.3, ease='linear', clip='run', face=-70),
       k(GO3, toon={'sq': [0.84, 1.22, 0.84], 'hip': 0, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': HFD, 'smear': 0.8}, toonDur=0.04)]
st.shot('S03', SET, setOpts=SETO, look=LOOK_IN, dark=[[0, 1, 0.0], [SLAP3, 0, 0.0]], **DARK,
        actors=[act('mec', H3, RY3, 'stand', 'neutral', keys=HK3)],
        props=[WELL('3', lit=[[0, 0], [SLAP3, 1]], top=2), BTNS('3', press=[[0, SLAP3]], floors=[0, 1, 2]), LINES('3', on=0.0, off_=SLAP3, top=2), BRIEF('3'),
               P('trou3', 'mnGhost', pos=H3, ry=RY3 + 48, opts={'at': r(GO3 + 0.05), 'dir': -1, 'dur': 0.45})],
        cams=[C3])
GAG('S03', 0.2, 'mec', 'slap and crouch')
st.cue('clack', 'S03', SLAP3, 0.5); st.cue('whoosh', 'S03', GO3, 0.3, 0.3, 600, 3000)

# 3b: « il a eu la lumière jusqu'à sa porte. » The seventh landing, still lit: he skids in from the top of the stairs, his left arm shooting out like
#     rubber across the frame to the lock, the key already in it; he turns to us and pumps both fists, a hop, a huge grin (VICTOIRE); on « porte » the
#     light cuts to deep blue: the grin and the eyes hang in the dark
D3b = st.dur('S03b'); PORTE3 = W('S03b', 'L03', 9)
H3a = [0.95, FH * 7, -0.88]; H3b = [1.95, FH * 7, -0.95]; RY3b = 90
F3b, L3b, LN3b = FIT([3.6, FH * 7 + 1.25, 3.6], {'h0': add(H3a, [0, 2.4, 0]), 'h1': add(H3b, [0, 2.45, 0.2]), 'fists': add(H3b, [0, 2.75, 0.3]), 'lock': LOCK7, 'feet': add(H3b, [0, 0.05, 0.3]), 'f0': add(H3a, [0, 0.05, 0])}, margin=0.13, top=0.22, bottom=0.74)
C3b = cam(0.0, F3b, add(F3b, [-0.1, 0.0, -0.2]), L3b, L3b, lens=LN3b, ease='inOut')
chk2('S03b', C3b, {'h0': add(H3a, [0, 2.35, 0]), 'h1': add(H3b, [0, 2.4, 0]), 'fists': add(H3b, [0, 2.6, 0.3]), 'lock': LOCK7, 'feet': H3b}, heads=('h0', 'h1', 'fists'), card=True)
ARM3 = 0.08; KEY3 = 0.24; TURN3 = 0.52
FR3 = off(H3b, 10, 0.18, 0.36, 2.2); FL3 = off(H3b, 10, 0.18, -0.36, 2.2)
VIC = lambda dy, **x: {**HAND(add(FR3, [0, dy, 0]), add(FL3, [0, dy, 0]), 'fist', 'fist', hose=0.25), **x}
GRIN = {'lid': 0.0, 'mouth': 'bigsmile', 'brow': 0.8, 'eye': 0.25}
HK3b = [k(-0.5, look=[3.2, FH * 7 + 2.0, 0.2]),
        k(0.0, to=H3b, dur=0.36, ease='out', glide=True, face=90), k(0.0, clip='skidStop'),
        k(0.0, toon={'hip': 0, 'sq': [1.05, 0.95, 1.05], 'face': HFD, 'auto': 0}, toonDur=0.0),
        k(ARM3, toon={**HAND(None, add(LOCK7, [0, 0, 0.05]), 'rest', 'pinch', tipL=0.08, hose=0.0), 'sq': [0.92, 1.08, 0.92], 'bend': {'spine': [-0.15, 0, 0, 1, None]}, 'face': {**HFD, 'eye': 0.3}, 'auto': 0}, toonDur=0.08, toonEase='outBack'),
        k(r(KEY3 + 0.06), toon={**HAND(None, add(LOCK7, [0, 0, 0.05]), 'rest', 'pinch', tipL=0.08), 'sq': [1.12, 0.88, 1.12], 'hairUp': 0.5, 'face': {**HFD, 'mouth': 'smirk'}, 'auto': 0}, toonDur=0.05),
        k(r(TURN3 - 0.06), face=10, turn=0.12), k(r(TURN3 - 0.04), look='camera', lookDur=0.1),
        k(TURN3, toon={**VIC(-0.25), 'sq': [1.1, 0.9, 1.1], 'face': GRIN}, toonDur=0.08),
        *[k(r(TURN3 + 0.12 + 0.2 * j), toon={**VIC(0.12 if j % 2 == 0 else -0.15), 'sq': [0.92, 1.1, 0.92] if j % 2 == 0 else [1.06, 0.95, 1.06], 'hairUp': 0.4 if j % 2 == 0 else 0.1, 'face': GRIN}, toonDur=0.07, toonEase='outBack') for j in range(5)],
        k(r(PORTE3 + 0.04), toon={**VIC(0.05), 'face': GRIN}, toonDur=0.08), *blink(r(PORTE3 + 0.22), GRIN, VIC(0.05))]
st.shot('S03b', SET, setOpts=SETO, look=LOOK_IN, dark=[[0, 0, 0.0], [PORTE3, 1, 0.0]], **DARK,
        actors=[act('mec', H3a, RY3b, 'run', 'neutral', keys=HK3b)],
        props=[WELL('3b', lit=[[0, 1], [PORTE3, 0]], topH=3.6, hall=False, **{'from': 6}), BTNS('3b', floors=[6, 7], big=False), LINES('3b', on=PORTE3, **{'from': 6}), BRIEF('3b'),
               P('cle3b', 'mnKey', pos=add(LOCK7, [0, 0, 0.02]), keys=[k(0.0, visible=False), k(KEY3, visible=True)], opts={'turn': [[0, 0], [r(KEY3 + 0.05), 0], [r(KEY3 + 0.12), 1.4]]}, inDark=True)],
        cams=[C3b])
st.card('S03b', 'VICTOIRE', at=0.55)
GAG('S03b', r(KEY3), 'mec', 'rubber arm to the lock'); GAG('S03b', 0.95, 'mec', 'victory pumps'); GAG('S03b', r(PORTE3 + 0.12), 'mec', 'grin in the dark')
st.cue('sfx:brake', 'S03b', 0.0, 0.2); st.cue('sfx:stretch', 'S03b', ARM3, 0.15); st.cue('sfx:click', 'S03b', r(KEY3 + 0.08), 0.3); st.cue('sfx:tada', 'S03b', TURN3, 0.18); st.cue('sfx:click', 'S03b', PORTE3, 0.35)

# ============================== the landlord: thin, grey suit, mustard tie, small round glasses, a clipboard
PF = {'lid': 0.35, 'mouth': 'line', 'brow': -0.5}
TB = [2.05, 1.5, -1.5]                    # the timer's grey box, on the back wall of the hall, under the first landing
KNOB = [2.05, 1.53, -1.35]
def TIMER(n, hand, open_=1.0, click=None): return P(f'minuterie{n}', 'mnTimerBox', pos=TB, opts={'hand': hand, 'open': open_, **({'click': click} if click else {})})

# 4: « Le propriétaire a trouvé ça trop long : » The hall: the landlord opens the little grey box (a dial, one hand, six ticks, a pale bar), leans in and
#    frowns at it, then frowns at us and ticks his clipboard; behind him the neighbour crosses the hall with her trolley toward the stairs
D4 = st.dur('S04')
PR4 = [2.62, G, -0.92]; RYPR4 = -62
OPEN4 = 0.22; TICK4 = 1.45
CLIP4 = off(PR4, RYPR4, 0.4, -0.22, 1.32)
F4, L4, LN4 = FIT([-0.35, 1.45, 1.3], {'head': add(PR4, [0, 2.4, 0]), 'box': add(TB, [0, 0.3, 0.1]), 'box2': add(TB, [0, -0.3, 0.1]), 'chest': add(PR4, [0, 1.2, 0.2]), 'vback': [4.8, 2.2, 0.0]}, margin=0.15, top=0.12, bottom=0.74)
C4 = cam(0.0, F4, add(F4, [0.15, 0.0, -0.1]), L4, L4, lens=LN4, ease='inOut')
chk2('S04', C4, {'head': add(PR4, [0, 2.35, 0]), 'box': TB, 'clip': CLIP4, 'v0': [4.8, 1.9, 0.1], 'v1': [1.9, 1.9, 0.75]}, heads=('head', 'v0', 'v1'))
HOLDC = lambda **x: {**HAND(None, CLIP4, 'rest', 'grip'), **x}
PK4 = [k(-0.5, look=lerp3(TB, F4, 0.35)), k(0.0, toon={**HOLDC(), 'face': PF}, toonDur=0.0),
       k(r(OPEN4 - 0.12), toon={**HOLDC(), 'reach': {'R': R5(add(TB, [0.2, 0.0, 0.16]), 1, 0.08), 'L': R5(CLIP4)}, 'hands': {'R': 'pinch', 'L': 'grip'}, 'face': PF}, toonDur=0.12),
       k(r(OPEN4 + 0.1), toon={**HOLDC(), 'reach': {'R': R5(add(TB, [-0.12, 0.0, 0.3]), 1, 0.08), 'L': R5(CLIP4)}, 'hands': {'R': 'pinch', 'L': 'grip'}, 'face': PF}, toonDur=0.14),
       k(0.45, toon={**HOLDC(), 'bend': {'spine': [0.18, 0, 0, 1, None], 'neck': [0.15, 0, 0, 1, None]}, 'face': {**PF, 'brow': -0.8, 'lid': 0.5, 'gx': -0.6}}, toonDur=0.16),
       k(0.95, look='camera', lookDur=0.12),
       k(1.0, toon={**HOLDC(), 'sq': [1.02, 0.98, 1.02], 'face': {**PF, 'brow': -0.9, 'mouth': 'line', 'lid': 0.4}}, toonDur=0.1),
       k(r(TICK4 - 0.12), toon={**HAND(add(CLIP4, [0.0, 0.1, 0.06]), CLIP4, 'point', 'grip', tipR=0.15), 'face': {**PF, 'gy': 0.6}}, toonDur=0.1),
       k(TICK4, toon={**HAND(add(CLIP4, [0.03, 0.04, 0.05]), CLIP4, 'point', 'grip', tipR=0.15), 'sq': [1.03, 0.97, 1.03], 'face': {**PF, 'gy': 0.6, 'mouth': 'smirk'}}, toonDur=0.05),
       k(r(TICK4 + 0.2), toon={**HOLDC(), 'face': {**PF, 'mouth': 'smirk'}}, toonDur=0.15)]
V4a = [5.0, G, 0.05]; V4b = [1.78, G, 0.72]
VK4 = [k(-0.5, look=[1.2, 1.7, 0.9]), k(0.05, to=V4b, dur=1.55, clip='walk', ease='linear', speed=0.85), k(1.62, face=-40, turn=0.2),
       k(0.0, toon={**VTT, 'face': VF}, toonDur=0.0)]
TRK4 = [k(0.12, to=off(V4b, -78, -0.5), dur=1.55, ease='linear')]
st.shot('S04', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('proprio', PR4, RYPR4, 'stand', 'neutral', keys=PK4), act('voisine', V4a, -78, 'walk', 'neutral', keys=VK4)],
        props=[WELL('4', top=1, front=True), BTNS('4', floors=[0, 1]), TIMER('4', 1.0, [[0, 0], [OPEN4, 1.0]]), P('bloc4', 'mnClipboard', on={'actor': 'proprio', 'hand': 'L', 'face': 'camera'}, opts={'tick': [TICK4]}),
               TROLLEY('4', off(V4a, -78, -0.5), -78, keys=TRK4)],
        cams=[C4])
GAG('S04', 1.1, 'proprio', 'frowns at the dial, then at us'); GAG('S04', 1.6, 'voisine', 'crosses toward the stairs')
st.cue('sfx:squeak', 'S04', OPEN4, 0.2); st.cue('sfx:paper', 'S04', TICK4, 0.25)

# 4b: « quinze secondes. » Close on the dial: his finger and thumb pinch the knob and turn it half way down; the hand snaps to the middle tick, the pale bar
#     halves, the box jolts: CLIC
D4b = st.dur('S04b'); SNAP4 = 0.42
F4b = [1.78, 1.66, -0.32]; L4b = add(TB, [0.0, 0.04, 0.12])
C4b = cam(0.0, F4b, add(F4b, [-0.04, 0.0, -0.08]), L4b, L4b, lens=34, ease='inOut')
chk2('S04b', C4b, {'box_tl': add(TB, [-0.18, 0.23, 0.11]), 'box_br': add(TB, [0.18, -0.23, 0.11]), 'knob': KNOB})
PK4b = [k(-0.5, look=TB), k(0.0, toon={**HAND(add(KNOB, [0.1, -0.1, 0.12]), None, 'pinch', 'rest', tipR=0.08), 'face': PF}, toonDur=0.0),
        k(0.12, toon={**HAND(add(KNOB, [0.0, -0.01, 0.05]), None, 'pinch', 'rest', tipR=0.08), 'face': PF}, toonDur=0.12),
        k(r(SNAP4 - 0.04), toon={**HAND(add(KNOB, [-0.03, 0.0, 0.05]), None, 'pinch', 'rest', tipR=0.08), 'face': PF}, toonDur=0.08),
        k(r(SNAP4 + 0.25), toon={**HAND(add(KNOB, [0.12, -0.15, 0.2]), None, 'open', 'rest', tipR=0.08), 'face': PF}, toonDur=0.15)]
st.shot('S04b', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('proprio', [2.55, G, -0.75], -110, 'stand', 'neutral', keys=PK4b)],
        props=[WELL('4b', top=1), TIMER('4b', [[0, 1.0], [r(SNAP4 - 0.08), 0.92], [SNAP4, 0.5, 'step']], 1.0, [SNAP4])],
        cams=[C4b])
st.text('S04b', 0.7, 'minuterie4b', 'the dial halved')
st.cue('sfx:click', 'S04b', SNAP4, 0.5); st.cue('clack', 'S04b', SNAP4, 0.2)

# ============================== the stride: one flight in one leap (a `to` key per frame: an even horizontal travel, a height in 1 - |2u - 1|^2.5)
def LEAP(p0, p1, t0, dur, peak, face):
    n = max(2, int(round(dur * 30))); out = []
    for i in range(1, n + 1):
        u = i / n; pos = lerp3(p0, p1, u); pos[1] = r(pos[1] + peak * (1 - abs(2 * u - 1) ** 2.5))
        out.append(k(r(t0 + dur * (i - 1) / n), to=pos, dur=r(dur / n), ease='linear', glide=True, face=face))
    return out
SCISSOR = {'legR': [-1.3, 0, 0, 1.75, None], 'shinR': [0.15, 0, 0, 1.3, None], 'legL': [1.15, 0, 0, 1.75, None], 'shinL': [0.35, 0, 0, 1.3, None],
           'armR': [0.9, 0, 0, 1.2, None], 'armL': [-1.0, 0, 0, 1.2, None]}
def STRIDE_KEYS(p_run0, p_take, p_land, t_take, t_land, face, exit_to=None, t_exit=None):
    ks = [k(0.0, to=p_take, dur=r(t_take - 0.1), clip='run', ease='linear', face=face, speed=1.5), k(0.0, toon={**RUNT}, toonDur=0.0),
          k(r(t_take - 0.1), toon={'hip': 0, 'sq': [1.2, 0.78, 1.2], 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': HFD, 'auto': 0}, toonDur=0.06),
          k(r(t_take - 0.1), clip='stand', blend=0.05),
          *LEAP(p_take, p_land, t_take, r(t_land - t_take), 1.0, face),
          k(t_take, toon={'hip': 0, 'sq': [0.88, 1.16, 0.88], 'bend': SCISSOR, 'hairUp': 0.7, 'face': {**HFD, 'mouth': 'clench'}, 'auto': 0}, toonDur=0.06, toonEase='outBack'),
          k(r(t_land - 0.06), toon={'hip': 0, 'sq': [0.95, 1.06, 0.95], 'bend': {**SCISSOR, 'legR': [-0.5, 0, 0, 1.2, None], 'legL': [0.4, 0, 0, 1.2, None]}, 'face': HFD, 'auto': 0}, toonDur=0.05),
          k(t_land, toon={'hip': 0, 'sq': [1.38, 0.64, 1.38], 'hairUp': 0.0, 'face': {**HFD, 'lid': 0.3}, 'auto': 0}, toonDur=0.03),
          k(r(t_land + 0.13), toon={'hip': 0, 'sq': [0.92, 1.1, 0.92], 'face': HFD, 'auto': 0}, toonDur=0.06, toonEase='outBack'),
          k(r(t_land + 0.24), toon={'hip': 0, 'sq': [1.0, 1.0, 1.0], 'face': HFD}, toonDur=0.08)]
    if exit_to: ks += [k(t_exit, to=exit_to, dur=0.4, clip='run', ease='in', speed=1.5), k(t_exit, toon={**RUNT}, toonDur=0.06)]
    return ks

# 5: « Ce mec a suivi. » The flight from the second landing, from the front: he runs in, crouches and takes the whole flight in one stride, legs scissored
#    across the frame (stretched, never along the lens), and lands on the half landing in a squash, springs up, turns for the next flight
D5 = st.dur('S05')
T5a = 0.16; T5b = 0.58
P5r = [3.0, FH * 2, 0.3]; P5t = [1.95, FH * 2, 0.95]; P5l = [-1.95, FH * 2 + 1.4, 0.95]
F5, L5, LN5 = FIT([0.1, 7.4, 9.2], {'r0': add(P5r, [0, 2.35, 0]), 'take': add(P5t, [0, 2.3, 0]), 'peak': [0.0, FH * 2 + 0.7 + 1.0 + 2.5, 0.95], 'land': add(P5l, [0, 2.3, 0]), 'landf': P5l, 'takef': P5t, 'legs': [1.0, FH * 2 + 1.2, 0.95], 'legs2': [-1.0, FH * 2 + 1.6, 0.95]}, margin=0.1, top=0.12, bottom=0.74)
C5 = cam(0.0, F5, add(F5, [-0.25, 0.1, 0.0]), L5, add(L5, [-0.25, 0.1, 0.0]), lens=LN5, ease='inOut')
chk2('S05', C5, {'take': add(P5t, [0, 2.3, 0]), 'peak': [0.0, FH * 2 + 4.2, 0.95], 'land': add(P5l, [0, 2.3, 0]), 'landf': P5l, 'takef': P5t}, heads=('take', 'peak', 'land'))
HK5 = [k(-0.5, look='camera'), *STRIDE_KEYS(P5r, P5t, P5l, T5a, T5b, -60, exit_to=[-2.0, FH * 2 + 1.4, -0.7], t_exit=r(D5 - 0.3))]
st.shot('S05', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('mec', P5r, -60, 'run', 'neutral', keys=HK5)],
        props=[WELL('5', top=4, hall=False, **{'from': 1}), BTNS('5', floors=[1, 2, 3, 4], big=False), BRIEF('5')],
        cams=[C5])
GAG('S05', r((T5a + T5b) / 2), 'mec', 'the whole flight in one stride'); GAG('S05', r(T5b + 0.05), 'mec', 'landing squash')
st.cue('sfx:stretch', 'S05', T5a, 0.15); st.cue('whoosh', 'S05', r(T5a + 0.05), 0.2, 0.35, 400, 2200); st.cue('thud', 'S05', T5b, 0.45); st.cue('sfx:boing', 'S05', r(T5b + 0.1), 0.12)

# 5b: « Cinq marches par enjambée. » A floor higher, the camera rising with him: the next flight in one stride; two floors below, the neighbour in her own
#     light has climbed exactly one step, and reaches back up to press the button of her landing, without looking
D5b = st.dur('S05b')
T5c = 0.12; T5d = 0.52
P6r = [2.6, FH * 3, 0.55]; P6t = [1.95, FH * 3, 0.95]; P6l = [-1.95, FH * 3 + 1.4, 0.95]
V5 = [1.78, FH * 2, 0.78]; V5s = [1.24, FH * 2 + 0.175, 0.92]; RYV5 = -55; STEP5 = 0.32; PRESS5 = 0.95
TP5 = [2.2, FH * 2, 0.95]; HD5 = handle(TP5, yaw(TP5, V5s))
F5b, L5b, LN5b = FIT([0.2, 8.6, 10.6], {'vfeet': V5, 'vhead': add(V5, [0, 2.0, 0]), 'take': add(P6t, [0, 2.3, 0]), 'peak': [0.0, FH * 3 + 4.2, 0.95], 'land': add(P6l, [0, 2.3, 0]), 'btn2': BTN(2), 'tro': TP5}, margin=0.1, top=0.1, bottom=0.74)
C5b = cam(0.0, F5b, add(F5b, [0.0, 0.35, -0.2]), L5b, add(L5b, [0.0, 0.45, 0.0]), lens=LN5b, ease='inOut')
chk2('S05b', C5b, {'vhead': add(V5s, [0, 1.95, 0]), 'vfeet': V5, 'take': add(P6t, [0, 2.3, 0]), 'peak': [0.0, FH * 3 + 4.2, 0.95], 'land': add(P6l, [0, 2.3, 0]), 'btn2': BTN(2)}, heads=('vhead', 'take', 'peak', 'land'))
HK5b = [k(-0.5, look='camera'), *STRIDE_KEYS(P6r, P6t, P6l, T5c, T5d, -60, exit_to=[-2.0, FH * 3 + 1.4, -0.7], t_exit=r(D5b - 0.35))]
VK5 = [k(-0.5, look=lerp3(add(V5, [0, 1.8, 0]), F5b, 0.6)), k(0.0, toon={**HAND(None, HD5, 'rest', 'grip'), 'face': VF}, toonDur=0.0),
       k(r(STEP5 - 0.08), toon={**HAND(None, HD5, 'rest', 'grip'), 'sq': [1.06, 0.94, 1.06], 'face': VF}, toonDur=0.06),
       k(STEP5, to=V5s, dur=0.2, ease='inOut', glide=True, face=RYV5),
       k(STEP5, toon={**HAND(None, HD5, 'rest', 'grip'), 'sq': [0.96, 1.06, 0.96], 'face': VF}, toonDur=0.08),
       k(r(STEP5 + 0.22), toon={**HAND(None, HD5, 'rest', 'grip'), 'sq': [1.05, 0.95, 1.05], 'face': VF}, toonDur=0.04),
       k(r(STEP5 + 0.32), toon={**HAND(None, HD5, 'rest', 'grip'), 'face': VF}, toonDur=0.08),
       *PRESS_KEYS(V5s, RYV5, 2, PRESS5, HD5)]
st.shot('S05b', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('mec', P6r, -60, 'run', 'neutral', keys=HK5b), act('voisine', V5, RYV5, 'stand', 'neutral', keys=VK5)],
        props=[WELL('5b', top=5, hall=False, **{'from': 1}), BTNS('5b', floors=[1, 2, 3, 4, 5], big=False, press=[[2, PRESS5]]), BRIEF('5b'), TROLLEY('5b', TP5, yaw(TP5, V5s))],
        cams=[C5b])
GAG('S05b', r((T5c + T5d) / 2), 'mec', 'next stride'); GAG('S05b', PRESS5, 'voisine', 'one step, one button')
st.cue('whoosh', 'S05b', r(T5c + 0.05), 0.2, 0.35, 400, 2200); st.cue('thud', 'S05b', T5d, 0.4); st.cue('sfx:step', 'S05b', r(STEP5 + 0.2), 0.2); st.cue('sfx:click', 'S05b', PRESS5, 0.3)

# 6: « Les champions s'entraînent dans son escalier. » The fourth landing: three champions in plain coloured kits sprint up from the flight below, round
#    the neighbour and up the next flight, one after the other; the gust blows her coat and her glasses askew; she presses the button, deadpan
D6 = st.dur('S06')
V6 = [1.76, FH * 4, 0.64]; RYV6 = -15; TP6 = off(V6, RYV6, -0.52, -0.3); HD6 = handle(TP6, yaw(TP6, V6)); PRESS6 = 1.42
PATH6 = [[0.2, FH * 4 - 0.32, -0.97], [1.6, FH * 4, -0.92], [2.45, FH * 4, -0.05], [2.25, FH * 4, 0.55], [1.3, FH * 4 + 0.1, 1.05], [-0.3, FH * 4 + 0.9, 1.0], [-1.6, FH * 4 + 1.45, 0.9]]
ATH = ['a1', 'a2', 'a3']; AT0 = [0.0, 0.22, 0.44]; ADUR = 1.0
F6, L6, LN6 = FIT([4.0, 12.7, 4.9], {'vhead': add(V6, [0, 2.0, 0]), 'vfeet': V6, 'p0': add(PATH6[0], [0, 2.3, 0]), 'p2': add(PATH6[2], [0, 2.4, 0]), 'p5': add(PATH6[5], [0, 2.4, 0]), 'btn': BTN(4), 'f5': PATH6[5]}, margin=0.12, top=0.1, bottom=0.74)
C6 = cam(0.0, F6, add(F6, [-0.2, 0.0, -0.25]), L6, L6, lens=LN6, ease='inOut')
chk2('S06', C6, {'vhead': add(V6, [0, 1.95, 0]), 'vfeet': V6, 'p0': add(PATH6[0], [0, 2.3, 0]), 'p2': add(PATH6[2], [0, 2.35, 0]), 'p4': add(PATH6[4], [0, 2.35, 0]), 'btn': BTN(4)}, heads=('vhead', 'p2', 'p4'))
AK6 = {a: [k(t0_, path=PATH6, dur=ADUR, clip='run', ease='linear', speed=1.4), k(0.0, toon={'hip': 0, 'autoSq': 0.3, 'smear': 0.6, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.0, 'mouth': 'clench', 'brow': -0.6}}, toonDur=0.0),
           k(0.0, visible=t0_ <= 0.0), *([k(t0_, visible=True)] if t0_ > 0 else []), k(r(t0_ + ADUR), visible=False)] for a, t0_ in zip(ATH, AT0)}
GUST = lambda t0_: [k(r(t0_), toon={**HAND(None, HD6, 'rest', 'grip'), 'wind': [-9, 2, 0], 'sq': [1.03, 0.97, 1.03], 'face': {**VF, 'lid': 0.6}}, toonDur=0.05), k(r(t0_ + 0.16), toon={**HAND(None, HD6, 'rest', 'grip'), 'wind': [0, 0, 0], 'face': VF}, toonDur=0.15)]
VK6 = [k(-0.5, look=lerp3(add(V6, [0, 1.8, 0]), F6, 0.7)), k(0.0, toon={**HAND(None, HD6, 'rest', 'grip'), 'face': VF}, toonDur=0.0),
       *GUST(0.62), *GUST(0.84), *GUST(1.06), *PRESS_KEYS(V6, RYV6, 4, PRESS6, HD6), *blink(1.8, VF, HAND(None, HD6, 'rest', 'grip'))]
st.shot('S06', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('voisine', V6, RYV6, 'stand', 'neutral', keys=VK6), *[act(a, PATH6[0], 90, 'run', 'neutral', keys=AK6[a]) for a in ATH]],
        props=[WELL('6', top=5, hall=False, **{'from': 3}), BTNS('6', floors=[3, 4, 5], big=False, press=[[4, PRESS6]]), TROLLEY('6', TP6, yaw(TP6, V6))],
        cams=[C6])
GAG('S06', 0.75, 'voisine', 'champions sprint past her'); GAG('S06', PRESS6, 'voisine', 'presses, deadpan')
for t_ in (0.62, 0.84, 1.06): st.cue('whoosh', 'S06', t_, 0.18, 0.25, 500, 2500)
st.cue('sfx:click', 'S06', PRESS6, 0.3)

# 6b: « Le propriétaire fait payer l'entrée. » The hall, at the foot of the stairs: the three champions queue, bouncing on their toes and stretching their
#     calves; the landlord tears a blank ticket off a roll (it flies to the first one), a plain gold coin flies back into his breast pocket, KA-CHING, a smirk
D6b = st.dur('S06b')
PR6 = [1.95, G, 0.9]; RYPR6 = 58
AQ = {'a1': ([2.8, G, 0.62], -72), 'a2': ([3.5, G, 0.32], -66), 'a3': ([4.2, G, 0.02], -60)}
TR6 = off(PR6, RYPR6, 0.42, -0.18, 1.32); TEAR6 = [0.42, 1.2]; POCK6 = off(PR6, RYPR6, 0.12, 0.13, 1.62)
COIN6 = [(0.62, add(off(AQ['a1'][0], AQ['a1'][1], 0.4, -0.2, 1.3), [0, 0, 0])), (1.4, off(AQ['a2'][0], AQ['a2'][1], 0.4, -0.2, 1.3))]
F6b, L6b, LN6b = FIT([3.25, 1.45, 4.9], {'phead': add(PR6, [0, 2.4, 0]), 'pfeet': PR6, 'a3head': add(AQ['a3'][0], [0, 2.5, 0]), 'a3feet': AQ['a3'][0], 'a1head': add(AQ['a1'][0], [0, 2.5, 0])}, margin=0.13, top=0.12, bottom=0.74)
C6b = cam(0.0, F6b, add(F6b, [0.15, 0.0, -0.25]), L6b, L6b, lens=LN6b, ease='inOut')
chk2('S06b', C6b, {'phead': add(PR6, [0, 2.4, 0]), 'a1head': add(AQ['a1'][0], [0, 2.4, 0]), 'a3head': add(AQ['a3'][0], [0, 2.4, 0]), 'roll': TR6}, heads=('phead', 'a1head', 'a3head'))
HOLD6 = lambda R=None, hr='rest', **x: {**HAND(R, add(TR6, [0.0, 0.0, 0.0]), hr, 'grip'), **x}
PK6 = [k(-0.5, look=lerp3(add(AQ['a1'][0], [0, 1.8, 0]), F6b, 0.5)), k(0.0, toon={**HOLD6(), 'face': PF}, toonDur=0.0)]
for tt in TEAR6:
    PK6 += [k(r(tt - 0.16), toon={**HOLD6(add(TR6, [0.05, -0.12, 0.05]), 'pinch'), 'face': PF}, toonDur=0.1),
            k(r(tt), toon={**HOLD6(add(TR6, [0.25, -0.15, 0.18]), 'pinch', sq=[1.03, 0.97, 1.03]), 'face': PF}, toonDur=0.05),
            k(r(tt + 0.22), toon={**HOLD6(), 'face': PF}, toonDur=0.12)]
PK6 += [k(r(COIN6[0][0] + 0.25), toon={**HOLD6(), 'sq': [0.97, 1.04, 0.97], 'face': {**PF, 'mouth': 'smirk', 'brow': 0.3}}, toonDur=0.06), k(r(COIN6[0][0] + 0.25), look='camera', lookDur=0.1),
        k(r(COIN6[1][0] + 0.25), toon={**HOLD6(), 'sq': [0.97, 1.04, 0.97], 'face': {**PF, 'mouth': 'smirk', 'brow': 0.5, 'lid': 0.5}}, toonDur=0.06)]
AF = {'lid': 0.1, 'mouth': 'line', 'brow': -0.3}
def CALF(a, t0_):
    # bouncing on his toes, then a calf stretch (one leg back, the knee of the other bent), hands on the hips
    p, ry = AQ[a]; out = [k(-0.5, look=lerp3(add(PR6, [0, 1.9, 0]), F6b, 0.4)), k(0.0, toon={'hip': 0, 'face': AF}, toonDur=0.0)]
    for j in range(4):
        t_ = r(t0_ + 0.22 * j); out += [k(t_, toon={'hip': 0, 'sq': [0.95, 1.07, 0.95], 'face': AF}, toonDur=0.08), k(r(t_ + 0.11), toon={'hip': 0, 'sq': [1.04, 0.96, 1.04], 'face': AF}, toonDur=0.08)]
    t_ = r(t0_ + 0.95); out += [k(t_, toon={'hip': 0, 'bend': {'legL': [0.55, 0, 0, 1.1, None], 'legR': [-0.35, 0, 0, 1, None], 'shinR': [0.45, 0, 0, 1, None], 'spine': [0.25, 0, 0, 1, None]}, 'sq': [1.02, 0.97, 1.02], 'face': AF}, toonDur=0.15)]
    return out
AK6b = {a: CALF(a, t0_) for a, t0_ in zip(['a1', 'a2', 'a3'], [0.0, 0.1, 0.05])}
AK6b['a1'] += [k(r(TEAR6[0] + 0.2), toon={**HAND(add(off(AQ['a1'][0], AQ['a1'][1], 0.42, -0.2, 1.3), [0, 0.0, 0]), None, 'pinch', 'rest'), 'face': AF}, toonDur=0.1),
               k(r(COIN6[0][0] + 0.25), toon={'hip': 0, 'face': AF}, toonDur=0.15)]
TKT6 = [P(f'billet6b{i}', 'mnTicketRoll', pos=TR6, ry=RYPR6, opts={'tear': [tt]}) for i, tt in enumerate(TEAR6[:1])]
COINP6 = [P(f'piece6b{i}', 'mnCoins', pos=c0, opts={'n': 1, 'r': 0.07}, keys=[k(0.0, visible=False), k(t0_, visible=True), k(t0_, to=POCK6, dur=0.24, ease='inOut'), k(r(t0_ + 0.26), visible=False)]) for i, (t0_, c0) in enumerate(COIN6)]
st.shot('S06b', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('proprio', PR6, RYPR6, 'stand', 'neutral', keys=PK6), *[act(a, AQ[a][0], AQ[a][1], 'stand', 'neutral', keys=AK6b[a]) for a in ['a1', 'a2', 'a3']]],
        props=[WELL('6b', top=1), BTNS('6b', floors=[0, 1]), P('rouleau6b', 'mnTicketRoll', pos=TR6, ry=RYPR6, opts={'tear': TEAR6}), *COINP6],
        cams=[C6b])
GAG('S06b', 0.5, 'proprio', 'tears a ticket'); GAG('S06b', 0.95, 'proprio', 'coin in the pocket, smirk')
for tt in TEAR6: st.cue('sfx:paper', 'S06b', tt, 0.25)
for t0_, _ in COIN6: st.cue('sfx:kaching', 'S06b', r(t0_ + 0.24), 0.25)

# 7: « Une minuterie courte, » The first landing like a gym: a towel over the banister, a water bottle on the bottom step; the landlord shows a young couple
#    in tracksuits round, sweeping his arm at the stairs like a gym owner; they look, eyebrows up
D7 = st.dur('S07')
PR7 = [2.2, FH, 0.95]; RYPR7 = -35
C71 = [3.05, FH, 0.2]; RYC71 = -45; C72 = [3.45, FH, 0.95]; RYC72 = -38
F7, L7, LN7 = FIT([4.5, FH + 1.45, 4.9], {'phead': add(PR7, [0, 2.4, 0]), 'c1head': add(C71, [0, 2.4, 0]), 'c2head': add(C72, [0, 2.3, 0]), 'towel': [1.28, FH + 0.9, 0.3], 'bottle': [1.3, FH + 0.18, 1.25], 'feet': add(C72, [0, 0, 0.2])}, margin=0.13, top=0.12, bottom=0.74)
C7 = cam(0.0, F7, add(F7, [-0.1, 0.0, -0.3]), L7, L7, lens=LN7, ease='inOut')
chk2('S07', C7, {'phead': add(PR7, [0, 2.35, 0]), 'c1head': add(C71, [0, 2.35, 0]), 'c2head': add(C72, [0, 2.25, 0]), 'towel': [1.28, FH + 0.9, 0.3], 'bottle': [1.3, FH + 0.2, 1.25]}, heads=('phead', 'c1head', 'c2head'))
SWEEP = [off(PR7, RYPR7, 0.35, -0.55, 1.75), off(PR7, RYPR7, 0.5, -0.75, 1.55)]
PK7 = [k(-0.5, look=lerp3(add(C71, [0, 1.9, 0]), F7, 0.5)), k(0.0, toon={**HAND(off(PR7, RYPR7, 0.3, -0.25, 1.2), None, 'open', 'rest'), 'face': {**PF, 'brow': 0.4, 'mouth': 'smile'}}, toonDur=0.0),
       k(0.15, toon={**HAND(SWEEP[0], None, 'spread', 'rest', hose=0.2), 'sq': [0.97, 1.04, 0.97], 'face': {**PF, 'brow': 0.6, 'mouth': 'smile'}}, toonDur=0.12),
       k(0.45, toon={**HAND(SWEEP[1], None, 'spread', 'rest', hose=0.2), 'face': {**PF, 'brow': 0.6, 'mouth': 'smile'}}, toonDur=0.25, toonEase='inOut'),
       k(0.5, look=[0.0, FH + 2.0, 1.0], lookDur=0.2), k(0.85, look='camera', lookDur=0.15),
       k(0.9, toon={**HAND(SWEEP[1], None, 'spread', 'rest', hose=0.2), 'face': {**PF, 'brow': 0.8, 'mouth': 'smile', 'lid': 0.2}}, toonDur=0.1)]
CF7 = {'lid': 0.2, 'mouth': 'o', 'brow': 0.6}
CK71 = [k(-0.5, look=[0.5, FH + 1.6, 0.9]), k(0.0, toon={'hip': 0, 'face': CF7}, toonDur=0.0), k(0.4, toon={'hip': 0, 'sq': [0.96, 1.05, 0.96], 'face': {**CF7, 'eye': 0.3, 'brow': 0.9}}, toonDur=0.08), *blink(0.85, CF7, {'hip': 0})]
CK72 = [k(-0.5, look=[0.5, FH + 1.2, 1.2]), k(0.0, toon={'hip': 0, 'face': CF7}, toonDur=0.0), k(0.5, toon={'hip': 0, 'sq': [0.96, 1.05, 0.96], 'face': {**CF7, 'eye': 0.3, 'brow': 0.9}}, toonDur=0.08), k(0.7, look='camera', lookDur=0.15)]
GYM = lambda n: [P(f'serviette{n}', 'mnTowel', pos=[1.28, FH + 0.97, 0.3], ry=90, opts={'sway': True}), P(f'gourde{n}', 'mnBottle', pos=[1.3, FH + 0.175, 1.25])]
st.shot('S07', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('proprio', PR7, RYPR7, 'stand', 'neutral', keys=PK7), act('c1', C71, RYC71, 'stand', 'neutral', keys=CK71), act('c2', C72, RYC72, 'stand', 'neutral', keys=CK72)],
        props=[WELL('7', top=2, hall=False), BTNS('7', floors=[0, 1, 2], big=False), *GYM('7')],
        cams=[C7])
GAG('S07', 0.5, 'proprio', 'shows the stairs like a gym')

# 7b: « c'est une salle de sport à domicile. » Closer: the young man steps up and down the bottom step like a step class, the young woman jogs on the spot
#     by the column, knees high; the landlord spreads both hands, « voilà »
D7b = st.dur('S07b')
C71b = [1.85, FH, 1.0]; RYC71b = -70; C72b = [2.6, FH, 0.3]; RYC72b = -25; PR7b = [3.35, FH, 0.85]; RYPR7b = -50
F7b, L7b, LN7b = FIT([3.6, FH + 1.35, 4.6], {'c1': add(C71b, [0, 2.6, 0]), 'c2': add(C72b, [0, 2.5, 0]), 'p': add(PR7b, [0, 2.4, 0]), 'c1f': add(C71b, [-0.5, 0, 0]), 'step': [1.0, FH + 0.2, 1.3]}, margin=0.13, top=0.12, bottom=0.74)
C7b = cam(0.0, F7b, add(F7b, [-0.2, 0.0, -0.2]), L7b, L7b, lens=LN7b, ease='inOut')
chk2('S07b', C7b, {'c1': add(C71b, [0, 2.5, 0]), 'c2': add(C72b, [0, 2.45, 0]), 'p': add(PR7b, [0, 2.35, 0])}, heads=('c1', 'c2', 'p'))
STEPUP = [1.22, FH + 0.175, 1.0]
CK71b = [k(-0.5, look='camera')]
for j in range(3):
    t_ = r(0.05 + 0.48 * j)
    CK71b += [k(t_, to=STEPUP, dur=0.16, ease='out', glide=True, face=RYC71b), k(t_, toon={'hip': 0, 'sq': [0.93, 1.1, 0.93], 'bend': {'legR': [-0.8, 0, 0, 1, None], 'shinR': [0.9, 0, 0, 1, None]}, 'face': {**CF7, 'mouth': 'smile'}}, toonDur=0.06),
              k(r(t_ + 0.22), to=C71b, dur=0.16, ease='in', glide=True, face=RYC71b), k(r(t_ + 0.22), toon={'hip': 0, 'sq': [1.06, 0.95, 1.06], 'face': {**CF7, 'mouth': 'smile'}}, toonDur=0.06)]
CK72b = [k(-0.5, look='camera')]
for j in range(7):
    t_ = r(0.03 + 0.21 * j); sd = 'L' if j % 2 == 0 else 'R'
    CK72b.append(k(t_, toon={'hip': 0, 'sq': [0.97, 1.04, 0.97], 'bend': {f'leg{sd}': [-1.2, 0, 0, 1, None], f'shin{sd}': [1.3, 0, 0, 1, None], 'armL': [0.6 if sd == 'L' else -0.6, 0, 0, 1, None], 'armR': [-0.6 if sd == 'L' else 0.6, 0, 0, 1, None]}, 'face': {**CF7, 'mouth': 'smile', 'lid': 0.0}}, toonDur=0.08))
PK7b = [k(-0.5, look='camera'), k(0.0, toon={**HAND(off(PR7b, RYPR7b, 0.3, 0.25, 1.2), off(PR7b, RYPR7b, 0.3, -0.25, 1.2), 'open', 'open'), 'face': {**PF, 'brow': 0.5, 'mouth': 'smile'}}, toonDur=0.0),
        k(0.55, toon={**HAND(off(PR7b, RYPR7b, 0.35, 0.6, 1.55), off(PR7b, RYPR7b, 0.35, -0.6, 1.55), 'spread', 'spread', hose=0.2), 'sq': [0.95, 1.06, 0.95], 'face': {**PF, 'brow': 0.9, 'mouth': 'bigsmile', 'lid': 0.0}}, toonDur=0.1, toonEase='outBack'),
        *blink(1.2, {**PF, 'brow': 0.9, 'mouth': 'bigsmile'}, HAND(off(PR7b, RYPR7b, 0.35, 0.6, 1.55), off(PR7b, RYPR7b, 0.35, -0.6, 1.55), 'spread', 'spread', hose=0.2))]
st.shot('S07b', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('c1', C71b, RYC71b, 'stand', 'neutral', keys=CK71b), act('c2', C72b, RYC72b, 'stand', 'neutral', keys=CK72b), act('proprio', PR7b, RYPR7b, 'stand', 'neutral', keys=PK7b)],
        props=[WELL('7b', top=2, hall=False), BTNS('7b', floors=[0, 1, 2], big=False), *GYM('7b')],
        cams=[C7b])
GAG('S07b', 0.6, 'proprio', 'voilà'); GAG('S07b', 0.3, 'c1', 'step class on the stairs')
for j in range(3): st.cue('sfx:step', 'S07b', r(0.2 + 0.48 * j), 0.2)

# 7c: « Les loyers ont doublé. » Low on the doormat of the flat for rent: a stack of plain gold coins on it; the landlord's hand sets a second stack beside it,
#     coin by coin; the couple gasp, mouths open like letterboxes
D7c = st.dur('S07c'); DOUB7 = W('S07c', 'L07', 13)
DM = [DOORX, FH, -1.12]; S1 = [2.66, FH + 0.034, -1.12]; S2 = [3.14, FH + 0.034, -1.12]
C71c = [1.9, FH, -0.55]; RYC71c = 35; C72c = [2.4, FH, -0.1]; RYC72c = 15; PR7c = [3.85, FH, -0.55]; RYPR7c = -105
F7c, L7c, LN7c = FIT([2.75, FH + 0.85, 2.4], {'c1': add(C71c, [0, 2.5, 0]), 'c2': add(C72c, [0, 2.45, 0]), 's1': S1, 's2': S2, 'mat': add(DM, [0, 0, 0.3]), 'phand': [3.3, FH + 1.0, -0.9]}, margin=0.1, top=0.12, bottom=0.74)
C7c = cam(0.0, F7c, add(F7c, [0.0, -0.05, -0.2]), L7c, L7c, lens=LN7c, ease='inOut')
chk2('S07c', C7c, {'c1': add(C71c, [0, 2.4, 0]), 'c2': add(C72c, [0, 2.4, 0]), 's1': S1, 's2': S2}, heads=('c1', 'c2'))
SET7 = 0.3
PK7c = [k(-0.5, look=S2), k(0.0, toon={**HAND(add(S2, [0.05, 0.45, 0.1]), None, 'pinch', 'rest'), 'bend': {'spine': [0.55, 0, 0, 1, None]}, 'face': PF}, toonDur=0.0),
        k(SET7, toon={**HAND(add(S2, [0.0, 0.22, 0.05]), None, 'pinch', 'rest'), 'bend': {'spine': [0.6, 0, 0, 1, None]}, 'face': PF}, toonDur=0.15),
        k(r(SET7 + 0.35), toon={**HAND(add(S2, [0.1, 0.5, 0.2]), None, 'open', 'rest'), 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {**PF, 'mouth': 'smirk'}}, toonDur=0.2)]
GASP = {'lid': 0.0, 'mouth': 'open', 'mouthW': 0.55, 'mouthH': -0.25, 'jaw': 0.35, 'eye': 0.45, 'brow': 1.0, 'gy': 0.5}
def GASPK(t0_, look_pt):
    return [k(-0.5, look=look_pt), k(0.0, toon={'hip': 0, 'face': {**CF7, 'gy': 0.5}}, toonDur=0.0),
            k(r(t0_ - 0.06), toon={'hip': 0, 'sq': [1.05, 0.95, 1.05], 'face': {**CF7, 'gy': 0.5}}, toonDur=0.05),
            k(t0_, toon={'hip': 0, 'sq': [0.9, 1.14, 0.9], 'hairUp': 0.6, 'face': GASP}, toonDur=0.05, toonEase='outBack'),
            k(r(t0_ + 0.35), toon={'hip': 0, 'sq': [0.96, 1.05, 0.96], 'hairUp': 0.3, 'face': {**GASP, 'gy': 0.0}}, toonDur=0.1), k(r(t0_ + 0.35), look='camera', lookDur=0.1)]
st.shot('S07c', SET, setOpts=SETO, look=LOOK_IN,
        actors=[act('c1', C71c, RYC71c, 'stand', 'neutral', keys=GASPK(r(DOUB7 + 0.02), lerp3(S1, F7c, 0.45))), act('c2', C72c, RYC72c, 'stand', 'neutral', keys=GASPK(r(DOUB7 + 0.08), lerp3(S2, F7c, 0.45))),
                act('proprio', PR7c, RYPR7c, 'stand', 'neutral', keys=PK7c)],
        props=[WELL('7c', top=2, hall=False), BTNS('7c', floors=[1, 2], big=False), P('paillasson7c', 'mnDoormat', pos=DM),
               P('tas7c1', 'mnCoins', pos=S1, opts={'n': 7}), P('tas7c2', 'mnCoins', pos=S2, opts={'n': 7, 'count': [[0, 0]] + [[r(SET7 + 0.05 * i), i + 1] for i in range(7)]})],
        cams=[C7c])
GAG('S07c', r(DOUB7 + 0.1), 'c1', 'gasp'); st.text('S07c', 0.8, 'tas7c2', 'two stacks')
for i in range(7): st.cue('sfx:clink', 'S07c', r(SET7 + 0.05 * i), 0.1)
st.cue('sfx:gasp', 'S07c', DOUB7, 0.3)
